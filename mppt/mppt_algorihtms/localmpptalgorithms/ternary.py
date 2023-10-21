"""
Ternary.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/24/20
Last Modified: 02/27/21
Description: Implementation of the Ternary Search algorithm.

The implementation of this algorithm is based on the wikipedia page for the
Ternary Search: https://en.wikipedia.org/wiki/Ternary_search

    The Ternary search seeks to find the min/max of a unimodal
    function. In this case,

    f(x) = P-V Curve, which is max at VMPP.

    This algorithm does not require an initial guess, but assumes that
    the initial voltage bound is [0, MAX_VOLTAGE].

    This algorithm has been serialized into the following steps:

    At initialization:
        [left, right] = [0, MAX_VOLTAGE]        # Bounds
        [l1, l2] = [left, right]                # Goalposts
        powerL1 = 0
        powerL2 = 0
        cycle = 0

    Cycle 0: Set the left third goalpost.
        powerL2 = ArrVoltage * ArrCurrent
        if powerL1 > powerL2:                   # Restrict the goalpost
            right = l2
        else:
            left = l1
        l1 = (right - left) / 3 + left
        VREF = l1
        GOTO Cycle 1

    Cycle 1: Set the right third goalpost.
        powerL1 = ArrVoltage * ArrCurrent
        l2 = right - (right - left) / 3
        VREF = l2
        GOTO Cycle 0

    As this algorithm standalone can only support unimodal functions,
    it is a subcomponent for a larger, global MPPT algorithm.

    Note that this method always needs at least two cycles to perform one
    convergence iteration.
"""
# Library Imports.
from math import sqrt

# Custom Imports.
from models.mppt.mppt_algorihtms.localmpptalgorithms.localMpptAlgorithm import localMpptAlgorithm
import environment.environment as ENV
import pv.pv as PV


class ternary(localMpptAlgorithm):
    """
    The Ternary class is a derived class of LocalMPPTAlgorithm. Ternary utilizes
    splitting the search space into third to determine the position of the next
    VREF. It belongs to the set of divide and conquer algorithms.
    """

    # Convergence constant.
    q = 0.33  # Roughly the same as dividing by 3.

    def __init__(self, numCells=1, strideType="Fixed"):
        super(ternary, self).__init__(numCells, "Ternary", strideType)

        # Current algorithm internal cycle.
        self.cycle = 0

        # New left and right bounds.
        self.l1 = self.leftBound
        self.l2 = self.rightBound

        # Power associated with the new left and right bounds.
        self.powerL1 = 0
        self.powerL2 = 0

    def getReferenceVoltage(self, arrVoltage, environment: ENV, pv: PV):
        dataf = ENV.get_voxels()
        irrad = dataf["IRRAD"]
        temp = dataf["TEMP"]
        arrCurrent = PV.get_voltage(arrVoltage, irrad, temp)
        vRef = 0
        if self.cycle == 0:
            self.powerL2 = arrVoltage * arrCurrent
            if self.powerL1 > self.powerL2:
                self.rightBound = self.l2
            else:
                self.leftBound = self.l1
            self.l1 = (self.rightBound - self.leftBound) * self.q + self.leftBound
            vRef = self.l1
            self.cycle = 1
        elif self.cycle == 1:
            self.powerL1 = arrVoltage * arrCurrent
            self.l2 = self.rightBound - (self.rightBound - self.leftBound) * self.q
            vRef = self.l2
            self.cycle = 0
        else:
            raise Exception("self.cycle is not 0 or 1: " + self.cycle)

        return vRef

    def reset(self):
        super(ternary, self).reset()
        self.cycle = 0
        self.l1 = self.leftBound
        self.l2 = self.rightBound
        self.powerL1 = 0
        self.powerL2 = 0
