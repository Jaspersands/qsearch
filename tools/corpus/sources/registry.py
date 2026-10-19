"""Parse research/registry/*.json list registries into documents."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Callable

from tools.corpus.docs import Doc, flatten, read_json, unique_ids, words

_ID_LINE = re.compile(r'^[ \t]*"id":[ \t]*"((?:[^"\\]|\\.)*)"', re.MULTILINE)


def _id_lines(text: str) -> dict[str, int]:
    """1-based line of the first `"id": "..."` line for each id, in one pass over the text."""
    lines: dict[str, int] = {}
    line, position = 1, 0
    for match in _ID_LINE.finditer(text):
        line += text.count("\n", position, match.start())
        position = match.start()
        lines.setdefault(match.group(1), line)
    return lines


def _negative(record: dict[str, Any]) -> tuple[str, str, str, str, dict[str, Any]]:
    evidence = record.get("evidence")
    status = evidence.get("status") if isinstance(evidence, dict) else None
    claim = str(record.get("claim", ""))
    reason = str(record.get("reason_invalid", ""))
    lesson = str(record.get("lesson", ""))
    rid = str(record["id"])
    text = f"{words(rid)}. {claim} {reason} {lesson}"
    meta = {
        "tags": list(record.get("applies_to") or []),
        "source": record.get("source"),
        "status": status or "retained",
        "reason": reason,
        "lesson": lesson,
    }
    return f"negative:{rid}", "negative", claim, text, meta


def _quarantined(record: dict[str, Any]) -> tuple[str, str, str, str, dict[str, Any]]:
    original = record.get("original_record") or {}
    if not isinstance(original, dict):  # a free-text note instead of the original record
        original = {"claim": flatten(original, 2000)}
    claim = str(original.get("claim", ""))
    reason = str(original.get("reason_invalid", ""))
    retraction = flatten(record.get("retraction_reasons"), 2000)
    rid = str(record["id"])
    text = f"{words(rid)}. {claim} {reason} Retracted: {retraction}"
    meta = {
        "tags": list(original.get("applies_to") or []),
        "status": record.get("status") or "QUARANTINED",
        "reason": reason,
        "retraction": retraction,
    }
    return f"quarantined:{rid}", "negative", claim, text, meta


def _dequant(record: dict[str, Any]) -> tuple[str, str, str, str, dict[str, Any]]:
    claim = str(record.get("claim_under_test", ""))
    action = str(record.get("required_action", ""))
    rid = str(record["id"])
    text = f"{words(rid)}. {claim} {action} {flatten(record.get('evidence'), 2000)}"
    meta = {
        "severity": record.get("severity"),
        "target_id": record.get("target_id"),
        "blocks_speedup_claim": record.get("blocks_speedup_claim"),
        "status": record.get("severity"),
        "reason": action,
    }
    return f"dequant:{rid}", "dequant", claim, text, meta


def _experiment(record: dict[str, Any]) -> tuple[str, str, str, str, dict[str, Any]]:
    rid = str(record["id"])
    title = str(record.get("title") or rid)
    body = flatten(
        [record.get("hypothesis"), record.get("protocol"), record.get("falsifiers"), record.get("positive_signal")], 3000
    )
    meta = {"status": record.get("status"), "candidate_id": record.get("candidate_id")}
    return f"experiment:{rid}", "experiment", title, f"{words(rid)}. {title} {body}", meta


def _result(record: dict[str, Any]) -> tuple[str, str, str, str, dict[str, Any]]:
    rid = str(record["id"])
    experiment = str(record.get("experiment_id", ""))
    summary = flatten(record.get("summary"), 2000)
    body = f"{words(experiment)}. {summary} {flatten(record.get('falsifiers_triggered'), 2000)}"
    meta = {"status": record.get("status"), "experiment_id": experiment}
    return f"result:{rid}", "result", f"{experiment} {record.get('status', '')}".strip(), body, meta


def _proof(record: dict[str, Any]) -> tuple[str, str, str, str, dict[str, Any]]:
    candidate = str(record.get("candidate_id", ""))
    obligation = str(record.get("obligation_id", ""))
    body = f"{words(obligation)} {record.get('field', '')}. {flatten(record.get('evidence'), 2000)} {record.get('next_action', '')}"
    meta = {"status": record.get("status"), "candidate_id": candidate}
    return f"proof:{candidate}:{obligation}", "proof", f"{candidate} {obligation}", body, meta


def _candidate(record: dict[str, Any]) -> tuple[str, str, str, str, dict[str, Any]]:
    rid = str(record["id"])
    title = str(record.get("title") or record.get("statement") or record.get("new_hypothesis") or rid)
    meta = {"status": record.get("status")}
    return f"candidate:{rid}", "candidate", title[:200], f"{words(rid)}. {flatten(record, 4000)}", meta


PARSERS: dict[str, Callable[[dict[str, Any]], tuple[str, str, str, str, dict[str, Any]]]] = {
    "negative_results.json": _negative,
    "quarantined_campaign_negatives.json": _quarantined,
    "dequantization_checks.json": _dequant,
    "experiments.json": _experiment,
    "experiment_results.json": _result,
    "proof_status.json": _proof,
    "candidates.json": _candidate,
    "conjectures.json": _candidate,
    "mutation_proposals.json": _candidate,
    "rejected_candidates.json": _candidate,
}


def parse(root: Path, rel: str, issues: list[str] | None = None) -> list[Doc]:
    """One document per record; a record that cannot be read is skipped and named in `issues`."""
    issues = [] if issues is None else issues
    path = root / rel
    parser = PARSERS.get(path.name)
    if parser is None:
        return []
    records = read_json(path)
    if not isinstance(records, list):
        raise ValueError(f"expected a JSON list of records, found {type(records).__name__}")
    lines = _id_lines(path.read_text(encoding="utf-8"))
    # A claim repeated across many records is a template; title those records by their target.
    claim_counts: dict[str, int] = {}
    for record in records:
        if isinstance(record, dict) and parser is _dequant:
            claim = str(record.get("claim_under_test", ""))
            claim_counts[claim] = claim_counts.get(claim, 0) + 1
    docs = []
    skipped: list[str] = []
    for index, record in enumerate(records):
        if not isinstance(record, dict) or ("id" not in record and parser is not _proof):
            skipped.append(f"#{index} (not a record with an id)")
            continue
        try:
            doc_id, kind, title, text, meta = parser(record)
            if claim_counts.get(title, 0) > 3 and record.get("target_id"):
                title = f"{record['target_id']}: {title}"
                meta["templated"] = True
            line = lines.get(str(record.get("id", "")), 0)
            docs.append(Doc(doc_id, kind, rel, line, str(title)[:300], text, meta))
        except Exception as error:  # noqa: BLE001 - skip one malformed record, keep the rest
            skipped.append(f"{record.get('id', f'#{index}')} ({type(error).__name__}: {error})"[:200])
    if skipped:
        issues.append(f"skipped {len(skipped)} malformed record(s): " + "; ".join(skipped[:5])[:600])
    return unique_ids(docs)
