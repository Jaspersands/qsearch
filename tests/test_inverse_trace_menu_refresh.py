"""Exact native-law countercontrols, not toy-oracle candidate algorithms."""
from fractions import Fraction as Q
from math import comb

import pytest

from theorems.inverse_trace_menu_refresh import (
    certificate, finite_reference, mobility_bound, support_tv_lower,
)


@pytest.mark.parametrize("size", [1, 2, 3, 4])
def test_native_kernel_and_unanchored_laws(size):
    row = finite_reference(3, (0, 1, 2, 3), 1, (1, 1, 1, 1), size)
    matrix = row["anchored_matrix"]
    assert row["native_words"] == 40
    assert all(sum(r) == 1 for r in matrix)
    assert all(matrix[i][j] == matrix[j][i] for i in range(40) for j in range(40))
    assert row["repaired_success"] == Q(5, 32)
    assert row["mds_repaired_success"] == Q(5*size, 32)
    assert row["mds_repair_exactly_uniform"]
    assert row["repair_exactly_uniform"] and not row["reference_is_scalable_sampler"]
    if size == 1:
        assert all(matrix[i][i] == 1 for i in range(40))
    if size == 2:
        assert row["abort_probability"] == Q(1, 54)
        assert row["conditional_tv"] == Q(39, 4240)
    if size == 3:
        assert row["abort_probability"] == 0
        assert row["conditional_tv"] == Q(9, 3640)
    if size == 4:
        assert all(x == Q(1, 40) for r in matrix for x in r)
        assert row["conditional_tv"] == 0


@pytest.mark.parametrize("targets,syndrome", [((0, 0, 0), (0, 0)),
                                              ((1, 0, 1), (1, 3)),
                                              ((1, 1, 1), (0, 0))])
def test_native_syndromes_and_all_zero_control(targets, syndrome):
    row = finite_reference(2, (0, 1, 2), 2, targets, 2, syndrome)
    if row["native_words"]:
        count = row["native_words"]
        assert row["repaired_success"] == Q(count, 2**3)
        assert row["mds_repaired_success"] == Q(count*2**2, 2**3)
        assert all(p == Q(1, count) for r in row["anchored_matrix"] for p in r)
    else:
        assert row["status"] == "EMPTY_NATIVE_FIBER" and row["conditional_tv"] is None


@pytest.mark.parametrize("bits,length,checks,size", [(3, 4, 2, 2), (5, 12, 3, 3),
                                                   (17, 289, 36, 2)])
def test_exact_support_union_bound_and_distances(bits, length, checks, size):
    expected = Q(sum(comb(length, w)*(size-1)**w for w in range(checks+1, length+1)),
                 (2**(bits-1)-1)**checks)
    assert mobility_bound(bits, length, checks, size) == min(Q(1), expected)
    assert mobility_bound(bits, length, checks, 1) == 0


@pytest.mark.parametrize("bits,size,exponent", [(17, 2, -286), (31, 2, -2638),
                                             (61, 61, -5831), (127, 16129, -28575)])
def test_outward_rounding_and_scope(bits, size, exponent):
    row = certificate(bits, size)
    bound = mobility_bound(bits, bits*bits, bits*bits//8, size)
    assert row["mobility_power2_upper"] == exponent
    assert bound <= Q(1, 2**-exponent)
    assert row["nonvacuous"] and not row["general_classical_hardness"]
    assert not row["native_large_chain_executed"]


def test_vacuous_regimes_are_not_promoted():
    for bits in (17, 31):
        row = certificate(bits, bits)
        assert not row["nonvacuous"] and row["mobility_power2_upper"] == 0
    assert certificate(17, 1)["mobility_exactly_zero"]


def test_adaptive_support_bound_includes_initial_bias_and_abort():
    assert support_tv_lower(Q(1, 1024), 32, Q(1, 4)) == Q(23, 32)
    assert support_tv_lower(Q(1), 2, Q(0)) == 0
    assert support_tv_lower(Q(0), 100, Q(1)) == 0
    with pytest.raises(ValueError):
        support_tv_lower(0.1, 1, Q(0))


@pytest.mark.parametrize("bits,length,checks,size", [(True, 4, 1, 2), (3, 9, 1, 2),
                                                   (3, 4, 4, 2), (3, 4, 1, 5)])
def test_bad_analytic_inputs_fail_closed(bits, length, checks, size):
    with pytest.raises(ValueError):
        mobility_bound(bits, length, checks, size)


def test_reference_caps_shapes_and_noncanonical_inputs():
    for points, targets, syndrome in [((0, 0, 2), (0, 0, 0), (0,)),
                                      ((0, 1, 4), (0, 0, 0), (0,)),
                                      ((0, 1, 2), (0, 0), (0,)),
                                      ((0, 1, 2), (0, 0, True), (0,)),
                                      ((0, 1, 2), (0, 0, 0), (4,)),
                                      ((0, 1, 2), (0, 0, 0), ())]:
        with pytest.raises(ValueError):
            finite_reference(2, points, 1, targets, 2, syndrome)
    with pytest.raises(ValueError, match="cap"):
        finite_reference(4, tuple(range(8)), 2, (0,)*8, 4)
