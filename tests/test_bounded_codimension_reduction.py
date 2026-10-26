"""Exact controls for the public reduction, not a hidden-intersection learner.

Hidden subspaces are supplied only as test ground truth. Exhaustive small
fibers falsify identities; their enumeration is not an algorithmic resource.
"""
from itertools import combinations, product
import random

import pytest

from theorems.bounded_codimension_reduction import (
    PublicLieAlgebra, centralizer, combine, contains, freeze_lazard_algebra,
    make_abelian_probe, normalizer, reduce_at_known_intersection, units,
)
from theorems.symbolic_scalar_phase_erasure import (
    _fmpz_nullspace_basis, _fmpz_solve_coordinates,
)
from theorems.uniform_bch_rees import bch_via_ode


def filiform(n, p):
    def bracket(x, y):
        return (0, 0) + tuple((x[0]*y[j-1] - y[0]*x[j-1]) % p
                             for j in range(2, n))
    return PublicLieAlgebra(p, n, bracket)


def unitriangular(size, p):
    positions = tuple(combinations(range(size), 2))
    index = {ij: k for k, ij in enumerate(positions)}

    def bracket(x, y):
        return tuple(sum(x[index[i, k]]*y[index[k, j]]
                         - y[index[i, k]]*x[index[k, j]]
                         for k in range(i+1, j)) % p for i, j in positions)
    return PublicLieAlgebra(p, len(positions), bracket)


def same_span(a, b, p):
    return all(contains(a, v, p) for v in b) and all(contains(b, v, p) for v in a)


def intersection(algebra, a, b):
    if not a or not b:
        return ()
    rows = [tuple(v[j] for v in a) + tuple(-v[j] % algebra.p for v in b)
            for j in range(algebra.dimension)]
    coefficients = _fmpz_nullspace_basis(rows, len(a)+len(b), algebra.p)
    return tuple(algebra.span([combine(v[:len(a)], a, algebra.dimension, algebra.p)
                               for v in coefficients]))


def closed(algebra, basis):
    return all(contains(basis, algebra.bracket(x, y), algebra.p)
               for x in basis for y in basis)


def bch(algebra, c, x, y):
    return bch_via_ode(x, y, prime=algebra.p, nilpotency_class=c,
                      bracket=algebra.bracket)


@pytest.mark.parametrize("n,p", [(4, 5), (8, 17), (17, 19), (24, 101)])
def test_growing_class_core_free_hidden_hyperplane_in_abelian_ideal(n, p):
    probe = make_abelian_probe(filiform(n, p), 2)
    e = units(n)
    assert probe.nilpotency_class == n-1
    assert same_span(probe.ideal_flag, e[1:], p)
    hidden = e[1:-1]
    reduction = reduce_at_known_intersection(probe, hidden)
    assert same_span(reduction.normalizer_basis, e[1:], p)
    assert reduction.quotient.dimension == 1
    assert reduction.next_codimension_bound == 1
    assert same_span(reduction.pullback(()), hidden, p)
    assert not contains(hidden, e[-1], p)  # No nonzero ideal lies in this h.


def test_nonunique_abelian_ideal_does_not_force_a_false_intersection():
    probe = make_abelian_probe(filiform(3, 5), 2)
    e = units(3)
    assert probe.terminal
    assert same_span(probe.ideal_flag, (e[0], e[2]), 5)
    assert intersection(probe.algebra, (e[1],), probe.ideal_flag) == ()
    assert probe.algebra.dimension == probe.terminal_dimension_bound


def test_terminal_remainder_need_not_be_abelian_or_nil_two():
    def bracket(x, y):
        return (0, 0, (x[0]*y[1]-y[0]*x[1]) % 5,
                (x[0]*y[2]-y[0]*x[2]) % 5, (x[1]*y[2]-y[1]*x[2]) % 5)
    probe = make_abelian_probe(PublicLieAlgebra(5, 5, bracket), 3)
    assert probe.terminal
    assert probe.nilpotency_class == 3
    assert len(probe.ideal_flag) == 3
    assert probe.algebra.dimension == 5


@pytest.mark.parametrize("algebra", [filiform(9, 11), unitriangular(4, 5),
                                     unitriangular(5, 7)])
def test_public_ideal_flag_is_abelian_ideal_and_self_centralizing(algebra):
    probe = make_abelian_probe(algebra, 2)
    a, p = probe.ideal_flag, algebra.p
    for j, vector in enumerate(a):
        assert all(contains(a[:j], algebra.bracket(x, vector), p)
                   for x in units(algebra.dimension))
    assert all(not any(algebra.bracket(x, y)) for x in a for y in a)
    assert same_span(centralizer(algebra, a), a, p)
    assert algebra.dimension <= len(a)*(len(a)+1)//2
    assert probe.nilpotency_class <= 2*len(a)-1


