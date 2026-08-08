import numpy as np

from self_dual_wreath_component_effect_algebra_boundary import (
    audit_component_effect_algebra,
    run_component_effect_algebra_boundary,
)


def _trine_povm() -> tuple[np.ndarray, ...]:
    effects = []
    for index in range(3):
        angle = 2 * np.pi * index / 3
        vector = np.asarray([[np.cos(angle)], [np.sin(angle)]], dtype=complex)
        effects.append((2 / 3) * vector @ vector.conj().T)
    return tuple(effects)


def test_full_rank_nonscalarity_can_be_completely_commuting() -> None:
    effects = tuple(
        np.diag([1.0 if row == column else 0.0 for row in range(4)]).astype(complex)
        for column in range(4)
    )
    row = audit_component_effect_algebra("ORTHOGONAL-PVM", effects)

    assert row.nonscalarity_defect_full_rank is True
    assert row.commutator_defect_rank == 0
    assert row.effects_pairwise_commute is True
    assert row.generated_algebra_commutative is True
    assert row.generated_unital_star_algebra_dimension == 4
    assert row.noncommutative_effect_algebra is False
    assert row.exact_commutator_criterion_verified is True


def test_trine_effects_generate_full_noncommutative_qubit_algebra() -> None:
    row = audit_component_effect_algebra("TRINE", _trine_povm())

    assert row.maximum_effect_commutator_norm > 0
    assert row.commutator_defect_rank == 2
    assert row.effects_pairwise_commute is False
    assert row.generated_algebra_commutative is False
    assert row.generated_unital_star_algebra_dimension == 4
    assert row.full_matrix_algebra_dimension == 4
    assert row.noncommutative_effect_algebra is True
    assert row.exact_commutator_criterion_verified is True


def test_global_scalar_povm_has_zero_both_defects() -> None:
    identity = np.eye(3, dtype=complex)
    row = audit_component_effect_algebra(
        "SCALAR",
        (0.2 * identity, 0.3 * identity, 0.5 * identity),
    )

    assert row.effects_globally_scalar is True
    assert row.nonscalarity_defect_rank == 0
    assert row.commutator_defect_rank == 0
    assert row.generated_unital_star_algebra_dimension == 1
    assert row.status == "globally-scalar-component-algebra-verified"


def test_report_retracts_noncommutative_mass_inference() -> None:
    report = run_component_effect_algebra_boundary()

    assert report.status == (
        "nonscalarity-versus-noncommutative-algebra-boundary-proved-natural-mass-open"
    )
    assert report.claim_gate[
        "nonscalarity_defect_support_implies_noncommutative_effect_algebra"
    ] is False
    assert report.claim_gate[
        "natural_component_nonscalarity_source_and_physical_mass_proved"
    ] is True
    assert report.claim_gate[
        "natural_noncommutative_component_algebra_source_mass_proved"
    ] is False
    assert report.claim_gate[
        "coherent_commuting_component_diagonalization_compiled"
    ] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
    assert report.headline_metrics[
        "full_rank_nonscalarity_commuting_counterexample_count"
    ] == 1
