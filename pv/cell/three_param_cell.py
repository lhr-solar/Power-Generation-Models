"""
@file       three_param_cell.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Model for a Three parameter PV cell.
@version    0.4.0
@date       2023-09-28
"""
from pv.cell.cell import Cell
from scipy import constants
import math as m

class ThreeParamCell(Cell):
    def __init__(self, params: dict, data_fp=None) -> None:
        super().__init__(params=params, data_fp=data_fp)

    def get_voltage(
        self, current: float, irrad: list[float], temp: list[float]
    ) -> float:
        irrad = irrad[0]
        temp = temp[0]

        if irrad == 0.0:
            raise Exception("Incident irradiance is too low!")
        if temp == 0.0:
            raise Exception("Cell temperature is too low!")

        # Reference parameters
        ref_g = self._params["ref_irrad"]
        ref_v_oc = self._params["ref_voc"]
        ref_i_sc = self._params["ref_isc"]

        # Curve Fitting parameters
        fit_n = self._params["fit_ideality_factor"]

        if fit_n == 0.0:
            raise Exception("Cell ideality factor is too low!")

        i_l = current
        g = irrad
        t_c = temp

        k_b = constants.k
        q = constants.e

        v_t = fit_n * k_b * t_c / q
        i_sc = ref_i_sc * g / ref_g

        # Add 0.00001 for satisfying the domain condition when g/ref_g = 0.
        v_oc = ref_v_oc + v_t * m.log((g / ref_g) + 0.00001)

        if 1 - i_l / i_sc <= 0:
            # Domain assumption that our load current cannot be greater than our
            # short circuit current: this implies that the diode current is
            # negative and contributes to the system instead of taking from it.

            # Likewise, assume that our load current cannot be equal to our
            # short circuit current: this implies that there is no
            # dark/saturation diode contribution at all.
            return 0.0

        v_l = v_t * m.log((1 - i_l / i_sc) * (m.exp(v_oc / v_t) - 1))
        return v_l

        # return get_voltage(ref_g, ref_v_oc, ref_i_sc, fit_n, i_l, g, t)

    def get_current(
        self, voltage: float, irrad: list[float], temp: list[float]
    ) -> float:
        irrad = irrad[0]
        temp = temp[0]

        if irrad == 0.0:
            raise Exception("Incident irradiance is too low!")
        if temp == 0.0:
            raise Exception("Cell temperature is too low!")

        # Reference parameters
        ref_g = self._params["ref_irrad"]
        ref_v_oc = self._params["ref_voc"]
        ref_i_sc = self._params["ref_isc"]

        # Curve Fitting parameters
        fit_n = self._params["fit_ideality_factor"]

        if fit_n == 0.0:
            raise Exception("Cell ideality factor is too low!")

        v_l = voltage
        g = irrad
        t_c = temp

        k_b = constants.k
        q = constants.e

        v_t = fit_n * k_b * t_c / q
        i_sc = ref_i_sc * g / ref_g

        # Add 0.00001 for satisfying the domain condition when g/ref_g = 0.
        v_oc = ref_v_oc + v_t * m.log((g / ref_g) + 0.00001)

        if v_l / v_t > 100:
            # Domain assumption that our load voltage cannot be well past open
            # circuit voltage: the ratio of load voltage versus thermal voltage
            # can overfill the exponential term.
            return 0.0
        
        i_l = i_sc * (1 - (m.exp(v_l / v_t) - 1) / (m.exp(v_oc / v_t) - 1))
        return i_l

    def fit_parameters(
        self, irradiance: float = None, temperature: float = None
    ) -> dict:
        fitting_parameters = {
            "irradiance": {
                "min": 100,
                "stc": 1000,
                "max": 1100,
                "val": irradiance,
                "given": irradiance is not None,
            },
            "temperature": {
                "min": 273.15,
                "stc": 298.15,
                "max": 398.15,
                "val": temperature,
                "given": temperature is not None,
            },
            "ideality_factor": {
                "min": 1.0,
                "stc": 2.0,
                "max": 2.5,
                "val": 2.0,
                "given": False,
            },
        }

        # TODO: Execute fitting function.
        # data = self._normalize_data(data)
        # self._set_params_and_fit(self._data, fitting_parameters)

        return fitting_parameters
