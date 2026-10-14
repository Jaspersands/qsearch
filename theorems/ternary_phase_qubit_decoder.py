"""Copy-only F3 phase-qubit base decoder with actual anti-trine readout.

Known fixed-exponent hidden-translation baseline, not a Shor-level discovery.
The source is the terminal character subgroup of supplied generalized-dihedral
phase states. No oracle values, hidden secret, or state inverse enter decoding.
"""
from __future__ import annotations

import argparse
import hashlib
from itertools import product
import json
from pathlib import Path
import random

from flint import fmpq, nmod_mat
import numpy as np

from native_generalized_dihedral_bridge import BinaryPhaseSample, extract_binary_source, extraction_budget
from native_uniform_descent_receiver import OriginalSource, SourceExhausted, forward_fixture
from nil3_state_hsp_descent_receiver import solve_full_rank_f3
from ternary_measured_lattice_decoder import exact_json, integer

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT/"research/TERNARY_PHASE_QUBIT_DECODER.md"
REPORT = ROOT/"research/reductions/ternary_phase_qubit_decoder.json"


def symmetric_basis(dimension):
    integer(dimension, "positive ternary dimension", 1)
    return tuple((i, j) for i in range(dimension) for j in range(i, dimension))


def quadratic_equation(row, excluded_value):
    row = tuple(row)
    if not row or any(type(k) is not int or k not in (0, 1, 2) for k in row) or type(excluded_value) is not int or excluded_value not in (0, 1, 2):
        raise ValueError("canonical F3 character row and actual excluded value required")
    coefficients = tuple(((1 if i == j else 2)*row[i]*row[j]) % 3 for i, j in symmetric_basis(len(row)))
    coefficients += tuple(excluded_value*k % 3 for k in row)
    return coefficients, (1-excluded_value**2) % 3


