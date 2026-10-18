"""Watch arXiv for papers that could kill, support or scoop a Q-Search track.

    python tools/arxiv_watch/watch.py                  # since the last run (default 14 days)
    python tools/arxiv_watch/watch.py --since 2026-09-01 --tracks dcp,dqi_opi
    python tools/arxiv_watch/watch.py --replay-seeds   # check the track classifier on seed papers

Each new paper is placed on tracks, matched against the corpus index (nearest negatives,
notes, theorem modules) and given a triage label from wording cues:
possible-kill, possible-scoop, related, already-cited or unrelated. Labels are for
triage only; read the paper before acting on one.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.arxiv_watch.tracks import TRACKS, Track, classify  # noqa: E402
from tools.corpus.api import Corpus  # noqa: E402
from tools.corpus.docs import read_json  # noqa: E402
from tools.corpus.sources.arxiv import Client, Paper  # noqa: E402

KILL_CUES = (
    r"dequantiz",
    r"classical (algorithm|simulation|simulat|procedure|method)s? (that )?(match|solve|achiev|run|simulat|for)",
    r"efficient(ly)? classical",
    r"classically simulat",
    r"\bno[- ]go\b",
    r"lower bound",
    r"impossib",
    r"\bbarrier",
    r"refut",
    r"does not (solve|yield|give|provide)",
    r"limitation",
)
SCOOP_CUES = (
    r"exponential (quantum )?speed[- ]?up",
    r"super-?polynomial (quantum )?speed[- ]?up",
    r"polynomial[- ]time quantum algorithm",
    r"(efficient|new|first) quantum algorithm",
    r"quantum advantage",
    r"subexponential[- ]time quantum algorithm",
)
NEAREST_KINDS = ("negative", "dequant", "note", "hypothesis", "theorem")
LABEL_ORDER = ("possible-kill", "possible-scoop", "related", "already-cited", "unrelated")


@dataclass
class RunReport:
    fetched: int = 0
    new: int = 0
    by_label: dict | None = None


def _cues(patterns: tuple[str, ...], text: str) -> list[str]:
    return [m.group(0) for p in patterns for m in [re.search(p, text, re.I)] if m]


def label_for(paper: Paper, tracks: list[str], cited: bool) -> tuple[str, list[str]]:
    """Kill and scoop labels need a core track and a quantum paper; everything else is related."""
    text = f"{paper.title}. {paper.abstract}"
    kill, scoop = _cues(KILL_CUES, text), _cues(SCOOP_CUES, text)
    if cited:
        return "already-cited", kill + scoop
    if not tracks:
        return "unrelated", kill + scoop
    core = any(TRACKS[name].core for name in tracks if name in TRACKS)
    quantum = re.search(r"quantum", text, re.I) is not None
    if core and quantum and kill:
        return "possible-kill", kill + scoop
    if core and quantum and scoop:
        return "possible-scoop", scoop
    return "related", kill + scoop


def relabel(root: Path, corpus: Corpus) -> int:
    """Recompute tracks and labels for every stored paper after a rule change; returns how many changed."""
    state = _load_state(root)
    changed = 0
    for arxiv_id, record in state["papers"].items():
        paper = Paper(
            arxiv_id, record.get("version", ""), record["title"], record.get("abstract", ""), record.get("authors", []),
            record["published"], record.get("updated", ""), record.get("categories", []), record["url"],
        )
        tracks = classify(f"{paper.title}. {paper.abstract}")
        label, cues = label_for(paper, tracks, cited=bool(corpus.mentions(arxiv_id)))
        if (label, tracks) != (record.get("label"), record.get("tracks")):
            changed += 1
        record.update({"label": label, "cues": cues, "tracks": tracks})
    _save(root, state)
    return changed


def _save(root: Path, state: dict) -> None:
    path, digest = _paths(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest.write_text(render_digest(state), encoding="utf-8")


def _paths(root: Path) -> tuple[Path, Path]:
    audits = root / "research" / "audits"
    return audits / "arxiv_collisions.json", audits / "ARXIV_WATCH.md"


def _load_state(root: Path) -> dict:
    path, _ = _paths(root)
    if path.exists():
        return read_json(path)
    return {"updated": None, "papers": {}}


def run(
    root: Path,
    client,
    corpus: Corpus,
    since: str | None = None,
    tracks: dict[str, Track] | None = None,
    max_results: int = 50,
    today: str | None = None,
) -> RunReport:
    tracks = tracks or TRACKS
    today = today or dt.date.today().isoformat()
    state = _load_state(root)
    if since is None:
        last = state.get("updated")
        since = (dt.date.fromisoformat(last) - dt.timedelta(days=1)).isoformat() if last else (
            dt.date.fromisoformat(today) - dt.timedelta(days=14)
        ).isoformat()

    fetched: dict[str, tuple[Paper, set[str]]] = {}
    for name, track in tracks.items():
        for paper in client.search(track.arxiv_query(), max_results=max_results):
            if paper.published < since:
                continue
            entry = fetched.setdefault(paper.arxiv_id, (paper, set()))
            entry[1].add(name)

    report = RunReport(fetched=len(fetched), by_label={})
    for arxiv_id, (paper, queried) in sorted(fetched.items()):
        if arxiv_id in state["papers"]:
            known = state["papers"][arxiv_id]
            known["queried_by"] = sorted(set(known.get("queried_by", [])) | queried)
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
        report.new += 1
        report.by_label[label] = report.by_label.get(label, 0) + 1

    state["updated"] = today
    _save(root, state)
    return report


def render_digest(state: dict, per_section: int = 40) -> str:
    papers = sorted(state["papers"].values(), key=lambda p: (p["published"], p["arxiv_id"]), reverse=True)
    counts = {label: sum(p["label"] == label for p in papers) for label in LABEL_ORDER}
    lines = [
        "# arXiv Collision Watch",
        "",
        f"Last run {state.get('updated')}. Generated by `tools/arxiv_watch/watch.py`; do not edit by hand.",
        "Labels come from wording cues and are for triage only. Read a paper before acting on its label.",
        "",
        "| Label | Papers |",
        "|---|---|",
        *[f"| {label} | {counts[label]} |" for label in LABEL_ORDER],
        "",
    ]
    titles = {"possible-kill": "Possible kills", "possible-scoop": "Possible scoops", "related": "Related"}
    for label, heading in titles.items():
        section = [p for p in papers if p["label"] == label][:per_section]
        lines += [f"## {heading}", ""]
        if not section:
            lines += ["None yet.", ""]
            continue
        lines += ["| Date | Paper | Tracks | Cues | Nearest Q-Search record |", "|---|---|---|---|---|"]
        for p in section:
            nearest = p["nearest"][0] if p["nearest"] else None
            near = f"`{nearest['doc_id']}` ({nearest['location']})" if nearest else ""
            title = p["title"].replace("|", "/")
            cues = ", ".join(p.get("cues", [])[:3]).replace("|", "/")
            lines.append(
                f"| {p['published']} | [{p['arxiv_id']}]({p['url']}) {title} | {', '.join(p['tracks'])} | {cues} | {near} |"
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--since", help="ISO date; default is the day before the last run, or 14 days ago.")
    parser.add_argument("--tracks", help=f"Comma list from: {', '.join(TRACKS)}")
    parser.add_argument("--max", type=int, default=50, help="Results per track query.")
    parser.add_argument("--replay-seeds", action="store_true")
    parser.add_argument("--relabel", action="store_true", help="Recompute labels for stored papers; no fetching.")
    args = parser.parse_args(argv)
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
    tracks = {name: TRACKS[name] for name in args.tracks.split(",")} if args.tracks else TRACKS
    corpus = Corpus(args.root)
    corpus.refresh()
    report = run(args.root, Client(), corpus, since=args.since, tracks=tracks, max_results=args.max)
    print(f"fetched {report.fetched} papers in range, {report.new} new: {report.by_label}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
