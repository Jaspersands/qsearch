import math

from self_dual_wreath_alternating_even_collision_entropy_bridge import (
    audit_even_collision_entropy,
    run_alternating_even_collision_entropy_bridge,
    subpolynomial_collision_scaling_control,
    write_alternating_even_collision_entropy_bridge_report,
)


def test_even_class_collision_equals_coarse_label_likelihood_second_moment() -> None:
    for n in range(2, 6):
        row = audit_even_collision_entropy(n)
        assert row.second_moment_duality_residual < 2e-8
        assert row.kl_bounded_by_renyi_two
        assert row.exact_even_collision_duality_verified


def test_subpolynomial_collision_has_sublogarithmic_renyi_divergence() -> None:
    ratios = []
    for n in (10**6, 10**12, 10**24):
        collision, ratio, verified = subpolynomial_collision_scaling_control(n)
        assert collision > 1
        assert verified
        ratios.append(ratio)

    assert ratios == sorted(ratios, reverse=True)
    assert ratios[-1] < ratios[0]


def test_finite_collision_values_are_not_mistaken_for_monotone_evidence() -> None:
    moments = [
        audit_even_collision_entropy(n).exact_even_class_signature_collision_moment
        for n in range(2, 6)
    ]

    assert moments != sorted(moments)
    assert moments != sorted(moments, reverse=True)
    assert all(math.isfinite(moment) and moment >= 1 for moment in moments)


def test_report_keeps_even_collision_and_rank_claims_open(tmp_path) -> None:
    report = run_alternating_even_collision_entropy_bridge()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "coarse_alternating_renyi_two_collision_identity_proved"
    ]
    assert report.claim_gate[
        "subpolynomial_even_collision_would_imply_rank_mixing"
    ]
    assert not report.claim_gate["even_collision_subpolynomial_proved"]
    assert not report.claim_gate["physical_rank_profile_mixes_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "even-collision.json"
    payload = write_alternating_even_collision_entropy_bridge_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
