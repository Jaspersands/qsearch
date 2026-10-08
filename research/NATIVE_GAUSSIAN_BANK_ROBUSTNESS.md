# Gaussian Bank Robustness Reopens The Generic-Ledger Exclusion

LOCAL DERIVATION / EXTERNAL REVIEW PENDING. This sharpens an error certificate
for the existing fixed-bank interface. No receiver, novelty, hardness transfer
or quantum speedup is claimed. All ideal-success numbers remain hypothetical.

## Why This Changes The Next Experiment

The [capacity audit](NATIVE_RECOVERY_CAPACITY.md) establishes that the
n64,q3^64,M512,alpha1/1048576 example cannot certify full recovery using the
SECOND-MOMENT-only loss W*sqrt(80MV/q^2). That statement is correct for that
particular certificate, not actual noise. Gaussian tails offer a stronger
certificate: the fixed diagonal bank's norm is controlled by a MAXIMUM, not
a sum of all squared phase errors. The distinction improves sqrt(M) to
sqrt(log M), without silently reducing alpha or acquiring extra originals.

The source convention comes from the continuous D_alpha lane in
[Brakerski et al., Theorem2.16](https://arxiv.org/html/1306.0281): a real lift
has density proportional to exp(-pi*x^2/alpha^2), hence variance
alpha^2/(2*pi). The scaled lift is nearest-integer rounded before taking
its residue. This is not an arbitrary discrete Gaussian or a fitted noise law.
The source theorem, containing-interval rounding and all caller/synthesis
errors remain separate obligations. Gaussian tails cannot be inferred from
the older public second-moment promise or from a small observed sample.

## Expected Operator Error

For N=2M scalar errors, let X_j have the above Gaussian marginal, and
e_j=nearest(q*X_j). Errors are FIXED across reused phase calls. Arbitrary
correlations between the X_j are allowed for this norm bound; upstream source
and ideal-receiver label promises may still require independence.

Completing the square gives E exp(t*X_j)=exp(t^2*alpha^2/(4*pi)). For t>0,

    E max_j |X_j| <=log(sum_j E exp(t*|X_j|))/t
                 <=log(2N)/t + t*alpha^2/(4*pi).

The first step uses pointwise log-sum-exp and Jensen; the second uses
exp(t*|x|)<=exp(t*x)+exp(-t*x). Optimizing the displayed bound over t gives

    E max_j |X_j| <=alpha*sqrt(log(4M)/pi).

Actual and ideal bank phases differ by exp(2*pi*i*e_j/q), so

    Delta=||V_C-V_s||
         =max_j |exp(2*pi*i*e_j/q)-1|
         <=min(2,2*pi*max_j |e_j|/q),
    E Delta <=min(2,2*alpha*sqrt(pi*log(4M))+pi/q).             (1)

Integer rounding costs at most1/2 on EACH error, but a maximum is used;
it does not become M/2. Taking residues leaves the phase unchanged. This
bound is averaged over the actual Gaussian source, NOT pointwise for every
bank. It covers the same secret-referenced complete circuit comparison as
the original indexed ledger, not only the fully averaged state marginal.

For canonical signed phase power k, the telescoping identity gives
||V_C^k-V_s^k||<=|k|*Delta. Any adaptive/purified receiver with committed
pathwise exposure W therefore loses at most min(1,W*E Delta), plus ALL
phase-gate, other-caller and source-rounding losses. Repeated bank calls
do not resample errors. A compact known powered gate still pays |k|.

## High-Probability Companion

Gaussian Chernoff and a union bound, neither needing independent errors, give

    Pr[max_j |X_j| >alpha*sqrt(log(4M/epsilon)/pi)] <=epsilon.

Replacing log(4M) by log(4M/epsilon) in (1) yields a good-event norm bound.
Any use of that bound must ALSO pay epsilon. The producer records the event
failure separately and never conditions it away. The expectation certificate
is usually tighter for a complete average-success guarantee.

## Exact Arithmetic And Resource Contract

Logarithms use dyadic reduction x=2^k*y with1<=y<2, followed by

    log(y)=2*sum_(j>=0) z^(2j+1)/(2j+1), z=(y-1)/(y+1)<=1/3.

After J terms the positive remainder is at most
2*z^(2J+1)/((2J+1)*(1-z^2)). The k*log2 contribution is included with its
own remainder. Rational Machin pi enclosures and integer-square-root
enclosures complete (1). No floating-point transcendental value accepts a
profile. Printed decimal losses are diagnostics only. Verification replays
the exact endpoints and checks a non-geometric accumulated series separately.

The joint controls use W unit-power calls, not one large fast-forwarded call:
a one-query state would have much smaller actual support than the general
weighted-exposure envelope. Each query retains the explicit O(M) index-branch
implementation, with no QRAM, new labels or source-creation oracle assumed.
Only the two branch phase gates affect the local diagonal norm, but every
equality control and other caller operation still needs its own exact gate
implementation or error budget. Physical gate synthesis has not been done.

At the necessary half-success capacity thresholds, approximate noise losses
are0.143 at M512 and0.032 at M1024 with alpha1/1048576. The old M512 profile's
generic all-exposure exclusion is therefore NOT a reason to change its
Gaussian source parameters. Its refined ledger can leave a positive success
margin IF an ideal receiver exists and remaining errors fit that margin.
The lower-alpha control is retained for comparison, not recommended as a
free source change. These are necessary budget compatibilities, not executions.

## Try To Falsify This Direction

- Heavy-tailed laws sharing the same second moment invalidate (1). Retain the
  original moment ledger when the Gaussian source premise is unavailable.
  The live countercontrol has1024 INDEPENDENT centered errors, each0 or
  +/-q/81, nonzero with probability1/1024. Its variance lies below the
  alpha1/1024 moment budget, but its expected bank error exceeds the Gaussian
  proxy. The rational witness uses2*sin(pi/81)>=4/81 and the exact probability
  1-(1023/1024)^1024. Independence alone does not rescue the false inference.
- Original interval rounding may fail or introduce extra error. Add that loss;
  do not quietly replace approximate torus samples by exact Gaussian integers.
- Bank entries must be the original noisy phases. Enlarging labels via noisy
  linear combinations changes the phase errors and requires a new tail bound.
- Both capacity and noise gates can pass while decoding remains exponential.
  The central missing operation is still useful joint processing, not norm
  certification. Do not turn a hypothetical half-success input into a result.
- A growing-q, polynomial-M polynomial-exposure receiver might require
  unsupported purification reflection or coherent syndrome-fiber erasure.
  Neither is supplied by this refinement.

## Finite Compatibility Does Not Supply An Asymptotic Research Family

There is a SECOND correction. With K=2M coordinates,

    L(K,W)<=2^K*binomial(K+W,K)<=[2e(1+W/K)]^K.              (2)

The first bound permits either sign on every coordinate and counts all weak
nonnegative compositions with total<=W. The second is the elementary
binomial upper bound. At q=3^n, M=O(n) and W=poly(n), log L=O(n log n),
whereas log(q^n)=n^2*log3. Full-uniform-secret correctness is therefore
exp(-Omega(n^2)). A fixed n64 example with moderate necessary exposure must
NOT be extrapolated as a polynomial-time family with a LINEAR bank.

More generally, for q=exp(Theta(n)) and polynomial W, a necessary bank size
is M=Omega(n^2/log n). This is a source/interface bound, not a no-go for
general classical-data quantum algorithms, small-secret priors or larger
polynomial banks. The compact certificate records log bounds directly;
it never materializes q^n or an enormous signed-ball sum. The n256 andn1024
linear-bank controls have small Gaussian noise losses but fail capacity.

A legitimate asymptotic target is instead

    q=3^n, M=n^2, W=n^2, alpha=n^-3.

The j=n^2 term in L(2n^2,n^2) is at least
2^(n^2)*binomial(2n^2,n^2)>=4^(n^2)>3^(n^2).
Thus the necessary SIGNATURE ENVELOPE clears the full-secret count.
This does NOT prove actual frequency coverage: collisions or label dependence
may shrink the true span, and no decoder is obtained from a large bound.
The Gaussian loss is O(sqrt(log n)/n); explicit sequential bank controls
cost O(n^4) compute/uncompute pairs before bit/gate precision factors.
The source guard holds for sufficiently large n. IF an efficient solver
for this precise Gaussian LWE family were built and composition proved,
the cited source theorem would give a quantum GapSVP solver at
~O(n/alpha)=~O(n^4). No such solver is implemented or inferred here.

Nine live scaling controls at n64/256/1024 compare M8n,Wn^3,alpha=n^-4
against Mn^2,Wn^2 at the SAME alpha, then the quadratic-bank alpha=n^-3
target separately. Every mode charges its changed source/noise parameters.
The lower single-term support certificate and upper logarithmic exclusion
must never be confused with an algorithmic feasibility theorem.

NEXT: prioritize a constructive receiver for the QUADRATIC-bank family,
not just the finite M512 profile. Seek useful full-label joint processing
or a matched original-data classical attack, rather than another source
wrapper. External review must check the source-conditioned Gaussian law,
the access contract, the asymptotic family and novelty.
