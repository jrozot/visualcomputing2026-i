"""
Control panel: Start / Pause / Reset buttons plus the live parameter sliders.

Each slider maps an integer Qt range onto a float parameter range and emits a
float value when moved, so the simulation can be retuned in real time.
"""

from __future__ import annotations

from PyQt6 import QtCore, QtWidgets

from .simulation import SimulationParams


class FloatSlider(QtWidgets.QWidget):
    """A labelled horizontal slider that emits float values.

    Internally a QSlider works in integer steps; we map those onto the
    [minimum, maximum] float range with `steps` resolution.
    """

    valueChanged = QtCore.pyqtSignal(float)

    def __init__(
        self,
        label: str,
        minimum: float,
        maximum: float,
        value: float,
        steps: int = 1000,
        decimals: int = 2,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._min = float(minimum)
        self._max = float(maximum)
        self._steps = int(steps)
        self._decimals = decimals

        self._name = QtWidgets.QLabel(label)
        self._value_label = QtWidgets.QLabel()
        self._value_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter
        )
        self._value_label.setMinimumWidth(48)

        self._slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self._slider.setMinimum(0)
        self._slider.setMaximum(self._steps)
        self._slider.valueChanged.connect(self._on_slider)

        header = QtWidgets.QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        header.addWidget(self._name)
        header.addStretch(1)
        header.addWidget(self._value_label)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(2)
        layout.addLayout(header)
        layout.addWidget(self._slider)

        self.set_value(value)

    def _on_slider(self, raw: int) -> None:
        value = self._raw_to_value(raw)
        self._value_label.setText(f"{value:.{self._decimals}f}")
        self.valueChanged.emit(value)

    def _raw_to_value(self, raw: int) -> float:
        frac = raw / self._steps
        return self._min + frac * (self._max - self._min)

    def set_value(self, value: float) -> None:
        value = max(self._min, min(self._max, value))
        frac = (value - self._min) / (self._max - self._min)
        self._slider.blockSignals(True)
        self._slider.setValue(round(frac * self._steps))
        self._slider.blockSignals(False)
        self._value_label.setText(f"{value:.{self._decimals}f}")


class ControlPanel(QtWidgets.QGroupBox):
    """Buttons + sliders. Emits signals consumed by the main window."""

    startClicked = QtCore.pyqtSignal()
    pauseClicked = QtCore.pyqtSignal()
    resetClicked = QtCore.pyqtSignal()
    paramChanged = QtCore.pyqtSignal(str, float)  # (attr name, value)

    def __init__(self, params: SimulationParams, parent=None) -> None:
        super().__init__("Controls", parent)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(8)

        # --- Transport buttons -------------------------------------------
        btn_row = QtWidgets.QHBoxLayout()
        self.start_btn = QtWidgets.QPushButton("▶  Start")
        self.pause_btn = QtWidgets.QPushButton("❚❚  Pause")
        self.reset_btn = QtWidgets.QPushButton("↻  Reset")
        self.start_btn.clicked.connect(self.startClicked)
        self.pause_btn.clicked.connect(self.pauseClicked)
        self.reset_btn.clicked.connect(self.resetClicked)
        for b in (self.start_btn, self.pause_btn, self.reset_btn):
            b.setMinimumHeight(34)
            btn_row.addWidget(b)
        layout.addLayout(btn_row)

        sep = QtWidgets.QFrame()
        sep.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        sep.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        layout.addWidget(sep)

        # --- Parameter sliders -------------------------------------------
        self._sliders: dict[str, FloatSlider] = {}
        self._add_slider(layout, "speed", "Boid Speed", 0.3, 3.0, params.max_speed,
                         "max_speed")
        self._add_slider(layout, "perception", "Perception Radius", 5.0, 45.0,
                         params.perception, "perception", decimals=1)
        self._add_slider(layout, "separation", "Separation Strength", 0.0, 3.5,
                         params.separation, "separation")
        self._add_slider(layout, "alignment", "Alignment Strength", 0.0, 3.5,
                         params.alignment, "alignment")
        self._add_slider(layout, "cohesion", "Cohesion Strength", 0.0, 3.5,
                         params.cohesion, "cohesion")

        layout.addStretch(1)

    def _add_slider(self, layout, key, label, lo, hi, value, attr, decimals=2):
        slider = FloatSlider(label, lo, hi, value, decimals=decimals)
        slider.valueChanged.connect(
            lambda v, a=attr: self.paramChanged.emit(a, v)
        )
        self._sliders[key] = slider
        layout.addWidget(slider)
