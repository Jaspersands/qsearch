from fractions import Fraction

from self_dual_wreath_occupied_carrier_octahedral_boundary import (
    LIVE_DIFFERENCES,
    audit_dense_occupied_compatibility,
    audit_octahedral_family,
    natural_mass_boundary_record,
    run_occupied_carrier_octahedral_boundary,
    write_occupied_carrier_octahedral_boundary_report,
)


def test_exact_octahedral_family_formulas_scale() -> None:
    for n in (5, 6, 8, 12):
        row = audit_octahedral_family(n)
        assert row.exact_family_formula_verified is True
        assert row.live_differences == LIVE_DIFFERENCES
        assert row.live_core_ranks == (
            (n - 1) ** 2,
            n - 1,
            (n - 1) ** 2,
            n - 1,
            (n - 1) ** 2,
            n - 1,
        )
        assert row.nonopposite_overlap_count == 12
        assert row.opposite_zero_overlap_count == 3
        assert row.correlation_denominator == n * (n - 1) * (n - 3) // 2
        assert row.octahedral_channel_multiplicity == n - 1
        assert row.triangle_channel_multiplicity == (n - 1) * (n - 2)
        assert row.total_coefficient_dimension == 3 * n * (n - 1)


def test_dense_occupied_labels_commute_but_clique_normalization_fails() -> None:
    row = audit_dense_occupied_compatibility()
    assert row.dense_control_verified is True
    assert row.occupied_support_projectors_commute is True
    assert row.support_projector_commutator_norm < 1e-10
    assert row.extracted_channel_count == 2
    assert row.octahedral_channel_multiplicity == 4
    assert row.triangle_channel_multiplicity == 12
    assert row.clique_path_composition_residual > 0.9
    assert abs(row.unit_correlation_minimum_eigenvalue + 1) < 1e-10
    assert row.unit_correlation_negative_eigenvalue_count == 8
    assert row.physical_gram_positive is True
    assert abs(row.physical_gram_minimum_eigenvalue - 0.9) < 1e-12


def test_conditional_trace_mass_is_not_natural_source_mass() -> None:
    rows = [natural_mass_boundary_record(n) for n in (5, 8, 16, 32)]
    assert all(row.repeats_source_partitions for row in rows)
    assert all(row.excluded_by_global_distinct_typical_event for row in rows)
    assert all(not row.positive_natural_mass_proved for row in rows)
    assert [row.conditional_octahedral_trace_mass for row in rows] == [
        2 / n for n in (5, 8, 16, 32)
    ]
    masses = [Fraction(row.full_control_mass) for row in rows]
    assert all(right < left for left, right in zip(masses, masses[1:]))


def test_report_keeps_collision_free_claims_blocked() -> None:
    report = run_occupied_carrier_octahedral_boundary()
    assert report.claim_gate[
        "all_n_occupied_octahedral_channel_formula_proved"
    ] is True
    assert report.claim_gate[
        "occupied_repeated_family_support_projectors_commute"
    ] is True
    assert report.claim_gate[
        "commuting_occupied_supports_force_clique_channels"
    ] is False
    assert report.claim_gate[
        "repeated_octahedral_family_has_positive_natural_mass"
    ] is False
    assert report.claim_gate[
        "collision_free_typical_occupied_projectors_commute_all_depth"
    ] is False
    assert report.claim_gate["speedup_claim_allowed"] is False


def test_registry_writer_records_both_scope_falsifiers(tmp_path) -> None:
    payload = write_occupied_carrier_octahedral_boundary_report(
        path=tmp_path / "octahedral.json",
        write_registry=False,
    )
    assert payload["headline_metrics"][
        "all_n_octahedral_channel_formula_theorem_count"
    ] == 1
    assert payload["headline_metrics"][
        "collision_free_positive_mass_contextuality_theorem_count"
    ] == 0
    assert len(payload["falsifiers_triggered"]) >= 4
