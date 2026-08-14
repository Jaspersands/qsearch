from fractions import Fraction

import pytest

from self_dual_wreath_disjoint_grid_recoupling_falsifier import (
    FIRST_PAIR,
    LABELS,
    SECOND_PAIRS,
    TARGET,
    audit_disjoint_grid_recoupling,
    run_disjoint_grid_recoupling_falsifier,
    write_disjoint_grid_recoupling_falsifier_report,
)


def test_primary_grid_strictly_contracts_below_waist_bound() -> None:
    row = audit_disjoint_grid_recoupling(
        "PRIMARY",
        TARGET,
        LABELS,
        FIRST_PAIR,
        SECOND_PAIRS[0],
    )

    assert row.occupied_grid_cell_count == 9
    assert row.every_occupied_cell_multiplicity_free
    assert row.first_core_rank == 1
    assert row.second_core_rank == 81
    assert row.nonzero_overlap_rank == 1
    assert Fraction(row.waist_bound_numerator, row.waist_bound_denominator) == Fraction(1, 5)
    assert row.observed_operator_norm == pytest.approx(1 / 15)
    assert row.reconstructed_operator_norm == "1/15"
    assert row.reconstructed_squared_norm == "1/225"
    assert row.waist_to_observed_ratio == pytest.approx(3.0)
    assert row.strict_waist_saturation_falsifier


def test_second_crossing_is_not_a_best_waist_dimension_formula() -> None:
    row = audit_disjoint_grid_recoupling(
        "SECONDARY",
        TARGET,
        LABELS,
        FIRST_PAIR,
        SECOND_PAIRS[1],
    )

    assert Fraction(row.waist_bound_numerator, row.waist_bound_denominator) == Fraction(1, 9)
    assert row.observed_operator_norm == pytest.approx(1 / 15)
    assert row.waist_to_observed_ratio == pytest.approx(5 / 3)
    assert row.strict_waist_saturation_falsifier


def test_pair_pairs_must_be_vertex_disjoint() -> None:
    with pytest.raises(ValueError):
        audit_disjoint_grid_recoupling(
            "INVALID",
            TARGET,
            LABELS,
            FIRST_PAIR,
            (15, 5),
        )


def test_report_kills_scalar_shortcut_without_promoting_algorithm() -> None:
    report = run_disjoint_grid_recoupling_falsifier()

    assert report.claim_gate[
        "finite_multiplicity_free_strict_grid_contraction_verified"
    ]
    assert not report.claim_gate["single_waist_bound_always_tight"]
    assert not report.claim_gate[
        "disjoint_overlap_determined_by_carrier_dimensions"
    ]
    assert report.claim_gate["full_grid_recoupling_data_required"]
    assert not report.claim_gate["exact_all_n_grid_spectrum_proved"]
    assert not report.claim_gate["coherent_grid_recoupling_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
    assert report.headline_metrics["new_quantum_algorithm_count"] == 0


def test_report_writer_materializes_standalone_artifact(tmp_path) -> None:
    path = tmp_path / "grid.json"
    payload = write_disjoint_grid_recoupling_falsifier_report(
        path=path,
        write_registry=False,
    )

    assert path.exists()
    assert payload["claim_gate"]["speedup_claim_allowed"] is False
    assert payload["headline_metrics"][
        "strict_waist_saturation_falsifier_count"
    ] == 2
