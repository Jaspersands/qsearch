from __future__ import annotations

import datetime as dt
import hashlib
import inspect
import json
import os
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path

import pytest

from tools.brief import build_brief as B

US = "\x1f"
SHA = "a" * 40
# POSIX TZ strings: no time-zone database needed. Sydney is UTC+10, UTC+11 from 2026-10-04.
SYDNEY = "AEST-10AEDT,M10.1.0,M4.1.0/3"
LOS_ANGELES = "PST8PDT,M3.2.0,M11.1.0"


@contextmanager
def _zone(tz: str):
    """Run with the process's local time zone set to tz; restore it after."""
    saved = os.environ.get("TZ")
    os.environ["TZ"] = tz
    time.tzset()
    try:
        yield
    finally:
        if saved is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = saved
        time.tzset()


@pytest.fixture(autouse=True)
def _utc_clock():
    # The window is local time (the clock the arXiv watch, the verdicts and the referee stamp
    # their dates with); every test runs in UTC unless it sets another zone.
    with _zone("UTC0"):
        yield


def _git(repo: Path, *args: str, env: dict | None = None) -> None:
    subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", *args],
        check=True,
        capture_output=True,
        env=env,
    )


def _dated(date: str, time: str = "12:00:00") -> dict:
    return {**os.environ, "GIT_AUTHOR_DATE": f"{date}T{time}Z", "GIT_COMMITTER_DATE": f"{date}T{time}Z"}


def _commit(repo: Path, files: dict[str, object | None], date: str, time: str = "12:00:00") -> None:
    """Write files (JSON-encoded unless already text; None deletes) and commit them at `time` UTC on `date`."""
    for rel, content in files.items():
        path = repo / rel
        if content is None:
            path.unlink()
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content if isinstance(content, str) else json.dumps(content), encoding="utf-8")
    env = _dated(date, time)
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
    # Something that is there but is no regular file cannot be read either; it is not "absent".
    (repo / B.QUARANTINE).unlink()
    (repo / B.QUARANTINE).mkdir()
    assert B.registry_delta(repo, since[0])["quarantined"] is None
    (repo / B.QUARANTINE).rmdir()
    (repo / B.QUARANTINE).symlink_to(repo / "nowhere.json")
    assert B.registry_delta(repo, since[0])["quarantined"] is None
    (repo / B.QUARANTINE).unlink()
    assert B.registry_delta(repo, since[0])["quarantined"] == []

    # A shorter window starts from the 2026-10-15 commit instead.
    later = B.since_commit(repo, since_days=3, today="2026-10-20")  # cutoff 2026-10-17
    assert later is not None and later[1] == "2026-10-15"
    delta = B.registry_delta(repo, later[0], since_date=later[1])
    assert delta["added"] == ["C"] and delta["removed"] == ["A"]


def test_registry_delta_rereads_a_file_caught_mid_write(tmp_path: Path, monkeypatch) -> None:
    # The agents rewrite the registry often; a read that lands mid-write sees half the file.
    repo = _history_repo(tmp_path)
    since = B.since_commit(repo, since_days=7, today="2026-10-20")
    (repo / B.QUARANTINE).write_text(json.dumps([{"id": "A"}]), encoding="utf-8")
    torn = {repo / B.REGISTRY, repo / B.QUARANTINE}
    real_text, real_bytes = Path.read_text, Path.read_bytes

    def torn_now(path: Path) -> bool:
        if path in torn:
            torn.discard(path)
            return True
        return False

    def read_text(self, *args, **kwargs):
        text = real_text(self, *args, **kwargs)
        return text[: len(text) // 2] if torn_now(self) else text

    def read_bytes(self):
        data = real_bytes(self)
        return data[: len(data) // 2] if torn_now(self) else data

    monkeypatch.setattr(Path, "read_text", read_text)
    monkeypatch.setattr(Path, "read_bytes", read_bytes)
    delta = B.registry_delta(repo, since[0], since_date=since[1])
    assert not torn  # each file was read half-written once
    assert delta["available"] is True and delta["added"] == ["B", "C"] and delta["quarantined"] == ["A"]


def test_cutoff_is_the_start_of_the_day_not_the_time_of_day(tmp_path: Path) -> None:
    # git reads a bare --before=2026-10-15 as 2026-10-15 at the current time of day, so a
    # commit at noon that day would count as "before" in the afternoon and not in the morning.
    repo = _history_repo(tmp_path)
    since = B.since_commit(repo, since_days=5, today="2026-10-20")  # cutoff 2026-10-15
    assert since is not None and since[1] == "2026-10-01"
    evening = dt.datetime(2026, 10, 20, 23, 59, tzinfo=dt.timezone.utc)  # a datetime counts as its day
    assert B.since_commit(repo, since_days=5, today=evening) == since


def test_baseline_ignores_a_side_branch_commit_that_left_the_registry_alone(tmp_path: Path) -> None:
    # The repository's own workflow: a tool branch that never touches the registry is merged
    # into main with --no-ff. Its last commit (10-12) is newer than the registry's last change
    # on main (10-05), but its registry is the older [A]; B was filed before the window.
    repo = tmp_path / "git"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _commit(repo, {B.REGISTRY: [{"id": "A"}]}, "2026-10-01")
    _git(repo, "branch", "side")
    _commit(repo, {B.REGISTRY: [{"id": "A"}, {"id": "B"}]}, "2026-10-05")
    _git(repo, "checkout", "-q", "side")
    _commit(repo, {"tools/x.txt": "tool work\n"}, "2026-10-12")
    _git(repo, "checkout", "-q", "main")
    _git(repo, "merge", "--no-ff", "-qm", "merge side", "side", env=_dated("2026-10-15"))
    since = B.since_commit(repo, since_days=7, today="2026-10-20")  # cutoff 2026-10-13
    assert since is not None and since[1] == "2026-10-05"
    delta = B.registry_delta(repo, since[0], since_date=since[1])
    assert (delta["added"], delta["removed"]) == ([], [])


def _merge(repo: Path, branch: str, date: str, registry: list | None = None) -> None:
    """Merge `branch` into the checked-out branch with --no-ff on `date`; `registry` resolves a conflict."""
    env = _dated(date)
    subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", "merge", "--no-ff",
                    "--no-commit", branch], capture_output=True, env=env)
    if registry is not None:
        (repo / B.REGISTRY).write_text(json.dumps(registry), encoding="utf-8")
        _git(repo, "add", B.REGISTRY, env=env)
    _git(repo, "commit", "-qm", f"merge {branch}", env=env)


