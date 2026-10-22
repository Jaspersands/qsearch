"""Judge the arXiv watch's unreviewed flags with in-session subagents.

    python tools/arxiv_watch/judge.py --export DIR [--batches 3]
    python tools/arxiv_watch/judge.py --import DIR/out/*.jsonl --judge NAME

A flag is a stored paper labelled possible-kill or possible-scoop with no verdict in
research/audits/arxiv_verdicts.json. Export writes INSTRUCTIONS.md and batch files; each item
carries the paper's abstract and its nearest Q-Search records, each with the first 600
characters of its text, so the judge can compare the paper with what the project claims.

A fresh subagent reads INSTRUCTIONS.md and one batch and writes one JSONL row per paper. Import
keeps a row only when its quote (at least six words) appears verbatim in the abstract or in the
one excerpt it names, as the batch showed them (DIR/out/batch_NN.jsonl is checked against
DIR/batch_NN.json), and never replaces a verdict recorded by anyone but a judge. Kept rows are
stored with by = "judge:NAME", copied onto the stored papers and listed in the digest's Reviewed
table.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sqlite3
import string
import sys
import unicodedata
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.arxiv_watch.verdicts import (  # noqa: E402
    JUDGE_PREFIX, VERDICTS, by_judge, load_verdicts, save_verdicts, verdict_entry,
)
from tools.arxiv_watch.watch import FLAGGED, _load_state, _save, attach_verdicts, checkout_error  # noqa: E402
from tools.audit.rediscovery import _rows  # noqa: E402
from tools.corpus.api import Corpus  # noqa: E402

EXCERPT_CHARS = 600
MIN_QUOTE_WORDS = 6
MEANINGS = {
    "kill": "The paper invalidates a project claim or retained result, for example a classical algorithm or bound "
            "that removes a quantum advantage a note claims.",
    "scoop": "The paper publishes, as its own, a result the project presents as new.",
    "should-cite": "No conflict, but a named project document should cite the paper or narrow a sentence.",
    "related-only": "Shared topic; nothing to do.",
    "false-alarm": "The wording cue or the corpus match is spurious.",
}

JUDGE_INSTRUCTIONS = """\
# arXiv watch: judging flagged papers

The arXiv watch labels new papers from wording cues. A `possible-kill` or `possible-scoop`
label is triage, not judgement. Your job is the judgement: for each paper in your batch,
decide what it means for the Q-Search project.

Each paper comes with its title, abstract, label, the cues that raised the label, its tracks
and its nearest Q-Search records (`nearest`), each with a `doc_id`, a `title` and an `excerpt`
(the first 600 characters of the record). You may read the repository (notes under
`research/`, the registry under `research/registry/`) to check what the project claims. Write
nothing except your output file, and do not search the web.

Pick one verdict per paper:

- `kill`: the paper invalidates a project claim or retained result, for example a classical
  algorithm or bound that removes a quantum advantage a note claims.
- `scoop`: the paper publishes, as its own, a result the project presents as new.
- `should-cite`: no conflict, but a named project document should cite the paper or narrow a
  sentence.
- `related-only`: shared topic; nothing to do.
- `false-alarm`: the wording cue or the corpus match is spurious.

For each paper give:

1. `verdict`: one of the five above.
2. `reason`: one or two sentences saying why, naming the project document or record the paper
   bears on.
