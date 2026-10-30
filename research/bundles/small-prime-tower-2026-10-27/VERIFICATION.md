# Verification And Handoff

2026-10-27. No quantum advantage, general hardness, novelty or implemented
higher-degree source is certified. The actual degree-eight input is
classically solved. Files here are local and outside Git; repository notes
point here but do not back up this bundle.

## Tests And Syntax

Final combined suite: **461 passed in 15.19s**, warnings treated as errors,
no skips. This includes the final 31 tests in test_small_prime.py, including
relative character signs, the proper-subcover extra fiber, exact strict
success bounds, classical dead ends and original-input verification.

Run from /Users/jaspersands/Developer/qsearch-research-work:

```sh
env PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPYCACHEPREFIX=/tmp/qsearch-review-pycache /opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider -W error \
  small-prime-tower-2026-10-27/test_small_prime.py \
  systematic-full-support-2026-10-27/test_systematic.py \
  constructive-tower-2026-10-27/test_source_controls.py \
  one-point-plane-adapter-2026-10-26/test_plane_control.py \
  compressed-graded-algebra-2026-10-26/test_compressed_control.py \
  auxiliary-four-list-2026-10-26/test_four_list.py \
  prime-sampler-halving-2026-10-26/test_sampler_contract.py \
  matrix-geometry-lift-2026-10-26/test_point_lift.py \
  ag-divisor-class-control-2026-10-26/test_divisor_control.py \
  usd-review-resolution-2026-10-26/test_resource_bounds.py \
  generic-divisor-class-2026-10-26/test_class_bound.py \
  prime-ag-tower-source-2026-10-26/test_tower_source.py \
  ag-affine-sampling-2026-10-26/test_affine_sampling.py \
  unambiguous-reduction-2026-10-26/test_usd_reduction.py \
  schur-growth-classical-gate-2026-10-26/test_schur_gate.py \
  inverse-trace-local-list-2026-10-26/test_local_list.py \
  inverse-trace-modular-norm-2026-10-25/test_modular_norm.py \
  inverse-trace-norm-transfer-2026-10-23/test_norm_transfer.py \
  inverse-trace-residual-2026-10-23/test_residual_sat.py
```

Python 3.13.5, python-flint 0.9.0. Final syntax check from this directory:

```sh
env PYTHONPYCACHEPREFIX=/tmp/qsearch-review-pycache /opt/anaconda3/bin/python -m py_compile seed_search.py small_prime.py avoidance.py test_small_prime.py replay.py
```

No executable changes followed that combined test run. RESULT.md was updated
after review to record its completed status. Syntax and replay were rerun
after that status update.

## Live Replay

Both commands completed successfully from this directory:

```sh
/opt/anaconda3/bin/python -B replay.py --write
/opt/anaconda3/bin/python -B replay.py --check
```

They reproduce the bounded seed search, actual complete matrix, exact bounds
and eight original-input witnesses: four deterministic, four systematic.
Systematic attempts were 1,1,2,1. The receipt hashes six local files and four
sibling dependencies; preserve their layout or explicitly adapt and retest
imports. It is not a standalone package.

Final receipt SHA256:
`37269bcd3f5894b3e6875409d7d218d0819e71624339b32b53a12f69f04146d8`.

## Independent Checks

../small-prime-review-2026-10-27/REVIEW.md accepts the scoped source, complete
RR basis, native ranks and fixed-p parameter transfer without required fixes.
It uses independent extension-field radical evaluation, vanishing jets and
plain-Python modular elimination. The final evidence reports PASS, 319488
radical-product checks, 19968 parent-evaluator comparisons, 12000 exhaustive
F5 avoidance cases, and 46 native witnesses for each of independent and
parent matrices. Higher degrees are checked only as exact parameter bounds.

Preserved evidence SHA256:
`872b922821a0555d70d65aea18a881328bdd6ca6166386c39f41d5499bc87562`.
Reviewer audit.py SHA256:
`795dd93b1d40699082205561ce34fc91d8c3d79ee2537024bbd14ffea48ac78b`.

The evidence source hashes matched when inspected after replay. The only
subsequent change among those sources is RESULT.md's review-status paragraph;
all executable reviewed sources remain unchanged. This is independent agent
review, not external peer review or a proof-assistant certification.

The separate ../ajt-extraction-review-2026-10-27/review.md is a bounded
primary-literature audit, not proof that no general extractor exists. Its
checks.py was also replayed successfully. Do not use the withdrawn
arXiv:2205.03389 as support for stronger hyperplane-cover claims.

## Repository Scope

Main /Users/jaspersands/Desktop/quantum algorithm search/qsearch.py validate
was rerun successfully: valid true, issues empty. It reports 8 candidates,
796 experiments, 807 results and 973 negative results. No new candidate was
admitted. Full main-repository tests were NOT run. No root index.js exists
in that checkout and no UI files changed. Git diff --check passed.

Only research/AGENT_HANDOFF.md and the new
research/CONSTRUCTIVE_AG_RESEARCH_CHECKPOINT.md were edited in the Git
checkout. No commit, push, migration repair or source move was performed.

## Next Work

GPT: seek a constructive classical solver for this special AG avoidance
family, or a useful-problem reduction surviving those attacks. Compare
expected research value against a pivot; no more seed optimization by default.

Gemini: use ../constructive-tower-2026-10-27/HANDOFF.md to construct an actual
next cover and complete RR matrix over F_1019. Then target genuine e256
inputs, followed by e512/1024 with fresh good divisor classes, matched
classical attacks and measured source costs. Those levels have NOT been
generated. e256 lies outside one greedy guarantee, not outside all classical
algorithms. Pullback of the current divisor neither has the prescribed new
degree nor guarantees persistence of the full cube.

Keep the conditional raw-success bound squared: (1-E_dec)^2/(1+alpha).
Separate search from uniform sampling. Back up selected artifacts and their
actual transitive dependencies at the next coherent Git milestone, not by
blindly copying every isolated experiment.
