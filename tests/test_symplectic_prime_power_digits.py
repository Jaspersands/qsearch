"""Exact ring-action controls; no quantum digit learner or hard oracle fixture."""
from itertools import combinations_with_replacement, product
import random

from flint import fmpz_mod_ctx, fmpz_mod_mat, nmod_poly
import pytest

from theorems.symplectic_prime_power_digits import (
    final_digit_query, final_verification_pairs, lift_symplectic_matrix,
    recover_scalar_digit, scalar_digit_query, scalar_verification_pair, socle_shift,
)
from theorems.symplectic_socle_probes import (
    add, eye, graph_polynomial, multiply, recover_symmetric_matrix,
    scale, symplectic_form, transpose,
)


def symmetric(n, entries):
    result = [[0]*n for _ in range(n)]
    for (i, j), x in zip(combinations_with_replacement(range(n), 2), entries):
        result[i][j] = result[j][i] = x
    return tuple(map(tuple, result))


def flatten(a):
    return tuple(a[i][j] for i, j in combinations_with_replacement(range(len(a)), 2))


def graph_image(g, s, modulus):
    """Actual matrix image of [I;S], normalized by independent FLINT inversion."""
    n = len(s)
    image = multiply(g, eye(n)+s, modulus)
    inverse = fmpz_mod_mat(image[:n], fmpz_mod_ctx(modulus)).inv()
    inverse = tuple(tuple(int(inverse[i, j]) for j in range(n)) for i in range(n))
    return multiply(image[n:], inverse, modulus)


