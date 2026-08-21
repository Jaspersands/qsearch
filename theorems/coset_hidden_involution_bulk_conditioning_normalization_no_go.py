"""Bulk conditioning is easy; access normalization is the real obstruction.

Let ``S`` be hidden-involution orbit synthesis with one normalized column per
candidate-fiber basis vector.  If ``M`` is the candidate count and ``k`` the
copy count, the uniform source eigenvalue law ``X`` of ``S^*S`` satisfies

    E[X]=1,        Var(X)=eta=(M-1)/2^k.                (1)

The alternative eigenvalue law is exactly the size bias of ``X``:

    Pr_alt[X in A] = E[X 1_(X in A)].                  (2)

For ``0<delta<1``, Chebyshev and Cauchy--Schwarz give

    Pr_alt[|X-1|>=delta]
      <= eta/delta^2 + eta/delta.                       (3)

Thus choosing ``k=ceil(log2((M-1)/eta_target))`` places all but vanishing
alternative mass in ``X in [1-delta,1+delta]``.  The unnormalized synthesis
polar is perfectly well conditioned on this bulk: its singular-value ratio is
at most ``sqrt((1+delta)/(1-delta))``.  No subgroup classification is needed
for this information-theoretic statement.

The incidence access primitive is instead

    D = S/sqrt(M).                                      (4)

Every useful bulk singular value therefore lies at ``Theta(M^-1/2)``.  An odd
QSVT polynomial implementing the polar has ``p(0)=0`` and must reach constant
amplitude by ``Theta(M^-1/2)``.  Bernstein's inequality forces degree
``Omega(sqrt(M))``.  Applying a source or physical unitary, including
canonicalization, a group QFT, or a coherently flaggable outlier trim, preserves
these nonzero singular values.  If the implementation inherits (4), it does
not improve the degree.

This separates two questions that earlier work mixed together:

1. Spectral conditioning on natural alternative mass is already constant.
2. A useful algorithm needs a new block encoding, factorization, fast-forward,
   or direct polar whose normalization is ``O(poly(n))`` rather than
   ``sqrt(M)``.

Subgroup/Foulkes support analysis remains useful only if it yields such an
access primitive or proves one impossible.  Merely identifying and deleting
large eigenvalue sectors cannot resolve the central bottleneck.  No structured
normalization escape, decoder, or speedup is claimed.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_hidden_involution_binary_decision_reduction import (
    involution_class_size,
)
from coset_hidden_involution_incidence_walk_boundary import incidence_matrix
from coset_perfect_matching_spherical_boundary import perfect_matching_count
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_bulk_conditioning_normalization_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-BULK-CONDITIONING-NORMALIZATION-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class BulkConditioningFiniteControl:
    n: int
    transposition_count: int
    copy_count: int
    candidate_count: int
    source_dimension: int
    source_mean_eigenvalue: float
    predicted_source_mean_eigenvalue: float
    source_centered_second_moment: float
    predicted_source_centered_second_moment: float
    size_biased_outside_window_mass: float
    moment_outside_window_upper_bound: float
    retained_bulk_condition_number: float
    normalized_bulk_singular_lower: float
    normalized_bulk_singular_upper: float
    exact_moment_and_size_bias_control_verified: bool
    status: str


@dataclass(frozen=True)
class BulkNormalizationScalingRecord:
    half_degree: int
    degree: int
    candidate_count_decimal: str
    target_source_variance: float
    copy_count: int
    relative_window_delta: float
    retained_alternative_mass_lower_bound: float
    unnormalized_bulk_condition_number_upper_bound: float
    inherited_incidence_bulk_singular_scale_log2: float
    bernstein_qsvt_degree_lower_bound_log2: float
    subgroup_outlier_classification_required_for_bulk_conditioning: bool
    unitary_basis_changes_improve_inherited_normalization: bool
    constant_normalization_row_access_compiled: bool
    status: str


@dataclass(frozen=True)
class BulkConditioningNormalizationTheorem:
    source_moments: str
    size_bias: str
    bulk_mass: str
    bulk_conditioning: str
    inherited_normalization: str
    bernstein_obstruction: str
    architecture_rule: str
    scope_limit: str
    exact_bulk_mass_bound_proved: bool
    constant_unnormalized_bulk_conditioning_proved: bool
    subgroup_classification_needed_for_bulk_conditioning: bool
    inherited_incidence_qsvt_sqrt_M_obstruction_proved: bool
    unitary_trims_change_inherited_singular_scale: bool
    structured_constant_normalization_access_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class BulkConditioningNormalizationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[BulkConditioningFiniteControl]
    scaling_records: list[BulkNormalizationScalingRecord]
    theorem: BulkConditioningNormalizationTheorem
    literature_links: list[dict[str, str]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def bulk_copy_count(candidate_count: int, target_source_variance: float) -> int:
    if candidate_count < 2:
        raise ValueError("candidate_count must be at least two")
    if not 0.0 < target_source_variance < 1.0:
        raise ValueError("target_source_variance must lie in (0,1)")
    return math.ceil(math.log2((candidate_count - 1) / target_source_variance))


def alternative_outside_window_bound(variance: float, delta: float) -> float:
    if variance < 0.0 or not 0.0 < delta < 1.0:
        raise ValueError("variance and delta must be valid")
    return min(1.0, variance * (delta**-2 + delta**-1))


def audit_bulk_conditioning(
    n: int,
    transposition_count: int,
    copy_count: int,
    *,
    delta: float = 0.5,
    tolerance: float = 1e-8,
) -> BulkConditioningFiniteControl:
    incidence, _ = incidence_matrix(n, transposition_count, copy_count)
    candidates = involution_class_size(n, transposition_count)
    synthesis = incidence / math.sqrt(2**copy_count)
    gram = synthesis.T @ synthesis
    eigenvalues = np.linalg.eigvalsh((gram + gram.T) / 2.0)
    mean = float(np.mean(eigenvalues))
    variance = float(np.mean((eigenvalues - 1.0) ** 2))
    predicted_variance = (candidates - 1) / (2**copy_count)
    outside = np.abs(eigenvalues - 1.0) >= delta - tolerance
    size_biased_outside = float(np.mean(eigenvalues[outside])) if np.any(outside) else 0.0
    # np.mean over the selected subarray has the wrong denominator for a size
    # bias.  Recompute as the uniform-source expectation of X 1_A.
    size_biased_outside = float(np.sum(eigenvalues[outside]) / len(eigenvalues))
    bound = alternative_outside_window_bound(predicted_variance, delta)
    retained = eigenvalues[
        (eigenvalues >= 1.0 - delta - tolerance)
        & (eigenvalues <= 1.0 + delta + tolerance)
        & (eigenvalues > tolerance)
    ]
    condition = math.sqrt(float(np.max(retained) / np.min(retained)))
    normalized_lower = math.sqrt(float(np.min(retained)) / candidates)
    normalized_upper = math.sqrt(float(np.max(retained)) / candidates)
    verified = bool(
        abs(mean - 1.0) <= tolerance
        and abs(variance - predicted_variance) <= 100 * tolerance
        and size_biased_outside <= bound + 100 * tolerance
        and condition <= math.sqrt((1 + delta) / (1 - delta)) + 100 * tolerance
    )
    return BulkConditioningFiniteControl(
        n=n,
        transposition_count=transposition_count,
        copy_count=copy_count,
        candidate_count=candidates,
        source_dimension=gram.shape[0],
        source_mean_eigenvalue=mean,
        predicted_source_mean_eigenvalue=1.0,
        source_centered_second_moment=variance,
        predicted_source_centered_second_moment=predicted_variance,
        size_biased_outside_window_mass=size_biased_outside,
        moment_outside_window_upper_bound=bound,
        retained_bulk_condition_number=condition,
        normalized_bulk_singular_lower=normalized_lower,
        normalized_bulk_singular_upper=normalized_upper,
        exact_moment_and_size_bias_control_verified=verified,
        status=(
            "exact-bulk-conditioning-normalization-control-verified"
            if verified
            else "bulk-conditioning-control-failure"
        ),
    )


def bulk_normalization_scaling_record(
    half_degree: int,
    *,
    target_source_variance: float = 1e-6,
    delta: float = 0.5,
) -> BulkNormalizationScalingRecord:
    if half_degree < 3:
        raise ValueError("half_degree must be at least three")
    candidates = perfect_matching_count(half_degree)
    copies = bulk_copy_count(candidates, target_source_variance)
    actual_variance = (candidates - 1) / (2**copies)
    outside = alternative_outside_window_bound(actual_variance, delta)
    condition = math.sqrt((1.0 + delta) / (1.0 - delta))
    useful_scale_log2 = 0.5 * (
        math.log2(1.0 - delta) - math.log2(candidates)
    )
    # Bernstein gives d >= c/sigma.  Report the asymptotic exponent and omit
    # an inessential constant.
    degree_log2 = -useful_scale_log2
    return BulkNormalizationScalingRecord(
        half_degree=half_degree,
        degree=2 * half_degree,
        candidate_count_decimal=str(candidates),
        target_source_variance=target_source_variance,
        copy_count=copies,
        relative_window_delta=delta,
        retained_alternative_mass_lower_bound=1.0 - outside,
        unnormalized_bulk_condition_number_upper_bound=condition,
        inherited_incidence_bulk_singular_scale_log2=useful_scale_log2,
        bernstein_qsvt_degree_lower_bound_log2=degree_log2,
        subgroup_outlier_classification_required_for_bulk_conditioning=False,
        unitary_basis_changes_improve_inherited_normalization=False,
        constant_normalization_row_access_compiled=False,
        status=(
            "bulk-well-conditioned-incidence-normalization-superpolynomial-"
            "structured-access-open"
        ),
    )


def build_bulk_conditioning_normalization_report(
    *,
    finite_specs: tuple[tuple[int, int, int], ...] = (
        (3, 1, 2),
        (3, 1, 3),
        (4, 2, 2),
    ),
    scaling_half_degrees: tuple[int, ...] = (3, 4, 8, 16, 32, 64, 128),
) -> BulkConditioningNormalizationReport:
    controls = [audit_bulk_conditioning(*spec) for spec in finite_specs]
    scaling = [bulk_normalization_scaling_record(m) for m in scaling_half_degrees]
    verified = all(row.exact_moment_and_size_bias_control_verified for row in controls)
    scaling_verified = all(
        row.retained_alternative_mass_lower_bound > 0.999
        and row.unnormalized_bulk_condition_number_upper_bound < 2.0
        and not row.subgroup_outlier_classification_required_for_bulk_conditioning
        and not row.unitary_basis_changes_improve_inherited_normalization
        and not row.constant_normalization_row_access_compiled
        for row in scaling
    )
    theorem = BulkConditioningNormalizationTheorem(
        source_moments="E[X]=1 and Var(X)=(M-1)/2^k exactly.",
        size_bias="The alternative eigenvalue law is the exact X-size bias.",
        bulk_mass=(
            "Alternative mass outside |X-1|<delta is at most "
            "eta(delta^-2+delta^-1)."
        ),
        bulk_conditioning=(
            "On the retained bulk, cond(S)<=sqrt((1+delta)/(1-delta))."
        ),
        inherited_normalization=(
            "The incidence discriminant is D=S/sqrt(M), so useful bulk "
            "singular values remain Theta(M^-1/2)."
        ),
        bernstein_obstruction=(
            "An odd bounded polar polynomial rising from zero at that scale has "
            "degree Omega(sqrt(M))."
        ),
        architecture_rule=(
            "Do not prioritize more outlier classifications unless they yield a "
            "new normalization, fast-forward, factorization, or direct polar."
        ),
        scope_limit=(
            "Structured group/row transforms may bypass inherited incidence "
            "normalization; no such transform is constructed here."
        ),
        exact_bulk_mass_bound_proved=True,
        constant_unnormalized_bulk_conditioning_proved=True,
        subgroup_classification_needed_for_bulk_conditioning=False,
        inherited_incidence_qsvt_sqrt_M_obstruction_proved=True,
        unitary_trims_change_inherited_singular_scale=False,
        structured_constant_normalization_access_compiled=False,
        theorem_verified=verified and scaling_verified,
        status=(
            "bulk-conditioning-resolved-access-normalization-is-active-obstruction"
            if verified and scaling_verified
            else "bulk-normalization-control-failure"
        ),
    )
    return BulkConditioningNormalizationReport(
        created_at=utc_now(),
        theorem_contract={
            "family": "Any conjugacy class of nonidentity involutions.",
            "source_law": "Uniform normalized candidate-fiber synthesis columns.",
            "alternative_law": "Uniform conjugacy-class mixture of k-copy plus states.",
            "access_model": "Inherited biregular incidence discriminant S/sqrt(M).",
            "outside_scope": (
                "Non-incidence block encodings, group fast-forwarding, direct "
                "row polars, decoding, and natural classical complexity."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        literature_links=[
            {
                "id": "ARXIV-2006.16924",
                "url": "https://arxiv.org/abs/2006.16924",
                "use": (
                    "General Petz/PGM implementation has inverse-small-eigenvalue "
                    "and environment-size costs and a search-based oracle lower "
                    "bound. This corroborates the access diagnosis but is not a "
                    "lower bound for the structured S_n row transform."
                ),
            },
            {
                "id": "ARXIV-QUANT-PH-0604174",
                "url": "https://arxiv.org/abs/quant-ph/0604174",
                "use": (
                    "Establishes logarithmic HSP sample sufficiency via the PGM; "
                    "the unresolved issue here is computational implementation."
                ),
            },
        ],
        proof_obligations=[
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-CONSTANT-NORMALIZATION-ROW-ACCESS",
                "statement": (
                    "Construct a block encoding or direct transform for the bulk "
                    "row synthesis with normalization poly(n), not sqrt(M)."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-ROW-FAST-FORWARD",
                "statement": (
                    "Determine whether the matrix group-convolution row walk can "
                    "be fast-forwarded using S_n representation structure."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-DIRECT-BULK-POLAR",
                "statement": (
                    "Compile the bulk polar without first block-encoding the "
                    "globally normalized incidence discriminant."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Large subgroup outliers are the main natural-mass obstruction.",
                "answer": (
                    "False: exact size-biased moments put arbitrarily high "
                    "alternative mass in a constant relative spectral window."
                ),
                "resolved": True,
            },
            {
                "challenge": "Constant bulk condition number makes QSVT efficient.",
                "answer": (
                    "False: the inherited block encoding scales the entire bulk "
                    "down by sqrt(M), forcing Omega(sqrt(M)) degree."
                ),
                "resolved": True,
            },
            {
                "challenge": "Canonicalization or a QFT changes the singular scale.",
                "answer": (
                    "False by unitary invariance unless those steps also expose a "
                    "different access normalization or non-polynomial direct polar."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_finite_control_count": len(controls),
            "finite_control_failure_count": sum(
                not row.exact_moment_and_size_bias_control_verified for row in controls
            ),
            "constant_bulk_conditioning_theorem_count": 1,
            "subgroup_classification_required_for_bulk_conditioning_count": 0,
            "inherited_sqrt_M_qsvt_obstruction_count": 1,
            "constant_normalization_row_access_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "natural_alternative_bulk_constant_conditioned": verified and scaling_verified,
            "subgroup_outlier_classification_is_active_bottleneck": False,
            "inherited_incidence_qsvt_is_efficient": False,
            "constant_normalization_row_access_compiled": False,
            "direct_bulk_polar_compiled": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The useful bulk is already well conditioned before normalization, "
                "but every inherited incidence access shrinks it by sqrt(M)."
            ),
        },
        status=theorem.status,
        summary=(
            "Separated natural-mass conditioning from access normalization, "
            "proved the former is already constant, and made a new poly(n)-"
            "normalization row access or direct polar the sole active compiler target."
        ),
        falsifiers_triggered=[
            "Further outlier classification is not needed to obtain a well-conditioned natural-mass bulk.",
            "Constant condition number of unnormalized synthesis does not remove sqrt(M) access cost.",
            "Unitary basis changes alone cannot improve inherited singular-value normalization.",
        ],
    )


def write_bulk_conditioning_normalization_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_bulk_conditioning_normalization_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_bulk_conditioning_normalization_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
