# Native Ring-LWE: Homogeneous Gaussian Sampling Is An Alternative Target

Date: 2026-10-04. LOCAL DERIVATION / REVIEW PENDING.

Follow-up to NATIVE_RLWE_CHOSEN_PREIMAGE_REDUCTION. This is essentially a
ONE-COORDINATE DUAL/HYBRID ATTACK, not a newly discovered quantum algorithm.
The contribution is a source-specific correctness/access certificate and
relaxation of the missing primitive. No efficient sampler, novelty,
independent verification, speedup or security estimate is claimed.

FOLLOW-UP: NATIVE_RLWE_GAUSSIAN_COOLING_AUDIT tests native Gibbs-parent
cooling with a state-specific warm-start bound and separately charges
approximate filtering. Centering does not supply useful native moves.

FURTHER ALTERNATIVE: NATIVE_RLWE_SINGLE_WITNESS_TARGET uses a DISTINCT
larger modulus to replace the distribution interface by finitely many
short, label-separated witnesses. Their efficient generation remains open.

RING BATCH FOLLOW-UP: NATIVE_RLWE_ROTATIONAL_WITNESS_REDUCTION sends one
K_0 Gaussian batch isometrically to every K_j by signed rotation. Reuse
m independent base samples for all coordinate scores: independence across
coordinates is not required by the union bound. This reduces primitive
calls, not the unresolved cost per sample. Its finite witness decoder
needs just one checked base vector rather than a Gaussian batch.

## 1. A Weaker Interface On The Existing d^4 Source

Retain the original two-record F,b from the chosen-preimage note:

    F=[C_(a_1)^T C_(a_2)^T], b=F^T*s+e mod q, n=2*d.

For coordinate j let P_j delete output coordinate j and define

    G_j=P_j*F,
    K_j={c in Z^(2*d): G_j*c=0 mod q}, det K_j=q^(d-1).     (1)

Instead of arbitrary chosen cosets, request independent measured samples
from the CENTERED homogeneous law

    nu_j(c) proportional to exp(-2*pi*||c||^2/sigma^2)
                         for c in K_j.                   (2)

In the conventional D_(K,s_G) notation s_G=sigma/sqrt(2). This is a
probability law, not periodized amplitudes or a clean coherent inverse.
No quantum phases, garbage uncomputation, chosen syndromes or correlated
pair queries are required. The sampler is STILL UNSOLVED at polynomial cost
on these PUBLIC lattices and widths. It is not part of the input.

Let t=(F*c)_j. Each measured sample supplies

    b dot c=s_j*t+e dot c mod q.                            (3)

The other secret coordinates cancel exactly. Same original errors are
reused; fresh sampler coins, not fresh training errors, justify concentration.
For r in a candidate coordinate set, estimate

    S_j(r)=E_[c from nu_j] cos(2*pi*(b dot c-r*t)/q).        (4)

Score the original small-prior box, or all q values for uniform secrets.
Use original F coordinates: deleting a row of a label-normalized F'
generally targets a different transformed secret and invalidates that box.

## 2. Centered Moment Bound: No Coset Flatness Needed Here

For ANY full-rank lattice K and CENTERED D_(K,s_G), completing the square
and Poisson summation give

    E exp(v dot c)
      =exp(s_G^2*||v||^2/(4*pi))
         *rho_(s_G)(K-s_G^2*v/(2*pi))/rho_(s_G)(K)
      <=exp(s_G^2*||v||^2/(4*pi)).                         (5)

The shifted lattice Gaussian sum is maximal at zero: its Poisson expansion
has positive coefficients multiplied by phases. Differentiating at v=0
therefore yields E[c*c^T]<=s_G^2/(2*pi)*I. The mean is zero by symmetry.
This is an established centered-Gaussian fact, not a new sampling method.

For fixed original error lift e define

    gamma_j=(2*pi^2/q^2)*E_(nu_j)(e dot c)^2,
    gamma_j<=gamma_0=pi*sigma^2*||e||^2/(2*q^2).            (6)

The SAME upper bound holds for ALL j, without a dimension-sized union loss.
Hidden elliptical shape is not observed or replaced by its mean. Using
uncentered integer lifts avoids incorrect covariance transfer after modular
centering. This lemma is not valid for arbitrary shifted cosets: a scalar
Gaussian on .5+Z at width .1 has variance approximately .25, much larger
than .1^2/(2*pi). The zero-center interface is essential.

## 3. The Separate Label-Entropy Obligation

Shortness alone is not enough. Let pi_j be the law of t and

    kappa_j=max_(Delta!=0) |E_[pi_j] omega^(Delta*t)|.

