"""Parse a research note into the packet a referee reads.

The packet keeps what a judge needs to test a note: the status block and what the preamble
says is not claimed, the producer command and its JSON artifact, the result section, the
derivation, control, self-check and decision sections, and the claim checker's flags on the
result. Sections are cut at `## ` headings outside fenced code.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from tools.claim_checker.check import check_text, split_sentences
from tools.corpus.sources.markdown import _sections, note_status

DATE = re.compile(r"20\d\d-\d\d-\d\d")
NEGATION = re.compile(r"\b(not|no)\b", re.I)
PRODUCER = re.compile(r"python (theorems/\w+\.py)([^`\n]*)")
ARTIFACT = re.compile(r"(?:research/)?[a-z_]+/[\w./-]+\.json")
# The script's own REPORT constant, not a prefixed one such as BASE_REPORT.
REPORT = re.compile(r"^[ \t]*REPORT\s*(?::[^=\n]*)?=.*?[\"']([^\"']+\.json)[\"']", re.M)
FENCE = re.compile(r"^\s*(```|~~~)")
LIST_MARKER = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")

RESULT = re.compile(r"Result|Question|Claim|Summary")
NOT_RESULT = re.compile(r"\b(?:Not|Cannot|Why)\b|\bNext\b.*\bQuestion|\b(?:Kill|Break)\b.*\bClaim")
DERIVATION = re.compile(r"Derivation|Lemma|Proof|\bBound(?:s|ing)?\b|Certificate")
CONTROLS = re.compile(r"Controls|Comparison|Classical")
SELF_CHECK = re.compile(
    r"Prov(?:e|ing)\b.*\bWrong|Disprove|Falsifi|(?i:to|and|can) Falsify|Refutation|Attempts? To Break|Kill|Self-Critique|Red Team")
DECISION = re.compile(r"Decision|Next")
WHY = re.compile(r"\bWhy\b")


@dataclass
class NotePacket:
    stem: str
    path: str
    title: str
    date: str | None
    status: str
    not_claimed: list[str]
    producer: dict | None
    result: str
    derivations: list[dict]
    controls: list[dict]
    self_check: str | None
    decision: str | None
    content_sha: str
    flags: list[str]


def _fenced(lines: list[str]) -> list[bool]:
    """True for fence markers and the lines between them."""
    inside, marks = False, []
    for line in lines:
        if FENCE.match(line):
            marks.append(True)
            inside = not inside
        else:
            marks.append(inside)
    return marks


def _note_sections(lines: list[str]) -> list[tuple[str, int, list[str]]]:
    """`markdown._sections` with `## ` lines inside fences kept in their section."""
    masked = [" " + line if inside and line.startswith("## ") else line for line, inside in zip(lines, _fenced(lines))]
    sections = []
    for index, (heading, line_no, body) in enumerate(_sections(masked)):
        start = 0 if index == 0 else line_no
        sections.append((heading, line_no, lines[start:start + len(body)]))
    return sections


def _status_block(lines: list[str]) -> list[str]:
    """Preamble lines from the first non-empty line after the title up to the next blank line."""
    block: list[str] = []
    for line in lines:
        if line.startswith("## "):
            break
        if line.startswith("# "):
            continue
        if not line.strip():
            if block:
                break
            continue
        block.append(line)
    return block


def prose(text: str) -> str:
    """Drop headings, table rows, fenced and indented code; strip list markers."""
    kept, inside = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            inside = not inside
            continue
        if inside or line.lstrip().startswith(("#", "|")) or line.startswith(("    ", "\t")):
            continue
        kept.append(LIST_MARKER.sub("", line))
    return "\n".join(kept).strip()


def _not_claimed(preamble: list[str]) -> list[str]:
    """Preamble sentences, and whole bullets, that contain "not" or "no"."""
    items: list[tuple[bool, list[str]]] = []
    for line, inside in zip(preamble, _fenced(preamble)):
        if inside or line.startswith("# ") or line.lstrip().startswith("|"):
            continue
        if not line.strip():
            items.append((False, []))
        elif LIST_MARKER.match(line):
            items.append((True, [LIST_MARKER.sub("", line)]))
        elif items:
            items[-1][1].append(line)
        else:
            items.append((False, [line]))
    found = []
    for bullet, parts in items:
        text = " ".join(" ".join(parts).split())
        if text:
            found += [piece for piece in ([text] if bullet else split_sentences(text)) if NEGATION.search(piece)]
    return found


def _producer(text: str, root: Path, stem: str = "") -> dict | None:
    """The note's own command (`theorems/<stem lower>.py`) if it runs one, else the first;
    with no command, the stem script `theorems/<stem lower>.py` when it exists (command None).

    Its artifact: a JSON path in the note named after the script, else the script's
    `REPORT` when that file exists, else the first JSON path in the note, else `REPORT`."""
    commands = list(PRODUCER.finditer(text))
    named = [match.group(0) for match in ARTIFACT.finditer(text)]
    own_script = f"theorems/{stem.lower()}.py"
    if commands:
        command = next((match for match in commands if match.group(1) == own_script), commands[0])
        script, flags = command.group(1), command.group(2).strip()
        line = f"python {script} {flags}".strip()
    elif stem and (root / own_script).is_file():
        script, flags, line = own_script, "", None
    else:
        return None if not named else {"command": None, "script": None, "flags": "", "artifact": named[0]}
    source = root / script
    found = REPORT.search(source.read_text(encoding="utf-8", errors="replace")) if source.is_file() else None
    report = found.group(1) if found else None
    own = next((name for name in named if Path(name).stem == Path(script).stem), None)
    if own:
        artifact = own
    elif report and _resolve_artifact(root, report):
        artifact = report
    else:
        artifact = named[0] if named else report
    return {"command": line, "script": script, "flags": flags, "artifact": artifact}


def _section_dict(section: tuple[str, int, list[str]]) -> dict:
    heading, line, body = section
    return {"heading": heading, "line": line, "text": "\n".join(body).strip()}


def parse_note(path: Path, raw: bytes | None = None) -> NotePacket:
    """The packet for the note at `path`, parsed from `raw` (its bytes, read once) when given."""
    raw = path.read_bytes() if raw is None else raw
    text = raw.decode("utf-8", errors="replace")
    lines = text.splitlines()
    title = next((line[2:].strip() for line in lines if line.startswith("# ")), path.stem)
    sections = _note_sections(lines)
    preamble, body = sections[0], sections[1:]
    block = " ".join(_status_block(lines))
    date = DATE.search(block)

    def first(pattern: re.Pattern) -> str | None:
        hit = next((s for s in body if pattern.search(s[0])), None)
        return _section_dict(hit)["text"] if hit else None

    # "What Can And Cannot Be Claimed" and "Why This Is The Next Question" are not results.
    chosen = next((s for s in body if RESULT.search(s[0]) and not NOT_RESULT.search(s[0])), None)
    explicit = chosen is not None
    if chosen is None:
        chosen = body[0] if body else (preamble[0], preamble[1], [line for line in preamble[2] if not line.startswith("# ")])
    result = _section_dict(chosen)["text"]
    # The first decision heading, passing over a result heading ("Question And Decision") and
    # motivations ("Why This Is The Next Question") when another one exists.
    decisions = [s for s in body if DECISION.search(s[0])]
    reasons = [s for s in decisions if not WHY.search(s[0])]
    preferred = [s for s in reasons if not (explicit and s is chosen)]
    decision = (preferred or reasons or decisions or [None])[0]
    return NotePacket(
        stem=path.stem,
        path=f"{path.parent.name}/{path.name}",
        title=title,
        date=date.group(0) if date else None,
        status=note_status(lines),
        not_claimed=_not_claimed(preamble[2]),
        producer=_producer(text, path.parents[1], path.stem),
        result=result,
        derivations=[_section_dict(s) for s in body if DERIVATION.search(s[0]) and s is not chosen and s is not decision],
        controls=[_section_dict(s) for s in body if CONTROLS.search(s[0])],
        self_check=first(SELF_CHECK),
        decision=_section_dict(decision)["text"] if decision else None,
        content_sha=hashlib.sha256(raw).hexdigest(),
        flags=[flag.name for flag in check_text(prose(result), title).flags if not flag.negated],
    )


def to_dict(packet: NotePacket) -> dict:
    return asdict(packet)


LIST_ITEMS = 5
MAX_STRING = 60
MAX_KEYS = 50
TRUNCATED = "[truncated]"


def _resolve_artifact(root: Path, rel: str) -> Path | None:
    """Notes write artifacts as `research/x/y.json` or `x/y.json`."""
    for candidate in (root / rel, root / "research" / rel):
        if candidate.is_file():
            return candidate
    return None


def _leaves(value, path: str):
    """Depth-first `path = value` lines in sorted key order: numbers and short strings."""
    if isinstance(value, dict):
        for key in sorted(value, key=str):
            yield from _leaves(value[key], f"{path}.{key}" if path else str(key))
    elif isinstance(value, list):
        for index, item in enumerate(value[:LIST_ITEMS]):
            yield from _leaves(item, f"{path}[{index}]")
        if len(value) > LIST_ITEMS:
            yield f"{path or '[]'} ... (+{len(value) - LIST_ITEMS})"
    elif isinstance(value, bool) or value is None:
        return
    elif isinstance(value, (int, float)):
        yield f"{path} = {value!r}"
    elif isinstance(value, str) and len(value) <= MAX_STRING:
        yield f"{path} = {json.dumps(value, ensure_ascii=False)}"


def _shared_leaves(data, budget: int) -> tuple[list[str], bool]:
    """Leaves taken in turn from each top-level key until `budget` characters (one newline
    per line counted), then grouped by key; True when some were left out. A large first key
    no longer hides the others."""
    keys = sorted(data, key=str) if isinstance(data, dict) else [None]
    streams = [_leaves(data[key], str(key)) if key is not None else _leaves(data, "") for key in keys]
    taken: list[list[str]] = [[] for _ in streams]
    active, used = list(range(len(streams))), 0
    while active:
        still = []
        for index in active:
            line = next(streams[index], None)
            if line is None:
                continue
            if used + len(line) + 1 > budget:
                return [line for lines in taken for line in lines], True
            taken[index].append(line)
            used += len(line) + 1
            still.append(index)
        active = still
    return [line for lines in taken for line in lines], False


def artifact_excerpt(root: Path, packet: NotePacket, max_chars: int = 4000) -> str | None:
    """A compact view of the producer's JSON artifact, or None when it is absent or unreadable."""
    rel = (packet.producer or {}).get("artifact")
    path = _resolve_artifact(root, rel) if rel else None
    if path is None:
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError):
        return None
    if isinstance(data, dict):
        keys = sorted(map(str, data))
        more = f" ... (+{len(keys) - MAX_KEYS})" if len(keys) > MAX_KEYS else ""
        head = f"keys: {', '.join(keys[:MAX_KEYS])}{more}"
    else:
        head = f"keys: none (top level is a {type(data).__name__})"
    leaves, cut = _shared_leaves(data, max_chars - len(head) - len(TRUNCATED) - 1)
    text = "\n".join([head, *leaves, *([TRUNCATED] if cut else [])])
    return text if len(text) <= max_chars else text[: max_chars - len(TRUNCATED) - 1] + "\n" + TRUNCATED
