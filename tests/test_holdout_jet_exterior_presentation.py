"""Bounded exact F2 controls, not a quotient algorithm or Goppa assumption test.

Polynomials are sets of integer bitset monomials with coefficient one. The
reference multiplication, elementary forms, Pfaffians, and tiny elimination
below do not use producer algebra. Only actual jet columns come from analyze.
Caps are checked before expansion; no full-size quotient matrix is constructed.
"""

from fractions import Fraction
from itertools import combinations
from math import comb

import pytest

from theorems import holdout_jet_audit as audit


MAX_VARIABLES = 13
MAX_POLYNOMIAL_TERMS = 2048
MAX_MULTIPLICATION_PAIRS = 100_000
MAX_JET_VARIABLES = 7
MAX_JET_ROWS = 64
MAX_JET_COLUMNS = 256
MAX_JET_ENTRIES = 8192  # Includes the held-out target.
MAX_PAIR_GENERATORS = 128
MAX_PFAFFIAN_VARIABLES = 8
MAX_PFAFFIAN_ORDER = 4  # At most 105 perfect matchings per coefficient.
MAX_KERNEL_ENUM_COORDINATES = 15  # At most 32768 coefficient assignments.


def _mask(indices):
    return sum(1 << i for i in indices)


def _subsets(k, degree):
    if not 0 <= k <= MAX_VARIABLES:
        raise ValueError("variable cap")
    if degree < 0 or degree > k:
        return ()
    if comb(k, degree) > MAX_POLYNOMIAL_TERMS:
        raise ValueError("polynomial term cap")
    return tuple(_mask(indices) for indices in combinations(range(k), degree))


def _multiply(left, right):
    """Multiply in F2[x]/(x_i^2), using disjoint unions and XOR cancellation."""
    if max(len(left), len(right)) > MAX_POLYNOMIAL_TERMS:
        raise ValueError("polynomial term cap")
    if len(left) * len(right) > MAX_MULTIPLICATION_PAIRS:
        raise ValueError("multiplication pair cap")
    if any(term < 0 or term.bit_length() > MAX_VARIABLES for term in (*left, *right)):
        raise ValueError("variable cap")
    result = set()
    for a in left:
        for b in right:
            if a & b:
                continue
            term = a | b
            if term in result:
                result.remove(term)
            else:
                result.add(term)
            if len(result) > MAX_POLYNOMIAL_TERMS:
                raise ValueError("polynomial term cap")
    return frozenset(result)


def _elementary(k, point, degree):
    if not 0 <= point < 1 << k:
        raise ValueError("point outside public coordinate space")
    return frozenset(term for term in _subsets(k, degree) if term & point == term)


def _pfaffian(vertices, edges):
    """Independent matching recurrence; signs disappear in characteristic two."""
    if not vertices:
        return 1
    first, rest = vertices[0], vertices[1:]
    value = 0
    for index, other in enumerate(rest):
        if ((1 << first) | (1 << other)) in edges:
            value ^= _pfaffian(rest[:index] + rest[index + 1:], edges)
    return value


def _gamma(k, quadratic, order):
    if not 0 <= k <= MAX_PFAFFIAN_VARIABLES or not 0 <= order <= MAX_PFAFFIAN_ORDER:
        raise ValueError("Pfaffian cap")
    assert all(term.bit_count() == 2 and term.bit_length() <= k for term in quadratic)
    return frozenset(
        _mask(vertices)
        for vertices in combinations(range(k), 2 * order)
        if _pfaffian(vertices, quadratic)
    )


