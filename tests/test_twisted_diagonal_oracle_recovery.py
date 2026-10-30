"""Independent opaque-oracle audit, with no producer group/oracle helpers.

Permutations compose right-to-left. The fixture evaluates the group action
g.x = b * x**((-1)**s) * a**-1 and lazily assigns opaque labels to its fibers.
The receiver gets only n and a call-only callback, never the fixture secret.
"""

from collections import Counter
from itertools import combinations, permutations
from math import comb, factorial
import random

import pytest

from theorems.wreath_coset_permutation_holevo_collapse import (
    recover_twisted_diagonal,
)


def _compose(left, right):
    return tuple(left[value] for value in right)


def _inverse(p):
    return tuple(p.index(value) for value in range(len(p)))


def _swap(n, i, j):
    return tuple(j if k == i else i if k == j else k for k in range(n))


def _multiply(g, h):
    a, b, s = g
    c, d, t = h
    if s:
        c, d = d, c
    return _compose(a, c), _compose(b, d), s ^ t


def _group_inverse(g):
    a, b, s = g
    if s:
        a, b = b, a
    return _inverse(a), _inverse(b), s


def _subgroup(tau):
    inv_tau = _inverse(tau)
    result = set()
    for pi in permutations(range(len(tau))):
        result.add((pi, _compose(tau, _compose(pi, inv_tau)), 0))
        result.add((_compose(pi, inv_tau), _compose(tau, pi), 1))
    return result


class _CallOnly:
    """Tripwire for ordinary evaluator/closure introspection, not a sandbox."""

    __slots__ = ("__evaluate",)

    def __init__(self, evaluate):
        object.__setattr__(self, "_CallOnly__evaluate", evaluate)

    def __getattribute__(self, name):
        raise AssertionError("the receiver may call, not inspect, the oracle")

    def __call__(self, element):
        evaluate = object.__getattribute__(self, "_CallOnly__evaluate")
        return evaluate(element)


class _SameHashLabel:
    __slots__ = ()

    def __hash__(self):
        return 0


class _FreshEqualLabel:
    """Equal returns need not have the same Python object identity."""

    __slots__ = ("__token",)

    def __init__(self, token):
        object.__setattr__(self, "_FreshEqualLabel__token", token)

    def __getattribute__(self, name):
        raise AssertionError("opaque labels expose no data")

    def __hash__(self):
        return hash(object.__getattribute__(self, "_FreshEqualLabel__token"))

    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented
        return object.__getattribute__(self, "_FreshEqualLabel__token") is (
            object.__getattribute__(other, "_FreshEqualLabel__token")
        )


def _oracle(tau, *, label_factory=object, fresh_equal=False, limit=None):
    tau = tuple(tau)
    n = len(tau)
    inv_tau = _inverse(tau)
    labels = {}
    calls = []

    def evaluate(element):
        a, b, s = element
        a, b = tuple(a), tuple(b)
        assert sorted(a) == sorted(b) == list(range(n))
        assert type(s) is int and s in (0, 1)
        calls.append((a, b, s))
        if limit is not None:
            assert len(calls) <= limit, "receiver exceeded its original-query budget"
        secret = inv_tau if s else tau
        # Direct image-array action, independent of the producer's composition.
        point = tuple(b[secret[preimage]] for preimage in _inverse(a))
        if point not in labels:
            labels[point] = label_factory()
        token = labels[point]
        return _FreshEqualLabel(token) if fresh_equal else token

    return _CallOnly(evaluate), calls


def _assert_recovery(tau, query, calls):
    n = len(tau)
    e = tuple(range(n))
    bound = comb(n, 2) + n + 1
    result = recover_twisted_diagonal(n, query)
    assert result["permutation"] == list(tau)
    assert result["query_count"] == result["query_bound"] == len(calls) == bound
    assert result["source_promise_verified"] is False
    assert result["original_query_relations_verified"] is True
    expected = [(e, _swap(n, i, j), 0) for i, j in combinations(range(n), 2)]
    expected += [(_swap(n, 0, i), e, 0) for i in range(1, n)]
    expected += [(e, e, 0), (_inverse(tau), tuple(tau), 1)]
    assert Counter(calls) == Counter(expected)
    return result


SMALL_SECRETS = tuple(tau for n in (3, 4) for tau in permutations(range(n)))


