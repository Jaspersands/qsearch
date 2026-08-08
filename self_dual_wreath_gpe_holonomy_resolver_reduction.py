"""Reduce flat carrier-channel resolution to executable holonomy fixed spaces.

The GPE pair-polar circuit makes every natural pair transport executable, but
different orientation pairs regroup tensor factors differently.  Products
around cycles are therefore genuine Racah/holonomy operators; they need not
cancel merely because each edge polar is a canonical carrier-row swap.

There is nevertheless an exact and useful reduction.  On one equal-rank flat
carrier channel, let ``U_(v<-u)`` be the unitary edge transports and impose

    x_v = U_(v<-u) x_u.

Choose a root and a spanning tree.  Tree transport writes every section as
``x_v=T_v x_root``.  Each non-tree edge then imposes one root-fiber fixed-space
condition

    H_e x_root = x_root,
    H_e = T_v^* U_(v<-u) T_u.

Thus the kernel of the full connection incidence/Laplacian is isometric to
the simultaneous ``+1`` eigenspace of the fundamental-cycle holonomies.  A
GPE pair-polar circuit compiles every factor of every ``H_e`` without an
explicit Kronecker multiplicity basis.

If a polynomially selectable generator family has an inverse-polynomial gap
for

    H_fix = average_e (I-H_e)^*(I-H_e)/4,

phase estimation or singular-value filtering gives a coherent common-section
resolver.  The gap assumption is substantive.  A two-dimensional rotation by
an arbitrarily small angle has efficient edge circuits but a fixed-space
Hamiltonian eigenvalue ``sin^2(theta/2)``.  Efficient pair transport alone
therefore does not imply an efficient higher-order resolver.

The theorem applies to flat equal-rank carrier channels.  Partial supports,
emergent child-span dependencies, and complete relative-frame whitening need
additional reductions; it is not a complete PGM circuit.
"""

from __future__ import annotations

import json
import math
from collections import deque
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_gpe_holonomy_resolver_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-GPE-HOLONOMY-RESOLVER-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Edge = tuple[int, int]


@dataclass(frozen=True)
class HolonomyFixedSpaceControl:
    control_id: str
    vertex_count: int
    edge_count: int
    fiber_dimension: int
    spanning_tree_edge_count: int
    fundamental_cycle_count: int
    connection_kernel_dimension: int
    holonomy_fixed_space_dimension: int
    kernel_dimension_residual: int
    minimum_positive_connection_laplacian_eigenvalue: float | None
    minimum_positive_fixed_space_hamiltonian_eigenvalue: float | None
    maximum_tree_edge_constraint_residual: float
    exact_holonomy_fixed_space_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class NearFlatHolonomyCounterexample:
    exponent: int
    rotation_angle: float
    edge_transport_gate_description_size: int
    fixed_space_dimension: int
    fixed_space_hamiltonian_gap: float
    inverse_gap_log2: float
    pair_transport_is_exact_unitary: bool
    inverse_polynomial_gap_guaranteed: bool
    status: str


@dataclass(frozen=True)
class GpeHolonomyResolverScalingRecord:
    n: int
    information_threshold_copy_count: int
    orientation_label_qubit_count: int
    gpe_pair_polar_per_edge_polynomial: bool
    cycle_holonomy_circuit_polynomial_given_short_paths: bool
    coherent_generator_select_proved: bool
    inverse_polynomial_fixed_space_gap_proved: bool
    partial_support_reduction_proved: bool
    emergent_dependency_reduction_proved: bool
    complete_relative_frame_resolver_proved: bool
    status: str


@dataclass(frozen=True)
class GpeHolonomyResolverReductionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[HolonomyFixedSpaceControl]
    near_flat_counterexamples: list[NearFlatHolonomyCounterexample]
    scaling_records: list[GpeHolonomyResolverScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def rotation(angle: float) -> np.ndarray:
    return np.asarray(
        [
            [math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)],
        ],
        dtype=complex,
    )


def _canonical_edge(edge: Edge) -> Edge:
    left, right = edge
    if left == right:
        raise ValueError("self loops are not allowed")
    return (min(left, right), max(left, right))


