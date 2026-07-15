"""Multi-copy distinguishability accounting for involution coset states.

For H_h={e,h} with h an involution in S_n, the mixed coset state is

    rho_h = (I + R_h) / |S_n|.

For distinct involutions h != k, the normalized Hilbert-Schmidt overlap of
rho_h and rho_k is 1/2, so k-copy overlaps decay as 2^-k.  This does not rule
out a quantum algorithm, but it gives explicit information/sample obligations:
an ensemble with M hidden involutions cannot be identified from irrep labels or
tiny-copy evidence; any serious collective measurement must specify how it uses
roughly log_2(M) bits of information and avoids classical-shadow collapse.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from math import ceil, factorial, log2
from pathlib import Path
from typing import Any

from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now
from weak_fourier_signal import involution_specs_for_n


REPRESENTATION_DIR = Path("research/representation")
COSET_DISTINGUISHABILITY_PATH = REPRESENTATION_DIR / "coset_state_distinguishability.json"
WEAK_FOURIER_SIGNAL_PATH = REPRESENTATION_DIR / "weak_fourier_involution_signal.json"


@dataclass(frozen=True)
class CosetDistinguishabilityRecord:
    n: int
    involution_type: str
    transposition_count: int
    fixed_point_count: int
    ensemble_size: int
    log2_ensemble_size: float
    holevo_copy_lower_bound: int
    pairwise_hs_overlap_one_copy: float
    copies_for_pairwise_overlap_below_inverse_ensemble: int
    copies_for_pairwise_overlap_below_inverse_square: int
    weak_fourier_total_variation: float | None
    weak_fourier_status: str | None
    status: str
    interpretation: str


@dataclass(frozen=True)
class CosetDistinguishabilityReport:
    created_at: str
    records: list[CosetDistinguishabilityRecord]
    headline_metrics: dict[str, int | float]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def involution_count(n: int, transposition_count: int) -> int:
    fixed = n - 2 * transposition_count
    if fixed < 0:
        raise ValueError("too many transpositions for S_n")
    return factorial(n) // ((2**transposition_count) * factorial(transposition_count) * factorial(fixed))


def copies_for_overlap_threshold(log2_ensemble_size: float, exponent: int = 1) -> int:
    return int(ceil(exponent * log2_ensemble_size))


def _read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
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


def audit_coset_distinguishability(
    n: int,
    transposition_count: int,
    involution_type: str,
    weak_index: dict[tuple[int, str, int], dict[str, Any]] | None = None,
) -> CosetDistinguishabilityRecord:
    ensemble_size = involution_count(n, transposition_count)
    log_ensemble = log2(ensemble_size) if ensemble_size > 0 else 0.0
    weak = (weak_index or {}).get((n, involution_type, transposition_count))
    weak_tv = float(weak["total_variation_from_plancherel"]) if weak else None
    weak_status = str(weak["status"]) if weak else None
    holevo_bound = int(ceil(log_ensemble))
    fixed_points = n - 2 * transposition_count
    inverse_copies = copies_for_overlap_threshold(log_ensemble, exponent=1)
    inverse_square_copies = copies_for_overlap_threshold(log_ensemble, exponent=2)
    if involution_type == "single_transposition_control":
        status = "visible-control-not-frontier-evidence"
        interpretation = "Transpositions are a control ensemble with visible structure; not evidence for GI/code-equivalence speedups."
    elif weak_status in {"weak-fourier-labels-nearly-plancherel", "weak-fourier-label-signal-small"}:
        status = "collective-measurement-copy-debt"
        interpretation = (
            "Weak Fourier labels are blocked; any viable route must give an explicit collective measurement using enough "
            "copies to distinguish a large involution ensemble without collapsing to known classical invariants."
        )
    else:
        status = "finite-size-distinguishability-control"
        interpretation = "Finite-size coset distinguishability row; rerun at larger n before interpreting as frontier evidence."
    return CosetDistinguishabilityRecord(
        n=n,
        involution_type=involution_type,
        transposition_count=transposition_count,
        fixed_point_count=fixed_points,
        ensemble_size=ensemble_size,
        log2_ensemble_size=log_ensemble,
        holevo_copy_lower_bound=holevo_bound,
        pairwise_hs_overlap_one_copy=0.5 if ensemble_size > 1 else 0.0,
        copies_for_pairwise_overlap_below_inverse_ensemble=inverse_copies,
        copies_for_pairwise_overlap_below_inverse_square=inverse_square_copies,
        weak_fourier_total_variation=weak_tv,
        weak_fourier_status=weak_status,
        status=status,
        interpretation=interpretation,
    )


def build_coset_distinguishability_report(n_values: list[int] | None = None) -> CosetDistinguishabilityReport:
    values = n_values or [6, 8, 10, 12, 14, 16]
    weak_index = _weak_fourier_index()
    records = [
        audit_coset_distinguishability(n, transpositions, label, weak_index=weak_index)
        for n in values
        for label, transpositions in involution_specs_for_n(n)
    ]
    copy_debt = sum(1 for record in records if record.status == "collective-measurement-copy-debt")
    fixed_point_free = [record for record in records if "fixed_point_free" in record.involution_type]
    metrics: dict[str, int | float] = {
        "record_count": len(records),
        "n_count": len(values),
        "copy_debt_count": copy_debt,
        "control_count": sum(1 for record in records if "control" in record.status),
        "max_log2_ensemble_size": max((record.log2_ensemble_size for record in records), default=0.0),
        "max_holevo_copy_lower_bound": max((record.holevo_copy_lower_bound for record in records), default=0),
        "max_fixed_point_free_holevo_bound": max((record.holevo_copy_lower_bound for record in fixed_point_free), default=0),
        "max_fixed_point_free_inverse_square_overlap_copies": max(
            (record.copies_for_pairwise_overlap_below_inverse_square for record in fixed_point_free),
            default=0,
        ),
    }
    status = "collective-measurement-distinguishability-debt" if copy_debt else "needs-weak-fourier-prerequisite"
    summary = (
        f"Audited {len(records)} involution coset-state distinguishability rows over S_n for n={values}. "
        f"{copy_debt} row(s) require explicit collective-measurement copy/decode obligations; "
        f"max Holevo copy lower bound is {metrics['max_holevo_copy_lower_bound']}."
    )
    falsifiers = []
    if copy_debt:
        falsifiers.append("Coset states are distinguishable only through explicit multi-copy measurement/decode obligations, not label-only evidence.")
    return CosetDistinguishabilityReport(utc_now(), records, metrics, status, summary, falsifiers)


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


def write_coset_distinguishability_negative_results(report: CosetDistinguishabilityReport) -> int:
    written = 0
    for record in report.records:
        if record.status != "collective-measurement-copy-debt":
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"COSET-DISTINGUISHABILITY-DEBT-S{record.n}-{record.involution_type.upper()}",
                source="coset_state_distinguishability.py",
                claim=f"Few-copy irrep-label or low-rank evidence solves S_{record.n} {record.involution_type} coset states.",
                reason_invalid=record.interpretation,
                lesson="A coset-state route must specify the multi-copy measurement and decoding cost for the full hidden-involution ensemble.",
                applies_to=["CODE-COSET-COLLECTIVE", "PO-MEASUREMENT", "PO-COST", "PO-DEQUANTIZATION"],
                evidence=asdict(record),
            )
        )
        written += 1
    return written


def write_coset_distinguishability_report(
    output_path: Path = COSET_DISTINGUISHABILITY_PATH,
    n_values: list[int] | None = None,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-COSET-STATE-DISTINGUISHABILITY",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-COSET-STATE-DISTINGUISHABILITY-LATEST",
) -> dict[str, Any]:
    report = build_coset_distinguishability_report(n_values=n_values)
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        negative_results_written = write_coset_distinguishability_negative_results(report)
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
                artifacts={"coset_state_distinguishability": str(output_path)},
            )
        )
    return payload
