from collections import Counter
from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
import subprocess

import numpy as np
import pytest

from native_diagonal_orbit_channel import (
    ROOT, effective_label, information_ledger, orbit_chart, orbit_word,
    run_controls, synthetic_rows,
)
from native_state_hsp_bridge import NativeGroup, ring_words


@pytest.fixture(scope="module")
def report():
    return run_controls()


@pytest.mark.parametrize("m", [1,2,3,4,5])
def test_word_orbit_chart_partitions_every_original_word(m):
    counts = Counter()
    for word in product(range(3),repeat=m):
        v,j = orbit_chart(word)
        assert orbit_word(v,j) == word
        counts[v] += 1
    assert len(counts) == 3**(m-1)
    assert set(counts.values()) == {3}


@pytest.mark.parametrize("r,n,m", [(1,1,2),(1,1,3),(1,2,2),(2,1,2)])
def test_one_actual_source_frequency_bijection_reproduces_full_iid_public_record(r,n,m):
    vectors = tuple(product(ring_words(r),repeat=n))
    counts = Counter()
    for u,auxiliary,vrest in product(vectors,product(vectors,repeat=m-1),product(range(3),repeat=m-1)):
        v = (0,)+vrest
        labels = synthetic_rows(u,v,auxiliary,r)
        assert effective_label(labels,v,r) == u
        counts[(labels,v)] += 1
    assert len(counts) == len(vectors)**m*3**(m-1)
    assert set(counts.values()) == {1}


def test_complete_original_sources_preserve_branch_weights_phases_and_full_output_channels(report):
    assert len(report["complete_source_controls"]) == 4
    for c in report["complete_source_controls"]:
        assert sum(Fraction(b["exact_orbit_weight"]) for b in c["complete_orbit_branches"]) == 1
        assert len(c["complete_orbit_branches"])*3 == c["complete_original_word_count"]
        for b in c["complete_orbit_branches"]:
            global_phase = Fraction(b["exact_secret_dependent_global_phase_mod1_NOT_USED_BY_SIMULATOR"])
            for orig,native in zip(b["exact_original_word_phases_mod1"],b["exact_effective_qutrit_phases_mod1"]):
                assert (Fraction(orig)-Fraction(native)) % 1 == global_phase
        assert c["maximum_original_vs_orbit_branch_state_error"] < 2e-12
        protocol = c["actual_label_dependent_group_protocol"]
        assert max(protocol["original_vs_one_copy_orbit_mixture_density_errors"]) < 2e-12
        for raw in protocol["full_output_group_density_real_imag_by_round"]:
            rho = np.array([[complex(*z) for z in row] for row in raw])
            assert np.isclose(np.trace(rho),1)
            assert np.allclose(rho,rho.conj().T,atol=2e-12)
            assert np.linalg.eigvalsh(rho).min() > -2e-12
        assert not c["simulation_global_phase_or_secret_is_an_algorithm_input"]
        assert not c["simulation_is_a_classical_dequantization"]


def test_explicit_seed_mixing_contrast_prevents_generalizing_to_all_collective_receivers(report):
    for c in report["complete_source_controls"]:
        escape = c["seed_mixing_escape"]
        assert np.isclose(escape["original_batch_all_plus_measurement_probability"],1)
        assert Fraction(escape["exact_pinched_probability"]) == Fraction(1,c["complete_word_orbit_count"])
        assert escape["orbit_pinched_batch_all_plus_measurement_probability"] < 1
        assert escape["this_measurement_interferes_distinct_word_orbits"]
    assert not report["all_native_quantum_receivers_ruled_out"]
    assert not report["arbitrary_seed_mixing_or_independent_per_copy_group_actions_covered"]


def test_original_unrestricted_native_batch_has_more_recovery_information_than_one_copy_cut():
    G = NativeGroup(2)
    states = [np.kron(G.supplied_phase_state(((1,0),),(s,)),G.supplied_phase_state(((0,1),),(s,))) for s in ring_words(2)]
    average = sum(np.outer(psi,psi.conj()) for psi in states)/len(states)
    eigenvalues = np.linalg.eigvalsh(average).clip(0)
    dense_PGM_success = sum(np.sqrt(eigenvalues))**2/len(states)
    assert dense_PGM_success > 3/len(states)+.1
    # This dense information-only calibration is not an efficient measurement compiler.


