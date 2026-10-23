"""Opt-in timing wrapper: run a command, then append one timed_run line to the spend ledger.

    python tools/spend/timed.py -- python qsearch.py <subcommand> ...
    python tools/spend/timed.py --label codex -- python qsearch.py <subcommand> ...

The command's stdin, stdout and stderr are the wrapper's own; nothing is captured. The
wrapper exits with the command's exit code (128+N if a signal N killed it, 127 if the
command was not found, 126 if it could not be executed), and writes a ledger line in every
case. It records wall-clock time, the command's own CPU time and peak RSS (from wait4 on the
child, so they cover the command and the processes it waited for, not earlier children of
the caller). On Linux the process-lifetime RSS high-water mark may include memory inherited
from the launcher before exec; it is not an isolated post-exec allocation measurement.
It also records the exit code and the record counts of every research/registry/*.json before
and after the run. The registry delta covers every writer during the run window, including
other agents.

The ledger is committed, so the command is recorded sanitized (see sanitize_command): the
program by name, repo files relative to the repo (the main checkout too, from a worktree),
any other local path as <path>, and the values of environment assignments and secret-looking
options as <redacted>.

SIGTERM and SIGHUP sent to the wrapper are passed on to the command. SIGINT is passed on
too, unless the wrapper and the command are in the foreground process group of the
terminal: then a Ctrl-C has already reached the command, and sending a second one could cut
its cleanup short.
"""

from __future__ import annotations

import argparse
import os
import re
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Iterable

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.spend.common import LEDGER, NEGATIVES, append_event, registry_counts, repo_roots, to_utc_iso  # noqa: E402

# Global qsearch.py options that take a value; their value is not the subcommand.
VALUE_OPTIONS = {"--root"}
SUBCOMMAND = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*")
SECRET_NAME = re.compile(r"token|key|secret|passw|auth|credential", re.IGNORECASE)
ASSIGNMENT = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)=(.*)", re.DOTALL)
OPTION = re.compile(r"(--?[A-Za-z0-9][\w.-]*)=(.*)", re.DOTALL)
# An absolute path inside a longer argument (code after -c, say): a slash not preceded by a word
# character, dot, slash or hyphen and not followed by a slash (so URLs survive), up to a delimiter.
DELIMITERS = r"\s'\"`,;)\]}"
EMBEDDED_PATH = re.compile(rf"(?<![\w.~/-])/(?=[^\s/'\"])[^{DELIMITERS}]*|(?<![\w.~/-])~[\w.-]*(?:/[^{DELIMITERS}]*)?")
PATH_MARK = "<path>"
REDACTED = "<redacted>"


def _secret_option(option: str) -> bool:
    return option.startswith("-") and bool(SECRET_NAME.search(option.lstrip("-")))


def subcommand_of(command: list[str]) -> str | None:
    """The qsearch subcommand when the command runs `qsearch.py <subcommand>`, else None.

    Only `--root VALUE` may come between qsearch.py and the subcommand (it is the only global
    option qsearch.py has), and the subcommand must look like one, so a path, a secret or an
    option's value is never returned.
    """
    for index, arg in enumerate(command):
        if Path(arg).name == "qsearch.py":
            rest = iter(command[index + 1:])
            for item in rest:
                if item in VALUE_OPTIONS:
                    next(rest, None)
                elif item.split("=", 1)[0] in VALUE_OPTIONS:
                    continue
                elif item.startswith("-"):
                    return None
                else:
                    return item if SUBCOMMAND.fullmatch(item) else None
            return None
    return None


def _roots(roots: Iterable[Path]) -> list[tuple[str, str]]:
    """(normalised, resolved) string forms of each root, most specific first."""
    forms = []
    for root in roots:
        forms.append((os.path.normpath(str(root)), str(Path(root).resolve())))
    return sorted(set(forms), key=lambda pair: -len(pair[1]))


def _relative(path: str, roots: list[tuple[str, str]]) -> str | None:
    """`path` relative to the most specific root containing it, else None."""
    expanded = os.path.expanduser(path)
    candidates = {os.path.normpath(expanded)}
    try:
        candidates.add(str(Path(expanded).resolve()))
    except (OSError, RuntimeError):
        pass
    for forms in roots:
        for root in forms:
            for candidate in candidates:
                if candidate == root:
                    return "."
                if candidate.startswith(root.rstrip(os.sep) + os.sep):
                    return Path(os.path.relpath(candidate, root)).as_posix()
    return None


def _is_path(arg: str) -> bool:
    return arg.startswith("/") or arg == "~" or arg.startswith("~/") or bool(re.match(r"~[\w.-]+/", arg))


def _path(arg: str, roots: list[tuple[str, str]]) -> str:
    return _relative(arg, roots) or PATH_MARK


def _scrub(text: str, roots: list[tuple[str, str]]) -> str:
    """Make repo paths inside `text` relative and replace every other absolute or ~ path."""
    for forms in roots:
        for root in sorted(set(forms), key=len, reverse=True):
            root = root.rstrip(os.sep)
            text = text.replace(root + os.sep, "")
            text = re.sub(re.escape(root) + rf"(?![^{DELIMITERS}])", ".", text)  # the bare root
    home = str(Path.home())
    if home and home != os.sep:
        text = re.sub(re.escape(home) + rf"(?:/[^{DELIMITERS}]*)?", PATH_MARK, text)
    return EMBEDDED_PATH.sub(lambda match: _relative(match.group(0), roots) or PATH_MARK, text)


