"""Physical CNOT merge audit under the real lattice-to-DCP bad-register promise.

Compact density parameters are private audit data, not chosen-phase access.
Balanced legal contamination is enough to test a claimed full-family solver.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import json
from math import isqrt
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "core") not in sys.path:
    sys.path.insert(0, str(ROOT / "core"))

from dcp_sample_workbench import dcp_state_access_contract
from dcp_carry_packets import compile_packet
from dcp_physical_phase_noise import IndependentPhysicalZ
from native_basis_lottery import power_box
from native_small_multiple_completion import _rational
from ternary_measured_lattice_decoder import exact_json, integer

DERIVATION = ROOT / "research/DCP_PHYSICAL_BAD_REGISTER_LINEAGE.md"
REPORT = ROOT / "research/phase_workbench/dcp_physical_bad_register_lineage.json"
PRIMARY = ROOT / "research/literature_cache/cs_0304005_source/quantum_average.tex"


@dataclass(frozen=True)
class PhaseDensity:
    modulus: int
    label: int
    source_ids: tuple[str, ...]
    zero_population: Fraction
    phase_visibility: Fraction
    merge_depth: int = 0

    def __post_init__(self):
        integer(self.modulus, "actual DCP modulus", 2)
        integer(self.label, "canonical measured Fourier label")
        integer(self.merge_depth, "nonnegative physical merge depth")
        ids = tuple(self.source_ids)
        if self.label >= self.modulus or not ids or len(set(ids)) != len(ids) or any(not isinstance(s, str) or not s for s in ids):
            raise ValueError("canonical label and disjoint original-state receipt IDs required")
        a, v = _rational(self.zero_population), _rational(self.phase_visibility)
        if not 0 <= a <= 1 or v < 0 or v * v > 4 * a * (1 - a):
            raise ValueError("positive semidefinite normalized physical phase density required")
        object.__setattr__(self, "zero_population", a)
        object.__setattr__(self, "phase_visibility", v)
        object.__setattr__(self, "source_ids", ids)

    def public_solver_view(self):
        return {"modulus": self.modulus, "measured_Fourier_label": self.label,
                "original_state_receipt_IDs": self.source_ids, "merge_depth": self.merge_depth}

    def audit_record(self):
        return {**self.public_solver_view(), "PRIVATE_density_zero_population": str(self.zero_population),
                "PRIVATE_density_phase_visibility": str(self.phase_visibility),
                "density_expression": "[[a,v*exp(-2*pi*i*k*s/N)/2],[v*exp(2*pi*i*k*s/N)/2,1-a]]",
                "phase_visibility_alone_certifies_secret_information_at_zero_label": False,
                "source_noise_parameters_or_phase_given_to_solver": False}

    def literal_density(self, hidden_s_FOR_CALIBRATION_ONLY):
        integer(hidden_s_FOR_CALIBRATION_ONLY, "canonical truth-only hidden slope")
        if hidden_s_FOR_CALIBRATION_ONLY >= self.modulus:
            raise ValueError("canonical calibration slope required")
        angle = 2 * np.pi * ((self.label * hidden_s_FOR_CALIBRATION_ONLY) % self.modulus / self.modulus)
        c = float(self.phase_visibility) * np.exp(-1j * angle) / 2
        return np.asarray([[float(self.zero_population), c], [c.conjugate(), float(1 - self.zero_population)]])


def source_density(N, label, source_id, bad_probability, bad_zero_probability="1/2"):
    p, b = map(_rational, (bad_probability, bad_zero_probability))
    if not 0 <= p <= 1 or not 0 <= b <= 1:
        raise ValueError("valid private source-mixture probabilities required")
    return PhaseDensity(N, label, (source_id,), (1 - p) / 2 + p * b, 1 - p)


def merge(left, right, branch, *, independent_given_secret=False):
    if independent_given_secret is not True:
        raise ValueError("conditional product source model must be established; receipt IDs do not prove independence")
    if not isinstance(left, PhaseDensity) or not isinstance(right, PhaseDensity) or left.modulus != right.modulus:
        raise ValueError("two physical phase densities at the same actual root required")
    if set(left.source_ids) & set(right.source_ids):
        raise ValueError("reused ancestors are not two independent quantum copies")
    if branch not in (0, 1) or type(branch) is not int:
        raise ValueError("actual target computational measurement branch required")
    a, b = left.zero_population, right.zero_population
    prob = a * b + (1 - a) * (1 - b) if branch == 0 else a * (1 - b) + (1 - a) * b
    base = {"input_public_views": (left.public_solver_view(), right.public_solver_view()), "branch": branch,
            "exact_branch_probability": str(prob), "branch_chosen_for_free": False,
            "conditional_product_source_model_required": True, "receipt_IDs_prove_statistical_independence": False,
            "coherent_phase_evaluator_or_chosen_label_query_supplied": False}
    if not prob:
        return {**base, "status": "IMPOSSIBLE_BRANCH_NOT_A_POSTSELECTED_STATE", "output_audit": None}, None
    out_a = a * (b if branch == 0 else 1 - b) / prob
    out_v = left.phase_visibility * right.phase_visibility / (2 * prob)
    label = (left.label + (1 if branch == 0 else -1) * right.label) % left.modulus
    out = PhaseDensity(left.modulus, label, left.source_ids + right.source_ids, out_a, out_v, max(left.merge_depth, right.merge_depth) + 1)
    return {**base, "status": "ACTUAL_CNOT_MEASURED_TARGET_BRANCH", "output_audit": out.audit_record()}, out


def literal_merge(left, right, branch, hidden_s_FOR_CALIBRATION_ONLY):
    validated, _ = merge(left, right, branch, independent_given_secret=True)
    CNOT = np.asarray([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
    joint = np.kron(left.literal_density(hidden_s_FOR_CALIBRATION_ONLY), right.literal_density(hidden_s_FOR_CALIBRATION_ONLY))
    joint = CNOT @ joint @ CNOT.T
    block = joint[np.ix_((branch, 2 + branch), (branch, 2 + branch))]
    probability = float(np.trace(block).real)
    exact_prob = Fraction(validated["exact_branch_probability"])
    if exact_prob > 0 and probability <= 0:
        raise ArithmeticError("literal float branch underflow is not an impossible quantum branch")
    return probability, block / probability if probability > 0 else None


def merge_controls():
    cases = []
    for name, pa, ba, pb, bb in (
        ("GOOD_GOOD", "0", "1/2", "0", "1/2"),
        ("GOOD_BAD_ZERO", "0", "1/2", "1", "1"),
        ("BAD_ONE_GOOD", "1", "0", "0", "1/2"),
        ("BAD_ZERO_BAD_ZERO", "1", "1", "1", "1"),
        ("BALANCED_CONTAMINATION", "1/32", "1/2", "1/32", "1/2"),
        ("BIASED_ALLOWED_CONTAMINATION", "1/32", "1", "1/32", "1"),
    ):
        left = source_density(32, 11, f"{name}:left", pa, ba)
        right = source_density(32, 7, f"{name}:right", pb, bb)
        branches = []
        for branch in (0, 1):
            result, out = merge(left, right, branch, independent_given_secret=True)
            p, density = literal_merge(left, right, branch, 13)
            if abs(p - float(Fraction(result["exact_branch_probability"]))) > 1e-12 or (out is not None and np.max(abs(density - out.literal_density(13))) > 1e-12):
                raise ArithmeticError("literal quantum CNOT branch differs from exact density algebra")
            branches.append({"merge": result, "diagnostic_literal_probability": p,
                             "literal_density_agrees_with_exact_output": out is not None,
                             "diagnostic_output_visibility": 0 if density is None else float(2 * abs(density[0, 1]))})
        cases.append({"case": name, "private_source_parameters": {"left_bad_probability": pa, "left_bad_zero_probability": ba,
                     "right_bad_probability": pb, "right_bad_zero_probability": bb},
                      "input_audits": (left.audit_record(), right.audit_record()), "literal_branches": tuple(branches),
                      "hidden_s_ONLY_FOR_LITERAL_CALIBRATION": 13})
    return tuple(cases)


def balanced_lineage_ledger(logN, failure_parameter, merge_depth, bits=192):
    for x, name in ((logN, "log2 original modulus"), (failure_parameter, "constant failure parameter"), (bits, "certificate bits")):
        integer(x, "positive " + name, 1)
    integer(merge_depth, "nonnegative balanced physical merge depth")
    if logN < 3 or failure_parameter > 64 or merge_depth > 4096 or bits > 256:
        raise ValueError("whole lineage/probability certificate cap exceeded")
    denominator, leaves = logN ** failure_parameter, 2 ** merge_depth
    p = Fraction(1, denominator)
    exact_power = power_box(1 - p, leaves, bits)
    bernoulli = Fraction(1, 2 ** min(bits, leaves // denominator))
    upper = min(bernoulli, Fraction(exact_power["upper"]))
    copies = None
    if upper <= Fraction(1, 2):
        need = 1 / (8 * upper * upper)
        copies = (need.numerator + need.denominator - 1) // need.denominator
    return {
        "log2_original_modulus": logN, "failure_parameter": failure_parameter,
        "legal_per_register_bad_probability": str(p), "bad_conditional_density": "I/2 from equal bad basis-state mixture",
        "visibility_bound_is_for_LEGAL_MAX_RATE_BALANCED_subclass_NOT_all_smaller_rates": True,
        "balanced_merge_depth": merge_depth, "disjoint_original_state_leaves": leaves,
        "exact_visibility_formula": "(1-p_bad)^original_leaves",
        "visibility_exact_power_box": exact_power,
        "reciprocal_Bernoulli_complete_blocks": leaves // denominator,
        "visibility_Bernoulli_upper": str(bernoulli), "output_phase_visibility_upper": str(upper),
        "best_single_target_parity_success_upper": str((1 + upper) / 2),
        "necessary_INDEPENDENT_target_copies_for_parity_success3over4_lower": copies,
        "parity_copy_lower_bound_uses_Pinsker_and_gamma_at_most_half": copies is not None,
        "target_label_would_encode_only_parity_not_full_secret": True,
        "parity_copy_bound_requires_actual_label_N_over_2_AND_independent_targets": True,
        "all_realized_branches_have_probability_half_IN_balanced_model": True,
        "label_target_success_certifies_phase_information": False,
        "any_output_ancestor_reuse_is_free": False,
        "source_bad_flags_given_to_algorithm": False,
        "independent_source_noise_conditional_on_common_secret_required": True,
        "source_ID_uniqueness_establishes_statistical_independence": False,
        "arbitrary_collective_DCP_decoder_or_fault_correction_excluded": False,
    }


def reduction_noise_tradeoff(n):
    integer(n, "positive source lattice dimension", 2)
    if n > 4096:
        raise ValueError("whole source tradeoff cap exceeded")
    logN = (4 * n + 1) * n
    depth = isqrt(logN)
    if depth * depth < logN:
        depth += 1
    leaves = 2 ** depth
    f = 1
    while logN ** f < 2 * leaves:
        f += 1
    # This is a diagnostic substitution, NOT a theorem with variable f.
    twice_approx_exponent = 1 + 4 * f
    exceeds_LLL = n ** twice_approx_exponent > 2 ** (n - 1)
    return {
        "lattice_dimension": n, "published_M": {"base": 2, "exponent": 4 * n},
        "published_DCP_log2N": logN, "illustrative_sqrt_log_depth_NOT_universal_sieve_requirement": depth,
        "balanced_original_leaves_at_illustrative_depth": leaves,
        "minimum_integer_f_for_Bernoulli_visibility_lower_at_least_half": f,
        "diagnostic_unique_SVP_approximation_n_power": str(Fraction(1, 2) + 2 * f),
        "diagnostic_approximation_exceeds_LLL_2_to_nminus1over2": exceeds_LLL,
        "published_prime_lower_bound_n_power": 2 + 2 * f,
        "variable_f_is_covered_by_constant_f_polynomial_reduction": False,
        "raising_f_removes_all_algorithmic_blockers": False,
        "different_sieves_or_collective_noise_handling_excluded": False,
    }


def correlated_noise_countercontrol():
    p = Fraction(1, 32)
    good_l = source_density(32, 11, "correlated:left", "0")
    good_r = source_density(32, 7, "correlated:right", "0")
    joint = (1 - float(p)) * np.kron(good_l.literal_density(13), good_r.literal_density(13))
    joint += float(p) * np.diag((0.5, 0, 0, 0.5))
    CNOT = np.asarray([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
    after = CNOT @ joint @ CNOT.T
    branches = []
    for b in (0, 1):
        block = after[np.ix_((b, 2 + b), (b, 2 + b))]
        prob = float(np.trace(block).real)
        exact_p = (1 + p) / 2 if b == 0 else (1 - p) / 2
        exact_v = (1 - p) / (1 + p) if b == 0 else Fraction(1)
        if abs(prob - float(exact_p)) > 1e-12 or abs(2 * abs(block[0, 1]) / prob - float(exact_v)) > 1e-12:
            raise ArithmeticError("correlated source countercontrol disagrees with literal CNOT")
        branches.append({"branch": b, "exact_branch_probability": str(exact_p), "exact_output_visibility": str(exact_v)})
    return {"legal_marginal_bad_probability": str(p), "noise_recipe": "all good with1-p; all bad00 or bad11 with p/2 each",
            "marginal_zero_population": "1/2", "marginal_phase_visibility": str(1 - p),
            "disjoint_receipt_IDs": ("correlated:left", "correlated:right"), "literal_joint_branches": tuple(branches),
            "marginal_product_CNOT_formula_applies": False, "IDs_or_marginal_rates_prove_independence": False,
            "countercontrol_claimed_as_all_published_source_models": False}


def one_register_heralding_control():
    plus = np.asarray((1, 1)) / np.sqrt(2)
    yplus = np.asarray((1, 1j)) / np.sqrt(2)
    effects = (np.diag((1, 0)), np.diag((0, 1)), np.outer(plus, plus.conj()), np.outer(yplus, yplus.conj()), np.eye(2))
    mean_good = sum(source_density(32, 7, f"herald:{s}", "0").literal_density(s) for s in range(32)) / 32
    if np.max(abs(mean_good - np.eye(2) / 2)) > 1e-12:
        raise ArithmeticError("nonzero-label uniform-secret one-copy twirl is not I/2")
    return {
        "actual_DCP_modulus": 32, "nonzero_measured_label": 7,
        "complete_hidden_sweep_FOR_CALIBRATION_ONLY": 32,
        "exact_uniform_secret_good_density": "I/2", "exact_balanced_bad_density": "I/2",
        "fixed_effects": ("Z0", "Z1", "Xplus", "Yplus", "identity"),
        "exact_good_AND_bad_acceptance_probabilities": ("1/2", "1/2", "1/2", "1/2", "1"),
        "diagnostic_same_good_bad_probabilities": tuple(float(np.trace(E @ mean_good).real) for E in effects),
        "PSD_effect_rejecting_both_bad_basis_states_must_be_zero": True,
        "source_phase_or_other_register_information_given_to_filter": False,
        "label_zero_EXCEPTION_has_known_phase_but_no_hidden_secret_information": True,
        "all_collective_or_posterior_conditioned_purification_excluded": False,
    }


def physical_Z_subclass_bridge():
    """Reuse the existing physical-noise engine, not its full-promise coverage."""
    p = Fraction(1, 5)
    left, right = compile_packet([[1, 1, 1]], 32), compile_packet([[1, 1, 0]], 32)
    noise = IndependentPhysicalZ.iid(left, right, p / 2)
    good = source_density(32, 11, "bridge:good", "0").literal_density(13)
    balanced = source_density(32, 11, "bridge:balanced", p).literal_density(13)
    biased = source_density(32, 11, "bridge:biased", p, "1").literal_density(13)
    Z = np.diag((1, -1))
    flipped = (1 - float(p / 2)) * good + float(p / 2) * Z @ good @ Z
    if np.max(abs(balanced - flipped)) > 1e-12:
        raise ArithmeticError("balanced bad-basis mixture is not the existing physical Z channel")
    rows = []
    for h in range(1 << left.retained_qubits):
        support = sum((r & h).bit_count() & 1 for r in left.kernel_rows + right.kernel_rows)
        contrast = noise.fourier(left, right, h)
        if contrast != (1 - p) ** support:
            raise ArithmeticError("existing packet physical-Z contrast and bad-basis subclass disagree")
        rows.append({"logical_Fourier_mask": h, "original_physical_phase_error_support": support,
                     "exact_existing_physical_Z_contrast": str(contrast), "exact_balanced_bad_contrast": str((1 - p) ** support)})
    return {"legal_balanced_bad_rate_at_logN5": str(p), "equivalent_physical_Z_flip_rate": str(p / 2),
            "exact_one_register_phase_contrast": str(1 - p),
            "left_public_packet_labels": left.labels, "right_public_packet_labels": right.labels,
            "left_actual_kernel_rows": left.kernel_rows, "right_actual_kernel_rows": right.kernel_rows,
            "existing_packet_noise_contrasts": tuple(rows),
            "diagnostic_balanced_density_channel_error": float(np.max(abs(balanced - flipped))),
            "diagnostic_biased_basis_density_channel_error": float(np.max(abs(biased - flipped))),
            "balanced_independent_subclass_covered_by_existing_physical_Z": True,
            "FULL_arbitrary_basis_contamination_promise_covered_by_existing_physical_Z": False,
            "unknown_coset_phases_are_made_classically_known_by_noise_bridge": False}


def build_report():
    profiles = tuple(balanced_lineage_ledger(logN, f, (isqrt(logN) + int(isqrt(logN) ** 2 < logN)))
                     for logN in (32, 128, 1024, 4096) for f in (1, 2, 4))
    return {
        "status": "PHYSICAL_DCP_BAD_REGISTER_CNOT_LINEAGE_AUDIT_NOT_A_GENERAL_DCP_NO_GO",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "primary_latex_sha256": hashlib.sha256(PRIMARY.read_bytes()).hexdigest(),
        "dependency_sha256": {f: hashlib.sha256((ROOT / "theorems" / f).read_bytes()).hexdigest() for f in ("dcp_sample_workbench.py", "dcp_carry_packets.py", "dcp_physical_phase_noise.py", "native_basis_lottery.py", "native_small_multiple_completion.py", "ternary_measured_lattice_decoder.py")},
        "existing_state_input_theorem_contract": asdict(dcp_state_access_contract()),
        "literal_physical_merge_controls": merge_controls(),
        "pure_bad_controls_are_components_NOT_all_promised_source_distributions": True,
        "correlated_bad_register_countercontrol": correlated_noise_countercontrol(),
        "single_register_heralding_countercontrol": one_register_heralding_control(),
        "existing_physical_Z_balanced_subclass_bridge": physical_Z_subclass_bridge(),
        "balanced_bad_register_lineage_profiles": profiles,
        "source_reduction_failure_tradeoffs": tuple(reduction_noise_tradeoff(n) for n in (8, 32, 128, 512)),
        "actual_lattice_to_coset_state_generator_implemented": False,
        "coherent_phase_evaluator_or_chosen_label_queries_supplied": False,
        "full_bad_register_DCP_solver_supplied": False,
        "additional_state_preparation_or_gate_errors_certified": False,
        "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
        "research_decision": "REQUIRE_PHASE_VISIBILITY_AND_REAL_BAD_REGISTER_COVERAGE_NOT_JUST_SIEVE_LABEL_SUCCESS",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    print(json.dumps({"status": report["status"], "physical_merge_cases": len(report["literal_physical_merge_controls"]),
        "lineage_profiles": len(report["balanced_bad_register_lineage_profiles"]),
        "source_reduction_dimensions": [p["lattice_dimension"] for p in report["source_reduction_failure_tradeoffs"]],
        "full_DCP_solver_or_actual_source_generator_supplied": False}, indent=2))


if __name__ == "__main__":
    main()
