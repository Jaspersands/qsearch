"""Naimark completion of all known-relative branch-character polars.

For one unequal source pair and a known relative permutation ``h``, the two
orientation-character Kraus factors have partial polars

    V_s(h) = polar((A(h) + s B(h))/2),  s in {+1,-1}.

The cyclic-polar compiler implements each ``V_s`` without an inverse singular
value.  Individually these partial isometries are not a complete instrument.
Let

    P_s = V_s^* V_s = supp(I+sU),  U=A^*B,
    F = P_+ + P_-.

On an eigenvalue ``omega`` of ``U``, ``F`` equals one when ``omega`` is
``+1`` or ``-1`` and equals two otherwise.  Hence ``I <= F <= 2I`` and

    J_h = (|0> V_+(h) + |1> V_-(h)) F^(-1/2)              (1)

is an exact isometry.  The same cyclic phase register implements the extra
factor: multiply by one on the ``+/-1`` phases and by ``1/sqrt(2)`` on every
other phase.  No small singular value is inverted.

For ``k`` source pairs the construction tensor-factorizes.  It uses all
``2^k`` character outputs but only ``k`` local cyclic compilers, so the
basis-independent sublinear-output-rank no-go is respected rather than
evaded.

This does not yet solve the unknown-relative covariance problem.  If one
tries to assemble candidate outputs by the block convolution

    C[g,s] = |G|^(-1/2) J_(s^-1 g),                       (2)

then

    (C^*C)[s,t] = |G|^-1 sum_g J_(s^-1g)^* J_(t^-1g).    (3)

Thus pointwise Naimark completion becomes a global operator-valued
autocorrelation problem.  Exact ``S_3`` controls show that (2) is not
automatically an isometry.  The three-pair collision-free threshold control
is nevertheless constant-conditioned, which makes an all-``n`` natural
autocorrelation theorem a legitimate positive target.  Finite conditioning
is not promoted to an asymptotic compiler or decoder.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_branch_character_cyclic_polar_compiler import (
    Label,
    Partition,
    Permutation,
    local_character_cyclic_polar,
)
from self_dual_wreath_character_moments import compose_permutations
from self_dual_wreath_orientation_fourier_reduction import (
    _source_representation_rows,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_branch_character_polar_naimark_completion.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-POLAR-NAIMARK-COMPLETION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class LocalPolarNaimarkControl:
    control_id: str
    n: int
    left_partition: Partition
    right_partition: Partition
    permutation: Permutation
    carrier_dimension: int
    plus_support_rank: int
    minus_support_rank: int
    support_frame_minimum_eigenvalue: float
    support_frame_maximum_eigenvalue: float
    support_frame_condition_number: float
    support_frame_integer_spectrum_residual: float
    naimark_isometry_residual: float
    direct_support_frame_residual: float
    exact_local_polar_naimark_completion_verified: bool
    status: str


@dataclass(frozen=True)
class TensorPolarNaimarkControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    permutation: Permutation
    factor_count: int
    character_output_count: int
    carrier_dimension: int
    output_dimension: int
    tensor_isometry_residual: float
    direct_tensor_factorization_residual: float
    exact_tensor_polar_naimark_completion_verified: bool
    status: str


@dataclass(frozen=True)
class CandidateRelativeConvolutionControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    group_order: int
    factor_count: int
    character_output_count: int
    input_dimension: int
    output_dimension: int
    minimum_singular_value: float
    maximum_singular_value: float
    condition_number: float
    convolution_isometry_residual: float
    autocorrelation_gram_residual: float
    maximum_nonidentity_autocorrelation_norm: float
    pointwise_isometries_do_not_imply_global_isometry: bool
    finite_constant_condition_observed: bool
    status: str


@dataclass(frozen=True)
class PolarNaimarkScalingRecord:
    n: int
    information_threshold_copy_count: int
    character_output_qubit_count: int
    character_output_dimension_decimal: str
    local_support_frame_condition_upper_bound: float
    local_cyclic_compilers_required: int
    known_relative_tensor_naimark_polynomial: bool
    full_coefficient_rank_used: bool
    all_n_natural_autocorrelation_gap_proved: bool
    candidate_relative_convolution_compiled: bool
    hidden_relative_decoder_compiled: bool
    status: str


@dataclass(frozen=True)
class PolarNaimarkTheorem:
    local_support_frame: str
    local_naimark_isometry: str
    cyclic_implementation: str
    tensor_completion: str
    candidate_convolution_gram: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class BranchCharacterPolarNaimarkReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PolarNaimarkTheorem
    local_controls: list[LocalPolarNaimarkControl]
    tensor_controls: list[TensorPolarNaimarkControl]
    convolution_controls: list[CandidateRelativeConvolutionControl]
    scaling_records: list[PolarNaimarkScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _psd_inverse_square_root(
    matrix: np.ndarray,
    tolerance: float = 1e-10,
) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2.0)
    if values[0] < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    inverse = np.zeros_like(values)
    positive = values > tolerance
    inverse[positive] = 1.0 / np.sqrt(values[positive])
    return (vectors * inverse) @ vectors.conj().T


def _inverse_permutation(permutation: Permutation) -> Permutation:
    inverse = [0] * len(permutation)
    for index, image in enumerate(permutation):
        inverse[image] = index
    return tuple(inverse)


def _kron_all(matrices: tuple[np.ndarray, ...]) -> np.ndarray:
    output = np.asarray([[1.0]], dtype=complex)
    for matrix in matrices:
        output = np.kron(output, matrix)
    return output


def local_polar_naimark_data(
    left_partition: Partition,
    right_partition: Partition,
    permutation: Permutation,
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return ``(V_plus,V_minus,F,F^-1/2,J)`` from equation (1)."""

    plus = local_character_cyclic_polar(
        left_partition,
        right_partition,
        permutation,
        1,
    )
    minus = local_character_cyclic_polar(
        left_partition,
        right_partition,
        permutation,
        -1,
    )
    plus_support = plus.conj().T @ plus
    minus_support = minus.conj().T @ minus
    frame = (plus_support + minus_support + (plus_support + minus_support).conj().T) / 2.0
    whitener = _psd_inverse_square_root(frame, tolerance)
    isometry = np.vstack((plus @ whitener, minus @ whitener))
    return plus, minus, frame, whitener, isometry


