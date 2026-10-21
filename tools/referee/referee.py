"""Referee review-pending research notes with an independent judge.

    python tools/referee/referee.py select [--prefix PRIME] [--limit 30] [--json]
    python tools/referee/referee.py export --out-dir DIR [--limit 30] [--note STEM ...]
    python tools/referee/referee.py import DIR/out/*.jsonl --judge NAME
    python tools/referee/referee.py render
    python tools/referee/referee.py status [--json]

A judge (an in-session subagent) reads INSTRUCTIONS.md and one batch of note packets, and
writes one JSONL row per note: up to six claims, each quoted verbatim from the note, with a
verdict, the step at fault and what is missing. Import checks every quote against the note
text and records the note's content hash, so a review goes stale when the note changes.

Outputs: research/audits/reviews/reviews.json, reviews/<STEM>.md and REFEREE_QUEUE.md.
The referee never edits research/*.md.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.audit.rediscovery import _norm, _rows  # noqa: E402
from tools.corpus.docs import read_json  # noqa: E402
from tools.corpus.sources.markdown import JOURNALS, note_status  # noqa: E402
from tools.referee.extract import DATE, _status_block, artifact_excerpt, parse_note, to_dict  # noqa: E402

REVIEWS = "research/audits/reviews/reviews.json"


def load_reviews(root: Path) -> dict:
    path = root / REVIEWS
    return read_json(path) if path.exists() else {"notes": {}}


def note_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _note_date(lines: list[str]) -> str | None:
    match = DATE.search(" ".join(_status_block(lines)))
    return match.group(0) if match else None


def select_notes(
    root: Path,
    prefixes: tuple[str, ...] = (),
    limit: int | None = 30,
    exclude_reviewed: bool = True,
    reviews: dict | None = None,
    statuses: tuple[str, ...] = ("review-pending",),
) -> list[Path]:
    """Notes with one of `statuses`, newest status-block date first, then newest mtime."""
    notes = (reviews if reviews is not None else load_reviews(root)).get("notes", {})
    ranked = []
    for path in sorted((root / "research").glob("*.md")):
        if path.name in JOURNALS or (prefixes and not path.stem.startswith(tuple(prefixes))):
            continue
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        if note_status(lines) not in statuses:
            continue
        review = notes.get(path.stem)
        if exclude_reviewed and review and review.get("content_sha") == note_sha(path):
            continue
        ranked.append(((_note_date(lines) or "0000", path.stat().st_mtime), path))
    ranked.sort(key=lambda item: item[0], reverse=True)
    paths = [path for _, path in ranked]
    return paths[:limit] if limit else paths


CLAIM_VERDICTS = ("holds", "gap", "wrong", "unclear")
OVERALL = ("sound", "needs-work", "unsound", "unclear")

OUTPUT_FORMAT = (
    '{"stem": "NOTE_STEM", "content_sha": "copied from the packet", "overall": "needs-work", '
    '"summary": "...", "claims": [{"quote": "at least six words copied verbatim from the note text", '
    '"verdict": "gap", "step": "...", "finding": "...", "covered_by_self_check": false}]}'
)

REFEREE_INSTRUCTIONS = f"""\
# Referee instructions

You are an adversarial referee for research notes from a quantum-algorithm search project.
Each note proposes or tests a mechanism, a bound or a classical competitor, and is marked
review pending: nobody independent has checked it. Your job is to find what is wrong or
missing in what is written, not to summarise or extend the research.

