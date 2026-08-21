"""Exhaustive research-lab audit and intervention planner.

This file is intentionally opinionated.  It treats the repository as a research
instrument and asks which changes most increase the expected probability of a
Shor-level algorithmic contribution.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from literature_radar import build_literature_index, write_literature_index
from problem_ontology import build_problem_ontology, write_problem_ontology


@dataclass(frozen=True)
class Improvement:
    id: str
    title: str
    category: str
    expected_breakthrough_lift: float
    difficulty: str
    dependencies: list[str]
    why_it_matters: str
    likely_failure_modes: list[str]
    falsifying_evidence: list[str]
    implementation_status: str


@dataclass(frozen=True)
class ModuleDecision:
    path: str
    decision: str
    reason: str
    replacement: str


@dataclass(frozen=True)
class ProofObligation:
    id: str
    obligation: str
    why_required: str
    reject_if_missing: bool


@dataclass(frozen=True)
class CritiquePass:
    target: str
    likely_to_fail_because: list[str]
    core_assumptions: list[str]
    falsifiers: list[str]
    revised_recommendation: str


def proposed_improvements() -> list[Improvement]:
    return [
        Improvement(
            "IMP-LITERATURE-KG",
            "Living literature knowledge graph with technique extraction",
            "literature",
            9.7,
            "High",
            ["arXiv API", "paper parser", "embedding/search index", "human curation"],
            "Breakthrough work is usually recombination of known mechanisms and unresolved barriers; the project needs memory of the field.",
            ["Extraction summarizes papers without capturing proof constraints.", "The graph becomes a bibliography instead of a source of hypotheses."],
            ["New leads are not traceable to papers or barriers.", "Researchers cannot query for analogous proof techniques across domains."],
            "Seeded by literature_radar.py; full parser/search still needed.",
        ),
        Improvement(
            "IMP-PROOF-GATE",
            "Proof-obligation gate for every candidate algorithm",
            "evaluation",
            9.6,
            "Medium",
            ["structured schemas", "complexity model", "review workflow"],
            "Prevents the system from recording unsupported speedup claims and forces scalable problem families, reductions, and cost accounting.",
            ["The gate becomes paperwork and blocks speculative ideas too early.", "Generated proof sketches remain unchecked."],
            ["Candidates pass without input model, lower-bound target, or oracle/state-preparation costs."],
            "Basic enforcement implemented in proof_gate.py; candidate generation still needs to call it by default.",
        ),
        Improvement(
            "IMP-REDUCTION-ONTOLOGY",
            "Problem and reduction ontology with no-go barriers",
            "mathematical representation",
            9.4,
            "Medium",
            ["curated reductions", "negative-result database", "graph search"],
            "Shor-level algorithms come from reductions and structural reframings; a circuit search cannot see that.",
            ["Ontology freezes current beliefs and misses unconventional routes.", "Edges are too informal for automated reasoning."],
            ["A proposed lead can ignore known no-go barriers without being flagged."],
            "Implemented in problem_ontology.py with first reduction/barrier graph.",
        ),
        Improvement(
            "IMP-REP-THEORY-LAB",
            "Representation-theory and coset-state laboratory",
            "experiment",
            9.2,
            "Extreme",
            ["SageMath", "GAP", "character tables", "tensor-network backend"],
            "Nonabelian HSP, GI, and code equivalence require irreps, coset states, and collective measurements, not qubit-level BFS.",
            ["Known no-go results dominate.", "Interesting measurements require exponential classical preprocessing."],
            ["All observables collapse to strong Fourier sampling or classical refinement invariants."],
            "Not yet implemented beyond coset fingerprint smoke metrics.",
        ),
        Improvement(
            "IMP-HSHIFT-SIEVE",
            "Hidden-shift and dihedral phase-state sieve workbench",
            "experiment",
            9.0,
            "High",
            ["finite abelian group library", "phase-state simulator", "sieve optimizer"],
            "This is one of the few frontier zones with a known subexponential quantum algorithm and lattice implications.",
            ["Structured families are classically easy.", "Generic subset-sum hardness reappears."],
            ["Sieve scaling matches Kuperberg/Regev with no structural improvement.", "A classical correlation attack recovers the shift."],
            "Partially supported by hidden_shift_metrics and new Gowers/derivative tests.",
        ),
        Improvement(
            "IMP-ADVERSARY-SPAN",
            "Adversary-bound SDP and span-program synthesizer",
            "query complexity",
            8.8,
            "High",
            ["CVXPY or MOSEK", "span-program compiler", "Boolean function family generator"],
            "Span programs convert query lower-bound structure into algorithms; this is a principled alternative to random circuit search.",
            ["Only produces oracle separations.", "SDPs scale poorly and yield uninterpretable witnesses."],
            ["Witnesses do not generalize across n.", "No explicit problem family survives the proof-obligation gate."],
            "Not implemented; should replace most oracle-circuit search.",
        ),
        Improvement(
            "IMP-COUNTEREXAMPLE-ENGINE",
            "Conjecture and counterexample engine",
            "proof workflow",
            8.5,
            "High",
            ["SAT/SMT", "SymPy/Sage", "finite model generators"],
            "Research progress often comes from killing false conjectures cheaply and finding the exact boundary of a phenomenon.",
            ["Search spaces are too arbitrary.", "Counterexamples do not scale or teach structure."],
            ["Conjectures lack formal predicates.", "No generated counterexample changes a research lead."],
            "Not implemented.",
        ),
        Improvement(
            "IMP-TENSOR-MEASUREMENTS",
            "Tensor-network search for multi-register measurements",
            "quantum information",
            8.4,
            "Extreme",
            ["quimb or opt_einsum", "representation labels", "optimization backend"],
            "Known barriers suggest single-register sampling is too weak; tensor networks are the plausible classical tool for exploring collective measurements.",
            ["Bond dimension grows exponentially.", "Optimized measurement has no clean mathematical description."],
            ["No polynomial-bond ansatz separates hard instances.", "Success relies on memorizing small instances."],
            "Not implemented.",
        ),
        Improvement(
            "IMP-CLASSICAL-BASELINE",
            "Classical baseline and dequantization checker",
            "evaluation",
            8.3,
            "Medium",
            ["classical algorithm registry", "complexity annotations", "randomized estimator library"],
            "Most false quantum speedups hide in weak baselines, data loading, or low-rank dequantization.",
            ["Baselines are incomplete.", "The checker rejects speculative leads without proof."],
            ["A claimed speedup survives only against brute force.", "Classical randomized estimators match the proposed quantum invariant."],
            "Specified in proof obligations; checker not yet implemented.",
        ),
        Improvement(
            "IMP-GOWERS-HARMONIC",
            "Higher-order Fourier and Gowers-uniformity testbed",
            "harmonic analysis",
            8.1,
            "Medium",
            ["finite fields", "fast transforms", "property-testing datasets"],
            "Large-Gowers-norm hidden shift algorithms show that higher-order harmonic analysis can be a real algorithmic handle.",
            ["Only rediscovers known quadratic cases.", "High Gowers norm correlates with classical learnability."],
            ["Derivative spectra are sparse only for classically learnable families."],
            "Implemented exact small-instance U^k and derivative spectrum metrics.",
        ),
        Improvement(
            "IMP-LATTICE-INFRASTRUCTURE",
            "Lattice and algebraic-number-theory periodicity workbench",
            "number theory",
            8.0,
            "Extreme",
            ["SageMath", "PARI/GP", "lattice reduction", "reversible arithmetic cost model"],
            "Hallgren/Regev-style ideas show hidden periodicity in number theory is one of the best places to hunt.",
            ["Maps are not efficiently reversible.", "Classical lattice reduction exploits the same structure."],
            ["Period ridges require exponential precision.", "No reduction to a hard lattice problem is found."],
            "Not implemented.",
        ),
        Improvement(
            "IMP-QSVT-COST-CALCULUS",
            "QSVT/block-encoding cost calculus",
            "linear algebra",
            7.7,
            "High",
            ["matrix access model schema", "polynomial approximation tools", "classical randomized baseline"],
            "QSVT is powerful but dangerous: many apparent speedups disappear once encoding and precision are counted.",
            ["Focus drifts to incremental primitive optimization.", "Input model assumptions dominate everything."],
            ["No candidate invariant survives data-loading and dequantization checks."],
            "Not implemented.",
        ),
        Improvement(
            "IMP-TECHNIQUE-RECOMBINATION",
            "Cross-paper technique recombination engine",
            "hypothesis generation",
            7.6,
            "High",
            ["literature KG", "LLM hypothesis generator", "red-team verifier"],
            "The system should ask questions like: can the proof trick from hidden shift apply to code equivalence?",
            ["Produces plausible nonsense.", "Recombinations ignore theorem assumptions."],
            ["Generated analogies cannot state proof obligations or falsifiers."],
            "Not implemented.",
        ),
        Improvement(
            "IMP-REDUCTION-MINER",
            "Reduction miner using symbolic unification",
            "mathematics",
            7.5,
            "Extreme",
            ["SMT", "Lean", "Sage", "domain schemas"],
            "A new reduction can be as valuable as a new circuit; reductions define what a breakthrough would affect.",
            ["Formalizing domains costs more than the search.", "Generated reductions are too weak or circular."],
            ["No nontrivial reduction can be machine-checked on finite models."],
            "Not implemented.",
        ),
        Improvement(
            "IMP-KNOWN-ALGO-REGRESSION",
            "Benchmark suite of known algorithms and no-go barriers",
            "validation",
            7.3,
            "Medium",
            ["canonical instances", "expected structural signatures", "negative tests"],
            "A discovery engine must rediscover Shor/Simon/Hallgren mechanisms and fail on known-dead strategies before being trusted.",
            ["Benchmarks reward imitation over novelty.", "Negative tests are too narrow."],
            ["The engine scores toy BV variants higher than known frontier problems."],
            "Partially implemented through audit diagnostics; benchmark suite still needed.",
        ),
        Improvement(
            "IMP-LLM-REDTEAM",
            "Multi-agent hypothesis generation with adversarial review",
            "workflow",
            7.1,
            "Medium",
            ["LLM", "structured schemas", "critique prompts", "literature KG"],
            "LLMs are useful for breadth, but only with red-team critique and hard gates.",
            ["Agents converge on fashionable buzzwords.", "Critique is rhetorical rather than mathematical."],
            ["Claims are not linked to papers, reductions, or experiments."],
            "Not implemented; old Theorist/Analyzer should be deleted rather than extended.",
        ),
        Improvement(
            "IMP-SCHEMA-PROGRAM-SYNTHESIS",
            "Program synthesis over algorithm schemas, not gate sequences",
            "automation",
            6.9,
            "High",
            ["DSL for algorithms", "typed transformations", "symbolic executor"],
            "Searching over QFT/phase-estimation/walk/QSVT schemas has far higher ceiling than raw gates.",
            ["DSL misses the next paradigm.", "Search still overfits tiny examples."],
            ["Synthesized schema lacks a proof path or scalable invariant."],
            "Not implemented.",
        ),
        Improvement(
            "IMP-SCALING-BAYES",
            "Scaling-law experiment manager with Bayesian model comparison",
            "experiment",
            6.8,
            "Medium",
            ["experiment database", "statistical model fitting"],
            "Finite experiments matter only if they compare asymptotic hypotheses and fail fast.",
            ["Small-n data remains misleading.", "Wrong model class gives false optimism."],
            ["Positive signals disappear under larger generated families."],
            "Not implemented.",
        ),
        Improvement(
            "IMP-FORMAL-VERIFY",
            "Formal verification path for candidate algorithms",
            "proof workflow",
            6.7,
            "Extreme",
            ["Lean", "SQIR/QWIRE", "linear algebra libraries"],
            "A serious system should eventually prove circuit identities and reductions, not trust prose.",
            ["Formalization overhead overwhelms ideation.", "Proof assistant libraries lack required mathematics."],
            ["Only trivial circuits can be verified."],
            "Not implemented.",
        ),
        Improvement(
            "IMP-WALK-GEOMETRY",
            "Quantum-walk geometry analyzer",
            "experiment",
            6.6,
            "High",
            ["graph generators", "spectral tools", "conductance estimators"],
            "Walk algorithms need geometry; this checks whether state spaces beat Grover before algorithm design.",
            ["Spectral proxies do not imply implementable walks.", "Classical walks improve similarly."],
            ["Gap-overlap product never beats amplitude amplification."],
            "Basic spectral metric exists; full analyzer not implemented.",
        ),
        Improvement(
            "IMP-FINITE-FIELD-FAMILIES",
            "Finite-field and algebraic-geometry family generator",
            "mathematics",
            6.5,
            "High",
            ["SageMath", "finite fields", "algebraic curves"],
            "Explicit families are the raw material for hidden shift, property testing, and code-equivalence experiments.",
            ["Families are classically easy.", "Generated structures have no hard baseline."],
            ["No family passes classical-baseline and proof-obligation gates."],
            "Not implemented.",
        ),
        Improvement(
            "IMP-CODE-GI-INSTANCES",
            "Hard instance generators for code equivalence and graph isomorphism",
            "benchmarks",
            6.4,
            "High",
            ["Magma/Sage/GAP", "nauty/traces", "coding theory library"],
            "Without hard families, coset-state experiments are meaningless.",
            ["Generated instances are easy for classical tools.", "Automorphism promises remove hardness."],
            ["Classical canonicalization solves all generated families quickly."],
            "Not implemented.",
        ),
        Improvement(
            "IMP-DELETE-LEGACY-LOOP",
            "Delete the old tiny-circuit LLM loop",
            "repo hygiene",
            6.2,
            "Low",
            [],
            "It actively creates false confidence and should not remain a first-class path.",
            ["Losing a small sanity-check tool.", "Deletion hides historical mistakes instead of documenting them."],
            ["Any future run produces unsupported speedup claims again."],
            "Recommended; root entrypoint already bypasses it, files still present for now.",
        ),
        Improvement(
            "IMP-QUARANTINE-RESULTS",
            "Quarantine legacy result corpus as negative examples",
            "repo hygiene",
            6.0,
            "Low",
            [],
            "The old outputs are useful only as anti-examples for the proof gate.",
            ["Historical data may be accidentally treated as discoveries.", "Deleting loses negative training data."],
            ["Dashboard presents them as successes."],
            "Partially done through dashboard relabeling; physical quarantine still pending.",
        ),
        Improvement(
            "IMP-SANDBOX-GENERATED-CODE",
            "Sandbox or eliminate generated Python execution",
            "safety/evaluation",
            5.8,
            "Medium",
            ["restricted interpreter", "AST validator"],
            "The current `exec` path is unsafe and scientifically noisy.",
            ["Sandbox engineering distracts from research.", "Better answer is to delete the code path."],
            ["Generated code still controls evaluation without typed semantics."],
            "Not implemented; best resolved by deleting legacy simulator.",
        ),
        Improvement(
            "IMP-REMOVE-DASHBOARD",
            "Remove web dashboard as a central artifact",
            "workflow",
            5.5,
            "Low",
            [],
            "The dashboard incentivizes demos and status optics instead of research progress.",
            ["Loses lightweight visibility into runs.", "A research log still needs a readable surface."],
            ["Dashboard metrics drive decisions instead of proof obligations."],
            "Recommended; wording changed but file remains.",
        ),
        Improvement(
            "IMP-HUMAN-REVIEW",
            "Expert review workflow with decision logs",
            "workflow",
            5.4,
            "Medium",
            ["issue templates", "review rubric", "research notebook"],
            "Breakthrough odds rise when machine-generated hypotheses are aggressively reviewed by humans with field context.",
            ["Becomes bureaucratic.", "Reviews are not tied to experiments."],
            ["Rejected ideas keep returning without new evidence."],
            "Not implemented.",
        ),
        Improvement(
            "IMP-NEGATIVE-RESULTS",
            "Negative-result database",
            "workflow",
            5.2,
            "Medium",
            ["structured failures", "literature links"],
            "Avoiding repeated dead ends is a direct expected-value gain.",
            ["Negative results overgeneralize and block creativity."],
            ["The same toy-oracle or no-go-barrier mistake recurs."],
            "Partially represented by ontology barriers.",
        ),
        Improvement(
            "IMP-ARXIV-MONITOR",
            "Recurring arXiv monitor for quantum algorithms",
            "literature",
            5.0,
            "Medium",
            ["arXiv API", "scheduler", "deduplication"],
            "Current literature can change frontier priorities; the project should notice automatically.",
            ["Noise from irrelevant papers overwhelms signal.", "Summaries are shallow."],
            ["New relevant papers are absent from the knowledge graph for months."],
            "Static seeds implemented; recurring automation not implemented.",
        ),
        Improvement(
            "IMP-RANDOM-MATRIX-INVARIANTS",
            "Random-matrix and spectral invariant search",
            "experiment",
            4.8,
            "High",
            ["linear algebra", "graph/code generators", "classical estimators"],
            "May reveal separations for isomorphism-like problems, but many invariants are classically estimable.",
            ["Produces dequantized invariants.", "Separates only easy instances."],
            ["Classical trace estimators match quantum access-model cost."],
            "Not implemented.",
        ),
        Improvement(
            "IMP-RESOURCE-ESTIMATOR",
            "Fault-tolerant resource estimator",
            "cost model",
            4.2,
            "Medium",
            ["resource estimation library"],
            "Useful after a real candidate exists; not a primary discovery driver.",
            ["Optimizes constants too early.", "Distracts from asymptotic mechanism."],
            ["Used to rank ideas before proof obligations are met."],
            "Not implemented.",
        ),
    ]


def module_decisions() -> list[ModuleDecision]:
    return [
        ModuleDecision("search_engine.py", "delete_or_quarantine", "Depth-5/N<=3 circuit search optimizes the wrong object.", "schema-level and structural experiment engines"),
        ModuleDecision("simulator.py", "delete_or_quarantine", "Only wraps the toy circuit search.", "structural_tests.py and future experiment workbenches"),
        ModuleDecision("theorist.py", "delete", "Prompt-driven toy-problem generation caused the bad result corpus.", "LLM hypothesis generator gated by literature/proof obligations"),
        ModuleDecision("analyzer.py", "delete", "LLM complexity labels from tiny data are actively misleading.", "proof obligation gate plus baseline checker"),
        ModuleDecision("synthesis.py", "delete", "Qiskit snippets are not research contributions.", "algorithm-schema synthesis and formal proof artifacts"),
        ModuleDecision("run_continuous.py", "replace", "A timed loop creates volume, not insight.", "event-driven literature/experiment pipeline"),
        ModuleDecision("index.html/index.js/index.css", "deprioritize_or_remove", "Dashboard polish rewards demos and legacy hits.", "research log generated from audit artifacts"),
        ModuleDecision("results/", "quarantine_as_negative_examples", "The corpus is useful mainly as evidence of failure modes.", "negative-result database"),
        ModuleDecision("history.json", "quarantine_as_negative_examples", "Contains repeated unsupported claims.", "decision log with proof obligations"),
        ModuleDecision("google-cloud-sdk/ and google-cloud-cli.tar.gz", "delete_from_repo", "Vendored 500MB toolchain has no research value.", "document external setup if deployment is ever needed"),
        ModuleDecision("research_engine.py", "keep_and_expand", "Good first agenda generator but still too static.", "research_lab.py plus literature/ontology/counterexample engines"),
        ModuleDecision("structural_tests.py", "keep_and_expand", "Contains relevant early filters.", "add group representation, Gowers, span-program, and lattice tests"),
    ]


def proof_obligations() -> list[ProofObligation]:
    return [
        ProofObligation("PO-FAMILY", "Define an explicit asymptotic problem family.", "Shor-level claims are asymptotic, not small-instance phenomena.", True),
        ProofObligation("PO-INPUT-MODEL", "State the input/oracle/access model exactly.", "Many quantum speedups disappear under realistic data access.", True),
        ProofObligation("PO-CLASSICAL-BASELINE", "Name the best known classical algorithms and hardness evidence.", "Beating brute force is not meaningful.", True),
        ProofObligation("PO-REDUCTION", "Connect the family to a known hard problem, lower-bound target, or frontier reduction.", "This separates natural problems from arbitrary oracle puzzles.", True),
        ProofObligation("PO-MECHANISM", "Identify the quantum mechanism: Fourier, phase estimation, walk, QSVT, span program, collective measurement, etc.", "The mechanism drives both search and proof.", True),
        ProofObligation("PO-STATE-PREP", "Account for state preparation, block encoding, QRAM, precision, and reversible arithmetic.", "Hidden costs often erase the claimed speedup.", True),
        ProofObligation("PO-MEASUREMENT", "Specify the measurement and decoding procedure.", "For nonabelian/coset problems this is usually the hard part.", True),
        ProofObligation("PO-SUCCESS-PROOF", "State a success probability theorem or conjecture with parameters.", "Finite experiments need a proof target.", True),
        ProofObligation("PO-COMPLEXITY", "Separate query, gate, space, precision, and classical postprocessing complexity.", "A query speedup alone may not be an algorithmic speedup.", True),
        ProofObligation("PO-NOGO", "List applicable no-go barriers and how the proposal avoids them.", "Avoids rediscovering known dead ends.", True),
        ProofObligation("PO-DEQUANTIZATION", "Check whether a classical randomized/low-rank/dequantized method matches the claimed advantage.", "Modern quantum linear algebra claims especially need this.", True),
        ProofObligation("PO-FALSIFIERS", "Provide explicit experiments or counterexamples that would kill the idea.", "A research engine must conserve attention.", True),
    ]


def critique_passes() -> list[CritiquePass]:
    return [
        CritiquePass(
            "Nonabelian HSP / code equivalence / graph isomorphism",
            [
                "Known Fourier-sampling barriers are strong and old.",
                "Collective measurements may require exponential entanglement or preprocessing.",
                "Hard instances may have too little representation-theoretic signal.",
            ],
            [
                "There exist structured instance families where collective observables have polynomial descriptions.",
                "Those observables are not equivalent to classical canonicalization or refinement.",
            ],
            [
                "Coset-state distinguishability remains exponentially small under all low-complexity observables tested.",
                "Classical GI/code-equivalence tools solve every generated family.",
            ],
            "Keep as high-upside, but only with no-go-aware measurement search and hard-instance generators.",
        ),
        CritiquePass(
            "Hidden shift / dihedral HSP / lattice route",
            [
                "Generic DHSP has resisted polynomial algorithms for decades.",
                "Structured exceptions may be classically easy.",
                "Approximate lattice periodicity may need infeasible precision.",
            ],
            [
                "There are algebraic hidden-shift distributions with phase-state structure not captured by generic subset-sum hardness.",
                "A sieve improvement can be linked to a meaningful lattice or number-theory problem.",
            ],
            [
                "All families either have simple classical correlation attacks or reduce to generic Kuperberg/Regev scaling.",
                "No reversible map with polynomial precision survives cost audit.",
            ],
            "Keep as top target; add Gowers/derivative tests and phase-sieve simulator before broader speculation.",
        ),
        CritiquePass(
            "Span-program/adversary synthesis",
            [
                "It may produce only oracle/query separations.",
                "SDP witnesses can be opaque and fail to generalize.",
            ],
            [
                "The generated witness has a recursively describable structure.",
                "The query model has a plausible explicit computational analogue.",
            ],
            [
                "Witness size improvements vanish outside handcrafted Boolean functions.",
                "No reduction connects the query family to a natural problem.",
            ],
            "Build it, but force every witness through natural-family and reduction gates.",
        ),
        CritiquePass(
            "QSVT/block-encoding frontier",
            [
                "Most QSVT novelty is incremental or input-model-sensitive.",
                "Classical randomized linear algebra may dequantize the advantage.",
            ],
            [
                "There are structured operators whose spectra are quantum-accessible but classically hard to estimate.",
                "Encoding costs remain below the claimed separation.",
            ],
            [
                "Block encoding dominates total cost.",
                "Classical trace/Lanczos/sketching recovers the same invariant.",
            ],
            "Keep as secondary target with strict cost calculus and dequantization checks.",
        ),
        CritiquePass(
            "LLM-based hypothesis generation",
            [
                "LLMs hallucinate complexity claims and overfit labels like HSP/QFT.",
                "The old corpus proves prompt novelty is not research novelty.",
            ],
            [
                "LLMs are constrained by typed schemas, literature citations, proof obligations, and adversarial review.",
                "Generated leads are evaluated by executable structural tests.",
            ],
            [
                "Generated ideas are not traceable to mechanisms or falsifiers.",
                "The same dead-end families recur with new names.",
            ],
            "Use LLMs only as breadth generators inside a hard-gated research pipeline.",
        ),
    ]


def build_research_audit(agenda: dict[str, Any] | None, root: Path) -> dict[str, Any]:
    improvements = sorted(
        [asdict(item) for item in proposed_improvements()],
        key=lambda item: item["expected_breakthrough_lift"],
        reverse=True,
    )
    return {
        "mission": "Maximize expected contribution to a Shor-level quantum algorithmic breakthrough.",
        "current_project_diagnosis": (agenda or {}).get("diagnosis", {}),
        "capability_gaps": [
            "No living literature ingestion or claim extraction.",
            "No formal problem ontology or reduction search.",
            "No proof-obligation gate before claiming speedups.",
            "No representation-theory toolkit for nonabelian HSP/coset states.",
            "No hidden-shift phase-state or sieve simulator.",
            "No adversary-bound/span-program synthesis.",
            "No hard instance generators for GI/code equivalence/lattice families.",
            "No counterexample search or theorem-proving path.",
            "No classical baseline/dequantization checker.",
            "No experiment database with scaling-law model comparison.",
        ],
        "ranked_improvements": improvements,
        "module_decisions": [asdict(item) for item in module_decisions()],
        "proof_obligations": [asdict(item) for item in proof_obligations()],
        "critique_passes": [asdict(item) for item in critique_passes()],
        "new_architecture": {
            "1_literature_memory": "Continuously ingest papers, extract mechanisms/barriers/reductions, and update a knowledge graph.",
            "2_problem_ontology": "Represent problems, reductions, no-go barriers, and hard families as graph data.",
            "3_hypothesis_factory": "Generate candidates by recombining mechanisms across the ontology, not by inventing oracles.",
            "4_proof_gate": "Reject candidates missing family/input model/baseline/reduction/mechanism/falsifiers.",
            "5_structural_labs": "Run dedicated experiments for HSP/coset states, hidden shift, span programs, walks, QSVT, and Gowers structure.",
            "6_counterexample_loop": "Automatically search small finite models for falsifiers before investing in proof.",
            "7_human_review": "Produce decision logs and questions for expert review instead of dashboard trophies.",
        },
        "implemented_this_pass": [
            "Seed literature radar.",
            "Problem/reduction ontology.",
            "Proof-obligation list.",
            "Ranked intervention portfolio.",
            "Self-critique passes.",
            "Higher-order Fourier/Gowers structural tests.",
        ],
    }


def audit_to_markdown(audit: dict[str, Any]) -> str:
    lines = [
        "# Exhaustive Research Audit",
        "",
        "## Core Verdict",
        "",
        "The project should stop behaving like an autonomous circuit-search demo and become a research lab operating system: literature memory, problem ontology, proof obligations, structural experiment workbenches, counterexample search, and expert review.",
        "",
        "## Capability Gaps",
        "",
    ]
    for gap in audit["capability_gaps"]:
        lines.append(f"- {gap}")

    lines.extend(
        [
            "",
            "## Ranked Improvements",
            "",
            "| Rank | Lift | Difficulty | Improvement | Dependencies | Why it matters |",
            "| ---: | ---: | --- | --- | --- | --- |",
        ]
    )
    for idx, item in enumerate(audit["ranked_improvements"], start=1):
        deps = ", ".join(item["dependencies"]) if item["dependencies"] else "none"
        lines.append(
            f"| {idx} | {item['expected_breakthrough_lift']:.1f} | {item['difficulty']} | "
            f"{item['title']} | {deps} | {item['why_it_matters']} |"
        )

    lines.extend(["", "## Modules To Delete Or Replace", ""])
    for item in audit["module_decisions"]:
        lines.append(
            f"- `{item['path']}`: **{item['decision']}**. {item['reason']} Replacement: {item['replacement']}."
        )

    lines.extend(["", "## Proof Obligations", ""])
    for item in audit["proof_obligations"]:
        severity = "hard reject" if item["reject_if_missing"] else "warning"
        lines.append(f"- `{item['id']}` ({severity}): {item['obligation']} {item['why_required']}")

    lines.extend(["", "## Self-Critique Passes", ""])
    for item in audit["critique_passes"]:
        lines.append(f"### {item['target']}")
        lines.append("Likely to fail because:")
        for value in item["likely_to_fail_because"]:
            lines.append(f"- {value}")
        lines.append("Assumptions:")
        for value in item["core_assumptions"]:
            lines.append(f"- {value}")
        lines.append("Falsifiers:")
        for value in item["falsifiers"]:
            lines.append(f"- {value}")
        lines.append(f"Revised recommendation: {item['revised_recommendation']}")
        lines.append("")

    lines.extend(["## Replacement Architecture", ""])
    for key, value in audit["new_architecture"].items():
        lines.append(f"- **{key}**: {value}")
    lines.append("")
    return "\n".join(lines)


def write_research_audit(agenda: dict[str, Any] | None, root: Path, output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    audit = build_research_audit(agenda, root)
    audit_json = output_dir / "exhaustive_audit.json"
    audit_md = output_dir / "exhaustive_audit.md"
    interventions_json = output_dir / "interventions.json"
    obligations_json = output_dir / "proof_obligations.json"
    ontology_json = output_dir / "problem_ontology.json"
    literature_json = output_dir / "literature_index.json"

    audit_json.write_text(json.dumps(audit, indent=2, sort_keys=True))
    audit_md.write_text(audit_to_markdown(audit))
    interventions_json.write_text(json.dumps(audit["ranked_improvements"], indent=2, sort_keys=True))
    obligations_json.write_text(json.dumps(audit["proof_obligations"], indent=2, sort_keys=True))
    write_problem_ontology(ontology_json)
    write_literature_index(literature_json, refresh_arxiv=False)

    return {
        "audit_json": str(audit_json),
        "audit_markdown": str(audit_md),
        "interventions_json": str(interventions_json),
        "proof_obligations_json": str(obligations_json),
        "problem_ontology_json": str(ontology_json),
        "literature_index_json": str(literature_json),
    }


if __name__ == "__main__":
    paths = write_research_audit(None, Path.cwd(), Path("research"))
    print(json.dumps(paths, indent=2))
