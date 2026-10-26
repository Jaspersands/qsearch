"""Independent finite controls, not an implementation of a general HSP solver.

The regular representation of the truncated free associative algebra supplies
actual matrix multiplication/exp/log. No class-three BCH formula is reused.
"""
from itertools import product
from fractions import Fraction
from math import factorial
import random

from flint import nmod_mat
import numpy as np
import pytest
import sympy as sp

from theorems.affine_phase_erasure import (
    cancellation_weights, initial_packet, leading_columns, square_weights,
    translate_combine,
)
from theorems.nil3_normal_word_bridge import NormalWordLieBridge
from theorems.folded_rs_decoder import affine_solution


def free_matrices():
    words = [w for length in range(5) for w in product((0, 1), repeat=length)]
    index = {word: i for i, word in enumerate(words)}
    generators = []
    for letter in (0, 1):
        matrix = np.zeros((len(words), len(words)), dtype=np.int64)
        for word in words:
            if len(word) < 4:
                matrix[index[(letter,) + word], index[word]] = 1
        generators.append(matrix)
    return generators


class ClassFourFixture:
    p = 7

    def __init__(self):
        self.x, self.y = free_matrices()
        self.identity = np.eye(len(self.x), dtype=np.int64)
        self.z = self.bracket(self.x, self.y)
        self.a = self.bracket(self.x, self.z)
        self.b = self.bracket(self.y, self.z)
        self.c = self.bracket(self.x, self.a)
        self.d = self.bracket(self.y, self.a)
        self.e = self.bracket(self.y, self.b)
        self.normal = [self.z, self.a, self.b, self.c, self.d, self.e]
        self.hidden = self.x + self.z

    def bracket(self, x, y):
        return (x @ y - y @ x) % self.p

    def exp(self, x):
        power, result = self.identity.copy(), self.identity.copy()
        for k in range(1, 5):
            power = power @ x % self.p
            result = (result + pow(factorial(k), -1, self.p) * power) % self.p
        return result

    def log(self, g):
        x = (g - self.identity) % self.p
        power, result = self.identity.copy(), np.zeros_like(x)
        for k in range(1, 5):
            power = power @ x % self.p
            result = (result + (-1)**(k+1) * pow(k, -1, self.p) * power) % self.p
        return result

    def section(self, x, y):
        return x*self.x + y*self.y

    def potential(self, x, y):
        # pi(x,y)=(x,0). This hidden witness is used ONLY in the test.
        word = self.exp(y*self.y) @ self.exp(x*self.hidden) % self.p
        return self.log(word @ self.exp(-self.section(x, y)) % self.p)


@pytest.fixture(scope="module")
def group():
    return ClassFourFixture()


def test_fixture_is_metabelian_and_genuinely_class_four(group):
    basis = [group.x, group.y] + group.normal
    assert nmod_mat([b[:, 0].tolist() for b in basis], group.p).rank() == 8
    assert np.any(group.c)
    assert np.array_equal(group.bracket(group.x, group.b), group.d)
    for a, b in product(group.normal, repeat=2):
        assert not np.any(group.bracket(a, b))
    for a, b in product([group.x, group.y], [group.c, group.d, group.e]):
        assert not np.any(group.bracket(a, b))


def test_matrix_exp_log_and_exponent_p_are_independent_controls(group):
    for x, y in product(range(group.p), repeat=2):
        value = group.section(x, y) + (x + 2*y)*group.z + x*group.b
        matrix = group.exp(value)
        assert np.array_equal(group.log(matrix), value % group.p)
        powered = group.identity.copy()
        for _ in range(group.p):
            powered = powered @ matrix % group.p
        assert np.array_equal(powered, group.identity)


def test_class_three_conjugation_formula_is_no_longer_valid(group):
    actual = group.exp(group.x) @ group.z @ group.exp(-group.x) % group.p
    old_formula = (group.z + group.a) % group.p
    full_formula = (old_formula + pow(2, -1, group.p)*group.c) % group.p
    assert not np.array_equal(actual, old_formula)
    assert np.array_equal(actual, full_formula)


