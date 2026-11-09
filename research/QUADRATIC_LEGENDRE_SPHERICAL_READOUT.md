# Quadratic Legendre two-copy spherical readout

2026-11-05. Independently reviewed WRITTEN polynomial-time quantum
composition for the stated growing-prime BIT-oracle reconstruction problem.
It uses the GL2 QFT toolbox Theorem 6.1 and Xi's Jacobi-moment theorem as
source theorems; their relevant assumptions and conventions were checked.
The final corollary also accepts fresh ordinary phase copies or an
uncontrolled raw phase oracle, with all copies and verification charged.
No compiled/executed receiver, novelty, speedup, separation or classical
hardness is claimed. The complete independent review is
audits/reviews/2026-11-05-legendre-receiver-review.md.

## Scientific contract and selection

The native input is a coherent bit/XOR oracle for
`g(x)=chi(x^2+b*x+c)` over a growing odd prime field F_p, with the monic
quadratic promised irreducible. Recover (b,c), then verify with fresh native
queries. Input length is O(log p). No extension-field oracle, target basis,
inverse map, supplied hidden advice, or uncharged postselection is available.
The homogeneous lift on P1 has h(infinity)=1 and sum h=0; its bit-oracle
implementation is paid in QUADRATIC_LEGENDRE_MATRIX_COSETS.md. This note
does not silently extend that lift to an uncontrolled raw phase oracle.

Repository been-tried and baseline lookups preceded this pass's literature
comparison. The retained native classical birthday attack costs expected
O(sqrt(p) polylog(p)) queries, time and storage; its six saved controls and
moment attacks are unchanged. The earlier quantum comparator
uses Kuperberg in 2^O(sqrt(log p)) time/queries/quantum space. Finite failures
of classical attacks establish no hardness. See QUADRATIC_LEGENDRE_RECOVERY.md.

The alternative considered was a classical cluster sampler for full-table
scalar OPI. The positive graphic/cographic mixing theorem of Hangleiter,
Ju and Vazirani does not cover the signed, frustrated native Fourier lift;
no new paid classical operation or general mixing obstruction was obtained.
The present direction is selected because a concrete spherical transform
could remove the previously unpaid collective-readout polar decomposition.

Mechanism: prepare two homogeneous phase copies; use the split
and nonsplit torus-normalizer permutation modules; retain principal-series
components; implement their scalar phases using Gauss/Jacobi phase circuits;
invert the nonsplit spherical transform and measure a quadratic. The sections below establish polynomial gate/query cost in log(p) and
log(1/eta), with bounded failure eta. The complete independent review
accepted retained mass, explicit basis conversion, coherent cleanup,
precision and retries after the recorded corrections. This is a written
upper bound, not a comparison theorem against the best classical algorithm.

## Exact geometric reduction

Let G=PGL2(F_p), Omega_s be the unordered pairs of distinct points of
P1(F_p), and Omega_n the unordered Frobenius-conjugate nonrational pairs.
The latter are exactly the monic irreducible quadratics. Their sizes are
N_s=p(p+1)/2 and M=p(p-1)/2. Their stabilizers are the split and nonsplit
torus normalizers, of orders 2(p-1) and 2(p+1), respectively.

Define the N_s by M real matrix

    T[{x,y},Q] = h_Q(x) h_Q(y).

Two homogeneous phase copies, projected onto x!=y and folded into the
unordered-pair basis, give T[:,Q]/sqrt(N_s), with success p/(p+1).
The discarded diagonal branch is independent of Q. Under projective
coordinate changes h can acquire a global quadratic-character sign, but
the two-copy product removes it. Thus T is an ordinary G-intertwiner.
For each x, sum_{y!=x} T[{x,y},Q]=-1, so the image has no ordinary
Steinberg vertex-star difference component. Its column sum is -(p+1)/2;
its row sum is -(p-1)/2.

Let C be the 0/1 incidence matrix: C[{x,y},Q]=1 precisely when the
rational lines x,y are orthogonal for Q. Let D be the split harmonic-pair
adjacency matrix: at {0,infinity}, its neighbors are {a,-a}, a!=0, modulo
sign. Then the following identity is exact:

    T = 2 D C - J.                                      (1)

Proof: at {0,infinity}, write Q=X^2+bX+c. The lines a,-a are orthogonal
iff a^2=c. There is one unordered pair when c is a square, and none when
c is a nonsquare. Irreducibility excludes c=0. Hence
(DC)[{0,infinity},Q]=(1+chi(c))/2 and T[{0,infinity},Q]=chi(c).
Transitivity and equivariance establish (1) at every entry.