@pytest.mark.parametrize("a", [(1,0),(0,1),(2,2)])
def test_one_qutrit_dimension_bound_is_tight_conditionally_on_nonzero_full_ring_frequency(a):
    G = NativeGroup(2)
    states = [G.supplied_phase_state((a,),(s,)) for s in ring_words(2)]
    effects = [3/len(states)*np.outer(psi,psi.conj()) for psi in states]
    assert np.allclose(sum(effects),np.eye(3),atol=2e-12)
    success = sum(np.vdot(psi,E@psi).real for psi,E in zip(states,effects))/len(states)
    assert np.isclose(success,3/len(states))


@pytest.mark.parametrize("r,n,m", [(2,1,3),(8,8,64),(32,32,1024),(128,128,16384)])
def test_information_bound_counts_actual_secret_prior_not_nominal_original_copy_count(r,n,m):
    ledger = information_ledger(r,n,m)
    assert ledger["simulating_original_native_source_copies"] == 1
    assert ledger["uniform_full_ring_secret_success_upper_bound"] == {"cap":1,"numerator":3,"denominator":{"base":3,"exponent":r*n}}
    assert ledger["uniform_integer_embedded_secret_success_upper_bound"]["denominator"]["exponent"] == n*((r+1)//2)
    assert ledger["simulation_requires_full_uniform_IID_frequency_prior"]
    assert ledger["joint_original_input_trace_distance_error_adds_to_raw_bound"]
    assert not ledger["arbitrary_seed_mixing_or_independent_per_copy_actions_covered"]


@pytest.mark.parametrize("word", [(),(False,),(3,),(-1,)])
def test_invalid_source_word_rejected(word):
    with pytest.raises(ValueError):
        orbit_chart(word)


def test_no_conditional_branch_or_invalid_copy_model_granted():
    with pytest.raises(ValueError):
        synthetic_rows(((1,0),),(0,1),(),2)
    with pytest.raises(ValueError):
        effective_label((((1,0),),),(1,),2)
    with pytest.raises(ValueError):
        information_ledger(4,1,False)


def replay(report,tmp_path):
    f=tmp_path/"channel.json"
    f.write_text(json.dumps(report,allow_nan=False))
    return subprocess.run(["node",str(ROOT/"research/certificates/native_diagonal_orbit_channel_crosscheck.js"),str(f)],capture_output=True,text=True)


def test_independent_exact_channel_and_full_density_replay(report,tmp_path):
    result = replay(report,tmp_path)
    assert result.returncode == 0,result.stderr
    checked = json.loads(result.stdout)
    assert checked["exact_original_word_phase_identities"] == 162
    assert checked["exact_induced_action_intertwiners"] == 1782
    assert checked["exact_full_group_density_entries"] == 972
    assert checked["seed_mixing_escape_preserved"]


@pytest.mark.parametrize("mutation", ["phase","offset","missing_branch","weight","density","simulation_access","fixed_prior","general_cut","secret_prior","escape"])
def test_independent_checker_rejects_forged_factorization_and_receiver_claims(report,mutation,tmp_path):
    bad = deepcopy(report)
    c=bad["complete_source_controls"][0]
    if mutation == "phase":
        c["complete_orbit_branches"][0]["exact_original_word_phases_mod1"][0] = "1/3"
    elif mutation == "offset":
        c["complete_orbit_branches"][0]["offset"] = (0,0,1)
    elif mutation == "missing_branch":
        c["complete_orbit_branches"].pop()
    elif mutation == "weight":
        c["complete_orbit_branches"][0]["exact_orbit_weight"] = "1"
    elif mutation == "density":
        c["actual_label_dependent_group_protocol"]["full_output_group_density_real_imag_by_round"][0][0][0][0] = 1
    elif mutation == "simulation_access":
        c["simulation_global_phase_or_secret_is_an_algorithm_input"] = True
    elif mutation == "fixed_prior":
        bad["simulation_is_valid_for_arbitrary_fixed_frequency_prior"] = True
    elif mutation == "general_cut":
        bad["all_native_quantum_receivers_ruled_out"] = True
    elif mutation == "secret_prior":
        bad["growing_information_ledgers"][0]["uniform_integer_embedded_secret_success_upper_bound"]["denominator"]["exponent"] = 0
    else:
        c["seed_mixing_escape"]["orbit_pinched_batch_all_plus_measurement_probability"] = 1
    assert replay(bad,tmp_path).returncode != 0
