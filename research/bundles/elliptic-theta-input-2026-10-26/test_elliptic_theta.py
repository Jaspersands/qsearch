from pathlib import Path
import sys

import pytest
from flint import fq_default_ctx, fq_default_poly_ctx

sys.path.insert(0, str(Path(__file__).resolve().parent))
from elliptic_theta import (
    EllipticCurve, apply, convert, identity, inverse, key, matmul, nullspace,
    point_key, projective, translation_matrix, verify_translation,
)


@pytest.fixture(scope="module", params=[(7, 1, 0), (23, 1, 2), (31, 1, 0)])
def converted(request):
    p, a, b = request.param
    return convert(EllipticCurve(fq_default_ctx(p, 2, "z"), a, b))


def test_actual_constant_torsion_and_signed_roundtrips(converted):
    model = converted
    assert model.resources == {"polynomial_root_calls": 46, "maximum_polynomial_degree": 4,
                               "field_elements_enumerated": False, "torsion_points": 64,
                               "normalization_root_calls": 2, "symbolic_translation_checks": 2,
                               "level": 4, "signed_points_preserved": True}
    encodings = {tuple(key(x) for x in model.encode(p)) for p in model.torsion}
    assert len(encodings) == 64
    for point in model.torsion:
        assert model.decode(model.encode(point)) == point
        if model.curve.multiply(2, point) is not None:
            assert model.encode(point) != model.encode(model.curve.neg(point))


def test_full_signed_heisenberg_and_reflection(converted):
    t = converted
    for point in t.torsion:
        value = t.encode(point)
        assert projective(tuple(t.root_unity**j*value[j] for j in range(4))) == t.encode(
            t.curve.add(point, t.first))
        assert projective((value[3], value[0], value[1], value[2])) == t.encode(
            t.curve.add(point, t.second))
        assert projective((value[0], value[3], value[2], value[1])) == t.encode(t.curve.neg(point))


def test_symbolic_translation_and_corruption(converted):
    t = converted
    matrix = translation_matrix(t.curve, t.first, t.torsion)
    assert verify_translation(t.curve, t.first, matrix)
    matrix[0][0] += t.curve.field.one()
    assert not verify_translation(t.curve, t.first, matrix)


def test_non_torsion_interpolation_points_roundtrip(converted):
    t = converted
    f = t.curve.field
    checked = 0
    outside = 0
    torsion_keys = {point_key(p) for p in t.torsion}
    for i in range(20):
        x = f(i)+f.gen()
        value = x**3+t.curve.a*x+t.curve.b
        if not value.is_square():
            continue
        point = x, value.sqrt()
        assert t.decode(t.encode(point)) == point
        outside += point_key(point) not in torsion_keys
        checked += 1
    assert checked
    if int(f.characteristic()) != 7:
        assert outside


def test_theta_null_relation_and_curve_equations(converted):
    null = converted.encode(None)
    a, b, c, d = null
    assert b == d and 2*b**4 == a*c*(a*a+c*c)
    assert b != 0 and a*a+c*c != 0
    for point in converted.torsion:
        v = converted.encode(point)
        assert b*b*(v[0]**2+v[2]**2) == (a*a+c*c)*v[1]*v[3]
        assert b*b*(v[1]**2+v[3]**2) == (a*a+c*c)*v[0]*v[2]


def test_kummer_shortcut_loses_signed_input(converted):
    curve = converted.curve
    point = converted.first
    negative = curve.neg(point)
    assert point[0] == negative[0]
    assert converted.encode(point) != converted.encode(negative)
    original = (converted.first, converted.second)
    changed = (converted.first, curve.neg(converted.second))
    assert tuple(p[0] for p in original) == tuple(p[0] for p in changed)
    assert all(tuple(curve.multiply(u, p) for p in original) != changed for u in (1, 3))


def test_supersingular_native_controls_include_generic_j(converted):
    curve = converted.curve
    p = int(curve.field.characteristic())
    x = fq_default_poly_ctx(curve.field).gen()
    assert ((x**3+curve.a*x+curve.b)**((p-1)//2))[p-1] == 0
    if p == 23:
        j = 1728*4*curve.a**3/(4*curve.a**3+27*curve.b**2)
        assert j != 0 and j != curve.field(1728)


def test_invalid_geometry_and_field_are_rejected():
    with pytest.raises(ValueError, match="singular"):
        EllipticCurve(fq_default_ctx(7, 2), 0, 0)
    with pytest.raises(ValueError, match="8-torsion|2-torsion"):
        convert(EllipticCurve(fq_default_ctx(7, 1), 1, 0))


def test_zero_field_elements_do_not_use_python_truthiness():
    f = fq_default_ctx(7, 2)
    # fq_default(0) has truth value True in this installed FLINT binding.
    assert projective((f(0), f(0), f(3), f(0))) == (f(0), f(0), f(1), f(0))
    assert nullspace([[f(0), f(1)], [f(0), f(0)]]) == [[f(1), f(0)]]
    with pytest.raises(ValueError, match="zero projective"):
        projective((f(0),)*4)
    with pytest.raises(ValueError, match="singular"):
        inverse([[f(0), f(0)], [f(0), f(1)]])


def test_decoder_rejects_invalid_model_point(converted):
    f = converted.curve.field
    bad = apply(converted.coordinates, (f(1), f(0), f(1), f(1)))
    with pytest.raises(ValueError):
        converted.decode(bad)
