# Preflight

Checks a checkout for the problems that have already blocked a merge. For the agents, one
line before every commit:

```bash
python tools/preflight/preflight.py
```

```bash
python tools/preflight/preflight.py --json                 # {"root", "problems", "count"}
python tools/preflight/preflight.py --imports --validate   # also run the two slow checks
python tools/preflight/preflight.py --root ../other-checkout
```

It prints one line per problem, `check: path: message`, then `N problems`. It exits 1 when
there is any problem and 0 when there is none. A `--root` that is not a directory, or that
has no `qsearch.py` (say `--root qsearch_cli` by mistake), is a usage error (exit 2). Paths
are relative to the checked root. It writes nothing.

## Why it exists

The merge of 2026-10-19 was blocked twice over:

1. The agents' `qsearch.py` had gained 24 imports of new theorem modules that were in their
   working copy but not in git. The modules had to be committed first (8831535f). Those
   imports now live in `qsearch_cli/imports.py`.
2. A hypothesis contract,
   `research/hypotheses/dcp_clifford_stabilizer_magic_monotone_carry_injection_bridge_contract.json`,
   is not valid JSON. It is still broken, and `qsearch.py validate` does not notice: it
   exits 0 with the file in place.

## Checks

The default checks are static. They parse files, ask git which files it tracks, and import
nothing. A run takes a few seconds, most of it parsing about 250 MB of
`research/classical_baselines/`.

| Check | Catches | Message |
|---|---|---|
| `json` | Any `*.json` under `research/hypotheses`, `research/registry`, `research/audits` or `research/classical_baselines` that does not parse, including non-UTF-8 bytes | the parser's own error, e.g. `Invalid \escape: line 7 column 167 (char 635)` |
| `imports` | A `theorems/`, `core/` or `qsearch_cli/` module the CLI refers to that is not on disk, or that `git ls-files` does not list | `missing on disk`, `missing on disk (case differs: theorems/x.py)`, `not tracked by git`, `not tracked by git (intent-to-add only)`, or one `git unavailable` (with the reason when the root is inside a work tree) |
| `manifest` | A subcommand in `research/audits/cli_manifest.json` that is no longer in `ORDER` in `qsearch_cli/registry.py`, or that moved module | `subcommand X missing from ORDER`, `X: manifest says A, ORDER says B` |

A `.json` file that fails to parse is read again up to three times, 25 to 75 ms apart, as
`tools/corpus/docs.py`'s `read_json` does: an agent rewriting a registry file in place can be
caught half way. Integers are parsed as text, so one longer than Python's 4300-digit `int()`
limit parses. Nesting deeper than Python's `json` can follow is reported with its
`maximum recursion depth exceeded` message. A `.json` symlink to nothing is a `dangling
symlink` problem, and a directory the walk cannot list is a `cannot list: <reason>` problem,
so neither is skipped in silence.

The `imports` check collects references from these places:

- Import statements anywhere in `qsearch.py`, `qsearch_cli/imports.py` and
  `qsearch_cli/commands/*.py`, including the lazy imports inside command bodies.
  `import theorems.x`, `from core.y import z`, `from qsearch_cli.main import main` and `from
  theorems import x` name their file, whether or not it exists. A bare name, `from x import
  f` (the usual style here, and the one an old-style addition to `qsearch.py` uses), counts
  when `theorems/x.py` exists, else when `core/x.py` exists. Standard library names are
  skipped.
- The `IMPORTS` table in `qsearch_cli/imports.py`, read with `ast.literal_eval`. A dotted
  `theorems.x` maps to `theorems/x.py`. A package-style entry, `("theorems", "x")` or
  `("core", "x")`, which is what `tools/split_cli/migrate.py sweep` writes for `from theorems
  import x`, maps to `theorems/x.py` or `core/x.py`. A bare name maps to `theorems/<name>.py`
  when that file exists, else `core/<name>.py`, the order the CLI puts them on `sys.path`.
  Standard library names (`os`, `json`, ...) are skipped.
- The module column of `DISPATCH` in `qsearch_cli/registry.py`.
- The module columns of `ORDER` and `FUNCTIONS` in `qsearch_cli/registry.py`, say
  `qsearch_cli/commands/general.py`. `qsearch_cli/parser.py` imports every `ORDER` module to
  build the parser, so one that is missing from a clone breaks every command, `--help`
  included.
