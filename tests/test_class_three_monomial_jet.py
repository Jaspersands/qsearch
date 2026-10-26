"""Adversarial identities for the class-three source, not HSP benchmarks."""
from dataclasses import replace
from fractions import Fraction
from itertools import product
from math import factorial, prod
import random

import numpy as np
import pytest

from theorems.affine_phase_erasure import monomials
from theorems.class_three_monomial_jet import (
    ClassThreeStructure, FullTaylorJetChart, align_full_jet,
    compile_full_jet_phase, full_jet_rank_schedule,
)
from theorems.nonlinear_jet_erasure import (
    _jet_terms, fourier_curve_packet, pullback_phase, weighted_degree, weighted_merge,
)
from theorems.ut5_matrix_phase_alignment import _identity, _product, _rank
from theorems.ut5_scalar_phase_compiler import SymbolicScalarPacket, _add


def _filiform(p):
    return ClassThreeStructure(p,(((0,1),(p-1,0)),),(((0,0),(0,0)),),(((1,),(0,)),))


def _ut4(p):
    # A=(E12+E13,E23,E34), B=(E13,E24), C=E14; gamma is nonzero.
    return ClassThreeStructure(p,
        (((0,1,0),(p-1,0,0),(0,0,0)),((0,0,0),(0,0,1),(0,p-1,0))),
        (((0,0,1),(0,0,0),(p-1,0,0)),),
        (((0,1),(0,0),(p-1,0)),))


def _mv(matrix,vector,p):
    return tuple(sum(a*b for a,b in zip(row,vector)) % p for row in matrix)


def _element(st,rng):
    return tuple(tuple(rng.randrange(st.p) for _ in range(n))
                 for n in (st.a_width,st.b_width,st.c_width))


def _design(chart,st):
    rows,scales,outcomes = [],[],[]
    for s,y in product(range(1,chart.degree+1),product(range(chart.degree),repeat=chart.quotient_width)):
        row = [pow(s,k,chart.p)*prod(pow(v,e,chart.p) for v,e in zip(y,alpha)) % chart.p
               for alpha,k,a in chart.indices if a == 0]
        row = list(map(int,row))
        if _rank(rows+[row],chart.p) > len(rows):
            rows.append(row)
            scales.append(s)
            outcomes.append(y)
    assert len(rows) == chart.jet_width//chart.noncentral_width
    labels = [tuple((i+j+1) % chart.p for j in range(st.c_width)) for i in range(len(rows))]
    return labels,scales,outcomes


@pytest.mark.parametrize("p",[5,11,2**127-1])
def test_bch_matches_independent_ut4_matrix_exponential(p):
    st,rng = _ut4(p),random.Random(213)
    def exp(g):
        a,b,c = g
        X = [[0,a[0],a[0]+b[0],c[0]], [0,0,a[1],b[1]],
             [0,0,0,a[2]], [0,0,0,0]]
        result,power = _identity(4),_identity(4)
        for k in range(1,4):
            power = _product(power,X,p)
            result = [[(u+pow(factorial(k),-1,p)*v) % p for u,v in zip(row,other)]
                      for row,other in zip(result,power)]
        return result
    for _ in range(40):
        g,h = _element(st,rng),_element(st,rng)
        assert exp(st.multiply_fixture(g,h)) == _product(exp(g),exp(h),p)
        inv = tuple(tuple(-x % p for x in row) for row in g)
        assert exp(st.multiply_fixture(g,inv)) == _identity(4)


def test_invalid_lie_data_and_transcripts_rejected():
    st = _ut4(11)
    with pytest.raises(ValueError,match="Jacobi"):
        replace(st,delta=(((0,1),(0,0),(0,0)),))
    with pytest.raises(ValueError,match="alternating"):
        replace(_filiform(11),beta=(((1,1),(10,0)),))
    chart = FullTaylorJetChart(11,1,3,2)
    labels,scales,ys = _design(chart,st)
    with pytest.raises(ValueError,match="rank deficient"):
        align_full_jet(chart,st,labels,[1]*len(labels),[(0,)]*len(labels))
    with pytest.raises(ValueError,match="nonzero"):
        align_full_jet(chart,st,labels,[0]+scales[1:],ys)
    with pytest.raises(ValueError,match="canonical"):
        align_full_jet(chart,st,[(11,)]+labels[1:],scales,ys)
    small,small_chart = _filiform(5),FullTaylorJetChart(5,1,2,2)
    args = _design(small_chart,small)
    small_alignment = align_full_jet(small_chart,small,*args)
    with pytest.raises(ValueError,match="p>3D"):
        compile_full_jet_phase(small_alignment,(0,)*(small_alignment.carrier_width-small_chart.jet_width),4)


