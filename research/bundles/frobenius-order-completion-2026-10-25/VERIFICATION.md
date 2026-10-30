# Verification

2026-10-25. This is an isolated research bundle, not an integrated main
repository subsystem. All commands below ran in this directory using
/opt/anaconda3/bin/python. No owned subprocess remains running.

## Final Checks

    python -B -W error -m pytest -q -p no:cacheprovider test_completion.py \
      ../product-corner-attack-2026-10-23/test_product_corners.py \
      ../kernel-output-2026-10-23/test_kernel_output.py \
      ../kernel-output-2026-10-23/test_uniform_source_bound.py

96 tests passed in 11.66 seconds: 25 new, 24 predecessor completion tests
and 47 kernel-output/source-bound tests. No skips; warnings are errors.

    python -W error -m py_compile completion.py test_completion.py replay.py

All three files pass syntax compilation. Two separate subsequent runs of
replay.py produced exactly identical receipt bytes. All five recorded
source hashes and five dependency hashes match the files; all six source
hashes in the frozen product-corner receipt remain intact.

Final receipt SHA256:

    f0977ad2eaef256b43f9dbf1593733b18a658669daa428338fac7f0a79878c0e

## What Was Tested

- An actual smooth genus-two curve over F_5: zero Cartier--Manin matrix,
  point counts 6 and 26 checked by two counting methods, chi=T^4+25.
- Exact degree-four factorization gates, including fixed 127-bit inputs,
  individually self-reciprocal factors and correctly retained failures.
- All 40 Lagrangian planes at ell=3. All complete with powers 0,1,2;
  sixteen do not complete with only powers 0,1. Literal matrix-span ranks
  agree with squared cyclic-space ranks in every case.
- Characteristic-polynomial CRT at auxiliary primes 7,11, M=77>60;
  insufficient CRT and invalid polarized matrices do not pass.
- Two integral maximal quaternion-order controls, with HNF index one and
  Gram determinant p^8. Scalar-map completion retains index ell^16.
- All 144 weak auxiliary actions match direct integral-map evaluation;
  a common scalar cancels, independent column masks do not.
- Repeated factors, paired distinct factors, scalar extension-field
  Frobenius, self-adjoint quadratic maps, invalid input and capped control
  enumeration. No negative control is promoted to a hardness result.

## What Was Not Tested Or Established

No incoming geometric weak isogeny was constructed for the curve. No
actual point-based target-order extraction or native secret-kernel recovery
was executed. Reference-coordinate HNF controls are not that algorithm.
The general proofs, bit-complexity composition, prior-art novelty and
applicability to a growing native family lack independent review.

The intended Developer checkout was still absent when inspected; the
Desktop checkout remains migration-sensitive. Main/staging files, CLI,
UI, registries, prior proofs, receipts and Git were not edited. Full main
repository tests, qsearch.py validate and node --check index.js were not
run. There is no new commit or push, no background search worker, and no
quantum speedup or general source-dequantization claim.
