"""Actual measurement/source boundaries, not another formula-only certificate."""
from fractions import Fraction
from itertools import product

import numpy as np
import pytest

from theorems.planted_qary_dual_intersection_cascade_bridge import (
    recover_measured_span, measured_span_recovery_probability,
    measurement_baseline_comparison,
)
from theorems.planted_qary_noisy_parity_check_likelihood_bridge import source_geometry


def span(rows, q, n):
    return {tuple(sum(c*r[j] for c,r in zip(coefficients,rows)) % q for j in range(n))
            for coefficients in product(range(q),repeat=len(rows))}


@pytest.mark.parametrize("q,n,rows,copies", [
    (2,3,[[1,1,0]],3), (3,2,[[1,2]],3), (3,2,[[1,0],[0,1]],2),
])
@pytest.mark.parametrize("affine", [False,True])
def test_complete_observation_census_matches_actual_recovery(q,n,rows,copies,affine):
    B = span(rows,q,n)
    offset = tuple((i+1) % q for i in range(n))
    observations = [tuple((x+y) % q for x,y in zip(b,offset)) if affine else b for b in B]
    successes = 0
    for sample in product(observations,repeat=copies):
        result = recover_measured_span(sample,q=q,n=n,shared_affine_offset=affine)
        recovered = span(result["observed_span_basis"],q,n)
        successes += recovered == B
        assert recovered <= B
        assert result["measured_input_copies"] == copies
        assert not result["full_unknown_subspace_recovery_certified"]
    probability = Fraction(successes,len(B)**copies)
    assert probability == measured_span_recovery_probability(q,len(rows),copies,shared_affine_offset=affine)


def test_unknown_fixed_offset_is_not_free_and_cannot_be_treated_as_homogeneous():
    observations = [(1,0),(1,1),(1,2)]
    assert recover_measured_span(observations,q=3,n=2)["observed_rank"] == 2
    result = recover_measured_span(observations,q=3,n=2,shared_affine_offset=True)
    assert result["observed_span_basis"] == [[0,1]]
    assert result["elimination_rows"] == 2
    assert not result["known_generator_or_offset_supplied_to_recovery"]


def density_and_fourier(q,n,rows):
    _,vectors,B,dual = source_geometry(q,n,rows,cap=128)
    psi = np.array([1/np.sqrt(len(B)) if x in B else 0 for x in vectors])
    F = np.array([[np.exp(2j*np.pi*sum(a*b for a,b in zip(u,x))/q)/np.sqrt(len(vectors))
                   for x in vectors] for u in vectors])
    return vectors,B,dual,np.outer(psi,psi.conj()),F


@pytest.mark.parametrize("rows", [[[1,0]],[[1,1]]])
def test_complete_phase_dephasing_preserves_direct_recovery_but_erases_fourier(rows):
    q,n = 3,2
    vectors,B,_,rho,F = density_and_fourier(q,n,rows)
    phased = np.zeros_like(rho,dtype=complex)
    for z in vectors:
        phase = np.array([np.exp(2j*np.pi*sum(a*b for a,b in zip(z,x))/q) for x in vectors])
        phased += phase[:,None]*rho*phase.conj()[None,:]/len(vectors)
    np.testing.assert_allclose(np.diag(phased),[1/len(B) if x in B else 0 for x in vectors],atol=1e-13)
    np.testing.assert_allclose(np.diag(F@phased@F.conj().T),1/len(vectors),atol=1e-13)
    replaced = np.eye(len(vectors))/len(vectors)
    assert not np.allclose(np.diag(replaced),np.diag(phased))


def test_fresh_uniform_offsets_defeat_all_direct_transcripts_not_coherent_fourier():
    marginals,readouts = [],[]
    for rows in ([[1,0]],[[1,1]]):
        q,n = 3,2
        vectors,B,dual,_,F = density_and_fourier(q,n,rows)
        rho = np.zeros((len(vectors),len(vectors)),complex)
        for offset in vectors:
            translated = {tuple((x+y) % q for x,y in zip(b,offset)) for b in B}
            psi = np.array([1/np.sqrt(len(B)) if x in translated else 0 for x in vectors])
            rho += np.outer(psi,psi.conj())/len(vectors)
        marginals.append(np.diag(rho).real)
        readout = np.diag(F@rho@F.conj().T).real
        readouts.append(readout)
        np.testing.assert_allclose(marginals[-1],1/len(vectors),atol=1e-13)
        np.testing.assert_allclose(readout,[1/len(dual) if x in dual else 0 for x in vectors],atol=1e-13)
    np.testing.assert_allclose(marginals[0],marginals[1],atol=1e-13)
    assert not np.allclose(readouts[0],readouts[1])
    np.testing.assert_allclose(np.kron(marginals[0],marginals[0]),
                               np.kron(marginals[1],marginals[1]),atol=1e-13)


def test_sample_only_receiver_does_not_enumerate_group_or_unknown_code(monkeypatch):
    import theorems.planted_qary_dual_intersection_cascade_bridge as module
    def forbidden(*args,**kwargs):
        raise AssertionError("receiver tried an exponential enumeration")
    n,d = 128,64
    sample = [[int(j == i or j == i+d) for j in range(n)] for i in range(d)]
    monkeypatch.setattr(module.itertools,"product",forbidden)
    result = recover_measured_span(sample,q=3,n=n)
    assert result["observed_rank"] == d
    assert result["coherent_operations_after_measurement"] == 0


@pytest.mark.parametrize("q", [True,0,1,4,9,128])
def test_field_gate_rejects_composite_and_unsupported_inputs(q):
    with pytest.raises(ValueError):
        recover_measured_span([(1,0)],q=q,n=2)
    with pytest.raises(ValueError):
        measured_span_recovery_probability(q,1,3)


@pytest.mark.parametrize("sample", [[(1,)],[(True,0)],[(3,0)],[(-1,0)],[(1.0,0)]])
def test_receiver_rejects_noncanonical_observations(sample):
    with pytest.raises(ValueError):
        recover_measured_span(sample,q=3,n=2)


def test_zero_copy_empty_space_and_underdetermined_cases():
    assert recover_measured_span([],q=3,n=2)["observed_span_basis"] == []
    assert measured_span_recovery_probability(3,0,0) == 1
    assert measured_span_recovery_probability(3,1,0) == 0
    assert measured_span_recovery_probability(3,1,1,shared_affine_offset=True) == 0
    assert measured_span_recovery_probability(3,1,3) == Fraction(26,27)


def test_comparison_keeps_source_cost_and_harder_tasks_outside_claim():
    comparison = measurement_baseline_comparison(3,3,1,3)
    assert Fraction(comparison["homogeneous_Z_sample_recovery_exact"]) == Fraction(26,27)
    assert Fraction(comparison["coherent_coset_Fourier_recovery_exact"]) == Fraction(208,243)
    assert comparison["fresh_uniform_offsets_hide_B_from_all_Z_transcripts"]
    assert not comparison["Z_samples_free_from_an_arbitrary_classical_problem_instance"]
    assert not comparison["quantum_state_source_cost_included_by_this_comparison"]
    assert not comparison["recovery_probability_is_an_algorithmic_speedup"]