def tensor_polar_naimark_isometry(
    labels: tuple[Label, ...],
    permutation: Permutation,
) -> np.ndarray:
    if not labels:
        raise ValueError("at least one source pair is required")
    return _kron_all(
        tuple(
            local_polar_naimark_data(left, right, permutation)[-1]
            for left, right in labels
        )
    )


def audit_local_polar_naimark(
    control_id: str,
    left_partition: Partition,
    right_partition: Partition,
    permutation: Permutation,
    *,
    tolerance: float = 1e-9,
) -> LocalPolarNaimarkControl:
    plus, minus, frame, _whitener, isometry = local_polar_naimark_data(
        left_partition,
        right_partition,
        permutation,
        tolerance=tolerance,
    )
    dimension = plus.shape[0]
    identity = np.eye(dimension, dtype=complex)
    values = np.linalg.eigvalsh(frame).real
    integer_residual = float(
        max(min(abs(value - 1.0), abs(value - 2.0)) for value in values)
    )
    direct_frame = plus.conj().T @ plus + minus.conj().T @ minus
    frame_residual = float(np.linalg.norm(frame - direct_frame, ord=2))
    isometry_residual = float(
        np.linalg.norm(isometry.conj().T @ isometry - identity, ord=2)
    )
    verified = bool(
        values[0] >= 1.0 - 1000 * tolerance
        and values[-1] <= 2.0 + 1000 * tolerance
        and integer_residual <= 1000 * tolerance
        and frame_residual <= 1000 * tolerance
        and isometry_residual <= 1000 * tolerance
    )
    return LocalPolarNaimarkControl(
        control_id=control_id,
        n=len(permutation),
        left_partition=left_partition,
        right_partition=right_partition,
        permutation=permutation,
        carrier_dimension=dimension,
        plus_support_rank=int(round(float(np.trace(plus.conj().T @ plus).real))),
        minus_support_rank=int(round(float(np.trace(minus.conj().T @ minus).real))),
        support_frame_minimum_eigenvalue=float(values[0]),
        support_frame_maximum_eigenvalue=float(values[-1]),
        support_frame_condition_number=float(values[-1] / values[0]),
        support_frame_integer_spectrum_residual=integer_residual,
        naimark_isometry_residual=isometry_residual,
        direct_support_frame_residual=frame_residual,
        exact_local_polar_naimark_completion_verified=verified,
        status=(
            "exact-known-relative-local-polar-naimark-isometry"
            if verified
            else "local-polar-naimark-completion-failure"
        ),
    )


