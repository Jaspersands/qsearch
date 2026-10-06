# Native Ring-LWE: Direct Classical Decoding At The Lower Modulus

Date: 2026-10-05. LOCAL DERIVATION / REVIEW PENDING.

This is a finite classical falsifier, not a novel algorithm, independent
proof verification, asymptotic attack, security estimate or quantum result.
It follows NATIVE_RLWE_PHASE_DECODER_TARGET and the source contracts in
STRUCTURED_EDCP_SOURCE_HARDNESS_AUDIT. Gemini owns production integration.

## 1. Research Decision

Two unconditioned seeded public labels at d=64, q=16777259 now have
explicit classical original-data decoders with source-specific analytic
success certificates. This tests the actual q-near-d^4 reference, NOT the
older q-near-d^12 all-coset witness target. It does not require a supplied
trapdoor, short secret box, auxiliary Gaussian sampler or ideal quantum state.

| Seed | Spherical failure upper, reference | Shared-shape failure upper, reference | LLL seconds | Construction plus controls seconds |
| --- | ---: | ---: | ---: | ---: |
| 290960 | .005441791865 | .010705464889 | 9.93 | 15.94 |
| 290961 | .005883405001 | .012670270530 | 10.34 | 16.23 |

These decimals are approximations to saved EXACT RATIONAL upper bounds.
They are fixed-public-label, exact-discrete-reference-law probabilities,
NOT observed source-draw success rates or probabilities over public labels.
The two labels are not a statistically established typical-label result.
All source discretization, anchor, precision and verification losses remain
outside these bounds. The timings include exact construction/profile work
and six bounded controls, but not a full original reduction or attack sweep.

Do not use successes at these saved labels as evidence for quantum advantage.
Do not prune larger dimensions, other parameter regimes or all Ring-LWE.
The relevant next comparison is original-data classical decoding at those
regimes, not compilation of a quantum measurement at a classically solved row.

## 2. Original-Coordinate Decoder

Retain ONE original normal-form record

    b=C_a*s+e mod q, R=Z[X]/(X^d+1).

a is uniform and independent of the prior/noise/latent shape. It need not
be a unit. C_a uses signed negacyclic multiplication. Construct the lattice

    Lambda_a={(x,C_a*x+q*z): x,z in Z^d}, det(Lambda_a)=q^d,
    column basis B=[I,0; C_a,qI], target t=(0,center_q(b)).

The planted lattice point has difference from t equal to w=(-s,e), using
the ORIGINAL unwrapped Gaussian lifts. Centering the OBSERVED b only changes
the planted point's q*z coordinate; it does not replace the prior or noise
by a centered-mod-q covariance. No inverse multiplier changes the prior.

Let beta_i be the Gram-Schmidt vectors of any full basis chosen using a
and public randomness only; write ell_i^2=||beta_i||^2, u_i=beta_i/ell_i.
Exact nearest plane returns the planted point whenever

    |<u_i,w>| < ell_i/2 for every i.                       (1)

Reverse induction through its rounding steps proves this sufficient
condition. Ties count as possible failures. The algorithm uses rational
arithmetic, not an unverified floating-point decoder or exact CVP oracle.
Basis selection using b, fitted recovery outcomes, the secret or hidden
shape invalidates the fixed-direction probability proof below.

