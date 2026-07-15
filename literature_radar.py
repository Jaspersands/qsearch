"""Literature radar for quantum-algorithm research.

This module is deliberately lightweight: it stores a curated seed bibliography
and can optionally refresh metadata from arXiv's public API.  The purpose is to
keep research leads anchored to real mechanisms, barriers, and proof techniques
instead of free-form invention.
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class PaperSeed:
    id: str
    title: str
    url: str
    year: int
    tags: list[str]
    why_it_matters: str


DEFAULT_LITERATURE = [
    PaperSeed(
        id="shor-1994",
        title="Algorithms for quantum computation: discrete logarithms and factoring",
        url="https://arxiv.org/abs/quant-ph/9508027",
        year=1994,
        tags=["period-finding", "abelian-hsp", "number-theory", "breakthrough-template"],
        why_it_matters="Reference model for a Shor-level algorithm: reduction plus Fourier sampling plus classical postprocessing.",
    ),
    PaperSeed(
        id="hsp-survey-2010",
        title="The Hidden Subgroup Problem",
        url="https://arxiv.org/abs/1008.0010",
        year=2010,
        tags=["hidden-subgroup", "nonabelian-hsp", "survey", "representation-theory"],
        why_it_matters="Maps the HSP search space and nonabelian barriers.",
    ),
    PaperSeed(
        id="symmetric-defies-fourier-2005",
        title="The Symmetric Group Defies Strong Fourier Sampling",
        url="https://arxiv.org/abs/quant-ph/0501056",
        year=2005,
        tags=["graph-isomorphism", "nonabelian-hsp", "no-go", "fourier-sampling"],
        why_it_matters="Prevents the project from rediscovering a known-dead GI strategy.",
    ),
    PaperSeed(
        id="beals-symmetric-qft-1997",
        title="Quantum computation of Fourier transforms over symmetric groups",
        url="https://doi.org/10.1145/258533.258548",
        year=1997,
        tags=["symmetric-qft", "representation-theory", "quantum-fourier", "proved-primitive"],
        why_it_matters=(
            "Makes the S_n quantum Fourier transform a solved polynomial-time primitive; a new coset-state route "
            "must identify the additional recoupling and decoding operations rather than relabel QFT as the obstacle."
        ),
    ),
    PaperSeed(
        id="bacon-chuang-harrow-schur-2004",
        title="Efficient Quantum Circuits for Schur and Clebsch-Gordan Transforms",
        url="https://arxiv.org/abs/quant-ph/0407082",
        year=2004,
        tags=["schur-transform", "clebsch-gordan", "generalized-phase-estimation", "proved-primitive"],
        why_it_matters=(
            "Provides efficient Schur-Weyl/Clebsch-Gordan circuits and weak irrep projection, but does not by itself "
            "supply the internal Specht-module Kronecker transform needed by symmetric-group coset-state decoding."
        ),
    ),
    PaperSeed(
        id="ikenmeyer-subramanian-kronecker-2023",
        title="A remark on the quantum complexity of the Kronecker coefficients",
        url="https://arxiv.org/abs/2307.02389",
        year=2023,
        tags=["kronecker-coefficient", "sharp-bqp", "invariant-projector", "representation-theory"],
        why_it_matters=(
            "Places exact Kronecker multiplicity counting in #BQP using commuting projectors; counting an invariant "
            "space is weaker than coherently resolving a basis and its state-dependent transition amplitudes."
        ),
    ),
    PaperSeed(
        id="larocca-havlicek-multiplicities-2024",
        title="Quantum Algorithms for Representation-Theoretic Multiplicities",
        url="https://arxiv.org/abs/2407.17649",
        year=2024,
        tags=["kronecker-coefficient", "multiplicity-estimation", "dimension-ratio", "representation-theory"],
        why_it_matters=(
            "Gives quantum multiplicity algorithms under dimension-ratio restrictions, but the revised paper no "
            "longer supports the original conjecture of a superpolynomial Kronecker advantage on those families."
        ),
    ),
    PaperSeed(
        id="panova-classical-multiplicities-2025",
        title="Polynomial time classical versus quantum algorithms for representation theoretic multiplicities",
        url="https://arxiv.org/abs/2502.20253",
        year=2025,
        tags=["kronecker-coefficient", "classical-algorithm", "dequantization", "representation-theory"],
        why_it_matters=(
            "Classically resolves many restricted Kronecker and plethysm instances previously proposed as quantum "
            "speedups, sharply limiting multiplicity estimation as an independent breakthrough direction."
        ),
    ),
    PaperSeed(
        id="burchardt-high-dimensional-schur-2025",
        title="High-dimensional quantum Schur transforms",
        url="https://arxiv.org/abs/2509.22640",
        year=2025,
        tags=["schur-transform", "multiplicity-space", "recoupling", "representation-theory"],
        why_it_matters=(
            "Corrects a multiplicity-space step that had been treated as a classical permutation and makes the "
            "required quantum isometry/F-moves explicit, a direct warning against hand-waving recoupling registers."
        ),
    ),
    PaperSeed(
        id="yoshida-random-dilation-2025",
        title="Random dilation superchannel",
        url="https://arxiv.org/abs/2512.21260",
        year=2025,
        tags=["kronecker-transform", "schur-transform", "multiplicity-space", "representation-theory"],
        why_it_matters=(
            "Defines the internal S_n Kronecker transform as a basis-change primitive in a circuit identity, but does "
            "not turn that definition into the hidden-involution recoupling and decoding theorem needed here."
        ),
    ),
    PaperSeed(
        id="code-equivalence-fourier-2011",
        title="Quantum Fourier sampling, Code Equivalence, and the quantum security of the McEliece and Sidelnikov cryptosystems",
        url="https://arxiv.org/abs/1111.4382",
        year=2011,
        tags=["code-equivalence", "nonabelian-hsp", "reduction", "classical-no-go", "fourier-sampling"],
        why_it_matters=(
            "States the search code-equivalence HSP construction and warns that HSP measurement hardness is irrelevant "
            "when support splitting or other classical invariants solve the code family."
        ),
    ),
    PaperSeed(
        id="bardet-otmani-saeed-trivial-hull-2019",
        title="Permutation Code Equivalence is not Harder than Graph Isomorphism when Hulls are Trivial",
        url="https://arxiv.org/abs/1905.00073",
        year=2019,
        tags=["code-equivalence", "graph-isomorphism", "hull", "projector", "classical-reduction", "classical-no-go"],
        why_it_matters=(
            "Gives an exact polynomial reduction from trivial-hull permutation code equivalence to weighted graph "
            "isomorphism and a shortening upper bound parameterized by hull dimension, preventing random planted "
            "codes from being treated as independent nonabelian hardness without a hull audit."
        ),
    ),
    PaperSeed(
        id="kuperberg-dhsp-2003",
        title="A subexponential-time quantum algorithm for the dihedral hidden subgroup problem",
        url="https://arxiv.org/abs/quant-ph/0302112",
        year=2003,
        tags=["dihedral-hsp", "hidden-shift", "sieve", "lattice-adjacent"],
        why_it_matters="Core algorithmic template for hidden shift and phase-state combining.",
    ),
    PaperSeed(
        id="regev-lattice-dhsp-2003",
        title="Quantum Computation and Lattice Problems",
        url="https://arxiv.org/abs/cs/0304005",
        year=2003,
        tags=["lattice", "dihedral-hsp", "unique-svp", "reduction"],
        why_it_matters="Connects efficient dihedral HSP progress to lattice breakthroughs.",
    ),
    PaperSeed(
        id="galbraith-shani-multivariate-hnp-2015",
        title="The Multivariate Hidden Number Problem",
        url="https://eprint.iacr.org/2015/111",
        year=2015,
        tags=["hidden-number", "random-multiplier", "noisy-fourier", "access-model", "uniform-samples"],
        why_it_matters=(
            "Separates uniform random-multiplier hidden-number access from chosen-multiplier Fourier methods and warns "
            "that the latter do not automatically solve the uniform distribution model."
        ),
    ),
    PaperSeed(
        id="galbraith-laity-shani-fourier-limitations-2016",
        title="Finding Significant Fourier Coefficients: Clarifications, Simplifications, Applications and Limitations",
        url="https://arxiv.org/abs/1607.01842",
        year=2016,
        tags=["hidden-number", "significant-fourier", "access-model", "chosen-query", "limitations"],
        why_it_matters=(
            "Provides a primary-source guide to significant-Fourier-coefficient algorithms and their access limitations, "
            "preventing chosen-query tools from being imported into random-label DCP decoding without proof."
        ),
    ),
    PaperSeed(
        id="kapralov-sparse-fourier-2016",
        title="Sparse Fourier Transform in Any Constant Dimension with Nearly-Optimal Sample Complexity in Sublinear Time",
        url="https://arxiv.org/abs/1604.00845",
        year=2016,
        tags=["sparse-fourier", "hash-to-bins", "correlated-samples", "access-model", "heavy-hitters"],
        why_it_matters=(
            "Provides a polylogarithmic sparse-spectrum localization benchmark, but its HashToBins measurements use "
            "algorithm-selected shifted and correlated sample locations that must not be conflated with iid DCP labels."
        ),
    ),
    PaperSeed(
        id="roetteler-hidden-shift-gowers-2009",
        title="Quantum algorithms to solve the hidden shift problem for quadratics and for functions of large Gowers norm",
        url="https://arxiv.org/abs/0911.4724",
        year=2009,
        tags=["hidden-shift", "gowers-norm", "quadratic-forms", "harmonic-analysis"],
        why_it_matters="Shows that higher-order Fourier structure is an algorithmic handle, not just a statistic.",
    ),
    PaperSeed(
        id="van-dam-hallgren-shifted-character-2000",
        title="Efficient Quantum Algorithms for Shifted Quadratic Character Problems",
        url="https://arxiv.org/abs/quant-ph/0011067",
        year=2000,
        tags=["hidden-shift", "shifted-character", "multiplicative-character", "finite-fields", "quantum-fourier"],
        why_it_matters="Provides the quantum Fourier template for shifted quadratic characters over finite fields.",
    ),
    PaperSeed(
        id="ip-shift-deconvolution-2002",
        title="Solving Shift Problems and Hidden Coset Problem Using the Fourier Transform",
        url="https://arxiv.org/abs/quant-ph/0205034",
        year=2002,
        tags=["hidden-shift", "shifted-character", "multiplicative-character", "finite-fields", "deconvolution"],
        why_it_matters="Generalizes shifted multiplicative-character recovery through finite-field Fourier deconvolution.",
    ),
    PaperSeed(
        id="bourgain-hidden-shifted-power-2011",
        title="On the Hidden Shifted Power Problem",
        url="https://arxiv.org/abs/1110.0812",
        year=2011,
        tags=["hidden-shifted-power", "shifted-character", "multiplicative-character", "finite-fields", "classical-upper-bound"],
        why_it_matters="Supplies classical query/time upper bounds that prevent shifted-character query gaps from being overstated.",
    ),
    PaperSeed(
        id="bardet-high-rate-alternant-2023",
        title="Polynomial time key-recovery attack on high rate random alternant codes",
        url="https://arxiv.org/abs/2304.14757",
        year=2023,
        tags=["code-equivalence", "alternant-code", "schur-product", "support-recovery", "classical-no-go"],
        why_it_matters="Shows that shortening, componentwise products, conductors, and algebraic recovery can destroy apparent alternant-code hardness.",
    ),
    PaperSeed(
        id="mora-tillich-dual-goppa-square-2021",
        title="On the dimension and structure of the square of the dual of a Goppa code",
        url="https://arxiv.org/abs/2111.13038",
        year=2021,
        tags=["code-equivalence", "goppa-code", "schur-product", "betti-number", "classical-distinguisher"],
        why_it_matters=(
            "Relates the dual Goppa square-code dimension to quadratic relations and supplies rigorous parameter-dependent "
            "bounds for classical distinguishers."
        ),
    ),
    PaperSeed(
        id="randriambololona-syzygy-distinguisher-2024",
        title="The syzygy distinguisher",
        url="https://arxiv.org/abs/2407.15740",
        year=2024,
        tags=["code-equivalence", "alternant-code", "goppa-code", "syzygy", "betti-number", "classical-distinguisher"],
        why_it_matters=(
            "Generalizes square-code tests to higher linear-strand Betti invariants of shortened dual codes and extends "
            "the classical distinguishing regime."
        ),
    ),
    PaperSeed(
        id="couvreur-ag-code-closure-2014",
        title="Cryptanalysis of public-key cryptosystems that use subcodes of algebraic geometry codes",
        url="https://arxiv.org/abs/1409.8220",
        year=2014,
        tags=["code-equivalence", "algebraic-geometry-code", "schur-product", "t-closure", "support-recovery", "classical-no-go"],
        why_it_matters=(
            "Introduces t-closure-based polynomial attacks that can reconstruct ambient algebraic-geometry codes "
            "from subcodes, closing a major gap left by dimension-only Schur tests."
        ),
    ),
    PaperSeed(
        id="astore-rank-metric-geometric-invariant-2024",
        title="A geometric invariant of linear rank-metric codes",
        url="https://arxiv.org/abs/2411.19087",
        year=2024,
        tags=["code-equivalence", "rank-metric", "schur-product", "geometric-invariant", "classical-baseline"],
        why_it_matters="Extends Schur-power dimension-sequence thinking to geometric invariants that distinguish Gabidulin structure.",
    ),
    PaperSeed(
        id="hallgren-pell-2002",
        title="Polynomial-Time Quantum Algorithms for Pell's Equation and the Principal Ideal Problem",
        url="https://authors.library.caltech.edu/records/wwa5n-3k633",
        year=2002,
        tags=["number-theory", "principal-ideal", "infrastructure", "periodicity"],
        why_it_matters="A non-Shor number-theoretic breakthrough template based on hidden periodic structure.",
    ),
    PaperSeed(
        id="span-programs-adversary-2009",
        title="Span programs and quantum query complexity: The general adversary bound is nearly tight for every boolean function",
        url="https://arxiv.org/abs/0904.2759",
        year=2009,
        tags=["query-complexity", "span-programs", "adversary-bound", "quantum-walks"],
        why_it_matters="Turns lower-bound machinery into algorithm synthesis machinery for query problems.",
    ),
    PaperSeed(
        id="qsvt-2018",
        title="Quantum singular value transformation and beyond",
        url="https://arxiv.org/abs/1806.01838",
        year=2018,
        tags=["qsvt", "block-encoding", "hamiltonian-simulation", "linear-algebra"],
        why_it_matters="Modern unifying framework for many quantum algorithms; useful for abstraction mining.",
    ),
    PaperSeed(
        id="cs-guide-qsvt-2023",
        title="A CS guide to the quantum singular value transformation",
        url="https://arxiv.org/abs/2302.14324",
        year=2023,
        tags=["qsvt", "exposition", "block-encoding", "algorithm-framework"],
        why_it_matters="Makes QSVT components easier to represent as reusable program abstractions.",
    ),
    PaperSeed(
        id="program-synthesis-components-2023",
        title="Discovering Quantum Circuit Components with Program Synthesis",
        url="https://arxiv.org/abs/2305.01707",
        year=2023,
        tags=["program-synthesis", "component-library", "automation", "circuit-synthesis"],
        why_it_matters="Useful for subroutine discovery, but must be subordinated to scalable math structure.",
    ),
    PaperSeed(
        id="automated-algorithm-synthesis-2025",
        title="Automated Quantum Algorithm Synthesis",
        url="https://arxiv.org/html/2503.08449v2",
        year=2025,
        tags=["automated-discovery", "algorithm-synthesis", "known-algorithms", "generalization"],
        why_it_matters="Evidence that example-driven synthesis can rediscover structure; also a warning about rediscovery-only systems.",
    ),
    PaperSeed(
        id="gowers-norm-algorithms-2025",
        title="Quantum Algorithms for Gowers Norm Estimation, Polynomial Structure Testing, and Counting Arithmetic Progressions",
        url="https://arxiv.org/abs/2508.01231",
        year=2025,
        tags=["gowers-norm", "property-testing", "higher-order-fourier", "finite-fields"],
        why_it_matters="Recent signal that higher-order harmonic analysis is an active quantum algorithms interface.",
    ),
    PaperSeed(
        id="randomized-qsvt-2025",
        title="Randomized Quantum Singular Value Transformation",
        url="https://arxiv.org/abs/2510.06851",
        year=2025,
        tags=["qsvt", "randomization", "early-fault-tolerant", "linear-systems"],
        why_it_matters="Suggests a frontier around replacing costly block encodings with randomized primitives.",
    ),
    PaperSeed(
        id="state-isomorphism-2026",
        title="Quantum state isomorphism problems for groups",
        url="https://arxiv.org/abs/2605.12615",
        year=2026,
        tags=["group-actions", "hidden-shift", "state-isomorphism", "complexity"],
        why_it_matters="Recent nearby problem class linking group actions, quantum states, and hidden-shift style structure.",
    ),
    PaperSeed(
        id="near-term-ai-discovery-2026",
        title="Automated near-term quantum algorithm discovery for molecular ground states",
        url="https://arxiv.org/abs/2603.26359",
        year=2026,
        tags=["automated-discovery", "quantum-chemistry", "heuristics", "interpretability"],
        why_it_matters="Shows useful automation patterns, but targets heuristic near-term chemistry rather than Shor-level complexity.",
    ),
    PaperSeed(
        id="proof-quantum-programs-2020",
        title="Proving Quantum Programs Correct",
        url="https://arxiv.org/abs/2010.01240",
        year=2020,
        tags=["formal-verification", "proof-assistant", "quantum-programs", "correctness"],
        why_it_matters="Points toward proof-checking candidate algorithms rather than trusting generated explanations.",
    ),
]


def _arxiv_id_from_url(url: str) -> str | None:
    marker = "arxiv.org/abs/"
    if marker not in url:
        return None
    return url.split(marker, 1)[1].split("#", 1)[0]


def fetch_arxiv_metadata(arxiv_ids: Iterable[str], timeout: int = 20) -> list[dict]:
    ids = [arxiv_id for arxiv_id in arxiv_ids if arxiv_id]
    if not ids:
        return []
    query = urllib.parse.urlencode({"id_list": ",".join(ids)})
    url = f"https://export.arxiv.org/api/query?{query}"
    with urllib.request.urlopen(url, timeout=timeout) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    records = []
    for entry in root.findall("atom:entry", ns):
        records.append(
            {
                "id": entry.findtext("atom:id", default="", namespaces=ns),
                "title": " ".join(entry.findtext("atom:title", default="", namespaces=ns).split()),
                "summary": " ".join(entry.findtext("atom:summary", default="", namespaces=ns).split()),
                "published": entry.findtext("atom:published", default="", namespaces=ns),
                "updated": entry.findtext("atom:updated", default="", namespaces=ns),
                "authors": [
                    author.findtext("atom:name", default="", namespaces=ns)
                    for author in entry.findall("atom:author", ns)
                ],
            }
        )
    return records


def build_literature_index(refresh_arxiv: bool = False) -> dict:
    seeds = [asdict(seed) for seed in DEFAULT_LITERATURE]
    index = {"seed_papers": seeds, "tag_index": {}, "arxiv_metadata": []}
    tag_index: dict[str, list[str]] = {}
    for seed in DEFAULT_LITERATURE:
        for tag in seed.tags:
            tag_index.setdefault(tag, []).append(seed.id)
    index["tag_index"] = dict(sorted(tag_index.items()))

    if refresh_arxiv:
        arxiv_ids = [_arxiv_id_from_url(seed.url) for seed in DEFAULT_LITERATURE]
        index["arxiv_metadata"] = fetch_arxiv_metadata([x for x in arxiv_ids if x])
    return index


def write_literature_index(path: Path, refresh_arxiv: bool = False) -> dict:
    index = build_literature_index(refresh_arxiv=refresh_arxiv)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(index, indent=2, sort_keys=True))
    return index


if __name__ == "__main__":
    write_literature_index(Path("research/literature_index.json"), refresh_arxiv=False)
