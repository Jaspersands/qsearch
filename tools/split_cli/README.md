# Splitting qsearch.py

`qsearch.py` was a 30,562-line file:
- 774 import statements, which loaded the theorem modules on every start;
- 895 command functions;
- an 8,400-line `build_parser`.

Adding a command meant editing three places in that one file. It is now a 358-line shim, most of which is the original command-list docstring. The commands live in `qsearch_cli/`.

## Layout

- **`qsearch_cli/commands/<domain>.py`** holds every subcommand. The domains are `dcp`, `code`, `coset`, `self_dual_wreath`, `native` and `general`. Each subcommand has an `add_<name>(subparsers)` function with its parser lines, moved verbatim, and its `command_<name>(args)` function.
- **Lazy imports.** A command's first line imports what it needs from `qsearch` at call time, for example `from qsearch import validate_registry, write_x_report`. So loading a domain module is cheap, and `monkeypatch.setattr(qsearch, name, ...)` still reaches the command.
- **`qsearch_cli/registry.py`** has three tables:
  - `ORDER`: every subcommand in `--help` order;
  - `FUNCTIONS`: every command function;
  - `DISPATCH`: the 34 certificate flags.
- **`qsearch_cli/imports.py`** lists the 814 names `qsearch.py` used to import. Each still works as `qsearch.<name>` and is imported on first use (PEP 562 `__getattr__` in the shim).
- **`qsearch_cli/parser.py` and `qsearch_cli/main.py`** build the parser and run a command, exactly as the old `build_parser` and `main` did.
- **`research/audits/cli_manifest.json`** records every subcommand, alias, function, module and flag. It also lists the 33 functions no subcommand uses, and the one duplicate definition that was dropped.

## What changed for users

Nothing in behaviour. Commands, options, defaults, help text and output are the same. On 2026-10-19, `validate`, two `list` runs and `--help` gave byte-identical output before and after the split.

Startup is faster:

| Command | Before | After |
|---|---|---|
| `python qsearch.py --help` | 5.1–5.8 s | 0.8–1.3 s |
| `python qsearch.py validate` | 4.9 s | 2.4 s |
| `python qsearch.py list --limit 5` | 5.0 s | 1.8 s |

## Adding a command

**Preferred.** In the matching `qsearch_cli/commands/<domain>.py`:
1. Write `add_<name>(subparsers)` and `command_<name>(args)`.
2. Import theorem code inside the command function.
3. Append `("<name>", "qsearch_cli.commands.<domain>", "add_<name>")` to `ORDER`, and the function to `FUNCTIONS`.

New certificate flags go in `add_flags` in `qsearch_cli/main.py` and in `DISPATCH`.

**The old style still works.** Put the import and the `command_*` function at module level in `qsearch.py`, above `_legacy_extensions`, and the `add_parser` lines inside `_legacy_extensions`. Then run this, which moves them into `qsearch_cli/`:

```bash
python tools/split_cli/migrate.py sweep --root .
```

Please don't add top-level theorem imports to `qsearch.py` and leave them there. They make every command slow again.

## How the split was made and checked

```bash
python tools/split_cli/migrate.py generate --root . --source LEGACY_QSEARCH.py --shim
python tools/split_cli/migrate.py verify --root . --legacy LEGACY_QSEARCH.py
```

- **`extract.py`** accepts only the shapes `qsearch.py` actually uses: top-level imports, the `sys.path` block, `command_*` functions, add-parser blocks, and the flag-and-dispatch `main`. Anything else stops the migration with the line number, so nothing is silently dropped. It uses `symtable` to find the module-level names each command reads, including names in nested scopes. Names a command binds itself, such as a local `from theorems.x import main`, are left alone.
- **`verify.py`** runs the legacy source as a module, with its own `sys.path` setup. Then it compares old and new:
  - **The full parser each `main` builds.** It intercepts `parse_args` to capture it, then compares every subcommand, alias, argument, default, type, help string and formatted `--help` page, plus the root flags.
  - **Every command body**, as an AST, ignoring only the added import line.
  - **Every name in `imports.py`**, which must resolve to the identical object the legacy module held.
  - **Undefined names**: no moved function may read a name that is not defined.
  - **The shim**: every subcommand's function must be `qsearch.<name>`.
- **Result on 2026-10-19:** 0 problems, over 863 subcommands (871 names with aliases), 34 flags, 895 functions and 814 imports.
- **The checker fails when it should.** Deleting one name from one command's import line made it report the undefined name. Changing one default in the test fixture made it report the default.
- **Test results:**
  - The 22 test files that exercise `qsearch` (560 tests) pass before and after the split.
  - `tests/tools/test_split_cli.py` covers extraction, generation, verification, the shim's identity and monkeypatch behaviour, lazy startup and `sweep` on a fixture CLI. It also checks the real repository: startup imports no theorem module, every subcommand's help page renders, and every subcommand in the manifest is still in the registry. Commands added later are allowed.

## Continuous integration

- **`.github/workflows/ci-fast.yml`** runs on changes to `qsearch.py`, `qsearch_cli/`, this tool, the manifest or the site. It installs only pytest, because building the parser imports no research code. It runs:
  - `tests/tools/test_split_cli.py`: lazy startup, every subcommand's help page, and no migrated subcommand missing;
  - `tests/test_cli_parser_integrity.py`;
  - the site JavaScript tests.

  In a fresh venv with only pytest, the Python part took about 10 s.
- **`.github/workflows/ci-full.yml`** runs every night and on demand. It runs all of `tests/` (15,886 tests in 1,254 files) in 8 shards with `pytest-split`. `validate.yml` never runs the whole suite. With no stored `.test_durations` file, the shards are balanced by test count, not time.
- **No `pytest.ini`.** The agents run `pytest tests/test_<x>.py` many times a day. A root config file would change the rootdir and options of every such run. The root `conftest.py` already sets `sys.path`, and nothing else needed configuring.

## Merging where qsearch.py has moved on

The agents keep editing `qsearch.py`, so don't merge this split by hand. Re-run it on their latest file:

1. Commit or set aside any uncommitted `qsearch.py` edits in the target checkout. Git will not merge over them anyway.
2. Merge the branch. `qsearch.py` will conflict.
3. Save the target's monolithic file, for example with `git show HEAD:qsearch.py > /tmp/qsearch_legacy.py`.
4. Run the `generate` and `verify` commands above with that file as `LEGACY_QSEARCH.py`.
5. Check `verify` reports 0 problems, then commit `qsearch.py`, `qsearch_cli/` and the manifest.

If `extract.py` refuses a new shape, it names the line. Either rewrite that part in the usual style, or extend the extractor and its tests.

## Things the split surfaced (unchanged behaviour)

- `command_native_banded_qft_transfer_matrix_audit` was defined twice. Python used the second definition, and only that one was moved.
- `command_dcp_quantum_z_error_detection_stabilizer_iceberg_code_bridge` names an undefined function, `generate_dcp_quantum_z_error_detection_stabilizer_iceberg_code_bridge`, inside `... if False else ...`. It is never evaluated, so the command works; the dead branch could be deleted.
- 33 command functions are not wired to any subcommand (`orphan_functions` in the manifest).
- The 34 certificate flags only work together with a subcommand, for example `python qsearch.py --dcp-...-bridge validate`. A flag on its own fails with "the following arguments are required: command". This was already the case before the split.
