"""Walsh-sparsity certificates for component diagonal leakage.

Let ``{H_x : x in F_2^m}`` be the canonical leaf POVM on a common component
fiber, let ``q=2^m``, and normalize its Boolean profile by

    F(x) = q H_x,                 E_x F(x) = I.

Write ``F(x)=sum_S A_S chi_S(x)``.  If only ``K`` matrix coefficients are
nonzero, positivity supplies a dimension-free leverage bound that generic
matrix hypercontractivity does not:

    0 <= H_x <= (K/q) I,
    sum_x Tr(H_x^4)/r <= (K/q)^3.                         (1)

For a unit vector ``v``, the scalar polynomial
``g_v(x)=<v,F(x)v>`` is nonnegative, has mean one, and has at most ``K`` Walsh
modes.  The evaluation-kernel bound and Parseval give

    max_x g_v(x)^2 <= K E_x g_v(x)^2
                     <= K max_x g_v(x) E_x g_v(x),

so ``max_x g_v(x)<=K``.  Scalarizing over ``v`` proves (1).

There is a robust version.  Retain a Walsh set ``A`` containing the constant
mode, let ``G`` be the corresponding truncation, and suppose

    eta = max_x ||F(x)-G(x)||_op.

Then ``G(x)+eta I`` is positive, has mean ``(1+eta)I``, and has at most
``K=|A|`` modes.  Therefore

    H_x <= K(1+eta)/q I,
    sum_x Tr(H_x^4)/r <= min(1,K(1+eta)/q)^3.             (2)

Degree ``d`` is one sufficient route, with
``K<=B(m,d)=sum_{j<=d} binom(m,j)``.  In particular every fixed gap below
half degree gives exponentially small diagonal leakage.  Exact or uniformly
approximable Fourier sparsity would therefore close the diagonal half of the
component-M4 budget.

The premise is not generic.  A projection-valued measurement has all ``q``
Walsh modes and saturates the bound at one.  Current repeated-label finite
wreath controls also have full support and operator-norm-one coefficients.
This module proves a representation-specific target, not natural sparsity,
natural M4, a measurement compiler, or a quantum speedup.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from research_registry import utc_now
from self_dual_wreath_component_povm_regular_master_reduction import (
    canonical_component_effects,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_leaf_fourier_leverage.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-LEAF-FOURIER-LEVERAGE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
UNIFORM_EFFECT_CAP_TARGET = 0.2
STRONG_POINTWISE_DIAGONAL_BUDGET = 1.0 / 8192.0

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class LeafFourierCertificate:
    certificate_id: str
    retained_mode_count: int
    maximum_retained_hamming_degree: int
    omitted_uniform_operator_residual: float
    raw_effect_operator_cap: float
    effect_operator_cap: float
    normalized_diagonal_fourth_moment_bound: float
    closes_uniform_effect_cap_target: bool
    closes_proposed_diagonal_budget: bool
    theorem_bound_verified: bool
    status: str


@dataclass(frozen=True)
class LeafFourierProfileControl:
    control_id: str
    profile_kind: str
    cube_dimension: int
    leaf_count: int
    fiber_dimension: int
    povm_sum_residual: float
    minimum_effect_eigenvalue: float
    walsh_reconstruction_residual: float
    numerical_fourier_support_size: int
    numerical_fourier_degree: int
    matrix_fourier_operator_l1: float
    actual_maximum_effect_eigenvalue: float
    actual_normalized_diagonal_fourth_moment: float
    exact_support_certificate: LeafFourierCertificate
    best_degree_certificate: LeafFourierCertificate
    best_sparse_certificate: LeafFourierCertificate
    direct_fourier_l1_effect_cap: float
    direct_fourier_l1_diagonal_bound: float
    all_certificates_verified: bool
    finite_control_closes_diagonal_budget: bool
    status: str


@dataclass(frozen=True)
class FourierDegreeScalingRecord:
    cube_dimension: int
    quarter_degree: int
    quarter_degree_mode_bound: int
    quarter_degree_mode_fraction: float
    quarter_degree_diagonal_bound: float
    maximum_degree_closing_uniform_cap: int
    maximum_uniform_cap_degree_fraction: float
    maximum_degree_closing_budget: int
    maximum_closing_degree_fraction: float
    fixed_gap_below_half_degree_is_asymptotically_sufficient: bool
    status: str


@dataclass(frozen=True)
class LeafFourierLeverageTheorem:
    normalized_profile: str
    exact_sparse_cap: str
    approximate_sparse_cap: str
    degree_corollary: str
    asymptotic_corollary: str
    direct_l1_cap: str
    matrix_hypercontractive_shortcut: str
    arbitrary_positive_povm: bool
    exact_or_uniform_approximation_required: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentLeafFourierLeverageReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: LeafFourierLeverageTheorem
    analytic_controls: list[LeafFourierProfileControl]
    natural_finite_controls: list[LeafFourierProfileControl]
    scaling_records: list[FourierDegreeScalingRecord]
    literature_audit: list[dict[str, str | bool]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _power_of_two_log(value: int) -> int:
    if value < 2 or value & (value - 1):
        raise ValueError("the number of effects must be a power of two")
    return value.bit_length() - 1


def _operator_norm(matrix: np.ndarray) -> float:
    return float(np.linalg.norm(matrix, ord=2))


def _effect_fourth_trace(effect: np.ndarray) -> float:
    square = effect @ effect
    return float(np.trace(square @ square).real)


def _validate_povm(
    effects: tuple[np.ndarray, ...],
    *,
    tolerance: float,
) -> tuple[int, int, float, float]:
    if not effects:
        raise ValueError("at least two POVM effects are required")
    q = len(effects)
    m = _power_of_two_log(q)
    if any(
        effect.ndim != 2
        or effect.shape[0] != effect.shape[1]
        or effect.shape != effects[0].shape
        for effect in effects
    ):
        raise ValueError("effects must be nonempty square matrices of one size")
    r = effects[0].shape[0]
    if r < 1:
        raise ValueError("the POVM fiber must be nonzero")
    minimum = min(
        float(np.linalg.eigvalsh((effect + effect.conj().T) / 2.0)[0])
        for effect in effects
    )
    if minimum < -1000 * tolerance:
        raise ValueError("all effects must be positive semidefinite")
    total = sum(effects, start=np.zeros_like(effects[0]))
    residual = _operator_norm(total - np.eye(r, dtype=complex))
    if residual > 1000 * tolerance:
        raise ValueError("effects must sum to the identity")
    return m, r, residual, minimum


def walsh_fourier_coefficients(
    effects: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, ...]:
    """Return coefficients of ``F(x)=q H_x`` under normalized Walsh transform."""

    m, _, _, _ = _validate_povm(effects, tolerance=tolerance)
    q = 1 << m
    zero = np.zeros_like(effects[0])
    return tuple(
        sum(
            (
                (1.0 if (mask & point).bit_count() % 2 == 0 else -1.0)
                * effects[point]
                for point in range(q)
            ),
            start=zero.copy(),
        )
        for mask in range(q)
    )


def _walsh_values(
    coefficients: tuple[np.ndarray, ...],
    selected_masks: Iterable[int],
) -> tuple[np.ndarray, ...]:
    q = len(coefficients)
    selected = tuple(selected_masks)
    return tuple(
        sum(
            (
                (1.0 if (mask & point).bit_count() % 2 == 0 else -1.0)
                * coefficients[mask]
                for mask in selected
            ),
            start=np.zeros_like(coefficients[0]),
        )
        for point in range(q)
    )


def sparse_fourier_certificate(
    effects: tuple[np.ndarray, ...],
    selected_masks: Iterable[int],
    *,
    certificate_id: str,
    tolerance: float = 1e-10,
) -> LeafFourierCertificate:
    """Certify equation (2) for a selected set of Walsh modes."""

    m, r, _, _ = _validate_povm(effects, tolerance=tolerance)
    q = 1 << m
    selected = tuple(sorted(set(selected_masks)))
    if not selected or selected[0] != 0:
        raise ValueError("the selected Walsh set must contain the constant mode")
    if selected[-1] >= q:
        raise ValueError("a selected Walsh mask is outside the cube")
    coefficients = walsh_fourier_coefficients(effects, tolerance=tolerance)
    truncated = _walsh_values(coefficients, selected)
    normalized = tuple(q * effect for effect in effects)
    eta = max(
        _operator_norm(value - approximation)
        for value, approximation in zip(normalized, truncated, strict=True)
    )
    mode_count = len(selected)
    raw_cap = mode_count * (1.0 + eta) / q
    cap = min(1.0, raw_cap)
    diagonal_bound = cap**3
    actual_cap = max(
        float(np.linalg.eigvalsh((effect + effect.conj().T) / 2.0)[-1])
        for effect in effects
    )
    actual_diagonal = sum(_effect_fourth_trace(effect) for effect in effects) / r
    verified = bool(
        actual_cap <= cap + 5000 * tolerance
        and actual_diagonal <= diagonal_bound + 5000 * tolerance
    )
    return LeafFourierCertificate(
        certificate_id=certificate_id,
        retained_mode_count=mode_count,
        maximum_retained_hamming_degree=max(mask.bit_count() for mask in selected),
        omitted_uniform_operator_residual=eta,
        raw_effect_operator_cap=raw_cap,
        effect_operator_cap=cap,
        normalized_diagonal_fourth_moment_bound=diagonal_bound,
        closes_uniform_effect_cap_target=cap <= UNIFORM_EFFECT_CAP_TARGET,
        closes_proposed_diagonal_budget=(
            diagonal_bound <= STRONG_POINTWISE_DIAGONAL_BUDGET
        ),
        theorem_bound_verified=verified,
        status=(
            "sparse-fourier-diagonal-certificate-verified"
            if verified
            else "sparse-fourier-certificate-control-failure"
        ),
    )


def _best_certificate(
    effects: tuple[np.ndarray, ...],
    selections: Iterable[tuple[str, tuple[int, ...]]],
    *,
    tolerance: float,
) -> LeafFourierCertificate:
    certificates = [
        sparse_fourier_certificate(
            effects,
            selected,
            certificate_id=certificate_id,
            tolerance=tolerance,
        )
        for certificate_id, selected in selections
    ]
    return min(
        certificates,
        key=lambda row: (
            row.normalized_diagonal_fourth_moment_bound,
            row.retained_mode_count,
        ),
    )


def audit_leaf_fourier_profile(
    control_id: str,
    profile_kind: str,
    effects: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> LeafFourierProfileControl:
    m, r, sum_residual, minimum = _validate_povm(
        effects,
        tolerance=tolerance,
    )
    q = 1 << m
    coefficients = walsh_fourier_coefficients(effects, tolerance=tolerance)
    reconstructed = _walsh_values(coefficients, range(q))
    normalized = tuple(q * effect for effect in effects)
    reconstruction_residual = max(
        _operator_norm(value - rebuilt)
        for value, rebuilt in zip(normalized, reconstructed, strict=True)
    )
    coefficient_norms = tuple(_operator_norm(value) for value in coefficients)
    support_threshold = 5000 * tolerance
    support = tuple(
        mask for mask, norm in enumerate(coefficient_norms) if norm > support_threshold
    )
    if 0 not in support:
        raise ArithmeticError("the identity Fourier coefficient disappeared")
    exact_support = sparse_fourier_certificate(
        effects,
        support,
        certificate_id="NUMERICAL-EXACT-SUPPORT",
        tolerance=tolerance,
    )
    degree_selections = (
        (
            f"DEGREE-{degree}",
            tuple(mask for mask in range(q) if mask.bit_count() <= degree),
        )
        for degree in range(m + 1)
    )
    best_degree = _best_certificate(
        effects,
        degree_selections,
        tolerance=tolerance,
    )
    nonconstant = sorted(
        range(1, q),
        key=lambda mask: (-coefficient_norms[mask], mask),
    )
    sparse_selections = (
        (
            f"TOP-{count}-MODES",
            tuple(sorted((0, *nonconstant[: count - 1]))),
        )
        for count in range(1, q + 1)
    )
    best_sparse = _best_certificate(
        effects,
        sparse_selections,
        tolerance=tolerance,
    )
    direct_cap = min(1.0, sum(coefficient_norms) / q)
    direct_diagonal = direct_cap**3
    actual_cap = max(
        float(np.linalg.eigvalsh((effect + effect.conj().T) / 2.0)[-1])
        for effect in effects
    )
    actual_diagonal = sum(_effect_fourth_trace(effect) for effect in effects) / r
    verified = bool(
        reconstruction_residual <= 5000 * tolerance
        and exact_support.theorem_bound_verified
        and best_degree.theorem_bound_verified
        and best_sparse.theorem_bound_verified
        and actual_cap <= direct_cap + 5000 * tolerance
        and actual_diagonal <= direct_diagonal + 5000 * tolerance
    )
    closes = min(
        exact_support.normalized_diagonal_fourth_moment_bound,
        best_degree.normalized_diagonal_fourth_moment_bound,
        best_sparse.normalized_diagonal_fourth_moment_bound,
        direct_diagonal,
    ) <= STRONG_POINTWISE_DIAGONAL_BUDGET
    return LeafFourierProfileControl(
        control_id=control_id,
        profile_kind=profile_kind,
        cube_dimension=m,
        leaf_count=q,
        fiber_dimension=r,
        povm_sum_residual=sum_residual,
        minimum_effect_eigenvalue=minimum,
        walsh_reconstruction_residual=reconstruction_residual,
        numerical_fourier_support_size=len(support),
        numerical_fourier_degree=max(mask.bit_count() for mask in support),
        matrix_fourier_operator_l1=sum(coefficient_norms),
        actual_maximum_effect_eigenvalue=actual_cap,
        actual_normalized_diagonal_fourth_moment=actual_diagonal,
        exact_support_certificate=exact_support,
        best_degree_certificate=best_degree,
        best_sparse_certificate=best_sparse,
        direct_fourier_l1_effect_cap=direct_cap,
        direct_fourier_l1_diagonal_bound=direct_diagonal,
        all_certificates_verified=verified,
        finite_control_closes_diagonal_budget=closes,
        status=(
            "leaf-fourier-certificates-verified"
            if verified
            else "leaf-fourier-certificate-control-failure"
        ),
    )


def _uniform_povm(cube_dimension: int, fiber_dimension: int) -> tuple[np.ndarray, ...]:
    q = 1 << cube_dimension
    effect = np.eye(fiber_dimension, dtype=complex) / q
    return tuple(effect.copy() for _ in range(q))


def _coarse_pvm(
    cube_dimension: int,
    active_bits: int,
) -> tuple[np.ndarray, ...]:
    if not 1 <= active_bits <= cube_dimension:
        raise ValueError("active bits must lie inside the cube")
    q = 1 << cube_dimension
    rank = 1 << active_bits
    repetitions = 1 << (cube_dimension - active_bits)
    effects = []
    for point in range(q):
        effect = np.zeros((rank, rank), dtype=complex)
        effect[point & (rank - 1), point & (rank - 1)] = 1.0 / repetitions
        effects.append(effect)
    return tuple(effects)


def _natural_effects(
    target: Partition,
    labels: tuple[Label, ...],
    *,
    tolerance: float,
) -> tuple[np.ndarray, ...]:
    m = len(labels) - 1
    q = 1 << m
    _, fiber, sides = canonical_component_effects(
        target,
        labels,
        tuple(range(q)),
        tuple(range(q, 2 * q)),
        tolerance=tolerance,
    )
    if not fiber:
        raise ValueError("the selected natural control has zero common span")
    return sides[0]


def fourier_degree_scaling_record(cube_dimension: int) -> FourierDegreeScalingRecord:
    if cube_dimension < 2:
        raise ValueError("at least two Boolean coordinates are required")
    q = 1 << cube_dimension
    quarter = cube_dimension // 4
    modes = sum(math.comb(cube_dimension, degree) for degree in range(quarter + 1))
    maximum_cap = -1
    maximum_budget = -1
    for degree in range(cube_dimension + 1):
        count = sum(math.comb(cube_dimension, level) for level in range(degree + 1))
        ratio = count / q
        if ratio <= UNIFORM_EFFECT_CAP_TARGET:
            maximum_cap = degree
        if ratio**3 <= STRONG_POINTWISE_DIAGONAL_BUDGET:
            maximum_budget = degree
        if (
            ratio > UNIFORM_EFFECT_CAP_TARGET
            and ratio**3 > STRONG_POINTWISE_DIAGONAL_BUDGET
        ):
            break
    return FourierDegreeScalingRecord(
        cube_dimension=cube_dimension,
        quarter_degree=quarter,
        quarter_degree_mode_bound=modes,
        quarter_degree_mode_fraction=modes / q,
        quarter_degree_diagonal_bound=(modes / q) ** 3,
        maximum_degree_closing_uniform_cap=maximum_cap,
        maximum_uniform_cap_degree_fraction=maximum_cap / cube_dimension,
        maximum_degree_closing_budget=maximum_budget,
        maximum_closing_degree_fraction=maximum_budget / cube_dimension,
        fixed_gap_below_half_degree_is_asymptotically_sufficient=True,
        status=(
            "quarter-degree-certificate-closes-budget"
            if (modes / q) ** 3 <= STRONG_POINTWISE_DIAGONAL_BUDGET
            else "finite-cube-too-small-for-quarter-degree-budget"
        ),
    )


def leaf_fourier_leverage_theorem() -> LeafFourierLeverageTheorem:
    return LeafFourierLeverageTheorem(
        normalized_profile="F(x)=qH_x, E_x F(x)=I",
        exact_sparse_cap=(
            "if F has K Walsh modes then H_x<=(K/q)I and "
            "sum_x Tr(H_x^4)/r<=(K/q)^3"
        ),
        approximate_sparse_cap=(
            "for constant-preserving K-mode truncation G with "
            "eta=max_x||F(x)-G(x)||op, H_x<=K(1+eta)I/q"
        ),
        degree_corollary=(
            "degree d permits K=sum_(j<=d) binom(m,j); the same cap applies"
        ),
        asymptotic_corollary=(
            "d<=(1/2-delta)m for fixed delta>0 makes diagonal leakage "
            "exponentially small by a binomial-tail bound"
        ),
        direct_l1_cap=(
            "H_x<=(sum_S ||A_S||op/q)I by Walsh inversion"
        ),
        matrix_hypercontractive_shortcut=(
            "rejected: Ben-Aroya-Regev-de Wolf controls weighted Schatten-p "
            "Fourier norms for p<=2, not a dimension-free matrix L2-to-L4 norm"
        ),
        arbitrary_positive_povm=True,
        exact_or_uniform_approximation_required=True,
        theorem_verified=True,
        status="leaf-fourier-sparsity-suffices-for-diagonal-leverage-control",
    )


def run_component_leaf_fourier_leverage(
    *,
    tolerance: float = 1e-9,
) -> ComponentLeafFourierLeverageReport:
    analytic = [
        audit_leaf_fourier_profile(
            "UNIFORM-Q32-R3",
            "uniform-scalar-povm",
            _uniform_povm(5, 3),
            tolerance=tolerance,
        ),
        audit_leaf_fourier_profile(
            "TWO-BIT-PVM-SPREAD-OVER-Q128",
            "four-mode-coarse-pvm",
            _coarse_pvm(7, 2),
            tolerance=tolerance,
        ),
        audit_leaf_fourier_profile(
            "FULL-Q8-PVM",
            "full-support-projection-valued-obstruction",
            _coarse_pvm(3, 3),
            tolerance=tolerance,
        ),
    ]
    standard = (2, 1)
    trivial = (3,)
    sign = (1, 1, 1)
    natural_specs = [
        (
            "S3-REPEATED-STANDARD-TRIVIAL-TARGET",
            trivial,
            ((standard, standard),) * 3,
        ),
        (
            "S3-NONIDENTICAL-STANDARD-TARGET",
            standard,
            (
                (trivial, standard),
                (trivial, standard),
                (standard, sign),
            ),
        ),
    ]
    natural = [
        audit_leaf_fourier_profile(
            control_id,
            "finite-wreath-canonical-component-povm",
            _natural_effects(target, labels, tolerance=tolerance),
            tolerance=tolerance,
        )
        for control_id, target, labels in natural_specs
    ]
    scaling = [fourier_degree_scaling_record(m) for m in (8, 16, 32, 64, 128)]
    theorem = leaf_fourier_leverage_theorem()
    all_controls = analytic + natural
    failures = sum(not row.all_certificates_verified for row in all_controls)
    natural_sparse = any(row.finite_control_closes_diagonal_budget for row in natural)
    analytic_sparse = sum(row.finite_control_closes_diagonal_budget for row in analytic)
    return ComponentLeafFourierLeverageReport(
        created_at=utc_now(),
        theorem_contract={
            "profile": theorem.normalized_profile,
            "exact_sparse_theorem": theorem.exact_sparse_cap,
            "robust_sparse_theorem": theorem.approximate_sparse_cap,
            "degree_corollary": theorem.degree_corollary,
            "direct_coefficient_bound": theorem.direct_l1_cap,
            "decisive_uniform_cap_target": (
                "max_x ||H_x||op<=0.2 gives zeta=0 in the existing "
                "diagonal-leakage bridge and leaves positive conditional M4 "
                "once chi<=10^-4"
            ),
            "strong_pointwise_diagonal_budget": (
                "sum_x Tr(H_x^4)/r<=1/8192 is sufficient but substantially "
                "stronger than the bridge requires"
            ),
            "scope": (
                "A deterministic Fourier-complexity reduction; no natural "
                "Fourier sparsity or M4 theorem is asserted."
            ),
        },
        theorem=theorem,
        analytic_controls=analytic,
        natural_finite_controls=natural,
        scaling_records=scaling,
        literature_audit=[
            {
                "literature_id": "Ben-Aroya-Regev-deWolf-2008-Matrix-Hypercontractivity",
                "url": "https://arxiv.org/abs/0705.3806",
                "used_claim": (
                    "Theorem 1 bounds weighted matrix Fourier coefficients in "
                    "normalized Schatten p norm for 1<=p<=2."
                ),
                "invalid_shortcut_rejected": True,
                "reason": (
                    "It does not state the dimension-free matrix L2-to-L4 "
                    "inequality needed for a 9^d/q leakage bound."
                ),
            }
        ],
        proof_obligations=[
            {
                "obligation": "replace_generic_matrix_hypercontractivity_with_valid_positive_povm_bound",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "Scalar evaluation kernels plus positivity prove exact and "
                    "uniformly approximate Walsh-sparsity leverage bounds."
                ),
            },
            {
                "obligation": "prove_natural_leaf_profile_has_sublinear_walsh_complexity",
                "resolved": False,
                "resolution": (
                    "Bound exact support, degree below half, coefficient operator "
                    "l1, or a uniform sparse-truncation residual under accepted "
                    "independent Plancherel source labels."
                ),
            },
            {
                "obligation": "bound_natural_distinct_crossing_term",
                "resolved": False,
                "resolution": (
                    "The diagonal certificate does not control ordered distinct "
                    "crossing words."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Ordinary matrix hypercontractivity gives 9^d/q immediately.",
                "resolved": True,
                "resolution": (
                    "False. A constant rank-one matrix already violates a "
                    "dimension-free normalized-Schatten L2-to-L4 inequality."
                ),
            },
            {
                "objection": "POVM positivity alone forces sparse leaf effects.",
                "resolved": True,
                "resolution": (
                    "False. The full PVM control has K=q, maximum leverage one, "
                    "and normalized diagonal fourth moment one."
                ),
            },
            {
                "objection": "The finite natural controls support the premise.",
                "resolved": True,
                "resolution": (
                    "They do not: both S3 controls have all four Walsh modes. "
                    "Repeated/small labels are only obstruction controls."
                ),
            },
            {
                "objection": "A Fourier sparsity theorem is already an algorithm.",
                "resolved": True,
                "resolution": (
                    "No. It would settle one annealed diagonal moment only; "
                    "crossing, coherent implementation, and decoding remain."
                ),
            },
        ],
        headline_metrics={
            "leaf_fourier_leverage_theorem_count": int(theorem.theorem_verified),
            "finite_control_count": len(all_controls),
            "finite_control_failure_count": failures,
            "analytic_controls_closing_diagonal_budget": analytic_sparse,
            "natural_finite_controls_closing_diagonal_budget": int(natural_sparse),
            "maximum_natural_finite_fourier_support_fraction": max(
                row.numerical_fourier_support_size / row.leaf_count for row in natural
            ),
            "minimum_natural_finite_actual_diagonal_fourth_moment": min(
                row.actual_normalized_diagonal_fourth_moment for row in natural
            ),
            "uniform_effect_cap_target": UNIFORM_EFFECT_CAP_TARGET,
            "strong_pointwise_diagonal_budget": (
                STRONG_POINTWISE_DIAGONAL_BUDGET
            ),
            "natural_leaf_fourier_sparsity_theorem_count": 0,
            "natural_diagonal_leakage_theorem_count": 0,
            "natural_component_M4_lower_bound_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "positive_povm_sparse_fourier_leverage_theorem_proved": (
                theorem.theorem_verified and failures == 0
            ),
            "sub_half_degree_would_close_diagonal_budget_asymptotically": True,
            "uniform_cap_at_point_two_would_close_diagonal_half_of_M4_bridge": True,
            "natural_leaf_fourier_sparsity_proved": False,
            "natural_diagonal_leakage_controlled": False,
            "natural_distinct_crossing_pressure_controlled": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Fourier sparsity is now a sufficient structural target, but it "
                "is unproved for natural Plancherel component fibers and fails "
                "in current small repeated-label controls."
            ),
        },
        status=(
            "leaf-fourier-leverage-reduction-verified-natural-sparsity-open"
            if failures == 0
            else "leaf-fourier-leverage-control-failure"
        ),
        summary=(
            "Proved exact and robust Walsh-sparsity bounds for component effect "
            "leverage, rejected an invalid matrix-hypercontractive shortcut, "
            "and isolated natural leaf Fourier complexity as a sufficient but "
            "currently open diagonal-M4 target."
        ),
        falsifiers_triggered=[
            "Dimension-free matrix L2-to-L4 hypercontractivity is not supplied by the cited theorem.",
            "A full projection-valued leaf measurement saturates the K=q obstruction.",
            "Both current finite wreath controls have full Walsh support and do not close the budget.",
        ],
    )


def write_component_leaf_fourier_leverage_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-LEAF-FOURIER-LEVERAGE"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_component_leaf_fourier_leverage" in globals():
        report = run_component_leaf_fourier_leverage(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-COMPONENT-LEAF-FOURIER-LEVERAGE",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-LEAF-FOURIER-LEVERAGE.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-LEAF-FOURIER-LEVERAGE.",
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
                    "self_dual_wreath_component_leaf_fourier_leverage": str(path)
                },
            )
        )
    return payload
