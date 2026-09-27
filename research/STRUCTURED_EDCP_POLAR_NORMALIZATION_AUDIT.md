# Structured EDCP: Polar Normalization, Filtering And Annealing Access Costs

Date: 2026-09-25. LOCAL DERIVATION / REVIEW PENDING.

## 1. Decision

Neither a nearly flat frequency law nor a well-conditioned NORMALIZED matrix
makes the required joint-fiber operation efficient. This pass supplies an
explicit projected-unitary encoding for the real structured source, then
charges the singular-value scale that generic polar/QSVT constructions must
amplify. It also checks diagonal filtering and a simple adiabatic path.

This is an applicability/resource audit, not a new fast algorithm or a lower
bound on every use of the explicit arithmetic labels. Source-specific
preconditioning or a different circuit could evade this representation.
No independent proof review, production integration or novelty claim.

## 2. The Source Gives A Concrete Encoding, Not A Free Polar Isometry

Use a finite coefficient source with known probability mu(c), frequency
f(c)=sum_l a_l*E(c_l) mod Q, and r(u)=sum_(f(c)=u) mu(c).
Let |g>=sum_c sqrt(mu(c))|c> be its efficiently prepared product state.
Define the rectangular matrix

    A_(u,c)=sqrt(mu(c))*1[f(c)=u].                           (1)

There is a useful unit-normalization projected encoding, with no Q-sized
table. In a common pair of registers use isometries

    L|u>=|u>|g>,        R|c>=|f(c)>|c>.

Then L^dagger*R=A. Preparing |g>, computing f, and reflecting about these
isometry ranges require only the specified source preparation and reversible
modular arithmetic. Padding does not supply additional conditional oracles.

The exact singular structure is

    A*A^dagger=diag(r),
    A|zeta_u>=sqrt(r(u))|u>,
    W=diag(r)^(-1/2)*A,
    W|zeta_u>=|u>.                                         (2)

Zero r entries are treated by the pseudoinverse. W^dagger prepares the
normalized weighted fibers, and W performs the desired erasure/compression.
This is exactly the missing map, not a simpler subroutine.

The norm RATIO sqrt(max r/min_positive r) can be near one while every
nonzero singular value is about Q^(-1/2). With the actual encoding (1),
the inverse singular scale is still about sqrt(Q). Multiplying A on paper
by sqrt(Q) does not construct a correspondingly normalized block encoding.

For the uniform-secret phase ensemble |psi_s>=sum_c sqrt(mu(c))*omega^(s f(c))
|c>, the usual weighted PGM matrix satisfies A_PGM=F_Q*A. This follows directly
from its row entries sqrt(mu(c))*omega^(-s f(c))/sqrt(Q).
Thus the arithmetic encoding removes an extra generic state-ensemble encoding
overhead, but NOT the intrinsic small singular values of this encoding.
For a nonuniform secret prior, that specific Fourier factorization of the
weighted PGM matrix changes; do not apply it unchanged.

## 3. A Source-Weighted QSVT Degree Bound

For an odd degree-m polynomial p with |p(x)|<=1 on [-1,1], the off-diagonal
singular-vector transform replaces sqrt(r(u)) by p(sqrt(r(u))). The oddness
and p(0)=0 matter: a constant even polynomial acts within one singular-vector
space and does not provide the rectangular polar map in (2).

Bernstein's inequality for bounded polynomials gives

    |p'(x)|<=m/sqrt(1-x^2),
    |p(x)|<=m*arcsin(x)<=m*pi*x/2,       0<=x<=1.

On the ACTUAL phase source, the successful output-block probability is

    S_m=sum_u r(u)*|p(sqrt(r(u)))|^2
        <= min(1, (pi^2/4)*m^2*(1+chi2(r))/Q),
    chi2(r)=Q*sum_u r(u)^2-1.                               (3)

