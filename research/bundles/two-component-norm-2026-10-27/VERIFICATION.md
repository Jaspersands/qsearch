# Verification Scope

27 October 2026. No quantum run, human peer review or novelty certification.

## Executed Checks

From this bundle, using the existing Anaconda Python and FLINT runtime:

```text
env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-two-norm-pycache /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_norm_completion.py test_point_ratio.py ../small-prime-tower-2026-10-27/test_small_prime.py ../schur-growth-classical-gate-2026-10-26/test_schur_gate.py ../affine-resampling-audit-2026-10-27/test_repair.py ../matrix-geometry-lift-2026-10-26/test_point_lift.py ../one-point-plane-adapter-2026-10-26/test_plane_control.py
```

169 selected tests PASS in10.91s, including41 new controls. This is not
the full repository suite. All warnings are errors; no skips reported.
The tests exhaust an affine coefficient fiber, compare every exact
coordinate-zero probability, exhaust the small offset-image law, and
verify mixed quadratic cancellation. They retain the reviewer's example
where full syndrome rank and q^2>=2m nevertheless give a zero output.
They test cap/input guards, zero annihilator coordinates, and the exact
field-size cutoff without calling it an asymptotic fixed-prime result.

The elliptic controls compare the degree-eight product/colon recurrence
against independently computed local series through vanishing order9.
They verify sigma L(jO) with extra denominator zeros, ratio extraction
at a common zero, frame invariance, and rejection at a wrong vanishing
order. This is not the native genus41 section-ring adapter.

```text
env PYTHONPYCACHEPREFIX=/tmp/qsearch-two-norm-pycache /opt/anaconda3/bin/python -m py_compile norm_completion.py scope_bounds.py replay.py test_norm_completion.py test_point_ratio.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-two-norm-pycache /opt/anaconda3/bin/python replay.py --write
env PYTHONPYCACHEPREFIX=/tmp/qsearch-two-norm-pycache /opt/anaconda3/bin/python replay.py --check
```

Syntax and exact receipt replay PASS. Large exact rational bounds use
lossless hexadecimal integer strings rather than floating-point estimates.
The original decimal serialization exceeded Python's integer-string limit;
the explicit encoding and round-trip regression fix that diagnostic bug.
An arithmetic cutoff typo was also corrected: floor(1019^2/44)=23599.

## Actual Native Replay

The original fixed input has p1019, k43, m176 and full Schur cube rank176.
The auxiliary has dimension32, square dimension64, mixed-product rank160,
and mixed-annihilator dimension16. The saved h and A have no base columns.
Each of five fixed original syndromes gives a verified witness on its
first recorded offset and kernel sample. Each accepted kernel has dimension21
and every coordinate marginal rank2. All witnesses are checked again by
direct arithmetic on the ORIGINAL B,s, not just the solver's verifier.

This input is the already-easy, handpicked degree-eight control. No generic
prime divisor or higher tower input was sampled, and no large matrix was
built. A comes from the existing explicit geometry. The all-input theorem
and matrix-only adapter are proofs to review, not empirical conclusions
from this replay. No uniform native output law is asserted.

## Repository Validation

From the main checkout, `python qsearch.py validate` returned valid:true,
issues:[], with unchanged8 candidates,796 experiments,807 results and973
negative results. No registry claim was promoted. No CLI/UI/JavaScript
changes were made, so no Node check is claimed. No external contact,
dependency installation, migration, commit or push occurred.

Review status and final source fingerprints are recorded separately in
REVIEW_RESPONSE.md. The independent reviewer did mathematics, not an
independent execution of this test suite or a human specialist review.
