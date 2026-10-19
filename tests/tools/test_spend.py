from __future__ import annotations

import datetime as dt
import json
import os
import re
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest

from tools.spend import common, ledger, report, timed, tokens

REPO_ROOT = Path(__file__).resolve().parents[2]


def _lines(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


# --- common: timestamps, ledger I/O, registry counts -------------------------------------------


def test_to_utc_iso_normalises_offsets_epochs_and_z() -> None:
    assert common.to_utc_iso("2026-07-15T10:25:51-07:00") == "2026-07-15T17:25:51+00:00"
    assert common.to_utc_iso("2026-10-13T01:02:03.456Z") == "2026-10-13T01:02:03+00:00"
    assert common.to_utc_iso("2026-07-07T06:04:08.043055+00:00") == "2026-07-07T06:04:08+00:00"
    assert common.to_utc_iso(0.0) == "1970-01-01T00:00:00+00:00"
    assert common.day_of("2026-10-18T23:59:59+00:00") == "2026-10-18"


def test_replace_kinds_keeps_other_kinds_and_sorts(tmp_path: Path) -> None:
    path = tmp_path / "audits" / "spend_ledger.jsonl"
    timed = {"kind": "timed_run", "timestamp": "2026-08-02T00:00:00+00:00", "wall_seconds": 1.5}
    common.append_event(path, timed)
    first = [
        {"kind": "experiment_run", "timestamp": "2026-08-03T00:00:00+00:00", "run_id": "R2"},
        {"kind": "experiment_run", "timestamp": "2026-08-01T00:00:00+00:00", "run_id": "R1"},
    ]
    kept = common.replace_kinds(path, {"experiment_run"}, first)
    assert kept == 1
    assert [row.get("run_id", row["kind"]) for row in _lines(path)] == ["R1", "timed_run", "R2"]

    common.replace_kinds(path, {"experiment_run"}, [{"kind": "experiment_run", "timestamp": "2026-08-04T00:00:00+00:00", "run_id": "R3"}])
    assert [row.get("run_id", row["kind"]) for row in _lines(path)] == ["timed_run", "R3"]


def test_read_ledger_skips_a_torn_line(tmp_path: Path) -> None:
    path = tmp_path / "ledger.jsonl"
    path.write_text('{"kind": "timed_run", "timestamp": "2026-08-01T00:00:00+00:00"}\n{"kind": "tim\n', encoding="utf-8")
    assert [row["kind"] for row in common.read_ledger(path)] == ["timed_run"]
    assert common.read_ledger(tmp_path / "missing.jsonl") == []


def test_registry_counts_reads_lists_and_dicts(fake_repo: Path) -> None:
    counts = common.registry_counts(fake_repo)
    assert counts["negative_results.json"] == 2
    assert counts["quarantined_campaign_negatives.json"] == 1
    assert counts["dequantization_checks.json"] == 1
    assert counts["reductions.json"] == 0  # {"edges": [], "counts": {}}: only list values count
    (fake_repo / "research" / "registry" / "broken.json").write_text("{not json", encoding="utf-8")
    assert common.registry_counts(fake_repo, retries=0)["broken.json"] is None


# --- ledger: code-free events from existing data ---------------------------------------------

HISTORY = [
    {
        "candidate_id": "DHS-GOWERS-SIEVE",
        "experiment_id": "EXP-DHS-PHASE-SIEVE",
        "falsifier_count": 5,
        "metrics": {"negative_results_written": 2, "sieve_final_states": 18},
        "recorded_at": "2026-07-07T06:04:08.043055+00:00",
        "run_id": "RUN-EXP-DHS-PHASE-SIEVE-00001",
        "status": "needs-theory",
        "summary": "Long prose that the ledger does not copy.",
    },
    {
        "candidate_id": "CODE-COSET-COLLECTIVE",
        "experiment_id": "EXP-CODE-COSET-RANK",
        "falsifier_count": 1,
        "metrics": {},
        "recorded_at": "2026-07-08T01:00:00+00:00",
        "run_id": "RUN-EXP-CODE-COSET-RANK-00002",
        "status": "blocked-by-code-invariants",
    },
    {"run_id": "RUN-NO-TIME", "metrics": {}},
]

THEOREM_LOG = """\
C 1f7df5789dd6e9a3fd0ed168c94b930fd4b57deb 2026-10-18T13:49:54+11:00

A\ttheorems/new_bridge.py
M\ttheorems/old_bridge.py
M\tqsearch.py
C ff722bd4f6336466f311b24ea8c1bd7b3741fe5a 2026-07-15T10:25:51-07:00

A\ttheorems/old_bridge.py
D\ttheorems/retired.py
A\ttheorems/data/table.json
"""


def test_experiment_run_events_copy_ids_and_negatives_not_prose() -> None:
    events = ledger.experiment_run_events(HISTORY)
    assert len(events) == 2
    first = events[0]
    assert first == {
        "kind": "experiment_run",
        "timestamp": "2026-07-07T06:04:08+00:00",
        "run_id": "RUN-EXP-DHS-PHASE-SIEVE-00001",
        "experiment_id": "EXP-DHS-PHASE-SIEVE",
        "candidate_id": "DHS-GOWERS-SIEVE",
        "status": "needs-theory",
        "falsifier_count": 5,
        "negatives_written": 2,
        "source": "research/experiment_run_history.json",
    }
    assert events[1]["negatives_written"] is None


def test_parse_theorem_log_gives_one_event_per_theorem_file_change() -> None:
    events = ledger.parse_theorem_log(THEOREM_LOG)
    assert [(e["path"], e["change"], e["timestamp"]) for e in events] == [
        ("theorems/new_bridge.py", "A", "2026-10-18T02:49:54+00:00"),
        ("theorems/old_bridge.py", "M", "2026-10-18T02:49:54+00:00"),
        ("theorems/old_bridge.py", "A", "2026-07-15T17:25:51+00:00"),
        ("theorems/retired.py", "D", "2026-07-15T17:25:51+00:00"),
    ]
    assert {e["kind"] for e in events} == {"theorem_commit"}
    assert events[0]["sha"] == "1f7df5789dd6"


def test_registry_commit_events_count_new_and_retained_ids() -> None:
    history = [
        ("a" * 40, "2026-07-15T10:00:00+00:00", [{"id": "A"}]),
        ("b" * 40, "2026-07-16T10:00:00+00:00", [{"id": "A"}, {"id": "B"}, {"id": "C"}]),
        ("c" * 40, "2026-07-17T10:00:00+00:00", [{"id": "A"}, {"id": "C"}]),
    ]
    events = ledger.registry_commit_events(history, current_ids={"A", "C", "D"}, current_mtime=1_800_000_000.0)
    commits = [e for e in events if e["kind"] == "registry_commit"]
    assert [(e["negatives"], e["negatives_delta"], e["negatives_new"], e["negatives_new_retained"]) for e in commits] == [
        (1, 1, 1, 1),
        (3, 2, 2, 1),  # B was added here but is no longer retained
        (2, -1, 0, 0),
    ]
    uncommitted = [e for e in events if e["kind"] == "registry_uncommitted"]
    assert uncommitted == [
        {
            "kind": "registry_uncommitted",
            "timestamp": common.to_utc_iso(1_800_000_000.0),
            "negatives": 3,
            "negatives_new_retained": 1,
            "source": "mtime research/registry/negative_results.json",
        }
    ]


def test_registry_commit_events_without_uncommitted_ids() -> None:
    history = [("a" * 40, "2026-07-15T10:00:00+00:00", [{"id": "A"}])]
    events = ledger.registry_commit_events(history, current_ids={"A"}, current_mtime=0.0)
    assert [e["kind"] for e in events] == ["registry_commit"]


def test_report_write_events_use_theorem_report_constants(fake_repo: Path) -> None:
    report = fake_repo / "research" / "classical_baselines" / "prime_character_exterior_bound.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("{}", encoding="utf-8")
    os.utime(report, (1_790_000_000, 1_790_000_000))
    multi = fake_repo / "theorems" / "multi_line_report.py"
    multi.write_text('REPORT_PATH = Path(\n    "research/reductions/multi.json"\n)\n', encoding="utf-8")
    (fake_repo / "research" / "reductions").mkdir(parents=True, exist_ok=True)
    (fake_repo / "research" / "reductions" / "multi.json").write_text("{}", encoding="utf-8")
    (fake_repo / "theorems" / "missing_report.py").write_text('REPORT = ROOT / "research/nowhere/gone.json"\n', encoding="utf-8")

    events = {e["path"]: e for e in ledger.report_write_events(fake_repo)}
    assert set(events) == {
        "research/classical_baselines/prime_character_exterior_bound.json",
        "research/reductions/multi.json",
    }
    first = events["research/classical_baselines/prime_character_exterior_bound.json"]
    assert first["kind"] == "report_write"
    assert first["theorem"] == "theorems/prime_character_exterior_bound.py"
    assert first["timestamp"] == common.to_utc_iso(1_790_000_000.0)
    assert events["research/reductions/multi.json"]["theorem"] == "theorems/multi_line_report.py"


def test_ledger_main_rebuilds_derived_kinds_and_keeps_timed_runs(fake_repo: Path) -> None:
    (fake_repo / "research" / "experiment_run_history.json").write_text(json.dumps(HISTORY), encoding="utf-8")
    out = fake_repo / "research" / "audits" / "spend_ledger.jsonl"
    common.append_event(out, {"kind": "timed_run", "timestamp": "2026-07-07T07:00:00+00:00", "wall_seconds": 3.0})
    common.append_event(out, {"kind": "experiment_run", "timestamp": "2026-01-01T00:00:00+00:00", "run_id": "STALE"})
    common.append_event(out, {"kind": "token_day", "timestamp": "2026-07-07T00:00:00+00:00", "total_tokens": 5})

    assert ledger.main(["--root", str(fake_repo), "--force"]) == 0  # --force: the fake repo has no git history
    rows = _lines(out)
    kinds = [row["kind"] for row in rows]
    assert kinds.count("timed_run") == 1
    assert kinds.count("token_day") == 1
    assert "STALE" not in {row.get("run_id") for row in rows}
    assert [row["run_id"] for row in rows if row["kind"] == "experiment_run"] == [
        "RUN-EXP-DHS-PHASE-SIEVE-00001",
        "RUN-EXP-CODE-COSET-RANK-00002",
    ]
    # The fake repo is not a git checkout, so there are no commit events.
    assert not {"theorem_commit", "registry_commit"} & set(kinds)
    assert rows == sorted(rows, key=lambda row: row["timestamp"])


def _runs(count: int) -> list[dict]:
    return [{"kind": "experiment_run", "timestamp": f"2026-08-{day:02d}T00:00:00+00:00", "run_id": f"R{day}"}
            for day in range(1, count + 1)]


def test_replace_kinds_refuses_to_drop_a_large_share_of_a_kind(tmp_path: Path) -> None:
    path = tmp_path / "ledger.jsonl"
    common.replace_kinds(path, set(), _runs(10))
    before = path.read_text(encoding="utf-8")
    with pytest.raises(common.RebuildRefused, match="experiment_run"):
        common.replace_kinds(path, {"experiment_run"}, _runs(7), max_drop_share=0.2)  # 30% fewer lines
    assert path.read_text(encoding="utf-8") == before
    common.replace_kinds(path, {"experiment_run"}, _runs(8), max_drop_share=0.2)  # 20%: allowed
    assert len(_lines(path)) == 8
    common.replace_kinds(path, {"experiment_run"}, _runs(1))  # no limit given: no check
    assert len(_lines(path)) == 1


def test_ledger_main_refuses_without_git_history_unless_forced(fake_repo: Path, capsys) -> None:
    out = fake_repo / "research" / "audits" / "spend_ledger.jsonl"
    common.replace_kinds(out, set(), [{"kind": "theorem_commit", "timestamp": "2026-08-01T00:00:00+00:00", "sha": "a"}])
    before = out.read_text(encoding="utf-8")
    assert ledger.main(["--root", str(fake_repo)]) != 0  # the fake repo is not a git checkout
    err = capsys.readouterr().err
    assert "git history" in err and "--force" in err
    assert out.read_text(encoding="utf-8") == before
    assert ledger.main(["--root", str(fake_repo), "--force"]) == 0


def test_ledger_history_problem_flags_shallow_and_missing_history(fake_repo: Path, monkeypatch) -> None:
    monkeypatch.setattr(ledger, "git", lambda root, *args: "true\n")
    assert "shallow" in ledger.history_problem(fake_repo)
    monkeypatch.setattr(ledger, "git", lambda root, *args: "false\n")
    assert ledger.history_problem(fake_repo) is None
    monkeypatch.setattr(ledger, "git", lambda root, *args: None)
    assert "git history" in ledger.history_problem(fake_repo)


def test_ledger_main_refuses_a_rebuild_that_drops_most_lines_of_a_kind(fake_repo: Path, monkeypatch, capsys) -> None:
    monkeypatch.setattr(ledger, "history_problem", lambda root: None)
    out = fake_repo / "research" / "audits" / "spend_ledger.jsonl"
    common.replace_kinds(out, set(), _runs(10))
    before = out.read_text(encoding="utf-8")
    (fake_repo / "research" / "experiment_run_history.json").write_text(json.dumps(HISTORY), encoding="utf-8")  # 2 runs
    assert ledger.main(["--root", str(fake_repo)]) != 0
    err = capsys.readouterr().err
    assert "experiment_run" in err and "--force" in err
    assert out.read_text(encoding="utf-8") == before
    assert ledger.main(["--root", str(fake_repo), "--force"]) == 0
    assert [row["kind"] for row in _lines(out)].count("experiment_run") == 2


# --- timed: the opt-in wrapper ---------------------------------------------------------------


def test_timed_run_records_fields_and_passes_stdout_through(fake_repo: Path, tmp_path: Path, capfd) -> None:
    out = tmp_path / "ledger.jsonl"
    code, event = timed.run_timed([sys.executable, "-c", "print(1)"], root=fake_repo, ledger=out)
    assert code == 0
    assert capfd.readouterr().out == "1\n"
    assert _lines(out) == [event]
    assert event["kind"] == "timed_run"
    assert event["exit_code"] == 0
    assert event["command"] == [Path(sys.executable).name, "-c", "print(1)"]  # the interpreter by name only
    assert isinstance(event["wall_seconds"], float) and event["wall_seconds"] > 0
    assert isinstance(event["cpu_seconds"], float) and event["cpu_seconds"] >= 0
    assert event["cpu_seconds"] == pytest.approx(event["cpu_user_seconds"] + event["cpu_system_seconds"], abs=2e-3)
    # `python -c 'print(1)'` peaks at a few tens of MB at most.
    assert isinstance(event["peak_rss_bytes"], int) and 1_000_000 < event["peak_rss_bytes"] < 200_000_000
    assert event["timestamp"] <= event["ended_at"]
    assert event["registry_before"] == event["registry_after"] == common.registry_counts(fake_repo)
    assert event["registry_delta"] == {}
    assert event["negatives_added"] == 0


def test_timed_main_passes_exit_code_and_stderr_through(fake_repo: Path, tmp_path: Path, capfd) -> None:
    out = tmp_path / "ledger.jsonl"
    script = "import sys; print('to stdout'); sys.stderr.write('to stderr\\n'); sys.exit(3)"
    code = timed.main(["--root", str(fake_repo), "--ledger", str(out), "--", sys.executable, "-c", script])
    assert code == 3
    captured = capfd.readouterr()
    assert captured.out == "to stdout\n"
    assert captured.err == "to stderr\n"
    (event,) = _lines(out)
    assert event["exit_code"] == 3


def test_timed_records_the_registry_delta(fake_repo: Path, tmp_path: Path) -> None:
    out = tmp_path / "ledger.jsonl"
    registry = fake_repo / "research" / "registry" / "negative_results.json"
    script = (
        "import json, sys; p = sys.argv[1]; rows = json.load(open(p)); "
        "rows.append({'id': 'NEG-NEW'}); json.dump(rows, open(p, 'w'))"
    )
    code, event = timed.run_timed([sys.executable, "-c", script, str(registry)], root=fake_repo, ledger=out, label="codex")
    assert code == 0
    assert event["negatives_added"] == 1
    assert event["registry_delta"] == {"negative_results.json": 1}
    assert event["registry_after"]["negative_results.json"] == 3
    assert event["label"] == "codex"
    # A path inside the repo is recorded relative to it, and the interpreter by its name only.
    assert event["command"][-1] == "research/registry/negative_results.json"
    assert event["command"][0] == Path(sys.executable).name
    assert str(fake_repo) not in json.dumps(event["command"])


def test_sanitized_command_holds_no_secrets_or_local_paths(tmp_path: Path) -> None:
    main = tmp_path / "main checkout"  # a space in the path, as in the real checkout
    worktree = main / ".claude" / "worktrees" / "wt"
    worktree.mkdir(parents=True)
    home = str(Path.home())
    command = [
        "env", "QS_API_TOKEN=tok-123", "/opt/anaconda3/bin/python3", "-B", str(main / "qsearch.py"),
        "--root", str(worktree), "validate", "--api-key=key-456", "--password", "pw-789",
        "--out", str(worktree / "research" / "x.json"), "--cache", "~/cache/dir", "/var/data/other.json",
        "-c", f"open('{home}/notes.txt'); open('{main}/research/y.json')", "--limit=5", "--auth-token", "tok-abc",
        "--sort-key", "--verbose", "--config=/etc/qsearch.toml", "https://example.org/a/b",
    ]
    recorded = timed.sanitize_command(command, [main, worktree])
    assert recorded == [
        "env", "QS_API_TOKEN=<redacted>", "python3", "-B", "qsearch.py",
        "--root", ".", "validate", "--api-key=<redacted>", "--password", "<redacted>",
        "--out", "research/x.json", "--cache", "<path>", "<path>",
        "-c", "open('<path>'); open('research/y.json')", "--limit=5", "--auth-token", "<redacted>",
        "--sort-key", "--verbose", "--config=<path>", "https://example.org/a/b",
    ]
    dumped = json.dumps(recorded)
    for leak in ("tok-123", "key-456", "pw-789", "tok-abc", home, str(tmp_path), "/opt/", "/var/", "/etc/"):
        assert leak not in dumped
    assert timed.sanitize_command(recorded, [main, worktree]) == recorded  # idempotent


def test_repo_roots_include_the_main_checkout_of_a_worktree(tmp_path: Path, monkeypatch) -> None:
    main = tmp_path / "main"
    worktree = main / ".claude" / "worktrees" / "wt"
    worktree.mkdir(parents=True)
    monkeypatch.setattr(common, "git", lambda root, *args: f"{main / '.git'}\n" if "--git-common-dir" in args else None)
    assert common.repo_roots(worktree) == [worktree.resolve(), main.resolve()]
    monkeypatch.setattr(common, "git", lambda root, *args: None)
    assert common.repo_roots(worktree) == [worktree.resolve()]


def test_timed_run_records_the_sanitized_command(fake_repo: Path, tmp_path: Path) -> None:
    out = tmp_path / "ledger.jsonl"
    command = ["env", "QS_API_TOKEN=tok-123", sys.executable, "-c", "pass", "--token", "tok-456", str(tmp_path / "x")]
    code, event = timed.run_timed(command, root=fake_repo, ledger=out)
    assert code == 0
    assert event["command"] == ["env", "QS_API_TOKEN=<redacted>", Path(sys.executable).name, "-c", "pass",
                                "--token", "<redacted>", "<path>"]
    assert event["subcommand"] is None
    text = out.read_text(encoding="utf-8")
    for leak in ("tok-123", "tok-456", str(tmp_path), sys.executable):
        assert leak not in text


def test_ledger_rebuild_sanitizes_kept_timed_run_lines(fake_repo: Path) -> None:
    out = fake_repo / "research" / "audits" / "spend_ledger.jsonl"
    raw = {
        "kind": "timed_run", "timestamp": "2026-10-18T21:26:28+00:00", "ended_at": "2026-10-18T21:26:34+00:00",
        "command": ["/opt/anaconda3/bin/python3", "-B", str(fake_repo / "qsearch.py"), "validate", "--api-key=s3cret"],
        "subcommand": "validate", "label": "claude-real-run", "wall_seconds": 6.321, "cpu_seconds": 6.788,
        "exit_code": 0, "source": "tools/spend/timed.py",
    }
    common.append_event(out, raw)
    assert ledger.main(["--root", str(fake_repo), "--force"]) == 0
    (row,) = [row for row in _lines(out) if row["kind"] == "timed_run"]
    assert row == {**raw, "command": ["python3", "-B", "qsearch.py", "validate", "--api-key=<redacted>"]}


def test_timed_cli_subprocess_passes_exit_code_and_output(fake_repo: Path, tmp_path: Path) -> None:
    out = tmp_path / "ledger.jsonl"
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "spend" / "timed.py"), "--root", str(fake_repo), "--ledger", str(out),
         "--", sys.executable, "-c", "import sys; print('hello'); sys.exit(3)"],
        capture_output=True, text=True,
    )
    assert result.returncode == 3
    assert result.stdout == "hello\n"
    assert result.stderr == ""
    assert _lines(out)[0]["exit_code"] == 3


