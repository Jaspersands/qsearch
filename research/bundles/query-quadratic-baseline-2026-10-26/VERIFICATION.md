# Verification: Query-Quadratic Classical Gate

2026-10-26. Workspace /Users/jaspersands/Developer/qsearch-research-work.
No native curve, geometric quotient, isogeny division or quantum circuit ran.
The new parent deductions have not been independently reviewed.

## Completed Commands

    /opt/anaconda3/bin/python -W error -m pytest -q query-quadratic-baseline-2026-10-26

27 passed in0.72s, warnings as errors, no skips.

    /opt/anaconda3/bin/python -W error -m pytest -q query-quadratic-baseline-2026-10-26 active-coset-density-2026-10-26 full-suborder-impact-audit-2026-10-26 native-suborder-preprocessing-2026-10-26 additive-framed-source-2026-10-26 classical-symmetry-harvest-2026-10-26 native-nonbass-realization-2026-10-26 local-order-scope-2026-10-26

187 passed in24.67s, warnings as errors, no skips. This is an eight-bundle
focused regression, not an all-tests claim for the unavailable main repo.

    /opt/anaconda3/bin/python -m py_compile query-quadratic-baseline-2026-10-26/quadratic_gate.py query-quadratic-baseline-2026-10-26/test_quadratic_gate.py
    /opt/anaconda3/bin/python native-nonbass-realization-2026-10-26/replay_realization.py --check
    /opt/anaconda3/bin/python classical-symmetry-harvest-2026-10-26/replay_harvest.py --check
    /opt/anaconda3/bin/python additive-framed-source-2026-10-26/replay_additive_source.py --check

All completed with exit0. All command sessions finished.

## Exact Evidence

The checks cover primitive intersection versus imprimitive query order;
commutator centralizers; factorization/product validation; odd-prime
overorder polynomials and discriminant scaling; multi-prime saturation in
supplied arithmetic without factoring unrelated discriminant primes;
integral-norm candidates rejected by the TRUE supplied target order;
scalar-unit completeness for p=103,q=5; exact q^2-1 growth count across
all q^3 residue triples; independence from the hidden line at q=3,5,7;
complete full-index centered counts at d=3,5; the transverse-corner
necessity; scalar exceptions; and invalid/even/fractional inputs.

The p=103,q=5 count is24 useful candidates among125 residue triples. This
is a SUPPLIED-ORDER verification of the analytic count, not125 native
division calls or a measured native algorithm. Complete finite unit
enumeration confirms the target has only +/-1; these hits are not simply
missing cheap units. It still is not a hard-instance or asymptotic test.

The helpers never return native_integrality_certified=true. Geometry,
native field arithmetic, evaluator compilation/compression and source
construction are not implemented by them. General success probabilities
come from the written proofs, not finite extrapolation.

The main local checkout was checked and remained absent. No qsearch.py,
main test suite, node --check index.js, UI, registry, staging/moving source,
Git commit or push was touched. No new reviewer was used.

## SHA-256

    a15870b074c5ae2765bee5bb36c891b42c499d2de69ad02d666a3f95acbc3d15 QUADRATIC_BASELINE.md
    396f396320bcbbcb071d469a0e0098be0e6410cdc54b2dcb8140b3b1c5a530f3 quadratic_gate.py
    12c89fe2ba9925eaaa742b2c837ec58c17418ee2627fc397704fc9361a09ad53 test_quadratic_gate.py

The prior active-coset proof remains unchanged:

    60fdb0114a04c292ccbfb459938a29f6d083586e550347f70e5eec7d80ad06d6 active-coset-density-2026-10-26/ACTIVE_COSETS.md