def test_self_centralizing_subalgebra_cannot_replace_abelian_ideal():
    algebra = filiform(8, 17)
    e = units(8)
    bad_probe = (e[0], e[-1])
    assert same_span(centralizer(algebra, bad_probe), bad_probe, 17)
    assert closed(algebra, bad_probe)
    assert not contains(bad_probe, algebra.bracket(e[1], e[0]), 17)
    assert algebra.dimension > len(bad_probe)*(len(bad_probe)+1)//2


def test_incomplete_intersection_can_pass_public_checks_and_lose_hidden_elements():
    probe = make_abelian_probe(filiform(6, 7), 2)
    e = units(6)
    hidden, exact, incomplete = (e[0],) + e[2:], e[2:], e[2:-1]
    assert closed(probe.algebra, hidden)
    assert same_span(intersection(probe.algebra, hidden, probe.ideal_flag), exact, 7)
    assert all(contains(hidden, v, 7) for v in incomplete)
    bad = reduce_at_known_intersection(probe, incomplete)
    assert not contains(bad.normalizer_basis, e[0], 7)
    good = reduce_at_known_intersection(probe, exact)
    assert all(contains(good.normalizer_basis, v, 7) for v in hidden)
    assert good.quotient.dimension == 2
    assert good.quotient.nilpotency_class(units(2)) == 1


def test_noncentral_quotient_preserves_all_small_fibers_with_nonhomomorphic_sections():
    probe = make_abelian_probe(filiform(4, 5), 1)
    e, p = units(4), 5
    hidden = (e[0], e[2], e[3])
    step = reduce_at_known_intersection(probe, e[2:])
    quotient = step.quotient
    assert any(probe.algebra.bracket(e[0], e[2]))  # K is not central.
    assert any(probe.algebra.bracket(*step.section_basis))  # Section not a Lie map.
    hidden_quotient = tuple(quotient.span([step.project(v) for v in hidden]))
    assert same_span(step.pullback(hidden_quotient), hidden, p)
    points = tuple(product(range(p), repeat=2))
    changed_section = tuple(tuple((v[j] + e[2+i][j]) % p for j in range(4))
                            for i, v in enumerate(step.section_basis))
    for x, y in product(points, repeat=2):
        quotient_difference = tuple((b-a) % p for a, b in zip(x, y))
        expected = contains(hidden_quotient, quotient_difference, p)
        for section in (step.section_basis, changed_section):
            sx, sy = (combine(v, section, 4, p) for v in (x, y))
            difference = bch(probe.algebra, 3, tuple(-v % p for v in sx), sy)
            assert contains(hidden, difference, p) == expected
            assert step.project(bch(probe.algebra, 3, sx, sy)) == tuple(
                (a+b) % p for a, b in zip(x, y))


def test_normalizer_is_necessary_before_quotienting():
    probe = make_abelian_probe(filiform(5, 7), 2)
    e = units(5)
    step = reduce_at_known_intersection(probe, e[1:-1])
    assert not contains(step.intersection, probe.algebra.bracket(e[0], e[-2]), 7)
    with pytest.raises(ValueError, match="outside the normalizer"):
        step.project(e[0])


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_coordinate_changes_do_not_require_a_filiform_basis(seed):
    original = filiform(7, 11)
    rng = random.Random(seed)
    basis = [tuple(0 if j < i else 1 if j == i else rng.randrange(11)
                   for j in range(7)) for i in range(7)]
    rng.shuffle(basis)

    def coords(v):
        return _fmpz_solve_coordinates(basis, v, 11)

    def bracket(x, y):
        return coords(original.bracket(combine(x, basis, 7, 11),
                                       combine(y, basis, 7, 11)))
    changed = PublicLieAlgebra(11, 7, bracket)
    probe = make_abelian_probe(changed, 2)
    hidden = tuple(coords(v) for v in units(7)[1:-1])
    exact = intersection(changed, probe.ideal_flag, hidden)
    step = reduce_at_known_intersection(probe, exact)
    assert step.quotient.dimension == 1
    assert same_span(step.pullback(()), hidden, 11)


