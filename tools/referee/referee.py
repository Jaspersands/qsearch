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
import os
import re
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.audit.rediscovery import _rows  # noqa: E402
from tools.corpus.docs import read_json  # noqa: E402
from tools.corpus.sources.markdown import JOURNALS, note_status  # noqa: E402
from tools.referee.extract import DATE, _resolve_artifact, _status_block, artifact_excerpt, parse_note, to_dict  # noqa: E402

REVIEWS = "research/audits/reviews/reviews.json"


class StoreError(ValueError):
    """reviews.json cannot be read or does not have the shape import writes."""


def _entry_problem(entry) -> str | None:
    if not isinstance(entry, dict):
        return "is not a JSON object"
    claims = entry.get("claims") or []
    if not isinstance(claims, list) or not all(
            isinstance(claim, dict) and isinstance(claim.get("quote"), str) and isinstance(claim.get("verdict"), str)
            for claim in claims):
        return "has claims that are not objects with a string quote and verdict"
    if not isinstance(entry.get("summary", ""), str):
        return "has a summary that is not a string"
    return None


def load_reviews(root: Path) -> dict:
    """The stored reviews, `{"notes": {}}` before the first import. A store that cannot be read
    or does not have import's shape (`{"notes": {STEM: entry}}`, each entry an object whose
    claims are objects with a string quote and verdict) raises StoreError naming the file."""
    path = root / REVIEWS
    if not path.exists():
        return {"notes": {}}
    try:
        data = read_json(path)
    except (OSError, ValueError) as error:  # ValueError covers JSONDecodeError and UnicodeDecodeError
        raise StoreError(f"{path}: cannot read the review store: {error}") from error
    if not isinstance(data, dict) or not isinstance(data.get("notes"), dict):
        raise StoreError(f'{path}: the review store is not a JSON object with a "notes" object')
    for stem, entry in data["notes"].items():
        problem = _entry_problem(entry)
        if problem:
            raise StoreError(f"{path}: the stored review of {stem!r} {problem}")
    return data


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
    """Notes with one of `statuses`, newest status-block date first (undated last), then by stem.

    Not by mtime: mtimes follow checkout and copy order, so the same commit would give a
    different queue (and a different cut at `limit`) on another machine."""
    notes = (reviews if reviews is not None else load_reviews(root)).get("notes", {})
    ranked = []
    for path in sorted((root / "research").glob("*.md"), key=lambda path: path.stem):  # kept by the stable sort below
        if path.name in JOURNALS or (prefixes and not path.stem.startswith(tuple(prefixes))):
            continue
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        if note_status(lines) not in statuses:
            continue
        review = notes.get(path.stem)
        if exclude_reviewed and review and review.get("content_sha") == note_sha(path):
            continue
        ranked.append((_note_date(lines) or "0000", path))
    ranked.sort(key=lambda item: item[0], reverse=True)
    paths = [path for _, path in ranked]
    return paths[:limit] if limit else paths


CLAIM_VERDICTS = ("holds", "gap", "wrong", "unclear")
OVERALL = ("sound", "needs-work", "unsound", "unclear")
WORST = {"wrong": 3, "gap": 2, "unclear": 1, "holds": 0}
OVERALL_FOR = {"wrong": "unsound", "gap": "needs-work", "unclear": "unclear", "holds": "sound"}  # by worst claim

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
`artifact_path` (where that JSON file is, relative to the repository root, or null; the
note may write it without the `research/` prefix), `content_sha` and the full note `text`.
The parsed fields are pointers taken from headings and may be empty or misplaced; work
from the full text.

For each note:

1. Pick up to 6 claims that carry the note's conclusion: the stated result, each bound or
   lemma the result depends on, each comparison with a classical baseline, and any finding
   from step 5.
