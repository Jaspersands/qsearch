"""Audit declared proof dependencies, not mathematical truth.

An attestation is a scoped, provenance-pinned research assertion. This module
does not turn it into a proof. Alternative routes are OR; each route's premises,
conclusion attestations and diagnostics are AND. Failed diagnostics block a
route without automatically refuting its conclusion.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

LEVELS = {"unresolved": 0, "observed": 1, "exact-finite": 2, "derived-review-pending": 3}
LEVEL_NAMES = {value: key for key, value in LEVELS.items()}
MANIFEST_PATH = Path("research/registry/proof_routes.json")
REPORT_PATH = Path("research/proof_route_audit.json")


def _pointer(value: Any, pointer: str) -> Any:
    if pointer == "":
        return value
    if not pointer.startswith("/"):
        raise ValueError("expected an RFC6901 JSON pointer")
    for part in pointer[1:].split("/"):
        if re.search(r"~(?![01])", part):
            raise ValueError("invalid JSON pointer escape")
        part = part.replace("~1", "/").replace("~0", "~")
        if isinstance(value, list):
            if not re.fullmatch(r"0|[1-9][0-9]*", part):
                raise ValueError("invalid JSON pointer array index")
            value = value[int(part)]
        else:
            value = value[part]
    return value


def _scope(value: Any) -> bool:
    return isinstance(value, dict) and value.get("quantifier") in {"finite", "universal"} and all(
        isinstance(value.get(key), str) and bool(value[key].strip())
        for key in ("domain", "input_model", "conclusion"))


def audit_proof_routes(manifest: dict[str, Any], root: Path = Path(".")) -> dict[str, Any]:
    if manifest.get("schema_version") != 1:
        raise ValueError("unsupported proof-route schema")
    claims, evidence = {}, {}
    for table, name in ((claims, "claims"), (evidence, "evidence")):
        for row in manifest.get(name, []):
            identifier = row.get("id")
            if not isinstance(identifier, str) or not identifier or identifier in table:
                raise ValueError(f"missing or duplicate {name} id")
            table[identifier] = row
    for claim in claims.values():
        if not _scope(claim.get("scope")) or claim.get("asserted_level") not in LEVELS:
            raise ValueError(f"invalid claim scope or evidence level: {claim['id']}")
        route_ids = [route.get("id") for route in claim.get("routes", [])]
        if any(not isinstance(value, str) or not value for value in route_ids) or len(set(route_ids)) != len(route_ids):
            raise ValueError(f"invalid route identifiers: {claim['id']}")

    issues: list[dict[str, str]] = []
    root = root.resolve()
    checked_files: dict[str, tuple[bytes | None, str]] = {}

    def issue(claim_id: str, route_id: str, code: str, detail: str) -> None:
        issues.append({"claim_id": claim_id, "route_id": route_id, "code": code, "detail": detail})

    def check_file(reference: dict[str, Any]) -> tuple[bytes | None, str]:
        path_text, digest = reference.get("path", ""), reference.get("sha256", "")
        if not isinstance(path_text, str) or not path_text or not isinstance(digest, str) or len(digest) != 64:
            return None, "invalid-provenance"
        path = (root / path_text).resolve()
        if not path.is_relative_to(root):
            return None, "outside-repository"
        key = str(path)
        if key not in checked_files:
            try:
                data = path.read_bytes()
                checked_files[key] = (data, hashlib.sha256(data).hexdigest())
            except OSError:
                checked_files[key] = (None, "missing-source")
        data, actual = checked_files[key]
        return (data, "") if actual == digest else (None, "missing-source" if data is None else "stale-source")

    def check_evidence(identifier: str, claim: dict[str, Any], route_id: str, diagnostic: bool) -> int:
        reference = evidence.get(identifier)
        if reference is None:
            issue(claim["id"], route_id, "missing-evidence", str(identifier))
            return 0
        level = reference.get("level")
        if not diagnostic and (reference.get("claim_id") != claim["id"] or reference.get("scope") != claim["scope"]):
            issue(claim["id"], route_id, "scope-mismatch", identifier)
            return 0
        if not diagnostic and level not in LEVELS:
            issue(claim["id"], route_id, "unsupported-evidence-level", identifier)
            return 0
        data, error = check_file(reference)
        if error:
            issue(claim["id"], route_id, error, identifier)
            return 0
        predicates = reference.get("predicates", [])
        if diagnostic and not predicates:
            issue(claim["id"], route_id, "diagnostic-without-predicate", identifier)
            return 0
        for predicate in predicates:
            try:
                actual = _pointer(json.loads(data), predicate["pointer"])
                # JSON booleans are not interchangeable with integers here.
                matched = json.dumps(actual, sort_keys=True, allow_nan=False) == json.dumps(predicate["equals"], sort_keys=True, allow_nan=False)
            except (KeyError, IndexError, ValueError, TypeError):
                matched = False
            if not matched:
                issue(claim["id"], route_id, "failed-diagnostic", identifier)
                return 0
        return 1 if diagnostic else LEVELS[level]

    prepared = {}
    for identifier, claim in claims.items():
        routes = []
        for route in claim.get("routes", []):
            route_id = route["id"]
            conclusion_evidence = route.get("conclusion_evidence", [])
            levels = [check_evidence(ref, claim, route_id, False) for ref in conclusion_evidence]
            if not levels:
                issue(identifier, route_id, "missing-conclusion-attestation", "Premises alone do not establish a different conclusion.")
                levels = [0]
            for premise in route.get("premises", []):
                if premise not in claims:
                    issue(identifier, route_id, "missing-premise", premise)
                    levels.append(0)
            for check in route.get("diagnostics", []):
                if check_evidence(check, claim, route_id, True) == 0:
                    levels.append(0)
            rank = min(levels)
            if claim["scope"]["quantifier"] == "universal" and 0 < rank < LEVELS["derived-review-pending"]:
                issue(identifier, route_id, "finite-to-universal-promotion", "Finite evidence does not establish this uniform claim.")
                rank = 0
            routes.append({"id": route_id, "base_rank": rank, "premises": route.get("premises", [])})
        prepared[identifier] = routes

    # Least fixed point prevents circular self-certification while allowing an
    # independently grounded alternative to support downstream claims in a cycle.
    ranks = dict.fromkeys(claims, 0)

    def route_rank(identifier: str, route: dict[str, Any]) -> int:
        value = min([route["base_rank"], *[ranks.get(premise, 0) for premise in route["premises"]]])
        return 0 if claims[identifier]["scope"]["quantifier"] == "universal" and value < 3 else value

    for _ in range(3 * len(claims) + 1):
        following = {identifier: max((route_rank(identifier, route) for route in routes), default=0)
                     for identifier, routes in prepared.items()}
        if following == ranks:
            break
        ranks = following

    def reaches(start: str, target: str, seen: set[str]) -> bool:
        if start == target:
            return True
        if start in seen or start not in prepared:
            return False
        seen.add(start)
        return any(reaches(premise, target, seen) for route in prepared[start] for premise in route["premises"])

    results = {}
    for identifier, claim in claims.items():
        routes = []
        for route in prepared[identifier]:
            rank = route_rank(identifier, route)
            for premise in route["premises"]:
                if premise in claims and ranks[premise] == 0:
                    issue(identifier, route["id"], "dependency-cycle" if reaches(premise, identifier, set()) else "unresolved-premise", premise)
            routes.append({"id": route["id"], "support_rank": rank, "supported_level": LEVEL_NAMES[rank]})
        rank = ranks[identifier]
        asserted = LEVELS[claim["asserted_level"]]
        row = {"id": identifier, "scope": claim["scope"], "asserted_level": claim["asserted_level"],
               "supported_level": LEVEL_NAMES[rank], "support_rank": rank,
               "unsupported_assertion": asserted > rank, "routes": routes}
        if asserted > rank:
            issue(identifier, "", "unsupported-assertion", f"Asserted {claim['asserted_level']}; available contract support is {LEVEL_NAMES[rank]}.")
        results[identifier] = row
    unsupported = sum(row["unsupported_assertion"] for row in results.values())
    return {
        "schema_version": 1, "claim_count": len(claims), "claims": list(results.values()), "issues": issues,
        "unsupported_assertion_count": unsupported,
        "unresolved_claim_count": sum(row["support_rank"] == 0 for row in results.values()),
        "status": "unsupported-assertions" if unsupported else "declared-assertions-consistent-with-contracts",
        "mathematical_truth_verified": False, "speedup_claim_allowed": False,
        "scope": "Declared dependency and provenance audit only. Attestations remain research assertions, not machine-checked proofs.",
    }


def write_proof_route_audit(manifest_path: Path = MANIFEST_PATH, report_path: Path = REPORT_PATH) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text())
    report = audit_proof_routes(manifest)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    return report
