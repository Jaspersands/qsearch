# Splitting qsearch.py

`qsearch.py` was a 30,562-line file:
- 774 import statements, which loaded the theorem modules on every start;
- 895 command functions;
- an 8,400-line `build_parser`.

Adding a command meant editing three places in that one file. It is now a 369-line shim, most of which is the original command-list docstring. The commands live in `qsearch_cli/`.

## Layout

- **`qsearch_cli/commands/<domain>.py`** holds every subcommand. The domains are `dcp`, `code`, `coset`, `self_dual_wreath`, `native` and `general`. Each subcommand has an `add_<name>(subparsers)` function with its parser lines, moved verbatim, and its `command_<name>(args)` function.
- **Lazy imports.** A command's first line imports what it needs from `qsearch` at call time, for example `from qsearch import validate_registry, write_x_report`. So loading a domain module is cheap, and `monkeypatch.setattr(qsearch, name, ...)` still reaches the command.
- **`qsearch_cli/registry.py`** has three tables:
  - `ORDER`: every subcommand in `--help` order;
  - `FUNCTIONS`: every command function;
  - `DISPATCH`: the 34 certificate flags.
- **`qsearch_cli/imports.py`** lists the 814 names `qsearch.py` used to import. Each still works as `qsearch.<name>` through the shim's PEP 562 `__getattr__`.
  - The lookup happens on every use and is not cached. So patching the source module, for example `research_registry.validate_registry`, reaches `qsearch` only while the patch lasts.
  - A name that no longer imports raises `ImportError` naming the module and the name, as `import qsearch` used to. `hasattr` does not hide it.
  - A name `qsearch` never had raises `AttributeError`, so `hasattr` gives False and `getattr(qsearch, name, default)` gives the default.
- **`qsearch_cli/legacy.py`** binds the former globals that old-style code in `qsearch.py` reads (see below).
- **`qsearch_cli/parser.py` and `qsearch_cli/main.py`** build the parser and run a command, as the old `build_parser` and `main` did. `main` runs whatever `qsearch.<command function>` is at call time. So `qsearch.command_x = fake`, or an old-style redefinition of `command_x` in `qsearch.py`, wins, as it did in the monolith.
- **`research/audits/cli_manifest.json`** records every subcommand, alias, function, module and flag. It also lists the 33 functions no subcommand uses, and the one duplicate definition that was dropped.

## What changed for users

Nothing in behaviour. Commands, options, defaults, help text and output are the same. On 2026-10-19, `validate`, two `list` runs and `--help` gave byte-identical output before and after the split. After the review fixes the same day, 17 runs gave byte-identical exit code, stdout and stderr: `--help`, `validate`, three `list` runs, five error paths and seven subcommand help pages.

`python -m cProfile -o out qsearch.py validate` and `python -m trace ... qsearch.py ...` work. The `__main__` block imports `qsearch` and runs its `main`.

Startup is faster:

| Command | Before | After |
|---|---|---|
| `python qsearch.py --help` | 5.1–5.8 s | 0.8–1.3 s |
| `python qsearch.py validate` | 4.9 s | 2.4 s |
| `python qsearch.py list --limit 5` | 5.0 s | 1.8 s |

The review fixes did not slow startup. `--help` was timed against the version before them, interleaved, 7 runs each, at a load average near 410: median CPU time 0.51 s against 0.56 s, median wall time 3.2 s against 4.2 s. The table above was measured at a lower load.

## Adding a command

**Preferred.** In the matching `qsearch_cli/commands/<domain>.py`:
1. Write `add_<name>(subparsers)` and `command_<name>(args)`.
2. Import theorem code inside the command function.
3. Append `("<name>", "qsearch_cli.commands.<domain>", "add_<name>")` to `ORDER`, and the function to `FUNCTIONS`.

New certificate flags go in `add_flags` in `qsearch_cli/main.py` and in `DISPATCH`.

**The old style still works.** Put the import and the `command_*` function at module level in `qsearch.py`, above `_legacy_extensions`, and the `add_parser` lines inside `_legacy_extensions`.
- The code may use any name the monolith had without importing it: `json`, `Path`, `validate_registry`, another `command_*`. A global lookup inside `qsearch.py` never reaches its `__getattr__`, so when `qsearch.py` loads, `qsearch_cli/legacy.py` binds exactly the names that code reads. With no old-style code it binds nothing and imports nothing.
- A name used in a default argument value or a decorator is evaluated before that binding. Import it.
- Redefining an existing `command_*` in `qsearch.py` replaces it, as in the monolith.

Then run this, which moves them into `qsearch_cli/`:

```bash
python tools/split_cli/migrate.py sweep --root .
```

