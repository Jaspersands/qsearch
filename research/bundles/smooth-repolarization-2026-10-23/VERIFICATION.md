# Verification Checkpoint

2026-10-23. All tests below were run in separate processes from their own
isolated bundle directories under `/Users/jaspersands/Developer/qsearch-research-work`.

| Bundle suffix omitted: -2026-10-23 | Passed |
| --- | ---: |
| normalizer | 68 |
| inverse-trace-residual | 30 |
| spectral-source | 42 |
| central-rank | 32 |
| terminal-fpt | 55 |
| rees-channel | 12 |
| prior-art | 19 |
| interacting-readout | 24 |
| bell-readout | 16 |
| ppav-source | 37 |
| smooth-repolarization | 56 |
| Total | 391 |

Command: `/opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider`.
Environment: `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` and
`PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache`.

New Python sources also pass `python -m py_compile`. The new replay and
the preceding PPAV replay completed; their receipts include source hashes.
The eight-square identity was additionally expanded symbolically in eight
independent coefficient variables, not only evaluated on finite examples.

This is NOT repository-wide validation. No `qsearch.py validate`, UI check,
geometric quotient, target-kernel recovery, quantum receiver or proof-assistant
verification was run in the moving repository. Its source and staging trees
were not edited. The migration coordinator was still live at this checkpoint.
No commit or push was made from these non-Git isolated research directories.
