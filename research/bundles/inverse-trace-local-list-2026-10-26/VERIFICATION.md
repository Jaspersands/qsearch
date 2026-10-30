# Verification: 2026-10-26

Working directory: `/Users/jaspersands/Developer/qsearch-research-work`.
Python: `/opt/anaconda3/bin/python` (3.13.5); python-flint 0.9.0.
No independent reviewer or proof assistant was used for this extension.

## Commands And Observed Results

All pytest commands used `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`,
`PYTHONPYCACHEPREFIX=/tmp/qsearch-local-list-pycache`, `-p no:cacheprovider`
and `-W error`.

1. `python -m pytest -q -p no:cacheprovider -W error inverse-trace-local-list-2026-10-26/test_local_list.py`
   passed **63 tests in 1.69s**, no skips or warnings.
2. The same command with the four files `test_local_list.py`,
   `inverse-trace-modular-norm-2026-10-25/test_modular_norm.py`,
   `inverse-trace-norm-transfer-2026-10-23/test_norm_transfer.py` and
   `inverse-trace-residual-2026-10-23/test_residual_sat.py` passed
   **151 tests in 2.78s**, no skips or warnings.
3. `python -m py_compile` on the three new Python files passed (exit 0).
4. `python inverse-trace-local-list-2026-10-26/verify_local_list.py --write`
   generated the receipt; `--check` replayed it exactly, including seven
   source/dependency hashes. Receipt SHA256:
   `c75052e06a71e2afde22c776c7711d114b0cea8f964327d29f09beeb494556bb`.
5. `python inverse-trace-modular-norm-2026-10-25/verify_modular_norm.py --check`
   passed, preserving ten hashes and its existing receipt SHA256
   `ca9170b9b06fc50c7454080837841cfb6681e71b6cc0430df889c654186c9fab`.

## What Was Actually Checked

- Exact inverse-trace Fourier and Kloosterman identities at q=4,8,32,128.
- All 28 pairs at q=8 and all 496 pairs at q=32 have zero unambiguous
  subspace dimension. These are bounded controls, not the asymptotic proof.
- Exact posterior identities for rational pure and mixed positive effects.
- Sharp two-label posterior attained at every nonzero label difference in
  the tested fields. Fourier readout still succeeds with probability 1/2.
- Affine halfsets and the n=2 inverse-trace alphabet admit a pair outcome;
  a sufficiently large list is not rejected on the native q=32 alphabet.
- Integer-only necessary list bounds and exact rounding through n=1024.
  At n=31 an error-free outcome needs at least 23,172 labels; this is an
  analytic lower bound, not a numerical experiment over 2^31 symbols.
- The old n=7, N=49, K=6 native witness still passes its original equations
  on its original points and targets. No new native search was run.
- Invalid field presentations, oversized finite enumeration, zero-mass
  outcomes, duplicate labels, inexact inputs and changed priors are rejected.

## Files And Limits

Created local_list.py, test_local_list.py, verify_local_list.py,
LOCAL_LIST_BARRIER.md, HANDOFF.md, this verification note and receipt.json.
Updated only the isolated top-level research checkpoint. Existing native
arithmetic, previous receipts, source constructions and reviews are unchanged.

The main local checkout was checked and remains absent. This directory is
not Git. No main CLI/UI/registry edits, commit or push occurred. Full-repo
pytest, `qsearch.py validate`, and `node --check index.js` were NOT run:
those application files are not in this isolated research workspace.
No native quantum execution, full dequantization, global-decoder rejection,
classical-hardness proof, or Shor-level result follows from these checks.
