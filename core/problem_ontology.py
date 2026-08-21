"""Problem ontology and reduction graph for quantum algorithm discovery."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProblemNode:
    id: str
    name: str
    category: str
    status: str
    research_value: str


@dataclass(frozen=True)
class Relation:
    source: str
    target: str
    relation: str
    evidence: str
    implication: str


@dataclass(frozen=True)
class NoGoBarrier:
    id: str
    applies_to: list[str]
    barrier: str
    avoid_by: str
    source_hint: str


NODES = [
    ProblemNode("factoring", "Integer factoring", "number theory", "solved quantumly", "Shor-level template and regression test"),
    ProblemNode("discrete-log", "Discrete logarithm", "number theory", "solved quantumly", "Shor-level template and regression test"),
    ProblemNode("order-finding", "Order finding", "periodicity", "solved quantumly", "Core abelian Fourier mechanism"),
    ProblemNode("abelian-hsp", "Abelian hidden subgroup problem", "hidden structure", "solved quantumly", "General framework behind Shor and Simon"),
    ProblemNode("simon", "Simon's problem", "query complexity", "solved quantumly", "Prototype exponential oracle separation"),
    ProblemNode("hidden-shift", "Hidden shift over abelian groups", "hidden structure", "partially solved", "Bridge from abelian Fourier methods to harder nonabelian-like behavior"),
    ProblemNode("dihedral-hsp", "Dihedral hidden subgroup problem", "hidden structure", "subexponential quantum", "Frontier linked to lattice problems"),
    ProblemNode("unique-svp", "Unique shortest vector problem", "lattice", "frontier", "Cryptographically significant target connected to DHSP"),
    ProblemNode("principal-ideal", "Principal ideal and infrastructure problems", "algebraic number theory", "partially solved quantumly", "Evidence that hidden periodicity extends beyond factoring"),
    ProblemNode("nonabelian-hsp", "Nonabelian hidden subgroup problem", "hidden structure", "frontier", "Possible umbrella for GI/code equivalence breakthroughs"),
    ProblemNode("symmetric-hsp", "Symmetric-group HSP", "hidden structure", "blocked by Fourier no-go", "Canonical barrier for GI and code equivalence"),
    ProblemNode("graph-isomorphism", "Graph isomorphism", "isomorphism", "frontier", "Central test of nonabelian quantum algorithms"),
    ProblemNode("code-equivalence", "Code equivalence", "isomorphism", "frontier", "Cryptographic and algebraic hidden-permutation target"),
    ProblemNode("span-programs", "Span programs/adversary bound", "query synthesis", "mature framework", "Algorithm synthesis route for query problems"),
    ProblemNode("learning-graphs", "Learning graphs", "query synthesis", "mature framework", "Combinatorial route to query algorithms"),
    ProblemNode("quantum-walks", "Quantum walks", "algorithmic framework", "mature with frontier uses", "Geometry-driven alternative to Fourier-only algorithms"),
    ProblemNode("qsvt", "Quantum singular value transformation", "linear algebra framework", "mature and expanding", "Unifying abstraction for matrix-function algorithms"),
    ProblemNode("block-encoding", "Block encoding", "input model", "mature and costly", "Dominant cost center for QSVT-style algorithms"),
    ProblemNode("forrelation", "Forrelation and Fourier checking", "query complexity", "oracle separation", "Useful for discovering new query phenomena"),
    ProblemNode("gowers-structure", "Gowers-uniformity and higher-order Fourier structure", "harmonic analysis", "emerging quantum interface", "Potential hidden-shift and property-testing handle"),
]


RELATIONS = [
    Relation("factoring", "order-finding", "reduces_to", "Shor", "A new order-finding-like primitive can have factoring-scale impact."),
    Relation("discrete-log", "abelian-hsp", "instance_of", "standard HSP formulation", "Abelian HSP coverage is not enough for new breakthroughs."),
    Relation("order-finding", "abelian-hsp", "instance_of", "standard HSP formulation", "Regression tests should recover this structure."),
    Relation("simon", "abelian-hsp", "instance_of", "Z_2^n hidden subgroup", "Useful for oracle-separation tooling, not enough for natural problems."),
    Relation("hidden-shift", "dihedral-hsp", "equivalent_or_related", "Kuperberg/Regev", "Phase-state sieving improvements may affect DHSP."),
    Relation("dihedral-hsp", "unique-svp", "would_imply_progress_on", "Regev reduction", "Efficient DHSP is high-value because of lattice implications."),
    Relation("principal-ideal", "abelian-hsp", "analogy", "Hallgren/infrastructure algorithms", "Look for hidden periodicity in richer algebraic objects."),
    Relation("graph-isomorphism", "symmetric-hsp", "reduces_to_or_embeds_in", "standard GI-HSP reduction", "Need to bypass strong Fourier sampling no-go barriers."),
    Relation("code-equivalence", "symmetric-hsp", "reduces_to_or_embeds_in", "hidden permutation formulation", "Same barrier family as GI but different instance structure."),
    Relation("symmetric-hsp", "nonabelian-hsp", "subproblem_of", "HSP taxonomy", "General nonabelian machinery is the broadest target."),
    Relation("span-programs", "quantum-walks", "constructs", "adversary/span program equivalence", "Query algorithms can be synthesized via linear-algebraic witnesses."),
    Relation("qsvt", "block-encoding", "requires", "QSVT framework", "Any QSVT lead must audit block-encoding cost."),
    Relation("gowers-structure", "hidden-shift", "algorithmic_handle_for", "Roetteler hidden shift algorithms", "Higher-order Fourier metrics should feed hidden-shift experiments."),
]


BARRIERS = [
    NoGoBarrier(
        id="NO-GI-STRONG-FOURIER",
        applies_to=["graph-isomorphism", "symmetric-hsp", "nonabelian-hsp"],
        barrier="Strong Fourier sampling over the symmetric group does not efficiently solve the GI-relevant HSP.",
        avoid_by="Use multi-register entangled measurements with a concrete scalable construction, or leave the HSP formulation.",
        source_hint="Moore-Russell-Schulman, The Symmetric Group Defies Strong Fourier Sampling",
    ),
    NoGoBarrier(
        id="NO-TOY-ORACLE",
        applies_to=["simon", "forrelation"],
        barrier="Oracle separations often fail to transfer to explicit computational problems.",
        avoid_by="Attach every oracle family to either a natural problem, a reduction, or a lower-bound research target.",
        source_hint="Query complexity literature and repeated failure of arbitrary secret-oracle variants in this repo",
    ),
    NoGoBarrier(
        id="NO-QSVT-DATALOADING",
        applies_to=["qsvt", "block-encoding"],
        barrier="State preparation, QRAM, and block-encoding construction can erase claimed speedups.",
        avoid_by="Track access model, encoding cost, precision, and classical randomized baselines as first-class proof obligations.",
        source_hint="QSVT and dequantization literature",
    ),
    NoGoBarrier(
        id="NO-GROVER-ONLY",
        applies_to=["quantum-walks", "learning-graphs"],
        barrier="Many search-space walks give only quadratic speedups.",
        avoid_by="Require spectral/hitting-time evidence that beats unstructured amplitude amplification.",
        source_hint="Quantum walk and query complexity baselines",
    ),
]


def build_problem_ontology() -> dict:
    return {
        "nodes": [asdict(node) for node in NODES],
        "relations": [asdict(relation) for relation in RELATIONS],
        "barriers": [asdict(barrier) for barrier in BARRIERS],
    }


def write_problem_ontology(path: Path) -> dict:
    ontology = build_problem_ontology()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ontology, indent=2, sort_keys=True))
    return ontology


if __name__ == "__main__":
    write_problem_ontology(Path("research/problem_ontology.json"))
