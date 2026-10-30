# Verification

2026-10-25. All commands below completed; no research subprocess remains.
Interpreter: /opt/anaconda3/bin/python. Source is outside the unverified
migrating checkout. No main/staging/registry/CLI/UI/Git or migration edits.

## Completed Checks

From /Users/jaspersands/Developer/qsearch-research-work:

```sh
/opt/anaconda3/bin/python -m pytest -q hdqi-hidden-mode-access-2026-10-25 hdqi-transfer-word-sampler-2026-10-25 hdqi-rational-transfer-2026-10-25 hdqi-ecf-tree-sampler-2026-10-25
```

170 tests PASS in 10.94 seconds: 106 predecessor tests plus 64 new controls.
Fifteen Python files across these four bundles pass py_compile, including
all five Python files in this new bundle. No JavaScript was changed.

From this bundle:

```sh
/opt/anaconda3/bin/python replay.py write
/opt/anaconda3/bin/python replay.py check
```

Both PASS. Exact replay receipt SHA256:

    6cbb7188ed53314322643acac2bc2fc7347365f132098252d031bb18f72174b5

The receipt hashes the six source/proof/test files and three predecessor
context files. This verification note and HANDOFF.md are not hashed, to
avoid circular receipt dependencies. Frozen predecessor receipts retain:

- hidden mode access: 616b57bda5a4d4f2d2655b953342f9a0a9d4b13eb83031a3d46e000f420387b1
- path word sampler: 33704f98675d2e685b2eb49536126f3afc339a35fb0c3fdd137c1abada1a3341
- rational transfer: ce694d62fdb30385174451a8d5224708dbd03bd6eff00b93f53e1fcca4ac9d49

## Live Cases

Every case executes TWO complex-rational transfer factors, mixed X/Z
measurements, exact normalization, two seeded actual samples and exact
sample probabilities. These are NOT thermal-factor executions.

| Graph | Vertices | Pair states/contract | Conditional thermal degree bound | Thermal log2 pair-state bound |
| --- | ---: | ---: | ---: | ---: |
| Odd cycle | 5 | 2546 | 494 | 2964 |
| Branching cliques | 6 | 499 | 560 | 2240 |
| Non-line path power | 7 | 1280 | 560 | 2240 |
| Binary-tree line graph | 30 | 3921 | 828 | 3312 |

For the first three, ALL full-output masses also match an independent exact
direct-Pauli reference, and bounded exhaustive checks confirm the ECF graph
property. The 30-vertex case has an explicit clique-tree certificate; its
entire output space is not enumerated. Seeded PRNG runs are reproducibility
controls, not a mathematical proof of fresh random bits.

## Adversarial Coverage

- Gaussian factors without conjugate pairing and mixed local measurement;
  all partial marginals on bounded fixtures, not just a prefix or histogram.
- Three-factor crossing orientation; unsigned shortcut fails in X readout.
- Scalar-zero products rejected; empty products correctly produce vacuum.
- Invalid running intersection, missing edges/vertices, false independence
  bound, duplicated edges/vertices, and bad arc endpoints rejected.
- Two replicas charged; oversized resource demands refused before expansion.
- Circular-arc bags, universal joins and genuinely branching clique gluing.
- Non-line-graph ECF fixture; non-ECF even-cycle exact product allowed without
  importing the thermal identity. Its scalar inversion identity fails.
- Full thermal-vector repeated-factor controls on an odd cycle and branching
  graph use dense expm ONLY as a bounded reference, with an analytic bound.
- Exact positive-even polynomial norm controls and real-path agreement with
  the preceding signed automaton, including its X normalization convention.
- Conditional thermal plans retain unresolved ECF recognition, factor roots
  and full execution flags, even when their scalar approximation is certified.

The 50-test and 58-test intermediate suites passed before later controls
were added. During API inspection, SymPy's GaussianRational was found not
to expose conjugate(); the implementation uses its exact real/imaginary
components. No production or proof claim relies on that failed API probe.

## What These Checks Do Not Establish

No independent/formal proof review of the general upper-bound composition;
no automatic general ECF decomposition frontend; no certified thermal roots;
no practical full thermal run; no arbitrary coherent-decoder simulation;
no novelty/optimality claim; no polynomial dequantization or quantum speedup.

Main qsearch validate, main full tests, and node --check were NOT run: no main
files were integrated or changed, and the verified Developer checkout is
still absent. The isolated result and handoff do not pretend otherwise.
