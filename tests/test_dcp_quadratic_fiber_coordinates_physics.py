from fractions import Fraction
from random import Random
import json

import numpy as np
import pytest

from theorems.dcp_correlated_phase_block import density
from theorems.dcp_nonlinear_fiber_pairing import phase_value
from theorems.dcp_quadratic_fiber_coordinates import (
    REPORT, build_report, coordinate_plan, finite_density_control,
    lift_free_word, noise_overlap, satisfies_quadratics,
)


def gates(x, plan, reverse=False):
    schedule = plan["Clifford_gates_after_measured_syndrome"]
    for g in reversed(schedule) if reverse else schedule:
        if g[0] == "X":
            x ^= 1 << g[1]
        elif x >> g[1] & 1:
            x ^= 1 << g[2]
    return x


@pytest.mark.parametrize("seed", range(12))
def test_native_coordinates_and_quadratics_match_all_original_assignments(seed):
    rng = Random(seed)
    n,m,t = 1+seed%3,3+seed%5,5
    A = [[rng.randrange(1 << t) for _ in range(m)] for _ in range(n)]
    y = phase_value(A,rng.randrange(1 << m),4)
    p = coordinate_plan(A,t,y)
    pivot_mask = sum(1 << i for i in p["cleared_pivot_wires"])
    assert len(p["Clifford_gates_after_measured_syndrome"]) <= p["binary_low_syndrome_rank"]*(p["retained_quantum_wires"]+1)
    for x in range(1 << m):
        out = gates(x,p)
        assert gates(out,p,reverse=True) == x
        u = sum(((out >> f)&1) << j for j,f in enumerate(p["retained_free_wires"]))
        low_matches = all(a%2 == b%2 for a,b in zip(phase_value(A,x,4),y))
        assert ((out & pivot_mask) == 0) == low_matches
        if low_matches:
            assert lift_free_word(p,u) == x
            assert satisfies_quadratics(p,u) == (phase_value(A,x,4) == y)


def test_carry_terms_are_not_dropped_and_noise_is_not_multiplied():
    p = coordinate_plan(((1,5,9),),4,(1,))
    assert p["quadratic_high_syndrome_equations"] == [{"constant":0,"linear_variables":[],"quadratic_pairs":[[0,1]],"equation_rhs":0}]
    assert [satisfies_quadratics(p,u) for u in range(4)] == [True,True,True,False]
    v = Fraction(3,4)
    assert noise_overlap(p,1,2,v) == v*v
    assert noise_overlap(p,0,1,v)*noise_overlap(p,0,2,v) == v**4 != v*v
    # Enumerate the original independent faults and check joint free parity.
    expectation = Fraction(0)
    probZ = (1-v)/2
    for e in range(8):
        prob = probZ**e.bit_count()*(1-probZ)**(3-e.bit_count())
        eta = [(e & int(d,16)).bit_count()%2 for d in p["kernel_direction_hex"]]
        expectation += prob*(-1)**sum(eta)
    assert expectation == v*v


def test_actual_full_density_permutation_clears_pivots_without_phase_loss():
    A,t,y,secret,v = ((1,0,5,1),(0,1,1,2)),4,(1,1),(1,2),Fraction(7,8)
    p = coordinate_plan(A,t,y)
    M = 1 << p["original_phase_wires"]
    F = [x for x in range(M) if phase_value(A,x,4) == y]
    original = density(A,t,secret,v)
    branch = np.zeros((M,M),complex)
    branch[np.ix_(F,F)] = original[np.ix_(F,F)]*M/len(F)
    U = np.zeros((M,M))
    for x in range(M):
        U[gates(x,p),x] = 1
    assert np.array_equal(U.T@U,np.eye(M))
    transformed = U@branch@U.T
    mask = sum(1 << i for i in p["cleared_pivot_wires"])
    assert all(abs(transformed[x,x]) < 1e-13 for x in range(M) if x&mask)
    assert np.linalg.eigvalsh(transformed) == pytest.approx(np.linalg.eigvalsh(branch))
    c = finite_density_control(A,t,y,secret,v)
    assert c["max_original_density_residual"] < 1e-12


def test_rank_zero_and_dependent_low_constraints_are_not_rejected_or_fabricated():
    p = coordinate_plan(((2,0,2),(0,2,2)),4,(2,0))
    assert p["binary_low_syndrome_rank"] == 0
    assert p["Clifford_gates_after_measured_syndrome"] == []
    assert p["retained_quantum_wires"] == 3
    dependent = coordinate_plan(((1,3,1),(3,1,3)),4,(1,3))
    assert dependent["binary_low_syndrome_rank"] == 1
    with pytest.raises(ValueError,match="inconsistent"):
        coordinate_plan(((1,3,1),(3,1,3)),4,(1,2))


def test_compiler_handles_a_non_enumerable_affine_domain_with_polynomial_output():
    # 40 free bits; exhaustive reindexing would not finish this test.
    A = [[int(i == j) for i in range(60)] for j in range(20)]
    p = coordinate_plan(A,8,[0]*20)
    assert p["retained_quantum_wires"] == 40
    assert not p["full_fiber_enumeration_used_by_compiler"]
    assert p["quadratic_high_syndrome_equations"] == [{"constant":0,"linear_variables":[],"quadratic_pairs":[],"equation_rhs":0}]*20


def test_live_controls_preserve_unresolved_source_and_inverse_obligations():
    r = build_report()
    assert json.loads(REPORT.read_text()) == r
    assert not r["accepted_speedup_candidate"]
    assert not r["source_noise_becomes_independent_after_compression"]
    assert not r["coherent_remaining_fiber_enumeration_or_inverse"]
    for c in r["finite_controls"]:
        p = c["plan"]
        assert not p["remaining_quadratic_fiber_inverse_supplied"]
        assert not p["higher_phase_linearity_in_free_bits_assumed"]
        assert not p["fresh_independent_phase_qubits_supplied"]
        assert c["max_original_density_residual"] < 1e-12
