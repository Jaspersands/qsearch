from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from tools.brief import build_brief as B

US = "\x1f"
SHA = "a" * 40


def _git(repo: Path, *args: str, env: dict | None = None) -> None:
    subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", *args],
        check=True,
        capture_output=True,
        env=env,
    )


def _commit(repo: Path, files: dict[str, object], date: str) -> None:
    """Write files (JSON-encoded unless already text) and commit them at noon UTC on `date`."""
    for rel, content in files.items():
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content if isinstance(content, str) else json.dumps(content), encoding="utf-8")
    env = {**os.environ, "GIT_AUTHOR_DATE": f"{date}T12:00:00Z", "GIT_COMMITTER_DATE": f"{date}T12:00:00Z"}
    _git(repo, "add", "-A", env=env)
    _git(repo, "commit", "-qm", date, env=env)


def _history_repo(tmp_path: Path) -> Path:
    """Registry [A] committed 2026-10-01, [A, B] on 2026-10-15; the working copy holds [B, C]."""
    repo = tmp_path / "git"
    repo.mkdir()
    _git(repo, "init", "-q")
    _commit(repo, {B.REGISTRY: [{"id": "A"}]}, "2026-10-01")
    _commit(repo, {B.REGISTRY: [{"id": "A"}, {"id": "B"}]}, "2026-10-15")
    (repo / B.REGISTRY).write_text(json.dumps([{"id": "B"}, {"id": "C"}]), encoding="utf-8")
    return repo


# ---------- Task 3.1: git runner and registry delta ----------


def test_registry_delta_lists_added_and_removed_ids_since_the_cutoff(tmp_path: Path) -> None:
    repo = _history_repo(tmp_path)
    since = B.since_commit(repo, since_days=7, today="2026-10-20")  # cutoff 2026-10-13
    assert since is not None and len(since[0]) == 40 and since[1] == "2026-10-01"
    delta = B.registry_delta(repo, since[0], since_date=since[1])
    assert delta["available"] is True
    assert delta["added"] == ["B", "C"] and delta["removed"] == ["A"]
    assert (delta["since_sha"], delta["since_date"]) == (since[0], "2026-10-01")
    assert (delta["baseline_count"], delta["current_count"]) == (1, 2)
    assert delta["quarantined"] == []

    # A removed record that moved to the quarantine file is named as quarantined, not lost.
    (repo / B.QUARANTINE).write_text(json.dumps([{"id": "A", "status": "QUARANTINED"}]), encoding="utf-8")
    assert B.registry_delta(repo, since[0])["quarantined"] == ["A"]
    (repo / B.QUARANTINE).write_text("[{not json", encoding="utf-8")
    assert B.registry_delta(repo, since[0])["quarantined"] is None

    # A shorter window starts from the 2026-10-15 commit instead.
    later = B.since_commit(repo, since_days=3, today="2026-10-20")  # cutoff 2026-10-17
    assert later is not None and later[1] == "2026-10-15"
    delta = B.registry_delta(repo, later[0], since_date=later[1])
    assert delta["added"] == ["C"] and delta["removed"] == ["A"]


def test_cutoff_is_the_start_of_the_utc_day_not_the_time_of_day(tmp_path: Path) -> None:
    # git reads a bare --before=2026-10-15 as 2026-10-15 at the current time of day, so a
    # commit at noon that day would count as "before" in the afternoon and not in the morning.
    repo = _history_repo(tmp_path)
    since = B.since_commit(repo, since_days=5, today="2026-10-20")  # cutoff 2026-10-15
    assert since is not None and since[1] == "2026-10-01"


def test_ids_reads_a_list_or_a_records_object() -> None:
    assert B._ids([{"id": "A"}, {"id": "B"}, {"no": "id"}, "junk"]) == {"A", "B"}
    assert B._ids({"records": [{"id": "X"}]}) == {"X"}
    with pytest.raises(ValueError):
        B._ids({"something": []})


def test_registry_delta_is_unavailable_outside_git(tmp_path: Path) -> None:
    root = tmp_path / "plain"
    (root / "research" / "registry").mkdir(parents=True)
    (root / B.REGISTRY).write_text(json.dumps([{"id": "A"}]), encoding="utf-8")
    assert B.since_commit(root, today="2026-10-20") is None
    delta = B.registry_delta(root, None)
    assert delta["available"] is False and "not a git checkout" in delta["reason"]
    assert "added" not in delta


