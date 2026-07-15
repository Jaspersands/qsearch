"""Literature ingestion and proof-gated hypothesis generation.

The pipeline is intentionally conservative: it mines mechanism-level records
from literature metadata and emits only scalable, proof-obligation-bearing
research candidates. Toy oracle candidates can be submitted to the gate by
tests or callers, but the production hypothesis factory does not generate them.
"""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from literature_radar import build_literature_index
from problem_ontology import build_problem_ontology
from proof_gate import validate_candidate
from research_registry import (
    CandidateRecord,
    ExperimentRecord,
    issue_to_dict,
    upsert_candidate,
    upsert_experiment,
    upsert_rejected_candidate,
    utc_now,
)


LITERATURE_RECORDS_PATH = Path("research/literature_records.json")


@dataclass(frozen=True)
class LiteratureMechanismRecord:
    id: str
    title: str
    url: str
    year: int | None
    source: str
    tags: list[str]
    mechanism: str
    problem_family: str
    reduction: str
    no_go_barrier: str
    proof_technique: str
    open_question: str
    reusable_abstraction: str
    abstract: str = ""


@dataclass(frozen=True)
class HypothesisFactoryResult:
    accepted: list[str] = field(default_factory=list)
    rejected: list[str] = field(default_factory=list)
    experiments: list[str] = field(default_factory=list)


