"""Relative-rank and natural-mass theorem for component nonscalarity defects.

For a POVM ``{H_e}`` on an ``r``-dimensional fiber, put

    h_e = Tr(H_e)/r,
    D = sum_e (H_e-h_e I)^2.                                (1)

The positive-edge bridge proves a spectral gap for ``D`` when every component
has a retained minimum positive eigenvalue.  A gap is not needed to control
the *central support* of ``D``.  Since (1) is a sum of positive operators,

    ker D = intersection_e ker(H_e-h_e I).                 (2)

For every positive-trace outcome, ``h_e>0`` and a vector in (2) is a nonzero-
eigenvalue vector of ``H_e``.  Hence

    ker D subseteq range(H_e),
    nullity(D) <= min_(h_e>0) rank(H_e),
    rank(D) >= r - min_(h_e>0) rank(H_e).                  (3)

If ``H_e=W^*P_eW`` is a coordinate-compression component effect and the
coordinate block has dimension ``b_e``, then ``rank(H_e)<=b_e``.  Therefore

    rank(D)/r >= 1-b_max/r.                                (4)

The companion natural final-root theorem proves, on globally distinct source
mass at least ``1/9-o(1)``,

    r/D_phys >= 19/128-o(1),
    b_max/r <= (520/19+o(1))/q,                            (5)

where ``q`` is the number of child orientation components.  Combining (4)-(5)
gives

    rank(D)/r >= 1-(520/19+o(1))/q,                        (6)

and conditional expected physical defect-support mass at least

    (1/9)(19/128)-o(1) = 19/1152-o(1).                    (7)

Thus matrix nonscalarity occurs on constant natural source mass and occupies
constant physical mass, with asymptotically full relative rank inside the
common fiber.  This resolves the center-valued *support/mass* gate without a
natural positive component edge.

It does not resolve circuit cost.  The nonzero eigenvalues of ``D`` and the
component effects may still be arbitrarily small.  Coherent square-root
preparation, support SELECT, tightly normalized pseudoinverse access, and any
MRS or speedup claim remain open.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_final_root_natural_common_span import (
    asymptotic_final_root_corollary,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_defect_rank_mass.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEFECT-RANK-MASS"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ComponentDefectRankControl:
    control_id: str
    fiber_dimension: int
    outcome_count: int
    positive_trace_outcome_count: int
    component_ranks: tuple[int, ...]
    minimum_positive_trace_component_rank: int
    maximum_component_rank: int
    observed_defect_rank: int
    observed_defect_nullity: int
    theorem_defect_rank_lower_bound: int
    coordinate_block_defect_rank_lower_bound: int | None
    effect_sum_identity_residual: float
    defect_kernel_intersection_residual: float
    rank_lower_bound_residual: int
    defect_has_positive_spectral_gap: bool
    exact_defect_rank_bridge_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalDefectRankMassCorollary:
    conditioned_source_event_mass_lower_bound: str
    common_span_relative_carrier_rank_lower_bound: str
    component_block_to_fiber_coefficient: str
    asymptotic_defect_relative_common_fiber_rank_lower_bound: str
    conditioned_expected_physical_defect_support_mass_lower_bound: str
    natural_positive_component_edge_required_for_support_mass: bool
    natural_positive_component_edge_proved: bool
    statement: str


@dataclass(frozen=True)
class DefectRankScalingRecord:
    child_orientation_count_decimal: str
    component_block_to_fiber_upper_bound: float
    defect_relative_common_fiber_rank_lower_bound: float
    physical_defect_support_relative_carrier_lower_bound: float
    conditioned_expected_physical_defect_support_mass_lower_bound: float
    positive_relative_rank_certified: bool
    positive_component_edge_assumed: bool
    status: str


@dataclass(frozen=True)
class ComponentDefectRankMassReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[ComponentDefectRankControl]
    natural_scaling_records: list[DefectRankScalingRecord]
    asymptotic_corollary: NaturalDefectRankMassCorollary
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def audit_component_defect_rank(
    control_id: str,
    effects: tuple[np.ndarray, ...],
    *,
    coordinate_block_dimensions: tuple[int, ...] | None = None,
    tolerance: float = 1e-9,
) -> ComponentDefectRankControl:
    """Verify equations (2)-(4) on an explicit finite POVM."""

    if not effects:
        raise ValueError("at least one component effect is required")
    dimension = effects[0].shape[0]
    if dimension < 1 or any(effect.shape != (dimension, dimension) for effect in effects):
        raise ValueError("component effects must share one positive square fiber")
    if coordinate_block_dimensions is not None:
        if len(coordinate_block_dimensions) != len(effects):
            raise ValueError("one coordinate block dimension per effect is required")
        if any(block < 1 for block in coordinate_block_dimensions):
            raise ValueError("coordinate block dimensions must be positive")
    identity = np.eye(dimension, dtype=complex)
    hermitian_effects = []
    ranks = []
    traces = []
    defect = np.zeros_like(identity)
    for effect in effects:
        hermitian = (effect + effect.conj().T) / 2.0
        values = np.linalg.eigvalsh(hermitian)
        if values[0] < -100 * tolerance or values[-1] > 1 + 100 * tolerance:
            raise ValueError("component is not a valid effect")
        rank = int(np.sum(values > 100 * tolerance))
        trace = float(np.trace(hermitian).real / dimension)
        shifted = hermitian - trace * identity
        hermitian_effects.append(hermitian)
        ranks.append(rank)
        traces.append(trace)
        defect += shifted @ shifted
    stacked_constraints = np.vstack(
        [effect - trace * identity for effect, trace in zip(hermitian_effects, traces)]
    )
    intersection_nullity = dimension - int(
        np.linalg.matrix_rank(stacked_constraints, tol=100 * tolerance)
    )
    defect_values = np.linalg.eigvalsh((defect + defect.conj().T) / 2.0)
    defect_rank = int(np.sum(defect_values > 1000 * tolerance))
    defect_nullity = dimension - defect_rank
    positive_indices = [index for index, trace in enumerate(traces) if trace > 100 * tolerance]
    if not positive_indices:
        raise ValueError("a POVM must have a positive-trace component")
    minimum_positive_rank = min(ranks[index] for index in positive_indices)
    theorem_lower = dimension - minimum_positive_rank
    coordinate_lower = None
    if coordinate_block_dimensions is not None:
        for rank, block in zip(ranks, coordinate_block_dimensions):
            if rank > block:
                raise ValueError("effect rank exceeds its coordinate block dimension")
        coordinate_lower = dimension - max(coordinate_block_dimensions)
    sum_residual = float(
        np.linalg.norm(
            sum(hermitian_effects, np.zeros_like(identity)) - identity,
            ord=2,
        )
    )
    kernel_residual = abs(defect_nullity - intersection_nullity)
    rank_residual = max(0, theorem_lower - defect_rank)
    verified = bool(
        sum_residual <= 1000 * tolerance
        and kernel_residual == 0
        and rank_residual == 0
        and (coordinate_lower is None or defect_rank >= coordinate_lower)
    )
    positive_gap = bool(defect_rank == dimension and defect_values[0] > 1000 * tolerance)
    return ComponentDefectRankControl(
        control_id=control_id,
        fiber_dimension=dimension,
        outcome_count=len(effects),
        positive_trace_outcome_count=len(positive_indices),
        component_ranks=tuple(ranks),
        minimum_positive_trace_component_rank=minimum_positive_rank,
        maximum_component_rank=max(ranks),
        observed_defect_rank=defect_rank,
        observed_defect_nullity=defect_nullity,
        theorem_defect_rank_lower_bound=theorem_lower,
        coordinate_block_defect_rank_lower_bound=coordinate_lower,
        effect_sum_identity_residual=sum_residual,
        defect_kernel_intersection_residual=float(kernel_residual),
        rank_lower_bound_residual=rank_residual,
        defect_has_positive_spectral_gap=positive_gap,
        exact_defect_rank_bridge_verified=verified,
        status=(
            "component-defect-relative-rank-bridge-verified"
            if verified
            else "component-defect-relative-rank-bridge-failure"
        ),
    )


def natural_defect_rank_scaling_record(
    child_orientation_count: int,
) -> DefectRankScalingRecord:
    if child_orientation_count < 32:
        raise ValueError("natural asymptotic record requires at least 32 components")
    event_mass = Fraction(1, 9)
    common_rank = Fraction(19, 128)
    block_coefficient = Fraction(520, 19)
    block_ratio = block_coefficient / child_orientation_count
    defect_relative = 1 - block_ratio
    physical = common_rank * defect_relative
    expected = event_mass * physical
    return DefectRankScalingRecord(
        child_orientation_count_decimal=str(child_orientation_count),
        component_block_to_fiber_upper_bound=float(block_ratio),
        defect_relative_common_fiber_rank_lower_bound=float(defect_relative),
        physical_defect_support_relative_carrier_lower_bound=float(physical),
        conditioned_expected_physical_defect_support_mass_lower_bound=float(expected),
        positive_relative_rank_certified=defect_relative > 0,
        positive_component_edge_assumed=False,
        status="natural-component-defect-asymptotically-full-relative-rank",
    )


def natural_defect_rank_mass_corollary() -> NaturalDefectRankMassCorollary:
    source_mass = Fraction(1, 9)
    common_rank = Fraction(19, 128)
    block_coefficient = Fraction(520, 19)
    physical_mass = source_mass * common_rank
    companion = asymptotic_final_root_corollary()
    if Fraction(companion.conditioned_event_mass_lower_bound) != source_mass:
        raise ArithmeticError("source-event constant disagrees with companion theorem")
    if Fraction(companion.common_span_relative_rank_lower_bound) != common_rank:
        raise ArithmeticError("common-span constant disagrees with companion theorem")
    if Fraction(companion.maximum_component_block_to_fiber_coefficient) != block_coefficient:
        raise ArithmeticError("block-ratio constant disagrees with companion theorem")
    return NaturalDefectRankMassCorollary(
        conditioned_source_event_mass_lower_bound=str(source_mass),
        common_span_relative_carrier_rank_lower_bound=str(common_rank),
        component_block_to_fiber_coefficient=str(block_coefficient),
        asymptotic_defect_relative_common_fiber_rank_lower_bound="1-o(1)",
        conditioned_expected_physical_defect_support_mass_lower_bound=str(physical_mass),
        natural_positive_component_edge_required_for_support_mass=False,
        natural_positive_component_edge_proved=False,
        statement=(
            "On globally distinct conditional source mass at least 1/9-o(1), "
            "the final component nonscalarity defect has relative common-fiber "
            "rank at least 1-(520/19+o(1))/q. Its conditioned expected physical "
            "support mass is at least 19/1152-o(1)."
        ),
    )


def _projective_povm(outcomes: int, rank_per_outcome: int) -> tuple[np.ndarray, ...]:
    dimension = outcomes * rank_per_outcome
    effects = []
    for outcome in range(outcomes):
        effect = np.zeros((dimension, dimension), dtype=complex)
        start = outcome * rank_per_outcome
        effect[start : start + rank_per_outcome, start : start + rank_per_outcome] = np.eye(
            rank_per_outcome
        )
        effects.append(effect)
    return tuple(effects)


def _trine_povm() -> tuple[np.ndarray, ...]:
    effects = []
    for index in range(3):
        angle = 2 * np.pi * index / 3
        vector = np.asarray([[np.cos(angle)], [np.sin(angle)]], dtype=complex)
        effects.append((2 / 3) * vector @ vector.conj().T)
    return tuple(effects)


def _kernel_control_povm() -> tuple[np.ndarray, ...]:
    first = np.diag([0.5, 1.0, 0.0]).astype(complex)
    return first, np.eye(3, dtype=complex) - first


def run_component_defect_rank_mass() -> ComponentDefectRankMassReport:
    controls = [
        audit_component_defect_rank(
            "FOUR-RANK2-ORTHOGONAL-COMPONENTS",
            _projective_povm(4, 2),
            coordinate_block_dimensions=(2, 2, 2, 2),
        ),
        audit_component_defect_rank(
            "TRINE-RANK1-COMPONENTS",
            _trine_povm(),
            coordinate_block_dimensions=(1, 1, 1),
        ),
        audit_component_defect_rank(
            "BINARY-COMMON-MEAN-EIGENVECTOR",
            _kernel_control_povm(),
            coordinate_block_dimensions=(2, 2),
        ),
    ]
    scaling = [
        natural_defect_rank_scaling_record(1 << exponent)
        for exponent in (5, 8, 12, 16, 20, 24)
    ]
    corollary = natural_defect_rank_mass_corollary()
    failures = sum(not row.exact_defect_rank_bridge_verified for row in controls)
    kernel_controls = sum(row.observed_defect_nullity > 0 for row in controls)
    exact = failures == 0
    tail = scaling[-1]
    return ComponentDefectRankMassReport(
        created_at=utc_now(),
        theorem_contract={
            "kernel_identity": (
                "For D=sum_e(H_e-h_e I)^2, ker D is exactly the intersection "
                "of the kernels of H_e-h_e I."
            ),
            "positive_trace_support_bound": (
                "If h_e>0, every defect-kernel vector is a nonzero-eigenvalue "
                "vector of H_e, so nullity(D)<=rank(H_e)."
            ),
            "coordinate_rank_corollary": (
                "For H_e=W^*P_eW with coordinate block dimension b_e, "
                "rank(D)/r>=1-b_max/r."
            ),
            "natural_final_root_mass": (
                "The natural final-root common-span theorem gives source event "
                "mass 1/9-o(1), r/D_phys>=19/128-o(1), and "
                "b_max/r<=(520/19+o(1))/q."
            ),
            "natural_defect_support": (
                "Consequently rank(D)/r=1-o(1) and conditioned expected physical "
                "defect-support mass is at least 19/1152-o(1)."
            ),
            "scope": (
                "This is a rank/support theorem. It supplies no lower bound on "
                "nonzero defect or component eigenvalues and no coherent circuit."
            ),
        },
        finite_controls=controls,
        natural_scaling_records=scaling,
        asymptotic_corollary=corollary,
        proof_obligations=[
            {
                "obligation": "prove_center_valued_natural_component_nonscalarity_mass",
                "resolved": True,
                "resolution": "The defect-kernel support inclusion plus natural b_max/r=O(1/q) makes the defect asymptotically full rank on source mass 1/9-o(1), with expected physical support mass at least 19/1152-o(1).",
            },
            {
                "obligation": "avoid_using_scalar_defect_trace_to_infer_source_probability",
                "resolved": True,
                "resolution": "The proof is blockwise and rank-valued. It never converts a small ordinary trace moment into a central-support claim.",
            },
            {
                "obligation": "bound_natural_positive_component_or_defect_edge",
                "resolved": False,
                "resolution": "Relative rank permits arbitrarily small nonzero eigenvalues. A direct structured dilation, trace-weighted trim, or positive-edge theorem is still required for implementation.",
            },
            {
                "obligation": "separate_physical_pgm_effect_from_all_mrs_transcript_postprocessings",
                "resolved": False,
                "resolution": "Component nonscalarity on positive mass is a necessary structural input, not an all-policy MRS separation witness.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "A tiny ordinary defect trace means matrix effects occur on negligible source mass.",
                "resolved": True,
                "resolution": "False. Defect rank is controlled blockwise by component support ranks and is asymptotically full on a constant-probability source event."
            },
            {
                "objection": "One low-rank positive-trace effect can coexist with a large defect kernel outside its support.",
                "resolved": True,
                "resolution": "Impossible: every defect-kernel vector must satisfy H_e v=h_e v with h_e>0 and therefore lies in that effect's range."
            },
            {
                "objection": "Asymptotically full defect rank implies a constant defect gap.",
                "resolved": False,
                "resolution": "No. The nonzero defect eigenvalues can approach zero arbitrarily quickly; rank and spectral conditioning are separate."
            },
            {
                "objection": "Positive-mass component nonscalarity proves an MRS lower-bound escape.",
                "resolved": False,
                "resolution": "No. The pulled-back physical decision effect still must be separated from every allowed adaptive transcript postprocessing."
            },
        ],
        headline_metrics={
            "component_defect_relative_rank_bridge_theorem_count": int(exact),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "finite_nontrivial_defect_kernel_control_count": kernel_controls,
            "natural_component_defect_positive_source_mass_theorem_count": 1,
            "natural_component_defect_asymptotically_full_common_rank_theorem_count": 1,
            "asymptotic_conditioned_source_event_mass_lower_bound": float(Fraction(1, 9)),
            "asymptotic_conditioned_physical_defect_support_mass_lower_bound": float(Fraction(19, 1152)),
            "tail_component_count": int(tail.child_orientation_count_decimal),
            "tail_defect_relative_common_rank_lower_bound": tail.defect_relative_common_fiber_rank_lower_bound,
            "natural_positive_component_edge_theorem_count": 0,
            "physical_mrs_separation_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "center_valued_natural_component_nonscalarity_source_mass_controlled": True,
            "natural_component_defect_has_asymptotically_full_relative_common_rank": True,
            "natural_component_defect_has_constant_physical_support_mass": True,
            "natural_positive_component_edge_required_for_defect_support_mass": False,
            "natural_positive_component_edge_proved": False,
            "coherent_component_povm_dilation_compiled": False,
            "physical_pgm_outside_mrs_transcript_postprocessing_proved": False,
            "recursive_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Natural matrix-component nonscalarity now has constant source "
                "and physical support mass, but spectral conditioning, coherent "
                "implementation, MRS separation, and decoding remain open."
            ),
        },
        status=(
            "natural-component-defect-rank-and-mass-proved-spectral-edge-open"
            if exact
            else "component-defect-rank-mass-control-failure"
        ),
        summary=(
            "Proved that final-root component nonscalarity occupies asymptotically "
            "full common-fiber rank on constant natural source mass, without a "
            "positive component-edge premise."
        ),
        falsifiers_triggered=[
            "Ordinary scalar defect trace is not needed to control center-valued defect support.",
            "A natural positive component edge is not required to prove positive nonscalarity source or physical mass.",
            "Asymptotically full defect rank does not imply a usable spectral gap.",
            "Positive-mass component nonscalarity is not itself an MRS lower-bound separation.",
        ],
    )


def write_component_defect_rank_mass_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEFECT-RANK-MASS"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_component_defect_rank_mass())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    return payload


if __name__ == "__main__":
    report = write_component_defect_rank_mass_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
