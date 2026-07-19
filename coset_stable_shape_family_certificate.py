"""Exact nine-shape support theorem for the stable Racah final sector.

For W_n=(n-2,2) and xi_n=(n-3,2,1), the xi_n-isotypic component of
W_n^tensor3 decomposes through nine padded intermediate partition shapes.
This module reconstructs each bounded-degree irreducible character polynomial
from a full-rank exact witness system and applies exact factorial moments of
cycle counts to prove both Kronecker multiplicities.

The character-polynomial theorem guarantees that the padded irreducible
character indexed by tail lambda is a weighted-degree |lambda| polynomial for
n>=|lambda|+lambda_1.  The product moments used here have weighted degree at
most nine, so the multiplicity formulas hold for every n>=9.  Direct exact
characters close n=8.

This proves a bounded sector search space, not coherent labels, spectral gaps,
Racah synthesis, or hidden-involution decoding for those sectors.
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path

import sympy as sp

from representation_obstruction import integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import kronecker_coefficient, symmetric_character


COSET_STABLE_SHAPE_FAMILY_PATH = Path(
    "research/representation/coset_stable_shape_family_certificate.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-STABLE-SHAPE-FAMILY-CERTIFICATE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

STABLE_TAILS = (
    (1,),
    (2,),
    (1, 1),
    (3,),
    (2, 1),
    (1, 1, 1),
    (4,),
    (3, 1),
    (2, 2),
)
SOURCE_TAIL = (2,)
FINAL_TAIL = (2, 1)
X = sp.symbols("X1:5")


@dataclass(frozen=True)
class StableShapeMultiplicityRecord:
    tail: tuple[int, ...]
    padded_partition: str
    tail_size: int
    character_polynomial_threshold: int
    character_polynomial_basis_dimension: int
    reconstruction_witness_rank: int
    exact_verification_row_count: int
    character_polynomial: str
    first_stage_multiplicity: int
    second_stage_multiplicity: int
    branch_dimension: int
    n8_endpoint_first_stage_multiplicity: int
    n8_endpoint_second_stage_multiplicity: int
    all_n_at_least_9_formula_verified: bool
    coherent_second_stage_label_proved: bool
    normalized_second_stage_gap_proved: bool


@dataclass(frozen=True)
class StableShapeFamilyCertificate:
    created_at: str
    theorem: dict[str, object]
    character_polynomial_contract: dict[str, object]
    shape_records: list[StableShapeMultiplicityRecord]
    endpoint_certificate: dict[str, object]
    literature_scope: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def padded_partition(n: int, tail: tuple[int, ...]) -> tuple[int, ...]:
    tail_size = sum(tail)
    first_row = n - tail_size
    if first_row < tail[0]:
        raise ValueError("n is below the padded-partition stability threshold")
    return (first_row, *tail)


def weighted_exponents(maximum_weight: int) -> tuple[tuple[int, ...], ...]:
    rows: list[tuple[int, ...]] = []

    def visit(cycle_length: int, remaining: int, prefix: list[int]) -> None:
        if cycle_length > maximum_weight:
            rows.append(tuple(prefix))
            return
        for exponent in range(remaining // cycle_length + 1):
            visit(
                cycle_length + 1,
                remaining - cycle_length * exponent,
                [*prefix, exponent],
            )

    visit(1, maximum_weight, [])
    return tuple(rows)


def _cycle_count_features(
    cycle_type: tuple[int, ...],
    exponents: tuple[tuple[int, ...], ...],
) -> list[int]:
    counts = {length: cycle_type.count(length) for length in range(1, 5)}
    return [
        int(
            sp.prod(
                counts.get(index, 0) ** exponent
                for index, exponent in enumerate(row, 1)
            )
        )
        for row in exponents
    ]


@lru_cache(maxsize=None)
def reconstruct_character_polynomial(
    tail: tuple[int, ...],
) -> tuple[sp.Expr, dict[str, object]]:
    tail_size = sum(tail)
    threshold = tail_size + tail[0]
    exponents = weighted_exponents(tail_size)
    witness_rows: list[list[int]] = []
    witness_values: list[int] = []
    witness_labels: list[dict[str, object]] = []
    rank = 0
    for n in range(threshold, threshold + 7):
        partition = padded_partition(n, tail)
        for cycle_type in integer_partitions(n):
            row = _cycle_count_features(cycle_type, exponents)
            proposed_rank = sp.Matrix([*witness_rows, row]).rank()
            if proposed_rank == rank:
                continue
            witness_rows.append(row)
            witness_values.append(symmetric_character(partition, cycle_type))
            witness_labels.append({"n": n, "cycle_type": list(cycle_type)})
            rank = proposed_rank
            if rank == len(exponents):
                break
        if rank == len(exponents):
            break
    if rank != len(exponents):
        raise ArithmeticError("character-polynomial witness system is rank deficient")
    coefficients = sp.Matrix(witness_rows).inv() * sp.Matrix(witness_values)
    variables = X[:tail_size]
    polynomial = sp.expand(
        sum(
            coefficient
            * sp.prod(
                variable**exponent
                for variable, exponent in zip(variables, exponent_row)
            )
            for coefficient, exponent_row in zip(coefficients, exponents)
        )
    )
    verification_count = 0
    for n in range(threshold, max(14, threshold + 6)):
        partition = padded_partition(n, tail)
        for cycle_type in integer_partitions(n):
            substitutions = {
                X[index - 1]: cycle_type.count(index)
                for index in range(1, tail_size + 1)
            }
            observed = sp.expand(polynomial).subs(substitutions)
            expected = symmetric_character(partition, cycle_type)
            if observed != expected:
                raise ArithmeticError(
                    f"character polynomial failed at {partition}, {cycle_type}"
                )
            verification_count += 1
    return polynomial, {
        "tail_size": tail_size,
        "threshold": threshold,
        "basis_dimension": len(exponents),
        "witness_rank": rank,
        "witness_rows": witness_labels,
        "verification_row_count": verification_count,
    }


def _stirling_second(power: int, falling_degree: int) -> int:
    if power == falling_degree == 0:
        return 1
    if power == 0 or falling_degree == 0 or falling_degree > power:
        return 0
    table = [[0] * (falling_degree + 1) for _ in range(power + 1)]
    table[0][0] = 1
    for row in range(1, power + 1):
        for column in range(1, min(row, falling_degree) + 1):
            table[row][column] = (
                table[row - 1][column - 1]
                + column * table[row - 1][column]
            )
    return table[power][falling_degree]


def factorial_cycle_moment(polynomial: sp.Expr) -> sp.Expr:
    """Exact uniform-permutation expectation in the stable support range."""
    total = sp.Integer(0)
    for powers, coefficient in sp.Poly(sp.expand(polynomial), *X).terms():
        term = coefficient
        for cycle_length, power in enumerate(powers, 1):
            term *= sum(
                _stirling_second(power, falling_degree)
                * sp.Rational(1, cycle_length) ** falling_degree
                for falling_degree in range(power + 1)
            )
        total += term
    return sp.simplify(total)


def _partition_formula(tail: tuple[int, ...]) -> str:
    tail_text = ",".join(str(value) for value in tail)
    return f"(n-{sum(tail)},{tail_text})"


@lru_cache(maxsize=1)
def build_stable_shape_family_certificate() -> StableShapeFamilyCertificate:
    polynomials: dict[tuple[int, ...], sp.Expr] = {}
    certificates: dict[tuple[int, ...], dict[str, object]] = {}
    for tail in STABLE_TAILS:
        polynomial, certificate = reconstruct_character_polynomial(tail)
        polynomials[tail] = polynomial
        certificates[tail] = certificate

    source_character = polynomials[SOURCE_TAIL]
    final_character = polynomials[FINAL_TAIL]
    records: list[StableShapeMultiplicityRecord] = []
    n8_channels: set[tuple[int, ...]] = set()
    source_n8 = padded_partition(8, SOURCE_TAIL)
    final_n8 = padded_partition(8, FINAL_TAIL)
    for tail in STABLE_TAILS:
        character = polynomials[tail]
        first = int(factorial_cycle_moment(source_character**2 * character))
        second = int(
            factorial_cycle_moment(character * source_character * final_character)
        )
        endpoint = padded_partition(8, tail)
        endpoint_first = kronecker_coefficient(source_n8, source_n8, endpoint)
        endpoint_second = kronecker_coefficient(endpoint, source_n8, final_n8)
        if endpoint_first and endpoint_second:
            n8_channels.add(endpoint)
        certificate = certificates[tail]
        records.append(
            StableShapeMultiplicityRecord(
                tail=tail,
                padded_partition=_partition_formula(tail),
                tail_size=sum(tail),
                character_polynomial_threshold=int(certificate["threshold"]),
                character_polynomial_basis_dimension=int(
                    certificate["basis_dimension"]
                ),
                reconstruction_witness_rank=int(certificate["witness_rank"]),
                exact_verification_row_count=int(
                    certificate["verification_row_count"]
                ),
                character_polynomial=str(sp.factor(character)),
                first_stage_multiplicity=first,
                second_stage_multiplicity=second,
                branch_dimension=first * second,
                n8_endpoint_first_stage_multiplicity=endpoint_first,
                n8_endpoint_second_stage_multiplicity=endpoint_second,
                all_n_at_least_9_formula_verified=bool(first and second),
                coherent_second_stage_label_proved=tail == FINAL_TAIL,
                normalized_second_stage_gap_proved=tail == FINAL_TAIL,
            )
        )

    expected_multiplicities = {
        (1,): (1, 1),
        (2,): (2, 2),
        (1, 1): (1, 2),
        (3,): (1, 2),
        (2, 1): (2, 4),
        (1, 1, 1): (1, 2),
        (4,): (1, 1),
        (3, 1): (1, 3),
        (2, 2): (1, 2),
    }
    formulas_verified = all(
        (record.first_stage_multiplicity, record.second_stage_multiplicity)
        == expected_multiplicities[record.tail]
        for record in records
    )
    endpoint_verified = all(
        (
            record.n8_endpoint_first_stage_multiplicity,
            record.n8_endpoint_second_stage_multiplicity,
        )
        == expected_multiplicities[record.tail]
        for record in records
    )
    total_multiplicity = sum(record.branch_dimension for record in records)
    direct_total_multiplicity = int(
        factorial_cycle_moment(source_character**3 * final_character)
    )
    all_n_exhaustion_verified = (
        total_multiplicity == direct_total_multiplicity == 25
    )
    direct_n8_channels = {
        intermediate
        for intermediate in integer_partitions(8)
        if kronecker_coefficient(source_n8, source_n8, intermediate)
        and kronecker_coefficient(intermediate, source_n8, final_n8)
    }
    direct_n8_total_multiplicity = sum(
        kronecker_coefficient(source_n8, source_n8, intermediate)
        * kronecker_coefficient(intermediate, source_n8, final_n8)
        for intermediate in direct_n8_channels
    )
    endpoint_exhaustion_verified = (
        n8_channels == direct_n8_channels
        and direct_n8_total_multiplicity == total_multiplicity
    )
    theorem_proved = (
        formulas_verified
        and endpoint_verified
        and all_n_exhaustion_verified
        and endpoint_exhaustion_verified
    )
    metrics: dict[str, int | float] = {
        "exact_stable_shape_family_theorem_count": int(theorem_proved),
        "stable_intermediate_shape_count": len(records),
        "exact_character_polynomial_count": len(records),
        "all_n_multiplicity_formula_count": sum(
            record.all_n_at_least_9_formula_verified for record in records
        ),
        "n8_endpoint_verified_shape_count": sum(
            (
                record.n8_endpoint_first_stage_multiplicity,
                record.n8_endpoint_second_stage_multiplicity,
            )
            == expected_multiplicities[record.tail]
            for record in records
        ),
        "stable_final_total_multiplicity": total_multiplicity,
        "direct_triple_character_moment_multiplicity": direct_total_multiplicity,
        "all_n_sector_exhaustion_theorem_count": int(all_n_exhaustion_verified),
        "maximum_first_stage_multiplicity": max(
            record.first_stage_multiplicity for record in records
        ),
        "maximum_second_stage_multiplicity": max(
            record.second_stage_multiplicity for record in records
        ),
        "nontrivial_second_stage_shape_count": sum(
            record.second_stage_multiplicity > 1 for record in records
        ),
        "coherent_gapped_second_stage_shape_count": sum(
            record.coherent_second_stage_label_proved
            and record.normalized_second_stage_gap_proved
            for record in records
        ),
        "unresolved_coherent_second_stage_shape_count": sum(
            record.second_stage_multiplicity > 1
            and not record.coherent_second_stage_label_proved
            for record in records
        ),
        "coherent_all_sector_transform_count": 0,
        "overlapping_racah_associator_count": 0,
        "hidden_involution_decoder_count": 0,
    }
    return StableShapeFamilyCertificate(
        created_at=utc_now(),
        theorem={
            "range": "every integer n>=9, with n=8 closed by exact endpoint characters",
            "source": "W_n=(n-2,2)",
            "final": "xi_n=(n-3,2,1)",
            "intermediate_tails": [list(tail) for tail in STABLE_TAILS],
            "multiplicity_pairs": {
                str(tail): list(expected_multiplicities[tail])
                for tail in STABLE_TAILS
            },
            "final_total_multiplicity": total_multiplicity,
            "statement": (
                "Exactly nine padded intermediate shapes occur in the final-xi_n component of W_n^tensor3, with "
                "the displayed first/second Kronecker multiplicities and total multiplicity 25."
            ),
            "proved": theorem_proved,
        },
        character_polynomial_contract={
            "basis": "ordinary monomials in X_i with weighted degree sum(i*a_i)<=tail size",
            "existence_theorem_threshold": "n>=tail size + largest tail row",
            "reconstruction": "full-rank exact character-value witness system",
            "moment_identity": "E[product_i (X_i)_(a_i)]=product_i i^(-a_i) when total support<=n",
            "exhaustion_identity": (
                "sum_eta g(W,W,eta)g(eta,W,xi)=<chi_W^3,chi_xi>=25; the nine displayed positive terms already sum to 25"
            ),
            "maximum_product_weight": 9,
            "all_n_moment_threshold": 9,
            "total_exact_verification_rows": sum(
                record.exact_verification_row_count for record in records
            ),
        },
        shape_records=records,
        endpoint_certificate={
            "n": 8,
            "source_partition": list(source_n8),
            "final_partition": list(final_n8),
            "distinct_intermediate_partition_count": len(n8_channels),
            "all_multiplicity_pairs_match": endpoint_verified,
            "direct_all_partition_channel_count": len(direct_n8_channels),
            "direct_total_multiplicity": direct_n8_total_multiplicity,
            "selected_shapes_exhaust_all_channels": endpoint_exhaustion_verified,
        },
        literature_scope=[
            {
                "id": "church-ellenberg-farb-fi-modules-2015",
                "url": "https://arxiv.org/abs/1204.4533",
                "role": "bounded-degree character polynomials and stable padded S_n representations",
            },
            {
                "id": "macdonald-symmetric-functions-1995",
                "url": "https://global.oup.com/academic/product/symmetric-functions-and-hall-polynomials-9780198504504",
                "role": "symmetric-group characters and cycle-index inner products",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "exact_bounded_stable_sector_family_proved": theorem_proved,
            "all_required_second_stage_labels_coherently_implemented": False,
            "all_required_normalized_gaps_proved": False,
            "overlapping_racah_associator_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The theorem bounds the relevant sector family exactly, but six nontrivial second-stage shape "
                "families still lack coherent gapped labels; no associator or decoder is constructed."
            ),
        },
        status=(
            "exact-nine-shape-family-proved-six-label-families-open"
            if theorem_proved
            else "stable-shape-family-certificate-failed"
        ),
        summary=(
            "Proved an exact nine-shape intermediate family with total final multiplicity 25 for n>=9 and exact n=8 endpoint; "
            "six nontrivial second-stage label families remain open."
            if theorem_proved
            else "Character-polynomial multiplicities or the n=8 endpoint failed."
        ),
        falsifiers_triggered=[
            "The stable final sector does not require an unbounded number of intermediate partition shapes.",
            "A bounded nine-shape list is not a coherent all-sector transform.",
            "Only one of seven nontrivial second-stage multiplicity shapes currently has a coherent normalized-gap certificate.",
            "Exact sector multiplicities do not imply hidden-involution information or quantum advantage.",
        ],
    )


def write_stable_shape_family_certificate(
    output_path: Path = COSET_STABLE_SHAPE_FAMILY_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_stable_shape_family_certificate())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-NINE-STABLE-SHAPES-AS-COHERENT-RACAH-TRANSFORM",
                source=str(output_path),
                claim=(
                    "An exact constant-size list of stable intermediate shapes supplies a coherent Racah transform and decoder."
                ),
                reason_invalid=(
                    "Six nontrivial second-stage multiplicity families still lack coherent normalized-gap labels, and transitions are not synthesized."
                ),
                lesson=(
                    "Use the theorem to bound operator synthesis to nine shapes, then prove every label/gap and transition primitive explicitly."
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
                artifacts={"coset_stable_shape_family_certificate": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_stable_shape_family_certificate()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
