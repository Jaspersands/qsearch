"""Matrix-POVM normal form for recursive partial-support compilation.

Scalar affine fibers are not necessary for an exact recursive compiler.  Let
``W:K -> direct_sum_e C_e`` be any normalized child embedding and write its
components as ``W_e``.  Their effects

    H_e = W_e^* W_e,             sum_e H_e = I_K,          (1)

form a POVM.  Polar decomposition gives

    W_e = V_e sqrt(H_e),                                  (2)

where ``V_e`` is a partial isometry from ``supp(H_e)`` into the mask-``e``
coefficient block.  Therefore ``W`` is exactly a coherent Naimark dilation

    |psi> -> sum_e |e> sqrt(H_e)|psi>                     (3)

followed by controlled support transports ``V_e``.  No square-root outcome-
count amplification is intrinsic to (3).

The recursive parent relation has one more two-outcome POVM.  With short
metrics ``A_L,A_R``, ``M=A_L+A_R``, and

    C_s=A_s^(1/2)M^(-1/2),       C_L^*C_L+C_R^*C_R=I,      (4)

first apply the endpoint dilation ``|L>C_L-|R>C_R``; then apply the child
POVM dilation (3) on the selected side; finally apply ``V_(s,e)``.  This
factorizes arbitrary noncommuting component effects and matrix endpoint
mixers exactly.

The theorem relocates, rather than solves, the circuit problem.  Pair GPE can
implement a compatible support partial isometry ``V_e``.  It does not prepare
the square-root POVM amplitudes.  In a generic bounded-polynomial block-
encoding model, approximating ``sqrt(x)`` down to a nonzero effect eigenvalue
``delta`` has degree at least ``Omega(delta^(-1/4))`` by the mean-value theorem
and Markov's inequality.  Thus exponentially small positive effect
eigenvalues remain an access obstruction unless representation structure supplies the dilation
directly.  However, small trace or outcome probability does not establish a
small positive ``delta``.  The companion sparse-support Jacobi boundary shows
that a rare coordinate outcome can instead have exponentially small rank and
a constant nonzero edge.  In that regime support-projector SELECT, not square-
root approximation, is the unresolved operation.  No arbitrary-circuit lower
bound or natural small-edge theorem is claimed.
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
    "self_dual_wreath_matrix_povm_recursive_compiler.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-MATRIX-POVM-RECURSIVE-COMPILER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class MatrixPovmControl:
    control_id: str
    fiber_dimension: int
    outcome_count: int
    output_coefficient_dimension: int
    minimum_positive_effect_eigenvalue: float
    maximum_effect_eigenvalue: float
    maximum_effect_commutator_norm: float
    effect_sum_identity_residual: float
    stacked_embedding_isometry_residual: float
    maximum_component_polar_reconstruction_residual: float
    maximum_partial_isometry_initial_projection_residual: float
    exact_matrix_povm_normal_form_verified: bool
    component_effects_commute: bool
    status: str


@dataclass(frozen=True)
class RecursiveMatrixPovmControl:
    control_id: str
    fiber_dimension: int
    left_outcome_count: int
    right_outcome_count: int
    endpoint_effect_sum_residual: float
    left_child_effect_sum_residual: float
    right_child_effect_sum_residual: float
    maximum_child_effect_commutator_norm: float
    endpoint_effect_commutator_norm: float
    direct_recursive_relation_isometry_residual: float
    nested_povm_factorization_residual: float
    exact_nested_matrix_povm_compiler_normal_form_verified: bool
    status: str


@dataclass(frozen=True)
class SquareRootPovmDegreeBoundary:
    input_size: int
    minimum_nonzero_effect_eigenvalue_log2: float
    relative_approximation_error: float
    markov_degree_lower_bound: float
    markov_degree_lower_bound_log2: float
    polynomial_degree_benchmark_log2: float
    generic_block_encoding_degree_superpolynomial_signal: bool
    representation_specific_direct_dilation_proved: bool
    status: str


@dataclass(frozen=True)
class MatrixPovmRecursiveCompilerReport:
    created_at: str
    theorem_contract: dict[str, Any]
    povm_controls: list[MatrixPovmControl]
    recursive_control: RecursiveMatrixPovmControl
    degree_boundary: list[SquareRootPovmDegreeBoundary]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _psd_power(
    matrix: np.ndarray,
    exponent: float,
    *,
    tolerance: float,
) -> np.ndarray:
    hermitian = (matrix + matrix.conj().T) / 2
    values, vectors = np.linalg.eigh(hermitian)
    if len(values) and values[0] < -100 * tolerance:
        raise ArithmeticError("matrix is not positive semidefinite")
    powered = np.zeros_like(values)
    positive = values > 100 * tolerance
    powered[positive] = values[positive] ** exponent
    return (vectors * powered) @ vectors.conj().T


def _component_polar(
    component: np.ndarray,
    *,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    effect = component.conj().T @ component
    root = _psd_power(effect, 0.5, tolerance=tolerance)
    inverse_root = _psd_power(effect, -0.5, tolerance=tolerance)
    partial = component @ inverse_root
    values, vectors = np.linalg.eigh((effect + effect.conj().T) / 2)
    positive = values > 100 * tolerance
    support = vectors[:, positive] @ vectors[:, positive].conj().T
    return effect, root, partial @ support


def audit_matrix_povm_normal_form(
    control_id: str,
    components: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> MatrixPovmControl:
    if not components:
        raise ValueError("at least one POVM component is required")
    fiber = components[0].shape[1]
    if any(component.shape[1] != fiber for component in components):
        raise ValueError("all components must share a source fiber")
    identity = np.eye(fiber, dtype=complex)
    effects = []
    positive_values = []
    maximum = 0.0
    reconstruction = 0.0
    initial_projection = 0.0
    for component in components:
        effect, root, partial = _component_polar(
            component,
            tolerance=tolerance,
        )
        effects.append(effect)
        values, vectors = np.linalg.eigh((effect + effect.conj().T) / 2)
        positive = values > 100 * tolerance
        positive_values.extend(float(value) for value in values[positive])
        maximum = max(maximum, float(values.max()))
        support = vectors[:, positive] @ vectors[:, positive].conj().T
        reconstruction = max(
            reconstruction,
            float(np.linalg.norm(component - partial @ root, ord=2)),
        )
        initial_projection = max(
            initial_projection,
            float(np.linalg.norm(partial.conj().T @ partial - support, ord=2)),
        )
    effect_sum = sum(effects, np.zeros_like(identity))
    stacked = np.vstack(components)
    sum_residual = float(np.linalg.norm(effect_sum - identity, ord=2))
    isometry = float(
        np.linalg.norm(stacked.conj().T @ stacked - identity, ord=2)
    )
    commutator = max(
        (
            float(np.linalg.norm(left @ right - right @ left, ord=2))
            for index, left in enumerate(effects)
            for right in effects[index + 1 :]
        ),
        default=0.0,
    )
    verified = max(
        sum_residual,
        isometry,
        reconstruction,
        initial_projection,
    ) <= 1000 * tolerance
    return MatrixPovmControl(
        control_id=control_id,
        fiber_dimension=fiber,
        outcome_count=len(components),
        output_coefficient_dimension=sum(component.shape[0] for component in components),
        minimum_positive_effect_eigenvalue=min(positive_values, default=0.0),
        maximum_effect_eigenvalue=maximum,
        maximum_effect_commutator_norm=commutator,
        effect_sum_identity_residual=sum_residual,
        stacked_embedding_isometry_residual=isometry,
        maximum_component_polar_reconstruction_residual=reconstruction,
        maximum_partial_isometry_initial_projection_residual=initial_projection,
        exact_matrix_povm_normal_form_verified=verified,
        component_effects_commute=commutator <= 1000 * tolerance,
        status=(
            "exact-commuting-matrix-povm-normal-form"
            if verified and commutator <= 1000 * tolerance
            else "exact-noncommuting-matrix-povm-normal-form"
            if verified
            else "matrix-povm-normal-form-failure"
        ),
    )


def _projective_components() -> tuple[np.ndarray, ...]:
    return (
        np.diag([1.0, 0.0]).astype(complex),
        np.diag([0.0, 1.0]).astype(complex),
    )


def _trine_components() -> tuple[np.ndarray, ...]:
    components = []
    for index in range(3):
        angle = 2 * math.pi * index / 3
        vector = np.asarray([[math.cos(angle)], [math.sin(angle)]], dtype=complex)
        effect = (2 / 3) * (vector @ vector.conj().T)
        components.append(_psd_power(effect, 0.5, tolerance=1e-12))
    return tuple(components)


def audit_recursive_matrix_povm_normal_form(
    control_id: str,
    left_components: tuple[np.ndarray, ...],
    right_components: tuple[np.ndarray, ...],
    left_metric: np.ndarray,
    right_metric: np.ndarray,
    *,
    tolerance: float = 1e-9,
) -> RecursiveMatrixPovmControl:
    fiber = left_metric.shape[0]
    if left_metric.shape != (fiber, fiber) or right_metric.shape != (fiber, fiber):
        raise ValueError("short metrics must share one square fiber")
    if any(component.shape[1] != fiber for component in (*left_components, *right_components)):
        raise ValueError("child components and short metrics must share a fiber")
    identity = np.eye(fiber, dtype=complex)
    metric = left_metric + right_metric
    metric_inverse_root = _psd_power(metric, -0.5, tolerance=tolerance)
    left_mixer = _psd_power(left_metric, 0.5, tolerance=tolerance) @ metric_inverse_root
    right_mixer = _psd_power(right_metric, 0.5, tolerance=tolerance) @ metric_inverse_root
    left_endpoint_effect = left_mixer.conj().T @ left_mixer
    right_endpoint_effect = right_mixer.conj().T @ right_mixer

    left_effects = tuple(component.conj().T @ component for component in left_components)
    right_effects = tuple(component.conj().T @ component for component in right_components)
    left_sum = sum(left_effects, np.zeros_like(identity))
    right_sum = sum(right_effects, np.zeros_like(identity))
    direct_blocks = tuple(
        [component @ left_mixer for component in left_components]
        + [-component @ right_mixer for component in right_components]
    )
    direct = np.vstack(direct_blocks)
    nested_blocks = []
    for sign, components, mixer in (
        (1.0, left_components, left_mixer),
        (-1.0, right_components, right_mixer),
    ):
        for component in components:
            _, root, partial = _component_polar(component, tolerance=tolerance)
            nested_blocks.append(sign * partial @ root @ mixer)
    nested = np.vstack(nested_blocks)
    child_commutator = max(
        audit_matrix_povm_normal_form("left", left_components).maximum_effect_commutator_norm,
        audit_matrix_povm_normal_form("right", right_components).maximum_effect_commutator_norm,
    )
    endpoint_sum = float(
        np.linalg.norm(left_endpoint_effect + right_endpoint_effect - identity, ord=2)
    )
    relation_isometry = float(
        np.linalg.norm(direct.conj().T @ direct - identity, ord=2)
    )
    factorization = float(np.linalg.norm(direct - nested, ord=2))
    verified = max(
        endpoint_sum,
        float(np.linalg.norm(left_sum - identity, ord=2)),
        float(np.linalg.norm(right_sum - identity, ord=2)),
        relation_isometry,
        factorization,
    ) <= 1000 * tolerance
    return RecursiveMatrixPovmControl(
        control_id=control_id,
        fiber_dimension=fiber,
        left_outcome_count=len(left_components),
        right_outcome_count=len(right_components),
        endpoint_effect_sum_residual=endpoint_sum,
        left_child_effect_sum_residual=float(np.linalg.norm(left_sum - identity, ord=2)),
        right_child_effect_sum_residual=float(np.linalg.norm(right_sum - identity, ord=2)),
        maximum_child_effect_commutator_norm=child_commutator,
        endpoint_effect_commutator_norm=float(
            np.linalg.norm(
                left_endpoint_effect @ right_endpoint_effect
                - right_endpoint_effect @ left_endpoint_effect,
                ord=2,
            )
        ),
        direct_recursive_relation_isometry_residual=relation_isometry,
        nested_povm_factorization_residual=factorization,
        exact_nested_matrix_povm_compiler_normal_form_verified=verified,
        status=(
            "exact-nested-endpoint-and-child-matrix-povm-normal-form"
            if verified
            else "recursive-matrix-povm-normal-form-failure"
        ),
    )


def square_root_povm_degree_boundary(
    input_size: int,
    *,
    relative_error: float = 1 / 8,
) -> SquareRootPovmDegreeBoundary:
    if input_size < 1 or not 0 < relative_error < 0.5:
        raise ValueError("invalid degree-boundary parameters")
    delta_log2 = -float(input_size)
    # If |p-sqrt(.)| <= eta sqrt(delta) at 0 and delta, the mean-value
    # derivative is at least (1-2 eta)/sqrt(delta). Markov on [0,1] gives
    # ||p'|| <= 2 d^2 ||p||, with ||p|| <= 1+eta.
    constant = math.sqrt(
        (1 - 2 * relative_error) / (2 * (1 + relative_error))
    )
    degree_log2 = math.log2(constant) + input_size / 4
    degree = 2**degree_log2 if degree_log2 < 1024 else math.inf
    benchmark = 12 * math.log2(max(2, input_size))
    return SquareRootPovmDegreeBoundary(
        input_size=input_size,
        minimum_nonzero_effect_eigenvalue_log2=delta_log2,
        relative_approximation_error=relative_error,
        markov_degree_lower_bound=degree,
        markov_degree_lower_bound_log2=degree_log2,
        polynomial_degree_benchmark_log2=benchmark,
        generic_block_encoding_degree_superpolynomial_signal=degree_log2 > benchmark,
        representation_specific_direct_dilation_proved=False,
        status=(
            "generic-square-root-block-encoding-superpolynomial-signal"
            if degree_log2 > benchmark
            else "finite-square-root-degree-below-n12-benchmark"
        ),
    )


def run_matrix_povm_recursive_compiler() -> MatrixPovmRecursiveCompilerReport:
    controls = [
        audit_matrix_povm_normal_form(
            "TWO-OUTCOME-PROJECTIVE-PARTIAL-SUPPORT",
            _projective_components(),
        ),
        audit_matrix_povm_normal_form(
            "THREE-OUTCOME-NONCOMMUTING-TRINE",
            _trine_components(),
        ),
    ]
    angle = 0.41
    rotation = np.asarray(
        [
            [math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)],
        ],
        dtype=complex,
    )
    recursive = audit_recursive_matrix_povm_normal_form(
        "NONCOMMUTING-CHILD-POVM-AND-MATRIX-ENDPOINT-MIXER",
        _trine_components(),
        _projective_components(),
        np.diag([1.0, 4.0]).astype(complex),
        rotation @ np.diag([3.0, 1.5]) @ rotation.conj().T,
    )
    degree = [
        square_root_povm_degree_boundary(size)
        for size in (16, 32, 64, 128, 256, 512)
    ]
    failures = sum(not row.exact_matrix_povm_normal_form_verified for row in controls)
    exact = failures == 0 and recursive.exact_nested_matrix_povm_compiler_normal_form_verified
    noncommuting = any(not row.component_effects_commute for row in controls)
    tail = degree[-1]
    return MatrixPovmRecursiveCompilerReport(
        created_at=utc_now(),
        theorem_contract={
            "child_nondegenerate_normal_form": (
                "Every isometric child embedding W has component POVM effects "
                "H_e=W_e^*W_e and exact factorization W_e=V_e sqrt(H_e)."
            ),
            "recursive_nested_dilation": (
                "The parent relation is endpoint POVM dilation C_L,C_R followed "
                "by the selected child component POVM dilation and controlled "
                "support partial isometries."
            ),
            "width_boundary": (
                "The exact Naimark isometry has no intrinsic sqrt(outcome-count) "
                "loss; any such loss belongs to the chosen access implementation."
            ),
            "generic_degree_boundary": (
                "Bounded-polynomial square-root approximation down to delta has "
                "degree Omega(delta^-1/4) by mean value plus Markov inequality; "
                "trace weight alone does not imply such a delta."
            ),
            "scope": (
                "This is a compiler normal form and generic block-encoding "
                "boundary. It does not construct the natural component-POVM "
                "dilation, prove GPE compatibility of every support polar, or "
                "bound high-dimensional-source native mass."
            ),
        },
        povm_controls=controls,
        recursive_control=recursive,
        degree_boundary=degree,
        proof_obligations=[
            {
                "obligation": "exact_matrix_component_povm_normal_form",
                "resolved": exact,
                "resolution": "Polar decomposition proves it for arbitrary components; projective and noncommuting trine controls validate the identities.",
            },
            {
                "obligation": "exact_nested_recursive_povm_factorization",
                "resolved": recursive.exact_nested_matrix_povm_compiler_normal_form_verified,
                "resolution": "Endpoint and child POVM isometries compose exactly even when child effects and short metrics are matrix valued.",
            },
            {
                "obligation": "compile_natural_component_povm_square_root_dilation",
                "resolved": False,
                "resolution": "Need a representation-specific coherent effect algebra or direct Naimark transform; generic QSVT can be superpolynomial at an exponentially small effect edge.",
            },
            {
                "obligation": "prove_component_support_polars_are_uniform_gpe_transports",
                "resolved": False,
                "resolution": "Pair GPE implements compatible invariant support polars, but no all-depth channel classification covers every W_e support.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Nonscalar or noncommuting component effects prevent an exact recursive normal form.",
                "resolved": True,
                "resolution": "False: they define a POVM, and its Naimark dilation followed by component polars is exact without commutativity.",
            },
            {
                "objection": "A matrix POVM necessarily costs square root of the number of masks.",
                "resolved": True,
                "resolution": "The target map is already an isometry because the effects sum to identity. Width loss is an access-construction defect, not an algebraic necessity.",
            },
            {
                "objection": "The exact Naimark normal form supplies a polynomial circuit.",
                "resolved": True,
                "resolution": "False in generic block-encoding access: exponentially small effect eigenvalues force a superpolynomial square-root polynomial degree signal.",
            },
            {
                "objection": "An exponentially small component trace activates the generic square-root degree obstruction.",
                "resolved": True,
                "resolution": "False without a small positive eigenvalue. The companion Haar/Jacobi sparse-block limit has exponentially small trace from low rank while its positive edge converges to a constant fiber aspect.",
            },
            {
                "objection": "The S6 1/178 channel itself proves an asymptotic degree obstruction.",
                "resolved": True,
                "resolution": "It is constant-size and its trivial/sign source mechanism has factorially vanishing mass. A high-dimensional natural effect edge is still needed.",
            },
        ],
        headline_metrics={
            "matrix_component_povm_normal_form_theorem_count": int(exact),
            "povm_control_count": len(controls),
            "povm_control_failure_count": failures,
            "noncommuting_povm_control_count": int(noncommuting),
            "nested_recursive_povm_normal_form_theorem_count": int(
                recursive.exact_nested_matrix_povm_compiler_normal_form_verified
            ),
            "companion_natural_s6_partial_support_control_count": 1,
            "companion_direct_s6_source_mass_no_go_count": 1,
            "generic_square_root_degree_boundary_theorem_count": 1,
            "tail_input_size": tail.input_size,
            "tail_effect_edge_log2": tail.minimum_nonzero_effect_eigenvalue_log2,
            "tail_markov_degree_lower_bound_log2": tail.markov_degree_lower_bound_log2,
            "tail_polynomial_benchmark_log2": tail.polynomial_degree_benchmark_log2,
            "natural_component_povm_dilation_circuit_count": 0,
            "all_depth_gpe_support_transport_count": 0,
            "recursive_orientation_polar_sampler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_matrix_component_povm_normal_form_proved": exact,
            "exact_nested_recursive_povm_normal_form_proved": recursive.exact_nested_matrix_povm_compiler_normal_form_verified,
            "noncommuting_component_effects_algebraically_supported": noncommuting,
            "intrinsic_square_root_outcome_count_loss_required": False,
            "generic_square_root_block_encoding_can_be_superpolynomial": tail.generic_block_encoding_degree_superpolynomial_signal,
            "small_component_trace_proves_small_positive_effect_edge": False,
            "natural_component_povm_dilation_compiled": False,
            "all_n_component_support_polars_gpe_compatible": False,
            "high_dimension_partial_support_native_mass_controlled": False,
            "recursive_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Matrix partial supports admit an exact width-free Naimark/GPE "
                "normal form, but the natural square-root POVM dilation, support "
                "classification, effect edge, and high-dimensional mass are open."
            ),
        },
        status=(
            "matrix-povm-recursive-normal-form-proved-natural-dilation-and-support-gpe-open"
            if exact
            else "matrix-povm-recursive-compiler-control-failure"
        ),
        summary=(
            "Replaced the dead scalar-affine extension with an exact nested "
            "matrix-POVM compiler normal form and isolated square-root POVM "
            "dilation as the new access bottleneck."
        ),
        falsifiers_triggered=[
            "Noncommuting component effects do not obstruct an exact algebraic compiler normal form.",
            "Outcome count alone does not impose square-root amplitude amplification on a normalized child embedding.",
            "Pair GPE transport does not prepare matrix POVM square-root amplitudes.",
            "Generic block-encoding access can still be superpolynomial at an exponentially small effect edge.",
            "Small component trace or outcome probability does not prove that the positive effect edge is small.",
            "The finite S6 effect edge is not asymptotic evidence because its source mechanism is negligible.",
        ],
    )


def write_matrix_povm_recursive_compiler_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_matrix_povm_recursive_compiler())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_matrix_povm_recursive_compiler_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
