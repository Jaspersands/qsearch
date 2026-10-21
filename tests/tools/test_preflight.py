from __future__ import annotations

from pathlib import Path

import pytest

from tools.preflight import preflight as pf

REPO = Path(__file__).resolve().parents[2]
BROKEN_CONTRACT = "research/hypotheses/dcp_clifford_stabilizer_magic_monotone_carry_injection_bridge_contract.json"


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_check_json_reports_the_parse_error(tmp_path: Path) -> None:
    _write(tmp_path / "research" / "hypotheses" / "bad_contract.json", '"bad \\x escape"\n')
    _write(tmp_path / "research" / "audits" / "empty.json", "[]\n")

    problems = pf.check_json(tmp_path)

    assert len(problems) == 1
    assert problems[0].check == "json"
    assert problems[0].path == "research/hypotheses/bad_contract.json"
    assert problems[0].message.startswith("Invalid \\escape: line 1 column")


def test_check_json_finds_todays_broken_contract() -> None:
    # Delete this test once the agents fix the contract.
    if not (REPO / "research" / "hypotheses").is_dir():
        pytest.skip("no research/hypotheses in this checkout")
    found = {p.path: p.message for p in pf.check_json(REPO)}
    assert found[BROKEN_CONTRACT].startswith("Invalid \\escape: line 7 column 167")


def test_problem_paths_are_relative_with_a_relative_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _write(tmp_path / "research" / "registry" / "nested" / "truncated.json", '{"id": ')
    monkeypatch.chdir(tmp_path)

    problems = pf.check_json(Path("."))

    assert [(p.check, p.path) for p in problems] == [("json", "research/registry/nested/truncated.json")]
