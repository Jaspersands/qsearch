"""Whole-quadrant path dilation and its exact erasure boundary.

The local cyclic compiler already combines the *complete* quadrant Fourier
sum when the relative element ``h`` is explicit.  Therefore the obvious
whole-sum construction is not a termwise power-map LCU.  It is the isometry

    D|s,psi> = |G|^-1/2 sum_h |h>|s h> J_h|psi>,          (1)

where every ``J_h`` is the completed branch-character isometry.  Uniform
group preparation, multiplication, and controlled cyclic phase estimation
compile (1) at normalization one.  The extra ``h`` register is the only
which-path information absent from the desired convolution

    C|s,psi> = |G|^-1/2 sum_h |s h> J_h|psi>.             (2)

Let ``P_+=<+|_h tensor I``.  Equations (1)-(2) give the exact block identity

    P_+ D = C/sqrt(|G|).                                  (3)

Consequently the principal amplitudes between ``Ran(D)`` and the uniform-path
subspace are ``sigma_j(C)/sqrt(|G|)``.  On any retained sector where the
singular values of ``C`` are order one, canonical alternating-reflection
unpreparation and QSVT on this block require ``Omega(sqrt(|G|))`` uses of the
dilation.  The all-order Frobenius contraction does not change this: better
conditioning of ``C`` makes the principal amplitudes uniformly close to
``1/sqrt(|G|)``, not close to one.

This is not a general circuit lower bound.  If the ranges ``J_h H`` are
orthogonal and there is an efficient coherent classifier

    W J_h|psi> = |h>|psi>,                                (4)

then (1) can be path-erased exactly: apply ``W``, subtract the decoded label
from the path register, and apply ``W^*``.  The result is ``|e>C|s,psi>``
with no amplification.  More generally, an approximate coherent classifier
is precisely the surviving structural escape suggested by the proved
multi-copy range-overlap contraction.

Thus a prepare-controlled-``J_h``-then-generic-unprepare architecture is
rejected.  A positive algorithm must compile a coherent range-label decoder,
an equivalent direct Fourier multiplier/polar, or another operation that uses
the carrier to remove which-path information.  Merely retaining all exponent
or irrep labels does not perform that operation.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable

import numpy as np

from research_registry import utc_now
from self_dual_wreath_branch_character_polar_naimark_completion import (
    Label,
    Permutation,
    candidate_relative_convolution,
)
from self_dual_wreath_character_moments import compose_permutations


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_branch_character_whole_sum_path_erasure_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-WHOLE-SUM-"
    "PATH-ERASURE-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class WholeSumPathControl:
    control_id: str
    group_order: int
    source_pair_count: int
    input_carrier_dimension: int
    field_output_dimension: int
    dilation_input_dimension: int
    dilation_output_dimension: int
    dilation_isometry_residual: float
    path_projection_block_residual: float
    convolution_minimum_singular_value: float
    convolution_maximum_singular_value: float
    projected_minimum_singular_value: float
    projected_maximum_singular_value: float
    singular_scale_identity_residual: float
    minimum_principal_amplitude: float
    maximum_principal_amplitude: float
    canonical_half_overlap_iteration_lower_bound: int
    exact_whole_sum_path_identity_verified: bool
    status: str


@dataclass(frozen=True)
class OrthogonalRangeClassifierControl:
    group_order: int
    input_carrier_dimension: int
    field_output_dimension: int
    maximum_cross_range_overlap: float
    classifier_unitarity_residual: float
    classifier_action_residual: float
    direct_convolution_isometry_residual: float
    generic_uniform_path_amplitude: float
    coherent_classifier_path_erasure_residual: float
    exact_classifier_bypass_verified: bool
    status: str


@dataclass(frozen=True)
class WholeSumPathScalingRecord:
    n: int
    log2_group_order: float
    natural_copy_count: int
    retained_convolution_singular_lower_bound: float
    retained_convolution_singular_upper_bound: float
    log2_uniform_path_amplitude_upper_bound: float
    log2_canonical_reflection_query_lower_bound: float
    polynomial_benchmark_log2: float
    generic_path_unpreparation_superpolynomial: bool
    coherent_range_classifier_compiled: bool
    status: str


@dataclass(frozen=True)
class WholeSumPathErasureTheorem:
    whole_sum_dilation: str
    exact_path_block: str
    principal_amplitudes: str
    canonical_reflection_boundary: str
    classifier_escape: str
    actual_wreath_obligation: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class WholeSumPathErasureBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: WholeSumPathErasureTheorem
    finite_controls: list[WholeSumPathControl]
    classifier_control: OrthogonalRangeClassifierControl
    scaling_records: list[WholeSumPathScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _group_multiplication_table(
    group: tuple[Permutation, ...],
) -> np.ndarray:
    index = {element: position for position, element in enumerate(group)}
    return np.asarray(
        [
            [index[compose_permutations(left, right)] for right in group]
            for left in group
        ],
        dtype=int,
    )


def whole_sum_path_dilation(
    group: tuple[Permutation, ...],
    fields: dict[Permutation, np.ndarray],
) -> np.ndarray:
    """Materialize equation (1) for a finite control."""

    if not group or set(group) != set(fields):
        raise ValueError("fields must contain exactly one isometry per group element")
    output_dimension, input_dimension = next(iter(fields.values())).shape
    if any(field.shape != (output_dimension, input_dimension) for field in fields.values()):
        raise ValueError("all fields must have the same shape")
    identity = np.eye(input_dimension, dtype=complex)
    if any(
        np.linalg.norm(field.conj().T @ field - identity, ord=2) > 1e-7
        for field in fields.values()
    ):
        raise ValueError("every field must be an isometry")
    order = len(group)
    table = _group_multiplication_table(group)
    dilation = np.zeros(
        (order * order * output_dimension, order * input_dimension),
        dtype=complex,
    )
    for source in range(order):
        input_block = slice(source * input_dimension, (source + 1) * input_dimension)
        for path, element in enumerate(group):
            target = int(table[source, path])
            row_start = (path * order + target) * output_dimension
            row_block = slice(row_start, row_start + output_dimension)
            dilation[row_block, input_block] = fields[element] / math.sqrt(order)
    return dilation


def uniform_path_coisometry(group_order: int, output_dimension: int) -> np.ndarray:
    if group_order < 1 or output_dimension < 1:
        raise ValueError("dimensions must be positive")
    return np.hstack(
        tuple(
            np.eye(group_order * output_dimension, dtype=complex)
            / math.sqrt(group_order)
            for _ in range(group_order)
        )
    )


def _half_overlap_iteration_lower_bound(amplitude: float) -> int:
    """Queries needed by alternating reflections to reach amplitude 1/2."""

    if not 0 < amplitude <= 1:
        return 0
    theta = math.asin(amplitude)
    target = math.asin(0.5)
    if theta >= target:
        return 0
    return max(0, math.ceil((target / theta - 1.0) / 2.0))


def audit_whole_sum_path_identity(
    control_id: str,
    labels: tuple[Label, ...],
    *,
    tolerance: float = 1e-9,
) -> WholeSumPathControl:
    convolution, group, fields = candidate_relative_convolution(labels)
    dilation = whole_sum_path_dilation(group, fields)
    output_dimension, input_dimension = next(iter(fields.values())).shape
    path = uniform_path_coisometry(len(group), output_dimension)
    projected = path @ dilation
    predicted = convolution / math.sqrt(len(group))
    dilation_residual = float(
        np.linalg.norm(
            dilation.conj().T @ dilation
            - np.eye(dilation.shape[1], dtype=complex),
            ord=2,
        )
    )
    block_residual = float(np.linalg.norm(projected - predicted, ord=2))
    convolution_singular = np.linalg.svd(convolution, compute_uv=False)
    projected_singular = np.linalg.svd(projected, compute_uv=False)
    expected_projected = convolution_singular / math.sqrt(len(group))
    scale_residual = float(np.max(np.abs(projected_singular - expected_projected)))
    minimum = float(convolution_singular[-1])
    maximum = float(convolution_singular[0])
    projected_minimum = float(projected_singular[-1])
    projected_maximum = float(projected_singular[0])
    verified = bool(
        dilation_residual <= 1000 * tolerance
        and block_residual <= 1000 * tolerance
        and scale_residual <= 1000 * tolerance
    )
    return WholeSumPathControl(
        control_id=control_id,
        group_order=len(group),
        source_pair_count=len(labels),
        input_carrier_dimension=input_dimension,
        field_output_dimension=output_dimension,
        dilation_input_dimension=dilation.shape[1],
        dilation_output_dimension=dilation.shape[0],
        dilation_isometry_residual=dilation_residual,
        path_projection_block_residual=block_residual,
        convolution_minimum_singular_value=minimum,
        convolution_maximum_singular_value=maximum,
        projected_minimum_singular_value=projected_minimum,
        projected_maximum_singular_value=projected_maximum,
        singular_scale_identity_residual=scale_residual,
        minimum_principal_amplitude=projected_minimum,
        maximum_principal_amplitude=projected_maximum,
        canonical_half_overlap_iteration_lower_bound=(
            _half_overlap_iteration_lower_bound(projected_minimum)
        ),
        exact_whole_sum_path_identity_verified=verified,
        status=(
            "whole-sum-dilation-exact-generic-path-erasure-subnormalized"
            if verified
            else "whole-sum-path-control-failure"
        ),
    )


def _cyclic_group(order: int) -> tuple[Permutation, ...]:
    """Represent C_order by its regular shifts as permutations."""

    return tuple(
        tuple((value + shift) % order for value in range(order))
        for shift in range(order)
    )


def audit_orthogonal_range_classifier(
    group_order: int = 4,
    input_dimension: int = 2,
    *,
    tolerance: float = 1e-10,
) -> OrthogonalRangeClassifierControl:
    """Verify the exact carrier-assisted bypass in equation (4)."""

    if group_order < 2 or input_dimension < 1:
        raise ValueError("invalid classifier dimensions")
    group = _cyclic_group(group_order)
    field_dimension = group_order * input_dimension
    fields: dict[Permutation, np.ndarray] = {}
    classifier = np.zeros((field_dimension, field_dimension), dtype=complex)
    for label, element in enumerate(group):
        phase = np.exp(
            2j
            * math.pi
            * label
            * np.arange(input_dimension)
            / max(group_order, input_dimension)
        )
        unitary = np.diag(phase)
        field = np.zeros((field_dimension, input_dimension), dtype=complex)
        block = slice(label * input_dimension, (label + 1) * input_dimension)
        field[block, :] = unitary
        fields[element] = field
        classifier[block, block] = unitary.conj().T

    maximum_cross = max(
        float(np.linalg.norm(fields[left].conj().T @ fields[right], ord=2))
        for left in group
        for right in group
        if left != right
    )
    classifier_unitarity = float(
        np.linalg.norm(classifier.conj().T @ classifier - np.eye(field_dimension), ord=2)
    )
    classifier_action = max(
        float(
            np.linalg.norm(
                classifier @ fields[element]
                - np.vstack(
                    (
                        np.zeros((label * input_dimension, input_dimension)),
                        np.eye(input_dimension),
                        np.zeros(
                            (
                                field_dimension - (label + 1) * input_dimension,
                                input_dimension,
                            )
                        ),
                    )
                ),
                ord=2,
            )
        )
        for label, element in enumerate(group)
    )

    dilation = whole_sum_path_dilation(group, fields)
    order = group_order
    # Layout is path, target, decoded-label, carrier after the classifier.
    first = np.kron(np.eye(order * order), classifier)
    subtract = np.zeros_like(first)
    for path in range(order):
        for target in range(order):
            for decoded in range(order):
                for carrier in range(input_dimension):
                    source = (((path * order + target) * order + decoded) * input_dimension + carrier)
                    erased = (path - decoded) % order
                    destination = (((erased * order + target) * order + decoded) * input_dimension + carrier)
                    subtract[destination, source] = 1.0
    last = np.kron(np.eye(order * order), classifier.conj().T)
    erased = last @ subtract @ first @ dilation

    convolution = np.zeros(
        (order * field_dimension, order * input_dimension),
        dtype=complex,
    )
    table = _group_multiplication_table(group)
    for source in range(order):
        source_block = slice(source * input_dimension, (source + 1) * input_dimension)
        for path, element in enumerate(group):
            target = int(table[source, path])
            target_block = slice(target * field_dimension, (target + 1) * field_dimension)
            convolution[target_block, source_block] = fields[element] / math.sqrt(order)
    expected = np.zeros_like(erased)
    expected[: order * field_dimension, :] = convolution
    erasure_residual = float(np.linalg.norm(erased - expected, ord=2))
    convolution_isometry = float(
        np.linalg.norm(
            convolution.conj().T @ convolution
            - np.eye(order * input_dimension),
            ord=2,
        )
    )
    verified = bool(
        maximum_cross <= 100 * tolerance
        and classifier_unitarity <= 100 * tolerance
        and classifier_action <= 100 * tolerance
        and convolution_isometry <= 100 * tolerance
        and erasure_residual <= 1000 * tolerance
    )
    return OrthogonalRangeClassifierControl(
        group_order=order,
        input_carrier_dimension=input_dimension,
        field_output_dimension=field_dimension,
        maximum_cross_range_overlap=maximum_cross,
        classifier_unitarity_residual=classifier_unitarity,
        classifier_action_residual=classifier_action,
        direct_convolution_isometry_residual=convolution_isometry,
        generic_uniform_path_amplitude=1.0 / math.sqrt(order),
        coherent_classifier_path_erasure_residual=erasure_residual,
        exact_classifier_bypass_verified=verified,
        status=(
            "coherent-range-classifier-bypasses-generic-path-projection"
            if verified
            else "orthogonal-range-classifier-control-failure"
        ),
    )


def whole_sum_path_scaling_record(
    n: int,
    *,
    retained_singular_lower: float = 0.5,
    retained_singular_upper: float = 1.5,
    polynomial_benchmark_degree: int = 20,
) -> WholeSumPathScalingRecord:
    if n < 2 or not 0 < retained_singular_lower <= retained_singular_upper:
        raise ValueError("invalid scaling parameters")
    log_order = math.log2(math.factorial(n))
    copies = math.ceil(3.0 * log_order) + 2
    log_amplitude = math.log2(retained_singular_upper) - 0.5 * log_order
    log_queries = 0.5 * log_order - math.log2(retained_singular_upper)
    benchmark = polynomial_benchmark_degree * math.log2(n)
    rejected = log_queries > benchmark
    return WholeSumPathScalingRecord(
        n=n,
        log2_group_order=log_order,
        natural_copy_count=copies,
        retained_convolution_singular_lower_bound=retained_singular_lower,
        retained_convolution_singular_upper_bound=retained_singular_upper,
        log2_uniform_path_amplitude_upper_bound=log_amplitude,
        log2_canonical_reflection_query_lower_bound=log_queries,
        polynomial_benchmark_log2=benchmark,
        generic_path_unpreparation_superpolynomial=rejected,
        coherent_range_classifier_compiled=False,
        status=(
            "canonical-whole-sum-path-unpreparation-superpolynomial"
            if rejected
            else "finite-path-erasure-separation-not-yet-visible"
        ),
    )


def run_whole_sum_path_erasure_boundary() -> WholeSumPathErasureBoundaryReport:
    controls = [
        audit_whole_sum_path_identity(
            "S3-SINGLE-PAIR-WHOLE-SUM-PATH",
            (((3,), (2, 1)),),
        ),
        audit_whole_sum_path_identity(
            "S3-THRESHOLD-WHOLE-SUM-PATH",
            (
                ((3,), (2, 1)),
                ((3,), (1, 1, 1)),
                ((2, 1), (1, 1, 1)),
            ),
        ),
    ]
    classifier = audit_orthogonal_range_classifier()
    scaling = [whole_sum_path_scaling_record(n) for n in (8, 16, 32, 64, 128)]
    verified = bool(
        all(row.exact_whole_sum_path_identity_verified for row in controls)
        and classifier.exact_classifier_bypass_verified
        and scaling[-1].generic_path_unpreparation_superpolynomial
    )
    theorem = WholeSumPathErasureTheorem(
        whole_sum_dilation=(
            "Uniform h preparation, multiplication, and controlled complete cyclic "
            "phase compilation implement D at normalization one."
        ),
        exact_path_block=(
            "Uniform projection of the which-h path gives exactly C/sqrt(|G|)."
        ),
        principal_amplitudes=(
            "The restricted principal amplitudes are sigma_j(C)/sqrt(|G|)."
        ),
        canonical_reflection_boundary=(
            "On an order-one singular window, alternating-reflection or generic "
            "QSVT path unpreparation needs Omega(sqrt(|G|)) dilation uses."
        ),
        classifier_escape=(
            "A coherent W with W J_h|psi>=|h>|psi> erases the path exactly by "
            "decode, subtract, and re-encode."
        ),
        actual_wreath_obligation=(
            "Compile an approximate coherent classifier for the natural overlapping "
            "ranges, or an equivalent direct multiplier/polar transform."
        ),
        scope=(
            "This rejects canonical path projection/reflection schemes, not arbitrary "
            "carrier-aware circuits or direct representation-specific compilers."
        ),
        theorem_verified=verified,
        status=(
            "whole-sum-path-dilation-compiled-generic-erasure-rejected-classifier-open"
            if verified
            else "whole-sum-path-erasure-boundary-control-failure"
        ),
    )
    tail = scaling[-1]
    return WholeSumPathErasureBoundaryReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        classifier_control=classifier,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "compile_complete_quadrant_sum_with_explicit_relative_path",
                "resolved": verified,
                "resolution": (
                    "The existing controlled cyclic compiler supplies every J_h; "
                    "uniform h preparation and group multiplication give D."
                ),
            },
            {
                "obligation": "test_generic_uniform_path_unpreparation",
                "resolved": verified,
                "resolution": (
                    "Rejected: its exact singular amplitudes are sigma(C)/sqrt(|G|), "
                    "so the natural order-one sector still has sqrt(|G|) query cost."
                ),
            },
            {
                "obligation": "compile_coherent_natural_range_classifier",
                "resolved": False,
                "resolution": (
                    "The orthogonal control proves sufficiency, but the actual J_h "
                    "ranges overlap and no efficient representation-specific classifier is known."
                ),
            },
            {
                "obligation": "compile_physical_decoder_and_prove_classical_separation",
                "resolved": False,
                "resolution": "No end-to-end hidden-label algorithm or speedup is established.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Summing all quadrant coefficients before projection removes the group normalization.",
                "resolved": True,
                "resolution": "False for the canonical dilation: the exact uniform-path block remains C/sqrt(|G|).",
            },
            {
                "objection": "Near-isometry of C makes path projection high amplitude.",
                "resolved": True,
                "resolution": "False. It makes every relevant principal amplitude approximately 1/sqrt(|G|).",
            },
            {
                "objection": "The sqrt(|G|) boundary is an arbitrary-circuit lower bound.",
                "resolved": True,
                "resolution": "False. The exact orthogonal-range classifier control erases the path deterministically.",
            },
        ],
        headline_metrics={
            "whole_sum_path_dilation_theorem_count": int(verified),
            "canonical_path_erasure_no_go_count": int(verified),
            "coherent_classifier_escape_theorem_count": int(verified),
            "finite_wreath_control_count": len(controls),
            "finite_control_failure_count": sum(
                not row.exact_whole_sum_path_identity_verified for row in controls
            ),
            "tail_n": tail.n,
            "tail_copy_count": tail.natural_copy_count,
            "tail_log2_canonical_query_lower_bound": tail.log2_canonical_reflection_query_lower_bound,
            "natural_range_classifier_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "complete_quadrant_sum_explicit_path_dilation_compiled": verified,
            "uniform_path_block_identity_proved": verified,
            "generic_reflection_path_unpreparation_superpolynomial": verified,
            "arbitrary_whole_sum_circuit_lower_bound_proved": False,
            "coherent_range_classifier_is_sufficient": verified,
            "natural_wreath_range_classifier_compiled": False,
            "direct_equivariant_multiplier_compiled": False,
            "physical_decoder_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "Compiled the complete quadrant field into an explicit which-h path "
            "dilation, proved that canonical path removal retains the exact "
            "sqrt(|G|) normalization barrier, and isolated a coherent range "
            "classifier as the carrier-aware escape. No such natural classifier is compiled."
        ),
        falsifiers_triggered=[
            "Whole-sum coefficient preparation does not by itself erase the relative-element path.",
            "State-weighted near-isometry of C does not improve the canonical path projection amplitude.",
            "A coherent carrier range classifier would bypass the generic barrier, so no universal circuit no-go is claimed.",
        ],
    )


def write_whole_sum_path_erasure_boundary_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_whole_sum_path_erasure_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


if __name__ == "__main__":
    report = write_whole_sum_path_erasure_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
