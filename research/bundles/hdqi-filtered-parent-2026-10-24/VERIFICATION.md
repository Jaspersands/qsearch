# Verification And Scope

## Completed Checks

31 new tests plus 56 dependency tests pass: 87 total, with warnings treated
as errors. Four Python files pass py_compile. Two live receipt generations
match byte for byte. Four recorded source/dependency hashes match.

The new checks include:

- An independent ordered-word operator map for complex-time-phase
  constraints, including the transpose/conjugation and Clifford factors.
- Exact continuous-time frequency contraction against adaptive numerical
  integration, and the real-time LCU against an independent quadrature.
- Positive finite parents, pilot kernels and term norm bounds on multiple
  graphs with signed, unequal and zero couplings.
- All 64 labeled four-vertex graphs for the dyadic first-order cancellation
  and single-excitation second-order formula, with signed/zero couplings.
- Finite-difference controls of the Taylor and path-derivative calculations.
- A priced quadrature control, invalid inputs, dense-size limits and large
  resource plans that are not silently executed.
- The exact commuting gap and the isolated-vertex temperature counterexample.

Receipt: five Taylor rows, 15 finite spectra (m<=5), one explicit quadrature
control and an analytic commuting counterexample. Maximum pilot-kernel
residual is about 1.6e-15. None is a universal gap certificate.

For the two-qubit quadrature control at beta=0.3 and delta=0.05, the
measured operator error is 0.00717900155, below the analytic bound
0.04998821244. The plan uses 437 outer and 1569 inner bins; maximum real
time is about 0.7862. This was a CLASSICAL spectral reference of the grid,
not execution of the corresponding quantum circuit. Arithmetic-rounding
and Hamiltonian-simulation errors remain separate implementation budgets.

## Issues Found During Verification

The first fixed-node integration check under-resolved the narrow sech
density. Adaptive integration independently confirms the frequency formula.
The underlying parent formula was not changed to match that coarse grid.

A beta=10 one-qubit check exposed floating-point leakage into an exactly
zero Bohr component, dominating the true approximately 4.1e-40 gap. The
exact two-frequency representation supplies that control; tiny dense gaps
are explicitly unresolved, not assigned trustworthy relative precision.
The initial unguarded beta^2 d gap target was corrected to beta^2(d+1),
or equivalently the intended regime with a separate commuting treatment.

## Still Unproved Or Unperformed

No uniform GLOBAL gap bound, asymptotic state-preparation algorithm,
physical HDQI decoder application, operational quantum speedup, novelty
review, formal proof or independent review of this pass. The kernel/access
and derivative arguments are local written proofs with finite controls.

No quantum circuit/hardware execution, full-repository tests, qsearch
validation, node check, registry admission, UI changes, commits or pushes.
The migration worker remained live and the verified final checkout absent.
The source and staging copies were not edited. All changes live in this
external six-file bundle and the external research checkpoint.

Files: filtered_parent.py, test_filtered_parent.py, FILTERED_PARENT.md,
receipt.json, HANDOFF.md, VERIFICATION.md. The previous parent-gap bundle
was read and tested but not modified by this pass.
