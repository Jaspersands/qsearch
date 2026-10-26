"""Support-budgeted guides on the ORIGINAL nonlinear residual chain.

Exact combinatorial Rayleigh witnesses and a local-operator upper certificate.
No quantum execution, new decoder, classical lower bound, or speedup claim.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import json
from math import comb, lcm, sqrt
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flint import fmpz_mat
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh

from theorems.nonlinear_filter_pinning import enclose, exact_moments, rational_filter
from theorems.prime_character_finite_readout import sqrt_interval

REPORT = ROOT / "research/reductions/chain_support_budget.json"


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def check(M, K, rho=Q(1, 2)):
    if type(M) is not int or M < 1 or type(K) is not int or not 0 <= K <= M+1:
        raise ValueError("positive path length and integer vertex budget required")
    if not isinstance(rho, Q) or not 0 < rho < 1:
        raise ValueError("exact rational density in (0,1) required")


def signature(word, M):
    """Number of active edges, runs, and covered vertices of a path."""
    if type(M) is not int or M < 1 or type(word) is not int or not 0 <= word < 1 << M:
        raise ValueError("physical path bit string required")
    d = word.bit_count()
    r = (word & ~(word << 1)).bit_count()
    return d, r, d+r


def counts(M, K):
    check(M, K)
    result = {(0, 0): 1}
    for d in range(1, min(M, K-1)+1):
        for r in range(1, min(d, M-d+1, K-d)+1):
            result[d, r] = choose(d-1, r-1)*choose(M-d+1, r)
    return result


def additions(M, state):
    """Total directed 0->1 flips from one (degree,run) class, not per word."""
    d, r = state
    if state == (0, 0):
        return {(1, 1): M}
    if not 1 <= r <= min(d, M-d+1):
        raise ValueError("impossible degree/run class")
    z, compositions = M-d, choose(d-1, r-1)
    count = compositions*choose(z+1, r)
    bridge = compositions*(r-1)*choose(z, r-1)
    isolated = compositions*(r+1)*choose(z, r+1)
    extend = z*count-bridge-isolated
    if min(bridge, extend, isolated) < 0:
        raise ArithmeticError("invalid flip count")
    return {key: value for key, value in
            [((d+1, r-1), bridge), ((d+1, r), extend), ((d+1, r+1), isolated)]
            if value}


def ritz_matrix(M, K, rho):
    """Compression only. Its square is NOT the compressed second moment."""
    check(M, K, rho)
    sizes = counts(M, K)
    states = tuple(sizes)
    index = {state: i for i, state in enumerate(states)}
    rows, cols, values = [], [], []
    for state, i in index.items():
        d, _ = state
        rows.append(i)
        cols.append(i)
        values.append(float(M*rho+(1-2*rho)*d))
        for target, edges in additions(M, state).items():
            if target in index:
                j = index[target]
                value = sqrt(float(rho*(1-rho)))*sqrt(edges/sizes[state])*sqrt(edges/sizes[target])
                rows.extend((i, j))
                cols.extend((j, i))
                values.extend((value, value))
    return states, coo_matrix((values, (rows, cols)), shape=(len(states),)*2).tocsr()


def propose(M, K, rho, weight_bits=40, root_bits=512):
    """Return rational coefficients of sums of products of (predicate-rho)."""
    states, matrix = ritz_matrix(M, K, rho)
    if len(states) == 1:
        weights = np.ones(1)
    else:
        _, vectors = eigsh(matrix, k=1, which="LA", tol=1e-12, v0=np.ones(len(states)))
        weights = vectors[:, 0]
        if sum(weights) < 0:
            weights = -weights
    sizes, variance = counts(M, K), rho*(1-rho)
    coefficients = {}
    for state, weight in zip(states, weights):
        w = Q(round(max(0., float(weight))*(1 << weight_bits)), 1 << weight_bits)
        norm = sizes[state]*variance**state[0]
        a = w*sqrt_interval(1/norm, root_bits)[0]
        if a:
            coefficients[state] = a
    return coefficients


def rayleigh(M, K, rho, coefficients):
    """Exact mean for THIS rational guide, not a numerical eigenvalue claim."""
    check(M, K, rho)
    sizes, variance = counts(M, K), rho*(1-rho)
    if any(s not in sizes for s in coefficients):
        raise ValueError("guide exceeds vertex budget")
    if any(not isinstance(a, (int, Q)) or isinstance(a, bool) for a in coefficients.values()):
        raise ValueError("explicit rational guide required")
    norm = Q(0)
    numerator = Q(0)
    for state, a in coefficients.items():
        d, _ = state
        mass = Q(a)**2*sizes[state]*variance**d
        norm += mass
        numerator += mass*(M*rho+(1-2*rho)*d)
        for target, edges in additions(M, state).items():
            numerator += 2*a*coefficients.get(target, 0)*edges*variance**(d+1)
    if norm <= 0:
        raise ValueError("nonzero guide required")
    return norm, numerator/norm


def transfer(dimension, K, moment_order=1):
    if any(type(x) is not int or x < 0 for x in (dimension, K, moment_order)):
        raise ValueError("nonnegative integer transfer parameters required")
    required = 2*K+2*moment_order
    if dimension < required:
        raise ValueError("RS independence budget does not certify this moment")
    return {"RS_dimension": dimension, "Fourier_support_cap": K,
            "moment_order": moment_order, "vertex_independence_required": required,
            "decoder": "existing whole-cap Hamming Prony, 2K syndrome coordinates",
            "entire_score_distribution_transferred": False}


def local_matrix(rho, block, penalty):
    """Rational entrywise upper comparison: replace sqrt(rho(1-rho)) by 1/2."""
    if type(block) is not int or not 2 <= block <= 8:
        raise ValueError("certificate block must be an integer in [2,8]")
    if not isinstance(rho, Q) or not 0 < rho < 1 or not isinstance(penalty, Q) or penalty < 0:
        raise ValueError("exact density and nonnegative rational penalty required")
    size = 1 << block
    matrix = [[Q(0)]*size for _ in range(size)]
    for word in range(size):
        degree = word.bit_count()
        pairs = (word & (word >> 1)).bit_count()
        matrix[word][word] = ((1-2*rho)*Q(degree, block)
                             -penalty*(Q(2*degree, block)-Q(pairs, block-1)))
        for i in range(block):
            matrix[word][word ^ (1 << i)] = Q(1, 2*block)
    return matrix


def cluster_certificate(M, K, rho, block=4, penalty=Q(8, 5), upper=Q(7761, 100000)):
    """Exact Sylvester certificate plus periodic-window operator inequality."""
    check(M, K, rho)
    if block > M or not isinstance(upper, Q):
        raise ValueError("block must fit the path and upper bound must be rational")
    matrix = local_matrix(rho, block, penalty)
    size = len(matrix)
    slack = [[upper*int(i == j)-matrix[i][j] for j in range(size)] for i in range(size)]
    scale = lcm(*(v.denominator for row in slack for v in row))
    integers = [[int(v*scale) for v in row] for row in slack]
    minors = [int(fmpz_mat([row[:j] for row in integers[:j]]).det()) for j in range(1, size+1)]
    if any(det <= 0 for det in minors):
        raise ValueError("proposed local eigenvalue upper bound failed exact positive-definiteness check")
    bound = rho+penalty*Q(K, M)+upper
    return {"path_edges": M, "vertex_budget": K, "rho": str(rho),
            "block": block, "penalty": str(penalty), "local_eigenvalue_upper": str(upper),
            "comparison_off_diagonal": "1/(2*block), >= sqrt(rho*(1-rho))/block",
            "integer_scale": str(scale), "positive_leading_minors": list(map(str, minors)),
            "score_fraction_upper_exact": str(bound),
            "scope": "all complex guides in span of centered-predicate products with covered vertices <= K"}


def verify_cluster(certificate):
    expected = cluster_certificate(certificate["path_edges"], certificate["vertex_budget"],
                                   Q(certificate["rho"]), certificate["block"],
                                   Q(certificate["penalty"]), Q(certificate["local_eigenvalue_upper"]))
    if certificate != expected:
        raise ValueError("corrupt local-operator certificate")
    return True


def native_report():
    p, M, n, K = 2053, 2051, 205, 100
    rho = Q(1026, p)
    coefficients = propose(M, K, rho)
    norm, mean = rayleigh(M, K, rho, coefficients)
    old = rational_filter(M, rho, K//2)
    _, old_mean, _ = exact_moments(old, M, rho)
    certificate = cluster_certificate(M, K, rho)
    verify_cluster(certificate)
    mean_cap = (n-2)//2
    mean_coefficients = propose(M, mean_cap, rho)
    mean_norm, mean_only = rayleigh(M, mean_cap, rho, mean_coefficients)
    mean_certificate = cluster_certificate(M, mean_cap, rho)
    return {
        "schema": "original_chain_support_budget_v1",
        "status": "certified_finite_guide_comparison; deprioritize_tuning; independent_proof_review_pending",
        "source": "https://arxiv.org/abs/2609.35101",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "problem": {"prime": p, "tests": M, "polynomial_dimension": n,
                    "density": str(rho), "input": "same original adjacent nonlinear residual chain",
                    "tables": "any explicit halfsets of size1026; any nonzero residual multipliers",
                    "new_task_or_input_resampling": False},
        "transfer": transfer(n, K, 1),
        "guide": {"shells": len(counts(M, K)), "nonzero_shells": len(coefficients),
                  "coefficients": [{"degree": d, "runs": r, "value": str(a)}
                                   for (d, r), a in coefficients.items()],
                  "norm": str(norm), "score_fraction_exact": str(mean/M),
                  "score_fraction_lower_dyadic": str(enclose(mean/M)),
                  "baseline_score_fraction_exact": str(old_mean/M),
                  "gain_fraction_exact": str((mean-old_mean)/M)},
        "upper_certificate": certificate,
        "mean_only_budget": {
            "transfer": transfer(n, mean_cap),
            "second_moment_certified": False,
            "coefficients": [{"degree": d, "runs": r, "value": str(a)}
                             for (d, r), a in mean_coefficients.items()],
            "norm": str(mean_norm), "score_fraction_exact": str(mean_only/M),
            "upper_certificate": mean_certificate},
        "decision": "Same-cap gain is about0.081 percentage points; not a breakthrough lead. Stop guide tuning.",
        "blocked": ["matched full classical portfolio/hardness", "novelty and independent proof review",
                    "coherent gate counts and approximation error budget",
                    "no full score distribution from one transferred moment"],
        "quantum_algorithm_executed": False,
        "speedup_claim_admitted": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = native_report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    guide = report["guide"]
    print(json.dumps({"output": str(args.output),
                      "mean_fraction": float(Q(guide["score_fraction_exact"])),
                      "gain_percentage_points": 100*float(Q(guide["gain_fraction_exact"])),
                      "class_upper": float(Q(report["upper_certificate"]["score_fraction_upper_exact"])),
                      "mean_only_fraction": float(Q(report["mean_only_budget"]["score_fraction_exact"])),
                      "mean_only_class_upper": float(Q(
                          report["mean_only_budget"]["upper_certificate"]["score_fraction_upper_exact"])),
                      "speedup_claim_admitted": False}))


if __name__ == "__main__":
    main()
