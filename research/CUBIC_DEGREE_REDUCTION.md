# A Polynomial Classical Easy Region For Cubic / RS Search

Status: constructive derivation with reference implementation (`cubic-degree-reduction-v2`),
expanded $n=64$ local campaign, and executed $>64$-bit local controls at $n \in \{96, 128\}$;
independent proof review pending. No new quantum algorithm or claim of a new local algebraic primitive.

## Prior Art And Exact Scope

[Cohen and Tal, Two Structural Results for Low Degree Polynomials and
Applications, Sections 4 and B](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.APPROX-RANDOM.2015.680)
give algorithms for degree reduction and constant affine restrictions.
Our cubic specialization uses third-polar linear constraints and elementary
quadratic-form reduction. The rejection-based approach in
`CUBIC_FLAT_POLARIZATION.md` also belongs to this established structural
framework, not a newly discovered primitive.

The repository's earlier `explicit_cubic_opi.py` already cites this work.
However, it uses balanced predicates of the form z0=g(z1,...), an affine
graph lift, and paid fallbacks. Uniform cubic ANFs on all n bits do not
satisfy that graph-form promise. Do not substitute that input distribution
or transfer an unproved local-success assumption.

The native relation remains f_i(x_i)=0 for independent uniform cubic ANFs,
and Hx=0 for H[j,i]=gamma_i^j over F_(2^n). The NEW parameter region has a
decreasing check rate r/m, not the fixed positive check rate of the
asymptotic conjecture in
[Briaud et al., arXiv:2509.07276v1](https://arxiv.org/html/2509.07276v1).
The original fixed-rate conjecture remains open.

## Local Construction

Define

    ell(n) = floor((1+sqrt(8n-7))/2),
    k(n)   = floor((ell(n)-1)/2).

Then ell(ell-1)/2<n. For every nonconstant-one Boolean polynomial of degree
at most three, the following procedure returns an affine zero flat of
dimension k, except for explicitly bounded random-draw failures.

1. Find an accepted origin a with up to 64n independent uniform samples.
   The nonzero Boolean polynomial 1+f has degree at most three and therefore
   weight at least 2^(n-3). Origin failure is at most 2^(-8n).
   Constant-one inputs are detected exactly, not resampled.
2. Build an ordered subspace U on which the third polar tensor vanishes.
   At dimension j, solve T(u_s,u_t,v)=0 for all s<t. There are at most
   binom(j,2) homogeneous linear constraints. Their kernel contains U and
   has dimension at least n-binom(j,2)>j for every required extension.
3. A uniform kernel sample lies outside U with probability at least 1/2.
   Allow 2n samples per stage. Each stage fails with probability at most
   2^(-2n), uniformly over previous choices. Linear-span membership uses
   echelon elimination, NOT an explicit list of 2^j vectors.
4. On a+U the original polynomial has degree at most two. Read its linear
   and quadratic coefficients from ell+binom(ell,2) evaluations.
5. Alternating Gram-Schmidt produces a bilinear-isotropic subspace I of
   dimension ell-rank(B)/2>=ceil(ell/2). The quadratic form restricted to I
   is linear. Take the kernel of this linear functional, losing at most
   one dimension, and retain exactly k directions.

Every operation has polynomial complexity in n and the explicit input
length. The number of candidates does not contain a factor 2^k. This is
the substantive improvement over the earlier rejection-based local method.
It may return a smaller flat; its guarantee is stronger, not uniformly
better finite dimensions or wall time.

## Polynomial Witness Certificate

The restriction of f to an alleged k-flat still has degree at most three.
Evaluate it at coefficient vectors of Hamming weight zero through three.
If all these values vanish, Boolean Mobius inversion makes every ANF
coefficient vanish; hence the restriction is identically zero.

This takes sum_(j<=3) binom(k,j) evaluations, not 2^k. Direction independence
is checked separately. The verifier uses the original ANF terms, not the
producer's quadratic surrogate. A regression cubic vanishing at the origin
and all unit vectors demonstrates why checking only linear coefficients
would be unsound.

## Global Average-Case Theorem

Use m independent uniform cubic inputs with arbitrary fixed distinct
gamma_i and the same local parameters. Conditional on local success, the
direction spaces are independent uniform k-subspaces:

- The uniform cubic ensemble is affine-invariant.
- Origin sampling and uniform kernel sampling are equivariant in law.
- The quadratic reduction acts on the ordered U-coordinate form, so an
  ambient affine change leaves its coordinate choices unchanged.
- Truncation to a FIXED guaranteed k prevents a dimension-selection bias.

This gives the conditional MDS rank bound established in
`CUBIC_RS_AFFINE_FLATS.md`. The exact compressed system has mk parameters
and rn binary rows. With S(n)=sum_(j=0)^3 binom(n,j), total solver failure is
at most

    m*2^(-S(n))
      + m*2^(-8n)
      + m*ell(n)*2^(-2n)
      + min(1, 2^(rn-m*k(n))).

The first term pays for constant-one inputs. The next two pay for ALL
local sampling failures. The last pays for rank deficiency; full row rank
makes every offset consistent. No assumption of IID binary matrix rows,
independent offsets, balanced cubic values, or favorable seed selection is
used.

The report rounds each of the four positive terms UP to a dyadic power
and bounds the sum by four times the largest. This conservative arithmetic
does not construct an integer with S(n) bits just to print a tail bound.

For n>=16, choose

    m=n^2, r=n*(k(n)-1).

Then mk-rn=n^2, all failure terms vanish as n grows, and

    r=Theta(n^(3/2)), r/m=Theta(n^(-1/2)).

This is a polynomial-time randomized classical solver with high success
probability for this asymptotic SUBFAMILY. The constituent local structural
algorithm is known. The combination and explicit parameter accounting here
need independent review before any external theorem claim.

For fixed r/m=rho>0, rn grows like rho*m*n whereas mk grows like
m*sqrt(n/2). The rank bound becomes vacuous. We have NOT removed the
fixed-rate obstruction, and no failed compressed solve proves native
unsatisfiability or general classical hardness.

## Native Controls, Expanded Local Campaigns, And >64-Bit Local Widths

The saved n=16 and n=32 cubic coefficients, field bases, and RS points are
reused from the previous audit. The number of code checks is deliberately
changed to the stated easy-region family:

| n | ell | retained k | old checks | new checks | rows | flat parameters |
|---|---|---|---|---|---|---|
| 16 | 6 | 2 | 30 | 16 | 256 | 512 |
| 32 | 8 | 3 | 120 | 64 | 2048 | 3072 |

Do not describe this as improving the previous n32,r120 algorithm. That
harder finite case remains solved by the preceding rejection-based method.
Both current full native witnesses are checked against their ACTUAL changed
matrices and every original ANF.

In `cubic-degree-reduction-v2`, local cubic ANF support in `theorems/cubic_degree_reduction.py`
is extended past the inherited 64-bit cap up to `MAX_LOCAL_BITS = 256` without modifying the
frozen reference producers (`cubic_rs_affine_flats.py` and `cubic_flat_polarization.py`):

| Campaign | Width `n` | ANF Monomials `S(n)` | Lowered `ell(n)` | Zero-Flat `k(n)` | Blocks Tested | Failures | Low-Weight Cert Evals / Block | Global RS Solved |
|---|---|---|---|---|---|---|---|---|
| Replayed `n64_local_flats` | 64 | 45,761 | 11 | 5 | 16 | 0 | 26 | `False` |
| Expanded `n64_expanded_local_campaign` | 64 | 45,761 | 11 | 5 | 64 | 0 | 26 | `False` |
| `beyond_64bit_local_controls` ($n=96$) | 96 | 147,537 | 14 | 6 | 4 | 0 | 42 | `False` |
| `beyond_64bit_local_controls` ($n=128$) | 128 | 349,633 | 16 | 7 | 2 | 0 | 64 | `False` |

All local campaigns execute with `span_points_enumerated = 0` and verify every constructed
$k(n)$-flat via the exact degree-$\le 3$ low-weight Mobius certificate (`certify_zero_flat`)
against `polynomial.direct(point)`. No full $m=n^2$ global code-constrained solve is claimed
at $n \ge 64$, and lifting the 64-bit local coefficient width limit is an implementation
extension rather than evidence of a fixed-rate asymptotic dequantization.

## Audit And Remaining Questions

The preceding 499/1000 success derivation survives the current manual audit:
its minimum-weight argument is valid on adaptively chosen kernels, and its
conditional MDS argument requires the ideal ensemble, not the fixed seed.
It remains review pending. A new independent reviewer should especially
challenge the affine-equivariance argument and the sum over RS zero sets.

No credible polynomial construction bypassing the one-flat restriction at
fixed positive check rate was established in this pass. Nonlinear graphs
and multiple-flat unions introduce a new global consistency problem; counting
their free parameters does not solve it. Do not convert those sketches into
accepted candidates or another uncharged relaxation.

Next scientific priority: a genuinely different global mechanism or a
meaningful reduction for the quantum relation. Further successful finite
flat runs are useful validation but not the main-model research objective.

Reproduce:

    python theorems/cubic_degree_reduction.py
    python -m pytest -q tests/test_cubic_degree_reduction.py

The producer does not modify its input reports. Its report records source,
dependency, and input-report hashes. No central candidate admission,
qsearch/UI wiring, commit, or push is part of this pass.
