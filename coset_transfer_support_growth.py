"""Exact support-growth barrier for the TT1+TC1 quotient transfer.

Marked conjugacy-class contraction is polynomial in ``n`` only while the
canonical pair has bounded active support.  This audit measures the exact
transfer weight outside that regime.  It closes only the direct termwise
fixed-support extension; it does not rule out a new full-support recurrence.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import defaultdict
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

from coset_typical_high_multiplicity_transfer import TRANSFER_KERNEL_PATH
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


CERTIFICATE_PATH = Path(
    "research/certificates/coset_transfer_support_growth_certificate.json"
)
REPORT_PATH = Path(
    "research/representation/coset_transfer_support_growth.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-TYPICAL-TRANSFER-SUPPORT-GROWTH"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class TransferSupportRecord:
    n: int
    degree: int
    state_count: int
    state_count_by_support: dict[str, int]
    total_weight: str
    full_support_state_count: int
    full_support_weight_fraction_exact: str
    full_support_weight_fraction: float
    at_most_n_minus_2_weight_fraction_exact: str
    at_most_n_minus_2_weight_fraction: float
    at_least_n_minus_1_weight_fraction: float
    full_support_marked_injection_count: int
    support_at_most_n_minus_2_termwise_coverage_complete: bool


@dataclass(frozen=True)
class TransferSupportGrowthReport:
    created_at: str
    support_contract: dict[str, object]
    records: list[TransferSupportRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def packed_pair_support_size(key: int, n: int) -> int:
    """Return the active support of a kernel-packed permutation pair."""

    if not 1 <= n <= 16:
        raise ValueError("packed transfer keys support 1 <= n <= 16")
    support = 0
    for point in range(n):
        left = (key >> (4 * point)) & 15
        right = (key >> (4 * n + 4 * point)) & 15
        if left >= n or right >= n:
            raise ValueError("packed key is not a permutation pair of degree n")
        support += left != point or right != point
    return support


def support_profile_from_distribution(
    n: int,
    distribution: dict[int, int],
) -> dict[str, object]:
    """Aggregate one exact transfer distribution by active support."""

    if not distribution:
        raise ValueError("transfer distribution must not be empty")
    state_counts: defaultdict[int, int] = defaultdict(int)
    weights: defaultdict[int, int] = defaultdict(int)
    for key, weight in distribution.items():
        if weight <= 0:
            raise ValueError("transfer weights must be positive")
        support = packed_pair_support_size(key, n)
        state_counts[support] += 1
        weights[support] += weight
    total_weight = sum(weights.values())
    full_fraction = Fraction(weights[n], total_weight)
    bounded_fraction = Fraction(
        sum(weight for support, weight in weights.items() if support <= n - 2),
        total_weight,
    )
    return {
        "state_count_by_support": {
            str(support): count for support, count in sorted(state_counts.items())
        },
        "weight_by_support": {
            str(support): str(weight) for support, weight in sorted(weights.items())
        },
        "total_weight": str(total_weight),
        "full_support_weight_fraction": str(full_fraction),
        "at_most_n_minus_2_weight_fraction": str(bounded_fraction),
    }


def _load_certificate(path: Path = CERTIFICATE_PATH) -> dict:
    resolved = path
    if not resolved.exists():
        resolved = Path(__file__).resolve().parent / path
    payload = json.loads(resolved.read_text())
    kernel = Path(__file__).resolve().parent / TRANSFER_KERNEL_PATH
    digest = hashlib.sha256(kernel.read_bytes()).hexdigest()
    if payload.get("certificate_contract", {}).get("kernel_sha256") != digest:
        raise ArithmeticError("support-growth certificate does not match transfer kernel")
    return payload


def _validated_records(certificate: dict) -> list[TransferSupportRecord]:
    records: list[TransferSupportRecord] = []
    seen: set[tuple[int, int]] = set()
    for row in certificate.get("records", []):
        n = int(row["n"])
        degree = int(row["degree"])
        if (n, degree) in seen:
            raise ArithmeticError("duplicate support-growth certificate row")
        seen.add((n, degree))
        total_weight = int(row["total_weight"])
        orbit_step_weight = 2 * n * (n - 1) * (n - 2) * (n - 3)
        expected_total = 2 * orbit_step_weight ** (degree - 1)
        if total_weight != expected_total:
            raise ArithmeticError("support-growth total violates transfer contract")
        state_counts = {
            str(support): int(count)
            for support, count in row["state_count_by_support"].items()
        }
        full = Fraction(row["full_support_weight_fraction"])
        bounded = Fraction(row["at_most_n_minus_2_weight_fraction"])
        if not (0 <= full <= 1 and 0 <= bounded <= 1):
            raise ArithmeticError("invalid support-growth weight fraction")
        if (full * total_weight).denominator != 1:
            raise ArithmeticError("full-support fraction is incompatible with total weight")
        if (bounded * total_weight).denominator != 1:
            raise ArithmeticError("bounded-support fraction is incompatible with total weight")
        records.append(
            TransferSupportRecord(
                n=n,
                degree=degree,
                state_count=sum(state_counts.values()),
                state_count_by_support=state_counts,
                total_weight=str(total_weight),
                full_support_state_count=state_counts.get(str(n), 0),
                full_support_weight_fraction_exact=str(full),
                full_support_weight_fraction=float(full),
                at_most_n_minus_2_weight_fraction_exact=str(bounded),
                at_most_n_minus_2_weight_fraction=float(bounded),
                at_least_n_minus_1_weight_fraction=float(1 - bounded),
                full_support_marked_injection_count=math.factorial(n),
                support_at_most_n_minus_2_termwise_coverage_complete=(
                    bounded == 1
                ),
            )
        )
    if not records:
        raise ArithmeticError("support-growth certificate is empty")
    return sorted(records, key=lambda record: (record.n, record.degree))


def build_transfer_support_growth_report() -> TransferSupportGrowthReport:
    records = _validated_records(_load_certificate())
    by_key = {(record.n, record.degree): record for record in records}
    n8 = by_key[(8, 17)]
    n9 = by_key[(9, 28)]
    n10 = by_key[(10, 5)]
    metrics: dict[str, int | float] = {
        "audited_size_count": len({record.n for record in records}),
        "exact_support_checkpoint_count": len(records),
        "maximum_audited_degree": max(record.degree for record in records),
        "n8_degree17_full_support_weight_fraction": (
            n8.full_support_weight_fraction
        ),
        "n9_degree28_full_support_weight_fraction": (
            n9.full_support_weight_fraction
        ),
        "n9_degree28_at_most_support7_weight_fraction": (
            n9.at_most_n_minus_2_weight_fraction
        ),
        "n10_degree5_full_support_weight_fraction": (
            n10.full_support_weight_fraction
        ),
        "n10_degree5_support9_or_10_weight_fraction": (
            n10.at_least_n_minus_1_weight_fraction
        ),
        "n10_full_support_marked_injection_count": (
            n10.full_support_marked_injection_count
        ),
        "direct_fixed_support_termwise_extension_falsification_count": 1,
        "scalable_full_support_character_contraction_count": 0,
        "all_n_support_concentration_theorem_count": 0,
    }
    return TransferSupportGrowthReport(
        created_at=utc_now(),
        support_contract={
            "operator": "H_n=average(TT1)+average(TC1)",
            "support_definition": (
                "Points moved by either member of a simultaneous-conjugacy pair."
            ),
            "exact_method": (
                "Aggregate arbitrary-precision quotient-transfer weights by support; "
                "the certificate is hash-gated to the C++ transfer kernel."
            ),
            "bounded_support_contraction_cost": (
                "The marked-class method enumerates n falling-factorial s injections "
                "for pair support s; at s=n this is n!."
            ),
            "claim_scope": (
                "This falsifies direct termwise completion by a fixed support bound. "
                "It does not rule out a representation-theoretic recurrence that "
                "contracts full-support pair states collectively."
            ),
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "direct_fixed_support_termwise_completion_viable": False,
            "full_support_pair_weight_is_positive": True,
            "full_support_pair_weight_dominates_n9_high_degree": True,
            "new_full_support_recurrence_required": True,
            "scalable_full_support_recurrence_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Full-support pairs carry 89.5% of exact n=9 degree-28 weight, "
                "and support 9 or 10 carries 62.0% at n=10 degree five. The "
                "fixed-support marked-injection evaluator therefore degenerates "
                "to factorial work on the states that dominate the required traces."
            ),
        },
        status="direct-fixed-support-extension-falsified-full-support-recurrence-open",
        summary=(
            "Exact transfer support concentrates on full-support pair orbits: "
            "89.5% at n=9 degree 28. Bounded-support class contraction remains "
            "useful for low moments but cannot directly finish the n=10 collision ladder."
        ),
        falsifiers_triggered=[
            "At n=9 degree 28, full-support pairs carry more than 89% of exact transfer weight.",
            "At n=10 degree five, support nine or ten carries more than 61% of exact transfer weight.",
            "The marked-injection count for a full-support n=10 pair is 10!, so its fixed-support advantage disappears.",
            "No all-n concentration theorem or scalable collective full-support contraction has been proved.",
        ],
    )


def write_transfer_support_growth_report(
    output_path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_transfer_support_growth_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TYPICAL-DIRECT-FIXED-SUPPORT-TRANSFER-CONTRACTION",
                source=str(output_path),
                claim=(
                    "The fixed-support marked-class contraction can be applied "
                    "termwise to finish high-degree typical-irrep transfer traces."
                ),
                reason_invalid=(
                    "Full-support pairs carry 89.5% of n=9 degree-28 weight and "
                    "20.5% of n=10 degree-five weight; support nine or ten carries "
                    "62.0% at n=10 degree five. Marked injection costs n! there."
                ),
                lesson=(
                    "Stop extending fixed-support injection enumeration. Search "
                    "for a collective representation, centralizer, branching, or "
                    "tensor-network recurrence over full-support pair orbits."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-LATEST"
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"coset_transfer_support_growth": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    print(
        json.dumps(
            write_transfer_support_growth_report()["headline_metrics"],
            indent=2,
            sort_keys=True,
        )
    )
