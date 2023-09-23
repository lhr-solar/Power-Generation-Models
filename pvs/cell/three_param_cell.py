"""
@file       three_param_cell.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Model for a Three parameter PV cell.
@version    0.4.0
@date       2023-09-23
"""
import sys

sys.path.extend([".", ".."])

import math as m

from pvs.cell.cell import Cell


class ThreeParamCell(Cell):
    def __init__(self, parameters, data_fp=None) -> None:
        super().__init__(parameters, data_fp=data_fp)

    def get_current(self, volt: float, irrad: float, temp: float) -> float:
        if volt == 0.0:
            raise Exception("Load voltage is too low!")
        if irrad == 0.0:
            raise Exception("Incident irradiance is too low!")
        if temp == 0.0:
            raise Exception("Cell temperature is too low!")

        # Reference parameters
        g_ref = self._parameters["ref_irrad"]
        v_oc_ref = self._parameters["ref_voc"]
        i_sc_ref = self._parameters["ref_isc"]

        # Curve Fitting parameters
        n = self._parameters["fit_ideality_factor"]

        if n == 0.0:
            raise Exception("Cell ideality factor is too low!")

        g = irrad
        t = temp
        v = volt

        # Thermal voltage
        v_t = n * ThreeParamCell.k_b * t / ThreeParamCell.q  # 26mV

        # Short circuit current
        i_sc = i_sc_ref * g / g_ref

        # Open circuit voltage
        v_oc = v_oc_ref + v_t * m.log(g / g_ref + 1)

        # Dark/reverse saturation current
        i_0 = i_sc / (m.exp(v_oc / v_t) - 1)

        # Dark/diode current
        i_d = i_0 * (m.exp(v / v_t) - 1)

        # Photocurrent
        i_pv = i_sc

        # Load current
        i_l = i_pv - i_d

        return i_l


if __name__ == "__main__":
    parameters = {
        "ref_irrad": 1000.0,  # W/m^2
        "ref_temp": 298.15,  # Kelvin
        "ref_voc": 0.721,  # Volts
        "ref_isc": 6.15,  # Amps
        "fit_ideality_factor": 2.0,
    }
    cell = ThreeParamCell(parameters)  # data_fp="" TODO: link to test file.
    cell.vis([1000], [298.15])
