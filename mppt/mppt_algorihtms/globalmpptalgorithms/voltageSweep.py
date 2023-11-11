"""
VoltageSweep.py

Author: Afnan Mir, Array Lead (2021).
Contact: afnanmir@utexas.edu
Created: 02/06/2021
Last Modified: 02/08/2021

Description: The Voltage Sweep class is a derived concrete class of
GlobalAlgorithm implementing the Voltage Sweep algorithm. It increments through
the range of all possible voltage values (the "sweep"), finding all local maxima
of the P-V curve. It then identifies the global maxima using a LocalMPPTAlgorithm.
"""
# Library Imports.


# Custom Imports.
from mppt.mppt_algorihtms.globalmpptalgorithms.globalMpptAlgorithm import GlobalMPPTAlgorithm
import environment.environment as ENV
import pv.pv as PV


class VoltageSweep(GlobalMPPTAlgorithm):
    """
    The Voltage Sweep class is a derived concrete class of GlobalAlgorithm
    implementing the Voltage Sweep algorithm. It increments through the range of
    all possible voltage values (the "sweep"), finding all local maxima of the
    P-V curve. It then identifies the global maxima using a LocalMPPTAlgorithm.
    """

    def __init__(self, numCells=1, MPPTLocalAlgoType="Default", strideType="Fixed"):
        super(VoltageSweep, self).__init__(
            numCells, "Voltage Sweep", MPPTLocalAlgoType, strideType
        )

        # Stores all the voltage values of the local maxima.
        self.voltage_peaks = []
        self.voltage_troughs = [0]

        # Stores the power values of the local maxima.
        self.power_peaks = []

        # Whether we are in sweeping mode or not.
        self.sweeping = True

        # Checks to see if we were increasing before.
        self.increasing = True

        # Sets the bounds for the first cycle of the LocalMPPTAlgorithm
        self.setup = True

        self.stride = 0.01
        self.vOld = 0.0
        self.iOld = 0.0
        self.tOld = 0.0
        self.irrOld = 0.0
        self.pOld = 0.0
    #TODO: round the values at a lower level like PVCell or MPPTAlgorithm instead of rounding the hell out of everything here
    def getReferenceVoltage(self, arrVoltage, environment: ENV, pv: PV):
        dataf = ENV.get_voxels()
        irrad = dataf["IRRAD"]
        temp = dataf["TEMP"]
        arrCurrent = PV.get_voltage(arrVoltage, irrad, temp)
        vRef = round(arrVoltage,2)
        if round(arrVoltage,2) < GlobalMPPTAlgorithm.MAX_VOLTAGE and self.sweeping:
            vRef = round(self._sweep(round(arrVoltage,2), arrCurrent, irrad, temp),2)
        else:
            (lBound, rBound) = self._getBounds()
            if self.setup:
                self.sweeping = False
                maxPower = max(self.power_peaks)
                maxVoltage = self.voltage_peaks[self.power_peaks.index(maxPower)]
                #TODO: Look at this later
                self._model.setup(maxVoltage, lBound, rBound)
                self.setup = False

            if arrVoltage >= GlobalMPPTAlgorithm.MAX_VOLTAGE:
                vRef = lBound
            elif arrVoltage == lBound:
                #TODO: Optimize this out
                vRef = lBound + 0.02
            else:
                vRef = self._model.getReferenceVoltage(
                    arrVoltage, arrCurrent, irrad, temp
                )
                if vRef < lBound:
                    vRef = lBound
                if vRef > rBound:
                    vRef = rBound
        return vRef

    def _sweep(self, arrVoltage, environment: ENV, pv: PV):
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
        """
        dataf = ENV.get_voxels()
        irrad = dataf["IRRAD"]
        temp = dataf["TEMP"]
        arrCurrent = PV.get_voltage(arrVoltage, irrad, temp)
        pIn = arrVoltage * arrCurrent
        vRef = arrVoltage
        if pIn < self.pOld and self.increasing:
            self.voltage_peaks.append(self.vOld)
            self.power_peaks.append(self.pOld)
            self.increasing = False
        elif pIn >= self.pOld and not self.increasing:
            self.increasing = True
            self.voltage_troughs.append(self.vOld)
        vRef += self.stride
        self.iOld = arrCurrent
        self.vOld = arrVoltage
        self.pOld = pIn
        self.tOld = temp
        self.irrOld = irrad
        return vRef

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
        maxPower = max(self.power_peaks)
        index = self.power_peaks.index(maxPower)
        maxVoltage = self.voltage_peaks[index]
        (leftBound, rightBound) = (
            0,
            0
        )
        if(index == 0):
            leftBound = round(self.voltage_peaks[index]/2,2)
        else:
            leftBound = max(self.voltage_troughs[index], (self.voltage_peaks[index] + self.voltage_peaks[index-1])/2)
        if(index == len(self.power_peaks)-1):
            rightBound = GlobalMPPTAlgorithm.MAX_VOLTAGE
        else:
            rightBound = min(self.voltage_troughs[index + 1] - 0.02, (self.voltage_peaks[index] + self.voltage_peaks[index+1])/2)
        #TODO: 0.1 is a placeholder for now. Will probably have to be some factor of the max voltage
        return (leftBound, rightBound)

    def reset(self):
        super(VoltageSweep, self).reset()
        self.stride = 0.01
        self.voltage_peaks = [0]
        self.power_peaks = [0]
        self.sweeping = True
        self.increasing = True
        self.setup = True
