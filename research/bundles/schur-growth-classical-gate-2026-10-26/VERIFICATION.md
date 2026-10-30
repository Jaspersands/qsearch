# Verification: 2026-10-26

Workdir: `/Users/jaspersands/Developer/qsearch-research-work`.
Python: `/opt/anaconda3/bin/python` 3.13.5, python-flint 0.9.0.
No independent reviewer or proof assistant checked the new deduction.

## Commands And Observed Results

All pytest runs used `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`,
`PYTHONPYCACHEPREFIX=/tmp/qsearch-schur-gate-pycache`, `-p no:cacheprovider`
and `-W error`.

1. New `test_schur_gate.py`: **36 passed in 1.07s**, no skips or warnings.
2. Five-bundle regression: **187 passed in 4.30s**, no skips or warnings.
   Files: the new suite, `inverse-trace-local-list-2026-10-26/test_local_list.py`,
   `inverse-trace-modular-norm-2026-10-25/test_modular_norm.py`,
   `inverse-trace-norm-transfer-2026-10-23/test_norm_transfer.py` and
   `inverse-trace-residual-2026-10-23/test_residual_sat.py`.
3. `python -m py_compile` on schur_gate.py, finite_controls.py,
   test_schur_gate.py and verify_schur_gate.py: exit 0.
4. `python schur-growth-classical-gate-2026-10-26/verify_schur_gate.py --write`
   and `--check`: exact replay passes, including eight source/dependency hashes.
   Receipt SHA256:
   `778b6595a508c482fdfc9e8bb5001c6eb0967329bafbb54d128592fff32c6f64`.
5. Previous inverse-trace local-list and modular-norm `--check` commands both
   pass, preserving their seven and ten hashes respectively. Their receipt
   SHA256 values remain
   `c75052e06a71e2afde22c776c7711d114b0cea8f964327d29f09beeb494556bb`
   and `ca9170b9b06fc50c7454080837841cfb6681e71b6cc0430df889c654186c9fab`.

## Tested Scope

- Exact field arithmetic, Schur powers, full-support-unit verification,
  shortened-space dimensions and comparison factors.
- All 121 original syndromes for the Reed-Solomon norm construction, all
  729 annihilators of the F3 parity control, and all 1024 RS zero restrictions.
- Smooth genus-one, two and three curve controls. Their evaluated RR spaces
  equal the computed Schur square/cube as rowspaces, not merely dimensions.
- All 8206 nonzero annihilators in those three controls pass, with zero the
  only failing annihilator in each case. Each successful attempt also checks
  the original equation. The genus-three control is outside the growth gate.
- Every nonzero elliptic codeword satisfies the zero-set surjectivity and
  shortening identities. Its exact C=133/1331 is distinguished from the
  actual rank-failure probability 1/1331.
- 361 changed-basis, permuted-column, nonconstant-scaled genus-three
  syndromes return independently checked original-relation witnesses.
- A direct-sum countercontrol has a bad first annihilator but a successful
  random attempt. UNKNOWN is preserved. No AG promise is inferred from a
  nonzero kernel or favorable dimensions.
- Composite/even fields, noncanonical entries, wrong predicates, bad
  nonsquares/annihilators and excessive diagnostic enumeration are rejected.

## Files And Limits

Created schur_gate.py, finite_controls.py, test_schur_gate.py,
verify_schur_gate.py, SCHUR_AG_CLASSICAL.md, HANDOFF.md, receipt.json and
this note. Updated the isolated research checkpoint only.

The intended main local checkout was rechecked and remains absent. This
workspace is not Git. No original/staging tree, main registry, CLI or UI was
edited; no commit/push occurred. Full-repository pytest, qsearch validate
and node syntax checks were NOT run because those application files are
not in this isolated workspace. No quantum execution, new native inverse-
trace solver, uniform sampler or Shor-level result is claimed.
