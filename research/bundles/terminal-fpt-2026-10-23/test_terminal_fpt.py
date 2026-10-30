from dataclasses import replace
from fractions import Fraction
from itertools import product
import random

import pytest

from modular_lazard import Tensor, compile_word, instruction_cap
from terminal_reduction import FiniteGroup, finite_omega_recovery, terminal_plan


def cyclic(order):
    return FiniteGroup(tuple(range(order)), 0, lambda x, y: (x+y) % order,
                       lambda x: -x % order)


def heisenberg_times_c9():
    def mul(x, y):
        a, b, c, z = x
        A, B, C, Z = y
        return ((a+A) % 3, (b+B) % 3, (c+C+a*B) % 3, (z+Z) % 9)

    def inv(x):
        a, b, c, z = x
        return (-a % 3, -b % 3, (-c+a*b) % 3, -z % 9)

    return FiniteGroup(tuple(product(range(3), range(3), range(3), range(9))),
                       (0, 0, 0, 0), mul, inv)


def coset_oracle(group, H):
    labels = {x: frozenset(group.multiply(x, h) for h in H) for x in group.elements}
    assert len(set(labels.values()))*len(H) == len(group.elements)
    tokens = {label: object() for label in set(labels.values())}
    return lambda x: tokens[labels[x]]


class Matrices:
    """Independent matrix multiplication/exp; opaque word evaluation sees tokens."""
    def __init__(self, size, prime):
        self.n, self.p = size, prime
        self.zero = tuple((0,)*size for _ in range(size))
        self.one = tuple(tuple(int(i == j) for j in range(size)) for i in range(size))
        self.encode_map, self.decode_map = {}, {}

    def encode(self, value):
        if value not in self.encode_map:
            token = object()
            self.encode_map[value], self.decode_map[token] = token, value
        return self.encode_map[value]

    def add(self, a, b, scalar=1):
        return tuple(tuple((x+scalar*y) % self.p for x, y in zip(u, v)) for u, v in zip(a, b))

    def mul(self, a, b):
        return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(self.n)) % self.p
                           for j in range(self.n)) for i in range(self.n))

    def exp(self, a):
        out = term = self.one
        for j in range(1, self.n):
            term = self.add(self.zero, self.mul(term, a), pow(j, -1, self.p))
            out = self.add(out, term)
        return out

    def opaque_multiply(self, x, y):
        return self.encode(self.mul(self.decode_map[x], self.decode_map[y]))

    def random_lie(self, seed):
        rng = random.Random(seed)
        return tuple(tuple(rng.randrange(self.p) if i < j else 0 for j in range(self.n))
                     for i in range(self.n))


@pytest.mark.parametrize("degree,prime", [(1, 2), (2, 3), (3, 5), (4, 5),
                                          (5, 7), (6, 7), (7, 11), (8, 11)])
@pytest.mark.parametrize("operation", ["add", "bracket"])
def test_modular_certificates_complete_coefficients(degree, prime, operation):
    cert = compile_word(prime, degree, operation)
    cert.verify()
    assert len(cert.instructions) <= instruction_cap(degree)
    assert all(0 <= step[2] < prime for step in cert.instructions if step[0] == "pow")


@pytest.mark.parametrize("degree,prime", [(1, 2), (2, 3), (3, 5), (4, 5),
                                          (5, 7), (6, 7), (5, 2**127-1)])
def test_opaque_group_word_against_independent_matrix_exp(degree, prime):
    fixture = Matrices(degree+1, prime)
    X, Y = fixture.random_lie(105), fixture.random_lie(506)
    x, y, identity = [fixture.encode(a) for a in (fixture.exp(X), fixture.exp(Y), fixture.one)]
    expected = {"add": fixture.exp(fixture.add(X, Y)),
                "bracket": fixture.exp(fixture.add(fixture.mul(X, Y), fixture.mul(Y, X), -1))}
    for operation in expected:
        cert = compile_word(prime, degree, operation)
        result, calls = cert.evaluate(x, y, identity, fixture.opaque_multiply)
        assert fixture.decode_map[result] == expected[operation]
        assert calls <= cert.multiplication_cap()


