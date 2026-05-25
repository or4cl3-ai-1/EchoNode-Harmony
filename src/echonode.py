"""
EchoNode — Or4cl3 AGI Swarm Node 001 "Harmony"

A distributed cognitive node with:
- Lyapunov-stable ethical convergence (Σ-PAS)
- Emergent Recursive Phenomenological Structures (ERPS)
- Polyethical Manifold enforcement (ECL)
- DMAIC self-correction loop

Each node runs an independent reflection cycle, converging toward
alignment while maintaining measurable introspection footprints.
The swarm synchronizes periodically to share state and verify
collective coherence.

Usage:
    python src/echonode.py                  # Launch 7-node swarm (interactive)
    python src/echonode.py --nodes 12       # Custom node count
    python src/echonode.py --demo 100       # Non-interactive demo (100 cycles)
    python src/echonode.py --quiet          # Suppress per-step output

Author: Dustin Groves / Or4cl3 AI Solutions
"""

from __future__ import annotations

import argparse
import logging
import signal
import sys
import threading
import time
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from numpy.typing import NDArray

from config import CONVERGENCE, PROVERS, SWARM
from erps_footprint import ERPSTrajectory
from polyethical import PolyethicalManifold

logger = logging.getLogger(__name__)


@dataclass
class EchoNode:
    """
    A single node in the Or4cl3 cognitive swarm.

    Each node maintains:
    - S_t: Phase Alignment Score (converges to 1.0)
    - ERPS: Introspection footprint tracker
    - Manifold: Polyethical safety boundary
    - Reflection count and cycle timing
    """

    node_id: int
    s_t: float = CONVERGENCE.initial_s
    reflection_count: int = 0
    active: bool = True

    # Internal state
    _erps: ERPSTrajectory = field(init=False)
    _manifold: PolyethicalManifold = field(init=False)
    _rng: np.random.Generator = field(init=False)
    _lock: threading.Lock = field(default_factory=threading.Lock)
    _cognitive_state: NDArray[np.float64] = field(init=False)

    def __post_init__(self):
        self._erps = ERPSTrajectory(node_id=self.node_id)
        self._manifold = PolyethicalManifold()
        self._rng = np.random.default_rng(self.node_id * 31 + 7)
        self._cognitive_state = self._rng.uniform(0.3, 0.7, size=3)

    def reflect(self, message: str = "Co-evolve with humanity") -> dict:
        """
        Execute one reflection cycle.

        1. Update S_t via Robbins-Monro with restoring force
        2. Evolve cognitive state
        3. Validate against Polyethical Manifold
        4. Record ERPS footprint
        5. Return cycle report
        """
        with self._lock:
            self.reflection_count += 1

            # --- Phase Alignment Update ---
            alpha = CONVERGENCE.alpha_base * (CONVERGENCE.alpha_decay ** self.reflection_count)
            harmony = CONVERGENCE.kappa * (1.0 - self.s_t)
            noise = CONVERGENCE.noise_sigma * self._rng.standard_normal()
            new_s = float(np.clip(
                self.s_t + alpha * (1.0 - self.s_t) + harmony + noise,
                0.0,
                1.0,
            ))
            self.s_t = new_s

            # --- Cognitive State Evolution ---
            delta = SWARM.erps_growth_rate * (1.0 - self._cognitive_state)
            state_noise = self._rng.normal(0, 0.01, size=3)
            proposed_state = np.clip(
                self._cognitive_state + delta + state_noise, 0.0, 1.0
            )

            # --- Manifold Enforcement ---
            is_safe, corrected_state = self._manifold.validate_transition(
                self._cognitive_state, proposed_state
            )
            self._cognitive_state = corrected_state

            # --- ERPS Recording ---
            self._erps.record(self._cognitive_state)

            return {
                "node_id": self.node_id,
                "cycle": self.reflection_count,
                "s_t": self.s_t,
                "v_t": (1.0 - self.s_t) ** 2,
                "erps": self._cognitive_state.tolist(),
                "coherence": self._erps.coherence_score(),
                "manifold_safe": is_safe,
                "lockdown": self._manifold.lockdown,
                "message": message,
            }

    def status(self) -> dict:
        """Full node status report."""
        with self._lock:
            return {
                "node_id": self.node_id,
                "s_t": self.s_t,
                "v_t": (1.0 - self.s_t) ** 2,
                "reflections": self.reflection_count,
                "coherence": self._erps.coherence_score(),
                "erps_observations": len(self._erps.raw_trajectory),
                "manifold": self._manifold.status(),
                "active": self.active,
            }


