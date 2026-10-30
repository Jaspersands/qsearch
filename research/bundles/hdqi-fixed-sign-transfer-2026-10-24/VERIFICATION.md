# Verification And Limits

2026-10-24, external research workspace only.

## Executed

- 64 focused tests passed in 0.56s with warnings as errors and pytest
  plugin autoload disabled. Repeated-Z formulas were compared with actual
  physical decoder matrices; all 32 signs at K=5 recover the average
  identity. Random noncommuting controls, zero couplings, identity terms,
  Pauli-gauge invariance, collision witnesses, exact kernel sums, rational
  bounds and both enumeration budgets were checked.
- The focused tests plus the prior 760-test external regression selection
  passed: **824 passed in 18.34s**, no warnings or skips. This covered the
  prior HDQI pilot/output/parent baselines, relative-interference-distance,
  Rees formal/class-three controls, orbit/OPI/decoder controls, affine
  converse, BPQM cluster/tree controls and central-rank code.
- Three files passed py_compile: fixed_sign.py, test_fixed_sign.py and
  make_receipt.py. Bytecode was directed to /tmp, not the source checkout.
- make_receipt.py generated receipt.json. Independent rerun produced
  byte-identical JSON; all 12 recorded source hashes matched.
- Receipt SHA256:
  `7a1d0053a036e3c1db6004c0bec6e388c5089c2e2cddf3c498fb29cfdbb4e762`.
- The K=65,536 negative certificate uses exact rational comparisons,
  not numerical hyperbolic-function values or a large dense pilot.
- The n=32,m=65 positive transfer certificate enumerated 1 nonzero kernel
  word and 2,146 decoder words; no 65-qubit pilot was constructed.

Initial expanded tests incorrectly supplied beta>1 to an existing model
whose documented executable domain is beta in [0,1]. Those fixture inputs
were corrected, with no change to the dependency or mathematical claim.
Final tests and receipt were rerun after the correction.

Reproduce the focused run from the external workspace:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  PYTHONPYCACHEPREFIX=/tmp/qsearch-fixed-sign-pycache \
  PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest \
  -q -p no:cacheprovider -W error \
  hdqi-fixed-sign-transfer-2026-10-24/test_fixed_sign.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  PYTHONPYCACHEPREFIX=/tmp/qsearch-fixed-sign-pycache \
  /opt/anaconda3/bin/python \
  hdqi-fixed-sign-transfer-2026-10-24/make_receipt.py
```

## What These Checks Do Not Establish

The all-size deductions remain LOCAL UNREVIEWED. Dense tests are capped
at m<=8,n<=3 and are not asymptotic evidence. The sufficient kernel bound
depends on the cited thermal inclusion theorem. Exact rational arithmetic
is not proof-assistant verification. No new independent reviewer was used.

No actual quantum preparation/circuit, new native hard family, general
degree-scale gap result, or speedup was produced. The positive transfer
control assumes an ideal pilot and does not prove that its output is hard
to sample classically. The negative result concerns a fixed-sign inference,
not the published random-sign theorem or all possible preparation methods.

No main-source/staging, registry, CLI, UI, Git, commit or push changes were
made. The intended main Developer checkout was checked and still absent;
migration is not verified. Whole-repository pytest, qsearch.py validate
and node --check index.js were not run. Seven files in this bundle and
the external checkpoint are this pass's changed artifacts. No owned test
or receipt process remains running.
