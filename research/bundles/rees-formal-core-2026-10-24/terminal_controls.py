"""Exact terminal-measurement controls and charged sampling budgets.

The finite density calculations are proof diagnostics, never an oracle
benchmark or scalable quantum implementation. Budget formulas assume the
declared field exists and fresh independent terminal sources are supplied.
"""

from fractions import Fraction
from itertools import product
from math import prod


def _natural(value, name, minimum=0):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def spanning_probability(field_order, rank, sample_count):
    """Exact IID uniform spanning probability in a rank-dimensional vector space."""
    q = _natural(field_order, "field order", 2)
    r = _natural(rank, "rank")
    k = _natural(sample_count, "sample count")
    if k < r:
        return Fraction(0)
    return prod((1 - Fraction(q**j, q**k) for j in range(r)), start=Fraction(1))


def hyperplane_failure_bound(field_order, rank, sample_count):
    q = _natural(field_order, "field order", 2)
    r = _natural(rank, "rank")
    k = _natural(sample_count, "sample count")
    return min(Fraction(1), Fraction((q**r - 1) // (q - 1), q**k))


def terminal_budget(field_order, ambient_dimension, arities, error):
    """Count every fresh source, internal conversion, and final readout.

Arithmetic/SDE/gate costs remain additional obligations. Arity j is the
packet size for grade j+2, in ascending grade order. No subtree is reused.
"""
    q = _natural(field_order, "field order", 2)
    n = _natural(ambient_dimension, "ambient dimension", 1)
    arities = tuple(_natural(a, "packet arity", 1) for a in arities)
    error = Fraction(error)
    if not 0 < error < 1:
        raise ValueError("error must lie strictly between zero and one")
    tail = 0
    while Fraction(1, (q - 1) * q**tail) > error / 3:
        tail += 1
    samples = n + tail
    leaves = 1
    merges_per_sample = 0
    for arity in arities:
        merges_per_sample += leaves
        leaves *= arity
    lifted_leaves = samples * leaves
    merges = samples * merges_per_sample
    instruments = lifted_leaves + merges + samples
    return {
        "field_order": q,
        "field_existence_is_a_premise": True,
        "ambient_dimension": n,
        "annihilator_dimension_is_not_assumed_known": True,
        "packet_arities_ascending_grade": list(arities),
        "class": len(arities) + 1,
        "terminal_samples": samples,
        "fresh_lifted_leaves": lifted_leaves,
        "original_source_copies": (len(arities) + 1) * lifted_leaves,
        "conversion_nodes": merges,
        "final_readout_instruments": samples,
        "complete_instruments": instruments,
        "per_instrument_half_diamond_error": str(error / (3 * instruments)),
        "rank_failure_upper_bound": str(Fraction(1, (q - 1) * q**tail)),
        "supplied_arity_sufficiency_must_be_justified_separately": True,
        "separate_sde_abort_allowance": str(error / 3),
        "total_error_budget": str(error),
        "source_independence_required": True,
        "gate_or_solver_runtime_certified": False,
        "quantum_execution": False,
    }


def _control_domain(prime, dimension):
    p = _natural(prime, "prime", 2)
    n = _natural(dimension, "dimension")
    if p > 31 or any(p % d == 0 for d in range(2, int(p**0.5) + 1)):
        raise ValueError("finite controls require a verified prime <= 31")
    if p**n > 125:
        raise ValueError("finite control allocation cap exceeded")
    return tuple(product(range(p), repeat=n))


def matrix_rank(rows, width, prime):
    """Small exact Gaussian elimination; no hidden subspace is an input."""
    rows = [list(row) for row in rows]
    if any(len(row) != width for row in rows):
        raise ValueError("wrong row width")
    rows = [[x % prime for x in row] for row in rows]
    rank = 0
    for column in range(width):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][column], -1, prime)
        rows[rank] = [x * inv % prime for x in rows[rank]]
        for i in range(rank + 1, len(rows)):
            coefficient = rows[i][column]
            rows[i] = [(x - coefficient * y) % prime for x, y in zip(rows[i], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    return rank


def nullspace_points(rows, prime, dimension):
    domain = _control_domain(prime, dimension)
    if any(len(row) != dimension for row in rows):
        raise ValueError("wrong row width")
    return {v for v in domain if all(sum(x * y for x, y in zip(row, v)) % prime == 0
                                   for row in rows)}


def literal_fourier_diagonal(density, prime, dimension, character_scale=1):
    """Literal U rho U* in Q[zeta_p], without the hidden subgroup.

    Each output is p-1 rational coefficients modulo 1+z+...+z^(p-1).
    A zero character scale is allowed ONLY to expose a nonunitary falsifier.
    """
    domain = _control_domain(prime, dimension)
    size = len(domain)
    if len(density) != size or any(len(row) != size for row in density):
        raise ValueError("density has incorrect dimension")
    result = {}
    for frequency in domain:
        coefficients = [Fraction(0)] * prime
        for i, x in enumerate(domain):
            for j, y in enumerate(domain):
                phase = character_scale * sum(k * (a - b) for k, a, b in zip(frequency, x, y)) % prime
                coefficients[phase] += Fraction(density[i][j], size)
        result[frequency] = tuple(a - coefficients[-1] for a in coefficients[:-1])
    return result


def source_fixture(hidden, prime, dimension):
    """Expected-input fixture only; never used by the operational readout."""
    domain = _control_domain(prime, dimension)
    hidden = set(hidden)
    return tuple(tuple(Fraction(int(tuple((a - b) % prime for a, b in zip(x, y)) in hidden),
                                len(domain)) for y in domain) for x in domain)


def exhaustive_rank_check(prime, rank, samples):
    domain = _control_domain(prime, rank)
    _natural(samples, "sample count")
    total = len(domain)**samples
    if total > 20000:
        raise ValueError("finite rank census cap exceeded")
    full = sum(matrix_rank(rows, rank, prime) == rank for rows in product(domain, repeat=samples))
    measured = Fraction(full, total)
    if measured != spanning_probability(prime, rank, samples):
        raise AssertionError("exact rank count disagrees with the claimed IID formula")
    return {"prime": prime, "rank": rank, "samples": samples,
            "tuples_checked": total, "spanning_probability": str(measured)}


def audit():
    p, n = 3, 2
    domain = _control_domain(p, n)
    zero = {(0, 0)}
    lines = [{(a * x % p, a * y % p) for a in range(p)} for x, y in ((1, 0), (0, 1), (1, 1), (1, 2))]
    source_checks = []
    for hidden in [zero, *lines, set(domain)]:
        result = literal_fourier_diagonal(source_fixture(hidden, p, n), p, n)
        expected_support = nullspace_points(hidden, p, n)
        expected_mass = Fraction(len(hidden), len(domain))
        for frequency, value in result.items():
            expected = expected_mass if frequency in expected_support else Fraction(0)
            if value != (expected, Fraction(0)):
                raise AssertionError("literal terminal readout is incorrect")
        if sum(value[0] for value in result.values()) != 1:
            raise AssertionError("terminal readout is not normalized")
        recovered = nullspace_points(tuple(expected_support), p, n)
        if recovered != hidden:
            raise AssertionError("annihilator did not recover full hidden space")
        source_checks.append({"hidden_size": len(hidden), "support_size": len(expected_support),
                              "probability_per_supported_frequency": str(expected_mass)})
    bad = literal_fourier_diagonal(source_fixture(set(domain), p, n), p, n, character_scale=0)
    bad_total = sum(value[0] for value in bad.values())
    if bad_total != len(domain):
        raise AssertionError("degenerate-character falsifier changed")
    correlated_success = Fraction(sum(matrix_rank([v]*4, 2, p) == 2 for v in domain), len(domain))
    return {
        "exact_density_controls": source_checks,
        "degenerate_character_total_mass": str(bad_total),
        "iid_rank_two_four_sample_success": str(spanning_probability(p, 2, 4)),
        "same_marginal_correlated_four_sample_success": str(correlated_success),
        "finite_rank_censuses": [exhaustive_rank_check(*args) for args in
                                  ((2, 0, 3), (2, 2, 1), (2, 2, 4), (3, 2, 3), (5, 2, 2))],
        "class_three_conservative_budget": terminal_budget(
            7, 5, ((2**8+1)*4**4, (3**27+1)*3**9), Fraction(1, 1000)),
        "large_prime_symbolic_budget": terminal_budget(
            65537, 1000, (1001**2, 1001), Fraction(1, 10**9)),
        "finite_controls_are_not_asymptotic_evidence": True,
        "quantum_execution": False,
        "novelty_or_speedup_claim": False,
    }