2. Quote each claim verbatim from the note `text`: at least 6 consecutive words copied
   exactly. Whitespace, letter case, punctuation and markdown markup may differ, but the
   letters in any script (Greek variables, superscript exponents) and the symbols <, >, =,
   +, -, /, ^, ±, √ and decimal points must be the note's, hyphens included, also before
   your first word and after your last (they are the mathematics; ≤ for <= is fine, and a
   prose em dash — may be written - or left out). Quote from the note text only, never
   from the artifact excerpt, the flags or these instructions. Every quote is checked
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
5. Two checks that are easy to skip; each finding is a claim like any other:
   - Scope of headline sentences: read the title, the status block, the result and the
     decision as a reader who reads nothing else. Each must keep the conditions the note
     states elsewhere: the review-pending derivations it rests on, the sizes or instances
     actually certified (one certified length is not a family), and the inputs on which
     the method fails. A headline that drops one of these is a `gap`, quoted from the
     headline, even when the derivation behind it holds.
   - Omissions in summaries: when a sentence summarises cases ("every saved input",
     "both", "all", a list of what is left open), compare it with every case the note
     reports elsewhere and with the artifact excerpt. A reported case missing from the
     summary, or a stated condition that cannot hold for a reported case, is a `gap`.
6. Give the note an `overall` verdict and a `summary` of at most five sentences:
   - `sound`: every load-bearing claim holds.
   - `needs-work`: at least one gap, nothing shown wrong.
   - `unsound`: a load-bearing claim is wrong.
   - `unclear`: too little is written to judge.
   The overall must agree with your worst claim: a `wrong` claim makes it `unsound`, else a
   `gap` makes it `needs-work`, else an `unclear` claim makes it `unclear`, and claims that
   all hold make it `sound` (with no claims, `sound` or `unclear`). A row that contradicts
   this, or that has more than 6 claims, rejects your whole output file.

You must not propose new research, new algorithms or next steps: judge only what is
written. Work from the packet and do not edit any file in the repository.

Write one JSON object per line (JSONL), one line per note, to your output path. Copy
`stem` and `content_sha` from the packet. Do not skip notes.

{OUTPUT_FORMAT}
"""


def build_packet(root: Path, path: Path) -> dict:
    raw = path.read_bytes()  # one read, so content_sha is the hash of `text`
    packet = parse_note(path, raw)
    text = raw.decode("utf-8", errors="replace")
    rel = (packet.producer or {}).get("artifact")
    found = _resolve_artifact(root, rel) if rel else None
    return {
        **to_dict(packet),
        "artifact_excerpt": artifact_excerpt(root, packet),
        "artifact_path": found.relative_to(root).as_posix() if found else None,
        "text": text,
    }


def export_batches(root: Path, out_dir: Path, notes: list[Path], batch_size: int = 5) -> list[Path]:
    """INSTRUCTIONS.md plus batch_NN.json files of `batch_size` packets, in the given order.

    Raises ValueError, before writing anything, when `out_dir` is a file or cannot be made, or
    already holds batch files: an earlier, larger export's leftovers would be judged again."""
    if out_dir.exists() and not out_dir.is_dir():
        raise ValueError(f"{out_dir} is not a folder")
    earlier = sorted(path.name for path in out_dir.glob("batch_*.json")) if out_dir.is_dir() else []
    if earlier:
        raise ValueError(f"{out_dir} already holds {', '.join(earlier)} from an earlier export; use a new folder per pass")
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        raise ValueError(f"cannot make {out_dir}: {error.strerror or error}") from error
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

# Words are runs of letters and digits in any script (Greek variables and superscript
# exponents included; an underscore splits words). Between two words and before the first and
# after the last word of a quote, the symbols must match the note: in ASCII-math notes
# "b<=epsilon" and "b>=epsilon" have the same words.
WORD = re.compile(r"[^\W_]+")
EM_DASH = "—"
DASHES = "-−–"  # hyphen, minus sign and en dash all read as a minus; a touching run of them is one
SYMBOL = re.compile(rf"!=|<=|>=|->|=>|[{DASHES}]+|{EM_DASH}|[≤≦≥≧≠→⇒≈∼±∓√<>=+/^~]")
SYMBOL_FORMS = {"≤": "<=", "≦": "<=", "≥": ">=", "≧": ">=", "≠": "!=", "→": "->", "⇒": "=>", "≈": "~", "∼": "~"}
LINE_MARKER = re.compile(r"(?m)^[ \t]*(?:[-+*>][ \t]+)+")
SPACE = re.compile(r"\s")


STEM = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.-]*$")  # a file name in research/, never a path
SHA = re.compile(r"[0-9a-f]{64}")


def _note_path(root: Path, stem: str) -> Path:
    return root / "research" / f"{stem}.md"


def _is_note(path: Path) -> bool:
    """`path` is a file under exactly its own name: on a case-insensitive file system (macOS)
    `research/bar_note.md` also opens `research/BAR_NOTE.md`."""
    return path.is_file() and path.name in os.listdir(path.parent)


