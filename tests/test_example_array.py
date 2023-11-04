"""
@file       test_example_array.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Simulate an example array.
@version    0.4.0
@date       2023-10-25
"""

import sys

sys.path.extend(["."])

import numpy as np

from environment.environment import Environment
from pv.cell.three_param_cell import ThreeParamCell
from pv.module.bypass_diode import BypassDiode
from pv.module.module import Module
from pv.panel.panel import Panel

if __name__ == "__main__":
    """Environment:
    - 3x3 matrix of varying irradiance and temperature.
    - Each row is a module of three cells in series. Bypass diode is negligible (N=100).
    """
    voxels = [
        [0, 0, 0, 1000, 273.15],
        [1, 0, 0, 1000, 273.15],
        [2, 0, 0, 1000, 273.15],
        [0, 1, 0, 1000, 272.15],
        [1, 1, 0, 1000, 272.15],
        [2, 1, 0, 1000, 272.15],
        [0, 2, 0, 1000, 273.15],
        [1, 2, 0, 1000, 273.15],
        [2, 2, 0, 1000, 273.15],
    ]
    env = Environment()
    env.add_voxels(*np.transpose(voxels))

    params = {
        "modules": {
            "0": {
                "instance": Module(
                    params={
                        "cells": {
                            "0": {
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
                                "pos": [1, 0],
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
                                "pos": [2, 0],
                            },
                        },
                        "diode": {
                            "instance": BypassDiode(
                                params={
                                    "fit_ideality_factor": 100,
                                    "fit_rev_sat_curr": 2 * 10**-4,
                                }
                            )
                        },
                    },
                ),
                "pos": [0, 0],
            },
            "1": {
                "instance": Module(
                    params={
                        "cells": {
                            "0": {
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
                                "pos": [1, 0],
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
                                "pos": [2, 0],
                            },
                        },
                        "diode": {
                            "instance": BypassDiode(
                                params={
                                    "fit_ideality_factor": 100,
                                    "fit_rev_sat_curr": 2 * 10**-4,
                                }
                            )
                        },
                    },
                ),
                "pos": [0, 1],
            },
            "2": {
                "instance": Module(
                    params={
                        "cells": {
                            "0": {
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
                                "pos": [1, 0],
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
                                "pos": [2, 0],
                            },
                        },
                        "diode": {
                            "instance": BypassDiode(
                                params={
                                    "fit_ideality_factor": 100,
                                    "fit_rev_sat_curr": 2 * 10**-4,
                                }
                            )
                        },
                    },
                ),
                "pos": [0, 2],
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

    panel.vis(irrad, temp)
