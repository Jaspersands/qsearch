from itertools import product
from math import gcd
import random

import pytest

from central_rank import bank_arity, compressed_witness, row_basis, terminal_envelope, valid_witness


def tiny_scalar(coefficients, degree, prime):
    """Bounded exhaustive TEST oracle; deliberately forbidden at large primes."""
    if prime > 19 or degree > 6:
        raise ValueError("not a scalable scalar backend")
    roots = {}
    for x in range(prime):
        roots.setdefault(pow(x, degree, prime), x)
    for powers in product(roots, repeat=len(coefficients)):
        if any(powers) and sum(a*x for a, x in zip(coefficients, powers)) % prime == 0:
            return tuple(roots[x] for x in powers)
    raise ArithmeticError("no scalar solution in test fixture")


def capped_quadratic(coefficients, degree, prime):
    """Real bounded arithmetic control for p=3 mod4; not the general backend."""
    if degree != 2 or prime % 4 != 3 or len(coefficients) != 3:
        raise ValueError("unsupported quadratic control")
    for j, a in enumerate(coefficients):
        if not a:
            return tuple(int(i == j) for i in range(3))
    a, b, c = coefficients
    rng = random.Random(sum(coefficients) + 701)
    for _ in range(128):
        x = rng.randrange(prime)
        square = -(a*x*x+c) * pow(b, -1, prime) % prime
        y = pow(square, (prime+1)//4, prime)
        if y*y % prime == square:
            return x, y, 1
    raise RuntimeError("explicit scalar-control cap exhausted")


def rank_matrix(ambient, rank, width, prime, seed):
    rng = random.Random(seed)
    generators = [[rng.randrange(prime) for _ in range(width)] for _ in range(rank)]
    if rank:
        for i in range(rank):
            for j in range(rank):
                generators[i][j] = int(i == j)
    rows = list(generators)
    for _ in range(ambient-rank):
        coefficients = [rng.randrange(prime) for _ in range(rank)]
        rows.append([sum(coefficients[i]*generators[i][j] for i in range(rank)) % prime
                     for j in range(width)])
    return rows


@pytest.mark.parametrize("degree,prime,rank", [(1, 5, 2), (2, 7, 3), (3, 7, 2),
                                               (4, 5, 2), (4, 17, 2), (6, 7, 1),
                                               (5, 7, 2), (6, 13, 1)])
def test_composition_on_original_equations(degree, prime, rank):
    reduced = gcd(degree, prime-1)
    width = (reduced+1)**rank + 2
    matrix = rank_matrix(9, rank, width, prime, 32+degree)
    result = compressed_witness(matrix, prime, degree, rank, tiny_scalar)
    assert valid_witness(matrix, result.weights, prime, degree)
    assert result.observed_rank == rank
    assert result.acquired_columns == width
    assert result.used_prefix_columns == bank_arity(reduced, rank)
    assert result.weights[-2:] == (0, 0)
    assert result.scalar_calls == (0 if reduced == 1 else ((reduced+1)**rank-1)//reduced)


def test_127_bit_prime_never_enters_exhaustive_backend():
    prime = 2**127-1
    matrix = rank_matrix(17, 3, 27, prime, 390)
    result = compressed_witness(matrix, prime, 2, 3, capped_quadratic)
    assert result.scalar_calls == 13
    assert valid_witness(matrix, result.weights, prime, 2)


def test_deficient_observed_span_is_safe_but_unused_inputs_stay_paid():
    # The hidden annihilator could be larger. No completeness claim is made.
    matrix = rank_matrix(8, 1, 16, 7, 105)
    result = compressed_witness(matrix, 7, 3, 2, tiny_scalar)
    assert result.observed_rank == 1
    assert result.acquired_columns == 16
    assert result.used_prefix_columns == 4
    assert result.weights[4:] == (0,)*12
    assert valid_witness(matrix, result.weights, 7, 3)


def test_all_zero_labels_need_no_scalar_backend():
    def forbidden(*_):
        raise AssertionError("zero-rank packet must not need a solve")
    result = compressed_witness([[0]*25 for _ in range(6)], 17, 4, 2, forbidden)
    assert result.weights == (1,)+(0,)*24
    assert result.scalar_calls == 0
    assert result.acquired_columns == 25


def test_wrong_rank_promise_aborts_without_solver():
    def forbidden(*_):
        raise AssertionError("invalid promise must fail before backend")
    with pytest.raises(ValueError, match="rank exceeds"):
        compressed_witness([[1, 0, 0], [0, 1, 0]], 7, 2, 1, forbidden)


def test_incomplete_bank_not_refunded_by_empirical_rank():
    with pytest.raises(ValueError, match="preallocated"):
        compressed_witness([[0, 0]], 7, 2, 2, tiny_scalar)


@pytest.mark.parametrize("kind", ["zero", "wrong", "noncanonical", "short"])
def test_bad_scalar_witnesses_are_rejected(kind):
    outputs = {"zero": (0, 0, 0), "wrong": (1, 0, 0),
               "noncanonical": (7, 1, 1), "short": (1, 1)}
    with pytest.raises(ArithmeticError, match="scalar backend"):
        compressed_witness([[1, 1, 1]], 7, 2, 1, lambda *_: outputs[kind])


def test_backend_abort_is_not_converted_to_quantum_success():
    def abort(*_):
        raise RuntimeError("arithmetic cap exhausted")
    with pytest.raises(RuntimeError, match="cap exhausted"):
        compressed_witness([[1, 1, 1]], 7, 2, 1, abort)


def test_zero_power_lift_does_not_turn_unused_registers_on():
    result = compressed_witness([[1, 1, 1, 1, 1, 0]], 5, 4, 1, tiny_scalar)
    assert result.weights[-1] == 0
    assert valid_witness([[1, 1, 1, 1, 1, 0]], result.weights, 5, 4)


def test_row_compression_preserves_entire_kernel():
    matrix = [[1, 2, 0], [2, 4, 0], [1, 0, 1], [2, 2, 1]]
    compressed = row_basis(matrix, 5)
    for vector in product(range(5), repeat=3):
        original_zero = all(sum(a*b for a, b in zip(row, vector)) % 5 == 0 for row in matrix)
        compressed_zero = all(sum(a*b for a, b in zip(row, vector)) % 5 == 0 for row in compressed)
        assert original_zero == compressed_zero


def span(basis, prime, dimension):
    return {tuple(sum(a*v[j] for a, v in zip(coefficients, basis)) % prime
                  for j in range(dimension))
            for coefficients in product(range(prime), repeat=len(basis))}


def test_all_19_heisenberg_subalgebras_satisfy_stronger_rank_bound():
    p, n = 3, 3
    vectors = list(product(range(p), repeat=n))
    subspaces = {(): {(0, 0, 0)}}
    for dimension in range(1, n+1):
        for previous in tuple(subspaces):
            if len(previous) != dimension-1:
                continue
            for vector in vectors:
                canonical = row_basis([*previous, vector], p)
                if len(canonical) == dimension:
                    subspaces[canonical] = span(canonical, p, n)
    subalgebras = 0
    for basis, elements in subspaces.items():
        closed = all((0, 0, (a[0]*b[1]-a[1]*b[0]) % p) in elements
                     for a in basis for b in basis)
        if not closed:
            continue
        subalgebras += 1
        k = n-len(basis)
        intersection_size = sum((0, 0, x) in elements for x in range(p))
        deficit = 0 if intersection_size == p else 1
        assert deficit <= max(0, k-1)
        # Enumerate actual annihilator characters, not an asserted rank.
        labels = [a for a in range(p)
                  if all(a*x % p == 0 for x in range(p) if (0, 0, x) in elements)]
        observed_rank = int(any(labels))
        assert observed_rank == deficit
    assert subalgebras == 19


def test_codimension_does_not_alone_bound_unreduced_number_of_grades():
    # Filiform [X,Y_i]=Y_(i+1). h=<Y_1,...,Y_(c-1)> is abelian of
    # codimension two, but excludes the final central line at every class.
    for c in (3, 8, 12):
        for d in range(2, c+1):
            gamma = set(range(d, c+1))
            hidden = set(range(1, c))
            assert len(gamma-hidden) == 1
    with pytest.raises(ValueError, match="terminal class"):
        terminal_envelope(2, tuple(range(11, 0, -1)), 17)


def test_rank_lemma_requires_subalgebra_closure_and_nilpotence():
    # In Heisenberg, <X,Y> is a codimension-one vector subspace but not a
    # subalgebra: its missing derived coordinate has deficit one, not zero.
    hidden = {(a, b, 0) for a, b in product(range(5), repeat=2)}
    assert (0, 0, 1) not in hidden
    assert 1 > (3-2)-1
    # In sl2(F5), the Borel <E,H> IS a subalgebra of codimension one,
    # while the full derived algebra is sl2. Nilpotence is indispensable.
    e, f, h = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    def bracket(a, b):
        return ((2*a[2]*b[0]-2*a[0]*b[2]) % 5,
                (-2*a[2]*b[1]+2*a[1]*b[2]) % 5,
                (a[0]*b[1]-a[1]*b[0]) % 5)
    assert bracket(h, e) == (2, 0, 0)
    assert len(row_basis([bracket(e, f), bracket(h, e), bracket(h, f)], 5)) == 3


def test_scalar_witness_cannot_be_reused_on_new_labels():
    original = [[1, 1, 1]]
    witness = compressed_witness(original, 7, 2, 1, tiny_scalar).weights
    changed = [original[0].copy()]
    active = next(i for i, x in enumerate(witness) if x)
    changed[0][active] = (changed[0][active]+1) % 7
    assert not valid_witness(changed, witness, 7, 2)


def test_actual_free_class_three_profile():
    # Free class-three rank-two algebra: gamma ranks 3,2; hidden <X,U>.
    # The center packet is missing U; the next packet annihilates U.
    center = [[0]*16, [i % 7 for i in range(16)]]
    grade_two = [[i % 7 for i in range(9)], [0]*9,
                 [(i*i) % 7 for i in range(9)]]
    assert compressed_witness(center, 7, 3, 2, tiny_scalar).observed_rank == 1
    assert compressed_witness(grade_two, 7, 2, 2, tiny_scalar).observed_rank == 2
    budget = terminal_envelope(3, (3, 2), 7, terminal_samples=5)
    assert budget["old_scalar_line_multiplier"] == 432
    assert budget["compressed_multiplier"] == 144
    assert budget["lifted_leaves"] == 720
    assert budget["central_merge_nodes"] == 50
    assert budget["original_queries_or_copies"] == 2160
    assert budget["complete_instruments"] == 775


def test_uniform_parameter_envelope_and_abelian_case():
    for k in range(2, 9):
        c = min(2*k-1, k*(k+1)//2-1)
        # This is an upper-envelope profile, not an assertion of a terminal Lie family.
        ranks = tuple(range(k*(k+1)//2-2, k*(k+1)//2-c-1, -1))
        budget = terminal_envelope(k, ranks, 127)
        assert budget["compressed_multiplier"] <= budget["uniform_parameter_envelope"]
        assert budget["compressed_multiplier"] <= budget["old_scalar_line_multiplier"]
        assert budget["complete_instruments"] <= 2*budget["lifted_leaves"]
        assert not budget["valid_terminal_input_verified"]
    abelian = terminal_envelope(1, (), 3, 7)
    assert abelian["original_queries_or_copies"] == 7
    assert abelian["central_merge_nodes"] == 0


@pytest.mark.parametrize("matrix", [[], [[]], [[1], [1, 2]], [[-1]], [[True]], [[7]]])
def test_reject_bad_equation_inputs(matrix):
    with pytest.raises(ValueError):
        compressed_witness(matrix, 7, 2, 1, tiny_scalar)