Chen's split/nonsplit correspondence relation, on each nontrivial common
irreducible constituent rho, gives C C*=p I-D^2. Consequently

    eigenvalue_rho(T*T)=4 d_rho^2 (p-d_rho^2),             (2)

where d_rho is the eigenvalue of D. The permutation modules are
multiplicity-free and C[Omega_s]=C[Omega_n] plus the ordinary Steinberg
representation. The representation/source details are checked in
audits/reviews/2026-11-05-legendre-spherical-identity-review.md.
The trivial eigenvalue of T*T is (p^2-1)/4, directly from the row/column
sums. Full rank, even if established, does not bound the smallest singular
value by an inverse polynomial in log(p).

## Principal-sector identities

For an even multiplicative character alpha, alpha^2!=1, use the
principal series Ind_B^G(alpha,alpha^-1), with alpha and alpha^-1
identifying the same irreducible representation. It has dimension p+1.
Choose a PUBLIC nonsquare lambda. In its induced P1 model unit normalizer-fixed vectors are

    v_s(z)=alpha(z)^-1/sqrt(p-1), z in F_p^*,
    v_s(0)=v_s(infinity)=0;
    v_n(z)=alpha(z^2-lambda)^-1/sqrt(p+1), z in F_p,
    v_n(infinity)=1/sqrt(p+1).

These vectors have explicit public arithmetic/character descriptions.
The actual Fourier-basis preparation is specified below. First define the
fixed-vector overlap scalar

    m_alpha = sqrt(p^2-1)/2 <v_s,v_n>
            = (1/2) sum_{z!=0} alpha(z/(z^2-lambda)),      (3)

The forward incidence scalar in the convention used below is its
CONJUGATE. Chen Proposition
9.3 gives

    d_alpha=(1/2) sum_{z!=0} alpha(z) chi(1+z^2).          (4)

With beta^2=alpha and J_beta=J_p(beta,chi), the independently checked identities are

    d_alpha=beta(-1) Re J_beta,
    m_alpha=i beta(-1) beta(4 lambda)^-1 Im J_beta,
    z_alpha=2 d_alpha m_alpha
             = beta(4 lambda)^-1 (J_beta^2-conj(J_beta)^2)/2. (5)

The actual forward T scalar is tau_alpha=conjugate(z_alpha). All relevant
nonexceptional Gauss/Jacobi characters are nontrivial, so |J_beta|=sqrt(p).
The successful receiver applies conjugate(tau_alpha)/p; its two-phase LCU
and exact normalization are specified below. No polar inverse is used.

The mass theorem established below is

    sum_principal (p+1) 4 d_alpha^2(p-d_alpha^2)
      =p^4/8+O(p^(7/2)).                                  (6)

The sum is over distinct nonexceptional principal irreducibles. Its
constant diagonal makes the receiver probability uniform over every
hidden quadratic, rather than merely an average over secrets. Cuspidal
state preparation is not assumed: only a coarse principal flag is
measured, retaining coherence between all admitted representation labels.

## Decisive controls and sources

Exact Sage controls for p=3,5,7,11,13 give full column rank of T and Gram
characteristic polynomials, respectively:

    (x-2)(x-8)^2
    (x-6)(x-16)^9
    (x-12)(x-48)^8(x^2-32x+128)^6
    (x-30)(x-72)^10(x-96)^20(x^2-80x+1280)^12
    (x-42)(x-48)^14(x-144)^27(x^3-208x^2+6656x-4096)^12

These are identity falsifiers only; no decoder or asymptotic guarantee was
executed. The small p13 cubic root warns against assuming conditioning.

Primary sources, downloaded in audits/sources/legendre_prf/:

- Imin Chen, On relations between Jacobians of certain modular curves,
  https://arxiv.org/abs/math/9809209, especially Sections 8-10.
- Anthony C. Kable, Legendre sums, Soto-Andrade sums and Kloosterman sums,
  Pacific J. Math. 206 (2002), 139-157,
  https://msp.org/pjm/2002/206-1/pjm-v206-n1-p09-s.pdf.
- The quantum Fourier transform toolbox, https://arxiv.org/abs/2608.28573,
  especially principal induced/GT models and coherent Gauss phases.
- Peter Bruin, Quantum computation of Kloosterman sums,
  https://arxiv.org/abs/1807.03600. Preparing the full Kloosterman state is
  not a free individual-value or individual-phase oracle.