def _produce(k, degree, multiplicity, points):
    if not 1 <= k <= MAX_JET_VARIABLES:
        raise ValueError("jet variable cap")
    rows = comb(k, degree)
    columns = (len(points) - 1) * sum(comb(k, u) for u in range(multiplicity))
    if rows > MAX_JET_ROWS or columns > MAX_JET_COLUMNS or rows * (columns + 1) > MAX_JET_ENTRIES:
        raise ValueError("jet matrix cap")
    public = [[(point >> i) & 1 for point in points] for i in range(k)]
    result = audit.analyze(
        public, degree, multiplicity, len(points) - 1,
        max_monomials=MAX_JET_ROWS, max_entries=MAX_JET_ENTRIES,
    )
    assert result["operator"] == "full_hasse"
    assert result["dimensions"]["training_columns"] == columns
    assert result["dimensions"]["monomials"] == rows
    return result


def _pack(polynomial, basis):
    assert len(basis) <= MAX_JET_ROWS
    assert polynomial <= set(basis)
    return sum(1 << index for index, term in enumerate(basis) if term in polynomial)


def _columns_by_block(result):
    blocks = {}
    for label, column in zip(result["training_columns"], result["packed_training_columns"]):
        blocks.setdefault(label["point"], {})[_mask(label["derivative"])] = column
    return blocks


def _pair_generators(k, degree, a, b, sa, sb):
    indices = [
        (i, ip) for i in range(degree - sa + 1, degree + 1)
        for ip in range(degree - sb + 1, degree - i + 1)
    ]
    if sum(comb(k, degree - i - ip) for i, ip in indices) > MAX_PAIR_GENERATORS:
        raise ValueError("pair generator cap")
    for i, ip in indices:
        ga, gb = _elementary(k, a, i), _elementary(k, b, ip)
        for c in _subsets(k, degree - i - ip):
            at_a = _multiply({c}, gb)
            at_b = _multiply({c}, ga)
            yield at_a, at_b, _multiply(ga, at_a)


def _image(columns, coefficients):
    result = 0
    for index, column in enumerate(columns):
        if coefficients >> index & 1:
            result ^= column
    return result


def _eliminate(columns, row_cap=MAX_JET_ROWS):
    """Tiny independent column elimination, tracking only exact F2 relations."""
    if len(columns) > MAX_JET_COLUMNS or any(c.bit_length() > row_cap for c in columns):
        raise ValueError("linear algebra cap")
    pivots, relations = {}, []
    for index, column in enumerate(columns):
        value, relation = column, 1 << index
        while value:
            pivot = value.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = (value, relation)
                break
            old_value, old_relation = pivots[pivot]
            value ^= old_value
            relation ^= old_relation
        if not value:
            relations.append(relation)
    return len(pivots), relations


def test_sparse_square_zero_multiplication_keeps_characteristic_two():
    assert _multiply({0}, {1, 2}) == {1, 2}
    assert _multiply(set(), {1}) == set()
    assert _multiply({1}, {1}) == set()
    assert _multiply({1}, {2}) == {3}
    assert _multiply({1, 2}, {1, 2}) == set()
    assert _elementary(4, 0, 0) == {0}
    assert _elementary(4, 0, 1) == set()
    assert _elementary(4, 15, 5) == set()


@pytest.mark.parametrize("k,d,s,points", [
    (3, 2, 1, (0, 1, 7)),
    (4, 3, 2, (1, 6, 15)),
    (6, 4, 3, (0, 21, 63)),
    (7, 5, 4, (0b1011011, 0b1101101, 0b0111110)),
    (7, 5, 3, (0b1011011, 0b1011011, 1)),
])
def test_elementary_forms_match_every_actual_producer_jet_column(k, d, s, points):
    result = _produce(k, d, s, points)
    basis = tuple(_mask(monomial) for monomial in result["monomials"])
    for label, actual in zip(result["training_columns"], result["packed_training_columns"]):
        derivative = _mask(label["derivative"])
        expected = _multiply(
            {derivative}, _elementary(k, points[label["point"]], d - derivative.bit_count()),
        )
        assert actual == _pack(expected, basis)
    assert result["packed_target"] == _pack(_elementary(k, points[-1], d), basis)