@pytest.mark.parametrize("tau", SMALL_SECRETS)
def test_independent_action_fibers_are_exactly_left_cosets(tau):
    n = len(tau)
    e = tuple(range(n))
    subgroup = _subgroup(tau)
    assert len(subgroup) == 2 * factorial(n)
    assert (e, e, 0) in subgroup
    assert all(_multiply(h, k) in subgroup for h in subgroup for k in subgroup)
    query, _ = _oracle(tau)
    seen, coset_labels = set(), set()
    for b in permutations(range(n)):
        representative = (e, b, 0)
        label = query(representative)
        assert type(label) is object
        assert label not in coset_labels
        coset_labels.add(label)
        coset = {_multiply(representative, h) for h in subgroup}
        assert len(coset) == len(subgroup)
        assert seen.isdisjoint(coset)
        assert all(query(g) is label for g in coset)
        seen.update(coset)
    assert len(coset_labels) == factorial(n)
    assert len(seen) == 2 * factorial(n) ** 2


def test_left_and_right_cosets_are_not_silently_identified():
    tau, e = (1, 2, 0), (0, 1, 2)
    query, _ = _oracle(tau)
    g = (e, _swap(3, 0, 1), 0)
    h = (_swap(3, 0, 1), _swap(3, 1, 2), 0)
    assert h in _subgroup(tau)
    assert query(_multiply(g, h)) is query(g)
    assert query(_multiply(h, g)) is not query(g)


@pytest.mark.parametrize("tau", SMALL_SECRETS)
def test_recovery_all_secrets_s3_s4(tau):
    query, calls = _oracle(tau, limit=comb(len(tau), 2) + len(tau) + 1)
    _assert_recovery(tau, query, calls)


@pytest.mark.parametrize("n", (8, 32))
@pytest.mark.parametrize("seed", range(8))
def test_randomized_recovery_with_exact_query_accounting(n, seed):
    tau = list(range(n))
    random.Random(1000 * n + seed).shuffle(tau)
    query, calls = _oracle(tau, limit=comb(n, 2) + n + 1)
    _assert_recovery(tuple(tau), query, calls)


@pytest.mark.parametrize("label_factory", (object, _SameHashLabel))
@pytest.mark.parametrize("fresh_equal", (False, True))
def test_opaque_relabeling_and_legal_hash_collisions(label_factory, fresh_equal):
    tau = (2, 0, 3, 1)
    for _ in range(4):
        query, calls = _oracle(tau, label_factory=label_factory, fresh_equal=fresh_equal)
        _assert_recovery(tau, query, calls)


@pytest.mark.parametrize("falsey_label", (None, False, 0, "", ()))
def test_hashable_falsey_labels_are_valid(falsey_label):
    first = True

    def allocate():
        nonlocal first
        if first:
            first = False
            return falsey_label
        return object()

    tau = (1, 2, 3, 0)
    query, calls = _oracle(tau, label_factory=allocate)
    _assert_recovery(tau, query, calls)


def test_receiver_has_no_evaluator_or_secret_advice():
    tau = (3, 0, 2, 1)
    query, calls = _oracle(tau)
    for attribute in ("tau", "secret", "labels", "__dict__", "__closure__",
                      "__code__", "__globals__", "__self__", "__wrapped__"):
        with pytest.raises(AssertionError, match="may call, not inspect"):
            getattr(query, attribute)
    assert calls == []
    _assert_recovery(tau, query, calls)


@pytest.mark.parametrize("n", (-2, 0, 1, 2, False, True, 3.0, "3", None))
def test_invalid_dimension_is_rejected_without_queries(n):
    def forbidden_query(element):
        pytest.fail("an invalid dimension must be rejected before querying")

    with pytest.raises(ValueError):
        recover_twisted_diagonal(n, _CallOnly(forbidden_query))


@pytest.mark.parametrize("query", (None, 0, object()))
def test_noncallable_oracle_is_rejected(query):
    with pytest.raises(ValueError):
        recover_twisted_diagonal(3, query)


@pytest.mark.parametrize("label", ([], {}))
def test_unhashable_oracle_labels_are_rejected(label):
    with pytest.raises(ValueError):
        recover_twisted_diagonal(3, _CallOnly(lambda element: label))


def test_colliding_labels_for_distinct_public_transpositions_are_rejected():
    shared_label = object()
    with pytest.raises(ValueError):
        recover_twisted_diagonal(4, _CallOnly(lambda element: shared_label))


def test_one_merged_cache_fiber_is_rejected():
    n, e = 4, tuple(range(4))
    query, calls = _oracle(e)
    source = (e, _swap(n, 0, 2), 0)
    target = (e, _swap(n, 0, 1), 0)
    corrupted = _CallOnly(lambda g: query(target if g == source else g))
    with pytest.raises(ValueError):
        recover_twisted_diagonal(n, corrupted)
    assert len(calls) <= comb(n, 2)


