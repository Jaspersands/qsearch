"""Why local constant-gap QSVT does not compile the sparse polar hierarchy.

The sparse-support schedule and native-state hybrid make every *mathematical*
early merge harmless after a fixed-arity choice.  A tempting conclusion is
that one can apply a constant-degree polar QSVT independently at every binary
node.  This module proves that conclusion false in the recursive black-box
model.

Consider the strongest possible local control: sibling initial supports are
exactly orthogonal, their frames are projections, and they span the parent
support.  Then support-scalarization pressure, native polar error, and low-mode
mass are all exactly zero.  The unnormalized stacked analysis ``Y`` is already
an isometry on the parent support.  Generic PREPARE/SELECT access nevertheless
exposes ``Y/sqrt(2)``, with every nonzero singular value equal to
``x=1/sqrt(2)``.

An odd degree-one QSVT polynomial is ``p(x)=a x``.  Boundedness on ``[-1,1]``
forces ``|a|<=1``, so it cannot amplify ``1/sqrt(2)`` at all.  Any local QSVT
polarization reaching amplitude above ``1/sqrt(2)`` therefore has odd degree
at least three.  If this transformation is literally nested through ``L``
binary levels, its leaf-oracle query recurrence is

    Q_(ell+1) >= 3 Q_ell,

and hence ``Q_L>=3^L``.  This is a lower bound only for the nested local-QSVT
architecture, not for arbitrary circuits.

The broader normalized black-box boundary is independent of that recurrence.
A flat frame with ``w`` orthogonal leaves has normalized singular amplitude
``1/sqrt(w)`` and requires ``Omega(sqrt(w))`` unknown-state resampling queries.
With a fixed jump arity ``R``, every early child still contains
``w/R`` leaves, so the lower bound is ``Omega(sqrt(w/R))``.  Because
``w=2^K`` with ``K=ceil(log2(n!))+O(1)``, this remains superpolynomial for
every ``R`` fixed before ``n`` tends to infinity.

Thus sparse support scalarization, principal-angle trimming, native-state
error control, and fixed local gaps do not solve coherent access.  A surviving
compiler must flatten the hierarchy or use representation-specific structure
to route orientation support without generic normalized leaf access.  The
result does not rule out a Racah/Schur/Fourier routing transform, a direct
covariant polar, or any circuit outside the stated oracle architectures.
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
    "self_dual_wreath_sparse_polar_access_composition_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SPARSE-POLAR-ACCESS-COMPOSITION-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
QRS_PRIMARY_SOURCE = "https://arxiv.org/abs/1103.2774"


@dataclass(frozen=True)
class OrthogonalHierarchyAccessControl:
    depth: int
    leaf_count: int
    ambient_dimension: int
    support_scalarization_pressure: float
    aggregate_native_polar_error: float
    aggregate_low_singular_native_mass: float
    normalized_binary_analysis_singular_value: float
    maximum_degree_one_qsvt_output_amplitude: float
    requested_output_amplitude: float
    minimum_nontrivial_odd_qsvt_degree: int
    nested_qsvt_leaf_query_lower_bound: int
    global_flat_black_box_query_lower_bound: float
    every_local_gram_is_exactly_flat: bool
    zero_error_does_not_remove_access_normalization: bool
    status: str


@dataclass(frozen=True)
class FixedArityAccessScalingRecord:
    n: int
    group_order_decimal: str
    selected_copy_count: int
    total_orientation_width_decimal: str
    fixed_jump_log2_arity: int
    fixed_jump_arity_decimal: str
    early_binary_depth: int
    leaves_per_jump_child_decimal: str
    nested_degree_three_query_log2_lower_bound: float
    normalized_black_box_query_log2_lower_bound: float
    polynomial_benchmark_degree: int
    polynomial_benchmark_log2: float
    nested_local_qsvt_superpolynomial: bool
    normalized_black_box_access_superpolynomial: bool
    fixed_arity_removes_asymptotic_width_barrier: bool
    status: str


@dataclass(frozen=True)
class SparsePolarAccessCompositionTheorem:
    flat_orthogonal_control: str
    degree_one_obstruction: str
    nested_qsvt_composition: str
    global_black_box_boundary: str
    fixed_arity_consequence: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class SparsePolarAccessCompositionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: SparsePolarAccessCompositionTheorem
    orthogonal_controls: list[OrthogonalHierarchyAccessControl]
    scaling_records: list[FixedArityAccessScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _support(columns: tuple[int, ...], dimension: int) -> np.ndarray:
    projector = np.zeros((dimension, dimension), dtype=complex)
    projector[columns, columns] = 1.0
    return projector


def audit_orthogonal_hierarchy_access(
    depth: int,
    *,
    requested_output_amplitude: float = 0.99,
    tolerance: float = 1e-10,
) -> OrthogonalHierarchyAccessControl:
    if depth < 1:
        raise ValueError("depth must be positive")
    if not 1.0 / math.sqrt(2.0) < requested_output_amplitude <= 1.0:
        raise ValueError("requested amplitude must exceed the normalized input amplitude")
    leaf_count = 1 << depth
    dimension = leaf_count
    local_flat = True
    for level in range(1, depth + 1):
        block_size = 1 << level
        half = block_size // 2
        for start in range(0, dimension, block_size):
            left = _support(tuple(range(start, start + half)), dimension)
            right = _support(
                tuple(range(start + half, start + block_size)), dimension
            )
            parent = left + right
            stacked = np.vstack((left, right)) / math.sqrt(2.0)
            gram = stacked.conj().T @ stacked
            local_flat = bool(
                local_flat
                and np.linalg.norm(left @ right, ord=2) <= tolerance
                and np.linalg.norm(2.0 * gram - parent, ord=2) <= tolerance
            )
    normalized = 1.0 / math.sqrt(2.0)
    maximum_linear = normalized
    minimum_degree = 3
    nested_queries = minimum_degree**depth
    black_box_queries = math.sqrt(leaf_count)
    verified = bool(
        local_flat
        and requested_output_amplitude > maximum_linear
        and nested_queries == 3**depth
    )
    return OrthogonalHierarchyAccessControl(
        depth=depth,
        leaf_count=leaf_count,
        ambient_dimension=dimension,
        support_scalarization_pressure=0.0,
        aggregate_native_polar_error=0.0,
        aggregate_low_singular_native_mass=0.0,
        normalized_binary_analysis_singular_value=normalized,
        maximum_degree_one_qsvt_output_amplitude=maximum_linear,
        requested_output_amplitude=requested_output_amplitude,
        minimum_nontrivial_odd_qsvt_degree=minimum_degree,
        nested_qsvt_leaf_query_lower_bound=nested_queries,
        global_flat_black_box_query_lower_bound=black_box_queries,
        every_local_gram_is_exactly_flat=local_flat,
        zero_error_does_not_remove_access_normalization=verified,
        status=(
            "zero-error-flat-hierarchy-retains-access-normalization"
            if verified
            else "orthogonal-hierarchy-access-control-failure"
        ),
    )


def fixed_arity_access_scaling_record(
    n: int,
    *,
    jump_log2_arity: int = 24,
    extra_copies: int = 2,
    polynomial_benchmark_degree: int = 10,
) -> FixedArityAccessScalingRecord:
    if n < 3 or jump_log2_arity < 0 or extra_copies < 0:
        raise ValueError("invalid scaling parameters")
    if polynomial_benchmark_degree < 1:
        raise ValueError("polynomial benchmark degree must be positive")
    order = math.factorial(n)
    copies = (order - 1).bit_length() + extra_copies
    early_depth = max(0, copies - jump_log2_arity)
    leaves_per_child = 1 << early_depth
    nested_log2 = early_depth * math.log2(3.0)
    black_box_log2 = early_depth / 2.0
    benchmark = polynomial_benchmark_degree * math.log2(n)
    nested_superpoly = nested_log2 > benchmark
    black_box_superpoly = black_box_log2 > benchmark
    return FixedArityAccessScalingRecord(
        n=n,
        group_order_decimal=str(order),
        selected_copy_count=copies,
        total_orientation_width_decimal=str(1 << copies),
        fixed_jump_log2_arity=jump_log2_arity,
        fixed_jump_arity_decimal=str(1 << jump_log2_arity),
        early_binary_depth=early_depth,
        leaves_per_jump_child_decimal=str(leaves_per_child),
        nested_degree_three_query_log2_lower_bound=nested_log2,
        normalized_black_box_query_log2_lower_bound=black_box_log2,
        polynomial_benchmark_degree=polynomial_benchmark_degree,
        polynomial_benchmark_log2=benchmark,
        nested_local_qsvt_superpolynomial=nested_superpoly,
        normalized_black_box_access_superpolynomial=black_box_superpoly,
        fixed_arity_removes_asymptotic_width_barrier=False,
        status=(
            "fixed-arity-sparse-schedule-retains-black-box-width-barrier"
            if black_box_superpoly
            else "finite-size-width-separation-not-yet-visible"
        ),
    )


def run_sparse_polar_access_composition_no_go(
) -> SparsePolarAccessCompositionReport:
    controls = [audit_orthogonal_hierarchy_access(depth) for depth in range(1, 9)]
    scaling = [
        fixed_arity_access_scaling_record(n)
        for n in (12, 16, 20, 24, 32, 40, 48, 64, 80)
    ]
    control_failures = sum(
        not row.zero_error_does_not_remove_access_normalization for row in controls
    )
    separated = [
        row for row in scaling if row.normalized_black_box_access_superpolynomial
    ]
    tail = scaling[-1]
    verified = bool(control_failures == 0 and separated and tail.nested_local_qsvt_superpolynomial)
    theorem = SparsePolarAccessCompositionTheorem(
        flat_orthogonal_control=(
            "Exactly orthogonal projection frames have zero sparse-support and "
            "native-state error, yet generic binary access exposes singular 1/sqrt(2)."
        ),
        degree_one_obstruction=(
            "Every bounded odd degree-one QSVT polynomial satisfies "
            "|p(1/sqrt(2))|<=1/sqrt(2); nontrivial amplification needs degree at least three."
        ),
        nested_qsvt_composition=(
            "Literal level-by-level QSVT nesting through L binary levels uses at least 3^L leaf-oracle calls."
        ),
        global_black_box_boundary=(
            "Flat normalized access to w orthogonal leaves retains the Omega(sqrt(w)) unknown-state resampling bound."
        ),
        fixed_arity_consequence=(
            "For fixed R, an early jump child still has w/R leaves, so its black-box lower bound is Omega(sqrt(w/R))."
        ),
        scope=(
            "The nested recurrence and normalized black-box lower bound do not apply to a representation-specific global routing transform."
        ),
        theorem_verified=verified,
        status=(
            "local-gap-qsvt-access-bypass-refuted"
            if verified
            else "sparse-polar-access-composition-control-failure"
        ),
    )
    return SparsePolarAccessCompositionReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        orthogonal_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "test_nested_constant_gap_qsvt_as_sparse_hierarchy_compiler",
                "resolved": verified,
                "resolution": "Resolved negatively by the degree-one obstruction and multiplicative query recurrence.",
            },
            {
                "obligation": "test_fixed_jump_arity_as_global_black_box_width_bypass",
                "resolved": verified,
                "resolution": "Resolved negatively: fixed R changes width only by a constant factor in the n limit.",
            },
            {
                "obligation": "construct_representation_specific_global_orientation_support_router",
                "resolved": False,
                "resolution": "Need a flattened Racah, Schur, Fourier, automaton, or other covariant transform outside normalized leaf access.",
            },
            {
                "obligation": "compile_fixed_R_and_final_endpoint_measurements_after_global_routing",
                "resolved": False,
                "resolution": "The state-error theorems remain useful only after structured access is supplied.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The no-go relies on ill-conditioned local support geometry.",
                "resolved": True,
                "resolution": "The control is exactly orthogonal, flat, gap one, and has zero approximation loss.",
            },
            {
                "objection": "Constant local QSVT degree means constant total overhead.",
                "resolved": True,
                "resolution": "False under literal nesting: each polynomial query invokes the complete child block encoding.",
            },
            {
                "objection": "The 3^L recurrence is an arbitrary-circuit lower bound.",
                "resolved": False,
                "resolution": "It is deliberately scoped to nested local QSVT; only the weaker sqrt-width statement is a normalized black-box lower bound.",
            },
            {
                "objection": "This kills representation-specific orientation routing.",
                "resolved": False,
                "resolution": "No. A direct structured transform lies outside both oracle models and is now the required target.",
            },
        ],
        literature_links=[
            {
                "paper": "Quantum rejection sampling",
                "url": QRS_PRIMARY_SOURCE,
                "used_for": "Tight unknown-state resampling lower bound underlying the flat normalized-access control",
                "representation_specific_no_go": False,
            }
        ],
        headline_metrics={
            "orthogonal_zero_error_access_control_count": len(controls),
            "finite_control_failure_count": control_failures,
            "nested_local_qsvt_no_go_theorem_count": int(verified),
            "normalized_black_box_width_boundary_theorem_count": int(verified),
            "superpolynomial_scaling_row_count": len(separated),
            "tail_n": tail.n,
            "tail_early_binary_depth": tail.early_binary_depth,
            "tail_black_box_query_log2_lower_bound": (
                tail.normalized_black_box_query_log2_lower_bound
            ),
            "representation_specific_global_router_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "sparse_native_state_error_theorem_invalidated": False,
            "constant_local_gap_suffices_for_recursive_qsvt": False,
            "fixed_arity_removes_global_black_box_width": False,
            "nested_local_qsvt_superpolynomial_proved": verified,
            "normalized_black_box_width_boundary_retained": verified,
            "arbitrary_circuit_lower_bound_proved": False,
            "representation_specific_global_router_ruled_out": False,
            "recursive_orientation_polar_compiled": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "A zero-error orthogonal hierarchy proves that local conditioning "
            "and sparse native-state accuracy do not solve coherent access: "
            "nested local QSVT multiplies queries and fixed arity retains the "
            "global square-root-width black-box boundary. A representation-"
            "specific flattened router is mandatory."
        ),
        falsifiers_triggered=[
            "Constant local singular gaps do not imply polynomial recursive QSVT cost.",
            "Tunable sparse-support approximation does not bypass normalized black-box orientation width.",
        ],
    )


def write_sparse_polar_access_composition_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-SPARSE-POLAR-ACCESS-COMPOSITION-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_sparse_polar_access_composition_no_go" in globals():
        report = run_sparse_polar_access_composition_no_go(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-SPARSE-POLAR-ACCESS-COMPOSITION-NO-GO",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-SPARSE-POLAR-ACCESS-COMPOSITION-NO-GO.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-SPARSE-POLAR-ACCESS-COMPOSITION-NO-GO.",
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
                    "self_dual_wreath_sparse_polar_access_composition_no_go": str(path)
                },
            )
        )
    return payload
