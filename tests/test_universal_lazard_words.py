from dataclasses import replace
from fractions import Fraction
import random

import pytest

from theorems.class_four_group_words import ClassFourGroupWords
from theorems.free_lazard_pullback import OpaqueFreePullback, free_lazard_domain
from theorems.universal_lazard_words import UniversalLazardWords, compile_lazard_word, build_report


class MatrixFixture:
    """Independent matrix multiplication/exp; the evaluator only gets tokens."""
    def __init__(self, n, p):
        self.n, self.p = n, p
        self.zero = tuple((0,)*n for _ in range(n))
        self.identity = tuple(tuple(int(i == j) for j in range(n)) for i in range(n))
        self.encoded, self.decoded = {}, {}

    def encode(self, matrix):
        if matrix not in self.encoded:
            token = object()
            self.encoded[matrix], self.decoded[token] = token, matrix
        return self.encoded[matrix]

    def matrix_multiply(self, A, B):
        n, p = self.n, self.p
        # Actual matrix multiplication; no BCH or compiler polynomial routines.
        C = [[0]*n for _ in range(n)]
        for i in range(n):
            for k in range(n):
                if A[i][k]:
                    for j in range(n):
                        C[i][j] += A[i][k]*B[k][j]
        return tuple(tuple(x % p for x in row) for row in C)

    def multiply(self, a, b):
        return self.encode(self.matrix_multiply(self.decoded[a], self.decoded[b]))

    def add(self, A, B, scalar=1):
        return tuple(tuple((a+scalar*b) % self.p for a, b in zip(ar, br)) for ar, br in zip(A, B))

    def exponential(self, X):
        result, term = self.identity, self.identity
        for k in range(1, self.n):
            term = self.matrix_multiply(term, X)
            term = self.add(self.zero, term, pow(k, -1, self.p))
            result = self.add(result, term)
        return result

    def random_lie(self, seed):
        rng = random.Random(seed)
        return tuple(tuple(rng.randrange(self.p) if i < j else 0 for j in range(self.n))
                     for i in range(self.n))


@pytest.mark.parametrize("c", range(1, 9))
@pytest.mark.parametrize("operation", ("add", "bracket"))
def test_exact_universal_certificates_all_coefficients(c, operation):
    certificate = compile_lazard_word(c, operation)
    certificate.verify()
    assert len(certificate.stages) == c
    assert certificate.stages[-1][1] == certificate.output


@pytest.mark.parametrize("c,p", ((1, 3), (2, 3), (3, 5), (4, 5), (5, 7), (6, 7), (5, 2**127-1)))
def test_words_on_opaque_matrices_with_independent_exponential(c, p):
    fixture = MatrixFixture(c+1, p)
    X, Y = fixture.random_lie(105), fixture.random_lie(506)
    x, y = (fixture.encode(fixture.exponential(Z)) for Z in (X, Y))
    words = UniversalLazardWords(p, c, fixture.encode(fixture.identity), fixture.multiply)
    before = words.multiplication_calls
    actual_sum = words.lie_add(x, y)
    assert words.multiplication_calls-before <= words.operation_caps()["lie_add"]
    before = words.multiplication_calls
    actual_bracket = words.lie_bracket(x, y)
    assert words.multiplication_calls-before <= words.operation_caps()["lie_bracket"]
    bracket = fixture.add(fixture.matrix_multiply(X, Y), fixture.matrix_multiply(Y, X), -1)
    assert fixture.decoded[actual_sum] == fixture.exponential(fixture.add(X, Y))
    assert fixture.decoded[actual_bracket] == fixture.exponential(bracket)
    combination = words.linear_combination((x, y), (2, p-1))
    assert fixture.decoded[combination] == fixture.exponential(fixture.add(fixture.add(fixture.zero, X, 2), Y, -1))
    if c == 4:
        old = ClassFourGroupWords(p, fixture.encode(fixture.identity), fixture.multiply)
        assert old.lie_add(x, y) == actual_sum
        assert old.lie_bracket(x, y) == actual_bracket
        assert words.operation_caps()["lie_add"] > old.operation_caps()["lie_add"]


def test_forged_certificates_and_wrong_denominators_rejected():
    certificate = compile_lazard_word(3, "add")
    with pytest.raises(ValueError):
        replace(certificate, output=0).verify()
    steps = list(certificate.instructions)
    i = next(i for i, step in enumerate(steps) if step[0] == "pow" and step[-1] > 1)
    _, source, numerator, denominator = steps[i]
    steps[i] = ("pow", source, numerator+denominator, denominator)
    with pytest.raises(ValueError):
        replace(certificate, instructions=tuple(steps)).verify()
    steps[i] = ("pow", source, 1, 13)
    with pytest.raises(ValueError, match="denominator"):
        replace(certificate, instructions=tuple(steps)).verify()
    with pytest.raises(ValueError, match="stage"):
        replace(certificate, stages=certificate.stages[:-1]).verify()


def test_lower_class_word_is_not_a_valid_substitute():
    fixture = MatrixFixture(6, 7)
    X, Y = fixture.random_lie(105), fixture.random_lie(506)
    x, y = (fixture.encode(fixture.exponential(Z)) for Z in (X, Y))
    incomplete = UniversalLazardWords(7, 4, fixture.encode(fixture.identity), fixture.multiply)
    assert fixture.decoded[incomplete.lie_add(x, y)] != fixture.exponential(fixture.add(X, Y))
    complete = UniversalLazardWords(7, 5, fixture.encode(fixture.identity), fixture.multiply)
    assert fixture.decoded[complete.lie_add(x, y)] == fixture.exponential(fixture.add(X, Y))


def test_free_pullback_extends_to_class_five_without_target_coordinates():
    fixture = MatrixFixture(6, 7)
    X, Y = fixture.random_lie(105), fixture.random_lie(506)
    domain = free_lazard_domain(7, 2, 5)
    bridge = OpaqueFreePullback(domain, tuple(fixture.encode(fixture.exponential(Z)) for Z in (X, Y)),
                               fixture.encode(fixture.identity), fixture.multiply)
    assert isinstance(bridge.words, UniversalLazardWords)
    assert any(g != bridge.words.identity for w, g in zip(domain.bracket_words, bridge.basis_images) if len(w) == 5)
    rng = random.Random(547)
    a, b = [tuple(rng.randrange(7) for _ in range(domain.dimension)) for _ in range(2)]
    before = bridge.words.multiplication_calls
    encoded_a = bridge.evaluate(a)
    assert bridge.words.multiplication_calls-before <= bridge.accounting()["per_map_group_multiplication_cap"]
    assert bridge.evaluate(domain.multiply(a, b)) == fixture.multiply(encoded_a, bridge.evaluate(b))


def test_scope_and_bad_inputs():
    for c in (0, -1, True, Fraction(3, 1)):
        with pytest.raises(ValueError):
            compile_lazard_word(c, "add")
    with pytest.raises(ValueError):
        compile_lazard_word(3, "multiply")
    with pytest.raises(ValueError):
        UniversalLazardWords(3, 3, 0, lambda a, b: (a+b) % 3)
    report = build_report()
    assert len(report["certificates"]) == 12
    for key in ("uniform_polynomial_cost_in_class", "target_chart_required", "quantum_circuit_synthesized",
                "hidden_subgroup_recovery_implemented", "novelty_established", "speedup_claim_allowed"):
        assert report[key] is False
