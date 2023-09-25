"""
@file       test_module.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Tests for the module model.
@version    0.4.0
@date       2023-09-24
"""

import sys

sys.path.extend(["."])

import numpy as np

from environment.environment import Environment
from pv.cell.three_param_cell import ThreeParamCell
from pv.module.module import Module

voxels = [[0, 0, 0, 1000, 273.15], [1, 0, 0, 500, 273.15], [2, 0, 0, 250, 273.15]]
env = Environment()
env.add_voxels(*np.transpose(voxels))

# Parameters for a module consist of parameters for individual solar cells,
# as well parameters for the bypass diode and lead resistance. Mix of
# reference and fitting parameters.
params = {
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
            ),
            "pos": [1, 0],
        },
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
            ),
            "pos": [2, 0],
        },
    },
    "diode": {},
}


def test_module_default():
    module = Module(env=env, params=params)
    assert module.get_voltage(0, (0, 0, 0)) >= 0.721 * 3
    assert module.get_voltage(6.15, (0, 0, 0)) == 0.0
    assert module.get_voltage(100, (0, 0, 0)) == 0.0


def test_module_get_pos():
    module = Module(env=env, params=params)
    assert module.get_pos() == [[0, 0], [1, 0], [2, 0]]


def test_module_fit_data():
    raise NotImplementedError


if __name__ == "__main__":
    module = Module(env=env, params=params)
    module.vis(([0, 0, 0],))
