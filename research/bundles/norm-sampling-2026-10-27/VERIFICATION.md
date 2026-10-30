# Verification And Scope

27 October 2026. Scientific result: a scoped exact CLASSICAL sampling
theorem, not a quantum discovery or a numerical advantage claim.

## Executed Parent Checks

From this bundle, with the existing /opt/anaconda3/bin/python environment:

```text
env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-norm-sampling-pycache /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error test_norm_sampling.py test_rank_weighting.py ../two-component-norm-2026-10-27/test_norm_completion.py ../two-component-norm-2026-10-27/test_point_ratio.py ../small-prime-tower-2026-10-27/test_small_prime.py ../schur-growth-classical-gate-2026-10-26/test_schur_gate.py ../affine-resampling-audit-2026-10-27/test_repair.py ../matrix-geometry-lift-2026-10-26/test_point_lift.py ../one-point-plane-adapter-2026-10-26/test_plane_control.py
```

**214 selected tests passed in18.30s:45new and169existing controls.**
An initial focused run was intentionally interrupted after24passing tests
while constructing enormous already-vacuous rational bounds. The bound
function now exits early once eta>=1; it returns no efficiency certificate
and does not calculate unused deficiency bounds. All final tests pass.

Five-file py_compile passed for norm_sampling.py, exact_control.py,
replay.py and both test files. replay.py --write and --check reproduce
receipt.json, including source hashes and transitive native dependency
hash checks. Main qsearch.py validate returned valid:true, issues:[], with
8candidates,796experiments,807results,973negative results and1330
dequantization checks. No candidate or central claim was promoted.

## Exact Controls And Native Replay

Each of two exact F5 controls enumerates625 offset cosets. In the case with
a randomized outside coordinate there are205 native witnesses; every one
has1296 nonzero norm lifts. The uncorrected good-coset law has native
TV74/3895. Reusing a coset changes that law by3/3116; freezing the outside
coordinate changes it by1167/1558. Discarding only rank-deficient cosets
still has native TV1727/1132420.

The rank-weighted proposal gives EXACT zero native TV in both controls.
Its success probabilities are13284/15725 and67392/78625. The public
normalization identity recovers the enumerated counts205 and52 exactly.
Separate625-coset controls have unequal incident restriction ranks1and2;
they verify thinning factors for R0andR1 and explicitly refute omitting
thinning. Code controls retain a reachable rank-zero system and reject
an unreachable target, rather than silently discarding deficient systems.

The existing original43x176 F1019 input produced nine verified native
outputs: three each from the approximate norm control, exact systematic
rejection and rank-weighted norm sampler. The latter uses the already
proved public-geometry rank premise R32: rowspace distance>=93 exceeds
auxiliary pole degree64, and h has full support. The replay checks the
actual matrices, h, dependency hashes and original relation; it does not
re-prove curve geometry from sampled witnesses. This input was already
classically easy, and no larger input was generated.

## Independent Review

The separate reviewer completed the scoped proof, all-input range,
exact implementation and counting-corollary audit in
../affine-pair-avoidance-review-2026-10-27/SAMPLING_REVIEW.md. Parent read
both its original proof and final implementation sections and closed it.
The reviewer independently ran14 exact-class tests successfully and
19earlier focused approximate-control tests. Those are not added to the
parent's214 count. Its code hash matches the final parent code:

```text
b37fefd08971a9c66803ba5447332d29d04bb2caf49059baa9434a3aa299c531 norm_sampling.py
455dfb432baa4143bafd37da5519caaf76789a1eee599d11114be5c72b7829be receipt.json
557b58bdde2a0c9b524c67b33c717d8418324d4815dc3421b43f7fcb3b906b85 SAMPLING_REVIEW.md
e557e2db299fbb31fde2d1a290d74c3131eb7c21d043d59e65616a7b4537b534 REVIEW.md
```

The separate literature REVIEW.md found no applicable fixed-q extractor
from generic LLL/rank independence. It proves a scoped obstruction to
sparse value-preserving native resampling, not hardness of the search
problem. Its small independent checks were not rerun by the parent.

## Boundaries

Exactness is conditional on success and the algebraic promises, with ideal
independent randomness. Fixed-seed replays do not certify PRNG output laws.
The expected-polynomial guarantee covers q>=1019,e>=8,q^2>=44e. At fixed
q1019 the sufficient cutoff remains23599, dyadic16384. It does not cover
unbounded e, nor implement the large native matrix-only adapter. R0 is an
exact fallback without the universal rank premise, but may be exponential.

The full main-repository test suite was not run; no UI, JavaScript, CLI or
central registry was changed, so no Node check or new CLI workflow is
claimed. No migration, dependency installation, external contact, commit
or push. The isolated bundle/review are outside Git; the main handoff
pointer is NOT a backup. Existing unrelated untracked files are preserved.
