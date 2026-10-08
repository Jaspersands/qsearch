"""Conditional approximate coherent access to a fixed noisy phase bank.

Known inverses are not exact ideal inverses; every phase power is charged.
No chosen-label source, reusable IID originals, or receiver is supplied.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from flint import fmpq

from native_noisy_phase_input import ReceiverInput, angle_recipe, checked_source_bank, native_labels, sqrt_box
from ternary_certified_noise_sampler import rational
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_noise_degradation import NoisyLinearRecord
from native_recovery_capacity import indexed_recovery_capacity

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_NOISY_INDEXED_ACCESS.md"
REPORT = ROOT / "research/reductions/native_noisy_indexed_access.json"


def canonical_power(exponent, q):
    root_digits(q)
    if type(exponent) is not int:
        raise ValueError("exact integer phase exponent required")
    k = exponent % q
    return k if 2*k < q else k-q


def indexed_access_bound(q, records, second_moment, powers, failure_bits=64):
    root_digits(q)
    integer(records, "positive fixed native bank size", 1)
    integer(failure_bits, "positive failure bits", 1)
    V = rational(second_moment, "public source integer moment")
    if V < 0:
        raise ValueError("nonnegative true source moment required")
    reduced = tuple(canonical_power(k, q) for k in powers)
    W, T = sum(abs(k) for k in reduced), sum(k != 0 for k in reduced)
    gate_bits = failure_bits+(2*T-1).bit_length() if T else failure_bits
    sqrt_bits = failure_bits+(4*W-1).bit_length() if W else failure_bits
    squared = 80*records*V/(q*q)
    lo, hi = sqrt_box(squared, sqrt_bits)
    noise = min(fmpq(1), W*hi)
    gate = min(fmpq(1), fmpq(2*T, 2**gate_bits))
    total = min(fmpq(1), noise+gate)
    return {"modulus": q, "fixed_original_bank_size": records,
            "independent_classical_originals_required": 2*records,
            "source_integer_second_moment_upper": str(V),
            "canonical_signed_phase_powers": reduced, "weighted_phase_exposure": W,
            "nonidentity_phase_call_count": T, "local_gate_precision_bits": gate_bits,
            "RMS_operator_error_squared_upper": str(squared), "sqrt_interval_bits": sqrt_bits,
            "sqrt_of_RMS_upper_bound_lower_enclosure": str(lo), "sqrt_of_RMS_upper_bound_upper_enclosure": str(hi),
            "expected_complete_receiver_noise_success_loss_upper": str(noise),
            "complete_gate_error_upper": str(gate), "complete_pre_rounding_success_loss_upper": str(total),
            "bound_is_nonvacuous": total < 1,
            "source_errors_are_fixed_across_reused_calls": True,
            "noise_resampled_on_every_call": False,
            "ideal_unknown_inverse_supplied_exactly": False,
            "approximate_ideal_phase_and_inverse_access_conditionally_supported": True,
            "chosen_label_oracle_supplied": False, "independent_quantum_originals_created_by_reuse": False,
            "fast_forwarded_power_costs_only_one_unit_of_noise_exposure": False,
            "source_law_or_moment_inferred_from_values": False,
            "hardware_synthesis_implemented": False, "efficient_receiver_supplied": False,
            "hardness_transfer_admitted": False,
            "assumptions": ["same integer-vector secret", "fixed original IID source bank",
                            "true public second-moment bound", "committed maximum phase exposure",
                            "receiver accesses only fixed-bank labels",
                            "charged known local gates and caller operation errors"]}


def indexed_recipe(samples, mask, exponent, precision_bits=64):
    samples, mask, q, _ = checked_source_bank(samples, mask)
    integer(precision_bits, "positive literal oracle angle precision", 1)
    k = canonical_power(exponent, q)
    private, receivers, ancestry = [], [], []
    for j, (a, c) in enumerate(zip(samples[::2], samples[1::2])):
        values = tuple((s.value+sum(x*y for x, y in zip(s.label, mask))) % q for s in (a, c))
        receivers.append(ReceiverInput(q, 2*root_digits(q), native_labels(a.label, c.label, q),
                                      a.label, c.label, f"qutrit-{j}").public()
                         | {"access": "fixed-bank index; phase oracle only"})
        private.append({"state_handle": f"qutrit-{j}",
                        "scaled_known_phase_values": tuple((k*x) % q for x in values),
                        "angle_recipes": tuple(angle_recipe(q, (k*x) % q, precision_bits) for x in values)})
        ancestry.append((a.source_id, c.source_id))
    count = len(receivers)
    return {"modulus": q, "canonical_phase_power": k, "local_angle_precision_bits": precision_bits,
            "original_source_ancestry": ancestry,
            "receiver_public_bank": receivers, "reduction_side_multiplexor_branches": private,
            "controlled_operation": "sum_i |i><i| tensor diag(1,omega^(k*b_i),omega^(k*d_i)); invalid indices identity",
            "index_bits": (count-1).bit_length(), "branch_count": count,
            "access_implementation": "explicit sequential reversible index equality controls; no QRAM assumed",
            "comparison_compute_uncompute_pairs_per_query_upper": count,
            "diagonal_branches_per_query_upper": 2*count,
            "inverse_by_negating_power": True, "arbitrary_new_frequency_labels_available": False,
            "source_moment_claimed_by_this_recipe": False, "quantum_hardware_executed": False}


def indexed_access_profile(n, q, records, second_moment, powers, failure_bits=64):
    bound = indexed_access_bound(q, records, second_moment, powers, failure_bits)
    return bound | {"secret_dimension": n,
                    "full_recovery_capacity": indexed_recovery_capacity(n, q, records, bound["weighted_phase_exposure"]),
                    "nonvacuous_noise_bound_is_full_recovery_feasibility": False}


def build_report():
    controls = []
    for q, powers in ((9, (1, -1, 3)), (3**80, (1, -1)*32), (3**80, (2**60,)), (9, (9, 10, -10))):
        controls.append(indexed_access_bound(q, 8, "1/2", powers))
    samples = tuple(NoisyLinearRecord((i % 9, (2*i+1) % 9), (3*i+2) % 9, 9, f"indexed-source-{i}") for i in range(6))
    recipes = [indexed_recipe(samples, (2, 4), k) for k in (1, -1, 3, 9)]
    V = 3**128*fmpq(1, 1048576)**2/3+fmpq(1, 2)
    gaussian = [indexed_access_profile(64, 3**64, 512, V, (1,)*T) for T in (128, 1024)]
    # A compact huge-exposure control does not materialize an exponential call list.
    gaussian.append(indexed_access_profile(64, 3**64, 512, V, (2**20,)))
    return {"status": "CONDITIONAL_FIXED_BANK_COHERENT_ACCESS_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "bounds": controls, "originals_for_recipe_replay": tuple(s.public() for s in samples),
            "reduction_side_mask_for_recipe_replay": (2, 4), "multiplexor_recipes": recipes,
            "Gaussian_moment_exposure_controls": gaussian,
            "quantum_hardware_states_executed": 0, "ideal_source_inverse_supplied_exactly": False,
            "chosen_label_oracle_supplied": False, "efficient_receiver_supplied": False,
            "hardness_transfer_admitted": False, "accepted_speedup_candidate": False,
            "unseen_label_phase_values_or_secret_reconstruction_supplied": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "bound_controls": len(report["bounds"]),
                      "indexed_recipes": len(report["multiplexor_recipes"]),
                      "Gaussian_exposure_loss_upper": [g["complete_pre_rounding_success_loss_upper"] for g in report["Gaussian_moment_exposure_controls"]],
                      "ideal_source_inverse_supplied_exactly": False}, indent=2))


if __name__ == "__main__":
    main()
