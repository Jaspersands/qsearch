"""Source-linked resource frontier for density-one subset-sum solver ideas.

The partial subset-sum route to DCP needs polynomial time, not merely a better
exponential exponent.  This module records known exact, heuristic, and quantum
frontiers and audits whether a basic balanced Wagner tree has sufficiently long
leaf lists at density one.  It is a resource/assumption gate, not a lower bound
against unknown subset-sum algorithms.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_SUBSET_SUM_RESOURCE_FRONTIER_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_resource_frontier.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-RESOURCE-FRONTIER"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class SubsetSumAlgorithmResource:
    algorithm_id: str
    regime: str
    computation_model: str
    time_exponent_in_n: float
    memory_exponent_in_n: float | None
    theorem_or_heuristic: str
    solves_full_random_instance: bool
    deterministic_interface: bool
    regev_partial_solver_interface_status: str
    source_id: str
    source_url: str
    caveat: str


@dataclass(frozen=True)
class WagnerSplitCertificate:
    n_bits: int
    register_count: int
    register_offset: int
    list_count: int
    tree_depth: int
    average_variables_per_leaf: float
    available_leaf_log2_size: float
    random_list_threshold_log2_size: float
    threshold_deficit_bits: float
    basic_random_list_threshold_met: bool
    representation_expansion_required: bool
    fixed_list_count_leaf_enumeration_exponential: bool
    polynomial_resource_route_established: bool


@dataclass(frozen=True)
class DCPSubsetSumResourceFrontierReport:
    created_at: str
    contract: dict[str, str]
    literature_sources: list[dict[str, str]]
    known_algorithms: list[SubsetSumAlgorithmResource]
    wagner_certificates: list[WagnerSplitCertificate]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def known_subset_sum_resources() -> list[SubsetSumAlgorithmResource]:
    return [
        SubsetSumAlgorithmResource(
            algorithm_id="horowitz-sahni-meet-in-the-middle",
            regime="worst-case binary subset sum",
            computation_model="classical deterministic",
            time_exponent_in_n=0.5,
            memory_exponent_in_n=0.5,
            theorem_or_heuristic="exact algorithm",
            solves_full_random_instance=True,
            deterministic_interface=True,
            regev_partial_solver_interface_status="interface-compatible but exponentially slow",
            source_id="HS74",
            source_url="https://doi.org/10.1145/321812.321823",
            caveat="Exact full solving is stronger than partial coverage, but 2^(n/2) is exponential in log N.",
        ),
        SubsetSumAlgorithmResource(
            algorithm_id="schroeppel-shamir-four-list",
            regime="worst-case binary subset sum",
            computation_model="classical deterministic",
            time_exponent_in_n=0.5,
            memory_exponent_in_n=0.25,
            theorem_or_heuristic="exact algorithm",
            solves_full_random_instance=True,
            deterministic_interface=True,
            regev_partial_solver_interface_status="interface-compatible but exponentially slow",
            source_id="SS81",
            source_url="https://doi.org/10.1137/0210039",
            caveat="The memory improvement does not change exponential time.",
        ),
        SubsetSumAlgorithmResource(
            algorithm_id="seven-way-dissection-low-memory-point",
            regime="random subset sum over a binary domain D of size 2^n",
            computation_model="classical deterministic dissection",
            time_exponent_in_n=4.0 / 7.0,
            memory_exponent_in_n=1.0 / 7.0,
            theorem_or_heuristic="dissection resource theorem for the stated random-instance model",
            solves_full_random_instance=True,
            deterministic_interface=True,
            regev_partial_solver_interface_status="interface-compatible but exponentially slow",
            source_id="DDKS12-and-2022-1329",
            source_url="https://eprint.iacr.org/2022/1329",
            caveat="Dissection trades memory for time; both remain 2^(Theta(n)) at fixed tradeoff points.",
        ),
        SubsetSumAlgorithmResource(
            algorithm_id="bcj-representation",
            regime="random density-one subset sum",
            computation_model="classical randomized/heuristic representation search",
            time_exponent_in_n=0.291,
            memory_exponent_in_n=None,
            theorem_or_heuristic="random-list and representation heuristics",
            solves_full_random_instance=True,
            deterministic_interface=False,
            regev_partial_solver_interface_status="exponential and deterministic matching interface unproved",
            source_id="BCJ11",
            source_url="https://doi.org/10.1007/978-3-642-20465-4_24",
            caveat="A finite optimized exponent and heuristic success model cannot instantiate Regev's deterministic polynomial assumption.",
        ),
        SubsetSumAlgorithmResource(
            algorithm_id="better-sample-representation-tree",
            regime="random density-one subset sum",
            computation_model="classical randomized sampling/representation tree",
            time_exponent_in_n=0.255,
            memory_exponent_in_n=None,
            theorem_or_heuristic="heuristic stochastic analysis",
            solves_full_random_instance=True,
            deterministic_interface=False,
            regev_partial_solver_interface_status="exponential and deterministic matching interface unproved",
            source_id="ARXIV-1907.04295",
            source_url="https://arxiv.org/abs/1907.04295",
            caveat="Increasing representation depth improves a heuristic exponent but does not approach polynomial time.",
        ),
        SubsetSumAlgorithmResource(
            algorithm_id="generalized-representation-classical",
            regime="random density-one subset sum",
            computation_model="classical heuristic representations in {-1,0,1,2}",
            time_exponent_in_n=0.283,
            memory_exponent_in_n=None,
            theorem_or_heuristic="standard classical subset-sum heuristics",
            solves_full_random_instance=True,
            deterministic_interface=False,
            regev_partial_solver_interface_status="exponential and deterministic matching interface unproved",
            source_id="ARXIV-2002.05276",
            source_url="https://arxiv.org/abs/2002.05276",
            caveat="The richer coefficient alphabet changes representation counts but retains exponential resource scaling.",
        ),
        SubsetSumAlgorithmResource(
            algorithm_id="quantum-representation-walk-standard-heuristics",
            regime="random density-one subset sum",
            computation_model="quantum walk/search with quantum-accessible classical or quantum memory",
            time_exponent_in_n=0.218,
            memory_exponent_in_n=None,
            theorem_or_heuristic="standard classical subset-sum heuristics; stronger variant reaches 0.216 with an update heuristic",
            solves_full_random_instance=True,
            deterministic_interface=False,
            regev_partial_solver_interface_status="exponential; new coherent composition theorem required",
            source_id="ARXIV-2002.05276",
            source_url="https://arxiv.org/abs/2002.05276",
            caveat="This is a quantum subexponential improvement, not a polynomial DCP decoder or a drop-in deterministic subroutine.",
        ),
    ]


def wagner_split_certificate(
    n_bits: int,
    register_offset: int,
    list_count: int,
) -> WagnerSplitCertificate:
    if n_bits < 2:
        raise ValueError("n_bits must be at least 2")
    if list_count < 2 or list_count & (list_count - 1):
        raise ValueError("list_count must be a power of two at least 2")
    register_count = n_bits + register_offset
    if register_count < list_count:
        raise ValueError("list_count cannot exceed the number of variables")
    tree_depth = int(math.log2(list_count))
    average_variables = register_count / list_count
    available_log2 = average_variables
    threshold_log2 = n_bits / (tree_depth + 1)
    deficit = threshold_log2 - available_log2
    met = deficit <= 1e-12
    return WagnerSplitCertificate(
        n_bits=n_bits,
        register_count=register_count,
        register_offset=register_offset,
        list_count=list_count,
        tree_depth=tree_depth,
        average_variables_per_leaf=average_variables,
        available_leaf_log2_size=available_log2,
        random_list_threshold_log2_size=threshold_log2,
        threshold_deficit_bits=deficit,
        basic_random_list_threshold_met=met,
        representation_expansion_required=not met,
        fixed_list_count_leaf_enumeration_exponential=average_variables / n_bits > 1e-9,
        polynomial_resource_route_established=False,
    )


def run_subset_sum_resource_frontier(
    n_values: Sequence[int] = (64, 128, 256, 512),
    register_offsets: Sequence[int] = (0, 4, 8),
    list_counts: Sequence[int] = (2, 4, 8, 16),
) -> DCPSubsetSumResourceFrontierReport:
    algorithms = known_subset_sum_resources()
    certificates = [
        wagner_split_certificate(n_bits, offset, list_count)
        for n_bits in n_values
        for offset in register_offsets
        for list_count in list_counts
        if n_bits + offset >= list_count
    ]
    deep = [item for item in certificates if item.list_count >= 4]
    metrics: dict[str, int | float] = {
        "known_algorithm_count": len(algorithms),
        "known_polynomial_time_algorithm_count": sum(item.time_exponent_in_n <= 0.0 for item in algorithms),
        "known_deterministic_interface_algorithm_count": sum(item.deterministic_interface for item in algorithms),
        "known_regev_contract_satisfying_algorithm_count": 0,
        "best_recorded_classical_time_exponent": min(
            item.time_exponent_in_n for item in algorithms if not item.computation_model.startswith("quantum")
        ),
        "best_recorded_quantum_time_exponent": min(
            item.time_exponent_in_n for item in algorithms if item.computation_model.startswith("quantum")
        ),
        "wagner_certificate_count": len(certificates),
        "basic_wagner_threshold_met_count": sum(item.basic_random_list_threshold_met for item in certificates),
        "deep_wagner_certificate_count": len(deep),
        "deep_basic_wagner_threshold_failure_count": sum(
            not item.basic_random_list_threshold_met for item in deep
        ),
        "representation_expansion_required_count": sum(item.representation_expansion_required for item in certificates),
        "polynomial_resource_route_count": 0,
        "source_contract_satisfying_row_count": 0,
    }
    return DCPSubsetSumResourceFrontierReport(
        created_at=utc_now(),
        contract={
            "required_time": "poly(n), where n=log2 N",
            "required_coverage": "inverse-polynomial fraction of legal random density-one inputs",
            "required_interface": "deterministic consistent solver in Regev's source theorem, or a separately proved coherent replacement",
            "wagner_threshold_scope": "balanced independent random-list k-tree heuristic L approximately 2^(n/(log2 k+1)); not a general lower bound",
            "promotion_rule": "an improved positive exponential exponent is negative for the polynomial contract unless a structural collapse to exponent zero is proved",
        },
        literature_sources=[
            {
                "source_id": item.source_id,
                "url": item.source_url,
                "role": item.algorithm_id,
            }
            for item in algorithms
        ],
        known_algorithms=algorithms,
        wagner_certificates=certificates,
        headline_metrics=metrics,
        claim_gate={
            "known_resource_frontier_source_linked": True,
            "exact_and_heuristic_results_separated": True,
            "quantum_memory_and_randomness_interfaces_charged": True,
            "basic_wagner_threshold_is_general_lower_bound": False,
            "known_polynomial_partial_solver_exists": False,
            "source_contract_satisfied": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Every recorded exact, representation, dissection, and quantum route retains a positive exponential "
                "time exponent. Basic deeper Wagner trees lack density-one leaf-list volume without representation "
                "expansion, and representation methods remain heuristic/exponential with an interface mismatch."
            ),
        },
        status="known-subset-sum-frontiers-exponential-polynomial-contract-open",
        summary=(
            f"Recorded {len(algorithms)} source-linked subset-sum frontiers and {len(certificates)} balanced split-tree "
            f"certificates. Best recorded classical/quantum exponents are {metrics['best_recorded_classical_time_exponent']}/"
            f"{metrics['best_recorded_quantum_time_exponent']}; polynomial source-contract rows=0."
        ),
        falsifiers_triggered=[
            "Meet-in-the-middle and Schroeppel-Shamir improve exact resource constants but retain 2^(Theta(n)) time.",
            "Dissection lowers memory at fixed points while retaining a positive time exponent.",
            "Deeper basic Wagner trees at density one need more leaf-list volume than disjoint binary blocks provide.",
            "Representation expansion can repair list volume but all recorded classical routes remain heuristic and exponential.",
            "Known quantum subset-sum exponents remain exponential and require memory/oracle interfaces absent from a deterministic source subroutine.",
            "These are class-specific resource barriers, not a lower bound against unknown structural partial solvers.",
        ],
    )


def write_subset_sum_resource_frontier(
    path: Path = DCP_SUBSET_SUM_RESOURCE_FRONTIER_PATH,
    n_values: Sequence[int] = (64, 128, 256, 512),
    register_offsets: Sequence[int] = (0, 4, 8),
    list_counts: Sequence[int] = (2, 4, 8, 16),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_subset_sum_resource_frontier(n_values, register_offsets, list_counts)
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-KNOWN-SUBSET-SUM-FRONTIERS-REMAIN-EXPONENTIAL",
                source=str(path),
                claim="A known meet-in-the-middle, dissection, Wagner, representation, or quantum subset-sum improvement satisfies Regev's polynomial partial-solver contract.",
                reason_invalid=(
                    "Every recorded route has a positive exponential time exponent; heuristic/randomized/quantum routes "
                    "also lack the deterministic matching interface or a replacement composition theorem."
                ),
                lesson=(
                    "Use these algorithms as mandatory resource baselines. A viable mutation must drive the exponent to zero "
                    "by exploiting new density-one structure and prove legal coverage plus interface compatibility."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "known_algorithm_count": payload["headline_metrics"]["known_algorithm_count"],
                    "best_recorded_classical_time_exponent": payload["headline_metrics"]["best_recorded_classical_time_exponent"],
                    "best_recorded_quantum_time_exponent": payload["headline_metrics"]["best_recorded_quantum_time_exponent"],
                    "known_regev_contract_satisfying_algorithm_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-SUBSET-SUM-RESOURCE-FRONTIER"
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"dcp_subset_sum_resource_frontier": str(path)},
            )
        )
    return payload