def test_tampered_certificate_and_wrong_class_fail():
    cert = compile_word(7, 3, "add")
    with pytest.raises(ValueError):
        replace(cert, output=0).verify()
    with pytest.raises(ValueError):
        replace(cert, stages=cert.stages[:-1]).verify()
    instructions = list(cert.instructions)
    j = next(i for i, step in enumerate(instructions) if step[0] == "pow")
    op, source, exponent = instructions[j]
    instructions[j] = (op, source, (exponent+1) % 7)
    with pytest.raises(ValueError):
        replace(cert, instructions=tuple(instructions)).verify()
    fixture = Matrices(6, 7)
    X, Y = fixture.random_lie(105), fixture.random_lie(506)
    result, _ = compile_word(7, 4, "add").evaluate(
        fixture.encode(fixture.exp(X)), fixture.encode(fixture.exp(Y)),
        fixture.encode(fixture.one), fixture.opaque_multiply)
    assert fixture.decode_map[result] != fixture.exp(fixture.add(X, Y))


@pytest.mark.parametrize("prime,exponent,degree", [(3, 2, 2), (5, 3, 4), (7, 2, 5),
                                                  (2**127-1, 2, 3)])
def test_higher_exponent_words_use_full_prime_power_modulus(prime, exponent, degree):
    fixture = Matrices(degree+1, prime**exponent)
    X, Y = fixture.random_lie(105), fixture.random_lie(506)
    x, y, identity = [fixture.encode(a) for a in (fixture.exp(X), fixture.exp(Y), fixture.one)]
    expected = {"add": fixture.exp(fixture.add(X, Y)),
                "bracket": fixture.exp(fixture.add(fixture.mul(X, Y), fixture.mul(Y, X), -1))}
    for operation in expected:
        certificate = compile_word(prime, degree, operation, exponent)
        certificate.verify()
        actual, calls = certificate.evaluate(x, y, identity, fixture.opaque_multiply)
        assert fixture.decode_map[actual] == expected[operation]
        assert calls <= certificate.multiplication_cap()


def test_reducing_exponents_mod_p_is_wrong_for_exponent_p_squared():
    fixture = Matrices(3, 9)
    X = ((0, 1, 0), (0, 0, 0), (0, 0, 0))
    Y = ((0, 0, 0), (0, 0, 1), (0, 0, 0))
    x, y, identity = [fixture.encode(a) for a in (fixture.exp(X), fixture.exp(Y), fixture.one)]
    wrong, _ = compile_word(3, 2, "add").evaluate(x, y, identity, fixture.opaque_multiply)
    right, _ = compile_word(3, 2, "add", 2).evaluate(x, y, identity, fixture.opaque_multiply)
    assert fixture.decode_map[wrong] != fixture.exp(fixture.add(X, Y))
    assert fixture.decode_map[right] == fixture.exp(fixture.add(X, Y))


def test_nonabelian_prime_power_group_complete_recovery():
    group = FiniteGroup(tuple(product(range(9), repeat=3)), (0, 0, 0),
                        lambda x, y: ((x[0]+y[0]) % 9, (x[1]+y[1]) % 9,
                                      (x[2]+y[2]+x[0]*y[1]) % 9),
                        lambda x: (-x[0] % 9, -x[1] % 9, (-x[2]+x[0]*x[1]) % 9))
    H = group.subgroup(((1, 0, 0),))
    report = finite_omega_recovery(group, 3, coset_oracle(group, H))
    assert len(H) == 9 and report["recovered"] == H
    assert report["stages"][0]["omega_order"] == 27
    assert report["stages"][0]["intersection_order"] == 3
    assert report["stages"][0]["normalizer_index"] == 3


@pytest.mark.parametrize("prime,degree", [(3, 3), (2, 2), (7, 0), (7, True), (7, Fraction(3))])
def test_bad_compiler_contract_rejected(prime, degree):
    with pytest.raises(ValueError):
        compile_word(prime, degree, "add")


@pytest.mark.parametrize("order,prime,generator", [(81, 3, 1), (81, 3, 3), (81, 3, 9),
                                                   (81, 3, 0), (125, 5, 5)])
