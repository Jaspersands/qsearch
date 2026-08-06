import math

import numpy as np
import pytest

from self_dual_wreath_mixed_covariant_decoder import (
    audit_physical_projector_orbit,
    canonical_pgm_seed,
    minimum_covariant_seed_rank,
    run_mixed_covariant_decoder,
)


THREE_UNEQUAL_TYPES = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_minimum_covariant_seed_rank_uses_multiplicity_support() -> None:
    assert minimum_covariant_seed_rank(((1, 4), (2, 8), (3, 7))) == 4
    assert minimum_covariant_seed_rank(()) == 0
    with pytest.raises(ValueError):
        minimum_covariant_seed_rank(((0, 1),))


def test_canonical_pgm_seed_for_orthogonal_regular_orbit() -> None:
    states = tuple(np.diag([1.0 if i == g else 0.0 for i in range(3)]) for g in range(3))
    average = sum(states) / 3
    seed = canonical_pgm_seed(states[0], average, 3)

    assert np.linalg.norm(seed - states[0]) < 1e-12
    assert math.isclose(float(np.trace(seed @ states[0])), 1.0)


def test_actual_w3_projector_orbit_requires_mixed_tight_frame() -> None:
    record = audit_physical_projector_orbit(
        "test-three-types",
        THREE_UNEQUAL_TYPES,
    )

    assert record.exact_finite_mixed_decoder_validation
    assert record.base_projector_rank == 4
    assert record.average_frame_support_rank == 24
    assert record.pgm_seed_rank == 4
    assert record.global_seed_junk_rank_lower_bound == 4
    assert record.support_rank_global_lower_bound == 4
    assert not record.pure_coherent_fourier_seed_possible
    assert record.pgm_seed_support_completeness_residual < 1e-10
    assert record.maximum_sector_probability_formula_residual < 1e-10


def test_cross_isotypic_coherence_beats_exact_label_ceiling() -> None:
    record = audit_physical_projector_orbit(
        "test-coherence",
        THREE_UNEQUAL_TYPES,
    )

    assert record.pgm_correct_success_probability > 0.97
    assert record.exact_label_dephasing_success_upper_bound == pytest.approx(2 / 3)
    assert record.pgm_beats_exact_label_dephasing_ceiling
    assert record.cross_isotypic_coherence_success_contribution > 0.49
    assert (
        record.isotypically_dephased_pgm_seed_success_probability
        < record.exact_label_dephasing_success_upper_bound
    )


def test_report_keeps_efficiency_and_speedup_gates_closed() -> None:
    report = run_mixed_covariant_decoder()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["pure_rank_one_seed_impossible_control_count"] >= 2
    assert report.headline_metrics["pgm_beats_dephasing_ceiling_control_count"] >= 2
    assert report.claim_gate["mixed_covariant_decoder_criterion_proved"]
    assert not report.claim_gate["pure_coherent_fourier_state_is_general_physical_decoder"]
    assert not report.claim_gate["polynomial_coherent_multiplicity_whitening_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