- `sweep` carries the imports each `add_parser` block needs into its new `add_*` function, for example `type=parse_int_csv` or `type=Path`.
- A command may read `_ROOT_DIR`, `_CORE_DIR`, `_THEOREMS_DIR`, `__file__` and `__doc__`. The shim keeps them, so the moved command imports them from `qsearch`.
- It refuses, with the line number and without writing anything:
  - edits to `main`, `build_parser`, `__getattr__`, the `sys.path` loop or the `__main__` block;
  - top-level statements other than imports and `command_*` functions, such as helpers, loops and assignments;
  - code after the `__main__` block;
  - a command that reads another module global, such as `_p` or `__name__`;
  - a subcommand name that already exists.

  Move such code by hand, or undo it, and sweep again.

Please don't add top-level theorem imports to `qsearch.py` and leave them there. They make every command slow again.

**The old wiring scripts no longer wire commands.** Use the old style above, or `qsearch_cli/` directly.
- `tools/wire_pass5_experiments.py` and `scratch/wire_generic_batch.py` open `research_registry.py` and `experiment_runner.py` at the repository root. Those moved to `core/` before the split, so the scripts stop with FileNotFoundError before they reach `qsearch.py`.
- `tools/wire_pass6_experiments.py` looks for monolith lines, `import argparse` and `def command_audit(args: argparse.Namespace) -> int:`. The shim has neither, so it leaves `qsearch.py` unchanged, although it still edits the registry, the runner and the tests and prints success. Its subcommand anchor never matched even the monolith.
- Restoring those lines in the shim would let the scripts add eager theorem imports and command functions with no subcommand. So the shim deliberately lacks them, and a test checks that.

## How the split was made and checked

```bash
python tools/split_cli/migrate.py generate --root . --source LEGACY_QSEARCH.py --shim
python tools/split_cli/migrate.py verify --root . --legacy LEGACY_QSEARCH.py
python tools/split_cli/migrate.py check-imports --root .
```

- **`extract.py`** accepts only the shapes `qsearch.py` actually uses: top-level imports, `command_*` functions, add-parser blocks, and the flag-and-dispatch `main`. The `_ROOT_DIR` lines, the `sys.path` loop and the `__main__` block must match their known text exactly, because they are not moved. Nothing may follow the `__main__` block except comments. Anything else stops the migration with the line number, so nothing is silently dropped.
  - It uses `symtable` to find the module-level names each command reads, including names in nested scopes. Names a command binds itself, such as a local `from theorems.x import main`, are left alone.
  - A command that reads `_ROOT_DIR`, `_CORE_DIR`, `_THEOREMS_DIR`, `__file__` or `__doc__` imports it from `qsearch`. A command that reads another module global stops the migration.
- **`generate`** refuses to run when `qsearch_cli/` already has subcommands, functions, flags or imports that the source lacks. It lists them. `--force` deletes them anyway.
- **`verify.py`** runs the legacy source as a module, with its own `sys.path` setup. Then it compares old and new:
  - **The full parser each `main` builds.** It intercepts `parse_args` to capture it, then compares every subcommand, alias, argument, default, type, help string and formatted `--help` page, plus the root flags.
  - **Every command body**, as an AST, ignoring only the added import line.
  - **Every name in `imports.py`**, which must resolve to the identical object the legacy module held.
  - **Undefined names**: no moved function may read a name that is not defined.
  - **Module globals**: no moved function may read a legacy global that is neither an import nor a function, such as `__file__`, `_ROOT_DIR` or `__name__`, unless it imports it from `qsearch`. In its new module that name is missing or has another value.
  - **Flag dispatch**: `DISPATCH` must equal the legacy `main`'s if-chain: the same flags, modules, functions and order.
  - **The shim**: every subcommand's function must be `qsearch.<name>`.
- **`check-imports`** imports every name in `imports.py` and every command function, and lists each failure with its module and name. The monolith did this on every start, so `python qsearch.py validate` used to catch a renamed theorem function. The shim imports lazily, so it no longer does.
- **Result on 2026-10-19, after the review fixes:**
  - `verify`: 0 problems, over 863 subcommands (871 names with aliases), 34 flags, 895 functions and 814 imports.
  - `check-imports`: 0 of 1,709 names failed. On the reviewer's copy with one theorem function renamed, it reported 7 failures and exited with 1.
  - `generate` from main's monolith reproduced `qsearch_cli/` and the manifest byte for byte.
- **The checkers fail when they should.**
  - Deleting one name from one command's import line made `verify` report the undefined name. Changing one default in the test fixture made it report the default.
  - Removing a moved command's `_ROOT_DIR` or `__file__` import, or changing the order, module or function of a flag in `DISPATCH`, made it report that.
  - The earlier extractor and `sweep` accepted the changed `__main__` blocks, `sys.path` loops, path assignments and edited shim functions that the tests now feed them, and dropped them without a message.
- **Test results:**
  - The 22 test files that exercise `qsearch` (560 tests) passed before and after the split. After the review fixes, four of them were re-run, including the two that patch `qsearch` with `monkeypatch.setattr`: `test_coset_overlap_echo.py`, `test_coset_overlap_transfer.py`, `test_dcp_affine_packet_noise.py` and `test_dcp_disjoint_kernel_pairing.py`. All 133 tests passed.
  - `tests/tools/test_split_cli.py` (50 tests) covers extraction, generation, verification, `sweep`, the shim's identity, monkeypatch and dispatch behaviour, old-style code, `-m cProfile` and `-m trace`, and lazy startup, on a fixture CLI. It also checks the real repository: startup imports no theorem module, every subcommand's help page renders, every subcommand in the manifest is still in the registry, an old-style copy of `validate` runs, and every import resolves. Commands added later are allowed.

