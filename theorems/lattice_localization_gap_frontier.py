"""Public dense-ternary source schedules, challenged before any hardness claim."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from sympy import nextprime

from theorems.lattice_cube_coset_source import exact_int
from theorems.planted_qary_cube_basis_coordinate_bridge import ternary_pivot_envelope
from theorems.planted_qary_usvp_source import (
    generate_source, public_LLL_attack, sparse_column_attack, audit_attacks,
)
from theorems.lattice_sine_window_source import SineWindowSource, resource_estimate
from theorems.ternary_measured_lattice_decoder import exact_json

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/lattice_localization_gap_frontier.json"
DOC = ROOT / "research/LATTICE_LOCALIZATION_GAP_FRONTIER.md"


def dyadic_ceiling(x):
    x = Fraction(x)
    if x <= 0:
        raise ValueError("positive exact dyadic target required")
    value = 2
    while value < x:
        value *= 2
    return value


def public_schedule(n, m, noise_mode):
    """No basis, short vector, source seed or successful trial enters this plan.

    Family promise: ALL n plant coordinates are +/-1. Every free coordinate
    is therefore a unit; the first free basis row can be chosen publicly.
    Orientation up to sign is allowed, not learned from a private witness.
    """
    exact_int(n, "dimension", 3)
    exact_int(m, "constraint count", 1)
    if m >= n - 1 or noise_mode not in ("constant", "inverse_log"):
        raise ValueError("rectangular kernel and explicit noise mode required")
    free = n - m
    L = free - 1 + m * ternary_pivot_envelope(free)
    M = 2
    while True:
        ell = n * M.bit_length()
        epsilon = Fraction(1, 8) if noise_mode == "constant" else Fraction(1, ell)
        if Fraction(L, M) <= epsilon / 2:
            break
        M *= 2
    K = 2
    while Fraction(242 * n, 49 * K * K) > epsilon / 2:
        K *= 2
    W = dyadic_ceiling(2 * n / epsilon)
    packet_loss = Fraction(242 * n, 49 * K * K)
    cube_loss = Fraction(n, W)
    boundary_loss = Fraction(L, M)
    return {
        "dimension": n, "constraint_count": m, "dense_ternary_norm_squared": n,
        "first_free_basis_coordinate": m, "residue": 1,
        "coordinate_trials_required_under_dense_ternary_promise": 1,
        "private_hitting_coordinate_selector_used": False,
        "sparse_ternary_supports_covered_by_this_one_trial_plan": False,
        "noise_mode": noise_mode, "epsilon": str(epsilon), "parent_side": M,
        "position_wires": ell, "public_parent_shift_L1_upper": L,
        "boundary_loss_upper": str(boundary_loss),
        "cube": {"side": W, "sufficient_relative_gap": W,
                 "split_prime": int(nextprime(W + 1)),
                 "localization_loss_upper": str(cube_loss),
                 "total_loss_upper_IF_geometry_holds": str(cube_loss + boundary_loss)},
        "sine": {"side": K, "sufficient_relative_gap": K,
                 "split_prime": int(nextprime(K + 1)),
                 "localization_loss_upper": str(packet_loss),
                 "total_loss_upper_IF_geometry_holds": str(packet_loss + boundary_loss)},
        "unique_vector_gap_is_an_external_promise": True,
        "individual_instance_gap_certified": False,
        "constant_noise_satisfies_inverse_log_budget": epsilon <= Fraction(1, ell),
        "efficient_robust_receiver_supplied": False,
        "quantum_advantage_claimed": False,
    }


def attack_control(n, noise_mode, seed):
    """Generate once, attack PUBLIC input, then perform private calibration."""
    m = n // 2
    schedule = public_schedule(n, m, noise_mode)
    chosen = schedule["sine"]
    generated = generate_source(n, m=m, gap=chosen["sufficient_relative_gap"],
                                support=n, plant_seed=seed, matrix_seed=seed + 1000)
    problem = generated.problem
    # No source/trial filtering based on any attack outcome.
    attacks = {"sparse_columns": sparse_column_attack(problem), "LLL": public_LLL_attack(problem)}
    private = audit_attacks(generated, attacks)
    source = SineWindowSource(problem.basis, chosen["split_prime"], 1, m,
                              schedule["parent_side"], chosen["side"])
    recovered = private["tested_instance_classically_recovers_planted_direction"]
    falsifier = {
        "scope": "THIS_PUBLIC_GENERATED_INSTANCE_AND_IMPLEMENTED_ATTACKS_ONLY",
        "classical_recovery_of_plant_verified": recovered,
        "all_lower_gap_lattices_dequantized": False,
        "negative_result": "FINITE_SOURCE_HARDNESS_CONTROL_FALSIFIED" if recovered else "UNRESOLVED_NOT_HARDNESS",
        "public_problem_sha256": problem.public_record()["public_problem_sha256"],
    }
    return {
        "public_schedule": schedule, "public_problem": problem.public_record(),
        "public_attacks": attacks,
        "private_calibration_after_attacks": private,
        "PRIVATE_AUDIT_ONLY_planted_vector": generated.private.plant,
        "distributional_uniqueness_ledger": generated.private.ledger,
        "closed_source_resource_estimate_NOT_compiled_or_simulated": resource_estimate(source),
        "finite_classical_falsifier": falsifier,
        "seed_harness": {"plant_seed": seed, "matrix_seed": seed + 1000,
                         "passed_to_public_attack": False},
        "generator_rejects_on_classical_attack_or_uniqueness_outcome": False,
        "BKZ_and_general_SIS_attacks": "NOT_RUN_NOT_EXCLUDED",
        "receiver_or_quantum_speedup_demonstrated": False,
    }


def build_report():
    controls = [attack_control(n, mode, seed)
                for n, seed in ((16, 72001), (32, 72002), (32, 72003), (64, 72004))
                for mode in ("constant", "inverse_log")]
    deps = ("planted_qary_cube_basis_coordinate_bridge.py", "planted_qary_usvp_source.py",
            "lattice_sine_window_source.py", "lattice_sine_packet.py")
    return {
        "status": "PUBLIC_LOCALIZATION_NOISE_GAP_FRONTIER_WITH_CLASSICAL_FALSIFIERS",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DOC.read_bytes()).hexdigest(),
        "dependency_sha256": {p: hashlib.sha256((ROOT / "theorems" / p).read_bytes()).hexdigest() for p in deps},
        "public_scaling_schedules": [public_schedule(n, n // 2, mode)
                                     for n in (16, 32, 64, 128, 256, 512)
                                     for mode in ("constant", "inverse_log")],
        "actual_public_attack_controls": controls,
        "classically_recovered_controls": sum(c["finite_classical_falsifier"]["classical_recovery_of_plant_verified"] for c in controls),
        "controls_tested": len(controls),
        "source_samples_or_quantum_solver_calls_performed": 0,
        "all_lattice_hardness_or_robust_decoding_resolved": False,
        "accepted_speedup_candidate": False,
        "novelty_claim": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("status", "controls_tested", "classically_recovered_controls", "accepted_speedup_candidate")}, indent=2))


if __name__ == "__main__":
    main()
