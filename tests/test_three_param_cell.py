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

from environment.environment import Environment
from pv.cell.three_param_cell import ThreeParamCell


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


def test_three_param_cell_default(setup):
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
    assert cell.get_voltage(params["ref_isc"], irrad, temp) == 0.0
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


def test_three_param_cell_fit_data():
    raise NotImplementedError


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

    edge, mpp = cell.get_edge(irrad, temp)
    pmpp = mpp[0] * mpp[1]
    pedge = edge[0] * edge[1]
    ff = pmpp / pedge
    print(pmpp, pedge, ff, edge, mpp)

    cell.vis(irrad, temp, curr_range=[-10, 10])
