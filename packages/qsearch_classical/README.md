# qsearch-classical

The Q-Search research loop proposes quantum mechanisms and attacks them classically. Some
of the attacks are useful classical solvers in their own right. This package collects them
so they can be installed and reused without the research repository.

```bash
pip install -e packages/qsearch_classical
QSEARCH_CLASSICAL_ROOT=out python -m qsearch_classical.prime_character_opi --write
```

The install needs `setuptools>=68` to build. Under pip's default build isolation pip
fetches it into a temporary build environment, so offline use
`pip install --no-build-isolation -e packages/qsearch_classical` with a recent setuptools
already installed.

The `--write` flag writes `out/research/classical_baselines/prime_character_opi.json`.
Reports are read and written under `$QSEARCH_CLASSICAL_ROOT`, which defaults to the
current directory. Point it at a checkout of the repository to read the committed reports
as inputs. For example, `prime_character_finite_readout` reads the OPI report.

## Modules

The modules keep their names from `theorems/`.

| Group | Modules | What they compute |
|---|---|---|
| Prime-character OPI | `prime_character_opi`, `prime_character_norm_attack`, `prime_character_morse_attack`, `prime_character_exterior_bound`, `prime_character_capacity_source`, `prime_character_finite_readout` | Instances of optimal polynomial intersection (OPI) with prime-power character constraints, and classical attacks on them. The attacks are power completion, norm factorization, Morse and exterior-power trace bounds, and source and readout certificates. |
| Polar Gibbs source | `polar_conditional_sampler`, `polar_source_design` | Classical conditional sampling for polar-code Gibbs tasks, with a certified finite source design. |
| Jacobi sums | `jacobi_surface_reconstruction`, `jacobi_known_norm_reduction` | Reconstruction of Jacobi-sum ideals and the known-norm reduction to published classical theorems. |

`_validators.py` holds the two exact-input checks, `integer` and `rational`, copied from
`theorems/bpqm_gibbs_frontier.py`. Copying them avoids pulling in the BPQM frontier and
its imports.

Each report keeps the original flags, such as `accepted_speedup_candidate: false` and
`new_quantum_algorithm_claimed: false`. The research notes in `research/*.md` state the
scope of each result. Read them before citing a number.

## Keeping in sync with `theorems/`

The solver modules are generated, not edited. The research agents keep working in
`theorems/`, and `sync.py` regenerates the copies.

```bash
python packages/qsearch_classical/sync.py           # regenerate src/qsearch_classical/*.py
python packages/qsearch_classical/sync.py --check   # list drifted files, exit 1 if any
```

The rewrites are mechanical:

- Imports change from `theorems.X` to `qsearch_classical.X`.
- The validators come from `_validators.py`.
- The `sys.path` block is replaced by `$QSEARCH_CLASSICAL_ROOT`.
- Dependency hashes read the vendored copies.

Only the canonical form `from theorems.X import ...` of a vendored module is rewritten.
After the rewrites, sync scans each module's imports with `ast` and stops with an error on
any import that still names `theorems`: `import theorems.X`, `from theorems import X`,
odd spacing such as `from  theorems.X` or `from theorems . X`, submodules, relative
imports, and `importlib.import_module` or `__import__` calls with a literal theorems name.
It also stops if a module imports a validator that `_validators.py` does not copy.
`--check` reports these errors, files that differ or are missing, and vendored files with
no upstream module. The tools CI workflow runs on changes to the vendored theorem files,
so drift shows up as a failing parity test.

The layout is flat, one module per theorem file. The plan sketched `prime_character/`,
`polar/` and `jacobi/` subpackages. Keeping the file names identical keeps the rewrite
rules trivial. The groups are listed in `qsearch_classical.PRIME_CHARACTER`, `POLAR` and
`JACOBI`.

## Tests

`tests/tools/test_classical_package.py` covers four things:

- **Rewrite rules:** imports, paths and the root are rewritten correctly; an unvendored
  import, every non-canonical theorems import form and an uncopied validator are
  rejected.
- **Parity:** the committed package matches a fresh sync of `theorems/`, and `check()`
  reports an unsupported upstream import and a stale vendored file with no upstream.
- **Isolation:** the package imports with only `src/` on the path, and no `theorems` or
  `core` module gets loaded.
- **Reproduction:** six modules recompute their committed reports exactly, ignoring
  source hashes and library versions. They are the OPI, norm-attack, capacity-source,
  finite-readout, conditional-sampler and small source-design modules, and each finishes
  in seconds. At N = 127, K = 77 the OPI report has perfect 127 of 127 witnesses only for
  the two common-coset (global) inputs; its mixed inputs reach 124 and 122. The perfect
  127 of 127 mixed witnesses are in the norm-attack report.

The Morse attack and the exterior bound are too slow for CI. Both were checked once by
hand on 2026-10-19 and matched exactly, in 271 s and 21 s.
`docs/papers/classical-competitors/reproduce.sh` reruns the eight prime-character and
polar modules, including the N = 32768 polar design; it does not run the two Jacobi
modules. It runs the vendored source from the checkout (it puts `src/` on `PYTHONPATH`),
not an installed copy, and it also needs scipy and cvxpy, which this package does not
list, for the DCP circuit search.

An editable install was checked offline on 2026-10-19 in a fresh virtual environment
with `--system-site-packages`, using `pip install --no-index --no-deps`. With build
isolation it fails, because pip cannot fetch `setuptools>=68`; with
`--no-build-isolation` it succeeds, and the installed package imports without loading
`theorems` or `core`.
