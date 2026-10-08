# Full-Record Native CVP Optimizer Attempt

LOCAL DERIVATIONS / REVIEW PENDING. A concrete classical proposal generator
on quantum-produced native records. NO9/8 approximation guarantee, original
source dequantization, hardness result or accepted quantum speedup.

## Change From The Subset Baseline

The previous paired-metric attack used small lattice subsets and ranked their
proposals on a larger training batch. This attempt places ALL original pairs
in the ORDINARY Euclidean lattice from `TERNARY_NATIVE_CVP_REDUCTION.md`.
It does not relabel the paired A2 metric as that reduction's objective.

Reuse the exact full-root systematic code lattice A Z^n+q Z^(2M), with public
unit-row inversion and index q^(2M-n). The underlying constructor now exposes
the code basis separately from its paired embedding, so the two metrics use
the same verified native congruences without duplicate geometry code.
Full-cohort rank failure or cap exhaustion is retained; partial data is not
silently promoted to full optimization.

## Actual Optimizer

1. Exact-gram LLL on the complete Euclidean basis. Preserve its integer
   unimodular transform, not a floating reduced matrix.
2. One exact Babai path plus32 public multi-rounding-repair vectors. Each
   vector changes one to four public rounding positions by +/-1. Lower
   coordinates are recomputed. This is a fixed finite repair menu, NOT
   exhaustive enumeration or Klein's discrete-Gaussian sampler.
3. Two target-dependent Kannan-style embeddings, at integer scales floor(q/4)
   and floor(q/2), clipped to1. Preserve every reduced row and transform.
4. A row is(l+k*y,k*T). For k=+/-1, y-row/k is a literal code-lattice point.
   More generally, when k is a unit modq, recover the code secret of l and
   form the modular trial -k^-1*s_l. This is a LEGAL proposal but is not a
   literal CVP error vector or an approximation certificate. Nonunit rows
   are rejected with their coefficients recorded.
5. Validate every candidate against the complete shared-secret code, then
   rank the deduplicated shortlist under TWO training objectives: wrapped
   Euclidean squared distance and the actual paired native likelihood score.
   Canonical wraps remove harmless q-axis aliases within a secret coset.
6. Freeze both selections before generating512 fresh records. The verifier
   charges the number of DISTINCT frozen trials jointly; it is not two
   unadjusted one-candidate confidence claims.

Plain lattice reduction reads labels only. Embedding reduction legitimately
reads the target outcomes. Neither may read hidden calibration truth or
held-out data. Public randomness is algorithmic randomness, not fresh source
independence. Classical reuse consumes original measured records only once.

## Exact Sparse Arithmetic, Not An Approximate Profile

The full lattice can have hundreds of dimensions. Compute its Gram entries
by column support incidence and perform exact rational LDL, retaining every
nonzero coefficient. Zero-support sparsity is exploited but no small entry
is truncated. The product of squared GS norms is checked against the exact
code index squared. Exact rational repaired nearest-plane paths consume this
profile; tests compare it with the earlier fraction-free dense GS routine.

Sparse certificates store all nonzero basis/transform entries and fixed
dimensions. Omitted entries mean EXACT zero. They are not partial matrices.
This avoids enormous zero-heavy reports, not the actual matrix dimension.
LLL, profile construction, every repair and embedding are charged; no wall
deadline is hidden inside LLL. The complete algorithm is finite and costed,
but has no scalable recovery proof or certified numerical score ordering.

## Why A Generic BDD Promise Does Not Transfer

The code lattice contains every q*e_i, so lambda1<=q. To decode the true
secret by a lambda1/2 bounded-distance guarantee, even its best wrapped
error must have squared norm<=q^2/4. Actual native errors are broad.

Write A for the true normalized mean of one error-pair squared cost. Its
exact formula from the CVP reduction and concavity of sine give A>=4/81:
sin(pi/q)>=3*sqrt3/(2q), the normalized gap<=8/81, and the uniform mean
is at least4/27. Each pair cost lies in[0,1/2]. Hence the true BDD promise
can hold with probability at most

    exp(-8*M*max(0,4/81-1/(4M))^2).

This is a conservative local source bound, not a general lattice/quantum
lower bound. It prevents importing a narrow Gaussian/unique-SVP theorem onto
this source. General CVP approximation and secret-CODE-COSET recovery do not
require lambda1/2 and remain open. Exact q-axis aliases are nuisance vectors,
not evidence that distinct secret cosets are close.

All eight live cohorts violate the true q/2 radius, including the two
small-root SUCCESS controls. Thus this gate is explicitly not a recovery
upper bound: an algorithm may succeed outside the sufficient BDD regime.

