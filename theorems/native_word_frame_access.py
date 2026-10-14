"""Actual original-data word frame, three access primitives and conditional receiver.

Dense controls are capped diagnostics. Normalized fibre access is NOT supplied
as a scalable circuit; all failure mass and original-data noise remain charged.
"""
from __future__ import annotations

import argparse
import hashlib
from itertools import product
import json
from pathlib import Path

from flint import fmpq
import numpy as np

from native_short_preimage_reduction import public_family
from native_known_seed_group_workbench import source_fixture
from native_noisy_phase_input import checked_source_bank
from known_preparation_coherent_reflection import checked_shape
from ternary_certified_noise_sampler import rational, sqrt_box
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_noise_degradation import NoisyLinearRecord

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT/"research/NATIVE_WORD_FRAME_ACCESS.md"
REPORT = ROOT/"research/reductions/native_word_frame_access.json"


def preparation_contract(records, mask, cohorts, sites):
    records, mask, q, n = checked_source_bank(records, mask)
    family = public_family(records, cohorts, sites)
    phases = []
    for b in range(cohorts):
        local = []
        for j in range(sites):
            rows = records[2*(b*sites+j):2*(b*sites+j)+2]
            y1, y2 = tuple((r.value+sum(a*m for a, m in zip(r.label, mask))) % q for r in rows)
            local.append((y1, (y2-y1) % q, -y2 % q))
        phases.append(tuple(local))
    return {"public_family": family.record(), "known_word_phases_by_cohort": tuple(phases),
            "original_records_paid_once": len(records), "cohort_controlled_local_diagonal_gates": cohorts*sites,
            "uniform_index_qubits": cohorts.bit_length()-1, "uniform_qutrits": sites,
            "word_domain_size": str(fmpq(cohorts*3**sites)), "frequency_group_size": str(fmpq(q**n)),
            "frequency_coordinate_trits": n*root_digits(q),
            "secret_or_errors_supplied_to_preparation": False,
            "same_as_previous_native_point_seed": False,
            "all_word_table_required_for_indexed_preparation": False,
            "normalized_fibre_oracle_supplied": False,
            "physical_gate_synthesis_and_precision_supplied": False}


def finite_frame(records, mask, cohorts, sites, cap=256):
    records, mask, q, n = checked_source_bank(records, mask)
    family = public_family(records, cohorts, sites)
    integer(cap, "positive bounded diagnostic matrix cap", 1)
    D, N = cohorts*3**sites, q**n
    if D > cap or N > cap or D*N > cap*cap:
        raise ValueError("dense word/frequency controls exceed finite cap; no scalable fibre access supplied")
    spec = preparation_contract(records, mask, cohorts, sites)
    freqs = tuple(product(range(q), repeat=n))
    index = {s: j for j, s in enumerate(freqs)}
    rows, eta, beta = [], [], []
    for b in range(cohorts):
        for word in product(range(3), repeat=sites):
            sigma = family.frequency(b, word)
            phase = sum(spec["known_word_phases_by_cohort"][b][j][t] for j, t in enumerate(word)) % q
            coefficients = [0]*len(records)
            for j, t in enumerate(word):
                i = 2*(b*sites+j)
                coefficients[i:i+2] = ((1, 0), (-1, 1), (0, -1))[t]
            rows.append({"cohort": b, "word": word, "frequency": sigma, "known_phase": phase})
            eta.append(index[sigma]); beta.append(tuple(coefficients))
    counts = np.bincount(eta, minlength=N)
    J, Q = np.zeros((N, D), dtype=complex), np.zeros((N, D), dtype=complex)
    for x, sigma in enumerate(eta):
        J[sigma, x] = 1/np.sqrt(D)
        Q[sigma, x] = 1/np.sqrt(counts[sigma])
    projector = Q.conj().T@Q
    fail = np.eye(D)-projector
    # This is a mathematical reference dilation, not a compiled quantum circuit.
    dilation = np.concatenate((Q, fail), axis=0)
    transform = np.exp(-2j*np.pi*(np.asarray(freqs)@np.asarray(freqs).T)/q)/np.sqrt(N)
    state = np.exp(2j*np.pi*np.asarray([r["known_phase"] for r in rows])/q)/np.sqrt(D)
    return {"family": family, "spec": spec, "frequencies": freqs, "rows": rows,
            "word_coefficients": beta, "counts": counts, "J": J, "Q": Q,
            "fibre_projector": projector, "failure": fail, "dilation": dilation,
            "group_inverse_Fourier": transform, "state": state}


