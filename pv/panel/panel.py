"""
@file       panel.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Model interface for a PV panel.
@version    0.4.0
@date       2023-09-24
"""

import numpy as np

from pv.pv import PV


class Panel(PV):
    def __init__(self, params: dict, data_fp=None) -> None:
        super().__init__(params, data_fp)

    def get_voltage(
        self, current: float, irrad: list[float], temp: list[float]
    ) -> float:
        v = 0.0
        for module in self._params["modules"].values():
            num_cells = len(module["instance"].get_pos())
            v += module["instance"].get_voltage(
                current, irrad[:num_cells], temp[:num_cells]
            )
            irrad = irrad[num_cells:]
            temp = temp[num_cells:]

        # lead contribution
        v -= current * self._params["fit_lead_resistance"]

        return v

    def get_current(
        self, voltage: float, irrad: list[float], temp: list[float]
    ) -> float:
        # Cheat and grab from IV curve. Current from voltage can be derived in
        # O(N), while voltage directly is O(N^N).
        iv = self.get_iv(irrad, temp)
        volt, curr, _ = np.transpose(iv)
        curr = np.interp(voltage, volt, curr)

        # Lead contribution derived from get_voltage downstream call.
        return curr

    def get_pos(self) -> list([int, int]):
        pos = []
        for module in self._params["modules"].values():
            module_pos = [
                [module["pos"][0] + x, module["pos"][1] + y]
                for x, y in module["instance"].get_pos()
            ]
            pos.extend(module_pos)

        return pos
