"""Intertwiner reduction and bad-gap controls; no logical-gate benchmark."""
from fractions import Fraction
from itertools import product

import numpy as np
import pytest

from theorems.logical_gate_source import MarkedEncoderGap, known_logical_fiber
from theorems.symbolic_scalar_phase_erasure import _fmpz_solve_coordinates
from theorems.ut5_matrix_phase_alignment import _identity


def test_rectangular_choi_action_and_normalized_phase_optimized_residual():
    rng = np.random.default_rng(244)
    def unitary(n):
        return np.linalg.qr(rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)))[0]
    for n,d in [(7,3),(9,4)]:
        v,a,b = unitary(n)[:,:d],unitary(n),unitary(d)
        choi = v.reshape(-1)/np.sqrt(d)  # Physical register before reference.
        overlap = np.vdot(choi,np.kron(a,b.conj()) @ choi)
        expected = np.trace(v.conj().T @ a @ v @ b.conj().T)/d
        assert overlap == pytest.approx(expected)
        phase = overlap/abs(overlap)
        residual = np.linalg.norm(a @ v-phase*v @ b,"fro")**2/d
        assert residual == pytest.approx(2*(1-abs(overlap)))
        # Discarding the reference loses which logical B was implemented.
        reduced = v @ v.conj().T/d
        assert np.trace(reduced) == pytest.approx(1)
        assert abs(overlap-np.trace(v.conj().T @ a @ v @ b.T)/d) > 1e-3
    # The maximally mixed physical marginal forgets the logical label.
    a = np.diag([1,np.exp(2j*np.pi/5)])
    j = np.eye(2).reshape(-1)/np.sqrt(2)
    assert np.vdot(j,np.kron(a,a.conj()) @ j) == pytest.approx(1)
    assert abs(np.vdot(j,np.kron(a,np.eye(2)) @ j)) < 1
    np.testing.assert_allclose(a @ (np.eye(2)/2) @ a.conj().T,np.eye(2)/2,atol=1e-14)


@pytest.mark.parametrize("p",[5,2**127-1])
def test_logical_fiber_recovers_known_nonnormal_graph_without_guessing_hidden_data(p):
    unit = tuple(map(tuple,_identity(3)))
    diagonal = tuple(v+v for v in unit)
    a = (2,3,4)
    fiber = known_logical_fiber(p,3,3,diagonal,a)
    assert fiber.particular == a and fiber.vertical_kernel == ()
    # H=diagonal(G) is nonnormal for Heisenberg G: [(x,0),(y,y)]=(z,0).
    assert _fmpz_solve_coordinates(diagonal,unit[2]+(0,0,0),p) is None
    # A central projective ambiguity must be returned, not suppressed.
    enlarged = diagonal+((0,0,0)+unit[2],)
    fiber = known_logical_fiber(p,3,3,enlarged,a)
    assert len(fiber.vertical_kernel) == 1
    assert _fmpz_solve_coordinates(fiber.vertical_kernel,unit[2],p) is not None
    for t in (0,1,p-1):
        b = tuple((v+t*w) % p for v,w in zip(fiber.particular,fiber.vertical_kernel[0]))
        assert _fmpz_solve_coordinates(enlarged,a+b,p) is not None


def test_logical_fiber_rejects_missing_and_malformed_lifts():
    assert known_logical_fiber(5,2,1,((1,0,2),),(0,1)) is None
    assert known_logical_fiber(5,2,1,(),(1,0)) is None
    assert known_logical_fiber(5,2,1,(),(0,0)).particular == (0,)
    assert known_logical_fiber(5,2,0,((1,0),),(1,0)).particular == ()
    with pytest.raises(ValueError,match="independent"):
        known_logical_fiber(5,2,1,((1,0,2),(2,0,4)),(0,0))
    with pytest.raises(ValueError,match="canonical"):
        known_logical_fiber(5,2,1,((1,0,2),),(5,0))


