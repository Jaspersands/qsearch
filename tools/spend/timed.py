"""Opt-in timing wrapper: run a command, then append one timed_run line to the spend ledger.

    python tools/spend/timed.py -- python qsearch.py <subcommand> ...
    python tools/spend/timed.py --label codex -- python qsearch.py <subcommand> ...

The command's stdin, stdout and stderr are the wrapper's own; nothing is captured. The
wrapper exits with the command's exit code (128+N if a signal N killed it, 127 if the
command was not found). It records wall-clock time, the child's CPU time and peak RSS from
getrusage(RUSAGE_CHILDREN), the exit code, and the record counts of every
research/registry/*.json before and after the run. The registry delta covers every writer
during the run window, including other agents.
"""

from __future__ import annotations

import argparse
import resource
import signal
import subprocess
import sys
import time
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.spend.common import LEDGER, NEGATIVES, append_event, registry_counts, to_utc_iso  # noqa: E402

# Global qsearch.py options that take a value; their value is not the subcommand.
VALUE_OPTIONS = {"--root"}


def subcommand_of(command: list[str]) -> str | None:
    """Best-effort: the first positional argument after qsearch.py."""
    for index, arg in enumerate(command):
        if Path(arg).name == "qsearch.py":
            rest = command[index + 1:]
            skip = False
            for item in rest:
                if skip:
                    skip = False
                elif item in VALUE_OPTIONS:
                    skip = True
                elif not item.startswith("-"):
                    return item
            return None
    return None


def portable_command(command: list[str], root: Path) -> list[str]:
    """The command as recorded: absolute paths inside the repo become repo-relative."""
    base = root.resolve()
    recorded = []
    for arg in command:
        path = Path(arg)
        if path.is_absolute():
            try:
                recorded.append(path.resolve().relative_to(base).as_posix())
                continue
            except ValueError:
                pass
        recorded.append(arg)
    return recorded


def _rss_bytes(maxrss: int) -> int:
    return int(maxrss if sys.platform == "darwin" else maxrss * 1024)  # Linux reports KiB


def _wait(proc: subprocess.Popen) -> int:
    """Wait for the child. Ctrl-C reaches the child through the process group; keep waiting for it."""
    def forward(signum, _frame):
        proc.send_signal(signum)

    previous = {sig: signal.signal(sig, forward) for sig in (signal.SIGTERM, signal.SIGHUP)}
    try:
        while True:
            try:
                return proc.wait()
            except KeyboardInterrupt:
                continue
    finally:
        for sig, handler in previous.items():
            signal.signal(sig, handler)


def _delta(before: dict, after: dict) -> dict[str, int]:
    delta = {}
    for name in sorted(set(before) | set(after)):
        old, new = before.get(name, 0), after.get(name, 0)
        if old is None or new is None:
            continue
        if new != old:
            delta[name] = new - old
    return delta


def run_timed(command: list[str], root: Path, ledger: Path, label: str | None = None) -> tuple[int, dict]:
    before = registry_counts(root)
    started = time.time()
    usage0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    t0 = time.perf_counter()
    error = None
    try:
        proc = subprocess.Popen(command)
    except FileNotFoundError as exc:
        exit_code, error = 127, exc
    except PermissionError as exc:
        exit_code, error = 126, exc
    else:
        returncode = _wait(proc)
        exit_code = 128 - returncode if returncode < 0 else returncode
    wall = time.perf_counter() - t0
    ended = time.time()
    usage1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    after = registry_counts(root)
    if error is not None:
        print(f"timed.py: cannot run {command[0]!r}: {error.strerror or error}", file=sys.stderr)

    user = usage1.ru_utime - usage0.ru_utime
    system = usage1.ru_stime - usage0.ru_stime
    delta = _delta(before, after)
    event = {
        "kind": "timed_run",
        "timestamp": to_utc_iso(started),
        "ended_at": to_utc_iso(ended),
        "command": portable_command(command, root),
        "subcommand": subcommand_of(command),
        "label": label,
        "wall_seconds": round(wall, 3),
        "cpu_seconds": round(user + system, 3),
        "cpu_user_seconds": round(user, 3),
        "cpu_system_seconds": round(system, 3),
        "peak_rss_bytes": _rss_bytes(usage1.ru_maxrss),
        "exit_code": exit_code,
        "registry_before": before,
        "registry_after": after,
        "registry_delta": delta,
        "negatives_added": delta.get(NEGATIVES, 0) if before.get(NEGATIVES) is not None and after.get(NEGATIVES) is not None else None,
        "source": "tools/spend/timed.py",
    }
    append_event(ledger, event)
    return exit_code, event


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        usage="python tools/spend/timed.py [--root ROOT] [--ledger FILE] [--label NAME] -- COMMAND [ARG ...]",
    )
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--ledger", type=Path, help=f"Ledger path (default: ROOT/{LEDGER}).")
    parser.add_argument("--label", help="Optional free-text label, e.g. which agent ran the command.")
    if "--" in argv:
        split = argv.index("--")
        options, command = argv[:split], argv[split + 1:]
    else:
        options, command = argv, []
    try:
        args = parser.parse_args(options)
    except SystemExit as exc:
        return int(exc.code or 0)
    if not command:
        parser.print_usage(sys.stderr)
        print("timed.py: give the command to run after --", file=sys.stderr)
        return 2
    code, _ = run_timed(command, args.root, args.ledger or args.root / LEDGER, label=args.label)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
