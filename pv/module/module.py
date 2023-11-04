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
        """It is O(n), n being the number of solar cells in the module, to
        derive the total module (cells in series) voltage with the current
        through each cell."""
        voltage = 0
        for cell, _irrad, _temp in zip(self._params["cells"].values(), irrad, temp):
            voltage += cell["instance"].get_voltage(current, [_irrad], [_temp])

        return voltage

    def _get_cell_iv(
        self,
        irrad: list[float],
        temp: list[float],
        curr_range: list[float] = [-10.0, 10.0],
        volt_range: list[float] = [-10.0, 10.0],
    ) -> list[list[float, float, float]]:
        def calc(curr):
            volt = self._get_cell_voltage(curr, irrad, temp)
            return volt, curr, volt * curr

        iv = [calc(curr) for curr in np.linspace(*curr_range, self.IV_POINTS)]

        if (
            self._cell_cache_iv[1] == irrad
            and self._cell_cache_iv[2] == temp
            and self._cell_cache_iv[3] == curr_range
        ):
            return self._cell_cache_iv[0]

        # Normalize data.
        iv = normalize(np.array(iv), self.IV_NORM_POINTS)

        self._cell_cache_iv = [iv, irrad, temp, curr_range]

        return iv

    def get_voltage(self, current: float, irrad: list[float], temp: list[float]):
        # Cheat and grab from IV curve. Current from voltage can be derived in
        # O(N), while voltage directly is O(N^N).
        c_iv = self._get_cell_iv(irrad, temp)
        c_volt, c_curr, c_pow = np.transpose(c_iv)
        c_vi = np.transpose([c_curr, c_volt, c_pow])
        c_vi = normalize(c_vi, 500)
        c_curr_t, c_volt_t, c_pow_t = np.transpose(c_vi)

        # Derive initial estimate assuming no contribution from diode.
        m_volt_est = np.interp(current, c_curr_t, c_volt_t)

        is_fwd = False
        while True:
            # Given module voltage estimate, derive current components.
            m_curr_est = np.interp(m_volt_est, c_volt, c_curr) + self._params["diode"][
                "instance"
            ].get_current(-m_volt_est, [np.average(irrad)], [np.average(temp)])
            if m.isclose(m_curr_est, current, abs_tol=0.001):
                break
            if m_curr_est > current:
                is_fwd = True

                # Current too high; increase module voltage.
                m_volt_est += 0.001
            else:
                if is_fwd:
                    # Toggled, exit early.
                    break
                # Current too low; decrease module voltage.
                m_volt_est -= 0.001

        return m_volt_est

    def get_current(
        self, voltage: float, irrad: list[float], temp: list[float]
    ) -> float:
        # Cheat and grab from IV curve. Current from voltage can be derived in
        # O(N), while voltage directly is O(N^N).
        c_iv = self._get_cell_iv(irrad, temp)
        c_volt, c_curr, _ = np.transpose(c_iv)

        # Diode contribution.
        m_curr = np.interp(voltage, c_volt, c_curr) + self._params["diode"][
            "instance"
        ].get_current(-voltage, [np.average(irrad)], [np.average(temp)])

        return m_curr

    def get_iv(
        self,
        irrad: list[float],
        temp: list[float],
        curr_range: list[float] = [-10.0, 10.0],
        volt_range: list[float] = [-10.0, 10.0],
    ) -> list[list[float, float, float]]:
        # For module level, it's easier to sweep voltage than current.
        iv = []
        c_iv = self._get_cell_iv(irrad, temp, curr_range, volt_range)

        for c_volt, c_curr, _ in c_iv:
            d_curr = self._params["diode"]["instance"].get_current(
                -c_volt, [np.average(irrad)], [np.average(temp)]
            )
            m_curr = c_curr + d_curr
            m_pow = c_volt * m_curr
            if (
                curr_range[0] <= m_curr
                and m_curr <= curr_range[1]
                and volt_range[0] <= c_volt
                and c_volt <= volt_range[1]
            ):
                iv.append([c_volt, m_curr, m_pow])

        return iv

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
