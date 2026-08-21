"""Quarantine accepted mutation candidates invalidated by exact interfaces."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from research_registry import (
    NegativeResultRecord,
    load_candidates,
    load_conjectures,
    load_experiment_results,
    load_experiments,
    load_proof_status,
    load_scaling_runs,
    save_candidates,
    save_conjectures,
    save_experiment_results,
    save_experiments,
    save_proof_status,
    save_scaling_runs,
    upsert_negative_result,
    upsert_rejected_candidate,
    utc_now,
)


REDUCTION_CONTRACT_AUDIT_PATH = Path("research/reductions/interface_audit.json")
QUARANTINE_REPORT_PATH = Path("research/quarantine_report.json")


def _read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return fallback


def exact_access_invalid_mutation_ids(
    audit_path: Path = REDUCTION_CONTRACT_AUDIT_PATH,
) -> dict[str, list[dict[str, Any]]]:
    report = _read_json(audit_path, {})
    invalid: dict[str, list[dict[str, Any]]] = {}
    for audit in report.get("audits", []):
        candidate_id = str(audit.get("candidate_id", ""))
        if not candidate_id.startswith("MUT-CAND-"):
            continue
        failed_access = [
            check
            for check in audit.get("checks", [])
            if check.get("axis") == "access-model" and not check.get("passed", False)
        ]
        if failed_access:
            invalid.setdefault(candidate_id, []).append(audit)
    return invalid


def quarantine_exact_access_invalid_mutations(
    audit_path: Path = REDUCTION_CONTRACT_AUDIT_PATH,
    report_path: Path = QUARANTINE_REPORT_PATH,
) -> dict[str, Any]:
    invalid = exact_access_invalid_mutation_ids(audit_path)
    candidates = load_candidates()
    quarantined = [candidate for candidate in candidates if candidate.get("id") in invalid]
    quarantined_ids = {str(candidate.get("id")) for candidate in quarantined}
    removed_experiment_ids = {
        str(experiment.get("id"))
        for experiment in load_experiments()
        if experiment.get("candidate_id") in quarantined_ids
    }

    for candidate in quarantined:
        candidate_id = str(candidate["id"])
        audits = invalid[candidate_id]
        route_ids = sorted({str(audit.get("route_id")) for audit in audits if audit.get("route_id")})
        theorem_ids = sorted(
            {str(audit.get("theorem_contract_id")) for audit in audits if audit.get("theorem_contract_id")}
        )
        evidence = " | ".join(
            str(check.get("burden", "access-model mismatch"))
            for audit in audits
            for check in audit.get("checks", [])
            if check.get("axis") == "access-model" and not check.get("passed", False)
        )
        upsert_rejected_candidate(
            {
                "id": candidate_id,
                "title": candidate.get("title", candidate_id),
                "source": str(audit_path),
                "created_at": utc_now(),
                "quarantine_status": "rejected-by-exact-reduction-access-contract",
                "route_ids": route_ids,
                "theorem_contract_ids": theorem_ids,
                "issues": [
                    {
                        "obligation_id": "PO-REDUCTION",
                        "field": "input_model",
                        "message": evidence,
                        "hard_reject": True,
                    }
                ],
                "candidate": candidate,
            }
        )
        upsert_negative_result(
            NegativeResultRecord(
                id=f"NEG-QUARANTINE-{candidate_id}",
                source=str(audit_path),
                claim=f"{candidate_id} is eligible to remain in the accepted candidate registry.",
                reason_invalid=(
                    "The exact upstream theorem contract does not supply the coherent evaluator or stronger oracle access "
                    "required by this mutation."
                ),
                lesson="Mutations must repair the exact state interface before proof-gate promotion.",
                applies_to=[candidate_id, *route_ids],
                evidence={"theorem_contract_ids": theorem_ids, "route_ids": route_ids, "access_issue": evidence},
            )
        )

    if quarantined_ids:
        save_candidates([candidate for candidate in candidates if candidate.get("id") not in quarantined_ids])
        save_experiments(
            [experiment for experiment in load_experiments() if experiment.get("candidate_id") not in quarantined_ids]
        )
        save_experiment_results(
            [
                result
                for result in load_experiment_results()
                if result.get("candidate_id") not in quarantined_ids
                and result.get("experiment_id") not in removed_experiment_ids
            ]
        )
        save_conjectures(
            [conjecture for conjecture in load_conjectures() if conjecture.get("candidate_id") not in quarantined_ids]
        )
        save_proof_status(
            [status for status in load_proof_status() if status.get("candidate_id") not in quarantined_ids]
        )
        save_scaling_runs(
            [run for run in load_scaling_runs() if run.get("candidate_id") not in quarantined_ids]
        )

    report = {
        "created_at": utc_now(),
        "status": "quarantined-invalid-mutations" if quarantined else "no-invalid-mutations-found",
        "quarantined_candidate_count": len(quarantined),
        "removed_experiment_count": len(removed_experiment_ids),
        "quarantined_candidate_ids": sorted(quarantined_ids),
        "removed_experiment_ids": sorted(removed_experiment_ids),
        "source_audit": str(audit_path),
        "summary": (
            f"Quarantined {len(quarantined)} mutation candidate(s) whose exact theorem-contract access axis failed; "
            f"removed {len(removed_experiment_ids)} dependent experiment(s)."
        ),
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True))
    return report

