"""
@file       module.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Model interface for a PV module.
@version    0.4.0
@date       2023-09-24
"""

from pv.pv import PV


class Module(PV):
    def __init__(self, params: dict, data_fp=None) -> None:
        super().__init__( params, data_fp)

    def get_voltage(self, current: float, irrad: list[float], temp: list[float]) -> float:
        v = 0.0
        for cell, irrad, temp in zip(self._params["cells"].values(), irrad, temp):
            v += cell["instance"].get_voltage(current, [irrad], [temp])

        # TODO: diode contribution

        return v

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


