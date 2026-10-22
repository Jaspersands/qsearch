from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
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
    if args: import core.gone  # a command module is parsed in full: the line scan misses this
    return a, b, core.gone
'''

ORDER = [("audit", "qsearch_cli.commands.general", "add_audit")]
FUNCTIONS = {"command_audit": "qsearch_cli.commands.general"}
# What every minimal checkout refers to inside qsearch_cli/: the shim's import and the registry's module columns.
CLI_REFS = {"qsearch_cli/main.py": {"qsearch.py"}, "qsearch_cli/commands/general.py": {"qsearch_cli/registry.py"}}
AUDIT_ENTRY = {"name": "audit", "aliases": [], "function": "command_audit", "module": "qsearch_cli.commands.general"}
GENERAL_PY = "qsearch_cli/commands/general.py"


def _by(reason: str, referrer: str = GENERAL_PY) -> str:
    """An imports problem's message: why, then the (first) file that refers to the module."""
    return f"{reason}; referred to by {referrer}"


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
    functions: dict | None = None,
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
        "qsearch_cli/main.py": "def main():\n    return 0\n",
        "qsearch_cli/imports.py": f"IMPORTS = {imports if imports is not None else {}!r}\n",
        "qsearch_cli/commands/__init__.py": "",
        "qsearch_cli/commands/general.py": general,
        "qsearch_cli/registry.py": (
            f"ORDER = {order if order is not None else ORDER!r}\n\n"
            f"FUNCTIONS = {functions if functions is not None else FUNCTIONS!r}\n\n"
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


def test_check_json_parses_a_huge_integer_and_reports_deep_nesting(tmp_path: Path) -> None:
    # Python's int() refuses more than 4300 digits and json recurses per level: neither may end the run.
    _write(tmp_path / "research" / "audits" / "big.json", "[" + "7" * 5000 + "]\n")
    _write(tmp_path / "research" / "audits" / "deep.json", "[" * 100_000 + "]" * 100_000)
    _write(tmp_path / "research" / "registry" / "truncated.json", '{"id": ')

    problems = pf.check_json(tmp_path)

    assert [p.path for p in problems] == ["research/registry/truncated.json", "research/audits/deep.json"]
    assert "recursion" in problems[1].message


def test_check_json_rereads_a_file_caught_mid_rewrite(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Another agent rewriting a registry file: the first read sees half of it.
    record = _write(tmp_path / "research" / "registry" / "negative_results.json", '[\n  {"id": "NEG-1"}\n]\n')
    broken = _write(tmp_path / "research" / "registry" / "broken.json", '{"id": ')
    real_read_text = Path.read_text
    reads: dict[str, int] = {}

    def read_text(self: Path, *args, **kwargs) -> str:
        text = real_read_text(self, *args, **kwargs)
        reads[self.name] = reads.get(self.name, 0) + 1
        return text[: len(text) // 2] if self == record and reads[self.name] == 1 else text

    sleeps: list[float] = []
    monkeypatch.setattr(Path, "read_text", read_text)
    monkeypatch.setattr(pf.time, "sleep", sleeps.append)

    problems = pf.check_json(tmp_path)

    assert [(p.path, p.message) for p in problems] == [
        ("research/registry/broken.json", "Expecting value: line 1 column 8 (char 7)")
    ]
    assert reads == {"negative_results.json": 2, "broken.json": pf.JSON_RETRIES + 1}
    assert broken.is_file() and len(sleeps) == 1 + pf.JSON_RETRIES


def test_check_json_reports_a_dangling_symlink(tmp_path: Path) -> None:
    audits = tmp_path / "research" / "audits"
    _write(audits / "fine.json", "[]\n")
    (audits / "dangling.json").symlink_to(audits / "deleted.json")

    assert [(p.path, p.message) for p in pf.check_json(tmp_path)] == [("research/audits/dangling.json", "dangling symlink")]


def test_check_json_reports_a_directory_it_cannot_list(tmp_path: Path) -> None:
    locked = tmp_path / "research" / "audits" / "locked"
    _write(locked / "broken.json", "{")
    locked.chmod(0)
    try:
        if os.access(locked, os.R_OK):
            pytest.skip("running as a user that can list any directory")
        problems = pf.check_json(tmp_path)
    finally:
        locked.chmod(0o755)

    assert [(p.path, p.message) for p in problems] == [("research/audits/locked", "cannot list: Permission denied")]


def test_check_json_reports_non_utf8_bytes_and_reads_only_regular_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    audits = tmp_path / "research" / "audits"
    (audits / "latin1.json").parent.mkdir(parents=True)
    (audits / "latin1.json").write_bytes('{"name": "Schrödinger"}'.encode("latin-1"))
    _write(audits / "folder.json" / "inner.json", "{")  # a directory named *.json is walked, not read
    monkeypatch.chdir(audits)  # AF_UNIX paths are short on macOS: bind a relative one
    with socket.socket(socket.AF_UNIX) as sock:
        sock.bind("socket.json")  # neither a file to parse nor a problem

        problems = pf.check_json(tmp_path)

    assert [p.path for p in problems] == ["research/audits/folder.json/inner.json", "research/audits/latin1.json"]
    assert "codec can't decode byte" in problems[1].message


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
    _write(tmp_path / "qsearch.py", "")
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
        **CLI_REFS,
        "theorems/tracked.py": {"qsearch_cli/commands/general.py"},
        "theorems/untracked.py": {"qsearch_cli/commands/general.py"},
        "core/gone.py": {"qsearch_cli/commands/general.py"},
        "theorems/table_mod.py": {"qsearch_cli/imports.py"},
        "theorems/dispatched.py": {"qsearch_cli/registry.py"},
    }
    problems = pf.check_untracked_imports(repo)

    assert {p.check for p in problems} == {"imports"}
    assert {(p.path, p.message) for p in problems} == {
        ("theorems/untracked.py", _by("not tracked by git")),
        ("theorems/table_mod.py", _by("not tracked by git", "qsearch_cli/imports.py")),
        ("theorems/dispatched.py", _by("not tracked by git", "qsearch_cli/registry.py")),
        ("core/gone.py", _by("missing on disk")),
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
        **CLI_REFS,
        "theorems/new_bare_bridge.py": {"qsearch.py"},
        "core/research_registry.py": {"qsearch_cli/commands/general.py"},
        "theorems/pkg_style.py": {"qsearch_cli/commands/general.py"},
        "core/gone_pkg.py": {"qsearch_cli/commands/general.py"},
    }
    assert {(p.path, p.message) for p in pf.check_untracked_imports(repo)} == {
        ("theorems/new_bare_bridge.py", _by("not tracked by git", "qsearch.py")),
        ("theorems/pkg_style.py", _by("not tracked by git")),
        ("core/gone_pkg.py", _by("missing on disk")),
    }


def test_package_style_imports_table_entries_name_the_submodule(tmp_path: Path) -> None:
    # `migrate.py sweep` turns `from theorems import x` in qsearch.py into ("theorems", "x"),
    # which qsearch_cli/resolve.py loads as the submodule theorems/x.py.
    imports = {
        "tracked_pkg": ("theorems", "tracked_pkg"),
        "new_pkg": ("theorems", "new_pkg"),
        "core_pkg": ("core", "core_pkg"),
        "theorems": ("theorems", None),
    }
    repo = _repo(tmp_path, imports=imports, committed={"theorems/tracked_pkg.py": "x = 1\n"})
    _write(repo / "theorems" / "new_pkg.py", "y = 2\n")

    assert pf.referenced_modules(repo) == {
        **CLI_REFS,
        "theorems/tracked_pkg.py": {"qsearch_cli/imports.py"},
        "theorems/new_pkg.py": {"qsearch_cli/imports.py"},
        "core/core_pkg.py": {"qsearch_cli/imports.py"},
    }
    assert {(p.path, p.message) for p in pf.check_untracked_imports(repo)} == {
        ("theorems/new_pkg.py", _by("not tracked by git", "qsearch_cli/imports.py")),
        ("core/core_pkg.py", _by("missing on disk", "qsearch_cli/imports.py")),
    }


def test_relative_imports_name_the_module_they_load(tmp_path: Path) -> None:
    # The CLI loads theorem modules as theorems.x, so `from .helper import h` loads theorems/helper.py.
    module = (
        "if __package__:\n"
        "    from .rel_helper import h\n"
        "    from . import rel_sibling, rel_pkg\n"
        "    from .rel_pkg.inner import i\n"
        "    from ..beyond_the_top import b\n"  # past the top package: an ImportError, no file
        "f = 1\n"
    )
    command = "from . import other_cmd\nfrom ..cli_helper import c\n\n" + GENERAL
    general = "def command_audit(args):\n    from theorems.mod import f\n    return f\n"
    repo = _repo(tmp_path, general=general, committed={"theorems/mod.py": module, "qsearch_cli/commands/dcp.py": command})
    _write(repo / "theorems" / "rel_helper.py", "h = 1\n")
    _write(repo / "theorems" / "beyond_the_top.py", "b = 1\n")
    _write(repo / "theorems" / "rel_pkg" / "__init__.py", "")
    _write(repo / "theorems" / "rel_pkg" / "inner.py", "i = 1\n")
    _write(repo / "qsearch_cli" / "cli_helper.py", "c = 1\n")
    _write(repo / "qsearch_cli" / "commands" / "other_cmd.py", "")
    order = [*ORDER, ("dcp-audit", "qsearch_cli.commands.dcp", "add_audit")]
    (repo / "qsearch_cli" / "registry.py").write_text(f"ORDER = {order!r}\n\nFUNCTIONS = {FUNCTIONS!r}\n", encoding="utf-8")

    refs = pf.referenced_modules(repo)

    assert {path: refs[path] for path in set(refs) - set(CLI_REFS)} == {
        "theorems/mod.py": {"qsearch_cli/commands/general.py"},
        "qsearch_cli/commands/dcp.py": {"qsearch_cli/registry.py"},
        "theorems/rel_helper.py": {"theorems/mod.py"},
        "theorems/rel_sibling.py": {"theorems/mod.py"},
        "theorems/rel_pkg/__init__.py": {"theorems/mod.py"},
        "theorems/rel_pkg/inner.py": {"theorems/mod.py"},
        "qsearch_cli/commands/__init__.py": {"qsearch_cli/commands/dcp.py"},
        "qsearch_cli/commands/other_cmd.py": {"qsearch_cli/commands/dcp.py"},
        "qsearch_cli/cli_helper.py": {"qsearch_cli/commands/dcp.py"},
    }
    dcp = "qsearch_cli/commands/dcp.py"
    assert {(p.path, p.message) for p in pf.check_untracked_imports(repo)} == {
        ("theorems/rel_helper.py", _by("not tracked by git", "theorems/mod.py")),
        ("theorems/rel_sibling.py", _by("missing on disk", "theorems/mod.py")),
        ("theorems/rel_pkg/__init__.py", _by("not tracked by git", "theorems/mod.py")),
        ("theorems/rel_pkg/inner.py", _by("not tracked by git", "theorems/mod.py")),
        ("qsearch_cli/commands/other_cmd.py", _by("not tracked by git", dcp)),
        ("qsearch_cli/cli_helper.py", _by("not tracked by git", dcp)),
    }


def test_package_style_imports_of_qsearch_cli_and_of_subpackages(tmp_path: Path) -> None:
    # `from qsearch_cli import helpers` loads qsearch_cli/helpers.py; `from theorems import sub`,
    # with sub a directory, loads theorems/sub/__init__.py, not a theorems/sub.py.
    general = (
        "from qsearch_cli import helpers, ghost\n"
        "from qsearch_cli.commands import wip, defined_in_init\n"
        "from theorems import sub\n"
        "\n" + GENERAL
    )
    imports = {
        "parser": ("qsearch_cli", "parser"),
        "qsearch_cli": ("qsearch_cli", None),
        "main": ("qsearch", "main"),
        "subpkg": ("theorems", "subpkg"),
        "g": ("theorems.subpkg", "g"),
        "deep": ("theorems.subpkg", "deep"),
    }
    repo = _repo(tmp_path, general=general, imports=imports, committed={"qsearch_cli/parser.py": ""})
    _write(repo / "qsearch_cli" / "helpers.py", "")
    _write(repo / "qsearch_cli" / "commands" / "wip.py", "")
    _write(repo / "theorems" / "sub" / "__init__.py", "")
    _write(repo / "theorems" / "subpkg" / "__init__.py", "g = 1\n")
    _write(repo / "theorems" / "subpkg" / "deep.py", "")

    refs = pf.referenced_modules(repo)

    assert {path: refs[path] for path in set(refs) - set(CLI_REFS)} == {
        "qsearch_cli/helpers.py": {"qsearch_cli/commands/general.py"},
        "qsearch_cli/ghost.py": {"qsearch_cli/commands/general.py"},
        "qsearch_cli/commands/__init__.py": {"qsearch_cli/commands/general.py"},
        "qsearch_cli/commands/wip.py": {"qsearch_cli/commands/general.py"},
        "theorems/sub/__init__.py": {"qsearch_cli/commands/general.py"},
        "qsearch_cli/parser.py": {"qsearch_cli/imports.py"},
        "theorems/subpkg/__init__.py": {"qsearch_cli/imports.py"},
        "theorems/subpkg/deep.py": {"qsearch_cli/imports.py"},
    }
    assert {(p.path, p.message) for p in pf.check_untracked_imports(repo)} == {
        ("qsearch_cli/helpers.py", _by("not tracked by git")),
        ("qsearch_cli/ghost.py", _by("missing on disk")),
        ("qsearch_cli/commands/wip.py", _by("not tracked by git")),
        ("theorems/sub/__init__.py", _by("not tracked by git")),
        ("theorems/subpkg/__init__.py", _by("not tracked by git", "qsearch_cli/imports.py")),
        ("theorems/subpkg/deep.py", _by("not tracked by git", "qsearch_cli/imports.py")),
    }


def test_cli_modules_the_registry_and_shim_load_are_checked(tmp_path: Path) -> None:
    # parser.py imports every ORDER module to build --help, so one missing from a clone breaks every command.
    order = [
        *ORDER,
        ("newcmd", "qsearch_cli.commands.newdomain", "add_newcmd"),
        ("ghost", "qsearch_cli.commands.ghost", "add_ghost"),
    ]
    functions = {**FUNCTIONS, "command_fn": "qsearch_cli.commands.fnonly"}
    # A dotted name that is a package directory loads its __init__.py, not qsearch_cli/commands.py.
    repo = _repo(tmp_path, general="import qsearch_cli.commands\n\n" + GENERAL, order=order, functions=functions)
    _write(repo / "qsearch_cli" / "commands" / "newdomain.py", "def add_newcmd(subparsers):\n    pass\n")
    _write(repo / "qsearch_cli" / "commands" / "fnonly.py", "def command_fn(args):\n    return 0\n")
    _git(repo, "rm", "-q", "--cached", "qsearch_cli/main.py")
    _git(repo, "commit", "-qm", "untrack main")

    assert pf.referenced_modules(repo) == {
        **CLI_REFS,
        "qsearch_cli/commands/newdomain.py": {"qsearch_cli/registry.py"},
        "qsearch_cli/commands/ghost.py": {"qsearch_cli/registry.py"},
        "qsearch_cli/commands/fnonly.py": {"qsearch_cli/registry.py"},
        "qsearch_cli/commands/__init__.py": {"qsearch_cli/commands/general.py"},
    }
    registry = "qsearch_cli/registry.py"
    assert {(p.path, p.message) for p in pf.check_untracked_imports(repo)} == {
        ("qsearch_cli/main.py", _by("not tracked by git", "qsearch.py")),
        ("qsearch_cli/commands/newdomain.py", _by("not tracked by git", registry)),
        ("qsearch_cli/commands/ghost.py", _by("missing on disk", registry)),
        ("qsearch_cli/commands/fnonly.py", _by("not tracked by git", registry)),
    }


def test_command_files_the_cli_never_loads_are_not_read(tmp_path: Path) -> None:
    # iCloud duplicates and scratch files beside the command modules: no table names them,
    # so neither parser.py nor resolve.py nor main.py ever imports them.
    repo = _repo(tmp_path)
    commands = repo / "qsearch_cli" / "commands"
    _write(commands / "general 2.py", "import theorems.renamed_away\n")
    _write(commands / "general 3.py", "def broken(:\n")
    (commands / "legacy_notes.py").write_bytes("# Schrödinger\nimport theorems.gone\n".encode("latin-1"))
    _write(commands / "wip.py", "from theorems.wip_mod import f\n")
    _write(repo / "theorems" / "wip_mod.py", "f = 1\n")

    assert pf.referenced_modules(repo) == CLI_REFS
    assert pf.check_untracked_imports(repo) == []


@pytest.mark.parametrize(
    "content, error",
    [(b"def add_audit(:\n", "SyntaxError: "), ("# Schrödinger\n".encode("latin-1"), "UnicodeDecodeError: ")],
)
def test_a_command_module_that_cannot_be_read_is_named(tmp_path: Path, content: bytes, error: str) -> None:
    repo = _repo(tmp_path)
    (repo / "qsearch_cli" / "commands" / "general.py").write_bytes(content)

    [problem] = pf.check_untracked_imports(repo)

    assert problem.path == "qsearch_cli/commands/general.py"
    assert problem.message.startswith(f"cannot read the CLI sources: {error}")


def test_each_problem_names_a_file_that_refers_to_the_module(tmp_path: Path) -> None:
    general = "def command_audit(args):\n    from theorems.gone import a\n    from theorems.shared import s\n    return a, s\n"
    repo = _repo(
        tmp_path,
        general=general,
        imports={"s": ("theorems.shared", "s")},
        committed={"theorems/user.py": "from theorems.shared import s\n"},
        dispatch=[("flag", "theorems.user", "gen")],
    )
    _write(repo / "theorems" / "shared.py", "s = 1\n")

    assert pf.check_untracked_imports(repo) == [
        pf.Problem("imports", "theorems/gone.py", "missing on disk; referred to by qsearch_cli/commands/general.py"),
        pf.Problem(
            "imports", "theorems/shared.py", "not tracked by git; referred to by qsearch_cli/commands/general.py and 2 more"
        ),
    ]


TRACKED_WITH_HELPERS = '''\
"""Uses helpers, but not this one:

from theorems.in_docstring import x
"""
QUOTE = "\'\'\'"  # a quote inside a string starts no string
from helper import h
from core.helper2 import h2  # import theorems.in_comment
import os, json