This already averages over the real fiber weights. Demanding only a good
source-weighted approximation, instead of every rare fiber, does not remove
the scale. Constant S_m and bounded chi2(r) require

    m >= (2/pi)*sqrt(S_m*Q/(1+chi2(r))).                     (4)

Each degree costs calls to the supplied encoding or inverse. Finite encoding
and polynomial approximation errors still need charging. The scope is THIS
bounded-polynomial singular-vector transform, not all structured algorithms.

Successful flag probability is not enough: fiber-dependent signs can spoil
coherent erasure. For example, r=(sin(pi/10)^2,sin(3*pi/10)^2,1/4) and the
degree-five amplitude polynomial sin(5*arcsin(x)) give flag probability 0.8125
but normalized target fidelity only about 0.2318409. A coherent phase/error
contract or a suitable fixed-point amplification polynomial remains necessary.

At the default q=nextprime(d^12), equation (4), even granting chi2(r)<=1,
gives the following analytic lower bounds for S_m>=0.9:

| d | log10 Necessary Polynomial Degree |
|---:|---:|
| 64 | 693.2036 |
| 256 | 3698.6871 |
| 1024 | 18494.9134 |

These are not quantum gate counts for an optimal decoder or classical-security
estimates. They diagnose generic amplification of the actual encoding (1).

The primary QSVT paper also proves black-box eigenvalue-transformation lower
bounds (Theorem 73). Those cannot be silently elevated to lower bounds against
algorithms exploiting this source's explicit arithmetic representation.

## 4. Diagonal Filters And Nested Predicate Measurements

For a requested target u, let Pi_u project onto f(c)=u. Starting with |g>,
any instrument with diagonal Kraus operators K_j satisfies

    sum_j p_j*F_j
      =sum_j |<zeta_u|K_j|g>|^2 <= r(u),                    (5)

where j ranges over success branches and F_j is their squared target fidelity.
Cauchy--Schwarz within the fiber and sum_j K_j^dagger*K_j<=I prove the
bound. More generally, an instrument that does not transfer probability
between the fiber and its complement cannot increase the available mass.

For the binary imaginary-time filter exp(-beta*(I-Pi_u)),

    Z_beta=r(u)+(1-r(u))*exp(-2*beta),
    F_beta=r(u)/Z_beta,
    Z_beta*F_beta=r(u).                                     (6)

Normalization creates apparent near-perfect output only after the small
success probability has been divided out. Polynomial beta is not a resource
bound for implementing that normalized nonlinear update deterministically.

Measuring a sequence of nested, increasingly precise residue predicates has
total acceptance r(u), by telescoping conditional probabilities. Their easy
subspace reflections commute and do not rotate a failed branch back into the
desired conditional state. Reflections about the PURE intermediate normalized
states are different operations and require their own implementations.

A Zeno path may have adjacent normalized states with large overlap. That
alone does not provide cheap projectors onto those states. Reusing a prior
preparation circuit inside each reflection must include its cost; projecting
onto an easy coarse subspace is not projecting onto its particular Gaussian
conditional vector. Target-dependent operations that actually move between
fibers are outside (5) and remain possible research directions.

## 5. The Simple Rank-One Adiabatic Escape Is A Search Baseline

Consider

    H(t)=(1-t)*(I-|g><g|)+t*(I-Pi_u),        0<=t<=1.

Evolution from |g> stays in the span of |zeta_u> and the normalized
unmarked component. Its two eigenvalues are

    lambda_+=(1+Delta_t)/2,   lambda_-=(1-Delta_t)/2,
    Delta_t=sqrt(1-4*t*(1-t)*(1-r(u))).                      (7)

The minimum gap IN THIS INVARIANT SECTOR is sqrt(r(u)). This is the
weighted marked-subspace counterpart of adiabatic search, not evidence of a
new polynomial algorithm. The familiar optimized search schedule still
charges an inverse-square-root marked-weight scale.

