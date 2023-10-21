"""
SimulatedAnnealing.py

Author: Afnan Mir, Array Lead (2021).
Contact: afnanmir@utexas.edu
Created: 02/06/2021
Last Modified: 02/27/2021

Description: First Iteration of Simulated Annealing implementation trying to use a look forward approach. **NOT CURRENT ITERATION DO NOT USE**
"""
# Library Imports.
import random
import math

# Custom Imports.
from models.mppt.mppt_algorihtms.globalmpptalgorithms.globalMpptAlgorithm import globalMpptAlgorithm
import environment.environment as ENV
import pv.pv as PV


class simulatedAnnealing(globalMpptAlgorithm):
    """
    The Simulated Annealing class is a derived concrete class of GlobalAlgorithm
    implementing the Simulated Annealing algorithm. It randomly samples values from
    the range of voltages and chooses the operating point of the voltage either if the power
    at the sampled point is greater than the power of the current operating point, or based
    on a calculated probability. It then identifies the global maxima using a LocalMPPTAlgorithm.
    """

    ALPHA = (
        0.8
    )  # geometric cooling constant. What you multiply the temperature by to decrease the temperature.
    MIN_TEMP = 0.3  # the temperature at which you stop searching
    INIT_TEMP = 25  # initial value of the temperature
    k = 15

    def __init__(self, numCells=1, MPPTLocalAlgoType="Default", strideType="Fixed"):
        super(simulatedAnnealing, self).__init__(
            numCells, "Simulated Annealing", MPPTLocalAlgoType, strideType
        )
        # The 'temperature' tells us how likely we are to accept a change even if the power decreases

        self.temp = simulatedAnnealing.INIT_TEMP
        self.cycle = 0
        self._PVEnv = ENV.get_voxels()
        self._PVSource = PVSource()
        self._PVEnv.setupModel(
            source="TwoCellsWithDiode.json", maxCycles=200
        )  # cource models needed to look forward
        self._PVSource.setupModel(modelType="Ideal")
        self.startLocal = (
            True
        )  # boolean variable used to kickstart the local algorithm.

    def getReferenceVoltage(self, arrVoltage, arrCurrent, irradiance, temperature):
        vRef = arrVoltage
        if self.temp > simulatedAnnealing.MIN_TEMP:
            if self.cycle == 0:
                vRef = round(
                    random.uniform(0, globalMpptAlgorithm.MAX_VOLTAGE), 2
                )  # first random sample and operating point
                self.cycle += 1
            else:
                arrPower = arrVoltage * arrCurrent
                sample = round(random.uniform(0, globalMpptAlgorithm.MAX_VOLTAGE), 2)
                modules = self._PVEnv.getSourceDefinition(sample)
                sourceCurrent = self._PVSource.getSourceCurrent(modules)
                power = (
                    sample * sourceCurrent
                )  # find a sample voltage and current pair and calculate the hypothetical power at that point
                if power > arrPower:
                    vRef = sample  # if it is greater, make it the new operating point
                else:
                    # if not greater, choose to go to this operating point if a calculated probability is met.
                    p_r = math.exp(
                        simulatedAnnealing.k * (power - arrPower) / self.temp
                    )
                    diceRoll = random.random()
                    if diceRoll < p_r:
                        vRef = sample
                if self.cycle % 4 == 0:  # temperature is decreased every 4 cycles
                    self.temp = self.temp * simulatedAnnealing.ALPHA
                self.cycle += 1
        else:
            if self.startLocal:  # kick start local algorithm
                vRef = arrVoltage + 0.02
                self.startLocal = False
                self.vOld = arrVoltage
                self.pOld = arrCurrent * arrVoltage
                self._model._strideModel.vOld = arrVoltage
                self._model._strideModel.pOld = self.pOld
                self.iOld = arrCurrent
            else:
                # print("Hello")
                # print("arrVoltage: " + str(arrVoltage) )
                # print("SELF.POLD: "+ str(self.pOld))
                vRef = self._model.getReferenceVoltage(
                    arrVoltage, arrCurrent, irradiance, temperature
                )
                if (
                    len(self.runningHistory) == 10
                ):  # running average sample to check if we have had a drastic change in the power output
                    # previousAverage = sum(self.runningHistory)/len(self.runningHistory)
                    self.runningHistory.remove(
                        self.runningHistory[0]
                    )  # pop the oldest value out and add the new value in
                    self.runningHistory.append(arrCurrent * arrVoltage)
                    if len(self.pastHistories) == 10:
                        pastAverage = self.pastHistories[0]
                        self.pastHistories.remove(self.pastHistories[0])
                        self.pastHistories.append(
                            sum(self.runningHistory) / len(self.runningHistory)
                        )  # all past averages
                        if (
                            self.pastHistories[len(self.pastHistories) - 1]
                            - pastAverage
                        ) / pastAverage <= -0.3:  # if drastic change in power output, then reinitialize the simulated annealing
                            vRef = 0
                            self.cycle = 0
                            self.temp = simulatedAnnealing.INIT_TEMP
                            self.startLocal = True
                            self.runningHistory.clear()
                            self.pastHistories.clear()
                            return vRef
                    else:
                        self.pastHistories.append(
                            sum(self.runningHistory) / len(self.runningHistory)
                        )
                # averageNow = sum(self.runningHistory)/len(self.runningHistory)
                # if((averageNow - previousAverage)/previousAverage <= -0.1):
                #     self.sweeping = True
                #     vRef = 0
                #     self.setup = True
                #     self.runningHistory.clear()
                #     return vRef

                else:
                    self.runningHistory.append(arrCurrent * arrVoltage)

        return vRef
        # print(self.cycle)
        # if self.temp >0.2:
        #     if self.cycle == 0:
        #         vRef = round(random.random()*GlobalMPPTAlgorithm.MAX_VOLTAGE,2)
        #         self.cycle+=1
        #         self.vOld = arrVoltage
        #         self.iOld = arrCurrent
        #         self.pOld = arrVoltage * arrCurrent
        #         self.irrOld = irradiance
        #         self.tOld = temperature
        #     else:
        #         arrPower = arrVoltage * arrCurrent
        #         print("Vold: "+ str(self.vOld) + " arrVoltage: " +str(arrVoltage))
        #         print("Array Power: " + str(arrPower) + " Old Power: "+ str(self.pOld))
        #         if arrPower > self.pOld:
        #             self.vOld = arrVoltage
        #             self.iOld = arrCurrent
        #             self.pOld = arrVoltage * arrCurrent
        #             self.irrOld = irradiance
        #             self.tOld = temperature
        #         else:
        #             p_r = math.exp(SimulatedAnnealing.k*(arrPower - self.pOld)/self.temp)
        #             print("Vold: "+ str(self.vOld) + " arrVoltage: " +str(arrVoltage))
        #             print("Array Power: " + str(arrPower) + " Old Power: "+ str(self.pOld) + " P_r: "+str(p_r))
        #             diceRoll = random.random()
        #             if(diceRoll < p_r):
        #                 self.vOld = arrVoltage
        #                 self.iOld = arrCurrent
        #                 self.pOld = arrVoltage * arrCurrent
        #                 self.irrOld = irradiance
        #                 self.tOld = temperature
        #         if self.cycle == 4:
        #             self.temp = self.temp * SimulatedAnnealing.ALPHA
        #             self.cycle = 0
        #         self.cycle+=1
        #         searchRange = GlobalMPPTAlgorithm.MAX_VOLTAGE * (self.temp/SimulatedAnnealing.INIT_TEMP)
        #         leftBound = max(self.vOld - (searchRange/2),0)
        #         rightBound = min(self.vOld + (searchRange/2), GlobalMPPTAlgorithm.MAX_VOLTAGE)
        #         vRef = round(random.uniform(leftBound, rightBound),2)
        # return vRef

    def reset(self):
        super(simulatedAnnealing, self).reset()
        self.temp = 25