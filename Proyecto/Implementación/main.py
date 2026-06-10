"""
Real-time 3D Flocking (Boids) Simulation — Desktop Dashboard.

Entry point. Launches the PyQt6 application and shows the main dashboard
window containing the 3D OpenGL viewport, control panel, live metrics and
real-time charts.

Run with:
    python main.py
"""

import sys

# pyqtgraph must be told which Qt binding to use *before* it is imported
# anywhere else, so we set it up here at the very top of the program.
import pyqtgraph as pg

pg.setConfigOptions(useOpenGL=True, antialias=True)

from PyQt6 import QtWidgets

from boids.main_window import MainWindow


def main() -> int:
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("3D Boids Flocking Dashboard")

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
