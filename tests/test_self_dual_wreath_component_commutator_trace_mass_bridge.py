import math

import numpy as np
import pytest

from self_dual_wreath_component_commutator_trace_mass_bridge import (
    audit_component_commutator_trace,
    commutator_mass_scaling_record,
    run_component_commutator_trace_mass_bridge,
)


def _trine_povm() -> tuple[np.ndarray, ...]:
    effects = []
    for angle in (0.0, 2 * math.pi / 3, 4 * math.pi / 3):
        vector = np.asarray(
            [[1.0], [complex(math.cos(angle), math.sin(angle))]],
            dtype=complex,
        ) / math.sqrt(2)
        effects.append((2 / 3) * (vector @ vector.conj().T))
    return tuple(effects)


def test_commutator_trace_is_exact_non_crossing_minus_crossing_gap() -> None:
    row = audit_component_commutator_trace("TRINE", _trine_povm())

    assert row.exact_trace_identity_verified is True
    assert row.fourth_moment_gap == pytest.approx(row.commutator_defect_trace)
    assert row.commutator_defect_trace == pytest.approx(2 / 9)
    assert row.normalized_commutator_trace == pytest.approx(1 / 9)
    assert row.commutator_defect_rank == 2
    assert row.commutator_support_fraction == pytest.approx(1.0)
    assert row.effects_pairwise_commute is False


def test_universal_operator_and_support_bounds_hold_for_random_povms() -> None:
    rng = np.random.default_rng(19)
    for dimension, outcomes in ((2, 3), (3, 5), (5, 7)):
        raw = rng.normal(size=(outcomes * dimension, dimension)) + 1j * rng.normal(
            size=(outcomes * dimension, dimension)
        )
        isometry, _ = np.linalg.qr(raw)
        effects = []
        for outcome in range(outcomes):
            block = isometry[
                outcome * dimension : (outcome + 1) * dimension
            ]
            effects.append(block.conj().T @ block)
        row = audit_component_commutator_trace(
            f"RANDOM-{dimension}-{outcomes}",
            tuple(effects),
        )

        assert row.universal_trace_bound_verified is True
        assert row.universal_operator_bound_verified is True
        assert row.support_mass_bridge_verified is True
        assert row.commutator_defect_maximum_eigenvalue <= 2 + 1e-10
        assert row.trace_half_support_lower_bound <= row.commutator_support_fraction


def test_full_rank_nonscalarity_commuting_pvm_has_zero_gap() -> None:
    effects = []
    for index in range(4):
        effect = np.zeros((4, 4), dtype=complex)
        effect[index, index] = 1
        effects.append(effect)
    row = audit_component_commutator_trace("PVM", tuple(effects))

    assert row.effects_pairwise_commute is True
    assert row.fourth_moment_gap == pytest.approx(0.0)
    assert row.commutator_defect_trace == pytest.approx(0.0)
    assert row.commutator_defect_rank == 0


def test_nonreciprocal_commuting_cyclic_effects_have_zero_gap() -> None:
    dimension = 7
    effects = []
    for outcome in range(dimension):
        effect = np.zeros((dimension, dimension), dtype=complex)
        effect[outcome, outcome] = 1 / 3
        effect[(outcome + 1) % dimension, (outcome + 1) % dimension] = 2 / 3
        effects.append(effect)
    row = audit_component_commutator_trace("CYCLIC", tuple(effects))

    assert row.effects_pairwise_commute is True
    assert row.fourth_moment_gap == pytest.approx(0.0)
    assert row.commutator_defect_trace == pytest.approx(0.0)


@pytest.mark.parametrize("mass", [1.0, 0.5, 0.1, 0.01, 0.001])
def test_scalar_moment_mass_transfers_without_edge_or_rank_law(mass: float) -> None:
    row = commutator_mass_scaling_record(mass)

    assert row.physical_support_mass_lower_bound == pytest.approx(mass / 2)
    assert row.source_block_probability_lower_bound == pytest.approx(mass / 2)
    assert row.minimum_component_edge_required is False
    assert row.center_valued_rank_law_required is False


def test_report_keeps_natural_fourth_moment_gate_open() -> None:
    report = run_component_commutator_trace_mass_bridge()

    assert report.status == (
        "commutator-support-reduced-to-natural-compressed-fourth-moment-gap"
    )
    assert report.headline_metrics[
        "exact_component_commutator_fourth_moment_identity_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "scalar_moment_to_physical_support_bridge_theorem_count"
    ] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "scalar_M4_lower_bound_implies_physical_support_mass"
    ] is True
    assert report.claim_gate["natural_compressed_component_M4_positive"] is False
    assert report.claim_gate[
        "natural_noncommutative_component_physical_mass_proved"
    ] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
