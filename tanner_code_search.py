"""Tanner/LDPC-style code-family search for code-equivalence frontiers.

Tanner codes are a natural place where code equivalence, graph structure, and
nonabelian hidden-permutation questions meet.  This module generates small
regular bipartite Tanner graphs, turns their parity-check matrices into binary
linear codes, searches for tuple-profile collisions, and immediately attacks
every row with Tanner-graph isomorphism, code structural invariants,
information-set canonicalization, and profile-pruned canonicalization.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any

import networkx as nx
import numpy as np

from code_canonicalization_baseline import audit_code_canonicalization_pair
from code_equivalence_workbench import codeword_int_set, gf2_rank
from code_family_search import gf2_nullspace_basis, strong_invariant_differences
from code_information_set_baseline import audit_code_information_set_pair
from code_tuple_profile_baseline import audit_code_tuple_profile_pair, tuple_profile_key
from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


CODE_EQUIVALENCE_DIR = Path("research/code_equivalence")
TANNER_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "tanner_code_search.json"


@dataclass(frozen=True)
class TannerSearchSpec:
    id: str
    variable_count: int
    check_count: int
    variable_degree: int
    check_degree: int
    max_trials: int
    max_collisions: int
    seed: int
    tuple_size: int = 2
    min_dimension: int = 2
    max_dimension: int = 12


@dataclass(frozen=True)
class TannerCodeDescriptor:
    parity_check: list[list[int]]
    generator: list[list[int]]
    variable_count: int
    check_count: int
    dimension: int
    rank: int


@dataclass(frozen=True)
class TannerGraphCertificate:
    evaluated: bool
    isomorphic: bool | None
    node_count: int
    edge_count: int
    interpretation: str


@dataclass(frozen=True)
class TannerCollisionAudit:
    id: str
    length: int
    dimension_a: int
    dimension_b: int
    tanner_graph: TannerGraphCertificate
    structural_distinguishing_invariants: list[str]
    tuple_profile_status: str
    information_set_status: str
    information_set_equal: bool | None
    canonical_status: str
    canonical_equal: bool | None
    status: str
    interpretation: str
    parity_check_a: list[list[int]]
    parity_check_b: list[list[int]]
    generator_a: list[list[int]]
    generator_b: list[list[int]]


@dataclass(frozen=True)
class TannerSearchRecord:
    spec: TannerSearchSpec
    trials_run: int
    code_count: int
    tuple_profile_key_count: int
    tuple_collision_count: int
    tanner_isomorphic_control_count: int
    equivalent_control_count: int
    structural_rejection_count: int
    tuple_profile_rejection_count: int
    information_set_rejection_count: int
    canonicalization_rejection_count: int
    proof_debt_collision_count: int
    max_profile_bucket_size: int
    control_audits: list[TannerCollisionAudit]
    collision_audits: list[TannerCollisionAudit]
    status: str
    interpretation: str


@dataclass(frozen=True)
class TannerCodeSearchReport:
    created_at: str
    records: list[TannerSearchRecord]
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


DEFAULT_TANNER_SPECS = [
    TannerSearchSpec("tanner-10-5-dv2-dc4", variable_count=10, check_count=5, variable_degree=2, check_degree=4, max_trials=80, max_collisions=4, seed=5101),
    TannerSearchSpec("tanner-12-6-dv2-dc4", variable_count=12, check_count=6, variable_degree=2, check_degree=4, max_trials=100, max_collisions=4, seed=5102),
    TannerSearchSpec("tanner-12-9-dv3-dc4", variable_count=12, check_count=9, variable_degree=3, check_degree=4, max_trials=120, max_collisions=4, seed=5103),
]


def validate_tanner_spec(spec: TannerSearchSpec) -> None:
    if spec.variable_count * spec.variable_degree != spec.check_count * spec.check_degree:
        raise ValueError(
            f"{spec.id} has incompatible socket counts: "
            f"{spec.variable_count}*{spec.variable_degree} != {spec.check_count}*{spec.check_degree}"
        )
    if spec.variable_degree > spec.check_count:
        raise ValueError("variable degree cannot exceed check count for simple Tanner graphs")
    if spec.check_degree > spec.variable_count:
        raise ValueError("check degree cannot exceed variable count for simple Tanner graphs")


def random_regular_tanner_parity_check(rng: np.random.Generator, spec: TannerSearchSpec) -> np.ndarray:
    validate_tanner_spec(spec)
    for _attempt in range(20_000):
        check_sockets = np.repeat(np.arange(spec.check_count, dtype=np.int64), spec.check_degree)
        rng.shuffle(check_sockets)
        parity = np.zeros((spec.check_count, spec.variable_count), dtype=np.uint8)
        ok = True
        cursor = 0
        for variable in range(spec.variable_count):
            checks = check_sockets[cursor : cursor + spec.variable_degree]
            cursor += spec.variable_degree
            if len(set(int(item) for item in checks.tolist())) != spec.variable_degree:
                ok = False
                break
            for check in checks.tolist():
                parity[int(check), variable] = 1
        if not ok:
            continue
        if all(int(parity[row].sum()) == spec.check_degree for row in range(spec.check_count)):
            return parity
    raise RuntimeError(f"failed to sample simple regular Tanner graph for {spec.id}")


def tanner_code_from_parity(parity_check: np.ndarray) -> TannerCodeDescriptor:
    parity = np.asarray(parity_check, dtype=np.uint8) & 1
    generator = gf2_nullspace_basis(parity)
    return TannerCodeDescriptor(
        parity_check=[[int(bit) for bit in row] for row in parity.tolist()],
        generator=[[int(bit) for bit in row] for row in generator.tolist()],
        variable_count=int(parity.shape[1]),
        check_count=int(parity.shape[0]),
        dimension=int(generator.shape[0]),
        rank=gf2_rank(parity),
    )


def _apply_variable_permutation(parity_check: np.ndarray, permutation: list[int]) -> np.ndarray:
    inverse = [0] * len(permutation)
    for old_index, new_index in enumerate(permutation):
        inverse[int(new_index)] = old_index
    return np.asarray(parity_check, dtype=np.uint8)[:, inverse]


def _apply_check_permutation(parity_check: np.ndarray, permutation: list[int]) -> np.ndarray:
    return np.asarray(parity_check, dtype=np.uint8)[list(permutation), :]


def tanner_graph(parity_check: np.ndarray) -> nx.Graph:
    parity = np.asarray(parity_check, dtype=np.uint8) & 1
    graph = nx.Graph()
    for variable in range(parity.shape[1]):
        graph.add_node(("v", int(variable)), side="variable")
    for check in range(parity.shape[0]):
        graph.add_node(("c", int(check)), side="check")
    for check in range(parity.shape[0]):
        for variable in range(parity.shape[1]):
            if parity[check, variable]:
                graph.add_edge(("c", int(check)), ("v", int(variable)))
    return graph


def tanner_graph_isomorphism(left_parity: np.ndarray, right_parity: np.ndarray) -> TannerGraphCertificate:
    left_graph = tanner_graph(left_parity)
    right_graph = tanner_graph(right_parity)

    def node_match(left: dict[str, Any], right: dict[str, Any]) -> bool:
        return left.get("side") == right.get("side")

    isomorphic = bool(nx.is_isomorphic(left_graph, right_graph, node_match=node_match))
    return TannerGraphCertificate(
        evaluated=True,
        isomorphic=isomorphic,
        node_count=left_graph.number_of_nodes(),
        edge_count=left_graph.number_of_edges(),
        interpretation=(
            "The Tanner graphs are isomorphic under variable/check side preservation; this is a graph-structured control."
            if isomorphic
            else "No side-preserving Tanner graph isomorphism was found."
        ),
    )


def _permuted_control_descriptor(spec: TannerSearchSpec, descriptor: TannerCodeDescriptor) -> TannerCodeDescriptor:
    rng = np.random.default_rng(spec.seed + 99_991)
    parity = np.asarray(descriptor.parity_check, dtype=np.uint8)
    variable_permutation = rng.permutation(spec.variable_count).tolist()
    check_permutation = rng.permutation(spec.check_count).tolist()
    permuted = _apply_check_permutation(_apply_variable_permutation(parity, variable_permutation), check_permutation)
    return tanner_code_from_parity(permuted)


def audit_tanner_pair(
    pair_id: str,
    left_descriptor: TannerCodeDescriptor,
    right_descriptor: TannerCodeDescriptor,
    tuple_size: int,
    tuple_cap: int,
    max_ordered_information_sets: int,
    canonical_max_assignments: int,
) -> TannerCollisionAudit:
    left = np.asarray(left_descriptor.generator, dtype=np.uint8)
    right = np.asarray(right_descriptor.generator, dtype=np.uint8)
    left_parity = np.asarray(left_descriptor.parity_check, dtype=np.uint8)
    right_parity = np.asarray(right_descriptor.parity_check, dtype=np.uint8)
    graph_certificate = tanner_graph_isomorphism(left_parity, right_parity)
    structural = strong_invariant_differences(left, right)
    tuple_audit = audit_code_tuple_profile_pair(
        record_id=f"{pair_id}-tuple",
        source="tanner_code_search",
        left=left,
        right=right,
        known_equivalent=None,
        max_tuple_size=min(3, tuple_size + 1),
        tuple_cap=tuple_cap,
    )

    info_status = "not-run-after-earlier-decision"
    info_equal: bool | None = None
    canonical_status = "not-run-after-earlier-decision"
    canonical_equal: bool | None = None
    if (
        graph_certificate.isomorphic is not True
        and not structural
        and tuple_audit.status != "rejected-by-coordinate-tuple-profile"
    ):
        info = audit_code_information_set_pair(
            record_id=f"{pair_id}-information-set",
            source="tanner_code_search",
            left=left,
            right=right,
            known_equivalent=None,
            max_ordered_information_sets=max_ordered_information_sets,
        )
        info_status = info.status
        info_equal = info.canonical_equal
        if info.canonical_equal is not True and info.status != "rejected-by-information-set-canonicalization":
            canonical = audit_code_canonicalization_pair(
                record_id=f"{pair_id}-canonical",
                source="tanner_code_search",
                left=left,
                right=right,
                known_equivalent=None,
                max_assignments=canonical_max_assignments,
            )
            canonical_status = canonical.status
            canonical_equal = canonical.canonical_equal

    if graph_certificate.isomorphic is True:
        status = "equivalent-control-under-tanner-graph-isomorphism"
        interpretation = graph_certificate.interpretation
    elif structural:
        status = "rejected-by-structural-code-invariant"
        interpretation = "Tanner-code pair is separated by structural code invariants: " + ", ".join(structural)
    elif tuple_audit.status == "rejected-by-coordinate-tuple-profile":
        status = "rejected-by-coordinate-tuple-profile"
        interpretation = tuple_audit.interpretation
    elif info_status == "rejected-by-information-set-canonicalization":
        status = "rejected-by-information-set-canonicalization"
        interpretation = "Exact information-set canonicalization separates this Tanner-code row."
    elif info_equal is True:
        status = "equivalent-control-under-information-set-canonicalization"
        interpretation = "Information-set canonicalization maps both Tanner codes to the same canonical form."
    elif canonical_status in {"rejected-by-coordinate-profile-partition", "rejected-by-exact-profile-canonical-form"}:
        status = canonical_status
        interpretation = "Profile-pruned canonicalization rejects this Tanner-code collision."
    elif canonical_status.startswith("canonical-equivalent"):
        status = "canonical-equivalent-control"
        interpretation = "Profile-pruned canonicalization identifies this Tanner-code row as an equivalent control."
    else:
        status = "tanner-code-proof-debt"
        interpretation = (
            "This Tanner row survived graph isomorphism, structural invariants, tuple profiles, information sets, "
            "and configured canonicalization; keep it as proof debt only."
        )

    return TannerCollisionAudit(
        id=pair_id,
        length=left_descriptor.variable_count,
        dimension_a=left_descriptor.dimension,
        dimension_b=right_descriptor.dimension,
        tanner_graph=graph_certificate,
        structural_distinguishing_invariants=structural,
        tuple_profile_status=tuple_audit.status,
        information_set_status=info_status,
        information_set_equal=info_equal,
        canonical_status=canonical_status,
        canonical_equal=canonical_equal,
        status=status,
        interpretation=interpretation,
        parity_check_a=left_descriptor.parity_check,
        parity_check_b=right_descriptor.parity_check,
        generator_a=left_descriptor.generator,
        generator_b=right_descriptor.generator,
    )


def run_tanner_search_spec(
    spec: TannerSearchSpec,
    tuple_cap: int = 50_000,
    max_ordered_information_sets: int = 500_000,
    canonical_max_assignments: int = 200_000,
) -> TannerSearchRecord:
    rng = np.random.default_rng(spec.seed)
    seen: dict[str, list[TannerCodeDescriptor]] = {}
    descriptors: list[TannerCodeDescriptor] = []
    collisions: list[TannerCollisionAudit] = []
    controls: list[TannerCollisionAudit] = []
    max_bucket = 0
    trials_run = 0

    for trial in range(1, spec.max_trials + 1):
        trials_run = trial
        descriptor = tanner_code_from_parity(random_regular_tanner_parity_check(rng, spec))
        if descriptor.dimension < spec.min_dimension or descriptor.dimension > spec.max_dimension:
            continue
        descriptors.append(descriptor)
        if len(controls) == 0:
            controls.append(
                audit_tanner_pair(
                    f"{spec.id}-permuted-control",
                    descriptor,
                    _permuted_control_descriptor(spec, descriptor),
                    tuple_size=spec.tuple_size,
                    tuple_cap=tuple_cap,
                    max_ordered_information_sets=max_ordered_information_sets,
                    canonical_max_assignments=canonical_max_assignments,
                )
            )
        generator = np.asarray(descriptor.generator, dtype=np.uint8)
        key = tuple_profile_key(generator, tuple_size=spec.tuple_size, tuple_cap=tuple_cap)
        if key == "skipped":
            break
        bucket = seen.setdefault(key, [])
        max_bucket = max(max_bucket, len(bucket) + 1)
        for prior_index, previous in enumerate(bucket):
            if previous.dimension != descriptor.dimension:
                continue
            if codeword_int_set(np.asarray(previous.generator, dtype=np.uint8)) == codeword_int_set(generator):
                continue
            collisions.append(
                audit_tanner_pair(
                    f"{spec.id}-collision-{len(collisions) + 1}-prior-{prior_index}",
                    previous,
                    descriptor,
                    tuple_size=spec.tuple_size,
                    tuple_cap=tuple_cap,
                    max_ordered_information_sets=max_ordered_information_sets,
                    canonical_max_assignments=canonical_max_assignments,
                )
            )
            if len(collisions) >= spec.max_collisions:
                break
        if len(collisions) >= spec.max_collisions:
            break
        if len(bucket) < 4:
            bucket.append(descriptor)

    all_audits = controls + collisions
    tanner_controls = sum(1 for audit in all_audits if audit.status == "equivalent-control-under-tanner-graph-isomorphism")
    equivalent_controls = sum(1 for audit in all_audits if "equivalent-control" in audit.status)
    structural_rejections = sum(1 for audit in collisions if audit.status == "rejected-by-structural-code-invariant")
    tuple_rejections = sum(1 for audit in collisions if audit.status == "rejected-by-coordinate-tuple-profile")
    info_rejections = sum(1 for audit in collisions if audit.status == "rejected-by-information-set-canonicalization")
    canonical_rejections = sum(1 for audit in collisions if audit.status in {"rejected-by-coordinate-profile-partition", "rejected-by-exact-profile-canonical-form"})
    proof_debt = sum(1 for audit in collisions if audit.status == "tanner-code-proof-debt")

    if proof_debt:
        status = "tanner-code-proof-debt"
        interpretation = "At least one Tanner tuple-profile collision survived implemented baselines as proof debt."
    elif collisions and (structural_rejections or tuple_rejections or info_rejections or canonical_rejections):
        status = "tanner-collisions-rejected-by-classical-baselines"
        interpretation = "Tanner tuple-profile collisions were rejected by classical code baselines."
    elif collisions and equivalent_controls >= len(collisions):
        status = "tanner-collisions-all-equivalent-controls"
        interpretation = "Tanner tuple-profile collisions found so far are equivalent controls."
    else:
        status = "no-tanner-tuple-profile-collision-found"
        interpretation = "No nontrivial Tanner tuple-profile collision was found under this deterministic search budget."

    return TannerSearchRecord(
        spec=spec,
        trials_run=trials_run,
        code_count=len(descriptors),
        tuple_profile_key_count=len(seen),
        tuple_collision_count=len(collisions),
        tanner_isomorphic_control_count=tanner_controls,
        equivalent_control_count=equivalent_controls,
        structural_rejection_count=structural_rejections,
        tuple_profile_rejection_count=tuple_rejections,
        information_set_rejection_count=info_rejections,
        canonicalization_rejection_count=canonical_rejections,
        proof_debt_collision_count=proof_debt,
        max_profile_bucket_size=max_bucket,
        control_audits=controls,
        collision_audits=collisions,
        status=status,
        interpretation=interpretation,
    )


def run_tanner_code_search(
    specs: list[TannerSearchSpec] | None = None,
    tuple_cap: int = 50_000,
    max_ordered_information_sets: int = 500_000,
    canonical_max_assignments: int = 200_000,
) -> TannerCodeSearchReport:
    active_specs = specs or DEFAULT_TANNER_SPECS
    records = [
        run_tanner_search_spec(
            spec,
            tuple_cap=tuple_cap,
            max_ordered_information_sets=max_ordered_information_sets,
            canonical_max_assignments=canonical_max_assignments,
        )
        for spec in active_specs
    ]
    metrics = {
        "search_count": len(records),
        "code_count": sum(record.code_count for record in records),
        "tuple_collision_count": sum(record.tuple_collision_count for record in records),
        "tanner_isomorphic_control_count": sum(record.tanner_isomorphic_control_count for record in records),
        "equivalent_control_count": sum(record.equivalent_control_count for record in records),
        "structural_rejection_count": sum(record.structural_rejection_count for record in records),
        "tuple_profile_rejection_count": sum(record.tuple_profile_rejection_count for record in records),
        "information_set_rejection_count": sum(record.information_set_rejection_count for record in records),
        "canonicalization_rejection_count": sum(record.canonicalization_rejection_count for record in records),
        "proof_debt_collision_count": sum(record.proof_debt_collision_count for record in records),
        "no_collision_count": sum(1 for record in records if record.status == "no-tanner-tuple-profile-collision-found"),
    }
    if metrics["proof_debt_collision_count"]:
        status = "tanner-code-search-proof-debt"
    elif (
        metrics["tanner_isomorphic_control_count"]
        or metrics["equivalent_control_count"]
        or metrics["structural_rejection_count"]
        or metrics["tuple_profile_rejection_count"]
        or metrics["information_set_rejection_count"]
        or metrics["canonicalization_rejection_count"]
    ):
        status = "tanner-code-search-dequantized-or-controls"
    else:
        status = "tanner-code-search-no-hard-row"
    summary = (
        f"Searched {metrics['search_count']} Tanner/LDPC parameter window(s), enumerating {metrics['code_count']} code(s). "
        f"Found {metrics['tuple_collision_count']} tuple-profile collision(s): "
        f"{metrics['equivalent_control_count']} equivalent control(s), "
        f"{metrics['structural_rejection_count'] + metrics['tuple_profile_rejection_count'] + metrics['information_set_rejection_count'] + metrics['canonicalization_rejection_count']} "
        f"classical rejection(s), and {metrics['proof_debt_collision_count']} proof-debt row(s)."
    )
    falsifiers = []
    if metrics["tanner_isomorphic_control_count"] or metrics["equivalent_control_count"]:
        falsifiers.append("Tanner graph or code canonicalization controls explain some Tanner rows.")
    if metrics["structural_rejection_count"] or metrics["tuple_profile_rejection_count"] or metrics["information_set_rejection_count"] or metrics["canonicalization_rejection_count"]:
        falsifiers.append("Classical code baselines reject some Tanner tuple-profile collisions.")
    if metrics["no_collision_count"]:
        falsifiers.append("Some Tanner search windows found no tuple-profile collision under the configured budget.")
    if metrics["proof_debt_collision_count"]:
        falsifiers.append("Some Tanner rows remain proof debt rather than positive evidence.")
    return TannerCodeSearchReport(utc_now(), records, metrics, status, summary, falsifiers)


def _json_ready(value: Any) -> Any:
    if is_dataclass(value):
        return _json_ready(asdict(value))
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, tuple):
        return _json_ready(list(value))
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def _safe_id(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value.upper()).strip("_")


def write_tanner_negative_results(report: TannerCodeSearchReport) -> int:
    written = 0
    for record in report.records:
        if record.status == "tanner-code-proof-debt":
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"TANNER-CODE-SEARCH-{_safe_id(record.spec.id)}",
                source="tanner_code_search.py",
                claim=f"{record.spec.id} supplies hard code-equivalence coset evidence.",
                reason_invalid=record.interpretation,
                lesson=(
                    "Tanner/LDPC rows must survive Tanner graph isomorphism, structural code invariants, tuple profiles, "
                    "information-set canonicalization, and code frontier triage before motivating a coset observable."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence={
                    "status": record.status,
                    "code_count": record.code_count,
                    "tuple_collision_count": record.tuple_collision_count,
                    "equivalent_control_count": record.equivalent_control_count,
                    "proof_debt_collision_count": record.proof_debt_collision_count,
                },
            )
        )
        written += 1
    return written


def write_tanner_code_search(
    output_path: Path = TANNER_CODE_SEARCH_PATH,
    specs: list[TannerSearchSpec] | None = None,
    tuple_cap: int = 50_000,
    max_ordered_information_sets: int = 500_000,
    canonical_max_assignments: int = 200_000,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-TANNER-LDPC-SEARCH",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-EXP-CODE-TANNER-LDPC-SEARCH-TANNER",
) -> dict[str, Any]:
    report = run_tanner_code_search(
        specs=specs,
        tuple_cap=tuple_cap,
        max_ordered_information_sets=max_ordered_information_sets,
        canonical_max_assignments=canonical_max_assignments,
    )
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    negative_results_written = 0
    if write_registry:
        negative_results_written = write_tanner_negative_results(report)
        upsert_experiment_result(
            ExperimentResultRecord(
                id=registry_result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=report.created_at,
                status=report.status,
                summary=report.summary,
                metrics=payload["headline_metrics"],
                falsifiers_triggered=report.falsifiers_triggered,
                artifacts={"tanner_code_search": str(output_path)},
            )
        )
    payload["negative_results_written"] = negative_results_written
    return payload

