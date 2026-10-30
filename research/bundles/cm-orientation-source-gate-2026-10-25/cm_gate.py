"""Exact local controls for a CM-to-weak-isogeny source audit.

No varieties, secret isogenies, hiding functions or quantum candidates are
constructed. Exhaustive controls are explicitly capped and not algorithms
polynomial in log(prime). See CM_SOURCE_GATE.md for the geometric premises.
"""

from fractions import Fraction
from itertools import combinations, product

from sympy import isprime


CONJUGATION = (2, 3, 0, 1)
CM8_EMBEDDINGS = (1, 3, 7, 5)


def odd_prime(value):
    if type(value) is not int or value < 3 or not isprime(value):
        raise ValueError("an exact odd prime is required")
    return value


def frobenius_permutation(permutation):
    permutation = tuple(permutation)
    if (len(permutation) != 4 or any(type(x) is not int for x in permutation)
            or sorted(permutation) != list(range(4))):
        raise ValueError("four-element permutation required")
    if any(permutation[CONJUGATION[i]] != CONJUGATION[permutation[i]] for i in range(4)):
        raise ValueError("Frobenius must commute with CM conjugation")
    return permutation


def etale_counts(prime, permutation):
    """Rank-four etale CM algebra, faithful rank-one module, odd residue field.

    Frobenius cycles exchanged by conjugation contribute q^d-1; a cycle
    preserved by conjugation has even length 2d and contributes q^d+1.
    Geometric realizability is not asserted by these local data.
    """
    prime = odd_prime(prime)
    permutation = frobenius_permutation(permutation)
    cycles = []
    unseen = set(range(4))
    while unseen:
        first = min(unseen)
        cycle, current = set(), first
        while current not in cycle:
            cycle.add(current)
            current = permutation[current]
        unseen -= cycle
        cycles.append(frozenset(cycle))
    used, factors = set(), []
    for cycle in cycles:
        if cycle in used:
            continue
        conjugate = frozenset(CONJUGATION[i] for i in cycle)
        used.update((cycle, conjugate))
        if conjugate == cycle:
            if len(cycle) % 2:
                raise ArithmeticError("fixed-point-free conjugation has an odd orbit")
            factors.append(prime ** (len(cycle) // 2) + 1)
        else:
            if conjugate not in cycles:
                raise ArithmeticError("conjugate Frobenius orbit is missing")
            factors.append(prime ** len(cycle) - 1)
    order = 1
    for factor in factors:
        order *= factor
    choices = []
    for pair in combinations(range(4), 2):
        selected = set(pair)
        if (selected.isdisjoint(CONJUGATION[i] for i in selected)
                and {permutation[i] for i in selected} == selected):
            choices.append(list(pair))
    return {"norm_one_order": order, "projective_weak_classes": order // 2,
            "torus_factors": sorted(factors), "horizontal_planes": choices,
            "geometric_input_verified": False}


def cm8_permutation(prime):
    prime = odd_prime(prime)
    return tuple(CM8_EMBEDDINGS.index(prime * x % 8) for x in CM8_EMBEDDINGS)


def mul8(first, second, prime):
    """Multiplication in F_prime[x]/(x^4+1), ascending coefficients."""
    out = [0] * 4
    for i, a in enumerate(first):
        for j, b in enumerate(second):
            degree = i + j
            out[degree % 4] += (-1 if degree >= 4 else 1) * a * b
    return tuple(x % prime for x in out)


def bar8(value, prime):
    # x -> x^-1 = -x^3, so (1,x,x^2,x^3) -> (1,-x^3,-x^2,-x).
    a, b, c, d = value
    return (a % prime, -d % prime, -c % prime, -b % prime)


def exhaustive_cm8(prime, *, cap=100_000):
    prime = odd_prime(prime)
    if type(cap) is not int or cap < 1:
        raise ValueError("positive exact enumeration cap required")
    if prime ** 4 > cap:
        return {"status": "NOT_RUN_CAP", "elements_required": prime ** 4,
                "elements_checked": 0, "geometric_input_verified": False}
    units, projective = [], set()
    for value in product(range(prime), repeat=4):
        if mul8(value, bar8(value, prime), prime) == (1, 0, 0, 0):
            units.append(value)
            projective.add(min(value, tuple(-x % prime for x in value)))
    expected = etale_counts(prime, cm8_permutation(prime))
    if (len(units), len(projective)) != (expected["norm_one_order"], expected["projective_weak_classes"]):
        raise ArithmeticError("norm-one enumeration disagrees with torus count")
    return {"status": "EXACT_LOCAL_CONTROL", "elements_checked": prime ** 4,
            "norm_one_order": len(units), "projective_weak_classes": len(projective),
            "geometric_input_verified": False}


def independent_completion_bound(ell, levels):
    """Conditional quartic-CM bound, NOT a test for honest weak evaluations.

    Fixed oriented endpoints and fixed prime multiplier ell are essential.
    Each level is (auxiliary prime, Frobenius permutation). The numerator
    uses <=12 polarized oriented automorphisms for ANY quartic CM field,
    hence <=6 projective maps per kernel, and <=4 horizontal kernels.
    This conservative bound does not assume that endpoints or maps exist.
    """
    ell = odd_prime(ell)
    denominator, seen = 1, set()
    for prime, permutation in levels:
        prime = odd_prime(prime)
        if prime == ell or prime in seen:
            raise ValueError("distinct auxiliary primes coprime to ell required")
        seen.add(prime)
        denominator *= etale_counts(prime, permutation)["projective_weak_classes"]
    probability = min(Fraction(1), Fraction(24, denominator))
    return {"conditional_probability_upper": str(probability),
            "local_tuple_count": denominator, "global_tuple_upper": 24,
            "geometric_input_verified": False,
            "applies_to_honest_evaluations": False,
            "classical_hardness_established": False}