This is the established [Babai nearest-plane method](https://isa-afp.org/entries/Babai_Nearest_Plane.html),
not a newly discovered algorithm. That formalization verifies its declared
CVP approximation theorem, NOT our code, source law or probability bounds.

## 3. Spherical Source Certificate

On the exact reference, s and e are independent D_(Z^d,rho), where

    rho^2=(d^(3/2)+1)*(log d)^2.

Completing the square and maximizing the shifted Gaussian lattice sum at
zero give, for any unit direction u,

    E exp(v*<u,w>) <= exp(rho^2*v^2/(4*pi)).

Chernoff, symmetry and (1) therefore imply

    P[Babai fails | a] <= sum_i 2*exp(-pi*ell_i^2/(4*rho^2)). (2)

No independence of GS projection events is assumed. No secret box or norm
promise is needed. This bound covers recovery of the entire integer lift,
which is sufficient, although stronger than recovering the secret modulo q.
Established Gaussian moment methods include [Regev--Stephens-Davidowitz](https://arxiv.org/abs/1502.04796).
The local MGF proof here explicitly uses centered sums; it is not a theorem
about arbitrary shifted Gaussian cosets or arbitrary error distributions.

## 4. Shared Hidden Shape: Two Legal Bounds

Use the ACTUAL joint reference law: conditional on one hidden shape H,
s,e are independent D_(Z^d,H). They are NOT independent after integrating H.
The d/2 paired coefficient-space eigenspaces have eigenvalues

    h_j=h_0+c*Z_j,
    h_0=(log d)^2+d*(log d)^4/2, c=d*(log d)^2/2,
    Z_j=x_j^2+y_j^2, x_j,y_j independent D_continuous(1/sqrt(2)).

Thus Z_j are independent exponentials with rate 2*pi. H is NOT given to
the algorithm. These are the local source audit's normal-form/rounding
contracts, not new error parameters or a theorem asserting finite hardness.

One bound conditions on all Z_j<=2. Its bad-shape probability is at most
(d/2)*exp(-4*pi). On that event H<=h_cap*I, with h_cap=h_0+2*c.
Apply (2) at width squared h_cap and charge the shape loss ONCE.

The stronger saved alternative does not condition on a shape event.
For a unit direction u=(u_s,u_e), let p_j be its total squared projection
onto paired eigenspace j across BOTH blocks. p_j>=0 and sum_j p_j=1.
Conditional Gaussian MGFs, then integration over the shared Z_j, give

    E exp(v*<u,w>)
      <= exp(h_0*v^2/(4*pi))
         *product_j [1-d*(log d)^2*v^2*p_j/(16*pi^2)]^(-1)
      <= exp(h_0*v^2/(4*pi))/(1-alpha),
    alpha=d*(log d)^2*v^2/(16*pi^2)<1.                     (3)

The final inequality uses product_j(1-alpha*p_j)>=1-alpha; it does NOT
replace H by E[H] or redraw shapes per coordinate. It also covers a direction
concentrated in one latent plane, where the denominator bound is tight.
For any v>0 with alpha<1 and r<=ell_i/2,

    P[|<u_i,w>|>=ell_i/2]
      <=2*exp(-v*r+h_0*v^2/(4*pi))/(1-alpha).              (4)

Union bound over i. The minimum of this certificate and the separately
valid conditioned certificate is valid; adding their losses would double
charge alternatives. Conditional secret/error independence and independent
latent pairs are ESSENTIAL source assumptions, not runtime observations.

## 5. Exact Rational Arithmetic, Not Transcendental Fits

The native table uses log(d)<L with L=25/6,45/8,7 at d=64,256,1024.
Only d=64 has been constructed/tested here. The other two are parameter
choices, NOT results. To certify each bound, write L=p/r and check

    (163/60)^p > d^r, since e>sum_(j=0)^5 1/j!=163/60.

Also (163/60)^25>2^36, so e>2^(36/25), and pi>3. Accordingly (2) is
bounded by sum_i 2*2^(-floor(27*ell_i^2/(25*h))) for a rational h>=rho^2.
Exponents above 4096 are RAISED to 4096, retaining a positive conservative
floor rather than underflowing tiny terms to zero.
Generated rational numerators/denominators and Gram determinants use HEX
strings, avoiding decimal conversion limits and loss of large-integer precision.

For (4), r=floor(sqrt(ell_i^2))/2, computed by integer square root.
Set v=6*r/H_0, where H_0=L^2+d*L^4/2. Halve v until the rational
A=d*L^2*v^2/144 is <=1/2. Then alpha<=A and h_0/(4*pi)<=H_0/12.
Use the exact exponent floor[(36/25)*(v*r-H_0*v^2/12)] and the denominator
1-A. This is a reproducible, conservative choice, not an optimized fit.
The shape-conditioned loss is bounded by (d/2)*2^-17.

Integer Bareiss elimination of the Gram matrix returns every leading Gram
determinant. Consecutive ratios give EXACT squared GS lengths; its upper
Schur entries give exact GS coefficients. Verify the row transform, lattice
membership and final Gram determinant q^(2*d). Membership plus this volume
proves index one, independently of floating-point LLL's claimed quality.
LLL is used to CONSTRUCT a basis, not trusted as its mathematical certificate.

## 6. Attempts To Falsify And Remaining Debts

- Both public labels are seeded uniform draws without unit/quality rejection.
  Two favorable draws do NOT establish typical-label success. Production
  sweeps must retain every failed label, retry and reduction cost.
- Six controls per label use bounded uniform integer secrets/errors, NOT
  either source distribution. Radii 1,10,50,100 decode; 1000,5000 fail for
  both labels. Those failures remain in the artifacts. The risk theorem is
  distributional and does not certify every bounded record or confident guess.
- A deliberately bad unimodular basis fails a nearest-plane control even
  on Z^2. A failed certificate is not hardness; stronger classical reduction,
  primal/hybrid attacks and extra original samples remain legal competitors.
- The hidden-shape theorem would fail with arbitrary conditional dependence
  between s and e, secret-dependent labels or basis fitting using b.
- The all-coset Babai norm certificate's d^4 obstruction is NOT an obstruction
  to this direct source-law decoder. They solve different endpoints; there
  is no contradiction and no reason to require its internal witness radius.
- No d=256/1024 construction, general scaling theorem, typical-label theorem,
  held-out experiment, original continuous-source transfer or independent
  proof review was completed. No candidate or proof status is promoted.

The PRS primary PDF returned HTTP403 in this pass. The precise error-family
assumptions above therefore remain explicitly dependent on the repository's
earlier source audit; they were not independently reread or reverified here.

## 7. Reproduce And Delegate

Use the project's Anaconda Python, which has python-flint0.9.0. The separate
system python3 lacks FLINT; construction is optional, exact profile/tests
do not require FLINT.

    python research/certificates/native_rlwe_primal_babai_probe.py --save
    python research/certificates/native_rlwe_primal_babai_probe.py --seed 290961 --save
    python -m pytest -q tests/test_native_rlwe_primal_babai.py
    node research/certificates/native_rlwe_primal_babai_crosscheck.js

The Node checker independently verifies native negacyclic rows, the complete
row transform, kernel membership, Gram determinants, both shape alternatives,
prime/factor-degree guards and exact original-coordinate decoding. Agreement
is an arithmetic regression check, not independent mathematical review.

Focused regression:132passed,1known PGM writer test deselected,10.05seconds.
Each independent saved-label checker covers16384basis entries,128Gram pivots,
384control coordinates and exact source ledgers. Python/JS syntax and4strict
JSON records pass. No full production-suite or qsearch validation is claimed.

Gemini: integrate original-data baseline artifacts, tagged fixed-label local
reference-law certificates; implement actual source draws and held-out tests;
pay rounding/anchor/precision losses; sweep unfiltered labels and larger
dimensions with complete cost/failure reporting. Use string/hex encodings for
large integers beyond JavaScript safe range. The current independent checker
intentionally covers d64 and refuses unsafe JSON numeric integers.

GPT next: do NOT treat these d64 quantum targets as promising evidence.
An unresolved larger-dimension computational target may remain, but it needs
serious original-data classical comparisons. Seek a costed quantum primitive
in a regime not already decoded, rather than another free PGM/sampler oracle.