def _validate_transport_graph(
    vertex_count: int,
    transports: dict[Edge, np.ndarray],
    tree_edges: tuple[Edge, ...],
    tolerance: float,
) -> tuple[dict[Edge, np.ndarray], tuple[Edge, ...], int]:
    if vertex_count < 2:
        raise ValueError("at least two vertices are required")
    canonical: dict[Edge, np.ndarray] = {}
    dimensions = set()
    for raw_edge, transport in transports.items():
        edge = _canonical_edge(raw_edge)
        if raw_edge != edge:
            transport = transport.conj().T
        if edge in canonical:
            raise ValueError("duplicate transport edge")
        if not 0 <= edge[0] < edge[1] < vertex_count:
            raise ValueError("edge endpoint out of range")
        if transport.ndim != 2 or transport.shape[0] != transport.shape[1]:
            raise ValueError("edge transports must be square")
        identity = np.eye(transport.shape[0])
        if np.linalg.norm(transport.conj().T @ transport - identity, ord=2) > tolerance:
            raise ValueError("edge transports must be unitary")
        canonical[edge] = transport
        dimensions.add(transport.shape[0])
    if len(dimensions) != 1:
        raise ValueError("all fibers must have the same dimension")
    tree = tuple(_canonical_edge(edge) for edge in tree_edges)
    if len(set(tree)) != len(tree) or any(edge not in canonical for edge in tree):
        raise ValueError("tree edges must be distinct graph edges")
    if len(tree) != vertex_count - 1:
        raise ValueError("a spanning tree must have vertex_count-1 edges")
    return canonical, tree, dimensions.pop()


def tree_root_transports(
    vertex_count: int,
    transports: dict[Edge, np.ndarray],
    tree_edges: tuple[Edge, ...],
    *,
    root: int = 0,
    tolerance: float = 1e-9,
) -> tuple[dict[int, np.ndarray], float]:
    canonical, tree, dimension = _validate_transport_graph(
        vertex_count,
        transports,
        tree_edges,
        tolerance,
    )
    if not 0 <= root < vertex_count:
        raise ValueError("root out of range")
    adjacency: dict[int, list[tuple[int, np.ndarray]]] = {
        vertex: [] for vertex in range(vertex_count)
    }
    for low, high in tree:
        forward = canonical[(low, high)]
        adjacency[low].append((high, forward))
        adjacency[high].append((low, forward.conj().T))
    root_maps = {root: np.eye(dimension, dtype=complex)}
    queue = deque([root])
    while queue:
        vertex = queue.popleft()
        for neighbor, step in adjacency[vertex]:
            if neighbor in root_maps:
                continue
            root_maps[neighbor] = step @ root_maps[vertex]
            queue.append(neighbor)
    if len(root_maps) != vertex_count:
        raise ValueError("tree edges are disconnected")
    residual = 0.0
    for low, high in tree:
        residual = max(
            residual,
            float(
                np.linalg.norm(
                    root_maps[high] - canonical[(low, high)] @ root_maps[low],
                    ord=2,
                )
            ),
        )
    return root_maps, residual


def fundamental_holonomies(
    vertex_count: int,
    transports: dict[Edge, np.ndarray],
    tree_edges: tuple[Edge, ...],
    *,
    root: int = 0,
    tolerance: float = 1e-9,
) -> tuple[tuple[np.ndarray, ...], float]:
    canonical, tree, _ = _validate_transport_graph(
        vertex_count,
        transports,
        tree_edges,
        tolerance,
    )
    root_maps, residual = tree_root_transports(
        vertex_count,
        canonical,
        tree,
        root=root,
        tolerance=tolerance,
    )
    tree_set = set(tree)
    holonomies = tuple(
        root_maps[high].conj().T @ transport @ root_maps[low]
        for (low, high), transport in sorted(canonical.items())
        if (low, high) not in tree_set
    )
    return holonomies, residual


def connection_incidence(
    vertex_count: int,
    transports: dict[Edge, np.ndarray],
) -> np.ndarray:
    if not transports:
        raise ValueError("at least one edge is required")
    canonical = {
        _canonical_edge(edge): (
            transport if edge == _canonical_edge(edge) else transport.conj().T
        )
        for edge, transport in transports.items()
    }
    dimension = next(iter(canonical.values())).shape[0]
    incidence = np.zeros(
        (len(canonical) * dimension, vertex_count * dimension),
        dtype=complex,
    )
    for edge_index, ((low, high), transport) in enumerate(sorted(canonical.items())):
        row = slice(edge_index * dimension, (edge_index + 1) * dimension)
        incidence[row, low * dimension : (low + 1) * dimension] = -transport
        incidence[row, high * dimension : (high + 1) * dimension] = np.eye(dimension)
    return incidence


