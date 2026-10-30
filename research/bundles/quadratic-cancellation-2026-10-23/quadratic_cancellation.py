"""Bounded prime-field implementation of Ivanyos--Santha Proposition 9.

Input is a public equation matrix, not a source of quantum states. Admission
uses a predeclared rank cap; no labels or copies are resampled after inspection.
This implements a published classical primitive, not a new quantum algorithm.
"""

from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
import random
import sys


WORK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORK / "central-rank-2026-10-23"))
sys.path.insert(0, str(WORK / "scalar-cancellation-2026-10-23"))
from central_rank import row_basis, valid_witness
from scalar_cancellation import (
    Counters, ScalarBackend, SmoothPowerRoots, check_prime, positive,
    verify_scalar,
)


def quadratic_arity(rank):
    if type(rank) is not int or rank < 0:
        raise ValueError("nonnegative integer rank cap required")
    return (rank + 1)**2


def linear_relation(rows, prime):
    """Return a checked ordinary dependence using the first free column."""
    basis = row_basis(rows, prime)
    width = len(rows[0])
    pivots = [next(i for i, value in enumerate(row) if value) for row in basis]
    free = next((i for i in range(width) if i not in pivots), None)
    if free is None:
        raise ValueError("a linearly dependent column bank is required")
    weights = [0] * width
    weights[free] = 1
    for pivot, row in zip(pivots, basis):
        weights[pivot] = -row[free] % prime
    if not valid_witness(rows, weights, prime, 1):
        raise ArithmeticError("ordinary dependence failed original-row check")
    return tuple(weights)


@dataclass(frozen=True)
class Representation:
    vector: tuple
    roots: tuple  # (original column index, nonzero square root coefficient)


@dataclass(frozen=True)
class QuadraticWitness:
    prime: int
    weights: tuple
    public_rank_cap: int
    observed_rank: int
    acquired_columns: int
    required_public_bank: int
    used_prefix_columns: int
    nonzero_weights: int
    method: str
    completed_first_level_groups: int
    linear_dependences_checked: int
    represented_vectors_checked: int
    four_cell_identities_checked: bool
    nonsquare: int | None
    root_counters: dict
    scalar_report: dict | None
    conditional_abort_bound: str
    probability_requires_iid_uniform_draws: bool
    randomness: str


