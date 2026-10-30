# Formal Compression Handoff

This is a successor to exterior-cancellation-2026-10-25, not a replacement
for its frozen receipt or proof-status history. Keep both bundles intact.

## Reproduce

From this directory, with the existing sibling rees-formal-core-2026-10-24
runtime and pinned mathlib cache:

```sh
/opt/anaconda3/bin/python -m pytest -q -W error test_verify.py
/opt/anaconda3/bin/python -m py_compile verify.py test_verify.py
/opt/anaconda3/bin/python verify.py --check
```

`--write` creates a new local receipt after intentional source changes.
`--check` also recompiles; it never accepts a stored receipt alone. A
different complete pinned runtime can be supplied with `--runtime PATH`.
Compilation output stays in this bundle, not the borrowed runtime.

From the preceding arithmetic bundle, rerun its 56-test suite and
`python replay.py --check` to validate the implementation controls.

## Integration Instructions

Only integrate after the repository migration has been independently
verified complete. Do not edit the Desktop or staging copy during copying.
Gemini can wire the prior arithmetic backend as specified in its HANDOFF.
For proof-status tracking, record only algebraic compression, closed-update
preservation, exact row dimension, dependence existence and top-degree
vanishing as Lean-checked. Do not upgrade the full solver, its nonempty
support induction, runtime, or a native quantum candidate to proved.

The authorized independent Rees reviewer did not review this new exterior
argument. Do not label this bundle independently reviewed.

## Next Research Decision

The mathematical work still needed before trusting the COMPLETE SDE bound
is the original-leaf/disjointness recursion and its resource implementation.
But further formalization is not automatically the highest-impact next
pass. Compare that bounded obligation with native-source construction and
full HDQI output sampling. A grade-four/vector-center complete-instrument
test is more informative for integration than additional scalar seeds.
No hidden source access, favorable-label resampling, uncharged discards,
or growing-degree polynomial-time claim may be introduced during wiring.
