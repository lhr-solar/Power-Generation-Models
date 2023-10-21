"""
IC.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/21/20
Last Modified: 2/27/21
Description: Implementation of the Incremental Conductance algorithm.

The implementation of this algorithm is based on the folowing paper:

    Incremental Conductance Based Maximum Power Point Tracking (MPPT)
    for Photovoltaic System (Bhaskar et Lokanadham.)

    Section 5, Incremental Conductance MPPT

    Given a P-V curve of the solar cell, we can identify three region
    of interest given its incremental versus instantaneous conductance:

        dI/dV = - I/V   At MPP
        dI/dV > - I/V   Left of MPP
        dI/dV < - I/V   Right of MPP

    The algorithm is then fairly straightforward. Identify which region
    of interest we are in, and move to the direction of the MPP using a
    stride function.
"""
# Library Imports.


# Custom Imports.
from models.mppt.mppt_algorihtms.localmpptalgorithms.localMpptAlgorithm import localMpptAlgorithm
import environment.environment as ENV
import pv.pv as PV


class ic(localMpptAlgorithm):
    """
    The IC (Incremental Conductance) class is a derived class of
    LocalMPPTAlgorithm, utilizing the comparison of the incremental conductance
    to the instantaneous conductance. It belongs to the set of hill climbing
    algorithms.
    """

    # Error tuning parameter.
    error = 0.01

    def __init__(self, numCells=1, strideType="Fixed"):
        super(ic, self).__init__(numCells, "IC", strideType)

    def getReferenceVoltage(self, arrVoltage, environment: ENV, pv: PV):
        dataf = ENV.get_voxels()
        irrad = dataf["IRRAD"]
        temp = dataf["TEMP"]
        arrCurrent = PV.get_voltage(arrVoltage, irrad, temp)
        # Compute secondary values.
        dI = arrCurrent - self.iOld
        dV = arrVoltage - self.vOld

        # Determine the stride.
        stride = self._strideModel.getStride(
            arrVoltage, arrCurrent, irrad, temp
        )

        # Determine the direction of movement and VREF.
        vRef = arrVoltage
        if abs(dI * arrVoltage + arrCurrent * dV) < ic.error:  # At MPP.
            pass
        elif dI * arrVoltage + arrCurrent * dV > ic.error:  # Left of MPP.
            vRef += stride
        elif dI * arrVoltage + arrCurrent * dV < -ic.error:  # Right o MPP.
            vRef -= stride
        else:
            raise Exception("[IC][getReferenceVoltage] Invalid region of interest.")

        # Update dependent values.
        self.iOld = arrCurrent
        self.vOld = arrVoltage

        return vRef