def audit_tensor_polar_naimark(
    control_id: str,
    labels: tuple[Label, ...],
    permutation: Permutation,
    *,
    tolerance: float = 1e-9,
) -> TensorPolarNaimarkControl:
    factors = tuple(
        local_polar_naimark_data(left, right, permutation)[-1]
        for left, right in labels
    )
    tensor = _kron_all(factors)
    direct = tensor_polar_naimark_isometry(labels, permutation)
    carrier_dimension = tensor.shape[1]
    factorization = float(np.linalg.norm(tensor - direct, ord=2))
    isometry = float(
        np.linalg.norm(
            tensor.conj().T @ tensor - np.eye(carrier_dimension),
            ord=2,
        )
    )
    verified = max(factorization, isometry) <= 2000 * tolerance
    return TensorPolarNaimarkControl(
        control_id=control_id,
        n=len(permutation),
        labels=labels,
        permutation=permutation,
        factor_count=len(labels),
        character_output_count=1 << len(labels),
        carrier_dimension=carrier_dimension,
        output_dimension=tensor.shape[0],
        tensor_isometry_residual=isometry,
        direct_tensor_factorization_residual=factorization,
        exact_tensor_polar_naimark_completion_verified=verified,
        status=(
            "exact-known-relative-tensor-polar-naimark-isometry"
            if verified
            else "tensor-polar-naimark-completion-failure"
        ),
    )


def candidate_relative_convolution(
    labels: tuple[Label, ...],
) -> tuple[np.ndarray, tuple[Permutation, ...], dict[Permutation, np.ndarray]]:
    """Materialize equation (2) for finite controls."""

    if not labels:
        raise ValueError("at least one source pair is required")
    group = tuple(_source_representation_rows(labels[0][0]))
    fields = {
        permutation: tensor_polar_naimark_isometry(labels, permutation)
        for permutation in group
    }
    output_block_dimension, input_block_dimension = next(iter(fields.values())).shape
    convolution = np.zeros(
        (
            len(group) * output_block_dimension,
            len(group) * input_block_dimension,
        ),
        dtype=complex,
    )
    for output_index, output_group in enumerate(group):
        for input_index, input_group in enumerate(group):
            relative = compose_permutations(
                _inverse_permutation(input_group),
                output_group,
            )
            output_slice = slice(
                output_index * output_block_dimension,
                (output_index + 1) * output_block_dimension,
            )
            input_slice = slice(
                input_index * input_block_dimension,
                (input_index + 1) * input_block_dimension,
            )
            convolution[output_slice, input_slice] = fields[relative] / math.sqrt(
                len(group)
            )
    return convolution, group, fields


