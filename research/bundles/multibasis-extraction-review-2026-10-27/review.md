# Multibasis extraction: independent mathematical review

Date: 2026-10-27. Fixed prime p=1019. All asymptotics let e grow.

## Verdict

**No polynomial extractor for every promised input was obtained.** This is a
bounded constructive audit, not a hardness result or an exhaustive literature
claim. The original task remains: given explicit B and arbitrary s, find
z in (F_p^*)^m with Bz=s. No supplied witness, geometric oracle, or uniform
sampling oracle is substituted for that task.

The substantive conclusions are:

1. The numerical promises alone give **three** disjoint column bases in
   O(k^2 m) field operations. They do not force four: explicit p=1019
   counterexamples with the exact parameters are given below.
2. Complete native AG codes of degree 2g+1 have stronger structure:
   **four disjoint bases are guaranteed**, by Riemann-Roch/Clifford and matroid
   base packing. Four is optimal by cardinality. Finding the bases is
   polynomial; extracting nonzero coefficients from them is still unresolved
   here. The three-basis additive theorem inspected does not close that gap.
3. There are precise obstructions to fixed tiny alphabets, exhaustive additive
   state tables, bounded-bucket reparameterized greedy, arbitrary pinning,
   formal-polynomial PIT on field slices, and replacing group-ring
   irredundancy by ordinary linear circuits. These obstruct particular
   arguments, not all classical algorithms.
4. The parent's **special-divisor fiber repair is valid**. On the stored actual
   e=8 matrix, I independently verified all eleven rank-15 fiber restrictions
   and all eleven full-support alternating kernel identities. The geometric
   argument gives search for any syndrome when 2e<p and the fiber certificate
   is available. This includes dyadic e<=256, not an unbounded fixed-p family.
5. The parent's **prime-source short-kernel bound and pair-overlap bound are
   correct with the distribution qualifications below**. They explain why the
   convenient G=11I-E control is not representative of prime-sampled classes.
   The stationary-walk result and explicit isolated-vertex example also pass
   algebraic review. None is a first-hitting lower bound for adaptive repair.

All new files are confined to this directory. The supplied four notes were
read, and the relevant primary papers were checked. No repository, Git, UI,
storage configuration, or parent artifact was changed. No subagent facility
was available; this review did not claim an independent second reviewer.

## 1. Scope and cost model

The numerical input promises are

    rank B = k = 5e+3, m = 22e, d_min(row B) >= delta = 12e-3,
    e dyadic, e >= 8, p = 1019.

Field operations cost O(1) because p is fixed; dense input has Theta(e^2)
entries. An original-relation verification costs O(km). Constants depending
only on p, including large polynomial exponents depending on p, are allowed.
Costs such as p^k or (p-1)^k are not polynomial in this input length.

The extra native hypothesis, used only where identified, is

    row B is monomially equivalent to C_L(D,G),
    genus g=5e+1, deg G=2g+1=10e+3, deg D=m,
    D consists of distinct rational evaluation points disjoint from G,
    and the entire L(G), not an arbitrary subspace, is evaluated.

The generic counterexamples below need not be native codes. Conversely,
the native four-basis proof must not be inferred from distance alone.
All witness constructions discussed are search algorithms, not uniform
samplers. A distribution claim needs a separate proof.

## 2. What multiple bases actually give

### 2.1 Three bases for every promised matrix

Deleting any set of fewer than delta columns preserves row rank. Otherwise
a nonzero row combination vanishes on the surviving columns and is supported
on fewer than delta positions. Select one basis, delete it, select another,
delete it, and select a third. This succeeds because

    delta - 2k = 2e-9 > 0.

Three Gaussian-elimination passes cost O(k^2 m). This algorithm does not need
to compute or certify minimum distance; it can directly verify the selected
bases. A false input promise is not silently turned into a certificate.

No matrix here can have five disjoint bases: 5k=25e+15>22e=m.

### 2.2 Exact counterexample: the numerical promises need not give four

For e in {8,16,32}, put n=17e-2, so n<=1019. Take the k by m matrix whose
first n columns are

    v(a)=(1,a,a^2,...,a^(k-1))^T,  a=0,...,n-1,

