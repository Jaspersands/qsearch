# Random-Kernel Regularity Without A Rank-Dependent Prime Guard

**Later 29 October follow-up:** [spanning-block sums](SPANNING_BLOCK_REGULAR_SDE.md)
give a simpler generic wrapper around arbitrary-input field SDE solvers.
They also remove dependence on the symmetric closure's degree-only guard,
conditional on the chosen backend. This supersedes the proposed all-coset
kernel extension, not the earlier controls or cheaper certified regimes.

29 October 2026. Constructive local deduction, exact arithmetic implementation
and independent automated adversarial review. Not a human-reviewed novelty
claim, a complete quantum receiver, or an established quantum speedup.

## Decision And Research Value

The [previous simultaneous ring converter](PRIME_POWER_REGULAR_SDE.md)
requires p-1>=4*M(r), with M(r) quadratic in the central cyclic rank.
This requirement came from demanding that its short first-level blocks
be full spark. It is not inherent to regular prime-power lifting.

**Randomized longer kernel relations remove that rank-dependent prime
condition.** Each attempted block has m=2(r+1) columns. A uniform kernel
relation has spanning active support with joint probability at least 1/4
on IID uniform labels, for EVERY odd prime and positive rank. Bounded
rejection produces spanning blocks; the nonzero symmetric contraction
preserves a selected block's active support, then ordinary regular Hensel
lifting finishes the mixed-order cancellation.

The remaining field restriction is degree-only: for g=gcd(d,p-1)>=2,
`p>=16*g^(2*g+2)`, inherited from the symmetric contraction. Require d<p.
For g=1 no symmetric closure is needed. This is not a uniform-in-degree
polynomial algorithm or an all-characteristic nonlinear solver.

The conditional capped source cost is O_g(R^2*(log R+b)) per grade,
including rejected blocks and paid pilots, where R is the fixed ambient
cyclic-rank upper bound and b controls local failure. This extends the
direct prime-power construction to unbounded rank at fixed admitted prime,
with a larger cost than the previous short-block method where both apply.
Keep the cheaper method in its certified regime; do not call the new
method uniformly faster.

