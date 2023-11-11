"""
PandO.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/18/20
Last Modified: 02/27/21

Description: Implementation of the PandO hill climbing algorithm.
"""
# Library Imports.


# Custom Imports.
from mppt.mppt_algorihtms.localmpptalgorithms.localMpptAlgorithm import LocalMpptAlgorithm
import environment.environment as ENV
import pv.pv as PV


class PandO(LocalMpptAlgorithm):
    """
    The PandO (Perturb and Observe) class is a derived class of
    LocalMPPTAlgorithm, utilizing the change of power and change of voltage over
    time to determine the direction of movement and stride of the next reference
    voltage. It belongs to the classification of hill climbing algorithms.
    """

    def __init__(self, numCells=1, strideType="Fixed"):
        super(PandO, self).__init__(numCells, "PandO", strideType)
        self._minVoltage = .05

    def getReferenceVoltage(self, arrVoltage, environment: ENV, pv: PV):
        dataf = environment.get_voxels()
        irrad = dataf["IRRAD"]
        temp = dataf["TEMP"]
        arrCurrent = pv.get_voltage(arrVoltage, irrad, temp)
        # Compute secondary values.
        pIn = arrVoltage * arrCurrent
        dV = arrVoltage - self.vOld
        dP = pIn - self.pOld

        # Determine the stride.
        stride = self._strideModel.getStride(
            arrVoltage, arrCurrent, irrad, temp
        )

        # Determine the direction of movement and VREF.
        vRef = arrVoltage
        if dP > 0:
            if dV > 0:  # Increase vRef.
                vRef += stride
                print('Right dp='+str(round(dP, 3))+' dV='+str(round(dV, 3)), end='\t')
            elif dV < 0:  # Decrease vRef.
                vRef -= stride
                print('Left dp='+str(round(dP, 3))+' dV='+str(round(dV, 3)), end='\t')
        else:
            if dV > 0:  # Decrease vRef.
                vRef -= stride
                print('Left dp='+str(round(dP, 3))+' dV='+str(round(dV, 3)), end='\t')
            elif dV < 0:  # Increase vRef.
                vRef += stride
                print('Right dp='+str(round(dP, 3))+' dV='+str(round(dV, 3)), end='\t')

        print(" to ", round(vRef, 3))

        # Update dependent values.
        self.vOld = arrVoltage
        self.pOld = pIn

        return vRef

