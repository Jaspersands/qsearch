"""Sparse-support boundary for natural component-POVM compilation.

The matrix-POVM recursive normal form isolates effects

    H_e = W^* P_e W,              sum_e H_e = I,          (1)

where ``W:C^r -> C^N`` is a normalized child embedding and ``P_e`` is the
coordinate projector for one orientation-mask block of dimension ``b_e``.
Small trace ``tr(H_e)`` does *not* imply a small positive spectral edge.  It
may instead come from low support rank.

This module makes that distinction exact and supplies the correct Haar/Jacobi
benchmark.  For a Haar isometry and one block with aspect ratios

    alpha = r/N,                  beta = b_e/N,

generic position gives

    mult_0(H_e) = max(r-b_e,0),
    mult_1(H_e) = max(r+b_e-N,0).                         (2)

The fractional spectrum has limiting free-Jacobi support

    lambda_+- = (sqrt((1-alpha) beta)
                  +- sqrt(alpha (1-beta)))^2.             (3)

In the many-outcome sparse-block regime ``beta -> 0`` with fixed
``alpha in (0,1)``, equation (3) gives

    lambda_-,lambda_+ -> alpha,
    lambda_+ - lambda_- = 4 sqrt(alpha(1-alpha)beta(1-beta)).  (4)

Meanwhile the support-rank fraction is ``beta/alpha`` and the expected trace
fraction is ``beta``.  Thus an exponentially rare outcome can have a constant
positive effect edge: asymptotically ``H_e`` is ``alpha`` times a small-rank
support projector, rather than a full-rank exponentially small effect.

This sharply limits the generic square-root-QSVT obstruction.  If natural
Plancherel/Racah child embeddings obey a sparse-block Jacobi edge law, their
hard operation is coherent SELECT of the support projectors, while the
square-root amplitude on support is constant scale.  No such natural
universality theorem is proved here; the Haar model is a falsifiable benchmark,
not evidence that the representation frames are random.

The free-Jacobi edge formula agrees with the Gaussian sibling-frame reduction
recorded from Erdos--Farrell, arXiv:1207.0031.
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
    "self_dual_wreath_component_povm_sparse_support_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-SPARSE-SUPPORT-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
PRIMARY_SOURCE_URL = "https://arxiv.org/abs/1207.0031"


@dataclass(frozen=True)
class HaarComponentEffectRecord:
    block_index: int
    ambient_dimension: int
    fiber_dimension: int
    coefficient_block_dimension: int
    fiber_aspect: float
    block_aspect: float
    expected_zero_multiplicity: int
    observed_zero_multiplicity: int
    expected_one_multiplicity: int
    observed_one_multiplicity: int
    expected_fractional_multiplicity: int
    observed_fractional_multiplicity: int
    trace_fraction: float
    haar_expected_trace_fraction: float
    minimum_positive_eigenvalue: float
    maximum_nonunit_eigenvalue: float
    predicted_fractional_edge_lower: float
    predicted_fractional_edge_upper: float
    nonzero_spectrum_duality_residual: float
    generic_position_atom_multiplicities_verified: bool
    status: str


@dataclass(frozen=True)
class HaarComponentPovmControl:
    control_id: str
    ambient_dimension: int
    fiber_dimension: int
    outcome_count: int
    coefficient_block_dimensions: tuple[int, ...]
    random_seed: int
    component_effects: list[HaarComponentEffectRecord]
    effect_sum_identity_residual: float
    maximum_nonzero_spectrum_duality_residual: float
    maximum_atom_multiplicity_error: int
    maximum_trace_fraction_deviation_from_haar_mean: float
    exact_finite_projection_geometry_verified: bool
    status: str


@dataclass(frozen=True)
class SparseOutcomeJacobiRecord:
    fiber_aspect: float
    outcome_count: int
    block_aspect: float
    zero_atom_fraction_within_fiber: float
    one_atom_fraction_within_fiber: float
    positive_support_rank_fraction_within_fiber: float
    expected_effect_trace_fraction: float
    average_positive_eigenvalue: float
    fractional_edge_lower: float
    fractional_edge_upper: float
    fractional_spectral_width: float
    maximum_edge_deviation_from_fiber_aspect: float
    positive_edge_bounded_away_from_zero: bool
    small_trace_caused_by_low_rank_not_small_positive_edge: bool
    status: str


@dataclass(frozen=True)
class ComponentPovmSparseSupportBoundaryReport:
    created_at: str
    primary_literature: list[dict[str, str]]
    theorem_contract: dict[str, Any]
    finite_controls: list[HaarComponentPovmControl]
    sparse_scaling_records: list[SparseOutcomeJacobiRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def free_jacobi_fractional_edges(
    fiber_aspect: float,
    block_aspect: float,
) -> tuple[float, float]:
    """Return the continuous support for two free projection aspects."""

    alpha = fiber_aspect
    beta = block_aspect
    if not 0 < alpha < 1 or not 0 < beta < 1:
        raise ValueError("fiber and block aspects must lie strictly between zero and one")
    left = math.sqrt((1.0 - alpha) * beta)
    right = math.sqrt(alpha * (1.0 - beta))
    return (left - right) ** 2, (left + right) ** 2


def generic_component_atom_multiplicities(
    ambient_dimension: int,
    fiber_dimension: int,
    block_dimension: int,
) -> tuple[int, int, int]:
    """Return generic zero, one, and fractional multiplicities of ``W*PW``."""

    if not 0 < fiber_dimension < ambient_dimension:
        raise ValueError("fiber dimension must lie between zero and ambient dimension")
    if not 0 < block_dimension < ambient_dimension:
        raise ValueError("block dimension must lie between zero and ambient dimension")
    zero = max(fiber_dimension - block_dimension, 0)
    one = max(fiber_dimension + block_dimension - ambient_dimension, 0)
    fractional = fiber_dimension - zero - one
    return zero, one, fractional


def _haar_isometry(
    ambient_dimension: int,
    fiber_dimension: int,
    *,
    seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    gaussian = (
        rng.normal(size=(ambient_dimension, fiber_dimension))
        + 1j * rng.normal(size=(ambient_dimension, fiber_dimension))
    ) / math.sqrt(2.0)
    isometry, _ = np.linalg.qr(gaussian, mode="reduced")
    return isometry


def audit_haar_component_povm(
    control_id: str,
    ambient_dimension: int,
    fiber_dimension: int,
    block_dimensions: tuple[int, ...],
    *,
    seed: int,
    tolerance: float = 1e-9,
) -> HaarComponentPovmControl:
    if sum(block_dimensions) != ambient_dimension:
        raise ValueError("coefficient blocks must partition the ambient dimension")
    if any(dimension < 1 for dimension in block_dimensions):
        raise ValueError("coefficient blocks must be nonempty")
    isometry = _haar_isometry(
        ambient_dimension,
        fiber_dimension,
        seed=seed,
    )
    identity = np.eye(fiber_dimension, dtype=complex)
    effects = []
    records = []
    offset = 0
    atom_error = 0
    duality_residual = 0.0
    trace_deviation = 0.0
    for block_index, block_dimension in enumerate(block_dimensions):
        block = isometry[offset : offset + block_dimension]
        offset += block_dimension
        effect = block.conj().T @ block
        effects.append(effect)
        values = np.linalg.eigvalsh((effect + effect.conj().T) / 2.0)
        dual_values = np.linalg.eigvalsh(block @ block.conj().T)
        positive = values[values > 100 * tolerance]
        dual_positive = dual_values[dual_values > 100 * tolerance]
        dual_residual = float(
            np.max(np.abs(positive - dual_positive))
        ) if len(positive) else 0.0
        predicted_zero, predicted_one, predicted_fractional = (
            generic_component_atom_multiplicities(
                ambient_dimension,
                fiber_dimension,
                block_dimension,
            )
        )
        observed_zero = int(np.sum(values <= 100 * tolerance))
        observed_one = int(np.sum(values >= 1.0 - 100 * tolerance))
        observed_fractional = fiber_dimension - observed_zero - observed_one
        current_error = max(
            abs(observed_zero - predicted_zero),
            abs(observed_one - predicted_one),
            abs(observed_fractional - predicted_fractional),
        )
        atom_error = max(atom_error, current_error)
        duality_residual = max(duality_residual, dual_residual)
        trace_fraction = float(np.trace(effect).real / fiber_dimension)
        beta = block_dimension / ambient_dimension
        trace_deviation = max(trace_deviation, abs(trace_fraction - beta))
        lower, upper = free_jacobi_fractional_edges(
            fiber_dimension / ambient_dimension,
            beta,
        )
        nonunit = values[values < 1.0 - 100 * tolerance]
        verified = current_error == 0 and dual_residual <= 1000 * tolerance
        records.append(
            HaarComponentEffectRecord(
                block_index=block_index,
                ambient_dimension=ambient_dimension,
                fiber_dimension=fiber_dimension,
                coefficient_block_dimension=block_dimension,
                fiber_aspect=fiber_dimension / ambient_dimension,
                block_aspect=beta,
                expected_zero_multiplicity=predicted_zero,
                observed_zero_multiplicity=observed_zero,
                expected_one_multiplicity=predicted_one,
                observed_one_multiplicity=observed_one,
                expected_fractional_multiplicity=predicted_fractional,
                observed_fractional_multiplicity=observed_fractional,
                trace_fraction=trace_fraction,
                haar_expected_trace_fraction=beta,
                minimum_positive_eigenvalue=float(positive[0]),
                maximum_nonunit_eigenvalue=float(nonunit[-1]),
                predicted_fractional_edge_lower=lower,
                predicted_fractional_edge_upper=upper,
                nonzero_spectrum_duality_residual=dual_residual,
                generic_position_atom_multiplicities_verified=verified,
                status=(
                    "exact-haar-component-projection-geometry"
                    if verified
                    else "haar-component-projection-control-failure"
                ),
            )
        )
    sum_residual = float(
        np.linalg.norm(sum(effects, np.zeros_like(identity)) - identity, ord=2)
    )
    exact = bool(
        atom_error == 0
        and duality_residual <= 1000 * tolerance
        and sum_residual <= 1000 * tolerance
    )
    return HaarComponentPovmControl(
        control_id=control_id,
        ambient_dimension=ambient_dimension,
        fiber_dimension=fiber_dimension,
        outcome_count=len(block_dimensions),
        coefficient_block_dimensions=block_dimensions,
        random_seed=seed,
        component_effects=records,
        effect_sum_identity_residual=sum_residual,
        maximum_nonzero_spectrum_duality_residual=duality_residual,
        maximum_atom_multiplicity_error=atom_error,
        maximum_trace_fraction_deviation_from_haar_mean=trace_deviation,
        exact_finite_projection_geometry_verified=exact,
        status=(
            "exact-haar-component-povm-projection-geometry"
            if exact
            else "haar-component-povm-control-failure"
        ),
    )


def sparse_outcome_jacobi_record(
    fiber_aspect: float,
    outcome_count: int,
) -> SparseOutcomeJacobiRecord:
    if outcome_count < 2:
        raise ValueError("at least two equal coordinate outcomes are required")
    beta = 1.0 / outcome_count
    alpha = fiber_aspect
    lower, upper = free_jacobi_fractional_edges(alpha, beta)
    zero = max(alpha - beta, 0.0) / alpha
    one = max(alpha + beta - 1.0, 0.0) / alpha
    positive_rank = min(alpha, beta) / alpha
    average_positive = beta / positive_rank
    width = upper - lower
    deviation = max(abs(lower - alpha), abs(upper - alpha))
    positive_edge = lower >= alpha / 4.0
    low_rank_explanation = bool(
        beta <= alpha / 16.0
        and positive_rank <= 1.0 / 16.0
        and positive_edge
    )
    return SparseOutcomeJacobiRecord(
        fiber_aspect=alpha,
        outcome_count=outcome_count,
        block_aspect=beta,
        zero_atom_fraction_within_fiber=zero,
        one_atom_fraction_within_fiber=one,
        positive_support_rank_fraction_within_fiber=positive_rank,
        expected_effect_trace_fraction=beta,
        average_positive_eigenvalue=average_positive,
        fractional_edge_lower=lower,
        fractional_edge_upper=upper,
        fractional_spectral_width=width,
        maximum_edge_deviation_from_fiber_aspect=deviation,
        positive_edge_bounded_away_from_zero=positive_edge,
        small_trace_caused_by_low_rank_not_small_positive_edge=low_rank_explanation,
        status=(
            "sparse-outcome-support-scalar-jacobi-regime"
            if low_rank_explanation
            else "preasymptotic-component-jacobi-regime"
        ),
    )


def run_component_povm_sparse_support_boundary(
) -> ComponentPovmSparseSupportBoundaryReport:
    controls = [
        audit_haar_component_povm(
            "MANY-EQUAL-SPARSE-COORDINATE-BLOCKS",
            96,
            56,
            (8,) * 12,
            seed=1701,
        ),
        audit_haar_component_povm(
            "ONE-ATOM-AND-ZERO-ATOM-COMPONENTS",
            96,
            72,
            (32, 32, 32),
            seed=1702,
        ),
        audit_haar_component_povm(
            "MIXED-MACROSCOPIC-COMPONENT-ASPECTS",
            96,
            40,
            (48, 24, 24),
            seed=1703,
        ),
    ]
    scaling = [
        sparse_outcome_jacobi_record(alpha, outcomes)
        for alpha in (0.55, 0.625, 0.75)
        for outcomes in (4, 16, 64, 256, 4096, 65536)
    ]
    failures = sum(
        not control.exact_finite_projection_geometry_verified
        for control in controls
    )
    tail_by_aspect = [
        next(
            row
            for row in scaling
            if row.fiber_aspect == alpha and row.outcome_count == 65536
        )
        for alpha in (0.55, 0.625, 0.75)
    ]
    shrinking = all(
        all(
            right.maximum_edge_deviation_from_fiber_aspect
            < left.maximum_edge_deviation_from_fiber_aspect
            for left, right in zip(rows, rows[1:])
        )
        for alpha in (0.55, 0.625, 0.75)
        for rows in [[row for row in scaling if row.fiber_aspect == alpha]]
    )
    sparse_boundary = bool(
        shrinking
        and all(row.small_trace_caused_by_low_rank_not_small_positive_edge for row in tail_by_aspect)
    )
    exact = failures == 0
    return ComponentPovmSparseSupportBoundaryReport(
        created_at=utc_now(),
        primary_literature=[
            {
                "id": "ERDOS-FARRELL-2013-JACOBI",
                "title": "Local Eigenvalue Density for General MANOVA Matrices",
                "url": PRIMARY_SOURCE_URL,
                "scope": "Jacobi/MANOVA limiting support; the repository uses the equivalent free-projection parameterization.",
            }
        ],
        theorem_contract={
            "deterministic_component_povm": (
                "Every normalized child embedding and coordinate-block partition "
                "gives H_e=W*P_eW, sum_e H_e=I, and rank(H_e)<=min(r,b_e)."
            ),
            "generic_position_atoms": (
                "For a Haar isometry, generic position gives zero multiplicity "
                "max(r-b_e,0) and one multiplicity max(r+b_e-N,0)."
            ),
            "free_jacobi_edges": (
                "At fixed aspects alpha=r/N and beta=b_e/N, the fractional "
                "spectrum has support (sqrt((1-alpha)beta) +- "
                "sqrt(alpha(1-beta)))^2."
            ),
            "sparse_outcome_limit": (
                "As beta tends to zero at fixed alpha, positive eigenvalues "
                "concentrate at alpha with width exactly "
                "4 sqrt(alpha(1-alpha)beta(1-beta)), while support rank and "
                "trace fractions are beta/alpha and beta."
            ),
            "scope": (
                "The finite identities and Haar benchmark do not prove that "
                "natural Plancherel/Racah component effects are Haar, free, or "
                "edge-rigid. Natural block aspects and coherent support SELECT "
                "remain open."
            ),
        },
        finite_controls=controls,
        sparse_scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "separate_small_effect_trace_from_small_positive_effect_edge",
                "resolved": exact and sparse_boundary,
                "resolution": "The exact rank atoms and Jacobi sparse-block limit exhibit exponentially small trace carried by exponentially small support rank at constant positive eigenvalue scale.",
            },
            {
                "obligation": "identify_natural_component_block_and_fiber_aspects",
                "resolved": False,
                "resolution": "Compute N, r, and every b_e under the frame-weighted natural node law, rather than unweighted finite portfolios.",
            },
            {
                "obligation": "prove_natural_sparse_component_jacobi_universality_and_edge_rigidity",
                "resolved": False,
                "resolution": "Need mixed trace moments or a representation-specific concentration theorem for W*P_eW under globally distinct Plancherel/Racah data.",
            },
            {
                "obligation": "compile_coherent_component_support_projector_select",
                "resolved": False,
                "resolution": "Even a constant positive effect edge leaves the support projector and its controlled GPE transport to be synthesized uniformly without an exponential table.",
            },
            {
                "obligation": "control_all_depth_support_scalar_approximation_error",
                "resolved": False,
                "resolution": "A natural edge law must hold in operator norm on positive accepted mass strongly enough to compose through Theta(log n!) recursive levels.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "An exponentially small orientation outcome necessarily gives an exponentially small nonzero H_e eigenvalue.",
                "resolved": True,
                "resolution": "False in the sparse-block Jacobi regime: its trace is small because rank fraction is beta/alpha, while positive eigenvalues converge to alpha."
            },
            {
                "objection": "The generic delta^(-1/4) square-root bound proves every many-outcome component POVM is hard.",
                "resolved": True,
                "resolution": "False without a small positive edge. Outcome probability or trace alone does not supply delta; a low-rank constant-edge effect evades that premise."
            },
            {
                "objection": "The Haar benchmark proves natural component effects are asymptotically support scalar.",
                "resolved": False,
                "resolution": "No. Natural Racah embeddings may have arithmetic correlations, non-Haar support alignment, outliers, or tiny edge channels. A universality theorem is mandatory."
            },
            {
                "objection": "Support-scalarity would by itself compile the recursive PGM.",
                "resolved": False,
                "resolution": "The algorithm still needs coherent support SELECT, support transport, endpoint mixing, holonomy control, accepted mass, and decoding."
            },
        ],
        headline_metrics={
            "exact_component_projection_geometry_theorem_count": int(exact),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "sparse_outcome_jacobi_limit_theorem_count": int(sparse_boundary),
            "sparse_scaling_record_count": len(scaling),
            "tail_minimum_positive_edge": min(row.fractional_edge_lower for row in tail_by_aspect),
            "tail_maximum_support_rank_fraction": max(row.positive_support_rank_fraction_within_fiber for row in tail_by_aspect),
            "tail_maximum_edge_deviation_from_fiber_aspect": max(row.maximum_edge_deviation_from_fiber_aspect for row in tail_by_aspect),
            "natural_component_jacobi_universality_theorem_count": 0,
            "natural_component_support_select_circuit_count": 0,
            "recursive_orientation_polar_sampler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "small_trace_implies_small_positive_effect_edge": False,
            "generic_square_root_qsvt_obstruction_applies_from_trace_alone": False,
            "haar_sparse_outcome_effects_become_support_scalar": sparse_boundary,
            "natural_component_effects_obey_haar_jacobi_law": False,
            "natural_positive_effect_edge_proved": False,
            "natural_component_support_select_compiled": False,
            "high_dimension_partial_support_native_mass_controlled": False,
            "recursive_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The correct random-isometry benchmark replaces a putative "
                "small-eigenvalue bottleneck by low-rank support selection, but "
                "natural Jacobi universality, edge rigidity, coherent support "
                "SELECT, and physical mass are all unproved."
            ),
        },
        status=(
            "sparse-support-jacobi-boundary-proved-natural-universality-and-select-open"
            if exact and sparse_boundary
            else "component-povm-sparse-support-control-failure"
        ),
        summary=(
            "Proved that rare component outcomes need not have small positive "
            "effect eigenvalues and identified sparse support-projector SELECT, "
            "not generic square-root approximation, as the relevant Haar-model "
            "compiler bottleneck."
        ),
        falsifiers_triggered=[
            "Small component trace is not evidence for an exponentially small positive effect edge.",
            "Many outcomes do not by themselves activate the generic square-root polynomial lower bound.",
            "The Haar sparse-support law is a benchmark, not a natural wreath-frame theorem.",
            "Asymptotic support-scalarity would not remove the coherent support-SELECT and holonomy problems.",
        ],
    )


def write_component_povm_sparse_support_boundary_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-SPARSE-SUPPORT-BOUNDARY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_component_povm_sparse_support_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-COMPONENT-POVM-SPARSE-SUPPORT-BOUNDARY",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-SPARSE-SUPPORT-BOUNDARY."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-SPARSE-SUPPORT-BOUNDARY."
                ),
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
                    "self_dual_wreath_component_povm_sparse_support_boundary": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_component_povm_sparse_support_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