and whose remaining 5e+2 columns are copies of (0,...,0,1)^T.

Any k finite evaluation columns form a Vandermonde basis. There are three
disjoint such bases since n>=3k. For a nonzero polynomial f of degree <=k-1:

- If its coefficient of X^(k-1) is zero, its word has at least
  n-(k-2)=12e-3 nonzero finite coordinates.
- If its coefficient of X^(k-1) is nonzero, all 5e+2 repeated coordinates
  are nonzero, in addition to at least n-(k-1) finite coordinates.

The distance is exactly delta: use f(X)=product_(a=0)^(k-3)(X-a), of degree
k-2, with its X^(k-1) coefficient zero.

Every column basis contains at most one of the repeated columns, hence needs
at least k-1 finite columns. Four disjoint bases would require

    4(k-1)=20e+8 <= n=17e-2,

which is false. At e=8 this is an exact [176,43,93] rowspace with precisely
three disjoint bases. The code verifies the three ranks and the
distance-attaining word; the root argument proves the distance lower bound.
It does not enumerate all 1019^43 words.

These fixtures disprove a universal four-packing implication from the
numerical promises. They are not unbounded RS families over a fixed field,
and are not the prescribed complete native AG family.

### 2.3 Native strengthening: four bases always exist

Let X be any subset of the evaluation positions, and put

    h = deg(G-D_X) = d-|X|,
    l = ell(G-D_X) = k-rank(B_X).

The second equality uses completeness and injectivity of evaluation, since
d<m. If l=0 there is no packing constraint. Otherwise h>=0.

For 0<=h<=2g-2, Clifford gives l<=h/2+1. This also holds in the nonspecial
case, by Riemann-Roch. In particular l<=g, and

    |D\X| = m-d+h >= delta+2l-2 >= 4l,

because delta-2-2g=2e-7>0. For h>=2g-1, Riemann-Roch gives l=h+1-g, so

    |D\X|-4l = m-d+4g-4-3h
              >= m-4(d+1-g) = m-4k = 2e-12 >= 4.

Thus |D\X|>=4(k-rank(B_X)) for every X. The matroid base-packing criterion
gives four disjoint bases. Column rescaling and permutation preserve the
argument. This applies to arbitrary admissible divisor classes, not only
G=11I-E or prime-sampled G.