Decisive falsifiers included an incorrect QFT basis, wrong conjugation,
hidden subgroup workspace, or a vanished principal mass. The reviews
resolved these for the written composition; exact wrong-conjugation
controls fail. A stronger classical native reconstruction remains open.

## Constructive update: bounded adjoint, no polar inversion

The following is the independently reviewed composition. The mass bound
uses a primary-source theorem; no conditioning theorem is needed.

**Moment bound.** Ping Xi, Equidistributions of Jacobi sums,
https://arxiv.org/abs/1809.04286, Theorem 1.3 and its Section 3.1 proof,
give, with quadratic chi fixed and beta ranging over all characters other
than 1,chi,

    |sum_beta J(beta,chi)^4| <= 12 p^(5/2).

The theorem explicitly permits the empty conjugate tuple (s=0). Remove
also beta^2=chi if present (at most two characters). Each nonexceptional
even principal irreducible is represented four times by beta:
beta, beta*chi, beta^-1, beta^-1*chi. The scalar squared is invariant on
that orbit and equals p^2/2-Re(J_beta^4)/2. Thus its principal trace A is

    A = sum_principal (p+1)|tau_alpha|^2
      = p^4/8 + O(p^(7/2)),
    A >= (p+1)p^2 (p-7-12 sqrt(p))/8.                   (8)

For all primes p>=625, A>=p^3(p+1)/16. The exact exceptional-label and
source checks are in the independent principal-mass review. This is an
asymptotic theorem application, not an inference from the finite Gram data.

**Fourier convention and scalar.** Fix the convention
F_G|g>=sum_{rho,i,j} sqrt(dim(rho)/|G|) rho(g)_{ij}|rho,i,j>.
A uniform left coset gH maps, on a rank-one H-invariant component, to
sqrt(dim(rho)/[G:H]) rho(g)v_H tensor conjugate(v_H). Hence the forward
incidence scalar is the CONJUGATE of (3). The actual forward T scalar is
the conjugate of the right side of (5). The receiver scalar is therefore

    conjugate(tau_alpha)/p
      = beta(4 lambda)^-1 [j_beta^2-j_beta^-2]/2,
    j_beta=J(beta,chi)/sqrt(p).                          (9)

Changing beta to beta*chi leaves (9) unchanged. Using the unconjugated
forward scalar in the receiver is an explicit falsifier. Right-register
fixed vectors must be conjugated IN THE GT BASIS, not only by conjugating
their induced-basis character amplitudes.

**Paid partial spherical transforms.** Use GL2 rather than assuming a
separate PGL2 circuit. Both subgroups contain the center, so only central
trivial representations occur. H_s consists of diagonal/antidiagonal
invertible matrices, order 2(p-1)^2. H_n consists of matrices
[[a,lambda*b],[b,a]], (a,b)!=0, and their products with diag(-1,1),
order 2(p^2-1). Their uniform states use a uniform bit and either two
nonzero field elements or one nonzero extension-field element.

The split coset representative is the matrix whose columns are the
canonical projective representatives of its two sorted rational points.
The inverse maps g to {g(infinity),g(0)} and h=r_R^-1 g in H_s.
For Q=(X-z)^2-d with d nonsquare, choose the canonical square root
r=sqrt(d/lambda) and use r_Q=[[r,z],[0,1]]. It maps the anchor roots
plus/minus sqrt(lambda) to Q's roots. Given g=[[a,b],[c,d]], put
den=d^2-lambda*c^2, z=(b*d-a*c*lambda)/den,
w=(a*d-b*c)/den. The target quadratic is (X-z)^2-lambda*w^2.
The denominator and w are nonzero. This supplies the inverse coset label
and then h=r_Q^-1 g. Uniform subgroup registers can therefore be erased
by reversible public arithmetic in both directions.

