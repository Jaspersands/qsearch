# Independent review: one-outcome Hankel resultant receiver

2026-11-05. Read the current `research/STATE.md` and `research/TRAPS.md`.
This review independently checks the parent's stated construction and its
uniform resource bounds. After the parent declared the main note closed,
I read all 283 lines of `research/LEGENDRE_HANKEL_RESULTANT_READOUT.md`;
the actual written construction and its ledger are accepted below. No
archive, network, Git, registry, or external-service action is authorized or
performed. Finite examples are not used to establish the theorem.

## Mathematical verdict and exact claim

The proposed one-outcome receiver is CORRECT as a written construction.
It replaces d separate Fourier outcomes and their rank-growth argument by
one vector of 2d moments and a public classical Hankel solve. It yields a
UNIFORM exp(O(d log d))*poly(log p,kappa^(-1),log(1/eta)) resource bound,
not a polynomial bound jointly in d and log p. This review does not claim
novelty, an executed quantum circuit, classical hardness, or a separation.

Let d>=2, m=2d-1, and let Q be an unknown monic squarefree degree-d polynomial
over an odd prime field F_p. The clean source supplies fresh pure padded
character copies. The robust source supplies fresh exact pure tensor copies
of ONE fixed F:F_p->{+1,-1} differing from lambda composed with Q at at most
rho p positions, where lambda(0)=+1, lambda(z)=chi_p(z) for z!=0,
0<=rho<1/4 is public, and kappa=1-4rho>0. This is not mixed/device noise,
changing masks, or correlated copies.

Sufficient thresholds and per-TRIAL ideal correct-candidate bounds are:

    Clean:  p>=256d^2, q_clean=1/(32m!).
    Robust: p>=max{256d^2,64d^2/kappa^2},
            q_robust=1/(32*36^m*m!).

Public approximate circuits, shared seed failure, and bounded sampling are
charged as described below. A trial consumes m fresh source copies.

## 1. Native coefficient state and the scalar exponent

Use m source copies and project onto pairwise distinct roots x_1,...,x_m.
The success probability is alpha_m=(p)_m/p^m because all source amplitudes
have equal absolute value. Sort coherently, extract the permutation rank,
and unprepare its uniform independent register. Append a coherent uniform
a in F_p^* with phase chi_p(a)^d, and cleanly encode

    R(X)=a product_{i=1}^m(X-x_i).

The scalar exponent is TARGET DEGREE d, not root count m. Indeed

    Res(Q,R)=(-1)^(dm) a^d product_i Q(x_i).

The sign (-1)^(dm) is a single Q-independent global character phase.
For even d, substituting chi_p(a)^m introduces an extra chi_p(a) and
forces the comparison overlap to zero, because the nonzero scalars sum to
zero under chi_p. An odd-target-degree-only test would miss this mistake.

There are N0=(p-1)binom(p,m) split coefficient labels. If Q has r<=d rational
roots, precisely Ngood=(p-1)binom(p-r,m) are coprime to Q. Bad labels stay
in the actual padded state. They are not rejected using an unavailable root
indicator. The virtual state below vanishes there.

The previous public signature seed factors every supported R simultaneously
and enables clean erasure of the sorted roots. It factors public degree-m
R, never hidden Q. Its algorithm and proof remain valid when m grows: there
are at most m current factors, each of degree at most m, and O(log p+
log(1/eta)) public signature shifts.

## 2. Virtual spectrum consists of complete moment vectors

For proof only, let A=F_p[X]/(Q), theta=X mod Q, and
U=|A^*|=product_i(p^(d_i)-1) for the squarefree factor degrees d_i. On
V=F_p[X]_{<=m}, the quotient map L:R |-> R(theta) is surjective, with kernel

    ker L = Q * F_p[X]_{<=m-d},
    dim(ker L)=m+1-d=d.

Every quotient element has p^(m+1-d) preimages. The virtual normalized state
is therefore

    |N_Q>=[p^(m+1-d) U]^(-1/2)
           sum_R chi_p(Norm_A/Fp(R(theta))) |coeff(R)>.

It is never prepared. The hidden quotient, CRT factors, theta, and t below
are proof variables, not supplied access.

The annihilator of ker L consists exactly of vectors

    y_j=Tr_A/Fp(t theta^j),  j=0,...,m,

as t ranges over A, because the finite etale trace pairing is nondegenerate.
The product quadratic-character Gauss sums show that the virtual Fourier
amplitude is zero unless t is a unit. At each of the U unit choices its
absolute value is 1/sqrt(U). The normalization follows from the
p^(m+1-d)-element fibers and the Fourier normalization on p^(m+1) labels.
This argument does not require the full support to be a linear subspace.