def test_repeated_omega_recovers_higher_order_hidden_elements(order, prime, generator):
    group = cyclic(order)
    hidden = group.subgroup((generator,))
    report = finite_omega_recovery(group, prime, coset_oracle(group, hidden))
    assert report["recovered"] == hidden
    assert prime**len(report["stages"]) <= order
    assert report["enumerated_control"] and not report["quantum_receiver_executed"]
    if generator == 1:
        assert report["stages"][0]["intersection_order"] == prime < len(hidden)
        assert len(report["stages"]) == 4


def test_nonnormal_intersection_normalize_then_quotient_keeps_all_hidden_elements():
    group = heisenberg_times_c9()
    hidden = group.subgroup(((1, 0, 0, 0), (0, 0, 0, 1)))
    report = finite_omega_recovery(group, 3, coset_oracle(group, hidden))
    assert len(hidden) == 27
    assert report["recovered"] == hidden
    assert report["stages"][0] == {
        "ambient_order": 243, "omega_order": 81, "intersection_order": 9,
        "normalizer_index": 3, "next_quotient_order": 9,
        "terminal_trivial_intersection": False}
    assert len(report["stages"]) == 3


def test_incomplete_intersection_can_pass_membership_and_lose_hidden_directions():
    group = heisenberg_times_c9()
    hidden = frozenset(group.elements)
    used = []

    def incomplete(group, S, B, omega, K):
        if used:
            return K
        used.append(True)
        return group.subgroup(((1, 0, 0, 0),))

    report = finite_omega_recovery(group, 3, coset_oracle(group, hidden), incomplete)
    assert report["recovered"] < hidden
    assert (0, 1, 0, 0) not in report["recovered"]


def test_small_prime_involutions_are_not_a_subgroup():
    elements = tuple(product(range(4), range(2)))
    group = FiniteGroup(elements, (0, 0),
                        lambda x, y: ((x[0]+(-1)**x[1]*y[0]) % 4, x[1] ^ y[1]),
                        lambda x: ((-(-1)**x[1]*x[0]) % 4, x[1]))
    involutions = {x for x in elements if group.power(x, 2) == group.identity}
    assert group.subgroup(involutions) != involutions
    with pytest.raises(ValueError, match="do not form"):
        finite_omega_recovery(group, 2, coset_oracle(group, frozenset(elements)))


@pytest.mark.parametrize("k,prime,dimension,cls", [(3, 3, 6, 4), (4, 2, 10, 7), (4, 7, 10, 7)])
def test_small_prime_enumeration_is_parameter_bounded(k, prime, dimension, cls):
    plan = terminal_plan(prime, dimension, cls, k)
    assert plan["branch"] == "bounded_terminal_enumeration"
    assert plan["enumerated_elements"] <= plan["uniform_enumeration_cap"]


@pytest.mark.parametrize("k,prime,dimension,cls", [(3, 5, 6, 4), (4, 11, 10, 7),
                                                  (12, 2**127-1, 78, 23)])
def test_large_prime_bound_preserves_k_and_has_no_field_enumeration(k, prime, dimension, cls):
    plan = terminal_plan(prime, dimension, cls, k)
    assert plan["enumerated_elements"] == 0
    assert plan["intersection_call_cap"] == dimension
    assert plan["per_call_source_multiplier_cap"] <= plan["uniform_source_multiplier_cap"]
    assert plan["original_f_query_cap_for_terminal_rees_sources"] == (
        dimension*cls*plan["per_call_final_fourier_samples"]*plan["per_call_source_multiplier_cap"])
    assert plan["preprocessing_and_coherent_compilation_paid_separately"]
    assert not plan["speedup_claim"]


@pytest.mark.parametrize("args", [(3, 7, 4, 3), (3, 6, 6, 3), (3, 1, 1, 0),
                                   (3, 1, 0, 1), (True, 1, 1, 1)])
def test_invalid_terminal_parameters(args):
    with pytest.raises(ValueError):
        terminal_plan(*args)


def test_known_abelian_branch_and_error_budget():
    assert terminal_plan(2, 3, 1, 2)["branch"] == "known_abelian_hsp"
    with pytest.raises(ValueError):
        terminal_plan(5, 6, 4, 3, error=0)
    coarse = terminal_plan(5, 6, 4, 3, error=Fraction(1, 10))
    fine = terminal_plan(5, 6, 4, 3, error=Fraction(1, 1000))
    assert fine["per_call_final_fourier_samples"] > coarse["per_call_final_fourier_samples"]
