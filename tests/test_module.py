"""
@file       test_module.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Tests for the module model.
@version    0.4.0
@date       2023-09-28
"""

import sys

sys.path.extend(["."])

import numpy as np
import pytest

from environment.environment import Environment
from pv.cell.three_param_cell import ThreeParamCell
from pv.module.bypass_diode import BypassDiode
from pv.module.module import Module
from common.graph import Graph
from PySide6 import QtWidgets


@pytest.fixture
def setup():
    voxels = [[0, 0, 0, 1000, 273.15], [1, 0, 0, 1000, 273.15], [2, 0, 0, 1000, 273.15]]
    env = Environment()
    env.add_voxels(*np.transpose(voxels))

    # Parameters for a module consist of parameters for individual solar cells,
    # as well parameters for the bypass diode and lead resistance. Mix of
    # reference and fitting parameters.
    params = {
        "cells": {
            "1": {
                "instance": ThreeParamCell(
                    params={
                        "ref_irrad": 1000.0,  # W/m^2
                        "ref_temp": 298.15,  # Kelvin
                        "ref_voc": 0.721,  # Volts
                        "ref_isc": 6.15,  # Amps
                        "fit_fwd_ideality_factor": 2,
                        "fit_rev_ideality_factor": 1,
                        "fit_rev_sat_curr": 1 * 10**-5,
                    },
                ),
                "pos": [0, 0],
            },
            "2": {
                "instance": ThreeParamCell(
                    params={
                        "ref_irrad": 1000.0,  # W/m^2
                        "ref_temp": 298.15,  # Kelvin
                        "ref_voc": 0.721,  # Volts
                        "ref_isc": 6.15,  # Amps
                        "fit_fwd_ideality_factor": 2,
                        "fit_rev_ideality_factor": 1,
                        "fit_rev_sat_curr": 1 * 10**-5,
                    },
                ),
                "pos": [1, 0],
            },
            "3": {
                "instance": ThreeParamCell(
                    params={
                        "ref_irrad": 1000.0,  # W/m^2
                        "ref_temp": 298.15,  # Kelvin
                        "ref_voc": 0.721,  # Volts
                        "ref_isc": 6.15,  # Amps
                        "fit_fwd_ideality_factor": 2,
                        "fit_rev_ideality_factor": 1,
                        "fit_rev_sat_curr": 1 * 10**-5,
                    },
                ),
                "pos": [2, 0],
            },
        },
        "diode": {
            "instance": BypassDiode(
                params={"fit_ideality_factor": 1.5, "fit_rev_sat_curr": 2 * 10**-4}
            )
        },
    }

    time_idx = 0

    yield env, params, time_idx


def test_sanity(setup):
    env, params, time_idx = setup

    module = Module(params=params)
    irrad = []
    temp = []
    pos = module.get_pos()
    for p in pos:
        g, t = env.get_voxel(*p, time_idx)
        irrad.append(g)
        temp.append(t)

    # At 0 A, we should be at VOC at STC.
    assert module.get_voltage(0, irrad, temp) >= 0.721 * 2.9
    # At ISC, we should be at 0 V at STC. However, the bypass diode decreases
    # the ISC marginally, shifting the 6.15 ISC back a fraction of the volt.
    assert module.get_voltage(6.15, irrad, temp) == pytest.approx(0.0, abs=0.2)
    # At very large current, we should be in quadrant II and negative voltage at STC.
    assert module.get_voltage(6.15 * 1.5, irrad, temp) < 0.0

    # At 0 V, we should be at ISC at STC.
    assert module.get_current(0, irrad, temp) == pytest.approx(6.15, abs=0.05)
    # At VOC, we should be at 0 A at STC. However, the bypass diode decreases
    # the ISC marginally, shifting the 6.15 ISC back a fraction of the volt.
    assert module.get_current(0.721 * 3, irrad, temp) == pytest.approx(0.0, abs=0.01)
    # At very large voltage, we should be in quadrant IV and negative current at STC.
    assert module.get_current(0.721 * 3 * 1.5, irrad, temp) < 0.0


def test_equiv(setup):
    """Assert that the two methods of deriving the model are within 5% of each
    other."""
    env, params, time_idx = setup

    module = Module(params=params)
    irrad = []
    temp = []
    pos = module.get_pos()
    for p in pos:
        g, t = env.get_voxel(*p, time_idx)
        irrad.append(g)
        temp.append(t)

    for volt in np.linspace(-2.0, 2.3, 100):
        curr = module.get_current(volt, irrad, temp)
        volt2 = module.get_voltage(curr, irrad, temp)
        print(f"{volt}\t{volt2}\t{curr}")
        assert volt2 == pytest.approx(volt, abs=0.03)

    for curr in np.linspace(-5.0, 10.0, 100):
        volt = module.get_voltage(curr, irrad, temp)
        curr2 = module.get_current(volt, irrad, temp)
        assert curr2 == pytest.approx(curr, rel=0.05)


def test_pos(setup):
    _, params, _ = setup

    module = Module(params=params)
    assert module.get_pos() == [[0, 0], [1, 0], [2, 0]]


def test_fit_data():
    raise NotImplementedError


if __name__ == "__main__":
    voxels = [[0, 0, 0, 1000, 273.15], [1, 0, 0, 1000, 273.15], [2, 0, 0, 1000, 273.15]]
    env = Environment()
    env.add_voxels(*np.transpose(voxels))

    # Parameters for a module consist of parameters for individual solar cells,
    # as well parameters for the bypass diode and lead resistance. Mix of
    # reference and fitting parameters.
    params = {
        "cells": {
            "1": {
                "instance": ThreeParamCell(
                    params={
                        "ref_irrad": 1000.0,  # W/m^2
                        "ref_temp": 298.15,  # Kelvin
                        "ref_voc": 0.721,  # Volts
                        "ref_isc": 6.15,  # Amps
                        "fit_fwd_ideality_factor": 1.294,
                        "fit_rev_ideality_factor": 2,
                        "fit_rev_sat_curr": 1 * 10**-5,
                    },
                ),
                "pos": [0, 0],
            },
            "2": {
                "instance": ThreeParamCell(
                    params={
                        "ref_irrad": 1000.0,  # W/m^2
                        "ref_temp": 298.15,  # Kelvin
                        "ref_voc": 0.721,  # Volts
                        "ref_isc": 6.15,  # Amps
                        "fit_fwd_ideality_factor": 1.294,
                        "fit_rev_ideality_factor": 2,
                        "fit_rev_sat_curr": 1 * 10**-5,
                    },
                ),
                "pos": [1, 0],
            },
            "3": {
                "instance": ThreeParamCell(
                    params={
                        "ref_irrad": 1000.0,  # W/m^2
                        "ref_temp": 298.15,  # Kelvin
                        "ref_voc": 0.721,  # Volts
                        "ref_isc": 6.15,  # Amps
                        "fit_fwd_ideality_factor": 1.294,
                        "fit_rev_ideality_factor": 2,
                        "fit_rev_sat_curr": 1 * 10**-5,
                    },
                ),
                "pos": [2, 0],
            },
        },
        "diode": {
            "instance": BypassDiode(
                params={"fit_ideality_factor": 1.5, "fit_rev_sat_curr": 2 * 10**-4}
            )
        },
    }

    time_idx = 0

    module = Module(params=params)
    irrad = []
    temp = []
    pos = module.get_pos()
    for p in pos:
        g, t = env.get_voxel(*p, time_idx)
        irrad.append(g)
        temp.append(t)

    module.vis(irrad, temp, curr_range=[-5, 15], volt_range=[-0.6, 0.721 * 3.5])
