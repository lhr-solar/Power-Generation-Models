"""_summary_
@file       utils.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Utility functions.
@version    0.4.0
@date       2023-05-14
"""

import collections.abc


def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d
