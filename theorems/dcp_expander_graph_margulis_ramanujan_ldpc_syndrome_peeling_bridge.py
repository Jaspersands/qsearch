r"""
Subsystem 152: Expander Graph Ramanujan Spectral Gap & Tanner Vertex-Expansion Arithmetic Audit.

Audits the Alon-Boppana / Ramanujan spectral gap and Tanner's eigenvalue vertex-expansion
bound for d-regular graphs, and verifies why the naive one-sided Tanner bound alone does
NOT reach the > d/2 unique-neighbor majority-peeling threshold:
  1. For a d-regular graph G on N vertices with adjacency eigenvalues
     d = \lambda_1 >= |\lambda_2| >= ... >= |\lambda_N|, the Ramanujan bound states
     |\lambda_2| <= 2 \sqrt{d - 1}.
  2. By Tanner's vertex-expansion bound, any subset S of size |S| <= \alpha N has
     neighbor set N(S) satisfying:
       \frac{|N(S)|}{|S|} >= \frac{d^2}{\lambda_2^2 + (d^2 - \lambda_2^2) \alpha}.
  3. Because d^2 / \lambda_2^2 = d^2 / (4(d - 1)) < d / 2 for every degree d >= 3,
     Tanner's eigenvalue bound never reaches the > d / 2 majority-peeling threshold
     on any row (`guarantees_linear_time_peeling == False`). No peeling decoding
     guarantee is claimed from this spectral formula.
"""

from __future__ import annotations
import math
from typing import Any, Dict, List


def tanner_vertex_expansion_lower_bound(degree_d: int, lambda_2: float, subset_fraction_alpha: float) -> float:
    r"""
    Tanner's eigenvalue lower bound on the vertex expansion ratio |N(S)| / |S|
    for any subset S of size |S| <= \alpha N in a d-regular graph with second
    eigenvalue \lambda_2:
      |N(S)| / |S| >= d^2 / (\lambda_2^2 + (d^2 - \lambda_2^2) * \alpha).
    """
    d2 = float(degree_d * degree_d)
    l2_sq = float(lambda_2 * lambda_2)
    denom = l2_sq + (d2 - l2_sq) * subset_fraction_alpha
    return d2 / denom


def evaluate_ramanujan_expander_peeling_regime(
    degrees_list: List[int] = [3, 4, 5, 6, 8, 10],
    subset_fraction_alpha: float = 0.02,
) -> List[Dict[str, Any]]:
    """
    Evaluate the Ramanujan spectral bound 2*sqrt(d-1), unnormalized spectral gap
    d - 2*sqrt(d-1), Tanner vertex expansion lower bound |N(S)|/|S|, and verify
    that Tanner expansion alone does NOT exceed the > d/2 majority-peeling
    threshold for any degree d in degrees_list.
    """
    rows: List[Dict[str, Any]] = []
    for d in degrees_list:
        ram_l2 = 2.0 * math.sqrt(d - 1.0)
        spec_gap = float(d) - ram_l2
        tanner_exp = tanner_vertex_expansion_lower_bound(d, ram_l2, subset_fraction_alpha)
        half_d = 0.5 * float(d)
        rows.append({
            "degree_d": int(d),
            "ramanujan_lambda2_bound": float(ram_l2),
            "spectral_gap_d_minus_lambda2": float(spec_gap),
            "tanner_expansion_ratio": float(tanner_exp),
            "majority_peeling_threshold_d_over_2": float(half_d),
            "guarantees_linear_time_peeling": bool(tanner_exp > half_d),
        })
    return rows


def generate_dcp_expander_graph_margulis_ramanujan_ldpc_syndrome_peeling_certificate() -> Dict[str, Any]:
    """Generate the Subsystem 152 spectral and Tanner arithmetic audit certificate."""
    sweep = evaluate_ramanujan_expander_peeling_regime([3, 4, 5, 6, 8, 10], subset_fraction_alpha=0.02)

    tanner_gt_1_45_for_d_ge_5 = all(
        r["tanner_expansion_ratio"] > 1.45 for r in sweep if r["degree_d"] >= 5
    )
    naive_tanner_below_half_d = all(
        not r["guarantees_linear_time_peeling"] for r in sweep
    )
    spectral_gap_monotone = all(
        sweep[i]["spectral_gap_d_minus_lambda2"] < sweep[i + 1]["spectral_gap_d_minus_lambda2"]
        for i in range(len(sweep) - 1)
    )

    theorem_checks = {
        "spectral_gap_d_minus_2sqrt_d_minus_1_strictly_increasing": bool(spectral_gap_monotone),
        "tanner_vertex_expansion_exceeds_1_45_for_d_ge_5": bool(tanner_gt_1_45_for_d_ge_5),
        "tanner_expansion_monotone_increasing_with_degree_d": bool(
            all(sweep[i]["tanner_expansion_ratio"] < sweep[i + 1]["tanner_expansion_ratio"] for i in range(len(sweep) - 1))
        ),
        "d10_ramanujan_lambda2_equals_6_exact": bool(
            abs(sweep[-1]["ramanujan_lambda2_bound"] - 6.0) < 1e-12
        ),
        "naive_tanner_bound_strictly_below_half_degree_peeling_threshold": bool(naive_tanner_below_half_d),
    }

    return {
        "subsystem_id": "dcp_expander_graph_margulis_ramanujan_ldpc_syndrome_peeling_bridge",
        "subsystem_number": 152,
        "domain": "expander_graphs_ramanujan_spectral_gap_tanner_arithmetic_audit",
        "ramanujan_degree_sweep": sweep,
        "peeling_decoding_threshold_certified": False,
        "theorem_checks": theorem_checks,
        "all_checks_passed": bool(all(theorem_checks.values())),
        "falsification_status": {
            "accepted_speedup_candidate": False,
            "new_active_negative_result_created": False,
            "novelty_claim": False,
        },
    }
