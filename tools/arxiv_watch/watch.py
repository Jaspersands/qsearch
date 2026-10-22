"""Watch arXiv for papers that could kill, support or scoop a Q-Search track.

    python tools/arxiv_watch/watch.py                  # since the last run, with a 7-day overlap
    python tools/arxiv_watch/watch.py --since 2026-09-01 --tracks dcp,dqi_opi
    python tools/arxiv_watch/watch.py --relabel        # re-apply the label rules to stored papers, offline
    python tools/arxiv_watch/watch.py --replay-seeds   # check the track classifier on seed papers
    python tools/arxiv_watch/watch.py --verdict 2610.06753 should-cite --reason "..." [--action "..."]
    python tools/arxiv_watch/watch.py --action-done 2610.06753  # its action has been carried out

Each new paper is placed on tracks, matched against the corpus index (nearest negatives,
notes, theorem modules) and given a triage label from wording cues:
possible-kill, possible-scoop, related, already-cited or unrelated. Labels are for
triage only; read the paper before acting on one. A reviewed verdict (research/audits/
arxiv_verdicts.json, see verdicts.py) is judgement: it is attached to the stored paper and
listed in the digest's Reviewed table. A person's verdict also moves the paper out of the
flagged sections; a judge's leaves it there, marked, until a person records one.

Each track query is paged until results are older than the window start. When the page
cap stops a query first, the uncovered window is recorded as a gap in the JSON and listed
in the digest until a later run covers it. The outputs are rewritten only when a run finds
something new (a paper, a gap opening or closing, a verdict, a citation of a flagged paper, or
another track's query returning a stored paper), so a quiet week changes nothing.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.arxiv_watch.tracks import TRACKS, Track, classify  # noqa: E402
from tools.arxiv_watch.verdicts import (  # noqa: E402
    VERDICTS, VERDICTS_FILE, by_judge, load_verdicts, mark_action_done, normalize_id, set_verdict, verdict_entry,
)
from tools.corpus.api import Corpus  # noqa: E402
from tools.corpus.docs import read_json  # noqa: E402
from tools.corpus.sources.arxiv import Client, Paper  # noqa: E402

# arXiv's `published` is the v1 submission date; a paper can be listed days later (weekends,
# holds), so each run re-reads a week before the previous one and dedupes by id.
OVERLAP_DAYS = 7
FIRST_RUN_DAYS = 14
PAGE_SIZE = 100
MAX_PAGES = 10

# --- labels -------------------------------------------------------------------------------------
# A kill cue needs a classical-algorithm or negative-result framing; a scoop cue needs positive
# quantum framing. Bare words such as "lower bound", "limitation" or a background "no-go" are not
# cues: positive papers use them for their own optimality proofs and for prior work.

_WE = r"\b(?:we|our|i|this (?:paper|work))\b"
_VERB = r"(?:give|present|propose|design|introduce|construct|develop|obtain|describe|provide)s?"
_CLASSICAL = r"classical (?:algorithm|solver|sampler|simulation|simulator|procedure|method)s?"
_NEGATION = re.compile(r"\b(?:no|not|against|rules? out|ruling out|without|cannot|lack of|absence of)\b[^.]{0,30}$", re.I)
# "conjectured hard for polynomial-time classical algorithms" is not a classical win.
_CLASSICAL_HARD = re.compile(
    r"\b(?:hard|harder|intractable|infeasible|beyond|outperforms?|beats?|than|no known|not known|exceeds?|against|unlike)\b"
    r"[^.]{0,30}$",
    re.I,
)
# An efficient classical algorithm named without a verb; guarded by _CLASSICAL_HARD.
_EFFICIENT_CLASSICAL = re.compile(
    rf"\b(?:efficient|polynomial[- ]time|quasi-?polynomial[- ]time|sub-?linear[- ]time|near-linear[- ]time|fast)\s+{_CLASSICAL}",
    re.I,
)

KILL_CUES = (_EFFICIENT_CLASSICAL,) + tuple(
    re.compile(pattern, re.I)
    for pattern in (
        rf"{_WE}[^.]{{0,60}}?\b{_VERB}\b[^.]{{0,40}}?\b{_CLASSICAL}",
        rf"{_WE}[^.]{{0,40}}?\bdequantiz\w*",
        r"\bdequantiz\w*\s+(?:of\s+)?(?:the\s+|this\s+|these\s+|an?\s+)?[^.]{0,40}?\bquantum\b",
        r"\b(?:no|against(?: an?)?|rules? out|ruling out|precludes?|(?:can ?not|does not|do not|fails? to) "
        r"(?:yield|give|provide|achieve|offer|admit))\s+(?:\w+\s+){0,3}?(?:quantum\s+)?(?:advantages?|speed-?ups?)\b",
        r"\b(?:advantage|guarantee|margin|speed-?up|improvement)\b[^.]{0,60}?\b(?:by at most|is at most|cannot exceed|is bounded by)\b",
        r"\bno \w+(?: \w+){0,4}? can (?:exceed|beat|outperform)\b",
        r"\b(?:any|every|no) (?:efficient |polynomial[- ]time )?quantum (?:algorithm|computer|circuit|strategy|measurement)s? "
        r"(?:requires?|needs?|must|cannot|can't|fails?)\b",
        r"\b(?:efficiently|can be) classically simulat\w*|\bclassically simulable\b",
        rf"{_WE}[^.]{{0,60}}?\b(?:refut\w*|disprov\w*)",
    )
)
TITLE_KILL_CUES = KILL_CUES + tuple(
    re.compile(pattern, re.I)
    for pattern in (
        r"\bclassical (?:algorithm|solver|simulation|sampler)s?\b",
        r"\bdequantiz\w*",
        r"\bno[- ]go\b",
        r"\bimpossib\w*",
        r"\bbarriers?\b",
        r"\blower bounds?\b",
        r"\blimit(?:s|ations)? (?:of|on|for) quantum\b",
    )
)
SCOOP_CUES = tuple(
    re.compile(pattern, re.I)
    for pattern in (
        rf"{_WE}[^.]{{0,80}}?\b{_VERB}\b[^.]{{0,60}}?\bquantum algorithms?\b",
        r"\befficient quantum (?:\w+ )?(?:algorithm|circuit|transform|protocol|implementation|procedure)s?\b",
        r"\bpolynomial[- ]time quantum algorithms?\b",
    )
)
# Only in a sentence the authors frame as their own (we/our/this paper) and with no "classical"
# in it, e.g. "We propose a Gibbs state preparation algorithm".
AUTHORED_SCOOP_CUES = tuple(
    re.compile(pattern, re.I)
    for pattern in (
        rf"\b(?:we|i)\s+(?:also\s+)?{_VERB}\s+[^.]{{0,60}}?\balgorithms?\b",
        r"\b(?:exponential|super-?polynomial|polynomial|quadratic|provable|unconditional)\s+(?:quantum\s+)?(?:space\s+|time\s+)?"
        r"(?:speed-?ups?|advantages?)\b",
    )
)
TITLE_SCOOP_CUES = SCOOP_CUES + AUTHORED_SCOOP_CUES[1:] + (
    re.compile(r"\bquantum algorithms?\b", re.I),
    re.compile(r"\bquantum (?:advantage|speed-?up)s?\b", re.I),
)
_AUTHORED = re.compile(_WE, re.I)

NEAREST_KINDS = ("negative", "dequant", "note", "hypothesis", "theorem")
LABEL_ORDER = ("possible-kill", "possible-scoop", "related", "already-cited", "unrelated")
FLAGGED = ("possible-kill", "possible-scoop")


@dataclass
class RunReport:
    fetched: int = 0
    new: int = 0
    by_label: dict = field(default_factory=dict)
    truncated: dict = field(default_factory=dict)
    saved: bool = False
    relabelled: int = 0


def _sentences(text: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def _matches(patterns, text: str, positive: bool = False) -> list[str]:
    found = []
    for pattern in patterns:
        for match in pattern.finditer(text):
            before = text[max(0, match.start() - 40) : match.start()]
            if positive and _NEGATION.search(before):
                continue  # "evidence against an exponential quantum advantage"
            if pattern is _EFFICIENT_CLASSICAL and _CLASSICAL_HARD.search(before):
                continue
            found.append(match.group(0))
            break
    return found


def _sentence_scoop_cues(sentence: str) -> list[str]:
    cues = _matches(SCOOP_CUES, sentence, positive=True)
    if _AUTHORED.search(sentence) and "classical" not in sentence.lower():
        cues += _matches(AUTHORED_SCOOP_CUES, sentence, positive=True)
    return cues


def label_cues(paper: Paper) -> tuple[list[str], list[str], bool, bool]:
    """(kill cues, scoop cues, title frames a kill, title frames a scoop)."""
    title_kill = _matches(TITLE_KILL_CUES, paper.title)
    title_scoop = [] if title_kill else _matches(TITLE_SCOOP_CUES, paper.title, positive=True)
    kill, scoop = list(title_kill), list(title_scoop)
    for sentence in _sentences(paper.abstract):
        negative = _matches(KILL_CUES, sentence)
        if negative:
            kill += negative  # a sentence framed as a negative result contributes no scoop cue
        else:
            scoop += _sentence_scoop_cues(sentence)
    return kill, scoop, bool(title_kill), bool(title_scoop)


def label_for(paper: Paper, tracks: list[str], cited: bool) -> tuple[str, list[str]]:
    """Kill and scoop labels need a core track and a quantum paper; everything else is related.

    Precedence: a kill framed in the title, then a scoop framed in the title, then any positive
    quantum framing in the abstract, then a kill cue in the abstract.
    """
    kill, scoop, title_kill, title_scoop = label_cues(paper)
    cues = list(dict.fromkeys(kill + scoop))
    if cited:
        return "already-cited", cues
    if not tracks:
        return "unrelated", cues
    core = any(TRACKS[name].core for name in tracks if name in TRACKS)
    quantum = re.search(r"quantum", f"{paper.title}. {paper.abstract}", re.I) is not None
    if not (core and quantum):
        return "related", cues
    if title_kill:
        return "possible-kill", cues
    if title_scoop or scoop:
        return "possible-scoop", cues
    if kill:
        return "possible-kill", cues
    return "related", cues


def _stored_paper(arxiv_id: str, record: dict) -> Paper:
    return Paper(
        arxiv_id, record.get("version", ""), record["title"], record.get("abstract", ""), record.get("authors", []),
        record["published"], record.get("updated", ""), record.get("categories", []), record["url"],
    )


def relabel(root: Path, corpus: Corpus) -> int:
    """Recompute tracks and labels for every stored paper after a rule change; returns how many changed."""
    state = _load_state(root)
    attach_verdicts(state, load_verdicts(root)["verdicts"])
    changed = 0
    for arxiv_id, record in state["papers"].items():
        paper = _stored_paper(arxiv_id, record)
        tracks = classify(f"{paper.title}. {paper.abstract}")
        label, cues = label_for(paper, tracks, cited=bool(corpus.mentions(arxiv_id)))
        if (label, tracks) != (record.get("label"), record.get("tracks")):
            changed += 1
        record.update({"label": label, "cues": cues, "tracks": tracks})
        if label != "already-cited":  # recheck_cited's demotion record no longer applies
            record.pop("relabelled_from", None)
            record.pop("relabelled_on", None)
    _save(root, state)
    return changed


def attach_verdicts(state: dict, verdicts: dict) -> int:
    """Copy each stored paper's verdict onto its record; returns how many records changed.

    `verdicts` maps arXiv id to entry, as in `load_verdicts(root)["verdicts"]`. A record has a
    `verdict` key only while the verdicts file holds one for it (a withdrawn verdict is dropped),
    so a week with no new paper and no new verdict leaves the JSON byte-identical.
    """
    changed = 0
    for arxiv_id, record in state["papers"].items():
        entry = verdicts.get(arxiv_id)
        if entry is not None:
            if record.get("verdict") != entry:
                record["verdict"] = dict(entry)
                changed += 1
        elif "verdict" in record:
            del record["verdict"]
            changed += 1
    return changed


def recheck_cited(state: dict, corpus: Corpus, today: str) -> int:
    """Demote stored possible kills and scoops to already-cited once a note or record cites them.

    Papers with a verdict are left alone. The record keeps the date and the label it had; returns
    how many records changed.
    """
    changed = 0
    for arxiv_id, record in sorted(state["papers"].items()):
        if record.get("label") not in FLAGGED or "verdict" in record:
            continue
        if corpus.mentions(arxiv_id):
            record.update({"label": "already-cited", "relabelled_on": today, "relabelled_from": record["label"]})
            changed += 1
    return changed


# --- state ----------------------------------------------------------------------------------------


def _save(root: Path, state: dict) -> None:
    path, digest = _paths(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest.write_text(render_digest(state, verdicts=load_verdicts(root)["verdicts"]), encoding="utf-8")


def _paths(root: Path) -> tuple[Path, Path]:
    audits = root / "research" / "audits"
    return audits / "arxiv_collisions.json", audits / "ARXIV_WATCH.md"


def _load_state(root: Path) -> dict:
    """The collisions file; empty when absent. ValueError, naming the file, when it is not JSON or
    not an object with a "papers" object."""
    path, _ = _paths(root)
    if not path.exists():
        return {"updated": None, "papers": {}}
    name = path.relative_to(root)
    try:
        state = read_json(path)
    except ValueError as error:
        raise ValueError(f"{name}: not valid JSON ({error})") from error
    if not isinstance(state, dict) or not isinstance(state.get("papers"), dict):
        raise ValueError(f'{name}: expected an object with a "papers" object')
    return state


def checkout_error(root: Path) -> str | None:
    """Why `root` cannot be a Q-Search checkout (it has no research/ directory), or None."""
    if not (Path(root) / "research").is_dir():
        return f"{root} is not a Q-Search checkout (no research/ directory); check --root"
    return None


def _since_for(state: dict, name: str, today: str) -> str:
    """A track's usual window start: a week before its own last fetch. A track with no date of its
    own (a state written before per-track dates) last ran no later than `updated`."""
    last = (state.get("tracks_updated") or {}).get(name) or state.get("updated")
    if last:
        return (dt.date.fromisoformat(last) - dt.timedelta(days=OVERLAP_DAYS)).isoformat()
    return (dt.date.fromisoformat(today) - dt.timedelta(days=FIRST_RUN_DAYS)).isoformat()


def fetch_track(client, query: str, since: str, page_size: int = PAGE_SIZE, max_pages: int = MAX_PAGES):
    """Page a newest-first query until a page reaches back past `since`.

    Returns (papers, cut): `cut` is None when the window was covered, else a description of
    where the page cap stopped the query. Pacing between requests is the client's job.
    """
    papers: list[Paper] = []
    for page in range(max_pages):
        batch = client.search(query, max_results=page_size, start=page * page_size)
        papers.extend(batch)
        if len(batch) < page_size or min(p.published for p in batch) < since:
            return papers, None
    oldest = min((p.published for p in papers), default=since)
    return papers, {"pages": max_pages, "page_size": page_size, "results": len(papers), "oldest_seen": oldest}


def run(
    root: Path,
    client,
    corpus: Corpus,
    since: str | None = None,
    tracks: dict[str, Track] | None = None,
    page_size: int = PAGE_SIZE,
    max_pages: int = MAX_PAGES,
    today: str | None = None,
) -> RunReport:
    tracks = tracks or TRACKS
    today = today or dt.date.today().isoformat()
    state = _load_state(root)

    fetched: dict[str, tuple[Paper, set[str]]] = {}
    windows: dict[str, str] = {}
    usual: dict[str, str] = {}
    report = RunReport()
    for name, track in tracks.items():
        usual[name] = _since_for(state, name, today)
        start = since or usual[name]
        windows[name] = start
        papers, cut = fetch_track(client, track.arxiv_query(), start, page_size, max_pages)
        if cut is not None:
            report.truncated[name] = {**cut, "since": start}
        for paper in papers:
            if paper.published < start:
                continue
            entry = fetched.setdefault(paper.arxiv_id, (paper, set()))
            entry[1].add(name)

    changed = False
    report.fetched = len(fetched)
    for arxiv_id, (paper, queried) in sorted(fetched.items()):
        # Seen before: not re-reported or re-scored, only its queried_by can grow. Verdicts and
        # citations below may still change the record (attach_verdicts, recheck_cited).
        if arxiv_id in state["papers"]:
            known = state["papers"][arxiv_id]
            merged = sorted(set(known.get("queried_by", [])) | queried)
            if merged != known.get("queried_by"):
                known["queried_by"] = merged
                changed = True
            continue
        text = f"{paper.title}. {paper.abstract}"
        tracks_found = classify(text)
        cited = bool(corpus.mentions(arxiv_id))
        label, cues = label_for(paper, tracks_found, cited)
        nearest = corpus.search(text, kinds=NEAREST_KINDS, k=5)
        state["papers"][arxiv_id] = {
            **{key: value for key, value in asdict(paper).items() if key != "abstract"},
            "abstract": paper.abstract[:1500],
            "tracks": tracks_found,
            "queried_by": sorted(queried),
            "label": label,
            "cues": cues,
            "nearest": [
                {"doc_id": h.doc_id, "kind": h.kind, "location": h.location, "title": h.title[:200]} for h in nearest
            ],
            "first_seen": today,
        }
        changed = True
        report.new += 1
        report.by_label[label] = report.by_label.get(label, 0) + 1

    # After the fetch, so a paper given a verdict before it was first stored carries it on arrival.
    changed |= bool(attach_verdicts(state, load_verdicts(root)["verdicts"]))
    report.relabelled = recheck_cited(state, corpus, today)
    changed |= bool(report.relabelled)

    # A gap stays listed until a run of that track that was not cut short starts at or before it.
    gaps = list(state.get("gaps", []))
    kept = [g for g in gaps if not (g["track"] in windows and g["track"] not in report.truncated and windows[g["track"]] <= g["since"])]
    for name, cut in report.truncated.items():
        gap = {"track": name, "since": cut["since"], "until": cut["oldest_seen"], "found_on": today}
        if gap not in kept:
            kept.append(gap)
    if kept != gaps:
        state["gaps"] = kept
        changed = True

    if changed:
        # Every track gets a date of its own before `updated` moves, so a run of some tracks never
        # shrinks another's window. A track whose --since started after its usual start keeps its
        # date, so its next run still fetches the days this one skipped.
        dates = state.get("tracks_updated") or {}
        if state.get("updated"):
            for name in sorted({*TRACKS, *tracks}):
                dates.setdefault(name, state["updated"])
        dates.update({name: today for name in tracks if windows[name] <= usual[name]})
        state["tracks_updated"] = dates
        state["updated"] = today
        _save(root, state)
        report.saved = True
    else:
        report.saved = _rerender_stale_digest(root, state)
    return report


def _rerender_stale_digest(root: Path, state: dict) -> bool:
    """Rewrite the digest alone when it no longer matches the stored papers and the verdicts file,
    e.g. after a verdict was added by hand for a paper the watch has not stored. Returns whether it
    was rewritten; a missing digest is left missing."""
    _, digest = _paths(root)
    if not digest.exists():
        return False
    text = render_digest(state, verdicts=load_verdicts(root)["verdicts"])
    if digest.read_text(encoding="utf-8") == text:
        return False
    digest.write_text(text, encoding="utf-8")
    return True


def _cell(text) -> str:
    return " ".join(str(text).split()).replace("|", "/")


def render_digest(state: dict, per_section: int = 40, verdicts: dict | None = None) -> str:
    """The markdown digest. `verdicts` (arXiv id -> entry) drives the Reviewed table, and papers
    with a person's verdict leave the possible-kill and possible-scoop sections; a flagged paper
    with only a judge's verdict stays there with "judge: VERDICT" in its cues. Those two sections
    list every paper; Related lists the newest `per_section` and counts the rest."""
    verdicts = verdicts or {}
    papers = sorted(state["papers"].values(), key=lambda p: (p["published"], p["arxiv_id"]), reverse=True)
    counts = {label: sum(p["label"] == label for p in papers) for label in LABEL_ORDER}
    lines = [
        "# arXiv Collision Watch",
        "",
        f"Last updated {state.get('updated')}. Generated by `tools/arxiv_watch/watch.py`; do not edit by hand.",
        "Labels come from wording cues and are for triage only. Read a paper before acting on its label.",
        "",
        "| Label | Papers |",
        "|---|---|",
        *[f"| {label} | {counts[label]} |" for label in LABEL_ORDER],
        "",
    ]
    if verdicts:
        lines += [
            "The counts are machine labels. A flagged paper with a person's verdict is listed under Reviewed,",
            "not in the possible-kill and possible-scoop sections. One with only a judge's verdict stays in",
            "its section, marked with that verdict, until a person checks it and records one.",
            "",
        ]
    gaps = state.get("gaps") or []
    if gaps:
        lines += [
            "## Incomplete coverage",
            "",
            "These track queries hit the page cap, so papers in the window below may be missing.",
            "Backfill with `watch.py --since SINCE --tracks TRACK --max-pages N`.",
            "",
            "| Track | Missing window | Found on |",
            "|---|---|---|",
            *[f"| {g['track']} | {g['since']} to {g['until']} | {g['found_on']} |" for g in gaps],
            "",
        ]
    titles = {"possible-kill": "Possible kills", "possible-scoop": "Possible scoops", "related": "Related"}
    for label, heading in titles.items():
        # A judge's verdict is one model's reading: it never moves a flag out of sight by itself.
        section = [
            p for p in papers
            if p["label"] == label and not (label in FLAGGED and p["arxiv_id"] in verdicts and not by_judge(verdicts[p["arxiv_id"]]))
        ]
        # Every flag is listed, however long the backlog: the oldest unreviewed kill matters most.
        shown = section if label in FLAGGED else section[:per_section]
        lines += [f"## {heading}", ""]
        if not shown:
            lines += ["None yet.", ""]
            continue
        lines += ["| Date | Paper | Tracks | Cues | Nearest Q-Search record |", "|---|---|---|---|---|"]
        for p in shown:
            nearest = p["nearest"][0] if p["nearest"] else None
            near = f"`{nearest['doc_id']}` ({nearest['location']})" if nearest else ""
            title = p["title"].replace("|", "/")
            cues = ", ".join(p.get("cues", [])[:3]).replace("|", "/")
            if label in FLAGGED and p["arxiv_id"] in verdicts:
                cues = f"**judge: {_cell(verdicts[p['arxiv_id']].get('verdict'))}**; {cues}"
            lines.append(
                f"| {p['published']} | [{p['arxiv_id']}]({p['url']}) {title} | {', '.join(p['tracks'])} | {cues} | {near} |"
            )
        lines.append("")
        if len(section) > len(shown):
            lines += [f"And {len(section) - len(shown)} more {label} papers, older, in `research/audits/arxiv_collisions.json`.", ""]
    lines += ["## Reviewed", ""]
    if not verdicts:
        lines += ["None yet.", ""]
        return "\n".join(lines)
    lines += [
        f"Verdicts from `{VERDICTS_FILE}`. Labels are triage; verdicts are judgement.",
        "A paper listed as not stored has a verdict but is not in the collisions file.",
        "",
        "| arXiv | Paper | Label | Verdict | By | Reviewed | Reason | Action |",
        "|---|---|---|---|---|---|---|---|",
    ]
    rank = {verdict: index for index, verdict in enumerate(VERDICTS)}
    for arxiv_id, entry in sorted(verdicts.items(), key=lambda item: (rank.get(item[1].get("verdict"), len(rank)), item[0])):
        p = state["papers"].get(arxiv_id)
        paper = f"[{_cell(p['title'])}]({p['url']})" if p else "not stored"
        action = _cell(entry.get("action") or "")
        if action and entry.get("action_done"):
            action += " (done)"
        lines.append(
            f"| {arxiv_id} | {paper} | {p['label'] if p else '-'} | {entry.get('verdict')} | {_cell(entry.get('by', ''))} | "
            f"{entry.get('reviewed_on', '')} | {_cell(entry.get('reason', ''))} | {action} |"
        )
    lines.append("")
    return "\n".join(lines)


def replay_seeds(root: Path) -> dict:
    """Classifier check: each literature seed whose tags map to a track should land on it."""
    records = read_json(root / "research" / "literature_records.json")
    checked = matched = 0
    misses = []
    for record in records:
        expected = {name for name, track in TRACKS.items() if track.seed_tags & set(record.get("tags", []))}
        if not expected:
            continue
        checked += 1
        found = set(classify(f"{record.get('title', '')}. {record.get('abstract', '')}"))
        if expected & found:
            matched += 1
        else:
            misses.append({"id": record["id"], "expected": sorted(expected), "found": sorted(found)})
    return {"checked": checked, "matched": matched, "misses": misses}


def _iso_date(text: str) -> str:
    """A YYYY-MM-DD date, compared as text with arXiv's `published` dates."""
    try:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
            return dt.date.fromisoformat(text).isoformat()
    except ValueError:
        pass
    raise argparse.ArgumentTypeError(f"expected a date such as 2026-09-18, not {text!r}")


