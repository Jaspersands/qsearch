# Stabilizer extent: source scope and failed in-span reconditioning

2026-11-07. Selection review, starting with STATE/TRAPS. Corpus been-tried
and baselines were queried with `--no-refresh`, including the specific
internal Pauli-projection/basis-exchange operation. The retrieved nearby
records did not settle it; the baseline catalog had no matching entry.
Read the actual primary texts below. No network/API, Git, new code or
finite experiment was used in this review.

**Selection:** no new polynomial-rank learner is admitted. The proposed
in-span basis/dictionary reconditioning lemma is false, by the quantified
family independently verified below. This does not falsify polynomial
optimized extent, projections allowed to leave the original span, or a
general polynomial-rank learning algorithm.

## Actual published scope

* `stabilizer_rank_priority/extent.txt`, 2610.06819v1, defines
  `Lambda_S=min sum |c_i|` and SQUARED extent `xi=Lambda_S^2`.
  Theorem 1.1/Corollary 3.6 give
  `xi(v)<=2^{O(sqrt(k log(k+1)))} ||v||^2` when `chi(v)<=k`.
  The finite Theorem 3.5 bound is
  `(2k)^(4r) (2^(floor(k/r)+1)-1) ||v||^2`, with the additional
  `2^k-1` bound. These optimize over NEW stabilizer decompositions.
* The same source's Theorem 8.2 gives copy-only pure-state tomography in
  `poly(n,1/epsilon,log(1/eta))*2^{O(sqrt(k log(2k)))}`. The frame and
  coefficients are unknown; the output is a stabilizer combination, not
  necessarily of rank k. This is polynomial for
  `k=O(log^2 n/log log n)`, not for unrestricted polynomial k.
* `stabilizer_rank_priority/low_rank.txt`, 2610.03658v1, instead calls the
  UNSQUARED coefficient norm xi (Definition (3)). Its bound is `2^{O(k)}`
  and its learner has `poly(n,2^k,1/epsilon,log(1/eta))` cost. The notation
  must not be substituted into the squared convention without adjustment.
* `stabilizer_extent/marton.txt`, 2609.20771v1, also uses UNSQUARED xi in
  Eq. (79). Theorem 8.10/Corollary 8.11 give polynomial bounded-extent
  tomography without the earlier algorithmic-PFR assumption. Consequently
  a proved polynomial optimized-extent bound would already pay the
  native copies-only endpoint; a supplied stabilizer frame is unnecessary.

The strongest bound in these opened sources is the square-root exponent.
Its proof ALREADY uses code merging and averaged Pauli projections:
Lemmas 3.2--3.4 have code dimension `(2k)^O(r)` and the recurrence
`B(t)<=D+2B(t-r)`. Optimizing the competing costs
`O(r log k)` and `O(k/r)` gives `O(sqrt(k log k))`. Removing only the
merging logarithm would give a square-root exponent, still not polynomial
extent. Simply proposing Pauli block elimination repeats the published
operation. The projections in that proof need not remain in the original
span; this freedom is essential to distinguish from the falsified route.

For fixed supplied-frame conditioning, actual Kalra--Sinha2503.04101v3
(`stabilizer_extent/barnes_wall.txt`, Theorem 31) bounds coefficients by
`sqrt(e)*(2k)^(k+1/2)` in any linearly independent supplied stabilizer
frame. Mehraban--Tahmasbi2410.24202v2 (`mehraban_tahmasbi.txt`, Lemma 4.1)
proves a positive lower bound on the smallest nonsingular Gram eigenvalue
for each FIXED k, independent of n, by compactness. Neither opened text
contains the alleged exponential-conditioning extremal construction in
the relevant proof sections. It would be incorrect to attribute the
following family to either source, or to infer an optimized-extent lower
bound from a supplied-frame lower bound. Priority is not established here.

## All-dimensional falsifier to every in-span positive frame

For every n>=2, let `E={0,e_1,...,e_n}` in F_2^n. For 1<=i<j<=n let
C_ij consist of strings whose first two 1s are at i,j. Thus coordinates
before j are zero except at i, coordinate j is one, and all coordinates
after j are free. The C_ij are disjoint affine spaces of dimension n-j
and partition the complement of E. Define normalized stabilizers

    s0=|+>^n,  b_ij=uniform state on C_ij,
    V=span{s0,b_ij},  K=binom(n,2)+1,
    e=uniform state on E,  delta=(n+1)/2^n.

