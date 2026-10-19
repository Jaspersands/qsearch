from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.split_cli import extract as ex
from tools.split_cli import generate as gen

REPO = Path(__file__).resolve().parents[2]
MIGRATE = REPO / "tools" / "split_cli" / "migrate.py"

MONOLITH = '''"""Mini CLI.

Commands:
  python qsearch.py dcp-alpha
"""

from __future__ import annotations

import os
import sys

_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
_CORE_DIR = os.path.join(_ROOT_DIR, "core")
_THEOREMS_DIR = os.path.join(_ROOT_DIR, "theorems")

for _p in [_ROOT_DIR, _CORE_DIR, _THEOREMS_DIR]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from fake_mod import write_report
from fake_registry import initialize_seed_registry, validate_registry
import argparse
import json
from pathlib import Path


def command_dcp_alpha(args: argparse.Namespace) -> int:
    """Run alpha."""
    initialize_seed_registry(root=args.root)
    report = write_report(n=args.n)
    print(json.dumps(report, sort_keys=True))
    return 0


# Beta calls a theorem main and another command.
def command_code_beta(args: argparse.Namespace) -> int:
    from fake_mod import main
    return main([]) + command_dcp_alpha(args)


def command_sdw_orphan(args: argparse.Namespace) -> int:
    return len(validate_registry())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    subparsers = parser.add_subparsers(dest="command", required=True)

    alpha = subparsers.add_parser("dcp-alpha", help="Alpha.")
    alpha.add_argument("--n", type=int, default=3)
    alpha.set_defaults(func=command_dcp_alpha)

    beta = subparsers.add_parser("code-beta", aliases=["cb"], help="Beta.")
    beta.add_argument("--n", type=int, default=1)
    beta.add_argument("--out", type=Path, default=Path("x"))
    beta.set_defaults(func=command_code_beta)

    gamma = subparsers.add_parser(
        "dcp-gamma",
        help="Gamma shares alpha.",
    )
    gamma.add_argument("--n", type=int, default=5)
    gamma.set_defaults(func=command_dcp_alpha)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    parser.add_argument(
        "--cert-flag",
        action="store_true",
        help="Print the certificate.",
    )
    args = parser.parse_args(argv)
    if getattr(args, "cert_flag", False):
        from theorems.fake_cert import generate_cert
        print(json.dumps(generate_cert(), indent=2, sort_keys=True))
        return 0

    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

# Subsystem CLI hook: dcp-alpha -> theorems.fake_mod
'''

MODULES = {
    "theorems/__init__.py": "",
    "theorems/fake_mod.py": "def write_report(**kw):\n    return {'n': kw['n']}\n\ndef main(argv):\n    return 0\n",
    "theorems/fake_cert.py": "def generate_cert():\n    return {'cert': 1}\n",
    "theorems/fake_mod2.py": "def thing():\n    return 'delta'\n",
    "core/fake_registry.py": "def initialize_seed_registry(**kw):\n    return None\n\ndef validate_registry():\n    return []\n",
}


def _fixture(tmp_path: Path, source: str = MONOLITH) -> Path:
    (tmp_path / "qsearch.py").write_text(source)
    for rel, text in MODULES.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(text)
    return tmp_path


def _run(root: Path, *argv: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *argv], cwd=root, capture_output=True, text=True, timeout=120)


def test_extract_reads_imports_commands_blocks_and_flags() -> None:
    mono = ex.extract(MONOLITH)
    names = {b.name: b for b in mono.bindings}
    assert names["write_report"].module == "fake_mod" and names["write_report"].attr == "write_report"
    assert names["json"].stdlib and names["Path"].stdlib and not names["validate_registry"].stdlib
    commands = {c.name: c for c in mono.commands}
    assert list(commands) == ["command_dcp_alpha", "command_code_beta", "command_sdw_orphan"]
    assert commands["command_dcp_alpha"].lazy == ["initialize_seed_registry", "write_report"]
    assert commands["command_dcp_alpha"].stdlib == ["json"]
    assert commands["command_code_beta"].lazy == ["command_dcp_alpha"]  # main is bound locally
    assert commands["command_code_beta"].source.startswith("# Beta calls")
    assert [(b.subcommand, b.aliases, b.function) for b in mono.blocks] == [
        ("dcp-alpha", [], "command_dcp_alpha"),
        ("code-beta", ["cb"], "command_code_beta"),
        ("dcp-gamma", [], "command_dcp_alpha"),
    ]
    assert mono.dispatch == [("cert_flag", "theorems.fake_cert", "generate_cert")]
    assert '"--cert-flag"' in mono.flags_source
    assert "# Subsystem CLI hook: dcp-alpha" in mono.trailer
    assert mono.docstring.startswith("Mini CLI.")


def test_extract_refuses_statements_it_cannot_move() -> None:
    bad = MONOLITH.replace('    return parser\n', '    print("side effect")\n    return parser\n')
    with pytest.raises(ex.SplitError, match="build_parser"):
        ex.extract(bad)
    bad_main = MONOLITH.replace("    return args.func(args)", "    print(args)\n    return args.func(args)")
    with pytest.raises(ex.SplitError, match="main"):
        ex.extract(bad_main)