def ideal_success_interval(counts, D, N, bits=96):
    counts = tuple(counts)
    integer(D, "positive actual word count", 1)
    integer(N, "positive actual frequency count", 1)
    integer(bits, "positive enclosure bits", 1)
    if len(counts) != N or any(type(c) is not int or c < 0 for c in counts) or sum(counts) != D:
        raise ValueError("complete actual fibre counts summing to word domain required")
    lo, hi = fmpq(0), fmpq(0)
    for c in counts:
        a, b = sqrt_box(c, bits)
        lo, hi = lo+a, hi+b
    return {"lower": str(lo*lo/(D*N)), "upper": str(min(fmpq(1), hi*hi/(D*N))),
            "enclosure_bits": bits, "source": "ACTUAL_COMPLETE_PUBLIC_FIBRE_COUNTS",
            "coverage_is_inferred_from_small_controls": False}


def word_error_second_moment(errors, cohorts, sites):
    errors = tuple(errors)
    integer(cohorts, "positive cohort count", 1)
    integer(sites, "positive site count", 1)
    if len(errors) != 2*cohorts*sites or any(type(e) is not int for e in errors):
        raise ValueError("complete unwrapped original integer errors required for truth-only audit")
    value = sum(a*a+b*b-a*b for a, b in zip(errors[::2], errors[1::2]))
    return fmpq(2*value, 3*cohorts)


def noise_ledger(sites, q, moment, bits=96):
    integer(sites, "positive source site count", 1)
    root_digits(q)
    V = rational(moment, "true marginal original integer second-moment upper bound")
    if V < 0: raise ValueError("nonnegative true marginal second moment required")
    delta2 = min(fmpq(1), 80*sites*V/(q*q))
    lo, hi = sqrt_box(delta2, bits)
    return {"modulus": str(q), "sites": sites, "true_marginal_original_second_moment_upper": str(V),
            "mean_pure_trace_distance_squared_upper": str(delta2),
            "mean_unconditional_measurement_loss_bound_lower_enclosure": str(lo),
            "mean_unconditional_measurement_loss_upper": str(min(fmpq(1), hi)),
            "enclosure_bits": bits, "original_independence_or_zero_mean_required": False,
            "errors_independent_of_public_labels_required": False,
            "fresh_original_errors_per_word_required": False,
            "bound_is_on_complete_good_and_failure_measurement": True,
            "ideal_fibre_coverage_or_success_proved_by_moments": False,
            "generic_physical_gate_errors_included": False,
            "efficient_normalized_fibre_circuit_supplied": False,
            "accepted_speedup_candidate": False}


