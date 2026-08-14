from __future__ import annotations

from fractions import Fraction

from self_dual_wreath_physical_recoupling_rank_pressure_no_go import (
    audit_size_biased_kronecker_law,
    physical_kronecker_triple_weight,
    physical_pressure_record,
    run_physical_recoupling_rank_pressure_no_go,
    write_physical_recoupling_rank_pressure_no_go_report,
)


def test_physical_triple_weight_has_expected_small_example() -> None:
    assert physical_kronecker_triple_weight((3,), (3,), (3,)) == Fraction(1, 36)
    assert physical_kronecker_triple_weight((3,), (2, 1), (2, 1)) == Fraction(1, 9)


def test_size_biased_local_law_has_exact_plancherel_marginals() -> None:
    for n in range(3, 7):
        row = audit_size_biased_kronecker_law(n)
        assert row.exact_total_physical_mass == "1"
        assert row.maximum_exact_plancherel_marginal_residual == "0"
        assert row.density_identity_verified
        assert row.plancherel_marginals_verified
        assert row.lower_tail_bound_verified


def test_physical_bound_is_stronger_than_independent_union_bound() -> None:
    row = physical_pressure_record(30)

    assert row.raw_squared_bound_lower_exceeds_one
    assert row.physical_good_event_probability_lower_bound > 0.78
    assert row.certificate_nontrivial_mass_upper_bound < 0.22
    assert row.raw_squared_bound_lower_log2 > 40


def test_report_closes_certificate_not_true_norm_or_coherent_network(tmp_path) -> None:
    report = run_physical_recoupling_rank_pressure_no_go()

    assert report.claim_gate["physical_trace_mass_law_derived"]
    assert report.claim_gate["all_six_edge_marginals_plancherel_proved"]
    assert report.claim_gate["local_size_biased_kronecker_law_proved"]
    assert report.claim_gate[
        "rank_certificate_nontrivial_physical_mass_vanishes_proved"
    ]
    assert not report.claim_gate["true_typical_6j_contraction_proved"]
    assert not report.claim_gate["coherent_generalized_3nj_contraction_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "physical-pressure.json"
    payload = write_physical_recoupling_rank_pressure_no_go_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
