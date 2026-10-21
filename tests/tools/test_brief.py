from __future__ import annotations

import json
import os
import subprocess
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


def test_allowed_git_args_accepts_only_the_three_shapes() -> None:
    assert B.allowed_git_args(("log", "-1", "--before=2026-10-13T00:00:00Z", f"--format=%H{US}%ct")) is True
    assert B.allowed_git_args(("show", f"{SHA}:{B.REGISTRY}")) is True
    assert B.allowed_git_args(("rev-parse", "--is-shallow-repository")) is True


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
        (),
    ],
)
def test_git_runner_refuses_other_argument_shapes(tmp_path: Path, args: tuple[str, ...]) -> None:
    assert B.allowed_git_args(args) is False
    with pytest.raises(ValueError, match="read-only"):
        B.git_runner(tmp_path)(*args)
