import numpy as np

from self_dual_wreath_component_common_codimension_curl_reduction import (
    _random_control,
    audit_common_codimension_curl_reduction,
    common_codimension_curl_theorem,
    common_codimension_scaling_record,
    full_and_dependency_projections,
    run_component_common_codimension_curl_reduction,
)


def test_support_difference_rank_is_exact_excluded_rank() -> None:
    synthesis, common = _random_control(8, 16, 5, seed=81)
    full, excluded, dependency = full_and_dependency_projections(synthesis, common)

    assert np.linalg.norm(full - dependency - excluded, ord=2) < 1e-9
    assert round(np.trace(excluded).real) == 3
    assert abs(np.linalg.norm(full - dependency, ord="fro") ** 2 - 3) < 1e-8


def test_full_support_words_and_curl_transfer_exactly() -> None:
    synthesis, common = _random_control(8, 16, 6, seed=82)
    row = audit_common_codimension_curl_reduction(
        "TEST-FULL-SUPPORT",
        synthesis,
        common,
        4,
    )

    assert row.exact_rank_and_word_reduction_verified
    assert row.stability_bound_verified
    assert row.maximum_full_support_word_residual < 1e-8
    assert row.full_support_curl_residual < 1e-8


def test_curl_transfer_bound_vanishes_with_nullity_fraction() -> None:
    rows = [
        common_codimension_scaling_record(n, 1 / n, 1 / n)
        for n in (32, 128, 512, 2048)
    ]

    assert not rows[0].common_compression_negligible_at_constant_scale
    assert rows[-1].common_compression_negligible_at_constant_scale
    assert rows[-1].normalized_curl_transfer_error_upper_bound < rows[0].normalized_curl_transfer_error_upper_bound
    assert not any(row.inverse_polynomial_signal_preserved_without_rate for row in rows)


def test_theorem_removes_common_compression_but_not_full_support_curl() -> None:
    theorem = common_codimension_curl_theorem()
    report = run_component_common_codimension_curl_reduction()

    assert theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["natural_common_codimension_subextensive"]
    assert report.claim_gate["common_compression_negligible_for_constant_normalized_curl"]
    assert report.claim_gate["full_support_canonical_effect_target_exact"]
    assert not report.claim_gate["natural_full_support_canonical_curl_positive"]
    assert not report.claim_gate["natural_component_M4_positive"]
    assert not report.claim_gate["speedup_claim_allowed"]
