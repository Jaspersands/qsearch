"""Boundary for retaining orientation characters in the physical decoder.

The physical row-copy isometry can be returned to the group time basis as

    |psi> -> |G|^(-1/2) sum_s |s> U_s^* |psi>.

Measuring only ``s`` is therefore exactly uniform, even if an arbitrary
unitary has first been applied to the residual register.  A natural attempted
escape is to Walsh-transform the physical orientation register, retain its
character ``z``, and use ``z`` to correct the random group label.

For unequal labels ``(lambda_i,mu_i)``, align the two induced branches and put

    sigma_e(h) = tensor_i [rho_lambda_i(h) tensor I]       if e_i=0,
                             [I tensor rho_mu_i(h)]         if e_i=1.

The source isometry is ``Vx=2^(-k/2) sum_e |e>x``.  A full orientation Walsh
measurement after the relative group action ``h`` has carrier Kraus operator

    K_z(h) = 2^(-k) sum_e (-1)^(z.e) sigma_e(h)
           = tensor_i (rho_lambda_i(h) tensor I
                 + (-1)^z_i I tensor rho_mu_i(h))/2.       (1)

On the maximally mixed source carrier its exact outcome law is

    p(z|h) = 2^(-k) product_i (1 + (-1)^z_i r_i(h)),       (2)

where

    r_i(h)=chi_lambda_i(h) chi_mu_i(h)/(d_lambda_i d_mu_i).

Every ``r_i`` is a symmetric-group character ratio, so (2) depends only on
the cycle type of ``h``.

Suppose the row-copy time label is ``s`` and a decoder applies a
character-controlled right correction ``d(z)``, outputting ``s d(z)``.  This
is exactly the operation induced by using ``z`` to select a group element on
the Fourier column before the inverse group QFT.  Its success is

    P_d = |S_n|^(-1) sum_z p(z|d(z)).                       (3)

The best such decoder obeys

    P_opt = |S_n|^(-1) sum_z max_h p(z|h)
          <= p(n)/n!,                                      (4)

because the channel is constant on conjugacy classes and ``S_n`` has ``p(n)``
classes.  For success modulo a stabilizer of size ``a``, the same argument and
a union bound give ``P_opt<=a p(n)/n!``.  Hence this architecture has
``exp(-Theta(n log n))`` success for every subfactorial stabilizer.

This does not rule out an arbitrary character-controlled unitary in the full
right group algebra, a transform that processes the carrier coherently, or a
multi-round orientation-index relocation.  It proves that a retained branch
character is not, by itself, the missing Fourier column.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_character_moments import permutation_cycle_type
from self_dual_wreath_orientation_fourier_reduction import (
    _orientation_representation_matrix,
    _source_representation_rows,
    _w4_collision_free_labels,
)
from symmetric_character import symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_branch_character_decoder_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-DECODER-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Permutation = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class BranchCharacterChannelControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    group_order: int
    conjugacy_class_count: int
    orientation_character_count: int
    carrier_dimension: int
    maximum_direct_factorization_residual: float
    maximum_probability_normalization_residual: float
    maximum_same_cycle_type_variation: float
    identity_zero_character_probability: float
    passive_group_guess_success: float
    optimal_character_correction_success: float
    conjugacy_class_success_ceiling: float
    optimal_to_ceiling_ratio: float
    exact_character_channel_verified: bool
    correction_decoder_bound_verified: bool
    status: str


@dataclass(frozen=True)
class BranchCharacterScalingRecord:
    n: int
    group_order_decimal: str
    conjugacy_class_count_decimal: str
    log2_group_order: float
    log2_conjugacy_class_count: float
    log2_character_correction_success_upper_bound: float
    amplitude_amplification_query_log2_lower_bound: float
    polynomial_benchmark_log2: float
    subfactorial_stabilizer_preserves_factorial_suppression: bool
    character_correction_superpolynomially_suppressed: bool
    carrier_dependent_coherent_decoder_ruled_out: bool
    status: str


@dataclass(frozen=True)
class BranchCharacterDecoderTheorem:
    passive_uniformity: str
    character_kraus_factorization: str
    character_probability_law: str
    correction_success: str
    conjugacy_class_bound: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class BranchCharacterDecoderBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: BranchCharacterDecoderTheorem
    finite_controls: list[BranchCharacterChannelControl]
    scaling_records: list[BranchCharacterScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def partition_number(n: int) -> int:
    """Return the number of integer partitions of ``n`` in O(n^2) time."""

    if n < 0:
        raise ValueError("n must be nonnegative")
    counts = [0] * (n + 1)
    counts[0] = 1
    for part in range(1, n + 1):
        for total in range(part, n + 1):
            counts[total] += counts[total - part]
    return counts[n]


def _validate_labels(n: int, labels: tuple[Label, ...]) -> None:
    if not labels:
        raise ValueError("at least one unequal partition pair is required")
    if any(
        sum(left) != n or sum(right) != n or left == right
        for left, right in labels
    ):
        raise ValueError("labels must be unequal partition pairs of n")


def branch_character_distribution_from_cycle_type(
    labels: tuple[Label, ...],
    cycle_type: Partition,
) -> np.ndarray:
    """Evaluate the exact product-Bernoulli law in equation (2)."""

    n = sum(cycle_type)
    _validate_labels(n, labels)
    ratios = []
    for left, right in labels:
        left_dimension = hook_length_dimension(left)
        right_dimension = hook_length_dimension(right)
        ratios.append(
            symmetric_character(left, cycle_type)
            * symmetric_character(right, cycle_type)
            / (left_dimension * right_dimension)
        )
    character_count = 1 << len(labels)
    probabilities = np.empty(character_count, dtype=float)
    for character in range(character_count):
        value = 1.0
        for index, ratio in enumerate(ratios):
            sign = -1.0 if character & (1 << index) else 1.0
            value *= (1.0 + sign * ratio) / 2.0
        probabilities[character] = value
    return probabilities


def branch_character_kraus(
    labels: tuple[Label, ...],
    permutation: Permutation,
    character: int,
) -> np.ndarray:
    """Return the factorized carrier Kraus operator in equation (1)."""

    n = len(permutation)
    _validate_labels(n, labels)
    character_count = 1 << len(labels)
    if character < 0 or character >= character_count:
        raise ValueError("orientation character out of range")
    factors = []
    for index, (left, right) in enumerate(labels):
        left_matrix = _source_representation_rows(left)[permutation]
        right_matrix = _source_representation_rows(right)[permutation]
        sign = -1.0 if character & (1 << index) else 1.0
        factors.append(
            (
                np.kron(left_matrix, np.eye(len(right_matrix)))
                + sign * np.kron(np.eye(len(left_matrix)), right_matrix)
            )
            / 2.0
        )
    output = factors[0]
    for factor in factors[1:]:
        output = np.kron(output, factor)
    return output


def direct_branch_character_distribution(
    labels: tuple[Label, ...],
    permutation: Permutation,
) -> np.ndarray:
    """Evaluate (1) by explicit matrices for finite theorem controls."""

    n = len(permutation)
    _validate_labels(n, labels)
    orientation_count = 1 << len(labels)
    carrier_dimension = math.prod(
        hook_length_dimension(left) * hook_length_dimension(right)
        for left, right in labels
    )
    orientations = tuple(
        _orientation_representation_matrix(labels, permutation, orientation)
        for orientation in range(orientation_count)
    )
    probabilities = np.empty(orientation_count, dtype=float)
    for character in range(orientation_count):
        direct_kraus = sum(
            (
                (-1.0 if (character & orientation).bit_count() % 2 else 1.0)
                * matrix
                for orientation, matrix in enumerate(orientations)
            ),
            np.zeros_like(orientations[0], dtype=complex),
        ) / orientation_count
        kraus = branch_character_kraus(labels, permutation, character)
        if np.linalg.norm(direct_kraus - kraus, ord=2) > 1e-9:
            raise ArithmeticError("orientation Walsh factorization failed")
        probabilities[character] = float(
            np.trace(kraus.conj().T @ kraus).real / carrier_dimension
        )
    return probabilities


def audit_branch_character_channel(
    n: int,
    labels: tuple[Label, ...],
    *,
    control_id: str,
    tolerance: float = 1e-10,
) -> BranchCharacterChannelControl:
    _validate_labels(n, labels)
    permutations = tuple(_source_representation_rows(labels[0][0]))
    cycle_types = tuple(integer_partitions(n))
    distributions_by_type = {
        cycle_type: branch_character_distribution_from_cycle_type(
            labels,
            cycle_type,
        )
        for cycle_type in cycle_types
    }
    maximum_factorization = 0.0
    maximum_normalization = 0.0
    direct_by_type: dict[Partition, list[np.ndarray]] = {
        cycle_type: [] for cycle_type in cycle_types
    }
    for permutation in permutations:
        cycle_type = permutation_cycle_type(permutation)
        direct = direct_branch_character_distribution(labels, permutation)
        predicted = distributions_by_type[cycle_type]
        maximum_factorization = max(
            maximum_factorization,
            float(np.max(np.abs(direct - predicted))),
        )
        maximum_normalization = max(
            maximum_normalization,
            abs(float(np.sum(direct)) - 1.0),
            max(0.0, -float(np.min(direct))),
        )
        direct_by_type[cycle_type].append(direct)
    same_type_variation = 0.0
    for rows in direct_by_type.values():
        if rows:
            reference = rows[0]
            same_type_variation = max(
                same_type_variation,
                *(float(np.max(np.abs(row - reference))) for row in rows),
            )

    stacked = np.stack(tuple(distributions_by_type.values()))
    optimal = float(np.sum(np.max(stacked, axis=0)) / math.factorial(n))
    ceiling = len(cycle_types) / math.factorial(n)
    identity = distributions_by_type[(1,) * n]
    channel_verified = bool(
        maximum_factorization <= 100 * tolerance
        and maximum_normalization <= 100 * tolerance
        and same_type_variation <= 100 * tolerance
        and abs(float(identity[0]) - 1.0) <= 100 * tolerance
        and float(np.max(np.abs(identity[1:]))) <= 100 * tolerance
    )
    bound_verified = optimal <= ceiling + 100 * tolerance
    return BranchCharacterChannelControl(
        control_id=control_id,
        n=n,
        labels=labels,
        group_order=math.factorial(n),
        conjugacy_class_count=len(cycle_types),
        orientation_character_count=1 << len(labels),
        carrier_dimension=math.prod(
            hook_length_dimension(left) * hook_length_dimension(right)
            for left, right in labels
        ),
        maximum_direct_factorization_residual=maximum_factorization,
        maximum_probability_normalization_residual=maximum_normalization,
        maximum_same_cycle_type_variation=same_type_variation,
        identity_zero_character_probability=float(identity[0]),
        passive_group_guess_success=1 / math.factorial(n),
        optimal_character_correction_success=optimal,
        conjugacy_class_success_ceiling=ceiling,
        optimal_to_ceiling_ratio=optimal / ceiling,
        exact_character_channel_verified=channel_verified,
        correction_decoder_bound_verified=bound_verified,
        status=(
            "exact-class-function-character-decoder-boundary"
            if channel_verified and bound_verified
            else "branch-character-decoder-validation-failure"
        ),
    )


def branch_character_scaling_record(
    n: int,
    *,
    polynomial_degree: int = 10,
) -> BranchCharacterScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    order = math.factorial(n)
    classes = partition_number(n)
    log_order = math.lgamma(n + 1) / math.log(2)
    log_classes = math.log2(classes)
    log_bound = log_classes - log_order
    benchmark = -polynomial_degree * math.log2(n)
    return BranchCharacterScalingRecord(
        n=n,
        group_order_decimal=str(order),
        conjugacy_class_count_decimal=str(classes),
        log2_group_order=log_order,
        log2_conjugacy_class_count=log_classes,
        log2_character_correction_success_upper_bound=log_bound,
        amplitude_amplification_query_log2_lower_bound=-0.5 * log_bound,
        polynomial_benchmark_log2=benchmark,
        subfactorial_stabilizer_preserves_factorial_suppression=True,
        character_correction_superpolynomially_suppressed=log_bound < benchmark,
        carrier_dependent_coherent_decoder_ruled_out=False,
        status="factorial-character-correction-suppression",
    )


def run_branch_character_decoder_boundary() -> BranchCharacterDecoderBoundaryReport:
    controls = [
        audit_branch_character_channel(
            3,
            (((3,), (2, 1)),),
            control_id="W3-SINGLE-UNEQUAL",
        ),
        audit_branch_character_channel(
            3,
            (
                ((3,), (2, 1)),
                ((3,), (1, 1, 1)),
                ((2, 1), (1, 1, 1)),
            ),
            control_id="W3-COLLISION-FREE-THRESHOLD",
        ),
        audit_branch_character_channel(
            4,
            _w4_collision_free_labels()[0],
            control_id="W4-COLLISION-FREE-PAIR",
        ),
    ]
    scaling = [
        branch_character_scaling_record(n)
        for n in (16, 32, 64, 80, 96, 128, 256, 512)
    ]
    failures = sum(
        not (
            row.exact_character_channel_verified
            and row.correction_decoder_bound_verified
        )
        for row in controls
    )
    verified = failures == 0
    theorem = BranchCharacterDecoderTheorem(
        passive_uniformity=(
            "Returning row-copy to the group basis gives unitary Kraus maps "
            "U_s^*/sqrt(|G|), so the group label alone is exactly uniform."
        ),
        character_kraus_factorization=(
            "K_z(h)=tensor_i[rho_lambda_i(h) tensor I + "
            "(-1)^z_i I tensor rho_mu_i(h)]/2."
        ),
        character_probability_law=(
            "p(z|h)=2^-k product_i[1+(-1)^z_i "
            "chi_lambda_i(h)chi_mu_i(h)/(d_lambda_i d_mu_i)]."
        ),
        correction_success=(
            "A character-controlled right correction d(z) has "
            "P_d=|S_n|^-1 sum_z p(z|d(z))."
        ),
        conjugacy_class_bound=(
            "P_opt<=p(n)/n!, or |Aut|p(n)/n! for success modulo a stabilizer."
        ),
        scope=(
            "The theorem excludes passive retention and character-controlled "
            "right-group corrections. Carrier-dependent coherent processing, "
            "general right-group-algebra unitaries, and multi-round routers remain open."
        ),
        theorem_verified=verified,
        status=(
            "branch-character-right-correction-factorially-suppressed"
            if verified
            else "branch-character-decoder-validation-failure"
        ),
    )
    return BranchCharacterDecoderBoundaryReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_native_branch_character_channel",
                "resolved": verified,
                "resolution": (
                    "The Walsh Kraus operators tensor-factor and their maximally "
                    "mixed probabilities are products of normalized character ratios."
                ),
            },
            {
                "obligation": "test_branch_character_as_group_column_correction",
                "resolved": verified,
                "resolution": (
                    "Every right-group correction selected only by the character "
                    "has success at most p(n)/n! for a rigid hidden label."
                ),
            },
            {
                "obligation": "analyze_arbitrary_character_controlled_commutant_unitary",
                "resolved": False,
                "resolution": (
                    "A general Fourier-column unitary is a right-group-algebra "
                    "operation, not necessarily a single right translation."
                ),
            },
            {
                "obligation": "construct_or_refute_carrier_dependent_joint_decoder",
                "resolved": False,
                "resolution": (
                    "The post-Walsh carrier contains matrix-valued, noncentral "
                    "information that equation (2) intentionally traces out."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "There are about n! character strings, so they can label permutations.",
                "resolved": verified,
                "resolution": (
                    "Cardinality is not information: the full outcome law is a "
                    "class function and cannot separate elements within a cycle type."
                ),
            },
            {
                "objection": "Keeping the character coherently changes the ordinary group marginal.",
                "resolved": verified,
                "resolution": (
                    "Any residual-only unitary leaves the group marginal invariant; "
                    "without a controlled correction the group label is uniform."
                ),
            },
            {
                "objection": "The class-function bound rules out every joint decoder.",
                "resolved": False,
                "resolution": (
                    "No. Tracing or ignoring the carrier removes cross-orientation "
                    "matrix information. A carrier-dependent coherent decoder is outside scope."
                ),
            },
        ],
        headline_metrics={
            "passive_uniformity_theorem_count": 1,
            "branch_character_factorization_theorem_count": 1,
            "conjugacy_class_decoder_bound_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "superpolynomial_scaling_row_count": sum(
                row.character_correction_superpolynomially_suppressed
                for row in scaling
            ),
            "carrier_dependent_joint_decoder_count": 0,
            "physical_orientation_polar_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "passive_branch_character_retention_changes_group_marginal": False,
            "native_branch_character_probability_factorization_proved": verified,
            "character_controlled_right_correction_factorially_suppressed": verified,
            "branch_character_alone_supplies_missing_fourier_column": False,
            "arbitrary_character_controlled_commutant_unitary_ruled_out": False,
            "carrier_dependent_joint_decoder_ruled_out": False,
            "multi_round_orientation_index_relocation_ruled_out": False,
            "physical_orientation_polar_compiled": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "A retained orientation character does not by itself replace the "
            "missing Fourier column: passive group outcomes are uniform, and every "
            "character-controlled right correction has at most p(n)/n! success."
        ),
        falsifiers_triggered=[
            (
                "Having as many branch characters as hidden labels does not imply "
                "decodability; their native probability law is conjugacy-class invariant."
            ),
            (
                "Keeping the full character instead of postselecting does not alter "
                "the ordinary inverse-QFT group marginal."
            ),
            (
                "A positive character-retaining decoder must process matrix-valued "
                "carrier information or use a broader commutant transform."
            ),
        ],
    )


def write_branch_character_decoder_boundary_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-DECODER-BOUNDARY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_branch_character_decoder_boundary" in globals():
        report = run_branch_character_decoder_boundary(**kwargs)
        payload = asdict(report) if hasattr(report, "__dataclass_fields__") else (dict(report) if isinstance(report, dict) else report)
    else:
        report = {}
        payload = {}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-BRANCH-CHARACTER-DECODER-BOUNDARY",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-DECODER-BOUNDARY.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-DECODER-BOUNDARY.",
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=payload.get("headline_metrics", {}),
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload.get("created_at", ""),
                status=payload.get("status", "completed"),
                summary=payload.get("summary", ""),
                metrics=payload.get("headline_metrics", {}),
                falsifiers_triggered=payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_branch_character_decoder_boundary": str(path)
                },
            )
        )
    return payload
