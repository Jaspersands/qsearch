"""Physical codomain instruments and a shared-oracle correlation audit.

LOCAL DERIVATION / REVIEW PENDING. Bounded tables are physical regression
controls, not algorithm candidates. No general DHSP query lower bound.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from itertools import combinations
from math import comb, isqrt
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/dhsp_codomain_instrument.json"


def rational(x):
    x = Fraction(x)
    return {"numerator": str(x.numerator), "denominator": str(x.denominator)}


def _integer(x, name, minimum=1):
    if type(x) is not int or x < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


def _source(N, K):
    _integer(N, "rotation order", 2)
    _integer(K, "hash bins")
    if N & (N - 1) or K > N or N % K:
        raise ValueError("power-of-two rotation order and dividing balanced hash required")


def probability(p):
    if not isinstance(p, (list, tuple)) or not p:
        raise ValueError("nonempty exact probability vector required")
    if any(type(x) not in (int, Fraction) or x < 0 for x in p):
        raise ValueError("nonnegative exact probabilities required")
    p = tuple(map(Fraction, p))
    if sum(p) != 1:
        raise ValueError("probabilities must sum to one")
    return p


def instrument(p):
    """Unnormalized H/F blocks; discard failed domain, retain full hash state."""
    p = probability(p)
    K = len(p)
    out = [[Fraction(0) for _ in range(2*K)] for _ in range(2*K)]
    for i in range(K):
        for j in range(K):
            out[i][j] = p[i]*p[j]
            out[K+i][K+j] = (p[i] if i == j else 0) - p[i]*p[j]
    return out


def classical_collision_records(p):
    """Two domain samples: tag equality and output the FIRST sample's hash."""
    p = probability(p)
    return tuple(p[i]**2 for i in range(len(p))) + tuple(p[i]*(1-p[i]) for i in range(len(p)))


def three_outcomes(p):
    p = probability(p)
    h = sum(x*x for x in p)
    return (1-h, Fraction(1, len(p)), h-Fraction(1, len(p)))


