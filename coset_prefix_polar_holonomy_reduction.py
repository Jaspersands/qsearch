"""Exact prefix-conditioning chain rule for the coset PGM polar.

Let ``J`` embed one ``G``-intertwiner multiplicity space into the vectorized
physical source and let ``P_1,...,P_k`` be the commuting source-factor
projectors ``(I+rho_lambda_i(h))/2``.  Define

    A_j = P_j ... P_1 J,
    D_j = A_j^* A_j,
    Q_j = A_j D_j^(-1/2).                              (1)

``Q_k`` is the desired restriction polar.  It is tempting to build it by
conditioning one parity at a time.  Assuming the two consecutive prefix
metrics are positive definite, put

    C_j = P_j Q_(j-1) = A_j D_(j-1)^(-1/2),
    E_j = C_j^* C_j
        = D_(j-1)^(-1/2) D_j D_(j-1)^(-1/2),
    V_j = C_j E_j^(-1/2).                              (2)

``V_j`` is the relative polar and has the same output range as ``Q_j``, but
in general it is not ``Q_j``.  The exact chain rule is

    Q_j = V_j U_j,
    U_j = E_j^(-1/2) D_(j-1)^(-1/2) D_j^(1/2).         (3)

``U_j`` is unitary: it is the left polar factor of
``D_(j-1)^(-1/2)D_j^(1/2)``.  It equals the identity exactly when the two
positive prefix metrics commute.  Thus source-factor projectors commuting in
the physical space does *not* remove multiplicity-space holonomy after
compression by ``J``.

This chain rule exposes a potentially important escape from the tiny global
principal angle.  If every relative effect ``E_j`` has inverse-polynomial
positive lower edge, each relative polar can be implemented by polynomial
degree QSVT even when ``D_k`` has exponentially small eigenvalues.  The price
is a coherent implementation of each ``U_j`` and support bookkeeping when a
prefix loses rank.  A direct path/recoupling implementation of these
holonomies could therefore bypass global amplitude amplification.

The exact fixed-point-free ``S_6`` control

    source = (5,1) tensor (5,1) tensor (5,1),
    target = (4,2)

has full-rank three-dimensional prefix metrics.  ``D_1`` is scalar, while
``[D_2,D_3]`` is nonzero.  The last relative effect has eigenvalues
``{11/42,1/3,1}``, but omitting its holonomy changes the polar by about
``0.066`` in operator norm.  This falsifies naive sequential conditioning
while showing that the finite relative gap itself can be benign.

When support is lost, the same formula holds with Moore--Penrose powers.  In
that case ``U_j`` is a partial isometry from ``supp(D_j)`` to
``supp(E_j)``.  The algebraic rank-loss extension is therefore exact; its
uniform coherent compilation is not.  No all-``n`` lower bound on relative
effects, uniform holonomy/support compiler, hidden-involution decoder, or
quantum speedup is claimed.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_hyperoctahedral_branching_polar_boundary import (
    canonical_fixed_point_free_involution,
)
from coset_state_distinguishability import involution_count
from research_registry import utc_now
from self_dual_wreath_orientation_fourier_reduction import (
    _source_representation_rows,
)


REPORT_PATH = Path(
    "research/representation/coset_prefix_polar_holonomy_reduction.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-PREFIX-POLAR-HOLONOMY-REDUCTION"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class PolarChainStepControl:
    step: int
    multiplicity_dimension: int
    previous_metric_minimum_eigenvalue: float
    previous_metric_maximum_eigenvalue: float
    next_metric_minimum_eigenvalue: float
    next_metric_maximum_eigenvalue: float
    prefix_metric_commutator_norm: float
    relative_effect_minimum_eigenvalue: float
    relative_effect_maximum_eigenvalue: float
    relative_effect_condition_number: float
    relative_polar_isometry_residual: float
    global_polar_isometry_residual: float
    holonomy_unitarity_residual: float
    holonomy_formula_residual: float
    holonomy_identity_distance: float
    relative_polar_to_global_polar_distance: float
    prefix_metrics_commute: bool
    holonomy_is_identity: bool
    exact_chain_rule_verified: bool
    status: str


@dataclass(frozen=True)
class FixedPointFreePrefixControl:
    degree: int
    source_partitions: tuple[Partition, ...]
    target_partition: Partition
    multiplicity_dimension: int
    prefix_metric_eigenvalues: tuple[tuple[float, ...], ...]
    final_global_minimum_singular_value: float
    final_global_maximum_singular_value: float
    chain_steps: list[PolarChainStepControl]
    scalar_first_prefix_verified: bool
    noncommuting_later_prefix_pair_found: bool
    naive_sequential_conditioning_falsified: bool
    finite_constant_relative_gap_found: bool
    control_verified: bool
    status: str


@dataclass(frozen=True)
class RankLossPolarChainControl:
    degree: int
    source_partitions: tuple[Partition, ...]
    target_partition: Partition
    multiplicity_dimension: int
    previous_prefix_rank: int
    next_prefix_rank: int
    relative_effect_rank: int
    lost_multiplicity_dimension: int
    next_support_outside_previous_support_residual: float
    positive_relative_effect_eigenvalues: tuple[float, ...]
    relative_polar_partial_isometry_residual: float
    global_polar_partial_isometry_residual: float
    holonomy_initial_support_residual: float
    holonomy_final_support_residual: float
    holonomy_formula_residual: float
    partial_chain_rule_residual: float
    exact_partial_support_chain_rule_verified: bool
    status: str


@dataclass(frozen=True)
class PrefixPolarScalingRecord:
    degree: int
    perfect_matching_hypothesis_count_decimal: str
    information_threshold_copy_count: int
    prefix_depth: int
    required_relative_effect_lower_edge: str
    required_holonomy_gate_cost: str
    required_support_rank_handling: str
    all_prefix_relative_gap_theorem_proved: bool
    uniform_holonomy_compiler_constructed: bool
    rank_loss_compiler_constructed: bool
    global_polar_constructed: bool
    status: str


@dataclass(frozen=True)
class PrefixPolarHolonomyTheorem:
    prefix_analysis: str
    relative_effect: str
    relative_polar: str
    exact_chain_rule: str
    holonomy_identification: str
    commutation_criterion: str
    polynomial_escape_criterion: str
    scope_limit: str
    exact_full_rank_chain_rule_proved: bool
    holonomy_unitarity_proved: bool
    identity_if_and_only_if_commuting_proved: bool
    naive_sequential_conditioning_universally_valid: bool
    finite_fixed_point_free_noncommuting_control_verified: bool
    all_n_relative_gap_proved: bool
    uniform_holonomy_compiler_constructed: bool
    rank_loss_extension_proved: bool
    polynomial_fused_polar_constructed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CosetPrefixPolarHolonomyReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_control: FixedPointFreePrefixControl
    rank_loss_control: RankLossPolarChainControl
    scaling_records: list[PrefixPolarScalingRecord]
    theorem: PrefixPolarHolonomyTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _kron_all(matrices: tuple[np.ndarray, ...]) -> np.ndarray:
    output = matrices[0]
    for matrix in matrices[1:]:
        output = np.kron(output, matrix)
    return output


def _positive_power(
    matrix: np.ndarray,
    exponent: float,
    *,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray]:
    hermitian = (matrix + matrix.conj().T) / 2
    values, vectors = np.linalg.eigh(hermitian)
    if len(values) and values[0] <= tolerance:
        raise ValueError("matrix must be positive definite on the audited domain")
    powered = (vectors * values**exponent) @ vectors.conj().T
    return powered, values


def _supported_power(
    matrix: np.ndarray,
    exponent: float,
    *,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    hermitian = (matrix + matrix.conj().T) / 2
    values, vectors = np.linalg.eigh(hermitian)
    if len(values) and values[0] < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    active = values > tolerance
    support_vectors = vectors[:, active]
    support = support_vectors @ support_vectors.conj().T
    powered = (
        support_vectors * values[active] ** exponent
    ) @ support_vectors.conj().T
    return powered, support, values[active]


def audit_polar_chain_step(
    step: int,
    previous_analysis: np.ndarray,
    next_analysis: np.ndarray,
    *,
    tolerance: float = 1e-9,
) -> PolarChainStepControl:
    """Verify equations (2)-(3) for one full-rank prefix transition."""

    if previous_analysis.shape != next_analysis.shape:
        raise ValueError("consecutive analyses must have the same shape")
    if not previous_analysis.shape[1]:
        raise ValueError("multiplicity domain must be nonempty")
    previous_metric = previous_analysis.conj().T @ previous_analysis
    next_metric = next_analysis.conj().T @ next_analysis
    previous_inverse_root, previous_values = _positive_power(
        previous_metric, -0.5, tolerance=tolerance
    )
    next_inverse_root, next_values = _positive_power(
        next_metric, -0.5, tolerance=tolerance
    )
    next_root, _ = _positive_power(next_metric, 0.5, tolerance=tolerance)

    previous_polar = previous_analysis @ previous_inverse_root
    global_polar = next_analysis @ next_inverse_root
    relative_analysis = next_analysis @ previous_inverse_root
    relative_effect = relative_analysis.conj().T @ relative_analysis
    relative_inverse_root, relative_values = _positive_power(
        relative_effect, -0.5, tolerance=tolerance
    )
    relative_polar = relative_analysis @ relative_inverse_root
    holonomy = relative_polar.conj().T @ global_polar
    holonomy_formula = (
        relative_inverse_root @ previous_inverse_root @ next_root
    )
    identity = np.eye(previous_analysis.shape[1], dtype=np.complex128)

    previous_residual = float(
        np.linalg.norm(
            previous_polar.conj().T @ previous_polar - identity,
            ord=2,
        )
    )
    relative_residual = float(
        np.linalg.norm(
            relative_polar.conj().T @ relative_polar - identity,
            ord=2,
        )
    )
    global_residual = float(
        np.linalg.norm(global_polar.conj().T @ global_polar - identity, ord=2)
    )
    holonomy_unitarity = float(
        np.linalg.norm(holonomy.conj().T @ holonomy - identity, ord=2)
    )
    formula_residual = float(np.linalg.norm(holonomy - holonomy_formula, ord=2))
    chain_residual = float(
        np.linalg.norm(global_polar - relative_polar @ holonomy, ord=2)
    )
    commutator = float(
        np.linalg.norm(
            previous_metric @ next_metric - next_metric @ previous_metric,
            ord=2,
        )
    )
    holonomy_distance = float(np.linalg.norm(holonomy - identity, ord=2))
    relative_distance = float(np.linalg.norm(relative_polar - global_polar, ord=2))
    commute = commutator <= 1e-8
    holonomy_identity = holonomy_distance <= 1e-8
    verified = bool(
        previous_residual <= 1e-8
        and relative_residual <= 1e-8
        and global_residual <= 1e-8
        and holonomy_unitarity <= 1e-8
        and formula_residual <= 1e-8
        and chain_residual <= 1e-8
        and commute == holonomy_identity
    )
    return PolarChainStepControl(
        step=step,
        multiplicity_dimension=previous_analysis.shape[1],
        previous_metric_minimum_eigenvalue=float(previous_values[0]),
        previous_metric_maximum_eigenvalue=float(previous_values[-1]),
        next_metric_minimum_eigenvalue=float(next_values[0]),
        next_metric_maximum_eigenvalue=float(next_values[-1]),
        prefix_metric_commutator_norm=commutator,
        relative_effect_minimum_eigenvalue=float(relative_values[0]),
        relative_effect_maximum_eigenvalue=float(relative_values[-1]),
        relative_effect_condition_number=float(
            relative_values[-1] / relative_values[0]
        ),
        relative_polar_isometry_residual=relative_residual,
        global_polar_isometry_residual=global_residual,
        holonomy_unitarity_residual=holonomy_unitarity,
        holonomy_formula_residual=max(formula_residual, chain_residual),
        holonomy_identity_distance=holonomy_distance,
        relative_polar_to_global_polar_distance=relative_distance,
        prefix_metrics_commute=commute,
        holonomy_is_identity=holonomy_identity,
        exact_chain_rule_verified=verified,
        status=(
            "commuting-prefix-no-holonomy"
            if verified and commute
            else (
                "noncommuting-prefix-unitary-holonomy"
                if verified
                else "prefix-polar-chain-control-failure"
            )
        ),
    )


def audit_partial_polar_chain_step(
    previous_analysis: np.ndarray,
    next_analysis: np.ndarray,
    *,
    tolerance: float = 1e-9,
) -> dict[str, Any]:
    """Verify the Moore--Penrose chain rule across a support loss."""

    if previous_analysis.shape != next_analysis.shape:
        raise ValueError("consecutive analyses must have the same shape")
    previous_metric = previous_analysis.conj().T @ previous_analysis
    next_metric = next_analysis.conj().T @ next_analysis
    previous_inverse_root, previous_support, previous_values = _supported_power(
        previous_metric, -0.5, tolerance=tolerance
    )
    next_inverse_root, next_support, next_values = _supported_power(
        next_metric, -0.5, tolerance=tolerance
    )
    next_root, _, _ = _supported_power(next_metric, 0.5, tolerance=tolerance)
    if not len(next_values):
        raise ValueError("next analysis must have nonempty support")

    global_polar = next_analysis @ next_inverse_root
    relative_analysis = next_analysis @ previous_inverse_root
    relative_effect = relative_analysis.conj().T @ relative_analysis
    relative_inverse_root, relative_support, relative_values = _supported_power(
        relative_effect, -0.5, tolerance=tolerance
    )
    relative_polar = relative_analysis @ relative_inverse_root
    holonomy = relative_polar.conj().T @ global_polar
    holonomy_formula = (
        relative_inverse_root @ previous_inverse_root @ next_root
    )
    return {
        "previous_rank": len(previous_values),
        "next_rank": len(next_values),
        "relative_rank": len(relative_values),
        "next_support_outside_previous_support_residual": float(
            np.linalg.norm(
                (np.eye(previous_support.shape[0]) - previous_support)
                @ next_support,
                ord=2,
            )
        ),
        "positive_relative_effect_eigenvalues": tuple(
            float(value) for value in relative_values
        ),
        "relative_polar_partial_isometry_residual": float(
            np.linalg.norm(
                relative_polar.conj().T @ relative_polar - relative_support,
                ord=2,
            )
        ),
        "global_polar_partial_isometry_residual": float(
            np.linalg.norm(
                global_polar.conj().T @ global_polar - next_support,
                ord=2,
            )
        ),
        "holonomy_initial_support_residual": float(
            np.linalg.norm(holonomy.conj().T @ holonomy - next_support, ord=2)
        ),
        "holonomy_final_support_residual": float(
            np.linalg.norm(holonomy @ holonomy.conj().T - relative_support, ord=2)
        ),
        "holonomy_formula_residual": float(
            np.linalg.norm(holonomy - holonomy_formula, ord=2)
        ),
        "partial_chain_rule_residual": float(
            np.linalg.norm(global_polar - relative_polar @ holonomy, ord=2)
        ),
    }


def fixed_point_free_prefix_control(
    *,
    tolerance: float = 1e-9,
) -> FixedPointFreePrefixControl:
    degree = 6
    source_partitions = ((5, 1), (5, 1), (5, 1))
    target_partition = (4, 2)
    source_tables = tuple(
        _source_representation_rows(partition)
        for partition in source_partitions
    )
    target_table = _source_representation_rows(target_partition)
    group = tuple(target_table)
    source_action = {
        element: _kron_all(tuple(table[element] for table in source_tables))
        for element in group
    }
    source_dimension = source_action[group[0]].shape[0]
    target_dimension = target_table[group[0]].shape[0]
    invariant = sum(
        np.kron(np.conjugate(target_table[element]), source_action[element])
        for element in group
    ) / len(group)
    invariant = (invariant + invariant.conj().T) / 2
    values, vectors = np.linalg.eigh(invariant)
    embedding = vectors[:, values > 1 - 100 * tolerance]

    hidden = canonical_fixed_point_free_involution(degree // 2)
    source_projectors = tuple(
        (np.eye(table[hidden].shape[0]) + table[hidden]) / 2
        for table in source_tables
    )
    analyses = []
    metric_spectra = []
    for prefix in range(1, len(source_projectors) + 1):
        projector = _kron_all(
            tuple(
                source_projectors[index]
                if index < prefix
                else np.eye(source_projectors[index].shape[0])
                for index in range(len(source_projectors))
            )
        )
        analysis = np.kron(np.eye(target_dimension), projector) @ embedding
        analyses.append(analysis)
        metric_spectra.append(
            tuple(
                float(value)
                for value in np.linalg.eigvalsh(
                    analysis.conj().T @ analysis
                )
            )
        )
    steps = [
        audit_polar_chain_step(index + 2, analyses[index], analyses[index + 1])
        for index in range(len(analyses) - 1)
    ]
    first_spectrum = metric_spectra[0]
    scalar_first = max(first_spectrum) - min(first_spectrum) <= 1e-8
    noncommuting = any(not row.prefix_metrics_commute for row in steps)
    falsified = any(
        row.relative_polar_to_global_polar_distance > 1e-6 for row in steps
    )
    constant_gap = min(
        row.relative_effect_minimum_eigenvalue for row in steps
    ) > 0.2
    final_spectrum = metric_spectra[-1]
    verified = bool(
        embedding.shape[1] == 3
        and scalar_first
        and noncommuting
        and falsified
        and constant_gap
        and all(row.exact_chain_rule_verified for row in steps)
    )
    return FixedPointFreePrefixControl(
        degree=degree,
        source_partitions=source_partitions,
        target_partition=target_partition,
        multiplicity_dimension=embedding.shape[1],
        prefix_metric_eigenvalues=tuple(metric_spectra),
        final_global_minimum_singular_value=math.sqrt(min(final_spectrum)),
        final_global_maximum_singular_value=math.sqrt(max(final_spectrum)),
        chain_steps=steps,
        scalar_first_prefix_verified=scalar_first,
        noncommuting_later_prefix_pair_found=noncommuting,
        naive_sequential_conditioning_falsified=falsified,
        finite_constant_relative_gap_found=constant_gap,
        control_verified=verified,
        status=(
            "fixed-point-free-prefix-holonomy-verified"
            if verified
            else "fixed-point-free-prefix-holonomy-control-failure"
        ),
    )


def fixed_point_free_rank_loss_control(
    *,
    tolerance: float = 1e-9,
) -> RankLossPolarChainControl:
    degree = 6
    source_partitions = ((5, 1), (5, 1), (5, 1))
    target_partition = (4, 1, 1)
    source_tables = tuple(
        _source_representation_rows(partition)
        for partition in source_partitions
    )
    target_table = _source_representation_rows(target_partition)
    group = tuple(target_table)
    source_action = {
        element: _kron_all(tuple(table[element] for table in source_tables))
        for element in group
    }
    source_dimension = source_action[group[0]].shape[0]
    target_dimension = target_table[group[0]].shape[0]
    invariant = sum(
        np.kron(np.conjugate(target_table[element]), source_action[element])
        for element in group
    ) / len(group)
    invariant = (invariant + invariant.conj().T) / 2
    values, vectors = np.linalg.eigh(invariant)
    embedding = vectors[:, values > 1 - 100 * tolerance]

    hidden = canonical_fixed_point_free_involution(degree // 2)
    source_projectors = tuple(
        (np.eye(table[hidden].shape[0]) + table[hidden]) / 2
        for table in source_tables
    )
    analyses = []
    for prefix in (2, 3):
        projector = _kron_all(
            tuple(
                source_projectors[index]
                if index < prefix
                else np.eye(source_projectors[index].shape[0])
                for index in range(len(source_projectors))
            )
        )
        analyses.append(
            np.kron(np.eye(target_dimension), projector) @ embedding
        )
    audit = audit_partial_polar_chain_step(
        analyses[0], analyses[1], tolerance=tolerance
    )
    residuals = (
        audit["next_support_outside_previous_support_residual"],
        audit["relative_polar_partial_isometry_residual"],
        audit["global_polar_partial_isometry_residual"],
        audit["holonomy_initial_support_residual"],
        audit["holonomy_final_support_residual"],
        audit["holonomy_formula_residual"],
        audit["partial_chain_rule_residual"],
    )
    verified = bool(
        embedding.shape[1] == 3
        and audit["previous_rank"] == 3
        and audit["next_rank"] == audit["relative_rank"] == 1
        and max(residuals) <= 1e-8
    )
    return RankLossPolarChainControl(
        degree=degree,
        source_partitions=source_partitions,
        target_partition=target_partition,
        multiplicity_dimension=embedding.shape[1],
        previous_prefix_rank=audit["previous_rank"],
        next_prefix_rank=audit["next_rank"],
        relative_effect_rank=audit["relative_rank"],
        lost_multiplicity_dimension=(
            audit["previous_rank"] - audit["next_rank"]
        ),
        next_support_outside_previous_support_residual=audit[
            "next_support_outside_previous_support_residual"
        ],
        positive_relative_effect_eigenvalues=audit[
            "positive_relative_effect_eigenvalues"
        ],
        relative_polar_partial_isometry_residual=audit[
            "relative_polar_partial_isometry_residual"
        ],
        global_polar_partial_isometry_residual=audit[
            "global_polar_partial_isometry_residual"
        ],
        holonomy_initial_support_residual=audit[
            "holonomy_initial_support_residual"
        ],
        holonomy_final_support_residual=audit[
            "holonomy_final_support_residual"
        ],
        holonomy_formula_residual=audit["holonomy_formula_residual"],
        partial_chain_rule_residual=audit["partial_chain_rule_residual"],
        exact_partial_support_chain_rule_verified=verified,
        status=(
            "fixed-point-free-rank-loss-partial-holonomy-verified"
            if verified
            else "rank-loss-partial-holonomy-control-failure"
        ),
    )


def prefix_polar_scaling_record(degree: int) -> PrefixPolarScalingRecord:
    if degree < 4 or degree % 2:
        raise ValueError("degree must be even and at least four")
    hypotheses = involution_count(degree, degree // 2)
    copies = math.ceil(math.log2(hypotheses))
    return PrefixPolarScalingRecord(
        degree=degree,
        perfect_matching_hypothesis_count_decimal=str(hypotheses),
        information_threshold_copy_count=copies,
        prefix_depth=copies,
        required_relative_effect_lower_edge=(
            "lambda_min^+(E_j)>=1/poly(degree,prefix_depth) on retained mass"
        ),
        required_holonomy_gate_cost=(
            "poly(degree,prefix_depth,log(1/error)) uniformly in source labels"
        ),
        required_support_rank_handling=(
            "coherent support update when rank(D_j)<rank(D_(j-1))"
        ),
        all_prefix_relative_gap_theorem_proved=False,
        uniform_holonomy_compiler_constructed=False,
        rank_loss_compiler_constructed=False,
        global_polar_constructed=False,
        status="prefix-chain-criterion-recorded-asymptotic-inputs-open",
    )


def build_coset_prefix_polar_holonomy_report(
    *,
    scaling_degrees: tuple[int, ...] = (8, 16, 32, 64, 128, 256),
) -> CosetPrefixPolarHolonomyReport:
    control = fixed_point_free_prefix_control()
    rank_loss = fixed_point_free_rank_loss_control()
    scaling = [prefix_polar_scaling_record(degree) for degree in scaling_degrees]
    verified = bool(
        control.control_verified
        and rank_loss.exact_partial_support_chain_rule_verified
    )
    theorem = PrefixPolarHolonomyTheorem(
        prefix_analysis=(
            "A_j=P_j...P_1J, D_j=A_j^*A_j, and "
            "Q_j=A_jD_j^(+,-1/2) on its prefix support."
        ),
        relative_effect=(
            "E_j=D_(j-1)^(-1/2)D_jD_(j-1)^(-1/2)."
        ),
        relative_polar=(
            "V_j=A_jD_(j-1)^(-1/2)E_j^(-1/2)."
        ),
        exact_chain_rule=(
            "Q_j=V_jU_j with U_j=E_j^(-1/2)"
            "D_(j-1)^(-1/2)D_j^(1/2)."
        ),
        holonomy_identification=(
            "U_j is the left polar/Uhlmann factor of "
            "D_(j-1)^(+,-1/2)D_j^(1/2): unitary at equal full "
            "rank and a support-carrying partial isometry after rank loss."
        ),
        commutation_criterion=(
            "U_j=I exactly iff positive D_(j-1) and D_j commute."
        ),
        polynomial_escape_criterion=(
            "Inverse-polynomial relative-effect gaps plus polynomial coherent "
            "holonomy and support compilers imply a polynomial prefix polar, "
            "without transforming the exponentially small global singular scale."
        ),
        scope_limit=(
            "The full-rank and Moore--Penrose support chain rules are exact, but "
            "no natural all-n gap or uniform holonomy/support circuit is supplied."
        ),
        exact_full_rank_chain_rule_proved=True,
        holonomy_unitarity_proved=True,
        identity_if_and_only_if_commuting_proved=True,
        naive_sequential_conditioning_universally_valid=False,
        finite_fixed_point_free_noncommuting_control_verified=verified,
        all_n_relative_gap_proved=False,
        uniform_holonomy_compiler_constructed=False,
        rank_loss_extension_proved=True,
        polynomial_fused_polar_constructed=False,
        theorem_verified=verified,
        status=(
            "prefix-polar-chain-rule-proved-holonomy-and-gaps-open"
            if verified
            else "prefix-polar-holonomy-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "exact_prefix_polar_chain_rule_theorem_count": 1,
        "exact_partial_support_chain_rule_theorem_count": 1,
        "finite_fixed_point_free_control_count": 2,
        "finite_validation_failure_count": int(not verified),
        "finite_prefix_step_count": len(control.chain_steps),
        "finite_noncommuting_prefix_step_count": sum(
            not row.prefix_metrics_commute for row in control.chain_steps
        ),
        "finite_constant_relative_gap_step_count": sum(
            row.relative_effect_minimum_eigenvalue > 0.2
            for row in control.chain_steps
        ),
        "maximum_finite_holonomy_identity_distance": max(
            row.holonomy_identity_distance for row in control.chain_steps
        ),
        "all_n_relative_gap_theorem_count": 0,
        "uniform_holonomy_compiler_count": 0,
        "finite_rank_loss_dimension": rank_loss.lost_multiplicity_dimension,
        "rank_loss_chain_rule_count": 1,
        "rank_loss_compiler_count": 0,
        "polynomial_fused_polar_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return CosetPrefixPolarHolonomyReport(
        created_at=utc_now(),
        theorem_contract={
            "domain": (
                "One fixed G-intertwiner multiplicity block and ordered commuting "
                "source-factor involution projectors."
            ),
            "proved_regime": (
                "Positive full-rank prefixes and changing-support prefixes via "
                "Moore--Penrose powers."
            ),
            "constructive_model": (
                "Coherent block access to each relative analysis plus a direct "
                "or block-encoded multiplicity-domain holonomy."
            ),
            "non_claim": (
                "No typical-source relative gap, uniform holonomy/support circuit, "
                "decoder, or end-to-end speedup."
            ),
        },
        finite_control=control,
        rank_loss_control=rank_loss,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-PREFIX-RELATIVE-GAP",
                "statement": (
                    "Prove inverse-polynomial positive lower edges for every "
                    "relative effect E_j on high natural source/PGM mass, or find "
                    "a natural small-gap counterfamily."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-PREFIX-HOLONOMY-COMPILER",
                "statement": (
                    "Compile U_j from wreath subduction/fusion path data with "
                    "polynomial gates, or prove typical U_j is negligible."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-PREFIX-RANK-LOSS",
                "statement": (
                    "Compile the proved partial Uhlmann support transport when a "
                    "prefix metric loses rank, uniformly over source labels."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-PREFIX-UNIFORMITY",
                "statement": (
                    "Give one source-label-uniform SELECT for all k=Theta(n log n) "
                    "relative effects and holonomies with controlled total error."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Physical source-factor projectors commute, so prefix metrics commute.",
                "answer": (
                    "False. Compression by the G-intertwiner embedding does not "
                    "preserve products; the exact S_6 D_2,D_3 commutator is nonzero."
                ),
                "resolved": True,
            },
            {
                "challenge": "Sequential relative polars automatically equal the global polar.",
                "answer": (
                    "False. They differ by the exact Uhlmann holonomy U_j, and "
                    "the S_6 final-step distance is strictly positive."
                ),
                "resolved": True,
            },
            {
                "challenge": "An exponentially small global overlap forces one tiny conditional step.",
                "answer": (
                    "Not proved and false in the finite control: all audited "
                    "relative-effect lower edges exceed 0.2 despite the shrinking prefix metric."
                ),
                "resolved": True,
            },
            {
                "challenge": "Rank loss invalidates the prefix chain algebra.",
                "answer": (
                    "False. Moore--Penrose powers give the same exact formula, "
                    "with U_j a partial isometry from supp(D_j) to supp(E_j)."
                ),
                "resolved": True,
            },
            {
                "challenge": "The finite constant gaps establish a scalable polar algorithm.",
                "answer": (
                    "False. The required natural all-n gap, uniform holonomy/support "
                    "compiler, uniformity, and decoder theorems are all open."
                ),
                "resolved": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "exact_full_rank_prefix_chain_rule_proved": True,
            "exact_partial_support_chain_rule_proved": True,
            "nontrivial_multiplicity_holonomy_exists": True,
            "naive_sequential_parity_conditioning_valid": False,
            "finite_relative_effects_constant_gap": True,
            "all_n_relative_effect_gap_proved": False,
            "uniform_holonomy_compiler_constructed": False,
            "rank_loss_chain_rule_proved": True,
            "rank_loss_compiler_constructed": False,
            "polynomial_fused_polar_constructed": False,
            "polynomial_hidden_involution_decoder_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Prefix conditioning can avoid the global tiny singular scale only "
                "if natural relative gaps and Uhlmann holonomy/support transports "
                "are compiled uniformly; the exact chain algebra is proved."
            ),
        },
        status="prefix-polar-chain-rule-proved-holonomy-and-gaps-open",
        summary=(
            "Derived the exact source-prefix polar chain rule. A fixed-point-free "
            "S_6 control falsifies naive recursion through noncommuting compressed "
            "metrics, but retains constant relative gaps. A second S_6 control "
            "proves the partial-support extension across rank loss; coherent "
            "Uhlmann transport is now the precise constructive correction."
        ),
        falsifiers_triggered=[
            (
                "Commuting physical parity projectors need not yield commuting "
                "multiplicity-prefix metrics."
            ),
            (
                "Relative polar composition without input-side holonomy is not exact."
            ),
            (
                "A small global principal angle does not by itself force a small "
                "finite conditional principal angle."
            ),
            (
                "Prefix rank loss does not break the polar chain rule; it changes "
                "the Uhlmann correction from a unitary to a partial isometry."
            ),
            (
                "A finite constant conditional gap does not imply an all-n algorithm."
            ),
        ],
    )


def write_coset_prefix_polar_holonomy_report(
    output_path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-COSET-PREFIX-POLAR-HOLONOMY-REDUCTION"
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
    payload = asdict(build_coset_prefix_polar_holonomy_report(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_coset_prefix_polar_holonomy_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
