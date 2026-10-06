"""Native affine-cube incidence, cube-free caps and dense-tail rank gates.

LOCAL DERIVATION / REVIEW PENDING. No decoder, novelty or general DCP no-go.
Symbolic scaling does not enumerate cube vertices, patterns, states or secrets.
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
from dcp_carry_packets import binary_rank, compile_packet
from dcp_dense_phase_transport import offset_collision_witness_certificate, verify_transport_witness
from dcp_pivot_span_obstructions import _row_basis
from dcp_terminal_affine_fibers import _positive_integer, charged_packet_menu_bound

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_affine_cube_hierarchy.json"


def parity_incidence_matrix(cube_dimension, *, maximum_dimension=6):
    _positive_integer(cube_dimension, "cube dimension")
    if cube_dimension > maximum_dimension:
        raise ValueError("explicit parity matrix exceeds bounded control budget")
    return tuple(tuple((x & p).bit_count() & 1 for p in range(1, 1 << cube_dimension))
                 for x in range(1, 1 << cube_dimension))


def cube_source_bound(n, width, modulus_bits, cube_dimension, *, log_precision=32,
                      prefix_conditioned=True):
    for value, name in ((n, "output dimension"), (width, "physical width"),
                        (modulus_bits, "tested modulus bits"), (cube_dimension, "cube dimension"),
                        (log_precision, "logarithm precision")):
        _positive_integer(value, name)
    if not 2 <= cube_dimension <= width or width < n or type(prefix_conditioned) is not bool:
        raise ValueError("independent cube directions, enough physical bits and Boolean conditioning required")
    if log_precision > 4096:
        raise ValueError("explicit logarithm precision exceeds budget")
    log_numerator = ((cube_dimension + 1) ** log_precision - 1).bit_length()
    effective_bits = max(0, modulus_bits - cube_dimension + 1)
    entropy = (width * log_numerator + log_precision * cube_dimension - 1) // (log_precision * cube_dimension)
    gap = n * effective_bits - cube_dimension - entropy
    bits = cube_dimension * gap + cube_dimension ** 2 - 3 if gap >= 1 else 0
    if gap >= 1 and prefix_conditioned:
        bits -= n + 2
    bits = max(0, bits)
    return {"status": "NATIVE_AFFINE_CUBE_INCIDENT_POINT_MASS_SOURCE_UPPER_BOUND",
            "dimension": n, "physical_width": width, "tested_modulus_bits": modulus_bits,
            "cube_dimension": cube_dimension,
            "parity_kernel_uniform_points_and_invertible_binary_prefix_conditioned": prefix_conditioned,
            "pattern_sum_divisibility_bits": effective_bits,
            "log2_cube_dimension_plus_one_upper_bound_numerator": log_numerator,
            "log2_cube_dimension_plus_one_upper_bound_denominator": log_precision,
            "per_pattern_assignment_entropy_bits_upper_bound": entropy,
            "per_pattern_probability_gap_bits": gap,
            "cube_basis_multiplicity_lower_bound": f"2^({cube_dimension ** 2}-2)",
            "source_mean_incident_point_mass_upper_bound_dyadic_exponent": bits,
            "source_mean_incident_point_mass_upper_bound": f"2^-{bits}",
            "conditioning_factor_upper_bound": f"2^{n + 2}" if prefix_conditioned else "1",
            "nonempty_pattern_groups_and_independent_modular_sums_required": True,
            "all_patterns_or_cube_vertices_enumerated_by_scaling_ledger": False,
            "all_high_label_adaptive_cube_choices_within_packet_covered": True,
            "global_cube_absence_or_this_packet_classification_proved": False,
            "nonlinear_blocks_interblock_mixing_or_unknown_trash_excluded": False,
            "independent_theorem_review": False, "candidate_record_accepted": False,
            "novelty_claim": False, "speedup_claim_allowed": False}


def finite_pattern_menu_bound(n, width, modulus_bits, cube_dimension, *, prefix_conditioned=True):
    """Finite combinatorial calibration; NEVER the growing-dimension evaluator."""
    if not (all(type(x) is int for x in (n, width, modulus_bits, cube_dimension)) and
            2 <= cube_dimension <= 5 and
            type(width) is int and max(n, cube_dimension) <= width <= 64 and
            type(n) is int and n >= 1 and type(modulus_bits) is int and modulus_bits >= 1 and
            n * modulus_bits <= 512 and type(prefix_conditioned) is bool):
        raise ValueError("bounded pattern-menu calibration parameters required")
    r, J = cube_dimension, (1 << cube_dimension) - 1
    exponent = max(0, modulus_bits - r + 1)
    basis_count = math.prod((1 << r) - (1 << i) for i in range(r))
    bound = sum((Fraction(math.comb(J, h) * (h + 1) ** width, 1 << (n * h * exponent))
                 for h in range(r, min(width, J) + 1)), Fraction(0)) / basis_count
    if prefix_conditioned:
        prefix = math.prod(1 - Fraction(1, 1 << j) for j in range(1, n + 1))
        bound *= (1 << n) / prefix
    return min(Fraction(1), bound)


def cube_free_cap_exact(tail_bits, cube_dimension, *, maximum_tail_bits=128):
    if type(tail_bits) is not int or not 0 <= tail_bits <= maximum_tail_bits:
        raise ValueError("bounded nonnegative tail dimension required")
    _positive_integer(cube_dimension, "cube dimension")
    if cube_dimension > tail_bits:
        return 1 << tail_bits
    cap = 1
    for r in range(2, cube_dimension + 1):
        d = tail_bits - cube_dimension + r
        cap = min(1 << d, (1 + math.isqrt(1 + 8 * ((1 << d) - 1) * cap)) // 2)
    return cap


def cube_free_cap_density(tail_bits, cube_dimension):
    _positive_integer(tail_bits, "tail bits")
    _positive_integer(cube_dimension, "cube dimension")
    if cube_dimension > tail_bits:
        bits = 0
    elif cube_dimension == 1:
        bits = tail_bits
    else:
        bits = max(0, ((tail_bits - cube_dimension + 1) >> (cube_dimension - 1)) - 1)
    return {"tail_bits": tail_bits, "cube_dimension": cube_dimension,
            "cube_free_fiber_density_upper_bound_dyadic_exponent": bits,
            "cube_free_fiber_density_upper_bound": f"2^-{bits}",
            "cube_dimension_fits_inside_tail": cube_dimension <= tail_bits,
            "exponential_cube_vertex_or_cap_enumeration_used": False}


def _two_term_below_two_thirds(a, b):
    return min(a, b) >= 2 or (min(a, b) == 1 and max(a, b) >= 3)


def cube_tail_compression_bound(source_ledger, tail_bits, *, target_rank=1):
    _positive_integer(target_rank, "effective target projector rank")
    width, n = source_ledger["physical_width"], source_ledger["dimension"]
    available = width - n if source_ledger[
        "parity_kernel_uniform_points_and_invertible_binary_prefix_conditioned"] else width
    if type(tail_bits) is not int or not 1 <= tail_bits <= available or (target_rank - 1).bit_length() > tail_bits:
        raise ValueError("valid physical affine tail and target rank required")
    cap = cube_free_cap_density(tail_bits, source_ledger["cube_dimension"])
    rank_bits = max(0, cap["cube_free_fiber_density_upper_bound_dyadic_exponent"] - (target_rank - 1).bit_length())
    source_bits = source_ledger["source_mean_incident_point_mass_upper_bound_dyadic_exponent"]
    return {"status": "HIGHER_CUBE_PHYSICAL_AFFINE_CLEAN_TAIL_COMPRESSION_GATE",
            "cube_dimension": source_ledger["cube_dimension"], "physical_tail_bits": tail_bits,
            "effective_target_projector_rank": target_rank, "cap_density": cap,
            "rank_adjusted_nonincident_probability_dyadic_exponent": rank_bits,
            "source_exception_probability_dyadic_exponent": source_bits,
            "uniform_secret_source_mean_acceptance_upper_bound": f"min(1,2^-{rank_bits}+2^-{source_bits})",
            "conservative_single_dyadic_exponent": max(0, min(rank_bits, source_bits) - 1),
            "uniform_secret_source_mean_acceptance_proved_below_two_thirds": _two_term_below_two_thirds(rank_bits, source_bits),
            "blocks_are_physical_binary_affine_equal_size_and_public_label_selected": True,
            "clean_workspace_or_entire_effective_projector_rank_charged": True,
            "secret_dependent_discarded_trash_or_interblock_mixing_covered": False,
            "secret_informative_prior_measurements_covered": False,
            "mean_is_a_fixed_secret_or_instance_guarantee": False,
            "full_quantum_decoder_ruled_out": False, "candidate_record_accepted": False,
            "independent_theorem_review": False, "speedup_claim_allowed": False}


def _validate_parity_rows(rows, width):
    if type(width) is not int or width < 1:
        raise ValueError("positive physical width required")
    rows = tuple(rows)
    if not rows or any(type(b) is not int or not 0 < b < 1 << width for b in rows) or binary_rank(rows, width) != len(rows):
        raise ValueError("nonempty independent binary parity rows required")
    return rows


def half_width_rank_gate(parity_rows, width, tail_bits):
    R = _validate_parity_rows(parity_rows, width)
    n = len(R)
    if type(tail_bits) is not int or not 1 <= tail_bits <= width - n:
        raise ValueError("tail fits in physical parity kernel required")
    active = 0
    for b in R:
        active |= b
    zeros = width - active.bit_count()
    gap = 2 * tail_bits - width - zeros
    half_rank = max(0, (gap + 2 * n - 1) // (2 * n))
    return {"status": "PER_INSTANCE_ALL_PHYSICAL_AFFINE_PARITY_BLOCK_QUADRATIC_RANK_GATE",
            "parity_rows_hex": [hex(b) for b in R], "dimension": n,
            "physical_width": width, "physical_affine_tail_bits": tail_bits,
            "zero_binary_columns": zeros,
            "maximum_common_isotropic_physical_dimension_upper_bound": (width + zeros) // 2,
            "generic_diagonal_restriction_rank_lower_bound": max(0, gap),
            "some_actual_scalar_carry_polar_rank_lower_bound": 2 * half_rank,
            "scalar_carry_bias_exponent_lower_bound": half_rank,
            "uniform_secret_rank_one_clean_tail_acceptance_upper_bound": f"1/2+2^-{half_rank + 1}",
            "all_tail_dimensional_physical_affine_full_modulus_fibers_excluded": gap > 0,
            "modulus_divisible_by_four_and_parity_coset_required": True,
            "generic_field_extension_is_only_a_rank_proof_not_a_physical_oracle": True,
            "all_higher_label_adaptive_physical_affine_blocks_covered": True,
            "some_output_row_can_depend_on_block_but_not_unknown_secret": True,
            "rank_two_clean_targets_or_unknown_trash_decoders_excluded": False,
            "nonlinear_physical_charts_or_interblock_mixing_excluded": False,
            "per_instance_gate_is_a_per_secret_success_bound": False,
            "secret_informative_prior_measurements_covered": False,
            "candidate_record_accepted": False, "independent_theorem_review": False,
            "novelty_claim": False, "speedup_claim_allowed": False}


def selected_block_polar_certificate(parity_rows, width, directions):
    R = _validate_parity_rows(parity_rows, width)
    W = tuple(directions)
    if not W or len(_row_basis(W, width)) != len(W) or any((b & w).bit_count() & 1 for b in R for w in W):
        raise ValueError("independent physical directions inside parity kernel required")
    gate = half_width_rank_gate(R, width, len(W))
    matrices = [tuple(sum(((b & u & v).bit_count() & 1) << j for j, v in enumerate(W)) for u in W) for b in R]
    ranks = [binary_rank(M, len(W)) for M in matrices]
    assert all(rank % 2 == 0 for rank in ranks)
    assert max(ranks) >= gate["some_actual_scalar_carry_polar_rank_lower_bound"]
    return {"parity_rows_hex": [hex(b) for b in R], "physical_width": width,
            "physical_directions_hex": [hex(w) for w in W],
            "actual_scalar_polar_matrices_hex": [[hex(x) for x in M] for M in matrices],
            "actual_scalar_polar_ranks": ranks, "all_block_gate": gate}


def dense_half_width_source_bound(n, width, modulus_bits):
    for value, name in ((n, "dimension"), (width, "physical width"), (modulus_bits, "full modulus bits")):
        _positive_integer(value, name)
    tail = width - n * modulus_bits
    if modulus_bits < 2 or tail < 2:
        raise ValueError("full modulus divisible by four and at least two surplus bits required")
    gap = 2 * tail - width
    zero_budget = max(0, gap // 2)
    half_rank = max(0, (gap - zero_budget + 2 * n - 1) // (2 * n))
    zero_probability = (Fraction(0) if zero_budget >= width - n else
                        min(Fraction(1), Fraction(width - n, (zero_budget + 1) * (1 << n))))
    comparison_bias_bits = min(half_rank + 1, 64)
    bound_for_threshold = min(Fraction(1), Fraction(1, 2) + Fraction(1, 1 << comparison_bias_bits) + zero_probability)
    return {"status": "NATIVE_DENSE_PHYSICAL_AFFINE_TAIL_QUADRATIC_RANK_SOURCE_GATE",
            "dimension": n, "physical_width": width, "full_modulus_bits": modulus_bits,
            "terminal_physical_tail_bits": tail, "allowed_zero_binary_columns": zero_budget,
            "on_good_sources_scalar_carry_bias_exponent_lower_bound": half_rank,
            "native_tail_zero_column_count_mean": exact(Fraction(width - n, 1 << n)),
            "probability_zero_column_budget_exceeded_upper_bound": exact(zero_probability),
            "uniform_secret_source_mean_rank_one_clean_acceptance_upper_bound": f"min(1,1/2+2^-{half_rank + 1}+zero_budget_probability)",
            "conservatively_rounded_acceptance_bound_for_two_thirds_comparison": exact(bound_for_threshold),
            "uniform_secret_source_mean_acceptance_proved_below_two_thirds": bound_for_threshold < Fraction(2, 3),
            "tail_binary_labels_independent_of_accepted_prefix": True,
            "prefix_conditioning_probability_reused_as_independence_assumption": False,
            "some_zero_columns_are_allowed_not_exponentially_filtered_away": True,
            "zero_tail_count_bound_is_markov_not_seed_estimation": True,
            "rank_two_targets_unknown_trash_or_general_decoder_ruled_out": False,
            "candidate_record_accepted": False, "independent_theorem_review": False,
            "novelty_claim": False, "speedup_claim_allowed": False}


def best_cube_gate(n, width, modulus_bits, *, maximum_cube_dimension=32):
    tail = width - n * modulus_bits
    if tail < 2 or type(maximum_cube_dimension) is not int or maximum_cube_dimension < 2:
        raise ValueError("positive cube design menu and terminal surplus at least two required")
    records = []
    for r in range(2, min(tail, modulus_bits, maximum_cube_dimension) + 1):
        source = cube_source_bound(n, width, modulus_bits, r)
        compression = cube_tail_compression_bound(source, tail)
        records.append({"source": source, "compression": compression})
    if not records:
        raise ValueError("tested modulus too small for cube menu")
    best = max(records, key=lambda row: (row["compression"]["conservative_single_dyadic_exponent"],
                                        row["compression"]["uniform_secret_source_mean_acceptance_proved_below_two_thirds"],
                                        row["source"]["source_mean_incident_point_mass_upper_bound_dyadic_exponent"]))
    return {"dimension": n, "physical_width": width, "full_modulus_bits": modulus_bits,
            "terminal_tail_bits": tail, "tested_cube_dimensions": len(records),
            "best_deterministic_design_gate": best,
            "choosing_minimum_of_valid_bounds_assumes_independence": False,
            "menu_search_is_a_quantum_algorithm_candidate": False}


def phase_separation_countercontrol():
    """Actual packet showing that clean fixed junk is NOT necessary for readout."""
    packet = compile_packet(((1, 1, 2, 4, 2, 4),), 8)
    permutation = tuple((j & 1) | (t << 1) | ((j >> 1) << 3) for j in range(8) for t in range(4))
    assert sorted(permutation) == list(range(32))
    offsets = [(j & 1) + (j >> 1 & 1) + 2 * (j >> 2 & 1) for j in range(8)]
    offsets = [c % 4 for c in offsets]
    for j, c in enumerate(offsets):
        for t in range(4):
            assert packet.residual(permutation[t + 4 * j]) == ((t + c) % 4,)
            for challenge in range(4):
                assert verify_transport_witness(packet, permutation, (challenge,), (t,), j) is not None
    histogram = [offsets.count(c) for c in range(4)]
    flat_tail_mass = Fraction(sum(c * c for c in histogram), 64)
    baseline = offset_collision_witness_certificate(packet, permutation)
    assert baseline["uniform_secret_mean_QFT_decoder_success"] == exact(Fraction(1))
    return {"status": "CALIBRATION_COUNTERCONTROL_NOT_NATIVE_SCALABLE_ALGORITHM",
            "labels": packet.labels, "modulus": 8,
            "logical_permutation": permutation, "junk_offsets": offsets,
            "phase_identity": "F(P(t,j))=t+c(j) mod4; QFT(t) decodes, junk need not be flattened",
            "exact_QFT_success_for_every_secret": exact(Fraction(1)),
            "uniform_secret_mean_flat_junk_projection_probability": exact(flat_tail_mass),
            "independent_uniform_target_two_call_witness_baseline": baseline,
            "verified_challenge_reference_junk_trials": 128,
            "literal_label_table_conditional_native_prefix_probability": exact(Fraction(1, 1 << 17)),
            "clean_fixed_junk_is_necessary_for_a_DCP_decoder": False,
            "source_prevalence_or_growing_dimension_decoder_proved": False,
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def run_controls():
    inverse_controls = []
    for r in range(1, 6):
        P = parity_incidence_matrix(r)
        J = len(P)
        for i in range(J):
            for j in range(J):
                assert sum(P[i][k] * (2 * P[j][k] - 1) for k in range(J)) == (1 << (r - 1)) * (i == j)
        inverse_controls.append({"cube_dimension": r, "parity_matrix_size": J,
                                 "integer_inverse_numerator_entries_are_plus_or_minus_one": True,
                                 "inverse_denominator": 1 << (r - 1), "checked_product_entries": J * J})
    pattern_controls = []
    for r, a in ((2, 3), (3, 2)):
        P = parity_incidence_matrix(r)
        Q, successes = 1 << a, 0
        for sums in itertools.product(range(Q), repeat=len(P)):
            if all(sum(x * s for x, s in zip(row, sums)) % Q == 0 for row in P):
                successes += 1
                assert all((s << (r - 1)) % Q == 0 for s in sums)
        pattern_controls.append({"cube_dimension": r, "modulus_bits": a,
                                 "all_nonzero_patterns_present": True,
                                 "complete_pattern_sum_tables": Q ** len(P), "flat_tables": successes,
                                 "exact_full_pattern_flatness_probability": exact(Fraction(successes, Q ** len(P))),
                                 "divisibility_necessary_probability_bound": exact(Fraction(1, 1 << (len(P) * max(a - r + 1, 0))))})
    profiles = []
    old = json.loads((ROOT / "research/phase_workbench/dcp_pivot_span_obstructions.json").read_text())
    for record in old["systematic_actual_packet_operator_profiles"]:
        A = record["provenance"]["labels"]
        R = tuple(sum((a & 1) << i for i, a in enumerate(row)) for row in A)
        W = tuple(int(x, 16) for x in record["physical_code_schur_certificate"]["physical_pivot_directions_hex"])
        profiles.append(selected_block_polar_certificate(R, len(A[0]), W))
    regimes = [(16, 1300, 65), (16, 2080, 65), (32, 8256, 129),
               (64, 32896, 257), (32, 12384, 129), (64, 49344, 257),
               (64, 65792, 257), (1024, 4 * 1024 * 4097, 4097)]
    regrouping_source = cube_source_bound(32, 8256, 129, 6)
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING",
            "parity_inverse_controls": inverse_controls, "complete_pattern_sum_controls": pattern_controls,
            "cube_source_and_compression_scaling": [best_cube_gate(*parameters) for parameters in regimes],
            "dense_half_width_source_scaling": [dense_half_width_source_bound(n, rho * n * (4 * n + 1), 4 * n + 1)
                                                for n, rho in ((8, 3), (16, 3), (32, 3), (64, 3), (64, 4), (64, 64))],
            "actual_packet_selected_polar_controls": profiles,
            "phase_separation_countercontrol": phase_separation_countercontrol(),
            "charged_cube_packet_menu_controls": [charged_packet_menu_bound(regrouping_source, packet_choices=32 ** 4),
                                                  charged_packet_menu_bound(regrouping_source, original_pool_states=32 ** 4)],
            "claim_gate": {"constant_density_escape_is_not_established_by_vacuous_two_plane_bound": True,
                           "clean_physical_affine_tail_architecture_only": True,
                           "nonlinear_blocks_interblock_mixing_unknown_trash_still_open": True,
                           "rank_two_clean_targets_not_excluded_by_half_width_gate": True,
                           "clean_fixed_junk_is_required_by_general_decoder": False,
                           "independent_theorem_review": False, "candidate_record_accepted": False,
                           "new_decoder_or_speedup": False, "novelty_claim": False},
            "dependency_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (Path(__file__), ROOT / "theorems/dcp_terminal_affine_fibers.py",
                                            ROOT / "theorems/dcp_pivot_span_obstructions.py",
                                            ROOT / "theorems/dcp_dense_phase_transport.py",
                                            ROOT / "research/phase_workbench/dcp_pivot_span_obstructions.json")}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"status": report["status"], "claim_gate": report["claim_gate"],
                      "best_cube_dimensions": [r["best_deterministic_design_gate"]["source"]["cube_dimension"]
                                               for r in report["cube_source_and_compression_scaling"]],
                      "compression_exponents": [r["best_deterministic_design_gate"]["compression"]["conservative_single_dyadic_exponent"]
                                                for r in report["cube_source_and_compression_scaling"]]}, indent=2))


if __name__ == "__main__":
    main()