MECHANISM_RULES: list[tuple[set[str], dict[str, str]]] = [
    (
        {"hull", "projector", "classical-reduction"},
        {
            "mechanism": "Basis-independent hull projectors reduce permutation code equivalence to weighted graph isomorphism; shortening extends the upper bound by hull dimension.",
            "problem_family": "Random and structured linear-code equivalence instances stratified by Euclidean or Hermitian hull dimension.",
            "reduction": "For trivial hulls, Sigma_C=G^T(GG^T)^(-1)G gives an iff weighted-GI instance in polynomial time; nontrivial hulls admit a shortening reduction parameterized by h.",
            "no_go_barrier": "A random planted code pair is not independent code-equivalence hardness when its public generators expose a trivial or bounded hull and a legal GI reduction.",
            "proof_technique": "Orthogonal direct sums, basis-independent projectors, permutation conjugacy, image recovery, shortening, and graph isomorphism.",
            "open_question": "Which natural code families have growing hull complexity, survive shortening/projector reductions, and still avoid algebraic support recovery?",
            "reusable_abstraction": "Hull-stratified equivalence record: input access, hull law, projector certificate, shortening exponent, graph matcher, and verified coordinate witness.",
        },
    ),
    (
        {"hidden-number", "random-multiplier", "noisy-fourier", "significant-fourier"},
        {
            "mechanism": "Recover a hidden cyclic frequency from partial or noisy information about random multiplier products using Fourier or lattice methods.",
            "problem_family": "Uniform random-multiplier hidden-number problems and random-label DCP local-quadrature decoding over growing cyclic groups.",
            "reduction": "Random X/Y measurements of DCP phase states give one-shot noisy quadratures of chi_d(k), but this is not the deterministic partial-bit HNP oracle and does not grant chosen multipliers.",
            "no_go_barrier": "Significant-Fourier and sparse-Fourier algorithms often require chosen signal queries, repeatable evaluation, advice, or preprocessing not supplied by independent random DCP labels.",
            "proof_technique": "Finite-abelian Fourier analysis, significant coefficient finding, hidden-number reductions, lattice approximation, and access-model separation.",
            "open_question": "Can noisy one-shot uniform random-multiplier quadratures be decoded in poly(log N) time and memory without chosen labels, advice, or a length-N spectrum?",
            "reusable_abstraction": "Random-design frequency record: multiplier distribution, observation channel, query repeatability, advice, decoder time/memory, bad-sample tolerance, and full-secret recovery.",
        },
    ),
    (
        {"shifted-character", "multiplicative-character", "hidden-shifted-power"},
        {
            "mechanism": "Finite-field Fourier deconvolution of a shifted multiplicative character using nonzero Gauss sums.",
            "problem_family": "Shifted Legendre, quartic-character, and hidden shifted-power problems over growing finite fields.",
            "reduction": "No registry-backed reduction to a major natural problem is known; the remaining separation is computational and oracle-model dependent.",
            "no_go_barrier": "Classical hidden-shifted-power recovery already uses logarithmically many queries with domain-scale time, and nonuniform preprocessing gives polylogarithmic online decoding.",
            "proof_technique": "Gauss sums, multiplicative characters, finite-field harmonic analysis, polynomial interpolation, and character-sum bounds.",
            "open_question": "Is there a uniform polylogarithmic classical decoder, or a natural reduction or named assumption supporting superpolynomial uniform decoding hardness?",
            "reusable_abstraction": "Character-shift complexity ledger separating queries, uniform time, preprocessing, advice, amortization, and reduction provenance.",
        },
    ),
    (
        {"schur-product", "alternant-code", "support-recovery", "geometric-invariant"},
        {
            "mechanism": "Classical Schur/star-product filtrations, shortening, conductors, and algebraic support recovery for structured codes.",
            "problem_family": "GRS, alternant, Goppa, rank-metric, and related algebraic code-equivalence families.",
            "reduction": "These are dequantization barriers for code-equivalence-to-symmetric-HSP routes, not quantum reductions.",
            "no_go_barrier": "Low-dimensional Schur powers or conductor filtrations can distinguish structure and recover hidden supports in polynomial time.",
            "proof_technique": "Componentwise code products, shortening/puncturing filtrations, conductors, Groebner bases, and algebraic geometry.",
            "open_question": "Which natural scalable code families survive all known star-product, support-recovery, and canonicalization attacks?",
            "reusable_abstraction": "Algebraic-code attack ledger: Schur dimensions, local filtrations, conductor status, support recovery, and equivalence certificate.",
        },
    ),
    (
        {"hidden-shift", "dihedral-hsp", "gowers-norm", "lattice-adjacent", "unique-svp", "state-isomorphism"},
        {
            "mechanism": "Phase-state Fourier sampling, higher-order harmonic analysis, and family-specific sieving.",
            "problem_family": "Hidden shift and dihedral HSP families over growing abelian groups and group actions.",
            "reduction": "Dihedral HSP reductions connect hidden-shift improvements to lattice-relevant unique-SVP frontiers.",
            "no_go_barrier": "Generic phase-state sieving is only subexponential, and many structured phase families are classically learnable.",
            "proof_technique": "Fourier analysis, Gowers norms, phase-state combining, and hidden-shift/DHSP reductions.",
            "open_question": "Can explicit non-classically-learnable phase families yield better-than-generic sieve exponents?",
            "reusable_abstraction": "Phase-state family record: derivative spectrum, merge constraints, sieve cost, and dequantization checks.",
        },
    ),
    (
        {
            "symmetric-qft",
            "schur-transform",
            "clebsch-gordan",
            "kronecker-coefficient",
            "kronecker-transform",
            "multiplicity-space",
            "recoupling",
        },
        {
            "mechanism": (
                "Separate the efficient S_n QFT and weak irrep projectors from the internal Kronecker transform, "
                "overlapping Racah/associator moves, state-dependent transition weights, and outcome decoding."
            ),
            "problem_family": (
                "Multi-register symmetric-group involution coset states and representation-theoretic multiplicity "
                "problems with explicit partition, dimension-ratio, and multiplicity-space promises."
            ),
            "reduction": (
                "Kronecker multiplicity projectors count invariant-space dimensions; they do not reduce hidden "
                "involution recovery to a coherent Kronecker basis transform or compressed decoder."
            ),
            "no_go_barrier": (
                "The ordinary S_n QFT is already efficient, restricted multiplicity speedups are classically matched "
                "on many families, and multiplicity-space isometries cannot be assumed to be classical relabelings."
            ),
            "proof_technique": (
                "Subgroup-tower QFT, generalized phase estimation, commuting invariant projectors, Schur-Weyl duality, "
                "Kronecker multiplicities, F-moves, and classical combinatorial multiplicity algorithms."
            ),
            "open_question": (
                "Is there a uniform polynomial internal S_n Kronecker/Racah transform, including multiplicity bases "
                "and state-transition amplitudes, that supports a hidden-involution decoder for k growing with n?"
            ),
            "reusable_abstraction": (
                "Kronecker/recoupling capability ledger separating QFT, label projection, multiplicity counting, "
                "coherent basis transforms, associators, transition amplitudes, decoding, and classical comparison."
            ),
        },
    ),
    (
        {"hidden-subgroup", "nonabelian-hsp", "symmetric-hsp", "graph-isomorphism", "code-equivalence", "representation-theory"},
        {
            "mechanism": "Multi-register coset-state observables beyond individual strong Fourier sampling.",
            "problem_family": "Hidden permutation and nonabelian HSP instances including graph isomorphism and code equivalence.",
            "reduction": "Graph isomorphism and code equivalence embed into symmetric-group hidden subgroup formulations.",
            "no_go_barrier": "Strong Fourier sampling over the symmetric group is known not to solve GI-relevant HSP instances.",
            "proof_technique": "Representation theory, coset-state distinguishability, tensor-network measurement ansatzes, and invariant comparison.",
            "open_question": "Can a polynomial-description collective measurement separate hard hidden-permutation coset states?",
            "reusable_abstraction": "Coset-state ensemble record: registers, observable family, distinguishability metric, and classical invariant overlap.",
        },
    ),
    (
        {"qsvt", "block-encoding", "hamiltonian-simulation", "linear-algebra"},
        {
            "mechanism": "Block-encoded matrix transformations using polynomial singular-value filters.",
            "problem_family": "Linear-algebraic and Hamiltonian simulation problems with explicit data-access models.",
            "reduction": "QSVT unifies many algorithms but gives advantage only when block encoding and state preparation are efficient.",
            "no_go_barrier": "Data loading, QRAM assumptions, and classical dequantization can erase apparent speedups.",
            "proof_technique": "Polynomial approximation, block-encoding composition, amplitude amplification, and precision accounting.",
            "open_question": "Can problem-native or randomized block encodings remove the dominant access-model bottleneck?",
            "reusable_abstraction": "Access-model ledger: block-encoding cost, precision, condition number, and dequantized baseline.",
        },
    ),
    (
        {"span-programs", "adversary-bound", "quantum-walks", "query-complexity", "learning-graphs"},
        {
            "mechanism": "Adversary-bound witnesses converted into span programs and quantum-walk algorithms.",
            "problem_family": "Structured query problems with provable separations from classical decision trees.",
            "reduction": "The general adversary bound characterizes quantum query complexity and can synthesize query algorithms.",
            "no_go_barrier": "Many query advantages remain oracle-only and do not transfer to natural computational problems.",
            "proof_technique": "Semidefinite duality, span-program witnesses, spectral-gap analysis, and composition theorems.",
            "open_question": "Can mined adversary witnesses expose reusable primitives for natural algebraic problems?",
            "reusable_abstraction": "Witness graph and span-program compiler with classical lower-bound comparison.",
        },
    ),
]


