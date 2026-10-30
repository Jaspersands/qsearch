# Executed Verification And Scope

Completed 2026-10-24 in `/Users/jaspersands/Developer/qsearch-research-work`.
Previous goal turn was progress: it closed two filtered-thermal comparison
routes. This pass inspected that checkpoint, the current Rees and HDQI
notes, selected main-source polynomial-stabilizer audits read-only, and
the relevant primary literature before choosing a different output-level
classical falsifier. No main-source edit or migration operation occurred.

## Exact Changes

Seven new files in this bundle:

- INTERFERENCE_DISTANCE.md: local all-size distance/TV argument, rational
  tail certificate, high-rank opposite family and adversarial scope.
- interference_distance.py: exact bounded relative-distance enumeration,
  rational factorial-moment tails, certified uniform sampler, capped
  physical reference and a fixed public 64-Pauli fixture.
- test_interference_distance.py: 28 tests, including nonlinear valid and
  invalid decoders, genuine thermal bias, exact truncated uniformity,
  scalar redundancies, complex phases, strict distance boundary,
  square-root error necessity, joint-law exclusion and budget refusal.
- make_receipt.py: deterministic live evidence with source manifest.
- receipt.json: full physical input, exact certificate, output examples
  and physical controls.
- HANDOFF.md: bounded integration instructions for Gemini.
- VERIFICATION.md: this executed scope.

Also updated the leading entry of RESEARCH_CHECKPOINT_2026-10-23.md.
No older bundle, main CLI, registry, UI, Git metadata or dependency changed.

## Results

All checks used `/opt/anaconda3/bin/python`, single-threaded BLAS,
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1, `-p no:cacheprovider -W error`, and
PYTHONPYCACHEPREFIX=/tmp/qsearch-distance-pycache.

- Focused suite after the nonzero-bias improvement: 28 passed in0.59s.
- Final broad external suite: **760 passed in17.20s**, no warnings/skips.
  This contains the prior732 external controls and the new28 controls.
- All three new Python files passed py_compile after the final code edit.
- The receipt was regenerated after the improved fixture and final test
  edit, then independently replayed byte-identically.
- All11 manifest entries matched before and after replay.
- The fixed input has n32,m64, rank(B)=64, rank(X)=32 and fiber bound2^32.
  All679,120 words of weights1 through4 were checked; none is diagonal
  nonidentity. Thus its relative interference distance is at least5.
- Its exact rational TV-squared upper bound is651/1073741824, implying
  TV<=0.000778646901<0.001. Decisions compare rationals to epsilon^2;
  this decimal is for readability, not interval certification.
- The old default full-fiber sampler explicitly refuses this same input;
  the new certified sampler produces n-bit outputs without pilot, decoder
  or signed-word calls. No large quantum state or measurement fiber is built.
- Four dense physical controls use a genuinely nonlinear valid decoder.
  At beta1, the untruncated output TV is0.06425194463 and the pilot tail
  is0.07222020685. The truncated output is uniform to1.111e-16 maximum
  error. Controls also cover beta0,1/16,1/4 and arbitrary bad decoders.

The first dense fixture accidentally had exactly uniform thermal outputs
at all tested temperatures. Before freezing evidence it was replaced with
a real-phase fixture exhibiting nonzero bias, and an explicit test was
added. Final tests, receipts and hashes all refer to the strengthened case.

Final receipt SHA-256:

    5d9dcf8710952168b418f1cf760eebed019b999dbc7b8ad657618cccc349ee21

The broad suite used the same preceding external test paths documented in
the filtered-KMS bundle, plus test_interference_distance.py. The focused
command is:

    env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-distance-pycache PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error hdqi-interference-distance-2026-10-24/test_interference_distance.py

## Unverified Or Not Claimed

The all-size deduction has no independent review or novelty determination.
Its thermal inclusion bound is a cited external dependency. No general
distance solver, high-temperature parent gap, coherent preparation, full
joint-output sampler, arbitrary-basis sampler or quantum speedup follows.
A failure of this test is not evidence of classical hardness. The fixed
Clifford-equivalent fixture is not a uniform random Clifford experiment.

The intended main Developer checkout was still absent. No whole-repository
tests, qsearch.py validate, node/UI checks, integration, commit or push were
performed against the unverified checkout. No new reviewer was spawned;
the completed Rees reviewer was not reused. All owned processes finished.