def test_registry_delta_reports_a_missing_registry_at_the_cutoff(tmp_path: Path) -> None:
    repo = tmp_path / "git"
    repo.mkdir()
    _git(repo, "init", "-q")
    _commit(repo, {"README.md": "start\n"}, "2026-10-01")
    _commit(repo, {B.REGISTRY: [{"id": "A"}]}, "2026-10-15")
    since = B.since_commit(repo, since_days=7, today="2026-10-20")
    assert since is not None and since[1] == "2026-10-01"
    delta = B.registry_delta(repo, since[0], since_date=since[1])
    assert delta["available"] is False
    assert "did not exist" in delta["reason"] and since[0][:8] in delta["reason"]
    assert "added" not in delta


def test_registry_delta_says_when_no_commit_is_older_than_the_window(tmp_path: Path) -> None:
    repo = tmp_path / "git"
    repo.mkdir()
    _git(repo, "init", "-q")
    _commit(repo, {B.REGISTRY: [{"id": "A"}]}, "2026-10-18")
    assert B.since_commit(repo, since_days=7, today="2026-10-20") is None
    delta = B.registry_delta(repo, None)
    assert delta["available"] is False and "no commit before the cutoff" in delta["reason"]


def test_since_commit_is_unavailable_on_a_shallow_clone(tmp_path: Path) -> None:
    source = _history_repo(tmp_path)
    clone = tmp_path / "shallow"
    subprocess.run(["git", "clone", "-q", "--depth", "1", source.resolve().as_uri(), str(clone)], check=True,
                   capture_output=True)
    # The depth-1 clone holds only the 2026-10-15 commit; a cutoff after it would find that
    # commit and report a delta against it, which is right only by luck. Shallow is unavailable.
    assert B.since_commit(clone, since_days=3, today="2026-10-20") is None
    delta = B.registry_delta(clone, None)
    assert delta["available"] is False and "shallow" in delta["reason"]


def test_since_commit_is_unavailable_for_a_copy_inside_another_repository(tmp_path: Path) -> None:
    repo = _history_repo(tmp_path)
    nested = repo / "scratch" / "copy"
    (nested / "research" / "registry").mkdir(parents=True)
    (nested / B.REGISTRY).write_text(json.dumps([{"id": "Z"}]), encoding="utf-8")
    # The outer repository has a registry at the same relative path and history before the
    # cutoff; comparing the copy with it would report a plausible, wrong delta.
    assert B.since_commit(nested, since_days=7, today="2026-10-20") is None
    delta = B.registry_delta(nested, None)
    assert delta["available"] is False and "not the top of its git work tree" in delta["reason"]
    assert "scratch/copy" in delta["reason"]


def test_allowed_git_args_accepts_only_the_three_shapes() -> None:
    assert B.allowed_git_args(("log", "-1", "--before=2026-10-13T00:00:00Z", f"--format=%H{US}%ct")) is True
    assert B.allowed_git_args(("show", f"{SHA}:{B.REGISTRY}")) is True
    assert B.allowed_git_args(("rev-parse", "--is-shallow-repository", "--show-prefix")) is True


@pytest.mark.parametrize(
    "args",
    [
        ("log", "-1", "--before=2026-10-13", f"--format=%H{US}%ct"),
        ("log", "-1", "--before=2026-10-13T00:00:00Z", f"--format=%H{US}%ct", "--output=/tmp/x"),
        ("log", "--before=2026-10-13T00:00:00Z", f"--format=%H{US}%ct"),
        ("log", "-1", "--before=yesterday", f"--format=%H{US}%ct"),
        ("log", "-1", "--before=2026-10-13T00:00:00Z", "--format=%H %s"),
        ("log", "-1", f"--format=%H{US}%ct", "--before=2026-10-13T00:00:00Z"),
        ("show", f"HEAD:{B.REGISTRY}"),
        ("show", f"{SHA}:research/registry/dequantization_checks.json"),
        ("show", f"{SHA}:{B.REGISTRY}", "--output=/tmp/x"),
        ("show", f"--output=/tmp/x {SHA}:{B.REGISTRY}"),
        ("status", "--porcelain"),
        ("rev-parse", "HEAD"),
        ("rev-parse", "--is-shallow-repository"),
        ("rev-parse", "--show-prefix", "--is-shallow-repository"),
        (),
    ],
)
def test_git_runner_refuses_other_argument_shapes(tmp_path: Path, args: tuple[str, ...]) -> None:
    assert B.allowed_git_args(args) is False
    with pytest.raises(ValueError, match="read-only"):
        B.git_runner(tmp_path)(*args)


