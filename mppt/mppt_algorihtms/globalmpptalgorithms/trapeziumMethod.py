"""
TrapeziumMethod.py

Author: Afnan Mir, Array Lead (2021).
Contact: afnanmir@utexas.edu
Created: 10/16/2021
Last Modified: 10/16/2021

Description: Implementation of Trapezoidal Sum Optimization GlobalMPPTAlgortihm.
"""

# library imports
import random
import math

# custom imports
from mppt.mppt_algorihtms.globalmpptalgorithms.globalMpptAlgorithm import GlobalMPPTAlgorithm
import environment.environment as ENV
import pv.pv as PV


class TrapeziumMethod(GlobalMPPTAlgorithm):
    """
    Class to implement the Trapezium Method Algorithm for Maximum Power Point Tracking
    (https://ieeexplore.ieee.org/document/9314467)
    """
    
    DV = .05
    def __init__(self, numCells=1, MPPTLocalAlgoType="Default", strideType="Variable"):
        super(TrapeziumMethod, self).__init__(
            numCells, "Trapezium Method", MPPTLocalAlgoType, strideType
        )  
        """
        Constructor for a Trapezoid in the Trapezium Method algorithm

        Parameters
        ----------
        numCells : int
            number of cells
        MPPTLocalAlgoType : str
            the local algorithm to use
        strideType : str
            Stride to use for perturb and observe

        Returns
        -------
        None.
        """
        self.pref = 0
        self.aref = 0
        self.vref = 0
        self.aold = 0
        self.findingtrapezoids = True
        self.startLocal = True
        self.kick = True
        self.areas=[]
    def getReferenceVoltage(self, arrVoltage, environment: ENV, pv: PV):
        """
        Method that updates output voltage of the array.
        
        Parameters
        ----------
        arrVoltage : float
            Array voltage of the current cycle
        arrCurrent : float
            Array current of the current cycle
        irradiance : float
            Irradiance of the current cycle
        temperature : float
            Temperature of the current cycle

        Returns
        -------
        vref : float
            array voltage to output
        """
        dataf = environment.get_voxels()
        irrad = dataf["IRRAD"]
        temp = dataf["TEMP"]
        arrCurrent = pv.get_voltage(arrVoltage, irrad, temp)
        vref = arrVoltage
        arrpower = arrVoltage * arrCurrent
        if (self.findingtrapezoids == True):
            # print("Hello")
            currentarea = (TrapeziumMethod.DV * 0.5)*(arrpower +  self.pOld) 
            self.areas.append({currentarea:[self.vOld, arrVoltage]})
            DA = currentarea - self.aold
            DP = arrpower - self.pOld
            if (DA > 0):
                self.aref = currentarea
                self.pref = self.pOld
                self.vref = self.vOld
                if (currentarea >= self.aref and arrpower >= self.pref):
                    self.pref = arrpower
                    self.vref = arrVoltage
            else:
                if (currentarea >= self.aref and arrpower >= self.pref):
                    self.pref = arrpower
                    self.vref = arrVoltage
            vref = vref + TrapeziumMethod.DV
            self.vOld = arrVoltage
            self.pOld = arrpower
            self.aold = currentarea
            if(vref > GlobalMPPTAlgorithm.MAX_VOLTAGE):
                self.findingtrapezoids = False
                print(self.aref, currentarea)
                return self.vref
            return vref
        else:
            if self.startLocal:
                print(self.areas)
                vref = self.vref
                self.startLocal = False  # start converging to global maximum
                self._model.setup(self.vref, 0, GlobalMPPTAlgorithm.MAX_VOLTAGE)
            elif self.kick:  # start local mppt algorithm.
                vref = arrVoltage + 0.02
                self.kick = False
                self.vOld = arrVoltage
                self.pOld = arrCurrent * arrVoltage
                self._model._strideModel.vOld = arrVoltage
                self._model._strideModel.pOld = self.pOld
                self.iOld = arrCurrent
            else:
                vref = self._model.getReferenceVoltage(arrVoltage,arrCurrent,irrad,temp)
                needsChange = self.checkEnvironmentalChanges(irrad)
                print(self.runningHistory)
                if needsChange:
                    vref = 0
                    self.pref = 0
                    self.aref = 0
                    self.vref = 0
                    self.aold = 0
                    self.findingtrapezoids = True
                    self.startLocal = True  
                    self.kick = True
                    self.runningHistory.clear()
                    return vref
            return vref
            
def reset(self):
    """
    Method to reset the pipeline

    Parameters
    ----------
    None.

    Returns
    -------
    None.
    """
    super(TrapeziumMethod,self).reset()
    # super(TrapeziumMethod, self).reset()
    self.pref = 0
    self.aref = 0
    self.vref = 0
    self.aold = 0
    self.findingtrapezoids = True
    self.startLocal = True  
    self.kick = True