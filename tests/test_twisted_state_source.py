"""Source and public-algebra falsifiers, not a state-symmetry solver."""
from fractions import Fraction
from itertools import product
from math import prod
import random

import numpy as np
import pytest

from theorems.class_three_monomial_jet import (
    ClassThreeStructure, FullTaylorJetChart, align_full_jet, compile_full_jet_phase,
)
from theorems.nonlinear_jet_erasure import (
    fourier_curve_packet, pullback_phase, weighted_degree,
)
from theorems.state_symmetry_coset_transfer import plan_orbit_state_transfer
from theorems.symbolic_scalar_phase_erasure import PublicLieAlgebra, _fmpz_solve_coordinates
from theorems.twisted_state_source import (
    affine_character_sector, attach_linear_character, character_normalizer,
)
from theorems.ut5_matrix_phase_alignment import _identity, _rank


def _heisenberg(p):
    return PublicLieAlgebra(p,3,lambda a,b: (0,0,(a[0]*b[1]-a[1]*b[0]) % p))


def _filiform_extra_center(p):
    return ClassThreeStructure(p,(((0,1),(p-1,0)),),
        (((0,0),(0,0)),((0,0),(0,0))),(((1,),(0,)),((0,),(0,))))


@pytest.mark.parametrize("p",[7,2**127-1])
def test_character_normalizer_is_strictly_smaller_than_plain_normalizer(p):
    algebra = _heisenberg(p)
    x,y,z = map(tuple,_identity(3))
    basis,chi = (y,z),(3,1)
    result = character_normalizer(algebra,basis,chi)
    assert len(result.normalizer) == 2 and len(result.kernel) == 1
    assert result.scalar_center_width == 1
    assert _fmpz_solve_coordinates(result.kernel,(0,1,p-3),p) is not None
    assert _fmpz_solve_coordinates(result.normalizer,x,p) is None
    for v in result.normalizer:
        for k in basis:
            assert _fmpz_solve_coordinates(result.kernel,algebra.bracket(v,k),p) is not None
    # K is an ideal, but conjugation by exp(x) changes its character.
    assert _fmpz_solve_coordinates(basis,algebra.bracket(x,y),p) == (0,1)
    ordinary = character_normalizer(algebra,basis,(0,0))
    assert len(ordinary.normalizer) == 3 and ordinary.scalar_center_width == 0
    assert len(ordinary.kernel) == 2
    empty = character_normalizer(algebra,(),())
    assert empty.kernel == () and len(empty.normalizer) == 3


def test_noncharacters_and_non_subalgebras_are_rejected():
    algebra = _heisenberg(7)
    x,y,z = map(tuple,_identity(3))
    for basis,chi,error in [((x,y,z),(0,0,1),"vanish"),
                            ((x,y),(0,0),"subalgebra"),
                            ((y,y),(0,0),"independent"),
                            ((y,z),(0,7),"canonical")]:
        with pytest.raises(ValueError,match=error):
            character_normalizer(algebra,basis,chi)


@pytest.mark.parametrize("p",[5,2**127-1])
def test_affine_sector_counts_include_fixed_and_unrestricted_labels(p):
    affine = affine_character_sector(p,2,((1,0),),(2,))
    assert affine.particular == (2,0)
    assert affine.label_probability == Fraction(1,p)
    assert affine.contains((2,p-1)) and not affine.contains((1,0))
    fixed = affine_character_sector(p,2,((1,0),(0,1)),(2,3))
    assert fixed.directions == () and fixed.label_probability == 1
    assert fixed.contains((2,3)) and not fixed.contains((2,2))
    free = affine_character_sector(p,2,(),())
    assert len(free.directions) == 2 and free.label_probability == Fraction(1,p*p)
    # Non-coordinate constraints must be solved, not treated as positions.
    tilted = affine_character_sector(p,3,((1,2,3),(0,1,4)),(2,1))
    assert tilted.contains(tilted.particular)
    assert len(tilted.directions) == 1
    for t in (0,1,p-1):
        assert tilted.contains(tuple((a+t*b) % p for a,b in
                                     zip(tilted.particular,tilted.directions[0])))


def test_affine_sector_rejects_invalid_public_constraints():
    with pytest.raises(ValueError,match="independent"):
        affine_character_sector(5,2,((1,0),(2,0)),(1,2))
    with pytest.raises(ValueError,match="canonical"):
        affine_character_sector(5,2,((1,0),),(5,))
    with pytest.raises(ValueError,match="positive"):
        affine_character_sector(5,0,(),())


