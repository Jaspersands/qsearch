import math

import pytest

from self_dual_wreath_component_leaf_fourier_leverage import (
    _coarse_pvm,
    _uniform_povm,
)
from self_dual_wreath_component_leaf_fourier_strata import (
    _cell_counts,
    _multinomial_count,
    _representative_masks,
    audit_leaf_fourier_strata,
    fourier_stratum_scaling_record,
    leaf_fourier_stratum_theorem,
    run_component_leaf_fourier_strata,
)


def test_venn_cells_reconstruct_masks_and_multinomial_orbit() -> None:
    masks = (0b1011, 0b0110, 0b1100)
    counts = _cell_counts(*masks, 4)
    representative = _representative_masks(counts)
    assert _cell_counts(*representative[:3], 4) == counts
    assert representative[3] == representative[0] ^ representative[1] ^ representative[2]
    assert _multinomial_count(counts) >= 1


def test_uniform_profile_reduces_exactly_to_polynomial_strata() -> None:
    row = audit_leaf_fourier_strata(
        "UNIFORM",
        "uniform",
        _uniform_povm(3, 2),
    )
    assert row.exact_annealed_fourier_stratum_reduction_verified
    assert row.observed_stratum_count == math.comb(10, 7)
    assert row.xor_surviving_word_count == 8**3
    assert row.direct_average_leaf_normalized_fourth_moment == pytest.approx(1 / 8**4)
    assert row.walsh_xor_residual < 1e-12


def test_asymmetric_coarse_profile_uses_translation_average_not_base_leaf() -> None:
    row = audit_leaf_fourier_strata(
        "COARSE",
        "coarse",
        _coarse_pvm(4, 2),
    )
    assert row.exact_annealed_fourier_stratum_reduction_verified
    assert row.translation_orbit_averaged_fixed_leaf_normalized_fourth_moment == pytest.approx(
        row.direct_average_leaf_normalized_fourth_moment
    )
    assert row.strata_reconstructed_normalized_fourth_moment_real == pytest.approx(
        row.direct_average_leaf_normalized_fourth_moment
    )


def test_scaling_is_degree_seven_instead_of_exponential_word_count() -> None:
    row = fourier_stratum_scaling_record(128)
    assert row.surviving_fourier_word_count_log2 == 384
    assert row.exact_stratum_count == math.comb(135, 7)
    assert row.stratum_count_polynomial_degree == 7
    assert row.log2_stratum_count < 64
    assert row.exponential_word_enumeration_removed
    assert not row.natural_representative_word_bound_proved


def test_invalid_cell_counts_and_cube_dimension_are_rejected() -> None:
    with pytest.raises(ValueError, match="eight"):
        _representative_masks((1, 2))
    with pytest.raises(ValueError, match="positive"):
        fourier_stratum_scaling_record(0)


def test_report_preserves_word_bound_M4_and_speedup_gates() -> None:
    report = run_component_leaf_fourier_strata()
    assert report.headline_metrics[
        "annealed_leaf_fourier_stratum_reduction_theorem_count"
    ] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["annealed_non_xor_fourier_words_cancel"]
    assert report.claim_gate["surviving_words_reduce_to_polynomial_venn_strata"]
    assert not report.claim_gate[
        "natural_representative_stratum_words_controlled"
    ]
    assert not report.claim_gate[
        "natural_fixed_leaf_diagonal_green_moment_controlled"
    ]
    assert not report.claim_gate["natural_component_M4_positive"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_theorem_allows_invariant_conditioning_and_physical_weight() -> None:
    theorem = leaf_fourier_stratum_theorem()
    assert theorem.theorem_verified
    assert theorem.arbitrary_flip_and_coordinate_invariant_law
    assert theorem.arbitrary_invariant_event_and_scalar_weight
    assert "binom(m+7,7)" in theorem.stratum_count