def _symbol_run(segment: str, em_dash: str) -> list[tuple[int, int, str]]:
    """(start, end, symbol) for each symbol in `segment`: typographic forms read as ASCII, a
    touching run of minus signs as one (in `x - (-y)` the two are two), and an em dash as
    `em_dash` ("-", or "" to leave it out)."""
    run: list[tuple[int, int, str]] = []
    for match in SYMBOL.finditer(segment):
        token = match.group()
        token = em_dash if token == EM_DASH else "-" if token[0] in DASHES else SYMBOL_FORMS.get(token, token)
        if token == "-" and run and run[-1][2] == "-" and run[-1][1] == match.start():  # touching: "-—" is one
            run[-1] = (run[-1][0], match.end(), "-")
        elif token:
            run.append((match.start(), match.end(), token))
    return run


def _symbols(segment: str, em_dash: str) -> tuple[str, ...]:
    return tuple(token for _, _, token in _symbol_run(segment, em_dash))


def _gaps(text: str, words: list[re.Match], em_dash: str) -> tuple[str, ...]:
    """The symbols in each gap between consecutive words; a decimal point counts as one."""
    gaps = []
    for left, right in zip(words, words[1:]):
        gap = text[left.end():right.start()]
        if gap == "." and left.group()[-1].isdigit() and right.group()[0].isdigit():
            gaps.append(".")
        else:
            gaps.append("".join(_symbols(gap, em_dash)))
    return tuple(gaps)


def _spread(text: str, start: int, end: int) -> str:
    """text[start:end] widened to whole whitespace-delimited tokens, less trailing .,;: marks."""
    while start > 0 and not text[start - 1].isspace():
        start -= 1
    while end < len(text) and not text[end].isspace():
        end += 1
    return text[start:end].rstrip(".,;:")


def find_quote(quote: str, text: str) -> tuple[str | None, str]:
    """The note's own span for `quote`, or None and why not.

    The words must appear consecutively in `text` (case, whitespace and punctuation aside), and
    the symbols (<, >, =, +, -, /, ^, ~, ±, √, decimal points) between them, before the first
    and after the last must be the note's. A quote may keep or drop the list and quote markers
    at the note's line starts, and may write a prose em dash as - or leave it out. The span is
    widened to whole whitespace-delimited tokens, so the note's signs and operators next to the
    quote's first and last words are kept.
    """
    quoted = list(WORD.finditer(quote))
    words = [word.group().lower() for word in quoted]
    if len(words) < MIN_QUOTE_WORDS:
        return None, f"quote under {MIN_QUOTE_WORDS} words"
    wanted = [(_gaps(quote, quoted, em), _symbols(quote[:quoted[0].start()], em), _symbols(quote[quoted[-1].end():], em))
              for em in ("-", "")]
    tokens = list(WORD.finditer(text))
    unmarked = LINE_MARKER.sub(lambda match: " " * len(match.group()), text)  # same positions
    joined, starts = " ", {}
    for index, token in enumerate(tokens):
        starts[len(joined)] = index
        joined += token.group().lower() + " "
    needle = " " + " ".join(words) + " "
    found, at = False, joined.find(needle)
    while at >= 0:
        found = True
        first = starts[at + 1]
        last = first + len(words) - 1
        before = tokens[first - 1].end() if first else 0
        after = tokens[last + 1].start() if last + 1 < len(tokens) else len(text)
        for version in (text, unmarked):
            for em in ("-", ""):
                lead = _symbol_run(version[before:tokens[first].start()], em)
                trail = _symbol_run(version[tokens[last].end():after], em)
                gaps = _gaps(version, tokens[first:last + 1], em)
                for want_gaps, want_lead, want_trail in wanted:
                    if (want_gaps != gaps or len(want_lead) > len(lead) or len(want_trail) > len(trail)
                            or want_lead != tuple(t for _, _, t in lead[len(lead) - len(want_lead):])
                            or want_trail != tuple(t for _, _, t in trail[:len(want_trail)])):
                        continue
                    start = before + lead[-len(want_lead)][0] if want_lead else tokens[first].start()
                    end = tokens[last].end() + trail[len(want_trail) - 1][1] if want_trail else tokens[last].end()
                    return _spread(text, start, end), ""
        at = joined.find(needle, at + 1)
    if found:
        return None, ("quote's symbols (<, >, =, +, -, /, ^, ~, ±, √, decimal points) differ from the note, "
                      "between its words or before or after them")
    return None, "quote not verbatim in the note"


