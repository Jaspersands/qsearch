# Review And Integration Handoff

Source and staging remain protected while migration is active. This bundle
is independent local work; do not integrate it into a moving checkout.

## Principal Research Tasks

1. Independently review the direct Hom bijection, Hermitian self-duality,
   prime-square order formula, and scalar-cancelled target action.
2. Review the preceding smooth-repolarization source and the full composition
   in KERNEL_TO_OUTPUT.md. Output conversion is no longer the key blocker.
3. Try to recover K classically from the SAME weak interface and canonical
   geometric labels, without granting a full target order. Membership alone
   and interpolated phi*a*phi^dagger are already mandatory classical tools.
4. Check whether a general repolarization/module theorem already gives the
   proposed source or makes the surface extension known. Do not infer novelty
   from an absent search hit.
5. Audit the 2026/276 module-conversion path if fully explicit maps are needed.
   Use the direct LEFT module J_K^dagger and its form, not a gratuitous PIP.
   Match field, base curve and output correspondence to the actual B.
6. UNIFORM_SOURCE_BOUND.md and uniform_source_bound.py now provide the
   missing worst-case compiler/trace/denominator calculation. Review the
   coherent compilation separately; it still assumes uniform bounded
   geometric subroutines and exact joint canonicalization.

## Gemini Integration Tasks After Migration Verification

- Integrate into a uniquely named theorem module and targeted tests.
- Keep the status CONDITIONAL_POSTPROCESSING, not accepted speedup.
- Use the already existing registry schema. Record the exact input promise:
  correct K, FULL O, compatible split and weak common-unit evaluation.
- Do not expose an order reconstruction as a classical secret-recovery solver.
- Use the independent module-left-order method if ell^2 splitting is unwanted.
- Connect the uniform compiler and shared D to the earlier source proposal.
  Never replace the uniform trace bound with an observed sweep maximum.
- Cache repeated basis inverses in performance-sensitive integration; do not
  change the exact arithmetic or weaken invariant checks.
- Add an entry to the existing proof dependency graph, linked to the source
  and receiver. Preserve unresolved source/quantum/prior-art/classical-attack
  obligations. Do not mark all project blockers resolved.
- Run repository tests, Python syntax checks, node --check index.js and
  python qsearch.py validate after integrating in a verified stable checkout.
  Those checks were not run against this moving repository.

## Replay

    env PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache \
      PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python \
      -m pytest -q -p no:cacheprovider test_kernel_output.py

    /opt/anaconda3/bin/python replay_kernel_output.py

The receipt records algebraic checks, not successful quantum execution.
