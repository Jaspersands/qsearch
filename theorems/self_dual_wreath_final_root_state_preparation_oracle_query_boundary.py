"""Coherent endpoint preparation has a square-root query barrier unless its
unitary extension leaks more than the prepared program state.

The prior direct-contraction theorem deliberately left coherent oracle access
open.  This pass separates two oracle promises.

Reflection-only model
---------------------
For a canonical endpoint

    V_C = [sqrt(C); sqrt(I-C)],       |v_C>=|V_C>>/sqrt(D),

grant controlled queries to ``R_C=I-2|v_C><v_C|``.  Fix the Weyl shift ``X``
and ask for an ``alpha``-normalized block encoding of
``B_C=V_C X V_C^*``.

There is an exact hard pair.  Let ``C_0=I/2`` and change only the first
diagonal entry to ``b`` in ``C_1``, where ``b`` is any fixed number in
``(1/2,1)``.  If

    gamma = sqrt(b/2)+sqrt((1-b)/2),
    beta  = sqrt(2-2 gamma),

then

    <v_0|v_1> = 1-beta^2/(2D),
    ||v_0-v_1|| = beta/sqrt(D),
    ||B_0-B_1|| = beta.                                  (1)

The reflection distance is

    ||R_0-R_1|| = 2 sqrt(1-|<v_0|v_1>|^2)
                <= 2 beta/sqrt(D).                       (2)

Suppose a ``T``-query compiler produces a block ``C_i`` satisfying
``||alpha C_i-B_i||<=eta beta/2`` for both inputs.  A standard telescoping
hybrid argument bounds the distance between its two output unitaries by
``T||R_0-R_1||``, whereas their designated blocks differ by at least
``(1-eta)beta/alpha``.  Thus

    T >= (1-eta)sqrt(D)/(2 alpha).                        (3)

Constant normalization and constant relative accuracy therefore require
``Omega(sqrt(D))`` reflection queries.  At the logical dimensions forced by
the prior natural high-row theorem, this is a superpolynomial *worst-case
uniform-compiler* cost.  The hard pair is not claimed to occur with typical
free-Jacobi mass.

Preparation-unitary model
-------------------------
A bare preparation promise specifies only

    A_C |0> = |v_C>.                                     (4)

It does not specify the other columns.  For the hard pair above one can
choose valid extensions ``A_0,A_1`` with

    ||A_0-A_1|| = ||v_0-v_1|| = beta/sqrt(D).             (5)

The same hybrid proof yields the stronger worst-extension bound

    T >= (1-eta)sqrt(D)/alpha                            (6)

for any compiler required to work for every unitary extension satisfying
(4), even with controlled ``A_C`` and ``A_C^*`` queries.

But a friendly extension can encode a unitary dilation of ``B_C`` in columns
orthogonal to ``|0>`` while still satisfying (4).  A known top-left block of
one query then equals ``B_C`` at normalization one.  Hence ``A_C|0>=|v_C>``
alone does *not* define an extension-independent query problem: worst-case
extensions obey (6), while leaky extensions solve the task in one query.

The result closes reflection-only and extension-robust black-box preparation
as polynomial routes.  It does not lower-bound a particular structured
Schur/QFT/GPE preparation circuit whose full action is promised.  The next
positive route must expose and exploit that full typed action, and the next
negative route must state its extension promise explicitly.  No physical PGM,
decoder, classical separation, arbitrary-circuit lower bound, or speedup is
claimed.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import (
    ExperimentRecord,
    NegativeResultRecord,
    upsert_experiment,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_final_root_byproduct_covariance_no_go import (
    canonical_endpoint,
)
from self_dual_wreath_final_root_purification_naimark_program_boundary import (
    _psd_power,
    weyl_unitary_error_basis,
)
from self_dual_wreath_joint_character_natural_sector_mass import partition_number


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_final_root_state_preparation_oracle_query_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-"
    "STATE-PREPARATION-ORACLE-QUERY-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NEGATIVE_RESULT_ID = (
    "SCHUR-COMPANION-FINAL-ROOT-REFLECTION-AND-ROBUST-PREPARATION-"
    "SQRT-D-QUERY"
)
BBBV_PAPER_ID = "bennett-bernstein-brassard-vazirani-hybrid-1997"
BBBV_PAPER_URL = "https://arxiv.org/abs/quant-ph/9701001"
NIELSEN_CHUANG_PAPER_ID = "nielsen-chuang-programmable-gate-arrays-1997"
NIELSEN_CHUANG_PAPER_URL = "https://arxiv.org/abs/quant-ph/9703032"
DEFAULT_PERTURBED_EFFECT = 0.9
DEFAULT_RELATIVE_SEPARATION_ERROR = 0.1
DEFAULT_BLOCK_NORMALIZATION = 1.0


@dataclass(frozen=True)
class CanonicalEndpointOracleHardPairControl:
    logical_dimension: int
    output_dimension: int
    baseline_effect: float
    perturbed_effect: float
    changed_endpoint_column_overlap: float
    changed_endpoint_column_distance: float
    endpoint_isometry_residual: float
    canonical_endpoint_formula_residual: float
    normalized_program_overlap: float
    predicted_normalized_program_overlap: float
    normalized_program_state_distance: float
    predicted_normalized_program_state_distance: float
    reflection_oracle_distance: float
    predicted_reflection_oracle_distance: float
    close_preparation_oracle_distance: float
    predicted_close_preparation_oracle_distance: float
    preparation_state_residual: float
    fixed_weyl_byproduct_separation: float
    predicted_fixed_weyl_byproduct_separation: float
    block_normalization: float
    relative_separation_error: float
    per_instance_operator_error: float
    exact_reflection_query_lower_bound: float
    certified_reflection_query_lower_bound: float
    exact_robust_preparation_query_lower_bound: float
    certified_robust_preparation_query_lower_bound: float
    constant_normalization_reflection_query_is_omega_sqrt_dimension: bool
    all_extension_robust_preparation_query_is_omega_sqrt_dimension: bool
    exact_canonical_hard_pair_verified: bool
    status: str


@dataclass(frozen=True)
class PreparationExtensionGaugeControl:
    logical_dimension: int
    program_hilbert_dimension: int
    target_hilbert_dimension: int
    dilation_hilbert_dimension: int
    preparation_state_residual: float
    preparation_unitarity_residual: float
    leaked_block_encoding_residual: float
    leaked_block_normalization: float
    leaked_block_query_count: int
    same_prepared_state_extension_distance: float
    bare_first_column_promise_defines_extension_independent_query_complexity: bool
    one_query_leaky_extension_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalStatePreparationOracleScalingRecord:
    n: int
    partition_count_decimal: str
    natural_high_row_irrep_dimension_lower_bound_decimal: str
    natural_high_row_irrep_dimension_lower_bound_log2: float
    reflection_query_lower_bound: float
    robust_preparation_query_lower_bound: float
    reflection_query_lower_bound_log2_leading_term: float
    robust_preparation_query_lower_bound_log2_leading_term: float
    independent_source_high_row_mass_lower_bound: float
    retained_logical_dimension_same_factorial_exponent_proved: bool
    uniform_reflection_compiler_worst_case_superpolynomial_at_natural_dimension_scale: bool
    uniform_robust_preparation_compiler_worst_case_superpolynomial_at_natural_dimension_scale: bool
    particular_structured_preparation_circuit_lower_bound_proved: bool
    status: str


@dataclass(frozen=True)
class StatePreparationOracleQueryTheorem:
    canonical_hard_pair: str
    reflection_hybrid_bound: str
    close_preparation_extensions: str
    robust_preparation_hybrid_bound: str
    extension_gauge: str
    natural_consequence: str
    surviving_route: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class StatePreparationOracleQueryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: StatePreparationOracleQueryTheorem
    hard_pair_controls: list[CanonicalEndpointOracleHardPairControl]
    extension_gauge_controls: list[PreparationExtensionGaugeControl]
    scaling_records: list[NaturalStatePreparationOracleScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    primary_literature: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _program_vector(endpoint: np.ndarray) -> np.ndarray:
    value = np.asarray(endpoint, dtype=complex)
    if value.ndim != 2:
        raise ValueError("endpoint must be a matrix")
    dimension = value.shape[1]
    return (value / math.sqrt(dimension)).reshape(-1)


def _program_reflection(program_state: np.ndarray) -> np.ndarray:
    state = np.asarray(program_state, dtype=complex)
    if state.ndim != 1 or abs(float(np.linalg.norm(state)) - 1.0) > 1e-8:
        raise ValueError("program_state must be a normalized vector")
    return np.eye(state.size, dtype=complex) - 2.0 * np.outer(state, state.conj())


def canonical_endpoint_oracle_hard_pair(
    logical_dimension: int,
    *,
    perturbed_effect: float = DEFAULT_PERTURBED_EFFECT,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return ``C_0,C_1,V_0,V_1`` for the one-column canonical hard pair."""

    if logical_dimension < 2:
        raise ValueError("logical_dimension must be at least two")
    if not 0.5 < perturbed_effect < 1.0:
        raise ValueError("perturbed_effect must lie in (1/2,1)")
    baseline = 0.5 * np.eye(logical_dimension, dtype=complex)
    perturbed = baseline.copy()
    perturbed[0, 0] = perturbed_effect
    return (
        baseline,
        perturbed,
        canonical_endpoint(baseline),
        canonical_endpoint(perturbed),
    )


