# Affine quadratic character copies by random slices and homogenization

2026-11-06. Independently reviewed WRITTEN end-to-end composition. Three
prescribed source/algebra controls are complete. No novelty, separation
or quantum execution claim.

## 1. Problem, admission and theorem contract

Given fresh exact copies of

    |phi_F>=p^(-n/2) sum_x lambda(F(x)) |x>,
    F(x)=x^T A x+2 b^T x+c,                                (1)

over an odd prime field, where lambda(0)=+1 and lambda(a)=chi(a) for a!=0,
recover (A,b,c) up to one nonzero scalar. Assume n>=3 and A symmetric
invertible. Neither b nor c is restricted. No value oracle, selected-slice
copies, unknown-source inverse, or supplied dual-cone samples are available.

Set k=1 for odd n and k=2 for even n; m=n-k>=2 is even, r=m+1 is odd. Put

    D=r(r+1)/2,  J=binom(k+2,2),  T=JD.                    (2)

For every such F and every prime p>=256T, the reviewed composition uses
poly(n,logp,log(1/eta)) gates, classical work and workspace to recover the
projective coefficients with failure at most eta, 0<eta<=1/2. The copy
count is at most R(T-1+K), with R,K defined below.

This is a concrete collective-data operation for the published broader
character-polynomial learning problem: independent random slices provide
equations for ONE shared polynomial matrix. It avoids the cost of obtaining
many copies of a selected slice. It does not improve the degree dependence
of the univariate algorithm. A preceding two-cone convolution proposal was
deferred as adjacent to known geometrically uniform hidden-shift machinery;
it is not needed here. No new general research subsystem is proposed.

## 2. Public coordinates and the actual one-copy operation

At the start of EACH attempt, sample a public uniform P in GL_n(F_p), and
apply |x> -> |P^-1 x> to fresh copies. In these coordinates write

    F(P(u,z))=u^T B u+2 w(z)^T u+h(z),
    w(z)=Lz+b_u,
    h(z)=z^T E_0 z+2 b_z^T z+c.                            (3)

The leading m-by-m block B is invertible with probability at least
1-4m/p. Indeed its determinant is a nonzero polynomial of degree2m in the
first m columns of P: A has a nondegenerate m-dimensional subspace. For
an unconditioned random matrix, Schwartz--Zippel bounds its vanishing by
2m/p. Conditioning on invertibility costs at most two, since a random
square matrix is invertible with probability at least1/2. The algorithm
does NOT learn or test B before collecting data. Bad P is handled by the
final original-copy verifier and by resampling P on every attempt.

Measure z. It is exactly uniform on F_p^k and leaves a pure slice copy
over u. Append a public uniform state over t in F_p^*, and reversibly map
(u,t) to (tu,t). The resulting state is

    |psi_z>=[p^m(p-1)]^(-1/2)
            sum_{u,t!=0} lambda(u^T B u+2t w(z)^T u+t^2 h(z)) |u,t>.
                                                               (4)

Because t^2 is a nonzero square, lambda(t^2 a)=lambda(a), INCLUDING a=0.
Thus (4) is exactly the normalized restriction t!=0 of the ideal global
padded-character state |phi_Hz> of the r-dimensional homogeneous form

    H_z=[[B,w(z)],[w(z)^T,h(z)]].                            (5)

No zero flag was queried and no unknown event was postselected. Their
overlap is sqrt(1-1/p), so after the same phase convention

    ||psi_z-phi_Hz||^2=2(1-sqrt(1-1/p))<=2/p.                (6)

Apply an approximate F_p^r Fourier transform and measure y. Each original
copy supplies ONE classical row (z,y); it never supplies repeated copies
of a chosen z. The ideal states in (5) are analytical comparisons only.

## 3. One shared adjugate relation and uniform rank escape

Assume B is invertible in this analysis and put

    S(z)=h(z)-w(z)^T B^-1 w(z),   a(z)=B^-1 w(z),
    C(z)=adj(H_z)/det(B)
        =[[S(z)B^-1+a(z)a(z)^T,-a(z)],[-a(z)^T,1]].          (7)