def test_actual_regular_kernel_fourier_all_center_labels_and_quantum_mu():
    p,st = 5,_filiform(5)
    omega = np.exp(2j*np.pi/p)
    raw = list(product(range(p),repeat=4))
    carriers = list(product(range(p),repeat=3))
    ni,ti = {x:i for i,x in enumerate(raw)},{x:i for i,x in enumerate(carriers)}
    n,d = len(raw),len(carriers)
    transform = np.zeros((n,n),dtype=complex)
    for j,(a0,a1,b,c) in enumerate(raw):
        for lam,mu in product(range(p),repeat=2):
            t = (-a0 % p,-a1 % p,mu)
            transform[lam*d+ti[t],j] = omega**((mu*b-lam*c) % p)/p
    np.testing.assert_allclose(transform @ transform.conj().T,np.eye(n),atol=2e-13)
    h = ((1,2),(3,),(4,))
    permutation = []
    for a0,a1,b,c in raw:
        a1b,b1,c1 = st.multiply_fixture(((a0,a1),(b,),(c,)),h)
        permutation.append(ni[a1b+b1+c1])
    # K_h[row n, column n*h]=1 is an actual ordinary right-coset off-diagonal block.
    transformed = transform @ transform[:,permutation].conj().T
    for lam in range(p):
        expected = np.zeros((d,d),dtype=complex)
        for t in carriers:
            target,phase = st.fourier_action_fixture((lam,),h,t)
            expected[ti[target],ti[t]] = omega**phase
        block = transformed[lam*d:(lam+1)*d,lam*d:(lam+1)*d]
        np.testing.assert_allclose(block,expected,atol=3e-13)
        for other in range(p):
            if other != lam:
                np.testing.assert_allclose(transformed[lam*d:(lam+1)*d,other*d:(other+1)*d],0,atol=3e-13)
        # In N x F_p^2, H={(exp(u*h),(u,0))}: proper quotient support.
        # A diagonal q block is I_n/(p^2*n); each center branch has mass 1/p.
        assert p**2*np.trace(np.eye(d)/(p**2*n)).real == pytest.approx(1/p)
        np.testing.assert_allclose(p*block/(p**2*n),expected/(p**2*d),atol=3e-13)
        assert np.linalg.norm(expected-np.abs(expected)) > 1  # Quadratic phases cannot be dropped.
        if lam:
            # Measuring/discarding the coherent mu register kills this off-diagonal block.
            traced = np.trace(expected.reshape(p*p,p,p*p,p),axis1=1,axis2=3)
            np.testing.assert_allclose(traced,0,atol=3e-13)
    assert d*d/n > 1  # Irrep-sector normalization is wrong for this reducible source.


@pytest.mark.parametrize("factory",[_filiform,_ut4])
def test_monomial_representation_composition_including_noncentral_commutators(factory):
    st,rng = factory(11),random.Random(51)
    for _ in range(70):
        g,h = _element(st,rng),_element(st,rng)
        label = tuple(rng.randrange(st.p) for _ in range(st.c_width))
        t = tuple(rng.randrange(st.p) for _ in range(st.carrier_width))
        u,ph = st.fourier_action_fixture(label,h,t)
        v,pg = st.fourier_action_fixture(label,g,u)
        target,phase = st.fourier_action_fixture(label,st.multiply_fixture(g,h),t)
        assert (v,(ph+pg) % st.p) == (target,phase)
    if factory is _filiform:
        # A B-coordinate element is diagonal but NOT scalar after the B-Fourier.
        phases = {st.fourier_action_fixture((1,),((0,0),(1,),(0,)),t)[1]
                  for t in product(range(11),repeat=3)}
        assert len(phases) == 11


