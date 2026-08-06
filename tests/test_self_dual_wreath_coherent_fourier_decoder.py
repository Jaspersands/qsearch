import numpy as np

from self_dual_wreath_coherent_fourier_decoder import (
    audit_coherent_fourier_decoder,
    coherent_fourier_success,
    entanglement_fidelity_from_schmidt,
    run_coherent_fourier_decoder,
    symmetric_group_fourier_matrix,
)


def test_young_matrix_coefficient_fourier_matrix_is_unitary() -> None:
    matrix, permutations, _ = symmetric_group_fourier_matrix(4)
    assert matrix.shape == (24, 24)
    assert len(permutations) == 24
    assert np.allclose(matrix @ matrix.T, np.eye(24))


def test_decoder_formula_is_perfect_for_plancherel_maximal_entanglement() -> None:
    dimensions = (1, 2, 1)
    plancherel = tuple(value * value / 6 for value in dimensions)
    fidelities = (1.0, 1.0, 1.0)
    assert abs(coherent_fourier_success(dimensions, plancherel, fidelities) - 1) < 1e-12
    assert entanglement_fidelity_from_schmidt((0.5, 0.5), 2) == 1
    assert entanglement_fidelity_from_schmidt((1.0,), 2) < 1


def test_exact_finite_control_matches_success_formula_for_every_permutation() -> None:
    control = audit_coherent_fourier_decoder(
        4,
        control_id="S4-MISMATCH",
        weight_mode="dimension",
        schmidt_mode="mixed-profile",
    )
    assert control.exact_decoder_formula_verified
    assert control.exact_permutation_independence_verified
    assert control.maximum_success_formula_residual < 1e-10
    assert control.predicted_correct_label_probability < 1


def test_report_opens_carrier_normalization_not_speedup_gate() -> None:
    report = run_coherent_fourier_decoder()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert abs(report.headline_metrics["ideal_control_success_probability"] - 1) < 1e-10
    assert report.claim_gate["coherent_fourier_decoder_criterion_proved"]
    assert report.claim_gate["efficient_inverse_symmetric_group_qft_available"]
    assert not report.claim_gate["coherent_dual_row_extraction_proved"]
    assert not report.claim_gate["sector_schmidt_flattening_proved"]
    assert not report.claim_gate["end_to_end_hidden_permutation_decoder_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
