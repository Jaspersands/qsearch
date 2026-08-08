from fractions import Fraction

import numpy as np
import pytest

from self_dual_wreath_component_povm_regular_master_reduction import (
    audit_canonical_component_effects,
    canonical_component_effects,
    enumerate_source_block_defects,
    run_component_povm_regular_master_reduction,
)
from self_dual_wreath_partial_support_child_embedding import (
    audit_partial_support_child_embedding,
)


def test_canonical_full_domain_effects_match_leaf_coefficient_effects() -> None:
    standard = (2, 1)
    labels = ((standard, standard), (standard, standard))
    canonical = audit_canonical_component_effects(
        "canonical",
        (1, 1, 1),
        labels,
        (0, 1),
        (2, 3),
    )
    coefficient = audit_partial_support_child_embedding(
        "coefficient",
        3,
        (1, 1, 1),
        labels,
        (0, 1),
        (2, 3),
    )

    coefficient_spectra = []
    for record in coefficient.component_effects:
        # This control has the exact spectrum {0, 1/2, 1/2, 1/2, 1}.
        assert record.support_rank == 4
        coefficient_spectra.append((0.0, 0.5, 0.5, 0.5, 1.0))
    assert canonical.common_span_dimension == coefficient.common_span_dimension == 5
    assert canonical.canonical_full_domain_effects_verified
    assert canonical.matrix_partial_support_required
    for observed, expected in zip(
        canonical.component_effect_spectra,
        coefficient_spectra,
    ):
        assert observed == pytest.approx(expected)


def test_canonical_component_effects_sum_to_identity_on_each_child() -> None:
    standard = (2, 1)
    ambient, rank, sides = canonical_component_effects(
        (1, 1, 1),
        ((standard, standard), (standard, standard)),
        (0, 1),
        (2, 3),
    )
    assert ambient == 16
    assert rank == 5
    for side in sides:
        assert np.linalg.norm(sum(side) - np.eye(rank), ord=2) < 1e-12


def test_regular_master_mass_accounting_distinguishes_three_masses() -> None:
    records, mass = enumerate_source_block_defects(
        3,
        (1, 1, 1),
        (0, 1),
        (2, 3),
    )
    assert len(records) == 81
    assert mass.exact_regular_dimension_accounting_verified
    assert mass.exact_central_support_mass_accounting_verified
    assert Fraction(mass.total_source_probability) == 1
    assert Fraction(mass.matrix_effect_source_probability) == Fraction(16, 81)
    assert Fraction(mass.matrix_effect_physical_common_span_mass) == Fraction(5, 81)
    assert mass.ordinary_scalar_defect_trace_mass == pytest.approx(2 / 81)
    assert mass.matrix_source_to_physical_common_mass_ratio == pytest.approx(16 / 5)
    assert mass.matrix_physical_common_to_scalar_defect_mass_ratio == pytest.approx(5 / 2)
    assert mass.matrix_effect_source_block_count == 1
    assert mass.globally_distinct_matrix_effect_source_block_count == 0


def test_report_opens_center_valued_problem_without_natural_promotion() -> None:
    report = run_component_povm_regular_master_reduction()
    assert report.claim_gate[
        "canonical_component_effects_are_regular_master_decomposable"
    ]
    assert report.claim_gate[
        "matrix_effect_source_probability_is_central_support_trace"
    ]
    assert report.claim_gate[
        "matrix_effect_physical_common_mass_is_common_cutdown_trace"
    ]
    assert not report.claim_gate[
        "ordinary_scalar_moments_control_bad_block_probability"
    ]
    assert not report.claim_gate[
        "low_dimension_source_cut_removes_all_low_internal_carriers"
    ]
    assert not report.claim_gate[
        "globally_distinct_high_dimension_matrix_effect_mass_controlled"
    ]
    assert not report.claim_gate["natural_sparse_support_jacobi_edge_proved"]
    assert not report.claim_gate["natural_component_support_select_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