def _claim_entry(where: str, claim: dict, source: str, strict: bool = True) -> dict:
    """A stored claim. When not `strict` (the judge read a version that is gone), a quote that
    is not in `source` is kept as the judge wrote it and marked unverified."""
    verdict = claim.get("verdict")
    if verdict not in CLAIM_VERDICTS:
        raise ValueError(f"{where}: bad claim verdict {verdict!r}")
    conceded = claim.get("covered_by_self_check")
    if conceded is not None and not isinstance(conceded, bool):
        raise ValueError(f"{where}: covered_by_self_check must be true or false, not {conceded!r}")
    quote = str(claim.get("quote", ""))
    span, reason = find_quote(quote, source)
    if span is None and (strict or reason.startswith("quote under")):
        raise ValueError(f"{where}: {reason}: {quote[:120]!r}")
    return {
        "quote": (span or quote)[:400],
        "verified": span is not None,
        "verdict": verdict,
        "step": str(claim.get("step", ""))[:300],
        "finding": str(claim.get("finding", ""))[:600],
        "covered_by_self_check": bool(conceded),
    }


def overall_conflict(overall: str, claims: list[dict]) -> str | None:
    """Why `overall` contradicts the claim verdicts, or None. The worst claim sets it: a wrong
    claim makes the note unsound, else a gap needs-work, else an unclear claim unclear, and
    claims that all hold sound. A row with no claims may be sound or unclear."""
    if not claims:
        needs = {"unsound": "a wrong claim", "needs-work": "a gap"}
        return f"{overall} needs {needs[overall]}" if overall in needs else None
    worst = max((claim["verdict"] for claim in claims), key=WORST.__getitem__)
    if overall != OVERALL_FOR[worst]:
        return f"the worst claim is {worst}, so overall must be {OVERALL_FOR[worst]}"
    return None


def exported_texts(paths: list[Path]) -> tuple[dict[tuple[str, str], str], dict[str, set[str]]]:
    """Note texts the judges read, by (stem, content_sha), from the `batch_NN.json` files in
    each judge file's folder or its parent (`DIR/out/*.jsonl` sits under `DIR/batch_NN.json`),
    and the `content_sha` each exported packet declares, by stem. A text whose hash is not its
    `content_sha` is left out of the texts."""
    texts: dict[tuple[str, str], str] = {}
    declared: dict[str, set[str]] = {}
    folders = {Path(path).resolve().parent for path in paths}
    batches = {batch for folder in folders for near in (folder, folder.parent) for batch in near.glob("batch_*.json")}
    for batch in sorted(batches):
        try:
            packets = json.loads(batch.read_text(encoding="utf-8")).get("notes") or []
        except (OSError, ValueError, AttributeError):
            continue
        for packet in packets if isinstance(packets, list) else []:
            if not isinstance(packet, dict):
                continue
            declared.setdefault(str(packet.get("stem")), set()).add(str(packet.get("content_sha")))
            if not isinstance(packet.get("text"), str):
                continue
            sha = hashlib.sha256(packet["text"].encode("utf-8")).hexdigest()
            if sha == packet.get("content_sha"):
                texts[(str(packet.get("stem")), sha)] = packet["text"]
    return texts, declared


