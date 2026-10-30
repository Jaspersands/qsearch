"""Exact public-label rank compression and diagonal-witness composition.

The scalar solver is an explicit dependency, not hidden enumeration. No
quantum sources, hidden intersections, or group elements enter this module.
"""

from dataclasses import dataclass
from math import gcd, prod


def row_basis(matrix, prime):
    rows = [list(row) for row in matrix]
    if not rows or not rows[0] or any(len(row) != len(rows[0]) for row in rows):
        raise ValueError("nonempty rectangular equation matrix required")
    if any(type(x) is not int or not 0 <= x < prime for row in rows for x in row):
        raise ValueError("canonical prime-field entries required")
    pivot = 0
    for column in range(len(rows[0])):
        selected = next((i for i in range(pivot, len(rows)) if rows[i][column]), None)
        if selected is None:
            continue
        rows[pivot], rows[selected] = rows[selected], rows[pivot]
        scale = pow(rows[pivot][column], -1, prime)
        rows[pivot] = [(x * scale) % prime for x in rows[pivot]]
        for i in range(len(rows)):
            if i != pivot and rows[i][column]:
                scale = rows[i][column]
                rows[i] = [(x - scale*y) % prime for x, y in zip(rows[i], rows[pivot])]
        pivot += 1
        if pivot == len(rows):
            break
    return tuple(tuple(row) for row in rows[:pivot])


def valid_witness(matrix, weights, prime, degree):
    width = len(matrix[0])
    return (len(weights) == width and any(weights)
            and all(type(x) is int and 0 <= x < prime for x in weights)
            and all(sum(a * pow(x, degree, prime) for a, x in zip(row, weights)) % prime == 0
                    for row in matrix))


@dataclass(frozen=True)
class Witness:
    weights: tuple
    observed_rank: int
    acquired_columns: int
    used_prefix_columns: int
    scalar_calls: int
    scalar_degree: int


def bank_arity(degree, rank):
    return rank+1 if degree == 1 else (degree+1)**rank


def compressed_witness(matrix, prime, degree, rank_cap, scalar_solver):
    """Compose verified scalar solves on disjoint supports, then lift powers.

    prime is a caller-verified prime; degree is positive and below prime.
    scalar_solver(coefficients, reduced_degree, prime) must return a nonzero
    canonical witness or raise an explicit failure. It gets no hidden data.
    Its runtime guarantee is an additional contract, not verified by this API.
    """
    if type(prime) is not int or prime < 3 or type(degree) is not int or not 1 <= degree < prime:
        raise ValueError("require odd caller-verified prime and 1 <= degree < prime")
    if type(rank_cap) is not int or rank_cap < 0:
        raise ValueError("nonnegative public rank cap required")
    reduced = gcd(degree, prime-1)
    basis = row_basis(matrix, prime)
    rank, width = len(basis), len(matrix[0])
    if rank > rank_cap:
        raise ValueError("observed rank exceeds public promise; abort")
    # Admission is based on the public cap, not an unproved guess of full rank.
    if width < bank_arity(reduced, rank_cap):
        raise ValueError("the full preallocated source bank was not supplied")
    used = bank_arity(reduced, rank)
    calls = 0

    def solve(rows, columns):
        nonlocal calls
        if not rows:
            return [1]
        block_size = len(columns) // (reduced+1)
        blocks, subweights, coefficients = [], [], []
        for j in range(reduced+1):
            block = columns[j*block_size:(j+1)*block_size]
            local = solve(rows[:-1], block)
            blocks.append(block)
            subweights.append(local)
            coefficients.append(sum(rows[-1][i] * pow(x, reduced, prime)
                                    for i, x in zip(block, local)) % prime)
        top = tuple(scalar_solver(tuple(coefficients), reduced, prime))
        calls += 1
        if not valid_witness((coefficients,), top, prime, reduced):
            raise ArithmeticError("scalar backend returned an invalid witness")
        return [(scale*x) % prime for scale, local in zip(top, subweights) for x in local]

    if reduced == 1 and rank:
        restricted = row_basis([row[:used] for row in basis], prime)
        pivots = [next(i for i, value in enumerate(row) if value) for row in restricted]
        free = next(i for i in range(used) if i not in pivots)
        small = [0] * used
        small[free] = 1
        for pivot, row in zip(pivots, restricted):
            small[pivot] = -row[free] % prime
    else:
        small = solve(basis, list(range(used)))
    modulus = (prime-1) // reduced
    exponent = pow(degree // reduced, -1, modulus) if modulus > 1 else 0
    lifted = tuple(pow(x, exponent, prime) if x else 0 for x in small)
    lifted += (0,) * (width-used)
    if not valid_witness(matrix, lifted, prime, degree):
        raise ArithmeticError("original moment check failed")
    return Witness(lifted, rank, width, used, calls, reduced)


def terminal_envelope(k, central_ranks, prime, terminal_samples=1):
    """Conditional explicit-Lie Rees source counts, not quantum execution.

    central_ranks lists dim gamma_d(L) for d=2,...,c of the TERMINAL algebra.
    The caller supplies the valid bounded-codimension reduction and Lie data.
    """
    if type(k) is not int or k < 1 or type(terminal_samples) is not int or terminal_samples < 1:
        raise ValueError("positive codimension bound and terminal sample count required")
    ranks = tuple(central_ranks)
    if any(type(r) is not int or r < 1 for r in ranks):
        raise ValueError("central layer dimensions must be positive integers")
    c = len(ranks)+1
    if type(prime) is not int or prime <= c or prime % 2 == 0:
        raise ValueError("caller-verified odd prime must exceed actual class")
    if c > 2*k-1:
        raise ValueError("not the claimed bounded-index terminal class")
    if any(a <= b for a, b in zip(ranks, ranks[1:])):
        raise ValueError("nonzero lower-central ranks must strictly decrease")
    degrees = tuple(gcd(d, prime-1) for d in range(2, c+1))
    caps = tuple(min(k-1, rank) for rank in ranks)
    banks = tuple(bank_arity(degree, cap) for degree, cap in zip(degrees, caps))
    old = prod((degree+1)**rank for degree, rank in zip(degrees, ranks))
    demand, merges = terminal_samples, 0
    for bank in banks:  # Reverse recursion from degree-one output toward leaves.
        merges += demand
        demand *= bank
    leaves = demand
    return {
        "k": k, "actual_class": c, "central_ranks": ranks,
        "reduced_degrees": degrees, "public_rank_caps": caps,
        "banks_per_stage": banks,
        "terminal_samples": terminal_samples,
        "old_scalar_line_multiplier": old,
        "compressed_multiplier": prod(banks),
        "lifted_leaves": leaves, "original_queries_or_copies": c*leaves,
        "central_merge_nodes": merges,
        "complete_instruments": leaves+merges+terminal_samples,
        "uniform_parameter_envelope": (2*k)**((2*k-2)*(k-1)),
        "quantum_receiver_executed": False,
        "scalar_solver_implemented": False,
        "valid_terminal_input_verified": False,
        "speedup_claim": False,
    }
