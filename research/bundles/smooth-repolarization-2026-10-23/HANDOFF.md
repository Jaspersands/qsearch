# Review Before Wiring

All work is isolated from the still-unverified Desktop migration. Do not
copy it into source or staging until migration has been completed and verified.

## Principal Research Tasks

1. Independently audit Sections 1-4 of SMOOTH_REPOLARIZATION.md. In particular:
   quaternion-Hermitian quadratic identity; geometric integrality of F;
   maximal isotropy of its kernel; base-field control; and marked transport.
2. Check the full composition with SYMPLECTIC_FIELD_CHART_REDUCTION.md.
   Stabilization leaves the acting group Sp_4, but marking rigidity uses 16.
3. Try to extract a polynomial classical kernel-recovery algorithm from the
   same weak auxiliary inputs and these geometric labels. The known descent
   membership test and sign-enumeration baseline are mandatory comparators.
   Also allow classical interpolation of phi*a*phi^dagger for every supplied
   polarized a, as detailed in Section 6. Do not treat target-ring saturation
   as free once a collection of represented endomorphisms is available.
4. Finish comparison with Chen et al. 2305.19897 and higher-dimensional module
   conversion. Key input contracts in 2026/276 were read and recorded in the
   note; the full novelty comparison remains incomplete. Do not claim novelty
   from a keyword search or from distinct theorem statements alone.

## Lower-Reasoning Integration Tasks For Gemini

- Preserve the status PROPOSED_SOURCE_LEMMA_REVIEW_PENDING. No speedup admission.
- Integrate the exact control module and tests only after the migration boundary
  is clear. Give the replay module a unique package name; existing isolated
  bundles contain unrelated generic replay.py modules.
- Add a registry artifact linking the proposal, input contract and falsifiers.
  Do not globally mark the old model-conversion blocker resolved for g>2.
- Implement a geometric backend only after review, using existing theta code
  and DIRECT prime-square quotient calls. Do not assume every maximal isotropic
  prime-square kernel is free, or reuse Algorithm 1's loop unchanged.
- Cover t=2 by returning the old eightfold product with direct markings.
- Construct a uniform trace bound from the actual elementary-lift compiler.
  Observed maxima from a sweep do not meet the coherent source contract.
- Verify geometric equality for different lifts of the same m, different
  four-square choices, and same/different hidden-kernel cosets at small honest
  instances. These are source-correctness tests, not hardness benchmarks.
- Keep common-unit weak evaluation at r^2 explicit. Refuse prime-only data
  rather than silently synthesize missing higher-order information.
- Run repository tests, syntax checks and qsearch validate after integration.
  This isolated pass cannot certify the moving repository's CLI or UI.

## Local Replay

Use /opt/anaconda3/bin/python with PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache
and PYTEST_DISABLE_PLUGIN_AUTOLOAD=1. Run this bundle's tests in its own process:

    python -m pytest -q -p no:cacheprovider test_smooth_repolarization.py
    python replay_smooth_repolarization.py

No geometric backend, classical secret-kernel recovery, or quantum execution
has occurred. The result is an exact, falsifiable mathematical proposal.
