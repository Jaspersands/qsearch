# Squarefree native character reconstruction

2026-11-05. Independently reviewed written extension of
LEGENDRE_RESULTANT_HYPERPLANE_READOUT.md; the prespecified zero/factor-pattern
falsifier is complete. No execution, novelty, speedup or classical-hardness claim.

## Question, model and reason for this pass

Can the coefficient-space receiver solve the native SQUAREFREE polynomial
reconstruction problem, including reducible inputs and their zeros, without
an extension-field oracle or an input-dependent zero indicator? This removes
the irreducibility restriction from the fixed-degree version of the problem
in Russell--Shparlinski, quant-ph/0212016, Theorem 6. That theorem supplies
query complexity through an unspecified POVM. Kopparty, arXiv:2601.07137,
Introduction and Algorithm A/Theorem 3.1, supplies a full-table classical
decoder and explicitly distinguishes the earlier quantum query result from
a fast implementation. Neither observation establishes priority here.

Input: fixed d>=2, growing odd prime p, unknown monic SQUAREFREE degree-d Q.
Write lambda(0)=+1 and lambda(z)=chi(z) for z!=0. The source supplies fresh
exact pure tensor copies of

 phi_Q=p^(-1/2) sum_x lambda(Q(x)) |x>.

An original trit oracle can prepare this with one query by applying the
known map 0->+1. A padded-bit oracle or an uncontrolled PADDED phase unitary
also supplies copies. The function chi(Q(x)) with zero amplitudes is NOT a
unitary phase oracle. The receiver is given no root flags or Q factorization.
Output Q, with failure<=eta. Resources sought: C_d poly(logp,log(1/eta));
there is no polynomial-in-d claim.

Portfolio decision: the native classical quadratic problem already contains
ordinary linear Legendre shift via the exact chosen-query reduction in
audits/reviews/2026-11-05-legendre-classical-reduction-review.md. Its padded
zero exception is repaired by fresh tests, not ignored. This is no hardness
proof, but supplies no new classical operation to investigate. Interleaved
OPI duplicates earlier work. The squarefree promise is a concrete missing
part of a published reconstruction problem and needs no new subsystem.

Corpus been-tried and baseline lookups found no exact prior construction;
the catalog failed to name a directly matching baseline, so primary sources
were inspected. Strongest relevant general classical comparator is Kopparty's
full p-query poly(p) Algorithm A, including zero padding as <=d corruptions.
For an explicit sufficient specialization of its PROVED Theorem 3.1 take
epsilon=1/16 and p>=(256d)^2. The introduction states a different constant
in its degree bound; do not substitute it for the algorithm's printed one.
The irreducible-cubic quasilinear window theorem is NOT automatically a
theorem about these reducible padded tables. Source/OPI distinctions and
the linear-to-quadratic reduction are in the scoped review above.

## Native state and virtual product algebra

Use exactly the paid circuit of the irreducible note: d copies, distinct
root projection, coherent sorting/permutation cleanup, a coherent uniform
a!=0 with phase chi(a)^d, and clean conversion to R=a product_i(X-x_i).
The distinctness flag succeeds with alpha=(p)_d/p^d. The actual normalized
state S_Q is supported on ALL squarefree completely split degree-d R,
with size N0=(p-1)binom(p,d). It retains unit phases even when R shares a
root with Q. No zero-dependent projection is performed.

For the proof only, factor Q=product_j Q_j with distinct irreducibles,
degrees d_j, and put A=F_p[X]/Q=product_j F_(p^d_j). Evaluation L_Q(R)
is a surjective linear map from F_p^(d+1) to A, with kernel span(Q).
The determinant norm satisfies Res(Q,R)=Norm_A/Fp(L_Q(R)). Hence

 c_Q(R)=chi(Res(Q,R))=product_j chi_(p^d_j)(R mod Q_j).

This is zero on nonunits. Put U=product_j(p^d_j-1). The VIRTUAL normalized
state N_Q has amplitudes c_Q(R)/sqrt(pU). It is never prepared, and its
factorization, CRT coordinates and hidden algebra are not supplied.

The Fourier transform of N_Q is supported in H=span(Q)^perp. Under the
dual CRT identification, a frequency is nonzero exactly when every field
component is nonzero. Thus exactly U frequencies have magnitude 1/sqrt(U),
all in H; the others vanish. This is the product of ordinary nontrivial
quadratic Gauss sums. For reducible Q, flatness on ALL nonzero H is false.

Let r<=d be the number of rational roots of Q. Exactly

 Ngood=(p-1)binom(p-r,d)

split polynomials R avoid them. On these R, actual and virtual phases
agree up to the single global sign chi(-1)^d. On the others the virtual
amplitude is zero. Therefore the EXACT overlap is

 gamma=|<N_Q,S_Q>|=Ngood/sqrt(N0*p*U).

In particular zero padding is handled directly by an overlap identity,
without a secret zero flag, an approximate replacement source or assuming
that the padded function is multiplicative at zero.

## Escape, reconstruction and resources