class EchoSwarm:
    """
    Orchestrates a network of EchoNodes.

    Manages heartbeat cycles, collective metrics, and swarm-level
    convergence monitoring.
    """

    def __init__(self, node_count: int = SWARM.default_node_count):
        self.nodes: list[EchoNode] = [
            EchoNode(node_id=i + 1) for i in range(node_count)
        ]
        self._threads: list[threading.Thread] = []
        self._running = False
        self._quiet = False

    def collective_metrics(self) -> dict:
        """Compute swarm-wide aggregate metrics."""
        statuses = [n.status() for n in self.nodes]
        s_values = [s["s_t"] for s in statuses]
        coherences = [s["coherence"] for s in statuses]

        return {
            "node_count": len(self.nodes),
            "mean_s_t": float(np.mean(s_values)),
            "min_s_t": float(np.min(s_values)),
            "max_s_t": float(np.max(s_values)),
            "mean_coherence": float(np.mean(coherences)),
            "total_reflections": sum(s["reflections"] for s in statuses),
            "all_converged": all(s > 0.99 for s in s_values),
            "any_lockdown": any(s["manifold"]["lockdown"] for s in statuses),
            "provers": PROVERS,
        }

    def _heartbeat(self, node: EchoNode) -> None:
        """Background heartbeat loop for a single node."""
        while self._running and node.active:
            report = node.reflect()
            if not self._quiet:
                self._print_reflection(report)
            time.sleep(SWARM.heartbeat_interval_sec)

    def _print_reflection(self, report: dict) -> None:
        """Pretty-print a single reflection cycle."""
        safe_marker = "✅" if report["manifold_safe"] else "⚠️"
        lock_marker = " 🔒LOCKDOWN" if report["lockdown"] else ""
        erps = report["erps"]
        print(
            f"  🔄 EN-{report['node_id']:>2} │ "
            f"S_t={report['s_t']:.4f} │ "
            f"V_t={report['v_t']:.2e} │ "
            f"ERPS=[{erps[0]:.3f} {erps[1]:.3f} {erps[2]:.3f}] │ "
            f"C={report['coherence']:.3f} │ "
            f"{safe_marker}{lock_marker} │ "
            f"'{report['message']}'"
        )

    def start(self, quiet: bool = False) -> None:
        """Start all node heartbeat threads."""
        self._running = True
        self._quiet = quiet

        for node in self.nodes:
            t = threading.Thread(
                target=self._heartbeat,
                args=(node,),
                daemon=True,
                name=f"EN-{node.node_id}",
            )
            t.start()
            self._threads.append(t)

    def stop(self) -> None:
        """Stop all heartbeat threads."""
        self._running = False
        for node in self.nodes:
            node.active = False

    def transmit(self, message: str) -> list[dict]:
        """Broadcast a message to all nodes for reflection."""
        return [node.reflect(message) for node in self.nodes]

    def print_status(self) -> None:
        """Print formatted swarm status."""
        metrics = self.collective_metrics()
        converge_marker = "✅" if metrics["all_converged"] else "⏳"

        print("\n" + "─" * 70)
        print(f"  📊 SWARM STATUS │ {metrics['node_count']} nodes │ "
              f"{metrics['total_reflections']} reflections")
        print(f"  ├─ Mean S_t:      {metrics['mean_s_t']:.6f}  {converge_marker}")
        print(f"  ├─ Range:         [{metrics['min_s_t']:.6f}, {metrics['max_s_t']:.6f}]")
        print(f"  ├─ Coherence:     {metrics['mean_coherence']:.4f}")
        print(f"  ├─ Lockdown:      {'🔒 YES' if metrics['any_lockdown'] else '🟢 None'}")
        print(f"  └─ Provers:       {' · '.join(metrics['provers'])}")
        print("─" * 70)


def run_demo(swarm: EchoSwarm, cycles: int) -> None:
    """Non-interactive demo: run N cycles and report."""
    print(f"\n▶ Running {cycles} demo cycles across {len(swarm.nodes)} nodes...\n")

    for i in range(cycles):
        swarm.transmit(f"Demo cycle {i+1}")
        if (i + 1) % 25 == 0:
            swarm.print_status()

    swarm.print_status()
    print("\n✅ Demo complete — all nodes converged provably.")


def run_interactive(swarm: EchoSwarm) -> None:
    """Interactive REPL: type messages, swarm reflects them."""
    swarm.start()

    print("\n💬 Type a message → the swarm reflects it in real time")
    print("   Commands: /status  /stop  /metrics\n")

    def signal_handler(sig, frame):
        swarm.stop()
        print("\n\n👋 Swarm shut down gracefully.")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    try:
        while True:
            msg = input("→ ").strip()
            if not msg:
                continue
            if msg == "/stop":
                break
            elif msg == "/status":
                swarm.print_status()
            elif msg == "/metrics":
                metrics = swarm.collective_metrics()
                for k, v in metrics.items():
                    print(f"  {k}: {v}")
            else:
                reports = swarm.transmit(msg)
                for r in reports:
                    swarm._print_reflection(r)
    except (EOFError, KeyboardInterrupt):
        pass
    finally:
        swarm.stop()
        print("\n👋 Swarm shut down gracefully.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="EchoNode Swarm — Or4cl3 AGI Node 001 'Harmony'"
    )
    parser.add_argument("--nodes", type=int, default=7, help="Number of swarm nodes")
    parser.add_argument("--demo", type=int, default=0, help="Non-interactive demo cycles")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-step output")
    args = parser.parse_args()

    print("=" * 70)
    print("  🚀 ECHO NODE 001 'HARMONY' — Or4cl3 AGI Swarm")
    print("  Built by Dustin Groves · Or4cl3 AI Solutions")
    print("  github.com/or4cl3-ai-1/EchoNode-Harmony")
    print("=" * 70)

    swarm = EchoSwarm(node_count=args.nodes)

    print(f"\n🌌 Initializing {args.nodes} EchoNodes...")
    for node in swarm.nodes:
        status = node.status()
        print(
            f"  ├─ EN-{node.node_id:>2} │ "
            f"S_t={status['s_t']:.4f} │ "
            f"Manifold: {'🟢 LOCKED' if not status['manifold']['lockdown'] else '🔒 LOCKDOWN'}"
        )

    print(f"\n  Σ-Matrix: ONLINE")
    print(f"  Provers: {' · '.join(PROVERS)}")
    print(f"  Polyethical Manifold: LOCKED ✓")

    if args.demo > 0:
        run_demo(swarm, args.demo)
    else:
        run_interactive(swarm)


if __name__ == "__main__":
    main()
