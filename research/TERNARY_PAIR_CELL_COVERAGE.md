# Exact Native Decoder Coverage

LOCAL DERIVATIONS / REVIEW PENDING. This is a decoder-specific analysis engine,
not a polynomial solver, quantum breakthrough, classical hardness proof or
accepted candidate. It follows `TERNARY_PAIR_LATTICE.md`.

## What Is Now Exact

For a legal original word z, its lattice point is P=3E(z-z0), target
T=E(ones)-3E(z0), and residual

```text
e=T-P=E(ones)-3E(z).
```

The nuisance target cancels. For a fixed public basis with exact GS rows R_i*,
let rho_i=<e,R_i*>/||R_i*||^2. Public center offsets add a known shift. Half-up
rounding is EXACT: floor(rho+1/2); -1/2 belongs to the zero cell,+1/2 does not.

Conditional on the true higher-row coefficients, the forced offset needed at
row i is -round(rho_i). Thus a word appears in a COMPLETE k-repair list with
allowed integer magnitudes<=B IFF at mostk rounded errors are nonzero and all
have magnitude<=B. A forced offset repairs the true prefix; recomputing lower
roundings preserves this induction. Full row independence makes the recovered
lattice coefficients unique, proving the reverse implication too.

This general predicate is tested against actual forced-rounding paths for
k0,1,2 and B1,2, as well as the implemented single-repair pair finder on EVERY
word and target of bounded scalar sources. It is not a floating margin test.

## Integer Compiler And Source Law

Exact Bareiss GS reconstruction yields primitive integer directions v_i.
If R_i*=lambda_i*v_i, then

```text
rho_i=<e,v_i>/<R_i,v_i>.
```

Every direction lies in the original blockwise A2 planes. Each native word
error block has values(2,-1,-1),(-1,2,-1),(-1,-1,2); its projection on a block
is therefore3*v_i[digit]. The compiler uses integer ternary lookup tables,
exact denominators and exact public shifts. No Fraction-heavy search over
unknown words is assumed efficient.

For an independent uniform native word, the unperturbed error has mean0 and
block covariance3I-J. Consequently distinct GS projections are UNCORRELATED,
but generally NOT INDEPENDENT. Write m=1/<R_i,v_i>, N=||v_i||^2, and
N_j=||v_i restricted to block j||^2. Exact centered moments are

```text
E rho^2 = 3*m^2*N = 3/||R_i*||^2;
E rho^3 = 9*m^3*sum_a v_i[a]^3;
E rho^4 = m^4*(27*N^2-(27/2)*sum_j N_j^2).
```

The fourth identity uses sum of fourth powers=(sum of squares)^2/2 for any
three coordinates summing to zero. Independent native BLOCKS combine their
moments; independent GS rows are NOT assumed. Known center shifts are included
exactly in raw moments. Markov gives a marginal rounding-error upper bound;
Cauchy applied to rho^2 gives a strict absolute half-cell tail lower bound.
Neither moment bound by itself proves concentration of the NUMBER of errors.
Tests exhibit a concrete uncorrelated-but-dependent native pair of projections.

## Uniform Target Coverage

The census classifies all3^M original words, unions recoverable words across
fixed public bases/centers, then buckets them by their ORIGINAL modular sum.
A pair target is covered exactly when at least two DISTINCT words are covered.
Empty targets and singletons stay in the Q denominator. The second-lowest
repair cost per fiber yields the entire minimum-pair-repair histogram.

This analyzes all targets without Q separate decoder runs, but still uses an
EXPONENTIAL word census. A full preflight word-budget guard returns no partial
coverage claim. The known-word analysis is never given to the actual solver.

For fixed labels, with gamma the covered fraction of native words,

```text
beta_label <= (3^M/(2Q))*gamma = gamma/6 at source density1/3.
```

This counting bound is deterministic. Population coverage across random labels
requires a separate source-law theorem. Uniform word probes have PLANTED /
size-biased targets; they are geometry diagnostics, not uniform-target pair
benchmarks. Small gamma is not a generic hardness statement: the explicit
zero-label kernel can have exponentially small word recall while the easy
nonempty target is decoded to a pair. This control is tested.

Each missed genuine pair target must lose at least one word, and different
targets have disjoint fibers. Hence covered_pair_targets>=true_pair_targets
minus(3^M-recovered_words). Combining this with the existing exact native
two-element mass bound gives

```text
E_labels beta >= max(0,(2/9-2/Q^2)/6-(1-E_labels gamma)/3).
```

This is positive if PROVEN mean word recall exceeds8/9+1/Q^2. It removes a
pair-correlation assumption at sufficiently high recall, not the need for a
population theorem. Do not insert planted sample recall for the unknown mean.

## Live Findings

Three exhaustive fixed-label controls classify59,787 words and account for
179,361 uniform targets. These are conditional coverage facts, not population
estimates:

| Width | Actual Pair Targets | One Repair | Two Repairs | Candidate Lists |
| --- | ---: | ---: | ---: | ---: |
| 2 | 1 | 1 | 1 | 54 / 198 |
| 6 | 129 | 128 | 129 | 150 / 1,734 |
| 10 | 7,686 | 6,873 | 7,676 | 246 / 4,806 |

The full candidate budget is C*sum_{j=0}^k binomial(2M,j)*(2B)^j, not simply
the number of observed successful words. Increasing k with M can make the
list exponential; the finite success of depth2 proves no scalable algorithm.

The artifact contains ACTUAL missed pair certificates at M6/Q2187/target470
and M10/Q177147/target97. Both fibers have two original words; the full recorded
single-repair decoder recovers only one, charging150 /246 candidates. Complete
fibers and every rounded projection are recorded and independently replayed.
This falsifies DETERMINISTIC COMPLETENESS of those recorded public policies.
It does not falsify every randomized pointwise success bound, every public
basis, average-case coverage, general CVP or the underlying quantum source.

Fifteen planted-word probe batches classify3,840 known words across five root
sizes. At r32/M30, one repair recovers only1,0,0 of256 words in the three label
batches; two repairs recover4,2,1. These are WORD observations, not measured
uniform-target pair successes. Typical words require several repairs.
Every r32 chart had256 distinct observed repair patterns with no sample
collisions. That is not a proof that the true collision probability is zero.
Pairwise sample comparisons and different charts are dependent; never treat
all sample pairs as independent Bernoulli trials.

## Attempts To Kill The Interpretation

- Small conditional success need not survive fresh labels or larger roots.
- More repairs can just hide exponential enumeration behind a better control.
- Orthogonal GS rows do not grant independent errors or a Gaussian joint law.
- Word recall is not pair coverage; the exact bucket count and source density matter.
- Failed recorded policies do not rule out target-adaptive or nonlinear solvers.
- Training/geometry words must not leak into unknown-target decoder inputs.
- Independent arithmetic replay is not independent LLL search or external review.

The next high-upside question is whether error patterns have a learnable,
polynomially sized structure. See `NATIVE_TERNARY_REPAIR_CATALOG_TARGET.md`.
If their population collision mass is exponentially small, fixed polynomial
catalogs fail by a rigorous counting argument. If they concentrate, implement
the catalog decoder and test TWO-witness uniform-target coverage, not word recall.

Run `python theorems/ternary_pair_cell_coverage.py --write`, then
`node research/certificates/ternary_pair_cell_coverage_crosscheck.js`.
Routine qsearch/registry exposure belongs to Gemini/Antigravity.
