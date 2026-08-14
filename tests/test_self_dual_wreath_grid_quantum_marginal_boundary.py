import math

import pytest

from self_dual_wreath_disjoint_grid_recoupling_falsifier import (
    FIRST_PAIR,
    LABELS,
    SECOND_PAIRS,
    TARGET,
)
from self_dual_wreath_grid_quantum_marginal_boundary import (
    audit_generalized_recoupling_control,
    growing_row_prefactor_record,
    run_grid_quantum_marginal_boundary,
    weyl_dimension_upper_bound_log2,
    write_grid_quantum_marginal_boundary_report,
)


def test_disjoint_core_norm_is_recoupling_block_norm() -> None:
    row = audit_generalized_recoupling_control(
        "PRIMARY",
        TARGET,
        LABELS,
        FIRST_PAIR,
        SECOND_PAIRS[0],
    )

    assert row.row_coupled_dimension == 1
    assert row.column_coupled_dimension == 81
    assert row.recoupling_block_rank == 1
    assert row.recoupling_operator_norm == pytest.approx(1 / 15)
    assert row.row_projector_product_norm == pytest.approx(1 / 15)
    assert row.projector_recoupling_norm_residual < 1e-14
    assert row.row_basis_isometry_residual < 1e-12
    assert row.column_basis_isometry_residual < 1e-12
    assert row.generalized_recoupling_identity_verified


def test_weyl_prefactor_has_quadratic_row_exponent() -> None:
    n = 1024

    assert weyl_dimension_upper_bound_log2(n, 1) == 0
    assert weyl_dimension_upper_bound_log2(n, 4) == pytest.approx(
        6 * math.log2(n + 4)
    )
    with pytest.raises(ValueError):
        weyl_dimension_upper_bound_log2(n, n + 1)


def test_plancherel_row_scale_overwhelms_constant_distance_rate() -> None:
    n = 4096
    row_count = math.ceil(2 * math.sqrt(n))
    row = growing_row_prefactor_record(
        n,
        "plancherel",
        row_count,
        "Theta(n log n)",
        False,
        False,
    )

    assert row.row_count == 128
    assert row.prefactor_to_maximum_suppression_ratio > 10
    assert not row.asymptotically_absorbable_into_exp_minus_omega_n
    assert not row.fixed_row_recoupling_theorem_directly_applies


def test_fixed_rows_remain_in_published_scope() -> None:
    row = growing_row_prefactor_record(
        4096,
        "fixed",
        4,
        "Theta(log n)",
        True,
        True,
    )

    assert row.prefactor_to_maximum_suppression_ratio < 0.02
    assert row.asymptotically_absorbable_into_exp_minus_omega_n
    assert row.fixed_row_recoupling_theorem_directly_applies


def test_report_preserves_plancherel_and_algorithm_gates() -> None:
    report = run_grid_quantum_marginal_boundary()

    assert report.claim_gate["disjoint_core_is_generalized_recoupling_block"]
    assert report.claim_gate[
        "fixed_row_quantum_marginal_dichotomy_literature_linked"
    ]
    assert not report.claim_gate[
        "published_fixed_row_proof_covers_plancherel_regime"
    ]
    assert not report.claim_gate[
        "dimension_uniform_plancherel_recoupling_bound_proved"
    ]
    assert not report.claim_gate["natural_source_marginal_compatibility_classified"]
    assert not report.claim_gate["coherent_generalized_recoupling_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
    assert report.headline_metrics["new_quantum_algorithm_count"] == 0


def test_report_writer_materializes_standalone_artifact(tmp_path) -> None:
    path = tmp_path / "marginal.json"
    payload = write_grid_quantum_marginal_boundary_report(
        path=path,
        write_registry=False,
    )

    assert path.exists()
    assert payload["claim_gate"]["speedup_claim_allowed"] is False
    assert payload["headline_metrics"][
        "generalized_recoupling_identity_failure_count"
    ] == 0