Every entry has total z-degree<=2, and C_rr=1. Since A is invertible,
the quadratic part E=E_0-L^T B^-1 L of S is invertible. Hence S is a
nonzero degree2 polynomial and Pr_z[S(z)=0]<=2/p. Also C has degree
EXACTLY2: its top homogeneous degree2 block is

    (z^T E z) B^-1+(B^-1 Lz)(B^-1 Lz)^T.                    (8)

Over F_p(z), the first summand has rank m>=2, whereas the second has rank
at most1, so they cannot sum to zero.

For S(z)!=0, H_z is invertible of odd dimension r. The reviewed theorem
in QUADRATIC_CHARACTER_CONE_READOUT.md applies to its IDEAL Fourier law.
Mass alpha=(1-p^(-(r-1)))(1-1/p)^2>=1-2/p is uniform on

    Z_z={y!=0:y^T C(z)y=0}.                                 (9)

On Z_z, any other homogeneous quadratic not proportional to C(z) vanishes
with probability at most5/p, by the reviewed Witt-chart proof. All source
normalizations and zero spikes are inherited unchanged.

Use all T features z^e y_i y_j with |e|<=2, i<=j. Polynomial matrices
are represented by the corresponding symmetric coefficients: halve the
off-diagonal monomial coefficient when assembling C. Write q(z,y)=y^TC(z)y.
It is a linear relation among these features.

For ANY different feature polynomial d(z,y)=y^T M(z)y, not a constant
multiple of q, some entry of

    M(z)-M_rr(z) C(z)                                       (10)

is a nonzero polynomial of degree at most4. Otherwise M=M_rr C, and an
entry of C of degree2 forces M_rr to be constant, contradicting the
choice of d. Thus M(z) can be proportional to C(z) on at most4/p of z.

Suppose the accepted feature rows so far span a proper subspace W of
q-perp, of dimension <T-1. Choose d in W-perp not proportional to q for
the ANALYSIS; the algorithm does not need to know d. For an ideal fresh
row, failure to be a correct q-row outside W is contained in:

- S(z)=0: probability<=2/p;
- a proportional fiber in (10): probability<=4/p;
- y outside the nonzero cone: probability<=2/p;
- d vanishing on an otherwise good cone: probability<=5/p.

The total is at most13/p. This also proves the unique-relation/full-span
claim; it is not inferred from finite feature-matrix ranks.

### The missing hyperplane costs O(1/p), not O(1/sqrt p)

For any event projector Pi, (6) gives

    ||Pi psi|| <= ||Pi phi||+sqrt(2/p).

Apply this to the FAILURE event of ideal probability<=13/p. For the
joint measured-z state one can use the canonical purification over z;
its squared distance is still (6). Therefore an ACTUAL fresh row fails
to be a correct row outside W with probability at most

    (sqrt(13)+sqrt(2))^2/p <26/p.                            (11)

A block of T-1 fresh raw rows consequently gives rankT-1 and kernel q
with probability at least1-26(T-1)/p, conditional on good coordinates.
Including random P, generation succeeds with probability at least
1-[26(T-1)+4m]/p>3/4 at p>=256T. It is harmless to use the weaker1/2
bound in the capped schedule. No rejection of hidden bad rows is assumed.

## 4. Public reconstruction from the learned polynomial matrix

If the raw feature matrix has rank other than T-1, abort this attempt.
Interpret its one-dimensional kernel as M(z), require M_rr to be a
nonzero CONSTANT, and normalize it to C_rr=1. Compute publicly

    a(z)=-C_top,r(z),  K(z)=C_top,top(z)-a(z)a(z)^T.          (12)

Require a to be affine and K to have degree<=2. For the true relation,
K(z)=S(z)B^-1. Choose z0 from a fixed unisolvent degree2 grid:
{0,1,-1} when k=1, or {0,+/-e1,+/-e2,e1+e2} when k=2, such that
G=K(z0) is nonzero and invertible. Some grid point works because S is
nonzero. Abort if no such point exists. Choose any nonzero entry G_ij and
set

    Btilde=G^-1,
    Stilde(z)=K_ij(z)/G_ij,
    wtilde(z)=Btilde a(z),
    htilde(z)=Stilde(z)+a(z)^T Btilde a(z).                  (13)

