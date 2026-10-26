"""Opaque-encoding controls for public group words, not quantum basis learning."""
from fractions import Fraction
import random

from flint import nmod_mat
import numpy as np
import pytest

from theorems.class_four_group_words import ClassFourGroupWords
from tests.test_metabelian_phase_extension import finite_matrix_exp_log


class OpaqueUT5:
    """Test-only private multiplication provider; the controller receives tokens."""
    def __init__(self, p):
        self.p = p
        self.values = {}
        self.tokens = {}
        self.identity = self.encode(np.eye(5, dtype=object))

    def encode(self, value):
        key = tuple(int(x) % self.p for x in value.flat)
        if key not in self.tokens:
            token = object()
            self.tokens[key] = token
            self.values[token] = np.array(key, dtype=object).reshape(5, 5)
        return self.tokens[key]

    def multiply(self, a, b):
        return self.encode(self.values[a] @ self.values[b] % self.p)

    def from_log(self, value):
        return self.encode(finite_matrix_exp_log(value, self.p))

    def log(self, token):
        return finite_matrix_exp_log(self.values[token], self.p, logarithm=True)


def random_log(rng, p):
    value = np.zeros((5, 5), dtype=object)
    for i in range(5):
        for j in range(i+1, 5):
            value[i, j] = rng.randrange(p)
    return value


@pytest.mark.parametrize("p", [5, 7, 11, 2**127-1])
def test_corrected_words_on_opaque_encodings_and_logarithmic_query_caps(p):
    provider = OpaqueUT5(p)
    words = ClassFourGroupWords(p, provider.identity, provider.multiply)
    rng = random.Random(20771)
    for _ in range(5):
        x, y = random_log(rng, p), random_log(rng, p)
        a, b = provider.from_log(x), provider.from_log(y)
        for operation, expected in (
            ("lie_add", (x+y) % p), ("lie_bracket", (x@y-y@x) % p)
        ):
            before = words.multiplication_calls
            result = getattr(words, operation)(a, b)
            assert words.multiplication_calls-before <= words.operation_caps()[operation]
            assert np.array_equal(provider.log(result), expected)
        before = words.multiplication_calls
        result = words.linear_combination((a, b), (p-1, 2))
        assert np.array_equal(provider.log(result), (-x+2*y) % p)
        assert words.multiplication_calls-before <= 2*words.operation_caps()["linear_combination_per_term"]


def test_group_generators_are_not_an_additive_basis_but_bracket_closure_spans():
    provider = OpaqueUT5(7)
    words = ClassFourGroupWords(7, provider.identity, provider.multiply)
    generators = []
    for i in range(4):
        matrix = np.zeros((5, 5), dtype=object)
        matrix[i, i+1] = 1
        generators.append(provider.from_log(matrix))
    slots = [(i, j) for i in range(5) for j in range(i+1, 5)]
    def rows(elements):
        return [[int(provider.log(g)[i, j]) for i, j in slots] for g in elements]
    assert nmod_mat(rows(generators), 7).rank() == 4
    before = words.multiplication_calls
    family = words.lie_spanning_family(generators)
    assert len(family) <= sum(4**k for k in range(1, 5))
    assert words.multiplication_calls-before <= sum(4**k for k in range(2, 5))*words.operation_caps()["lie_bracket"]
    assert nmod_mat(rows(family), 7).rank() == 10
    assert len(family) > 10  # Deliberately not mislabeled as an acquired basis.


def test_additive_encoding_is_a_homomorphism_even_for_dependent_generators():
    p, rng = 7, random.Random(888)
    provider = OpaqueUT5(p)
    words = ClassFourGroupWords(p, provider.identity, provider.multiply)
    first = provider.from_log(random_log(rng, p))
    second = provider.from_log(random_log(rng, p))
    elements = (first, second, words.lie_add(first, second))
    assert words.linear_combination(elements, (1, 1, p-1)) == provider.identity
    for _ in range(4):
        a, b = [tuple(rng.randrange(p) for _ in elements) for _ in range(2)]
        added = tuple((x+y) % p for x, y in zip(a, b))
        assert words.linear_combination(elements, added) == words.lie_add(
            words.linear_combination(elements, a), words.linear_combination(elements, b))
    assert words.lie_add(first, second) != words.multiply(first, second)


@pytest.mark.parametrize("p", [2, 3, 9])
def test_invalid_characteristic_is_rejected(p):
    with pytest.raises(ValueError):
        ClassFourGroupWords(p, None, lambda a, b: a)


def test_empty_and_malformed_public_word_inputs():
    provider = OpaqueUT5(5)
    words = ClassFourGroupWords(5, provider.identity, provider.multiply)
    assert words.lie_spanning_family(()) == ()
    assert words.linear_combination((), ()) == provider.identity
    for coefficients in ((True,), (5,), (-1,), ()):
        with pytest.raises(ValueError):
            words.linear_combination((provider.identity,), coefficients)
    with pytest.raises(ValueError):
        words.power(provider.identity, Fraction(1, 2))


@pytest.mark.parametrize("p,power,extra", [(5, 2, 0), (7, 3, 0), (5, 2, 3),
                                         (2**127-1, 2, 0)])
