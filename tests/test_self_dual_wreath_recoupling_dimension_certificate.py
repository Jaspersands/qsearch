from fractions import Fraction

import pytest

from self_dual_wreath_recoupling_dimension_certificate import (
    audit_complete_s6_recoupling_bounds,
    recoupling_dimension_bound,
    run_recoupling_dimension_certificate,
    write_recoupling_dimension_certificate_report,
)


def test_selected_s6_block_has_exact_rank_aware_bound() -> None:
    row = recoupling_dimension_bound(
        (4, 2),
        (4, 2),
        (4, 2),
        (5, 1),
        (5, 1),
        (3, 3),
    )

    assert row.dimension_uniform
    assert row.first_swapped_rank_upper_bound == 1
    assert row.second_swapped_rank_upper_bound == 1
    assert Fraction(row.exact_best_squared_bound) == Fraction(25, 81)
    assert row.operator_norm_upper_bound == pytest.approx(5 / 9)
    assert row.nontrivial_contraction_certified


def test_absent_recoupling_block_is_rejected() -> None:
    with pytest.raises(ValueError):
        recoupling_dimension_bound(
            (6,),
            (6,),
            (6,),
            (5, 1),
            (5, 1),
            (6,),
        )


def test_complete_s6_racah_blocks_respect_dimension_certificate() -> None:
    rows = audit_complete_s6_recoupling_bounds()

    assert len(rows) == 51
    assert all(row.certificate_respected for row in rows)
    assert sum(row.nontrivial_contraction_certified for row in rows) == 24
    selected = next(
        row
        for row in rows
        if row.final_partition == (3, 3)
        and row.left_intermediate == (5, 1)
        and row.right_intermediate == (5, 1)
    )
    assert selected.actual_operator_norm == pytest.approx(1 / 3)
    assert selected.certified_operator_norm_upper_bound == pytest.approx(5 / 9)


def test_report_keeps_natural_grid_and_compiler_open() -> None:
    report = run_recoupling_dimension_certificate()

    assert report.claim_gate["dimension_uniform_6j_contraction_bound_proved"]
    assert report.claim_gate["complete_s6_racah_controls_respect_bound"]
    assert not report.claim_gate["fixed_row_assumption_required"]
    assert not report.claim_gate[
        "natural_plancherel_kronecker_rank_pressure_bounded"
    ]
    assert not report.claim_gate["generalized_3nj_grid_contraction_proved"]
    assert not report.claim_gate["coherent_recoupling_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
    assert report.headline_metrics["new_quantum_algorithm_count"] == 0


def test_report_writer_materializes_standalone_artifact(tmp_path) -> None:
    path = tmp_path / "certificate.json"
    payload = write_recoupling_dimension_certificate_report(
        path=path,
        write_registry=False,
    )

    assert path.exists()
    assert payload["headline_metrics"][
        "complete_s6_certificate_violation_count"
    ] == 0
    assert payload["claim_gate"]["speedup_claim_allowed"] is False