The finite-field gonality/Clifford bounds are explicitly recorded in
[Munuera-Torres, Lemma 2.5](https://arxiv.org/pdf/math/0303104).
For packing and its constructive matroid machinery, the primary sources are
[Edmonds, Minimum Partition of a Matroid into Independent Subsets](https://nvlpubs.nist.gov/nistpubs/jres/69B/jresv69Bn1-2p67_A1b.pdf)
and its sequel
[Lehman's Switching Game and a Theorem of Tutte and Nash-Williams](https://nvlpubs.nist.gov/nistpubs/jres/69B/jresv69Bn1-2p73_A1b.pdf).

Use matroid union with four copies of the column matroid, with rank tests by
elimination. An augmenting-path implementation uses polynomially many such
tests; a conservative implementation that rebuilds the exchange graph at
each augmentation takes O(m^3) independence tests for fixed four, each at
most O(k^3) by fresh elimination. This deliberately loose O(m^3 k^3) bound
already suffices. Greedily deleting arbitrary bases is not the general proof
of the fourth basis.

On the stored e=8 native matrix, repeated greedy selection happened to find
four bases, each of rank 43, leaving four columns. The indices and input hash
are in countercontrols.json. This is a finite certificate of packing, not a
coefficient extractor or a substitute for the argument above.

## 3. Additive-basis theorem: exact remaining extraction operations

[Nagy-Pach-Tomon, Theorem 1.1(ii)](https://arxiv.org/html/2111.13658#S1.SS1)
gives nonzero-coefficient representations of every target from any three
bases when p>=11. Thus it applies directly after fixing unused coordinates
to 1. I checked Theorem 3.1 and Lemmas 2.4-2.5, not a broad AJT survey.

Their proof selects a subset minimal for vanishing of
product_v(1-g^v)^r in F_p[F_p^k], takes a quotient, and uses a nonzero
coefficient and two bounded-coefficient representations to improve a
representation. Here r=(p-3)/2=508. The inspected proof gives no polynomial
algorithm for those selections and representations. A literal group-ring
table has p^k entries. Ordinary rank tests do not implement these operations.
This is an accounting gap in that route, not a lower bound on all algorithms.

A concrete distinction: three parallel copies of v form a minimal vanishing
set for r=508, because (1-g^v)^1524=0 but (1-g^v)^1016!=0. An ordinary
linear circuit already consists of two copies. Extracting a linear circuit
therefore does not supply the needed irredundant group-ring set. The exact
mod-1019 coefficient counts are 0 and 1017, respectively.

Four bases provide additional redundancy, but I found no operation-by-operation
polynomial extraction using it. An algorithm for three or four arbitrary
bases would be sufficient, though the native four-basis matrices might admit
an algorithm not available for arbitrary ones.

## 4. Precise obstructions to proposed shortcuts

### 4.1 Fixed small alphabets cannot cover arbitrary syndromes

Even allowing a different prescribed alphabet A_j at each coordinate, if
|A_j|<=4, the image under B contains at most 4^m syndromes. But

    4^(22e) < 1019^(5e) < 1019^(5e+3).

Thus every B has some syndrome missed by that restriction. This includes
binary subset sums, signs, and every four-letter fixed alphabet. For b
binary-selected basis blocks, the simpler necessary condition is 2^b>=p;
at p=1019 at least ten blocks are necessary just by cardinality, whereas
at most four disjoint column bases fit here. This is not an objection to
target-dependent alphabets or larger alphabets with a proved extractor.

### 4.2 High distance does not make additive state tables small

For any ordering, both halves of the columns have rank k. Indeed, deleting
11e columns cannot reduce rank because 11e<delta for e>=8. In either half,
fix all columns outside one basis to coefficient 1 and vary the k basis
coefficients over F_p^*. These already give (p-1)^k distinct partial sums.

Consequently, a DP explicitly listing all attainable nonzero-coefficient
partial syndromes has an exponential middle layer in every order. With
unrestricted coefficients it has all p^k syndromes there. This only rules
out that literal state-table representation, not compressed algorithms or
target-directed procedures. The related linear-code trellis phenomenon is
also stated in [Munuera-Torres, Proposition 2.3](https://arxiv.org/pdf/math/0303104).

### 4.3 Bounded-bucket greedy is not rescued by an arbitrary kernel basis

Write an affine parameterization z=a+Nt, where the columns of N form a basis
of ker B. In the last variable, exactly wt(N_last) coordinate forms have
their last nonzero coefficient. A guarantee of fewer than p forbidden roots
at every stage therefore requires some nonzero kernel vector of weight <p.

The numerical promises do not imply that. Let B be iid uniform k by m over
F_p. A union bound for a nonzero row combination of weight below delta is

    Pr(row-distance failure) < 2^m p^(k+delta-1-m)
                            = 2^(22e) / p^(5e+1).

This event includes rank deficiency. A union bound for a nonzero kernel
word of weight <=p-1 is at most

    p^(-k) sum_(j=1)^(p-1) binom(m,j)(p-1)^j
    <= (p-1)[m(p-1)]^(p-1) / p^k.

Their sum is less than 1 at e=512, checked using exact integers/fractions.
The logarithms base two of these two upper bounds are approximately
-14327.9 and -1728.8. Both go to zero as e grows. Hence there exist promised
generic matrices with d_min(ker B)>=1019. For all their kernel bases and
orders, the simple last-bucket size guarantee fails. No particular such
large matrix was generated, and this does not prove that every greedy run
fails: forbidden roots can coincide. The point is the absence of a
universal small-bucket proof from the promises.

The parent's prime-source result in Section 7 gives the analogous,
source-specific obstruction once 2e+1>=p, with high probability rather than
for every native class.

### 4.4 Pinning can destroy feasibility even when rank survives

For any promised B, pick a basis I, put R=I^c, set s=B_R*1, and pin z_R=1.
The unique remaining solution is z_I=0. The full original problem has
full-support solutions, but this nonzero partial assignment has none.

This is a same-relation obstruction, valid also for native inputs. The
e=8 generic fixture has the bad prefix and a separately checked global
full-support witness in the receipt. A rank-preserving deletion is not a
full-support feasibility oracle. Retaining two bases avoids this particular
dead end but returns to unresolved affine avoidance.

### 4.5 Formal PIT and extension-field evaluation are not extraction

The warning X^p-X is relevant inside the promised family, not just to an
unrelated polynomial. For e>=128, delta>p. Choose a full-support homogeneous
kernel word w, whose existence follows from the supplied all-syndrome count.
On p positions prescribe a_j=-t_j w_j for all t_j in F_p. Deleting these p
positions leaves B full rank, so the remaining a_j can be chosen by linear
algebra to satisfy Ba=s, for any s.

The entire line a+Tw stays in the affine fiber. Each T in F_p kills at least
one coordinate, although product_j(a_j+T w_j) is a nonzero formal polynomial
with leading coefficient product_j w_j. Its first p factors include a
nonzero scalar multiple of T^p-T. There is no full-support point on this line.

This is an existence countercontrol for bad restrictions, not an efficient
construction of w from nothing. The coefficient identity T^1019-T is checked
exactly. Formal PIT, or finding a good T over an extension, does not give a
base-field point. The latest inspected
[Jafari preprint, v2, Theorems 1.1 and 3.1](https://arxiv.org/html/2608.23647)
requires sufficient extension degree for its multimap statements; p=1019
has extension degree one. I did not use it as a prime-field extractor.

## 5. A distinct diagonal-quadratic reformulation, not an extractor

Because 1019=3 mod 4, x^2+1 is never zero in F_1019. It is enough to solve

    B (x_1^2,...,x_m^2)^T = s-B*1,

then put z_j=x_j^2+1. This restricted relation is total under the distance
promise. For a nontrivial additive character psi and c!=0,

    |sum_x psi(c x^2)| = sqrt(p).

One can check this directly by squaring the magnitude and substituting
(x-y,x+y), an invertible change because p is odd. Orthogonality then gives
the solution count

    p^(m-k)(1+R),  |R| <= (p^k-1)p^(-delta/2)
                           < p^(4.5-e) < 1.

This holds for every syndrome and every promised matrix, without geometry.
It is a stronger restricted-existence statement, but does not solve the
diagonal system. Uniform x has equation-hit probability about p^(-k).

[Ivanyos-Santha, Proposition 9](https://arxiv.org/pdf/1503.09016)
provides an algorithm for a nontrivial homogeneous diagonal quadratic zero
with (k+1)^2 variables. Here there are only 22e=O(k) variables. Also,
homogenizing the displayed inhomogeneous system does not ensure a solution
with nonzero homogenizing coordinate. Neither requirement can be omitted.
This was a focused near-match check, not a general polynomial-systems audit.

Padding by splitting one x_j^2 into many squares is invalid: 1+x^2+y^2 can
vanish. For example 1+1^2+778^2=0 mod 1019, checked exactly. Independent
copies of a column can change the allowed original coordinate. The two
small diagonal controls verify the character-count consequence only; they
are not evidence for efficient unbounded extraction.

## 6. Parent finite-control falsifier: special-divisor fiber repair

**Verdict: accepted, including its limitation to the special divisor family.**

For the parent's unramified degree-e cover of the genus-six base, let I be
the pullback of infinity. Then deg I=e, div(dx/y)=10I, and
div(x-a)=F_a-2I at an unramified split x-fiber. If G=11I-E with
E effective of degree e-3 and disjoint from D, the differential

    eta_a = (dx/y)/(x-a)

has divisor 12I-F_a. Therefore

    div(eta_a) - (G-F_a) = I+E >= 0.

For f in L(G), f eta_a has no poles except possible simple poles at F_a.
Its residues there are f(P)/y(P). The global residue theorem gives

    sum_(P in F_a) f(P)/y(P)=0.

Thus v_a, with entries 1/y(P) on F_a and zero elsewhere, is a kernel word
nonzero at every position of F_a. The local parameter is x-a; unramifiedness
and y(P)!=0 are essential. This is the ordinary curve residue/duality
mechanism, also explicitly recalled in
[Grant-Massman-Srimathy, Introduction, equations (1.2)-(1.3)](https://arxiv.org/html/2009.09311).
If B has evaluation-column multipliers lambda_P, replace v_a(P) by
v_a(P)/lambda_P. Row operations do not change the kernel.

Given any particular z0 with Bz0=s, independently select for each fiber

    c_a not in {-z0(P)/v_a(P): P in F_a}.

At most 2e values are forbidden. If 2e<p, a scalar exists, and
z=z0+sum_a c_a v_a is full support with the original syndrome. Disjoint
supports make this a deterministic repair algorithm, not a mixing argument.
Computing z0 costs O(k^2 m); with the certificate already obtained, forming
forbidden sets and the repair costs O(m+11p), followed by O(km) verification.
Local nullspace computation can obtain/verify a proposed block certificate
from B by polynomial elimination. Geometry need not be trusted for checking it.

For fixed p=1019, the condition is e<=509, hence dyadic e<=256. This improves
the guaranteed dyadic scope of the elementary two-basis dimension cutoff
(e<=128), but is not an asymptotic dequantization at fixed p. A full Schur
cube does not invalidate this solver. An e=256 claim still requires an
actual appropriate complete matrix; none was constructed here.

I independently checked the stored actual e=8 B, not merely the geometric
description: each consecutive 16-column fiber has rank 15, and the vector
(-1,1,...,-1,1) on that fiber, zero elsewhere, is in ker B. The local
nullity is consequently exactly one. No parent repair implementation or
test suite was duplicated.

Access qualification: for an arbitrarily permuted explicit B, a source
description or fiber partition is not automatically part of the native
input. A certificate is cheaply checkable, but a general polynomial
partition-recovery algorithm was not established here. The actual stored
ordering exposes its eleven blocks directly. Do not hide geometric
reconstruction behind a free oracle.

Most importantly, effectiveness of 11I-G is special. It is not a property
of arbitrary or typical prime-sampled G. Even uniformly over classes its
probability is at most A_(e-3)/h, and the same CCX estimate used below bounds
this by g/[p^(4e+3)*30^2]. Prime sampling and cube conditioning require their
transfer factors. Convenient inputs of this form cannot establish behavior
for the intended generic source, even when their complete Schur cube is full.

## 7. Parent prime-source short-kernel deduction

**Verdict: the deduction is correct, subject to the exact sampling law.**

Fix the actual curve and D and put t=2e. For a t-element subset T of D,
Riemann-Roch gives

    rank(ev_T L(G)) = ell(G)-ell(G-T)
                     = t-ell(K-G+T),

since deg(K-G)=-3 and ell(K-G)=0. A nonzero kernel word supported on at
most t positions can be padded to such a T, so the rank is below t.
Conversely that rank defect gives a nonzero word supported in T. Completeness
of L(G) matters. Coordinate multipliers preserve the rank condition.

For fixed T, the class map [G] -> [K+T-G] is a bijection from Pic^d to
Pic^(t-3); its linear part is inversion, not multiplication by 2 or 3.
There is **no torsion factor**. Classes with ell(K-G+T)>0 number at most
A_(t-3), because each has at least one effective representative. Union over
the binom(m,t) possible subsets gives the proposed bound for uniform classes.

Here r=t-3=2e-3 lies in [0,g-1], and g-r-1=g-t+2=3e+3.
[Cascudo-Cramer-Xing, Proposition 3.4](https://arxiv.org/html/1207.2936#S3)
states A_r/h<=g/[p^(g-r-1)(sqrt(p)-1)^2] in this range. Replacing sqrt(p)-1
by L=30 weakens the denominator correctly. Consequently

    epsilon_class <= binom(22e,2e) g / [p^(3e+3)*30^2].

### Transfer to closed primes

This is not uniform-Picard sampling. Every degree-d class has exactly
(p^(d+1-g)-1)/(p-1) effective representatives, and hence no more degree-d
prime representatives. With N_d>=p^d/(2d) and h<=U^(2g), U=33,

    max_class Pr([G]=class) <= (1/h) C,
    C = 2dp/(p-1) * (U^2/p)^g.

The source's sufficient prime-count condition
p^d>=4(g+1)^2(d+6)^2 supplies that lower bound on N_d. A degree-d prime is
automatically disjoint from rational D because d>1. Therefore

    epsilon_prime <= C * epsilon_class.

For completeness, the prime-count premise follows by Mobius inversion of
the extension-field point counts: the proper-divisor contributions and the
Weil error together are bounded by (g+1)(d+6)p^(d/2). The stated condition
makes this at most p^d/2. Thus no class-number lower bound or unproved
equidistribution of prime classes is hidden in this step.

These statements concern exact uniform sampling of degree-d CLOSED primes
on a fixed curve. A biased construction of effective divisors, arbitrary
admissible classes, a handpicked divisor, or an unverified prime-generation
law does not inherit the estimate. No conjectural class equidistribution is
needed; the maximum-class-mass argument is enough.

### Conditioning and asymptotics

Let F be full Schur cube. If epsilon_cube bounds Pr_prime(F^c) under that
same prime law, then

    Pr_prime(d_min(ker B)<=2e | F)
       <= min(1, C*epsilon_class/(1-epsilon_cube)).

No independence assumption is needed. The existing parameter_bounds uses a
bad-PRIME bound, so that quantity is the applicable epsilon_cube, not its
smaller uniform-class precursor. Additional source acceptance conditions
need their own acceptance-probability denominator or a fresh proof.

Even the crude binom(22e,2e)<=2^(22e) gives an upper bound equal to a
constant times dg times

    [ (2^22/p^3) * (33^2/p)^5 ]^e,

whose bracket is below 0.006. Thus the bad probability tends to zero
exponentially; the cube-conditioning denominator tends to one under the
supplied cube bound. The parent is performing the sharper exact parameter
checks. This review did not duplicate them.

The conclusion is typical-source minimum kernel weight >2e, not a
deterministic statement for every divisor class. The special e=8 fiber
word of weight 16 is entirely consistent: that control is not prime-sampled.

## 8. Parent pair-overlap and fixed-bank isolation

**Verdict: accepted; quantify over a bank fixed before drawing the state.**

Fix nonzero v in ker B and nonzero c in F_p, and let w=wt(v). The simultaneous
conditions z,z+cv full support restrict coordinate j to

    A_j=F_p\{0,-cv_j} if v_j!=0, and A_j=F_p\{0} otherwise.

For a nontrivial character at a nonzero frequency, the normalized coordinate
sum has magnitude at most 2/(p-2) in the first case and 1/(p-1) in the
second. Every nonzero uB has at least delta nonzero positions. Character
orthogonality therefore gives

    N_pair <= p^(-k)(p-2)^w(p-1)^(m-w)(1+eta),
    eta=(p^k-1)[2/(p-2)]^delta.

The supplied denominator count is
|S| >= p^(-k)(p-1)^m(1-alpha), with alpha<1. Taking their ratio proves

    Pr_(z uniform S)(z+cv in S)
       <= [(p-2)/(p-1)]^w * (1+eta)/(1-alpha).

All syndromes are allowed. The expression can exceed one at small
parameters; use min(1, RHS) when reporting a probability. At the fixed prime,
both alpha and eta go to zero exponentially. For example
4p<(p-2)^2 implies eta<p^(k-delta/2)=p^(4.5-e).

For a bank D_B,s of L(e) nonzero directions, selected from B and s but not
from the random z, if every direction has weight >=2e+1, then

    Pr_(z uniform S)(some distinct valid bank-line neighbor)
      <= L(e)(p-1) [(p-2)/(p-1)]^(2e+1) (1+eta)/(1-alpha).

If L is polynomial in e, this tends to zero. Conditioning on the good
prime-source event of Section 7 justifies its weight hypothesis. The
combined failure probability is at most the source failure bound plus the
displayed fixed-bank bound. This does not say the bound is numerically
useful at the currently available e values.

The isolated-vertex statement is about the induced chain ON valid states,
with scalar moves in a fixed polynomial-size bank. Directions chosen in
response to z, exponentially large banks, intermediate invalid states,
and solving for an appropriate long move are not excluded. In particular,
this is not a first-witness lower bound for state-adaptive repair.

## 9. Parent stationary-walk side check

Assume X_0 is uniform on Omega={z:Bz=s}, and each transition kernel is a
state-independent mixture of translations by kernel vectors. Time-dependent
fixed schedules also qualify. Uniform measure on Omega is preserved, even
if the walk is reducible. Fixed directions alone are not enough if step
probabilities depend on the current state.

Set pi=|S|/|Omega| and H=min{t>=0:X_t in S}, including time zero. Marginal
stationarity and a union bound, without independence, give

    Pr(H<=T) <= min(1,(T+1)pi),
    E H = sum_(t>=0) Pr(H>t)
        >= sum_(j>=1) max(0,1-j*pi).

For 0<pi<=1, put a=1/pi, n=floor(a), r=a-n. The last sum is

    n-pi*n(n+1)/2
      = (1-pi)/(2pi) + r(1-r)/(2a)
      >= (1-pi)/(2pi).

For pi=0, H is infinite; for pi=1, H=0. The supplied character formula
pi=(1-1/p)^m(1+R_s), |R_s|<=alpha, is consistent with this convention.
The result is for an unfocused stationary walk, not an algorithm initialized
from a designed, nonuniform state or using adaptive transitions.

The parent's separate basis-line example also passes algebraic inspection.
For m=2(p-1)+1, B all ones, v=(1,...,p-1,1,...,p-1,0), and
d_j=v+e_j-e_m, all directions lie in ker B. Their coordinate matrix in the
usual kernel basis is I+v*1^T, with determinant 1+sum v=1. For each j and
nonzero scalar c, an unmodified copy of -1/c remains among the first m-1
entries, so the all-ones state moves to a vector with a zero coordinate.
There are ((p-1)^m+1)/p>1 full-support solutions at syndrome -1. Thus this
valid state is isolated despite maximal rowspace distance m. It is an
arithmetic, non-AG counterexample to arbitrary-basis mixing, not hardness.
No duplicate implementation was made here.

## 10. Exact controls and resulting status

Executed successfully:

    python3 -B /Users/jaspersands/Developer/qsearch-research-work/multibasis-extraction-review-2026-10-27/checks.py --write
    python3 -B /Users/jaspersands/Developer/qsearch-research-work/multibasis-extraction-review-2026-10-27/checks.py --check

An initial replay comparison exposed tuple/list JSON normalization in the
square-padding control. It was corrected; both commands then passed. The
mathematical assertions passed before and after that serialization fix.

The companion checks.py and countercontrols.json contain:

- Three reconstructible p=1019 RS-plus-parallel fixtures, at e=8,16,32,
  with three basis certificates, four-basis obstructions, and exact
  distance-attaining words.
- A nonextendible nonzero partial assignment with a separately verified
  full-support global witness on the e=8 generic fixture.
- Four basis certificates and both half-rank checks for the actual stored
  e=8 native matrix; its source file is hashed in the receipt.
- Independent checks of all eleven actual rank-15 fiber restrictions and
  alternating kernel vectors, without implementing the parent's repair code.
- Exact group-ring, T^p-T, four-letter cardinality, shifted-square, and
  invalid square-padding controls; an exact probabilistic-existence
  certificate for the generic no-short-kernel example at e=512.
- Complete small diagonal-system syndrome counts at p=3 and p=7. These
  are algebraic controls, not native inputs or scaling evidence.

**Recommended mathematical status:** four native bases are a proved
structural strengthening; an unbounded polynomial coefficient extractor is
not established. Special-divisor block repair is a genuine stronger search
baseline on its certified inputs and bounded fixed-p range. The generic
prime-source and fixed-bank isolation bounds are compatible with that
baseline and prevent transferring its behavior to a different source law.
They do not establish a classical lower bound, uniform sampling, a quantum
advantage, or an implemented higher tower.
