"""Fixed GF32 scalar-cover falsifier, not a canonical-size or global sampler.

All arithmetic and enumerations are independent of the production backend.
Integer labels refer only to the polynomial basis modulo t^5 + t^2 + 1.
The rejection control repairs a conditional LOCAL point law, not a regular
flat source or the native Hx=0 fiber. No parity constraints are imposed here.
"""

from collections import Counter
from fractions import Fraction

import pytest


BITS = 5
Q = 1 << BITS
MODULUS = 0b100101
D = 3
D_INVERSE = 21
V = (0, 1, 2, 3)
EXPECTED_ALPHABET = (1, 6, 8, 9, 10, 11, 14, 15, 18, 19, 20, 22, 25, 29, 30, 31)
EXPECTED_PLANES = (
    (1, 6, 8, 15),
    (1, 10, 22, 29),
    (1, 15, 19, 29),
    (6, 10, 18, 30),
    (6, 11, 18, 31),
    (6, 11, 19, 30),
    (6, 14, 22, 30),
    (6, 15, 20, 29),
    (8, 9, 10, 11),
    (8, 15, 25, 30),
    (9, 11, 20, 22),
    (14, 15, 18, 19),
)
DUAL = {1: 1, 14: 1, 20: 1, 25: 1, 15: -1, 22: -1}


def _multiply(left, right):
    result = 0
    while right:
        if right & 1:
            result ^= left
        right >>= 1
        left <<= 1
        if left & Q:
            left ^= MODULUS
    return result


def _power(value, exponent):
    result = 1
    while exponent:
        if exponent & 1:
            result = _multiply(result, value)
        value = _multiply(value, value)
        exponent >>= 1
    return result


def _inv0(value):
    return _power(value, Q - 2) if value else 0


def _trace(value):
    result = 0
    for _ in range(BITS):
        result ^= value
        value = _multiply(value, value)
    return result


def _predicate(value):
    return _trace(_power(_inv0(value), D))


def _binary_rank(rows):
    pivots = {}
    for row in rows:
        while row:
            pivot = row.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = row
                break
            row ^= pivots[pivot]
    return len(pivots)


def _tv(left, right):
    return sum((abs(left.get(x, 0) - right.get(x, 0))
                for x in left.keys() | right.keys()), Fraction(0)) / 2


@pytest.fixture(scope="module")
def control():
    alphabet = tuple(x for x in range(Q) if _predicate(x) == 1)
    accepted = set(alphabet)
    planes = set()
    affine_images_examined = 0
    for origin in range(Q):
        for scalar in range(1, Q):
            affine_images_examined += 1
            plane = tuple(sorted(origin ^ _multiply(scalar, v) for v in V))
            if set(plane) <= accepted:
                planes.add(plane)

    # Original law: uniform a, then uniform solution mu when consistent.
    # Retain the raw one-trial failure mass before conditioning on success.
    records = []
    occurrences = Counter()
    raw_flat_law = Counter()
    for origin in range(Q):
        if origin in V:
            continue
        points = tuple(origin ^ v for v in V)
        coefficients = tuple(_power(_inv0(z), D) for z in points)
        rows = tuple(sum(_trace(_multiply(c, 1 << j)) << j
                         for j in range(BITS)) for c in coefficients)
        solutions = tuple(mu for mu in range(Q)
                          if all(_trace(_multiply(mu, c)) == 1 for c in coefficients))
        mask_solutions = tuple(mu for mu in range(Q)
                               if all((row & mu).bit_count() % 2 == 1 for row in rows))
        assert solutions == mask_solutions
        records.append((origin, _binary_rank(rows), solutions))
        for mu in solutions:
            assert mu != 0
            scale = _power(mu, D_INVERSE)
            assert scale != 0 and _power(scale, D) == mu
            plane = tuple(sorted(_multiply(z, _inv0(scale)) for z in points))
            assert 0 not in plane and all(_predicate(x) == 1 for x in plane)
            occurrences[plane] += 1
            raw_flat_law[plane] += Fraction(1, Q * len(solutions))

    success = sum(raw_flat_law.values(), Fraction(0))
    flat_law = {plane: mass / success for plane, mass in raw_flat_law.items()}
    point_law = {x: sum((mass / len(plane) for plane, mass in flat_law.items()
                        if x in plane), Fraction(0)) for x in alphabet}
    return {
        "alphabet": alphabet,
        "planes": tuple(sorted(planes)),
        "affine_images_examined": affine_images_examined,
        "records": records,
        "occurrences": occurrences,
        "raw_flat_law": raw_flat_law,
        "success": success,
        "flat_law": flat_law,
        "point_law": point_law,
        "incidence": Counter(x for plane in planes for x in plane),
    }


def test_independent_field_arithmetic_and_full_accepted_alphabet(control):
    assert MODULUS == 0b100101
    assert _multiply(1 << 4, 2) == 0b00101
    assert (D * D_INVERSE) % (Q - 1) == 1
    for x in range(Q):
        assert _power(x, Q) == x
        assert _trace(x) in (0, 1)
        assert _predicate(x) == _trace(_power(x, Q - 1 - D))
        if x:
            assert _multiply(x, _inv0(x)) == 1
        for y in range(Q):
            assert _trace(x ^ y) == (_trace(x) ^ _trace(y))
    assert _inv0(0) == _predicate(0) == 0
    assert control["alphabet"] == EXPECTED_ALPHABET
    assert len(control["alphabet"]) == Q // 2
    assert 0 not in control["alphabet"]