def _unitary_mapping_anchor_to_state(
    state: np.ndarray,
    *,
    tolerance: float = 1e-12,
) -> np.ndarray:
    """Return a Householder unitary sending the first basis vector to ``state``."""

    value = np.asarray(state, dtype=complex)
    if value.ndim != 1 or abs(float(np.linalg.norm(value)) - 1.0) > 1000 * tolerance:
        raise ValueError("state must be a normalized vector")
    anchor = np.zeros(value.size, dtype=complex)
    anchor[0] = 1.0
    phase = complex(np.vdot(anchor, value))
    if abs(phase.imag) > 100 * tolerance or phase.real < -100 * tolerance:
        raise ValueError("Householder helper requires nonnegative real anchor overlap")
    difference = anchor - value
    norm = float(np.linalg.norm(difference))
    if norm <= tolerance:
        return np.eye(value.size, dtype=complex)
    direction = difference / norm
    return np.eye(value.size, dtype=complex) - 2.0 * np.outer(
        direction,
        direction.conj(),
    )


def _minimal_state_rotation(
    first: np.ndarray,
    second: np.ndarray,
    *,
    tolerance: float = 1e-12,
) -> np.ndarray:
    """Return the identity-off-span rotation mapping ``first`` to ``second``."""

    left = np.asarray(first, dtype=complex)
    right = np.asarray(second, dtype=complex)
    if left.shape != right.shape or left.ndim != 1:
        raise ValueError("states must be vectors of the same size")
    if max(abs(float(np.linalg.norm(left)) - 1.0), abs(float(np.linalg.norm(right)) - 1.0)) > 1000 * tolerance:
        raise ValueError("states must be normalized")
    overlap = complex(np.vdot(left, right))
    if abs(overlap.imag) > 100 * tolerance or not -tolerance < overlap.real < 1 - tolerance:
        raise ValueError("states must have a real overlap strictly between zero and one")
    cosine = float(overlap.real)
    sine = math.sqrt(max(0.0, 1.0 - cosine**2))
    orthogonal = (right - cosine * left) / sine
    return (
        np.eye(left.size, dtype=complex)
        + (cosine - 1.0)
        * (np.outer(left, left.conj()) + np.outer(orthogonal, orthogonal.conj()))
        + sine
        * (np.outer(orthogonal, left.conj()) - np.outer(left, orthogonal.conj()))
    )


