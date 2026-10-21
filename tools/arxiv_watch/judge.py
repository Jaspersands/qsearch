"""Judge the arXiv watch's unreviewed flags with in-session subagents.

    python tools/arxiv_watch/judge.py --export DIR [--batches 3]
    python tools/arxiv_watch/judge.py --import DIR/out/*.jsonl --judge NAME

A flag is a stored paper labelled possible-kill or possible-scoop with no verdict in
research/audits/arxiv_verdicts.json. Export writes INSTRUCTIONS.md and batch files; each item
carries the paper's abstract and its nearest Q-Search records, each with the first 600
characters of its text, so the judge can compare the paper with what the project claims.

A fresh subagent reads INSTRUCTIONS.md and one batch and writes one JSONL row per paper. Import
keeps a row only when its quote (at least six words) appears verbatim in the abstract or in the
one excerpt it names, and never replaces a verdict recorded by anyone but a judge. Kept rows are
stored with by = "judge:NAME", copied onto the stored papers and listed in the digest's Reviewed
table.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.arxiv_watch.verdicts import VERDICTS, load_verdicts, save_verdicts, set_verdict  # noqa: E402
from tools.arxiv_watch.watch import FLAGGED, _load_state, _save, attach_verdicts  # noqa: E402
from tools.audit.rediscovery import _norm, _rows  # noqa: E402
from tools.corpus.api import Corpus  # noqa: E402

EXCERPT_CHARS = 600
MIN_QUOTE_WORDS = 6
JUDGE_PREFIX = "judge:"
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
   from a file you opened yourself. Quotes are checked automatically; a paper whose quote is
   not found gets no verdict.
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
        path.write_text(json.dumps({"batch": index + 1, "verdicts": MEANINGS, "papers": papers}, indent=1), encoding="utf-8")
        paths.append(path)
    return paths


def _verbatim(quote: str, source: str) -> bool:
    """At least six words of `quote` appear as whole words, in order, in `source` (case and punctuation ignored)."""
    words = _norm(quote)
    return bool(source) and len(words.split()) >= MIN_QUOTE_WORDS and f" {words} " in f" {_norm(source)} "


def _by_judge(entry) -> bool:
    """A stored verdict a judge may replace: one whose `by` names a judge. An entry without `by`
    (written by hand) counts as a human's."""
    return isinstance(entry, dict) and str(entry.get("by") or "").startswith(JUDGE_PREFIX)


def _confidence(value) -> float | None:
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return None


def import_judgements(
    root: Path, paths: list[Path], judge_name: str, corpus: Corpus | None = None, today: str | None = None
) -> dict:
    """Store the judge's verdicts whose quotes check out.

    Returns {"imported": [arxiv ids], "rejected": [{"arxiv_id", "why"}]}. Every row is checked
    before anything is written: an unknown verdict, or an arxiv_id that is missing or not a stored
    paper, raises ValueError. A quote is looked for only in the one text `quote_from` names: the
    abstract, or the excerpt of one of the paper's nearest records.
    """
    root = Path(root)
    state = _load_state(root)
    rows = [(path, row) for path in paths for row in _rows(Path(path))]
    for path, row in rows:
        if row.get("verdict") not in VERDICTS:
            raise ValueError(f"{path}: unknown verdict {row.get('verdict')!r} for {row.get('arxiv_id')!r}")
        if row.get("arxiv_id") not in state["papers"]:
            raise ValueError(f"{path}: arxiv_id {row.get('arxiv_id')!r} is missing or not a stored paper")
    existing = load_verdicts(root)["verdicts"]
    imported: list[str] = []
    rejected: list[dict] = []
    evidence: dict[str, dict] = {}
    for _, row in rows:
        arxiv_id = row["arxiv_id"]
        record = state["papers"][arxiv_id]
        if arxiv_id in existing and not _by_judge(existing[arxiv_id]):
            rejected.append({"arxiv_id": arxiv_id, "why": "human verdict exists"})
            continue
        quote, quote_from = str(row.get("quote") or ""), str(row.get("quote_from") or "abstract")
        if quote_from == "abstract":
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
        set_verdict(
            root, arxiv_id, row["verdict"], str(row.get("reason") or "")[:600], f"{JUDGE_PREFIX}{judge_name}",
            action=str(action)[:300] if action else None, today=today,
        )
        evidence[arxiv_id] = {"quote": quote[:400], "quote_from": quote_from, "confidence": _confidence(row.get("confidence"))}
        if arxiv_id not in imported:
            imported.append(arxiv_id)
    if imported:
        data = load_verdicts(root)
        for arxiv_id, extra in evidence.items():
            data["verdicts"][arxiv_id].update(extra)
        save_verdicts(root, data)
        attach_verdicts(state, data["verdicts"])
        _save(root, state)
    return {"imported": imported, "rejected": rejected}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--export", type=Path, metavar="DIR", help="Write INSTRUCTIONS.md and batches for the unreviewed flags.")
    parser.add_argument("--batches", type=int, default=3)
    parser.add_argument("--import", dest="imports", nargs="+", type=Path, metavar="FILE", help="Judge outputs (JSONL).")
    parser.add_argument("--judge", help="Name stored as by = judge:NAME on imported verdicts.")
    args = parser.parse_args(argv)
    if bool(args.export) == bool(args.imports):
        parser.error("give either --export DIR or --import FILE ...")
    if args.export:
        paths = export_batches(args.root, args.export, args.batches)
        count = sum(len(json.loads(path.read_text(encoding="utf-8"))["papers"]) for path in paths)
        print(f"exported {count} unreviewed flags in {len(paths)} batches; instructions in {args.export / 'INSTRUCTIONS.md'}")
        return 0
    if not args.judge:
        parser.error("--import needs --judge NAME")
    try:
        result = import_judgements(args.root, args.imports, args.judge)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(f"imported {len(result['imported'])} verdicts; rejected {len(result['rejected'])}")
    for item in result["rejected"]:
        print(f"  {item['arxiv_id']}: {item['why']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
