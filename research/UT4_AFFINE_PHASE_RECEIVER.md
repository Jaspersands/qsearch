# Collective Affine-Support Phase Erasure

Status: **constructive derivation, independently unreviewed**. This is a
candidate polynomial-time quotient-line conversion, not an admitted
breakthrough, a novelty claim, or a new external computational reduction.
Finite state tests are diagnostic evidence, not the asymptotic argument.

## What Changed

The preceding graded-dilation construction needed the grade-two component
of the hidden generator's logarithm to vanish. That condition is not needed
by the construction below. Instead of intersecting differently dilated
group supports, it partially Fourier-transforms an abelian normal subgroup,
then combines coordinate registers whose supports are parallel affine lines.
Computational-basis measurement aligns those supports on every outcome.

The proposed target is a standard cyclic HSP in
`G=UT4(Fp)^r`, with `p>3` prime and `H` of order `p`.
The executed public cancellation controller assumes `p=11 mod12`.
The substantive case has nonzero image in the quotient defined below.
No state is supplied with a known hidden coset representative.

## Public Semidirect Coordinates

In one factor write the matrix entries as `(x,b,z,u,v,w)` at positions
`(12,23,34,13,24,14)`. Define

```
q = (x,z)
n = (u,b,v-bz,w-uz).
```

Then `G=N semidirect A`, with `N=Fp^(4r)`, `A=Fp^(2r)`, product
`(n,q)(n',q')=(n+Phi(q)n',q+q')`. In one factor,

```
Phi(x,z)(u,b,v,w) = (u+xb, b, v-zb, w+xv-zu-xzb).
```

Let the unknown generator be `h=(w,v)`, with `v!=0` in `A`, and write
`h^t=(g(t),tv)`. The cocycle identity is
`g(s+t)=g(s)+Phi(sv)g(t)`. The order of the arguments matters.

For a coset represented by `(n0,q0)`, Fourier-transform ONLY `N` and measure
its character `lambda`. This gives, up to global phase,

```
p^(-1/2) sum_t omega^[lambda.Phi(q0)g(t)] |q0+tv>.
```

Every character occurs with probability `p^(-4r)`, independently of the
unknown coset. The algorithm uses the character that actually occurs; it
never requests or postselects a particular one.

## One Fixed Cubic Potential

For the proof only, choose a linear functional `ell` with `ell(v)=1`.
It is UNKNOWN and is not supplied to the receiver. Define

```
Q(q) = Phi(q-ell(q)v) g(ell(q)).
```

The cocycle identity gives

```
Q(q+tv)-Q(q) = Phi(q)g(t).
```

Consequently every input phase is the restriction of the SAME unknown
vector-valued polynomial `Q`, paired with its public character `lambda`.
The coset representative changes only the affine support and global phase.
This is stronger than knowing each coset has some unrelated cubic phase.
Unrelated coefficients per input would invalidate the controller.

To verify the degree bound explicitly, for a logarithmic generator
`(a,b,c,u,v,w)` in one factor, the normal component of `h^t` is

```
(ut+ab*t^2/2,
 bt,
 vt-bc*t^2/2,
 wt+(av-uc)*t^2/2-abc*t^3/3).
```

Substitute this into `Phi(q-ell(q)v)`. Each resulting term has total
degree at most three: the coordinates that are multiplied by a linear
or quadratic action coefficient have degree at most two or one,
respectively. This remains true with ONE shared `ell(q)` across all factors.
All denominators are invertible because `p>3`.

The receiver allocates formal unknowns for every nonconstant coefficient
of `Q`; it does not compute those coefficients. There are
`4r*(binom(2r+3,3)-1)=O(r^4)` such unknowns.

## The Physical Merge

More generally, suppose each independent input is

```
|psi_i> = |L|^(-1/2) sum_(q in a_i+L) omega^[P_i(q)] |q>,
```

where `L` is the SAME unknown linear subspace of `Fp^m` and each `P_i` is
a polynomial whose coefficients are known linear forms in fixed unknown
parameters. Choose public scalars `c_i`, not all zero. Discard zero-scale
inputs and charge them as consumed.

1. Prepare a fresh uniform register `x` on ALL `Fp^m`.
2. Reversibly send each retained `q_i` to `q_i-c_i*x`.
3. Measure every old register, obtaining `y_i`.
4. Retain `x`.

The conditional support is

```
intersection_i c_i^(-1)(a_i-y_i+L).
```

These affine spaces are parallel. Every outcome that can occur makes the
intersection nonempty, so it is one complete coset of `L`, not a small
intersection or a postselection event. Its phase is
`sum_i P_i(y_i+c_i*x)`.