def test_timed_missing_command_exits_127_and_is_recorded(fake_repo: Path, tmp_path: Path, capfd) -> None:
    out = tmp_path / "ledger.jsonl"
    code = timed.main(["--root", str(fake_repo), "--ledger", str(out), "--", "qsearch-no-such-command-xyz"])
    assert code == 127
    assert "qsearch-no-such-command-xyz" in capfd.readouterr().err
    assert _lines(out)[0]["exit_code"] == 127


def test_timed_without_a_command_is_a_usage_error(fake_repo: Path, tmp_path: Path, capfd) -> None:
    out = tmp_path / "ledger.jsonl"
    assert timed.main(["--root", str(fake_repo), "--ledger", str(out)]) == 2
    assert timed.main(["--root", str(fake_repo), "--ledger", str(out), "--"]) == 2
    assert not out.exists()


@pytest.mark.parametrize(
    ("command", "expected"),
    [
        (["python", "qsearch.py", "validate"], "validate"),
        (["python", "qsearch.py", "--root", "/x", "list", "--kind", "negative"], "list"),
        (["/opt/anaconda3/bin/python3", "-B", "/abs/qsearch.py", "dcp-samples"], "dcp-samples"),
        (["python", "qsearch.py", "--root=/x", "validate"], "validate"),
        (["python", "qsearch.py", "--help"], None),
        (["python", "-c", "print(1)"], None),
        # Never a path, a secret or anything else that is not a subcommand name.
        (["python", "qsearch.py", "/Users/someone/private/file.json"], None),
        (["python", "qsearch.py", "~/private"], None),
        (["python", "qsearch.py", "--token", "tok-123", "validate"], None),
        (["python", "qsearch.py", "QS_API_TOKEN=tok-123"], None),
        (["python", "tool.py", "validate"], None),
    ],
)
def test_subcommand_of(command: list[str], expected: str | None) -> None:
    assert timed.subcommand_of(command) == expected


