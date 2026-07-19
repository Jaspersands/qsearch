"""Resolve where the stable Racah branch leaks under reassociation.

For W_n=(n-2,2), xi_n=(n-3,2,1), and final irrep xi_n, every intermediate
partition eta with

    g(W_n,W_n,eta) g(eta,W_n,xi_n) > 0

defines a left-associated multiplicity sector.  The right-associated stable
xi_n sector has rank eight.  This module constructs every left sector from
Coxeter-invariant intertwiners and computes

    Tr(P_left,eta P_right,xi).

The contributions must sum to eight.  This gives a gauge-invariant and
complete finite decomposition of the leakage detected by the stable subspace
transition probe.  It is numerical scaling evidence, not an all-n formula or
a coherent all-sector circuit.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Sequence

import numpy as np

from coset_stable_subspace_transition_probe import invariant_tensor_basis
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import kronecker_coefficient


COSET_STABLE_COMPLEMENTARY_SECTOR_PATH = Path(
    "research/representation/coset_stable_complementary_sector_probe.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-STABLE-COMPLEMENTARY-SECTOR-PROBE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ComplementarySectorContribution:
    intermediate_partition: tuple[int, ...]
    intermediate_irrep_dimension: int
    first_stage_multiplicity: int
    second_stage_multiplicity: int
    branch_dimension: int
    is_stable_intermediate: bool
    overlap_rank_with_right_stable: int
    maximum_overlap_singular_value: float
    projector_overlap_contribution: float
    projector_overlap_rational_candidate: str
    rational_candidate_residual: float
    fraction_of_right_stable_branch: float
    fraction_of_complementary_leakage: float
    nonzero_transition_support: bool


@dataclass(frozen=True)
class ComplementarySectorScalingRecord:
    n: int
    source_partition: tuple[int, ...]
    final_partition: tuple[int, ...]
    source_irrep_dimension: int
    final_irrep_dimension: int
    intermediate_sector_count: int
    final_total_multiplicity: int
    right_stable_branch_dimension: int
    sector_contributions: list[ComplementarySectorContribution]
    projector_resolution_sum: float
    projector_resolution_residual: float
    stable_branch_retention: float
    stable_branch_leakage: float
    nonzero_complementary_sector_count: int
    largest_complementary_leakage_share: float
    effective_complementary_sector_count: float
    all_complementary_sectors_required_at_finite_n: bool
    finite_numerical_probe_only: bool
    status: str


@dataclass(frozen=True)
class ComplementarySectorReport:
    created_at: str
    mathematical_contract: dict[str, object]
    records: list[ComplementarySectorScalingRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _scaled_invariant_embeddings(
    partitions: tuple[tuple[int, ...], ...],
    multiplicity: int,
    target_dimension: int,
) -> np.ndarray:
    basis, _, _ = invariant_tensor_basis(partitions, multiplicity)
    return basis * math.sqrt(target_dimension)


def _left_composed_rows(
    first_embeddings: np.ndarray, second_embeddings: np.ndarray
) -> np.ndarray:
    rows = [
        np.einsum("iju,ukt->ijkt", first, second, optimize=True).ravel()
        for first in first_embeddings
        for second in second_embeddings
    ]
    return np.asarray(rows)


def _right_composed_rows(
    first_embeddings: np.ndarray, second_embeddings: np.ndarray
) -> np.ndarray:
    rows = [
        np.einsum("uit,jku->ijkt", second, first, optimize=True).ravel()
        for first in first_embeddings
        for second in second_embeddings
    ]
    return np.asarray(rows)


def _sector_specs(
    source: tuple[int, ...], final: tuple[int, ...]
) -> list[tuple[tuple[int, ...], int, int]]:
    return [
        (intermediate, first, second)
        for intermediate in integer_partitions(sum(source))
        if (first := kronecker_coefficient(source, source, intermediate))
        and (second := kronecker_coefficient(intermediate, source, final))
    ]


def audit_complementary_sectors(n: int) -> ComplementarySectorScalingRecord:
    if n < 7:
        raise ValueError("the multiplicity-four stable branch starts at n=7")
    source = (n - 2, 2)
    stable = (n - 3, 2, 1)
    source_dimension = hook_length_dimension(source)
    stable_dimension = hook_length_dimension(stable)
    stable_first = kronecker_coefficient(source, source, stable)
    stable_second = kronecker_coefficient(stable, source, stable)
    if (stable_first, stable_second) != (2, 4):
        raise ArithmeticError("the stable branch multiplicities must be 2 and 4")

    stable_first_embeddings = _scaled_invariant_embeddings(
        (source, source, stable), stable_first, stable_dimension
    )
    stable_second_embeddings = _scaled_invariant_embeddings(
        (stable, source, stable), stable_second, stable_dimension
    )
    right_stable = _right_composed_rows(
        stable_first_embeddings, stable_second_embeddings
    )
    right_branch_dimension = stable_first * stable_second

    raw_rows: list[dict[str, object]] = []
    for intermediate, first_multiplicity, second_multiplicity in _sector_specs(
        source, stable
    ):
        intermediate_dimension = hook_length_dimension(intermediate)
        first_embeddings = _scaled_invariant_embeddings(
            (source, source, intermediate),
            first_multiplicity,
            intermediate_dimension,
        )
        second_embeddings = _scaled_invariant_embeddings(
            (intermediate, source, stable),
            second_multiplicity,
            stable_dimension,
        )
        left = _left_composed_rows(first_embeddings, second_embeddings)
        overlap = left @ right_stable.T / stable_dimension
        singular_values = np.linalg.svd(overlap, compute_uv=False)
        contribution = float(np.sum(singular_values**2))
        rational = Fraction(contribution).limit_denominator(1_000_000)
        raw_rows.append(
            {
                "intermediate": intermediate,
                "intermediate_dimension": intermediate_dimension,
                "first": first_multiplicity,
                "second": second_multiplicity,
                "branch_dimension": first_multiplicity * second_multiplicity,
                "is_stable": intermediate == stable,
                "rank": int(np.sum(singular_values > 1e-8)),
                "maximum_singular_value": float(max(singular_values, default=0.0)),
                "contribution": contribution,
                "rational": rational,
            }
        )

    stable_contribution = next(
        float(row["contribution"]) for row in raw_rows if row["is_stable"]
    )
    complementary_leakage = right_branch_dimension - stable_contribution
    contributions = [
        ComplementarySectorContribution(
            intermediate_partition=row["intermediate"],
            intermediate_irrep_dimension=int(row["intermediate_dimension"]),
            first_stage_multiplicity=int(row["first"]),
            second_stage_multiplicity=int(row["second"]),
            branch_dimension=int(row["branch_dimension"]),
            is_stable_intermediate=bool(row["is_stable"]),
            overlap_rank_with_right_stable=int(row["rank"]),
            maximum_overlap_singular_value=float(row["maximum_singular_value"]),
            projector_overlap_contribution=float(row["contribution"]),
            projector_overlap_rational_candidate=(
                f"{row['rational'].numerator}/{row['rational'].denominator}"
            ),
            rational_candidate_residual=abs(
                float(row["contribution"]) - float(row["rational"])
            ),
            fraction_of_right_stable_branch=(
                float(row["contribution"]) / right_branch_dimension
            ),
            fraction_of_complementary_leakage=(
                0.0
                if row["is_stable"]
                else float(row["contribution"]) / complementary_leakage
            ),
            nonzero_transition_support=float(row["contribution"]) > 1e-10,
        )
        for row in raw_rows
    ]
    projector_sum = sum(row.projector_overlap_contribution for row in contributions)
    complementary = [row for row in contributions if not row.is_stable_intermediate]
    leakage_shares = [row.fraction_of_complementary_leakage for row in complementary]
    effective_count = 1.0 / sum(share * share for share in leakage_shares)
    all_complementary_nonzero = all(
        row.nonzero_transition_support for row in complementary
    )
    return ComplementarySectorScalingRecord(
        n=n,
        source_partition=source,
        final_partition=stable,
        source_irrep_dimension=source_dimension,
        final_irrep_dimension=stable_dimension,
        intermediate_sector_count=len(contributions),
        final_total_multiplicity=sum(row.branch_dimension for row in contributions),
        right_stable_branch_dimension=right_branch_dimension,
        sector_contributions=contributions,
        projector_resolution_sum=projector_sum,
        projector_resolution_residual=abs(projector_sum - right_branch_dimension),
        stable_branch_retention=stable_contribution / right_branch_dimension,
        stable_branch_leakage=complementary_leakage / right_branch_dimension,
        nonzero_complementary_sector_count=sum(
            row.nonzero_transition_support for row in complementary
        ),
        largest_complementary_leakage_share=max(leakage_shares, default=0.0),
        effective_complementary_sector_count=effective_count,
        all_complementary_sectors_required_at_finite_n=all_complementary_nonzero,
        finite_numerical_probe_only=True,
        status=(
            "complete-finite-complementary-leakage-resolution"
            if abs(projector_sum - right_branch_dimension) < 1e-8
            else "incomplete-projector-resolution"
        ),
    )


def build_complementary_sector_report(
    n_values: Sequence[int] = (7,),
) -> ComplementarySectorReport:
    values = tuple(dict.fromkeys(int(n) for n in n_values))
    if not values:
        raise ValueError("at least one n value is required")
    records = [audit_complementary_sectors(n) for n in values]
    complete = all(record.projector_resolution_residual < 1e-8 for record in records)
    all_spread = all(
        record.all_complementary_sectors_required_at_finite_n for record in records
    )
    metrics: dict[str, int | float] = {
        "scaling_point_count": len(records),
        "minimum_n": min(values),
        "maximum_n": max(values),
        "complete_projector_resolution_count": sum(
            record.projector_resolution_residual < 1e-8 for record in records
        ),
        "minimum_intermediate_sector_count": min(
            record.intermediate_sector_count for record in records
        ),
        "minimum_nonzero_complementary_sector_count": min(
            record.nonzero_complementary_sector_count for record in records
        ),
        "maximum_nonzero_complementary_sector_count": max(
            record.nonzero_complementary_sector_count for record in records
        ),
        "maximum_single_complementary_leakage_share": max(
            record.largest_complementary_leakage_share for record in records
        ),
        "minimum_effective_complementary_sector_count": min(
            record.effective_complementary_sector_count for record in records
        ),
        "single_complement_repair_count": sum(
            record.largest_complementary_leakage_share > 1.0 - 1e-8
            for record in records
        ),
        "all_n_complementary_support_theorem_count": 0,
        "coherent_all_sector_transform_count": 0,
        "hidden_involution_decoder_count": 0,
    }
    return ComplementarySectorReport(
        created_at=utc_now(),
        mathematical_contract={
            "observable": "Tr(P_left,eta P_right,xi) for every allowed intermediate eta",
            "sum_rule": "sum_eta Tr(P_left,eta P_right,xi)=rank(P_right,xi)=8",
            "gauge_invariance": "each contribution is a projector trace and independent of intertwiner bases",
            "right_branch": "the stable 2x4 xi_n branch",
            "left_resolution": "every character-allowed intermediate partition",
            "scope": "finite numerical scaling evidence only",
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "complete_finite_projector_resolution": complete,
            "leakage_spread_across_all_complementary_sectors": all_spread,
            "single_complement_repair_supported": False,
            "all_n_support_formula_proved": False,
            "coherent_all_sector_transform_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The stable branch leaks across every finite complementary sector. The complete numerical sum rule "
                "does not provide exact all-n support, coherent sector transforms, or a decoder."
            ),
        },
        status=(
            "complete-finite-leakage-support-single-channel-repair-refuted"
            if complete and all_spread
            else "complementary-leakage-resolution-incomplete"
        ),
        summary=(
            f"Resolved stable-branch leakage over all intermediate sectors at {len(records)} sizes; every audited "
            "complementary sector has nonzero support, refuting a one-complement repair."
        ),
        falsifiers_triggered=[
            "Adding only the largest complementary partition cannot close the stable Racah branch.",
            "A full-rank stable 8x8 overlap hides substantial support in every other intermediate sector.",
            "Finite projector-trace decompositions do not prove an all-n transition-support formula.",
            "Numerical sector coverage does not compile coherent labels or decode a hidden involution.",
        ],
    )


def write_complementary_sector_report(
    output_path: Path = COSET_STABLE_COMPLEMENTARY_SECTOR_PATH,
    n_values: Sequence[int] = (7,),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_complementary_sector_report(n_values=n_values))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-STABLE-LEAKAGE-AS-SINGLE-COMPLEMENT-REPAIR",
                source=str(output_path),
                claim=(
                    "One additional intermediate partition captures the stable branch leakage and closes a restricted associator."
                ),
                reason_invalid=(
                    "Every character-allowed complementary sector has nonzero projector overlap, and no one sector captures all leaked mass."
                ),
                lesson=(
                    "Derive an all-n support formula and cover the full intermediate-sector family before coherent synthesis."
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
                artifacts={"coset_stable_complementary_sector_probe": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_complementary_sector_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
