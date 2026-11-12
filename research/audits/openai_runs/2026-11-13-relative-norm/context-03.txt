# Quadratic squareclasses by rational norm conics

2026-11-13. Independent mathematical attack on the parent's proposed
quadratic bypass. The exact sequence and a stronger primitive-numerator
lifting lemma survive. The algebra below is proved directly. A polynomial
algorithm is **conditional here** on a source-verified rational-conic search
backend with the stated bit clock. The parent is separately checking that
source. No API report, ACCEPT label, or finite example proves that clock.

Read context: `research/STATE.md` (current top state), `research/TRAPS.md`,
`research/GOAL.md`, and `research/GENERAL_NATIVE_SELMER_COMPOSITION.md`.
No archives, Git, network, or external API were used for this review.

## 1. Exact scope and statement

Let d be a nonzero squarefree integer other than 1, K=Q(sqrt(d)), and use
the maximal order for prime-ideal valuations. Let S_Q be a finite set of
rational primes containing every prime dividing 2 disc(K), equivalently
every prime dividing 2d. Let S contain ALL prime ideals over S_Q. Define

    U = Q(S_Q,2) = {q in Q*: v_p(q) even for p outside S_Q}/Q*^2,
    W = K(S,2) = {alpha in K*: v_P(alpha) even for P outside S}/K*^2.

Let V be the subgroup of U consisting of squareclasses having a rational
representative in N(K*). This is independent of the representative:
every rational square t^2 is N(t). Then there is an exact sequence

    0 -> U/<[d]> --inclusion--> W --norm--> V -> 0.

Thus, for s=|S_Q|,

    dim_F2 W = s + dim_F2 V.

The support condition is essential. No real-place sign restriction is
imposed on W itself; signs enter only in V through norm solvability.

## 2. Descent of the norm and injection on the rational kernel

For alpha in W and p outside S_Q,

    v_p(N alpha) = sum_(P|p) f_P v_P(alpha)

is even. Hence norm indeed maps W into U and its image lies in V.

A rational q in U belongs to W because v_P(q)=e_P v_p(q), so outside S
all valuations are even. If q is a square in K, write q=(x+y sqrt(d))^2
with x,y rational. Its sqrt(d) coefficient gives 2xy=0. Therefore q is
either a rational square or d times a rational square. Conversely d is a
square in K, and [d] belongs to U by the support hypothesis. This proves
the claimed injection U/<[d]> -> W, including d<0 and K=Q(i).

## 3. Complete norm kernel, with an elementary proof

Suppose alpha in W has square norm, N(alpha)=c^2 with c in Q*.
If alpha=-c, it is already rational. Otherwise put

    q = Tr(alpha) + 2c.

Then

    (alpha+c)^2 = q alpha.

Since alpha+c is nonzero in a field, q is nonzero. Thus [alpha]=[q] in
K*/K*^2. This is a direct version of the Hilbert-90 argument, requiring
no constructive Hilbert-90 oracle.

For P outside S over p, all such primes are unramified, so e_P=1.
Taking valuations in the displayed square relation gives

    v_p(q) + v_P(alpha) = 2 v_P(alpha+c).

Since v_P(alpha) is even, v_p(q) is even. Hence [q] is in U. The special
case alpha=-c has the same parity conclusion directly. The kernel is
therefore exactly the rational image; there is no extra real-field,
torsion, ordinary-class-group, or negative-Pell term missing from it.

## 4. Stronger lift: no denominator factoring is needed

Take [a] in V and choose its signed squarefree integer representative a,
whose prime support is contained in S_Q. By definition there is a
rational solution of x^2-d y^2=a. Clearing denominators and removing the
common gcd gives a primitive integer point

    X^2 - d Y^2 = a Z^2,       gcd(X,Y,Z)=1.

Here Z is nonzero: otherwise nonsquare d forces X=Y=0. Define simply

    beta = X + Y sqrt(d).

This algebraic integer is already in W, and N(beta)=a Z^2 gives its
required norm squareclass. In particular, **do not factor Z or multiply
by a product of denominator primes**: those operations are unnecessary.

Proof: let p be outside S_Q. Then p is odd and does not divide ad. If
p divided both X and Y, the conic equation would imply p|Z, contrary to
primitivity. If p is inert, divisibility of beta by the unique prime
over p would mean X=Y=0 in the two-dimensional residue field over F_p,
again impossible. So its valuation is zero at inert p.

If p splits as P Pbar, both primes cannot divide beta: that would imply
beta is zero modulo p and hence p|X,Y. Therefore one of v_P(beta) and
v_Pbar(beta) is zero. The other is even, since

    v_P(beta)+v_Pbar(beta)=v_p(N beta)=2 v_p(Z).

This proves the required parity at every prime outside S. Ramified and
dyadic primes are all in S and impose no condition in this argument.

The original proposed normalization of alpha=beta/Z also works: at
each outside split denominator prime its valuations are (-k,+k), and
multiplication by p for odd k clears the parities. The numerator proof
is stronger because it avoids identifying or factoring those primes.

## 5. Exact linear algebra and constructive output

Use the basis -1 and the primes in S_Q for U. The standard quadratic
local-global theorem says

    [a] in V  iff  (a,d)_v = +1 for every place v of Q.

Equivalently this is Hasse--Minkowski for the ternary form
X^2-dY^2-aZ^2; a nonzero isotropic vector automatically has Z nonzero.
It is enough to test v in S_Q together with infinity: outside S_Q both
a and d are units at an odd prime, so the Hilbert symbol is +1.

