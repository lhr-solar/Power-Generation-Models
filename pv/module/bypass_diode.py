"""
@file       bypass_diode.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Model interface for a Bypass diode.
@version    0.4.0
@date       2023-09-24
"""
import math as m

from scipy import constants

from pv.pv import PV


class BypassDiode(PV):
    def __init__(self, params: dict, data_fp=None) -> None:
        super().__init__(params, data_fp)

    def get_voltage(
        self, current: float, irrad: list[float], temp: list[float]
    ) -> float:
        irrad = irrad[0]
        temp = temp[0]

        if temp == 0.0:
            raise Exception("Cell temperature is too low!")

        # Curve Fitting parameters
        fit_n = self._params["fit_ideality_factor"]
        fit_i_d = self._params["fit_rev_sat_current"]

        i_d = current
        t_d = temp

        k_b = constants.k
        q = constants.e

        v_t = k_b * t_d / q

        if i_d > 0:
            v_d = m.log(i_d / fit_i_d + 1) * fit_n * v_t
        else:
            v_d = 0.0

        return v_d

    def get_current(
        self, voltage: float, irrad: list[float], temp: list[float]
    ) -> float:
        irrad = irrad[0]
        temp = temp[0]

        if temp == 0.0:
            raise Exception("Cell temperature is too low!")

        # Curve Fitting parameters
        fit_n = self._params["fit_ideality_factor"]
        fit_i_d = self._params["fit_rev_sat_current"]

        v_d = voltage
        t_d = temp

        k_b = constants.k
        q = constants.e

        v_t = k_b * t_d / q

        if v_d >= 0:
            i_d = fit_i_d * (m.exp(v_d / (fit_n * v_t)) - 1)
        else:
            i_d = 0.0

        return i_d
