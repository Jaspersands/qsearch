# Rounded Gaussian Noise Tolerance

Local conditional derivation; external review pending. This repairs one
source-law interface, not the missing decision mechanism or secret decoder.

## Translation Survives Rounding

For original E=q*X with X distributed continuously with density proportional
to exp(-pi*x^2/alpha^2), the continuous standard deviation is
sigma=alpha*q/sqrt(2*pi). The source width alpha is NOT that deviation.
Nearest-integer rounding commutes with integer translations. Modulo-q
reduction and rounding are deterministic channels, so data processing
bounds the translated integer-bank TV by the continuous Gaussian-bank TV.

For m independent Gaussian errors and shift vector v with |v_i|<=B,
the equal-covariance Gaussian KL is ||v||^2/(2*sigma^2). Pinsker gives

    TV^2 <= ||v||^2/(4*sigma^2)
          <= pi*m*B^2/(2*(alpha*q)^2)
          <= 11*m*B^2/(7*(alpha*q)^2).

The last inequality uses pi<22/7. Integer square roots of rational bounds
choose a certified B without floating-point logarithms, square roots or
Gaussian tail fitting. This proves smoothness under the stated Gaussian
law; a moment upper alone cannot replace it.
Shifts are fixed or chosen independently of the original errors, including
label-only choices under the independence premise. Do not condition this
local TV bound on data-selected shifts or past query responses.
The rounded moment upper follows from E round(E)^2<=2E E^2+1/2 and pi>3:
V<=(alpha*q)^2/3+1/2, matching the original-bank completion ledger.

## Precision Abort And Hybrid Budget

If each complete-bank encoding law is within unconditioned TV delta of its
ideal rounded law, triangle inequality charges TWO adapter losses:
translated TV<=ideal_bound+2delta. Conditioning on adapter success does not
erase them. The containing-interval/precision promise must be established
separately; delta=0 means an ideal exact integer-rounding interface, not an
inference from a successfully read file.
The live profile plans containing-interval precision using the existing
Gaussian rounding-abort ledger. Its whole-bank loss is at most eta/16;
the source must supply those intervals and retain every abort outcome.
The published reduction's handling of those abort outcomes still requires
an explicit interface audit; this module does not supply that implementation.

For a hypothetical decision advantage epsilon, choose the least integer t
with2^t>=(qm/epsilon)^4. This certifies the terminal-hybrid squared bound
m^2*q/(4*2^t)<=epsilon^4/(4*q^2*m^2), avoiding any log-base ambiguity.
The hybrid argument requires a primitive secret; at a ternary prime power
a uniform secret misses that promise with probability3^(-n). Actual secret
uniformity, any claimed advantage and the hybrid algorithm remain external.
For classical originals, a paid known uniform secret mask can also
randomize an arbitrary fixed secret without adding samples or changing its
noise; subtract that mask only from a valid final recovery. This is not
access to fresh unknown quantum phases.

Set eta=epsilon/(4t) and margin=eta-2delta. If margin<=0 no positive
tolerance is certified. Otherwise choose

    B = min(floor(q/4)-1,
            floor(sqrt(7*(alpha*q)^2*margin^2/(11*m)))).

With B>=1 the local noise contract clears the required eta bound.
Zero B is a failure of this sufficient budget, not a noise impossibility.

## Literature Interface And Remaining Gap

[Bogdanov, Tan and Vasudevan](https://arxiv.org/html/2610.12913v1),
Theorem3.1, accepts a general tolerant noise function. This local proof can
support that interface for rounded continuous noise; it does NOT import
their discrete-Gaussian-specific corollary. The reduction and distinguisher
are still unimplemented.

The report calculates the conditional coefficient-size ceiling from the
declared interface, then applies the original-bank completion audit.
Positive tolerance does not guarantee that the list contains a usable
3-adic valuation. This is the substantive remaining Fourier/recovery gap,
not an alleged incompatibility caused solely by integer rounding.

An explicit symmetric heavy-tail law obeys the SAME second-moment upper
but has translation TV=1, while the promised Gaussian bound is small.
Never infer Gaussian tolerance from successful calibration or moments.

## Correlation Does Not Force Primitive Characters

Here is a further logical falsifier, not a supplied decision oracle. Let t
be uniform in Z_q, f(t)=1 when its circular distance to0 is<=B, and
h(t)=f_Q(t modQ) for Q=q/g, g=3^D, with2B+1<Q. Set p=(2B+1)/q.
Then E f=p, E h=g*p, E(f*h)=p, and

    Cov(f,h)=p*(1-g*p).
    Cov(f,h)/Var(f)=(1-g*p)/(1-p).

When g*p is tiny the censored predictor preserves nearly all threshold
covariance. Yet its Q-periodicity makes every primitive Fourier coefficient
zero: partition t=z+kQ, and the geometric inner sum vanishes unless g
divides the coefficient index. With a primitive secret vector, the scalar
character statement lifts to the corresponding secret-frequency multiples.
Thus even strong window correlation ALONE cannot force usable valuations.
Live profiles use the actual certified B and a polynomial coarse factor,
then charge the original-bank completion budget at that factor.

The real receiver is NOT granted the unknown scalar inner product t.
This falsifies a proposed inference about correlation and Fourier support;
it is neither an original-source distinguisher nor a new oracle problem.

Next: construct an original-source predicate with primitive/bounded-
valuation Fourier information, or strengthen completion beyond exact
rounding. In the latter route, bounded small-alphabet quotient errors are
worth examining at the ACTUAL prime-power ring. Arora-Ge-style field
linearization cannot be assumed to work in characteristic3 when the error
alphabet covers all three residues; carry and nonunit constraints must be
derived rather than removed by a field shadow.

    python theorems/native_rounded_gaussian_tolerance.py --write
    node research/certificates/native_rounded_gaussian_tolerance_crosscheck.js
    python -m pytest -q tests/test_native_rounded_gaussian_tolerance.py
