from fractions import Fraction

import pytest

from theorems.hermite_parameter_theorem import (
    ceil_log2, finite_certificate, growing_family, m_for_target, schedule,
    sufficient_prime,
)


@pytest.mark.parametrize("alpha,m", [(Fraction(3, 4), 2), (Fraction(8, 9), 3),
                                   (Fraction(19, 20), 5), (Fraction(99, 100), 10),
                                   (Fraction(999, 1000), 32)])
def test_accuracy_parameter_is_exact_and_reaches_target(alpha, m):
    assert m_for_target(alpha) == m
    assert schedule(m)["target"] >= alpha
    if m > 2:
        assert 1-Fraction(1, (m-1)**2) < alpha


@pytest.mark.parametrize("m,extra", [(2, 0), (3, 0), (4, 17), (10, 0), (100, 0)])
def test_all_finite_inequalities_follow_from_explicit_sufficient_region(m, extra):
    ell = schedule(m)["minimum_multiplicity"]+extra
    report = finite_certificate(sufficient_prime(m, ell), ell, m)
    assert all(report["checks"].values())
    assert report["finite_parameter_conditions_verified"]
    assert report["module_rank"] == 8*m
    assert report["unconditional_failure_upper"]["float"] < 0.01
    assert report["new_quantum_algorithm_claim_allowed"] is False
    assert report["native_decoder_or_quantum_execution"] is False
    n, s, d = report["q"]-1, 8*m-2, report["source_cap"]
    k, h = ell*n//2, ell-s
    a = (n*h-k-(s+1)*(s+2)//2)//(s+2)+1
    assert (n-d-2)*h > a+k-1
    assert 4*m*m*report["pins"] <= n
    assert Fraction(22*m**4, n) < Fraction(1, 100)


def test_scope_failures_are_not_promoted_to_no_go_results():
    ell = schedule(10)["minimum_multiplicity"]
    bad_field = finite_certificate(1000000007, ell, 10)
    assert bad_field["issues"] == ["FIELD_BELOW_SUFFICIENT_REGION"]
    bad_ell = finite_certificate(sufficient_prime(10, ell), 1, 10)
    assert bad_ell["issues"] == ["MULTIPLICITY_BELOW_SUFFICIENT_REGION"]
    assert bad_ell["status"] == "OUTSIDE_SUFFICIENT_REGION_NOT_A_NO_GO"
    with pytest.raises(ValueError):
        finite_certificate(1000000008, ell, 10)


def test_uniform_order_and_growing_target_are_charged():
    family = growing_family(Fraction(1, 2))
    assert family["quantum_space_power_of_q_excluding_logs"]["float"] == 1.75
    assert family["target_shortfall_exponent"]["float"] == -0.25
    assert family["failure_upper_exponent"]["float"] == -0.5
    assert family["field_condition_margin_exponent"]["float"] == 0.125
    assert family["classical_comparison_requires_unknown_external_constant"]
    assert not family["polylog_N_total_runtime_claim"]
    with pytest.raises(ValueError):
        growing_family(Fraction(4, 7))
    with pytest.raises(ValueError):
        growing_family(0.5)


def test_integer_logs_and_invalid_fixed_targets():
    for n in range(2, 257):
        b = ceil_log2(n)
        assert 2**(b-1) < n <= 2**b
    for bad in (Fraction(0), Fraction(1), 0.99):
        with pytest.raises(ValueError):
            m_for_target(bad)
    with pytest.raises(ValueError):
        schedule(1)