Require K=Stilde G coefficientwise. The resulting affine quadratic is
F(P(u,z))/S(z0) for the true C. Check that its FULL n-by-n quadratic part
is invertible, then undo the public P to obtain a candidate Ftilde in the
original coordinates. Everything here is polynomial-sized field linear
algebra and degree2 arithmetic in at most two variables. No hidden matrix
entry, random projective-scale matching or expensive symbolic factoring
is supplied.

## 5. Original-copy validation, including bad-coordinate attempts

Validation uses fresh ORIGINAL copies, not conic row membership. This is
essential: when B was singular, the row model is not justified. For the
explicit candidate G, implement its public uniform phase-state preparation
U_G and apply U_G^-1 to each original copy, accepting the all-zero
outcome. The probability is |<phi_G|phi_F>|^2. This inverse is of a known
candidate circuit, never the unknown source.

If G=aF for a!=0, then the probability is at least(1-4/p)^2: square a
changes nothing, while nonsquare a changes only the relative convention
at the at-most2/p zero fraction after a global sign.

For any nonproportional F,G with invertible quadratic parts and n>=3,
both are absolutely irreducible, since a product of affine linear forms
has quadratic-part rank at most2. Choose, for analysis only, a direction
v with both leading quadratic coefficients nonzero; one exists for p>4.
In complementary coordinates, each quadratic has a nonzero discriminant
polynomial of degree<=2, and their resultant is nonzero of degree<=4.
Gauss's lemma and constant nonzero leading coefficients justify these
nonvanishing claims. Except for at most8/p of transverse coordinates,
the product of the two line restrictions is squarefree degree4. Weil's
bound gives normalized character correlation at most3/sqrt(p). The bad
lines contribute8/p; padding on at most four roots contributes4/p. Thus

    |<phi_G|phi_F>| <= 3/sqrt(p)+12/p.                       (14)

For p>=256, true acceptance is>=3/4 and false acceptance<=1/4. The
stronger threshold p>=256T already implies this. A K-copy empirical mean
threshold1/2 therefore has error at most exp(-K/8) in either direction.
Reject candidates whose quadratic part is singular BEFORE this test.

## 6. Bounded resources and failure ledger

Let

    R=ceil(log2(8/eta)),  K=ceil(8 ln(8R/eta)),
    L=R(T-1+K).                                           (15)

Try at most R independently chosen coordinate matrices, each with T-1
training copies and at most K verification copies. Return the first
accepted candidate; otherwise ABORT. Generation fails on every attempt
with probability<=2^-R<=eta/8. Union bounds for any false acceptance and
for rejecting a generated true candidate cost at most eta/8 each. The
ideal total is at most3eta/8.

Uniform classical GL_n sampling is paid with capped rejection: use
J_P=ceil(log2(16R/eta)) matrix draws per attempt, since each has success
probability>=1/2. Draw uniform field entries by ceil(log2 p)-bit rejection,
with a per-entry cap ceil(log2(16 R J_P n^2/eta)). The two abort budgets
sum to at most eta/8. Successful draws retain the exact uniform laws.

Use the already paid binary-prefix uniform-interval construction for
F_p^* in (4), and approximate arbitrary-modulus QFTs for the Fourier step
and public candidate preparation. Compile all known unitaries with total
hybrid output error<=eta/8 over the at-most L copies; inverse-polynomial
per-operation error O(eta/L) requires only polynomially many precision
bits. Source copies remain exact. Total failure is then<=5eta/8<eta.
The copy count (15), feature storage O(T^2 logp), finite-field linear
algebra, public P inverses and all gate precisions are polynomial in
n,logp,log(1/eta). No amplitude amplification or quantum memory bank is
required.

## 7. Classical baselines, prior coverage and falsifiers

Corpus been-tried and baselines lookups preceded this derivation. Existing
Boolean quadratic/full-field-exponent attacks do not receive these signs
or these copies. Native chosen-sign-query line reconstruction DOES apply
with a random translated interpolation grid and common direction, subject
to explicit squarefree-line checks. Its full-table moment decoder costs
O(n^2 p) queries and O(n^3 p) field work. The affine leading character must
be recovered from moments, not incorrectly read as lambda(F(u)). A
four-template birthday composition additionally gives
O(n^2 sqrt(p)*poly(logp,logn,log(1/eta))) chosen queries, with an extra
factor n for explicit query assembly. Its mathematical proof is checked;
this extension has NOT been implemented or executed. The original saved
birthday code still covers monic irreducible lines only. Full derivation:
audits/reviews/2026-11-06-affine-quadric-classical-scope.md.

