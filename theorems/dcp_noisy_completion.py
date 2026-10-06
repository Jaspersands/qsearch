"""Noisy known-residue completion, promise-transfer gates and candidate tests.

LOCAL DERIVATION / REVIEW PENDING. Classicalization of a commuting input
experiment is not a classical polynomial-time LPN solver or a full DCP decoder.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

from dcp_bell_inference_kernel import exact

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_noisy_completion.json"


def _probability(value):
    value = Fraction(value)
    if not 0 <= value <= 1:
        raise ValueError("probability must lie in [0,1]")
    return value


def phase_flip_binary_density(parity, flip_probability):
    if parity not in (0, 1):
        raise ValueError("binary parity required")
    e = _probability(flip_probability)
    off = (-1 if parity else 1) * (1 - 2 * e) / 2
    return ((Fraction(1, 2), off), (off, Fraction(1, 2)))


def basis_contamination_binary_density(parity, bad_probability, bad_basis_bit):
    if parity not in (0, 1) or bad_basis_bit not in (0, 1):
        raise ValueError("binary parity and bad basis bit required")
    gamma = _probability(bad_probability)
    off = (-1 if parity else 1) * (1 - gamma) / 2
    return (((1 - gamma) / 2 + (gamma if bad_basis_bit == 0 else 0), off),
            (off, (1 - gamma) / 2 + (gamma if bad_basis_bit == 1 else 0)))


def _multiply(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def commutator_squared_norm(a, b):
    ab, ba = _multiply(a, b), _multiply(b, a)
    return sum((ab[i][j] - ba[i][j])**2 for i in range(2) for j in range(2))


def _x_twirl(rho):
    return tuple(tuple((rho[i][j] + rho[1 - i][1 - j]) / 2 for j in range(2)) for i in range(2))


def noise_promise_gate(model, capability, *, independent_registers=False,
                       uniform_native_labels=False, independent_of_higher_labels=False,
                       independent_of_secret=False, correct_residue_known=False,
                       public_constant_basis_bias_known=False):
    models = {"iid_physical_Z", "classical_correlated_Z", "balanced_basis_contamination",
              "arbitrary_basis_contamination", "known_biased_basis_contamination", "unknown_corruption"}
    capabilities = {"native_iid_phase_moment", "lossless_binary_classicalization", "iid_lpn_completion",
                    "heralded_binary_classicalization"}
    if model not in models or capability not in capabilities:
        raise ValueError("unknown noise promise or transfer capability")
    issues = []
    if capability == "native_iid_phase_moment":
        if model != "iid_physical_Z":
            issues.append("native weighted moment requires IID physical Z phase errors, not basis-state failures or correlated masks")
        if not independent_registers:
            issues.append("independent physical/register error law is not established")
        if not independent_of_higher_labels:
            issues.append("higher-label/noise independence is not established; character averaging cannot be reused")
        if not independent_of_secret:
            issues.append("secret-independent error source is not established")
        if not uniform_native_labels:
            issues.append("native uniform source law is not established")
    else:
        if not correct_residue_known:
            issues.append("known CORRECT s mod(q/2) is required before binary classicalization")
        if capability == "heralded_binary_classicalization":
            if model != "known_biased_basis_contamination" or not public_constant_basis_bias_known:
                issues.append("heralded filter requires a public constant basis bias and known bad basis bit")
        elif model not in {"iid_physical_Z", "classical_correlated_Z", "balanced_basis_contamination"}:
            issues.append("arbitrary basis contamination need not commute; X-basis measurement is not lossless")
        if capability == "iid_lpn_completion":
            if model == "classical_correlated_Z" or not independent_registers:
                issues.append("IID LPN labels cannot be inferred from correlated register corruption")
            if not uniform_native_labels or not independent_of_higher_labels or not independent_of_secret:
                issues.append("uniform label-independent noise source needed for standard IID LPN")
    return {"status": "CONDITIONAL_PROMISE_GATE_NOT_PROVEN_SOURCE_REDUCTION", "model": model,
            "requested_capability": capability, "transfer_obligations_satisfied_as_declared": not issues,
            "issues": issues, "declarations_programmatically_proven": False,
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def known_basis_bias_filter(bad_probability, bad_basis_bit):
    gamma = _probability(bad_probability)
    if gamma == 1 or bad_basis_bit not in (0, 1):
        raise ValueError("contamination<1 and public binary bad basis bit required")
    a2 = (1 - gamma) / (1 + gamma)
    return {"status": "PUBLIC_BIAS_HERALDED_SAMPLE_CONVERSION_NOT_LOSSLESS_ONE_COPY",
            "basis_contamination_probability": exact(gamma), "public_bad_basis_bit": bad_basis_bit,
            "success_filter": "attenuate_the_bad_basis_amplitude_by_sqrt((1-gamma)/(1+gamma))",
            "attenuation_squared": exact(a2), "success_probability": exact(1 - gamma),
            "conditional_binary_contrast_squared": exact(a2),
            "conditional_lpn_flip_rate_expression": "(1-sqrt((1-gamma)/(1+gamma)))/2",
            "reverse_from_unerased_lpn_sample": "prepare_sqrt((1+gamma)/2)_ket_bad_plus_sign_y_sqrt((1-gamma)/2)_ket_other",
            "reverse_preparation_sign_depends_on_classical_y_not_secret": True,
            "failure_branch_has_no_binary_secret_information": True,
            "expected_native_inputs_per_output": exact(Fraction(1, 1 - gamma)),
            "uniform_source_preserved_requires_constant_gamma_and_public_bad_bit": True,
            "arbitrary_hidden_or_label_dependent_basis_bias_covered": False,
            "known_correct_residue_required": True,
            "one_copy_lossless_equivalence_claim": False,
            "physical_filter_backend_or_precision_verified": False,
            "classical_lpn_solver_or_unknown_residue_decoder_provided": False,
            "speedup_claim_allowed": False}


def known_residue_classicalization_certificate(n, flip_probability):
    if n < 1:
        raise ValueError("positive vector dimension required")
    e = _probability(flip_probability)
    for parity in (0, 1):
        rho = phase_flip_binary_density(parity, e)
        # LPN outcome y=parity+E can recreate the density via H|y>.
        recreated = tuple(tuple((1 - e) * phase_flip_binary_density(parity, 0)[i][j]
                                + e * phase_flip_binary_density(parity ^ 1, 0)[i][j]
                                for j in range(2)) for i in range(2))
        assert rho == recreated
    assert commutator_squared_norm(phase_flip_binary_density(0, e), phase_flip_binary_density(1, e)) == 0
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "dimension": n,
            "physical_phase_flip_probability": exact(e),
            "requires_correct_known_lower_residue_and_fresh_original_phase_states": True,
            "classical_sample_law": "a_uniform_F2n_y_equals_a_dot_high_bit_secret_xor_Bernoulli_e",
            "measure_H_then_Z_is_lossless_for_declared_binary_experiment": True,
            "reverse_channel": "given_classical_a_y_prepare_H_ket_y_and_preserve_a",
            "coherent_label_or_example_oracle_granted": False,
            "quantum_computation_on_classical_lpn_data_ruled_out": False,
            "classical_polynomial_time_lpn_decoder_provided": False,
            "arbitrary_basis_contamination_covered": False,
            "incorrect_residue_or_nonphase_channels_covered": False,
            "independent_theorem_review": False, "speedup_claim_allowed": False}


def low_noise_clean_block_baseline(n, flip_probability, rank_failure_exponent=40):
    if n < 1 or rank_failure_exponent < 1:
        raise ValueError("positive dimension and rank-failure exponent required")
    e = _probability(flip_probability)
    M = n + rank_failure_exponent
    rank_failure = Fraction((1 << n) - 1, 1 << M)
    iid_clean = (1 - e)**M
    iid_success = iid_clean * (1 - rank_failure)
    marginal_success = max(Fraction(0), 1 - M * e - rank_failure)
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "dimension": n,
            "fresh_original_phase_states_per_trial": M, "effective_parity_flip_probability": exact(e),
            "random_binary_rank_failure_upper_bound": exact(rank_failure),
            "iid_label_independent_clean_block_probability": exact(iid_clean),
            "iid_clean_block_correct_completion_success_lower_bound": exact(iid_success),
            "marginal_flip_bound_only_correct_completion_success_lower_bound": exact(marginal_success),
            "marginal_bound_does_not_require_noise_label_independence": True,
            "uniform_native_label_rank_law_still_required": True,
            "requires_known_correct_lower_residue": True,
            "classical_solver": "binary_elimination_then_fresh_full_candidate_verification",
            "wrong_or_inconsistent_blocks_not_accepted_without_verification": True,
            "noisy_constant_rate_polynomial_decoder_claim": False,
            "speedup_claim_allowed": False}


def _binomial_tail(M, probability, lower, upper):
    return sum(Fraction(math.comb(M, j)) * probability**j * (1 - probability)**(M - j)
               for j in range(lower, upper + 1))


def robust_full_candidate_verification(M, conditional_bad_probability_bound):
    """Uniform fresh native labels, fixed FULL candidate, arbitrary bad states."""
    gamma = _probability(conditional_bad_probability_bound)
    if M < 1 or gamma >= Fraction(1, 4):
        raise ValueError("positive test count and conditional bad probability<1/4 required")
    # Accept iff at least ceil(3M/4) known-candidate projections return zero.
    threshold = (3 * M + 3) // 4
    correct_lower, wrong_upper = 1 - gamma, Fraction(1, 2) + gamma
    false_reject = _binomial_tail(M, correct_lower, 0, threshold - 1)
    false_accept = _binomial_tail(M, wrong_upper, threshold, M)
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "fresh_original_phase_states_consumed": M,
            "per_trial_conditional_arbitrary_bad_probability_bound": exact(gamma),
            "projection_zero_votes_required": threshold,
            "correct_full_candidate_per_trial_acceptance_lower_bound": exact(correct_lower),
            "incorrect_full_candidate_per_trial_acceptance_upper_bound": exact(wrong_upper),
            "false_rejection_probability_upper_bound": exact(false_reject),
            "false_acceptance_probability_upper_bound": exact(false_accept),
            "candidate_committed_before_verification_source_labels": True,
            "fresh_native_labels_uniform_conditioned_on_past_required": True,
            "bad_state_can_depend_on_secret_label_and_history": True,
            "conditional_bad_probability_bound_not_just_unconditional_marginals_required": True,
            "conditional_bad_bound_required_for_each_fixed_secret_and_history": True,
            "bad_states_can_be_arbitrary_not_only_Z_flips": True,
            "known_public_candidate_phase_correction_not_unknown_inverse": True,
            "ideal_gates_measurement_precision_and_noise_not_charged_here": True,
            "lower_residue_alone_is_not_a_full_candidate": True,
            "conditional_source_promise_programmatically_verified": False,
            "decoder_provided": False, "speedup_claim_allowed": False}


def _density_controls():
    rows = []
    for gamma in (Fraction(0), Fraction(1, 128), Fraction(1, 8), Fraction(1, 2)):
        for bad in (0, 1):
            plus = basis_contamination_binary_density(0, gamma, bad)
            minus = basis_contamination_binary_density(1, gamma, bad)
            norm = commutator_squared_norm(plus, minus)
            assert norm == 2 * gamma**2 * (1 - gamma)**2
            for parity in (0, 1):
                assert _x_twirl(basis_contamination_binary_density(parity, gamma, bad)) == phase_flip_binary_density(parity, gamma / 2)
            rows.append({"basis_contamination_probability": exact(gamma), "bad_basis_bit": bad,
                         "commutator_frobenius_squared": exact(norm),
                         "X_twirl_is_legal_degradation_to_flip_rate": exact(gamma / 2),
                         "X_twirl_is_lossless": norm == 0,
                         "full_basis_contamination_has_not_been_dequantized": True})
    return rows


def run_controls():
    declaration = {"independent_registers": True, "uniform_native_labels": True,
                   "independent_of_higher_labels": True, "independent_of_secret": True,
                   "correct_residue_known": True}
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "basis_contamination_commutators": _density_controls(),
            "noise_transfer_gates": [noise_promise_gate(model, capability, **declaration)
                                     for model in ("iid_physical_Z", "classical_correlated_Z", "arbitrary_basis_contamination")
                                     for capability in ("native_iid_phase_moment", "lossless_binary_classicalization", "iid_lpn_completion")],
            "binary_experiment_classicalization": known_residue_classicalization_certificate(128, Fraction(1, 32)),
            "known_public_basis_bias_filters": [known_basis_bias_filter(gamma, bad)
                                                for gamma in (Fraction(1, 128), Fraction(1, 8)) for bad in (0, 1)],
            "low_noise_completion_scaling": [low_noise_clean_block_baseline(n, Fraction(1, n * n)) for n in (8, 16, 32, 64, 128)],
            "constant_noise_completion_control": low_noise_clean_block_baseline(128, Fraction(1, 8)),
            "robust_full_candidate_verifier": robust_full_candidate_verification(256, Fraction(1, 16)),
            "claim_gate": {"iid_phase_noise_and_regev_basis_failure_are_distinct": True,
                           "known_correct_residue_phase_noise_is_a_classical_lpn_experiment": True,
                           "arbitrary_basis_noise_losslessly_classicalized": False,
                           "quantum_lpn_example_oracle_available": False,
                           "low_noise_clean_blocks_cover_all_lpn_parameters": False,
                           "native_reduction_conditional_failure_promise_verified": False,
                           "unknown_residue_decoder": False, "independent_theorem_review": False,
                           "speedup_claim_allowed": False},
            "dependency_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (Path(__file__), ROOT / "theorems/dcp_bell_inference_kernel.py")}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"status": report["status"], "claim_gate": report["claim_gate"]}, indent=2))


if __name__ == "__main__":
    main()