def test_identity_fiber_cannot_merge_with_a_cached_transposition_fiber():
    tau, e = (1, 2, 3, 0), tuple(range(4))
    query, _ = _oracle(tau)
    identity = (e, e, 0)
    odd = (_inverse(tau), tau, 1)
    cached_label = query((e, _swap(4, 0, 1), 0))

    def corrupt(g):
        if g in (identity, odd):
            return cached_label
        return query(g)

    # The final equality still holds, but these two observed fibers must differ
    # under every promised H_tau. This is a finite, not an unqueried, defect.
    with pytest.raises(ValueError):
        recover_twisted_diagonal(4, _CallOnly(corrupt))


def test_a_star_label_absent_from_the_cache_is_rejected():
    query, _ = _oracle(tuple(range(4)))
    absent = object()
    corrupted = _CallOnly(lambda g: absent if g[0] != tuple(range(4)) else query(g))
    with pytest.raises(ValueError):
        recover_twisted_diagonal(4, corrupted)


@pytest.mark.parametrize("star, replacement_pair", (
    (2, (0, 1)),  # First two image edges coincide: two candidate origins.
    (2, (2, 3)),  # First two image edges are disjoint: no candidate origin.
    (3, (1, 2)),  # A later image edge omits the inferred origin.
    (3, (0, 2)),  # A later edge repeats an already recovered image.
))
def test_inconsistent_star_images_are_rejected(star, replacement_pair):
    n, e = 4, tuple(range(4))
    query, calls = _oracle(e)
    source = (_swap(n, 0, star), e, 0)
    target = (e, _swap(n, *replacement_pair), 0)
    corrupted = _CallOnly(lambda g: query(target if g == source else g))
    with pytest.raises(ValueError):
        recover_twisted_diagonal(n, corrupted)
    assert len(calls) <= comb(n, 2) + n - 1


@pytest.mark.parametrize("corrupt_odd", (False, True))
def test_both_original_queries_in_the_final_odd_check_are_required(corrupt_odd):
    tau, e = (1, 2, 3, 0), tuple(range(4))
    query, calls = _oracle(tau)
    target = (_inverse(tau), tau, 1) if corrupt_odd else (e, e, 0)
    wrong_label = object()

    def corrupt(g):
        honest = query(g)
        return wrong_label if g == target else honest

    with pytest.raises(ValueError):
        recover_twisted_diagonal(4, _CallOnly(corrupt))
    assert len(calls) == comb(4, 2) + 4 + 1
    assert (e, e, 0) in calls and (_inverse(tau), tau, 1) in calls


def test_odd_check_alone_is_not_a_unique_secret_certificate():
    tau, e = (1, 2, 3, 0), tuple(range(4))
    query, _ = _oracle(tau)
    wrong = _compose(tau, _swap(4, 0, 1))
    assert wrong != tau
    assert query((_inverse(wrong), wrong, 1)) is query((e, e, 0))
    correct_query, calls = _oracle(tau)
    _assert_recovery(tau, correct_query, calls)


def test_recovery_probes_alone_cannot_distinguish_left_from_right_convention():
    tau = (1, 2, 3, 0)
    left_query, _ = _oracle(tau)
    calls = []

    def right_query(g):
        calls.append(g)
        return left_query(_group_inverse(g))

    _assert_recovery(tau, _CallOnly(right_query), calls)
    assert all(_group_inverse(g) == g for g in calls)


@pytest.mark.parametrize("merge_fibers", (False, True))
def test_finite_checks_do_not_verify_the_whole_oracle_promise(merge_fibers):
    tau, e = (1, 2, 3, 0), tuple(range(4))
    query, calls = _oracle(tau)
    unqueried = ((1, 2, 0, 3), e, 0)
    changed_label = object()

    def corrupt(g):
        if g == unqueried:
            return query((e, e, 0)) if merge_fibers else changed_label
        return query(g)

    corrupted = _CallOnly(corrupt)
    result = _assert_recovery(tau, corrupted, calls)
    assert unqueried not in calls
    assert result["source_promise_verified"] is False
    same_coset = _multiply(unqueried, (_inverse(tau), tau, 1))
    assert query(unqueried) is query(same_coset)
    assert corrupted(unqueried) is not corrupted(same_coset)
    if merge_fibers:
        assert query(unqueried) is not query((e, e, 0))
        assert corrupted(unqueried) is corrupted((e, e, 0))
