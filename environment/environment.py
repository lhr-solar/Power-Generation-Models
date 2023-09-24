"""
@file       environment.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Models the external environment for the photovoltaics.
@version    0.4.0
@date       2023-09-22
"""
import sys

sys.path.extend(["."])
sys.path.extend([".."])

import random
import numpy as np
import pandas as pd
import pyqtgraph as pg
from PySide6 import QtWidgets
import common.config as CONFIG


class Environment:
    """Environment class models external conditions experienced by the
    photovoltaic system."""

    def __init__(self, filepath: str = None) -> None:
        """Initialize a new environment instance.

        Args:
            filepath (str, optional): Filepath for environment data file.
                Defaults to None.
        """
        if filepath != None:
            self.df = self.load_env(filepath)
        else:
            self.df = pd.DataFrame(
                data={
                    "X": [],
                    "Y": [],
                    "T": [],
                    "IRRAD": [],
                    "TEMP": [],
                }
            )
        self.np = self.df.to_numpy()

    def load_env(self, filepath: str) -> pd.DataFrame:
        """Load from an environmental file that represents a complete or
        incomplete set of voxels.

        Args:
            filepath (str): Path of file to load.

        Returns:
            pd.DataFrame: Pandas Dataframe of file.
        """
        return pd.read_csv(filepath)

    def save_env(self, filepath: str) -> None:
        """Save into an environmental file that represents a complete or incomplete
        set of voxels.

        Args:
            filepath (str): Path of file to save/overwrite.
        """
        self.get_voxels()
        self.df.to_csv(filepath, index=None)

    def add_voxel(self, X: int, Y: int, T: int, irrad: float, temp: float) -> None:
        """Add a voxel to our current environment.

        Args:
            X (int): X axis position.
            Y (int): Y axis position.
            T (int): Point in time since 0s (start of simulation).
            irrad (float): Irradiance (W/m^2) at this place, at this time.
            temp (float): Temperature (K) at this place, at this time.
        """
        self.np = np.vstack((self.np, [X, Y, T, irrad, temp]))

    def add_voxels(
        self,
        X: list[int],
        Y: list[int],
        T: list[int],
        irrad: list[float],
        temp: list[float],
    ) -> None:
        """Add a set of voxels to our current environment.

        Args:
            X (list, int): X axis position.
            Y (list, int): Y axis position.
            T (list, int): Point in time since 0s (start of simulation).
            irrad (list, float): Irradiance (W/m^2) at this place, at this time.
            temp (list, float): Temperature (K) at this place, at this time.
        """
        self.np = np.vstack((self.np, np.array([X, Y, T, irrad, temp]).transpose()))

    def gen_voxels(self, func) -> None:
        """Generate voxels from a function.

        Args:
            func ([[int, int, int, float, float]] func(void)): Function that
            explicitly returns inputs like add_voxels. Must return a set of
            Voxels.
        """
        self.np = np.vstack((self.np, func()))

    def interp_voxels(self) -> None:
        """TODO: Interpolate voxels not explicitly specified in the environment based on
        existing voxels.
        """
        return

    def vis_voxels(self) -> None:
        """Visualize voxels in the current environment using PySide6, PyQtGraph.
        Runs through time.
        """
        if not QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()

        win = QtWidgets.QMainWindow()
        win.setGeometry(0, 0, 1080, 480)
        win.setWindowTitle("Environment")
        view = pg.GraphicsLayoutWidget()

        # Get first timeslice.
        df = self.get_voxels()

        # Plot first mesh on irradiance plot.
        plot_irrad = view.addPlot()
        mesh_irrad = pg.PColorMeshItem(levels=(0, 1000), enableAutoLevels=True)
        plot_irrad.addItem(mesh_irrad, row=0, col=0, rowspan=1, colspan=1)

        # Plot first mesh on temperature plot.
        plot_temp = view.addPlot()
        mesh_temp = pg.PColorMeshItem(levels=(273.15, 398.15), enableAutoLevels=False)
        plot_temp.addItem(mesh_temp)

        # Cycle through time and update the meshes.
        def update():
            def _get_slice(df: pd.DataFrame, idx: int):
                df = df[df["T"] == idx]
                if df["X"].empty:
                    return df["IRRAD"], df["TEMP"], None, None
                else:
                    return (
                        df["IRRAD"],
                        df["TEMP"],
                        int(df["X"].max()) + 1,
                        int(df["Y"].max()) + 1,
                    )

            update.time_idx += 1

            irrad, temp, max_x, max_y = _get_slice(df, update.time_idx)
            if max_x == None:
                update.time_idx = 0
            else:
                mesh_irrad.setData(irrad.to_numpy().reshape(max_x, max_y))
                mesh_temp.setData(temp.to_numpy().reshape(max_x, max_y))

        update.time_idx = 0

        timer = pg.QtCore.QTimer()
        timer.timeout.connect(update)
        timer.start(1000 / CONFIG.FPS)

        # Run the application
        win.setCentralWidget(view)
        win.show()
        app.exec()

    def get_voxels(self) -> pd.DataFrame:
        """Get all voxels, sorted by X, Y, T axes.

        Returns:
            pd.DataFrame: Pandas Dataframe of all voxels.
        """
        self.df = pd.DataFrame(
            self.np,
            columns=[
                f"X",
                f"Y",
                f"T",
                "IRRAD",
                "TEMP",
            ],
        )
        self.df = self.df.sort_values(by=["T", "X", "Y"])
        return self.df

    def get_voxel(self, X: int, Y: int, T: int) -> (float, float):
        """Get the voxel outputs associated with a set of voxel inputs.

        Args:
            X (int): X space coordinate.
            Y (int): Y space coordinate.
            Z (int): Z time coordinate.

        Returns:
            (float, float): Tuple of irradiance (W/m^2) and temperature (K).
        """
        self.df = pd.DataFrame(
            self.np,
            columns=[
                f"X",
                f"Y",
                f"T",
                "IRRAD",
                "TEMP",
            ],
        )

        voxel = self.df.loc[
            (self.df["X"] == X) & (self.df["Y"] == Y) & (self.df["T"] == T)
        ]
        return voxel.values.tolist()[0][3:]

    def get_voxels_slice(self, idx: int, axis: str = "T") -> pd.DataFrame:
        """Get a slice of voxels in some independent axis, sorted by X, Y, T
        axes.

        Args:
            idx (int): Idx of slice.
            axis (str): Axis to slice. Either 'X', or 'Y', 'T'. Default T.

        Returns:
            pd.DataFrame: Pandas DataFrame of associated environmental voxels.
        """
        if axis not in ["X", "Y", "T"]:
            return None

        self.get_voxels()
        df = self.df[self.df[axis] == idx]
        df = df.sort_values(by=["T", "X", "Y"])
        return df


if __name__ == "__main__":
    voxel = [0, 0, 0, 1000.0, 273.15]
    voxels = [
        [1, 0, 0, 1000.0, 273.15],
        [0, 1, 1, 1000.0, 273.15],
        [1, 1, 0, 1000.0, 273.15],
    ]

    env = Environment()
    print(env.get_voxels())
    env.add_voxel(*voxel)
    print(env.get_voxels())
    env.add_voxels(*np.transpose(voxels))
    print(env.get_voxels())
    print(env.get_voxel(0, 1, 1))

    def generator() -> list:
        rows, columns = 50, 50
        time = 500

        def get_irrad(x, y, t):
            irrad = x * y
            return max(0, min(irrad, 1000))

        def get_temp(x, y, t):
            temp = 298.15 + random.gauss(x * y * t / 500, 1)
            return max(273.15, min(temp, 398.15))

        return [
            [x, y, t, get_irrad(x, y, t), get_temp(x, y, t)]
            for t in range(time)
            for y in range(rows)
            for x in range(columns)
        ]

    # env = Environment()
    # env.gen_voxels(generator)
    # print(env.get_voxels_slice(1))
    # env.vis_voxels()
    # env.save_env("./test.csv")