@pytest.mark.parametrize("p,m,D",[(11,1,2),(11,2,3),(2**127-1,2,3)])
def test_full_jet_alignment_retains_top_without_label_relation(p,m,D):
    st,chart = _ut4(p),FullTaylorJetChart(p,m,3,D)
    labels,scales,ys = _design(chart,st)
    alignment = align_full_jet(chart,st,labels,scales,ys)
    R,J = alignment.carrier_width,chart.jet_width
    assert _product(alignment.forward,alignment.inverse,p) == _identity(R)
    assert _product(alignment.forward,alignment.displacement_map,p) == [row[:J] for row in _identity(R)]
    assert any(k == D for _,k,_ in chart.indices)
    # No cancellation requirement, even if a proposed old degree-2D relation fails.
    labels = [(1,)]*len(labels)
    assert align_full_jet(chart,st,labels,scales,ys).chart == chart
    assert align_full_jet(chart,st,[(0,)]*len(labels),scales,ys).chart == chart
    B,bound = full_jet_rank_schedule(chart)
    assert B > J//3 and bound <= Fraction(1,4*p)
    assert {(k-1,)+alpha for alpha,k,a in chart.indices if a == 0} == set(monomials(m+1,D-1))


@pytest.mark.parametrize("p", [11, 2**127-1])
@pytest.mark.parametrize("label", [0, 1])
def test_public_left_inverse_split_and_alternative_spectator_complement(p, label):
    st, chart = _filiform(p), FullTaylorJetChart(p, 1, 2, 2)
    _, scales, ys = _design(chart, st)
    alignment = align_full_jet(chart, st, [(label,)]*len(scales), scales, ys)
    J, R = chart.jet_width, alignment.carrier_width
    rng = random.Random(441)
    change = _identity(R)
    for i in range(J):
        for j in range(J, R):
            change[i][j] = rng.randrange(p)
    inverse_change = _identity(R)
    for i in range(J):
        for j in range(J, R):
            inverse_change[i][j] = -change[i][j] % p
    forward = _product(change, alignment.forward, p)
    inverse = _product(alignment.inverse, inverse_change, p)
    T, P, spectator = alignment.displacement_map, forward[:J], forward[J:]
    assert _product(P, T, p) == _identity(J)
    assert _product(spectator, T, p) == [[0]*J for _ in range(R-J)]
    assert _product(forward, inverse, p) == _identity(R)
    for _ in range(8):
        x = tuple(rng.randrange(p) for _ in range(R))
        j = _mv(P, x, p)
        Tj = _mv(T, j, p)
        kernel = tuple((a-b) % p for a, b in zip(x, Tj))
        assert _mv(P, kernel, p) == (0,)*J
        assert tuple((a+b) % p for a, b in zip(Tj, kernel)) == x
        assert _mv(spectator, kernel, p) == _mv(spectator, x, p)
        # The abstract ker(P) spectator is the same residual represented by
        # the implementation's chosen complement columns, not lost garbage.
        assert _mv(inverse, (0,)*J+_mv(spectator, x, p), p) == kernel


@pytest.mark.parametrize("p", [11, 2**127-1])
def test_alternative_public_alignment_requires_exact_phase_pullback(p):
    st, chart = _filiform(p), FullTaylorJetChart(p, 1, 2, 2)
    labels, scales, ys = _design(chart, st)
    alignment = align_full_jet(chart, st, labels, scales, ys)
    J, R = chart.jet_width, alignment.carrier_width
    rng = random.Random(819)
    change, inverse_change = _identity(R), _identity(R)
    for i in range(J):
        for j in range(J, R):
            change[i][j] = rng.randrange(p)
            inverse_change[i][j] = -change[i][j] % p
    forward = _product(change, alignment.forward, p)
    inverse = _product(alignment.inverse, inverse_change, p)
    elements = [_element(st, rng) for _ in labels]
    def action(carrier):
        result, phase = (), 0
        for i, (label, g) in enumerate(zip(labels, elements)):
            target, value = st.fourier_action_fixture(label, g, carrier[3*i:3*i+3])
            result += target
            phase = (phase+value) % p
        return result, phase
    zero_target, _ = action((0,)*R)
    displacement = _mv(forward, zero_target, p)
    wrong_phase_seen = False
    for _ in range(12):
        t = tuple(rng.randrange(p) for _ in range(R))
        raw = _mv(inverse, t, p)
        target, phase = action(raw)
        assert _mv(forward, target, p) == tuple((a+b) % p for a, b in zip(t, displacement))
        _, old_phase = action(_mv(alignment.inverse, t, p))
        wrong_phase_seen |= phase != old_phase
    assert wrong_phase_seen  # Matching translation alone is not a channel certificate.


