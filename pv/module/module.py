"""
@file       module.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Model interface for a PV module.
@version    0.4.0
@date       2023-09-28
"""

from pv.pv import PV
import numpy as np


class Module(PV):
    def __init__(self, params: dict, data_fp=None) -> None:
        super().__init__(params, data_fp)

    def get_voltage(
        self, current: float, irrad: list[float], temp: list[float]
    ) -> float:
        volt = 0.0
        for cell, irrad, temp in zip(self._params["cells"].values(), irrad, temp):
            volt += cell["instance"].get_voltage(current, [irrad], [temp])

        # TODO: diode contribution.

        return volt
    
    def get_current(
        self, voltage: float, irrad: list[float], temp: list[float]
    ) -> float:
        # Cheat and grab from IV curve. Current from voltage can be derived in
        # O(N), while voltage directly is O(N^N).
        iv = self.get_iv(irrad, temp)
        volt, curr, _ = np.transpose(iv)
        curr = np.interp(voltage, volt, curr)

        # TODO: diode contribution.

        return curr

    def get_pos(self) -> list([int, int]):
        pos = []
        for cell in self._params["cells"].values():
            cell_pos = [
                [cell["pos"][0] + x, cell["pos"][1] + y]
                for x, y in cell["instance"].get_pos()
            ]
            pos.extend(cell_pos)

        return pos

    def fit_parameters(
        self, irradiance: float = None, temperature: float = None
    ) -> dict:
        raise NotImplementedError
