"""Signed-tensor centralizer access: exact degree and natural-source budget.

Orellana's signed-permutation tensor rule moves one box between the two
bipartition components. This is NOT the Specht-restriction problem itself.
We audit whether using that diagram construction could even cover its
required K-types before asking for a coherent embedding.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

from coset_hidden_involution_paired_tower_missing_label_boundary import (
    bipartitions, removable_corner_partitions,
)
from coset_hidden_involution_natural_recoupling_boundary import hyperoctahedral_irrep_dimension
from research_registry import utc_now

REPORT_PATH = Path("research/representation/coset_hidden_involution_signed_tensor_access.json")
DEFAULT_EXPERIMENT_ID = "EXP-COSET-HIDDEN-INVOLUTION-SIGNED-TENSOR-ACCESS"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
PAPER_URL = "https://math.dartmouth.edu/~orellana/hcentpart.pdf"
Partition = tuple[int, ...]
Bipartition = tuple[Partition, Partition]


def _validate_partition(partition: Partition) -> None:
    if any(type(value) is not int or value <= 0 for value in partition) or tuple(sorted(partition, reverse=True)) != partition:
        raise ValueError("partition must be a nonincreasing tuple of positive integers")


def minimum_signed_tensor_degree(alpha: Partition, beta: Partition) -> int:
    """Exact shortest degree from ((m),()) in the signed-tensor Bratteli graph."""
    _validate_partition(alpha)
    _validate_partition(beta)
    return sum(beta) + 2 * (sum(alpha) - (alpha[0] if alpha else 0))


def _add_box(partition: Partition) -> tuple[Partition, ...]:
    results = []
    for row in range(len(partition) + 1):
        if row and row < len(partition) and partition[row] == partition[row - 1]:
            continue
        target = list(partition)
        if row == len(partition):
            target.append(1)
        else:
            target[row] += 1
        results.append(tuple(target))
    return tuple(results)


def signed_tensor_step(decomposition: dict[Bipartition, int]) -> dict[Bipartition, int]:
    result: Counter[Bipartition] = Counter()
    for (alpha, beta), multiplicity in decomposition.items():
        for reduced in removable_corner_partitions(alpha):
            for enlarged in _add_box(beta):
                result[(reduced, enlarged)] += multiplicity
        for reduced in removable_corner_partitions(beta):
            for enlarged in _add_box(alpha):
                result[(enlarged, reduced)] += multiplicity
    return dict(result)


def signed_tensor_source_mass_bound(rank: int, degree_budget: int) -> Fraction:
    """Necessary K-type coverage in tensor degrees <=budget; exact rational upper bound.