The underlying collision scaffold is established prior work:
[Ivanyos--Santha, Lemma 12](https://arxiv.org/html/1503.09016v2).
This pass changes how first-level relations are selected and retained for
regularity, rather than claiming a new arbitrary-instance SDE solver.
Elementary finite-field counting and Hensel lifting are not new ingredients.
A targeted literature search is not a novelty certificate.

## 1. Input And Source Contract

The intended application is removal of a homogeneous central grade Z from
a Rees HSP source. Its actual character support is the unknown module
`C=(H intersect Z)^perp`. Unit dilation acts as u^d on Z and must preserve
the HIDDEN subgroup, not merely the ambient grading. Fresh ideal coset
sources give IID uniform labels in C, conditional on previous transcripts.

Use the previous public pilot procedure: P=R+2 fresh labels generate C'.
Compute full intrinsic invariant-factor coordinates, their embedding back
into dual(Z), and a membership map using integer relation lattices. If a
new label lies outside C', abort the whole episode. Never quotient by an
estimated hidden central intersection. A zero-rank C' uses the earlier
one-fresh-zero-label branch, outside the positive-rank collector API.

Conditional on complete pilots C'=C, the intrinsic residues of fresh labels
are IID uniform in F_p^r, r<=R. The first-level policy uses this observed
intrinsic rank r. Pilot counts and a uniform whole-episode cost use the
FIXED ambient R, not a rank chosen after observing the pilots.

The implemented API takes supplied intrinsic label coordinates through a
`draw_block(width)` callback. It does not implement Fourier measurement,
learn pilot coordinates, certify independence, or verify an embedding back
into the original ambient module. Those remain explicit receiver obligations.
It counts every supplied label, verifies every returned arithmetic witness,
and rejects malformed data. High-order module bit lengths are charged.

## 2. Exact Joint Probability, Not A Fixed-Matrix Claim

Let A be an IID uniform r-by-m matrix over F_p, r>=1, m>r. One raw trial:

1. Reject if rank(A)<r.
2. Otherwise choose y uniformly from ker(A), INCLUDING zero, by independent
   uniform coefficients in an exact kernel basis.
3. Accept iff the original columns with y_i!=0 have rank r.

Define the full-row-rank probability

```
rho(r,k) = product_(i=0..r-1) (1-p^(i-k))     if k>=r,
rho(r,k) = 0                                if k<r.
```

Fix a nonzero y of support size t. The relation A*y=0 makes the restriction
of A to those coordinates factor through a space of dimension t-1.
Requiring active column rank r gives

```
number of qualifying A
  = p^(r*(m-t)) * p^(r*(t-1)) * rho(r,t-1).
```

Such A necessarily has full row rank. Every qualifying pair (A,y) has
probability `p^(-r*m) * p^(-(m-r))` in the ACTUAL trial, since its kernel
dimension is m-r. Therefore

```
Pr[Y=y AND trial accepts] = p^(-m)*rho(r,t-1),

alpha(p,r,m)
  = p^(-m) * sum_(t=r+1..m) binom(m,t)*(p-1)^t*rho(r,t-1).
```

This includes rank-deficient A as rejected probability mass. It does not
condition them away. It does NOT say that the algorithm's kernel sample
is an ambient-uniform vector for a fixed matrix. The equality merely
expresses the joint acceptance probability as an expectation over an
AUXILIARY uniform ambient vector. This distinction is essential.

### Uniform Constant Bound

Set m=2(r+1). The auxiliary uniform vector has expected zero count m/p.
Weight at most r+1 entails at least m/2 zeros. Markov gives probability
at most 2/p for that bad weight event. For weight t>=r+2,

```
rho(r,t-1) >= 1-sum_(i=0..r-1) p^(i-(t-1))
           >= 1-1/(p*(p-1)).
```

Consequently, uniformly in r>=1 and odd p,

```
alpha(p,r,2(r+1)) >= (1-2/p)*(1-1/(p*(p-1))) >= 5/18 > 1/4.
```

No concentration conjecture, fitted rank histogram or lower bound on p/r
is used. Exact exhaustive counts at (p,r,m)=(3,1,4) and (5,1,4) give
1616/2187 and 72064/78125 respectively. Tests also enumerate two-row cases.

### Decisive Falsifier Of A Stronger Claim

For the FULL-RANK fixed matrix A=[I_r | 0], every kernel relation is
supported only on zero columns, so active rank is zero. Repeatedly using
this matrix fails forever under any coefficient randomness. The success
theorem requires fresh IID matrices, not just full rank or a random seed.
The live artifact records a capped fixed-matrix ABORT with all 96 consumed
labels retained, rather than silently retrying until success.

## 3. Preserve The Sampled Relations

Collect h=(g-1)r+1 accepted blocks for g>=2; use h=1 for g=1. Every accepted
block carries a verified nonzero linear relation whose active columns
span F_p^r. Decompose its nonzero coefficients into power cosets and roots
as in the existing collision construction. Invertible row compression
preserves the original relation and active span.

The second-level relation selects at least one block with nonzero weight.
Every coefficient of the symmetric contraction is nonzero, and different
cells have disjoint original supports. Thus ALL active columns of that
block remain active in the final SDE witness. Their span is still F_p^r.
Accepted blocks may be heavily biased; the second-level construction is
valid on arbitrary cell values and does not need a renewed IID promise.

The Bezout conversion to ORIGINAL degree d preserves nonzero support.
The active Jacobian has rank r because p does not divide d. Apply the
existing simultaneous mixed-order lift; active scales stay units and
inactive scales stay exactly zero. Verify each original supplied modulus.
Before a future quantum conversion, also verify the embedded equation in
the original ambient character module.

Do not recompute a first-free-variable kernel relation after collection.
That can discard the spanning support. The code passes every verified
sampled relation explicitly through `first_level_relations`, with the
wider `first_level_width` paid in the collision and root budgets.
The g=1 branch also uses its sampled relation directly, not the generic
deterministic linear solver. A duplicated e1/e2-column regression exhibits
a spanning sampled relation while the first null basis vector has rank one.

## 4. All Retries And Random Bits Are Paid

For local failure parameter b>=4 let

```
K = 4*(b+ceil(log2(h)))        # attempts per required block
N = h*K*(m-r)                # kernel coefficient draws, upper bound
L = b+ceil(log2(N))           # bit rejections per coefficient draw
```

Each block attempt consumes m FRESH source labels. Rank-deficient blocks,
zero relations, nonspanning active supports and integer-rejection aborts
are retained. There is no free resampling of measured labels.

The ideal uncapped-uniform collector has block-exhaustion probability

```
h*(3/4)^K <= h*exp(-(b+ceil(log2(h)))) <= 2^-b.
```

Uniform integer sampling uses fresh fair bits and at most L bit-rejection
attempts per draw. A first-error coupling to the ideal infinite bit tape
adds at most `N/2^L<=2^-b`. Do not condition on eventual completion and then
assert the accepted adaptive draws are IID. Actual kernel calls, bit draws
and bits are recorded; deterministic overuse and backend errors are not
misclassified as ordinary stochastic aborts.

Wider blocks also increase the symmetric stage's root allowance. The
correct bound is

```
R_roots = h*(m+2) + g*(g+1)/2.
```

This pays first-level classification before and after normalization,
second-level classification and closure roots. All downstream scalar,
splitting and bit-rejection caps are recomputed from that allowance.
The previous `h*(r+3)+...` allowance would be invalid here. The resulting
separate symmetric-stage exhaustion probability is at most 2^-b; it is
zero for g=1. Its caps are recorded even on an aborted run; actual internal
stage counters are available on success, not after every internal exception.

Use fresh P=R+2 pilots on EVERY whole-episode retry. With complete pilots
the collection guarantees above apply. Incomplete pilots are charged
wholesale at probability less than 1/[p^2(p-1)]<=1/16. Every accepted
original-module cancellation still gives the correct quotient source
pointwise even when pilots were incomplete; it does not change the quotient.

For uniform cost, compute h_R, m_R and K_R at ambient rank R. Then

```
Pr[whole-episode failure] <= 1/16+3*2^-b <= 1/4,
sources per episode <= R+2+h_R*K_R*m_R = B,
expected predecessors per accepted conversion <= (4/3)*B <= 2*B.
```

Both pilot overhead and all rejected blocks are included. The API separates
observed intrinsic rank from ambient_cyclic_rank; the latter controls
pilot count and the uniform source bound. A source callback's implementation
cost, whole receiver gate count, primality arithmetic clock and OS deadline
are NOT certified by these counters.

The prior recursive expectation/product and whole-run Markov leaf cap can
use this per-grade bound, with disjoint fresh sources and pointwise output
independence. Approximate sources still need a JOINT input error and a
complete flagged-channel precision budget. This pass does not implement
that recursive controller or promote its formal status.

## 5. Live Arithmetic Evidence

Run `python qsearch.py prime-power-sde --random-kernel --write` to retain
all attempted blocks, sampled relations, accepted indices, final field
and ring witnesses, actual counters, caps and exact probability bounds in
`research/reductions/random_regular_sde.json`.

| Prime | Original degree | Intrinsic rank | Accepted blocks / attempts | Labels consumed | Prior short-block guard |
| --- | --- | --- | --- | --- | --- |
| 3 | 1 | 3 | 1 / 1 | 8 | Inconclusive |
| 1031 | 2 | 16 | 17 / 17 | 578 | Inconclusive |
| 105037 | 3 | 4 | 9 / 9 | 90 | Admitted |
| 2^128-275 | 12 | 2 | 7 / 7 | 42 | Admitted |

The quadratic rank-16 case is outside the earlier p-1>=4*(r+1)^2 guard,
while satisfying the degree-only p>=1024 guard. It lifts mixed exponents
1,2,4,3 repeated across all sixteen factors. Its bank cap is 30056; the
conditional expected predecessor upper bound INCLUDING pilots is 60148.
The fourth control checks degree-12 to degree-4 exponent reduction.

These are deterministic seeded arithmetic fixtures, not physical IID
certification, quantum simulations or runtime comparisons. The final
artifact explicitly says no pilot acquisition or quantum receiver was
executed and no speedup was established. The fixed-matrix falsifier is a
source-assumption countercontrol, not a new toy candidate or a hardness
claim about an HSP family. No registry evidence status is promoted.

## 6. Review And Remaining Work

An independent automated reviewer checked the exact pair counting,
constant lower bound, biased accepted blocks, nonzero support preservation,
pilot conditioning and source budgets. It confirmed the joint law and
required the wider root allowance and retention in the g=1 branch; both
are implemented. Independent enumeration reproduced the two fractions
above. A read-only implementation review found no actionable issue and
checked 900 ambient/intrinsic budget pairs, duplicate-column retention and
exception classification. This is not human or kernel verification.

The remaining scientific/implementation obligations are:

- Compile pilot subgroup coordinates with transformation and membership
  maps, and replay every cancellation in the original ambient module.
- Execute the complete quotient-source policy with real source handles,
  all failures and the joint approximation budget. Algebraic successes
  alone cannot certify this channel.
- Address the degree-only small-field regime, rather than silently using
  a symmetric closure that may not exist there.
- Compare the resulting direct explicit-Lie algorithm with the existing
  outer reduction and prior art before making an originality claim.
- Identify a compelling native application and its strongest classical
  competitor. This classical SDE subroutine is not itself a speedup.

The source-count question asked in this pass is resolved conditionally;
additional rank histograms would not strengthen its proof. Choose the
next task by which end-to-end obligation it removes, not by generating
more parameter tables.

## 7. Verification Checkpoint

**517 selected tests passed in 73.14 seconds**, using Anaconda Python
3.13.5, disabled pytest plugin autoload, warnings as errors, no pytest
cache, and PYTHONPYCACHEPREFIX=/tmp/qsearch-random-kernel-pycache.

```text
python -m pytest -q -p no:cacheprovider -W error tests/test_random_regular_sde.py tests/test_prime_power_rees_descent.py tests/test_rees_hsp_reduction.py tests/test_uniform_bch_rees.py tests/test_rees_complete_instrument.py tests/test_rees_copy_only_outer.py tests/test_central_character_descent.py tests/test_rees_review_controls.py tests/test_power_sde.py tests/test_power_sde_budget.py tests/test_bounded_power_roots.py tests/test_weighted_two_erasure_cascade.py tests/test_odd_power_sde.py tests/test_cli_parser_integrity.py tests/tools/test_split_cli.py tests/test_polynomial_phase_copy_learning.py tests/test_phase_copy_controller_boundaries.py tests/test_ut5_matrix_phase_alignment.py tests/test_symbolic_scalar_phase_erasure.py
python qsearch.py prime-power-sde --random-kernel --write
python qsearch.py validate
```

All four saved controls were independently replayed: accepted linear
relations, active ranks using a separate modular-elimination implementation,
selected column indices, original degree and mixed moduli, unit/zero
scales, all consumed labels and declared counters. The fixed-matrix ABORT
was also replayed. Seven Python syntax checks, 12 JavaScript checks,
registry validation (`valid: true, issues: []`) and tracked diff whitespace
checks passed. No full repository suite or new Lean build is claimed.

Changed files: new random_regular_sde.py and its test, power_sde.py,
power_sde_budget.py, CLI sde routing/docstring/parser test, the live JSON,
this note, the prior regular-SDE and randomness-budget notes, README and
AGENT_HANDOFF. Earlier/concurrent changes outside this scope were preserved.
No commit, push, install, UI modification or external contact occurred.
The reviewer is closed and all owned test processes ended.
