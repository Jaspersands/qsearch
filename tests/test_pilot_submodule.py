"""Exact subgroup/certificate controls, including invisible ambient mod-p rank."""
from dataclasses import replace
from itertools import product
from math import prod
import random

import pytest
from flint import fmpq_mat, fmpz_mat

from theorems.pilot_submodule import compile_pilot_frame, verify_pilot_frame


def subgroup_closure(generators, moduli):
    zero = (0,)*len(moduli)
    found,queue = {zero},[zero]
    while queue:
        x = queue.pop()
        for g in generators:
            y = tuple((a+b)%m for a,b,m in zip(x,g,moduli))
            if y not in found:
                found.add(y)
                queue.append(y)
    return found


def check_against_enumeration(p,es,generators):
    moduli = tuple(p**e for e in es)
    expected = subgroup_closure(generators,moduli)
    f = compile_pilot_frame(prime=p,ambient_exponents=es,pilot_columns=generators)
    assert verify_pilot_frame(f) and prod(f.smith_orders)==len(expected)
    decoded = {f.decode(x) for x in product(*(range(p**e) for e in f.intrinsic_exponents))}
    assert decoded==expected
    for x in product(*(range(m) for m in moduli)):
        y = f.encode(x)
        assert (y is not None)==(x in expected)
        if y is not None:
            assert f.decode(y)==x
    return f


def test_p_times_cyclic_group_is_not_zero_despite_zero_ambient_mod_p_rank():
    frame = check_against_enumeration(3,(2,),[(3,)])
    assert frame.intrinsic_exponents==(1,)
    assert frame.encode((3,))==(1,) and frame.decode((2,))==(6,)
    assert frame.encode((1,)) is None
    assert not frame.certificate()["hidden_support_completeness_certified"]


def test_oblique_mixed_order_embedding_requires_left_smith_inverse_not_right():
    frame = check_against_enumeration(3,(2,3),[(3,3),(0,9)])
    assert frame.intrinsic_exponents==(2,)
    assert frame.decode((1,))==(3,3)
    assert frame.smith_left!=frame.smith_right
    with pytest.raises(ArithmeticError,match="Smith"):
        verify_pilot_frame(replace(frame,smith_left=frame.smith_right))


@pytest.mark.parametrize("p,es",[(3,(1,2)),(3,(2,2)),(3,(2,3)),(5,(1,2))])
def test_seeded_mixed_modules_match_independent_group_closure(p,es):
    rng = random.Random(20261029)
    for _ in range(8):
        generators = [tuple(rng.randrange(p**e) for e in es) for _ in range(2)]
        check_against_enumeration(p,es,generators)


def test_every_pair_of_pilots_in_c3_times_c3():
    elements = list(product(range(3),repeat=2))
    for a,b in product(elements,repeat=2):
        check_against_enumeration(3,(1,1),[a,b])


@pytest.mark.parametrize("generators",[[],[(0,0)],[(0,0)]*5])
def test_trivial_pilot_subgroup_has_empty_intrinsic_coordinates(generators):
    frame = check_against_enumeration(3,(1,2),generators)
    assert frame.intrinsic_exponents==() and frame.decode(())==(0,0)
    assert frame.encode((0,0))==() and frame.encode((0,3)) is None
    with pytest.raises(ValueError):
        frame.decode((0,))


@pytest.mark.parametrize("field",["lattice_basis","basis_from_generators","generators_from_basis",
                                  "relation_matrix","smith_left","smith_right"])
def test_certificate_mutations_rejected(field):
    frame = compile_pilot_frame(prime=3,ambient_exponents=(2,3),pilot_columns=[(3,3),(0,9)])
    rows = [list(row) for row in getattr(frame,field)]
    rows[0][0] += 1
    with pytest.raises((ArithmeticError,ValueError)):
        verify_pilot_frame(replace(frame,**{field:tuple(tuple(row) for row in rows)}))


def test_smith_orders_are_not_just_a_cardinality_certificate():
    frame = compile_pilot_frame(prime=3,ambient_exponents=(2,3),pilot_columns=[(3,3),(0,9)])
    assert frame.smith_orders==(1,9)
    with pytest.raises(ArithmeticError):
        verify_pilot_frame(replace(frame,smith_orders=(3,3)))


def test_coordinate_map_is_additive_and_scalar_compatible():
    frame = compile_pilot_frame(prime=3,ambient_exponents=(2,3),pilot_columns=[(3,3),(0,9)])
    for a,b in product(range(9),repeat=2):
        x,y = frame.decode((a,)),frame.decode((b,))
        summed = tuple((u+v)%m for u,v,m in zip(x,y,(9,27)))
        assert frame.encode(summed)==((a+b)%9,)
        scaled = tuple((b*b*u)%m for u,m in zip(x,(9,27)))
        assert frame.encode(scaled)==((b*b*a)%9,)


@pytest.mark.parametrize("es,pilots",[((3,2),[(1,4),(1,1)]),
                                     ((2,2,3),[(5,3,24),(4,4,1)])])
def test_negative_determinant_smith_transform_uses_correct_inverse(es,pilots):
    frame = check_against_enumeration(3,es,pilots)
    left = fmpz_mat(frame.smith_left)
    assert left.det()==-1
    # Do not require the dependency defect to persist: require our map to
    # implement the true inverse even if the installed backend is repaired.
    inverse = fmpq_mat(frame.lattice_basis).inv()*fmpq_mat(frame._embedding)
    product_matrix = fmpq_mat(left)*inverse
    assert product_matrix==fmpq_mat([[int(i==j) for j in range(len(es))] for i in range(len(es))])


def test_certificate_replay_does_not_need_smith_solver(monkeypatch):
    import theorems.pilot_submodule as module
    frame = compile_pilot_frame(prime=3,ambient_exponents=(2,3),pilot_columns=[(3,3),(0,9)])
    monkeypatch.setattr(module,"smith_normal_decomp",lambda *args:pytest.fail("certificate reran Smith solver"))
    assert verify_pilot_frame(frame)


def test_large_prime_exponents_require_no_module_enumeration():
    p = 2**61-1
    generators = [(p**38,p**67),(0,p**69)]
    frame = compile_pilot_frame(prime=p,ambient_exponents=(40,70),pilot_columns=generators)
    assert frame.intrinsic_exponents==(3,)
    assert frame.decode(frame.encode(generators[0]))==generators[0]
    assert frame.encode((1,0)) is None


@pytest.mark.parametrize("exponents,pilots",[((0,),[(0,)]),((2,),[(9,)]),
                                            ((2,),[(True,)]),((2,3),[(1,)])])
def test_noncanonical_inputs_rejected(exponents,pilots):
    with pytest.raises(ValueError):
        compile_pilot_frame(prime=3,ambient_exponents=exponents,pilot_columns=pilots)
