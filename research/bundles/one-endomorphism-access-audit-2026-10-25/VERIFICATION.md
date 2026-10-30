# Verification

2026-10-25. All writes stayed in the isolated local research workspace.
The main rigidity note was READ and copied as an unchanged snapshot, with
matching SHA256. No moving source/staging changes, main CLI/UI integration,
central registry modification, commit or push. The intended main Developer
checkout was still absent. No new independent reviewer was started.

## Executed Checks

From `/Users/jaspersands/Developer/qsearch-research-work`:

```sh
env OPENBLAS_NUM_THREADS=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error one-endomorphism-access-audit-2026-10-25 suborder-transcript-2026-10-25 large-prime-source-audit-2026-10-25
/opt/anaconda3/bin/python -m py_compile one-endomorphism-access-audit-2026-10-25/access_audit.py one-endomorphism-access-audit-2026-10-25/test_access_audit.py one-endomorphism-access-audit-2026-10-25/replay_access_audit.py
env OPENBLAS_NUM_THREADS=1 /opt/anaconda3/bin/python one-endomorphism-access-audit-2026-10-25/replay_access_audit.py --write --check
env OPENBLAS_NUM_THREADS=1 /opt/anaconda3/bin/python one-endomorphism-access-audit-2026-10-25/replay_access_audit.py --check
```

96 PASS in 2.78s, including all 31 new access-audit tests and the preceding
65 transcript/calibration tests. Warnings-as-errors, no skips or failures.
Three syntax checks and both replay checks PASS. Receipt SHA256:
`30f042334f22ad1ba98a087a9192727e54e431606d960f8a66d8dd6814731ec3`.

Validation was proportional to this new isolated audit. The prior 451-test
source milestone is historical, not rerun here; it is documented in the
preceding bundle. Main repository tests, qsearch.py validate and node checks
were not run because no main code or UI was edited or integrated. All required
command processes completed.

## Exact Evidence

- Projective centralizer counts at primes 3,5,7,13,17 equal 4,4,8,12,16.
- Product-copy controls at primes 3,5,7 and copy counts 1,2,3 give generated
  algebra dimensions 2,8,18 instead of 4,16,36, with commutant dimension two.
- Four Frobenius-product controls retain dimension eight and commutant two.
  These are typed finite-module controls, not a native generic-curve backend.
- Genuine supplied h and 1-h in characteristic 11 have degree three,
  distinct kernels and different transported integral Gram operators despite
  agreeing on the same known quadratic action. Checked auxiliary primes:
  5,7,13,17.
- Primitive maps h^k were checked at k=1,2,4,8,16,32,64; the written proof
  covers every positive k. This refutes a universal primitive-map bound,
  not the existence of a small representative.
- Two integral automorphisms have Gram matrices over Q(j), while their
  product does not. This falsifies an assumed HSP query-group closure.

Four scoped negative records are retained. No quantum lower bound, general
no-go theorem, native hardness, independent review, novelty, unknown-map
recovery or speedup is claimed. A new combined-proof reviewer was requested
asynchronously, but approval and review are not assumed. Goal remains ACTIVE.
