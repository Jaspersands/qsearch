from itertools import combinations, product
import random

import numpy as np
import pytest

from theorems.free_lazard_pullback import (
    OpaqueFreePullback, build_report, free_lazard_domain,
)
from theorems.rees_hsp_reduction import _units
from theorems.rees_nongradable_control import dixmier_lister_algebra
from theorems.symbolic_scalar_phase_erasure import _fmpz_nullspace_basis, _fmpz_solve_coordinates


def _opaque_class_three(algebra):
    """Only this fixture can inspect target coordinates; compiler sees objects."""
    encoded, decoded = {}, {}
    def encode(vector):
        vector = tuple(vector)
        if vector not in encoded:
            token = object()
            encoded[vector], decoded[token] = token, vector
        return encoded[vector]
    def multiply(a, b):
        x, y, p = decoded[a], decoded[b], algebra.p
        xy = algebra.bracket(x, y)
        xxy = algebra.bracket(x, xy)
        yyx = algebra.bracket(y, tuple(-t % p for t in xy))
        return encode(tuple((a+b+pow(2, -1, p)*c+pow(12, -1, p)*(d+e)) % p
                            for a, b, c, d, e in zip(x, y, xy, xxy, yyx)))
    return encode, decoded.__getitem__, multiply


@pytest.mark.parametrize("s,c,dimension", [(1, 4, 1), (2, 2, 3), (2, 3, 5),
                                         (2, 4, 8), (3, 3, 14), (4, 3, 30)])
def test_standard_free_dimensions_and_jacobi(s, c, dimension):
    domain = free_lazard_domain(7, s, c)
    assert domain.dimension == dimension
    assert len(domain.associative_words) == sum(s**j for j in range(1, c+1))
    units = _units(dimension)
    for i, j, k in combinations(range(dimension), 3):
        rows = [domain.algebra.bracket(units[a], domain.algebra.bracket(units[b], units[d]))
                for a, b, d in ((i, j, k), (j, k, i), (k, i, j))]
        assert not any(sum(row[t] for row in rows) % 7 for t in range(dimension))
    for word, unit in zip(domain.bracket_words, units):
        assert domain.word_coordinates(word) == unit


@pytest.mark.parametrize("p", [7, 2**127-1])
def test_opaque_surjection_to_nongradable_target_without_target_chart(p):
    target = dixmier_lister_algebra(p)
    encode, decode, multiply = _opaque_class_three(target)
    domain = free_lazard_domain(p, 4, 3)
    basis = _units(8)
    bridge = OpaqueFreePullback(domain, [encode(v) for v in basis[:4]], encode((0,)*8), multiply)
    images = [decode(v) for v in bridge.basis_images]
    assert len(target.span(images)) == 8
    assert domain.dimension == 30
    rng = random.Random(941)
    for _ in range(3):
        x, y = [tuple(rng.randrange(p) for _ in range(domain.dimension)) for _ in range(2)]
        assert bridge.evaluate(domain.multiply(x, y)) == multiply(bridge.evaluate(x), bridge.evaluate(y))
        before = bridge.words.multiplication_calls
        bridge.evaluate(x)
        assert bridge.words.multiplication_calls-before <= bridge.accounting()["per_map_group_multiplication_cap"]
    calls = []
    bridge.query(lambda x: calls.append(x), (0,)*domain.dimension)
    assert calls == [encode((0,)*8)]
    # A genuine nonhomogeneous kernel relation: [a,d]+[b,[a,c]].
    u, v = domain.word_coordinates((0, 3)), domain.word_coordinates((1, 0, 2))
    relation = tuple((a+b) % p for a, b in zip(u, v))
    assert bridge.evaluate(relation) == bridge.words.identity
    assert bridge.evaluate(domain.dilate(relation, 2)) != bridge.words.identity
    # Ordinary products of basis powers are NOT the logarithmic linear map.
    x = tuple(int(i in (0, 1)) for i in range(domain.dimension))
    assert bridge.evaluate(x) != multiply(bridge.generators[0], bridge.generators[1])


def test_full_preimage_projects_correctly_without_dropping_unknown_kernel():
    p = 7
    target = dixmier_lister_algebra(p)
    encode, decode, multiply = _opaque_class_three(target)
    domain = free_lazard_domain(p, 4, 3)
    units = _units(8)
    bridge = OpaqueFreePullback(domain, [encode(v) for v in units[:4]], encode((0,)*8), multiply)
    images = tuple(decode(v) for v in bridge.basis_images)
    matrix = tuple(zip(*images))
    kernel = _fmpz_nullspace_basis(matrix, domain.dimension, p)
    assert len(kernel) == 22
    hidden = (units[0], units[4], units[7])
    preimage = _fmpz_nullspace_basis([matrix[i] for i in (1, 2, 3, 5, 6)], domain.dimension, p)
    assert len(preimage) == 25
    assert all(_fmpz_solve_coordinates(preimage, v, p) is not None for v in kernel)
    for a, b in product(preimage, repeat=2):
        assert _fmpz_solve_coordinates(preimage, domain.algebra.bracket(a, b), p) is not None
    recovered = [decode(g) for g in bridge.project_recovered_generators(preimage)]
    assert target.span(recovered) == target.span(hidden)
    assert bridge.project_recovered_generators(kernel) == ()
    # Selecting one lift per hidden generator can fail even bracket closure.
    incomplete = tuple(domain.word_coordinates(word) for word in ((0,), (0, 1), (1, 2)))
    assert target.span([decode(bridge.evaluate(v)) for v in incomplete]) == target.span(hidden)
    assert _fmpz_solve_coordinates(incomplete, domain.algebra.bracket(incomplete[0], incomplete[1]), p) is None


