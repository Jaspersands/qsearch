"""Quasi-cyclic code-family search with immediate dequantization baselines.

Random weak-invariant collisions are too low-ceiling.  Quasi-cyclic and related
algebraic code families are a more plausible place to look for structured
code-equivalence instances with large automorphism groups.  This module creates
small quasi-cyclic binary generator matrices, searches for collisions of
higher-order tuple profiles, and immediately attacks every collision with
profile-pruned canonicalization.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any

import numpy as np

from code_canonicalization_baseline import audit_code_canonicalization_pair
from code_equivalence_workbench import codeword_int_set, gf2_rank
from code_tuple_profile_baseline import audit_code_tuple_profile_pair, tuple_profile_key
from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


CODE_EQUIVALENCE_DIR = Path("research/code_equivalence")
QUASI_CYCLIC_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "quasi_cyclic_code_search.json"


@dataclass(frozen=True)
class QuasiCyclicSearchSpec:
    id: str
    index: int
    circulant_blocks: int
    max_trials: int
    max_collisions: int
    seed: int


@dataclass(frozen=True)
class QuasiCyclicCollisionAudit:
    id: str
    trial: int
    length: int
    dimension: int
    tuple_profile_bucket_size: int
    canonical_status: str
    canonical_equal: bool | None
    estimated_assignments: int
    tuple_profile_status: str
    interpretation: str
    generator_a: list[list[int]]
    generator_b: list[list[int]]


@dataclass(frozen=True)
class QuasiCyclicSearchRecord:
    spec: QuasiCyclicSearchSpec
    trials_run: int
    length: int
    dimension: int
    tuple_profile_key_count: int
    tuple_collision_count: int
    equivalent_collision_count: int
    rejected_collision_count: int
    tuple_profile_rejection_count: int
    canonicalization_rejection_count: int
    proof_debt_collision_count: int
    max_profile_bucket_size: int
    collision_audits: list[QuasiCyclicCollisionAudit]
    status: str
    interpretation: str


@dataclass(frozen=True)
class QuasiCyclicCodeSearchReport:
    created_at: str
    records: list[QuasiCyclicSearchRecord]
    tuple_size: int
    tuple_cap: int
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


DEFAULT_QC_SPECS = [
    QuasiCyclicSearchSpec("qc-index4-two-circulants", index=4, circulant_blocks=2, max_trials=80, max_collisions=2, seed=1201),
    QuasiCyclicSearchSpec("qc-index5-two-circulants", index=5, circulant_blocks=2, max_trials=100, max_collisions=2, seed=1202),
    QuasiCyclicSearchSpec("qc-index5-three-circulants", index=5, circulant_blocks=3, max_trials=120, max_collisions=2, seed=1203),
]


def circulant_binary(row: np.ndarray) -> np.ndarray:
    values = np.asarray(row, dtype=np.uint8) & 1
    return np.vstack([np.roll(values, shift) for shift in range(len(values))]).astype(np.uint8)


def quasi_cyclic_generator(block_rows: list[np.ndarray]) -> np.ndarray:
    """Return a systematic quasi-cyclic generator [I | C_1 | ... | C_m]."""

    if not block_rows:
        raise ValueError("at least one circulant block is required")
    index = len(block_rows[0])
    identity = np.eye(index, dtype=np.uint8)
    blocks = [identity] + [circulant_binary(row) for row in block_rows]
    generator = np.concatenate(blocks, axis=1).astype(np.uint8)
    if gf2_rank(generator) != index:
        raise ValueError("systematic quasi-cyclic generator unexpectedly lost rank")
    return generator


def random_quasi_cyclic_generator(
    rng: np.random.Generator,
    index: int,
    circulant_blocks: int,
) -> np.ndarray:
    for _ in range(10_000):
        rows = []
        for _block in range(circulant_blocks):
            row = rng.integers(0, 2, size=index, dtype=np.uint8)
            if not row.any():
                row[int(rng.integers(0, index))] = 1
            rows.append(row)
        generator = quasi_cyclic_generator(rows)
        if len(codeword_int_set(generator)) == 1 << index:
            return generator
    raise RuntimeError("failed to sample quasi-cyclic generator")


def run_quasi_cyclic_search_spec(
    spec: QuasiCyclicSearchSpec,
    tuple_size: int = 2,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 20_000,
) -> QuasiCyclicSearchRecord:
    rng = np.random.default_rng(spec.seed)
    seen: dict[str, list[np.ndarray]] = {}
    audits: list[QuasiCyclicCollisionAudit] = []
    equivalent = 0
    rejected = 0
    tuple_rejected = 0
    canonical_rejected = 0
    proof_debt = 0
    trials_run = 0
    max_bucket = 0
    length = spec.index * (spec.circulant_blocks + 1)

    for trial in range(1, spec.max_trials + 1):
        trials_run = trial
        candidate = random_quasi_cyclic_generator(rng, spec.index, spec.circulant_blocks)
        key = tuple_profile_key(candidate, tuple_size=tuple_size, tuple_cap=tuple_cap)
        if key == "skipped":
            break
        bucket = seen.setdefault(key, [])
        max_bucket = max(max_bucket, len(bucket) + 1)
        for prior_index, previous in enumerate(bucket):
            if codeword_int_set(previous) == codeword_int_set(candidate):
                continue
            canonical = audit_code_canonicalization_pair(
                record_id=f"{spec.id}-trial-{trial}-prior-{prior_index}",
                source="quasi_cyclic_code_search",
                left=previous,
                right=candidate,
                known_equivalent=None,
                max_assignments=canonical_max_assignments,
            )
            tuple_audit = audit_code_tuple_profile_pair(
                record_id=f"{spec.id}-tuple-{trial}-{prior_index}",
                source="quasi_cyclic_code_search",
                left=previous,
                right=candidate,
                known_equivalent=None,
                max_tuple_size=min(3, tuple_size + 1),
                tuple_cap=tuple_cap,
            )
            if tuple_audit.status == "rejected-by-coordinate-tuple-profile":
                tuple_rejected += 1
                rejected += 1
            elif canonical.status.startswith("canonical-equivalent"):
                equivalent += 1
            elif canonical.status == "canonicalization-proof-debt":
                proof_debt += 1
            else:
                canonical_rejected += 1
                rejected += 1
            audits.append(
                QuasiCyclicCollisionAudit(
                    id=canonical.id,
                    trial=trial,
                    length=length,
                    dimension=spec.index,
                    tuple_profile_bucket_size=len(bucket) + 1,
                    canonical_status=canonical.status,
                    canonical_equal=canonical.canonical_equal,
                    estimated_assignments=max(
                        int(canonical.left_canonical.estimated_assignments),
                        int(canonical.right_canonical.estimated_assignments),
                    ),
                    tuple_profile_status=tuple_audit.status,
                    interpretation=canonical.interpretation,
                    generator_a=[[int(bit) for bit in row] for row in previous.tolist()],
                    generator_b=[[int(bit) for bit in row] for row in candidate.tolist()],
                )
            )
            if len(audits) >= spec.max_collisions:
                break
        if len(audits) >= spec.max_collisions:
            break
        if len(bucket) < 4:
            bucket.append(candidate)

    if proof_debt:
        status = "qc-tuple-collision-proof-debt"
        interpretation = (
            "Some quasi-cyclic tuple-profile collisions remain proof debt after tuple-profile and canonicalization checks."
        )
    elif tuple_rejected:
        status = "qc-tuple-collisions-rejected-by-higher-tuple-profile"
        interpretation = "Quasi-cyclic tuple-profile collisions are rejected by higher-order tuple profiles."
    elif canonical_rejected:
        status = "qc-tuple-collisions-rejected-by-canonicalization"
        interpretation = "Quasi-cyclic tuple-profile collisions exist but canonicalization rejects them."
    elif equivalent:
        status = "qc-tuple-collisions-all-equivalent-controls"
        interpretation = "Quasi-cyclic tuple-profile collisions found so far are equivalent controls."
    else:
        status = "no-qc-tuple-profile-collision-found"
        interpretation = "No nontrivial quasi-cyclic tuple-profile collision was found under this deterministic search budget."

    return QuasiCyclicSearchRecord(
        spec=spec,
        trials_run=trials_run,
        length=length,
        dimension=spec.index,
        tuple_profile_key_count=len(seen),
        tuple_collision_count=len(audits),
        equivalent_collision_count=equivalent,
        rejected_collision_count=rejected,
        tuple_profile_rejection_count=tuple_rejected,
        canonicalization_rejection_count=canonical_rejected,
        proof_debt_collision_count=proof_debt,
        max_profile_bucket_size=max_bucket,
        collision_audits=audits,
        status=status,
        interpretation=interpretation,
    )


def run_quasi_cyclic_code_search(
    specs: list[QuasiCyclicSearchSpec] | None = None,
    tuple_size: int = 2,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 20_000,
) -> QuasiCyclicCodeSearchReport:
    active_specs = specs or DEFAULT_QC_SPECS
    records = [
        run_quasi_cyclic_search_spec(
            spec,
            tuple_size=tuple_size,
            tuple_cap=tuple_cap,
            canonical_max_assignments=canonical_max_assignments,
        )
        for spec in active_specs
    ]
    metrics = {
        "search_count": len(records),
        "tuple_collision_count": sum(record.tuple_collision_count for record in records),
        "equivalent_collision_count": sum(record.equivalent_collision_count for record in records),
        "rejected_collision_count": sum(record.rejected_collision_count for record in records),
        "tuple_profile_rejection_count": sum(record.tuple_profile_rejection_count for record in records),
        "canonicalization_rejection_count": sum(record.canonicalization_rejection_count for record in records),
        "proof_debt_collision_count": sum(record.proof_debt_collision_count for record in records),
        "no_collision_count": sum(1 for record in records if record.status == "no-qc-tuple-profile-collision-found"),
        "max_length": max((record.length for record in records), default=0),
    }
    if metrics["proof_debt_collision_count"]:
        status = "quasi-cyclic-code-search-proof-debt"
    elif metrics["tuple_collision_count"]:
        status = "quasi-cyclic-code-search-dequantized"
    else:
        status = "quasi-cyclic-code-search-incomplete"
    summary = (
        f"Searched {metrics['search_count']} quasi-cyclic code budget(s) for tuple-profile collisions. "
        f"Found {metrics['tuple_collision_count']} collision(s), with {metrics['equivalent_collision_count']} equivalent controls, "
        f"{metrics['tuple_profile_rejection_count']} tuple-profile rejection(s), "
        f"{metrics['canonicalization_rejection_count']} canonicalization rejection(s), and "
        f"{metrics['proof_debt_collision_count']} proof-debt row(s)."
    )
    falsifiers = []
    if metrics["equivalent_collision_count"] or metrics["rejected_collision_count"]:
        falsifiers.append(
            "Quasi-cyclic tuple-profile collisions found so far are equivalent controls, higher-tuple rejections, or canonicalization rejections."
        )
    if metrics["no_collision_count"]:
        falsifiers.append("No nontrivial quasi-cyclic tuple-profile collision appears under current deterministic budgets.")
    if metrics["proof_debt_collision_count"]:
        falsifiers.append("Quasi-cyclic proof-debt collisions require stronger canonicalization and asymptotic construction evidence.")
    return QuasiCyclicCodeSearchReport(utc_now(), records, tuple_size, tuple_cap, metrics, status, summary, falsifiers)


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


def write_quasi_cyclic_negative_results(report: QuasiCyclicCodeSearchReport) -> int:
    written = 0
    for record in report.records:
        if record.status not in {
            "qc-tuple-collisions-rejected-by-canonicalization",
            "qc-tuple-collisions-rejected-by-higher-tuple-profile",
            "qc-tuple-collisions-all-equivalent-controls",
        }:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"QUASI-CYCLIC-CODE-SEARCH-{_safe_id(record.spec.id)}",
                source="quasi_cyclic_code_search.py",
                claim=f"{record.spec.id} quasi-cyclic tuple-profile collisions provide hard code-equivalence coset evidence.",
                reason_invalid=record.interpretation,
                lesson=(
                    "Algebraic or quasi-cyclic structure alone is not evidence.  Rows must be non-equivalent, "
                    "survive tuple-profile and canonicalization baselines, and scale beyond tiny controls."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence=asdict(record),
            )
        )
        written += 1
    return written


def write_quasi_cyclic_code_search(
    output_path: Path = QUASI_CYCLIC_CODE_SEARCH_PATH,
    specs: list[QuasiCyclicSearchSpec] | None = None,
    tuple_size: int = 2,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 20_000,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-QUASI-CYCLIC-SEARCH",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-CODE-QUASI-CYCLIC-SEARCH-LATEST",
) -> dict[str, Any]:
    report = run_quasi_cyclic_code_search(
        specs=specs,
        tuple_size=tuple_size,
        tuple_cap=tuple_cap,
        canonical_max_assignments=canonical_max_assignments,
    )
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_quasi_cyclic_negative_results(report)
        metrics = dict(report.headline_metrics)
        metrics["negative_results_written"] = negative_results_written
        upsert_experiment_result(
            ExperimentResultRecord(
                id=registry_result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=report.created_at,
                status=report.status,
                summary=report.summary,
                metrics=metrics,
                falsifiers_triggered=report.falsifiers_triggered,
                artifacts={"quasi_cyclic_code_search": str(output_path)},
            )
        )
    return payload
