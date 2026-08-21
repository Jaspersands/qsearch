"""A latent master fiber moves, but does not remove, polar normalization cost.

Let ``A=stack_v(E_v)`` be the orientation analysis map, let ``m`` be the
number of orientations, and normalize the available coherent analyzer as

    C=A/sqrt(m),       X=C^*C=F/m,       F=sum_v E_v.

On ``supp(F)``, introduce a latent master fiber and the graph map

    G_(a,b) = [a I; b C].                                 (1)

Its polar is explicit:

    J_(a,b)=G_(a,b)(a^2 I+b^2 X)^(-1/2).                  (2)

The identity block can make (2) constant-conditioned, but the orientation
branch then has squared amplitude

    p(x)=b^2 x/(a^2+b^2 x)                                (3)

on an ``X`` eigenvalue ``x``.  Conditional orientation output is the desired
analysis polar only after the spectral gain

    q_flat(x)=sqrt(a^2+b^2 x)/(b sqrt(x)).                 (4)

With the natural flagged block-encoding normalization
``alpha=sqrt(a^2+b^2)``, the graph-polar threshold cost at the smallest
occupied eigenvalue ``x_min`` is

    q_graph=alpha/sqrt(a^2+b^2 x_min).

Therefore

    q_graph q_flat(x_min)=alpha/(b sqrt(x_min))
                         >=1/sqrt(x_min).                  (5)

At ``a=0`` all cost sits in polarizing ``C``.  At large ``a`` the graph polar
is easy and all cost sits in flattening/postselection.  No master weight
improves the generic normalized-analyzer query exponent.

This is an access-model theorem, not an arbitrary-circuit lower bound.  Pair
GPE already shows that representation-specific reassociation can bypass a
small scalar singular value.  A direct rectangular CS transform, structured
singular-vector pairing, or another non-black-box use of the group action
remains open.  No complete polar, decoder, classical separation, or speedup
is claimed.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_orientation_fourier_reduction import (
    orientation_invariant_projector,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_latent_master_polar_tradeoff.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-LATENT-MASTER-POLAR-TRADEOFF"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class LatentMasterTradeoffControl:
    control_id: str
    n: int
    target_partition: Partition
    labels: tuple[Label, ...]
    orientation_count: int
    frame_support_rank: int
    master_weight: float
    analyzer_weight: float
    minimum_normalized_frame_eigenvalue: float
    maximum_normalized_frame_eigenvalue: float
    flagged_access_normalization: float
    minimum_normalized_graph_singular_value: float
    graph_polar_threshold_scale: float
    minimum_orientation_branch_probability: float
    spectral_flattening_gain: float
    combined_graph_and_flattening_scale: float
    direct_normalized_analyzer_polar_scale: float
    tradeoff_product_identity_residual: float
    graph_polar_formula_residual: float
    flattened_orientation_polar_residual: float
    exact_latent_master_tradeoff_verified: bool
    status: str


@dataclass(frozen=True)
class LatentMasterScalingRecord:
    n: int
    symmetric_group_order_log2: float
    information_threshold_copy_count: int
    flat_benchmark_x_min_log2: float
    best_latent_master_scale_log2_lower_bound: float
    direct_normalized_analyzer_scale_log2: float
    constant_graph_condition_and_constant_output_possible: bool
    master_weight_improves_generic_query_exponent: bool
    representation_specific_direct_bypass_open: bool
    complete_orientation_polar_compiled: bool
    status: str


@dataclass(frozen=True)
class LatentMasterTradeoffTheorem:
    normalized_analyzer: str
    graph_polar: str
    orientation_probability: str
    flattening_gain: str
    product_identity: str
    access_model_scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class LatentMasterTradeoffReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: LatentMasterTradeoffTheorem
    finite_controls: list[LatentMasterTradeoffControl]
    scaling_records: list[LatentMasterScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _positive_spectral_basis(
    matrix: np.ndarray,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray]:
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2.0)
    active = values > tolerance
    return values[active], vectors[:, active]


def _inverse_square_root(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2.0)
    inverse = np.zeros_like(values)
    inverse[values > tolerance] = 1.0 / np.sqrt(values[values > tolerance])
    return (vectors * inverse) @ vectors.conj().T


def _positive_square_root(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2.0)
    root = np.sqrt(np.maximum(values, 0.0))
    root[values <= tolerance] = 0.0
    return (vectors * root) @ vectors.conj().T


def _polar(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    left, singular_values, right_adjoint = np.linalg.svd(
        matrix,
        full_matrices=False,
    )
    active = singular_values > tolerance
    return left[:, active] @ right_adjoint[active, :]


def audit_latent_master_tradeoff(
    control_id: str,
    target_partition: Partition,
    labels: tuple[Label, ...],
    master_weight: float,
    analyzer_weight: float,
    *,
    tolerance: float = 1e-9,
) -> LatentMasterTradeoffControl:
    if master_weight < 0 or analyzer_weight <= 0:
        raise ValueError("master weight must be nonnegative and analyzer weight positive")
    if not labels:
        raise ValueError("at least one orientation label is required")

    orientation_count = 1 << len(labels)
    projectors = tuple(
        orientation_invariant_projector(target_partition, labels, orientation)
        for orientation in range(orientation_count)
    )
    frame = sum(projectors, np.zeros_like(projectors[0]))
    frame_values, support = _positive_spectral_basis(frame, tolerance)
    if not len(frame_values):
        raise ValueError("the orientation frame has empty support")
    reduced_frame = support.conj().T @ frame @ support
    normalized_frame = reduced_frame / orientation_count
    normalized_values = frame_values / orientation_count

    analysis = np.vstack(projectors) @ support / math.sqrt(orientation_count)
    support_identity = np.eye(support.shape[1], dtype=complex)
    graph = np.vstack(
        (master_weight * support_identity, analyzer_weight * analysis)
    )
    graph_gram = (
        master_weight**2 * support_identity
        + analyzer_weight**2 * normalized_frame
    )
    graph_polar_formula = graph @ _inverse_square_root(graph_gram, tolerance)
    graph_polar_svd = _polar(graph, tolerance)
    graph_polar_residual = float(
        np.linalg.norm(graph_polar_formula - graph_polar_svd, ord=2)
    )

    minimum_x = float(np.min(normalized_values))
    maximum_x = float(np.max(normalized_values))
    access_normalization = math.hypot(master_weight, analyzer_weight)
    minimum_graph_singular = (
        math.sqrt(master_weight**2 + analyzer_weight**2 * minimum_x)
        / access_normalization
    )
    graph_scale = 1.0 / minimum_graph_singular
    minimum_output_probability = (
        analyzer_weight**2 * minimum_x
        / (master_weight**2 + analyzer_weight**2 * minimum_x)
    )
    flattening_gain = 1.0 / math.sqrt(minimum_output_probability)
    combined_scale = graph_scale * flattening_gain
    direct_scale = 1.0 / math.sqrt(minimum_x)
    product_residual = abs(
        combined_scale
        - access_normalization / (analyzer_weight * math.sqrt(minimum_x))
    )

    graph_orientation = graph_polar_formula[support.shape[1] :, :]
    correction = (
        _positive_square_root(graph_gram, tolerance)
        @ _inverse_square_root(normalized_frame, tolerance)
        / analyzer_weight
    )
    desired_polar = analysis @ _inverse_square_root(normalized_frame, tolerance)
    flattened_residual = float(
        np.linalg.norm(graph_orientation @ correction - desired_polar, ord=2)
    )
    verified = bool(
        graph_polar_residual <= 1000 * tolerance
        and flattened_residual <= 1000 * tolerance
        and product_residual <= 1000 * tolerance
        and combined_scale + 1000 * tolerance >= direct_scale
    )
    return LatentMasterTradeoffControl(
        control_id=control_id,
        n=sum(target_partition),
        target_partition=target_partition,
        labels=labels,
        orientation_count=orientation_count,
        frame_support_rank=support.shape[1],
        master_weight=master_weight,
        analyzer_weight=analyzer_weight,
        minimum_normalized_frame_eigenvalue=minimum_x,
        maximum_normalized_frame_eigenvalue=maximum_x,
        flagged_access_normalization=access_normalization,
        minimum_normalized_graph_singular_value=minimum_graph_singular,
        graph_polar_threshold_scale=graph_scale,
        minimum_orientation_branch_probability=minimum_output_probability,
        spectral_flattening_gain=flattening_gain,
        combined_graph_and_flattening_scale=combined_scale,
        direct_normalized_analyzer_polar_scale=direct_scale,
        tradeoff_product_identity_residual=product_residual,
        graph_polar_formula_residual=graph_polar_residual,
        flattened_orientation_polar_residual=flattened_residual,
        exact_latent_master_tradeoff_verified=verified,
        status=(
            "latent-master-normalization-cost-conservation-verified"
            if verified
            else "latent-master-tradeoff-control-failure"
        ),
    )


def latent_master_scaling_record(n: int) -> LatentMasterScalingRecord:
    if n < 5:
        raise ValueError("n must be at least five")
    order_log2 = math.lgamma(n + 1) / math.log(2)
    copies = math.ceil(order_log2) + 2
    return LatentMasterScalingRecord(
        n=n,
        symmetric_group_order_log2=order_log2,
        information_threshold_copy_count=copies,
        flat_benchmark_x_min_log2=-order_log2,
        best_latent_master_scale_log2_lower_bound=0.5 * order_log2,
        direct_normalized_analyzer_scale_log2=0.5 * order_log2,
        constant_graph_condition_and_constant_output_possible=False,
        master_weight_improves_generic_query_exponent=False,
        representation_specific_direct_bypass_open=True,
        complete_orientation_polar_compiled=False,
        status="latent-master-generic-access-no-bypass-direct-structure-open",
    )


def _finite_controls() -> list[LatentMasterTradeoffControl]:
    families = (
        (
            "S3-TWO-PAIR",
            (2, 1),
            (((3,), (2, 1)), ((2, 1), (1, 1, 1))),
        ),
        (
            "S4-TWO-PAIR",
            (2, 2),
            (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
        ),
        (
            "S5-TWO-PAIR",
            (2, 1, 1, 1),
            (((5,), (4, 1)), ((2, 1, 1, 1), (1, 1, 1, 1, 1))),
        ),
    )
    weights = ((0.0, 1.0), (1.0, 1.0), (0.125, 1.0))
    return [
        audit_latent_master_tradeoff(
            f"{family_id}-A{master:g}-B{analyzer:g}",
            target,
            labels,
            master,
            analyzer,
        )
        for family_id, target, labels in families
        for master, analyzer in weights
    ]


def run_latent_master_polar_tradeoff() -> LatentMasterTradeoffReport:
    controls = _finite_controls()
    scaling = [
        latent_master_scaling_record(n)
        for n in (5, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64, 96, 128)
    ]
    failures = sum(not row.exact_latent_master_tradeoff_verified for row in controls)
    verified = failures == 0
    theorem = LatentMasterTradeoffTheorem(
        normalized_analyzer="C=stack_v(E_v)/sqrt(m), X=C^*C=F/m",
        graph_polar="polar([aI;bC])=[aI;bC](a^2I+b^2X)^(-1/2)",
        orientation_probability="p(x)=b^2x/(a^2+b^2x)",
        flattening_gain="q_flat(x)=sqrt(a^2+b^2x)/(b sqrt(x))",
        product_identity=(
            "q_graph q_flat(x_min)=sqrt(a^2+b^2)/(b sqrt(x_min)) "
            ">=1/sqrt(x_min)"
        ),
        access_model_scope=(
            "applies to flagged identity-plus-normalized-analyzer graph access; "
            "does not lower-bound representation-specific direct transforms"
        ),
        theorem_verified=verified,
        status=(
            "latent-master-polar-normalization-tradeoff-proved"
            if verified
            else "latent-master-polar-tradeoff-control-failure"
        ),
    )
    return LatentMasterTradeoffReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_exact_latent_graph_polar",
                "resolved": verified,
                "resolution": (
                    "The graph Gram is a^2I+b^2X, so its polar and branch "
                    "probabilities follow by functional calculus."
                ),
            },
            {
                "obligation": "test_conditioning_postselection_tradeoff",
                "resolved": verified,
                "resolution": (
                    "The graph threshold scale times the exact spectral "
                    "flattening gain obeys the stated identity on every control."
                ),
            },
            {
                "obligation": "find_representation_specific_rectangular_cs_bypass",
                "resolved": False,
                "resolution": (
                    "Need a normalization-one transform using more than generic "
                    "flagged access to C; pair GPE is only the local precedent."
                ),
            },
            {
                "obligation": "prove_natural_occupied_x_min_bound",
                "resolved": False,
                "resolution": (
                    "The factorial flat row is an access benchmark, not a new "
                    "typical-sector spectral-edge theorem."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A large identity block makes the polar constant-conditioned.",
                "resolved": True,
                "resolution": (
                    "It simultaneously suppresses the orientation branch by "
                    "p(x), moving the inverse-sqrt cost into spectral flattening."
                ),
            },
            {
                "objection": "Set a=0 so no branch amplification is needed.",
                "resolved": True,
                "resolution": (
                    "Then the graph polar is exactly polar(C), whose normalized "
                    "singular threshold is sqrt(x_min)."
                ),
            },
            {
                "objection": "Postselecting the orientation flag always gives W.",
                "resolved": True,
                "resolution": (
                    "Only on one X eigenspace. A superposition is distorted by "
                    "the eigenvalue-dependent probability p(x)."
                ),
            },
            {
                "objection": "This rules out a direct GPE/recoupling circuit.",
                "resolved": True,
                "resolution": (
                    "No. The theorem is restricted to generic normalized analyzer "
                    "and latent-graph access."
                ),
            },
        ],
        headline_metrics={
            "latent_master_tradeoff_theorem_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_graph_polar_formula_residual": max(
                row.graph_polar_formula_residual for row in controls
            ),
            "maximum_flattened_orientation_polar_residual": max(
                row.flattened_orientation_polar_residual for row in controls
            ),
            "maximum_tradeoff_product_identity_residual": max(
                row.tradeoff_product_identity_residual for row in controls
            ),
            "minimum_combined_to_direct_scale_ratio": min(
                row.combined_graph_and_flattening_scale
                / row.direct_normalized_analyzer_polar_scale
                for row in controls
            ),
            "scaling_record_count": len(scaling),
            "generic_latent_master_query_exponent_improvement_count": 0,
            "direct_rectangular_cs_compiler_count": 0,
            "complete_orientation_polar_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "latent_graph_polar_formula_proved": True,
            "conditioning_postselection_product_tradeoff_proved": verified,
            "constant_conditioning_alone_compiles_orientation_polar": False,
            "latent_master_improves_generic_analyzer_query_exponent": False,
            "natural_typical_x_min_bound_proved": False,
            "representation_specific_direct_bypass_rejected": False,
            "direct_rectangular_cs_polar_compiled": False,
            "complete_natural_orientation_polar_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The identity master can regularize the graph or preserve output "
                "amplitude, but the exact product identity prevents doing both "
                "without the original inverse singular scale."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that a latent identity master only redistributes the generic "
            "orientation-polar normalization cost between graph filtering and "
            "spectral flattening."
        ),
        falsifiers_triggered=[
            "Constant graph conditioning does not imply constant orientation-output probability.",
            "Orientation postselection is spectrally biased on superpositions of frame eigenvalues.",
            "No choice of latent-master weight improves the normalized-analyzer inverse-singular exponent.",
        ],
    )


def write_latent_master_polar_tradeoff_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_latent_master_polar_tradeoff())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_latent_master_polar_tradeoff_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