def test_section_potential_matches_actual_right_action_in_class_four(group):
    potentials = {(x, y): group.potential(x, y)
                  for x, y in product(range(group.p), repeat=2)}
    normal = group.z + 2*group.b
    for x, y, t in product(range(group.p), repeat=3):
        q = group.section(x, y)
        q_next = group.section((x+t) % group.p, y)
        actual = group.exp(normal) @ group.exp(q) % group.p
        actual = actual @ group.exp(t*group.hidden) % group.p
        actual_normal = group.log(actual @ group.exp(-q_next) % group.p)
        expected = (normal + potentials[((x+t) % group.p, y)] -
                    potentials[(x, y)]) % group.p
        assert np.array_equal(actual_normal, expected)


def test_full_preimage_is_not_class_two_and_has_no_abelian_index_p_subgroup(group):
    # T = <X,N> for the transverse H=<exp X>. It has class three, not two.
    assert np.any(group.bracket(group.x, group.bracket(group.x, group.z)))
    assert not np.any(group.bracket(
        group.x, group.bracket(group.x, group.bracket(group.x, group.z))))
    # Any index-p subgroup contains [L,L]=N and a nonzero quotient line.
    # That line fails to commute with Z. The whole fixture is not N' ⋊ C_p
    # with abelian N', although each learned basis-line restriction is.
    for x, y in product(range(group.p), repeat=2):
        if x or y:
            assert np.any(group.bracket(group.section(x, y), group.z))


def test_known_line_restriction_has_the_published_split_cyclic_interface(group):
    for s, t in product(range(group.p), repeat=2):
        assert np.array_equal(group.exp(s*group.x) @ group.exp(t*group.x) % group.p,
                              group.exp(((s+t) % group.p)*group.x))
    for t in range(group.p):
        chart = group.log(group.exp(t*group.hidden) @ group.exp(-t*group.x) % group.p)
        expected = (t*group.z + t*t*pow(2, -1, group.p)*group.a +
                    t**3*pow(6, -1, group.p)*group.c) % group.p
        assert np.array_equal(chart, expected)
        assert np.array_equal(group.exp(chart) @ group.exp(t*group.x) % group.p,
                              group.exp(t*group.hidden))


def test_quartic_potential_is_structural_not_interpolated(group):
    x, y = sp.symbols("x y")
    X, Y = [sp.SparseMatrix(m.tolist()) for m in (group.x, group.y)]
    # Use a characteristic-zero bracket, not the reduced fixture's Z.
    Z = X*Y - Y*X
    identity = sp.eye(X.rows)

    def exp(value):
        return sum((value**k / factorial(k) for k in range(1, 5)),
                   identity).applyfunc(sp.expand)

    word = (exp(y*Y) * exp(x*(X+Z)) * exp(-x*X-y*Y)).applyfunc(sp.expand)
    offset = word - identity
    logarithm = sum(((-1)**(k+1)*offset**k / k for k in range(1, 5)),
                    sp.zeros(X.rows)).applyfunc(sp.expand)
    degrees = [sp.Poly(entry, x, y).total_degree() for entry in logarithm if entry]
    assert max(degrees) == 4
    quartic = logarithm.applyfunc(lambda entry: sum(
        coefficient*x**alpha[0]*y**alpha[1]
        for alpha, coefficient in sp.Poly(entry, x, y).terms() if sum(alpha) == 4))
    increment = quartic.subs({x: 2, y: 1}) - quartic.subs({x: 1, y: 1})
    assert any(int(sp.numer(v)) % group.p for v in increment)
    # The quartic part changes along the hidden X direction. Dropping it
    # cannot be excused as a harmless polynomial constant on U-cosets.
    for a, b in [(0, 3), (1, 1), (2, 5), (6, 4)]:
        evaluated = logarithm.subs({x: a, y: b})
        reduced = np.array([
            [int(sp.numer(v)) * pow(int(sp.denom(v)), -1, group.p) % group.p
             for v in evaluated.row(row)] for row in range(X.rows)
        ], dtype=np.int64)
        assert np.array_equal(reduced, group.potential(a, b))


def test_nonmetabelian_class_four_is_not_in_the_scalar_phase_scope():
    def unit(i, j):
        result = np.zeros((5, 5), dtype=np.int64)
        result[i, j] = 1
        return result

    def bracket(a, b):
        return a @ b - b @ a

    a = bracket(unit(0, 1), unit(1, 2))
    b = bracket(unit(2, 3), unit(3, 4))
    assert np.array_equal(bracket(a, b), unit(0, 4))
    assert not np.array_equal((np.eye(5) + a) @ (np.eye(5) + b),
                              (np.eye(5) + b) @ (np.eye(5) + a))