@pytest.mark.parametrize("k",[1,3,5,7])
def test_actual_mixed_copy_source_converges_to_twisted_not_ordinary_cosets(k):
    p = 5
    omega = np.exp(2j*np.pi/p)
    addresses = list(product(range(p),repeat=2))
    # R(x,y)=diag(omega^x,omega^(x+y)), rho=diag(.6,.4).
    # Projective support stabilizer H={(x,0)}, chi(x,0)=omega^x.
    overlaps = np.array([[omega**((x-u) % p)*(.6+.4*omega**((y-v) % p))
                          for u,v in addresses] for x,y in addresses])
    sigma = overlaps**k/len(addresses)
    twisted = np.array([[omega**(k*(x-u) % p) if y == v else 0
                         for u,v in addresses] for x,y in addresses])/len(addresses)
    ordinary = np.array([[int(y == v) for u,v in addresses] for x,y in addresses])/len(addresses)
    eta = max(abs(.6+.4*omega**j) for j in range(1,p))**k
    assert np.linalg.eigvalsh(sigma).min() > -2e-15
    assert np.linalg.eigvalsh(twisted).min() > -2e-15
    assert np.trace(sigma) == pytest.approx(1)
    td = np.abs(np.linalg.eigvalsh(sigma-twisted)).sum()/2
    assert td <= np.sqrt(len(addresses))*eta/2+2e-14
    if k % p:
        assert np.abs(np.linalg.eigvalsh(twisted-ordinary)).sum()/2 == pytest.approx(1)
    else:
        np.testing.assert_allclose(twisted,ordinary,atol=2e-14)
    # An original single copy still has the nonzero phase when k=0 mod p.
    assert overlaps[addresses.index((1,0)),addresses.index((0,0))] == pytest.approx(omega)


def test_sparse_regular_state_really_has_the_claimed_character_and_gap():
    p,st = 5,_filiform_extra_center(5)
    omega = np.exp(2j*np.pi/p)
    v = (1,2,3,4,1)
    def group_multiply(a,b):
        n = st.multiply_fixture((a[:2],a[2:3],a[3:5]),(b[:2],b[2:3],b[3:5]))
        return sum(n,())+tuple((x+y) % p for x,y in zip(a[5:],b[5:]))
    def h(u,z):
        n = tuple(u*x % p for x in v)
        return n[:3]+((n[3]+z) % p,n[4])+(u,0)
    support = {h(u,z):omega**((-2*u-3*z) % p)/p for u,z in product(range(p),repeat=2)}
    assert len(support) == p*p
    def expectation(g):
        return sum(np.conj(support.get(group_multiply(g,a),0))*value for a,value in support.items())
    for u,z in product(range(p),repeat=2):
        assert expectation(h(u,z)) == pytest.approx(omega**((2*u+3*z) % p))
    for g in [(0,0,0,0,0,0,1),(0,0,1,0,0,0,0),(0,0,0,0,1,0,0)]:
        assert expectation(g) == pytest.approx(0)


def test_relative_abelian_base_is_not_an_ordinary_abelian_hiding_source():
    p,a,b = 5,2,1
    omega,half = np.exp(2j*np.pi/p),pow(2,-1,p)
    psi = np.array([omega**((half*a*t*t+b*t) % p)/np.sqrt(p) for t in range(p)])
    # Linear Heisenberg representation in BCH coordinates:
    # R(x,y,z)=omega^(z-x*y/2) X^x Z^(-y).
    def acted(x,y,z):
        state = np.zeros(p,dtype=complex)
        for t in range(p):
            state[(t+x) % p] = omega**((z-half*x*y-y*t) % p)*psi[t]
        return state
    for x,y,z in product(range(p),repeat=3):
        overlap = np.vdot(psi,acted(x,y,z))
        expected = omega**((z-b*x) % p) if (y+a*x) % p == 0 else 0
        assert overlap == pytest.approx(expected,abs=2e-14)
    addresses = list(product(range(p),repeat=2))
    rows = np.array([acted(x,y,0) for x,y in addresses])
    sigma = rows @ rows.conj().T/(p*p)
    phase = lambda x,y: (half*x*(y+a*x)-b*x) % p
    expected = np.array([[omega**((phase(x,y)-phase(u,v)) % p)
                           if (y+a*x-v-a*u) % p == 0 else 0
                          for u,v in addresses] for x,y in addresses])/(p*p)
    np.testing.assert_allclose(sigma,expected,atol=2e-14)
    fourier = np.array([[omega**((-s*x-t*y) % p)/p for x,y in addresses]
                        for s,t in addresses])
    probabilities = np.diag(fourier @ sigma @ fourier.conj().T).real
    outside = sum(prob for (s,t),prob in zip(addresses,probabilities) if (s-a*t) % p)
    assert outside == pytest.approx(1-1/p)
    # The known-subgroup character is learned from one ORIGINAL copy.
    controlled = np.array([acted(t,-a*t % p,0) for t in range(p)])/np.sqrt(p)
    ft = np.array([[omega**((-s*t) % p)/np.sqrt(p) for t in range(p)] for s in range(p)])
    char_probs = np.abs(ft @ controlled)**2
    np.testing.assert_allclose(char_probs.sum(axis=1),np.eye(p)[-b % p],atol=2e-14)


