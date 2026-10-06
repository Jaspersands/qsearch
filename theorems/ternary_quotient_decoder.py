"""Certified degree-D quotient decoder for ternary binary-error equations.

Implementation of arXiv:2609.40321v1 Section4.2, not a new algorithm.
LOCAL IMPLEMENTATION AUDIT / REVIEW PENDING. No quantum source bridge or speedup.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from math import comb
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/ternary_quotient_decoder.json"


def monomials(n, degree):
    """Bounded-degree compositions, NOT a loop over all ternary secrets."""
    if n == 0:
        return [()] if degree == 0 else []
    return [(head, *tail) for head in range(min(2, degree)+1)
            for tail in monomials(n-1, degree-head)]


def monomial_dimension(n, degree):
    """Coefficient of t^degree in (1+t+t^2)^n, without listing monomials."""
    if type(n) is not int or n < 0 or type(degree) is not int or degree < 0:
        raise ValueError("nonnegative integer dimension and degree required")
    if n == 0:
        return int(degree == 0)
    if degree > 2*n:
        return 0
    return sum((-1)**j*comb(n, j)*comb(n+degree-3*j-1, degree-3*j)
               for j in range(min(n, degree//3)+1))


def single_sample_image_certificate(n, degree):
    """Rank of multiplication by a nonzero linear form squared in x_j^3=0."""
    if type(n) is not int or n < 1 or type(degree) is not int or not 2 <= degree <= 2*n+1:
        raise ValueError("positive dimension and degree between2 and2n+1 required")
    image = monomial_dimension(n-1, degree-2)
    top = monomial_dimension(n, degree)
    return {"dimension": n, "degree": degree, "leading_dimension": top,
            "nonzero_sample_image_rank": image,
            "necessary_nonzero_samples": (top+image-1)//image if image else 0,
            "counting_condition_is_sufficient": False,
            "uniqueness_or_native_source_probability_proved": False,
            "status": "EXACT_ALGEBRAIC_COUNT_REVIEW_PENDING"}


class Span:
    def __init__(self, dimension):
        self.dimension = dimension
        self.rows = {}

    def reduce(self, vector):
        v = np.asarray(vector, dtype=np.int64).copy() % 3
        if v.shape != (self.dimension,):
            raise ValueError("finite-field vector has wrong dimension")
        for pivot, row in sorted(self.rows.items()):
            if v[pivot]:
                v = (v-v[pivot]*row) % 3
        return v

    def add(self, vector):
        v = self.reduce(vector)
        support = np.flatnonzero(v)
        if not len(support):
            return None
        pivot = int(support[0])
        v = v*int(v[pivot]) % 3  # Nonzero elements1,2 are their own inverses.
        self.rows[pivot] = v
        return v


def invariant_closure(initial_vectors, operators):
    H = operators[0].shape[0]
    relations = Span(H)
    queue = []
    for vector in initial_vectors:
        new = relations.add(vector)
        if new is not None:
            queue.append(new)
    initial_rank = len(queue)
    cursor = 0
    while cursor < len(queue):
        vector = queue[cursor]
        cursor += 1
        for matrix in operators:
            new = relations.add(matrix@vector % 3)
            if new is not None:
                queue.append(new)
    return relations, initial_rank, cursor


def _annihilator(column, observation):
    n = len(column)
    zero = (0,)*n
    terms = {zero: observation*(observation-1) % 3}
    for j, a in enumerate(column):
        e = tuple(int(k == j) for k in range(n))
        terms[e] = a*(1-2*observation) % 3
        terms[tuple(2*v for v in e)] = a*a % 3
        for k in range(j):
            alpha = tuple(int(t in (j, k)) for t in range(n))
            terms[alpha] = 2*a*column[k] % 3
    return {alpha: value for alpha, value in terms.items() if value}


def decode_ternary_binary_error(labels, observations, degree, *, include_certificate=False):
    A = tuple(tuple(row) for row in labels)
    b = tuple(observations)
    if not A or not A[0] or any(len(row) != len(A[0]) for row in A) or len(b) != len(A[0]):
        raise ValueError("nonempty n-by-m matrix and m observations required")
    if any(type(v) is not int or v not in (0, 1, 2) for row in A for v in row) or any(type(v) is not int or v not in (0, 1, 2) for v in b):
        raise ValueError("canonical F3 labels and observations required")
    n, m = len(A), len(b)
    if type(degree) is not int or not 2 <= degree <= 2*n+1:
        raise ValueError("degree between2 and2n+1 required; growing degree costs are charged")
    low = [alpha for d in range(degree) for alpha in monomials(n, d)]
    top = monomials(n, degree)
    multipliers = monomials(n, degree-2)
    low_index, top_index = {a:i for i,a in enumerate(low)}, {a:i for i,a in enumerate(top)}
    H, K = len(low), len(top)
    columns = tuple(zip(*A))
    polynomials = [_annihilator(a, v) for a, v in zip(columns, b)]
    leading = {}
    for polynomial in polynomials:
        for mu in multipliers:
            upper, lower = np.zeros(K, dtype=np.int64), np.zeros(H, dtype=np.int64)
            for alpha, coefficient in polynomial.items():
                beta = tuple(x+y for x,y in zip(alpha, mu))
                beta = tuple(v if v < 3 else v-2 for v in beta)
                if sum(beta) == degree:
                    upper[top_index[beta]] = (upper[top_index[beta]]+coefficient) % 3
                else:
                    lower[low_index[beta]] = (lower[low_index[beta]]+coefficient) % 3
            for pivot, (u, v) in sorted(leading.items()):
                coefficient = int(upper[pivot])
                if coefficient:
                    upper, lower = (upper-coefficient*u) % 3, (lower-coefficient*v) % 3
            support = np.flatnonzero(upper)
            if len(support):
                pivot = int(support[0])
                inverse = int(upper[pivot])
                leading[pivot] = (upper*inverse % 3, lower*inverse % 3)
    base = {"status": "LEADING_DEGREE_CERTIFICATE_FAILED", "secret": None,
            "dimension": n, "samples": m, "degree": degree, "low_monomial_dimension": H,
            "leading_monomial_dimension": K, "leading_rank": len(leading),
            "secret_assignments_enumerated_by_decoder": False,
            "runtime_polynomial_for_each_FIXED_degree_not_uniform_in_growing_degree": True,
            "asymptotic_source_probability_proved_by_these_trials": False,
            "candidate_record_accepted": False, "novelty_claim": False, "speedup_claim_allowed": False}
    if len(leading) != K:
        return base
    # Back elimination tracks true inhomogeneous equations, including x^3=x.
    for pivot in sorted(leading, reverse=True):
        upper, lower = leading[pivot]
        for previous in range(pivot):
            u, v = leading[previous]
            coefficient = int(u[pivot])
            if coefficient:
                leading[previous] = ((u-coefficient*upper) % 3, (v-coefficient*lower) % 3)
    rewrite = {top[p]: -v % 3 for p, (_, v) in leading.items()}
    operators = []
    for j in range(n):
        matrix = np.zeros((H, H), dtype=np.int64)
        for i, alpha in enumerate(low):
            beta = list(alpha)
            beta[j] += 1
            if beta[j] == 3:
                beta[j] = 1
            beta = tuple(beta)
            if sum(beta) < degree:
                matrix[low_index[beta], i] = 1
            else:
                matrix[:, i] = rewrite[beta]
        operators.append(matrix)
    identity = np.eye(H, dtype=np.int64)
    generator_maps = [((X@X % 3)@X-X) % 3 for X in operators]
    generator_maps += [(X@Y-Y@X) % 3 for j, X in enumerate(operators) for Y in operators[:j]]
    for a, v in zip(columns, b):
        linear = sum((int(c)*X for c, X in zip(a, operators)), np.zeros((H,H), dtype=np.int64)) % 3
        generator_maps.append((linear@linear+(1-2*v)*linear+v*(v-1)*identity) % 3)
    relations, initial_rank, processed = invariant_closure((v for matrix in generator_maps for v in matrix.T), operators)
    stable = all(not np.any(relations.reduce(X@v % 3)) for X in operators for v in relations.rows.values())
    equations_hold = all(not np.any(relations.reduce(v)) for matrix in generator_maps for v in matrix.T)
    assert stable and equations_hold
    quotient_dimension = H-len(relations.rows)
    result = {**base, "status": "MULTIPLE_BINARY_ERROR_SECRETS" if quotient_dimension > 1 else "INCONSISTENT_BINARY_ERROR_EQUATIONS",
              "quotient_dimension": quotient_dimension, "initial_relation_rank": initial_rank,
              "final_relation_rank": len(relations.rows), "closure_basis_vectors_processed": processed,
              "relation_space_stable_under_every_variable": stable,
              "commutators_field_and_sample_equations_vanish_on_quotient": equations_hold,
              "complete_quotient_not_just_truncated_Macaulay_rank": True}
    if include_certificate:
        result["algebra_certificate"] = {"low_monomials": low, "degree_monomials": top,
            "degree_rewrite_vectors": [rewrite[a].tolist() for a in top],
            "provisional_variable_multiplication_matrices": [X.tolist() for X in operators],
            "stable_relation_basis": [v.tolist() for v in relations.rows.values()]}
    if quotient_dimension != 1:
        return result
    unit = relations.reduce(identity[:, 0])
    support = np.flatnonzero(unit)
    assert len(support) == 1
    pivot = int(support[0])
    secret = tuple(int(relations.reduce(X@identity[:, 0] % 3)[pivot])*int(unit[pivot]) % 3 for X in operators)
    errors = tuple((v-sum(a*s for a,s in zip(column, secret))) % 3 for column,v in zip(columns,b))
    assert all(e in (0,1) for e in errors)
    return {**result, "status": "CERTIFIED_UNIQUE_TERNARY_BINARY_ERROR_SECRET",
            "secret": secret, "verified_errors": errors}


def run_controls():
    rng = random.Random(72105)
    trials = []
    for n, m, D in ((2, 5, 3), (4, 8, 3), (6, 18, 3), (8, 30, 3)):
        A = tuple(tuple(rng.randrange(3) for _ in range(m)) for _ in range(n))
        secret = tuple(rng.randrange(3) for _ in range(n))
        errors = tuple(i % 2 for i in range(m))
        b = tuple((sum(A[j][i]*secret[j] for j in range(n))+errors[i]) % 3 for i in range(m))
        result = decode_ternary_binary_error(A, b, D, include_certificate=n <= 4)
        assert result["secret"] is None or result["secret"] == secret
        trials.append({"labels": A, "observations": b, "planted_secret": secret,
                       "degree_two_feature_dimension": n*(n+1)//2,
                       "fewer_samples_than_degree_two_feature_dimension": m < n*(n+1)//2,
                       "planted_secret_recovered": result["secret"] == secret, "result": result})
    return {"status": "LITERATURE_ALGORITHM_IMPLEMENTATION_REVIEW_PENDING",
            "source_url": "https://arxiv.org/html/2609.40321v1", "source_sections": "4.1-4.2, Definition4.11",
            "actual_fixed_source_decoder_trials": trials,
            "single_sample_image_certificates": [single_sample_image_certificate(n, D)
                                                  for n,D in ((4,3),(8,3),(8,4))],
            "claim_gate": {"full_quotient_closure_implemented": True,
                           "complete_published_sample_time_tradeoff_implemented": False,
                           "quantum_subset_sum_algorithm_or_native_DCP_source_bridge_implemented": False,
                           "small_degree_trials_meet_published_500n_surjectivity_theorem_regime": False,
                           "independent_implementation_review": False,
                           "candidate_record_accepted": False, "novelty_claim": False, "speedup_claim_allowed": False},
            "dependency_sha256": {str(Path(__file__).relative_to(ROOT)): hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"status": report["status"], "claim_gate": report["claim_gate"],
                      "trials": [(r["result"]["dimension"],r["planted_secret_recovered"],r["result"]["status"]) for r in report["actual_fixed_source_decoder_trials"]]}, indent=2))


if __name__ == "__main__":
    main()