# ---------- Task 3.2: the other sections ----------

REPO = Path(__file__).resolve().parents[2]
SINCE = "2026-10-14"


def _write_json(path: Path, data) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def _paper(arxiv_id: str, title: str, label: str, first_seen: str | None) -> dict:
    record = {"arxiv_id": arxiv_id, "title": title, "label": label, "published": "2026-10-10", "url": "u"}
    if first_seen is not None:
        record["first_seen"] = first_seen
    return record


def _verdict(verdict: str, reviewed_on: str | None, action: str | None = None, by: str = "human", **extra) -> dict:
    return {"verdict": verdict, "reason": "r", "action": action, "by": by, "reviewed_on": reviewed_on, **extra}


def _arxiv_files(root: Path, papers: list[dict], verdicts: dict) -> None:
    _write_json(root / B.ARXIV_STATE, {"updated": "2026-10-19", "papers": {p["arxiv_id"]: p for p in papers}})
    _write_json(root / B.ARXIV_VERDICTS, {"verdicts": verdicts})


def test_arxiv_section_lists_open_flags_new_reviews_and_open_actions(tmp_path: Path) -> None:
    _arxiv_files(
        tmp_path,
        [
            _paper("2610.11111", "Open new kill", "possible-kill", "2026-10-18"),
            _paper("2610.22222", "Open old scoop", "possible-scoop", "2026-09-30"),
            _paper("2610.33333", "Reviewed new kill", "possible-kill", "2026-10-19"),
            _paper("2610.44444", "Reviewed old scoop", "possible-scoop", "2026-09-30"),
            _paper("2610.55555", "Related paper", "related", "2026-10-19"),
        ],
        {
            "2610.33333": _verdict("should-cite", "2026-10-20", action="Cite it in research/X.md."),
            "2610.44444": _verdict("false-alarm", "2026-10-01"),
            "2610.66666": _verdict("related-only", "2026-10-19", action="Done already.", by="judge:x", action_done=True),
        },
    )
    section = B.arxiv_section(tmp_path, SINCE)
    assert section["available"] is True
    assert [(f["id"], f["verdict"]) for f in section["flagged"]] == [
        ("2610.11111", None), ("2610.22222", None), ("2610.33333", "should-cite")]
    assert section["flagged"][0] == {
        "id": "2610.11111", "title": "Open new kill", "label": "possible-kill", "first_seen": "2026-10-18", "verdict": None}
    assert section["reviewed"] == [
        {"id": "2610.33333", "verdict": "should-cite", "by": "human", "reviewed_on": "2026-10-20"},
        {"id": "2610.66666", "verdict": "related-only", "by": "judge:x", "reviewed_on": "2026-10-19"},
    ]
    assert section["actions"] == [{"id": "2610.33333", "action": "Cite it in research/X.md.", "by": "human"}]


def test_arxiv_section_tolerates_verdicts_for_unknown_papers_and_null_first_seen(tmp_path: Path) -> None:
    _arxiv_files(
        tmp_path,
        [
            _paper("2610.77777", "Open, date unknown", "possible-kill", None),
            {**_paper("2610.88888", "Reviewed, date null", "possible-scoop", None), "first_seen": None},
        ],
        {
            "2610.88888": _verdict("false-alarm", None),
            "2610.99999": _verdict("should-cite", "2026-10-20", action="Cite the unknown paper."),
        },
    )
    section = B.arxiv_section(tmp_path, SINCE)
    assert [(f["id"], f["first_seen"]) for f in section["flagged"]] == [("2610.77777", None)]
    assert [r["id"] for r in section["reviewed"]] == ["2610.99999"]
    assert section["actions"] == [{"id": "2610.99999", "action": "Cite the unknown paper.", "by": "human"}]

    # Verdicts with no stored papers at all still give the reviews and actions.
    (tmp_path / B.ARXIV_STATE).unlink()
    section = B.arxiv_section(tmp_path, SINCE)
    assert section["available"] is True and section["flagged"] == []
    assert [a["id"] for a in section["actions"]] == ["2610.99999"]