@pytest.mark.parametrize("k,d,a,b,sa,sb", [
    (6, 4, 0b111111, 0b101101, 3, 3),
    (7, 5, 0b1011011, 0b1101101, 4, 4),
    (7, 5, 0b1011011, 0b1101101, 3, 4),
    (7, 5, 0b1111111, 0b1111111, 4, 4),
])
def test_pair_products_are_actual_two_block_relations(k, d, a, b, sa, sb):
    result = _produce(k, d, max(sa, sb), (a, b, 0))
    basis = tuple(_mask(monomial) for monomial in result["monomials"])
    blocks = _columns_by_block(result)
    checked = 0
    for at_a, at_b, polynomial in _pair_generators(k, d, a, b, sa, sb):
        assert all(term.bit_count() < sa for term in at_a)
        assert all(term.bit_count() < sb for term in at_b)
        image_a, image_b = 0, 0
        for derivative in at_a:
            image_a ^= blocks[0][derivative]
        for derivative in at_b:
            image_b ^= blocks[1][derivative]
        assert image_a == image_b == _pack(polynomial, basis)
        assert image_a ^ image_b == 0
        checked += 1
    assert 0 < checked <= MAX_PAIR_GENERATORS


@pytest.mark.parametrize("k,d,s,point", [
    (5, 3, 1, 0b11101),
    (6, 4, 3, 0b010010),
    (7, 4, 3, 0b1010101),
    (7, 5, 4, 0b0010101),
])
def test_native_jet_identity_minor_proves_symbolic_rank_bound(k, d, s, point):
    """With e=d-s+1, an e-subset W of the ones gives rank >= C(k-w,s-1).

    Equal-sized zero-support S,S' satisfy S' <= W union S iff S'=S.
    The remaining factor on the diagonal is y^W=1, so this is an identity
    minor, not a dimension assumption. Only the bounded instances expand.
    """
    result = _produce(k, d, s, (point, 0))
    block = _columns_by_block(result)[0]
    support = tuple(i for i in range(k) if point >> i & 1)
    zeros = tuple(i for i in range(k) if not (point >> i & 1))
    e, w = d - s + 1, len(support)
    assert w >= e and len(zeros) >= s - 1
    W = _mask(support[:e])
    derivatives = tuple(_mask(S) for S in combinations(zeros, s - 1))
    row_indices = {_mask(B): i for i, B in enumerate(result["monomials"])}
    assert len(derivatives) == comb(k - w, s - 1)
    for S in derivatives:
        row = row_indices[W | S]
        for Sp in derivatives:
            assert ((block[Sp] >> row) & 1) == int(S == Sp)
    rank, _ = _eliminate(list(block.values()))
    assert rank == result["gf2"]["rank"] >= comb(k - w, s - 1)
    # Apply the proved symbolic bound without constructing a larger operator.
    assert comb(150 - 75, 6 - 1) == 17_259_390


@pytest.mark.parametrize("target,member", [
    (0b001111, True),
    (0b111111, False),
    (0, True),
])
def test_augmented_native_kernel_counts_and_single_bit_readout(target, member):
    k, d, s = 6, 3, 2
    units = tuple(1 << i for i in range(k))
    result = _produce(k, d, s, (*units, 0b011100, 0b010011, target))
    blocks = _columns_by_block(result)
    assert all(column == 0 for j in range(k) for column in blocks[j].values())
    # Remove zero systematic blocks; held-out jets stay absent, with only b appended.
    assert result["dimensions"]["heldout_points_in_training"] == 0
    columns = [*blocks[k].values(), *blocks[k + 1].values()]
    b = result["packed_target"]
    augmented = [*columns, b]
    assert len(augmented) <= MAX_KERNEL_ENUM_COORDINATES
    rank, training_kernel = _eliminate(columns)
    augmented_rank, _ = _eliminate(augmented)
    delta = augmented_rank - rank
    assert rank == result["gf2"]["rank"] == 8
    assert result["gf2"]["member"] is member
    assert delta == int(not member)

    counts = [0, 0]
    for coefficients in range(1 << len(augmented)):
        if _image(augmented, coefficients) == 0:
            counts[(coefficients >> len(columns)) & 1] += 1
    assert counts[0] == 1 << (len(columns) - rank)
    assert counts[1] == (counts[0] if member else 0)
    assert Fraction(sum(counts), 1 << len(augmented)) == Fraction(1, 1 << (rank + delta))
    assert Fraction(counts[1], sum(counts)) == Fraction(int(member), 2)

    # Even the whole training kernel supplies no t=1 solution when b != 0.
    # This does not assert that generated local relations exhaust that kernel.
    assert len(training_kernel) <= MAX_KERNEL_ENUM_COORDINATES
    for coefficients in range(1 << len(training_kernel)):
        v = _image(training_kernel, coefficients)
        assert _image(augmented, v) == 0
        assert _image(augmented, v | (1 << len(columns))) == b


