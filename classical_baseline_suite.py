"""Classical baseline sweeps for hidden-shift candidates.

This module is deliberately adversarial: it treats every apparent hidden-shift
signal as provisional until it has been tested across access models and sample
budgets.  The goal is not to find small wins, but to turn classical
dequantization pressure into a structured artifact that proof and mutation
systems can use.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

from phase_state_workbench import audit_hidden_shift_family
from research_registry import NegativeResultRecord, upsert_negative_result, upsert_scaling_run, utc_now


CLASSICAL_BASELINE_DIR = Path("research/classical_baselines")
HIDDEN_SHIFT_BASELINE_PATH = CLASSICAL_BASELINE_DIR / "hidden_shift_baselines.json"


@dataclass(frozen=True)
class HiddenShiftBaselineRow:
    family_id: str
    n_bits: int
    domain_size: int
    sample_count: int
    sample_exponent_log2: float
    overlap_bound: int
    reached_overlap_bound: bool
    full_table_success: bool
    random_sample_success: bool
    low_complexity_evaluator_success: bool
    exhaustive_evaluator_success: bool
    coherent_oracle_lower_bound_debt: bool
    derivative_best_support: int
    autocorrelation_alias_ratio: float
    dequantization_risk: str
    verdict: str
    notes: str


@dataclass(frozen=True)
class FamilyBaselineSummary:
    family_id: str
    tested_n_bits: list[int]
    tested_sample_counts: list[int]
    random_sample_recovery_count: int
    collision_scale_survival_count: int
    low_complexity_evaluator_recovery_count: int
    high_or_critical_risk_count: int
    best_verdict: str
    lesson: str


def _attack_success(audit: Any, model: str, names: set[str] | None = None) -> bool:
    for attack in audit.classical_attacks:
        if model in attack.legal_query_models and attack.success and (names is None or attack.name in names):
            return True
    return False


def _probe_for_model(audit: Any, model: str) -> Any | None:
    for probe in audit.query_lower_bound_probes:
        if probe.model == model:
            return probe
    return None


def _row_verdict(audit: Any, sample_count: int) -> tuple[str, str]:
    random_probe = _probe_for_model(audit, "random_sample")
    explicit_probe = _probe_for_model(audit, "explicit_evaluator")
    random_verdict = random_probe.verdict if random_probe else "missing-random-sample-probe"
    explicit_verdict = explicit_probe.verdict if explicit_probe else "missing-explicit-evaluator-probe"
    if explicit_verdict == "low-complexity-evaluator-dequantization":
        return (
            "dequantized-by-polynomial-evaluator",
            "A low-complexity evaluator attack recovers the shift; this family should not support a speedup claim.",
        )
    if random_verdict == "dequantized-random-sample":
        return (
            "dequantized-by-random-samples",
            f"Random-sample access recovers the shift with sample_count={sample_count}.",
        )
    if random_verdict == "undersampled-gap-not-evidence":
        return (
            "undersampled-survival",
            "The sampled baseline is below the overlap/collision scale, so survival is not positive evidence.",
        )
    if explicit_verdict == "exhaustive-evaluator-recovery-only":
        return (
            "collision-scale-sampled-survival-but-exhaustive-evaluator-baseline",
            "Random-sample baselines survive at or above overlap scale, but evaluator access still has exponential exhaustive recovery.",
        )
    return (
        "unresolved-query-model-survival",
        "Current baselines do not recover the shift, but coherent-oracle lower bounds are still absent.",
    )


def hidden_shift_baseline_sweep(
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
    sample_counts: Sequence[int] | None = None,
    shift: int = 7,
    seed: int = 0,
) -> dict[str, Any]:
    active_families = list(families) if families is not None else [
        "bent_quadratic_f2",
        "masked_quadratic_f2",
        "quartic_character",
        "kloosterman_trace",
        "noisy_cubic_chirp",
        "fp2_quadratic_form",
        "mm_majority_bent_f2",
    ]
    active_n = list(n_values) if n_values is not None else [5, 6, 7, 8]
    active_samples = list(sample_counts) if sample_counts is not None else [4, 8, 16, 32, 64, 128]
    rows: list[HiddenShiftBaselineRow] = []

    for n_bits in active_n:
        for family_id in active_families:
            for sample_count in active_samples:
                audit = audit_hidden_shift_family(
                    family_id=family_id,
                    n_bits=n_bits,
                    shift=shift,
                    sample_count=sample_count,
                    seed=seed + n_bits * 1009 + sample_count,
                )
                random_probe = _probe_for_model(audit, "random_sample")
                explicit_probe = _probe_for_model(audit, "explicit_evaluator")
                verdict, notes = _row_verdict(audit, sample_count)
                rows.append(
                    HiddenShiftBaselineRow(
                        family_id=audit.family.id,
                        n_bits=int(n_bits),
                        domain_size=audit.family.domain_size,
                        sample_count=int(sample_count),
                        sample_exponent_log2=float(math.log2(max(1, sample_count))),
                        overlap_bound=int(random_probe.required_queries_for_constant_signal if random_probe else 0),
                        reached_overlap_bound=bool(
                            random_probe
                            and random_probe.observed_query_budget is not None
                            and random_probe.required_queries_for_constant_signal is not None
                            and random_probe.observed_query_budget >= random_probe.required_queries_for_constant_signal
                        ),
                        full_table_success=_attack_success(audit, "full_table"),
                        random_sample_success=_attack_success(audit, "random_sample"),
                        low_complexity_evaluator_success=bool(
                            explicit_probe and explicit_probe.verdict == "low-complexity-evaluator-dequantization"
                        ),
                        exhaustive_evaluator_success=bool(
                            explicit_probe and explicit_probe.verdict == "exhaustive-evaluator-recovery-only"
                        ),
                        coherent_oracle_lower_bound_debt=True,
                        derivative_best_support=audit.derivative_profile.best_support_99_percent,
                        autocorrelation_alias_ratio=audit.autocorrelation_alias_ratio,
                        dequantization_risk=audit.dequantization_risk,
                        verdict=verdict,
                        notes=notes,
                    )
                )

    summaries = build_family_summaries(rows)
    status = "blocked-by-classical-baselines"
    if summaries and all(summary.collision_scale_survival_count for summary in summaries):
        status = "query-model-survival-needs-lower-bound"
    if any(summary.random_sample_recovery_count for summary in summaries):
        status = "dequantized-by-sample-baselines"

    return {
        "id": "CLASSICAL-HS-BASELINES-LATEST",
        "created_at": utc_now(),
        "kind": "hidden-shift-classical-baselines",
        "families": active_families,
        "n_values": active_n,
        "sample_counts": active_samples,
        "status": status,
        "row_count": len(rows),
        "summary": (
            f"Ran {len(rows)} hidden-shift classical baseline rows over {len(active_families)} families, "
            f"{len(active_n)} n-values, and {len(active_samples)} sample budgets."
        ),
        "headline_metrics": {
            "random_sample_recovery_count": sum(1 for row in rows if row.random_sample_success),
            "collision_scale_survival_count": sum(
                1 for row in rows if row.reached_overlap_bound and not row.random_sample_success
            ),
            "low_complexity_evaluator_recovery_count": sum(1 for row in rows if row.low_complexity_evaluator_success),
            "high_or_critical_risk_count": sum(
                1 for row in rows if row.dequantization_risk.startswith(("critical", "high"))
            ),
            "undersampled_survival_count": sum(1 for row in rows if row.verdict == "undersampled-survival"),
        },
        "family_summaries": [asdict(summary) for summary in summaries],
        "rows": [asdict(row) for row in rows],
    }


def build_family_summaries(rows: Sequence[HiddenShiftBaselineRow]) -> list[FamilyBaselineSummary]:
    by_family: dict[str, list[HiddenShiftBaselineRow]] = {}
    for row in rows:
        by_family.setdefault(row.family_id, []).append(row)

    summaries: list[FamilyBaselineSummary] = []
    for family_id, family_rows in sorted(by_family.items()):
        random_count = sum(1 for row in family_rows if row.random_sample_success)
        collision_survival = sum(1 for row in family_rows if row.reached_overlap_bound and not row.random_sample_success)
        evaluator_count = sum(1 for row in family_rows if row.low_complexity_evaluator_success)
        risk_count = sum(1 for row in family_rows if row.dequantization_risk.startswith(("critical", "high")))
        if evaluator_count:
            best_verdict = "reject-low-complexity-evaluator"
            lesson = "Polynomial-query evaluator reconstruction is enough to demote this family."
        elif random_count:
            best_verdict = "reject-random-sample-dequantized"
            lesson = "Random sampled access recovers the shift at tested budgets."
        elif collision_survival:
            best_verdict = "survives-sampled-baselines-needs-lower-bound"
            lesson = "Survival at collision-scale sample budgets is useful only if a formal lower bound follows."
        else:
            best_verdict = "undersampled-or-unresolved"
            lesson = "Test stronger sampled and chosen-query baselines before treating this as evidence."
        summaries.append(
            FamilyBaselineSummary(
                family_id=family_id,
                tested_n_bits=sorted({row.n_bits for row in family_rows}),
                tested_sample_counts=sorted({row.sample_count for row in family_rows}),
                random_sample_recovery_count=random_count,
                collision_scale_survival_count=collision_survival,
                low_complexity_evaluator_recovery_count=evaluator_count,
                high_or_critical_risk_count=risk_count,
                best_verdict=best_verdict,
                lesson=lesson,
            )
        )
    return summaries


def write_hidden_shift_baselines(
    output_path: Path = HIDDEN_SHIFT_BASELINE_PATH,
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
    sample_counts: Sequence[int] | None = None,
    shift: int = 7,
    seed: int = 0,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = hidden_shift_baseline_sweep(
        families=families,
        n_values=n_values,
        sample_counts=sample_counts,
        shift=shift,
        seed=seed,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        upsert_scaling_run(
            {
                "id": payload["id"],
                "created_at": payload["created_at"],
                "kind": payload["kind"],
                "status": payload["status"],
                "summary": payload["summary"],
                "row_count": payload["row_count"],
                "artifacts": {"hidden_shift_classical_baselines": str(output_path)},
                "headline_metrics": payload["headline_metrics"],
            }
        )
        write_negative_results_from_baselines(payload)
    return payload


def write_negative_results_from_baselines(payload: dict[str, Any]) -> int:
    written = 0
    for summary in payload.get("family_summaries", []):
        if summary.get("low_complexity_evaluator_recovery_count", 0) <= 0 and summary.get("random_sample_recovery_count", 0) <= 0:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"CLASSICAL-BASELINE-DEQUANTIZED-{summary['family_id'].upper()}",
                source="classical_baseline_suite.py",
                claim=f"{summary['family_id']} survives classical hidden-shift baselines under the tested access models.",
                reason_invalid=(
                    f"Baseline sweep found {summary['low_complexity_evaluator_recovery_count']} low-complexity evaluator "
                    f"recoveries and {summary['random_sample_recovery_count']} random-sample recoveries."
                ),
                lesson=summary["lesson"],
                applies_to=["DHS-GOWERS-SIEVE", "HYP-LIT-HIDDEN-SHIFT-SIEVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence={
                    "family_id": summary["family_id"],
                    "tested_n_bits": summary["tested_n_bits"],
                    "tested_sample_counts": summary["tested_sample_counts"],
                    "best_verdict": summary["best_verdict"],
                },
            )
        )
        written += 1
    return written
