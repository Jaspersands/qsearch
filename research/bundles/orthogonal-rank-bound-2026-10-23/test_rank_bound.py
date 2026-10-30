from fractions import Fraction

import pytest

import rank_bound as rb


@pytest.mark.parametrize("q", [3, 5, 9, 27, 81, 125, 3**64, 2**127-1])
def test_supported_odd_field_orders(q):
    assert rb.odd_prime_power(q)
    assert 0 < rb.fixed_point_bound(3, q) < 1


@pytest.mark.parametrize("q", [True, 0, 1, 2, 4, 15, 21, 45, 3.0])
def test_nonfields_and_even_fields_rejected(q):
    with pytest.raises(ValueError):
        rb.fixed_point_bound(3, q)


@pytest.mark.parametrize("n", [True, 0, 1, 2, 3.0])
def test_rank_two_exception_not_silently_admitted(n):
    with pytest.raises(ValueError):
        rb.fixed_point_bound(n, 3)


@pytest.mark.parametrize("n,p,total", [(3, 3, 80), (3, 5, 312), (4, 3, 2240)])
def test_complete_orbits_root_formula_and_general_bound(n, p, total):
    receipt = rb.finite_control(n, p)
    assert receipt["spaces_exhausted"] == total
    assert receipt["component_sizes"] == [total//2]*2
    assert receipt["controls"]["component_switch"]["fixed_in_components"] == [0, 0]
    assert receipt["entire_group_exhausted"] is False


def test_rank_decay_and_root_control_has_same_exponent():
    for q in (3, 5, 9, 127):
        for n in (3, 4, 8, 32, 64):
            bound = rb.fixed_point_bound(n, q)
            root = rb.root_fixed_point_ratio(n, q)
            assert rb.fixed_point_bound(n+1, q) == bound/q
            assert Fraction(1, 2*q**(n-2)) < root < bound
            assert bound <= Fraction(7, 3*q**(n-2))


@pytest.mark.parametrize("n,q", [(3, 3), (8, 9), (16, 3), (64, 3), (128, 5), (8, 2**127-1)])
def test_necessary_query_threshold_exactly_crosses_bound(n, q):
    target = Fraction(2, 3)
    threshold = rb.necessary_queries(n, q, target)
    assert rb.classical_success_bound(n, q, threshold-1) < target
    assert rb.classical_success_bound(n, q, threshold) >= target
    assert rb.classical_success_bound(n, q, 0) == Fraction(1, rb.component_size(n, q))
    assert rb.classical_success_bound(n, q, 1) == rb.classical_success_bound(n, q, 0)
    assert rb.classical_success_bound(n, q, rb.component_size(n, q)) == 1


def test_small_success_target_can_require_no_queries():
    assert rb.necessary_queries(3, 3, Fraction(1, 100)) == 0


@pytest.mark.parametrize("target", [0, 1, -1, 0.5])
def test_ambiguous_or_invalid_probability_rejected(target):
    with pytest.raises(ValueError):
        rb.necessary_queries(3, 3, target)


def test_center_is_public_repeat_not_informative_collision():
    p, n = 3, 3
    for g in rb.structural_controls(n, p).values():
        negative = tuple(tuple(-value % p for value in row) for row in g)
        assert rb.central_query_key(g, p) == rb.central_query_key(negative, p)
        assert rb.central_query_key(g, p) != rb.central_query_key(rb.op.eye(2*n), p)
    identity = rb.op.eye(2*n)
    negative = tuple(tuple(-value % p for value in row) for row in identity)
    for space in rb.all_maximal(n, p):
        assert rb.op.image(identity, space, p) == space
        assert rb.op.image(negative, space, p) == space
    assert rb.scalar_sign(identity, p) == 1
    assert rb.scalar_sign(negative, p) == p-1


def test_structured_label_source_is_a_one_query_classical_counterexample():
    p, n = 3, 3
    hidden = rb.op.image(rb.structural_controls(n, p)["lower_root"], rb.op.eye(2*n)[:n], p)
    calls = 0

    def natural_label(g):
        nonlocal calls
        calls += 1
        return rb.op.image(g, hidden, p)

    assert natural_label(rb.op.eye(2*n)) == hidden and calls == 1
    with pytest.raises(ValueError, match="opaque"):
        rb.classical_success_bound(n, p, 1, label_model="subspace_coordinates")


def test_enumeration_cannot_be_used_as_scalable_algorithm():
    with pytest.raises(ValueError, match="cap"):
        rb.all_maximal(8, 127)
    with pytest.raises(ValueError, match="prime fields"):
        rb.all_maximal(3, 9)


@pytest.mark.parametrize("queries", [True, -1, 1.5])
def test_invalid_query_counts_rejected(queries):
    with pytest.raises(ValueError):
        rb.classical_success_bound(3, 3, queries)