def _complete_isometry(
    prefix: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> np.ndarray:
    """Complete an exact orthonormal column prefix by Gram--Schmidt."""

    value = np.asarray(prefix, dtype=complex)
    if value.ndim != 2 or value.shape[1] > value.shape[0]:
        raise ValueError("prefix must have at most as many columns as rows")
    identity = np.eye(value.shape[1], dtype=complex)
    if np.linalg.norm(value.conj().T @ value - identity, ord=2) > 1000 * tolerance:
        raise ValueError("prefix columns must be orthonormal")
    columns = [value[:, index].copy() for index in range(value.shape[1])]
    for index in range(value.shape[0]):
        candidate = np.zeros(value.shape[0], dtype=complex)
        candidate[index] = 1.0
        for column in columns:
            candidate -= column * np.vdot(column, candidate)
        norm = float(np.linalg.norm(candidate))
        if norm > 100 * tolerance:
            columns.append(candidate / norm)
        if len(columns) == value.shape[0]:
            break
    if len(columns) != value.shape[0]:
        raise ValueError("failed to complete isometry")
    return np.column_stack(columns)


def _unitary_contraction_dilation(
    contraction: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> np.ndarray:
    """Return the Julia unitary with ``contraction`` as its top-left block."""

    value = np.asarray(contraction, dtype=complex)
    if value.ndim != 2 or value.shape[0] != value.shape[1]:
        raise ValueError("contraction must be square")
    if float(np.linalg.norm(value, ord=2)) > 1 + 100 * tolerance:
        raise ValueError("matrix must be a contraction")
    identity = np.eye(value.shape[0], dtype=complex)
    left_defect = _psd_power(
        identity - value @ value.conj().T,
        0.5,
        tolerance=tolerance,
    )
    right_defect = _psd_power(
        identity - value.conj().T @ value,
        0.5,
        tolerance=tolerance,
    )
    return np.block(
        [
            [value, left_defect],
            [right_defect, -value.conj().T],
        ]
    )


def _leaky_preparation_extension(
    program_state: np.ndarray,
    target: np.ndarray,
    domain_embedding: np.ndarray,
    range_embedding: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, np.ndarray]:
    """Build a valid preparation unitary whose known block encodes ``target``."""

    state = np.asarray(program_state, dtype=complex)
    value = np.asarray(target, dtype=complex)
    dilation = _unitary_contraction_dilation(value, tolerance=tolerance)
    dilation_dimension = dilation.shape[0]
    if domain_embedding.shape != (state.size, dilation_dimension):
        raise ValueError("domain embedding has the wrong shape")
    if range_embedding.shape != (state.size, dilation_dimension):
        raise ValueError("range embedding has the wrong shape")
    anchor = np.zeros(state.size, dtype=complex)
    anchor[0] = 1.0
    domain_prefix = np.column_stack((anchor, domain_embedding))
    range_prefix = np.column_stack((state, range_embedding @ dilation))
    domain_basis = _complete_isometry(domain_prefix, tolerance=tolerance)
    range_basis = _complete_isometry(range_prefix, tolerance=tolerance)
    oracle = range_basis @ domain_basis.conj().T
    return oracle, dilation


def audit_canonical_endpoint_oracle_hard_pair(
    logical_dimension: int,
    *,
    perturbed_effect: float = DEFAULT_PERTURBED_EFFECT,
    block_normalization: float = DEFAULT_BLOCK_NORMALIZATION,
    relative_separation_error: float = DEFAULT_RELATIVE_SEPARATION_ERROR,
    tolerance: float = 1e-9,
) -> CanonicalEndpointOracleHardPairControl:
    """Verify the hard pair and both hybrid-query lower bounds."""

    if not math.isfinite(block_normalization) or block_normalization < 1.0:
        raise ValueError("block_normalization must be at least one")
    if not 0 <= relative_separation_error < 1:
        raise ValueError("relative_separation_error must lie in [0,1)")
    effect_zero, effect_one, endpoint_zero, endpoint_one = (
        canonical_endpoint_oracle_hard_pair(
            logical_dimension,
            perturbed_effect=perturbed_effect,
        )
    )
    dimension = logical_dimension
    output_dimension = endpoint_zero.shape[0]
    identity = np.eye(dimension, dtype=complex)
    shift = weyl_unitary_error_basis(dimension)[dimension]
    program_zero = _program_vector(endpoint_zero)
    program_one = _program_vector(endpoint_one)
    reflection_zero = _program_reflection(program_zero)
    reflection_one = _program_reflection(program_one)

    column_zero = endpoint_zero[:, 0]
    column_one = endpoint_one[:, 0]
    gamma = float(np.vdot(column_zero, column_one).real)
    beta = float(np.linalg.norm(column_zero - column_one))
    predicted_gamma = math.sqrt(perturbed_effect / 2.0) + math.sqrt(
        (1.0 - perturbed_effect) / 2.0
    )
    predicted_beta = math.sqrt(2.0 - 2.0 * predicted_gamma)
    predicted_program_overlap = 1.0 - predicted_beta**2 / (2.0 * dimension)
    program_overlap = float(np.vdot(program_zero, program_one).real)
    program_distance = float(np.linalg.norm(program_zero - program_one))
    predicted_program_distance = predicted_beta / math.sqrt(dimension)
    reflection_distance = float(
        np.linalg.norm(reflection_zero - reflection_one, ord=2)
    )
    predicted_reflection_distance = 2.0 * math.sqrt(
        1.0 - predicted_program_overlap**2
    )

    anchor_preparation = _unitary_mapping_anchor_to_state(program_zero)
    minimal_rotation = _minimal_state_rotation(program_zero, program_one)
    second_preparation = minimal_rotation @ anchor_preparation
    preparation_distance = float(
        np.linalg.norm(anchor_preparation - second_preparation, ord=2)
    )
    preparation_state_residual = max(
        float(
            np.linalg.norm(
                anchor_preparation[:, 0] - program_zero,
            )
        ),
        float(np.linalg.norm(second_preparation[:, 0] - program_one)),
    )

    byproduct_zero = endpoint_zero @ shift @ endpoint_zero.conj().T
    byproduct_one = endpoint_one @ shift @ endpoint_one.conj().T
    byproduct_separation = float(
        np.linalg.norm(byproduct_zero - byproduct_one, ord=2)
    )
    error = relative_separation_error * predicted_beta / 2.0
    required_output_separation = (
        predicted_beta - 2.0 * error
    ) / block_normalization
    exact_reflection_lower = required_output_separation / reflection_distance
    exact_preparation_lower = required_output_separation / preparation_distance
    certified_reflection_lower = (
        (1.0 - relative_separation_error)
        * math.sqrt(dimension)
        / (2.0 * block_normalization)
    )
    certified_preparation_lower = (
        (1.0 - relative_separation_error)
        * math.sqrt(dimension)
        / block_normalization
    )
    endpoint_residual = max(
        float(
            np.linalg.norm(
                endpoint_zero.conj().T @ endpoint_zero - identity,
                ord=2,
            )
        ),
        float(
            np.linalg.norm(
                endpoint_one.conj().T @ endpoint_one - identity,
                ord=2,
            )
        ),
    )
    formula_residual = max(
        float(np.linalg.norm(endpoint_zero - canonical_endpoint(effect_zero), ord=2)),
        float(np.linalg.norm(endpoint_one - canonical_endpoint(effect_one), ord=2)),
    )
    verified = bool(
        endpoint_residual <= 100 * tolerance
        and formula_residual <= 100 * tolerance
        and abs(gamma - predicted_gamma) <= 100 * tolerance
        and abs(beta - predicted_beta) <= 100 * tolerance
        and abs(program_overlap - predicted_program_overlap) <= 100 * tolerance
        and abs(program_distance - predicted_program_distance) <= 100 * tolerance
        and abs(reflection_distance - predicted_reflection_distance) <= 100 * tolerance
        and abs(preparation_distance - predicted_program_distance) <= 100 * tolerance
        and preparation_state_residual <= 100 * tolerance
        and abs(byproduct_separation - predicted_beta) <= 100 * tolerance
        and exact_reflection_lower + 100 * tolerance >= certified_reflection_lower
        and exact_preparation_lower + 100 * tolerance >= certified_preparation_lower
    )
    return CanonicalEndpointOracleHardPairControl(
        logical_dimension=dimension,
        output_dimension=output_dimension,
        baseline_effect=0.5,
        perturbed_effect=perturbed_effect,
        changed_endpoint_column_overlap=gamma,
        changed_endpoint_column_distance=beta,
        endpoint_isometry_residual=endpoint_residual,
        canonical_endpoint_formula_residual=formula_residual,
        normalized_program_overlap=program_overlap,
        predicted_normalized_program_overlap=predicted_program_overlap,
        normalized_program_state_distance=program_distance,
        predicted_normalized_program_state_distance=predicted_program_distance,
        reflection_oracle_distance=reflection_distance,
        predicted_reflection_oracle_distance=predicted_reflection_distance,
        close_preparation_oracle_distance=preparation_distance,
        predicted_close_preparation_oracle_distance=predicted_program_distance,
        preparation_state_residual=preparation_state_residual,
        fixed_weyl_byproduct_separation=byproduct_separation,
        predicted_fixed_weyl_byproduct_separation=predicted_beta,
        block_normalization=block_normalization,
        relative_separation_error=relative_separation_error,
        per_instance_operator_error=error,
        exact_reflection_query_lower_bound=exact_reflection_lower,
        certified_reflection_query_lower_bound=certified_reflection_lower,
        exact_robust_preparation_query_lower_bound=exact_preparation_lower,
        certified_robust_preparation_query_lower_bound=certified_preparation_lower,
        constant_normalization_reflection_query_is_omega_sqrt_dimension=True,
        all_extension_robust_preparation_query_is_omega_sqrt_dimension=True,
        exact_canonical_hard_pair_verified=verified,
        status=(
            "exact-canonical-endpoint-oracle-sqrt-d-hard-pair"
            if verified
            else "canonical-endpoint-oracle-hard-pair-control-failure"
        ),
    )


def audit_preparation_extension_gauge(
    logical_dimension: int,
    *,
    perturbed_effect: float = DEFAULT_PERTURBED_EFFECT,
    tolerance: float = 1e-9,
) -> PreparationExtensionGaugeControl:
    """Exhibit a valid preparation extension leaking ``B_C`` in one query."""

    if logical_dimension < 3:
        raise ValueError("leaky-extension control requires dimension at least three")
    _, _, endpoint_zero, endpoint_one = canonical_endpoint_oracle_hard_pair(
        logical_dimension,
        perturbed_effect=perturbed_effect,
    )
    dimension = logical_dimension
    output_dimension = endpoint_zero.shape[0]
    program_zero = _program_vector(endpoint_zero)
    program_one = _program_vector(endpoint_one)
    program_dimension = program_zero.size
    shift = weyl_unitary_error_basis(dimension)[dimension]
    targets = (
        endpoint_zero @ shift @ endpoint_zero.conj().T,
        endpoint_one @ shift @ endpoint_one.conj().T,
    )
    dilation_dimension = 2 * output_dimension
    if program_dimension < 1 + dilation_dimension:
        raise ValueError("program Hilbert space is too small for the leaky control")

    anchor = np.zeros(program_dimension, dtype=complex)
    anchor[0] = 1.0
    domain_candidates = np.eye(program_dimension, dtype=complex)[:, 1:]
    domain_embedding = domain_candidates[:, :dilation_dimension]

    pair_prefix = np.column_stack((program_zero, program_one))
    pair_gram = pair_prefix.conj().T @ pair_prefix
    pair_root_inverse = _psd_power(pair_gram, -0.5, tolerance=tolerance)
    pair_basis = pair_prefix @ pair_root_inverse
    full_pair_basis = _complete_isometry(pair_basis, tolerance=tolerance)
    range_embedding = full_pair_basis[:, 2 : 2 + dilation_dimension]

    oracles: list[np.ndarray] = []
    state_residual = 0.0
    unitarity_residual = 0.0
    block_residual = 0.0
    for state, target in zip((program_zero, program_one), targets):
        oracle, dilation = _leaky_preparation_extension(
            state,
            target,
            domain_embedding,
            range_embedding,
            tolerance=tolerance,
        )
        oracles.append(oracle)
        state_residual = max(
            state_residual,
            float(np.linalg.norm(oracle @ anchor - state)),
        )
        unitarity_residual = max(
            unitarity_residual,
            float(
                np.linalg.norm(
                    oracle.conj().T @ oracle
                    - np.eye(program_dimension, dtype=complex),
                    ord=2,
                )
            ),
            float(
                np.linalg.norm(
                    dilation.conj().T @ dilation
                    - np.eye(dilation_dimension, dtype=complex),
                    ord=2,
                )
            ),
        )
        observed = (
            range_embedding[:, :output_dimension].conj().T
            @ oracle
            @ domain_embedding[:, :output_dimension]
        )
        block_residual = max(
            block_residual,
            float(np.linalg.norm(observed - target, ord=2)),
        )

    close_extension = _unitary_mapping_anchor_to_state(program_zero)
    same_state_extension_distance = float(
        np.linalg.norm(oracles[0] - close_extension, ord=2)
    )
    verified = bool(
        state_residual <= 100 * tolerance
        and unitarity_residual <= 1000 * tolerance
        and block_residual <= 1000 * tolerance
        and same_state_extension_distance > 100 * tolerance
    )
    return PreparationExtensionGaugeControl(
        logical_dimension=dimension,
        program_hilbert_dimension=program_dimension,
        target_hilbert_dimension=output_dimension,
        dilation_hilbert_dimension=dilation_dimension,
        preparation_state_residual=state_residual,
        preparation_unitarity_residual=unitarity_residual,
        leaked_block_encoding_residual=block_residual,
        leaked_block_normalization=1.0,
        leaked_block_query_count=1,
        same_prepared_state_extension_distance=same_state_extension_distance,
        bare_first_column_promise_defines_extension_independent_query_complexity=False,
        one_query_leaky_extension_verified=verified,
        status=(
            "one-query-leaky-preparation-extension-gauge"
            if verified
            else "preparation-extension-gauge-control-failure"
        ),
    )


def natural_state_preparation_oracle_scaling_record(
    n: int,
    *,
    block_normalization: float = DEFAULT_BLOCK_NORMALIZATION,
    relative_separation_error: float = DEFAULT_RELATIVE_SEPARATION_ERROR,
) -> NaturalStatePreparationOracleScalingRecord:
    """Transfer the ``sqrt(D)`` oracle bound to the natural high-row scale."""

    if n < 4:
        raise ValueError("n must be at least four")
    if not math.isfinite(block_normalization) or block_normalization < 1.0:
        raise ValueError("block_normalization must be at least one")
    if not 0 <= relative_separation_error < 1:
        raise ValueError("relative_separation_error must lie in [0,1)")
    partitions = partition_number(n)
    dimension = math.isqrt(math.factorial(n)) // partitions + 1
    reflection_lower = (
        (1.0 - relative_separation_error)
        * math.sqrt(dimension)
        / (2.0 * block_normalization)
    )
    preparation_lower = 2.0 * reflection_lower
    log_dimension = math.log2(dimension)
    return NaturalStatePreparationOracleScalingRecord(
        n=n,
        partition_count_decimal=str(partitions),
        natural_high_row_irrep_dimension_lower_bound_decimal=str(dimension),
        natural_high_row_irrep_dimension_lower_bound_log2=log_dimension,
        reflection_query_lower_bound=reflection_lower,
        robust_preparation_query_lower_bound=preparation_lower,
        reflection_query_lower_bound_log2_leading_term=0.5 * log_dimension,
        robust_preparation_query_lower_bound_log2_leading_term=0.5 * log_dimension,
        independent_source_high_row_mass_lower_bound=max(0.0, 1.0 - 1.0 / partitions),
        retained_logical_dimension_same_factorial_exponent_proved=True,
        uniform_reflection_compiler_worst_case_superpolynomial_at_natural_dimension_scale=True,
        uniform_robust_preparation_compiler_worst_case_superpolynomial_at_natural_dimension_scale=True,
        particular_structured_preparation_circuit_lower_bound_proved=False,
        status="natural-dimension-scale-worst-case-oracle-query-superpolynomial",
    )


def run_final_root_state_preparation_oracle_query_boundary(
) -> StatePreparationOracleQueryReport:
    hard_pairs = [
        audit_canonical_endpoint_oracle_hard_pair(dimension)
        for dimension in (2, 3, 4, 5, 8)
    ]
    gauge_controls = [
        audit_preparation_extension_gauge(dimension)
        for dimension in (3, 4, 5)
    ]
    scaling = [
        natural_state_preparation_oracle_scaling_record(n)
        for n in (8, 12, 16, 24, 32, 48)
    ]
    hard_pair_failures = sum(
        not row.exact_canonical_hard_pair_verified for row in hard_pairs
    )
    gauge_failures = sum(
        not row.one_query_leaky_extension_verified for row in gauge_controls
    )
    verified = bool(hard_pair_failures == 0 and gauge_failures == 0)
    theorem = StatePreparationOracleQueryTheorem(
        canonical_hard_pair=(
            "For C_0=I/2 and C_1 differing in one fixed diagonal entry, ||v_0-v_1||=beta/sqrt(D) while ||V_0XV_0^*-V_1XV_1^*||=beta for a D-independent beta>0."
        ),
        reflection_hybrid_bound=(
            "A T-query alpha-normalized reflection-oracle block encoder with relative separation error eta obeys T>=(1-eta)sqrt(D)/(2alpha)."
        ),
        close_preparation_extensions=(
            "There exist valid unitary extensions A_i|0>=|v_i> with ||A_0-A_1||=beta/sqrt(D); controlled queries and adjoints have the same distance."
        ),
        robust_preparation_hybrid_bound=(
            "Any compiler correct for every preparation-unitary extension obeys T>=(1-eta)sqrt(D)/alpha on the close-extension pair."
        ),
        extension_gauge=(
            "Other valid extensions can place a Julia unitary dilation of VXV^* in known orthogonal columns, giving a normalization-one block in one query; the first-column promise alone therefore has no extension-independent query complexity."
        ),
        natural_consequence=(
            "Because retained logical dimensions have the same factorial exponent as d_nu>sqrt(n!)/p(n), a compiler uniform over all canonical endpoints has superpolynomial worst-case query cost at those dimensions; no typical-C or average-natural-mass lower bound follows."
        ),
        surviving_route=(
            "Specify the complete typed Schur/QFT/GPE preparation circuit and exploit its non-program columns, or formulate a restricted extension promise and analyze it directly."
        ),
        scope=(
            "This is a black-box reflection lower bound and a worst-extension preparation lower bound plus an extension-gauge counterexample, not a lower bound for a particular structured preparation circuit or arbitrary quantum circuits."
        ),
        theorem_verified=verified,
        status=(
            "reflection-and-robust-preparation-sqrt-d-no-go-extension-promise-boundary"
            if verified
            else "state-preparation-oracle-query-control-failure"
        ),
    )
    return StatePreparationOracleQueryReport(
        created_at=utc_now(),
        theorem_contract={
            "hypothesis": (
                "Controlled coherent access to a unitary A_V satisfying A_V|0>=|V>>/sqrt(D), or merely to the corresponding program reflection, permits constant-normalization synthesis of VXV^* with subpolynomially many queries."
            ),
            "reflection_access_model": (
                "Controlled calls to R_V=I-2|V>><<V|/D and its identical adjoint, interleaved with arbitrary V-independent unitaries, with an alpha-normalized output block encoding."
            ),
            "preparation_access_model": (
                "Controlled calls to A_V and A_V^*, where only A_V|0>=|V>>/sqrt(D) is promised. Worst-extension correctness and friendly specified extensions are analyzed separately."
            ),
            "positive_identity": (
                "A friendly unitary extension can expose a normalization-one VXV^* block in one query through otherwise unconstrained columns."
            ),
            "negative_boundary": (
                "Reflection access requires Omega(sqrt(D)/alpha) queries, and preparation access required to work for every valid extension satisfies the same stronger square-root barrier."
            ),
            "claim_boundary": (
                "The theorem does not constrain a particular fully specified representation-theoretic preparation circuit unless its full oracle family contains the exhibited close extensions or is reducible to reflection-only access."
            ),
        },
        theorem=theorem,
        hard_pair_controls=hard_pairs,
        extension_gauge_controls=gauge_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "construct_hard_pair_inside_canonical_final_root_family",
                "resolved": True,
                "evidence": "Changing one diagonal entry of C changes one endpoint column by beta, hence the normalized Choi state by beta/sqrt(D), while the two shift-byproduct edge terms retain operator separation beta.",
            },
            {
                "obligation": "prove_reflection_oracle_query_lower_bound",
                "resolved": True,
                "evidence": "Rank-one reflection distance is at most 2beta/sqrt(D); telescoping T oracle substitutions and the required output-block separation give T>=(1-eta)sqrt(D)/(2alpha).",
            },
            {
                "obligation": "decide_first_column_preparation_oracle_promise",
                "resolved": True,
                "evidence": "Minimal rotations give close valid extensions and an Omega(sqrt(D)/alpha) worst-extension lower bound, while orthogonal columns can encode a Julia dilation of the target and solve the task in one query.",
            },
            {
                "obligation": "analyze_actual_structured_schur_qft_gpe_preparation_extension",
                "resolved": False,
                "evidence": "The repository has not yet specified the complete unitary action and inverse of the physical endpoint preparation outside its prepared first column.",
            },
            {
                "obligation": "compile_physical_endpoint_byproduct_block_encoding",
                "resolved": False,
                "evidence": "The one-query leaky extension is an access-model witness, not a construction from the known physical transforms.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The previous 1/D contraction coefficient alone proves an Omega(D) coherent-oracle lower bound.",
                "resolved": True,
                "resolution": "False. The new proof is an independent hard-pair hybrid argument and certifies Omega(sqrt(D)); it does not promote the direct-contraction Bernstein bound to arbitrary coherent queries.",
            },
            {
                "objection": "The hard pair leaves the canonical final-root family by applying an arbitrary logical gauge.",
                "resolved": True,
                "resolution": "False. Both endpoints are exactly [sqrt(C_i);sqrt(I-C_i)] for diagonal effects C_i; only one effect eigenvalue changes.",
            },
            {
                "objection": "Controlled queries or access to A_V^* evade the hybrid distance.",
                "resolved": True,
                "resolution": "Controlled oracle differences and adjoint oracle differences have the same operator norm, so every queried occurrence contributes at most the same hybrid increment.",
            },
            {
                "objection": "A state-preparation unitary is determined by the state it prepares.",
                "resolved": True,
                "resolution": "False. Right multiplication by any unitary fixing |0> changes the other columns without changing A_V|0>; the explicit close and leaky extensions have radically different query behavior.",
            },
            {
                "objection": "The worst-extension lower bound rules out the actual representation-theoretic preparation circuit.",
                "resolved": False,
                "resolution": "It does not. The actual full unitary may have structured non-program columns, just as the leaky witness does; those columns must be specified and audited.",
            },
            {
                "objection": "The natural high-row dimension theorem makes the one-coordinate hard pair typical under the free-Jacobi endpoint law.",
                "resolved": False,
                "resolution": "No. The imported theorem supplies only the dimension scale. The oracle result is a worst-case lower bound for a compiler uniform over all canonical endpoints at that dimension; typical-C query hardness remains open.",
            },
        ],
        primary_literature=[
            {
                "paper_id": BBBV_PAPER_ID,
                "url": BBBV_PAPER_URL,
                "scope": "Hybrid-query method context; the exact hard-pair distances and telescoping bound are derived directly here.",
            },
            {
                "paper_id": NIELSEN_CHUANG_PAPER_ID,
                "url": NIELSEN_CHUANG_PAPER_URL,
                "scope": "Programmable-gate context; cited to delimit a program state from a fully specified unitary oracle, not as the lower-bound engine.",
            },
        ],
        headline_metrics={
            "canonical_endpoint_oracle_hard_pair_theorem_count": int(verified),
            "reflection_oracle_sqrt_dimension_query_no_go_count": int(verified),
            "robust_preparation_oracle_sqrt_dimension_query_no_go_count": int(verified),
            "preparation_extension_gauge_boundary_count": int(verified),
            "one_query_leaky_extension_count": int(verified),
            "hard_pair_control_count": len(hard_pairs),
            "hard_pair_control_failure_count": hard_pair_failures,
            "extension_gauge_control_count": len(gauge_controls),
            "extension_gauge_control_failure_count": gauge_failures,
            "particular_structured_preparation_circuit_lower_bound_count": 0,
            "physical_byproduct_block_encoding_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "canonical_final_root_hard_pair_has_program_distance_beta_over_sqrt_D": verified,
            "fixed_weyl_byproducts_have_constant_operator_separation": verified,
            "constant_normalization_reflection_only_query_complexity_is_omega_sqrt_D": verified,
            "all_extension_robust_preparation_query_complexity_is_omega_sqrt_D": verified,
            "bare_first_column_preparation_promise_defines_query_complexity": False,
            "friendly_preparation_extension_can_leak_target_in_one_query": verified,
            "particular_structured_schur_qft_gpe_preparation_lower_bound_proved": False,
            "typical_natural_endpoint_oracle_query_lower_bound_proved": False,
            "physical_byproduct_block_encoding_compiled": False,
            "arbitrary_coherent_processor_lower_bound_proved": False,
            "physical_pgm_circuit_proved": False,
            "hidden_involution_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Reflection-only and extension-robust compilers uniform over all canonical endpoints have superpolynomial worst-case cost at the retained natural dimension scale. Typical endpoint hardness is not proved, and a fully specified structured preparation unitary may expose useful non-program columns."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved an Omega(sqrt(D)) coherent-query lower bound for reflection-only and all-extension-robust preparation access using a canonical final-root hard pair, then proved that the bare first-column preparation promise is ill-posed by constructing a one-query leaky extension."
        ),
        falsifiers_triggered=[
            "Coherent reflection access does not turn the endpoint Choi program into a constant-normalization byproduct block encoding with sub-square-root queries.",
            "The direct-contraction 1/D signal does not justify an Omega(D) arbitrary-query claim; the independently proved black-box lower bound is Omega(sqrt(D)).",
            "Granting A_V and A_V^* with only A_V|0>=|v_V> promised does not define a unique query model because unconstrained columns can hide the target.",
            "A compiler robust to every valid preparation-unitary extension still requires Omega(sqrt(D)) queries.",
            "The one-query leaky extension is not evidence that the physical Schur/QFT/GPE preparation circuit exposes the same block.",
        ],
    )


