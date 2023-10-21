"""
Firefly.py

Author: Afnan Mir, Array Lead (2021).
Contact: afnanmir@utexas.edu
Created: 08/08/2021
Last Modified: 09/25/2021

Description: Implementation of Firefly Global Maximum Power Point Tracking Algortihm.
"""

# library imports
from hashlib import new
import random
import math

# custom imports
from models.mppt.mppt_algorihtms.globalmpptalgorithms.globalMpptAlgorithm import globalMpptAlgorithm
import environment.environment as ENV
import pv.pv as PV

class firefly:
    """
    Class represents a firefly in the Firefly optimization algorithm. It requries a brightness
    level, which is the value of the objective function (power) and a position (a voltage).
    """
    
    B_0 = 1
    N = 2
    GAMMA = 2
    ALPHA = 0.5

    def __init__(self,pos):
        """
        Constructor for a Firefly object.

        Parameters
        ----------
        pos : float
            The initial voltage of the firefly.

        Returns
        -------
        None
        """

        self.position = pos
        self.brightness = 0
    
    def getPosition(self):
        """
        Returns the current voltage of the firefly.

        Parameters
        ----------
        None

        Returns
        -------
        self.position : float
            The current voltage of the firefly.
        """

        return self.position
    
    def getBrightness(self):
        """
        Returns the current brightness (power) of the firefly.

        Parameters
        ----------
        None

        Returns
        -------
        self.brightness : float
            The current brightness/power of the firefly
        """

        return self.brightness

    def getAttractionLevel(self, otherFirefly):
        """
        Returns the attraction between the firefly and another firefly based on the following equation:
            a = B_0 * exp(-GAMMA * (abs(X - X_i)^2))
            X = current position of firefly
            X_i = current position of other firefly
            B_0 = initial brightness condition
            GAMMA = an absorption constant.
        
        Parameters
        ----------
        otherFirefly : Firefly
            The other firefly to compare it with

        Returns
        -------
        a : float
            The attractiveness between the two fireflies.
        """

        r_pq = abs(self.position - otherFirefly.position)
        return firefly.B_0 * math.exp(-firefly.GAMMA*(r_pq**2))
    
    def getNextPosition(self, otherFirefly):
        """
        Returns the next position the firefly should go to based on the conditions of the maximum brightness firefly.
        It is based on the following equation:
            X_{t+1} = X_t + beta*(X_t - X_i) + a(rand - 1/2)
            X_t is the current position
            X_i is the current position of the maximum brightness firefly
            a is a constant
            rand is a random number between 0 and 1
            beta is the attractiveness between the two fireflies.
        
        Parameters
        otherFirefly : Firefly
            The maximum brightness firefly

        Returns
        -------
        newPos : float
            The new position of the firefly.
        """

        beta = self.getAttractionLevel(otherFirefly)
        dist = self.position - otherFirefly.position
        newPos = self.position + beta*dist + firefly.ALPHA*(random.random() - 0.5)
        return newPos
    
class fireflyAlgorithm(globalMpptAlgorithm):
    NUM_FIREFLIES = 6

    def __init__(self, numCells=1, MPPTLocalAlgoType="Default",strideType="Fixed"):
        super(firefly, self).__init__(
            numCells, "Firefly", MPPTLocalAlgoType, strideType
        )
        self.fireflies = []
        interval = globalMpptAlgorithm.MAX_VOLTAGE / (fireflyAlgorithm.NUM_FIREFLIES + 1)
        for i in range(fireflyAlgorithm.NUM_FIREFLIES):
            self.fireflies.append(firefly(interval*i))
        self.startLocal = True
        self._setup = True
        self.kick = True

    def getReferenceVoltage(self, arrVoltage, environment: ENV, pv: PV):
        dataf = ENV.get_voxels()
        irrad = dataf["IRRAD"]
        temp = dataf["TEMP"]
        arrCurrent = PV.get_voltage(arrVoltage, irrad, temp)
        return arrVoltage

    def reset(self):
        return 

        