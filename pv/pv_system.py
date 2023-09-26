"""
@file       pv_system.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Models the photovoltaic system.
@version    0.4.0
@date       2023-09-24
"""

from pv.pv import PV


class PVSystem:
    """Models the entire system in the solar deployment. Can be moved around in
    the environment."""

    def __init__(self, filepath: str = None) -> None:
        """Initialize a new PVSystem instance.

        Args:
            filepath (str, optional): Filepath for photovoltaic data file.
                Defaults to None.
        """
        if filepath != None:
            self._items = self.load_pv(filepath)
        else:
            self._items = {}

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
                for a, b in other_item["item"].get_pos()
            ]
            if set(pos).intersection(other_pos):
                raise Exception("Overlap with another PV.")

        self._items[id] = {"item": item, "pos": (X, Y)}

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

    def get_pv_voltage(self, id: int, current: float, time: int) -> float:
        """Get the voltage generated by the PV as a function of the current
        applied across the PV and external environment and internal cell
        characteristics.

        Args:
            id (int): ID of PV to query.
            current (float): Current across PV. Amps.
            time (int): Time idx of environment to query.

        Returns:
            float: Voltage from PV. Volts.
        """
        if id not in self._items:
            return Exception("ID does not exist in system.")

        return self._items[id]["item"].get_voltage(
            current,
            (
                self._pos[0] + self._items[id]["pos"][0],
                self._pos[1] + self._items[id]["pos"][1],
                time,
            ),
        )

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

        return self._items[id]["item"].get_iv(
            (
                self._pos[0] + self._items[id]["pos"][0],
                self._pos[1] + self._items[id]["pos"][1],
                time,
            )
        )

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

        return self._items[id]["item"].get_edge(
            (
                self._pos[0] + self._items[id]["pos"][0],
                self._pos[1] + self._items[id]["pos"][1],
                time,
            )
        )

    def vis_pv(self, id: int, time: int) -> None:
        """Visualize a PV instance at a point in time.

        Args:
            id (int): ID of PV to query.
            time (int): Time idx of environment to query.
        """
        if id not in self._items:
            return Exception("ID does not exist in system.")

        return self._items[id]["item"].vis(
            (
                [
                    self._pos[0] + self._items[id]["pos"][0],
                    self._pos[1] + self._items[id]["pos"][1],
                    time,
                ],
            )
        )

    def set_sys_pos(self, X: int, Y: int) -> None:
        """Set the origin position of the entire PVSystem.

        Args:
            self (Photovoltaic): Photovoltaic instance.
            X (int): New origin X position.
            Y (int): New origin Y position.
        """
        self._pos = [X, Y]