def test_timed_exec_error_exits_126_and_is_recorded(fake_repo: Path, tmp_path: Path, capfd) -> None:
    out = tmp_path / "ledger.jsonl"
    program = tmp_path / "not_a_program"
    program.write_text("plain text, no shebang\n", encoding="utf-8")
    program.chmod(0o755)  # executable, but exec fails with ENOEXEC
    code = timed.main(["--root", str(fake_repo), "--ledger", str(out), "--", str(program)])
    assert code == 126
    assert "not_a_program" in capfd.readouterr().err
    (event,) = _lines(out)
    assert event["exit_code"] == 126
    assert event["command"] == ["not_a_program"]
    assert event["peak_rss_bytes"] is None and event["cpu_seconds"] == 0.0  # nothing ran


def test_timed_forwards_sigint_sent_to_the_wrapper_only(fake_repo: Path, tmp_path: Path) -> None:
    out = tmp_path / "ledger.jsonl"
    marker = tmp_path / "started"
    child = f"import pathlib, time; pathlib.Path({str(marker)!r}).write_text('1'); time.sleep(30)"
    wrapper = subprocess.Popen(
        [sys.executable, str(REPO_ROOT / "tools" / "spend" / "timed.py"), "--root", str(fake_repo), "--ledger", str(out),
         "--", sys.executable, "-c", child],
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True,
    )
    try:
        deadline = time.monotonic() + 20
        while not marker.exists() and time.monotonic() < deadline:
            time.sleep(0.05)
        assert marker.exists()
        started = time.monotonic()
        wrapper.send_signal(signal.SIGINT)  # to the wrapper alone, as `kill -INT <pid>` does
        code = wrapper.wait(timeout=15)
    finally:
        if wrapper.poll() is None:
            os.killpg(wrapper.pid, signal.SIGKILL)
            wrapper.wait()
    assert time.monotonic() - started < 10  # the child did not sleep out its 30 s
    assert code == 128 + signal.SIGINT
    (event,) = _lines(out)
    assert event["exit_code"] == 128 + signal.SIGINT
    assert event["wall_seconds"] < 25


