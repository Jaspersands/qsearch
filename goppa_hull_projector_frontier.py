"""Hull-projector reduction on the scalable Goppa frontier.

For a full-rank binary code generator ``G`` with trivial Euclidean hull,

    Sigma_C = G.T (G G.T)^(-1) G

is a basis-independent symmetric idempotent whose image is the code.  Two
such codes are permutation equivalent iff their projector matrices are
simultaneously row/column permutation conjugate.  Diagonal entries become
node colors and off-diagonal ones become graph edges.

This module applies that source-linked reduction directly to Goppa pairs that
survived earlier code-native invariants.  A fixed-round WL-hash mismatch is a
polynomial-time nonequivalence certificate.  A hash collision is not evidence
of hardness and is escalated to exact graph matching or retained as proof debt.
"""

from __future__ import annotations

import json
import random
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import networkx as nx
import numpy as np

from code_hull_projector_reduction import (
    ProjectorCertificate,
    ProjectorGraphMatch,
    certify_hull_projector,
    hull_projector,
    match_trivial_hull_codes,
    projector_graph,
    theorem_certificate,
)
from goppa_scaling_frontier import GOPPA_SCALING_FRONTIER_PATH
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


GOPPA_HULL_PROJECTOR_PATH = Path("research/code_equivalence/goppa_hull_projector_frontier.json")
DEFAULT_EXPERIMENT_ID = "EXP-CODE-GOPPA-HULL-PROJECTOR"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ProjectorInvariantSignature:
    length: int
    loop_weight_count: int
    degree_histogram: list[list[int]]
    loop_degree_histogram: list[list[int]]
    wl_iterations: int
    wl_hash: str

    @property
    def key(self) -> tuple[Any, ...]:
        return (
            self.length,
            self.loop_weight_count,
            tuple(tuple(item) for item in self.degree_histogram),
            tuple(tuple(item) for item in self.loop_degree_histogram),
            self.wl_iterations,
            self.wl_hash,
        )


@dataclass(frozen=True)
class GoppaProjectorInstance:
    instance_id: str
    certificate: ProjectorCertificate
    signature: ProjectorInvariantSignature | None


@dataclass(frozen=True)
class GoppaProjectorPairAudit:
    id: str
    family_id: str
    left_id: str
    right_id: str
    known_equivalent: bool
    prior_status: str | None
    both_trivial_hull_certified: bool
    polynomial_signatures_match: bool | None
    graph_match: ProjectorGraphMatch | None
    status: str
    interpretation: str


@dataclass(frozen=True)
class GoppaProjectorFamilyRecord:
    family_id: str
    instances: list[GoppaProjectorInstance]
    control_audits: list[GoppaProjectorPairAudit]
    pair_audits: list[GoppaProjectorPairAudit]
    frontier_pair_count: int
    polynomial_projector_rejection_count: int
    exact_graph_rejection_count: int
    equivalent_or_automorphic_count: int
    projector_proof_debt_count: int
    status: str
    interpretation: str


