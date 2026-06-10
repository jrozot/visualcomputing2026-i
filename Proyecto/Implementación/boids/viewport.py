"""
3D OpenGL viewport for the flock, built on pyqtgraph's GLViewWidget.

Boids are drawn as oriented line segments (short "darts") aligned with each
boid's velocity, plus a bright head point, so direction of travel is always
visually obvious. The scene also contains a ground grid, XYZ axis indicators
and the wire-frame bounding cube. The widget keeps GLViewWidget's built-in
mouse controls (rotate / zoom / pan).
"""

from __future__ import annotations

import numpy as np
import pyqtgraph.opengl as gl
from PyQt6 import QtGui


# Colours (RGBA, 0..1)
BG_COLOR = (0.04, 0.05, 0.08, 1.0)
GRID_COLOR = (0.20, 0.30, 0.40, 0.45)
CUBE_COLOR = (0.25, 0.45, 0.65, 0.55)
AXIS_LEN_RATIO = 0.28


class FlockViewport(gl.GLViewWidget):
    """OpenGL scene that renders and updates the boids each frame."""

    def __init__(self, bounds: float, parent=None) -> None:
        super().__init__(parent)
        self.bounds = float(bounds)

        self.setBackgroundColor(QtGui.QColor.fromRgbF(*BG_COLOR))
        self.setCameraPosition(distance=self.bounds * 2.1, elevation=22, azimuth=45)
        # Look at the centre of the cube instead of the origin corner.
        self.opts["center"] = QtGui.QVector3D(
            self.bounds / 2, self.bounds / 2, self.bounds / 2
        )

        self._build_static_scene()
        self._build_boid_items()

    # ------------------------------------------------------------------ #
    # Static scene elements
    # ------------------------------------------------------------------ #
    def _build_static_scene(self) -> None:
        b = self.bounds

        # Ground grid on the floor of the cube.
        grid = gl.GLGridItem()
        grid.setSize(x=b, y=b)
        grid.setSpacing(x=b / 16, y=b / 16)
        grid.translate(b / 2, b / 2, 0)
        grid.setColor(QtGui.QColor.fromRgbF(*GRID_COLOR))
        self.addItem(grid)

        # XYZ axis indicator anchored at the cube origin corner.
        axis = gl.GLAxisItem()
        axis.setSize(x=b * AXIS_LEN_RATIO, y=b * AXIS_LEN_RATIO, z=b * AXIS_LEN_RATIO)
        self.addItem(axis)

        # Wire-frame bounding cube (12 edges).
        self.addItem(self._make_cube_wireframe(b))

    def _make_cube_wireframe(self, b: float) -> gl.GLLinePlotItem:
        # 8 corners of the cube.
        c = np.array(
            [
                [0, 0, 0], [b, 0, 0], [b, b, 0], [0, b, 0],
                [0, 0, b], [b, 0, b], [b, b, b], [0, b, b],
            ],
            dtype=np.float32,
        )
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),   # bottom
            (4, 5), (5, 6), (6, 7), (7, 4),   # top
            (0, 4), (1, 5), (2, 6), (3, 7),   # verticals
        ]
        pts = np.empty((len(edges) * 2, 3), dtype=np.float32)
        for k, (a, d) in enumerate(edges):
            pts[2 * k] = c[a]
            pts[2 * k + 1] = c[d]
        return gl.GLLinePlotItem(
            pos=pts, color=CUBE_COLOR, width=1.4, mode="lines", antialias=True
        )

    # ------------------------------------------------------------------ #
    # Dynamic boid items
    # ------------------------------------------------------------------ #
    def _build_boid_items(self) -> None:
        # Body segments: one line per boid (2 vertices each).
        self.body_item = gl.GLLinePlotItem(
            mode="lines", width=2.2, antialias=True
        )
        self.addItem(self.body_item)

        # Head points: a bright dot at the front of each boid.
        self.head_item = gl.GLScatterPlotItem(
            size=5.0, pxMode=True
        )
        self.head_item.setGLOptions("translucent")
        self.addItem(self.head_item)

    def update_boids(self, pos: np.ndarray, vel: np.ndarray) -> None:
        """Refresh the rendered geometry from the latest sim state."""
        n = pos.shape[0]

        speed = np.linalg.norm(vel, axis=1, keepdims=True)
        direction = vel / np.maximum(speed, 1e-9)

        # Dart length scales gently with the cube size.
        length = self.bounds * 0.022
        tail = pos - direction * (length * 0.5)
        head = pos + direction * (length * 0.5)

        # Interleave tail/head into a (2N, 3) segment buffer.
        segs = np.empty((2 * n, 3), dtype=np.float32)
        segs[0::2] = tail
        segs[1::2] = head

        # Colour each boid from deep blue (slow) to bright cyan (fast).
        colors = self._speed_colors(speed.ravel())
        seg_colors = np.repeat(colors, 2, axis=0)

        self.body_item.setData(pos=segs, color=seg_colors)
        self.head_item.setData(pos=head.astype(np.float32), color=colors)

    def _speed_colors(self, speed: np.ndarray) -> np.ndarray:
        """Map speed to a blue -> cyan gradient (RGBA float array)."""
        if speed.size == 0:
            return np.empty((0, 4), dtype=np.float32)
        lo, hi = speed.min(), speed.max()
        t = (speed - lo) / max(hi - lo, 1e-9)  # 0..1

        colors = np.empty((speed.size, 4), dtype=np.float32)
        colors[:, 0] = 0.10 + 0.20 * t          # R: subtle
        colors[:, 1] = 0.55 + 0.45 * t          # G: rises toward cyan
        colors[:, 2] = 0.85 + 0.15 * t          # B: always strong
        colors[:, 3] = 1.0                       # A
        return colors
