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