@dataclass(frozen=True)
class GoppaHullProjectorReport:
    created_at: str
    source_artifact: str
    theorem: dict[str, Any]
    records: list[GoppaProjectorFamilyRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _histogram(values: list[int]) -> list[list[int]]:
    return [[int(value), int(count)] for value, count in sorted(Counter(values).items())]


def projector_invariant_signature(generator: np.ndarray, wl_iterations: int = 8) -> ProjectorInvariantSignature | None:
    projector = hull_projector(generator)
    if projector is None:
        return None
    graph = projector_graph(projector)
    degrees = [int(graph.degree(vertex)) for vertex in graph.nodes]
    loop_degrees = [
        2 * degrees[vertex] + int(graph.nodes[vertex]["loop_weight"])
        for vertex in graph.nodes
    ]
    return ProjectorInvariantSignature(
        length=int(projector.shape[0]),
        loop_weight_count=int(np.trace(projector)),
        degree_histogram=_histogram(degrees),
        loop_degree_histogram=_histogram(loop_degrees),
        wl_iterations=int(wl_iterations),
        wl_hash=nx.weisfeiler_lehman_graph_hash(
            graph,
            node_attr="loop_weight",
            iterations=int(wl_iterations),
        ),
    )


def projector_instance(instance: dict[str, Any], seed: int = 0) -> GoppaProjectorInstance:
    generator = np.asarray(instance["generator"], dtype=np.uint8) & 1
    certificate = certify_hull_projector(generator, seed=seed)
    signature = (
        projector_invariant_signature(generator)
        if certificate.status == "trivial-hull-projector-certified"
        else None
    )
    return GoppaProjectorInstance(
        instance_id=str(instance["id"]),
        certificate=certificate,
        signature=signature,
    )


def audit_projector_pair(
    family_id: str,
    left_source: dict[str, Any],
    right_source: dict[str, Any],
    left: GoppaProjectorInstance,
    right: GoppaProjectorInstance,
    *,
    audit_id: str,
    known_equivalent: bool,
    prior_status: str | None = None,
    max_search_seconds: float = 10.0,
) -> GoppaProjectorPairAudit:
    certified = (
        left.certificate.status == "trivial-hull-projector-certified"
        and right.certificate.status == "trivial-hull-projector-certified"
        and left.signature is not None
        and right.signature is not None
    )
    signatures_match = left.signature.key == right.signature.key if certified else None
    graph_match: ProjectorGraphMatch | None = None
    if certified and (known_equivalent or signatures_match):
        graph_match = match_trivial_hull_codes(
            np.asarray(left_source["generator"], dtype=np.uint8),
            np.asarray(right_source["generator"], dtype=np.uint8),
            max_search_seconds=max_search_seconds,
        )
    if known_equivalent:
        passed = certified and signatures_match and graph_match is not None and graph_match.status == "projector-graph-equivalence-witness-verified"
        if not certified:
            status = "equivalent-control-projector-inapplicable-nontrivial-hull"
            interpretation = (
                "The known equivalent control has nontrivial hull, so the direct projector theorem is inapplicable rather than failed."
            )
        else:
            status = "equivalent-control-goppa-projector-witness-verified" if passed else "control-failure-goppa-projector"
            interpretation = (
                "Known coordinate permutation preserves the projector signature and yields a verified code-space mapping."
                if passed
                else "The hull-projector pipeline failed a known coordinate-permutation control."
            )
    elif certified and signatures_match is False:
        status = "rejected-by-polynomial-goppa-projector-invariant"
        interpretation = (
            "The basis-independent projector graphs have different loop/degree/WL signatures, proving code nonequivalence in polynomial time."
        )
    elif graph_match is not None and graph_match.status == "projector-graphs-nonisomorphic-code-nonequivalence-certified":
        status = "rejected-by-exact-goppa-projector-graph"
        interpretation = graph_match.interpretation
    elif graph_match is not None and graph_match.status == "projector-graph-equivalence-witness-verified":
        status = "goppa-projector-equivalent-or-automorphic-control"
        interpretation = (
            "The projector graph matcher recovered and verified a coordinate permutation; this row is equivalent, not a hard nonequivalent pair."
        )
    elif prior_status == "rejected-by-scalable-goppa-invariant":
        status = "prior-classical-rejection-preserved-projector-inapplicable"
        interpretation = "A prior exact scalable invariant already rejects this pair; projector applicability does not reopen it."
    elif not certified:
        status = "goppa-projector-nontrivial-hull-proof-debt"
        interpretation = (
            "At least one Gram matrix is singular, so the direct trivial-hull projector theorem is unavailable. Apply the source shortening reduction."
        )
    elif graph_match is not None and graph_match.timed_out:
        status = "goppa-projector-graph-match-timeout-proof-debt"
        interpretation = graph_match.interpretation
    else:
        status = "goppa-projector-signature-collision-proof-debt"
        interpretation = (
            "Projector signatures collide without a verified graph decision. This is graph-isomorphism proof debt, not code-native hardness evidence."
        )
    return GoppaProjectorPairAudit(
        id=audit_id,
        family_id=family_id,
        left_id=left.instance_id,
        right_id=right.instance_id,
        known_equivalent=known_equivalent,
        prior_status=prior_status,
        both_trivial_hull_certified=certified,
        polynomial_signatures_match=signatures_match,
        graph_match=graph_match,
        status=status,
        interpretation=interpretation,
    )


def _permuted_instance(instance: dict[str, Any], seed: int) -> dict[str, Any]:
    generator = np.asarray(instance["generator"], dtype=np.uint8)
    permutation = list(range(generator.shape[1]))
    random.Random(seed).shuffle(permutation)
    return {"id": f"{instance['id']}-permuted", "generator": generator[:, permutation].tolist()}


def run_goppa_hull_projector_frontier(
    scaling_path: Path = GOPPA_SCALING_FRONTIER_PATH,
    max_search_seconds: float = 10.0,
) -> GoppaHullProjectorReport:
    if not scaling_path.exists():
        raise FileNotFoundError(
            f"missing scalable Goppa artifact {scaling_path}; run `python qsearch.py code-goppa-scaling` first"
        )
    source = json.loads(scaling_path.read_text())
    records: list[GoppaProjectorFamilyRecord] = []
    for family_index, source_family in enumerate(source["records"]):
        family_id = str(source_family["spec"]["id"])
        instances = [
            projector_instance(instance, seed=71_003 * (family_index + 1) + index)
            for index, instance in enumerate(source_family["instances"])
        ]
        sources = {str(item["id"]): item for item in source_family["instances"]}
        by_id = {item.instance_id: item for item in instances}
        audits = [
            audit_projector_pair(
                family_id,
                sources[str(audit["left_id"])],
                sources[str(audit["right_id"])],
                by_id[str(audit["left_id"])],
                by_id[str(audit["right_id"])],
                audit_id=str(audit["id"]),
                known_equivalent=False,
                prior_status=str(audit["status"]),
                max_search_seconds=max_search_seconds,
            )
            for audit in source_family["collision_audits"]
        ]
        controls: list[GoppaProjectorPairAudit] = []
        if source_family["instances"]:
            left_source = source_family["instances"][0]
            right_source = _permuted_instance(left_source, 97_003 + family_index)
            right_instance = projector_instance(right_source, seed=191_003 + family_index)
            controls.append(
                audit_projector_pair(
                    family_id,
                    left_source,
                    right_source,
                    instances[0],
                    right_instance,
                    audit_id=f"{family_id}-known-permutation-projector-control",
                    known_equivalent=True,
                    max_search_seconds=max_search_seconds,
                )
            )
        frontier = [audit for audit in audits if audit.prior_status != "rejected-by-scalable-goppa-invariant"]
        poly_rejections = sum(audit.status == "rejected-by-polynomial-goppa-projector-invariant" for audit in frontier)
        exact_rejections = sum(audit.status == "rejected-by-exact-goppa-projector-graph" for audit in frontier)
        equivalent = sum(audit.status == "goppa-projector-equivalent-or-automorphic-control" for audit in frontier)
        proof_debt = sum("proof-debt" in audit.status for audit in frontier)
        control_failures = sum(audit.status.startswith("control-failure") for audit in controls)
        if control_failures:
            status = "rejected-goppa-projector-pipeline-control-failure"
            interpretation = "A known coordinate permutation failed the projector reduction control."
        elif proof_debt:
            status = "goppa-projector-frontier-proof-debt"
            interpretation = f"{proof_debt} frontier pair(s) remain unresolved after the projector reduction."
        elif frontier:
            status = "goppa-projector-frontier-classically-resolved"
            interpretation = f"All {len(frontier)} previously unresolved pair(s) are classically rejected or verified equivalent."
        else:
            status = "no-unresolved-goppa-projector-frontier-pair"
            interpretation = "Earlier scalable invariants already resolved every audited pair in this family."
        records.append(
            GoppaProjectorFamilyRecord(
                family_id=family_id,
                instances=instances,
                control_audits=controls,
                pair_audits=audits,
                frontier_pair_count=len(frontier),
                polynomial_projector_rejection_count=poly_rejections,
                exact_graph_rejection_count=exact_rejections,
                equivalent_or_automorphic_count=equivalent,
                projector_proof_debt_count=proof_debt,
                status=status,
                interpretation=interpretation,
            )
        )
    metrics: dict[str, int | float] = {
        "family_count": len(records),
        "instance_count": sum(len(record.instances) for record in records),
        "trivial_hull_certificate_count": sum(
            instance.certificate.status == "trivial-hull-projector-certified"
            for record in records
            for instance in record.instances
        ),
        "frontier_pair_count": sum(record.frontier_pair_count for record in records),
        "polynomial_projector_rejection_count": sum(record.polynomial_projector_rejection_count for record in records),
        "exact_graph_rejection_count": sum(record.exact_graph_rejection_count for record in records),
        "equivalent_or_automorphic_count": sum(record.equivalent_or_automorphic_count for record in records),
        "projector_proof_debt_count": sum(record.projector_proof_debt_count for record in records),
        "known_permutation_control_count": sum(len(record.control_audits) for record in records),
        "control_failure_count": sum(
            audit.status.startswith("control-failure")
            for record in records
            for audit in record.control_audits
        ),
        "control_inapplicable_count": sum(
            audit.status == "equivalent-control-projector-inapplicable-nontrivial-hull"
            for record in records
            for audit in record.control_audits
        ),
        "code_native_hard_pair_count": 0,
        "classical_superpolynomial_lower_bound_count": 0,
        "nonabelian_measurement_necessity_proof_count": 0,
    }
    resolved = int(metrics["polynomial_projector_rejection_count"] + metrics["exact_graph_rejection_count"] + metrics["equivalent_or_automorphic_count"])
    status = (
        "goppa-projector-controls-failed"
        if metrics["control_failure_count"]
        else "goppa-projector-frontier-resolved-no-code-native-hard-row"
        if metrics["projector_proof_debt_count"] == 0
        else "goppa-projector-frontier-proof-debt-only"
    )
    return GoppaHullProjectorReport(
        created_at=utc_now(),
        source_artifact=str(scaling_path),
        theorem=asdict(theorem_certificate()),
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "explicit_public_generators_available": True,
            "trivial_hull_projector_reduction_legal": True,
            "wl_hash_mismatch_is_polynomial_nonequivalence_certificate": True,
            "wl_hash_collision_is_hardness_evidence": False,
            "gi_reduction_is_polynomial_gi_solver": False,
            "code_native_hard_pair_survives": metrics["projector_proof_debt_count"] > 0,
            "classical_superpolynomial_lower_bound_proved": False,
            "nonabelian_measurement_necessity_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Public trivial-hull generators expose a basis-independent projector reduction. Polynomial invariant "
                "mismatches reject code equivalence; collisions only transfer debt to graph isomorphism."
            ),
        },
        status=status,
        summary=(
            f"Applied the trivial-hull projector reduction to {metrics['frontier_pair_count']} scalable Goppa frontier pair(s); "
            f"resolved={resolved}, remaining proof debt={metrics['projector_proof_debt_count']}."
        ),
        falsifiers_triggered=[
            "A trivial-hull public generator exposes the exact basis-independent projector reduction.",
            "Different loop/degree/WL projector signatures prove nonequivalence in polynomial time.",
            "A verified projector-graph mapping proves the row is equivalent rather than hard.",
            "A projector signature collision only transfers the row to graph-isomorphism debt.",
            "A finite exact matcher timeout is not a classical lower bound or quantum signal.",
        ],
    )


