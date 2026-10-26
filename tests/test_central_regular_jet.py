"""Source/covariance falsifiers for central-only Fourier, not HSP benchmarks."""
from fractions import Fraction
from itertools import product
from math import prod, sqrt
import random

import numpy as np
import pytest

from theorems.affine_phase_erasure import monomials
from theorems.central_regular_jet import (
    compile_regular_scalar_packet, regular_jet_maps, regular_rank_schedule,
    regular_weyl_map, scalar_features,
)
from theorems.nonlinear_jet_erasure import TaylorJetChart, weighted_degree
from theorems.ut5_matrix_phase_alignment import (
    _product, _rank, align_jet_maps, symplectic_pair, verify_alignment,
)


def _mv(matrix, vector, p):
    return [sum(a*b for a, b in zip(row, vector)) % p for row in matrix]


def _forms(p, w):
    result = []
    for i in range(w):
        for j in range(i+1, w):
            form = [[0]*w for _ in range(w)]
            form[i][j], form[j][i] = 1, p-1
            result.append(form)
    return result


@pytest.mark.parametrize("p", [3, 7, 2**127-1])
def test_injective_regular_weyl_map_including_zero_labels_and_singular_forms(p):
    forms = _forms(p, 3)
    for label in ((0,0,0),(1,0,0),(1,2 % p,p-1)):
        D = regular_weyl_map(p, forms, label)
        assert _rank(D, p) == 3
        assert D[:3] == ((1,0,0),(0,1,0),(0,0,1))
        columns = list(zip(*D))
        for i, j in product(range(3), repeat=2):
            expected = sum(a*form[i][j] for a, form in zip(label, forms)) % p
            assert symplectic_pair(columns[i], columns[j], p) == expected
    # A common radical is legal for this representation interface.
    assert _rank(regular_weyl_map(p, [[[0]*3 for _ in range(3)]], [1]), p) == 3


def test_actual_group_cosets_and_complete_central_only_transform():
    p, omega = 3, np.exp(2j*np.pi/3)
    half = pow(2, -1, p)
    vectors, normal, quotient = [list(product(range(p), repeat=n)) for n in (2,3,2)]
    vi, ni, qi = [{x:i for i,x in enumerate(items)} for items in (vectors,normal,quotient)]
    order, width, carrier = len(normal), len(quotient), len(vectors)
    def beta(a,b):
        return (a[0]*b[1]-a[1]*b[0]) % p
    def multiply(a,b):
        return ((a[0]+b[0]) % p, (a[1]+b[1]) % p,
                (a[2]+b[2]+half*beta(a,b)) % p)
    def potential(u):
        return (u % p, 2*u % p, u % p)
    def gauge(lam, g, sign=1):
        out = np.zeros((carrier,carrier), dtype=complex)
        for t in vectors:
            r = tuple((a+b) % p for a,b in zip(t,g))
            out[vi[r],vi[t]] = omega**((lam*(g[2]+sign*half*beta(g,t))) % p)
        return out

    # G=N x F_p^2; H={(potential(u),(u,0))}. Actual right-coset source.
    density = np.zeros((width*order,width*order), dtype=complex)
    for q,n,u in product(quotient,normal,range(p)):
        assert multiply(potential(q[0]),potential(u)) == potential(q[0]+u)
        r = ((q[0]+u) % p,q[1])
        density[qi[q]*order+ni[n],qi[r]*order+ni[multiply(n,potential(u))]] += 1/(width*order)
    transform, wrong_negation = [np.zeros((order,order),dtype=complex) for _ in range(2)]
    for lam,n in product(range(p),normal):
        t = tuple(-a % p for a in n[:2])
        transform[lam*carrier+vi[t],ni[n]] = omega**(-lam*n[2])/sqrt(p)
        wrong_negation[lam*carrier+vi[n[:2]],ni[n]] = omega**(-lam*n[2])/sqrt(p)
    np.testing.assert_allclose(transform.conj().T @ transform,np.eye(order),atol=2e-13)
    total = np.kron(np.eye(width),transform)
    wrong_total = np.kron(np.eye(width),wrong_negation)
    actual = total @ density @ total.conj().T
    wrong = wrong_total @ density @ wrong_total.conj().T
    probability = 0
    for lam in range(p):
        addresses = [q*order+lam*carrier+t for q,t in product(range(width),range(carrier))]
        block = actual[np.ix_(addresses,addresses)]
        assert np.trace(block) == pytest.approx(1/p)
        gauges = [gauge(lam,potential(q[0])) for q in quotient]
        expected = np.block([[a.conj().T@b if q[1] == r[1] else np.zeros((carrier,carrier))
                              for r,b in zip(quotient,gauges)] for q,a in zip(quotient,gauges)])/(width*carrier)
        np.testing.assert_allclose(p*block,expected,atol=2e-13)
        assert np.linalg.norm(p*wrong[np.ix_(addresses,addresses)]-expected) > 0.05
        # Discarding the retained regular carrier loses this proper hidden line.
        reduced = np.array([[np.trace(expected[a*carrier:(a+1)*carrier,b*carrier:(b+1)*carrier])
                             for b in range(width)] for a in range(width)])
        np.testing.assert_allclose(reduced,np.eye(width)/width,atol=2e-13)
        probability += np.trace(block).real
    assert probability == pytest.approx(1)
    assert carrier**2/order > 1  # The irreducible-sector normalization is invalid here.
    a,b = (1,0,0),(0,1,0)
    np.testing.assert_allclose(gauge(1,a)@gauge(1,b),gauge(1,multiply(a,b)),atol=2e-13)
    assert np.linalg.norm(gauge(1,a,-1)@gauge(1,b,-1)-gauge(1,multiply(a,b),-1)) > 1


