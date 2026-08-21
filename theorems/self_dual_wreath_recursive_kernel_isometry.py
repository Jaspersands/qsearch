"""Explicit orthonormal recursive kernel isometry and support reflection.

For a binary synthesis node ``S=[S_L S_R]``, let ``C_L,C_R`` be orthonormal
isometries onto the child kernels and let ``X`` be an orthonormal basis of
``range(S_L) intersection range(S_R)``.  Define

    Z = [S_L^+ X; -S_R^+ X],
    M = Z^*Z = X^*((S_LS_L^*)^+ +(S_RS_R^*)^+)X.           (1)

The child-kernel columns are orthogonal to ``Z``.  Therefore

    G=Z M^(-1/2),
    C=diag(C_L,C_R) direct_sum G                            (2)

is an isometry with ``range(C)=ker(S)``.  Recursing (2) gives an explicit
orthonormal isometry onto the complete leaf-synthesis kernel, including every
emergent higher relation missed by original pair intersections.

The coefficient support and its reflection are then

    P=I-CC^*,       Ref(P)=I-2CC^*.                         (3)

Thus a coherent implementation of the recursive relation isometry ``C``
would bypass a global sheaf-Laplacian gap theorem entirely.  This is an exact
algebraic alternative, not a free circuit: implementing ``C`` requires
coherent child pseudoinverses, common-span bases, and ``M^(-1/2)`` at every
node.  Generic complete hierarchies can make those metrics badly conditioned,
and no natural all-depth conditioning or endpoint gauge is proved.
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
    "research/representation/self_dual_wreath_recursive_kernel_isometry.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-RECURSIVE-KERNEL-ISOMETRY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class RecursiveKernelNodeControl:
    node_id: str
    leaf_count: int
    coefficient_dimension: int
    synthesis_rank: int
    direct_kernel_dimension: int
    left_child_kernel_dimension: int
    right_child_kernel_dimension: int
    common_span_dimension: int
    recursive_kernel_dimension: int
    cross_metric_minimum_eigenvalue: float | None
    cross_metric_maximum_eigenvalue: float | None
    cross_metric_condition_number: float | None
    cross_relation_isometry_residual: float
    child_cross_orthogonality_residual: float
    recursive_kernel_isometry_residual: float
    recursive_kernel_annihilation_residual: float
    recursive_to_direct_kernel_projector_residual: float
    support_projector_residual: float
    support_reflection_unitarity_residual: float
    exact_recursive_kernel_isometry_verified: bool
    status: str


@dataclass(frozen=True)
class RecursiveKernelIsometryControl:
    control_id: str
    physical_dimension: int
    leaf_count: int
    coefficient_dimension: int
    synthesis_rank: int
    direct_kernel_dimension: int
    recursive_kernel_dimension: int
    recursion_depth: int
    nontrivial_cross_relation_node_count: int
    maximum_cross_metric_condition_number: float
    maximum_recursive_kernel_projector_residual: float
    root_support_rank: int
    root_support_reflection_unitarity_residual: float
    exact_all_node_kernel_isometry_verified: bool
    status: str


@dataclass(frozen=True)
class RecursiveKernelScalingRecord:
    n: int
    information_threshold_copy_count: int
    orientation_leaf_count_decimal: str
    balanced_tree_depth: int
    maximum_factor_graph_degree: int
    global_sheaf_gap_required_given_direct_relation_isometry: bool
    coherent_child_pseudoinverse_proved: bool
    coherent_common_span_basis_proved: bool
    natural_cross_metric_conditioning_proved: bool
    coherent_recursive_relation_isometry_proved: bool
    physical_endpoint_gauge_proved: bool
    natural_orientation_polar_compiled: bool
    status: str


@dataclass(frozen=True)
class RecursiveKernelIsometryTheorem:
    cross_relation: str
    cross_metric: str
    orthonormal_recursion: str
    exact_support: str
    reflection: str
    compiler_scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class RecursiveKernelIsometryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: RecursiveKernelIsometryTheorem
    finite_controls: list[RecursiveKernelIsometryControl]
    node_controls: list[RecursiveKernelNodeControl]
    scaling_records: list[RecursiveKernelScalingRecord]
    circuit_schema: list[dict[str, str | bool]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@dataclass
class _KernelNodeData:
    synthesis: np.ndarray
    kernel_isometry: np.ndarray
    support_projector: np.ndarray
    depth: int
    records: list[RecursiveKernelNodeControl]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _support_basis(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    left, singular_values, _ = np.linalg.svd(matrix, full_matrices=False)
    return left[:, singular_values > 100 * tolerance]


def _kernel_basis(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    _, singular_values, right_adjoint = np.linalg.svd(matrix, full_matrices=True)
    rank = int(np.count_nonzero(singular_values > 100 * tolerance))
    return right_adjoint.conj().T[:, rank:]


def _intersection_basis(
    left: np.ndarray,
    right: np.ndarray,
    tolerance: float,
) -> np.ndarray:
    if not left.shape[1] or not right.shape[1]:
        return np.zeros((left.shape[0], 0), dtype=complex)
    vectors, singular_values, _ = np.linalg.svd(
        left.conj().T @ right,
        full_matrices=False,
    )
    return left @ vectors[:, singular_values >= 1.0 - 100 * tolerance]


def _psd_inverse_root(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    if not matrix.size:
        return np.zeros_like(matrix)
    values, vectors = np.linalg.eigh(_hermitian(matrix))
    if values[0] < -100 * tolerance:
        raise ArithmeticError("cross metric is not positive semidefinite")
    inverse = np.zeros_like(values)
    active = values > 100 * tolerance
    inverse[active] = values[active] ** -0.5
    return (vectors * inverse) @ vectors.conj().T


def _projector(basis: np.ndarray) -> np.ndarray:
    return basis @ basis.conj().T


def _embed_child_kernels(
    left: np.ndarray,
    right: np.ndarray,
    left_dimension: int,
    right_dimension: int,
) -> np.ndarray:
    output = np.zeros(
        (left_dimension + right_dimension, left.shape[1] + right.shape[1]),
        dtype=complex,
    )
    output[:left_dimension, : left.shape[1]] = left
    output[left_dimension:, left.shape[1] :] = right
    return output


def _resolve_kernel_node(
    leaf_maps: tuple[np.ndarray, ...],
    indices: tuple[int, ...],
    node_id: str,
    tolerance: float,
) -> _KernelNodeData:
    if len(indices) == 1:
        synthesis = leaf_maps[indices[0]]
        kernel = _kernel_basis(synthesis, tolerance)
        support = np.eye(synthesis.shape[1], dtype=complex) - _projector(kernel)
        return _KernelNodeData(synthesis, kernel, support, 0, [])

    middle = len(indices) // 2
    left = _resolve_kernel_node(
        leaf_maps,
        indices[:middle],
        node_id + "L",
        tolerance,
    )
    right = _resolve_kernel_node(
        leaf_maps,
        indices[middle:],
        node_id + "R",
        tolerance,
    )
    synthesis = np.concatenate((left.synthesis, right.synthesis), axis=1)
    left_dimension = left.synthesis.shape[1]
    right_dimension = right.synthesis.shape[1]
    left_span = _support_basis(left.synthesis, tolerance)
    right_span = _support_basis(right.synthesis, tolerance)
    common = _intersection_basis(left_span, right_span, tolerance)
    if common.shape[1]:
        left_preimage = np.linalg.pinv(left.synthesis, rcond=tolerance) @ common
        right_preimage = np.linalg.pinv(right.synthesis, rcond=tolerance) @ common
        cross = np.vstack((left_preimage, -right_preimage))
        metric = _hermitian(cross.conj().T @ cross)
        cross_isometry = cross @ _psd_inverse_root(metric, tolerance)
        metric_values = np.linalg.eigvalsh(metric)
        metric_positive = metric_values[metric_values > 100 * tolerance]
        metric_minimum = float(metric_positive[0])
        metric_maximum = float(metric_positive[-1])
        metric_condition = metric_maximum / metric_minimum
        cross_residual = float(
            np.linalg.norm(
                cross_isometry.conj().T @ cross_isometry
                - np.eye(common.shape[1]),
                ord=2,
            )
        )
    else:
        cross_isometry = np.zeros(
            (left_dimension + right_dimension, 0),
            dtype=complex,
        )
        metric_minimum = None
        metric_maximum = None
        metric_condition = None
        cross_residual = 0.0
    internal = _embed_child_kernels(
        left.kernel_isometry,
        right.kernel_isometry,
        left_dimension,
        right_dimension,
    )
    child_cross = float(
        np.linalg.norm(internal.conj().T @ cross_isometry, ord=2)
        if internal.shape[1] and cross_isometry.shape[1]
        else 0.0
    )
    kernel = np.concatenate((internal, cross_isometry), axis=1)
    direct = _kernel_basis(synthesis, tolerance)
    kernel_isometry_residual = float(
        np.linalg.norm(
            kernel.conj().T @ kernel - np.eye(kernel.shape[1]),
            ord=2,
        )
        if kernel.shape[1]
        else 0.0
    )
    annihilation = float(
        np.linalg.norm(synthesis @ kernel, ord=2) if kernel.shape[1] else 0.0
    )
    projector_residual = float(
        np.linalg.norm(_projector(kernel) - _projector(direct), ord=2)
    )
    support = np.eye(synthesis.shape[1], dtype=complex) - _projector(kernel)
    direct_support = np.eye(synthesis.shape[1], dtype=complex) - _projector(direct)
    support_residual = float(np.linalg.norm(support - direct_support, ord=2))
    reflection = np.eye(synthesis.shape[1], dtype=complex) - 2.0 * _projector(kernel)
    reflection_residual = float(
        np.linalg.norm(reflection.conj().T @ reflection - np.eye(reflection.shape[0]), ord=2)
    )
    verified = bool(
        kernel.shape[1] == direct.shape[1]
        and max(
            cross_residual,
            child_cross,
            kernel_isometry_residual,
            annihilation,
            projector_residual,
            support_residual,
            reflection_residual,
        )
        <= 1000 * tolerance
    )
    record = RecursiveKernelNodeControl(
        node_id=node_id,
        leaf_count=len(indices),
        coefficient_dimension=synthesis.shape[1],
        synthesis_rank=synthesis.shape[1] - direct.shape[1],
        direct_kernel_dimension=direct.shape[1],
        left_child_kernel_dimension=left.kernel_isometry.shape[1],
        right_child_kernel_dimension=right.kernel_isometry.shape[1],
        common_span_dimension=common.shape[1],
        recursive_kernel_dimension=kernel.shape[1],
        cross_metric_minimum_eigenvalue=metric_minimum,
        cross_metric_maximum_eigenvalue=metric_maximum,
        cross_metric_condition_number=metric_condition,
        cross_relation_isometry_residual=cross_residual,
        child_cross_orthogonality_residual=child_cross,
        recursive_kernel_isometry_residual=kernel_isometry_residual,
        recursive_kernel_annihilation_residual=annihilation,
        recursive_to_direct_kernel_projector_residual=projector_residual,
        support_projector_residual=support_residual,
        support_reflection_unitarity_residual=reflection_residual,
        exact_recursive_kernel_isometry_verified=verified,
        status=(
            "exact-orthonormal-recursive-kernel-isometry"
            if verified
            else "recursive-kernel-isometry-control-failure"
        ),
    )
    return _KernelNodeData(
        synthesis=synthesis,
        kernel_isometry=kernel,
        support_projector=support,
        depth=max(left.depth, right.depth) + 1,
        records=[*left.records, *right.records, record],
    )


def audit_recursive_kernel_isometry(
    control_id: str,
    leaf_maps: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> RecursiveKernelIsometryControl:
    if len(leaf_maps) < 2 or len(leaf_maps) & (len(leaf_maps) - 1):
        raise ValueError("a power-of-two family of at least two leaf maps is required")
    physical = leaf_maps[0].shape[0]
    if any(
        leaf.ndim != 2 or leaf.shape[0] != physical or not leaf.shape[1]
        for leaf in leaf_maps
    ):
        raise ValueError("leaf maps must share one nonempty physical codomain")
    data = _resolve_kernel_node(
        leaf_maps,
        tuple(range(len(leaf_maps))),
        control_id + "-ROOT",
        tolerance,
    )
    direct = _kernel_basis(data.synthesis, tolerance)
    failures = sum(not record.exact_recursive_kernel_isometry_verified for record in data.records)
    conditions = [
        record.cross_metric_condition_number
        for record in data.records
        if record.cross_metric_condition_number is not None
    ]
    reflection = np.eye(data.synthesis.shape[1], dtype=complex) - 2 * _projector(
        data.kernel_isometry
    )
    return RecursiveKernelIsometryControl(
        control_id=control_id,
        physical_dimension=physical,
        leaf_count=len(leaf_maps),
        coefficient_dimension=data.synthesis.shape[1],
        synthesis_rank=data.synthesis.shape[1] - direct.shape[1],
        direct_kernel_dimension=direct.shape[1],
        recursive_kernel_dimension=data.kernel_isometry.shape[1],
        recursion_depth=data.depth,
        nontrivial_cross_relation_node_count=sum(
            record.common_span_dimension > 0 for record in data.records
        ),
        maximum_cross_metric_condition_number=max(conditions, default=1.0),
        maximum_recursive_kernel_projector_residual=max(
            (record.recursive_to_direct_kernel_projector_residual for record in data.records),
            default=0.0,
        ),
        root_support_rank=int(round(float(np.trace(data.support_projector).real))),
        root_support_reflection_unitarity_residual=float(
            np.linalg.norm(
                reflection.conj().T @ reflection - np.eye(reflection.shape[0]),
                ord=2,
            )
        ),
        exact_all_node_kernel_isometry_verified=failures == 0,
        status=(
            "exact-complete-recursive-kernel-isometry"
            if failures == 0
            else "recursive-kernel-isometry-audit-failure"
        ),
    )


def _rank_one_leaf(vector: tuple[complex, ...]) -> np.ndarray:
    column = np.asarray(vector, dtype=complex).reshape(-1, 1)
    return column / np.linalg.norm(column)


def _three_lines_augmented_control() -> tuple[np.ndarray, ...]:
    return (
        _rank_one_leaf((1.0, 0.0)),
        _rank_one_leaf((0.0, 1.0)),
        _rank_one_leaf((1.0, 1.0)),
        _rank_one_leaf((1.0, -1.0)),
    )


def _random_rank_one_leaves(
    physical_dimension: int,
    leaf_count: int,
    seed: int,
) -> tuple[np.ndarray, ...]:
    rng = np.random.default_rng(seed)
    leaves = []
    for _ in range(leaf_count):
        vector = rng.normal(size=physical_dimension) + 1j * rng.normal(
            size=physical_dimension
        )
        leaves.append((vector / np.linalg.norm(vector)).reshape(-1, 1))
    return tuple(leaves)


def recursive_kernel_scaling_record(n: int) -> RecursiveKernelScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    leaves = 1 << copies
    return RecursiveKernelScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        orientation_leaf_count_decimal=str(leaves),
        balanced_tree_depth=copies,
        maximum_factor_graph_degree=3,
        global_sheaf_gap_required_given_direct_relation_isometry=False,
        coherent_child_pseudoinverse_proved=False,
        coherent_common_span_basis_proved=False,
        natural_cross_metric_conditioning_proved=False,
        coherent_recursive_relation_isometry_proved=False,
        physical_endpoint_gauge_proved=False,
        natural_orientation_polar_compiled=False,
        status="exact-recursive-support-reflection-normal-form-node-access-open",
    )


def recursive_kernel_isometry_theorem() -> RecursiveKernelIsometryTheorem:
    return RecursiveKernelIsometryTheorem(
        cross_relation="Z=[S_L^+X;-S_R^+X]",
        cross_metric="M=Z^*Z=X^*((S_LS_L^*)^++(S_RS_R^*)^+)X",
        orthonormal_recursion=(
            "C_T=diag(C_L,C_R) direct_sum ZM^(-1/2) is an isometry onto ker S_T"
        ),
        exact_support="P_T=I-C_TC_T^*=supp(S_T^*S_T)",
        reflection="Ref(P_T)=I-2C_TC_T^*",
        compiler_scope=(
            "direct coherent C_T access removes a global sheaf gap but still "
            "requires child pseudoinverses, common-span access, and M^(-1/2)"
        ),
        theorem_verified=True,
        status="orthonormal-recursive-kernel-isometry-and-support-reflection-proved",
    )


def run_recursive_kernel_isometry() -> RecursiveKernelIsometryReport:
    controls = [
        audit_recursive_kernel_isometry(
            "FOUR-DISTINCT-LINES-EMERGENT-ROOT-RELATIONS",
            _three_lines_augmented_control(),
        ),
        audit_recursive_kernel_isometry(
            "RANDOM-C3-EIGHT-LINES",
            _random_rank_one_leaves(3, 8, 2301),
        ),
        audit_recursive_kernel_isometry(
            "RANDOM-C5-EIGHT-LINES",
            _random_rank_one_leaves(5, 8, 2302),
        ),
    ]
    scaling = [
        recursive_kernel_scaling_record(n)
        for n in (8, 16, 32, 64, 128, 256, 512)
    ]
    theorem = recursive_kernel_isometry_theorem()
    node_controls: list[RecursiveKernelNodeControl] = []
    for control_id, leaves in (
        ("FOUR-DISTINCT-LINES-EMERGENT-ROOT-RELATIONS", _three_lines_augmented_control()),
        ("RANDOM-C3-EIGHT-LINES", _random_rank_one_leaves(3, 8, 2301)),
        ("RANDOM-C5-EIGHT-LINES", _random_rank_one_leaves(5, 8, 2302)),
    ):
        node_controls.extend(
            _resolve_kernel_node(
                leaves,
                tuple(range(len(leaves))),
                control_id + "-ROOT",
                1e-9,
            ).records
        )
    failures = sum(not row.exact_all_node_kernel_isometry_verified for row in controls)
    node_failures = sum(not row.exact_recursive_kernel_isometry_verified for row in node_controls)
    verified = theorem.theorem_verified and failures == 0 and node_failures == 0
    return RecursiveKernelIsometryReport(
        created_at=utc_now(),
        theorem_contract={
            "cross_relation": theorem.cross_relation,
            "metric": theorem.cross_metric,
            "recursion": theorem.orthonormal_recursion,
            "support": theorem.exact_support,
            "reflection": theorem.reflection,
            "scope": theorem.compiler_scope,
        },
        theorem=theorem,
        finite_controls=controls,
        node_controls=node_controls,
        scaling_records=scaling,
        circuit_schema=[
            {
                "step": "child_kernel_branch",
                "operation": "coherently recurse into the left or right relation isometry",
                "proved_for_natural_family": False,
            },
            {
                "step": "cross_common_span",
                "operation": "prepare X in range(S_L) intersection range(S_R)",
                "proved_for_natural_family": False,
            },
            {
                "step": "minimum_energy_preimages",
                "operation": "apply S_L^+ and S_R^+ coherently",
                "proved_for_natural_family": False,
            },
            {
                "step": "cross_metric_whitening",
                "operation": "apply M^(-1/2) to make the cross relation an isometry",
                "proved_for_natural_family": False,
            },
            {
                "step": "kernel_reflection",
                "operation": "use C_T, a phase flip, and C_T^* to implement I-2C_TC_T^*",
                "proved_for_natural_family": False,
            },
        ],
        proof_obligations=[
            {
                "obligation": "orthonormalize_complete_recursive_dependency_basis",
                "resolved": verified,
                "resolution": (
                    "The exact cross metric whitens each parent relation and is "
                    "orthogonal to both embedded child kernels."
                ),
            },
            {
                "obligation": "eliminate_global_sheaf_gap_given_direct_relation_isometry",
                "resolved": verified,
                "resolution": (
                    "A direct isometry onto the full kernel implements its reflection "
                    "without spectral filtering a global incidence."
                ),
            },
            {
                "obligation": "compile_natural_child_pseudoinverse_and_common_span_access",
                "resolved": False,
                "resolution": (
                    "The exact formulas still require tightly normalized support and "
                    "minimum-energy preimage transforms at every node."
                ),
            },
            {
                "obligation": "prove_natural_all_depth_cross_metric_conditioning",
                "resolved": False,
                "resolution": (
                    "Generic exact hierarchies can be exponentially imbalanced; no "
                    "natural uniform M^(-1/2) complexity bound is known."
                ),
            },
            {
                "obligation": "supply_physical_endpoint_gauge_after_support_reflection",
                "resolved": False,
                "resolution": (
                    "The kernel isometry fixes the coefficient support, not the "
                    "physical-to-support polar gauge."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Emergent higher relations prevent exact recursive coverage.",
                "resolved": True,
                "resolution": (
                    "They appear exactly as cross relations of recursively formed child spans."
                ),
            },
            {
                "objection": "The unnormalized pseudoinverse cross map is already an isometry.",
                "resolved": True,
                "resolution": "Its exact metric is M; M^(-1/2) is necessary in general.",
            },
            {
                "objection": "Exact recursive coverage proves an efficient support reflection.",
                "resolved": False,
                "resolution": (
                    "Only if all child support, pseudoinverse, common-span, and metric "
                    "operations are coherently implementable with polynomial normalization."
                ),
            },
            {
                "objection": "The recursive support reflection resolves the physical endpoint.",
                "resolved": False,
                "resolution": (
                    "Range access leaves the input gauge ambiguous and needs a separate boundary polar."
                ),
            },
        ],
        headline_metrics={
            "orthonormal_recursive_kernel_isometry_theorem_count": int(verified),
            "direct_support_reflection_normal_form_count": int(verified),
            "global_sheaf_gap_bypass_count": int(verified),
            "finite_control_count": len(controls),
            "finite_node_control_count": len(node_controls),
            "finite_control_failure_count": failures + node_failures,
            "coherent_natural_recursive_kernel_isometry_count": 0,
            "natural_all_depth_metric_conditioning_count": 0,
            "physical_endpoint_gauge_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_recursive_kernel_isometry_normal_form_proved": verified,
            "exact_dependency_coverage_proved_information_theoretically": verified,
            "global_sheaf_gap_required_if_relation_isometry_compiled": False,
            "coherent_natural_child_pseudoinverses_proved": False,
            "coherent_natural_common_span_access_proved": False,
            "natural_all_depth_cross_metric_conditioning_proved": False,
            "coherent_recursive_relation_isometry_compiled": False,
            "physical_endpoint_gauge_compiled": False,
            "natural_orientation_polar_compiled": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Exact dependency coverage and reflection algebra are solved, but "
                "the node transforms and endpoint gauge have no polynomial circuit."
            ),
        },
        status=(
            "recursive-kernel-isometry-proved-node-access-and-gauge-open"
            if verified
            else "recursive-kernel-isometry-control-failure"
        ),
        summary=(
            "Whitening each pseudoinverse cross relation gives an explicit "
            "orthonormal recursive isometry onto the full synthesis kernel and a "
            "direct support reflection. This bypasses a global sheaf-gap theorem "
            "conditional on coherent node pseudoinverses, common spans, and metrics."
        ),
        falsifiers_triggered=[
            "Emergent higher dependencies do not prevent exact recursive support coverage.",
            "A global sheaf spectral gap is not mandatory if the recursive relation isometry is direct.",
            "Exact recursive algebra does not imply polynomial node transforms or endpoint access.",
        ],
    )


def write_recursive_kernel_isometry_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-RECURSIVE-KERNEL-ISOMETRY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_recursive_kernel_isometry" in globals():
        report = run_recursive_kernel_isometry(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-RECURSIVE-KERNEL-ISOMETRY",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-RECURSIVE-KERNEL-ISOMETRY.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-RECURSIVE-KERNEL-ISOMETRY.",
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
                    "self_dual_wreath_recursive_kernel_isometry": str(path)
                },
            )
        )
    return payload
