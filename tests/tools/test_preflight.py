from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from tools.preflight import preflight as pf

REPO = Path(__file__).resolve().parents[2]
BROKEN_CONTRACT = "research/hypotheses/dcp_clifford_stabilizer_magic_monotone_carry_injection_bridge_contract.json"

GENERAL = '''\
def add_audit(subparsers):
    subparsers.add_parser("audit")


def command_audit(args):
    return 0
'''

LAZY_IMPORTS = '''\
def command_audit(args):
    from theorems.tracked import a
    from theorems.untracked import b
    import core.gone
    return a, b, core.gone
'''

ORDER = [("audit", "qsearch_cli.commands.general", "add_audit")]
AUDIT_ENTRY = {"name": "audit", "aliases": [], "function": "command_audit", "module": "qsearch_cli.commands.general"}


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", *args],
        check=True,
        capture_output=True,
    )


def _repo(
    tmp_path: Path,
    *,
    general: str = GENERAL,
    imports: dict | None = None,
    order: list | None = None,
    dispatch: list | None = None,
    manifest: list | None = None,
    committed: dict[str, str] | None = None,
    git: bool = True,
) -> Path:
    """A minimal checkout of the split CLI; committed to a fresh git repository unless git=False."""
    repo = tmp_path / "repo"
    files = {
        "qsearch.py": '"""Shim."""\n\nfrom qsearch_cli.main import main\n',
        "qsearch_cli/__init__.py": "",
        "qsearch_cli/imports.py": f"IMPORTS = {imports if imports is not None else {}!r}\n",
        "qsearch_cli/commands/__init__.py": "",
        "qsearch_cli/commands/general.py": general,
        "qsearch_cli/registry.py": (
            f"ORDER = {order if order is not None else ORDER!r}\n\n"
            "FUNCTIONS = {'command_audit': 'qsearch_cli.commands.general'}\n\n"
            f"DISPATCH = {dispatch if dispatch is not None else []!r}\n"
        ),
        "research/audits/cli_manifest.json": json.dumps(
            {"subcommands": manifest if manifest is not None else [AUDIT_ENTRY]}, indent=1
        ) + "\n",
        **(committed or {}),
    }
    for rel, text in files.items():
        _write(repo / rel, text)
    if git:
        _git(repo, "init", "-q")
        _git(repo, "add", "-A")
        _git(repo, "commit", "-qm", "minimal checkout")
    return repo


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