def test_timed_peak_rss_is_the_childs_own_not_an_earlier_childs(fake_repo: Path, tmp_path: Path) -> None:
    # An earlier, larger child of the same process (as other tests in one pytest run are).
    subprocess.run([sys.executable, "-c", "b = bytearray(300 * 1024 * 1024); b[::4096] = b'x' * len(b[::4096])"], check=True)
    code, event = timed.run_timed([sys.executable, "-c", "pass"], root=fake_repo, ledger=tmp_path / "ledger.jsonl")
    assert code == 0
    assert 1_000_000 < event["peak_rss_bytes"] < 150 * 1024 * 1024


# --- report: per-day table, cost per retained negative, cockpit summary -----------------------


def _event(kind: str, timestamp: str, **fields) -> dict:
    return {"kind": kind, "timestamp": timestamp, **fields}


EVENTS = [
    _event("experiment_run", "2026-08-01T01:00:00+00:00", run_id="R1", negatives_written=2),
    _event("experiment_run", "2026-08-01T05:00:00+00:00", run_id="R2", negatives_written=None),
    _event("registry_commit", "2026-08-01T06:00:00+00:00", negatives=3, negatives_delta=3, negatives_new=4, negatives_new_retained=3),
    _event("theorem_commit", "2026-08-01T06:00:00+00:00", path="theorems/a.py", change="A"),
    _event("theorem_commit", "2026-08-01T06:00:00+00:00", path="theorems/b.py", change="M"),
    _event("token_day", "2026-08-01T00:00:00+00:00", date="2026-08-01", agent="codex", sessions=1, input_tokens=900,
           cached_input_tokens=600, output_tokens=100, reasoning_output_tokens=40, total_tokens=1000),
    _event("timed_run", "2026-08-02T10:00:00+00:00", ended_at="2026-08-02T10:00:10+00:00", wall_seconds=10.0,
           cpu_seconds=4.0, exit_code=0, negatives_added=1),
    _event("experiment_run", "2026-08-02T10:00:05+00:00", run_id="R3", negatives_written=1),  # inside the timed window
    _event("timed_run", "2026-08-02T11:00:00+00:00", ended_at="2026-08-02T11:00:02+00:00", wall_seconds=2.0,
           cpu_seconds=1.0, exit_code=3, negatives_added=0),
    _event("registry_uncommitted", "2026-08-02T12:00:00+00:00", negatives=4, negatives_new_retained=1),
    _event("report_write", "2026-08-03T00:00:00+00:00", path="research/x.json", theorem="theorems/x.py"),
]


