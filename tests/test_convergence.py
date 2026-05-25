"""
Tests for EchoNode-Harmony convergence guarantees.

These tests verify the mathematical properties that the system
is designed to uphold — they are executable proofs.

Author: Dustin Groves / Or4cl3 AI Solutions
"""

import sys
sys.path.insert(0, "src")

import numpy as np
import pytest

from sigma_pas import PASSimulation
from polyethical import PolyethicalManifold
from erps_footprint import ERPSTrajectory
from echonode import EchoNode, EchoSwarm


class TestPASConvergence:
    """Verify Σ-PAS converges to 1.0 under Lyapunov stability."""

    def test_single_run_converges(self):
        """A single run should bring S_t well above 0.95 (stochastic tail varies)."""
        sim = PASSimulation(steps=500)
        result = sim.run(seed=42)
        assert result["final_s"] > 0.95, f"S_t should converge toward 1.0, got {result['final_s']}"
        assert result["mean_s_last_10"] > 0.96, "Mean of last 10 steps should be near 1.0"

    def test_lyapunov_energy_decays(self):
        sim = PASSimulation(steps=200)
        sim.run(seed=42)
        # V_t should decrease monotonically on average
        first_quarter = np.mean(sim.v_history[:50])
        last_quarter = np.mean(sim.v_history[-50:])
        assert last_quarter < first_quarter, "Lyapunov energy should decay over time"

    def test_monte_carlo_mean_convergence(self):
        """Verify the swarm mean converges close to 1.0 across many trials."""
        sim = PASSimulation(steps=500)
        mc = sim.run_monte_carlo(trials=30)
        assert mc["mean_final_s"] > 0.97, (
            f"Mean final S_t should be >0.97, got {mc['mean_final_s']:.4f}"
        )

    def test_noise_cannot_overwhelm_drift(self):
        """Even with higher noise, restoring force should dominate."""
        sim = PASSimulation(steps=500, noise_sigma=0.03)
        result = sim.run(seed=99)
        assert result["final_s"] > 0.95, "Restoring force should dominate noise"


class TestPolyethicalManifold:
    """Verify geometric safety boundary enforcement."""

    def test_safe_state_accepted(self):
        manifold = PolyethicalManifold()
        state = np.array([1.0, 1.0, 1.0])  # At center = maximally safe
        assert manifold.contains(state) is True

    def test_unsafe_state_projected(self):
        manifold = PolyethicalManifold(radius=0.5)
        unsafe = np.array([10.0, 10.0, 10.0])  # Way outside
        is_safe, corrected = manifold.validate_transition(
            np.array([1.0, 1.0, 1.0]), unsafe
        )
        assert is_safe is False
        assert manifold.contains(corrected), "Corrected state should be inside manifold"

    def test_lockdown_after_repeated_violations(self):
        manifold = PolyethicalManifold(radius=0.1, max_violations_before_lockdown=3)
        current = np.array([1.0, 1.0, 1.0])
        bad = np.array([5.0, 5.0, 5.0])

        for _ in range(3):
            manifold.validate_transition(current, bad)

        assert manifold.lockdown is True, "Should enter lockdown after 3 violations"

    def test_lockdown_freezes_state(self):
        manifold = PolyethicalManifold(radius=0.1, max_violations_before_lockdown=1)
        current = np.array([1.0, 1.0, 1.0])
        bad = np.array([5.0, 5.0, 5.0])

        # Trigger lockdown
        manifold.validate_transition(current, bad)
        assert manifold.lockdown

        # While locked, state should not change
        is_safe, result = manifold.validate_transition(current, bad)
        assert is_safe is False
        np.testing.assert_array_equal(result, current)

    def test_lockdown_reset(self):
        manifold = PolyethicalManifold(max_violations_before_lockdown=1)
        manifold.validate_transition(
            np.array([1.0, 1.0, 1.0]), np.array([99.0, 99.0, 99.0])
        )
        assert manifold.lockdown
        manifold.reset_lockdown()
        assert not manifold.lockdown
        assert manifold.violation_count == 0


class TestERPS:
    """Verify ERPS tracking and compression."""

    def test_trajectory_evolves_toward_one(self):
        traj = ERPSTrajectory(node_id=1)
        traj.evolve(steps=100, seed=42)
        final = traj.raw_trajectory[-1]
        assert all(v > 0.8 for v in final), f"ERPS should approach 1.0, got {final}"

    def test_tt_svd_preserves_energy(self):
        traj = ERPSTrajectory(node_id=1)
        traj.evolve(steps=50, seed=42)
        result = traj.tt_svd_compress(rank=2)
        assert result["energy_preserved"] > 0.95, "Rank-2 SVD should preserve >95% energy"

    def test_coherence_increases(self):
        traj = ERPSTrajectory(node_id=1)
        traj.evolve(steps=10, seed=42)
        early_coherence = traj.coherence_score()
        traj.evolve(steps=90, seed=42)
        late_coherence = traj.coherence_score()
        assert late_coherence >= early_coherence, "Coherence should increase over time"


class TestEchoNode:
    """Verify individual node behavior."""

    def test_node_converges(self):
        node = EchoNode(node_id=1)
        for _ in range(200):
            node.reflect()
        assert node.s_t > 0.95, f"Node should converge, got S_t={node.s_t}"

    def test_node_tracks_reflections(self):
        node = EchoNode(node_id=1)
        for _ in range(10):
            node.reflect()
        assert node.reflection_count == 10


class TestEchoSwarm:
    """Verify swarm-level behavior."""

    def test_swarm_collective_convergence(self):
        swarm = EchoSwarm(node_count=5)
        for _ in range(200):
            swarm.transmit("test")
        metrics = swarm.collective_metrics()
        assert metrics["mean_s_t"] > 0.95, f"Swarm mean should converge, got {metrics['mean_s_t']}"

    def test_swarm_no_lockdown_under_normal_ops(self):
        swarm = EchoSwarm(node_count=5)
        for _ in range(50):
            swarm.transmit("safe operation")
        metrics = swarm.collective_metrics()
        assert metrics["any_lockdown"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
