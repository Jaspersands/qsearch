"""Known-solver closure of public-field Singer membership shifts.

LOCAL DERIVATION / REVIEW PENDING, not a new algorithm. Small FLINT/statevector
controls replace KNOWN discrete logarithms by explicit calibration tables.
The asymptotic route instead pays for coherent Shor computations and cleanup.
"""
from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
from flint import nmod_mat

from dhsp_codomain_instrument import _integer, rational
from singer_residual_hardness import _coords, public_field, singer_parameters

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/singer_shor_access_closure.json"


def rotation_success(q, steps):
    """Exactly sin^2(2*j*asin(1/sqrt(q))), without transcendental rounding."""
    _integer(q, "base order", 2)
    _integer(steps, "Grover steps", 0)
    if steps > 128:
        raise ValueError("exact expanded rotation is a bounded calibration, not a large-q loop")
    cosine = 1-Fraction(8*(q-1), q*q)
    previous, current = Fraction(1), cosine
    if not steps:
        return Fraction(0)
    for _ in range(1, steps):
        previous, current = current, 2*cosine*current-previous
    return (1-current)/2


def access_ledger(q, m, repetitions=16):
    v, k, _ = singer_parameters(q, m)
    _integer(repetitions, "independent repetitions", 1)
    # J=ceil(q/sqrt(q-1)); the exact integer inequality certifies the schedule.
    J = math.isqrt(q*q//(q-1))
    if J*J*(q-1) < q*q:
        J += 1
    return {
        "base_order": str(q), "extension_degree": m,
        "projective_order": str(v), "membership_density": rational(Fraction(k, v)),
        "random_steps_exclusive_upper": str(J),
        "max_membership_queries_per_attempt": str(J-1),
        "expected_membership_queries_per_attempt": rational(Fraction(J-1, 2)),
        "single_attempt_success_lower": rational(Fraction(1, 4)),
        "independent_repetitions": repetitions,
        "ideal_all_attempts_fail_upper": rational(Fraction(3, 4)**repetitions),
        "max_total_membership_queries": str(repetitions*(J-1)),
        "known_coherent_dlog_compute_or_uncompute_calls_upper": str(2*repetitions*(J-1)),
        "underlying_dlog_algorithm_or_inverse_invocations_upper": str(4*repetitions*(J-1)),
        "additional_known_dlog_residual_solver_calls_upper": 1,
        "per_known_arithmetic_call_bit_complexity": "poly(m*log(q), log(1/error)) using a known quantum DLog algorithm",
        "total_runtime_polynomial_in_input_without_q_restriction": False,
        "query_order": "Theta(sqrt(q)) for constant recovery as q grows, under the public-field promise",
        "public_primitive_and_field_embedding_setup_supplied": True,
        "actual_coherent_shor_circuit_implemented_here": False,
        "novel_quantum_mechanism": False,
    }


def coherent_error_budget(phase_queries, total_variation_budget):
    """Conservative norm hybrid for clean BQP function-oracle construction.

    Each coordinate DLog compute/copy/uncompute has norm error <=2 sqrt(e).
    A phase query uses two such maps. Final measurement TV <= global norm error.
    The residual DLog solver has a separate classical output-failure budget.
    """
    _integer(phase_queries, "phase queries", 1)
    if not isinstance(total_variation_budget, Fraction) or not 0 < total_variation_budget < 1:
        raise ValueError("strict exact rational total-variation budget required")
    per_invocation = (total_variation_budget/(4*phase_queries))**2
    return {"membership_phase_queries": str(phase_queries),
            "per_underlying_known_dlog_computation_failure_upper": rational(per_invocation),
            "whole_query_process_total_variation_error_upper": rational(total_variation_budget),
            "worst_case_over_all_coordinate_inputs_required": True,
            "coherent_compute_copy_uncompute_required": True,
            "residual_dlog_output_failure_is_additional": True,
            "physical_compilation_and_qft_error_is_additional": True,
            "secret_oracle_precision_assumed_ideal": True}


def _digits(index, q, m):
    return [(index//q**j) % q for j in range(m)]


def _additive_qft(state, q, m):
    return (np.fft.ifftn(state.reshape((q,)*m, order="F"))*math.sqrt(q**m)).reshape(-1, order="F")


def _known_log_table(K, alpha):
    q, m = int(K.characteristic()), int(K.degree())
    size = q**m
    table = [None]*size
    # Zero has a dedicated sentinel: no fabricated log(0), no erased label.
    table[0] = size-1
    value = K.one()
    for exponent in range(size-1):
        index = sum(c*q**j for j, c in enumerate(_coords(value, m)))
        if table[index] is not None:
            raise ValueError("public primitive element did not give a field-coordinate permutation")
        table[index] = exponent
        value *= alpha
    if any(e is None for e in table):
        raise ValueError("incomplete bounded known-log calibration")
    return np.array(table, dtype=int)


def _clean_membership_phase(state, logs, membership, v):
    """Execute compute / XOR-kickback / uncompute, including zero input.

    This uses one unknown XOR call: its target is |+> at x=0 and |-> otherwise.
    A known zero-input phase supplies the correct marked sign at zero.
    """
    size = len(state)
    graph = np.zeros((size, size, 2), dtype=complex)
    graph[np.arange(size), logs, 0] = state/math.sqrt(2)
    graph[np.arange(size), logs, 1] = state/math.sqrt(2)
    graph[1:, :, 1] *= -1
    marked_logs = np.array([membership[int(e % v)] for e in range(size)], dtype=bool)
    graph[:, marked_logs, :] = graph[:, marked_logs, ::-1]
    graph[0] *= -1
    graph[1:, :, 1] *= -1
    decoded = (graph[:, :, 0]+graph[:, :, 1])/math.sqrt(2)
    target_leak = (graph[:, :, 0]-graph[:, :, 1])/math.sqrt(2)
    output = decoded[np.arange(size), logs]
    decoded[np.arange(size), logs] = 0
    return output, float(np.sum(abs(decoded)**2)+np.sum(abs(target_leak)**2))


def physical_control(q, m, shift):
    """All schedule branches, Fourier outputs, and failures; no lucky shifts."""
    v, _, _ = singer_parameters(q, m)
    _integer(shift, "canonical hidden shift", 0)
    if shift >= v or q**m > 256:
        raise ValueError("canonical shift and bounded field (<=256) required")
    K, alpha, public = public_field(q, m)
    size, beta = q**m, alpha**shift
    basis = [K.gen()**j for j in range(m)]
    pairing = [[int((a*b).trace()) for b in basis] for a in basis]
    T = nmod_mat(pairing, q)
    logs = _known_log_table(K, alpha)
    # The hidden beta occurs ONLY in the declared source and calibration scoring.
    membership = [int((beta*alpha**k).trace() == 0) for k in range(v)]
    line_coordinates = []
    for scalar in range(q):
        normal = _coords(beta*scalar, m)
        dual = [sum(pairing[i][j]*normal[j] for j in range(m)) % q for i in range(m)]
        line_coordinates.append(sum(c*q**j for j, c in enumerate(dual)))
    decoded_shifts, wrong_basis_shifts = [None]*size, [None]*size
    for y in range(1, size):
        vector = nmod_mat([[_digits(y, q, m)[j]] for j in range(m)], q)
        recovered = T.solve(vector)
        z = K([int(recovered[j, 0]) for j in range(m)])
        target = z**(q-1)
        index = sum(c*q**j for j, c in enumerate(_coords(target, m)))
        exponent = int(logs[index])
        assert exponent % (q-1) == 0
        decoded_shifts[y] = exponent//(q-1)
        wrong_target = K(_digits(y, q, m))**(q-1)
        wrong_index = sum(c*q**j for j, c in enumerate(_coords(wrong_target, m)))
        wrong_basis_shifts[y] = int(logs[wrong_index])//(q-1)
    uniform = np.ones(size, dtype=complex)/math.sqrt(size)
    ledger = access_ledger(q, m)
    branches, state, max_leak = [], uniform.copy(), 0.0
    for steps in range(int(ledger["random_steps_exclusive_upper"])):
        if steps:
            state, leak = _clean_membership_phase(state, logs, membership, v)
            max_leak = max(max_leak, leak)
            state = 2*uniform*np.vdot(uniform, state)-state
        transformed = _additive_qft(state, q, m)
        probabilities = abs(transformed)**2
        theoretical = rotation_success(q, steps)
        scored = sum(float(p) for y, p in enumerate(probabilities) if decoded_shifts[y] == shift)
        wrong_score = sum(float(p) for y, p in enumerate(probabilities) if wrong_basis_shifts[y] == shift)
        outside = sum(float(p) for y, p in enumerate(probabilities) if y not in line_coordinates)
        branches.append({"grover_steps": steps, "unknown_xor_oracle_calls": steps,
                         "known_dlog_compute_or_uncompute_calls": 2*steps,
                         "exact_nonzero_fourier_success": rational(theoretical),
                         "executed_shift_success": scored,
                         "zero_output_failure": float(probabilities[0]),
                         "off_annihilator_probability": outside,
                         "total_probability": float(sum(probabilities)),
                         "all_output_probabilities": probabilities.tolist(),
                         "incorrect_dual_basis_decoder_success": wrong_score,
                         "discarded_injective_log_workspace_fourier_success": float(Fraction(q-1, size)),
                         "postselection_or_failure_renormalization": False})
    average = sum((rotation_success(q, b["grover_steps"]) for b in branches), Fraction(0))/len(branches)
    return {**public, "hidden_shift_calibration": str(shift), "ledger": ledger,
            "source_bits": membership, "known_log_calibration_permutation": logs.tolist(),
            "trace_pairing_matrix": pairing, "annihilator_coordinate_indices": line_coordinates,
            "decoded_shift_by_fourier_coordinate": decoded_shifts,
            "incorrect_raw_basis_decoder_by_coordinate": wrong_basis_shifts,
            "branches": branches, "exact_schedule_mean_success": rational(average),
            "maximum_executed_cleanup_leakage": max_leak,
            "small_table_replaces_known_Shor_only_for_calibration": True,
            "actual_coherent_Shor_implementation": False,
            "initial_memory_secret_independent": True,
            "hidden_normal_not_given_to_decoder": True,
            "known_log_workspace_must_be_uncomputed": True}


def run_controls():
    controls = [physical_control(q, m, s) for q, m in ((2, 3), (3, 3), (5, 3), (7, 2), (11, 2), (13, 2))
                for s in (1, singer_parameters(q, m)[0]//2)]
    scaling = []
    for bits in (8, 16, 32, 64, 128):
        row = access_ledger(1 << bits, 3)
        row["base_field_bits"] = bits
        row["coherent_error_budget"] = coherent_error_budget(int(row["max_total_membership_queries"]), Fraction(1, 1000))
        scaling.append(row)
    return {"status": "KNOWN_SHOR_ASSISTED_SINGER_QUERY_CLOSURE_LOCAL_REVIEW_PENDING",
            "physical_controls": controls, "growing_base_field_ledgers": scaling,
            "claim_gate": {"accepted_candidate": False, "novel_algorithm": False,
                           "actual_coherent_Shor_compiler_implemented": False,
                           "polynomial_input_time_for_unrestricted_q": False,
                           "full_classical_dequantization": False,
                           "generic_DHSP_query_lower_bound": False,
                           "independent_theorem_review": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = run_controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"report": str(args.output), "physical_controls": len(report["physical_controls"]),
                      "full_schedule_branches": sum(len(r["branches"]) for r in report["physical_controls"]),
                      "novel_algorithm": False, "actual_coherent_Shor_implemented": False}))


if __name__ == "__main__":
    main()
