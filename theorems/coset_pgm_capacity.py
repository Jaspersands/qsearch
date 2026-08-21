"""Pretty-good-measurement capacity ledger for involution coset states.

Weak Fourier labels and small graph/tensor shadows are already blocked in the
current project.  The next question is not whether coset states are
information-theoretically distinguishable in principle, but whether a proposed
algorithm specifies an efficient multi-copy measurement and decoder.  This
module computes simple PGM-style copy thresholds for symmetric-group involution
ensembles and records the remaining obligation as measurement proof debt.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from math import ceil, factorial, log2
from pathlib import Path
from typing import Any

from coset_state_distinguishability import involution_count
from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now
from weak_fourier_signal import involution_specs_for_n


REPRESENTATION_DIR = Path("research/representation")
COSET_PGM_CAPACITY_PATH = REPRESENTATION_DIR / "coset_pgm_capacity.json"
WEAK_FOURIER_SIGNAL_PATH = REPRESENTATION_DIR / "weak_fourier_involution_signal.json"


@dataclass(frozen=True)
class CosetPGMCapacityRecord:
    n: int
    involution_type: str
    transposition_count: int
    fixed_point_count: int
    ensemble_size: int
    log2_ensemble_size: float
    single_copy_group_register_bits: float
    holevo_copy_lower_bound: int
    copies_for_overlap_cross_mass_below_one: int
    copies_for_overlap_cross_mass_below_epsilon: int
    copies_for_pairwise_overlap_below_inverse_square: int
    register_bits_at_cross_mass_threshold: float
    explicit_pgm_vector_log2_count: float
    explicit_pgm_matrix_log2_entries: float
    weak_fourier_status: str | None
    tested_copy_count: int
    tested_cross_mass: float
    status: str
    interpretation: str
    required_next_step: str


@dataclass(frozen=True)
class CosetPGMCapacityReport:
    created_at: str
    epsilon: float
    records: list[CosetPGMCapacityRecord]
    headline_metrics: dict[str, int | float]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return fallback


def _weak_fourier_index(path: Path = WEAK_FOURIER_SIGNAL_PATH) -> dict[tuple[int, str, int], dict[str, Any]]:
    payload = _read_json(path, {})
    index: dict[tuple[int, str, int], dict[str, Any]] = {}
    for record in payload.get("records", []):
        key = (
            int(record.get("n", 0)),
            str(record.get("involution_type", "")),
            int(record.get("transposition_count", 0)),
        )
        index[key] = record
    return index


def _copies_for_cross_mass(log2_ensemble_size: float, epsilon: float) -> int:
    if log2_ensemble_size <= 0:
        return 0
    return max(1, int(ceil(log2_ensemble_size + log2(1.0 / epsilon))))


def audit_coset_pgm_capacity(
    n: int,
    transposition_count: int,
    involution_type: str,
    epsilon: float = 0.1,
    weak_index: dict[tuple[int, str, int], dict[str, Any]] | None = None,
) -> CosetPGMCapacityRecord:
    ensemble_size = involution_count(n, transposition_count)
    log_ensemble = log2(ensemble_size) if ensemble_size > 0 else 0.0
    group_bits = log2(factorial(n))
    holevo = int(ceil(log_ensemble))
    cross_one = _copies_for_cross_mass(log_ensemble, epsilon=1.0)
    cross_epsilon = _copies_for_cross_mass(log_ensemble, epsilon=epsilon)
    pair_inverse_square = int(ceil(2 * log_ensemble))
    tested_copies = cross_one
    tested_cross_mass = (ensemble_size - 1) * (2.0 ** (-tested_copies)) if ensemble_size > 1 else 0.0
    fixed_points = n - 2 * transposition_count
    weak = (weak_index or {}).get((n, involution_type, transposition_count))
    weak_status = str(weak["status"]) if weak else None

    if involution_type == "single_transposition_control":
        status = "visible-control-not-frontier-evidence"
        interpretation = (
            "Single transpositions are a control ensemble with visible classical structure; PGM capacity here "
            "does not support GI/code-equivalence speedup claims."
        )
        next_step = "Keep as a calibration row only."
    elif weak_status in {"weak-fourier-labels-nearly-plancherel", "weak-fourier-label-signal-small"}:
        status = "pgm-capacity-measurement-proof-debt"
        interpretation = (
            "A PGM-style distinguishability threshold exists only after many copies, and an explicit PGM has "
            "superpolynomial description in the hidden-involution ensemble size. This is measurement-design proof debt, not an algorithm."
        )
        next_step = (
            "Provide a symmetry-exploiting collective measurement and decoder with polynomial construction/evaluation cost, "
            "or record a no-go/reduction explaining why this ensemble is the wrong route."
        )
    else:
        status = "finite-size-pgm-control"
        interpretation = (
            "Finite-size PGM accounting is available, but weak-Fourier obstruction evidence is incomplete or only a control."
        )
        next_step = "Run weak Fourier and distinguishability audits at larger n before interpreting this row."

    return CosetPGMCapacityRecord(
        n=n,
        involution_type=involution_type,
        transposition_count=transposition_count,
        fixed_point_count=fixed_points,
        ensemble_size=ensemble_size,
        log2_ensemble_size=log_ensemble,
        single_copy_group_register_bits=group_bits,
        holevo_copy_lower_bound=holevo,
        copies_for_overlap_cross_mass_below_one=cross_one,
        copies_for_overlap_cross_mass_below_epsilon=cross_epsilon,
        copies_for_pairwise_overlap_below_inverse_square=pair_inverse_square,
        register_bits_at_cross_mass_threshold=cross_one * group_bits,
        explicit_pgm_vector_log2_count=log_ensemble,
        explicit_pgm_matrix_log2_entries=2 * log_ensemble,
        weak_fourier_status=weak_status,
        tested_copy_count=tested_copies,
        tested_cross_mass=tested_cross_mass,
        status=status,
        interpretation=interpretation,
        required_next_step=next_step,
    )


def build_coset_pgm_capacity_report(
    n_values: list[int] | None = None,
    epsilon: float = 0.1,
) -> CosetPGMCapacityReport:
    values = n_values or [6, 8, 10, 12, 14, 16]
    weak_index = _weak_fourier_index()
    records = [
        audit_coset_pgm_capacity(n, transpositions, label, epsilon=epsilon, weak_index=weak_index)
        for n in values
        for label, transpositions in involution_specs_for_n(n)
    ]
    measurement_debt = sum(1 for record in records if record.status == "pgm-capacity-measurement-proof-debt")
    controls = sum(1 for record in records if "control" in record.status)
    metrics: dict[str, int | float] = {
        "record_count": len(records),
        "n_count": len(values),
        "measurement_proof_debt_count": measurement_debt,
        "control_count": controls,
        "max_log2_ensemble_size": max((record.log2_ensemble_size for record in records), default=0.0),
        "max_holevo_copy_lower_bound": max((record.holevo_copy_lower_bound for record in records), default=0),
        "max_cross_mass_threshold_copies": max(
            (record.copies_for_overlap_cross_mass_below_one for record in records),
            default=0,
        ),
        "max_epsilon_threshold_copies": max(
            (record.copies_for_overlap_cross_mass_below_epsilon for record in records),
            default=0,
        ),
        "max_register_bits_at_threshold": max(
            (record.register_bits_at_cross_mass_threshold for record in records),
            default=0.0,
        ),
        "max_explicit_pgm_matrix_log2_entries": max(
            (record.explicit_pgm_matrix_log2_entries for record in records),
            default=0.0,
        ),
    }
    status = "pgm-measurement-design-debt" if measurement_debt else "pgm-controls-only"
    summary = (
        f"Audited PGM copy/capacity obligations for {len(records)} involution coset-state rows over S_n={values}. "
        f"{measurement_debt} row(s) are measurement-design proof debt; max cross-mass threshold is "
        f"{metrics['max_cross_mass_threshold_copies']} copies."
    )
    falsifiers = []
    if measurement_debt:
        falsifiers.append("Information-theoretic PGM capacity is not an efficient algorithm without an explicit collective measurement and decoder.")
    return CosetPGMCapacityReport(utc_now(), epsilon, records, metrics, status, summary, falsifiers)


def _json_ready(value: Any) -> Any:
    if is_dataclass(value):
        return _json_ready(asdict(value))
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    return value


def _safe_id(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value.upper()).strip("_")


def write_coset_pgm_negative_results(report: CosetPGMCapacityReport) -> int:
    written = 0
    for record in report.records:
        if record.status != "pgm-capacity-measurement-proof-debt":
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"COSET-PGM-CAPACITY-DEBT-S{record.n}-{_safe_id(record.involution_type)}",
                source="coset_pgm_capacity.py",
                claim=f"PGM capacity for S_{record.n} {record.involution_type} already supplies an efficient coset-state algorithm.",
                reason_invalid=record.interpretation,
                lesson=(
                    "Information-theoretic distinguishability is not enough: a Shor-level coset route must specify "
                    "a polynomial-time collective measurement, compressed representation, and decoder."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-MEASUREMENT", "PO-COST", "PO-NOGO"],
                evidence=asdict(record),
            )
        )
        written += 1
    return written


def write_coset_pgm_capacity_report(
    output_path: Path = COSET_PGM_CAPACITY_PATH,
    n_values: list[int] | None = None,
    epsilon: float = 0.1,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-COSET-PGM-CAPACITY",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-COSET-PGM-CAPACITY-LATEST",
) -> dict[str, Any]:
    report = build_coset_pgm_capacity_report(n_values=n_values, epsilon=epsilon)
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        negative_results_written = write_coset_pgm_negative_results(report)
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
                artifacts={"coset_pgm_capacity": str(output_path)},
            )
        )
    return payload
