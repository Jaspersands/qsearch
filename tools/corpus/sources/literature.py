"""Parse literature records, per-topic literature audits and hypothesis contracts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from tools.corpus.docs import Doc, flatten, read_json, unique_ids

_SEED_FIELDS = (
    "abstract",
    "mechanism",
    "problem_family",
    "reduction",
    "no_go_barrier",
    "proof_technique",
    "open_question",
)


def parse_records(root: Path, rel: str, issues: list[str] | None = None) -> list[Doc]:
    data = read_json(root / rel)
    records = data if isinstance(data, list) else data.get("records", []) if isinstance(data, dict) else []
    docs = []
    for record in records:
        if not isinstance(record, dict) or "id" not in record:
            continue
        title = str(record.get("title", record["id"]))
        text = " ".join([title] + [str(record.get(name, "")) for name in _SEED_FIELDS] + [str(record.get("url") or "")])
        meta = {"url": record.get("url"), "year": record.get("year"), "tags": record.get("tags", []), "status": "seed"}
        docs.append(Doc(f"literature:{record['id']}", "literature", rel, 0, title[:300], text, meta))
    return unique_ids(docs)


def _without_urls(record: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in record.items() if key not in {"url", "pdf", "html"}}


def parse_audit(root: Path, rel: str, issues: list[str] | None = None) -> list[Doc]:
    path = root / rel
    data = read_json(path)
    stem = path.stem
    if isinstance(data, dict) and isinstance(data.get("records"), list):
        records, status, checked = data["records"], data.get("status"), data.get("checked_on")
    elif isinstance(data, list):
        records, status, checked = data, None, None
    else:
        return [Doc(f"literature:{stem}", "literature", rel, 0, stem, flatten(data, 4000), {"status": "audit"})]
    docs = []
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            continue
        rid = str(record.get("id", index))
        title = str(record.get("title", rid))
        meta = {"url": record.get("url"), "audit_status": status, "checked_on": checked, "status": "audit"}
        text = f"{flatten(_without_urls(record), 4000)} {rid} {record.get('url') or ''}"
        docs.append(Doc(f"literature:{stem}:{rid}", "literature", rel, 0, title[:300], text, meta))
    return unique_ids(docs)


def parse_hypothesis(root: Path, rel: str, issues: list[str] | None = None) -> list[Doc]:
    path = root / rel
    data = read_json(path)
    stem = path.stem
    record = data if isinstance(data, dict) else {"items": data}
    title = str(record.get("problem") or record.get("contract_id") or stem)
    meta = {"status": record.get("status"), "contract_id": record.get("contract_id")}
    return [Doc(f"hypothesis:{stem}", "hypothesis", rel, 0, flatten(title, 300), flatten(record, 4000), meta)]
