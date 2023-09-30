"""
@file       test_bypass_diode.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Tests for the bypass diode model.
@version    0.4.0
@date       2023-09-28
"""

import sys

sys.path.extend(["."])

import numpy as np
import pytest

from environment.environment import Environment
from pv.module.bypass_diode import BypassDiode


@pytest.fixture
def setup():
    # Parameters for a module consist of parameters for individual solar cells,
    # as well parameters for the bypass diode and lead resistance. Mix of
    # reference and fitting parameters.
    params = {"fit_ideality_factor": 1.5, "fit_rev_sat_current": 2 * 10 ^ -4}

    time_idx = 0

    yield params, time_idx


def test_bypass_diode_default(setup):
    params, time_idx = setup

    diode = BypassDiode(params=params)
    irrad = [1000]
    temp = [298.15]

    # TODO: this has not been tuned yet.
    # At 0 A, we should be at VOC at STC.
    assert diode.get_voltage(0, irrad, temp) >= 0.721 * 3
    # At ISC, we should be at 0 V at STC.
    assert diode.get_voltage(6.15, irrad, temp) == 0.0
    # At very large current, we should be in quadrant II and negative voltage at STC.
    assert diode.get_voltage(6.15 * 1.5, irrad, temp) < 0.0


def test_bypass_diode_fit_data():
    raise NotImplementedError


if __name__ == "__main__":
    # Parameters for a module consist of parameters for individual solar cells,
    # as well parameters for the bypass diode and lead resistance. Mix of
    # reference and fitting parameters.
    params = {"fit_ideality_factor": 1.5, "fit_rev_sat_current": 2 * 10**-4}

    time_idx = 0

    diode = BypassDiode(params=params)
    irrad = [1000]
    temp = [298.15]

    print(diode.get_voltage(12, irrad, temp))
    diode.vis(irrad, temp, curr_range=[0, 10])
