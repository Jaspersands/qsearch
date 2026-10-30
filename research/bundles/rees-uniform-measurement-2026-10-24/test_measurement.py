from fractions import Fraction as F
import json
from pathlib import Path

import numpy as np
import pytest

import measurement_controls as c
import measurement_plan as p


@pytest.mark.parametrize("prime,rank,eps", [(3, 1, F(1, 2)), (101, 7, F(1, 100)),
                                          (2**127 - 1, 73, F(1, 10**6))])
def test_complete_instrument_budget_and_public_power_cost(prime, rank, eps):
    plan = p.character_plan(prime, rank, eps, public_fast_powers=True)
    assert plan.phase_grid >= 8 * prime
    assert plan.instrument_error_squared <= (eps / 2)**2
    assert plan.qft_blocks * plan.per_qft_operator_error == eps / 2
    assert plan.controlled_public_translations == 2 * rank * len(plan.powers)
    assert plan.powers == tuple(pow(2, k, prime) for k in range(len(plan.powers)))
    assert plan.phase_bits_per_coordinate < prime.bit_length() + rank.bit_length() + 2 * eps.denominator.bit_length() + 6
    assert not plan.report()["group_or_field_enumeration"]


def test_generic_black_box_power_access_cannot_be_declared_free():
    for contract in (False, None, "yes", 1):
        with pytest.raises(ValueError, match="fast powers"):
            p.character_plan(101, 2, F(1, 10), public_fast_powers=contract)


@pytest.mark.parametrize("prime,rank,eps", [(2, 1, F(1, 2)), (4, 1, F(1, 2)), (3, 0, F(1, 2)),
                                          (3, True, F(1, 2)), (3, 1, 0), (3, 1, 1), (3, 1, 0.1)])
def test_invalid_resource_contracts_rejected(prime, rank, eps):
    with pytest.raises(ValueError):
        p.character_plan(prime, rank, eps, public_fast_powers=True)


@pytest.mark.parametrize("prime,bits", [(3, 5), (5, 6), (7, 6), (11, 7), (13, 7)])
def test_tail_bound_holds_for_every_character_in_bounded_controls(prime, bits):
    assert 1 << bits >= 8 * prime
    for label in range(prime):
        assert c.qpe_bad_probability(prime, bits, label) <= 4 * prime / (1 << bits) + 1e-13


def test_rounding_handles_zero_wraparound_and_ties_with_integer_arithmetic():
    assert p.decode_phase(0, 4, 3) == 0
    assert p.decode_phase(15, 4, 3) == 0
    assert p.decode_phase(8, 4, 3) == 2
    assert p.decode_phase(5, 4, 3) == 1
    for index in (-1, 16, True):
        with pytest.raises(ValueError, match="canonical"):
            p.decode_phase(index, 4, 3)


@pytest.mark.parametrize("prime,label", [(3, 0), (3, 1), (3, 2), (5, 1), (7, 6)])
def test_literal_circuit_matches_sector_error_identity(prime, label):
    bits = 7
    state = c.fourier_state(prime, label)[None, :, None]
    actual = c.extract_character(state, prime, bits)
    ideal = c.ideal_extraction(state, prime, bits)
    assert abs(np.linalg.norm(actual) - 1) < 1e-12
    bad = c.qpe_bad_probability(prime, bits, label)
    assert abs(np.linalg.norm(actual - ideal)**2 - 2 * bad) < 1e-12
    assert c.cq_trace_distance(actual, ideal) <= np.sqrt(2 * bad) + 1e-12


def test_degenerate_sector_coherence_and_entangled_reference_survive():
    rng = np.random.default_rng(2026)
    spectator_reference = rng.normal(size=(9, 2)) + 1j * rng.normal(size=(9, 2))
    spectator_reference /= np.linalg.norm(spectator_reference)
    state = np.einsum("qr,z->qzr", spectator_reference, c.fourier_state(3, 1))
    actual = c.extract_character(state, 3, 7)
    # Trace out phase, label and center. Full spectator/reference coherence remains.
    a = actual.transpose(0, 1, 3, 2, 4).reshape(-1, 18)
    reduced = a.T @ a.conj()
    v = spectator_reference.ravel()
    assert np.max(np.abs(reduced - np.outer(v, v.conj()))) < 1e-12


@pytest.fixture(scope="module")
def report():
    return c.audit()


def test_full_record_reference_controls_not_only_selected_outcomes(report):
    for row in report["finite_controls"]:
        assert row["norm_error"] < 1e-12
        assert row["isometry_error"] <= row["worst_sector_isometry_error_bound"] + 1e-12
        assert row["complete_cq_trace_distance"] <= row["isometry_error"] + 1e-12
    assert report["wrong_sign_complete_instrument_distance"] > 0.95
    assert report["retained_fourier_basis_correlation_error"] > 0.999


@pytest.mark.parametrize("prime,dimension,eps", [(3, 1, F(1, 10)), (5, 17, F(1, 10000)),
                                               (2**127 - 1, 200, F(1, 10**6))])
def test_public_rejection_is_capped_and_not_hidden_postselection(prime, dimension, eps):
    plan = p.address_plan(prime, dimension, eps)
    cap = plan["attempts_per_coordinate_cap"]
    assert F(plan["complete_channel_abort_bound"]) <= F(dimension, 2**cap) <= eps
    assert plan["native_copies_consumed_before_success"] == 0
    assert plan["uniform_on_every_successful_record"]


@pytest.mark.parametrize("prime,dimension", [(3, 1), (3, 8), (5, 13), (2**127 - 1, 73)])
def test_rank_bound_works_for_every_possible_hidden_codimension(prime, dimension):
    eps = F(1, 10000)
    plan = p.terminal_sampling_plan(prime, dimension, eps)
    k = plan["terminal_samples"]
    reported = F(plan["span_failure_union_bound"])
    assert reported <= eps
    for rank in range(dimension + 1):
        exact_success = F(1)
        for i in range(rank):
            exact_success *= 1 - F(prime**i, prime**k)
        assert 1 - exact_success <= reported
    assert not plan["measurement_and_source_error_included"]


def test_no_new_algorithm_or_compiler_is_inferred_from_controls(report):
    flags = report["scope_flags"]
    assert flags["known_phase_estimation_primitive_not_novel"]
    for name in ("independently_reviewed_current_pass", "new_lean_theorem", "full_gate_compiler_implemented",
                 "end_to_end_hsp_execution", "novelty_or_speedup_certified"):
        assert not flags[name]


def test_existing_formal_projection_uses_the_same_sign_convention():
    # Bind the direct-projector comparator to the frozen formal interface.
    root = Path(__file__).resolve().parent.parent / "rees-formal-core-2026-10-24"
    source = (root / "ReesStageInstrument.lean").read_text()
    assert "chi z * star (chi w) * rho (x * (embed z)⁻¹) (y * (embed w)⁻¹)" in source
    for label in range(3):
        projector = c.spectral_projector(3, label)
        state = c.fourier_state(3, label)
        assert np.max(np.abs(projector - np.outer(state, state.conj()))) < 1e-12
    receipt = json.loads((root / "native_source_receipt.json").read_text())
    assert receipt["combined_theorem_count"] == 180
