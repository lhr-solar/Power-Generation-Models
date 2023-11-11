"""
Stride.py

Author: Praneel Murali & Nash Wu (2023)
Created: 09/30/23
Description: Implementation of the Stride class.
"""
# Library Imports.


# Custom Imports.
import environment.environment as ENVIRONMENT
import pv.pv as PV

class Stride:
    """
    The Stride class provides the base API for derived classes to
    calculate the stride (change of VREF) for various MPPT algorithms.

    By default, the stride function implemented by the concrete base class is a
    fixed stride.
    """

    def __init__(self, strideType="Fixed", minStride=0.01, VMPP=0.621, error=0.05):
        """
        Sets up the initial source parameters.

        Parameters
        ----------
        strideType: String
            The name of the stride type.
        minStride: float
            The minimum value of the stride, if applicable.
        VMPP: float
            Our estimation of the PVSource voltage at the maximum power point.
            Note that the default value is for a single cell and is an
            experimental estimate; according to Sunniva the cell VMPP is 0.621.
        error: float
            The minimum error percentage of V_best to serve as our minimum
            stride.
        """
        # Name of the explicit stride function used.
        self._strideType = strideType

        # The minimum stride attempted in any iteration.
        self._minStride = minStride

        # The previous iteration characteristics.
        self.vOld = 0.0
        self.iOld = 0.0
        self.pOld = 0.0
        self.irrOld = 0.0
        self.tOld = 0.0

        # The anticipated VMPP to aim for.
        self.VMPP = VMPP

        # User defined error for determining variable minimum stride distance.
        self.error = error

    def getStride(self, environment, pv):
        """
        Calculates the voltage stride for the given PVSource output.
        May use prior history.

        By default, we output a fixed stride.

        Parameters
        ----------
        arrVoltage: float
            Array voltage in V.
        arrCurrent: float
            Array current in A.
        irradiance: float
            Irradiance in W/M^2 (G)
        temperature: float
            Cell Temperature in C.

        Return
        ------
        float The change in voltage that should be applied to the array in the
        next cycle.

        Assumptions
        -----------
        This method is called sequentially in increasing cycle order. The
        arrVoltage and arrCurrent are expected to have stabilized to the
        reference voltage applied in the last cycle, if any.

        Note that the second assumption doesn't hold true in reality, as large
        changes in reference voltage may mean the array does not converge to
        steady state behavior by the next MPPT cycle. This should always be
        considered in the algorithms.
        """
        return self._minStride

    def reset(self):
        """
        Resets any internal variables set by the MPPT algorithm during operation.
        """
        self.vOld = 0.0
        self.iOld = 0.0
        self.pOld = 0.0
        self.irrOld = 0.0
        self.tOld = 0.0

    def getStrideType(self):
        """
        Returns the Stride model type used for the simulation.

        Return
        ------
        String: Stride type name.
        """
        return self._strideType


