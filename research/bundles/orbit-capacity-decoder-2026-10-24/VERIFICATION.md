# Verification: Source-Specific Capacity Application

2026-10-24. LOCAL UNREVIEWED mathematical application with an explicit
external preprint decoder dependency. No capacity backend or quantum
circuit was run. This is not a whole-repository validation result.

## Executed Controls

- 15 focused tests passed in0.26s, warnings as errors, no skips.
- Broad external research suite: **641 passed in6.93s**, warnings as
  errors, no skips. These are the preceding626 controls plus15 new ones.
- capacity.py, test_capacity.py and make_receipt.py passed py_compile.
- The full producer ran twice after the final source changes. Its JSON
  outputs were byte-identical, verified by cmp exit0.
- All9 source/dependency/snapshot hashes matched after the final run.
- The100 fixed finite received-syndrome controls agreed with a DIFFERENT
  complete-list computation: support enumeration versus code-message
  enumeration. They include inputs without a bounded-source promise.

No owned process remains running. No independent reviewer was launched;
the one previously authorized Rees review is already finished and is not
evidence for this proof.

## Results Actually Observed

1. p31,M7,K6, source weight4, whole cap5: the old Prony certificate has
   rank at most3 and returns ABSTAIN_INCONSISTENT. The complete reference
   list contains exactly the original error, recovered from the syndrome
   alone. This is a Fourier-label decoder check, NOT a native polynomial
   solving the original halfset predicates or a quantum execution.
2. The radius guard matters: a fixed source error has exactly one candidate
   at radius3 and two at radius4. The whole-cap receiver rejects ambiguity.
3. At p13,M4,K3,w2,C2, all28561 free-frequency assignments were enumerated
   with fixed nonzero last frequencies1/2. Exactly13 collide, giving
   1/2197=1/13^3. All13 saved collision cases were checked by the full-list
   receiver. The count matches the derived finite support bound.
4. Twenty-one fixed nonzero labels have explicit DIFFERENT competitors at
   the endpoint capK, each independently checked against the original
   syndrome and support cap. This checks the constructive endpoint proof.
5. Scalar and Cartesian budget limits return unavailable/incomplete, not
   a singleton. Mixed row supports whose union is too large are rejected.
   The first version of that test used a fixture with no actual mismatched
   row combinations; it failed and was replaced with a genuinely rejecting
   fixture, rather than weakening the assertion or changing the decoder.

## Analytic Output, Not Execution

The new ledger has p12289,M4096,K2621,n7863,D2375,C2376 and rate2621/4096,
approximately0.640. Its guarded collision exponent is492; the old receiver
has only735 recurrence equations for2375 active columns. Exact rational
arithmetic with upward dyadic rounding gives the CONDITIONAL ideal
one-attempt failure upper bound approximately3.134836389875868e-9.

The finite minimum length and concrete implementation costs of the cited
capacity theorem are NOT instantiated. The ledger therefore does not
certify an executable finite quantum algorithm at p12289. The asymptotic
R>1/2 deduction is conditional on that theorem and the existing source/
coherent guard derivation. Classical separation, novelty, natural reduction
and independent proof acceptance remain unestablished.

## Provenance And Changed Files

Receipt SHA256:
`64194d0dd6bf6b74bb0c84f196b58eaf8eeeeceef6e3efe6b7f18bdf9f947cb1`

The downloaded v1 primary-paper HTML snapshot has SHA256:
`7ee3f94e0d5b0c8b1cf79405ece4e5838ce2e0c3a1fa998a80f66a3f2cd536ee`

This pass created eight external files:

- CAPACITY.md: exact source/collision proof, known decoder dependency,
  conditional rate consequence, endpoint limitation and falsifiers.
- capacity.py: bounded complete-list reference, exact ambiguity bounds,
  endpoint competitor construction and conditional scalar ledger.
- test_capacity.py: independent enumerations and adversarial controls.
- make_receipt.py: fixed-case live producer and source manifest.
- receipt.json: complete lists, collision witnesses and analytic ledger.
- capacity-theorem.html: frozen primary-paper theorem provenance, not code.
- HANDOFF.md: bounded integration/research instructions.
- VERIFICATION.md: this evidence record.

The parent RESEARCH_CHECKPOINT_2026-10-23.md was updated. No original
Desktop source, migration staging, main CLI, registry, UI or Git metadata
was edited. The intended Developer checkout was still absent when checked.
No whole-repo tests, qsearch.py validate, node --check, commit or push was
performed. Existing source/guard/classical artifacts remain unchanged.

## Reproduction

From this directory:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_capacity.py
/opt/anaconda3/bin/python -m py_compile capacity.py test_capacity.py make_receipt.py
/opt/anaconda3/bin/python make_receipt.py --output /tmp/capacity-replay.json
cmp receipt.json /tmp/capacity-replay.json
```

Do not describe these commands as implementing the asymptotic capacity
decoder or executing the quantum construction. The scope flags deliberately
keep those statements false.
