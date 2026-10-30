# Completed Local Pass

2026-10-23. All work is isolated from the actively migrating repository.
Source and staging were not edited. No commit, push, CLI, or UI change.

## Result

The conditional-product canonical-TFD Pauli estimator extends to genuinely
interacting 1D conditional chains. The written composition uses the existing
correlated worldline sampler and published constructive relative-Schatten-2
MPO approximation, with a uniform additional bias at most 4 eta + 2 eta^2.
Independent mathematical review remains required. This is a scoped matched
classical attack, not a quantum algorithm or a general simulation theorem.

## Files

- INTERACTING_COHERENT_READOUT.md: inputs, proof, dependencies, error ledger,
  attempts to falsify the argument, limitations, and next scientific question.
- paired_mpo.py: logarithmically scaled paired tensor contraction and rational
  error accounting. No thermal constructor or certified arithmetic backend.
- controls.py: independent small dense references and an easy exact bond-two
  Ising MPO. These controls are not research candidates.
- test_paired_mpo.py: 24 tests including all central Pauli pairs, interactions,
  bad sector normalization, Y transpose, weight imbalance and a 192-site chain.
- replay.py and readout_receipt.json: actual diagnostics with five source
  hashes and explicit false end-to-end, speedup and novelty admission flags.

## Verification Actually Run

- New tests: 24 passed, RuntimeWarning fatal, 0.71 seconds.
- All eight isolated bundles: 282 passed, RuntimeWarning fatal, 24.70 seconds.
- All four Python files passed py_compile; live replay completed.
- Wrong normalization changes a checked answer by 0.08471746283186932;
  omitting interactions changes another by 0.30454158229986306.
- No full-repository tests, qsearch.py validate, UI checks, or quantum run.

Commands from this directory:

```
env PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -W error::RuntimeWarning
env PYTHONPYCACHEPREFIX=/tmp/qsearch-rees-pycache /opt/anaconda3/bin/python replay.py
```

## After Verified Migration

Reconcile with concurrent changes before moving these files. Keep the proof
under research/ and controls explicitly labeled as diagnostics. Replace the
old note's interacting-Pauli open question with this scoped result, without
removing its valid counterexample to the PRODUCT contraction.

Do not label the current NumPy implementation certified. A production
integration would need a relative-Frobenius thermal constructor, outward
contractions, and the existing worldline sampler's full error/ABSTAIN ledger.
That engineering is lower priority than identifying a concrete useful task
which escapes the classical readout attack. No benchmark campaign is needed.

The next theory check is whether Bell-label measurements are also classical
pushforwards of efficiently sampled source Bell labels. This is a distinct
joint-distribution question, not a claim that Pauli expectations imply full
measurement simulation.

Same-day follow-up completed in `../bell-readout-2026-10-23/`: Bell sampling
is a decoder-free pushforward in the certified approximation regime. A
separate prior-art CT-state composition also estimates physical Pauli
expectations with a supplied classical decoder and source-amplitude access.
Prefer that broader argument when these inputs are already available.
The present attack retains its distinct decoder-free scope. Do not implement
two redundant thermal pipelines before a genuinely escaping task is stated.
