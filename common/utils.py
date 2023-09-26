"""_summary_
@file       utils.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Utility functions.
@version    0.4.0
@date       2023-05-14
"""

import collections.abc
import numpy as np
import math as m
from scipy.interpolate import interp1d as scipy_interp1d

def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

def normalize(data, num_points=100):
    """Take a numpy array of list of lists, and:
    1. Sort by the first axis ([:, 0]).
    2. Replace redundant data with the mean.
    3. Interpolate data across the set.
    4. Return N points of this interpolation.

    Args:
        data (np.array()): List of lists, with first axis being the axis to
            align on. 
        num_points (int, optional): Number of points to return.
    """

    def groupby_mean(a):
        # Sort array by groupby column
        b = a[a[:, 0].argsort()]

        # Get interval indices for the sorted groupby col
        idx = np.flatnonzero(np.r_[True, b[:-1, 0] != b[1:, 0], True])

        # Get counts of each group and sum rows based on the groupings & hence averages
        counts = np.diff(idx)
        avg = (
            np.add.reduceat(b[:, 1:], idx[:-1], axis=0)
            / counts.astype(float)[:, None]
        )

        # Finally concatenate for the output in desired format
        return np.c_[b[idx[:-1], 0], avg]
    
    # Sort by voltage and delete dups
    data = groupby_mean(data[data[:, 0].argsort()])

    # Generate interpolate function
    volt, curr, _ = np.transpose(data)
    f_interp = scipy_interp1d(volt, curr, kind="slinear")

    # Interpolate across the space in even increments.
    volts = np.linspace(np.min(volt), np.max(volt), num=num_points)
    curr = f_interp(volts)
    pow = volts * curr

    # Sort and reform data.
    data = np.transpose([volts, curr, pow])
    data = data[data[:, 0].argsort()]

    return data