def _normalize_text(value: str) -> str:
    return " ".join(value.split())


def _rule_for_item(tags: Iterable[str], title: str, abstract: str) -> dict[str, str]:
    tag_set = set(tags)
    text = f"{title} {abstract}".lower().replace("_", " ")
    recoupling_tags = {
        "symmetric-qft",
        "schur-transform",
        "clebsch-gordan",
        "kronecker-coefficient",
        "kronecker-transform",
        "multiplicity-space",
        "recoupling",
    }
    if tag_set & recoupling_tags:
        for tags_for_rule, payload in MECHANISM_RULES:
            if tags_for_rule == recoupling_tags:
                return payload
    for tags_for_rule, payload in MECHANISM_RULES:
        keyword_hit = any(keyword.replace("-", " ") in text for keyword in tags_for_rule)
        if tag_set & tags_for_rule or keyword_hit:
            return payload
    return {
        "mechanism": "Unclassified quantum-algorithm mechanism requiring manual extraction.",
        "problem_family": "Unclassified scalable problem family.",
        "reduction": "No reduction extracted yet.",
        "no_go_barrier": "No no-go barrier extracted yet.",
        "proof_technique": "Unknown proof technique.",
        "open_question": "What structural theorem would make this more than a benchmark improvement?",
        "reusable_abstraction": "Manual-review literature record.",
    }