The toolbox Theorem 6.1 supplies the approximate GL2 QFT, with operator
norm error epsilon and gate size poly(log p,log(1/epsilon)). Its principal
model is I_{alpha,alpha^-1}, with the explicit vectors above: Equations
(79)-(81) fix the cocycle. Evenness removes the infinity-chart sign.
Equation (97) gives its GT basis as infinity, the finite additive zero
mode, and the multiplicative Fourier transform of the nonzero additive
modes after multiplying by alpha. This basis conversion uses additive
and multiplicative QFTs and public character phases, all polylogarithmic.
Explicitly, v_t=p^-1/2 sum_x conjugate(psi(tx))|x> and
w_delta=(p-1)^-1/2 sum_{t!=0} delta(t)alpha(t)|v_t>.
The conjugation bars were verified on ORIGINAL PDF page 32: pdftotext
drops them and would suggest the wrong additive sign. If C_alpha has
these GT vectors as its columns in the induced basis, prepare
C_alpha^dagger v_H for the carrier and its complex conjugate for the dual.
Use the first label of the actual canonical pair (A,B) as alpha=A,
B=alpha^-1; do not substitute the equivalent inverse representation
without its intertwiner. This label order was corrected during review.
For the right dual register use the COMPLEX CONJUGATE of this entire
state-preparation/conversion circuit. Its inverse unprepares the actual
conjugate(v_H) without unknown label-dependent phases.

Consequently: coset embedding -> GL2 QFT -> coarse principal flag ->
controlled unpreparation of the right invariant vector implements the
partial spherical transform, preserving coherence among principal labels.
Reverse the process with H_n to synthesize a quadratic label. The image
after the diagonal operation remains in the corresponding nonsplit module;
no secret-dependent inverse or extension-field query is used.

**Bounded adjoint receiver.** The toolbox Theorem 6.9 supplies clean
coherent normalized Gauss phases Gamma. On these nonexceptional labels,
j_beta=Gamma(beta) Gamma(chi) Gamma(beta*chi)^dagger. All three characters
are nontrivial. A one-qubit LCU of j_beta^2 and -j_beta^-2, followed by
the public phase beta(4 lambda)^-1, implements (9) in its successful block.
The normalization is p, not p times a hidden conditioning factor.

Apply that block between the split partial transform and the inverse
nonsplit partial transform. On input T[:,Q]/sqrt(N_s), the joint amplitude
for a successful flag and the correct Q is

    A / (p M sqrt(N_s)).                               (10)

This follows from the constant diagonal of each transitive-module
projector, dim(rho)/M. Squaring (10) gives the joint probability; there is
no renormalization by the principal or LCU success probabilities. By (8),
it is at least p(p+1)/(32(p-1)^2) for p>=625. Including the off-diagonal
preparation probability gives at least p^2/(32(p-1)^2)>1/32. It tends to
1/8. The independent end-to-end review accepted the precisely specified
composition, with its bounded approximation/retry budget below.

**Resources and verification.** Public generator finding,
factoring p-1, discrete-log coordinate changes, a public nonsquare, canonical
square roots, QFT precision and uniform-state preparation all use bounded
preprocessing and clean ancillas. These use known polynomial quantum/field
arithmetic, not an oracle for Q. Two native bit queries make each ideal
two-copy state. Different irreducible quadratics have agreement probability
at most (1+3/sqrt(p))/2 under a fresh uniform field query, by the degree-four
Weil bound. Thus repeated candidate verification and bounded independent
attempts can amplify a constant correct-output bound. The next section supplies exact retry and precision budgets and
small-prime handling. The source theorem assumptions were checked; no
stronger classical same-oracle upper bound is established here.

## Explicit total error and resource budget

For p>=625 and target failure 0<eta<1/2, set

    R = ceil(64 log(4/eta)),
    K = ceil(log(4R/eta)/log(25/14)).                     (11)

Use at most R attempts. Each uses two native bit queries for the phase
copies. Abort that attempt if the distinct-pair, principal, or LCU flag
fails. Otherwise reject invalid padded encodings with ABORT, decode its valid
irreducible quadratic label, and compare with
K independent uniformly random native oracle queries. Return the first
candidate passing all K; if none passes, return ABORT. Each returned true
candidate passes exactly. For any wrong candidate, condition on the full
preceding transcript; the newly chosen verification inputs are still
independent and its agreement probability is at most 14/25. Therefore
the probability that ANY wrong candidate passes is at most
R(14/25)^K<=eta/4, including adaptive stopping. Generate each verification
input by exact classical rejection from ceil(log_2 p) random bits, capped
at L=ceil(log_2(8RK/eta)) proposals. The failure probability per draw is
at most 2^-L. Abort on any exhausted draw; the total additional abort
probability across at most RK draws is <=eta/8. Conditional accepted
inputs are exactly uniform. No approximate quantum sampler is substituted.

