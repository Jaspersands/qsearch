from __future__ import annotations

import math

import pytest

from hidden_shift_public_evaluator_admission_theorem import (
    audit_analytic_family,
    audit_public_decoder,
    fingerprint_query_ceiling,
    fingerprint_theorem_control,
    run_public_evaluator_admission_theorem,
)


@pytest.mark.parametrize(
    ("domain_size", "agreement"),
    ((64, 0.5), (257, 0.25), (1024, 0.75)),
)
def test_fingerprint_ceiling_is_the_least_union_bound_certificate(
    domain_size: int,
    agreement: float,
) -> None:
    epsilon = 0.01
    queries = fingerprint_query_ceiling(domain_size, agreement, epsilon)

    assert queries is not None
    assert (domain_size - 1) * agreement**queries <= epsilon
    assert (domain_size - 1) * agreement ** (queries - 1) > epsilon


def test_fingerprint_theorem_does_not_claim_a_polynomial_time_decoder() -> None:
    row = fingerprint_theorem_control(2**20, 0.5)

    assert row.logarithmic_query_ceiling
    assert row.shifted_oracle_query_ceiling is not None
    assert row.shifted_oracle_query_ceiling <= 2 * math.log2(row.domain_size)
    assert row.exhaustive_candidate_evaluations == (
        row.domain_size * row.shifted_oracle_query_ceiling
    )
    assert not row.polynomial_time_decoder_proved


@pytest.mark.parametrize(
    "family_id",
    (
        "quadratic_chirp",
        "cubic_chirp",
        "noisy_cubic_chirp",
        "legendre_symbol",
        "quartic_character",
        "kloosterman_trace",
        "bent_quadratic_f2",
        "mm_majority_bent_f2",
        "fp2_quadratic_form",
    ),
)
def test_analytic_family_bounds_dominate_exact_finite_agreement(
    family_id: str,
) -> None:
    row = audit_analytic_family(family_id, n_bits=6)

    assert row.analytic_agreement_bound is not None
    assert row.analytic_bound_verified_by_finite_control
    assert row.exact_finite_max_equal_points <= row.analytic_equal_point_bound
    assert row.public_evaluator_query_ceiling is not None
    assert row.asymptotic_query_class.startswith("O(log")
    assert not row.public_evaluator_superlog_query_advantage_possible
    assert not row.two_black_box_oracle_lower_bound_invalidated


def test_even_dimensional_bent_controls_have_exact_half_agreement() -> None:
    quadratic = audit_analytic_family("bent_quadratic_f2", n_bits=8)
    maiorana = audit_analytic_family("mm_majority_bent_f2", n_bits=8)

    assert quadratic.exact_finite_max_agreement == pytest.approx(0.5)
    assert maiorana.exact_finite_max_agreement == pytest.approx(0.5)
    assert quadratic.analytic_equal_point_bound == quadratic.domain_size // 2
    assert maiorana.analytic_equal_point_bound == maiorana.domain_size // 2


def test_character_and_rational_bounds_have_the_claimed_point_counts() -> None:
    legendre = audit_analytic_family("legendre_symbol", n_bits=6)
    quartic = audit_analytic_family("quartic_character", n_bits=6)
    kloosterman = audit_analytic_family("kloosterman_trace", n_bits=6)

    assert legendre.analytic_equal_point_bound == (legendre.modulus + 1) // 2
    assert quartic.analytic_equal_point_bound == (quartic.modulus + 3) // 4
    assert kloosterman.analytic_equal_point_bound == 4
    assert kloosterman.exact_finite_max_equal_points <= 4


@pytest.mark.parametrize(
    "family_id",
    (
        "quadratic_chirp",
        "cubic_chirp",
        "kloosterman_trace",
        "bent_quadratic_f2",
        "mm_majority_bent_f2",
        "fp2_quadratic_form",
    ),
)
@pytest.mark.parametrize("shift", (0, 1, 7, 37))
def test_certified_public_decoders_recover_exact_shift(
    family_id: str,
    shift: int,
) -> None:
    row = audit_public_decoder(family_id, n_bits=6, shift=shift)

    assert row.recovered_exactly
    assert row.recovered_shift == row.true_shift
    assert row.polynomial_in_input_length
    assert row.shifted_value_query_count <= 7
    assert row.status == "public-value-shift-polynomially-dequantized"


def test_arbitrary_hash_mask_is_not_promoted_from_finite_evidence() -> None:
    row = audit_analytic_family("masked_quadratic_f2", n_bits=6)

    assert row.analytic_agreement_bound is None
    assert row.public_evaluator_query_ceiling is None
    assert row.status == "no-uniform-agreement-certificate"
    assert row.public_evaluator_superlog_query_advantage_possible


def test_access_boundary_preserves_known_black_box_and_dhsp_questions() -> None:
    report = run_public_evaluator_admission_theorem()
    by_model = {row.access_model: row for row in report.access_model_boundaries}

    assert by_model["public-base shifted-value oracle"].fingerprint_theorem_applies
    assert not by_model["two-black-box hidden shift"].fingerprint_theorem_applies
    assert not by_model["coherent phase oracle only"].fingerprint_theorem_applies
    assert not by_model["DHSP phase/coset-state samples"].fingerprint_theorem_applies
    assert not report.claim_gate["two_black_box_bent_query_separation_refuted"]
    assert not report.claim_gate["dhsp_phase_state_bound_proved"]


def test_current_explicit_family_list_has_no_breakthrough_admission() -> None:
    report = run_public_evaluator_admission_theorem()
    triage = {row.family_id: row for row in report.decoder_triage}

    assert report.theorem.theorem_verified
    assert report.headline_metrics["analytic_control_failure_count"] == 0
    assert report.headline_metrics["breakthrough_search_family_admission_count"] == 0
    assert report.headline_metrics["polynomial_time_public_decoder_family_count"] == 6
    assert report.headline_metrics["polynomial_decoder_control_success_count"] == 6
    assert report.headline_metrics["polynomial_decoder_control_failure_count"] == 0
    assert triage["legendre_symbol"].classical_time_status == "computational decoding gap remains"
    assert not triage["legendre_symbol"].mechanism_novel
    assert not triage["noisy_cubic_chirp"].natural_problem_reduction_present
    assert not triage["masked_quadratic_f2"].admit_as_breakthrough_search_family
    assert not report.claim_gate["speedup_claim_allowed"]


def test_invalid_fingerprint_parameters_are_rejected() -> None:
    with pytest.raises(ValueError):
        fingerprint_query_ceiling(1, 0.5)
    with pytest.raises(ValueError):
        fingerprint_query_ceiling(8, 1.1)
    with pytest.raises(ValueError):
        fingerprint_query_ceiling(8, 0.5, 1.0)
    assert fingerprint_query_ceiling(8, 1.0) is None
    assert fingerprint_query_ceiling(8, 0.0) == 1