def test_existing_public_packet_algebra_handles_a_quartic_cancellation():
    import random

    p, width = 11, 2
    packets = [initial_packet(p, width, [i, (i*i + 1) % p], max_degree=4)
               for i in range(9)]
    columns = leading_columns(packets, 4)
    square = square_weights(p, columns, random.Random(91))
    # 4*3 = 2 mod 10. This is one explicit finite witness, NOT a new
    # general-degree diagonal solver or an end-to-end class-four receiver.
    weights = [pow(value, 3, p) for value in square]
    assert any(weights)
    assert all(sum(column[j]*pow(c, 4, p) for column, c in zip(columns, weights)) % p == 0
               for j in range(len(columns[0])))
    outcomes = [(i % p, (2*i + 3) % p) for i in range(len(packets))]
    merged = translate_combine(packets, weights, outcomes)
    assert merged.degree == 3
    parameters = [(3*i + 1) % p for i in range(merged.parameter_count)]

    def expected(point):
        return sum(packet.evaluate_fixture(
            tuple((y + c*x) % p for y, x in zip(outcome, point)), parameters)
            for packet, c, outcome in zip(packets, weights, outcomes)) % p

    constant = expected((0, 0))
    for point in product(range(p), repeat=width):
        assert merged.evaluate_fixture(point, parameters) == (expected(point)-constant) % p


def test_production_controller_does_not_pretend_to_implement_degree_four():
    with pytest.raises(ValueError, match="implemented degrees"):
        cancellation_weights([initial_packet(11, 2, [1], max_degree=4)], 4)


def _matrix_span(matrices, p):
    """Small exact reference only; retains independent supplied matrices."""
    basis = []
    for matrix in matrices:
        if not np.any(matrix % p):
            continue
        rows = [m.ravel().tolist() for m in basis + [matrix % p]]
        if nmod_mat(rows, p).rank() > len(basis):
            basis.append(matrix % p)
    return basis


def _matrix_coordinates(matrix, basis, p):
    rows = list(map(list, zip(*(m.ravel().tolist() for m in basis))))
    result = affine_solution(p, rows, matrix.ravel().tolist(), len(basis))
    if result is None:
        return None
    assert not result["basis"]
    return result["offset"]


def _matrix_lower_central(group, basis):
    dimensions, current = [len(basis)], basis
    for _ in range(len(basis)):
        current = _matrix_span([group.bracket(a, b) for a in basis for b in current], group.p)
        dimensions.append(len(current))
        if not current:
            return dimensions
    raise ValueError("reference input is not nilpotent")


def _public_derived_chart(group, ambient):
    normal = _matrix_span([group.bracket(a, b) for a in ambient for b in ambient], group.p)
    if any(np.any(group.bracket(a, b)) for a in normal for b in normal):
        raise ValueError("scalar phase source requires abelian derived ideal")
    adapted = _matrix_span(normal + ambient, group.p)
    assert len(adapted) == len(ambient)
    return normal, adapted[len(normal):]


def _public_descent_step(group, ambient, fourier_rows):
    """PUBLIC arithmetic predicate, not a Fourier sampler or HSP solver.

    Receives no hidden generator, true support or oracle. All samples must
    already come from the current group's correctly erased source.
    """
    normal, section = _public_derived_chart(group, ambient)
    solution = affine_solution(group.p, fourier_rows, [0]*len(fourier_rows), len(section))
    lifts = [sum((a*b for a, b in zip(v, section)), np.zeros_like(ambient[0])) % group.p
             for v in solution["basis"]]
    preimage = _matrix_span(normal + lifts, group.p)
    old_profile = _matrix_lower_central(group, ambient)
    new_profile = _matrix_lower_central(group, preimage)
    return {"basis": preimage, "derived": normal, "section": section,
            "image_basis": solution["basis"], "old_profile": old_profile,
            "new_profile": new_profile,
            "strict_class_drop": len(new_profile) < len(old_profile)}