@pytest.mark.parametrize("p,d",[(3,2),(5,4),(5,16),(11,8)])
def test_marked_encoder_changes_exact_symmetry_but_not_much_choi_mass(p,d):
    omega = np.exp(2j*np.pi/p)
    def encoder(mark):
        v = np.zeros((d*p,d),dtype=complex)
        for x in range(d):
            v[p*x+int(x == mark),x] = 1
        return v
    plain,marked = encoder(None),encoder(d-1)
    j0,j1 = plain.reshape(-1)/np.sqrt(d),marked.reshape(-1)/np.sqrt(d)
    np.testing.assert_allclose(marked.conj().T @ marked,np.eye(d))
    assert np.vdot(j0,j1) == pytest.approx(1-1/d)
    gaps = []
    for t in range(1,p):
        action = np.diag([omega**(t*flag % p) for x,flag in product(range(d),range(p))])
        assert np.trace(plain.conj().T @ action @ plain)/d == pytest.approx(1)
        overlap = np.trace(marked.conj().T @ action @ marked)/d
        assert overlap == pytest.approx(1-1/d+omega**t/d)
        assert abs(overlap) < 1
        gaps.append(1-abs(overlap))
    lo,hi = MarkedEncoderGap(p,d).gap_bounds
    assert float(lo) <= min(gaps) <= float(hi)
    # A middle power has constant worst-case action on the marked word,
    # while its normalized Choi gap vanishes with d.
    t = (p-1)//2
    worst_case_residual = abs(omega**t-1)
    assert worst_case_residual >= np.sqrt(3)-1e-14
    phase_optimized_operator_error = 2*np.sin(np.pi*t/(2*p))
    assert phase_optimized_operator_error >= 1-1e-14
    assert 1-abs(1-1/d+omega**t/d) <= 2/d+1e-14


@pytest.mark.parametrize("d",[2,4,16,256])
def test_copy_lower_bound_uses_the_actual_pair_overlap(d):
    control = MarkedEncoderGap(5,d)
    for k in (0,1,2,5):
        exact_distance_squared = 1-Fraction(d-1,d)**(2*k)
        assert exact_distance_squared <= Fraction(2*k,d)
    bound = control.choi_copy_lower_bound()
    assert bound == (d+17)//18
    if bound > 1:
        before = 1-Fraction(d-1,d)**(2*(bound-1))
        assert before < Fraction(1,9)


def test_gap_bounds_remain_exact_at_large_dimensions_and_large_primes():
    p,d = 2**127-1,2**100
    control = MarkedEncoderGap(p,d)
    lo,hi = control.gap_bounds
    assert isinstance(lo,Fraction) and hi/lo == 5
    assert 0 < lo < hi < Fraction(1,d)
    assert control.choi_copy_lower_bound() == (d+17)//18
    # The displayed p^2 gap penalty is NOT a p^2 copy lower bound.
    assert control.choi_copy_lower_bound() == MarkedEncoderGap(5,d).choi_copy_lower_bound()
    with pytest.raises(ValueError,match="rational"):
        control.choi_copy_lower_bound(0.8)
    with pytest.raises(ValueError,match="odd"):
        MarkedEncoderGap(2,d)
    with pytest.raises(ValueError,match="at least two"):
        MarkedEncoderGap(5,1)


def test_subcode_composition_preserves_knill_laflamme_and_logical_gap():
    # A supplied code satisfying KL retains KL under every isometric subcode.
    # E=(I,0)^T and errors sending E to orthogonal syndrome blocks provide
    # an exact abstract control; no physical distance is inferred from it.
    d,p = 3,5
    size = d*p
    e = np.vstack((np.eye(size),np.zeros((size,size))))
    error = np.block([[np.zeros((size,size)),np.eye(size)],
                      [np.eye(size),np.zeros((size,size))]])
    v = np.zeros((size,d))
    for x in range(d):
        v[p*x+int(x == d-1),x] = 1
    code = e @ v
    for a,b in product([np.eye(2*size),error],repeat=2):
        parent = e.T @ a.T @ b @ e
        scalar = np.trace(parent)/size
        np.testing.assert_allclose(parent,scalar*np.eye(size),atol=1e-14)
        np.testing.assert_allclose(code.T @ a.T @ b @ code,scalar*np.eye(d),atol=1e-14)
    logical_z = np.diag([np.exp(2j*np.pi*flag/p) for x,flag in product(range(d),range(p))])
    physical = e @ logical_z @ e.T+np.eye(2*size)-e @ e.T
    assert np.trace(code.T @ physical @ code)/d == pytest.approx(
        np.trace(v.T @ logical_z @ v)/d)
