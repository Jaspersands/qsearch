# One-sample Hankel readout for native character reconstruction

2026-11-05. Independently reviewed written uniform parameterized algorithm.
It runs in exp(O(d log d)) times a polynomial in the
remaining input parameters. It is NOT polynomial in d, a novelty claim,
a classical separation, or an executed quantum algorithm.

## Scientific contract and the new operation

Let p be an odd prime and Q in F_p[X] an unknown monic squarefree polynomial
of degree d>=2. Unlike the earlier fixed-degree statements, d is an input
parameter here. The source supplies fresh pure tensor copies

    |phi_F>=p^(-1/2) sum_x F(x)|x>,  F:F_p->{+1,-1}.

In the clean case F=lambda composed with Q, where lambda(0)=+1 and
lambda(z)=chi_p(z) otherwise. In the robust case ONE FIXED F disagrees
with this padded table at at most rho*p positions, for public
0<=rho<1/4 and kappa=1-4rho. A coherent BIT oracle or uncontrolled padded
raw phase unitary supplies one copy per query. No extension-field oracle,
unknown preparation inverse, root flags or hidden factorization is given.
Mixed/device noise, varying masks and correlated banks are outside the model.

The new operation uses m=2d-1 native copies and encodes a public split
polynomial R of degree m. A Fourier outcome has 2d coordinates. On the
support of a VIRTUAL comparison state, these are trace moments of Q's
quotient algebra. ONE such outcome determines Q by an invertible d-by-d
Hankel system. This replaces the previous requirement for d independent
good hyperplane samples. It also removes the subtraction of proper-subspace
mass from the success proof: the entire virtual support is decodable.

The clean all-flags success bound per attempt is 1/(32m!). With fixed
corruptions it is 1/(32*36^m*m!). Public postprocessing, source conversion,
factor erasure and Fourier gates have polynomial cost in d and log p.
The resulting total cost is exp(O(d log d)), with only a polynomial prime
threshold. This removes the older exp(O(d^2 log d)) block-retry dependence
and factorial prime threshold; it does not remove the split-mask factorial.

The external problem is the published native character reconstruction
query/time gap. Corpus been-tried found related Prony/recurrence primitives
but no exact native composition; a textual search is not a novelty result.
Prony/Hankel reconstruction from 2d supplied moments is known. See
audits/sources/legendre_prf/kaltofen_prony_2022.txt, opening discussion,
and the existing Cayley--Hamilton/Hankel recurrence bridge in the repository.
The work here pays those moments from ORIGINAL character-only copies and
proves their source probability. Childs et al., arXiv:1509.09271, Theorem 3,
uses full FIELD-VALUE polynomial queries; that oracle is not available here.
Its fixed-degree efficient interpolation result cannot be imported as a
character-query decoder. Russell--Shparlinski supplies an O(d)-query POVM,
not this circuit. No primitive or overall priority claim is made.

## 1. Paid degree-m split coefficient source

Take m copies of phi_F and project onto distinct x_1,...,x_m. This succeeds
with alpha=(p)_m/p^m, since every F(x) is a sign. Reversibly sort and retain
the permutation rank. The symmetric phase product makes that rank an
independent uniform state on m! labels; unprepare it without postselection.
Append a coherent uniform a in F_p^* with the PUBLIC phase

    chi_p(a)^d,

where d is the TARGET degree, not the number m of roots. Form the coefficient
vector of R=a product_i(X-x_i), in ascending order. Erase the canonical
roots using the paid public factorization inverse described below. The
resulting normalized state is supported on all squarefree completely split
degree-m R, a set of size N_m=(p-1)binom(p,m), with phase

    chi_p(a)^d product_i F(x_i).

The target-degree exponent is essential. The resultant identity is

    Res(Q,R)=(-1)^(dm) a^d product_i Q(x_i).

Because m=2d-1 is odd, the global sign is chi_p(-1)^d. Blindly calling an
m-copy helper that uses chi_p(a)^m gives the wrong source for even d.
It cannot be repaired by renaming an exponent in the probability analysis.

