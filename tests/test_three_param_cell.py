"""
@file       test_three_param_cell.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Tests for the Three parameter cell model.
@version    0.4.0
@date       2023-09-28
"""

import sys

sys.path.extend(["."])

import pytest
import numpy as np

from environment.environment import Environment
from pv.cell.three_param_cell import ThreeParamCell
from common.graph import Graph
from PySide6 import QtWidgets


@pytest.fixture
def setup():
    env = Environment()
    env.add_voxel(0, 0, 0, 1000, 273.15)

    # Parameters of a 3 param solar cell include reference parameters for that
    # particular cell as well as fitting parameters for that cell.
    params = {
        "ref_irrad": 1000.0,  # W/m^2
        "ref_temp": 298.15,  # Kelvin
        "ref_voc": 0.721,  # Volts
        "ref_isc": 6.15,  # Amps
        "fit_fwd_ideality_factor": 2,
        "fit_rev_ideality_factor": 1,
        "fit_rev_sat_curr": 1 * 10**-5,
    }

    time_idx = 0

    yield env, params, time_idx


def test_sanity(setup):
    env, params, time_idx = setup

    cell = ThreeParamCell(params=params)
    irrad = []
    temp = []
    pos = cell.get_pos()
    for p in pos:
        g, t = env.get_voxel(*p, time_idx)
        irrad.append(g)
        temp.append(t)

    # At 0 A, we should be at VOC at STC.
    assert cell.get_voltage(0, irrad, temp) >= params["ref_voc"]
    # At ISC, we should be at 0 V at STC.
    assert cell.get_voltage(params["ref_isc"], irrad, temp) == pytest.approx(
        0.0, abs=0.0001
    )
    # At very large current, we should be in quadrant II and negative voltage at STC.
    assert cell.get_voltage(params["ref_isc"] * 1.5, irrad, temp) < 0.0

    # At 0 V, we should be at ISC at STC.
    assert cell.get_current(0, irrad, temp) >= params["ref_isc"]
    # At VOC, we should be at 0 A at STC.
    assert cell.get_current(params["ref_voc"], irrad, temp) == pytest.approx(
        0.0, abs=0.0001
    )
    # At very large voltage, we should be in quadrant IV and negative current at STC.
    assert cell.get_current(params["ref_voc"] * 1.5, irrad, temp) < 0.0


def test_equiv(setup):
    """Assert that the two methods of deriving the model are within 5% of each
    other."""
    env, params, time_idx = setup

    cell = ThreeParamCell(params=params)
    irrad = []
    temp = []
    pos = cell.get_pos()
    for p in pos:
        g, t = env.get_voxel(*p, time_idx)
        irrad.append(g)
        temp.append(t)

    for volt in np.linspace(-params["ref_voc"], params["ref_voc"] * 1.5, 100):
        curr = cell.get_current(volt, irrad, temp)
        volt2 = cell.get_voltage(curr, irrad, temp)
        # Edge case where functions diverge or break down near zero (due to
        # flatness of IV at this point).
        if 0 < volt and volt < 0.1:
            assert volt2 == pytest.approx(volt, abs=0.1)
        else:
            assert volt2 == pytest.approx(volt, rel=0.05)

    for curr in np.linspace(-params["ref_isc"], params["ref_isc"] * 1.5, 100):
        volt = cell.get_voltage(curr, irrad, temp)
        curr2 = cell.get_current(volt, irrad, temp)
        assert curr2 == pytest.approx(curr, rel=0.05)


def test_fit_data(setup):
    _, params, _ = setup

    cell = ThreeParamCell(
        params=params, data_fp="./tests/example_captures/example_cell.capture"
    )
    params = cell.fit_params(irradiance=1000, temperature=298.15)


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
        "fit_fwd_ideality_factor": 1.294,
        "fit_rev_ideality_factor": 1,
        "fit_rev_sat_curr": 1 * 10**-5,
    }

    time_idx = 0

    cell = ThreeParamCell(params=params)
    irrad = []
    temp = []
    pos = cell.get_pos()
    for p in pos:
        g, t = env.get_voxel(*p, time_idx)
        irrad.append(g)
        temp.append(t)

    cell.vis(irrad, temp, curr_range=[-10, 10], volt_range=[-0.4, 0.8])