def _merge_delta(repo: Path, today: str = "2026-10-20") -> dict:
    since = B.since_commit(repo, since_days=7, today=today)  # cutoff 2026-10-13
    assert since is not None
    return B.registry_delta(repo, since[0], since_date=since[1])


def _forked_repo(tmp_path: Path) -> Path:
    """main holds [A] from 2026-10-01; the branch `side` starts there."""
    repo = tmp_path / "git"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _commit(repo, {B.REGISTRY: [{"id": "A"}]}, "2026-10-01")
    _git(repo, "branch", "side")
    return repo


def test_a_record_merged_in_from_a_side_branch_in_the_window_counts_as_added(tmp_path: Path) -> None:
    # B was filed on a side branch before the window and reached main in it: the agents on main
    # first saw it in the window. The baseline is main's own registry at the cutoff, [A].
    repo = _forked_repo(tmp_path)
    _git(repo, "checkout", "-q", "side")
    _commit(repo, {B.REGISTRY: [{"id": "A"}, {"id": "B"}]}, "2026-10-12")
    _git(repo, "checkout", "-q", "main")
    _merge(repo, "side", "2026-10-16")
    delta = _merge_delta(repo)
    assert delta["since_date"] == "2026-10-01"
    assert (delta["added"], delta["removed"]) == (["B"], [])


def test_a_merge_of_two_changed_registries_compares_with_the_checked_out_branch(tmp_path: Path) -> None:
    # main filed X (2026-10-10) and the side branch Y (2026-10-12), both before the window; the
    # merge in the window keeps both. Only Y is new on main; X was there at the cutoff.
    repo = _forked_repo(tmp_path)
    _commit(repo, {B.REGISTRY: [{"id": "A"}, {"id": "X"}]}, "2026-10-10")
    _git(repo, "checkout", "-q", "side")
    _commit(repo, {B.REGISTRY: [{"id": "A"}, {"id": "Y"}]}, "2026-10-12")
    _git(repo, "checkout", "-q", "main")
    _merge(repo, "side", "2026-10-16", registry=[{"id": "A"}, {"id": "X"}, {"id": "Y"}])
    delta = _merge_delta(repo)
    assert delta["since_date"] == "2026-10-10"
    assert (delta["added"], delta["removed"]) == (["Y"], [])


def test_an_older_main_change_is_not_reported_because_a_newer_side_change_was_merged(tmp_path: Path) -> None:
    repo = _forked_repo(tmp_path)
    _commit(repo, {B.REGISTRY: [{"id": "A"}, {"id": "B"}]}, "2026-10-05")
    _git(repo, "checkout", "-q", "side")
    _commit(repo, {B.REGISTRY: [{"id": "A"}, {"id": "S"}]}, "2026-10-10")
    _git(repo, "checkout", "-q", "main")
    _merge(repo, "side", "2026-10-20", registry=[{"id": "A"}, {"id": "B"}, {"id": "S"}])
    delta = _merge_delta(repo)
    assert delta["since_date"] == "2026-10-05"
    assert (delta["added"], delta["removed"]) == (["S"], [])


def test_a_commit_at_midnight_on_the_cutoff_day_is_inside_the_window(tmp_path: Path) -> None:
    # git's --before keeps a commit dated exactly at the limit; the window starts at 00:00 (UTC here).
    repo = tmp_path / "git"
    repo.mkdir()
    _git(repo, "init", "-q")
    _commit(repo, {B.REGISTRY: [{"id": "A"}]}, "2026-10-12", "23:59:59")
    _commit(repo, {B.REGISTRY: [{"id": "A"}, {"id": "B"}]}, "2026-10-13", "00:00:00")
    since = B.since_commit(repo, since_days=7, today="2026-10-20")  # cutoff 2026-10-13
    assert since is not None and since[1] == "2026-10-12"
    assert B.registry_delta(repo, since[0], since_date=since[1])["added"] == ["B"]


def test_a_datetime_counts_as_its_local_day() -> None:
    morning = dt.datetime(2026, 10, 20, 22, 0, tzinfo=dt.timezone.utc)  # 09:00 on 2026-10-21 in Sydney
    assert B._day(morning) == dt.date(2026, 10, 20)  # in UTC
    with _zone(SYDNEY):
        assert B._day(morning) == dt.date(2026, 10, 21)
        assert B.cutoff_day(7, morning) == dt.date(2026, 10, 14)
        assert B._day(dt.datetime(2026, 10, 20, 23, 30)) == dt.date(2026, 10, 20)  # naive: taken as local
    with _zone(LOS_ANGELES):
        assert B._day(morning) == dt.date(2026, 10, 20)


@pytest.mark.parametrize("tz", ["<+14>-14", "<-12>12"])  # 26 hours apart: one is never on UTC's date
def test_the_brief_dates_by_the_clock_the_sources_stamp_with(tmp_path: Path, tz: str) -> None:
    # The arXiv watch, the verdicts store and the referee stamp dt.date.today(): local time. A
    # brief dated by UTC printed "Generated 2026-10-21" above reviews dated 2026-10-22.
    from tools.arxiv_watch import verdicts

    with _zone(tz):
        stamped = verdicts.verdict_entry("kill", "r", "human")["reviewed_on"]
        assert B._day(None).isoformat() == stamped == dt.date.today().isoformat()
        brief = B.build(tmp_path, today=None)
        assert brief["generated_on"] == dt.date.today().isoformat()