The h-even K-Plancherel marginal has A=|alpha| binomial(rank,1/2)
conditioned on rank-A even. Conditional alpha has Plancherel law on S_A.
RSK plus the expected count of increasing L-subsequences bounds its first row.
"""
    if type(rank) is not int or rank < 2 or type(degree_budget) is not int or degree_budget < 0:
        raise ValueError("rank must be an integer >=2 and degree_budget nonnegative")
    total = Fraction(0)
    for a in range(rank + 1):
        if (rank - a) % 2:
            continue
        required_first_row = max(0, (rank + a - degree_budget + 1) // 2)
        if required_first_row > a:
            continue
        lis_bound = min(Fraction(1), Fraction(math.comb(a, required_first_row), math.factorial(required_first_row)))
        total += Fraction(math.comb(rank, a), 2**(rank - 1)) * lis_bound
    return min(Fraction(1), total)


def signed_tensor_degree_control(rank: int) -> dict[str, Any]:
    if type(rank) is not int or not 2 <= rank <= 8:
        raise ValueError("exact Bratteli controls use ranks 2..8")
    decomposition: dict[Bipartition, int] = {((rank,), ()): 1}
    first_seen: dict[Bipartition, int] = {}
    dimensions_ok = True
    parity_ok = True
    for degree in range(2 * rank + 1):
        dimensions_ok &= sum(mult * hyperoctahedral_irrep_dimension(*pair)
                             for pair, mult in decomposition.items()) == rank**degree
        for pair in decomposition:
            first_seen.setdefault(pair, degree)
            parity_ok &= sum(pair[1]) % 2 == degree % 2
        decomposition = signed_tensor_step(decomposition)
    pairs = bipartitions(rank)
    formula_ok = len(first_seen) == len(pairs) and all(
        first_seen[pair] == minimum_signed_tensor_degree(*pair) for pair in pairs)
    denominator = 2**(rank - 1) * math.factorial(rank)
    even_pairs = [pair for pair in pairs if sum(pair[1]) % 2 == 0]
    assert sum(hyperoctahedral_irrep_dimension(*pair)**2 for pair in even_pairs) == denominator
    covered = Fraction(sum(hyperoctahedral_irrep_dimension(*pair)**2 for pair in even_pairs
                           if minimum_signed_tensor_degree(*pair) <= rank), denominator)
    upper = signed_tensor_source_mass_bound(rank, rank)
    return {"rank": rank, "bipartition_count": len(pairs),
            "tensor_dimension_identities_exact": bool(dimensions_ok),
            "central_parity_identities_exact": bool(parity_ok),
            "minimum_degree_formula_matches_all_types": bool(formula_ok),
            "degree_at_most_rank_exact_source_mass": str(covered),
            "analytic_upper_bound": str(upper), "source_bound_respected": covered <= upper}


def build_signed_tensor_access_report() -> dict[str, Any]:
    controls = [signed_tensor_degree_control(rank) for rank in range(2, 7)]
    scaling = []
    for rank in (8, 16, 32, 64, 128, 256):
        bound = signed_tensor_source_mass_bound(rank, rank)
        scaling.append({"rank": rank, "maximum_faithful_tensor_degree": rank,
                        "source_coverage_upper_bound": str(bound),
                        "log2_display": math.log2(bound.numerator) - math.log2(bound.denominator)})
    exact_checks = all(row["tensor_dimension_identities_exact"] and row["central_parity_identities_exact"]
                       and row["minimum_degree_formula_matches_all_types"] and row["source_bound_respected"] for row in controls)
    return {
        "created_at": utc_now(), "status": "faithful-signed-tensor-diagram-route-source-negligible",
        "summary": "The faithful even-partition diagram range k<=m covers exponentially vanishing necessary K-type source mass. A useful signed-tensor approach must handle a nonfaithful quotient or a different embedding.",
        "derivation_document": "research/SIGNED_TENSOR_ACCESS.md",
        "literature": [{"url": PAPER_URL, "location": "Theorem 2.1 and Section 3",
                        "scope": "signed permutation tensor powers, not arbitrary Specht restrictions"}],
        "finite_controls": controls, "scaling_records": scaling,
        "headline_metrics": {"exact_degree_controls_passed": sum(row["minimum_degree_formula_matches_all_types"] for row in controls),
                             "source_mass_scaling_record_count": len(scaling), "coherent_embedding_count": 0,
                             "formal_proof_count": 0},
        "claim_gate": {"exact_finite_controls_passed": exact_checks,
                       "faithful_range_source_coverage_obstruction_derived": True,
                       "all_signed_tensor_algorithms_ruled_out": False,
                       "specht_to_tensor_embedding_compiled": False, "small_parameter_quotient_transform_compiled": False,
                       "speedup_claim_allowed": False},
        "assumptions": ["Use the signed permutation module of K_m, not a different tensor alphabet.",
                        "Cover the unpostselected h-even K-Plancherel marginal of the branching source.",
                        "Restrict to tensor degrees k<=m where every even orbital diagram remains nonzero.",
                        "K-type reachability is only necessary, not sufficient, for a multiplicity-preserving embedding."],
        "falsifiers_triggered": ["Stable diagram labels cannot be assumed to cover typical Specht restriction K-types.",
                                  "The signed tensor centralizer is not automatically the target copy algebra."],
        "next_experiments": ["Construct the required Specht-to-signed-tensor intertwiner and charge its normalization.",
                             "Work in the physical even-partition quotient at k>m; quantify its Gram kernel and source support.",
                             "Compare an implicit-copy-register algorithm which bypasses explicit tensor embeddings."],
    }


def write_signed_tensor_access_report(path: Path = REPORT_PATH, *, write_registry: bool = True,
                                     registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
                                     registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
                                     registry_result_id: str = "") -> dict[str, Any]:
    payload = build_signed_tensor_access_report()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (ExperimentRecord, ExperimentResultRecord, NegativeResultRecord,
                                       upsert_experiment, upsert_experiment_result, upsert_negative_result)
        upsert_experiment(ExperimentRecord(
            id=registry_experiment_id, candidate_id=registry_candidate_id,
            title="Signed-tensor diagram access and natural source coverage", status=payload["status"],
            hypothesis="A faithful signed-tensor centralizer representation covers typical required K-types.",
            protocol="Check exact tensor-degree paths, dimensions and parity; compare the h-even Plancherel marginal with a first-row tail bound.",
            positive_signal="An explicit source-preserving quotient or alternative embedding avoids the faithful-range mass obstruction.",
            falsifiers=["degree bound misses a Bratteli path", "source normalization fails", "coverage vanishes in the faithful diagram regime"],
            metrics=list(payload["headline_metrics"]), dependencies=[PAPER_URL, "exact branching source marginal"],
            next_actions=payload["next_experiments"],
        ))
        upsert_experiment_result(ExperimentResultRecord(
            id=registry_result_id or f"RESULT-{registry_experiment_id}", experiment_id=registry_experiment_id,
            candidate_id=registry_candidate_id, created_at=payload["created_at"], status=payload["status"],
            summary=payload["summary"], metrics=payload["headline_metrics"],
            falsifiers_triggered=payload["falsifiers_triggered"], artifacts={"signed_tensor_access": str(path)},
        ))
        upsert_negative_result(NegativeResultRecord(
            id="FAITHFUL-SIGNED-TENSOR-DIAGRAM-RANGE-MISSES-TYPICAL-SOURCE",
            source=registry_experiment_id, claim="Faithful signed-tensor diagram bases directly cover typical hidden-involution branching labels.",
            reason_invalid="The exact shortest degree is |beta|+2(|alpha|-alpha_1); degrees at most m cover exponentially vanishing necessary K-type mass under the h-even marginal.",
            lesson="Do not substitute a signed tensor centralizer for Specht restriction. Supply a normalized intertwiner and handle the nonfaithful quotient, or use a different representation.",
            applies_to=[registry_candidate_id, "faithful signed-permutation tensor embeddings"],
            evidence={"artifact": str(path), "derivation": payload["derivation_document"]},
        ))
    return payload