The b_ij are orthonormal and

    s0-sum_{i<j} 2^(-j/2) b_ij=sqrt(delta)*e.

Therefore dim V=K and e belongs to V. Every vector in V has a common
amplitude on all points of E (and separately on each C_ij).

Let s be ANY normalized stabilizer ray contained in V. If its amplitude
on E is zero, `<e|s>=0`. Otherwise its affine computational support contains
E. Since E affine-spans F_2^n, that support must be the entire cube.
Every amplitude then has magnitude `2^(-n/2)`, and the equal-amplitude
condition on E fixes their phases there. Consequently

    |<e|s>|^2 is either 0 or delta.                         (1)

Now take ANY finite positive weighted stabilizer frame entirely in V that
spans V, with arbitrary number of rays and arbitrary positive weights:
`F=sum_a w_a |s_a><s_a|`. Its trace on V is W=sum_a w_a. Equation (1) gives

    lambda_min(F|V)<=<e|F|e><=delta W,
    lambda_max(F|V)>=W/K.

Hence its spectral condition number satisfies

    condition(F|V)>=1/(K delta)=2^n/[K(n+1)].               (2)

This is independent of the dictionary size and all positive weights. In
particular any unweighted stabilizer basis of V has minimum Gram
eigenvalue at most `K(n+1)/2^n`. Since K=Theta(n^2), this rules out an
inverse-polynomial bound in either K alone or (n,K). If a proposed frame
does not span V, it already fails the promised reconstruction.

Define restricted squared extent by allowing only stabilizer rays in V.
Taking the inner product of any such decomposition of e with e proves

    xi_V(e)>=1/delta=2^n/(n+1).

In sharp contrast, its computational-basis decomposition gives unrestricted
`xi(e)<=n+1`. Each individual computational-basis ray in this decomposition
lies outside V, since it is not constant on E. One can also determine the
unrestricted fidelity exactly: a dimension-d affine support meets the
affinely independent set E in at most d+1 points, so

    F_S(e)<=max_{0<=d<=n} (d+1)^2/[(n+1)2^d]
           =9/[4(n+1)].

The uniform stabilizer on span(e_1,e_2) achieves equality. Thus the global
extent is between `4(n+1)/9` and n+1: polynomial, while its restricted
extent and every in-span frame's conditioning are exponentially worse in n.

## What operation this rejects, and what remains open

A concrete attempted operation was to sample a signed Pauli from a
supplied frame member's stabilizer group, project another member, retain
the resulting normalized stabilizer only if it lies in V, and exchange
a basis column when its Gram determinant grows. All individual steps are
paid classical tableau/inner-product/linear-algebra operations. For
`t=S*c` in V, replacing column j multiplies the Gram determinant by
`|c_j|^2`. An inverse-polynomial-probability improvement lemma until
polynomial conditioning would have supplied a constructive basis theorem.
Equation (2) falsifies that lemma and even unrestricted in-span dictionary
augmentation. Better search or extra in-span projection depth cannot
remove this exact obstruction.

The native endpoint of interest remains: copies of an unknown normalized
n-qubit pure state of rank at most polynomial k, no decomposition advice,
and an epsilon-accurate preparation description in polynomial
`(n,k,1/epsilon,log(1/eta))` resources. A supplied-frame construction is only
a possible structural proof tool; it is not secretly available to that
learner. Public-frame Gram/tableau processing is the matched classical
baseline, while the published bounded-extent learner already handles the
quantum access once its extent promise is paid.

Progress now requires an OUT-OF-SPAN operation whose total coefficient cost
improves the actual published recurrence, or another concrete native
learning mechanism. No such operation was established in this review.
The parent's one exact control may falsify algebraic implementation details;
it is not needed for, and cannot establish, these all-n statements. There
is no new learner, novelty claim, general extent lower bound, state-learning
hardness claim or quantum execution here.

## Addendum: forcing every minimum-rank decomposition into V

The following strengthening is valid for every n>=2. It removes the
possibility that a minimum-rank decomposition repairs the conditioning by
choosing a different span. It still does not obstruct unrestricted extent
or approximate tomography.

Let F0=Q(zeta_8), choose the original K-element stabilizer basis
`s_0,...,s_(K-1)` of V with its canonical phases, and put
`R=sum_{x in E}|x>`. All these vectors have coordinates in F0 and R is in V.
Choose an odd prime p with `K<p<2K`, which exists by Bertrand's theorem
since K>=2, and let theta be the positive root of `X^p-2`. Define

    epsilon0=2^(-2n)/(8K),
    z=R+epsilon0*sum_{j=0}^{K-1} theta^(j+1) s_j,
    v=z/||z||.