def test_redundant_and_identity_target_generators_are_legal():
    p = 7
    domain = free_lazard_domain(p, 3, 3)
    multiply = lambda a, b: (a+b) % p
    bridge = OpaqueFreePullback(domain, (1, 1, 0), 0, multiply)
    x = tuple((i+1) % p for i in range(domain.dimension))
    assert bridge.evaluate(x) == (x[0]+x[1]) % p
    assert bridge.evaluate(domain.word_coordinates((2,))) == 0
    assert bridge.evaluate(domain.word_coordinates((0, 1))) == 0


def test_class_four_map_against_actual_opaque_unitriangular_multiplication():
    p = 7
    identity = tuple(tuple(int(i == j) for j in range(5)) for i in range(5))
    encoded, decoded = {}, {}
    def encode(matrix):
        if matrix not in encoded:
            token = object()
            encoded[matrix], decoded[token] = token, matrix
        return encoded[matrix]
    def multiply(a, b):
        A, B = decoded[a], decoded[b]
        return encode(tuple(tuple(sum(A[i][k]*B[k][j] for k in range(5)) % p
                                  for j in range(5)) for i in range(5)))
    generators = [tuple(tuple(identity[i][j]+int((i, j) in slots) for j in range(5)) for i in range(5))
                  for slots in (((0, 1), (2, 3)), ((1, 2), (3, 4)))]
    domain = free_lazard_domain(p, 2, 4)
    bridge = OpaqueFreePullback(domain, [encode(g) for g in generators], encode(identity), multiply)
    assert any(g != bridge.words.identity for w, g in zip(domain.bracket_words, bridge.basis_images) if len(w) == 4)
    rng = random.Random(421)
    for _ in range(3):
        x, y = [tuple(rng.randrange(p) for _ in range(domain.dimension)) for _ in range(2)]
        assert bridge.evaluate(domain.multiply(x, y)) == multiply(bridge.evaluate(x), bridge.evaluate(y))


def test_exponent_p_promise_cannot_be_replaced_by_arbitrary_p_power_exponent():
    domain = free_lazard_domain(7, 1, 1)
    bridge = OpaqueFreePullback(domain, (1,), 0, lambda a, b: (a+b) % 49)
    # Invalid promised input: this map need not be a homomorphism.
    assert bridge.evaluate(domain.multiply((6,), (1,))) != (bridge.evaluate((6,))+bridge.evaluate((1,))) % 49


def test_one_copy_physical_pullback_with_nontrivial_kernel_and_workspace_falsifier():
    p = 5
    domain = free_lazard_domain(p, 2, 2)
    target = tuple(product(range(p), repeat=2))
    position = {g: i for i, g in enumerate(target)}
    multiply = lambda a, b: tuple((x+y) % p for x, y in zip(a, b))
    bridge = OpaqueFreePullback(domain, ((1, 0), (0, 1)), (0, 0), multiply)
    addresses = tuple(product(range(p), repeat=domain.dimension))
    images = [bridge.evaluate(a) for a in addresses]
    # Purification of rho_H for H=span((1,0)), with a private coset environment.
    source = np.zeros((len(target), p))
    for (x, y), index in position.items():
        source[index, y] = 1/p
    amplitudes = np.zeros((len(addresses), len(target), p))
    for a, shift in enumerate(images):
        permutation = [position[tuple((x-y) % p for x, y in zip(g, shift))] for g in target]
        amplitudes[a, permutation, :] = source/np.sqrt(len(addresses))
    flat = amplitudes.reshape(len(addresses), -1)
    actual = flat @ flat.T
    expected = np.array([[float(a[1] == b[1])/len(addresses) for b in images] for a in images])
    assert np.allclose(actual, expected, atol=1e-14)
    assert np.isclose(np.trace(actual), 1)
    assert np.linalg.matrix_rank(actual, tol=1e-10) == p
    leaked = actual*np.array([[a == b for b in images] for a in images])
    assert not np.allclose(leaked, actual)
    assert np.linalg.matrix_rank(leaked, tol=1e-10) == p*p


def test_backend_boundary_and_scope_flags():
    domain = free_lazard_domain(3, 2, 2)
    bridge = OpaqueFreePullback(domain, (1, 1), 0, lambda a, b: (a+b) % 3)
    assert bridge.evaluate(domain.word_coordinates((0,))) == 1
    assert bridge.evaluate(domain.word_coordinates((0, 1))) == 0
    report = build_report()
    assert report["general_inverse_bch_backend_implemented"] is True
    for flag in ("target_chart_acquisition_required_by_this_bridge", "unknown_target_kernel_required",
                 "quantum_receiver_implemented",
                 "independent_review", "novelty_established", "speedup_claim_allowed"):
        assert report[flag] is False
