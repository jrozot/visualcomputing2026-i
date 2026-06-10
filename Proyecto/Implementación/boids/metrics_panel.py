"""
Live metrics panel: a compact grid of name/value labels that is refreshed
every frame from the simulation's latest metrics snapshot.
"""

from __future__ import annotations

from PyQt6 import QtCore, QtWidgets

from .simulation import SimulationMetrics


class MetricsPanel(QtWidgets.QGroupBox):
    """Displays the live scalar metrics of the flock."""

    def __init__(self, parent=None) -> None:
        super().__init__("Live Metrics", parent)

        grid = QtWidgets.QGridLayout(self)
        grid.setVerticalSpacing(6)
        grid.setHorizontalSpacing(12)

        self._value_labels: dict[str, QtWidgets.QLabel] = {}
        rows = [
            ("count", "Total boids"),
            ("avg_speed", "Average speed"),
            ("avg_nn", "Avg neighbour dist"),
            ("clusters", "Cluster count"),
            ("runtime", "Runtime"),
        ]
        for r, (key, label) in enumerate(rows):
            name = QtWidgets.QLabel(label)
            value = QtWidgets.QLabel("—")
            value.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignRight
                | QtCore.Qt.AlignmentFlag.AlignVCenter
            )
            value.setProperty("metricValue", True)
            font = value.font()
            font.setPointSize(font.pointSize() + 2)
            font.setBold(True)
            value.setFont(font)

            grid.addWidget(name, r, 0)
            grid.addWidget(value, r, 1)
            self._value_labels[key] = value

        grid.setColumnStretch(1, 1)

    def update_metrics(self, metrics: SimulationMetrics, runtime_s: float) -> None:
        self._value_labels["count"].setText(f"{metrics.count}")
        self._value_labels["avg_speed"].setText(f"{metrics.avg_speed:.3f}")
        self._value_labels["avg_nn"].setText(f"{metrics.avg_neighbor_dist:.2f}")
        self._value_labels["clusters"].setText(f"{metrics.cluster_count}")
        self._value_labels["runtime"].setText(self._fmt_time(runtime_s))

    @staticmethod
    def _fmt_time(seconds: float) -> str:
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        if h:
            return f"{h:d}:{m:02d}:{s:02d}"
        return f"{m:02d}:{s:02d}"
