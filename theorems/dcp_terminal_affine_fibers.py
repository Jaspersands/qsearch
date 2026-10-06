"""Native terminal-fiber affine-plane and fixed-tail-compression gates.

LOCAL DERIVATION / REVIEW PENDING. Not a decoder or a general DCP no-go.
Only bounded controls enumerate assignments; scaling ledgers do not.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

from dcp_bell_inference_kernel import exact
from dcp_carry_packets import binary_rank

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_terminal_affine_fibers.json"


def _positive_integer(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def direction_pair_counts(width):
    _positive_integer(width, "physical width")
    if width < 2:
        raise ValueError("at least two physical bits required")
    degenerate = 3 * (3 ** width - 2 * 2 ** width + 1)
    generic = 4 ** width - 3 * 3 ** width + 3 * 2 ** width - 1
    assert degenerate + generic == (2 ** width - 1) * (2 ** width - 2)
    assert degenerate % 6 == generic % 6 == 0
    return degenerate, generic


def exact_plane_expectation(n, width, modulus_bits):
    """Expected number of constant affine two-planes through any fixed anchor."""
    _positive_integer(n, "output dimension")
    _positive_integer(modulus_bits, "modulus bits")
    _positive_integer(width, "physical width")
    if width > 256 or n * modulus_bits > 4096:
        raise ValueError("exact control exceeds budget; use the symbolic source ledger")
    degenerate, generic = direction_pair_counts(width)
    return (Fraction(degenerate // 6, 1 << (2 * n * modulus_bits))
            + Fraction((generic // 6) << n, 1 << (3 * n * modulus_bits)))


def native_affine_fiber_bound(n, width, modulus_bits, *, prefix_conditioned=True):
    """Source-mean POINT MASS, not probability that no global plane exists."""
    for value, name in ((n, "output dimension"), (width, "physical width"),
                        (modulus_bits, "tested modulus bits")):
        _positive_integer(value, name)
    if width < max(n, 2) or type(prefix_conditioned) is not bool:
        raise ValueError("width>=max(n,2) and Boolean conditioning flag required")
    # 3^5<2^8; generic planes are fewer than 4^m/4. No floating logs.
    degenerate_bits = 2 * n * modulus_bits - (8 * width + 4) // 5 + 1
    generic_bits = 3 * n * modulus_bits - 2 * width - n + 2
    if prefix_conditioned:
        # Uniform parity-kernel points cost 2^n; prefix acceptance exceeds 1/4.
        degenerate_bits -= n + 2
        generic_bits -= n + 2
    total_bits = max(0, min(degenerate_bits, generic_bits) - 1)
    return {"status": "NATIVE_SOURCE_MEAN_AFFINE_PLANE_INCIDENT_POINT_MASS_UPPER_BOUND",
            "dimension": n, "physical_width": width, "tested_modulus_bits": modulus_bits,
            "modulus": f"2^{modulus_bits}",
            "parity_kernel_uniform_points_and_invertible_binary_prefix_conditioned": prefix_conditioned,
            "ordered_degenerate_direction_pairs": "3*(3^m-2*2^m+1)",
            "ordered_generic_direction_pairs": "4^m-3*3^m+3*2^m-1",
            "each_affine_plane_ordered_basis_multiplicity": 6,
            "degenerate_pair_per_row_source_probability": "2^(-2a)",
            "generic_pair_per_row_source_probability": "2^(1-3a)",
            "two_adic_order_two_intersection_contribution_included": True,
            "degenerate_term_dyadic_exponent": degenerate_bits,
            "generic_term_dyadic_exponent": generic_bits,
            "source_mean_incident_point_mass_upper_bound_dyadic_exponent": total_bits,
            "source_mean_incident_point_mass_upper_bound": f"2^-{total_bits}",
            "conditioning_factor_upper_bound": f"2^{n + 2}" if prefix_conditioned else "1",
            "every_public_label_adaptive_affine_chart_within_this_packet_covered": True,
            "no_affine_plane_exists_anywhere_in_the_packet_proved": False,
            "every_particular_packet_classified": False,
            "higher_precision_labels_may_be_used_for_chart_selection": True,
            "nonlinear_charts_or_interblock_quantum_mixing_excluded": False,
            "independent_theorem_review": False, "candidate_record_accepted": False,
            "novelty_claim": False, "speedup_claim_allowed": False}


def charged_packet_menu_bound(source_ledger, *, packet_choices=1, original_pool_states=None):
    """Charge all menus; an enormous pool menu is allowed to make this vacuous."""
    _positive_integer(packet_choices, "packet menu size")
    if original_pool_states is not None:
        _positive_integer(original_pool_states, "original IID pool states")
        if packet_choices != 1 or original_pool_states < source_ledger["physical_width"]:
            raise ValueError("choose one menu model and enough original registers")
        menu_bits = source_ledger["physical_width"] * (original_pool_states - 1).bit_length()
        menu_model = "ALL_ORDERED_DISTINCT_REGISTER_PACKETS_FROM_ORIGINAL_IID_POOL"
    else:
        menu_bits = (packet_choices - 1).bit_length()
        menu_model = "COMPLETED_NATIVE_PACKET_MENU"
    exponent = max(0, source_ledger["source_mean_incident_point_mass_upper_bound_dyadic_exponent"] - menu_bits)
    return {"status": "CHARGED_PACKET_SELECTION_POINT_MASS_UPPER_BOUND",
            "menu_model": menu_model, "packet_choices": packet_choices,
            "original_pool_states": original_pool_states,
            "menu_log2_upper_bound": menu_bits,
            "selected_packet_source_mean_incident_point_mass_upper_bound_dyadic_exponent": exponent,
            "selected_packet_source_mean_incident_point_mass_upper_bound": f"2^-{exponent}",
            "selection_independence_assumed": False,
            "within_packet_chart_choices_already_charged_by_global_incident_set": True,
            "vacuous_is_not_a_negative_result": exponent == 0,
            "same_label_copies_or_chosen_phase_sources_granted": False,
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def high_probability_point_mass_bound(source_ledger):
    bits = source_ledger["source_mean_incident_point_mass_upper_bound_dyadic_exponent"]
    threshold = bits // 2
    return {"status": "MARKOV_SOURCE_PACKET_TAIL_BOUND_NOT_AN_INSTANCE_CERTIFICATE",
            "incident_point_fraction_threshold": f"2^-{threshold}",
            "incident_point_fraction_threshold_dyadic_exponent": threshold,
            "packet_probability_of_exceeding_threshold_upper_bound": f"2^-{bits - threshold}",
            "packet_probability_of_exceeding_threshold_upper_bound_dyadic_exponent": bits - threshold,
            "nonvacuous_source_bound": bits > 0,
            "no_global_affine_plane_exists_in_good_packets_proved": False,
            "all_label_adaptive_affine_charts_of_good_packets_obey_same_mass_gate": True,
            "this_particular_packet_classified": False}


def sidon_cap_bound(tail_bits):
    _positive_integer(tail_bits, "affine tail bits")
    if tail_bits < 2:
        raise ValueError("at least two free affine tail bits required")
    size = 1 << tail_bits
    return (1 + math.isqrt(8 * size - 7)) // 2


def affine_tail_compression_bound(source_ledger, tail_bits, *, target_rank=1):
    """Uniform-secret mean for block-local, secret-independent rank-r compression."""
    _positive_integer(target_rank, "target projector rank")
    cap = sidon_cap_bound(tail_bits)
    width = source_ledger["physical_width"]
    available = width - source_ledger["dimension"] if source_ledger[
        "parity_kernel_uniform_points_and_invertible_binary_prefix_conditioned"] else width
    if tail_bits > available or target_rank > 1 << tail_bits:
        raise ValueError("tail and target rank exceed the available block")
    rank_term = min(Fraction(1), Fraction(target_rank * cap, 1 << tail_bits))
    bits = source_ledger["source_mean_incident_point_mass_upper_bound_dyadic_exponent"]
    return {"status": "PHYSICAL_AFFINE_BLOCK_LOCAL_TAIL_COMPRESSION_NECESSARY_GATE",
            "physical_affine_tail_bits": tail_bits, "block_size": str(1 << tail_bits),
            "target_projector_rank": target_rank, "plane_free_fiber_size_upper_bound": str(cap),
            "nonincident_points_rank_compression_probability_upper_bound": exact(rank_term),
            "source_mean_exception_mass_upper_bound": f"2^-{bits}",
            "uniform_secret_source_mean_acceptance_upper_bound": f"min(1,{rank_term}+2^-{bits})",
            "block_partition_can_depend_on_all_public_labels": True,
            "blocks_are_physical_binary_affine_and_equal_size": True,
            "within_block_projection_can_be_arbitrary_secret_independent_rank_r": True,
            "clean_workspace_return_or_entire_effective_projector_rank_required": True,
            "pointwise_phase_corrections_or_block_local_quantum_unitaries_do_not_evade": True,
            "labels_are_native_and_original_packet_is_not_postselected_without_cost": True,
            "uniform_secret_mean_is_a_per_secret_guarantee": False,
            "global_interblock_branch_mixing_or_nonlinear_physical_charts_covered": False,
            "unrestricted_reset_or_secret_dependent_discarded_trash_covered": False,
            "a_specific_packet_exception_fraction_certified": False,
            "general_quantum_decoder_no_go": False, "candidate_record_accepted": False,
            "independent_theorem_review": False, "speedup_claim_allowed": False}


def bounded_affine_planes(width, *, maximum_width=7):
    _positive_integer(width, "physical width")
    if width < 2 or width > maximum_width:
        raise ValueError("bounded control width exceeded; this is not a scalable search")
    through_zero = {tuple(sorted((0, u, v, u ^ v)))
                    for u in range(1, 1 << width) for v in range(u + 1, 1 << width)}
    planes = {tuple(sorted(x ^ anchor for x in plane))
              for plane in through_zero for anchor in range(1 << width)}
    return tuple(sorted(planes))


def bounded_fiber_incidence(labels, modulus_bits, *, maximum_width=7):
    _positive_integer(modulus_bits, "modulus bits")
    A = tuple(tuple(row) for row in labels)
    if not A or not A[0] or any(len(row) != len(A[0]) for row in A):
        raise ValueError("nonempty rectangular label matrix required")
    width, modulus = len(A[0]), 1 << modulus_bits
    if any(type(a) is not int or not 0 <= a < modulus for row in A for a in row):
        raise ValueError("canonical modular integer labels required")
    planes = bounded_affine_planes(width, maximum_width=maximum_width)
    values = [tuple(sum(a for i, a in enumerate(row) if x >> i & 1) % modulus for row in A)
              for x in range(1 << width)]
    constant = tuple(plane for plane in planes if len({values[x] for x in plane}) == 1)
    incident = tuple(sorted({x for plane in constant for x in plane}))
    return {"constant_planes": constant, "incident_points": incident, "values": values}


def _source_control(n, width, modulus_bits):
    modulus = 1 << modulus_bits
    if n * width * modulus_bits > 13:
        raise ValueError("complete source control budget exceeded")
    plane_total = point_total = accepted = kernel_incident_total = 0
    sources = modulus ** (n * width)
    for entries in itertools.product(range(modulus), repeat=n * width):
        A = tuple(tuple(entries[l * width:(l + 1) * width]) for l in range(n))
        row = bounded_fiber_incidence(A, modulus_bits)
        plane_total += 4 * len(row["constant_planes"])
        point_total += len(row["incident_points"])
        prefix = tuple(sum((a & 1) << j for j, a in enumerate(component[:n])) for component in A)
        if binary_rank(prefix, n) == n:
            accepted += 1
            kernel_incident_total += sum(all(t % 2 == 0 for t in row["values"][x])
                                         for x in row["incident_points"])
    expectation = exact_plane_expectation(n, width, modulus_bits)
    assert Fraction(plane_total, sources * (1 << width)) == expectation
    prefix_mass = math.prod(1 - Fraction(1, 1 << j) for j in range(1, n + 1))
    assert Fraction(accepted, sources) == prefix_mass
    kernel_mass = Fraction(kernel_incident_total, accepted * (1 << (width - n)))
    assert kernel_mass <= min(Fraction(1), expectation * (1 << n) / prefix_mass)
    ledger = native_affine_fiber_bound(n, width, modulus_bits)
    assert kernel_mass <= Fraction(1, 1 << ledger["source_mean_incident_point_mass_upper_bound_dyadic_exponent"])
    return {"dimension": n, "physical_width": width, "modulus_bits": modulus_bits,
            "complete_label_tables": sources, "prefix_accepted_tables": accepted,
            "source_mean_affine_planes_through_uniform_point": exact(expectation),
            "source_mean_full_cube_incident_point_fraction": exact(Fraction(point_total, sources * (1 << width))),
            "source_mean_zero_syndrome_incident_point_fraction_conditioned_prefix": exact(kernel_mass),
            "source_ledger": ledger}


def run_controls():
    scalings = [native_affine_fiber_bound(n, n * (4 * n + 1) + 16, 4 * n + 1)
                for n in (4, 8, 16, 32, 64)]
    partial = [native_affine_fiber_bound(16, 1056, a) for a in (32, 48, 56, 60, 65)]
    anchor_counter = bounded_fiber_incidence(((1, 1, 1, 1),), 2)
    assert 0 not in anchor_counter["incident_points"] and anchor_counter["constant_planes"]
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING",
            "complete_native_source_controls": [_source_control(*parameters) for parameters in
                                               ((1, 3, 1), (1, 3, 2), (1, 3, 3), (2, 3, 1), (1, 4, 2))],
            "native_near_density_one_scaling": scalings,
            "partial_modulus_affine_restart_bounds": partial,
            "increased_density_escape_controls": [native_affine_fiber_bound(16, m, 65)
                                                   for m in (1248, 1300, 2080)],
            "high_probability_packet_gates": [high_probability_point_mass_bound(row) for row in scalings],
            "affine_tail_compression": [affine_tail_compression_bound(row, 16) for row in scalings],
            "charged_selection": [charged_packet_menu_bound(scalings[2], packet_choices=16 ** 4),
                                  charged_packet_menu_bound(scalings[2], original_pool_states=16 ** 4)],
            "rare_source_global_plane_countercontrol": {
                "labels": [[1, 1, 1, 1]], "modulus_bits": 2,
                "anchor_zero_has_a_plane": False,
                "other_fibers_have_planes": True,
                "constant_planes": anchor_counter["constant_planes"],
                "incident_points": anchor_counter["incident_points"]},
            "claim_gate": {"incidence_mass_not_global_plane_absence": True,
                           "native_even_modulus_torsion_charged": True,
                           "nonlinear_terminal_charts_are_not_excluded": True,
                           "general_quantum_branch_mixing_is_not_excluded": True,
                           "full_transport_or_decoder_implemented": False,
                           "independent_theorem_review": False, "candidate_record_accepted": False,
                           "novelty_claim": False, "speedup_claim_allowed": False},
            "dependency_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (Path(__file__), ROOT / "theorems/dcp_carry_packets.py",
                                            ROOT / "theorems/dcp_dense_phase_transport.py")}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"status": report["status"], "claim_gate": report["claim_gate"],
                      "scaling_dyadic_exponents": [row[
                          "source_mean_incident_point_mass_upper_bound_dyadic_exponent"] for row in
                                                  report["native_near_density_one_scaling"]]}, indent=2))


if __name__ == "__main__":
    main()
