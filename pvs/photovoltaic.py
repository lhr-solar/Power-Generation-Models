"""
@file       photovoltaic.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Models the photovoltaic system.
@version    0.4.0
@date       2023-09-22
"""
import sys

sys.path.extend(["."])
sys.path.extend([".."])

import pandas as pd
import common.config as CONFIG
from environment.environment import Environment
from cell.cell import Cell
from module.module import Module
from panel.panel import Panel
    

class Photovoltaic:
    """Photovoltaic class models power generation elements in the system."""

    def __init__(self, filepath: str = None, hierarchy: str = "Cell") -> None:
        """Initialize a new photovoltaic instance.

        Args:
            self (Photovoltaic): Photovoltaic instance.
            filepath (str, optional): Filepath for photovoltaic data file.
                Defaults to None.
            hierarchy (str, optional): Hierarchy of photovoltaic system. "Cell",
                "Module", or "Panel". Defaults to "Cell".
        """
        if filepath != None:
            self._items, self._hierarchy = self.load_pv(filepath)
        else:
            self._items = {}
            self._hierarchy = hierarchy

        self._pos = [0, 0]

    def load_pv(self, filepath: str) -> (dict, str):
        """TODO: Load from a photovoltaic file that represents a complete or
        incomplete set of photovoltaics.

        Args:
            self (Photovoltaic): Photovoltaic instance.
            filepath (str): Path of file to load.

        Returns:
            (dict, str): Dict of items, hierarchy of system.
        """
        return {}, "CELL"

    def save_pv(self, filepath: str) -> None:
        """TODO: Save into a photovoltaic file that represents a complete or
        incomplete set of photovoltaics.

        Args:
            self (Photovoltaic): Photovoltaic instance.
            filepath (str): Path of file to save/overwrite.
        """
        return

    def add_item(self, id: int, item: Cell | Module | Panel, X: int, Y: int) -> bool:
        """Add an item to our current photovoltaic model. Failure if the model
        hierarchy level does not match the item added.

        Args:
            self (Photovoltaic): Photovoltaic instance.
            id (int): Unique ID of cell.
            item (Cell | Module | Panel): Item instance to add.
            X (int): X position of item relative to the canvas.
            Y (int): Y position of the item relative to the canvas.

        Returns:
            bool: True if item can be added. False otherwise.
        """
        if self._hierarchy != item.__class__.__name__:
            return False
        if id in self._items:
            return False

        # TODO: check against all other item positions
        is_overlap = False
        if is_overlap:
            return False

        self._items[id] = {"item": item, "pos": (X, Y)}
        return True

    def rem_item(self, id: int) -> bool:
        """Remove an item from the model.

        Args:
            self (Photovoltaic): Photovoltaic instance.
            id (int): Unique ID of item.

        Returns:
            bool: True if removed properly, False otherwise.
        """
        if id not in self._items:
            return False

        del self._items[id]
        return True

    def get_item(self, id: int) -> Cell | Module | Panel:
        """Get an item from the model.

        Args:
            self (Photovoltaic): Photovoltaic instance.
            id (int): Id of item to grab.

        Returns:
            Cell | Module | Panel: Item, may be of Cell, Module, Panel type.
        """
        return self._items[id]

    def set_item_position(self, id: int, X: int, Y: int) -> bool:
        """Update the position of a specific item in the model. Failure if item
        overlaps with another.

        Args:
            self (Photovoltaic): Photovoltaic instance.
            id (int): Unique item ID to move.
            X (int): New X origin point.
            Y (int): New Y origin point.

        Returns:
            bool: True if item is moved successfully.
        """
        if id not in self._items:
            return False

        # TODO: check if item position overlaps with another item.
        self._items[id]["pos"] = (X, Y)
        return True

    def get_pv(self) -> dict:
        """Get model.

        Returns:
            self (Photovoltaic): Photovoltaic instance.
            dict: Model of PV.
        """
        return self._items

    def set_pv_position(self, X: int, Y: int) -> None:
        """Set the origin position of the entire PV.

        Args:
            self (Photovoltaic): Photovoltaic instance.
            X (int): New origin X position.
            Y (int): New origin Y position.
        """
        self._pos = (X, Y)

    def get_item_current(
        self, id: int, item_voltage: float, env: Environment, time: int
    ) -> float:
        """Get the output current of a specific item in the model.

        Args:
            self (Photovoltaic): Photovoltaic instance.
            id (int): Unique item ID to query.
            item_voltage (float): Voltage across the particular item.
            env (Environment): Environment to generate item inputs for.
            time (int): Time of measurement.

        Returns:
            float: Output current, in A.
        """
        # TODO: check if ID exists.
        # TODO: check if environment exists.
        # TODO: generate set of X, Y points to measure.
        # TODO: measure from environment and capture inputs
        # TODO: input into models and return result.
        return 0.0

    def get_item_iv(self, id: int, env: Environment, time: int) -> [(float, float)]:
        """Get the output I-V curve of a specific item in the model.

        Args:
            self (Photovoltaic): Photovoltaic instance.
            id (int): Unique item ID to query.
            env (Environment): Environment to generate item inputs for.
            time (int): Time of measurement.

        Returns:
            [(float, float)]: List of voltage current pairs across some voltage
            range. Volts and Amps.
        """
        return [[0.0], [0.0]]

    def get_item_edge(
        self, id: int, env: Environment, time: int
    ) -> ((float, float), (float, float), float):
        """Get the edge characteristics (V_OC, I_SC, V_MPP, I_MPP, FF) of a
        specific item in the model.

        Args:
            self (Photovoltaic): Photovoltaic instance.
            id (int): Unique item ID to query.
            env (Environment): Environment to generate item inputs for.
            time (int): Time of measurement.

        Returns:
            ((float, float), (float, float), float): V_OC, I_SC, V_MPP, I_MPP,
            FF. V_OC, V_MPP is in volts. I_SC, I_MPP is in amps.
        """
        return (0.0, 0.0), (0.0, 0.0), 0.0

    def get_pv_current(self, pv_voltage: float, env: Environment, time: int) -> float:
        """Get the output current of the model.

        Args:
            self (Photovoltaic): Photovoltaic instance.
            pv_voltage (float): Voltage across the entire model.
            env (Environment): Environment to generate model inputs for.
            time (int): Time of measurement.

        Returns:
            float: Output current, in A.
        """
        return 0.0

    def get_pv_iv(self, env: Environment, time: int) -> [(float, float)]:
        """Get the output I-V curve of the model.

        Args:
            self (Photovoltaic): Photovoltaic instance.
            env (Environment): Environment to generate model inputs for.
            time (int): Time of measurement.

        Returns:
            [(float, float)]: List of voltage current pairs across some voltage
            range. Volts and Amps.
        """
        return [[0.0], [0.0]]

    def get_pv_edge(
        self, env: Environment, time: int
    ) -> ((float, float), (float, float), float):
        """Get the edge characteristics (V_OC, I_SC, V_MPP, I_MPP, FF) of the
        model.

        Args:
            self (Photovoltaic): Photovoltaic instance.
            env (Environment): Environment to generate model inputs for.
            time (int): Time of measurement.

        Returns:
            ((float, float), (float, float), float): V_OC, I_SC, V_MPP, I_MPP,
            FF. V_OC, V_MPP is in volts. I_SC, I_MPP is in amps.
        """
        return (0.0, 0.0), (0.0, 0.0), 0.0

    def vis_item(self, id: int, env: Environment, time_range: [int, int]) -> None:
        """Visualize an item's I-V curve in the model over time.

        Args:
            id (int): Unique item ID to query.
            env (Environment): Environment to generate item inputs for.
            time_range ([int, int]): Range of time to visualize.
        """
        return

    def vis_pv(self, env: Environment, time_range: [int, int]) -> None:
        """Visualize the model's I-V curve over time.

        Args:
            env (Environment): Environment to generate model inputs for.
            time_range ([int, int]): Range of time to visualize.
        """
        return

if __name__ == "__main__":
    pv = Photovoltaic(hierarchy="Cell")

    # Check empty pv.
    assert(not pv.get_pv())

    # Check adding an item
    assert(pv.add_item(0, Cell(), 0, 0))

    # Check adding item with same unique ID
    assert(not pv.add_item(0, Cell(), 1, 1))
    
    # Check adding item with same coordinates
    assert(not pv.add_item(1, Cell(), 0, 0))

    # Check adding item with different hierarchy
    assert(not pv.add_item(1, Module(), 1, 1))

    