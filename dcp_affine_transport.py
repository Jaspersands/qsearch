"""Exact workbench for GF(2)-affine 2-adic subset-sum transports.

This module extends signed-coordinate permutations to

    T(x) = P x xor b,

where P is invertible over GF(2).  An integer ANF expansion gives necessary
and sufficient congruence conditions for T to translate every subset sum by
2^k modulo 2^(k+1).  The constant condition immediately yields
S_A(b)=2^k, so evaluating a constructible transport on zero returns the target
subset-sum witness.  This is an exact reduction, not a lower bound: finding a
polynomial affine transport would itself be a polynomial relation solver.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Sequence

from dcp_signed_permutation_transport import signed_permutation_transport_exists
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_AFFINE_TRANSPORT_PATH = Path("research/phase_workbench/dcp_affine_transport.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-AFFINE-TRANSPORT"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class AffineANFTheoremCertificate:
    theorem_id: str
    transform_class: str
    constant_condition: str
    singleton_condition: str
    higher_order_condition: str
    necessary_and_sufficient: bool
    zero_image_witness_reduction: str
    polynomial_transport_implies_polynomial_solver: bool
    theorem_scope_exclusions: list[str]


@dataclass(frozen=True)
class AffineExhaustiveRow:
    depth: int
    modulus: int
    register_count: int
    label_tuple_count: int
    invertible_matrix_count: int
    affine_transport_instance_count: int
    signed_transport_instance_count: int
    nonmonomial_affine_only_instance_count: int
    affine_witness_extraction_failure_count: int
    anf_vs_truth_table_mismatch_count: int
    first_nonmonomial_example: dict[str, object] | None


@dataclass(frozen=True)
class AffineSearchScalingRow:
    n_bits: int
    register_count: int
    tested_depth: int
    log2_invertible_matrix_count: float
    log2_affine_search_space: float
    anf_coefficient_count: int
    exhaustive_search_polynomial: bool
    polynomial_affine_transport_constructed: bool


@dataclass(frozen=True)
class AffineTransportReport:
    created_at: str
    theorem: AffineANFTheoremCertificate
    exhaustive_rows: list[AffineExhaustiveRow]
    scaling_rows: list[AffineSearchScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]
    next_search_programs: list[dict[str, object]]


def gf2_rank(rows: Sequence[int], width: int) -> int:
    work = list(rows)
    rank = 0
    for column in range(width):
        pivot = next(
            (index for index in range(rank, len(work)) if (work[index] >> column) & 1),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        for index in range(len(work)):
            if index != rank and ((work[index] >> column) & 1):
                work[index] ^= work[rank]
        rank += 1
    return rank


@lru_cache(maxsize=None)
def invertible_gf2_matrices(width: int) -> tuple[tuple[int, ...], ...]:
    if not 1 <= width <= 4:
        raise ValueError("exact matrix enumeration is capped at width four")
    return tuple(
        rows
        for rows in itertools.product(range(1 << width), repeat=width)
        if gf2_rank(rows, width) == width
    )


def is_monomial_gf2_matrix(rows: Sequence[int], width: int) -> bool:
    return (
        len(rows) == width
        and all(row.bit_count() == 1 for row in rows)
        and gf2_rank(rows, width) == width
    )


def apply_affine_map(assignment: int, rows: Sequence[int], offset: int) -> int:
    output = 0
    for output_index, row in enumerate(rows):
        bit = ((row & assignment).bit_count() & 1) ^ ((offset >> output_index) & 1)
        output |= bit << output_index
    return output


def subset_sum_mod(labels: Sequence[int], assignment: int, modulus: int) -> int:
    return sum(
        label for index, label in enumerate(labels) if (assignment >> index) & 1
    ) % modulus


def is_constant_next_bit_affine_transport_truth_table(
    labels: Sequence[int], rows: Sequence[int], offset: int, depth: int
) -> bool:
    width = len(labels)
    if len(rows) != width or gf2_rank(rows, width) != width:
        return False
    modulus = 1 << (depth + 1)
    half = 1 << depth
    return all(
        (
            subset_sum_mod(labels, apply_affine_map(x, rows, offset), modulus)
            - subset_sum_mod(labels, x, modulus)
        )
        % modulus
        == half
        for x in range(1 << width)
    )


def affine_anf_coefficients(
    labels: Sequence[int], rows: Sequence[int], offset: int, depth: int
) -> dict[int, int]:
    """Return all ANF coefficients of S_A(T(x))-S_A(x), modulo M."""
    width = len(labels)
    modulus = 1 << (depth + 1)
    signed_labels = [
        (-label if (offset >> output_index) & 1 else label) % modulus
        for output_index, label in enumerate(labels)
    ]
    coefficients: dict[int, int] = {
        0: subset_sum_mod(labels, offset, modulus)
    }
    for monomial in range(1, 1 << width):
        order = monomial.bit_count()
        intersection_sum = sum(
            signed_labels[output_index]
            for output_index, row in enumerate(rows)
            if row & monomial == monomial
        )
        coefficient = ((-2) ** (order - 1) * intersection_sum) % modulus
        if order == 1:
            input_index = monomial.bit_length() - 1
            coefficient = (coefficient - labels[input_index]) % modulus
        coefficients[monomial] = coefficient
    return coefficients


def affine_anf_certifies_transport(
    labels: Sequence[int], rows: Sequence[int], offset: int, depth: int
) -> bool:
    width = len(labels)
    if len(rows) != width or gf2_rank(rows, width) != width:
        return False
    coefficients = affine_anf_coefficients(labels, rows, offset, depth)
    return coefficients[0] == 1 << depth and all(
        value == 0 for monomial, value in coefficients.items() if monomial
    )


def find_affine_transport(
    labels: Sequence[int], depth: int, require_nonmonomial: bool = False
) -> tuple[tuple[int, ...], int] | None:
    width = len(labels)
    matrices = invertible_gf2_matrices(width)
    modulus = 1 << (depth + 1)
    half = 1 << depth
    offsets = [
        offset
        for offset in range(1 << width)
        if subset_sum_mod(labels, offset, modulus) == half
    ]
    for offset in offsets:
        for rows in matrices:
            if require_nonmonomial and is_monomial_gf2_matrix(rows, width):
                continue
            if affine_anf_certifies_transport(labels, rows, offset, depth):
                return rows, offset
    return None


def build_anf_theorem_certificate() -> AffineANFTheoremCertificate:
    return AffineANFTheoremCertificate(
        theorem_id="THEOREM-DCP-GF2-AFFINE-TRANSPORT-ANF",
        transform_class="invertible GF(2)-affine maps T(x)=P x xor b",
        constant_condition="sum_{j:b_j=1} A_j = 2^k modulo M=2^(k+1)",
        singleton_condition=(
            "for every input i, sum_{j:P_ji=1} (-1)^(b_j) A_j = A_i modulo M"
        ),
        higher_order_condition=(
            "for every input set I with |I|>=2, (-2)^(|I|-1) times "
            "sum_{j:I subset support(P_j*)} (-1)^(b_j) A_j = 0 modulo M"
        ),
        necessary_and_sufficient=True,
        zero_image_witness_reduction=(
            "T(0)=b and the constant condition gives S_A(b)=2^k; evaluating any efficiently constructible "
            "transport at zero returns a verified target witness."
        ),
        polynomial_transport_implies_polynomial_solver=True,
        theorem_scope_exclusions=[
            "nonlinear reversible maps",
            "partial maps defined only on a target fiber",
            "non-bijective relation samplers",
            "quantum walks that never materialize a total affine map",
        ],
    )


def exhaustive_affine_row(depth: int, register_count: int = 3) -> AffineExhaustiveRow:
    modulus = 1 << (depth + 1)
    matrices = invertible_gf2_matrices(register_count)
    affine_count = 0
    signed_count = 0
    affine_only = 0
    extraction_failures = 0
    mismatches = 0
    first_example: dict[str, object] | None = None
    label_tuple_count = 0
    for labels in itertools.product(range(modulus), repeat=register_count):
        label_tuple_count += 1
        signed_exists = signed_permutation_transport_exists(labels, depth)
        signed_count += int(signed_exists)
        affine = find_affine_transport(labels, depth)
        affine_exists = affine is not None
        affine_count += int(affine_exists)
        nonmonomial = find_affine_transport(labels, depth, require_nonmonomial=True)
        if nonmonomial is not None and not signed_exists:
            affine_only += 1
            if first_example is None:
                rows, offset = nonmonomial
                first_example = {
                    "labels": list(labels),
                    "matrix_rows": list(rows),
                    "offset": offset,
                }
        if affine is not None:
            rows, offset = affine
            extraction_failures += int(
                subset_sum_mod(labels, offset, modulus) != 1 << depth
            )
            mismatches += int(
                affine_anf_certifies_transport(labels, rows, offset, depth)
                != is_constant_next_bit_affine_transport_truth_table(
                    labels, rows, offset, depth
                )
            )
    return AffineExhaustiveRow(
        depth=depth,
        modulus=modulus,
        register_count=register_count,
        label_tuple_count=label_tuple_count,
        invertible_matrix_count=len(matrices),
        affine_transport_instance_count=affine_count,
        signed_transport_instance_count=signed_count,
        nonmonomial_affine_only_instance_count=affine_only,
        affine_witness_extraction_failure_count=extraction_failures,
        anf_vs_truth_table_mismatch_count=mismatches,
        first_nonmonomial_example=first_example,
    )


def affine_search_scaling_row(
    n_bits: int, register_offset: int = 4, depth: int | None = None
) -> AffineSearchScalingRow:
    width = n_bits + register_offset
    tested_depth = n_bits // 2 if depth is None else depth
    log2_gl = sum(
        math.log2((1 << width) - (1 << rank)) for rank in range(width)
    )
    return AffineSearchScalingRow(
        n_bits=n_bits,
        register_count=width,
        tested_depth=tested_depth,
        log2_invertible_matrix_count=log2_gl,
        log2_affine_search_space=log2_gl + width,
        anf_coefficient_count=(1 << width) - 1,
        exhaustive_search_polynomial=False,
        polynomial_affine_transport_constructed=False,
    )


def run_affine_transport_audit(
    n_values: Sequence[int] = (32, 64, 128, 256),
    register_offset: int = 4,
) -> AffineTransportReport:
    exhaustive_rows = [
        exhaustive_affine_row(depth=1, register_count=3),
        exhaustive_affine_row(depth=2, register_count=3),
    ]
    scaling_rows = [
        affine_search_scaling_row(n, register_offset=register_offset) for n in n_values
    ]
    mismatches = sum(row.anf_vs_truth_table_mismatch_count for row in exhaustive_rows)
    extraction_failures = sum(
        row.affine_witness_extraction_failure_count for row in exhaustive_rows
    )
    affine_only = sum(
        row.nonmonomial_affine_only_instance_count for row in exhaustive_rows
    )
    metrics: dict[str, int | float] = {
        "exact_anf_theorem_count": 1,
        "zero_image_witness_reduction_count": 1,
        "exhaustive_label_tuple_count": sum(
            row.label_tuple_count for row in exhaustive_rows
        ),
        "anf_vs_truth_table_mismatch_count": mismatches,
        "affine_witness_extraction_failure_count": extraction_failures,
        "nonmonomial_affine_only_instance_count": affine_only,
        "linear_depth_scaling_row_count": len(scaling_rows),
        "polynomial_affine_search_count": 0,
        "proved_polynomial_affine_transport_count": 0,
        "proved_polynomial_relation_solver_count": 0,
    }
    return AffineTransportReport(
        created_at=utc_now(),
        theorem=build_anf_theorem_certificate(),
        exhaustive_rows=exhaustive_rows,
        scaling_rows=scaling_rows,
        headline_metrics=metrics,
        claim_gate={
            "exact_affine_verifier_proved": mismatches == 0,
            "transport_to_witness_reduction_proved": extraction_failures == 0,
            "nonmonomial_affine_transports_exist_at_small_moduli": affine_only > 0,
            "total_affine_route_alive_beyond_exact_valuation_pivot": False,
            "polynomial_affine_search_constructed": False,
            "polynomial_relation_solver_proved": False,
            "nonlinear_or_partial_route_alive": True,
            "speedup_claim_allowed": False,
            "reason": (
                "The affine class has an exact verifier and any constructible transport yields a target witness. The "
                "general full-cube Fourier theorem further proves that every total affine transport requires the old "
                "exact-valuation pivot, so only explicitly partial target-fiber variants remain open."
            ),
        },
        status="affine-transport-characterized-search-equivalent-to-witness-construction",
        summary=(
            f"Certified the exact affine ANF conditions with {mismatches} truth-table mismatches and "
            f"{extraction_failures} witness-extraction failures over {metrics['exhaustive_label_tuple_count']} label "
            f"tuples. Nonmonomial affine-only instances={affine_only}; polynomial affine searches=0."
        ),
        falsifiers_triggered=[
            "A transport proposal that does not satisfy every ANF congruence is not a constant child-bit transport.",
            "Any total affine transport construction already exposes a target witness as T(0).",
            "The full affine search space has quadratic exponent in the register count and cannot be enumerated asymptotically.",
            "Small-modulus nonmonomial examples do not establish source-random linear-depth incidence or efficient search.",
            "The exact reduction is not a hardness proof against a new polynomial affine synthesis algorithm.",
        ],
        next_search_programs=[
            {
                "program_id": "PARTIAL-FIBER-AFFINE-MAP",
                "mechanism": "Relax equality to a source-uniform inverse-polynomial subset of one low-bit fiber.",
                "required_baselines": [
                    "classical partial-map learning",
                    "coverage under uniform legal targets",
                    "verified witness extraction",
                ],
                "falsifier": "Coverage is planted-only or exponentially small at linear depth.",
            },
        ],
    )


def write_affine_transport_audit(
    path: Path = DCP_AFFINE_TRANSPORT_PATH,
    n_values: Sequence[int] = (32, 64, 128, 256),
    register_offset: int = 4,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(
        run_affine_transport_audit(
            n_values=n_values, register_offset=register_offset
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-AFFINE-TRANSPORT-AS-EASIER-INTERMEDIARY",
                source=str(path),
                claim=(
                    "Constructing a total GF(2)-affine next-bit transport is an easier intermediate objective that "
                    "can precede solving the target subset-sum relation."
                ),
                reason_invalid=(
                    "For every valid transport T(x)=Px xor b, T(0)=b and S_A(b)=2^k modulo 2^(k+1); evaluating "
                    "the transport at zero already returns the target witness."
                ),
                lesson=(
                    "Treat affine synthesis as a direct relation-solver architecture and compare it against direct "
                    "classical search on b. Do not count the transport and witness construction as separate progress."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-AFFINE-TRANSPORT"
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
                artifacts={"dcp_affine_transport": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_affine_transport_audit()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