def write_goppa_hull_projector_frontier(
    path: Path = GOPPA_HULL_PROJECTOR_PATH,
    scaling_path: Path = GOPPA_SCALING_FRONTIER_PATH,
    max_search_seconds: float = 10.0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(
        run_goppa_hull_projector_frontier(
            scaling_path=scaling_path,
            max_search_seconds=max_search_seconds,
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        for record in payload["records"]:
            for audit in record["pair_audits"]:
                if audit["status"] not in {
                    "rejected-by-polynomial-goppa-projector-invariant",
                    "rejected-by-exact-goppa-projector-graph",
                    "goppa-projector-equivalent-or-automorphic-control",
                }:
                    continue
                upsert_negative_result(
                    NegativeResultRecord(
                        id=f"NEG-CODE-GOPPA-PROJECTOR-{audit['id'].upper()}",
                        source=str(path),
                        claim=f"{audit['id']} remains a code-native hard row after public-generator preprocessing.",
                        reason_invalid=audit["interpretation"],
                        lesson=(
                            "Audit the Euclidean hull and apply the basis-independent projector before treating a public "
                            "code generator as a nonabelian-HSP frontier instance."
                        ),
                        applies_to=[registry_candidate_id, registry_experiment_id],
                        evidence=audit,
                    )
                )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=registry_result_id or f"RESULT-{registry_experiment_id}-LATEST",
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"goppa_hull_projector_frontier": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    print(json.dumps(write_goppa_hull_projector_frontier()["headline_metrics"], indent=2, sort_keys=True))