All source-conversion operations are uniform in m. Compute m!, rank and
unrank permutations using their Lehmer codes in poly(m) integer operations
on O(m log m) bits. Prepare the uniform rank state on [0,m!-1] with binary
prefix-count rotations, not a hardcoded circuit or an enumerated m! table.
This realizes the exact ideal tensor-factor removal with polynomial-size
approximation circuits. Polynomial multiplication maps roots to coefficients
in polynomially many field operations.

For clean root erasure use the previous public-shift procedure: L independent
uniform shifts, L=ceil(log2(8p^2/eta)), distinguish every pair of field
elements by their Legendre trit signatures with failure<=eta/16. Gcds with
X+t_j and (X+t_j)^((p-1)/2) +/-1, taken modulo the current public factors,
split EVERY supported degree-m R into linear factors on that one good-seed
event. The number and sizes of operations are polynomial in m,log p,L.
Canonical sorting then permits reversible root erasure. The factorization
is of PUBLIC R, never hidden Q. Bounded uniform shift sampling retains the
previous <=eta/8 ABORT budget. No domain-sized signature table is stored.

## 2. Virtual quotient-algebra Fourier law

For the proof only, let A=F_p[X]/Q, theta=X mod Q. Squarefreeness makes
A a product of fields F_(p^d_j). Put U=product_j(p^d_j-1). The linear map

    L_Q: V_m=F_p^(m+1) -> A,  coeff(R) |-> R(theta)

is surjective, with kernel Q times all polynomials of degree<=m-d.
The kernel has dimension m+1-d. The virtual normalized state is

    |N_Q>=[p^(m+1-d)U]^(-1/2)
           sum_R chi_p(Res(Q,R)) |coeff(R)>.

It is never prepared. Its norm character is the product of the nontrivial
quadratic characters on the field components and vanishes on nonunits.
The additive Fourier transform of N_Q is supported on H=(ker L_Q)^perp.
With the nondegenerate trace pairing, every frequency there has a unique
description

    y_j=Tr_(A/Fp)(t theta^j),  0<=j<=m,  t in A.

Either Fourier sign convention gives the same set (replace t by -t).
Exactly the unit t contribute: all field components of t must be nonzero.
The component Gauss sums and kernel normalization give magnitude 1/sqrt(U)
on these U frequencies and zero elsewhere. This proves a Fourier law;
it does not supply A, theta, t, Q's factors or an extension oracle.

## 3. Every virtual supported outcome determines Q

Given a measured y=(y_0,...,y_(2d-1)), form

    H_y=(y_(i+j))_(0<=i,j<d),
    v_y=(y_d,...,y_(2d-1))^T.

If H_y is singular, abort this attempt. Otherwise solve q=-H_y^(-1)v_y
and construct C=X^d+sum_(j=0)^(d-1) q_j X^j. Keep it only if squarefree.
This is polynomial-time finite-field linear algebra and a public gcd check.

For a virtual supported frequency, H_y is the Gram matrix in the basis
1,theta,...,theta^(d-1) of

    B_t(a,b)=Tr_(A/Fp)(tab).

The trace pairing of an etale algebra is nondegenerate. Multiplication by
the unit t is invertible, so B_t and H_y are nondegenerate. Moreover
Tr(t theta^i Q(theta))=0 for i=0,...,d-1, giving exactly
H_y*(Q_0,...,Q_(d-1))^T=-v_y. Hence the public decoder returns Q on EVERY
virtual supported label, including arbitrary squarefree factor patterns.
Nonunit t can give singular Hankel matrices; they have zero virtual mass.
The proof needs the unit/cyclicity condition, not merely Cayley--Hamilton.

Let D_Q be the set of measured labels whose Hankel decoder actually returns
Q. It is an analysis event, not an available target-dependent predicate.
The support of F N_Q is contained in D_Q. Thus for the actual encoded state S,

    Pr_(F S)[D_Q] >= |<F N_Q,F S>|^2 = |<N_Q,S>|^2.

This bounds CORRECT decoding, not the probability that a random Hankel
matrix is nonsingular. Nonsingular outcomes returning a wrong polynomial
are handled by verification. No inlier recognizer is supplied.

## 4. Clean success and polynomial field threshold