def _truth_frequencies(group, ambient, hidden):
    """Finite ideal-sampling fixture only; never called by the public predicate."""
    normal, section = _public_derived_chart(group, ambient)
    image = _matrix_coordinates(hidden, normal + section, group.p)[len(normal):]
    return affine_solution(group.p, [image], [0], len(section))["basis"]


def test_certified_class_descent_reaches_an_abelian_group_without_line_finisher(group):
    ambient = [group.x, group.y] + group.normal
    dimensions, classes = [len(ambient)], [4]
    for _ in range(3):
        frequencies = _truth_frequencies(group, ambient, group.hidden)
        step = _public_descent_step(group, ambient, frequencies)
        assert step["strict_class_drop"]
        ambient = step["basis"]
        assert _matrix_coordinates(group.hidden, ambient, group.p) is not None
        assert all(_matrix_coordinates(v, group.normal, group.p) is not None
                   for v in _public_derived_chart(group, ambient)[0])
        dimensions.append(len(ambient))
        classes.append(len(step["new_profile"])-1)
    assert dimensions == [8, 7, 4, 2]
    assert classes == [4, 3, 2, 1]
    # The terminal abelian Fourier nullspace recovers the H direction.
    hidden_coordinates = _matrix_coordinates(group.hidden, ambient, group.p)
    frequencies = affine_solution(group.p, [hidden_coordinates], [0], len(ambient))["basis"]
    recovered = affine_solution(group.p, frequencies, [0]*len(frequencies), len(ambient))["basis"]
    assert len(recovered) == 1
    generator = sum((a*b for a, b in zip(recovered[0], ambient)), np.zeros_like(group.x)) % group.p
    assert _matrix_coordinates(generator, [group.hidden], group.p) is not None

    def original_label(logarithm):
        return min(tuple((group.exp(logarithm) @ group.exp(t*group.hidden) % group.p).ravel())
                   for t in range(group.p))

    identity_label = original_label(np.zeros_like(group.x))
    assert original_label(generator) == identity_label
    # An incomplete terminal rank batch could leave the whole abelian
    # ambient as estimate; original-label checks detect its extra direction.
    assert any(original_label(a) != identity_label for a in ambient)


def test_strict_overestimate_can_pass_the_public_class_drop_guard(group):
    ambient = _public_descent_step(group, [group.x, group.y] + group.normal, [[0, 1]])["basis"]
    normal, section = _public_derived_chart(group, ambient)
    hidden_image = _matrix_coordinates(group.hidden, normal + section, group.p)[len(normal):]
    extra_image = _matrix_coordinates(group.e, normal + section, group.p)[len(normal):]
    assert nmod_mat([hidden_image, extra_image], group.p).rank() == 2
    frequencies = affine_solution(group.p, [hidden_image, extra_image], [0, 0], len(section))["basis"]
    step = _public_descent_step(group, ambient, frequencies)
    assert step["strict_class_drop"]
    assert len(step["image_basis"]) == 2  # True hidden image is a line.
    assert len(step["new_profile"])-1 == 2
    assert _matrix_coordinates(group.hidden, step["basis"], group.p) is not None
    # Extra central directions are harmless: a later restriction still
    # reaches an abelian ambient containing all of H.
    last = _public_descent_step(group, step["basis"],
        _truth_frequencies(group, step["basis"], group.hidden))
    assert last["strict_class_drop"] and len(last["new_profile"])-1 == 1
    assert _matrix_coordinates(group.hidden, last["basis"], group.p) is not None


def test_dimension_reduction_is_not_a_substitute_for_class_reduction(group):
    # Add one central factor. Discarding it reduces dimension but leaves
    # the entire class-four factor, so it cannot certify this recursion.
    pad = lambda a: np.pad(a, ((0, 2), (0, 2)))
    ambient = [pad(a) for a in [group.x, group.y] + group.normal]
    extra = np.zeros_like(ambient[0])
    extra[-2, -1] = 1
    ambient.append(extra)
    step = _public_descent_step(group, ambient, [[0, 0, 1]])
    assert len(step["basis"]) == len(ambient)-1
    assert not step["strict_class_drop"]
    assert len(step["new_profile"])-1 == 4


