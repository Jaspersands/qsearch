import math

import pytest

from coset_hyperoctahedral_source_plancherel_typicality import (
    audit_source_plancherel,
    build_source_plancherel_report,
    nonidentity_character_bound,
    normalized_source_fiber_character,
    source_plancherel_scaling_record,
    source_plancherel_tv_upper_bound,
    write_source_plancherel_report,
)
from coset_hyperoctahedral_trivial_color_mass_no_go import (
    canonical_matching_involution,
)


@pytest.mark.parametrize("half_degree", (3, 4, 5))
def test_exact_source_character_and_wreath_plancherel_controls(half_degree):
    control = audit_source_plancherel(half_degree)
    assert control.exact_character_and_plancherel_controls_verified
    assert control.maximum_exact_nonidentity_normalized_character <= (
        control.class_size_normalized_character_bound + 1e-12
    )
    assert control.maximum_character_bound_residual == 0.0
    assert control.wreath_dimension_square_sum == control.hyperoctahedral_order
    assert control.color_mass_identity_residual < 1e-12
    assert control.conditional_product_plancherel_residual < 1e-12


def test_normalized_character_formula_handles_identity_and_hidden_element():
    m = 3
    identity = tuple(range(2 * m))
    hidden = canonical_matching_involution(m)
    assert normalized_source_fiber_character(m, identity) == 1.0
    assert normalized_source_fiber_character(m, hidden) == pytest.approx(1 / 15)
    assert nonidentity_character_bound(m) == pytest.approx(2 / 15)

    with pytest.raises(ValueError, match="wrong degree"):
        normalized_source_fiber_character(m, (0, 1))


def test_source_irrep_law_converges_rapidly_to_wreath_plancherel():
    rows = [
        source_plancherel_scaling_record(m)
        for m in (3, 4, 8, 16, 32, 64, 128)
    ]
    assert all(row.copy_count >= row.half_degree for row in rows)
    assert all(row.source_irrep_law_wreath_plancherel_typical for row in rows)
    assert all(row.uniform_wreath_qft_available for row in rows)
    assert all(not row.source_specific_matrix_hecke_polar_compiled for row in rows)
    assert rows[-1].source_irrep_to_wreath_plancherel_tv_upper_bound < 1e-100
    assert rows[-1].alternative_balanced_plancherel_mass_lower_bound > 0.999
    assert source_plancherel_tv_upper_bound(8, rows[2].copy_count) < 1e-10

    with pytest.raises(ValueError, match="at least three"):
        nonidentity_character_bound(2)
    with pytest.raises(ValueError, match="positive"):
        source_plancherel_tv_upper_bound(3, 0)


def test_report_identifies_typical_blocks_without_claiming_polar(tmp_path):
    report = build_source_plancherel_report(
        finite_half_degrees=(3, 4),
        scaling_half_degrees=(3, 4, 8, 16, 32),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.exact_normalized_character_formula_proved
    assert report.theorem.source_to_wreath_plancherel_convergence_proved
    assert report.theorem.hierarchical_plancherel_law_proved
    assert report.theorem.typical_alternative_sector_mass_proved
    assert not report.theorem.typical_sector_matrix_hecke_polar_compiled
    assert not report.theorem.hidden_involution_algorithm_constructed
    assert report.claim_gate["natural_source_wreath_plancherel_typical"]
    assert not report.claim_gate["typical_multiplicity_transfer_classified"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_source_plancherel_report(
        tmp_path / "source-plancherel.json",
        finite_half_degrees=(3,),
        scaling_half_degrees=(3, 4, 8),
    )
    assert payload["status"] == (
        "natural-source-wreath-plancherel-typical-polar-open"
    )
    assert payload["headline_metrics"][
        "typical_sector_matrix_hecke_compiler_count"
    ] == 0