def test_arxiv_section_missing(tmp_path: Path) -> None:
    section = B.arxiv_section(tmp_path, SINCE)
    assert section["available"] is False and "arxiv_collisions.json" in section["reason"]


def test_arxiv_constants_match_the_watch() -> None:
    from tools.arxiv_watch import verdicts, watch

    assert B.FLAGGED_LABELS == watch.FLAGGED
    assert B.ARXIV_VERDICTS == verdicts.VERDICTS_FILE
    assert (REPO / B.ARXIV_STATE) == watch._paths(REPO)[0]


def _reviewed_note(root: Path, overall: str = "unsound") -> None:
    note = root / "research" / "FIXTURE_NOTE.md"
    note.parent.mkdir(parents=True, exist_ok=True)
    note.write_text("# Fixture\n\n2026-10-18. REVIEW PENDING.\n\n## Result\n\nIt holds for all twelve saved inputs.\n",
                    encoding="utf-8")
    claim = {"quote": "It holds for all twelve saved inputs", "verified": True, "verdict": "wrong", "step": "Result",
             "finding": "Input 7 fails.", "covered_by_self_check": False}
    entry = {"reviewed_on": "2026-10-21", "judge": "j", "content_sha": hashlib.sha256(note.read_bytes()).hexdigest(),
             "overall": overall, "claims": [claim], "summary": "s", "stale": False}
    _write_json(root / "research/audits/reviews/reviews.json", {"notes": {"FIXTURE_NOTE": entry}})


def test_referee_section_reports_flagged_reviews(tmp_path: Path) -> None:
    _reviewed_note(tmp_path)
    section = B.referee_section(tmp_path)
    assert section["available"] is True and section["reviewed"] == 1 and section["stale"] == []
    assert [f["stem"] for f in section["flagged"]] == ["FIXTURE_NOTE"]
    assert section["flagged"][0]["worst_claim"]["finding"] == "Input 7 fails."


def test_referee_section_missing(tmp_path: Path, monkeypatch) -> None:
    section = B.referee_section(tmp_path)
    assert section["available"] is False and "no reviews yet" in section["reason"]
    monkeypatch.setitem(sys.modules, "tools.referee.referee", None)
    section = B.referee_section(tmp_path)
    assert section["available"] is False and section["reason"] == "tools/referee not present"


def test_preflight_section_groups_problems_by_check(fake_repo: Path) -> None:
    (fake_repo / "research" / "hypotheses" / "broken.json").write_text('{"bad": "\\x"}', encoding="utf-8")
    section = B.preflight_section(fake_repo)
    assert section["available"] is True
    # The fake checkout is not a git repository and has no CLI manifest.
    assert set(section["by_check"]) == {"json", "imports", "manifest"} and section["total"] == 3
    [problem] = section["by_check"]["json"]
    assert problem["path"] == "research/hypotheses/broken.json" and problem["message"].startswith("Invalid \\escape")
    assert section["by_check"]["imports"] == [{"path": ".", "message": "git unavailable"}]