def test_daily_rows_merge_sources_and_count_runs_apart_from_timed_commands() -> None:
    rows = report.daily_rows(EVENTS)
    assert [row["date"] for row in rows] == ["2026-08-01", "2026-08-02"]  # a report_write-only day is not activity
    first, second = rows
    assert (first["runs"], first["experiment_runs"], first["timed_runs"]) == (2, 2, 0)
    assert (first["wall_seconds"], first["cpu_seconds"]) == (0.0, None)
    assert (first["negatives_added"], first["theorems_added"]) == (3, 1)
    assert (first["tokens"], first["tokens_uncached"]) == (1000, 400)
    # runs are experiment runs only; the timed command that logged no experiment run is not one.
    assert (second["runs"], second["experiment_runs"], second["timed_runs"]) == (1, 1, 2)
    assert (second["wall_seconds"], second["cpu_seconds"]) == (12.0, 5.0)
    assert second["negatives_added"] == 1
    assert second["tokens"] is None


def test_summary_has_exactly_the_cockpit_shape() -> None:
    summary = report.summarize(report.daily_rows(EVENTS), generated_on="2026-10-19")
    assert set(summary) == {"generated_on", "days"}
    assert summary["generated_on"] == "2026-10-19"
    for day in summary["days"]:
        assert set(day) == {"date", "runs", "wall_seconds", "cpu_seconds", "negatives_added", "tokens"}
        assert isinstance(day["date"], str) and len(day["date"]) == 10
        assert isinstance(day["runs"], int) and isinstance(day["negatives_added"], int)
        assert isinstance(day["wall_seconds"], float)
        assert day["cpu_seconds"] is None or isinstance(day["cpu_seconds"], float)
        assert day["tokens"] is None or isinstance(day["tokens"], int)
    assert summary["days"][0] == {
        "date": "2026-08-01", "runs": 2, "wall_seconds": 0.0, "cpu_seconds": None, "negatives_added": 3, "tokens": 1000,
    }
    assert summary["days"][1]["cpu_seconds"] == 5.0


def test_costs_per_retained_negative() -> None:
    costs = report.costs(report.daily_rows(EVENTS), EVENTS)
    assert costs["runs"] == 3 and costs["negatives"] == 4
    assert costs["runs_per_negative"] == pytest.approx(0.75)
    # The only token day is 2026-08-01, so the token window holds that day's 3 negatives.
    assert costs["token_days"] == 1
    assert costs["token_negatives"] == 3
    assert costs["tokens_per_negative"] == pytest.approx(1000 / 3)
    assert costs["uncached_tokens_per_negative"] == pytest.approx(400 / 3)
    assert costs["timed_runs"] == 2
    # Raw growth of the negatives registry while timed commands ran, from any writer.
    assert costs["timed_registry_growth"] == 1
    assert costs["timed_wall_per_registry_record"] == pytest.approx(12.0)
    assert costs["timed_cpu_per_registry_record"] == pytest.approx(5.0)


def test_costs_without_timed_negatives_or_tokens_are_none() -> None:
    events = [e for e in EVENTS if e["kind"] not in {"token_day", "timed_run"}]
    costs = report.costs(report.daily_rows(events), events)
    assert costs["tokens_per_negative"] is None
    assert costs["timed_wall_per_registry_record"] is None


WINDOW_EVENTS = [
    _event("registry_commit", "2026-07-30T00:00:00+00:00", negatives_new_retained=11),  # before the first token day
    _event("token_day", "2026-08-01T00:00:00+00:00", date="2026-08-01", input_tokens=900, cached_input_tokens=600,
           output_tokens=100, total_tokens=1000),
    _event("registry_commit", "2026-08-01T06:00:00+00:00", negatives_new_retained=2),
    _event("registry_commit", "2026-08-02T06:00:00+00:00", negatives_new_retained=3),  # no token record that day
    _event("token_day", "2026-08-03T00:00:00+00:00", date="2026-08-03", input_tokens=1500, cached_input_tokens=1000,
           output_tokens=500, total_tokens=2000),
    _event("registry_commit", "2026-08-03T06:00:00+00:00", negatives_new_retained=5),
    _event("registry_commit", "2026-08-05T06:00:00+00:00", negatives_new_retained=7),  # after the last token day
]


