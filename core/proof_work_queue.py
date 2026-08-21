"""Prioritized proof-debt work queue.

The proof tracker records obligations, lemmas, reductions, and counterexample
searches.  This module turns those records into an actionable queue: which
claim is blocked, which artifact currently blocks it, what executable command
or theory step should be run next, and what would falsify or discharge it.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import load_candidates, utc_now


PROOF_WORK_QUEUE_PATH = Path("research/proof_work_queue.json")
PROOF_DEBT_REPORT_PATH = Path("research/proof_debt_report.json")
BLOCKER_TAXONOMY_PATH = Path("research/blocker_taxonomy.json")
FRONTIER_MAP_PATH = Path("research/frontier_map.json")
MUTATION_REPORT_PATH = Path("research/mutation_report.json")
EXPERIMENT_TRENDS_PATH = Path("research/experiment_trends.json")
DCP_CONTAMINATED_PGM_PATH = Path("research/phase_workbench/dcp_contaminated_pgm_audit.json")
DCP_SUBSET_SUM_BRIDGE_PATH = Path("research/reductions/dcp_subset_sum_bridge.json")
DCP_SUBSET_SUM_LATTICE_PATH = Path("research/classical_baselines/dcp_subset_sum_lattice_search.json")
DCP_SUBSET_SUM_TWO_ADIC_PATH = Path("research/classical_baselines/dcp_subset_sum_two_adic_search.json")
DCP_SUBSET_SUM_RESOURCE_FRONTIER_PATH = Path("research/classical_baselines/dcp_subset_sum_resource_frontier.json")
DCP_SUBSET_SUM_CARRY_ANF_PATH = Path("research/classical_baselines/dcp_subset_sum_carry_anf.json")


@dataclass(frozen=True)
class ProofWorkItem:
    id: str
    priority_score: int
    candidate_id: str
    work_type: str
    claim: str
    blocker: str
    recommended_action: str
    recommended_command: str
    success_criterion: str
    kill_criterion: str
    dependencies: list[str]
    linked_debts: list[str]
    linked_artifacts: list[str]
    status: str


def _read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return fallback


def _candidate_kind(candidate_id: str) -> str:
    lower = candidate_id.lower()
    if "dhs" in lower or "hidden" in lower:
        return "hidden-shift"
    if "code" in lower or "coset" in lower or "cfi" in lower:
        return "coset-code"
    return "general"


def _is_state_native_dcp(candidate_id: str) -> bool:
    for candidate in load_candidates():
        if candidate.get("id") != candidate_id:
            continue
        input_model = str(candidate.get("input_model", "")).lower()
        return "independent coset-state samples" in input_model or "independent dcp" in input_model
    return False


def _top_blocker() -> str:
    blockers = _read_json(BLOCKER_TAXONOMY_PATH, {})
    return str(blockers.get("top_actionable_blocker_class", "") or blockers.get("top_blocker_class", ""))


def _blocker_score(blocker_class: str) -> int:
    blockers = _read_json(BLOCKER_TAXONOMY_PATH, {})
    for item in blockers.get("classes", []):
        if item.get("blocker_class") == blocker_class:
            return int(item.get("priority_score", 0) or 0)
    return 0


def _frontier_bonus(candidate_id: str) -> int:
    frontier = _read_json(FRONTIER_MAP_PATH, {})
    top = str(frontier.get("top_frontier", ""))
    kind = _candidate_kind(candidate_id)
    if top == "nonabelian-coset-collective-observables" and kind == "coset-code":
        return 30
    if top == "code-equivalence-hard-family-search" and "code" in candidate_id.lower():
        return 25
    if top in {
        "hidden-shift-phase-family-generation",
        "character-shift-decoding-lower-bound",
        "dcp-recursive-decoder-asymptotics",
        "dcp-density-one-subset-sum-partial-solver",
        "dcp-f1-contamination-tolerant-decoder",
    } and kind == "hidden-shift":
        return 20
    return 0


def _stale_trend_penalty(command_hint: str) -> int:
    trends = _read_json(EXPERIMENT_TRENDS_PATH, {})
    text = command_hint.lower()
    for item in trends.get("trends", []):
        experiment_id = str(item.get("experiment_id", "")).lower()
        if experiment_id and any(token in experiment_id for token in text.split() if token.startswith("exp-")):
            return min(20, 2 * int(item.get("run_count", 0) or 0))
    return 0


def _action_for_debt(debt: dict[str, Any]) -> tuple[str, str, str, str, str, list[str], list[str], str]:
    candidate_id = str(debt.get("candidate_id", ""))
    evidence = str(debt.get("evidence", "")).lower()
    kind = _candidate_kind(candidate_id)
    if debt.get("debt_type") == "reduction-route" or "no complete certificate-gated" in evidence:
        return (
            "reduction-route-certification",
            "Compose the exact primary-source theorem contract with a complete candidate edge whose access, group, promise, overhead, uniformity, family coverage, and decoder all pass the gate.",
            "python qsearch.py reduction-contracts && python qsearch.py reductions && python qsearch.py conjectures && python qsearch.py proofs",
            "At least one natural-problem route for the candidate has status complete-certified-route.",
            "Every route retains a blocked family-specialization or model-preservation edge.",
            [
                "reduction_theorem_catalog.py",
                "reduction_contract_audit.py",
                "reduction_gate.py",
                "proof_tracker.py",
                "conjecture_tracker.py",
            ],
            [
                "research/reductions/theorem_contracts.json",
                "research/reductions/interface_audit.json",
                "research/reductions/reduction_ledger.json",
                "research/registry/reductions.json",
                "research/proof_debt_report.json",
            ],
            "theory-or-mixed",
        )
    if kind == "coset-code":
        top_blocker = _top_blocker()
        if (
            top_blocker == "code-equivalence-invariant-collapse"
            or "code" in evidence
            or "support" in evidence
            or "matroid" in evidence
            or "low-weight" in evidence
            or "closure" in evidence
            or "conductor" in evidence
            or "tuple" in evidence
            or "canonical" in evidence
            or "information-set" in evidence
        ):
            return (
                "code-family-hardening",
                "Search algebraic code families that survive Schur products, conductor/t-closure support recovery, low-weight matroid, structural, tuple-profile, automorphism, and aggregate code-triage baselines before coset use.",
                "python qsearch.py code-cyclic-search && python qsearch.py code-bch-search && python qsearch.py code-goppa-search && python qsearch.py code-tanner-search && python qsearch.py code-rm-search && python qsearch.py code-pg-search && python qsearch.py code-qc-search && python qsearch.py code-qc-canonicalize && python qsearch.py code-qc-info-resolve && python qsearch.py code-low-weight && python qsearch.py code-schur-filtration && python qsearch.py code-closure-attack && python qsearch.py code-triage && python qsearch.py mutate",
                "A non-equivalent code family row survives code_frontier_triage.py as proof debt rather than rejection or equivalent control.",
                "Rows are rejected or classified as equivalent/no-hard controls by code_frontier_triage.py.",
                [
                    "cyclic_code_search.py",
                    "bch_code_search.py",
                    "goppa_code_search.py",
                    "tanner_code_search.py",
                    "reed_muller_code_search.py",
                    "projective_geometry_code_search.py",
                    "quasi_cyclic_code_search.py",
                    "quasi_cyclic_canonicalization.py",
                    "qc_information_set_resolver.py",
                    "code_low_weight_structure.py",
                    "code_schur_filtration.py",
                    "code_closure_attack.py",
                    "code_frontier_triage.py",
                    "mutation_engine.py",
                ],
                [
                    "research/code_equivalence/cyclic_code_search.json",
                    "research/code_equivalence/bch_code_search.json",
                    "research/code_equivalence/goppa_code_search.json",
                    "research/code_equivalence/tanner_code_search.json",
                    "research/code_equivalence/reed_muller_code_search.json",
                    "research/code_equivalence/projective_geometry_code_search.json",
                    "research/code_equivalence/quasi_cyclic_code_search.json",
                    "research/code_equivalence/quasi_cyclic_canonicalization.json",
                    "research/code_equivalence/qc_information_set_resolver.json",
                    "research/code_equivalence/code_low_weight_structure.json",
                    "research/code_equivalence/code_schur_filtration.json",
                    "research/code_equivalence/code_closure_attack.json",
                    "research/code_equivalence/code_frontier_triage.json",
                ],
                "ready-to-run",
            )
        if "triage" in evidence or "coset" in evidence or "wl" in evidence or "graph" in evidence or "pgm" in evidence or "measurement" in evidence:
            return (
                "coset-triage-escape-search",
                "Generate or import natural graph/coset rows, then reject every row that fails the aggregate triage gate.",
                "python qsearch.py gm-switching && python qsearch.py weak-fourier && python qsearch.py coset-distinguishability && python qsearch.py coset-pgm && python qsearch.py coset-triage && python qsearch.py mutate",
                "At least one scalable row survives coset_frontier_triage.py without relying on skipped tuple caps.",
                "All generated rows are triage-rejected or survive only because a classical baseline was capped.",
                ["godsil_mckay_search.py", "weak_fourier_signal.py", "coset_state_distinguishability.py", "coset_pgm_capacity.py", "coset_frontier_triage.py", "mutation_engine.py"],
                [
                    "research/coset_workbench/godsil_mckay_switching_search.json",
                    "research/representation/weak_fourier_involution_signal.json",
                    "research/representation/coset_state_distinguishability.json",
                    "research/representation/coset_pgm_capacity.json",
                    "research/coset_workbench/coset_frontier_triage.json",
                ],
                "ready-to-run",
            )
        return (
            "code-family-hardening",
            "Search algebraic code families that survive Schur products, conductor/t-closure support recovery, low-weight matroid, structural, tuple-profile, and canonicalization baselines before coset use.",
            "python qsearch.py code-cyclic-search && python qsearch.py code-bch-search && python qsearch.py code-goppa-search && python qsearch.py code-tanner-search && python qsearch.py code-rm-search && python qsearch.py code-pg-search && python qsearch.py code-qc-search && python qsearch.py code-qc-canonicalize && python qsearch.py code-qc-info-resolve && python qsearch.py code-low-weight && python qsearch.py code-schur-filtration && python qsearch.py code-closure-attack && python qsearch.py code-triage",
            "A non-equivalent code family row survives tuple profiles, information sets, automorphism-aware canonicalization, and code triage.",
            "Rows are separated by support splitting, tuple profiles, information-set canonicalization, exact canonical forms, or code triage.",
            ["cyclic_code_search.py", "bch_code_search.py", "goppa_code_search.py", "tanner_code_search.py", "reed_muller_code_search.py", "projective_geometry_code_search.py", "quasi_cyclic_code_search.py", "code_information_set_baseline.py", "quasi_cyclic_canonicalization.py", "qc_information_set_resolver.py", "code_low_weight_structure.py", "code_schur_filtration.py", "code_closure_attack.py", "code_frontier_triage.py"],
            [
                "research/code_equivalence/cyclic_code_search.json",
                "research/code_equivalence/bch_code_search.json",
                "research/code_equivalence/goppa_code_search.json",
                "research/code_equivalence/tanner_code_search.json",
                "research/code_equivalence/reed_muller_code_search.json",
                "research/code_equivalence/projective_geometry_code_search.json",
                "research/code_equivalence/quasi_cyclic_code_search.json",
                "research/code_equivalence/qc_information_set_resolver.json",
                "research/code_equivalence/code_information_set_baseline.json",
                "research/code_equivalence/code_low_weight_structure.json",
                "research/code_equivalence/code_schur_filtration.json",
                "research/code_equivalence/code_closure_attack.json",
                "research/code_equivalence/code_frontier_triage.json",
            ],
            "ready-to-run",
        )
    if kind == "hidden-shift":
        if _is_state_native_dcp(candidate_id):
            bridge_metrics = _read_json(DCP_SUBSET_SUM_BRIDGE_PATH, {}).get("headline_metrics", {})
            contaminated_pgm_metrics = _read_json(DCP_CONTAMINATED_PGM_PATH, {}).get("headline_metrics", {})
            source_bridge_verified = int(
                bridge_metrics.get("primary_source_conditional_dcp_reduction_count", 0) or 0
            ) > 0
            partial_solver_open = not int(
                bridge_metrics.get("proved_polynomial_partial_average_subset_sum_solver_count", 0) or 0
            )
            information_robustness_proved = int(
                contaminated_pgm_metrics.get("proved_exact_f1_information_robustness_count", 0) or 0
            ) > 0
            if source_bridge_verified and partial_solver_open and information_robustness_proved:
                return (
                    "dcp-density-one-partial-subset-sum-solver",
                    "Construct a deterministic or explicit target-independent shared-seed randomized polynomial-time partial solver for random density-one modular subset sum with uniform inverse-polynomial legal-input coverage. For a genuinely quantum relation solver, prove a target-independent decomposition or paired-workspace fidelity.",
                    "python qsearch.py dcp-subset-sum-bridge && python qsearch.py dcp-coherent-matching && python qsearch.py dcp-subset-sum-randomize && python qsearch.py dcp-odd-unit-geometry && python qsearch.py dcp-subset-sum-resource-frontier && python qsearch.py dcp-subset-sum-lattice && python qsearch.py dcp-subset-sum-two-adic && python qsearch.py dcp-subset-sum-carry-anf && python qsearch.py dcp-subset-sum-low-bit-bdd && python qsearch.py dcp-subset-sum-conditioned-quotient && python qsearch.py dcp-subset-sum-carry-slice-lattice && python qsearch.py dcp-subset-sum-target-distribution && python qsearch.py dcp-subset-sum-synthesize && python qsearch.py dcp-decoder-frontier && python qsearch.py proofs && python qsearch.py mutate",
                    "At least one source-contract row has a uniform inverse-polynomial legal-input coverage theorem, polynomial time and memory, verified witnesses, and a deterministic, shared-seed randomized, or algorithm-specific coherent interface.",
                    "Success collapses in the scaling tail, covers only polynomially many explicit candidates, uses target-dependent or measured coins, or leaves paired quantum workspaces with vanishing overlap.",
                    [
                        "dcp_subset_sum_bridge.py",
                        "dcp_subset_sum_lattice_search.py",
                        "dcp_subset_sum_two_adic_search.py",
                        "dcp_subset_sum_resource_frontier.py",
                        "dcp_subset_sum_carry_anf.py",
                        "dcp_subset_sum_solver_synthesis.py",
                        "dcp_subset_sum_low_bit_bdd.py",
                        "dcp_subset_sum_conditioned_quotient.py",
                        "dcp_subset_sum_carry_slice_lattice.py",
                        "dcp_subset_sum_target_distribution.py",
                        "dcp_coherent_matching_interface.py",
                        "dcp_subset_sum_random_self_reduction.py",
                        "dcp_odd_unit_orbit_geometry.py",
                        "dcp_decoder_frontier.py",
                        "proof_tracker.py",
                        "mutation_engine.py",
                    ],
                    [
                        "research/reductions/dcp_subset_sum_bridge.json",
                        "research/classical_baselines/dcp_subset_sum_lattice_search.json",
                        "research/classical_baselines/dcp_subset_sum_two_adic_search.json",
                        "research/classical_baselines/dcp_subset_sum_resource_frontier.json",
                        "research/classical_baselines/dcp_subset_sum_carry_anf.json",
                        "research/hypotheses/dcp_subset_sum_solver_synthesis.json",
                        "research/classical_baselines/dcp_subset_sum_low_bit_bdd.json",
                        "research/classical_baselines/dcp_subset_sum_conditioned_quotient.json",
                        "research/classical_baselines/dcp_subset_sum_carry_slice_lattice.json",
                        "research/classical_baselines/dcp_subset_sum_target_distribution.json",
                        "research/reductions/dcp_coherent_matching_interface.json",
                        "research/reductions/dcp_subset_sum_random_self_reduction.json",
                        "research/classical_baselines/dcp_odd_unit_orbit_geometry.json",
                        "research/phase_workbench/dcp_decoder_frontier.json",
                        "research/proof_debt_report.json",
                        "research/mutation_report.json",
                    ],
                    "theory-and-experiment",
                )
            return (
                "dcp-f1-collective-robustness-proof",
                "Construct a polynomial-description collective common-reflection measurement, prove its error under arbitrary f=1 basis-state contamination, then compose it with a shallow full-reflection decoder and named resource baselines.",
                "python qsearch.py dcp-contamination && python qsearch.py dcp-witness-search && python qsearch.py dcp-clifford-witnesses && python qsearch.py dcp-clifford-contamination && python qsearch.py dcp-hadamard-scaling && python qsearch.py dcp-random-decoder && python qsearch.py dcp-multiscale-aliasing && python qsearch.py dcp-decoder-frontier && python qsearch.py dcp-bad-registers && python qsearch.py reduction-contracts && python qsearch.py proofs",
                "A machine-checkable collective measurement and decoder achieve inverse-polynomial success in polynomial time on the exact f=1 DCP promise without hidden validity flags.",
                "The signal is locally indistinguishable, needs exponential subset-sum enumeration, or arbitrary bad states erase the full-decoder advantage.",
                [
                    "dcp_contamination_witness.py",
                    "dcp_collective_witness_search.py",
                    "dcp_clifford_witness_search.py",
                    "dcp_clifford_contamination.py",
                    "dcp_hadamard_scaling.py",
                    "dcp_random_design_decoder.py",
                    "dcp_decoder_frontier.py",
                    "dcp_multiscale_aliasing_audit.py",
                    "dcp_bad_register_audit.py",
                    "dcp_sample_workbench.py",
                    "dcp_recursive_decoder.py",
                    "dcp_recurrence_analysis.py",
                    "reduction_contract_audit.py",
                    "proof_tracker.py",
                ],
                [
                    "research/phase_workbench/dcp_contamination_witness.json",
                    "research/phase_workbench/dcp_collective_witness_search.json",
                    "research/phase_workbench/dcp_clifford_witness_search.json",
                    "research/phase_workbench/dcp_clifford_contamination.json",
                    "research/phase_workbench/dcp_hadamard_scaling.json",
                    "research/classical_baselines/dcp_random_design_decoder.json",
                    "research/phase_workbench/dcp_decoder_frontier.json",
                    "research/classical_baselines/dcp_multiscale_aliasing_audit.json",
                    "research/phase_workbench/dcp_bad_register_audit.json",
                    "research/phase_workbench/dcp_sample_native_sieve.json",
                    "research/phase_workbench/dcp_recursive_decoder.json",
                    "research/phase_workbench/dcp_recurrence_analysis.json",
                    "research/reductions/interface_audit.json",
                    "research/proof_debt_report.json",
                ],
                "theory-and-experiment",
            )
        if "query" in evidence or "sample" in evidence or "coherent" in evidence:
            return (
                "query-model-lower-bound",
                "Formalize which classical access models are legal, then rerun sample/evaluator baselines at collision-scale budgets.",
                "python qsearch.py dcp-samples && python qsearch.py dcp-decode && python qsearch.py query-lower-bounds && python qsearch.py character-query-info && python qsearch.py character-lower-bound && python qsearch.py character-moments && python qsearch.py query-models && python qsearch.py baselines && python qsearch.py character-decoders",
                "Every legal classical baseline is either superpolynomial under the stated model or has a recorded lower-bound obligation.",
                "A legal evaluator, sample, sparse Fourier, or character decoder recovers the shift.",
                [
                    "hidden_shift_query_lower_bounds.py",
                    "dcp_sample_workbench.py",
                    "dcp_recursive_decoder.py",
                    "query_model_ledger.py",
                    "classical_baseline_suite.py",
                    "character_decoder_search.py",
                    "character_query_information.py",
                    "character_shift_lower_bound.py",
                    "character_moment_obstruction.py",
                ],
                [
                    "research/classical_baselines/hidden_shift_query_lower_bounds.json",
                    "research/phase_workbench/dcp_sample_native_sieve.json",
                    "research/phase_workbench/dcp_recursive_decoder.json",
                    "research/query_model_ledger.json",
                    "research/classical_baselines/hidden_shift_baselines.json",
                    "research/classical_baselines/character_decoder_search.json",
                    "research/classical_baselines/character_query_information.json",
                    "research/classical_baselines/character_shift_lower_bound.json",
                    "research/classical_baselines/character_moment_obstruction.json",
                ],
                "ready-to-run",
            )
        return (
            "learnability-counterexample-search",
            "Try to kill the hidden-shift family with low-degree, sparse Fourier, finite-difference, and chosen-query attacks.",
            "python qsearch.py learnability && python qsearch.py fourier-learnability && python qsearch.py trace-functions",
            "A natural family survives low-degree, sparse-spectrum, sample, and evaluator attacks with an attached reduction.",
            "Any learner reconstructs the phase or shift with polynomial samples/queries under a legal model.",
            ["learnability_baselines.py", "fourier_compressibility_baselines.py", "trace_function_search.py"],
            [
                "research/classical_baselines/learnability_baselines.json",
                "research/classical_baselines/fourier_compressibility_baselines.json",
            ],
            "ready-to-run",
        )
    return (
        "formalization",
        "Turn the candidate into an asymptotic theorem or reject it as non-formalizable.",
        "python qsearch.py proofs && python qsearch.py conjectures",
        "The candidate has explicit parameters, input model, mechanism, success theorem, and falsifiers.",
        "The statement cannot be made asymptotic or duplicates a known negative result.",
        ["proof_tracker.py", "conjecture_tracker.py"],
        ["research/proof_debt_report.json", "research/conjecture_report.json"],
        "theory-required",
    )


def _work_item_from_debt(debt: dict[str, Any]) -> ProofWorkItem:
    candidate_id = str(debt.get("candidate_id", "unknown"))
    work_type, action, command, success, kill, dependencies, artifacts, status = _action_for_debt(debt)
    top_blocker = _top_blocker()
    blocker_bonus = min(40, _blocker_score(top_blocker) // 300) if top_blocker else 0
    priority = (
        int(debt.get("priority_score", 0) or 0)
        + _frontier_bonus(candidate_id)
        + blocker_bonus
        - _stale_trend_penalty(command)
    )
    return ProofWorkItem(
        id=f"WORK-{debt.get('id', candidate_id)}-{work_type}".upper().replace("_", "-"),
        priority_score=priority,
        candidate_id=candidate_id,
        work_type=work_type,
        claim=str(debt.get("claim_blocked", "")),
        blocker=top_blocker or str(debt.get("debt_type", "")),
        recommended_action=action,
        recommended_command=command,
        success_criterion=success,
        kill_criterion=kill,
        dependencies=dependencies,
        linked_debts=[str(debt.get("id", ""))],
        linked_artifacts=artifacts,
        status=status,
    )


def _lemma_work_items(existing_ids: set[str]) -> list[ProofWorkItem]:
    debt_report = _read_json(PROOF_DEBT_REPORT_PATH, {})
    items: list[ProofWorkItem] = []
    for lemma in debt_report.get("lemmas", []):
        candidate_id = str(lemma.get("candidate_id", "unknown"))
        if not any(dep in lemma.get("depends_on", []) for dep in ["PO-DEQUANTIZATION", "PO-NO-GO", "PO-REDUCTION"]):
            continue
        work_id = f"WORK-LEMMA-{lemma.get('id', candidate_id)}".upper().replace("_", "-")
        if work_id in existing_ids:
            continue
        kind = _candidate_kind(candidate_id)
        if kind == "coset-code":
            command = "python qsearch.py coset-triage && python qsearch.py representation-obstructions && python qsearch.py weak-fourier"
            artifacts = [
                "research/coset_workbench/coset_frontier_triage.json",
                "research/representation/symmetric_group_obstructions.json",
            ]
        elif kind == "hidden-shift":
            command = "python qsearch.py query-lower-bounds && python qsearch.py character-query-info && python qsearch.py character-lower-bound && python qsearch.py character-moments && python qsearch.py query-models && python qsearch.py baselines && python qsearch.py proofs"
            artifacts = [
                "research/classical_baselines/hidden_shift_query_lower_bounds.json",
                "research/query_model_ledger.json",
                "research/dequantization_attack_matrix.json",
            ]
        else:
            command = "python qsearch.py proofs"
            artifacts = ["research/proof_debt_report.json"]
        items.append(
            ProofWorkItem(
                id=work_id,
                priority_score=75 + _frontier_bonus(candidate_id),
                candidate_id=candidate_id,
                work_type="lemma-formalization",
                claim=str(lemma.get("statement", "")),
                blocker=_top_blocker() or "proof-formalization-debt",
                recommended_action=str(lemma.get("falsification_test", "")),
                recommended_command=command,
                success_criterion="Lemma is either proved with explicit assumptions or replaced by a negative result.",
                kill_criterion="The falsification test finds a legal classical attack or no-go reduction.",
                dependencies=["proof_tracker.py"],
                linked_debts=[],
                linked_artifacts=artifacts,
                status="theory-and-experiment",
            )
        )
    return items


def build_proof_work_queue(max_items: int = 30) -> dict[str, Any]:
    debt_report = _read_json(PROOF_DEBT_REPORT_PATH, {})
    work_items = [_work_item_from_debt(debt) for debt in debt_report.get("proof_debts", [])]
    existing = {item.id for item in work_items}
    work_items.extend(_lemma_work_items(existing))
    work_items.sort(key=lambda item: (-item.priority_score, item.candidate_id, item.id))
    visible = work_items[:max_items]
    executable = [item for item in visible if item.status == "ready-to-run"]
    theory = [item for item in visible if item.status != "ready-to-run"]
    clusters: dict[tuple[str, str], dict[str, Any]] = {}
    for item in visible:
        key = (item.work_type, item.recommended_command)
        cluster = clusters.setdefault(
            key,
            {
                "work_type": item.work_type,
                "recommended_command": item.recommended_command,
                "priority_score": item.priority_score,
                "affected_candidates": [],
                "linked_work_items": [],
                "success_criterion": item.success_criterion,
                "kill_criterion": item.kill_criterion,
            },
        )
        cluster["priority_score"] = max(int(cluster["priority_score"]), item.priority_score)
        if item.candidate_id not in cluster["affected_candidates"]:
            cluster["affected_candidates"].append(item.candidate_id)
        cluster["linked_work_items"].append(item.id)
    action_clusters = sorted(
        (
            {
                **cluster,
                "affected_candidate_count": len(cluster["affected_candidates"]),
            }
            for cluster in clusters.values()
        ),
        key=lambda item: (-int(item["priority_score"]), -int(item["affected_candidate_count"]), item["work_type"]),
    )
    top_item = visible[0] if visible else None
    return {
        "created_at": utc_now(),
        "work_item_count": len(visible),
        "total_candidate_work_item_count": len(work_items),
        "action_cluster_count": len(action_clusters),
        "ready_to_run_count": len(executable),
        "theory_or_mixed_count": len(theory),
        "top_work_item": asdict(top_item) if top_item else None,
        "top_action_cluster": action_clusters[0] if action_clusters else None,
        "status": "proof-work-ready" if visible else "no-proof-work",
        "action_clusters": action_clusters,
        "items": [asdict(item) for item in visible],
    }


def write_proof_work_queue(path: Path = PROOF_WORK_QUEUE_PATH, max_items: int = 30) -> dict[str, Any]:
    report = build_proof_work_queue(max_items=max_items)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True))
    return report