def test_all_coordinate_subalgebras_of_ut4_obey_recursive_invariants():
    original = unitriangular(4, 5)
    e = units(original.dimension)
    seen = 0
    for mask in range(1 << len(e)):
        hidden = tuple(e[i] for i in range(len(e)) if mask >> i & 1)
        if not closed(original, hidden):
            continue
        seen += 1
        algebra, k, steps = original, len(e)-len(hidden), []
        while algebra is not None:
            probe = make_abelian_probe(algebra, k)
            if probe.terminal or probe.nilpotency_class == 1 or k == 0:
                if probe.terminal:
                    assert algebra.dimension <= k*(k+1)//2
                    assert probe.nilpotency_class <= 2*k-1
                break
            exact = intersection(algebra, hidden, probe.ideal_flag)
            step = reduce_at_known_intersection(probe, exact)
            assert all(contains(step.normalizer_basis, v, 5) for v in hidden)
            next_hidden = (tuple(step.quotient.span([step.project(v) for v in hidden]))
                           if step.quotient is not None else ())
            assert same_span(step.pullback(next_hidden), hidden, 5)
            assert len(step.section_basis)-len(next_hidden) <= step.next_codimension_bound
            assert len(step.section_basis) < algebra.dimension
            steps.append(step)
            algebra, hidden, k = step.quotient, next_hidden, step.next_codimension_bound
        assert len(steps) <= original.dimension
    assert seen > 20


def test_zero_dimensional_quotient_and_empty_coordinates():
    algebra = PublicLieAlgebra(7, 3, lambda x, y: (0, 0, 0))
    probe = make_abelian_probe(algebra, 0)
    step = reduce_at_known_intersection(probe, units(3))
    assert step.quotient is None
    assert step.next_codimension_bound == 0
    assert step.lift(()) == (0, 0, 0)
    assert step.project((1, 2, 3)) == ()
    assert same_span(step.pullback(()), units(3), 7)


@pytest.mark.parametrize("k", [-1, 5, True, 1.5])
def test_invalid_codimension(k):
    with pytest.raises(ValueError, match="codimension bound"):
        make_abelian_probe(filiform(4, 5), k)


@pytest.mark.parametrize("bad", [(), ((1, 0, 0, 0),), ((0, 1, 0),),
                                 ((0, 1, 0, -1),)])
def test_invalid_intersection(bad):
    probe = make_abelian_probe(filiform(4, 5), 2)
    with pytest.raises(ValueError):
        reduce_at_known_intersection(probe, bad)


def test_intersection_and_normalizer_dimension_contradictions():
    probe = make_abelian_probe(filiform(6, 7), 1)
    with pytest.raises(ValueError, match="intersection dimension"):
        reduce_at_known_intersection(probe, units(6)[2:-1])
    # In UT4 an abelian hyperplane K in A can have normalizer codimension two.
    algebra = unitriangular(4, 5)
    probe = make_abelian_probe(algebra, 1)
    candidates = [probe.ideal_flag[:i] + probe.ideal_flag[i+1:]
                  for i in range(len(probe.ideal_flag))]
    witness = next(k for k in candidates if len(normalizer(algebra, k)) < 5)
    with pytest.raises(ValueError, match="normalizer drop"):
        reduce_at_known_intersection(probe, witness)


@pytest.mark.parametrize("vector", [(), (0,), (0, 0, 0), (0, 0, 0, 0, 0),
                                    (0, 0, 0, 5), (False, 0, 0, 0)])
def test_projection_rejects_wrong_width_or_noncanonical_coordinates(vector):
    step = reduce_at_known_intersection(make_abelian_probe(filiform(4, 5), 1),
                                        units(4)[2:])
    with pytest.raises(ValueError):
        step.project(vector)


@pytest.mark.parametrize("p,n", [(2, 2), (3, 4), (5, 6)])
def test_outside_lazard_contract(p, n):
    with pytest.raises(ValueError):
        make_abelian_probe(filiform(n, p), 1)


def test_freezing_validates_structure_and_does_not_certify_arbitrary_callback():
    with pytest.raises(ValueError, match="nonalternating"):
        freeze_lazard_algebra(PublicLieAlgebra(5, 2, lambda x, y: (x[0]*y[0] % 5, 0)))
    with pytest.raises(ValueError, match="nonantisymmetric"):
        freeze_lazard_algebra(PublicLieAlgebra(5, 2, lambda x, y: (x[0]*y[1] % 5, 0)))

    def non_lie(x, y):
        return (0, (x[0]*y[1]-y[0]*x[1]) % 5, (x[1]*y[2]-y[1]*x[2]) % 5)
    with pytest.raises(ValueError, match="Jacobi"):
        freeze_lazard_algebra(PublicLieAlgebra(5, 3, non_lie))
    with pytest.raises(ValueError, match="not nilpotent"):
        freeze_lazard_algebra(PublicLieAlgebra(5, 2, lambda x, y:
                                             (0, (x[0]*y[1]-y[0]*x[1]) % 5)))

    def nonlinear(x, y):
        return ((x[0]*x[1]*y[0]) % 5, 0)
    callback = PublicLieAlgebra(5, 2, nonlinear)
    frozen, c = freeze_lazard_algebra(callback)
    assert c == 1
    assert callback.bracket((1, 1), (1, 0)) != frozen.bracket((1, 1), (1, 0))
    assert frozen.bracket((1, 1), (1, 0)) == (0, 0)