def test_tokens_per_negative_counts_every_negative_in_the_token_window() -> None:
    rows = report.daily_rows(WINDOW_EVENTS)
    costs = report.costs(rows, WINDOW_EVENTS)
    assert (costs["first_token_day"], costs["last_token_day"]) == ("2026-08-01", "2026-08-03")
    assert costs["token_negatives"] == 2 + 3 + 5  # the 08-02 negatives count although that day has no token record
    assert costs["tokens_per_negative"] == pytest.approx(3000 / 10)
    assert costs["uncached_tokens_per_negative"] == pytest.approx((400 + 1000) / 10)
    text = report.render(rows, WINDOW_EVENTS, generated_on="2026-10-19")
    assert "10 retained negatives dated 2026-08-01 to 2026-08-03" in text
    assert "lower bound" not in text
    assert "Codex only" in text and "Gemini" in text


def test_headline_counts_experiment_runs_and_timed_commands_separately() -> None:
    text = report.render(report.daily_rows(EVENTS), EVENTS, generated_on="2026-10-19")
    assert "| Experiment runs | 3 |" in text
    assert "| Timed commands | 2 " in text
    assert "| Experiment runs per retained negative | 0.75 |" in text
    assert "Measured time per retained negative" not in text
    assert "| Timed seconds per negatives-registry record added during timed commands |" in text


@pytest.mark.parametrize("zone", ["Etc/GMT-14", "Etc/GMT+12"])  # UTC+14 and UTC-12: one differs from UTC at any hour
def test_report_generated_on_is_the_utc_date(fake_repo: Path, zone: str) -> None:
    common.replace_kinds(fake_repo / "research" / "audits" / "spend_ledger.jsonl", set(), EVENTS)
    before = dt.datetime.now(dt.timezone.utc).date().isoformat()
    subprocess.run([sys.executable, str(REPO_ROOT / "tools" / "spend" / "report.py"), "--root", str(fake_repo)],
                   env={**os.environ, "TZ": zone}, check=True, capture_output=True)
    after = dt.datetime.now(dt.timezone.utc).date().isoformat()
    summary = json.loads((fake_repo / "research" / "audits" / "spend_summary.json").read_text(encoding="utf-8"))
    assert summary["generated_on"] in {before, after}
    assert f"Generated {summary['generated_on']} " in (fake_repo / "research" / "audits" / "SPEND_REPORT.md").read_text(encoding="utf-8")


def test_tools_workflow_token_is_read_only() -> None:
    text = (REPO_ROOT / ".github" / "workflows" / "tools.yml").read_text(encoding="utf-8")
    assert re.search(r"^permissions:\n  contents: read\n", text, re.M)


def test_mtime_check_flags_checkout_clusters() -> None:
    clustered = [_event("report_write", f"2026-10-18T12:{m:02d}:00+00:00") for m in range(9)]
    clustered.append(_event("report_write", "2026-09-01T00:00:00+00:00"))
    check = report.mtime_check(clustered)
    assert check == {"files": 10, "modal_hour": "2026-10-18T12", "modal_share": 0.9, "clustered": True}
    spread = [_event("report_write", f"2026-09-{d:02d}T00:00:00+00:00") for d in range(1, 11)]
    assert report.mtime_check(spread)["clustered"] is False
    assert report.mtime_check([])["files"] == 0


def test_render_reports_per_day_tables_and_costs() -> None:
    text = report.render(report.daily_rows(EVENTS), EVENTS, generated_on="2026-10-19")
    assert text.startswith("# Spend Report")
    assert "| 2026-08-01 | 2 | 0 | 3 | 1 |" in text
    assert "Experiment runs per retained negative" in text
    assert "333" in text  # Codex tokens per retained negative
    assert "Codex" in text and "Gemini" in text
    # The first commit of a file back-fills everything made before it; the report says so.
    assert "first registry commit (2026-08-01) holds 3" in text
    assert "first theorem commit (2026-08-01) adds 1" in text


def test_report_main_writes_markdown_and_summary(fake_repo: Path) -> None:
    out = fake_repo / "research" / "audits" / "spend_ledger.jsonl"
    common.replace_kinds(out, set(), EVENTS)
    assert report.main(["--root", str(fake_repo)]) == 0
    audits = fake_repo / "research" / "audits"
    summary = json.loads((audits / "spend_summary.json").read_text(encoding="utf-8"))
    assert [day["date"] for day in summary["days"]] == ["2026-08-01", "2026-08-02"]
    assert len(summary["generated_on"]) == 10
    assert (audits / "SPEND_REPORT.md").read_text(encoding="utf-8").startswith("# Spend Report")


# --- tokens: per-day Codex token totals, aggregate only -------------------------------------

PROJECT = "/work/qsearch"
SECRETS = ("sess-123", "secret prompt", "please print token_count totals", PROJECT, "rollout-")


def _usage(total: int, input_: int, cached: int, output: int, reasoning: int) -> dict:
    return {"total_tokens": total, "input_tokens": input_, "cached_input_tokens": cached, "output_tokens": output,
            "reasoning_output_tokens": reasoning, "cache_write_input_tokens": 0}


def _session(path: Path, cwd: str, rows: list[tuple[str, dict, dict]], forked: bool = False) -> Path:
    lines = [
        {"timestamp": "2026-08-01T09:00:00.000Z", "type": "session_meta",
         "payload": {"id": "sess-123", "cwd": cwd, "forked_from_id": "sess-000" if forked else None,
                     "base_instructions": "secret prompt"}},
        {"timestamp": "2026-08-01T09:00:01.000Z", "type": "response_item",
         "payload": {"type": "message", "content": [{"text": "please print token_count totals"}]}},
        {"timestamp": "2026-08-01T09:00:02.000Z", "type": "event_msg", "payload": {"type": "token_count", "info": None}},
    ]
    for stamp, cumulative, last in rows:
        lines.append({"timestamp": stamp, "type": "event_msg", "payload": {
            "type": "token_count", "info": {"total_token_usage": cumulative, "last_token_usage": last}, "rate_limits": {}}})
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8")
    return path