## Continuous integration

- **`.github/workflows/ci-fast.yml`** runs on changes to `qsearch.py`, `qsearch_cli/`, this tool, the manifest or the site. It installs only pytest, because building the parser imports no research code. It runs:
  - `tests/tools/test_split_cli.py`;
  - `tests/test_cli_parser_integrity.py`;
  - the site JavaScript tests.

  Three tests need the research packages that resolving every import loads (numpy, scipy, sympy, networkx, python-flint), so they skip there: the full import check and the two old-style runs of a real theorem command. `tools.yml` has no networkx, so they skip there too. `ci-full.yml` installs `requirements.txt` and runs them. In a venv with only pytest, the two files gave 47 passed and 3 skipped in 15 s.
- **`.github/workflows/ci-full.yml`** runs every night and on demand. It runs all of `tests/` (15,886 tests in 1,254 files) in 8 shards with `pytest-split`. `validate.yml` never runs the whole suite. With no stored `.test_durations` file every test counts as equally long, and `--splitting-algorithm least_duration` deals them out in turn so slow files spread across shards. Shard run time is unmeasured: a local timing on 2026-10-19 was abandoned because other work held the machine's load average above 600. The 180-minute timeout is a guess; commit a `.test_durations` file (`pytest --store-durations`) after the first run to balance by time.
- **No `pytest.ini`.** The agents run `pytest tests/test_<x>.py` many times a day. A root config file would change the rootdir and options of every such run. The root `conftest.py` already sets `sys.path`, and nothing else needed configuring.

## Merging where qsearch.py has moved on

`generate` rebuilds `qsearch_cli/` from a monolithic `qsearch.py`. It applies only while the target branch's `qsearch.py` is still the monolith, that is, for the first merge of this split. Don't merge that first one by hand, because the agents keep editing `qsearch.py`:

1. Commit or set aside any uncommitted `qsearch.py` edits in the target checkout. Git will not merge over them anyway.
2. Merge the branch. `qsearch.py` will conflict.
3. Save the target's monolithic file, for example with `git show HEAD:qsearch.py > /tmp/qsearch_legacy.py`.
4. Run the `generate` and `verify` commands above with that file as `LEGACY_QSEARCH.py`, then `check-imports`.
5. If `generate` refuses, `qsearch_cli/` has commands the monolith lacks, for example ones added on this branch after the split. Add each listed one to the saved monolith the old way (import, function, `add_parser` lines), then run `generate` again. Use `--force` only for entries you mean to delete.
6. Check `verify` reports 0 problems and `check-imports` 0 failures, then commit `qsearch.py`, `qsearch_cli/` and the manifest.

After that, the target has the shim. Merge normally:
- `qsearch.py` is short. Old-style additions on either side sit above or inside `_legacy_extensions`; keep both, then run `sweep`.
- Conflicts in `qsearch_cli/registry.py` and `imports.py` are in plain lists; keep both sides' lines.
- Don't run `generate` again. There is no monolith to read, and it would refuse anyway.

If `extract.py` refuses a new shape, it names the line. Either rewrite that part in the usual style, or extend the extractor and its tests.

## Things the split surfaced

These were already so before the split:
- `command_native_banded_qft_transfer_matrix_audit` was defined twice. Python used the second definition, and only that one was moved.
- `command_dcp_quantum_z_error_detection_stabilizer_iceberg_code_bridge` names an undefined function, `generate_dcp_quantum_z_error_detection_stabilizer_iceberg_code_bridge`, inside `... if False else ...`. It is never evaluated, so the command works; the dead branch could be deleted.
- 33 command functions are not wired to any subcommand (`orphan_functions` in the manifest).
- The 34 certificate flags only work together with a subcommand, for example `python qsearch.py --dcp-...-bridge validate`. A flag on its own fails with "the following arguments are required: command".

These came from the monolith importing every module at start:
- `theorems/coset_typical_modular_gap_bound.py` calls `sys.set_int_max_str_digits(100_000)` when imported, so every command could turn integers of up to 100,000 digits into text. Python's default is 4,300. The shim sets the same limit itself, without the import.
- Importing the monolith left 12 warnings filters; importing the shim leaves Python's 5. The other 7 come from numpy (three "size changed" ignores, `RankWarning` always), scipy ("the matrix subclass" ignore, `SpecialFunctionWarning` always) and sympy (`SymPyDeprecationWarning` once). A command now gets them when it first imports those packages, so a warning raised before that could print differently. None of the compared runs changed.

Verification imports current source with a fresh temporary bytecode-cache location and bytecode writes disabled. Same-size edits made in one filesystem timestamp tick cannot be hidden by an older `.pyc` file.
