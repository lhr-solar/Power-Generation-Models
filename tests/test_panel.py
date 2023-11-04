"""
@file       test_panel.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Tests for the panel model.
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
from pv.panel.panel import Panel
from common.graph import Graph
from PySide6 import QtWidgets


@pytest.fixture
def setup():
    voxels = [
        [0, 0, 0, 1000, 298.15],
        [1, 0, 0, 1000, 298.15],
        [2, 0, 0, 1000, 298.15],
        [3, 0, 0, 1000, 298.15],
    ]
    env = Environment()
    env.add_voxels(*np.transpose(voxels))

    # Parameters for a module consist of parameters for individual solar cells,
    # as well parameters for the bypass diode and lead resistance. Mix of
    # reference and fitting parameters.
    params = {
        "modules": {
            "1": {
                "instance": Module(
                    params={
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
                                    # data_fp="" TODO: link to test file.
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
                                    # data_fp="" TODO: link to test file.
                                ),
                                "pos": [1, 0],
                            },
                        },
                        "diode": {
                            "instance": BypassDiode(
                                params={
                                    "fit_ideality_factor": 1.5,
                                    "fit_rev_sat_curr": 2 * 10**-4,
                                }
                            )
                        },
                    },
                    # data_fp="" TODO: link to test file
                ),
                "pos": (0, 0),
            },
            "2": {
                "instance": Module(
                    params={
                        "cells": {
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
                                    # data_fp="" TODO: link to test file.
                                ),
                                "pos": [0, 0],
                            },
                            "4": {
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
                                    # data_fp="" TODO: link to test file.
                                ),
                                "pos": [1, 0],
                            },
                        },
                        "diode": {
                            "instance": BypassDiode(
                                params={
                                    "fit_ideality_factor": 1.5,
                                    "fit_rev_sat_curr": 2 * 10**-4,
                                }
                            )
                        },
                    },
                    # data_fp="" TODO: link to test file
                ),
                "pos": (2, 0),
            },
        },
        "fit_lead_resistance": 0.0,  # Ohms
    }

    time_idx = 0

    yield env, params, time_idx


def test_sanity(setup):
    env, params, time_idx = setup

    panel = Panel(params=params)
    irrad = []
    temp = []
    pos = panel.get_pos()
    for p in pos:
        g, t = env.get_voxel(*p, time_idx)
        irrad.append(g)
        temp.append(t)

    assert panel.get_voltage(0, irrad, temp) >= 0.721 * 4
    assert panel.get_voltage(6.15, irrad, temp) == 0.0
    assert panel.get_voltage(100, irrad, temp) == 0.0

    assert panel.get_current(0, irrad, temp) >= 6.15
    assert panel.get_current(0.721 * 4, irrad, temp) == pytest.approx(0.0, abs=0.0001)
    assert panel.get_current(100, irrad, temp) == 0.0


def test_panel_get_pos(setup):
    _, params, _ = setup

    panel = Panel(params=params)
    assert panel.get_pos() == [[0, 0], [1, 0], [2, 0], [3, 0]]


def test_panel_fit_data():
    raise NotImplementedError


if __name__ == "__main__":
    voxels = [
        [0, 0, 0, 1000, 298.15],
        [1, 0, 0, 500, 298.15],
        [2, 0, 0, 250, 298.15],
        [3, 0, 0, 750, 298.15],
    ]
    env = Environment()
    env.add_voxels(*np.transpose(voxels))

    # Parameters for a module consist of parameters for individual solar cells,
    # as well parameters for the bypass diode and lead resistance. Mix of
    # reference and fitting parameters.
    params = {
        "modules": {
            "1": {
                "instance": Module(
                    params={
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
                                    # data_fp="" TODO: link to test file.
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
                                    # data_fp="" TODO: link to test file.
                                ),
                                "pos": [1, 0],
                            },
                        },
                        "diode": {
                            "instance": BypassDiode(
                                params={
                                    "fit_ideality_factor": 1.5,
                                    "fit_rev_sat_curr": 2 * 10**-4,
                                }
                            )
                        },
                    },
                    # data_fp="" TODO: link to test file
                ),
                "pos": (0, 0),
            },
            "2": {
                "instance": Module(
                    params={
                        "cells": {
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
                                    # data_fp="" TODO: link to test file.
                                ),
                                "pos": [0, 0],
                            },
                            "4": {
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
                                    # data_fp="" TODO: link to test file.
                                ),
                                "pos": [1, 0],
                            },
                        },
                        "diode": {
                            "instance": BypassDiode(
                                params={
                                    "fit_ideality_factor": 1.5,
                                    "fit_rev_sat_curr": 2 * 10**-4,
                                }
                            )
                        },
                    },
                    # data_fp="" TODO: link to test file
                ),
                "pos": (2, 0),
            },
        },
        "fit_lead_resistance": 0.0,  # Ohms
    }

    time_idx = 0

    panel = Panel(params=params)
    irrad = []
    temp = []
    pos = panel.get_pos()
    for p in pos:
        g, t = env.get_voxel(*p, time_idx)
        irrad.append(g)
        temp.append(t)

    panel.vis(irrad, temp, curr_range=[-5, 15], volt_range=[-1, 3])
