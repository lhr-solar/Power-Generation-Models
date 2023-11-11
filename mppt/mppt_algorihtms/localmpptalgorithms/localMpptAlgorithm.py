"""
LocalMPPTAlgorithm.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/18/20
Last Modified: 02/27/22
Description: Implementation of the LocalMPPTAlgorithm class.
"""
# Library Imports.


# Custom Imports.
from mppt.mppt_algorihtms.strides.stride import Stride
from mppt.mppt_algorihtms.strides.adaptiveStride import AdaptiveStride
from mppt.mppt_algorihtms.strides.bisectionStride import BisectionStride
from mppt.mppt_algorihtms.strides.optimalStride import OptimalStride
import environment.environment as ENV
import pv.pv as PV



class LocalMpptAlgorithm:
    """
    The LocalMPPTAlgorithm class provides the base API for derived classes to
    calculate or predict voltage setpoints that would maximize the output power
    of the PVSource given a set of input conditions.
    """

    # The upper voltage bound that should be predicted by any model. We expect
    # the PV to always be at open circuit voltage at this point. Adjustable
    # based on the number of cells determined from the initialization.
    MAX_VOLTAGE = 100

    # The upper voltage bound for a single cell that should be predicted by any
    # model. We expect the PV to always be at open circuit voltage at this
    # point. The reference value was determined from experimentation from the
    # Maxeon Gen III Bin Le1 solar cells, which have a rated voltage of .721V at
    # standard conditions.
    MAX_VOLTAGE_PER_CELL = 0.8

    def __init__(self, numCells=1, MPPTLocalAlgoType="Default", strideType="Fixed", environment: ENV = None, pv: PV = None):
        """
        Sets up the initial source parameters.

        Parameters
        ----------
        numCells: int
            The number of cells that should be accounted for in the MPPT
            algorithm.
        MPPTLocalAlgoType: String
            The name of the local MPPT algorithm type.
        strideType: String
            The name of the stride algorithm type.
        """
        LocalMpptAlgorithm.MAX_VOLTAGE = (
            numCells * LocalMpptAlgorithm.MAX_VOLTAGE_PER_CELL
        )
        self._MPPTLocalAlgoType = MPPTLocalAlgoType

        if strideType == "Adaptive":
            self._strideModel = AdaptiveStride()
        elif strideType == "Bisection":
            self._strideModel = BisectionStride()
        elif strideType == "Optimal":
            self._strideModel = OptimalStride()
        elif strideType == "Fixed":
            self._strideModel = Stride()
        else:
            self._strideModel = Stride()

        # Previous array voltage value.
        self.vOld = 0.0

        # Previous array current voltage.
        self.iOld = 0.0

        # Previous array power voltage.
        self.pOld = 0.0

        # Previous array irradiance value.
        self.irrOld = 0.0

        # Previous array temperature value.
        self.tOld = 0.0

        # Bounds for the LocalMPPTAlgorithm. A naive assumption is that the
        # function within these bounds are unimodal.
        self.leftBound = 0
        dataf = environment.get_voxels()
        irrad = dataf["IRRAD"]
        temp = dataf["TEMP"]
        f,s = pv.get_edge(irrad, temp)
        self.rightBound = f[0]
        

    def setup(self, VMPP=0.621, leftBound=0, rightBound=100, environment: ENV = None, pv: PV = None):
        """
        Reinitializes the predicted parameters for the local MPPT algorithms context.

        Parameters
        ----------
        VMPP: float
            The voltage of the Maximum Power Point.
        """
        self.leftBound = leftBound
        dataf = environment.get_voxels()
        irrad = dataf["IRRAD"]
        temp = dataf["TEMP"]
        f,s = pv.get_edge(irrad, temp)
        self.rightBound = f[0]
        self._strideModel.setup(VMPP)

    def getReferenceVoltage(self, arrVoltage, environment: ENV, pv: PV):
        """
        Calculates the reference voltage output for the given PVSource input.
        May use prior history.

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
        float: The reference voltage that should be applied to the array in the
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
        return 0.0

    def reset(self):
        """
        Resets any internal variables set by the MPPT algorithm during operation.
        """
        self._strideModel.reset()
        self.vOld = 0.0
        self.iOld = 0.0
        self.pOld = 0.0
        self.irrOld = 0.0
        self.tOld = 0.0
        self.leftBound = 0
        self.rightBound = LocalMpptAlgorithm.MAX_VOLTAGE

    def getLocalMPPTType(self):
        """
        Returns the Local MPPT algorithm type used for the simulation.

        Return
        ------
        String: Model type name.
        """
        return self._MPPTLocalAlgoType

    def getStrideType(self):
        """
        Returns the Stride model type used for the simulation.

        Return
        ------
        String: Model type name.
        """
        return self._strideModel.getStrideType()