def test_problem_paths_are_relative_with_a_relative_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _write(tmp_path / "research" / "registry" / "nested" / "truncated.json", '{"id": ')
    monkeypatch.chdir(tmp_path)

    problems = pf.check_json(Path("."))

    assert [(p.check, p.path) for p in problems] == [("json", "research/registry/nested/truncated.json")]
    assert pf.main(["--root", ".", "--json"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["root"] == str(tmp_path.resolve())
    assert "research/registry/nested/truncated.json" in {p["path"] for p in payload["problems"]}


def test_untracked_and_missing_theorem_modules(tmp_path: Path) -> None:
    repo = _repo(
        tmp_path,
        general=LAZY_IMPORTS,
        imports={"w": ("table_mod", "w"), "os": ("os", None)},
        dispatch=[("flag", "theorems.dispatched", "gen")],
        committed={"theorems/tracked.py": "a = 1\n"},
    )
    _write(repo / "theorems" / "untracked.py", "b = 2\n")
    _write(repo / "theorems" / "table_mod.py", "w = 3\n")
    _write(repo / "theorems" / "dispatched.py", "def gen():\n    return 0\n")  # named only by DISPATCH

    assert pf.referenced_modules(repo) == {
        "theorems/tracked.py": {"qsearch_cli/commands/general.py"},
        "theorems/untracked.py": {"qsearch_cli/commands/general.py"},
        "core/gone.py": {"qsearch_cli/commands/general.py"},
        "theorems/table_mod.py": {"qsearch_cli/imports.py"},
        "theorems/dispatched.py": {"qsearch_cli/registry.py"},
    }
    problems = pf.check_untracked_imports(repo)

    assert {p.check for p in problems} == {"imports"}
    assert {(p.path, p.message) for p in problems} == {
        ("theorems/untracked.py", "not tracked by git"),
        ("theorems/table_mod.py", "not tracked by git"),
        ("theorems/dispatched.py", "not tracked by git"),
        ("core/gone.py", "missing on disk"),
    }


def test_bare_and_package_style_imports_are_followed(tmp_path: Path) -> None:
    # An old-style addition to qsearch.py, bare, as the agents usually write imports.
    shim = '"""Shim."""\n\nfrom new_bare_bridge import generate_new_certificate\nfrom qsearch_cli.main import main\n'
    general = (
        "import json\n"
        "import numpy\n"
        "\n"
        "def command_audit(args):\n"
        "    from qsearch import validate_registry\n"
        "    from research_registry import load\n"
        "    from theorems import pkg_style\n"
        "    from core import gone_pkg\n"
        "    return json, numpy, validate_registry, load, pkg_style, gone_pkg\n"
    )
    repo = _repo(
        tmp_path, general=general, committed={"qsearch.py": shim, "core/research_registry.py": "load = 0\n"}
    )
    _write(repo / "theorems" / "new_bare_bridge.py", "def generate_new_certificate():\n    return 0\n")
    _write(repo / "theorems" / "pkg_style.py", "x = 1\n")

    # json is stdlib; numpy and qsearch are not files under theorems/ or core/, so they are skipped.
    assert pf.referenced_modules(repo) == {
        "theorems/new_bare_bridge.py": {"qsearch.py"},
        "core/research_registry.py": {"qsearch_cli/commands/general.py"},
        "theorems/pkg_style.py": {"qsearch_cli/commands/general.py"},
        "core/gone_pkg.py": {"qsearch_cli/commands/general.py"},
    }
    assert {(p.path, p.message) for p in pf.check_untracked_imports(repo)} == {
        ("theorems/new_bare_bridge.py", "not tracked by git"),
        ("theorems/pkg_style.py", "not tracked by git"),
        ("core/gone_pkg.py", "missing on disk"),
    }


def test_referenced_modules_ignores_stdlib_table_entries(tmp_path: Path) -> None:
    imports = {
        "os": ("os", None),
        "Path": ("pathlib", "Path"),
        "JSONDecoder": ("json.decoder", "JSONDecoder"),
        "w": ("table_mod", "w"),
    }
    repo = _repo(tmp_path, imports=imports, git=False)

    assert pf.referenced_modules(repo) == {"core/table_mod.py": {"qsearch_cli/imports.py"}}


def test_real_checkout_has_no_untracked_imports() -> None:
    assert pf.check_untracked_imports(REPO) == []


def test_without_git_reports_one_git_unavailable_problem(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    general = "def command_audit(args):\n    from theorems.tracked import a\n    return a\n"
    repo = _repo(tmp_path, general=general, committed={"theorems/tracked.py": "a = 1\n"}, git=False)

    assert pf.tracked_files(repo) is None
    assert pf.check_untracked_imports(repo) == [pf.Problem("imports", ".", "git unavailable")]


def test_manifest_subcommand_missing_from_order(tmp_path: Path) -> None:
    hidden = {**AUDIT_ENTRY, "name": "hidden-shift", "function": "command_hidden_shift"}
    repo = _repo(tmp_path / "missing", manifest=[AUDIT_ENTRY, hidden], git=False)

    assert pf.registry_order(repo) == {"audit": "qsearch_cli.commands.general"}
    assert pf.check_manifest(repo) == [
        pf.Problem("manifest", "qsearch_cli/registry.py", "subcommand hidden-shift missing from ORDER")
    ]

    moved = _repo(tmp_path / "moved", order=[("audit", "qsearch_cli.commands.dcp", "add_audit")], git=False)
    assert [p.message for p in pf.check_manifest(moved)] == [
        "audit: manifest says qsearch_cli.commands.general, ORDER says qsearch_cli.commands.dcp"
    ]

    (moved / pf.MANIFEST).unlink()
    assert [(p.check, p.path, p.message) for p in pf.check_manifest(moved)] == [("manifest", pf.MANIFEST, "missing")]


def test_real_manifest_matches_registry() -> None:
    assert pf.check_manifest(REPO) == []


def test_main_prints_problems_and_exits_one(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    general = "def command_audit(args):\n    from theorems.untracked import b\n    return b\n"
    dirty = _repo(tmp_path / "dirty", general=general)
    _write(dirty / "theorems" / "untracked.py", "b = 2\n")

    assert pf.main(["--root", str(dirty)]) == 1
    assert capsys.readouterr().out.splitlines() == [
        "imports: theorems/untracked.py: not tracked by git",
        "1 problems",
    ]

    clean = _repo(tmp_path / "clean")
    assert pf.main(["--root", str(clean), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload == {"root": str(clean.resolve()), "problems": [], "count": 0}


def test_validate_flag_reports_nonzero_exit(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    shim = 'import sys\nprint("checking", file=sys.stderr)\nprint("registry is broken", file=sys.stderr)\nsys.exit(3)\n'
    repo = _repo(tmp_path, committed={"qsearch.py": shim})

    assert pf.main(["--root", str(repo), "--json"]) == 0
    capsys.readouterr()
    assert pf.main(["--root", str(repo), "--validate", "--json"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["problems"] == [{"check": "validate", "path": "qsearch.py", "message": "exit 3: registry is broken"}]


def test_imports_flag_uses_split_cli_verify(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = _repo(tmp_path)
    roots = []

    def fake_check_imports(root: Path) -> tuple[int, list[str]]:
        roots.append(root)
        return 2, ["x: ImportError: y"]

    monkeypatch.setattr(pf, "_check_imports", fake_check_imports)

    assert pf.main(["--root", str(repo), "--imports", "--json"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["count"] == 1
    assert payload["problems"] == [{"check": "resolve", "path": "qsearch_cli", "message": "x: ImportError: y"}]
    assert roots == [repo.resolve()]