@pytest.mark.parametrize("k",[2,5])
def test_actual_twisted_regular_kernel_has_affine_not_uniform_center_sectors(k):
    p,st = 5,_filiform_extra_center(5)
    omega = np.exp(2j*np.pi/p)
    chi,ell,u = 3,2,2
    h = ((2,4),(1,),(3,2))
    # Selected entries of T (sum_z conj(chi(h*z)^k) K_(h*z)) T^dag.
    # T[lambda,x,mu; a,b,c] = [x=-a] omega^(mu*b-lambda.c)/sqrt(p^3).
    # No exponentially large group density matrix is constructed.
    def entry(label,other,row,col):
        a = tuple(-x % p for x in row[:2])
        total = 0j
        for b,c0,c1,z in product(range(p),repeat=4):
            hz = (h[0],h[1],((h[2][0]+z) % p,h[2][1]))
            ap,bp,cp = st.multiply_fixture((a,(b,),(c0,c1)),hz)
            if tuple(-x % p for x in ap) != col[:2]:
                continue
            exponent = (row[2]*b-label[0]*c0-label[1]*c1-col[2]*bp[0]
                        +sum(x*y for x,y in zip(other,cp))-k*(ell*u+chi*z)) % p
            total += omega**exponent/p**3
        return total
    sector = affine_character_sector(p,2,((1,0),),(k*chi % p,))
    for label in product(range(p),repeat=2):
        for col in [(0,0,0),(1,3,2),(4,2,1)]:
            row,phase = st.fourier_action_fixture(label,h,col)
            expected = p*omega**((phase-k*ell*u) % p) if sector.contains(label) else 0
            assert entry(label,label,row,col) == pytest.approx(expected,abs=3e-13)
        wrong = row[:2]+((row[2]+1) % p,)
        assert entry(label,label,wrong,col) == pytest.approx(0,abs=3e-13)
        other = (label[0],(label[1]+1) % p)
        assert entry(label,other,row,col) == pytest.approx(0,abs=3e-13)
    # Diagonal blocks sum over |Z|=p; all allowed labels have mass 1/p.
    m,r,s,z = 2,2,1,2
    mass = Fraction(p**m*p**(r+s)*p,p**m*p**(r+s+z))
    assert mass == sector.label_probability == Fraction(1,p)
    assert p*mass == 1
    assert Fraction(p,p**m*p**(r+s+z))/mass == Fraction(1,p**(m+r+s))


@pytest.mark.parametrize("p,m",[(11,1),(11,2),(2**127-1,1)])
def test_unknown_character_is_in_the_public_compiler_without_hidden_coefficients(p,m):
    st,chart = _filiform_extra_center(p),FullTaylorJetChart(p,m,2,2)
    rows,scales,ys = [],[],[]
    for scale,y in product((1,2),product(range(2),repeat=m)):
        row = [pow(scale,k,p)*prod(pow(v,e,p) for v,e in zip(y,alpha)) % p
               for alpha,k,a in chart.indices if a == 0]
        if _rank(rows+[row],p) > len(rows):
            rows.append(row)
            scales.append(scale)
            ys.append(y)
    labels = [(3,2)]*len(rows)  # Fixed labels, not uniformly sampled ones.
    alignment = align_full_jet(chart,st,labels,scales,ys)
    spectator = (1,)*(alignment.carrier_width-chart.jet_width)
    base = compile_full_jet_phase(alignment,spectator,4)
    powers = tuple(i % 3 for i in range(len(rows)))
    twisted = attach_linear_character(base,scales,ys,powers)
    assert len(twisted.parameter_basis) == len(base.parameter_basis)+m
    assert weighted_degree(chart,twisted) <= max(4,6)
    rng = random.Random(124)
    theta = tuple(rng.randrange(p) for _ in base.parameter_basis)
    ell = tuple(rng.randrange(p) for _ in range(m))
    for _ in range(15):
        point = tuple(rng.randrange(p) for _ in range(base.width))
        extra = sum(k*sum(e*(y0+s*q) for e,y0,q in zip(ell,y,point[:m]))
                    for k,s,y in zip(powers,scales,ys)) % p
        assert twisted.evaluate_fixture(point,theta+ell) == (base.evaluate_fixture(point,theta)+extra) % p
    pulled = pullback_phase(chart,twisted,(2,)*m,(1,)*chart.jet_width,3)
    assert weighted_degree(chart,pulled) <= 6
    zero = attach_linear_character(base,scales,ys,(0,)*len(rows))
    assert zero.parameter_basis == twisted.parameter_basis and zero.terms == base.terms
    eta = (1,)*chart.jet_width
    assert fourier_curve_packet(chart,base.parameter_basis,eta).terms == fourier_curve_packet(
        chart,twisted.parameter_basis,eta).terms
    with pytest.raises(ValueError,match="nonzero"):
        attach_linear_character(base,[0]+scales[1:],ys,powers)
    with pytest.raises(ValueError,match="canonical"):
        attach_linear_character(base,scales,ys,[p]+list(powers[1:]))


def test_existing_source_error_ledger_does_not_charge_p_copies_to_kill_phase():
    p = 2**127-1
    plan = plan_orbit_state_transfer(p**20,Fraction(1,8),1000,Fraction(1,100))
    # Its arithmetic applies to the twisted comparison after its separate
    # source lemma, not to an ordinary coset source with phase ignored.
    assert plan.copies_per_label < p
    assert plan.total_preparation_uses_bound == 1000*plan.copies_per_label
    assert plan.hybrid_error_bound <= Fraction(1,400)
