"""
@file       bypass_diode.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Model interface for a Bypass diode.
@version    0.4.0
@date       2023-09-24
"""
import sys

sys.path.extend([".", "..", "../.."])

from environment.environment import Environment
from pvs.pv_interface import PVInterface


class BypassDiode(PVInterface):
    def __init__(self, env: Environment, params: dict, data_fp=None) -> None:
        super().__init__(env, params, data_fp)

    def get_current(self, voltage: float, root_pos: (int, int, int)) -> float:
        # If a cell is forward biased, then this diode is reverse biased:
        # - there is a reverse quiescient current through the diode
        # If a cell is reverse biased, then this diode is forward biased:
        # - there is a forward voltage drop across the diode
        # - the current flowing through this cell is dependent on this forward
        #   voltage drop.
        # There is also some dependency on temperature. This model may or may
        # not include self heating effects.

        return 0.0