@pytest.mark.parametrize("p,D",[(11,2),(11,3),(17,4),(2**127-1,2)])
def test_symbolic_phase_common_full_jet_and_second_erasure_degree(p,D):
    st,chart,rng = _filiform(p),FullTaylorJetChart(p,1,2,D),random.Random(716)
    labels,scales,ys = _design(chart,st)
    alignment = align_full_jet(chart,st,labels,scales,ys)
    spectator = tuple(rng.randrange(p) for _ in range(alignment.carrier_width-chart.jet_width))
    packet = compile_full_jet_phase(alignment,spectator,D+2)
    assert weighted_degree(chart,packet) <= max(D+2,3*D)
    theta = [rng.randrange(p) for _ in packet.parameter_basis]
    def potential(q):
        coordinates = [sum(value*pow(q,nu[0],p) for (b,nu),value in zip(packet.parameter_basis,theta)
                           if a == b) % p for a in range(4)]
        return tuple(coordinates[:2]),(coordinates[2],),(coordinates[3],)
    for _ in range(12):
        q = rng.randrange(p)
        t = tuple(rng.randrange(p) for _ in chart.indices)
        raw = _mv(alignment.inverse,t+spectator,p)
        expected = 0
        for i,(label,s,y) in enumerate(zip(labels,scales,ys)):
            _,phase = st.fourier_action_fixture(label,potential((y[0]+s*q) % p),raw[3*i:3*i+3])
            expected -= phase
        assert packet.evaluate_fixture((q,)+t,theta) == expected % p
        y,z,s = (rng.randrange(p),),tuple(rng.randrange(p) for _ in chart.indices),rng.randrange(1,p)
        offset,matrix = chart.affine_map(y,z,s)
        point = tuple((a+b) % p for a,b in zip(offset,_mv(matrix,(q,)+t,p)))
        pulled = pullback_phase(chart,packet,y,z,s)
        assert pulled.evaluate_fixture((q,)+t,theta) == packet.evaluate_fixture(point,theta)
    eta = [int(k == D and a == 0) for _,k,a in chart.indices]
    residual = fourier_curve_packet(chart,packet.parameter_basis,eta)
    assert residual.degree == D  # Reusing the previous D-1 budget would be wrong.
    with pytest.raises(ValueError,match="verified"):
        compile_full_jet_phase(replace(alignment,forward=alignment.inverse),spectator,D+2)
    degree = weighted_degree(chart,packet)
    negative = replace(packet,terms={key:-value % p for key,value in packet.terms.items()})
    result = weighted_merge(chart,[packet,negative],[1,1],
                            [((0,),(0,)*chart.jet_width),((1,),(2,)*chart.jet_width)],degree)
    assert weighted_degree(chart,result) < degree


def test_full_jet_transport_identity_is_coefficientwise_and_invertible():
    chart = FullTaylorJetChart(11,2,2,3)
    basis = tuple((a,nu) for a in range(2) for nu in monomials(2,3))
    y,s = (3,7),4
    A = chart.transport_matrix(y,s)
    assert _rank(A,11) == chart.jet_width
    for j in range(chart.jet_width):
        packet = SymbolicScalarPacket(11,2,chart.jet_width,basis,_jet_terms(chart,basis,j,chart.width))
        pulled = pullback_phase(chart,packet,y,(0,)*chart.jet_width,s)
        expected = {}
        for k,c in enumerate(A[j]):
            _add(expected,_jet_terms(chart,basis,k,chart.width),c,11)
        assert {key:v for key,v in pulled.terms.items() if any(key[0])} == expected


