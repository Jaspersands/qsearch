"""Partial-isometry sheaf resolver for noncommuting component geometry.

The flat equal-rank GPE holonomy model cannot realize the natural component
POVM because every vertex effect is scalar.  The correct graph-level object is
a partial-isometry connection.

For an oriented edge ``a=(u,v)``, let ``U_a:H_u->H_v`` be a partial isometry,
with initial and final projections

    P_a=U_a^*U_a,       Q_a=U_aU_a^*.                       (1)

The edge residual of a vertex field ``x=(x_v)`` is

    (delta x)_a = Q_a x_v-U_a P_a x_u.                     (2)

The sheaf Laplacian ``L=delta^*delta`` has

    ker L=ker delta.                                       (3)

If ``B:F->direct_sum_v H_v`` is an orthonormal basis of that kernel, then

    H_v=B^*D_vB,       sum_v H_v=I_F,                      (4)

is the component POVM of the resolved section space.  Unlike the flat case,
these effects can be noncommuting; a rank-one partial triangle gives an exact
finite witness.

If the graph has maximum degree ``Delta``, then

    ||delta|| <= sqrt(2 Delta).                            (5)

Consequently a coherent block encoding of the edge incidence, normalized by
``beta<=sqrt(2 Delta)``, and a minimum positive singular value ``sigma`` give
a kernel reflection/filter with polynomial degree

    O((beta/sigma) log(1/epsilon)).                        (6)

This removes explicit path choice and cycle-gauge fixing: both are encoded in
one positive sheaf Laplacian.  It does not remove the substantive natural
gates.  One must prove a polynomially selectable sparse family of GPE partial
edges, prove that its incidence kernel is the exact natural coefficient
support (including emergent higher relations), establish an inverse-polynomial
gap on native mass, and compile the endpoint intertwiner from the physical
input into the resolved support.

The construction is therefore a precise conditional architecture, not a
completed PGM, decoder, algorithm, or speedup.
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
    "self_dual_wreath_partial_holonomy_sheaf_resolver.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PARTIAL-HOLONOMY-SHEAF-RESOLVER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PartialTransportEdge:
    source: int
    target: int
    transport: np.ndarray


@dataclass(frozen=True)
class PartialSheafResolverControl:
    control_id: str
    vertex_count: int
    edge_count: int
    vertex_fiber_dimension: int
    maximum_graph_degree: int
    incidence_row_dimension: int
    incidence_column_dimension: int
    incidence_rank: int
    section_space_dimension: int
    minimum_positive_incidence_singular_value: float | None
    incidence_operator_norm: float
    sparse_degree_norm_upper_bound: float
    kernel_laplacian_residual: float
    section_isometry_residual: float
    component_effect_sum_residual: float
    maximum_component_commutator_norm: float
    normalized_component_m4: float
    component_effects_pairwise_commute: bool
    partial_edge_identities_verified: bool
    exact_sheaf_kernel_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class PartialSheafScalingRecord:
    n: int
    information_threshold_copy_count: int
    orientation_vertex_count_decimal: str
    conditional_maximum_generator_degree: int
    conditional_incidence_normalization_upper_bound: float
    pair_gpe_partial_transport_per_edge_polynomial: bool
    polynomial_coherent_edge_select_proved: bool
    exact_natural_dependency_kernel_coverage_proved: bool
    inverse_polynomial_sheaf_gap_proved: bool
    endpoint_intertwiner_polar_proved: bool
    natural_component_povm_compiled: bool
    status: str


@dataclass(frozen=True)
class PartialSheafResolverTheorem:
    incidence: str
    kernel: str
    component_povm: str
    sparse_norm: str
    conditional_filter_complexity: str
    natural_scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PartialHolonomySheafResolverReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PartialSheafResolverTheorem
    finite_controls: list[PartialSheafResolverControl]
    scaling_records: list[PartialSheafScalingRecord]
    circuit_schema: list[dict[str, str | bool]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _projection_residual(matrix: np.ndarray) -> float:
    return float(
        max(
            np.linalg.norm(matrix - matrix.conj().T, ord=2),
            np.linalg.norm(matrix @ matrix - matrix, ord=2),
        )
    )


def _validate_edges(
    vertex_count: int,
    edges: tuple[PartialTransportEdge, ...],
    tolerance: float,
) -> tuple[int, int, float]:
    if vertex_count < 2 or not edges:
        raise ValueError("a nonempty graph on at least two vertices is required")
    dimension = edges[0].transport.shape[0]
    if dimension < 1:
        raise ValueError("vertex fibers must be nonempty")
    degrees = [0] * vertex_count
    residual = 0.0
    seen: set[tuple[int, int]] = set()
    for edge in edges:
        if not 0 <= edge.source < vertex_count or not 0 <= edge.target < vertex_count:
            raise ValueError("edge endpoint out of range")
        if edge.source == edge.target:
            raise ValueError("self edges are not allowed")
        key = tuple(sorted((edge.source, edge.target)))
        if key in seen:
            raise ValueError("duplicate undirected edges are not allowed")
        seen.add(key)
        transport = edge.transport
        if transport.ndim != 2 or transport.shape != (dimension, dimension):
            raise ValueError("all edge transports must share one square fiber")
        initial = _hermitian(transport.conj().T @ transport)
        final = _hermitian(transport @ transport.conj().T)
        edge_residual = max(
            _projection_residual(initial),
            _projection_residual(final),
            float(np.linalg.norm(transport @ initial - transport, ord=2)),
            float(np.linalg.norm(final @ transport - transport, ord=2)),
        )
        if edge_residual > 1000 * tolerance:
            raise ValueError("edge maps must be partial isometries")
        residual = max(residual, edge_residual)
        degrees[edge.source] += 1
        degrees[edge.target] += 1
    return dimension, max(degrees), residual


def partial_connection_incidence(
    vertex_count: int,
    edges: tuple[PartialTransportEdge, ...],
    *,
    tolerance: float = 1e-9,
) -> tuple[np.ndarray, int, float]:
    dimension, maximum_degree, residual = _validate_edges(
        vertex_count,
        edges,
        tolerance,
    )
    incidence = np.zeros(
        (len(edges) * dimension, vertex_count * dimension),
        dtype=complex,
    )
    for index, edge in enumerate(edges):
        row = slice(index * dimension, (index + 1) * dimension)
        source = slice(edge.source * dimension, (edge.source + 1) * dimension)
        target = slice(edge.target * dimension, (edge.target + 1) * dimension)
        final = _hermitian(edge.transport @ edge.transport.conj().T)
        incidence[row, source] = -edge.transport
        incidence[row, target] = final
    return incidence, maximum_degree, residual


def kernel_basis(matrix: np.ndarray, tolerance: float = 1e-9) -> np.ndarray:
    _, singular_values, right_adjoint = np.linalg.svd(matrix, full_matrices=True)
    rank = int(np.count_nonzero(singular_values > 100 * tolerance))
    return right_adjoint.conj().T[:, rank:]


def coordinate_component_effects(
    section_basis: np.ndarray,
    vertex_count: int,
) -> tuple[np.ndarray, ...]:
    if section_basis.ndim != 2 or section_basis.shape[0] % vertex_count:
        raise ValueError("section basis must split into equal vertex fibers")
    dimension = section_basis.shape[0] // vertex_count
    return tuple(
        _hermitian(
            section_basis[index * dimension : (index + 1) * dimension].conj().T
            @ section_basis[index * dimension : (index + 1) * dimension]
        )
        for index in range(vertex_count)
    )


def component_m4(effects: tuple[np.ndarray, ...]) -> float:
    return sum(
        float(np.linalg.norm(left @ right - right @ left, ord="fro") ** 2 / 2)
        for left in effects
        for right in effects
    )


def audit_partial_sheaf_resolver(
    control_id: str,
    vertex_count: int,
    edges: tuple[PartialTransportEdge, ...],
    *,
    tolerance: float = 1e-9,
) -> PartialSheafResolverControl:
    incidence, maximum_degree, edge_residual = partial_connection_incidence(
        vertex_count,
        edges,
        tolerance=tolerance,
    )
    dimension = incidence.shape[1] // vertex_count
    singular_values = np.linalg.svd(incidence, compute_uv=False)
    positive = singular_values[singular_values > 100 * tolerance]
    rank = len(positive)
    basis = kernel_basis(incidence, tolerance)
    laplacian = incidence.conj().T @ incidence
    kernel_residual = float(np.linalg.norm(laplacian @ basis, ord=2))
    section_residual = float(
        np.linalg.norm(
            basis.conj().T @ basis - np.eye(basis.shape[1]),
            ord=2,
        )
    )
    effects = coordinate_component_effects(basis, vertex_count)
    identity = np.eye(basis.shape[1], dtype=complex)
    effect_sum_residual = float(
        np.linalg.norm(sum(effects, np.zeros_like(identity)) - identity, ord=2)
    )
    maximum_commutator = max(
        (
            float(np.linalg.norm(left @ right - right @ left, ord=2))
            for index, left in enumerate(effects)
            for right in effects[index + 1 :]
        ),
        default=0.0,
    )
    commute = maximum_commutator <= 1000 * tolerance
    m4 = component_m4(effects) / basis.shape[1]
    operator_norm = float(np.linalg.norm(incidence, ord=2))
    norm_bound = math.sqrt(2.0 * maximum_degree)
    verified = bool(
        max(
            edge_residual,
            kernel_residual,
            section_residual,
            effect_sum_residual,
            max(0.0, operator_norm - norm_bound),
        )
        <= 1000 * tolerance
        and basis.shape[1] == incidence.shape[1] - rank
    )
    return PartialSheafResolverControl(
        control_id=control_id,
        vertex_count=vertex_count,
        edge_count=len(edges),
        vertex_fiber_dimension=dimension,
        maximum_graph_degree=maximum_degree,
        incidence_row_dimension=incidence.shape[0],
        incidence_column_dimension=incidence.shape[1],
        incidence_rank=rank,
        section_space_dimension=basis.shape[1],
        minimum_positive_incidence_singular_value=(
            float(positive[-1]) if len(positive) else None
        ),
        incidence_operator_norm=operator_norm,
        sparse_degree_norm_upper_bound=norm_bound,
        kernel_laplacian_residual=kernel_residual,
        section_isometry_residual=section_residual,
        component_effect_sum_residual=effect_sum_residual,
        maximum_component_commutator_norm=maximum_commutator,
        normalized_component_m4=m4,
        component_effects_pairwise_commute=commute,
        partial_edge_identities_verified=edge_residual <= 1000 * tolerance,
        exact_sheaf_kernel_reduction_verified=verified,
        status=(
            "exact-partial-sheaf-noncommuting-component-resolver"
            if verified and not commute
            else "exact-flat-sheaf-scalar-component-resolver"
            if verified
            else "partial-sheaf-resolver-control-failure"
        ),
    )


def _unit_vector(rng: np.random.Generator, dimension: int) -> np.ndarray:
    vector = rng.normal(size=dimension) + 1j * rng.normal(size=dimension)
    return vector / np.linalg.norm(vector)


def rank_one_partial_edge(
    source: int,
    target: int,
    initial_vector: np.ndarray,
    final_vector: np.ndarray,
) -> PartialTransportEdge:
    left = np.asarray(initial_vector, dtype=complex)
    right = np.asarray(final_vector, dtype=complex)
    if left.ndim != 1 or right.shape != left.shape:
        raise ValueError("rank-one edge vectors must share one dimension")
    if not np.linalg.norm(left) or not np.linalg.norm(right):
        raise ValueError("rank-one edge vectors must be nonzero")
    left = left / np.linalg.norm(left)
    right = right / np.linalg.norm(right)
    return PartialTransportEdge(source, target, np.outer(right, left.conj()))


def _partial_triangle(seed: int) -> tuple[PartialTransportEdge, ...]:
    rng = np.random.default_rng(seed)
    return tuple(
        rank_one_partial_edge(u, v, _unit_vector(rng, 2), _unit_vector(rng, 2))
        for u, v in ((0, 1), (1, 2), (0, 2))
    )


def _flat_tree() -> tuple[PartialTransportEdge, ...]:
    rotation = np.asarray(
        [[math.cos(0.4), -math.sin(0.4)], [math.sin(0.4), math.cos(0.4)]],
        dtype=complex,
    )
    phase = np.diag([np.exp(0.3j), np.exp(-0.2j)]).astype(complex)
    return (
        PartialTransportEdge(0, 1, rotation),
        PartialTransportEdge(1, 2, phase),
    )


def partial_sheaf_scaling_record(n: int) -> PartialSheafScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    vertices = 1 << copies
    conditional_degree = max(2, copies * copies)
    return PartialSheafScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        orientation_vertex_count_decimal=str(vertices),
        conditional_maximum_generator_degree=conditional_degree,
        conditional_incidence_normalization_upper_bound=math.sqrt(
            2.0 * conditional_degree
        ),
        pair_gpe_partial_transport_per_edge_polynomial=True,
        polynomial_coherent_edge_select_proved=False,
        exact_natural_dependency_kernel_coverage_proved=False,
        inverse_polynomial_sheaf_gap_proved=False,
        endpoint_intertwiner_polar_proved=False,
        natural_component_povm_compiled=False,
        status="partial-sheaf-architecture-defined-natural-generator-gap-open",
    )


def partial_sheaf_resolver_theorem() -> PartialSheafResolverTheorem:
    return PartialSheafResolverTheorem(
        incidence="(delta x)_a=Q_a x_v-U_aP_a x_u for partial edge U_a",
        kernel="ker(delta^*delta)=ker(delta)",
        component_povm="H_v=B^*D_vB and sum_vH_v=I for B=orth(ker delta)",
        sparse_norm="||delta||<=sqrt(2 Delta) for maximum graph degree Delta",
        conditional_filter_complexity=(
            "O((beta/sigma)log(1/error)) singular-value-filter degree given "
            "a beta-normalized coherent incidence block encoding"
        ),
        natural_scope=(
            "pair-edge circuits alone do not prove sparse coherent SELECT, exact "
            "dependency coverage, a natural gap, or the physical endpoint polar"
        ),
        theorem_verified=True,
        status="partial-isometry-sheaf-kernel-resolver-normal-form-proved",
    )


def run_partial_holonomy_sheaf_resolver() -> PartialHolonomySheafResolverReport:
    controls = [
        audit_partial_sheaf_resolver(
            "FLAT-UNITARY-TREE-CONTROL",
            3,
            _flat_tree(),
        ),
        audit_partial_sheaf_resolver(
            "RANK-ONE-PARTIAL-TRIANGLE-SEED-5",
            3,
            _partial_triangle(5),
        ),
        audit_partial_sheaf_resolver(
            "RANK-ONE-PARTIAL-TRIANGLE-SEED-17",
            3,
            _partial_triangle(17),
        ),
    ]
    scaling = [
        partial_sheaf_scaling_record(n)
        for n in (8, 16, 32, 64, 128, 256, 512)
    ]
    theorem = partial_sheaf_resolver_theorem()
    failures = sum(not row.exact_sheaf_kernel_reduction_verified for row in controls)
    partial_noncommuting = sum(
        row.normalized_component_m4 > 1e-10 for row in controls[1:]
    )
    flat_scalar = bool(
        controls[0].component_effects_pairwise_commute
        and controls[0].normalized_component_m4 <= 1e-10
    )
    verified = theorem.theorem_verified and failures == 0 and partial_noncommuting == 2
    return PartialHolonomySheafResolverReport(
        created_at=utc_now(),
        theorem_contract={
            "incidence": theorem.incidence,
            "kernel": theorem.kernel,
            "component_povm": theorem.component_povm,
            "normalization": theorem.sparse_norm,
            "conditional_filter": theorem.conditional_filter_complexity,
            "scope": theorem.natural_scope,
        },
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        circuit_schema=[
            {
                "step": "coherent_edge_select",
                "operation": (
                    "prepare a sparse generator edge label and SELECT its GPE "
                    "partial transport plus initial/final support flags"
                ),
                "proved_for_natural_family": False,
            },
            {
                "step": "incidence_block_encoding",
                "operation": (
                    "combine signed endpoint maps into delta/sqrt(2 Delta)"
                ),
                "proved_for_natural_family": False,
            },
            {
                "step": "kernel_filter",
                "operation": (
                    "singular-value transform delta across a promised gap sigma"
                ),
                "proved_for_natural_family": False,
            },
            {
                "step": "endpoint_intertwiner",
                "operation": (
                    "map the physical input coherently into the resolved coefficient support"
                ),
                "proved_for_natural_family": False,
            },
            {
                "step": "coordinate_readout",
                "operation": "reversibly expose the orientation vertex register",
                "proved_for_natural_family": True,
            },
        ],
        proof_obligations=[
            {
                "obligation": "define_nonflat_partial_holonomy_resolver",
                "resolved": verified,
                "resolution": (
                    "The partial incidence and sheaf Laplacian exactly resolve a "
                    "section space whose coordinate effects may be noncommuting."
                ),
            },
            {
                "obligation": "construct_polynomial_coherent_natural_edge_select",
                "resolved": False,
                "resolution": (
                    "Need a reversible polynomial-degree generator rule; an "
                    "exponential table of orientation pairs is not acceptable."
                ),
            },
            {
                "obligation": "prove_exact_natural_dependency_kernel_coverage",
                "resolved": False,
                "resolution": (
                    "Pair relations can miss emergent higher dependencies. Prove "
                    "the multilevel incidence has kernel equal to the natural support."
                ),
            },
            {
                "obligation": "prove_inverse_polynomial_natural_sheaf_gap",
                "resolved": False,
                "resolution": (
                    "The weighted pair bulk edge is relevant input but does not "
                    "control incomplete relations or multilevel outliers."
                ),
            },
            {
                "obligation": "compile_physical_endpoint_intertwiner",
                "resolved": False,
                "resolution": (
                    "A support reflection does not fix the polar gauge mapping the "
                    "physical input into that support."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Partial connections still force scalar vertex effects.",
                "resolved": True,
                "resolution": (
                    "Two exact rank-one triangle controls have nonzero component M4."
                ),
            },
            {
                "objection": "Explicit path and holonomy gauges remain necessary.",
                "resolved": True,
                "resolution": (
                    "The kernel of one positive sheaf Laplacian enforces all edge "
                    "and cycle constraints without choosing a spanning path."
                ),
            },
            {
                "objection": "The abstract sheaf normal form is already a circuit.",
                "resolved": False,
                "resolution": (
                    "Natural edge SELECT, kernel coverage, gap, and endpoint polar "
                    "are all unproved and are exactly the expensive operations."
                ),
            },
            {
                "objection": "Any pair-edge family spans the full natural dependency space.",
                "resolved": False,
                "resolution": (
                    "Existing emergent-homology controls disprove this without a "
                    "multilevel completion theorem."
                ),
            },
        ],
        headline_metrics={
            "partial_sheaf_kernel_normal_form_theorem_count": int(verified),
            "finite_partial_noncommuting_control_count": partial_noncommuting,
            "finite_flat_scalar_control_count": int(flat_scalar),
            "finite_control_failure_count": failures,
            "polynomial_natural_edge_select_count": 0,
            "exact_natural_dependency_coverage_count": 0,
            "inverse_polynomial_natural_sheaf_gap_count": 0,
            "physical_endpoint_intertwiner_count": 0,
            "natural_component_povm_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "partial_sheaf_resolver_normal_form_proved": verified,
            "partial_connections_can_have_noncommuting_component_effects": (
                partial_noncommuting == 2
            ),
            "flat_holonomy_limit_recovers_scalar_effects": flat_scalar,
            "natural_sparse_coherent_edge_select_proved": False,
            "natural_exact_dependency_kernel_coverage_proved": False,
            "natural_inverse_polynomial_sheaf_gap_proved": False,
            "physical_endpoint_intertwiner_compiled": False,
            "natural_component_povm_compiled": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The correct nonflat resolver is defined, but none of its four "
                "natural access, coverage, gap, and endpoint obligations is solved."
            ),
        },
        status=(
            "partial-holonomy-sheaf-normal-form-proved-natural-compiler-open"
            if verified
            else "partial-holonomy-sheaf-control-failure"
        ),
        summary=(
            "A partial-isometry sheaf Laplacian is the first graph resolver in "
            "the project capable of noncommuting component geometry. It replaces "
            "explicit path/holonomy bookkeeping by one kernel filter, conditional "
            "on a sparse natural edge SELECT, exact dependency coverage, a gap, and "
            "the physical endpoint polar."
        ),
        falsifiers_triggered=[
            "Flat equal-rank holonomy is not expressive enough for the natural component POVM.",
            "Pair-edge availability does not imply exact global dependency coverage.",
            "A kernel reflection alone does not determine the physical input gauge.",
        ],
    )


def write_partial_holonomy_sheaf_resolver_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-PARTIAL-HOLONOMY-SHEAF-RESOLVER"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_partial_holonomy_sheaf_resolver" in globals():
        report = run_partial_holonomy_sheaf_resolver(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-PARTIAL-HOLONOMY-SHEAF-RESOLVER",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-PARTIAL-HOLONOMY-SHEAF-RESOLVER.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-PARTIAL-HOLONOMY-SHEAF-RESOLVER.",
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
                    "self_dual_wreath_partial_holonomy_sheaf_resolver": str(path)
                },
            )
        )
    return payload
