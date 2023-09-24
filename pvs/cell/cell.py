"""
@file       cell.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Model interface for a PV cell.
@version    0.4.0
@date       2023-09-24
"""

import sys

sys.path.extend([".", "..", "../.."])


from environment.environment import Environment
from pvs.pv_interface import PVInterface


class Cell(PVInterface):
    k_b = 1.381e-23  # Boltzmann's constant (J/K).
    q = 1.602e-19  # Electron charge (C).

    def __init__(self, env: Environment, params: dict, data_fp=None) -> None:
        super().__init__(env, params, data_fp)

    def get_pos(self) -> list((int, int)):
        return [(0, 0)]
