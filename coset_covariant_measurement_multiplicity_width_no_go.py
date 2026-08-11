"""Multiplicity-width lower bound for successful covariant coset POVMs.

Let ``rho_h=P_h/r`` be ``M`` equiprobable rank-``r`` projector states in one
conjugacy orbit.  For any exact-identification POVM with conclusive effects
``E_h`` and optional failure effect, put ``K=sum_h E_h``.  Since ``P_h<=I``,

    p_id <= Tr(K)/(M r) <= rank(K)/(M r).                 (1)

Covariant symmetrization preserves average success.  The symmetrized
conclusive operator commutes with the group action and has support

    supp(K) = direct_sum_nu V_nu tensor S_nu.

Writing ``ell_nu=dim(S_nu)`` and ``d_max=max_nu dim(V_nu)``, equation (1)
implies

    sum_nu ell_nu / r >= p_id M / d_max.                 (2)

For fixed-point-free involutions in ``S_n``, ``M=(n-1)!!``.  The
Aggarwal--Elboim asymptotic

    d_max(S_n)=sqrt(n!) exp(-(d+o(1))sqrt(n)), d>0

and ``M/sqrt(n!)=Theta(n^-1/4)`` show that every covariant measurement with
``p_id>=n^-a`` has normalized multiplicity width
``exp(Omega(sqrt(n)))`` for fixed ``a``.

This rules out polynomial explicit multiplicity-mode catalogs, bounded-mode
ansatze, and sparse tables as complete exact-identification measurements.  It
is not a gate, time, memory, or qubit lower bound: exponentially many modes
can be manipulated implicitly on polynomially many qubits.  A fused polar
isometry or another structured collective circuit remains possible.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_measurement_copy_width_whitening_tradeoff import (
    _regular_involution_states,
)
from coset_whitening_rank_sandwich_no_go import (
    MAXIMAL_DIMENSION_PAPER_ID,
    MAXIMAL_DIMENSION_PAPER_URL,
    maximum_irrep_dimension,
)
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from symmetric_character import symmetric_character
from symmetric_marked_class_contraction import cycle_type


REPORT_PATH = Path(
    "research/representation/"
    "coset_covariant_measurement_multiplicity_width_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-COVARIANT-MEASUREMENT-MULTIPLICITY-WIDTH-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]


@dataclass(frozen=True)
class FiniteCovariantMeasurementWidthControl:
    degree: int
    copy_count: int
    hidden_hypothesis_count: int
    input_support_rank: int
    conclusive_support_rank: int
    pgm_success_probability: float
    success_forced_support_rank_lower_bound: float
    maximum_irrep_dimension: int
    exact_multiplicity_mode_count: int
    success_forced_multiplicity_mode_lower_bound: float
    support_rank_decomposition_residual: int
    multiplicity_divisibility_failure_count: int
    covariance_commutator_residual: float
    pgm_completeness_residual: float
    support_dimension_bound_verified: bool
    multiplicity_width_bound_verified: bool
    theorem_control_passed: bool
    status: str


@dataclass(frozen=True)
class CovariantMeasurementWidthScalingRecord:
    n: int
    success_requirement_id: str
    target_success_probability: float
    target_success_polynomial_exponent: int | None
    perfect_matching_count_decimal: str
    maximum_irrep_partition: tuple[int, ...]
    maximum_irrep_dimension_decimal: str
    normalized_multiplicity_mode_lower_bound: float
    log2_normalized_multiplicity_mode_lower_bound: float
    polynomial_explicit_mode_catalog_possible_asymptotically: bool
    polynomial_gate_lower_bound_proved: bool
    polynomial_qubit_lower_bound_proved: bool
    status: str


@dataclass(frozen=True)
class CovariantMeasurementMultiplicityWidthTheorem:
    conclusive_trace_bound: str
    covariance_reduction: str
    isotypic_support_decomposition: str
    multiplicity_width_bound: str
    perfect_matching_asymptotic: str
    route_consequence: str
    scope_limit: str
    arbitrary_povm_support_rank_bound_proved: bool
    covariant_symmetrization_preserves_success_proved: bool
    exp_sqrt_multiplicity_width_for_inverse_polynomial_success_proved: bool
    polynomial_explicit_mode_catalog_possible: bool
    fused_polar_isometry_ruled_out: bool
    polynomial_gate_lower_bound_proved: bool
    polynomial_qubit_lower_bound_proved: bool
    decision_problem_lower_bound_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CosetCovariantMeasurementMultiplicityWidthReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[FiniteCovariantMeasurementWidthControl]
    scaling_records: list[CovariantMeasurementWidthScalingRecord]
    theorem: CovariantMeasurementMultiplicityWidthTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def multiplicity_width_lower_bound(
    hidden_count: int,
    maximum_irrep_dimension: int,
    success_probability: float,
) -> float:
    if hidden_count < 2:
        raise ValueError("hidden_count must be at least two")
    if maximum_irrep_dimension < 1:
        raise ValueError("maximum_irrep_dimension must be positive")
    if not 0.0 < success_probability <= 1.0:
        raise ValueError("success_probability must lie in (0,1]")
    return success_probability * hidden_count / maximum_irrep_dimension


def _compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(len(left)))


def _inverse(permutation: Permutation) -> Permutation:
    output = [0] * len(permutation)
    for source, target in enumerate(permutation):
        output[target] = source
    return tuple(output)


def _tensor_power(matrix: np.ndarray, copy_count: int) -> np.ndarray:
    result = matrix
    for _ in range(copy_count - 1):
        result = np.kron(result, matrix)

    return result


def _conjugation_actions(
    degree: int,
    copy_count: int,
) -> tuple[tuple[Permutation, ...], dict[Permutation, np.ndarray]]:
    group = tuple(itertools.permutations(range(degree)))
    index = {element: position for position, element in enumerate(group)}
    actions: dict[Permutation, np.ndarray] = {}
    for group_element in group:
        inverse = _inverse(group_element)
        one_copy = np.zeros((len(group), len(group)))
        for column, element in enumerate(group):
            conjugate = _compose(_compose(group_element, element), inverse)
            one_copy[index[conjugate], column] = 1.0
        actions[group_element] = _tensor_power(one_copy, copy_count)
    return group, actions


def _support_and_inverse_root(
    matrix: np.ndarray,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray, int]:
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2)
    positive = values > tolerance
    support_vectors = vectors[:, positive]
    support = support_vectors @ support_vectors.conj().T
    inverse_root = (
        support_vectors * values[positive] ** -0.5
    ) @ support_vectors.conj().T
    return support, inverse_root, int(np.count_nonzero(positive))


def audit_finite_covariant_measurement_width(
    degree: int,
    copy_count: int,
    *,
    tolerance: float = 1e-9,
) -> FiniteCovariantMeasurementWidthControl:
    """Decompose the exact regular-coset PGM conclusive support."""

    if degree < 3:
        raise ValueError("degree must be at least three")
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    states = _regular_involution_states(degree, copy_count)
    hidden_count = len(states)
    input_rank = int(np.linalg.matrix_rank(states[0], tol=tolerance))
    average = sum(states) / hidden_count
    support, inverse_root, support_rank = _support_and_inverse_root(
        average, tolerance
    )
    effects = tuple(
        inverse_root @ (state / hidden_count) @ inverse_root
        for state in states
    )
    conclusive = sum(effects)
    completeness_residual = float(
        np.linalg.norm(conclusive - support, ord=2)
    )
    success = sum(
        float(np.trace(effect @ state).real)
        for effect, state in zip(effects, states)
    ) / hidden_count

    group, actions = _conjugation_actions(degree, copy_count)
    covariance_residual = max(
        float(np.linalg.norm(action @ support - support @ action, ord=2))
        for action in actions.values()
    )
    decomposed_rank = 0
    mode_count = 0
    divisibility_failures = 0
    dimensions = []
    for partition in integer_partitions(degree):
        dimension = hook_length_dimension(partition)
        dimensions.append(dimension)
        central = sum(
            symmetric_character(partition, cycle_type(element))
            * actions[element]
            for element in group
        ) * (dimension / math.factorial(degree))
        central = (central + central.conj().T) / 2
        block_rank = int(
            np.linalg.matrix_rank(central @ support @ central, tol=tolerance)
        )
        decomposed_rank += block_rank
        if block_rank % dimension:
            divisibility_failures += 1
        mode_count += block_rank // dimension

    maximum_dimension = max(dimensions)
    support_lower = success * hidden_count * input_rank
    mode_lower = support_lower / maximum_dimension
    support_verified = support_rank + 1e-8 >= support_lower
    width_verified = mode_count + 1e-8 >= mode_lower
    decomposition_residual = abs(decomposed_rank - support_rank)
    passed = bool(
        completeness_residual <= 1e-8
        and covariance_residual <= 1e-8
        and divisibility_failures == 0
        and decomposition_residual == 0
        and support_verified
        and width_verified
    )
    return FiniteCovariantMeasurementWidthControl(
        degree=degree,
        copy_count=copy_count,
        hidden_hypothesis_count=hidden_count,
        input_support_rank=input_rank,
        conclusive_support_rank=support_rank,
        pgm_success_probability=success,
        success_forced_support_rank_lower_bound=support_lower,
        maximum_irrep_dimension=maximum_dimension,
        exact_multiplicity_mode_count=mode_count,
        success_forced_multiplicity_mode_lower_bound=mode_lower,
        support_rank_decomposition_residual=decomposition_residual,
        multiplicity_divisibility_failure_count=divisibility_failures,
        covariance_commutator_residual=covariance_residual,
        pgm_completeness_residual=completeness_residual,
        support_dimension_bound_verified=support_verified,
        multiplicity_width_bound_verified=width_verified,
        theorem_control_passed=passed,
        status=(
            "covariant-measurement-multiplicity-width-control-passed"
            if passed
            else "covariant-measurement-multiplicity-width-control-failed"
        ),
    )


def covariant_measurement_width_scaling_record(
    n: int,
    *,
    success_requirement_id: str,
    target_success_probability: float,
    polynomial_exponent: int | None,
) -> CovariantMeasurementWidthScalingRecord:
    if n < 4 or n % 2:
        raise ValueError("n must be even and at least four")
    hidden_count = math.factorial(n) // (
        (2 ** (n // 2)) * math.factorial(n // 2)
    )
    partition, maximum = maximum_irrep_dimension(n)
    lower = multiplicity_width_lower_bound(
        hidden_count, maximum, target_success_probability
    )
    return CovariantMeasurementWidthScalingRecord(
        n=n,
        success_requirement_id=success_requirement_id,
        target_success_probability=target_success_probability,
        target_success_polynomial_exponent=polynomial_exponent,
        perfect_matching_count_decimal=str(hidden_count),
        maximum_irrep_partition=partition,
        maximum_irrep_dimension_decimal=str(maximum),
        normalized_multiplicity_mode_lower_bound=lower,
        log2_normalized_multiplicity_mode_lower_bound=math.log2(lower),
        polynomial_explicit_mode_catalog_possible_asymptotically=False,
        polynomial_gate_lower_bound_proved=False,
        polynomial_qubit_lower_bound_proved=False,
        status=(
            "inverse-polynomial-success-forces-exp-sqrt-multiplicity-width"
            if polynomial_exponent is not None
            else "bounded-error-success-forces-exp-sqrt-multiplicity-width"
        ),
    )


def build_coset_covariant_measurement_multiplicity_width_report(
    *,
    finite_copy_counts: tuple[int, ...] = (1, 2),
    scaling_n_values: tuple[int, ...] = (8, 10, 12, 16, 20, 24, 28, 32),
) -> CosetCovariantMeasurementMultiplicityWidthReport:
    finite = [
        audit_finite_covariant_measurement_width(3, copy_count)
        for copy_count in finite_copy_counts
    ]
    requirements = (
        ("bounded-error-two-thirds", 2.0 / 3.0, None),
        ("inverse-linear", None, 1),
        ("inverse-quadratic", None, 2),
    )
    scaling: list[CovariantMeasurementWidthScalingRecord] = []
    for n in scaling_n_values:
        for requirement_id, constant, exponent in requirements:
            target = constant if constant is not None else n ** (-int(exponent))
            scaling.append(
                covariant_measurement_width_scaling_record(
                    n,
                    success_requirement_id=requirement_id,
                    target_success_probability=target,
                    polynomial_exponent=exponent,
                )
            )
    verified = all(row.theorem_control_passed for row in finite)
    theorem = CovariantMeasurementMultiplicityWidthTheorem(
        conclusive_trace_bound=(
            "For K=sum_h E_h<=I, p_id<=Tr(K)/(M r)<=rank(K)/(M r)."
        ),
        covariance_reduction=(
            "Uniform orbit symmetrization preserves average success and makes "
            "the conclusive operator commute with the group action."
        ),
        isotypic_support_decomposition=(
            "supp(K)=direct_sum_nu V_nu tensor S_nu, so "
            "rank(K)=sum_nu d_nu ell_nu."
        ),
        multiplicity_width_bound=(
            "sum_nu ell_nu/r >= p_id M/d_max for every covariant conclusive POVM."
        ),
        perfect_matching_asymptotic=(
            "For M=(n-1)!! and p>=n^-a, M p/d_max(S_n)="
            "exp(Omega(sqrt(n))) for every fixed a."
        ),
        route_consequence=(
            "Polynomial explicit multiplicity catalogs and bounded-mode sparse "
            "ansatze cannot realize inverse-polynomial-success exact identification."
        ),
        scope_limit=(
            "Multiplicity mode count is not gate complexity, memory, or qubit "
            "complexity; implicit fused transforms remain open."
        ),
        arbitrary_povm_support_rank_bound_proved=True,
        covariant_symmetrization_preserves_success_proved=True,
        exp_sqrt_multiplicity_width_for_inverse_polynomial_success_proved=True,
        polynomial_explicit_mode_catalog_possible=False,
        fused_polar_isometry_ruled_out=False,
        polynomial_gate_lower_bound_proved=False,
        polynomial_qubit_lower_bound_proved=False,
        decision_problem_lower_bound_proved=False,
        theorem_verified=verified,
        status=(
            "exp-sqrt-covariant-measurement-multiplicity-width-proved"
            if verified
            else "covariant-measurement-width-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_covariant_measurement_control_count": len(finite),
        "finite_control_failure_count": sum(
            not row.theorem_control_passed for row in finite
        ),
        "scaling_record_count": len(scaling),
        "arbitrary_povm_support_rank_theorem_count": 1,
        "covariant_multiplicity_width_theorem_count": 1,
        "exp_sqrt_multiplicity_width_theorem_count": 1,
        "maximum_finite_normalized_mode_lower_bound": max(
            row.normalized_multiplicity_mode_lower_bound for row in scaling
        ),
        "polynomial_explicit_mode_catalog_count": 0,
        "fused_polar_isometry_lower_bound_count": 0,
        "polynomial_gate_lower_bound_count": 0,
        "polynomial_qubit_lower_bound_count": 0,
        "decision_problem_lower_bound_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return CosetCovariantMeasurementMultiplicityWidthReport(
        created_at=utc_now(),
        theorem_contract={
            "ensemble": (
                "Uniform fixed-point-free involution orbit in S_n with "
                "equal-rank regular coset-state projectors."
            ),
            "measurement": (
                "Any exact-label POVM may first be symmetrized; a failure "
                "outcome is allowed."
            ),
            "width_measure": (
                "Sum of multiplicity-support dimensions of the invariant "
                "conclusive operator, normalized by input projector rank."
            ),
            "non_claim": (
                "No gate/qubit lower bound and no decision-only reduction theorem."
            ),
        },
        finite_controls=finite,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-IMPLICIT-WIDE-POLAR",
                "statement": (
                    "Determine whether the exp(sqrt(n))-wide multiplicity "
                    "support admits an implicit polynomial fused polar transform."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-MODE-WIDTH-TO-CIRCUIT",
                "statement": (
                    "Prove a valid access-model lower bound before interpreting "
                    "mode width as circuit complexity."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-DECISION-WIDTH-TRANSFER",
                "statement": (
                    "Establish whether worst-case decision reductions require "
                    "exact hidden-involution identification."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "A noncovariant POVM can have smaller support.",
                "answer": (
                    "Orbit symmetrization preserves average success and gives a "
                    "covariant normal form, but the theorem does not claim the "
                    "original circuit explicitly occupies the symmetrized support."
                ),
                "resolved": True,
            },
            {
                "challenge": "Exponentially many modes require exponential qubits.",
                "answer": (
                    "False. Their labels need only logarithmically many qubits; "
                    "the theorem rules out explicit sparse enumeration, not implicit access."
                ),
                "resolved": True,
            },
            {
                "challenge": "The bound assumes the PGM.",
                "answer": (
                    "False. It uses only positivity, POVM completeness, covariance "
                    "normal form, and representation dimensions."
                ),
                "resolved": True,
            },
            {
                "challenge": "Finite S_3 mode counts prove the asymptotic.",
                "answer": (
                    "False. The asymptotic uses the cited maximal-dimension theorem; "
                    "finite controls verify only the exact decomposition identities."
                ),
                "resolved": True,
            },
        ],
        literature_links=[
            {
                "paper_id": MAXIMAL_DIMENSION_PAPER_ID,
                "title": (
                    "On the maximal dimension of an irreducible representation "
                    "of the symmetric group"
                ),
                "url": MAXIMAL_DIMENSION_PAPER_URL,
                "use": (
                    "Converts the exact pM/d_max width lower bound into "
                    "exp(Omega(sqrt(n)))."
                ),
                "external_theorem_not_reproved_here": True,
            }
        ],
        headline_metrics=metrics,
        claim_gate={
            "exp_sqrt_covariant_multiplicity_width_proved": True,
            "polynomial_explicit_multiplicity_catalog_possible": False,
            "bounded_mode_sparse_measurement_ansatz_possible": False,
            "implicit_fused_polar_transform_ruled_out": False,
            "polynomial_hidden_involution_decoder_proved": False,
            "polynomial_gate_lower_bound_proved": False,
            "polynomial_qubit_lower_bound_proved": False,
            "decision_problem_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Every covariant inverse-polynomial-success exact-label POVM "
                "has exp(Omega(sqrt(n))) normalized multiplicity width. This "
                "kills sparse explicit mode catalogs but leaves implicit fused "
                "transforms and structured collective circuits open."
            ),
        },
        status=(
            "sparse-multiplicity-measurements-closed-"
            "implicit-wide-polar-open"
        ),
        summary=(
            "Proved an exp(Omega(sqrt(n))) multiplicity-width requirement for "
            "every covariant inverse-polynomial-success exact-involution POVM. "
            "Sparse explicit mode representations are closed; circuit complexity "
            "and implicit fused polar implementations remain open."
        ),
        falsifiers_triggered=[
            (
                "A polynomial catalog of multiplicity modes cannot support an "
                "inverse-polynomial-success covariant exact-label measurement."
            ),
            (
                "The multiplicity-width obstruction is not specific to the PGM."
            ),
            (
                "Mode count alone cannot be promoted to a gate, memory, qubit, "
                "decision-problem, or general quantum lower bound."
            ),
        ],
    )


def write_coset_covariant_measurement_multiplicity_width_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-COSET-COVARIANT-MEASUREMENT-MULTIPLICITY-WIDTH-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(
        build_coset_covariant_measurement_multiplicity_width_report(**kwargs)
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        _res_payload = report if "report" in locals() else (payload if "payload" in locals() else (result if "result" in locals() else output))
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG--COVARIANT-MEASUREMENT-MULTIPLICITY-WIDTH-NO-GO",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-COSET-COVARIANT-MEASUREMENT-MULTIPLICITY-WIDTH-NO-GO."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-COSET-COVARIANT-MEASUREMENT-MULTIPLICITY-WIDTH-NO-GO."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=_res_payload.get("headline_metrics", {}),
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
                created_at=_res_payload.get("created_at", ""),
                status=_res_payload.get("status", "completed"),
                summary=_res_payload.get("summary", ""),
                metrics=_res_payload.get("headline_metrics", {}),
                falsifiers_triggered=_res_payload.get("falsifiers_triggered", []),
                artifacts={
                    "coset_covariant_measurement_multiplicity_width_no_go": str(path)
                },
            )
        )

    return payload


if __name__ == "__main__":
    report = write_coset_covariant_measurement_multiplicity_width_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
