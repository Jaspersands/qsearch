import itertools

import pytest
import sympy as sp

from native_rlwe_ideal_class_orbits import (
    class_orbit, finite_classes, generic_source_member, ring_inverse,
    rotate, run_controls, source_class_count,
)
from native_rlwe_quaternion_kernel import conjugate, kernel_member, mul, quaternion_multiply


def test_dihedral_relations_and_exact_classical_canonicalization():
    m,q = (1,1,0,0),3
    assert generic_source_member(m,q)
    R = lambda a: rotate(a,2,q)
    T = lambda a: tuple(-v % q for v in ring_inverse(a,q))
    assert T(T(m))==m
    assert T(R(T(m)))==rotate(m,2*(len(m)-1),q)
    assert rotate(m,2*len(m),q)==m
    row = class_orbit(m,q)
    assert row["orbit_size"]==8
    canonical = row["canonical_class_label"]
    for member in row["all_orbit_ratios"]:
        other = class_orbit(member,q)
        assert other["canonical_class_label"]==canonical
        assert other["all_orbit_ratios"]==row["all_orbit_ratios"]


def test_explicit_quaternion_units_transport_every_kernel_basis_column_isometrically():
    m,q = (1,1,0,0),3
    d = len(m)
    zero,one = (0,)*d,(1,)+(0,)*(d-1)
    for k in range(d):
        u = rotate(one,k,q)
        u = tuple(v if v<=q//2 else v-q for v in u)
        for kind,unit in (("rotation",(u,zero)),("reflection",(zero,conjugate(u)))):
            target = rotate(m,2*k,q) if kind=="rotation" else rotate(tuple(-v % q for v in ring_inverse(m,q)),2*k,q)
            for i in range(d):
                e = tuple(int(j==i) for j in range(d))
                for pair in ((tuple(q*v for v in e),zero),(mul(m,e),e)):
                    out = quaternion_multiply(pair,unit,one)
                    assert kernel_member(out,target,q)
                    assert sum(v*v for a in out for v in a)==sum(v*v for a in pair for v in a)


def test_central_unit_equivalence_adds_no_new_public_orbit():
    m,q = (1,1,0,0),3
    central = (1,1,0,-1)
    assert conjugate(central)==central
    assert mul(central,(-1,1,0,-1))==(1,0,0,0)
    pair = (m,(1,0,0,0))
    out = quaternion_multiply(pair,(central,(0,0,0,0)),(1,0,0,0))
    assert kernel_member(out,m,q)
    assert sum(v*v for a in out for v in a)!=sum(v*v for a in pair for v in a)
    # It permutes the SAME integer lattice; it is not a new class or global
    # geometry even though this particular vector's physical length changes.
    assert class_orbit(m,q)["classmates_have_an_explicit_signed_isometric_transport"]


def test_exact_source_class_count_and_only_two_short_orbits():
    row = finite_classes(4,3)
    assert row["generic_ratio_count"]==56
    assert row["exact_native_class_count"]==8
    assert row["orbit_size_histogram"]=={"4":2,"8":6}
    monomials = set()
    for i in range(4):
        for sign in (1,2):
            m = tuple(sign if j==i else 0 for j in range(4))
            monomials.add(m)
            assert class_orbit(m,3)["orbit_size"]==4
    for m in itertools.product(range(3),repeat=4):
        if generic_source_member(m,3):
            assert (class_orbit(m,3)["orbit_size"]==4)==(m in monomials)


def test_saved_native_classes_keep_shortness_and_source_scope_debts():
    report = run_controls()
    assert report["complete_finite_source_orbits"][1]["exact_native_class_count"]==396
    native = report["same_saved_native_d64_kernel"]
    assert native["orbit_size"]==128
    assert len(native["distinct_orbit_ratio_sha256"])==128
    assert native["class_label_is_not_a_hidden_oracle"]
    assert not native["new_short_relation_or_completion_supplied"]
    assert not report["mechanism"]["general_nonprincipal_short_element_or_transport_algorithms_ruled_out"]
    assert not report["claim_gate"]["speedup_claim_allowed"]
    assert not report["claim_gate"]["independent_review"]


@pytest.mark.parametrize("d,q", [(2,3),(3,3),(4,17),(4,27),(True,3)])
def test_unmatched_or_composite_source_regimes_rejected(d,q):
    with pytest.raises(ValueError):
        source_class_count(d,q)


def test_nonunit_and_beta_zero_ratios_are_not_promoted_to_generic_classes():
    with pytest.raises(ValueError):
        class_orbit((0,0,0,0),3)
    # Norm=-1 in the d4 field pair, so ambient saturation is not the full O_0.
    exceptional = next(m for m in itertools.product(range(3),repeat=4)
                       if tuple(v % 3 for v in mul(m,conjugate(m)))==(2,0,0,0))
    with pytest.raises(ValueError):
        class_orbit(exceptional,3)
    with pytest.raises(ValueError):
        ring_inverse((0,0,0,0),3)