def fetch_recent_arxiv_quantum_algorithms(max_results: int = 20, timeout: int = 20) -> list[dict[str, Any]]:
    """Query arXiv for recent quantum-algorithm papers."""

    search_query = 'all:"quantum algorithm" OR all:"hidden subgroup" OR all:"hidden shift" OR all:"quantum walk"'
    query = urllib.parse.urlencode(
        {
            "search_query": search_query,
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
    url = f"https://export.arxiv.org/api/query?{query}"
    with urllib.request.urlopen(url, timeout=timeout) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    papers: list[dict[str, Any]] = []
    for entry in root.findall("atom:entry", ns):
        arxiv_url = entry.findtext("atom:id", default="", namespaces=ns)
        published = entry.findtext("atom:published", default="", namespaces=ns)
        year_match = re.match(r"(\d{4})", published or "")
        papers.append(
            {
                "id": arxiv_url.rsplit("/", 1)[-1] if arxiv_url else f"recent-arxiv-{len(papers)}",
                "title": _normalize_text(entry.findtext("atom:title", default="", namespaces=ns)),
                "url": arxiv_url,
                "year": int(year_match.group(1)) if year_match else None,
                "tags": ["recent-arxiv", "quantum-algorithms"],
                "abstract": _normalize_text(entry.findtext("atom:summary", default="", namespaces=ns)),
                "source": "arxiv",
            }
        )
    return papers


def extract_literature_records(
    refresh_arxiv: bool = False,
    max_arxiv_results: int = 20,
) -> list[LiteratureMechanismRecord]:
    """Extract structured records from seed literature and optional arXiv metadata."""

    index = build_literature_index(refresh_arxiv=False)
    raw_items: list[dict[str, Any]] = []
    for seed in index["seed_papers"]:
        raw_items.append(
            {
                "id": seed["id"],
                "title": seed["title"],
                "url": seed["url"],
                "year": seed["year"],
                "tags": seed["tags"],
                "abstract": seed.get("why_it_matters", ""),
                "source": "seed",
            }
        )

    if refresh_arxiv:
        raw_items.extend(fetch_recent_arxiv_quantum_algorithms(max_results=max_arxiv_results))

    records: list[LiteratureMechanismRecord] = []
    seen: set[str] = set()
    for item in raw_items:
        record_id = item["id"]
        if record_id in seen:
            continue
        seen.add(record_id)
        rule = _rule_for_item(item.get("tags", []), item.get("title", ""), item.get("abstract", ""))
        records.append(
            LiteratureMechanismRecord(
                id=record_id,
                title=item.get("title", ""),
                url=item.get("url", ""),
                year=item.get("year"),
                source=item.get("source", "seed"),
                tags=list(item.get("tags", [])),
                abstract=item.get("abstract", ""),
                **rule,
            )
        )
    return records


def write_literature_records(
    path: Path = LITERATURE_RECORDS_PATH,
    refresh_arxiv: bool = False,
    max_arxiv_results: int = 20,
) -> list[dict[str, Any]]:
    records = [asdict(record) for record in extract_literature_records(refresh_arxiv, max_arxiv_results)]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records, indent=2, sort_keys=True))
    return records


def _records_with_tags(records: list[LiteratureMechanismRecord], wanted: set[str]) -> list[LiteratureMechanismRecord]:
    return [record for record in records if wanted & set(record.tags)]


def _ontology_ids(*wanted: str) -> list[str]:
    node_ids = {node["id"] for node in build_problem_ontology()["nodes"]}
    return [node_id for node_id in wanted if node_id in node_ids]


