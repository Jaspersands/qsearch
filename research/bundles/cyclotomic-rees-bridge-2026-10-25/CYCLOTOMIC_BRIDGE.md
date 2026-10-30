# Cyclotomic Cosets Versus The Rees Receiver

2026-10-25. A scoped bridge audit with exact arithmetic controls. These are
local mathematical deductions, not a new algorithm, a hardness result,
independent review, or an audit of the entire source paper.

## Decision

The existing fixed-class Rees proposal does **not** turn the cyclotomic
coset sieve into a polynomial algorithm for growing modulus. This fails
at the parameter level, at scalar coefficient separation, and at the
suggested Newton-basis repair. All three failures are distinct. The
existing Rees theorem keeps its original scope; none of these controls
refutes it or the published cyclotomic algorithm.

The last obstruction is stronger than a bad choice of coordinates:
for every prime p and t>=2, an actual order-p unipotent dilation cannot
be diagonalized by ANY linear change of basis, even over an extension field.

## Source And Input

[Boucher, Fouque and Shen, arXiv:2609.34996v1](https://arxiv.org/html/2609.34996v1)
introduce cyclotomic cosets and a fixed-prime quasipolynomial sieve. Their
input is independent quantum samples, not a preparation circuit with its
inverse. They explicitly do not infer an algorithm for standard LWE.

Use the paper's native setting: prime p, q=p^t,
R=(Z/q)[zeta_p], pi=zeta_p-1, L=t(p-1), and

    G = R^n semidirect F_p,
    (x,a)(y,b) = (x + zeta^a y, a+b),
    lambda_a = sum_(i=0..a-1) zeta^i,
    H_s = {(lambda_a s,a): a in F_p}, s in (Z/q)^n.

The input states are p^(-1/2) sum_a |a>|x+lambda_a s>.
The Fourier pairing is the RAMIFIED pairing

    B_L(x,y) = Tr_(Q(zeta)/Q)(xy/(p*pi^(L-1))) mod 1.

Replacing this with finite-field trace changes the source. Our explicit
ring controls implement this pairing with rational arithmetic and retain
the original scalar-secret restriction. n=1 controls below are diagnostic
instances of this source, not proposed toy search problems.

## 1. There Is No Growing-Modulus Fixed-Class Regime

Commutators satisfy

    [(x,a),(y,b)] = ((1-zeta^b)x + (zeta^a-1)y,0),
    [(0,1),(x,0)] = (pi*x,0).

Consequently gamma_k(G)=pi^(k-1)R^n for k>=2, and the nilpotency
class is exactly L. This also matches the cited paper's Lemma 2.
The important parameter deduction for the proposed bridge is

    p <= 2^(p-1), hence q=p^t <= 2^L.

Thus class bounded by an absolute C forces q<=2^C, regardless of how p
and t vary. ANY unbounded-q regime leaves the fixed-class guarantee.
For the original prime-field Lazard core, L<p holds precisely when t=1.
At t=1 the group has exponent p, but increasing q=p increases its class
p-1. At t>=2 even a translation by 1 has order p^t, not p.

The separate bounded-prime branch of the whole Rees proposal does not
remove the fixed-class condition. Do not present failure of the Lazard
core alone as a refutation of that broader branch. The derived-rank
extension is not an immediate polynomial remedy either: at t=1 the
derived F_p-dimension is n(p-2). The hidden index has log_p index nL;
bounded-codimension hypotheses cannot silently be imported.

At bounded q the cited sieve's 2^O_p(log n log q) bound is already
polynomial in n. Staying inside fixed class therefore does not supply
the sought change in complexity class for this particular application.

The frozen Rees resource note provides a sufficient copy bound with
dimension exponent sum_(j=2..c) j^2 and class-dependent constants. It is
not uniform polynomial time in growing c. A very large upper bound is
also not a lower bound on possible improved receivers.

## 2. Scalar Evaluation Loses A Retained Direction

For EVERY prime p and t>=2 consider the positive-degree formal polynomial

    P(T)=p^(t-1)*(T^p-T) in (Z/p^t)[T].

Both displayed coefficients are nonzero, yet P(s)=0 for every integer
s, by Fermat's congruence. Its degree p is at most L. Regard its
coefficients as commuting translations in the native cyclotomic group.
The degree-p coefficient lies in gamma_p: p^(t-1) is in
pi^((t-1)(p-1))R, which is contained in pi^(p-1)R. The first coefficient
is a nonzero retained grade-one direction. Thus it meets the coefficient
filtration used in the proposed scalar-evaluation extension.

Every scalar evaluation is the identity translation, hence belongs to
H_s. But H_s intersects the translation subgroup trivially. The nonzero
first coefficient does NOT belong to that intersection. Therefore the
equivalence "all evaluations are hidden iff every coefficient is hidden"
fails. Taking more scalar evaluation points, even all of Z/p^t, cannot
repair it. This uses commuting components and does not assume an illegal
BCH formula exists at class >=p.

Nor can we just quotient out null polynomials: the vectors
p^(t-1)T^p and p^(t-1)T then become equal, while their grade-one
projections differ. The retained grade-one recovery map would cease to
be well-defined. This rules out that particular repair, not every cover.

## 3. Newton Separation Is Not Homogeneous Cancellation

Integer-valued Newton functions binom(T,j), j=1,...,c, evaluated at
T=1,...,c form a unit lower triangular matrix. They DO separate additive
coefficients over torsion rings. This is a genuine repair of separation.
It does NOT by itself construct a compatible nonabelian cover.

Under scalar substitution the action is triangular rather than diagonal:

    binom(2T,4)=binom(T,2)+12 binom(T,3)+16 binom(T,4).

In the actual p=3,t=2 ring, z=pi^3 is central, nonzero, and 3z=0.
The top sequence binom(T,4)z acquires a nonzero degree-two term under
T -> 2T. Discarding the top grade therefore does not commute with this
dilation. At T=2 the actual value is z; the guessed diagonal value is 0.

There is a basis-independent obstruction as well. On the F_3 module
with basis z*binom(T,j), j=1,...,4, substitution T -> 4T has matrix

    D_4 = [[1,0,1,1],
           [0,1,0,2],
           [0,0,1,0],
           [0,0,0,1]] over F_3.

Writing D_4=I+N gives N!=0, N^2=0, D_4^3=I. Its minimal polynomial
is (X-1)^2. It cannot become diagonal under a linear basis change.
Every putative scalar weight 4^j is 1 mod 3; their diagonal matrix
would be I, not D_4. This is an actual unit substitution (4 is a unit
mod 9), not an inadmissible zero or nonunit dilation. The action retains
p-adic information discarded by residue-field scalar powers.

This obstruction holds for EVERY prime p and t>=2, not just the finite
control. Choose nonzero z in pi^(L-1)R, so pz=0, and retain the central
module with basis z*binom(T,j), j=1,...,p. The filtration permits it
because p<=L. The basis is independent by the unit triangular evaluation
matrix. In F_p, compare coefficients through degree p in

    (1+X)^((1+p)T) = (1+X)^T * (1+X^p)^T.

For nonnegative integer T this gives

    binom((1+p)T,j) = binom(T,j)           mod p, j<p,
    binom((1+p)T,p) = binom(T,p)+T         mod p.

It follows that substitution by the legal unit 1+p has matrix
D_(1+p)=I+E_(1,p) on this module. Its nonzero nilpotent part squares
to zero, its order is p, and its minimal polynomial is (X-1)^2.
Thus NO linear basis repair makes the action diagonal. The Newton
functions used here have period p^2 mod p, compatible with the scalar
domain Z/p^t for t>=2. This does not require any unsupported extension
from field points to a larger coherent evaluation domain. This is an
action on central-valued FUNCTIONS of the scalar parameter; it does not
assert that a compatible nonabelian cover has already been constructed.

A next attempt needs a non-diagonal cancellation theorem on a genuine
filtered group source, or a different source reduction. Merely replacing
monomials with binomial functions does not establish either one.

## 4. Reducing Modulo p Loses Native Secret Information

At p=3,t=2,n=1 there are 81 ring elements and 243 group elements.
The ideals pi^k R have sizes [81,27,9,3,1]. H_0 and H_3 are different
native hidden subgroups, but coefficient reduction mod 3 identifies
their images. This reduction cannot be called lossless secret recovery.

The source itself distinguishes them. For the legal phase label y=zeta,
the three phase exponents for s=0 and s=3 are respectively

    (0,0,0) and (0,1/3,0).

Their pure-state fidelity is exactly 1/3. The pairing matrix q*B_L in
basis (1,zeta) is [[0,1],[1,8]] modulo 9 with unit determinant -1.
Both nondegeneracy and the nonzero high-digit signal are checked exactly.
This is an information-loss control, not a search algorithm or a lower
bound on all adaptive quotient-and-lifting strategies.

An unramified finite-field replacement is not innocuous either: in
characteristic p, Phi_p(X)=(X-1)^(p-1). A field has no nontrivial
p-th root of unity, whereas pi is a nonzero nilpotent in this input.

## 5. The Small Normalizer Does Not Supply An Algorithm

Conjugating the generator (s,1) by (v,a) gives
(zeta^a s-pi*v,1). A normalizer must fix that generator, since it is
the unique member of H_s with second coordinate 1. Hence

    N_G(H_s) = {(lambda_a s+w,a): w in ann(pi)^n},
    ann(pi)=pi^(L-1)R,
    |N_G(H_s)|=p^(n+1), [G:N_G(H_s)]=p^(n*(L-1)).

This exact normalizer formula contains the UNKNOWN secret. It does not
give a public normalizer-construction routine. The L=1 edge case correctly
returns all of the abelian group. Exhaustive native controls check the
formula for three different secrets at p=3,t=2,n=1.

## What Could Still Work, And How To Falsify It

The live question is a receiver for the actual ramified source that
handles the nonsemisimple unit action with polynomial TOTAL copy cost
in n and log q. A Hall--Petresco/divided-power construction might be a
language for this question, not an answer. It must specify its group,
hidden subgroup, source channel, stable central quotients and cancellation
algorithm before any implementation campaign is justified.

Reject a proposal if any of the following is unaccounted for:

- It grants a coherent preparation inverse for copy-only input.
- It replaces the ring by a field or drops the high secret digits.
- It uses the scalar diagonal equations on the non-diagonal D_4 module.
- It hides the full copy tree behind polynomial cost per layer. Fresh
  branching at each of L layers multiplies, not adds, acquisition cost.
- It supplies only correct single-copy marginals, not the required joint
  source/error guarantee. For M independent delta-close copies, the
  elementary bound is M*delta; correlated inputs need a separate argument.
- It claims a consequence for classical LWE without a charged reduction
  producing the required number and quality of quantum samples.

No new classical hardness assumption is established here. A putative
advantage needs comparison at the SAME input representation; measuring
samples early is a restricted baseline, not a general dequantization.
The explicit known-secret controls are not performance comparisons.

This audit rejects a bridge, not the cyclotomic direction wholesale.
Do not build another sieve framework from this note. First produce an
actual replacement cancellation/source mechanism, and compare its bound
with the existing published receiver. Otherwise pivot back to a
constructive frontier rather than enlarging these finite controls.