def _boundary_repo(tmp_path: Path, last_before: str, first_in: str) -> Path:
    """Registry [A] at 2026-10-01; [A, B] at `last_before` and [A, B, C] at `first_in` (UTC times on 2026-10-12/13)."""
    repo = tmp_path / "git"
    repo.mkdir()
    _git(repo, "init", "-q")
    _commit(repo, {B.REGISTRY: [{"id": "A"}]}, "2026-10-01")
    _commit(repo, {B.REGISTRY: [{"id": "A"}, {"id": "B"}]}, *last_before.split("T"))
    _commit(repo, {B.REGISTRY: [{"id": "A"}, {"id": "B"}, {"id": "C"}]}, *first_in.split("T"))
    return repo


@pytest.mark.parametrize("tz, last_before, first_in, limit", [
    # 00:00 AEDT on 2026-10-13 is 13:00 UTC on 2026-10-12.
    (SYDNEY, "2026-10-12T12:59:59", "2026-10-12T13:00:00", "2026-10-12T12:59:59Z"),
    # 00:00 PDT on 2026-10-13 is 07:00 UTC that day.
    (LOS_ANGELES, "2026-10-13T06:59:59", "2026-10-13T07:00:00", "2026-10-13T06:59:59Z"),
])
def test_the_window_starts_at_local_midnight(tmp_path: Path, tz: str, last_before: str, first_in: str,
                                             limit: str) -> None:
    repo = _boundary_repo(tmp_path, last_before, first_in)
    with _zone(tz):
        assert B._log_args(dt.date(2026, 10, 13))[3] == f"--before={limit}"
        assert B.allowed_git_args(B._log_args(dt.date(2026, 10, 13)))
        since = B.since_commit(repo, since_days=7, today="2026-10-20")  # cutoff 2026-10-13
        # The baseline is dated by the local calendar too: the day before the cutoff, never on it.
        assert since is not None and since[1] == "2026-10-12"
        delta = B.registry_delta(repo, since[0], since_date=since[1])
        assert (delta["added"], delta["removed"]) == (["C"], [])
        brief = B.build(repo, today="2026-10-20")
        assert brief["window_start"] == B.window_start(dt.date(2026, 10, 13)).isoformat()
        text = B.render(brief)
    offset = "+11:00" if tz == SYDNEY else "-07:00"
    assert brief["window_start"] == f"2026-10-13T00:00:00{offset}"
    assert f"since 2026-10-13 (00:00 local time, UTC{offset})" in text


def test_the_window_start_takes_the_offset_of_its_own_day() -> None:
    with _zone(SYDNEY):  # daylight saving began on 2026-10-04
        assert B.window_start(dt.date(2026, 10, 1)).isoformat() == "2026-10-01T00:00:00+10:00"
        assert B._log_args(dt.date(2026, 10, 1))[3] == "--before=2026-09-30T13:59:59Z"
        assert B.window_start(dt.date(2026, 10, 13)).isoformat() == "2026-10-13T00:00:00+11:00"


def test_the_arxiv_window_and_the_generated_date_use_the_local_calendar(tmp_path: Path) -> None:
    # 08:00 in Sydney on 2026-10-21 is 21:00 UTC on 2026-10-20: the sources stamp 2026-10-21.
    now = dt.datetime(2026, 10, 20, 21, 0, tzinfo=dt.timezone.utc)
    _arxiv_files(tmp_path, [], {"2610.11111": _verdict("kill", "2026-10-21"),
                                "2610.22222": _verdict("scoop", "2026-10-14"),
                                "2610.33333": _verdict("false-alarm", "2026-10-13")})
    with _zone(SYDNEY):
        brief = B.build(tmp_path, today=now)
    assert brief["generated_on"] == "2026-10-21"
    assert [r["id"] for r in brief["arxiv"]["reviewed"]] == ["2610.11111", "2610.22222"]


@pytest.mark.parametrize("days", [0, -3, 3651, 1_000_000, 7.5, "7", True])
def test_build_refuses_a_window_outside_one_day_to_ten_years(tmp_path: Path, days) -> None:
    with pytest.raises(ValueError, match="since_days"):
        B.build(tmp_path, since_days=days, today="2026-10-20")


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


def test_registry_delta_reports_a_registry_younger_than_the_window(tmp_path: Path) -> None:
    repo = tmp_path / "git"
    repo.mkdir()
    _git(repo, "init", "-q")
    _commit(repo, {"README.md": "start\n"}, "2026-10-01")
    _commit(repo, {B.REGISTRY: [{"id": "A"}]}, "2026-10-15")
    # A commit before the cutoff exists, but none of them holds the registry.
    assert B.since_commit(repo, since_days=7, today="2026-10-20") is None
    section = B._registry_section(repo, 7, dt.date(2026, 10, 20), B.git_runner(repo))
    assert section == {"available": False, "reason": f"no commit before 2026-10-13 changed {B.REGISTRY}: "
                                                      "the registry, or the history, is younger than the window"}


def test_a_failing_git_log_is_not_reported_as_a_young_history(tmp_path: Path) -> None:
    def git(*args):
        return "false\n\n" if args == B.HISTORY_ARGS else None  # a full clone at its top; log fails

    section = B._registry_section(tmp_path, 7, dt.date(2026, 10, 20), git)
    assert section == {"available": False,
                       "reason": f"git log could not list the changes to {B.REGISTRY} before 2026-10-13"}


