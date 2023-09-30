"""
@file       module.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Model interface for a PV module.
@version    0.4.0
@date       2023-09-28
"""

import math as m

import numpy as np

from common.utils import normalize
from pv.pv import PV


class Module(PV):
    def __init__(self, params: dict, data_fp=None) -> None:
        super().__init__(params, data_fp)
        self._cell_cache_iv = [None, [], [], []]
        self._diode_cache_iv = [None, [], [], []]

    def _get_cell_voltage(
        self, current: float, irrad: list[float], temp: list[float]
    ) -> float:
        voltage = 0
        for cell, _irrad, _temp in zip(self._params["cells"].values(), irrad, temp):
            voltage += cell["instance"].get_voltage(current, [_irrad], [_temp])

        return voltage
    
    def _get_diode_voltage(
        self, current: float, irrad: list[float], temp: list[float]
    ) -> float:
        voltage = self._params["diode"]["instance"].get_voltage(
            current, [np.average(irrad)], [np.average(temp)]
        )

        return voltage

    def _get_cell_iv(
        self,
        irrad: list[float],
        temp: list[float],
        curr_range: list[float] = [-10.0, 10.0],
    ) -> list[list[float, float, float]]:
        if (
            self._cell_cache_iv[1] == irrad
            and self._cell_cache_iv[2] == temp
            and self._cell_cache_iv[3] == curr_range
        ):
            return self._cell_cache_iv[0]

        iv = []

        curr = curr_range[0]
        bound_curr = 0.0
        res = 0.1
        loop = 0
        num_loops = 3
        while loop < num_loops:
            # Increment resolution decreases by (0.05)^n
            volt = self._get_cell_voltage(curr, irrad, temp)
            iv.append([volt, curr, volt * curr])

            if volt < 0.0 and bound_curr == 0.0:
                # Capture Y axis boundary condition; this is where the IV curve
                # is the most flat and needs more resolution.
                bound_curr = curr

            if curr > curr_range[1]:
                # https://www.desmos.com/calculator/mffm3b9ucm
                # Set x=num_loops and adjust a, b, z to meet requirements
                # - z: I_SC of typical cell
                # - a: Starting proportion of Z, set to right side of knee of
                #   typical I-V curve
                # - b: Adjust such that at X=num_loops the curve is barely under
                #   it (<0.1).
                new_curr = bound_curr * (0.5 + m.log(loop + 1) * 0.45)
                res = res / 3
                curr = new_curr
                loop += 1

            curr += res

        # Normalize data.
        iv = normalize(np.array(iv), 500)

        self._cell_cache_iv = [iv, irrad, temp, curr_range]

        return iv

    def _get_diode_iv(
        self,
        irrad: list[float],
        temp: list[float],
        curr_range: list[float] = [-10.0, 10.0],
    ) -> list[list[float, float, float]]:
        if (
            self._diode_cache_iv[1] == irrad
            and self._diode_cache_iv[2] == temp
            and self._diode_cache_iv[3] == curr_range
        ):
            return self._diode_cache_iv[0]

        iv = []

        curr = curr_range[0]
        bound_curr = 0.0
        res = 0.1
        loop = 0
        num_loops = 3
        while loop < num_loops:
            # Increment resolution decreases by (0.05)^n
            volt = self._get_diode_voltage(curr, irrad, temp)
            iv.append([volt, curr, volt * curr])

            if volt < 0.0 and bound_curr == 0.0:
                # Capture Y axis boundary condition; this is where the IV curve
                # is the most flat and needs more resolution.
                bound_curr = curr

            if curr > curr_range[1]:
                # https://www.desmos.com/calculator/mffm3b9ucm
                # Set x=num_loops and adjust a, b, z to meet requirements
                # - z: I_SC of typical cell
                # - a: Starting proportion of Z, set to right side of knee of
                #   typical I-V curve
                # - b: Adjust such that at X=num_loops the curve is barely under
                #   it (<0.1).
                new_curr = bound_curr * (0.5 + m.log(loop + 1) * 0.45)
                res = res / 3
                curr = new_curr
                loop += 1

            curr += res

        # Normalize data.
        iv = normalize(np.array(iv), 500)

        self._diode_cache_iv = [iv, irrad, temp, curr_range]

        return iv

    def get_voltage(
        self, current: float, irrad: list[float], temp: list[float]
    ) -> float:
        voltage = self._get_cell_voltage(current, irrad, temp)
        if voltage >= 0.0:
            return voltage

        # Constraints:
        # I_L = I_PV + I_D
        # 0 = V_PV(I_PV) - V_D(I_D)
        i_c = current 
        i_d = 0
        is_fwd = False
        while True:
            v_c = self._get_cell_voltage(i_c, irrad, temp)
            # Diode is antiparallel; increasing current is decreasing voltage.
            v_d = -self._get_diode_voltage(i_d, irrad, temp)
            # if m.isclose(v_d, v_c, abs_tol=0.005):
                # return v_c
            if v_c > v_d:
                is_fwd = True
                # v_pv needs to decrease, increase current
                i_c += 0.001
                i_d = current - i_c
            else:
                if is_fwd:
                    return v_c
                # v_pv needs to increase, decrease current
                i_c -= 0.001
                i_d = current - i_c

    def get_current(
        self, voltage: float, irrad: list[float], temp: list[float]
    ) -> float:
        # Cheat and grab from IV curve. Current from voltage can be derived in
        # O(N), while voltage directly is O(N^N).
        c_iv = self._get_cell_iv(irrad, temp)
        c_volt, c_curr, _ = np.transpose(c_iv)
        
        # Diode contribution.        
        m_curr = np.interp(voltage, c_volt, c_curr) - self._params["diode"]["instance"].get_current(
            -voltage, [np.average(irrad)], [np.average(temp)]
        )

        return m_curr

    def get_pos(self) -> list([int, int]):
        pos = []
        for cell in self._params["cells"].values():
            cell_pos = [
                [cell["pos"][0] + x, cell["pos"][1] + y]
                for x, y in cell["instance"].get_pos()
            ]
            pos.extend(cell_pos)

        return pos

    def fit_parameters(
        self, irradiance: float = None, temperature: float = None
    ) -> dict:
        raise NotImplementedError
