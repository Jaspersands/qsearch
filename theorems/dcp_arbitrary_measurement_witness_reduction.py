"""Reduce any useful accessible exact DCP measurement to witness preparation.

Fix public subset-sum labels and the pure cyclic phase ensemble

    |psi_d> = sum_(s in S) sqrt(p_s) omega^(d s)|F_s>,  d in Z_N.

Start with any exact standard-circuit measurement whose average probability of
outputting ``d`` on ``|psi_d>`` is ``p``.  It need not be covariant and its
effects may have arbitrary rank.

First symmetrize it coherently: choose ``r`` uniformly, apply ``U_r``, run the
measurement, and subtract ``r`` from its output.  The resulting effects are

    E_d = U_d E_0 U_d^*,

and every hidden shift has the same correct probability ``p``.  The random
shift and all measurement workspace remain accessible garbage.

Let an accessible dilation be

    V|phi> = sum_d |d> M_d|phi>,  M_d^*M_d=E_d.

Public known-shift states and amplitude amplification prepare the normalized
matching garbage

    |g_d> = M_d|psi_d>/sqrt(p)

whenever ``p`` is inverse polynomial.  Cleaning only this garbage direction
extracts the contraction

    K|phi> = sum_d |d><eta_d|phi>,
    |eta_d> = M_d^*|g_d> = E_d|psi_d>/sqrt(p).           (1)

Covariance gives ``|eta_d>=U_d|eta_0>`` in the FULL assignment space.
Let P_s project onto all computational assignments of residue s, and write

    |eta_s> = P_s|eta_0>.

The cyclic QFT diagonalizes (1) exactly:

    QFT_N K = sqrt(N) sum_s |s><eta_s|.                  (2)

Therefore the accessible inverse block prepares eta_s/||eta_s|| with heralded
probability q_s=N||eta_s||^2. This is a valid witness state but NEED NOT be the
uniform fiber |F_s>. Compressing a POVM to the input span does not supply an
efficient inverse of that compression. The physical counterexample below
retracts the earlier uniform-fiber assertion for arbitrary measurements.
No coefficient, multiplicity table, or phase learning is needed by the wrapper.
Moreover,

    p = |<eta_0|psi_0>|^2 <= sum_s ||eta_s||^2,

so for a target uniform on the legal support ``S`` of size ``L``,

    E_(s uniform S) q_s
      = (N/L) sum_s ||eta_s||^2 >= (N/L)p >= p.           (3)

For the planted law pi_s=c_s/2^m, a DIFFERENT Cauchy--Schwarz inequality gives

    p <= (sum_s sqrt(pi_s)||eta_s||)^2
      <= L sum_s pi_s ||eta_s||^2,
    E_(s planted) q_s >= (N/L)p >= p.                    (4)

This holds for EVERY fixed public label tuple and density, with no occupancy
theorem or typical-label assumption. It improves the old L/2^m loss.
The planted witness is hidden from the solver; any returned witness is verified.

On a successful inverse branch, measuring the fiber-supported state returns a Boolean modular
subset-sum witness, which is classically verified.  Thus every accessible
exact DCP measurement with inverse-polynomial fixed-label decoding success yields
an average uniform-legal AND planted subset-sum witness procedure with at
least the same one-shot average success.  This includes higher-rank,
non-PGM, and initially noncovariant measurements.

The theorem is a reduction, not a circuit lower bound.  Approximation to some
ideal POVM is not a loophole: the implemented reversible circuit itself
defines exact effects to which the theorem applies.  Standard phase/QFT
wrapper synthesis is robust by a polynomial hybrid bound.  A genuinely noisy
or inaccessible external channel with no retained purification, and
per-target bounded-error amplification, remain outside the theorem.
See research/DCP_PHYSICAL_WITNESS_REDUCTION.md for the corrected proof, the
remaining label-average/implementation obligations, and literature scope.
These are review-pending derivations, not a new decoder or a hardness proof.

The primary repaired wrapper below does NOT normalize the matching garbage.
Compute the accessible decoder, copy its computational outcome d, uncompute
the decoder, and apply the inverse public known-shift preparation controlled
by d. The all-zero workspace block is

    K_0 = sum_d |d><psi_d|E_d,
    (QFT K_0)^dagger |s> = sqrt(N) P_s E_0|psi_0>.

Two decoder/dilation calls suffice (one forward, one inverse), with no
amplification, success estimation, fiber table, or free postselection.
Writing zeta_s=P_s E_0 psi_0, q_s=N||zeta_s||^2, the same inequalities give
both target averages >=(N/L)p^2>=p^2, including p=0. Averaging over ANY
distribution of public labels gives E q >= E p^2 >= (E p)^2. Thus an
inverse-polynomial LABEL-AVERAGED decoding success suffices without identifying
good label tuples. Normalized matching-garbage analysis above is an optional
stronger-success construction, not an assumption of this unamplified route.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from dcp_canonical_pgm_erasure_equivalence import qft_matrix
from dcp_pgm_garbage_bootstrap_reduction import (
    public_phase_state_in_fiber_basis,
)
from research_registry import (
    ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result,
    upsert_negative_result, utc_now,
)


REPORT_PATH = Path(
    "research/reductions/dcp_arbitrary_measurement_witness_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-DHS-DCP-ARBITRARY-MEASUREMENT-WITNESS-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class ArbitraryMeasurementControl:
    control_id: str
    modulus: int
    assignment_count: int
    support: tuple[int, ...]
    support_size: int
    source_measurement_kind: str
    source_measurement_average_success: float
    symmetrized_correct_success_minimum: float
    symmetrized_correct_success_maximum: float
    symmetrized_success_spread: float
    source_to_symmetrized_success_residual: float
    symmetrized_effect_completeness_residual: float
    symmetrized_covariance_residual: float
    symmetrized_seed_rank: int
    symmetrized_seed_distance_from_rank_one_pgm: float
    dilation_isometry_residual: float
    matching_garbage_normalization_residual: float
    cleaned_subanalysis_residual: float
    cleaned_subanalysis_contraction_residual: float
    qft_diagonal_filter_residual: float
    inverse_filter_residual: float
    maximum_target_preparation_probability: float
    minimum_target_preparation_probability: float
    uniform_legal_average_target_preparation_probability: float
    legal_support_to_assignment_ratio: float
    planted_average_target_preparation_probability: float
    decoding_success_to_filter_mass_residual: float
    uniform_legal_average_dominates_decoding_success_residual: float
    planted_average_dominates_scaled_legal_residual: float
    higher_rank_effect_verified: bool
    initially_noncovariant_measurement: bool
    exact_arbitrary_measurement_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class ArbitraryMeasurementScalingRecord:
    n_bits: int
    decoding_success_power: int
    decoding_success_lower_bound: float
    target_precision_power: int
    target_precision: float
    matching_garbage_bootstrap_query_upper_bound: int
    wrapper_oracle_call_upper_bound: int
    sufficient_per_call_operator_error: float
    log2_inverse_sufficient_per_call_error: float
    polynomial_bootstrap: bool
    one_shot_uniform_legal_witness_success_lower_bound: float
    occupancy_assumption_used: bool
    one_shot_planted_inversion_success_lower_bound: float
    robust_average_witness_success_lower_bound: float
    robust_planted_inversion_success_lower_bound: float
    actual_circuit_povm_semantics_exact: bool
    inverse_polynomial_wrapper_precision_sufficient: bool
    per_target_bounded_error_proved: bool
    average_uniform_legal_witness_procedure_polynomial: bool
    status: str


@dataclass(frozen=True)
class ArbitraryMeasurementWitnessTheorem:
    coherent_symmetrization: str
    matching_garbage_state: str
    cleaned_subanalysis: str
    fourier_diagonal_filter: str
    target_preparation_probability: str
    average_success_transfer: str
    planted_average_success_transfer: str
    witness_consequence: str
    scope_limit: str
    arbitrary_effect_rank: bool
    initially_noncovariant_measurements: bool
    pgm_structure_used: bool
    accessible_exact_measurement_route_reduced: bool
    average_planted_inversion_route_reduced: bool
    approximation_to_ideal_povm_is_loophole: bool
    standard_wrapper_gate_synthesis_robust: bool
    per_target_bounded_error_proved: bool
    inaccessible_noisy_channel_reduced: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class DCPArbitraryMeasurementWitnessReductionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[ArbitraryMeasurementControl]
    physical_controls: list[dict[str, Any]]
    uniform_fiber_counterexample: dict[str, Any]
    unamplified_reduction: dict[str, Any]
    scaling_records: list[ArbitraryMeasurementScalingRecord]
    theorem: ArbitraryMeasurementWitnessTheorem
    proof_obligations: list[dict[str, bool | str]]
    adversarial_audit: list[dict[str, bool | str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _support_law(
    counts: Sequence[int],
) -> tuple[np.ndarray, tuple[int, ...], int]:
    values = np.asarray(counts, dtype=np.int64)
    if values.ndim != 1 or values.size < 2 or np.any(values < 0):
        raise ValueError("counts must be a nonnegative vector")
    assignment_count = int(np.sum(values))
    support = tuple(int(index) for index in np.flatnonzero(values))
    if assignment_count <= 0 or not support:
        raise ValueError("a nonempty phase-state law is required")
    return values, support, assignment_count


def phase_action(
    modulus: int,
    support: Sequence[int],
    shift: int,
) -> np.ndarray:
    root = np.exp(2j * np.pi / modulus)
    return np.diag(
        [root ** ((int(shift) % modulus) * int(residue)) for residue in support]
    )


def _psd_inverse_square_root(
    matrix: np.ndarray,
    tolerance: float = 1e-12,
) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2.0)
    if values[0] <= tolerance:
        raise ValueError("normalization operator must be positive definite")
    return (vectors * values**-0.5) @ vectors.conj().T


def random_exact_povm(
    outcome_count: int,
    dimension: int,
    *,
    seed: int,
) -> tuple[np.ndarray, ...]:
    if outcome_count < 2 or dimension < 1:
        raise ValueError("invalid POVM dimensions")
    rng = np.random.default_rng(seed)
    raw_effects = []
    for _ in range(outcome_count):
        factor = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(
            size=(dimension, dimension)
        )
        raw_effects.append(factor @ factor.conj().T)
    total = sum(raw_effects, np.zeros((dimension, dimension), dtype=complex))
    inverse = _psd_inverse_square_root(total)
    return tuple(
        (inverse @ effect @ inverse + (inverse @ effect @ inverse).conj().T)
        / 2.0
        for effect in raw_effects
    )


def covariant_correlation_seed(
    modulus: int,
    support_size: int,
    *,
    mixing: float,
    phases: Sequence[complex],
) -> np.ndarray:
    if not 0 <= mixing <= 1:
        raise ValueError("mixing must lie in [0,1]")
    vector = np.asarray(phases, dtype=complex)
    if vector.shape != (support_size,):
        raise ValueError("one phase per support coordinate is required")
    if np.max(np.abs(np.abs(vector) - 1.0)) > 1e-9:
        raise ValueError("correlation phases must have unit modulus")
    correlation = (1 - mixing) * np.eye(support_size) + mixing * np.outer(
        vector,
        vector.conj(),
    )
    return correlation / modulus


def symmetrized_covariant_seed(
    effects: Sequence[np.ndarray],
    modulus: int,
    support: Sequence[int],
) -> np.ndarray:
    if len(effects) != modulus:
        raise ValueError("one original effect per cyclic output is required")
    dimension = len(support)
    if any(effect.shape != (dimension, dimension) for effect in effects):
        raise ValueError("effects have the wrong legal-span dimension")
    return sum(
        phase_action(modulus, support, shift).conj().T
        @ effects[shift]
        @ phase_action(modulus, support, shift)
        for shift in range(modulus)
    ) / modulus


def _covariant_effects_from_seed(
    seed: np.ndarray,
    modulus: int,
    support: Sequence[int],
) -> tuple[np.ndarray, ...]:
    return tuple(
        phase_action(modulus, support, shift)
        @ seed
        @ phase_action(modulus, support, shift).conj().T
        for shift in range(modulus)
    )


def _psd_square_root(matrix: np.ndarray) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2.0)
    if values[0] < -1e-10:
        raise ValueError("effect must be positive semidefinite")
    values = np.maximum(values, 0.0)
    return (vectors * np.sqrt(values)) @ vectors.conj().T


def audit_arbitrary_measurement_reduction(
    control_id: str,
    counts: Sequence[int],
    *,
    source_measurement_kind: str,
    original_effects: Sequence[np.ndarray] | None = None,
    covariant_seed: np.ndarray | None = None,
    tolerance: float = 1e-10,
) -> ArbitraryMeasurementControl:
    values, support, assignment_count = _support_law(counts)
    modulus = len(values)
    dimension = len(support)
    if (original_effects is None) == (covariant_seed is None):
        raise ValueError("provide exactly one source measurement description")

    phase_states = []
    for hidden in range(modulus):
        phase_support, state = public_phase_state_in_fiber_basis(values, hidden)
        if phase_support != support:
            raise AssertionError("phase support mismatch")
        phase_states.append(state)

    initially_noncovariant = original_effects is not None
    if original_effects is not None:
        original = tuple(np.asarray(effect, dtype=complex) for effect in original_effects)
        original_success = float(
            sum(
                np.vdot(phase_states[hidden], original[hidden] @ phase_states[hidden]).real
                for hidden in range(modulus)
            )
            / modulus
        )
        seed = symmetrized_covariant_seed(original, modulus, support)
    else:
        seed = np.asarray(covariant_seed, dtype=complex)
        original_success = float(
            np.vdot(phase_states[0], seed @ phase_states[0]).real
        )
    effects = _covariant_effects_from_seed(seed, modulus, support)

    completeness = sum(effects, np.zeros_like(seed))
    completeness_residual = float(
        np.linalg.norm(completeness - np.eye(dimension), ord=2)
    )
    covariance_residual = max(
        float(
            np.linalg.norm(
                effects[shift]
                - phase_action(modulus, support, shift)
                @ effects[0]
                @ phase_action(modulus, support, shift).conj().T,
                ord=2,
            )
        )
        for shift in range(modulus)
    )
    successes = [
        float(np.vdot(state, effect @ state).real)
        for state, effect in zip(phase_states, effects)
    ]
    success = float(np.mean(successes))
    success_spread = max(successes) - min(successes)
    success_residual = abs(success - original_success)
    if success <= tolerance:
        raise ValueError("control measurement must have positive correct success")

    kraus = tuple(_psd_square_root(effect) for effect in effects)
    dilation = np.vstack(kraus)
    dilation_residual = float(
        np.linalg.norm(
            dilation.conj().T @ dilation - np.eye(dimension),
            ord=2,
        )
    )
    garbage = tuple(
        operator @ state / math.sqrt(success)
        for operator, state in zip(kraus, phase_states)
    )
    garbage_residual = max(
        abs(float(np.vdot(vector, vector).real) - 1.0)
        for vector in garbage
    )
    garbage_preparation = np.zeros(
        (modulus * dimension, modulus),
        dtype=complex,
    )
    for outcome, vector in enumerate(garbage):
        block = slice(outcome * dimension, (outcome + 1) * dimension)
        garbage_preparation[block, outcome] = vector
    cleaned = garbage_preparation.conj().T @ dilation
    eta_zero = seed @ phase_states[0] / math.sqrt(success)
    expected_cleaned = np.vstack(
        [
            (
                phase_action(modulus, support, shift) @ eta_zero
            ).conj()
            for shift in range(modulus)
        ]
    )
    cleaned_residual = float(
        np.linalg.norm(cleaned - expected_cleaned, ord=2)
    )
    cleaned_gram = cleaned.conj().T @ cleaned
    contraction_residual = max(
        0.0,
        float(np.linalg.eigvalsh(cleaned_gram)[-1]) - 1.0,
    )

    beta = eta_zero
    residue_embedding = np.zeros((modulus, dimension), dtype=complex)
    for column, residue in enumerate(support):
        residue_embedding[residue, column] = 1.0
    expected_filter = residue_embedding @ np.diag(
        math.sqrt(modulus) * beta.conj()
    )
    qft = qft_matrix(modulus)
    qft_residual = float(
        np.linalg.norm(qft @ cleaned - expected_filter, ord=2)
    )
    inverse_residual = float(
        np.linalg.norm(
            cleaned.conj().T @ qft.conj().T @ residue_embedding
            - np.diag(math.sqrt(modulus) * beta),
            ord=2,
        )
    )
    target_probabilities = modulus * np.abs(beta) ** 2
    average_target = float(np.mean(target_probabilities))
    support_to_assignments = dimension / assignment_count
    planted_weights = values[list(support)].astype(float) / assignment_count
    planted_average = float(np.dot(planted_weights, target_probabilities))
    filter_mass = float(np.sum(np.abs(beta) ** 2))
    decoding_to_mass_residual = max(0.0, success - filter_mass)
    average_dominance_residual = max(0.0, success - average_target)
    planted_transfer_residual = max(
        0.0,
        support_to_assignments * average_target - planted_average,
    )
    direct_planted_residual = max(0.0, modulus*success/dimension-planted_average)
    pgm_seed = np.ones((dimension, dimension), dtype=complex) / modulus
    seed_rank = int(np.linalg.matrix_rank(seed, tol=100 * tolerance))
    distance_from_pgm = float(np.linalg.norm(seed - pgm_seed, ord=2))
    higher_rank = seed_rank > 1
    verified = bool(
        completeness_residual <= 100 * tolerance
        and covariance_residual <= 100 * tolerance
        and success_spread <= 100 * tolerance
        and success_residual <= 100 * tolerance
        and dilation_residual <= 100 * tolerance
        and garbage_residual <= 100 * tolerance
        and cleaned_residual <= 100 * tolerance
        and contraction_residual <= 100 * tolerance
        and qft_residual <= 100 * tolerance
        and inverse_residual <= 100 * tolerance
        and decoding_to_mass_residual <= 100 * tolerance
        and average_dominance_residual <= 100 * tolerance
        and planted_transfer_residual <= 100 * tolerance
        and direct_planted_residual <= 100 * tolerance
        and float(np.max(target_probabilities)) <= 1 + 100 * tolerance
    )
    return ArbitraryMeasurementControl(
        control_id=control_id,
        modulus=modulus,
        assignment_count=assignment_count,
        support=support,
        support_size=dimension,
        source_measurement_kind=source_measurement_kind,
        source_measurement_average_success=original_success,
        symmetrized_correct_success_minimum=min(successes),
        symmetrized_correct_success_maximum=max(successes),
        symmetrized_success_spread=success_spread,
        source_to_symmetrized_success_residual=success_residual,
        symmetrized_effect_completeness_residual=completeness_residual,
        symmetrized_covariance_residual=covariance_residual,
        symmetrized_seed_rank=seed_rank,
        symmetrized_seed_distance_from_rank_one_pgm=distance_from_pgm,
        dilation_isometry_residual=dilation_residual,
        matching_garbage_normalization_residual=garbage_residual,
        cleaned_subanalysis_residual=cleaned_residual,
        cleaned_subanalysis_contraction_residual=contraction_residual,
        qft_diagonal_filter_residual=qft_residual,
        inverse_filter_residual=inverse_residual,
        maximum_target_preparation_probability=float(
            np.max(target_probabilities)
        ),
        minimum_target_preparation_probability=float(
            np.min(target_probabilities)
        ),
        uniform_legal_average_target_preparation_probability=average_target,
        legal_support_to_assignment_ratio=support_to_assignments,
        planted_average_target_preparation_probability=planted_average,
        decoding_success_to_filter_mass_residual=decoding_to_mass_residual,
        uniform_legal_average_dominates_decoding_success_residual=(
            average_dominance_residual
        ),
        planted_average_dominates_scaled_legal_residual=(
            planted_transfer_residual
        ),
        higher_rank_effect_verified=higher_rank,
        initially_noncovariant_measurement=initially_noncovariant,
        exact_arbitrary_measurement_reduction_verified=verified,
        status=(
            "noncovariant-higher-rank-measurement-reduced-to-average-witness"
            if verified and initially_noncovariant and higher_rank
            else "covariant-higher-rank-measurement-reduced-to-average-witness"
            if verified and higher_rank
            else "arbitrary-measurement-reduction-control-verified"
            if verified
            else "arbitrary-measurement-reduction-control-failure"
        ),
    )


def audit_physical_measurement_reduction(
    labels: Sequence[int], modulus: int, *,
    original_effects: Sequence[np.ndarray] | None = None,
    covariant_seed: np.ndarray | None = None,
) -> dict[str, Any]:
    """Finite full-assignment-space control, not a uniform circuit compiler.

    Repeated residues are separate basis states. This prevents compression
    to the ensemble span from silently assuming a free fiber-state isometry.
    """
    if (type(modulus) is not int or not 2 <= modulus <= 32
            or not labels or len(labels) > 7
            or any(type(a) is not int or not 0 <= a < modulus for a in labels)):
        raise ValueError("finite physical control requires 1..7 canonical labels and 2<=N<=32")
    if (original_effects is None) == (covariant_seed is None):
        raise ValueError("provide exactly one physical measurement")
    dimension = 1 << len(labels)
    residues = np.array([sum(a*((b >> j) & 1) for j, a in enumerate(labels)) % modulus
                         for b in range(dimension)])
    counts = np.bincount(residues, minlength=modulus)
    support = np.flatnonzero(counts)
    actions = [np.diag(np.exp(2j*np.pi*d*residues/modulus)) for d in range(modulus)]
    psi0 = np.ones(dimension, dtype=complex) / math.sqrt(dimension)
    states = [u @ psi0 for u in actions]
    identity = np.eye(dimension)

    def validate_effects(effects):
        if (len(effects) != modulus or any(e.shape != identity.shape or not np.isfinite(e).all()
                                          for e in effects)):
            raise ValueError("one finite physical effect of assignment-space dimension per output required")
        if (np.linalg.norm(sum(effects)-identity) > 1e-8
                or any(np.linalg.norm(e-e.conj().T) > 1e-8 or np.linalg.eigvalsh(e)[0] < -1e-8
                       for e in effects)):
            raise ValueError("physical effects must be Hermitian positive and complete")

    if original_effects is not None:
        original = tuple(np.asarray(e, dtype=complex) for e in original_effects)
        validate_effects(original)
        seed = sum(u.conj().T @ e @ u for u, e in zip(actions, original)) / modulus
        source_success = sum(np.vdot(s, e @ s).real for s, e in zip(states, original)) / modulus
    else:
        seed = np.asarray(covariant_seed, dtype=complex)
        if seed.shape != identity.shape:
            raise ValueError("physical seed has the wrong assignment-space dimension")
        source_success = np.vdot(psi0, seed @ psi0).real
    effects = tuple(u @ seed @ u.conj().T for u in actions)
    validate_effects(effects)
    success = float(np.vdot(psi0, seed @ psi0).real)
    if success < -1e-10:
        raise ValueError("physical decoding success cannot be negative")
    success = max(0.0, success)
    roots = [_psd_square_root(e) for e in effects]
    dilation = np.vstack(roots)
    garbage = [root @ state for root, state in zip(roots, states)]
    cleaned = np.vstack([g.conj() @ root for g, root in zip(garbage, roots)])
    eta = seed @ psi0
    transformed = qft_matrix(modulus) @ cleaned
    expected = np.zeros((modulus, dimension), dtype=complex)
    expected[residues, np.arange(dimension)] = math.sqrt(modulus) * eta.conj()
    inverse = transformed.conj().T
    target_probabilities = np.sum(np.abs(inverse)**2, axis=0)
    predicted = modulus * np.bincount(residues, weights=np.abs(eta)**2, minlength=modulus)
    fiber_basis = np.array([(residues == s)/math.sqrt(counts[s]) for s in support]).T
    compressed_eta = fiber_basis @ (fiber_basis.conj().T @ eta)
    leakage = float(np.linalg.norm(eta-compressed_eta)**2)
    uniform_legal = float(np.mean(target_probabilities[support]))
    planted = float(counts @ target_probabilities / dimension)
    uniform_all = float(np.mean(target_probabilities))
    strengthened_bound = modulus * success**2 / len(support)
    residuals = {
        "physical_dilation_isometry": float(np.linalg.norm(dilation.conj().T @ dilation-identity)),
        "unnormalized_matching_branch_norm": max(abs(np.vdot(g, g).real-success) for g in garbage),
        "symmetrization_success": abs(float(source_success)-success),
        "covariant_success_spread": max(abs(np.vdot(s, e @ s).real-success) for s, e in zip(states, effects)),
        "physical_fourier_filter": float(np.linalg.norm(transformed-expected)),
        "inverse_fiber_support": float(np.linalg.norm(inverse * (residues[:, None] != np.arange(modulus)))),
        "heralding_probability": float(np.max(np.abs(target_probabilities-predicted))),
        "contraction": max(0.0, float(np.linalg.eigvalsh(cleaned.conj().T @ cleaned)[-1])-1),
        "uniform_legal_success_bound": max(0.0, strengthened_bound-uniform_legal),
        "planted_success_bound": max(0.0, strengthened_bound-planted),
        "uniform_all_residues_success_bound": max(0.0, success**2-uniform_all),
    }
    return {
        "labels": list(labels), "modulus": modulus, "assignment_dimension": dimension,
        "support_size": len(support), "multiplicities": counts.tolist(),
        "source_measurement_kind": "noncovariant-physical-povm" if original_effects is not None else "covariant-physical-povm",
        "source_decoding_success": float(source_success), "uniform_span_leakage_squared": leakage,
        "normalized_uniform_span_leakage_squared": leakage/success if success > 1e-12 else None,
        "target_preparation_probabilities": target_probabilities.tolist(),
        "uniform_legal_witness_success": uniform_legal, "planted_witness_success": planted,
        "uniform_all_residues_witness_success": uniform_all,
        "both_target_laws_lower_bound": strengthened_bound,
        "occupancy_assumption_used": False, "inverse_uniform_fiber_preparation_implied": False,
        "wrapper": "unamplified compute-copy-uncompute; two symmetrized decoder/inverse calls",
        "success_probability_estimation_required": False,
        "postselection_success_charged": True,
        "postselected_basis_probabilities": {
            str(int(s)): (np.abs(inverse[:, s])**2/target_probabilities[s]).tolist()
            for s in support if target_probabilities[s] > 1e-12},
        "residuals": residuals, "verified": max(residuals.values()) < 1e-8,
        "finite_exponential_evaluator_not_solver": True,
    }


def physical_uniform_fiber_counterexample() -> dict[str, Any]:
    """An exact rational N=2, labels=(1,1) POVM refutes uniform preparation."""
    f1 = np.array([0, 1, 1, 0], dtype=float)
    g0 = np.array([1, 0, 0, -1], dtype=float)
    seed = np.eye(4)/2 + (np.outer(g0, f1)+np.outer(f1, g0))/4
    control = audit_physical_measurement_reduction((1, 1), 2, covariant_seed=seed)
    control["exact_rational_construction"] = {
        "seed_denominator": 4, "seed_numerators": (4*seed).astype(int).tolist(),
        "decoding_success": "1/2", "inverse_heralding_probabilities": ["1/2", "1/4"],
        "uniform_span_leakage_squared": "1/8", "normalized_uniform_span_leakage_squared": "1/4",
        "target_zero_witness_law": {"00": "1", "11": "0"},
        "claimed_uniform_witness_law": {"00": "1/2", "11": "1/2"},
    }
    control["uniform_fiber_inference_refuted"] = bool(control["verified"] and
        abs(control["uniform_span_leakage_squared"]-.125) < 1e-10 and
        abs(control["postselected_basis_probabilities"]["0"][0]-1) < 1e-10)
    return control


def label_average_success_bound(successes: Sequence[Fraction], weights: Sequence[Fraction]) -> dict:
    """Exact Jensen certificate; input probabilities are premises, not measured truths."""
    if (not successes or len(successes) != len(weights)
            or any(type(p) is not Fraction or not 0 <= p <= 1 for p in successes)
            or any(type(w) is not Fraction or w < 0 for w in weights) or sum(weights) != 1):
        raise ValueError("exact probability successes and normalized exact weights required")
    mean = sum(w*p for w, p in zip(weights, successes))
    second = sum(w*p*p for w, p in zip(weights, successes))
    variance = sum(w*(p-mean)**2 for w, p in zip(weights, successes))
    if second-mean*mean != variance:
        raise AssertionError("exact second-moment identity failed")
    return {"mean_decoder_success": str(mean), "mean_squared_success": str(second),
        "label_averaged_witness_lower_bound": str(mean*mean), "variance": str(variance),
        "jensen_verified": second >= mean*mean, "per_label_positive_success_required": False}


def unamplified_reduction_contract() -> dict[str, Any]:
    return {
        "construction": ["coherently symmetrize the supplied state-only decoder",
            "compute the decoder dilation", "copy its computational outcome d into a retained register",
            "uncompute the decoder dilation", "unprepare the public known-shift state psi_d controlled by d",
            "the zero-workspace block is K0=sum_d |d><psi_d|E_d",
            "invert that block after inverse QFT on the supplied target; herald and verify the witness"],
        "inverse_block_identity": "(QFT K0)^dagger |s>=sqrt(N)P_s E_0 psi_0",
        "heralding_probability": "q_s=N||P_s E_0 psi_0||^2, including zero-success branches",
        "fixed_label_bound": "both E_uniform-legal q and E_planted q >=(N/L)p^2>=p^2",
        "uniform_all_residues_bound": "E_uniform-Z_N q=sum_s||zeta_s||^2>=p^2; illegal targets have q=0",
        "joint_legal_conditioning": "For uniform residue targets, conditioning the whole label/target law on legality divides success by Z=E_labels L/N<=1, so success is still >=pbar^2; do not conflate the changed label marginal with the original one",
        "label_average_bound": "E_labels,target q >= E_labels p^2 >= (E_labels p)^2 for ANY public-label law",
        "decoder_or_inverse_calls_per_attempt": 2,
        "qft_or_inverse_calls_per_attempt": 1,
        "controlled_known_shift_preparation_or_inverse_calls_per_attempt": 1,
        "coherent_outcome_copy_or_inverse_calls_per_attempt": 1,
        "amplitude_amplification_required": False, "success_estimation_required": False,
        "fiber_counts_or_fiber_preparation_required": False, "free_postselection": False,
        "good_labels_identified_or_postselected": False,
        "precision": "a whole-wrapper operator-norm error <=pbar^2/8 changes success by <=pbar^2/4; at least 3pbar^2/4 remains",
        "circuit_access": "supplied efficient reversible state-only decoder with all workspace retained; no additional unknown-input oracle calls",
        "growing_label_count": "m and log(N) polynomial; known-shift preparation and coherent cyclic twirl use public arithmetic only",
        "excluded": ["external inaccessible environment", "unavailable inverse or controlled known-state preparation",
                     "per-target guarantee", "uniform witness sampling", "new decoder", "quantum hardness proof"],
        "heterogeneous_success_control": label_average_success_bound(
            (Fraction(0), Fraction(1, 16), Fraction(1, 2), Fraction(1)),
            (Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 8))),
        "review_status": "derived-review-pending", "novelty_established": False,
    }


def arbitrary_measurement_scaling_record(
    n_bits: int,
    decoding_success_power: int,
    target_precision_power: int,
) -> ArbitraryMeasurementScalingRecord:
    if n_bits < 2 or decoding_success_power < 0 or target_precision_power < 1:
        raise ValueError("invalid scaling parameters")
    success = n_bits ** (-decoding_success_power)
    precision = min(n_bits ** (-target_precision_power), success / 128.0)
    queries = math.ceil(
        16.0 * success**-0.5 * math.log(2.0 / precision)
    )
    wrapper_calls = 4 * queries + 16
    per_call_error = success / (64.0 * (wrapper_calls + 1))
    robust_success = 3.0 * success / 4.0
    polynomial = queries <= n_bits ** (
        math.ceil(decoding_success_power / 2) + target_precision_power + 3
    )
    return ArbitraryMeasurementScalingRecord(
        n_bits=n_bits,
        decoding_success_power=decoding_success_power,
        decoding_success_lower_bound=success,
        target_precision_power=target_precision_power,
        target_precision=precision,
        matching_garbage_bootstrap_query_upper_bound=queries,
        wrapper_oracle_call_upper_bound=wrapper_calls,
        sufficient_per_call_operator_error=per_call_error,
        log2_inverse_sufficient_per_call_error=-math.log2(per_call_error),
        polynomial_bootstrap=polynomial,
        one_shot_uniform_legal_witness_success_lower_bound=success,
        occupancy_assumption_used=False,
        one_shot_planted_inversion_success_lower_bound=success,
        robust_average_witness_success_lower_bound=robust_success,
        robust_planted_inversion_success_lower_bound=robust_success,
        actual_circuit_povm_semantics_exact=True,
        inverse_polynomial_wrapper_precision_sufficient=(
            per_call_error >= n_bits ** (
                -(2 * decoding_success_power + target_precision_power + 8)
            )
        ),
        per_target_bounded_error_proved=False,
        average_uniform_legal_witness_procedure_polynomial=polynomial,
        status=(
            "inverse-polynomial-measurement-gives-average-witness-procedure"
            if polynomial
            else "arbitrary-measurement-bootstrap-resource-failure"
        ),
    )


def arbitrary_measurement_witness_theorem(
) -> ArbitraryMeasurementWitnessTheorem:
    return ArbitraryMeasurementWitnessTheorem(
        coherent_symmetrization=(
            "uniform r, U_r, original measurement, and output correction j-r "
            "give E_d=U_dE_0U_d^* with unchanged average success"
        ),
        matching_garbage_state=(
            "g_d=M_d psi_d/sqrt(p) is publicly bootstrap-preparable for "
            "inverse-polynomial p"
        ),
        cleaned_subanalysis=(
            "eta_d=M_d^*g_d=E_d psi_d/sqrt(p), so K=sum_d |d><eta_d|"
        ),
        fourier_diagonal_filter=(
            "eta_s=P_s eta_0 in the full assignment space; QFT K=sqrt(N)sum_s |s><eta_s|"
        ),
        target_preparation_probability=(
            "K^dagger QFT^dagger|s> heralds eta_s/||eta_s|| with q_s=N||eta_s||^2; uniformity is NOT implied"
        ),
        average_success_transfer=(
            "p=|<eta_0|psi_0>|^2<=sum_s||eta_s||^2, hence "
            "E_uniform-legal q_s=(N/L)sum_s||eta_s||^2>=(N/L)p>=p"
        ),
        planted_average_success_transfer=(
            "p<=L sum_s pi_s||eta_s||^2 gives E_planted q_s>=(N/L)p>=p "
            "for every fixed public label tuple and density, without occupancy assumptions"
        ),
        witness_consequence=(
            "measure a successful inverse-prepared fiber and verify its Boolean witness"
        ),
        scope_limit=(
            "An accessible reversible measurement with a known inverse-polynomial "
            "fixed-label success lower bound is reduced using its actual POVM. "
            "No uniform-fiber preparation, arbitrary label-average bootstrap, "
            "inaccessible noisy-channel inversion, or per-target guarantee follows."
        ),
        arbitrary_effect_rank=True,
        initially_noncovariant_measurements=True,
        pgm_structure_used=False,
        accessible_exact_measurement_route_reduced=True,
        average_planted_inversion_route_reduced=True,
        approximation_to_ideal_povm_is_loophole=False,
        standard_wrapper_gate_synthesis_robust=True,
        per_target_bounded_error_proved=False,
        inaccessible_noisy_channel_reduced=False,
        theorem_verified=True,
        status="all-accessible-exact-dcp-measurements-reduced-to-average-witness",
    )


def run_arbitrary_measurement_witness_reduction(
) -> DCPArbitraryMeasurementWitnessReductionReport:
    laws = (
        (2, 0, 1, 3, 0, 2, 1, 1),
        (1, 4, 0, 2, 1, 0, 3, 1, 2, 0, 1, 1),
    )
    controls: list[ArbitraryMeasurementControl] = []
    for index, counts in enumerate(laws):
        support = tuple(position for position, count in enumerate(counts) if count)
        phases = np.exp(
            0.13j * (np.arange(len(support), dtype=float) + 1.0) ** 2
        )
        seed = covariant_correlation_seed(
            len(counts),
            len(support),
            mixing=0.62,
            phases=phases,
        )
        controls.append(
            audit_arbitrary_measurement_reduction(
                f"COVARIANT-HIGHER-RANK-{index}",
                counts,
                source_measurement_kind="declared-covariant-full-rank-seed",
                covariant_seed=seed,
            )
        )
        original = random_exact_povm(
            len(counts),
            len(support),
            seed=2309 + index,
        )
        controls.append(
            audit_arbitrary_measurement_reduction(
                f"NONCOVARIANT-HIGHER-RANK-{index}",
                counts,
                source_measurement_kind="random-exact-noncovariant-povm",
                original_effects=original,
            )
        )
    scaling = [
        arbitrary_measurement_scaling_record(n, power, 8)
        for n in (16, 32, 64, 128, 256, 512, 1024)
        for power in (0, 2, 4, 8)
    ]
    theorem = arbitrary_measurement_witness_theorem()
    unamplified = unamplified_reduction_contract()
    physical = [audit_physical_measurement_reduction(labels, modulus,
        original_effects=random_exact_povm(modulus, 1 << len(labels), seed=5900+i))
        for i, (modulus, labels) in enumerate(((2, (1, 1)), (8, (1, 2, 3, 0)),
                                             (8, (0, 0, 0, 0, 0, 0)), (5, (1, 4, 2))))]
    counterexample = physical_uniform_fiber_counterexample()
    failures = sum(
        not row.exact_arbitrary_measurement_reduction_verified
        for row in controls
    )
    failures += sum(not row["verified"] for row in physical)
    failures += int(not counterexample["uniform_fiber_inference_refuted"])
    verified = bool(
        failures == 0
        and all(row.higher_rank_effect_verified for row in controls)
        and any(row.initially_noncovariant_measurement for row in controls)
        and all(row.polynomial_bootstrap for row in scaling)
        and theorem.theorem_verified
    )
    return DCPArbitraryMeasurementWitnessReductionReport(
        created_at=utc_now(),
        theorem_contract={
            "ensemble": "public-label cyclic DCP phase states in the full Boolean assignment space",
            "input_measurement": "arbitrary exact accessible standard-circuit POVM",
            "symmetrization": theorem.coherent_symmetrization,
            "cleaned_subanalysis": theorem.cleaned_subanalysis,
            "filter": theorem.fourier_diagonal_filter,
            "average_transfer": theorem.average_success_transfer,
            "planted_transfer": theorem.planted_average_success_transfer,
            "consequence": theorem.witness_consequence,
            "scope": theorem.scope_limit,
            "derivation_document": "research/DCP_PHYSICAL_WITNESS_REDUCTION.md",
            "evidence_level": "derived-review-pending; finite controls are not a proof checker",
            "fixed_label_success_promise": "known positive inverse-polynomial lower bound, uniform over symmetrized hidden shifts",
            "primary_wrapper": "UNAMPLIFIED; only label-averaged inverse-polynomial success needed, with squared success loss",
            "fixed_label_success_promise_scope": "optional normalized matching-garbage variant only",
            "theorem_and_scaling_records_scope": "optional normalized matching-garbage variant; unamplified_reduction is the primary constant-call construction",
            "uniform_fiber_inference": "retracted for arbitrary physical POVMs; valid only under an additional preserved-span condition",
            "occupancy_assumption_used": False,
        },
        finite_controls=controls,
        physical_controls=physical,
        uniform_fiber_counterexample=counterexample,
        unamplified_reduction=unamplified,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "symmetrize_arbitrary_measurement_without_success_loss",
                "resolved": verified,
                "resolution": (
                    "A coherent random cyclic shift makes every correct branch "
                    "have the original average success and preserves circuit access."
                ),
            },
            {
                "obligation": "extract_rank_one_correct_branch_from_higher_rank_effects",
                "resolved": verified,
                "resolution": (
                    "Bootstrapped matching garbage gives eta_d=E_d psi_d/sqrt(p) "
                    "for any effect rank."
                ),
            },
            {
                "obligation": "convert_cleaned_subanalysis_to_fiber_supported_witness",
                "resolved": verified,
                "resolution": (
                    "Cyclic covariance separates full residue eigenspaces. The inverse "
                    "heralds P_s eta_0/||P_s eta_0||, not necessarily the uniform fiber."
                ),
            },
            {
                "obligation": "transfer_decoder_success_to_uniform_legal_targets",
                "resolved": verified,
                "resolution": (
                    "Cauchy--Schwarz gives average heralding probability at "
                    "least p, with no fiber-occupancy regularity assumption."
                ),
            },
            {
                "obligation": "transfer_decoder_success_directly_to_planted_inversion",
                "resolved": verified,
                "resolution": (
                    "Weighted Cauchy--Schwarz gives E_planted q_s>=(N/L)p>=p "
                    "for every label tuple, without a density-one or occupancy assumption."
                ),
            },
            {
                "obligation": "remove_standard_circuit_approximation_semantics_loophole",
                "resolved": True,
                "resolution": (
                    "The executed reversible decoder defines an exact POVM. A "
                    "hybrid over O(p^-1/2 log(1/epsilon)) wrapper calls preserves "
                    "at least 3p/4 success at inverse-polynomial gate precision."
                ),
            },
            {
                "obligation": "prepare_uniform_fiber_from_arbitrary_physical_effects",
                "resolved": False,
                "resolution": "REFUTED in general: the exact two-qubit counterexample leaves the uniform-fiber span. Only witness support is guaranteed.",
            },
            {
                "obligation": "transfer_only_label_averaged_success_without_bootstrap",
                "resolved": verified,
                "resolution": "The unamplified compute-copy-uncompute wrapper works at every p including zero and gives q-average>=p^2. Jensen yields label-average witness success>=pbar^2 without estimating p or selecting labels.",
            },
            {
                "obligation": "reduce_inaccessible_noisy_or_external_channels",
                "resolved": False,
                "resolution": (
                    "The bootstrap uses the implemented dilation and its inverse; "
                    "a physical environment that cannot be retained or reversed "
                    "is outside the standard quantum-circuit model."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Use a noncovariant measurement to evade Fourier fibers.",
                "resolved": True,
                "resolution": (
                    "Coherent random-shift symmetrization preserves average "
                    "success and remains an accessible standard circuit."
                ),
            },
            {
                "objection": "Use higher-rank effects so outcome garbage depends on the input.",
                "resolved": True,
                "resolution": (
                    "Only the matching known-state garbage direction is needed; "
                    "cleaning it extracts E_d psi_d/sqrt(p) exactly."
                ),
            },
            {
                "objection": "The extracted filter may vanish on many target residues.",
                "resolved": True,
                "resolution": (
                    "Per-target success may vanish, but its uniform-legal average "
                    "is at least the claimed decoding success. The theorem does "
                    "not falsely claim a per-target guarantee."
                ),
            },
            {
                "objection": "Uniform-legal targets are not the standard planted inversion law.",
                "resolved": True,
                "resolution": (
                    "A direct weighted Cauchy--Schwarz inequality gives planted "
                    "success at least (N/L)p, without transferring through uniform-legal targets."
                ),
            },
            {
                "objection": "The proof assumes the PGM or rank-one completeness.",
                "resolved": True,
                "resolution": (
                    "Neither is used. Positivity, exact POVM completeness, "
                    "covariant symmetrization, and accessible dilation suffice."
                ),
            },
            {
                "objection": "All input states lie in the uniform-fiber span, so the physical inverse stays there.",
                "resolved": False,
                "resolution": "False. Full-space effects can leak from that span. The counterexample gives target-zero witness 00 with probability one instead of a uniform 00/11 superposition. The repaired proof needs only fiber support.",
            },
            {
                "objection": "This proves no efficient DCP measurement exists.",
                "resolved": False,
                "resolution": (
                    "No. It proves that such a measurement would constitute an "
                    "average subset-sum witness procedure under a fixed-label success promise, not a hardness theorem or a new algorithm."
                ),
            },
            {
                "objection": "Call the circuit an approximate PGM to evade exactness.",
                "resolved": True,
                "resolution": (
                    "The reduction never compares it with the PGM. It applies to "
                    "the circuit's actual effects and actual decoding success; "
                    "only wrapper synthesis error is charged by a hybrid bound."
                ),
            },
        ],
        headline_metrics={
            "arbitrary_exact_measurement_to_witness_theorem_count": int(verified),
            "noncovariant_symmetrization_theorem_count": int(verified),
            "higher_rank_correct_branch_extraction_theorem_count": int(verified),
            "uniform_legal_average_success_transfer_theorem_count": int(verified),
            "planted_average_inversion_transfer_theorem_count": int(verified),
            "finite_control_count": len(controls),
            "full_physical_space_control_count": len(physical)+1,
            "uniform_fiber_inference_counterexample_count": int(counterexample["uniform_fiber_inference_refuted"]),
            "occupancy_free_planted_transfer_derived": int(verified),
            "unamplified_label_average_transfer_derived": int(verified),
            "finite_control_failure_count": failures,
            "higher_rank_control_count": sum(
                row.higher_rank_effect_verified for row in controls
            ),
            "initially_noncovariant_control_count": sum(
                row.initially_noncovariant_measurement for row in controls
            ),
            "maximum_symmetrized_success_spread": max(
                row.symmetrized_success_spread for row in controls
            ),
            "maximum_qft_diagonal_filter_residual": max(
                row.qft_diagonal_filter_residual for row in controls
            ),
            "minimum_average_witness_to_decoder_success_ratio": min(
                row.uniform_legal_average_target_preparation_probability
                / row.source_measurement_average_success
                for row in controls
            ),
            "minimum_planted_to_scaled_legal_transfer_ratio": min(
                row.planted_average_target_preparation_probability
                / (
                    row.legal_support_to_assignment_ratio
                    * row.uniform_legal_average_target_preparation_probability
                )
                for row in controls
            ),
            "polynomial_scaling_row_count": sum(
                row.polynomial_bootstrap for row in scaling
            ),
            "standard_circuit_approximation_semantics_closure_count": int(verified),
            "robust_wrapper_scaling_row_count": sum(
                row.inverse_polynomial_wrapper_precision_sufficient
                and row.robust_average_witness_success_lower_bound > 0
                for row in scaling
            ),
            "inaccessible_noisy_channel_reduction_count": 0,
            "per_target_bounded_error_witness_solver_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "physical_residue_fiber_witness_reduction_derived": verified,
            "arbitrary_measurement_implies_uniform_fiber_preparation": False,
            "occupancy_free_planted_success_transfer_derived": verified,
            "label_average_only_bootstrap_proved": False,
            "unamplified_label_average_success_transfer_derived": verified,
            "independently_reviewed": False,
            "novelty_established": False,
            "accessible_exact_non_pgm_measurement_shortcut_open": False,
            "accessible_exact_higher_rank_measurement_shortcut_open": False,
            "accessible_exact_noncovariant_measurement_shortcut_open": False,
            "arbitrary_exact_measurement_implies_average_witness_procedure": verified,
            "arbitrary_exact_measurement_implies_planted_inversion_procedure": verified,
            "approximation_to_ideal_standard_circuit_measurement_is_loophole": False,
            "standard_wrapper_gate_synthesis_robust": True,
            "inaccessible_noisy_channel_route_closed": False,
            "per_target_bounded_error_witness_solver_proved": False,
            "polynomial_dcp_measurement_constructed": False,
            "polynomial_average_subset_sum_witness_solver_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "For an accessible state-only decoder/inverse, unamplified compute-copy-uncompute "
                "prepares a witness-supported state, not a uniform fiber. Both target laws have "
                "success >=(N/L)p^2, and label-averaged success is >=pbar^2 without estimating p. "
                "The optional normalized variant gives (N/L)p with bootstrap cost. No new solver, "
                "hardness claim, independent review, or per-target guarantee is supplied."
            ),
        },
        status=(
            "physical-witness-reduction-derived-review-pending"
            if verified
            else "arbitrary-measurement-reduction-certificate-failure"
        ),
        summary=(
            "Repaired the arbitrary-measurement reduction in the full assignment space: "
            "a physical inverse need not prepare a uniform fiber, but supports valid target "
            "witnesses. An unamplified compute-copy-uncompute wrapper gives planted and "
            "uniform-legal success >=pbar^2 over any public-label law, with two decoder/inverse "
            "calls and no success estimation or occupancy assumption. Review pending."
        ),
        falsifiers_triggered=[
            "The earlier inference from arbitrary physical effects to UNIFORM fiber preparation is false; its full-space counterexample is retained.",
            "Initial noncovariance is removable without average-success loss by an accessible coherent symmetrization.",
            "The cleaned correct branch need not be a full POVM; its Fourier-diagonal inverse already suffices on average.",
            "Planted witness success is bounded directly by (N/L)p for every label tuple; an occupancy theorem is unnecessary for this step.",
            "Approximation to a named ideal POVM is not a loophole because the executed circuit has exact effects.",
            "The repaired reduction is not an entanglement lower bound for uniform-fiber preparation and must not inherit those exclusions.",
        ],
    )


def write_arbitrary_measurement_witness_reduction_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-DHS-DCP-ARBITRARY-MEASUREMENT-WITNESS-REDUCTION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    if kwargs:
        raise TypeError(f"unexpected report arguments: {sorted(kwargs)}")
    payload = asdict(run_arbitrary_measurement_witness_reduction())
    payload["artifacts"] = {"report": str(path), "derivation": "research/DCP_PHYSICAL_WITNESS_REDUCTION.md"}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    if write_registry:
        upsert_experiment_result(ExperimentResultRecord(
            id=registry_result_id or f"RESULT-{registry_experiment_id}-COSET",
            experiment_id=registry_experiment_id, candidate_id=registry_candidate_id,
            created_at=payload["created_at"], status=payload["status"],
            summary=payload["summary"], metrics=payload["headline_metrics"],
            falsifiers_triggered=payload["falsifiers_triggered"], artifacts=payload["artifacts"]))
        if payload["uniform_fiber_counterexample"]["uniform_fiber_inference_refuted"] is True:
            upsert_negative_result(NegativeResultRecord(
                id="DCP-ARBITRARY-PHYSICAL-UNIFORM-FIBER-INFERENCE", source=str(path),
                claim="The accessible inverse of an arbitrary useful physical DCP measurement prepares a uniform subset-sum fiber.",
                reason_invalid="The N=2, labels=(1,1) rational POVM has success 1/2. Its unamplified inverse has uniform-span leakage squared 1/8 (1/4 after matching-branch normalization) and target-zero conditional output 00 with certainty instead of the uniform 00/11 state.",
                lesson="Full-space Fourier inversion guarantees fiber SUPPORTED witnesses, not uniform sampling. The witness reduction survives; uniform-fiber entanglement exclusions cannot be transferred through it.",
                applies_to=[registry_candidate_id], evidence={"artifact": str(path), "scope": "correction of a proof inference, not a DCP no-go", "review_status": "derived-review-pending"}))
    return payload


if __name__ == "__main__":
    report = write_arbitrary_measurement_witness_reduction_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
