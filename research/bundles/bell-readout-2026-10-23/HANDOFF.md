# Completed Bell And CT Readout Pass

2026-10-23. Kept outside the repository because its source-to-staging ditto
copy was still active. Source, staging, registry and Git were untouched.

## Scientific Outcome

Full Bell-label sampling is a classical forward-map pushforward whenever
the source Bell law is classically sampleable. Connecting this law to the
ideal thermal target still requires the actual relative-distance and shared
polynomial-approximation promises. No classical decoder is executed.

Further prior-art review gives a broader Pauli-expectation baseline via
computationally tractable states: with an efficient classical decoder and
source-amplitude evaluation, the entire label-stage state INCLUDING decoder
garbage is CT. Physical Pauli observables pull back to efficient monomials.
The written argument handles the non-Clifford diagonal Bell-label gauge.
This is an application of known simulation methods, not a novelty claim.

The earlier interacting-chain paired-MPO route is now a secondary,
decoder-free baseline. Do not spend engineering effort building redundant
thermal backends without a useful output task that survives both attacks.
Neither argument is a complete simulator of arbitrary output distributions.

## Exactly What Changed

- BELL_READOUT_DECISION.md: population identity, ideal-target error transfer,
  paid 1D source-MPO/MPS construction, CT extension, scope and counterexamples.
- bell_pushforward.py: single-label binary map, actual finite quantum circuit
  and partial trace, bounded paired CT estimator, exact sparse Pauli controls.
- test_bell_pushforward.py: 16 tests; interactions, noncommutation, collisions,
  wrong decoders, arbitrary phases, diagonal gauges, and zero partner support.
- replay_bell.py and bell_receipt.json: actual exact calibration and numerical
  CT readout, four source hashes, no algorithm/speedup admission.
- HANDOFF.md: this record.
- The neighboring interacting-readout proof/handoff was updated to reflect
  the stronger CT route. Its receipt was regenerated after the late changes.

## Verification Actually Run

- All NINE isolated bundles: 298 passed in 25.29 seconds, RuntimeWarning fatal.
- The two new bundles contain 24 + 16 = 40 tests.
- All seven Python files in the two new bundles passed py_compile.
- Both live replay workflows completed after the final source changes.
- All nine recorded source hashes were independently verified.
- Native noncommuting chain control: 24 terms, degree two, 234 coefficient
  labels, exact Bell-law TV zero under the distance-five promise.
- Degree-three countercontrol: 1,099 source versus 1,047 target labels, with
  TV 1964880960/92843598241. This invalid extension is explicitly rejected.
- Paired CT readout agrees with the independently traced -4/7 expectation.
- No full-repository test, qsearch.py validate, UI check, quantum execution,
  scalable thermal constructor run, Git commit or push was performed.

Commands from this directory:

```
env PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -W error::RuntimeWarning
env PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache /opt/anaconda3/bin/python replay_bell.py
```

## Gemini / Integration Work After Migration

First verify completion of the copy and identify the authoritative checkout.
A vanished worker PID is insufficient: the worker has restarted repeatedly.
Reconcile concurrent changes before integrating any isolated bundle.

1. Keep the two proof notes under research/ and clearly label finite controls.
2. Update the existing coherent-Gibbs and priority notes with a short scoped
   summary. Do not append another large benchmark inventory to the website.
3. Preserve decoder-free Bell sampling and decoder-required CT Pauli readout
   as DIFFERENT access contracts. Never silently provide a decoder callback.
4. Update imports/replay paths and regenerate receipts if files move. Run
   targeted integrated tests and the actual qsearch registry validation.
5. Do not add a new candidate or mark a theorem formally verified from these
   tests. Do not claim independent proof review or a production sampler.

Only if a concrete downstream task needs execution: reuse a reviewed thermal
MPO constructor with a relative-Frobenius certificate, canonical MPS sampling,
source amplitude evaluation, and charged finite-precision errors. No dense
Pauli expansion is allowed as the purported scalable backend. No raw callback
promises should become proof certificates. This engineering is deferred, not
represented as implemented by the finite controls.

## Next Main-Model Question

The Gibbs route now needs a useful reduction/output outside these baselines,
not another observable or temperature sweep. A many-bit non-Bell outcome
with nontrivial postprocessing is NOT ruled out by efficient single-Pauli
estimation. It also is not established hard merely because this method does
not simulate it. Specify a useful task and charge its entire quantum source
and measurement before launching another implementation campaign.

Absent such a task, return to the proposed Rees algorithm's full-proof and
natural-input/application audit. The main unresolved issue there is still
computational relevance and whole-result correctness, not missing plotting
or more small group examples. Goal remains active; these are completed,
reviewable passes rather than an assertion that the overall goal is achieved.
