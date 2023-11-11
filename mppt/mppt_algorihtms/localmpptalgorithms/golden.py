"""
Golden.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/19/20
Last Modified: 02/27/21
Description: Implementation of the Golden Section Search algorithm.

The implementation of this algorithm is based on the wikipedia page for the
Golden Section Search: https://en.wikipedia.org/wiki/Golden-section_search

    The Golden Section search seeks to find the min/max of a unimodal
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

    Cycle 0: Determine our first reference voltage.
        l1 = right - (right - left) * phi
        VREF = l1
        GOTO Cycle 1

    Cycle 1: Determine our second reference voltage.
        powerL1 = ArrVoltage * ArrCurrent
        l2 = (right - left) * phi + left
        VREF = l2
        GOTO Cycle X

    Cycle X:
        powerL2 = ArrVoltage * ArrCurrent

    Cycle X + 1:
        powerL1 = ArrVoltage * ArrCurrent

    Cycle X, X + 1:
        if powerL1 > powerL2:                   # Move right goalpost.
            right = l2                          # Cut the right bound to the right goalpost.
            l2 = l1                             # Set right goalpost voltage, power to the left goalpost's.
            powerL2 = powerL1

            l1 = right - (right - left) * phi   # Set left goalpost to a new spot.
            VREF = l1
            GOTO Cycle X + 1
        else:                                   # Move left goalpost
            left = l1                           # Cut the left bound to the left goalpost.
            l1 = l2                             # Set left goalpost voltage, power to the right goalpost's.
            powerL1 = powerL2

            l2 = (right - left) * phi + left    # Set right goalpost to a new spot.
            VREF = l2
            GOTO Cycle X

    As this algorithm standalone can only support unimodal functions,
    it is a subcomponent for a larger, global MPPT algorithm.

    Note that this method needs two starting cycles to begin convergence.
    Unlike Ternary Search, it can converge every cycle rather than every
    other cycles.
"""
# Library Imports.
from math import sqrt

# Custom Imports.
from mppt.mppt_algorihtms.localmpptalgorithms.localMpptAlgorithm import LocalMpptAlgorithm
import environment.environment as ENV
import pv.pv as PV


class Golden(LocalMpptAlgorithm):
    """
    The Golden class is a derived class that determines a VREF to apply
    over PSource to maximize the power generated. Golden splitting the search
    space into gtheold ratio to determine the position of the next
    VREF. It belongs to the set of divide and conquer algorithms.
    """

    phi = (sqrt(5) + 1) / 2 - 1

    def __init__(self, numCells=1, strideType="Fixed"):
        super(Golden, self).__init__(numCells, "Golden", strideType)

        # Current algorithm internal cycle.
        self.cycle = 0

        # New left and right bounds.
        self.l1 = self.leftBound
        self.l2 = self.rightBound

        # Power associated with the new left and right bounds.
        self.powerL1 = 0
        self.powerL2 = 0

    def getReferenceVoltage(self, arrVoltage, environment: ENV, pv: PV):
        dataf = environment.get_voxels()
        irrad = dataf["IRRAD"]
        temp = dataf["TEMP"]
        arrCurrent = pv.get_voltage(arrVoltage, irrad, temp)
        vRef = 0

        if self.cycle == 0:
            self.l1 = self.rightBound - (self.rightBound - self.leftBound) * Golden.phi
            vRef = self.l1
            self.cycle = 1
        elif self.cycle == 1:
            self.powerL1 = arrVoltage * arrCurrent
            self.l2 = (self.rightBound - self.leftBound) * Golden.phi + self.leftBound
            vRef = self.l2
            self.cycle = 2
        else:
            if self.cycle == 2:
                self.powerL2 = arrVoltage * arrCurrent
            elif self.cycle == 3:
                self.powerL1 = arrVoltage * arrCurrent
            else:
                raise Exception("self.cycle is not 2 or 3: " + self.cycle)

            if self.powerL1 > self.powerL2:
                self.rightBound = self.l2
                self.l2 = self.l1
                self.powerL2 = self.powerL1

                self.l1 = (
                    self.rightBound - (self.rightBound - self.leftBound) * Golden.phi
                )
                vRef = self.l1
                self.cycle = 3
            else:
                self.leftBound = self.l1
                self.l1 = self.l2
                self.powerL1 = self.powerL2

                self.l2 = (
                    self.rightBound - self.leftBound
                ) * Golden.phi + self.leftBound
                vRef = self.l2
                self.cycle = 2

        return vRef

    def reset(self):
        super(Golden, self).reset()
        self.cycle = 0
        self.l1 = self.leftBound
        self.l2 = self.rightBound
        self.powerL1 = 0
        self.powerL2 = 0