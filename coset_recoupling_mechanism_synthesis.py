"""Typed mutation search for symmetric-group collective measurements.

Candidate mechanisms are composed from primitives with explicit state types and
capability dependencies.  The evaluator rejects known-invalid transfers before
they can become proof-gated candidates.  Architectures that name all missing
operations remain proposal-only until those operations have uniform circuit and
decoder proofs.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_mutation_proposal,
    upsert_negative_result,
    utc_now,
)


COSET_RECOUPLING_SYNTHESIS_PATH = Path(
    "research/representation/coset_recoupling_mechanism_synthesis.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-RECOUPLING-MECHANISM-SYNTHESIS"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PrimitiveSpec:
    id: str
    input_type: str
    output_type: str
    capability_id: str
    available_with_uniform_proof: bool
    role: str


@dataclass(frozen=True)
class MechanismTemplate:
    id: str
    title: str
    stages: tuple[str, ...]
    source_family_scope: str
    target_register_scaling: str
    known_no_go_violations: tuple[str, ...]
    additional_proof_obligations: tuple[str, ...]
    upside_score: int


@dataclass(frozen=True)
class MechanismEvaluation:
    id: str
    title: str
    stages: tuple[str, ...]
    typed_interfaces_valid: bool
    interface_issues: list[str]
    missing_capabilities: list[str]
    known_no_go_violations: list[str]
    additional_proof_obligations: list[str]
    holevo_copy_budget_obligation_attached: bool
    minimum_copy_budget_rule: str
    full_source_family_coverage: bool
    proof_gate_eligible: bool
    decision: str
    priority_score: int
    rationale: str


@dataclass(frozen=True)
class RecouplingMechanismSynthesisReport:
    created_at: str
    primitive_specs: list[PrimitiveSpec]
    evaluations: list[MechanismEvaluation]
    ranked_survivors: list[str]
    mutation_proposals: list[dict]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


PRIMITIVES = {
    item.id: item
    for item in (
        PrimitiveSpec("PREPARE_COSET_K", "start", "coset_state_k", "CAP-COSET-PREPARATION", True, "Prepare k independent coset states."),
        PrimitiveSpec("SN_QFT_K", "coset_state_k", "fourier_registers_k", "CAP-SN-QFT", True, "Apply the solved S_n QFT registerwise."),
        PrimitiveSpec("WEAK_LABEL_MEASUREMENT", "fourier_registers_k", "irrep_labels", "CAP-WEAK-IRREP-PROJECTION", True, "Measure only irrep labels."),
        PrimitiveSpec("PROJECTOR_MULTIPLICITY_STATS", "fourier_registers_k", "multiplicity_statistics", "CAP-KRONECKER-SHARP-BQP", True, "Estimate invariant-space or multiplicity statistics."),
        PrimitiveSpec(
            "DIAGONAL_JM_LABEL_TRANSFORM",
            "fourier_registers_k",
            "jm_labelled_registers",
            "CAP-DIAGONAL-JM-LABEL-TRANSFORM",
            True,
            "Measure or coherently expose target tableau/Gelfand--Tsetlin labels while retaining multiplicity degeneracy.",
        ),
        PrimitiveSpec(
            "KRONECKER_MULTIPLICITY_BASIS",
            "jm_labelled_registers",
            "pair_coupled_registers",
            "CAP-GAPPED-KRONECKER-MULTIPLICITY-TRANSFORM",
            False,
            "Resolve a uniformly gapped bounded-support commutant Hamiltonian in each residual multiplicity register.",
        ),
        PrimitiveSpec("INTERNAL_KRONECKER_TRANSFORM", "fourier_registers_k", "pair_coupled_registers", "CAP-INTERNAL-SN-KRONECKER-TRANSFORM", False, "Resolve pair irreps and multiplicity bases coherently."),
        PrimitiveSpec("RESTRICTED_MULTIPLICITY_FREE_TRANSFORM", "fourier_registers_k", "pair_coupled_registers", "CAP-RESTRICTED-MULTIPLICITY-ESTIMATION", True, "Use an exceptional multiplicity-free or commuting promise."),
        PrimitiveSpec("SINGLE_TREE_RECOUPLING", "pair_coupled_registers", "tree_coupled_registers", "CAP-SINGLE-TREE-RECOUPLING", True, "Recouple in one fixed binary tree."),
        PrimitiveSpec("TREE_SPECTRUM_FILTER", "tree_coupled_registers", "measurement_outcome", "CAP-SPECTRUM-RANK-PGM", True, "Apply a spectrum/rank-derived measurement in that tree."),
        PrimitiveSpec("RACAH_ASSOCIATOR_NETWORK", "pair_coupled_registers", "globally_coupled_registers", "CAP-KCOPY-RACAH-ASSOCIATOR", False, "Move coherently among overlapping recoupling trees."),
        PrimitiveSpec("TRANSITION_FRAME_FILTER", "globally_coupled_registers", "measurement_outcome", "CAP-STATE-TRANSITION-FILTER", False, "Implement state-dependent frame inverse/transition weights."),
        PrimitiveSpec("TENSOR_NETWORK_ASSOCIATOR", "fourier_registers_k", "measurement_outcome", "CAP-TENSOR-ASSOCIATOR", False, "Approximate recoupling and frame action by a tensor network."),
        PrimitiveSpec("LABEL_DECODER", "irrep_labels", "hidden_candidate", "CAP-HIDDEN-INVOLUTION-OUTCOME-DECODER", False, "Decode from weak labels."),
        PrimitiveSpec("STATISTICS_DECODER", "multiplicity_statistics", "hidden_candidate", "CAP-HIDDEN-INVOLUTION-OUTCOME-DECODER", False, "Decode from multiplicity statistics."),
        PrimitiveSpec("OUTCOME_DECODER", "measurement_outcome", "hidden_candidate", "CAP-HIDDEN-INVOLUTION-OUTCOME-DECODER", False, "Decode a compressed collective outcome."),
        PrimitiveSpec("CLASSICAL_VERIFY", "hidden_candidate", "verified_solution", "CAP-CLASSICAL-VERIFY", True, "Verify a proposed hidden permutation on the natural instance."),
    )
}


TEMPLATES = (
    MechanismTemplate(
        "MECH-QFT-WEAK-LABELS",
        "Registerwise QFT and weak label decoding",
        ("PREPARE_COSET_K", "SN_QFT_K", "WEAK_LABEL_MEASUREMENT", "LABEL_DECODER", "CLASSICAL_VERIFY"),
        "full symmetric involution family",
        "k=poly(n)",
        ("Strong/weak Fourier sampling is already obstructed on GI-relevant symmetric HSP instances.",),
        (),
        5,
    ),
    MechanismTemplate(
        "MECH-PROJECTOR-COUNT-DECODER",
        "Kronecker projector statistics as a decoder",
        ("PREPARE_COSET_K", "SN_QFT_K", "PROJECTOR_MULTIPLICITY_STATS", "STATISTICS_DECODER", "CLASSICAL_VERIFY"),
        "full symmetric involution family",
        "k=poly(n)",
        ("Multiplicity counting or label projection does not construct state-dependent recoupling amplitudes.",),
        (),
        12,
    ),
    MechanismTemplate(
        "MECH-PAIR-TREE-RANK-PGM",
        "Recursive pairwise Kronecker tree with spectrum-rank PGM",
        ("PREPARE_COSET_K", "SN_QFT_K", "INTERNAL_KRONECKER_TRANSFORM", "SINGLE_TREE_RECOUPLING", "TREE_SPECTRUM_FILTER", "OUTCOME_DECODER", "CLASSICAL_VERIFY"),
        "full symmetric involution family",
        "k=poly(n), including k>=3",
        (
            "The two-copy rank-only mixed-state PGM formula is false on S_3.",
            "At k=3, overlapping pair class sums satisfy an all-n nonzero commutator and do not share one tree basis.",
        ),
        (),
        25,
    ),
    MechanismTemplate(
        "MECH-RESTRICTED-COMMUTING-CLASS",
        "Multiplicity-free or commuting-class recoupling",
        ("PREPARE_COSET_K", "SN_QFT_K", "RESTRICTED_MULTIPLICITY_FREE_TRANSFORM", "SINGLE_TREE_RECOUPLING", "TREE_SPECTRUM_FILTER", "OUTCOME_DECODER", "CLASSICAL_VERIFY"),
        "exceptional commuting or dimension-ratio-restricted subfamilies",
        "k=O(1) or restricted",
        (
            "Exceptional commuting classes do not cover the full natural reduction family.",
            "Many restricted multiplicity instances have polynomial classical algorithms.",
        ),
        ("Supply a model-preserving natural-problem reduction if any restricted family is retained.",),
        18,
    ),
    MechanismTemplate(
        "MECH-JM-LABEL-MULTIPLICITY-RECOUPLING",
        "YJM label front end with explicit residual multiplicity-space recoupling",
        (
            "PREPARE_COSET_K",
            "SN_QFT_K",
            "DIAGONAL_JM_LABEL_TRANSFORM",
            "KRONECKER_MULTIPLICITY_BASIS",
            "RACAH_ASSOCIATOR_NETWORK",
            "TRANSITION_FRAME_FILTER",
            "OUTCOME_DECODER",
            "CLASSICAL_VERIFY",
        ),
        "full reduction-backed symmetric involution family",
        "k=poly(n)",
        (),
        (
            "Prove an inverse-polynomial LCU-normalized gap for the commutant Hamiltonian on all source sectors.",
            "Prove polynomial Racah/associator moves between overlapping subset coupling trees.",
            "Block-encode the state-dependent transition filter with controlled conditioning.",
            "Decode the hidden involution and beat legal graph/code baselines on the source family.",
        ),
        104,
    ),
    MechanismTemplate(
        "MECH-FULL-RECOUPLING-TRANSITION-DECODER",
        "Full coherent recoupling, transition filter, and decoder",
        ("PREPARE_COSET_K", "SN_QFT_K", "INTERNAL_KRONECKER_TRANSFORM", "RACAH_ASSOCIATOR_NETWORK", "TRANSITION_FRAME_FILTER", "OUTCOME_DECODER", "CLASSICAL_VERIFY"),
        "full reduction-backed symmetric involution family",
        "k=poly(n)",
        (),
        (
            "Prove a uniform internal S_n Kronecker transform with multiplicity basis and precision bounds.",
            "Prove a polynomial Racah/associator network for all overlapping subset terms at growing k.",
            "Block-encode state-dependent transition weights and control inverse-frame conditioning.",
            "Decode the hidden involution and beat all legal graph/code baselines on a natural family.",
        ),
        100,
    ),
    MechanismTemplate(
        "MECH-TENSOR-ASSOCIATOR-DECODER",
        "Implicit tensor-network associator and compressed decoder",
        ("PREPARE_COSET_K", "SN_QFT_K", "TENSOR_NETWORK_ASSOCIATOR", "OUTCOME_DECODER", "CLASSICAL_VERIFY"),
        "full reduction-backed symmetric involution family",
        "k=poly(n)",
        (),
        (
            "Prove polynomial bond dimension and contraction/circuit cost at inverse-polynomial error.",
            "Show the tensor network is not a classical invariant shadow or efficiently contractible dequantization.",
            "Prove robust hidden-involution decoding from its compressed outcome."
        ),
        72,
    ),
)


def evaluate_template(template: MechanismTemplate) -> MechanismEvaluation:
    issues: list[str] = []
    current_type = "start"
    missing: list[str] = []
    for stage_id in template.stages:
        primitive = PRIMITIVES[stage_id]
        if primitive.input_type != current_type:
            issues.append(
                f"{stage_id} expects {primitive.input_type}, received {current_type}"
            )
        current_type = primitive.output_type
        if not primitive.available_with_uniform_proof:
            missing.append(primitive.capability_id)
    if current_type != "verified_solution":
        issues.append(f"mechanism terminates at {current_type}, not verified_solution")
    full_coverage = "full" in template.source_family_scope and "restricted" not in template.source_family_scope
    if issues or template.known_no_go_violations:
        decision = "rejected"
        rationale = "Known no-go or typed-interface failure invalidates the architecture."
    elif missing:
        decision = "proposal-only-missing-proof-capabilities"
        rationale = "The architecture targets the right interface but names unimplemented proof-critical primitives."
    elif not full_coverage:
        decision = "rejected-reduction-coverage"
        rationale = "The mechanism does not cover the source family inherited from the reduction."
    else:
        decision = "proof-gate-eligible"
        rationale = "All typed stages and capability proofs are present; submit the full candidate schema."
    proof_gate_eligible = decision == "proof-gate-eligible"
    priority = template.upside_score - 20 * len(template.known_no_go_violations) - 5 * len(issues)
    return MechanismEvaluation(
        id=template.id,
        title=template.title,
        stages=template.stages,
        typed_interfaces_valid=not issues,
        interface_issues=issues,
        missing_capabilities=sorted(set(missing)),
        known_no_go_violations=list(template.known_no_go_violations),
        additional_proof_obligations=list(template.additional_proof_obligations),
        holevo_copy_budget_obligation_attached=True,
        minimum_copy_budget_rule=(
            "k >= ceil([log2|C|-h2(epsilon)-epsilon*log2(|C|-1)]/chi_1), "
            "with chi_1 from the exact involution character formula"
        ),
        full_source_family_coverage=full_coverage,
        proof_gate_eligible=proof_gate_eligible,
        decision=decision,
        priority_score=max(0, priority),
        rationale=rationale,
    )


def build_recoupling_mutation_proposals(
    evaluations: Sequence[MechanismEvaluation] | None = None,
) -> list[dict]:
    active = list(evaluations) if evaluations is not None else [
        evaluate_template(template) for template in TEMPLATES
    ]
    proposals = []
    for evaluation in active:
        if not evaluation.decision.startswith("proposal-only"):
            continue
        proposals.append(
            {
                "id": f"MUTATE-CODE-COSET-COLLECTIVE-{evaluation.id.removeprefix('MECH-')}",
                "created_at": utc_now(),
                "source_candidate_id": DEFAULT_CANDIDATE_ID,
                "status": "proposal",
                "formalization_status": "typed-architecture-proof-capabilities-missing",
                "proof_gate_eligible": False,
                "mutation_type": "typed-recoupling-mechanism",
                "rationale": evaluation.rationale,
                "new_hypothesis": evaluation.title,
                "typed_stages": list(evaluation.stages),
                "required_modules": evaluation.missing_capabilities,
                "proof_obligations_to_resolve": evaluation.additional_proof_obligations,
                "rejection_filters": [
                    "Reject if any missing capability is replaced by an undefined circuit box.",
                    "Reject if the mechanism covers only an exceptional commuting or classically tractable family.",
                    "Reject if the decoder is distinguishability or verification without hidden-involution recovery.",
                    "Reject if classical invariant or tensor-network contraction reproduces the outcome."
                ],
                "linked_blockers": [
                    "DEQ-COSET-SOLVED-QFT-COUNTING-NOT-RECOUPLING-DECODER",
                    "DEQ-COSET-K3-SINGLE-RECOUPLING-BASIS-OBSTRUCTED",
                    "DEQ-COSET-EXPLICIT-TWO-COPY-TRANSITIONS-FACTORIAL",
                ],
                "proof_debts_targeted": evaluation.missing_capabilities,
                "priority_score": evaluation.priority_score,
            }
        )
    return proposals


def build_recoupling_mechanism_synthesis_report() -> RecouplingMechanismSynthesisReport:
    evaluations = [evaluate_template(template) for template in TEMPLATES]
    proposals = build_recoupling_mutation_proposals(evaluations)
    survivors = sorted(
        (item for item in evaluations if item.decision != "rejected"),
        key=lambda item: (-item.priority_score, item.id),
    )
    metrics: dict[str, int | float] = {
        "primitive_count": len(PRIMITIVES),
        "mechanism_count": len(evaluations),
        "typed_interface_valid_count": sum(item.typed_interfaces_valid for item in evaluations),
        "known_no_go_rejected_count": sum(item.decision == "rejected" for item in evaluations),
        "proposal_only_count": sum(item.decision.startswith("proposal-only") for item in evaluations),
        "proof_gate_eligible_count": sum(item.proof_gate_eligible for item in evaluations),
        "automatically_promoted_candidate_count": 0,
        "holevo_copy_budget_rule_count": 1,
        "undercharged_mechanism_promoted_count": 0,
        "highest_survivor_priority_score": max((item.priority_score for item in survivors), default=0),
        "minimum_missing_capability_count": min(
            (len(item.missing_capabilities) for item in survivors), default=0
        ),
    }
    return RecouplingMechanismSynthesisReport(
        created_at=utc_now(),
        primitive_specs=list(PRIMITIVES.values()),
        evaluations=evaluations,
        ranked_survivors=[item.id for item in survivors],
        mutation_proposals=proposals,
        headline_metrics=metrics,
        claim_gate={
            "known_invalid_architectures_rejected": True,
            "exact_holevo_copy_budget_attached": all(
                item.holevo_copy_budget_obligation_attached for item in evaluations
            ),
            "undercharged_mechanism_promoted": False,
            "undefined_circuit_boxes_promoted": False,
            "proof_gate_eligible_mechanism_exists": metrics["proof_gate_eligible_count"] > 0,
            "speedup_claim_allowed": False,
            "reason": (
                "The only surviving architectures explicitly require unproved internal recoupling, transition/filter, "
                "and decoder capabilities; known shortcuts are rejected."
            ),
        },
        status="typed-mutations-ranked-no-proof-gate-eligible-mechanism",
        summary=(
            f"Evaluated {len(evaluations)} typed collective-measurement architectures, rejected "
            f"{metrics['known_no_go_rejected_count']} known-invalid shortcuts, and retained "
            f"{metrics['proposal_only_count']} proof-capability research proposals without promoting candidates."
        ),
        falsifiers_triggered=[
            "QFT-only weak-label decoding is a known no-go route.",
            "Multiplicity statistics are not a coherent transform or decoder.",
            "Spectrum-rank PGM and one-tree k-copy recursion fail exact finite/all-n tests.",
            "Exceptional commuting or restricted multiplicity families do not inherit full source-family reductions.",
            "No surviving architecture currently satisfies every proof-critical capability."
            ,
            "Every architecture must also satisfy the exact class-specific Holevo/Fano copy budget; that polynomial "
            "budget is not a substitute for a measurement circuit."
        ],
    )


def write_recoupling_mechanism_synthesis_report(
    output_path: Path = COSET_RECOUPLING_SYNTHESIS_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_recoupling_mechanism_synthesis_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        for proposal in payload["mutation_proposals"]:
            upsert_mutation_proposal(proposal)
        for evaluation in payload["evaluations"]:
            if not evaluation["decision"].startswith("rejected"):
                continue
            upsert_negative_result(
                NegativeResultRecord(
                    id=f"NEG-{evaluation['id']}",
                    source=str(output_path),
                    claim=f"{evaluation['title']} is eligible for promotion as a collective algorithm.",
                    reason_invalid=" | ".join(
                        evaluation["known_no_go_violations"] + evaluation["interface_issues"]
                    )
                    or evaluation["rationale"],
                    lesson="Compose only typed, scope-matched primitives and retain every unproved circuit or decoder as proof debt.",
                    applies_to=[registry_candidate_id, registry_experiment_id],
                    evidence={"stages": evaluation["stages"], "decision": evaluation["decision"]},
                )
            )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-LATEST"
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
                artifacts={"coset_recoupling_mechanism_synthesis": str(output_path)},
            )
        )
    return payload