def _positive(text: str) -> int:
    try:
        value = int(text)
    except ValueError:
        value = 0
    if value < 1:
        raise argparse.ArgumentTypeError(f"expected a whole number of at least 1, not {text!r}")
    return value


def _track_names(text: str) -> list[str]:
    """Comma-separated track names; spaces and empty names are ignored."""
    names = [name.strip() for name in text.split(",") if name.strip()]
    unknown = [name for name in names if name not in TRACKS]
    if not names or unknown:
        raise argparse.ArgumentTypeError(f"unknown track {', '.join(unknown) or text!r}; choose from {', '.join(TRACKS)}")
    return names


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--since", type=_iso_date, help=f"ISO date; default is {OVERLAP_DAYS} days before each track's last run.")
    parser.add_argument("--tracks", type=_track_names, help=f"Comma list from: {', '.join(TRACKS)}")
    parser.add_argument("--max", type=_positive, default=PAGE_SIZE, help="Results per page of a track query.")
    parser.add_argument("--max-pages", type=_positive, default=MAX_PAGES, help="Pages per track query before reporting a gap.")
    parser.add_argument("--replay-seeds", action="store_true")
    parser.add_argument("--relabel", action="store_true", help="Recompute labels for stored papers; no fetching.")
    parser.add_argument(
        "--verdict", nargs=2, metavar=("ARXIV_ID", "VERDICT"),
        help=f"Record a reviewed verdict ({', '.join(VERDICTS)}) and re-render the digest; no fetching.",
    )
    parser.add_argument(
        "--reason",
        help="With --verdict: why, in a sentence or two. Left out, a person's verdict re-recorded unchanged keeps its reason.",
    )
    parser.add_argument(
        "--action",
        help='With --verdict: what a named document should change. Left out, a person\'s re-recorded verdict keeps its earlier action; "" clears it.',
    )
    parser.add_argument("--by", default="human", help="With --verdict: who decided (default: human).")
    parser.add_argument(
        "--action-done", metavar="ARXIV_ID", help="Mark a recorded verdict's action as carried out and re-render the digest; no fetching."
    )
    args = parser.parse_args(argv)
    if args.verdict and args.action_done:
        parser.error("give --verdict or --action-done, not both")
    problem = checkout_error(args.root)  # a mistyped --root would otherwise get a fresh research/audits/
    if problem:
        print(f"error: {problem}", file=sys.stderr)
        return 2
    if not args.replay_seeds:
        try:  # an unreadable verdicts or collisions file stops every mode before it writes anything
            load_verdicts(args.root)
            _load_state(args.root)
        except (ValueError, OSError) as error:
            print(f"error: {error}", file=sys.stderr)
            return 2
    if args.verdict or args.action_done:
        notes: list[str] = []
        try:
            state = _load_state(args.root)
            if args.verdict:
                raw_id, verdict = args.verdict
                arxiv_id = normalize_id(raw_id)
                verdict_entry(verdict, "", args.by)  # an unknown verdict is reported before a missing reason
                previous = load_verdicts(args.root)["verdicts"].get(arxiv_id) or {}
                # Only a person's own earlier entry is carried over: a judge's reason and action
                # are one model's reading, not the person's.
                own = bool(previous) and not by_judge(previous)
                reason, action = args.reason, args.action
                if reason is None:
                    if own and previous.get("verdict") == verdict and previous.get("reason"):
                        reason = previous["reason"]
                        notes.append("kept the earlier reason (--reason replaces it)")
                    elif previous.get("reason"):
                        raise ValueError(
                            f"{arxiv_id} has a {previous.get('verdict')} verdict by {previous.get('by') or 'hand'} "
                            "with its own reason; give --reason for this one"
                        )
                    else:
                        reason = ""
                if action is None and previous.get("action"):
                    if own:
                        action = previous["action"]
                    else:
                        notes.append(f"did not keep the judge's action ({previous['action']}); give --action to adopt it")
                done = own and bool(previous.get("action_done")) and action == previous.get("action")
                if own and args.action is None and action:
                    notes.append(
                        f"kept the earlier action ({action}) and whether it was done ({'done' if done else 'not done'});"
                        ' --action "" clears it'
                    )
                set_verdict(args.root, arxiv_id, verdict, reason, args.by, action=action, action_done=done)
                outcome = verdict
            else:
                arxiv_id = normalize_id(args.action_done)
                mark_action_done(args.root, arxiv_id)
                outcome = "action marked done"
            attach_verdicts(state, load_verdicts(args.root)["verdicts"])
            _save(args.root, state)
        except (ValueError, OSError) as error:
            print(f"error: {error}", file=sys.stderr)
            return 2
        stored = "" if arxiv_id in state["papers"] else " (not in the collisions file yet)"
        print(f"{arxiv_id}: {outcome}{stored}; digest re-rendered")
        for note in notes:
            print(note)
        return 0
    if args.relabel:
        corpus = Corpus(args.root)
        corpus.refresh()
        print(f"{relabel(args.root, corpus)} papers changed label or tracks")
        return 0
    if args.replay_seeds:
        result = replay_seeds(args.root)
        print(json.dumps(result, indent=2))
        print(f"\n{result['matched']}/{result['checked']} seed papers land on a track their tags name.")
        return 0
    tracks = {name: TRACKS[name] for name in args.tracks} if args.tracks else TRACKS
    corpus = Corpus(args.root)
    corpus.refresh()
    report = run(args.root, Client(), corpus, since=args.since, tracks=tracks, page_size=args.max, max_pages=args.max_pages)
    print(f"fetched {report.fetched} papers in range, {report.new} new: {report.by_label}")
    print(f"{report.relabelled} stored possible kills or scoops are now cited and relabelled already-cited")
    for name, cut in report.truncated.items():
        print(
            f"warning: {name} hit the page cap ({cut['results']} results back to {cut['oldest_seen']}); "
            f"papers from {cut['since']} to {cut['oldest_seen']} may be missing",
            file=sys.stderr,
        )
    if not report.saved:
        print("No new papers; outputs unchanged.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
