"""Proof-gated research registry for Q-Search.

The registry is the new source of truth. It stores only research candidates
that pass the proof gate, experiment plans with falsifiers, and negative results
that should prevent the system from repeating dead ends.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from proof_gate import GateIssue, validate_candidate


REGISTRY_DIR = Path("research/registry")
CANDIDATES_PATH = REGISTRY_DIR / "candidates.json"
EXPERIMENTS_PATH = REGISTRY_DIR / "experiments.json"
EXPERIMENT_RESULTS_PATH = REGISTRY_DIR / "experiment_results.json"
DEQUANTIZATION_CHECKS_PATH = REGISTRY_DIR / "dequantization_checks.json"
PROOF_STATUS_PATH = REGISTRY_DIR / "proof_status.json"
SCALING_RUNS_PATH = REGISTRY_DIR / "scaling_runs.json"
CONJECTURES_PATH = REGISTRY_DIR / "conjectures.json"
MUTATION_PROPOSALS_PATH = REGISTRY_DIR / "mutation_proposals.json"
NEGATIVE_RESULTS_PATH = REGISTRY_DIR / "negative_results.json"
REJECTED_CANDIDATES_PATH = REGISTRY_DIR / "rejected_candidates.json"
REDUCTIONS_PATH = REGISTRY_DIR / "reductions.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class CandidateRecord:
    id: str
    title: str
    status: str
    created_at: str
    updated_at: str
    literature_ids: list[str]
    ontology_node_ids: list[str]
    problem_family: str
    input_model: str
    classical_baseline: str
    reduction_or_lower_bound: str
    quantum_mechanism: str
    cost_model: str
    measurement_and_decoding: str
    success_statement: str
    complexity_accounting: str
    no_go_analysis: str
    dequantization_check: str
    falsifiers: list[str]
    experiment_ids: list[str] = field(default_factory=list)
    notes: str = ""


@dataclass(frozen=True)
class ExperimentRecord:
    id: str
    candidate_id: str
    title: str
    status: str
    hypothesis: str
    protocol: str
    positive_signal: str
    falsifiers: list[str]
    metrics: list[str]
    dependencies: list[str]
    next_actions: list[str]


@dataclass(frozen=True)
class ExperimentResultRecord:
    id: str
    experiment_id: str
    candidate_id: str
    created_at: str
    status: str
    summary: str
    metrics: dict[str, Any]
    falsifiers_triggered: list[str]
    artifacts: dict[str, str]


@dataclass(frozen=True)
class NegativeResultRecord:
    id: str
    source: str
    claim: str
    reason_invalid: str
    lesson: str
    applies_to: list[str]
    evidence: dict[str, Any]


def _read_json(path: Path, fallback: Any, retries: int = 3, delay_seconds: float = 0.025) -> Any:
    if not path.exists():
        return fallback
    last_error: json.JSONDecodeError | None = None
    for attempt in range(retries + 1):
        try:
            text = path.read_text()
            if text.strip() == "":
                raise json.JSONDecodeError("empty registry file", text, 0)
            return json.loads(text)
        except json.JSONDecodeError as error:
            last_error = error
            if attempt >= retries:
                raise
            time.sleep(delay_seconds * (attempt + 1))
    if last_error is not None:
        raise last_error
    return fallback


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, indent=2, sort_keys=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    tmp.write_text(payload)
    tmp.replace(path)


def issue_to_dict(issue: GateIssue) -> dict[str, Any]:
    return asdict(issue)


def validate_candidate_record(record: dict[str, Any]) -> list[GateIssue]:
    return validate_candidate(record)


def load_candidates() -> list[dict[str, Any]]:
    return _read_json(CANDIDATES_PATH, [])


def load_experiments() -> list[dict[str, Any]]:
    return _read_json(EXPERIMENTS_PATH, [])


def load_experiment_results() -> list[dict[str, Any]]:
    return _read_json(EXPERIMENT_RESULTS_PATH, [])


def load_dequantization_checks() -> list[dict[str, Any]]:
    return _read_json(DEQUANTIZATION_CHECKS_PATH, [])


def load_proof_status() -> list[dict[str, Any]]:
    return _read_json(PROOF_STATUS_PATH, [])


def load_scaling_runs() -> list[dict[str, Any]]:
    return _read_json(SCALING_RUNS_PATH, [])


def load_conjectures() -> list[dict[str, Any]]:
    return _read_json(CONJECTURES_PATH, [])


def load_mutation_proposals() -> list[dict[str, Any]]:
    return _read_json(MUTATION_PROPOSALS_PATH, [])


def load_negative_results() -> list[dict[str, Any]]:
    return _read_json(NEGATIVE_RESULTS_PATH, [])


def load_rejected_candidates() -> list[dict[str, Any]]:
    return _read_json(REJECTED_CANDIDATES_PATH, [])


def load_reduction_ledger() -> dict[str, Any]:
    return _read_json(REDUCTIONS_PATH, {})


def save_reduction_ledger(payload: dict[str, Any]) -> None:
    _write_json(REDUCTIONS_PATH, payload)


def save_candidates(records: list[dict[str, Any]]) -> None:
    _write_json(CANDIDATES_PATH, records)


def save_experiments(records: list[dict[str, Any]]) -> None:
    _write_json(EXPERIMENTS_PATH, records)


def save_experiment_results(records: list[dict[str, Any]]) -> None:
    _write_json(EXPERIMENT_RESULTS_PATH, records)


def save_dequantization_checks(records: list[dict[str, Any]]) -> None:
    _write_json(DEQUANTIZATION_CHECKS_PATH, records)


def save_proof_status(records: list[dict[str, Any]]) -> None:
    _write_json(PROOF_STATUS_PATH, records)


def save_scaling_runs(records: list[dict[str, Any]]) -> None:
    _write_json(SCALING_RUNS_PATH, records)


def save_conjectures(records: list[dict[str, Any]]) -> None:
    _write_json(CONJECTURES_PATH, records)


def save_mutation_proposals(records: list[dict[str, Any]]) -> None:
    _write_json(MUTATION_PROPOSALS_PATH, records)


def save_negative_results(records: list[dict[str, Any]]) -> None:
    _write_json(NEGATIVE_RESULTS_PATH, records)


def save_rejected_candidates(records: list[dict[str, Any]]) -> None:
    _write_json(REJECTED_CANDIDATES_PATH, records)


def upsert_candidate(record: CandidateRecord) -> None:
    payload = asdict(record)
    issues = validate_candidate_record(payload)
    if issues:
        rendered = "; ".join(f"{issue.obligation_id}:{issue.field}:{issue.message}" for issue in issues)
        raise ValueError(f"Candidate rejected by proof gate: {rendered}")

    records = load_candidates()
    kept = [item for item in records if item.get("id") != record.id]
    kept.append(payload)
    kept.sort(key=lambda item: item["id"])
    save_candidates(kept)


def upsert_experiment(record: ExperimentRecord) -> None:
    records = load_experiments()
    kept = [item for item in records if item.get("id") != record.id]
    kept.append(asdict(record))
    kept.sort(key=lambda item: item["id"])
    save_experiments(kept)


def upsert_experiment_result(record: ExperimentResultRecord) -> None:
    records = load_experiment_results()
    kept = [item for item in records if item.get("id") != record.id]
    kept.append(asdict(record))
    kept.sort(key=lambda item: item["id"])
    save_experiment_results(kept)


def upsert_negative_result(record: NegativeResultRecord) -> None:
    records = load_negative_results()
    kept = [item for item in records if item.get("id") != record.id]
    kept.append(asdict(record))
    kept.sort(key=lambda item: item["id"])
    save_negative_results(kept)


def upsert_rejected_candidate(record: dict[str, Any]) -> None:
    records = load_rejected_candidates()
    kept = [item for item in records if item.get("id") != record.get("id")]
    kept.append(record)
    kept.sort(key=lambda item: item.get("id", ""))
    save_rejected_candidates(kept)


def upsert_scaling_run(record: dict[str, Any]) -> None:
    records = load_scaling_runs()
    kept = [item for item in records if item.get("id") != record.get("id")]
    kept.append(record)
    kept.sort(key=lambda item: item.get("id", ""))
    save_scaling_runs(kept)


def upsert_conjecture(record: dict[str, Any]) -> None:
    records = load_conjectures()
    kept = [item for item in records if item.get("id") != record.get("id")]
    kept.append(record)
    kept.sort(key=lambda item: item.get("id", ""))
    save_conjectures(kept)


def upsert_mutation_proposal(record: dict[str, Any]) -> None:
    records = load_mutation_proposals()
    kept = [item for item in records if item.get("id") != record.get("id")]
    kept.append(record)
    kept.sort(key=lambda item: item.get("id", ""))
    save_mutation_proposals(kept)


def seed_candidate_records() -> tuple[list[CandidateRecord], list[ExperimentRecord]]:
    now = utc_now()
    candidates = [
        CandidateRecord(
            id="DHS-GOWERS-SIEVE",
            title="State-sample-native generic DCP sieve and decoder",
            status="active",
            created_at=now,
            updated_at=now,
            literature_ids=[
                "kuperberg-dhsp-2003",
                "regev-lattice-dhsp-2003",
                "roetteler-hidden-shift-gowers-2009",
                "gowers-norm-algorithms-2025",
            ],
            ontology_node_ids=["hidden-shift", "dihedral-hsp", "unique-svp", "gowers-structure"],
            problem_family=(
                "The full family of dihedral coset-problem state instances over D_N emitted by the exact Regev "
                "unique-SVP reduction as N grows. Structured quadratic, character, trace, and Gowers phase families are "
                "adversarial testbeds only and do not define the claimed algorithmic scope."
            ),
            input_model=(
                "Independent coset-state samples from D_N under the exact f=1 DCP promise: each register is good with "
                "probability at least 1-1/log N and otherwise may be an arbitrary basis-state register. Good registers "
                "transform into known uniformly random labels k and phase states. No evaluator or chosen labels are available."
            ),
            classical_baseline=(
                "Generic dihedral hidden-reflection and subset-sum postprocessing baselines, plus all classical attacks legal "
                "for any public side information. Explicit phase-family learners are rejection tests for restricted testbeds, "
                "not evidence about the full DCP state-input problem."
            ),
            reduction_or_lower_bound=(
                "Use the exact THM-REGEV-USVP-TO-DCP-2003 contract. A speedup claim requires full-family coverage, a uniform "
                "lattice-dimension/modulus/sample/precision map, and bounded-error composition with the lattice decoder."
            ),
            quantum_mechanism=(
                "Combine independent labeled DCP phase states using uniform, state-only sum/difference measurements and "
                "postselection while tracking undetectable bad-register propagation. Search implicit merge rules over arbitrary "
                "D_N labels, never over a privileged phase evaluator."
            ),
            cost_model=(
                "Count every input coset state, zero-information label, 1/2 measurement branch, discarded state, live qubit, "
                "classical label operation, precision bit, merge depth, decoder stage, and lattice-reduction overhead."
            ),
            measurement_and_decoding=(
                "Measure known Fourier labels, perform auditable two-state or implicit multi-state collimation, recover each "
                "hidden-reflection congruence bit through a uniform recursive modulus reduction, and verify the full reflection "
                "before invoking the exact lattice decoder."
            ),
            success_statement=(
                "Target theorem: on every DCP state instance in the Regev contract, recover the complete hidden reflection with "
                "bounded error while proving an asymptotic sample, time, or memory improvement over a named Kuperberg/Regev "
                "baseline and preserving the end-to-end lattice approximation guarantee."
            ),
            complexity_accounting=(
                "Report asymptotic functions of log N and lattice dimension for coset-state copies, branch survival, time, "
                "space, precision, full decoding, and reduction overhead; empirical schedules never establish an exponent."
            ),
            no_go_analysis=(
                "Reject deterministic favorable-branch traces, evaluator-dependent rules, selected easy phase subfamilies, "
                "valuation-only endpoints, hidden nonuniform advice, and any schedule that merely reproduces generic sieve behavior."
            ),
            dequantization_check=(
                "Audit the exact state-access contract and all public classical side information; test structured subfamilies "
                "against correlation, sparse Fourier, derivative, algebraic, sample, and preprocessing attacks, and require "
                "state-native branch accounting before any quantum improvement claim."
            ),
            falsifiers=[
                "The rule queries a coherent evaluator, requests chosen labels, or uses family advice absent from DCP samples.",
                "An allowed 1/log N rate of arbitrary bad registers destroys decoder success or the claimed recurrence.",
                "Physical sum/difference postselection removes the apparent sample or memory advantage.",
                "The mechanism covers only quadratic, character, trace, Gowers, or another selected phase family.",
                "The endpoint reveals one parity bit without a complete uniform hidden-reflection decoder.",
                "The proved resource bound matches or loses to generic Kuperberg/Regev after reduction overhead.",
            ],
            experiment_ids=[
                "EXP-DHS-GOWERS-SPECTRUM",
                "EXP-DHS-FOURIER-COMPRESSIBILITY",
                "EXP-DHS-QUERY-LOWER-BOUND-PROBES",
                "EXP-DHS-CHARACTER-SHIFT-BASELINE",
                "EXP-DHS-CHARACTER-DECODER-SEARCH",
                "EXP-DHS-CHARACTER-QUERY-INFORMATION",
                "EXP-DHS-CHARACTER-LOWER-BOUND",
                "EXP-DHS-CHARACTER-MOMENT-OBSTRUCTION",
                "EXP-DHS-CHARACTER-COMPLEXITY-PREPROCESSING",
                "EXP-DHS-PHASE-NATURALNESS",
                "EXP-DHS-TRACE-FUNCTION-SEARCH",
                "EXP-DHS-PHASE-SIEVE",
                "EXP-DHS-DCP-SAMPLE-NATIVE-SIEVE",
                "EXP-DHS-DCP-RECURSIVE-DECODER",
                "EXP-DHS-DCP-RECURRENCE-SCALING",
                "EXP-DHS-DCP-SCHEDULE-SEARCH",
                "EXP-DHS-DCP-UNIFORM-SCHEDULE-FAMILY",
                "EXP-DHS-DCP-BAD-REGISTER-ROBUSTNESS",
                "EXP-DHS-DCP-CONTAMINATION-WITNESS",
                "EXP-DHS-DCP-COLLECTIVE-WITNESS-SEARCH",
                "EXP-DHS-DCP-CLIFFORD-WITNESS-SEARCH",
                "EXP-DHS-DCP-CLIFFORD-CONTAMINATION",
                "EXP-DHS-DCP-HADAMARD-SCALING",
                "EXP-DHS-DCP-RANDOM-DESIGN-DECODER",
                "EXP-DHS-DCP-DECODER-FRONTIER",
                "EXP-DHS-DCP-MULTISCALE-ALIASING",
                "EXP-DHS-DCP-CARRY-HIGH-PART-NOGO",
                "EXP-DHS-DCP-BOOLEAN-COSET-SEPARATION",
                "EXP-DHS-DCP-MARKER-AWARE-LIST-DECODER",
                "EXP-DHS-DCP-MARKER-DEVIATION-GEOMETRY",
                "EXP-DHS-DCP-MARKER-ALL-TARGET-COVERAGE",
            ],
            notes=(
                "Primary high-upside candidate. The authoritative algorithmic interface is independent DCP state input; "
                "all evaluator-based phase-family artifacts are negative-test infrastructure only."
            ),
        ),
        CandidateRecord(
            id="CODE-COSET-COLLECTIVE",
            title="Collective coset-state observables for code equivalence",
            status="active",
            created_at=now,
            updated_at=now,
            literature_ids=["hsp-survey-2010", "symmetric-defies-fourier-2005", "program-synthesis-components-2023"],
            ontology_node_ids=["nonabelian-hsp", "symmetric-hsp", "code-equivalence"],
            problem_family=(
                "Linear code equivalence families over increasing block length and finite fields, with controlled "
                "automorphism strata and hard classical canonicalization baselines."
            ),
            input_model=(
                "Efficient coherent preparation of hidden-permutation coset states derived from generator matrices; "
                "classical descriptions of code families are part of the input."
            ),
            classical_baseline=(
                "Best available code-equivalence canonicalization, information-set, support-splitting, and automorphism-group "
                "tools on the same generated families."
            ),
            reduction_or_lower_bound=(
                "Code equivalence embeds as a hidden permutation problem in the symmetric-group HSP frontier, but must "
                "explicitly bypass strong Fourier sampling no-go barriers."
            ),
            quantum_mechanism=(
                "Search for polynomial-description multi-register observables or tensor-network measurement ansatzes "
                "that distinguish coset states beyond individual strong Fourier labels."
            ),
            cost_model=(
                "Count coset-state preparation, number of registers, tensor bond dimension, measurement synthesis, "
                "classical preprocessing, and decoding cost."
            ),
            measurement_and_decoding=(
                "Use collective measurement candidates over several coset-state registers; decode candidate permutations "
                "or invariant separators and verify equivalence classically."
            ),
            success_statement=(
                "Conjecture: a restricted but hard code family admits a polynomial-bond collective observable whose "
                "distinguishing advantage remains inverse polynomial as length grows."
            ),
            complexity_accounting=(
                "Separate coset-state samples, quantum measurement size, tensor contraction complexity, and classical "
                "verification; compare against canonicalization and automorphism baselines."
            ),
            no_go_analysis=(
                "Strong Fourier sampling alone is ruled out for symmetric-group GI-style HSPs; this candidate survives "
                "only if it uses genuine collective measurements or leaves the blocked HSP route."
            ),
            dequantization_check=(
                "Check whether each separating observable is equivalent to classical color refinement, code invariants, "
                "support splitting, or canonicalization heuristics."
            ),
            falsifiers=[
                "Coset fingerprints remain nearly identical under all low-complexity relation tests.",
                "Tensor-network bond dimension grows exponentially before any signal appears.",
                "Classical code-equivalence tools solve every generated family.",
                "The observable collapses to a known classical invariant.",
            ],
            experiment_ids=[
                "EXP-CODE-COSET-RANK",
                "EXP-CODE-STRUCTURAL-INVARIANTS",
                "EXP-CODE-INFORMATION-SET-CANONICALIZATION",
                "EXP-CODE-CANONICALIZATION-BASELINE",
                "EXP-CODE-HARD-FAMILY-SEARCH",
                "EXP-CODE-PROFILE-COLLISION-SEARCH",
                "EXP-CODE-TUPLE-PROFILE-BASELINE",
                "EXP-CODE-LOW-WEIGHT-MATROID-BASELINE",
                "EXP-CODE-QUASI-CYCLIC-SEARCH",
                "EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION",
                "EXP-CODE-QC-INFORMATION-SET-RESOLVER",
                "EXP-CODE-CYCLIC-ALGEBRAIC-SEARCH",
                "EXP-CODE-BCH-ALGEBRAIC-SEARCH",
                "EXP-CODE-GOPPA-ALGEBRAIC-SEARCH",
                "EXP-CODE-GOPPA-SCALING-FRONTIER",
                "EXP-CODE-GOPPA-SYZYGY-FRONTIER",
                "EXP-CODE-GOPPA-HULL-PROJECTOR",
                "EXP-CODE-TANNER-LDPC-SEARCH",
                "EXP-CODE-REED-MULLER-PUNCTURE-SEARCH",
                "EXP-CODE-RANK-METRIC-SEARCH",
                "EXP-CODE-INCIDENCE-ISOMORPHISM-RESOLVER",
                "EXP-CODE-AFFINE-GEOMETRY-SEARCH",
                "EXP-CODE-PROJECTIVE-GEOMETRY-SEARCH",
                "EXP-CODE-SCHUR-FILTRATION",
                "EXP-CODE-CLOSURE-CONDUCTOR-ATTACK",
                "EXP-CODE-CFI-FAITHFUL-REDUCTION",
                "EXP-CODE-TRIVIAL-HULL-PROJECTOR-GI",
                "EXP-CODE-FRONTIER-TRIAGE",
                "EXP-COSET-COLLECTIVE-OBSERVABLE-SEARCH",
                "EXP-COSET-GM-SWITCHING-SEARCH",
                "EXP-COSET-CFI-BASE-FAMILY-SEARCH",
                "EXP-COSET-CFI-SCALING",
                "EXP-COSET-CFI-PARITY-SOLVER",
                "EXP-COSET-CFI-STRUCTURAL-DECODER",
                "EXP-COSET-CFI-IRREGULAR-STRUCTURAL-DECODER",
                "EXP-COSET-CFI-BIPARTITE-STRUCTURAL-DECODER",
                "EXP-COSET-INDIVIDUALIZED-WL",
                "EXP-COSET-INDIVIDUALIZED-TENSOR-OBSERVABLES",
                "EXP-COSET-FRONTIER-TRIAGE",
                "EXP-COSET-REPRESENTATION-OBSTRUCTIONS",
                "EXP-COSET-WEAK-FOURIER-SIGNAL",
                "EXP-COSET-STATE-DISTINGUISHABILITY",
                "EXP-COSET-PGM-CAPACITY",
                "EXP-COSET-HOLEVO-INFORMATION",
                "EXP-COSET-JUCYS-MURPHY-LABEL-TRANSFORM",
                "EXP-COSET-MULTIPLICITY-COMMUTANT-SEARCH",
                "EXP-CODE-TENSOR-MEASUREMENT",
            ],
            notes="High upside but high no-go risk; registry keeps the no-go analysis mandatory.",
        ),
    ]
    experiments = [
        ExperimentRecord(
            id="EXP-DHS-GOWERS-SPECTRUM",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Derivative Fourier and Gowers spectrum sweep",
            status="planned",
            hypothesis="Useful hidden-shift families show derivative Fourier sparsity without becoming classically learnable.",
            protocol=(
                "Generate algebraic phase families across increasing group sizes; compute Gowers U^k, derivative Fourier "
                "support, autocorrelation aliases, and classical sparse-learning attacks."
            ),
            positive_signal="Derivative support grows polynomially while classical attacks fail on the same access model.",
            falsifiers=[
                "Autocorrelation identifies the shift directly.",
                "Sparse derivatives imply a simple classical learner.",
                "No family has stable structure beyond small n.",
            ],
            metrics=["gowers_u2_u3", "derivative_support_99", "autocorrelation_peak_ratio", "classical_attack_success"],
            dependencies=["structural_tests.py", "finite group family generator"],
            next_actions=["Implement finite-field phase-family generator.", "Add classical sparse-learning baseline."],
        ),
        ExperimentRecord(
            id="EXP-DHS-PHASE-SIEVE",
            candidate_id="DHS-GOWERS-SIEVE",
            title="DCP state-sample-native phase-state sieve",
            status="planned",
            hypothesis=(
                "A valid sieve improvement acts directly on independent DCP phase states and survives exact branch, sample, "
                "memory, and decoder accounting."
            ),
            protocol=(
                "Run dcp_sample_workbench.py on the full uniform D_N label distribution with no evaluator access; "
                "charge sum/difference outcomes and every discarded state."
            ),
            positive_signal=(
                "A uniform full-family rule proves a better asymptotic resource bound than a named Kuperberg/Regev baseline "
                "and includes a complete reflection decoder."
            ),
            falsifiers=[
                "The merge rule requires evaluator or chosen-label access.",
                "Physical postselection removes the apparent sample advantage.",
                "The endpoint reveals only parity rather than the full hidden reflection.",
                "The schedule has no proved asymptotic improvement.",
            ],
            metrics=[
                "coset_state_query_count",
                "evaluator_query_count",
                "postselection_optimism_gap",
                "memory_peak_states",
                "full_hidden_reflection_decode_count",
            ],
            dependencies=["dcp_sample_workbench.py", "THM-REGEV-USVP-TO-DCP-2003"],
            next_actions=["Synthesize state-only merge rules.", "Prove a complete recursive decoder."],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SAMPLE-NATIVE-SIEVE",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Theorem-contract-faithful DCP state-sample sieve audit",
            status="planned",
            hypothesis=(
                "A valid DHSP improvement must operate on independent DCP coset/phase-state samples, charge the physical "
                "sum/difference branch, and include a uniform full-reflection decoder."
            ),
            protocol=(
                "Generate uniform Fourier labels from the full D_N state-input promise; run generic signed-label merge rules; "
                "charge every coset-state sample, branch measurement, discarded outcome, memory peak, and decoder stage."
            ),
            positive_signal=(
                "A uniform state-only rule proves an asymptotic sample/time/memory improvement over a named generic baseline "
                "and composes with a complete hidden-reflection and lattice decoder."
            ),
            falsifiers=[
                "The rule requires coherent evaluator or chosen-label access absent from the DCP theorem contract.",
                "Deterministic favorable-branch accounting understates sample complexity.",
                "A target valuation yields only parity rather than a complete hidden-reflection decoder.",
                "Empirical schedules do not prove an asymptotic improvement over Kuperberg/Regev.",
            ],
            metrics=[
                "coset_state_query_count",
                "evaluator_query_count",
                "postselection_optimism_gap",
                "sample_exponent_log2",
                "memory_peak_states",
                "parity_endpoint_trial_count",
                "full_hidden_reflection_decode_count",
            ],
            dependencies=[
                "dcp_sample_workbench.py",
                "THM-REGEV-USVP-TO-DCP-2003 exact theorem contract",
            ],
            next_actions=[
                "Search implicit merge rules over full D_N labels without evaluator access.",
                "Formalize recursive bit recovery and compose it with the lattice parameter map.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-RECURSIVE-DECODER",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Fresh-batch recursive DCP reflection decoder audit",
            status="planned",
            hypothesis=(
                "Parity endpoints can be composed into full reflection recovery using only fresh independent DCP states, "
                "known-label phase corrections, and recursive modulus reduction."
            ),
            protocol=(
                "Recover low bits one at a time from N/2 phase endpoints. After each bit, correct a fresh batch by the "
                "known recovered residue, reinterpret labels modulo the reduced modulus, and rerun the state-native sieve. "
                "Exhaustively verify the accumulated phase identity and charge every fresh coset state."
            ),
            positive_signal=(
                "A theorem gives a uniform endpoint-success lower bound, bounded end-to-end failure, and an asymptotic "
                "sample/time/space recurrence that improves a named Kuperberg/Regev baseline."
            ),
            falsifiers=[
                "Any decoder stage requires evaluator, chosen-label, or hidden-reflection access.",
                "The accumulated phase-correction identity fails for a label, reflection, or recursion depth.",
                "Fresh-batch endpoint generation fails with non-negligible probability under the proposed schedule.",
                "The complete recurrence merely reproduces or loses to generic Kuperberg/Regev asymptotics.",
                "Finite successful trials are promoted without a uniform failure bound.",
            ],
            metrics=[
                "empirical_full_recovery_rate",
                "total_coset_state_samples",
                "evaluator_query_count",
                "fresh_batch_violation_count",
                "phase_correction_failure_count",
                "proved_full_failure_bound_count",
            ],
            dependencies=[
                "dcp_recursive_decoder.py",
                "dcp_sample_workbench.py",
                "THM-REGEV-USVP-TO-DCP-2003 exact theorem contract",
            ],
            next_actions=[
                "Prove a uniform per-stage endpoint probability for the physical merge process.",
                "Derive and compare the end-to-end sample/time/space recurrence.",
                "Compose the bounded-error decoder with the exact lattice parameter map.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-RECURRENCE-SCALING",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Exact pair-kernel and finite DCP recurrence scaling audit",
            status="planned",
            hypothesis=(
                "A state-only label-pairing rule may exhibit a uniform endpoint-yield recurrence whose optimized resource "
                "frontier improves a named generic DHSP sieve."
            ),
            protocol=(
                "Exhaustively verify one-pair sum/difference kernels; compare randomized, maximum-nonzero, opposite-residue, "
                "and target-complement pairing; sweep sqrt(log N)-scaled sample budgets; exclude endpoints already present "
                "in raw inputs; report Wilson intervals and descriptive sqrt(n)/linear-n fits."
            ),
            positive_signal=(
                "A symbolic adaptive multi-round recurrence proves a uniform endpoint lower bound, bounded recursive failure, "
                "and improved sample, time, or memory asymptotics over a named Kuperberg/Regev baseline."
            ),
            falsifiers=[
                "A pairing rule relies on evaluator, chosen-label, or hidden-reflection information.",
                "The analytic pair kernel fails exhaustive small-modulus verification.",
                "Apparent endpoint success comes from target labels already present in raw samples.",
                "Finite threshold fits are promoted without controlling adaptive bucket dependence.",
                "The optimized recurrence matches or loses to generic Kuperberg/Regev resources.",
            ],
            metrics=[
                "pair_kernel_failure_count",
                "total_charged_coset_states",
                "direct_target_input_count",
                "sieve_generated_target_count",
                "target_capable_pair_count",
                "exact_conditional_expected_target_count",
                "no_target_opportunity_trial_count",
                "generated_endpoint_success_row_count",
                "proved_uniform_endpoint_lower_bound_count",
                "proved_asymptotic_improvement_count",
            ],
            dependencies=[
                "dcp_recurrence_analysis.py",
                "dcp_sample_workbench.py",
                "dcp_recursive_decoder.py",
                "THM-REGEV-USVP-TO-DCP-2003 exact theorem contract",
            ],
            next_actions=[
                "Replace finite fits with a stochastic bucket-occupancy recurrence and concentration proof.",
                "Optimize per-stage budgets under a total failure constraint.",
                "Compare the resulting sample/time/space constants and exponents with named generic baselines.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SCHEDULE-SEARCH",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Train/holdout DCP bucket-schedule synthesis",
            status="planned",
            hypothesis=(
                "A nonstandard state-only bucket schedule may generate target-capable pairs more reliably than the default "
                "block schedule without increasing the asymptotic resource frontier."
            ),
            protocol=(
                "Mutate increasing bucket-bit schedules; score only generated endpoints and exact target opportunities on "
                "training seeds; select once; compare the selected schedule with the default schedule on disjoint holdout seeds."
            ),
            positive_signal=(
                "A schedule generalizes across held-out seeds and growing n, then admits a uniform recurrence proof with a "
                "strict sample/time/memory improvement over a named Kuperberg/Regev schedule."
            ),
            falsifiers=[
                "The selected schedule fails to improve held-out endpoint success.",
                "Training success materially exceeds holdout success.",
                "The schedule exploits direct target labels or an exponential birthday regime.",
                "The gain disappears after sample, memory, branch, and recursive failure accounting.",
                "No symbolic uniform recurrence supports the selected finite schedule family.",
            ],
            metrics=[
                "unique_schedule_count",
                "evaluated_schedule_count",
                "optimizer_trial_count",
                "holdout_trial_count",
                "heldout_seed_improvement_count",
                "statistically_confirmed_improvement_count",
                "birthday_regime_record_count",
                "max_holdout_success_improvement",
                "max_selection_optimism_gap",
                "proved_uniform_recurrence_count",
                "proved_asymptotic_improvement_count",
            ],
            dependencies=[
                "dcp_schedule_search.py",
                "dcp_recurrence_analysis.py",
                "dcp_sample_workbench.py",
            ],
            next_actions=[
                "Extract symbolic schedule families from any held-out survivor.",
                "Rerun survivors across larger n and multiple sample-resource frontiers.",
                "Prove or reject the induced adaptive bucket-occupancy recurrence.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-UNIFORM-SCHEDULE-FAMILY",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Uniform sqrt(log N) block-schedule family on unseen moduli",
            status="planned",
            hypothesis=(
                "Per-modulus schedule gains may compress into one block formula that improves finite endpoint yield on "
                "unseen modulus sizes."
            ),
            protocol=(
                "Search b_j=min(n-1,j ceil(c sqrt(n))) over one constant c on training sizes; freeze c; compare with "
                "c=1 on larger unseen sizes using independent seeds and sub-birthday sample budgets."
            ),
            positive_signal=(
                "A uniform schedule family generalizes, then a symbolic recurrence proves a new asymptotic sample/time/memory class."
            ),
            falsifiers=[
                "The selected constant regresses on unseen sizes.",
                "The gain changes only the constant inside a known 2^O(sqrt(log N)) bound.",
                "The gain disappears after recursive failure or memory accounting.",
                "No uniform bucket-occupancy recurrence can be proved.",
            ],
            metrics=[
                "block_scale_candidate_count",
                "training_trial_count",
                "unseen_trial_count",
                "positive_mean_unseen_improvement_count",
                "asymptotic_class_change_count",
                "max_mean_unseen_success_improvement",
            ],
            dependencies=["dcp_uniform_schedule_family.py", "dcp_schedule_search.py", "dcp_recurrence_analysis.py"],
            next_actions=[
                "Derive exact occupancy recurrences for any unseen-size survivor.",
                "Reject constant-only gains as baseline strengthening rather than candidate algorithms.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-BAD-REGISTER-ROBUSTNESS",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Exact f=1 DCP bad-register contamination audit",
            status="planned",
            hypothesis="A state-native sieve and recursive decoder can tolerate arbitrary bad basis-state registers at rate 1/log N.",
            protocol=(
                "Inject hidden bad registers at the exact f=1 theorem rate, propagate validity through legal merges, allow "
                "adversarial bad-bad branch choices, and measure corrupted endpoints and parity-bit error."
            ),
            positive_signal="A uniform adversarial robustness theorem gives bounded endpoint and full-decoder error under the exact DCP promise.",
            falsifiers=[
                "Corrupted endpoints are indistinguishable from valid endpoints by public labels.",
                "The recursive all-bits-valid probability vanishes at the theorem bad rate.",
                "Robustness requires more than polynomial overhead or unavailable verification access.",
            ],
            metrics=[
                "theorem_corrupted_endpoint_row_count",
                "maximum_theorem_false_bit_probability",
                "minimum_theorem_all_bits_valid_probability",
                "proved_bad_register_robustness_count",
            ],
            dependencies=["dcp_bad_register_audit.py", "THM-REGEV-USVP-TO-DCP-2003 primary LaTeX theorem"],
            next_actions=[
                "Design state-native bad-register detection or error-tolerant endpoint decoding.",
                "Prove a contamination threshold across all recursive stages or block the lattice route.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-CONTAMINATION-WITNESS",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Exact state-only DCP contamination-witness boundary",
            status="planned",
            hypothesis=(
                "A shallow collective measurement can exploit common-reflection correlations to tolerate Regev f=1 bad "
                "registers without evaluator access or simulator-only validity flags."
            ),
            protocol=(
                "Average exact public-label phase-state ensembles over the unknown reflection, compare them with allowed "
                "randomized basis-state contamination, enumerate modular subset-sum blocks, compute trace distances, and "
                "charge the computation required to realize each witness."
            ),
            positive_signal=(
                "A uniform polynomial-description measurement has inverse-polynomial distinguishing bias, logarithmic "
                "dependency depth, and a proved adversarial threshold that composes with full reflection decoding."
            ),
            falsifiers=[
                "The good and bad ensembles are identical for the proposed label batches.",
                "Distinguishability exists only after exponential subset-sum enumeration.",
                "The witness uses hidden bad flags, reflection verification, or evaluator access.",
                "The dependency cone makes the all-good component superpolynomially small.",
            ],
            metrics=[
                "collision_free_exact_indistinguishability_count",
                "information_signal_instance_count",
                "maximum_trace_distance",
                "minimum_linear_register_all_good_probability",
                "polynomial_time_witness_count",
                "proved_robust_decoder_count",
            ],
            dependencies=[
                "dcp_contamination_witness.py",
                "dcp_bad_register_audit.py",
                "THM-REGEV-USVP-TO-DCP-2003 primary LaTeX theorem",
            ],
            next_actions=[
                "Search polynomial-description collective observables on subset-sum collision spaces.",
                "Prove false-positive and false-negative bounds under arbitrary allowed basis-state contamination.",
                "Compose any witness with a shallow full-reflection decoder and exact lattice reduction contract.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-COLLECTIVE-WITNESS-SEARCH",
            candidate_id="DHS-GOWERS-SIEVE",
            title="State-native DCP collective witness language search",
            status="planned",
            hypothesis=(
                "A polynomial-description collective observable can expose common-reflection coherence and reject f=1 "
                "basis-state contamination without solving an exponential subset-sum instance."
            ),
            protocol=(
                "Start with bounded-support X/Y Pauli correlators, enumerate their signed modular label relations, derive "
                "union bounds for polynomial label pools, and reject observable classes whose aggregate signal probability "
                "is negligible before extending the measurement language."
            ),
            positive_signal=(
                "An implicit polynomial-time observable family has inverse-polynomial signal on random public labels, "
                "survives arbitrary bad basis states, and composes with full reflection decoding."
            ),
            falsifiers=[
                "Nonzero signal requires a signed relation whose probability is negligible for the observable locality.",
                "Relations can be found only by exponential enumeration or postselection.",
                "The measurement uses hidden validity flags, evaluator access, or the unknown reflection.",
                "The observable distinguishes good batches but does not yield a robust full decoder.",
            ],
            metrics=[
                "finite_relation_trial_count",
                "finite_relation_count",
                "logarithmic_locality_negligible_count",
                "minimum_first_unruled_relation_weight",
                "polynomial_time_robust_witness_count",
                "proved_full_decoder_count",
            ],
            dependencies=[
                "dcp_collective_witness_search.py",
                "dcp_contamination_witness.py",
                "dcp_bad_register_audit.py",
            ],
            next_actions=[
                "Extend beyond bounded Pauli support to implicit global measurements only when execution cost is explicit.",
                "Search algebraic transforms of modular subset-sum collision blocks with polynomial circuit descriptions.",
                "Prove adversarial error and full-decoder composition for every surviving observable family.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-CLIFFORD-WITNESS-SEARCH",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Global public-label Clifford witness search",
            status="planned",
            hypothesis=(
                "A public-label-derived quadratic-phase Clifford circuit exposes common-reflection correlations with an "
                "efficiently decodable inverse-polynomial bias while mapping arbitrary basis-state batches to uniform outputs."
            ),
            protocol=(
                "Exactly construct hidden-reflection-averaged subset-sum collision blocks, evaluate polynomial-description "
                "CZ-plus-Hadamard circuit families, compare unrestricted output total variation with polynomial-time "
                "Hamming-weight decoding, and sweep growing register counts."
            ),
            positive_signal=(
                "One uniform circuit/decoder schema has a proved inverse-polynomial Hamming-statistic bias under arbitrary "
                "f=1 contamination and composes with a full reflection decoder."
            ),
            falsifiers=[
                "Only an exponentially described accepting set sees the total-variation signal.",
                "Efficient Hamming-weight bias decays exponentially or lacks a uniform lower bound.",
                "Partial arbitrary contamination defeats the statistic.",
                "The measurement distinguishes batches but does not recover the hidden reflection.",
            ],
            metrics=[
                "schema_evaluation_count",
                "inverse_polynomial_hamming_signal_count",
                "maximum_full_tv",
                "maximum_hamming_tv",
                "finite_log2_hamming_tv_slope_per_n",
                "proved_inverse_polynomial_signal_family_count",
                "proved_adversarial_threshold_count",
                "proved_full_decoder_count",
            ],
            dependencies=[
                "dcp_clifford_witness_search.py",
                "dcp_contamination_witness.py",
                "dcp_collective_witness_search.py",
            ],
            next_actions=[
                "Derive analytic output-statistic moments for every finite signal schema.",
                "Test partial arbitrary dephasing and adversarial basis patterns without hidden validity flags.",
                "Reject schemas whose decoding statistic has exponential sample complexity.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-CLIFFORD-CONTAMINATION",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Adversarial one-bad-register Clifford witness audit",
            status="planned",
            hypothesis=(
                "A global public-label Clifford statistic retains inverse-polynomial common-reflection signal for every "
                "location and basis value of an arbitrary bad DCP register."
            ),
            protocol=(
                "For every generated label batch and Clifford schema, replace each coordinate in turn by |0> and |1>, "
                "compute the exact hidden-reflection-averaged output distribution, and minimize polynomial Hamming-weight "
                "distinguishability over all hidden one-bad cases."
            ),
            positive_signal=(
                "One uniform schema has a proved inverse-polynomial worst-case signal, extends to the full f=1 bad-count "
                "distribution, and composes with full reflection decoding."
            ),
            falsifiers=[
                "One coordinate/basis choice erases the efficient statistic.",
                "Worst-case signal decays exponentially with n.",
                "The schema survives one bad register but fails at allowed larger bad counts.",
                "The statistic does not yield a hidden-reflection decoder.",
            ],
            metrics=[
                "adversarial_one_bad_case_count",
                "inverse_polynomial_one_bad_signal_count",
                "zero_worst_case_signal_count",
                "maximum_robust_one_bad_hamming_tv",
                "finite_log2_robust_tv_slope_per_n",
                "proved_uniform_one_bad_signal_family_count",
                "proved_full_f1_threshold_count",
                "proved_full_decoder_count",
            ],
            dependencies=[
                "dcp_clifford_contamination.py",
                "dcp_clifford_witness_search.py",
                "dcp_bad_register_audit.py",
            ],
            next_actions=[
                "Kill schemas with exponential worst-case signal decay.",
                "Extend survivors to t-bad and probabilistic f=1 contamination without hidden flags.",
                "Require a full reflection decoder before reduction composition.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-HADAMARD-SCALING",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Hadamard witness register-ratio phase transition",
            status="planned",
            hypothesis=(
                "The loss of efficient Hadamard signal at m=log N may reverse above a critical polynomial-state ratio, "
                "while an analytic second-moment bound kills the entire subcritical regime."
            ),
            protocol=(
                "Sweep m/log2(N), compute exact Hamming output distributions for every hidden reflection and random public "
                "label batch, compare prior-mixture and worst-reflection statistics, and attach the signed-relation "
                "chi-square upper bound for m/log2(N)<1/log2(3/2)."
            ),
            positive_signal=(
                "A supercritical ratio has a proved worst-reflection inverse-polynomial statistic, polynomial sample cost, "
                "f=1 bad-register robustness, and a full hidden-reflection decoder."
            ),
            falsifiers=[
                "The ratio lies below the analytic average-case threshold.",
                "Supercritical Hamming signal is only a prior average and vanishes for some reflections.",
                "State or repetition costs become superpolynomial.",
                "Arbitrary bad registers erase the signal or no full decoder exists.",
            ],
            metrics=[
                "analytic_subcritical_ratio_threshold",
                "analytically_subcritical_row_count",
                "supercritical_row_count",
                "supercritical_inverse_polynomial_signal_row_count",
                "maximum_supercritical_mean_hamming_tv",
                "proved_worst_case_reflection_signal_family_count",
                "proved_f1_robust_decoder_count",
            ],
            dependencies=[
                "dcp_hadamard_scaling.py",
                "dcp_clifford_witness_search.py",
                "dcp_clifford_contamination.py",
            ],
            next_actions=[
                "Concentrate measurement search above the analytic register-ratio threshold.",
                "Derive worst-reflection rather than prior-mixture signal bounds for supercritical ratios.",
                "Extend any survivor to the exact f=1 promise and hidden-reflection decoding.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-RANDOM-DESIGN-DECODER",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Random-label local-quadrature frequency decoder baseline",
            status="planned",
            hypothesis=(
                "Random X/Y measurements of DCP phase states contain enough information to identify the hidden frequency "
                "with O(log N) samples, but locating its Fourier peak may still require exponential classical time."
            ),
            protocol=(
                "Measure each random-label phase qubit in X or Y, encode the outcome as an unbiased complex phase estimate, "
                "run a length-N FFT, compare with polynomial random candidate testing, and account for sample, time, memory, "
                "and access legality separately."
            ),
            positive_signal=(
                "A state-sample-native decoder locates the planted random-design frequency in poly(log N) time and memory, "
                "tolerates f=1 bad registers, and recovers the complete reflection."
            ),
            falsifiers=[
                "Recovery requires a length-N FFT, exhaustive frequency scoring, or Theta(N) memory.",
                "A proposed sparse Fourier method assumes chosen labels or repeated-label queries.",
                "Polynomially many candidate probes do not locate the hidden frequency.",
                "Bad-register robustness or full reflection recovery is absent.",
            ],
            metrics=[
                "local_quantum_measurement_count",
                "fft_success_count",
                "high_success_fft_row_count",
                "polynomial_random_candidate_success_count",
                "maximum_fft_time_proxy",
                "maximum_fft_memory_proxy",
                "proved_polynomial_time_decoder_count",
            ],
            dependencies=[
                "dcp_random_design_decoder.py",
                "dcp_hadamard_scaling.py",
                "query_model_ledger.py",
            ],
            next_actions=[
                "Audit sparse Fourier and heavy-frequency algorithms against random-label rather than chosen-query access.",
                "Search structured hashing or multiscale decoders that avoid materializing N frequencies.",
                "Apply adversarial bad-register corruption before promoting any decoder.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-DECODER-FRONTIER",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Named DCP decoder resource frontier",
            status="planned",
            hypothesis=(
                "A useful DCP direction must improve a named legal resource frontier rather than merely moving cost "
                "between samples, time, memory, measurement, and classical decoding."
            ),
            protocol=(
                "Compare local-quadrature FFT, Grover likelihood search, Kuperberg and Regev generic sieves, chosen-label "
                "phase estimation, global Clifford statistics, and the polynomial target under the same n=log2(N) contract."
            ),
            positive_signal=(
                "A legal exact-f=1 method has a complete decoder and strictly improves a named sample/time/memory class."
            ),
            falsifiers=[
                "The method uses chosen labels or a coherent likelihood oracle absent from DCP.",
                "Polynomial samples hide exponential time or memory.",
                "The method is asymptotically dominated by a generic DCP sieve.",
                "Bad-register robustness or full lattice composition is missing.",
            ],
            metrics=[
                "legal_row_count",
                "illegal_access_row_count",
                "exponential_time_row_count",
                "generic_subexponential_baseline_count",
                "proved_polynomial_exact_f1_decoder_count",
                "complete_lattice_composition_count",
            ],
            dependencies=[
                "dcp_decoder_frontier.py",
                "dcp_random_design_decoder.py",
                "dcp_bad_register_audit.py",
                "reduction_theorem_catalog.py",
            ],
            next_actions=[
                "Reject every new decoder that does not improve a named legal frontier row.",
                "Attach exact f=1 and lattice-composition columns before promotion.",
                "Prioritize the missing polynomial random-label decoder rather than dominated FFT/Grover variants.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-MULTISCALE-ALIASING",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Random-label multiscale aliasing access no-go",
            status="planned",
            hypothesis=(
                "A polynomial random-label decoder might recover reflection bits by waiting for raw labels or pair "
                "differences with enough 2-adic valuation to expose small effective moduli."
            ),
            protocol=(
                "For b=Theta(log n) effective modulus bits and polynomial label budgets, compute exact raw-label and "
                "pair-difference hit probabilities, union bounds, and expected-one sample thresholds across growing n."
            ),
            positive_signal=(
                "A legal multiscale construction reaches useful aliases with polynomial states and composes them into a "
                "poly(n)-time robust full decoder without chosen labels."
            ),
            falsifiers=[
                "Raw useful labels require 2^(n-b) samples.",
                "Pair differences require birthday scale 2^((n-b)/2).",
                "The method requests chosen/repeated high-valuation labels.",
                "Only deeper subexponential collimation remains.",
            ],
            metrics=[
                "raw_polynomial_access_ruled_out_count",
                "pair_polynomial_access_ruled_out_count",
                "tail_raw_polynomial_access_ruled_out_count",
                "tail_pair_polynomial_access_ruled_out_count",
                "minimum_tail_log2_raw_samples",
                "minimum_tail_log2_pair_samples",
                "proved_general_random_label_decoder_lower_bound_count",
            ],
            dependencies=[
                "dcp_multiscale_aliasing_audit.py",
                "dcp_random_design_decoder.py",
                "query_model_ledger.py",
            ],
            next_actions=[
                "Exclude raw and pair-only aliasing from decoder mutation grammars.",
                "Search deeper implicit collimation or algebraic frequency localization.",
                "Do not generalize this restricted no-go into a full DCP lower bound.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-RANDOM-FOURIER-BRIDGE",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Random-label DCP to noisy-Fourier/hidden-number bridge",
            status="planned",
            hypothesis=(
                "Random-basis measurements of DCP phase states admit a rigorous polynomial-sample character-learning "
                "description, while efficient localization remains blocked by random rather than chosen labels."
            ),
            protocol=(
                "Derive the exact measurement moment, prove an exhaustive correlation sample bound under the f=1 "
                "basis-state contamination contract, classify SFT/HNP/LPN/LWE bridge edges, and reject every transfer "
                "that changes access, observation channel, or resource accounting."
            ),
            positive_signal=(
                "An advantage-preserving random-example reduction yields a poly(log N)-time frequency localizer or a "
                "standard hard problem under the exact DCP access and contamination model."
            ),
            falsifiers=[
                "The decoder enumerates all N frequencies or materializes an N-sized table.",
                "The imported SFT/HNP algorithm uses chosen, correlated, repeated, or interval-conditioned multipliers.",
                "The LPN/LWE connection is only an analogy with no explicit reduction.",
                "Sample-level contamination attenuation does not survive the efficient decoding transform.",
            ],
            metrics=[
                "bridge_edge_count",
                "proved_one_way_edge_count",
                "access_invalid_transfer_count",
                "polynomial_sample_certificate_count",
                "proved_exact_f1_sample_robustness_count",
                "proved_polynomial_time_decoder_count",
                "proved_hnp_reduction_count",
                "proved_lpn_lwe_reduction_count",
            ],
            dependencies=[
                "dcp_hidden_number_bridge.py",
                "dcp_random_design_decoder.py",
                "paper_ingestion.py",
                "query_model_ledger.py",
            ],
            next_actions=[
                "Search random-example frequency-localization algorithms that never request chosen labels.",
                "Attempt and aggressively audit a channel reduction to random-multiplier hidden-number observations.",
                "Lift any efficient decoder through the exact f=1 and Regev lattice contracts.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SPARSE-FOURIER-TRANSFER-AUDIT",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Sparse-Fourier structured-query transfer audit",
            status="planned",
            hypothesis=(
                "Polylogarithmic sparse-Fourier localization mechanisms either adapt to iid random-label DCP records "
                "without hidden query power or expose a precise access primitive that must be replaced."
            ),
            protocol=(
                "Classify significant-Fourier, HashToBins, compressed-sensing, periodogram, and signed-label-closure "
                "mechanisms by joint sample schedule, time, and memory; union-bound constant-arity synthesis of prescribed "
                "offsets; retain fundamentally new iid estimators as an open contract."
            ),
            positive_signal=(
                "A uniform iid random-example hash estimator localizes the hidden cyclic character in poly(log N) time "
                "and memory and remains valid under exact f=1 contamination."
            ),
            falsifiers=[
                "The sparse-FFT routine evaluates chosen shifted, filtered, repeated, or correlated sample locations.",
                "The adaptation materializes N candidate frequencies or invokes a poly(N) generic solver.",
                "Constant-arity closure has exponentially small prescribed-offset coverage.",
                "A restricted template failure is overstated as a general decoder lower bound.",
            ],
            metrics=[
                "mechanism_count",
                "direct_access_invalid_count",
                "closure_certificate_count",
                "tail_inverse_polynomial_coverage_ruled_out_count",
                "proved_polylog_random_example_decoder_count",
                "proved_general_random_example_lower_bound_count",
            ],
            dependencies=[
                "dcp_sparse_fourier_transfer_audit.py",
                "dcp_hidden_number_bridge.py",
                "paper_ingestion.py",
                "research/literature_cache/1604.00845_source",
            ],
            next_actions=[
                "Design unbiased iid estimators for sparse-FFT hash bins and prove their variance.",
                "Search beyond constant-arity label closure without hiding superpolynomial combination counts.",
                "Apply every survivor to worst-frequency and exact f=1 decoding before lattice composition.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-IID-LINEAR-HASH-ESTIMATOR",
            candidate_id="DHS-GOWERS-SIEVE",
            title="IID linear hash-bin Parseval tradeoff",
            status="planned",
            hypothesis=(
                "A coarse frequency bucket can be estimated from iid DCP quadrature records by a low-variance linear "
                "statistic without enumerating exponentially many buckets."
            ),
            protocol=(
                "Derive the normalized Parseval identity for every exact unbiased linear bucket estimator, calculate "
                "sample lower bounds across coarse and fine bucket schedules, verify finite transforms numerically, and "
                "separate the resulting restricted theorem from nonlinear and collective decoder classes."
            ),
            positive_signal=(
                "A linear or provably biased low-variance bucket statistic has both polynomial iid sample cost and "
                "polynomial bucket-enumeration cost with an inverse-polynomial decision margin."
            ),
            falsifiers=[
                "Parseval weight energy is N/B for a bucket of size N/B.",
                "Coarse polynomial bucket counts require exponential iid samples.",
                "Fine sample-efficient buckets leave exponentially many bucket candidates.",
                "The argument is overstated beyond exact unbiased one-pass linear estimators.",
            ],
            metrics=[
                "certificate_count",
                "finite_parseval_failure_count",
                "polynomial_bucket_rows_with_exponential_sample_lower_bound",
                "polynomial_sample_rows_with_exponential_bucket_count",
                "joint_polynomial_resource_row_count",
                "proved_exact_linear_estimator_no_go_count",
                "proved_nonlinear_decoder_lower_bound_count",
            ],
            dependencies=[
                "dcp_iid_hash_estimator_audit.py",
                "dcp_sparse_fourier_transfer_audit.py",
                "dcp_hidden_number_bridge.py",
            ],
            next_actions=[
                "Search biased linear estimators with explicit margin and second-moment bounds.",
                "Search nonlinear multi-record sketches that do not materialize N candidates.",
                "Do not generalize the linear no-go to collective measurements or generic DCP decoding.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-IID-BIASED-LINEAR-MARGIN",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Biased linear iid margin-energy tradeoff",
            status="planned",
            hypothesis=(
                "Replacing exact bucket indicators by biased or smooth expected scores can yield a uniformly separated "
                "coarse-frequency test with polynomial iid samples and polynomially many bucket tests."
            ),
            protocol=(
                "Minimize Fourier-response energy over every one-pass linear score whose expectation separates a target "
                "bucket from its complement by a common margin; derive the worst-instance empirical-mean MSE sample "
                "bound, verify the optimizer with finite FFTs, and preserve all nonlinear and adaptive decoder classes."
            ),
            positive_signal=(
                "A linear score with an inverse-polynomial uniform margin has both polynomial sample cost and polynomial "
                "bucket enumeration, or a rigorously analyzed decision rule escapes the MSE certificate."
            ),
            falsifiers=[
                "The minimum-energy response is the two-level function separated by twice the margin.",
                "Parseval forces energy 4 gamma^2 S(N-S)/N.",
                "Uniform MSE below the squared margin retains an exponential coarse-bucket sample bound.",
                "A one-score MSE theorem is overstated as a lower bound for adaptive or nonlinear classifiers.",
            ],
            metrics=[
                "certificate_count",
                "finite_check_failure_count",
                "polynomial_bucket_rows_with_super_budget_samples",
                "polynomial_sample_rows_with_exponential_bucket_count",
                "joint_polynomial_resource_row_count",
                "proved_uniform_margin_linear_no_go_count",
                "proved_arbitrary_linear_classifier_lower_bound_count",
                "proved_nonlinear_decoder_lower_bound_count",
            ],
            dependencies=[
                "dcp_biased_linear_margin_audit.py",
                "dcp_iid_hash_estimator_audit.py",
                "dcp_hidden_number_bridge.py",
            ],
            next_actions=[
                "Analyze multiple adaptive linear statistics rather than mutating a single bucket response.",
                "Build a degree-indexed hierarchy of nonlinear U-statistics over iid records.",
                "Do not generalize the result beyond the explicit uniform-margin and MSE contract.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-IID-MULTIRECORD-HIERARCHY",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Degree-indexed iid multirecord estimator hierarchy",
            status="planned",
            hypothesis=(
                "Products or other fixed-degree multilinear functions of iid DCP quadrature records create coarse "
                "frequency information unavailable to one-record linear scores without exponential sample cost."
            ),
            protocol=(
                "For each degree and signed-label pattern, condition the kernel on its aggregate label, apply Jensen and "
                "Parseval, derive disjoint-block margin/MSE sample bounds, exhaustively verify finite aggregate-label "
                "uniformity, and classify overlapping U-statistic, adaptive, growing-degree, and collective exceptions."
            ),
            positive_signal=(
                "An overlapping or implicitly contracted multirecord estimator has polynomial evaluation, a uniform "
                "worst-reflection margin, polynomial samples, and exact f=1 robustness without materializing N scores."
            ),
            falsifiers=[
                "Every fixed signed aggregate of independent uniform labels remains uniform.",
                "Conditional Jensen reduces a disjoint multilinear kernel to the same response Parseval problem.",
                "The product outcome introduces a 4^r block second moment.",
                "A disjoint-block theorem is overstated as a lower bound on overlapping U-statistics or collective measurements.",
            ],
            metrics=[
                "certificate_count",
                "degree_count",
                "finite_check_failure_count",
                "joint_polynomial_resource_row_count",
                "higher_degree_rows_cheaper_than_degree_one_count",
                "proved_disjoint_block_multilinear_no_go_count",
                "proved_overlapping_ustatistic_lower_bound_count",
                "proved_adaptive_multistatistic_lower_bound_count",
                "proved_collective_measurement_lower_bound_count",
            ],
            dependencies=[
                "dcp_multirecord_estimator_hierarchy.py",
                "dcp_biased_linear_margin_audit.py",
                "dcp_hidden_number_bridge.py",
            ],
            next_actions=[
                "Derive Hoeffding projections for overlapping kernels and search for genuinely degenerate responses.",
                "Audit adaptive multistatistic decision trees with shared samples.",
                "Search polynomial-description premeasurement collective observables outside the classical kernel theorem.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-IID-USTATISTIC-VARIANCE",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Overlapping U-statistic Hoeffding variance audit",
            status="planned",
            hypothesis=(
                "Averaging a signed-product kernel over all overlapping record tuples uses dependence or Hoeffding "
                "degeneracy to evade the disjoint-block DCP margin-energy bound with polynomial resources."
            ),
            protocol=(
                "Apply the exact Hoeffding variance decomposition to symmetric order-r kernels, combine its minimum "
                "coefficient with the DCP Jensen/Parseval worst-instance kernel variance, solve the required binomial "
                "tuple and record counts, and separate explicit enumeration from implicit contraction."
            ),
            positive_signal=(
                "A polynomial-time implicit contraction evaluates a growing-degree statistic with uniform margin, "
                "polynomial records, bounded precision, and no N-sized intermediate spectrum."
            ),
            falsifiers=[
                "Var(U_m) is at least Var(h)/C(m,r) for every Hoeffding projection profile.",
                "Fixed degree requires exponentially many records for coarse polynomial bucket counts.",
                "Growing degree reduces records only while explicit tuple evaluation remains exponential.",
                "An explicit-tuple theorem is overstated as a lower bound on implicit contractions or collective measurements.",
            ],
            metrics=[
                "certificate_count",
                "degree_count",
                "coefficient_check_failure_count",
                "polynomial_bucket_rows_with_super_budget_records",
                "polynomial_bucket_rows_with_super_budget_explicit_tuples",
                "polynomial_record_but_exponential_tuple_row_count",
                "joint_polynomial_explicit_resource_row_count",
                "proved_overlapping_ustatistic_variance_bound_count",
                "proved_implicit_contraction_lower_bound_count",
                "proved_collective_measurement_lower_bound_count",
            ],
            dependencies=[
                "dcp_ustatistic_variance_audit.py",
                "dcp_multirecord_estimator_hierarchy.py",
                "dcp_biased_linear_margin_audit.py",
            ],
            next_actions=[
                "Search factorizable growing-degree kernels with polynomial elementary-symmetric or tensor contractions.",
                "Reject every contraction that materializes N Fourier bins or requires exponential precision.",
                "Move premeasurement entangled observables to a separate circuit-size theorem contract.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-IID-FACTORIZED-CONTRACTION",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Rank-one implicit U-statistic contraction audit",
            status="planned",
            hypothesis=(
                "An elementary-symmetric contraction computes a growing-degree rank-one DCP product U-statistic in "
                "polynomial time and thereby evades explicit tuple enumeration with polynomial samples."
            ),
            protocol=(
                "Represent the kernel response as H=F^r, derive the exact first Hoeffding projection, combine the margin "
                "large-response class with Parseval base energy, verify finite exact variance formulas, and sweep degree, "
                "bucket count, and n while keeping polynomial-rank and low-bond contractions separate."
            ),
            positive_signal=(
                "A polynomial-rank or low-bond contraction cancels lower Hoeffding projections while retaining a uniform "
                "bucket margin, polynomial norm, precision, records, and intermediate dimension."
            ),
            falsifiers=[
                "Rank-one response factorization H=F^r forces a complete class with |F|^r at least the margin.",
                "Parseval base energy makes the first projection require Omega(r^2 N/B) records.",
                "Elementary-symmetric O(mr) arithmetic remains exponential because m is exponential.",
                "A rank-one theorem is overstated as a lower bound on polynomial-rank or tensor-network contractions.",
            ],
            metrics=[
                "certificate_count",
                "degree_count",
                "finite_variance_check_failure_count",
                "polynomial_bucket_rows_with_super_budget_samples",
                "joint_polynomial_resource_row_count",
                "proved_rank_one_implicit_contraction_no_go_count",
                "proved_polynomial_rank_contraction_lower_bound_count",
                "proved_tensor_train_contraction_lower_bound_count",
                "proved_collective_measurement_lower_bound_count",
            ],
            dependencies=[
                "dcp_factorized_contraction_audit.py",
                "dcp_ustatistic_variance_audit.py",
                "dcp_hidden_number_bridge.py",
            ],
            next_actions=[
                "Search polynomial-rank sums with explicit projection-cancellation and coefficient-norm accounting.",
                "Search low-bond tensor-train kernels and audit every intermediate Fourier dimension.",
                "Reject any apparent gain that requires exponential coefficient precision or hidden N-sized state.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-IID-LOW-RANK-CONTRACTION",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Polynomial-rank implicit contraction search",
            status="planned",
            hypothesis=(
                "A polynomial-rank sum of contractible product kernels cancels low-order Hoeffding projections while "
                "retaining a uniform coarse-frequency margin and polynomial total resources."
            ),
            protocol=(
                "Generate closed-form cosine, Fejer, and hybrid response dictionaries; optimize worst-point bucket margin "
                "under an L1 coefficient budget; compute exact all-order cross-component Hoeffding covariance; solve the "
                "minimum record count; and charge rank, precision, bucket enumeration, and contraction operations."
            ),
            positive_signal=(
                "A scaling family retains inverse-polynomial worst-point margin, polynomial exact variance sample count, "
                "rank, precision, and contraction work without an N-entry runtime intermediate."
            ),
            falsifiers=[
                "The response dictionary cannot separate adjacent target and non-target frequencies uniformly.",
                "Exact cross-component Hoeffding variance requires superpolynomial records.",
                "Projection cancellation requires superpolynomial coefficient precision or tensor rank.",
                "Finite separation lacks a uniform asymptotic theorem, f=1 robustness, or lattice composition.",
            ],
            metrics=[
                "row_count",
                "uniform_separation_row_count",
                "superpolynomial_sample_row_count",
                "superpolynomial_precision_row_count",
                "superpolynomial_contraction_row_count",
                "joint_polynomial_finite_survivor_count",
                "proved_uniform_low_rank_family_count",
                "proved_exact_f1_robust_low_rank_decoder_count",
                "proved_lattice_composition_count",
            ],
            dependencies=[
                "dcp_low_rank_contraction_search.py",
                "dcp_factorized_contraction_audit.py",
                "scipy.optimize.linprog",
            ],
            next_actions=[
                "If a finite row survives, fit larger n and prove uniform margin and projection bounds symbolically.",
                "Mutate the response dictionary only when a new cancellation mechanism is specified.",
                "Move any asymptotic survivor through exact f=1 robustness and the Regev lattice contract.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-MEASUREMENT-AUDIT",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Collective subset-sum measurement and tensor-bond audit",
            status="planned",
            hypothesis=(
                "A polynomial circuit can compute the public-label subset sum, Fourier transform or compress its residue "
                "register, and expose hidden-reflection phase interference without solving coherent subset-sum fibers."
            ),
            protocol=(
                "Prove the output law of sum measurement and sum-register QFT with retained input garbage; enumerate "
                "finite prefix residue ranks; certify high-probability exact residue bond dimensions; and separate exact "
                "MPS, approximate hashing, coherent fiber erasure, quantum walks, and compressed PGM architectures."
            ),
            positive_signal=(
                "A polynomial-bond approximate residue network or compressed fiber measurement retains inverse-polynomial "
                "worst-reflection signal, tolerates arbitrary f=1 bad states, and has a polynomial decoder."
            ),
            falsifiers=[
                "Measuring the computed subset sum is independent of the hidden reflection.",
                "QFT on the sum register is exactly uniform while orthogonal input garbage remains.",
                "Exact residue tracking has exponentially many reachable prefix residues with high probability.",
                "An exact residue-automaton theorem is overstated against approximate hashing or compressed PGMs.",
            ],
            metrics=[
                "finite_instance_count",
                "qft_uniformity_failure_count",
                "compute_qft_signal_instance_count",
                "bond_certificate_count",
                "high_probability_exponential_bond_certificate_count",
                "proved_zero_information_architecture_count",
                "proved_polynomial_collective_measurement_count",
                "proved_exact_f1_robust_decoder_count",
                "proved_lattice_composition_count",
            ],
            dependencies=[
                "dcp_subset_sum_measurement_audit.py",
                "dcp_contamination_witness.py",
                "dcp_collective_witness_search.py",
            ],
            next_actions=[
                "Search hashed residue networks with a proved phase-signal/error tradeoff.",
                "Formalize coherent equal-sum fiber symmetrization as a circuit primitive and attack its complexity.",
                "Test any survivor under adversarial basis-state contamination before lattice composition.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-HASHED-FIBER-MEASUREMENT-AUDIT",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Hashed collision-fiber erasure audit",
            status="planned",
            hypothesis=(
                "Hashing exact subset sums to polynomially many residues and postselecting the input onto the uniform "
                "state yields polynomial-success coherent phase interference for every hidden reflection."
            ),
            protocol=(
                "Compute exact subset-sum multiplicities, evaluate every hidden-reflection postselection probability for "
                "modulo and affine hashes, prove the hidden-average collision identity, derive high-probability random-label "
                "worst-d bounds, and charge amplitude amplification while preserving nonuniform projections and walks."
            ),
            positive_signal=(
                "A public nonuniform fiber reference, collision walk, or compressed PGM has inverse-polynomial uniform "
                "overlap and retained d signal with polynomial circuit size and exact f=1 robustness."
            ),
            falsifiers=[
                "False hash collisions cancel when success is averaged over d.",
                "Uniform Hadamard fiber erasure succeeds only at the exact subset-sum collision probability on average.",
                "Worst-d postselection remains exponentially small with high probability for m=Theta(n).",
                "The uniform projection theorem is overstated against nonuniform references or collision walks.",
            ],
            metrics=[
                "finite_instance_count",
                "mean_identity_failure_count",
                "polynomial_hash_instance_count",
                "polynomial_uniform_postselection_instance_count",
                "asymptotic_certificate_count",
                "high_probability_polynomial_uniform_success_ruled_out_count",
                "proved_polynomial_fiber_symmetrization_count",
                "proved_exact_f1_robust_decoder_count",
                "proved_lattice_composition_count",
            ],
            dependencies=[
                "dcp_hashed_fiber_measurement_audit.py",
                "dcp_subset_sum_measurement_audit.py",
                "dcp_contamination_witness.py",
            ],
            next_actions=[
                "Search public nonuniform tensor reference states with provable uniform overlap.",
                "Search coherent collision walks that avoid global fiber postselection.",
                "Apply exact f=1 contamination before promoting any conditional signal.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-REFERENCE-PROJECTION-AUDIT",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Public low-trace DCP reference-projection theorem",
            status="planned",
            hypothesis=(
                "A public label-dependent rank-one or polynomial-rank reference subspace can erase subset identity "
                "with inverse-polynomial uniform success while preserving hidden-reflection phase information."
            ),
            protocol=(
                "Derive the exact hidden-average success of an arbitrary public postselection effect after any subset-sum "
                "hash, upper-bound it by Tr(E)c_max/2^m, verify the rank-one identity and tightness numerically, and use "
                "random-label collision moments to certify high-probability polynomial-trace bounds."
            ),
            positive_signal=(
                "A full-rank many-outcome measurement, compressed PGM, or adaptive collision walk implements a complete "
                "polynomial decoder without reducing to a low-trace postselection event."
            ),
            falsifiers=[
                "Every rank-one public reference has hidden-average success at most c_max/2^m.",
                "Polynomial rank or polynomial trace only multiplies the maximum-fiber bound polynomially.",
                "Random m=Theta(n) labels make the maximum-fiber fraction exponentially small with high probability.",
                "The low-trace theorem is overstated against full-rank many-outcome or adaptive collective measurements.",
            ],
            metrics=[
                "finite_instance_count",
                "random_reference_identity_failure_count",
                "random_reference_bound_violation_count",
                "tight_rank_one_bound_failure_count",
                "asymptotic_certificate_count",
                "below_polynomial_threshold_certificate_count",
                "proved_arbitrary_rank_one_projection_no_go_count",
                "proved_polynomial_rank_projection_no_go_count",
                "proved_low_trace_effect_no_go_count",
                "proved_full_rank_collective_measurement_no_go_count",
            ],
            dependencies=[
                "dcp_reference_projection_audit.py",
                "dcp_hashed_fiber_measurement_audit.py",
                "dcp_subset_sum_measurement_audit.py",
            ],
            next_actions=[
                "Formalize full-rank covariant/PGM effects without postselection.",
                "Search compressed implementations of the DCP Gram operator and collision walks.",
                "Require a complete exact-f=1 decoder and lattice parameter composition for every survivor.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-COVARIANT-PGM-AUDIT",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Clean covariant DCP PGM information/implementation audit",
            status="planned",
            hypothesis=(
                "The exact full-rank covariant PGM has useful clean-state success with m=Theta(n), and its normalized "
                "subset-sum fiber measurement admits a uniform polynomial implementation."
            ),
            protocol=(
                "Compute exact subset-sum multiplicities, Gram eigenvalues, and covariant-PGM success across scaling "
                "sweeps; compare to occupancy benchmarks; then audit explicit matrices, normalized-fiber isometries, "
                "residue DPs, low-trace references, Gram block encodings, and collision walks separately."
            ),
            positive_signal=(
                "A poly(n)-gate full-rank implementation decodes every clean hidden reflection with inverse-polynomial "
                "success, survives exact f=1 contamination, and composes with the lattice reduction."
            ),
            falsifiers=[
                "Clean PGM information success is mistaken for efficient implementation.",
                "The implementation materializes N outcomes, multiplicities, advice, or QRAM entries.",
                "The proposed fiber erasure reduces to exact residue DP or polynomial-trace postselection.",
                "The clean measurement fails exact f=1 robustness or complete lattice composition.",
            ],
            metrics=[
                "finite_instance_count",
                "inverse_polynomial_information_success_count",
                "constant_information_success_count",
                "mean_n_register_pgm_success",
                "minimum_n_register_pgm_success",
                "proved_clean_information_theorem_count",
                "proved_polynomial_pgm_circuit_count",
                "proved_polynomial_fiber_erasure_count",
                "proved_exact_f1_robust_pgm_count",
                "proved_lattice_composition_count",
            ],
            dependencies=[
                "dcp_covariant_pgm_audit.py",
                "dcp_reference_projection_audit.py",
                "dcp_subset_sum_measurement_audit.py",
            ],
            next_actions=[
                "Formalize normalized subset-sum fiber indexing as the implementation target.",
                "Search block encodings and collision walks without N-sized classical advice.",
                "Derive the exact contaminated ensemble and robust covariant measurement obligations.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-CONTAMINATED-PGM-AUDIT",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Exact f=1 contaminated covariant-PGM information audit",
            status="planned",
            hypothesis=(
                "The exact f=1 bad-register rate destroys the information advantage of the clean global covariant PGM "
                "on a linear-size register block."
            ),
            protocol=(
                "Apply the fixed clean PGM to the primary-source tensor-product contamination model, prove the all-good "
                "branch lower bound uniformly over arbitrary basis-state bad values, verify it numerically for adversarial "
                "patterns, and keep implementation complexity separate."
            ),
            positive_signal=(
                "A uniform polynomial implementation of the full-rank clean PGM retains inverse-polynomial success under "
                "the exact f=1 product contamination promise and composes with the lattice reduction."
            ),
            falsifiers=[
                "The all-good component has constant weight for m=Theta(log N).",
                "Arbitrary bad basis values cannot subtract from POVM success on the all-good component.",
                "The argument silently assumes independent/tensor-product registers absent from the source contract.",
                "Information robustness is promoted without a polynomial measurement circuit.",
            ],
            metrics=[
                "finite_instance_count",
                "lower_bound_violation_count",
                "inverse_polynomial_robust_information_instance_count",
                "minimum_n_register_all_good_probability",
                "minimum_n_register_adversarial_lower_bound",
                "proved_exact_f1_information_robustness_count",
                "proved_exact_f1_robust_pgm_circuit_count",
                "proved_lattice_composition_count",
            ],
            dependencies=[
                "dcp_contaminated_pgm_audit.py",
                "dcp_covariant_pgm_audit.py",
                "THM-REGEV-USVP-TO-DCP-2003 primary LaTeX definition",
            ],
            next_actions=[
                "Stop treating f=1 as the global PGM information barrier.",
                "Construct the normalized-fiber measurement with a uniform polynomial circuit.",
                "Compose robust measurement success with complete reflection and lattice recovery.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-AVERAGE-SUBSET-SUM-BRIDGE",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Regev average-case modular subset-sum bridge",
            status="planned",
            hypothesis=(
                "A deterministic polynomial-time solver for an inverse-polynomial fraction of legal random modular "
                "subset-sum instances at density one can be constructed and inserted into Regev's matching routine."
            ),
            protocol=(
                "Formalize the primary-source conditional reduction, audit low-weight/contiguous/random candidate "
                "baselines and an exact exponential control, prove explicit polynomial-enumeration coverage bounds, and "
                "separate deterministic, randomized, quantum, and full-fiber solver interfaces."
            ),
            positive_signal=(
                "A uniform deterministic poly(log N)-time partial solver achieves inverse-polynomial legal-input coverage, "
                "or a randomized/quantum solver is given a new coherent reduction with the same end-to-end consequence."
            ),
            falsifiers=[
                "The solver only enumerates polynomially many explicit candidate subsets.",
                "Finite coverage is promoted without a uniform inverse-polynomial theorem.",
                "The method is meet-in-the-middle or otherwise exponential in log N.",
                "A randomized/quantum witness generator is inserted into a theorem that assumes deterministic consistency.",
            ],
            metrics=[
                "finite_baseline_count",
                "polynomial_baseline_count",
                "polynomial_inverse_coverage_row_count",
                "source_contract_satisfying_row_count",
                "polynomial_enumeration_ruled_out_count",
                "primary_source_conditional_dcp_reduction_count",
                "proved_polynomial_partial_average_subset_sum_solver_count",
                "proved_randomized_or_quantum_solver_bridge_count",
                "proved_polynomial_dcp_decoder_count",
            ],
            dependencies=[
                "dcp_subset_sum_bridge.py",
                "regev-lattice-dhsp-2003 primary LaTeX lines 700-1065",
                "THM-REGEV-USVP-TO-DCP-2003",
            ],
            next_actions=[
                "Search structural partial average-case subset-sum solvers near density one.",
                "Formalize coherent reductions for randomized or quantum witness generators.",
                "Use partial-solver coverage rather than requiring a stronger all-fiber PGM primitive.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-LATTICE-SEARCH",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Density-one modular subset-sum LLL partial-solver search",
            status="planned",
            hypothesis=(
                "A deterministic polynomial-time modular subset-sum lattice embedding has inverse-polynomial random legal-input "
                "coverage near density one and can instantiate Regev's partial-solver assumption."
            ),
            protocol=(
                "Sweep exact integer LLL embeddings over density offsets, embedding scales, reduction strengths, and fixed-arity "
                "reduced-basis combinations; sample uniform random targets, verify every witness, measure exact legal coverage "
                "where feasible, and require a uniform coverage and reversibility theorem."
            ),
            positive_signal=(
                "A uniform embedding family retains inverse-polynomial random-input success through growing n, has a proved "
                "coverage lower bound and polynomial exact bit complexity, and admits reversible deterministic implementation."
            ),
            falsifiers=[
                "High small-n success collapses in the scaling tail.",
                "Tuning embedding constants changes finite recovery but supplies no uniform coverage theorem.",
                "Growing reduced-basis combination arity hides superpolynomial enumeration.",
                "The solver is polynomial classically but has no uniform reversible implementation for the matching routine.",
            ],
            metrics=[
                "row_count",
                "trial_count",
                "successful_trial_count",
                "invalid_witness_count",
                "finite_success_row_count",
                "tail_success_row_count",
                "maximum_tested_n_bits",
                "source_contract_satisfying_row_count",
                "proved_uniform_inverse_polynomial_coverage_count",
                "proved_reversible_uniform_implementation_count",
                "proved_polynomial_dcp_decoder_count",
            ],
            dependencies=[
                "dcp_subset_sum_lattice_search.py",
                "dcp_subset_sum_bridge.py",
                "sympy exact integer LLL",
            ],
            next_actions=[
                "Search embeddings whose short-vector geometry changes the tail rather than retuning constants.",
                "Attempt average-case coverage analysis for any tail survivor.",
                "Build a reversible resource contract before inserting a solver into Regev's matching routine.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-TWO-ADIC-SEARCH",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Density-one modular subset-sum 2-adic lifting audit",
            status="planned",
            hypothesis=(
                "For modulus 2^n, the sequence of carry constraints defining a density-one subset-sum witness has a "
                "uniform compact algebraic representation that supports a polynomial partial solver."
            ),
            protocol=(
                "Enumerate exact small-instance fibers through moduli 2,4,...,2^n; measure affine-hull dimension, "
                "affine overcoverage, and minimum restricted-domain ANF degree of each lift predicate; distinguish "
                "nonvacuous fits from interpolation on shrinking fibers; require a separate uniform solver theorem."
            ),
            positive_signal=(
                "A uniform compact lift representation yields a polynomial-time witness algorithm with inverse-polynomial "
                "coverage on random legal inputs and a deterministic reversible or rigorously coherent interface."
            ),
            falsifiers=[
                "The representation is extracted only by 2^(n+O(1)) exact enumeration.",
                "Late low-degree fits use at least as many features as domain points.",
                "Affine hulls exponentially overcover the exact subset-sum fiber.",
                "A bounded-degree equation system is presented without a polynomial solving algorithm.",
                "Finite structure is promoted without legal-input coverage or reversibility proofs.",
            ],
            metrics=[
                "trial_count",
                "legal_target_trial_count",
                "lift_row_count",
                "affine_exact_lift_count",
                "degree_censored_lift_count",
                "nonvacuous_bounded_degree_lift_count",
                "all_lifts_affine_trial_count",
                "mean_final_affine_hull_overcoverage_log2",
                "maximum_exact_enumeration_log2_cost",
                "proved_uniform_polynomial_two_adic_solver_count",
                "proved_uniform_inverse_polynomial_coverage_count",
                "source_contract_satisfying_row_count",
            ],
            dependencies=[
                "dcp_subset_sum_two_adic_search.py",
                "dcp_subset_sum_bridge.py",
                "power-of-two DCP modulus contract",
            ],
            next_actions=[
                "Derive symbolic carry recurrences rather than fitting enumerated truth tables.",
                "Search exact compact representations closed under every 2-adic lift.",
                "Prove or falsify polynomial solvability for any bounded-degree structured system found.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-RESOURCE-FRONTIER",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Source-linked density-one subset-sum resource frontier",
            status="planned",
            hypothesis=(
                "A known meet-in-the-middle, dissection, generalized-birthday, representation, or quantum subset-sum "
                "method can satisfy the polynomial partial-solver interface required by Regev's DCP reduction."
            ),
            protocol=(
                "Record exact versus heuristic assumptions and time/memory exponents for named classical and quantum "
                "algorithms; audit balanced Wagner leaf-list thresholds at density one; compare every route with the "
                "deterministic polynomial legal-coverage and reversible-interface contract."
            ),
            positive_signal=(
                "A source-supported route drives its asymptotic time exponent to zero, retains inverse-polynomial legal "
                "coverage, and provides the deterministic or coherently composable interface required by the reduction."
            ),
            falsifiers=[
                "The method merely lowers a positive exponential time or memory exponent.",
                "A random-list or representation heuristic is presented as an exact theorem.",
                "A deeper Wagner tree lacks sufficient density-one leaf-list volume without uncharged representations.",
                "A randomized or quantum algorithm is inserted into a deterministic matching theorem without a new proof.",
                "A class-specific barrier is overstated as a lower bound on unknown structural solvers.",
            ],
            metrics=[
                "known_algorithm_count",
                "known_polynomial_time_algorithm_count",
                "known_regev_contract_satisfying_algorithm_count",
                "best_recorded_classical_time_exponent",
                "best_recorded_quantum_time_exponent",
                "wagner_certificate_count",
                "deep_basic_wagner_threshold_failure_count",
                "representation_expansion_required_count",
                "polynomial_resource_route_count",
                "source_contract_satisfying_row_count",
            ],
            dependencies=[
                "dcp_subset_sum_resource_frontier.py",
                "dcp_subset_sum_bridge.py",
                "primary literature for HS, Schroeppel-Shamir, dissection, BCJ, BetterSample, and quantum representation algorithms",
            ],
            next_actions=[
                "Require every solver mutation to declare its exponent, memory, assumptions, and source-interface status.",
                "Search structures that invalidate random-list genericity rather than optimizing a positive exponent.",
                "Formalize a coherent bridge before treating randomized or quantum partial solvers as relevant to DCP.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-CARRY-ANF",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Full-domain subset-sum carry ANF audit",
            status="planned",
            hypothesis=(
                "The power-of-two subset-sum carry constraints have a uniformly bounded-degree sparse algebraic normal "
                "form that supports polynomial witness recovery on random density-one inputs."
            ),
            protocol=(
                "Compute every carry-bit truth table on the full Boolean cube, apply the exact Mobius transform, measure "
                "ANF degree and monomial growth by bit and n, and separate full-domain structure from restricted-fiber interpolation."
            ),
            positive_signal=(
                "A symbolic construction proves uniformly bounded representation size and supplies a polynomial equation "
                "solver with inverse-polynomial legal coverage and a reversible matching interface."
            ),
            falsifiers=[
                "Only the parity bit is affine while later carry degree grows with n.",
                "The ANF is obtained by exponential truth-table enumeration.",
                "A finite sparse polynomial is promoted without a uniform symbolic construction.",
                "A compact equation system is supplied without a polynomial witness solver.",
                "High ANF degree is overstated as a lower bound against non-algebraic algorithms.",
            ],
            metrics=[
                "trial_count",
                "carry_row_count",
                "bounded_degree_row_count",
                "tail_bounded_degree_row_count",
                "all_carries_bounded_degree_trial_count",
                "maximum_observed_anf_degree",
                "maximum_observed_monomial_count",
                "fitted_final_bit_degree_slope_per_n",
                "proved_uniform_bounded_degree_carry_family_count",
                "proved_polynomial_algebraic_witness_solver_count",
                "source_contract_satisfying_row_count",
            ],
            dependencies=[
                "dcp_subset_sum_carry_anf.py",
                "dcp_subset_sum_two_adic_search.py",
                "dcp_subset_sum_bridge.py",
            ],
            next_actions=[
                "Derive any anomalous low-degree carry family symbolically and test uniform random-label prevalence.",
                "Search polynomial solvers for structured systems only after representation size survives scaling.",
                "Keep lattice, representation, and non-algebraic partial-solver routes separate from this rejection class.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-SOLVER-SYNTHESIS",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Typed density-one partial subset-sum solver synthesis",
            status="planned",
            hypothesis=(
                "Combining mathematically distinct lattice, 2-adic, representation, coherent-walk, and decoding-reduction "
                "primitives can generate a route that escapes every current negative result and eventually meets the source contract."
            ),
            protocol=(
                "Build typed solver primitives from live artifacts; generate hybrid hypotheses; attach complexity, legal "
                "coverage, witness, deterministic/coherent interface, and reversibility obligations; reject exact matches "
                "to LLL-retuning, bounded-carry, basic-Wagner, and positive-exponent negative results."
            ),
            positive_signal=(
                "A proposal graduates only after theorem artifacts prove polynomial resources, inverse-polynomial legal "
                "coverage, verified witnesses, and a source-compatible reversible interface."
            ),
            falsifiers=[
                "The mutation only retunes a tested algorithm or lowers a positive exponential exponent.",
                "The mechanism contradicts live full-domain carry or Wagner-list evidence.",
                "The proposal changes the legal input distribution or hides nonuniform advice.",
                "A randomized/quantum solver lacks a coherent matching theorem.",
                "A research proposal is inserted into the accepted candidate registry before its theorems exist.",
            ],
            metrics=[
                "primitive_count",
                "hypothesis_count",
                "proposal_only_survivor_count",
                "negative_match_rejection_count",
                "accepted_candidate_count",
                "source_contract_satisfying_hypothesis_count",
                "maximum_survivor_priority_score",
            ],
            dependencies=[
                "dcp_subset_sum_solver_synthesis.py",
                "dcp_subset_sum_bridge.py",
                "dcp_subset_sum_lattice_search.py",
                "dcp_subset_sum_two_adic_search.py",
                "dcp_subset_sum_resource_frontier.py",
                "dcp_subset_sum_carry_anf.py",
            ],
            next_actions=[
                "Execute the highest-priority hybrid's first falsification experiments.",
                "Feed new negative results back into the grammar before generating another batch.",
                "Keep all survivors proposal-only until the proof gate can validate actual algorithmic claims.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-LOW-BIT-BDD",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Polynomial low-bit subset-sum BDD and state-preparation audit",
            status="planned",
            hypothesis=(
                "An exact compact representation of O(log n) low congruence constraints can be constructed uniformly and "
                "used as a preconditioner without being mistaken for a full density-one witness solver."
            ),
            protocol=(
                "Build running-residue decision diagrams for b=ceil(c log2 n), compute exact completion counts, prove width "
                "and reversible conditional state-preparation bounds, measure fiber entropy, and leave high-bit geometry as "
                "a separately gated obligation."
            ),
            positive_signal=(
                "Polynomial BDD/state-preparation certificates hold uniformly, and a subsequent preconditioned solver proves "
                "changed high-bit geometry, inverse-polynomial legal coverage, and a reversible source-compatible witness map."
            ),
            falsifiers=[
                "The low-bit representation exceeds O(n 2^b) states or needs exponential count precision.",
                "O(log n)-bit conditioning is promoted despite leaving linear residual entropy.",
                "Taking b=Theta(n) silently restores exponential width.",
                "Conditional state preparation is presented as measurement or witness recovery.",
                "No average-case short-vector or decoding improvement follows from preconditioning.",
            ],
            metrics=[
                "row_count",
                "theorem_certificate_count",
                "polynomial_width_certificate_count",
                "polynomial_state_preparation_certificate_count",
                "linear_residual_entropy_certificate_count",
                "mean_acceptance_log2_ratio_to_uniform",
                "proved_high_bit_geometry_improvement_count",
                "proved_polynomial_witness_solver_count",
                "source_contract_satisfying_row_count",
            ],
            dependencies=[
                "dcp_subset_sum_low_bit_bdd.py",
                "dcp_subset_sum_solver_synthesis.py",
                "dcp_subset_sum_bridge.py",
            ],
            next_actions=[
                "Use the exact low-bit BDD as input to a preregistered quotient-lattice geometry experiment.",
                "Prove whether conditioned quotient labels remain sufficiently random for average-case analysis.",
                "Reject any mutation that merely increases b until the BDD is exponential.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-CONDITIONED-QUOTIENT",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Conditioned high-bit quotient concentration audit",
            status="planned",
            hypothesis=(
                "Conditioning a random density-one subset-sum instance on O(log n) exact low bits may alter the remaining "
                "quotient distribution enough to support a polynomial implicit decoder or a useful lattice preconditioner."
            ),
            protocol=(
                "Compute exact small-n quotient multiplicities after low-bit conditioning, measure support, Shannon and "
                "collision entropy, target mass, and top-polynomial-list mass, while forbidding finite entropy from being "
                "reported as a lower bound."
            ),
            positive_signal=(
                "A uniform theorem shows non-generic quotient geometry or inverse-polynomial concentration, together with "
                "a polynomial implicit decoder and Regev-compatible legal-input coverage."
            ),
            falsifiers=[
                "The conditioned quotient retains broad support and near-maximal entropy in scaling tails.",
                "Any concentration appears only for an explicit polynomial candidate list or planted-target sampling.",
                "No asymptotic quotient-distribution theorem or changed lattice geometry is supplied.",
                "The decoder requires full multiplicity tables, exponential advice, or b=Theta(n) conditioning.",
            ],
            metrics=[
                "row_count",
                "minimum_tail_normalized_shannon_entropy",
                "minimum_tail_collision_effective_support_fraction",
                "maximum_tail_exact_target_probability",
                "maximum_tail_top_polynomial_candidate_mass",
                "proved_uniform_high_entropy_quotient_count",
                "proved_polynomial_high_bit_decoder_count",
                "proved_high_bit_geometry_improvement_count",
                "source_contract_satisfying_row_count",
            ],
            dependencies=[
                "dcp_subset_sum_conditioned_quotient.py",
                "dcp_subset_sum_low_bit_bdd.py",
                "dcp_subset_sum_bridge.py",
            ],
            next_actions=[
                "Derive an asymptotic quotient-distribution theorem for random legal labels.",
                "Preregister a quotient-lattice or representation statistic before extending finite sweeps.",
                "Reject explicit-list concentration as a substitute for an implicit polynomial decoder.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-CARRY-SLICE-LATTICE",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Carry-sliced quotient lattice partial-solver audit",
            status="planned",
            hypothesis=(
                "Enumerating the O(n) exact low-bit carry slices and adding the corresponding exact low-sum equation "
                "changes modular LLL geometry enough to produce inverse-polynomial random legal-instance coverage."
            ),
            protocol=(
                "For each random instance, compute every reachable carry by exact polynomial low-sum DP, run a lattice "
                "embedding with both the high modular equation and exact low-sum equation, and compare against unsliced "
                "LLL on identical instances and extraction parameters."
            ),
            positive_signal=(
                "A uniform average-case short-vector theorem proves inverse-polynomial legal coverage and a deterministic "
                "reversible polynomial implementation, with paired tail gains over unsliced LLL."
            ),
            falsifiers=[
                "Paired tail recovery matches or loses to unsliced LLL.",
                "Improvement is confined to finite sizes or tuned scales.",
                "The method skips carries using nonuniform advice or grows extraction arity.",
                "No inverse-polynomial legal-coverage theorem or reversible implementation is supplied.",
            ],
            metrics=[
                "trial_count",
                "baseline_success_count",
                "carry_sliced_success_count",
                "carry_sliced_only_success_count",
                "baseline_only_success_count",
                "tail_baseline_success_count",
                "tail_carry_sliced_success_count",
                "polynomial_carry_enumeration_certificate_count",
                "proved_uniform_inverse_polynomial_coverage_count",
                "source_contract_satisfying_row_count",
            ],
            dependencies=[
                "dcp_subset_sum_carry_slice_lattice.py",
                "dcp_subset_sum_low_bit_bdd.py",
                "dcp_subset_sum_conditioned_quotient.py",
                "dcp_subset_sum_lattice_search.py",
            ],
            next_actions=[
                "Scale paired trials beyond the finite high-success regime.",
                "Analyze Gaussian-heuristic and competing-short-vector distributions for each carry slice.",
                "Prove whether the extra exact equation changes average-case shortest-vector separation.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-CARRY-HIGH-PART-NOGO",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Carry-selected high-quotient product-distribution no-go",
            status="planned",
            hypothesis=(
                "Selecting a reachable carry from exposed low bits may create a specially distributed high quotient "
                "whose ordinary high-only lattice geometry is easier than a fresh random subset-sum instance."
            ),
            protocol=(
                "Prove the low/high decomposition product law, condition on arbitrary low data and a reachable carry, "
                "translate the high target by that carry, verify exact finite bijection controls, and charge a union "
                "bound over every polynomially enumerable carry."
            ),
            positive_signal=(
                "No positive signal is expected inside the high-only class. A surviving mechanism must retain joint "
                "low/high constraints or prove that a concrete generic high event already has inverse-polynomial probability."
            ),
            falsifiers=[
                "The high labels remain independent uniform after conditioning on all low data.",
                "Target subtraction by the carry is a permutation of the quotient group.",
                "A low-only carry selector leaves the high instance exactly generic.",
                "A polynomial carry sweep is claimed to rescue an exponentially rare generic event without charging the union bound.",
            ],
            metrics=[
                "conditional_product_uniformity_theorem_count",
                "low_only_selection_no_bias_theorem_count",
                "polynomial_carry_union_bound_theorem_count",
                "exact_translation_control_failure_count",
                "joint_low_high_geometry_no_go_count",
                "polynomial_witness_solver_count",
            ],
            dependencies=[
                "dcp_carry_high_part_no_go.py",
                "dcp_subset_sum_carry_slice_lattice.py",
                "dcp_subset_sum_preconditioned_geometry.py",
            ],
            next_actions=[
                "Stop treating low-only carry selection as a high-coefficient distribution change.",
                "For a concrete high-only LLL event, prove its generic source probability before sweeping carries.",
                "Search only genuinely joint low/high reduced-basis events or carry-restricted witness geometry.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-BOOLEAN-COSET-SEPARATION",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Uniform-legal Boolean witness-coset separation theorem",
            status="planned",
            hypothesis=(
                "Exponentially many short marker-zero relations may close marker-aware affine decoding because they "
                "create correspondingly close valid Boolean witnesses in a typical legal target coset."
            ),
            protocol=(
                "Count ordered Boolean witness pairs by Hamming distance under independent uniform labels and targets; "
                "derive exact first and second witness-count moments, condition on the true uniform-legal source via "
                "Paley-Zygmund, prove a sub-half-radius exponential separation bound, and verify exact small source censuses."
            ),
            positive_signal=(
                "A source-correct theorem can keep marker-aware affine decoding mathematically open by proving short "
                "kernel relations almost never connect legal Boolean witnesses. It does not count as a solver."
            ),
            falsifiers=[
                "The ordered-pair expectation fails an exhaustive source census.",
                "A planted size-biased target is substituted for the uniform-legal source.",
                "A source-average conditional bound is promoted to a fixed-instance guarantee.",
                "Sub-half Hamming separation is promoted to uniqueness against far witnesses.",
                "Separation geometry is promoted without a polynomial marker-aware decoder and coverage theorem.",
            ],
            metrics=[
                "exact_pair_census_count",
                "exact_pair_formula_failure_count",
                "uniform_legal_source_theorem_count",
                "fixed_beta_exponential_separation_theorem_count",
                "tail_inverse_polynomial_close_pair_no_go_row_count",
                "marker_aware_decoder_count",
                "proved_babai_or_lll_coverage_count",
            ],
            dependencies=[
                "dcp_subset_sum_boolean_coset_separation.py",
                "dcp_subset_sum_short_relation_theorem.py",
                "dcp_subset_sum_carry_relation_theorem.py",
                "dcp_subset_sum_marker_coset_theorem.py",
                "dcp_subset_sum_target_distribution.py",
            ],
            next_actions=[
                "Run qsearch.py dcp-boolean-coset-separation.",
                "Replace shortest-vector uniqueness arguments with marker-aware affine-coset geometry.",
                "Search for a polynomial decoder whose success event uses Boolean separation and prove uniform-legal coverage.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-MARKER-AWARE-LIST-DECODER",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Fixed-depth marker-aware nearest-plane list decoder",
            status="planned",
            hypothesis=(
                "A valid Boolean witness may lie in one of polynomially many neighboring nearest-plane cells even "
                "when the single Babai cell misses it, providing a stronger legal classical attack on the open "
                "marker-aware affine route."
            ),
            protocol=(
                "LLL-reduce the standard and every reachable carry-sliced marker-zero kernel; enumerate all "
                "nearest-plane paths with at most one or two one-step rounding deviations; sample independent uniform "
                "targets, determine legality exactly by meet in the middle, and verify every output against the original equation."
            ),
            positive_signal=(
                "Persistent legal-target recovery beyond depth zero is a stronger polynomial classical baseline that "
                "must be killed. A source-conditioned inverse-polynomial cell-mass theorem would dequantize the route."
            ),
            falsifiers=[
                "The generated list count differs from sum_{j<=k} 2^j binom(d,j) for the actual kernel rank d.",
                "A planted witness replaces an independent uniform target.",
                "An unverified affine vector is counted as a subset-sum witness.",
                "Finite recovery is promoted to a source-coverage theorem.",
                "Fixed-depth failure is promoted to a lower bound against general affine-CVP decoding.",
            ],
            metrics=[
                "fixed_depth_polynomial_list_theorem_count",
                "candidate_count_theorem_failure_count",
                "standard_depth_zero_legal_success_count",
                "standard_max_depth_legal_success_count",
                "carry_depth_zero_legal_success_count",
                "carry_max_depth_legal_success_count",
                "strict_standard_list_improvement_count",
                "strict_carry_list_improvement_count",
                "proved_inverse_polynomial_uniform_legal_coverage_count",
            ],
            dependencies=[
                "dcp_marker_aware_list_decoder.py",
                "dcp_subset_sum_boolean_coset_separation.py",
                "dcp_subset_sum_affine_cvp_baseline.py",
                "dcp_subset_sum_affine_cvp_scaling.py",
                "dcp_subset_sum_marker_coset_theorem.py",
            ],
            next_actions=[
                "Run qsearch.py dcp-marker-list-decoder.",
                "If bounded lists recover, derive the exact source mass of their nearest-plane cell union.",
                "If they collapse, characterize the first required deviation depth without claiming a general lower bound.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-MARKER-DEVIATION-GEOMETRY",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Exact marker-witness nearest-plane deviation geometry",
            status="planned",
            hypothesis=(
                "The collapse of fixed-depth marker lists can be localized to growing rounding-deviation depth, "
                "rounding offsets larger than one, or both, by replaying every exact witness path in the reduced kernel."
            ),
            protocol=(
                "Enumerate every witness by meet in the middle, solve its lattice point exactly in each LLL-reduced "
                "standard and witness-carry kernel, replay nearest-plane with the true later coefficients, and record "
                "all rounding offsets and exact bounded-list membership."
            ),
            positive_signal=(
                "A stable low-complexity deviation law suggests a stronger classical decoder; a proved source law "
                "forcing growing depth would close this branching grammar without claiming a general affine lower bound."
            ),
            falsifiers=[
                "A witness path replay does not end at its exact +/-1 error vector.",
                "Truncated witness sets are treated as witness-complete.",
                "A planted target replaces independent uniform target sampling.",
                "Finite deviation growth is promoted to an asymptotic source theorem.",
                "Escape from one-step branches is promoted to a lower bound against other affine decoders.",
            ],
            metrics=[
                "exact_replay_failure_count",
                "complete_witness_enumeration_trial_count",
                "tail_standard_depth_two_predicted_success_count",
                "tail_carry_depth_two_predicted_success_count",
                "tail_standard_one_step_tree_escape_count",
                "tail_carry_one_step_tree_escape_count",
                "proved_asymptotic_deviation_growth_count",
                "proved_fixed_depth_source_coverage_upper_bound_count",
            ],
            dependencies=[
                "dcp_marker_deviation_geometry.py",
                "dcp_marker_aware_list_decoder.py",
                "dcp_subset_sum_affine_bdd_geometry.py",
                "dcp_subset_sum_affine_cvp_scaling.py",
            ],
            next_actions=[
                "Run qsearch.py dcp-marker-deviations.",
                "Fit no claim from finite medians; derive an LLL-coordinate source theorem or abandon this grammar.",
                "If offsets stay bounded but depth grows, audit growing-depth list exponents explicitly.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-MARKER-ALL-TARGET-COVERAGE",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Exact all-target marker-list coverage census",
            status="planned",
            hypothesis=(
                "Target-independent marker kernels permit exact fixed-depth coverage over every legal target by "
                "classifying each Boolean assignment from its Gram-Schmidt error projections once."
            ),
            protocol=(
                "Prove the witness rounding-offset identity, convert exact Gram-Schmidt rows to integer projection "
                "tests, Gray-code the full Boolean cube, group assignments by their exact target, and report complete "
                "legal-target coverage for standard and carry-sliced branch depths."
            ),
            positive_signal=(
                "Exact coverage eliminates target-sampling noise and can expose the label statistic needed for a "
                "source theorem or decisively falsify small-size fixed-depth optimism."
            ),
            falsifiers=[
                "Either marker-zero kernel changes with target or carry.",
                "Integer projection decisions differ from exact rational Gram-Schmidt rounding.",
                "Any Boolean assignment or legal target is omitted from a claimed complete row.",
                "Finite exact target coverage is promoted to an asymptotic random-label law.",
                "Fixed-depth decay is promoted to a lower bound against other affine decoders.",
            ],
            metrics=[
                "target_independent_kernel_failure_count",
                "full_boolean_cube_failure_count",
                "target_independent_rounding_identity_theorem_count",
                "exact_all_target_coverage_census_count",
                "tail_mean_standard_max_depth_coverage",
                "tail_mean_carry_max_depth_coverage",
                "tail_mean_standard_no_one_step_target_fraction",
                "tail_mean_carry_no_one_step_target_fraction",
                "proved_asymptotic_fixed_depth_coverage_bound_count",
            ],
            dependencies=[
                "dcp_marker_all_target_coverage.py",
                "dcp_marker_deviation_geometry.py",
                "dcp_marker_aware_list_decoder.py",
            ],
            next_actions=[
                "Run qsearch.py dcp-marker-all-targets.",
                "Correlate exact coverage with preregistered reduced-basis statistics across independent label rows.",
                "Prove a random-label concentration law or abandon fixed-depth branching.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-PRECONDITIONED-GEOMETRY",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Exact low-bit-conditioned residual geometry theorem",
            status="planned",
            hypothesis=(
                "Conditioning O(log n) low subset-sum bits changes high-residual candidate density or variance enough "
                "to explain a polynomial quotient-lattice solver."
            ),
            protocol=(
                "Condition on the complete low-bit data, prove exact first and second factorial moments for every fixed "
                "low fiber and residual window, then audit finite exact multiplicities without treating simulation as proof."
            ),
            positive_signal=(
                "Only higher-order correlation, basis geometry, or an implicit decoder survives after the exact pairwise "
                "moment theorem, and it comes with inverse-polynomial legal coverage and polynomial resources."
            ),
            falsifiers=[
                "The low fiber and quotient modulus shrink by the same factor, leaving the density exponent unchanged.",
                "Residual indicators are pairwise independent for every fixed low fiber.",
                "The proposed improvement uses only fixed residual-window counts or their variance.",
                "Finite LLL behavior has no higher-order or basis-geometric theorem.",
            ],
            metrics=[
                "theorem_certificate_count",
                "exact_conditional_first_moment_certificate_count",
                "exact_conditional_second_factorial_moment_certificate_count",
                "exact_conditional_variance_certificate_count",
                "maximum_absolute_density_exponent_change",
                "mean_tail_conditional_to_unconditioned_density_ratio",
                "count_based_geometry_improvement_proved_count",
                "lll_geometry_improvement_proved_count",
                "polynomial_witness_solver_proved_count",
                "source_contract_satisfying_row_count",
            ],
            dependencies=[
                "dcp_subset_sum_preconditioned_geometry.py",
                "dcp_subset_sum_low_bit_bdd.py",
                "dcp_subset_sum_conditioned_quotient.py",
                "dcp_subset_sum_carry_slice_lattice.py",
            ],
            next_actions=[
                "Search only higher-order residual correlations not fixed by pairwise moments.",
                "Define an LLL basis statistic and prove it changes under low-bit conditioning.",
                "Retire count-only preconditioner mutations immediately.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-FOURTH-MOMENT-OBSTRUCTION",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Low-fiber fourth-moment additive-energy obstruction",
            status="planned",
            hypothesis=(
                "Logarithmic low-bit conditioning creates a fixed low-order residual correlation that can support a "
                "polynomial high-bit subset-sum decoder."
            ),
            protocol=(
                "Prove exact three-wise residual independence, localize every fourth-order deviation to distinct xor-zero "
                "quadruples, compute their additive energy by Walsh transform, and bound the fourth factorial moment."
            ),
            positive_signal=(
                "An inverse-polynomial source mass of atypical low fibers survives the exact vanishing source-average "
                "theorem, with an efficiently computable observable and polynomial witness-decoder implication."
            ),
            falsifiers=[
                "The proposed signal has degree at most three and is exactly zero by joint uniformity.",
                "A fourth-order tuple is affine independent and therefore exactly uniform.",
                "Measured additive-energy excess decays and has no uniform lower bound.",
                "The statistic requires exponential Walsh tables or has no polynomial decoder implication.",
            ],
            metrics=[
                "theorem_certificate_count",
                "triplewise_independence_certificate_count",
                "fourth_order_localization_certificate_count",
                "maximum_tail_additive_energy_inflation",
                "maximum_tail_fourth_excess_relative_upper_bound",
                "fitted_log2_additive_energy_inflation_slope_per_n",
                "fitted_log2_fourth_excess_relative_upper_bound_slope_per_n",
                "proved_uniform_polynomial_energy_inflation_bound_count",
                "source_fourth_moment_certificate_count",
                "proved_source_fixed_offset_fourth_excess_vanishing_count",
                "proved_asymptotic_fixed_fourth_order_obstruction_count",
                "polynomial_witness_solver_proved_count",
            ],
            dependencies=[
                "dcp_subset_sum_fourth_moment_obstruction.py",
                "dcp_subset_sum_preconditioned_geometry.py",
                "dcp_subset_sum_low_bit_bdd.py",
            ],
            next_actions=[
                "Bound the source probability of atypically energetic low fibers despite vanishing mean excess.",
                "Search for an implicit polynomial estimator and decoder only on a proved inverse-polynomial tail.",
                "Move to growing-order Smith spectra or reduced-basis geometry if atypical order four is absent.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-SMITH-MOMENT-SPECTRUM",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Density-one subset-sum Smith moment spectrum",
            status="planned",
            hypothesis=(
                "An atypical fixed-fifth/fixed-sixth, fixed order at least seven, or growing-order 2-adic dependency class in random "
                "density-one modular subset sum survives low-order obstructions and supports an implicit polynomial statistic."
            ),
            protocol=(
                "Compute exact finite factorial moments by complete Smith-normal-form census where tractable, sample "
                "dependency types elsewhere with an explicit rare-event warning, and derive candidate asymptotic class "
                "counts rather than fitting finite moment slopes."
            ),
            positive_signal=(
                "A uniformly counted atypical fifth/sixth-order, order>=7, or growing-order Smith class has nonnegligible source contribution, an "
                "implicit polynomial estimator, and a proved witness-decoder implication."
            ),
            falsifiers=[
                "The proposed class is already covered by pairwise, triplewise, or source-average fourth-order no-go theorems.",
                "The class appears only because moment order exceeds the small-instance source matrix rank.",
                "The evidence is absence or frequency in polynomially many sampled tuples.",
                "The statistic requires enumerating exponentially many assignment tuples or has no decoder implication.",
            ],
            metrics=[
                "complete_exact_census_row_count",
                "sampled_rare_event_blind_row_count",
                "fourth_moment_formula_crosscheck_count",
                "fourth_moment_formula_crosscheck_failure_count",
                "source_fifth_moment_certificate_count",
                "fifth_moment_formula_crosscheck_count",
                "proved_asymptotic_fixed_fifth_order_obstruction_count",
                "unresolved_order_at_least_five_row_count",
                "unresolved_order_at_least_six_row_count",
                "maximum_observed_two_adic_valuation",
                "proved_asymptotic_order_at_least_five_obstruction_count",
                "proved_growing_order_obstruction_count",
                "polynomial_witness_decoder_count",
            ],
            dependencies=[
                "dcp_subset_sum_smith_moment_spectrum.py",
                "dcp_subset_sum_fourth_moment_obstruction.py",
                "dcp_subset_sum_preconditioned_geometry.py",
            ],
            next_actions=[
                "Classify order-seven affine dependency matroids or prove a general fixed-order transfer bound.",
                "Derive uniform transfer recurrences without exploding the state space.",
                "Search for an implicit statistic only after a nonnegligible source contribution is proved.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-SMITH-TRANSFER-ORDER-SIX",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Order-six subset-sum Smith transfer theorem",
            status="planned",
            hypothesis=(
                "A generic source-averaged fixed-sixth Smith dependency class retains nonvanishing density-one signal "
                "at fixed register offset."
            ),
            protocol=(
                "Enumerate the closed HNF lattice-state graph generated by all 64 Boolean six-row columns, verify "
                "non-self acyclicity and ordered-distinct tuple normalization, and compare every bad terminal lattice's "
                "Boolean self-loop base with its source-probability rank penalty."
            ),
            positive_signal=(
                "A certified bad terminal lattice has growth ratio at least one, or an atypical inverse-polynomial "
                "conditioned-fiber class evades the source-average transfer bound and has an implicit decoder."
            ),
            falsifiers=[
                "The complete state graph has strict growth ratio below one for every bad terminal lattice.",
                "A finite sixth-moment excess is cited despite the exact asymptotic transfer bound.",
                "The route requires an order that grows with n but is presented as fixed order six.",
                "No implicit statistic or witness-decoder implication is supplied.",
            ],
            metrics=[
                "reachable_lattice_state_count",
                "terminal_distinct_lattice_state_count",
                "non_generic_terminal_state_count",
                "tuple_count_normalization_certificate_count",
                "maximum_bad_growth_ratio",
                "proved_asymptotic_fixed_sixth_order_obstruction_count",
                "proved_asymptotic_order_at_least_seven_obstruction_count",
                "proved_growing_order_obstruction_count",
                "polynomial_witness_decoder_count",
            ],
            dependencies=[
                "dcp_subset_sum_smith_transfer.py",
                "dcp_subset_sum_smith_moment_spectrum.py",
            ],
            next_actions=[
                "Attempt a symmetry-reduced order-seven transfer system.",
                "Prove a general fixed-order contraction theorem from Boolean lattice geometry.",
                "Search atypical conditioned fibers only with a source-probability lower bound and implicit decoder.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-ALL-FIXED-MOMENT-THEOREM",
            candidate_id="DHS-GOWERS-SIEVE",
            title="All-fixed-order subset-sum source moment obstruction",
            status="planned",
            hypothesis=(
                "Increasing to some sufficiently large but fixed factorial-moment order evades the low-order source "
                "obstructions for density-one modular subset sum."
            ),
            protocol=(
                "Formalize the finite monotone lattice transfer for arbitrary fixed order k; use an injective coordinate "
                "projection to bound Boolean points in each rank-r span and characterize equality via Boolean linear "
                "coordinate functionals."
            ),
            positive_signal=(
                "A fixed-order terminal lattice with distinct rows attains Boolean growth ratio one, invalidating the "
                "strict contraction lemma, or a growing-order mechanism controls its k-dependent resources."
            ),
            falsifiers=[
                "Every bad fixed-order distinct-row lattice has growth ratio at most 1-2^-k.",
                "The proposed order is fixed and merely larger than previously audited constants.",
                "The route silently lets k grow without charging transfer states, samples, memory, or decoder cost.",
                "Source-moment excess has no implicit witness statistic or decoder implication.",
            ],
            metrics=[
                "certificate_count",
                "proved_fixed_order_source_obstruction_count",
                "general_all_fixed_orders_theorem_count",
                "largest_instantiated_fixed_order",
                "proved_growing_order_obstruction_count",
                "proved_atypical_conditioned_fiber_obstruction_count",
                "polynomial_witness_decoder_count",
            ],
            dependencies=[
                "dcp_subset_sum_fixed_order_moment_theorem.py",
                "dcp_subset_sum_smith_transfer.py",
            ],
            next_actions=[
                "Formalize resource growth for k=k(n) and reject uncharged state-space explosions.",
                "Search for inverse-polynomial atypical conditioned-fiber tails not contradicted by source averaging.",
                "Prioritize explicit reduced-basis events over further fixed-degree moment escalation.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-CONDITIONED-FIXED-MOMENT-TAIL",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Conditioned low-fiber fixed-moment tail obstruction",
            status="planned",
            hypothesis=(
                "Although generic fixed source moments vanish, an inverse-polynomial mass of exposed low-bit fibers has "
                "inverse-polynomial conditional bad-tuple signal usable by a partial subset-sum decoder."
            ),
            protocol=(
                "Define the nonnegative source-nongeneric tuple contribution B_k, condition it on the complete low-bit "
                "sigma-field, apply the tower property and Markov at every fixed inverse-polynomial threshold, and keep "
                "signed or reduced-basis observables outside the claim."
            ),
            positive_signal=(
                "A growing-order, signed, or non-moment statistic evades domination by B_k and has inverse-polynomial "
                "source mass, efficient detection, and a polynomial witness-decoder implication."
            ),
            falsifiers=[
                "The proposed signal is a nonnegative fixed-order bad-tuple contribution covered by tower plus Markov.",
                "Large conditional signal appears only on exponentially small source mass.",
                "The evidence selects energetic finite fibers without a source-tail theorem.",
                "No efficient fiber detector or witness decoder is supplied.",
            ],
            metrics=[
                "certificate_count",
                "proved_conditioned_tail_bound_count",
                "general_fixed_order_conditioned_tail_theorem_count",
                "proved_growing_order_conditioned_tail_count",
                "proved_signed_statistic_tail_count",
                "proved_reduced_basis_event_tail_count",
                "polynomial_witness_decoder_count",
            ],
            dependencies=[
                "dcp_subset_sum_conditioned_tail_theorem.py",
                "dcp_subset_sum_fixed_order_moment_theorem.py",
            ],
            next_actions=[
                "Define k(n) with explicit state/sample/memory scaling before any growing-order experiment.",
                "Specify a signed observable and prove why bad-tuple domination fails without hiding exponential variance.",
                "Preregister reduced-basis events with inverse-polynomial source coverage and decoder implications.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-GROWING-ORDER-MOMENT-THEOREM",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Growing-order subset-sum moment obstruction",
            status="planned",
            hypothesis=(
                "A nonnegative moment order k(n) below the half-logarithmic boundary can retain source signal once the "
                "fixed-order theorem is no longer uniform."
            ),
            protocol=(
                "Bound lattice-enlarging transitions by q=2^k, count their positions and identities, apply Hadamard to "
                "Smith numerators, and compare the complete path overhead with strict bad-state contraction."
            ),
            positive_signal=(
                "A half-logarithmic-or-larger, signed, or non-moment mechanism survives with explicit state, sample, "
                "memory, source-coverage, and decoder accounting."
            ),
            falsifiers=[
                "The schedule satisfies 4^k log n=o(n) and is covered by the uniform transfer bound.",
                "The proposal ignores the q=2^k pattern and transition overhead.",
                "Finite moment excess is cited against an asymptotic path-count theorem.",
                "No implicit statistic or polynomial witness decoder is supplied.",
            ],
            metrics=[
                "row_count",
                "finite_bound_below_one_row_count",
                "maximum_instantiated_moment_order",
                "proved_sub_half_log_growing_order_obstruction_count",
                "proved_half_log_boundary_obstruction_count",
                "proved_super_half_log_order_obstruction_count",
                "proved_signed_statistic_obstruction_count",
                "polynomial_witness_decoder_count",
            ],
            dependencies=[
                "dcp_subset_sum_growing_order_theorem.py",
                "dcp_subset_sum_fixed_order_moment_theorem.py",
            ],
            next_actions=[
                "Analyze the k approximately (1/2)log_2 n boundary with symmetry-reduced transfer or sharper entropy bounds.",
                "Demand explicit estimation and decoder costs for every boundary-order statistic.",
                "Compare boundary-order moments against signed contractions and reduced-basis events.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-EMBEDDING-VOLUME-THEOREM",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Density-one embedding volume geometry theorem",
            status="planned",
            hypothesis=(
                "The standard or logarithmically carry-sliced modular embedding creates an asymptotic planted "
                "short-vector gap visible from covolume."
            ),
            protocol=(
                "Compute the square standard determinant and rectangular sliced Gram determinant exactly, derive "
                "determinant-root limits for m=n+c and b=O(log n), and compare the planted norm with the Gaussian "
                "volume scale without treating that heuristic as a shortest-vector theorem."
            ),
            positive_signal=(
                "A non-volume local Gram-Schmidt or short-vector count event has inverse-polynomial source coverage and "
                "supports deterministic polynomial witness extraction."
            ),
            falsifiers=[
                "Both determinant roots tend to the same constant and the planted/volume ratio does not vanish.",
                "A claimed gap is only a finite LLL success rate or Gaussian-heuristic assertion.",
                "Logarithmic slicing changes only subexponential covolume factors.",
                "No local reduced-basis event, source-coverage theorem, or decoder implication is stated.",
            ],
            metrics=[
                "exact_standard_covolume_theorem_count",
                "exact_carry_sliced_covolume_theorem_count",
                "volume_only_asymptotic_separation_ruled_out_count",
                "limiting_witness_to_gaussian_scale_ratio",
                "proved_local_reduced_basis_separation_count",
                "proved_average_case_short_vector_gap_count",
                "polynomial_witness_decoder_count",
            ],
            dependencies=[
                "dcp_subset_sum_embedding_volume_theorem.py",
                "dcp_subset_sum_lattice_search.py",
                "dcp_subset_sum_carry_slice_lattice.py",
            ],
            next_actions=[
                "Define explicit Gram-Schmidt or reduced-basis events not determined by covolume.",
                "Count competing short vectors under the exact source distribution.",
                "Prove inverse-polynomial event coverage and deterministic witness extraction before further sweeps.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-SHORT-RELATION-THEOREM",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Standard embedding short signed-relation theorem",
            status="planned",
            hypothesis=(
                "The planted binary marker vector is isolated among shortest vectors in the standard density-one "
                "modular subset-sum embedding."
            ),
            protocol=(
                "Count weight-one-quarter signed relations modulo global negation, compute exact joint probabilities "
                "from unit minors and Smith-(1,2) same-support pairs, and prove concentration by the second moment."
            ),
            positive_signal=(
                "An added constraint eliminates the signed-relation family, or a marker-aware reduction algorithm finds "
                "valid witnesses with inverse-polynomial source coverage despite exponentially many competitors."
            ),
            falsifiers=[
                "Signed marker-zero vectors no longer than the planted witness occur exponentially often.",
                "A uniqueness argument uses only determinant or Gaussian-heuristic scale.",
                "Finite LLL recovery is cited without asymptotic extraction coverage.",
                "The proposed repair does not eliminate or distinguish marker-zero relations.",
            ],
            metrics=[
                "positive_expectation_exponent_theorem_count",
                "exact_second_moment_theorem_count",
                "high_probability_exponential_competitor_theorem_count",
                "asymptotic_log2_expectation_rate",
                "standard_embedding_shortest_vector_uniqueness_ruled_out_count",
                "carry_sliced_short_relation_obstruction_count",
                "proved_lll_failure_probability_count",
                "polynomial_witness_decoder_count",
            ],
            dependencies=[
                "dcp_subset_sum_short_relation_theorem.py",
                "dcp_subset_sum_embedding_volume_theorem.py",
                "dcp_subset_sum_lattice_search.py",
            ],
            next_actions=[
                "Count signed relations satisfying the carry-sliced low coordinate exactly.",
                "Design marker-aware extraction and test whether competitors hide all valid marker vectors.",
                "Prove source coverage and asymptotic extraction probability before any solver claim.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-CARRY-RELATION-THEOREM",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Carry-sliced balanced signed-relation source-coverage theorem",
            status="planned",
            hypothesis=(
                "An exact O(log n) low-bit constraint uniformly isolates the planted binary marker vector in the "
                "carry-sliced density-one subset-sum embedding."
            ),
            protocol=(
                "Count balanced signed relations of weight at most (m+1)/4, lower-bound exact low-sum collisions by "
                "Cauchy-Schwarz, bound high modular joint probabilities by Smith minors, and apply Paley-Zygmund."
            ),
            positive_signal=(
                "A proved source-subset condition avoids the competitor event while retaining inverse-polynomial legal "
                "coverage, or a marker-aware polynomial extractor succeeds despite the competitors."
            ),
            falsifiers=[
                "Balanced relations retain positive exponential expectation after logarithmic slicing.",
                "Inverse-polynomial source mass contains exponentially many marker-zero competitors no longer than the witness.",
                "A claimed repair only reports finite LLL/BKZ success without source-subset separation.",
                "No deterministic marker-aware extraction implication is stated.",
            ],
            metrics=[
                "positive_expectation_exponent_theorem_count",
                "pairwise_joint_probability_bound_theorem_count",
                "inverse_polynomial_source_coverage_theorem_count",
                "high_probability_source_coverage_theorem_count",
                "carry_sliced_uniform_shortest_vector_isolation_ruled_out_count",
                "proved_lll_failure_probability_count",
                "polynomial_marker_aware_decoder_count",
            ],
            dependencies=[
                "dcp_subset_sum_carry_relation_theorem.py",
                "dcp_subset_sum_carry_slice_lattice.py",
                "dcp_subset_sum_short_relation_theorem.py",
            ],
            next_actions=[
                "Refine the overlap census to test whether competitor coverage tends to one.",
                "Characterize source subsets where balanced relations are suppressed.",
                "Design and prove or kill marker-aware extraction among marker-zero competitors.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-MARKER-COSET-THEOREM",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Marker-coset affine-CVP equivalence theorem",
            status="planned",
            hypothesis=(
                "Filtering for marker-one vectors turns standard or carry-sliced LLL output into a polynomial binary "
                "subset-sum witness decoder."
            ),
            protocol=(
                "Decompose each embedding into the marker-zero relation kernel and marker-one affine coset; prove the "
                "exact witness-radius equivalence under explicit scale conditions and audit marker gcd normalization."
            ),
            positive_signal=(
                "A polynomial affine-CVP algorithm returns a radius-sqrt(m+1) marker-one vector on an inverse-polynomial "
                "fraction of legal uniform instances with deterministic witness verification."
            ),
            falsifiers=[
                "Marker filtering merely restates the original binary subset-sum search.",
                "Extended-gcd marker normalization produces no useful norm bound.",
                "Finite reduced-row success has no source-coverage theorem.",
                "The proposed method assumes uniqueness despite multiple legal witnesses.",
            ],
            metrics=[
                "exact_marker_kernel_affine_coset_decomposition_count",
                "basis_marker_gcd_one_theorem_count",
                "exact_witness_radius_equivalence_theorem_count",
                "polynomial_unbounded_marker_one_vector_theorem_count",
                "polynomial_short_marker_one_decoder_count",
                "proved_affine_cvp_easier_than_subset_sum_count",
            ],
            dependencies=[
                "dcp_subset_sum_marker_coset_theorem.py",
                "dcp_subset_sum_carry_relation_theorem.py",
                "dcp_subset_sum_lattice_search.py",
            ],
            next_actions=[
                "Implement affine nearest-plane and embedding baselines with exact marker-coset diagnostics.",
                "Search source-conditioned kernel geometries that imply bounded-distance decoding.",
                "Prove or falsify inverse-polynomial legal coverage for any marker-aware extractor.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-AFFINE-CVP-BASELINE",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Marker-aware affine-CVP nearest-plane baseline",
            status="planned",
            hypothesis=(
                "LLL-reduced nearest plane in the marker-zero kernel finds short marker-one witness vectors on an "
                "inverse-polynomial fraction of legal density-one subset-sum inputs."
            ),
            protocol=(
                "Run exact-rational Babai nearest plane against the target affine coset in standard and all reachable "
                "carry-sliced embeddings; track radius, constraint, binary-defect, legality, and tail scaling."
            ),
            positive_signal=(
                "Held-out tail legal coverage has a defensible inverse-polynomial lower bound and is explained by a "
                "source-conditioned BDD or Gram-Schmidt theorem."
            ),
            falsifiers=[
                "Tail success collapses with n.",
                "Nearest vectors retain nonzero constraints or binary defects.",
                "Success is confined to planted or otherwise size-biased targets.",
                "No theorem links finite coverage to an inverse-polynomial source subset.",
            ],
            metrics=[
                "standard_legal_success_count",
                "carry_sliced_legal_success_count",
                "invalid_witness_count",
                "marker_coset_enforced_trial_count",
                "tail_standard_success_count",
                "tail_carry_sliced_success_count",
                "proved_uniform_inverse_polynomial_coverage_count",
                "proved_affine_cvp_scaling_advantage_count",
                "polynomial_witness_decoder_count",
            ],
            dependencies=[
                "dcp_subset_sum_affine_cvp_baseline.py",
                "dcp_subset_sum_marker_coset_theorem.py",
                "dcp_subset_sum_carry_slice_lattice.py",
            ],
            next_actions=[
                "Add source-conditioned Gram-Schmidt and BDD-radius diagnostics.",
                "Compare stronger nearest-plane, enumeration, and bounded-distance decoders under identical source draws.",
                "Seek an analytic source-coverage bound before any solver claim.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-AFFINE-CVP-SCALING",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Source-native marker-aware affine-CVP scaling audit",
            status="planned",
            hypothesis=(
                "The high finite success of marker-aware standard or carry-sliced nearest plane persists on independent "
                "uniform targets at larger density-one scales."
            ),
            protocol=(
                "Use exact meet-in-the-middle legality for every independent uniform target, run exact-rational affine "
                "Babai through larger n, and retain distance, binary-defect, constraint, and tail-success histories."
            ),
            positive_signal=(
                "Persistent held-out classical success identifies a dequantization attack; a quantum proposal must beat "
                "it. An algorithmic claim additionally needs an analytic inverse-polynomial coverage theorem."
            ),
            falsifiers=[
                "Carry-sliced tail success collapses as n grows.",
                "Distance or binary defect diverges away from the witness radius.",
                "A result discards failed runs whose targets are actually legal.",
                "A finite empirical slope is presented as an asymptotic theorem.",
            ],
            metrics=[
                "exact_mitm_legality_trial_count",
                "standard_legal_success_count",
                "carry_sliced_legal_success_count",
                "tail_standard_success_count",
                "tail_carry_sliced_success_count",
                "tail_mean_standard_distance_ratio",
                "tail_mean_carry_sliced_distance_ratio",
                "proved_inverse_polynomial_legal_coverage_count",
                "proved_asymptotic_affine_cvp_advantage_count",
            ],
            dependencies=[
                "dcp_subset_sum_affine_cvp_scaling.py",
                "dcp_subset_sum_affine_cvp_baseline.py",
                "dcp_subset_sum_marker_coset_theorem.py",
            ],
            next_actions=[
                "Run larger held-out n and confidence-controlled trial batches.",
                "Compute exact Babai-cell margins for all legal witnesses on tractable rows.",
                "Derive a source-conditioned Gram-Schmidt or BDD-radius law.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-AFFINE-BDD-GEOMETRY",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Exact witness-specific affine Babai-cell geometry audit",
            status="planned",
            hypothesis=(
                "Legal density-one witnesses retain positive nearest-plane decoding-cell margins in the standard or "
                "carry-sliced marker-zero kernel at growing n."
            ),
            protocol=(
                "Enumerate exact witnesses by meet in the middle, construct their +/-1 zero-constraint errors, audit "
                "exact Gram-Schmidt Babai cells, and separately test the global BDD sufficient condition."
            ),
            positive_signal=(
                "A source-distribution theorem lower-bounds positive witness-cell margin on an inverse-polynomial legal "
                "subset and yields a verified polynomial decoder."
            ),
            falsifiers=[
                "Positive witness-cell margins disappear in the scaling tail.",
                "The global Gram-Schmidt BDD condition never holds.",
                "Nearest-plane output disagrees with exhaustive witness-cell prediction.",
                "A finite cell frequency is promoted without a source theorem.",
            ],
            metrics=[
                "exact_witness_enumeration_trial_count",
                "standard_positive_babai_cell_trial_count",
                "carry_sliced_positive_babai_cell_trial_count",
                "standard_global_bdd_condition_trial_count",
                "carry_sliced_global_bdd_condition_trial_count",
                "cell_prediction_inconsistency_count",
                "tail_standard_positive_cell_trial_count",
                "tail_carry_sliced_positive_cell_trial_count",
                "proved_source_bdd_coverage_count",
            ],
            dependencies=[
                "dcp_subset_sum_affine_bdd_geometry.py",
                "dcp_subset_sum_affine_cvp_scaling.py",
                "dcp_subset_sum_marker_coset_theorem.py",
            ],
            next_actions=[
                "Classify witness-specific Gram-Schmidt coordinate distributions under the exact source.",
                "Search preprocessing that changes cell margins without selecting planted targets.",
                "Abandon nearest plane if positive margins vanish and no source theorem emerges.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-TARGET-DISTRIBUTION",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Uniform legal versus planted subset-sum target audit",
            status="planned",
            hypothesis=(
                "Regev's independent uniform source targets contain a detectable inverse-polynomial subfamily with "
                "non-generic representation multiplicity that supports a polynomial partial solver."
            ),
            protocol=(
                "Compute complete target multiplicity tables for random labels; compare independent uniform targets, "
                "uniform legal targets, and planted-witness size-biased targets; certify exact first and second factorial "
                "moments and measure polynomial multiplicity tails."
            ),
            positive_signal=(
                "A source-distribution theorem identifies an efficiently detectable inverse-polynomial high-multiplicity "
                "subfamily and a polynomial witness algorithm with a deterministic or coherent matching interface."
            ),
            falsifiers=[
                "The apparent representation gain occurs only under planted-witness target sampling.",
                "High-multiplicity source targets have sub-inverse-polynomial coverage or cannot be detected efficiently.",
                "Finite Poisson-like histograms are promoted to an asymptotic theorem.",
                "Multiplicity is observed without a polynomial witness algorithm.",
            ],
            metrics=[
                "moment_certificate_count",
                "mean_tail_legal_target_fraction",
                "mean_tail_planted_vs_uniform_legal_total_variation",
                "maximum_tail_planted_to_uniform_legal_mean_ratio",
                "maximum_tail_uniform_target_linear_tail_probability",
                "maximum_tail_uniform_target_quadratic_tail_probability",
                "mean_tail_poisson_total_variation",
                "proved_inverse_polynomial_high_multiplicity_legal_subfamily_count",
                "proved_polynomial_representation_solver_count",
                "source_contract_satisfying_row_count",
            ],
            dependencies=[
                "dcp_subset_sum_target_distribution.py",
                "dcp_subset_sum_bridge.py",
                "dcp_subset_sum_resource_frontier.py",
            ],
            next_actions=[
                "Derive higher factorial-moment or contiguity bounds for independent uniform targets.",
                "Search for efficiently detectable high-multiplicity statistics under the source law.",
                "Evaluate generalized representations without substituting planted target sampling.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-COHERENT-MATCHING-INTERFACE",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Coherent partial-solver matching-interface theorem audit",
            status="planned",
            hypothesis=(
                "Regev's deterministic matching routine extends to randomized or quantum subset-sum partial solvers "
                "when their randomness and witness workspaces preserve paired-endpoint coherence."
            ),
            protocol=(
                "Extract every deterministic use from the primary LaTeX source; derive an averaging and matching bound "
                "for target-independent explicit shared seeds; compute exact paired-workspace interference visibility; "
                "and separate seeded randomized solvers from arbitrary quantum relation solvers."
            ),
            positive_signal=(
                "A source-linked theorem proves inverse-polynomial DCP routine success for an expanded solver interface "
                "with polynomial resources, balanced paired amplitudes, and reversible workspace erasure."
            ),
            falsifiers=[
                "Solver coins are measured, target-dependent, or not shared across matched endpoints.",
                "Different witnesses leave orthogonal which-path workspaces.",
                "Paired amplitudes are unbalanced or have no inverse-polynomial overlap theorem.",
                "An interface theorem is presented as if it constructed a subset-sum solver.",
            ],
            metrics=[
                "primary_source_deterministic_use_site_count",
                "seeded_bridge_certificate_count",
                "proved_seeded_randomized_solver_bridge_count",
                "minimum_certified_routine_success_probability",
                "zero_visibility_counterexample_count",
                "proved_arbitrary_quantum_relation_solver_bridge_count",
                "proved_polynomial_partial_subset_sum_solver_count",
                "source_contract_satisfying_solver_count",
            ],
            dependencies=[
                "dcp_coherent_matching_interface.py",
                "dcp_subset_sum_bridge.py",
                "research/literature_cache/cs_0304005_source/quantum_average.tex",
            ],
            next_actions=[
                "Reclassify explicit-coin randomized subset-sum algorithms as interface-compatible.",
                "For quantum walks, derive a target-independent seed decomposition or paired-workspace fidelity bound.",
                "Keep solver construction and interface compatibility as separate proof obligations.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-QUANTUM-RELATION-FIDELITY",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Quantum relation paired-workspace fidelity audit",
            status="planned",
            hypothesis=(
                "A genuinely quantum density-one subset-sum relation solver can compose with Regev's matching routine "
                "only when paired endpoint amplitudes are balanced and retained witness/history workspaces have "
                "inverse-polynomial overlap or admit reversible canonical cleanup."
            ),
            protocol=(
                "Derive the exact uniform-support workspace-overlap and amplitude-balance identities; audit shared-seed, "
                "endpoint-tagged, sparse-history, common-core, and canonical-cleanup mechanisms; and require a concrete "
                "all-n solver, cleanup circuit, and overlap theorem before composition."
            ),
            positive_signal=(
                "A concrete polynomial density-one quantum solver exposes target-by-target amplitudes and histories, "
                "proves inverse-polynomial paired fidelity with bounded error, and composes through every DCP stage."
            ),
            falsifiers=[
                "Endpoint-dependent witness or walk histories are orthogonal across matched endpoints.",
                "Normalized common-history overlap decays exponentially at the required walk depth.",
                "Only finite overlap is measured, with no uniform scaling theorem.",
                "Canonical witness selection or garbage erasure requires exponential search, memory, or advice.",
                "The mechanism proves interface compatibility but does not construct a polynomial partial solver.",
            ],
            metrics=[
                "mechanism_count",
                "exact_zero_visibility_count",
                "exponential_history_overlap_count",
                "finite_only_or_conditional_count",
                "proved_shared_seed_interface_control_count",
                "proved_inverse_polynomial_overlap_count",
                "proved_polynomial_partial_solver_count",
                "proved_full_quantum_relation_composition_count",
            ],
            dependencies=[
                "dcp_quantum_relation_fidelity.py",
                "dcp_coherent_matching_interface.py",
                "dcp_subset_sum_bridge.py",
                "research/literature_cache/cs_0304005_source/quantum_average.tex",
            ],
            next_actions=[
                "Extract exact witness and history states from a concrete quantum subset-sum walk.",
                "Prove a target-independent history decomposition or inverse-polynomial paired-workspace fidelity.",
                "Compose cleanup, approximation, bad-register, and source-coverage bounds end to end.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-QUANTUM-WALK-SOURCE-AUDIT",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Primary-source audit of the 0.2182 subset-sum quantum walk",
            status="planned",
            hypothesis=(
                "The repaired Bonnetain--Bricout--Schrottenloher--Shen walk resolves its internal path-consistency "
                "problem, but neither its exponential QRAQM resource contract nor its marked-vertex output theorem "
                "supplies the polynomial coherent partial function required by Regev's matching reduction."
            ),
            protocol=(
                "Parse the cached arXiv LaTeX and fingerprint claims about time, memory, QRAQM, heuristic removal, "
                "history-independent updates, data-independent error, deterministic data structures, marked-set "
                "preservation, output type, and remaining heuristics. Audit resource and paired-output contracts separately."
            ),
            positive_signal=(
                "A primary-source theorem or explicit circuit gives polynomial resources, target-paired aligned output "
                "states, inverse-polynomial workspace fidelity, reversible cleanup, and a complete Regev composition."
            ),
            falsifiers=[
                "The repaired update remains path dependent or has target-dependent approximation error.",
                "The time or memory exponent remains positive.",
                "The algorithm requires exponentially large QRAQM.",
                "The source proves only marked-vertex recovery, not an aligned paired-endpoint output state.",
                "Internal history independence is promoted as if it proved output-workspace fidelity.",
            ],
            metrics=[
                "primary_source_claim_count",
                "verified_source_claim_count",
                "internal_history_independence_certificate_count",
                "data_independent_update_error_certificate_count",
                "positive_exponential_time_count",
                "positive_exponential_memory_count",
                "qraqm_required_count",
                "paired_endpoint_output_fidelity_theorem_count",
                "full_regev_composition_count",
            ],
            dependencies=[
                "dcp_quantum_walk_source_audit.py",
                "dcp_quantum_relation_fidelity.py",
                "research/literature_cache/2002.05276_source",
            ],
            next_actions=[
                "Extract the exact marked-output workspace and witness-selection map from the walk circuit.",
                "Test whether a coherent canonical-witness transform can avoid exponential enumeration.",
                "Search for a polynomial-resource walk mechanism rather than treating the 0.2182 baseline as one.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SYMMETRIC-RELATION-LIFT",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Symmetric double-evaluation lift for quantum relation solvers",
            status="planned",
            hypothesis=(
                "A purified quantum density-one subset-sum relation solver can replace Regev's deterministic partial "
                "function by evaluating both matched endpoints in a fixed order, measuring a symmetric witness-pair "
                "label, and paying an explicit polynomial weighted-matching loss."
            ),
            protocol=(
                "Verify the deterministic selector sites in Regev's primary source; derive exact orientation-amplitude "
                "and ordered-garbage identities for double endpoint evaluation; threshold mean relation success; apply "
                "the q-matching lemma; and retain all-good-register, verifier, purification, and resource assumptions."
            ),
            positive_signal=(
                "An exact circuit identity gives unit paired visibility for arbitrary solver amplitudes and garbage, "
                "while a weighted matching theorem transfers inverse-polynomial mean valid-output probability with "
                "only polynomial loss."
            ),
            falsifiers=[
                "The two orientations invoke endpoint circuits in different register orders.",
                "The current witness is not checked against the output in its target slot.",
                "The measured label does not identify the same ordered endpoint-witness pair on both branches.",
                "Mean relation success has no inverse-polynomial threshold support under the source distribution.",
                "The product-source all-good component is absent or has subpolynomial weight.",
                "An interface theorem is promoted as a polynomial solver construction.",
            ],
            metrics=[
                "verified_primary_source_site_count",
                "exact_symmetric_pair_identity_count",
                "ordered_garbage_alignment_certificate_count",
                "deterministic_selector_required_count",
                "coherent_relation_interface_certificate_count",
                "fixed_list_weighted_matching_loss_exponent",
                "global_source_weighted_matching_loss_exponent",
                "product_contamination_composition_certificate_count",
                "proved_polynomial_relation_solver_count",
                "proved_end_to_end_dcp_speedup_count",
            ],
            dependencies=[
                "dcp_symmetric_relation_lift.py",
                "dcp_coherent_matching_interface.py",
                "dcp_quantum_relation_fidelity.py",
                "research/literature_cache/cs_0304005_source/quantum_average.tex",
            ],
            next_actions=[
                "Formalize the double-evaluation circuit as a register-by-register unitary and measurement proof.",
                "Mechanize the product-mixture contamination composition in the end-to-end reduction ledger.",
                "Search for polynomial purified relation solvers now that deterministic selection is unnecessary.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-TWO-ADIC-FIBER-TRANSPORT",
            candidate_id="DHS-GOWERS-SIEVE",
            title="2-adic child-fiber transport and local-dictionary no-go audit",
            status="planned",
            hypothesis=(
                "Exact reversible transports between the two children of a low-bit subset-sum fiber may expose a "
                "polynomial relation sampler, but explicit coordinate, swap, and logarithmic-block dictionaries are "
                "expected to stall before linear 2-adic depth."
            ),
            protocol=(
                "Prove coordinate-flip, residue-matched-swap, and block-pattern transport identities; measure their "
                "scaling depth on random density-one labels; prove a union-bound no-go for polynomial explicit "
                "O(log n)-block dictionaries; and retain implicit global transports and fiber walks separately."
            ),
            positive_signal=(
                "An implicit polynomial circuit or polynomial-gap walk transports inverse-polynomial fiber mass through "
                "k=Theta(n), returns verified binary witnesses, and survives classical mixing/reconstruction baselines."
            ),
            falsifiers=[
                "Transport coverage disappears after O(log n) low bits.",
                "The proposed circuit merely enumerates a polynomial correction dictionary.",
                "The fiber graph fragments under an efficiently computable invariant.",
                "Starting-state preparation, conductance, or child marking is exponentially costly.",
                "A finite low-bit symmetry is promoted as a full relation solver.",
            ],
            metrics=[
                "exact_identity_certificate_count",
                "maximum_observed_single_flip_depth",
                "maximum_observed_swap_depth",
                "maximum_observed_block_transport_depth",
                "minimum_tail_transport_free_bits",
                "local_dictionary_linear_depth_no_go_count",
                "open_implicit_transport_architecture_count",
                "proved_polynomial_linear_depth_transport_count",
                "proved_polynomial_relation_solver_count",
            ],
            dependencies=[
                "dcp_two_adic_fiber_transport.py",
                "dcp_subset_sum_low_bit_bdd.py",
                "dcp_subset_sum_conditioned_quotient.py",
                "dcp_symmetric_relation_lift.py",
            ],
            next_actions=[
                "Construct the fiber transport graph and test component invariants and spectral gaps exactly at small n.",
                "Search implicit arithmetic involutions outside the explicit block-dictionary model.",
                "Compose any surviving transport with exact low-bit state preparation and the symmetric relation lift.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-FIBER-TRANSPORT-GRAPH",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Exact low-fiber transport graph and spectral audit",
            status="planned",
            hypothesis=(
                "Local 2-adic transports may generate a large cross-child component with useful conductance even when "
                "no explicit correction covers the full fiber, but finite connectivity must survive exact classical "
                "traversal and scale to a uniform polynomial-gap theorem."
            ),
            protocol=(
                "Enumerate exact uniformly supported low-residue fibers; build graphs from divisible-coordinate flips, "
                "equal-residue swaps, and fixed small-block substitutions; compute components, child mixing, normalized "
                "adjacency gaps, invariants, and same-graph classical BFS costs."
            ),
            positive_signal=(
                "A source-uniform family has inverse-polynomial conductance and cross-child mass through linear depth, "
                "polynomial low-fiber state preparation and reflections, verified relation output, and no comparable "
                "classical local-mixing algorithm."
            ),
            falsifiers=[
                "Linear-depth graphs fragment under a classical invariant.",
                "Cross-child component mass or spectral gap collapses exponentially.",
                "Preparing the linear-depth fiber state is exponential.",
                "Classical traversal or mixing matches the claimed quantum mechanism.",
                "Finite eigenspectra are promoted without an all-n theorem.",
            ],
            metrics=[
                "linear_depth_row_count",
                "zero_cross_child_linear_depth_row_count",
                "fragmented_linear_depth_row_count",
                "minimum_linear_depth_largest_component_fraction",
                "minimum_linear_depth_cross_child_vertex_fraction",
                "minimum_positive_linear_depth_spectral_gap",
                "maximum_linear_depth_classical_bfs_vertex_visits",
                "uniform_polynomial_spectral_gap_theorem_count",
                "proved_polynomial_fiber_transport_walk_count",
                "proved_classical_separation_count",
            ],
            dependencies=[
                "dcp_fiber_transport_graph.py",
                "dcp_two_adic_fiber_transport.py",
                "dcp_subset_sum_low_bit_bdd.py",
            ],
            next_actions=[
                "Classify exact graph components by efficiently computable invariants.",
                "Fit no asymptotic gap until analytic conductance bounds exist for random source fibers.",
                "Design a polynomial linear-depth state preparation or kill the walk route.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SIGNED-PERMUTATION-TRANSPORT",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Exact signed-permutation fiber-transport classification",
            status="planned",
            hypothesis=(
                "A total coordinate permutation with arbitrary output-bit complements might provide a global "
                "constant next-bit subset-sum transport beyond the known exact-valuation coordinate pivot."
            ),
            protocol=(
                "Expand S_A(T(x))-S_A(x) for T(x)_j=x_{pi(j)} xor b_j; classify coefficient and constant-term "
                "constraints by sign orbits modulo 2^(k+1); exhaustively verify the classification at small moduli; "
                "and bound its incidence for random density-one labels at linear depth."
            ),
            positive_signal=(
                "A certified signed-permutation transport exists without any label of exact valuation k and has "
                "inverse-polynomial incidence through k=Theta(n)."
            ),
            falsifiers=[
                "The coefficient condition forces the signed label multiset to equal the original multiset.",
                "All non-self-inverse sign-orbit contributions cancel from the translation constant.",
                "The class exists exactly when an original exact-valuation coordinate pivot exists.",
                "Linear-depth incidence is exponentially small for independent uniform labels.",
                "Finite exhaustive checks are promoted beyond the accompanying symbolic proof.",
            ],
            metrics=[
                "exact_classification_theorem_count",
                "exhaustive_label_tuple_count",
                "exhaustive_classification_mismatch_count",
                "linear_depth_exponential_no_go_row_count",
                "maximum_linear_depth_transport_probability_bound",
                "proved_polynomial_relation_solver_count",
            ],
            dependencies=[
                "dcp_signed_permutation_transport.py",
                "dcp_two_adic_fiber_transport.py",
                "dcp_fiber_transport_graph.py",
            ],
            next_actions=[
                "Remove signed-coordinate permutations from the implicit global-transport search space.",
                "Classify genuinely coordinate-mixing GF(2)-affine transports next.",
                "Retain nonlinear, partial, and walk-based transports as separately gated architectures.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-AFFINE-TRANSPORT",
            candidate_id="DHS-GOWERS-SIEVE",
            title="GF(2)-affine subset-sum transport characterization",
            status="planned",
            hypothesis=(
                "XOR mixing between coordinates may evade the signed-permutation collapse and yield a total "
                "next-bit transport on random density-one subset-sum instances."
            ),
            protocol=(
                "Derive the exact integer-ANF congruences for T(x)=Px xor b, verify them against truth tables, "
                "exhaustively search small moduli for nonmonomial counterexamples, and reduce transport construction "
                "to witness extraction by evaluating T(0)."
            ),
            positive_signal=(
                "A source-uniform polynomial synthesis algorithm finds nonmonomial affine transports without an "
                "exact-valuation pivot and beats direct classical witness search."
            ),
            falsifiers=[
                "The ANF coefficients fail any required modular congruence.",
                "Every affine transport instance also has the old exact-valuation pivot.",
                "The transport construction merely hides direct search for b=T(0).",
                "Enumeration over GL(m,2) remains exponential.",
                "Finite small-modulus existence is promoted as an asymptotic algorithm.",
            ],
            metrics=[
                "exact_anf_theorem_count",
                "zero_image_witness_reduction_count",
                "anf_vs_truth_table_mismatch_count",
                "nonmonomial_affine_only_instance_count",
                "polynomial_affine_search_count",
                "proved_polynomial_relation_solver_count",
            ],
            dependencies=[
                "dcp_affine_transport.py",
                "dcp_signed_permutation_transport.py",
                "dcp_fiber_balance_obstruction.py",
            ],
            next_actions=[
                "Close the total affine route using the general Fourier transport theorem.",
                "Reuse the ANF verifier only for explicitly scoped partial-fiber affine proposals.",
                "Compare every partial proposal against direct classical search for the same witness relation.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-FIBER-BALANCE-OBSTRUCTION",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Fourier no-go for total global fiber transport",
            status="planned",
            hypothesis=(
                "An implicit or nonlinear total Boolean-cube bijection might toggle a subset-sum child bit even when "
                "no exact-valuation coordinate pivot exists."
            ),
            protocol=(
                "Prove that a total transport forces half-periodic subset-sum multiplicities; factor the first Fourier "
                "coefficient; derive the exact pivot equivalence; then audit balanced target fibers and optimal partial "
                "pairing mass separately under uniform-supported and subset-sample-weighted targets."
            ),
            positive_signal=(
                "A target-dependent partial fiber map has inverse-polynomial source coverage, a polynomial coherent "
                "implementation, verified witness output, and advantage over classical pairing access."
            ),
            falsifiers=[
                "Any proposed total full-cube transport lacks an exact-valuation pivot.",
                "A finite balanced fiber is treated as an efficient map.",
                "Large set-theoretic partial-pairing mass has no constructive circuit.",
                "Coverage holds only under planted or size-biased targets.",
                "A partial map is promoted without direct classical pairing baselines.",
            ],
            metrics=[
                "exact_total_transport_fourier_theorem_count",
                "finite_theorem_mismatch_count",
                "linear_depth_pivot_row_count",
                "maximum_linear_depth_uniform_balanced_target_fraction_without_pivot",
                "minimum_linear_depth_optimal_partial_pairing_mass",
                "proved_polynomial_target_fiber_map_count",
                "proved_polynomial_relation_solver_count",
            ],
            dependencies=[
                "dcp_fiber_balance_obstruction.py",
                "dcp_two_adic_fiber_transport.py",
                "dcp_signed_permutation_transport.py",
                "dcp_affine_transport.py",
            ],
            next_actions=[
                "Delete total full-cube transports from candidate generation.",
                "Search only target-dependent partial maps or non-bijective relation samplers.",
                "Prove source-weighted coverage and efficient construction before any quantum-walk composition.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-PARTIAL-RELATION-COVERAGE",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Explicit signed-relation partial-map coverage theorem",
            status="planned",
            hypothesis=(
                "A polynomial dictionary of signed-difference masks may pair inverse-polynomial mass between target "
                "fiber children even though no total global transport exists."
            ),
            protocol=(
                "Relate mask support to exact compatible-domain mass; count all ternary relations up to beta*n "
                "support; prove a uniform single-relation probability and union bound at k=n/2; then charge the "
                "coverage of every polynomial explicit dictionary."
            ),
            positive_signal=(
                "A source-valid relation family has sublinear support or an implicit target-indexed representation "
                "with inverse-polynomial coverage and beats direct classical relation search."
            ),
            falsifiers=[
                "The minimum signed-relation support is linear with exponentially high probability.",
                "Each mask covers only 2^(1-support) of subset-sampled assignments.",
                "Polynomially many masks retain exponentially small total coverage.",
                "Coverage is measured only under a favorable planted target law.",
                "An exponentially indexed implicit family is mislabeled as a polynomial dictionary.",
            ],
            metrics=[
                "linear_minimum_support_theorem_count",
                "polynomial_dictionary_exponential_coverage_theorem_count",
                "asymptotic_union_bound_exponent",
                "asymptotic_inverse_polynomial_existence_no_go_row_count",
                "asymptotic_inverse_polynomial_dictionary_coverage_no_go_row_count",
                "proved_target_indexed_implicit_map_no_go_count",
                "proved_polynomial_relation_solver_count",
            ],
            dependencies=[
                "dcp_partial_relation_coverage.py",
                "dcp_fiber_balance_obstruction.py",
                "dcp_subset_sum_short_relation_theorem.py",
            ],
            next_actions=[
                "Delete polynomial explicit signed-difference dictionaries from synthesis.",
                "Formalize target-indexed implicit map access and source-law coverage.",
                "Search nontranslation partial maps with matched classical relation baselines.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-TARGET-INDEXED-LOCALITY",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Target-indexed child-fiber locality obstruction",
            status="planned",
            hypothesis=(
                "Although fixed mask dictionaries fail, an implicitly target-indexed map may find a nearby legal "
                "partner for inverse-polynomial random-source mass at linear 2-adic depth."
            ),
            protocol=(
                "For a fixed source x, express every partner y as a flip set S whose signs are forced by x. Count "
                "Hamming balls without a spurious 2^|S| sign factor, prove the exact fixed-S hit probability, and "
                "derive the H_2(beta)-alpha union-bound exponent. Compare exact nearest-partner dynamic programming, "
                "meet-in-the-middle, local enumeration, and coherent exhaustive search under explicit query models."
            ),
            positive_signal=(
                "A linear-support target-indexed relation sampler with inverse-polynomial source-law coverage, a "
                "polynomial coherent implementation, verified paired output, and a separation from classical access "
                "to the same explicit labels."
            ),
            falsifiers=[
                "Target dependence is incorrectly counted as an independent sign choice for each changed coordinate.",
                "The proposed map changes at most beta*n bits where H_2(beta)<alpha.",
                "Polynomially many sampled sources are claimed to defeat a negative exponential union bound.",
                "Finite sparse partners are extrapolated against the asymptotic entropy threshold.",
                "Linear output support is mislabeled as a classical or quantum time lower bound.",
                "The quantum mechanism receives stronger relation access than the classical baseline.",
            ],
            metrics=[
                "arbitrary_target_indexed_local_map_no_go_theorem_count",
                "polynomial_source_batch_local_map_no_go_theorem_count",
                "asymptotic_locality_union_bound_exponent",
                "entropy_threshold_locality_fraction",
                "asymptotic_single_source_no_go_row_count",
                "asymptotic_polynomial_batch_no_go_row_count",
                "polynomial_classical_relation_solver_count",
                "polynomial_quantum_relation_solver_count",
                "unrestricted_linear_support_time_lower_bound_count",
            ],
            dependencies=[
                "dcp_target_indexed_locality.py",
                "dcp_partial_relation_coverage.py",
                "dcp_fiber_balance_obstruction.py",
            ],
            next_actions=[
                "Delete all target-indexed maps whose output remains inside the forbidden Hamming ball.",
                "Search only linear-support implicit relation samplers with source-law coverage.",
                "Require matched classical access and do not infer search hardness from Hamming distance.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-FIBER-ENTANGLEMENT",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Exact subset-sum fiber Schmidt spectrum and bond obstruction",
            status="planned",
            hypothesis=(
                "A low-bond tensor network may prepare or manipulate linear-depth modular subset-sum fiber states "
                "even when local target-indexed maps fail."
            ),
            protocol=(
                "Split coordinates, compute exact left/right residue multiplicities, derive the blockwise Schmidt "
                "spectrum, and prove a random-instance rank lower bound from pairwise independence and "
                "Paley-Zygmund. Audit exact and finite approximate bond requirements without converting "
                "entanglement into a general circuit lower bound."
            ),
            positive_signal=(
                "A partial-instance tensor preparation theorem with inverse-polynomial source-law coverage beyond the "
                "certified exact and 99-percent-fidelity density-one obstructions, "
                "a coherent verified relation output, and a matched classical contraction baseline."
            ),
            falsifiers=[
                "The exact Schmidt rank is exponential on a constant fraction of random fibers.",
                "The tensor network silently targets only a selected easy instance subset.",
                "Finite approximate ranks are presented without an asymptotic Schmidt-tail theorem.",
                "A coordinate reordering or cut is changed after seeing the instance without charging that procedure.",
                "Schmidt rank is mislabeled as a lower bound for all polynomial quantum circuits.",
                "The prepared state does not output a verified child-fiber relation."
            ],
            metrics=[
                "exact_schmidt_decomposition_theorem_count",
                "constant_fraction_exponential_rank_theorem_count",
                "exact_polynomial_bond_density_one_no_go_theorem_count",
                "approximate_polynomial_bond_asymptotic_no_go_theorem_count",
                "polynomial_layout_dictionary_density_one_no_go_theorem_count",
                "minimum_certified_hard_instance_probability",
                "minimum_polynomial_layout_family_hard_probability",
                "minimum_finite_99_percent_rank_fraction",
                "polynomial_fiber_state_preparation_count",
                "polynomial_relation_solver_count",
            ],
            dependencies=[
                "dcp_fiber_entanglement.py",
                "dcp_target_indexed_locality.py",
                "dcp_subset_sum_low_bit_bdd.py",
            ],
            next_actions=[
                "Delete exact and 99-percent-fidelity polynomial-bond density-one fiber-state proposals.",
                "Search only explicitly partial-instance tensor routes outside the certified constant-fraction hard set.",
                "Require any surviving state-preparation mechanism to emit a verified relation under the DCP source law.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-ADAPTIVE-LAYOUT-AUDIT",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Label-adaptive fiber tensor layout audit",
            status="planned",
            hypothesis=(
                "A layout selected after seeing the public subset-sum labels may compress the linear-depth fiber "
                "Schmidt spectrum even though every fixed polynomial layout dictionary fails."
            ),
            protocol=(
                "Prove a binomial large-deviation obstruction to balanced 2-adic subgroup compression; then compare "
                "natural, numeric, valuation-sorted, exact small-instance optimal, and target-adaptive swap layouts "
                "using exact Schmidt scores while charging O(m 2^q) per score."
            ),
            positive_signal=(
                "A polynomially computable additive layout statistic with an all-n polynomial 99-percent bond theorem, "
                "inverse-polynomial source coverage, coherent contraction, and verified relation output."
            ),
            falsifiers=[
                "Compression comes only from a constant even/odd subgroup factor.",
                "The adaptive selector evaluates exact residue tables of size 2^q.",
                "Finite layout improvements retain a positive log-rank slope.",
                "No all-layout or source-coverage theorem is supplied.",
                "The tensor state does not yield a verified child-fiber relation.",
            ],
            metrics=[
                "adaptive_valuation_compression_no_go_theorem_count",
                "valuation_inverse_polynomial_no_go_row_count",
                "exact_balanced_optimum_row_count",
                "evaluated_layout_count",
                "maximum_adaptive_improvement_bits",
                "fitted_tail_best_log2_rank_slope_per_n",
                "polynomial_selector_and_contraction_count",
                "general_adaptive_layout_no_go_theorem_count",
                "polynomial_relation_solver_count",
            ],
            dependencies=[
                "dcp_adaptive_layout_audit.py",
                "dcp_fiber_entanglement.py",
                "dcp_target_indexed_locality.py",
            ],
            next_actions=[
                "Delete valuation-only adaptive layout mechanisms.",
                "Search for polynomial additive-energy proxies whose selected cuts admit an all-n rank theorem.",
                "Reject selectors that call exponential residue-DP or fail to produce a verified relation."
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-SUBSET-SUM-RANDOM-SELF-REDUCTION",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Source-preserving random self-reduction for density-one subset sum",
            status="planned",
            hypothesis=(
                "A polynomial family of explicit shared-seed signed and odd-unit automorphisms of modular subset sum "
                "reaches a transformed presentation on which a deterministic partial solver has inverse-polynomial legal coverage."
            ),
            protocol=(
                "Prove exact witness, multiplicity, joint-source, and legal-conditioned-source preservation for "
                "A'_i=u(-1)^m_i A_i and t'=u(t-sum m_i A_i); certify that sign-only maps are centered-embedding "
                "isometries; then compare direct, sign-only, odd-unit, and signed-unit LLL under polynomial seed budgets "
                "using independent uniform targets and verified mapped-back witnesses."
            ),
            positive_signal=(
                "Odd-unit randomization has a held-out noncollapsing legal-input success rate and an average-case geometry "
                "theorem proving inverse-polynomial source coverage with polynomial reversible fixed-seed evaluation."
            ),
            falsifiers=[
                "A proposed transformation does not preserve every witness multiplicity or the joint uniform source.",
                "Apparent gains come only from sign/complement maps that are exact embedding isometries.",
                "Success appears only on planted targets or selected successful instances.",
                "Odd-unit rescues collapse in the scaling tail or lack a uniform coverage theorem.",
                "Random seeds are target dependent, measured, exponentially long, or not reversibly evaluable.",
            ],
            metrics=[
                "source_distribution_bijection_certificate_count",
                "all_target_multiplicity_certificate_count",
                "shared_seed_interface_certificate_count",
                "signed_embedding_isometry_certificate_count",
                "direct_legal_success_count",
                "sign_only_legal_success_count",
                "odd_unit_legal_success_count",
                "signed_odd_unit_legal_success_count",
                "odd_unit_rescue_count",
                "signed_odd_unit_rescue_count",
                "scaling_row_count",
                "tail_odd_unit_unconditional_success_count",
                "tail_signed_odd_unit_unconditional_success_hoeffding_lower_95pct",
                "proved_uniform_inverse_polynomial_legal_coverage_count",
                "source_contract_satisfying_row_count",
            ],
            dependencies=[
                "dcp_subset_sum_random_self_reduction.py",
                "dcp_coherent_matching_interface.py",
                "dcp_subset_sum_lattice_search.py",
                "dcp_subset_sum_target_distribution.py",
            ],
            next_actions=[
                "Fit held-out odd-unit orbit-hitting rates over larger n without planted-target substitution.",
                "Identify a source-invariant statistic that predicts transformed LLL success and admit an asymptotic proof.",
                "Synthesize non-isometric witness-preserving transformations only after exact soundness checks.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-ODD-UNIT-ORBIT-GEOMETRY",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Held-out odd-unit easy-orbit geometry search",
            status="planned",
            hypothesis=(
                "The odd-unit orbit contains an inverse-polynomial fraction of canonical modular embeddings with an "
                "efficiently recognizable geometric condition that forces deterministic LLL witness extraction."
            ),
            protocol=(
                "Sample independent uniform source instances and target-independent odd units; certify exact 2-adic orbit "
                "invariants and exponential orbit size; record normalized pre-LLL and post-LLL geometry; fit one threshold "
                "per fixed feature on even-index units and evaluate once on disjoint odd-index units."
            ),
            positive_signal=(
                "A pre-reduction rule has reproducible held-out enrichment, inverse-polynomial unconditional source "
                "prevalence, and an analytic theorem that the selected odd-unit embeddings are decoded by LLL."
            ),
            falsifiers=[
                "The putative mechanism changes only 2-adic valuations, which odd units preserve exactly.",
                "Enrichment appears only in training or only in post-reduction diagnostics.",
                "Selected-unit prevalence or conditional LLL success collapses with n.",
                "The rule is measured on planted targets or selected successful instances.",
                "Finite held-out enrichment is presented without an orbit-measure and LLL theorem.",
            ],
            metrics=[
                "invariant_certificate_count",
                "full_two_adic_invariant_certificate_count",
                "exact_exponential_orbit_certificate_count",
                "geometry_record_count",
                "verified_witness_count",
                "tail_verified_witness_count",
                "tail_unconditional_success_rate",
                "feature_rule_count",
                "heldout_positive_pre_reduction_rule_count",
                "maximum_heldout_pre_reduction_enrichment",
                "proved_inverse_polynomial_easy_orbit_measure_count",
                "proved_polynomial_partial_subset_sum_solver_count",
            ],
            dependencies=[
                "dcp_odd_unit_orbit_geometry.py",
                "dcp_subset_sum_random_self_reduction.py",
                "dcp_subset_sum_lattice_search.py",
            ],
            next_actions=[
                "Kill any surviving pre-reduction rule on larger held-out unit orbits.",
                "Derive an odd-part equidistribution or anti-concentration statement for a surviving feature.",
                "Prove selected-unit source prevalence and LLL witness extraction as separate lemmas.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-DCP-LIKELIHOOD-BRANCH-BOUND",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Exact nonlinear likelihood branch-and-bound",
            status="planned",
            hypothesis=(
                "Random-label DCP likelihoods admit rigorous interval upper bounds that prune the exponential frequency "
                "domain to poly(log N) candidates without chosen queries or an N-entry score table."
            ),
            protocol=(
                "Measure f=1-rate contaminated DCP records locally, maximize the exact correlation likelihood with a "
                "complete interval branch-and-bound using per-term Lipschitz caps, compare unique score evaluations to N, "
                "and fit their exponential scaling."
            ),
            positive_signal=(
                "Exact candidate evaluations and queue memory scale polynomially in n across a proved worst-frequency "
                "family while complete reflection recovery remains bounded-error."
            ),
            falsifiers=[
                "Random high-frequency terms saturate every broad interval bound.",
                "The decoder evaluates an exponential fraction of all candidates.",
                "Removing an N-entry score table only moves exponential work into interval search.",
                "A method-specific failure is overstated as a lower bound for all nonlinear decoders.",
            ],
            metrics=[
                "trial_count",
                "exact_decode_success_count",
                "mean_score_evaluation_fraction",
                "fitted_log2_evaluation_slope_per_n",
                "proved_polynomial_branch_bound_count",
                "proved_nonlinear_decoder_lower_bound_count",
            ],
            dependencies=[
                "dcp_likelihood_branch_bound.py",
                "dcp_iid_hash_estimator_audit.py",
                "dcp_hidden_number_bridge.py",
            ],
            next_actions=[
                "Search nonseparable global upper bounds for sparse trigonometric likelihoods.",
                "Test algebraic or lattice sketches that compress candidate intervals without selected labels.",
                "Retain the implemented result as method-specific unless a formal nonlinear lower bound is proved.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-FOURIER-COMPRESSIBILITY",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Sparse Fourier and derivative-spectrum dequantization sweep",
            status="planned",
            hypothesis="Viable hidden-shift phase families are not compressible by sparse Fourier or derivative-spectrum learners under legal access models.",
            protocol=(
                "Generate explicit phase families across increasing group sizes; compute full-table Fourier concentration, "
                "derivative spectra, sparse-recovery query estimates, and sample-budget legality."
            ),
            positive_signal="No polynomial-query evaluator or sample-limited sparse Fourier learner is certified while phase-state structure remains.",
            falsifiers=[
                "Base phase spectrum is poly-sparse.",
                "A derivative spectrum is poly-sparse with polynomial sparse-recovery query estimate.",
                "Sample budgets reach the estimated sparse-recovery threshold.",
            ],
            metrics=[
                "explicit_evaluator_sparse_recovery_count",
                "random_sample_sparse_recovery_count",
                "derivative_sparse_count",
                "spectrally_unresolved_count",
            ],
            dependencies=["fourier_compressibility_baselines.py", "phase_state_workbench.py"],
            next_actions=["Run qsearch.py fourier-learnability.", "Turn every sparse family into a negative result."],
        ),
        ExperimentRecord(
            id="EXP-DHS-QUERY-LOWER-BOUND-PROBES",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Hidden-shift query/time lower-bound fingerprint probes",
            status="planned",
            hypothesis=(
                "A hidden-shift family cannot be evidence for a Shor-level idea merely because sampled access is "
                "under-tested; polynomial sample fingerprints must be separated from polynomial-time decoding."
            ),
            protocol=(
                "For each explicit phase family and sample budget, draw shifted-oracle fingerprints, exhaustively count "
                "consistent shifts, estimate random-sample overlap scale, and classify query/time gaps versus true lower-bound debt."
            ),
            positive_signal="No positive signal is emitted; surviving rows become lower-bound obligations only.",
            falsifiers=[
                "Polynomially many samples uniquely fingerprint the shift when exhaustive candidate enumeration is allowed.",
                "Random-sample survival occurs below the collision/overlap scale.",
                "A claimed coherent-oracle advantage lacks a reduction to a natural input model with reversible costs counted.",
            ],
            metrics=[
                "poly_sample_fingerprint_unique_count",
                "overlap_scale_collision_count",
                "undersampled_gap_count",
                "positive_evidence_count",
            ],
            dependencies=["hidden_shift_query_lower_bounds.py", "phase_state_workbench.py"],
            next_actions=[
                "Run qsearch.py query-lower-bounds.",
                "Use query/time-gap rows to drive lower-bound proofs or decoder mutations.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-CHARACTER-SHIFT-BASELINE",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Multiplicative-character shift sample/elimination baseline",
            status="planned",
            hypothesis=(
                "Legendre and quartic-character hidden shifts may survive sparse-spectrum checks, but any claimed "
                "advantage must separate query information from exponential candidate enumeration."
            ),
            protocol=(
                "Generate multiplicative-character hidden-shift samples, filter all candidate shifts, track candidate-set "
                "entropy, and classify whether sample-efficient identification still relies on domain-size enumeration."
            ),
            positive_signal="No polynomial-time non-exhaustive decoder is found while query/sample lower-bound obligations remain explicit.",
            falsifiers=[
                "Polynomially many samples plus a non-exhaustive decoder recover the shift.",
                "The claimed advantage is only query complexity while classical samples already isolate the shift.",
                "Full-table correlation is treated as unavailable without a formal access-model reason.",
            ],
            metrics=[
                "poly_sample_unique_count",
                "exhaustive_decoding_only_count",
                "insufficient_sample_count",
                "full_table_correlation_success_count",
            ],
            dependencies=["character_shift_baselines.py", "phase_state_workbench.py"],
            next_actions=["Run qsearch.py character-shift.", "Search for non-exhaustive algebraic decoders or prove lower bounds."],
        ),
        ExperimentRecord(
            id="EXP-DHS-CHARACTER-DECODER-SEARCH",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Non-exhaustive decoder search for character hidden shifts",
            status="planned",
            hypothesis=(
                "Multiplicative-character shifts remain a query/time gap only if natural non-exhaustive decoders fail "
                "while exhaustive candidate-scoring baselines are clearly labelled."
            ),
            protocol=(
                "Run shift-invariant statistic probes, phase-frequency decoders, and exhaustive low-moment signature "
                "scoring on Legendre/quartic hidden-shift samples; classify every success by time model."
            ),
            positive_signal="No non-exhaustive decoder succeeds, and the remaining gap is turned into a formal lower-bound obligation.",
            falsifiers=[
                "A non-exhaustive decoder recovers shifts at tested budgets.",
                "Exhaustive candidate scoring is reported as a polynomial-time dequantization.",
                "Shift-invariant statistics are mistaken for shift information.",
            ],
            metrics=[
                "non_exhaustive_success_count",
                "exhaustive_decoder_success_count",
                "shift_invariant_obstruction_count",
                "domain_linear_attempt_count",
            ],
            dependencies=["character_decoder_search.py", "character_shift_baselines.py", "phase_state_workbench.py"],
            next_actions=["Run qsearch.py character-decoders.", "Promote only lower-bound obligations, not positive evidence."],
        ),
        ExperimentRecord(
            id="EXP-DHS-CHARACTER-LOWER-BOUND",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Multiplicative-character decoding lower-bound ledger",
            status="planned",
            hypothesis=(
                "Legendre/quartic rows are useful only as explicit decoding lower-bound obligations: polynomial samples "
                "may fingerprint shifts, while known decoders remain candidate-set or full-degree in p."
            ),
            protocol=(
                "Compare random-sample fingerprints, adaptive chosen-query fingerprints, full-degree cyclotomic GCD recovery, "
                "and candidate-enumeration operations across increasing primes."
            ),
            positive_signal="No positive signal is emitted; the output is a falsifier/proof-debt ledger for the character-shift frontier.",
            falsifiers=[
                "A polynomial-style decoder recovers shifts from comparable samples.",
                "The full-degree cyclotomic constraints compress to poly(log p) degree.",
                "Chosen-query fingerprints are reported as speedup evidence instead of decoding lower-bound debt.",
            ],
            metrics=[
                "sample_fingerprint_count",
                "chosen_query_fingerprint_count",
                "full_degree_gcd_success_count",
                "max_gcd_operation_exponent_per_bit",
            ],
            dependencies=["character_shift_lower_bound.py", "character_decoder_search.py", "hidden_shift_query_lower_bounds.py"],
            next_actions=["Run qsearch.py character-lower-bound.", "Use output to state or falsify a formal decoding lower bound."],
        ),
        ExperimentRecord(
            id="EXP-DHS-CHARACTER-QUERY-INFORMATION",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Multiplicative-character information-theoretic query ceiling",
            status="planned",
            hypothesis=(
                "Legendre/quartic character shifts cannot support a large query-complexity separation if pairwise "
                "agreement profiles give logarithmic random-sample fingerprints."
            ),
            protocol=(
                "Compute exact pairwise agreement counts for every nonzero shift difference, use a union bound to "
                "derive random-sample query ceilings for unique fingerprinting, and separate query information from decoding time."
            ),
            positive_signal="No positive speedup signal is emitted; this experiment kills or weakens query-lower-bound claims.",
            falsifiers=[
                "Distinct shifts have constant disagreement, yielding O(log p) random-sample fingerprints.",
                "The remaining claim is computational decoding time rather than query complexity.",
                "Candidate enumeration is mistaken for a polynomial-time decoder.",
            ],
            metrics=[
                "query_lower_bound_killed_count",
                "max_union_bound_queries",
                "max_query_ceiling_over_log2_prime",
                "max_wrong_shift_agreement_fraction",
            ],
            dependencies=["character_query_information.py", "phase_state_workbench.py"],
            next_actions=["Run qsearch.py character-query-info.", "Reclassify any surviving character frontier as decoding-time lower-bound debt."],
        ),
        ExperimentRecord(
            id="EXP-DHS-CHARACTER-MOMENT-OBSTRUCTION",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Multiplicative-character low-degree moment obstruction",
            status="planned",
            hypothesis=(
                "Low-degree full-domain moment regression cannot decode multiplicative-character shifts before the first "
                "nonzero character moment, which appears at degree growing with p."
            ),
            protocol=(
                "Compute exact finite-field character moments for Legendre and quartic families, record the first nonzero "
                "degree, and classify which low-degree moment windows vanish."
            ),
            positive_signal="No positive speedup signal is emitted; this only blocks one classical decoder class.",
            falsifiers=[
                "A low-degree moment appears inside the tested window.",
                "Sampled/adaptive decoders bypass the full-domain moment obstruction.",
                "The obstruction is used as a general lower bound instead of a narrow decoder-class result.",
            ],
            metrics=[
                "low_degree_moment_obstruction_count",
                "moment_signal_found_count",
                "max_first_nonzero_degree",
                "positive_evidence_count",
            ],
            dependencies=["character_moment_obstruction.py", "phase_state_workbench.py"],
            next_actions=["Run qsearch.py character-moments.", "Use output only as a narrow lower-bound lemma candidate."],
        ),
        ExperimentRecord(
            id="EXP-DHS-CHARACTER-COMPLEXITY-PREPROCESSING",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Shifted-character complexity, preprocessing, and reduction audit",
            status="planned",
            hypothesis=(
                "The surviving Legendre/quartic evidence is at most a uniform single-instance decoding gap; it is not "
                "query evidence and cannot support a major speedup claim without a natural reduction or named assumption."
            ),
            protocol=(
                "Record literature-backed classical query/time upper bounds, build fixed chosen-query signature tables "
                "for every public modulus, separate preprocessing/advice from online cost, and audit whether any uniform "
                "polylog decoder, unconditional lower bound, or natural-problem reduction is actually known."
            ),
            positive_signal=(
                "No positive speedup signal is emitted. Progress requires a model-preserving natural reduction, a named "
                "hardness assumption, or a uniform decoder/lower-bound theorem that changes the classification."
            ),
            falsifiers=[
                "Known classical hidden-shifted-power recovery already uses logarithmically many queries.",
                "Fixed-prefix online decoding succeeds after modulus-dependent domain-size preprocessing/advice.",
                "No unconditional superpolynomial decoding lower bound is known.",
                "No reduction to a major natural problem is recorded.",
            ],
            metrics=[
                "fixed_prefix_decode_success_count",
                "logarithmic_query_domain_time_upper_bound_count",
                "max_unique_prefix_over_n_bits",
                "max_preprocessing_operation_exponent_per_bit",
                "uniform_polylog_classical_decoder_count",
                "unconditional_superpolynomial_lower_bound_count",
                "natural_problem_reduction_count",
            ],
            dependencies=[
                "character_shift_complexity.py",
                "phase_state_workbench.py",
                "van-dam-hallgren-shifted-character-2000",
                "ip-shift-deconvolution-2002",
                "bourgain-hidden-shifted-power-2011",
            ],
            next_actions=[
                "Run qsearch.py character-complexity.",
                "Either formalize a uniform no-preprocessing hardness assumption and natural reduction or retire this frontier.",
            ],
        ),
        ExperimentRecord(
            id="EXP-DHS-PHASE-NATURALNESS",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Phase-family naturalness and description-complexity audit",
            status="planned",
            hypothesis="Hidden-shift evidence must come from natural algebraic or reduction-backed families, not hash-masked pseudo-hard controls.",
            protocol="Audit phase-family descriptions and parameters for active masks, noise, pseudorandom tables, unsupported generators, and reduction hints.",
            positive_signal="No artificial hash/mask/noise family is used as positive evidence.",
            falsifiers=[
                "A surviving family is hard only because of a hash mask or pseudorandom noise.",
                "A family lacks named algebraic structure or a natural problem interpretation.",
                "Naturalness failures are counted as positive hidden-shift evidence.",
            ],
            metrics=[
                "artificial_record_count",
                "unsupported_record_count",
                "natural_algebraic_record_count",
                "positive_evidence_record_count",
            ],
            dependencies=["phase_family_naturalness.py", "phase_family_triage.py"],
            next_actions=["Run qsearch.py phase-naturalness.", "Reject artificial families in phase-family triage."],
        ),
        ExperimentRecord(
            id="EXP-DHS-TRACE-FUNCTION-SEARCH",
            candidate_id="DHS-GOWERS-SIEVE",
            title="Natural finite-field trace-function hidden-shift search",
            status="planned",
            hypothesis="Rational finite-field trace functions may provide natural phase families that survive low-degree, sparse-spectrum, and sampled baselines.",
            protocol="Enumerate Kloosterman/two-pole/cubic rational trace phases over growing prime fields and attack each row immediately.",
            positive_signal="A natural trace row survives sampled candidate elimination, sparse spectra, and low-degree tests without being counted as evidence before lower bounds.",
            falsifiers=[
                "Sampled candidate elimination recovers shifts.",
                "Sparse Fourier or derivative spectra explain the signal.",
                "Finite-difference tests certify low-degree structure.",
            ],
            metrics=[
                "sample_elimination_rejected_count",
                "sparse_spectrum_rejected_count",
                "low_degree_rejected_count",
                "unresolved_count",
            ],
            dependencies=["trace_function_search.py", "phase_state_workbench.py"],
            next_actions=["Run qsearch.py trace-functions.", "Keep survivors as lower-bound obligations only."],
        ),
        ExperimentRecord(
            id="EXP-CODE-COSET-RANK",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Coset-state relation rank sweep for code equivalence",
            status="planned",
            hypothesis="Hard code-equivalence families retain low-complexity relation signals across hidden permutations.",
            protocol="Generate code families, build equality-relation fingerprints for hidden permutations, and track rank/overlap scaling.",
            positive_signal="Relation rank and distinguishability grow with instance count while classical tools fail.",
            falsifiers=["Max pairwise overlap stays above 0.9.", "Rank saturates at a constant.", "Classical canonicalization solves the family."],
            metrics=["relation_rank", "max_pairwise_overlap", "classical_solver_success", "automorphism_group_size"],
            dependencies=["code family generator", "coset fingerprint metrics"],
            next_actions=["Add small binary linear-code generator.", "Integrate classical canonicalization baseline."],
        ),
        ExperimentRecord(
            id="EXP-CODE-STRUCTURAL-INVARIANTS",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Structural invariant baseline for code equivalence",
            status="planned",
            hypothesis=(
                "Any credible code-equivalence coset candidate must first survive support-splitting, dual/hull, "
                "puncturing, and shortening invariants before canonicalization or quantum observable search is relevant."
            ),
            protocol=(
                "Audit seed and generated code pairs with codeword weight enumerators, dual-code weight enumerators, "
                "hull dimension, support-splitting coordinate fingerprints, punctured-code profiles, and shortened-code profiles."
            ),
            positive_signal="No positive signal; structural separations are dequantization evidence and survivors are proof debt.",
            falsifiers=[
                "Support-splitting fingerprints distinguish the row.",
                "Dual weight enumerator or hull dimension distinguishes the row.",
                "Punctured or shortened code profiles distinguish the row.",
                "Structural-invariant survival is promoted without tuple-profile, automorphism, canonicalization, and lower-bound checks.",
            ],
            metrics=[
                "structural_rejection_count",
                "support_splitting_rejection_count",
                "dual_rejection_count",
                "puncture_shorten_rejection_count",
                "proof_debt_count",
            ],
            dependencies=["code_structural_invariants.py", "code_family_search.py", "code_canonicalization_baseline.py"],
            next_actions=[
                "Run qsearch.py code-invariants.",
                "Reject structurally separated rows before collective-observable search.",
                "Route only survivors into tuple-profile and automorphism-aware canonicalization baselines.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-INFORMATION-SET-CANONICALIZATION",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Information-set canonicalization baseline for code equivalence",
            status="planned",
            hypothesis=(
                "Rows that survive structural invariants still should not be treated as code-coset evidence if "
                "information-set systematic forms give different canonical signatures."
            ),
            protocol=(
                "Enumerate independent ordered information sets under a cap, transform each generator to systematic "
                "form, canonicalize the suffix-column multiset, and compare the minimal signatures between code pairs."
            ),
            positive_signal="No positive signal; signature differences are dequantization evidence and matches remain proof debt.",
            falsifiers=[
                "Information-set canonical signatures differ.",
                "Enumeration exceeds the cap and is promoted without a lower-bound argument.",
                "Signature equality is treated as equivalence or hardness without automorphism-aware canonicalization.",
            ],
            metrics=[
                "information_set_rejection_count",
                "equivalent_control_count",
                "survivor_proof_debt_count",
                "cap_proof_debt_count",
                "max_ordered_information_sets_evaluated",
            ],
            dependencies=["code_information_set_baseline.py", "code_canonicalization_baseline.py"],
            next_actions=[
                "Run qsearch.py code-info-sets.",
                "Reject rows separated by information-set canonicalization.",
                "Route only survivors into automorphism-aware canonicalization and lower-bound tracking.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-CANONICALIZATION-BASELINE",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Profile-pruned code canonicalization baseline",
            status="planned",
            hypothesis=(
                "Any credible code-equivalence coset candidate must survive support-splitting-style coordinate "
                "profiles and exact canonical forms whenever profile buckets are small."
            ),
            protocol=(
                "Build coordinate refinement profiles from codeword supports, enumerate profile-compatible coordinate "
                "assignments under a cap, compare exact canonical forms, and record unresolved buckets as proof debt."
            ),
            positive_signal="No positive signal; canonicalization failures only define harder rows to attack next.",
            falsifiers=[
                "Coordinate profile partitions differ.",
                "Profile-pruned canonical forms differ.",
                "A weak-invariant collision is promoted before canonicalization baselines run.",
                "Large unresolved coordinate buckets are counted as quantum evidence instead of proof debt.",
            ],
            metrics=[
                "profile_rejection_count",
                "canonical_form_rejection_count",
                "canonical_equivalent_count",
                "proof_debt_count",
                "max_estimated_assignments",
            ],
            dependencies=["code_canonicalization_baseline.py", "code_family_search.py", "code_equivalence_workbench.py"],
            next_actions=[
                "Run qsearch.py code-canonicalize.",
                "Mutate code-family generators only toward rows that survive this baseline.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-HARD-FAMILY-SEARCH",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Code-equivalence weak-collision hard-family search",
            status="planned",
            hypothesis="A useful code-equivalence frontier family should fool weak invariants and survive support-splitting, dual/hull, puncturing, shortening, and canonicalization baselines.",
            protocol=(
                "Randomly generate full-rank binary linear codes across fixed scaling budgets; retain pairs with matching weak invariants, "
                "then reject them when stronger classical code invariants or bounded exact search separate them."
            ),
            positive_signal="A generated family survives all implemented classical invariant baselines and is promoted only as proof debt.",
            falsifiers=[
                "Weak-invariant collisions are separated by support-splitting or puncturing/shortening profiles.",
                "Dual weight enumerators or hull dimension distinguish the pair.",
                "Bounded exact search resolves the small instance before a scalable pattern appears.",
            ],
            metrics=[
                "collision_found_count",
                "strong_invariant_rejection_count",
                "bounded_exact_rejection_count",
                "hard_family_candidate_count",
            ],
            dependencies=["code_family_search.py", "code_equivalence_workbench.py"],
            next_actions=[
                "Run qsearch.py code-family-search.",
                "Add algebraic family generators only after random weak collisions are not immediately dequantized.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-PROFILE-COLLISION-SEARCH",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Coordinate-profile collision search for code equivalence",
            status="planned",
            hypothesis=(
                "A harder code-equivalence generator should collide support-splitting-style coordinate profiles before "
                "it is worth testing any quantum coset observable."
            ),
            protocol=(
                "Randomly generate full-rank binary linear codes, bucket them by full coordinate-refinement profile multisets, "
                "and attack every profile collision with profile-pruned canonicalization."
            ),
            positive_signal="Only a non-equivalent profile collision that survives canonicalization becomes proof debt; equivalent collisions are controls.",
            falsifiers=[
                "All profile collisions are equivalent controls.",
                "Non-equivalent profile collisions are rejected by canonicalization.",
                "No profile collision appears under deterministic search budgets.",
            ],
            metrics=[
                "profile_collision_count",
                "equivalent_collision_count",
                "rejected_collision_count",
                "proof_debt_collision_count",
            ],
            dependencies=["code_profile_collision_search.py", "code_canonicalization_baseline.py", "code_family_search.py"],
            next_actions=[
                "Run qsearch.py code-profile-search.",
                "Use any proof-debt survivor as the only acceptable input to later code-coset observable search.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-TUPLE-PROFILE-BASELINE",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Higher-order coordinate tuple-profile code baseline",
            status="planned",
            hypothesis=(
                "Code-equivalence rows should survive 2- and 3-coordinate puncturing/shortening-style tuple profiles "
                "before they motivate any nonabelian coset observable."
            ),
            protocol=(
                "For each code pair, enumerate coordinate tuples, compute residual weight profiles conditioned on tuple "
                "patterns, compare profile multisets, and search random code families for 2-coordinate tuple-profile "
                "collisions before applying canonicalization."
            ),
            positive_signal=(
                "Only a non-equivalent tuple-profile collision that survives profile-pruned canonicalization becomes "
                "proof debt; tuple-profile separations and equivalent collisions are negative evidence."
            ),
            falsifiers=[
                "Higher-order coordinate tuple profiles separate the pair.",
                "Tuple-profile collisions are equivalent controls.",
                "Tuple-profile collisions are rejected by canonicalization.",
                "No nontrivial tuple-profile collision appears under deterministic search budgets.",
            ],
            metrics=[
                "tuple_profile_rejection_count",
                "tuple_profile_survivor_count",
                "tuple_collision_count",
                "tuple_collision_rejected_count",
                "tuple_collision_proof_debt_count",
            ],
            dependencies=["code_tuple_profile_baseline.py", "code_canonicalization_baseline.py", "code_family_search.py"],
            next_actions=[
                "Run qsearch.py code-tuple-profiles.",
                "Use tuple-profile survivors only as proof debt for stronger automorphism and canonicalization baselines.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-LOW-WEIGHT-MATROID-BASELINE",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Low-weight support matroid baseline for code equivalence",
            status="planned",
            hypothesis=(
                "A code-equivalence coset frontier row must survive classical low-weight codeword support "
                "hypergraph and matroid-style invariants before collective quantum measurement design is relevant."
            ),
            protocol=(
                "Enumerate low-weight codeword supports under a codeword cap, compare minimum distance, "
                "low-weight spectra, coordinate/pair support profiles, and 1-WL incidence signatures of the "
                "coordinate/support hypergraph across code pairs; for small matching rows, run exact colored "
                "incidence-graph isomorphism and import external automorphism/canonicalization control certificates."
            ),
            positive_signal="No positive signal; separations are dequantization evidence and matches are proof debt or controls.",
            falsifiers=[
                "Minimum distance or low-weight support spectrum differs.",
                "Coordinate or coordinate-pair low-weight support profiles differ.",
                "The low-weight support incidence WL signature differs.",
                "Exact low-weight incidence-graph isomorphism rejects the row.",
                "A matching low-weight signature is promoted without information-set, canonicalization, automorphism, and lower-bound checks.",
            ],
            metrics=[
                "low_weight_rejection_count",
                "equivalent_control_count",
                "survivor_proof_debt_count",
                "cap_proof_debt_count",
                "incidence_wl_rejection_count",
                "incidence_isomorphism_rejection_count",
                "incidence_isomorphism_match_count",
                "incidence_isomorphism_cap_count",
            ],
            dependencies=[
                "code_low_weight_structure.py",
                "code_family_search.py",
                "quasi_cyclic_code_search.py",
                "cyclic_code_search.py",
                "goppa_code_search.py",
                "tanner_code_search.py",
            ],
            next_actions=[
                "Run qsearch.py code-low-weight.",
                "Reject rows separated by low-weight support structure.",
                "Treat rows certified by cyclic, quasi-cyclic, semilinear, Tanner, information-set, or canonicalization controls as controls.",
                "Route only survivors into stronger canonicalization, automorphism, and reduction/lower-bound tracking.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-QUASI-CYCLIC-SEARCH",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Quasi-cyclic code-family tuple-profile search",
            status="planned",
            hypothesis=(
                "Structured quasi-cyclic code families are a more credible source of code-equivalence frontier rows "
                "than random weak-invariant collisions, but they must still collide tuple profiles and survive canonicalization."
            ),
            protocol=(
                "Generate systematic binary quasi-cyclic codes from circulant blocks, bucket them by 2-coordinate tuple profiles, "
                "and attack every nontrivial collision with higher-order tuple profiles and profile-pruned canonicalization."
            ),
            positive_signal=(
                "Only a non-equivalent quasi-cyclic tuple-profile collision that survives canonicalization becomes proof debt. "
                "Equivalent controls, canonicalization rejections, and no-collision searches are blocker evidence."
            ),
            falsifiers=[
                "No nontrivial tuple-profile collision appears under deterministic quasi-cyclic budgets.",
                "Quasi-cyclic tuple-profile collisions are equivalent controls.",
                "Quasi-cyclic tuple-profile collisions are rejected by canonicalization.",
            ],
            metrics=[
                "tuple_collision_count",
                "equivalent_collision_count",
                "rejected_collision_count",
                "proof_debt_collision_count",
                "no_collision_count",
            ],
            dependencies=["quasi_cyclic_code_search.py", "code_tuple_profile_baseline.py", "code_canonicalization_baseline.py"],
            next_actions=[
                "Run qsearch.py code-qc-search.",
                "Escalate only proof-debt rows into observable search; otherwise mutate the algebraic family generator.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Quasi-cyclic automorphism canonicalization baseline",
            status="planned",
            hypothesis=(
                "Quasi-cyclic tuple-profile proof-debt rows should be rejected as controls if they are equivalent under "
                "natural block permutations and cyclic shifts."
            ),
            protocol=(
                "Read quasi-cyclic tuple-profile collision rows, enumerate the block-permutation/cyclic-shift automorphism group "
                "under a cap, compute canonical codeword-set forms, and classify equivalent controls separately from unresolved proof debt."
            ),
            positive_signal=(
                "No positive signal; QC-equivalent rows are negative controls, and non-equivalence inside the restricted group remains "
                "proof debt for stronger canonicalization."
            ),
            falsifiers=[
                "A tuple-profile collision is equivalent under the quasi-cyclic automorphism group.",
                "QC automorphism enumeration exceeds the cap.",
                "Restricted no-equivalence is promoted as full non-equivalence without stronger canonicalization.",
            ],
            metrics=[
                "record_count",
                "evaluated_count",
                "equivalent_control_count",
                "qc_no_equivalence_proof_debt_count",
                "canonicalization_cap_proof_debt_count",
            ],
            dependencies=["quasi_cyclic_canonicalization.py", "quasi_cyclic_code_search.py"],
            next_actions=[
                "Run qsearch.py code-qc-canonicalize.",
                "Only unresolved rows should feed a stronger canonical labeling or automorphism-group baseline.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-QC-INFORMATION-SET-RESOLVER",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Quasi-cyclic proof-debt information-set resolver",
            status="planned",
            hypothesis=(
                "Rows that survive quasi-cyclic automorphism checks may still collapse under exact ordered "
                "information-set canonicalization, so QC automorphism non-equivalence must not be treated as full "
                "code non-equivalence."
            ),
            protocol=(
                "Read quasi-cyclic collision rows left as proof debt by the QC automorphism audit, run exact ordered "
                "information-set canonicalization under a high but explicit cap, and classify equal canonical forms as "
                "equivalent controls, unequal forms as classical rejections, and cap exits as proof debt."
            ),
            positive_signal=(
                "No positive signal; only a row that exceeds exact information-set resolution remains proof debt for "
                "stronger canonical labeling or lower-bound work."
            ),
            falsifiers=[
                "Information-set canonical forms match, proving an equivalent-control row.",
                "Information-set canonical forms differ, giving a classical rejection.",
                "The row exceeds the cap and remains proof debt rather than evidence.",
            ],
            metrics=[
                "record_count",
                "evaluated_count",
                "equivalent_control_count",
                "information_set_rejection_count",
                "proof_debt_count",
            ],
            dependencies=["qc_information_set_resolver.py", "quasi_cyclic_code_search.py", "quasi_cyclic_canonicalization.py"],
            next_actions=[
                "Run qsearch.py code-qc-info-resolve after qsearch.py code-qc-canonicalize.",
                "Feed resolved QC rows into qsearch.py code-triage.",
                "Do not use QC automorphism non-equivalence as full code non-equivalence evidence.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-CYCLIC-ALGEBRAIC-SEARCH",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Binary cyclic-code algebraic family search",
            status="planned",
            hypothesis=(
                "Binary cyclic codes are a natural algebraic source of code-equivalence rows, but tuple-profile "
                "collisions must survive structural invariants, cyclic dihedral/multiplier automorphism groups, and "
                "canonicalization before they can motivate nonabelian coset measurements."
            ),
            protocol=(
                "Enumerate cyclic codes from divisors of x^n - 1 over F_2 for small length windows, bucket by "
                "coordinate tuple profiles, audit every nontrivial collision with structural invariants, higher tuple "
                "profiles, dihedral rotation/reversal equivalence, multiplier-affine automorphisms, and profile-pruned canonicalization."
            ),
            positive_signal=(
                "No positive signal; only a non-dihedral, non-rejected collision that survives canonicalization as "
                "proof debt can feed later code-coset observable design."
            ),
            falsifiers=[
                "A cyclic-code collision is an equivalent control under coordinate rotations, reversal, or multiplier automorphisms.",
                "Structural invariants or higher tuple profiles separate the collision.",
                "Profile-pruned canonicalization proves equivalence or rejects the row.",
                "Cyclic algebraic structure is promoted without automorphism accounting.",
            ],
            metrics=[
                "code_count",
                "tuple_collision_count",
                "dihedral_equivalent_count",
                "multiplier_equivalent_count",
                "canonicalization_rejection_count",
                "proof_debt_collision_count",
            ],
            dependencies=["cyclic_code_search.py", "code_tuple_profile_baseline.py", "code_canonicalization_baseline.py"],
            next_actions=[
                "Run qsearch.py code-cyclic-search.",
                "Feed cyclic-code rows into qsearch.py code-triage.",
                "Treat reciprocal/dihedral/multiplier cyclic collisions as negative controls, not hardness evidence.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-BCH-ALGEBRAIC-SEARCH",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Primitive BCH algebraic code-family search",
            status="planned",
            hypothesis=(
                "Primitive BCH codes are a natural algebraic code-equivalence source with cyclotomic structure, but "
                "any tuple-profile or coarse algebraic-profile signal must survive defining-set decimation controls, "
                "low-weight matroid baselines, and scalable canonicalization before motivating nonabelian coset measurements."
            ),
            protocol=(
                "Generate primitive binary BCH codes from GF(2^m) cyclotomic cosets and minimal polynomials, vary "
                "designed distance and starting roots, bucket rows by exact tuple profiles when dimensions are small "
                "and by explicit algebraic profiles when dimensions are too large for codeword enumeration, then audit "
                "collisions with cyclotomic decimation, structural invariants, low-weight support structure, and canonicalization."
            ),
            positive_signal=(
                "No positive signal; only a BCH row that is not a duplicate defining set, not decimation-equivalent, "
                "and not rejected by code baselines may remain proof debt for scalable canonical labeling or lower-bound work."
            ),
            falsifiers=[
                "A BCH defining interval closes to a duplicate cyclotomic defining set.",
                "A BCH collision is explained by a unit decimation/multiplier of defining sets.",
                "Structural, tuple-profile, low-weight, or canonical baselines separate the row.",
                "A high-dimensional BCH row is promoted without scalable canonicalization or lower-bound proof debt.",
            ],
            metrics=[
                "generated_code_count",
                "duplicate_code_count",
                "tuple_collision_count",
                "multiplier_equivalent_count",
                "low_weight_rejection_count",
                "dual_rejection_count",
                "dual_higher_tuple_rejection_count",
                "proof_debt_collision_count",
            ],
            dependencies=[
                "bch_code_search.py",
                "cyclic_code_search.py",
                "code_tuple_profile_baseline.py",
                "code_low_weight_structure.py",
                "code_canonicalization_baseline.py",
            ],
            next_actions=[
                "Run qsearch.py code-bch-search.",
                "Feed BCH rows into qsearch.py code-low-weight and qsearch.py code-triage.",
                "Resolve high-dimensional BCH proof debt using parity-check-side invariants or scalable defining-set canonicalization before observable design.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-GOPPA-ALGEBRAIC-SEARCH",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Binary Goppa/alternant algebraic family search",
            status="planned",
            hypothesis=(
                "Binary Goppa and alternant-style codes are natural algebraic code-equivalence sources, but any "
                "small tuple-profile signal must survive structural invariants, semilinear field automorphism controls, "
                "and canonicalization before it can motivate nonabelian coset measurements."
            ),
            protocol=(
                "Generate small binary Goppa codes over GF(2^m) from rootless monic generator polynomials, convert "
                "field parity checks to binary generator matrices, bucket by coordinate tuple profiles, and audit every "
                "collision with structural invariants, higher tuple profiles, full-support affine semilinear field "
                "permutations, and profile-pruned canonicalization."
            ),
            positive_signal=(
                "No positive signal; only a non-semilinear, non-rejected Goppa row that survives canonicalization as "
                "proof debt can feed later code-coset observable design."
            ),
            falsifiers=[
                "A Goppa collision is explained by an affine semilinear field permutation.",
                "Structural invariants or tuple profiles separate the collision.",
                "Profile-pruned canonicalization proves equivalence or rejects the row.",
                "Small algebraic-code coincidences are promoted without automorphism accounting.",
            ],
            metrics=[
                "code_count",
                "tuple_collision_count",
                "semilinear_control_count",
                "canonicalization_rejection_count",
                "proof_debt_collision_count",
            ],
            dependencies=["goppa_code_search.py", "code_tuple_profile_baseline.py", "code_canonicalization_baseline.py"],
            next_actions=[
                "Run qsearch.py code-goppa-search.",
                "Feed Goppa rows into qsearch.py code-triage.",
                "Treat semilinear Goppa collisions as negative controls, not hardness evidence.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-GOPPA-SCALING-FRONTIER",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Scalable punctured Goppa/alternant classical frontier",
            status="planned",
            hypothesis=(
                "Natural Goppa/alternant code-equivalence rows must survive scalable exact dual, hull, Schur-square, "
                "incidence, and semilinear-support baselines before they can motivate nonabelian coset measurements."
            ),
            protocol=(
                "Generate punctured rootless binary Goppa/alternant codes over GF(2^m) through length 160; compute "
                "rank, hull, primal/dual Schur squares, exact dual weight and minimum-word incidence signatures where "
                "dimension permits, verify coordinate-permutation controls, and audit matching rows under affine-semilinear support maps."
            ),
            positive_signal=(
                "No positive quantum signal. A row may remain classical proof debt only after every exact scalable "
                "signature and complete support-orbit check agrees; enumeration caps are never hardness evidence."
            ),
            falsifiers=[
                "A known coordinate permutation fails to preserve the exact signature.",
                "Exact dual weight/incidence, hull, or Schur-square data separates the pair.",
                "An affine-semilinear support map explains the pair as a control candidate.",
                "A cap-limited or sampled calculation is promoted as exact non-equivalence or quantum evidence.",
            ],
            metrics=[
                "instance_count",
                "maximum_length",
                "exact_dual_signature_count",
                "exact_invariant_rejection_count",
                "proof_debt_pair_count",
                "baseline_cap_pair_count",
            ],
            dependencies=[
                "goppa_scaling_frontier.py",
                "goppa_code_search.py",
                "code_schur_filtration.py",
                "code_frontier_triage.py",
            ],
            next_actions=[
                "Run qsearch.py code-goppa-scaling.",
                "Feed family-level statuses into qsearch.py code-triage.",
                "Resolve cap rows using scalable dual-code signatures and support recovery before any observable design.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-GOPPA-SYZYGY-FRONTIER",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Exact dual Goppa syzygy frontier",
            status="planned",
            hypothesis=(
                "Scalable Goppa code-equivalence rows must survive exact low-degree Betti invariants of the dual "
                "projective system and complete coordinate-shortening profiles before they can remain classical proof debt."
            ),
            protocol=(
                "Compute the exact quadratic relation dimension beta_1,2 and linear syzygy dimension beta_2,3 over "
                "GF(2) with bit-packed elimination for every scalable Goppa instance; compute complete histograms over "
                "all single-coordinate shortenings for unresolved pairs; verify coordinate-permutation controls and reject exact mismatches."
            ),
            positive_signal=(
                "No positive quantum signal. A complete Betti collision remains proof debt for deeper shortening, "
                "support recovery, and canonicalization; it does not establish code-equivalence hardness."
            ),
            falsifiers=[
                "A whole-code beta_1,2 or beta_2,3 invariant differs.",
                "A complete single-coordinate-shortening Betti histogram differs.",
                "A known coordinate permutation fails to preserve the exact signature.",
                "An incomplete profile or invariant collision is promoted as a hardness or speedup signal.",
                "A family distinguisher is mistaken for a code-equivalence solver.",
            ],
            metrics=[
                "exact_whole_syzygy_signature_count",
                "complete_shortening_profile_count",
                "evaluated_shortening_count",
                "exact_syzygy_rejection_count",
                "exact_syzygy_collision_count",
                "shortening_cap_pair_count",
            ],
            dependencies=[
                "code_syzygy_invariants.py",
                "goppa_syzygy_frontier.py",
                "goppa_scaling_frontier.py",
                "mora-tillich-dual-goppa-square-2021",
                "bardet-high-rate-alternant-2023",
                "randriambololona-syzygy-distinguisher-2024",
            ],
            next_actions=[
                "Run qsearch.py code-goppa-syzygies.",
                "Feed exact pair decisions into qsearch.py code-triage.",
                "Escalate complete collisions to deeper shortening and support-recovery attacks, never to measurement design directly.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-GOPPA-HULL-PROJECTOR",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Scalable Goppa trivial-hull projector reduction",
            status="planned",
            hypothesis=(
                "Public-generator Goppa rows with trivial Euclidean hull are not code-native hard instances: the "
                "basis-independent projector reduces their permutation equivalence exactly to colored graph isomorphism."
            ),
            protocol=(
                "For every scalable Goppa frontier pair, certify hull dimension and the symmetric idempotent projector; "
                "compute loop, degree, and fixed-round WL graph invariants; reject polynomial mismatches; run bounded "
                "exact graph matching only on collisions; and verify recovered mappings on complete code row spaces."
            ),
            positive_signal=(
                "No direct quantum signal. A projector collision only transfers the row to graph-isomorphism proof debt; "
                "a mismatch or verified mapping removes it from the code-native frontier."
            ),
            falsifiers=[
                "A trivial-hull projector invariant separates the pair in polynomial time.",
                "Exact projector graphs are nonisomorphic.",
                "A recovered graph mapping verifies code equivalence.",
                "The direct theorem is applied despite a singular Gram matrix.",
                "A graph-matcher timeout or WL collision is promoted as a lower bound.",
            ],
            metrics=[
                "trivial_hull_certificate_count",
                "frontier_pair_count",
                "polynomial_projector_rejection_count",
                "exact_graph_rejection_count",
                "equivalent_or_automorphic_count",
                "projector_proof_debt_count",
            ],
            dependencies=[
                "goppa_hull_projector_frontier.py",
                "code_hull_projector_reduction.py",
                "goppa_scaling_frontier.py",
                "bardet-otmani-saeed-trivial-hull-2019",
            ],
            next_actions=[
                "Run qsearch.py code-goppa-projectors.",
                "Remove every polynomially separated or verified-equivalent row from code triage.",
                "Route only projector collisions to graph-side baselines, never directly to collective measurement design.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-TANNER-LDPC-SEARCH",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Tanner/LDPC code-family search",
            status="planned",
            hypothesis=(
                "Regular Tanner and LDPC-style codes are natural graph-structured code-equivalence families, but "
                "tuple-profile coincidences must survive Tanner graph isomorphism, structural code invariants, "
                "information-set canonicalization, and aggregate code triage before motivating nonabelian coset measurements."
            ),
            protocol=(
                "Generate small regular bipartite Tanner graphs, convert parity-check matrices to binary linear codes, "
                "bucket by coordinate tuple profiles, and audit every collision with side-preserving Tanner graph "
                "isomorphism, code structural invariants, higher tuple profiles, exact information-set canonicalization, "
                "and profile-pruned canonicalization."
            ),
            positive_signal=(
                "No positive signal; only a non-isomorphic, non-rejected Tanner row that survives canonicalization as "
                "proof debt can feed later code-coset observable design."
            ),
            falsifiers=[
                "A Tanner collision is explained by side-preserving Tanner graph isomorphism.",
                "Structural invariants or tuple profiles separate the collision.",
                "Information-set or profile-pruned canonicalization proves equivalence or rejects the row.",
                "Graph-structured LDPC coincidences are promoted without graph/canonicalization accounting.",
            ],
            metrics=[
                "code_count",
                "tuple_collision_count",
                "tanner_isomorphic_control_count",
                "equivalent_control_count",
                "proof_debt_collision_count",
            ],
            dependencies=["tanner_code_search.py", "code_tuple_profile_baseline.py", "code_information_set_baseline.py", "code_canonicalization_baseline.py"],
            next_actions=[
                "Run qsearch.py code-tanner-search.",
                "Feed Tanner rows into qsearch.py code-triage.",
                "Treat Tanner graph/isomorphism controls as negative evidence, not hardness evidence.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-REED-MULLER-PUNCTURE-SEARCH",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Punctured Reed-Muller code-family search",
            status="planned",
            hypothesis=(
                "Punctured Reed-Muller/evaluation codes are a natural algebraic code-equivalence source, but "
                "any tuple-profile coincidences must survive affine-support automorphism controls, structural "
                "code invariants, low-weight support matroids, and canonicalization before motivating nonabelian "
                "coset measurements."
            ),
            protocol=(
                "Generate punctured RM(r,m) binary evaluation codes from random coordinate supports, include explicit "
                "affine-equivalent support controls, bucket sampled codes by coordinate tuple profiles, and audit every "
                "collision with affine support enumeration, structural invariants, higher tuple profiles, low-weight "
                "support hypergraphs, and profile-pruned canonicalization."
            ),
            positive_signal=(
                "No positive signal; only a non-affine, non-rejected punctured RM row that survives canonicalization "
                "as proof debt can feed later code-coset observable design."
            ),
            falsifiers=[
                "A puncturing-support collision is explained by an affine RM automorphism.",
                "Structural invariants, tuple profiles, low-weight support hypergraphs, or canonicalization separate the collision.",
                "The affine enumeration cap is exceeded and the row is promoted without proof-debt accounting.",
                "Reed-Muller algebraic structure is promoted without affine geometry controls.",
            ],
            metrics=[
                "code_count",
                "tuple_collision_count",
                "affine_control_count",
                "low_weight_rejection_count",
                "canonicalization_rejection_count",
                "proof_debt_collision_count",
            ],
            dependencies=[
                "reed_muller_code_search.py",
                "code_tuple_profile_baseline.py",
                "code_low_weight_structure.py",
                "code_canonicalization_baseline.py",
            ],
            next_actions=[
                "Run qsearch.py code-rm-search.",
                "Feed Reed-Muller rows into qsearch.py code-low-weight and qsearch.py code-triage.",
                "Treat affine-support controls as negative evidence, not hardness evidence.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-RANK-METRIC-SEARCH",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Binary-expanded Gabidulin/rank-metric code-family search",
            status="planned",
            hypothesis=(
                "Rank-metric/Gabidulin codes are a natural algebraic source not covered by cyclic, Goppa, "
                "Tanner, RM, or finite-geometry line-incidence generators. Binary-expanded rows must still "
                "survive symbol-block permutation controls, canonicalization, and aggregate code triage before "
                "they can motivate nonabelian coset measurements."
            ),
            protocol=(
                "Generate small GF(2^m)-linear Gabidulin evaluation codes from GF(2)-independent evaluation "
                "sets, expand symbols into binary coordinates, add explicit symbol-block permutation controls, "
                "bucket rows by coordinate tuple profiles, and attack collisions with structural invariants, "
                "tuple profiles, low-weight support structure, and profile-pruned canonicalization. Record full "
                "rank-metric semilinear equivalence as algebraic context only, not as binary code-equivalence proof."
            ),
            positive_signal=(
                "No positive signal; only a non-block-permutation, non-rejected binary-expanded rank-metric row "
                "that survives canonicalization as proof debt can feed later code-coset observable design."
            ),
            falsifiers=[
                "A row is explained by a symbol-block coordinate permutation.",
                "Profile-pruned canonicalization identifies the row as equivalent or rejects it.",
                "Structural invariants, tuple profiles, or low-weight support hypergraphs separate the row.",
                "Rank-metric semilinear structure is mistaken for binary code-equivalence evidence after expansion.",
            ],
            metrics=[
                "descriptor_count",
                "tuple_collision_count",
                "block_permutation_control_count",
                "equivalent_control_count",
                "low_weight_rejection_count",
                "canonicalization_rejection_count",
                "proof_debt_collision_count",
            ],
            dependencies=[
                "rank_metric_code_search.py",
                "goppa_code_search.py",
                "code_tuple_profile_baseline.py",
                "code_low_weight_structure.py",
                "code_canonicalization_baseline.py",
            ],
            next_actions=[
                "Run qsearch.py code-rank-metric-search.",
                "Feed rank-metric rows into qsearch.py code-low-weight and qsearch.py code-triage.",
                "Treat symbol-block controls as negative evidence, not hardness evidence.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-INCIDENCE-ISOMORPHISM-RESOLVER",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Exact codeword-incidence isomorphism proof-debt resolver",
            status="planned",
            hypothesis=(
                "Small code-equivalence rows that survive profile and information-set caps may still be exact "
                "coordinate-permutation controls. Complete codeword-coordinate incidence graphs give an exact "
                "finite-instance equivalence reduction when code dimension is small enough to enumerate."
            ),
            protocol=(
                "Load proof-debt pairs from binary-expanded rank-metric and quasi-cyclic artifacts, row-reduce each "
                "generator, enumerate every codeword under an explicit 2^k cap, build support-colored bipartite "
                "codeword-coordinate incidence graphs, and run exact colored graph isomorphism. Independently verify "
                "every recovered coordinate permutation against the complete codeword sets; record caps and timeouts "
                "as unresolved proof debt."
            ),
            positive_signal=(
                "No quantum-positive signal. The useful output is a certified control/rejection or a precisely "
                "bounded unresolved row that still needs scalable canonicalization or a lower-bound argument."
            ),
            falsifiers=[
                "An exact incidence isomorphism proves the pair is a coordinate-permutation equivalent control.",
                "Complete incidence graphs are non-isomorphic, classically deciding the finite pair.",
                "The recovered permutation fails full-code verification.",
                "Codeword expansion exceeds the configured 2^k cap.",
                "Exact graph-isomorphism search times out; the row remains proof debt rather than positive evidence.",
            ],
            metrics=[
                "input_count",
                "family_count",
                "equivalent_control_count",
                "exact_rejection_count",
                "verified_permutation_count",
                "proof_debt_count",
                "timeout_count",
                "expansion_cap_count",
            ],
            dependencies=[
                "code_incidence_resolver.py",
                "rank_metric_code_search.py",
                "quasi_cyclic_code_search.py",
                "quasi_cyclic_canonicalization.py",
                "qc_information_set_resolver.py",
                "networkx",
            ],
            next_actions=[
                "Run qsearch.py code-incidence-resolve after rank-metric or quasi-cyclic search artifacts change.",
                "Feed family-level exact certificates into qsearch.py code-triage.",
                "Do not infer asymptotic efficiency from a small exact incidence resolution; the graph has 2^k codeword vertices.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-AFFINE-GEOMETRY-SEARCH",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Affine-geometry incidence-code family search",
            status="planned",
            hypothesis=(
                "Affine-plane incidence codes are natural finite-geometry code-equivalence sources, but punctured "
                "rows must survive AGL(2,q) support automorphism controls, affine line/parallel-class support "
                "profiles, and standard code baselines before they can motivate nonabelian coset measurements."
            ),
            protocol=(
                "Generate binary line-incidence codes from AG(2,q) over prime fields, sample puncturing supports "
                "and explicit AGL(2,q)-equivalent controls, bucket punctured codes by coordinate tuple profiles and "
                "affine support profiles, and audit collisions with affine support enumeration, structural invariants, "
                "tuple profiles, low-weight support structure, and canonicalization."
            ),
            positive_signal=(
                "No positive signal; only a non-affine-equivalent, non-rejected affine-geometry row that survives "
                "canonicalization as proof debt can feed later code-coset observable design."
            ),
            falsifiers=[
                "A puncturing-support collision is explained by an affine-linear automorphism.",
                "Affine line or parallel-class profiles only generate equivalent controls.",
                "Structural invariants, tuple profiles, low-weight support hypergraphs, or canonicalization separate the collision.",
                "Affine-geometry incidence structure is promoted without automorphism accounting.",
            ],
            metrics=[
                "code_count",
                "tuple_collision_count",
                "support_affine_profile_collision_count",
                "affine_control_count",
                "low_weight_rejection_count",
                "canonicalization_rejection_count",
                "proof_debt_collision_count",
            ],
            dependencies=[
                "affine_geometry_code_search.py",
                "code_tuple_profile_baseline.py",
                "code_low_weight_structure.py",
                "code_canonicalization_baseline.py",
            ],
            next_actions=[
                "Run qsearch.py code-ag-search.",
                "Feed affine-geometry rows into qsearch.py code-low-weight and qsearch.py code-triage.",
                "Treat affine-linear support controls as negative evidence, not hardness evidence.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-PROJECTIVE-GEOMETRY-SEARCH",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Projective-geometry incidence-code family search",
            status="planned",
            hypothesis=(
                "Projective-plane incidence codes are natural finite-geometry code-equivalence sources, but "
                "punctured rows must survive projective-linear support automorphism controls and standard code "
                "baselines before they can motivate nonabelian coset measurements."
            ),
            protocol=(
                "Generate binary line-incidence codes from PG(2,q), sample puncturing supports and explicit "
                "projective-linear support controls, bucket punctured codes by coordinate tuple profiles, and audit "
                "collisions with projective support enumeration, structural invariants, tuple profiles, low-weight "
                "support structure, and canonicalization."
            ),
            positive_signal=(
                "No positive signal; only a non-projective-equivalent, non-rejected finite-geometry row that survives "
                "canonicalization as proof debt can feed later code-coset observable design."
            ),
            falsifiers=[
                "A puncturing-support collision is explained by a projective-linear automorphism.",
                "Structural invariants, tuple profiles, low-weight support hypergraphs, or canonicalization separate the collision.",
                "Finite-geometry incidence structure is promoted without automorphism accounting.",
            ],
            metrics=[
                "code_count",
                "tuple_collision_count",
                "projective_control_count",
                "low_weight_rejection_count",
                "canonicalization_rejection_count",
                "proof_debt_collision_count",
            ],
            dependencies=[
                "projective_geometry_code_search.py",
                "code_tuple_profile_baseline.py",
                "code_low_weight_structure.py",
                "code_canonicalization_baseline.py",
            ],
            next_actions=[
                "Run qsearch.py code-pg-search.",
                "Feed finite-geometry rows into qsearch.py code-low-weight and qsearch.py code-triage.",
                "Treat projective-linear support controls as negative evidence, not hardness evidence.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-SCHUR-FILTRATION",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Primal/dual Schur-product code filtration",
            status="planned",
            hypothesis=(
                "Algebraic code-equivalence rows must survive polynomial-time Schur/star-product dimensions and local "
                "puncture/shortening filtrations before they can motivate collective coset-state measurements."
            ),
            protocol=(
                "For every available binary code pair, compute primal and dual Schur powers through degree three, "
                "coordinate puncture and shortening square-dimension multisets, and joint coordinate filtration profiles. "
                "Reject mismatches, preserve equivalent controls, and label all matches as proof debt."
            ),
            positive_signal=(
                "No positive signal is emitted. A matching Schur filtration only permits stronger conductor, support-recovery, "
                "and canonical-labeling attacks; it never certifies hard code equivalence."
            ),
            falsifiers=[
                "Primal or dual Schur-power dimensions differ.",
                "Coordinate puncture/shortening Schur profiles differ.",
                "A matching filtration is mistaken for evidence instead of proof debt.",
                "Known alternant/GRS support-recovery attacks apply to the parameter regime.",
            ],
            metrics=[
                "input_pair_count",
                "family_count",
                "schur_rejection_count",
                "equivalent_control_count",
                "schur_proof_debt_count",
                "positive_evidence_count",
            ],
            dependencies=[
                "code_schur_filtration.py",
                "code_low_weight_structure.py",
                "bardet-high-rate-alternant-2023",
                "astore-rank-metric-geometric-invariant-2024",
            ],
            next_actions=[
                "Run qsearch.py code-schur-filtration.",
                "Apply conductor/support-recovery attacks to Schur-profile collisions.",
                "Route only aggregate-triage proof debt into measurement design.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-CLOSURE-CONDUCTOR-ATTACK",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Prime-field conductor and t-closure support-recovery attack",
            status="planned",
            hypothesis=(
                "Schur-profile collisions remain classically vulnerable when conductors or t-closures distinguish "
                "the pair or reconstruct a hidden ambient algebraic evaluation code."
            ),
            protocol=(
                "Implement exact row reduction over prime fields, compute Cond(C^(t-1), C^t), primal/dual local "
                "puncture and shortening closure signatures for every available binary code pair, and calibrate "
                "support recovery by reconstructing an ambient Reed-Solomon code from a proper subcode."
            ),
            positive_signal=(
                "No positive signal is emitted. Matching closure signatures remain proof debt for explicit support, "
                "automorphism, and canonical-labeling recovery."
            ),
            falsifiers=[
                "A conductor or t-closure dimension separates the pair.",
                "A local puncture/shortening closure profile separates the pair.",
                "The closure reconstructs a hidden ambient evaluation code.",
                "A matching closure signature is promoted as quantum evidence.",
            ],
            metrics=[
                "input_pair_count",
                "family_count",
                "closure_rejection_count",
                "equivalent_control_count",
                "closure_proof_debt_count",
                "ambient_recovery_calibration_count",
                "positive_evidence_count",
            ],
            dependencies=[
                "code_closure_attack.py",
                "code_schur_filtration.py",
                "couvreur-ag-code-closure-2014",
                "bardet-high-rate-alternant-2023",
            ],
            next_actions=[
                "Run qsearch.py code-closure-attack.",
                "Feed closure family decisions into qsearch.py code-triage.",
                "Reject every separated row before coset-state measurement design.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-TRIVIAL-HULL-PROJECTOR-GI",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Hull-projector graph reduction for planted random code equivalence",
            status="planned",
            hypothesis=(
                "Random planted code-equivalence rows must be stratified by hull dimension because trivial-hull codes "
                "reduce exactly to weighted graph isomorphism and bounded hull activates a shortening upper bound."
            ),
            protocol=(
                "Sample unconditional half-rate binary codes to estimate finite hull distributions; separately build "
                "trivial-hull planted equivalent pairs and matched independent nulls, certify the basis-independent "
                "projector, run exact colored graph matching, recover coordinate permutations, and verify full row spaces."
            ),
            positive_signal=(
                "No direct quantum signal. Only growing-hull families that survive source-linked shortening, GI, and "
                "code-native baselines may remain code-specific proof debt."
            ),
            falsifiers=[
                "The projector graph recovers and verifies the planted coordinate permutation.",
                "The independent null is rejected by projector graph nonisomorphism.",
                "Finite hull dimensions remain bounded, activating the source shortening upper bound.",
                "A finite GI timeout is mislabeled as a lower bound or quantum signal.",
            ],
            metrics=[
                "trivial_hull_fraction",
                "hull_at_most_two_fraction",
                "projector_finite_resolved_count",
                "projector_timeout_count",
                "maximum_observed_hull_dimension",
                "fitted_log2_graph_match_time_slope_per_n",
                "proved_polynomial_gi_solver_count",
                "positive_quantum_evidence_count",
            ],
            dependencies=[
                "code_hull_projector_reduction.py",
                "bardet-otmani-saeed-trivial-hull-2019",
                "networkx",
            ],
            next_actions=[
                "Run qsearch.py code-hull-projector.",
                "Reject trivial-hull rows as independent code-native evidence; route them to GI research instead.",
                "Search for natural growing-hull code families and charge Theorem 10 shortening before observable design.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-CFI-FAITHFUL-REDUCTION",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Faithful CFI graph-to-code equivalence reduction",
            status="planned",
            hypothesis=(
                "A useful CFI-derived code benchmark must preserve graph isomorphism in both directions and survive "
                "every graph-side attack that remains legal after explicit generator recovery."
            ),
            protocol=(
                "Encode each CFI graph with multiplicity-two vertex basis tags and multiplicity-one edge sums; prove "
                "graph isomorphism iff binary code equivalence, scramble rows and coordinates, recover the unlabeled "
                "graph in polynomial time, verify equivalent controls, and run low-cost and promised CFI decoders."
            ),
            positive_signal=(
                "No positive quantum signal. A row remains proof debt only if the iff reduction verifies and the "
                "recovered graph survives every legal graph-side decoder."
            ),
            falsifiers=[
                "The equivalent-control or graph-recovery certificate fails.",
                "A polynomial graph invariant separates the recovered pair.",
                "The promised CFI structural decoder recovers global twist parity.",
                "Graph recovery alone is mislabeled as a graph-isomorphism solution.",
            ],
            metrics=[
                "theorem_direction_count",
                "recovery_verified_count",
                "equivalent_control_verified_count",
                "promised_decoder_dequantized_count",
                "transferred_gi_proof_debt_count",
                "positive_quantum_evidence_count",
            ],
            dependencies=[
                "cfi_code_reduction.py",
                "cfi_base_family_search.py",
                "cfi_structural_decoder.py",
            ],
            next_actions=[
                "Run qsearch.py cfi-code-reduction.",
                "Reject promised CFI code rows decoded after legal graph recovery.",
                "Use the reduction only to transfer genuinely hard general-GI families, never to manufacture hardness.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-FRONTIER-TRIAGE",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Aggregate code-equivalence frontier triage",
            status="planned",
            hypothesis=(
                "A code-equivalence row should not feed nonabelian coset measurement design unless it survives every "
                "implemented structural, tuple-profile, information-set, canonicalization, and quasi-cyclic automorphism baseline."
            ),
            protocol=(
                "Read all code-equivalence workbench artifacts, normalize row identities across generated families and "
                "quasi-cyclic collision records, merge evidence, and classify each row as rejected, control/no-hard-row, "
                "or proof debt."
            ),
            positive_signal=(
                "No positive signal; the only acceptable output is explicit proof debt for a row that survives all current "
                "classical baselines without being an equivalent control or no-collision search."
            ),
            falsifiers=[
                "Any structural, tuple-profile, information-set, or canonicalization baseline rejects the row.",
                "The row is an equivalent control under natural automorphisms.",
                "The search budget finds no nontrivial collision and is still treated as evidence.",
            ],
            metrics=[
                "record_count",
                "rejected_row_count",
                "proof_debt_row_count",
                "control_or_no_hard_row_count",
                "evidence_count",
            ],
            dependencies=[
                "code_frontier_triage.py",
                "code_structural_invariants.py",
                "code_tuple_profile_baseline.py",
                "quasi_cyclic_canonicalization.py",
            ],
            next_actions=[
                "Run qsearch.py code-triage.",
                "Route only proof-debt survivors into stronger canonical labeling or code-coset observable design.",
                "Treat rejected/control rows as negative search information for the mutation engine.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-COLLECTIVE-OBSERVABLE-SEARCH",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Adversarial low-register collective observable search",
            status="planned",
            hypothesis="A useful coset-state observable must distinguish CFI/code boundary instances without collapsing to WL, spectra, walk counts, or bounded tensor contractions.",
            protocol=(
                "Evaluate explicit low-register observable templates on CFI, strongly regular, and control graph pairs; "
                "tag every separator with its classical shadow and treat scaling caps as proof debt rather than evidence."
            ),
            positive_signal="A polynomial-description observable separates a boundary pair while no implemented classical shadow or WL baseline explains the signal.",
            falsifiers=[
                "Every separating observable matches a WL, spectral, walk-count, or low-rank tensor contraction baseline.",
                "Boundary CFI instances have no separating signal under the implemented observable family.",
                "The first separating high-register probe exceeds brute-force tuple caps without an implicit polynomial description.",
            ],
            metrics=[
                "classical_shadow_collapse_count",
                "boundary_pair_count",
                "skipped_scaling_count",
                "nonclassical_candidate_count",
            ],
            dependencies=["collective_observable_search.py", "coset_state_workbench.py", "classical invariant baselines"],
            next_actions=[
                "Run qsearch.py collective-observables.",
                "If any nonclassical candidate appears, add proof obligations before promotion.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-GM-SWITCHING-SEARCH",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Godsil-McKay cospectral row generation and dequantization",
            status="planned",
            hypothesis=(
                "Cospectral non-isomorphic graph rows from natural Godsil-McKay switching are a more credible "
                "nonabelian-HSP stress source than toy oracle rows, but they must survive WL, graphlet, "
                "individualization, and rooted tensor baselines before measurement design."
            ),
            protocol=(
                "Search deterministic Godsil-McKay switching sets in rook and strongly regular Cayley graph families, "
                "keep non-isomorphic cospectral switched rows, and immediately attack each row with classical shadows."
            ),
            positive_signal=(
                "No positive signal; a row only becomes measurement-design proof debt if it is non-isomorphic, "
                "cospectral, and survives every implemented classical baseline without skipped-cap ambiguity."
            ),
            falsifiers=[
                "4-WL, graphlet tensors, individualization-refinement, or rooted tensor signatures distinguish the switched row.",
                "Valid switching sets produce only isomorphic controls.",
                "Cospectrality is promoted without triage and exact-isomorphism sanity checks.",
            ],
            metrics=[
                "nonisomorphic_cospectral_count",
                "dequantized_row_count",
                "proof_debt_row_count",
                "survivor_row_count",
                "valid_switching_sets_seen",
            ],
            dependencies=["godsil_mckay_search.py", "individualized_tensor_observables.py", "graphlet_tensor_observables.py"],
            next_actions=[
                "Run qsearch.py gm-switching.",
                "Reject switched rows separated by classical baselines.",
                "Feed only survivors into coset frontier triage and measurement-proof obligations.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-CFI-BASE-FAMILY-SEARCH",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="CFI base-family search beyond complete graphs",
            status="planned",
            hypothesis="Useful CFI/coset stress tests should survive low-cost invariants and individualization-refinement beyond complete-graph gadgets.",
            protocol=(
                "Generate CFI parity twists over complete, prism, cube, Mobius-ladder, Petersen, and larger cubic bases; "
                "compare cheap invariants, WL2, individualized-WL, and capped exact sanity checks."
            ),
            positive_signal="Only rows surviving implemented baselines become proof debt for later measurement design; no row is positive evidence.",
            falsifiers=[
                "Low-cost invariants or WL2 distinguish the CFI twist.",
                "Individualization-refinement distinguishes the CFI twist.",
                "Exact sanity check finds the twisted row isomorphic to the untwisted row.",
                "Survival is promoted without asymptotic proof or stronger classical baselines.",
            ],
            metrics=[
                "low_cost_dequantized_count",
                "individualized_wl_dequantized_count",
                "proof_debt_survivor_count",
                "finite_survivor_count",
            ],
            dependencies=["cfi_base_family_search.py", "individualized_wl_baseline.py", "coset_state_workbench.py"],
            next_actions=[
                "Run qsearch.py cfi-base-search.",
                "Use only survivor/proof-debt rows as inputs to future collective-observable design.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-CFI-SCALING",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="CFI parity scaling boundary probe",
            status="planned",
            hypothesis="CFI parity families force collective-measurement proof debt when low-cost invariants fail and brute-force WL/graphlet probes hit scaling caps.",
            protocol=(
                "Generate complete-graph CFI parity twists across increasing base sizes; compare degree, spectrum, walk, WL2, "
                "homomorphism moments, bounded 3-WL, and four-graphlet tensor counts while tracking tuple-cap failures."
            ),
            positive_signal="No low-cost classical invariant distinguishes the family, and larger rows force implicit polynomial collective observables rather than brute-force tuple enumeration.",
            falsifiers=[
                "A low-cost invariant distinguishes the CFI row.",
                "3-WL or graphlet tensor counts distinguish before scaling caps matter.",
                "Boundary status is promoted without an explicit measurement construction and dequantization proof.",
            ],
            metrics=[
                "boundary_record_count",
                "wl3_skipped_count",
                "graphlet4_skipped_count",
                "max_vertex_count",
            ],
            dependencies=["cfi_scaling_probe.py", "coset_state_workbench.py", "graphlet_tensor_observables.py"],
            next_actions=[
                "Run qsearch.py cfi-scaling.",
                "Use boundary rows only to specify representation-theoretic measurement proof obligations.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-CFI-PARITY-SOLVER",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Promised CFI gadget parity decoder baseline",
            status="planned",
            hypothesis=(
                "Complete-graph CFI parity benchmark rows should not be treated as hard coset evidence if "
                "the global twist is classically recoverable from the promised gadget structure."
            ),
            protocol=(
                "Generate untwisted and single-twist complete-CFI graphs, randomly relabel vertices, reconstruct "
                "degree classes, edge-copy twin pairs, vertex gadgets, and decode the global twist parity."
            ),
            positive_signal=(
                "No positive signal; failure to decode remains proof debt.  Successful decoding is a dequantization "
                "baseline for promised complete-CFI families."
            ),
            falsifiers=[
                "The promised CFI gadget structure reveals the global twist parity classically.",
                "A candidate counts complete-CFI boundary rows as evidence while using an access model where the structural decoder is legal.",
                "K4 ambiguity or larger-row failures are promoted without a generic measurement/lower-bound argument.",
            ],
            metrics=[
                "decoded_count",
                "dequantized_count",
                "ambiguous_count",
                "failed_count",
                "max_vertex_count",
            ],
            dependencies=["cfi_parity_solver.py", "coset_state_workbench.py"],
            next_actions=[
                "Run qsearch.py cfi-parity-solver.",
                "If larger complete-CFI rows decode, demote them as promised-family negative results.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-CFI-STRUCTURAL-DECODER",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Structural CFI gadget parity decoder over regular bases",
            status="planned",
            hypothesis=(
                "Non-complete CFI base-family survivors should not be treated as coset evidence if the promised "
                "regular CFI gadget structure classically reveals the global twist parity."
            ),
            protocol=(
                "Generate untwisted and single-edge-twisted CFI graphs over complete, prism, cube, Mobius-ladder, "
                "Petersen, and larger cubic bases; randomly relabel vertices; infer middle/edge-copy degree classes, "
                "reconstruct edge-copy pairs and vertex gadgets, then decode global twist parity."
            ),
            positive_signal=(
                "No positive signal; decoder failures remain proof debt.  Successful decoding is a dequantization "
                "baseline for promised regular-CFI families."
            ),
            falsifiers=[
                "Regular CFI gadget structure reveals the global twist parity classically.",
                "A candidate counts non-complete CFI survivor rows as evidence while the structural decoder is legal.",
                "Ambiguous or failed rows are promoted without a measurement construction and lower-bound argument.",
            ],
            metrics=[
                "decoded_count",
                "dequantized_count",
                "ambiguous_count",
                "failed_count",
                "max_vertex_count",
            ],
            dependencies=["cfi_structural_decoder.py", "cfi_base_family_search.py"],
            next_actions=[
                "Run qsearch.py cfi-structural-decoder.",
                "If non-complete CFI rows decode, demote them as promised-family negative results.",
                "If rows fail, keep them as proof debt and add a stronger structural/canonicalization baseline.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-CFI-IRREGULAR-STRUCTURAL-DECODER",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Structural CFI gadget parity decoder over irregular degree-separated bases",
            status="planned",
            hypothesis=(
                "Making CFI base graphs irregular should not be counted as escaping the promised-gadget classical "
                "attack unless degree-separated gadget structure no longer reveals the global twist parity."
            ),
            protocol=(
                "Generate untwisted and single-edge-twisted CFI graphs over complete bipartite and tripartite "
                "irregular bases; randomly relabel vertices; infer degree-separated middle gadgets, reconstruct "
                "edge-copy twin pairs and vertex gadgets, then decode global twist parity."
            ),
            positive_signal=(
                "No positive signal; successful decoding is a dequantization baseline. Decoder failures only define "
                "proof debt for stronger structural/canonicalization attacks."
            ),
            falsifiers=[
                "Degree-separated irregular CFI gadget structure reveals the global twist parity classically.",
                "A candidate treats irregular CFI rows as promising while this decoder is legal.",
                "Decoder failures are promoted without proving that the CFI promise is unavailable in the input model.",
            ],
            metrics=[
                "decoded_count",
                "dequantized_count",
                "proof_debt_count",
                "degree_separated_count",
                "max_vertex_count",
            ],
            dependencies=["cfi_irregular_structural_decoder.py", "cfi_base_family_search.py"],
            next_actions=[
                "Run qsearch.py cfi-irregular-decoder.",
                "Record degree-separated irregular CFI rows as negative results when decoded.",
                "If any row fails, add a non-degree-separated structural recognizer before treating it as evidence.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-CFI-BIPARTITE-STRUCTURAL-DECODER",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Bipartition structural CFI parity decoder beyond degree separation",
            status="planned",
            hypothesis=(
                "CFI rows whose middle degrees collide with edge-copy degrees should still not be counted as coset "
                "evidence if the bipartition-visible gadget structure reveals the global twist parity."
            ),
            protocol=(
                "Generate regular, degree-separated irregular, and non-degree-separated CFI parity graphs; randomly "
                "relabel vertices; infer the graph bipartition, reconstruct edge-copy twin pairs and vertex gadgets, "
                "then decode global twist parity without assuming degree-class separation."
            ),
            positive_signal=(
                "No positive signal; successful decoding is a dequantization baseline. Remaining failures are proof "
                "debt requiring stronger CFI recognizers or proof that the gadget promise is unavailable."
            ),
            falsifiers=[
                "Bipartition-visible CFI gadget structure reveals the global twist parity classically.",
                "A candidate treats non-degree-separated CFI rows as promising while this decoder is legal.",
                "Ambiguous bipartition rows are promoted without an additional side-selection or measurement proof.",
            ],
            metrics=[
                "decoded_count",
                "dequantized_count",
                "proof_debt_count",
                "non_degree_separated_count",
                "max_vertex_count",
            ],
            dependencies=["cfi_bipartite_structural_decoder.py", "cfi_base_family_search.py"],
            next_actions=[
                "Run qsearch.py cfi-bipartite-decoder.",
                "Record non-degree-separated CFI rows as negative results when decoded.",
                "If rows fail, require a natural input-model argument before using them in collective-observable search.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-INDIVIDUALIZED-WL",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Individualization-refinement WL baseline for graph/coset rows",
            status="planned",
            hypothesis="Graph/coset boundary rows must survive individualization plus color refinement before motivating quantum observables.",
            protocol="Individualize one, two, and three vertices under a tuple cap, run WL color refinement, and compare signature multisets.",
            positive_signal="No positive signal; separated rows are classical dequantizations and skipped rows are proof debt.",
            falsifiers=[
                "Individualization-refinement separates the graph pair.",
                "A matching quantum observable is promoted without comparison to individualized WL.",
                "Scaling caps are counted as evidence instead of proof debt.",
            ],
            metrics=[
                "dequantized_pair_count",
                "survivor_pair_count",
                "proof_debt_pair_count",
                "distinguishing_record_count",
            ],
            dependencies=["individualized_wl_baseline.py", "coset_state_workbench.py"],
            next_actions=[
                "Run qsearch.py individualized-wl.",
                "Reject any graph/coset row separated by individualization-refinement.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-INDIVIDUALIZED-TENSOR-OBSERVABLES",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Individualized rooted tensor-shadow baseline for coset observables",
            status="planned",
            hypothesis=(
                "A proposed collective coset observable should not count as nonclassical evidence if it is reproduced "
                "by individualizing a few vertices and comparing rooted graphlet/tensor signatures."
            ),
            protocol=(
                "For each graph/coset pair, individualize root sets under a cap, compute rooted one- and two-extension "
                "graphlet tensor signature multisets, and classify every separator as a classical shadow."
            ),
            positive_signal=(
                "No positive signal; separated rows are dequantized and cap-limited rows are proof debt requiring "
                "implicit or sampled rooted-tensor baselines."
            ),
            falsifiers=[
                "Individualized rooted tensor signatures separate the graph pair.",
                "A proposed collective observable is equivalent to rooted graphlet/tensor counting.",
                "Rooted tensor enumeration caps are treated as evidence instead of proof debt.",
            ],
            metrics=[
                "dequantized_pair_count",
                "survivor_pair_count",
                "proof_debt_pair_count",
                "distinguishing_record_count",
                "skipped_record_count",
            ],
            dependencies=["individualized_tensor_observables.py", "graphlet_tensor_observables.py", "coset_state_workbench.py"],
            next_actions=[
                "Run qsearch.py individualized-tensors.",
                "Reject rows separated by rooted tensor shadows before designing quantum collective measurements.",
                "For cap-limited rows, add implicit rooted-tensor contractions or sample-complexity lower bounds.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-FRONTIER-TRIAGE",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Coset frontier row triage gate",
            status="planned",
            hypothesis=(
                "No graph/coset row should feed collective-measurement design until all existing WL, tensor, "
                "individualization, rooted tensor, and structural CFI evidence is aggregated into a reject/proof-debt decision."
            ),
            protocol=(
                "Read coset workbench, collective-observable, graphlet tensor, individualized WL, individualized rooted "
                "tensor, and promised CFI decoder artifacts; classify each row as rejected, proof debt, or surviving current baselines."
            ),
            positive_signal=(
                "No positive signal; survivors become measurement-design proof debt and rejected rows are written as negative results."
            ),
            falsifiers=[
                "A row is already separated by a classical invariant or rooted tensor shadow.",
                "A promised CFI structural decoder recovers the twist.",
                "A cap-limited row is treated as quantum evidence instead of proof debt.",
            ],
            metrics=[
                "rejected_pair_count",
                "proof_debt_pair_count",
                "survivor_pair_count",
                "dequantizing_evidence_count",
                "proof_debt_evidence_count",
            ],
            dependencies=[
                "coset_frontier_triage.py",
                "collective_observable_search.py",
                "graphlet_tensor_observables.py",
                "individualized_wl_baseline.py",
                "individualized_tensor_observables.py",
                "cfi_parity_solver.py",
            ],
            next_actions=[
                "Run qsearch.py coset-triage.",
                "Route only survivor/proof-debt rows into any future collective measurement search.",
                "Delete or quarantine measurement ideas whose target row is triage-rejected.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-REPRESENTATION-OBSTRUCTIONS",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Symmetric-group representation obstruction ledger",
            status="planned",
            hypothesis="Strong Fourier sampling over S_n should be treated as a blocked route unless a candidate supplies genuinely collective measurement information.",
            protocol=(
                "Enumerate partitions of n, compute hook-length irrep dimensions and Plancherel masses, then track where mass leaves "
                "low-dimensional labels and concentrates on balanced high-dimensional irreps."
            ),
            positive_signal="No positive signal; this experiment is a no-go ledger that forces collective-measurement proof obligations.",
            falsifiers=[
                "A candidate relies only on single-register strong Fourier labels over the symmetric group.",
                "Representation-label evidence is promoted without showing collective information beyond known no-go barriers.",
            ],
            metrics=[
                "no_go_pressure_count",
                "min_low_dimension_mass",
                "max_balanced_shape_mass",
                "max_partition_count",
            ],
            dependencies=["representation_obstruction.py"],
            next_actions=[
                "Run qsearch.py representation-obstructions.",
                "Require any coset candidate to explain how it bypasses the strong Fourier sampling obstruction.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-WEAK-FOURIER-SIGNAL",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Weak Fourier label signal for symmetric involution subgroups",
            status="planned",
            hypothesis="Weak Fourier irrep labels over S_n carry too little hidden-involution information for GI/code-equivalence routes without collective measurements.",
            protocol=(
                "Compute Murnaghan-Nakayama characters for cycle types 2^r 1^(n-2r), compare hidden-subgroup weak Fourier label "
                "distributions against Plancherel, and measure total variation, KL divergence, and low-dimensional signal fraction."
            ),
            positive_signal="No positive signal; transposition rows are controls and fixed-point-free rows should force collective-measurement proof obligations.",
            falsifiers=[
                "Fixed-point-free involution labels are nearly Plancherel.",
                "Residual label signal lives outside low-dimensional irreps accessible to efficient single-register postprocessing.",
                "A candidate promotes weak label bias without a collective measurement or decoding procedure.",
            ],
            metrics=[
                "near_plancherel_count",
                "small_signal_count",
                "max_fixed_point_free_total_variation",
                "min_fixed_point_free_low_dimension_fraction",
            ],
            dependencies=["weak_fourier_signal.py", "representation_obstruction.py"],
            next_actions=[
                "Run qsearch.py weak-fourier.",
                "Require any symmetric-HSP candidate to exceed irrep-label-only information.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-STATE-DISTINGUISHABILITY",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Multi-copy distinguishability accounting for involution coset states",
            status="planned",
            hypothesis="A symmetric-HSP coset route must account for ensemble size, copy complexity, and decoding cost after weak Fourier labels fail.",
            protocol=(
                "For involution hidden subgroups H={e,h}, compute ensemble sizes, Holevo copy lower bounds, pairwise Hilbert-Schmidt overlaps, "
                "and k-copy overlap thresholds, linked to weak Fourier label-signal artifacts."
            ),
            positive_signal="No positive signal; this experiment records measurement/copy obligations for any future collective observable.",
            falsifiers=[
                "A candidate claims progress from few-copy or label-only evidence without addressing ensemble-size information requirements.",
                "A proposed collective measurement omits decoding/cost accounting for the hidden involution ensemble.",
            ],
            metrics=[
                "copy_debt_count",
                "max_holevo_copy_lower_bound",
                "max_fixed_point_free_holevo_bound",
                "max_fixed_point_free_inverse_square_overlap_copies",
            ],
            dependencies=["coset_state_distinguishability.py", "weak_fourier_signal.py"],
            next_actions=[
                "Run qsearch.py coset-distinguishability.",
                "Require future coset candidates to state copy, measurement, and decoding complexity against this ledger.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-PGM-CAPACITY",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="PGM capacity and measurement-debt ledger for coset states",
            status="planned",
            hypothesis=(
                "Information-theoretic PGM distinguishability of symmetric-group involution coset states is not "
                "algorithmic evidence unless there is an efficient collective measurement and decoder."
            ),
            protocol=(
                "For transposition, partial-matching, and fixed-point-free involution ensembles, compute ensemble "
                "sizes, copy thresholds for overlap cross-mass, explicit PGM matrix scale, register-bit obligations, "
                "and weak-Fourier obstruction context."
            ),
            positive_signal="No positive signal; PGM capacity rows become measurement-design proof debt unless an efficient implementation is supplied.",
            falsifiers=[
                "The route relies on explicit PGM over an exponentially large hidden-involution ensemble.",
                "Weak Fourier labels are nearly Plancherel or small-signal while no collective decoder is specified.",
                "Information-theoretic copy thresholds are treated as an efficient algorithm.",
            ],
            metrics=[
                "measurement_proof_debt_count",
                "max_cross_mass_threshold_copies",
                "max_register_bits_at_threshold",
                "max_explicit_pgm_matrix_log2_entries",
            ],
            dependencies=["coset_pgm_capacity.py", "weak_fourier_signal.py", "coset_state_distinguishability.py"],
            next_actions=[
                "Run qsearch.py coset-pgm.",
                "Reject label-only or explicit-PGM routes without polynomial measurement/decoder structure.",
                "Use surviving rows only to specify concrete collective-measurement proof obligations.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-HOLEVO-INFORMATION",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Exact Holevo information and involution copy lower bound",
            status="planned",
            hypothesis=(
                "The exact central one-copy spectrum may impose a stronger-than-one-bit sample barrier on hard "
                "symmetric-group involution ensembles."
            ),
            protocol=(
                "Compute the exact one-copy Holevo information from character ratios; prove the same-hidden k-copy "
                "subadditivity bound; apply Fano's inequality for bounded-error and zero-error decoding; and compare "
                "the resulting copy budget with polynomial recoupling resource claims."
            ),
            positive_signal=(
                "A superpolynomial copy lower bound kills the coset route, or a polynomial-copy mechanism explicitly "
                "meets the certified budget and supplies recoupling plus a verified decoder."
            ),
            falsifiers=[
                "A proposal uses fewer copies than the exact Holevo/Fano lower bound.",
                "Pairwise overlap is substituted for accessible information.",
                "A polynomial Omega(n log n) lower bound is called a no-algorithm theorem.",
                "Information sufficiency is presented without a collective measurement.",
                "The decoder enumerates the full involution conjugacy class.",
            ],
            metrics=[
                "exact_holevo_formula_count",
                "multi_copy_subadditivity_theorem_count",
                "fano_copy_lower_bound_count",
                "minimum_hard_family_one_copy_holevo_bits",
                "maximum_hard_family_zero_error_copy_lower_bound",
                "polynomial_collective_measurement_count",
                "polynomial_outcome_decoder_count",
            ],
            dependencies=[
                "coset_holevo_information.py",
                "coset_covariant_frame.py",
                "coset_state_distinguishability.py",
                "symmetric_character.py",
            ],
            next_actions=[
                "Charge every recoupling mechanism the certified copy budget.",
                "Do not pursue copy lower bounds further unless a superpolynomial regime appears.",
                "Focus on internal Kronecker transforms, associators, frame action, and compressed decoding.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-COVARIANT-FRAME",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Covariant coset-state frame spectrum and one-copy PGM theorem",
            status="planned",
            hypothesis=(
                "Central class-sum normalization of a conjugacy-class involution ensemble may expose a compressed "
                "collective-measurement primitive beyond weak Fourier labels."
            ),
            protocol=(
                "Diagonalize the uniform one-copy frame using exact character ratios, derive its support and condition "
                "number, prove the exact PGM success probability, and isolate multi-copy diagonal-action obligations."
            ),
            positive_signal=(
                "A polynomial circuit block-diagonalizes the k-copy diagonal conjugation algebra and decodes the hidden "
                "involution without an explicit conjugacy-class outcome table."
            ),
            falsifiers=[
                "One-copy PGM improves random guessing only by a constant factor.",
                "The proposal stops at central frame diagonalization.",
                "The k-copy decomposition or outcome table is exponential.",
                "No polynomial decoder maps compressed representation data to the hidden involution.",
            ],
            metrics=[
                "exact_central_frame_spectrum_count",
                "exact_single_copy_pgm_formula_count",
                "maximum_frontier_one_copy_pgm_advantage",
                "multi_copy_diagonal_action_proof_debt_count",
                "efficient_multi_copy_diagonal_action_circuit_count",
                "polynomial_outcome_decoder_count",
            ],
            dependencies=[
                "coset_covariant_frame.py",
                "weak_fourier_signal.py",
                "coset_state_distinguishability.py",
            ],
            next_actions=[
                "Construct the two-copy diagonal-conjugation commutant explicitly on small S_n.",
                "Search recoupling/Schur-transform circuits for k=Theta(n log n) without class enumeration.",
                "Design compressed covariant outcome decoding and compare it to classical invariants.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-TWO-COPY-FRAME",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Two-copy Kronecker frame spectrum and transition-algebra obstruction",
            status="planned",
            hypothesis=(
                "Recoupling two involution coset-state registers into symmetric-group Kronecker sectors may expose "
                "a compressed collective-measurement mechanism unavailable to one-copy Fourier labels."
            ),
            protocol=(
                "Compute exact symmetric-group characters by Murnaghan-Nakayama, exact Kronecker multiplicities, "
                "the two-copy average-frame spectrum, rigorous PGM spectral bounds, and an explicit S_3 "
                "noncommutation control testing whether sector ranks determine mixed-state PGM success."
            ),
            positive_signal=(
                "A uniform polynomial procedure computes the cross-sector transition coefficients, implements the "
                "coherent recoupling transform, and decodes a hidden involution without class enumeration."
            ),
            falsifiers=[
                "Character ratios and Kronecker multiplicities fail to determine mixed-state PGM success.",
                "An individual coset state does not commute with the average two-copy frame.",
                "Transition coefficients require exponential multiplicity-space data.",
                "The coherent transform or hidden-involution outcome decoder has superpolynomial cost.",
            ],
            metrics=[
                "exact_two_copy_recoupling_spectrum_count",
                "spectral_pgm_bound_count",
                "rank_formula_counterexample_count",
                "coherent_kronecker_transform_proof_debt_count",
                "coherent_kronecker_transform_count",
                "polynomial_outcome_decoder_count",
            ],
            dependencies=[
                "coset_two_copy_frame.py",
                "symmetric_character.py",
                "coset_covariant_frame.py",
            ],
            next_actions=[
                "Derive exact transition weights between Kronecker sectors using symmetric-group recoupling data.",
                "Audit whether multiplicity-space access can be implemented uniformly in polynomial time.",
                "Extend to k>=3 and reject any route whose associator or outcome representation is exponential.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-TWO-COPY-TRANSITION-ALGEBRA",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Two-copy cross-sector transition algebra audit",
            status="planned",
            hypothesis=(
                "The off-diagonal transition weights of an individual involution coset state may possess a compressed "
                "recoupling formula that turns the exact average-frame spectrum into a collective measurement."
            ),
            protocol=(
                "Construct regular two-copy states for tractable S_n, verify the exact character/Kronecker frame "
                "spectrum, measure every cross-eigenspace Frobenius transition, reconstruct PGM success, and account "
                "for the dense |S_n|^4 representation cost."
            ),
            positive_signal=(
                "Transition weights admit a uniform partition-level formula and polynomial coherent implementation "
                "that avoids regular-space matrices and supports compressed outcome decoding."
            ),
            falsifiers=[
                "Off-diagonal transitions remain essential but require factorial multiplicity-space data.",
                "Only exceptional commuting or abelian classes obey the spectrum-rank shortcut.",
                "The transition table or recoupling transform requires |S_n|^Omega(1) resources.",
                "Exact finite PGM success has no polynomial hidden-involution decoder.",
            ],
            metrics=[
                "spectrum_verified_count",
                "noncommuting_frame_count",
                "nonzero_off_diagonal_transition_count",
                "rank_formula_falsified_count",
                "commuting_class_control_count",
                "polynomial_transition_table_count",
                "maximum_dense_matrix_entry_count",
            ],
            dependencies=[
                "coset_two_copy_transition_audit.py",
                "coset_two_copy_frame.py",
                "symmetric_character.py",
            ],
            next_actions=[
                "Derive transition traces from recoupling coefficients without constructing the regular tensor space.",
                "Separate multiplicity-free or Gelfand-pair cases from genuinely noncommuting symmetric-group classes.",
                "Reject the route if transition data or outcome decoding has unavoidable factorial description size.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-THREE-COPY-RECOUPLING-OBSTRUCTION",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Three-copy overlapping-recoupling obstruction theorem",
            status="planned",
            hypothesis=(
                "A single recursively chosen Kronecker basis may diagonalize the three-copy involution frame and "
                "extend the two-copy spectrum into an efficient collective measurement."
            ),
            protocol=(
                "Construct exact standard-representation pair class sums on overlapping tensor factors, prove or "
                "falsify commutation, audit full three-copy standard blocks, and retain exceptional commuting classes "
                "as controls."
            ),
            positive_signal=(
                "Despite overlapping noncommutation, a uniform polynomial Racah/associator circuit and compressed "
                "multiplicity-space decoder handle k growing with n."
            ),
            falsifiers=[
                "Overlapping pair class sums have an all-n nonzero commutator.",
                "A proposed measurement assumes one pairwise recoupling basis diagonalizes every subset term.",
                "Associator data or multiplicity spaces require superpolynomial description or circuit size.",
                "Only an exceptional commuting class supports the simplified construction.",
            ],
            metrics=[
                "single_transposition_all_n_theorem_row_count",
                "noncommuting_overlapping_pair_count",
                "commuting_class_control_count",
                "uniform_coherent_associator_count",
                "polynomial_multiplicity_space_decoder_count",
                "maximum_three_copy_block_dimension",
            ],
            dependencies=[
                "coset_three_copy_recoupling_obstruction.py",
                "coset_two_copy_transition_audit.py",
                "symmetric_character.py",
            ],
            next_actions=[
                "Construct uniform symmetric-group Racah transforms with explicit gate and conditioning bounds.",
                "Represent multiplicity spaces without Young-tableau or conjugacy-class enumeration.",
                "Prove a decoder theorem or use the obstruction to terminate the naive recursive-recoupling route.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-JUCYS-MURPHY-LABEL-TRANSFORM",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Diagonal Young--Jucys--Murphy label-transform boundary",
            status="planned",
            hypothesis=(
                "The diagonal Young--Jucys--Murphy algebra isolates a uniform polynomial target-tableau label "
                "transform while exposing Kronecker multiplicity-space control as the narrower unresolved operation."
            ),
            protocol=(
                "Construct exact seminormal S_n representations, diagonal YJM operators on selected tensor sectors, "
                "verify Coxeter and commutation relations, and compare their complete encoded spectrum with exact "
                "Kronecker coefficients and tableau content vectors. Separately audit the uniform QFT/group-action/"
                "block-encoding circuit contract."
            ),
            positive_signal=(
                "Target tableau labels are uniformly measurable with polynomial resources and the remaining "
                "multiplicity-space operation has a precise state interface that can be attacked independently."
            ),
            falsifiers=[
                "The seminormal matrices fail Coxeter relations or the diagonal YJM operators fail to commute.",
                "The joint spectrum does not reproduce exact Kronecker multiplicity degeneracies.",
                "The uniform circuit silently uses finite tableau enumeration or dense diagonalization.",
                "Tableau labels are promoted as a multiplicity basis, associator, or hidden-involution decoder.",
            ],
            metrics=[
                "finite_label_spectrum_verified_count",
                "nontrivial_multiplicity_witness_count",
                "diagonal_jm_label_poly_contract_count",
                "coherent_multiplicity_basis_count",
                "kcopy_associator_count",
                "hidden_involution_decoder_count",
                "maximum_encoded_spectrum_residual",
            ],
            dependencies=[
                "coset_jucys_murphy_label_transform.py",
                "symmetric_character.py",
                "representation_obstruction.py",
                "efficient S_n QFT and block-encoding primitives",
            ],
            next_actions=[
                "Construct a coherent basis inside the residual Kronecker multiplicity spaces without tableau enumeration.",
                "Derive multiplicity-space Racah moves and transition-filter matrix elements for overlapping copy subsets.",
                "Require an end-to-end hidden-involution decoder before any speedup claim.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-MULTIPLICITY-COMMUTANT-SEARCH",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Bounded-support Kronecker multiplicity commutant search",
            status="planned",
            hypothesis=(
                "Polynomial-description simultaneous-conjugacy orbit sums may define a nontrivial Hermitian "
                "commutant Hamiltonian with resolvable spectrum inside every YJM-degenerate multiplicity register."
            ),
            protocol=(
                "Build disjoint transposition-pair and support-stratified transposition/3-cycle orbit sums, verify "
                "diagonal S_n commutation, search small-integer Hermitian combinations, and charge every LCU term, "
                "normalization factor, multiplicity eigenvalue gap, and target-tableau consistency check."
            ),
            positive_signal=(
                "A uniform family has a proved inverse-polynomial LCU-normalized gap on every reduction-relevant "
                "Kronecker sector and composes with polynomial associators and decoding."
            ),
            falsifiers=[
                "Bounded-support orbit generators remain scalar on a growing multiplicity subspace.",
                "The minimum LCU-normalized gap shrinks superpolynomially with n.",
                "A claimed implementation materializes dense tableau matrices or factorial group orbits.",
                "A one-coupling multiplicity basis is relabeled as an overlapping associator or decoder.",
            ],
            metrics=[
                "bounded_support_commutant_block_encoding_count",
                "finite_all_block_split_count",
                "inverse_polynomial_gap_theorem_count",
                "coherent_polynomial_multiplicity_transform_count",
                "minimum_observed_lcu_normalized_gap",
                "kcopy_associator_count",
                "hidden_involution_decoder_count",
            ],
            dependencies=[
                "coset_multiplicity_commutant_search.py",
                "coset_jucys_murphy_label_transform.py",
                "symmetric_character.py",
                "LCU/block encoding and phase estimation",
            ],
            next_actions=[
                "Derive exact multiplicity spectra for bounded-support orbit Hamiltonians as functions of partitions.",
                "Prove or falsify inverse-polynomial normalized gaps on balanced Plancherel-relevant sectors.",
                "Construct coherent Racah matrices between multiplicity bases only after the gap theorem survives.",
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-RECOUPLING-CAPABILITY-LEDGER",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Literature-backed symmetric-group recoupling capability ledger",
            status="planned",
            hypothesis=(
                "Existing efficient S_n Fourier, Schur, projection, or multiplicity primitives may already implement "
                "enough of the collective coset-state measurement to close the recoupling proof debt."
            ),
            protocol=(
                "Separate each literature-backed primitive by exact group action, promise, output, gate theorem, "
                "multiplicity handling, associator scope, decoder role, and classical comparison; compute finite exact "
                "Kronecker growth only as a stress test."
            ),
            positive_signal=(
                "A cited uniform polynomial theorem implements the internal S_n Kronecker transform, overlapping "
                "k-copy associators, state transitions, and a reduction-compatible hidden-involution decoder."
            ),
            falsifiers=[
                "An efficient S_n QFT is relabeled as an internal Kronecker transform.",
                "Multiplicity counting or irrep projection is relabeled as a coherent basis transform.",
                "A Schur-Weyl/U(d) transform is applied to arbitrary internal Specht tensor products without proof.",
                "Restricted multiplicity estimation is promoted despite polynomial classical algorithms.",
                "Large finite dimensions or multiplicities are treated as circuit lower bounds.",
            ],
            metrics=[
                "proved_polynomial_primitive_count",
                "internal_kronecker_transform_poly_proof_count",
                "kcopy_associator_poly_proof_count",
                "hidden_involution_decoder_count",
                "unresolved_required_capability_count",
                "restricted_multiplicity_classical_match_count",
                "maximum_kronecker_multiplicity",
            ],
            dependencies=[
                "coset_recoupling_capability_ledger.py",
                "literature_radar.py",
                "literature_pipeline.py",
                "symmetric_character.py",
            ],
            next_actions=[
                "Search specifically for uniform internal S_n Kronecker transform circuit theorems, not generic QFT results.",
                "Extract gate, precision, multiplicity, and promise bounds from any claimed recoupling construction.",
                "Require a hidden-involution decoder and classical comparison before promoting a solved primitive."
            ],
        ),
        ExperimentRecord(
            id="EXP-COSET-RECOUPLING-MECHANISM-SYNTHESIS",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Typed symmetric-group recoupling mechanism synthesis",
            status="planned",
            hypothesis=(
                "A collective hidden-involution algorithm can be assembled from scope-matched representation "
                "primitives without silently replacing an open recoupling transform or decoder by an oracle box."
            ),
            protocol=(
                "Compose candidate mechanisms through typed state interfaces, attach capability-ledger dependencies, "
                "reject known Fourier/counting/rank shortcuts, and retain only architectures whose missing operations "
                "are explicit proof obligations."
            ),
            positive_signal=(
                "A full-family architecture has a valid typed chain, no known no-go violation, uniform polynomial "
                "proofs for every primitive, and an end-to-end hidden-involution decoder."
            ),
            falsifiers=[
                "Weak or strong Fourier labels are used as the decoder despite the symmetric-HSP no-go barrier.",
                "Multiplicity counting is substituted for a coherent internal Kronecker transform.",
                "A two-copy rank formula or one recoupling tree is extended through the known finite/all-n counterexamples.",
                "An exceptional commuting or classically tractable family is substituted for the reduction source family.",
                "Any proof-critical operation remains an undefined circuit box.",
            ],
            metrics=[
                "mechanism_count",
                "typed_interface_valid_count",
                "known_no_go_rejected_count",
                "proposal_only_count",
                "proof_gate_eligible_count",
                "automatically_promoted_candidate_count",
                "minimum_missing_capability_count",
            ],
            dependencies=[
                "coset_recoupling_mechanism_synthesis.py",
                "coset_recoupling_capability_ledger.py",
                "coset_three_copy_recoupling_obstruction.py",
                "coset_two_copy_transition_audit.py",
            ],
            next_actions=[
                "Attack the full recoupling/transition/decoder architecture one missing capability at a time.",
                "Search for tensor-network associators only with uniform bond, precision, and dequantization bounds.",
                "Promote no mutation until every typed primitive and the source-family decoder pass the proof gate.",
            ],
        ),
        ExperimentRecord(
            id="EXP-CODE-TENSOR-MEASUREMENT",
            candidate_id="CODE-COSET-COLLECTIVE",
            title="Tensor-network collective measurement ansatz",
            status="planned",
            hypothesis="A polynomial-bond ansatz separates coset states missed by single-register tests.",
            protocol="Optimize k-register tensor-network observables over generated instances and compare against classical invariants.",
            positive_signal="Bond dimension remains polynomial while distinguishing advantage remains inverse polynomial.",
            falsifiers=["Bond dimension grows exponentially.", "Observable matches a classical invariant.", "Signal vanishes on larger families."],
            metrics=["bond_dimension", "distinguishing_advantage", "register_count", "classical_invariant_overlap"],
            dependencies=["tensor-network backend", "representation labels"],
            next_actions=["Choose tensor backend.", "Define observable serialization."],
        ),
    ]
    return candidates, experiments


def initialize_seed_registry(overwrite: bool = False) -> None:
    candidates, experiments = seed_candidate_records()
    if overwrite or not CANDIDATES_PATH.exists():
        save_candidates([])
        for candidate in candidates:
            upsert_candidate(candidate)
    else:
        existing_candidates = load_candidates()
        changed = False
        for seed_candidate in candidates:
            for index, existing in enumerate(existing_candidates):
                if existing.get("id") != seed_candidate.id:
                    continue
                refreshed = asdict(seed_candidate)
                refreshed["created_at"] = existing.get("created_at", refreshed["created_at"])
                refreshed["experiment_ids"] = list(
                    dict.fromkeys(seed_candidate.experiment_ids + list(existing.get("experiment_ids", [])))
                )
                old_substantive = {key: value for key, value in existing.items() if key not in {"created_at", "updated_at"}}
                new_substantive = {key: value for key, value in refreshed.items() if key not in {"created_at", "updated_at"}}
                if old_substantive != new_substantive:
                    refreshed["updated_at"] = utc_now()
                    existing_candidates[index] = refreshed
                    changed = True
        if changed:
            existing_candidates.sort(key=lambda item: item.get("id", ""))
            save_candidates(existing_candidates)
        existing_candidate_ids = {candidate.get("id") for candidate in load_candidates()}
        for candidate in candidates:
            if candidate.id not in existing_candidate_ids:
                upsert_candidate(candidate)
    if overwrite or not EXPERIMENTS_PATH.exists():
        save_experiments([])
        for experiment in experiments:
            upsert_experiment(experiment)
    else:
        for experiment in experiments:
            upsert_experiment(experiment)
    if not EXPERIMENT_RESULTS_PATH.exists():
        save_experiment_results([])
    if not DEQUANTIZATION_CHECKS_PATH.exists():
        save_dequantization_checks([])
    if not PROOF_STATUS_PATH.exists():
        save_proof_status([])
    if not SCALING_RUNS_PATH.exists():
        save_scaling_runs([])
    if not CONJECTURES_PATH.exists():
        save_conjectures([])
    if not MUTATION_PROPOSALS_PATH.exists():
        save_mutation_proposals([])
    if not NEGATIVE_RESULTS_PATH.exists():
        save_negative_results([])
    if not REJECTED_CANDIDATES_PATH.exists():
        save_rejected_candidates([])
    if overwrite or not REDUCTIONS_PATH.exists():
        save_reduction_ledger({})


def negative_results_from_legacy(root: Path) -> list[NegativeResultRecord]:
    results_dir = root / "results"
    if not results_dir.exists():
        return []
    records: list[NegativeResultRecord] = []
    for proposal_path in sorted(results_dir.glob("*/proposal.json")):
        run_dir = proposal_path.parent
        try:
            proposal = json.loads(proposal_path.read_text())
            analysis = json.loads((run_dir / "analysis.json").read_text())
            scaling = json.loads((run_dir / "scaling.json").read_text())
        except (OSError, json.JSONDecodeError):
            continue

        max_success = max((float(item.get("success_rate", 0.0) or 0.0) for item in scaling), default=0.0)
        speedup = str(analysis.get("speedup_type", "missing"))
        problem_name = proposal.get("problem_name") or run_dir.name
        claimed = speedup not in {"None", "missing", "Unsubstantiated"}
        invalid_reason = []
        if proposal.get("problem_type") == "oracle_secret_finding":
            invalid_reason.append("arbitrary oracle_secret_finding proposal")
        if proposal.get("max_qubits_to_simulate") == 3:
            invalid_reason.append("N=3 simulation cap")
        if max_success == 0.0 and claimed:
            invalid_reason.append("claimed speedup despite zero simulation success")
        if "secret" in f"{problem_name} {proposal.get('description', '')}".lower():
            invalid_reason.append("secret-finding framing with no natural scalable family")

        if invalid_reason:
            records.append(
                NegativeResultRecord(
                    id=f"LEGACY-{run_dir.name.upper().replace('-', '_')}",
                    source=str(run_dir),
                    claim=f"{problem_name}: {speedup}",
                    reason_invalid="; ".join(invalid_reason),
                    lesson="Do not accept tiny custom-oracle runs as evidence of algorithmic speedup.",
                    applies_to=["NO-TOY-ORACLE", "PO-FAMILY", "PO-CLASSICAL-BASELINE", "PO-FALSIFIERS"],
                    evidence={
                        "problem_type": proposal.get("problem_type"),
                        "max_qubits_to_simulate": proposal.get("max_qubits_to_simulate"),
                        "max_success_rate": max_success,
                        "claimed_speedup": speedup,
                        "description": proposal.get("description", ""),
                    },
                )
            )
    return records


def import_legacy_negative_results(root: Path) -> int:
    records = negative_results_from_legacy(root)
    for record in records:
        upsert_negative_result(record)
    return len(records)


def validate_registry() -> dict[str, Any]:
    candidates = load_candidates()
    issues = []
    for candidate in candidates:
        for issue in validate_candidate_record(candidate):
            issues.append({"candidate_id": candidate.get("id", "unknown"), **issue_to_dict(issue)})
    experiment_candidate_ids = {candidate["id"] for candidate in candidates}
    experiment_ids = {experiment["id"] for experiment in load_experiments()}
    for experiment in load_experiments():
        if experiment.get("candidate_id") not in experiment_candidate_ids:
            issues.append(
                {
                    "candidate_id": experiment.get("candidate_id", "unknown"),
                    "obligation_id": "REGISTRY",
                    "field": "candidate_id",
                    "message": f"Experiment {experiment.get('id')} references a missing candidate.",
                    "hard_reject": True,
                }
            )
        if not experiment.get("falsifiers"):
            issues.append(
                {
                    "candidate_id": experiment.get("candidate_id", "unknown"),
                    "obligation_id": "PO-FALSIFIERS",
                    "field": "falsifiers",
                    "message": f"Experiment {experiment.get('id')} has no falsifiers.",
                    "hard_reject": True,
                }
            )
    for result in load_experiment_results():
        if result.get("experiment_id") not in experiment_ids:
            issues.append(
                {
                    "candidate_id": result.get("candidate_id", "unknown"),
                    "obligation_id": "REGISTRY",
                    "field": "experiment_id",
                    "message": f"Experiment result {result.get('id')} references a missing experiment.",
                    "hard_reject": True,
                }
            )
    reduction_ledger = load_reduction_ledger()
    for edge in reduction_ledger.get("edges", []):
        certificate = edge.get("certificate", {})
        if certificate.get("candidate_id") not in experiment_candidate_ids:
            issues.append(
                {
                    "candidate_id": certificate.get("candidate_id", "unknown"),
                    "obligation_id": "PO-REDUCTION",
                    "field": "candidate_id",
                    "message": f"Reduction edge {certificate.get('id')} references a missing candidate.",
                    "hard_reject": True,
                }
            )
        if edge.get("accepted") and edge.get("issues"):
            issues.append(
                {
                    "candidate_id": certificate.get("candidate_id", "unknown"),
                    "obligation_id": "PO-REDUCTION",
                    "field": "issues",
                    "message": f"Accepted reduction edge {certificate.get('id')} still has gate issues.",
                    "hard_reject": True,
                }
            )
    return {
        "candidate_count": len(candidates),
        "experiment_count": len(load_experiments()),
        "experiment_result_count": len(load_experiment_results()),
        "dequantization_check_count": len(load_dequantization_checks()),
        "proof_status_count": len(load_proof_status()),
        "scaling_run_count": len(load_scaling_runs()),
        "conjecture_count": len(load_conjectures()),
        "mutation_proposal_count": len(load_mutation_proposals()),
        "negative_result_count": len(load_negative_results()),
        "rejected_candidate_count": len(load_rejected_candidates()),
        "reduction_edge_count": len(reduction_ledger.get("edges", [])),
        "reduction_route_count": len(reduction_ledger.get("routes", [])),
        "issues": issues,
        "valid": not issues,
    }


def registry_summary() -> str:
    validation = validate_registry()
    lines = [
        f"Candidates: {validation['candidate_count']}",
        f"Experiments: {validation['experiment_count']}",
        f"Experiment results: {validation['experiment_result_count']}",
        f"Dequantization checks: {validation['dequantization_check_count']}",
        f"Proof statuses: {validation['proof_status_count']}",
        f"Scaling runs: {validation['scaling_run_count']}",
        f"Conjectures: {validation['conjecture_count']}",
        f"Mutation proposals: {validation['mutation_proposal_count']}",
        f"Negative results: {validation['negative_result_count']}",
        f"Rejected candidates: {validation['rejected_candidate_count']}",
        f"Reduction edges: {validation['reduction_edge_count']}",
        f"Reduction routes: {validation['reduction_route_count']}",
        f"Valid: {validation['valid']}",
    ]
    for candidate in load_candidates():
        lines.append(f"- {candidate['id']}: {candidate['title']} [{candidate['status']}]")
    return "\n".join(lines)