def write_final_root_state_preparation_oracle_query_boundary_report(
    path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = asdict(run_final_root_state_preparation_oracle_query_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if write_registry:
        upsert_experiment(
            ExperimentRecord(
                id=DEFAULT_EXPERIMENT_ID,
                candidate_id=DEFAULT_CANDIDATE_ID,
                title="Final-root state-preparation oracle query boundary",
                status="completed-oracle-query-boundary-theorem",
                hypothesis=payload["theorem_contract"]["hypothesis"],
                protocol=(
                    "Construct a one-column canonical endpoint hard pair, compute exact program/reflection/target distances, apply the hybrid query bound to reflection and close preparation extensions, and construct a one-query leaky preparation extension by unitary dilation."
                ),
                positive_signal=(
                    "A complete typed description of the actual physical Schur/QFT/GPE endpoint-preparation unitary whose non-program columns yield a polynomial constant-normalization block encoding of the endpoint Weyl pair."
                ),
                falsifiers=payload["falsifiers_triggered"],
                metrics=list(payload["headline_metrics"].keys()),
                dependencies=[
                    "self_dual_wreath_final_root_program_contraction_normalization_no_go.py",
                    "self_dual_wreath_final_root_byproduct_covariance_no_go.py",
                    "self_dual_wreath_final_root_purification_naimark_program_boundary.py",
                    "self_dual_wreath_joint_character_natural_sector_mass.py",
                ],
                next_actions=[
                    "Write the exact full-domain circuit contract for the physical endpoint program preparation and its inverse, then test whether its non-first columns are branch preserving, merely gauge workspace, or contain a constant-normalization block of V_C X V_C^* and V_C Z V_C^*."
                ],
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id=NEGATIVE_RESULT_ID,
                source=str(path),
                claim=(
                    "Reflection about the normalized endpoint program, or a preparation unitary specified only by its prepared first column, generically supplies a sub-square-root-query constant-normalization block encoding of V_C X V_C^*."
                ),
                reason_invalid=(
                    "A canonical pair with one changed effect eigenvalue has program and close-oracle distance beta/sqrt(D) but target byproduct distance beta. Hybrid telescoping forces Omega(sqrt(D)/alpha) queries for reflections and for compilers robust to every preparation extension. Conversely, unconstrained non-first columns can leak a unitary dilation of the target in one query, so the bare preparation promise is not an extension-independent oracle model."
                ),
                lesson=(
                    "State the complete unitary extension promise. Reflection-only and worst-extension preparation compilers have superpolynomial worst-case cost at natural high-row dimensions, but no typical-endpoint mass bound is proved. A structured physical circuit can survive through explicitly audited action outside its prepared first column."
                ),
                applies_to=[
                    DEFAULT_CANDIDATE_ID,
                    "PO-MECHANISM",
                    "PO-MEASUREMENT",
                    "PO-COMPLEXITY",
                ],
                evidence={
                    "reflection_query_lower_bound": "(1-eta)sqrt(D)/(2alpha)",
                    "robust_preparation_query_lower_bound": "(1-eta)sqrt(D)/alpha",
                    "hard_pair_program_distance": "beta/sqrt(D)",
                    "hard_pair_target_distance": "beta",
                    "friendly_extension_query_count": 1,
                    "bare_first_column_promise_well_posed": False,
                    "particular_structured_preparation_lower_bound_proved": False,
                    "speedup_claim_allowed": False,
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_final_root_state_preparation_oracle_query_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
