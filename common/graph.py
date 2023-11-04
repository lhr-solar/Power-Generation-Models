"""_summary_
@file       graph.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Generic graph plotting.
@version    0.4.0
@date       2023-05-13
"""

import sys

import pyqtgraph as pg
import pyqtgraph.opengl as gl

sys.path.extend([".."])

from common.utils import update


class Graph:
    def __init__(self, title, x_label, y_label, use_gl=False) -> None:
        self.setup_graph(title, x_label, y_label, use_gl)
        self.series = {}
        self.use_gl = use_gl

    def add_series(self, series, series_type) -> None:
        # Update data entry
        self.series.update(series)
        keys = list(series.keys())

        for key in keys:
            series = self.series[key]

            # Generate plot item
            match series_type:
                case "line":
                    if self.use_gl:
                        raise Exception("2D series for 3D Graph.")
                    plot_item = self.plot.plot(
                        x=series["x"],
                        y=series["y"],
                        pen=pg.mkPen(series["color"], width=1.5),
                        name=key,
                    )
                case "scatter":
                    if self.use_gl:
                        raise Exception("2D series for 3D Graph.")
                    plot_item = pg.ScatterPlotItem(
                        x=series["x"],
                        y=series["y"],
                        pen=pg.mkPen(series["color"], width=1.5),
                        size=5,
                        name=key,
                    )
                    self.plot.addItem(plot_item)
                case "3dscatter":
                    if not self.use_gl:
                        raise Exception("3D series for non 3D Graph.")

                    cm = series["colormap"]
                    colors = cm.map(series["voxels"][:, 2], mode=cm.FLOAT)

                    plot_item = gl.GLScatterPlotItem(
                        pos=series["voxels"], size=series["size"], color=colors
                    )
                    self.widget.addItem(plot_item)
                case _:
                    raise Exception("Invalid series type.")

            series["graph"] = plot_item

    def update_series(self, series) -> None:
        self.series = update(self.series, series)
        keys = list(series.keys())

        for key in keys:
            series = self.series[key]
            series["graph"].setData(
                x=series["x"],
                y=series["y"],
            )

    def remove_series(self, series) -> None:
        keys = list(series.keys())

        for key in keys:
            if key in self.series:
                # Clear from graph before deleting
                self.series[key]["graph"].clear()
                del self.series[key]

    def set_graph_range(self, x_range, y_range):
        self.plot.setXRange(*x_range)
        self.plot.setYRange(*y_range)

    def setup_graph(self, title, x_label, y_label, use_gl) -> None:
        if use_gl:
            widget = gl.GLViewWidget()
        else:
            widget = pg.GraphicsLayoutWidget()
            plot = widget.addPlot(title=title)
            plot.setLabel("bottom", x_label)
            plot.setLabel("left", y_label)
            plot.addLegend()
            plot.showGrid(x=True, y=True, alpha=1.0)
            self.plot = plot
        self.widget = widget

    def update_graph(self) -> None:
        for series in self.series.values():
            series["graph"].setData(
                x=series["x"],
                y=series["y"],
            )

    def get_graph(self):
        return self.widget
