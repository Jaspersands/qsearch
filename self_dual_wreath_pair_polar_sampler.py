"""Constant-conditioned polar sampler for two orientation projectors.

Let ``E`` and ``F`` be orthogonal projectors and define the analysis map

    R|psi> = |0> E|psi> + |1> F|psi>,       S=R^*R=E+F.

Jordan's two-projector decomposition expresses every nontrivial block using a
principal correlation ``c``.  The positive eigenvalues of ``S`` on that block
are ``1-c`` and ``1+c``.  A common range has ``c=1`` and contributes the sole
positive eigenvalue ``2``; it does not create a small positive singular value.

The exact wreath pair-angle theorem says that every noncommon correlation of
two orientation invariant projectors is ``1/d_alpha``.  For ``S_n``, ``n>=5``,
every non-one-dimensional irrep has ``d_alpha>=n-1``.  Hence

    spec_+(E+F) subset [1-1/(n-1), 1+1/(n-1)] union {1,2},

and the support condition number is at most ``2(n-1)/(n-2)``.  The normalized
analysis ``R/sqrt(2)`` therefore has a constant singular gap.  Controlled
invariant-projector block encodings plus singular-value transformation give a
polynomial, logarithmic-precision implementation of the polar isometry
``R(E+F)^(-1/2)``.

This is a genuine positive primitive: noncommutation does not by itself make
the wreath PGM sampler hard.  It is not a full decoder.  A recursive sampler
must merge already-combined subspaces; the pair-angle theorem does not bound
the new higher-level angles, and a local fusion architecture must also be
checked against the Moore--Russell--Sniady sieve lower bound.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import integer_partitions
from research_registry import utc_now
from self_dual_wreath_collision_free_frame_probe import Label
from self_dual_wreath_orientation_fourier_reduction import (
    _w4_collision_free_labels,
    orientation_invariant_projector,
)
from self_dual_wreath_orientation_pair_angle_spectrum import (
    exact_pair_principal_angle_spectrum,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_pair_polar_sampler.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-PAIR-POLAR-SAMPLER"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PairPolarControl:
    control_id: str
    n: int
    target_partition: tuple[int, ...]
    labels: tuple[Label, ...]
    left_orientation_mask: int
    right_orientation_mask: int
    carrier_dimension: int
    left_projector_rank: int
    right_projector_rank: int
    nonzero_principal_correlation_count: int
    common_range_dimension: int
    maximum_noncommon_principal_correlation: float
    maximum_pair_angle_formula_residual: float
    minimum_positive_projector_sum_eigenvalue: float
    maximum_projector_sum_eigenvalue: float
    support_condition_number: float
    predicted_support_condition_upper_bound: float
    projector_sum_spectrum_formula_residual: float
    normalized_analysis_minimum_positive_singular_value: float
    polar_support_isometry_residual: float
    exact_pair_polar_sampler_validation: bool
    status: str


@dataclass(frozen=True)
class PairPolarScalingRecord:
    n: int
    maximum_noncommon_principal_correlation: float
    minimum_positive_projector_sum_eigenvalue_lower_bound: float
    maximum_projector_sum_eigenvalue_upper_bound: float
    support_condition_number_upper_bound: float
    normalized_analysis_singular_gap_lower_bound: float
    polar_query_prefactor_upper_bound: float
    precision_dependence: str
    invariant_projector_block_encoding_polynomial: bool
    pair_polar_sampler_polynomial: bool
    recursive_global_sampler_proved: bool
    status: str


@dataclass(frozen=True)
class PairPolarSamplerReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[PairPolarControl]
    scaling_records: list[PairPolarScalingRecord]
    proof_obligations: list[dict[str, bool | str]]
    adversarial_audit: list[dict[str, bool | str]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _projector_basis(projector: np.ndarray, tolerance: float) -> np.ndarray:
    eigenvalues, eigenvectors = np.linalg.eigh(
        (projector + projector.conj().T) / 2
    )
    return eigenvectors[:, eigenvalues > 1 - 100 * tolerance]


def _positive_inverse_square_root(
    matrix: np.ndarray,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    eigenvalues, eigenvectors = np.linalg.eigh(
        (matrix + matrix.conj().T) / 2
    )
    if eigenvalues[0] < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    positive = eigenvalues > tolerance
    values = np.zeros_like(eigenvalues)
    values[positive] = eigenvalues[positive] ** -0.5
    inverse = (eigenvectors * values) @ eigenvectors.conj().T
    support = eigenvectors[:, positive] @ eigenvectors[:, positive].conj().T
    return inverse, support, eigenvalues[positive]


def projector_sum_spectrum_from_correlations(
    left_rank: int,
    right_rank: int,
    correlations: tuple[float, ...],
    *,
    tolerance: float = 1e-10,
) -> np.ndarray:
    if left_rank < 0 or right_rank < 0:
        raise ValueError("projector ranks must be nonnegative")
    if len(correlations) > min(left_rank, right_rank):
        raise ValueError("too many principal correlations")
    values: list[float] = []
    for correlation in correlations:
        if not tolerance < correlation <= 1 + tolerance:
            raise ValueError("only positive principal correlations are expected")
        if correlation >= 1 - tolerance:
            values.append(2.0)
        else:
            values.extend((1 - correlation, 1 + correlation))
    unmatched = left_rank + right_rank - 2 * len(correlations)
    values.extend((1.0,) * unmatched)
    return np.asarray(sorted(values))


def audit_pair_polar_sampler(
    control_id: str,
    n: int,
    target: tuple[int, ...],
    labels: tuple[Label, ...],
    left_mask: int,
    right_mask: int,
    *,
    tolerance: float = 1e-8,
) -> PairPolarControl:
    if left_mask == right_mask:
        raise ValueError("distinct orientation masks are required")
    left = orientation_invariant_projector(target, labels, left_mask)
    right = orientation_invariant_projector(target, labels, right_mask)
    left_basis = _projector_basis(left, tolerance)
    right_basis = _projector_basis(right, tolerance)
    left_rank = left_basis.shape[1]
    right_rank = right_basis.shape[1]
    actual_correlations = np.linalg.svd(
        left_basis.conj().T @ right_basis,
        compute_uv=False,
    )
    actual_correlations = tuple(
        sorted(
            (
                float(value)
                for value in actual_correlations
                if value > tolerance
            ),
            reverse=True,
        )
    )
    predicted_rows = exact_pair_principal_angle_spectrum(
        target,
        labels,
        left_mask,
        right_mask,
    )
    predicted_correlations = tuple(
        sorted(
            (
                float(value)
                for value, multiplicity, _ in predicted_rows
                for _ in range(multiplicity)
            ),
            reverse=True,
        )
    )
    if len(actual_correlations) != len(predicted_correlations):
        angle_residual = math.inf
    else:
        angle_residual = max(
            (
                abs(actual - predicted)
                for actual, predicted in zip(
                    actual_correlations,
                    predicted_correlations,
                )
            ),
            default=0.0,
        )
    projector_sum = left + right
    actual_positive = np.linalg.eigvalsh(
        (projector_sum + projector_sum.conj().T) / 2
    )
    actual_positive = actual_positive[actual_positive > tolerance]
    predicted_positive = projector_sum_spectrum_from_correlations(
        left_rank,
        right_rank,
        actual_correlations,
        tolerance=tolerance,
    )
    if len(actual_positive) != len(predicted_positive):
        spectrum_residual = math.inf
    else:
        spectrum_residual = float(
            np.max(np.abs(actual_positive - predicted_positive))
            if len(actual_positive)
            else 0.0
        )
    analysis = np.vstack((left, right))
    inverse, support, positive = _positive_inverse_square_root(
        projector_sum,
        tolerance,
    )
    polar = analysis @ inverse
    polar_residual = float(
        np.linalg.norm(polar.conj().T @ polar - support, ord=2)
    )
    noncommon = [
        value for value in actual_correlations if value < 1 - 100 * tolerance
    ]
    max_noncommon = max(noncommon, default=0.0)
    common = sum(value >= 1 - 100 * tolerance for value in actual_correlations)
    condition = float(positive[-1] / positive[0]) if len(positive) else 1.0
    predicted_condition = (
        2 / (1 - max_noncommon) if max_noncommon else 2.0
    )
    verified = (
        angle_residual <= 100 * tolerance
        and spectrum_residual <= 100 * tolerance
        and polar_residual <= 100 * tolerance
        and condition <= predicted_condition + 100 * tolerance
    )
    return PairPolarControl(
        control_id=control_id,
        n=n,
        target_partition=target,
        labels=labels,
        left_orientation_mask=left_mask,
        right_orientation_mask=right_mask,
        carrier_dimension=len(left),
        left_projector_rank=left_rank,
        right_projector_rank=right_rank,
        nonzero_principal_correlation_count=len(actual_correlations),
        common_range_dimension=common,
        maximum_noncommon_principal_correlation=max_noncommon,
        maximum_pair_angle_formula_residual=angle_residual,
        minimum_positive_projector_sum_eigenvalue=(
            float(positive[0]) if len(positive) else 0.0
        ),
        maximum_projector_sum_eigenvalue=(
            float(positive[-1]) if len(positive) else 0.0
        ),
        support_condition_number=condition,
        predicted_support_condition_upper_bound=predicted_condition,
        projector_sum_spectrum_formula_residual=spectrum_residual,
        normalized_analysis_minimum_positive_singular_value=(
            math.sqrt(float(positive[0]) / 2) if len(positive) else 0.0
        ),
        polar_support_isometry_residual=polar_residual,
        exact_pair_polar_sampler_validation=verified,
        status=(
            "exact-constant-conditioned-pair-polar-control"
            if verified
            else "pair-polar-validation-failure"
        ),
    )


def pair_polar_scaling_record(n: int) -> PairPolarScalingRecord:
    if n < 5:
        raise ValueError("the all-n noncommon dimension bound starts at n=5")
    correlation = 1 / (n - 1)
    minimum = 1 - correlation
    condition = 2 / minimum
    singular_gap = math.sqrt(minimum / 2)
    return PairPolarScalingRecord(
        n=n,
        maximum_noncommon_principal_correlation=correlation,
        minimum_positive_projector_sum_eigenvalue_lower_bound=minimum,
        maximum_projector_sum_eigenvalue_upper_bound=2.0,
        support_condition_number_upper_bound=condition,
        normalized_analysis_singular_gap_lower_bound=singular_gap,
        polar_query_prefactor_upper_bound=1 / singular_gap,
        precision_dependence="O(log(1/error)) singular-value transformation",
        invariant_projector_block_encoding_polynomial=True,
        pair_polar_sampler_polynomial=True,
        recursive_global_sampler_proved=False,
        status="pair-polar-polynomial-global-composition-open",
    )


def _finite_controls() -> list[PairPolarControl]:
    controls: list[PairPolarControl] = []
    for tuple_index, labels in enumerate(_w4_collision_free_labels()[:3]):
        count = 1 << len(labels)
        for target in integer_partitions(4):
            for left_mask, right_mask in itertools.combinations(range(count), 2):
                left = orientation_invariant_projector(target, labels, left_mask)
                right = orientation_invariant_projector(target, labels, right_mask)
                if (
                    float(np.trace(left).real) < 1e-8
                    and float(np.trace(right).real) < 1e-8
                ):
                    continue
                controls.append(
                    audit_pair_polar_sampler(
                        (
                            f"W4-{tuple_index}-{'-'.join(map(str, target))}-"
                            f"{left_mask}-{right_mask}"
                        ),
                        4,
                        target,
                        labels,
                        left_mask,
                        right_mask,
                    )
                )
    return controls


def run_pair_polar_sampler() -> PairPolarSamplerReport:
    controls = _finite_controls()
    scaling = [
        pair_polar_scaling_record(n)
        for n in (5, 8, 16, 32, 64, 128, 256, 512)
    ]
    failures = sum(not row.exact_pair_polar_sampler_validation for row in controls)
    noncommuting_controls = sum(
        row.maximum_noncommon_principal_correlation > 1e-8
        for row in controls
    )
    maximum_condition = max(row.support_condition_number for row in controls)
    verified = failures == 0
    return PairPolarSamplerReport(
        created_at=utc_now(),
        theorem_contract={
            "two_projector_analysis": (
                "R=|0> tensor E+|1> tensor F and R^*R=E+F."
            ),
            "jordan_spectrum": (
                "Each principal correlation c in (0,1) contributes positive "
                "eigenvalues 1-c and 1+c; c=1 contributes only eigenvalue 2."
            ),
            "wreath_pair_angle_input": (
                "Every noncommon c is 1/d_alpha, while exact common ranges "
                "are isolated at c=1."
            ),
            "symmetric_group_gap": (
                "For n>=5, d_alpha>=n-1 outside trivial/sign, so the minimum "
                "positive eigenvalue is at least 1-1/(n-1)."
            ),
            "circuit": (
                "Coherently select the two polynomial invariant-projector "
                "block encodings and apply singular-value transformation to "
                "their constant-gap normalized analysis."
            ),
            "scope": (
                "This implements one pair polar. No theorem controls principal "
                "angles after recursive merges or places a full merge tree "
                "outside the nonabelian sieve lower-bound model."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "two_projector_polar_spectrum",
                "resolved": verified,
                "resolution": (
                    "Jordan blocks give the exact 1+/-c spectrum and the finite "
                    "controls verify it against dense projector sums."
                ),
            },
            {
                "obligation": "all_n_wreath_pair_singular_gap",
                "resolved": True,
                "resolution": (
                    "The exact pair-angle theorem and the minimum nontrivial "
                    "S_n irrep dimension give a gap at least sqrt((n-2)/(2(n-1)))."
                ),
            },
            {
                "obligation": "polynomial_pair_polar_circuit",
                "resolved": True,
                "resolution": (
                    "The normalized analysis has constant singular gap and its "
                    "controlled invariant-projector blocks have polynomial circuits."
                ),
            },
            {
                "obligation": "recursive_angle_stability",
                "resolved": False,
                "resolution": (
                    "No lower bound is known for the positive principal-angle "
                    "gap between ranges produced by previous merge levels."
                ),
            },
            {
                "obligation": "sieve_model_escape",
                "resolved": False,
                "resolution": (
                    "A pairwise recursive construction must be formally compared "
                    "with Moore--Russell--Sniady before it can be promoted."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Noncommuting orientation projectors rule out direct polar sampling.",
                "resolved": True,
                "resolution": (
                    "False for pairs. Their noncommuting Jordan blocks are better "
                    "conditioned as n grows because c<=1/(n-1)."
                ),
            },
            {
                "objection": "Exact common ranges make the pair inverse singular.",
                "resolved": True,
                "resolution": (
                    "The zero antisymmetric direction is outside support; the "
                    "common symmetric direction has eigenvalue two."
                ),
            },
            {
                "objection": "Constant pair conditioning proves the full orientation sampler efficient.",
                "resolved": False,
                "resolution": (
                    "No. Whitening a pair changes the subspaces seen by the next "
                    "level, where near-parallel nonidentical ranges may emerge."
                ),
            },
            {
                "objection": "A balanced pair tree automatically avoids known sieve lower bounds.",
                "resolved": False,
                "resolution": (
                    "No formal escape is established. A local adaptive fusion tree "
                    "may be exactly the architecture ruled out for graph isomorphism."
                ),
            },
        ],
        literature_links=[
            {
                "paper_id": "gilyen-su-low-wiebe-2018",
                "title": "Quantum singular value transformation and beyond",
                "url": "https://arxiv.org/abs/1806.01838",
                "use": (
                    "A constant-gap block encoding admits logarithmic-precision "
                    "polar/sign singular-value transformation."
                ),
                "external_theorem_not_reproved_here": True,
            },
            {
                "paper_id": "moore-russell-sniady-2007",
                "title": "On the impossibility of a quantum sieve algorithm for graph isomorphism",
                "url": "https://arxiv.org/abs/quant-ph/0612089",
                "use": (
                    "Any recursive local fusion proposal must be checked against "
                    "the paper's formal sieve model."
                ),
                "external_theorem_not_reproved_here": True,
            },
        ],
        headline_metrics={
            "constant_condition_pair_polar_theorem_count": 1,
            "polynomial_pair_polar_circuit_schema_count": 1,
            "finite_pair_control_count": len(controls),
            "finite_pair_validation_failure_count": failures,
            "finite_noncommuting_pair_control_count": noncommuting_controls,
            "maximum_finite_pair_support_condition_number": maximum_condition,
            "tail_n": scaling[-1].n,
            "tail_support_condition_number_upper_bound": (
                scaling[-1].support_condition_number_upper_bound
            ),
            "tail_normalized_analysis_singular_gap_lower_bound": (
                scaling[-1].normalized_analysis_singular_gap_lower_bound
            ),
            "recursive_angle_stability_theorem_count": 0,
            "sieve_model_escape_theorem_count": 0,
            "global_nonorthogonal_sampler_count": 0,
            "polynomial_hidden_permutation_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "pair_polar_sampler_polynomial": verified,
            "noncommutation_is_pair_sampler_obstruction": False,
            "common_ranges_are_pair_conditioning_obstruction": False,
            "recursive_pair_sampler_polynomial": False,
            "moore_russell_sniady_sieve_bound_evaded": False,
            "global_pgm_circuit_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "One nonorthogonal merge is efficiently normalized with a "
                "constant singular gap. The decisive next theorem is stability "
                "of that gap under global recursive composition, together with "
                "a formal sieve-model audit."
            ),
        },
        status=(
            "pair-polar-polynomial-global-composition-open"
            if verified
            else "pair-polar-validation-failure"
        ),
        summary=(
            "Proved that every pair of wreath orientation invariant projectors "
            "has a constant-conditioned polar sampler for n>=5. This rescues "
            "one noncommuting merge primitive but leaves recursive angle "
            "stability and the nonabelian sieve boundary unresolved."
        ),
        falsifiers_triggered=[
            (
                "Do not treat noncommutation or exact common ranges as a barrier "
                "to a single orientation-projector merge."
            ),
            (
                "Do not infer a global sampler from pair conditioning; measure "
                "the principal angles of recursively merged ranges first."
            ),
            (
                "Do not promote a pairwise merge tree before proving it lies "
                "outside the Moore--Russell--Sniady sieve model."
            ),
        ],
    )


def write_pair_polar_sampler_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_pair_polar_sampler())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_pair_polar_sampler_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
