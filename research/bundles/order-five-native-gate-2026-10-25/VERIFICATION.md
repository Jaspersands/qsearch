# Verification

2026-10-25. Final runs used /opt/anaconda3/bin/python with warnings as
errors and pytest cache disabled. No skips or failures in the final runs.

| Scope | Passed | Pytest elapsed |
|---|---:|---:|
| New test_native_maps.py | 27 | 13.62s |
| Existing source-pullback/test_pullback.py rerun | 30 | 5.99s |

57 tests passed in this pass. The immediately preceding regular-spectrum
pass ran 160 tests, including these same 30 pullback tests. Thus the two
passes cover 187 DISTINCT tests, not 217. The preceding frozen source and
dependency manifests still match. Full main-repository validation was
not run, and these counts are not described as the entire repository suite.

The four new Python files passed py_compile. Two fresh replay processes
produced byte-identical receipts with no stderr. All six source and six
direct dependency hashes match. Each replay also checked the preceding
six source and 23 dependency hashes before using the old modules.

Receipt SHA256:

```text
1014304613a03080064fa3220886358ef6a5907fcd90b15f6e29aaf0da93c8fc
```

## Evidence

Actual C/F_19: y^2=x^5-1 has 438 F_(19^2) points including infinity.
Map and Frobenius-relation checks cover all 437 affine points, the
identity divisor and forty degree-two divisors. Public map acquisition
is checked at seven characteristics, including p=4294967279, without
field enumeration. The exhaustive point helper is separate and capped.

The local ell=11 matrix census covers all 1464 Lagrangians. Every orbit
has ranks (2,4,4). Sixteen separately constructed prime-square neighbor
controls give source image ranks (2,2) and match their reference kernel.
These are NOT an ell-torsion basis or incoming isogenies for the curve.

Regression controls reject missing inversion relations, incorrect spectra,
degenerate multipliers, unsupported characteristics/ell, invalid divisors,
and exceeded finite-control budgets. Tests retain changed-chart checks,
the counterexample to using the automorphism alone, and the common-field
scalar-Frobenius distinction.

During development the controls caught zero-field-element truthiness in
point enumeration, an incorrect census count in a test, a residue-versus-
signed-matrix comparison, and a deprecated composite-modulus SymPy inverse
path. These were fixed in the new files; the final tests/replays above
were rerun afterward. The composite inverse now uses the repository's
existing modular inverse helper, not a warning suppression.

## Not Established

No incoming weak geometric isogeny, auxiliary-torsion basis backend,
native kernel recovery, source hiding function, independent review,
generic classical solver, classical hardness or quantum speedup.
The mathematical deduction is written and self-checked, not formalized.

Eight research artifacts were added in this external bundle plus an
external checkpoint entry. Main/staging, CLI/UI, registry, Git, migration
and previous reviewer outputs were untouched. No extra reviewer was
spawned. All owned subprocesses finished; no background job was installed.