Primary context: [embedding/BDD analysis](https://arxiv.org/abs/1102.2936)
and [randomized lattice decoding](https://arxiv.org/abs/1003.0064). These are
known techniques with their own promises. Our public signed repairs do not
inherit Klein sampling guarantees, and unit-k modular trials do not inherit
the signed-unit embedding guarantee.

## Precommitted Growing-Root Experiments

Eight fresh cohorts: (n,r)=(2,2),(2,8),(4,8),(8,8), each with M=4nr and8nr.
Seeds are fixed as97200+100n+10r+density before fresh data. Every original
pair belongs to the optimization; lattice dimension is2M, up to1024.
This density exceeds the earlier measured-channel information obstruction,
but is BELOW the conservative population9/8-CVP copy guarantee. No finite
success or failure inherits that theorem's confidence certificate.

Record both training selections, all repaired paths, embedding rows and
nonunit rejections, original-source counts, complete runtime, the true
cost/BDD diagnostic and fresh verification. One cohort per regime is not a
population success estimate. Native-law simulation is not unknown-state
supply. No positive seed or favorable transcript is filtered into the report.

Falsifiers: wrong full-root code index, a nonunimodular transform, missing
nonzero sparse entries, rounded GS arithmetic, invalid modular row extraction,
hidden truth influencing a proposal, or uncharged held-out multiplicity.
Failure of this menu does not exclude BKZ, sphere enumeration, quotient-aware
CVP optimization, nonlinear inference or genuinely collective measurements.

## Exact Approximation Falsifiers, Not Just Failed Recovery

The live eight-cohort pass recovers ONLY the two small-root controls under
both objectives. All six growing-root cohorts fail fresh verification. Each
also has a fully public code-lattice comparison point, formed AFTER the
optimizer has finished from a known calibration secret. Its membership and
distance are exact and independently checked. No claim that this comparison
point is globally nearest is needed.

Let C be the minimum wrapped Euclidean cost among ALL generated candidates,
and W the cost of the valid comparison point. If64*C>81*W then

    C > (9/8)^2*W >= (9/8)^2*OPT.

This disproves a norm9/8 approximation guarantee for this optimizer on THAT
actual public instance. Five growing-root cohorts have positive integer
margins. The remaining failed cohort has no such witness and is retained as
inconclusive for approximation quality. This is not population hardness,
failure of every lattice method, or a claim that the original quantum source
is classically simulated. The comparison truth never enters generation,
ranking or held-out selection; it is strictly posthoc certificate material.

`--replay-saved --write` can append/revalidate these comparison witnesses
from the saved actual optimizer outputs without repeating the expensive
LLL computations. The replay is explicitly NOT a new source or optimizer run.
Independent certificates still replay every transform and repaired path.

## Positive Follow-Up: Exact Rounding Influence Compiler

Most reduced rows on the large cohorts are q-axis aliases, but discarding
every such row would be wrong: forcing its rounding coefficient can change
earlier non-alias coefficients through Gram--Schmidt feedforward.

The implemented compiler maps each reduced basis row to its public code
secret and forms a DAG with edge i->j for each nonzero exact GS coefficient
mu_i,j. Mark i influential when its own code secret is nonzero OR an earlier
influential node is reachable. Every other node is DEAD. A repair supported
only on dead nodes changes only coefficients on dead ancestors; all their
basis rows have zero code secret. Therefore it preserves the returned
modular secret for EVERY target, even with arbitrarily many dead repairs.
This is an exact source-class invariance, not a heuristic threshold or a
statement that an influential repair will improve anything.

A two-row countercontrol has a zero-code-secret second row but nonzero GS
coupling to the first, and a repair of that row DOES change the returned
secret. It prevents unsound blanket q-axis removal. Tests also enumerate all
targets of a bounded exact dead-axis control. The saved report contains all
row secrets, live/dead masks and explicit earlier-parent witnesses.

`public_repairs(..., positions=influential_rounding_positions)` now generates
a public menu restricted to potentially useful rounding variables without
spending paths on rigorously dead nodes. The current eight cohorts used the
ORIGINAL broad menu, not this optimized one. Any new optimized selection
must receive NEW held-out samples; the old validation batch is not certified
for candidates chosen after these results. The compiler is implemented and
tested; optimized-menu recovery has not yet been measured.

Next decisions must follow these actual outcomes, not another conditional
statistical theorem. If both methods fail at growing roots, address the
q-axis quotient/global optimization explicitly rather than retune a BDD
radius or count more fixed-field successes. The efficient solver remains
missing until a source-valid algorithm actually meets its performance claim.

```
python theorems/ternary_full_record_cvp.py --write
node research/certificates/ternary_full_record_cvp_crosscheck.js
python -m pytest -q tests/test_ternary_full_record_cvp.py
```

Gemini/Antigravity owns routine CLI, registry, production validation and Git.
This is an implemented heuristic optimizer, not a proven near-exact solver.