def oracle_table(N, shift, permutation, epsilon):
    """f(b,x)=pi(x-b*s), restricted to x=2j+epsilon*b."""
    _source(N, 1)
    if N > 64:
        raise ValueError("literal oracle tables are bounded calibration only")
    if type(shift) is not int or not 0 <= shift < N:
        raise ValueError("canonical shift required")
    if type(epsilon) is not int or epsilon not in (0, 1):
        raise ValueError("subgroup parity required")
    if not isinstance(permutation, (tuple, list)) or any(type(x) is not int for x in permutation) or sorted(permutation) != list(range(N)):
        raise ValueError("output permutation required")
    return [permutation[(2*j+epsilon*b-b*shift) % N] for b in range(2) for j in range(N//2)]


def physical_control(values, hash_map, K):
    """Literal query/hash/query-inverse, then a binary uniform-domain projection."""
    _integer(K, "hash bins")
    if K > 64:
        raise ValueError("literal hash matrices are bounded calibration only")
    if not isinstance(values, (tuple, list)) or not values or len(values) > 64:
        raise ValueError("bounded nonempty oracle table required")
    if not isinstance(hash_map, (tuple, list)) or not hash_map or len(hash_map) > 64:
        raise ValueError("bounded public hash table required")
    if any(type(v) is not int or not 0 <= v < len(hash_map) for v in values) or any(type(w) is not int or not 0 <= w < K for w in hash_map):
        raise ValueError("canonical function and hash outputs required")
    D, M = len(values), len(hash_map)
    # XOR evaluation is its own inverse; it is NOT an inverse-function oracle.
    L = 1 << (M-1).bit_length()
    state = np.zeros((D, L, K), dtype=complex)
    state[:, 0, 0] = 1/np.sqrt(D)
    queried = np.empty_like(state)
    for a, v in enumerate(values):
        queried[a] = state[a, np.arange(L) ^ v]
    hashed = np.zeros_like(state)
    for v in range(L):
        # A reversible modular-add hash evaluation, extended arbitrarily off range.
        w = hash_map[v] if v < M else 0
        hashed[:, v] = np.roll(queried[:, v], w, axis=1)
    discarded = np.einsum("avw,avz->wz", hashed, hashed.conj())
    erased = np.empty_like(state)
    for a, v in enumerate(values):
        erased[a] = hashed[a, np.arange(L) ^ v]
    assert np.max(np.abs(erased[:, 1:])) < 1e-12
    amplitudes = erased[:, 0]
    uniform_domain = np.ones(D)/np.sqrt(D)
    herald_vector = uniform_domain @ amplitudes
    failed = amplitudes - np.outer(uniform_domain, herald_vector)
    H = np.outer(herald_vector, herald_vector.conj())
    F = failed.T @ failed.conj()
    sigma = np.zeros((2*K, 2*K), dtype=complex)
    sigma[:K, :K], sigma[K:, K:] = H, F
    counts = [sum(hash_map[v] == w for v in values) for w in range(K)]
    p = tuple(Fraction(c, D) for c in counts)
    expected = np.array(instrument(p), dtype=float)
    flat = np.ones(K)/np.sqrt(K)
    return {
        "domain_size": D, "hash_bins": K, "oracle_queries": 2,
        "histogram": [rational(x) for x in p],
        "state": sigma.real.tolist(), "discarded_state": discarded.real.tolist(),
        "instrument_residual": float(np.max(np.abs(sigma-expected))),
        "discarded_diagonal_residual": float(np.max(np.abs(discarded-np.diag(list(map(float, p)))))),
        "herald_vector_residual": float(np.max(np.abs(herald_vector-np.array(p, dtype=float)))),
        "minimum_state_eigenvalue": float(np.linalg.eigvalsh(sigma).min()),
        "trace": float(np.trace(sigma).real),
        "unconditional_herald_flat": float((flat @ H @ flat).real),
        "all_failure_hash_outputs_retained": True,
        "failed_domain_register_retained": False,
    }


def balanced_histogram(N, K, subset):
    _source(N, K)
    if N > 64 or not isinstance(subset, (tuple, list)) or len(subset) != N//2 or len(set(subset)) != len(subset) or any(type(v) is not int or not 0 <= v < N for v in subset):
        raise ValueError("bounded distinct half-range subset required")
    return tuple(Fraction(2*sum(v % K == w for v in subset), N) for w in range(K))


def one_copy_moments(N, K):
    _source(N, K)
    u = Fraction(1, K)
    covariance = [[Fraction(int(i == j), K*(N-1))-Fraction(1, K*K*(N-1)) for j in range(K)] for i in range(K)] if K <= 64 else None
    return {"mean_coordinate": u, "covariance": covariance,
            "mean_squared_deviation": Fraction(K-1, K*(N-1)),
            "one_copy_averaged_trace_distance": Fraction(K-1, K*(N-1))}


def _kron(A, B):
    return [[a*b for a in rowA for b in rowB] for rowA in A for rowB in B]


def _rotated_instrument(d):
    # Basis: H,U; H,V; F,U; F,V. F,U is the identically empty subspace.
    z = Fraction(0)
    return [[Fraction(1, 2), d, z, z], [d, 2*d*d, z, z],
            [z, z, z, z], [z, z, z, Fraction(1, 2)-2*d*d]]


def shared_two_copy_control(N=8):
    _source(N, 2)
    if N > 256:
        raise ValueError("two-copy exact matrices are bounded calibration only")
    size = 16
    mean = [[Fraction(0) for _ in range(4)] for _ in range(4)]
    shared = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    moments = [Fraction(0) for _ in range(5)]
    law = []
    for c in range(N//2+1):
        weight = Fraction(comb(N//2, c)**2, comb(N, N//2))
        d = Fraction(2*c, N)-Fraction(1, 2)
        single = _rotated_instrument(d)
        pair = _kron(single, single)
        for power in range(5):
            moments[power] += weight*d**power
        for i in range(4):
            for j in range(4):
                mean[i][j] += weight*single[i][j]
        for i in range(size):
            for j in range(size):
                shared[i][j] += weight*pair[i][j]
        law.append({"count": c, "probability": rational(weight), "deviation": rational(d)})
    wrong = _kron(_rotated_instrument(Fraction(0)), _rotated_instrument(Fraction(0)))
    independent = _kron(mean, mean)
    difference = [[shared[i][j]-wrong[i][j] for j in range(size)] for i in range(size)]
    # Known measurement: HH (UU-VV)/sqrt2, HF U,V, FH V,U, FF V,V.
    event_difference = (difference[0][0]+difference[5][5]-difference[0][5]-difference[5][0])/2
    event_difference += difference[3][3]+difference[12][12]+difference[15][15]
    M2, M4 = moments[2], moments[4]
    assert moments[0] == 1 and moments[1] == moments[3] == 0
    assert M2 == Fraction(1, 4*(N-1))
    assert M4 == Fraction(3*N-8, 16*N*(N-1)*(N-3))
    assert event_difference == -5*M2+6*M4
    numeric_difference = np.array(difference, dtype=float)
    return {
        "rotation_order": N, "hash_bins": 2, "shared_oracle": True,
        "hypergeometric_law": law, "second_moment": rational(M2), "fourth_moment": rational(M4),
        "shared_two_copy_state": [[rational(x) for x in row] for row in shared],
        "fresh_resampled_two_copy_state": [[rational(x) for x in row] for row in independent],
        "wrong_two_copy_state": [[rational(x) for x in row] for row in wrong],
        "fixed_measurement_absolute_difference": rational(abs(event_difference)),
        "twice_averaged_one_copy_distance": rational(4*M2),
        "naive_averaged_one_copy_hybrid_falsified": abs(event_difference) > 4*M2,
        "shared_is_not_resampled": shared != independent,
        "optimal_two_copy_trace_distance_numeric_only": float(np.sum(np.abs(np.linalg.eigvalsh(numeric_difference)))/2),
        "measurement_depends_on_hidden_permutation": False,
        "algorithm_or_scaling_evidence": False,
    }


def _sqrt_dyadic_upper(x):
    if x <= 0:
        return Fraction(0)
    if x >= 1:
        return Fraction(1)
    exponent = ((x.denominator//x.numerator).bit_length()-1)//2
    upper = Fraction(1, 1 << exponent)
    assert upper**2 >= x
    return upper


def scoped_scaling_certificate(n, K, probes, hash_menu, implementation_error=Fraction(0)):
    _integer(n, "modulus bits")
    _integer(probes, "instrument probes", 0)
    _integer(hash_menu, "predeclared hash menu")
    N = 1 << n
    _source(N, K)
    if type(implementation_error) not in (int, Fraction) or not 0 <= implementation_error <= 1:
        raise ValueError("exact total composed trace-error budget in [0,1] required")
    delta = Fraction(K-1, K*(N-1))
    ceil_root = isqrt(K)
    ceil_root += ceil_root**2 != K
    coefficient = Fraction(4+ceil_root, 2)
    squared = probes**2*coefficient**2*hash_menu*delta
    ideal_distance = _sqrt_dyadic_upper(squared)
    distance = min(Fraction(1), ideal_distance+implementation_error)
    thin_distance = min(Fraction(1), probes*hash_menu*delta+implementation_error)
    return {
        "modulus_bits": n, "rotation_order": str(N), "hash_bins": K,
        "instrument_probes": probes, "oracle_queries": 2*probes,
        "predeclared_balanced_hash_menu_size": hash_menu,
        "one_copy_averaged_distance": rational(delta),
        "pointwise_distance_coefficient_upper": rational(coefficient),
        "shared_oracle_quantum_hybrid_squared_bound": rational(squared),
        "ideal_quantum_trace_distance_upper": rational(ideal_distance),
        "quantum_trace_distance_upper_with_error": rational(distance),
        "binary_success_upper_with_error": rational((1+distance)/2),
        "three_outcome_classical_transcript_distance_upper": rational(thin_distance),
        "total_composed_trace_error_budget": rational(implementation_error),
        "nonzero_precision_budget_requires_separate_proof": True,
        "arbitrary_quantum_postprocessing_retained_hashes_allowed": True,
        "classical_adaptive_selection_from_predeclared_menu_allowed": True,
        "coherent_hash_selection_or_retained_domain_covered": False,
        "other_full_oracle_algorithms_covered": False,
        "independent_nuisance_resampling_assumed": False,
        "source_mean_not_pointwise_permutation": True,
        "speedup_claim_allowed": False,
    }


def index_erasure_range_gate(domain_size, codomain_size, epsilon=Fraction(1)):
    """Check a theorem premise, NOT a DHSP complexity theorem or finite bound."""
    _integer(domain_size, "injective domain size", 2)
    _integer(codomain_size, "codomain size", domain_size)
    if type(epsilon) not in (int, Fraction) or epsilon <= 0:
        raise ValueError("positive fixed exact range exponent margin required")
    epsilon = Fraction(epsilon)
    meets = codomain_size**epsilon.denominator >= domain_size**(3*epsilon.denominator+epsilon.numerator)
    return {"injective_domain_size": domain_size, "codomain_size": codomain_size,
            "fixed_positive_epsilon": rational(epsilon),
            "large_range_numeric_premise_met": meets,
            "asymptotic_fixed_epsilon_family_premise_still_required": True,
            "surjective_permutation_dhsp_transfer_licensed": False,
            "general_dhsp_lower_bound_licensed": False,
            "embedding": "f(b,x)=g(x) hides the known reflection H_0; one g query per f query",
            "only_primitive_conclusion": "Generic pure-image preparation would solve injective index erasure",
            "primary_theorem": "Lindzey-Rosmanis 2022, Theorem1, m>=n^(3+epsilon)"}


def encoded_instrument(vectors, subset):
    """Bounded codomain-only pure encoders; every encoder output is retained."""
    V = np.asarray(vectors, dtype=complex)
    if V.ndim != 2 or not 2 <= len(V) <= 16 or not 1 <= V.shape[1] <= 64 or not np.isfinite(V).all():
        raise ValueError("bounded finite codomain vectors required")
    if not np.allclose(np.sum(np.abs(V)**2, axis=1), 1, atol=1e-12, rtol=0):
        raise ValueError("all codomain encoder vectors must be normalized")
    if not isinstance(subset, (tuple, list)) or not subset or len(set(subset)) != len(subset) or any(type(i) is not int or not 0 <= i < len(V) for i in subset):
        raise ValueError("distinct nonempty codomain subset required")
    A = V[list(subset)]/np.sqrt(len(subset))
    mu = np.ones(len(subset))/np.sqrt(len(subset)) @ A
    failed = A-np.outer(np.ones(len(subset))/np.sqrt(len(subset)), mu)
    d = V.shape[1]
    state = np.zeros((2*d, 2*d), dtype=complex)
    state[:d, :d] = np.outer(mu, mu.conj())
    state[d:, d:] = failed.T @ failed.conj()
    return state


def encoder_variance_control(vectors, name):
    V = np.asarray(vectors, dtype=complex)
    N, d = V.shape
    _source(N, 1)
    wrong = encoded_instrument(V, list(range(N)))
    mu = V.mean(axis=0)
    rho = V.T @ V.conj()/N
    covariance = (rho-np.outer(mu, mu.conj()))/(N-1)
    expected = np.zeros_like(wrong)
    expected[:d, :d], expected[d:, d:] = covariance, -covariance
    mean = np.zeros_like(wrong)
    mean_vector_variance = mean_density_variance = mean_distance = 0.0
    subsets = list(combinations(range(N), N//2))
    for S in subsets:
        state = encoded_instrument(V, list(S))
        mean += state/len(subsets)
        subset_V = V[list(S)]
        vector_var = np.linalg.norm(subset_V.mean(axis=0)-mu)**2
        density_var = np.linalg.norm(subset_V.T @ subset_V.conj()/len(S)-rho, ord="fro")**2
        distance = np.sum(np.abs(np.linalg.eigvalsh(state-wrong)))/2
        assert distance <= 2*np.sqrt(vector_var)+np.sqrt(d*density_var)/2+1e-10
        mean_vector_variance += vector_var/len(subsets)
        mean_density_variance += density_var/len(subsets)
        mean_distance += distance/len(subsets)
    vector_expected = (1-float(np.vdot(mu, mu).real))/(N-1)
    density_expected = (1-float(np.trace(rho@rho).real))/(N-1)
    assert abs(mean_vector_variance-vector_expected) < 1e-10
    assert abs(mean_density_variance-density_expected) < 1e-10
    assert np.max(np.abs(mean-wrong-expected)) < 1e-10
    return {"name": name, "rotation_order": N, "retained_encoder_dimension": d,
            "encoder_vectors_real": V.real.tolist(), "encoder_vectors_imag": V.imag.tolist(),
            "subset_count": len(subsets), "mean_vector_variance": mean_vector_variance,
            "mean_density_frobenius_variance": mean_density_variance,
            "mean_complete_instrument_distance": mean_distance,
            "one_copy_averaged_distance": float(np.trace(covariance).real),
            "averaged_instrument_formula_residual": float(np.max(np.abs(mean-wrong-expected))),
            "numerical_physical_calibration_only": True}


def general_encoder_scaling_certificate(n, dimension, probes, encoder_menu):
    _integer(n, "modulus bits")
    _integer(dimension, "complete retained encoder Hilbert dimension")
    _integer(probes, "probes", 0)
    _integer(encoder_menu, "predeclared encoder menu")
    root = isqrt(dimension)
    root += root*root != dimension
    C = Fraction(4+root, 2)
    squared = probes**2*C*C*Fraction(encoder_menu, (1 << n)-1)
    upper = _sqrt_dyadic_upper(squared)
    return {"modulus_bits": n, "retained_encoder_hilbert_dimension": dimension,
            "probes": probes, "predeclared_encoder_menu": encoder_menu,
            "shared_oracle_distance_squared_upper": rational(squared),
            "shared_oracle_distance_dyadic_upper": rational(upper),
            "coherent_hash_selector_inside_fresh_known_encoder_covered": True,
            "polynomial_qubits_implies_polynomial_hilbert_dimension": False,
            "coherent_cross_call_or_domain_retaining_oracle_access_covered": False,
            "candidate_record_accepted": False}


def run_controls():
    controls = []
    for N in (4, 8, 16):
        bits = (N-1).bit_length()
        permutations = [[(3*x+1) % N for x in range(N)],
                        [int(f"{x:0{bits}b}"[::-1], 2) for x in range(N)]]
        for pi in permutations:
            for K in (1, 2, 4):
                for s in (0, 1, N-1):
                    for epsilon in (0, 1):
                        row = physical_control(oracle_table(N, s, pi, epsilon), [v % K for v in range(N)], K)
                        row.update(rotation_order=N, shift=s, subgroup_parity=epsilon, output_permutation=pi)
                        controls.append(row)
    # Enumerate subsets, not permutations: the histogram depends only on pi(even).
    moment_controls = []
    for N, K in ((4, 2), (8, 2), (8, 4)):
        ps = [balanced_histogram(N, K, S) for S in combinations(range(N), N//2)]
        count = len(ps)
        cov = [[sum((p[i]-Fraction(1, K))*(p[j]-Fraction(1, K)) for p in ps)/count for j in range(K)] for i in range(K)]
        expected = one_copy_moments(N, K)
        assert cov == expected["covariance"]
        means = [sum(p[i] for p in ps)/count for i in range(K)]
        assert means == [Fraction(1, K)]*K
        moment_controls.append({"rotation_order": N, "hash_bins": K, "subset_count": count,
                                "covariance": [[rational(x) for x in row] for row in cov],
                                "averaged_one_copy_trace_distance": rational(expected["one_copy_averaged_trace_distance"])})
    ledgers = []
    for n in (16, 32, 64, 128, 256):
        K = 1 << (n-1).bit_length()
        ledgers.append(scoped_scaling_certificate(n, K, n*n, n))
    coherent = np.zeros((8, 4), dtype=complex)
    complex_vectors = np.zeros((8, 2), dtype=complex)
    for y in range(8):
        coherent[y, y % 2] = 1/np.sqrt(2)
        coherent[y, 2+(y//2) % 2] = 1j/np.sqrt(2)
        complex_vectors[y] = [3/5, (4/5)*1j**(y % 4)]
    return {
        "status": "LOCAL_DERIVATION_REVIEW_PENDING",
        "source": "Full DHSP oracle f_s(b,x)=pi(x-b*s), fixed uniform output permutation, index-two subgroup probes",
        "withdrawn_paper": "https://arxiv.org/abs/2202.09697",
        "physical_controls": controls, "exact_moment_controls": moment_controls,
        "shared_nuisance_controls": [shared_two_copy_control(N) for N in (4, 8, 16, 32)],
        "native_scaling_ledgers": ledgers,
        "precision_floor_counterledger": scoped_scaling_certificate(256, 256, 256**2, 256, Fraction(1, 10**6)),
        "index_erasure_scope_controls": [index_erasure_range_gate(8, 8), index_erasure_range_gate(8, 4096)],
        "general_encoder_controls": [encoder_variance_control(coherent, "coherent_two_hash_selector"),
                                     encoder_variance_control(complex_vectors, "complex_nonorthogonal_encoder"),
                                     encoder_variance_control(np.eye(8), "full_label_encoder_dimension_countercontrol")],
        "general_encoder_scaling_ledgers": [general_encoder_scaling_certificate(n, n*n, n*n, n) for n in (32, 64, 128, 256)],
        "claim_gate": {"candidate_record_accepted": False, "speedup_claim_allowed": False,
                       "independent_review": False, "novelty_claim": False,
                       "general_dhsp_or_oracle_lower_bound": False},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = run_controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"report": str(args.output), "physical_controls": len(report["physical_controls"]),
                      "shared_oracle_witness": report["shared_nuisance_controls"][1]["fixed_measurement_absolute_difference"],
                      "candidate_accepted": False}))


if __name__ == "__main__":
    main()
