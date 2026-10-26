from collections import Counter
from fractions import Fraction as Q
import json

import numpy as np
import pytest

from theorems import chain_support_budget as work


@pytest.mark.parametrize("M", range(1, 9))
def test_counts_and_directed_flips_against_every_bit_string(M):
    observed, flips = Counter(), {}
    for word in range(1 << M):
        d, r, c = work.signature(word, M)
        assert c == sum(bool(word & ((1 << j) | (1 << (j-1)) if j else 1)) for j in range(M+1))
        observed[d, r] += 1
        counter = flips.setdefault((d, r), Counter())
        for i in range(M):
            if not word & (1 << i):
                counter[work.signature(word | (1 << i), M)[:2]] += 1
    assert work.counts(M, M+1) == observed
    for state in observed:
        assert work.additions(M, state) == flips[state]
    for K in range(M+2):
        assert work.counts(M, K) == {s: n for s, n in observed.items() if sum(s) <= K}


def full_operator(M, rho):
    matrix = np.diag([float(M*rho+(1-2*rho)*w.bit_count()) for w in range(1 << M)])
    for word in range(1 << M):
        for i in range(M):
            matrix[word, word ^ (1 << i)] = np.sqrt(float(rho*(1-rho)))
    return matrix


def test_compression_and_exact_rational_rayleigh():
    M, K, rho = 7, 5, Q(2, 5)
    states, matrix = work.ritz_matrix(M, K, rho)
    sizes = work.counts(M, K)
    embedding = np.zeros((1 << M, len(states)))
    coefficients = {s: Q(i+1, 11) for i, s in enumerate(states)}
    state_vector = np.zeros(1 << M)
    variance = float(rho*(1-rho))
    for w in range(1 << M):
        state = work.signature(w, M)[:2]
        if state in sizes:
            embedding[w, states.index(state)] = 1/np.sqrt(sizes[state])
            state_vector[w] = float(coefficients[state])*variance**(state[0]/2)
    operator = full_operator(M, rho)
    np.testing.assert_allclose(matrix.toarray(), embedding.T @ operator @ embedding, atol=1e-13)
    norm, mean = work.rayleigh(M, K, rho, coefficients)
    assert float(norm) == pytest.approx(state_vector @ state_vector)
    assert float(mean) == pytest.approx(state_vector @ operator @ state_vector / float(norm))
    # Leakage invalidates using the compressed matrix squared as a second moment.
    gap = embedding.T @ operator @ operator @ embedding - matrix.toarray() @ matrix.toarray()
    assert np.linalg.eigvalsh(gap)[-1] > .1


def test_old_radial_space_is_contained_in_degree_run_space():
    M, D, rho = 11, 3, Q(3, 7)
    radial = (Q(1), Q(2), Q(3), Q(4))
    coefficients = {s: radial[s[0]] for s in work.counts(M, 2*D) if s[0] <= D}
    norm, mean = work.rayleigh(M, 2*D, rho, coefficients)
    expected_norm, expected_mean, _ = work.exact_moments(radial, M, rho)
    assert (norm, mean) == (expected_norm, expected_mean)


def test_overlapping_edge_products_have_bounded_fourier_support_but_interfere():
    p, M, rho = 5, 3, Q(2, 5)
    tables = ({0, 1}, {1, 3}, {0, 4})
    values = np.indices((p,)*(M+1))
    centered = [np.isin((values[i+1]+(i+1)*values[i]**2) % p, list(tables[i]))-float(rho)
                for i in range(M)]
    for word in range(1 << M):
        array = np.ones((p,)*(M+1))
        for i in range(M):
            if word & (1 << i):
                array *= centered[i]
        transformed = np.fft.fftn(array, norm="ortho")
        cost = work.signature(word, M)[2]
        forbidden = np.count_nonzero(values, axis=0) > cost
        assert np.max(np.abs(transformed[forbidden]), initial=0.) < 1e-12
    a = np.fft.fftn(centered[0]*centered[2], norm="ortho")
    b = np.fft.fftn(centered[0]*centered[1]*centered[2], norm="ortho")
    assert np.max(np.abs(abs(a+b)**2-abs(a)**2-abs(b)**2)) > .01