def quadratic_witness(matrix, prime, rank_cap, *, rng=None, security_bits=64):
    """Solve sum_i matrix[j][i] * x_i**2 = 0 with a nonzero x.

    Supply at least (rank_cap+1)**2 columns BEFORE observing label rank.
    Randomness only selects a nonsquare and, if needed, solves one scalar
    ternary quadratic. Every randomized loop has a declared finite cap.
    Abort probability <= 2**(-security_bits) assumes fresh uniform draws;
    seeded runs certify exact arithmetic, not this probabilistic assumption.
    """
    check_prime(prime)
    positive(security_bits, "security bits")
    required = quadratic_arity(rank_cap)
    matrix = tuple(tuple(row) for row in matrix)
    basis = row_basis(matrix, prime)
    rank, width = len(basis), len(matrix[0])
    if rank > rank_cap:
        raise ValueError("observed rank exceeds the predeclared cap")
    if width < required:
        raise ValueError("full preallocated source bank was not supplied")
    used = quadratic_arity(rank)
    randomness = "system_random" if rng is None else "caller_supplied_replay_or_rng"
    rng = random.SystemRandom() if rng is None else rng
    stats = Counters()
    groups = relations = represented = 0
    four_cells_checked = False
    zeta = None
    scalar = None
    abort_bound = Fraction(0)

    def finish(representation, method):
        weights = [0] * width
        for index, coefficient in representation.roots:
            weights[index] = coefficient
        if not valid_witness(matrix, weights, prime, 2):
            raise ArithmeticError("original quadratic moment check failed")
        return QuadraticWitness(
            prime, tuple(weights), rank_cap, rank, width, required, used,
            sum(bool(x) for x in weights), method, groups, relations,
            represented, four_cells_checked, zeta, asdict(stats),
            None if scalar is None else scalar.report(), str(abort_bound),
            True, randomness,
        )

    if rank == 0:
        return finish(Representation((), ((0, 1),)), "zero_rank")

    roots = SmoothPowerRoots(prime, 2, rng=rng,
                             attempt_cap=security_bits + 1, counters=stats)
    abort_bound = roots.abort_bound
    zeta = roots.generator
    if pow(zeta, (prime-1)//2, prime) != prime-1:
        raise ArithmeticError("smooth generator is not a quadratic nonresidue")
    inverse_zeta = pow(zeta, -1, prime)
    root_cache = {}

    def classify(rows):
        nonlocal relations
        coefficients = linear_relation(rows, prime)
        relations += 1
        classes = [[], []]
        for index, coefficient in enumerate(coefficients):
            if not coefficient:
                continue
            character = pow(coefficient, (prime-1)//2, prime)
            kind = 0 if character == 1 else 1
            value = coefficient if kind == 0 else coefficient*inverse_zeta % prime
            if value not in root_cache:
                root_cache[value] = roots.root(value)
            beta = root_cache[value]
            if (type(beta) is not int or not 0 < beta < prime
                    or beta*beta % prime != value):
                raise ArithmeticError("classified coefficient has no verified square root")
            classes[kind].append((index, beta))
        return tuple(tuple(part) for part in classes)

    def combine(parts):
        nonlocal represented
        vector = [0] * rank
        coefficients = {}
        for representation, scale in parts:
            if type(scale) is not int or not 0 <= scale < prime:
                raise ArithmeticError("noncanonical combination scale")
            if not scale:
                continue
            for index, value in representation.roots:
                if index in coefficients:
                    raise ArithmeticError("representations must have disjoint supports")
                coefficient = value*scale % prime
                if not coefficient:
                    raise ArithmeticError("nonzero support coefficient was lost")
                coefficients[index] = coefficient
            for j, value in enumerate(representation.vector):
                vector[j] = (vector[j] + scale*scale*value) % prime
        direct = tuple(sum(basis[j][i]*coefficient**2
                           for i, coefficient in coefficients.items()) % prime
                       for j in range(rank))
        if tuple(vector) != direct:
            raise ArithmeticError("represented vector failed exact expansion")
        represented += 1
        return Representation(direct, tuple(sorted(coefficients.items())))

    def relation_holds(left, right):
        return all((a + zeta*b) % prime == 0
                   for a, b in zip(left.vector, right.vector))

    pairs = []
    for group in range(rank + 1):
        indices = range(group*(rank+1), (group+1)*(rank+1))
        bank = tuple(Representation(tuple(row[i] for row in basis), ((i, 1),))
                     for i in indices)
        rows = tuple(tuple(item.vector[j] for item in bank) for j in range(rank))
        classes = classify(rows)
        pair = tuple(combine((bank[i], beta) for i, beta in part) for part in classes)
        if not relation_holds(*pair):
            raise ArithmeticError("first-level coset relation failed")
        groups += 1
        for cell in pair:
            if cell.roots and not any(cell.vector):
                return finish(cell, "first_level_zero_cell")
        if any(not cell.roots for cell in pair):
            raise ArithmeticError("empty class without a returned zero witness")
        pairs.append(pair)

    rows = tuple(tuple(pair[0].vector[j] for pair in pairs) for j in range(rank))
    classes = classify(rows)
    # First index chooses a member of the pair; second chooses a coset class.
    cells = tuple(tuple(combine((pairs[i][a], gamma) for i, gamma in part)
                        for part in classes) for a in range(2))
    if not all(relation_holds(cells[a][0], cells[a][1]) for a in range(2)):
        raise ArithmeticError("second-level row relation failed")
    if not all(relation_holds(cells[0][b], cells[1][b]) for b in range(2)):
        raise ArithmeticError("second-level column relation failed")
    four_cells_checked = True
    for row in cells:
        for cell in row:
            if cell.roots and not any(cell.vector):
                return finish(cell, "second_level_zero_cell")
    if any(not cell.roots for row in cells for cell in row):
        raise ArithmeticError("empty second-level cell without a zero witness")

    scalar = ScalarBackend(prime, 2, max_scalar_calls=1,
                           security_bits=security_bits+1, rng=rng)
    scalar_coefficients = (zeta*zeta % prime, -2*zeta % prime, 1)
    delta = scalar(scalar_coefficients, 2, prime)
    verify_scalar(prime, 2, scalar_coefficients, delta)
    abort_bound += scalar.abort_bound
    if abort_bound > Fraction(1, 2**security_bits):
        raise ArithmeticError("global abort budget exceeded")
    d11, d12, d22 = delta
    result = combine(((cells[0][0], d11), (cells[0][1], d12),
                      (cells[1][0], d12), (cells[1][1], d22)))
    return finish(result, "four_cell_scalar")