- Import statements inside every module found so far, followed until no new module turns
  up, by the same rules. A committed theorem module whose new helper was never committed
  works in the working copy and fails with `ModuleNotFoundError` in a clone. On 2026-10-22
  the CLI's sources named 962 modules directly and 1092 with their imports.

  These modules are scanned line by line rather than parsed, which keeps the check at about
  one second instead of four: an `import` or `from ... import` that starts a line, outside
  strings and comments, with its bracketed or backslash-continued names. On 2026-10-22 the
  scan found exactly the import statements a full parse finds in every one of the 1281 files
  under `theorems/`, `core/` and `qsearch_cli/`.

A CLI source that does not parse, or a table of the wrong shape (an `IMPORTS` entry whose
module is `None`, an `ORDER` that is a dict), is one `imports` problem, `cannot read the
CLI sources: ...`, and the other checks still run.

A module named in another case than its file (`theorems.Foo` for `theorems/foo.py`) is
missing: Python's import matches case even on macOS, whose file system does not. The
message names the file, `missing on disk (case differs: theorems/foo.py)`, on every
platform.

A module that is staged with `git add` counts as tracked, since the commit will include it.
One marked with `git add -N` (intent to add) does not: `git ls-files` lists it, but a plain
`git commit` leaves it out. Preflight asks `git diff-files --diff-filter=A` for those and
reports them as `not tracked by git (intent-to-add only)`. Only plumbing commands run, and
none of them writes the index: porcelain `git diff` refreshes stale stat data, rewriting
`.git/index` under `index.lock`, which would fail another agent's `git add` or `git commit`
in the same checkout.

Git is asked only when the root is the top of its own work tree. Without that (no git, a
directory that is not a repository, or an exported tree sitting inside some other
repository such as a dotfiles repository in `$HOME`) the check still reports modules
missing on disk and adds one `git unavailable` problem instead of calling every module
untracked. When git works but the root is not the top of the work tree, the problem says
so: `git unavailable: the root is not the top of a git work tree (git sees it as
export/)`.

## Slow checks

| Flag | Check | What it does |
|---|---|---|
| `--imports` | `resolve` | Calls `tools/split_cli/verify.py`'s `check_imports`, which imports every `IMPORTS` name and command function in this process. It catches a module that exists but fails to import. One problem per failing name, under the path `qsearch_cli`. |
| `--validate` | `validate` | Runs `python qsearch.py validate` in the root, as CI does. A non-zero exit is one problem. Validate prints its report as JSON on stdout, so the message is `exit N: K issues, first: <candidate>: <message>`; when there is no report (a crash) it is `exit N:` and the last line of stderr, else of stdout. |

Both together took about 40 seconds on 2026-10-21.

## Today's output

On this checkout on 2026-10-21 (also with `--imports --validate`):

```
json: research/hypotheses/dcp_clifford_stabilizer_magic_monotone_carry_injection_bridge_contract.json: Invalid \escape: line 7 column 167 (char 635)
1 problems
```

Preflight reports the contract and does not fix it. The agents own `research/hypotheses/`.
`tests/tools/test_preflight.py::test_check_json_finds_todays_broken_contract` pins this
error. Delete that test once the agents fix the file.

## Limits

- A bare import statement whose module is in neither `theorems/` nor `core/` is skipped,
  since it may be a third-party package. So a bare import of a module that was never
  written, or was deleted, is not reported. `--imports` does not catch one inside a command
  body either: it resolves command functions without running them. A dotted or `from
  theorems import x` import of a missing module is reported.
- In a module reached through another module, the line scan misses an import in a one-line
  compound statement (`if x: import y`) or after a semicolon. A module that is not valid
  UTF-8 is checked itself, but its imports are not followed.
- A bare third-party name added to `IMPORTS` (say `numpy`) would be reported as a missing
  `core/numpy.py`. Today the table holds only `theorems/` and `core/` modules and six
  standard library names.
- The `json` check parses only. It does not check any schema. `qsearch.py validate` checks
  the registries.
- The `json` check reads only its four directories: 550 of the 1711 tracked
  `research/**/*.json` files on 2026-10-22. It does not read `research/representation`
  (619), `research/reductions` (231), `research/phase_workbench` (162),
  `research/literature_audits` (47), `research/code_equivalence` (34),
  `research/certificates` (26), `research/coset_workbench` (15), `research/scaling`,
  `research/quarantine`, or the 25 files at the top of `research/` such as
  `research/proof_obligations.json`. A broken file there passes. Parsing all of them on
  2026-10-22 found only the contract above.
