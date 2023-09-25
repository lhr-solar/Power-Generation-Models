"""
@file       test_three_param_cell.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Tests for the Three parameter cell model.
@version    0.4.0
@date       2023-09-24
"""

import sys

sys.path.extend(["."])

from environment.environment import Environment
from pv.cell.three_param_cell import ThreeParamCell

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


def test_three_param_cell_default():
    cell = ThreeParamCell(env=env, params=params)
    assert cell.get_voltage(0, (0, 0, 0)) >= params["ref_voc"]
    assert cell.get_voltage(params["ref_isc"], (0, 0, 0)) == 0.0
    assert cell.get_voltage(100, (0, 0, 0)) == 0.0


def test_three_param_cell_fit_data():
    raise NotImplementedError


if __name__ == "__main__":
    cell = ThreeParamCell(env=env, params=params)  # data_fp="" TODO: link to test file.
    cell.vis(([0, 0, 0],))
