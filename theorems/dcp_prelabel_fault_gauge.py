"""Prelabel basis-fault gauge and exact native correlated-fault Bell moments.

LOCAL DERIVATION / REVIEW PENDING. Extends the existing pairing-program gauge;
no new programmable oracle, native reduction certificate or decoder is granted.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from dcp_bell_inference_kernel import exact
from dcp_carry_packets import binary_rank, compile_packet
from dcp_physical_phase_noise import native_physical_source_mean, read
from dcp_noisy_completion import low_noise_clean_block_baseline

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_prelabel_fault_gauge.json"


@dataclass(frozen=True)
class PrelabelBasisFaultLaw:
    """A classical joint mask law, independent of subsequent Fourier labels.

    Entries are (left_mask, right_mask, probability). They flag failed basis
    registers, NOT physical Z errors. Lineage assumptions are not proven here.
    """
    entries: tuple[tuple[int, int, Fraction], ...]

    def __post_init__(self):
        if any(type(a) is not int or type(b) is not int for a, b, _ in self.entries):
            raise ValueError("integer basis-fault masks required")
        entries = tuple((a, b, Fraction(p)) for a, b, p in self.entries)
        if not entries or any(a < 0 or b < 0 or p < 0 for a, b, p in entries) or sum(p for _, _, p in entries) != 1:
            raise ValueError("normalized nonnegative classical fault-mask law required")
        object.__setattr__(self, "entries", entries)

    def validate_widths(self, left_width, right_width):
        if left_width < 1 or right_width < 1 or any(a >= 1 << left_width or b >= 1 << right_width for a, b, _ in self.entries):
            raise ValueError("basis-fault mask outside supplied physical width")

    def fourier(self, left, right, h):
        self.validate_widths(left.input_qubits, right.input_qubits)
        if left.retained_qubits != right.retained_qubits or not 0 <= h < 1 << left.retained_qubits:
            raise ValueError("equal logical widths and a valid logical mask required")
        images = [sum(((row & h).bit_count() & 1) << i for i, row in enumerate(p.kernel_rows))
                  for p in (left, right)]
        return sum(probability for a, b, probability in self.entries if not (a & images[0] or b & images[1]))


def basis_gauge_transfer_gate(*, fault_data_precedes_uniform_fourier_labels=False,
                             independent_uniform_fourier_labels=False,
                             old_labels_and_gauge_coins_discarded=False,
                             classical_mixture_of_product_good_or_basis_states=False,
                             independent_fault_statuses=False):
    declarations = {
        "prelabel_fault_and_bad_bit_lineage": fault_data_precedes_uniform_fourier_labels,
        "independent_uniform_fourier_labels": independent_uniform_fourier_labels,
        "discard_old_labels_and_gauge_coins_before_selection": old_labels_and_gauge_coins_discarded,
        "classical_mixture_of_product_good_or_basis_states": classical_mixture_of_product_good_or_basis_states,
    }
    issues = [name + " is not established" for name, value in declarations.items() if not value]
    return {"status": "CONDITIONAL_SOURCE_TRANSFER_NOT_AUTOMATIC_REDUCTION_CERTIFICATE",
            "transfer_obligations_satisfied_as_declared": not issues, "issues": issues,
            "resulting_channel": "classical_correlated_physical_Z_with_fault_avoidance_Fourier_law" if not issues else None,
            "iid_physical_phase_formula_usable_as_declared": not issues and independent_fault_statuses,
            "iid_basis_failure_to_phase_flip_rate": "epsilon_i=gamma_i/2" if not issues and independent_fault_statuses else None,
            "independence_not_inferred_from_fault_marginals": True,
            "gauge_is_legal_degradation_not_lossless_original_experiment": True,
            "declarations_programmatically_proven": False,
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def _union_fault_moment(n, left_union, right_union):
    """Average low charts analytically; no 2^k logical direction enumeration."""
    k, N = 2 * n, 1 << (2 * n)
    pivot_mask = (1 << n) - 1
    b = (left_union & pivot_mask).bit_count() + (right_union & pivot_mask).bit_count()
    free_union = (left_union | right_union) >> n
    d = k - free_union.bit_count()
    nonzero_single = (1 << d) - 1
    nonzero_pair = (1 << (k - d)) * 3**d - N - (1 << d) + 1
    return (Fraction(N) + Fraction(nonzero_single, 1 << b)
            + nonzero_pair * Fraction(1, 1 << b) * Fraction(3, 4)**(2 * n - b)) / N


def native_gauged_source_mean(n, law):
    if type(n) is not int or n < 1:
        raise ValueError("positive integer vector dimension required")
    law.validate_widths(3 * n, 3 * n)
    value = sum(p * t * _union_fault_moment(n, a | c, b | d)
                for a, b, p in law.entries for c, d, t in law.entries)
    assert value >= 1
    prefix = native_physical_source_mean(n, 0)["two_public_prefix_invertibility_probability"]
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "dimension": n, "logical_width": 2 * n,
            "source": "native_n_by_3n_conditioned_on_first_n_columns_invertible_after_discarded_prelabel_gauge",
            "conditional_mean_relative_full_collision": exact(value),
            "joint_source_chi_squared_to_uniform_output": exact(value - 1),
            "two_public_prefix_invertibility_probability": prefix,
            "joint_prelabel_fault_law": [{"left_mask_hex": hex(a), "right_mask_hex": hex(b), "probability": exact(p)}
                                        for a, b, p in law.entries],
            "conceptual_independent_fault_law_pairs_evaluated": len(law.entries)**2,
            "physical_states_or_batches_not_duplicated_by_this_moment_identity": True,
            "logical_mask_enumeration_required": False,
            "cost_polynomial_in_explicit_fault_support_and_dimension": True,
            "fault_support_may_be_exponential_for_an_iid_law": True,
            "higher_label_independence_and_prelabel_gauge_required": True,
            "faults_can_be_classically_correlated_across_supplied_packets": True,
            "arbitrary_entangled_or_postlabel_corruption_covered": False,
            "effective_secret_character_order_at_least_four_required": True,
            "natural_reduction_source_promise_programmatically_verified": False,
            "decoder_or_speedup_provided": False}


def _fixed_source_calibration(law):
    total = Fraction(0)
    for a, b in itertools.product(range(4), repeat=2):
        packets = [compile_packet([[1, x & 1, x >> 1]], 8) for x in (a, b)]
        for h in range(4):
            selected = [r for p in packets for r in p.kernel_rows if (r & h).bit_count() & 1]
            total += law.fourier(*packets, h)**2 * Fraction(1, 1 << binary_rank(selected, 2)) / 16
    assert total == read(native_gauged_source_mean(1, law)["conditional_mean_relative_full_collision"])
    return total


def _iid_fault_law_calibration(gamma):
    gamma = Fraction(gamma)
    def p(mask):
        return gamma**mask.bit_count() * (1 - gamma)**(3 - mask.bit_count())
    return PrelabelBasisFaultLaw(tuple((a, b, p(a) * p(b)) for a, b in itertools.product(range(8), repeat=2)))


def _all_or_none(n, gamma):
    gamma = Fraction(gamma)
    if not 0 <= gamma <= 1:
        raise ValueError("basis failure probability must lie in [0,1]")
    mask = (1 << (3 * n)) - 1
    law = PrelabelBasisFaultLaw(((0, 0, 1 - gamma), (mask, mask, gamma)))
    row = native_gauged_source_mean(n, law)
    clean = read(native_physical_source_mean(n, 0)["conditional_mean_relative_full_collision"])
    assert read(row["conditional_mean_relative_full_collision"]) == 1 + (1 - gamma)**2 * (clean - 1)
    iid = native_physical_source_mean(n, gamma / 2)
    row.update({"each_register_basis_failure_marginal": exact(gamma),
                "same_marginal_iid_phase_source_mean": iid["conditional_mean_relative_full_collision"],
                "same_marginal_iid_uniformization_regime": iid["exponential_uniformization_regime"],
                "correlated_source_excess_is_clean_excess_times": exact((1 - gamma)**2),
                "counterexample_to_marginal_only_iid_uniformization_claim": True,
                "does_not_prove_actual_reduction_supplies_correlated_faults": True})
    return row


def _gauge_algebra_control():
    checks = 0
    for secret, updated_label, flip, x, y in itertools.product(range(8), range(8), range(2), range(2), range(2)):
        old = (-updated_label if flip else updated_label) % 8
        assert secret * old * ((x ^ flip) - (y ^ flip)) % 8 == secret * updated_label * (x - y) % 8
        checks += 1
    for updated_label, prelabel_bad_bit in itertools.product(range(8), range(2)):
        counts = [0, 0]
        for flip in range(2):
            counts[prelabel_bad_bit ^ flip] += 1
        assert counts == [1, 1]
    adaptive = [0, 0]
    for flip in range(2):
        old = (-1 if flip else 1) % 8
        adaptive[int(old >= 4) ^ flip] += 1
    assert adaptive == [2, 0]
    return {"modulus": 8, "exact_good_density_phase_identities_checked": checks,
            "fixed_prelabel_bad_bit_conditional_counts": [1, 1],
            "postlabel_bad_bit_counterexample": "bad_bit=1_if_original_label>=4_else_0",
            "counterexample_updated_label": 1, "counterexample_conditional_counts": adaptive,
            "discarding_old_labels_and_gauge_coins_is_essential": True,
            "arbitrary_postlabel_basis_faults_not_balanced": True}


def two_point_completion_ledger(n, q, failure_parameter=1, rank_failure_exponent=40):
    """Conditional Definition 3.1 transfer at M=q/2 a power of two.

    This maps the stated TWO-POINT input promise, not a full lattice reduction.
    Correct lower residue and fresh original registers are still prerequisites.
    """
    if type(n) is not int or n < 1 or type(q) is not int or q < 4 or q & (q - 1):
        raise ValueError("positive dimension and power-of-two q>=4 required")
    if type(failure_parameter) is not int or failure_parameter < 1:
        raise ValueError("positive integer failure parameter required")
    gamma = Fraction(1, (n * (q.bit_length() - 1))**failure_parameter)
    completion = low_noise_clean_block_baseline(n, gamma / 2, rank_failure_exponent)
    return {"status": "CONDITIONAL_TWO_POINT_SOURCE_MAP_NOT_LATTICE_REDUCTION_CERTIFICATE",
            "dimension": n, "modulus": q, "two_point_coordinate_range_M": q // 2,
            "failure_parameter": failure_parameter,
            "definition_3_1_basis_failure_bound": exact(gamma),
            "gauged_each_original_phase_flip_marginal_bound": exact(gamma / 2),
            "coordinate_qft_public_label_law": "IID_uniform_(Z_q)^n_conditional_on_prelabel_classical_fault_data",
            "signed_original_difference_unique_mod_q": True,
            "source_map_requires_padding_each_position_coordinate_to_q_and_exact_qft": True,
            "known_correct_residue_completion": completion,
            "three_n_packet_fault_union_bound": exact(min(Fraction(1), 3 * n * gamma)),
            "natural_lattice_M_and_total_state_supply_parameter_map_verified": False,
            "fault_independence_or_conditional_history_budget_inferred": False,
            "qft_correction_and_gauge_physical_precision_verified": False,
            "unknown_residue_decoder": False, "speedup_claim_allowed": False}


def run_controls():
    laws = [PrelabelBasisFaultLaw(((0, 0, Fraction(7, 8)), (7, 7, Fraction(1, 8)))),
            PrelabelBasisFaultLaw(((1, 0, Fraction(1, 2)), (0, 2, Fraction(1, 2)))),
            _iid_fault_law_calibration(Fraction(1, 8))]
    complete = [native_gauged_source_mean(1, law) for law in laws]
    for row, law in zip(complete, laws):
        value = _fixed_source_calibration(law)
        row["complete_systematic_low_chart_pairs_calibrated"] = 16
        row["direct_selected_row_rank_source_mean"] = exact(value)
    iid_expected = native_physical_source_mean(1, Fraction(1, 16))["conditional_mean_relative_full_collision"]
    assert complete[-1]["conditional_mean_relative_full_collision"] == iid_expected
    good = {"fault_data_precedes_uniform_fourier_labels": True,
            "independent_uniform_fourier_labels": True, "old_labels_and_gauge_coins_discarded": True,
            "classical_mixture_of_product_good_or_basis_states": True}
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "gauge_algebra": _gauge_algebra_control(),
            "complete_low_source_controls": complete,
            "correlated_all_or_none_scaling": [_all_or_none(n, Fraction(1, 8)) for n in (8, 16, 32, 64, 128, 256)],
            "source_transfer_gates": [basis_gauge_transfer_gate(**good),
                                      basis_gauge_transfer_gate(**good, independent_fault_statuses=True),
                                      basis_gauge_transfer_gate(),
                                      basis_gauge_transfer_gate(**{**good, "old_labels_and_gauge_coins_discarded": False}),
                                      basis_gauge_transfer_gate(**{**good, "fault_data_precedes_uniform_fourier_labels": False})],
            "two_point_completion_scaling": [two_point_completion_ledger(n, max(8, 1 << (n - 1).bit_length()))
                                              for n in (16, 32, 64, 128, 256, 512)],
            "existing_gauge_implementation": "core/dcp_pairing_programs.py:gauge_control",
            "claim_gate": {"prelabel_basis_fault_gauge_has_a_conditional_phase_channel_transfer": True,
                           "arbitrary_basis_failure_is_automatically_iid_phase_noise": False,
                           "correlated_native_source_formula_requires_exponential_mask_enumeration": False,
                           "actual_natural_reduction_fault_independence_verified": False,
                           "full_unknown_residue_decoder": False, "independent_theorem_review": False,
                           "speedup_claim_allowed": False},
            "dependency_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (Path(__file__), ROOT / "theorems/dcp_physical_phase_noise.py",
                                            ROOT / "theorems/dcp_bell_inference_kernel.py",
                                            ROOT / "theorems/dcp_full_bell_source_moments.py",
                                            ROOT / "theorems/dcp_noisy_completion.py",
                                            ROOT / "theorems/dcp_carry_packets.py", ROOT / "core/dcp_pairing_programs.py")}}


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