3. `quote`: at least 6 words copied verbatim from the paper's abstract or from one nearest
   record's excerpt, supporting the verdict, with `quote_from` set to `"abstract"` or to that
   record's `doc_id`. The quote must lie inside that one text. A quote that runs from the
   abstract into an excerpt, or from one excerpt into the next, is rejected, and so is a quote
   from a file you opened yourself. Copy the maths exactly as written: Greek letters (κ, Ω),
   signs and operators (≤, +, -, /, !, %, #, ×), exponents and subscripts (^, _, ², ₁), primes
   (`W'`, `f'(x)`), decimal points, braces and TeX commands (`\\Omega` is not `\\omega`, and
   `Omega` is not `omega`), and the case of one-letter symbols (`O(n)` is not `o(n)`, `N` is
   not `n`). Only spacing, the case of ordinary words, and punctuation between words (. , ; : ?
   quote marks, apostrophes, a dash between clauses, TeX's `$`) may differ. Start and end the
   quote on whole words, not inside a formula or a hyphenated word: not just after a sign, an
   operator, a fraction bar, a root or a function such as `\\log`, and not just before an
   operator, an exponent, a factorial, a percent sign or a prime. Quotes are checked
   automatically; a paper whose quote is not found gets no verdict.
4. `action`: one line naming what a document should change (cite the paper in X, narrow
   sentence Y of note Z), or null when nothing is to be done.
5. `confidence`: your probability (0 to 1) that the verdict is right.

Write one JSON object per line (JSONL), one line per paper, to your output path:

{"arxiv_id": "2610.12345", "verdict": "should-cite", "reason": "...", "quote": "...", "quote_from": "abstract", "action": "Cite it in research/X.md next to ...", "confidence": 0.8}

Do not skip papers. Papers that already have a human verdict are not in your batch, and a row
for one is rejected at import.
"""


def pending(state: dict) -> list[tuple[str, dict]]:
    """Stored possible kills and scoops without a verdict, sorted by arXiv id."""
    flags = [(arxiv_id, record) for arxiv_id, record in state["papers"].items()
             if record.get("label") in FLAGGED and "verdict" not in record]
    return sorted(flags, key=lambda item: item[0])


def _corpus(root: Path) -> Corpus:
    corpus = Corpus(root)
    corpus.refresh()
    return corpus


def _excerpt(corpus: Corpus, doc_id: str) -> str:
    doc = corpus.get(doc_id)
    return doc.text[:EXCERPT_CHARS] if doc is not None else ""


def _item(arxiv_id: str, record: dict, corpus: Corpus) -> dict:
    return {
        "arxiv_id": arxiv_id,
        "title": record["title"],
        "abstract": record.get("abstract", ""),
        "label": record["label"],
        "cues": record.get("cues", []),
        "tracks": record.get("tracks", []),
        "nearest": [
            {"doc_id": near["doc_id"], "title": near["title"], "excerpt": _excerpt(corpus, near["doc_id"])}
            for near in record.get("nearest", [])
        ],
    }


def export_batches(root: Path, out_dir: Path, n_batches: int = 3, corpus: Corpus | None = None) -> list[Path]:
    """Write INSTRUCTIONS.md and batch_NN.json (papers dealt round-robin); returns the batches written.

    The verdicts file is read here, so a paper reviewed since the last watch run is left out.
    """
    if n_batches < 1:
        raise ValueError("n_batches must be at least 1")
    root, out_dir = Path(root), Path(out_dir)
    state = _load_state(root)
    attach_verdicts(state, load_verdicts(root)["verdicts"])
    flags = pending(state)
    if flags and corpus is None:
        corpus = _corpus(root)
    items = [_item(arxiv_id, record, corpus) for arxiv_id, record in flags]
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "INSTRUCTIONS.md").write_text(JUDGE_INSTRUCTIONS, encoding="utf-8")
    paths = []
    for index in range(n_batches):
        papers = items[index::n_batches]
        if not papers:
            continue
        path = out_dir / f"batch_{index + 1:02d}.json"
        # Unescaped, so the judge sees the same characters the quote check compares against.
        batch = {"batch": index + 1, "verdicts": MEANINGS, "papers": papers}
        path.write_text(json.dumps(batch, indent=1, ensure_ascii=False), encoding="utf-8")
        paths.append(path)
    return paths


_LOWER_LATIN = str.maketrans(string.ascii_uppercase, string.ascii_lowercase)
# A decimal point before its digits (".5") and a ratio's colon ("1:2"), both kept; TeX control
# words (\Omega, \log), TeX control symbols (\{, \,), decimal numbers, other runs of letters and
# digits, then any other single character.
_TOKEN = re.compile(r"(?P<kept>\.(?=\d)|(?<=\d):(?=\d))|\\[A-Za-z]+|\\[^A-Za-z\s]|\d+(?:\.\d+)*|[^\W_]+|\S")
# Sentence punctuation, quote marks, TeX's math delimiters, spacing commands and line breaks, and a
# lone backslash. Everything else (signs, /, !, #, %, ^, _, braces, brackets, primes) is maths and kept.
_DROPPED = frozenset(".,;:?\"'`$\\") | frozenset({
    "\\(", "\\)", "\\[", "\\]", "\\,", "\\;", "\\:", "\\!", "\\>", "\\\\", "\\quad", "\\qquad", "\\enspace",
    "\\enskip", "\\thinspace", "\\medspace", "\\thickspace", "\\negthinspace", "\\negmedspace",
    "\\negthickspace", "\\space", "\\nobreakspace", "\\hfill",
})
# Spacing commands that take a length: \hspace{1em}, \hspace*{2pt}, \kern 1pt, \mkern3mu.
_SPACING_WITH_LENGTH = re.compile(r"\\(?:hspace\*?|hskip|mskip|mspace|kern|mkern)\s*(?:\{[^{}]*\}|-?\d*\.?\d+\s*[a-z]{2})")
# An em dash ("—", TeX's "---") or a spaced en dash (" – ", " -- ") between clauses is punctuation;
# an unspaced "--" is TeX's en dash, one dash like "–" (a range, a name pair).
_CLAUSE_DASH = re.compile(r"---|[\u2014\u2015\u2e3a\u2e3b]|(?<=\s)(?:--|\u2013)(?=\s)")
_QUOTE_MARKS = re.compile(r"[\u2018`]+|['\u2019]+")
_WORD_BEFORE = re.compile(r"(\\?)([^\W\d_]+)$")
# Greek letters whose capital is another symbol; spelled out in ASCII ("Omega", "omega") they keep their case.
_CASED_GREEK = frozenset({"gamma", "delta", "theta", "lambda", "xi", "pi", "sigma", "upsilon", "phi", "psi", "omega"})
_SUPERSCRIPTS = "".join(chr(c) for c in range(0x3000) if unicodedata.decomposition(chr(c)).startswith("<super>"))
_SUBSCRIPTS = "".join(chr(c) for c in range(0x3000) if unicodedata.decomposition(chr(c)).startswith("<sub>"))
_SCRIPT_RUN = re.compile(f"[{re.escape(_SUPERSCRIPTS)}]+|[{re.escape(_SUBSCRIPTS)}]+")
# A quote may not cut a formula: start just after an operator or a prefix (a root, a function, a
# font, a decimal point, #), or end just before an operator, or before a postfix (factorial,
# percent, prime) that follows a number or symbol. A hyphen counts: half a compound is a cut too.
_OPERATORS = frozenset("-+±∓/^_=<>≤≥≠≈∼≪≫·⋅×*÷∘⊗⊕:") | frozenset({
    "\\pm", "\\mp", "\\times", "\\cdot", "\\div", "\\circ", "\\otimes", "\\oplus", "\\le", "\\leq", "\\ge",
    "\\geq", "\\neq", "\\ne", "\\approx", "\\sim", "\\ll", "\\gg", "\\lt", "\\gt", "\\equiv", "\\propto",
})
_PREFIXES = frozenset("√∛.#") | frozenset({
    "\\sqrt", "\\log", "\\ln", "\\exp", "\\frac", "\\tilde", "\\widetilde", "\\hat", "\\widehat", "\\bar",
    "\\overline", "\\mathbb", "\\mathcal", "\\mathrm", "\\mathbf", "\\mathsf", "\\mathfrak", "\\operatorname",
    "\\Pr", "\\det", "\\sin", "\\cos",
})
_POSTFIXES = frozenset("!%′")


def _as_tex(match: re.Match) -> str:
    """A run of superscript or subscript characters as TeX: "ⁿ" -> "^n", "⁻ⁿ" -> "^{-n}", "₁₂" -> "_{12}"."""
    run = match.group(0)
    body = unicodedata.normalize("NFKC", run)
    mark = "^" if run[0] in _SUPERSCRIPTS else "_"
    return f"{mark}{body}" if len(body) == 1 else f"{mark}{{{body}}}"


def _primes(text: str) -> str:
    """Write each ASCII ' or ’ that marks a prime as ′, so "W'" matches "W′" and not "W".

    A run of them is a prime after a digit, a closing bracket, a one-letter symbol or a TeX control
    word (W', f''(x), (x+y)', \\alpha'). It is an apostrophe inside a word (Shor's) or after a longer
    one (the players'), and a quote mark when it opens a quotation (after a space or an opening
    bracket) or closes one opened by ‘, ` or '; those stay and are dropped as punctuation.
    """
    out, last, quoting = [], 0, False
    for match in _QUOTE_MARKS.finditer(text):
        run, start, end = match.group(0), match.start(), match.end()
        before = text[start - 1] if start else " "
        after = text[end] if end < len(text) else " "
        if run[0] in "‘`" or before.isspace() or before in "([{\"“":
            quoting = True
        elif len(run) == 1 and before.isalpha() and after.isalpha():
            pass  # an apostrophe inside a word
        elif quoting:
            quoting = False
        else:
            word = _WORD_BEFORE.search(text[max(0, start - 60) : start])
            if before.isdigit() or before in ")]}′" or (word and (word.group(1) or len(word.group(2)) == 1)):
                out += [text[last:start], "′" * len(run)]
                last = end
    return "".join(out) + text[last:]


def _tokens(text: str) -> list[str]:
    """Words, numbers and symbols for the verbatim check.

    Superscripts and subscripts are first written as TeX exponents and subscripts ("2ⁿ" is
    "2^n"), then the text is NFKC-normalised. Dropped: spacing, sentence punctuation (. , ; : ?),
    quote marks and apostrophes, an em dash or spaced en dash between clauses, TeX's $, \\( \\),
    \\[ \\] and spacing commands (\\, \\quad \\hspace{1em} ...), and markdown's ** bold. Every other
    symbol is its own token: every other dash and the minus sign read as "-", an ASCII prime as
    ′ (see _primes), and a decimal point before its digits (".5") and a ratio's colon ("1:2") are
    kept. Latin letter case is ignored in words of two or more letters and in the word "a", but
    not in other one-letter symbols (O, N, d, I), TeX control words (\\Omega, \\omega) or the
    spelled-out names of Greek letters with their own capital (Omega, omega). Whether a letter
    sits inside TeX maths does not matter, since a quote may drop the $ or start inside a formula.
    So "κ ≤ 0.207" and "κ≤0.207," match, but "κ ≥ 0.207", "0.207" for "-0.207", "n^{1/2}" for
    "n^{-1/2}", "2n" for "2ⁿ", "o(n)" for "O(n)", "W" for "W'" or "\\omega" for "\\Omega" do not.
    """
    text = unicodedata.normalize("NFKC", _SCRIPT_RUN.sub(_as_tex, text))
    text = _SPACING_WITH_LENGTH.sub(" ", re.sub(r"\*{2,}", " ", text))
    text = _primes(_CLAUSE_DASH.sub(" ", text).replace("--", "-"))
    tokens = []
    for match in _TOKEN.finditer(text):
        token = match.group(0)
        if match.lastgroup == "kept":
            tokens.append(token)
            continue
        if token in _DROPPED:
            continue
        if len(token) == 1 and not token.isalnum():
            category = unicodedata.category(token)
            if category in ("Pi", "Pf"):  # curly quote marks
                continue
            if category == "Pd" or token == "−":
                token = "-"
        elif token[0] != "\\":
            lower = token.translate(_LOWER_LATIN)
            if lower in _CASED_GREEK and token[0].isupper():
                token = lower.capitalize()
            elif len(token) > 1 or lower == "a":  # the article; any other one-letter symbol keeps its case
                token = lower
        tokens.append(token)
    return tokens


def _operand(token: str) -> bool:
    """What a postfix binds: a number, a one-letter symbol, a TeX command, a closing bracket or a prime."""
    return token[:1].isdigit() or token[:1] == "\\" or (len(token) == 1 and token.isalpha()) or token in (")", "]", "}", "′")


def _cuts_a_formula(source: list[str], start: int, end: int) -> bool:
    before = source[start - 1] if start else ""
    after = source[end] if end < len(source) else ""
    return (
        before in _OPERATORS
        or before in _PREFIXES
        or after in _OPERATORS
        or (after in _POSTFIXES and _operand(source[end - 1]))
    )


def _verbatim(quote: str, source: str) -> bool:
    """At least six words of `quote` (numbers count, symbols and TeX commands do not) appear, with
    its symbols, as whole tokens in order in `source`, without starting or ending inside a formula."""
    words = _tokens(quote)
    if not source or sum(token[:1].isalnum() for token in words) < MIN_QUOTE_WORDS:
        return False
    text = _tokens(source)
    return any(
        text[start : start + len(words)] == words and not _cuts_a_formula(text, start, start + len(words))
        for start in range(len(text) - len(words) + 1)
    )


def _confidence(value) -> float | None:
    """The judge's confidence clamped to [0, 1]; None unless it is a finite number (not a bool or NaN)."""
    if isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):  # OverflowError: an integer too large for a float
        return None
    return max(0.0, min(1.0, number)) if math.isfinite(number) else None


_BATCH_OUTPUT = re.compile(r"batch_\d+")


def _shown(path: Path) -> dict[str, dict] | None:
    """The papers in the batch an output answers ({arxiv_id: item}), or None when there is none.

    The documented layout puts DIR/batch_NN.json's answers in DIR/out/batch_NN.jsonl.
    """
    batch = path.parent.parent / f"{path.stem}.json"
    if not _BATCH_OUTPUT.fullmatch(path.stem) or not batch.is_file():
        return None
    data = json.loads(batch.read_text(encoding="utf-8"))
    papers = data.get("papers") if isinstance(data, dict) else None
    if not isinstance(papers, list) or not all(isinstance(item, dict) for item in papers):
        raise ValueError(f"{batch}: not a batch file (no list of papers)")
    return {item.get("arxiv_id"): item for item in papers}


def _quoted_text(item: dict, quote_from: str) -> str:
    """The abstract or the excerpt `quote_from` names, as the batch item showed it."""
    if quote_from == "abstract":
        return str(item.get("abstract") or "")
    for near in item.get("nearest") or []:
        if isinstance(near, dict) and near.get("doc_id") == quote_from:
            return str(near.get("excerpt") or "")
    return ""


def import_judgements(
    root: Path, paths: list[Path], judge_name: str, corpus: Corpus | None = None, today: str | None = None
) -> dict:
    """Store the judge's verdicts whose quotes check out.

    Returns {"imported": [arxiv ids], "rejected": [{"arxiv_id", "why"}]}. Every row is checked
    before anything is written: an unknown verdict, or an arxiv_id that is missing or not a stored
    paper, raises ValueError, and so does nothing get written when the corpus cannot be opened to
    check an excerpt quote. A quote is looked for only in the one text `quote_from` names: the
    abstract, or the excerpt of one of the paper's nearest records. Those are the texts the judge
    was shown when its output sits where the README puts it (DIR/out/batch_NN.jsonl beside
    DIR/batch_NN.json, which holds the paper), so a record edited since the export changes
    nothing; otherwise they are the stored abstract and today's excerpt. The accepted rows are then
    merged into fresh copies of the verdicts and collisions files in one write each, so a verdict
    or a run recorded meanwhile is kept, and a person's verdict recorded meanwhile still wins.
    """
    root = Path(root)
    state = _load_state(root)
    paths = [Path(path) for path in paths]
    rows = [(path, row) for path in paths for row in _rows(path)]
    shown = {path: _shown(path) for path in paths}
    for path, row in rows:
        if not isinstance(row, dict):
            raise ValueError(f"{path}: each row must be a JSON object, not {row!r:.80}")
        if row.get("verdict") not in VERDICTS:
            raise ValueError(f"{path}: unknown verdict {row.get('verdict')!r} for {row.get('arxiv_id')!r}")
        if not isinstance(row.get("arxiv_id"), str) or row["arxiv_id"] not in state["papers"]:
            raise ValueError(f"{path}: arxiv_id {row.get('arxiv_id')!r} is missing or not a stored paper")
    existing = load_verdicts(root)["verdicts"]
    rejected: list[dict] = []
    accepted: dict[str, dict] = {}
    for path, row in rows:
        arxiv_id = row["arxiv_id"]
        record = state["papers"][arxiv_id]
        if arxiv_id in existing and not by_judge(existing[arxiv_id]):
            rejected.append({"arxiv_id": arxiv_id, "why": "human verdict exists"})
            continue
        quote, quote_from = str(row.get("quote") or ""), str(row.get("quote_from") or "abstract")
        item = (shown[path] or {}).get(arxiv_id)
        if item is not None:
            source = _quoted_text(item, quote_from)
        elif quote_from == "abstract":
            source = record.get("abstract", "")
        elif quote_from in {near["doc_id"] for near in record.get("nearest", [])}:
            corpus = corpus or _corpus(root)
            source = _excerpt(corpus, quote_from)
        else:
            source = ""
        if not _verbatim(quote, source):
            rejected.append({"arxiv_id": arxiv_id, "why": "quote not found"})
            continue
        action = row.get("action")
        accepted[arxiv_id] = {
            **verdict_entry(row["verdict"], str(row.get("reason") or "")[:600], f"{JUDGE_PREFIX}{judge_name}",
                            action=str(action)[:300] if action else None, today=today),
            "quote": quote[:400], "quote_from": quote_from, "confidence": _confidence(row.get("confidence")),
        }
    imported: list[str] = []
    if accepted:
        data = load_verdicts(root)
        for arxiv_id, entry in accepted.items():
            current = data["verdicts"].get(arxiv_id)
            if current is not None and not by_judge(current):
                rejected.append({"arxiv_id": arxiv_id, "why": "human verdict exists"})
                continue
            data["verdicts"][arxiv_id] = entry
            imported.append(arxiv_id)
    if imported:
        save_verdicts(root, data)
        state = _load_state(root)
        attach_verdicts(state, data["verdicts"])
        _save(root, state)
    return {"imported": imported, "rejected": rejected}


def _at_least_one(text: str) -> int:
    value = int(text)
    if value < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--export", type=Path, metavar="DIR", help="Write INSTRUCTIONS.md and batches for the unreviewed flags.")
    parser.add_argument("--batches", type=_at_least_one, default=3)
    parser.add_argument("--import", dest="imports", nargs="+", type=Path, metavar="FILE", help="Judge outputs (JSONL).")
    parser.add_argument("--judge", help="Name stored as by = judge:NAME on imported verdicts.")
    args = parser.parse_args(argv)
    if bool(args.export) == bool(args.imports):
        parser.error("give either --export DIR or --import FILE ...")
    if args.imports and not args.judge:
        parser.error("--import needs --judge NAME")
    problem = checkout_error(args.root)
    if problem:
        print(f"error: {problem}", file=sys.stderr)
        return 2
    try:
        if args.export:
            paths = export_batches(args.root, args.export, args.batches)
            count = sum(len(json.loads(path.read_text(encoding="utf-8"))["papers"]) for path in paths)
            print(f"exported {count} unreviewed flags in {len(paths)} batches; instructions in {args.export / 'INSTRUCTIONS.md'}")
            return 0
        result = import_judgements(args.root, args.imports, args.judge)
    except (ValueError, OSError, sqlite3.Error) as error:  # a bad row, unreadable JSON, a missing file, a locked index
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(f"imported {len(result['imported'])} verdicts; rejected {len(result['rejected'])}")
    for item in result["rejected"]:
        print(f"  {item['arxiv_id']}: {item['why']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