def import_reviews(root: Path, paths: list[Path], judge: str, today: str | None = None) -> dict:
    """Verify judge rows against the notes and store them; nothing is written if any row fails.

    A row's `content_sha` must be 64 lower-case hex digits. A row for the note's current version
    is checked against the note. A row for an earlier version (the note changed after export)
    is checked against the exported text when it is found beside the judge file, and is stored
    as stale either way; a sha that no packet for the note beside the judge file declares is a
    miscopy and rejected. With no exported packet for the note at all, quotes that are not in
    the current note are stored unverified."""
    reviewed_on = today or dt.date.today().isoformat()
    exported, declared = exported_texts(paths)
    entries: dict[str, dict] = {}
    currents: dict[str, str] = {}
    seen: dict[str, str] = {}
    for path in paths:
        try:
            rows = _rows(Path(path))
        except OSError as error:
            raise ValueError(f"{path}: cannot read: {error.strerror or error}") from error
        except ValueError as error:
            raise ValueError(f"{path}: not JSON lines: {error}") from error
        for number, row in enumerate(rows, start=1):
            if not isinstance(row, dict):
                raise ValueError(f"{path}: row {number} is not a JSON object")
            stem = str(row.get("stem") or "")
            if not STEM.match(stem):
                raise ValueError(f"{path}: row {number}: bad note stem {stem!r}")
            if stem in seen:
                raise ValueError(f"{path}: {stem}: a second row for this note in one import (the first is in {seen[stem]})")
            seen[stem] = f"{path} row {number}"
            note = _note_path(root, stem)
            if not _is_note(note):
                raise ValueError(f"{path}: unknown note {stem!r}")
            overall = row.get("overall")
            if overall not in OVERALL:
                raise ValueError(f"{path}: {stem}: bad overall verdict {overall!r}")
            given = row.get("claims") or []
            if not isinstance(given, list) or not all(isinstance(claim, dict) for claim in given):
                raise ValueError(f"{path}: {stem}: claims must be a list of JSON objects")
            sha = row.get("content_sha")
            if not isinstance(sha, str) or not SHA.fullmatch(sha):
                raise ValueError(f"{path}: {stem}: content_sha must be the packet's 64 lower-case hex digits, not {sha!r}")
            raw = note.read_bytes()  # one read, so the quotes are checked against the bytes hashed
            current = hashlib.sha256(raw).hexdigest()
            source, strict = raw.decode("utf-8", errors="replace"), True
            if sha != current:
                if (stem, sha) in exported:
                    source = exported[(stem, sha)]
                elif sha not in declared.get(stem, {sha}):
                    raise ValueError(f"{path}: {stem}: content_sha {sha[:12]}... is neither the note's nor that of its "
                                     "exported packet beside the judge file (miscopied?)")
                else:
                    strict = False
            if len(given) > MAX_CLAIMS:
                raise ValueError(f"{path}: {stem}: {len(given)} claims; at most {MAX_CLAIMS}")
            claims = [_claim_entry(f"{path}: {stem}", claim, source, strict) for claim in given]
            conflict = overall_conflict(overall, claims)
            if conflict:
                raise ValueError(f"{path}: {stem}: overall {overall!r} contradicts the claims: {conflict}")
            currents[stem] = current
            entries[stem] = {
                "reviewed_on": reviewed_on,
                "judge": judge,
                "content_sha": sha,
                "overall": overall,
                "claims": claims,
                "summary": str(row.get("summary", ""))[:1500],
                "stale": sha != current,
            }
    data = load_reviews(root)
    notes = data.setdefault("notes", {})
    # A row that is stale on arrival (an earlier pass, re-imported) never replaces a review of
    # the note's current bytes.
    skipped = sorted(stem for stem, entry in entries.items() if entry["stale"]
                     and isinstance(notes.get(stem), dict) and notes[stem].get("content_sha") == currents[stem])
    stored = {stem: entry for stem, entry in entries.items() if stem not in skipped}
    notes.update(stored)
    store = root / REVIEWS
    store.parent.mkdir(parents=True, exist_ok=True)
    tmp = store.with_name(f".{store.name}.{os.getpid()}.tmp")  # replaced in one step, never left half written
    try:
        tmp.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(tmp, store)
    finally:
        tmp.unlink(missing_ok=True)
    return {"imported": sorted(stored), "stale": sorted(stem for stem, entry in stored.items() if entry["stale"]),
            "skipped": skipped}


FLAGGED = ("unsound", "needs-work")
QUEUE = "research/audits/REFEREE_QUEUE.md"
NEXT = 30


def worst_claim(entry: dict) -> dict | None:
    claims = entry.get("claims") or []
    return max(claims, key=lambda claim: WORST.get(claim.get("verdict"), 0)) if claims else None


def stored_reviews(root: Path) -> dict:
    """Stored reviews whose key is a note name: import never writes another, so a hand-added
    key such as a path is skipped (a malformed entry already failed in load_reviews)."""
    return {stem: entry for stem, entry in load_reviews(root).get("notes", {}).items() if STEM.match(stem)}


def is_stale(root: Path, stem: str, entry: dict) -> bool:
    """True when the note is gone or its bytes differ from the version the judge read."""
    path = _note_path(root, stem)
    return not _is_note(path) or note_sha(path) != entry.get("content_sha")