def convolution_autocorrelation_gram(
    group: tuple[Permutation, ...],
    fields: dict[Permutation, np.ndarray],
) -> np.ndarray:
    """Return the block matrix on the right side of equation (3)."""

    input_dimension = next(iter(fields.values())).shape[1]
    output = np.zeros(
        (len(group) * input_dimension, len(group) * input_dimension),
        dtype=complex,
    )
    for left_index, left in enumerate(group):
        left_inverse = _inverse_permutation(left)
        for right_index, right in enumerate(group):
            right_inverse = _inverse_permutation(right)
            block = sum(
                (
                    fields[compose_permutations(left_inverse, value)].conj().T
                    @ fields[compose_permutations(right_inverse, value)]
                    for value in group
                ),
                np.zeros((input_dimension, input_dimension), dtype=complex),
            ) / len(group)
            row = slice(left_index * input_dimension, (left_index + 1) * input_dimension)
            column = slice(
                right_index * input_dimension,
                (right_index + 1) * input_dimension,
            )
            output[row, column] = block
    return output


def audit_candidate_relative_convolution(
    control_id: str,
    labels: tuple[Label, ...],
    *,
    constant_condition_threshold: float = 4.0,
    tolerance: float = 1e-9,
) -> CandidateRelativeConvolutionControl:
    convolution, group, fields = candidate_relative_convolution(labels)
    gram = convolution.conj().T @ convolution
    predicted = convolution_autocorrelation_gram(group, fields)
    residual = float(np.linalg.norm(gram - predicted, ord=2))
    singular_values = np.linalg.svd(convolution, compute_uv=False)
    positive = singular_values[singular_values > tolerance]
    if len(positive) != convolution.shape[1]:
        minimum = 0.0
        condition = math.inf
    else:
        minimum = float(positive[-1])
        condition = float(positive[0] / positive[-1])
    maximum = float(positive[0]) if len(positive) else 0.0
    identity = np.eye(convolution.shape[1], dtype=complex)
    isometry_residual = float(np.linalg.norm(gram - identity, ord=2))
    identity_group = tuple(range(len(group[0])))
    nonidentity = []
    input_dimension = next(iter(fields.values())).shape[1]
    for shift in group:
        if shift == identity_group:
            continue
        block = sum(
            (
                fields[value].conj().T
                @ fields[compose_permutations(shift, value)]
                for value in group
            ),
            np.zeros((input_dimension, input_dimension), dtype=complex),
        ) / len(group)
        nonidentity.append(float(np.linalg.norm(block, ord=2)))
    nonisometric = isometry_residual > 1000 * tolerance
    finite_constant = math.isfinite(condition) and condition <= constant_condition_threshold
    verified = bool(
        residual <= 5000 * tolerance
        and nonisometric
        and len(positive) == convolution.shape[1]
    )
    return CandidateRelativeConvolutionControl(
        control_id=control_id,
        n=sum(labels[0][0]),
        labels=labels,
        group_order=len(group),
        factor_count=len(labels),
        character_output_count=1 << len(labels),
        input_dimension=convolution.shape[1],
        output_dimension=convolution.shape[0],
        minimum_singular_value=minimum,
        maximum_singular_value=maximum,
        condition_number=condition,
        convolution_isometry_residual=isometry_residual,
        autocorrelation_gram_residual=residual,
        maximum_nonidentity_autocorrelation_norm=max(nonidentity, default=0.0),
        pointwise_isometries_do_not_imply_global_isometry=nonisometric,
        finite_constant_condition_observed=finite_constant,
        status=(
            "candidate-relative-autocorrelation-nontrivial-finite-gap-observed"
            if verified and finite_constant
            else "candidate-relative-autocorrelation-boundary"
            if verified
            else "candidate-relative-convolution-control-failure"
        ),
    )


