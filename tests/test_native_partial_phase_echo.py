from dataclasses import replace
from itertools import product
import json
import random
import subprocess

import numpy as np
import pytest

from native_partial_phase_echo import (
    EchoFamily, F3, REPORT, ROOT, adapted_coupling, bounded_score,
    local_product_probabilities, randomized_local_baseline,
)
from ternary_covariant_noise import phase


def family(q=9, n=1, m=3, w=1, seed=19):
    rng = random.Random(seed)
    return EchoFamily(
        tuple(tuple(rng.randrange(q) for _ in range(n)) for _ in range(m)),
        tuple(tuple(rng.randrange(q) for _ in range(n)) for _ in range(m)),
        q, w, tuple(tuple(rng.randrange(q) for _ in range(n)) for _ in range(n)),
        tuple(tuple(rng.randrange(q) for _ in range(2)) for _ in range(m)),
    )


@pytest.mark.parametrize("q,n,m,w", [(3,1,2,1), (9,1,3,1), (3,2,3,2), (9,2,3,1)])
def test_streaming_likelihood_matches_complete_physical_circuit(q,n,m,w):
    f = family(q,n,m,w)
    words = tuple(product(range(3), repeat=m))
    for secret in product(range(q), repeat=n):
        replay = f.dense_output(secret)
        assert np.allclose([f.amplitude(secret, out) for out in words], replay, atol=2e-13)
        assert np.isclose(np.vdot(replay,replay),1,atol=2e-13)


@pytest.mark.parametrize("q,n", [(3,1),(9,1),(3,2)])
def test_zero_coupling_is_product_measurement_and_same_copy_baseline(q,n):
    f = replace(family(q,n),coupling=tuple((0,)*n for _ in range(n)))
    secrets = tuple(product(range(q),repeat=n))
    P = local_product_probabilities(f,secrets,0,f.copies)
    assert np.allclose(P,[abs(f.dense_output(s))**2 for s in secrets],atol=2e-13)
    score = bounded_score(f)
    local = randomized_local_baseline(f)
    assert np.isclose(score["full_uniform_secret_MAP_success_numeric_reference"],local["full_uniform_secret_MAP_success_numeric_reference"])
    assert np.isclose(score["least_trit_MAP_success_numeric_reference"],local["least_trit_MAP_success_numeric_reference"])


def scratch_replay(f,s,word_tag=False):
    """Attach a real orthogonal scratch tag, replay gates, trace it out."""
    A = tuple(product(range(3),repeat=f.main_width))
    B = tuple(product(range(3),repeat=f.mediator_width))
    tags = {b:(b if word_tag else f.frequency(b,f.main_width)) for b in B}
    values = tuple(sorted(set(tags.values())))
    amplitudes = np.zeros((len(A),len(B),len(values)),complex)
    for ia,a in enumerate(A):
        for ib,b in enumerate(B):
            word = a+b
            exponent = sum(x*y for x,y in zip(s,f.frequency(word)))-f.setting_phase(word)
            exponent += f.bilinear(f.frequency(a),f.frequency(b,f.main_width))
            amplitudes[ia,ib,values.index(tags[b])] = phase(exponent,f.modulus)/np.sqrt(3**f.copies)
    U_A = F3
    for _ in range(f.main_width-1):
        U_A = np.kron(U_A,F3)
    U_B = F3
    for _ in range(f.mediator_width-1):
        U_B = np.kron(U_B,F3)
    amplitudes = np.einsum("ij,jbt->ibt",U_A,amplitudes)
    for ia,a in enumerate(A):
        for ib,b in enumerate(B):
            amplitudes[ia,ib] *= phase(-f.bilinear(f.frequency(a),f.frequency(b,f.main_width)),f.modulus)
    amplitudes = np.einsum("ij,ajt->ait",U_B,amplitudes)
    return (abs(amplitudes)**2).sum(axis=2).ravel(),len(values)


@pytest.mark.parametrize("collision", [False,True])
def test_dirty_frequency_scratch_preserves_collisions_and_is_not_word_dephasing(collision):
    f = family(9,1,4,2)
    if collision:
        f = replace(f,first=f.first[:2]+((0,),(0,)),second=f.second[:2]+((0,),(0,)),
                    local_settings=f.local_settings[:2]+((0,0),(0,0)))
    secrets = tuple((s,) for s in range(9))
    dirty,word = [],[]
    for s in secrets:
        d,R = scratch_replay(f,s)
        z,_ = scratch_replay(f,s,word_tag=True)
        clean = abs(f.dense_output(s))**2
        assert np.isclose(sum(d),1)
        assert np.all(clean<=R*d+2e-13)
        dirty.append(d)
        word.append(z)
        if collision:
            assert R==1
            assert np.allclose(clean,d)
            assert not np.allclose(d,z)
    baseline = randomized_local_baseline(f)
    assert np.isclose(np.array(dirty).max(axis=0).sum()/9,baseline["dirty_echo_with_unerased_F_B_scratch_MAP_success"])
    assert np.isclose(np.array(word).max(axis=0).sum()/9,baseline["dirty_echo_with_a_full_B_WORD_tag_MAP_success"])
    assert baseline["dirty_echo_with_unerased_F_B_scratch_MAP_success"] <= baseline["randomized_A_only_with_y_recorded_MAP_success"]+2e-13
    assert baseline["randomized_A_only_with_y_recorded_MAP_success"] <= baseline["full_uniform_secret_MAP_success_numeric_reference"]+2e-13


