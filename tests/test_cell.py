"""
@file       test_cell.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Tests for the cell model.
@version    0.4.0
@date       2023-09-24
"""

import sys

sys.path.extend(["."])

from environment.environment import Environment
from pv.cell.cell import Cell


def test_cell_get_pos():
    env = Environment()
    env.add_voxel(0, 0, 0, 1000, 273.15)

    params = {}
    cell = Cell(env=env, params=params)
    assert cell.get_pos() == [[0, 0]]
