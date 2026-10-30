# Verification: Affine-Filter Converse

2026-10-24. External workspace. LOCAL UNREVIEWED synthesis of known measurement
characterization and the repository's existing classical comparator. No new
quantum algorithm, independent review or formal proof-assistant verification.

## Executed

**529 tests passed** in5.41s, warnings as errors, no skips: 29 new controls
plus the preceding500 external controls. Three files pass py_compile.
`make_receipt.py --write` completed. A separate replay to
`/tmp/qsearch-affine-converse-replay-2026-10-24.json` compares byte-identically
with receipt.json. All six bundle source hashes recompute correctly.
The three resident predecessor source hashes were captured on direct reads.
All required owned command sessions have completed.

The focused suite covers exact positive-semidefinite and spectral-budget
validation; covariance and unambiguity; singular spectra; affine offsets with
negative overlaps; direct physical character-basis POVMs; the coherent-prior
counterexample; asymmetric USD and minimum-error exclusions; and caps/bad inputs.

The existing four-message dual is checked on all51 affine frequency spaces,
at five distinct exact c values including both endpoints. The formula is degree
at most4, so these exact identity checks also determine its polynomial equality.
The signed-overlap optimum is checked on all11 spaces. Independent row/column
rank tests cover512 binary3x3 maps times16 residual subspaces:8192 cases.

## Fixed-Sign Counterexample

For the declared one-bit public factor and epsilon=1/64, b=0 gives target
P(0)=79/142 and proposed P(0)=65/128. TV=441/9088 is greater than3/64,
falsifying application of the SIGN-AVERAGE bound to each fixed sign. All16
signs are retained and their exact mean obeys the average bound. This trivially
sampleable one-bit fixture is a scope check, not a hardness example.

The receipt stores five four-message cases, the signed-overlap case and the
full sign census. Every mixture reconstructs its input spectrum exactly.
Fixed-instance sampling, efficient growing-block extraction and arbitrary
postmeasurement coherent processing remain unproved and explicitly unadmitted.

## Reproduce

From this directory:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-affine-converse-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error
env PYTHONPYCACHEPREFIX=/tmp/qsearch-affine-converse-pycache /opt/anaconda3/bin/python -m py_compile affine_converse.py test_affine_converse.py make_receipt.py
env PYTHONPYCACHEPREFIX=/tmp/qsearch-affine-converse-pycache /opt/anaconda3/bin/python make_receipt.py --write
env PYTHONPYCACHEPREFIX=/tmp/qsearch-affine-converse-pycache /opt/anaconda3/bin/python make_receipt.py --output /tmp/qsearch-affine-converse-replay-2026-10-24.json
cmp receipt.json /tmp/qsearch-affine-converse-replay-2026-10-24.json
```

The broad529-test command adds affine-filter-converse-2026-10-24/test_affine_converse.py
to the preceding tree-duality milestone, using this pass's /tmp pycache prefix.
All checks exited zero. No original large classical benchmark or quantum circuit
was run. Small physical matrices only validate the instrument correspondence.

## Changed And Unchanged

Eight new files: affine_converse.py, test_affine_converse.py, AFFINE_CONVERSE.md,
source_context.json, HANDOFF.md, make_receipt.py, receipt.json, VERIFICATION.md.
The external research checkpoint was updated. No frozen predecessor was edited.

The intended Developer checkout is absent and migration remains needs_inspection.
Desktop/staging/main CLI/registry/UI/Git remain untouched. No main-repository
tests, qsearch validate, node syntax checks, commits or pushes were performed.
Gemini integration is pending safe relocation. The authorized Rees review was
already complete; no additional reviewer was used for either new bundle.

## Next Research Decision

The old nonlinear residual-chain lift and coherent BPQM split/erasure notes were
also inspected. They already reject square-blind lifting, paid-cloning depth
scans and eigenvalue-only sharpening; do not repeat these as fresh ideas.
Do not fund local affine-filter LP sweeps as an escape from the existing sampler.
A further binary Gibbs pass needs a concrete coherent/overlap-aware global
construction with a full readout law and resource bound. Without one, compare
independent high-upside directions before adding more local controls.
