"""
BisectionStride.py

Author: Praneel Murali & Nash Wu (2023)
Created: 09/30/23
Description: Implementation of the Bisection Stride perturbation function.

The BisectionStride class implements the perturbation function
discussed in the following paper:

    Bisection Method Based Modified Perturb and Observe MPPT
    Algorithm for a PV Generation System with an Interleaved,
    Isolated DC-DC Converter (T. Anuradha et al.)

    Section 4, Proposed Modified P&O Algorithm (Bisection Method)

    This paper uses the slope of the P-V curve in order to make
    estimations on where and how much the VREF should go in order
    to reach VMPP.

    In particular, they use the following piecewise function.

    dV = V - V_old
    dP = P - P_old
    stride = f(V)
    f(V) = (V + V_old) / 2 - V_old  , dP/dV < 0
           dV                       , dP/dV > 0

    The behavior of this function is relatively straight forward.
    On the left side of the P-V curve, where the slope is positive,
    advance by a linear change in voltage. On the right side, where
    the slope is negative, take the average of the current and previous
    voltage and the stride is the difference between the average and
    the previous voltage.

    Afnan Mir and I have further optimized this stride function for
    use in our simulations: we make the portion of the piecewise function
    that refers to the left side of the P-V curve dependent on the slope
    of the curve.

    By doing this, and applying a constant multiplier (to make sure we
    don't jump too far at a time), this stride function allows us to
    converge much faster (and surprisingly steadier) to the VMPP.

    Our new piecewise function is the following:

    f(V) = stride_min                   , |dV| < error1, |dP| < error2 (we use 0.01, 0.1, respectively)
           (V + V_old) / 2 - V_old      , dP/dV < 0
           dP / dV * slope_multiplier   , dP/dV > 0

    stride_min is a constant defined by the user.
"""
# Library Imports.


# Custom Imports.
import environment.environment as ENV
from models.mppt.mppt_algorihtms.stride import stride
import pv.pv as PV


class bisectionStride(stride):
    """
    Derived class of Stride seeking to jump to the VMPP at all times.
    """

    def __init__(self, minStride=0.01, VMPP=0.621, error=0.05, slopeMultiplier=0.01):
        """
        Sets up the initial source parameters.

        Parameters
        ----------
        minStride: float
            The minimum value of the stride, if applicable.
        slopeMultiplier: float
            The multiplier that dictates how large the stride is calculated when
            on the left side of the P-V curve. Empirically determined.
        """
        super(bisectionStride, self).__init__("Bisection", minStride, VMPP, error)

        # Constant for determining convergence speed on the left side of the VMPP.
        self.slopeMultiplier = slopeMultiplier

        # Constant for selecting the minimum power and voltage difference.
        self._minPowDiff = 0.01
        self._minVoltDiff = 0.001

    def getStride(self, arrVoltage, environment: ENV, pv: PV):
        dataf = ENV.get_voxels()
        irrad = dataf["IRRAD"]
        temp = dataf["TEMP"]
        arrCurrent = PV.get_voltage(arrVoltage, irrad, temp)
        pIn = arrVoltage * arrCurrent
        dV = arrVoltage - self.vOld
        dP = pIn - self.pOld

        stride = 0
        if abs(dP) >= self._minPowDiff and abs(dV) >= self._minVoltDiff:
            slope = dP / dV
            if slope < 0:
                stride = (arrVoltage + self.vOld) / 2 - self.vOld
            elif slope > 0:
                stride = slope * self.slopeMultiplier

        self.vOld = arrVoltage
        self.pOld = pIn
        return max(abs(stride), self._minStride)