def test_actual_ut7_derived_algebra_crosses_old_class_two_boundary():
    p,n,rng = 17,7,random.Random(291)
    normal = [(i,j) for i in range(n) for j in range(i+2,n)]
    def bracket(a,b):
        terms = {}
        if a[1] == b[0]:
            terms[(a[0],b[1])] = 1
        if b[1] == a[0]:
            terms[(b[0],a[1])] = -1
        return terms
    C = [a for a in normal if all(not bracket(a,b) for b in normal)]
    B = [a for a in normal if a[1]-a[0] >= 4 and a not in C]
    A = [a for a in normal if a not in B+C]
    assert (len(A),len(B),len(C)) == (9,2,4)
    tensor = lambda out,left,right: tuple(tuple(tuple(bracket(a,b).get(c,0) % p for b in right)
                                               for a in left) for c in out)
    st = ClassThreeStructure(p,tensor(B,A,A),tensor(C,A,A),tensor(C,A,B))
    assert bracket((0,2),(2,4)) == {(0,4):1}
    assert bracket((0,4),(4,6)) == {(0,6):1}  # N is genuinely class THREE.
    def exp(element):
        X = [[0]*n for _ in range(n)]
        for (i,j),value in zip(A+B+C,sum(element,())):
            X[i][j] = value
        result,power = _identity(n),_identity(n)
        for k in range(1,4):
            power = _product(power,X,p)
            result = [[(u+pow(factorial(k),-1,p)*v) % p for u,v in zip(row,other)]
                      for row,other in zip(result,power)]
        assert _product(power,X,p) == [[0]*n for _ in range(n)]
        return result
    for _ in range(20):
        g,h = _element(st,rng),_element(st,rng)
        assert exp(st.multiply_fixture(g,h)) == _product(exp(g),exp(h),p)
        label = tuple(rng.randrange(p) for _ in C)
        assert _rank(st.translation_map(label),p) == len(A)
        t = tuple(rng.randrange(p) for _ in A+B)
        u,ph = st.fourier_action_fixture(label,h,t)
        v,pg = st.fourier_action_fixture(label,g,u)
        w,phase = st.fourier_action_fixture(label,st.multiply_fixture(g,h),t)
        assert (v,(ph+pg) % p) == (w,phase)


@pytest.mark.parametrize("p",[7,2**127-1])
def test_empty_B_unifies_class_two_source_without_isotropy_or_phantom_registers(p):
    st = ClassThreeStructure(p,(),(((0,1),(p-1,0)),),(((),()),))
    chart = FullTaylorJetChart(p,1,2,2)
    _,scales,ys = _design(chart,st)
    labels = [(1,)]*len(scales)
    # An old top-displacement label relation fails in this actual design.
    assert sum(pow(s,4,p) for s in scales) % p != 0
    alignment = align_full_jet(chart,st,labels,scales,ys)
    assert alignment.carrier_width == len(labels)*2 == chart.jet_width
    packet = compile_full_jet_phase(alignment,(),4)
    assert weighted_degree(chart,packet) <= 4
    assert all(len(params) == 1 for _,params in packet.terms)
    rng = random.Random(901)
    theta = [rng.randrange(p) for _ in packet.parameter_basis]
    def value(a,q):
        return sum(v*pow(q,nu[0],p) for (b,nu),v in zip(packet.parameter_basis,theta) if a == b) % p
    for _ in range(20):
        q = rng.randrange(p)
        t = tuple(rng.randrange(p) for _ in chart.indices)
        raw = _mv(alignment.inverse,t,p)
        phase = 0
        for i,(s,y) in enumerate(zip(scales,ys)):
            qi = (y[0]+s*q) % p
            a = (value(0,qi),value(1,qi))
            x = raw[2*i:2*i+2]
            phase -= value(2,qi)+pow(2,-1,p)*(a[0]*x[1]-a[1]*x[0])
            target,known_phase = st.fourier_action_fixture((1,),(a,(),(value(2,qi),)),x)
            assert target == tuple((u+v) % p for u,v in zip(a,x))
            assert known_phase == (value(2,qi)+pow(2,-1,p)*(a[0]*x[1]-a[1]*x[0])) % p
        assert packet.evaluate_fixture((q,)+t,theta) == phase % p


