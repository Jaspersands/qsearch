from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from tools.corpus.cli import build_parser, main

CLI = Path(__file__).resolve().parents[2] / "tools" / "corpus" / "cli.py"


def run(capsys, *args: str) -> tuple[int, str]:
    code = main(list(args))
    return code, capsys.readouterr().out


def test_build_reports_counts(fake_repo: Path, capsys) -> None:
    code, out = run(capsys, "--root", str(fake_repo), "build")
    assert code == 0
    assert "files changed" in out and "docs total" in out


def test_been_tried_text_lists_groups_with_reason_and_location(fake_repo: Path, capsys) -> None:
    code, out = run(capsys, "--root", str(fake_repo), "been-tried", "solve mixed coset OPI with a quadratic extension norm")
    assert code == 0
    assert "Killed before" in out and "Notes and handoff" in out
    assert "NEG-OPI-MIXED-COSET-HARDNESS" in out
    assert "Why not: A polynomial norm construction" in out
    assert "research/registry/negative_results.json:" in out


def test_been_tried_json(fake_repo: Path, capsys) -> None:
    code, out = run(capsys, "--root", str(fake_repo), "been-tried", "Helstrom product readout", "--json", "-k", "2")
    payload = json.loads(out)
    assert payload["query"] == "Helstrom product readout"
    killed = payload["groups"]["Killed before"]
    assert killed[0]["doc_id"] == "negative:NEG-DCP-LOCAL-HELSTROM-HIERARCHY"
    assert {"doc_id", "kind", "location", "title", "snippet", "status", "score"} <= set(killed[0])
    assert all(len(hits) <= 2 for hits in payload["groups"].values())


def test_search_kind_filter_json(fake_repo: Path, capsys) -> None:
    code, out = run(capsys, "--root", str(fake_repo), "search", "exterior characters", "--kinds", "note", "--json")
    hits = json.loads(out)["hits"]
    assert hits and {hit["kind"] for hit in hits} == {"note"}


def test_get_prints_the_full_doc(fake_repo: Path, capsys) -> None:
    run(capsys, "--root", str(fake_repo), "build")
    code, out = run(capsys, "--root", str(fake_repo), "get", "dequant:DEQ-POLAR-GIBBS-SOURCE")
    doc = json.loads(out)
    assert code == 0 and doc["meta"]["severity"] == "high"
    code, out = run(capsys, "--root", str(fake_repo), "get", "negative:NOPE")
    assert code == 1


def test_heldout_counts_hits_at_k_and_enforces_minimum(fake_repo: Path, tmp_path: Path, capsys) -> None:
    cases = tmp_path / "cases.json"
    cases.write_text(json.dumps([{"id": "NEG-OPI-MIXED-COSET-HARDNESS", "query": "quadratic norm solver for OPI"}]))
    code, out = run(capsys, "--root", str(fake_repo), "heldout", str(cases), "-k", "5")
    assert code == 0 and "1/1" in out
    code, _ = run(capsys, "--root", str(fake_repo), "heldout", str(cases), "-k", "5", "--min", "2")
    assert code == 1


def test_script_runs_directly_without_package_install(fake_repo: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(CLI), "--root", str(fake_repo), "search", "Helstrom", "--json"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert json.loads(result.stdout)["hits"]


def _cli(fake_repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(CLI), "--root", str(fake_repo), *args], capture_output=True, text=True)


def test_corrupt_registry_is_reported_as_incomplete_not_as_novel(fake_repo: Path) -> None:
    negatives = fake_repo / "research" / "registry" / "negative_results.json"
    text = negatives.read_text()
    negatives.write_text(text[: len(text) // 2])  # a non-atomic rewrite caught half-way
    idea = "quadratic extension norm for mixed coset OPI"
    result = _cli(fake_repo, "been-tried", idea, "--json")
    payload = json.loads(result.stdout)
    assert result.returncode == 2
    assert payload["index_incomplete"] is True
    assert any(issue["path"].endswith("negative_results.json") for issue in payload["index_issues"])
    assert "negative_results.json" in result.stderr
    text_mode = _cli(fake_repo, "been-tried", idea)
    assert text_mode.returncode == 2
    assert "INDEX INCOMPLETE" in text_mode.stdout
    negatives.write_text(text)  # repaired: the warning goes away
    ok = _cli(fake_repo, "been-tried", idea, "--json")
    assert ok.returncode == 0
    assert json.loads(ok.stdout)["index_incomplete"] is False


@pytest.mark.parametrize(
    "command", [["check-new", "--text", "hidden shift sieve"], ["baselines", "hidden shift"], ["near-duplicates"], ["build"]]
)
def test_a_root_that_is_not_a_checkout_is_an_error_and_creates_nothing(tmp_path: Path, capsys, command) -> None:
    missing = tmp_path / "nosuch"
    assert main(["--root", str(missing), *command]) == 1
    assert "is not a directory" in capsys.readouterr().err
    assert not missing.exists()
    bare = tmp_path / "bare"
    bare.mkdir()
    assert main(["--root", str(bare), *command]) == 1
    assert "is not a Q-Search checkout" in capsys.readouterr().err
    assert list(bare.iterdir()) == []
    hollow = tmp_path / "hollow"
    (hollow / "research").mkdir(parents=True)
    assert main(["--root", str(hollow), *command]) == 1
    assert "nothing to index" in capsys.readouterr().err


def test_mcp_server_refuses_a_root_that_is_not_a_checkout(tmp_path: Path) -> None:
    from tools.corpus.api import CorpusRootError
    from tools.corpus.mcp_server import create_server

    with pytest.raises(CorpusRootError, match="is not a directory"):
        create_server(tmp_path / "nosuch", dense="off")
    assert not (tmp_path / "nosuch").exists()


def _options(command: str) -> set[str]:
    sub = next(action for action in build_parser()._actions if isinstance(action, argparse._SubParsersAction))
    return {option for action in sub.choices[command]._actions for option in action.option_strings}


def _named_commands(readme: str, lead: str) -> set[str]:
    match = re.search(re.escape(lead) + r" (.*?) \(", readme, re.S)
    assert match, f"README no longer says {lead!r}"
    return set(re.findall(r"`([a-z-]+)`", match.group(1)))


def test_readme_names_the_commands_that_take_json_dense_and_no_refresh() -> None:
    readme = " ".join((CLI.parent / "README.md").read_text(encoding="utf-8").split())  # one line per paragraph
    sub = next(action for action in build_parser()._actions if isinstance(action, argparse._SubParsersAction))
    commands = set(sub.choices)
    with_json = {c for c in commands if "--json" in _options(c)}
    with_dense = {c for c in commands - {"build"} if "--dense" in _options(c)}
    assert _named_commands(readme, "`--json` prints machine-readable output from") == with_json
    assert _named_commands(readme, "`--dense` adds the embedding ranker to") == with_dense
    assert {"check-new", "near-duplicates", "baselines"}.isdisjoint(with_dense)  # they reject --dense (exit 2)
    assert all("--no-refresh" in _options(c) for c in commands - {"build"})
    assert "Every command but `build` takes `--no-refresh`" in readme
