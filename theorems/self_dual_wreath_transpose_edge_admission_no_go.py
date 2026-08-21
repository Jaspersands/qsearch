"""Admission no-go for source-level transpose Young-edge sign twists.

The explicit sign-twist activation needs a source pair ``(C,D)`` for which
``C^T`` and ``D`` share an ``S_(n-1)`` child.  Replacing its fixed low-weight
pair by naturally sampled typical labels does not make this local condition
likely.

For independent Plancherel labels ``C,D`` define

    P_edge = Pr[g(C^T,D,(n-1,1))>0 and C!=D].             (1)

Every partition has at most

    Delta_n <= (sqrt(2n)+1)^2                             (2)

Young-graph neighbors: choose a removable child and an addable parent.  If
``p_*`` is the largest Plancherel atom, then

    P_edge <= Delta_n p_*.                               (3)

The maximal-irrep theorem gives ``p_*=exp(-Theta(sqrt(n)))``.  Polynomial
degree in (2), or polynomially many sampled source pairs, cannot overcome this
stretched-exponential scale.  Collision-free conditioning has asymptotic mass
one and does not change the conclusion.

This closes the *source-local transpose-edge* mutation of the sign-twist
portfolio.  It does not rule out collective tensor-product recoupling, where
intermediate parents can become adjacent despite every source-level edge being
absent; the repository already has finite examples of exactly that escape.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_point_stabilizer_quotient import removable_children
from self_dual_wreath_point_standard_energy import standard_kronecker_multiplicity
from self_dual_wreath_sign_twist_collective_activation import transpose_partition


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_transpose_edge_admission_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-TRANSPOSE-EDGE-ADMISSION-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
MAXIMAL_DIMENSION_PAPER_ID = "aggarwal-elboim-maximal-dimension-2026"
MAXIMAL_DIMENSION_PAPER_URL = "https://arxiv.org/abs/2605.25995"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class TransposeEdgeAdmissionControl:
    n: int
    partition_count: int
    group_order: int
    exact_distinct_transpose_edge_probability: str
    distinct_transpose_edge_probability: float
    ordered_active_pair_count: int
    maximum_transpose_neighbor_count: int
    removable_addable_degree_upper_bound: float
    maximum_plancherel_atom: float
    degree_times_max_atom_upper_bound: float
    probability_bound_violation: float
    maximum_degree_bound_violation: float
    transpose_edge_symmetry_residual: int
    exact_finite_admission_bound_verified: bool
    status: str


@dataclass(frozen=True)
class TransposeEdgeAdmissionScalingRecord:
    n: int
    polynomial_sample_exponent: int
    sample_pool_pair_count_log2_upper: float
    young_neighbor_degree_upper: float
    maximum_plancherel_atom_asymptotic: str
    one_pair_transpose_edge_probability_upper_asymptotic: str
    polynomial_pool_probability_upper_asymptotic: str
    inverse_polynomial_source_local_transpose_edge_admission: bool
    collective_intermediate_recoupling_ruled_out: bool
    status: str


@dataclass(frozen=True)
class TransposeEdgeAdmissionTheorem:
    event: str
    young_degree: str
    probability_bound: str
    asymptotic: str
    polynomial_pool: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class TransposeEdgeAdmissionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: TransposeEdgeAdmissionTheorem
    finite_controls: list[TransposeEdgeAdmissionControl]
    scaling_records: list[TransposeEdgeAdmissionScalingRecord]
    literature_links: list[dict[str, str | bool]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def transpose_young_neighbors(
    partition: Partition,
    universe: tuple[Partition, ...],
) -> tuple[Partition, ...]:
    conjugate = transpose_partition(partition)
    return tuple(
        candidate
        for candidate in universe
        if candidate != partition
        and standard_kronecker_multiplicity(conjugate, candidate) > 0
    )


def audit_transpose_edge_admission(
    n: int,
    *,
    tolerance: float = 1e-15,
) -> TransposeEdgeAdmissionControl:
    if n < 3:
        raise ValueError("n must be at least three")
    partitions = tuple(integer_partitions(n))
    order = math.factorial(n)
    weights = {
        partition: Fraction(hook_length_dimension(partition) ** 2, order)
        for partition in partitions
    }
    neighbors = {
        partition: transpose_young_neighbors(partition, partitions)
        for partition in partitions
    }
    probability = sum(
        (
            weights[left] * weights[right]
            for left, rows in neighbors.items()
            for right in rows
        ),
        Fraction(),
    )
    maximum_atom = max(weights.values())
    maximum_degree = max(len(rows) for rows in neighbors.values())
    degree_upper = (math.sqrt(2 * n) + 1) ** 2
    probability_upper = min(1.0, maximum_degree * float(maximum_atom))
    probability_violation = max(0.0, float(probability) - probability_upper)
    degree_violation = max(0.0, maximum_degree - degree_upper)
    symmetry_residual = max(
        (
            abs(
                standard_kronecker_multiplicity(
                    transpose_partition(left),
                    right,
                )
                - standard_kronecker_multiplicity(
                    transpose_partition(right),
                    left,
                )
            )
            for left in partitions
            for right in partitions
        ),
        default=0,
    )
    verified = bool(
        probability_violation <= tolerance
        and degree_violation <= tolerance
        and symmetry_residual == 0
    )
    return TransposeEdgeAdmissionControl(
        n=n,
        partition_count=len(partitions),
        group_order=order,
        exact_distinct_transpose_edge_probability=str(probability),
        distinct_transpose_edge_probability=float(probability),
        ordered_active_pair_count=sum(len(rows) for rows in neighbors.values()),
        maximum_transpose_neighbor_count=maximum_degree,
        removable_addable_degree_upper_bound=degree_upper,
        maximum_plancherel_atom=float(maximum_atom),
        degree_times_max_atom_upper_bound=probability_upper,
        probability_bound_violation=probability_violation,
        maximum_degree_bound_violation=degree_violation,
        transpose_edge_symmetry_residual=symmetry_residual,
        exact_finite_admission_bound_verified=verified,
        status=(
            "finite-transpose-edge-admission-bound-verified"
            if verified
            else "transpose-edge-admission-validation-failure"
        ),
    )


def transpose_edge_admission_scaling_record(
    n: int,
    *,
    polynomial_sample_exponent: int = 4,
) -> TransposeEdgeAdmissionScalingRecord:
    if n < 3 or polynomial_sample_exponent < 1:
        raise ValueError("invalid scaling parameters")
    pool_log2 = polynomial_sample_exponent * math.log2(n)
    return TransposeEdgeAdmissionScalingRecord(
        n=n,
        polynomial_sample_exponent=polynomial_sample_exponent,
        sample_pool_pair_count_log2_upper=2 * pool_log2 - 1,
        young_neighbor_degree_upper=(math.sqrt(2 * n) + 1) ** 2,
        maximum_plancherel_atom_asymptotic="exp(-Theta(sqrt(n)))",
        one_pair_transpose_edge_probability_upper_asymptotic=(
            "poly(n) exp(-Theta(sqrt(n)))=exp(-Theta(sqrt(n)))"
        ),
        polynomial_pool_probability_upper_asymptotic=(
            "poly(n) exp(-Theta(sqrt(n)))=exp(-Theta(sqrt(n)))"
        ),
        inverse_polynomial_source_local_transpose_edge_admission=False,
        collective_intermediate_recoupling_ruled_out=False,
        status="source-local-transpose-edge-stretched-exponential-admission",
    )


def run_transpose_edge_admission_no_go() -> TransposeEdgeAdmissionReport:
    controls = [audit_transpose_edge_admission(n) for n in range(4, 17)]
    scaling = [
        transpose_edge_admission_scaling_record(n)
        for n in (32, 64, 128, 256, 512, 1024)
    ]
    failures = sum(not row.exact_finite_admission_bound_verified for row in controls)
    verified = failures == 0
    theorem = TransposeEdgeAdmissionTheorem(
        event=(
            "P_edge=Pr[g(C^T,D,(n-1,1))>0 and C!=D] under independent "
            "Plancherel labels."
        ),
        young_degree=(
            "Each C^T has at most (sqrt(2n)+1)^2 distinct parents reachable "
            "through one removable child."
        ),
        probability_bound="P_edge<=Delta_n max_lambda d_lambda^2/n!.",
        asymptotic=(
            "The maximal-irrep theorem gives P_edge<=exp(-Theta(sqrt(n))) "
            "up to polynomial factors."
        ),
        polynomial_pool=(
            "A polynomial label pool has only polynomially many pairs and retains "
            "stretched-exponentially small transpose-edge admission."
        ),
        scope=(
            "The no-go covers a source-local transpose Young edge. It does not cover "
            "collective intermediate tensor-product recoupling."
        ),
        theorem_verified=verified,
        status=(
            "source-local-transpose-edge-admission-no-go"
            if verified
            else "transpose-edge-admission-validation-failure"
        ),
    )
    return TransposeEdgeAdmissionReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        literature_links=[
            {
                "paper_id": MAXIMAL_DIMENSION_PAPER_ID,
                "url": MAXIMAL_DIMENSION_PAPER_URL,
                "supports": (
                    "The largest Plancherel atom is exp(-Theta(sqrt(n)))."
                ),
                "external_theorem_not_reproved_here": True,
            }
        ],
        proof_obligations=[
            {
                "obligation": "test_typical_source_local_transpose_edge_mutation",
                "resolved": verified,
                "resolution": (
                    "Polynomial Young degree times the maximal Plancherel atom leaves "
                    "stretched-exponentially small admission."
                ),
            },
            {
                "obligation": "derive_typical_collective_intermediate_recoupling_law",
                "resolved": False,
                "resolution": (
                    "Tensor products can create adjacent intermediate parents without "
                    "any source edge; their natural aggregate mass is unbounded."
                ),
            },
            {
                "obligation": "find_label_adaptive_dense_recoupling_transform",
                "resolved": False,
                "resolution": (
                    "A viable circuit must act uniformly on sampled typical labels and "
                    "coherently aggregate many intermediate channels."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Each typical partition has polynomially many Young neighbors, so one should appear with polynomial probability.",
                "resolved": True,
                "resolution": (
                    "False. Every neighbor atom is at most stretched-exponentially "
                    "small; polynomial degree does not change that scale."
                ),
            },
            {
                "objection": "A birthday search over polynomially many labels repairs the edge event.",
                "resolved": True,
                "resolution": (
                    "False. The number of tested pairs remains polynomial."
                ),
            },
            {
                "objection": "The no-go extends to the S_6 collective activation witness.",
                "resolved": True,
                "resolution": (
                    "False. That witness is generated after tensor-product recoupling "
                    "and has no source-level Young edge."
                ),
            },
        ],
        headline_metrics={
            "source_local_transpose_edge_bound_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "polynomial_pool_source_edge_admission_count": 0,
            "collective_intermediate_recoupling_no_go_count": 0,
            "natural_typical_collective_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "source_local_transpose_edge_probability_bound_proved": verified,
            "source_local_transpose_edge_admission_stretched_exponential": verified,
            "polynomial_label_pool_repairs_source_edge": False,
            "collective_intermediate_recoupling_ruled_out": False,
            "typical_collective_energy_bound_proved": False,
            "polynomial_point_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Local transpose edges are too rare; only a genuinely collective, "
                "label-adaptive intermediate-channel mechanism remains viable."
            ),
        },
        status=theorem.status,
        summary=(
            "Closed the natural source-local transpose-edge repair using Young-graph "
            "degree and maximal Plancherel mass. Redirected the search to collective "
            "intermediate recoupling across typical unmatched labels."
        ),
        falsifiers_triggered=[
            (
                "Polynomial Young-neighbor degree does not imply inverse-polynomial "
                "natural edge mass."
            ),
            (
                "Exact conjugacy is not the only rare local event; one-box proximity "
                "to a conjugate shape is also stretched-exponentially rare."
            ),
            (
                "The no-go leaves collective tensor-product recoupling open and must "
                "not be generalized beyond source-local edges."
            ),
        ],
    )


def write_transpose_edge_admission_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-TRANSPOSE-EDGE-ADMISSION-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_transpose_edge_admission_no_go" in globals():
        report = run_transpose_edge_admission_no_go(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-TRANSPOSE-EDGE-ADMISSION-NO-GO",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-TRANSPOSE-EDGE-ADMISSION-NO-GO.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-TRANSPOSE-EDGE-ADMISSION-NO-GO.",
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
                    "self_dual_wreath_transpose_edge_admission_no_go": str(path)
                },
            )
        )
    return payload
