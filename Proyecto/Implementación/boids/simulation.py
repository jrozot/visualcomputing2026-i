"""
Classic Reynolds Boids flocking simulation, vectorised with NumPy.

The simulation lives inside a 3D bounded cube with wrap-around (periodic)
boundaries. Each boid steers according to three local rules:

    * Separation  -- steer away from crowding nearby flockmates
    * Alignment   -- steer towards the average heading of nearby flockmates
    * Cohesion    -- steer towards the average position of nearby flockmates

All neighbour interactions are computed with the *minimum image convention*
so that flockmates "see" each other across the wrap-around boundaries.

The per-step pairwise distance matrix is reused to derive the live metrics
(average speed, nearest-neighbour distance and cluster count) so we never
pay for that computation twice.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class SimulationParams:
    """Tunable flocking parameters, all live-editable from the UI."""

    max_speed: float = 1.2          # movement, in cube-units per step
    perception: float = 18.0        # neighbour search radius (cube units)
    separation: float = 1.6         # separation steering weight
    alignment: float = 1.0          # alignment steering weight
    cohesion: float = 1.0           # cohesion steering weight

    # Fixed tuning constants (not exposed as sliders) that keep the motion
    # smooth and stable.
    turn_rate: float = 0.12         # how aggressively boids change heading
    min_speed_ratio: float = 0.45   # floor on speed as a fraction of max


@dataclass
class SimulationMetrics:
    """Snapshot of derived quantities, refreshed every step."""

    count: int = 0
    avg_speed: float = 0.0
    avg_neighbor_dist: float = 0.0
    cluster_count: int = 0
    history_len: int = 0
    extras: dict = field(default_factory=dict)


class BoidsSimulation:
    """A vectorised flock of boids inside a periodic cube."""

    def __init__(self, n_boids: int = 250, bounds: float = 130.0) -> None:
        self.bounds = float(bounds)
        self.params = SimulationParams()
        self.metrics = SimulationMetrics()
        self._rng = np.random.default_rng()
        self.n = int(n_boids)
        self.reset(self.n)

    # ------------------------------------------------------------------ #
    # Setup / lifecycle
    # ------------------------------------------------------------------ #
    def reset(self, n_boids: int | None = None) -> None:
        """Re-seed the flock with random positions and headings."""
        if n_boids is not None:
            self.n = int(n_boids)

        b = self.bounds
        self.pos = self._rng.uniform(0.0, b, size=(self.n, 3)).astype(np.float64)

        vel = self._rng.uniform(-1.0, 1.0, size=(self.n, 3))
        vel = self._normalize(vel) * self.params.max_speed
        self.vel = vel.astype(np.float64)

        self._update_metrics(
            dist2=None, nearest=None, neighbour_count=None
        )

    # ------------------------------------------------------------------ #
    # Core update
    # ------------------------------------------------------------------ #
    def step(self) -> None:
        """Advance the flock by one time-step and refresh metrics."""
        p = self.params
        b = self.bounds

        # Pairwise displacement using the minimum image convention so that
        # neighbours are detected across the periodic boundaries.
        # diff[i, j] = (pos[j] - pos[i]) wrapped into [-b/2, b/2)
        diff = self.pos[np.newaxis, :, :] - self.pos[:, np.newaxis, :]
        diff -= b * np.round(diff / b)

        dist2 = np.einsum("ijk,ijk->ij", diff, diff)
        np.fill_diagonal(dist2, np.inf)  # a boid is not its own neighbour

        perception2 = p.perception * p.perception
        neighbours = dist2 < perception2          # boolean (N, N)
        mask = neighbours.astype(np.float64)
        counts = mask.sum(axis=1)
        safe_counts = np.maximum(counts, 1.0)[:, None]

        # --- Cohesion: steer toward the local centre of mass. Because diff
        # already points from i to its neighbours, the mean displacement is
        # the (wrap-aware) direction to the local centre.
        cohesion = np.einsum("ij,ijk->ik", mask, diff) / safe_counts

        # --- Alignment: match the average velocity of neighbours.
        alignment = (mask @ self.vel) / safe_counts

        # --- Separation: steer away from close neighbours, weighted by the
        # inverse square distance so the nearest ones dominate.
        inv = mask / np.where(neighbours, dist2, 1.0)
        separation = -np.einsum("ij,ijk->ik", inv, diff)

        # Combine the three normalised steering directions, weighted.
        acc = (
            self._normalize(separation) * p.separation
            + self._normalize(alignment) * p.alignment
            + self._normalize(cohesion) * p.cohesion
        )

        # Integrate heading. turn_rate controls how fast boids can change
        # direction, keeping motion smooth instead of jittery.
        self.vel += acc * p.turn_rate

        # Clamp the speed to [min_speed, max_speed] so boids always keep
        # moving but never outrun the simulation.
        speed = np.linalg.norm(self.vel, axis=1, keepdims=True)
        speed = np.maximum(speed, 1e-9)
        min_speed = p.max_speed * p.min_speed_ratio
        desired = np.clip(speed, min_speed, p.max_speed)
        self.vel *= desired / speed

        # Advance positions and wrap around the cube.
        self.pos = (self.pos + self.vel) % b

        # Nearest-neighbour distance reuses the distance matrix we already
        # computed this step.
        nearest = np.sqrt(np.min(dist2, axis=1))
        self._update_metrics(
            dist2=dist2, nearest=nearest, neighbour_count=counts
        )

    # ------------------------------------------------------------------ #
    # Metrics
    # ------------------------------------------------------------------ #
    def _update_metrics(self, dist2, nearest, neighbour_count) -> None:
        m = self.metrics
        m.count = self.n
        m.avg_speed = float(np.mean(np.linalg.norm(self.vel, axis=1)))

        if nearest is not None:
            finite = nearest[np.isfinite(nearest)]
            m.avg_neighbor_dist = float(np.mean(finite)) if finite.size else 0.0
        else:
            m.avg_neighbor_dist = 0.0

        if dist2 is not None:
            m.cluster_count = self._count_clusters(dist2)
        else:
            m.cluster_count = self.n

    def _count_clusters(self, dist2: np.ndarray) -> int:
        """Estimate the number of clusters via connected components.

        Two boids belong to the same cluster when they sit within half the
        perception radius of one another. Connectivity is resolved with a
        small union-find over the (sparse) edge set.
        """
        cluster_radius = max(self.params.perception * 0.5, 6.0)
        cr2 = cluster_radius * cluster_radius

        # Upper-triangular edges only, to avoid processing each pair twice.
        adj = np.triu(dist2 < cr2, k=1)
        edges = np.argwhere(adj)
        if edges.size == 0:
            return self.n

        parent = np.arange(self.n)

        def find(x: int) -> int:
            root = x
            while parent[root] != root:
                root = parent[root]
            while parent[x] != root:  # path compression
                parent[x], x = root, parent[x]
            return root

        components = self.n
        for i, j in edges:
            ri, rj = find(int(i)), find(int(j))
            if ri != rj:
                parent[ri] = rj
                components -= 1
        return int(components)

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def _normalize(v: np.ndarray, eps: float = 1e-9) -> np.ndarray:
        norm = np.linalg.norm(v, axis=1, keepdims=True)
        return v / np.maximum(norm, eps)