def lazy():
    from helper3 import (
        h3,
    )
    import theorems.gone \\
        as gone
    return h3, gone, """
import theorems.in_string"""


a = 1
'''


def test_imports_inside_referenced_modules_are_followed(tmp_path: Path) -> None:
    # A committed module whose own helper never was: fine in this copy, ModuleNotFoundError in a clone.
    general = "def command_audit(args):\n    from theorems.tracked import a\n    return a\n"
    repo = _repo(tmp_path, general=general, committed={"theorems/tracked.py": TRACKED_WITH_HELPERS})
    _write(repo / "theorems" / "helper.py", "from deep import d\n\nh = 1\n")  # bare: theorems/ first
    _write(repo / "theorems" / "deep.py", "import theorems.tracked\n\nd = 1\n")  # a cycle back
    _write(repo / "core" / "helper2.py", "h2 = 1\n")
    _write(repo / "core" / "helper3.py", "h3 = 1\n")

    refs = pf.referenced_modules(repo)

    assert refs["theorems/tracked.py"] == {"qsearch_cli/commands/general.py", "theorems/deep.py"}
    assert refs["theorems/helper.py"] == {"theorems/tracked.py"}
    assert refs["theorems/deep.py"] == {"theorems/helper.py"}
    assert not {"theorems/in_docstring.py", "theorems/in_comment.py", "theorems/in_string.py"} & set(refs)
    tracked = "theorems/tracked.py"
    assert {(p.path, p.message) for p in pf.check_untracked_imports(repo)} == {
        ("theorems/helper.py", _by("not tracked by git", tracked)),
        ("theorems/deep.py", _by("not tracked by git", "theorems/helper.py")),
        ("core/helper2.py", _by("not tracked by git", tracked)),
        ("core/helper3.py", _by("not tracked by git", tracked)),
        ("theorems/gone.py", _by("missing on disk", tracked)),
    }


def test_line_scan_finds_what_a_full_parse_finds_on_the_real_checkout() -> None:
    import ast

    def statements(nodes) -> list[str]:
        return sorted(ast.unparse(n) for n in nodes if isinstance(n, (ast.Import, ast.ImportFrom)))

    files = [p for d in ("theorems", "core", "qsearch_cli") for p in sorted((REPO / d).rglob("*.py"))]
    differing = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        if statements(pf._scanned_imports(text)) != statements(ast.walk(ast.parse(text))):
            differing.append(path.relative_to(REPO).as_posix())
    assert len(files) > 1000
    assert differing == []


def test_bare_names_resolve_to_theorems_before_core_and_skip_stdlib_and_stars(tmp_path: Path) -> None:
    # The CLI puts theorems/ on sys.path before core/; the README says standard library names
    # are skipped, even beside a file of that name, and `import *` names no file.
    general = (
        "import json\n"
        "from dual import f\n"
        "from theorems import *\n"
        "\n"
        "def command_audit(args):\n"
        "    return json, f\n"
    )
    repo = _repo(tmp_path, general=general, imports={"g": ("dual", "g")}, git=False)
    for directory in ("theorems", "core"):
        _write(repo / directory / "dual.py", "f = g = 1\n")
        _write(repo / directory / "json.py", "")

    assert pf.referenced_modules(repo) == {
        **CLI_REFS,
        "theorems/dual.py": {"qsearch_cli/commands/general.py", "qsearch_cli/imports.py"},
    }


def test_referenced_modules_ignores_stdlib_table_entries(tmp_path: Path) -> None:
    imports = {
        "os": ("os", None),
        "Path": ("pathlib", "Path"),
        "JSONDecoder": ("json.decoder", "JSONDecoder"),
        "w": ("table_mod", "w"),
    }
    repo = _repo(tmp_path, imports=imports, git=False)

    assert pf.referenced_modules(repo) == {**CLI_REFS, "core/table_mod.py": {"qsearch_cli/imports.py"}}


def test_staged_module_counts_as_tracked_but_intent_to_add_does_not(tmp_path: Path) -> None:
    # Run before a commit: a plain commit includes a staged file, but leaves out one added with -N.
    general = "def command_audit(args):\n    from theorems.staged import a\n    from theorems.intent import b\n    return a, b\n"
    repo = _repo(tmp_path, general=general)
    _write(repo / "theorems" / "staged.py", "a = 1\n")
    _write(repo / "theorems" / "intent.py", "b = 2\n")
    _git(repo, "add", "theorems/staged.py")
    _git(repo, "add", "-N", "theorems/intent.py")

    assert "theorems/staged.py" in pf.tracked_files(repo)
    assert "theorems/intent.py" not in pf.tracked_files(repo)
    assert pf.check_untracked_imports(repo) == [
        pf.Problem("imports", "theorems/intent.py", _by("not tracked by git (intent-to-add only)"))
    ]


def test_an_unstaged_edit_is_not_intent_to_add(tmp_path: Path) -> None:
    # The usual state before a commit: committed modules edited, not yet staged.
    general = "def command_audit(args):\n    from theorems.edited import a\n    from theorems.intent import b\n    return a, b\n"
    repo = _repo(tmp_path, general=general, committed={"theorems/edited.py": "a = 1\n"})
    _write(repo / "theorems" / "edited.py", "a = 2\n")
    _write(repo / "qsearch_cli" / "commands" / "general.py", general + "\n# edited\n")
    _write(repo / "theorems" / "intent.py", "b = 2\n")
    _git(repo, "add", "-N", "theorems/intent.py")

    assert pf.check_untracked_imports(repo) == [
        pf.Problem("imports", "theorems/intent.py", _by("not tracked by git (intent-to-add only)"))
    ]


def test_a_renamed_module_marked_intent_to_add_is_still_not_tracked(tmp_path: Path) -> None:
    # Rename detection would pair the new name with the deleted old one and hide it from --diff-filter=A.
    general = "def command_audit(args):\n    from theorems.new_name import a\n    return a\n"
    repo = _repo(tmp_path, general=general, committed={"theorems/old_name.py": "a = 1\n" * 20})
    (repo / "theorems" / "old_name.py").rename(repo / "theorems" / "new_name.py")
    _git(repo, "add", "-N", "theorems/new_name.py")

    assert pf.check_untracked_imports(repo) == [
        pf.Problem("imports", "theorems/new_name.py", _by("not tracked by git (intent-to-add only)"))
    ]


def test_the_imports_check_never_writes_the_git_index(tmp_path: Path) -> None:
    # Porcelain `git diff` refreshes stale stat data and rewrites .git/index under index.lock,
    # which fails another agent's `git add` or `git commit` in the same checkout.
    general = "def command_audit(args):\n    from theorems.tracked import a\n    from theorems.intent import b\n    return a, b\n"
    repo = _repo(tmp_path, general=general, committed={"theorems/tracked.py": "a = 1\n", "core/c.py": "c = 1\n"})
    _write(repo / "theorems" / "intent.py", "b = 2\n")
    _git(repo, "add", "-N", "theorems/intent.py")
    for rel in ("theorems/tracked.py", "core/c.py", "qsearch_cli/commands/general.py"):
        path = repo / rel
        path.write_bytes(path.read_bytes())  # same content, new stat data
        stat = path.stat()
        os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns + 5_000_000_000))
    index = repo / ".git" / "index"
    before = (index.read_bytes(), index.stat().st_mtime_ns, index.stat().st_ino)

    problems = pf.check_untracked_imports(repo)

    assert [p.path for p in problems] == ["theorems/intent.py"]
    assert (index.read_bytes(), index.stat().st_mtime_ns, index.stat().st_ino) == before


def test_a_module_named_in_the_wrong_case_is_missing_on_every_file_system(tmp_path: Path) -> None:
    # Python's import matches case even on macOS, whose file system does not: git add would not help.
    general = "def command_audit(args):\n    from theorems.Tracked import a\n    from theorems.Gone import b\n    return a, b\n"
    repo = _repo(tmp_path, general=general, committed={"theorems/tracked.py": "a = 1\n"})

    assert pf.check_untracked_imports(repo) == [
        pf.Problem("imports", "theorems/Gone.py", _by("missing on disk")),
        pf.Problem("imports", "theorems/Tracked.py", _by("missing on disk (case differs: theorems/tracked.py)")),
    ]


@pytest.mark.parametrize(
    "tables, table",
    [
        ({"imports": {"x": (None, "x")}}, "IMPORTS"),
        ({"imports": [("a", "b")]}, "IMPORTS"),
        ({"imports": {"x": "ab"}}, "IMPORTS"),  # would unpack into module "a", attribute "b"
        ({"dispatch": [("f", 3, "g")]}, "DISPATCH"),
        ({"order": [("audit", None, "add_audit")]}, "ORDER"),
        ({"functions": ["command_audit"]}, "FUNCTIONS"),
        ({"functions": {"command_audit": 3}}, "FUNCTIONS"),
    ],
)
def test_a_table_of_the_wrong_shape_is_one_problem(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], tables: dict, table: str
) -> None:
    repo = _repo(tmp_path, git=False, **tables)

    assert pf.main(["--root", str(repo)]) == 1
    lines = capsys.readouterr().out.splitlines()
    [line] = [line for line in lines if line.startswith("imports: .: cannot read")]
    assert line.startswith(f"imports: .: cannot read the CLI sources: ValueError: {table} in qsearch_cli/")
    if table == "ORDER":
        assert any(line.startswith("manifest: qsearch_cli/registry.py: cannot read ORDER: ValueError: ORDER") for line in lines)


def test_real_checkout_has_no_untracked_imports() -> None:
    assert pf.check_untracked_imports(REPO) == []


def test_without_git_reports_one_git_unavailable_problem(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    general = "def command_audit(args):\n    from theorems.tracked import a\n    return a\n"
    repo = _repo(tmp_path, general=general, committed={"theorems/tracked.py": "a = 1\n"}, git=False)

    assert pf.tracked_files(repo) is None
    assert pf.check_untracked_imports(repo) == [pf.Problem("imports", ".", "git unavailable")]


def test_tree_inside_an_unrelated_repository_is_git_unavailable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Say an exported tree unpacked inside a dotfiles repository: that repository tracks none of it.
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    outer = tmp_path / "home"
    _write(outer / "README", "outer\n")
    _git(outer, "init", "-q")
    _git(outer, "add", "README")
    _git(outer, "commit", "-qm", "outer")
    general = "def command_audit(args):\n    from theorems.tracked import a\n    return a\n"
    repo = _repo(outer / "export", general=general, committed={"theorems/tracked.py": "a = 1\n"}, git=False)

    assert pf.tracked_files(repo) is None
    assert pf.check_untracked_imports(repo) == [
        pf.Problem("imports", ".", "git unavailable: the root is not the top of a git work tree (git sees it as export/repo/)")
    ]


def test_git_variables_of_another_repository_are_ignored(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # A hook of another repository or worktree exports its own GIT_DIR and GIT_INDEX_FILE.
    other = _repo(tmp_path / "other")
    general = "def command_audit(args):\n    from theorems.tracked import a\n    return a\n"
    repo = _repo(tmp_path / "mine", general=general, committed={"theorems/tracked.py": "a = 1\n"})
    monkeypatch.setenv("GIT_DIR", str(other / ".git"))
    monkeypatch.setenv("GIT_INDEX_FILE", str(other / ".git" / "index"))

    assert pf.check_untracked_imports(repo) == []


def test_the_index_a_hook_of_this_checkout_commits_is_used(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # `git commit -a` or `git commit <paths>` runs the pre-commit hook with GIT_INDEX_FILE set to
    # the index it is about to commit, which can track more than .git/index does.
    general = "def command_audit(args):\n    from theorems.new import a\n    return a\n"
    repo = _repo(tmp_path, general=general)
    _write(repo / "theorems" / "new.py", "a = 1\n")
    next_index = repo / ".git" / "next-index-1.lock"
    next_index.write_bytes((repo / ".git" / "index").read_bytes())
    subprocess.run(
        ["git", "-C", str(repo), "add", "theorems/new.py"],
        env={**os.environ, "GIT_INDEX_FILE": str(next_index)},
        check=True,
    )
    assert [p.path for p in pf.check_untracked_imports(repo)] == ["theorems/new.py"]

    monkeypatch.setenv("GIT_DIR", str(repo / ".git"))
    monkeypatch.setenv("GIT_INDEX_FILE", ".git/next-index-1.lock")  # relative to the work tree, as git exports it

    assert pf.check_untracked_imports(repo) == []


def test_a_root_inside_a_checkout_is_named_as_such(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    # Say --root qsearch_cli by mistake: git works there, so "git unavailable" alone would mislead.
    repo = _repo(tmp_path)

    assert pf.check_untracked_imports(repo / "qsearch_cli") == [
        pf.Problem("imports", ".", "git unavailable: the root is not the top of a git work tree (git sees it as qsearch_cli/)")
    ]
    with pytest.raises(SystemExit) as exit_info:
        pf.main(["--root", str(repo / "qsearch_cli")])
    assert exit_info.value.code == 2
    assert "qsearch_cli is not a Q-Search checkout: it has no qsearch.py" in capsys.readouterr().err


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
        "imports: theorems/untracked.py: not tracked by git; referred to by qsearch_cli/commands/general.py",
        "1 problems",
    ]

    clean = _repo(tmp_path / "clean")
    assert pf.main(["--root", str(clean), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload == {"root": str(clean.resolve()), "problems": [], "count": 0}


def test_main_rejects_a_root_that_is_not_a_directory(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exit_info:
        pf.main(["--root", str(tmp_path / "no_such_checkout")])

    assert exit_info.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "no_such_checkout is not a directory" in captured.err


def test_validate_flag_reports_nonzero_exit(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    shim = 'import sys\nprint("checking", file=sys.stderr)\nprint("registry is broken", file=sys.stderr)\nsys.exit(3)\n'
    repo = _repo(tmp_path, committed={"qsearch.py": shim})

    assert pf.main(["--root", str(repo), "--json"]) == 0
    capsys.readouterr()
    assert pf.main(["--root", str(repo), "--validate", "--json"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["problems"] == [{"check": "validate", "path": "qsearch.py", "message": "exit 3: registry is broken"}]


def test_validate_reports_the_issues_printed_on_stdout(tmp_path: Path) -> None:
    # qsearch.py validate prints its report as JSON on stdout and exits 1 when it has issues.
    report = {
        "issues": [
            {"candidate_id": "CODE-X", "field": "falsifiers", "message": "Experiment EXP-1 has no falsifiers."},
            {"candidate_id": "CODE-Y", "field": "falsifiers", "message": "Experiment EXP-2 has no falsifiers."},
        ],
        "valid": False,
    }
    shim = f"import json, sys\nprint(json.dumps({report!r}, indent=2))\nsys.exit(1)\n"
    repo = _repo(tmp_path, committed={"qsearch.py": shim})

    assert pf.check_validate(repo) == [
        pf.Problem("validate", "qsearch.py", "exit 1: 2 issues, first: CODE-X: Experiment EXP-1 has no falsifiers.")
    ]

    (repo / "qsearch.py").write_text('print("registry unreadable")\nraise SystemExit(2)\n', encoding="utf-8")
    assert [p.message for p in pf.check_validate(repo)] == ["exit 2: registry unreadable"]

    (repo / "qsearch.py").write_text("raise SystemExit(4)\n", encoding="utf-8")
    assert [p.message for p in pf.check_validate(repo)] == ["exit 4: (no output)"]

    # A crash prints its reason on stderr, after whatever went to stdout: stderr wins.
    shim = 'import sys\nprint("loading the registry")\nprint("KeyError: id", file=sys.stderr)\nsys.exit(5)\n'
    (repo / "qsearch.py").write_text(shim, encoding="utf-8")
    assert [p.message for p in pf.check_validate(repo)] == ["exit 5: KeyError: id"]


def test_imports_flag_reports_a_verifier_that_cannot_start(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def broken_check_imports(root: Path) -> tuple[int, list[str]]:
        raise RuntimeError("qsearch_cli imported from another checkout")

    monkeypatch.setattr(pf, "_check_imports", broken_check_imports)

    assert pf.check_imports_resolve(tmp_path) == [
        pf.Problem("resolve", ".", "RuntimeError: qsearch_cli imported from another checkout")
    ]


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


def test_imports_flag_finds_a_tracked_module_that_fails_to_import(tmp_path: Path) -> None:
    # The real verifier, unpatched. It runs in a fresh process: it imports qsearch_cli from the
    # checked root, and refuses when this process already imported it from another checkout.
    repo = _repo(
        tmp_path,
        imports={"broken": ("theorems.broken_mod", "f"), "os": ("os", None)},
        committed={
            "qsearch_cli/resolve.py": (REPO / "qsearch_cli" / "resolve.py").read_text(encoding="utf-8"),
            "theorems/__init__.py": "",
            "theorems/broken_mod.py": "import qsearch_missing_dependency\n\nf = 1\n",
        },
    )

    result = subprocess.run(
        [sys.executable, str(REPO / "tools" / "preflight" / "preflight.py"), "--root", str(repo), "--imports", "--json"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1, result.stderr
    assert json.loads(result.stdout)["problems"] == [
        {
            "check": "resolve",
            "path": "qsearch_cli",
            "message": "broken: ModuleNotFoundError: No module named 'qsearch_missing_dependency'",
        }
    ]


def test_imports_flag_imports_every_certificate_flag_and_subcommand_adder(tmp_path: Path) -> None:
    # main.py imports a DISPATCH module only when its flag is given, and parser.py looks up
    # each ORDER adder: neither is an IMPORTS name or a command function.
    order = [("audit", "qsearch_cli.commands.general", "add_audti")]
    dispatch = [
        ("broken_cert", "theorems.broken_cert", "generate_broken_certificate"),
        ("misnamed_cert", "theorems.good_cert", "generate_misnamed_certificate"),
        ("good_cert", "theorems.good_cert", "generate_good_certificate"),
    ]
    repo = _repo(
        tmp_path,
        order=order,
        dispatch=dispatch,
        committed={
            "qsearch_cli/resolve.py": (REPO / "qsearch_cli" / "resolve.py").read_text(encoding="utf-8"),
            "theorems/__init__.py": "",
            "theorems/broken_cert.py": "import qsearch_missing_dependency\n",
            "theorems/good_cert.py": "def generate_good_certificate():\n    return {}\n",
        },
    )

    result = subprocess.run(
        [sys.executable, str(REPO / "tools" / "preflight" / "preflight.py"), "--root", str(repo), "--imports", "--json"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1, result.stderr
    assert [p["message"] for p in json.loads(result.stdout)["problems"] if p["check"] == "resolve"] == [
        "--broken-cert: ModuleNotFoundError: No module named 'qsearch_missing_dependency'",
        "--misnamed-cert: AttributeError: module 'theorems.good_cert' has no attribute 'generate_misnamed_certificate'",
        "subcommand audit: AttributeError: module 'qsearch_cli.commands.general' has no attribute 'add_audti'",
    ]