def test_wrong_fourier_samples_can_lose_h_despite_a_valid_class_drop(group):
    ambient = [group.x, group.y] + group.normal
    step = _public_descent_step(group, ambient, [[1, 0], [0, 1]])
    assert step["strict_class_drop"] and len(step["new_profile"])-1 == 1
    assert _matrix_coordinates(group.hidden, step["basis"], group.p) is None
    # H intersects this abelian ambient trivially. Its trivial answer
    # passes all membership checks but is WRONG for the original input.
    assert all(_matrix_coordinates(group.hidden * t % group.p, step["basis"], group.p) is None
               for t in range(1, group.p))


def test_transversality_and_nontrivial_rank_progress_cannot_be_omitted(group):
    ambient = [group.x, group.y] + group.normal
    step = _public_descent_step(group, ambient, [])
    assert not step["strict_class_drop"]
    assert len(step["basis"]) == len(ambient)
    # If H=G, this is its TRUE quotient image, not a finite-rank failure.
    # The initial normal-intersection reduction is indispensable.


def test_descent_reference_rejects_a_nonabelian_derived_ideal(group):
    ambient = []
    for i in range(5):
        for j in range(i+1, 5):
            matrix = np.zeros((5, 5), dtype=np.int64)
            matrix[i, j] = 1
            ambient.append(matrix)
    with pytest.raises(ValueError, match="abelian derived"):
        _public_descent_step(group, ambient, [])


def inverse_bch_words(multiply, power, a, b, corrected):
    """Test-only rational group words; no logarithm is used in this evaluator."""
    def comm(x, y):
        return multiply(multiply(multiply(power(x, -1), power(y, -1)), x), y)

    w = comm(a, b)
    aw, bw = comm(a, w), comm(b, w)
    added = multiply(multiply(a, b), power(w, Fraction(-1, 2)))
    added = multiply(multiply(added, power(aw, Fraction(-1, 12))),
                     power(bw, Fraction(1, 12)))
    bracket = multiply(multiply(w, power(aw, Fraction(1, 2))),
                       power(bw, Fraction(1, 2)))
    if corrected:
        aaw, baw, bbw = comm(a, aw), comm(b, aw), comm(b, bw)
        added = multiply(multiply(added, power(aaw, Fraction(-1, 24))),
                         power(bbw, Fraction(1, 24)))
        bracket = multiply(multiply(multiply(bracket, power(aaw, Fraction(1, 3))),
                                    power(baw, Fraction(1, 4))), power(bbw, Fraction(1, 3)))
    return added, bracket


def test_inverse_bch_corrections_in_free_rational_algebra_not_interpolation():
    X, Y = [sp.SparseMatrix(matrix.tolist()) for matrix in free_matrices()]
    identity = sp.eye(X.rows)

    def exp(value):
        return sum((value**k / factorial(k) for k in range(1, 5)), identity)

    def log(value):
        return sum(((-1)**(k+1)*(value-identity)**k / k for k in range(1, 5)),
                   sp.zeros(X.rows))

    def power(value, coefficient):
        coefficient = Fraction(coefficient)
        return exp(sp.Rational(coefficient.numerator, coefficient.denominator) * log(value))

    Z = X*Y - Y*X
    A, B = X*Z-Z*X, Y*Z-Z*Y
    C, D, E = X*A-A*X, Y*A-A*Y, Y*B-B*Y
    old_sum, old_bracket = inverse_bch_words(lambda a, b: a*b, power, exp(X), exp(Y), False)
    assert log(old_sum)-X-Y == C/24-E/24
    assert log(old_bracket)-Z == -C/3-D/4-E/3
    fixed_sum, fixed_bracket = inverse_bch_words(lambda a, b: a*b, power, exp(X), exp(Y), True)
    assert log(fixed_sum) == X+Y
    assert log(fixed_bracket) == Z


def finite_matrix_exp_log(value, p, *, logarithm=False):
    identity = np.eye(len(value), dtype=object)
    x = (value-identity) % p if logarithm else value % p
    result = np.zeros_like(identity) if logarithm else identity.copy()
    power = identity.copy()
    for k in range(1, 5):
        power = power @ x % p
        coefficient = (-1)**(k+1)*pow(k, -1, p) if logarithm else pow(factorial(k), -1, p)
        result = (result + coefficient*power) % p
    return result


