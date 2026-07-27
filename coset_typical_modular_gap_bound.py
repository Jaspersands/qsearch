"""Rigorous root-separation bounds for modularly certified typical blocks.

Square-freeness proves a nonzero gap, but an algorithm needs a quantitatively
usable gap.  This module clears denominators in the exact characteristic
polynomial using the YJM projector and orbit-average formulas, then applies the
integer discriminant bound.  The result is rigorous and intentionally
conservative; it demonstrates how little finite square-freeness alone says
about efficient phase estimation.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from coset_jucys_murphy_label_transform import (
    standard_young_tableaux,
    tableau_content_vector,
)
from representation_obstruction import conjugate_partition
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_yjm_projector_trace import (
    possible_yjm_contents,
    separator_terms,
)

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(100_000)


MODULAR_REPORT_PATH = Path(
    "research/representation/coset_typical_modular_yjm_contraction.json"
)
REPORT_PATH = Path(
    "research/representation/coset_typical_modular_gap_bounds.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-TYPICAL-MODULAR-GAP-BOUND"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CertifiedGapBoundRecord:
    n: int
    target_partition: list[int]
    multiplicity: int
    square_free_source: str
    yjm_projector_denominator: str
    yjm_projector_denominator_digits: int
    separator_common_denominator: int
    power_trace_common_denominator: str
    characteristic_clearing_denominator: str
    characteristic_clearing_denominator_digits: int
    root_pair_count: int
    lcu_normalized_gap_lower_bound_numerator: int
    lcu_normalized_gap_lower_bound_denominator_digits: int
    lcu_normalized_gap_lower_bound_denominator_sha256: str
    lcu_normalized_gap_lower_bound_log10: float
    inverse_polynomial_bound_established: bool


@dataclass(frozen=True)
class ModularGapBoundReport:
    created_at: str
    theorem_contract: dict[str, object]
    records: list[CertifiedGapBoundRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def yjm_projector_denominator(
    target_partition: tuple[int, ...],
    *,
    tableau_index: int = 0,
) -> int:
    tableaux = standard_young_tableaux(target_partition)
    if not 0 <= tableau_index < len(tableaux):
        raise ValueError("tableau index is out of range")
    content = tableau_content_vector(tableaux[tableau_index])
    denominator = 1
    for label in range(2, sum(target_partition) + 1):
        selected = content[label - 1]
        for alternative in possible_yjm_contents(label):
            if alternative != selected:
                denominator *= abs(selected - alternative)
    return denominator


def separator_common_denominator(n: int) -> int:
    return math.lcm(
        *(
            coefficient.denominator
            for _, coefficient in separator_terms(n)
        )
    )


def characteristic_clearing_denominator(
    multiplicity: int,
    projector_denominator: int,
    separator_denominator: int,
) -> tuple[int, int]:
    """Return ``(Q,B)`` with all traces over Q and ``B chi_H`` integral."""

    if multiplicity < 1:
        raise ValueError("multiplicity must be positive")
    power_trace_common = (
        projector_denominator * separator_denominator**multiplicity
    )
    clearing = (
        math.factorial(multiplicity)
        * power_trace_common**multiplicity
    )
    return power_trace_common, clearing


def _integer_log10(value: int) -> float:
    if value <= 0:
        raise ValueError("logarithm requires a positive integer")
    text = str(value)
    prefix_length = min(16, len(text))
    prefix = int(text[:prefix_length])
    return (
        len(text)
        - prefix_length
        + math.log10(prefix)
    )


def certified_gap_bound_record(
    target_partition: tuple[int, ...],
    multiplicity: int,
    *,
    square_free_source: str,
) -> CertifiedGapBoundRecord:
    n = sum(target_partition)
    projector = yjm_projector_denominator(target_partition)
    separator = separator_common_denominator(n)
    trace_denominator, clearing = characteristic_clearing_denominator(
        multiplicity,
        projector,
        separator,
    )
    pair_count = multiplicity * (multiplicity - 1) // 2
    # H has norm at most two. All non-minimal pair gaps are therefore at most 4.
    raw_gap_denominator = (
        clearing ** (multiplicity - 1)
        * 4 ** max(0, pair_count - 1)
    )
    lcu_normalized_denominator = 2 * raw_gap_denominator
    encoded = str(lcu_normalized_denominator)
    return CertifiedGapBoundRecord(
        n=n,
        target_partition=list(target_partition),
        multiplicity=multiplicity,
        square_free_source=square_free_source,
        yjm_projector_denominator=str(projector),
        yjm_projector_denominator_digits=len(str(projector)),
        separator_common_denominator=separator,
        power_trace_common_denominator=str(trace_denominator),
        characteristic_clearing_denominator=str(clearing),
        characteristic_clearing_denominator_digits=len(str(clearing)),
        root_pair_count=pair_count,
        lcu_normalized_gap_lower_bound_numerator=1,
        lcu_normalized_gap_lower_bound_denominator_digits=len(encoded),
        lcu_normalized_gap_lower_bound_denominator_sha256=hashlib.sha256(
            encoded.encode()
        ).hexdigest(),
        lcu_normalized_gap_lower_bound_log10=(
            -_integer_log10(lcu_normalized_denominator)
        ),
        inverse_polynomial_bound_established=False,
    )


def _load_modular_report(path: Path = MODULAR_REPORT_PATH) -> dict:
    resolved = path
    if not resolved.exists():
        resolved = Path(__file__).resolve().parent / path
    return json.loads(resolved.read_text())


def build_modular_gap_bound_report() -> ModularGapBoundReport:
    modular = _load_modular_report()
    direct = {
        tuple(record["target_partition"]): record
        for record in modular.get("n10_prime_certificates", [])
        if record.get(
            "rational_characteristic_polynomial_square_free_consequence",
            False,
        )
    }
    covered = set(direct)
    covered.update(conjugate_partition(target) for target in direct)
    records = [
        certified_gap_bound_record(
            target,
            int(
                (
                    direct.get(target)
                    or direct[conjugate_partition(target)]
                )["multiplicity"]
            ),
            square_free_source=(
                "direct-good-prime"
                if target in direct
                else (
                    "all-n-conjugate-sign-duality-from-"
                    + "-".join(
                        str(value)
                        for value in conjugate_partition(target)
                    )
                )
            ),
        )
        for target in sorted(covered, reverse=True)
    ]
    if not records:
        raise ArithmeticError("no exact modular square-free targets are available")
    strongest = max(
        record.lcu_normalized_gap_lower_bound_log10
        for record in records
    )
    weakest = min(
        record.lcu_normalized_gap_lower_bound_log10
        for record in records
    )
    metrics: dict[str, int | float] = {
        "exact_denominator_root_separation_theorem_count": 1,
        "square_free_target_bound_count": len(records),
        "maximum_bounded_multiplicity": max(
            record.multiplicity for record in records
        ),
        "maximum_characteristic_clearing_denominator_digits": max(
            record.characteristic_clearing_denominator_digits
            for record in records
        ),
        "maximum_gap_bound_denominator_digits": max(
            record.lcu_normalized_gap_lower_bound_denominator_digits
            for record in records
        ),
        "strongest_lcu_normalized_gap_lower_bound_log10": strongest,
        "weakest_lcu_normalized_gap_lower_bound_log10": weakest,
        "inverse_polynomial_normalized_gap_theorem_count": 0,
        "polynomial_phase_estimation_precision_certificate_count": 0,
        "all_n_simple_spectrum_theorem_count": 0,
        "coherent_typical_multiplicity_transform_count": 0,
        "typical_label_hidden_involution_decoder_count": 0,
    }
    return ModularGapBoundReport(
        created_at=utc_now(),
        theorem_contract={
            "trace_denominators": (
                "For degrees i<=m, Tr(P_T H^i) has denominator dividing "
                "D_P D_H^m, where D_P is the exact YJM Lagrange-projector "
                "denominator and D_H clears both orbit averages."
            ),
            "newton_denominators": (
                "Newton identities imply the kth characteristic coefficient "
                "has denominator dividing k! Q^k. Thus B=m! Q^m clears the "
                "entire monic characteristic polynomial."
            ),
            "discriminant": (
                "For square-free B chi_H in Z[x], the nonzero integer "
                "discriminant has magnitude at least one."
            ),
            "root_range": (
                "H is a sum of two Hermitian unitary averages, so every root "
                "lies in [-2,2] and every non-minimal pair gap is at most four."
            ),
            "bound": (
                "If M=m(m-1)/2, the raw minimum gap is at least "
                "B^{-(m-1)} 4^{-(M-1)}; LCU normalization contributes another 1/2."
            ),
            "interpretation": (
                "This is a rigorous existence bound, not evidence that the "
                "actual gaps are this small. Its role is to show that finite "
                "square-freeness does not establish efficient precision."
            ),
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "exact_nonzero_gap_bound_proved_for_certified_targets": True,
            "bound_is_inverse_polynomial_in_n": False,
            "efficient_phase_estimation_precision_proved": False,
            "all_n_simple_spectrum_proved": False,
            "coherent_transform_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact discriminant bound is nonzero but astronomically "
                "weak; no inverse-polynomial normalized gap or scalable "
                "measurement theorem follows."
            ),
        },
        status=(
            "exact-nonzero-gap-bounds-proved-efficient-precision-still-blocked"
        ),
        summary=(
            f"Exact denominator clearing yields rigorous normalized gap bounds "
            f"for {len(records)} n=10 targets, but even the strongest has "
            f"log10 lower bound {strongest:.1f}; square-freeness alone is "
            "far too weak to justify efficient phase estimation."
        ),
        falsifiers_triggered=[
            "A nonzero finite discriminant is not an inverse-polynomial gap theorem.",
            "Good-prime square-freeness alone supplies no useful real gap magnitude.",
            "The safest certified normalized lower bounds require thousands of decimal digits of precision.",
            "No all-n recurrence, coherent transform, decoder, or classical separation is supplied.",
        ],
    )


def write_modular_gap_bound_report(
    output_path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_modular_gap_bound_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TYPICAL-FINITE-SQUARE-FREE-DOES-NOT-CERTIFY-EFFICIENT-PRECISION",
                source=str(output_path),
                claim=(
                    "Exact square-freeness of the audited n=10 multiplicity "
                    "blocks is enough to justify efficient phase estimation."
                ),
                reason_invalid=(
                    "Safe denominator clearing and the integer discriminant give "
                    "only astronomically weak normalized gap lower bounds; the "
                    "best certified log10 bound is "
                    f"{payload['headline_metrics']['strongest_lcu_normalized_gap_lower_bound_log10']:.1f}."
                ),
                lesson=(
                    "Prove an inverse-polynomial normalized gap from separator "
                    "structure or reject phase-estimation implementations; do "
                    "not substitute finite square-freeness for precision analysis."
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
                artifacts={
                    "coset_typical_modular_gap_bounds": str(output_path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    print(
        json.dumps(
            write_modular_gap_bound_report()["headline_metrics"],
            indent=2,
            sort_keys=True,
        )
    )