def assert_symplectic(g, modulus):
    j = symplectic_form(len(g)//2)
    assert multiply(multiply(transpose(g), j, modulus), g, modulus) == scale(j, 1, modulus)


@pytest.mark.parametrize("p,length,n", [(3, 3, 2), (3, 7, 3), (5, 4, 3),
                                      (11, 5, 2), (2**127-1, 4, 3)])
def test_each_digit_action_including_growing_depth_and_large_prime(p, length, n):
    rng, modulus = random.Random(123), p**length
    s = symmetric(n, [p*rng.randrange(p**(length-1)) for _ in range(n*(n+1)//2)])
    for digit in range(1, length):
        prefix = scale(s, 1, p**digit)
        hidden_digit = tuple(tuple((x//p**digit) % p for x in row) for row in s)
        for t in (0, 1, p-1):
            x = symmetric(n, [rng.randrange(p) for _ in range(n*(n+1)//2)])
            if digit < length-1:
                g = scalar_digit_query(prefix, x, t, digit, p, length)
                polynomial = scale(hidden_digit, -2*t, p)
            else:
                g = final_digit_query(prefix, x, t, 0, 1, p, length)
                b, c = graph_polynomial(hidden_digit, 0, 1, p)
                polynomial = add(scale(b, t, p), scale(c, t*t, p), p)
            expected = add(s, scale(add(x, polynomial, p), p**(length-1), modulus), modulus)
            assert_symplectic(g, modulus)
            assert graph_image(g, s, modulus) == expected


@pytest.mark.parametrize("p,length,digit", [(3, 4, 1), (3, 4, 2), (5, 4, 2), (3, 3, 2)])
def test_all_small_fibers_are_complete_and_have_one_prime_scalar_each(p, length, digit):
    modulus = p**length
    s = symmetric(2, [p*(p+1), p*(p-1), p*(p*p+2)])
    s = scale(s, 1, modulus)
    prefix = scale(s, 1, p**digit)
    hidden = tuple(tuple((x//p**digit) % p for x in row) for row in s)
    b, c = graph_polynomial(hidden, 0, 1, p)
    fibers = {}
    for entries in product(range(p), repeat=3):
        x = symmetric(2, entries)
        for t in range(p):
            if digit < length-1:
                g = scalar_digit_query(prefix, x, t, digit, p, length)
                polynomial = scale(hidden, -2*t, p)
            else:
                g = final_digit_query(prefix, x, t, 0, 1, p, length)
                polynomial = add(scale(b, t, p), scale(c, t*t, p), p)
            actual = graph_image(g, s, modulus)
            fibers.setdefault(actual, []).append((t, add(x, polynomial, p)))
    assert len(fibers) == p**3
    for fiber in fibers.values():
        assert len(fiber) == p
        assert {t for t, _ in fiber} == set(range(p))
        assert len({offset for _, offset in fiber}) == 1


@pytest.mark.parametrize("p,length", [(3, 2), (3, 5), (5, 7), (2**127-1, 4)])
def test_postprocessing_correct_supplied_answers_reconstructs_all_digits(p, length):
    n, rng, modulus = 3, random.Random(879), p**length
    secret = symmetric(n, [p*rng.randrange(p**(length-1)) for _ in range(6)])
    prefix = scale(secret, 1, p)
    for digit in range(1, length):
        truth = tuple(tuple((x//p**digit) % p for x in row) for row in secret)
        if digit < length-1:
            t = p-1
            vector = (t,) + flatten(scale(truth, 2*t, p))
            answer = recover_scalar_digit(vector, n, p)
            pair = scalar_verification_pair(prefix, answer, digit, p, length)
            assert graph_image(pair[0], secret, modulus) == graph_image(pair[1], secret, modulus)
            wrong = add(answer, eye(n), p)
            pair = scalar_verification_pair(prefix, wrong, digit, p, length)
            assert graph_image(pair[0], secret, modulus) != graph_image(pair[1], secret, modulus)
        else:
            coefficients = [graph_polynomial(truth, i, (i+1) % n, p) for i in range(n)]
            answer = recover_symmetric_matrix([b for b, c in coefficients], p)
            for i, (b, c) in enumerate(coefficients):
                pairs = final_verification_pairs(prefix, b, c, i, (i+1) % n, p, length)
                assert all(graph_image(a, secret, modulus) == graph_image(b, secret, modulus)
                           for a, b in pairs)
        assert answer == truth
        prefix = add(prefix, scale(answer, p**digit, modulus), modulus)
    assert prefix == secret


def test_nonzero_prefix_correction_and_precision_are_essential():
    p, length, digit = 5, 4, 2
    modulus = p**length
    s = symmetric(2, (5+25*2+125*3, 10+25*3, 15+25))
    prefix, zero = scale(s, 1, p**digit), scale(eye(2), 0, p)
    correct = scalar_digit_query(prefix, zero, 1, digit, p, length)
    wrong = scalar_digit_query(zero, zero, 1, digit, p, length)
    assert graph_image(correct, s, modulus) != graph_image(wrong, s, modulus)
    # A corrupted earlier digit cannot be repaired by guessing the next one.
    corrupted = add(prefix, scale(eye(2), p, p**digit), p**digit)
    truth = tuple(tuple((x//p**digit) % p for x in row) for row in s)
    pair = scalar_verification_pair(corrupted, truth, digit, p, length)
    assert graph_image(pair[0], s, modulus) != graph_image(pair[1], s, modulus)


def test_final_prefix_carries_and_two_point_certificate():
    p, length = 5, 3
    modulus = p**length
    s = symmetric(2, (5+25*2, 20+25*3, 15+25))
    prefix, zero = scale(s, 1, p**(length-1)), scale(eye(2), 0, p)
    truth = tuple(tuple(x//p**(length-1) for x in row) for row in s)
    correct = final_digit_query(prefix, zero, p-1, 0, 1, p, length)
    wrong = final_digit_query(zero, zero, p-1, 0, 1, p, length)
    assert graph_image(correct, s, modulus) != graph_image(wrong, s, modulus)
    b, c = graph_polynomial(truth, 0, 1, p)
    pairs = final_verification_pairs(prefix, add(b, eye(2), p),
                                    add(c, scale(eye(2), -1, p), p), 0, 1, p, length)
    assert graph_image(pairs[0][0], s, modulus) == graph_image(pairs[0][1], s, modulus)
    assert graph_image(pairs[1][0], s, modulus) != graph_image(pairs[1][1], s, modulus)


def test_scalar_query_map_is_not_asserted_to_be_a_group_homomorphism():
    p, length, digit = 5, 4, 2
    s = symmetric(2, (5+25, 10+25*2, 15+125))
    prefix, zero = scale(s, 1, p**digit), scale(eye(2), 0, p)
    g4 = scalar_digit_query(prefix, zero, 4, digit, p, length)
    product_g = multiply(g4, g4, p**length)
    g3 = scalar_digit_query(prefix, zero, 3, digit, p, length)
    assert product_g != g3
    assert graph_image(product_g, s, p**length) == graph_image(g3, s, p**length)


@pytest.mark.parametrize("p,length", [(3, 2), (5, 4), (2**127-1, 5)])
def test_public_symplectic_hensel_lift(p, length):
    rng, n, modulus = random.Random(97), 3, p**length
    x = symmetric(n, [rng.randrange(p) for _ in range(6)])
    residue = final_digit_query(scale(x, 0, p), x, p-1, 0, 1, p, 2)
    perturbed = tuple(tuple((v+p*rng.randrange(p**(length-1))) % modulus for v in row)
                      for row in residue)
    lifted = lift_symplectic_matrix(perturbed, p, length)
    assert scale(lifted, 1, p) == scale(residue, 1, p)
    assert_symplectic(lifted, modulus)
    assert lifted == lift_symplectic_matrix(lifted, p, length)


@pytest.mark.parametrize("length", [2, 3, 4, 7])
def test_field_unipotent_only_certificate_is_unsound_over_rings(length):
    p, n = 5, 2
    modulus = p**length
    s = scale(((1, 0), (0, 0)), p**((length+1)//2), modulus)
    assert any(v for row in s for v in row)
    for entries in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
        b = symmetric(n, entries)
        upper = tuple(tuple(int(i == j) + (b[i][j-n] if i < n and j >= n else 0)
                            for j in range(2*n)) for i in range(2*n))
        assert graph_image(upper, s, modulus) == s
    # Passing the candidate L0's entire upper-unipotent test does not mean W=L0.
    assert s != scale(s, 0, modulus)


@pytest.mark.parametrize("length", [2, 3, 5])
def test_field_transvection_membership_equivalence_also_fails_over_rings(length):
    p, modulus = 5, 5**length
    v = (1, 0, p**((length+1)//2), 0)
    j = symplectic_form(2)
    jv = tuple(sum(row[k]*v[k] for k in range(4)) % modulus for row in j)
    g = tuple(tuple((int(i == k) + v[i]*jv[k]) % modulus for k in range(4))
              for i in range(4))
    assert_symplectic(g, modulus)
    assert graph_image(g, ((0, 0), (0, 0)), modulus) == ((0, 0), (0, 0))
    assert v[2] != 0  # Primitive v is not in the fixed top Lagrangian.


@pytest.mark.parametrize("p", [3, 5])
def test_deepest_digit_full_query_fixed_point_bound_and_common_subgroup(p):
    secrets = tuple(symmetric(2, values) for values in product(range(p), repeat=3))
    largest_nonuniversal_fiber = 0
    checked = 0
    for entries in product(range(p), repeat=4):
        a = (entries[:2], entries[2:])
        if (a[0][0]*a[1][1]-a[0][1]*a[1][0]) % p == 0:
            continue
        inv = fmpz_mod_mat(a, fmpz_mod_ctx(p)).inv()
        inv = tuple(tuple(int(inv[i, j]) for j in range(2)) for i in range(2))
        fibers = {}
        for s in secrets:
            change = add(multiply(multiply(transpose(inv), s, p), inv, p),
                         scale(s, -1, p), p)
            fibers[change] = fibers.get(change, 0)+1
        universal = a in (eye(2), scale(eye(2), -1, p))
        assert (len(fibers) == 1) == universal
        if not universal:
            largest_nonuniversal_fiber = max(largest_nonuniversal_fiber, max(fibers.values()))
            assert max(fibers.values()) <= p**2
        # Actual ring matrices check the affine fixed-point equation separately.
        if checked < 12:
            modulus = p**3
            inv_ring = fmpz_mod_mat(a, fmpz_mod_ctx(modulus)).inv()
            inv_ring = tuple(tuple(int(inv_ring[i, j]) for j in range(2)) for i in range(2))
            diagonal = tuple(tuple(a[r][c] if r < 2 and c < 2 else
                                   transpose(inv_ring)[r-2][c-2] if r >= 2 and c >= 2 else 0
                                   for c in range(4)) for r in range(4))
            y = symmetric(2, (1, 0, 1))
            g = multiply(socle_shift(y, p, 3), diagonal, modulus)
            for s in secrets:
                expected = add(y, add(multiply(multiply(transpose(inv), s, p), inv, p),
                                      scale(s, -1, p), p), p) == ((0, 0), (0, 0))
                actual_s = scale(s, p*p, modulus)
                assert (graph_image(g, actual_s, modulus) == actual_s) == expected
            checked += 1
    assert largest_nonuniversal_fiber == p**2  # The 1/q bound is attained at rank two.


@pytest.mark.parametrize("p,length", [(3, 3), (5, 5)])
def test_written_chain_ring_identity_in_equal_characteristic_with_nonhomomorphic_lifts(p, length):
    # This tests the written extension, not an unimplemented generic-ring backend.
    z = nmod_poly([0, 1], p)
    modulus = z**length
    constant = lambda x: nmod_poly([x % p], p)
    ident = tuple(tuple(constant(x) for x in row) for row in eye(2))
    zero = constant(0)
    secret = symmetric(2, [sum((j+v)*z**j for j in range(1, length)) % modulus
                           for v in (1, 2, 3)])
    e = ((zero, constant(1)), (zero, zero))
    jform = tuple(tuple(constant(x) for x in row) for row in symplectic_form(2))
    for digit in range(1, length):
        prefix = tuple(tuple(x % z**digit for x in row) for row in secret)
        hidden = tuple(tuple(constant(int(x[digit])) for x in row) for row in secret)
        for t in range(p):
            lifted_t = constant(t) + z*constant(t*t+1)
            if digit < length-1:
                h = z**(length-1-digit)*lifted_t
                unit = (1+h) % modulus
                inverse_unit = sum((-h)**i for i in range(length)) % modulus
                a = scale(ident, unit, modulus)
                inverse = scale(ident, inverse_unit, modulus)
                polynomial = scale(hidden, -2*t, modulus)
            else:
                a = add(ident, scale(e, lifted_t, modulus), modulus)
                inverse = add(ident, scale(e, -lifted_t, modulus), modulus)
                b = scale(add(multiply(transpose(e), hidden, modulus),
                              multiply(hidden, e, modulus), modulus), -1, modulus)
                c = multiply(multiply(transpose(e), hidden, modulus), e, modulus)
                polynomial = add(scale(b, t, modulus), scale(c, t*t, modulus), modulus)
            correction = add(multiply(multiply(transpose(inverse), prefix, modulus),
                                      inverse, modulus), scale(prefix, -1, modulus), modulus)
            translation = scale(correction, -1, modulus)
            diagonal = tuple(tuple(a[r][c] if r < 2 and c < 2 else
                                   transpose(inverse)[r-2][c-2] if r >= 2 and c >= 2 else zero
                                   for c in range(4)) for r in range(4))
            lower = tuple(tuple(constant(int(r == c)) +
                                (translation[r-2][c] if r >= 2 and c < 2 else zero)
                                for c in range(4)) for r in range(4))
            g = multiply(lower, diagonal, modulus)
            assert multiply(multiply(transpose(g), jform, modulus), g, modulus) == jform
            expected = add(secret, scale(polynomial, z**(length-1), modulus), modulus)
            assert multiply(g, ident+secret, modulus) == multiply(ident+expected, a, modulus)


@pytest.mark.parametrize("p,length", [(2, 3), (4, 2), (5, 1), (5, True)])
def test_invalid_scope(p, length):
    with pytest.raises(ValueError):
        socle_shift(((0, 0), (0, 0)), p, length)


@pytest.mark.parametrize("digit", [0, 3, True, -1])
def test_final_digit_is_not_a_scalar_near_identity_digit(digit):
    with pytest.raises(ValueError):
        scalar_digit_query(((0, 0), (0, 0)), ((0, 0), (0, 0)), 0, digit, 5, 4)


def test_malformed_public_inputs_and_kernel_records():
    zero = ((0, 0), (0, 0))
    for prefix in [((0,),), ((0, 1), (0, 0)), ((25, 0), (0, 0))]:
        with pytest.raises(ValueError):
            scalar_digit_query(prefix, zero, 1, 2, 5, 4)
    for vector in [(), (0, 1, 2, 3), (1, 2, 3), (1, 2, 3, 5)]:
        with pytest.raises(ValueError):
            recover_scalar_digit(vector, 2, 5)
    with pytest.raises(ValueError):
        final_digit_query(zero, zero, 5, 0, 1, 5, 3)
    with pytest.raises(ValueError):
        lift_symplectic_matrix(scale(eye(4), 0, 25), 5, 2)