@pytest.mark.parametrize("p", [5, 7, 11, 2**127-1])
def test_corrected_words_use_only_group_multiplication_and_integer_powers(p):
    rng = random.Random(20261021)
    identity = np.eye(5, dtype=object)
    count = 0

    def multiply(a, b):
        nonlocal count
        count += 1
        return a @ b % p

    def power(value, coefficient):
        coefficient = Fraction(coefficient)
        exponent = coefficient.numerator * pow(coefficient.denominator, -1, p) % p
        result = identity.copy()
        while exponent:
            if exponent & 1:
                result = multiply(result, value)
            value = multiply(value, value)
            exponent //= 2
        return result

    for _ in range(4):
        values = []
        for _ in range(2):
            value = np.zeros((5, 5), dtype=object)
            for i in range(5):
                for j in range(i+1, 5):
                    value[i, j] = rng.randrange(p)
            values.append(value)
        x, y = values
        a, b = [finite_matrix_exp_log(value, p) for value in values]
        added, bracket = inverse_bch_words(multiply, power, a, b, True)
        assert np.array_equal(finite_matrix_exp_log(added, p, logarithm=True), (x+y) % p)
        assert np.array_equal(finite_matrix_exp_log(bracket, p, logarithm=True),
                              (x @ y-y @ x) % p)
    assert count < 1000*p.bit_length()


@pytest.mark.parametrize("flag", ["central", "refined-noncentral"])
def test_existing_flag_peeling_extends_once_correct_lie_words_are_supplied(flag):
    p = 7
    slots = [(i, j) for i in range(5) for j in range(i+1, 5)]
    if flag == "central":
        slots.sort(key=lambda pair: (pair[1]-pair[0], pair))
    identity = np.eye(5, dtype=object)

    def matrix(word):
        result = identity.copy()
        for coefficient, (i, j) in zip(word, slots):
            factor = identity.copy()
            factor[i, j] = coefficient
            result = result @ factor % p
        return result

    def word(value):
        value, result = value.copy(), []
        for i, j in slots:
            coefficient = int(value[i, j]) % p
            result.append(coefficient)
            inverse = identity.copy()
            inverse[i, j] = -coefficient
            value = inverse @ value % p
        assert np.array_equal(value, identity)
        return tuple(result)

    class TestOnlyBridge(NormalWordLieBridge):
        # Reuse ONLY the class-independent peeling/element methods. Its
        # adapted_presentation method is class-three and is not called.
        def rational_power(self, element, coefficient):
            coefficient = Fraction(coefficient)
            return self.power(element, coefficient.numerator *
                              pow(coefficient.denominator, -1, self.p) % self.p)

        def lie_add(self, a, b):
            return inverse_bch_words(self.multiply, self.rational_power, a, b, True)[0]

        def lie_bracket(self, a, b):
            return inverse_bch_words(self.multiply, self.rational_power, a, b, True)[1]

    collector = lambda a, b: word(matrix(a) @ matrix(b) % p)
    bridge = TestOnlyBridge(p, len(slots), collector)
    legacy = NormalWordLieBridge(p, len(slots), collector)
    rng = random.Random(20261022)
    saw_nontrivial_coordinate_change = False
    saw_legacy_mismatch = False
    for _ in range(6):
        original = tuple(rng.randrange(p) for _ in slots)
        logarithm = finite_matrix_exp_log(matrix(original), p, logarithm=True)
        expected = tuple(int(logarithm[i, j]) for i, j in slots)
        assert bridge.coordinates(original) == expected
        assert bridge.element(expected) == original
        saw_nontrivial_coordinate_change |= expected != original
        saw_legacy_mismatch |= legacy.coordinates(original) != expected
    assert saw_nontrivial_coordinate_change
    assert saw_legacy_mismatch
    if flag == "refined-noncentral":
        # This tail is normal only in the preceding tail, not in all UT5.
        e12, e23, e13 = [np.zeros((5, 5), dtype=object) for _ in range(3)]
        e12[0, 1], e23[1, 2], e13[0, 2] = 1, 1, 1
        assert np.array_equal(e12 @ e23-e23 @ e12, e13)
        assert slots.index((0, 2)) < slots.index((1, 2))
