"""Distinguish actual quantum channels from classical Fourier coefficients."""
from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import subprocess

import numpy as np
import pytest

from theorems.planted_qary_noisy_parity_check_likelihood_bridge import (
    build_planted_qary_noisy_parity_check_likelihood_bridge,
    evaluate_noisy_parity_check_case, evaluate_quantum_source_control, source_geometry,
)

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "research/certificates/planted_qary_noisy_parity_check_likelihood_bridge_crosscheck.js"


@pytest.fixture(scope="module")
def report():
    return build_planted_qary_noisy_parity_check_likelihood_bridge()


def test_the_original_translation_claim_has_an_exact_counterexample():
    c = evaluate_quantum_source_control(q=3, n=2, generator_matrix=[[1, 0]], gamma_num=1, gamma_den=2)
    i = c["vector_order"].index([1, 0])
    x, xz, classical = c["modes"].values()
    assert Fraction(x["target_probabilities_exact"][i]) == 0
    assert Fraction(xz["target_probabilities_exact"][i]) == Fraction(1, 18)
    assert Fraction(xz["outside_dual_mass_exact"]) == Fraction(1, 3)
    assert Fraction(classical["outside_dual_mass_exact"]) == Fraction(2, 3)
    assert c["same_computational_marginal_for_all_three_sources"]
    assert not c["translation_only_equals_claimed_phase_convolution"]


@pytest.mark.parametrize("q,n,M", [(2, 3, [[1, 0, 1], [0, 1, 1]]), (3, 2, [[1, 1]]), (5, 2, [[1, 2]])])
@pytest.mark.parametrize("gamma", [Fraction(0), Fraction(2, 5), Fraction(1)])
def test_independent_Kraus_density_replay(q, n, M, gamma):
    _, V, B, dual = source_geometry(q, n, M, cap=128)
    N = len(V)
    psi = np.array([complex(1/np.sqrt(len(B))) if x in B else 0 for x in V])
    clean = np.outer(psi, psi.conj())
    p0, p1 = 1-Fraction(q-1, q)*gamma, gamma/q
    noise = [float(p0**(n-sum(a != 0 for a in e))*p1**sum(a != 0 for a in e)) for e in V]
    rho = np.zeros_like(clean)
    for e, pe in zip(V, noise):
        permutation = [V.index(tuple((x[j]-e[j]) % q for j in range(n))) for x in V]
        rho += pe*clean[np.ix_(permutation, permutation)]
    phased = np.zeros_like(clean)
    for f, pf in zip(V, noise):
        Z = np.diag([np.exp(2j*np.pi*sum(a*b for a, b in zip(f, x))/q) for x in V])
        phased += pf*(Z @ rho @ Z.conj().T)
    F = np.array([[np.exp(2j*np.pi*sum(a*b for a,b in zip(u, x))/q)/np.sqrt(N) for x in V] for u in V])
    c = evaluate_quantum_source_control(q=q, n=n, generator_matrix=M, gamma_num=gamma.numerator, gamma_den=gamma.denominator)
    for name, matrix in zip(c["modes"], (rho, phased, np.diag(np.diag(rho)))):
        assert np.linalg.eigvalsh(matrix).min() > -1e-13
        assert np.trace(matrix) == pytest.approx(1)
        probabilities = np.diag(F@matrix@F.conj().T).real
        assert np.allclose(probabilities, c["modes"][name]["Born_probabilities"], atol=1e-13)
        assert np.allclose(np.diag(matrix), np.diag(rho), atol=1e-13)
    assert c["all_physical_laws_verified"]


def test_arbitrary_correlated_translation_preserves_dual_support():
    q, n = 3, 3
    _, V, B, dual = source_geometry(q, n, [[1, 1, 0], [0, 1, 1]], cap=128)
    F = np.array([[np.exp(2j*np.pi*sum(a*b for a,b in zip(u, x))/q)/np.sqrt(len(V)) for x in V] for u in V])
    # Neither product noise nor independent coordinates are needed for translation.
    for e in ((0, 0, 0), (1, 1, 1), (2, 1, 0)):
        psi = np.array([1/np.sqrt(len(B)) if tuple((x[j]-e[j]) % q for j in range(n)) in B else 0 for x in V])
        assert np.allclose(np.abs(F@psi)**2, [1/len(dual) if u in dual else 0 for u in V], atol=1e-13)


