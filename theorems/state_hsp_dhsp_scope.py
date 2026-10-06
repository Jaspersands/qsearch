"""StateHSP literature applicability audit for the existing DHSP source.

LOCAL DERIVATION / REVIEW PENDING. SymPy supplies bounded group algebra.
No proposed toy oracle, generic impossibility theorem or new decoder.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
import json
import math
from pathlib import Path
import random

import numpy as np
from sympy import divisors
from sympy.combinatorics.named_groups import DihedralGroup
from sympy.combinatorics.perm_groups import PermutationGroup

from dhsp_codomain_instrument import _integer, rational

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/state_hsp_dhsp_scope.json"


@lru_cache(maxsize=16)
def geometry(N):
    _integer(N, "rotation order", 3)
    if N > 32:
        raise ValueError("subgroup enumeration is calibration only, N<=32")
    group = DihedralGroup(N)
    rotation, reflection = group.generators
    elements = [rotation**x * reflection**b for b in range(2) for x in range(N)]
    index = {g: i for i, g in enumerate(elements)}
    assert len(index) == 2*N == group.order()
    conjugate = [[index[g*h*g**-1] for h in elements] for g in elements]
    all_subgroups = set()
    for d in divisors(N):
        generators = [rotation**int(d)]
        all_subgroups.add(frozenset(index[g] for g in PermutationGroup(generators).generate_schreier_sims()))
        for a in range(int(d)):
            H = PermutationGroup(generators+[rotation**a * reflection])
            all_subgroups.add(frozenset(index[g] for g in H.generate_schreier_sims()))
    center = [i for i in range(2*N) if all(conjugate[i][j] == j for j in range(2*N))]
    baer = [i for i in range(2*N) if all(frozenset(conjugate[i][j] for j in H) == H for H in all_subgroups)]
    assert set(baer) == set(center)
    assert len(center) == math.gcd(N, 2)
    return {"elements": elements, "index": index, "conjugate": conjugate,
            "center": center, "baer": baer, "subgroups": all_subgroups}


def weak_distribution(N, shift):
    _integer(N, "rotation order", 3)
    _integer(shift, "canonical hidden shift", 0)
    if shift >= N:
        raise ValueError("canonical shift required")
    probabilities = {}
    for a in ((1, -1) if N % 2 == 0 else (1,)):
        for b in (1, -1):
            probabilities[f"one-dim:a={a},b={b}"] = Fraction(1+a**shift*b, 2*N)
    for k in range(1, (N+1)//2):
        probabilities[f"two-dim:k={k}"] = Fraction(2, N)
    assert sum(probabilities.values()) == 1
    return probabilities


def graph_control(N, shift, seed=43001):
    g = geometry(N)
    _integer(shift, "canonical hidden shift", 0)
    if shift >= N:
        raise ValueError("canonical shift required")
    elements, index = g["elements"], g["index"]
    H = {0, N+shift}
    core = set.intersection(*(set(row[h] for h in H) for row in g["conjugate"]))
    assert core == {0}
    normalizer = [i for i, row in enumerate(g["conjugate"]) if set(row[h] for h in H) == H]
    label_count = 1 << (N-1).bit_length()
    pi = list(range(N))
    random.Random(seed).shuffle(pi)
    source = np.array([pi[(x-b*shift) % N] for b in range(2) for x in range(N)], dtype=int)
    graph = np.zeros((2*N, label_count), complex)
    graph[np.arange(2*N), source] = 1/math.sqrt(2*N)
    overlaps = []
    for h in elements:
        target = [index[a*h**-1] for a in elements]
        transformed = np.empty_like(graph)
        transformed[target] = graph
        overlaps.append(float(np.vdot(graph, transformed).real))
    assert all(abs(value-int(i in H)) < 1e-12 for i, value in enumerate(overlaps))
    # Execute A^{-1}: self-inverse XOR oracle then inverse known uniform prep.
    uncomputed = np.empty_like(graph)
    for i in range(2*N):
        uncomputed[i, np.arange(label_count) ^ source[i]] = graph[i]
    returned = np.fft.fft(uncomputed, axis=0)/math.sqrt(2*N)
    inverse_return = float(abs(returned[0, 0])**2)
    exact_probabilities = weak_distribution(N, shift)
    numeric = {}
    for name in exact_probabilities:
        if name.startswith("one"):
            a, b = map(int, name.split(":")[1].replace("a=", "").replace("b=", "").split(","))
            chars = [a**x*b**c for c in range(2) for x in range(N)]
            dimension = 1
        else:
            k = int(name.split("=")[1])
            chars = [2*math.cos(2*math.pi*k*x/N) if not c else 0 for c in range(2) for x in range(N)]
            dimension = 2
        numeric[name] = dimension*sum(a*b for a, b in zip(chars, overlaps))/(2*N)
        assert abs(numeric[name]-float(exact_probabilities[name])) < 1e-12
    return {"rotation_order": N, "hidden_shift_calibration": shift, "seed": seed,
            "group_order": 2*N, "source_label_permutation": pi, "source_labels": source.tolist(),
            "graph_representation_overlaps": overlaps, "hidden_reflection_subgroup_indices": sorted(H),
            "normal_core_indices": sorted(core), "reflection_normalizer_indices": normalizer,
            "all_subgroup_count": len(g["subgroups"]), "baer_norm_indices": g["baer"],
            "center_indices": g["center"], "baer_and_center_index": 2*N//len(g["center"]),
            "rotation_subgroup_index": 2,
            "rotation_restriction_stabilizer": [0],
            "abelianization_distinct_shift_images": math.gcd(N, 2),
            "weak_irrep_probabilities": {name: rational(p) for name, p in exact_probabilities.items()},
            "executed_character_probabilities": numeric,
            "graph_state_norm": float(np.vdot(graph, graph).real),
            "executed_A_inverse_return_probability": inverse_return,
            "unknown_oracle_calls_for_A": 1, "unknown_oracle_calls_for_A_inverse": 1,
            "minimum_asymmetry_gap": 1,
            "normal_core_output_recovers_shift": False,
            "abelian_theorem_applies_to_full_group": False,
            "coherent_access_lacking_is_the_blocker": False,
            "irreducible_quantum_blocks_declared_uninformative": False}


def run_controls():
    controls = [graph_control(N, s) for N in (3, 4, 5, 6, 8, 12, 16) for s in range(N)]
    ledgers = [{"rotation_order": str(1 << n), "rotation_order_bits": n,
                "group_order": str(1 << (n+1)), "center_order": 2,
                "baer_norm_order": 2, "center_and_baer_index": str(1 << n),
                "rotation_subgroup_index": 2,
                "uniform_shift_weak_irrep_information_bits": rational(Fraction(1, 1 << n)),
                "full_shift_images_in_abelianization": 2,
                "poly_near_hamiltonian_family": False,
                "poly_near_abelian_family": False} for n in (8, 16, 32, 64, 128)]
    return {"status": "STATE_HSP_DHSP_APPLICABILITY_LOCAL_SCOPE_AUDIT_REVIEW_PENDING",
            "primary_sources": ["https://arxiv.org/html/2609.38085v1", "https://arxiv.org/html/2609.35656v1"],
            "graph_controls": controls, "exponential_order_ledgers": ledgers,
            "theorem_transfer": {"normal_core_theorem": "applies, but exact core is trivial for every reflection shift",
                                 "poly_near_hamiltonian": "not applicable to the growing dihedral family; Baer index is exponential",
                                 "poly_near_abelian": "center-index definition, NOT existence of an index-two abelian subgroup",
                                 "abelian_query_access_theorem": "not applicable to nonabelian D_N; A and inverse are already accessible",
                                 "projective_abelian_linearisation": "does not remove nonabelian reflection-conjugacy information"},
            "claim_gate": {"accepted_candidate": False, "new_algorithm": False,
                           "new_papers_refuted": False, "general_state_HSP_impossibility": False,
                           "full_irrep_block_information_excluded": False, "independent_theorem_review": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = run_controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"report": str(args.output), "all_shift_controls": len(report["graph_controls"]),
                      "normal_core_decodes_shift": False, "candidate_accepted": False}))


if __name__ == "__main__":
    main()
