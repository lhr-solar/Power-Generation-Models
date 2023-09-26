"""
@file       test_three_param_cell.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Tests for the Three parameter cell model.
@version    0.4.0
@date       2023-09-24
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
        "fit_ideality_factor": 1.0,
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

    assert cell.get_voltage(0,                  irrad, temp) >= params["ref_voc"]
    assert cell.get_voltage(params["ref_isc"],  irrad, temp) == 0.0
    assert cell.get_voltage(100,                irrad, temp) == 0.0

    assert cell.get_current(0,                  irrad, temp) >= params["ref_isc"]
    assert cell.get_current(params["ref_voc"],  irrad, temp) == 0.0
    assert cell.get_current(100,                irrad, temp) == 0.0

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
        "fit_ideality_factor": 2.0,
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

    # print(cell.get_edge(irrad, temp))
    cell.vis(irrad, temp)
