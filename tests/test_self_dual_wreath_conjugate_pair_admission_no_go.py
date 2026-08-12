import json

from self_dual_wreath_conjugate_pair_admission_no_go import (
    audit_conjugate_pair_admission,
    conjugate_pair_admission_scaling_record,
    run_conjugate_pair_admission_no_go,
    write_conjugate_pair_admission_no_go_report,
)


def test_conjugate_pair_probability_equals_plancherel_collision() -> None:
    for n in range(4, 13):
        row = audit_conjugate_pair_admission(n)
        assert row.conjugation_preserves_plancherel_weight_verified
        assert row.exact_collision_identity_verified
        assert row.status == "exact-conjugate-pair-equals-plancherel-collision"


def test_collision_probability_obeys_partition_and_max_atom_sandwich() -> None:
    for n in range(4, 17):
        row = audit_conjugate_pair_admission(n)
        assert row.lower_bound_residual == 0
        assert row.upper_bound_residual == 0
        assert row.plancherel_collision_probability >= (
            row.reciprocal_partition_lower_bound
        )
        assert row.plancherel_collision_probability <= row.maximum_plancherel_atom


def test_distinct_conditioning_removes_self_conjugate_duplicates() -> None:
    for n in range(4, 13):
        row = audit_conjugate_pair_admission(n)
        assert abs(
            row.distinct_conjugate_pair_probability
            - row.plancherel_collision_probability
            + row.self_conjugate_duplicate_probability
        ) < 1e-15
        assert 0 <= row.unequal_conditioned_conjugate_probability <= 1


def test_polynomial_pool_scaling_keeps_approximate_routes_open() -> None:
    row = conjugate_pair_admission_scaling_record(1024)
    assert not row.inverse_polynomial_exact_conjugate_admission
    assert not row.approximate_or_distributed_twist_ruled_out
    assert row.global_distinct_conditioning_mass_tends_to_one
    assert row.amplitude_amplification_query_lower_asymptotic == (
        "exp(Theta(sqrt(n)))"
    )


def test_report_preserves_scoped_no_go() -> None:
    report = run_conjugate_pair_admission_no_go()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["exact_conjugate_admission_stretched_exponential"]
    assert not report.claim_gate["polynomial_sample_pool_repairs_exact_matching"]
    assert not report.claim_gate["approximate_or_distributed_sign_twist_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_emits_valid_json(tmp_path) -> None:
    path = tmp_path / "conjugate_pair_admission_no_go.json"
    payload = write_conjugate_pair_admission_no_go_report(path)
    parsed = json.loads(path.read_text())
    assert parsed["status"] == payload["status"]
    assert parsed["headline_metrics"] == payload["headline_metrics"]
