import pytest

from coset_hyperoctahedral_trivial_color_mass_no_go import (
    audit_trivial_color_mass,
    base_subgroup_element,
    build_trivial_color_mass_report,
    exact_trivial_color_source_fraction,
    normalized_fiber_character,
    trivial_color_mass_scaling_record,
    write_trivial_color_mass_report,
)


@pytest.mark.parametrize(
    ("half_degree", "copy_count"),
    ((1, 1), (2, 1), (2, 2), (3, 1), (3, 2)),
)
def test_direct_coset_fixed_points_match_burnside_formula(
    half_degree, copy_count
):
    control = audit_trivial_color_mass(half_degree, copy_count)
    assert control.exact_burnside_formula_verified
    assert control.direct_character_mismatch_count == 0
    assert control.source_fraction_residual == 0.0
    assert control.exact_source_fraction == pytest.approx(
        float(exact_trivial_color_source_fraction(half_degree, copy_count))
    )


def test_middle_weight_gets_exact_twisted_fixed_point_term():
    assert normalized_fiber_character(2, 1) == pytest.approx(1 / 3)
    assert normalized_fiber_character(3, 1) == pytest.approx(1 / 15)
    assert normalized_fiber_character(3, 2) == pytest.approx(1 / 45)
    assert base_subgroup_element(2, 3) == (1, 0, 3, 2)

    with pytest.raises(ValueError, match="invalid"):
        normalized_fiber_character(2, 3)
    with pytest.raises(ValueError, match="invalid"):
        base_subgroup_element(2, 4)


def test_trivial_color_alternative_mass_vanishes_at_flatness_width():
    rows = [
        trivial_color_mass_scaling_record(m)
        for m in (3, 4, 8, 16, 32, 64, 128)
    ]
    assert all(row.copy_count >= row.half_degree for row in rows)
    assert all(
        row.exact_source_fraction <= row.elementary_source_fraction_upper_bound
        * (1.0 + 1e-12)
        for row in rows
    )
    assert all(
        row.elementary_source_fraction_upper_bound <= 2.0 ** (1 - row.half_degree)
        for row in rows
    )
    assert all(
        not row.embedded_kronecker_sector_has_constant_alternative_mass
        for row in rows
    )
    assert all(not row.generic_wreath_cg_is_natural_source_bottleneck for row in rows)
    assert all(not row.colored_source_fusion_compiled for row in rows)
    assert rows[-1].alternative_contribution_log2_upper_bound < -60

    with pytest.raises(ValueError, match="at least two"):
        trivial_color_mass_scaling_record(1)


def test_report_redirects_search_to_colored_source_sectors(tmp_path):
    report = build_trivial_color_mass_report(
        finite_specs=((1, 1), (2, 1), (3, 1)),
        scaling_half_degrees=(3, 4, 8, 16, 32),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.exact_source_fraction_proved
    assert report.theorem.exponential_source_mass_upper_bound_proved
    assert report.theorem.exponential_alternative_mass_upper_bound_proved
    assert not report.theorem.generic_kronecker_sector_natural_bottleneck
    assert not report.theorem.source_heavy_colored_fusion_compiled
    assert not report.theorem.full_matrix_hecke_polar_compiled
    assert report.claim_gate["embedded_symmetric_kronecker_sector_negligible"]
    assert not report.claim_gate["source_heavy_colored_sectors_classified"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_trivial_color_mass_report(
        tmp_path / "trivial-color.json",
        finite_specs=((1, 1), (2, 1)),
        scaling_half_degrees=(3, 4, 8),
    )
    assert payload["status"] == (
        "embedded-kronecker-sector-negligible-colored-transfer-open"
    )
    assert payload["headline_metrics"][
        "source_heavy_colored_fusion_compiler_count"
    ] == 0