def fixed_space_hamiltonian(holonomies: tuple[np.ndarray, ...]) -> np.ndarray:
    if not holonomies:
        raise ValueError("at least one holonomy generator is required")
    dimension = holonomies[0].shape[0]
    identity = np.eye(dimension, dtype=complex)
    hamiltonian = sum(
        (
            (identity - holonomy).conj().T @ (identity - holonomy) / 4
            for holonomy in holonomies
        ),
        np.zeros((dimension, dimension), dtype=complex),
    ) / len(holonomies)
    return (hamiltonian + hamiltonian.conj().T) / 2


def _kernel_dimension(matrix: np.ndarray, tolerance: float) -> int:
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    return matrix.shape[1] - int(np.count_nonzero(singular_values > tolerance))


def _minimum_positive_eigenvalue(
    matrix: np.ndarray,
    tolerance: float,
) -> float | None:
    eigenvalues = np.linalg.eigvalsh((matrix + matrix.conj().T) / 2)
    positive = eigenvalues[eigenvalues > tolerance]
    return float(positive[0]) if len(positive) else None


def audit_holonomy_fixed_space_reduction(
    control_id: str,
    vertex_count: int,
    transports: dict[Edge, np.ndarray],
    tree_edges: tuple[Edge, ...],
    *,
    tolerance: float = 1e-8,
) -> HolonomyFixedSpaceControl:
    canonical, tree, dimension = _validate_transport_graph(
        vertex_count,
        transports,
        tree_edges,
        tolerance,
    )
    holonomies, tree_residual = fundamental_holonomies(
        vertex_count,
        canonical,
        tree,
        tolerance=tolerance,
    )
    incidence = connection_incidence(vertex_count, canonical)
    connection_laplacian = incidence.conj().T @ incidence
    if holonomies:
        fixed_hamiltonian = fixed_space_hamiltonian(holonomies)
        fixed_dimension = _kernel_dimension(fixed_hamiltonian, tolerance)
        fixed_gap = _minimum_positive_eigenvalue(fixed_hamiltonian, tolerance)
    else:
        fixed_hamiltonian = np.zeros((dimension, dimension), dtype=complex)
        fixed_dimension = dimension
        fixed_gap = None
    connection_dimension = _kernel_dimension(incidence, tolerance)
    residual = connection_dimension - fixed_dimension
    verified = residual == 0 and tree_residual <= 100 * tolerance
    return HolonomyFixedSpaceControl(
        control_id=control_id,
        vertex_count=vertex_count,
        edge_count=len(canonical),
        fiber_dimension=dimension,
        spanning_tree_edge_count=len(tree),
        fundamental_cycle_count=len(holonomies),
        connection_kernel_dimension=connection_dimension,
        holonomy_fixed_space_dimension=fixed_dimension,
        kernel_dimension_residual=residual,
        minimum_positive_connection_laplacian_eigenvalue=(
            _minimum_positive_eigenvalue(connection_laplacian, tolerance)
        ),
        minimum_positive_fixed_space_hamiltonian_eigenvalue=fixed_gap,
        maximum_tree_edge_constraint_residual=tree_residual,
        exact_holonomy_fixed_space_reduction_verified=verified,
        status=(
            "exact-connection-kernel-holonomy-fixed-space-reduction"
            if verified
            else "holonomy-fixed-space-reduction-control-failure"
        ),
    )


def near_flat_holonomy_counterexample(
    exponent: int,
) -> NearFlatHolonomyCounterexample:
    if exponent < 1:
        raise ValueError("exponent must be positive")
    angle = 2.0**-exponent
    holonomy = rotation(angle)
    hamiltonian = fixed_space_hamiltonian((holonomy,))
    gap = _minimum_positive_eigenvalue(hamiltonian, 1e-300)
    if gap is None:
        raise ArithmeticError("nontrivial rotation must have a positive gap")
    return NearFlatHolonomyCounterexample(
        exponent=exponent,
        rotation_angle=angle,
        edge_transport_gate_description_size=exponent + 1,
        fixed_space_dimension=0,
        fixed_space_hamiltonian_gap=gap,
        inverse_gap_log2=-math.log2(gap),
        pair_transport_is_exact_unitary=True,
        inverse_polynomial_gap_guaranteed=False,
        status="efficient-edge-transport-exponentially-small-holonomy-gap",
    )


