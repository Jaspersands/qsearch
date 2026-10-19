"""Research tracks the watch follows: an arXiv query, text patterns and matching seed tags."""

from __future__ import annotations

import re
from dataclasses import dataclass

CATEGORIES = "(cat:quant-ph OR cat:cs.CC OR cat:cs.DS OR cat:cs.CR OR cat:cs.IT OR cat:math.RT OR cat:math.NT)"


@dataclass(frozen=True)
class Track:
    phrases: tuple[str, ...]  # arXiv abstract phrases that define the query
    patterns: tuple[str, ...]  # regexes (case-insensitive) that place a paper on this track
    seed_tags: frozenset[str]  # literature seed tags that belong to this track
    core: bool = True  # peripheral tracks never raise a kill or scoop label on their own

    def arxiv_query(self) -> str:
        terms = " OR ".join(f'abs:"{phrase}"' for phrase in self.phrases)
        return f"({terms}) AND {CATEGORIES}"

    def matches(self, text: str) -> bool:
        return any(re.search(pattern, text, re.I) for pattern in self.patterns)


TRACKS: dict[str, Track] = {
    "dcp": Track(
        ("dihedral coset", "dihedral hidden subgroup", "Kuperberg sieve", "dihedral coset problem"),
        (r"dihedral", r"kuperberg", r"\bDCP\b", r"collimation sieve"),
        frozenset({"dihedral-coset", "dihedral-hsp", "dcp-label-digest"}),
    ),
    "hidden_shift": Track(
        ("hidden shift", "shifted character", "hidden shifted power"),
        (
            r"hidden[- ]shift",
            r"shifted (quadratic )?character",
            r"shifted power",
            r"gowers norm",
            r"shift problems?",
            r"hidden coset",
            r"multiplicative character",
        ),
        frozenset({"hidden-shift", "shifted-character", "hidden-shifted-power", "gowers-norm"}),
    ),
    "nonabelian_hsp": Track(
        ("hidden subgroup problem", "coset states", "strong Fourier sampling"),
        (r"hidden subgroup", r"coset state", r"fourier sampling", r"graph isomorphism", r"period[- ]finding"),
        frozenset({"nonabelian-hsp", "hidden-subgroup", "abelian-hsp", "graph-isomorphism", "coset-state", "period-finding"}),
    ),
    "representation": Track(
        ("symmetric group", "Schur transform", "Kronecker coefficient", "plethysm", "quantum Fourier transform over"),
        (
            r"symmetric group",
            r"schur transform",
            r"clebsch[- ]gordan",
            r"kronecker coefficient",
            r"plethysm",
            r"fourier transform (for|over) (the )?(symmetric|nonabelian|finite|semisimple)",
            r"irreducible representation",
            r"character (bound|ratio)",
            r"wreath product",
            r"semisimple algebra",
            r"representation[- ]theoretic",
            r"kronecker",
            r"finite simple group",
            r"group QFT",
        ),
        frozenset(
            {
                "symmetric-qft", "wreath-qft-toolbox", "diagram-algebra-qft", "schur-transform", "kronecker-coefficient",
                "symmetric-character", "multiplicity-estimation", "maximal-irrep-dimension", "symmetric-group",
                "kronecker-transform", "branching-multiplicity",
            }
        ),
    ),
    "code_equivalence": Track(
        ("code equivalence", "Goppa code", "alternant code", "McEliece"),
        (
            r"code equivalence",
            r"goppa",
            r"alternant code",
            r"mceliece",
            r"schur product",
            r"rank[- ]metric code",
            r"syzygy",
            r"dual codes?\b",
            r"algebraic[- ]geometry codes?",
            r"subcodes",
            r"square[- ]code",
        ),
        frozenset({"code-equivalence", "goppa-code", "alternant-code"}),
    ),
    "dqi_opi": Track(
        ("decoded quantum interferometry", "optimal polynomial intersection"),
        (r"decoded quantum interferometry", r"\bDQI\b", r"optimal polynomial intersection", r"\bOPI\b"),
        frozenset({"dqi", "opi"}),
    ),
    "bpqm_gibbs": Track(
        ("belief propagation with quantum messages", "quantum Gibbs sampling", "Gibbs state preparation"),
        (r"belief propagation with quantum messages", r"\bBPQM\b", r"gibbs (state|sampl)", r"quantum belief propagation"),
        frozenset({"bpqm", "gibbs"}),
    ),
    "lattice": Track(
        ("learning with errors", "shortest vector problem", "lattice problems", "bounded distance decoding"),
        (r"learning with errors", r"\bLWE\b", r"shortest vector", r"\bSVP\b", r"lattice (problem|algorithm|reduction)", r"bounded distance decoding"),
        frozenset({"lattice", "unique-svp"}),
    ),
    "number_theory": Track(
        ("factoring", "discrete logarithm", "principal ideal", "class group", "Pell equation"),
        (r"factoring", r"discrete log", r"principal ideal", r"class (group|number)", r"unit group", r"\bpell", r"regulator", r"regev"),
        frozenset({"number-theory", "principal-ideal"}),
    ),
    "state_discrimination": Track(
        ("pretty good measurement", "quantum state discrimination", "Helstrom"),
        (
            r"pretty[- ]good measurement",
            r"state discrimination",
            r"helstrom",
            r"accessible (classical )?(information|correlation)",
            r"\blocking\b",
        ),
        frozenset({"state-discrimination", "pretty-good-measurement", "pgm-implementation", "quantum-data-locking", "accessible-information"}),
    ),
    "dequantization": Track(
        ("dequantization", "dequantized", "classical simulation of quantum algorithms"),
        (r"dequantiz",),
        frozenset({"dequantization"}),
        core=False,
    ),
    "qsvt": Track(
        ("quantum singular value transformation", "block encoding"),
        (r"singular value transformation", r"\bQSVT\b", r"block[- ]encoding"),
        frozenset({"qsvt", "block-encoding"}),
        core=False,
    ),
    "algorithm_discovery": Track(
        ("automated quantum algorithm discovery", "quantum algorithm synthesis", "program synthesis quantum"),
        (r"(automated|automatic) (quantum )?algorithm (discovery|synthesis)", r"program synthesis", r"algorithm discovery"),
        frozenset({"automated-discovery", "algorithm-synthesis", "program-synthesis"}),
        core=False,
    ),
    "query_and_fourier": Track(
        ("hidden number problem", "sparse Fourier transform", "quantum query complexity", "adversary bound"),
        (r"hidden number", r"sparse fourier", r"significant fourier", r"query complexity", r"adversary bound", r"span program", r"index erasure"),
        frozenset({"hidden-number", "sparse-fourier", "significant-fourier", "query-complexity", "span-programs", "adversary-bound", "query-lower-bound", "index-erasure"}),
        core=False,
    ),
}


def classify(text: str) -> list[str]:
    """Tracks whose patterns appear in the text, in TRACKS order."""
    return [name for name, track in TRACKS.items() if track.matches(text)]
