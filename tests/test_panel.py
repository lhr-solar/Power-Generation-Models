"""
@file       test_panel.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Tests for the panel model.
@version    0.4.0
@date       2023-09-24
"""

import sys

sys.path.extend(["."])


import numpy as np

from environment.environment import Environment
from pv.cell.three_param_cell import ThreeParamCell
from pv.module.module import Module
from pv.panel.panel import Panel

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
                env=env,
                params={
                    "cells": {
                        "1": {
                            "instance": ThreeParamCell(
                                env=env,
                                params={
                                    "ref_irrad": 1000.0,  # W/m^2
                                    "ref_temp": 298.15,  # Kelvin
                                    "ref_voc": 0.721,  # Volts
                                    "ref_isc": 6.15,  # Amps
                                    "fit_ideality_factor": 2.0,
                                },
                                # data_fp="" TODO: link to test file.
                            ),
                            "pos": [0, 0],
                        },
                        "2": {
                            "instance": ThreeParamCell(
                                env=env,
                                params={
                                    "ref_irrad": 1000.0,  # W/m^2
                                    "ref_temp": 298.15,  # Kelvin
                                    "ref_voc": 0.721,  # Volts
                                    "ref_isc": 6.15,  # Amps
                                    "fit_ideality_factor": 2.0,
                                },
                                # data_fp="" TODO: link to test file.
                            ),
                            "pos": [1, 0],
                        },
                    },
                    "diode": {},
                },
                # data_fp="" TODO: link to test file
            ),
            "pos": (0, 0),
        },
        "2": {
            "instance": Module(
                env=env,
                params={
                    "cells": {
                        "3": {
                            "instance": ThreeParamCell(
                                env=env,
                                params={
                                    "ref_irrad": 1000.0,  # W/m^2
                                    "ref_temp": 298.15,  # Kelvin
                                    "ref_voc": 0.721,  # Volts
                                    "ref_isc": 6.15,  # Amps
                                    "fit_ideality_factor": 2.0,
                                },
                                # data_fp="" TODO: link to test file.
                            ),
                            "pos": [0, 0],
                        },
                        "4": {
                            "instance": ThreeParamCell(
                                env=env,
                                params={
                                    "ref_irrad": 1000.0,  # W/m^2
                                    "ref_temp": 298.15,  # Kelvin
                                    "ref_voc": 0.721,  # Volts
                                    "ref_isc": 6.15,  # Amps
                                    "fit_ideality_factor": 2.0,
                                },
                                # data_fp="" TODO: link to test file.
                            ),
                            "pos": [1, 0],
                        },
                    },
                    "diode": {},
                },
                # data_fp="" TODO: link to test file
            ),
            "pos": (2, 0),
        },
    },
    "fit_lead_resistance": 0.0,  # Ohms
}


def test_panel_default():
    panel = Panel(env=env, params=params)
    assert panel.get_voltage(0, (0, 0, 0)) >= 0.721 * 4
    assert panel.get_voltage(6.15, (0, 0, 0)) == 0.0
    assert panel.get_voltage(100, (0, 0, 0)) == 0.0


def test_panel_get_pos():
    panel = Panel(env=env, params=params)
    assert panel.get_pos() == [[0, 0], [1, 0], [2, 0], [3, 0]]


def test_panel_fit_data():
    raise NotImplementedError


if __name__ == "__main__":
    panel = Panel(env=env, params=params)
    panel.vis(([0, 0, 0],))
