# Handoff: Restricted Norm Transfer

This is a negative certificate for a specific proposed classical ansatz,
not a new candidate algorithm, native hardness result, or speedup claim.
All files are outside the moving source and migration staging.

After migration verification, Gemini may move this reviewed bundle into
the existing research-note/test layout. Preserve the exact input points,
all-one target, degree guards and the same-input valid witness. Registry
wording must say "global low-degree Artin-Schreier/square-polynomial
parameterization excluded on this input", never "classical attack ruled
out" or "native family hard". Independent review is still pending; do not
automatically admit this as a general negative result for the candidate.

The implementation imports only the existing isolated residual field and
native verifier. FLINT performs polynomial factorization. Reuse the repo's
native field API upon integration, preserving the independent integer
replay in the tests. No qsearch CLI/UI work is needed merely for this note.

The substantive next task is a genuinely constructive modular-lift solver
or a different native classical attack, NOT increased seed counts, solver
timeouts, a dashboard, or another opaque-label oracle benchmark. The
generic surface source remains an independent high-value option, but its
geometric implementation has not been executed. Its existing handoffs are
the authority; do not describe those arithmetic controls as geometry.

Run locally:

```sh
env PYTHONPYCACHEPREFIX=/tmp/qsearch-norm-transfer-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider test_norm_transfer.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-norm-transfer-pycache /opt/anaconda3/bin/python norm_transfer.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-norm-transfer-pycache /opt/anaconda3/bin/python -m py_compile norm_transfer.py test_norm_transfer.py
```

These are scoped checks, not full repository validation. Do not run or
change the moving checkout to obtain a green full-suite claim.
