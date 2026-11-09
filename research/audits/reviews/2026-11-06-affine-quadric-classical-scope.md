# Affine quadratic character learning: classical and oracle scope

2026-11-06. Written derivation independently reviewed by the parent against
this complete text, the existing irreducible birthday control, and the
native access contract. The two prescribed Sage algebra controls below
are complete. The four-template birthday extension is accepted as a
WRITTEN algorithm; it is NOT implemented or executed at this checkpoint.
No Git, network, external-service action, registry promotion or quantum
execution. Repository Python is `/opt/anaconda3/bin/python`; exact finite
field controls use `/opt/anaconda3/envs/qsearch-cas/bin/python`.

## 1. Native contract and source distinctions

Let p be an odd prime, n>=3, and

    F(x)=x^T A x+2 b^T x+c,

where A is an unknown invertible symmetric matrix over F_p. Neither b nor
c is restricted. A native classical query returns ONLY lambda(F(x)),
where lambda(0)=+1 and lambda(z)=chi(z) otherwise. Output is (A,b,c) up
to a common nonzero scalar. The parent claim in
`../../AFFINE_QUADRATIC_CHARACTER_SLICE_READOUT.md` instead starts from
fresh exact GLOBAL pure phase copies. These are different access models.

Corpus `been-tried` and `baselines` lookups preceded this derivation; no
catalog entry directly matched the exact affine character input. The
actual prior code/source distinctions in
`2026-11-05-quadric-classical-scope.md` remain applicable. Full field-value
quadratic interpolation and Boolean additive-phase reconstruction do not
receive this sign-only input. The saved
`../../classical_baselines/quadratic_legendre_birthday.py` implements only
the monic IRREDUCIBLE line promise. Section 5 below proves a separate
proposed scope extension; it is not a claim about that implementation.

## 2. Paid affine line reduction, including the exceptional center

Let

    T={0,+e_i,-e_i,e_i+e_j : 1<=i<=n, i<j<=n},
    m=|T|=(n+1)(n+2)/2.

Choose independent uniform w,u in F_p^n and query the lines v+t u for
v in w+T. Write

    a=u^T A u,
    ell_v(u)=u^T(A v+b),
    D_v(u)=ell_v(u)^2-a F(v).

If a D_v(u)!=0, the restriction divided by a is the monic squarefree
quadratic

    q_v(t)=t^2+2 ell_v(u)/a*t+F(v)/a.                 (1)

The possibility that D_v is IDENTICALLY zero must be handled. If
F(v)!=0, its matrix is

    (A v+b)(A v+b)^T-F(v)A,

which cannot vanish: the first summand has rank at most one, while the
second has rank n>=3. If F(v)=0, D_v=ell_v^2 is identically zero exactly
when A v+b=0. Thus the only structural exception is the unique critical
point h=-A^-1 b, and only if F(h)=c-b^T A^-1 b=0. A fixed grid can contain
that point, making all its line restrictions repeated squares.

The random translation avoids this exception with probability at least
1-m/p^n. Conditional on avoidance, each D_v is a nonzero degree-two
polynomial in u. The polynomial a is also nonzero. Schwartz--Zippel gives

    Pr[a!=0 and all D_v(u)!=0]
      >=1-m/p^n-2(m+1)/p.                            (2)

No hidden coefficients or discriminants are used to select w or u. Their
goodness is an analysis event, not an oracle or postselection rule. For
p>=16n^2, n>=3, the right side exceeds 3/4.

Given the constant coefficients of all decoded q_v, let
z_t=F(w+t)/a. Recover the public-coordinate coefficients by

    Abar_ii=(z_ei+z_-ei-2z_0)/2,
    dbar_i=(z_ei-z_-ei)/4,
    Abar_ij=(z_(ei+ej)-z_ei-z_ej+z_0)/2,
    bbar=dbar-Abar w,
    cbar=z_0-w^T Abar w-2 bbar^T w.                  (3)

These are exactly A/a, b/a, c/a. Normalize the returned coefficient
vector by its first nonzero entry to compare projective outputs across
independent attempts. Bounded repetition and majority pay the constant
failure probability in (2); no unknown-value verification is needed.

## 3. Full-table moment decoder with an UNKNOWN leading character

A squarefree line has the form

    g(t)=lambda(a((t-h)^2-d)), a*d!=0,
    epsilon=chi(a), r in {0,2} its number of roots.

In the affine problem epsilon is NOT available as lambda(F(u)). Query
all p signs. Let S0=sum_t g(t) be an INTEGER sum, let
S_j=sum_t t^j g(t) in F_p, and use centered field moments M_j.
For p>=11,

    S0=r-epsilon, h=S_1/S0,
    M2=S_2-h^2 S0=d(r-epsilon/2),
    M4=S_4-4h S_3+6h^2 S_2-3h^4 S0
       =d^2(r-3epsilon/8).                           (4)