For `k` active line inputs and ambient dimension `m`, every possible branch
has probability `p^(1-m-k)`. There are `p^(m+k-1)` possible branches.
The small probability of ONE specified outcome is never paid: all are used.
For general `dim(L)=l`, replace these by `p^(l-m-kl)` and its reciprocal.
Every source and the fresh register have uniform computational marginals,
so the unconditioned output diagonal stays uniform on the ambient space.
After full phase erasure this is the usual uniform coset-state mixture.

## Public Degree Cancellation

At current degree `d`, let `Y_i` be the public coefficient vector for ALL
degree-`d` monomials and ALL formal unknown parameters. Solve

```
sum_i c_i^d Y_i = 0,    not all c_i zero.
```

Translation does not change the highest homogeneous degree. This identity
therefore removes it on EVERY measurement outcome. Update lower
coefficients using the measured `y_i`; they are still known linear forms in
the same fixed unknowns. Repeat at degrees three, two, and one. Degree zero
is a global phase. This erases, rather than estimates, the polynomial.

The diagonal-equation strategy is known, not invented here. The implemented
cubic step uses the invertible cube map for `p=2 mod3`. The quadratic step
specializes the two-layer square-coefficient construction of
[Ivanyos and Santha, Proposition 9](https://arxiv.org/pdf/1503.09016)
to `p=3 mod4`; the final step is ordinary linear dependence. Only public
linear algebra, modular roots and a constant-expected-trial conic search
are used. The potential extension to other primes would use their general
SDE machinery and is not implemented.

### A Polynomial Copy Bound

Put `m=2r`, `n=4r`. At degree `d`, the rank of the public coefficient
columns is at most

```
R_d = n * binom(m+3-d, 3-d).
```

Reason: every packet remains a sum of expressions
`lambda_i.Q(a_i+b_i*x)`. A coefficient at degree `d` depends only on the
translation moments `sum_i lambda_i*b_i^d*a_i^gamma`,
`|gamma|<=3-d`. Dropping constants or cancelling higher degrees does not
alter this representation of the remaining coefficients.

Thus one conservative fixed schedule uses

```
B3 = n+1
B2 = (n*(m+1)+1)^2
B1 = n*binom(m+2,2)+1
S  = B3*B2*B1 = O(r^8)
```

original cosets per phase-free quotient state. No IID assumption is made
about the later public coefficients. The SDE bounds work for EVERY batch.
The symbolic arrays have polynomial size and the transformations are
polynomial-size arithmetic circuits in `r,log p`. The local FLINT backend
uses machine-word primes; the written algebraic bound is not tied to that
implementation limit. Sparse amplitude enumeration costs at least `p`
per line and is NOT the proposed quantum implementation.

`O(m+log(1/epsilon))` phase-free copies suffice for ordinary Fourier
learning of `L=span(v)`, with failure at most `epsilon` after a suitable
constant additive margin. An explicit bound for `k` samples is
`Pr[not spanning L^perp] <= (p^(m-1)-1)*p^(-k)`.
A finite gate compilation can approximate uniform states and QFTs with
total error bounded by the sum of complete-instrument errors. Since no
branch is postselected, there is no division by a rare-outcome probability.

## Completion Using Known HPGP

Learning the line is not learning `H`. There is, however, a copies-only
completion, without demanding an oracle restricted to an unknown subgroup.

Choose any now-KNOWN nonzero representative `v` of the line and a KNOWN
`ell` satisfying `ell(v)=1`. On a fresh original coset:

1. In the public semidirect chart, measure `q_perp=q-ell(q)v`.
2. Retain `tau=ell(q)`.
3. Apply the public linear map `Phi(-q_perp)` to the normal coordinates.

The resulting state is

```
p^(-1/2) sum_tau |tau>|u+g_v(tau)>,
```

where `g_v` is the single fixed degree-at-most-three normal orbit of the
generator normalized to project to `v`. The offset `u` is uniform and
unknown. This matches univariate vector-output HPGP-prime.
[Ivanyos and Santha, Theorem 5, Corollary 6 and Section 4.1](https://arxiv.org/pdf/1503.09016)
provide the relevant known polynomial-time solver. Its answer at `tau=1`
reconstructs a generator. The relabeling is tested here; that full solver
and its gate implementation are NOT executed.

The case `H<=N` also needs no restricted oracle. On fresh original cosets,
measure `q` and apply `Phi(-q)` to `n`. The result is a coset of `H intersect N`
in the explicit abelian `N`. For cyclic `H`, this either recovers all of `H`
or finds a trivial intersection, after which the nonzero quotient case
applies. The public chart conversion is tested in both cases. The final
abelian learning and HPGP routines remain written compositions, not a
fully executed HSP receiver. Arbitrary higher-dimensional `H` is outside
the claimed derivation.

## Attempted Falsification

- **Hidden direction advice:** the controller receives only phase maps,
  public labels, and measurement outcomes. The proof's `ell` and actual
  potential coefficients occur only in separately named fixture functions.
- **Different unknown phases per coset:** checked against a single global
  cubic potential, including nonzero logarithmic grade-two coordinates.
- **Support collapse:** exhaustive direct permutation simulation checks all
  branches of two parallel-line inputs. Nonparallel inputs give a point,
  demonstrating why the shared-support premise is essential.
- **Rare outcomes:** exact branch probabilities sum to one; a fresh ambient
  vector is charged. Random-source tests do not select labels or outcomes.
- **False classical advantage:** dephased input control gives uniform Fourier
  output, not annihilator samples. This establishes need for coherence in
  this mechanism. A separate opaque-label query bound is given below.
- **Phase only apparently constant:** exact symbolic leading coefficients
  vanish at every stage; direct complex amplitudes independently agree at
  the end, and Fourier mass outside the true annihilator is checked.
- **Easy rank-one or secret-aligned instance:** the executed logarithm is
  `(1,2,3,4,5,6)` at `p=23`; both grade-two terms are nonzero. Shared-parameter
  rank-two tests check the cocycle and copies-only graph relabeling.

### The Strongest Classical Statement Established Here

For `p>3`, every nonidentity element of `UT4(Fp)^r` has order `p`.
There are

```
M = (p^(6r)-p^(4r))/(p-1)
```

cyclic subgroups whose quotient image in `A` is nonzero. Choose one
uniformly, and assign independent random opaque names to its cosets.
Each distinct query pair tests at most ONE of these subgroups, because
its nonidentity quotient `g^(-1)g'` generates a unique order-`p` subgroup.

Couple an adaptive classical algorithm to an injective random-name oracle
up to the first collision. The first `T` queries on that transcript can
encounter at most `binom(T,2)` hidden subgroups that would cause a collision.
If no collision occurs, any final guess adds at most one subgroup. Thus

```
Pr[correct H] <= min(1, (binom(T,2)+1)/M).
```

This holds for randomized algorithms after conditioning on their coins.
Constant success requires `Omega(sqrt(M))` classical queries in THIS
opaque-oracle distribution, irrespective of classical computation time.
It does not apply when an explicit evaluator exposes useful additional
structure through its outputs. This is the familiar type of oracle-HSP
separation, not a computational problem reduction.

The small executed `p=23,r=1` example consumes more source states than
the square-root subgroup-count scale. It demonstrates neither a practical
runtime advantage nor an experimental asymptotic separation. Its role is
to attack the algebra and physical state interface.
The fixed small-prime HSP was already tractable by known methods. What
requires review is the uniform growing-prime, growing-rank construction.

## What Remains Unproved Or Unestablished

Independent review of the full mathematical composition and its novelty
is the priority. The nearby 2016 theorem explicitly treats a cyclic quotient;
absence of a matching search result does NOT establish that this extension
is new. The 2023
[zero-sum conversion paper](https://arxiv.org/abs/2304.08376)
is relevant context, not evidence that every large-prime special case was open.

There is no reduction here from lattice problems, code equivalence, graph
isomorphism, or a cryptographic target. A polynomial oracle HSP algorithm,
even if the derivation survives and is new, is not automatically Shor-level.
Do not add more small-prime sweeps or promote a registry claim before
auditing the proof, source-state interface and prior art.

Files: `theorems/affine_phase_erasure.py`,
`theorems/ut4_affine_phase_receiver.py`,
`tests/test_affine_phase_erasure.py`.
Reproduce: `python -m theorems.ut4_affine_phase_receiver --write`.

## Executed Control

The fixed `p=23,r=1,seed=20261021` run consumes 21,125 original random
cosets, performs 4,225 cubic, 25 quadratic and one linear merge, and
retains a complete 23-point quotient line. Public equation ranks are
4,12,24. There are ZERO zero Fourier labels and ZERO single-active-input
merges. No failed outcome, label, or seed was discarded.
Final relative phase error is `8.21e-14`; Fourier mass outside the true
annihilator is `1.64e-27`.

The preliminary `p=11` control also passed, but its field is small enough
that an incidental zero character could make the mechanism test weaker.
The stronger live control records that confound explicitly. Changing the
field here is a falsifier against an easy-sector shortcut, not a scaling
campaign or evidence of asymptotic speedup.
