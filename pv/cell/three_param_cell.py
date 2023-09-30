"""
@file       three_param_cell.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Model for a Three parameter PV cell.
@version    0.4.0
@date       2023-09-28
"""
import math as m

from scipy import constants

from pv.cell.cell import Cell


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
        fit_n1 = self._params["fit_fwd_ideality_factor"]
        fit_n2 = self._params["fit_rev_ideality_factor"]
        fit_i_d = self._params["fit_rev_sat_curr"]

        if fit_n1 == 0.0 or fit_n2 == 0.0:
            raise Exception("Cell ideality factor is too low!")

        i_l = current
        g = irrad
        t_c = temp

        k_b = constants.k
        q = constants.e

        v_t = k_b * t_c / q
        i_sc = ref_i_sc * g / ref_g

        # Add 0.00001 for satisfying the domain condition when g/ref_g = 0.
        v_oc = ref_v_oc + fit_n1 * v_t * m.log((g / ref_g) + 0.00001)

        if i_l <= i_sc - 1 * 10**-10:
            v_l = (fit_n1 * v_t) * m.log(
                (1 - i_l / i_sc) * (m.exp(v_oc / (fit_n1 * v_t)) - 1)
            )
        else:
            v_l = -m.log((i_l - i_sc) / fit_i_d + 1) * fit_n2 * v_t

        return v_l

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
        fit_n1 = self._params["fit_fwd_ideality_factor"]
        fit_n2 = self._params["fit_rev_ideality_factor"]
        fit_i_d = self._params["fit_rev_sat_curr"]

        if fit_n1 == 0.0 or fit_n2 == 0.0:
            raise Exception("Cell ideality factor is too low!")

        v_l = voltage
        g = irrad
        t_c = temp

        k_b = constants.k
        q = constants.e

        v_t = k_b * t_c / q
        i_sc = ref_i_sc * g / ref_g

        # Add 0.00001 for satisfying the domain condition when g/ref_g = 0.
        v_oc = ref_v_oc + v_t * m.log((g / ref_g) + 0.00001)

        if v_l > 0.0:
            if v_l / v_t > 100:
                # Domain assumption that our load voltage cannot be well past open
                # circuit voltage: the ratio of load voltage versus thermal voltage
                # can overfill the exponential term.
                return 0.0

            i_l = i_sc * (
                1
                - (m.exp(v_l / (fit_n1 * v_t)) - 1) / (m.exp(v_oc / (fit_n1 * v_t)) - 1)
            )
        else:
            i_l = i_sc  # fit_i_d * (m.exp(-v_l / (fit_n2 * v_t)) - 1) + i_sc

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
