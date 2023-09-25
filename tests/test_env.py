"""
@file       test_env.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Tests for the environment model.
@version    0.4.0
@date       2023-09-24
"""

import sys

sys.path.extend(["."])

import random

import numpy as np

from environment.environment import Environment


def test_env_empty():
    env = Environment()
    assert env.get_voxels().empty


def test_env_add_voxel():
    env = Environment()
    voxel = [0, 0, 0, 1000.0, 273.15]

    env.add_voxel(*voxel)
    assert not env.get_voxels().empty


def test_env_add_voxels():
    env = Environment()
    voxels = [
        [1, 0, 0, 1000.0, 273.15],
        [0, 1, 1, 1000.0, 273.15],
        [1, 1, 0, 1000.0, 273.15],
    ]

    env.add_voxels(*np.transpose(voxels))
    assert not env.get_voxels().empty
    assert env.get_voxel(0, 1, 1) == [1000.0, 273.15]


def test_env_gen_voxels():
    def generator() -> list:
        rows, columns = 50, 50
        time = 500

        def get_irrad(x, y, t):
            irrad = x * y
            return max(0, min(irrad, 1000))

        def get_temp(x, y, t):
            temp = 298.15 + random.gauss(x * y * t / 500, 1)
            return max(273.15, min(temp, 398.15))

        return [
            [x, y, t, get_irrad(x, y, t), get_temp(x, y, t)]
            for t in range(time)
            for y in range(rows)
            for x in range(columns)
        ]

    env = Environment()
    env.gen_voxels(generator)
    assert not env.get_voxels().empty
    assert not env.get_voxels_slice(1).empty


if __name__ == "__main__":

    def generator() -> list:
        rows, columns = 50, 50
        time = 500

        def get_irrad(x, y, t):
            irrad = x * y
            return max(0, min(irrad, 1000))

        def get_temp(x, y, t):
            temp = 298.15 + random.gauss(x * y * t / 500, 1)
            return max(273.15, min(temp, 398.15))

        return [
            [x, y, t, get_irrad(x, y, t), get_temp(x, y, t)]
            for t in range(time)
            for y in range(rows)
            for x in range(columns)
        ]

    env = Environment()
    env.gen_voxels(generator)

    env.vis_voxels()
