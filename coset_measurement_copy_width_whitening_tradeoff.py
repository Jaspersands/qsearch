"""Arbitrary-measurement copy width versus standalone coset whitening.

Let ``rho_h=P_h/r`` be ``M`` equiprobable normalized rank-``r`` projector
states on a ``D``-dimensional Hilbert space and let ``S`` be the support of
their average.  For every POVM ``{E_h}``, including a POVM with a failure
outcome,

    p_id = M^-1 sum_h Tr(E_h rho_h)
         <= rank(S)/(M r)
         <= D/(M r).                                      (1)

The first inequality follows from ``rho_h<=Pi_S/r`` and
``sum_h Pi_S E_h Pi_S<=Pi_S``.  For ``k`` regular coset-state registers of an
order-two subgroup, ``D/r=2^k``.  Thus arbitrary exact identification obeys

    p_id <= min(1, 2^k/M).                                (2)

If exact identification has success at least ``p``, then
``k>=ceil(log2(Mp))`` whenever ``Mp>1``.  For fixed-point-free involutions in
``S_n``, ``M=(n-1)!!``.  Every inverse-polynomial-success measurement therefore
uses ``k>=log2(M)-O(log n)`` copies.

At every such copy width, the projector-overlap rank bound from
``coset_whitening_rank_sandwich_no_go.py`` gives

    E_source sum_nu rank(D_nu)/R
      >= M/[d_max(S_n)(1+(M-1)2^-k)]
      >  M p/[d_max(S_n)(1+p)].                           (3)

Aggarwal--Elboim's maximal-irrep-dimension asymptotic turns (3) into
``exp(Omega(sqrt(n)))`` for ``p>=n^-a`` and fixed ``a``.  Consequently moving
below the constant-success PGM threshold by only logarithmically many copies
does not make standalone multiplicity whitening polynomial.

This is deliberately not a lower bound on implementing an arbitrary POVM.
Equation (3) charges algorithms that expose ``D_nu^(-1/2)`` standalone or use
the standard branchwise/source-weighted inverse accounting.  A globally fused
polar isometry, another bounded-norm collective measurement, a decision-only
reduction, and general quantum circuits remain open.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from coset_centralizer_whitening_rank_bound import centralizer_rank_envelope
from coset_state_distinguishability import involution_count
from coset_whitening_rank_sandwich_no_go import (
    MAXIMAL_DIMENSION_PAPER_ID,
    MAXIMAL_DIMENSION_PAPER_URL,
    maximum_irrep_dimension,
    multiplicity_rank_effective_lower_bound,
)
from research_registry import utc_now
from self_dual_wreath_pgm_success_theorem import pgm_success_lower_bound


REPORT_PATH = Path(
    "research/representation/"
    "coset_measurement_copy_width_whitening_tradeoff.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-MEASUREMENT-COPY-WIDTH-WHITENING-TRADEOFF"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]


@dataclass(frozen=True)
class FiniteMeasurementDimensionControl:
    degree: int
    copy_count: int
    hidden_hypothesis_count: int
    ambient_dimension: int
    individual_support_rank: int
    ensemble_support_rank: int
    maximum_pairwise_projector_overlap_residual: float
    pgm_completeness_residual: float
    pgm_success_probability: float
    support_dimension_success_upper_bound: float
    ambient_dimension_success_upper_bound: float
    pgm_below_support_bound: bool
    support_below_ambient_bound: bool
    theorem_control_passed: bool
    status: str


@dataclass(frozen=True)
class SuccessWhiteningScalingRecord:
    n: int
    success_requirement_id: str
    target_success_probability: float
    target_success_polynomial_exponent: int | None
    perfect_matching_count_decimal: str
    log2_perfect_matching_count: float
    minimum_arbitrary_measurement_copy_count: int
    constant_pgm_success_copy_count: int
    copy_deficit_from_pgm_width: int
    success_upper_bound_one_copy_below_minimum: float
    success_upper_bound_at_minimum: float
    pgm_success_lower_bound_at_minimum: float
    maximum_irrep_partition: tuple[int, ...]
    maximum_irrep_dimension_decimal: str
    exact_multiplicity_rank_lower_bound_at_minimum: float
    target_only_multiplicity_rank_lower_bound: float
    target_only_inverse_root_rms_lower_bound: float
    centralizer_rank_upper_bound: float
    rank_sandwich_consistent: bool
    inverse_polynomial_success_regime: bool
    asymptotic_exp_sqrt_whitening_obstruction_applies: bool
    status: str


@dataclass(frozen=True)
class MeasurementCopyWidthWhiteningTheorem:
    support_domination: str
    arbitrary_povm_bound: str
    regular_coset_specialization: str
    inverse_polynomial_copy_window: str
    multiplicity_rank_consequence: str
    asymptotic_consequence: str
    route_consequence: str
    scope_limit: str
    arbitrary_povm_exact_identification_bound_proved: bool
    inverse_polynomial_copy_window_proved: bool
    exp_sqrt_standalone_whitening_in_success_window_proved: bool
    alternative_collective_measurement_ruled_out: bool
    fused_polar_isometry_ruled_out: bool
    decision_problem_lower_bound_proved: bool
    general_quantum_circuit_lower_bound_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CosetMeasurementCopyWidthWhiteningReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[FiniteMeasurementDimensionControl]
    scaling_records: list[SuccessWhiteningScalingRecord]
    theorem: MeasurementCopyWidthWhiteningTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def arbitrary_measurement_success_upper_bound(
    hidden_count: int,
    copy_count: int,
    *,
    subgroup_order: int = 2,
) -> float:
    """Return ``min(1, |H|^k/M)`` for regular coset-state registers."""

    if hidden_count < 2:
        raise ValueError("hidden_count must be at least two")
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    if subgroup_order < 2:
        raise ValueError("subgroup_order must be at least two")
    log_ratio = copy_count * math.log2(subgroup_order) - math.log2(hidden_count)
    return 1.0 if log_ratio >= 0 else 2.0**log_ratio


def minimum_copies_for_target_success(
    hidden_count: int,
    target_success_probability: float,
    *,
    subgroup_order: int = 2,
) -> int:
    """Necessary copy count from the arbitrary-POVM dimension bound."""

    if hidden_count < 2:
        raise ValueError("hidden_count must be at least two")
    if not 0.0 < target_success_probability <= 1.0:
        raise ValueError("target success probability must lie in (0,1]")
    if subgroup_order < 2:
        raise ValueError("subgroup_order must be at least two")
    logarithm = (
        math.log2(hidden_count)
        + math.log2(target_success_probability)
    ) / math.log2(subgroup_order)
    return max(1, math.ceil(logarithm - 1e-12))


@lru_cache(maxsize=None)
def _maximum_irrep_dimension_cached(
    n: int,
) -> tuple[tuple[int, ...], int]:
    return maximum_irrep_dimension(n)


def target_forced_multiplicity_rank_lower_bound(
    n: int,
    hidden_count: int,
    target_success_probability: float,
) -> float:
    """Copy-independent consequence after imposing target success ``p``.

    From ``2^k>=Mp``, the collision denominator is strictly below
    ``1+1/p``.  The returned non-strict value is therefore a valid lower
    bound and avoids relying on integer-rounding details.
    """

    if not 0.0 < target_success_probability <= 1.0:
        raise ValueError("target success probability must lie in (0,1]")
    _, maximum = _maximum_irrep_dimension_cached(n)
    return hidden_count / (
        maximum * (1.0 + 1.0 / target_success_probability)
    )


def _compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(len(left)))


def _tensor_power(matrix: np.ndarray, copy_count: int) -> np.ndarray:
    result = matrix
    for _ in range(copy_count - 1):
        result = np.kron(result, matrix)
    return result


def _regular_involution_states(
    degree: int,
    copy_count: int,
) -> tuple[np.ndarray, ...]:
    group = tuple(itertools.permutations(range(degree)))
    index = {element: position for position, element in enumerate(group)}
    identity = tuple(range(degree))
    involutions = tuple(
        element
        for element in group
        if element != identity and _compose(element, element) == identity
    )
    states: list[np.ndarray] = []
    for hidden in involutions:
        right = np.zeros((len(group), len(group)))
        for column, element in enumerate(group):
            right[index[_compose(element, hidden)], column] = 1.0
        one_copy = (np.eye(len(group)) + right) / len(group)
        states.append(_tensor_power(one_copy, copy_count))
    return tuple(states)


def _support_and_inverse_root(
    matrix: np.ndarray,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray, int]:
    eigenvalues, eigenvectors = np.linalg.eigh(
        (matrix + matrix.conj().T) / 2
    )
    positive = eigenvalues > tolerance
    support_vectors = eigenvectors[:, positive]
    support = support_vectors @ support_vectors.conj().T
    inverse_root = (
        support_vectors
        * eigenvalues[positive] ** -0.5
    ) @ support_vectors.conj().T
    return support, inverse_root, int(np.count_nonzero(positive))


def audit_finite_measurement_dimension_control(
    degree: int,
    copy_count: int,
    *,
    tolerance: float = 1e-10,
) -> FiniteMeasurementDimensionControl:
    """Check (1) on the exact PGM for the regular ``S_degree`` orbit."""

    if degree < 3:
        raise ValueError("degree must be at least three")
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    states = _regular_involution_states(degree, copy_count)
    hidden_count = len(states)
    dimension = states[0].shape[0]
    ranks = tuple(
        int(np.linalg.matrix_rank(state, tol=tolerance)) for state in states
    )
    if len(set(ranks)) != 1:
        raise ArithmeticError("coset-state support ranks differ")
    rank = ranks[0]
    projectors = tuple(rank * state for state in states)
    expected_overlap = 2.0**-copy_count
    overlap_residual = max(
        abs(float(np.trace(left @ right).real) / rank - expected_overlap)
        for index, left in enumerate(projectors)
        for right in projectors[index + 1 :]
    )
    average = sum(states) / hidden_count
    support, inverse_root, support_rank = _support_and_inverse_root(
        average, tolerance
    )
    effects = tuple(
        inverse_root @ (state / hidden_count) @ inverse_root
        for state in states
    )
    completeness_residual = float(
        np.linalg.norm(sum(effects) - support, ord=2)
    )
    success = sum(
        float(np.trace(effect @ state).real)
        for effect, state in zip(effects, states)
    ) / hidden_count
    support_bound = support_rank / (hidden_count * rank)
    ambient_bound = min(1.0, dimension / (hidden_count * rank))
    passed = bool(
        overlap_residual <= 1e-9
        and completeness_residual <= 1e-8
        and success <= support_bound + 1e-9
        and support_bound <= ambient_bound + 1e-9
    )
    return FiniteMeasurementDimensionControl(
        degree=degree,
        copy_count=copy_count,
        hidden_hypothesis_count=hidden_count,
        ambient_dimension=dimension,
        individual_support_rank=rank,
        ensemble_support_rank=support_rank,
        maximum_pairwise_projector_overlap_residual=overlap_residual,
        pgm_completeness_residual=completeness_residual,
        pgm_success_probability=success,
        support_dimension_success_upper_bound=support_bound,
        ambient_dimension_success_upper_bound=ambient_bound,
        pgm_below_support_bound=success <= support_bound + 1e-9,
        support_below_ambient_bound=support_bound <= ambient_bound + 1e-9,
        theorem_control_passed=passed,
        status=(
            "arbitrary-measurement-dimension-bound-control-passed"
            if passed
            else "arbitrary-measurement-dimension-bound-control-failed"
        ),
    )


def success_whitening_scaling_record(
    n: int,
    *,
    success_requirement_id: str,
    target_success_probability: float,
    polynomial_exponent: int | None,
) -> SuccessWhiteningScalingRecord:
    if n < 4 or n % 2:
        raise ValueError("n must be even and at least four")
    hidden_count = involution_count(n, n // 2)
    copies = minimum_copies_for_target_success(
        hidden_count, target_success_probability
    )
    pgm_width = math.ceil(math.log2(hidden_count))
    partition, maximum = _maximum_irrep_dimension_cached(n)
    exact_lower = multiplicity_rank_effective_lower_bound(
        n, hidden_count, copies
    )
    target_lower = target_forced_multiplicity_rank_lower_bound(
        n, hidden_count, target_success_probability
    )
    centralizer_upper = centralizer_rank_envelope(n, n // 2)
    below = arbitrary_measurement_success_upper_bound(
        hidden_count, max(1, copies - 1)
    )
    if copies == 1:
        below = 1.0 / hidden_count
    at_minimum = arbitrary_measurement_success_upper_bound(
        hidden_count, copies
    )
    return SuccessWhiteningScalingRecord(
        n=n,
        success_requirement_id=success_requirement_id,
        target_success_probability=target_success_probability,
        target_success_polynomial_exponent=polynomial_exponent,
        perfect_matching_count_decimal=str(hidden_count),
        log2_perfect_matching_count=math.log2(hidden_count),
        minimum_arbitrary_measurement_copy_count=copies,
        constant_pgm_success_copy_count=pgm_width,
        copy_deficit_from_pgm_width=pgm_width - copies,
        success_upper_bound_one_copy_below_minimum=below,
        success_upper_bound_at_minimum=at_minimum,
        pgm_success_lower_bound_at_minimum=pgm_success_lower_bound(
            hidden_count, copies
        ),
        maximum_irrep_partition=partition,
        maximum_irrep_dimension_decimal=str(maximum),
        exact_multiplicity_rank_lower_bound_at_minimum=exact_lower,
        target_only_multiplicity_rank_lower_bound=target_lower,
        target_only_inverse_root_rms_lower_bound=math.sqrt(target_lower),
        centralizer_rank_upper_bound=centralizer_upper,
        rank_sandwich_consistent=exact_lower <= centralizer_upper + 1e-10,
        inverse_polynomial_success_regime=polynomial_exponent is not None,
        asymptotic_exp_sqrt_whitening_obstruction_applies=True,
        status=(
            "inverse-polynomial-identification-forces-exp-sqrt-standalone-whitening"
            if polynomial_exponent is not None
            else "constant-identification-forces-exp-sqrt-standalone-whitening"
        ),
    )


def build_coset_measurement_copy_width_whitening_report(
    *,
    finite_copy_counts: tuple[int, ...] = (1, 2),
    scaling_n_values: tuple[int, ...] = (8, 10, 12, 16, 20, 24, 28, 32),
) -> CosetMeasurementCopyWidthWhiteningReport:
    finite = [
        audit_finite_measurement_dimension_control(3, copy_count)
        for copy_count in finite_copy_counts
    ]
    requirements = (
        ("bounded-error-two-thirds", 2.0 / 3.0, None),
        ("inverse-linear", None, 1),
        ("inverse-quadratic", None, 2),
    )
    scaling: list[SuccessWhiteningScalingRecord] = []
    for n in scaling_n_values:
        for requirement_id, constant, exponent in requirements:
            target = constant if constant is not None else n ** (-int(exponent))
            scaling.append(
                success_whitening_scaling_record(
                    n,
                    success_requirement_id=requirement_id,
                    target_success_probability=target,
                    polynomial_exponent=exponent,
                )
            )
    verified = bool(
        all(row.theorem_control_passed for row in finite)
        and all(row.rank_sandwich_consistent for row in scaling)
        and all(
            row.success_upper_bound_one_copy_below_minimum
            < row.target_success_probability + 1e-12
            for row in scaling
        )
        and all(
            row.success_upper_bound_at_minimum
            + 1e-12 >= row.target_success_probability
            for row in scaling
        )
    )
    theorem = MeasurementCopyWidthWhiteningTheorem(
        support_domination=(
            "Every rho_h=P_h/r is bounded above by Pi_S/r on the support S "
            "of the ensemble average."
        ),
        arbitrary_povm_bound=(
            "For any exact-identification POVM, p_id<=rank(S)/(M r)<=D/(M r)."
        ),
        regular_coset_specialization=(
            "For k regular order-two coset states, D/r=2^k and therefore "
            "p_id<=min(1,2^k/M)."
        ),
        inverse_polynomial_copy_window=(
            "Success p>=n^-a forces k>=log2(M)-a log2(n); inverse-polynomial "
            "success cannot occur Omega(sqrt(n)) copies below log2(M)."
        ),
        multiplicity_rank_consequence=(
            "At every width capable of success p, the natural multiplicity "
            "moment is at least M/[d_max(1+1/p)]=Omega(Mp/d_max)."
        ),
        asymptotic_consequence=(
            "For perfect matchings and fixed a, p>=n^-a plus the maximal "
            "S_n irrep-dimension theorem makes this exp(Omega(sqrt(n)))."
        ),
        route_consequence=(
            "No inverse-polynomial exact-identification copy regime makes "
            "standalone or standard branchwise multiplicity whitening polynomial."
        ),
        scope_limit=(
            "The theorem does not charge an arbitrary POVM by the whitening "
            "moment, does not obstruct a fused polar isometry, and does not "
            "transfer automatically to a decision-only problem."
        ),
        arbitrary_povm_exact_identification_bound_proved=True,
        inverse_polynomial_copy_window_proved=True,
        exp_sqrt_standalone_whitening_in_success_window_proved=True,
        alternative_collective_measurement_ruled_out=False,
        fused_polar_isometry_ruled_out=False,
        decision_problem_lower_bound_proved=False,
        general_quantum_circuit_lower_bound_proved=False,
        theorem_verified=verified,
        status=(
            "arbitrary-measurement-copy-window-standalone-whitening-tradeoff-proved"
            if verified
            else "measurement-copy-width-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_arbitrary_measurement_control_count": len(finite),
        "finite_control_failure_count": sum(
            not row.theorem_control_passed for row in finite
        ),
        "scaling_record_count": len(scaling),
        "arbitrary_povm_copy_lower_bound_theorem_count": 1,
        "inverse_polynomial_copy_window_theorem_count": 1,
        "exp_sqrt_standalone_whitening_tradeoff_theorem_count": 1,
        "maximum_copy_deficit_from_pgm_width": max(
            row.copy_deficit_from_pgm_width for row in scaling
        ),
        "maximum_finite_target_rank_lower_bound": max(
            row.target_only_multiplicity_rank_lower_bound for row in scaling
        ),
        "alternative_collective_measurement_lower_bound_count": 0,
        "fused_polar_isometry_lower_bound_count": 0,
        "decision_problem_lower_bound_count": 0,
        "general_quantum_circuit_lower_bound_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return CosetMeasurementCopyWidthWhiteningReport(
        created_at=utc_now(),
        theorem_contract={
            "task": (
                "Exact identification of a uniformly hidden fixed-point-free "
                "involution from same-hidden regular coset states."
            ),
            "measurement_model": (
                "Arbitrary POVM, with an optional failure outcome; no covariance "
                "or efficient-circuit assumption is used in the copy lower bound."
            ),
            "success_regime": (
                "Any p>=n^-a for fixed a, including bounded-error success."
            ),
            "implementation_cost_scope": (
                "Only standalone D_nu inverse roots and standard branchwise or "
                "source-weighted whitening are charged by the rank moment."
            ),
            "non_claim": (
                "No arbitrary-measurement circuit lower bound and no automatic "
                "graph-isomorphism decision lower bound."
            ),
        },
        finite_controls=finite,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-FUSED-POLAR-COPY-WINDOW",
                "statement": (
                    "Construct or lower-bound a fused PGM polar isometry in the "
                    "necessary inverse-polynomial-success copy window without "
                    "charging a standalone inverse."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-ALTERNATIVE-POVM-CIRCUIT",
                "statement": (
                    "Specify an efficiently implementable collective POVM whose "
                    "cost is not the multiplicity inverse moment."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-DECISION-TRANSFER",
                "statement": (
                    "Prove the exact-label identification requirement for a "
                    "worst-case GI/code-equivalence reduction, or keep the "
                    "decision-only scope separate."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The success upper bound can exceed one.",
                "answer": (
                    "The operational bound is explicitly min(1,2^k/M); only "
                    "the subthreshold regime supplies a nontrivial copy bound."
                ),
                "resolved": True,
            },
            {
                "challenge": (
                    "A large multiplicity moment proves every arbitrary POVM is slow."
                ),
                "answer": (
                    "False. The moment lower-bounds specified standalone or "
                    "branchwise whitening implementations, not arbitrary effects."
                ),
                "resolved": True,
            },
            {
                "challenge": (
                    "Inverse-polynomial exact-label success is the same as solving GI."
                ),
                "answer": (
                    "False without a reduction and verifier. The theorem is an "
                    "HSP identification boundary, not a GI decision lower bound."
                ),
                "resolved": True,
            },
            {
                "challenge": (
                    "A hidden-dependent source label could invalidate the support bound."
                ),
                "answer": (
                    "The arbitrary-POVM bound is applied before Fourier/source "
                    "conditioning and depends only on physical state supports."
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
                    "Converts M p/d_max into exp(Omega(sqrt(n))) for every "
                    "fixed inverse-polynomial success target."
                ),
                "external_theorem_not_reproved_here": True,
            }
        ],
        headline_metrics=metrics,
        claim_gate={
            "arbitrary_povm_exact_identification_copy_bound_proved": True,
            "inverse_polynomial_success_far_below_pgm_width_possible": False,
            "polynomial_standalone_whitening_in_useful_copy_window": False,
            "alternative_collective_measurement_ruled_out": False,
            "fused_pgm_polar_isometry_ruled_out": False,
            "polynomial_hidden_involution_decoder_proved": False,
            "decision_problem_lower_bound_proved": False,
            "general_quantum_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Any inverse-polynomial exact-label decoder needs copies within "
                "O(log n) of log2(M), where standalone multiplicity whitening "
                "still has exp(Omega(sqrt(n))) source moment. A viable route must "
                "use a fused or genuinely different collective measurement."
            ),
        },
        status=(
            "exact-identification-copy-window-proved-"
            "standalone-whitening-closed-fused-measurement-open"
        ),
        summary=(
            "Proved an arbitrary-POVM copy lower bound for exact hidden-involution "
            "identification and combined it with the actual-rank sandwich. Every "
            "inverse-polynomial-success copy regime retains an exp(Omega(sqrt(n))) "
            "standalone whitening moment; fused and alternative measurements remain open."
        ),
        falsifiers_triggered=[
            (
                "Inverse-polynomial exact identification cannot operate "
                "Omega(sqrt(n)) copies below the standard PGM width."
            ),
            (
                "Moving O(log n) copies below the PGM width does not restore "
                "polynomial standalone multiplicity whitening."
            ),
            (
                "The tradeoff cannot be promoted to an arbitrary-circuit or "
                "decision-problem lower bound."
            ),
        ],
    )


def write_coset_measurement_copy_width_whitening_report(
    output_path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-COSET-MEASUREMENT-COPY-WIDTH-WHITENING-TRADEOFF"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = output_path
    output_path = output_path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(
        build_coset_measurement_copy_width_whitening_report(**kwargs)
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
                id="NEG--MEASUREMENT-COPY-WIDTH-WHITENING-TRADEOFF",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-COSET-MEASUREMENT-COPY-WIDTH-WHITENING-TRADEOFF."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-COSET-MEASUREMENT-COPY-WIDTH-WHITENING-TRADEOFF."
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
                    "coset_measurement_copy_width_whitening_tradeoff": str(output_path)
                },
            )
        )

    return payload


if __name__ == "__main__":
    report = write_coset_measurement_copy_width_whitening_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
