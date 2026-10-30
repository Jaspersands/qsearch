# Exact Controls And Analytical Scaling

Question: does the published all-element fixed-point estimate provide a
rank-dependent classical lower bound under the same full-group query model?

The universal answer is a mathematical application, not a fitted experiment.
Finite controls target transcription, component, center and field mistakes.

- Enumerate every maximal singular space at (n,p)=(3,3),(3,5),(4,3):
  80+312+2240=2632 spaces, split into both equal components.
- Evaluate seven representative noncentral isometries on every space:
  upper/lower/Levi roots, semisimple, one/two hyperbolic swaps and a mixed
  element. This is 18,424 matrix/subspace checks, not all group elements.
- Match root counts against the independent line-incidence expression.
- Check universal +/-I repeats and zero fixed points for a component swap.
- Reject rank two, even fields and non-prime-power field orders.
- Reject a claimed lower bound on a coordinate-label source, which reveals
  L in one identity query.
- Use exact fractions and integer square roots for necessary query counts.
  These are necessary thresholds, NOT achieved classical costs.

The receipt contains seven scaling deductions, including n=64,q=3. There
the conservative proposed quantum schedule is 324,289 original queries for
error <=2^-40, while success >=2/3 in the random-opaque classical model
requires at least 466,917,199,436,564 queries by this bound. These numbers
are mathematical ledgers, not executions or proof of a useful application.

Run:

```sh
env PYTHONPYCACHEPREFIX=/tmp/qsearch-rank-bound-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider
env PYTHONPYCACHEPREFIX=/tmp/qsearch-rank-bound-pycache /opt/anaconda3/bin/python replay.py
```

Falsifiers: incorrect applicability of GK's bound to the stated action;
noncentral universal kernel at admitted ranks; a failure of the adaptive
coupling; or extra source information defeating opaque-label independence.
Passing finite controls alone cannot rule out the first two universally.