def build_hidden_shift_candidate(records: list[LiteratureMechanismRecord]) -> tuple[CandidateRecord, list[ExperimentRecord]]:
    now = utc_now()
    support = _records_with_tags(records, {"hidden-shift", "dihedral-hsp", "gowers-norm", "lattice-adjacent", "unique-svp"})
    literature_ids = sorted({record.id for record in support}) or ["kuperberg-dhsp-2003", "roetteler-hidden-shift-gowers-2009"]
    candidate = CandidateRecord(
        id="HYP-LIT-HIDDEN-SHIFT-SIEVE",
        title="Literature-mined state-sample-native DCP sieve and decoder",
        status="hypothesis",
        created_at=now,
        updated_at=now,
        literature_ids=literature_ids[:8],
        ontology_node_ids=_ontology_ids("hidden-shift", "dihedral-hsp", "unique-svp", "gowers-structure"),
        problem_family=(
            "The full family of D_N coset-state inputs emitted by the exact lattice-to-DCP reduction. Literature-mined "
            "structured phase families are retained only as counterexamples and mechanism testbeds, never as coverage of the full promise."
        ),
        input_model=(
            "Independent coset-state samples under the f=1 DCP promise, including arbitrary bad basis-state registers at "
            "per-register probability up to 1/log N; good registers transform into known random Fourier labels and one-qubit "
            "phase states. No coherent evaluator, chosen-label access, or nonuniform advice is supplied."
        ),
        classical_baseline=(
            "Known generic DCP/DHSP postprocessing and subset-sum baselines, exact Kuperberg/Regev resource classes, and "
            "classical attacks on any public structure introduced by a literature-mined restriction."
        ),
        reduction_or_lower_bound=(
            "Compose only through THM-REGEV-USVP-TO-DCP-2003 and require full-family coverage, uniform state construction, "
            "parameter preservation, bounded success, and a complete lattice decoder before claiming relevance."
        ),
        quantum_mechanism=(
            "Extract reusable state-processing primitives, implicit label-combination schemes, representation transforms, and "
            "decoder recurrences from the literature, then instantiate only operations legal on independent DCP phase states."
        ),
        cost_model=(
            "Count input coset states, zero labels, physical sum/difference branches, postselection, memory, label arithmetic, "
            "precision, merge depth, every recursive decoder stage, and the lattice parameter map as functions of log N."
        ),
        measurement_and_decoding=(
            "Apply uniform state-only collective measurements, recover all hidden-reflection congruence bits through a proved "
            "recurrence, verify the reflection from the supplied state interface, and compose it with the lattice decoder."
        ),
        success_statement=(
            "Target theorem: a literature-composed uniform algorithm recovers the complete reflection on every promised DCP "
            "state instance with bounded error and proves an asymptotic resource improvement over a named generic sieve baseline."
        ),
        complexity_accounting=(
            "Report theorem-level sample, time, space, precision, postselection, and full-decoder bounds in log N and lattice "
            "dimension; empirical favorable schedules and online costs with hidden preprocessing do not count."
        ),
        no_go_analysis=(
            "Known failure modes include evaluator smuggling, selected-family scope, deterministic favorable branches, "
            "parity-only endpoints, generic subset-sum behavior, nonuniform preprocessing, and exponential precision or memory."
        ),
        dequantization_check=(
            "Audit the exact theorem interface and physical branch probabilities; attack every introduced public structure with "
            "autocorrelation, sparse Fourier, derivative, algebraic, sample, and preprocessing baselines before promotion."
        ),
        falsifiers=[
            "A mined primitive requires evaluator, chosen-label, or family-advice access absent from DCP samples.",
            "The primitive applies only to a selected algebraic phase family rather than all DCP instances.",
            "Physical branch accounting removes the apparent resource improvement.",
            "The endpoint supplies parity but no complete hidden-reflection decoder.",
            "The theorem-level bound matches or loses to Kuperberg/Regev after all overheads.",
        ],
        experiment_ids=["EXP-HYP-HS-LIT-SPECTRUM", "EXP-HYP-HS-SIEVE"],
        notes="Generated from DHSP/lattice literature under the exact independent-state access contract; phase-family records are falsification inputs only.",
    )
    experiments = [
        ExperimentRecord(
            id="EXP-HYP-HS-LIT-SPECTRUM",
            candidate_id=candidate.id,
            title="Literature-mined DCP state-interface mechanism audit",
            status="planned",
            hypothesis="Mechanism records contain reusable operations legal on independent DCP states without stronger oracle access.",
            protocol="Extract state inputs, measurements, branch probabilities, label transforms, and decoder outputs; reject every mechanism requiring an evaluator or selected phase family.",
            positive_signal="A uniform full-family state primitive composes with the exact DCP contract and has a theorem-level resource bound.",
            falsifiers=[
                "The mechanism consumes an evaluator or chosen labels.",
                "The mechanism is defined only on a structured phase subfamily.",
                "No complete decoder or asymptotic resource theorem is extractable.",
            ],
            metrics=["state_native_mechanism_count", "access_mismatch_count", "full_family_count", "complete_decoder_count"],
            dependencies=["literature_records", "reduction_theorem_catalog", "dcp_sample_workbench.py"],
            next_actions=["Extract exact state contracts from source theorems.", "Property-test legal merge primitives."],
        ),
        ExperimentRecord(
            id="EXP-HYP-HS-SIEVE",
            candidate_id=candidate.id,
            title="DCP state-sample merge-rule search constrained by extracted mechanisms",
            status="planned",
            hypothesis="Reusable state-only abstractions induce a uniform full-DCP merge and decoder rule with a better proved resource class.",
            protocol="Search rules over arbitrary uniform D_N labels, charge 1/2 branches and discarded states, and compare complete-decoder bounds to generic DHSP sieves.",
            positive_signal="A theorem proves an asymptotic sample, time, or memory improvement with full reflection recovery and no stronger access.",
            falsifiers=[
                "Merge search rediscovers generic subset-sum sieving.",
                "Any improvement requires evaluator, chosen-label, or family advice.",
                "Postselection, memory, precision, or missing decoder stages erase the improvement.",
            ],
            metrics=["coset_state_queries", "branch_survival", "sample_exponent", "memory_exponent", "decoded_reflection_bits"],
            dependencies=["dcp_sample_workbench.py", "reduction_theorem_catalog", "generic_sieve_baselines"],
            next_actions=["Synthesize implicit state-only merge rules.", "Prove recursive full-reflection decoding."],
        ),
    ]
    return candidate, experiments


