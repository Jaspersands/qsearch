"""Proof-obligation gate for candidate quantum algorithms."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


@dataclass(frozen=True)
class GateIssue:
    obligation_id: str
    field: str
    message: str
    hard_reject: bool = True


REQUIRED_FIELDS = {
    "PO-FAMILY": ("problem_family", "explicit asymptotic problem family"),
    "PO-INPUT-MODEL": ("input_model", "input/oracle/access model"),
    "PO-CLASSICAL-BASELINE": ("classical_baseline", "best known classical baseline or hardness evidence"),
    "PO-REDUCTION": ("reduction_or_lower_bound", "reduction, hardness link, or lower-bound target"),
    "PO-MECHANISM": ("quantum_mechanism", "specific quantum mechanism"),
    "PO-STATE-PREP": ("cost_model", "state preparation, encoding, precision, and reversible arithmetic costs"),
    "PO-MEASUREMENT": ("measurement_and_decoding", "measurement and decoding procedure"),
    "PO-SUCCESS-PROOF": ("success_statement", "success theorem or conjecture with parameters"),
    "PO-COMPLEXITY": ("complexity_accounting", "query, gate, space, precision, and postprocessing complexity"),
    "PO-NOGO": ("no_go_analysis", "known no-go barriers and escape route"),
    "PO-DEQUANTIZATION": ("dequantization_check", "classical randomized/dequantized baseline check"),
    "PO-FALSIFIERS": ("falsifiers", "experiments or counterexamples that would kill the idea"),
}


LOW_VALUE_MARKERS = (
    "brute force",
    "custom oracle",
    "n<=3",
    "n = 3",
    "small example",
    "qiskit simulation",
)


def _is_missing(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return len(value) == 0
    return False


def validate_candidate(candidate: Mapping[str, object]) -> list[GateIssue]:
    """Return hard-reject issues for an algorithm candidate."""

    issues: list[GateIssue] = []
    text_blob = " ".join(str(value).lower() for value in candidate.values())

    for obligation_id, (field, description) in REQUIRED_FIELDS.items():
        if _is_missing(candidate.get(field)):
            issues.append(
                GateIssue(
                    obligation_id=obligation_id,
                    field=field,
                    message=f"Missing {description}.",
                )
            )

    if "classical_baseline" in candidate:
        baseline = str(candidate.get("classical_baseline", "")).lower()
        if baseline.strip() in {"brute force", "exhaustive search", "o(2^n)", "o(2**n)"}:
            issues.append(
                GateIssue(
                    obligation_id="PO-CLASSICAL-BASELINE",
                    field="classical_baseline",
                    message="Baseline is too weak; compare against best known classical algorithms, not brute force.",
                )
            )

    if any(marker in text_blob for marker in LOW_VALUE_MARKERS):
        issues.append(
            GateIssue(
                obligation_id="PO-FAMILY",
                field="problem_family",
                message="Candidate contains low-value toy/circuit/oracle markers; justify natural scalable structure or reject.",
            )
        )

    return issues


def passes_proof_gate(candidate: Mapping[str, object]) -> bool:
    return not any(issue.hard_reject for issue in validate_candidate(candidate))