def gpe_holonomy_scaling_record(n: int) -> GpeHolonomyResolverScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    return GpeHolonomyResolverScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        orientation_label_qubit_count=copies,
        gpe_pair_polar_per_edge_polynomial=True,
        cycle_holonomy_circuit_polynomial_given_short_paths=True,
        coherent_generator_select_proved=False,
        inverse_polynomial_fixed_space_gap_proved=False,
        partial_support_reduction_proved=False,
        emergent_dependency_reduction_proved=False,
        complete_relative_frame_resolver_proved=False,
        status="pair-holonomies-executable-natural-gap-and-coverage-open",
    )


def _finite_controls() -> list[HolonomyFixedSpaceControl]:
    first = rotation(0.17)
    second = rotation(-0.31)
    flat_chord = second @ first
    frustrated_chord = rotation(0.43) @ flat_chord
    partial_first = np.eye(3, dtype=complex)
    partial_second = np.eye(3, dtype=complex)
    partial_chord = np.zeros((3, 3), dtype=complex)
    partial_chord[0, 0] = 1
    partial_chord[1:, 1:] = rotation(0.71)
    tree = ((0, 1), (1, 2))
    return [
        audit_holonomy_fixed_space_reduction(
            "flat-two-dimensional-triangle",
            3,
            {(0, 1): first, (1, 2): second, (0, 2): flat_chord},
            tree,
        ),
        audit_holonomy_fixed_space_reduction(
            "frustrated-two-dimensional-triangle",
            3,
            {
                (0, 1): first,
                (1, 2): second,
                (0, 2): frustrated_chord,
            },
            tree,
        ),
        audit_holonomy_fixed_space_reduction(
            "one-dimensional-fixed-channel",
            3,
            {
                (0, 1): partial_first,
                (1, 2): partial_second,
                (0, 2): partial_chord,
            },
            tree,
        ),
    ]


