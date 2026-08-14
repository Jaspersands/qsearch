"""Branch-only candidate erasure inherits the square-root normalization loss.

Let ``C`` be the candidate conjugacy class, ``|C|=M``, and let
``B_h:E_h->H`` be the isometric synthesis embedding for candidate ``h``.  The
clean controlled preparation

    V(direct_sum_h x_h) = sum_h |h> B_h x_h              (1)

is an isometry because the candidate label keeps the summands orthogonal.  A
one-row operation on that label has a normalized coefficient vector ``c`` and
therefore induces

    T_c(direct_sum_h x_h) = sum_h conj(c_h) B_h x_h.      (2)

To obtain one common multiple ``S/alpha`` of the unlabelled synthesis
``S=sum_h B_h`` on the entire direct sum, every coefficient must equal
``1/alpha``.  The row-norm identity then forces

    alpha >= sqrt(M),                                    (3)

with equality for the uniform Fourier row.  Candidate-dependent phases do not
help because the target polar fixes their relative phases; retaining several
Fourier rows avoids some postselection loss only by retaining an unresolved
candidate-character register.

For an input in a relative spectral window
``S^*S in [1-delta,1+delta]``, the uniform erasure succeeds with probability

    ||Sx||^2/M in [(1-delta)/M,(1+delta)/M].              (4)

Thus even after the exact bulk-conditioning theorem, postselection and
ordinary amplitude amplification need ``Theta(sqrt(M))`` uses in this
architecture.  Source canonicalization and branch QFTs do not change (3).

This is deliberately not an arbitrary-circuit lower bound.  It does not cover
a transform that acts jointly on candidate and physical multiplicity data,
coherently computes and relocates the candidate label from the carrier, or
implements the row polar without a one-row branch erasure.  Those mechanisms
are now the only meaningful normalization escapes.
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
from coset_hidden_involution_bulk_conditioning_normalization_no_go import (
    alternative_outside_window_bound,
    bulk_copy_count,
)
from coset_hidden_involution_incidence_walk_boundary import incidence_matrix
from coset_perfect_matching_spherical_boundary import perfect_matching_count
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_branch_erasure_normalization_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-BRANCH-ERASURE-NORMALIZATION-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class BranchErasureFiniteControl:
    n: int
    transposition_count: int
    copy_count: int
    candidate_count: int
    physical_dimension: int
    source_dimension: int
    labelled_dilation_dimension: int
    maximum_labelled_isometry_residual: float
    uniform_erasure_synthesis_residual: float
    uniform_erasure_amplitude: float
    uniform_erasure_success_scale: float
    minimum_observed_success_probability: float
    maximum_observed_success_probability: float
    minimum_predicted_success_probability: float
    maximum_predicted_success_probability: float
    exact_success_spectrum_residual: float
    exact_branch_erasure_boundary_verified: bool
    status: str


@dataclass(frozen=True)
class BranchErasureScalingRecord:
    half_degree: int
    degree: int
    candidate_count_decimal: str
    copy_count: int
    retained_alternative_mass_lower_bound: float
    bulk_success_probability_lower_log2: float
    bulk_success_probability_upper_log2: float
    branch_erasure_normalization_log2_lower_bound: float
    amplitude_amplification_query_log2_lower_order: float
    branch_only_erasure_polynomial: bool
    joint_physical_multiplicity_escape_ruled_out: bool
    status: str


@dataclass(frozen=True)
class BranchErasureNormalizationTheorem:
    labelled_dilation: str
    one_row_kraus_map: str
    coefficient_norm_obstruction: str
    bulk_success_transfer: str
    retained_character_boundary: str
    architecture_consequence: str
    scope_limit: str
    exact_labelled_isometry_proved: bool
    uniform_erasure_equals_S_over_sqrt_M: bool
    arbitrary_branch_row_sqrt_M_boundary_proved: bool
    bulk_inverse_M_success_proved: bool
    branch_only_amplification_superpolynomial: bool
    joint_source_physical_transform_ruled_out: bool
    direct_orbit_row_polar_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class BranchErasureNormalizationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[BranchErasureFiniteControl]
    scaling_records: list[BranchErasureScalingRecord]
    theorem: BranchErasureNormalizationTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def branch_row_normalization_lower_bound(candidate_count: int) -> float:
    if candidate_count < 2:
        raise ValueError("candidate_count must be at least two")
    return math.sqrt(candidate_count)


def retained_character_acceptance_bound(
    candidate_count: int,
    retained_character_count: int,
) -> float:
    if candidate_count < 2:
        raise ValueError("candidate_count must be at least two")
    if not 0 <= retained_character_count <= candidate_count:
        raise ValueError("retained character count is outside the label space")
    return retained_character_count / candidate_count


def audit_branch_erasure_normalization(
    n: int,
    transposition_count: int,
    copy_count: int,
    *,
    tolerance: float = 1e-9,
) -> BranchErasureFiniteControl:
    """Verify the labelled Stinespring map and every-source success spectrum."""

    incidence, column_candidates = incidence_matrix(
        n, transposition_count, copy_count
    )
    candidate_count = involution_class_size(n, transposition_count)
    source_column_degree = 2**copy_count
    synthesis = incidence / math.sqrt(source_column_degree)
    physical_dimension, source_dimension = synthesis.shape
    candidates = tuple(sorted(set(column_candidates)))
    candidate_index = {candidate: index for index, candidate in enumerate(candidates)}
    if len(candidates) != candidate_count:
        raise AssertionError("incidence candidate labels are incomplete")

    labelled = np.zeros(
        (candidate_count * physical_dimension, source_dimension),
        dtype=float,
    )
    for column, candidate in enumerate(column_candidates):
        branch = candidate_index[candidate]
        rows = slice(
            branch * physical_dimension,
            (branch + 1) * physical_dimension,
        )
        labelled[rows, column] = synthesis[:, column]

    labelled_residual = float(
        np.linalg.norm(
            labelled.T @ labelled - np.eye(source_dimension),
            ord=2,
        )
    )
    erasure = np.hstack(
        [
            np.eye(physical_dimension) / math.sqrt(candidate_count)
            for _ in range(candidate_count)
        ]
    )
    postselected = erasure @ labelled
    target = synthesis / math.sqrt(candidate_count)
    erasure_residual = float(np.linalg.norm(postselected - target, ord=2))

    gram = synthesis.T @ synthesis
    eigenvalues = np.linalg.eigvalsh((gram + gram.T) / 2.0)
    observed_success = np.linalg.eigvalsh(
        (postselected.T @ postselected + postselected.T @ postselected) / 2.0
    )
    predicted_success = eigenvalues / candidate_count
    spectrum_residual = float(
        np.max(np.abs(observed_success - predicted_success))
    )
    verified = bool(
        labelled_residual <= 100 * tolerance
        and erasure_residual <= 100 * tolerance
        and spectrum_residual <= 100 * tolerance
    )
    return BranchErasureFiniteControl(
        n=n,
        transposition_count=transposition_count,
        copy_count=copy_count,
        candidate_count=candidate_count,
        physical_dimension=physical_dimension,
        source_dimension=source_dimension,
        labelled_dilation_dimension=candidate_count * physical_dimension,
        maximum_labelled_isometry_residual=labelled_residual,
        uniform_erasure_synthesis_residual=erasure_residual,
        uniform_erasure_amplitude=1.0 / math.sqrt(candidate_count),
        uniform_erasure_success_scale=1.0 / candidate_count,
        minimum_observed_success_probability=float(np.min(observed_success)),
        maximum_observed_success_probability=float(np.max(observed_success)),
        minimum_predicted_success_probability=float(np.min(predicted_success)),
        maximum_predicted_success_probability=float(np.max(predicted_success)),
        exact_success_spectrum_residual=spectrum_residual,
        exact_branch_erasure_boundary_verified=verified,
        status=(
            "exact-branch-erasure-sqrt-M-boundary-verified"
            if verified
            else "branch-erasure-normalization-control-failure"
        ),
    )


def branch_erasure_scaling_record(
    half_degree: int,
    *,
    target_source_variance: float = 1e-6,
    delta: float = 0.5,
) -> BranchErasureScalingRecord:
    if half_degree < 3:
        raise ValueError("half_degree must be at least three")
    if not 0.0 < delta < 1.0:
        raise ValueError("delta must lie in (0,1)")
    candidates = perfect_matching_count(half_degree)
    copies = bulk_copy_count(candidates, target_source_variance)
    variance = (candidates - 1) / (2**copies)
    retained_mass = 1.0 - alternative_outside_window_bound(variance, delta)
    lower_log2 = math.log2(1.0 - delta) - math.log2(candidates)
    upper_log2 = math.log2(1.0 + delta) - math.log2(candidates)
    normalization_log2 = 0.5 * math.log2(candidates)
    return BranchErasureScalingRecord(
        half_degree=half_degree,
        degree=2 * half_degree,
        candidate_count_decimal=str(candidates),
        copy_count=copies,
        retained_alternative_mass_lower_bound=retained_mass,
        bulk_success_probability_lower_log2=lower_log2,
        bulk_success_probability_upper_log2=upper_log2,
        branch_erasure_normalization_log2_lower_bound=normalization_log2,
        amplitude_amplification_query_log2_lower_order=normalization_log2,
        branch_only_erasure_polynomial=False,
        joint_physical_multiplicity_escape_ruled_out=False,
        status="branch-only-erasure-superpolynomial-joint-row-transform-open",
    )


def build_branch_erasure_normalization_report(
    *,
    finite_specs: tuple[tuple[int, int, int], ...] = (
        (3, 1, 2),
        (3, 1, 3),
        (4, 2, 2),
    ),
    scaling_half_degrees: tuple[int, ...] = (3, 4, 8, 16, 32, 64, 128),
) -> BranchErasureNormalizationReport:
    controls = [audit_branch_erasure_normalization(*spec) for spec in finite_specs]
    scaling = [branch_erasure_scaling_record(m) for m in scaling_half_degrees]
    verified = all(row.exact_branch_erasure_boundary_verified for row in controls)
    scaling_verified = all(
        row.retained_alternative_mass_lower_bound > 0.999
        and not row.branch_only_erasure_polynomial
        and not row.joint_physical_multiplicity_escape_ruled_out
        for row in scaling
    )
    theorem = BranchErasureNormalizationTheorem(
        labelled_dilation=(
            "V:direct_sum_h E_h -> C^C tensor H, Vx=sum_h |h>B_hx_h, "
            "is an exact isometry."
        ),
        one_row_kraus_map=(
            "A normalized success row c on the candidate label induces "
            "T_c x=sum_h conj(c_h)B_hx_h."
        ),
        coefficient_norm_obstruction=(
            "T_c=S/alpha on the full direct sum requires c_h=1/alpha for "
            "all h, hence alpha>=sqrt(M), with equality for the uniform row."
        ),
        bulk_success_transfer=(
            "On S^*S eigenvalues in [1-delta,1+delta], uniform erasure "
            "succeeds in [(1-delta)/M,(1+delta)/M]."
        ),
        retained_character_boundary=(
            "Keeping r orthogonal candidate characters accepts at most r/M of "
            "a uniform branch law; constant acceptance leaves Theta(M) rows."
        ),
        architecture_consequence=(
            "Candidate preparation, branch QFT, one-row erasure, and ordinary "
            "amplification cannot provide polynomial normalization."
        ),
        scope_limit=(
            "Joint source-physical multiplicity transforms, coherent candidate "
            "relocation, direct row polars, and arbitrary natural-input circuits "
            "remain open."
        ),
        exact_labelled_isometry_proved=True,
        uniform_erasure_equals_S_over_sqrt_M=True,
        arbitrary_branch_row_sqrt_M_boundary_proved=True,
        bulk_inverse_M_success_proved=True,
        branch_only_amplification_superpolynomial=True,
        joint_source_physical_transform_ruled_out=False,
        direct_orbit_row_polar_compiled=False,
        theorem_verified=verified and scaling_verified,
        status=(
            "branch-only-normalization-closed-joint-row-transform-open"
            if verified and scaling_verified
            else "branch-erasure-normalization-control-failure"
        ),
    )
    return BranchErasureNormalizationReport(
        created_at=utc_now(),
        theorem_contract={
            "family": "Perfect-matching involution candidates in S_(2m).",
            "source": "Direct sum of normalized candidate-fiber synthesis spaces.",
            "architecture": (
                "Candidate-controlled physical preparation followed by a unitary "
                "on the candidate label and one clean success row."
            ),
            "mass_window": (
                "The constant-condition alternative bulk certified by the exact "
                "source moment and size-bias theorem."
            ),
            "outside_scope": (
                "Operations coupling the candidate label to physical multiplicity "
                "coordinates, multi-round relocation, and direct polar circuits."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-JOINT-LABEL-MULTIPLICITY-RELOCATION",
                "statement": (
                    "Construct or refute a polynomial circuit that moves candidate "
                    "information into accessible S_n multiplicity coordinates before erasure."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-DIRECT-ORBIT-ROW-POLAR",
                "statement": (
                    "Compile the orbit-representative row polar without a single "
                    "candidate-label success row."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-MULTIROW-DECODER",
                "statement": (
                    "Determine whether retaining polynomially many structured "
                    "candidate characters supports a complete decoder."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "A nonuniform label state can improve the common coefficient.",
                "answer": (
                    "False: equality with S/alpha on every candidate summand fixes "
                    "all coefficients to 1/alpha, and row normalization gives alpha>=sqrt(M)."
                ),
                "resolved": True,
            },
            {
                "challenge": "Constant conditioning of S makes branch postselection constant-success.",
                "answer": (
                    "False: the exact success operator is S^*S/M, so the entire "
                    "constant relative window remains at Theta(1/M) probability."
                ),
                "resolved": True,
            },
            {
                "challenge": "Keeping many Fourier rows removes the obstruction.",
                "answer": (
                    "Only by retaining an equally large unresolved character space; "
                    "a polynomial number of rows still has vanishing uniform acceptance."
                ),
                "resolved": True,
            },
            {
                "challenge": "This proves hidden involution requires exponential time.",
                "answer": (
                    "False. The theorem is restricted to branch-only erasure and "
                    "leaves joint representation-specific row transforms open."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_labelled_dilation_control_count": len(controls),
            "finite_control_failure_count": sum(
                not row.exact_branch_erasure_boundary_verified for row in controls
            ),
            "branch_row_sqrt_M_boundary_theorem_count": 1,
            "bulk_inverse_M_success_theorem_count": 1,
            "joint_label_multiplicity_relocation_count": 0,
            "direct_orbit_row_polar_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "labelled_candidate_preparation_isometry_compiled": verified,
            "uniform_branch_erasure_equals_S_over_sqrt_M": verified,
            "branch_only_polynomial_normalization_possible": False,
            "joint_source_physical_transform_ruled_out": False,
            "direct_orbit_row_polar_compiled": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Every one-row candidate-label erasure that realizes the common "
                "synthesis inherits normalization sqrt(M); only a genuinely joint "
                "multiplicity transform or direct polar can escape."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that clean candidate-controlled preparation followed by any "
            "branch-only one-row erasure necessarily realizes S/sqrt(M), with "
            "Theta(1/M) success on the already well-conditioned alternative bulk."
        ),
        falsifiers_triggered=[
            "Changing the candidate-label preparation amplitudes cannot preserve uniform synthesis and improve normalization.",
            "A candidate-label QFT followed by one-row postselection does not exploit the regular-orbit reduction.",
            "Bulk conditioning does not turn branch-only erasure into a polynomial primitive.",
        ],
    )


def write_branch_erasure_normalization_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_branch_erasure_normalization_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_branch_erasure_normalization_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
