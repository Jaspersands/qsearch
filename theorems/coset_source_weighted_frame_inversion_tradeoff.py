"""Source-weighted obstruction for direct coset-frame inversion.

Let ``{rho_h}`` be an equiprobable ensemble of normalized rank-``R``
projectors, so ``rho_h=P_h/R``, and write

    F = E_h rho_h,                 B = E_h P_h = R F.

``B`` is exactly the normalized projected-LCU operator used by the natural
multi-copy involution frame construction.  Under the spectral source law of
``F``, the inverse-root second moment is

    E_F[(B^(-1/2))^2] = Tr(F B^+) = rank(F) / R.

The same ratio is forced by information.  Since every input state has entropy
``log2 R``, the branch Holevo information is ``chi=S(F)-log2 R`` and

    rank(F) / R >= 2^chi.

With hidden-independent classical source labels ``Z``, Jensen's inequality
gives ``E_Z[rank(F_Z)/R_Z] >= 2^E_Z[chi_Z]``.  Fano therefore makes the direct
source-weighted inverse-root moment superpolynomial whenever the ensemble can
decode one of the fixed-point-free involutions of ``S_n`` with bounded error.

This is deliberately not a circuit lower bound.  It closes only schemes that
materialize the normalized average-frame inverse as a separate nonunitary
primitive, including the obvious source-weighted or branchwise variable-time
repair of the projected-LCU normalization.  A fused PGM polar isometry, a
different factorization, or another collective covariant measurement remains
open.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from itertools import combinations_with_replacement
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from coset_holevo_information import binary_entropy, fano_required_information
from coset_natural_multicopy_pgm_benchmark import (
    _multiset_multiplicity,
    _source_data,
    _tensor_states,
)
from coset_state_distinguishability import involution_count
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_source_weighted_frame_inversion_tradeoff.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-SOURCE-WEIGHTED-FRAME-INVERSION-TRADEOFF"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class UniformProjectorFrameControl:
    control_id: str
    n: int | None
    transposition_count: int | None
    copy_count: int
    source_partitions: tuple[tuple[int, ...], ...]
    natural_source_probability: float
    hidden_hypothesis_count: int
    carrier_dimension: int
    individual_projector_rank: int
    average_frame_support_rank: int
    conditional_holevo_bits: float
    direct_lcu_mean_eigenvalue: float
    generic_mean_scale_inverse_root_factor: float
    source_weighted_inverse_root_second_moment: float
    source_weighted_inverse_root_rms_factor: float
    entropy_forced_second_moment_lower_bound: float
    entropy_rank_bound_residual: float
    hypothesis_span_bound_residual: float
    uniform_projector_residual: float
    source_moment_identity_residual: float
    normalized_frame_spectral_upper_residual: float
    theorem_control_passed: bool
    status: str


@dataclass(frozen=True)
class NaturalSourceAggregate:
    n: int
    transposition_count: int
    copy_count: int
    hidden_hypothesis_count: int
    source_branch_count: int
    total_natural_source_probability: float
    average_conditional_holevo_bits: float
    average_source_weighted_inverse_root_second_moment: float
    global_source_weighted_inverse_root_rms_factor: float
    jensen_second_moment_lower_bound: float
    jensen_bound_residual: float
    bounded_error: float
    fano_required_information_bits: float
    bounded_error_decoding_information_available: bool
    all_finite_controls_passed: bool
    status: str


@dataclass(frozen=True)
class PerfectMatchingScalingRecord:
    n: int
    hidden_hypothesis_count: int
    log2_hidden_hypothesis_count: float
    bounded_error: float
    fano_required_information_bits: float
    fano_forced_log2_direct_inverse_rms: float
    elementary_log2_hypothesis_lower_bound: float
    elementary_log2_direct_inverse_rms_lower_bound: float
    direct_inverse_rms_lower_bound_is_superpolynomial: bool
    asymptotic_status: str


@dataclass(frozen=True)
class SourceWeightedFrameTheorem:
    ensemble: str
    exact_moment_identity: str
    entropy_tradeoff: str
    hidden_independent_source_extension: str
    fano_consequence: str
    perfect_matching_consequence: str
    direct_route_consequence: str
    scope_limit: str
    exact_source_moment_identity_proved: bool
    entropy_rank_tradeoff_proved: bool
    source_averaged_jensen_tradeoff_proved: bool
    bounded_error_direct_inverse_obstruction_proved: bool
    fused_polar_isometry_ruled_out: bool
    arbitrary_collective_measurement_ruled_out: bool
    general_quantum_circuit_lower_bound_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CosetSourceWeightedFrameInversionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[UniformProjectorFrameControl]
    natural_source_aggregates: list[NaturalSourceAggregate]
    scaling_records: list[PerfectMatchingScalingRecord]
    theorem: SourceWeightedFrameTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _entropy_bits(eigenvalues: np.ndarray, tolerance: float) -> float:
    positive = eigenvalues[eigenvalues > tolerance]
    return -float(np.sum(positive * np.log2(positive)))


def audit_uniform_projector_ensemble(
    control_id: str,
    states: Sequence[np.ndarray],
    *,
    copy_count: int = 1,
    source_partitions: tuple[tuple[int, ...], ...] = (),
    natural_source_probability: float = 1.0,
    n: int | None = None,
    transposition_count: int | None = None,
    tolerance: float = 1e-10,
) -> UniformProjectorFrameControl:
    """Verify the source-moment and entropy identities on one finite ensemble."""

    if not states:
        raise ValueError("a nonempty state ensemble is required")
    matrices = tuple(np.asarray(state, dtype=np.complex128) for state in states)
    dimension = matrices[0].shape[0]
    if any(state.shape != (dimension, dimension) for state in matrices):
        raise ValueError("all states must be square matrices of one dimension")

    ranks: list[int] = []
    projector_residual = 0.0
    for state in matrices:
        hermitian = (state + state.conj().T) / 2
        eigenvalues = np.linalg.eigvalsh(hermitian)
        if float(np.min(eigenvalues)) < -tolerance:
            raise ValueError("states must be positive semidefinite")
        if abs(float(np.trace(hermitian).real) - 1.0) > tolerance:
            raise ValueError("states must have unit trace")
        rank = int(np.count_nonzero(eigenvalues > tolerance))
        if rank <= 0:
            raise ValueError("states must have nonempty support")
        ranks.append(rank)
        projector = rank * hermitian
        projector_residual = max(
            projector_residual,
            float(np.linalg.norm(projector @ projector - projector, ord=2)),
        )
    if len(set(ranks)) != 1:
        raise ValueError("all states must have the same projector rank")

    projector_rank = ranks[0]
    average = sum(matrices) / len(matrices)
    average = (average + average.conj().T) / 2
    eigenvalues = np.linalg.eigvalsh(average)
    positive = eigenvalues[eigenvalues > tolerance]
    support_rank = len(positive)
    entropy = _entropy_bits(eigenvalues, tolerance)
    holevo = entropy - math.log2(projector_rank)

    normalized_frame_eigenvalues = projector_rank * positive
    source_moment = float(
        np.sum(positive / normalized_frame_eigenvalues)
    )
    exact_moment = support_rank / projector_rank
    entropy_lower = 2.0**holevo
    mean_eigenvalue = projector_rank / dimension
    generic_factor = math.sqrt(dimension / projector_rank)
    source_rms = math.sqrt(source_moment)
    moment_residual = abs(source_moment - exact_moment)
    entropy_residual = max(0.0, entropy_lower - source_moment)
    span_residual = max(0.0, source_moment - len(matrices))
    spectral_upper_residual = max(
        0.0,
        float(np.max(normalized_frame_eigenvalues, initial=0.0)) - 1.0,
    )
    passed = bool(
        projector_residual <= 5e-9
        and moment_residual <= 1e-10
        and entropy_residual <= 1e-10
        and span_residual <= 1e-10
        and spectral_upper_residual <= 1e-10
    )
    return UniformProjectorFrameControl(
        control_id=control_id,
        n=n,
        transposition_count=transposition_count,
        copy_count=copy_count,
        source_partitions=source_partitions,
        natural_source_probability=natural_source_probability,
        hidden_hypothesis_count=len(matrices),
        carrier_dimension=dimension,
        individual_projector_rank=projector_rank,
        average_frame_support_rank=support_rank,
        conditional_holevo_bits=holevo,
        direct_lcu_mean_eigenvalue=mean_eigenvalue,
        generic_mean_scale_inverse_root_factor=generic_factor,
        source_weighted_inverse_root_second_moment=source_moment,
        source_weighted_inverse_root_rms_factor=source_rms,
        entropy_forced_second_moment_lower_bound=entropy_lower,
        entropy_rank_bound_residual=entropy_residual,
        hypothesis_span_bound_residual=span_residual,
        uniform_projector_residual=projector_residual,
        source_moment_identity_residual=moment_residual,
        normalized_frame_spectral_upper_residual=spectral_upper_residual,
        theorem_control_passed=passed,
        status=(
            "source-weighted-frame-identities-verified"
            if passed
            else "source-weighted-frame-control-failure"
        ),
    )


def natural_source_controls(
    n: int,
    transposition_count: int,
    copy_count: int,
    *,
    bounded_error: float = 1 / 3,
) -> tuple[list[UniformProjectorFrameControl], NaturalSourceAggregate]:
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    partitions, probabilities, state_families = _source_data(
        n, transposition_count
    )
    controls: list[UniformProjectorFrameControl] = []
    for indices in combinations_with_replacement(
        range(len(partitions)), copy_count
    ):
        source_probability = float(_multiset_multiplicity(indices))
        for index in indices:
            source_probability *= probabilities[index]
        source_partitions = tuple(partitions[index] for index in indices)
        states = _tensor_states(
            tuple(state_families[index] for index in indices)
        )
        controls.append(
            audit_uniform_projector_ensemble(
                "source-" + "-".join(".".join(map(str, p)) for p in source_partitions),
                states,
                copy_count=copy_count,
                source_partitions=source_partitions,
                natural_source_probability=source_probability,
                n=n,
                transposition_count=transposition_count,
            )
        )

    source_mass = sum(row.natural_source_probability for row in controls)
    average_holevo = sum(
        row.natural_source_probability * row.conditional_holevo_bits
        for row in controls
    )
    average_moment = sum(
        row.natural_source_probability
        * row.source_weighted_inverse_root_second_moment
        for row in controls
    )
    jensen_lower = 2.0**average_holevo
    jensen_residual = max(0.0, jensen_lower - average_moment)
    hidden_count = controls[0].hidden_hypothesis_count
    required = fano_required_information(
        math.log2(hidden_count), bounded_error
    )
    passed = bool(
        abs(source_mass - 1.0) <= 1e-10
        and jensen_residual <= 1e-10
        and all(row.theorem_control_passed for row in controls)
    )
    aggregate = NaturalSourceAggregate(
        n=n,
        transposition_count=transposition_count,
        copy_count=copy_count,
        hidden_hypothesis_count=hidden_count,
        source_branch_count=len(controls),
        total_natural_source_probability=source_mass,
        average_conditional_holevo_bits=average_holevo,
        average_source_weighted_inverse_root_second_moment=average_moment,
        global_source_weighted_inverse_root_rms_factor=math.sqrt(average_moment),
        jensen_second_moment_lower_bound=jensen_lower,
        jensen_bound_residual=jensen_residual,
        bounded_error=bounded_error,
        fano_required_information_bits=required,
        bounded_error_decoding_information_available=(
            average_holevo + 1e-10 >= required
        ),
        all_finite_controls_passed=passed,
        status=(
            "natural-source-moment-tradeoff-verified"
            if passed
            else "natural-source-moment-control-failure"
        ),
    )
    return controls, aggregate


def perfect_matching_scaling_record(
    n: int,
    *,
    bounded_error: float = 1 / 3,
) -> PerfectMatchingScalingRecord:
    if n < 8 or n % 4:
        raise ValueError("n must be a multiple of four and at least eight")
    if not 0.0 <= bounded_error < 1.0:
        raise ValueError("bounded_error must lie in [0,1)")
    hidden_count = involution_count(n, n // 2)
    log_hidden = math.log2(hidden_count)
    required = fano_required_information(log_hidden, bounded_error)
    elementary_log_hidden = (n // 4) * math.log2(n / 2)
    elementary_log_rms = 0.5 * max(
        0.0,
        (1.0 - bounded_error) * elementary_log_hidden
        - binary_entropy(bounded_error),
    )
    return PerfectMatchingScalingRecord(
        n=n,
        hidden_hypothesis_count=hidden_count,
        log2_hidden_hypothesis_count=log_hidden,
        bounded_error=bounded_error,
        fano_required_information_bits=required,
        fano_forced_log2_direct_inverse_rms=required / 2,
        elementary_log2_hypothesis_lower_bound=elementary_log_hidden,
        elementary_log2_direct_inverse_rms_lower_bound=elementary_log_rms,
        direct_inverse_rms_lower_bound_is_superpolynomial=(
            elementary_log_rms > 4 * math.log2(n)
        ),
        asymptotic_status=(
            "bounded-error-direct-inverse-rms-superpolynomial"
            if elementary_log_rms > 4 * math.log2(n)
            else "finite-asymptotic-control"
        ),
    )


def build_coset_source_weighted_frame_inversion_report(
    *,
    finite_n: int = 5,
    finite_transposition_count: int = 2,
    finite_copy_counts: tuple[int, ...] = (1, 2, 3),
    scaling_n_values: tuple[int, ...] = (8, 16, 32, 64),
    bounded_error: float = 1 / 3,
) -> CosetSourceWeightedFrameInversionReport:
    controls: list[UniformProjectorFrameControl] = []
    aggregates: list[NaturalSourceAggregate] = []
    for copy_count in finite_copy_counts:
        branch_controls, aggregate = natural_source_controls(
            finite_n,
            finite_transposition_count,
            copy_count,
            bounded_error=bounded_error,
        )
        controls.extend(branch_controls)
        aggregates.append(aggregate)
    scaling = [
        perfect_matching_scaling_record(n, bounded_error=bounded_error)
        for n in scaling_n_values
    ]
    verified = bool(
        all(row.theorem_control_passed for row in controls)
        and all(row.all_finite_controls_passed for row in aggregates)
        and all(
            row.elementary_log2_hypothesis_lower_bound
            <= row.log2_hidden_hypothesis_count + 1e-10
            for row in scaling
        )
    )
    theorem = SourceWeightedFrameTheorem(
        ensemble=(
            "Equiprobable normalized rank-R projector states rho_h=P_h/R; "
            "the direct normalized frame is B=E_h P_h=R F."
        ),
        exact_moment_identity=(
            "For the spectral source law of F, E_F[1/b]=Tr(F B^+)="
            "rank(F)/R, where b ranges over positive eigenvalues of B."
        ),
        entropy_tradeoff=(
            "chi=S(F)-log2 R and S(F)<=log2 rank(F), hence "
            "rank(F)/R>=2^chi."
        ),
        hidden_independent_source_extension=(
            "For a classical source Z independent of h, Jensen gives "
            "E_Z[rank(F_Z)/R_Z]>=2^(E_Z chi_Z)."
        ),
        fano_consequence=(
            "If any decoder has error epsilon, E_Z chi_Z is at least "
            "log2 M-h2(epsilon)-epsilon log2(M-1); the direct inverse-root "
            "RMS factor is therefore at least 2^(that quantity/2)."
        ),
        perfect_matching_consequence=(
            "For fixed-point-free involutions, M=(n-1)!! and "
            "M>=(n/2)^(n/4), so every constant-error direct source-weighted "
            "inverse schema carrying enough information has n^Omega(n) RMS."
        ),
        direct_route_consequence=(
            "Source weighting does not rescue the projected-LCU route once "
            "that route is required to carry enough information to decode."
        ),
        scope_limit=(
            "The theorem does not lower-bound a fused PGM polar isometry, a "
            "different frame factorization, an arbitrary covariant POVM, or "
            "general quantum circuits."
        ),
        exact_source_moment_identity_proved=True,
        entropy_rank_tradeoff_proved=True,
        source_averaged_jensen_tradeoff_proved=True,
        bounded_error_direct_inverse_obstruction_proved=True,
        fused_polar_isometry_ruled_out=False,
        arbitrary_collective_measurement_ruled_out=False,
        general_quantum_circuit_lower_bound_proved=False,
        theorem_verified=verified,
        status=(
            "source-weighted-direct-frame-inversion-tradeoff-proved"
            if verified
            else "source-weighted-frame-inversion-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_branch_control_count": len(controls),
        "natural_source_aggregate_count": len(aggregates),
        "finite_control_failure_count": sum(
            not row.theorem_control_passed for row in controls
        ),
        "maximum_uniform_projector_residual": max(
            row.uniform_projector_residual for row in controls
        ),
        "maximum_source_moment_identity_residual": max(
            row.source_moment_identity_residual for row in controls
        ),
        "maximum_entropy_rank_bound_residual": max(
            row.entropy_rank_bound_residual for row in controls
        ),
        "maximum_jensen_bound_residual": max(
            row.jensen_bound_residual for row in aggregates
        ),
        "maximum_finite_average_holevo_bits": max(
            row.average_conditional_holevo_bits for row in aggregates
        ),
        "maximum_finite_global_source_inverse_rms": max(
            row.global_source_weighted_inverse_root_rms_factor
            for row in aggregates
        ),
        "bounded_error_direct_inverse_obstruction_theorem_count": 1,
        "fused_polar_isometry_lower_bound_count": 0,
        "general_quantum_circuit_lower_bound_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return CosetSourceWeightedFrameInversionReport(
        created_at=utc_now(),
        theorem_contract={
            "operator": "B_Z=R_Z F_Z=E_h P_(h,Z)",
            "source_law": (
                "Natural weak-Fourier labels Z are retained with their exact "
                "hidden-independent probabilities; within a branch, spectral "
                "weight is the average state F_Z."
            ),
            "cost_quantity": (
                "The second moment of the standalone inverse-root factor "
                "under the actual source spectrum, not a worst-case condition number."
            ),
            "information_requirement": (
                "Fano is used only conditionally: if bounded-error decoding is "
                "possible, the ensemble Holevo information must meet the bound."
            ),
            "non_claim": (
                "No runtime lower bound is inferred for implementations that "
                "avoid a standalone B_Z^(-1/2) primitive."
            ),
        },
        finite_controls=controls,
        natural_source_aggregates=aggregates,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-FUSED-POLAR-ISOMETRY",
                "statement": (
                    "Construct or obstruct the source-specific polar isometry "
                    "as one coherent transform without standalone frame inversion."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-MULTICOPY-COMMUTANT-QFT",
                "statement": (
                    "Give a uniform polynomial circuit for the diagonal "
                    "conjugation/centralizer commutant at k=Theta(n log n)."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-COMPRESSED-OUTCOME-DECODER",
                "statement": (
                    "Decode the exponentially large involution orbit without "
                    "an explicit outcome table."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": (
                    "Could source weighting remove the exponentially weak "
                    "mean LCU scale?"
                ),
                "answer": (
                    "It can reduce the generic dimension/rank factor, but the "
                    "exact remaining moment rank(F)/R is exponential whenever "
                    "the branch carries extensive Holevo information."
                ),
                "route_killed": True,
            },
            {
                "challenge": "Does this prove the PGM is computationally hard?",
                "answer": (
                    "No. The inverse may cancel inside a fused polar isometry; "
                    "the theorem charges only implementations exposing it separately."
                ),
                "route_killed": False,
            },
            {
                "challenge": "Can rare source branches evade the tradeoff?",
                "answer": (
                    "Not in mean-square accounting: hidden independence plus "
                    "Jensen converts average conditional Holevo information "
                    "into an average moment lower bound."
                ),
                "route_killed": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "exact_source_weighted_inverse_moment_proved": True,
            "entropy_information_tradeoff_proved": True,
            "bounded_error_direct_projected_lcu_inverse_rescued": False,
            "fused_source_specific_polar_transform_constructed": False,
            "fused_source_specific_polar_transform_ruled_out": False,
            "polynomial_hidden_involution_decoder_proved": False,
            "general_quantum_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Source weighting cannot by itself repair the standalone "
                "projected-LCU inverse at decoding-scale information. The "
                "remaining high-upside route must fuse the polar transform or "
                "use a genuinely different collective measurement."
            ),
        },
        status="coset-source-weighted-direct-inverse-closed-fused-polar-open",
        summary=(
            f"Verified the exact source-moment and entropy tradeoff on "
            f"{len(controls)} natural S_{finite_n} carrier branches across "
            f"{len(aggregates)} copy widths. Bounded-error perfect-matching "
            "decoding forces n^Omega(n) direct inverse-root RMS, while fused "
            "polar and alternative collective measurements remain open."
        ),
        falsifiers_triggered=[
            (
                "Actual source weighting does not make the standalone direct "
                "average-frame inverse polynomial at decoding-scale information."
            ),
            (
                "Finite low condition number is irrelevant to the exact "
                "rank-over-input-rank source moment."
            ),
            (
                "Rare favorable source labels cannot remove the mean-square "
                "tradeoff while the total ensemble meets Fano."
            ),
            (
                "The obstruction must not be promoted to a lower bound on a "
                "fused PGM isometry or arbitrary quantum measurement."
            ),
        ],
    )


def write_coset_source_weighted_frame_inversion_report(
    output_path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-COSET-SOURCE-WEIGHTED-FRAME-INVERSION-TRADEOFF"
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
        build_coset_source_weighted_frame_inversion_report(**kwargs)
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_coset_source_weighted_frame_inversion_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
