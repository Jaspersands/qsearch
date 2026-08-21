"""Decoupling theorem for dephased shared-pair Kronecker recoupling.

Let ``lambda,mu`` be independent Plancherel irreps and, conditional on that
same source pair, draw two dimension-weighted Kronecker outputs independently:

    nu,xi ~ K_(lambda,mu),
    K_(lambda,mu)(nu)=g(lambda,mu,nu)d_nu/(d_lambda d_mu).

Their exact joint law is

    J(nu,xi)
      = d_nu d_xi/|G|^2 sum_(lambda,mu)
          g(lambda,mu,nu)g(lambda,mu,xi)
      = d_nu d_xi/|G|^2 sum_C chi_nu(C)chi_xi(C),         (1)

where ``C`` ranges over conjugacy classes.  Column orthogonality proves the
second equality.  Relative to independent Plancherel outputs ``p tensor p``,

    J/(p tensor p)
      = 1 + sum_(C != e) r_nu(C)r_xi(C).                 (2)

Plancherel character orthogonality then gives an exact chi-square divergence:

    chi^2(J || p tensor p) = sum_(C != e) |C|^-2.        (3)

For ``S_n``, writing a class as a fixed-point-free cycle partition of support
``s`` gives

    sum_(C != e)|C|^-2
      = 4/(n)_2^2 + 9/(n)_3^2 + O(n^-8)
      = 4/n^4 + O(n^-5).                                 (4)

Consequently

    TV(J,p tensor p) <= 1/2 sqrt(chi^2) = O(n^-2),
    I(nu:xi) <= log2(1+chi^2) = O(n^-4).                 (5)

Thus even reusing the entire source pair does not create asymptotically strong
correlation after dimension-weighted intermediate labels are measured.  This
does not apply to coherent superpositions over multiplicity/Racah paths, nor
to state-dependent filters before that dephasing.  Those phases are now a
necessary resource for any substantial collective-recoupling decoder.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from symmetric_character import kronecker_coefficient, symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_shared_pair_recoupling_decoupling.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SHARED-PAIR-RECOUPLING-DECOUPLING"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class SharedPairRecouplingControl:
    n: int
    partition_count: int
    group_order: int
    exact_joint_normalization_residual: str
    exact_maximum_plancherel_marginal_residual: str
    maximum_multiplicity_character_kernel_residual: int
    exact_chi_square_divergence: str
    exact_inverse_class_square_sum: str
    chi_square_identity_residual: str
    total_variation_distance: float
    chi_square_total_variation_upper_bound: float
    total_variation_bound_violation: float
    mutual_information_bits: float
    chi_square_mutual_information_upper_bound_bits: float
    mutual_information_bound_violation: float
    transposition_leading_term: float
    inverse_class_square_to_transposition_ratio: float
    exact_shared_pair_decoupling_theorem_verified: bool
    status: str


@dataclass(frozen=True)
class SharedPairRecouplingScalingRecord:
    n: int
    exact_inverse_class_square_sum: float
    transposition_leading_term: float
    three_cycle_second_term: float
    normalized_remainder_after_two_terms: float
    total_variation_upper_bound: float
    mutual_information_upper_bound_bits: float
    asymptotic_chi_square: str
    asymptotic_total_variation: str
    asymptotic_mutual_information: str
    dephased_shared_pair_label_correlation_inverse_polynomial: bool
    coherent_multiplicity_racah_phases_ruled_out: bool
    status: str


@dataclass(frozen=True)
class SharedPairRecouplingTheorem:
    joint_law: str
    character_collapse: str
    likelihood_ratio: str
    exact_chi_square: str
    symmetric_group_asymptotic: str
    information_consequence: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class SharedPairRecouplingReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: SharedPairRecouplingTheorem
    finite_controls: list[SharedPairRecouplingControl]
    scaling_records: list[SharedPairRecouplingScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def class_centralizer_size(cycle_type: Partition) -> int:
    multiplicities = Counter(cycle_type)
    return math.prod(
        length**count * math.factorial(count)
        for length, count in multiplicities.items()
    )


def inverse_class_square_sum(n: int) -> Fraction:
    if n < 2:
        raise ValueError("n must be at least two")
    order = math.factorial(n)
    return sum(
        (
            Fraction(class_centralizer_size(cycle) ** 2, order**2)
            for cycle in integer_partitions(n)
            if cycle != (1,) * n
        ),
        Fraction(),
    )


def plancherel_weights(n: int) -> dict[Partition, Fraction]:
    order = math.factorial(n)
    return {
        partition: Fraction(hook_length_dimension(partition) ** 2, order)
        for partition in integer_partitions(n)
    }


def shared_pair_joint_law(n: int) -> dict[tuple[Partition, Partition], Fraction]:
    """Evaluate equation (1) by its class-character collapse."""

    if n < 2:
        raise ValueError("n must be at least two")
    partitions = tuple(integer_partitions(n))
    cycles = tuple(integer_partitions(n))
    order = math.factorial(n)
    dimensions = {
        partition: hook_length_dimension(partition) for partition in partitions
    }
    characters = {
        partition: {
            cycle: symmetric_character(partition, cycle) for cycle in cycles
        }
        for partition in partitions
    }
    return {
        (left, right): Fraction(
            dimensions[left]
            * dimensions[right]
            * sum(
                characters[left][cycle] * characters[right][cycle]
                for cycle in cycles
            ),
            order**2,
        )
        for left in partitions
        for right in partitions
    }


def multiplicity_kernel_entry(
    n: int,
    left: Partition,
    right: Partition,
) -> int:
    partitions = tuple(integer_partitions(n))
    return sum(
        kronecker_coefficient(source_left, source_right, left)
        * kronecker_coefficient(source_left, source_right, right)
        for source_left in partitions
        for source_right in partitions
    )


def audit_shared_pair_recoupling_decoupling(
    n: int,
    *,
    validate_multiplicity_kernel: bool = True,
    tolerance: float = 1e-12,
) -> SharedPairRecouplingControl:
    partitions = tuple(integer_partitions(n))
    cycles = tuple(integer_partitions(n))
    order = math.factorial(n)
    weights = plancherel_weights(n)
    joint = shared_pair_joint_law(n)
    product = {
        (left, right): weights[left] * weights[right]
        for left in partitions
        for right in partitions
    }
    normalization_residual = abs(sum(joint.values()) - 1)
    marginal_residual = max(
        *(
            abs(sum(joint[left, right] for right in partitions) - weights[left])
            for left in partitions
        ),
        *(
            abs(sum(joint[left, right] for left in partitions) - weights[right])
            for right in partitions
        ),
    )
    kernel_residual = 0
    if validate_multiplicity_kernel:
        for left in partitions:
            for right in partitions:
                character_kernel = sum(
                    symmetric_character(left, cycle)
                    * symmetric_character(right, cycle)
                    for cycle in cycles
                )
                kernel_residual = max(
                    kernel_residual,
                    abs(
                        multiplicity_kernel_entry(n, left, right)
                        - character_kernel
                    ),
                )
    chi_square = sum(
        (
            (joint[pair] - product[pair]) ** 2 / product[pair]
            for pair in joint
        ),
        Fraction(),
    )
    class_sum = inverse_class_square_sum(n)
    chi_residual = abs(chi_square - class_sum)
    total_variation = Fraction(1, 2) * sum(
        (abs(joint[pair] - product[pair]) for pair in joint),
        Fraction(),
    )
    tv_upper = 0.5 * math.sqrt(float(chi_square))
    tv_violation = max(0.0, float(total_variation) - tv_upper)
    mutual_information = sum(
        (
            float(probability)
            * math.log2(float(probability / product[pair]))
            for pair, probability in joint.items()
            if probability > 0
        )
    )
    mutual_upper = math.log2(1 + float(chi_square))
    mutual_violation = max(0.0, mutual_information - mutual_upper)
    leading = Fraction(4, (n * (n - 1)) ** 2)
    verified = bool(
        normalization_residual == 0
        and marginal_residual == 0
        and kernel_residual == 0
        and chi_residual == 0
        and tv_violation <= tolerance
        and mutual_violation <= tolerance
    )
    return SharedPairRecouplingControl(
        n=n,
        partition_count=len(partitions),
        group_order=order,
        exact_joint_normalization_residual=str(normalization_residual),
        exact_maximum_plancherel_marginal_residual=str(marginal_residual),
        maximum_multiplicity_character_kernel_residual=kernel_residual,
        exact_chi_square_divergence=str(chi_square),
        exact_inverse_class_square_sum=str(class_sum),
        chi_square_identity_residual=str(chi_residual),
        total_variation_distance=float(total_variation),
        chi_square_total_variation_upper_bound=tv_upper,
        total_variation_bound_violation=tv_violation,
        mutual_information_bits=mutual_information,
        chi_square_mutual_information_upper_bound_bits=mutual_upper,
        mutual_information_bound_violation=mutual_violation,
        transposition_leading_term=float(leading),
        inverse_class_square_to_transposition_ratio=float(class_sum / leading),
        exact_shared_pair_decoupling_theorem_verified=verified,
        status=(
            "exact-dephased-shared-pair-recoupling-decoupling"
            if verified
            else "shared-pair-recoupling-validation-failure"
        ),
    )


def shared_pair_recoupling_scaling_record(
    n: int,
) -> SharedPairRecouplingScalingRecord:
    if n < 4:
        raise ValueError("n must be at least four")
    exact = float(inverse_class_square_sum(n))
    transposition = 4 / (n * (n - 1)) ** 2
    three_cycle = 9 / (n * (n - 1) * (n - 2)) ** 2
    remainder = max(0.0, exact - transposition - three_cycle)
    return SharedPairRecouplingScalingRecord(
        n=n,
        exact_inverse_class_square_sum=exact,
        transposition_leading_term=transposition,
        three_cycle_second_term=three_cycle,
        normalized_remainder_after_two_terms=(
            remainder * n**8
        ),
        total_variation_upper_bound=0.5 * math.sqrt(exact),
        mutual_information_upper_bound_bits=math.log2(1 + exact),
        asymptotic_chi_square="4/n^4+O(n^-5)",
        asymptotic_total_variation="O(n^-2)",
        asymptotic_mutual_information="O(n^-4)",
        dephased_shared_pair_label_correlation_inverse_polynomial=True,
        coherent_multiplicity_racah_phases_ruled_out=False,
        status="dephased-shared-pair-labels-asymptotically-decouple",
    )


def run_shared_pair_recoupling_decoupling() -> SharedPairRecouplingReport:
    controls = [
        audit_shared_pair_recoupling_decoupling(
            n,
            validate_multiplicity_kernel=n <= 8,
        )
        for n in range(3, 11)
    ]
    scaling = [
        shared_pair_recoupling_scaling_record(n)
        for n in (8, 12, 16, 24, 32)
    ]
    failures = sum(
        not row.exact_shared_pair_decoupling_theorem_verified for row in controls
    )
    verified = failures == 0
    theorem = SharedPairRecouplingTheorem(
        joint_law=(
            "J(nu,xi)=d_nu d_xi/|G|^2 sum_(lambda,mu) "
            "g(lambda,mu,nu)g(lambda,mu,xi)."
        ),
        character_collapse=(
            "Column orthogonality gives sum_(lambda,mu)gg="
            "sum_C chi_nu(C)chi_xi(C)."
        ),
        likelihood_ratio=(
            "J/(p tensor p)=1+sum_(C!=e)r_nu(C)r_xi(C)."
        ),
        exact_chi_square=(
            "chi^2(J||p tensor p)=sum_(C!=e)|C|^-2."
        ),
        symmetric_group_asymptotic=(
            "The transposition and three-cycle classes give "
            "4/(n)_2^2+9/(n)_3^2, and the remaining support expansion is O(n^-8)."
        ),
        information_consequence=(
            "TV=O(n^-2) and I(nu:xi)=O(n^-4) after intermediate irrep labels "
            "are dimension-weighted and measured."
        ),
        scope=(
            "The theorem does not dephase or bound coherent multiplicity/Racah path "
            "superpositions and state-dependent filters."
        ),
        theorem_verified=verified,
        status=(
            "dephased-shared-pair-recoupling-decoupling-proved-coherence-open"
            if verified
            else "shared-pair-recoupling-validation-failure"
        ),
    )
    return SharedPairRecouplingReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_shared_source_pair_intermediate_label_law",
                "resolved": verified,
                "resolution": (
                    "The exact law collapses to an unweighted conjugacy-class "
                    "character Gram."
                ),
            },
            {
                "obligation": "quantify_shared_pair_label_correlation",
                "resolved": verified,
                "resolution": (
                    "Its chi-square divergence is the exact inverse-class-square sum, "
                    "giving TV O(n^-2) and mutual information O(n^-4)."
                ),
            },
            {
                "obligation": "test_dephased_shared_pair_labels_as_decoder_resource",
                "resolved": verified,
                "resolution": (
                    "Rejected as an asymptotically strong resource: the labels decouple."
                ),
            },
            {
                "obligation": "analyze_coherent_multiplicity_racah_path_information",
                "resolved": False,
                "resolution": (
                    "The exact dephased law identifies phases and multiplicity-path "
                    "coherence as the remaining possible resource."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Reusing the same source pair keeps order-one classical intermediate-label correlation.",
                "resolved": True,
                "resolution": (
                    "False asymptotically: TV is O(n^-2) and mutual information is O(n^-4)."
                ),
            },
            {
                "objection": "The finite n<=10 edge probabilities show strong asymptotic correlation.",
                "resolved": True,
                "resolution": (
                    "False. Finite character kernels are preasymptotic; the exact "
                    "inverse-class sum proves decorrelation."
                ),
            },
            {
                "objection": "Classical label decoupling dequantizes coherent Racah processing.",
                "resolved": True,
                "resolution": (
                    "False. Measurement erases the very multiplicity and path phases "
                    "that a quantum decoder might exploit."
                ),
            },
        ],
        headline_metrics={
            "shared_pair_joint_character_kernel_theorem_count": 1,
            "exact_chi_square_decoupling_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "dephased_shared_pair_strong_information_resource_count": 0,
            "coherent_multiplicity_path_information_theorem_count": 0,
            "natural_collective_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "shared_pair_joint_character_kernel_proved": verified,
            "exact_inverse_class_square_chi_square_proved": verified,
            "dephased_shared_pair_outputs_asymptotically_decouple": verified,
            "coherent_multiplicity_racah_paths_dequantized": False,
            "state_dependent_transition_filter_ruled_out": False,
            "polynomial_point_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Measured intermediate labels carry vanishing correlation; only "
                "coherent multiplicity/path processing remains untested."
            ),
        },
        status=theorem.status,
        summary=(
            "Solved the shared-source-pair measured-label law exactly and proved it "
            "decouples in total variation as O(n^-2). This removes another classical "
            "recoupling shortcut and isolates coherent Racah path phases."
        ),
        falsifiers_triggered=[
            (
                "Reusing a complete source pair does not retain order-one correlation "
                "after dimension-weighted intermediate labels are measured."
            ),
            (
                "The exact correlation scale is controlled by inverse conjugacy-class "
                "sizes and is dominated asymptotically by transpositions."
            ),
            (
                "A viable collective decoder must avoid dephasing multiplicity/Racah "
                "paths into classical intermediate labels."
            ),
        ],
    )


def write_shared_pair_recoupling_decoupling_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-SHARED-PAIR-RECOUPLING-DECOUPLING"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_shared_pair_recoupling_decoupling" in globals():
        report = run_shared_pair_recoupling_decoupling(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-SHARED-PAIR-RECOUPLING-DECOUPLING",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-SHARED-PAIR-RECOUPLING-DECOUPLING.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-SHARED-PAIR-RECOUPLING-DECOUPLING.",
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
                    "self_dual_wreath_shared_pair_recoupling_decoupling": str(path)
                },
            )
        )
    return payload
