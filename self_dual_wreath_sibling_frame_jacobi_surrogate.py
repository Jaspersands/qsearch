"""Exact Gaussian/Jacobi benchmark for hierarchical sibling-frame balance.

This module does not model the natural wreath-product frames as Gaussian.  It
builds the correct random-matrix benchmark that a future universality theorem
would have to transfer.

Let ``X,Y`` be independent ``D x m`` Gaussian matrices, put

    A = X X*,  B = Y Y*,  C = (A+B)^(-1/2) A (A+B)^(-1/2),

and write ``alpha=m/D>1/2``.  When ``alpha<1``, ``C`` has ``D-m`` exact zeros,
``D-m`` exact ones, and ``2m-D`` fractional eigenvalues.  The fractional law
is not obtained by naively inserting ``alpha`` into the full-rank MANOVA
formula.  If ``Z=[X Y]``, the row-space projector

    P = Z* (Z Z*)^(-1) Z

is a Haar rank-``D`` projector in dimension ``2m`` and the positive spectrum
of ``C`` is the spectrum of its first ``m x m`` principal block.  Passing to
the rank ``r=2m-D`` orthogonal complement reduces the fractional sector to a
Jacobi ensemble with effective parameter

    t = m/r = alpha/(2 alpha-1) > 1.

For ``alpha>1`` the direct MANOVA parameter is instead ``t=alpha``.  Applying
the Wachter support formula in both regimes and simplifying gives the same
fractional support

    lambda_+- = (1 +- sqrt(2 alpha-1))^2 / (4 alpha).       (1)

The source formula is Erdos--Farrell, arXiv:1207.0031, equations (1), (3),
and (4).  The row-space/complement reduction above handles the singular
``alpha<1`` regime that their stated ``a,b>1`` model does not directly cover.

Equation (1) exposes a copy-count effect.  At the information threshold
``K=ceil(log2 |G|)``, a sibling has

    alpha_0 = 2^(K-1)/|G| in [1/2,1).

Using either ``K`` or ``K+1`` copies, choose ``K`` when ``alpha_0<=3/4`` and
``K+1`` otherwise.  The selected aspect avoids the hard edge ``alpha=1`` and
has the uniform Gaussian-surrogate endpoint gap

    min(lambda_-,1-lambda_+) >= (3-2 sqrt(2))/6 > 0.0285. (2)

This is a rigorous theorem for the Gaussian surrogate and a precise target
for natural frames.  It is not evidence that the globally-distinct
Plancherel sibling frames obey a Jacobi law.  Marginal Marchenko--Pastur
moments do not imply the joint asymptotic freeness, injective-law transfer, or
spectral-edge rigidity needed for that conclusion.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_sibling_frame_jacobi_surrogate.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JACOBI-SURROGATE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
PRIMARY_SOURCE_URL = "https://arxiv.org/abs/1207.0031"
ADAPTIVE_GAP_FLOOR = (3.0 - 2.0 * math.sqrt(2.0)) / 6.0


@dataclass(frozen=True)
class JacobiAspectRecord:
    aspect_ratio: float
    regime: str
    effective_jacobi_parameter: float
    zero_atom_mass: float
    one_atom_mass: float
    fractional_mass: float
    fractional_support_lower: float
    fractional_support_upper: float
    endpoint_gap: float
    hard_edge: bool
    status: str


@dataclass(frozen=True)
class GaussianProjectionReductionControl:
    ambient_dimension: int
    child_column_count: int
    aspect_ratio: float
    random_seed: int
    expected_zero_multiplicity: int
    observed_zero_multiplicity: int
    expected_one_multiplicity: int
    observed_one_multiplicity: int
    expected_fractional_multiplicity: int
    observed_fractional_multiplicity: int
    row_projection_spectrum_residual: float
    complement_fractional_spectrum_residual: float | None
    predicted_fractional_edge_lower: float
    predicted_fractional_edge_upper: float
    observed_fractional_minimum: float
    observed_fractional_maximum: float
    finite_size_support_excursion: float
    exact_projection_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class AdaptiveCopyRecord:
    n: int
    group_order_decimal: str
    information_threshold_copy_count: int
    threshold_child_aspect_exact: str
    threshold_child_aspect: float
    selected_copy_count: int
    extra_copy_count: int
    selected_child_aspect_exact: str
    selected_child_aspect: float
    selected_endpoint_gap: float
    uniform_surrogate_gap_floor: float
    hard_edge_avoided: bool
    uniform_gap_bound_verified: bool
    natural_frame_jacobi_transfer_proved: bool
    status: str


@dataclass(frozen=True)
class SiblingFrameJacobiSurrogateReport:
    created_at: str
    theorem_contract: dict[str, Any]
    aspect_controls: list[JacobiAspectRecord]
    projection_reduction_controls: list[GaussianProjectionReductionControl]
    adaptive_copy_records: list[AdaptiveCopyRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def jacobi_fractional_edges(alpha: float) -> tuple[float, float]:
    """Return the limiting fractional support in equation (1)."""

    if not math.isfinite(alpha) or alpha <= 0.5:
        raise ValueError("the parent frame must be spanning: alpha > 1/2")
    root = math.sqrt(2.0 * alpha - 1.0)
    lower = (1.0 - root) ** 2 / (4.0 * alpha)
    upper = (1.0 + root) ** 2 / (4.0 * alpha)
    return lower, upper


def effective_jacobi_parameter(alpha: float) -> float:
    """Return the full-rank MANOVA parameter after the complement reduction."""

    if not math.isfinite(alpha) or alpha <= 0.5:
        raise ValueError("alpha must exceed one half")
    if alpha < 1.0:
        return alpha / (2.0 * alpha - 1.0)
    return alpha


def jacobi_aspect_record(alpha: float) -> JacobiAspectRecord:
    lower, upper = jacobi_fractional_edges(alpha)
    if alpha < 1.0:
        atom = 1.0 - alpha
        fractional = 2.0 * alpha - 1.0
        regime = "rank-deficient-complement-jacobi"
    elif alpha > 1.0:
        atom = 0.0
        fractional = 1.0
        regime = "full-rank-direct-jacobi"
    else:
        atom = 0.0
        fractional = 1.0
        regime = "square-hard-edge-boundary"
    hard_edge = math.isclose(alpha, 1.0, rel_tol=0.0, abs_tol=1e-15)
    return JacobiAspectRecord(
        aspect_ratio=alpha,
        regime=regime,
        effective_jacobi_parameter=effective_jacobi_parameter(alpha),
        zero_atom_mass=atom,
        one_atom_mass=atom,
        fractional_mass=fractional,
        fractional_support_lower=lower,
        fractional_support_upper=upper,
        endpoint_gap=min(lower, 1.0 - upper),
        hard_edge=hard_edge,
        status=(
            "gaussian-surrogate-hard-edge"
            if hard_edge
            else "gaussian-surrogate-fractional-gap-positive"
        ),
    )


def _inverse_square_root(matrix: np.ndarray) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2.0)
    if values[0] <= 0:
        raise ArithmeticError("combined Gaussian frame is not positive definite")
    return (vectors * values**-0.5) @ vectors.conj().T


def audit_gaussian_projection_reduction(
    ambient_dimension: int,
    child_column_count: int,
    *,
    seed: int,
    tolerance: float = 1e-8,
) -> GaussianProjectionReductionControl:
    """Verify the finite row-projector and complement reductions exactly."""

    dimension = ambient_dimension
    columns = child_column_count
    if dimension < 2 or columns < 1 or 2 * columns <= dimension:
        raise ValueError("a nontrivial spanning parent requires 2m>D")

    rng = np.random.default_rng(seed)
    combined = (
        rng.normal(size=(dimension, 2 * columns))
        + 1j * rng.normal(size=(dimension, 2 * columns))
    ) / math.sqrt(2.0 * dimension)
    left_columns = combined[:, :columns]
    right_columns = combined[:, columns:]
    left = left_columns @ left_columns.conj().T
    right = right_columns @ right_columns.conj().T
    inverse_root = _inverse_square_root(left + right)
    effect = inverse_root @ left @ inverse_root
    effect_values = np.linalg.eigvalsh((effect + effect.conj().T) / 2.0)

    # The columns of row_basis span the row space of [X Y].  Completing the QR
    # also exposes the rank-(2m-D) orthogonal-complement projector.
    complete_basis, _ = np.linalg.qr(combined.conj().T, mode="complete")
    row_basis = complete_basis[:, :dimension]
    principal_block = row_basis[:columns] @ row_basis[:columns].conj().T
    block_values = np.linalg.eigvalsh(
        (principal_block + principal_block.conj().T) / 2.0
    )
    positive_effect = effect_values[effect_values > tolerance]
    positive_block = block_values[block_values > tolerance]
    row_residual = float(np.max(np.abs(positive_effect - positive_block)))

    fractional = effect_values[
        (effect_values > tolerance) & (effect_values < 1.0 - tolerance)
    ]
    aspect = columns / dimension
    if columns < dimension:
        complement_basis = complete_basis[:, dimension:]
        complement_block = (
            complement_basis[:columns]
            @ complement_basis[:columns].conj().T
        )
        complement_values = np.linalg.eigvalsh(
            (complement_block + complement_block.conj().T) / 2.0
        )
        complement_positive = complement_values[
            complement_values > tolerance
        ]
        complement_prediction = np.sort(1.0 - complement_positive)
        complement_residual: float | None = float(
            np.max(np.abs(fractional - complement_prediction))
        )
    else:
        complement_residual = None

    expected_zero = max(dimension - columns, 0)
    expected_one = max(dimension - columns, 0)
    expected_fractional = (
        2 * columns - dimension if columns < dimension else dimension
    )
    observed_zero = int(np.sum(effect_values <= tolerance))
    observed_one = int(np.sum(effect_values >= 1.0 - tolerance))
    observed_fractional = len(fractional)
    lower, upper = jacobi_fractional_edges(aspect)
    finite_excursion = max(
        lower - float(fractional[0]),
        float(fractional[-1]) - upper,
        0.0,
    )
    verified = bool(
        observed_zero == expected_zero
        and observed_one == expected_one
        and observed_fractional == expected_fractional
        and row_residual <= 100 * tolerance
        and (
            complement_residual is None
            or complement_residual <= 100 * tolerance
        )
    )
    return GaussianProjectionReductionControl(
        ambient_dimension=dimension,
        child_column_count=columns,
        aspect_ratio=aspect,
        random_seed=seed,
        expected_zero_multiplicity=expected_zero,
        observed_zero_multiplicity=observed_zero,
        expected_one_multiplicity=expected_one,
        observed_one_multiplicity=observed_one,
        expected_fractional_multiplicity=expected_fractional,
        observed_fractional_multiplicity=observed_fractional,
        row_projection_spectrum_residual=row_residual,
        complement_fractional_spectrum_residual=complement_residual,
        predicted_fractional_edge_lower=lower,
        predicted_fractional_edge_upper=upper,
        observed_fractional_minimum=float(fractional[0]),
        observed_fractional_maximum=float(fractional[-1]),
        finite_size_support_excursion=finite_excursion,
        exact_projection_reduction_verified=verified,
        status=(
            "finite-gaussian-projection-reduction-verified"
            if verified
            else "finite-gaussian-projection-reduction-failed"
        ),
    )


def adaptive_copy_record(n: int) -> AdaptiveCopyRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    order = math.factorial(n)
    threshold_copies = (order - 1).bit_length()
    threshold_aspect = Fraction(1 << (threshold_copies - 1), order)
    extra = int(threshold_aspect > Fraction(3, 4))
    selected_copies = threshold_copies + extra
    selected_aspect = threshold_aspect * (1 << extra)
    selected_float = float(selected_aspect)
    lower, upper = jacobi_fractional_edges(selected_float)
    gap = min(lower, 1.0 - upper)
    bound_verified = gap + 1e-14 >= ADAPTIVE_GAP_FLOOR
    hard_edge_avoided = bool(
        selected_aspect <= Fraction(3, 4)
        or selected_aspect >= Fraction(3, 2)
    )
    return AdaptiveCopyRecord(
        n=n,
        group_order_decimal=str(order),
        information_threshold_copy_count=threshold_copies,
        threshold_child_aspect_exact=str(threshold_aspect),
        threshold_child_aspect=float(threshold_aspect),
        selected_copy_count=selected_copies,
        extra_copy_count=extra,
        selected_child_aspect_exact=str(selected_aspect),
        selected_child_aspect=selected_float,
        selected_endpoint_gap=gap,
        uniform_surrogate_gap_floor=ADAPTIVE_GAP_FLOOR,
        hard_edge_avoided=hard_edge_avoided,
        uniform_gap_bound_verified=bound_verified,
        natural_frame_jacobi_transfer_proved=False,
        status=(
            "adaptive-gaussian-surrogate-gap-certified-natural-transfer-open"
            if hard_edge_avoided and bound_verified
            else "adaptive-gaussian-surrogate-gap-bound-failed"
        ),
    )


def run_sibling_frame_jacobi_surrogate() -> SiblingFrameJacobiSurrogateReport:
    aspects = [
        jacobi_aspect_record(alpha)
        for alpha in (0.51, 0.625, 0.75, 1.0, 1.5, 2.0)
    ]
    controls = [
        audit_gaussian_projection_reduction(80, 50, seed=11),
        audit_gaussian_projection_reduction(96, 72, seed=17),
        audit_gaussian_projection_reduction(80, 120, seed=23),
    ]
    adaptive = [
        adaptive_copy_record(n)
        for n in (8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48)
    ]
    reduction_failures = sum(
        not row.exact_projection_reduction_verified for row in controls
    )
    schedule_failures = sum(
        not (row.hard_edge_avoided and row.uniform_gap_bound_verified)
        for row in adaptive
    )
    verified = reduction_failures == 0 and schedule_failures == 0
    minimum_observed_gap = min(row.selected_endpoint_gap for row in adaptive)
    metrics: dict[str, int | float] = {
        "exact_gaussian_projection_reduction_theorem_count": 1,
        "gaussian_jacobi_fractional_edge_theorem_count": 1,
        "adaptive_copy_minimax_theorem_count": 1,
        "projection_reduction_control_count": len(controls),
        "projection_reduction_control_failure_count": reduction_failures,
        "adaptive_scaling_row_count": len(adaptive),
        "adaptive_scaling_failure_count": schedule_failures,
        "uniform_gaussian_surrogate_gap_floor": ADAPTIVE_GAP_FLOOR,
        "minimum_scaling_record_surrogate_gap": minimum_observed_gap,
        "maximum_extra_copy_count": max(row.extra_copy_count for row in adaptive),
        "natural_jacobi_universality_theorem_count": 0,
        "globally_distinct_edge_transfer_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return SiblingFrameJacobiSurrogateReport(
        created_at=utc_now(),
        theorem_contract={
            "finite_projection_reduction": (
                "For Gaussian Z=[X Y], whitening identifies C with the left "
                "principal block of the Haar row-space projector."
            ),
            "rank_deficient_complement_reduction": (
                "For 1/2<alpha<1, complementing the rank-D row projector "
                "reduces the 2m-D fractional eigenvalues to a full-rank "
                "Jacobi ensemble with parameter alpha/(2alpha-1)."
            ),
            "fractional_support": (
                "The Wachter/MANOVA edge formula simplifies in both rank "
                "regimes to (1 +- sqrt(2alpha-1))^2/(4alpha)."
            ),
            "adaptive_copy_schedule": (
                "Choosing K at threshold aspect at most 3/4 and K+1 otherwise "
                "gives endpoint gap at least (3-2sqrt(2))/6."
            ),
            "primary_source": PRIMARY_SOURCE_URL,
            "scope": (
                "All spectral-law and uniform-gap statements are Gaussian "
                "surrogate results. No natural Plancherel-frame universality, "
                "coherent transform, or algorithmic speedup is inferred."
            ),
        },
        aspect_controls=aspects,
        projection_reduction_controls=controls,
        adaptive_copy_records=adaptive,
        proof_obligations=[
            {
                "obligation": "derive_correct_rank_deficient_gaussian_jacobi_law",
                "resolved": True,
                "resolution": (
                    "The Haar row-projector complement gives effective aspect "
                    "alpha/(2alpha-1), including the exact 0/1 atom counts."
                ),
            },
            {
                "obligation": "avoid_gaussian_hard_edge_with_constant_copy_overhead",
                "resolved": True,
                "resolution": (
                    "The K-or-K+1 schedule has the exact minimax gap floor "
                    "(3-2sqrt(2))/6."
                ),
            },
            {
                "obligation": "prove_joint_jacobi_universality_for_natural_sibling_frames",
                "resolved": False,
                "resolution": (
                    "Marginal MP moments and E Tr(AB) do not prove joint "
                    "asymptotic freeness or extreme-eigenvalue rigidity."
                ),
            },
            {
                "obligation": "transfer_spectral_edges_under_global_distinctness",
                "resolved": False,
                "resolution": (
                    "The injective Plancherel law must control growing joint "
                    "resolvent or trace-word observables, not only total variation."
                ),
            },
            {
                "obligation": "construct_coherent_hierarchical_common_span_transform",
                "resolved": False,
                "resolution": (
                    "The surrogate theorem supplies no circuit for child-span "
                    "intersection or compressed pseudoinverse access."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Plugging alpha<1 directly into the full-rank MANOVA parameter is valid.",
                "resolved": True,
                "resolution": (
                    "It is invalid; the singular sector has exact 0/1 atoms and "
                    "the fractional complement parameter is alpha/(2alpha-1)."
                ),
            },
            {
                "objection": "The information-threshold aspect can approach the Jacobi hard edge alpha=1.",
                "resolved": True,
                "resolution": (
                    "It can, but selecting between K and K+1 copies keeps the "
                    "Gaussian benchmark uniformly outside (3/4,3/2)."
                ),
            },
            {
                "objection": "Matching four marginal moments proves the natural Jacobi edge.",
                "resolved": False,
                "resolution": (
                    "Fixed moments miss a vanishing extreme sector and do not "
                    "establish the required joint law of A and B."
                ),
            },
            {
                "objection": "A Gaussian surrogate constant gap is already an algorithmic result.",
                "resolved": False,
                "resolution": (
                    "The physical natural-frame universality and coherent "
                    "implementation gates remain entirely open."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "finite_gaussian_projection_reduction_proved": verified,
            "gaussian_fractional_jacobi_support_proved": True,
            "adaptive_at_most_one_extra_copy_surrogate_gap_proved": (
                schedule_failures == 0
            ),
            "rank_deficient_naive_parameterization_rejected": True,
            "natural_sibling_frames_joint_jacobi_law_proved": False,
            "globally_distinct_natural_spectral_edge_proved": False,
            "natural_pseudoinverse_frame_comparability_proved": False,
            "polynomial_hierarchical_polar_sampler_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The Gaussian benchmark has a constant-gap adaptive schedule, "
                "but transferring its joint edge law to globally-distinct "
                "Plancherel projector frames is the unresolved theorem."
            ),
        },
        status=(
            "gaussian-adaptive-gap-proved-natural-jacobi-universality-open"
            if verified
            else "gaussian-jacobi-surrogate-control-failure"
        ),
        summary=(
            "Derived the correct singular/full-rank Gaussian Jacobi benchmark "
            "and proved that an adaptive K-or-K+1 schedule has constant "
            "surrogate endpoint gap; natural-frame universality remains open."
        ),
        falsifiers_triggered=[
            "The rank-deficient fractional law does not use alpha as its direct MANOVA parameter.",
            "The separate-frame condition-number bound is not the exact relative-effect edge.",
            "A fixed number of marginal MP moments cannot certify a Jacobi spectral edge.",
        ],
    )


def write_sibling_frame_jacobi_surrogate_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_sibling_frame_jacobi_surrogate())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


if __name__ == "__main__":
    report = write_sibling_frame_jacobi_surrogate_report()
    print(json.dumps(report, indent=2))
