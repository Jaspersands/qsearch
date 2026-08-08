from fractions import Fraction

import numpy as np
import pytest

from self_dual_wreath_component_defect_rank_mass import (
    audit_component_defect_rank,
    natural_defect_rank_mass_corollary,
    natural_defect_rank_scaling_record,
    run_component_defect_rank_mass,
)


def test_binary_control_exposes_exact_defect_kernel_identity() -> None:
    first = np.diag([0.5, 1.0, 0.0]).astype(complex)
    second = np.eye(3, dtype=complex) - first
    row = audit_component_defect_rank(
        "BINARY-KERNEL",
        (first, second),
        coordinate_block_dimensions=(2, 2),
    )

    assert row.component_ranks == (2, 2)
    assert row.observed_defect_nullity == 1
    assert row.observed_defect_rank == 2
    assert row.theorem_defect_rank_lower_bound == 1
    assert row.coordinate_block_defect_rank_lower_bound == 1
    assert row.defect_kernel_intersection_residual == 0
    assert row.exact_defect_rank_bridge_verified is True


def test_low_rank_components_force_large_defect_rank_without_edge_input() -> None:
    effects = []
    for index in range(4):
        effect = np.zeros((8, 8), dtype=complex)
        effect[2 * index : 2 * index + 2, 2 * index : 2 * index + 2] = np.eye(2)
        effects.append(effect)
    row = audit_component_defect_rank(
        "PROJECTIVE-RANK2",
        tuple(effects),
        coordinate_block_dimensions=(2, 2, 2, 2),
    )

    assert row.minimum_positive_trace_component_rank == 2
    assert row.theorem_defect_rank_lower_bound == 6
    assert row.observed_defect_rank == 8
    assert row.defect_has_positive_spectral_gap is True
    assert row.exact_defect_rank_bridge_verified is True


def test_natural_mass_constants_follow_from_final_root_theorem() -> None:
    row = natural_defect_rank_mass_corollary()

    assert Fraction(row.conditioned_source_event_mass_lower_bound) == Fraction(1, 9)
    assert Fraction(row.common_span_relative_carrier_rank_lower_bound) == Fraction(19, 128)
    assert Fraction(row.component_block_to_fiber_coefficient) == Fraction(520, 19)
    assert Fraction(
        row.conditioned_expected_physical_defect_support_mass_lower_bound
    ) == Fraction(19, 1152)
    assert row.natural_positive_component_edge_required_for_support_mass is False
    assert row.natural_positive_component_edge_proved is False


def test_defect_relative_rank_converges_to_one_with_component_count() -> None:
    small = natural_defect_rank_scaling_record(32)
    large = natural_defect_rank_scaling_record(1 << 20)

    assert 0 < small.defect_relative_common_fiber_rank_lower_bound < 1
    assert large.defect_relative_common_fiber_rank_lower_bound > 0.9999
    assert large.conditioned_expected_physical_defect_support_mass_lower_bound > 0.016
    assert large.positive_component_edge_assumed is False


def test_report_resolves_mass_but_keeps_spectral_and_algorithm_gates_closed() -> None:
    report = run_component_defect_rank_mass()

    assert report.status == (
        "natural-component-defect-rank-and-mass-proved-spectral-edge-open"
    )
    assert report.claim_gate[
        "center_valued_natural_component_nonscalarity_source_mass_controlled"
    ] is True
    assert report.claim_gate[
        "natural_component_defect_has_constant_physical_support_mass"
    ] is True
    assert report.claim_gate["natural_positive_component_edge_proved"] is False
    assert report.claim_gate["coherent_component_povm_dilation_compiled"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
    assert report.headline_metrics[
        "natural_component_defect_positive_source_mass_theorem_count"
    ] == 1


def test_invalid_coordinate_rank_claim_is_rejected() -> None:
    with pytest.raises(ValueError, match="exceeds"):
        audit_component_defect_rank(
            "INVALID-BLOCK",
            (np.eye(2, dtype=complex),),
            coordinate_block_dimensions=(1,),
        )