Do NOT call sqrt(r(u)) the minimum full-Hilbert-space gap. If the fiber has
dimension >1, marked vectors orthogonal to zeta_u have energy 1-t. They become
degenerate at the endpoint. At r=1/4,t=1/2, the sector gap is 1/2 but the
full gap is 1/4. Exact symmetry prevents coupling to those extra vectors in
this specified path; a modified Hamiltonian requires a new analysis.

This rank-one driver result does not analyze a sum of local Gaussian drivers,
a nonbinary potential, noncommuting counterdiabatic terms, or a different
interpolation. The companion off-fiber annealing note separately treats
reversible sparse-block chains for graded Gaussian residual penalties.

## 6. Bounded Verification

Seed 20260925; no production tests, integration, candidate promotion or
full-suite run.

- Eight native finite-source matrices, using (q,d,L,R) equal to
  (3,2,2,1),(5,2,2,1),(7,2,2,1),(5,2,3,1), each at amplitude sigma=1.3,3,
  checked (1)-(2), the partial-isometry property and A_PGM=F_Q*A.
- Forty odd-polynomial/source comparisons checked (3), at degrees
  1,3,7,15,31. Another 120 phase-map controls checked the actual transformed
  source vectors, retaining zero fibers and overrotation signs.
- Thirty full/invariant Hamiltonian spectra checked (7), including endpoint
  degeneracy and small marked weights. They explicitly distinguished the
  sector gap from the full spectral gap.
- The degree-five sign countercontrol above passed. A high success flag alone
  would have incorrectly accepted that transform as good coherent erasure.
- Three analytic degree bounds used 110-digit arithmetic and the real modulus
  recipe. These are mathematical resource bounds, not executed algorithms.

## 7. What Could Escape, And What Gemini Should Check

Potential escapes must supply a new operation, not simply rename W:

1. A source-specific projected encoding with polynomially accessible singular
   values, including its normalization and state-preparation costs.
2. A genuinely nonlocal arithmetic map on the weighted fibers, with a
   source-weighted coherent error proof rather than a generic polar wrapper.
3. A nonstationary quantum path with an explicit accessible gap or a different
   proof of preparation, not the rank-one driver or the obstructed reversible
   chain under a different description.
4. A prior-specific measurement that does not implement this full phase-orbit
   fiber isometry, compared with the prior-aware classical decoder.

Gemini should add normalization, absolute singular scale, polynomial degree,
flag success and coherent phase checks to any proposal using these methods.
Retain the exact arithmetic encoding as a baseline, not a breakthrough
candidate. Any claimed sqrt(Q)-rescaled encoding must have a real construction.
Do not assume an oracle for r(u), normalized fibers or intermediate annealing
states. Routine CLI/registry/test wiring remains Gemini's task.

## Sources

- Gilyen, Su, Low and Wiebe, *Quantum singular value transformation and
  beyond*, [arXiv:1806.01838](https://arxiv.org/pdf/1806.01838), singular-vector
  parity/normalization requirements and Theorem 73. The source-weighted bound
  (3) is derived here for (1), not quoted as a source-specific theorem there.
- Quek and Rebentrost, *Fast algorithm for quantum polar decomposition,
  pretty-good measurements, and the Procrustes problem*,
  [arXiv:2106.07634](https://arxiv.org/pdf/2106.07634), Algorithm 2/Theorem 3.
  Their cost retains encoding normalization and inverse smallest singular
  value. This audit does not criticize a cost omission in that paper.
- Roland and Cerf, *Quantum Search by Local Adiabatic Evolution*,
  [arXiv:quant-ph/0107015](https://arxiv.org/pdf/quant-ph/0107015), the
  rank-one search path and local schedule. Equation (7) is its direct
  marked-subspace specialization; it is not a novel search algorithm.
- Local source and coherent-error contracts are in the Gaussian-fiber,
  information-threshold and conditional-core notes. No standalone oracle
  or physical source error is silently replaced by (1).
