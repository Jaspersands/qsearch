# Verification And Scope

2026-10-24. Local classical reduction, not independent review or novelty.

## Executed

From `/Users/jaspersands/Developer/qsearch-research-work`:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -W error -m pytest -q -p no:cacheprovider diagonal-source-baseline-2026-10-24/test_diagonal_source.py rees-coarse-spectrum-2026-10-24/test_coarse_spectrum.py rees-code-support-2026-10-24/test_code_support.py rees-spectral-mixture-2026-10-24/test_spectral_mixture.py
```

Final result: **106 passed in 0.42s**, including29 new tests. Warnings were
errors; no skips. Syntax compilation passed for all three new Python files.
`run_audit.py --output receipt.json` ran. A fresh in-memory replay equaled
the saved parsed JSON. All eight new local/dependency hashes matched.
All eleven source/dependency hashes in the predecessor coarse-spectrum
receipt also matched. No predecessor source file was modified.

Final receipt SHA256:

`a1e7986dbcf1597b3d682698edb75ebeab984148f51707915a30ff28e91f4988`

## Live Sample Control

The sampler received exactly196608 labels from a reproducible rational
three-point source. It did not receive the probability table or support.
The reference source has minimum weight `2^-200` and two unequal heavy
weights differing by `2^-179`. The tiny label was unseen, as permitted.
The two observed counts were98195 and98413.

For the supplied UT3(F5) action, reference exhaustion of125 group elements
gave the SAME subgroup before rounding, after rounding, and after colored
affine encoding. That subgroup has order5 and normal core of order1.
The coarsening loss was exactly877/98304, below the analytic3/32 bound.
The true minimum outside TV distance is1-2^-200, exceeding promised3/4.

This is an easy finite reference and a seeded-PRNG execution, not an
implementation of the general group algorithm, a new oracle candidate,
an information-theoretic RNG test or evidence of classical hardness.

## Countercontrols

- Unequal empirical counts must not split equal true weights.
- Chained intervals, not fixed bins or complete-linkage clusters, implement
  the stated rounding rule.
- All720 permutations of a six-label reference agree on the original and
  rounded weighted stabilizers under a valid separation promise.
- A false global gap can add a spurious symmetry even with accurate
  frequencies. Sampling cannot certify that global promise.
- Removing colors or requiring pointwise fixing changes the target group.
- Dephasing a non-diagonal pure state can change its symmetry subgroup;
  polynomial matrix rank does not imply sparse computational support.
- An insufficient sample budget fails BEFORE querying the source; observed
  rank violations and malformed labels abort rather than producing an answer.
- A127-bit-prime affine encoding runs without enumerating the field or basis.

The rank128 resource ledger is NOT executed: its conservative bound asks
for643252956954624 samples. Polynomial bounds are not practical timings.

## Not Verified Or Changed

The general Luks set-stabilizer backend is cited, not implemented or tested.
No independent proof review, new Lean check, quantum circuit, natural hard
application, full repository suite, `qsearch.py validate`, or UI check ran.
The exploratory HDQI star experiment was abandoned BEFORE implementation
because an existing all-orders gap theorem already covers that family.
No new HDQI gap theorem emerged.

All seven bundle files and the parent checkpoint are outside the moving
checkout. No main/staging, registry, CLI/UI, Git, migration or other-agent
files were changed. The intended Developer checkout was checked and remains
absent. No additional reviewer was started. All owned processes finished.