def test_affine_images_and_original_scalar_law_have_the_same_twelve_planes(control):
    assert control["affine_images_examined"] == Q * (Q - 1) == 992
    assert control["planes"] == EXPECTED_PLANES
    assert tuple(sorted(control["occurrences"])) == EXPECTED_PLANES
    assert set(control["occurrences"].values()) == {4}
    for plane in control["planes"]:
        assert len(set(plane)) == len(V) == 4
        assert _binary_rank(tuple(x ^ plane[0] for x in plane)) == 2
        assert 0 not in plane
        assert all(_predicate(x) == 1 for x in plane)


def test_all_successful_translations_have_rank_four_and_paid_uniform_law(control):
    records = control["records"]
    successful = [record for record in records if record[2]]
    assert len(records) == Q - len(V) == 28
    assert len(successful) == 24
    assert len(records) - len(successful) == 4
    assert all(rank == 4 and len(solutions) == 2 and 0 not in solutions
               for _, rank, solutions in successful)
    assert control["success"] == Fraction(3, 4)
    assert 1 - control["success"] == Fraction(len(V) + 4, Q)
    assert set(control["raw_flat_law"].values()) == {Fraction(1, 16)}
    assert set(control["flat_law"].values()) == {Fraction(1, 12)}
    assert sum(control["point_law"].values()) == 1


def test_exact_point_incidence_and_uniform_flat_point_bias(control):
    incidence = control["incidence"]
    assert set(incidence) == set(EXPECTED_ALPHABET)
    assert sum(incidence.values()) == 12 * 4
    assert min(incidence.values()) == 1 and max(incidence.values()) == 6
    assert incidence[6] == 6 and incidence[25] == incidence[31] == 1
    assert control["point_law"] == {x: Fraction(count, 48)
                                    for x, count in incidence.items()}
    uniform = {x: Fraction(1, 16) for x in EXPECTED_ALPHABET}
    assert _tv(control["point_law"], uniform) == Fraction(7, 48)


def test_integer_dual_certificate_excludes_every_regular_reweighting(control):
    """h^T B=0 and h^T 1=2 contradict B w=c 1 for any c>0, even signed w."""
    assert set(DUAL) <= set(control["alphabet"])
    assert all(isinstance(value, int) for value in DUAL.values())
    assert all(sum(DUAL.get(x, 0) for x in plane) == 0 for plane in control["planes"])
    assert sum(DUAL.get(x, 0) for x in control["alphabet"]) == 2


def test_dual_certificate_proves_universal_local_tv_lower_bound(control):
    """Each component has E[h]=0, hence so does every probability mixture.

    Uniform A has E[h]=1/8. Since ||h||_infinity=1, the expectation gap
    is at most 2*TV, proving TV>=1/16 without enumerating mixture weights.
    """
    component_means = [Fraction(sum(DUAL.get(x, 0) for x in plane), len(plane))
                       for plane in control["planes"]]
    assert set(component_means) == {Fraction(0)}
    uniform_mean = sum((Fraction(DUAL.get(x, 0), len(control["alphabet"]))
                        for x in control["alphabet"]), Fraction(0))
    norm = max(abs(DUAL.get(x, 0)) for x in control["alphabet"])
    assert uniform_mean == Fraction(1, 8) and norm == 1
    assert abs(uniform_mean) / (2 * norm) == Fraction(1, 16)


def test_point_dependent_rejection_repairs_only_the_conditional_local_law(control):
    """Incidence means the integer number of planes, not inclusion probability.

    Accept a proposed point x with probability 1/incidence(x). This changes
    the conditional point law WITHIN a flat, so it evades rather than repairs
    the regular-cover obstruction. The finite enumeration is not scalable.
    """
    incidence = control["incidence"]
    acceptance = {x: Fraction(1, incidence[x]) for x in control["alphabet"]}
    assert all(0 < probability <= 1 for probability in acceptance.values())
    accepted_mass = {x: probability * acceptance[x]
                     for x, probability in control["point_law"].items()}
    assert set(accepted_mass.values()) == {Fraction(1, 48)}
    success = sum(accepted_mass.values(), Fraction(0))
    assert success == Fraction(1, 3)
    conditional = {x: mass / success for x, mass in accepted_mass.items()}
    uniform = {x: Fraction(1, 16) for x in control["alphabet"]}
    assert conditional == uniform and _tv(conditional, uniform) == 0
    with_abort = dict(accepted_mass, ABORT=1 - success)
    assert with_abort["ABORT"] == Fraction(2, 3)
    assert _tv(with_abort, uniform) == Fraction(2, 3)

    accepted_flat_law = {
        plane: mass * sum((acceptance[x] / len(plane) for x in plane), Fraction(0)) / success
        for plane, mass in control["flat_law"].items()
    }
    assert sum(accepted_flat_law.values()) == 1
    assert accepted_flat_law != control["flat_law"]
    assert len({acceptance[x] for x in EXPECTED_PLANES[0]}) > 1