def finite_control(n, r, B, M, noisy, seed):
    recipe, truth, errors = source_fixture(n, r, B, M, noisy, seed)
    src = recipe["source_receipts"]
    records = tuple(NoisyLinearRecord(tuple(row["label"]), row["value"], row["modulus"], row["source_id"])
                    for row in src["original_classical_records"])
    mask = tuple(src["preparation_random_mask"])
    F = finite_frame(records, mask, B, M)
    J, Q, psi, counts, Fourier = (F[k] for k in ("J", "Q", "state", "counts", "group_inverse_Fourier"))
    q, D, N = 3**r, J.shape[1], J.shape[0]
    p = counts/D
    ideal = np.exp(2j*np.pi*np.asarray([sum(a*s for a, s in zip(row["frequency"], truth)) % q for row in F["rows"]])/q)/np.sqrt(D)
    good, discarded, comparison = Fourier@(Q@psi), F["failure"]@psi, Fourier@(J@psi)
    ideal_good = Fourier@(Q@ideal)
    target = F["frequencies"].index(tuple(truth))
    polar_residual = np.max(np.abs(J-np.sqrt(p)[:, None]*Q))
    complete_residual = np.max(np.abs(F["dilation"].conj().T@F["dilation"]-np.eye(D)))
    fourier_residual = np.max(np.abs(Fourier.conj().T@Fourier-np.eye(N)))
    ideal_success = abs(ideal_good[target])**2
    ideal_bound = ideal_success_interval(tuple(int(c) for c in counts), D, N)
    trace2 = max(0., 1-abs(np.vdot(ideal, psi))**2)
    error_moment = word_error_second_moment(errors, B, M)
    angle_trace2_upper = min(fmpq(1), 40*error_moment/(q*q))
    # The discarded forward pointer kills ALL off-diagonal frequency coherence.
    discarded_pointer = Fourier@np.diag(p)@Fourier.conj().T
    total_mass = float(np.sum(abs(good)**2)+np.vdot(discarded, discarded).real)
    actual_success = float(abs(good[target])**2)
    if max(polar_residual, complete_residual, fourier_residual, abs(total_mass-1)) > 1e-10:
        raise ArithmeticError("finite frame/reference dilation failed normalization")
    if abs(actual_success-ideal_success) > np.sqrt(trace2)+1e-10 or trace2 > float(angle_trace2_upper)+1e-10:
        raise ArithmeticError("complete receiver or pathwise source-noise contraction check failed")
    return {"original_records": tuple(row.public() for row in records), "known_mask": mask,
            "preparation_contract": F["spec"], "word_rows": F["rows"], "frequency_order": F["frequencies"],
            "fibre_counts": tuple(int(c) for c in counts),
            "truth_fixture_only": {"masked_secret": truth, "original_errors": errors},
            "public_singular_values_squared_exact": tuple(str(fmpq(int(c), D)) for c in counts),
            "supported_condition_number_squared_exact": str(fmpq(int(max(counts)), int(min(c for c in counts if c)))),
            "ideal_clean_receiver_success_interval": ideal_bound,
            "reference_good_outcome_probabilities": tuple(float(abs(x)**2) for x in good),
            "reference_good_mass": float(np.sum(abs(good)**2)),
            "reference_failure_mass": float(np.vdot(discarded, discarded).real),
            "reference_correct_and_good_probability": actual_success,
            "reference_ideal_correct_probability": float(ideal_success),
            "comparison_good_mass": float(np.sum(abs(comparison)**2)),
            "comparison_correct_and_good_probability": float(abs(comparison[target])**2),
            "ideal_comparison_good_mass_exact": str(sum((fmpq(int(c*c), D*D) for c in counts), fmpq(0))),
            "ideal_comparison_correct_and_good_exact": str(fmpq(1, N)),
            "pointer_discarded_Fourier_probabilities": tuple(float(x.real) for x in np.diag(discarded_pointer)),
            "pure_source_trace_distance_squared": float(trace2),
            "word_error_mean_square_exact": str(error_moment),
            "pathwise_trace_distance_squared_rational_upper": str(angle_trace2_upper),
            "maximum_diagnostic_matrix_residual": float(max(polar_residual, complete_residual, fourier_residual)),
            "dense_control_is_exponential_calibration": True,
            "finite_float_laws_are_exact_certificates": False,
            "normalized_row_oracle_is_supplied_at_polynomial_cost": False,
            "new_speedup_claim": False}