def _design(chart, nonzero):
    """Independent test witness, not a claimed generic SDE solver."""
    p = chart.p
    rows, points = [], []
    for s,y in product(range(1,chart.degree+1),product(range(chart.degree),repeat=chart.quotient_width)):
        row = scalar_features(chart,s,y)
        if _rank(rows+[row],p) > len(rows):
            rows.append(row)
            points.append((s,y))
    assert len(rows) == 1+chart.jet_width//chart.noncentral_width
    labels,scales,outcomes = [],[],[]
    z = len(_forms(p,chart.noncentral_width))
    for s,y in points:
        if nonzero:
            labels += [(1,)+(0,)*(z-1),(p-1,)+(0,)*(z-1)]
            scales += [s,s]
            outcomes += [y,y]
        else:
            labels.append((0,)*z)
            scales.append(s)
            outcomes.append(y)
    return labels,scales,outcomes


@pytest.mark.parametrize("p,nonzero", [(7,False),(7,True),(2**127-1,True)])
def test_same_cubic_jet_alignment_and_symbolic_phase_without_irrep_data(p,nonzero):
    chart,rng = TaylorJetChart(p,1,2,3),random.Random(514)
    forms = _forms(p,2)
    labels,scales,outcomes = _design(chart,nonzero)
    maps = regular_jet_maps(chart,forms,labels,scales,outcomes)
    assert maps.carrier_width == len(scales)*2 >= 2+chart.jet_width
    alignment = align_jet_maps(maps)
    assert verify_alignment(alignment)
    R = maps.carrier_width
    spectator = [rng.randrange(p) for _ in range(R-chart.jet_width)]
    packet = compile_regular_scalar_packet(alignment,forms,labels,scales,outcomes,spectator,5)
    assert weighted_degree(chart,packet) <= 5
    theta = [rng.randrange(p) for _ in packet.parameter_basis]
    coefficients = dict(zip(packet.parameter_basis,theta))
    def potential(q,a):
        return sum(value*pow(q,nu[0],p) for (b,nu),value in coefficients.items() if a == b) % p
    for q in (0,1,3,p-1):
        raw,psi = [0]*(2*R),0
        for block,(lam,s,y,D) in enumerate(zip(labels,scales,outcomes,maps.weyl_maps)):
            x = (y[0]+s*q) % p
            displacement = _mv(D,[potential(x,0),potential(x,1)],p)
            raw[2*block:2*block+2] = displacement[:2]
            raw[R+2*block:R+2*block+2] = displacement[2:]
            psi += lam[0]*potential(x,2)
        transformed = _mv(alignment.symplectic,raw,p)
        t = [rng.randrange(p) for _ in chart.indices]
        expected = (-psi-pow(2,-1,p)*sum(a*b for a,b in zip(transformed[:R],transformed[R:]))
                    -sum(a*b for a,b in zip(transformed[R:],t+spectator))) % p
        assert packet.evaluate_fixture([q]+t,theta) == expected
    bad = [list(label) for label in labels]
    bad[0][0] = (bad[0][0]+1) % p
    with pytest.raises(ValueError,match="degree-2D"):
        regular_jet_maps(chart,forms,bad,scales,outcomes)