def test_cluster_upper_on_full_small_feasible_subspace():
    M, K, rho = 7, 4, Q(1, 2)
    certificate = work.cluster_certificate(M, K, rho)
    words = [w for w in range(1 << M) if work.signature(w, M)[2] <= K]
    actual = np.linalg.eigvalsh(full_operator(M, rho)[np.ix_(words, words)])[-1]/M
    assert actual < float(Q(certificate["score_fraction_upper_exact"]))
    assert work.verify_cluster(certificate)
    corrupt = dict(certificate)
    corrupt["score_fraction_upper_exact"] = "0"
    with pytest.raises(ValueError, match="corrupt"):
        work.verify_cluster(corrupt)
    with pytest.raises(ValueError, match="positive-definiteness"):
        work.cluster_certificate(M, K, rho, upper=Q(0))


def test_periodic_window_identity_and_path_cost_domination():
    M, block, rho, penalty = 7, 4, Q(1026, 2053), Q(8, 5)
    local = work.local_matrix(rho, block, penalty)
    for w in range(1 << M):
        bits = [(w >> i) & 1 for i in range(M)]
        cyclic_cost = 2*sum(bits)-sum(bits[i]*bits[(i+1) % M] for i in range(M))
        assert cyclic_cost <= work.signature(w, M)[2]
        diagonal = sum(local[sum(bits[(s+j) % M] << j for j in range(block))]
                             [sum(bits[(s+j) % M] << j for j in range(block))]
                       for s in range(M))
        assert diagonal == (1-2*rho)*sum(bits)-penalty*cyclic_cost
        assert sum(Q(1, 2*block) for _ in range(block)) == Q(1, 2)


def test_budget_checks_and_proposed_guide():
    assert work.transfer(205, 100, 2)["vertex_independence_required"] == 204
    with pytest.raises(ValueError, match="independence"):
        work.transfer(201, 100)
    with pytest.raises(ValueError, match="budget"):
        work.rayleigh(7, 2, Q(1, 2), {(2, 1): Q(1)})
    coefficients = work.propose(20, 8, Q(2, 5))
    _, mean = work.rayleigh(20, 8, Q(2, 5), coefficients)
    assert 8 < mean < 20
    assert work.propose(2, 1, Q(1, 2)) == {(0, 0): Q(1)}


def test_saved_native_scope_and_replay():
    report = json.loads(work.REPORT.read_text())
    assert report["producer_sha256"] == work.hashlib.sha256(work.Path(work.__file__).read_bytes()).hexdigest()
    assert not report["speedup_claim_admitted"]
    assert not report["quantum_algorithm_executed"]
    coefficients = {(a["degree"], a["runs"]): Q(a["value"]) for a in report["guide"]["coefficients"]}
    norm, mean = work.rayleigh(2051, 100, Q(1026, 2053), coefficients)
    assert str(norm) == report["guide"]["norm"]
    assert str(mean/2051) == report["guide"]["score_fraction_exact"]
    assert .6439 < float(mean/2051) < .644
    assert 0 < float(Q(report["guide"]["gain_fraction_exact"])) < .001
    assert work.verify_cluster(report["upper_certificate"])
    assert float(Q(report["upper_certificate"]["score_fraction_upper_exact"])) < .65538
    extra = report["mean_only_budget"]
    coefficients = {(a["degree"], a["runs"]): Q(a["value"]) for a in extra["coefficients"]}
    norm, mean = work.rayleigh(2051, 101, Q(1026, 2053), coefficients)
    assert str(norm) == extra["norm"]
    assert str(mean/2051) == extra["score_fraction_exact"]
    assert not extra["second_moment_certified"]
    with pytest.raises(ValueError, match="independence"):
        work.transfer(205, 101, 2)
    assert work.verify_cluster(extra["upper_certificate"])
    assert float(Q(extra["upper_certificate"]["score_fraction_upper_exact"])) < .65616
