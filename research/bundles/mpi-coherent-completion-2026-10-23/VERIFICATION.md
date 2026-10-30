# Verification

2026-10-23. Local isolated bundle, not integrated into the moving repository.

- **21 tests passed in 1.62s** with `/opt/anaconda3/bin/python`.
- All three Python files passed `py_compile` after the final code edits.
- The live `coherent_receipt.json` was regenerated after those edits.
- Four bundle/dependency hashes and the original decoder source hash match.
- The native source mass and mean lower bounds were recomputed with exact
  integer/rational arithmetic and a rational square-root enclosure.
- The whole-round success lower bound is exactly `17851/349000`, greater
  than `1/20`. The conservative 800-round failure bound is `2^-40`.
- The finite F16 instrument uses floating complex arithmetic: correct norm
  and mean agree within 2e-14. Retaining count records gives mean near zero
  instead of 7/15. Incorrect QFT16 padding loses about 0.227 probability to
  invalid outputs and has TV distance about 0.642, including ABORT.
- The finite total-decoder reference was checked on all 65,536 encoded
  syndrome words. It is an enumerated dictionary ONLY for that diagnostic.
- Separately, the original rational decoder body was AST-loaded unchanged
  and executed on 21 licensed patterns plus one rejected outside-box pattern
  over F_(2^64). It used 88 field exponentiations and no full-field log table.
  An explicitly easy F16 subfield supplied the public fixture matrix.
- The rational score verifier encloses cosines and rejects ambiguous
  threshold cases; its elementary interval proof is in the accompanying note.

Test command:

```sh
env PYTHONPYCACHEPREFIX=/tmp/qsearch-mpi-completion-pycache \
  PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python \
  -m pytest -q -p no:cacheprovider
```

The imported field helper does not execute its Z3 search. Repository imports
were not traversed: the decoder replay selects only its two required function
bodies to avoid touching unrelated offloaded dependencies.

NOT DONE: native quantum optimizer execution, reversible gate synthesis,
physical-resource estimation, a new classical optimization campaign,
independent proof review, Lean checking of this composition, full repository
tests, qsearch validation, UI changes, registry admission, commits or pushes.
The explicit arithmetic/operation ledger is not a synthesized gate count.

Files created: `coherent_contract.py`, `decoder_replay.py`,
`test_coherent_contract.py`, `coherent_receipt.json`,
`COHERENT_COMPLETION.md`, `HANDOFF.md`, and this record. The local research
checkpoint was updated. No moving repository/staging files were edited.