def test_extract_keeps_only_the_live_copy_of_a_redefined_command() -> None:
    twice = MONOLITH.replace("def command_sdw_orphan(", "def command_dcp_alpha(args: argparse.Namespace) -> int:\n"
                             "    return 99\n\n\ndef command_sdw_orphan(", 1)
    mono = ex.extract(twice)
    alphas = [c for c in mono.commands if c.name == "command_dcp_alpha"]
    assert len(alphas) == 1 and "return 99" in alphas[0].source
    assert mono.dropped == ["command_dcp_alpha"]


def test_domain_of_groups_by_command_prefix() -> None:
    assert gen.domain_of("command_dcp_alpha") == "dcp"
    assert gen.domain_of("command_code_beta") == "code"
    assert gen.domain_of("command_self_dual_wreath_x") == "self_dual_wreath"
    assert gen.domain_of("command_sdw_orphan") == "self_dual_wreath"
    assert gen.domain_of("command_native_y") == "native"
    assert gen.domain_of("command_validate") == "general"


def test_generated_function_gains_only_a_lazy_import_line() -> None:
    mono = ex.extract(MONOLITH)
    text = gen.render_domain("dcp", [c for c in mono.commands if c.name == "command_dcp_alpha"],
                             [b for b in mono.blocks if b.function == "command_dcp_alpha"], mono.bindings)
    assert '    """Run alpha."""\n    from qsearch import initialize_seed_registry, write_report\n' in text
    assert "import json\n" in text
    assert "def add_dcp_alpha(subparsers" in text and "def add_dcp_gamma(subparsers" in text
    compile(text, "dcp.py", "exec")


