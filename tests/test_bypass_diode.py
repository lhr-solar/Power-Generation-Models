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
    params = {"fit_ideality_factor": 1.5, "fit_rev_sat_curr": 2 * 10**-4}

    yield params


def test_sanity(setup):
    params = setup

    diode = BypassDiode(params=params)
    irrad = [1000]
    temp = [298.15]

    # At 0 current, voltage should less than equal to 0.
    assert diode.get_voltage(0.0, irrad, temp) <= 0.0
    # At some current, voltage should be greater than 0.0.
    assert diode.get_voltage(3.0, irrad, temp) > 0.0


def test_equiv(setup):
    """Assert that the two methods of deriving the model are within 1% of each
    other."""
    params = setup

    diode = BypassDiode(params=params)
    irrad = [1000]
    temp = [298.15]

    for volt in np.linspace(0.0, 0.5, 100):
        curr = diode.get_current(volt, irrad, temp)
        volt2 = diode.get_voltage(curr, irrad, temp)
        assert volt2 == pytest.approx(volt, rel=0.01)

    for curr in np.linspace(0.0, 5.0, 100):
        volt = diode.get_voltage(curr, irrad, temp)
        assert diode.get_current(volt, irrad, temp) == pytest.approx(curr, rel=0.01)


def test_fit_data(setup):
    params = setup

    diode = BypassDiode(
        params=params, data_fp="./tests/example_captures/example_diode.capture"
    )
    params = diode.fit_params(irradiance=1000, temperature=298.15)


if __name__ == "__main__":
    # Parameters for a module consist of parameters for individual solar cells,
    # as well parameters for the bypass diode and lead resistance. Mix of
    # reference and fitting parameters.
    params = {"fit_ideality_factor": 1.5, "fit_rev_sat_curr": 2 * 10**-4}

    time_idx = 0

    diode = BypassDiode(params=params)
    irrad = [1000]
    temp = [298.15]

    print(diode.get_voltage(12, irrad, temp))
    diode.vis(irrad, temp, curr_range=[-1.0, 10.0], volt_range=[-0.1, 0.5])
