"""Paired-workspace fidelity audit for quantum subset-sum relation solvers.

Regev's DCP matching composition needs coherent interference between two
endpoints.  A relation solver's success probability does not imply that this
interference survives: witness choices, walk histories, phase-estimation
records, or measured coins can remain entangled with the endpoint.

This module audits an exact uniform-support model.  If endpoint workspaces are
uniform over sets H_0 and H_1, their overlap is

    |H_0 intersection H_1| / sqrt(|H_0| |H_1|).

The observable paired visibility is this overlap multiplied by the exact
amplitude-balance factor 2 sqrt(p_0 p_1)/(p_0+p_1).  The identity is a scoped
composition test, not a lower bound against all quantum subset-sum algorithms.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_QUANTUM_RELATION_FIDELITY_PATH = Path(
    "research/reductions/dcp_quantum_relation_fidelity.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-QUANTUM-RELATION-FIDELITY"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class WorkspaceMechanismSpec:
    mechanism_id: str
    title: str
    left_history_count: int
    right_history_count: int
    common_history_count: int
    history_universe_size: int
    left_success_probability: float
    right_success_probability: float
    valid_witness_fraction: float
    history_depth: int
    branch_factor: int
    asymptotic_model: str
    solver_status: str
    cleanup_status: str
    scaling_proof_status: str
    assumptions: tuple[str, ...]


@dataclass(frozen=True)
class PairedWorkspaceAudit:
    mechanism_id: str
    title: str
    workspace_overlap: float
    amplitude_balance_factor: float
    paired_visibility: float
    valid_weighted_visibility: float
    history_collision_fraction: float
    asymptotic_overlap_class: str
    exact_zero_visibility: bool
    inverse_polynomial_overlap_proved: bool
    polynomial_solver_proved: bool
    full_composition_proved: bool
    decision: str
    missing_obligations: list[str]


@dataclass(frozen=True)
class HistoryScalingCertificate:
    certificate_id: str
    branch_factor: int
    history_depth_symbol: str
    endpoint_support_size: str
    expected_common_histories: str
    normalized_overlap: str
    classification: str
    theorem_scope: str


@dataclass(frozen=True)
class QuantumRelationFidelityReport:
    created_at: str
    theorem: dict[str, bool | str]
    mechanisms: list[PairedWorkspaceAudit]
    scaling_certificates: list[HistoryScalingCertificate]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


DEFAULT_MECHANISMS = (
    WorkspaceMechanismSpec(
        mechanism_id="SHARED-SEED-DETERMINISTIC-CONTROL",
        title="Target-independent shared-seed deterministic control",
        left_history_count=64,
        right_history_count=64,
        common_history_count=64,
        history_universe_size=64,
        left_success_probability=0.25,
        right_success_probability=0.25,
        valid_witness_fraction=1.0,
        history_depth=6,
        branch_factor=2,
        asymptotic_model="identical target-independent seed support",
        solver_status="interface-control-no-partial-solver",
        cleanup_status="reversible-fixed-seed-evaluation-proved",
        scaling_proof_status="constant-overlap-proved",
        assumptions=("The same explicit seed register controls both endpoint evaluations.",),
    ),
    WorkspaceMechanismSpec(
        mechanism_id="ENDPOINT-TAGGED-WALK-HISTORY",
        title="Endpoint-tagged quantum-walk history",
        left_history_count=64,
        right_history_count=64,
        common_history_count=0,
        history_universe_size=128,
        left_success_probability=0.25,
        right_success_probability=0.25,
        valid_witness_fraction=1.0,
        history_depth=6,
        branch_factor=2,
        asymptotic_model="disjoint endpoint-tagged path supports",
        solver_status="abstract-relation-success-only",
        cleanup_status="endpoint-tag-remains",
        scaling_proof_status="zero-overlap-proved",
        assumptions=("The endpoint tag is retained in the walk workspace.",),
    ),
    WorkspaceMechanismSpec(
        mechanism_id="INDEPENDENT-SPARSE-PATH-HISTORIES",
        title="Independent sparse path-history supports",
        left_history_count=64,
        right_history_count=64,
        common_history_count=1,
        history_universe_size=4096,
        left_success_probability=0.25,
        right_success_probability=0.25,
        valid_witness_fraction=1.0,
        history_depth=12,
        branch_factor=2,
        asymptotic_model="support B^(alpha L), alpha=1/2, independently placed in B^L histories",
        solver_status="finite-success-model-only",
        cleanup_status="history-not-uncomputed",
        scaling_proof_status="expected-exponential-overlap-decay",
        assumptions=("Endpoint path supports behave as independent sparse subsets.",),
    ),
    WorkspaceMechanismSpec(
        mechanism_id="CORRELATED-COMMON-HISTORY-CORE",
        title="Correlated common-history core",
        left_history_count=128,
        right_history_count=128,
        common_history_count=32,
        history_universe_size=4096,
        left_success_probability=0.20,
        right_success_probability=0.30,
        valid_witness_fraction=0.95,
        history_depth=12,
        branch_factor=2,
        asymptotic_model="finite common core; no all-n lower bound",
        solver_status="proposal-only-no-density-one-solver",
        cleanup_status="common-history-map-not-constructed",
        scaling_proof_status="finite-only-no-scaling-proof",
        assumptions=("A common history core can be identified without target-dependent advice.",),
    ),
    WorkspaceMechanismSpec(
        mechanism_id="REVERSIBLE-CANONICAL-WITNESS-CLEANUP",
        title="Reversible canonical witness cleanup",
        left_history_count=1,
        right_history_count=1,
        common_history_count=1,
        history_universe_size=1,
        left_success_probability=0.20,
        right_success_probability=0.20,
        valid_witness_fraction=1.0,
        history_depth=0,
        branch_factor=1,
        asymptotic_model="constant overlap conditional on canonical witness and clean uncompute",
        solver_status="proposal-only-canonicalizer-missing",
        cleanup_status="uniform-canonical-uncompute-unproved",
        scaling_proof_status="conditional-constant-overlap",
        assumptions=(
            "A unique canonical witness can be selected in polynomial time.",
            "All search and verification garbage can be reversibly erased.",
        ),
    ),
    WorkspaceMechanismSpec(
        mechanism_id="MEASURED-ENDPOINT-DEPENDENT-HISTORY",
        title="Measured endpoint-dependent history control",
        left_history_count=32,
        right_history_count=32,
        common_history_count=0,
        history_universe_size=64,
        left_success_probability=0.40,
        right_success_probability=0.40,
        valid_witness_fraction=1.0,
        history_depth=5,
        branch_factor=2,
        asymptotic_model="classical endpoint-dependent measurement records",
        solver_status="measured-relation-output",
        cleanup_status="irreversible-measurement-record",
        scaling_proof_status="zero-overlap-proved",
        assumptions=("Measurement records are available to the environment.",),
    ),
)


def workspace_overlap(spec: WorkspaceMechanismSpec) -> float:
    if spec.left_history_count <= 0 or spec.right_history_count <= 0:
        return 0.0
    if spec.common_history_count < 0:
        raise ValueError("common history count must be nonnegative")
    if spec.common_history_count > min(spec.left_history_count, spec.right_history_count):
        raise ValueError("common histories cannot exceed either endpoint support")
    if max(spec.left_history_count, spec.right_history_count) > spec.history_universe_size:
        raise ValueError("endpoint history support exceeds the declared universe")
    return spec.common_history_count / math.sqrt(
        spec.left_history_count * spec.right_history_count
    )


def amplitude_balance(left_probability: float, right_probability: float) -> float:
    if left_probability < 0 or right_probability < 0:
        raise ValueError("success probabilities must be nonnegative")
    total = left_probability + right_probability
    if total == 0:
        return 0.0
    return 2.0 * math.sqrt(left_probability * right_probability) / total


def _overlap_class(spec: WorkspaceMechanismSpec, overlap: float) -> str:
    if overlap == 0.0:
        return "zero-proved-for-model"
    if spec.scaling_proof_status == "constant-overlap-proved":
        return "constant-proved-interface-control"
    if spec.scaling_proof_status == "expected-exponential-overlap-decay":
        return "exponential-expected-under-sparse-history-model"
    if spec.scaling_proof_status == "conditional-constant-overlap":
        return "constant-conditional-on-unproved-canonical-cleanup"
    return "finite-only-no-asymptotic-overlap-proof"


def audit_workspace_mechanism(spec: WorkspaceMechanismSpec) -> PairedWorkspaceAudit:
    if not 0.0 <= spec.valid_witness_fraction <= 1.0:
        raise ValueError("valid witness fraction must lie in [0,1]")
    overlap = workspace_overlap(spec)
    balance = amplitude_balance(
        spec.left_success_probability, spec.right_success_probability
    )
    visibility = overlap * balance
    valid_visibility = visibility * spec.valid_witness_fraction
    overlap_class = _overlap_class(spec, overlap)
    inverse_poly = spec.scaling_proof_status == "constant-overlap-proved"
    polynomial_solver = spec.solver_status == "polynomial-density-one-partial-solver-proved"
    cleanup_proved = spec.cleanup_status in {
        "reversible-fixed-seed-evaluation-proved",
        "uniform-canonical-uncompute-proved",
    }
    full_composition = (
        inverse_poly
        and polynomial_solver
        and cleanup_proved
        and spec.valid_witness_fraction == 1.0
    )
    missing: list[str] = []
    if not inverse_poly:
        missing.append("uniform inverse-polynomial paired-workspace overlap theorem")
    if not polynomial_solver:
        missing.append("polynomial density-one partial subset-sum solver with source coverage")
    if not cleanup_proved:
        missing.append("reversible endpoint-independent history/witness cleanup")
    if spec.valid_witness_fraction < 1.0:
        missing.append("coherent invalid-witness rejection with composed error bound")
    if full_composition:
        decision = "source-composition-eligible"
    elif overlap == 0.0:
        decision = "rejected-zero-visibility"
    elif overlap_class.startswith("exponential"):
        decision = "rejected-exponential-history-overlap"
    elif spec.mechanism_id == "SHARED-SEED-DETERMINISTIC-CONTROL":
        decision = "proved-interface-control-no-solver"
    else:
        decision = "proposal-only-proof-debt"
    collision_fraction = (
        spec.common_history_count / spec.history_universe_size
        if spec.history_universe_size
        else 0.0
    )
    return PairedWorkspaceAudit(
        mechanism_id=spec.mechanism_id,
        title=spec.title,
        workspace_overlap=overlap,
        amplitude_balance_factor=balance,
        paired_visibility=visibility,
        valid_weighted_visibility=valid_visibility,
        history_collision_fraction=collision_fraction,
        asymptotic_overlap_class=overlap_class,
        exact_zero_visibility=visibility == 0.0,
        inverse_polynomial_overlap_proved=inverse_poly,
        polynomial_solver_proved=polynomial_solver,
        full_composition_proved=full_composition,
        decision=decision,
        missing_obligations=missing,
    )


def build_scaling_certificates() -> list[HistoryScalingCertificate]:
    return [
        HistoryScalingCertificate(
            certificate_id="CERT-DCP-SPARSE-INDEPENDENT-HISTORY-OVERLAP",
            branch_factor=2,
            history_depth_symbol="L",
            endpoint_support_size="B^(alpha L), 0<=alpha<1",
            expected_common_histories="B^((2 alpha - 1)L)",
            normalized_overlap="B^(-(1-alpha)L)",
            classification="exponential when L=Omega(n) and alpha is bounded below one",
            theorem_scope=(
                "Expectation under independent uniformly placed endpoint history supports; this is not a lower bound "
                "for correlated or coherently cleaned quantum walks."
            ),
        ),
        HistoryScalingCertificate(
            certificate_id="CERT-DCP-COMMON-CORE-OVERLAP-REQUIREMENT",
            branch_factor=2,
            history_depth_symbol="L",
            endpoint_support_size="M_0(n), M_1(n)",
            expected_common_histories="C(n)",
            normalized_overlap="C(n)/sqrt(M_0(n) M_1(n))",
            classification="must be at least inverse polynomial for this matching composition",
            theorem_scope=(
                "Exact for uniform positive workspace amplitudes after aligning paired witnesses; arbitrary amplitudes "
                "require their full inner product rather than support counts."
            ),
        ),
    ]


def run_quantum_relation_fidelity_audit(
    mechanisms: Sequence[WorkspaceMechanismSpec] = DEFAULT_MECHANISMS,
) -> QuantumRelationFidelityReport:
    audits = [audit_workspace_mechanism(spec) for spec in mechanisms]
    metrics: dict[str, int | float] = {
        "mechanism_count": len(audits),
        "exact_zero_visibility_count": sum(item.exact_zero_visibility for item in audits),
        "exponential_history_overlap_count": sum(
            item.asymptotic_overlap_class.startswith("exponential") for item in audits
        ),
        "finite_only_or_conditional_count": sum(
            item.decision == "proposal-only-proof-debt" for item in audits
        ),
        "proved_shared_seed_interface_control_count": sum(
            item.decision == "proved-interface-control-no-solver" for item in audits
        ),
        "proved_inverse_polynomial_overlap_count": sum(
            item.inverse_polynomial_overlap_proved for item in audits
        ),
        "proved_polynomial_partial_solver_count": sum(item.polynomial_solver_proved for item in audits),
        "proved_full_quantum_relation_composition_count": sum(
            item.full_composition_proved for item in audits
        ),
        "maximum_noncontrol_valid_weighted_visibility": max(
            (
                item.valid_weighted_visibility
                for item in audits
                if item.mechanism_id != "SHARED-SEED-DETERMINISTIC-CONTROL"
            ),
            default=0.0,
        ),
    }
    return QuantumRelationFidelityReport(
        created_at=utc_now(),
        theorem={
            "uniform_support_workspace_overlap_identity": True,
            "amplitude_balance_identity": True,
            "success_probability_alone_implies_interference": False,
            "scope": (
                "Regev-style paired-endpoint matching with uniform positive workspace amplitudes; arbitrary quantum "
                "states use the exact paired workspace inner product."
            ),
            "required_extension": (
                "A concrete quantum walk must expose target-by-target amplitudes, witness alignment, histories, cleanup, "
                "precision, and an all-n inverse-polynomial overlap or shared-seed theorem."
            ),
        },
        mechanisms=audits,
        scaling_certificates=build_scaling_certificates(),
        headline_metrics=metrics,
        claim_gate={
            "paired_workspace_identity_proved": True,
            "shared_seed_interface_control_retained": True,
            "concrete_quantum_walk_audited": False,
            "polynomial_density_one_solver_proved": False,
            "full_quantum_relation_composition_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Success probabilities do not control paired workspace fidelity. The only proved overlap row is the "
                "existing shared-seed interface control, which does not construct a partial solver."
            ),
        },
        status="quantum-relation-workspace-fidelity-blocked",
        summary=(
            f"Audited {len(audits)} paired-workspace mechanisms: "
            f"{metrics['exact_zero_visibility_count']} have exact zero visibility, "
            f"{metrics['exponential_history_overlap_count']} has exponential expected overlap decay, and zero combine "
            "a polynomial density-one solver with a complete coherence theorem."
        ),
        falsifiers_triggered=[
            "Endpoint-tagged or measured histories have exactly zero paired visibility.",
            "Independent sparse path supports have exponentially decaying expected normalized overlap at linear depth.",
            "A finite common-history fraction is not an all-n overlap theorem.",
            "Canonical witness cleanup is a proposal, not a circuit, until uniqueness and reversible erasure are proved.",
            "The shared-seed interface control proves composability only; it does not construct a partial solver.",
        ],
    )


def write_quantum_relation_fidelity_audit(
    path: Path = DCP_QUANTUM_RELATION_FIDELITY_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(run_quantum_relation_fidelity_audit())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        negatives = (
            (
                "NEG-DCP-QUANTUM-RELATION-SUCCESS-WITHOUT-FIDELITY",
                "A quantum relation solver's witness success probability is enough for Regev's matching composition.",
                "Paired endpoint interference also depends on amplitude balance and the inner product of retained witness/history workspaces.",
            ),
            (
                "NEG-DCP-ENDPOINT-HISTORY-ORTHOGONALITY",
                "Endpoint-tagged or measured quantum-walk histories preserve the required phase signal.",
                "Disjoint retained history supports give an exact zero workspace inner product and zero paired visibility.",
            ),
            (
                "NEG-DCP-FINITE-COMMON-HISTORY-WITHOUT-SCALING",
                "A finite common-history overlap establishes a scalable coherent partial-solver bridge.",
                "The source composition needs an all-n inverse-polynomial overlap and balanced-amplitude theorem with complete resource accounting.",
            ),
        )
        for negative_id, claim, reason in negatives:
            upsert_negative_result(
                NegativeResultRecord(
                    id=negative_id,
                    source=str(path),
                    claim=claim,
                    reason_invalid=reason,
                    lesson=(
                        "Extract exact endpoint amplitudes and retained workspace states from a concrete solver; prove "
                        "shared histories or reversible canonical cleanup before claiming composition."
                    ),
                    applies_to=[registry_candidate_id, registry_experiment_id],
                    evidence=payload["headline_metrics"],
                )
            )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-QUANTUM-RELATION-FIDELITY"
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"dcp_quantum_relation_fidelity": str(path)},
            )
        )
    return payload