def run_gpe_holonomy_resolver_reduction(
) -> GpeHolonomyResolverReductionReport:
    controls = _finite_controls()
    counterexamples = [
        near_flat_holonomy_counterexample(exponent)
        for exponent in (4, 8, 12, 16, 20)
    ]
    scaling = [
        gpe_holonomy_scaling_record(n)
        for n in (8, 16, 32, 64, 128, 256, 512)
    ]
    failures = sum(
        not row.exact_holonomy_fixed_space_reduction_verified
        for row in controls
    )
    inverse_gap_growth = all(
        right.inverse_gap_log2 > left.inverse_gap_log2
        for left, right in zip(counterexamples, counterexamples[1:])
    )
    verified = failures == 0
    return GpeHolonomyResolverReductionReport(
        created_at=utc_now(),
        theorem_contract={
            "tree_gauge": (
                "A spanning tree identifies every vertex fiber with one root "
                "fiber by executable products of pair-polar transports."
            ),
            "fundamental_holonomies": (
                "Every non-tree edge becomes H_e=T_v^*U_(v<-u)T_u on the root "
                "fiber, and covariantly constant sections are exactly the "
                "simultaneous +1 eigenspace of all H_e."
            ),
            "connection_kernel": (
                "The connection-incidence kernel and the holonomy fixed space "
                "have equal dimension, with an explicit isometry given by tree "
                "transport."
            ),
            "coherent_resolver_condition": (
                "If the holonomy generators have coherent SELECT and their "
                "averaged frustration Hamiltonian has inverse-polynomial gap, "
                "phase/singular-value filtering yields a polynomial resolver."
            ),
            "scope_exclusion": (
                "The reduction assumes one flat equal-rank carrier channel. It "
                "does not cover partial support traffic, emergent child-span "
                "relations, or complete relative-frame whitening."
            ),
        },
        finite_controls=controls,
        near_flat_counterexamples=counterexamples,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "compile_pair_transport_without_dense_racah_matrices",
                "resolved": True,
                "resolution": (
                    "The companion GPE theorem compiles every edge polar; cycle "
                    "products are executable even when their multiplicity-space "
                    "matrices are not classically materialized."
                ),
            },
            {
                "obligation": "reduce_flat_connection_kernel_to_holonomy_fixed_space",
                "resolved": verified,
                "resolution": (
                    "Spanning-tree gauge fixing proves the equivalence exactly; "
                    "flat, frustrated, and partially fixed controls agree."
                ),
            },
            {
                "obligation": "natural_polynomial_holonomy_generator_and_gap_theorem",
                "resolved": False,
                "resolution": (
                    "Need a coherently selectable short generator family and an "
                    "inverse-polynomial gap on positive native PGM mass."
                ),
            },
            {
                "obligation": "extend_from_flat_pair_channels_to_recursive_child_spans",
                "resolved": False,
                "resolution": (
                    "Pair-generated common sections do not exhaust emergent "
                    "dependencies or the recursively complete child-span cokernel."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Canonical GPE row swaps force all cycle holonomies to identity.",
                "resolved": True,
                "resolution": (
                    "Different edges use different tensor-block decompositions; "
                    "their composition is the nontrivial Racah operator."
                ),
            },
            {
                "objection": "Dense multiplicity matrices make holonomy circuits intractable.",
                "resolved": True,
                "resolution": (
                    "Each holonomy is a product of GPE edge circuits, so it is "
                    "implicit and executable without dense matrix entries."
                ),
            },
            {
                "objection": "Efficient holonomy circuits imply efficient fixed-space projection.",
                "resolved": True,
                "resolution": (
                    "The near-flat rotation family has succinct exact edge "
                    "unitaries but exponentially small frustration gap."
                ),
            },
            {
                "objection": "Fundamental-cycle resolution handles every hierarchy relation.",
                "resolved": False,
                "resolution": (
                    "It handles flat pair-transport sections. Existing finite "
                    "audits contain emergent child-span dependencies not generated "
                    "by leaf pair intersections."
                ),
            },
        ],
        literature_links=[
            {
                "id": "ARXIV-QUANT-PH-0407082",
                "url": "https://arxiv.org/abs/quant-ph/0407082",
                "use": "Coherent GPE carrier-row access used by every edge circuit.",
                "supports_natural_holonomy_gap": False,
            },
            {
                "id": "ARXIV-QUANT-PH-0612107",
                "url": "https://arxiv.org/abs/quant-ph/0612107",
                "use": "Clebsch-Gordan transforms as efficient HSP measurement primitives.",
                "supports_natural_holonomy_gap": False,
            },
        ],
        headline_metrics={
            "connection_kernel_holonomy_reduction_theorem_count": int(verified),
            "finite_holonomy_control_count": len(controls),
            "finite_holonomy_control_failure_count": failures,
            "implicit_dense_racah_circuit_compiler_count": 1,
            "near_flat_gap_counterexample_count": len(counterexamples),
            "near_flat_inverse_gap_growth_verified_count": int(inverse_gap_growth),
            "natural_inverse_polynomial_holonomy_gap_theorem_count": 0,
            "recursive_child_span_holonomy_reduction_theorem_count": 0,
            "complete_relative_frame_resolver_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "pair_racah_holonomies_implicitly_executable": True,
            "flat_connection_kernel_equals_holonomy_fixed_space_proved": verified,
            "polynomial_resolver_conditional_on_select_and_gap": verified,
            "natural_coherent_holonomy_generator_select_proved": False,
            "natural_inverse_polynomial_holonomy_gap_proved": False,
            "partial_support_and_emergent_dependencies_resolved": False,
            "complete_higher_order_relative_polar_proved": False,
            "hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Dense pair-level Racah matrices are no longer an implementation "
                "barrier, but a natural fixed-space gap and coverage theorem is "
                "required before holonomy filtering becomes a decoder primitive."
            ),
        },
        status=(
            "gpe-holonomy-fixed-space-reduction-proved-natural-gap-open"
            if verified and inverse_gap_growth
            else "gpe-holonomy-reduction-control-failure"
        ),
        summary=(
            "Reduced flat higher-order carrier consistency to simultaneous fixed "
            "spaces of executable GPE holonomies and isolated the natural "
            "holonomy-gap theorem as the remaining circuit bottleneck."
        ),
        falsifiers_triggered=[
            (
                "Canonical pair transport does not trivialize cycles because each "
                "edge uses a different tensor-block decomposition."
            ),
            (
                "Dense Racah matrices need not be computed classically to run or "
                "phase-estimate their cycle products."
            ),
            (
                "Efficient edge circuits alone do not imply efficient common-"
                "section projection; the holonomy frustration gap can be tiny."
            ),
        ],
    )


def write_gpe_holonomy_resolver_reduction_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_gpe_holonomy_resolver_reduction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_gpe_holonomy_resolver_reduction_report()
    print(json.dumps(report, indent=2, sort_keys=True))
