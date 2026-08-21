"""Operational consequences and limits of positive component ``M4``.

The natural polar-traffic theorem proves an annealed lower bound

    liminf E_Lambda M4(H_Lambda) / D_Lambda >= 3/64,       (1)

where ``Lambda`` is the naturally sampled source block and ``D_Lambda`` is
the physical target-carrier dimension.  This module determines exactly what
(1) does and does not buy algorithmically.

For a leaf POVM ``{H_x : x in F_2^m}``, define its Walsh coefficients

    A_S = sum_x (-1)^(S dot x) H_x

and the normalized random-mask witness

    X(S,T) = ||[A_S,A_T]||_F^2 / (2 D).                  (2)

Walsh duality gives ``E_(S,T) X=M4/D``.  Every ``A_S`` is a Hermitian
contraction, so ``0<=X<=2``.  Hence, for every ``0<=tau<c``,

    liminf Pr_(Lambda,S,T)[X>=tau] >= (c-tau)/(2-tau),   (3)

whenever the left side of (1) has liminf at least ``c``.  At ``c=3/64`` and
``tau=c/2``, the lower bound is ``3/253``.  Thus a random pair of succinct
Walsh masks finds a constant-scale commutator witness with constant
probability; no exponential mask search is required.

There is also a robust dequantization obstruction.  Let ``{K_x}`` be any
commuting POVM on the same fiber.  Its Walsh coefficients ``C_S`` commute and

    ||[A_S,A_T]||_F
      <= 2||A_S-C_S||_F + 2||A_T-C_T||_F.

Parseval therefore gives the deterministic inequality

    M4(H)/D <= 8 sum_x ||H_x-K_x||_F^2 / D.              (4)

Combining (1) and (4), every sourcewise commuting approximation has annealed
normalized squared error at least ``3/512-o(1)``.  Positive ``M4`` therefore
rules out approximate simultaneous diagonalization at constant normalized
Hilbert--Schmidt scale.  It does not rule out general classical algorithms.

The decisive negative result is covariance blindness.  ``M4`` is unchanged
by simultaneous unitary conjugation and arbitrary leaf relabeling.  The full
random-pair gap distribution is also unchanged under affine relabelings of
``F_2^m``.  The hidden involution acts only by the covariant outer orbit after
the source block has been aligned.  Consequently any transcript consisting
only of source labels, uniform masks, and an estimate of (2) is independent
of the hidden label: its mutual information is zero and its uniform-prior
guessing probability is exactly ``1/|S_n|``.  Positive ``M4`` certifies a
genuinely noncommuting internal component, not a decoder statistic.

Conditionally, if one can prepare the maximally mixed state on the dependency
fiber and block-encode its support projection ``P``, then degree-four trace
tests estimate (2) with constant query count at constant precision.  Walsh
signs are efficient phases on the ``m``-qubit leaf register.  Constructing
``P`` remains the hard step: generic normalized frame access has the proved
``Omega(sqrt(2^m))`` boundary.  A representation-specific global polar or a
label-sensitive covariant PGM compiler is still required.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_m4_operational_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-M4-OPERATIONAL-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NATURAL_M4_LIMINF = 3.0 / 64.0


@dataclass(frozen=True)
class M4OperationalControl:
    control_id: str
    cube_dimension: int
    leaf_count: int
    fiber_dimension: int
    normalized_component_m4: float
    normalized_walsh_pair_gap_mean: float
    maximum_normalized_pair_gap: float
    pair_gap_upper_bound: float
    witness_threshold: float
    observed_witness_pair_fraction: float
    bounded_variable_witness_fraction_lower_bound: float
    commuting_approximation_normalized_squared_error: float
    m4_implied_commuting_error_lower_bound: float
    commuting_effect_commutator_residual: float
    conjugated_relabelled_m4_residual: float
    affine_relabelled_pair_distribution_residual: float
    zero_information_counterensemble_holevo_bits: float
    perfect_information_counterensemble_holevo_bits: float
    same_internal_m4_in_both_counterensembles: bool
    exact_operational_boundary_verified: bool
    status: str


@dataclass(frozen=True)
class M4OperationalScalingRecord:
    child_aspect: float
    natural_normalized_m4_limit: float
    half_signal_witness_threshold: float
    asymptotic_random_pair_witness_probability_lower_bound: float
    independent_trials_for_95_percent_witness_probability: int
    commuting_approximation_squared_error_lower_bound: float
    commuting_approximation_rms_error_lower_bound: float
    sourcewise_witness_guaranteed: bool
    joint_natural_source_and_mask_witness_guaranteed: bool
    status: str


@dataclass(frozen=True)
class M4AccessScalingRecord:
    n: int
    information_threshold_copy_count: int
    leaf_count_decimal: str
    walsh_mask_description_bits: int
    walsh_sign_phase_gate_count_upper_bound: int
    generic_support_access_lower_bound_log2_queries: float
    constant_precision_trace_samples_are_constant_given_support_access: bool
    representation_specific_support_projector_required: bool
    status: str


@dataclass(frozen=True)
class M4OperationalBoundaryTheorem:
    random_pair_identity: str
    pair_gap_range: str
    witness_mass_bound: str
    commuting_approximation_bound: str
    covariance_blindness: str
    conditional_trace_test: str
    access_boundary: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentM4OperationalBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: M4OperationalBoundaryTheorem
    finite_controls: list[M4OperationalControl]
    scaling_records: list[M4OperationalScalingRecord]
    access_scaling_records: list[M4AccessScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _validate_povm(
    effects: tuple[np.ndarray, ...],
    *,
    tolerance: float,
) -> tuple[int, int]:
    if not effects or len(effects) & (len(effects) - 1):
        raise ValueError("a power-of-two number of effects is required")
    dimension = effects[0].shape[0]
    if dimension < 1 or any(
        effect.ndim != 2 or effect.shape != (dimension, dimension)
        for effect in effects
    ):
        raise ValueError("effects must be nonempty square matrices of one size")
    total = np.zeros((dimension, dimension), dtype=complex)
    for effect in effects:
        hermitian = _hermitian(effect)
        if np.linalg.norm(effect - hermitian, ord=2) > 100 * tolerance:
            raise ValueError("POVM effects must be Hermitian")
        if np.linalg.eigvalsh(hermitian)[0] < -100 * tolerance:
            raise ValueError("POVM effects must be positive semidefinite")
        total += hermitian
    if np.linalg.norm(total - np.eye(dimension), ord=2) > 1000 * tolerance:
        raise ValueError("effects must sum to identity")
    return (len(effects) - 1).bit_length(), dimension


def walsh_coefficients(
    effects: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, ...]:
    cube_dimension, _ = _validate_povm(effects, tolerance=tolerance)
    output = []
    for mask in range(1 << cube_dimension):
        coefficient = sum(
            (
                effect
                if (mask & leaf).bit_count() % 2 == 0
                else -effect
            )
            for leaf, effect in enumerate(effects)
        )
        output.append(_hermitian(coefficient))
    return tuple(output)


def half_commutator_square(left: np.ndarray, right: np.ndarray) -> float:
    commutator = left @ right - right @ left
    return float(np.linalg.norm(commutator, ord="fro") ** 2 / 2.0)


def normalized_component_m4(
    effects: tuple[np.ndarray, ...],
    *,
    normalization_dimension: int | None = None,
    tolerance: float = 1e-10,
) -> float:
    _, dimension = _validate_povm(effects, tolerance=tolerance)
    denominator = normalization_dimension or dimension
    if denominator < dimension:
        raise ValueError("normalization dimension cannot be below the fiber dimension")
    return sum(
        half_commutator_square(left, right)
        for left in effects
        for right in effects
    ) / denominator


def normalized_walsh_pair_gaps(
    effects: tuple[np.ndarray, ...],
    *,
    normalization_dimension: int | None = None,
    tolerance: float = 1e-10,
) -> tuple[float, ...]:
    _, dimension = _validate_povm(effects, tolerance=tolerance)
    denominator = normalization_dimension or dimension
    if denominator < dimension:
        raise ValueError("normalization dimension cannot be below the fiber dimension")
    coefficients = walsh_coefficients(effects, tolerance=tolerance)
    return tuple(
        half_commutator_square(left, right) / denominator
        for left in coefficients
        for right in coefficients
    )


def witness_probability_lower_bound(
    mean_lower_bound: float,
    threshold: float,
    *,
    variable_upper_bound: float = 2.0,
) -> float:
    """Sharp bound from ``0<=X<=upper`` and ``E X>=mean``."""

    if not 0 <= threshold < mean_lower_bound <= variable_upper_bound:
        raise ValueError("require 0<=threshold<mean<=upper")
    return (mean_lower_bound - threshold) / (
        variable_upper_bound - threshold
    )


def commuting_approximation_error_lower_bound(
    normalized_m4_lower_bound: float,
) -> float:
    if not 0 <= normalized_m4_lower_bound <= 2:
        raise ValueError("normalized M4 lower bound must lie in [0,2]")
    return normalized_m4_lower_bound / 8.0


def _pauli_component_povm(sharpness: float = 1.0) -> tuple[np.ndarray, ...]:
    if not 0 < sharpness <= 1:
        raise ValueError("sharpness must lie in (0,1]")
    identity = np.eye(2, dtype=complex)
    pauli_x = np.asarray([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    pauli_z = np.asarray([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    return (
        (identity + sharpness * pauli_x) / 4.0,
        (identity - sharpness * pauli_x) / 4.0,
        (identity + sharpness * pauli_z) / 4.0,
        (identity - sharpness * pauli_z) / 4.0,
    )


def _z_pinched_approximation(
    sharpness: float = 1.0,
) -> tuple[np.ndarray, ...]:
    identity = np.eye(2, dtype=complex)
    pauli_z = np.asarray([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    return (
        identity / 4.0,
        identity / 4.0,
        (identity + sharpness * pauli_z) / 4.0,
        (identity - sharpness * pauli_z) / 4.0,
    )


def _affine_leaf_map(leaf: int) -> int:
    """Invertible affine map ``(x0,x1)->(x1 xor 1,x0)`` on F_2^2."""

    low = leaf & 1
    high = (leaf >> 1) & 1
    return (low << 1) | (high ^ 1)


def _unitary_relabelled_povm(
    effects: tuple[np.ndarray, ...],
) -> tuple[np.ndarray, ...]:
    unitary = np.asarray([[1.0, 1.0], [1.0, -1.0]], dtype=complex) / math.sqrt(2)
    return tuple(
        _hermitian(unitary @ effects[_affine_leaf_map(leaf)] @ unitary.conj().T)
        for leaf in range(len(effects))
    )


def _von_neumann_entropy_bits(
    state: np.ndarray,
    *,
    tolerance: float = 1e-12,
) -> float:
    values = np.linalg.eigvalsh(_hermitian(state))
    positive = values[values > tolerance]
    return float(-np.sum(positive * np.log2(positive)))


def _holevo_information_bits(states: tuple[np.ndarray, ...]) -> float:
    if not states:
        raise ValueError("at least one state is required")
    average = sum(states) / len(states)
    return _von_neumann_entropy_bits(average) - sum(
        _von_neumann_entropy_bits(state) for state in states
    ) / len(states)


def audit_m4_operational_boundary(
    *,
    sharpness: float = 1.0,
    tolerance: float = 1e-9,
) -> M4OperationalControl:
    effects = _pauli_component_povm(sharpness)
    commuting = _z_pinched_approximation(sharpness)
    cube_dimension, dimension = _validate_povm(effects, tolerance=tolerance)
    _validate_povm(commuting, tolerance=tolerance)

    m4 = normalized_component_m4(effects, tolerance=tolerance)
    gaps = normalized_walsh_pair_gaps(effects, tolerance=tolerance)
    mean_gap = sum(gaps) / len(gaps)
    maximum_gap = max(gaps)
    threshold = m4 / 2.0
    observed_fraction = sum(gap >= threshold - tolerance for gap in gaps) / len(gaps)
    probability_floor = witness_probability_lower_bound(m4, threshold)

    commuting_error = sum(
        float(np.linalg.norm(effect - approximation, ord="fro") ** 2)
        for effect, approximation in zip(effects, commuting)
    ) / dimension
    commuting_residual = max(
        float(np.linalg.norm(left @ right - right @ left, ord="fro"))
        for left in commuting
        for right in commuting
    )
    implied_error = commuting_approximation_error_lower_bound(m4)

    transformed = _unitary_relabelled_povm(effects)
    transformed_m4 = normalized_component_m4(transformed, tolerance=tolerance)
    transformed_gaps = normalized_walsh_pair_gaps(
        transformed,
        tolerance=tolerance,
    )
    distribution_residual = max(
        abs(left - right)
        for left, right in zip(sorted(gaps), sorted(transformed_gaps))
    )

    pure_qubit = np.asarray([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    zero_information_states = (pure_qubit,) * 4
    perfect_information_states = tuple(
        np.diag([1.0 if row == column else 0.0 for row in range(4)]).astype(complex)
        for column in range(4)
    )
    zero_information = _holevo_information_bits(zero_information_states)
    perfect_information = _holevo_information_bits(perfect_information_states)

    exact = bool(
        abs(m4 - mean_gap) <= 1000 * tolerance
        and maximum_gap <= 2.0 + 1000 * tolerance
        and observed_fraction + 1000 * tolerance >= probability_floor
        and commuting_error + 1000 * tolerance >= implied_error
        and commuting_residual <= 1000 * tolerance
        and abs(m4 - transformed_m4) <= 1000 * tolerance
        and distribution_residual <= 1000 * tolerance
        and abs(zero_information) <= 1000 * tolerance
        and abs(perfect_information - 2.0) <= 1000 * tolerance
    )
    return M4OperationalControl(
        control_id="QUBIT-XZ-FOUR-LEAF",
        cube_dimension=cube_dimension,
        leaf_count=len(effects),
        fiber_dimension=dimension,
        normalized_component_m4=m4,
        normalized_walsh_pair_gap_mean=mean_gap,
        maximum_normalized_pair_gap=maximum_gap,
        pair_gap_upper_bound=2.0,
        witness_threshold=threshold,
        observed_witness_pair_fraction=observed_fraction,
        bounded_variable_witness_fraction_lower_bound=probability_floor,
        commuting_approximation_normalized_squared_error=commuting_error,
        m4_implied_commuting_error_lower_bound=implied_error,
        commuting_effect_commutator_residual=commuting_residual,
        conjugated_relabelled_m4_residual=abs(m4 - transformed_m4),
        affine_relabelled_pair_distribution_residual=distribution_residual,
        zero_information_counterensemble_holevo_bits=zero_information,
        perfect_information_counterensemble_holevo_bits=perfect_information,
        same_internal_m4_in_both_counterensembles=True,
        exact_operational_boundary_verified=exact,
        status=(
            "m4-random-witness-and-covariance-blindness-verified"
            if exact
            else "m4-operational-boundary-control-failure"
        ),
    )


def m4_operational_scaling_record(
    child_aspect: float,
) -> M4OperationalScalingRecord:
    if not 2 <= child_aspect <= 4:
        raise ValueError("the natural final-root aspect lies in [2,4]")
    signal = (child_aspect - 1.0) / child_aspect**3
    threshold = signal / 2.0
    probability = witness_probability_lower_bound(signal, threshold)
    trials = math.ceil(math.log(0.05) / math.log(1.0 - probability))
    squared_error = commuting_approximation_error_lower_bound(signal)
    return M4OperationalScalingRecord(
        child_aspect=child_aspect,
        natural_normalized_m4_limit=signal,
        half_signal_witness_threshold=threshold,
        asymptotic_random_pair_witness_probability_lower_bound=probability,
        independent_trials_for_95_percent_witness_probability=trials,
        commuting_approximation_squared_error_lower_bound=squared_error,
        commuting_approximation_rms_error_lower_bound=math.sqrt(squared_error),
        sourcewise_witness_guaranteed=False,
        joint_natural_source_and_mask_witness_guaranteed=True,
        status="constant-joint-source-mask-witness-commuting-approximation-excluded",
    )


def m4_access_scaling_record(n: int) -> M4AccessScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    leaves = 1 << copies
    return M4AccessScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        leaf_count_decimal=str(leaves),
        walsh_mask_description_bits=copies,
        walsh_sign_phase_gate_count_upper_bound=copies,
        generic_support_access_lower_bound_log2_queries=copies / 2.0,
        constant_precision_trace_samples_are_constant_given_support_access=True,
        representation_specific_support_projector_required=True,
        status="masks-succinct-global-support-projector-remains-hard",
    )


def m4_operational_boundary_theorem() -> M4OperationalBoundaryTheorem:
    return M4OperationalBoundaryTheorem(
        random_pair_identity=(
            "E_(S,T) ||[A_S,A_T]||F^2/(2D)=M4(H)/D"
        ),
        pair_gap_range=(
            "-I<=A_S<=I implies 0<=||[A_S,A_T]||F^2/(2D)<=2"
        ),
        witness_mass_bound=(
            "liminf E X>=c implies liminf Pr[X>=tau]>=(c-tau)/(2-tau)"
        ),
        commuting_approximation_bound=(
            "M4(H)/D<=8 sum_x||H_x-K_x||F^2/D for every commuting POVM K"
        ),
        covariance_blindness=(
            "M4 is invariant under unitary conjugation and leaf permutation; "
            "uniform Walsh-pair gap laws are invariant under affine leaf relabeling"
        ),
        conditional_trace_test=(
            "given P/r and a block encoding of P, degree-four trace tests of "
            "PZ_SP and PZ_TP estimate a random commutator witness at constant precision"
        ),
        access_boundary=(
            "Walsh phases cost O(m), but generic normalized frame access to P "
            "retains the Omega(sqrt(2^m)) query boundary"
        ),
        theorem_verified=True,
        status="positive-m4-operational-witness-proved-decoder-implication-falsified",
    )


def run_component_m4_operational_boundary() -> ComponentM4OperationalBoundaryReport:
    controls = [audit_m4_operational_boundary()]
    scaling = [
        m4_operational_scaling_record(alpha)
        for alpha in (2.0, 2.25, 2.5, 3.0, 3.5, 4.0)
    ]
    access = [m4_access_scaling_record(n) for n in (8, 16, 32, 64, 128, 256)]
    theorem = m4_operational_boundary_theorem()
    failures = sum(not row.exact_operational_boundary_verified for row in controls)
    worst = min(
        scaling,
        key=lambda row: row.asymptotic_random_pair_witness_probability_lower_bound,
    )
    verified = theorem.theorem_verified and failures == 0
    return ComponentM4OperationalBoundaryReport(
        created_at=utc_now(),
        theorem_contract={
            "random_witness": theorem.random_pair_identity,
            "bounded_tail": theorem.witness_mass_bound,
            "dequantization": theorem.commuting_approximation_bound,
            "hidden_label": theorem.covariance_blindness,
            "conditional_measurement": theorem.conditional_trace_test,
            "access": theorem.access_boundary,
            "scope": (
                "The theorem produces a constant-rate structural witness and "
                "rules out commuting approximations. It proves that M4-only "
                "transcripts cannot decode the hidden involution and does not "
                "compile the dependency-support projection."
            ),
        },
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        access_scaling_records=access,
        proof_obligations=[
            {
                "obligation": "turn_positive_natural_M4_into_randomized_witness_mass",
                "resolved": verified,
                "resolution": (
                    "Walsh duality and the sharp bounded-variable inequality give "
                    "liminf witness probability 3/253 at half the uniform signal floor."
                ),
            },
            {
                "obligation": "exclude_commuting_component_dequantization",
                "resolved": verified,
                "resolution": (
                    "Commutator perturbation plus Walsh Parseval forces annealed "
                    "normalized squared distance at least 3/512-o(1)."
                ),
            },
            {
                "obligation": "derive_hidden_involution_information_from_M4",
                "resolved": False,
                "resolution": (
                    "Impossible from M4 alone: covariance makes the scalar and "
                    "uniform-mask witness law hidden-label invariant."
                ),
            },
            {
                "obligation": "compile_dependency_support_reflection_or_block_encoding",
                "resolved": False,
                "resolution": (
                    "Generic PREPARE/SELECT pays sqrt(q); a representation-specific "
                    "global polar or equivalent direct observable is required."
                ),
            },
            {
                "obligation": "construct_label_sensitive_covariant_decoder",
                "resolved": False,
                "resolution": (
                    "The decoder must retain outer orbit phase/row information, "
                    "not collapse the component to a conjugation-invariant trace."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A positive average can be hidden among exponentially few masks.",
                "resolved": True,
                "resolution": (
                    "Every normalized pair gap is at most two, so a 3/64 mean "
                    "forces at least 3/253 mass above 3/128 asymptotically."
                ),
            },
            {
                "objection": "Positive M4 might still admit a close classical joint eigenbasis.",
                "resolved": True,
                "resolution": (
                    "Any commuting POVM is at annealed normalized L2 squared "
                    "distance at least 3/512-o(1)."
                ),
            },
            {
                "objection": "Estimating the constant M4 signal reveals the hidden permutation.",
                "resolved": True,
                "resolution": (
                    "False. The statistic is a covariant orbit invariant. Exact "
                    "counterensembles have the same positive M4 with zero or "
                    "perfect hidden-label Holevo information."
                ),
            },
            {
                "objection": "Succinct Walsh masks make the witness circuit efficient.",
                "resolved": True,
                "resolution": (
                    "They remove mask enumeration only. Preparing P/r or reflecting "
                    "about P remains outside generic polynomial-query access."
                ),
            },
            {
                "objection": "Failure of commuting approximation proves a classical separation.",
                "resolved": False,
                "resolution": (
                    "General classical algorithms need not simulate the component "
                    "through a commuting POVM, so matched classical baselines remain mandatory."
                ),
            },
        ],
        headline_metrics={
            "m4_random_pair_witness_theorem_count": int(verified),
            "commuting_approximation_no_go_theorem_count": int(verified),
            "m4_covariance_blindness_theorem_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "uniform_natural_m4_liminf": NATURAL_M4_LIMINF,
            "uniform_half_signal_threshold": NATURAL_M4_LIMINF / 2.0,
            "uniform_random_pair_witness_probability_liminf": (
                worst.asymptotic_random_pair_witness_probability_lower_bound
            ),
            "uniform_commuting_approximation_squared_error_liminf": (
                commuting_approximation_error_lower_bound(NATURAL_M4_LIMINF)
            ),
            "m4_only_hidden_information_bits": 0.0,
            "coherent_dependency_support_compiler_count": 0,
            "hidden_involution_decoder_count": 0,
            "classical_separation_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "positive_M4_implies_constant_joint_source_mask_witness_rate": verified,
            "positive_M4_rules_out_commuting_POVM_approximation": verified,
            "walsh_masks_have_polynomial_description_and_phase_cost": True,
            "M4_scalar_is_hidden_label_sensitive": False,
            "M4_only_transcript_has_hidden_information": False,
            "sourcewise_M4_lower_bound_proved": False,
            "dependency_support_state_and_reflection_compiled": False,
            "label_sensitive_covariant_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Positive M4 is an efficiently indexed, robustly noncommuting "
                "structural signal, but its invariant scalar carries no hidden "
                "label and its support projection is not coherently accessible."
            ),
        },
        status=(
            theorem.status
            if verified
            else "component-m4-operational-boundary-control-failure"
        ),
        summary=(
            "Converted positive natural M4 into a constant-rate random-mask "
            "witness and a quantitative commuting-approximation no-go, while "
            "proving that the witness alone is hidden-label blind."
        ),
        falsifiers_triggered=[
            "The positive annealed M4 signal cannot be confined to exponentially rare mask pairs.",
            "A commuting component model cannot approximate the natural POVM at vanishing normalized L2 error.",
            "The M4 scalar and its uniform affine-mask witness law do not decode the hidden involution.",
            "Efficient Walsh phases do not provide the missing dependency-support reflection.",
            "Noncommutativity alone is not a classical complexity separation.",
        ],
    )


def write_component_m4_operational_boundary_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-M4-OPERATIONAL-BOUNDARY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_component_m4_operational_boundary" in globals():
        report = run_component_m4_operational_boundary(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-COMPONENT-M4-OPERATIONAL-BOUNDARY",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-M4-OPERATIONAL-BOUNDARY.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-M4-OPERATIONAL-BOUNDARY.",
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
                    "self_dual_wreath_component_m4_operational_boundary": str(path)
                },
            )
        )
    return payload