def test_prime_power_words_use_ring_denominators_and_allow_loose_annihilator(p, power, extra):
    modulus = p**power
    provider = OpaqueUT5(modulus)
    words = ClassFourGroupWords(p, provider.identity, provider.multiply,
                               exponent_bound=p**(power+extra))
    rng = random.Random(557)
    x, y = random_log(rng, modulus), random_log(rng, modulus)
    a, b = provider.from_log(x), provider.from_log(y)
    for name, expected in (("lie_add", (x+y) % modulus),
                           ("lie_bracket", (x@y-y@x) % modulus)):
        before = words.multiplication_calls
        result = getattr(words, name)(a, b)
        assert np.array_equal(provider.log(result), expected)
        assert words.multiplication_calls-before <= words.operation_caps()[name]
    assert words.multiply(a, words.power(a, -1)) == provider.identity
    assert np.array_equal(provider.log(words.linear_combination(
        (a, b), (p+1, words.exponent_bound-1))), ((p+1)*x-y) % modulus)


def test_mod_p_inverse_is_wrong_when_group_exponent_is_p_squared():
    p = 5
    add = lambda a, b: (a+b) % (p*p)
    wrong = ClassFourGroupWords(p, 0, add)
    correct = ClassFourGroupWords(p, 0, add, exponent_bound=p*p)
    assert wrong.multiply(1, wrong.power(1, -1)) != 0
    assert correct.multiply(1, correct.power(1, -1)) == 0
    assert add(wrong._rational_power(1, 1, 2), wrong._rational_power(1, 1, 2)) != 1
    assert add(correct._rational_power(1, 1, 2), correct._rational_power(1, 1, 2)) == 1


@pytest.mark.parametrize("annihilator_power", [2, 4])
def test_torsion_from_mixed_cyclic_factors_does_not_use_one_common_power(annihilator_power):
    p = 5
    add = lambda a, b: ((a[0]+b[0]) % (p*p), (a[1]+b[1]) % p)
    words = ClassFourGroupWords(p, (0, 0), add, exponent_bound=p**annihilator_power)
    before = words.multiplication_calls
    basis = words.p_torsion_from_decomposition(((1, 0), (0, 1)), (p*p, p))
    assert basis == ((p, 0), (0, 1))
    assert words.multiplication_calls-before <= 2*words.operation_caps()["p_torsion_per_factor"]
    assert words.power((0, 1), words.exponent_bound//p) == (0, 0)
    # Even irredundancy and correct orders do NOT imply additive independence.
    dependent = words.p_torsion_from_decomposition(((1, 0), (1, 1)), (p*p, p*p))
    assert dependent == ((p, 0), (p, 0))


def test_torsion_can_remain_nonabelian_inside_a_higher_exponent_class_four_group():
    p = 7
    provider = OpaqueUT5(p)
    identity = (provider.identity, 0)
    multiply = lambda a, b: (provider.multiply(a[0], b[0]), (a[1]+b[1]) % (p*p))
    words = ClassFourGroupWords(p, identity, multiply, exponent_bound=p*p)
    additive_basis = []
    for i in range(5):
        for j in range(i+1, 5):
            matrix = np.zeros((5, 5), dtype=object)
            matrix[i, j] = 1
            additive_basis.append((provider.from_log(matrix), 0))
    additive_basis.append((provider.identity, 1))
    torsion = words.p_torsion_from_decomposition(additive_basis, (p,)*10+(p*p,))
    assert torsion[:-1] == tuple(additive_basis[:-1])
    assert torsion[-1] == (provider.identity, p)
    # E12 and E23, the fifth entry in lexicographic slot order.
    assert words.commutator(torsion[0], torsion[4]) != identity
    assert all(words.power(g, p) == identity for g in torsion)


@pytest.mark.parametrize("bound", [0, 1, 6, 10, 35, True, 25.0])
def test_invalid_prime_power_annihilator_rejected(bound):
    with pytest.raises(ValueError):
        ClassFourGroupWords(5, 0, lambda a, b: a, exponent_bound=bound)


def test_false_decomposition_orders_are_rejected_without_modular_shortcut():
    words = ClassFourGroupWords(5, 0, lambda a, b: (a+b) % 25, exponent_bound=25)
    for generators, orders in [((1,), (5,)), ((5,), (25,)), ((1,), (1,)),
                               ((1,), (0,)), ((1,), (True,)), ((1,), (10,)),
                               ((1,), ())]:
        with pytest.raises(ValueError):
            words.p_torsion_from_decomposition(generators, orders)
    assert words.p_torsion_from_decomposition((0, 1), (1, 25)) == (5,)
    assert words.p_torsion_from_decomposition((), ()) == ()


def test_mixed_order_normalizer_is_a_congruence_not_naive_field_linearization():
    p, modulus = 5, 25
    provider = OpaqueUT5(modulus)
    words = ClassFourGroupWords(p, provider.identity, provider.multiply,
                               exponent_bound=modulus)
    jordan = np.zeros((5, 5), dtype=object)
    for i in range(4):
        jordan[i, i+1] = 1
    k = np.zeros((5, 5), dtype=object)
    k[0, 1] = p
    subgroup = {provider.from_log(j*k) for j in range(p)}
    assert np.count_nonzero(k % p) == 0  # Field reduction erases a real subgroup.
    assert len(subgroup) == p
    for a in range(modulus):
        x = a*jordan
        g = provider.from_log(x)
        inverse = words.power(g, -1)
        conjugated = {words.multiply(words.multiply(g, h), inverse) for h in subgroup}
        bracket = (x@k-k@x) % modulus
        stabilizes_lie_subgroup = any(np.array_equal(bracket, j*k) for j in range(p))
        assert (conjugated == subgroup) == stabilizes_lie_subgroup == (a % p == 0)