To derive the fourth identity, apply Euler's criterion to
z^4(z^2-d)^((p-1)/2). For p>=7 its only positive exponent divisible by
p-1 has coefficient binom((p-1)/2,2)d^2=3d^2/8 in F_p; the field power
sum contributes its negative. The padded roots contribute r*d^2.
The analogous second-moment coefficient is d/2. Odd centered moments
vanish by symmetry. Padding is retained throughout.

The three integer possibilities for S0 are -1,1,3. If S0=-1, epsilon=+1;
if S0=3, epsilon=-1. If S0=1, there are two possibilities:

    epsilon=-1, r=0: 2 M4=3 M2^2;
    epsilon=+1, r=2: 18 M4=13 M2^2.                 (5)

For p>=11, M2!=0 and these alternatives are disjoint: the two ratios
M4/M2^2 are 3/2 and 13/18, differing by 7/9. Characteristic seven is
therefore excluded from this particular leading-sign decoder. Recover
r=S0+epsilon and d=M2/(r-epsilon/2), then q(t)=(t-h)^2-d. All denominators
are nonzero for p>=11. Off-promise tables may be rejected; correctness
and the success estimate only use the good-line event (2).

The complete grid costs m*p=O(n^2 p) native sign queries and O(n^2 p)
scalar field operations for moments. Explicit n-coordinate query assembly
gives the safe O(n^3 p) field-operation bound, with polynomial(log p)
bit cost per operation. No hidden leading sign, full-value query, root
flag, or irreducibility promise is supplied. Independent canonical-majority
attempts multiply these costs by O(log(1/eta)).

## 4. Existing quantum ORACLE corollary

BIT or raw phase access prepares the chosen line phase state with one
query, using reversible public computation of v+t u. Up to the physically
irrelevant global sign epsilon=chi(a), that state has signs

    epsilon lambda(a q_v(t)).

These agree with lambda(q_v(t)) away from the at-most-two roots; the
root signs may differ. This is ONE fixed corrupted sign function for that
line, with fresh pure copies, not resampled or mixed noise. The reviewed
fixed-corruption degree-two theorem applies, for example using rho=1/8
and sufficiently large p. The newer bound in
`../../LEGENDRE_HANKEL_RESULTANT_READOUT.md` permits p>=1024 at d=2,
kappa=1/2; p>=16 already pays the at-most-two-root corruption fraction.

Apply the decoder to all m lines with failure at most 1/(16m) each and
then (3). Together with (2), a whole attempt succeeds with probability
at least 11/16 when p>=max{16n^2,1024}. Independent canonical-majority
repetition gives error eta with polynomial(n,log p,log(1/eta)) total
oracle queries, gates and workspace. There is no controlled unknown
unitary or source inverse in this composition.

Thus the polynomial BIT/raw-phase upper bound already follows from the
univariate theorem. Fresh GLOBAL copies do not freely supply these
chosen-line states: direct computational projection onto a prescribed
affine line has probability p^(1-n). This is a source distinction, not
a general impossibility theorem for processing global copies.

## 5. Four-template birthday extension: reviewed written algorithm

This section extends the mathematical center/width strategy of the
existing irreducible-line control. The parent independently checked this
actual proof; it has NOT been implemented. It handles every squarefree line above, including
split roots and an unknown leading character, for p>=61.

Fix a desired per-line error zeta in (0,1). Obtain a public nonsquare
nu by capped independent sampling from F_p^*. Each trial fails with
probability 1/2; ceil(log2(8/zeta)) trials pay failure at most zeta/8.
All character computations here are public and charged.

For distinct monic squarefree quadratics, their product is not a square.
The quartic Weil bound is at most 3sqrt(p). Replacing zero character values
by padded signs changes a correlation on at most four points. Restricting
to F_p^* adds at most one further unit. Therefore any pair of distinct
functions arising below has fingerprint agreement at most

    1/2+(3sqrt(p)+5)/(2(p-1)) <=3/4,  p>=61.        (6)

If the monic quadratics coincide and only the leading-character signs
differ, they agree only at roots, at most two points; (6) still holds.
The center-stage bound over all F_p is no larger.

Set B=ceil(sqrt(p)). Query fingerprints of g(x+t), t=0,...,B-1, and
g(-x+u), u=jB mod p, j=0,...,B-1, at the same independent uniform offsets
x. There is an exact match with t+u=2h, since the integer sums t+jB cover
0,...,p-1. A false match has probability at most (3/4)^L, where

    L=ceil(log(16p^2/zeta)/log(4/3)).

All translated/reflected functions belong to the same family of p distinct
translates, so this stage is covered by fewer than p^2 potential false
pairs. Abort on duplicate signatures for distinct stored translations;
this caps work even on a bad fingerprint event. An exact match gives h.

For the width stage use four public template classes

    T_(a0,e,v)(y)=lambda(a0((v y)^2-e)),
    a0 in {1,nu}, e in {1,nu}, v in G=F_p^*/{+1,-1}.

The quotient has N=(p-1)/2 elements, represented by 1,...,N. For the
correct two character classes, d/e is a square and the equality

    d=e(u/v)^2

