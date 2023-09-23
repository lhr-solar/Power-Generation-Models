"""
@file       module.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Model interface for a PV module.
@version    0.4.0
@date       2023-09-23
"""
import sys

sys.path.extend(["."])

import pyqtgraph as pg
import numpy as np
import pandas as pd
from PySide6 import QtWidgets
from common.graph import Graph
import common.config as CONFIG

class Module:
    def __init__(self) -> None:
        pass