For the full ambient Gaussian syndrome law r_sigma(u),

    pi_j(t)=r_sigma(t*e_j)/sum_v r_sigma(v*e_j).             (7)

If the earlier certificate |q^d*r_sigma(u)-1|<=eta<1 holds for EVERY u,
then |q*pi_j(t)-1|<=2*eta/(1-eta), hence

    kappa_j<=kappa=2*eta/(1-eta).                          (8)

This single full-syndrome event covers all j. There is no assumption that
observed labels are uniform just because an unconstrained ambient draw
has a uniform-looking marginal.

The true score obeys S_j(s_j)>=1-gamma_j by 1-cos(x)<=x^2/2. For r!=s_j,
subtract the noise-free character in (4) and use Cauchy--Schwarz:

    S_j(r)<=kappa_j+E|omega^(e dot c)-1|
          <=kappa_j+sqrt(2*gamma_j),
    score_gap>=g=1-gamma_0-kappa-sqrt(2*gamma_0).            (9)

Do not assume t and e dot c are independent; the proof does not need that.
The zero-only sampler has perfect shortness and gamma=0, but kappa=1 and
no positive gap. Valid membership and tiny vectors do not imply information.

At eta=.01 and gamma_0<=.2, g>=.1473424478. As in the chosen-preimage note,
for K tested values and d coordinates use m>=ceil[(2/tau^2)*log(2*d*K/delta_est)]
independent samples PER coordinate. There are d*m sampler calls, half the
paired-query count. Require 2*(tau+beta)<g. For example tau=.04, TV sampler
error epsilon=.001 and a separate .001 arithmetic score bound suffice,
with beta=2*epsilon+.001. Approximation must be certified for EVERY queried
K_j; an average-over-j error can destroy one coordinate of the full secret.

Charge prior tails once, then verify the full answer on an independent
original held-out record. All original source/reduction losses remain.
Same-b repetitions assert no joint closeness to many ideal phase states.

## 4. Actual Parameter Losses And Classical Comparison

On the existing d^4 L2 references, E gamma_0=delta_phase^2/2, including
shared hidden shape and correlated errors. Markov gives

    Pr[gamma_0>.2]<=delta_phase^2/.4.                     (10)

| d | Spherical bad-error upper fraction | Elliptical bad-error upper fraction |
| ---: | ---: | ---: |
| 64 | .3384765924 | .3692065926 |
| 256 | .0750891095 | .0725276655 |
| 1024 | .0146627098 | .0110439849 |

These are HYPOTHETICAL conditional-decoder losses, not measured algorithm
success. The existing B_2/(eta*p_U) bounds the bad flatness-label event
conditional on first-label unit; unit rejection is separately charged.
One good-noise event plus one good-label event covers ALL coordinate
decoders. Prior, numerical, statistical and verification terms remain due.

If a polynomial classical sampler implements (2), the decoder is entirely
classical. If only a polynomial quantum sampler exists, classical scoring
does not make that sampler available classically. The expected leverage is
in sampling, not score computation or an unexplained quantum output peak.

