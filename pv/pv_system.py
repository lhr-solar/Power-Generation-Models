"""
@file       pv_system.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Models the photovoltaic system.
@version    0.4.0
@date       2023-09-28
"""

from pv.pv import PV
from environment.environment import Environment
import numpy as np
import pandas as pd
from common.utils import normalize
from PySide6 import QtWidgets
from common.graph import Graph
import sys
import math as m


class PVSystem:
    """Models the entire system in the solar deployment. Can be moved around in
    the environment."""

    def __init__(self, env: Environment, filepath: str = None) -> None:
        """Initialize a new PVSystem instance.

        Args:
            env (Environment): Environment to provide irradiance and temp data.
            filepath (str, optional): Filepath for photovoltaic data file.
                Defaults to None.
        """
        if filepath != None:
            self._items = self.load_pv(filepath)
        else:
            self._items = {}

        self._env = env
        self._pos = [0, 0]

    def load_pv(self, filepath: str) -> dict:
        """TODO: Load from a photovoltaic file that represents the PVSystem.

        Args:
            filepath (str): Path of file to load.

        Returns:
            dict: Dict of PV instance in system.
        """
        raise NotImplementedError

    def save_pv(self, filepath: str) -> None:
        """TODO: Save into a photovoltaic file that represents the PVSystem.

        Args:
            filepath (str): Path of file to save/overwrite.
        """
        raise NotImplementedError

    def add_pv(self, id: int, item: PV, X: int, Y: int) -> None:
        """Add a pv instance to the system.

        Args:
            id (int): Unique ID of PV instance.
            pv (PV): PV instance to add.
            X (int): X position of PV relative to the canvas.
            Y (int): Y position of the PV relative to the canvas.
        """
        if id in self._items:
            raise Exception("ID already exists in system.")

        pos = [(a + X, b + Y) for a, b in item.get_pos()]
        for other_item in self._items.values():
            other_pos = [
                (a + other_item["pos"][0], b + other_item["pos"][1])
                for a, b in other_item["instance"].get_pos()
            ]
            if set(pos).intersection(other_pos):
                raise Exception("Overlap with another PV.")

        self._items[id] = {"instance": item, "pos": (X, Y)}

    def rem_pv(self, id: int) -> PV:
        """Remove a pv instance from the model.

        Args:
            id (int): Unique ID of PV instance.

        Returns:
            PV: PV instance.
        """
        if id not in self._items:
            return Exception("ID does not exist in system.")

        return self._items.pop(id)

    def _get_pv_env(self, id: int, time: int) -> (list[float], list[float]):
        """Get the irrad and temp for a particular PV item.

        Args:
            id (int): PV Item ID.

        Returns:
            (list[float], list[float]): Tuple of irradiance and temperature
                points.
        """
        pos = [
            [self._items[id]["pos"][0] + x, self._items[id]["pos"][1] + y]
            for x, y in self._items[id]["instance"].get_pos()
        ]

        irrad = []
        temp = []
        for p in pos:
            g, t = self._env.get_voxel(*p, time)
            irrad.append(g)
            temp.append(t)

        return irrad, temp

    def get_pv_voltage(self, id: int, current: float, time: int) -> float:
        """Get the voltage generated by the PV as a function of the current
        applied through the PV and external environment and internal cell
        characteristics.

        Args:
            id (int): ID of PV to query.
            current (float): Current through PV. Amps.
            time (int): Time idx of environment to query.

        Returns:
            float: Voltage across PV. Volts.
        """
        if id not in self._items:
            return Exception("ID does not exist in system.")

        return self._items[id]["instance"].get_voltage(
            current, *self._get_pv_env(id, time)
        )
    
    def get_pv_current(self, id: int, voltage: float, time: int) -> float:
        """Get the current generated by the PV as a function of the voltage
        applied across the PV and external environment and internal cell
        characteristics.

        Args:
            id (int): ID of PV to query.
            voltage (float): Voltage across PV. Volts.
            time (int): Time idx of environment to query.

        Returns:
            float: Current through PV. Amps.
        """
        if id not in self._items:
            return Exception("ID does not exist in system.")

        # Cheat and grab from IV curve. Current from voltage can be derived in
        # O(N), while voltage directly is O(N^N).
        iv = self.get_pv_iv(id, time)
        volt, curr, _ = np.transpose(iv)
        curr = np.interp(voltage, volt, curr)

        return curr


    def get_pv_iv(self, id: int, time: int) -> [(float, float)]:
        """Get the output I-V curve of a specific item in the model.

        Args:
            id (int): ID of PV to query.
            time (int): Time idx of environment to query.

        Returns:
            [(float, float, float)]: List of voltage-current-power pairs.
            Ordered.
        """
        if id not in self._items:
            return Exception("ID does not exist in system.")

        return self._items[id]["instance"].get_iv(*self._get_pv_env(id, time))

    def get_pv_edge(
        self, id: int, time: int
    ) -> ((float, float), (float, float), float):
        """Get the 1st power quadrant edge characteristics of the pv.

        Args:
            id (int): ID of PV to query.
            time (int): Time idx of environment to query.

        Returns:
            (float, float), (float, float):
                Open circuit voltage (Volts)
                Short circuit current (Amps)
                Maximum power point voltage (Volts)
                Maximum power point current (Amps)
        """
        if id not in self._items:
            return Exception("ID does not exist in system.")

        return self._items[id]["instance"].get_edge(*self._get_pv_env(id, time))

    def vis_pv(self, id: int, time: int) -> None:
        """Visualize a PV instance at a point in time.

        Args:
            id (int): ID of PV to query.
            time (int): Time idx of environment to query.
        """
        if id not in self._items:
            return Exception("ID does not exist in system.")

        return self._items[id]["instance"].vis(*self._get_pv_env(id, time))

    def set_sys_pos(self, X: int, Y: int) -> None:
        """Set the origin position of the entire PVSystem.

        Args:
            self (Photovoltaic): Photovoltaic instance.
            X (int): New origin X position.
            Y (int): New origin Y position.
        """
        self._pos = [X, Y]

    def get_sys_voltage(self, current: float, time: int) -> float:
        """Get the voltage generated by the entire system as a function of the
        current applied through the system and external environment and internal
        cell characteristics.

        Args:
            current (float): Current through the PV. Amps.
            time (int): Time idx of environment to query.

        Returns:
            float: Voltage across system. Volts.
        """
        pos = []
        for item in self._items.values():
            item_pos = [
                [self._pos[0] + item["pos"][0] + x, self._pos[1] + item["pos"][1] + y]
                for x, y in item["instance"].get_pos()
            ]
            pos.extend(item_pos)

        irrad = []
        temp = []
        for p in pos:
            g, t = self._env.get_voxel(*p, time)
            irrad.append(g)
            temp.append(t)

        v = 0.0
        for item in self._items.values():
            num_cells = len(item["instance"].get_pos())
            v += item["instance"].get_voltage(
                current, irrad[:num_cells], temp[:num_cells]
            )
            irrad = irrad[num_cells:]
            temp = temp[num_cells:]

        return v

    def get_sys_iv(self, time: int) -> [(float, float)]:
        """Get the output I-V curve of the system.

        Args:
            time (int): Time idx of environment to query.

        Returns:
            [(float, float, float)]: List of voltage-current-power pairs.
            Ordered.
        """
        iv = []

        curr = 0.0
        res = 0.1
        loop = 0
        num_loops = 3
        while loop < num_loops:
            # Increment resolution decreases by (0.05)^n
            curr += res
            volt = self.get_sys_voltage(curr, time)
            iv.append([volt, curr, volt * curr])
            if volt == 0.0:
                # https://www.desmos.com/calculator/mffm3b9ucm
                # Set x=num_loops and adjust a, b, z to meet requirements
                # - z: I_SC of typical cell
                # - a: Starting proportion of Z, set to right side of knee of
                #   typical I-V curve
                # - b: Adjust such that at X=num_loops the curve is barely under
                #   it (<0.1).
                new_curr = curr * (0.5 + m.log(loop + 1) * 0.45)
                res = res / 3
                curr = new_curr
                loop += 1

        # Normalize data.
        iv = normalize(np.array(iv))

        return iv

    def get_sys_edge(self, time: int) -> ((float, float), (float, float), float):
        """Get the 1st power quadrant edge characteristics of the system.

        Args:
            time (int): Time idx of environment to query.

        Returns:
            (float, float), (float, float):
                Open circuit voltage (Volts)
                Short circuit current (Amps)
                Maximum power point voltage (Volts)
                Maximum power point current (Amps)
        """
        iv = self.get_sys_iv(time)
        df = pd.DataFrame(iv, columns=["Voltage (V)", "Current (A)", "Power (W)"])

        v_oc = df.nlargest(1, "Voltage (V)").iloc[0]["Voltage (V)"]
        i_sc = df.nlargest(1, "Current (A)").iloc[0]["Current (A)"]

        mpp = df.nlargest(1, "Power (W)")
        v_mpp = mpp.iloc[0]["Voltage (V)"]
        i_mpp = mpp.iloc[0]["Current (A)"]

        return (v_oc, i_sc), (v_mpp, i_mpp)

    def vis_pv(self, time: int) -> None:
        """Visualize the system at a point in time.

        Args:
            time (int): Time idx of environment to query.
        """
        if not QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()

        container = QtWidgets.QWidget()
        container_layout = QtWidgets.QGridLayout()
        container.setLayout(container_layout)

        # Create graphs
        data = self.get_sys_iv(time)
        data = np.transpose(data)

        # Populate graph
        graph = {
            "instance": Graph(
                "I-V/P-V Curve",
                "Voltage (V)",
                "Current (A)",
            ),
            "title": "I-V/P-V Curve",
            "widget": None,
            "position": [0, 0],
        }
        graph["instance"].add_series(
            {
                "iv": {"x": data[0], "y": data[1], "color": (255, 0, 0, 255)},
                "pv": {"x": data[0], "y": data[2], "color": (0, 255, 0, 255)},
            },
            "scatter",
        )
        graph["widget"] = graph["instance"].get_graph()
        # graph["instance"].set_graph_range([0, 0.8], [0, 6.5])

        container_layout.addWidget(graph["widget"], *graph["position"])

        win = QtWidgets.QMainWindow()
        win.setGeometry(0, 0, 720, 480)
        win.setWindowTitle(f"I-V/P-V Curve")
        win.setCentralWidget(container)

        win.show()
        exe = app.exec()
