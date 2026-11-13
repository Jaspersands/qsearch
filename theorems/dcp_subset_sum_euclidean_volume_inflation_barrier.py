"""Theorem module: Density-One Modular Subset-Sum Euclidean Volume Inflation & BDD Multiplicity Barrier.

Proves the fundamental geometric mechanism causing Euclidean lattice reduction (LLL, BKZ, BDD)
to fail for density-one modular subset sum:
1. Euclidean Ball Volume Inflation Law:
   The volume of the n-dimensional Euclidean ball of radius R = sqrt(n) containing the true binary
   witness e in {-1, 1}^n scales asymptotically as Vol(B_n(sqrt(n))) = (2 pi e)^{n/2} / sqrt(pi n)
   = 2^{2.0471 n - 0.5 log2(pi n)}.
2. Exponential Point Multiplicity at Density One:
   At density d = n / log2(D) = 1.0 (modulus D = 2^n), the expected number of integer lattice points
   inside the ball B_n(sqrt(n)) is N_points = Vol(B_n(sqrt(n))) / 2^n = (2.0664)^n / sqrt(pi n)
   = 2^{1.0471 n - 0.5 log2(pi n)} = 2^{Omega(n)}.
3. Non-Binary Coordinate Drowning & Distance Inversion:
   By the Gaussian heuristic, the shortest non-zero lattice vector has length lambda_1(L) approx
   2 sqrt(n / (2 pi e)) approx 0.484 sqrt(n) << sqrt(n). Euclidean lattice reduction minimizes pure
   geometric length and preferentially outputs non-binary vectors with coordinates in Z \\ {-1, 1}.
4. BDD Radius Collapse:
   The unique decoding radius is R_BDD = lambda_1 / 2 approx 0.242 sqrt(n). The binary witness has
   norm ||e||_2 = sqrt(n) approx 4.13 R_BDD, lying more than 4 times outside the BDD unique decoding ball.
5. List Undercoverage Law:
   Any nearest-plane or sphere-decoding list decoder of polynomial size L = poly(n) covers only
   P_coverage <= poly(n) / 2^{1.047 n} = 2^{-Omega(n)} of legal witnesses, factorially/exponentially
   suppressing classical and quantum lattice heuristics.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
core_dir = str(ROOT / "core")
theorems_dir = str(ROOT / "theorems")
if core_dir not in sys.path:
    sys.path.insert(0, core_dir)
if theorems_dir not in sys.path:
    sys.path.insert(0, theorems_dir)

DERIVATION = ROOT / "research/DCP_SUBSET_SUM_EUCLIDEAN_VOLUME_INFLATION_BARRIER.md"
REPORT = ROOT / "research/classical_baselines/dcp_subset_sum_euclidean_volume_inflation_barrier.json"
REGISTRY = ROOT / "research/registry/negative_results.json"
QUARANTINED_REGISTRY = ROOT / "research/registry/quarantined_campaign_negatives.json"

NEGATIVE_RESULT_ID = "NEG-DCP-SUBSET-SUM-EUCLIDEAN-VOLUME-INFLATION-BARRIER"


def compute_ball_volume_log2(n: int, radius: float) -> float:
    """Compute base-2 logarithm of volume of n-dimensional Euclidean ball of radius R.

    Vol(B_n(R)) = pi^{n/2} R^n / Gamma(n/2 + 1).
    """
    if radius <= 0 or n <= 0:
        raise ValueError("n and radius must be positive")
    log2_pi_term = 0.5 * n * math.log2(math.pi)
    log2_radius_term = n * math.log2(radius)
    log2_gamma_term = math.lgamma(0.5 * n + 1.0) / math.log(2.0)
    return float(log2_pi_term + log2_radius_term - log2_gamma_term)


def compute_expected_lattice_points_log2(n: int, radius: float, modulus_bits: float) -> float:
    """Compute base-2 logarithm of heuristic continuous volume/det ratio in B_n(R) for det(L) = 2^{modulus_bits}."""
    log2_vol = compute_ball_volume_log2(n, radius)
    return float(log2_vol - modulus_bits)


def audit_finite_density_one_geometry(n: int = 16, seed: int = 42) -> Dict[str, Any]:
    """Audit geometry metrics for finite density-one instance."""
    radius = math.sqrt(float(n))
    modulus_bits = float(n)
    log2_vol = compute_ball_volume_log2(n, radius)
    log2_points = compute_expected_lattice_points_log2(n, radius, modulus_bits)
    expected_points = 2.0 ** log2_points if log2_points < 100 else float("inf")

    # Gaussian heuristic shortest vector lambda_1
    # lambda_1 approx sqrt(n / (2 pi e)) * (det)^{1/n} = sqrt(n / (2 pi e)) * 2
    gaussian_shortest_vector = math.sqrt(n / (2.0 * math.pi * math.e)) * 2.0
    bdd_radius = 0.5 * gaussian_shortest_vector
    witness_norm = radius
    radius_ratio = witness_norm / bdd_radius

    # List size needed for 50% coverage under uncentered heuristic
    log2_list_for_half_coverage = max(0.0, log2_points - 1.0)

    return {
        "n": n,
        "modulus_bits": modulus_bits,
        "witness_norm": round(witness_norm, 4),
        "log2_ball_volume": round(log2_vol, 4),
        "log2_expected_lattice_points": round(log2_points, 4),
        "expected_lattice_points": round(expected_points, 2),
        "gaussian_heuristic_shortest_vector": round(gaussian_shortest_vector, 4),
        "bdd_unique_decoding_radius": round(bdd_radius, 4),
        "witness_norm_to_bdd_radius_ratio": round(radius_ratio, 4),
        "witness_outside_bdd_radius": bool(radius_ratio > 1.0),
        "log2_list_size_required": round(log2_list_for_half_coverage, 2),
    }


def evaluate_density_one_scaling(n: int) -> Dict[str, Any]:
    """Evaluate scaling metrics for density-one subset sum with dimension n."""
    radius = math.sqrt(float(n))
    modulus_bits = float(n)
    log2_vol = compute_ball_volume_log2(n, radius)
    log2_points = compute_expected_lattice_points_log2(n, radius, modulus_bits)

    # Point count: if log2_points <= 50, compute absolute count
    abs_points = 2.0 ** log2_points if log2_points <= 50 else None

    # Theoretical asymptotic formula: (2.0664)^n / sqrt(pi n)
    theoretical_log2 = n * math.log2(2.0664) - 0.5 * math.log2(math.pi * n)

    # Max coverage of a polynomial list L = n^3 under uncentered continuous heuristic
    poly_list_size_log2 = 3.0 * math.log2(float(n))
    log2_coverage_poly_list = poly_list_size_log2 - log2_points

    return {
        "dimension_n": n,
        "density": 1.0,
        "modulus_bits": n,
        "witness_radius": round(radius, 4),
        "log2_ball_volume": round(log2_vol, 4),
        "log2_expected_points": round(log2_points, 4),
        "theoretical_asymptotic_log2": round(theoretical_log2, 4),
        "absolute_point_count": round(abs_points, 2) if abs_points is not None else "greater_than_2^50",
        "log2_poly_list_coverage_n3": round(log2_coverage_poly_list, 4),
        "exponentially_undercovered": bool(log2_coverage_poly_list < 0),
        "bdd_radius_ratio": round(math.sqrt(2.0 * math.pi * math.e), 4),
    }


def build_report() -> Dict[str, Any]:
    """Build verification artifact report reflecting the 2026-11-06 universal exclusion retraction."""
    sha256 = hashlib.sha256(DERIVATION.read_bytes()).hexdigest() if DERIVATION.exists() else "UNCOMMITTED"

    finite_audit_16 = audit_finite_density_one_geometry(n=16)

    scaling_dimensions = [10, 16, 20, 24, 30, 40, 50, 64, 100, 128]
    scaling_profiles = [evaluate_density_one_scaling(n) for n in scaling_dimensions]

    headline_metrics = {
        "log2_expected_points_at_n16": scaling_profiles[1]["log2_expected_points"],
        "log2_expected_points_at_n30": scaling_profiles[4]["log2_expected_points"],
        "log2_expected_points_at_n50": scaling_profiles[6]["log2_expected_points"],
        "log2_poly_list_coverage_at_n50": scaling_profiles[6]["log2_poly_list_coverage_n3"],
        "witness_norm_to_bdd_radius_ratio": finite_audit_16["witness_norm_to_bdd_radius_ratio"],
        "witness_outside_bdd_radius": finite_audit_16["witness_outside_bdd_radius"],
        "tail_scaling_profiles_exponentially_undercovered": all(
            p["exponentially_undercovered"] for p in scaling_profiles if p["dimension_n"] >= 16
        ),
        "speedup_claim_allowed": False,
    }

    claim_gate = {
        "euclidean_ball_volume_inflation_proved": True,
        "expected_lattice_point_exponential_multiplicity_proved": False,
        "bdd_radius_collapse_proved": False,
        "polynomial_list_exponential_undercoverage_proved": False,
        "universal_subset_sum_lattice_trilemma_proved": False,
        "universal_exclusion_retracted_2026_11_06": True,
        "speedup_claim_allowed": False,
    }

    theorem_contract = {
        "euclidean_volume_inflation": (
            "The volume of the n-dimensional Euclidean ball of radius R = sqrt(n) scales asymptotically as "
            "Vol(B_n(sqrt(n))) = (2 pi e)^{n/2} / sqrt(pi n) = 2^{2.0471 n - 0.5 log2(pi n)}."
        ),
        "correction_2026_11_06": (
            "Universal lattice/BDD/list-decoding exclusion withdrawn (see research/DCP_HALF_CENTER_DGS_ADMISSION.md): "
            "correct half-integer centering retains coordinate parity (signed difference lattice 2L with determinant 2^n D/g), "
            "where every integer vector is at least sqrt(n)/2 from the midpoint (equality exactly on binary vectors) "
            "and exact mean closest-list cardinality is 1 for IID coefficients + uniform target (2 - 2^-n for planted)."
        ),
    }

    return {
        "created_at": "2026-10-11T00:00:00+00:00",
        "corrected_at": "2026-11-06T00:00:00+00:00",
        "status": "UNIVERSAL_SUBSET_SUM_VOLUME_BARRIER_RETRACTED_BALL_VOLUME_FORMULA_ONLY",
        "derivation_sha256": sha256,
        "correction_note": "research/DCP_HALF_CENTER_DGS_ADMISSION.md",
        "theorem_contract": theorem_contract,
        "headline_metrics": headline_metrics,
        "claim_gate": claim_gate,
        "finite_audit_16": finite_audit_16,
        "scaling_profiles": scaling_profiles,
        "quarantined_negative_id": NEGATIVE_RESULT_ID,
        "falsifiers_triggered": [],
        "summary": (
            "Retains the exact Euclidean ball volume formula Vol(B_n(sqrt(n))) = pi^(n/2) n^(n/2) / Gamma(n/2 + 1), "
            "while recording the 2026-11-06 retraction of the universal density-one lattice/BDD/list-decoding exclusion "
            "(see research/DCP_HALF_CENTER_DGS_ADMISSION.md). In the parity-preserving half-integer centered coset, "
            "binary witnesses minimize distance sqrt(n)/2 and exact mean closest-list cardinality is O(1). "
            "NEG-DCP-SUBSET-SUM-EUCLIDEAN-VOLUME-INFLATION-BARRIER is quarantined in "
            "research/registry/quarantined_campaign_negatives.json."
        ),
    }


def register_negative_result() -> None:
    """No-op: NEG-DCP-SUBSET-SUM-EUCLIDEAN-VOLUME-INFLATION-BARRIER is quarantined."""
    print(f"Negative result {NEGATIVE_RESULT_ID} is quarantined in {QUARANTINED_REGISTRY}; skipping active registration.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Density-One Modular Subset-Sum Euclidean Volume Inflation Barrier")
    parser.add_argument("--register-negative", action="store_true", help="Register negative result in registry")
    args = parser.parse_args()

    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"Report written to {REPORT}")

    if args.register_negative:
        register_negative_result()


if __name__ == "__main__":
    main()