def test_a_classical_random_seed_kept_as_garbage_destroys_coset_coherence():
    # Reversible copying of b to an output does not erase the sampler's b register.
    B = [0, 2, 4]
    purification = np.zeros((3, 9), complex)
    for i, b in enumerate(B):
        purification[i, b] = 1/np.sqrt(len(B))
    rho = purification.T @ purification.conj()
    F = np.exp(2j*np.pi*np.outer(np.arange(9), np.arange(9))/9)/3
    assert np.allclose(np.diag(F@rho@F.conj().T).real, 1/9)
    coherent = np.zeros(9, complex)
    coherent[B] = 1/np.sqrt(len(B))
    assert not np.allclose(np.abs(F@coherent)**2, 1/9)


def test_full_noise_keeps_classical_marginal_uniform_but_not_quantum_readout(report):
    for c in report["quantum_source_controls"]:
        assert not c["coherent_state_preparation_from_classical_samples_supplied"]
        assert not c["scalable_state_preparation"]
        if Fraction(c["gamma_exact"]) == 1:
            x, xz, classical = c["modes"].values()
            assert Fraction(x["outside_dual_mass_exact"]) == 0
            assert np.allclose(xz["Born_probabilities"], classical["Born_probabilities"])
            assert not np.allclose(x["Born_probabilities"], classical["Born_probabilities"])


def test_empty_full_windows_and_full_subspace_do_not_claim_a_nonzero_dual():
    for window in ([], [0, 1], [1]):
        c = evaluate_noisy_parity_check_case(case_id="full", q=2, n=2,
            generator_matrix=[[1, 0], [0, 1]], gamma_num=1, gamma_den=2, window=window)
        assert c["dual_minimum_distance_d_perp"] is None
        assert not c["nonzero_dual_exists"]
        assert Fraction(c["max_nonzero_probe_bias_exact"]) == 0
        assert c["all_theorems_verified"]


@pytest.mark.parametrize("override", [
    {"q": 4}, {"q": True}, {"gamma_num": -1}, {"gamma_num": 3},
    {"gamma_den": 0}, {"n": 9}, {"generator_matrix": [[0, 0]]},
    {"generator_matrix": [[1.0, 0]]}, {"generator_matrix": [[1]]},
])
def test_unsupported_fields_sources_and_rates_fail_closed(override):
    args = dict(q=3, n=2, generator_matrix=[[1, 0]], gamma_num=1, gamma_den=2)
    with pytest.raises(ValueError):
        evaluate_quantum_source_control(**(args | override))


@pytest.mark.parametrize("window", [[1, 1], [-1], [3]])
def test_window_is_a_set_of_canonical_field_elements(window):
    with pytest.raises(ValueError, match="window"):
        evaluate_noisy_parity_check_case(case_id="invalid", q=3, n=2,
            generator_matrix=[[1, 0]], gamma_num=1, gamma_den=2, window=window)


def test_live_artifact_and_independent_Born_replay(report):
    artifact = ROOT / "research/reductions/planted_qary_noisy_parity_check_likelihood_bridge.json"
    assert json.loads(artifact.read_text()) == report
    result = subprocess.run(["node", str(CHECKER)], capture_output=True, text=True, check=True)
    assert json.loads(result.stdout)["quantum_source_control_count"] == 9


@pytest.mark.parametrize("forgery", ["translation_is_phase_noise", "source_grant", "classical_coherence", "subspace", "phase_purity"])
def test_crosscheck_rejects_physically_wrong_artifacts_even_with_green_flags(report, tmp_path, forgery):
    altered = deepcopy(report)
    c = altered["quantum_source_controls"][1]
    if forgery == "translation_is_phase_noise":
        c["modes"]["coherent_random_translation"] = deepcopy(c["modes"]["coherent_translation_and_phase_noise"])
    elif forgery == "source_grant":
        c["coherent_state_preparation_from_classical_samples_supplied"] = True
    elif forgery == "classical_coherence":
        c["modes"]["incoherent_classical_samples"] = deepcopy(c["modes"]["coherent_random_translation"])
    elif forgery == "subspace":
        c["generator_matrix"] = [[1, 1]]
    else:
        c["modes"]["coherent_translation_and_phase_noise"]["purity"] += 0.1
    file = tmp_path / "forged.json"
    file.write_text(json.dumps(altered))
    result = subprocess.run(["node", str(CHECKER), str(file)], capture_output=True, text=True)
    assert result.returncode != 0