## 3. Every virtual-supported outcome reconstructs Q

Given a measured y_0,...,y_(2d-1), form

    H_ij=y_(i+j), 0<=i,j<d,
    z_i=y_(d+i), 0<=i<d.

For a virtual-supported outcome, H is the matrix of the bilinear form

    (u,v) |-> Tr_A/Fp(t u v)

in the basis 1,theta,...,theta^(d-1). The ordinary trace pairing is
nondegenerate because Q is squarefree; multiplication by unit t is
invertible. Thus H is invertible. Equivalently, its determinant is the
trace-basis discriminant times Norm(t), both nonzero (up to determinant
convention). This remains true when some factor degrees are divisible by
the characteristic; no unjustified assumption Tr(1)!=0 is used.

Writing Q(X)=X^d+sum_{j<d}q_j X^j and multiplying Q(theta)=0 by t theta^i
then tracing gives

    H q = -z.

The public classical solve q=-H^(-1)z therefore returns all coefficients
of Q from ONE outcome. The field inverse is an ordinary exact classical
matrix operation, not a quantum singular-value inverse. Abort if H is
singular, then check that the monic candidate is squarefree.

Let D_Q be the Q-specific outcome event 'H is invertible and the decoder
returns Q'. The virtual Fourier state is supported entirely in D_Q.
Cauchy-Schwarz consequently gives

    Pr_actual[D_Q] >= |<N_Q|S_actual>|^2.

The event must be Q-specific: merely lower-bounding the probability of
some nonsingular Hankel matrix would not establish correct decoding.
The algorithm does not need to recognize D_Q in advance; public candidate
verification handles other outcomes.

## 4. Clean overlap and all source flags

The exact normalized clean overlap is

    gamma_clean = Ngood/sqrt(N0*p^(m+1-d)*U).

Since U<=p^d,

    gamma_clean^2 >= (Ngood/N0)^2 * N0/p^(m+1).

At p>=256d^2 and m=2d-1, a union bound gives alpha_m>=1/2.
The probability that a uniform distinct m-tuple hits one of r roots is
at most mr/p, so Ngood/N0>=1/2. Finally

    N0/p^(m+1)=(1-1/p)alpha_m/m!>=1/(4m!).

Hence gamma_clean^2>=1/(16m!). Multiplying by the actual distinctness
projection success alpha_m>=1/2 gives q_clean>=1/(32m!).
There is no factorial postselection when folding permutations; the factorial
here is the density of split polynomials in coefficient space. The coherent
public scalar state must be implemented deterministically to its assigned
precision, or additional heralding must be explicitly charged.

## 5. Robust signed-subset recurrence

Let n=p-r and let B be the number of nonroot errors in F. On the Ngood labels,
the overlap gains the exact signed-subset factor

    E_k=sum_j(-1)^j binom(B,j)binom(n-B,k-j)/binom(n,k).

Root errors again do not contribute to this overlap. Put S=n-2B and E_0=1.
The generating polynomial (1+z)^(n-B)(1-z)^B gives the exact recurrence

    (n-k)E_(k+1)=S E_k-k E_(k-1),
    E_1=S/n.

At p>=4d and rho<=1/4, S>=n/3. If n>=36m, induction proves
E_k/E_(k-1)>=1/6 for 1<=k<=m: the base ratio is >=1/3; given the previous
ratio >=1/6, the next is at least

    (n/3-6k)/(n-k) >=1/6

whenever n>=35k, which follows from n>=36m. Denominators and all previous
E_k are positive, so taking ratios is justified. Therefore E_m>=6^(-m).
This recurrence avoids the earlier collision-bound requirement exponential
in d for positivity of the signed-subset mean.

The threshold p>=256d^2 implies n>=p-d>=36(2d-1) for every d>=2, as well
as every root-distinctness bound used above. Thus

    gamma_F^2=gamma_clean^2 E_m^2
       >=1/(16*36^m*m!),

and including the distinctness flag gives q_robust>=1/(32*36^m*m!).
There is no assumption of independently resampled corruption per copy.

## 6. Uniform time, precision, and active space

The construction can be compiled uniformly in d; it does not hide a
fixed-degree lookup circuit. In particular:

- Sort m distinct O(log p)-bit field labels while recording their permutation.
  Rank/unrank permutations through factoradic integer arithmetic. The rank
  has ceil(log2(m!))=O(m log m) bits and the bijections have polynomial cost
  in m and log p.
