"""
@file       test_cell.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Tests for the cell model.
@version    0.4.0
@date       2023-09-24
"""

import sys

sys.path.extend(["."])

from pv.cell.cell import Cell


def test_cell_get_pos():
    params = {}
    cell = Cell(params=params)
    assert cell.get_pos() == [[0, 0]]
