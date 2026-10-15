"""Exact pre-complement single-direction descent law; local proof, review pending.

Full public labels may choose the direction. They must not choose it after
the complement-Z outcome. This is not a general DCP or quantum lower bound.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_adaptive_direction_rank_gate.json"
CONTRACT = ROOT / "research/hypotheses/dcp_adaptive_direction_rank_gate_contract.json"
SELECTION = "all-public-labels-before-complement-Z"
NOISE_MODEL = "pure-flat-native-phase-packet"


def integer(value, name, minimum=0, maximum=None):
    if type(value) is not int or value < minimum or (maximum is not None and value > maximum):
        raise ValueError(f"invalid {name}")
    return value


def binary_basis(vectors, width):
    """Canonical reduced GF(2) row basis, highest-coordinate pivots first."""
    integer(width, "binary width", 1, 16384)
    pivots = {}
    for value in vectors:
        integer(value, "binary row", 0, (1 << width) - 1)
        for p in sorted(pivots, reverse=True):
            if value >> p & 1:
                value ^= pivots[p]
        if value:
            p = value.bit_length() - 1
            for other in pivots:
                if pivots[other] >> p & 1:
                    pivots[other] ^= value
            pivots[p] = value
    return tuple(pivots[p] for p in sorted(pivots, reverse=True))


def binary_kernel(rows, width):
    basis = binary_basis(rows, width)
    pivots = {row.bit_length() - 1 for row in basis}
    return tuple((1 << f) | sum(((row >> f) & 1) << (row.bit_length() - 1)
                               for row in basis)
                 for f in range(width) if f not in pivots)


def binary_map(rows, x):
    return sum(((row & x).bit_count() & 1) << j for j, row in enumerate(rows))


def in_span(value, basis):
    for row in basis:
        if value >> (row.bit_length() - 1) & 1:
            value ^= row
    return value == 0


def dyadic(value):
    value = Fraction(value)
    d = value.denominator
    if d & (d - 1):
        raise ValueError("non-dyadic probability/bound")
    return {"numerator_hex": hex(value.numerator),
            "denominator_binary_exponent": d.bit_length() - 1}


def decode_dyadic(value):
    return Fraction(int(value["numerator_hex"], 16),
                    1 << value["denominator_binary_exponent"])


def connectivity_rank(rows, width, direction):
    integer(direction, "nonzero physical direction", 1, (1 << width) - 1)
    rows = tuple(rows)
    full = (1 << width) - 1
    return (len(binary_basis((b & direction for b in rows), width))
            + len(binary_basis((b & (full ^ direction) for b in rows), width))
            - len(binary_basis(rows, width)))


def posterior_law(labels, phase_bits, direction, origin=0, *,
                  selection_model=SELECTION, noise_model=NOISE_MODEL):
    """Fix ALL A first; only complement measurement supplies randomness.

    No assumption that the high labels remain uniform after choosing u(A).
    origin represents any measured parity syndrome's affine kernel coset.
    """
    integer(phase_bits, "phase bits", 3, 4096)
    if selection_model != SELECTION:
        raise ValueError("direction must be selected before complement-Z outcomes")
    if noise_model != NOISE_MODEL:
        raise ValueError("mixed/non-flat source requires a separate source law")
    labels = tuple(tuple(row) for row in labels)
    if not labels or not labels[0] or any(len(row) != len(labels[0]) for row in labels):
        raise ValueError("nonempty rectangular label matrix required")
    n, m, q = len(labels), len(labels[0]), 1 << phase_bits
    if max(n, m) > 4096 or n * m > 2000000:
        raise ValueError("UNKNOWN: matrix certificate work cap exceeded")
    for row in labels:
        for a in row:
            integer(a, "canonical public label", 0, q - 1)
    integer(origin, "physical origin", 0, (1 << m) - 1)
    integer(direction, "nonzero physical direction", 1, (1 << m) - 1)
    B = tuple(sum((a & 1) << i for i, a in enumerate(row)) for row in labels)
    if binary_map(B, direction):
        raise ValueError("physical direction must lie in ker(B)")
    kernel = binary_kernel(B, m)
    images = tuple(binary_map(tuple(b & direction for b in B), w) for w in kernel)
    image_basis = binary_basis(images, n)
    rank = len(image_basis)
    cut_rank = connectivity_rank(B, m, direction)
    if rank != cut_rank:
        raise ArithmeticError("kernel-image rank disagrees with cut-rank identity")
    # Difference of the ORIGINAL integer phase at x and x XOR u, divided by 2.
    offset = sum(((sum(a for i, a in enumerate(row) if direction >> i & 1) // 2
                    - (b & direction & origin).bit_count()) & 1) << j
                 for j, (row, b) in enumerate(zip(labels, B)))
    possible = in_span(offset, image_basis)
    dual = binary_kernel(image_basis, n)
    return {
        "phase_bits": phase_bits, "component_count": n, "original_registers": m,
        "selection_model": selection_model, "noise_model": noise_model,
        "public_labels_hex": [[hex(a) for a in row] for row in labels],
        "physical_direction_hex": hex(direction), "physical_origin_hex": hex(origin),
        "low_rows_hex": [hex(b) for b in B],
        "kernel_basis_hex": [hex(w) for w in kernel],
        "kernel_image_basis_hex": [hex(v) for v in image_basis],
        "affine_low_output_offset_hex": hex(offset),
        "dual_constraints": [{"mask_hex": hex(v), "target": (v & offset).bit_count() & 1}
                             for v in dual],
        "low_matrix_rank": m - len(kernel), "posterior_rank": rank,
        "matroid_connectivity_rank": cut_rank,
        "complement_outcome_bits": len(kernel) - 1,
        "uniform_pushforward_from_quotient_D_mod_u": True,
        "all_even_output_attainable": possible,
        "extra_descent_probability": dyadic(Fraction(int(possible), 1 << rank)),
        "success_means_shift_recovery": False,
        "mixed_noise_law_supplied": False,
    }


def rank_pair_exponent(n, side_size, a, b):
    return (n - a) * (side_size - a) + (n - b) * (3 * n - side_size - b)


def native_bound(n, w=None, r=None):
    """Uniform over ALL full-label selectors fixed before complement-Z.

    No random matrix is sampled to assert this bound. This is exact union
    arithmetic for the native IID Bernoulli B law; see the proof document.
    """
    integer(n, "native dimension", 32, 4096)
    m = 3 * n
    w = m // 32 if w is None else integer(w, "support cutoff", 1, n // 2)
    r = w // 2 if r is None else integer(r, "rank cutoff", 1, w)
    if not 1 <= r <= w <= n // 2:
        raise ValueError("require 1 <= r <= w <= n/2")
    full_rank_failure = Fraction((1 << n) - 1, 1 << m)
    small_support_failure = Fraction(2 * sum(comb(m, j) for j in range(w)) - 1, 1 << n)
    exponent = (n - r + 1) * (w - r + 1)
    cut_failure = min(Fraction(1), Fraction(16 * (n + 1)**2 * (1 << m), 1 << exponent))
    failure = min(Fraction(1), full_rank_failure + small_support_failure + cut_failure)
    good_success = Fraction(1, 1 << r)
    source_mean = failure + (1 - failure) * good_success
    return {
        "dimension": n, "original_registers": m,
        "minimum_kernel_support_and_complement": w, "uniform_cut_rank_lower_bound": r,
        "rank_pair_exponent_minimum": exponent,
        "full_rank_failure_upper_bound": dyadic(full_rank_failure),
        "small_or_near_full_kernel_support_failure_upper_bound": dyadic(small_support_failure),
        "small_cut_rank_and_full_rank_failure_upper_bound": dyadic(cut_failure),
        "bad_low_matrix_probability_upper_bound": dyadic(failure),
        "extra_descent_probability_given_good_B_upper_bound": dyadic(good_success),
        "native_source_mean_extra_descent_upper_bound": dyadic(source_mean),
        "source_bound_vacuous": failure == 1,
        "uniform_over_every_precomplement_full_label_selector": True,
        "good_B_bound_uniform_over_initial_parity_syndrome": True,
        "native_mean_before_source_or_syndrome_postselection": True,
        "post_complement_direction_selection_covered": False,
        "quantum_query_lower_bound": False,
    }


def direct_complement_census(labels, phase_bits, direction, origin):
    """Small original signed-label reference, independent of affine image code."""
    m = len(labels[0])
    if m > 8:
        raise ValueError("UNKNOWN: direct physical complement census limited to m<=8")
    rows = tuple(sum((a & 1) << i for i, a in enumerate(row)) for row in labels)
    syndrome = binary_map(rows, origin)
    hist = Counter()
    pairs = []
    Q = 1 << (phase_bits - 1)
    for x in range(1 << m):
        if binary_map(rows, x) != syndrome or x > (x ^ direction):
            continue
        y = x ^ direction
        differences = tuple(sum(a * (((y >> i) & 1) - ((x >> i) & 1))
                                for i, a in enumerate(row)) for row in labels)
        if any(d & 1 for d in differences):
            raise ArithmeticError("original chart phase difference not even")
        output = tuple(d // 2 % Q for d in differences)
        low = sum((v & 1) << j for j, v in enumerate(output))
        hist[low] += 1
        pairs.append({"x_hex": hex(x), "x_xor_u_hex": hex(y),
                      "output_label_hex": [hex(a) for a in output]})
    return {"physical_complement_pairs": pairs,
            "low_output_histogram": {hex(k): v for k, v in sorted(hist.items())},
            "extra_descent_probability": dyadic(Fraction(hist[0], sum(hist.values())))}


def physical_controls():
    controls = []
    # Both parity syndromes, unattainable targets, rank-zero exceptional B,
    # and multiple high phase levels are retained instead of cherry-picked.
    for t in (3, 4, 8, 64):
        q = 1 << t
        for seed in range(3):
            B = (45, 54)
            labels = tuple(tuple(((b >> i) & 1) + 2 * ((seed * 7 + i * i + j * i + j) % (q // 2))
                                 for i in range(6)) for j, b in enumerate(B))
            kernel = binary_kernel(B, 6)
            choices = [u for u in range(1, 64) if binary_map(B, u) == 0]
            # Bounded calibration of a genuinely HIGH-label-dependent selector:
            # prefer directions whose output at the zero background is even.
            direction = min(choices, key=lambda u: (
                any(sum(a for i, a in enumerate(row) if u >> i & 1) // 2 & 1
                    for row in labels), u))
            for origin in (0, 1):
                law = posterior_law(labels, t, direction, origin)
                census = direct_complement_census(labels, t, direction, origin)
                if law["extra_descent_probability"] != census["extra_descent_probability"]:
                    raise ArithmeticError("physical complement census disagrees")
                controls.append({"law": law, "direct_census": census,
                                 "selector": "min(zero-background-not-even, physical-mask)",
                                 "selector_bounded_enumeration_only": True,
                                 "selector_kernel_dimension": len(kernel)})
    # All-one direction: T_u=B|ker(B)=0. It is not silently covered by a
    # uniform positive-rank assertion; this exceptional support must be paid.
    for labels, direction, origin in ((((1, 1, 1, 1),), 15, 0),
                                      (((1, 1, 1, 1),), 3, 0),
                                      (((0, 0, 0), (0, 0, 0)), 1, 0),
                                      (((1, 3),), 3, 1)):
        law = posterior_law(labels, 3, direction, origin)
        controls.append({"law": law,
                         "direct_census": direct_complement_census(labels, 3, direction, origin),
                         "selector": "explicit-exception-or-affine-target-control",
                         "selector_bounded_enumeration_only": True})
    return controls


def small_rank_exponent_controls():
    rows = []
    for n in range(2, 10):
        for w in range(1, n // 2 + 1):
            for r in range(1, w + 1):
                minimum = min(rank_pair_exponent(n, s, a, b)
                              for s in range(w, 3 * n - w + 1)
                              for a in range(min(n, s) + 1)
                              for b in range(min(n, 3 * n - s) + 1)
                              if n <= a + b < n + r)
                expected = (n - r + 1) * (w - r + 1)
                if minimum != expected:
                    raise ArithmeticError("rank-pair exponent minimization falsified")
                rows.append({"n": n, "w": w, "r": r,
                             "exhaustive_integer_minimum": minimum})
    return rows


def exhaustive_low_rank_identity_controls():
    cases = 0
    for n, m in ((1, 3), (2, 4)):
        for rows in product(range(1 << m), repeat=n):
            kernel = binary_kernel(rows, m)
            for u in range(1, 1 << m):
                if binary_map(rows, u):
                    continue
                mapped = [binary_map(tuple(b & u for b in rows), w) for w in kernel]
                if len(binary_basis(mapped, n)) != connectivity_rank(rows, m, u):
                    raise ArithmeticError("exhaustive connectivity identity failed")
                cases += 1
    return {"all_binary_matrices_shapes": [[1, 3], [2, 4]],
            "nonzero_kernel_directions_checked": cases}


def build_report():
    contract = json.loads(CONTRACT.read_text())
    return {
        "schema_version": "1.0.0",
        "status": "LOCAL_SINGLE_OUTPUT_DESCENT_OBSTRUCTION_REVIEW_PENDING",
        "contract_id": contract["contract_id"],
        "native_source_bounds": [native_bound(n) for n in (32, 64, 128, 256, 512, 1024)],
        "physical_controls": physical_controls(),
        "rank_pair_minimization_controls": small_rank_exponent_controls(),
        "exhaustive_connectivity_controls": exhaustive_low_rank_identity_controls(),
        "scope": contract["scope"],
        "remaining_proof_obligations": contract["remaining_proof_obligations"],
        "provisional_negative_result": {
            "id": "NEG-DCP-PRECOMPLEMENT-HIGH-LABEL-SINGLE-DIRECTION-DESCENT",
            "claim_restricted": "Full-label pre-complement direction selection makes simultaneous extra phase descent frequent on native IID vector labels.",
            "status": "LOCAL_DERIVATION_NOT_CENTRALLY_PROMOTED",
            "evidence": "Uniform random-B cut-rank bound and exact complement pushforward law",
            "general_DCP_lower_bound": False,
        },
        "accepted_speedup_candidate": False, "novelty_claim": False,
        "efficient_quantum_receiver_supplied": False,
        "source_quantum_preparations_executed": 0,
        "mathematical_background": {
            "matroid_connectivity_definition": "r(S)+r(E-S)-r(E), without +1 convention",
            "reference": "https://collaborate.princeton.edu/en/publications/on-the-connectivity-function-of-a-matroid/",
            "reference_does_not_prove_this_DCP_source_claim": True,
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args(argv)
    report = build_report()
    if not args.no_write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"],
                      "physical_controls": len(report["physical_controls"]),
                      "accepted_speedup_candidate": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
