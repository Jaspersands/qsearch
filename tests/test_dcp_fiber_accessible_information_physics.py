from fractions import Fraction
from itertools import product
import json

import numpy as np
import pytest

from theorems.dcp_correlated_phase_block import density
from theorems.dcp_fiber_accessible_information import (
    REPORT, build_report, fiber_geometry, finite_POVM_control,
    moment_certificate, native_additive_alias_bound, weighted_fourth_moment,
)


def ensemble(A, t, y):
    _, F, frequencies, groups = fiber_geometry(A, t, y)
    Q, q = 1 << (t-2), 1 << t
    states = np.array([[np.exp(2j*np.pi*sum(a*b for a,b in zip(f,s))/q)
                        for f in frequencies] for s in product(range(Q), repeat=len(A))])
    return states, F, groups


@pytest.mark.parametrize("A,t,y", [(((1,5,13,29),),6,(1,)),
                                   (((1,17,33,49),),6,(1,)),
                                   (((4,8,16),),5,(0,))])
def test_complex_weight_fourth_moment_matches_actual_secret_characters(A,t,y):
    states, F, groups = ensemble(A,t,y)
    rng = np.random.default_rng(19)
    c = moment_certificate(A,t,y)
    bound = Fraction(c["all_complex_weight_fourth_moment_upper_exact"])
    D = len(F)
    assert states.T@states.conj()/len(states) == pytest.approx(np.eye(D))
    for _ in range(20):
        w = rng.normal(size=D)+1j*rng.normal(size=D)
        w /= np.linalg.norm(w)
        actual = np.mean(np.abs(states@w)**4)
        counted = sum(abs(sum(w[i]*w[j] for i,j in pairs))**2 for pairs in groups.values())
        assert actual == pytest.approx(counted, abs=1e-11)
        assert actual <= float(bound)+1e-11
    signed = [(-1)**i*(i+1) for i in range(D)]
    exact = weighted_fourth_moment(groups,signed)
    w = np.array(signed)/np.linalg.norm(signed)
    assert float(exact) == pytest.approx(np.mean(np.abs(states@w)**4), abs=1e-11)


@pytest.mark.parametrize("visibility", [Fraction(0), Fraction(1,2), Fraction(1)])
def test_nonprojective_POVM_frame_on_actual_noisy_density_respects_bound(visibility):
    A,t,y = ((1,5,13,29),),6,(1,)
    c = moment_certificate(A,t,y)
    D, F = c["fiber_dimension"], c["enumerated_assignments"]
    rng = np.random.default_rng(770)
    # A rectangular isometry gives a complete, nonorthogonal rank-one POVM.
    U,_ = np.linalg.qr(rng.normal(size=(3*D,D))+1j*rng.normal(size=(3*D,D)))
    assert U.conj().T@U == pytest.approx(np.eye(D))
    probabilities = []
    for s in range(16):
        rho = density(A,t,(s,),visibility)[np.ix_(F,F)]*16/D
        assert np.trace(rho) == pytest.approx(1)
        probabilities.append(np.diag(U@rho@U.conj().T).real)
    P = np.array(probabilities)
    assert P.sum(axis=1) == pytest.approx(np.ones(16))
    pz = P.mean(axis=0)
    active = P>1e-30
    info = np.sum(P[active]*np.log2((P/pz)[active]))/16
    assert info <= c["single_block_uniform_prior_all_POVM_information_upper_bits"]+1e-12
    if visibility == 0:
        assert abs(info) < 1e-12


def test_Sidon_bound_and_modular_alias_countermodel_have_same_fiber_size():
    sidon = moment_certificate(((1,5,13,29),),6,(1,))
    aliases = moment_certificate(((1,17,33,49),),6,(1,))
    assert sidon["fiber_dimension"] == aliases["fiber_dimension"] == 4
    assert sidon["Sidon_unordered_pair_sums_including_diagonals"]
    assert not aliases["Sidon_unordered_pair_sums_including_diagonals"]
    assert Fraction(sidon["all_complex_weight_fourth_moment_upper_exact"]) == Fraction(7,4)
    assert sidon["single_block_uniform_prior_all_POVM_information_upper_bits"] < 1
    assert Fraction(aliases["all_complex_weight_fourth_moment_upper_exact"]) == 4


def test_known_dyadic_source_actually_achieves_large_information():
    c = finite_POVM_control(((4,8,16),),5,(0,))
    assert c["uniform_weight_fourth_moment_exact"] == "8"
    assert c["all_complex_weight_fourth_moment_upper_exact"] == "8"
    info = next(v for v in c["abstract_finite_POVM_controls"] if v["basis"] == "index_inverse_DFT")
    assert info["mutual_information_bits"] == pytest.approx(3)
    assert not info["measurement_is_gate_compiled"]
    assert not c["selected_matrix_is_native_average_evidence"]


def test_full_source_alias_union_counts_odd_and_even_coefficients_differently():
    q = 8
    for c in ((1,2), (-2,2), (0,-2)):
        count = sum((a*c[0]+b*c[1])%q == 0 for a,b in product(range(q), repeat=2))
        expected = Fraction(1,q) if any(v%2 for v in c) else Fraction(2,q)
        assert Fraction(count,q*q) == expected
    for n in (4,8,32,128):
        for multiple in (3,4):
            r = native_additive_alias_bound(n,multiple)
            m,t = multiple*n,n+8
            exact = Fraction(5**m-3**m+(3**m-1)*2**n,2**(t*n))
            assert exact <= Fraction(1,2**r["nonzero_integer_four_vertex_alias_probability_power_of_two_upper_exponent"])
            assert r["holds_simultaneously_for_every_measured_syndrome"]
            assert not r["constant_or_polylog_all_POVM_information_bound_proved_for_native_fibers"]


def test_noninjective_empty_and_oversized_fibers_are_not_given_invalid_certificates():
    with pytest.raises(ValueError,match="noninjective"):
        moment_certificate(((0,0),),4,(0,))
    with pytest.raises(ValueError,match="zero-probability"):
        moment_certificate(((4,8),),4,(1,))
    with pytest.raises(ValueError,match="cap"):
        moment_certificate(((1,)*13,),4,(0,))
    with pytest.raises(ValueError,match="nonzero"):
        weighted_fourth_moment({0:[(0,0)]},[0])


def test_live_scope_never_turns_uniform_moments_into_general_accessible_information():
    r = build_report()
    assert json.loads(REPORT.read_text()) == r
    assert r["single_block_scope"] and r["uniform_secret_prior_required"]
    assert not r["native_weighted_fourth_moment_bound_resolved"]
    assert not r["accepted_speedup_candidate"]
    assert not r["new_active_negative_result_created"]
    for c in r["selected_controls"]+r["selected_native_fragments"]:
        assert not c["uniform_weight_moment_is_a_bound_for_every_measurement"]
        assert not c["applies_to_nonuniform_posterior_or_adaptive_multi_packet_chain"]
        assert not c["fiber_or_measurement_inverse_supplied"]
