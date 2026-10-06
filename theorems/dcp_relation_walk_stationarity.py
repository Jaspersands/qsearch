"""Actual signed-relation swaps and a scoped native fiber-walk falsifier.

LOCAL DERIVATION / REVIEW PENDING. This is not a no-go for general collective
measurements, word-adaptive implicit neighbor finders or transverse walk drives.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
from fractions import Fraction
from pathlib import Path

import numpy as np

from dcp_bell_inference_kernel import exact
from dcp_terminal_affine_fibers import _positive_integer

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_relation_walk_stationarity.json"


def _matrix(labels, modulus):
    if type(modulus) is not int or modulus < 3:
        raise ValueError("q>=3 required for distinct signed coefficients")
    A = tuple(tuple(row) for row in labels)
    if not A or not A[0] or any(len(row) != len(A[0]) for row in A):
        raise ValueError("nonempty rectangular native matrix required")
    if any(type(a) is not int or not 0 <= a < modulus for row in A for a in row):
        raise ValueError("canonical native labels required")
    return A


def signed_relation_swap(labels, modulus, relation, word):
    """Known O(n*m) verification and O(m) conditional endpoint transposition."""
    A = _matrix(labels, modulus)
    m = len(A[0])
    delta = tuple(relation)
    if len(delta) != m or any(type(d) is not int or d not in (-1, 0, 1) for d in delta) or not any(delta):
        raise ValueError("nonempty physical signed relation required")
    if type(word) is not int or not 0 <= word < 1 << m:
        raise ValueError("canonical physical Boolean word required")
    if any(sum(a*d for a, d in zip(row, delta)) % modulus for row in A):
        raise ValueError("relation must preserve full native residue")
    support = sum((d != 0) << j for j, d in enumerate(delta))
    positive = sum((d == 1) << j for j, d in enumerate(delta))
    negative = support ^ positive
    return word ^ support if word & support in (positive, negative) else word


def signed_relation_dictionary_certificate(dimension, modulus_bits, columns, excluded_support, dictionary_size):
    for value, name in ((dimension, "dimension"), (modulus_bits, "modulus bits"), (columns, "columns")):
        _positive_integer(value, name)
    if modulus_bits < 2 or type(excluded_support) is not int or not 0 <= excluded_support <= columns:
        raise ValueError("q>=4 and physical support threshold required")
    if type(dictionary_size) is not int or dictionary_size < 0:
        raise ValueError("nonnegative explicitly listed dictionary size required")
    # Quotient signed relations by global negation. Every nonzero +/-1 coefficient
    # is a unit, so each fixed relation event has probability exactly1/q^n.
    count = sum(math.comb(columns, k) * (1 << (k-1)) for k in range(1, excluded_support+1))
    entropy = dimension * modulus_bits
    source_failure = min(Fraction(1), Fraction(count, 1 << entropy))
    applicability = min(Fraction(1), Fraction(dictionary_size, 1 << excluded_support))
    exponent = max(0, entropy - (count-1).bit_length()) if count else None
    return {
        "status": "LOCAL_NATIVE_SIGNED_MOVE_DICTIONARY_GATE_REVIEW_PENDING",
        "dimension": dimension, "modulus_bits": modulus_bits, "columns": columns,
        "excluded_relation_support": excluded_support,
        "signed_relation_classes_of_support_at_most_threshold": str(count),
        "any_short_relation_native_probability_union_upper_bound": exact(source_failure),
        "conservative_short_relation_failure_dyadic_exponent": exponent,
        "listed_relation_count": dictionary_size,
        "on_no_short_relation_event_uniform_word_dictionary_applicability_upper_bound": exact(applicability),
        "unconditional_native_applicability_probability_upper_bound": exact(min(Fraction(1), source_failure+applicability)),
        "label_adaptive_choice_of_the_entire_dictionary_allowed": True,
        "dictionary_must_be_explicit_and_fixed_before_unknown_word_access": True,
        "implicit_word_adaptive_neighbor_finders_ruled_out": False,
        "arbitrary_quantum_walks_or_collective_measurements_ruled_out": False,
        "candidate_record_accepted": False, "speedup_claim_allowed": False,
    }


def _targets(A, q):
    return [tuple(sum(a*(x >> j & 1) for j, a in enumerate(row)) % q for row in A)
            for x in range(1 << len(A[0]))]


def _source_controls():
    q, m = 4, 4
    records = []
    for w in (1, 2):
        relations = []
        for delta in itertools.product((-1, 0, 1), repeat=m):
            if 0 < sum(d != 0 for d in delta) <= w and next(d for d in delta if d) == 1:
                relations.append(delta)
        hits = [0] * len(relations)
        any_hit = 0
        for a in itertools.product(range(q), repeat=m):
            zeros = [sum(x*d for x, d in zip(a, delta)) % q == 0 for delta in relations]
            hits = [old+int(zero) for old, zero in zip(hits, zeros)]
            any_hit += any(zeros)
        assert all(h == q**(m-1) for h in hits)
        assert any_hit <= sum(hits)
        records.append({"modulus": q, "columns": m, "support_threshold": w,
                        "all_native_label_tables": q**m, "all_canonical_signed_relations": len(relations),
                        "exact_one_fixed_relation_source_hits": hits[0],
                        "actual_tables_with_any_short_relation": any_hit,
                        "complete_relation_source_event_checks": q**m*len(relations)})
    return records


def _actual_swap_control():
    A, q, delta = ((1, 1, 2, 3, 0),), 4, (1, -1, 0, 0, 0)
    targets = _targets(A, q)
    permutation = [signed_relation_swap(A, q, delta, x) for x in range(32)]
    assert sorted(permutation) == list(range(32))
    for x, y in enumerate(permutation):
        assert permutation[y] == x and targets[y] == targets[x]
    touched = sum(x != y for x, y in enumerate(permutation))
    assert touched == 16
    residuals = []
    for s in range(q):
        state = np.asarray([np.exp(2j*np.pi*s*t[0]/q)/math.sqrt(32) for t in targets])
        residuals.append(float(np.max(np.abs(state[np.asarray(permutation)]-state))))
    assert max(residuals) < 1e-10
    return {"labels": A, "modulus": q, "signed_relation": delta,
            "full_basis_permutation": permutation, "touched_physical_words": touched,
            "all_fixed_secret_state_residuals": residuals,
            "implemented_swap_is_a_new_hidden_secret_decoder": False}


def _laplacian_controls():
    rng = random.Random(61105)
    rows = []
    for n, q, m in ((1, 8, 5), (1, 8, 7), (2, 4, 7)):
        A = tuple(tuple(rng.randrange(q) for _ in range(m)) for _ in range(n))
        target = _targets(A, q)
        N = len(target)
        L = np.zeros((N, N))
        edges = []
        for x in range(N):
            for y in range(x):
                if target[x] == target[y]:
                    weight = 1 + ((x+3*y) % 7)/8
                    L[x, x] += weight
                    L[y, y] += weight
                    L[x, y] -= weight
                    L[y, x] -= weight
                    edges.append([x, y, weight])
        eigenvalues, eigenvectors = np.linalg.eigh(L)
        maximum = spectral_mass = 0.0
        for secret in itertools.product(range(q), repeat=n):
            state = np.asarray([np.exp(2j*np.pi*sum(s*t for s, t in zip(secret, value))/q)/math.sqrt(N) for value in target])
            maximum = max(maximum, float(np.max(np.abs(L@state))))
            coefficients = eigenvectors.conj().T@state
            spectral_mass = max(spectral_mass, float(np.sum(np.abs(coefficients[eigenvalues > 1e-8])**2)))
        assert maximum < 1e-9 and spectral_mass < 1e-9
        assert len(edges) > 0
        # An irregular adjacency Hamiltonian is not a Laplacian. This positive
        # variance is a scope countercontrol, not a secret-reading primitive.
        degrees = np.diag(L)
        adjacency_variance = float(np.mean(degrees**2)-np.mean(degrees)**2)
        assert adjacency_variance > 1e-8
        rows.append({"dimension": n, "modulus": q, "labels": A, "Boolean_width": m,
                     "explicit_fiber_edges": edges, "occupied_fibers": len(set(target)),
                     "all_fixed_secrets": q**n, "maximum_actual_Laplacian_state_residual": maximum,
                     "maximum_positive_eigenvalue_phase_estimation_mass": spectral_mass,
                     "laplacian_is_zero_operator": False,
                     "non_Laplacian_adjacency_source_energy_variance": adjacency_variance,
                     "all_fiber_preserving_Hamiltonians_leave_state_unchanged": False,
                     "unknown_phase_state_is_already_stationary_in_every_fiber": True,
                     "dense_enumeration_is_a_uniform_walk_construction": False})
    return rows


def run_controls():
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING",
            "complete_native_short_relation_source_controls": _source_controls(),
            "actual_signed_relation_swap": _actual_swap_control(),
            "actual_nonzero_fiber_Laplacian_controls": _laplacian_controls(),
            "native_label_adaptive_dictionary_ledgers": [signed_relation_dictionary_certificate(n, 4*n+1, n*(4*n+1)+16,
                                                                                               (n*(4*n+1)+16)//5,
                                                                                               (n*(4*n+1)+16)**4) for n in (8, 16, 32)],
            "claim_gate": {"pure_equal_sum_Laplacian_walk_moves_the_native_unknown_state": False,
                           "explicit_polynomial_signed_move_dictionary_is_a_native_readout": False,
                           "general_transverse_or_implicit_quantum_walk_ruled_out": False,
                           "uniform_polynomial_witness_finder_supplied": False,
                           "independent_mathematical_review_complete": False,
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
                      "short_relation_failure_dyadic_exponents": [r["conservative_short_relation_failure_dyadic_exponent"] for r in report["native_label_adaptive_dictionary_ledgers"]]}, indent=2))


if __name__ == "__main__":
    main()
