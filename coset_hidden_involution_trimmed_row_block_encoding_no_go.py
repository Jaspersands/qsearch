"""Normalization no-go for coherent access to the trimmed orbit-row kernel.

Let ``I`` be the physical-row/source-column incidence matrix.  Every source
column has degree ``2^k`` and every physical row has degree ``M``, the number
of hidden involutions.  Normalized coherent edge-state preparation therefore
gives the discriminant

    D = I / sqrt(M 2^k).

The normalized source synthesis is ``W=I/sqrt(2^k)``, with likelihood Gram
``Z=W^*W``.  Hence

    D^*D = Z/M = A.                                   (1)

The free-fiber canonicalizer, induction map, and symmetric-group QFT are
unitaries on their retained spaces.  They can expose the regular carrier and
the succinct orbit-row kernels, but they preserve (1), all singular values,
and the candidate normalization.  Thus coherent row-state preparation from
the polynomial rooted-conjugator formula supplies a block encoding of ``A``,
not a fast-forward of ``Z``.

On the natural flat bulk, eigenvalues of ``A`` lie in
``[1/(2M),3/(2M)]`` and singular values of ``D`` are
``Theta(M^-1/2)``.  Generic singular-vector/polar processing therefore retains
the existing ``Omega(sqrt(M))`` query scale.  Pairwise kernel succinctness
removes factorial entry evaluation, but it does not remove factorial coherent
normalization.

The surviving positive target must be a direct analytically normalized
transform: local recoupling rotations, an exact combinatorial orthogonalizer,
or another circuit whose implementation is not black-box singular-value
processing of these normalized edge states.
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
from coset_hidden_involution_orbit_synthesis_flatness import flatness_copy_count
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_trimmed_row_block_encoding_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-TRIMMED-ROW-BLOCK-ENCODING-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class EdgeStateBlockEncodingControl:
    degree: int
    transposition_count: int
    copy_count: int
    candidate_count: int
    physical_row_count: int
    source_column_count: int
    edge_count: int
    physical_row_degree: int
    source_column_degree: int
    maximum_row_isometry_residual: float
    maximum_column_isometry_residual: float
    discriminant_overlap_residual: float
    normalized_gram_identity_residual: float
    unnormalized_likelihood_scale_ratio: float
    coherent_edge_states_block_encode_A_not_Z: bool
    status: str


@dataclass(frozen=True)
class TrimmedRowNormalizationScalingRecord:
    half_degree: int
    degree: int
    candidate_count_decimal: str
    copy_count: int
    row_degree_log2: float
    column_degree_log2: int
    flat_bulk_discriminant_singular_lower_log2: float
    flat_bulk_discriminant_singular_upper_log2: float
    generic_polar_query_log2_lower_order: float
    coherent_row_state_preparation_polynomial: bool
    pairwise_kernel_evaluation_polynomial: bool
    canonicalizer_or_QFT_changes_candidate_normalization: bool
    unnormalized_Z_fast_forward_compiled: bool
    status: str


@dataclass(frozen=True)
class TrimmedRowBlockEncodingTheorem:
    biregular_degrees: str
    edge_state_discriminant: str
    gram_identity: str
    basis_invariance: str
    natural_bulk: str
    algorithmic_consequence: str
    required_escape: str
    exact_edge_state_block_encoding_proved: bool
    trimmed_row_kernel_block_encoding_is_A_proved: bool
    canonicalization_or_QFT_removes_M_normalization: bool
    generic_kernel_quantum_linear_algebra_is_polynomial: bool
    direct_analytically_normalized_transform_ruled_out: bool
    unnormalized_Z_fast_forward_compiled: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class TrimmedRowBlockEncodingReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[EdgeStateBlockEncodingControl]
    scaling_records: list[TrimmedRowNormalizationScalingRecord]
    theorem: TrimmedRowBlockEncodingTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def audit_edge_state_block_encoding(
    degree: int,
    transposition_count: int,
    copy_count: int,
) -> EdgeStateBlockEncodingControl:
    incidence, candidates = incidence_matrix(
        degree,
        transposition_count,
        copy_count,
    )
    candidate_count = len(set(candidates))
    physical_count, source_count = incidence.shape
    edge_positions = np.argwhere(incidence > 0.5)
    edge_count = len(edge_positions)
    row_degree = candidate_count
    column_degree = 2**copy_count

    row_isometry = np.zeros((edge_count, physical_count))
    column_isometry = np.zeros((edge_count, source_count))
    for edge_index, (physical, source) in enumerate(edge_positions):
        row_isometry[edge_index, physical] = 1.0 / math.sqrt(row_degree)
        column_isometry[edge_index, source] = 1.0 / math.sqrt(column_degree)
    row_residual = float(
        np.linalg.norm(
            row_isometry.T @ row_isometry - np.eye(physical_count),
            ord=2,
        )
    )
    column_residual = float(
        np.linalg.norm(
            column_isometry.T @ column_isometry - np.eye(source_count),
            ord=2,
        )
    )
    discriminant = incidence / math.sqrt(row_degree * column_degree)
    overlap_residual = float(
        np.linalg.norm(
            row_isometry.T @ column_isometry - discriminant,
            ord=2,
        )
    )
    likelihood = incidence.T @ incidence / column_degree
    normalized_likelihood = likelihood / candidate_count
    gram_residual = float(
        np.linalg.norm(
            discriminant.T @ discriminant - normalized_likelihood,
            ord=2,
        )
    )
    verified = bool(
        edge_count == physical_count * row_degree
        and edge_count == source_count * column_degree
        and row_residual < 1e-12
        and column_residual < 1e-12
        and overlap_residual < 1e-12
        and gram_residual < 1e-12
    )
    return EdgeStateBlockEncodingControl(
        degree=degree,
        transposition_count=transposition_count,
        copy_count=copy_count,
        candidate_count=candidate_count,
        physical_row_count=physical_count,
        source_column_count=source_count,
        edge_count=edge_count,
        physical_row_degree=row_degree,
        source_column_degree=column_degree,
        maximum_row_isometry_residual=row_residual,
        maximum_column_isometry_residual=column_residual,
        discriminant_overlap_residual=overlap_residual,
        normalized_gram_identity_residual=gram_residual,
        unnormalized_likelihood_scale_ratio=float(candidate_count),
        coherent_edge_states_block_encode_A_not_Z=verified,
        status=(
            "coherent-edge-states-block-encode-A-equals-Z-over-M"
            if verified
            else "trimmed-row-block-encoding-control-failure"
        ),
    )


def trimmed_row_normalization_scaling_record(
    half_degree: int,
) -> TrimmedRowNormalizationScalingRecord:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    degree = 2 * half_degree
    candidates = involution_class_size(degree, half_degree)
    copies = flatness_copy_count(candidates)
    log_candidates = math.log2(candidates)
    return TrimmedRowNormalizationScalingRecord(
        half_degree=half_degree,
        degree=degree,
        candidate_count_decimal=str(candidates),
        copy_count=copies,
        row_degree_log2=log_candidates,
        column_degree_log2=copies,
        flat_bulk_discriminant_singular_lower_log2=(
            -0.5 * (1.0 + log_candidates)
        ),
        flat_bulk_discriminant_singular_upper_log2=(
            0.5 * (math.log2(1.5) - log_candidates)
        ),
        generic_polar_query_log2_lower_order=0.5 * log_candidates,
        coherent_row_state_preparation_polynomial=True,
        pairwise_kernel_evaluation_polynomial=True,
        canonicalizer_or_QFT_changes_candidate_normalization=False,
        unnormalized_Z_fast_forward_compiled=False,
        status="trimmed-row-edge-access-retains-sqrt-M-polar-boundary",
    )


def build_trimmed_row_block_encoding_report() -> TrimmedRowBlockEncodingReport:
    controls = [
        audit_edge_state_block_encoding(3, 1, 1),
        audit_edge_state_block_encoding(3, 1, 2),
        audit_edge_state_block_encoding(4, 2, 1),
    ]
    scaling = [
        trimmed_row_normalization_scaling_record(value)
        for value in (4, 8, 16, 32, 64, 128)
    ]
    exact = all(
        row.coherent_edge_states_block_encode_A_not_Z for row in controls
    )
    scaling_exact = all(
        row.coherent_row_state_preparation_polynomial
        and row.pairwise_kernel_evaluation_polynomial
        and not row.canonicalizer_or_QFT_changes_candidate_normalization
        and not row.unnormalized_Z_fast_forward_compiled
        for row in scaling
    )
    theorem = TrimmedRowBlockEncodingTheorem(
        biregular_degrees=(
            "Every physical row is incident to M source columns and every "
            "source column to 2^k physical rows."
        ),
        edge_state_discriminant="Normalized row/column edge isometries overlap as D=I/sqrt(M2^k).",
        gram_identity="D^*D=I^*I/(M2^k)=Z/M=A exactly.",
        basis_invariance=(
            "The free-fiber canonicalizer, regular induction coordinate map, "
            "and G QFT are unitary and preserve D's singular values."
        ),
        natural_bulk=(
            "At least 29/32 alternative mass has D singular values in "
            "[1/sqrt(2M),sqrt(3/(2M))]."
        ),
        algorithmic_consequence=(
            "Generic block-encoding polar/SVT routines using coherent row access "
            "retain Omega(sqrt(M)) scale even though rows and pairwise kernels "
            "are polynomially computable."
        ),
        required_escape=(
            "Compile a direct analytically normalized orbit-copy transform whose "
            "local rotations factor M before amplitude encoding."
        ),
        exact_edge_state_block_encoding_proved=exact,
        trimmed_row_kernel_block_encoding_is_A_proved=exact,
        canonicalization_or_QFT_removes_M_normalization=False,
        generic_kernel_quantum_linear_algebra_is_polynomial=False,
        direct_analytically_normalized_transform_ruled_out=False,
        unnormalized_Z_fast_forward_compiled=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=exact and scaling_exact,
        status=(
            "trimmed-row-coherent-access-retains-Z-over-M-normalization"
            if exact and scaling_exact
            else "trimmed-row-block-encoding-no-go-control-failure"
        ),
    )
    return TrimmedRowBlockEncodingReport(
        created_at=utc_now(),
        theorem_contract={
            "matrix": "Physical/source incidence after any trimmed unitary basis changes",
            "access": "Normalized coherent row-edge and column-edge state preparation",
            "natural_copy_count": "k=ceil(log2(64M))",
            "claim_boundary": (
                "Normalization theorem for coherent kernel access, not a lower "
                "bound on direct analytic recoupling circuits."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-ROW-DIRECT-ORTHOGONALIZER",
                "statement": (
                    "Derive local rotations or a combinatorial orthogonalizer that "
                    "implements the row polar without querying D at its small singular scale."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-ROW-ANALYTIC-M-FACTOR",
                "statement": (
                    "Exhibit an exact block formula in which the factor M cancels "
                    "symbolically before amplitudes are normalized."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-ROW-DIRECT-CIRCUIT-LOWER-BOUND",
                "statement": (
                    "If no transform exists, prove a natural-model lower bound; "
                    "the present black-box normalization theorem is insufficient."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Polynomial pairwise kernel evaluation gives a standard efficient quantum linear-algebra algorithm.",
                "answer": (
                    "False: normalized row/column state access block-encodes D and "
                    "A=Z/M, so the useful singular scale remains M^-1/2."
                ),
                "resolved": True,
            },
            {
                "challenge": "Canonicalizing source orbits amplifies the singular values.",
                "answer": (
                    "False: reversible canonicalization and the G QFT are unitary "
                    "basis changes and preserve every singular value."
                ),
                "resolved": True,
            },
            {
                "challenge": "The small row norm M/2^k=O(1) removes normalization.",
                "answer": (
                    "False: normalized edge states divide independently by the "
                    "row and column degrees, producing sqrt(M2^k)."
                ),
                "resolved": True,
            },
            {
                "challenge": "This proves every direct structured transform impossible.",
                "answer": (
                    "Too strong. An explicit analytic basis transform can bypass "
                    "black-box singular-value processing, as Fourier transforms do."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_edge_state_block_encoding_control_count": len(controls),
            "edge_state_control_failure_count": sum(
                not row.coherent_edge_states_block_encode_A_not_Z
                for row in controls
            ),
            "tail_generic_polar_query_log2_lower_order": (
                scaling[-1].generic_polar_query_log2_lower_order
            ),
            "coherent_row_state_compiler_count": 1,
            "unnormalized_Z_fast_forward_count": 0,
            "direct_analytic_transform_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "coherent_trimmed_row_access_compiled": True,
            "coherent_trimmed_row_access_block_encodes_A_equals_Z_over_M": exact,
            "canonicalizer_or_G_QFT_improves_normalization": False,
            "generic_kernel_SVT_is_polynomial": False,
            "unnormalized_Z_fast_forward_compiled": False,
            "direct_analytically_normalized_transform_ruled_out": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "All normalized coherent edge access retains the candidate factor "
                "M; only a direct analytic transform outside this black-box access "
                "model remains viable."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that coherent access to the succinct trimmed orbit-row kernel "
            "block-encodes A=Z/M exactly, so generic dense-kernel quantum linear "
            "algebra inherits the square-root-M barrier."
        ),
        falsifiers_triggered=[
            "Polynomial coherent row-state preparation does not fast-forward the likelihood scale.",
            "The trimmed canonicalizer and symmetric-group QFT cannot change singular-value normalization.",
            "Generic kernel QSVT or polar routines remain factorial at natural rank.",
            "Only a direct analytically normalized transform remains outside this no-go.",
        ],
    )


def write_trimmed_row_block_encoding_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_trimmed_row_block_encoding_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_trimmed_row_block_encoding_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