Compile the full unitary dilation of each attempt, including approximate
uniform preparations and coherent discrete-logarithm computations, with
operator-norm error at most 1/256. Intermediate flags can be deferred;
ideal-versus-actual event probability differs by at most 1/128 under this
conservative norm bound. The ideal correct-candidate event is >1/32, so
each actual fresh attempt has correct-candidate probability >=1/64.
No extra approximation-failure union term is needed: this reduction in
the per-attempt bound already charges the error. Thus the probability
that all R attempts miss the true candidate is <=exp(-R/64)<=eta/4.
An early false acceptance belongs to the separately charged event above.

Public preprocessing is capped with total abort probability <=eta/4:
quantum factor p-1 and p^2-1, certify the returned factorizations, and
sample primitive generators with their usual power tests against every
distinct prime factor. A cyclic group of order N has primitive-element
density phi(N)/N>=1/(1+log_2 N): if it has k distinct prime factors,
the i-th is at least i+1, giving a product at least 1/(k+1).
O(log N log(1/eta)) capped trials therefore suffice. All accepted public
parameters are checked, so failures cannot silently become bad advice.
Choose the public nonsquare lambda to be an initially certified primitive
generator of F_p^*. The quadratic extension is F_p[sqrt(lambda)]. Once
its primitive generator h is found, set g=h^(p+1)=Norm(h) and use THIS
base-field generator consistently for all character labels and discrete
logarithms, as the toolbox requires. It can differ from the initial lambda;
all formulas permit any public nonsquare lambda. Capped exact sampling
and factoring retries in this preprocessing share its eta/4 abort budget.
Canonical base-field square roots use public Tonelli--Shanks arithmetic;
exponent/field conversions use the toolbox's clean amplified Shor circuit.
The source's uniform operator-norm guarantee, rather than an unamplified
pointwise discrete-log success claim, is what is composed here.

The total failure-or-incorrect-output probability is at most 7eta/8<eta.
The worst-case native-query cap is 2R+RK. Total gates, preprocessing time,
and quantum workspace are polynomial in log(p) and log(1/eta); no table
of length p is supplied or acquired. Uniform superpositions over ranges
p+1,p-1,p^2-1 are generated by binary interval-state circuits, to the
allocated error; they do not require uncharged rejection postselection.
The sort/fold of x,y includes an order bit in |+>, erased with a Hadamard,
so only the explicitly charged distinct-pair projection is probabilistic.

For the finitely many odd primes p<625, use the full-data moment recovery
already proved in QUADRATIC_LEGENDRE_RECOVERY.md for p>=5. At p=3 the
three irreducible quadratics have distinct native truth tables, so compare
the three possibilities after three queries. These are bounded constants
in the growing-prime resource statement; the p3 moment exception is not
silently used. The bound above concerns an abstract uniform circuit family,
not a compiled or experimentally run quantum device.

Source integrity: xi_jacobi_1809_04286.pdf SHA256
ebca67d566b3e6e678e261438b5c6176bb21177bd42fd4af7ed1d73f8b43357b.

## Reviewed finite-domain phase-copy corollary

The next pass reread STATE/TRAPS, checked the corpus and baseline catalog,
and read Russell--Shparlinski Theorem 6's actual phase-copy source. That
source is the ordinary finite-field phase state, not a homogeneous bit
oracle. The catalog's norm-search attack concerns explicit OPI predicates;
its factorization input is not supplied here. The existing character-only
moment/birthday baselines remain the relevant classical comparison.

This continuation directly removes an input-access restriction of the
reviewed receiver. It proposes no new subsystem or conditioning scan.
Assume fresh independent pure copies

    |f_Q>=p^-1/2 sum_(x in F_p) chi(Q(x))|x>,

with the same unknown monic irreducible Q and known odd prime p. No
oracle, inverse preparation, controlled unknown unitary or extension-field
access is supplied. A raw uncontrolled phase query can make one such copy,
but the proposed procedure needs only the copies themselves.

Take two copies, project distinct finite x,y, and fold/sort. This succeeds
with probability (p-1)/p and produces the vector phi_Q supported on finite
rows of Omega_s. With psi_Q=T|Q>/sqrt(N_s),

    phi_Q = P_finite T|Q>/sqrt(M),
    ||phi_Q-psi_Q||^2
      =2-2 sqrt((p-1)/(p+1)) <=2/(p-1).                 (12)

For p>=625 the norm difference is <1/16. The reviewed adjoint receiver
K is a contraction, and its ideal correct amplitude on psi_Q exceeds
1/sqrt(32)>1/6. Its amplitude on phi_Q is therefore >5/48. Including the
distinct-pair probability gives joint correct output at least

    (624/625)(5/48)^2 =13/1200 >1/128.                 (13)

