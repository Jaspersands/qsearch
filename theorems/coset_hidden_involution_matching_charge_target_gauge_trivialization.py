"""Gauge trivialization of naive target-controlled matching charges.

The physical tuple basis is the right-coset space

    L/A,  L=G^k x G,
    A={(r,...,r;r):r in G}.

The apparent target coordinate is not an independent classical register.  A
coset has representatives

    (g_1,...,g_k;t) ~ (g_1 r,...,g_k r;t r),

and the canonical relative-coordinate identification is

    Phi([(g_1,...,g_k;t)])=(g_1 t^-1,...,g_k t^-1).    (1)

Suppose one tries to use the target representative to control a right action
by a charge term ``d`` on source coordinate ``j`` while leaving the target
unchanged.  Representative covariance uniquely gives

    g_j -> g_j t^-1 d t.                              (2)

Under a gauge change ``t->tr``, the multiplier becomes
``r^-1 t^-1 d t r``, so (2) is well defined on ``L/A``.  But applying (1)
after (2) gives simply

    x_j=g_jt^-1 -> x_j d.                             (3)

Thus target-controlled conjugation by the representative target is gauge
trivial: it is exactly an ordinary source-local charge in physical relative
coordinates.  Averaging ``d`` over ``D_h``, applying coherent phase
estimation, or using any target-diagonal polynomial of these actions does not
change this conclusion.

The all-finite-group source-local likelihood theorem then applies.  Joint
measurements of these gauge-trivialized ``K``-centralizing charges have
identical baseline and alternative outcome distributions.  The faithful
external charge orbit ``tK -> D_(t h t^-1)`` remains mathematically valid,
but the physical quotient target cannot be used as a free external candidate
register to exploit it.

A viable target recoupling must genuinely change the target coordinate (for
example through right convolution), couple all source coordinates before
gauge fixing, and generate the factorial implicit interference required by
the negativity theorem.  This result does not rule out such operations or an
externally supplied candidate-matching oracle.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from coset_hidden_involution_binary_decision_reduction import (
    Permutation,
    compose_permutations,
    inverse_permutation,
    symmetric_group,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_matching_charge_target_gauge_trivialization.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-TARGET-GAUGE-TRIVIALIZATION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

SourceTuple = tuple[Permutation, ...]


@dataclass(frozen=True)
class QuotientGaugeControl:
    degree: int
    copy_count: int
    tested_source_tuple_count: int
    tested_target_count: int
    tested_gauge_count: int
    tested_charge_term_count: int
    quotient_coordinate_gauge_failure_count: int
    controlled_action_gauge_covariance_failure_count: int
    relative_source_action_failure_count: int
    target_coordinate_changed_by_controlled_action: bool
    exact_gauge_trivialization_verified: bool
    status: str


@dataclass(frozen=True)
class TargetGaugeTrivializationTheorem:
    physical_quotient: str
    relative_coordinates: str
    representative_covariant_action: str
    gauge_fixed_action: str
    likelihood_consequence: str
    exact_all_finite_groups_gauge_trivialization_proved: bool
    target_diagonal_charge_control_is_genuinely_target_coupled: bool
    coherent_D_phase_label_from_physical_target_is_detector: bool
    external_candidate_charge_orbit_invalidated: bool
    target_changing_convolution_route_ruled_out: bool
    all_copy_target_recoupling_compiled: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class TargetGaugeTrivializationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[QuotientGaugeControl]
    theorem: TargetGaugeTrivializationTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def quotient_relative_coordinates(
    sources: SourceTuple,
    target: Permutation,
) -> SourceTuple:
    target_inverse = inverse_permutation(target)
    return tuple(
        compose_permutations(source, target_inverse) for source in sources
    )


def gauge_change_representative(
    sources: SourceTuple,
    target: Permutation,
    gauge: Permutation,
) -> tuple[SourceTuple, Permutation]:
    return (
        tuple(compose_permutations(source, gauge) for source in sources),
        compose_permutations(target, gauge),
    )


def representative_covariant_source_action(
    sources: SourceTuple,
    target: Permutation,
    charge_term: Permutation,
    source_index: int,
) -> tuple[SourceTuple, Permutation]:
    if not 0 <= source_index < len(sources):
        raise ValueError("source_index out of range")
    multiplier = compose_permutations(
        compose_permutations(inverse_permutation(target), charge_term),
        target,
    )
    output = list(sources)
    output[source_index] = compose_permutations(
        output[source_index],
        multiplier,
    )
    return tuple(output), target


def direct_relative_source_action(
    relative_sources: SourceTuple,
    charge_term: Permutation,
    source_index: int,
) -> SourceTuple:
    output = list(relative_sources)
    output[source_index] = compose_permutations(
        output[source_index],
        charge_term,
    )
    return tuple(output)


def audit_quotient_gauge_trivialization(
    degree: int,
    copy_count: int,
) -> QuotientGaugeControl:
    if degree < 2 or copy_count < 1:
        raise ValueError("require degree>=2 and copy_count>=1")
    group = symmetric_group(degree)
    # Deterministic probes span identities, transpositions, and noncommuting cycles.
    probes = tuple(group[: min(len(group), 6)])
    sources_catalog = tuple(
        tuple(probes[(offset + index) % len(probes)] for index in range(copy_count))
        for offset in range(min(4, len(probes)))
    )
    coordinate_failures = 0
    covariance_failures = 0
    relative_failures = 0
    tested = 0
    for sources in sources_catalog:
        for target in probes:
            relative = quotient_relative_coordinates(sources, target)
            for gauge in probes:
                changed_sources, changed_target = gauge_change_representative(
                    sources,
                    target,
                    gauge,
                )
                coordinate_failures += (
                    quotient_relative_coordinates(changed_sources, changed_target)
                    != relative
                )
                for charge_term in probes:
                    for source_index in range(copy_count):
                        acted_sources, acted_target = (
                            representative_covariant_source_action(
                                sources,
                                target,
                                charge_term,
                                source_index,
                            )
                        )
                        changed_acted_sources, changed_acted_target = (
                            representative_covariant_source_action(
                                changed_sources,
                                changed_target,
                                charge_term,
                                source_index,
                            )
                        )
                        expected_changed = gauge_change_representative(
                            acted_sources,
                            acted_target,
                            gauge,
                        )
                        covariance_failures += (
                            (changed_acted_sources, changed_acted_target)
                            != expected_changed
                        )
                        observed_relative = quotient_relative_coordinates(
                            acted_sources,
                            acted_target,
                        )
                        expected_relative = direct_relative_source_action(
                            relative,
                            charge_term,
                            source_index,
                        )
                        relative_failures += observed_relative != expected_relative
                        tested += 1
    verified = not coordinate_failures and not covariance_failures and not relative_failures
    return QuotientGaugeControl(
        degree=degree,
        copy_count=copy_count,
        tested_source_tuple_count=len(sources_catalog),
        tested_target_count=len(probes),
        tested_gauge_count=len(probes),
        tested_charge_term_count=len(probes),
        quotient_coordinate_gauge_failure_count=coordinate_failures,
        controlled_action_gauge_covariance_failure_count=covariance_failures,
        relative_source_action_failure_count=relative_failures,
        target_coordinate_changed_by_controlled_action=False,
        exact_gauge_trivialization_verified=verified,
        status=(
            "target-controlled-charge-action-gauge-trivialized"
            if verified
            else "target-gauge-trivialization-control-failure"
        ),
    )


def build_target_gauge_trivialization_report() -> TargetGaugeTrivializationReport:
    controls = [
        audit_quotient_gauge_trivialization(3, 2),
        audit_quotient_gauge_trivialization(4, 2),
        audit_quotient_gauge_trivialization(4, 3),
    ]
    exact = all(row.exact_gauge_trivialization_verified for row in controls)
    theorem = TargetGaugeTrivializationTheorem(
        physical_quotient=(
            "The physical basis is L/A with (g_i;t)~(g_i r;t r), so the "
            "target representative is a gauge coordinate."
        ),
        relative_coordinates=(
            "Phi([(g_i;t)])=(g_i t^-1)_i is an exact bijection L/A -> G^k."
        ),
        representative_covariant_action=(
            "Leaving t fixed while acting on source j requires the multiplier "
            "t^-1 d t to remain well defined under t->tr."
        ),
        gauge_fixed_action=(
            "Under Phi, g_j->g_j t^-1 d t becomes x_j->x_j d: an ordinary "
            "source-local right action."
        ),
        likelihood_consequence=(
            "Target-diagonal coherent charge labels and their spectral functions "
            "are source-local after gauge fixing and therefore likelihood blind."
        ),
        exact_all_finite_groups_gauge_trivialization_proved=exact,
        target_diagonal_charge_control_is_genuinely_target_coupled=False,
        coherent_D_phase_label_from_physical_target_is_detector=False,
        external_candidate_charge_orbit_invalidated=False,
        target_changing_convolution_route_ruled_out=False,
        all_copy_target_recoupling_compiled=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=exact,
        status=(
            "physical-target-controlled-charge-gauge-trivialized"
            if exact
            else "target-gauge-trivialization-theorem-control-failure"
        ),
    )
    return TargetGaugeTrivializationReport(
        created_at=utc_now(),
        theorem_contract={
            "physical_space": "Right-coset quotient (G^k x G)/diag(G)",
            "tested_operation": (
                "Representative-target-diagonal conjugated right charge action "
                "that leaves the target coordinate unchanged"
            ),
            "claim_boundary": (
                "Rules out only the gauge-trivial target control; target-changing "
                "convolution and externally supplied candidate registers remain open."
            ),
        },
        finite_controls=controls,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-MATCHING-CHARGE-TARGET-CHANGING-RECOUPLING",
                "statement": (
                    "Construct a quotient-well-defined operation that changes the "
                    "target coordinate and couples all sources before gauge fixing."
                ),
                "resolved": False,
            },
            {
                "id": "PO-MATCHING-CHARGE-EXTERNAL-CANDIDATE-ACCESS",
                "statement": (
                    "If an external candidate-matching register is used, include its "
                    "preparation/search cost and compare against classical candidate access."
                ),
                "resolved": False,
            },
            {
                "id": "PO-MATCHING-CHARGE-GAUGE-NONLINEAR-POLAR",
                "statement": (
                    "Express any proposed matrix polar directly on quotient-relative "
                    "coordinates to verify it is not another source-local gauge artifact."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The target coordinate can be measured and used as a classical control.",
                "answer": (
                    "Not on L/A without choosing a nonphysical representative; only "
                    "gauge-covariant operations descend to the quotient."
                ),
                "resolved": True,
            },
            {
                "challenge": "Conjugating D by the target makes the action nonlocal.",
                "answer": (
                    "False after exact gauge fixing: it becomes the fixed source-local D action."
                ),
                "resolved": True,
            },
            {
                "challenge": "The faithful external charge orbit theorem was wrong.",
                "answer": (
                    "No. Its stabilizer/injectivity result is valid for an explicitly "
                    "supplied conjugator; the physical quotient target is not that resource."
                ),
                "resolved": True,
            },
            {
                "challenge": "Every target-coupled operation is gauge trivial.",
                "answer": (
                    "Too strong. Operations that change the target coordinate become "
                    "genuine all-source transformations in relative coordinates."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_all_finite_groups_gauge_trivialization_count": int(exact),
            "finite_gauge_control_count": len(controls),
            "physical_target_diagonal_charge_detector_count": 0,
            "target_changing_recoupling_count": 0,
            "hidden_involution_detector_count": 0,
        },
        claim_gate={
            "target_diagonal_conjugated_charge_is_source_local_after_gauge_fixing": exact,
            "physical_target_diagonal_D_label_is_detector": False,
            "external_candidate_charge_orbit_remains_valid": True,
            "target_changing_convolution_route_ruled_out": False,
            "all_copy_target_recoupling_compiled": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The physical target representative is gauge; its covariant charge "
                "control reduces exactly to a source-local likelihood-blind action."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that naive physical-target-controlled matching-charge labels are "
            "gauge-equivalent to source-local operations and cannot detect the likelihood."
        ),
        falsifiers_triggered=[
            "The physical quotient target is not a free candidate-matching control register.",
            "Target-diagonal conjugated D phase estimation is source-local after gauge fixing.",
            "A viable charge recoupling must change the target coordinate genuinely.",
        ],
    )


def write_target_gauge_trivialization_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_target_gauge_trivialization_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_target_gauge_trivialization_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
