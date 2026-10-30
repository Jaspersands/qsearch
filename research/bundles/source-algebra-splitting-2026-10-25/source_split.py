"""Split a supplied source order at factored unramified levels.

No torsion points or target order are inputs. Primality and source maximality
are mathematical input promises; finite checks do not authenticate provenance.
"""

from itertools import combinations
from pathlib import Path
from random import SystemRandom
import sys

from sympy import Matrix, eye, zeros
from sympy.ntheory.modular import crt

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "double-level-source-2026-10-25"))
from double_level_source import checked_factors, split_at_two
from kernel_output import action, check_split, coordinate_map, inverse_mod, mod


class SearchBudgetExceeded(RuntimeError):
    """UNKNOWN after a sampling cap, not a nonsplitting certificate."""


def square_root(value, prime, rng, trials):
    """Tonelli-Shanks with bounded random nonresidue acquisition."""
    value %= prime
    if value == 0:
        return 0, 0
    if pow(value, (prime-1)//2, prime) != 1:
        raise ValueError("nonzero square required")
    if prime % 4 == 3:
        return pow(value, (prime+1)//4, prime), 0
    odd, exponent = prime-1, 0
    while odd % 2 == 0:
        odd //= 2
        exponent += 1
    for draw in range(1, trials+1):
        nonresidue = rng.randrange(1, prime)
        if pow(nonresidue, (prime-1)//2, prime) == prime-1:
            break
    else:
        raise SearchBudgetExceeded("UNKNOWN: nonresidue sampling cap")
    c = pow(nonresidue, odd, prime)
    root = pow(value, (odd+1)//2, prime)
    residue = pow(value, odd, prime)
    while residue != 1:
        power, index = residue, 0
        while power != 1 and index < exponent:
            power = power*power % prime
            index += 1
        if index >= exponent:
            raise ValueError("prime-field square-root promise failed")
        correction = pow(c, 1 << (exponent-index-1), prime)
        root = root*correction % prime
        c = correction*correction % prime
        residue = residue*c % prime
        exponent = index
    if root*root % prime != value:
        raise ArithmeticError("square-root verification failed")
    return root, draw


def module_action(order, module, prime, modulus):
    rows = next((pair for pair in combinations(range(4), 2)
                 if int(module[list(pair), :].det()) % prime), None)
    if rows is None:
        raise ValueError("rank-two direct summand required")
    inverse = inverse_mod(module[list(rows), :], modulus)
    actions = []
    for i in range(4):
        image = Matrix.hstack(*(order.multiply(eye(4)[:, i], module[:, j]) for j in range(2)))
        coefficients = mod(inverse*image[list(rows), :], modulus)
        if mod(module*coefficients-image, modulus) != zeros(4, 2):
            raise ValueError("left ideal not stable under the source order")
        actions.append(coefficients)
    result = tuple(actions)
    check_split(order, result, modulus)
    return result


def initial_odd_split(order, prime, rng, trials):
    for draw in range(1, trials+1):
        element = Matrix([rng.randrange(prime) for _ in range(4)])
        trace = int((order.traces*element)[0])
        norm = (order.traces*order.multiply(order.star(element), element))[0]/2
        if norm.q != 1:
            raise ValueError("integral source reduced norm required")
        discriminant = (trace*trace-4*int(norm)) % prime
        if discriminant and pow(discriminant, (prime-1)//2, prime) == 1:
            break
    else:
        raise SearchBudgetExceeded("UNKNOWN: split-semisimple element sampling cap")
    root, nonresidue_draws = square_root(discriminant, prime, rng, trials)
    eigenvalue = (trace-root)*pow(2, -1, prime) % prime
    e = mod((element-eigenvalue*order.unit)*pow(root, -1, prime), prime)
    if mod(order.multiply(e, e)-e, prime) != zeros(4, 1):
        raise ValueError("source characteristic-polynomial identity failed")
    columns = [mod(order.multiply(eye(4)[:, i], e), prime) for i in range(4)]
    for pair in combinations(range(4), 2):
        module = Matrix.hstack(*(columns[i] for i in pair))
        if any(int(module[list(rows), :].det()) % prime
               for rows in combinations(range(4), 2)):
            result = module_action(order, module, prime, prime)
            return result, {"semisimple_draws": draw, "nonresidue_draws": nonresidue_draws}
    raise ValueError("idempotent does not give a rank-two source ideal")


def lift_once(order, actions, prime, modulus):
    """Lift while preserving the specified coordinates, not merely conjugacy."""
    check_split(order, actions, modulus)
    inverse = inverse_mod(coordinate_map(actions), modulus)
    e0 = mod(inverse*Matrix([1, 0, 0, 0]), modulus)
    next_modulus = prime*modulus
    square = order.multiply(e0, e0)
    e = mod(3*square-2*order.multiply(square, e0), next_modulus)
    if mod(order.multiply(e, e)-e, next_modulus) != zeros(4, 1):
        raise ArithmeticError("idempotent precision lift failed")
    e21 = mod(inverse*Matrix([0, 0, 1, 0]), modulus)
    module = Matrix.hstack(e, mod(order.multiply(e21, e), next_modulus))
    result = module_action(order, module, prime, next_modulus)
    if any(mod(a-b, modulus) != zeros(2) for a, b in zip(result, actions)):
        raise ArithmeticError("lift changed source coordinates")
    return result


def source_split(order, modulus, factors, characteristic, rng=None, trials=64):
    """Capped Las Vegas splitter, conditional on the declared source promises."""
    factors = checked_factors(modulus, factors)
    if type(trials) is not int or trials < 1:
        raise ValueError("positive sampling cap required")
    if any(prime == characteristic for prime, _ in factors):
        raise ValueError("ramified characteristic is not a split level")
    rng = SystemRandom() if rng is None else rng
    local, records, levels = [], [], []
    for prime, exponent in factors:
        if prime == 2:
            actions = split_at_two(order)
            cost = {"semisimple_draws": 0, "nonresidue_draws": 0,
                    "constant_size_dyadic_search": True}
        else:
            actions, cost = initial_odd_split(order, prime, rng, trials)
        level = prime
        for _ in range(1, exponent):
            actions = lift_once(order, actions, prime, level)
            level *= prime
        local.append(actions)
        levels.append(level)
        records.append({"prime": prime, "exponent": exponent, "lift_steps": exponent-1, **cost})
    result = tuple(Matrix(2, 2, [int(crt(levels, [entry[i][j] for entry in local])[0])
                                for j in range(4)]) for i in range(4))
    check_split(order, result, modulus)
    return result, {"modulus": modulus, "prime_powers": records, "sampling_cap": trials,
                    "large_prime_element_enumeration": False, "native_torsion_used": False,
                    "target_order_used": False, "input_factorization_required": True,
                    "source_maximal_order_promised": True, "global_dictionary_constructed": False}