- The independent permutation rank is exactly uniform on [0,m!-1]. A public
  uniform-interval preparation circuit on O(m log m) bits unprepares it to
  the required precision; enumerating all m! permutations is unnecessary.
- Coefficient multiplication, signature-seed gcd factoring, reversible
  compute-copy-uncompute, m+1 field QFTs, and the d-by-d classical solve
  are uniform polynomial work in d, log p, the seed length, and precision.
- The one shared good signature seed works for all p field elements and
  hence all supported degree-m R in every trial. Its failure bound does
  not acquire an exponential factor from the number of trials.

For the robust verifier reuse beta=1-2rho, Delta=beta^2-1/4>=kappa/2 and
tau=(beta^2+1/4)/2. The condition p>=64d^2/kappa^2 pays the reviewed
true/wrong projection gap. For either q0=q_clean or q0=q_robust, use

    R=ceil((2/q0)ln(4/eta)),
    K=ceil((8/Delta^2)ln(8R/eta)).

Per-trial public-circuit operator error <=q0/8 implies event error<=q0/4,
leaving correct-candidate probability>=q0/2. Per-verification probability
error<=Delta/8, with threshold rounding<=Delta/8 if needed, retains the
Hoeffding margin Delta/4. The previous failure allocation remains valid:
missed true candidate<=eta/4, all verification errors<=eta/8, shared bad seed
<=eta/16, capped seed-sampler ABORT<=eta/8. Total<=9eta/16<eta.

Total source-copy cap is R(m+K), NOT the old R(d^2+K). Since

    log(1/q_clean)=O(d log d),
    log(1/q_robust)=O(d log d),

all circuit precision logarithms are polynomial in d and the other stated
parameters. The number of trials is exp(O(d log d))*O(log(1/eta)); K is
polynomial in d, kappa^(-1), and log(1/eta). This proves the claimed uniform
exp(O(d log d))*poly(log p,kappa^(-1),log(1/eta)) gate and copy bound.

Trials and verification copies can be requested and consumed sequentially.
Peak ACTIVE quantum workspace and persistent classical state are polynomial
in d, log p, kappa^(-1), and log(1/eta): only one trial, one candidate, counters,
and the shared seed are retained. This does not say that storing all
exponentially many total source copies simultaneously uses polynomial space.
The fresh-copy interface, rather than an imposed simultaneous-input storage
requirement, is the relevant model.

## Retained falsifiers and claim boundaries

- Replace chi(a)^d by chi(a)^m for even d: overlap vanishes. Test this parity.
- Retain injective sorted-root workspace: coefficient Fourier interference
  is lost; the clean inverse remains essential.
- Include nonunit t in the virtual-success argument: H may be singular.
  Unit support follows from the character Gauss sums and is necessary.
- Drop squarefreeness: trace degeneracy and native identifiability can fail.
- Count all nonsingular H outcomes as correct: this omits candidate identity.
- Replace the signed-subset law by an uncontrolled IID power: finite
  cancellation examples from the prior robust review still apply below
  its threshold, although the recurrence gives the new uniform bound.
- Regard m! density as a polynomial in d: the central growing-degree blocker
  is still present. The improvement removes the extra exponent from d
  independent rank-growth trials; it does not solve the full polynomial
  dependence question.

Known classical Prony/Hankel recovery is a public postprocessing primitive,
not a novelty claim. Native classical BIT queries can still have polynomial
query complexity with exponential candidate-enumeration time. Source and
prior-art checks remain distinct from mathematical correctness and finite
implementation falsifiers.

## Final actual-text acceptance

After the parent declared the main note closed, I read its complete actual
text, including the scientific contract and Sections 1--6. It matches the
reviewed construction. In particular it uses chi(a)^d rather than chi(a)^m,
the Q-specific decoder event D_Q, the correct virtual fiber dimension,
nondegenerate weighted trace pairing, the exact signed-moment recurrence,
R(m+K) copy cap, one shared seed event, uniform permutation circuitry, and
active rather than simultaneous-total-input space accounting. I found no
correction required in the mathematical statement or resource ledger.

The parent will add the completed finite-control observations and primary
source links; those editorial additions are outside this actual-text check.
A focused read of the closed control's metadata confirms that its negative
control is the UNCORRECTED old helper phase chi(a)^m, with the public
chi(a)^(d-m) correction omitted. For even d, merely omitting the desired
chi(a)^d would do nothing, since that desired phase equals one. Describe
the test as omitted target-degree correction or wrong scalar exponent, not
ambiguously as absence of all scalar phase. No finite control was rerun for
this review, and its tiny fields are outside the sufficient theorem regime.
