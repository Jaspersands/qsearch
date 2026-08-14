import math

from self_dual_wreath_compressed_racah_coupling_probe import (
    compile_complete_racah_coupling,
)
from self_dual_wreath_plancherel_character_racah_fourier_reduction import (
    audit_natural_racah_character_sum,
    audit_plancherel_character_basis,
    identity_coupling_fourier_tail_control,
    run_plancherel_character_racah_fourier_reduction,
)


def test_normalized_characters_are_complete_plancherel_basis() -> None:
    row = audit_plancherel_character_basis(8)
    assert row.partition_count == row.conjugacy_class_count
    assert row.maximum_orthonormality_residual < 1e-11
    assert row.maximum_constant_mode_residual == 0.0
    assert row.exact_plancherel_character_basis_verified


def test_racah_fourier_coefficient_equals_gauge_free_character_sum() -> None:
    outer = ((3, 1),) * 4
    coupling = compile_complete_racah_coupling(outer)
    row = audit_natural_racah_character_sum(
        outer,
        (2, 1, 1),
        (3, 1),
        coupling=coupling,
    )
    assert row.formula_residual < 1e-9
    assert row.exact_character_sum_formula_verified


def test_identity_coupling_exposes_uncontrolled_fourier_tail() -> None:
    row = identity_coupling_fourier_tail_control(30, 3)
    assert row.retained_nonconstant_mode_count == 2
    assert row.omitted_nonconstant_mode_count > row.retained_nonconstant_mode_count
    assert row.retained_energy_fraction < 0.01
    assert row.identity_coupling_mutual_information_bits > math.log2(30)
    assert row.exact_tail_decomposition_verified


def test_report_keeps_growing_support_and_algorithm_gates_closed() -> None:
    report = run_plancherel_character_racah_fourier_reduction()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["plancherel_character_basis_complete_proved"] is True
    assert report.claim_gate["low_support_fourier_modes_control_full_label_tail"] is False
    assert report.claim_gate["efficient_classical_estimator_proved"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
