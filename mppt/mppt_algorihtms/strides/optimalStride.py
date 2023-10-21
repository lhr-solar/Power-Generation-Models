"""
OptimalStride.py

Author: Praneel Murali & Nash Wu (2023)
Created: 09/30/23
Description: Implementation of the Optimal Stride perturbation function.

The OptimalStride class implements the perturbation function
discussed in the following paper:

    Optimized Adaptive Perturb and Observe Maximum Power Point Tracking  
    Control for Photovoltaic Generation (Piegari et al.)

    Section 3, Adaptive Pertubation Function for P&O Algorithm

    We can define any stride function as follow:
        stride = f(V_best - V) + dV_min
    
    Optimally, 
        f(V_best - V) = |V_best - V| 
    
    where V_best is an estimate of the MPP of the solar cell.

    Since V_best is unlikely to match physical conditions, we need
    to add an error estimation constant, dV_min.

    We can define an inequality for dV_min:
        dV_min > k^2 / (2 * (1 - k)) * V_best
    
    where k is the percent error. In our implementation, we set this 
    to .05 for 5% error.
"""
# Library Imports.


# Custom Imports.
import environment.environment as ENV
from models.mppt.mppt_algorihtms.strides.stride import stride
import pv.pv as PV


class optimalStride(stride):
    def __init__(self, minStride=0.01, VMPP=0.621, error=0.05):
        super(optimalStride, self).__init__("Optimal", minStride, VMPP, error)

    def getStride(self, arrVoltage, environment: ENV, pv: PV):
        dataf = ENV.get_voxels()
        irrad = dataf["IRRAD"]
        temp = dataf["TEMP"]
        arrCurrent = PV.get_voltage(arrVoltage, irrad, temp)
        minStride = self.error * self.error * self.VMPP / (2 * (1 - self.error))
        stride = abs(self.VMPP - arrVoltage)
        return stride + minStride