Let r<=d be the number of rational Q roots. Exactly
N_good=(p-1)binom(p-r,m) supported R are coprime to Q. On those R the
clean source phase and virtual phase agree up to the single global sign;
on other R the virtual amplitude is zero. The exact squared overlap is

    gamma_clean^2=N_good^2/[N_m p^(m+1-d) U].

For p>=256d^2, alpha>=1/2, and N_good/N_m>=1/2: a uniform distinct
m-tuple hits a root of Q with probability at most mr/p. Also U<=p^d and
N_m/p^(m+1)=(1-1/p)alpha/m!>=1/(4m!). Therefore

    gamma_clean^2>=1/(16m!),
    Pr[distinctness flag AND decode Q]>=1/(32m!).

The true prime threshold is polynomial in d. There is no proper-subspace
escape subtraction requiring p to exceed a factorial. The factorial remains
in the split-source density and therefore the number of repetitions.

## 5. Fixed corruptions: a uniform signed-moment bound

For the same one fixed corrupted F as in the robust contract, let n=p-r
and B be the number of corrupted nonroot positions. The overlap magnitude is
gamma_clean times the absolute value of

    E_m = sum_j (-1)^j binom(B,j)binom(n-B,m-j) / binom(n,m).

Errors at Q roots do not contribute to this overlap. They are retained in
the actual source and are covered separately in verification. Put S=n-2B.
The generating polynomial (1+z)^(n-B)(1-z)^B shows that normalized signed
subset moments E_k satisfy

    E_0=1, E_1=S/n,
    (n-k)E_(k+1)=S E_k-k E_(k-1).

At p>=4d and rho<=1/4, S/n>=1/3. If n>=36m, inductively every ratio
R_k=E_k/E_(k-1) is positive and >=1/6: the base ratio is >=1/3, and

    R_(k+1)=(S-k/R_k)/(n-k)
           >=(n/3-6k)/(n-k)>=1/6   for k<=n/36.

Consequently E_m>=6^(-m). This direct recurrence is stronger than using
an absolute IID-coupling error; it needs only polynomial n in m. The
condition p>=256d^2 implies n>=p-d>=36m for every d>=2. We obtain

    Pr[distinctness flag AND decode Q]>=1/(32*36^m*m!).

The small-field Krawtchouk cancellation examples remain valid outside these
conditions. No independence of error positions or averaging over masks is
assumed. This is uniform over EVERY fixed F within the promised radius.

## 6. Verification, total resources and active memory

Use the statistical public-candidate verifier already proved in
LEGENDRE_CORRUPTED_CHARACTER_READOUT.md. With kappa=1-4rho,

    p>=max{256d^2,64d^2/kappa^2}

ensures true candidate acceptance probability at least beta^2,
beta=1-2rho, and wrong candidate acceptance at most 1/4. The latter follows
from the shared-factor Weil correlation bound plus 2rho changes. Set
Delta=beta^2-1/4 and tau=(beta^2+1/4)/2. For clean input one may take
rho=0 and the cleaner generation bound.

Set q0=1/(32m!) in the clean case, or 1/(32*36^m*m!) in the robust case.
Allocate total generation-circuit operator error<=q0/8 per attempt, so
the true candidate probability remains >=q0/2. Choose

    R=ceil((2/q0)ln(4/eta)),
    K=ceil((8/Delta^2)ln(8R/eta)).

At most R attempts are made. Each verification uses K NEW source copies;
accept when its empirical projection mean is >=tau. Per-test event error
<=Delta/8 and threshold rounding error<=Delta/8 retain the Hoeffding margin.
Missing all true candidates costs <=eta/4; all classification errors cost
<=eta/8; public seed failure and capped samplers cost <=eta/16 and eta/8.
The total is <=9eta/16. Approximate gates are already included in these
event bounds, not counted twice. Copies are capped by R(m+K), not R(d^2+K).
The verifier uses the inverse preparation of PUBLIC candidate states only.