def test_registry_delta_reports_a_registry_deleted_before_the_cutoff(tmp_path: Path) -> None:
    repo = tmp_path / "git"
    repo.mkdir()
    _git(repo, "init", "-q")
    _commit(repo, {B.REGISTRY: [{"id": "A"}]}, "2026-10-01")
    _commit(repo, {B.REGISTRY: None, "README.md": "registry moved\n"}, "2026-10-05")
    _commit(repo, {B.REGISTRY: [{"id": "A"}]}, "2026-10-15")
    since = B.since_commit(repo, since_days=7, today="2026-10-20")
    assert since is not None and since[1] == "2026-10-05"
    delta = B.registry_delta(repo, since[0], since_date=since[1])
    assert delta["available"] is False and "added" not in delta
    assert delta["reason"] == f"{B.REGISTRY} did not exist at the cutoff (commit {since[0][:8]} of 2026-10-05)"


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


def _git_version() -> tuple[int, ...]:
    out = subprocess.run(["git", "--version"], capture_output=True, text=True, check=True).stdout
    return tuple(int(part) for part in out.split()[2].split(".")[:2])


def _blobless_clone(tmp_path: Path) -> Path:
    """A --filter=blob:none clone of _history_repo: it has the 2026-10-15 registry, not the 2026-10-01 one."""
    source = _history_repo(tmp_path)
    _git(source, "config", "uploadpack.allowFilter", "true")
    clone = tmp_path / "partial"
    subprocess.run(["git", "clone", "-q", "--filter=blob:none", source.resolve().as_uri(), str(clone)], check=True,
                   capture_output=True)
    return clone


@pytest.mark.skipif(_git_version() < (2, 44), reason="GIT_NO_LAZY_FETCH needs git 2.44")
def test_registry_delta_never_fetches_a_missing_blob(tmp_path: Path) -> None:
    clone = _blobless_clone(tmp_path)
    since = B.since_commit(clone, since_days=7, today="2026-10-20")  # the 2026-10-01 commit
    assert since is not None and since[1] == "2026-10-01"
    delta = B.registry_delta(clone, since[0], since_date=since[1])
    # The origin is reachable; reading the old registry would have fetched it from there.
    assert delta["available"] is False
    assert delta["reason"] == (f"git could not read {B.REGISTRY} at commit {since[0][:8]} of 2026-10-01: the file is "
                               "in that commit, but its content is not in this clone (a partial clone?)")


def test_registry_delta_does_not_call_an_unreadable_registry_missing(tmp_path: Path) -> None:
    clone = _blobless_clone(tmp_path)
    _git(clone, "remote", "remove", "origin")  # offline, whatever the git version
    since = B.since_commit(clone, since_days=7, today="2026-10-20")
    assert since is not None
    reason = B.registry_delta(clone, since[0], since_date=since[1])["reason"]
    assert "did not exist" not in reason and "content is not in this clone" in reason

    # When git cannot even list the commit's files, the reason stays generic.
    def git(*args):
        return None

    reason = B.registry_delta(clone, SHA, git)["reason"]
    assert reason == f"git could not read {B.REGISTRY} at commit {SHA[:8]}"


def test_git_runner_stays_offline_and_has_a_timeout(tmp_path: Path, monkeypatch) -> None:
    calls = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        return subprocess.CompletedProcess(command, 0, b"false\n\n", b"")

    monkeypatch.setattr(B.subprocess, "run", fake_run)
    assert B.git_runner(tmp_path)(*B.HISTORY_ARGS) == "false\n\n"
    [(command, kwargs)] = calls
    assert command == ["git", "-C", str(tmp_path), *B.HISTORY_ARGS]
    env = kwargs["env"]
    assert (env["GIT_NO_LAZY_FETCH"], env["GIT_TERMINAL_PROMPT"], env["GIT_OPTIONAL_LOCKS"]) == ("1", "0", "0")
    assert kwargs["stdin"] is subprocess.DEVNULL and kwargs["timeout"] == B.GIT_TIMEOUT

    def slow_run(command, **kwargs):
        raise subprocess.TimeoutExpired(command, kwargs["timeout"])

    monkeypatch.setattr(B.subprocess, "run", slow_run)
    brief = B.build(tmp_path, today="2026-10-20")
    assert brief["registry"] == {"available": False,
                                 "reason": f"RuntimeError: git rev-parse did not finish within {B.GIT_TIMEOUT} s"}


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


def test_git_reads_the_root_not_an_inherited_git_dir(tmp_path: Path, monkeypatch) -> None:
    # git exports GIT_DIR to hooks (and a shell may export it): git would then answer from that
    # repository's history for any -C directory, which it takes as the top of the work tree.
    other = _history_repo(tmp_path)
    plain = tmp_path / "plain"
    (plain / "research" / "registry").mkdir(parents=True)
    (plain / B.REGISTRY).write_text(json.dumps([{"id": "Z"}]), encoding="utf-8")
    monkeypatch.setenv("GIT_DIR", str(other / ".git"))
    assert B.since_commit(plain, since_days=7, today="2026-10-20") is None
    section = B._registry_section(plain, 7, dt.date(2026, 10, 20), B.git_runner(plain))
    assert section["available"] is False and "not a git checkout" in section["reason"]

    # The root's own repository is still found, whatever the inherited variables name.
    monkeypatch.setenv("GIT_WORK_TREE", str(plain))
    monkeypatch.setenv("GIT_INDEX_FILE", str(plain / "index"))
    since = B.since_commit(other, since_days=7, today="2026-10-20")
    assert since is not None and since[1] == "2026-10-01"

    calls = []
    for name in ("GIT_COMMON_DIR", "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_NAMESPACE"):
        monkeypatch.setenv(name, str(other / ".git"))
    monkeypatch.setattr(B.subprocess, "run", lambda command, **kw: calls.append(kw["env"]) or
                        subprocess.CompletedProcess(command, 0, b"false\n\n", b""))
    B.git_runner(plain)(*B.HISTORY_ARGS)
    assert not {"GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR", "GIT_OBJECT_DIRECTORY",
                "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_NAMESPACE"} & set(calls[0])
    assert calls[0]["GIT_NO_LAZY_FETCH"] == "1"