@pytest.mark.parametrize("q", [3,9,27,81])
def test_original_even_native_source_reconstruction_and_clean_resource_ledger(q):
    f = family(q,2)
    assert f.native_source().frequencies==tuple(zip(f.first,f.second))
    recipe = f.recipe()
    assert recipe["full_frequency_scratch_cleared_BEFORE_mediator_Fourier"]
    assert not recipe["unknown_source_preparation_inverse_used"]
    assert not recipe["fiber_count_rank_unrank_oracle_used"]
    assert recipe["original_native_source_copies"]==f.copies


@pytest.mark.parametrize("q", [9,27,81])
def test_full_label_calibration_inverts_composite_modulus_without_rejection(q):
    rows = ((3,0),(2,1),(1,2),(0,1))
    K,ledger = adapted_coupling(rows,q,4)
    assert ledger["pivot_indices"]==[1,3]
    assert ledger["full_A_labels_used_in_coupling"]
    assert not ledger["shifted_probe_Gram_bound_for_A_independent_couplings_applies"]
    V = [rows[i] for i in ledger["pivot_indices"]]
    assert tuple(tuple(sum(V[i][k]*K[k][j] for k in range(2))%q for j in range(2)) for i in range(2))==((1,0),(0,1))
    K,ledger = adapted_coupling(((1,0),(2,0)),q,2)
    assert K==((0,0),(0,0))
    assert not ledger["full_mod3_rank"]
    assert ledger["rank_failure_returns_product_readout_without_source_rejection"]


def test_complete_reference_budget_failures_do_not_return_partial_scores():
    f = family(9,2,4,1)
    with pytest.raises(ValueError,match="complete"):
        bounded_score(f,secret_budget=80)
    with pytest.raises(ValueError,match="complete"):
        randomized_local_baseline(f,word_budget=80)
    with pytest.raises(ValueError,match="complete"):
        f.dense_output((0,0),word_budget=80)


def test_live_controls_remain_negative_and_do_not_claim_decoder_or_speedup():
    report = json.loads(REPORT.read_text())
    assert len(report["cohort_controls"])==12
    for cohort in report["cohort_controls"]:
        assert cohort["best_echo_minus_best_matched_product_score"]<0
        assert cohort["best_echo_minus_best_stronger_LOCC_score"]<0
        assert cohort["best_echo_minus_best_product_LEAST_TRIT_score"]<0
        for r in cohort["receiver_records"]:
            assert not r["score"]["efficient_unknown_secret_decoder_supplied"]
            if r["receiver_policy"]!="product":
                assert r["full_secret_echo_minus_OWN_matched_LOCC"]<0
                assert r["least_trit_echo_minus_OWN_matched_LOCC"]<0
    assert not report["polynomial_secret_search_follows_from_fast_likelihood"]
    assert not report["new_algorithmic_speedup_claimed"]


def test_independent_exact_cyclotomic_control():
    result = subprocess.run(["node",str(ROOT/"research/certificates/native_partial_phase_echo_crosscheck.js")],capture_output=True,text=True,check=True)
    out = json.loads(result.stdout)
    assert out["exactProbabilities"]==1944
    assert out["exactWinnerChecks"]==1944
    assert out["dominationChecks"]==1944


@pytest.mark.parametrize("tamper", ["speedup","decoder","winner","dirty_score"])
def test_independent_checker_rejects_unearned_claims_and_false_scores(tmp_path,tamper):
    report = json.loads(REPORT.read_text())
    receiver = report["exact_checker_control"]["receiver_records"][0]
    if tamper=="speedup":
        report["new_algorithmic_speedup_claimed"] = True
    elif tamper=="decoder":
        receiver["score"]["efficient_unknown_secret_decoder_supplied"] = True
    elif tamper=="winner":
        receiver["score"]["full_secret_MAP_winner_indices_by_outcome"][0] = -1
    else:
        receiver["matched_randomized_local_baseline"]["dirty_echo_with_unerased_F_B_scratch_MAP_success"] += .01
    path = tmp_path/"tampered.json"
    path.write_text(json.dumps(report))
    result = subprocess.run(["node",str(ROOT/"research/certificates/native_partial_phase_echo_crosscheck.js"),str(path)],capture_output=True,text=True)
    assert result.returncode!=0


def test_gram_background_is_actual_positive_normalized_dephased_A_channel():
    f = family(9,1,3,1)
    A = tuple(product(range(3),repeat=2))
    B = tuple(product(range(3),repeat=1))
    words = tuple(a+b for a in A for b in B)
    FA = [f.frequency(a)[0] for a in A]
    FB = [f.frequency(b,2)[0] for b in B]
    K = f.coupling[0][0]
    chirp = np.diag([phase(K*x*y,9) for x in FA for y in FB])
    U = np.kron(np.eye(9),F3)@chirp.conj()@np.kron(np.kron(F3,F3),np.eye(3))@chirp
    for s in range(9):
        psi = np.array([phase(s*f.frequency(w)[0]-f.setting_phase(w),9) for w in words])/np.sqrt(27)
        rho = np.outer(psi,psi.conj())
        for i in range(27):
            for j in range(27):
                if i//3!=j//3:
                    rho[i,j]=0
        measured = np.diag(U@rho@U.conj().T).real
        background = []
        for ia,a in enumerate(A):
            for b in B:
                density = 0j
                for iy,y in enumerate(B):
                    for iz,z in enumerate(B):
                        diff = FB[iy]-FB[iz]
                        C = np.prod([(1+phase(K*diff*f.first[i][0],9)+phase(K*diff*f.second[i][0],9))/3 for i in range(2)])
                        density += C*phase((s-K*FA[ia])*diff-f.setting_phase(y,2)+f.setting_phase(z,2),9)*phase(-b[0]*(y[0]-z[0]),3)/3
                background.append(density/27)
        assert np.allclose(background,measured,atol=2e-13)
        assert measured.min()>-2e-13
        assert np.isclose(sum(measured),1)