def test_cutover_matches_legacy_and_runs(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    legacy = root / "qsearch_legacy.py"
    legacy.write_text(MONOLITH)
    gen_out = _run(root, str(MIGRATE), "generate", "--root", str(root), "--shim")
    assert gen_out.returncode == 0, gen_out.stderr
    shim = (root / "qsearch.py").read_text()
    assert "def command_dcp_alpha" not in shim and "Mini CLI." in shim and "# Subsystem CLI hook: dcp-alpha" in shim
    check = _run(root, str(MIGRATE), "verify", "--root", str(root), "--legacy", str(legacy))
    assert check.returncode == 0, check.stdout + check.stderr
    assert "0 problems" in check.stdout
    ran = _run(root, "qsearch.py", "dcp-alpha", "--n", "4")
    assert ran.returncode == 0, ran.stderr
    assert json.loads(ran.stdout) == {"n": 4}
    flag = _run(root, "qsearch.py", "--cert-flag", "dcp-alpha")
    assert json.loads(flag.stdout) == {"cert": 1}
    alias = _run(root, "qsearch.py", "cb")
    assert alias.returncode == 0, alias.stderr
    manifest = json.loads((root / "research/audits/cli_manifest.json").read_text())
    assert [c["name"] for c in manifest["subcommands"]] == ["dcp-alpha", "code-beta", "dcp-gamma"]


def test_verify_reports_a_changed_default(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    legacy = root / "qsearch_legacy.py"
    legacy.write_text(MONOLITH)
    assert _run(root, str(MIGRATE), "generate", "--root", str(root), "--shim").returncode == 0
    dcp = root / "qsearch_cli/commands/dcp.py"
    dcp.write_text(dcp.read_text().replace("default=3", "default=4"))
    check = _run(root, str(MIGRATE), "verify", "--root", str(root), "--legacy", str(legacy))
    assert check.returncode == 1 and "dcp-alpha" in check.stdout


def test_shim_keeps_identity_monkeypatching_and_lazy_startup(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    assert _run(root, str(MIGRATE), "generate", "--root", str(root), "--shim").returncode == 0
    probe = (
        "import sys, io, contextlib, argparse\n"
        "import qsearch\n"
        "p = qsearch.build_parser()\n"
        "assert 'fake_mod' not in sys.modules, 'theorem module imported at startup'\n"
        "a = p.parse_args(['dcp-alpha'])\n"
        "assert a.func is qsearch.command_dcp_alpha\n"
        "from qsearch import command_sdw_orphan\n"
        "assert command_sdw_orphan(a) == 0\n"
        "qsearch.write_report = lambda **kw: {'patched': True}\n"
        "out = io.StringIO()\n"
        "with contextlib.redirect_stdout(out):\n"
        "    qsearch.command_dcp_alpha(argparse.Namespace(root='.', n=1))\n"
        "assert 'patched' in out.getvalue(), out.getvalue()\n"
        "print('ok')\n"
    )
    result = _run(root, "-c", probe)
    assert result.returncode == 0 and result.stdout.strip() == "ok", result.stderr


def test_real_cli_starts_without_importing_theorem_modules() -> None:
    probe = (
        "import sys, argparse, qsearch\n"
        "parser = qsearch.build_parser()\n"
        "heavy = [m for m, v in sys.modules.items() if '/theorems/' in str(getattr(v, '__file__', ''))]\n"
        "sub = next(a for a in parser._actions if isinstance(a, argparse._SubParsersAction))\n"
        "print(len(heavy), len(sub.choices))\n"
    )
    result = _run(REPO, "-c", probe)
    assert result.returncode == 0, result.stderr
    heavy, names = map(int, result.stdout.split())
    assert heavy == 0
    manifest = json.loads((REPO / gen.MANIFEST).read_text())
    assert names >= len(manifest["subcommands"]) + sum(len(s["aliases"]) for s in manifest["subcommands"])


def test_every_real_subcommand_renders_its_help_page() -> None:
    # argparse only formats help lazily, so a bad help string (a stray "%") fails here, not at build time.
    probe = (
        "import sys, argparse, qsearch\n"
        "parser = qsearch.build_parser()\n"
        "parser.format_help()\n"
        "sub = next(a for a in parser._actions if isinstance(a, argparse._SubParsersAction))\n"
        "for name, page in sub.choices.items():\n"
        "    assert page.format_help().startswith('usage:'), name\n"
        "heavy = [m for m, v in sys.modules.items() if '/theorems/' in str(getattr(v, '__file__', ''))]\n"
        "print(len(sub.choices), len(heavy))\n"
    )
    result = _run(REPO, "-c", probe)
    assert result.returncode == 0, result.stderr[-2000:]
    rendered, heavy = map(int, result.stdout.split())
    assert rendered > 800
    assert heavy == 0


def test_real_registry_keeps_every_migrated_subcommand() -> None:
    # New subcommands may be added after the migration; none of the migrated ones may vanish.
    sys.path.insert(0, str(REPO))
    from qsearch_cli import registry

    manifest = json.loads((REPO / gen.MANIFEST).read_text())
    order = {n: (m, a) for n, m, a in registry.ORDER}
    assert len(order) == len(registry.ORDER), "duplicate subcommand in ORDER"
    for entry in manifest["subcommands"]:
        assert order.get(entry["name"], (None,))[0] == entry["module"], entry["name"]
    assert len(registry.FUNCTIONS) >= manifest["functions"]
    import importlib

    for name, module, adder in registry.ORDER:
        assert module.startswith("qsearch_cli.commands."), name
        assert callable(getattr(importlib.import_module(module), adder, None)), f"{name}: {module}.{adder} missing"
    for function, module in registry.FUNCTIONS.items():
        assert callable(getattr(importlib.import_module(module), function, None)), f"{module}.{function} missing"


def test_sweep_moves_legacy_style_additions(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    assert _run(root, str(MIGRATE), "generate", "--root", str(root), "--shim").returncode == 0
    shim = root / "qsearch.py"
    text = shim.read_text()
    text = text.replace("def _legacy_extensions(subparsers", "from fake_mod2 import thing\n\n\n"
                        "def command_dcp_delta(args):\n    print(thing())\n    return 0\n\n\n"
                        "def _legacy_extensions(subparsers", 1)
    text = text.replace("    pass  # legacy-extensions\n",
                        '    delta = subparsers.add_parser("dcp-delta", help="Delta.")\n'
                        "    delta.set_defaults(func=command_dcp_delta)\n", 1)
    shim.write_text(text)
    before = _run(root, "qsearch.py", "dcp-delta")
    assert before.returncode == 0 and before.stdout.strip() == "delta", before.stderr
    swept = _run(root, str(MIGRATE), "sweep", "--root", str(root))
    assert swept.returncode == 0, swept.stderr
    assert "command_dcp_delta" not in shim.read_text() and "fake_mod2" not in shim.read_text()
    assert "def command_dcp_delta" in (root / "qsearch_cli/commands/dcp.py").read_text()
    after = _run(root, "qsearch.py", "dcp-delta")
    assert after.returncode == 0 and after.stdout.strip() == "delta", after.stderr
    listing = _run(root, "qsearch.py", "--help")
    assert listing.stdout.index("dcp-gamma") < listing.stdout.index("dcp-delta")


# ---- old-style code in the shim, dispatch, and the shim's module behaviour ----------------

SHIM_ANCHOR = "def _legacy_extensions(subparsers"


def _generated(tmp_path: Path, source: str = MONOLITH) -> Path:
    root = _fixture(tmp_path, source)
    out = _run(root, str(MIGRATE), "generate", "--root", str(root), "--shim")
    assert out.returncode == 0, out.stdout + out.stderr
    return root


def _add_old_style(shim: Path, top: str = "", parser_lines: str = "") -> None:
    """Edit the shim the way the monolith used to be edited: code above, add_parser lines inside."""
    text = shim.read_text()
    assert SHIM_ANCHOR in text and gen.LEGACY_SENTINEL in text
    if top:
        text = text.replace(SHIM_ANCHOR, top.rstrip("\n") + "\n\n\n" + SHIM_ANCHOR, 1)
    if parser_lines:
        text = text.replace(gen.LEGACY_SENTINEL + "\n", parser_lines, 1)
    shim.write_text(text)


OLD_STYLE_TOP = '''def command_dcp_old(args: argparse.Namespace) -> int:
    report = {"n": args.n, "out": str(args.out), "valid": validate_registry() == []}
    print(json.dumps(report, sort_keys=True))
    return command_sdw_orphan(args)
'''
OLD_STYLE_PARSER = '''    old = subparsers.add_parser("dcp-old", help="Old style.")
    old.add_argument("--n", type=int, default=2)
    old.add_argument("--out", type=Path, default=Path("o"))
    old.set_defaults(func=command_dcp_old)
'''


def test_old_style_code_in_the_shim_reads_former_monolith_globals(tmp_path: Path) -> None:
    # json, Path, validate_registry and command_sdw_orphan were globals of the monolith. The
    # shim's __getattr__ is never consulted for a global lookup inside the shim itself.
    root = _generated(tmp_path)
    _add_old_style(root / "qsearch.py", OLD_STYLE_TOP, OLD_STYLE_PARSER)
    listing = _run(root, "qsearch.py", "--help")
    assert listing.returncode == 0 and "dcp-old" in listing.stdout, listing.stderr
    ran = _run(root, "qsearch.py", "dcp-old", "--n", "5")
    assert ran.returncode == 0, ran.stderr
    assert json.loads(ran.stdout) == {"n": 5, "out": "o", "valid": True}
    other = _run(root, "qsearch.py", "dcp-alpha")
    assert other.returncode == 0 and json.loads(other.stdout) == {"n": 3}, other.stderr
    probe = (
        "import argparse, sys, qsearch\n"
        "assert qsearch.command_dcp_old(argparse.Namespace(n=1, out='x', root='.')) == 0\n"
        "assert 'fake_mod' not in sys.modules\n"
        "print('ok')\n"
    )
    result = _run(root, "-c", probe)
    assert result.returncode == 0 and result.stdout.strip().endswith("ok"), result.stderr


def test_an_empty_legacy_section_binds_and_imports_nothing(tmp_path: Path) -> None:
    root = _generated(tmp_path)
    probe = (
        "import sys, qsearch\n"
        "names = set(vars(qsearch))\n"
        "assert not names & {'json', 'Path', 'validate_registry', 'write_report'}, names\n"
        "assert 'qsearch_cli.imports' not in sys.modules and 'dis' not in sys.modules\n"
        "print('ok')\n"
    )
    result = _run(root, "-c", probe)
    assert result.returncode == 0 and result.stdout.strip() == "ok", result.stderr


# Third-party packages that resolving every name in qsearch_cli/imports.py loads. ci-fast
# installs only pytest and tools.yml has no networkx, so tests that need them skip there;
# ci-full installs requirements.txt and runs them.
RESEARCH_DEPS = ("numpy", "scipy", "sympy", "networkx", "flint")


def _needs_research_deps() -> None:
    for module in RESEARCH_DEPS:
        pytest.importorskip(module)


def _real_shim_copy(tmp_path: Path) -> Path:
    """A copy of the real shim next to links to the real package and research code."""
    work = tmp_path / "cli"
    work.mkdir()
    (work / "qsearch.py").write_text((REPO / "qsearch.py").read_text())
    for name in ("qsearch_cli", "core", "theorems"):
        (work / name).symlink_to(REPO / name, target_is_directory=True)
    return work


VALIDATE_AGAIN_TOP = '''def command_validate_again(args: argparse.Namespace) -> int:
    validation = validate_registry()
    print(json.dumps(validation, indent=2, sort_keys=True))
    return 0 if validation["valid"] else 1
'''
VALIDATE_AGAIN_PARSER = '''    validate_again = subparsers.add_parser("validate-again", help="Validate again.")
    validate_again.add_argument("--output-dir", type=Path, default=Path("research"))
    validate_again.set_defaults(func=command_validate_again)
'''


def test_real_shim_runs_an_old_style_copy_of_validate(tmp_path: Path) -> None:
    # Runs in an empty directory, so nothing is read from or written to the real research/.
    work = _real_shim_copy(tmp_path)
    _add_old_style(work / "qsearch.py", VALIDATE_AGAIN_TOP, VALIDATE_AGAIN_PARSER)
    listing = _run(work, "qsearch.py", "--help")
    assert listing.returncode == 0 and "validate-again" in listing.stdout, listing.stderr[-2000:]
    original = _run(work, "qsearch.py", "validate")
    again = _run(work, "qsearch.py", "validate-again")
    assert again.stderr == "" and original.stderr == "", again.stderr[-2000:]
    assert (again.returncode, again.stdout) == (original.returncode, original.stdout)


DIGEST_IMPORT = "from dcp_label_digest_audit import write_digest_audit_report\n"
DIGEST_TOP = '''def command_dcp_label_digest_audit_again(args: argparse.Namespace) -> int:
    initialize_seed_registry(overwrite=False)
    report = write_digest_audit_report()
    print(report["summary"])
    print(json.dumps(report["headline_metrics"], indent=2))
    valid = validate_registry()["valid"]
    print(f"Registry valid: {valid}")
    return 0 if valid and report["claim_gate"]["finite_controls_passed"] is True else 1
'''


@pytest.mark.parametrize("typed", [False, True], ids=["plain", "type-path"])
def test_real_shim_runs_the_reviewers_old_style_digest_audit(tmp_path: Path, typed: bool) -> None:
    # The reviewer's legacy_test/ and legacy_test2/: a real monolith command, its import and
    # its add_parser lines, copied into the shim the old way. Runs in an empty directory.
    _needs_research_deps()
    work = _real_shim_copy(tmp_path)
    parser_lines = (
        "    again = subparsers.add_parser(\n"
        '        "dcp-label-digest-audit-again",\n'
        '        help="Audit again.",\n'
        "    )\n"
        + ('    again.add_argument("--output-dir", type=Path, default=Path("research"))\n' if typed else "")
        + "    again.set_defaults(func=command_dcp_label_digest_audit_again)\n"
    )
    _add_old_style(work / "qsearch.py", DIGEST_IMPORT + "\n\n" + DIGEST_TOP, parser_lines)
    for argv in (["--help"], ["validate"], ["dcp-label-digest-audit-again"]):
        result = _run(work, "qsearch.py", *argv)
        assert "Traceback" not in result.stderr, (argv, result.stderr[-2000:])
        assert result.returncode in (0, 1), (argv, result.stderr[-2000:])
        if argv[0] == "dcp-label-digest-audit-again":
            assert "Registry valid:" in result.stdout


def test_cli_runs_under_cprofile_and_trace(tmp_path: Path) -> None:
    root = _generated(tmp_path)
    profiled = _run(root, "-m", "cProfile", "-o", str(tmp_path / "prof.out"), "qsearch.py", "dcp-alpha", "--n", "4")
    assert profiled.returncode == 0, profiled.stderr
    assert json.loads(profiled.stdout) == {"n": 4}
    traced = _run(root, "-m", "trace", "--trackcalls", "qsearch.py", "dcp-alpha", "--n", "6")
    assert traced.returncode == 0, traced.stderr
    assert traced.stdout.splitlines()[0] == '{"n": 6}'


def test_dispatch_follows_patches_and_old_style_redefinitions(tmp_path: Path) -> None:
    root = _generated(tmp_path)
    probe = (
        "import qsearch\n"
        "calls = []\n"
        "qsearch.command_dcp_alpha = lambda args: calls.append(args.command) or 42\n"
        "assert qsearch.main(['dcp-alpha']) == 42 and calls == ['dcp-alpha'], calls\n"
        "del qsearch.command_dcp_alpha\n"
        "args = qsearch.build_parser().parse_args(['dcp-alpha'])\n"
        "assert args.func is qsearch.command_dcp_alpha\n"
        "print('ok')\n"
    )
    result = _run(root, "-c", probe)
    assert result.returncode == 0 and result.stdout.strip() == "ok", result.stderr
    # In the monolith a later definition of a command replaced the earlier one.
    _add_old_style(root / "qsearch.py", 'def command_dcp_alpha(args) -> int:\n    print("PATCHED")\n    return 0\n')
    ran = _run(root, "qsearch.py", "dcp-alpha")
    assert ran.returncode == 0 and ran.stdout.strip() == "PATCHED", ran.stderr


def test_shim_restores_the_monoliths_int_digit_limit(tmp_path: Path) -> None:
    # theorems/coset_typical_modular_gap_bound.py raises it at import, and the monolith
    # imported that module for every command.
    assert "sys.set_int_max_str_digits(100_000)" in (REPO / "theorems/coset_typical_modular_gap_bound.py").read_text()
    root = _generated(tmp_path)
    probe = "import sys, qsearch\nprint(sys.get_int_max_str_digits(), len(str(10 ** 5000)))\n"
    for where in (root, REPO):
        result = _run(where, "-c", probe)
        assert result.returncode == 0, result.stderr
        assert result.stdout.split() == ["100000", "5001"]
        assert "coset_typical_modular_gap_bound" not in result.stderr


def test_qsearch_attributes_follow_the_source_module_without_caching(tmp_path: Path) -> None:
    # A lookup during a patch of the source module must not pin the fake after the patch ends.
    root = _generated(tmp_path)
    probe = (
        "import pytest, qsearch, fake_registry\n"
        "real = fake_registry.validate_registry\n"
        "mp = pytest.MonkeyPatch()\n"
        "fake = lambda: ['fake']\n"
        "mp.setattr(fake_registry, 'validate_registry', fake)\n"
        "assert qsearch.validate_registry is fake\n"
        "mp.undo()\n"
        "assert qsearch.validate_registry is real\n"
        "mp.setattr(qsearch, 'validate_registry', fake)\n"
        "assert qsearch.validate_registry is fake\n"
        "mp.undo()\n"
        "assert qsearch.validate_registry is real\n"
        "print('ok')\n"
    )
    result = _run(root, "-c", probe)
    assert result.returncode == 0 and result.stdout.strip() == "ok", result.stderr


def test_missing_names_raise_clear_errors(tmp_path: Path) -> None:
    root = _generated(tmp_path)
    mod = root / "theorems/fake_mod.py"
    mod.write_text(mod.read_text().replace("def write_report(", "def write_report_v2("))
    probe = (
        "import qsearch\n"
        "assert hasattr(qsearch, 'no_such_name') is False\n"
        "assert getattr(qsearch, 'no_such_name', 7) == 7\n"
        "for how in ('attribute', 'from-import'):\n"
        "    try:\n"
        "        if how == 'attribute':\n"
        "            qsearch.write_report\n"
        "        else:\n"
        "            from qsearch import write_report\n"
        "    except ImportError as error:\n"
        "        assert type(error) is ImportError, type(error)\n"
        "        assert \"'write_report'\" in str(error) and \"'fake_mod'\" in str(error), str(error)\n"
        "    else:\n"
        "        raise AssertionError(how)\n"
        "print('ok')\n"
    )
    result = _run(root, "-c", probe)
    assert result.returncode == 0 and result.stdout.strip() == "ok", result.stderr


# ---- generate and sweep must not lose work ------------------------------------------------

DELTA_TOP = "from fake_mod2 import thing\n\n\ndef command_dcp_delta(args):\n    print(thing())\n    return 0\n"
DELTA_PARSER = '    delta = subparsers.add_parser("dcp-delta", help="Delta.")\n    delta.set_defaults(func=command_dcp_delta)\n'


def test_generate_refuses_to_drop_commands_its_source_lacks(tmp_path: Path) -> None:
    # Re-running generate from a monolith would delete a command added after the split.
    root = _generated(tmp_path)
    legacy = root / "qsearch_legacy.py"
    legacy.write_text(MONOLITH)
    _add_old_style(root / "qsearch.py", DELTA_TOP, DELTA_PARSER)
    assert _run(root, str(MIGRATE), "sweep", "--root", str(root)).returncode == 0
    registry = (root / "qsearch_cli/registry.py").read_text()
    again = _run(root, str(MIGRATE), "generate", "--root", str(root), "--source", str(legacy), "--shim")
    assert again.returncode == 2, again.stdout + again.stderr
    assert "dcp-delta" in again.stderr and "command_dcp_delta" in again.stderr and "--force" in again.stderr
    assert (root / "qsearch_cli/registry.py").read_text() == registry
    assert _run(root, "qsearch.py", "dcp-delta").stdout.strip() == "delta"
    forced = _run(root, str(MIGRATE), "generate", "--root", str(root), "--source", str(legacy), "--shim", "--force")
    assert forced.returncode == 0, forced.stderr
    assert "dcp-delta" not in (root / "qsearch_cli/registry.py").read_text()


def test_sweep_carries_the_imports_a_parser_block_needs(tmp_path: Path) -> None:
    # The reviewer's legacy_test3/: sweep exited 0 and every command then failed with NameError.
    root = _generated(tmp_path)
    (root / "theorems/fake_sizes.py").write_text("def parse_sizes(text):\n    return [int(x) for x in text.split(',')]\n")
    top = (
        "from fake_sizes import parse_sizes\n\n\n"
        "def command_dcp_sizes_echo(args) -> int:\n"
        "    print(json.dumps([args.sizes, str(args.out)]))\n"
        "    return 0\n"
    )
    parser_lines = (
        '    echo = subparsers.add_parser("dcp-sizes-echo", help="Echo sizes.")\n'
        "    echo.add_argument(\"--sizes\", type=parse_sizes, default=[3, 5])\n"
        '    echo.add_argument("--out", type=Path, default=Path("x"))\n'
        "    echo.set_defaults(func=command_dcp_sizes_echo)\n"
    )
    _add_old_style(root / "qsearch.py", top, parser_lines)
    before = _run(root, "qsearch.py", "dcp-sizes-echo", "--sizes", "1,2")
    assert before.returncode == 0 and json.loads(before.stdout) == [[1, 2], "x"], before.stderr
    swept = _run(root, str(MIGRATE), "sweep", "--root", str(root))
    assert swept.returncode == 0, swept.stderr
    assert "fake_sizes" not in (root / "qsearch.py").read_text()
    for argv in (["dcp-sizes-echo", "--sizes", "1,2"], ["dcp-alpha"], ["--help"]):
        after = _run(root, "qsearch.py", *argv)
        assert after.returncode == 0, (argv, after.stderr)
    assert _run(root, "qsearch.py", "dcp-sizes-echo", "--sizes", "1,2").stdout == before.stdout


def test_sweep_keeps_commands_that_read_the_shims_own_globals(tmp_path: Path) -> None:
    root = _generated(tmp_path)
    top = "def command_dcp_where(args) -> int:\n    print(_ROOT_DIR, Path(__file__).name, __doc__.splitlines()[0])\n    return 0\n"
    parser_lines = '    where = subparsers.add_parser("dcp-where", help="Where.")\n    where.set_defaults(func=command_dcp_where)\n'
    _add_old_style(root / "qsearch.py", top, parser_lines)
    before = _run(root, "qsearch.py", "dcp-where")
    assert before.returncode == 0 and before.stdout.split() == [str(root), "qsearch.py", "Mini", "CLI."], before.stderr
    swept = _run(root, str(MIGRATE), "sweep", "--root", str(root))
    assert swept.returncode == 0, swept.stderr
    after = _run(root, "qsearch.py", "dcp-where")
    assert (after.returncode, after.stdout) == (0, before.stdout), after.stderr


SWEEP_REFUSALS = {
    "main": ("    return run(argv, build_parser())\n", '    print("hi")\n    return run(argv, build_parser())\n'),
    "build_parser": ("extend=_legacy_extensions)\n", "extend=_legacy_extensions)  # edited\n    pass\n"),
    "__getattr__": ("    return resolve(name)\n", "    print(name)\n    return resolve(name)\n"),
    "for loop": (SHIM_ANCHOR, "for _x in []:\n    pass\n\n\n" + SHIM_ANCHOR),
    "assignment": (SHIM_ANCHOR, "LIMIT = 3\n\n\n" + SHIM_ANCHOR),
    "helper": (SHIM_ANCHOR, "def helper():\n    return 1\n\n\n" + SHIM_ANCHOR),
    "path loop": ("        sys.path.insert(0, _p)\n", "        sys.path.append(_p)\n"),
    "__main__ block": ("    raise SystemExit(qsearch.main())\n", '    print("BANNER")\n    raise SystemExit(qsearch.main())\n'),
    "loop variable": (SHIM_ANCHOR, "def command_dcp_p(args):\n    return len(_p)\n\n\n" + SHIM_ANCHOR),
    "code after __main__": ("    raise SystemExit(qsearch.main())\n", "    raise SystemExit(qsearch.main())\n\n\ndef command_dcp_late(args):\n    return 0\n"),
}


@pytest.mark.parametrize("edit", sorted(SWEEP_REFUSALS))
def test_sweep_refuses_shim_edits_it_would_drop(tmp_path: Path, edit: str) -> None:
    root = _generated(tmp_path)
    shim = root / "qsearch.py"
    old, new = SWEEP_REFUSALS[edit]
    text = shim.read_text()
    assert old in text, edit
    shim.write_text(text.replace(old, new, 1))
    before = {p: p.read_text() for p in [shim, *sorted((root / "qsearch_cli").rglob("*.py"))]}
    swept = _run(root, str(MIGRATE), "sweep", "--root", str(root))
    assert swept.returncode == 2, (edit, swept.stdout, swept.stderr)
    assert "line " in swept.stderr, swept.stderr
    assert {p: p.read_text() for p in before} == before


# ---- checks: imports, legacy module globals, exact shapes, flag dispatch ------------------

def test_check_imports_reports_a_broken_import(tmp_path: Path) -> None:
    # The monolith imported every name at start, so `python qsearch.py validate` caught a
    # renamed theorem function. The shim imports lazily; check-imports does it on purpose.
    root = _generated(tmp_path)
    ok = _run(root, str(MIGRATE), "check-imports", "--root", str(root))
    assert ok.returncode == 0 and "0 of " in ok.stdout, ok.stdout + ok.stderr
    mod = root / "theorems/fake_mod.py"
    mod.write_text(mod.read_text().replace("def write_report(", "def write_report_v2("))
    broken = _run(root, str(MIGRATE), "check-imports", "--root", str(root))
    assert broken.returncode == 1, broken.stdout + broken.stderr
    assert "write_report" in broken.stdout and "'fake_mod'" in broken.stdout and "1 of " in broken.stdout


def test_every_real_import_and_command_function_resolves() -> None:
    _needs_research_deps()
    result = _run(REPO, str(MIGRATE), "check-imports", "--root", str(REPO))
    assert result.returncode == 0, result.stdout[-3000:] + result.stderr[-3000:]
    assert result.stdout.strip().splitlines()[-1].startswith("0 of ")


GLOBALS_MONOLITH = (
    MONOLITH.replace(
        '    print(json.dumps(report, sort_keys=True))\n    return 0',
        '    report["out"] = str(Path(__file__).resolve().parent / "research")\n'
        '    print(json.dumps(report, sort_keys=True))\n    return 0', 1)
    .replace("def command_sdw_orphan(args: argparse.Namespace) -> int:\n    return len(validate_registry())",
             "def command_sdw_orphan(args: argparse.Namespace) -> int:\n    print(_ROOT_DIR)\n    return len(validate_registry())")
    .replace("    gamma.set_defaults(func=command_dcp_alpha)",
             "    gamma.set_defaults(func=command_dcp_alpha)\n\n"
             '    orphan = subparsers.add_parser("sdw-orphan", help="Orphan.")\n'
             "    orphan.set_defaults(func=command_sdw_orphan)")
)


def test_moved_commands_keep_reading_the_monoliths_path_globals(tmp_path: Path) -> None:
    # The reviewer's gapfix2/: commands reading __file__ and _ROOT_DIR. The shim keeps both,
    # so a moved command imports them from qsearch, and verify flags any read it does not cover.
    assert GLOBALS_MONOLITH.count("__file__") == 2 and "print(_ROOT_DIR)" in GLOBALS_MONOLITH
    root = _fixture(tmp_path, GLOBALS_MONOLITH)
    legacy = root / "qsearch_legacy.py"
    legacy.write_text(GLOBALS_MONOLITH)
    old = {argv: _run(root, "qsearch_legacy.py", argv) for argv in ("dcp-alpha", "sdw-orphan")}
    assert _run(root, str(MIGRATE), "generate", "--root", str(root), "--shim").returncode == 0
    check = _run(root, str(MIGRATE), "verify", "--root", str(root), "--legacy", str(legacy))
    assert check.returncode == 0 and "0 problems" in check.stdout, check.stdout + check.stderr
    for argv, before in old.items():
        after = _run(root, "qsearch.py", argv)
        assert (after.returncode, after.stdout) == (before.returncode, before.stdout), after.stderr
    sdw = root / "qsearch_cli/commands/self_dual_wreath.py"
    dcp = root / "qsearch_cli/commands/dcp.py"
    sdw.write_text(sdw.read_text().replace("from qsearch import _ROOT_DIR, validate_registry", "from qsearch import validate_registry"))
    dcp.write_text(dcp.read_text().replace("from qsearch import __file__, ", "from qsearch import "))
    check = _run(root, str(MIGRATE), "verify", "--root", str(root), "--legacy", str(legacy))
    assert check.returncode == 1, check.stdout
    assert "command_sdw_orphan reads legacy module global _ROOT_DIR" in check.stdout, check.stdout
    assert "command_dcp_alpha reads legacy module global __file__" in check.stdout, check.stdout


@pytest.mark.parametrize("name", ["_p", "__name__"])
def test_extract_refuses_commands_reading_other_module_globals(name: str) -> None:
    source = MONOLITH.replace("    return len(validate_registry())", f"    print({name})\n    return len(validate_registry())")
    with pytest.raises(ex.SplitError, match=f"line \\d+: command_sdw_orphan reads module global {name}"):
        ex.extract(source)


EXTRACT_SHAPES = {
    "__main__ block": ('if __name__ == "__main__":\n    raise SystemExit(main())',
                       'if __name__ == "__main__":\n    sys.setrecursionlimit(54321)\n    print("BANNER")\n    raise SystemExit(main())'),
    "sys.path loop": ("        sys.path.insert(0, _p)", "        sys.path.append(_p)"),
    "_CORE_DIR assignment": ('_CORE_DIR = os.path.join(_ROOT_DIR, "core")', '_CORE_DIR = os.path.join(_ROOT_DIR, "lib")'),
    "after __main__": ("# Subsystem CLI hook: dcp-alpha", "print('late')\n# Subsystem CLI hook: dcp-alpha"),
}


@pytest.mark.parametrize("edit", sorted(EXTRACT_SHAPES))
def test_extract_refuses_changed_framework_statements(tmp_path: Path, edit: str) -> None:
    # The reviewer's gapfix/: these bodies used to be matched by their header and dropped.
    old, new = EXTRACT_SHAPES[edit]
    assert old in MONOLITH
    source = MONOLITH.replace(old, new, 1)
    with pytest.raises(ex.SplitError, match=r"line \d+"):
        ex.extract(source)
    root = _fixture(tmp_path, source)
    refused = _run(root, str(MIGRATE), "generate", "--root", str(root), "--shim")
    assert refused.returncode == 2 and "line " in refused.stderr, refused.stdout + refused.stderr
    assert not (root / "qsearch_cli").exists()


TWO_FLAGS = MONOLITH.replace(
    "    args = parser.parse_args(argv)\n",
    '    parser.add_argument("--other-flag", action="store_true", help="Other.")\n'
    "    args = parser.parse_args(argv)\n"
    '    if getattr(args, "other_flag", False):\n'
    "        from theorems.fake_cert import generate_other\n"
    "        print(json.dumps(generate_other(), indent=2, sort_keys=True))\n"
    "        return 0\n", 1)


@pytest.mark.parametrize("edit", ["order", "function", "module"])
def test_verify_compares_flag_dispatch_with_the_legacy_main(tmp_path: Path, edit: str) -> None:
    root = _fixture(tmp_path, TWO_FLAGS)
    legacy = root / "qsearch_legacy.py"
    legacy.write_text(TWO_FLAGS)
    assert _run(root, str(MIGRATE), "generate", "--root", str(root), "--shim").returncode == 0
    clean = _run(root, str(MIGRATE), "verify", "--root", str(root), "--legacy", str(legacy))
    assert clean.returncode == 0, clean.stdout
    registry = root / "qsearch_cli/registry.py"
    text = registry.read_text()
    first = '    ("other_flag", "theorems.fake_cert", "generate_other"),\n'
    second = '    ("cert_flag", "theorems.fake_cert", "generate_cert"),\n'
    assert first + second in text
    changed = {
        "order": second + first,
        "function": first + second.replace('"generate_cert"', '"generate_cert_v2"'),
        "module": first + second.replace('"theorems.fake_cert"', '"theorems.fake_mod"'),
    }[edit]
    registry.write_text(text.replace(first + second, changed))
    check = _run(root, str(MIGRATE), "verify", "--root", str(root), "--legacy", str(legacy))
    assert check.returncode == 1 and "DISPATCH" in check.stdout, check.stdout


def test_real_package_framework_files_match_the_generator() -> None:
    pkg = REPO / gen.PACKAGE
    assert (pkg / "resolve.py").read_text() == gen.RESOLVE
    assert (pkg / "legacy.py").read_text() == gen.LEGACY
    assert (pkg / "__init__.py").read_text() == gen.INIT
    shim = (REPO / "qsearch.py").read_text()
    assert gen.SHIM.split("{docstring}")[1].split("{sentinel}")[0].split("def _legacy_extensions")[0] in shim


def test_old_wiring_scripts_find_no_anchor_in_the_shim() -> None:
    # tools/wire_pass5_experiments.py, tools/wire_pass6_experiments.py and
    # scratch/wire_generic_batch.py edit qsearch.py by str.replace/find on monolith lines.
    # Restoring those lines would let them add eager theorem imports and handlers with no
    # subcommand (pass 6's subcommand anchor never matched even the monolith), so the shim
    # keeps none of them and pass 5/6 leave it unchanged. See tools/split_cli/README.md.
    shim = (REPO / "qsearch.py").read_text()
    anchors = [
        "from research_registry import (",
        "def build_parser() -> argparse.ArgumentParser:",
        "    reduction_contracts = subparsers.add_parser(",
        "import argparse",
        "def command_audit(args: argparse.Namespace) -> int:",
        '    subparsers = parser.add_subparsers(dest="command")',
        "from blocker_taxonomy import write_blocker_taxonomy",
        "def command_coset_strong_fourier_information(",
        "    coset_strong_fourier_information = subparsers.add_parser(",
    ]
    assert [a for a in anchors if a in shim] == []