Bilinearity makes these conditions a binary matrix with s+1 columns
and at most s+1 rows. Odd-prime Hilbert symbols use valuations and
Legendre symbols; the dyadic row uses the usual odd-unit residues mod8;
the real row is nonzero only when both arguments are negative. There is
no global class group or fundamental unit in this matrix computation.

Choose a complement to [d] in U by binary elimination and use its
rational representatives as the first s basis elements of W. Compute a
basis [a_1],...,[a_r] of V. For each a_j, get a primitive conic point and
output beta_j=X_j+Y_j sqrt(d) as above. Together these give a COMPLETE
basis of W. Independence follows by applying norm, then the injection
of U/<[d]>. Spanning follows by cancelling the norm of an arbitrary
class with a product of the beta_j, leaving the complete rational
kernel from section 3. No field-square independence test is needed.

The local-global theorem is used as a standard mathematical theorem
here. The parent owns its primary-source attribution and, separately,
the effective search theorem; this review did not browse for sources.

## 6. Bit resources and the precise conditional algorithm

Let L include log|d|, the summed bit lengths of the primes in S_Q, and
any conversion from the native quadratic polynomial to sqrt(d).
Assume that integer factorization is paid, and that a proved backend
finds a nonzero rational point on each solvable input conic in time
polynomial in its coefficient bit length, with controlled error and
only polynomially many factoring calls on polynomial-bit integers.
Alternatively, one may use its stronger actually verified interface if
it needs only factorizations of the original coefficients. Do not infer
that stronger interface from this proof.

There are at most s+1 conic calls; every a_j is a product of selected
input primes and a sign, so log|a_j|<=L. The matrix and all local tests
have polynomial bit cost. A polynomial-time backend necessarily returns
polynomial-bit coordinates. Clearing the three denominators and taking
their common gcd preserves polynomial bit size. Each beta_j therefore
has polynomial-bit explicit coordinates. There is no Pell-sized output,
unit expansion, ideal principality search, or support-factorization bill
for these beta_j. Exact conic residuals can be checked before using them.

For a native monic quadratic t^2+b t+c, write its discriminant as m^2 d
using paid integer factoring. In its native field,

    sqrt(d) = (2 theta+b)/m.

The conversion has polynomial bit size. This proof constructs global
squareclasses without computing the maximal order, although the global
Selmer pipeline may still need it for its separately paid local frames.

Consequently the global quadratic-squareclass stage is a classical
polynomial reduction to factoring plus the precisely specified conic
backend. If a primary-source theorem verifies that conic backend as a
polynomial factoring-oracle algorithm, it gives the corresponding
unconditional factoring-oracle upper bound. Replacing factoring by Shor
then gives a quantum polynomial stage without quantum S-unit or
class-group algorithms and without GRH. The parent must first verify
the source's actual bit clock, factoring requirements, output model,
randomness/error guarantee, and both signs of d. These are not supplied
by a conic software command or this finite control.

## 7. Real-field attack and the one durable exact control

Let d=34 and S_Q={2,17}. The equation X^2-34Y^2=-Z^2 has primitive point
(3,1,5). Hence beta=3+sqrt(34) has norm -25, and

    (beta) = (5, sqrt(34)+3)^2.

Thus beta belongs to W, including at the outside prime5. Meanwhile the
continued-fraction period of sqrt(34) is (1,4,1,10), of even length, so
the INTEGRAL negative-Pell equation x^2-34y^2=-1 has no solution.
Integral norm-minus-one units are therefore not a prerequisite for the
required virtual squareclass. Rational beta/5 has norm exactly -1.

Also N(6+sqrt(34))=2 and N(sqrt(34))=-34. These norm squareclasses span
U=<-1,2,17>, so dim V=3 and the theorem gives dim W=2+3=5. This dimension
is a deduction from the exact sequence, not a computed class-group
oracle result. No class group was needed for this control.

Durable one-example script and exact output:

- `2026-11-13-quadratic-norm-squareclasses-control.sage`
- `2026-11-13-quadratic-norm-squareclasses-control.json`

Command, from the repository root:

    /opt/anaconda3/envs/qsearch-cas/bin/sage research/audits/reviews/2026-11-13-quadratic-norm-squareclasses-control.sage > research/audits/reviews/2026-11-13-quadratic-norm-squareclasses-control.json

All final assertions passed. The control falsifies an integral-negative-
Pell prerequisite; it is not evidence for the universal bit clock.

## 8. Boundaries and next decisive work

The full-ramified-support assumption cannot be removed silently. For
K=Q(sqrt(35)) with S_Q={2}, the rational class5 is admissible in K(S,2)
because its valuation at the ramified prime over5 is2, but it has no
representative in Q({2},2) modulo the field-square relation35. The
displayed rational-kernel statement would fail. Likewise, S must contain
both primes over every selected split prime for the claimed rational
inclusion to be valid as written.

No extension to cubic/general branch fields follows. No local-image
algorithm, full Selmer composition, classical lower bound, practical
implementation, novelty, speedup, or negative-Pell decision algorithm
is claimed. The output retains the SAME complete native K(S,2) space;
it is not a weakened unit-only problem.

Next hard question: verify an original conic-search source at the
polynomial-bit factoring-oracle interface. Acceptance test: an actual
algorithm/theorem supplying a valid nonzero point for every locally
solvable diagonal ternary form, with controlled coordinate lengths and
the stated total bit/factorization cost. Mechanical follow-up after the
parent's source disposition: retain the one exact control, link the
proof/source in the composition note, and preserve all false gates.
The parent will record this checkpoint in the shared handoff, mechanical
queue, and state to avoid concurrent edits by this helper.