def balanced_scale(n, r, surplus_sites=24):
    integer(n, "positive original dimension", 1)
    integer(r, "positive root exponent", 1)
    integer(surplus_sites, "nonnegative word-domain trit surplus")
    N, D = 3**(n*r), 3**(n*r+surplus_sites)
    return {"dimension": n, "root_digits": r, "word_domain_size": str(fmpq(D)), "frequency_group_size": str(fmpq(N)),
            "hypothetical_exact_balanced_fibre_size": str(fmpq(D//N)),
            "comparison_singular_value_squared": str(fmpq(1, N)),
            "supported_condition_number_squared": "1", "ideal_clean_receiver_success": "1",
            "raw_comparison_correct_and_good_probability": str(fmpq(1, N)),
            "normalization_multiplier_squared": str(fmpq(N)),
            "actual_random_native_family_is_proved_balanced": False,
            "this_is_a_symbolic_access_countercontrol_not_generated_source": True,
            "polynomial_clean_row_implementation_supplied": False,
            "all_decoders_have_this_normalization_cost": False}


def random_label_receiver_ledger(n, r, cohorts, sites, moment, bits=96):
    """Population expectation, not per-instance balance or an efficient row circuit."""
    integer(n, "positive original dimension", 1)
    integer(r, "positive root exponent", 1)
    q = 3**r
    # Reuse the actual native source shape checks without materializing records.
    checked_shape(cohorts, sites)
    N, D = q**n, cohorts*3**sites
    ideal_failure = min(fmpq(1), fmpq(N-1, D))
    noise = noise_ledger(sites, q, moment, bits)
    loss = fmpq(noise["mean_unconditional_measurement_loss_upper"])
    return {"dimension": n, "root_digits": r, "cohorts": cohorts, "sites": sites,
            "frequency_group_size": str(fmpq(N)), "word_domain_size": str(fmpq(D)),
            "ideal_ensemble_receiver_failure_upper": str(ideal_failure),
            "ideal_ensemble_receiver_success_lower": str(1-ideal_failure),
            "noisy_complete_ensemble_receiver_success_lower": str(max(fmpq(0), 1-ideal_failure-loss)),
            "noise": noise,
            "IID_uniform_original_public_labels_for_each_fixed_secret_required": True,
            "original_errors_independent_of_labels_required": False,
            "source_population_promises_established_by_small_artifacts": False,
            "per_dataset_success_or_exact_balance_guaranteed": False,
            "bound_is_unconditional_over_original_dataset_and_complete_receiver": True,
            "normalized_fibre_circuit_is_an_explicit_missing_assumption": True,
            "efficient_receiver_constructed": False, "accepted_speedup_candidate": False}


def build_report():
    controls = [finite_control(*p) for p in ((1, 1, 1, 3, False, 88001), (1, 2, 1, 4, False, 88002),
                                            (2, 2, 1, 4, True, 88003), (1, 2, 2, 3, True, 88004))]
    scales = []
    for n in (8, 32, 64, 128):
        q, M = 3**n, n*n+24
        V = fmpq(q*q, 3*n**6)+fmpq(1, 2)
        scales.append({"dimension": n, "noise": noise_ledger(M, q, V),
                       "random_label_reference": random_label_receiver_ledger(n, n, 1, M, V),
                       "hypothetical_balanced_access": balanced_scale(n, n)})
    dependencies = ("native_short_preimage_reduction.py", "native_known_seed_group_workbench.py", "native_noisy_phase_input.py",
                    "ternary_certified_noise_sampler.py", "ternary_covariant_noise.py", "ternary_measured_lattice_decoder.py", "ternary_noise_degradation.py",
                    "known_preparation_coherent_reflection.py")
    return {"status": "NATIVE_WORD_FRAME_ROW_ACCESS_AND_NOISE_CONTRACT_EXTERNAL_REVIEW_PENDING",
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "dependency_sha256": {f: hashlib.sha256((ROOT/"theorems"/f).read_bytes()).hexdigest() for f in dependencies},
            "bounded_reference_controls": controls, "scalable_conditional_access_ledgers": scales,
            "literature_background": [{"id": "BCVD-2005-DIHEDRAL-PGM", "url": "https://arxiv.org/abs/quant-ph/0501044",
                                        "scope": "known optimal-measurement/subset-sum-sampling connection; not a theorem for this noisy native source"}],
            "research_decision": "SEARCH_FOR_ACTUAL_NORMALIZED_ROW_IMPLEMENTATION_NOT_FREE_FORWARD_COMPUTATION_OR_POSTSELECTION",
            "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
            "efficient_normalized_fibre_circuit_supplied": False, "general_quantum_decoder_lower_bound_proved": False,
            "remaining_obligations": ["external proof review", "constructive coherent normalized-fibre access and retained-garbage circuit",
                                      "actual random-label fibre coverage, runtime and original-data classical comparison",
                                      "physical gate synthesis and complete precision budget", "production admission wiring"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "controls": [{"good": c["reference_good_mass"],
                     "failure": c["reference_failure_mass"], "correct_and_good": c["reference_correct_and_good_probability"]}
                     for c in report["bounded_reference_controls"]], "accepted_speedup_candidate": False}, indent=2))


if __name__ == "__main__": main()
