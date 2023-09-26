"""
@file       test_pv_system.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Tests for the pv system.
@version    0.4.0
@date       2023-09-24
"""

import sys

sys.path.extend(["."])

import numpy as np
import pytest
from environment.environment import Environment
from pv.cell.three_param_cell import ThreeParamCell
from pv.pv_system import PVSystem


@pytest.fixture
def setup():
    voxels = [
        [0, 0, 0, 1000, 298.15],
        [1, 0, 0, 500, 298.15],
        [2, 0, 0, 250, 298.15],
        [3, 0, 0, 750, 298.15],
    ]
    env = Environment()
    env.add_voxels(*np.transpose(voxels))

    params = {
        "ref_irrad": 1000.0,  # W/m^2
        "ref_temp": 298.15,  # Kelvin
        "ref_voc": 0.721,  # Volts
        "ref_isc": 6.15,  # Amps
        "fit_ideality_factor": 2.0,
    }

    time_idx = 0

    yield env, params, time_idx


def test_pv_system(setup):
    env, params, time_idx = setup

    system = PVSystem(env=env)
    system.add_pv(
        0,
        ThreeParamCell(
            params=params,
        ),
        0,
        0,
    )

    system.add_pv(
        1,
        ThreeParamCell(
            params=params,
        ),
        1,
        0,
    )

    system.rem_pv(0)

    assert system.get_pv_voltage(1, 0, 0) >= 0.721
    assert system.get_pv_voltage(1, 6.15, 0) == 0.0
    assert system.get_pv_voltage(1, 100, 0) == 0.0


if __name__ == "__main__":
    voxels = [
        [0, 0, 0, 1000, 298.15],
        [1, 0, 0, 750, 298.15],
        [2, 0, 0, 500, 298.15],
        [3, 0, 0, 250, 298.15],
    ]
    env = Environment()
    env.add_voxels(*np.transpose(voxels))

    params = {
        "ref_irrad": 1000.0,  # W/m^2
        "ref_temp": 298.15,  # Kelvin
        "ref_voc": 0.721,  # Volts
        "ref_isc": 6.15,  # Amps
        "fit_ideality_factor": 2.0,
    }

    time_idx = 0

    system = PVSystem(env=env)
    system.add_pv(
        0,
        ThreeParamCell(
            params=params,
        ),
        0,
        0,
    )

    system.add_pv(
        1,
        ThreeParamCell(params=params),
        1,
        0,
    )

    system.add_pv(
        2,
        ThreeParamCell(params=params),
        2,
        0,
    )

    system.vis_pv(0)

    system.set_sys_pos(1, 0)
    system.vis_pv(0)