def status(root: Path) -> dict:
    if not (root / REVIEWS).exists():
        return {"available": False, "reason": f"no reviews yet ({REVIEWS} absent)", "reviewed": 0, "flagged": [], "stale": []}
    notes = stored_reviews(root)
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
            *(["- Quote: not found in the current note, and the version the judge read was not available to check it."]
              if claim.get("verified") is False else []),
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
    notes = stored_reviews(root)
    stale = sorted(stem for stem, entry in notes.items() if is_stale(root, stem, entry))
    out = (root / REVIEWS).parent
    out.mkdir(parents=True, exist_ok=True)
    for stem, entry in sorted(notes.items()):
        (out / f"{stem}.md").write_text(_render_review(stem, entry, stem in stale), encoding="utf-8")
    queue = root / QUEUE
    queue.write_text(_render_queue(root, notes, stale, today or dt.date.today().isoformat()), encoding="utf-8")


def _count(least: int):
    def parse(text: str) -> int:
        try:
            value = int(text)
        except ValueError:
            raise argparse.ArgumentTypeError(f"not an integer: {text!r}") from None
        if value < least:
            raise argparse.ArgumentTypeError(f"must be at least {least}: {value}")
        return value
    return parse


def _selected(root: Path, args: argparse.Namespace) -> list[Path]:
    return select_notes(root, prefixes=tuple(args.prefix), limit=args.limit, exclude_reviewed=not args.include_reviewed)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    choose = argparse.ArgumentParser(add_help=False)
    choose.add_argument("--prefix", action="append", default=[], help="Only notes whose stem starts with this (repeatable).")
    choose.add_argument("--limit", type=_count(0), default=NEXT, help="At most this many notes; 0 for all.")
    choose.add_argument("--include-reviewed", action="store_true", help="Keep notes whose review is still current.")
    sub = parser.add_subparsers(dest="command", required=True)
    select = sub.add_parser("select", parents=[common, choose], help="List the newest review-pending notes.")
    select.add_argument("--json", action="store_true")
    export = sub.add_parser("export", parents=[common, choose], help="Write INSTRUCTIONS.md and judge batches.")
    export.add_argument("--out-dir", type=Path, required=True)
    export.add_argument("--batch-size", type=_count(1), default=5)
    export.add_argument("--note", action="append", default=[], metavar="STEM",
                        help="Export this note whatever its status (repeatable); replaces the selection.")
    imp = sub.add_parser("import", parents=[common], help="Verify and store judge reviews (JSONL).")
    imp.add_argument("files", nargs="+", type=Path)
    imp.add_argument("--judge", required=True, help="Judge name stored with each review.")
    sub.add_parser("render", parents=[common], help="Write reviews/<STEM>.md and REFEREE_QUEUE.md.")
    stat = sub.add_parser("status", parents=[common], help="Flagged and stale reviews.")
    stat.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        return _run(parser, args)
    except StoreError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


def _run(parser: argparse.ArgumentParser, args: argparse.Namespace) -> int:
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
            notes = [_note_path(root, Path(stem).name.removesuffix(".md")) for stem in args.note]
            missing = [path.stem for path in notes if not _is_note(path)]
            if missing:
                parser.error(f"no such note: {', '.join(missing)}")
        else:
            notes = _selected(root, args)
        try:
            paths = export_batches(root, args.out_dir, notes, batch_size=args.batch_size)
        except ValueError as error:
            print(f"error: {error}; nothing exported", file=sys.stderr)
            return 2
        print(f"{len(notes)} notes in {len(paths)} batches; instructions in {args.out_dir / 'INSTRUCTIONS.md'}")
        return 0

    if args.command == "import":
        try:
            result = import_reviews(root, args.files, args.judge)
        except ValueError as error:
            print(f"error: {error}; nothing imported", file=sys.stderr)
            return 2
        stale = f": {', '.join(result['stale'])}" if result["stale"] else ""
        skipped = (f"; {len(result['skipped'])} skipped (a current review is stored): {', '.join(result['skipped'])}"
                   if result["skipped"] else "")
        print(f"imported {len(result['imported'])} reviews; {len(result['stale'])} stale{stale}{skipped}")
        return 0

    if args.command == "render":
        render(root)
        print(f"wrote {len(stored_reviews(root))} reviews and {QUEUE}")
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