This is a norm-perturbation proof uniform over Q, not an assertion that
the missing infinity component can be prepared. No bit oracle is used.

Fresh-copy verification also avoids a bit oracle: publicly prepare the
KNOWN candidate state f_A, apply the inverse of THAT public preparation
to a fresh input copy, and accept the all-zero outcome. A true candidate
passes with probability one ideally. A wrong irreducible A passes with
probability |<f_A,f_Q>|^2<=9/p<1/64 at p>=625, by Weil. This projection
consumes its copy; it is not an inverse of the unknown source.

Proposed capped budget: compile reconstruction to operator error 1/1024,
leaving correct-candidate probability >=1/256. Set
R=ceil(512 log(4/eta)), K_v=ceil(log(4R/eta)/log(32)). Each verification
projection has event error <=1/(128 K_v), paid by its public circuit.
A true candidate passes all K_v with probability >=127/128, and a wrong
one passes each test with probability <=3/128<1/32. Fresh independent
copies give false acceptance <=eta/4 and no accepted true candidate
<=eta/4 after R trials; preprocessing retains its eta/4 cap. Total copies
are at most 2R+R K_v, and the gate/space bound stays polynomial in
log(p),log(1/eta). The independent receiver-review addendum accepted these constants,
adaptive conditioning and the small-prime procedure below. Total failure
is <=3eta/4<eta. This is a written copy-only algorithm, not quantum
execution, novelty, speedup or a classical separation.

For p<625 the bit algorithm's full-data operation is NOT used. It proves
injectivity only: equal sign tables determine Q by moments for p>=5,
and the three p3 tables are distinct. Opposite sign tables are impossible
because every such table sums to -1. Thus no two candidate phase states
are equal up to global phase, and their overlap magnitude is <=1-2/p.
Enumerate all M=p(p-1)/2 candidate irreducibles, taking

    K_s=ceil(p log(4M/eta)),
    delta_s=min(1/p,eta/(4K_s))

as tests per candidate and maximum per-test event error. Each wrong
candidate passes a test with probability <=1-1/p; any false acceptance
costs <=M exp(-K_s/p)<=eta/4. The true candidate is ever rejected with
probability <=K_s delta_s<=eta/4. Return the first full acceptance or
ABORT. The worst-case copy count is M K_s, a bounded constant times
log(1/eta) in this finite-prime branch. All tests consume fresh copies;
only PUBLIC known-candidate preparation is inverted.

An uncontrolled raw phase oracle supplies one input copy per query from
a public uniform state. Include its uniform-preparation approximation in
the reconstruction or verification error budget above. No controlled use
of the unknown unitary and no pointwise bit compiler is needed. These
bounds require the stated pure tensor-power source; no noisy/correlated
source robustness theorem is asserted. The earlier classical chosen-bit
baseline is retained under ITS original access model, not reinterpreted
as an algorithm receiving quantum copies.

## Subsequent source and classical audit

The focused classical recheck admitted no new operation. Already for
Q=X^2-d, Q^((p-1)/2) has (p+1)/2 nonzero monomials. The formal relation
QF'=((p-1)/2)Q'F does not supply derivative access: from arbitrary native
values, F'(a)=sum_(x!=a)F(x)/(a-x) is a dense interpolation functional.
This observation is not a lower bound under the quadratic promise.
KKK's cubic Mobius fingerprint yield first reads all p values; its actual
limited-query construction has quadratic affine yield. None of these
shortcuts improves the retained expected-sqrt(p) classical algorithm.

The new quantum result's critical GL2 source dependency received a further
independent audit, recorded in
`audits/reviews/2026-11-05-gl2-hard-block-source-review.md`. It verifies the
all-q coherent hard A_gamma block, including explicit noncircular
exceptional-column preparation and clean root/label arithmetic. The
isometry of its torus construction also proves target-column
orthonormality directly, without assuming the target circuit exists.
This is a focused source audit, not a new proof of all generic Mackey theory.

A single predeclared finite falsifier, implemented in
`classical_baselines/gl2_qft_hard_block_control.py` with its sibling JSON,
uses exact Sage fields and 200-bit complex matrices at q=3,5,7, gamma=1.
All 15 columns, including unused outputs, agree with the published target
formulas below 2^-150; the largest residual is below 2.1e-58. Omitting the
exceptional correction fails at every field. The dense correction used
by this check is NOT an efficient state-preparation implementation; that
cost is supplied by the separate proof audit. No quantum execution or
all-q conclusion is inferred from these finite controls.
