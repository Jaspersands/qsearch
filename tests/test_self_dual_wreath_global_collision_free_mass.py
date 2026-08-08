from fractions import Fraction

import pytest

from self_dual_wreath_global_collision_free_mass import (
    exact_global_collision_free_probability,
    global_collision_free_mass_record,
    plancherel_weights,
    run_global_collision_free_mass,
)


@pytest.mark.parametrize("n", [2, 3, 4, 5, 6])
def test_plancherel_weights_are_exact_probabilities(n: int) -> None:
    weights = plancherel_weights(n)

    assert sum(weights, Fraction()) == 1
    assert all(weight > 0 for weight in weights)


def test_global_distinct_formula_handles_impossible_and_conditioned_events() -> None:
    assert exact_global_collision_free_probability(3, 2) == 0

    unconditioned = exact_global_collision_free_probability(5, 2)
    conditioned = exact_global_collision_free_probability(
        5,
        2,
        condition_within_pairs_unequal=True,
    )

    assert 0 < unconditioned < conditioned < 1


def test_information_threshold_is_preasymptotic_at_n48() -> None:
    record = global_collision_free_mass_record(48)

    assert record.enough_distinct_partitions_exist
    assert record.stable_log_domain_evaluation
    assert record.log2_unconditioned_global_collision_free_probability < -20
    assert not record.global_collision_free_mass_inverse_polynomial


def test_report_resolves_mass_gate_but_not_spectral_gate() -> None:
    report = run_global_collision_free_mass()

    assert report.headline_metrics[
        "global_collision_free_mass_formula_count"
    ] == 1
    assert report.headline_metrics[
        "asymptotic_global_collision_free_mass_tends_to_one_theorem_count"
    ] == 1
    assert report.claim_gate[
        "asymptotic_collision_free_mass_tends_to_one_proved"
    ]
    assert report.claim_gate[
        "mass_gate_for_uniform_collision_free_theorem_resolved"
    ]
    assert not report.claim_gate[
        "selected_finite_collision_free_controls_are_uniform"
    ]
    assert not report.claim_gate[
        "collision_free_block_spectral_theorem_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