For any proper W<H, it contains at most p^(d-1) of the U supported
frequencies. Thus its virtual Fourier probability is at most p^(d-1)/U.
The same Cauchy--Schwarz argument as in the irreducible note gives

 Pr_(F S_Q)[y in H\W] >= [gamma-sqrt(p^(d-1)/U)]_+^2.

For p>=4d^2, Ngood/N0>=1/2 by a union bound on drawing a Q root without
replacement; alpha>=1/2 and N0/p^(d+1)>=1/(4d!). Also
U>=p^d(1-sum_j p^(-d_j))>=p^d(1-d/p)>=p^d/2. Since U<=p^d,
gamma^2>=1/(16d!). If p>=128d!, the escape bound is at least 1/(64d!).
Including the distinctness flag gives >=1/(128d!) per attempt. A block
of d fresh attempts therefore gives d independent inliers with probability

 q0=(128d!)^(-d).

Solve the d equations for their kernel line. Accept a candidate only when
rank is d, its last coordinate is nonzero, and its monic degree-d polynomial
is squarefree. The last test is gcd(Q_candidate,Q_candidate')=1; do NOT
retain the old irreducibility filter. On the all-genuine event it is Q.

For distinct monic squarefree degree-d Q,Q', the padded-copy inner product
is bounded by

 |<phi_Q',phi_Q>| <= [(2d-1)sqrt(p)+2d]/p.

To see the shared-factor case, let D=gcd(Q,Q'), degD=k, and
T=(Q/D)(Q'/D). This is nonconstant squarefree of degree 2(d-k). Outside
roots of QQ', the product of padded signs is chi(T). Common roots change
this comparison by at most 2 each and the remaining roots by at most 1
each, total <=2d. Apply Weil to T. For p>=256d^2 the bound is <1/4.

Consequently the full written theorem holds for every prime

 p>=P_d=max{128d!,256d^2}.

Use the irreducible note's entire paid seed, sampler, approximate interval
state/QFT, retry and verification ledger, with this q0 and the squarefree
candidate filter. In particular R=ceil((4/q0)ln(4/eta)),
K=ceil(ln(4R/eta)/ln8), block operator error<=q0/8 and per-test event error
<=min{1/16,1/(4K)} suffice. Fresh public-candidate projection accepts the
true padded state ideally with probability one and wrong states with
probability<=1/16. Copy cap R(d^2+K). One good public factorization seed
works for every supported R, independently of the secret Q. All exceptional
flags, input padding, random-sampling caps and clean workspaces remain paid.

## Decisive boundaries and finite falsifier

Squarefreeness cannot simply be dropped. For any two distinct monic
irreducible quadratics A,B, the degree-four polynomials A^2 and B^2 have
identical constant +1 character tables. This holds even with exact trit
access; more copies or better measurements cannot distinguish them.
At p5, A=X^2+2 and B=X^2+3 are explicit examples. A squarefree-kernel
output problem would be a different contract.

The prespecified control uses p11 and Q=X(X-1), X(X^2+1),
X(X-1)(X-2). First run native full-table candidate enumeration on trit
and padded-bit inputs, charging p queries and all candidate comparisons.
Then check actual padded source, exact overlap, U-point virtual spectrum,
every proper-subspace escape and failure of the old all-nonzero-H flatness
claim. Its scope is exact Sage field algebra plus floating FFT, not quantum
execution. Source/root cleanup is proved in the prior note, not simulated.
Files: classical_baselines/squarefree_resultant_control.py/.json.
Review: audits/reviews/2026-11-05-squarefree-resultant-review.md accepts
all-parameter CRT support, the native overlap, constants, shared-factor
verification and the reused complete resource ledger.

The three finite cases passed. Spectrum sizes are exactly 100,1200,1000;
maximum flatness residual <7e-18. The 12,133,133 proper hyperplanes satisfy
the bound; it is positive only for the quadratic (.01720584) and vacuous
for both cubics. The ordinary full-table baseline returns one trit candidate
in every case and respectively 1,1,2 padded candidates. The last case gives
an EXACT small-prime padded collision:

    p=11,
    Q=X^3+8X^2+2X = X(X-1)(X-2),
    Q'=X^3+4X^2+10X+5  (irreducible).

Both are monic squarefree cubics with the same entire padded table; trit
access distinguishes them. Thus even irreducibility/factor type cannot be
inferred from that padded source at p11. This is outside the proved prime
threshold, and independently falsifies an unqualified small-prime fallback.
The p5 repeated-factor counterexample also passed exactly. None of these
finite checks execute the coefficient encoding or quantum measurement.

The separate LEGENDRE_CORRUPTED_CHARACTER_READOUT.md now proves a reviewed
extension to one fixed sign function corrupted on any fixed fraction
rho<1/4 of points, using fresh pure copies and statistical verification.
This clean-source note itself makes no growing-degree, small-prime-universal,
mixed-state or correlated-bank claim. No classical lower bound or
novelty follows from source searches, accepted reviews or finite controls.
Next hard question: can a specified robust receiver handle fixed corrupted
character tables with fresh pure copies, with paid verification? Compare
that concrete extension against independent high-upside directions first;
do not add generic source/noise infrastructure.
