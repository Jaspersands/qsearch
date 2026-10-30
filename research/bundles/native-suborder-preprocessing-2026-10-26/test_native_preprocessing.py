from pathlib import Path
from random import Random
import sys

import pytest
from flint import fq_default_ctx
from sympy import Matrix, eye, nextprime, zeros

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "source-algebra-splitting-2026-10-25"))
sys.path.insert(0, str(ROOT / "elliptic-theta-input-2026-10-26"))
from native_preprocessing import (
    check_dictionary, check_order, clear_denominators, dictionary_from_bimodule,
    recover_order, reference_half_frobenius,
)
from elliptic_theta import EllipticCurve, point_key
from kernel_output import QuaternionOrder, action, odd_maximal_order
from source_split import source_split


def changed_order(order, change):
    inverse = change.inv()
    return QuaternionOrder(
        tuple(tuple(inverse*order.multiply(change[:, i], change[:, j]) for j in range(4))
              for i in range(4)), inverse*order.unit,
        inverse*order.involution*change, order.traces*change,
    )


def fixture(level=6, p=11):
    source = odd_maximal_order(p)
    shear = Matrix([[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 2], [0, 0, 0, 1]])
    change = Matrix.diag(1, level, level, level)*shear
    return source, changed_order(source, change), change


def transcripts_for(source, change, bound, p=11):
    transcripts, modulus, prime = [], 1, 2
    while modulus <= 4*bound**2:
        prime = int(nextprime(prime))
        if prime == p:
            continue
        actions, _ = source_split(source, prime, [(prime, 1)], p, Random(prime))
        transcripts.append((prime, tuple(action(change[:, i], actions) for i in range(4))))
        modulus *= prime
    return transcripts


def degree_bound(order):
    return max(int((order.traces*order.multiply(eye(4)[:, i], order.star(eye(4)[:, i])))[0]/2)
               for i in range(4))


@pytest.mark.parametrize("level", [1, 6, 101])
def test_reconstruct_order_without_supplied_multiplication_or_dual_maps(level):
    source, target, change = fixture(level)
    bound = degree_bound(target)
    reconstructed = recover_order(transcripts_for(source, change, bound), bound, 11)
    assert reconstructed.products == target.products
    assert reconstructed.unit == target.unit
    assert reconstructed.traces == target.traces
    assert reconstructed.involution == target.involution


def test_reconstruct_basis_without_identity_in_first_position():
    source, _, change = fixture()
    change.col_swap(0, 2)
    target = changed_order(source, change)
    bound = degree_bound(target)
    reconstructed = recover_order(transcripts_for(source, change, bound), bound, 11)
    assert reconstructed.unit == Matrix([0, 0, 1, 0])
    assert reconstructed.products == target.products


def test_insufficient_crt_precision_is_rejected():
    source, target, change = fixture()
    bound = degree_bound(target)
    transcript = transcripts_for(source, change, bound)
    with pytest.raises(ValueError, match="insufficient CRT"):
        recover_order(transcript[:1], bound, 11)


@pytest.mark.parametrize("bad_prime", [11, 9, 3])
def test_bad_or_duplicate_torsion_level_rejected(bad_prime):
    source, target, change = fixture()
    bound = degree_bound(target)
    transcript = transcripts_for(source, change, bound)
    transcript.append((bad_prime, transcript[0][1]))
    with pytest.raises(ValueError, match="distinct prime-to-characteristic"):
        recover_order(transcript, bound, 11)


def test_rank_two_algebra_does_not_become_full_rank_input():
    source, target, change = fixture()
    bound = degree_bound(target)
    transcript = transcripts_for(source, change, bound)
    transcript = [(p, (a[0], a[1], a[0], a[1])) for p, a in transcript]
    with pytest.raises(ValueError, match="rank-four"):
        recover_order(transcript, bound, 11)


def test_corrupt_torsion_transcript_is_rejected():
    source, target, change = fixture()
    bound = degree_bound(target)
    transcript = transcripts_for(source, change, bound)
    p, a = transcript[-1]
    corrupted = list(a)
    corrupted[1] = corrupted[1]+eye(2)
    transcript[-1] = (p, tuple(corrupted))
    with pytest.raises(ValueError):
        recover_order(transcript, bound, 11)


def test_underdeclared_degree_bound_is_rejected():
    source, target, change = fixture()
    bound = degree_bound(target)
    with pytest.raises(ValueError):
        recover_order(transcripts_for(source, change, bound), 1, 11)


def bimodule_fixture():
    source, target, change = fixture(30)
    basis = [eye(4)[:, i] for i in range(4)]
    conjugator = Matrix([2, 1, 1, 0])
    norm = (source.traces*source.multiply(conjugator, source.star(conjugator)))[0]/2
    inverse = source.star(conjugator)/norm
    conjugation = Matrix.hstack(*(source.multiply(source.multiply(conjugator, x), inverse)
                                  for x in basis))
    dictionary = change.inv()*conjugation
    left = tuple(Matrix.hstack(*(source.multiply(a, x) for x in basis)) for a in basis)
    right = tuple(Matrix.hstack(*(source.multiply(x, dictionary.inv()[:, j]) for x in basis))
                  for j in range(4))
    return source, target, dictionary, left, right


