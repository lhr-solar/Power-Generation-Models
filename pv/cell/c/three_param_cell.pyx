"""
@file       three_param_cell.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Model for a Three parameter PV cell.
@version    0.4.0
@date       2023-09-24

$ python setup.py build_ext --inplace
"""

import math as m

from scipy import constants


cdef float k_b = constants.k
cdef float q = constants.e

def get_voltage(
    float ref_g,
    float ref_v_oc,
    float ref_i_sc,
    float fit_n,
    float i_l,
    float g,
    float t
):
    # Thermal voltage
    cdef float v_t = (fit_n * k_b * t) / q

    # Short circuit current
    cdef float i_sc = (ref_i_sc * g) / ref_g

    # Photocurrent
    cdef float i_pv = i_sc

    # Open circuit voltage
    cdef float v_oc = ref_v_oc + v_t * m.log((g / ref_g) + 1)
    print(v_oc)

    # Dark/reverse saturation current
    cdef float i_0 = i_sc / (m.exp(v_oc / v_t) - 1)

    # Reverse engineer voltage from diode/dark current
    cdef float i_d = i_pv - i_l
    if i_d < 0:
        # Make the simple assumption that there is no avalanche breakdown;
        # Return 0.0 and the user must assume that for negative voltages the
        # load current is at I_SC.
        return 0.0

    cdef float v = m.log((i_d / i_0) + 1) * v_t

    return v