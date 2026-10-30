# Exact Native Sampling: Research And Integration Handoff

27 October 2026. Read EXACT_SAMPLER.md first. RESULT.md preserves the
earlier approximate sampler, which the exact correction supersedes.

## Established Scope

Under the preceding complete-AG promises, every original syndrome has an
expected-polynomial EXACT classical uniform sampler for odd q>=1019,
e>=8 and q^2>=44e. This uses exact random draws and the paid theoretical
matrix-only adapter; that adapter is NOT implemented on a large native
input. For e<64 use ordinary systematic rejection; for e>=64 use the
rank-size-biased two-component norm sampler. The degree-eight public-
geometry control was already classically easy.

The key extra step samples offsets with mass proportional to
q^(k-rank(M)). It does so through a base/incident mixture, uniform nonzero
lambda, a paid linear kernel sampler and exact thinning. Large affine
fibers then receive exactly their proper weight. Rank-deficient reachable
systems are essential and must not be rejected. The uniform conditional
law has no approximation floor; caps add only an UNKNOWN outcome.

The same success-probability identity yields randomized multiplicative
approximate counting in this constant-success range. No exact counting
or fixed-prime asymptotic sampler is established. At q1019 the same
sufficient cutoff is e23599, dyadic16384, not a hardness boundary.

## What The New Files Do

- norm_sampling.py: keeps the approximate GlobalNormSampler as a control;
  adds RankWeightedNormSampler and exact systematic rejection. A positive
  restriction-rank bound is a DECLARED universal promise, not inferred
  from a few rank tests. R0 is unconditionally valid but may be exponential.
- exact_control.py: enumerates625 cosets and full norm fibers, including
  outside-coordinate variation; computes exact output laws and bias controls.
- test_norm_sampling.py/test_rank_weighting.py: native relation, counts,
  uniformity, varying incident ranks, deficient solves, thinning, integer
  coins, retry schedules, field-size scopes and honest failure controls.
- replay.py/receipt.json: reuse the previous actual43x176 input after
  verifying its dependency hashes. Nine original witnesses, three methods,
  plus exhaustive finite laws. No larger matrix or quantum execution.
- Independent reports are in sibling
  affine-pair-avoidance-review-2026-10-27/REVIEW.md and SAMPLING_REVIEW.md.

## Gemini: Concrete Low-Theory Integration Work

1. Keep the existing matrix-only adapter task from the previous bundle.
   Add the new sampler only after carrying the SAME original B,s and a
   proved rank-bound provenance record. Do not turn a measured rank into
   the universal premise. Preserve prime-field/backend limitations.
2. Keep whole-trial rejection. Randomize all outside coordinates, including
   P0, on every trial. Keep rank-deficient systems, use their full nullspace,
   reject unreachable targets, and do not retain the approximate G filter.
3. Preserve integer mixture/thinning coins. Floating-point rounding can
   erase the rare branch that is necessary for EXACTNESS. Never wait for
   a rare branch or thinning event with its lambda frozen.
4. The one_trial interface accepts an RNG. Seeded Random is for replay;
   use an appropriate fresh random-bit source for actual sampling and
   never describe repeated fixed-seed outputs as independent samples.
5. Distinguish EXACT conditional output law from cap failure, unverified
   upstream input promises, and theoretical expected runtime. Do not
   promote a quantum candidate or rewrite the older search solver's law.
6. At a later coherent backup milestone, import the actual selected
   modules, proofs and transitive dependencies into Git and replay there.
   This isolated directory and a main handoff pointer are NOT a backup.
   Do not create frequent commits or copy all historical experiments.

## Next Scientific Decision

Do not spend another pass on small fixed-q witness sweeps or a generic
MCMC framework. The independent LLL audit establishes that value-preserving
resampling changes Omega(e) native coordinates, so its usual sparse
dependency certificate cannot extend the fixed-q regime. High joint ranks
do not replace a resampling oracle or bound point-to-set transition charges.
This is not a classical hardness result.

A return to this fixed-q question needs an explicit constructive repair
kernel with a proved efficient charge bound, another end-to-end extractor,
or a useful native reduction. Otherwise compare the independently live
nonabelian/orthogonal and inverse-trace directions rather than extending
nearby norm parameters by inertia. Rees human review is still unsent and
requires explicit authorization; it is not a blocker to other research.
