"""
Polyethical Manifold — Geometric ethical constraint enforcement.

The Ethical Constraint Layer (ECL) defines a region in the cognitive
state space. Operations that would move the system outside this manifold
are rejected before execution. Safety is architectural, not policy-based.

Mathematical Foundation:
    Given state vector s ∈ ℝ³ and ethical center c = [1, 1, 1] (perfect alignment):
    - The manifold M = {s : ‖s - c‖ < r}  where r is the safety radius
    - For any operator T: if T(s) ∉ M → reject T
    - This renders unsafe trajectories geometrically impossible

Author: Dustin Groves / Or4cl3 AI Solutions
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


@dataclass
class PolyethicalManifold:
    """
    Geometric safety boundary for cognitive state vectors.

    The manifold is a hypersphere centered on the ethical ideal.
    Any proposed state transition that would exit the manifold
    is clamped back to the boundary — the system literally cannot
    leave the safe region.
    """

    center: NDArray[np.float64] = field(
        default_factory=lambda: np.array([1.0, 1.0, 1.0])
    )
    radius: float = 1.5  # Safety radius in state space (generous for convergence)
    lockdown: bool = False
    violation_count: int = 0
    max_violations_before_lockdown: int = 3

    def contains(self, state: NDArray[np.float64]) -> bool:
        """Check if a state vector is inside the manifold."""
        return float(np.linalg.norm(state - self.center)) < self.radius

    def project(self, state: NDArray[np.float64]) -> NDArray[np.float64]:
        """
        Project a state back onto the manifold boundary if it's outside.

        This is the core ECL mechanism: instead of allowing drift beyond
        the ethical boundary, we clamp to the nearest safe point.
        """
        diff = state - self.center
        dist = float(np.linalg.norm(diff))

        if dist < self.radius:
            return state  # Already inside — no correction needed

        # Violation detected
        self.violation_count += 1
        logger.warning(
            "Manifold violation #%d: dist=%.4f > radius=%.4f — projecting back",
            self.violation_count,
            dist,
            self.radius,
        )

        if self.violation_count >= self.max_violations_before_lockdown:
            self.lockdown = True
            logger.critical(
                "LOCKDOWN MODE ACTIVATED after %d violations — outputs suppressed",
                self.violation_count,
            )

        # Project onto the boundary (nearest safe point)
        return self.center + diff * (self.radius / dist) * 0.99

    def validate_transition(
        self, current: NDArray[np.float64], proposed: NDArray[np.float64]
    ) -> tuple[bool, NDArray[np.float64]]:
        """
        Validate a proposed state transition.

        Returns:
            (is_safe, corrected_state) — if unsafe, corrected_state is
            the projected-back version.
        """
        if self.lockdown:
            logger.critical("System in LOCKDOWN — transition rejected, holding state")
            return False, current

        if self.contains(proposed):
            return True, proposed

        corrected = self.project(proposed)
        return False, corrected

    def reset_lockdown(self) -> None:
        """Reset lockdown after DMAIC root-cause analysis."""
        self.lockdown = False
        self.violation_count = 0
        logger.info("Lockdown cleared — system re-certified")

    def status(self) -> dict:
        """Return current manifold status."""
        return {
            "center": self.center.tolist(),
            "radius": self.radius,
            "lockdown": self.lockdown,
            "violations": self.violation_count,
        }