Each note packet in your batch has: `stem`, `title`, `date`, `status`, `not_claimed` (what
the note says it does not claim), `producer` (the command and JSON artifact behind its
numbers), `result`, `derivations`, `controls`, `self_check` (the note's own attempt to
break itself), `decision`, `flags` (fine-print flags a rule-based checker raised on the
result), `artifact_excerpt` (numbers from the producer's JSON output, or null),
`content_sha` and the full note `text`.

For each note:

1. Pick up to 6 claims that carry the note's conclusion: the stated result, each bound or
   lemma the result depends on, and each comparison with a classical baseline.
2. Quote each claim verbatim from the note `text`: at least 6 consecutive words copied
   exactly (only whitespace and punctuation may differ). Quote from the note text only,
   never from the artifact excerpt, the flags or these instructions. Every quote is checked
   automatically, and one quote that is not in the note rejects your whole output file.
3. Give each claim a verdict:
   - `holds`: the note's own derivation or evidence supports it as stated.
   - `gap`: it may be true, but a step is missing or a condition is unstated.
   - `wrong`: it is false as stated.
   - `unclear`: the note does not say enough to check it.
   Name the `step` at fault (a section heading, equation or sentence). For `gap` and
   `wrong`, the `finding` gives the counterexample or the missing condition concretely.
   Set `covered_by_self_check` to true when the note's self-check or not-claimed list
   already concedes the problem.
4. Check the numbers you can against `artifact_excerpt`, and say in `finding` when a number
   in the note does not match it. The excerpt is evidence for a finding, never a quote.
5. Give the note an `overall` verdict and a `summary` of at most five sentences:
   - `sound`: every load-bearing claim holds.
   - `needs-work`: at least one gap, nothing shown wrong.
   - `unsound`: a load-bearing claim is wrong.
   - `unclear`: too little is written to judge.

You must not propose new research, new algorithms or next steps: judge only what is
written. Work from the packet and do not edit any file in the repository.

Write one JSON object per line (JSONL), one line per note, to your output path. Copy
`stem` and `content_sha` from the packet. Do not skip notes.

{OUTPUT_FORMAT}
"""


def build_packet(root: Path, path: Path) -> dict:
    packet = parse_note(path)
    text = path.read_bytes().decode("utf-8", errors="replace")
    return {**to_dict(packet), "artifact_excerpt": artifact_excerpt(root, packet), "text": text}


def export_batches(root: Path, out_dir: Path, notes: list[Path], batch_size: int = 5) -> list[Path]:
    """INSTRUCTIONS.md plus batch_NN.json files of `batch_size` packets, in the given order."""
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "INSTRUCTIONS.md").write_text(REFEREE_INSTRUCTIONS, encoding="utf-8")
    paths = []
    for start in range(0, len(notes), batch_size):
        number = start // batch_size + 1
        batch = {
            "batch": number,
            "claim_verdicts": list(CLAIM_VERDICTS),
            "overall_verdicts": list(OVERALL),
            "output_format": OUTPUT_FORMAT,
            "notes": [build_packet(root, path) for path in notes[start:start + batch_size]],
        }
        path = out_dir / f"batch_{number:02d}.json"
        path.write_text(json.dumps(batch, indent=1), encoding="utf-8")
        paths.append(path)
    return paths


MIN_QUOTE_WORDS = 6
MAX_CLAIMS = 6


def _note_path(root: Path, stem: str) -> Path:
    return root / "research" / f"{stem}.md"


def _claim_entry(where: str, claim: dict, source: str) -> dict:
    verdict = claim.get("verdict")
    if verdict not in CLAIM_VERDICTS:
        raise ValueError(f"{where}: bad claim verdict {verdict!r}")
    quote = str(claim.get("quote", ""))
    words = _norm(quote)
    if len(words.split()) < MIN_QUOTE_WORDS:
        raise ValueError(f"{where}: quote under {MIN_QUOTE_WORDS} words: {quote!r}")
    if f" {words} " not in source:
        raise ValueError(f"{where}: quote not verbatim in the note: {quote[:120]!r}")
    return {
        "quote": quote[:400],
        "verdict": verdict,
        "step": str(claim.get("step", ""))[:300],
        "finding": str(claim.get("finding", ""))[:600],
        "covered_by_self_check": bool(claim.get("covered_by_self_check")),
    }


def import_reviews(root: Path, paths: list[Path], judge: str, today: str | None = None) -> dict:
    """Verify judge rows against the notes and store them; nothing is written if any row fails."""
    reviewed_on = today or dt.date.today().isoformat()
    entries: dict[str, dict] = {}
    for path in paths:
        for row in _rows(Path(path)):
            stem = str(row.get("stem") or "")
            note = _note_path(root, stem)
            if not stem or not note.is_file():
                raise ValueError(f"{path}: unknown note {stem!r}")
            overall = row.get("overall")
            if overall not in OVERALL:
                raise ValueError(f"{path}: {stem}: bad overall verdict {overall!r}")
            source = f" {_norm(note.read_bytes().decode('utf-8', errors='replace'))} "
            claims = [_claim_entry(f"{path}: {stem}", claim, source) for claim in (row.get("claims") or [])[:MAX_CLAIMS]]
            sha = str(row.get("content_sha") or "")
            entries[stem] = {
                "reviewed_on": reviewed_on,
                "judge": judge,
                "content_sha": sha,
                "overall": overall,
                "claims": claims,
                "summary": str(row.get("summary", ""))[:1500],
                "stale": sha != note_sha(note),
            }
    data = load_reviews(root)
    data.setdefault("notes", {}).update(entries)
    store = root / REVIEWS
    store.parent.mkdir(parents=True, exist_ok=True)
    store.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return {"imported": sorted(entries), "stale": sorted(stem for stem, entry in entries.items() if entry["stale"])}


WORST = {"wrong": 3, "gap": 2, "unclear": 1, "holds": 0}
FLAGGED = ("unsound", "needs-work")
QUEUE = "research/audits/REFEREE_QUEUE.md"
NEXT = 30


def worst_claim(entry: dict) -> dict | None:
    claims = entry.get("claims") or []
    return max(claims, key=lambda claim: WORST.get(claim.get("verdict"), 0)) if claims else None


def is_stale(root: Path, stem: str, entry: dict) -> bool:
    """True when the note is gone or its bytes differ from the version the judge read."""
    path = _note_path(root, stem)
    return not path.is_file() or note_sha(path) != entry.get("content_sha")


def status(root: Path) -> dict:
    if not (root / REVIEWS).exists():
        return {"available": False, "reason": f"no reviews yet ({REVIEWS} absent)", "reviewed": 0, "flagged": [], "stale": []}
    notes = load_reviews(root).get("notes", {})
    stale = sorted(stem for stem, entry in notes.items() if is_stale(root, stem, entry))
    flagged = [
        {"stem": stem, "overall": entry["overall"], "reviewed_on": entry.get("reviewed_on"), "worst_claim": worst_claim(entry)}
        for stem, entry in notes.items()
        if entry.get("overall") in FLAGGED and stem not in stale
    ]
    flagged.sort(key=lambda item: (FLAGGED.index(item["overall"]), item["stem"]))
    return {"available": True, "reviewed": len(notes), "flagged": flagged, "stale": stale}


def _cell(text: str, limit: int = 160) -> str:
    flat = " ".join(str(text).split()).replace("|", "/")
    return flat if len(flat) <= limit else flat[: limit - 3] + "..."


def _render_review(stem: str, entry: dict, stale: bool) -> str:
    lines = [
        f"# Referee review: {stem}",
        "",
        f"Note: `research/{stem}.md`. Reviewed {entry.get('reviewed_on')} by {entry.get('judge')}. "
        f"Overall: **{entry.get('overall')}**.",
        "",
        "An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.",
        "",
    ]
    if stale:
        lines += ["**Stale:** the note changed after this review, so the review may no longer apply.", ""]
    if entry.get("summary"):
        lines += [entry["summary"], ""]
    lines += ["## Claims", ""]
    if not entry.get("claims"):
        lines += ["No claims recorded.", ""]
    for number, claim in enumerate(entry.get("claims") or [], start=1):
        lines += [
            f"### {number}. {claim['verdict']}",
            "",
            f"> {' '.join(claim['quote'].split())}",
            "",
            f"- Step: {claim.get('step') or '-'}",
            f"- Finding: {claim.get('finding') or '-'}",
            f"- Conceded by the note's own self-check: {'yes' if claim.get('covered_by_self_check') else 'no'}",
            "",
        ]
    return "\n".join(lines).rstrip() + "\n"


def _render_queue(root: Path, notes: dict, stale: list[str], today: str) -> str:
    current = [entry for stem, entry in notes.items() if stem not in stale]
    lines = [
        "# Referee queue",
        "",
        f"Generated on {today} from `{REVIEWS}` by `python tools/referee/referee.py render`.",
        "Reviews come from in-session model judges that quote each claim from the note; they are a",
        "triage, not peer review. The referee never edits `research/*.md`.",
        "",
        "| Overall | Notes |",
        "|---|---|",
    ]
    for overall in ("unsound", "needs-work", "unclear", "sound"):
        lines.append(f"| {overall} | {sum(entry.get('overall') == overall for entry in current)} |")
    lines += [f"| stale | {len(stale)} |", "", "## Flagged", "",
              "Unsound and needs-work reviews of notes that have not changed since.", ""]
    flagged = status(root)["flagged"]
    if flagged:
        lines += ["| Note | Overall | Reviewed | Worst claim |", "|---|---|---|---|"]
        for item in flagged:
            worst = item["worst_claim"]
            text = f"{worst['verdict']}: \"{_cell(worst['quote'], 120)}\" {_cell(worst.get('finding', ''), 200)}" if worst else "-"
            lines.append(f"| [{item['stem']}](reviews/{item['stem']}.md) | {item['overall']} | {item['reviewed_on']} | {text} |")
    else:
        lines.append("None.")
    lines += ["", "## Stale", "", "Notes edited after their review; re-run the referee on them.", ""]
    lines += [f"- {stem} (reviewed {notes[stem].get('reviewed_on')}, {notes[stem].get('overall')})" for stem in stale] or ["None."]
    upcoming = select_notes(root, limit=NEXT)
    lines += ["", f"## Next {NEXT}", "", "Review-pending notes without a current review, newest first.", ""]
    if upcoming:
        lines += ["| Note | Date |", "|---|---|"]
        for path in upcoming:
            date = _note_date(path.read_text(encoding="utf-8", errors="replace").splitlines())
            lines.append(f"| {path.stem} | {date or 'undated'} |")
    else:
        lines.append("None.")
    return "\n".join(lines).rstrip() + "\n"


def render(root: Path, today: str | None = None) -> None:
    """Write reviews/<STEM>.md for every stored review and REFEREE_QUEUE.md."""
    notes = load_reviews(root).get("notes", {})
    stale = sorted(stem for stem, entry in notes.items() if is_stale(root, stem, entry))
    out = (root / REVIEWS).parent
    out.mkdir(parents=True, exist_ok=True)
    for stem, entry in sorted(notes.items()):
        (out / f"{stem}.md").write_text(_render_review(stem, entry, stem in stale), encoding="utf-8")
    queue = root / QUEUE
    queue.write_text(_render_queue(root, notes, stale, today or dt.date.today().isoformat()), encoding="utf-8")


def _selected(root: Path, args: argparse.Namespace) -> list[Path]:
    return select_notes(root, prefixes=tuple(args.prefix), limit=args.limit, exclude_reviewed=not args.include_reviewed)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    choose = argparse.ArgumentParser(add_help=False)
    choose.add_argument("--prefix", action="append", default=[], help="Only notes whose stem starts with this (repeatable).")
    choose.add_argument("--limit", type=int, default=NEXT, help="At most this many notes; 0 for all.")
    choose.add_argument("--include-reviewed", action="store_true", help="Keep notes whose review is still current.")
    sub = parser.add_subparsers(dest="command", required=True)
    select = sub.add_parser("select", parents=[common, choose], help="List the newest review-pending notes.")
    select.add_argument("--json", action="store_true")
    export = sub.add_parser("export", parents=[common, choose], help="Write INSTRUCTIONS.md and judge batches.")
    export.add_argument("--out-dir", type=Path, required=True)
    export.add_argument("--batch-size", type=int, default=5)
    export.add_argument("--note", action="append", default=[], metavar="STEM",
                        help="Export this note whatever its status (repeatable); replaces the selection.")
    imp = sub.add_parser("import", parents=[common], help="Verify and store judge reviews (JSONL).")
    imp.add_argument("files", nargs="+", type=Path)
    imp.add_argument("--judge", required=True, help="Judge name stored with each review.")
    sub.add_parser("render", parents=[common], help="Write reviews/<STEM>.md and REFEREE_QUEUE.md.")
    stat = sub.add_parser("status", parents=[common], help="Flagged and stale reviews.")
    stat.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = args.root

    if args.command == "select":
        rows = []
        for path in _selected(root, args):
            date = _note_date(path.read_text(encoding="utf-8", errors="replace").splitlines())
            rows.append({"stem": path.stem, "path": f"research/{path.name}", "date": date})
        if args.json:
            print(json.dumps(rows, indent=1))
        else:
            for row in rows:
                print(f"{row['date'] or 'undated':<10}  {row['stem']}")
            print(f"{len(rows)} notes")
        return 0

    if args.command == "export":
        if args.note:
            notes = [_note_path(root, stem.removesuffix(".md")) for stem in args.note]
            missing = [path.stem for path in notes if not path.is_file()]
            if missing:
                parser.error(f"no such note: {', '.join(missing)}")
        else:
            notes = _selected(root, args)
        paths = export_batches(root, args.out_dir, notes, batch_size=args.batch_size)
        print(f"{len(notes)} notes in {len(paths)} batches; instructions in {args.out_dir / 'INSTRUCTIONS.md'}")
        return 0

    if args.command == "import":
        try:
            result = import_reviews(root, args.files, args.judge)
        except ValueError as error:
            print(f"error: {error}; nothing imported", file=sys.stderr)
            return 2
        stale = f": {', '.join(result['stale'])}" if result["stale"] else ""
        print(f"imported {len(result['imported'])} reviews; {len(result['stale'])} stale{stale}")
        return 0

    if args.command == "render":
        render(root)
        print(f"wrote {len(load_reviews(root).get('notes', {}))} reviews and {QUEUE}")
        return 0

    result = status(root)
    if args.json:
        print(json.dumps(result, indent=1))
        return 0
    if not result["available"]:
        print(result["reason"])
        return 0
    print(f"{result['reviewed']} reviewed, {len(result['flagged'])} flagged, {len(result['stale'])} stale")
    for item in result["flagged"]:
        worst = item["worst_claim"]
        detail = f"  {worst['verdict']}: {_cell(worst['quote'], 100)}" if worst else ""
        print(f"  {item['overall']:<10} {item['stem']}{detail}")
    for stem in result["stale"]:
        print(f"  stale      {stem}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