def test_explicit_tiny_local_quotient_preserves_syndrome_rank():
    k, d, s = 6, 4, 3
    a, b = 0b111111, 0b101101
    result = _produce(k, d, s, (a, b, 0))
    blocks = _columns_by_block(result)
    derivatives = tuple(blocks[0])
    assert tuple(blocks[1]) == derivatives
    width = len(derivatives)
    positions = {term: i for i, term in enumerate(derivatives)}
    columns = [*blocks[0].values(), *blocks[1].values()]
    local = []
    for j in range(2):
        _, internal = _eliminate(list(blocks[j].values()))
        local.extend(relation << (j * width) for relation in internal)
    pairs = []
    for at_a, at_b, _ in _pair_generators(k, d, a, b, s, s):
        pairs.append(
            sum(1 << positions[term] for term in at_a)
            | sum(1 << (width + positions[term]) for term in at_b)
        )
    assert pairs and all(pairs)
    local.extend(pairs)
    assert all(_image(columns, relation) == 0 for relation in local)
    local_rank, _ = _eliminate(local, row_cap=len(columns))
    assert local_rank > 0

    # Explicit bounded elimination constructs representatives here. This checks
    # rank preservation, not efficient generator access from a symbolic description.
    span, span_rank, representatives = list(local), local_rank, []
    for i in range(len(columns)):
        candidate = 1 << i
        next_rank, _ = _eliminate([*span, candidate], row_cap=len(columns))
        if next_rank > span_rank:
            span.append(candidate)
            representatives.append(candidate)
            span_rank = next_rank
    assert span_rank == len(columns)
    assert len(representatives) == len(columns) - local_rank
    quotient_columns = [_image(columns, v) for v in representatives]
    rank, _ = _eliminate(columns)
    quotient_rank, _ = _eliminate(quotient_columns)
    assert quotient_rank == rank == result["gf2"]["rank"]
    assert Fraction(1 << (len(representatives) - quotient_rank),
                    1 << len(representatives)) == Fraction(1, 1 << rank)


def test_minimal_support_native_membership_criterion():
    k, d, s = 6, 3, 2
    point = 0b010010
    assert point.bit_count() == d - s + 1
    assert k <= MAX_JET_VARIABLES
    seen = set()
    for target in range(1 << k):
        result = _produce(k, d, s, (point, target))
        columns = result["packed_training_columns"]
        nonzero = [column for column in columns if column]
        rank, _ = _eliminate(columns)
        assert len(nonzero) == len(set(nonzero)) == rank == comb(k - point.bit_count(), s - 1)
        assert all(column & (column - 1) == 0 for column in nonzero)
        expected = target.bit_count() < d or (
            target.bit_count() == d and target & point == point
        )
        augmented_rank, _ = _eliminate([*columns, result["packed_target"]])
        assert (augmented_rank == rank) == result["gf2"]["member"] == expected
        seen.add((result["packed_target"] == 0, expected))
    assert seen == {(True, True), (False, True), (False, False)}