The stronger BIT/raw-phase model already has a polynomial quantum upper
bound from the existing univariate degree2 learner plus O(n^2) chosen
lines. This new claim concerns GLOBAL copies without a chosen-line source.
Classical signs are a different access model; no oracle-query separation
or classical hardness follows. Expected comparison is polynomial logp
versus the recorded native classical p or sqrt(p) dependence, not a
proved speedup. A worst-case classical poly(n,logp) affine sign learner
would solve every shifted-Legendre instance by simulating
F_s(x)=sum_i x_i^2+s with one L_s query, and reading s=c'/A'_11. A=I for
all s, including0. This is an oracle implication, not a hardness result
or a classical-to-copy-source reduction.

Russell--Shparlinski0212016 motivates character-polynomial learning and
mentions the multivariate extension at the query level. The locally read
CSV0705_2784 sphere/level-set sources and Roetteler0911_4724 Boolean
additive phases do not supply this source for free. These bounded checks
do not establish novelty or settle all published coverage.

The first scientific falsifier is an additional joint feature relation
or two nonproportional F with the same C(z); Sections3--4 rule both out
under the stated promises. The next fixed controls are n3,p7 and n4,p5,
A=I+vv^T with v=(1,1,0,...), b=(1,2,...,n), c=1. Check the complete ideal
joint-cone feature rank, reconstruct from its kernel, and compare actual
slice-lift amplitudes with the ideal ONLY as a source-law control. A
third n3,p7 coordinate guard has A=[[0,0,1],[0,1,0],[1,0,0]], whose leading
2-by-2 block is singular; it must not silently pass a B inverse.
All finite primes are BELOW the theorem threshold. No noisy-label rank
experiment, broad sweep or coherent circuit execution was performed.

## 8. Closed reviews and exact scope of validation

The independent reviewer read the complete 276-line version of this note,
Sections1--6, and accepted all quantified cases, constants, the original-
copy validator, per-attempt P resampling and the5eta/8 error ledger. The
parent independently checked the derivations and read the completed
classical scope note; the stronger written birthday bound is accepted with
the separate implementation limitation above. These are automated reviews,
not a human correctness/priority certificate.

The two prescribed good-coordinate cases give:

| p,n | Good slices | Joint ideal feature rank | Ideal good-cone mass | Actual good-cone mass |
|---|---|---|---|---|
| 7,3 | 7/7 | 17=T-1 | 1728/2401 | 0.6568691617 |
| 5,4 | 21/25 | 35=T-1 | 8064/15625 | 0.3760128 |

The decoder receives only the KERNEL-DERIVED matrix C and public field/
dimensions, and returns exactly -(A,b,c) in both cases. All4558 native
restriction-sign identities pass. Source norms retain the bad z slices;
the distance is precisely2(1-sqrt(1-1/p)), and the largest floating ideal
Fourier-amplitude discrepancy is below2.8e-17. The script's features use
2y_i y_j for off-diagonal entries, so kernel entries are directly symmetric
matrix entries; this is equivalent to the halving convention in Section3.

The singular-B control is an ANALYSIS-ONLY guard. It does not let the
receiver test a hidden determinant. The actual algorithm protects against
bad coordinates through original-copy validation and independent P retries.
Enumerating all ideal cone rows verifies algebra; it does not execute the
actual noisy-row learner or grant those rows as input. Artifacts:
classical_baselines/affine_quadric_slice_control.py/.json.

The native full-table baseline was run BEFORE the source controls: all220
signed squarefree F11 line quadratics decode from2420 sign queries, with
110 ambiguous S0=1 cases resolved by M4. A single F101,n3 affine instance
with zero critical value reconstructs exactly from ten lines/1010queries.
Reproduction: classical_baselines/affine_quadric_line_control.py. That
finite p101 is also below its stated genericity threshold; these checks
are exact algebra receipts, not evidence for the uniform success theorem.

The new operation is now accounted for. Next work must be selected by
external value, not by extending this to singular A, device noise, n2 or
smaller primes. The general poly(d,logp) native univariate question remains
open. No claim that random-slice homogenization removes its factorial
barrier has been made.