def build_coset_state_candidate(records: list[LiteratureMechanismRecord]) -> tuple[CandidateRecord, list[ExperimentRecord]]:
    now = utc_now()
    support = _records_with_tags(records, {"nonabelian-hsp", "hidden-subgroup", "graph-isomorphism", "no-go", "representation-theory"})
    literature_ids = sorted({record.id for record in support}) or ["hsp-survey-2010", "symmetric-defies-fourier-2005"]
    candidate = CandidateRecord(
        id="HYP-LIT-COSET-OBSERVABLES",
        title="Literature-mined collective coset-state observables for hidden permutation problems",
        status="hypothesis",
        created_at=now,
        updated_at=now,
        literature_ids=literature_ids[:8],
        ontology_node_ids=_ontology_ids("nonabelian-hsp", "symmetric-hsp", "graph-isomorphism", "code-equivalence"),
        problem_family=(
            "Hidden permutation instances from graph isomorphism and linear code equivalence over growing sizes, "
            "with controlled automorphism strata and classical canonicalization baselines."
        ),
        input_model=(
            "Efficient coherent preparation of hidden-permutation coset states from explicit graph or generator-matrix inputs, "
            "with register count, state-preparation cost, and verification cost tracked separately."
        ),
        classical_baseline=(
            "Best available graph and code canonicalization, Weisfeiler-Leman/color-refinement variants, support splitting, "
            "automorphism tools, and instance-family-specific classical invariants."
        ),
        reduction_or_lower_bound=(
            "Use the symmetric-group HSP embedding as the reduction frame while requiring a route around the strong-Fourier-sampling no-go theorem."
        ),
        quantum_mechanism=(
            "Search for polynomial-description multi-register observables or tensor-network measurements that distinguish coset states "
            "where single-register strong Fourier sampling provably fails."
        ),
        cost_model=(
            "Count coset-state preparation, number of registers, representation-label manipulation, tensor-network bond dimension, "
            "measurement synthesis, contraction cost, and classical verification."
        ),
        measurement_and_decoding=(
            "Apply collective observables over k coset-state registers, decode candidate permutations or invariant separators, "
            "and verify equivalence or non-equivalence classically."
        ),
        success_statement=(
            "Target theorem: a restricted but classically hard hidden-permutation family admits a polynomial-bond collective observable "
            "with inverse-polynomial distinguishing advantage as instance size grows."
        ),
        complexity_accounting=(
            "Separate coset-state samples, quantum measurement size, tensor contraction complexity, representation-theoretic preprocessing, "
            "and classical verification; compare against the strongest canonicalization baseline."
        ),
        no_go_analysis=(
            "Strong Fourier sampling alone is ruled out for symmetric-group GI-style HSPs; this hypothesis survives only if the observable is genuinely collective "
            "and does not collapse to a classical invariant."
        ),
        dequantization_check=(
            "For each observable, test whether the same separator is reproduced by color refinement, code support splitting, canonical labeling, "
            "or low-rank classical tensor contractions."
        ),
        falsifiers=[
            "All candidate observables reduce to known classical invariants.",
            "Distinguishing advantage vanishes on larger hidden-permutation families.",
            "Required tensor bond dimension grows exponentially.",
            "Classical canonicalization solves every generated hard family.",
        ],
        experiment_ids=["EXP-HYP-COSET-NOGO-MAP", "EXP-HYP-COSET-TENSOR"],
        notes="Generated from nonabelian HSP, symmetric-group no-go, and representation-theory literature records.",
    )
    experiments = [
        ExperimentRecord(
            id="EXP-HYP-COSET-NOGO-MAP",
            candidate_id=candidate.id,
            title="Coset-state no-go boundary map",
            status="planned",
            hypothesis="Some multi-register relation observables escape the strong-Fourier-sampling barrier without reducing to classical refinement.",
            protocol="Generate graph/code hidden-permutation families, compute low-register relation features, and compare against strong Fourier labels and classical invariants.",
            positive_signal="A relation observable separates instances with inverse-polynomial advantage while classical invariants fail.",
            falsifiers=[
                "Observable equals a known classical invariant.",
                "Signal appears only in single-register Fourier labels.",
                "Advantage decays exponentially with instance size.",
            ],
            metrics=["distinguishing_advantage", "classical_invariant_overlap", "register_count", "instance_size_scaling"],
            dependencies=["coset_state_schema", "classical_invariant_suite"],
            next_actions=["Define hidden-permutation family generator.", "Implement invariant-overlap tests."],
        ),
        ExperimentRecord(
            id="EXP-HYP-COSET-TENSOR",
            candidate_id=candidate.id,
            title="Tensor-network search for collective coset observables",
            status="planned",
            hypothesis="A polynomial-bond tensor ansatz can approximate a separating collective measurement on restricted hidden-permutation families.",
            protocol="Optimize k-register tensor observables against generated coset ensembles and audit bond dimension, contraction cost, and classical mimicry.",
            positive_signal="Bond dimension and contraction cost remain polynomial while advantage stays inverse polynomial.",
            falsifiers=[
                "Bond dimension grows exponentially before separation appears.",
                "Low-rank classical contractions match the quantum observable.",
                "Optimized measurement fails outside hand-picked instances.",
            ],
            metrics=["bond_dimension", "contraction_cost", "distinguishing_advantage", "dequantized_tensor_match"],
            dependencies=["tensor_backend", "representation_label_schema"],
            next_actions=["Choose tensor backend.", "Serialize observable ansatzes and contraction certificates."],
        ),
    ]
    return candidate, experiments


