"""Exact controls for the prescribed, destructive Rees source tree only."""

from fractions import Fraction
from math import comb, factorial, prod

from flint import fmpz


def _integer(value, name, minimum):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


def _prime(p):
    _integer(p, "p", 2)
    if not fmpz(p).is_prime():
        raise ValueError("p must be prime")


def rank_mod(rows, p):
    """Small exact diagnostic, not a general diagonal-equation solver."""
    _prime(p)
    if not rows:
        return 0
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError("ragged matrix")
    a = [[int(x) % p for x in row] for row in rows]
    rank = 0
    for col in range(width):
        pivot = next((i for i in range(rank, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inverse = pow(a[rank][col], -1, p)
        a[rank] = [(x * inverse) % p for x in a[rank]]
        for i in range(len(a)):
            if i != rank:
                scale = a[i][col]
                a[i] = [(x - scale * y) % p for x, y in zip(a[i], a[rank])]
        rank += 1
        if rank == len(a):
            break
    return rank


def dependence_probability(p, dimension, count):
    """Probability that count IID uniform vectors in F_p^dimension depend."""
    _prime(p)
    _integer(dimension, "dimension", 1)
    _integer(count, "count", 0)
    if count > dimension:
        return Fraction(1)
    return 1 - prod(
        (1 - Fraction(1, p ** (dimension - i)) for i in range(count)),
        start=Fraction(1),
    )


def adaptive_pool_bound(p, dimension, inspected):
    """Union bound including arbitrary classical selection from one IID stream.

    A dependent short subset extends to one of size min(inspected, dimension).
    Pool labels can be retained, grouped adaptively, or discarded; no new
    correlated quantum-source operation is certified by this calculation.
    """
    _integer(inspected, "inspected", 0)
    _prime(p)
    _integer(dimension, "dimension", 1)
    if inspected > dimension:
        # The exact square-matrix dependence probability is < 1/(p-1).
        return min(Fraction(1), Fraction(comb(inspected, dimension), p - 1))
    k = min(inspected, dimension)
    probability = dependence_probability(p, dimension, k)
    return min(Fraction(1), comb(inspected, k) * probability)


def filiform_bracket(u, v, p):
    """Basis x,y_0,...,y_(c-1), [x,y_i]=y_(i+1); all y brackets vanish."""
    _prime(p)
    if len(u) != len(v) or len(u) < 2:
        raise ValueError("equal vectors of dimension >= 2 required")
    return (0, 0) + tuple(
        (u[0] * v[i - 1] - v[0] * u[i - 1]) % p
        for i in range(2, len(u))
    )


def profile(c, p, inspected_per_stage, native_budget):
    """Conditional architecture certificate, NOT an HSP success lower bound."""
    _integer(c, "class", 1)
    _prime(p)
    if p <= c or p == 2:
        raise ValueError("the Lazard family requires odd p > class")
    _integer(inspected_per_stage, "inspected_per_stage", 0)
    _integer(native_budget, "native_budget", 0)
    ranks = tuple(c + 1 - j for j in range(2, c + 1))
    stage_bounds = tuple(
        adaptive_pool_bound(p, r, inspected_per_stage) for r in ranks
    )
    exceptional_probability = min(Fraction(1), sum(stage_bounds, Fraction(0)))
    lifted_leaves = prod(r + 1 for r in ranks)
    assert lifted_leaves == factorial(c)
    native_copies = c * lifted_leaves
    return {
        "class": c,
        "prime": p,
        "lie_dimension": c + 1,
        "central_ranks": ranks,
        "cover_dimension": c + 1 + sum(ranks),
        "inspected_per_stage_cap": inspected_per_stage,
        "native_budget": native_budget,
        "stage_exception_bounds": stage_bounds,
        "exception_probability_bound": exceptional_probability,
        "lifted_leaves_if_no_exception": lifted_leaves,
        "native_copies_if_no_exception": native_copies,
        "terminal_source_success_upper_bound": (
            exceptional_probability if native_budget < native_copies else Fraction(1)
        ),
        "scope": "exact fresh-source descending full-grade destructive merges",
        "general_hsp_lower_bound": False,
        "algorithmic_advantage_established": False,
    }
