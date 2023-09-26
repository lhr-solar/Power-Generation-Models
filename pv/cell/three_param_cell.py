"""
@file       three_param_cell.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Model for a Three parameter PV cell.
@version    0.4.0
@date       2023-09-24
"""
from pv.cell.c.three_param_cell import get_voltage
from pv.cell.cell import Cell


class ThreeParamCell(Cell):
    def __init__(self, params: dict, data_fp=None) -> None:
        super().__init__(params=params, data_fp=data_fp)

    def get_voltage(self, current: float, irrad: list[float], temp: list[float]) -> float:
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
        t = temp
        return get_voltage(ref_g, ref_v_oc, ref_i_sc, fit_n, i_l, g, t)

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
