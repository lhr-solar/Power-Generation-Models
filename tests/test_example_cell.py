"""
@file       test_example_cell.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Simulate an example cell.
@version    0.4.0
@date       2023-10-25
"""

import sys

sys.path.extend(["."])

import numpy as np

from environment.environment import Environment
from pv.cell.three_param_cell import ThreeParamCell

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
        "ref_irrad": 1000.0,  # W/m^2
        "ref_temp": 298.15,  # Kelvin
        "ref_voc": 0.721,  # Volts
        "ref_isc": 6.15,  # Amps
        "fit_fwd_ideality_factor": 10,
        "fit_rev_ideality_factor": 1,
        "fit_rev_sat_curr": 1 * 10**-5,
    }

    time_idx = 0

    cell = ThreeParamCell(
        params=params, data_fp="./tests/example_captures/example_cell.capture"
    )
    irrad = []
    temp = []
    pos = cell.get_pos()
    for p in pos:
        g, t = env.get_voxel(*p, time_idx)
        irrad.append(g)
        temp.append(t)

    cell.vis(
        [375],
        [298.15],
        curr_range=[-3.0, 8.0],
        volt_range=[-0.5, 0.8],
        show_exp_data=True,
    )
    fit_params = cell.fit_params()
    import json

    print(json.dumps(fit_params, indent=4))

    cell.vis(
        [fit_params["irradiance"]["val"]],
        [fit_params["temperature"]["val"]],
        curr_range=[-3.0, 8.0],
        volt_range=[-0.5, 0.8],
        show_exp_data=True,
    )