def terminal_character_row(sample):
    if not isinstance(sample, BinaryPhaseSample):
        raise ValueError("actual supplied binary phase sample required")
    axes, row = [], []
    for j, (k, m) in enumerate(zip(sample.dual_label, sample.cyclic_orders)):
        if m == 1:
            continue
        exponent, rest = 0, m
        while rest % 3 == 0:
            exponent, rest = exponent+1, rest//3
        if rest != 1 or exponent < 1 or k % (m//3):
            raise ValueError("sample label must lie in the actual order3 character subgroup")
        axes.append(j)
        row.append(k//(m//3))
    if not axes:
        raise ValueError("nontrivial ternary character coordinates required")
    return tuple(row), tuple(axes)


def measurement_isometry():
    b = np.arange(3)
    return np.column_stack((np.ones(3), -np.exp(-2j*np.pi*b/3)))/np.sqrt(3)


def anti_trine_measure(sample, rng):
    row, axes = terminal_character_row(sample)
    V = measurement_isometry()
    probabilities = np.diag(V@sample.state@V.conj().T).real
    if min(probabilities) < -1e-12 or abs(sum(probabilities)-1) > 1e-12:
        raise ArithmeticError("supplied density violated the known POVM instrument")
    probabilities = np.maximum(probabilities, 0)
    probabilities /= sum(probabilities)
    outcome = int(rng.choice(3, p=probabilities))
    return row, outcome, {"public_dual_label": sample.dual_label, "cyclic_orders": sample.cyclic_orders,
                          "active_phase_axes": axes, "ternary_character_row": row, "excluded_value_observed": outcome,
                          "actual_probabilities": tuple(map(float, probabilities)), "original_indices": sample.original_indices,
                          "supplied_binary_density": [[[float(z.real), float(z.imag)] for z in r] for r in sample.state],
                          "measurement_uses_hidden_secret": False, "unknown_source_inverse_used": False}


class FiniteBinarySource:
    """Each supplied physical packet can enter the measurement stream once."""

    def __init__(self, samples, cap):
        integer(cap, "positive supplied binary copy cap", 1)
        self.inputs, self.cap, self.count, self.original_ids = iter(samples), cap, 0, set()

    def take(self):
        if self.count == self.cap:
            raise SourceExhausted("paid binary sample budget exhausted")
        try:
            sample = next(self.inputs)
        except StopIteration as error:
            raise SourceExhausted("finite supplied binary source exhausted") from error
        if not isinstance(sample, BinaryPhaseSample) or self.original_ids.intersection(sample.original_indices):
            raise ValueError("distinct original physical phase packets required, no cloning")
        self.original_ids.update(sample.original_indices)
        self.count += 1
        return sample


def decoder_budget(dimension, failure_bits=8):
    pairs = symmetric_basis(dimension)
    integer(failure_bits, "positive failure bits", 1)
    D = len(pairs)+dimension
    M = 3*D+2*failure_bits
    return {"dimension": dimension, "symmetric_monomial_basis": pairs, "lifted_unknown_dimension": D,
            "binary_copy_cap": M, "failure_bits": failure_bits,
            "exact_rank_failure_upper_compact": {"projective_hyperplanes": {"base": 3, "exponent": D, "subtract": 1, "denominator": 2},
                                                "single_hyperplane_capture_probability": "2/3", "sample_count": M},
            "simpler_rank_failure_upper": str(fmpq(1, 2**(failure_bits+1))),
            "naive_classical_field_operation_upper_order": "O(M*D^2)=O(d^6+d^4*b)",
            "classical_matrix_storage_upper_order": "O(M*D)",
            "source_IID_label_promise_proved_from_data": False,
            "noise_and_hardware_errors_included": False, "oracle_value_access_required": False}


def receive(source, dimension, rng, failure_bits=8):
    budget = decoder_budget(dimension, failure_bits)
    if source.count or source.cap < budget["binary_copy_cap"]:
        raise ValueError("fresh finite source with the complete paid decoder cap required")
    records, rows, rhs, error = [], [], [], None
    group = None
    for _ in range(budget["binary_copy_cap"]):
        try:
            sample = source.take()
        except SourceExhausted as exhausted:
            error = str(exhausted)
            break
        row, outcome, record = anti_trine_measure(sample, rng)
        if len(row) != dimension or (group is not None and group != (sample.cyclic_orders, record["active_phase_axes"])):
            raise ValueError("one declared terminal ternary source group required")
        group = sample.cyclic_orders, record["active_phase_axes"]
        equation, value = quadratic_equation(row, outcome)
        rows.append(equation)
        rhs.append(value)
        records.append(record)
    rank = nmod_mat(rows, 3).rank() if rows else 0
    status, lifted, secret = "NO_COMPLETE_FINITE_SAMPLE_BATCH", None, None
    if error is None:
        try:
            lifted = solve_full_rank_f3(rows, rhs, budget["lifted_unknown_dimension"])
        except ValueError as inconsistent:
            if str(inconsistent) != "inconsistent F3 equations":
                raise
            status = "INCONSISTENT_EXCLUSION_EQUATIONS"
        else:
            status = "INSUFFICIENT_INDEPENDENT_QUADRATIC_ROWS" if lifted is None else "INVALID_RANK_ONE_LIFT"
            if lifted is not None:
                proposed = lifted[-dimension:]
                if lifted[:-dimension] == tuple(proposed[i]*proposed[j] % 3 for i, j in symmetric_basis(dimension)):
                    secret, status = proposed, "IDEAL_TERMINAL_TERNARY_SECRET_DECODED"
    return {"status": status, "recovered_ternary_secret": secret, "lifted_solution": lifted,
            "budget": budget, "consumed_binary_inputs": source.count,
            "consumed_original_ancestors": len(source.original_ids), "original_indices": tuple(sorted(source.original_ids)),
            "source_exhaustion": error, "coefficient_rank": rank, "measurement_records": records,
            "receiver_takes_hidden_secret": False, "classical_hypotheses_enumerated": False,
            "quantum_hardware_executed": False, "noisy_error_correcting_decoder_supplied": False,
            "source_promises_verified_by_receiver": False,
            "decoding_correctness_is_conditional_on_common_ideal_phase_source": True,
            "growing_depth_hidden_shift_solved": False, "new_quantum_speedup_established": False}


def strict_decoder_noise_contract(dimension, visibility, failure_bits=8):
    visibility = fmpq(visibility)
    if not 0 <= visibility <= 1:
        raise ValueError("visibility promise must lie in[0,1]")
    budget = decoder_budget(dimension, failure_bits)
    M = budget["binary_copy_cap"]
    permitted = (2+visibility)/3
    no_bad = permitted**M
    rank_error = fmpq(budget["simpler_rank_failure_upper"])
    return {"dimension": dimension, "binary_copy_cap": M, "uniform_input_visibility": str(visibility),
            "forbidden_outcome_probability_exact": str((1-visibility)/3),
            "no_forbidden_outcomes_probability_exact": str(no_bad),
            "this_strict_decoder_correct_recovery_upper": str(no_bad),
            "this_strict_decoder_correct_recovery_lower": str(no_bad*(1-rank_error)),
            "scope": "independent equal-visibility phase dephasing, IID uniform terminal character rows, fixed sample count",
            "robust_error_correction_implemented": False, "all_quantum_receivers_excluded": False}


def source_control(dimension, seed, zero_secret=False, visibility="1"):
    rng = random.Random(seed)
    truth = tuple(0 if zero_secret else rng.randrange(3) for _ in range(dimension))
    budget = decoder_budget(dimension)
    M = budget["binary_copy_cap"]
    extraction = extraction_budget(M, 8)
    original = OriginalSource(forward_fixture(1, tuple((x, 0) for x in truth), seed+1), 1, dimension, extraction["original_copy_cap"], retain_trace=True)
    samples, projection = extract_binary_source(original, M, np.random.default_rng(seed+2), 8)
    gamma = float(fmpq(visibility))
    samples = tuple(BinaryPhaseSample(s.dual_label, s.cyclic_orders, gamma*s.state+(1-gamma)*np.eye(2)/2, s.original_indices) for s in samples)
    result = receive(FiniteBinarySource(samples, M), dimension, np.random.default_rng(seed+3))
    if visibility == "1" and result["recovered_ternary_secret"] != truth:
        raise ArithmeticError("committed ideal terminal native-source control failed")
    return {"dimension": dimension, "truth_fixture_only": truth, "zero_secret_fixture": zero_secret,
            "visibility_after_original_projection": visibility, "original_projection": projection, "decoder": result,
            "forbidden_outcomes_fixture_only": sum(r["excluded_value_observed"] == sum(k*s for k, s in zip(r["ternary_character_row"], truth)) % 3 for r in result["measurement_records"]),
            "known_native_qutrit_F3_readout_is_a_stronger_baseline_on_this_calibration_source": True}


def dual_polynomial_census():
    n, basis = 2, symmetric_basis(2)
    D = len(basis)+n
    secrets = tuple(product(range(3), repeat=n))
    # Exhaust all nonzero dual polynomials, not just random solver examples.
    counts = []
    for secret in secrets:
        nonzero_counts = []
        for dual in product(range(3), repeat=D):
            if not any(dual):
                continue
            nonzero = 0
            for k in product(range(3), repeat=n):
                j = sum(a*s for a, s in zip(k, secret)) % 3
                for b in range(3):
                    if b != j:
                        row, _ = quadratic_equation(k, b)
                        nonzero += sum(a*x for a, x in zip(dual, row)) % 3 != 0
            nonzero_counts.append(nonzero)
        if min(nonzero_counts) < 6:
            raise ArithmeticError("claimed one-third dual-polynomial escape probability failed")
        counts.append({"secret_fixture": secret, "dual_polynomials_tested": 3**D-1,
                       "source_row_outcomes": 18, "nonzero_count_histogram": {str(c): nonzero_counts.count(c) for c in sorted(set(nonzero_counts))},
                       "minimum_nonzero_count": min(nonzero_counts)})
    return counts


def build_report():
    controls = [source_control(n, 15000+n) for n in (1, 2, 4, 8, 16)]
    controls.append(source_control(4, 15040, zero_secret=True))
    noisy = [source_control(4, 15100, visibility=v) for v in ("9/10", "0")]
    return {"status": "COPY_ONLY_TERMINAL_TERNARY_PHASE_DECODER_REVIEW_PENDING",
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT/"theorems"/name).read_bytes()).hexdigest()
                                  for name in ("native_generalized_dihedral_bridge.py", "nil3_state_hsp_descent_receiver.py", "native_uniform_descent_receiver.py")},
            "measurement_recipe": "embed qubit in qutrit basis0,1; diag(1,-1,1); inverse_F3; measure excluded value",
            "ideal_original_source_controls": controls, "noisy_original_source_countercontrols": noisy,
            "complete_dual_polynomial_censuses_dimension2": dual_polynomial_census(),
            "scaling_budgets": [decoder_budget(d) for d in (8, 16, 32, 64, 128, 256)],
            "strict_decoder_noise_contracts": [strict_decoder_noise_contract(d, v) for d in (2, 4, 8, 16) for v in ("1", "99/100", "9/10", "0")],
            "known_fixed_exponent_baseline": "https://arxiv.org/abs/quant-ph/0211091",
            "growing_depth_receiver_supplied": False, "noisy_error_correcting_decoder_supplied": False,
            "algorithmic_novelty_verified": False, "accepted_speedup_candidate": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "ideal_source_recoveries": len(report["ideal_original_source_controls"]),
                      "noise_countercontrol_statuses": [c["decoder"]["status"] for c in report["noisy_original_source_countercontrols"]],
                      "complete_dual_polynomial_censuses": 9, "classical_secret_enumeration_used": False,
                      "new_quantum_speedup_established": False}, indent=2))


if __name__ == "__main__":
    main()