def candidate_blueprints(records: list[LiteratureMechanismRecord]) -> list[tuple[CandidateRecord, list[ExperimentRecord]]]:
    blueprints = []
    if _records_with_tags(records, {"hidden-shift", "dihedral-hsp", "gowers-norm"}):
        blueprints.append(build_hidden_shift_candidate(records))
    if _records_with_tags(records, {"nonabelian-hsp", "hidden-subgroup", "graph-isomorphism", "no-go"}):
        blueprints.append(build_coset_state_candidate(records))
    return blueprints


def submit_hypothesis(candidate: CandidateRecord, experiments: list[ExperimentRecord]) -> tuple[bool, list[dict[str, Any]]]:
    """Write accepted candidates or rejected-candidate records with gate issues."""

    payload = asdict(candidate)
    issues = validate_candidate(payload)
    if issues:
        issue_dicts = [issue_to_dict(issue) for issue in issues]
        upsert_rejected_candidate(
            {
                "id": candidate.id,
                "title": candidate.title,
                "rejected_at": datetime.now(timezone.utc).isoformat(),
                "literature_ids": candidate.literature_ids,
                "ontology_node_ids": candidate.ontology_node_ids,
                "issues": issue_dicts,
                "candidate": payload,
            }
        )
        return False, issue_dicts

    upsert_candidate(candidate)
    for experiment in experiments:
        upsert_experiment(experiment)
    return True, []


def hypothesize_from_literature(refresh_arxiv: bool = False, max_arxiv_results: int = 20) -> HypothesisFactoryResult:
    """Generate and register structural hypotheses from literature records."""

    records = extract_literature_records(refresh_arxiv=refresh_arxiv, max_arxiv_results=max_arxiv_results)
    result = HypothesisFactoryResult()
    accepted: list[str] = []
    rejected: list[str] = []
    experiments_written: list[str] = []
    for candidate, experiments in candidate_blueprints(records):
        accepted_flag, _issues = submit_hypothesis(candidate, experiments)
        if accepted_flag:
            accepted.append(candidate.id)
            experiments_written.extend(experiment.id for experiment in experiments)
        else:
            rejected.append(candidate.id)
    return HypothesisFactoryResult(accepted=accepted, rejected=rejected, experiments=experiments_written)
