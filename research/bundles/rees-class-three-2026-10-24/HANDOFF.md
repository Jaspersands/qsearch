# Integration And Reproduction

This bundle is outside the original checkout. On 2026-10-24 the migration
worker PID 4829 was no longer running; its status file reported qsearch
`needs_inspection` because cloud files remained unavailable. The intended
Developer checkout still did not exist. Source, staging, Git and aliases
were not changed. Do not treat the previous `copying` status as current.

Run from this directory using Python 3.11 or later with pytest available:

```sh
env PYTHONPYCACHEPREFIX=/tmp/qsearch-class-three-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_class_three.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-class-three-pycache /opt/anaconda3/bin/python -m py_compile class_three.py test_class_three.py
/opt/anaconda3/bin/python -B class_three.py --output receipt.json
```

There are no third-party runtime dependencies. The receipt contains source,
test, mathematical-note and handoff SHA-256 hashes. `VERIFICATION.md` records
actual checks, not intended checks. Regenerate receipts after source edits.

Do not register this as a new accepted algorithm, generic SDE solver, or
independent review. It is an exact finite validation artifact for the
existing Rees manuscript. Do not add a new candidate or a toy-oracle
benchmark. No UI work is needed. The original reviewer files are unchanged.

When a complete, verified local checkout exists, integrate as a focused
mathematical validation bundle if still useful, preserving provenance and
the limited-scope flags. Running central CLI/registry or the entire old
repository test suite against an incomplete cloud checkout is not part of
this pass. No commit/push was attempted.
