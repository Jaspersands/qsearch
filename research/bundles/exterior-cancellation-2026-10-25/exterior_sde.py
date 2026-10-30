"""Exact exterior-collision SDE arithmetic; not a quantum receiver.

Adapts Ivanyos--Santha's collision construction. Public bank sizes are
fixed before labels are inspected. Random loop caps do not clock FLINT.
"""

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from math import comb, gcd, prod
import random

from flint import fmpz, fmpz_mod_ctx, fmpz_mod_mat, fmpz_mod_poly_ctx


def _integer(value, minimum, name):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


def _prime(p):
    _integer(p, 3, "prime")
    if not fmpz(p).is_prime():
        raise ValueError("odd prime required")


def collision_arity(index, width):
    _integer(index, 1, "power index")
    _integer(width, 1, "equation width")
    return prod(width * comb(index - 1, j) + 1 for j in range(index))


@dataclass(frozen=True)
class Plan:
    prime: int
    degree: int
    width: int
    index: int
    lift_exponent: int
    collision_columns: int
    rounds: int
    required_columns: int
    mode: str


def plan(p, degree, width):
    _prime(p)
    _integer(degree, 1, "degree")
    _integer(width, 1, "equation width")
    if degree >= p:
        raise ValueError("degree must be below the prime")
    index = gcd(degree, p - 1)
    modulus = (p - 1) // index
    lift = pow(degree // index, -1, modulus) if modulus > 1 else 1
    bank = collision_arity(index, width)
    if ((p - 1) // index) % 2 == 0:
        rounds, mode = 1, "signed_collision"
    elif p > 16 * (index - 1)**4:
        rounds, mode = 2, "ternary_accumulation"
    else:
        rounds, mode = index.bit_length(), "degree_bounded_accumulation"
    return Plan(p, degree, width, index, lift, bank, rounds, bank**rounds, mode)


def _columns(columns, p, width):
    if not columns or any(len(v) != width for v in columns):
        raise ValueError("nonempty equal-width columns required")
    if any(type(a) is not int or not 0 <= a < p for v in columns for a in v):
        raise ValueError("canonical prime-field coefficients required")


def represented(columns, weights, degree, p):
    width = len(columns[0])
    return tuple(sum(pow(root, degree, p) * columns[i][j]
                     for i, root in weights.items()) % p for j in range(width))


def verify_witness(p, degree, columns, weights):
    _prime(p)
    _integer(degree, 1, "degree")
    if not columns or not columns[0]:
        raise ValueError("nonempty columns required")
    _columns(columns, p, len(columns[0]))
    if (len(weights) != len(columns)
            or any(type(s) is not int or not 0 <= s < p for s in weights)
            or not any(weights)):
        raise ValueError("nonzero canonical witness of matching length required")
    if any(represented(columns, dict(enumerate(weights)), degree, p)):
        raise ArithmeticError("original moment does not vanish")


def dependence(columns, p):
    if not columns:
        raise ValueError("empty dependence input")
    rows = list(map(list, zip(*columns)))
    reduced, rank = fmpz_mod_mat(rows, fmpz_mod_ctx(p)).rref()
    pivots = [next(j for j in range(len(columns)) if int(reduced[i, j]))
              for i in range(rank)]
    free = next((j for j in range(len(columns)) if j not in pivots), None)
    if free is None:
        raise ArithmeticError("promised dependence is absent")
    result = [0] * len(columns)
    result[free] = 1
    for i, pivot in enumerate(pivots):
        result[pivot] = -int(reduced[i, free]) % p
    if any(sum(a * col[j] for a, col in zip(result, columns)) % p
           for j in range(len(columns[0]))):
        raise ArithmeticError("invalid modular dependence")
    return result


def prime_divisors(n):
    divisors, divisor = [], 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            divisors.append(divisor)
            while n % divisor == 0:
                n //= divisor
        divisor += 1
    if n > 1:
        divisors.append(n)
    return divisors


class PowerClasses:
    def __init__(self, p, index, rng, cap):
        _prime(p)
        _integer(index, 1, "power index")
        _integer(cap, 1, "attempt cap")
        if (p - 1) % index:
            raise ValueError("power index must divide p-1")
        self.p, self.index, self.rng = p, index, rng
        self.polys = fmpz_mod_poly_ctx(p)
        self.root_calls = 0
        self.cache = {}
        self.draws = 0
        divisors = prime_divisors(index)
        if index == 1:
            generator = 1
        else:
            for self.draws in range(1, cap + 1):
                generator = rng.randrange(1, p)
                if type(generator) is not int or not 1 <= generator < p:
                    raise ValueError("random source returned a noncanonical element")
                if all(pow(generator, (p - 1) // divisor, p) != 1
                       for divisor in divisors):
                    break
            else:
                raise RuntimeError("power-class generator cap exhausted")
        self.representatives = tuple(pow(generator, i, p) for i in range(index))
        self.characters = tuple(pow(a, (p - 1) // index, p)
                                for a in self.representatives)
        if len(set(self.characters)) != index:
            raise ArithmeticError("power classes are not distinct")
        phi = prod(Fraction(divisor - 1, divisor) for divisor in divisors)
        self.abort_bound = (1 - phi)**cap if index > 1 else Fraction(0)

    def root(self, value):
        p, d = self.p, self.index
        if type(value) is not int or not 0 <= value < p:
            raise ValueError("canonical power residue required")
        if value == 0:
            return 0
        if pow(value, (p - 1) // d, p) != 1:
            raise ValueError("not a certified power residue")
        if value not in self.cache:
            if d == 1:
                root = value
            else:
                found = self.polys([-value] + [0] * (d - 1) + [1]).roots()
                self.root_calls += 1
                if not found:
                    raise ArithmeticError("missing root of certified residue")
                root = min(int(item[0]) for item in found)
            if not 0 < root < p or pow(root, d, p) != value:
                raise ArithmeticError("invalid power root")
            self.cache[value] = root
        return self.cache[value]

    def classify(self, value):
        p = self.p
        if not 0 < value < p:
            raise ValueError("nonzero canonical classification input required")
        index = self.characters.index(pow(value, (p - 1) // self.index, p))
        root = self.root(value * pow(self.representatives[index], -1, p) % p)
        return index, root


def contract(values, degree, representatives, p, width):
    output = {key: [0] * width
              for key in combinations(range(len(representatives)), degree - 1)}
    for key, vector in values.items():
        for position, letter in enumerate(key):
            shorter = key[:position] + key[position + 1:]
            factor = (-1)**position * representatives[letter]
            for j, value in enumerate(vector):
                output[shorter][j] = (output[shorter][j] + factor * value) % p
    return output


@dataclass
class Collision:
    positive: dict
    negative: dict
    value: tuple


def exterior_collision(columns, context, stats):
    p, d = context.p, context.index
    width = len(columns[0])
    required = collision_arity(d, width)
    if len(columns) != required:
        raise ValueError("collision requires its complete public bank")
    _columns(columns, p, width)
    sizes = [1]
    for j in range(d):
        sizes.append(sizes[-1] * (width * comb(d - 1, j) + 1))

    def build(start, level):
        if not level:
            return {start: ((), 1, 1)}, {(): tuple(columns[start])}
        count = width * comb(d - 1, level - 1) + 1
        children = [build(start + k * sizes[level - 1], level - 1)
                    for k in range(count)]
        projected_keys = tuple(combinations(range(d - 1), level - 1))
        vectors = [tuple(a for key in projected_keys for a in values[key])
                   for _, values in children]
        relation = dependence(vectors, p)
        if not any(relation):
            raise ArithmeticError("all-zero intermediate dependence")
        first = next(value for value in relation if value)
        old_class, _ = context.classify(first)
        scalar = context.representatives[level - 1] * pow(
            context.representatives[old_class], -1, p) % p
        relation = [scalar * a % p for a in relation]
        terms = {}
        values = {key: [0] * width for key in combinations(range(d), level)}
        for alpha, (child_terms, child_values) in zip(relation, children):
            if not alpha:
                continue
            letter, root = context.classify(alpha)
            if not 0 < root < p or context.representatives[letter] * pow(root, d, p) % p != alpha:
                raise ArithmeticError("invalid classified dependence coefficient")
            root_power = pow(root, d, p)
            for key, vector in child_values.items():
                if letter in key:
                    continue
                sign = (-1)**sum(a > letter for a in key)
                new_key = tuple(sorted(key + (letter,)))
                for j, value in enumerate(vector):
                    values[new_key][j] = (values[new_key][j] + sign * root_power * value) % p
            for index, (key, sign, coefficient) in child_terms.items():
                if letter in key:
                    continue
                if index in terms:
                    raise ArithmeticError("overlapping collision supports")
                wedge_sign = (-1)**sum(a > letter for a in key)
                terms[index] = (tuple(sorted(key + (letter,))), sign * wedge_sign,
                                root * coefficient % p)
        distinguished = tuple(range(level))
        if not any(key == distinguished and sign == 1 for key, sign, _ in terms.values()):
            raise ArithmeticError("lost positive distinguished support")
        if any(any(v) for v in contract(values, level, context.representatives, p, width).values()):
            raise ArithmeticError("exterior contraction invariant failed")
        expanded = {key: [0] * width for key in values}
        for index, (key, sign, root) in terms.items():
            for j, a in enumerate(columns[index]):
                expanded[key][j] = (expanded[key][j] + sign * pow(root, d, p) * a) % p
        if expanded != values:
            raise ArithmeticError("signed support does not represent exterior data")
        stats["exterior_nodes"] += 1
        stats["contraction_checks"] += 1
        stats["represented_node_checks"] += 1
        stats["maximum_dependence_dimension"] = max(
            stats["maximum_dependence_dimension"], len(vectors[0]))
        return terms, values

    terms, values = build(0, d)
    if any(any(v) for v in values.values()):
        raise ArithmeticError("top exterior value is not zero")
    positive = {i: root for i, (_, sign, root) in terms.items() if sign == 1}
    negative = {i: root for i, (_, sign, root) in terms.items() if sign == -1}
    value = represented(columns, positive, d, p)
    if not positive or positive.keys() & negative.keys() or value != represented(columns, negative, d, p):
        raise ArithmeticError("invalid disjoint collision")
    return Collision(positive, negative, value)


def scalar_row(context, mode, cap):
    p, d = context.p, context.index
    if mode == "ternary_accumulation":
        if not p > 16 * (d - 1)**4:
            raise ValueError("ternary Weil guard absent")
        for trial in range(1, cap + 1):
            x = context.rng.randrange(p)
            if type(x) is not int or not 0 <= x < p:
                raise ValueError("random source returned a noncanonical element")
            value = (-1 - pow(x, d, p)) % p
            if not value or pow(value, (p - 1) // d, p) == 1:
                row = (1, x, context.root(value))
                return row, trial, Fraction(2*d - 1, 2*d)**cap, 0
        raise RuntimeError("ternary Fermat sampling cap exhausted")
    if mode != "degree_bounded_accumulation" or p > 16 * (d - 1)**4:
        raise ValueError("field enumeration lacks its degree bound")
    roots = {}
    for value in range(p):
        roots.setdefault(pow(value, d, p), value)
    levels = [{0: None}]
    for _ in range(d):
        current = {}
        for before in levels[-1]:
            for power, root in roots.items():
                after = (before + power) % p
                current.setdefault(after, (before, root))
                if p-1 in current:
                    break
            if p-1 in current:
                break
        levels.append(current)
        if p-1 in current:
            recovered, value = [], p-1
            for level in reversed(levels[1:]):
                value, root = level[value]
                recovered.append(root)
            return (1,) + tuple(reversed(recovered)), 0, Fraction(0), p
    raise ArithmeticError("scalar Chevalley-Warning existence contradicted")


@dataclass(frozen=True)
class Witness:
    weights: tuple
    plan: Plan
    acquired_columns: int
    statistics: dict
    sampling_abort_bound: Fraction
    root_runtime_locally_clocked: bool = False


def solve(columns, setup, *, rng=None, attempt_cap=256):
    if not isinstance(setup, Plan) or setup != plan(setup.prime, setup.degree, setup.width):
        raise ValueError("valid public pre-acquisition plan required")
    _integer(attempt_cap, 1, "attempt cap")
    p, d, width = setup.prime, setup.index, setup.width
    _columns(columns, p, width)
    if len(columns) < setup.required_columns:
        raise ValueError("insufficient already-acquired columns")
    rng = random.SystemRandom() if rng is None else rng
    context = PowerClasses(p, d, rng, attempt_cap)
    stats = {"exterior_nodes": 0, "contraction_checks": 0,
             "represented_node_checks": 0, "maximum_dependence_dimension": 0,
             "fermat_trials": 0, "enumerated_field_elements": 0,
             "zero_representation_early_exit": False}
    budget = context.abort_bound

    if setup.mode == "signed_collision":
        collision = exterior_collision(columns[:setup.collision_columns], context, stats)
        negative_root = context.root(p - 1)
        solution = dict(collision.positive)
        solution.update({i: negative_root * root % p for i, root in collision.negative.items()})
    else:
        row, trials, abort, enumerated = scalar_row(context, setup.mode, attempt_cap)
        if (not row or len(row) > 2**setup.rounds
                or any(type(a) is not int or not 0 <= a < p for a in row)
                or not any(row) or sum(pow(a, d, p) for a in row) % p):
            raise ArithmeticError("invalid scalar combining row")
        stats["fermat_trials"], stats["enumerated_field_elements"] = trials, enumerated
        budget = min(Fraction(1), budget + abort)

        class FoundZero(Exception):
            def __init__(self, representation):
                self.representation = representation

        def accumulate(start, rounds):
            if not rounds:
                return tuple(columns[start]), [{start: 1}]
            bank = setup.collision_columns
            child_size = bank**(rounds-1)
            children = [accumulate(start + i*child_size, rounds-1) for i in range(bank)]
            collision = exterior_collision([value for value, _ in children], context, stats)
            representations = []
            for side in (collision.positive, collision.negative):
                if not side:
                    continue
                for index in range(2**(rounds-1)):
                    representation = {}
                    for child, root in side.items():
                        for leaf, coefficient in children[child][1][index].items():
                            if leaf in representation:
                                raise ArithmeticError("overlapping accumulated supports")
                            representation[leaf] = root * coefficient % p
                    if not representation or represented(columns, representation, d, p) != collision.value:
                        raise ArithmeticError("invalid accumulated representation")
                    representations.append(representation)
            if not any(collision.value):
                raise FoundZero(representations[0])
            if len(representations) != 2**rounds:
                raise ArithmeticError("nonzero value lacks all disjoint representations")
            supports = [set(rep) for rep in representations]
            if sum(map(len, supports)) != len(set().union(*supports)):
                raise ArithmeticError("accumulated representations share leaves")
            return collision.value, representations

        try:
            _, representations = accumulate(0, setup.rounds)
            solution = {}
            for scalar, representation in zip(row, representations):
                if scalar:
                    solution.update({i: scalar * root % p for i, root in representation.items()})
        except FoundZero as found:
            solution = found.representation
            stats["zero_representation_early_exit"] = True

    weights = [0] * len(columns)
    for index, root in solution.items():
        weights[index] = pow(root, setup.lift_exponent, p)
    verify_witness(p, setup.degree, columns, weights)
    stats.update(power_class_draws=context.draws, root_calls=context.root_calls,
                 active_scales=sum(bool(s) for s in weights))
    return Witness(tuple(weights), setup, len(columns), stats, budget)