def test_nonabelian_intersection_does_not_license_quotienting_the_whole_derived_group():
    # In UT7: H=<E12,E13>, N=L', K=H intersect N=<E13>.
    units = {(i,j) for i in range(7) for j in range(i+1,7)}
    derived = {(i,j) for i,j in units if j-i >= 2}
    K,H = {(0,2)},{(0,1),(0,2)}
    def brackets(left,right):
        return {(i,l) for i,j in left for k,l in right if j == k} | {
            (k,j) for i,j in left for k,l in right if l == i}
    def series(basis,quotient=frozenset()):
        layer,answer = basis,[basis]
        while layer:
            layer = brackets(basis,layer)-quotient
            answer.append(layer)
        return answer
    normalizer = {x for x in units if brackets({x},K) <= K}
    assert H & derived == K and H <= normalizer
    assert (2,4) in derived-normalizer  # [E35,E13]=-E15, not in K.
    assert brackets(normalizer,K) <= K
    assert brackets(normalizer,normalizer) <= normalizer
    quotient = normalizer-K
    new_derived = brackets(normalizer,normalizer)-K
    assert new_derived <= (derived & normalizer)-K
    Hbar = H-K
    assert not (Hbar & new_derived)
    preimage = Hbar | new_derived
    assert len(series(preimage,K)) < len(series(quotient,K))
    assert len(series(new_derived,K))-1 <= 3


@pytest.mark.parametrize("p",[11,2**127-1])
@pytest.mark.parametrize("kind",["filiform","ut4","class_two"])
def test_checked_parameter_decomposition_matches_python_source(p,kind):
    # Lean checks universal linear/bilinear maps. This separately pins the
    # Python source formula to that decomposition, not a formal refinement.
    st = (_filiform(p) if kind == "filiform" else _ut4(p) if kind == "ut4" else
          ClassThreeStructure(p,(),(((0,1),(p-1,0)),),(((),()),)))
    rng = random.Random(1458)
    def contract(forms,x,y):
        return tuple(sum(c*x[i]*y[j] for i,row in enumerate(form) for j,c in enumerate(row)) % p
                     for form in forms)
    def add(g,h):
        return tuple(tuple((u+v) % p for u,v in zip(a,b)) for a,b in zip(g,h))
    for label in [(0,)*st.c_width,tuple(rng.randrange(p) for _ in range(st.c_width))]:
        gamma = lambda a,x: sum(u*v for u,v in zip(label,contract(st.gamma,a,x))) % p
        delta = lambda a,b: sum(u*v for u,v in zip(label,contract(st.delta,a,b))) % p
        beta = lambda a,x: contract(st.beta,a,x)
        for _ in range(25):
            g,h = _element(st,rng),_element(st,rng)
            t = tuple(rng.randrange(p) for _ in range(st.carrier_width))
            x,mu = t[:st.a_width],t[st.a_width:]
            dot = lambda v: sum(a*b for a,b in zip(mu,v)) % p
            def linear(element):
                a,b,c = element
                return (sum(u*v for u,v in zip(label,c))-dot(b)
                        +pow(2,-1,p)*(gamma(a,x)-delta(x,b)-dot(beta(a,x)))
                        -pow(12,-1,p)*delta(x,beta(a,x))) % p
            def quadratic(left,right):
                return (-pow(2,-1,p)*delta(left[0],right[1])
                        -pow(6,-1,p)*delta(left[0],beta(right[0],x))) % p
            _,phase = st.fourier_action_fixture(label,g,t)
            assert phase == (linear(g)+quadratic(g,g)) % p
            assert linear(add(g,h)) == (linear(g)+linear(h)) % p
            _,combined = st.fourier_action_fixture(label,add(g,h),t)
            _,other = st.fourier_action_fixture(label,h,t)
            assert (combined-phase-other) % p == (quadratic(g,h)+quadratic(h,g)) % p
