from math import gcd

import pytest
from sympy import Matrix, eye

from source_field_controls import (auxiliary_field_plan, conjugate_curve_control,
                                   embedding_key37, field37, unsafe_galois_key37)


def test_actual_supersingular_conjugates_are_not_geometrically_isomorphic():
    record = conjugate_curve_control()
    assert record["curve"] == {"a": (11, 36), "b": (32, 24), "j": (3, 1), "points": 1444}
    assert record["conjugate_curve"] == {"a": (11, 1), "b": (32, 13), "j": (3, 36), "points": 1444}
    assert all(record["checks"].values())
    assert record["p_frobenius_self_isomorphism_exists"] is False
    assert record["ppav_geometric_label_generator_executed"] is False


def test_a_field_isomorphism_requires_transport_not_galois_minimization():
    field = field37()
    u = field.generator
    # A second presentation uses v=-u. The SAME j is 3-v, not 3+v.
    v_in_fixed_field = -u
    assert embedding_key37(field(3)-v_in_fixed_field) == embedding_key37(field(3)+u)
    assert embedding_key37(field(3)+v_in_fixed_field) != embedding_key37(field(3)+u)
    assert unsafe_galois_key37(field(3)+v_in_fixed_field) == unsafe_galois_key37(field(3)+u)


@pytest.mark.parametrize("p,m,sign", [(5, 1, 1), (7, 2, -1), (37, 1, -1), (101, 17, 1)])
def test_uniform_separate_field_bounds(p, m, sign):
    levels = tuple((r, e) for r in (2, 3, 5, 7, 11, 13) if r != p for e in (1, 2))
    result = auxiliary_field_plan(p, m, sign, levels)
    assert result["fixed_base_degree"] == 4*m
    assert result["fixed_scalar_mod_8"] == 1
    assert result["max_point_field_degree"] <= 4*m*13*12
    assert result["common_field_and_scalar_promises_verified"] is False
    for row in result["auxiliary_fields"]:
        n, degree = row["torsion_order"], row["extension_degree_over_fixed_base"]
        assert gcd(p, n) == 1
        assert pow(p, 2*m*degree, n) == 1


@pytest.mark.parametrize("arguments", [
    (2, 1, 1, ((3, 2),)), (9, 1, 1, ((5, 2),)),
    (37, 0, 1, ((3, 2),)), (37, 1, 0, ((3, 2),)),
    (37, 1, 1, ((37, 2),)), (37, 1, 1, ((3, 3),)),
    (37, 1, 1, ((3, 2), (3, 2))), (37, 1, 1, ()),
])
def test_invalid_source_field_plans_rejected(arguments):
    with pytest.raises(ValueError):
        auxiliary_field_plan(*arguments)


@pytest.mark.parametrize("ell", [3, 5, 7, 11])
def test_source_wrapped_frobenius_cannot_supply_a_mixing_endomorphism(ell):
    # Local Tate-module controls only. The geometric proof is naturality;
    # arbitrary displayed similitudes are NOT claimed to be curve Frobenius.
    j = Matrix([[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, 1], [0, 0, -1, 0]])
    phi = Matrix.diag(ell, 1, ell, 1)
    adjoint = -j*phi.T*j
    ta = Matrix.diag(37, 1, 37, 1)
    shear = Matrix([[1, 2, 0, 0], [0, 1, 0, 0], [0, 0, 1, 3], [0, 0, 0, 1]])
    tb = ta*shear
    phi_p = tb*phi*ta.inv_mod(ell) % ell
    adjoint_p = -j*phi_p.T*j % ell
    assert ta.T*j*ta == 37*j and tb.T*j*tb == 37*j
    assert (adjoint_p*tb-ta*adjoint) % ell == Matrix.zeros(4)
    assert phi*adjoint == ell*eye(4)
    for index in range(16):
        rho = Matrix.zeros(4)
        rho[index//4, index % 4] = 1
        wrapped = phi*rho*adjoint_p*tb % ell
        transported = phi*(rho*ta)*adjoint % ell
        assert wrapped == transported
        assert wrapped*phi % ell == Matrix.zeros(4)
