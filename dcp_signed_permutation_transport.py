"""Exact classification of signed-permutation 2-adic fiber transports.

Consider total Boolean-cube bijections

    T(x)_j = x_{pi(j)} xor b_j.

For modular subset sum S_A(x)=sum_j A_j x_j modulo M=2^(k+1), this
module classifies when S_A(T(x))-S_A(x) is the constant M/2 for every x.
The class looks substantially broader than a coordinate flip, but it is not:
such a transport exists if and only if some A_j equals M/2 modulo M.  Hence
the whole class has exactly the reach of the v_2(A_j)=k pivot and occurs with
probability at most m/M for independent uniform labels.

The theorem does not cover general GF(2)-affine maps, nonlinear arithmetic
maps, partial transports, or quantum walks on a fiber.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_SIGNED_PERMUTATION_TRANSPORT_PATH = Path(
    "research/phase_workbench/dcp_signed_permutation_transport.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SIGNED-PERMUTATION-TRANSPORT"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class SignedPermutationTheoremCertificate:
    theorem_id: str
    transform_class: str
    necessary_and_sufficient_condition: str
    coefficient_condition: str
    constant_term_condition: str
    orbit_argument: str
    converse_construction: str
    exact_classification_proved: bool
    excluded_transform_classes: list[str]


@dataclass(frozen=True)
class ExhaustiveClassificationRow:
    depth: int
    modulus: int
    register_count: int
    label_tuple_count: int
    complement_mask_count: int
    signed_balance_transport_count: int
    pivot_condition_count: int
    mismatch_count: int


@dataclass(frozen=True)
class SignedPermutationScalingRow:
    n_bits: int
    register_count: int
    tested_depth: int
    exact_transport_probability: float
    union_bound_probability: float
    inverse_polynomial_threshold: float
    exponentially_small_at_linear_depth: bool
    expected_transport_count: float


@dataclass(frozen=True)
class SignedPermutationTransportReport:
    created_at: str
    theorem: SignedPermutationTheoremCertificate
    exhaustive_rows: list[ExhaustiveClassificationRow]
    scaling_rows: list[SignedPermutationScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def apply_signed_permutation(
    assignment: int,
    permutation: Sequence[int],
    complement_mask: int,
) -> int:
    """Apply T(x)_j=x_{pi(j)} xor b_j using output-index convention."""
    width = len(permutation)
    if sorted(permutation) != list(range(width)):
        raise ValueError("permutation must contain every coordinate exactly once")
    output = 0
    for output_index, input_index in enumerate(permutation):
        bit = ((assignment >> input_index) & 1) ^ (
            (complement_mask >> output_index) & 1
        )
        output |= bit << output_index
    return output


def subset_sum_mod(labels: Sequence[int], assignment: int, modulus: int) -> int:
    return sum(
        label for index, label in enumerate(labels) if (assignment >> index) & 1
    ) % modulus


def is_constant_next_bit_transport(
    labels: Sequence[int],
    permutation: Sequence[int],
    complement_mask: int,
    depth: int,
) -> bool:
    modulus = 1 << (depth + 1)
    target_delta = 1 << depth
    return all(
        (
            subset_sum_mod(
                labels,
                apply_signed_permutation(assignment, permutation, complement_mask),
                modulus,
            )
            - subset_sum_mod(labels, assignment, modulus)
        )
        % modulus
        == target_delta
        for assignment in range(1 << len(labels))
    )


def signed_multiset_condition(
    labels: Sequence[int], complement_mask: int, depth: int
) -> bool:
    """Whether some permutation can restore all linear coefficients."""
    modulus = 1 << (depth + 1)
    original = Counter(label % modulus for label in labels)
    signed = Counter(
        ((-label if (complement_mask >> index) & 1 else label) % modulus)
        for index, label in enumerate(labels)
    )
    return original == signed


def complement_constant(labels: Sequence[int], complement_mask: int, depth: int) -> int:
    modulus = 1 << (depth + 1)
    return sum(
        label
        for index, label in enumerate(labels)
        if (complement_mask >> index) & 1
    ) % modulus


def mask_certifies_some_signed_permutation_transport(
    labels: Sequence[int], complement_mask: int, depth: int
) -> bool:
    return signed_multiset_condition(labels, complement_mask, depth) and (
        complement_constant(labels, complement_mask, depth) == 1 << depth
    )


def signed_permutation_transport_exists(labels: Sequence[int], depth: int) -> bool:
    """The exact closed-form classification."""
    modulus = 1 << (depth + 1)
    half = 1 << depth
    return any(label % modulus == half for label in labels)


def exhaustive_signed_balance_transport_exists(
    labels: Sequence[int], depth: int
) -> bool:
    """Enumerate complement masks independently of the closed form."""
    return any(
        mask_certifies_some_signed_permutation_transport(labels, mask, depth)
        for mask in range(1 << len(labels))
    )


def construct_pivot_transport(
    labels: Sequence[int], depth: int
) -> tuple[tuple[int, ...], int] | None:
    modulus = 1 << (depth + 1)
    half = 1 << depth
    for index, label in enumerate(labels):
        if label % modulus == half:
            return tuple(range(len(labels))), 1 << index
    return None


def build_theorem_certificate() -> SignedPermutationTheoremCertificate:
    return SignedPermutationTheoremCertificate(
        theorem_id="THEOREM-DCP-SIGNED-PERMUTATION-COLLAPSE",
        transform_class="total maps T(x)_j=x_{pi(j)} xor b_j on the Boolean cube",
        necessary_and_sufficient_condition=(
            "There exists j with A_j=2^k modulo 2^(k+1), equivalently v_2(A_j)=k."
        ),
        coefficient_condition=(
            "Writing B={j:b_j=1}, constancy for all x requires the signed multiset "
            "{(-1)^(b_j) A_j}_j to equal {A_j}_j modulo 2^(k+1)."
        ),
        constant_term_condition=(
            "The translation is sum_{j in B} A_j and must equal 2^k modulo 2^(k+1)."
        ),
        orbit_argument=(
            "On every non-self-inverse sign orbit {a,-a}, multiset balance forces equal selected counts, "
            "whose contribution cancels. The only self-inverse residues are 0 and 2^k; therefore the "
            "constant is 2^k exactly when B contains an odd number of labels congruent to 2^k."
        ),
        converse_construction=(
            "If A_j=2^k, complement coordinate j and use the identity permutation. Since -A_j=A_j "
            "modulo 2^(k+1), every assignment is translated by exactly 2^k."
        ),
        exact_classification_proved=True,
        excluded_transform_classes=[
            "general GF(2)-affine maps with coordinate mixing",
            "nonlinear or arithmetic global bijections",
            "partial transports defined only on a subset of a fiber",
            "quantum walks and non-bijective relation samplers",
        ],
    )


def exhaustive_classification_row(
    depth: int, register_count: int
) -> ExhaustiveClassificationRow:
    modulus = 1 << (depth + 1)
    if modulus**register_count > 100_000:
        raise ValueError("exhaustive label audit is capped at 100,000 tuples")
    transport_count = 0
    pivot_count = 0
    mismatches = 0
    label_tuple_count = 0
    for labels in itertools.product(range(modulus), repeat=register_count):
        label_tuple_count += 1
        brute = exhaustive_signed_balance_transport_exists(labels, depth)
        classified = signed_permutation_transport_exists(labels, depth)
        transport_count += int(brute)
        pivot_count += int(classified)
        mismatches += int(brute != classified)
    return ExhaustiveClassificationRow(
        depth=depth,
        modulus=modulus,
        register_count=register_count,
        label_tuple_count=label_tuple_count,
        complement_mask_count=1 << register_count,
        signed_balance_transport_count=transport_count,
        pivot_condition_count=pivot_count,
        mismatch_count=mismatches,
    )


def scaling_row(
    n_bits: int, register_offset: int = 4, depth: int | None = None
) -> SignedPermutationScalingRow:
    register_count = n_bits + register_offset
    tested_depth = n_bits // 2 if depth is None else depth
    modulus = 1 << (tested_depth + 1)
    exact_probability = 1.0 - (1.0 - 1.0 / modulus) ** register_count
    union_bound = min(1.0, register_count / modulus)
    threshold = n_bits**-2
    return SignedPermutationScalingRow(
        n_bits=n_bits,
        register_count=register_count,
        tested_depth=tested_depth,
        exact_transport_probability=exact_probability,
        union_bound_probability=union_bound,
        inverse_polynomial_threshold=threshold,
        exponentially_small_at_linear_depth=union_bound < threshold,
        expected_transport_count=register_count / modulus,
    )


def run_signed_permutation_transport_audit(
    n_values: Sequence[int] = (32, 64, 128, 256),
    register_offset: int = 4,
) -> SignedPermutationTransportReport:
    exhaustive_rows = [
        exhaustive_classification_row(depth=1, register_count=3),
        exhaustive_classification_row(depth=2, register_count=3),
        exhaustive_classification_row(depth=3, register_count=3),
    ]
    scaling_rows = [scaling_row(n, register_offset=register_offset) for n in n_values]
    mismatches = sum(row.mismatch_count for row in exhaustive_rows)
    no_go_count = sum(row.exponentially_small_at_linear_depth for row in scaling_rows)
    metrics: dict[str, int | float] = {
        "exact_classification_theorem_count": 1,
        "exhaustive_label_tuple_count": sum(
            row.label_tuple_count for row in exhaustive_rows
        ),
        "exhaustive_classification_mismatch_count": mismatches,
        "linear_depth_scaling_row_count": len(scaling_rows),
        "linear_depth_exponential_no_go_row_count": no_go_count,
        "maximum_linear_depth_transport_probability_bound": max(
            (row.union_bound_probability for row in scaling_rows), default=0.0
        ),
        "proved_signed_permutation_advantage_count": 0,
        "proved_polynomial_relation_solver_count": 0,
    }
    return SignedPermutationTransportReport(
        created_at=utc_now(),
        theorem=build_theorem_certificate(),
        exhaustive_rows=exhaustive_rows,
        scaling_rows=scaling_rows,
        headline_metrics=metrics,
        claim_gate={
            "signed_permutation_classification_proved": mismatches == 0,
            "signed_permutation_route_extends_single_pivot": False,
            "signed_permutation_linear_depth_route_alive": no_go_count < len(scaling_rows),
            "nonlinear_implicit_transport_route_alive": True,
            "partial_or_walk_transport_route_alive": True,
            "polynomial_relation_solver_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "All total signed-coordinate permutations collapse exactly to the existing v2 pivot condition, "
                "which has exponentially small incidence at linear depth. Only genuinely coordinate-mixing, "
                "nonlinear, partial, or walk-based mechanisms remain outside this theorem."
            ),
        },
        status="signed-permutation-transport-class-collapses-to-single-pivot",
        summary=(
            f"Proved and exhaustively checked the signed-permutation collapse on "
            f"{metrics['exhaustive_label_tuple_count']} label tuples with {mismatches} mismatches. "
            f"Linear-depth incidence is below n^-2 in {no_go_count}/{len(scaling_rows)} scaling rows."
        ),
        falsifiers_triggered=[
            "Permuting complemented coordinates cannot synthesize a new constant next-bit translation.",
            "Sign-paired non-self-inverse labels cancel from the constant translation term.",
            "The only useful self-inverse residue is 2^k, exactly the original single-coordinate pivot.",
            "Random density-one labels contain such a pivot at linear depth with probability at most m/2^(k+1).",
            "This theorem does not reject partial transports, nonlinear global maps, or fiber quantum walks.",
        ],
    )


def write_signed_permutation_transport_audit(
    path: Path = DCP_SIGNED_PERMUTATION_TRANSPORT_PATH,
    n_values: Sequence[int] = (32, 64, 128, 256),
    register_offset: int = 4,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(
        run_signed_permutation_transport_audit(
            n_values=n_values, register_offset=register_offset
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-SIGNED-PERMUTATIONS-AS-GLOBAL-FIBER-TRANSPORT",
                source=str(path),
                claim=(
                    "Coordinate permutations plus arbitrary bit complements provide a broader total linear-depth "
                    "2-adic fiber transport than a single exact-valuation pivot."
                ),
                reason_invalid=(
                    "Exact coefficient and sign-orbit balance forces the translation to come from an odd number "
                    "of labels congruent to 2^k, so the class exists exactly when a single pivot exists."
                ),
                lesson=(
                    "Exclude all signed-coordinate permutations from the global transport search. Search only "
                    "genuine coordinate-mixing GF(2)-affine maps, nonlinear arithmetic maps, partial transports, "
                    "or walks, and subject each to source and classical-access audits."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or (
            f"RESULT-{registry_experiment_id}-DCP-SIGNED-PERMUTATION-TRANSPORT"
        )
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
                artifacts={"dcp_signed_permutation_transport": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_signed_permutation_transport_audit()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