Reversible permutation ranking, uniform interval states, polynomial
arithmetic, public root erasure, the m+1 arbitrary-modulus QFTs and the
Hankel solve have gate-generation and execution cost polynomial in
d,log p,log(1/eta),log(kappa^(-1)) and the requested precision. Kitaev's
paid approximate QFT and all input-padding rules are unchanged. Generation
precision has log(q0^(-1))=O(d log d); it does not create exponential
precision bit lengths. Verification has polynomial kappa^(-1) sample cost.
Consequently total gates and copies are

    exp(O(d log d))*poly(log p,kappa^(-1),log(1/eta)).

ACTIVE quantum and classical workspace is polynomial in these bit/degree
parameters. Request only the m copies for the current attempt; after the
Fourier measurement keep its classical candidate and request verification
copies sequentially. Do not retain R attempts or a bank of all future copies.
Public seeds occupy O(L log p) bits; permutation ranks occupy O(m log m);
root/polynomial workspaces and reversible histories are polynomial; retry
counters need O(log R) bits. No table of p values, m! permutations or all
candidate polynomials is stored. The large resource is TIME/repetitions.

## Classical comparison, falsifiers and current status

The native F problem and classical access have not changed. Kopparty's
full-table poly(p) decoder applies below its proved approximately 1/8
radius and degree condition; it is not extended here to 1/4. Throughout
rho<1/4, classical empirical exhaustive decoding uses poly(d,log p,
kappa^(-1),log(1/eta)) BIT queries and p^d candidate enumeration. Earlier
quasilinear cubic and sqrt(p) quadratic attacks retain their exact promises.
These are upper bounds, not hardness. No classical value queries are
silently supplied in the phase-copy-only model. The baseline campaigns
were reused because the native input/target is unchanged.

Required falsifiers: the scalar exponent must use TARGET d; every virtual
unit label must give invertible Hankel and the correct Q; nonunit/cyclic
failure must not be ignored; actual success must count D_Q, not all
nonsingular outcomes; the m! density and every source flag must remain
charged. The prespecified finite control checks these on five small clean
and corrupted cases. It does not simulate coherent source preparation or
the full quantum circuit and cannot prove the asymptotic theorem.

Independent review accepted the actual complete note and resource ledger:
[review](audits/reviews/2026-11-05-hankel-resultant-review.md).
The [control](classical_baselines/hankel_resultant_control.py) and
[artifact](classical_baselines/hankel_resultant_control.json) cover exactly
four clean sources and one fixed corrupted source. Their virtual support
sizes are 16,24,288,342; every supported label has full Hankel rank and
returns Q, while every virtual zero inside the annihilator is singular.
Actual Q-decoding mass exceeds the exact squared-overlap bound in each case.
Both quadratic cases have zero comparison overlap if the old chi(a)^m
phase is left uncorrected; omitting the correction chi(a)^(d-m), not
literally omitting chi(a)^d (which is 1 for even d), is the negative control.
The p7 mixed-cubic single-flip source has exact E5=-2/3.

All five finite sources have some wrong candidate with public projection
score 1. The corrupted cubic table is exactly another polynomial's padded
table, so its true Q is not even a nearest-table candidate. Every tested
prime is below the theorem threshold. These are algebra/overlap controls
and explicit small-prime identifiability failures, not demonstrations of
the complete verifier or asymptotic success. Exact field/rank/solve algebra
and floating FFT were used; no coherent circuit was run.

Primary sources used for the known-primitive and access-model checks are
[Kaltofen, Sparse Polynomial Hermite Interpolation (2022)](https://users.cs.duke.edu/~elk27/bibliography/22/Ka22herm.pdf)
and [Childs et al., Optimal quantum algorithm for polynomial interpolation](https://arxiv.org/abs/1509.09271).
Their local texts are kaltofen_prony_2022.txt and
optimal_interpolation_1509_09271.txt under audits/sources/legendre_prf/.
Kopparty's [noisy polynomial reconstruction paper](https://www.math.toronto.edu/swastik/weil-decoding.pdf)
records the native character query/time distinction; its proved algorithm
and degree constants remain as audited in the classical reduction review.

The operation is admitted after corpus/primary checks, with no novelty
conclusion. The next uniform-polynomial question remains how to remove the
split-mask factorial with a genuinely new paid source/readout. Compare that
specific operation with independent directions before further extension;
this recurrence operation alone does not solve it. No generic infrastructure
or broad sweep is warranted.