def _codex_dir(base: Path) -> Path:
    sessions = base / "sessions" / "2026" / "08"
    first = _usage(100, 80, 50, 20, 5)
    _session(sessions / "rollout-a.jsonl", PROJECT, [
        ("2026-08-01T10:00:00.000Z", first, first),
        ("2026-08-01T10:00:01.000Z", first, first),  # repeated event: no new usage
        ("2026-08-02T00:30:00.000Z", _usage(250, 200, 120, 50, 10), _usage(150, 120, 70, 30, 5)),
    ])
    _session(sessions / "rollout-b.jsonl", PROJECT + "/.claude/worktrees/x", [
        # A fork starts from its parent's cumulative total; only its own turns count.
        ("2026-08-02T01:00:00.000Z", _usage(10_000, 9_000, 5_000, 1_000, 100), _usage(40, 30, 10, 10, 2)),
        ("2026-08-02T02:00:00.000Z", _usage(10_060, 9_050, 5_030, 1_010, 104), _usage(60, 50, 30, 10, 4)),
    ], forked=True)
    _session(sessions / "rollout-c.jsonl", "/work/other", [
        ("2026-08-02T03:00:00.000Z", _usage(999, 999, 0, 0, 0), _usage(999, 999, 0, 0, 0)),
    ])
    _session(sessions / "rollout-d.jsonl", PROJECT + "-sibling", [
        ("2026-08-02T03:00:00.000Z", _usage(777, 777, 0, 0, 0), _usage(777, 777, 0, 0, 0)),
    ])
    big = _usage(500, 400, 100, 100, 0)
    small = _usage(30, 20, 0, 10, 0)
    _session(sessions / "rollout-e.jsonl", PROJECT, [
        ("2026-08-03T00:00:00.000Z", big, big),
        ("2026-08-03T01:00:00.000Z", small, small),  # cumulative went down: count the event's own usage
    ])
    return base / "sessions"


EXPECTED_DAYS = {
    "2026-08-01": {"sessions": 1, "total_tokens": 100, "input_tokens": 80, "cached_input_tokens": 50,
                   "output_tokens": 20, "reasoning_output_tokens": 5},
    "2026-08-02": {"sessions": 2, "total_tokens": 250, "input_tokens": 200, "cached_input_tokens": 110,
                   "output_tokens": 50, "reasoning_output_tokens": 11},
    "2026-08-03": {"sessions": 1, "total_tokens": 530, "input_tokens": 420, "cached_input_tokens": 100,
                   "output_tokens": 110, "reasoning_output_tokens": 0},
}


def test_import_codex_sums_per_day_increments_for_project_sessions_only(tmp_path: Path) -> None:
    days, stats = tokens.import_codex([_codex_dir(tmp_path / "codex")], PROJECT)
    assert days == EXPECTED_DAYS
    assert stats["files"] == 5
    assert stats["in_project"] == 3
    assert stats["other_project"] == 2


def test_token_day_events_hold_aggregates_and_no_identifiers(tmp_path: Path) -> None:
    days, _ = tokens.import_codex([_codex_dir(tmp_path / "codex")], PROJECT)
    events = tokens.token_day_events(days)
    assert [e["date"] for e in events] == ["2026-08-01", "2026-08-02", "2026-08-03"]
    assert set(events[0]) == {"kind", "timestamp", "date", "agent", "sessions", "input_tokens", "cached_input_tokens",
                              "output_tokens", "reasoning_output_tokens", "total_tokens", "source"}
    assert events[0]["kind"] == "token_day" and events[0]["agent"] == "codex"
    assert events[0]["timestamp"] == "2026-08-01T00:00:00+00:00"
    dumped = json.dumps(events)
    for secret in SECRETS:
        assert secret not in dumped


def _rollout(path: Path, session_id: str, start: str, totals: list[tuple[str, int]], parent: str | None = None,
             cwd: str = PROJECT) -> Path:
    """A synthetic session log; each total is a cumulative total_tokens (input = total, no cache, no output)."""
    lines = [{"timestamp": start, "type": "session_meta",
              "payload": {"id": session_id, "cwd": cwd, "forked_from_id": parent}}]
    previous = 0
    for stamp, total in totals:
        lines.append({"timestamp": stamp, "type": "event_msg", "payload": {"type": "token_count", "info": {
            "total_token_usage": _usage(total, total, 0, 0, 0),
            "last_token_usage": _usage(total - previous, total - previous, 0, 0, 0)}}})
        previous = total
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8")
    return path


def _totals(days: dict) -> dict[str, int]:
    return {date: usage["total_tokens"] for date, usage in days.items()}


def test_a_fork_that_replays_its_parent_is_counted_once(tmp_path: Path) -> None:
    sessions = tmp_path / "sessions"
    _rollout(sessions / "parent.jsonl", "P", "2026-08-01T09:00:00.000Z",
             [("2026-08-01T10:00:00.000Z", 1000), ("2026-08-01T11:00:00.000Z", 3000)])
    # The fork's log starts with a copy of the parent's token_count history, re-stamped on the fork's day.
    _rollout(sessions / "fork.jsonl", "F", "2026-08-05T09:00:00.000Z",
             [("2026-08-05T09:00:01.000Z", 1000), ("2026-08-05T09:00:01.000Z", 3000), ("2026-08-05T10:00:00.000Z", 3500)],
             parent="P")
    # A fork of the fork replays the fork's whole history, the parent's copy included.
    _rollout(sessions / "grandchild.jsonl", "G", "2026-08-07T09:00:00.000Z",
             [("2026-08-07T09:00:01.000Z", 1000), ("2026-08-07T09:00:01.000Z", 3000),
              ("2026-08-07T09:00:01.000Z", 3500), ("2026-08-07T10:00:00.000Z", 3600)], parent="F")
    days, stats = tokens.import_codex([sessions], PROJECT)
    assert _totals(days) == {"2026-08-01": 3000, "2026-08-05": 500, "2026-08-07": 100}
    assert days["2026-08-05"]["input_tokens"] == 500 and days["2026-08-05"]["sessions"] == 1
    assert stats["replaying_sessions"] == 2
    assert stats["replayed_events"] == 2 + 3


def test_a_fork_of_a_parent_that_kept_running_counts_its_own_turns(tmp_path: Path) -> None:
    sessions = tmp_path / "sessions"
    _rollout(sessions / "parent.jsonl", "P", "2026-08-01T09:00:00.000Z",
             [("2026-08-01T10:00:00.000Z", 1000), ("2026-08-01T11:00:00.000Z", 3000),
              ("2026-08-02T10:00:00.000Z", 9000)])  # after the fork was made
    _rollout(sessions / "fork.jsonl", "F", "2026-08-05T09:00:00.000Z",
             [("2026-08-05T09:00:01.000Z", 1000), ("2026-08-05T09:00:01.000Z", 3000), ("2026-08-05T10:00:00.000Z", 3400)],
             parent="P")
    days, _ = tokens.import_codex([sessions], PROJECT)
    assert _totals(days) == {"2026-08-01": 3000, "2026-08-02": 6000, "2026-08-05": 400}