LOG = ("--", B.REGISTRY)


def test_allowed_git_args_accepts_only_the_brief_shapes() -> None:
    assert B.allowed_git_args(
        ("log", "-1", "--first-parent", "--before=2026-10-12T23:59:59Z", f"--format=%H{US}%ct", *LOG)) is True
    assert B.allowed_git_args(  # 00:00 on 2026-10-13 at UTC+05:45
        ("log", "-1", "--first-parent", "--before=2026-10-12T18:14:59Z", f"--format=%H{US}%ct", *LOG)) is True
    assert B.allowed_git_args(("show", f"{SHA}:{B.REGISTRY}")) is True
    assert B.allowed_git_args(("ls-tree", "--name-only", SHA, *LOG)) is True
    assert B.allowed_git_args(("rev-parse", "--is-shallow-repository", "--show-prefix")) is True


@pytest.mark.parametrize(
    "args",
    [
        ("log", "-1", "--first-parent", "--before=2026-10-12", f"--format=%H{US}%ct", *LOG),
        ("log", "-1", "--first-parent", "--before=2026-10-13T00:00:00Z", f"--format=%H{US}%ct", *LOG),  # git keeps 00:00:00
        ("log", "-1", "--first-parent", "--before=2026-10-12T23:59:59+11:00", f"--format=%H{US}%ct", *LOG),
        ("log", "-1", "--first-parent", "--before=2026-10-12T23:59:59", f"--format=%H{US}%ct", *LOG),  # local to git
        ("log", "-1", "--first-parent", "--before=2026-10-12T23:59:59Z", f"--format=%H{US}%ct"),  # not the registry's
        ("log", "-1", "--first-parent", "--before=2026-10-12T23:59:59Z", f"--format=%H{US}%ct", "--", "research/registry"),
        ("log", "-1", "--first-parent", "--before=2026-10-12T23:59:59Z", f"--format=%H{US}%ct", *LOG, "--output=/tmp/x"),
        ("log", "-1", "--first-parent", "--before=2026-10-12T23:59:59Z", f"--format=%H{US}%ct", "--output=/tmp/x",
         B.REGISTRY),
        ("log", "--first-parent", "--before=2026-10-12T23:59:59Z", f"--format=%H{US}%ct", *LOG),
        ("log", "-1", "--first-parent", "--before=yesterday", f"--format=%H{US}%ct", *LOG),
        ("log", "-1", "--first-parent", "--before=٢٠٢٦-١٠-١٢T23:59:59Z",
         f"--format=%H{US}%ct", *LOG),  # Arabic-Indic digits: \d would take them
        ("log", "-1", "--first-parent", "--before=2026-10-12T23:59:59Z", "--format=%H %s", *LOG),
        ("log", "-1", "--first-parent", f"--format=%H{US}%ct", "--before=2026-10-12T23:59:59Z", *LOG),
        ("log", "-1", "--before=2026-10-12T23:59:59Z", "--first-parent", f"--format=%H{US}%ct", *LOG),
        # Without --first-parent, a merge's other side can stand in for the checked-out branch's registry.
        ("log", "-1", "--before=2026-10-12T23:59:59Z", f"--format=%H{US}%ct", *LOG),
        ("show", f"HEAD:{B.REGISTRY}"),
        ("show", f"{SHA}:research/registry/dequantization_checks.json"),
        ("show", f"{SHA}:{B.REGISTRY}", "--output=/tmp/x"),
        ("show", f"--output=/tmp/x {SHA}:{B.REGISTRY}"),
        ("ls-tree", "--name-only", "HEAD", *LOG),
        ("ls-tree", "--name-only", SHA, "--", "research/registry"),
        ("ls-tree", "--name-only", SHA, B.REGISTRY),
        ("ls-tree", "-r", SHA, *LOG),
        ("ls-tree", "--name-only", f"{SHA} --output=/tmp/x", *LOG),
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
    assert section["available"] is True and section["flagged"] is None
    assert [a["id"] for a in section["actions"]] == ["2610.99999"]


@pytest.mark.parametrize("state", ["missing", "directory", "no papers", "not json"])
def test_arxiv_open_flags_are_not_available_without_a_readable_collisions_file(tmp_path: Path, state: str) -> None:
    # Open flags live only in the collisions file; without it "0 open" would be a guess.
    _arxiv_files(tmp_path, [_paper("2610.11111", "Open kill", "possible-kill", "2026-09-01")],
                 {"2610.99999": _verdict("should-cite", "2026-10-20", action="Cite it.")})
    path = tmp_path / B.ARXIV_STATE
    path.unlink()
    if state == "directory":
        path.mkdir()
    elif state == "no papers":
        _write_json(path, {"updated": "2026-10-19"})
    elif state == "not json":
        path.write_text("{not json", encoding="utf-8")
    section = B.arxiv_section(tmp_path, SINCE)
    assert section["available"] is True and section["flagged"] is None
    assert B.ARXIV_STATE in section["flagged_reason"]
    assert [a["id"] for a in section["actions"]] == ["2610.99999"]
    assert [r["id"] for r in section["reviewed"]] == ["2610.99999"]
    text = "\n".join(B._render_arxiv(section, SINCE))
    assert "no verdict yet: 0" not in text and "already reviewed: 0" not in text
    assert f"Possible kills and scoops: not available: {section['flagged_reason']}" in text
    assert "`2610.99999`: should-cite (human, 2026-10-20)" in text  # the verdict is still named
    assert "Cite it." in text


def test_arxiv_names_a_verdict_in_the_window_on_a_paper_first_seen_before_it(tmp_path: Path) -> None:
    # The flagged table keeps reviewed papers only when first seen in the window, so a kill
    # recorded this week on an older paper, with no action, would be only a tally.
    _arxiv_files(
        tmp_path,
        [_paper("2610.00002", "Old paper, judged a kill", "possible-kill", "2026-10-01"),
         _paper("2610.33333", "New paper", "possible-scoop", "2026-10-18")],
        {"2610.00002": _verdict("kill", "2026-10-20"),
         "2610.33333": _verdict("false-alarm", "2026-10-19"),
         "2610.44444": _verdict("scoop", "2026-10-01")},  # before the window: not named
    )
    section = B.arxiv_section(tmp_path, SINCE)
    assert [f["id"] for f in section["flagged"]] == ["2610.33333"]
    text = "\n".join(B._render_arxiv(section, SINCE))
    assert "`2610.00002`: kill (human, 2026-10-20)" in text
    assert "`2610.33333`: false-alarm" not in text  # already in the table
    assert "2610.44444" not in text


@pytest.mark.parametrize("done", ["false", "no", 1, "true"])
def test_only_action_done_true_closes_an_action(tmp_path: Path, done) -> None:
    # action_done is written by hand; a string or number is not a JSON true.
    _arxiv_files(tmp_path, [], {"2610.11111": _verdict("kill", "2026-10-20", action="Retract the note.",
                                                       action_done=done),
                                "2610.22222": _verdict("kill", "2026-10-20", action="Done.", action_done=True)})
    section = B.arxiv_section(tmp_path, SINCE)
    assert [a["id"] for a in section["actions"]] == ["2610.11111"]


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


def test_inertia_section_takes_a_string_of_warnings_as_one_warning(tmp_path: Path) -> None:
    _write_json(tmp_path / B.COCKPIT, {**COCKPIT, "warnings": "registry history unavailable"})
    assert B.inertia_section(tmp_path)["warnings"] == ["registry history unavailable"]
    _write_json(tmp_path / B.COCKPIT, {**COCKPIT, "inertia": {"available": False}, "warnings": "no git"})
    section = B.inertia_section(tmp_path)
    assert section["available"] is False and section["reason"].endswith("has no inertia measure: no git")


@pytest.mark.parametrize("field, value", [
    ("warnings", {"a": "b"}), ("warnings", 3),
    ("threshold", float("nan")), ("threshold", "8"), ("threshold", True), ("threshold", 8.5),
    ("streak", float("inf")), ("streak", None), ("streak", "13"),
])
def test_inertia_section_is_unavailable_for_a_malformed_cockpit(tmp_path: Path, field: str, value) -> None:
    # Only a hand-edited or corrupted cockpit.json gets here; a garbled section must not pass as data.
    cockpit = json.loads(json.dumps(COCKPIT))
    if field == "warnings":
        cockpit["warnings"] = value
    elif field == "threshold":
        cockpit["inertia"]["threshold"] = value
    else:
        cockpit["inertia"]["flags"][0]["streak"] = value
    _write_json(tmp_path / B.COCKPIT, cockpit)  # json writes NaN and Infinity, and Python reads them back
    section = B._section("inertia", B.inertia_section, tmp_path)
    assert section["available"] is False and field in section["reason"], section


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
    assert set(brief) == {"generated_on", "since_days", "window_start", *SECTIONS}
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
        "1 at commit ",
        "(2026-10-01), the registry's last change before 2026-10-13.",
        "Cite it in research/X.md and run the LP decoder.",  # the open action, verbatim
        "2610.11111",  # the open flag
        "FIXTURE_NOTE", "Input 7 fails.",  # the referee's flagged note and its worst claim
        "the old claim", "0.93",  # the possible duplicate
        f"Not available: {brief['inertia']['reason']}",
        "python tools/preflight/preflight.py",
    ):
        assert needle in text, needle


def test_render_shows_what_each_section_found(tmp_path: Path, monkeypatch) -> None:
    # Each actionable line, checked under its own heading: a renderer that printed "nothing to
    # report" (no open flag, no problem, no flagged direction) where there is something must fail.
    repo = _full_repo(tmp_path, monkeypatch)
    _write_json(repo / B.COCKPIT, COCKPIT)
    page = _sections(B.render(B.build(repo, today="2026-10-20")))
    registry, arxiv = page["Registry"], page["arXiv watch"]
    assert "Added (2): `B`, `C`." in registry
    assert "Removed (1, none now in the quarantine file): `A`." in registry
    assert "Possible kills and scoops with no verdict yet: 1. First seen since 2026-10-13 and already reviewed: 0." in arxiv
    assert "Verdicts recorded since 2026-10-13: 1 (should-cite 1)." in arxiv
    assert "- `2610.33333`: should-cite (human, 2026-10-19)." in arxiv  # not in the flagged table
    assert "| 2610.11111 | possible-kill | 2026-10-18 | **open**: read it | Open new kill |" in arxiv
    assert "- `FIXTURE_NOTE` **unsound** (reviewed 2026-10-21)." in page["Referee"]
    preflight = page["Preflight"]
    assert "No problems" not in preflight
    assert "- manifest: `research/audits/cli_manifest.json`: missing" in preflight
    inertia = page["Inertia"]
    assert "built 2026-10-19" in inertia and "flagged after 8 handoff sections" in inertia
    assert "- OPI / prime character (`opi`): 13 sections since the registry last gained a record here (never)." in inertia
    assert "- DCP / dihedral coset (`dcp`): 32 sections since the registry last gained a record here (2026-10-12)." in inertia
    assert "- Warning: Git history is shallow." in inertia and "No direction is flagged" not in inertia
    assert "| 0.93 | `negative:A` | the old claim | `negative:C` | the new claim |" in page["Possible duplicates"]


def test_the_window_includes_its_first_day(tmp_path: Path) -> None:
    _arxiv_files(
        tmp_path,
        [_paper("2610.11111", "First day", "possible-kill", SINCE),
         _paper("2610.22222", "Day before", "possible-scoop", "2026-10-13")],
        {"2610.11111": _verdict("false-alarm", SINCE), "2610.22222": _verdict("false-alarm", "2026-10-13")},
    )
    section = B.arxiv_section(tmp_path, SINCE)
    assert [f["id"] for f in section["flagged"]] == ["2610.11111"]
    assert [r["id"] for r in section["reviewed"]] == ["2610.11111"]


def _sections(text: str) -> dict[str, str]:
    """The rendered page split at its "## " headings: heading -> body."""
    parts = text.split("\n## ")[1:]
    return {part.split("\n", 1)[0]: part.split("\n", 1)[1] for part in parts}


def _registry(added: list[str], removed: list[str], quarantined: list[str] | None) -> dict:
    return {"available": True, "added": added, "removed": removed, "quarantined": quarantined, "since_sha": SHA,
            "since_date": "2026-10-01", "baseline_count": len(removed), "current_count": len(added)}


def _page(**sections) -> dict[str, str]:
    brief = {"generated_on": "2026-10-20", "since_days": 7, **{name: {"available": False, "reason": "x"}
                                                                for name in SECTIONS}, **sections}
    return _sections(B.render(brief))


@pytest.mark.parametrize("quarantined, expected", [
    (["NEG-B"], "Removed (3): 1 now in the quarantine file: `NEG-B`; 2 not in it: `NEG-A`, `NEG-C`."),
    (["NEG-A", "NEG-B", "NEG-C"], "Removed (3, all now in the quarantine file): `NEG-A`, `NEG-B`, `NEG-C`."),
    ([], "Removed (3, none now in the quarantine file): `NEG-A`, `NEG-B`, `NEG-C`."),
    (None, "Removed (3, the quarantine file could not be read): `NEG-A`, `NEG-B`, `NEG-C`."),
])
def test_render_names_which_removed_ids_are_quarantined(quarantined, expected) -> None:
    page = _page(registry=_registry([], ["NEG-A", "NEG-B", "NEG-C"], quarantined))
    assert expected in page["Registry"]


def test_render_keeps_pipes_in_list_items_and_escapes_them_in_table_cells() -> None:
    claim = {"quote": "max(|A|,D) <= 9 and |A|+|B|=31", "verdict": "wrong", "finding": "|A| is 12."}
    page = _page(
        referee={"available": True, "reviewed": 1, "stale": [],
                 "flagged": [{"stem": "NOTE", "overall": "unsound", "reviewed_on": "2026-10-20", "worst_claim": claim}]},
        arxiv={"available": True, "reviewed": [], "actions": [{"id": "2610.1", "action": "Check |x| < 1.", "by": "h"}],
               "flagged": [{"id": "2610.1", "title": "Bounds on |S| | T", "label": "possible-kill",
                            "first_seen": "2026-10-19", "verdict": None}]},
        duplicates={"available": True, "checked": 1, "threshold": 0.8,
                    "pairs": [{"a": "negative:A", "b": "negative:B", "score": 0.9, "title_a": "x | y", "title_b": "z"}]},
    )
    assert '"max(|A|,D) <= 9 and |A|+|B|=31". |A| is 12.' in page["Referee"]
    assert "- `2610.1` (h): Check |x| < 1." in page["arXiv watch"]
    row = next(line for line in page["arXiv watch"].splitlines() if line.startswith("| 2610.1 "))
    assert "Bounds on \\|S\\| \\| T" in row and row.replace("\\|", "").count("|") == 6
    row = next(line for line in page["Possible duplicates"].splitlines() if line.startswith("| 0.90 "))
    assert "x \\| y" in row and row.replace("\\|", "").count("|") == 6


def test_render_caps_every_list_and_says_how_many_more() -> None:
    assert B.LIST_CAP == 40  # the README's number
    n = 41
    ids = [f"{i:02d}" for i in range(n)]
    worst = {"quote": "q", "verdict": "wrong", "finding": "f"}
    page = _page(
        registry=_registry([f"ADD{i}" for i in ids], [f"REM{i}" for i in ids], []),
        arxiv={"available": True,
               "flagged": [{"id": f"FLAG{i}", "title": "t", "label": "possible-kill", "first_seen": "2026-10-19",
                            "verdict": None} for i in ids],
               "reviewed": [{"id": f"REV{i}", "verdict": "kill", "by": "h", "reviewed_on": "2026-10-19"} for i in ids],
               "actions": [{"id": f"ACT{i}", "action": "do it", "by": "h"} for i in ids]},
        referee={"available": True, "reviewed": n, "stale": [f"STALE{i}" for i in ids],
                 "flagged": [{"stem": f"NOTE{i}", "overall": "unsound", "reviewed_on": "2026-10-20",
                              "worst_claim": worst} for i in ids]},
        preflight={"available": True, "total": n,
                   "by_check": {"json": [{"path": f"PATH{i}", "message": "m"} for i in ids]}},
        inertia={"available": True, "generated_on": "2026-10-19", "threshold": 8, "warnings": [f"WARN{i}" for i in ids],
                 "flags": [{"direction": f"DIR{i}", "label": "l", "streak": 9, "last_gain": None} for i in ids]},
        duplicates={"available": True, "checked": 1, "threshold": 0.8,
                    "pairs": [{"a": f"DUP{i}", "b": "negative:B", "score": 0.9, "title_a": "x", "title_b": "y"}
                              for i in ids]},
    )
    last, over = "39", "40"
    for heading, prefixes in {"Registry": ["ADD", "REM"], "arXiv watch": ["FLAG", "REV", "ACT"],
                              "Referee": ["NOTE", "STALE"], "Preflight": ["PATH"], "Inertia": ["DIR", "WARN"],
                              "Possible duplicates": ["DUP"]}.items():
        body = page[heading]
        for prefix in prefixes:
            assert f"{prefix}{last}" in body and f"{prefix}{over}" not in body, (heading, prefix)
        assert body.count("1 more") == len(prefixes), (heading, body)


PREFLIGHT_PY = (REPO / "tools" / "preflight" / "preflight.py").resolve()


def test_build_runs_only_allow_listed_git_and_preflight_local_reads(tmp_path: Path, monkeypatch) -> None:
    # The brief's own git goes through the allow-list. The preflight section runs preflight's
    # own git, outside it: the module docstring and README must say so, and name each command.
    repo = _full_repo(tmp_path, monkeypatch)
    real_run, own, preflight = subprocess.run, [], []

    def spy(command, *args, **kwargs):
        if command[0] == "git":
            git_args = tuple(command[3:]) if command[1] == "-C" else tuple(command[1:])
            callers = {Path(frame.filename).resolve() for frame in inspect.stack()[1:]}
            (preflight if PREFLIGHT_PY in callers else own).append(git_args)
        return real_run(command, *args, **kwargs)

    monkeypatch.setattr(subprocess, "run", spy)
    B.build(repo, today="2026-10-20")
    assert own and all(B.allowed_git_args(args) for args in own), own
    assert preflight, "the preflight section ran no git"
    readme = (REPO / "tools" / "brief" / "README.md").read_text(encoding="utf-8")
    for args in preflight:
        assert args[0] in {"rev-parse", "ls-files", "diff"}, args  # local reads: none contacts a remote
        assert f"`git {args[0]}" in readme, args
    assert "preflight" in B.__doc__.split("Git is used read-only")[1].split("\n\n")[0]


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

    for days in ("0", "3651", "1000000", "seven"):  # a usage error, not a traceback
        with pytest.raises(SystemExit) as exit_info:
            B.main(["--root", str(root), "--since-days", days])
        assert exit_info.value.code == 2, days
    assert B.main(["--root", str(root), "--since-days", "3650", "--out", str(out)]) == 0


def _bare_brief() -> dict:
    return {"generated_on": "2026-10-20", "since_days": 7, **{name: {"available": False, "reason": "x"}
                                                              for name in SECTIONS}}


def test_main_refuses_an_out_that_cannot_take_the_files_before_building(tmp_path: Path, monkeypatch, capsys) -> None:
    root = tmp_path / "empty"
    root.mkdir()
    a_file = tmp_path / "a_file"
    a_file.write_text("x", encoding="utf-8")
    cases = [a_file, a_file / "below"]
    locked = tmp_path / "locked"
    locked.mkdir()
    locked.chmod(0o555)
    if os.geteuid() != 0:  # root writes anywhere
        cases += [locked, locked / "below"]
    monkeypatch.setattr(B, "build", lambda *args, **kwargs: pytest.fail("built before checking --out"))
    try:
        for out in cases:
            with pytest.raises(SystemExit) as exit_info:
                B.main(["--root", str(root), "--out", str(out)])
            assert exit_info.value.code == 2, out
            err = capsys.readouterr().err
            assert "--out" in err and "Traceback" not in err, err
    finally:
        locked.chmod(0o755)


def test_main_reports_a_failed_write_in_one_line(tmp_path: Path, monkeypatch, capsys) -> None:
    root = tmp_path / "empty"
    root.mkdir()
    out = tmp_path / "out"

    def fail(*args, **kwargs):
        raise PermissionError(13, "Permission denied", str(out / "agent_brief.json"))

    monkeypatch.setattr(B, "write", fail)
    assert B.main(["--root", str(root), "--out", str(out)]) == 2
    err = capsys.readouterr().err
    assert err.count("\n") == 1 and "Permission denied" in err and "agent_brief.json" in err, err


def test_write_replaces_each_file_whole_json_first(tmp_path: Path, monkeypatch) -> None:
    # A reader (an agent starting its session) must see the old file or the new one, never an
    # empty or half-written one.
    out = tmp_path / "out"
    out.mkdir()
    md, js = out / "AGENT_BRIEF.md", out / "agent_brief.json"
    md.write_text("old md", encoding="utf-8")
    js.write_text('{"old": true}', encoding="utf-8")
    real_replace, real_write_text, replaced, written = os.replace, Path.write_text, [], []

    def spy_replace(src, dst):
        assert md.read_text(encoding="utf-8") == "old md"  # whole, until it is replaced
        replaced.append(Path(dst).name)
        real_replace(src, dst)

    def spy_write_text(self, *args, **kwargs):
        written.append(self)
        return real_write_text(self, *args, **kwargs)

    monkeypatch.setattr(B.os, "replace", spy_replace)
    monkeypatch.setattr(Path, "write_text", spy_write_text)
    B.write(tmp_path, _bare_brief(), out)
    monkeypatch.undo()
    assert replaced == ["agent_brief.json", "AGENT_BRIEF.md"]
    assert md not in written and js not in written
    assert sorted(path.name for path in out.iterdir()) == ["AGENT_BRIEF.md", "agent_brief.json"]
    assert md.read_text(encoding="utf-8").startswith("# Agent brief")
    assert json.loads(js.read_text(encoding="utf-8"))["since_days"] == 7

    # A write that fails leaves the old files whole and no temporary file behind.
    md.write_text("old md", encoding="utf-8")
    js.write_text('{"old": true}', encoding="utf-8")

    def full(src, dst):
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(B.os, "replace", full)
    with pytest.raises(OSError):
        B.write(tmp_path, _bare_brief(), out)
    assert md.read_text(encoding="utf-8") == "old md" and js.read_text(encoding="utf-8") == '{"old": true}'
    assert sorted(path.name for path in out.iterdir()) == ["AGENT_BRIEF.md", "agent_brief.json"]