def test_pfaffian_reference_counts_matchings_modulo_two():
    complete = frozenset(_subsets(4, 2))
    assert _pfaffian((0, 1, 2, 3), complete) == 1  # Three matchings, not zero.
    assert _gamma(4, {0b0011, 0b1100}, 2) == {0b1111}
    assert _gamma(4, {0b0011, 0b0101}, 2) == set()


@pytest.mark.parametrize("k,points", [
    (6, tuple(range(64))),
    (8, (0, 1, 0b10101010, 0b01111111, 0b11111111)),
])
def test_gamma_identities_use_independent_pfaffians(k, points):
    for point in points:
        linear = _elementary(k, point, 1)
        quadratic = _elementary(k, point, 2)
        for order in range(k // 2 + 1):
            divided = _gamma(k, quadratic, order)
            assert divided == _elementary(k, point, 2 * order)
            assert _multiply(linear, divided) == _elementary(k, point, 2 * order + 1)


def test_tiny_step_two_quotient_matches_ideal_product_presentation():
    k, d, s, sp = 7, 5, 4, 3
    a, b = 0b1011011, 0b1101101
    result = _produce(k, d, s, (a, b, 0))
    basis = tuple(_mask(monomial) for monomial in result["monomials"])
    block = _columns_by_block(result)[0]
    derivatives, columns = tuple(block), list(block.values())
    positions = {term: index for index, term in enumerate(derivatives)}
    rank, internal = _eliminate(columns)
    assert all(_image(columns, relation) == 0 for relation in internal)
    projected, ideal_images = [], []
    for at_a, _, polynomial in _pair_generators(k, d, a, b, s, s):
        projected.append(sum(1 << positions[term] for term in at_a))
        ideal_images.append(_pack(polynomial, basis))
    nuisance = []
    for derivative in derivatives:
        if derivative.bit_count() <= s - sp:
            nuisance.append(1 << positions[derivative])
            ideal_images.append(_pack(_multiply(
                {derivative}, _elementary(k, a, d - derivative.bit_count()),
            ), basis))
    denominator_rank, _ = _eliminate(internal + projected + nuisance, row_cap=len(columns))
    image_rank, _ = _eliminate(ideal_images)
    assert len(columns) == 64 and len(basis) == 21
    assert len(columns) - denominator_rank == rank - image_rank == 8


def test_k13_d7_quadratic_only_replacement_has_sparse_annihilator_witness():
    k, point, f = 13, (1 << 13) - 1, frozenset({0b111})
    g2, g4, g6 = (_elementary(k, point, r) for r in (2, 4, 6))
    assert _multiply(g2, g2) == set()
    assert _multiply(g2, g4) == g6
    degree_seven = _multiply(g4, f)
    witness = _multiply(g2, degree_seven)
    assert all(term.bit_count() == 7 for term in degree_seven)
    assert witness == _multiply(g6, f)
    assert len(witness) == comb(10, 6) == 210
    assert all(term.bit_count() == 9 for term in witness)
    # If degree_seven = g2*u with u in A_5, g2*degree_seven would be zero.
    assert witness


def test_expansion_budgets_are_enforced_before_producer_call(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("producer called after budget exceeded")

    monkeypatch.setattr(audit, "analyze", forbidden)
    with pytest.raises(ValueError, match="jet variable cap"):
        _produce(13, 7, 6, (0, 1))
    with pytest.raises(ValueError, match="jet matrix cap"):
        _produce(7, 5, 4, (0,) * 6)
    with pytest.raises(ValueError, match="variable cap"):
        _subsets(14, 2)
    with pytest.raises(ValueError, match="multiplication pair cap"):
        _multiply(frozenset(range(400)), frozenset(range(400)))
    with pytest.raises(ValueError, match="Pfaffian cap"):
        _gamma(9, frozenset(), 2)
    with pytest.raises(ValueError, match="pair generator cap"):
        list(_pair_generators(13, 7, 0, 0, 6, 6))
