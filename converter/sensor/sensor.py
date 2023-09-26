"""
@file       sensor.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Models sensor readings from the source and load.
@version    0.4.0
@date       2023-09-25
"""

from pv.pv_system import PVSystem


class SourceSensor:
    def __init__(self, system: PVSystem) -> None:
        self._system = system

    def inject_noise(self):
        pass

    def get_voltage(self):
        pass

    def get_current(self):
        pass


class LoadSensor:
    def __init__(self, load) -> None:
        self._load = load

    def inject_noise(self):
        pass

    def get_voltage(self):
        pass

    def get_current(self):
        pass