def test_forks_whose_parent_log_is_gone_count_the_shared_history_once(tmp_path: Path) -> None:
    sessions = tmp_path / "sessions"
    replay = [("2026-08-05T09:00:01.000Z", 1000), ("2026-08-05T09:00:01.000Z", 3000)]
    _rollout(sessions / "fork1.jsonl", "F1", "2026-08-05T09:00:00.000Z", [*replay, ("2026-08-05T10:00:00.000Z", 3200)],
             parent="GONE")
    _rollout(sessions / "fork2.jsonl", "F2", "2026-08-06T09:00:00.000Z",
             [(stamp.replace("08-05", "08-06"), total) for stamp, total in replay] + [("2026-08-06T10:00:00.000Z", 3300)],
             parent="GONE")
    days, stats = tokens.import_codex([sessions], PROJECT)
    # The parent's 3000 is counted once, in the earlier fork, on that fork's day (its own day is unknown).
    assert _totals(days) == {"2026-08-05": 3200, "2026-08-06": 300}
    assert stats["fork_parent_missing"] == 2


def test_a_torn_line_or_a_bad_record_skips_that_line_only(tmp_path: Path) -> None:
    sessions = tmp_path / "sessions"
    torn = _rollout(sessions / "a.jsonl", "A", "2026-08-01T09:00:00.000Z",
                    [("2026-08-01T10:00:00.000Z", 1000), ("2026-08-01T11:00:00.000Z", 3000)])
    with torn.open("a", encoding="utf-8") as handle:  # a session still being written
        handle.write('{"timestamp":"2026-08-01T12:00:00.000Z","type":"event_msg","payload":{"type":"token_count","info":{"tot')
    bad = _rollout(sessions / "b.jsonl", "B", "2026-08-02T09:00:00.000Z",
                   [("2026-08-02T10:00:00.000Z", 5), ("2026-08-02T11:00:00.000Z", 12)])
    rows = [json.loads(line) for line in bad.read_text(encoding="utf-8").splitlines()]
    no_stamp = json.loads(json.dumps(rows[1]))
    del no_stamp["timestamp"]
    not_a_number = json.loads(json.dumps(rows[1]))
    not_a_number["payload"]["info"]["total_token_usage"]["total_tokens"] = "lots"
    bad.write_text("".join(json.dumps(row) + "\n" for row in [rows[0], no_stamp, not_a_number, *rows[1:]]),
                   encoding="utf-8")
    days, stats = tokens.import_codex([sessions], PROJECT)
    assert _totals(days) == {"2026-08-01": 3000, "2026-08-02": 12}
    assert stats["bad_lines"] == 3
    assert stats["in_project"] == 2 and stats["unreadable"] == 0


def test_tokens_main_refuses_when_zst_logs_are_skipped(fake_repo: Path, tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.setattr(tokens, "zstd_available", lambda: False)
    out = tmp_path / "ledger.jsonl"
    sessions = _codex_dir(tmp_path / "codex")
    (sessions / "2026" / "08" / "rollout-z.jsonl.zst").write_bytes(b"\x28\xb5\x2f\xfd compressed")
    argv = ["--root", str(fake_repo), "--ledger", str(out), "--codex-dir", str(sessions), "--project-dir", PROJECT]
    assert tokens.main(argv) != 0
    err = capsys.readouterr().err
    assert "zstandard" in err and "--force" in err
    assert not out.exists() or _lines(out) == []
    assert tokens.main([*argv, "--dry-run"]) == 0  # a preview writes nothing, so it goes ahead
    assert tokens.main([*argv, "--force"]) == 0
    assert [row["date"] for row in _lines(out)] == list(EXPECTED_DAYS)


def test_tokens_main_refuses_a_rebuild_that_drops_most_token_days(fake_repo: Path, tmp_path: Path, capsys) -> None:
    out = tmp_path / "ledger.jsonl"
    old = [{"kind": "token_day", "timestamp": f"2026-07-{day:02d}T00:00:00+00:00", "date": f"2026-07-{day:02d}",
            "total_tokens": 1} for day in range(1, 11)]
    common.replace_kinds(out, set(), old)
    before = out.read_text(encoding="utf-8")
    argv = ["--root", str(fake_repo), "--ledger", str(out), "--codex-dir", str(_codex_dir(tmp_path / "codex")),
            "--project-dir", PROJECT]
    assert tokens.main(argv) != 0  # 3 days would replace 10: pruned or missing logs
    assert "token_day" in capsys.readouterr().err
    assert out.read_text(encoding="utf-8") == before
    assert tokens.main([*argv, "--force"]) == 0
    assert [row["date"] for row in _lines(out)] == list(EXPECTED_DAYS)


def test_import_reads_zstd_archives(tmp_path: Path) -> None:
    zstandard = pytest.importorskip(
        "zstandard", reason="zstandard is not in requirements-tools.txt; pip install zstandard to test .jsonl.zst reading")
    sessions = _codex_dir(tmp_path / "codex")
    for path in list(sessions.rglob("*.jsonl")):
        path.with_suffix(".jsonl.zst").write_bytes(zstandard.ZstdCompressor().compress(path.read_bytes()))
        path.unlink()
    days, stats = tokens.import_codex([sessions], PROJECT)
    assert days == EXPECTED_DAYS
    assert stats["files"] == 5


def test_tokens_main_replaces_token_days_and_keeps_other_lines(fake_repo: Path, tmp_path: Path, capsys) -> None:
    out = tmp_path / "ledger.jsonl"
    common.append_event(out, {"kind": "timed_run", "timestamp": "2026-08-01T12:00:00+00:00", "wall_seconds": 1.0})
    common.append_event(out, {"kind": "token_day", "timestamp": "2026-07-01T00:00:00+00:00", "date": "2026-07-01"})
    sessions = _codex_dir(tmp_path / "codex")
    argv = ["--root", str(fake_repo), "--ledger", str(out), "--codex-dir", str(sessions), "--project-dir", PROJECT]

    assert tokens.main([*argv, "--dry-run"]) == 0
    assert len(_lines(out)) == 2  # dry run writes nothing

    assert tokens.main(argv) == 0
    assert tokens.main(argv) == 0  # idempotent
    rows = _lines(out)
    assert [row["kind"] for row in rows].count("timed_run") == 1
    assert [row["date"] for row in rows if row["kind"] == "token_day"] == list(EXPECTED_DAYS)
    printed = capsys.readouterr().out
    for secret in SECRETS:
        assert secret not in printed


def test_project_dir_falls_back_to_root_outside_git(fake_repo: Path) -> None:
    assert tokens.project_dir(fake_repo) == str(fake_repo.resolve())