def polar_naimark_scaling_record(n: int) -> PolarNaimarkScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2)) + 2
    return PolarNaimarkScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        character_output_qubit_count=copies,
        character_output_dimension_decimal=str(1 << copies),
        local_support_frame_condition_upper_bound=2.0,
        local_cyclic_compilers_required=copies,
        known_relative_tensor_naimark_polynomial=True,
        full_coefficient_rank_used=True,
        all_n_natural_autocorrelation_gap_proved=False,
        candidate_relative_convolution_compiled=False,
        hidden_relative_decoder_compiled=False,
        status="known-relative-dense-isometry-compiled-global-autocorrelation-open",
    )


def _threshold_labels() -> tuple[Label, ...]:
    return (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )


def run_branch_character_polar_naimark_completion(
) -> BranchCharacterPolarNaimarkReport:
    group = tuple(_source_representation_rows((3,)))
    pairs: tuple[Label, ...] = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    local = [
        audit_local_polar_naimark(
            f"S3-LOCAL-{pair_index}-{permutation_index}",
            left,
            right,
            permutation,
        )
        for pair_index, (left, right) in enumerate(pairs)
        for permutation_index, permutation in enumerate(group)
    ]
    local.append(
        audit_local_polar_naimark(
            "S4-MIXED-ONE-TWO-SUPPORT-FRAME",
            (3, 1),
            (4,),
            (0, 2, 3, 1),
        )
    )
    labels = _threshold_labels()
    tensor = [
        audit_tensor_polar_naimark(
            f"S3-THRESHOLD-TENSOR-{index}",
            labels,
            permutation,
        )
        for index, permutation in enumerate(group)
    ]
    convolutions = [
        audit_candidate_relative_convolution(
            "S3-SINGLE-PAIR-CANDIDATE-CONVOLUTION",
            (((3,), (2, 1)),),
        ),
        audit_candidate_relative_convolution(
            "S3-THRESHOLD-CANDIDATE-CONVOLUTION",
            labels,
        ),
    ]
    scaling = [
        polar_naimark_scaling_record(n)
        for n in (8, 16, 32, 64, 128, 256, 512)
    ]
    failures = sum(
        not row.exact_local_polar_naimark_completion_verified for row in local
    )
    failures += sum(
        not row.exact_tensor_polar_naimark_completion_verified for row in tensor
    )
    failures += sum(
        row.autocorrelation_gram_residual > 5e-8
        or not row.pointwise_isometries_do_not_imply_global_isometry
        for row in convolutions
    )
    verified = failures == 0
    theorem = PolarNaimarkTheorem(
        local_support_frame=(
            "P_++P_- has eigenvalue one on U phases +/-1 and eigenvalue two "
            "on every other phase."
        ),
        local_naimark_isometry=(
            "J_h=(|0>V_++|1>V_-)(P_++P_-)^-1/2 satisfies J_h^*J_h=I."
        ),
        cyclic_implementation=(
            "The existing cyclic phase register applies the extra weight one "
            "or 1/sqrt(2), so no inverse minimum singular value is used."
        ),
        tensor_completion=(
            "J_h^(k)=tensor_i J_(i,h) is a full-2^k-output isometry using k "
            "local known-relative compilers."
        ),
        candidate_convolution_gram=(
            "For C[g,s]=|G|^-1/2 J_(s^-1g), (C^*C)[s,t] is the exact "
            "operator-valued autocorrelation in equation (3)."
        ),
        scope=(
            "Known-relative dense Naimark access is solved. An all-n natural "
            "autocorrelation gap, a structured convolution circuit, unknown-relative "
            "covariance, and the physical PGM remain open."
        ),
        theorem_verified=verified,
        status=(
            "known-relative-character-polar-naimark-compiled-autocorrelation-open"
            if verified
            else "character-polar-naimark-control-failure"
        ),
    )
    return BranchCharacterPolarNaimarkReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        local_controls=local,
        tensor_controls=tensor,
        convolution_controls=convolutions,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "complete_both_local_character_polars_to_one_isometry",
                "resolved": verified,
                "resolution": (
                    "The support sum has exact spectrum in {1,2}; its inverse "
                    "square root is a constant cyclic phase function."
                ),
            },
            {
                "obligation": "respect_full_coefficient_rank_requirement",
                "resolved": verified,
                "resolution": (
                    "The tensor completion emits all 2^k characters and uses only "
                    "k local cyclic compilers."
                ),
            },
            {
                "obligation": "prove_natural_candidate_convolution_autocorrelation_gap",
                "resolved": False,
                "resolution": (
                    "The exact S3 threshold is constant-conditioned, but no source-"
                    "weighted all-n operator bound is proved."
                ),
            },
            {
                "obligation": "compile_candidate_relative_convolution_without_sqrt_group_normalization",
                "resolved": False,
                "resolution": (
                    "Efficient pointwise J_h does not itself erase the time label or "
                    "implement the dense group convolution at normalization one."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Branchwise polar support normalization may be exponentially ill-conditioned.",
                "resolved": verified,
                "resolution": "Its exact condition number is at most two for every finite-order U.",
            },
            {
                "objection": "Using all characters requires exponentially many separate branch circuits.",
                "resolved": verified,
                "resolution": "The complete isometry is a tensor product of k two-output local isometries.",
            },
            {
                "objection": "Pointwise isometries automatically assemble a global covariant isometry.",
                "resolved": True,
                "resolution": (
                    "False. Both exact S3 convolutions have nonzero off-diagonal "
                    "operator autocorrelation and fail the isometry identity."
                ),
            },
            {
                "objection": "Constant conditioning in the S3 threshold proves an all-n decoder.",
                "resolved": True,
                "resolution": "It is only a finite mechanism witness; natural asymptotics and access are open.",
            },
        ],
        headline_metrics={
            "exact_local_polar_naimark_theorem_count": int(verified),
            "exact_tensor_polar_naimark_theorem_count": int(verified),
            "finite_local_control_count": len(local),
            "finite_tensor_control_count": len(tensor),
            "finite_convolution_control_count": len(convolutions),
            "finite_control_failure_count": failures,
            "maximum_local_support_frame_condition_number": max(
                row.support_frame_condition_number for row in local
            ),
            "threshold_convolution_condition_number": convolutions[-1].condition_number,
            "threshold_maximum_nonidentity_autocorrelation_norm": (
                convolutions[-1].maximum_nonidentity_autocorrelation_norm
            ),
            "all_n_natural_autocorrelation_gap_theorem_count": 0,
            "candidate_relative_convolution_compiler_count": 0,
            "physical_pgm_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "known_relative_local_polar_naimark_isometry_compiled": verified,
            "known_relative_tensor_polar_naimark_isometry_compiled": verified,
            "full_coefficient_rank_used": verified,
            "inverse_minimum_singular_value_used": False,
            "pointwise_completion_implies_global_isometry": False,
            "finite_threshold_candidate_convolution_constant_condition_observed": (
                convolutions[-1].finite_constant_condition_observed
            ),
            "all_n_natural_autocorrelation_gap_proved": False,
            "normalization_one_candidate_convolution_compiled": False,
            "hidden_relative_covariance_solved": False,
            "physical_orientation_polar_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "Completed all known-relative cyclic character polars into one exact "
            "full-rank tensor Naimark isometry with local condition at most two. "
            "The remaining positive target is the natural operator-autocorrelation "
            "gap and a normalization-one structured group convolution."
        ),
        falsifiers_triggered=[
            "Local branch-polar completion does not require singular-value amplification.",
            "Exponential coefficient dimension does not force exponential local gate count.",
            "Pointwise isometry is insufficient for hidden-relative covariant assembly.",
            "Finite constant conditioning is not an asymptotic decoder theorem.",
        ],
    )


def write_branch_character_polar_naimark_completion_report(
    path: Path = REPORT_PATH,
    **_: Any,
) -> dict[str, Any]:
    payload = json.loads(
        json.dumps(asdict(run_branch_character_polar_naimark_completion()))
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_branch_character_polar_naimark_completion_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
