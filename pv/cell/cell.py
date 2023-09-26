"""
@file       cell.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Model interface for a PV cell.
@version    0.4.0
@date       2023-09-24
"""
from pv.pv import PV


class Cell(PV):
    def __init__(self, params: dict, data_fp=None) -> None:
        super().__init__(params, data_fp)

    def get_pos(self) -> list[list[int, int]]:
        return [[0, 0]]