def _program(arg: str, roots: list[tuple[str, str]]) -> str:
    """A program as recorded: repo-relative inside the repo, else its name only (python3, not its path)."""
    if not arg:
        return arg
    if "/" in arg or arg.startswith("~"):
        relative = _relative(arg, roots) if _is_path(arg) else None
        return relative or Path(os.path.expanduser(arg)).name
    return arg


def sanitize_command(command: list[str], roots: Iterable[Path]) -> list[str]:
    """The command as recorded in the committed ledger.

    - The program (argv[0], and the program after `env`) by name, or repo-relative if it is a repo file.
    - Paths inside a root (the repo, and its main checkout from a worktree) relative to it.
    - Any other absolute or ~ path, whole or inside a longer argument, as <path>.
    - NAME=VALUE (environment assignments) as NAME=<redacted>.
    - The value of an option whose name looks secret (token, key, secret, password, auth,
      credential), as --name=<redacted> or as the next argument <redacted>.
    Applying it twice changes nothing.
    """
    forms = _roots(roots)
    recorded: list[str] = []
    program_next = True
    redact_next = False
    for arg in command:
        if redact_next:
            redact_next = False
            if not arg.startswith("-"):
                recorded.append(REDACTED)
                continue
        assignment = ASSIGNMENT.fullmatch(arg)
        option = OPTION.fullmatch(arg)
        if assignment and not arg.startswith("-"):
            recorded.append(f"{assignment.group(1)}={REDACTED}" if assignment.group(2) else arg)
            continue
        if program_next:
            if arg.startswith("-"):
                recorded.append(arg)  # an option of `env`
                continue
            name = _program(arg, forms)
            recorded.append(name)
            program_next = Path(name).name == "env"
            continue
        if option:
            name, value = option.groups()
            if _secret_option(name):
                recorded.append(f"{name}={REDACTED}")
            elif _is_path(value):
                recorded.append(f"{name}={_path(value, forms)}")
            else:
                recorded.append(f"{name}={_scrub(value, forms)}")
        elif arg.startswith("-"):
            recorded.append(arg)
            redact_next = _secret_option(arg)
        elif _is_path(arg):
            recorded.append(_path(arg, forms))
        else:
            recorded.append(_scrub(arg, forms))
    return recorded


def sanitize_event(event: dict, roots: Iterable[Path]) -> dict:
    """A timed_run ledger line with its command (and subcommand) recorded as sanitize_command does."""
    command = event.get("command")
    if event.get("kind") != "timed_run" or not isinstance(command, list) or not all(isinstance(a, str) for a in command):
        return event
    return {**event, "command": sanitize_command(command, roots), "subcommand": subcommand_of(command)}


def _rss_bytes(maxrss: int) -> int:
    return int(maxrss if sys.platform == "darwin" else maxrss * 1024)  # Linux reports KiB


def _terminal_delivers_sigint(pid: int) -> bool:
    """True when the child is in the foreground process group of our terminal, so Ctrl-C reached it too."""
    for fd in (0, 1, 2):
        try:
            foreground = os.tcgetpgrp(fd)
        except OSError:
            continue
        try:
            return os.getpgid(pid) == foreground
        except OSError:
            return False
    return False


def _wait(proc: subprocess.Popen):
    """Reap the child with wait4 (its own status and rusage), passing on signals sent to the wrapper."""
    def forward(signum, _frame):
        if signum == signal.SIGINT and _terminal_delivers_sigint(proc.pid):
            return
        try:
            os.kill(proc.pid, signum)  # not proc.send_signal: its poll() could reap the child before wait4
        except ProcessLookupError:
            pass

    previous = {}
    if threading.current_thread() is threading.main_thread():
        previous = {sig: signal.signal(sig, forward) for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)}
    try:
        while True:
            try:
                _, status, usage = os.wait4(proc.pid, 0)
                break
            except InterruptedError:
                continue
            except KeyboardInterrupt:  # not the main thread: Ctrl-C reached the child as well
                continue
    finally:
        for sig, handler in previous.items():
            signal.signal(sig, handler)
    proc.returncode = os.waitstatus_to_exitcode(status)
    return proc.returncode, usage


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
    t0 = time.perf_counter()
    error = None
    usage = None
    try:
        proc = subprocess.Popen(command)
    except FileNotFoundError as exc:
        exit_code, error = 127, exc
    except OSError as exc:  # permission denied, exec format error, ...
        exit_code, error = 126, exc
    else:
        returncode, usage = _wait(proc)
        exit_code = 128 - returncode if returncode < 0 else returncode
    wall = time.perf_counter() - t0
    ended = time.time()
    after = registry_counts(root)
    if error is not None:
        print(f"timed.py: cannot run {command[0]!r}: {error.strerror or error}", file=sys.stderr)

    user = usage.ru_utime if usage is not None else 0.0
    system = usage.ru_stime if usage is not None else 0.0
    delta = _delta(before, after)
    event = {
        "kind": "timed_run",
        "timestamp": to_utc_iso(started),
        "ended_at": to_utc_iso(ended),
        "command": sanitize_command(command, repo_roots(root)),
        "subcommand": subcommand_of(command),
        "label": label,
        "wall_seconds": round(wall, 3),
        "cpu_seconds": round(user + system, 3),
        "cpu_user_seconds": round(user, 3),
        "cpu_system_seconds": round(system, 3),
        "peak_rss_bytes": _rss_bytes(usage.ru_maxrss) if usage is not None else None,
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
