"""Exact accounting for a published fixed-point bound applied to opaque HSP.

No algorithm discovery or quantum execution is performed here. Enumeration
is a finite algebra control; the universal bound comes from GK Lemma 3.14.
"""

from collections import deque
from fractions import Fraction
from math import comb, isqrt, prod
from pathlib import Path
import sys

from flint import fmpz
from sympy import integer_nthroot

WORK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORK / "orthogonal-three-probe-2026-10-23"))
import orthogonal_probe as op


def odd_prime_power(q):
    if type(q) is not int or q < 3 or q % 2 == 0:
        return False
    if fmpz(q).is_prime():
        return True
    for exponent in range(2, q.bit_length()):
        base, exact = integer_nthroot(q, exponent)
        if exact and fmpz(base).is_prime():
            return True
    return False


def validate(n, q):
    if type(n) is not int or n < 3 or not odd_prime_power(q):
        raise ValueError("Witt rank >=3 and odd prime-power field order required")


def component_size(n, q):
    validate(n, q)
    return prod(q**i + 1 for i in range(1, n))


def fixed_point_bound(n, q):
    """Noncentral isometries only; never apply this to +/-I."""
    validate(n, q)
    return Fraction(2, q**(n-2)) + Fraction(1, q**(n-1))


def root_fixed_point_ratio(n, q):
    validate(n, q)
    return Fraction((q+1)*q**(n-2)+1, (q**(n-2)+1)*(q**(n-1)+1))


def classical_success_bound(n, q, queries, *, label_model="random_opaque"):
    """Average-case success upper bound; arbitrary adaptive full-group queries.

    The hidden space is uniform in a known component and coset names are
    randomly injectively relabeled. This does NOT bound structured evaluators.
    """
    validate(n, q)
    if label_model != "random_opaque":
        raise ValueError("bound requires random opaque labels, not natural encodings")
    if type(queries) is not int or queries < 0:
        raise ValueError("nonnegative integer query count required")
    return min(Fraction(1), Fraction(1, component_size(n, q))
               + comb(queries, 2)*fixed_point_bound(n, q))


def necessary_queries(n, q, target=Fraction(2, 3)):
    """Necessary, NOT sufficient, query count for the given success target."""
    validate(n, q)
    if not isinstance(target, (int, Fraction)) or not 0 < target < 1:
        raise ValueError("exact success probability strictly between zero and one required")
    required_pairs = (target - Fraction(1, component_size(n, q))) / fixed_point_bound(n, q)
    if required_pairs <= 0:
        return 0
    pairs = -(-required_pairs.numerator // required_pairs.denominator)
    result = (1 + isqrt(1 + 8*pairs)) // 2
    while comb(result, 2) < pairs:
        result += 1
    return result


def scalar_sign(g, p):
    for sign in (1, p-1):
        if g == tuple(tuple(sign*value % p for value in row) for row in op.eye(len(g))):
            return sign
    return None


def central_query_key(g, p):
    """Public equivalence class modulo +/-I, not a secret coset label."""
    negative = tuple(tuple(-value % p for value in row) for row in g)
    return min(g, negative)


def swap_pair(n, index):
    g = [list(row) for row in op.eye(2*n)]
    g[index], g[n+index] = g[n+index], g[index]
    return tuple(tuple(row) for row in g)


def all_maximal(n, p, *, cap=3000):
    """Exponential finite control; refuses an oversized complete orbit."""
    validate(n, p)
    if not fmpz(p).is_prime():
        raise ValueError("matrix controls implement prime fields only")
    if 2*component_size(n, p) > cap:
        raise ValueError("finite enumeration cap exceeded")
    start = op.eye(2*n)[:n]
    generators = op.certificate_matrices(start, p)
    generators += tuple(swap_pair(n, i) for i in range(n))
    found, queue = {start}, deque([start])
    while queue:
        current = queue.popleft()
        for g in generators:
            moved = op.image(g, current, p)
            if moved not in found:
                found.add(moved)
                queue.append(moved)
    if len(found) != 2*component_size(n, p):
        raise ArithmeticError("orbit traversal did not cover both complete components")
    return tuple(sorted(found))


def component(space, p):
    n = len(space)
    intersection = op.intersection(space, op.eye(2*n)[:n], 2*n, p)
    return (n-len(intersection)) % 2


def structural_controls(n, p):
    """Representative legal matrices, NOT an exhaustive group classifier."""
    standard = op.eye(2*n)[:n]
    tests = op.certificate_matrices(standard, p)
    diagonal = [1]*(2*n)
    diagonal[0] = 2 % p
    diagonal[n] = pow(2, -1, p)
    semisimple = tuple(tuple(value*entry % p for entry in row)
                       for value, row in zip(diagonal, op.eye(2*n)))
    root = tests[-1]
    switched = swap_pair(n, 0)
    return {
        "levi_root": tests[0],
        "upper_root": root,
        "lower_root": op.transpose(root),
        "semisimple": semisimple,
        "component_switch": switched,
        "two_switches": op.mm(switched, swap_pair(n, 1), p),
        "mixed": op.mm(root, op.mm(semisimple, op.transpose(root), p), p),
    }


def finite_control(n, p):
    spaces = all_maximal(n, p)
    components = [tuple(space for space in spaces if component(space, p) == c)
                  for c in (0, 1)]
    controls = {}
    for name, g in structural_controls(n, p).items():
        if not op.is_orthogonal(g, p) or scalar_sign(g, p) is not None:
            raise ArithmeticError("control must be a noncentral isometry")
        fixed = [sum(op.image(g, space, p) == space for space in sector)
                 for sector in components]
        ratios = [Fraction(count, len(sector)) for count, sector in zip(fixed, components)]
        if not all(ratio < fixed_point_bound(n, p) for ratio in ratios):
            raise ArithmeticError("published bound failed a finite control")
        if name in ("upper_root", "lower_root", "levi_root"):
            if ratios != [root_fixed_point_ratio(n, p)]*2:
                raise ArithmeticError("root incidence formula failed")
        if name == "component_switch" and any(fixed):
            raise ArithmeticError("determinant-minus-one element fixed a component")
        controls[name] = {"fixed_in_components": fixed, "ratios": list(map(str, ratios))}
    return {"rank": n, "prime": p, "spaces_exhausted": len(spaces),
            "component_sizes": list(map(len, components)), "controls": controls,
            "entire_group_exhausted": False, "bound": str(fixed_point_bound(n, p))}