@pytest.mark.parametrize("vector", [Matrix([1, 0, 0, 0]), Matrix([0, 1, 0, 0]),
                                    Matrix([2, -3, 1, 7])])
def test_extract_dictionary_from_supplied_split_tensor_module(vector):
    source, target, original, left, right = bimodule_fixture()
    recovered = dictionary_from_bimodule(source, target, left, right, vector)
    check_dictionary(source, target, recovered)
    if vector == source.unit:
        assert recovered == original
    denominator, coordinates = clear_denominators(source, target, recovered)
    assert denominator > 1
    assert coordinates == denominator*recovered
    assert all(x.q == 1 for x in coordinates)


def test_changed_tensor_module_coordinates_preserve_dictionary():
    source, target, original, left, right = bimodule_fixture()
    frame = Matrix([[1, 2, 0, 0], [0, 1, 3, 0], [0, 0, 1, 4], [0, 0, 0, 1]])
    left = tuple(frame*a*frame.inv() for a in left)
    right = tuple(frame*a*frame.inv() for a in right)
    assert dictionary_from_bimodule(source, target, left, right, frame*source.unit) == original


def test_regular_representation_instead_of_opposite_is_rejected():
    source, target, _, left, _ = bimodule_fixture()
    basis = [eye(4)[:, i] for i in range(4)]
    wrong_right = tuple(Matrix.hstack(*(target.multiply(b, x) for x in basis)) for b in basis)
    with pytest.raises(ValueError, match="opposite|commute"):
        dictionary_from_bimodule(source, target, left, wrong_right, source.unit)


def test_zero_module_vector_rejected():
    source, target, _, left, right = bimodule_fixture()
    with pytest.raises(ValueError, match="nonzero"):
        dictionary_from_bimodule(source, target, left, right, zeros(4, 1))


def test_arbitrary_vector_space_identification_is_not_an_algebra_dictionary():
    source, target, _, _, _ = bimodule_fixture()
    with pytest.raises(ValueError, match="multiplication"):
        clear_denominators(source, target, eye(4))


@pytest.mark.parametrize("p", [7, 23, 31])
def test_reference_maximal_order_on_actual_elliptic_four_torsion(p):
    field = fq_default_ctx(p, 2, "z")
    curve = EllipticCurve(field, -1, 0)
    points, _ = curve.torsion_eight()
    halves = {}
    for half in points:
        point = curve.multiply(2, half)
        halves.setdefault(point_key(point), (point, []))[1].append(half)
    assert len(halves) == 16
    root = field(-1).sqrt()

    def i_map(point):
        return None if point is None else (-point[0], root*point[1])

    def h_map(point):
        lifts = halves[point_key(point)][1]
        values = [reference_half_frobenius(curve, point, half) for half in lifts]
        assert len(lifts) == 4 and all(value == values[0] for value in values)
        return values[0]

    maps = (lambda p: p, i_map, h_map, lambda p: i_map(h_map(p)))
    order = odd_maximal_order(p)
    assert check_order(order).det() == p*p
    for point, _ in halves.values():
        assert curve.add(curve.add(h_map(h_map(point)), curve.neg(h_map(point))),
                         curve.multiply((p+1)//4, point)) is None
        for a in range(4):
            for b in range(4):
                expected = None
                for coefficient, f in zip(order.products[a][b], maps):
                    expected = curve.add(expected, curve.multiply(int(coefficient), f(point)))
                assert maps[a](maps[b](point)) == expected


def test_same_j_does_not_justify_the_same_half_frobenius_basis():
    field = fq_default_ctx(7, 2, "z")
    wrong_curve = EllipticCurve(field, 1, 0)
    z = field(-1).sqrt()
    point = (z, field(0))
    frobenius = (z**7, field(0))
    assert wrong_curve.contains(point) and wrong_curve.multiply(2, point) is None
    assert wrong_curve.add(point, frobenius) is not None
    with pytest.raises(ValueError, match="reference model"):
        reference_half_frobenius(wrong_curve, None, None)


def test_invalid_half_rejected():
    curve = EllipticCurve(fq_default_ctx(7, 2, "z"), -1, 0)
    point = (curve.field(0), curve.field(0))
    with pytest.raises(ValueError, match="valid half"):
        reference_half_frobenius(curve, point, None)


@pytest.mark.parametrize("p", [7, 11, 23])
def test_small_cm_commutation_bound_needs_the_characteristic_inequality(p):
    order = odd_maximal_order(p)
    x, y = Matrix([0, 0, 0, 1]), Matrix([0, -1, 0, 1])
    assert (order.traces*x)[0] == (order.traces*y)[0] == 0
    norm = (p+1)//4
    assert order.multiply(x, x) == order.multiply(y, y) == -norm*order.unit
    xy, yx = order.multiply(x, y), order.multiply(y, x)
    trace = int((order.traces*xy)[0])
    assert xy != yx and xy+yx == trace*order.unit
    change = Matrix.hstack(order.unit, x, y, xy)
    generated_order = changed_order(order, change)
    gram = check_order(generated_order)
    assert gram.det() == (4*norm**2-trace**2)**2 == p*p
    assert 0 < p <= 4*norm**2
