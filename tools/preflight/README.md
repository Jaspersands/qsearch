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
there is any problem and 0 when there is none. Paths are relative to the checked root. It
writes nothing.

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

The default checks are static. They parse files and ask git one question, and import
nothing. A run takes a few seconds, most of it parsing about 250 MB of
`research/classical_baselines/`.

| Check | Catches | Message |
|---|---|---|
| `json` | Any `*.json` under `research/hypotheses`, `research/registry`, `research/audits` or `research/classical_baselines` that does not parse, including non-UTF-8 bytes | the parser's own error, e.g. `Invalid \escape: line 7 column 167 (char 635)` |
| `imports` | A `theorems/` or `core/` module the CLI refers to that is not on disk, or that `git ls-files` does not list | `missing on disk`, `not tracked by git`, or one `git unavailable` |
| `manifest` | A subcommand in `research/audits/cli_manifest.json` that is no longer in `ORDER` in `qsearch_cli/registry.py`, or that moved module | `subcommand X missing from ORDER`, `X: manifest says A, ORDER says B` |

The `imports` check collects references from three places:

- `import theorems.x` and `from core.y import z` anywhere in `qsearch.py`,
  `qsearch_cli/imports.py` and `qsearch_cli/commands/*.py`, including the lazy imports inside
  command bodies.
- The `IMPORTS` table in `qsearch_cli/imports.py`, read with `ast.literal_eval`. A dotted
  `theorems.x` maps to `theorems/x.py`. A bare name maps to `theorems/<name>.py` when that
  file exists, else `core/<name>.py`, the order the CLI puts them on `sys.path`. Standard
  library names (`os`, `json`, ...) are skipped.
- The module column of `DISPATCH` in `qsearch_cli/registry.py`.

A module that is staged with `git add` counts as tracked, since the commit will include it.
Without git (an exported tree, or a directory that is not a repository) the check still
reports modules missing on disk and adds one `git unavailable` problem instead of calling
every module untracked.

## Slow checks

| Flag | Check | What it does |
|---|---|---|
| `--imports` | `resolve` | Calls `tools/split_cli/verify.py`'s `check_imports`, which imports every `IMPORTS` name and command function in this process. It catches a module that exists but fails to import. One problem per failing name, under the path `qsearch_cli`. |
| `--validate` | `validate` | Runs `python qsearch.py validate` in the root, as CI does. A non-zero exit is one problem, `exit N: <last stderr line>`. |

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

- Bare imports inside command bodies are not followed. Only `theorems.*` and `core.*`
  imports are. `qsearch_cli/commands/native.py` has `from ternary_measured_lattice_decoder
  import exact_json`, so an untracked module imported that way is not caught. `--imports`
  does not catch it either: it resolves command functions without running them.
- A bare third-party name added to `IMPORTS` (say `numpy`) would be reported as a missing
  `core/numpy.py`. Today the table holds only `theorems/` and `core/` modules and six
  standard library names.
- The `json` check parses only. It does not check any schema. `qsearch.py validate` checks
  the registries.
