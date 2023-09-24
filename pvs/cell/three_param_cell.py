"""
@file       three_param_cell.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Model for a Three parameter PV cell.
@version    0.4.0
@date       2023-09-23
"""
import sys

sys.path.extend([".", "..", "../.."])

import math as m

from pvs.cell.cell import Cell
from pvs.cell.c.three_param_cell import get_voltage
from environment.environment import Environment

class ThreeParamCell(Cell):
    def __init__(self, env: Environment, params: dict, data_fp=None) -> None:
        super().__init__(env=env, params=params, data_fp=data_fp)

    def get_voltage(self, current: float, root_pos: (int, int, int)) -> float:
        (irrad, temp) = self._env.get_voxel(*root_pos)

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


if __name__ == "__main__":
    env = Environment()
    env.add_voxel(0, 0, 0, 1000, 273.15)

    # Parameters of a 3 param solar cell include reference parameters for that
    # particular cell as well as fitting parameters for that cell.
    params = {
        "ref_irrad": 1000.0,  # W/m^2
        "ref_temp": 298.15,  # Kelvin
        "ref_voc": 0.721,  # Volts
        "ref_isc": 6.15,  # Amps
        "fit_ideality_factor": 2.0,
    }
    cell = ThreeParamCell(env=env, params=params)  # data_fp="" TODO: link to test file.
    cell.get_iv(([0, 0, 0],))
