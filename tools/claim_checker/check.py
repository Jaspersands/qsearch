"""Read the fine print of a quantum-advantage claim.

    python tools/claim_checker/check.py 0811.3171                 # fetch the abstract from arXiv
    python tools/claim_checker/check.py --file abstract.txt
    python tools/claim_checker/check.py 2408.08292 --json

Flags the caveats that most often turn an advantage claim into a negative result:
input loading, readout, oracle-only separations, heuristic assumptions, finite or
numerical evidence, restricted classical baselines and parameter dependence. Every flag
quotes the sentence that raised it. A caveat that the sentence itself rules out ("does not
require QRAM", "oracle-free", "independent of the condition number") is listed separately
as apparently ruled out, still with its quote. The nearest Q-Search negatives and their
lessons come from the corpus index.

This reads the abstract only, in English. A missing flag means the abstract does not raise
the issue, not that the paper is clear of it.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


@dataclass(frozen=True)
class FlagSpec:
    title: str
    mode: str  # failure mode in tools/audit/failure_modes.py
    question: str
    patterns: tuple[str, ...]


DATA_WORDS = r"matri(x|ces)|vectors?|data ?sets?|database|directory|entries|items|names|records|preference|data points|training data|N by N"
SUBLINEAR = (
    r"poly\s*\(\s*log|polylog|poly-?logarithmic|logarithmic in the (dimension|size)|O\(\s*\\?sqrt\s*\(?\s*N|O\(\s*√N"
    r"|time (that is )?(sub-?linear|polylogarithmic)"
)

FLAGS: dict[str, FlagSpec] = {
    "input_loading": FlagSpec(
        "Input loading",
        "state_prep",
        "How is the input loaded, and is that cost charged? A sublinear-time claim on classical data "
        "needs a quantum access model (QRAM, block encoding, copies of a state).",
        (
            r"\bQRAM\b|quantum random access memory|quantum access to|quantum data structure|data structure",
            r"given (multiple |many |several )?copies|copies of (an? |the )?(unknown )?(quantum )?(state|system)",
            r"state preparation|prepar(e|ing) the (input|initial) state|amplitude encod|load(ing)? (the )?(data|input|vector|matrix)",
            r"block[- ]encod|oracle access to the (data|matrix|entries)",
        ),
    ),
    "readout": FlagSpec(
        "Readout",
        "readout",
        "What exactly is output? A quantum state, a sample or an estimate is weaker than the full answer; "
        "is the classical competitor allowed the same relaxation?",
        (
            r"expectation values?",
            r"estimat(e|es|ing) (the |an? )?(overlap|propert(y|ies)|value|amplitude)",
            r"outputs? (a|the) (quantum )?state|quantum state (proportional|encoding|whose amplitudes)",
            r"sampl(e|es|ing) (efficiently )?from (an? |the )?(approximation|distribution|low-rank)",
            r"amplitude estimation",
        ),
    ),
    "oracle_model": FlagSpec(
        "Oracle-only separation",
        "hidden_advice",
        "Is the separation only relative to an oracle? Can the oracle be instantiated by an efficient, natural function?",
        (r"(?<!non-)\boracles?\b|(?<!non-)\boracular\b|black[- ]box|query complexity|random oracle model",),
    ),
    "heuristic_assumption": FlagSpec(
        "Heuristic assumption",
        "proof_gap",
        "Which conjecture or heuristic does correctness or hardness rest on, and how well is it supported?",
        (
            r"heuristic assumption|\bconjectur|unproven|plausible (assumption|conjecture)",
            r"relies on (a|an|the) [\w-]+( [\w-]+)? (assumption|hypothesis)",
            r"under (a|the) [\w-]+( [\w-]+)? (assumption|hypothesis)|\bassuming (a|that|the)\b",
        ),
    ),
    "numerical_only": FlagSpec(
        "Numerical or finite evidence",
        "finite_size",
        "Is the advantage shown asymptotically, or only on finite instances or simulations?",
        (
            r"numerical(ly)? (simulations?|experiments?|evidence|results?|studies)|numerical(ly)? (find|show|observe)",
            r"simulations? (of )?up to|up to \d+ (qubits|variables|nodes)|empirical(ly)?",
            r"we construct an? [\w-]+( [\w-]+)? instance|on (this|these|small) instances?|finite[- ]size",
        ),
    ),
    "restricted_baseline": FlagSpec(
        "Restricted classical baseline",
        "classical_competitor",
        "Is the comparison against the best classical algorithm, including tailored and quantum-inspired ones, "
        "or only against generic heuristics or one class of methods?",
        (
            r"(general-purpose|generic) (classical )?(heuristics?|solvers?|methods?|algorithms?)",
            r"simulated annealing|known to us",
            r"(tailored|specialized|specialised|dedicated) classical (solver|algorithm|method)s?[^.]{0,20}(outperform|beat|match)",
            r"classical (solver|algorithm|method)s? (can|could|may) (outperform|beat|match)",
            r"all known classical algorithms[^.]{0,80}that (work|use|rely)",
        ),
    ),
    "parameter_dependence": FlagSpec(
        "Parameter dependence",
        "resource_blowup",
        "How do condition number, sparsity, rank, gap or precision scale on the instances that matter?",
        (r"condition number|\bkappa\b|κ|\bsparse\b|sparsity|spectral gap|\bprecision\b|low[- ]rank|rank-\$?k",),
    ),
}

CLAIMS = (
    ("exponential", r"exponential(ly)? (quantum )?(speed-?up|faster|improvement|advantage|separation)|super-?polynomial (quantum )?(speed-?up|advantage|separation)"
                    r"|(hard|intractable) (on|for) (a )?classical|no classical algorithm can"),
    ("polynomial", r"quadratic (quantum )?(speed-?up|improvement|advantage)|polynomial (quantum )?speed-?up|O\(\s*\\?sqrt|√N|square[- ]root speed"),
)


@dataclass
class Flag:
    name: str
    title: str
    mode: str
    question: str
    quote: str
    match: str
    negated: bool = False


@dataclass
class Report:
    title: str
    claim: str
    claim_quote: str
    flags: list[Flag]
    sentences: int
    neighbours: list[dict] = field(default_factory=list)


_ABBREV = re.compile(r"\b(e\.g|i\.e|et al|cf|vs|resp|Fig|Eq|Ref)\.$", re.I)


def split_sentences(text: str) -> list[str]:
    """Split on sentence ends followed by an upper-case start; keep e.g./i.e. inside sentences."""
    sentences, start = [], 0
    for match in re.finditer(r"[.!?](?=\s+[A-Z$\\(\[])", text):
        end = match.end()
        if _ABBREV.search(text[start:end]):
            continue
        piece = text[start:end].strip()
        if piece:
            sentences.append(piece)
        start = end
    tail = text[start:].strip()
    if tail:
        sentences.append(tail)
    return sentences


# A negation within the six words before a match, in the same clause (six, so that "does not require
# QRAM or any quantum data structure" covers both items), or "-free" right after it.
_NEGATION_WORDS = frozenset("not no without never nor neither unlike non".split())
_NEGATION_PHRASES = re.compile(r"\b(independent of|free of|instead of|rather than)\b|n't\b", re.I)


def is_negated(sentence: str, match: re.Match) -> bool:
    if re.match(r"\s*-?\s*free\b", sentence[match.end():], re.I):
        return True
    clause = re.split(r"[,;:]", sentence[: match.start()])[-1]
    words = clause.split()[-6:]
    if any(word.strip("(\"'").lower() in _NEGATION_WORDS for word in words):
        return True
    return bool(_NEGATION_PHRASES.search(" ".join(clause.split()[-7:])))


def _continues_list(gap: str) -> bool:
    """True when the text between two matches only extends a list: ", ", " and ", " or estimate "."""
    if re.search(r"[;:.]", gap):
        return False
    words = re.findall(r"[\w-]+", gap)
    return len(words) <= 2 and (not words or words[0].lower() in {"and", "or", "nor"})


def _first_flag(name: str, spec: FlagSpec, sentences: list[str], patterns: tuple[str, ...]) -> Flag | None:
    """The first plain mention; failing that, the first negated one. Matches are read in sentence order,
    and a negation carries along a list ("independent of the condition number, sparsity and precision")."""
    fallback = None
    for sentence in sentences:
        matches = sorted((m for pattern in patterns for m in re.finditer(pattern, sentence, re.I)), key=lambda m: m.start())
        previous = None
        for match in matches:
            if previous is not None and match.start() < previous[0].end():
                continue  # overlapping alternatives
            negated = is_negated(sentence, match) or bool(
                previous and previous[1] and _continues_list(sentence[previous[0].end():match.start()]))
            previous = (match, negated)
            flag = Flag(name, spec.title, spec.mode, spec.question, sentence, match.group(0), negated)
            if not negated:
                return flag
            fallback = fallback or flag
    return fallback


def check_text(abstract: str, title: str = "") -> Report:
    text = f"{title}. {abstract}" if title else abstract
    sentences = split_sentences(text)
    flags: list[Flag] = []
    for name, spec in FLAGS.items():
        flag = _first_flag(name, spec, sentences, spec.patterns)
        if flag:
            flags.append(flag)
    loading = next((f for f in flags if f.name == "input_loading"), None)
    if (loading is None or loading.negated) and re.search(DATA_WORDS, text, re.I):
        sublinear = _first_flag("input_loading", FLAGS["input_loading"], sentences, (SUBLINEAR,))
        if sublinear and (loading is None or not sublinear.negated):
            flags = [f for f in flags if f.name != "input_loading"] + [sublinear]
    claim, claim_quote = "none-stated", ""
    for label, pattern in CLAIMS:
        hit = next((s for s in sentences if re.search(pattern, s, re.I)), None)
        if hit:
            claim, claim_quote = label, hit
            break
    order = list(FLAGS)
    flags.sort(key=lambda f: order.index(f.name))
    return Report(title=title, claim=claim, claim_quote=claim_quote, flags=flags, sentences=len(sentences))


def neighbours(text: str, root: Path, k: int = 5) -> list[dict]:
    """Nearest retained negatives in the corpus index, with their lessons."""
    from tools.corpus.api import Corpus
    from tools.corpus.docs import read_json

    corpus = Corpus(root)
    corpus.refresh()
    registry = {r["id"]: r for r in read_json(root / "research" / "registry" / "negative_results.json") if isinstance(r, dict)}
    rows = []
    for hit in corpus.search(text, kinds=("negative",), k=k):
        record = registry.get(hit.doc_id.split(":", 1)[-1], {})
        rows.append({
            "doc_id": hit.doc_id,
            "title": hit.title,
            "location": hit.location,
            "reason": record.get("reason_invalid", ""),
            "lesson": record.get("lesson", ""),
        })
    return rows


def render(report: Report, source: str = "") -> str:
    lines = [f"# Claim check: {report.title or source or 'abstract'}", ""]
    if source:
        lines += [f"Source: {source}", ""]
    lines += [
        "Abstract only: a missing flag means the abstract does not raise the issue, not that the paper is clear of it.",
        "",
        f"Claimed advantage: **{report.claim}**" + (f". \"{report.claim_quote}\"" if report.claim_quote else ""),
        "",
        "## Flags",
        "",
    ]
    raised = [flag for flag in report.flags if not flag.negated]
    ruled_out = [flag for flag in report.flags if flag.negated]
    if not raised:
        lines.append("None raised by the abstract.")
    for flag in raised:
        lines.append(f"- **{flag.title}** (`{flag.name}`, failure mode `{flag.mode}`): \"{flag.quote}\"")
    if ruled_out:
        lines += ["", "## Apparently ruled out", "",
                  "The abstract mentions these caveats with a negation. Check the quote: the paper may still depend on them.", ""]
        for flag in ruled_out:
            lines.append(f"- **{flag.title}** (`{flag.name}`): \"{flag.quote}\"")
    lines += ["", "## Questions to ask", ""]
    for flag in report.flags:
        lines.append(f"- {flag.question}")
    if not report.flags:
        lines.append("- Who supplies the input, what is output, and what is the best classical algorithm for the same task?")
    lines += ["", "## Nearest Q-Search records", ""]
    if not report.neighbours:
        lines.append("Not looked up.")
    for row in report.neighbours:
        text = row.get("lesson") or ""
        lesson = f" Lesson: {text[:300]}{'...' if len(text) > 300 else ''}" if text else ""
        lines.append(f"- `{row['doc_id']}` {row.get('title', '')[:160]}.{lesson}")
    return "\n".join(lines).rstrip() + "\n"


def _default_client():
    from tools.audit.rediscovery import CACHE_DIR, PacedOpener
    from tools.corpus.sources.arxiv import Client

    cache = Path(__file__).resolve().parents[2] / CACHE_DIR
    return Client(opener=PacedOpener(cache), delay=0.0, cache_dir=cache)


def main(argv: list[str] | None = None, client=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("arxiv_ids", nargs="*", help="arXiv ids, e.g. 0811.3171 or quant-ph/9508027")
    parser.add_argument("--file", type=Path, help="A text file holding an abstract.")
    parser.add_argument("--text", help="Abstract text.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-corpus", action="store_true", help="Skip the nearest-negative lookup.")
    args = parser.parse_args(argv)

    items: list[tuple[str, str, str]] = []  # (source, title, abstract)
    if args.file:
        items.append((str(args.file), "", args.file.read_text(encoding="utf-8")))
    if args.text:
        items.append(("text", "", args.text))
    if args.arxiv_ids:
        for paper in (client or _default_client()).get(args.arxiv_ids):
            items.append((f"arXiv:{paper.arxiv_id}", paper.title, paper.abstract))
    if not items:
        parser.error("give arXiv ids, --file or --text")

    outputs = []
    for source, title, abstract in items:
        report = check_text(abstract, title=title)
        if not args.no_corpus:
            report.neighbours = neighbours(f"{title} {abstract}", args.root)
        outputs.append((source, report))
    if args.json:
        print(json.dumps([{"source": s, **asdict(r)} for s, r in outputs], indent=1))
    else:
        print("\n".join(render(r, source=s) for s, r in outputs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
