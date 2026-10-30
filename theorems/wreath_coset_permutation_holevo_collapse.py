"""Corrected wreath source: normalized states and matched classical recovery.

The historical Holevo-collapse claim is withdrawn. The repaired twisted-
diagonal subgroup family is NOT general code equivalence or rigid GI.
Finite state controls are explicitly bounded; the recovery algorithm receives
only an opaque-label oracle, never the hidden permutation.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import combinations, permutations, product
import json
import math
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
DERIVATION = ROOT / "research/WREATH_COSET_PERMUTATION_HOLEVO_COLLAPSE.md"
REPORT = ROOT / "research/representation/wreath_coset_permutation_holevo_collapse.json"
REGISTRY = ROOT / "research/registry/negative_results.json"
NEGATIVE_RESULT_ID = "NEG-WREATH-COSET-PERMUTATION-HOLEVO-INFORMATION-COLLAPSE"


def compose(left, right):
    return tuple(left[right[i]] for i in range(len(left)))


def inverse(p):
    result = [0] * len(p)
    for i, value in enumerate(p):
        result[value] = i
    return tuple(result)


def wreath_multiply(x, y):
    a, b, s = x
    c, d, t = y
    return (compose(a, d), compose(b, c), s ^ t) if s else (compose(a, c), compose(b, d), s ^ t)


def _dimension(n, low, high=None):
    if isinstance(n, bool) or not isinstance(n, int) or n < low or (high is not None and n > high):
        raise ValueError(f"n must be an integer >= {low}" + (f" and <= {high}" if high is not None else ""))


def valid_subgroup(tau):
    """Explicit bounded subgroup listing for controls, not used by recovery."""
    tau = tuple(tau)
    _dimension(len(tau), 3, 4)
    if any(type(x) is not int for x in tau) or sorted(tau) != list(range(len(tau))):
        raise ValueError("tau must be a permutation")
    inv = inverse(tau)
    group = tuple(permutations(range(len(tau))))
    return frozenset([(p, compose(compose(tau, p), inv), 0) for p in group]
                     + [(compose(p, inv), compose(tau, p), 1) for p in group])


def invalid_subgroup_counterexample():
    e, tau, pi = (0, 1, 2), (0, 2, 1), (1, 0, 2)
    proposed = {(p, p, 0) for p in permutations(range(3))}
    proposed |= {(p, compose(p, tau), 1) for p in permutations(range(3))}
    x, y = (e, tau, 1), (pi, pi, 0)
    xy = wreath_multiply(x, y)
    if x not in proposed or y not in proposed or xy in proposed:
        raise ArithmeticError("failed to reproduce nonclosure")
    return {"tau": list(tau), "x": x, "y": y, "product": xy,
            "both_factors_in_proposed_set": True, "product_in_proposed_set": False}


def _transposition(n, i, j):
    p = list(range(n))
    p[i], p[j] = p[j], p[i]
    return tuple(p)


def recover_twisted_diagonal(n, query):
    """Recover tau from opaque labels for LEFT cosets of the promised H_tau.

    The oracle promise is supplied, not established by finitely many probes.
    Only label equality/hashing is used. No secret, evaluator code or subgroup
    enumeration enters the receiver. n=2 is excluded because its conjugation
    action is uninformative.
    """
    _dimension(n, 3)
    if not callable(query):
        raise ValueError("query must be callable")
    e = tuple(range(n))
    calls = 0

    def ask(element):
        nonlocal calls
        calls += 1
        label = query(element)
        try:
            hash(label)
        except TypeError as error:
            raise ValueError("opaque labels must support hashing and equality") from error
        return label

    table = {}
    for i, j in combinations(range(n), 2):
        label = ask((e, _transposition(n, i, j), 0))
        if label in table:
            raise ValueError("distinct right transpositions have colliding labels")
        table[label] = frozenset((i, j))
    images = []
    for i in range(1, n):
        label = ask((_transposition(n, 0, i), e, 0))
        if label not in table:
            raise ValueError("star-transposition image not found in the promised conjugacy class")
        images.append(table[label])
    common = images[0] & images[1]
    if len(common) != 1:
        raise ValueError("star images do not identify a unique common vertex")
    origin = next(iter(common))
    recovered = [origin]
    for pair in images:
        if origin not in pair:
            raise ValueError("inconsistent star-transposition images")
        recovered.append(next(iter(pair - {origin})))
    if sorted(recovered) != list(range(n)):
        raise ValueError("recovered image array is not a permutation")
    tau = tuple(recovered)
    identity_label = ask((e, e, 0))
    if identity_label in table:
        raise ValueError("identity fiber collides with a cached transposition fiber")
    if identity_label != ask((inverse(tau), tau, 1)):
        raise ValueError("recovered permutation fails the original odd-branch coset relation")
    return {"permutation": recovered, "query_count": calls,
            "query_bound": math.comb(n, 2) + n + 1,
            "original_query_relations_verified": True, "source_promise_verified": False,
            "access": "OPAQUE_LABEL_LEFT_COSET_ORACLE_FOR_TWISTED_DIAGONAL_WREATH_SUBGROUP",
            "hidden_permutation_supplied_to_solver": False,
            "general_code_equivalence_solved": False}


def information_profile(n):
    """Exact partition weights with numerical logarithms, not a measurement."""
    from theorems.representation_obstruction import integer_partitions, hook_length_dimension

    _dimension(n, 3, 32)
    dims = [hook_length_dimension(p) for p in integer_partitions(n)]
    order = math.factorial(n)
    if sum(d * d for d in dims) != order:
        raise ArithmeticError("irreducible dimensions do not sum to the group order")
    weights = [Fraction(d * d, order) for d in dims]
    entropy = -sum(float(p) * math.log2(float(p)) for p in weights)
    chi = 2 * sum(float(p) * math.log2(d) for p, d in zip(weights, dims))
    return {"n": n, "partition_count": len(dims), "symmetric_group_order": order,
            "compressed_purity": str(sum((p * p for p in weights), Fraction(0))),
            "raw_regular_coset_purity": str(Fraction(1, order)),
            "plancherel_entropy_bits": entropy, "secret_entropy_bits": math.log2(order),
            "one_copy_holevo_bits": chi,
            "optimal_one_copy_guessing_probability": str(sum((p * p for p in weights), Fraction(0))),
            "trace_distance_from_ensemble_average": str(1 - Fraction(len(dims), order)),
            "optimal_measurement_implemented": False,
            "elementary_holevo_lower_bound_bits": max(0.0, math.log2(order) - (n - 1)),
            "holevo_is_achieved_accessible_information": False,
            "mode": "EXACT_WEIGHTS_NUMERICAL_ENTROPY_NOT_QUANTUM_EXECUTION"}


def _entropy(state):
    state = np.asarray(state)
    if (state.ndim != 2 or state.shape[0] != state.shape[1] or not np.isfinite(state).all()
            or not np.allclose(state, state.conj().T, atol=1e-12, rtol=0)):
        raise ArithmeticError("density matrix must be finite and Hermitian")
    values = np.linalg.eigvalsh(state)
    if values.min() < -1e-10 or abs(values.sum() - 1) > 1e-10:
        raise ArithmeticError("density matrix is not normalized positive semidefinite")
    return -sum(float(v) * math.log2(float(v)) for v in values if v > 1e-12)


def finite_state_control_s3():
    """Build actual 72-dimensional regular coset states, not guessed overlaps."""
    group = tuple(permutations(range(3)))
    ambient = tuple((a, b, s) for a, b, s in product(group, group, (0, 1)))
    index = {g: i for i, g in enumerate(ambient)}
    subgroups = [valid_subgroup(tau) for tau in group]
    raw, compressed = [], []
    helmert = np.array([[1 / math.sqrt(2), 1 / math.sqrt(6)],
                        [-1 / math.sqrt(2), 1 / math.sqrt(6)], [0, -2 / math.sqrt(6)]])
    for tau, subgroup in zip(group, subgroups):
        if len(subgroup) != 12 or any(wreath_multiply(x, y) not in subgroup for x in subgroup for y in subgroup):
            raise ArithmeticError("repaired H_tau is not a subgroup of the asserted order")
        rho = np.zeros((72, 72))
        for i, g in enumerate(ambient):
            for h in subgroup:
                rho[index[wreath_multiply(g, h)], i] += 1 / 72
        raw.append(rho)
        perm = np.zeros((3, 3))
        perm[list(tau), range(3)] = 1
        vector = (helmert.T @ perm @ helmert).reshape(-1) / math.sqrt(2)
        sigma = np.zeros((6, 6))
        sigma[0, 0] = sigma[1, 1] = 1 / 6
        sigma[2:, 2:] = (2 / 3) * np.outer(vector, vector)
        compressed.append(sigma)
    residual = max(abs(float(np.trace(r @ s)) - len(h & k) / 72)
                   for r, h in zip(raw, subgroups) for s, k in zip(raw, subgroups))
    raw_entropies, compressed_entropies = [_entropy(r) for r in raw], [_entropy(r) for r in compressed]
    return {"n": 3, "native_subgroup_order": 12, "ambient_group_order": 72,
            "states_checked": len(group), "pair_overlaps_checked": len(group) ** 2,
            "all_states_normalized_positive": True,
            "raw_purity": float(np.trace(raw[0] @ raw[0])),
            "compressed_purity": float(np.trace(compressed[0] @ compressed[0])),
            "raw_holevo_bits": _entropy(sum(raw) / len(raw)) - sum(raw_entropies) / len(raw),
            "compressed_holevo_bits": _entropy(sum(compressed) / len(compressed)) - sum(compressed_entropies) / len(compressed),
            "raw_overlap_identity_max_residual": residual,
            "mode": "BOUNDED_DENSITY_MATRIX_CONTROL_NOT_QUANTUM_RECEIVER"}


def opaque_oracle_control(tau):
    """Exact opaque-token native coset oracle for finite regression, not a hard input."""
    tau = tuple(tau)
    labels = {}

    def query(element):
        a, b, s = element
        point = compose(compose(b, inverse(tau) if s else tau), inverse(a))
        if point not in labels:
            labels[point] = object()
        return labels[point]

    recovered = recover_twisted_diagonal(len(tau), query)
    if recovered["permutation"] != list(tau):
        raise ArithmeticError("opaque-oracle recovery disagrees with the independently supplied control secret")
    return {"n": len(tau), "query_count": recovered["query_count"],
            "exact_recovery": True, "labels_read_as_permutations": False,
            "mode": "CLASSICAL_REPAIRED_SOURCE_CONTROL_NOT_GENERAL_CODE_EQUIVALENCE"}


def build_report():
    controls = [opaque_oracle_control(tau) for n in (3, 4) for tau in permutations(range(n))]
    controls += [opaque_oracle_control(tuple(reversed(range(n)))) for n in (8, 32, 64)]
    return {"schema_version": 2, "reviewed_on": "2026-10-30",
            "status": "WREATH_SOURCE_CORRECTED_AND_REPAIRED_FAMILY_CLASSICALLY_RECOVERED",
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "invalid_subgroup_counterexample": invalid_subgroup_counterexample(),
            "source_contract": "Valid conjugate of diagonal S_n extended by swap, with exact opaque labels of left cosets; NOT general code equivalence or rigid GI.",
            "repaired_subgroup": "H_tau={(pi,tau*pi*tau^-1,0)} union {(pi*tau^-1,tau*pi,1)}",
            "information_profiles": [information_profile(n) for n in (3, 4, 5, 8, 12, 16, 24, 32)],
            "physical_state_control": finite_state_control_s3(),
            "classical_recovery_controls": controls,
            "classical_query_bound": "binom(n,2)+n+1, n>=3, including odd-branch consistency check",
            "classical_time_scope": "Polynomial image-array work plus charged oracle evaluation and opaque-label comparisons/hashing; no oracle truth table is constructed.",
            "retracted_negative_ids": [NEGATIVE_RESULT_ID],
            "general_copy_lower_bound_proved": False,
            "factorial_holevo_collapse_proved": False,
            "general_code_equivalence_solved": False,
            "quantum_receiver_implemented": False, "speedup_claim_allowed": False,
            "accepted_speedup_candidate": False,
            "summary": "The old subgroup is invalid and information formulas conflict. A valid highly symmetric repair has large Holevo information and polynomial classical recovery under the same full oracle access. This does not solve the hard general problem."}


def write_report(write_registry=True):
    from core.research_registry import _write_json
    from theorems.nonabelian_barrier_scope_audit import quarantine_reviewed_negatives

    report = build_report()
    if write_registry:
        quarantine_reviewed_negatives()
    _write_json(REPORT, report)
    return REPORT


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--no-registry", action="store_true")
    args = parser.parse_args()
    if args.write:
        print(write_report(not args.no_registry))
    else:
        print(json.dumps(build_report(), indent=2))


if __name__ == "__main__":
    main()
