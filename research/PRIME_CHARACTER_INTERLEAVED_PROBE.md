# A Fast Interleaved Decoder Does Not Preserve This DQI Objective

2026-10-18. Scoped constructive hypothesis test. LOCAL APPLICATION REVIEW
PENDING. No general interleaving impossibility, novelty or speedup claim.

## Candidate And Decision

The [finite single-copy DQI certificate](PRIME_CHARACTER_FINITE_READOUT.md)
has a useful radius32 score but lacks a practical capacity decoder. A
concrete attempted repair is to prepare c error rows with the SAME support,
decode their syndromes collaboratively, erase the errors, apply separate
Fourier transforms, and select the best of the resulting c polynomials.

Classical collaborative decoding is real prior art:
[Schmidt-Sidorenko-Bossert](https://arxiv.org/abs/cs/0610074) studies
multi-sequence syndrome reconstruction beyond half distance. We derive and
execute the power-sum version for our prescribed points1,...,N rather than
importing their cyclic-domain/failure theorem without checking its premises.

The decoder ingredient WORKS on the saved large basis controls. The attempted
quantum repair FAILS to preserve the single-polynomial score. Under the local
bound, selecting among five original output rows reaches110/127 with probability
at most1.863e-8, versus the correct single-copy conditional floor0.314586.
The extra rows retain which-support information. The joint product correlation
is enhanced, but each original polynomial is nearly uniformly distributed.

Cut this plain shared-support/separate-readout replacement from the current
algorithm plan. Retain the verified classical decoder as a reusable primitive.
Do NOT infer that all interleaved sources or joint quantum processing fail.

## Input, Mechanism And Resource Accounting

Same explicit prime-character OPI: p=3 mod4, public shifts/orientations,
quadratic half-density lists, N points, degree<K. At each chosen support S,
prepare independent nonzero Fourier values in every row using the native
ghat_i phases. The row error values are independent uniform Fp* in basis
probability, conditional on S. No random input-shift assumption is used.

There are cN error registers and cK syndrome registers of O(log p) bits.
The proposed cheap step solves a stacked field-linear system. Reversible
source/arithmetic/decoder/QFT compilation is NOT supplied here, but even
granting efficient exact operations does not repair the output objective.

For fixed positive gap, a constant number of rows could in principle replace
the known generic capacity decoder's severe gap-dependent exponent. That is
why this was worth testing. It is not a new classical decoding algorithm.
The strongest comparator is the correctly prepared single-copy DQI state,
plus the saved same-input classical109/127 word; this experiment produces no
new classical-hardness or matched-runtime claim.

## Actual Syndrome-Only Decoder

For row a, use power sums

    s[a,j]=sum_(i in S) e[a,i]*(i+1)^j, j=0,...,K-1.

A monic locator Lambda(z)=product_(i in S)(z-(i+1)) obeys

    sum_(m=0)^d Lambda_m*s[a,j+m]=0,
    Lambda_d=1, j=0,...,K-d-1.

At a maximum burst cap ell, the stacked recurrence matrix has
c*(K-ell) rows and ell columns. Radius32,K39 needs at least five rows for
this route: four rows give only28 equations, five give35.

The implementation first computes rank d of that CAP matrix, without the
source support. It solves the degree-d recurrence, checks all locator roots
among the N public points, solves a Vandermonde system for every row, and
replays ALL K syndromes. Every failure stays UNKNOWN, not a reroll.

The cap-rank check certifies uniqueness against the WHOLE burst ball, not
only weight d. Multiples of the recovered degree-d locator by monic polynomials
of degree ell-d form an affine solution family of dimension ell-d. Rank d
means this is the entire degree-ell recurrence family. Any competing locator
of degree<=ell, extended with powers of z, must therefore contain the recovered
nonzero roots. Its support contains S. Since at most ell<K public columns
are independent, the replayed errors are unique and all extra values are zero.
This reasoning also handles actual weights smaller than the requested cap.

The FLINT nmod reference uses word primes; that operational limit is recorded
and is not a general finite-field restriction on the mathematics.

Executed at p=2^61-1,N127,K39,cap32:

- Five independent rows: rank32, all32 positions and all values recovered.
- Eight independent rows: rank32, same full recovery.
- Two rows: only14 cap equations; recovery remains UNKNOWN.
- Five identical rows:35 equations but rank7; recovery remains UNKNOWN.

The controls use prefixes of the SAME seeded error block. All errors, supports,
syndromes, locator coefficients and failed cases are retained. The decoder
itself receives only syndromes/public parameters. These are classical basis
executions, not a coherent quantum decoder or a measured failure probability.

## Local Fixed-Support Rank Guarantee

Let j<=ell be the actual support size and w=K-ell. The cap matrix factors
as W*V, where V is the j-by-ell Vandermonde of support nodes and

    W[(a,t),i]=e[a,i]*(i+1)^t, 0<=t<w.

If cw>=ell, partition any j columns into c groups of size at most w. A j-minor
of W is a degree-j polynomial in the independent row error values. Setting
one group to1 in its assigned row and0 in other rows exhibits a nonzero
block-Vandermonde determinant. This exhibits a nonzero polynomial; the actual
sampling domain remains Fp*, not that zero-containing witness assignment.

Schwartz-Zippel on Fp* gives rank-failure probability at most

    zeta = ell/(p-1).

On the rank-good event the preceding decoder necessarily succeeds. The bound
is uniform over support and arbitrary support superposition weights. Deliberately
sampling every row as a copy of the first does NOT satisfy independence.
Repeated-value OUTCOMES are still possible under independent sampling; their
mass is included in the rank-failure bound. The exhaustive p5 control retains
all64 such failures among256 source-value tuples rather than rerolling them.

## Why The Joint Readout Changes The Task

For every S let phi_S(x)=product_(i in S)g_i(Q_x(i+1)), with the native centered,
unit-variance predicate g_i. Apart from normalization, joint readout prepares

    Psi(x_1,...,x_c)=sum_S b_S*product_(a=1)^c phi_S(x_a),

not the single-copy sum_S b_S*phi_S(x). The scalar b_S may be arbitrary, not
just uniform within each degree. Copying the support into all rows removes
its useful coherence from an individual row when other rows are ignored.

To make that statement finite and fixed-input, strengthen the previous source
lemma to the ALL-support frame. Each support source has flat nonzero values;
different supports have disjoint preimages. Its ambiguity bound is uniform
over S. For M=sum_(r<=ell)C(N,r) and the existing epsilon bound,

    ||G_all_support-I|| <= delta=max(1,M-1)*epsilon.

This applies to arbitrary support coefficients, not only radial ones. It is a
proof about an exponentially large frame, NOT an exponential matrix built by
the large-input code. Only the O(N)-bit count M is evaluated.

If delta<1, polar decomposition gives V=J*sqrt(G) with J an isometry, and
||V-J||<=gamma=delta/(1-delta). For c rows, put eta=(1+gamma)^c-1. If eta<1,
the normalized actual joint vector differs in trace distance by at most
2eta/(1-eta) from the J-frame joint state. The latter has EXACTLY the marginal
sum_S |b_S|^2 |J S><J S|, for c>=2. Replacing J by V in that mixture costs
at most gamma in trace distance; each native phi_S column has norm1.

For these half-density predicates, pointwise

    g_i(x)^2 in [(p-1)/(p+1),(p+1)/(p-1)].

Since |S|<=ell, every mixture of normalized |phi_S|^2 differs from the uniform
coefficient distribution in TV by at most

    density_error = (((p+1)/(p-1))^ell-1)/2.

This is why the objective collapses. The joint product observable can improve
while individual polynomials remain almost uniform. No independent-output-row
assumption is made.

## Rank Postselection Must Also Be Paid

Do not simply assume successful rank tests leave the state unchanged. Their
failed source mass is at most zeta. But multiplying ALL that mass by M would
give a useless bound. Separate failed fibers which are genuinely colliding
from singleton failed fibers. Only the former can amplify coherently.

Two distinct source tuples have fully nonzero entries on their common support.
A collision on all c syndromes implies a collision on the first row, unless
the supports agree, in which case column independence forbids any collision.
Thus genuinely colliding source mass is at most the earlier single-row epsilon.
Every joint fiber has size at most M. With C=(M-1)*epsilon, the failed image
has squared norm at most b+C, where b<=zeta. Good and failed images are disjoint
because the decoder flag is a function of the public syndromes. Therefore

    rank_herald_trace_distance^2 <= (zeta+C)/(1+C).

Add its rational square-root upper enclosure to the preceding marginal bound.
This licenses the actual rank-heralded receiver model, not just a hypothetical
complete unique verifier. The source-to-gate compiler remains unimplemented.

At N127,K39,ell32,p61, delta<=5.266e-69, zeta<=1.388e-17. For five and eight
rows, each rank-heralded output polynomial is within3.726e-9 TV of a uniform
polynomial. Hence its normalized mean is at most0.500000003726.

## Selecting The Best Row Does Not Repair It

Uniform degree<K polynomials give K-wise independent predicate indicators,
not a fully independent N-bit score. Their even central moments through K
match the binomial moments. Exact integer sums compute these moments; Markov's
inequality supplies a conservative tail upper bound, choosing the strongest
legal even order. No full binomial tail is asserted.

For110/127 the uniform upper bound is about4.852e-14 using moment order38.
Adding the marginal TV and UNION bounding over output rows gives:

- Best of five original rows: probability<=1.863e-8.
- Best of eight original rows: probability<=2.981e-8.

The rows may be arbitrarily correlated. These are upper bounds conditional
on rank herald; aborting on failure cannot increase per-attempt success.
Extra rare postselection, constructing NEW linear combinations, joint quantum
processing or support-dependent feedforward are not covered by this claim.
They require their own mechanism and costs, not this simple replacement.

## Independent Physical And Mathematical Checks

Four full joint-state controls use p7/11,N4,K2,ell1, both zero conventions.
All145/401 shared-support error tuples and2401/14641 joint coefficient words
are explicitly charged. Native products of centered predicates reproduce an
independent complete syndrome/QFT amplitude calculation.

At p7 including zero, single-copy mean0.760829 becomes individual mean0.553571;
at p11 it becomes0.534091 from0.785897. Strict siblings are retained. Marginal
purity is5/16, while the joint centered-product correlation is about0.567/0.510.
The joint task is genuinely enhanced; the required individual task is not.

Other controls include exhaustive whole-ball uniqueness checks at p5, a nonzero
rank-minor witness, lower actual weights/zero rows, and an independent ALL-support
Gram from a one-dimensional dual code at p10007. Its three-copy polar tensor
calculation checks the nontrivial frame argument without p^4 coefficient-word
enumeration. Approximation/certification failures are never converted to hardness.

## Attempt To Prove The Rejection Wrong

- The frame bound must hold on arbitrary support coefficients. Fixed-support
  error probabilities are uniform in S, so it is stronger than a per-radial-
  state norm observation. The nontrivial Gram test checks this distinction.
- Rank failure is not identical to source collision. Both are paid separately;
  amplifying only collision mass is essential and explicitly tested.
- Repeated row values invalidate the independence premise. They remain failed
  controls rather than favorable source rerolls.
- Finite density is not exactly1/2, so the marginal is not declared exactly
  uniform. The exact pointwise density ratio is retained for strict and
  zero-including lists.
- The result only rejects this shared-support product-packet/separate-QFT/
  original-row-selection route. It does NOT reject general interleaving,
  asymmetric support sources, other local packets, joint readout or a new
  phase-correction primitive. A faster decoder alone is insufficient.

Next constructive work must restore the original single-polynomial interference
while retaining cheap syndrome access, or compare another independent route.
Do not compile this failed replacement or add more neighboring decoder/rank
sweeps. Any auxiliary measurement/feedforward repair must explicitly show how
its support-dependent phases are corrected without reintroducing the missing
single-copy decoder or uncharged postselection.

```text
python theorems/prime_character_interleaved_probe.py --write
python -m pytest -q tests/test_prime_character_interleaved_probe.py
```
