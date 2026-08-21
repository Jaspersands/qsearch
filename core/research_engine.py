"""Research engine for high-upside quantum algorithm search.

The goal is not to synthesize tiny circuits.  The goal is to keep a ranked,
falsifiable research agenda aimed at structural mechanisms that could plausibly
lead to a major quantum speedup.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

from structural_tests import (
    as_jsonable,
    coset_fingerprint_metrics,
    fourier_metrics,
    hidden_shift_metrics,
    periodicity_metrics,
    truth_table_from_boolean,
    walk_spectral_metrics,
)


TOY_PATTERNS = (
    "bernstein",
    "vazirani",
    "deutsch",
    "jozsa",
    "ghz",
    "w state",
    "standalone state preparation",
    "unitary synthesis task",
    "custom nonlinear oracle",
    "custom non-linear oracle",
    "secret bitstring",
    "secret finding",
    "3 qubit",
    "n = 3",
    "tiny circuit",
)


STRUCTURAL_HANDLE_PATTERNS = (
    "fourier",
    "coset",
    "representation",
    "phase estimation",
    "period",
    "hidden shift",
    "hidden subgroup",
    "quantum walk",
    "block-encoding",
    "hamiltonian",
    "tensor",
    "sieve",
    "pretty good measurement",
    "collective measurement",
)


CLASSICAL_BARRIER_PATTERNS = (
    "worst-case",
    "average-case",
    "lower bound",
    "query lower bound",
    "lattice",
    "code equivalence",
    "graph isomorphism",
    "nonabelian",
    "symmetric group",
    "dihedral",
    "exponential",
    "subexponential",
    "hard distribution",
)


@dataclass(frozen=True)
class Domain:
    id: str
    name: str
    upside: int
    why_high_upside: str
    known_barriers: list[str]
    useful_handles: list[str]


@dataclass(frozen=True)
class Experiment:
    id: str
    title: str
    protocol: str
    positive_signal: str
    kill_criteria: str
    upside_rank: int


@dataclass(frozen=True)
class Candidate:
    id: str
    title: str
    domain_ids: list[str]
    hypothesis: str
    problem_family: str
    proposed_quantum_mechanism: str
    classical_barrier: str
    why_not_toy: str
    first_failure_modes: list[str]
    experiments: list[Experiment] = field(default_factory=list)


@dataclass(frozen=True)
class Evaluation:
    candidate_id: str
    score: float
    upside: float
    structural_handle: float
    classical_barrier: float
    falsifiability: float
    toy_penalty: float
    barrier_penalty: float
    flags: list[str]


DOMAINS = [
    Domain(
        id="nonabelian-hsp",
        name="Nonabelian hidden subgroup and coset-state measurements",
        upside=10,
        why_high_upside=(
            "A general nonabelian HSP breakthrough could affect graph isomorphism, "
            "code equivalence, lattice automorphism variants, and group action problems."
        ),
        known_barriers=[
            "Strong Fourier sampling is insufficient for several symmetric-group cases.",
            "Useful measurements may require entangled or collective measurements across registers.",
        ],
        useful_handles=[
            "representation theory",
            "coset-state distinguishability",
            "pretty good measurements",
            "tensor-network contraction for measurement design",
        ],
    ),
    Domain(
        id="hidden-shift",
        name="Hidden shift, dihedral HSP, and phase-state sieving",
        upside=10,
        why_high_upside=(
            "Hidden shift sits near the boundary between Shor-style Fourier methods and "
            "lattice-relevant subexponential algorithms."
        ),
        known_barriers=[
            "Generic dihedral HSP has subexponential quantum algorithms but no known polynomial one.",
            "Naive Fourier sampling reduces to hard subset-sum-like postprocessing.",
        ],
        useful_handles=[
            "phase states",
            "sieve design",
            "Fourier flatness",
            "low-density subset-sum structure",
        ],
    ),
    Domain(
        id="lattice-periodicity",
        name="Lattice, number-field, and approximate periodicity problems",
        upside=9,
        why_high_upside=(
            "Factoring succeeds because periodicity survives noisy arithmetic structure. "
            "Finding analogous exploitable periodicity in lattices would be high impact."
        ),
        known_barriers=[
            "Worst-case to average-case reductions can also imply resistance to simple algorithms.",
            "Approximate periods can be too noisy for standard phase estimation.",
        ],
        useful_handles=[
            "approximate QFT",
            "phase estimation",
            "dual lattice sampling",
            "period-finding reductions",
        ],
    ),
    Domain(
        id="code-equivalence",
        name="Code equivalence and algebraic isomorphism problems",
        upside=9,
        why_high_upside=(
            "A serious quantum improvement here would hit a major family of hidden "
            "permutation and isomorphism problems rather than a hand-built oracle."
        ),
        known_barriers=[
            "Reduction to symmetric-group HSP inherits nonabelian Fourier-sampling barriers.",
            "Random instances may hide too little exploitable representation structure.",
        ],
        useful_handles=[
            "automorphism group stratification",
            "coset-state comparisons",
            "quantum walks over generator sets",
            "collective measurements",
        ],
    ),
    Domain(
        id="graph-isomorphism",
        name="Graph isomorphism beyond strong Fourier sampling",
        upside=8,
        why_high_upside=(
            "GI is not expected to be NP-complete and remains a central test case for "
            "nonabelian quantum algorithm design."
        ),
        known_barriers=[
            "Known negative results rule out simple strong Fourier sampling approaches.",
            "Classical quasi-polynomial algorithms raised the bar for a meaningful speedup.",
        ],
        useful_handles=[
            "collective coset measurements",
            "graph coherent states",
            "quantum walks on refinement trees",
            "tensor networks",
        ],
    ),
    Domain(
        id="quantum-walks",
        name="Quantum walks on algebraic and combinatorial state spaces",
        upside=8,
        why_high_upside=(
            "Quantum walks can turn geometry, expansion, and marked-subspace structure into "
            "query or time speedups without requiring full Fourier solvability."
        ),
        known_barriers=[
            "Many walks reproduce Grover-like quadratic gains only.",
            "Spectral gaps and marked-state overlaps often vanish on hard instances.",
        ],
        useful_handles=[
            "spectral gap",
            "hitting time",
            "Johnson and Cayley graphs",
            "span programs",
        ],
    ),
    Domain(
        id="query-separations",
        name="Query complexity separations with recursive structure",
        upside=8,
        why_high_upside=(
            "New query separations can expose mechanisms later converted into algorithms, "
            "as happened historically with several oracle models."
        ),
        known_barriers=[
            "Oracle separations often fail to transfer to explicit computational problems.",
            "Artificial promise problems can look impressive while teaching little.",
        ],
        useful_handles=[
            "adversary bounds",
            "polynomial method",
            "span programs",
            "forrelation",
        ],
    ),
    Domain(
        id="hamiltonian-tensor",
        name="Hamiltonian simulation, block-encoding, and tensor-network discovery",
        upside=7,
        why_high_upside=(
            "Block-encodings and simulation primitives can convert spectral structure into "
            "algorithms for linear algebra, optimization, and dynamics."
        ),
        known_barriers=[
            "Many candidates become incremental improvements to known simulation primitives.",
            "Input models can hide the real cost in state preparation or data loading.",
        ],
        useful_handles=[
            "block-encoding",
            "quantum singular value transformation",
            "tensor contraction",
            "phase estimation",
        ],
    ),
]


def _experiment(
    id: str,
    title: str,
    protocol: str,
    positive_signal: str,
    kill_criteria: str,
    upside_rank: int,
) -> Experiment:
    return Experiment(id, title, protocol, positive_signal, kill_criteria, upside_rank)


def seed_candidates() -> list[Candidate]:
    """High-variance starting hypotheses worth testing first."""

    return [
        Candidate(
            id="NAHSP-COLLECTIVE-CODE-EQUIV",
            title="Collective coset measurements for code equivalence",
            domain_ids=["nonabelian-hsp", "code-equivalence"],
            hypothesis=(
                "Code equivalence instances with structured automorphism groups may expose "
                "low-rank collective coset-state observables missed by strong Fourier sampling."
            ),
            problem_family=(
                "Families of linear codes with controlled automorphism strata, moving from "
                "small finite fields to asymptotic length n."
            ),
            proposed_quantum_mechanism=(
                "Prepare multiple coset states for hidden permutation subgroups, search over "
                "entangled measurements using representation labels and tensor-network ansatzes."
            ),
            classical_barrier=(
                "Code equivalence has hard average-case regimes and is a canonical hidden "
                "permutation problem."
            ),
            why_not_toy=(
                "The family is explicit, scales with code length, and has a real classical "
                "algorithmic baseline rather than an arbitrary oracle."
            ),
            first_failure_modes=[
                "Coset fingerprints collapse to near-identical relation data.",
                "Useful measurements require exponential tensor bond dimension.",
                "The structured automorphism promise excludes hard instances.",
            ],
            experiments=[
                _experiment(
                    "E1-CODE-COSET-RANK",
                    "Coset-state relation rank sweep",
                    (
                        "Generate code families with known permutation automorphisms. For each "
                        "hidden permutation, compute equality-relation fingerprints and rank, "
                        "then scale length and field size."
                    ),
                    "Rank and pairwise distinguishability grow with instance count using low-degree invariants.",
                    "Max pairwise overlap stays above 0.9 or rank saturates at a constant.",
                    1,
                ),
                _experiment(
                    "E2-COLLECTIVE-MEASUREMENT-ANSATZ",
                    "Tensor ansatz for collective measurements",
                    (
                        "Represent k-register measurement candidates as tensor networks over "
                        "irrep labels. Optimize distinguishability on generated code instances."
                    ),
                    "Bond dimension grows polynomially while success probability beats individual-register tests.",
                    "Required bond dimension or sample count grows exponentially on the first three scales.",
                    2,
                ),
            ],
        ),
        Candidate(
            id="DHS-SIEVE-STRUCTURED-SHIFTS",
            title="Structured hidden-shift sieve beyond generic dihedral HSP",
            domain_ids=["hidden-shift", "lattice-periodicity"],
            hypothesis=(
                "Some explicit hidden-shift families have phase-state distributions that avoid "
                "generic subset-sum hardness and admit polynomial-time sieving."
            ),
            problem_family=(
                "Cyclic and dihedral hidden shifts where the shifted object comes from bent, "
                "multiplicative-character, or low-degree algebraic functions."
            ),
            proposed_quantum_mechanism=(
                "Fourier sampling creates phase states whose frequency support has algebraic "
                "structure. A custom sieve combines phases without losing signal."
            ),
            classical_barrier=(
                "Generic hidden shift and dihedral HSP connect to lattice-relevant hard cases; "
                "classical correlation search is exponential without exploitable structure."
            ),
            why_not_toy=(
                "The work tests entire algebraic families and asks whether a known barrier has "
                "structured exceptions."
            ),
            first_failure_modes=[
                "Fourier support is either too sparse and classical, or too random and subset-sum hard.",
                "The sieve only works because the family is classically easy.",
                "Noise in approximate shifts destroys phase coherence.",
            ],
            experiments=[
                _experiment(
                    "E3-HSHIFT-SPECTRUM",
                    "Hidden-shift Fourier flatness and alias test",
                    (
                        "For each algebraic base function, measure Fourier flatness, "
                        "autocorrelation aliases, and shift distinguishability over growing domains."
                    ),
                    "Flat spectra with low autocorrelation aliases and no obvious classical correlation handle.",
                    "Large autocorrelation aliases or a simple classical correlation recovers the shift.",
                    1,
                ),
                _experiment(
                    "E4-PHASE-SIEVE",
                    "Phase-combination sieve simulation",
                    (
                        "Simulate phase-state frequency samples and search for merge rules that "
                        "increase useful phase precision faster than generic Kuperberg-style sieves."
                    ),
                    "Sample count and merge depth fit a polynomial or clearly improved subexponential law.",
                    "Scaling matches generic subset-sum sieving with no family-specific gain.",
                    2,
                ),
            ],
        ),
        Candidate(
            id="APPROX-PERIOD-LATTICE",
            title="Approximate period finding for lattice and number-field maps",
            domain_ids=["lattice-periodicity"],
            hypothesis=(
                "There may be number-field or lattice maps with approximate periods stable "
                "enough for phase estimation but hidden enough to resist classical sampling."
            ),
            problem_family=(
                "Explicit maps from lattice points or ideals to coarse invariants with tunable "
                "noise, period rank, and collision profile."
            ),
            proposed_quantum_mechanism=(
                "Use approximate QFT and phase estimation to recover dual-period information "
                "from coherent evaluations of noisy periodic maps."
            ),
            classical_barrier=(
                "Relevant regimes should map to lattice problems with worst-case or average-case evidence."
            ),
            why_not_toy=(
                "The objective is a reduction-quality scalable family, not a hand-marked solution state."
            ),
            first_failure_modes=[
                "Coherence requirements exceed the precision needed to define the map.",
                "Classical lattice reduction exploits the same approximate periods.",
                "The candidate map is not efficiently reversible.",
            ],
            experiments=[
                _experiment(
                    "E5-APPROX-PERIOD-COLLISIONS",
                    "Approximate-period collision landscape",
                    (
                        "Construct maps with known planted periods and noise. Measure whether "
                        "period-preserving collisions dominate all other collisions as dimension grows."
                    ),
                    "A stable period ridge remains visible under polynomial precision.",
                    "False periods dominate or the ridge requires exponential precision.",
                    1,
                ),
                _experiment(
                    "E6-REVERSIBLE-MAP-COST",
                    "Reversible arithmetic cost audit",
                    (
                        "Estimate reversible circuit and precision costs for candidate maps before "
                        "claiming any quantum advantage."
                    ),
                    "Map evaluation cost is polynomial with realistic precision overhead.",
                    "State preparation or arithmetic cost dominates the proposed speedup.",
                    2,
                ),
            ],
        ),
        Candidate(
            id="GI-COLLECTIVE-OBSERVABLES",
            title="Graph-isomorphism observables beyond strong Fourier sampling",
            domain_ids=["nonabelian-hsp", "graph-isomorphism"],
            hypothesis=(
                "Graph families with controlled refinement structure may admit collective "
                "observables that distinguish isomorphism cosets without solving full HSP."
            ),
            problem_family=(
                "Strongly regular graphs, CFI-like constructions, and refinement-hard families "
                "with known automorphism behavior."
            ),
            proposed_quantum_mechanism=(
                "Prepare graph-indexed coset or coherent refinement states and search for "
                "collective observables using tensor-network contractions."
            ),
            classical_barrier=(
                "Meaningful wins must beat modern quasi-polynomial classical GI baselines on "
                "well-defined families."
            ),
            why_not_toy=(
                "Graph isomorphism is a real structural problem with known quantum no-go zones."
            ),
            first_failure_modes=[
                "The observable is equivalent to classical color refinement.",
                "The family is already easy for modern classical GI.",
                "Collective measurement construction scales exponentially.",
            ],
            experiments=[
                _experiment(
                    "E7-GI-NOGO-BOUNDARY",
                    "Map the no-go boundary",
                    (
                        "Reproduce failures of strong Fourier sampling on small GI-HSP instances, "
                        "then mutate observables and record exactly which barrier is bypassed, if any."
                    ),
                    "A candidate observable separates instances that strong Fourier labels cannot.",
                    "All gains reduce to known classical refinement invariants.",
                    1,
                ),
            ],
        ),
        Candidate(
            id="WALK-ALGEBRAIC-STATE-SPACES",
            title="Quantum walks over algebraic solution complexes",
            domain_ids=["quantum-walks", "code-equivalence", "lattice-periodicity"],
            hypothesis=(
                "Some hard algebraic search problems have state-space graphs where the quantum "
                "walk spectral gap and marked overlap beat Grover-like behavior."
            ),
            problem_family=(
                "Cayley and local-move graphs over code bases, lattice bases, isomorphism "
                "certificates, or partial algebraic assignments."
            ),
            proposed_quantum_mechanism=(
                "Use coined or Szegedy walks to amplify structured marked subspaces whose "
                "geometry is invisible to unstructured search."
            ),
            classical_barrier=(
                "Classical local search and MCMC mixing can be slow on these spaces; the target "
                "is a provable hitting-time separation."
            ),
            why_not_toy=(
                "The experiment studies graph families, spectral gaps, and marked geometry over "
                "scaling instances."
            ),
            first_failure_modes=[
                "The walk only recovers a quadratic Grover speedup.",
                "The marked overlap vanishes faster than the gap helps.",
                "Classical random walks mix just as well after better coordinates are chosen.",
            ],
            experiments=[
                _experiment(
                    "E8-WALK-SPECTRAL-SWEEP",
                    "Spectral gap and marked-overlap sweep",
                    (
                        "Build local-move graphs for each algebraic family. Track normalized "
                        "spectral gap, marked overlap, and classical conductance proxies."
                    ),
                    "Quantum hitting-time proxy improves asymptotically over classical and Grover baselines.",
                    "Gap-overlap product predicts only quadratic or worse behavior.",
                    1,
                ),
            ],
        ),
        Candidate(
            id="HIGHER-ORDER-FOURIER-HIDDEN-STRUCTURE",
            title="Higher-order Fourier search for nonlinear hidden structure",
            domain_ids=["query-separations", "hidden-shift"],
            hypothesis=(
                "Nonlinear hidden structure may become tractable when expressed through "
                "higher-order Fourier or Gowers-uniformity observables rather than plain BV-style parity."
            ),
            problem_family=(
                "Explicit low-degree phase polynomials, bent-function shifts, and locally "
                "testable hidden constraints over finite fields."
            ),
            proposed_quantum_mechanism=(
                "Use phase queries and controlled derivatives to turn high-order structure into "
                "linear Fourier information over an expanded domain."
            ),
            classical_barrier=(
                "Choose distributions with known classical query lower bounds or reductions to "
                "hard property-testing tasks."
            ),
            why_not_toy=(
                "Candidates must supply a scalable distribution and lower-bound target before "
                "any circuit search starts."
            ),
            first_failure_modes=[
                "Derivative queries collapse the problem to classical low-degree learning.",
                "The promise is artificial and has no explicit computational analogue.",
                "The quantum routine is just BV on a relabeled oracle.",
            ],
            experiments=[
                _experiment(
                    "E9-DERIVATIVE-FOURIER-LIFT",
                    "Derivative Fourier lift test",
                    (
                        "For each nonlinear family, compute whether controlled finite differences "
                        "produce sparse Fourier spectra over polynomially many derivative orders."
                    ),
                    "Higher-order spectra become sparse while the original family remains classically hard.",
                    "Sparsity appears only after using exponentially many derivative settings.",
                    1,
                ),
            ],
        ),
        Candidate(
            id="BLOCK-ENCODED-INVARIANTS",
            title="Block-encoded spectral invariants for isomorphism-like problems",
            domain_ids=["hamiltonian-tensor", "graph-isomorphism", "code-equivalence"],
            hypothesis=(
                "Quantum singular value transformation may expose algebraic invariants of "
                "graphs or codes that are expensive to estimate classically."
            ),
            problem_family=(
                "Sparse matrices derived from graph lifts, code Tanner graphs, association "
                "schemes, and coherent constraint systems."
            ),
            proposed_quantum_mechanism=(
                "Block-encode structured operators and use polynomial transformations or phase "
                "estimation to estimate invariants that separate hard instances."
            ),
            classical_barrier=(
                "Candidate invariants must not be cheaply approximable by classical randomized "
                "linear algebra on the same sparse access model."
            ),
            why_not_toy=(
                "The input model and block-encoding cost are part of the score, preventing hidden data-loading wins."
            ),
            first_failure_modes=[
                "The invariant is classically estimable by Lanczos or trace estimation.",
                "Block-encoding construction costs more than the classical baseline.",
                "The invariant fails to separate hard instances.",
            ],
            experiments=[
                _experiment(
                    "E10-INVARIANT-SEPARATION",
                    "Invariant separation and access-model audit",
                    (
                        "Search for operator families whose spectra separate hard paired "
                        "instances. For every hit, compare against classical trace/Lanczos estimators."
                    ),
                    "A separating invariant is quantum-estimable in polylog or polynomially lower cost.",
                    "Classical randomized estimators recover the invariant within the same asymptotic cost.",
                    2,
                ),
            ],
        ),
    ]


def _text_of(candidate: Candidate) -> str:
    parts: list[str] = [
        candidate.title,
        candidate.hypothesis,
        candidate.problem_family,
        candidate.proposed_quantum_mechanism,
        candidate.classical_barrier,
        candidate.why_not_toy,
    ]
    parts.extend(candidate.first_failure_modes)
    for experiment in candidate.experiments:
        parts.extend(
            [
                experiment.title,
                experiment.protocol,
                experiment.positive_signal,
                experiment.kill_criteria,
            ]
        )
    return " ".join(parts).lower()


def evaluate_candidate(candidate: Candidate, domain_index: dict[str, Domain]) -> Evaluation:
    text = _text_of(candidate)
    domains = [domain_index[domain_id] for domain_id in candidate.domain_ids]
    upside = max(domain.upside for domain in domains) * 10.0

    structural_hits = sum(1 for pattern in STRUCTURAL_HANDLE_PATTERNS if pattern in text)
    structural_handle = min(100.0, 18.0 * structural_hits)

    barrier_hits = sum(1 for pattern in CLASSICAL_BARRIER_PATTERNS if pattern in text)
    classical_barrier = min(100.0, 18.0 * barrier_hits)

    falsifiability = min(
        100.0,
        30.0
        + 12.0 * len(candidate.experiments)
        + 7.0 * len(candidate.first_failure_modes)
        + sum(4.0 for exp in candidate.experiments if exp.kill_criteria),
    )

    toy_hits = [pattern for pattern in TOY_PATTERNS if pattern in text]
    toy_penalty = min(70.0, 18.0 * len(toy_hits))

    known_barrier_count = sum(len(domain.known_barriers) for domain in domains)
    barrier_penalty = min(18.0, 3.0 * known_barrier_count)

    score = (
        0.34 * upside
        + 0.24 * structural_handle
        + 0.20 * classical_barrier
        + 0.22 * falsifiability
        - toy_penalty
        - barrier_penalty
    )
    score = max(0.0, min(100.0, score))

    flags: list[str] = []
    if toy_hits:
        flags.append("toy-risk:" + ",".join(toy_hits[:4]))
    if structural_handle < 45:
        flags.append("weak structural quantum handle")
    if classical_barrier < 45:
        flags.append("classical baseline not hard enough yet")
    if barrier_penalty >= 12:
        flags.append("known no-go barriers must be confronted explicitly")

    return Evaluation(
        candidate_id=candidate.id,
        score=round(score, 2),
        upside=round(upside, 2),
        structural_handle=round(structural_handle, 2),
        classical_barrier=round(classical_barrier, 2),
        falsifiability=round(falsifiability, 2),
        toy_penalty=round(toy_penalty, 2),
        barrier_penalty=round(barrier_penalty, 2),
        flags=flags,
    )


def diagnose_project(root: Path) -> dict[str, Any]:
    """Summarize why the previous repository direction is low ceiling."""

    ignored = {".git", "__pycache__", "google-cloud-sdk"}
    project_files = [
        path
        for path in root.rglob("*")
        if path.is_file() and not any(part in ignored for part in path.parts)
    ]

    history_path = root / "history.json"
    history: list[dict[str, Any]] = []
    if history_path.exists():
        try:
            history = json.loads(history_path.read_text())
        except json.JSONDecodeError:
            history = []

    names = [str(item.get("problem_name", "")) for item in history]
    descriptions = [str(item.get("description", "")) for item in history]
    all_history_text = " ".join(names + descriptions).lower()
    toy_term_counts = {
        term: all_history_text.count(term)
        for term in [
            "secret finding",
            "bernstein-vazirani",
            "bitwise",
            "oracle",
            "state preparation",
            "unitary synthesis",
        ]
    }

    speedups = Counter(str(item.get("speedup_type", "N/A")) for item in history)
    solved = sum(1 for item in history if float(item.get("success_rate", 0.0) or 0.0) >= 1.0)
    repeated = Counter(name for name in names if name)

    source_notes = []
    for filename, needle, note in [
        (
            "theorist.py",
            "Set max_qubits_to_simulate to exactly 3",
            "The theorist prompt hard-caps proposals at N=3, which cannot validate asymptotic advantage.",
        ),
        (
            "search_engine.py",
            "for depth in range(1, 6)",
            "The state/unitary search is capped at depth 5, making it a small-circuit synthesizer.",
        ),
        (
            "discover_algorithms.py",
            "custom, or non-textbook quantum problem/task",
            "Novelty was delegated to prompt phrasing instead of formal search-space constraints.",
        ),
    ]:
        path = root / filename
        if path.exists() and needle in path.read_text(errors="ignore"):
            source_notes.append(note)

    return {
        "scanned_files_excluding_vendor_and_git": len(project_files),
        "history_runs": len(history),
        "success_rate_1_runs": solved,
        "claimed_speedups": dict(speedups),
        "most_repeated_problem_names": repeated.most_common(8),
        "toy_term_counts": toy_term_counts,
        "source_notes": source_notes,
        "blunt_diagnosis": [
            "The old loop is not a credible path to a Shor-level algorithm.",
            "It searches tiny circuits and arbitrary oracle puzzles, then lets an LLM label complexity from N<=3 data.",
            "Most successful runs rediscover Bernstein-Vazirani-like parity structure; most exotic names are unsolved or unsupported.",
            "The dashboard's 'solved novel algorithms' criterion is just success_rate >= 1.0 on tiny instances, not a research result.",
            "The project needs explicit scalable families, classical baselines, structural quantum handles, and kill criteria.",
        ],
    }


def run_reference_structural_tests() -> dict[str, Any]:
    """Run small reference checks that demonstrate the structural-test harness."""

    parity_signal = truth_table_from_boolean(
        lambda x: bin(x & 0b10101).count("1") % 2,
        5,
    )
    fourier = fourier_metrics(parity_signal)

    periodic_labels = [x % 4 for x in range(16)]
    periodic = periodicity_metrics(periodic_labels)

    rng = np.random.default_rng(7)
    hidden_shift_signal = rng.choice([-1.0, 1.0], size=64)
    shift = hidden_shift_metrics(hidden_shift_signal)

    coset = coset_fingerprint_metrics(
        [
            [x % 2 for x in range(8)],
            [x % 4 for x in range(8)],
            [(x // 2) % 2 for x in range(8)],
            [0 if x in {0, 1, 4, 5} else 1 for x in range(8)],
        ]
    )

    cycle = np.zeros((10, 10), dtype=float)
    for i in range(10):
        cycle[i, (i - 1) % 10] = 1
        cycle[i, (i + 1) % 10] = 1
    walk = walk_spectral_metrics(cycle, marked=[0])

    return {
        "parity_fourier_smoke_test": as_jsonable(fourier),
        "periodicity_smoke_test": as_jsonable(periodic),
        "hidden_shift_random_baseline": as_jsonable(shift),
        "coset_fingerprint_smoke_test": as_jsonable(coset),
        "cycle_walk_smoke_test": as_jsonable(walk),
    }


def build_agenda(root: Path, top_k: int | None = None) -> dict[str, Any]:
    domain_index = {domain.id: domain for domain in DOMAINS}
    candidates = seed_candidates()
    evaluations = [evaluate_candidate(candidate, domain_index) for candidate in candidates]
    eval_by_id = {evaluation.candidate_id: evaluation for evaluation in evaluations}
    ranked = sorted(candidates, key=lambda candidate: eval_by_id[candidate.id].score, reverse=True)
    if top_k is not None:
        ranked = ranked[:top_k]

    ranked_experiments = []
    for rank, candidate in enumerate(ranked, start=1):
        evaluation = eval_by_id[candidate.id]
        for experiment in sorted(candidate.experiments, key=lambda exp: exp.upside_rank):
            ranked_experiments.append(
                {
                    "candidate_rank": rank,
                    "candidate_id": candidate.id,
                    "candidate_title": candidate.title,
                    "candidate_score": evaluation.score,
                    **asdict(experiment),
                }
            )
    ranked_experiments.sort(
        key=lambda item: (item["upside_rank"], -float(item["candidate_score"]), item["id"])
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mission": (
            "Increase the chance of discovering or clarifying a genuinely major quantum "
            "algorithmic idea by searching for scalable structural advantage, not tiny demos."
        ),
        "diagnosis": diagnose_project(root),
        "revised_direction": {
            "one_sentence": (
                "Make this a research-program generator and structural-test harness for "
                "high-upside quantum algorithm mechanisms."
            ),
            "cut_or_deprioritize": [
                "Arbitrary secret-bitstring oracle variants with no natural problem family.",
                "N<=3 circuit searches used as evidence for asymptotic speedup.",
                "State-preparation and unitary-synthesis tasks unless they directly support a larger algorithm.",
                "LLM-only complexity claims without a lower bound, reduction, or scalable mechanism.",
                "Dashboard labels that call tiny solved instances 'novel algorithms'.",
            ],
            "positive_filter": [
                "Explicit scalable family.",
                "Known or conjectured classical barrier.",
                "Quantum mechanism tied to Fourier sampling, coset states, phase estimation, walks, block-encodings, or tensor measurements.",
                "A structural experiment with a positive signal and a kill criterion.",
                "A path from toy finite instances to asymptotic proof obligations.",
            ],
        },
        "domains": [asdict(domain) for domain in DOMAINS],
        "ranked_candidates": [
            {
                **asdict(candidate),
                "evaluation": asdict(eval_by_id[candidate.id]),
            }
            for candidate in ranked
        ],
        "ranked_experiments": ranked_experiments,
        "reference_structural_tests": run_reference_structural_tests(),
    }


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def agenda_to_markdown(agenda: dict[str, Any]) -> str:
    diagnosis = agenda["diagnosis"]
    lines = [
        "# Quantum Algorithm Research Engine",
        "",
        "## Blunt diagnosis",
        "",
    ]
    for item in diagnosis["blunt_diagnosis"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "Repository scan:",
            f"- Scanned files, excluding vendor and git: {diagnosis['scanned_files_excluding_vendor_and_git']}",
            f"- Historical runs: {diagnosis['history_runs']}",
            f"- Tiny-instance success_rate >= 1.0 runs: {diagnosis['success_rate_1_runs']}",
            f"- Claimed speedups: `{json.dumps(diagnosis['claimed_speedups'], sort_keys=True)}`",
            f"- Toy-term counts: `{json.dumps(diagnosis['toy_term_counts'], sort_keys=True)}`",
            "",
        ]
    )
    if diagnosis["source_notes"]:
        lines.append("Source-level issues:")
        for note in diagnosis["source_notes"]:
            lines.append(f"- {note}")
        lines.append("")

    direction = agenda["revised_direction"]
    lines.extend(
        [
            "## Revised direction",
            "",
            direction["one_sentence"],
            "",
            "Cut or deprioritize:",
        ]
    )
    for item in direction["cut_or_deprioritize"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Only admit a lead when it has:")
    for item in direction["positive_filter"]:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Top research leads",
            "",
            "| Rank | Score | Lead | Domains | Main kill criterion |",
            "| ---: | ---: | --- | --- | --- |",
        ]
    )
    for rank, candidate in enumerate(agenda["ranked_candidates"], start=1):
        evaluation = candidate["evaluation"]
        domains = ", ".join(candidate["domain_ids"])
        first_kill = candidate["experiments"][0]["kill_criteria"] if candidate["experiments"] else ""
        anchor = _slug(candidate["title"])
        lines.append(
            f"| {rank} | {evaluation['score']:.2f} | [{candidate['title']}](#{anchor}) | "
            f"{domains} | {first_kill} |"
        )

    lines.extend(["", "## Experiment roadmap", ""])
    for idx, experiment in enumerate(agenda["ranked_experiments"], start=1):
        lines.extend(
            [
                f"{idx}. **{experiment['title']}** (`{experiment['id']}`)",
                f"   - Lead: {experiment['candidate_title']}",
                f"   - Protocol: {experiment['protocol']}",
                f"   - Positive signal: {experiment['positive_signal']}",
                f"   - Kill criterion: {experiment['kill_criteria']}",
            ]
        )

    lines.extend(["", "## Lead details", ""])
    for candidate in agenda["ranked_candidates"]:
        evaluation = candidate["evaluation"]
        lines.extend(
            [
                f"### {candidate['title']}",
                "",
                f"- Candidate id: `{candidate['id']}`",
                f"- Score: `{evaluation['score']}`",
                f"- Hypothesis: {candidate['hypothesis']}",
                f"- Problem family: {candidate['problem_family']}",
                f"- Quantum mechanism: {candidate['proposed_quantum_mechanism']}",
                f"- Classical barrier: {candidate['classical_barrier']}",
                f"- Why this is not toy: {candidate['why_not_toy']}",
                "- First failure modes:",
            ]
        )
        for failure in candidate["first_failure_modes"]:
            lines.append(f"  - {failure}")
        if evaluation["flags"]:
            lines.append(f"- Evaluation flags: `{', '.join(evaluation['flags'])}`")
        lines.append("")

    lines.extend(
        [
            "## Structural-test harness",
            "",
            "The current executable tests are smoke checks for the metrics, not proof of advantage.",
            "Use them to reject bad leads early and to decide which finite families deserve deeper math.",
            "",
            "Available checks:",
            "- Walsh-Fourier concentration for Boolean phase oracles.",
            "- Gowers uniformity and derivative Fourier sparsity for higher-order structure.",
            "- Periodicity collision landscapes for exact or approximate periods.",
            "- Hidden-shift spectral flatness and autocorrelation aliasing.",
            "- Coset equality-relation rank and pairwise distinguishability.",
            "- Quantum-walk spectral gap and marked-overlap proxies.",
            "",
            "Run:",
            "",
            "```bash",
            "python discover_algorithms.py --output-dir research",
            "python -m unittest discover -s tests",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(agenda: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "agenda.json"
    md_path = output_dir / "project_plan.md"
    json_path.write_text(json.dumps(agenda, indent=2, sort_keys=True))
    md_path.write_text(agenda_to_markdown(agenda))
    return {"json": str(json_path), "markdown": str(md_path)}


def print_summary(agenda: dict[str, Any], paths: dict[str, str] | None = None) -> None:
    print("Quantum Algorithm Research Engine")
    print("=================================")
    for item in agenda["diagnosis"]["blunt_diagnosis"]:
        print(f"- {item}")
    print()
    print("Top leads:")
    for idx, candidate in enumerate(agenda["ranked_candidates"][:5], start=1):
        evaluation = candidate["evaluation"]
        print(f"{idx}. {candidate['title']} [{evaluation['score']:.2f}]")
    if paths:
        print()
        print(f"Wrote JSON agenda: {paths['json']}")
        print(f"Wrote markdown plan: {paths['markdown']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output-dir", type=Path, default=Path("research"))
    parser.add_argument("--top-k", type=int, default=None)
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--skip-audit", action="store_true")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    agenda = build_agenda(root, top_k=args.top_k)
    paths = None if args.no_write else write_outputs(agenda, args.output_dir)
    if not args.no_write and not args.skip_audit:
        from research_lab import write_research_audit

        audit_paths = write_research_audit(agenda, root, args.output_dir)
        if paths is not None:
            paths.update(audit_paths)
    print_summary(agenda, paths)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
