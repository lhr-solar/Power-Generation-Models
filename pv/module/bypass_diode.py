"""
@file       bypass_diode.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Model interface for a Bypass diode.
@version    0.4.0
@date       2023-09-24
"""
import math as m
import numpy as np

from scipy import constants

from common.utils import normalize
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
        fit_i_d = self._params["fit_rev_sat_curr"]

        i_d = current
        t_d = temp

        k_b = constants.k
        q = constants.e

        v_t = k_b * t_d / q

        if i_d >= 0:
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
        fit_i_d = self._params["fit_rev_sat_curr"]

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

    def get_iv(
        self,
        irrad: list[float],
        temp: list[float],
        curr_range: list[float] = [-10.0, 10.0],
        volt_range: list[float] = [-10.0, 10.0],
    ) -> list[list[float, float, float]]:
        def calc(volt):
            curr = self.get_current(volt, irrad, temp)
            return volt, curr, volt * curr

        iv = [calc(volt) for volt in np.linspace(*volt_range, self.IV_POINTS)]

        # Normalize data.
        iv = normalize(np.array(iv), self.IV_NORM_POINTS)
        return iv

    def fit_params(self, irradiance: float = None, temperature: float = None) -> dict:
        """
        Curve fitting parameters
        - temperature
        - fit_ideality_factor
        - fit_rev_sat_curr
        """
        fitting_parameters = {
            "temperature": {
                "min": 273.15,  # 0 C
                "stc": 298.15,  # 25 C
                "max": 398.15,  # 125 C
                "val": temperature,
                "given": temperature is not None,
            },
            "fit_ideality_factor": {
                "min": 0.1,
                "stc": 1.42,
                "max": 100,
                "given": False,
            },
            "fit_rev_sat_curr": {
                "min": 1 * 10**-25,
                "stc": 2 * 10**-4,
                "max": 1 * 10**-3,
                "given": False,
            },
        }

        data = normalize(np.array(self._data), self.IV_POINTS)
        params = self._fit_params(data, fitting_parameters, self.residual)

        for key in fitting_parameters.keys():
            if "fit" in key:
                self._params[key] = fitting_parameters[key]["val"]

        return params

    def residual(self, params, points, data=None, eps=None):
        values = params.valuesdict()
        temp = values["temperature"] * self.FIT_RESOLUTION
        self._params["fit_ideality_factor"] = (
            values["fit_ideality_factor"] * self.FIT_RESOLUTION
        )
        self._params["fit_rev_sat_curr"] = (
            values["fit_rev_sat_curr"] * self.FIT_RESOLUTION
        )

        error = [i - self.get_current(v, [0.0], [temp]) for v, i, _ in points]
        return error
