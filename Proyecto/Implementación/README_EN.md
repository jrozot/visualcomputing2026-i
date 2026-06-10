# 3D Boids Flocking Dashboard

A real-time **3D flocking (Boids) simulation** rendered with OpenGL inside a
professional-looking desktop dashboard. Built with **PyQt6**, **pyqtgraph**
(OpenGL `GLViewWidget`) and **NumPy**. Everything runs locally.

## Features

- **Classic Reynolds Boids** — separation, alignment and cohesion.
- **3D bounded cube** with wrap-around (periodic) boundaries, using the
  minimum-image convention so boids interact across the edges.
- **~250 boids**, fully vectorised with NumPy for smooth animation.
- **OpenGL 3D viewport** with a ground grid, XYZ axis indicators and a
  wire-frame bounding cube. Boids are drawn as oriented "darts" coloured by
  speed (deep blue → bright cyan) so direction of travel is obvious.
- **Camera controls** — drag to rotate, scroll to zoom, middle-drag / shift-drag
  to pan (standard `GLViewWidget` controls).
- **Control panel** — Start / Pause / Reset plus live sliders for boid speed,
  perception radius and separation / alignment / cohesion strengths. Changes
  apply instantly.
- **Live metrics** — total boid count, average speed, average nearest-neighbour
  distance, estimated cluster count and simulation runtime.
- **Real-time charts** — average speed, average neighbour distance and cluster
  count over a rolling time window.
- **Dark theme** throughout.

## Project structure

```
.
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md
└── boids/                  # Application package
    ├── __init__.py
    ├── simulation.py       # Vectorised Boids simulation + metrics (NumPy)
    ├── viewport.py         # 3D OpenGL scene (GLViewWidget)
    ├── controls.py         # Buttons + live parameter sliders
    ├── metrics_panel.py    # Live scalar metrics readout
    ├── charts.py           # Real-time pyqtgraph charts
    ├── theme.py            # Dark Qt stylesheet
    └── main_window.py      # Dashboard layout + simulation loop
```

## Requirements

- Python **3.11+**
- A GPU/driver with basic OpenGL support (any typical laptop works).

## Installation & run

```bash
# (optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
python main.py
```

Press **Start** to begin the simulation, then experiment with the sliders.

### Linux note

PyQt6/OpenGL needs system GL libraries. On Debian/Ubuntu, if the window fails
to open with an OpenGL error, install:

```bash
sudo apt install libgl1 libglu1-mesa libxcb-cursor0
```

## How it works

Each step computes the wrap-aware pairwise displacement matrix once and reuses
it for both the steering forces and the live metrics:

- **Separation** steers away from close neighbours, weighted by inverse-square
  distance.
- **Alignment** steers toward the average heading of neighbours within the
  perception radius.
- **Cohesion** steers toward the local centre of mass of those neighbours.

Speed is clamped to a `[min, max]` band so boids always keep moving but never
outrun the simulation. The **cluster count** is estimated with a union-find over
the graph of boids that sit within half the perception radius of each other.

## Tuning

Defaults live in `boids/simulation.py` (`SimulationParams`) and
`boids/main_window.py` (`N_BOIDS`, `BOUNDS`, `FPS`). Lowering `N_BOIDS` or `FPS`
will help on slower machines.
