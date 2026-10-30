# Handoff: Native Order-Five Target Gate

This bundle is external to the migration-sensitive checkout. Do not
integrate, move the source or edit the main registry/Git until the local
checkout is verified. Read ORDER_FIVE_GATE.md before changing any status.

## What Gemini Can Integrate

1. Recognize only a supplied verified model y^2=x^5+c with nonzero
   prime-field c, prime p>5, p=4 mod 5. Do not assume a generic target
   has a known isomorphism or descent to this family.
2. Build the public fifth root in F_(p^2). Extend it compatibly to each
   PAID auxiliary point field; the current frontend only evaluates
   F_(p^2) divisors and does not construct torsion bases.
3. Add target maps gamma and the actual p-Frobenius to the existing
   weak-basis observation packet, with squared Rosati bounds 4 and 4p.
   The source, target and isogeny may live over a larger common field;
   do not replace this pi by that larger field's scalar Frobenius.
4. Reuse reconstruct_pullbacks followed by extract_kernel with adjoints.
   The theorem predicts COMPLETE_UNDER_INPUT_PROMISE by layer two.
   A different outcome is a bug/input inconsistency to investigate, not
   a hard instance or a reason to provide the true kernel to the solver.
5. No geometric hiding-function calls are needed by this branch. Retain
   all original source-access, field and exact-CRT assumptions. Do not
   turn the finite point and local lattice controls into an end-to-end
   weak-isogeny receipt. That experiment has NOT been run.
6. Record a conditional classical exclusion for this supplied model,
   not a generic algorithm, literature novelty or positive quantum signal.
   Preserve independent_review_completed=false.

## Verification Commands

```sh
/opt/anaconda3/bin/python -B -W error -m pytest -q -x -p no:cacheprovider test_native_maps.py
/opt/anaconda3/bin/python -B -W error replay.py
```

The replay checks predecessor hashes and records native point/divisor
checks separately from local matrix controls. The exact main regression
suite and qsearch validate belong AFTER migration verification and actual
integration, not in this external proof pass. No daemon is installed.