The degree of Q(theta) is p by Eisenstein. If
`d=[F0(theta):F0]`, the tower formula gives
`4d=p*[F0(theta):Q(theta)]`; hence p divides d, while d<=p. Thus d=p.
In particular `1,theta,...,theta^K` are linearly independent over F0.
This does not incorrectly infer linear disjointness from an arbitrary
intersection statement; the coprime degrees directly force the result.

Let W be ANY complex span of stabilizer rays containing v. Choose a
canonical global-phase representative for each ray; every such normalized
stabilizer has coordinates in F0, and changing its global phase does not
change W. If V is not contained in W, linear algebra over F0 supplies an
F0-linear functional ell that vanishes on W's F0 generators but not on V.
Extending ell complex-linearly, it vanishes on W and therefore on z:
normalization is irrelevant because z is a nonzero scalar multiple of v.
It follows that

    ell(R)+epsilon0*sum_j theta^(j+1) ell(s_j)=0.

This is a polynomial in theta of degree at most K<p with F0 coefficients.
All coefficients must vanish, so every ell(s_j)=0, contrary to the choice
of ell. Therefore EVERY stabilizer span containing v contains V.

Since v itself lies in V, its exact stabilizer rank is K. A decomposition
with exactly K stabilizer terms has a span W of dimension at most K; the
preceding containment forces W=V, with independent terms. Thus every
rank-minimal decomposition is confined to precisely the same V, regardless
of its chosen rays or phases.

The quantitative perturbation is small. Since theta^K<2,

    d0:=||z-R|| <= 2K epsilon0 = 2^(-2n)/4,
    ||v-e|| <= 2 d0/sqrt(n+1)
              <=2^(-2n)/(2 sqrt(n+1)) <= sqrt(delta).

Here e is the normalized uniform state on E, and delta=(n+1)/2^n as
above. The first normalization inequality follows directly from the
reverse triangle inequality, with z nonzero. Equation (1) therefore gives
`|<s|v>|<=2 sqrt(delta)` for every stabilizer s in V. Any decomposition
of v using only such rays has squared coefficient l1 norm at least

    1/(4 delta)=2^n/[4(n+1)].                              (3)

In particular (3) holds for EVERY exact rank-minimal decomposition of v.
It is exponential in sqrt(K), up to polynomial factors.

There is nevertheless an explicit low-cost decomposition outside V. Use
the n+1 computational-basis terms of R and the K displayed perturbation
terms. Its coefficient sum, after normalization, is at most

    ((n+1)+2K epsilon0)/(sqrt(n+1)-2K epsilon0)
        <=2 sqrt(n+1).

Consequently the unrestricted squared extent satisfies `xi(v)<=4(n+1)`,
using at most K+n+1 terms. This upper bound is polynomial and is consistent
with the known bounded-extent learner.

The family has polynomial classical descriptions: p=O(K), epsilon0 has
O(n+log K) bits, and z's coefficients lie in the degree-4p field F0(theta).
Its norm squared remains in that field because complex conjugation fixes
theta and preserves F0. Adjoining the positive normalizer increases the
degree by at most two, so degree at most 8p suffices. Computing the norm
uses the polynomial-size stabilizer Gram matrix and the displayed algebraic
coefficients; it does not require an expanded 2^n-coordinate vector.

For this KNOWN family, the outside decomposition also gives paid ordinary
LCU preparation: the normalized coefficient sum is at most 2 sqrt(n+1),
so standard LCU success is at least `1/[4(n+1)]`. Controlled preparations
of all displayed stabilizers and approximation of these bounded-degree
algebraic coefficients have polynomial cost. Capped repetitions and a
fallback give an approximate finite preparation procedure. This is not
access to an unknown source's frame or inverse.

The strengthened falsifier rejects the assertion that one can first choose
an EXACT minimum-rank decomposition and then rely on polynomial coefficient
norm for LCU or coefficient-based sampling. It is not a lower bound on
every preparation method using a supplied description. Moreover v is
exponentially close to e: at ordinary inverse-polynomial target accuracy,
the tiny algebraic perturbation can be ignored. No approximate-learning
hardness, superpolynomial global extent or generic tomography obstruction
follows. No new finite test was used for this addendum.
