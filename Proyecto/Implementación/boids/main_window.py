"""
Main dashboard window.

Lays out the 3D viewport (large, left) alongside a right-hand sidebar holding
the control panel, live metrics and the real-time charts. Owns the QTimer that
drives the simulation loop and routes UI signals to the simulation.
"""

from __future__ import annotations

import time

from PyQt6 import QtCore, QtWidgets

from .charts import ChartsPanel
from .controls import ControlPanel
from .metrics_panel import MetricsPanel
from .simulation import BoidsSimulation
from .theme import DARK_STYLESHEET
from .viewport import FlockViewport

# Simulation / rendering cadence.
N_BOIDS = 250
BOUNDS = 130.0
FPS = 60
TIMER_MS = int(1000 / FPS)
# Charts are heavier to redraw, so sample them a few frames apart.
CHART_EVERY = 6


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("3D Boids Flocking Dashboard")
        self.resize(1480, 900)
        self.setStyleSheet(DARK_STYLESHEET)

        # --- Simulation --------------------------------------------------
        self.sim = BoidsSimulation(n_boids=N_BOIDS, bounds=BOUNDS)

        # Runtime accounting (only advances while running).
        self._running = False
        self._runtime = 0.0
        self._last_tick: float | None = None
        self._frame = 0

        # --- Widgets -----------------------------------------------------
        self.viewport = FlockViewport(bounds=BOUNDS)
        self.controls = ControlPanel(self.sim.params)
        self.metrics_panel = MetricsPanel()
        self.charts = ChartsPanel()

        self._build_layout()
        self._wire_signals()

        # --- Drive loop --------------------------------------------------
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(TIMER_MS)
        self.timer.timeout.connect(self._on_tick)

        # Render the initial (paused) state once.
        self._render_frame()
        self.statusBar().showMessage("Ready — press Start to begin the simulation.")
        self._set_running(False)

    # ------------------------------------------------------------------ #
    # Layout
    # ------------------------------------------------------------------ #
    def _build_layout(self) -> None:
        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)

        # Left: the big 3D viewport.
        splitter.addWidget(self.viewport)

        # Right: a scrollable sidebar of panels.
        sidebar = QtWidgets.QWidget()
        side_layout = QtWidgets.QVBoxLayout(sidebar)
        side_layout.setContentsMargins(8, 8, 8, 8)
        side_layout.setSpacing(10)
        side_layout.addWidget(self.controls)
        side_layout.addWidget(self.metrics_panel)
        side_layout.addWidget(self.charts, stretch=1)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(sidebar)
        scroll.setMinimumWidth(380)
        scroll.setMaximumWidth(460)
        splitter.addWidget(scroll)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 0)
        splitter.setSizes([1080, 400])

        self.setCentralWidget(splitter)

    def _wire_signals(self) -> None:
        self.controls.startClicked.connect(self.start)
        self.controls.pauseClicked.connect(self.pause)
        self.controls.resetClicked.connect(self.reset)
        self.controls.paramChanged.connect(self._on_param_changed)

    # ------------------------------------------------------------------ #
    # Transport controls
    # ------------------------------------------------------------------ #
    def start(self) -> None:
        if not self._running:
            self._last_tick = time.perf_counter()
            self.timer.start()
            self._set_running(True)
            self.statusBar().showMessage("Running…")

    def pause(self) -> None:
        if self._running:
            self.timer.stop()
            self._set_running(False)
            self.statusBar().showMessage("Paused.")

    def reset(self) -> None:
        self.timer.stop()
        self.sim.reset()
        self._runtime = 0.0
        self._last_tick = None
        self._frame = 0
        self.charts.clear()
        self._set_running(False)
        self._render_frame()
        self.statusBar().showMessage("Reset — press Start to begin again.")

    def _set_running(self, running: bool) -> None:
        self._running = running
        self.controls.start_btn.setEnabled(not running)
        self.controls.pause_btn.setEnabled(running)

    # ------------------------------------------------------------------ #
    # Parameter editing
    # ------------------------------------------------------------------ #
    def _on_param_changed(self, attr: str, value: float) -> None:
        setattr(self.sim.params, attr, value)

    # ------------------------------------------------------------------ #
    # Main loop
    # ------------------------------------------------------------------ #
    def _on_tick(self) -> None:
        now = time.perf_counter()
        if self._last_tick is not None:
            self._runtime += now - self._last_tick
        self._last_tick = now

        self.sim.step()
        self._render_frame()
        self._frame += 1

        if self._frame % CHART_EVERY == 0:
            m = self.sim.metrics
            self.charts.append(
                self._runtime, m.avg_speed, m.avg_neighbor_dist, m.cluster_count
            )

    def _render_frame(self) -> None:
        self.viewport.update_boids(self.sim.pos, self.sim.vel)
        self.metrics_panel.update_metrics(self.sim.metrics, self._runtime)

    # ------------------------------------------------------------------ #
    # Shutdown
    # ------------------------------------------------------------------ #
    def closeEvent(self, event) -> None:  # noqa: N802 (Qt naming)
        self.timer.stop()
        super().closeEvent(event)
