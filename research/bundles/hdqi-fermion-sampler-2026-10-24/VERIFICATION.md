# Verification Boundary

Date: 2026-10-24. Python: `/opt/anaconda3/bin/python`.

## Completed Checks

```sh
python -m pytest -q -W error test_fermion_sampler.py ../hdqi-parent-gap-2026-10-23/test_parent_gap.py ../hdqi-sign-sampler-2026-10-24/test_sign_sampler.py ../hdqi-paired-positivity-2026-10-24/test_paired_positivity.py
```

231 passed in 3.46s: 94 new and 137 predecessor tests. No skips; warnings
treated as errors. They cover exact rational DPP conditionals and rejection
normalization, Pfaffian determinants, incidence/chord decoding, signed native
state amplitudes, disconnected cycles, isolated vertices, changed generator
ordering, zero-temperature and zero-coupling cases, invalid inputs, rank caps
and explicit rejection failure.

Four Python files passed `py_compile`, including a rerun after the final
receipt-checker correction.

Live rational-backend runs used 32-, 64- and 128-vertex roots, corresponding
to 31, 63 and 127 native generators, with three samples each and acceptance
on the first trial for every forest sample. Their native Hilbert dimensions
were NOT allocated. These are 16-bit rational surrogates, not certified
native samples. The small controls use 40-bit rationalization; their signed
state L2 discrepancies from the dense native reference are below 9e-13.

The two-cycle incoherent shortcut has TV distance approximately 0.7321253820.
The four-cycle control has distance approximately 0.4876856476. Exact
rejection acceptance is 1/2^r, including zero-temperature cases.

All twelve source hashes in the preceding bielliptic receipt remain intact.
The seven hashes in this bundle cover six local science/code/handoff files
and the frozen parent-gap constructor. The verification file and parent
checkpoint are excluded to avoid a circular receipt hash.

## Receipt Check Passed

An initial `--check` compared Python tuples with JSON lists and failed even
though all seven hashes matched. It now compares JSON-normalized objects.
The final `python replay.py --write` completed. A separate fresh
`python replay.py --check` returned:

    PASS: fresh replay matches receipt and all source hashes

Final receipt SHA256:

    2b944a0773b0e6cadb57c3b12ebe98de84c06c22f6f60509c37f87cf2086743a

All owned test, syntax and replay processes have completed. No work is left
running by this pass.

## Not Established

No interval-certified eigensolver/matrix-function front end, independent
mathematical review, formal proof, quantum circuit compilation or execution,
generic parent-gap proof, extensive-cycle-rank polynomial sampler, novelty
or quantum speedup. Tests check the stated implementation and finite algebra;
the all-size algorithm claims depend on the local derivation in the note.

No Desktop/staging checkout, qsearch CLI, registry, UI, Git, migration or
other agents were changed. The intended Developer checkout was still absent.
Full-repository tests, `qsearch.py validate` and UI checks were not run on the
unverified migrating checkout; they would not validate this external proof
bundle in any case.