This route has a direct literature match. In [Chevignard--Shen--Schrottenloher,
Section 4](https://arxiv.org/pdf/2605.20133), set A=F^T, Aguess=its column j,
and Adual=all remaining columns. Their dual sampling lattice is exactly K_j.
The explicit moment/entropy argument here checks our source without importing
their different geometric premises. Their Theorem 7 and Section 3.4 retain
a basis-dependent rejection ratio and reduced-basis preprocessing; a quadratic
improvement in that ratio is not a polynomial sampler for arbitrary inputs.
Reimplementing this known attack is not a Shor-level discovery.

## 5. Native Klein Still Has Exponential Normalization Cost

G_j has rank d-1. Public pivot selection, output row reduction and coefficient
permutation put it in [I|M] form. The natural integer basis is

    B_j=[q*I_(d-1)  -M],
        [    0       I_(d+1)],

with Gram--Schmidt lengths q repeated d-1 times and 1 repeated d+1 times.
Changing pivots is not lattice reduction. The full K_A is an R-module,
but K_j need not be: its allowed output line is not generally stable under
ring multiplication. Earlier q-isodual identities for K_A do not transfer
automatically to K_j or supply a short basis.

Write s_G=sigma/sqrt(2), Theta(t)=sum_z exp(-pi*z^2/t^2). For the untruncated
native Klein proposal the universal rejection denominator is

    C=Theta(s_G/q)^(d-1)*Theta(s_G)^(d+1),
    Z=rho_(s_G)(K_j)=Theta(s_G)^(2*d)*Pr[G_j*c=0].

On the eta-flat event, Pr[G_j*c=0] lies between
(1-eta)*q^(-(d-1)) and (1+eta)*q^(-(d-1)). Hence

    Delta=Z/C<= (1+eta)*[Theta(s_G)/(q*Theta(s_G/q))]^(d-1),
    1/sqrt(Delta)>=[q/(1+s_G)]^((d-1)/2)/sqrt(1+eta).       (11)

For THIS proposal/target, C/Z is the exact peak target/proposal probability
ratio: all shifted theta normalizers are at most their centered values,
and the lattice point zero attains all centered values simultaneously.
Thus simply tightening the global rejection envelope does not repair the
native proposal. Its classical exact correction accepts with probability
Delta; generic amplitude-amplified correction still has the small-acceptance
burden. Log2 of the right side of (11) is 362.2350942,1976.2408403,9974.2423247.

These are a scoped native-proposal cost proxy, not a lower bound for every
sampler or a lower bound inferred from a published upper-complexity theorem.
Finite proposal/tail/precision ledgers must be audited before transferring
this expression to a particular implementation of Theorem 7.
Good-basis construction and its matched classical sampler remain missing.
Taking sigma near q to make native sampling easy loses the low-error
moment condition; that is not a solution at the requested widths.

Starting at zero is legal for centered optimization, but is not a warm
stationary sample: at sigma approximately 2*sqrt(q), its reference probability
is approximately 1/(q*2^d). Native-basis walks at narrow physical cutoffs
remain frozen as in the earlier sampler audit. Centering removes the need
to find a starting coset representative, not the need for useful nonlocal
moves or a proved mixing/preparation bound.

## 6. Checks And Failed Controls

- Seed 290945: 14 complete native d=2 cases, q=11,17,31, tested both
  coordinate lattices. Exact wrapped probability sums reconstruct the
  UNWRAPPED conditional moments from scalar lift first/second moments.
  All 28 centered covariance and score bounds passed; maximum numerical
  covariance-bound excess 9.24e-14. Tested 4,000 independent draws per
  coordinate. All 16 coordinates with a positive exact moment/entropy gap
  recovered empirically. Among all 28, only 26 exact-score and 25 empirical
  winners were true. Initial unconditional-success assertions FAILED;
  the unsupported requirement was removed, not the adverse instances.
- One q=31 label pair had eta=14.5 and kappa=.9605370208. Both exact
  scores selected a wrong coordinate. Its gap certificates were negative,
  correctly refusing a success claim. A q=11 case had an exact score tie
  and an empirical wrong winner. This is why entropy and flatness matter.
- A zero-only sample law gives gamma=0,kappa=1,g=0 and is uncertified.
- Seed 290946: 32 public pivot-basis/Gram--Schmidt checks and 1,280
  shifted-theta Klein peak-ratio controls. Zero attained the peak in all
  cases. Off-center scalar covariance counterexample was .25 versus the
  invalid centered bound .0015915494.
- Recomputed the three bad-error fractions, fixed positive gap, native
  rejection proxies and zero-point normalization references.

Enumeration is EXPONENTIAL, not a primitive implementation. These are
targeted algebra/falsifier controls, without production wiring, full suite,
live source changes, commit or proof-status promotion.

## 7. Gemini Contract And Main-Model Target

Implement an ALTERNATIVE conditional decoder, separate from the paired
chosen-syndrome route. Build G_j from original F, charge rank/pivot/basis
work and total preprocessing across ALL j. A reference enumerator must be
marked exponential. Record the DGS width convention, zero center, geometry,
fresh-call independence, per-j TV/tail costs, syndrome membership, t entropy,
moment/noise bound, certified gap, original-prior candidate scores and held-
out residuals. No default polynomial sampling certificate.

Regression tests must retain the adverse entropy/flatness rows, zero-only
law, shifted-center covariance failure, native Klein cost, source/prior
coordinate normalization, and correct fixed-error/fresh-coin distinction.
The sampler proof obligation stays OPEN. Full suite/CLI/live integration
is Gemini's task, not evidence already supplied by this note.

Main-model task: a polynomial quantum homogeneous DGS implementation on
these explicit K_j at s_G approximately sqrt(2*q), or a non-Gaussian law
with PROVED small error-weighted moments and spread t characters. Seek
structural relation generation, better bases or genuinely nonlocal quantum
sampling; benchmark complete classical costs. Generic native Klein/QRS,
frozen basis walks and improving score estimation do not meet the goal.
