"""Native-source collision converse for nonadaptive individual phase readout.

LOCAL DERIVATION / REVIEW PENDING. Not a no-go for adaptive local instruments,
entangled measurements, higher sample budgets or classical arithmetic solvers.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np

from dcp_bell_inference_kernel import exact
from dcp_terminal_affine_fibers import _positive_integer

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/dcp_native_product_readout_bound.json"


def native_product_readout_certificate(n, L, m):
    for value, name in ((n, "dimension"), (L, "modulus bits"), (m, "phase qubits")):
        _positive_integer(value, name)
    G, Ghalf = 1 << (n*L), 1 << (n*(L-1))
    C = Fraction(3, 2)**m
    squared = min(Fraction(1), (C+(2**m-C)/Ghalf)/G)
    exponent = ((squared.denominator//squared.numerator).bit_length()-1)//2
    return {
        "status": "LOCAL_NATIVE_NONADAPTIVE_PRODUCT_POVM_CONVERSE_REVIEW_PENDING",
        "dimension": n, "modulus_bits": L, "phase_qubits": m,
        "native_hidden_group_size": str(G), "doubled_character_image_size": str(Ghalf),
        "source_mean_uniform_secret_correct_probability_squared_upper_bound": exact(squared),
        "bound_also_applies_to_mean_of_squared_conditional_uniform_secret_success": True,
        "simultaneous_high_probability_label_gate": "Pr_A[any allowed product POVM achieves conditional uniform-secret success>=delta] <= min(1,bound_squared/delta^2)",
        "conservative_correct_probability_dyadic_exponent": exponent,
        "source_bound": "min(1,sqrt(((3/2)^m+(2^m-(3/2)^m)/(q/2)^n)/q^n))",
        "entire_public_label_matrix_may_choose_all_local_POVMs": True,
        "arbitrary_single_qubit_POVM_outcomes_private_ancillas_and_shared_public_randomness_allowed": True,
        "unlimited_classical_or_quantum_processing_of_classical_outcomes_allowed": True,
        "hidden_secret_uniform_independent_of_IID_native_labels_required": True,
        "measurement_choice_may_depend_on_previous_outcomes": False,
        "claim_is_pointwise_for_each_fixed_secret_or_label_matrix": False,
        "adaptive_local_or_entangled_measurements_ruled_out": False,
        "classical_arithmetic_subset_sum_task_bounded": False,
        "candidate_record_accepted": False, "speedup_claim_allowed": False,
    }


def _povm(outcomes):
    rows = np.asarray(outcomes, dtype=float)
    if rows.ndim != 2 or rows.shape[1] != 4 or not len(rows) or not np.all(np.isfinite(rows)):
        raise ValueError("finite weight,Bloch-x,Bloch-y,Bloch-z rows required")
    if np.any(rows[:, 0] <= 0) or np.any(np.sum(rows[:, 1:]**2, axis=1) > 1+1e-10):
        raise ValueError("positive weights and positive qubit effects required")
    if abs(float(np.sum(rows[:, 0]))-1) > 1e-10 or np.max(np.abs(rows[:, 0]@rows[:, 1:])) > 1e-10:
        raise ValueError("POVM must sum to identity")
    return rows


def projective_povm(angle):
    return _povm(((0.5, math.cos(angle), math.sin(angle), 0),
                  (0.5, -math.cos(angle), -math.sin(angle), 0)))


def _product_control(A, q, measurements):
    n, m = len(A), len(A[0])
    P = [_povm(p) for p in measurements]
    if len(P) != m:
        raise ValueError("one independent instrument per native phase qubit required")
    secrets = list(itertools.product(range(q), repeat=n))
    probabilities = []
    collision_envelope = 0.0
    for s in secrets:
        theta = [2*math.pi*(sum(A[j][i]*s[j] for j in range(n)) % q)/q for i in range(m)]
        probabilities.append([p[:, 0]*(1+p[:, 1]*math.cos(t)+p[:, 2]*math.sin(t)) for p, t in zip(P, theta)])
        collision_envelope += math.prod(1+math.cos(t)**2 for t in theta)/len(secrets)
    success = weighted_collision = 0.0
    for y in itertools.product(*(range(len(p)) for p in P)):
        base = math.prod(P[i][v, 0] for i, v in enumerate(y))
        likelihood = [math.prod(p[i][v] for i, v in enumerate(y)) for p in probabilities]
        success += max(likelihood)/len(secrets)
        weighted_collision += sum(v*v/base for v in likelihood)/len(secrets)
    assert weighted_collision <= collision_envelope+1e-9
    bound = min(1, math.sqrt(collision_envelope/len(secrets)))
    assert success <= bound+1e-9
    return {"labels": A, "modulus": q, "dimension": n,
            "local_POVMs_weight_and_Bloch_rows": [p.tolist() for p in P],
            "actual_optimal_decoder_correct_probability": success,
            "actual_mean_weighted_likelihood_collision": weighted_collision,
            "matrix_pointwise_collision_envelope": collision_envelope,
            "matrix_pointwise_correct_probability_upper_bound": bound,
            "enumeration_is_an_efficient_native_decoder": False}


def _complete_native_source_controls():
    records = []
    for n, q, m in ((1, 4, 2), (1, 8, 2), (2, 4, 2)):
        total = 0.0
        for entries in itertools.product(range(q), repeat=n*m):
            A = tuple(entries[j*m:(j+1)*m] for j in range(n))
            value = 0.0
            for s in itertools.product(range(q), repeat=n):
                value += math.prod(1+math.cos(2*math.pi*(sum(A[j][i]*s[j] for j in range(n)) % q)/q)**2
                                   for i in range(m))/q**n
            total += value/q**(n*m)
        expected = (3/2)**m+(2**m-(3/2)**m)/(q//2)**n
        assert abs(total-expected) < 1e-9
        records.append({"dimension": n, "modulus": q, "phase_qubits": m,
                        "complete_native_label_matrices": q**(n*m), "secrets_per_matrix": q**n,
                        "actual_native_mean_collision_envelope": total,
                        "exact_rational_native_mean_collision_envelope": exact(Fraction(3, 2)**m+(2**m-Fraction(3, 2)**m)/(q//2)**n)})
    return records


def _adaptive_scope_countercontrol():
    # Known q4 calibration: measuring label2 in X first reveals parity;
    # label1 then requires X for even secrets and Y for odd secrets.
    successes = []
    for s in range(4):
        total = 0.0
        for parity, high in itertools.product(range(2), repeat=2):
            p2 = (1+(-1)**parity*math.cos(math.pi*s))/2
            mean = math.cos(math.pi*s/2) if parity == 0 else math.sin(math.pi*s/2)
            p1 = (1+(-1)**high*mean)/2
            if parity+2*high == s:
                total += p2*p1
        assert abs(total-1) < 1e-10
        successes.append(total)
    product = _product_control(((1, 2),), 4, [projective_povm(0)]*2)
    assert abs(product["actual_optimal_decoder_correct_probability"]-0.75) < 1e-10
    return {"labels": [[1, 2]], "modulus": 4, "adaptive_every_secret_correct_probabilities": successes,
            "nonadaptive_X_optimal_correct_probability": 0.75,
            "nonadaptive_matrix_pointwise_correct_probability_bound": product["matrix_pointwise_correct_probability_upper_bound"],
            "native_literal_label_probability": exact(Fraction(1, 16)),
            "scalable_native_adaptive_label_selector_or_decoder_supplied": False,
            "general_adaptive_measurement_impossibility_claim_allowed": False}


def run_controls():
    trine = _povm([(1/3, math.cos(2*math.pi*k/3), math.sin(2*math.pi*k/3), 0) for k in range(3)])
    tetra = _povm([(0.25, x/math.sqrt(3), y/math.sqrt(3), z/math.sqrt(3)) for x,y,z in
                  ((1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1))])
    controls = []
    for A, q in ((((1, 2),), 4), (((1, 3, 7),), 8), (((1, 0, 3), (2, 1, 2)), 4)):
        for family in ("label_adaptive_projective", "trine", "tetrahedral"):
            measurements = [projective_povm(2*math.pi*(A[0][i]+i)/q) if family == "label_adaptive_projective"
                            else (trine if family == "trine" else tetra) for i in range(len(A[0]))]
            controls.append({"family": family, **_product_control(A, q, measurements)})
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING",
            "actual_arbitrary_product_POVM_controls": controls,
            "complete_native_source_controls": _complete_native_source_controls(),
            "adaptive_scope_countercontrol": _adaptive_scope_countercontrol(),
            "native_near_entropy_width_ledgers": [native_product_readout_certificate(n, 4*n+1, n*(4*n+1)+16) for n in (8, 16, 32)],
            "order_two_exception_ledger": native_product_readout_certificate(8, 1, 8),
            "claim_gate": {"near_entropy_width_nonadaptive_product_readout_high_success_allowed": False,
                           "source_bound_uses_legal_native_states_not_a_noise_conversion_assumption": True,
                           "adaptive_local_or_collective_quantum_decoder_ruled_out": False,
                           "independent_mathematical_review_complete": False,
                           "candidate_record_accepted": False, "novelty_claim": False, "speedup_claim_allowed": False},
            "dependency_sha256": {str(Path(__file__).relative_to(ROOT)): hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"status": report["status"], "claim_gate": report["claim_gate"],
                      "correct_probability_dyadic_exponents": [r["conservative_correct_probability_dyadic_exponent"] for r in report["native_near_entropy_width_ledgers"]]}, indent=2))


if __name__ == "__main__":
    main()
