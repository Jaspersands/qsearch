"""Exact n=10 transfer feasibility and first collision probe."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

import sympy as sp

from coset_typical_high_multiplicity_transfer import EIGENVALUE
from coset_typical_n9_low_multiplicity_probe import _characteristic_polynomial
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


COSET_TYPICAL_N10_FEASIBILITY_PATH = Path(
    "research/representation/coset_typical_n10_feasibility.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-TYPICAL-N10-FEASIBILITY"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
SOURCE_PARTITION = (4, 3, 2, 1)
SOURCE_DIMENSION = 768
NONTRIVIAL_TARGET_COUNT = 40
MAXIMUM_MULTIPLICITY = 117
TRANSFER_STATE_COUNTS = {
    1: 2,
    2: 87,
    3: 2161,
    4: 54168,
    5: 310071,
}
TARGET_CERTIFICATES = (
    {
        "target": (9, 1),
        "dimension": 9,
        "multiplicity": 3,
        "traces": ("-7/48", "7247/1016064", "-815/2322432"),
    },
    {
        "target": (2, 1, 1, 1, 1, 1, 1, 1, 1),
        "dimension": 9,
        "multiplicity": 3,
        "traces": ("7/48", "7247/1016064", "815/2322432"),
    },
)


@dataclass(frozen=True)
class N10FirstTargetRecord:
    target_partition: tuple[int, ...]
    target_dimension: int
    kronecker_multiplicity: int
    exact_power_traces: list[str]
    exact_characteristic_polynomial: str
    exact_square_free_gcd: str
    certified_minimum_raw_gap_lower_bound: float
    characteristic_polynomial_square_free: bool
    status: str


@dataclass(frozen=True)
class N10FeasibilityReport:
    created_at: str
    feasibility_contract: dict[str, object]
    records: list[N10FirstTargetRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def build_n10_feasibility_report() -> N10FeasibilityReport:
    records = []
    for item in TARGET_CERTIFICATES:
        traces = tuple(Fraction(value) for value in item["traces"])
        polynomial = sp.Poly(_characteristic_polynomial(traces), EIGENVALUE)
        gcd = sp.gcd(polynomial, polynomial.diff())
        intervals = polynomial.intervals(eps=sp.Rational(1, 10**12))
        bounds = [interval for interval, _ in intervals]
        lower = min(
            right[0] - left[1] for left, right in zip(bounds, bounds[1:])
        )
        square_free = gcd.degree() == 0 and all(
            multiplicity == 1 for _, multiplicity in intervals
        )
        if not square_free:
            raise ArithmeticError(f"n=10 repeated root on {item['target']}")
        records.append(
            N10FirstTargetRecord(
                target_partition=item["target"],
                target_dimension=int(item["dimension"]),
                kronecker_multiplicity=int(item["multiplicity"]),
                exact_power_traces=[str(value) for value in traces],
                exact_characteristic_polynomial=str(
                    sp.factor(polynomial.as_expr())
                ),
                exact_square_free_gcd=str(gcd.as_expr()),
                certified_minimum_raw_gap_lower_bound=float(lower),
                characteristic_polynomial_square_free=True,
                status="exact-n10-first-target-simple-spectrum",
            )
        )
    minimum_gap = min(
        record.certified_minimum_raw_gap_lower_bound for record in records
    )
    metrics: dict[str, int | float] = {
        "n": 10,
        "source_dimension": SOURCE_DIMENSION,
        "maximum_exact_transfer_degree": 5,
        "degree5_transfer_state_count": TRANSFER_STATE_COUNTS[5],
        "degree5_transfer_state_union_count": 364239,
        "degree5_unique_left_translation_count": 4132,
        "degree5_unique_right_translation_count": 12630,
        "degree5_naive_temporary_character_table_bytes": 91663488000,
        "degree3_exact_contraction_target_count": len(records),
        "degree3_quotient_state_union_count": 2248,
        "degree3_unique_left_translation_count": 268,
        "degree3_unique_right_translation_count": 395,
        "degree3_conjugacy_class_count": 42,
        "degree3_temporary_character_table_bytes": 2866752000,
        "degree3_maximum_character_chunk_bytes_at_128_rows": 928972800,
        "certified_n10_simple_spectrum_target_count": len(records),
        "n10_nontrivial_multiplicity_target_count": NONTRIVIAL_TARGET_COUNT,
        "n10_unaudited_target_count": NONTRIVIAL_TARGET_COUNT - len(records),
        "maximum_certified_kronecker_multiplicity": 3,
        "maximum_n10_kronecker_multiplicity": MAXIMUM_MULTIPLICITY,
        "certified_n10_minimum_raw_gap_lower_bound": minimum_gap,
        "all_n10_target_simple_spectrum_theorem_count": 0,
        "scalable_s10_character_contraction_count": 0,
        "all_n_simple_spectrum_theorem_count": 0,
        "inverse_polynomial_normalized_gap_theorem_count": 0,
        "coherent_typical_multiplicity_transform_count": 0,
        "typical_label_hidden_involution_decoder_count": 0,
    }
    return N10FeasibilityReport(
        created_at=utc_now(),
        feasibility_contract={
            "source": "lambda=(4,3,2,1), self-conjugate, dimension 768",
            "transfer": (
                "Exact parallel quotient transfer through degree five with total weight 2*10080^(degree-1)."
            ),
            "first_target_contraction": (
                "Exact class-Fourier contraction through degree three for both multiplicity-three conjugate targets."
            ),
            "scaling_boundary": (
                "Extending the same explicit translation table through degree five requires 12630 S_10 character rows, or 91.7 GB before contraction."
            ),
            "all_target_claimed": False,
            "algorithmic_speedup_claimed": False,
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "first_n10_targets_simple_spectrum": True,
            "all_n10_targets_audited": False,
            "scalable_s10_character_contraction_proved": False,
            "all_n_simple_spectrum_proved": False,
            "inverse_polynomial_normalized_gap_proved": False,
            "coherent_transform_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Only two of 40 n=10 blocks are certified; explicit S_10 translation storage grows to 91.7 GB by degree five and multiplicities reach 117."
            ),
        },
        status="n10-first-targets-survive-scalable-contraction-blocked",
        summary=(
            "The fixed separator has exact simple spectrum on both multiplicity-three n=10 targets, while degree-five transfer exposes a 91.7 GB naive character-contraction barrier and leaves 38 targets unaudited."
        ),
        falsifiers_triggered=[
            "The first n=10 multiplicity-three cubics do not contain a repeated root.",
            "Only 2 of 40 n=10 targets are audited.",
            "The explicit translation table reaches 91.7 GB by degree five.",
            "No scalable S_10 contraction, all-n gap, coherent transform, or decoder is proved.",
        ],
    )


def write_n10_feasibility_report(
    output_path: Path = COSET_TYPICAL_N10_FEASIBILITY_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_n10_feasibility_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TYPICAL-N10-EXPLICIT-TRANSLATION-CONTRACTION-SCALING",
                source=str(output_path),
                claim=(
                    "The explicit n=9 translation-contraction architecture scales directly to n=10 and beyond."
                ),
                reason_invalid=(
                    "At n=10, degree-five support already requires 12630 rows over 10!, or 91.7 GB, while only multiplicity three has been contracted and target multiplicities reach 117."
                ),
                lesson=(
                    "Replace explicit group-row storage with a representation- or class-algebra recurrence before extending the finite collision ladder."
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
                artifacts={"coset_typical_n10_feasibility": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    print(
        json.dumps(
            write_n10_feasibility_report()["headline_metrics"],
            indent=2,
            sort_keys=True,
        )
    )
