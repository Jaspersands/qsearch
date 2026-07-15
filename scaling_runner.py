"""Parameter sweep runner for executable research workbenches."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Sequence

from phase_state_workbench import run_hidden_shift_workbench
from research_registry import upsert_scaling_run, utc_now


SCALING_DIR = Path("research/scaling")
HIDDEN_SHIFT_SWEEP_PATH = SCALING_DIR / "hidden_shift_sweep.json"


def _parse_csv_ints(value: str) -> list[int]:
    return [int(item.strip()) for item in value.split(",") if item.strip()]


def hidden_shift_sweep(
    n_values: Sequence[int],
    sample_counts: Sequence[int],
    families: Sequence[str],
    shift: int = 7,
    seed: int = 0,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for n_bits in n_values:
        for sample_count in sample_counts:
            result = run_hidden_shift_workbench(
                families=families,
                min_bits=n_bits,
                max_bits=n_bits,
                shift=shift,
                sieve_samples=sample_count,
                sample_count=max(4, min(sample_count, 4 * n_bits)),
                seed=seed + n_bits + sample_count,
            )
            rows.append(
                {
                    "n_bits": int(n_bits),
                    "sample_count": int(sample_count),
                    "family_count": len(families),
                    "family_audit_count": len(result.family_audits),
                    "high_dequantization_risk_count": sum(
                        1 for audit in result.family_audits if audit.dequantization_risk.startswith(("critical", "high"))
                    ),
                    "restricted_query_survivor_count": sum(
                        1 for audit in result.family_audits if audit.survives_restricted_query_models
                    ),
                    "structured_signal_count": sum(
                        1 for audit in result.family_audits if "structured" in audit.positive_signal or "flat" in audit.positive_signal
                    ),
                    "best_sieve_strategy": result.sieve_search.best_strategy,
                    "best_two_adic_valuation": result.sieve_search.best_two_adic_valuation,
                    "target_two_adic_valuation": result.sieve_search.baseline.target_two_adic_valuation,
                    "best_target_success": result.sieve_search.best_target_success,
                    "best_memory_exponent_log2": result.sieve_search.best_memory_exponent_log2,
                    "generic_sample_exponent_log2": result.sieve_search.generic_sample_exponent_log2,
                    "falsifier_count": len(result.falsifiers_triggered),
                }
            )
    status = "blocked-speedup-claims" if any(row["high_dequantization_risk_count"] for row in rows) else "needs-review"
    return {
        "id": "SWEEP-HIDDEN-SHIFT-LATEST",
        "created_at": utc_now(),
        "kind": "hidden-shift",
        "status": status,
        "families": list(families),
        "n_values": list(n_values),
        "sample_counts": list(sample_counts),
        "rows": rows,
        "summary": (
            f"Ran {len(rows)} hidden-shift sweep points over {len(families)} families, "
            f"{len(n_values)} n-values, and {len(sample_counts)} sample budgets."
        ),
    }


def write_hidden_shift_sweep(
    output_path: Path = HIDDEN_SHIFT_SWEEP_PATH,
    n_values: Sequence[int] | None = None,
    sample_counts: Sequence[int] | None = None,
    families: Sequence[str] | None = None,
    shift: int = 7,
    seed: int = 0,
    write_registry: bool = True,
) -> dict[str, Any]:
    active_n = list(n_values) if n_values is not None else [5, 6, 7, 8]
    active_samples = list(sample_counts) if sample_counts is not None else [256, 512, 1024, 2048]
    active_families = (
        list(families)
        if families is not None
        else ["bent_quadratic_f2", "masked_quadratic_f2", "quartic_character", "kloosterman_trace", "noisy_cubic_chirp"]
    )
    payload = hidden_shift_sweep(active_n, active_samples, active_families, shift=shift, seed=seed)
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
                "row_count": len(payload["rows"]),
                "artifacts": {"hidden_shift_sweep": str(output_path)},
                "headline_metrics": {
                    "max_best_two_adic_valuation": max(row["best_two_adic_valuation"] for row in payload["rows"]),
                    "max_restricted_query_survivor_count": max(row["restricted_query_survivor_count"] for row in payload["rows"]),
                    "max_high_dequantization_risk_count": max(row["high_dequantization_risk_count"] for row in payload["rows"]),
                },
            }
        )
    return payload


def parse_int_csv(value: str) -> list[int]:
    return _parse_csv_ints(value)
