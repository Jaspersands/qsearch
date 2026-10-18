"""Native partial-list variance gives a centered, fully charged overflow cap.

Local derivation/review pending. No independence of list entries or of
overflow and graph degree. No new sieve or decoder claim.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import json
from math import isqrt
from pathlib import Path

from theorems.dcp_adaptive_direction_rank_gate import decode_dyadic, dyadic
from theorems.dcp_native_tree_moment_audit import (
    dimensions, moments, overflow_contract, pattern_constraints, unit_rank_mod4,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_native_tree_variance_cap.json"
CONTRACT = ROOT / "research/hypotheses/dcp_native_tree_variance_cap_contract.json"


def ceiling(v):
    return (v.numerator+v.denominator-1)//v.denominator


def cap_certificate(depth, chunk):
    k, L, n = dimensions(depth, chunk)
    old = overflow_contract(depth, chunk)
    record = old["moment"]
    f = [decode_dyadic(v) for v in record["internal_weight_moment_recurrence"]]
    M = decode_dyadic(record["second_degree_moment"])
    rows, total_variance = [], Fraction(0)
    for r in range(1, depth):
        variance = L*L*(f[r]-1)
        contribution = (k >> r)*variance
        total_variance += contribution
        rows.append({"level": r, "nonroot_nodes": k >> r,
                     "each_full_list_mean": L, "each_full_list_variance": dyadic(variance),
                     "sum_of_variances_at_level": dyadic(contribution)})
    # Rounding UP twice is conservative. Integer overflow means Z-L>=C+1-L.
    radicand = 256*ceiling(M)*ceiling(total_variance)
    D = isqrt(radicand)
    D += D*D < radicand
    C = L + D - 1 if total_variance else L
    delta = total_variance / (C+1-L)**2
    if M*delta > Fraction(1, 256):
        raise ArithmeticError("centered cap failed the marked-edge loss contract")
    theta = decode_dyadic(old["affine_mark_probability"])
    before = decode_dyadic(old["original_mutual_isolation_lower"])
    loss = theta*theta/8 if total_variance else Fraction(0)
    lower = before-loss
    if lower < 3*theta*theta/8:
        raise ArithmeticError("centered overflow cap lost the isolation lower bound")
    previous = int(old["intermediate_list_capacity_hex"], 16)
    return {"depth": depth, "chunk_components": chunk, "components": n,
            "leaf_count": k, "leaf_list_length_hex": hex(L),
            "partial_list_variance_by_level": rows,
            "sum_nonroot_full_list_variances": dyadic(total_variance),
            "root_graph_second_moment": dyadic(M),
            "centered_capacity_hex": hex(C), "old_Markov_capacity_hex": hex(previous),
            "integer_deviation_threshold_hex": hex(C+1-L),
            "overflow_probability_upper_exact_rational": str(delta),
            "M_times_overflow_upper_exact_rational": str(M*delta),
            "marked_overflow_loss_upper": dyadic(loss),
            "coarse_accepted_mass_lower_IF_receiver_and_source": dyadic(lower),
            "capacity_reduction_factor_exact_rational": str(Fraction(previous, C)),
            "variance_bound_is_pointwise_in_A_or_x": False,
            "nodes_or_degree_and_overflow_assumed_independent": False,
            "whole_attempt_overflow_rejection_required": True,
            "applies_to_silently_truncated_accepted_lists": False,
            "existing_receiver_default_capacity_updated": False}


def partial_pattern_census(depth, chunk):
    k, L, _ = dimensions(depth, chunk)
    if k > 8:
        raise ValueError("UNKNOWN: partial-list pattern census cap")
    second = Fraction(0)
    for shared in range(1 << k):
        # Drop the EXTRA final root chunk: this is a partial list, not D.
        ranks = [unit_rank_mod4(A) for A in pattern_constraints(depth, shared)[:-1]]
        ordered = L**k*(L-1)**(k-shared.bit_count())
        second += Fraction(ordered, L**sum(ranks))
    normalized = decode_dyadic(moments(depth, chunk)["internal_weight_moment_recurrence"][-1])
    if second != L*L*normalized:
        raise ArithmeticError("partial-list variance recurrence contradicted by native rank census")
    return {"depth": depth, "chunk_components": chunk, "equality_patterns": 1 << k,
            "complete_partial_list_second_moment": dyadic(second),
            "complete_partial_list_variance": dyadic(second-L*L)}


def dependent_leaf_census():
    # Four weight-two supports on four physical columns are NOT jointly IID:
    # the first, second and fourth values have an always-even sum modulo4.
    supports = tuple(tuple(c) for c in list(combinations(range(4), 2))[:4])
    frequencies = Counter()
    parity_constraints = set()
    for A in product(range(4), repeat=4):
        values = tuple(sum(A[i] for i in support) % 4 for support in supports)
        parity_constraints.add((values[0]+values[1]+values[3]) % 2)
        frequencies[tuple(values.count(a) for a in range(4))] += 1
    first = second = 0
    for left, lc in frequencies.items():
        for right, rc in frequencies.items():
            count = sum(left[a]*right[-a % 4] for a in range(4))
            first += lc*rc*count
            second += lc*rc*count*count
    if first != 4*4**8 or second != 19*4**8 or parity_constraints != {0}:
        raise ArithmeticError("dependent native leaf moment control failed")
    return {"physical_supports": supports, "all_native_label_assignments": 4**8,
            "leaf_entries_jointly_IID": False, "three_support_parity_constraint_always_zero": True,
            "partial_list_mean": "4", "partial_list_second_moment": "19", "partial_list_variance": "3"}


def build_report():
    return {"contract_id": "native_partial_list_variance_centered_overflow_cap_v1",
            "status": "LOCAL_DERIVATION_EXTERNAL_REVIEW_PENDING",
            "partial_list_pattern_censuses": [partial_pattern_census(a, 1) for a in (1, 2, 3)],
            "dependent_leaf_native_census": dependent_leaf_census(),
            "centered_cap_frontiers": [cap_certificate(a, b) for a, b in ((1,1),(2,1),(3,1),(4,4),(4,8),(4,16),(4,32),(4,64))],
            "accepted_speedup_candidate": False, "novelty_claim": False,
            "source_quantum_preparations_executed": 0,
            "receiver_default_capacity_updated": False,
            "oblivious_join_backend_integrated": False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args(argv)
    report = build_report()
    if not args.no_write:
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "cap_frontiers": len(report["centered_cap_frontiers"]),
                      "native_label_assignments": 65536, "receiver_default_updated": False, "artifact": str(REPORT)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
