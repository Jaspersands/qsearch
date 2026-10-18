"""Split qsearch.py into the qsearch_cli package, check the split, and sweep later additions.

    python tools/split_cli/migrate.py generate --root . [--source FILE] [--shim]
    python tools/split_cli/migrate.py verify --root . [--legacy FILE]
    python tools/split_cli/migrate.py sweep --root .

``generate`` reads a monolithic qsearch.py (by default the one in --root) and writes
qsearch_cli/ plus research/audits/cli_manifest.json; with --shim it also replaces
qsearch.py with the short shim. ``verify`` compares the package against a legacy source.
``sweep`` moves old-style additions from the shim's legacy section into qsearch_cli/.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools.split_cli import extract as ex  # noqa: E402
from tools.split_cli import generate as gen  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    g = sub.add_parser("generate", help="Write qsearch_cli/ (and with --shim, the qsearch.py shim).")
    g.add_argument("--root", type=Path, default=Path("."))
    g.add_argument("--source", type=Path, help="monolithic qsearch.py to split (default: ROOT/qsearch.py)")
    g.add_argument("--shim", action="store_true", help="also replace ROOT/qsearch.py with the shim")
    v = sub.add_parser("verify", help="Compare qsearch_cli/ with a legacy monolithic qsearch.py.")
    v.add_argument("--root", type=Path, default=Path("."))
    v.add_argument("--legacy", type=Path, help="legacy qsearch.py (default: ROOT/qsearch.py)")
    s = sub.add_parser("sweep", help="Move old-style additions from the shim into qsearch_cli/.")
    s.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args(argv)
    root = args.root.resolve()

    if args.command == "generate":
        source_path = args.source or root / "qsearch.py"
        source = source_path.read_text(encoding="utf-8")
        try:
            mono = ex.extract(source)
        except ex.SplitError as error:
            print(f"cannot split {source_path}: {error}", file=sys.stderr)
            return 2
        paths = gen.write_package(mono, root, source, shim=args.shim)
        print(f"wrote {len(paths)} files: {len(mono.commands)} command functions, {len(mono.blocks)} subcommands, "
              f"{len(mono.dispatch)} flags, {len(mono.bindings)} imports" + (", and the shim" if args.shim else ""))
        return 0

    if args.command == "verify":
        sys.path.insert(0, str(root))
        from tools.split_cli import verify

        problems, notes = verify.compare(root, (args.legacy or root / "qsearch.py").resolve())
        for note in notes:
            print("note:", note)
        for problem in problems[:200]:
            print(problem)
        print(f"{len(problems)} problems")
        return 1 if problems else 0

    try:
        summary = gen.sweep(root)
    except ex.SplitError as error:
        print(f"cannot sweep: {error}", file=sys.stderr)
        return 2
    print(f"swept {len(summary['commands'])} functions, {len(summary['subcommands'])} subcommands, "
          f"{len(summary['imports'])} imports")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