makes T_(a0,e,v)(y)=g(h+u y) for EVERY y, including padded roots.
The unknown ratio a/a0 and the factor (u/v)^2 are squares. Thus the
source's N width functions are exactly one of these public N-element
template families, in permuted order. No unknown square root is computed.

Take M=min{N,ceil(sqrt(N log(4/zeta)))} distinct public quotient labels v
in each template class, and M independent uniform source labels u with
replacement. The true matching u->v is a bijection of G. If M<N, missing
all matches has probability at most

    (1-M/N)^M <= exp(-M^2/N) <=zeta/4;

if M=N, a match is certain. Use L fresh shared uniform nonzero fingerprint
offsets y. The complete four-template family has 4N<2p elements, hence
fewer than 2p^2 potential false pairs. Together with the center stage,
the union probability of any false fingerprint is at most
3p^2(3/4)^L<=3zeta/16. Store at most one entry per signature, aborting on
duplicates, so fingerprint failure cannot cause unbounded candidate work.
One matching pair yields d=e(u/v)^2 and the monic polynomial immediately.

All lists and samples have fixed caps. Exact uniform finite-field/quotient
sampling may use bounded binary rejection; allocating zeta/8 over all
planned draws adds polynomial logarithmic overhead. Combining that cap,
nonsquare search, fingerprint collisions and missing-width matches gives
failure at most 11zeta/16<zeta. This proves the written resource bound

    O(sqrt(p)*poly(log p,log(1/zeta)))

for native chosen queries, classical time and storage per squarefree line.
It does not assume consecutive/passive data, monicity of the original
restriction, irreducibility, a supplied leading character or supplied
roots. The four template classes are essential to the extension.

Compose with (1)--(3), taking zeta=1/(16m), to get success at least 11/16
per whole affine attempt at p>=max{61,16n^2}. With
R=ceil((128/9)log(1/eta)) independent attempts, canonical majority fails
with probability at most exp(-9R/128)<=eta by Hoeffding. The resulting
query bound is O(n^2 sqrt(p)*poly(log p,log n,log(1/eta))); explicit query
assembly adds a factor n to the field-work bound. This is still
exponential in log p. No optimality, novelty or classical lower bound is
claimed. Section 3 is the executed finite-control baseline; this section
is the stronger independently checked WRITTEN upper bound. The existing
saved birthday implementation still has its monic irreducible scope.

The parent checked the false-pair counting explicitly: after the correct
center is found, all source width functions belong to one of the four
public template families. Thus the union bound ranges over fewer than
2p^2 unordered false width pairs, not an extra independent source family.
The exact width match includes padded roots because the entire polynomial
ratio is a nonzero square. When M=N the miss probability is zero; the
exponential estimate is only needed for M<N. The exceptional affine center,
fourth-moment ambiguity and oracle-only source conversion in Sections2--4
were also checked. No broader prior-art or optimality conclusion follows.

## 6. Clean shifted-Legendre implication

Suppose a worst-case classical polynomial(n,log p) learner exists for
this native affine family. For an unknown shift s, take the public family

    F_s(x)=sum_i x_i^2+s.

Each query is simulated by one call to L_s(sum_i x_i^2), where
L_s(t)=lambda(t+s). The quadratic matrix is I for EVERY s, including zero.
Any returned projective triple gives s=c'/A'_{11}. Thus the hypothetical
classical learner solves all shifted Legendre instances. No zero repair,
singular-input call or extra oracle is needed. This is a reduction between
chosen classical oracle problems, not hardness, separation, or a reduction
from a classical sign oracle to the parent's copy-only input.

## 7. Exact controls and boundaries

The standalone reproduction is

    /opt/anaconda3/envs/qsearch-cas/bin/python research/classical_baselines/affine_quadric_line_control.py

It performs only the two predeclared controls; it does not execute the
birthday extension or any quantum circuit.

1. Over F_11, all 11*10 monic squarefree quadratics, represented as
   (t-h)^2-d with d!=0, and both leading-character classes. All220 cases
   recover correctly from2420 native sign queries. Exactly110 cases have
   the otherwise ambiguous integer sum S0=1. No failures.
2. Over F_101, n=3, A=diag(1,2,3), b=(4,5,6),
   c=b^T A^-1 b=91, w=(2,3,5), u=(1,4,2). The ten grid lines use1010
   native sign queries. All line decodes succeed and (3) returns exactly
   (A,b,c)/(u^T A u). The critical value is zero, so this control includes
   the family for which a fixed grid could hit the exceptional center.
   The public selected grid does not hit it. p101 is below16n^2=144;
   this is an algebra receipt, not a genericity-probability test.

The decoder receives only public p,n,w,u and the sign callable. Hidden
coefficients are confined to source construction and post-output truth
comparison. These finite controls do not prove any asymptotic guarantee.

Keep novelty, asymptotic separation, classical hardness, global-copy to
chosen-line conversion, mixed-source robustness and quantum execution
claims false. The scope of the parent's fresh-copy theorem requires its
own actual-text review; this note reviews the native baselines and source
comparison, not that new receiver.
