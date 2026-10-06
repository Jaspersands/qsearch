# Native Repair Catalog And Collision-Mass Target

NEXT THEORY TASK / LOCAL DERIVATION REVIEW PENDING. Not yet implemented.
Read `TERNARY_PAIR_CELL_COVERAGE.md`. Do not merely increase generic repair
depth: at larger roots that can conceal an exponential list.

## Mechanism

A fixed public chart maps each original word w to its exact required forced
rounding pattern P(w)=-round(rho(w)). Applying a KNOWN pattern to nearest plane
is polynomial public arithmetic and returns at most one lattice point for a
given target. Verify its original shell and congruence as usual. Two distinct
words in the same target fiber cannot share the same required pattern for one
chart, by deterministic decoding and full-row-rank coefficient uniqueness.

Instead of all binomial rounding repairs, train a catalog of frequent patterns
from ordinary independent known words using ONLY stripped labels/public bases.
Use held-out WORDS to evaluate recall; then separate fresh independent UNIFORM
TARGETS to evaluate pair coverage. Training never supplies an unknown target's
actual word or quantum phase. Charge training, compilation and all catalog
decodes anew for fresh label arrays, unless a justified label-reuse model exists.

## Rigorous Fixed-Catalog Bound

For fixed public labels/chart, let p_e be the true uniform-word probability of
pattern e and collision mass C=sum_e p_e^2. Any target-INDEPENDENT K-pattern
catalog S captures word mass gamma satisfying

```text
gamma=sum_{e in S}p_e <= sqrt(K*C).
```

This is Cauchy, not an independence or entropy fit. It remains true for catalogs
chosen after public training: condition on that catalog and use the same true
distribution. Multiple charts obey a union bound

```text
gamma_union <= min(1,sum_chart sqrt(K_chart*C_chart));
beta_label <= gamma_union/6 at the underfull source scale.
```

NO independence across charts is needed. A population theorem making C
exponentially small would rule out fixed polynomial catalogs in THIS decoder
family. Empirical zero collisions do not establish such a theorem. Target-
adaptive pattern synthesis is outside this bound and remains a possible escape.

## Implementation And Proof Work

1. Reuse saved exact GS directions and word-probe fixtures; do not rerun LLL just
   to produce the same matrices. Implement an exact forced-pattern decoder.
2. On affordable widths, enumerate true pattern distributions and collision
   mass, test the Cauchy bound and full pair bucket coverage for each catalog.
3. Train label-local catalogs with multiple public size budgets and evaluate
   independent held-out words. Keep all train/test seeds and access restrictions.
4. Run actual uniform-target pair tests with two distinct verified outputs,
   all failures and full training/decoding costs. Planted recall is not acceptance.
5. For statistical collision upper bounds use independent disjoint word pairs
   or a justified U-statistic theorem. N*(N-1)/2 comparisons are NOT independent;
   charts built from the same word sample are also dependent. Correct multiple
   comparisons and keep statistical evidence separate from population proof.
6. Investigate whether errors admit a low-entropy catalog, small unsafe coordinate
   set, symbolic dependency graph or algebraic pattern generator. Any such claim
   must survive held-out words, fresh labels and uniform targets.
7. If fixed catalogs fail, test a separately scoped TARGET-ADAPTIVE repair rule
   guided by the exact original shell deficit and one-hot constraints. Do not
   infer that a catalog obstruction rules out adaptive CVP or arbitrary receivers.

Likelihood of failure is substantial: all r32 charts currently show256 distinct
patterns in256 sampled words, and typical repair support grows with root size.
But those observations are too weak to prove collision mass exponentially small.
Strong evidence against this failure would be verified polynomial catalogs or
target-adaptive rules with inverse-polynomial pair coverage and a proof of
source-law scaling, not a finite repair-depth success plot.

No new accepted candidate should be created until this mechanism meets the
existing pair-finder, source-runtime, access, reduction and hardware obligations.
