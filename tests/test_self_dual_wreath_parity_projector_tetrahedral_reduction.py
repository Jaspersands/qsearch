import itertools
import math

import numpy as np

from self_dual_wreath_character_moments import permutation_cycle_type
from self_dual_wreath_alternating_parity_coset_channel import (
    parity_coset_word_likelihood_arrays,
)
from self_dual_wreath_parity_projector_tetrahedral_reduction import (
    active_rank_fraction_upper_bounds,
    audit_fully_paired_trace_energy,
    audit_parity_projector_control,
    full_plancherel_signed_support_fraction,
    parity_isotypic_operators,
    projector_rank_barrier_record,
    run_parity_projector_tetrahedral_reduction,
    young_irrep_matrices,
)
from symmetric_character import symmetric_character


def test_young_irrep_matrix_traces_match_character_table() -> None:
    for partition in ((3,), (2, 1), (1, 1, 1)):
        matrices = young_irrep_matrices(partition)
        assert len(matrices) == 6
        for permutation, matrix in matrices.items():
            expected = symmetric_character(
                partition,
                permutation_cycle_type(permutation),
            )
            assert abs(float(np.trace(matrix)) - expected) < 1e-10


def test_signed_isotypic_operators_are_orthogonal_projectors() -> None:
    partitions = ((2, 1),) * 6
    for active in ((0, 1, 3), (1, 2, 4), (0, 1, 2, 5)):
        trivial, sign = parity_isotypic_operators(partitions, active)
        assert np.linalg.norm(trivial @ trivial - trivial, ord=2) < 1e-10
        assert np.linalg.norm(sign @ sign - sign, ord=2) < 1e-10
        assert np.linalg.norm(trivial @ sign, ord=2) < 1e-10


def test_direct_parity_cosets_equal_signed_three_projector_traces() -> None:
    standard = (2, 1)
    labels = (standard,) * 6
    for parity in itertools.product((0, 1), repeat=3):
        control = audit_parity_projector_control(
            f"S3-{parity}",
            labels,
            parity,
        )
        assert control.exact_signed_projector_normal_form_verified
        assert control.projector_trace_residual < 1e-10
        assert all(
            rank <= bound + 1e-10
            for rank, bound in zip(
                control.active_support_rank_fractions,
                active_rank_fraction_upper_bounds(labels),
            )
        )


def test_projector_trace_matches_existing_parity_coset_array_axis_order() -> None:
    standard = (2, 1)
    orbits, arrays = parity_coset_word_likelihood_arrays(3)
    standard_orbit = next(index for index, orbit in enumerate(orbits) if orbit == (standard,))
    index = (standard_orbit,) * 6
    order = math.factorial(3)
    tensor_dimension = 2**6
    for parity in itertools.product((0, 1), repeat=3):
        control = audit_parity_projector_control(
            f"ARRAY-{parity}",
            (standard,) * 6,
            parity,
        )
        reconstructed = (
            (order / 2) ** 3
            * control.signed_projector_trace_average
        )
        assert abs(reconstructed - float(arrays[parity][index])) < 1e-10
        assert abs(
            control.signed_projector_trace_average
            - control.direct_coset_average
        ) < 1e-10
        assert control.tensor_dimension == tensor_dimension


def test_full_plancherel_signed_support_fraction_is_exactly_two_over_order() -> None:
    for n in range(2, 6):
        observed = full_plancherel_signed_support_fraction(n)
        assert abs(observed - 2.0 / math.factorial(n)) < 1e-12


def test_fully_paired_energy_is_sum_of_squared_projector_traces() -> None:
    s4 = audit_fully_paired_trace_energy(4, 1)
    s5 = audit_fully_paired_trace_energy(5, 1)

    assert s4.exact_tuplewise_weight_cancellation_verified
    assert s5.exact_tuplewise_weight_cancellation_verified
    assert s4.face_direct_energy == 0.0
    assert s4.opposite_direct_energy == 0.0
    assert s5.face_direct_energy > 0.0
    assert s5.opposite_direct_energy > 0.0
    assert s5.face_nonzero_trace_count == s5.retained_orbit_tuple_count
    assert s5.opposite_nonzero_trace_count == s5.retained_orbit_tuple_count
    assert not s5.finite_positive_signal_is_asymptotic_evidence


def test_rank_only_bound_is_vacuous_and_report_keeps_claim_gates_closed() -> None:
    rows = [projector_rank_barrier_record(n) for n in (10, 20, 50, 100)]
    assert all(not row.rank_only_method_certifies_decay for row in rows)
    assert all(row.rank_only_seven_sector_energy_bound_log2 > 0 for row in rows)
    assert rows[-1].rank_only_seven_sector_energy_bound_log2 > rows[0].rank_only_seven_sector_energy_bound_log2

    report = run_parity_projector_tetrahedral_reduction()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["parity_coset_signed_projector_normal_form_proved"]
    assert report.claim_gate["fully_paired_energy_is_squared_projector_trace_sum"]
    assert report.claim_gate["projector_rank_only_route_eliminated"]
    assert report.claim_gate["relative_6j_angle_estimate_required"]
    assert not report.claim_gate["canonical_face_energy_vanishes_proved"]
    assert not report.claim_gate["canonical_opposite_energy_vanishes_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]