def test_preflight_section_missing(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setitem(sys.modules, "tools.preflight.preflight", None)
    section = B.preflight_section(tmp_path)
    assert section["available"] is False and section["reason"] == "tools/preflight not present"


COCKPIT = {
    "generated_on": "2026-10-19",
    "inertia": {
        "available": True,
        "threshold": 8,
        "directions": [],
        "flags": [
            {"direction": "opi", "label": "OPI / prime character", "streak": 13, "flag": True, "last_gain": None},
            {"direction": "dcp", "label": "DCP / dihedral coset", "streak": 32, "flag": True,
             "last_gain": {"date": "2026-10-12", "records": 3, "ids": ["NEG-X"]}},
        ],
        "runs": [],
    },
    "warnings": ["Git history is shallow."],
}


def test_inertia_section_reads_the_cockpit_flags(tmp_path: Path) -> None:
    _write_json(tmp_path / B.COCKPIT, COCKPIT)
    section = B.inertia_section(tmp_path)
    assert section["available"] is True
    assert (section["generated_on"], section["threshold"]) == ("2026-10-19", 8)
    assert section["warnings"] == ["Git history is shallow."]
    assert section["flags"] == [
        {"direction": "opi", "label": "OPI / prime character", "streak": 13, "last_gain": None},
        {"direction": "dcp", "label": "DCP / dihedral coset", "streak": 32, "last_gain": "2026-10-12"},
    ]


def test_inertia_section_missing(tmp_path: Path) -> None:
    section = B.inertia_section(tmp_path)
    assert section["available"] is False and "build_cockpit.py" in section["reason"]
    _write_json(tmp_path / B.COCKPIT, {**COCKPIT, "inertia": {"available": False, "flags": []}, "warnings": ["no git"]})
    section = B.inertia_section(tmp_path)
    assert section["available"] is False and "no git" in section["reason"]


def test_duplicates_section_keeps_pairs_that_involve_a_new_record(tmp_path: Path, monkeypatch) -> None:
    from tools.corpus.duplicates import Pair

    pairs = [
        Pair("negative:NEG-NEW-1", "negative:NEG-OLD-1", 0.97, "new one", "old one"),
        Pair("negative:NEG-OLD-2", "quarantined:NEG-NEW-2", 0.91, "old two", "new two"),
        Pair("negative:NEG-OLD-3", "negative:NEG-OLD-4", 0.99, "old three", "old four"),
    ]
    seen = {}

    def fake(corpus, **kwargs):
        seen.update(kwargs, corpus=corpus)
        return pairs

    monkeypatch.setattr(B, "_near_duplicates", fake)
    marker = object()
    section = B.duplicates_section(tmp_path, ["NEG-NEW-1", "NEG-NEW-2"], corpus=marker)
    assert section["available"] is True and section["checked"] == 2
    assert [(p["a"], p["b"], p["new"]) for p in section["pairs"]] == [
        ("negative:NEG-NEW-1", "negative:NEG-OLD-1", ["NEG-NEW-1"]),
        ("negative:NEG-OLD-2", "quarantined:NEG-NEW-2", ["NEG-NEW-2"]),
    ]
    assert seen["corpus"] is marker and seen["kind"] == "negative" and seen["threshold"] == B.DUPLICATE_THRESHOLD


def test_duplicates_section_finds_a_planted_restatement_with_the_real_corpus(fake_repo: Path) -> None:
    from tests.tools.conftest import NEGATIVES
    from tests.tools.test_corpus_duplicates import DUP_A, DUP_B

    _write_json(fake_repo / B.REGISTRY, NEGATIVES + [DUP_A, DUP_B])
    section = B.duplicates_section(fake_repo, ["NEG-DUP-B"])
    assert [(p["a"], p["b"]) for p in section["pairs"]] == [("negative:NEG-DUP-A", "negative:NEG-DUP-B")]
    assert section["pairs"][0]["score"] >= B.DUPLICATE_THRESHOLD


def test_duplicates_section_missing(tmp_path: Path, monkeypatch) -> None:
    section = B.duplicates_section(tmp_path, None)
    assert section["available"] is False and "registry" in section["reason"]

    def no_corpus(root):
        raise AssertionError("no corpus should be opened when nothing was added")

    monkeypatch.setattr(B, "_open_corpus", no_corpus)
    section = B.duplicates_section(tmp_path, [])
    assert section == {"available": True, "checked": 0, "threshold": B.DUPLICATE_THRESHOLD, "pairs": []}


def test_commands_section_names_five_commands_that_exist() -> None:
    section = B.commands_section()
    assert section["available"] is True
    assert [c["name"] for c in section["commands"]] == ["oracle", "screener", "baselines", "preflight", "duplicates"]
    for command in section["commands"]:
        script = command["command"].split()[1]
        assert command["command"].startswith("python ") and (REPO / script).is_file(), command
        assert command["when"]


def test_section_turns_an_exception_into_unavailable() -> None:
    def broken(key):
        raise KeyError(key)

    assert B._section("broken", broken, "inertia") == {"available": False, "reason": "KeyError: 'inertia'"}
    assert B._section("odd", lambda: ["not", "a", "dict"])["available"] is False
    assert B._section("fine", lambda: {"available": True}) == {"available": True}


# ---------- Task 3.3: build, render, main ----------

SECTIONS = ("registry", "arxiv", "referee", "preflight", "inertia", "duplicates", "commands")
HEADINGS = ("## Registry", "## arXiv watch", "## Referee", "## Preflight", "## Inertia", "## Possible duplicates",
            "## Commands")


def test_build_never_fails_when_every_source_is_missing(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "empty"
    root.mkdir()
    for module in ("tools.preflight.preflight", "tools.referee.referee", "tools.arxiv_watch.verdicts"):
        monkeypatch.setitem(sys.modules, module, None)
    brief = B.build(root, today="2026-10-21")
    assert set(brief) == {"generated_on", "since_days", *SECTIONS}
    assert (brief["generated_on"], brief["since_days"]) == ("2026-10-21", 7)
    for name in SECTIONS[:-1]:
        assert brief[name]["available"] is False and brief[name]["reason"], name
    assert brief["commands"]["available"] is True
    json.dumps(brief)  # JSON-ready
    text = B.render(brief)
    assert text.count("Not available: ") == 6

    def boom(*args):
        raise RuntimeError("git exploded")

    brief = B.build(root, today="2026-10-21", git=boom)
    assert brief["registry"] == {"available": False, "reason": "RuntimeError: git exploded"}
    assert brief["duplicates"]["available"] is False


def _full_repo(tmp_path: Path, monkeypatch) -> Path:
    repo = _history_repo(tmp_path)
    _arxiv_files(
        repo,
        [_paper("2610.11111", "Open new kill", "possible-kill", "2026-10-18")],
        {"2610.33333": _verdict("should-cite", "2026-10-19", action="Cite it in research/X.md and run the LP decoder.")},
    )
    _reviewed_note(repo)
    from tools.corpus.duplicates import Pair

    monkeypatch.setattr(B, "_open_corpus", lambda root: "corpus")
    monkeypatch.setattr(B, "_near_duplicates", lambda corpus, **kw: [
        Pair("negative:A", "negative:C", 0.93, "the old claim", "the new claim")])
    return repo


def test_render_contains_every_section_heading_and_action_strings(tmp_path: Path, monkeypatch) -> None:
    repo = _full_repo(tmp_path, monkeypatch)
    brief = B.build(repo, today="2026-10-20")
    assert brief["registry"]["added"] == ["B", "C"]
    assert brief["duplicates"]["pairs"][0]["new"] == ["C"]
    assert brief["inertia"]["available"] is False  # no cockpit in this checkout
    text = B.render(brief)
    positions = [text.index(heading) for heading in HEADINGS]
    assert positions == sorted(positions)
    for needle in (
        "since 2026-10-13",
        "Cite it in research/X.md and run the LP decoder.",  # the open action, verbatim
        "2610.11111",  # the open flag
        "FIXTURE_NOTE", "Input 7 fails.",  # the referee's flagged note and its worst claim
        "the old claim", "0.93",  # the possible duplicate
        f"Not available: {brief['inertia']['reason']}",
        "python tools/preflight/preflight.py",
    ):
        assert needle in text, needle


def test_main_writes_both_files(tmp_path: Path, capsys) -> None:
    root = tmp_path / "empty"
    root.mkdir()
    out = tmp_path / "out"
    assert B.main(["--root", str(root), "--out", str(out)]) == 0
    printed = capsys.readouterr().out
    md, js = out / "AGENT_BRIEF.md", out / "agent_brief.json"
    assert str(md) in printed and str(js) in printed
    assert md.read_text(encoding="utf-8").startswith("# Agent brief")
    assert json.loads(js.read_text(encoding="utf-8"))["since_days"] == 7

    assert B.main(["--root", str(root), "--since-days", "3", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["since_days"] == 3 and set(SECTIONS) <= set(payload)
    assert (root / B.OUTPUT_MD).is_file() and (root / B.OUTPUT_JSON).is_file()

    with pytest.raises(SystemExit):
        B.main(["--root", str(root), "--since-days", "0"])
