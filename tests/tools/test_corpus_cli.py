from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from tools.corpus.cli import main

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