def test_rank_bound_is_width_and_label_independent_and_features_are_full_monomials():
    for p,D,m in ((7,3,1),(11,4,2),(2**127-1,3,1)):
        counts = []
        for w in (1,3,7):
            chart = TaylorJetChart(p,m,w,D)
            count,bound = regular_rank_schedule(chart)
            counts.append((count,bound))
            assert bound <= Fraction(1,4*p)
            powers = {(D-1,)+(0,)*m} | {(k-1,)+alpha for alpha,k,a in chart.indices if a == 0}
            assert powers == set(monomials(m+1,D-1))
        assert counts[0] == counts[1] == counts[2]
    # Exact single-polynomial check, not a finite-frequency asymptotic claim.
    p = 5
    for a,b,c in product(range(p),repeat=3):
        if a or b or c:
            zeros = sum((a*s+b+c*y) % p == 0 for s,y in product(range(1,p),range(p)))
            assert Fraction(zeros,p*(p-1)) <= Fraction(1,p-1)


def test_central_characters_outside_the_commutator_need_not_cancel():
    chart = TaylorJetChart(7,1,2,3)
    forms = _forms(7,2)+[[[0,0],[0,0]]]
    _,scales,outcomes = _design(chart,False)
    labels = [(0,1)]*len(scales)
    assert sum(pow(s,6,7) for s in scales) % 7 != 0
    maps = regular_jet_maps(chart,forms,labels,scales,outcomes)
    alignment = align_jet_maps(maps)
    packet = compile_regular_scalar_packet(alignment,forms,labels,scales,outcomes,
                                           [0]*(maps.carrier_width-chart.jet_width),5)
    assert weighted_degree(chart,packet) == 5  # Uncancelled central phase is paid later.


def test_bad_public_features_zero_scales_and_invalid_forms_rejected():
    chart = TaylorJetChart(7,1,2,3)
    forms = _forms(7,2)
    # Nonzero labels and a valid relation do not repair tied-scale features.
    labels = [(1,),(6,)]*7
    with pytest.raises(ValueError,match="feature design"):
        regular_jet_maps(chart,forms,labels,[1]*14,[(y,) for y in range(7) for _ in range(2)])
    labels,scales,outcomes = _design(chart,False)
    original = regular_jet_maps(chart,forms,labels,scales,outcomes)
    extended = regular_jet_maps(chart,forms,labels+[(5,)],scales+[0],outcomes+[(2,)])
    assert original == extended
    with pytest.raises(ValueError,match="degree-2D"):
        regular_jet_maps(chart,forms,labels,[0]*len(scales),outcomes)
    with pytest.raises(ValueError,match="alternating"):
        regular_weyl_map(7,[[[1,0],[0,0]]],[1])
    with pytest.raises(ValueError,match="canonical"):
        regular_weyl_map(7,forms,[-1])


def test_class_three_derived_group_has_nonscalar_commutator_beyond_weyl_scope():
    # In UT_7, these elements lie in G'. Their nested commutator is nonzero.
    p,n = 2**127-1,7
    I = [[int(i == j) for j in range(n)] for i in range(n)]
    def root(i,j,sign=1):
        A = [row[:] for row in I]
        A[i][j] = sign % p
        return A
    def commutator(A,B,Ainv,Binv):
        return _product(_product(_product(A,B,p),Ainv,p),Binv,p)
    C = commutator(root(0,2),root(2,4),root(0,2,-1),root(2,4,-1))
    assert C == root(0,4)
    nested = commutator(C,root(4,6),root(0,4,-1),root(4,6,-1))
    assert nested == root(0,6) and nested != I
    # Thus C is not central in G': its coset still translates N/Z(N).
    # A Weyl family has scalar commutators, so the unchanged interface fails.
