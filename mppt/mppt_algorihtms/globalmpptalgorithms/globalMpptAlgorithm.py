"""
GlobalMPPTAlgorithm.py

Author: Afnan Mir, Array Lead (2021).
Contact: afnanmir@utexas.edu
Created: 02/06/2021
Last Modified: 02/27/2021

Description: Implementation of the GlobalMPPTAlgorithm class.
"""
# Library Imports.


# Custom Imports.
from mppt.mppt_algorihtms.localmpptalgorithms.localMpptAlgorithm import LocalMpptAlgorithm
from mppt.mppt_algorihtms.localmpptalgorithms.pando import PandO
from mppt.mppt_algorihtms.localmpptalgorithms.ic import IC
from mppt.mppt_algorihtms.localmpptalgorithms.fc import FC
from mppt.mppt_algorihtms.localmpptalgorithms.ternary import Ternary
from mppt.mppt_algorihtms.localmpptalgorithms.golden import Golden
from mppt.mppt_algorihtms.localmpptalgorithms.bisection import Bisection
import environment.environment as ENV
import pv.pv as PV

class GlobalMPPTAlgorithm:
    """
    The GlobalMPPTAlgorithm class and derived classes attempt to solve P-V
    curves with multiple local maxima and a single global maxima.
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

    def __init__(
        self,
        numCells=1,
        MPPTGlobalAlgoType="Default",
        MPPTLocalAlgoType="Default",
        strideType="Fixed",
    ):
        """
        Sets up the initial source parameters.

        Parameters
        ----------
        numCells: int
            The number of cells that should be accounted for in the MPPT
            algorithm.
        MPPTGlobalAlgoType: String
            The name of the global MPPT algorithm type.
        MPPTLocalAlgoType: String
            The name of the local MPPT algorithm type.
        strideType: String
            The name of the stride algorithm type.
        TODO: Add stride argument to voltage sweep constructor.
        """
        GlobalMPPTAlgorithm.MAX_VOLTAGE = round(
            GlobalMPPTAlgorithm.MAX_VOLTAGE_PER_CELL * numCells, 2
        )
        self._MPPTGlobalAlgoType = MPPTGlobalAlgoType

        if MPPTLocalAlgoType == "Bisection":
            self._model = Bisection(numCells, strideType)
        elif MPPTLocalAlgoType == "FC":
            self._model = FC(numCells, strideType)
        elif MPPTLocalAlgoType == "Golden":
            self._model = Golden(numCells, strideType)
        elif MPPTLocalAlgoType == "IC":
            self._model = IC(numCells, strideType)
        elif MPPTLocalAlgoType == "PandO":
            self._model = PandO(numCells, strideType)
        elif MPPTLocalAlgoType == "Ternary":
            self._model = Ternary(numCells, strideType)
        elif MPPTLocalAlgoType == "Default":
            self._model = LocalMpptAlgorithm(numCells, MPPTLocalAlgoType, strideType)
        else:
            self._model = LocalMpptAlgorithm(numCells, MPPTLocalAlgoType, strideType)

        self.vOld = 0.0
        self.iOld = 0.0
        self.tOld = 0.0
        self.irrOld = 0.0
        self.pOld = 0.0

    def getReferenceVoltage(self, arrVoltage, environment: ENV, pv: PV):
        """
        Calculates the reference voltage output for the given PVSource output.
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
        float The reference voltage that should be applied to the array in the
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
        dataf = environment.get_voxels()
        irrad = dataf["IRRAD"]
        temp = dataf["TEMP"]
        arrCurrent = pv.get_voltage(arrVoltage, irrad, temp)
        vRef = self._model.getReferenceVoltage(
            arrVoltage, arrCurrent, irrad, temp
        )
        (left, right) = self._getBounds()
        if vRef < left:
            vRef = left
        if vRef > right:
            vRef = right

        return vRef

    def reset(self):
        """
        Resets any internal variables set by the MPPT algorithm during operation.
        """
        self._model.reset()
        self.vOld = 0.0
        self.iOld = 0.0
        self.pOld = 0.0
        self.irrOld = 0.0
        self.tOld = 0.0

    def getGlobalMPPTType(self):
        """
        Returns the Global MPPT algorithm type used for the simulation.

        Return
        ------
        String: Model type name.
        """
        return self._MPPTGlobalAlgoType

    def getLocalMPPTType(self):
        """
        Returns the Local MPPT type used for the simulation.

        Return
        ------
        String: Model type name.
        """
        return self._model.getLocalMPPTType()

    def getStrideType(self):
        """
        Returns the Stride model type used for the simulation.

        Return
        ------
        String: Model type name.
        """
        return self._model.getStrideType()

    def _getBounds(self):
        """
        Finds left and right bounds for the global maximum of the P-V curve.

        Parameters
        ----------
        None

        Return
        ------
        The left and right bounds for the global maximum of the P-V curve.
        """
        return (0.0, GlobalMPPTAlgorithm.MAX_VOLTAGE)
