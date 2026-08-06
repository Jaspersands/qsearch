"""Access and reduction boundary for coherent DCP fiber erasure.

The normalized subset-sum fiber state is

    |u_s> = c_s^(-1/2) sum_{x:f_a(x)=s} |x>.

Preparing or erasing these states resembles index erasure, but the access
models differ sharply.  The tight square-root query lower bound for
non-coherent index erasure concerns an arbitrary injective black-box function.
In DCP, the labels ``a_i`` are public and ``f_a(x)=sum_i a_i x_i`` has a
polynomial reversible arithmetic circuit.  The black-box theorem is therefore
a generic warning, not a lower bound for structured subset sum.

This module also formalizes two conditional reductions:

* A target-addressable, flagged normalized-fiber preparer with
  inverse-polynomial legal success decides subset-sum support.
* If that primitive remains valid on every fixed-variable subinstance, repeated
  support decisions recover a verified Boolean witness by self-reduction.

Neither reduction covers a global collective PGM circuit that never exposes a
target-addressable preparation flag.  The distinction prevents both false
lower-bound transfers and uncharged state-generation primitives.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


REPORT_PATH = Path(
    "research/reductions/dcp_coherent_fiber_erasure_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-DHS-DCP-COHERENT-FIBER-ERASURE-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"
INDEX_ERASURE_LITERATURE_ID = (
    "lindzey-rosmanis-index-erasure-2019"
)


@dataclass(frozen=True)
class AccessBoundaryRecord:
    access_model: str
    function_access: str
    target_interface: str
    applicable_lower_bound: str
    transfer_to_dcp_valid: bool
    reason: str
    required_resource_charges: list[str]


@dataclass(frozen=True)
class FiberReductionCertificate:
    primitive: str
    assumptions: list[str]
    consequence: str
    query_or_call_cost: str
    proved: bool
    scope_limit: str


@dataclass(frozen=True)
class IndexErasureScalingRow:
    n_bits: int
    domain_size_log2: int
    black_box_query_lower_bound_log2: float
    polynomial_query_threshold_log2: float
    black_box_bound_superpolynomial: bool
    structured_subset_sum_transfer_valid: bool


@dataclass(frozen=True)
class CoherentFiberErasureBoundaryReport:
    created_at: str
    literature_links: list[str]
    state_generation_contract: dict[str, str]
    access_boundaries: list[AccessBoundaryRecord]
    reduction_certificates: list[FiberReductionCertificate]
    scaling_rows: list[IndexErasureScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def build_access_boundaries() -> list[AccessBoundaryRecord]:
    return [
        AccessBoundaryRecord(
            access_model="arbitrary-injective-black-box",
            function_access=(
                "coherent queries to an otherwise unstructured injective "
                "oracle f:[D]->[R]"
            ),
            target_interface="generate the uniform image state",
            applicable_lower_bound="Theta(sqrt(D)) quantum queries",
            transfer_to_dcp_valid=False,
            reason=(
                "The theorem applies in its native black-box model, but the "
                "DCP function family is structured, many-to-one, and publicly "
                "specified by n arithmetic labels."
            ),
            required_resource_charges=[
                "oracle queries",
                "ancillary garbage dependence",
                "coherent versus non-coherent output",
            ],
        ),
        AccessBoundaryRecord(
            access_model="public-subset-sum-evaluator",
            function_access=(
                "public labels a_i and a reversible poly(n)-gate circuit for "
                "f_a(x)=sum_i a_i x_i mod 2^n"
            ),
            target_interface=(
                "target-addressable normalized-fiber state and a legal/illegal "
                "success flag"
            ),
            applicable_lower_bound=(
                "no transferred black-box index-erasure lower bound"
            ),
            transfer_to_dcp_valid=False,
            reason=(
                "Arithmetic structure may defeat black-box adversary bounds; "
                "the actual blockers are normalization, spectral spacing, "
                "state preparation, and average-source complexity."
            ),
            required_resource_charges=[
                "reversible arithmetic gates",
                "state preparations and reflections",
                "postselection or amplification",
                "normalization and condition number",
                "precision",
                "advice or QRAM",
            ],
        ),
        AccessBoundaryRecord(
            access_model="independent-dcp-state-input",
            function_access=(
                "independent phase states with measured public labels; no "
                "rewind, hidden-state reflection, or chosen-label oracle"
            ),
            target_interface=(
                "global collective measurement may avoid a separately "
                "target-addressable fiber primitive"
            ),
            applicable_lower_bound=(
                "neither black-box index erasure nor target-addressable "
                "support-decision reduction applies automatically"
            ),
            transfer_to_dcp_valid=False,
            reason=(
                "A full measurement must be audited as a channel on the "
                "available independent states, including every preparation "
                "and reflection it assumes."
            ),
            required_resource_charges=[
                "DCP state copies",
                "collective width",
                "public-label classical work",
                "measurement outcomes",
                "complete hidden-shift decoder",
            ],
        ),
    ]


def build_reduction_certificates() -> list[FiberReductionCertificate]:
    return [
        FiberReductionCertificate(
            primitive="target-addressable-flagged-normalized-fiber-preparer",
            assumptions=[
                "input is public (a,s)",
                "good-flag probability is at least gamma(n)>=1/poly(n) when c_s>0",
                "good-flag probability is zero when c_s=0",
                "one call uses poly(n) gates and no hidden advice",
            ],
            consequence=(
                "one-sided-error decision of whether the modular subset-sum "
                "fiber is nonempty"
            ),
            query_or_call_cost=(
                "O(gamma(n)^-1 log(1/delta)) repetitions, or the charged "
                "amplitude-amplification equivalent"
            ),
            proved=True,
            scope_limit=(
                "Does not recover a witness and does not cover a global "
                "measurement with no target-addressable success flag."
            ),
        ),
        FiberReductionCertificate(
            primitive="fixed-variable-stable-target-addressable-preparer",
            assumptions=[
                "all support-decision assumptions hold",
                "the guarantee holds on every subinstance obtained by fixing a prefix of Boolean variables",
                "errors compose below 1/poly(n)",
                "the final witness is verified against the original equation",
            ],
            consequence=(
                "recover a Boolean subset-sum witness by testing the zero and "
                "one branches at each variable"
            ),
            query_or_call_cost=(
                "O(n gamma_min(n)^-1 log(n/delta)) primitive calls"
            ),
            proved=True,
            scope_limit=(
                "Average density-one success on the original source does not "
                "imply the required guarantees on lower-density conditioned "
                "subinstances."
            ),
        ),
        FiberReductionCertificate(
            primitive="global-full-rank-collective-pgm-channel",
            assumptions=[
                "acts only on legal independent DCP state input",
                "does not expose a target-addressable support flag",
            ],
            consequence=(
                "no support-decision or witness-search reduction established"
            ),
            query_or_call_cost="must be audited from its explicit circuit",
            proved=False,
            scope_limit=(
                "This is the principal open escape from the target-addressable "
                "fiber-preparation reduction."
            ),
        ),
    ]


def index_erasure_scaling_row(
    n_bits: int,
    polynomial_query_power: int = 8,
) -> IndexErasureScalingRow:
    if n_bits < 2:
        raise ValueError("n_bits must be at least two")
    lower_log2 = n_bits / 2
    threshold_log2 = polynomial_query_power * math.log2(n_bits)
    return IndexErasureScalingRow(
        n_bits=n_bits,
        domain_size_log2=n_bits,
        black_box_query_lower_bound_log2=lower_log2,
        polynomial_query_threshold_log2=threshold_log2,
        black_box_bound_superpolynomial=lower_log2 > threshold_log2,
        structured_subset_sum_transfer_valid=False,
    )


def build_coherent_fiber_erasure_boundary_report(
    n_values: tuple[int, ...] = (64, 128, 256, 512, 1024),
) -> CoherentFiberErasureBoundaryReport:
    boundaries = build_access_boundaries()
    reductions = build_reduction_certificates()
    scaling = [index_erasure_scaling_row(n_bits) for n_bits in n_values]
    metrics: dict[str, int | float] = {
        "access_model_count": len(boundaries),
        "reduction_certificate_count": len(reductions),
        "proved_target_addressable_support_decision_reduction_count": 1,
        "proved_fixed_variable_witness_self_reduction_count": 1,
        "proved_global_collective_measurement_reduction_count": 0,
        "black_box_index_erasure_lower_bound_count": 1,
        "valid_black_box_lower_bound_transfer_to_structured_subset_sum_count": 0,
        "scaling_row_count": len(scaling),
        "black_box_superpolynomial_row_count": sum(
            row.black_box_bound_superpolynomial for row in scaling
        ),
        "maximum_n_bits": max(n_values),
        "tail_black_box_query_lower_bound_log2": (
            scaling[-1].black_box_query_lower_bound_log2
        ),
        "polynomial_source_aware_fiber_preparer_count": 0,
        "polynomial_global_collective_pgm_channel_count": 0,
    }
    return CoherentFiberErasureBoundaryReport(
        created_at=utc_now(),
        literature_links=[INDEX_ERASURE_LITERATURE_ID],
        state_generation_contract={
            "fiber_state": (
                "|u_s>=c_s^-1/2 sum_{x:f_a(x)=s}|x> for c_s>0"
            ),
            "target_addressable_interface": (
                "U_a|s,0,0>=sqrt(p_s)|s,u_s,good>+"
                "sqrt(1-p_s)|garbage,bad>"
            ),
            "global_interface": (
                "A collective channel on DCP registers need not expose U_a "
                "or a reusable success flag."
            ),
            "input_model": (
                "Public labels permit reversible subset-sum arithmetic; hidden "
                "DCP states remain independent, nonrewindable inputs."
            ),
        },
        access_boundaries=boundaries,
        reduction_certificates=reductions,
        scaling_rows=scaling,
        headline_metrics=metrics,
        claim_gate={
            "black_box_index_erasure_lower_bound_known": True,
            "black_box_lower_bound_transfers_to_subset_sum": False,
            "target_addressable_preparer_implies_support_decision": True,
            "fixed_variable_stability_implies_witness_search": True,
            "global_collective_measurement_reduced_to_support_decision": False,
            "polynomial_source_aware_fiber_preparer_constructed": False,
            "polynomial_global_collective_pgm_channel_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Black-box index erasure supplies a generic square-root "
                "barrier but cannot be transferred to public arithmetic "
                "subset sum. Target-addressable primitives inherit support "
                "decision and, with fixed-variable stability, witness-search "
                "obligations. A genuinely global collective channel remains "
                "open and must be explicitly constructed."
            ),
        },
        status=(
            "index-erasure-transfer-invalid-target-addressable-"
            "reductions-proved-global-channel-open"
        ),
        summary=(
            f"Separated {len(boundaries)} state-generation access models and "
            f"proved {sum(row.proved for row in reductions)} conditional "
            "reductions. The black-box square-root lower bound has zero valid "
            "transfers to structured subset sum; target-addressable support "
            "decision and fixed-variable witness obligations are explicit."
        ),
        falsifiers_triggered=[
            "A black-box index-erasure lower bound cannot be cited as a lower bound for public arithmetic subset-sum maps.",
            "A target-addressable normalized-fiber primitive with a success flag is already an average-case support-decision algorithm.",
            "Witness self-reduction additionally requires guarantees on every fixed-variable subinstance.",
            "A global collective channel need not expose the target-addressable interface and is not ruled out by these reductions.",
            "Any use of DCP state reflection, rewinding, chosen labels, QRAM, or advice must be charged separately.",
        ],
    )


def write_coherent_fiber_erasure_boundary_report(
    output_path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    n_values: tuple[int, ...] = (64, 128, 256, 512, 1024),
) -> dict[str, object]:
    payload = asdict(
        build_coherent_fiber_erasure_boundary_report(n_values)
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True)
    )
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-BLACK-BOX-INDEX-ERASURE-LOWER-BOUND-TRANSFER",
                source=str(output_path),
                claim=(
                    "The black-box non-coherent index-erasure lower bound "
                    "directly rules out polynomial DCP subset-sum fiber erasure."
                ),
                reason_invalid=(
                    "DCP exposes public arithmetic labels and a structured "
                    "many-to-one map, outside the arbitrary injective black-box "
                    "model of the lower bound."
                ),
                lesson=(
                    "Use index erasure as a generic baseline. Prove a "
                    "structure-preserving reduction before transferring any "
                    "lower bound, and separately charge target-addressable "
                    "support-decision or fixed-variable witness obligations."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    INDEX_ERASURE_LITERATURE_ID,
                ],
                evidence=payload["headline_metrics"],
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
                created_at=str(payload["created_at"]),
                status=str(payload["status"]),
                summary=str(payload["summary"]),
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload[
                    "falsifiers_triggered"
                ],
                artifacts={
                    "dcp_coherent_fiber_erasure_boundary": str(
                        output_path
                    )
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_coherent_fiber_erasure_boundary_report()
    print(
        json.dumps(
            report["headline_metrics"], indent=2, sort_keys=True
        )
    )
