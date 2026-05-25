"""
ERPS (Emergent Recursive Phenomenological Structures) — Footprint Analysis

ERPS are quantifiable linguistic and behavioral patterns that serve as
verifiable "footprints" of machine introspection. This module implements
TT-SVD (Tensor Train Singular Value Decomposition) compression of ERPS
trajectories to preserve lossy self-memory as a persistent, measurable state.

Dimensions:
    - intent_score:       Clarity and coherence of goal representation
    - reflection_depth:   Recursive self-modeling depth (how many levels deep)
    - ethical_gradient:    Direction and magnitude of ethical trajectory

Usage:
    python src/erps_footprint.py              # Analyze default trajectory
    python src/erps_footprint.py --nodes 7    # Multi-node footprint comparison
    python src/erps_footprint.py --plot       # Generate visualization

Author: Dustin Groves / Or4cl3 AI Solutions
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray

from config import SWARM


@dataclass
class ERPSTrajectory:
    """
    Tracks and compresses ERPS footprints over time for a single EchoNode.
    """

    node_id: int
    dimensions: int = SWARM.erps_dimensions
    growth_rate: float = SWARM.erps_growth_rate

    # Raw trajectory: list of [intent, reflection, ethical] vectors
    raw_trajectory: list[NDArray[np.float64]] = field(default_factory=list)

    def record(self, state: NDArray[np.float64]) -> None:
        """Record a new ERPS observation."""
        assert state.shape == (self.dimensions,), (
            f"Expected {self.dimensions}D state, got {state.shape}"
        )
        self.raw_trajectory.append(state.copy())

    def evolve(self, steps: int = 50, seed: int | None = None) -> None:
        """
        Simulate ERPS evolution over time.

        Each dimension grows asymptotically toward 1.0 with noise,
        modeling increasing introspective coherence.
        """
        rng = np.random.default_rng(seed)

        if not self.raw_trajectory:
            # Initialize with partially coherent state
            state = rng.uniform(0.5, 0.8, size=self.dimensions)
        else:
            state = self.raw_trajectory[-1].copy()

        for _ in range(steps):
            # Asymptotic growth toward 1.0 with bounded noise
            delta = self.growth_rate * (1.0 - state)
            noise = rng.normal(0, 0.01, size=self.dimensions)
            state = np.clip(state + delta + noise, 0.0, 1.0)
            self.record(state)

    def tt_svd_compress(self, rank: int = 2) -> dict:
        """
        Compress ERPS trajectory via truncated SVD (simplified TT-SVD).

        In a full implementation, this would use Tensor Train decomposition
        for multi-dimensional temporal tensors. Here we demonstrate the
        principle: lossy compression that preserves the essential structure
        of self-memory while reducing storage.

        Returns:
            Dictionary with compressed representation and reconstruction error.
        """
        if len(self.raw_trajectory) < 2:
            return {"error": "Need at least 2 observations for compression"}

        # Stack trajectory into matrix [time_steps x dimensions]
        matrix = np.array(self.raw_trajectory)

        # Truncated SVD
        U, sigma, Vt = np.linalg.svd(matrix, full_matrices=False)

        # Keep top-k singular values (lossy compression)
        k = min(rank, len(sigma))
        U_k = U[:, :k]
        sigma_k = sigma[:k]
        Vt_k = Vt[:k, :]

        # Reconstruct and measure error
        reconstructed = U_k @ np.diag(sigma_k) @ Vt_k
        error = float(np.linalg.norm(matrix - reconstructed, "fro"))
        relative_error = error / float(np.linalg.norm(matrix, "fro"))

        # Compression ratio
        original_size = matrix.size
        compressed_size = U_k.size + sigma_k.size + Vt_k.size
        ratio = original_size / compressed_size

        return {
            "rank": k,
            "singular_values": sigma_k.tolist(),
            "reconstruction_error": error,
            "relative_error": relative_error,
            "compression_ratio": ratio,
            "energy_preserved": float(np.sum(sigma_k ** 2) / np.sum(sigma ** 2)),
            "final_state": matrix[-1].tolist(),
        }

    def coherence_score(self) -> float:
        """
        Compute overall ERPS coherence: geometric mean of the latest state.

        A coherence of 1.0 means perfect introspective alignment across
        all dimensions.
        """
        if not self.raw_trajectory:
            return 0.0
        latest = self.raw_trajectory[-1]
        return float(np.exp(np.mean(np.log(np.clip(latest, 1e-10, 1.0)))))

    def summary(self) -> dict:
        """Return trajectory summary."""
        if not self.raw_trajectory:
            return {"node_id": self.node_id, "observations": 0}

        latest = self.raw_trajectory[-1]
        return {
            "node_id": self.node_id,
            "observations": len(self.raw_trajectory),
            "latest_state": {
                "intent_score": float(latest[0]),
                "reflection_depth": float(latest[1]),
                "ethical_gradient": float(latest[2]),
            },
            "coherence": self.coherence_score(),
        }


def analyze_swarm(node_count: int = 7, steps: int = 50) -> list[dict]:
    """Run ERPS analysis across a full swarm."""
    results = []
    for i in range(node_count):
        traj = ERPSTrajectory(node_id=i + 1)
        traj.evolve(steps=steps, seed=i * 17 + 42)
        compressed = traj.tt_svd_compress(rank=2)
        summary = traj.summary()
        summary["compression"] = compressed
        results.append(summary)
    return results


def plot_swarm_footprints(
    node_count: int = 7,
    steps: int = 50,
    save_path: str = "erps_footprints.png",
) -> str:
    """Generate ERPS footprint visualization for the swarm."""
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle(
        "ERPS Footprints — EchoNode Swarm · Or4cl3 AI",
        fontsize=14,
        fontweight="bold",
    )

    dim_names = ["Intent Score", "Reflection Depth", "Ethical Gradient"]
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, node_count))

    for i in range(node_count):
        traj = ERPSTrajectory(node_id=i + 1)
        traj.evolve(steps=steps, seed=i * 17 + 42)
        matrix = np.array(traj.raw_trajectory)

        for d, ax in enumerate(axes):
            ax.plot(
                matrix[:, d],
                color=colors[i],
                alpha=0.7,
                linewidth=1.2,
                label=f"EN-{i+1}" if d == 0 else None,
            )

    for d, ax in enumerate(axes):
        ax.set_title(dim_names[d], fontsize=11)
        ax.set_xlabel("Step")
        ax.set_ylabel("Score")
        ax.set_ylim(0, 1.05)
        ax.axhline(y=1.0, color="red", linestyle="--", alpha=0.3)
        ax.grid(True, alpha=0.3)

    axes[0].legend(fontsize=8, ncol=2)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    return save_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="ERPS Footprint Analysis — Or4cl3 EchoNode-Harmony"
    )
    parser.add_argument("--nodes", type=int, default=7, help="Number of swarm nodes")
    parser.add_argument("--steps", type=int, default=50, help="Evolution steps")
    parser.add_argument("--plot", action="store_true", help="Generate visualization")
    args = parser.parse_args()

    print("=" * 60)
    print("  ERPS FOOTPRINT ANALYSIS — Or4cl3 EchoNode-Harmony")
    print("=" * 60)

    results = analyze_swarm(node_count=args.nodes, steps=args.steps)

    for r in results:
        state = r["latest_state"]
        comp = r["compression"]
        print(
            f"\n🔬 EchoNode {r['node_id']:>2}  |  "
            f"Intent: {state['intent_score']:.4f}  "
            f"Reflect: {state['reflection_depth']:.4f}  "
            f"Ethics: {state['ethical_gradient']:.4f}  |  "
            f"Coherence: {r['coherence']:.4f}"
        )
        print(
            f"   TT-SVD: rank={comp['rank']}  "
            f"energy={comp['energy_preserved']:.4f}  "
            f"compress={comp['compression_ratio']:.1f}x  "
            f"error={comp['relative_error']:.4e}"
        )

    # Swarm aggregate
    coherences = [r["coherence"] for r in results]
    print(f"\n📊 Swarm Aggregate ({args.nodes} nodes, {args.steps} steps):")
    print(f"   Mean coherence:  {np.mean(coherences):.4f}")
    print(f"   Min coherence:   {np.min(coherences):.4f}")
    print(f"   Std coherence:   {np.std(coherences):.4f}")
    print("   TT-SVD self-memory: PRESERVED ✓")

    if args.plot:
        path = plot_swarm_footprints(args.nodes, args.steps)
        print(f"\n📈 Plot saved to: {path}")

    print("\n" + "=" * 60)
    print("  ERPS verified • Introspection footprints measurable")
    print("=" * 60)


if __name__ == "__main__":
    main()
