"""
Real-time charts using pyqtgraph.

Three stacked plots share a rolling time window and update live:

    * Average Speed vs Time
    * Average Neighbour Distance vs Time
    * Cluster Count vs Time

History is kept in fixed-length deques so memory use stays bounded as the
simulation runs indefinitely.
"""

from __future__ import annotations

from collections import deque

import pyqtgraph as pg
from PyQt6 import QtWidgets

# History window: number of samples retained per series.
HISTORY = 400


class ChartsPanel(QtWidgets.QGroupBox):
    """A vertical stack of three live pyqtgraph plots."""

    def __init__(self, parent=None) -> None:
        super().__init__("Live Charts", parent)

        pg.setConfigOption("background", (18, 20, 26))
        pg.setConfigOption("foreground", (170, 180, 195))

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(8)

        self._t: deque[float] = deque(maxlen=HISTORY)
        self._speed: deque[float] = deque(maxlen=HISTORY)
        self._nn: deque[float] = deque(maxlen=HISTORY)
        self._clusters: deque[float] = deque(maxlen=HISTORY)

        self._speed_curve = self._make_plot(
            layout, "Average Speed", "speed", (0, 220, 220)
        )
        self._nn_curve = self._make_plot(
            layout, "Avg Neighbour Distance", "distance", (120, 200, 255)
        )
        self._cluster_curve = self._make_plot(
            layout, "Cluster Count", "clusters", (255, 170, 90)
        )

    def _make_plot(self, layout, title, ylabel, color):
        plot = pg.PlotWidget(title=title)
        plot.setMinimumHeight(120)
        plot.showGrid(x=True, y=True, alpha=0.25)
        plot.setLabel("bottom", "time", units="s")
        plot.setLabel("left", ylabel)
        plot.setMouseEnabled(x=False, y=False)
        plot.setMenuEnabled(False)
        pen = pg.mkPen(color=color, width=2)
        curve = plot.plot([], [], pen=pen)
        layout.addWidget(plot)
        return curve

    def append(
        self,
        t: float,
        avg_speed: float,
        avg_nn: float,
        cluster_count: float,
    ) -> None:
        self._t.append(t)
        self._speed.append(avg_speed)
        self._nn.append(avg_nn)
        self._clusters.append(cluster_count)

        ts = list(self._t)
        self._speed_curve.setData(ts, list(self._speed))
        self._nn_curve.setData(ts, list(self._nn))
        self._cluster_curve.setData(ts, list(self._clusters))

    def clear(self) -> None:
        for d in (self._t, self._speed, self._nn, self._clusters):
            d.clear()
        for c in (self._speed_curve, self._nn_curve, self._cluster_curve):
            c.setData([], [])
