"""Exact subset-orbit carrier algebra for the wreath-product k-copy frame.

The average k-copy frame has the formal expansion

    B_k = 2^-k sum_{A subseteq [k]} T_A,

where

    T_A = (1/n!) sum_s tensor_{i in A} R(h_s)_i.

Register permutations group the 2^k subsets into k+1 orbit sums

    U_r = sum_{|A|=r} T_A.

This polynomial orbit count is useful only if the resulting carrier algebra
can be transformed efficiently.  It is not a scalar/Krawtchouk algebra:
overlapping T_A fail to commute for nonabelian S_n, and the fully symmetrized
U_2 and U_3 already fail to commute at k=4.  This module computes exact sparse
group-algebra commutators and modular lower bounds on truncated word-algebra
dimension without constructing factorial Hilbert-space matrices.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path
from typing import Any, Iterable

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


SELF_DUAL_WREATH_SUBSET_CARRIER_PATH = Path(
    "research/representation/self_dual_wreath_subset_carrier_algebra.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-SUBSET-CARRIER-ALGEBRA"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]
WreathElement = tuple[Permutation, Permutation, int]
TensorWreathElement = tuple[WreathElement, ...]
SparseElement = dict[TensorWreathElement, int]


@dataclass(frozen=True)
class WreathSubsetCarrierSpec:
    symmetrized_n_values: tuple[int, ...] = (2, 3, 4, 5)
    symmetrized_copy_count: int = 4
    algebra_rank_n: int = 3
    algebra_rank_copy_count: int = 4
    algebra_rank_max_word_depth: int = 3


@dataclass(frozen=True)
class CarrierCommutatorRecord:
    id: str
    n: int
    copy_count: int
    left_operator: str
    right_operator: str
    left_support_size: int
    right_support_size: int
    commutator_support_size: int
    commutator_l2_squared_exact: str
    commutator_l2_squared: float
    commutes: bool
    role: str
    status: str


@dataclass(frozen=True)
class TruncatedAlgebraRankRecord:
    n: int
    copy_count: int
    maximum_word_depth: int
    word_count: int
    modular_rank_lower_bound: int
    maximum_word_support_size: int
    generator_count: int
    scalar_orbit_dimension: int
    exceeds_scalar_orbit_dimension: bool
    status: str


@dataclass(frozen=True)
class SelfDualWreathSubsetCarrierReport:
    created_at: str
    spec: WreathSubsetCarrierSpec
    algebra_definition: dict[str, Any]
    commutator_records: list[CarrierCommutatorRecord]
    truncated_rank_records: list[TruncatedAlgebraRankRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def compose_permutations(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(len(left)))


def inverse_permutation(permutation: Permutation) -> Permutation:
    inverse = [0] * len(permutation)
    for index, image in enumerate(permutation):
        inverse[image] = index
    return tuple(inverse)


def wreath_multiply(left: WreathElement, right: WreathElement) -> WreathElement:
    left_a, left_b, left_swap = left
    right_a, right_b, right_swap = right
    return (
        compose_permutations(left_a, right_b if left_swap else right_a),
        compose_permutations(left_b, right_a if left_swap else right_b),
        left_swap ^ right_swap,
    )


def tensor_wreath_multiply(
    left: TensorWreathElement,
    right: TensorWreathElement,
) -> TensorWreathElement:
    return tuple(
        wreath_multiply(left_item, right_item)
        for left_item, right_item in zip(left, right)
    )


def _add_coefficient(
    target: SparseElement,
    key: TensorWreathElement,
    coefficient: int,
) -> None:
    value = target.get(key, 0) + coefficient
    if value:
        target[key] = value
    elif key in target:
        del target[key]


def sparse_sum(elements: Iterable[SparseElement]) -> SparseElement:
    output: SparseElement = {}
    for element in elements:
        for key, coefficient in element.items():
            _add_coefficient(output, key, coefficient)
    return output


def sparse_product(left: SparseElement, right: SparseElement) -> SparseElement:
    output: SparseElement = {}
    for left_key, left_coefficient in left.items():
        for right_key, right_coefficient in right.items():
            _add_coefficient(
                output,
                tensor_wreath_multiply(left_key, right_key),
                left_coefficient * right_coefficient,
            )
    return output


def sparse_difference(left: SparseElement, right: SparseElement) -> SparseElement:
    return sparse_sum(
        (
            left,
            {key: -coefficient for key, coefficient in right.items()},
        )
    )


def subset_operator_numerator(
    n: int,
    copy_count: int,
    subset: tuple[int, ...],
) -> SparseElement:
    if n < 2:
        raise ValueError("n must be at least two")
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    if any(index < 0 or index >= copy_count for index in subset):
        raise ValueError("subset index out of range")
    subset_set = set(subset)
    identity_permutation = tuple(range(n))
    identity_wreath = (identity_permutation, identity_permutation, 0)
    output: SparseElement = {}
    for permutation in permutations(range(n)):
        bridge = (
            permutation,
            inverse_permutation(permutation),
            1,
        )
        key = tuple(
            bridge if index in subset_set else identity_wreath
            for index in range(copy_count)
        )
        _add_coefficient(output, key, 1)
    return output


def orbit_sum_numerator(
    n: int,
    copy_count: int,
    subset_size: int,
) -> SparseElement:
    if subset_size < 0 or subset_size > copy_count:
        raise ValueError("subset_size out of range")
    return sparse_sum(
        subset_operator_numerator(n, copy_count, subset)
        for subset in combinations(range(copy_count), subset_size)
    )


def _commutator_record(
    identifier: str,
    n: int,
    copy_count: int,
    left_name: str,
    right_name: str,
    left: SparseElement,
    right: SparseElement,
    role: str,
) -> CarrierCommutatorRecord:
    commutator = sparse_difference(
        sparse_product(left, right),
        sparse_product(right, left),
    )
    denominator = math.factorial(n) ** 4
    norm_squared = Fraction(
        sum(coefficient * coefficient for coefficient in commutator.values()),
        denominator,
    )
    commutes = not commutator
    return CarrierCommutatorRecord(
        id=identifier,
        n=n,
        copy_count=copy_count,
        left_operator=left_name,
        right_operator=right_name,
        left_support_size=len(left),
        right_support_size=len(right),
        commutator_support_size=len(commutator),
        commutator_l2_squared_exact=str(norm_squared),
        commutator_l2_squared=float(norm_squared),
        commutes=commutes,
        role=role,
        status=(
            "commuting-control"
            if commutes
            else "exact-noncommutative-carrier-witness"
        ),
    )


def overlapping_subset_commutator(n: int) -> CarrierCommutatorRecord:
    copy_count = 3
    left = subset_operator_numerator(n, copy_count, (0, 1))
    right = subset_operator_numerator(n, copy_count, (1, 2))
    return _commutator_record(
        identifier=f"overlapping-subsets-n{n}",
        n=n,
        copy_count=copy_count,
        left_name="T_{0,1}",
        right_name="T_{1,2}",
        left=left,
        right=right,
        role="overlapping-subset carrier control",
    )


def disjoint_subset_commutator(n: int) -> CarrierCommutatorRecord:
    copy_count = 4
    left = subset_operator_numerator(n, copy_count, (0, 1))
    right = subset_operator_numerator(n, copy_count, (2, 3))
    return _commutator_record(
        identifier=f"disjoint-subsets-n{n}",
        n=n,
        copy_count=copy_count,
        left_name="T_{0,1}",
        right_name="T_{2,3}",
        left=left,
        right=right,
        role="disjoint-register commuting control",
    )


def symmetrized_orbit_commutator(
    n: int,
    copy_count: int = 4,
    left_size: int = 2,
    right_size: int = 3,
) -> CarrierCommutatorRecord:
    left = orbit_sum_numerator(n, copy_count, left_size)
    right = orbit_sum_numerator(n, copy_count, right_size)
    return _commutator_record(
        identifier=(
            f"symmetrized-orbits-n{n}-k{copy_count}-r{left_size}-r{right_size}"
        ),
        n=n,
        copy_count=copy_count,
        left_name=f"U_{left_size}",
        right_name=f"U_{right_size}",
        left=left,
        right=right,
        role="register-permutation-symmetrized carrier test",
    )


def _modular_rank(
    elements: Iterable[SparseElement],
    prime: int,
) -> int:
    basis: dict[TensorWreathElement, dict[TensorWreathElement, int]] = {}
    rank = 0
    for element in elements:
        vector = {
            key: coefficient % prime
            for key, coefficient in element.items()
            if coefficient % prime
        }
        while vector:
            pivot = min(vector)
            pivot_value = vector[pivot]
            if pivot not in basis:
                inverse = pow(pivot_value, -1, prime)
                normalized = {
                    key: (value * inverse) % prime
                    for key, value in vector.items()
                    if value % prime
                }
                basis[pivot] = normalized
                rank += 1
                break
            pivot_row = basis[pivot]
            for key, value in pivot_row.items():
                reduced = (
                    vector.get(key, 0) - pivot_value * value
                ) % prime
                if reduced:
                    vector[key] = reduced
                elif key in vector:
                    del vector[key]
    return rank


def truncated_orbit_algebra_ranks(
    n: int = 3,
    copy_count: int = 4,
    maximum_word_depth: int = 3,
) -> list[TruncatedAlgebraRankRecord]:
    if maximum_word_depth < 1:
        raise ValueError("maximum_word_depth must be positive")
    generators = {
        subset_size: orbit_sum_numerator(n, copy_count, subset_size)
        for subset_size in range(1, copy_count + 1)
    }
    identity_permutation = tuple(range(n))
    identity_wreath = (identity_permutation, identity_permutation, 0)
    identity = {tuple(identity_wreath for _ in range(copy_count)): 1}
    words: dict[tuple[int, ...], SparseElement] = {(): identity}
    records: list[TruncatedAlgebraRankRecord] = []
    for depth in range(1, maximum_word_depth + 1):
        for word in product(range(1, copy_count + 1), repeat=depth):
            words[word] = sparse_product(
                words[word[:-1]],
                generators[word[-1]],
            )
        ordered = [
            element
            for _, element in sorted(
                words.items(),
                key=lambda item: (len(item[0]), item[0]),
            )
        ]
        ranks = [
            _modular_rank(ordered, prime)
            for prime in (1_000_003, 1_000_033)
        ]
        rank_lower_bound = max(ranks)
        scalar_dimension = copy_count + 1
        records.append(
            TruncatedAlgebraRankRecord(
                n=n,
                copy_count=copy_count,
                maximum_word_depth=depth,
                word_count=len(words),
                modular_rank_lower_bound=rank_lower_bound,
                maximum_word_support_size=max(
                    (len(element) for element in ordered),
                    default=0,
                ),
                generator_count=len(generators),
                scalar_orbit_dimension=scalar_dimension,
                exceeds_scalar_orbit_dimension=rank_lower_bound > scalar_dimension,
                status=(
                    "noncommutative-word-algebra-growth"
                    if rank_lower_bound > scalar_dimension
                    else "bounded-depth-scalar-dimension-control"
                ),
            )
        )
    return records


def run_self_dual_wreath_subset_carrier_algebra(
    spec: WreathSubsetCarrierSpec = WreathSubsetCarrierSpec(),
) -> SelfDualWreathSubsetCarrierReport:
    commutators = [
        overlapping_subset_commutator(2),
        overlapping_subset_commutator(3),
        disjoint_subset_commutator(3),
        symmetrized_orbit_commutator(3, copy_count=3),
        *[
            symmetrized_orbit_commutator(
                n,
                copy_count=spec.symmetrized_copy_count,
            )
            for n in spec.symmetrized_n_values
        ],
    ]
    rank_records = truncated_orbit_algebra_ranks(
        n=spec.algebra_rank_n,
        copy_count=spec.algebra_rank_copy_count,
        maximum_word_depth=spec.algebra_rank_max_word_depth,
    )
    symmetrized_noncommuting = [
        record
        for record in commutators
        if record.left_operator.startswith("U_") and not record.commutes
    ]
    metrics: dict[str, int | float] = {
        "commutator_record_count": len(commutators),
        "commuting_control_count": sum(record.commutes for record in commutators),
        "overlapping_subset_noncommutation_count": sum(
            record.role == "overlapping-subset carrier control"
            and not record.commutes
            for record in commutators
        ),
        "symmetrized_orbit_noncommutation_count": len(
            symmetrized_noncommuting
        ),
        "first_symmetrized_noncommuting_copy_count": min(
            (record.copy_count for record in symmetrized_noncommuting),
            default=0,
        ),
        "maximum_commutator_support_size": max(
            (record.commutator_support_size for record in commutators),
            default=0,
        ),
        "truncated_rank_record_count": len(rank_records),
        "maximum_truncated_word_depth": max(
            (record.maximum_word_depth for record in rank_records),
            default=0,
        ),
        "maximum_truncated_algebra_rank_lower_bound": max(
            (record.modular_rank_lower_bound for record in rank_records),
            default=0,
        ),
        "maximum_truncated_word_support_size": max(
            (record.maximum_word_support_size for record in rank_records),
            default=0,
        ),
        "scalar_krawtchouk_preconditioner_count": 0,
        "uniform_noncommutative_carrier_block_transform_count": 0,
        "polynomial_structured_frame_preconditioner_count": 0,
        "polynomial_frame_inverse_count": 0,
        "carrier_sensitive_povm_circuit_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    return SelfDualWreathSubsetCarrierReport(
        created_at=utc_now(),
        spec=spec,
        algebra_definition={
            "subset_operator": (
                "T_A=(1/n!) sum_s tensor_{i in A} R(h_s)_i"
            ),
            "orbit_sum": "U_r=sum_{|A|=r} T_A",
            "average_frame": "B_k=2^-k sum_{r=0}^k U_r",
            "symmetries": (
                "Each U_r commutes with diagonal W_n conjugation and register "
                "permutations S_k."
            ),
            "noncommutative_warning": (
                "Belonging to the joint symmetry commutant does not imply "
                "mutual commutativity when carrier multiplicities are present."
            ),
            "normalization": (
                "Sparse numerators omit one factor 1/n! per T_A; commutator "
                "L2 norms restore denominator (n!)^4."
            ),
            "rank_semantics": (
                "Word-algebra ranks are certified lower bounds over two large "
                "prime fields, not exact characteristic-zero closure dimensions."
            ),
        },
        commutator_records=commutators,
        truncated_rank_records=rank_records,
        headline_metrics=metrics,
        claim_gate={
            "register_subset_orbit_count_is_polynomial": True,
            "overlapping_subset_operators_commute": False,
            "symmetrized_subset_orbit_sums_commute_uniformly": False,
            "scalar_krawtchouk_transform_diagonalizes_carrier_frame": False,
            "noncommutative_carrier_algebra_growth_observed": True,
            "uniform_noncommutative_carrier_block_transform_proved": False,
            "polynomial_structured_frame_preconditioner_proved": False,
            "polynomial_frame_inverse_proved": False,
            "carrier_sensitive_povm_circuit_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Register symmetry compresses formal subset labels to k+1 "
                "orbit sums, but their carrier algebra is already "
                "noncommutative at k=4 and its truncated word dimension grows "
                "past the scalar orbit dimension. A noncommutative block "
                "transform and preconditioner remain missing."
            ),
        },
        status="subset-orbit-compressed-carrier-algebra-noncommutative",
        summary=(
            f"Computed {len(commutators)} exact sparse commutator controls and "
            f"found {len(symmetrized_noncommuting)} noncommuting symmetrized "
            f"orbit rows, first at k="
            f"{metrics['first_symmetrized_noncommuting_copy_count']}. The "
            f"depth-{metrics['maximum_truncated_word_depth']} modular algebra "
            f"rank lower bound is "
            f"{metrics['maximum_truncated_algebra_rank_lower_bound']}."
        ),
        falsifiers_triggered=[
            "Disjoint-register subset operators commute, validating the sparse multiplication control.",
            "Overlapping subset operators fail to commute as soon as the base symmetric group is nonabelian.",
            "Register-symmetrized U_2 and U_3 commute at k=3 but fail at k=4.",
            "The truncated U_r word algebra exceeds the k+1 scalar orbit dimension by depth two.",
            "A Hamming-weight/Krawtchouk transform cannot by itself diagonalize the carrier frame.",
        ],
    )


def write_self_dual_wreath_subset_carrier_algebra(
    path: Path = SELF_DUAL_WREATH_SUBSET_CARRIER_PATH,
    spec: WreathSubsetCarrierSpec = WreathSubsetCarrierSpec(),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_self_dual_wreath_subset_carrier_algebra(spec=spec))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-CODE-SELF-DUAL-WREATH-SCALAR-SUBSET-ORBIT-PRECONDITIONER",
                source=str(path),
                claim=(
                    "Grouping the 2^k subset terms by Hamming weight produces "
                    "a commutative k+1-dimensional carrier algebra."
                ),
                reason_invalid=(
                    "The exact symmetrized orbit sums U_2 and U_3 have a "
                    "nonzero commutator at k=4, and the truncated word algebra "
                    "grows beyond k+1 dimensions."
                ),
                lesson=(
                    "Use register symmetry for compression, but construct a "
                    "noncommutative multiplicity-block transform and "
                    "representation-specific preconditioner."
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
                artifacts={"self_dual_wreath_subset_carrier_algebra": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_self_dual_wreath_subset_carrier_algebra()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
