from fractions import Fraction

from representation_obstruction import integer_partitions
from self_dual_wreath_commutator_sector_filter_no_go import cycle_centralizer_size
from self_dual_wreath_plancherel_carrier_asymptotic_closure import (
    asymptotic_log_corner_kernel_bound,
    audit_centralizer_envelopes,
    audit_log_corner_kernel,
    centralizer_ratio_envelope,
    even_nonmatching_centralizer_ratio_bound,
    fixed_point_free_centralizer_envelope,
    logarithmic_fixed_point_cutoff,
    matching_centralizer_order,
    run_plancherel_carrier_asymptotic_closure,
    write_plancherel_carrier_asymptotic_closure_report,
)


def test_fixed_point_free_envelopes_cover_every_small_cycle_type() -> None:
    for n in range(4, 25):
        envelope = fixed_point_free_centralizer_envelope(n)
        for cycle_type in integer_partitions(n):
            if 1 not in cycle_type:
                assert cycle_centralizer_size(cycle_type) <= envelope


def test_even_perfect_matching_is_unique_exception_with_quantitative_gap() -> None:
    for n in range(6, 26, 2):
        k = n // 2
        baseline = matching_centralizer_order(k)
        matching = (2,) * k
        gap = even_nonmatching_centralizer_ratio_bound(k)
        assert cycle_centralizer_size(matching) == baseline
        for cycle_type in integer_partitions(n):
            if 1 not in cycle_type and cycle_type != matching:
                assert Fraction(
                    cycle_centralizer_size(cycle_type), baseline
                ) <= gap


def test_fixed_point_factor_envelopes_cover_log_corner_finite_audits() -> None:
    for n in range(6, 25):
        audit = audit_centralizer_envelopes(n)
        assert audit.fixed_point_free_envelope_verified is True
        assert audit.fixed_point_envelopes_verified is True
        assert audit.even_nonmatching_gap_verified is True
        assert audit.maximum_actual_to_envelope_ratio <= 1.0
        baseline = matching_centralizer_order(n // 2)
        for cycle_type in integer_partitions(n):
            fixed = cycle_type.count(1)
            if fixed > 4 or fixed > n - 2:
                continue
            matching = bool(n % 2 == 0 and cycle_type == (2,) * (n // 2))
            envelope = centralizer_ratio_envelope(
                n,
                fixed,
                perfect_matching_exception=matching,
            )
            assert Fraction(cycle_centralizer_size(cycle_type), baseline) <= envelope


def test_exact_class_pair_kernels_obey_exception_split() -> None:
    for n in range(6, 15):
        audit = audit_log_corner_kernel(n)
        assert audit.analytic_bound_verified is True
        assert (
            audit.maximum_exact_class_pair_probability
            <= audit.analytic_uniform_upper_bound + 1e-15
        )
        if n % 2 == 0:
            assert audit.exceptional_matching_pair is True


def test_logarithmic_corner_bounds_are_asymptotically_vanishing() -> None:
    even_degrees = (10**10, 10**12, 10**14)
    even_bounds = [
        asymptotic_log_corner_kernel_bound(
            n, logarithmic_fixed_point_cutoff(n)
        )
        for n in even_degrees
    ]
    odd_bounds = [
        asymptotic_log_corner_kernel_bound(
            n + 1, logarithmic_fixed_point_cutoff(n + 1)
        )
        for n in even_degrees
    ]
    assert all(right < left for left, right in zip(even_bounds, even_bounds[1:]))
    assert all(right < left for left, right in zip(odd_bounds, odd_bounds[1:]))
    assert even_bounds[-1] < 0.02
    assert odd_bounds[-1] < 2e-7


def test_report_closes_character_moment_but_not_algorithm_gate() -> None:
    report = run_plancherel_carrier_asymptotic_closure()
    assert report.theorem.centralizer_envelope_induction_proved is True
    assert report.theorem.even_nonmatching_gap_proved is True
    assert (
        report.theorem.logarithmic_fixed_point_uniform_kernel_vanishes_proved
        is True
    )
    assert report.theorem.weighted_commuting_probability_vanishes_proved is True
    assert report.theorem.asymptotic_constant_contextuality_proved is True
    assert report.theorem.coherent_multistar_racah_resolver_compiled is False
    assert report.claim_gate[
        "natural_aggregate_carrier_contextuality_limit_two_proved"
    ] is True
    assert report.claim_gate["structured_multistar_racah_resolver_compiled"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False


def test_writer_emits_proved_asymptotic_artifact_without_registry(tmp_path) -> None:
    payload = write_plancherel_carrier_asymptotic_closure_report(
        path=tmp_path / "asymptotic-closure.json",
        write_registry=False,
    )
    assert payload["headline_metrics"][
        "weighted_commuting_probability_vanishing_theorem_count"
    ] == 1
    assert payload["headline_metrics"][
        "asymptotic_constant_contextuality_theorem_count"
    ] == 1
    assert payload["headline_metrics"]["coherent_multistar_racah_resolver_count"] == 0
    assert len(payload["falsifiers_triggered"]) >= 5
