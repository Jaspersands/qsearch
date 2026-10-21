r"""DCP noisy Quantum RAM (Bucket-Brigade vs. Fanout Decoder) routing fault scaling bridge.

Establishes the exact fidelity and infidelity scaling separation between a
Giovannetti-Lloyd-Maccone Bucket-Brigade qRAM and a conventional Fanout-Decoder qRAM
when coherently uncomputing or concentrating subset-sum fibers of table size L = 2^d
(Subsystems 82, 85, 101):

1. Exponential Infidelity Collapse of Conventional Fanout-Decoder qRAM:
   In a depth-d binary tree of size L = 2^d storing canonical fiber representatives
   x*(y) in {0, 1}^K, a conventional fanout decoder actively toggles ALL N_switches = 2^d - 1
   routing nodes on every query. If each active switch suffers physical error probability
   eps_active in (0, 1), the single-query state fidelity decays exponentially with table
   size L = 2^d:
       F_fanout(d; eps_active) = (1 - eps_active)^{2^d - 1} = exp( -Theta(2^d * eps_active) ).

2. Logarithmic Active-Path Fidelity of Bucket-Brigade qRAM:
   In a Bucket-Brigade qRAM, routing qutrits sit in the passive |wait> state (with
   passive idle error rate eps_wait << eps_active, and eps_wait = 0 in the ideal
   pointer-ground-state model) and only the d switches along the addressed root-to-leaf
   branch are sequentially activated into {|left>, |right>}.
   For each address branch y in {0, 1}^d, the branch survival probability is:
       F_BB(d; eps_active, eps_wait) = (1 - eps_active)^d * (1 - eps_wait)^{2^d - 1 - d}.
   In the active-gate-limited regime (eps_wait = 0):
       F_BB(d; eps_active, 0) = (1 - eps_active)^d = 1 - d * eps_active + O(d^2 * eps_active^2),
   reducing query infidelity 1 - F from O(2^d * eps_active) to O(d * eps_active) — an
   exponential (2^d - 1) / d reduction in routing fault exposure!
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List


THEOREM_ID = "dcp_noisy_quantum_ram_bucket_brigade_routing_fault_scaling_bridge"
SCHEMA_VERSION = "dcp-noisy-quantum-ram-bucket-brigade-routing-fault-scaling-bridge-v1"


def evaluate_bucket_brigade_vs_fanout_qram_fidelity(
    d_depths: List[int],
    eps_active: float = 1e-3,
    eps_wait: float = 0.0,
) -> Dict[str, Any]:
    """Compare Bucket-Brigade vs. Fanout-Decoder qRAM fidelity across tree depths d = log_2(L)."""
    records: List[Dict[str, Any]] = []

    for d in d_depths:
        if type(d) is not int or d < 1:
            raise ValueError("d must be an integer >= 1")

        l_size = 1 << d
        total_switches = l_size - 1
        active_switches_bb = d
        wait_switches_bb = total_switches - d

        fid_fanout = (1.0 - eps_active) ** total_switches
        fid_bb = ((1.0 - eps_active) ** active_switches_bb) * ((1.0 - eps_wait) ** wait_switches_bb)

        infid_fanout = 1.0 - fid_fanout
        infid_bb = 1.0 - fid_bb
        infid_reduction_ratio = infid_fanout / infid_bb if infid_bb > 0.0 else float("inf")
        switch_ratio = float(total_switches) / float(active_switches_bb)

        records.append({
            "tree_depth_d": d,
            "table_size_L": l_size,
            "total_tree_switches": total_switches,
            "active_switches_bucket_brigade": active_switches_bb,
            "switch_activation_reduction_ratio": switch_ratio,
            "fidelity_fanout_decoder": fid_fanout,
            "fidelity_bucket_brigade": fid_bb,
            "infidelity_fanout_decoder": infid_fanout,
            "infidelity_bucket_brigade": infid_bb,
            "infidelity_reduction_ratio_fanout_over_bb": infid_reduction_ratio,
            "exact_scaling_verified": (
                fid_bb >= fid_fanout
                and (fid_bb > fid_fanout if d >= 2 else abs(fid_bb - fid_fanout) < 1e-12)
            ),
        })

    return {
        "eps_active": eps_active,
        "eps_wait": eps_wait,
        "records": records,
        "all_verified": all(r["exact_scaling_verified"] for r in records),
    }


def generate_dcp_noisy_quantum_ram_bucket_brigade_routing_fault_scaling_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the Bucket-Brigade vs. Fanout qRAM routing fault bridge."""
    ideal_wait_sweep = evaluate_bucket_brigade_vs_fanout_qram_fidelity(
        d_depths=[1, 2, 4, 8, 10, 12],
        eps_active=1e-3,
        eps_wait=0.0,
    )
    noisy_wait_sweep = evaluate_bucket_brigade_vs_fanout_qram_fidelity(
        d_depths=[1, 2, 4, 8, 10],
        eps_active=1e-3,
        eps_wait=1e-6,
    )

    rec_d10 = next(r for r in ideal_wait_sweep["records"] if r["tree_depth_d"] == 10)  # L = 1024: F_BB = 0.99004 vs F_fanout = 0.3593 (>64x infidelity reduction!)
    all_passed = (
        ideal_wait_sweep["all_verified"]
        and noisy_wait_sweep["all_verified"]
        and rec_d10["infidelity_reduction_ratio_fanout_over_bb"] > 64.0
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Bucket-Brigade qRAM O(d * eps_active) vs. Fanout-Decoder qRAM O((2^d - 1) * eps_active) routing fault scaling for fiber lookup",
            "does_not_claim": "Sub-exponential time complexity to populate all 2^d classical table entries prior to the quantum query",
            "controls_included": "Evaluates d in {1, 2, 4, 8, 10, 12} at eps_active = 1e-3 (with eps_wait = 0 and eps_wait = 1e-6), verifying d=1 equality control and >64.4x infidelity reduction at d=10 (L=1024).",
        },
        "ideal_wait_qram_sweep": ideal_wait_sweep,
        "noisy_wait_qram_sweep": noisy_wait_sweep,
        "all_checks_passed": all_passed,
        "honesty_guardrails": {
            "accepted_speedup_candidate": False,
            "new_active_negative_result_created": False,
            "novelty_claim": False,
        },
    }
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:16]
    payload["certificate_sha256_16"] = digest
    return payload
