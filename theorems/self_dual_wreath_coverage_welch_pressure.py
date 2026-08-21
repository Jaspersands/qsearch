"""Welch-pressure theorem for natural affine-plane coverage.

The support-pressure no-go proves that affine-plane carrier supports must
overlap heavily.  The correct benchmark for that overlap is the fusion-frame
Welch floor, not zero.

Let ``P_a`` be the line-incidence support projectors embedded in the direct
sum of incident pair-core coefficient spaces ``H``, with ``Q=dim(H)``.  Put

    D=sum_a P_a,       T=tr(D)=sum_a rank(P_a),
    R=T/Q.                                                  (1)

The Hilbert--Schmidt Cauchy inequality gives

    tr(D^2) >= T^2/Q = R T.                                (2)

Since ``tr(P_a^2)=rank(P_a)``, equation (2) is equivalent to

    sum_(a!=b) tr(P_a P_b) >= (R-1)T.                      (3)

Thus a large support-pressure ratio *forces* large inter-plane overlap.  A
proof that treats distinct planes as weak perturbations is impossible.

Define the dimensionless excess fusion potential

    epsilon = Q tr(D^2)/T^2 - 1 >= 0.                      (4)

Equality means ``D=RI``, a tight fusion frame.  Moreover

    tr((D-RI)^2)=epsilon R T.                              (5)

For ``0<delta<1``, the fraction of coverage eigenvalues below
``(1-delta)R`` (or above ``(1+delta)R``) is at most

    epsilon/delta^2.                                      (6)

Consequently ``epsilon=o(1)`` is exactly the second-moment theorem needed by
the operator-Steiner bulk reduction.  Raw support demand, raw pairwise
overlap, and cycle holonomy are insufficient substitutes.

The collision-free pressure theorem supplies a divergent lower bound on
``R`` after square-root Markov slack, but supplies no upper bound on
``epsilon``.  This module therefore strengthens the research target without
claiming natural tightness.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_affine_plane_support_pressure_no_go import (
    affine_plane_support_pressure_scaling_record,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_coverage_welch_pressure.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COVERAGE-WELCH-PRESSURE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
FUSION_FRAME_POTENTIAL_URL = "https://arxiv.org/abs/1201.1798"


@dataclass(frozen=True)
class FusionCoverageControl:
    control_id: str
    ambient_dimension: int
    projector_count: int
    total_projector_rank: int
    redundancy: float
    fusion_potential: float
    welch_floor: float
    offdiagonal_fusion_potential: float
    forced_offdiagonal_floor: float
    normalized_excess_fusion_potential: float
    relative_window_delta: float
    observed_low_coverage_fraction: float
    observed_high_coverage_fraction: float
    proved_each_tail_fraction_bound: float
    welch_floor_respected: bool
    coverage_tail_bound_respected: bool
    status: str


@dataclass(frozen=True)
class NaturalCoveragePressureTarget:
    n: int
    copy_count: int
    collision_free_redundancy_lower_bound_log2: float
    forced_offdiagonal_over_trace_lower_bound_log2: float
    raw_overlap_is_perturbative: bool
    natural_excess_fusion_potential_upper_bound: float | None
    natural_tight_fusion_frame_proved: bool
    status: str


@dataclass(frozen=True)
class CoverageWelchPressureReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[FusionCoverageControl]
    natural_scaling_targets: list[NaturalCoveragePressureTarget]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _projector(basis: np.ndarray) -> np.ndarray:
    if basis.ndim != 2:
        raise ValueError("basis must be a matrix")
    residual = np.linalg.norm(basis.T @ basis - np.eye(basis.shape[1]))
    if residual > 1e-8:
        raise ValueError("basis columns must be orthonormal")
    return basis @ basis.T


def audit_fusion_coverage(
    control_id: str,
    projectors: tuple[np.ndarray, ...],
    *,
    delta: float = 0.5,
) -> FusionCoverageControl:
    if not projectors or not 0 < delta < 1:
        raise ValueError("need projectors and delta in (0,1)")
    dimension = projectors[0].shape[0]
    if any(projector.shape != (dimension, dimension) for projector in projectors):
        raise ValueError("projectors must share an ambient dimension")
    coverage = sum(projectors, np.zeros_like(projectors[0]))
    ranks = [int(round(float(np.trace(projector)))) for projector in projectors]
    total_rank = sum(ranks)
    redundancy = total_rank / dimension
    potential = float(np.trace(coverage @ coverage))
    floor = total_rank**2 / dimension
    offdiagonal = potential - total_rank
    forced_offdiagonal = floor - total_rank
    excess = dimension * potential / total_rank**2 - 1
    values = np.linalg.eigvalsh((coverage + coverage.T) / 2)
    low_fraction = float(np.mean(values < (1 - delta) * redundancy - 1e-9))
    high_fraction = float(np.mean(values > (1 + delta) * redundancy + 1e-9))
    tail_bound = excess / delta**2
    welch = potential >= floor - 1e-9
    tails = low_fraction <= tail_bound + 1e-9 and high_fraction <= tail_bound + 1e-9
    return FusionCoverageControl(
        control_id=control_id,
        ambient_dimension=dimension,
        projector_count=len(projectors),
        total_projector_rank=total_rank,
        redundancy=redundancy,
        fusion_potential=potential,
        welch_floor=floor,
        offdiagonal_fusion_potential=offdiagonal,
        forced_offdiagonal_floor=forced_offdiagonal,
        normalized_excess_fusion_potential=excess,
        relative_window_delta=delta,
        observed_low_coverage_fraction=low_fraction,
        observed_high_coverage_fraction=high_fraction,
        proved_each_tail_fraction_bound=tail_bound,
        welch_floor_respected=welch,
        coverage_tail_bound_respected=tails,
        status=(
            "fusion-coverage-welch-and-tail-verified"
            if welch and tails
            else "fusion-coverage-control-failure"
        ),
    )


def _tight_coordinate_projectors(
    dimension: int,
    repetitions: int,
) -> tuple[np.ndarray, ...]:
    identity = np.eye(dimension)
    return tuple(
        _projector(identity[:, index : index + 1])
        for _ in range(repetitions)
        for index in range(dimension)
    )


def _aligned_projectors(
    dimension: int,
    count: int,
    rank: int,
) -> tuple[np.ndarray, ...]:
    basis = np.eye(dimension)[:, :rank]
    projector = _projector(basis)
    return (projector,) * count


def _random_projectors(
    dimension: int,
    count: int,
    rank: int,
    seed: int,
) -> tuple[np.ndarray, ...]:
    rng = np.random.default_rng(seed)
    output = []
    for _ in range(count):
        basis, _ = np.linalg.qr(rng.normal(size=(dimension, rank)), mode="reduced")
        output.append(_projector(basis))
    return tuple(output)


def natural_coverage_pressure_target(n: int) -> NaturalCoveragePressureTarget:
    pressure = affine_plane_support_pressure_scaling_record(n)
    redundancy_log2 = pressure.residual_pressure_after_markov_slack_log2
    # R-1 has the same logarithm asymptotically; use a stable exact conversion
    # where finite values permit it.
    redundancy = 2**redundancy_log2
    forced_log2 = (
        math.log2(redundancy - 1)
        if redundancy > 1
        else -math.inf
    )
    return NaturalCoveragePressureTarget(
        n=n,
        copy_count=pressure.selected_copy_count,
        collision_free_redundancy_lower_bound_log2=redundancy_log2,
        forced_offdiagonal_over_trace_lower_bound_log2=forced_log2,
        raw_overlap_is_perturbative=False,
        natural_excess_fusion_potential_upper_bound=None,
        natural_tight_fusion_frame_proved=False,
        status="divergent-redundancy-forces-overlap-tightness-excess-open",
    )


def run_coverage_welch_pressure() -> CoverageWelchPressureReport:
    controls = [
        audit_fusion_coverage(
            "TIGHT-COORDINATE-Q8-R4",
            _tight_coordinate_projectors(8, 4),
        ),
        audit_fusion_coverage(
            "ALIGNED-Q8-M32-R1",
            _aligned_projectors(8, 32, 1),
        ),
        audit_fusion_coverage(
            "RANDOM-Q12-M48-R3",
            _random_projectors(12, 48, 3, 912),
        ),
    ]
    scaling = [
        natural_coverage_pressure_target(n)
        for n in (12, 16, 20, 24, 28, 32, 40, 48)
    ]
    failures = sum(
        not (row.welch_floor_respected and row.coverage_tail_bound_respected)
        for row in controls
    )
    tight = controls[0]
    aligned = controls[1]
    tail = scaling[-1]
    return CoverageWelchPressureReport(
        created_at=utc_now(),
        theorem_contract={
            "fusion_welch_floor": (
                "For D=sum P_a in Q dimensions with total rank T, "
                "tr(D^2)>=T^2/Q."
            ),
            "forced_overlap": (
                "At redundancy R=T/Q, total off-diagonal projector overlap is "
                "at least (R-1)T."
            ),
            "tightness_excess": (
                "epsilon=Q tr(D^2)/T^2-1 is nonnegative and vanishes exactly "
                "when D=RI."
            ),
            "coverage_tail": (
                "Each lower or upper relative-delta coverage tail has rank "
                "fraction at most epsilon/delta^2."
            ),
            "natural_target": (
                "The collision-free pressure theorem makes R diverge but leaves "
                "epsilon uncontrolled."
            ),
        },
        finite_controls=controls,
        natural_scaling_targets=scaling,
        proof_obligations=[
            {
                "obligation": "identify_correct_interplane_overlap_baseline",
                "resolved": failures == 0,
                "resolution": (
                    "Fusion-frame Welch pressure proves that raw overlap must be "
                    "large whenever support redundancy is large."
                ),
            },
            {
                "obligation": "derive_coverage_tail_from_fusion_potential_excess",
                "resolved": failures == 0,
                "resolution": (
                    "The exact centered second moment is epsilon R T, giving the "
                    "relative-rank tail bound by Markov on eigenvalue squares."
                ),
            },
            {
                "obligation": "prove_natural_excess_fusion_potential_vanishes",
                "resolved": False,
                "resolution": (
                    "Need a four-orientation/inter-plane recoupling second moment "
                    "under the collision-free source law."
                ),
            },
            {
                "obligation": "compute_center_valued_coverage_second_moment",
                "resolved": False,
                "resolution": (
                    "The target statistic is sum_{a,b} tr(P_aP_b), resolved by "
                    "pair-core carrier and multiplicity sectors."
                ),
            },
            {
                "obligation": "transfer_tight_coverage_to_pgm_state_mass",
                "resolved": False,
                "resolution": (
                    "Even a rank-tight coefficient fusion frame needs physical "
                    "state-weight normalization."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Natural planes should have factorially small pairwise overlap.",
                "resolved": True,
                "resolution": (
                    "Impossible at the proved redundancy: the aggregate overlap "
                    "must exceed (R-1)T."
                ),
            },
            {
                "objection": "Support pressure alone implies uniform coverage.",
                "resolved": True,
                "resolution": (
                    "False: repeated aligned projectors have arbitrary redundancy "
                    "and large fusion-potential excess."
                ),
            },
            {
                "objection": "Large raw overlap is evidence against conditioning.",
                "resolved": True,
                "resolution": (
                    "Not by itself; a tight fusion frame has the minimum forced "
                    "overlap and perfect coverage."
                ),
            },
            {
                "objection": "Finite random projectors establish the natural excess law.",
                "resolved": False,
                "resolution": (
                    "They only demonstrate the criterion; natural carrier "
                    "projectors are structured and dependent."
                ),
            },
        ],
        literature_links=[
            {
                "id": "bachoc-ehler-tight-p-fusion-frames-2012",
                "url": FUSION_FRAME_POTENTIAL_URL,
                "relevance": (
                    "Primary fusion-frame-potential framework; the present "
                    "second-moment inequality is the p=1 tightness boundary."
                ),
                "direct_natural_wreath_theorem": False,
            }
        ],
        headline_metrics={
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "tight_control_excess": tight.normalized_excess_fusion_potential,
            "aligned_control_excess": aligned.normalized_excess_fusion_potential,
            "tail_n": tail.n,
            "tail_forced_overlap_over_trace_log2_lower_bound": (
                tail.forced_offdiagonal_over_trace_lower_bound_log2
            ),
            "fusion_welch_pressure_theorem_count": 1,
            "coverage_tail_criterion_theorem_count": 1,
            "natural_tight_coverage_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "raw_interplane_overlap_must_be_large": failures == 0,
            "fusion_potential_excess_is_correct_coverage_target": failures == 0,
            "support_pressure_implies_tight_coverage": False,
            "natural_excess_fusion_potential_vanishes": False,
            "natural_diagonal_coverage_edge_proved": False,
            "pgm_bad_state_mass_controlled": False,
            "collision_free_noncommon_frame_edge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Pressure forces overlap but only a vanishing excess above the "
                "Welch floor would prove uniform natural coverage."
            ),
        },
        status="coverage-target-reduced-to-natural-fusion-potential-excess",
        summary=(
            "Proved that divergent support pressure forces divergent aggregate "
            "inter-plane overlap and isolated the normalized excess fusion "
            "potential as the exact natural coverage statistic."
        ),
        falsifiers_triggered=[
            (
                "Distinct-plane overlaps cannot remain factorially weak once "
                "their total rank demand exceeds pair-core capacity."
            ),
            (
                "Neither large support demand nor large raw overlap certifies a "
                "coverage edge."
            ),
            (
                "The next natural calculation must be a four-orientation "
                "projector second moment and report excess above the Welch floor."
            ),
        ],
    )


def write_coverage_welch_pressure_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COVERAGE-WELCH-PRESSURE"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_coverage_welch_pressure())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    return payload


if __name__ == "__main__":
    report = write_coverage_welch_pressure_report()
    print(json.dumps(report, indent=2, sort_keys=True))
