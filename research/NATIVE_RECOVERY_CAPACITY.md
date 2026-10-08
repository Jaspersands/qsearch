# Full-Recovery Capacity Before Source Or Noise Admission

Status: LOCAL DERIVATION / EXTERNAL REVIEW PENDING. These gates reject
impossible FULL-UNIFORM-SECRET recovery promises under stated input access.
They do NOT supply a receiver, settle noisy LWE, prove computational hardness,
or exclude weaker objectives and small-secret priors. Passing a capacity
gate is necessary, never sufficient for an algorithm or efficient compilation.

## The Missing Check In Existing Source Profiles

The earlier Gaussian profiles n64,q3^16/3^64,M512 test source-theorem guards
and approximation errors. Their noise losses can be small, but the profiles
do NOT contain enough qutrit copies for constant-probability full recovery.
Likewise a nonvacuous coherent-query error budget need not permit sufficient
query capacity. Source validity, approximation quality, information capacity
and efficient decoding are FOUR distinct obligations. None may substitute
for the others. Existing hypothetical success inputs are not demonstrations.

## Copy-Only Dimension Bound, Even With Noise

Condition on public labels and take a uniform secret in G=Z_q^n, q=3^r.
There are N=q^n possible answers. M qutrits occupy dimension d=3^M.
For any conditional density rho_s and POVM E_s,

    (1/N)*sum_s Tr(E_s*rho_s) <=(1/N)*sum_s Tr(E_s)=d/N,

since rho_s<=I. Cap the bound at1. A fixed secret-independent ancilla tau
does not help: rho_s tensor tau<=I tensor tau, whose trace is d. Arbitrary
adaptive processing, collective measurement and aborts are CPTP postprocessing.
Thus the bound covers noisy states without distributional assumptions.
It is an UNCONDITIONAL success bound, not conditional-on-herald correctness.

    P_full_recovery <=min(1,3^(M-n*r)).

At n64,q3^64,M512 this is3^-3584. At q3^16 it is3^-512. Both decisively
exclude an inverse-polynomial or constant-success full-secret decoder for
these displayed copy profiles. M4096 at q3^64 and M1024 at q3^16 clear
this dimension barrier but do NOT implement or prove a decoder.

The uniform prior conditioned on labels is essential. A sparse/small-secret
prior, already acquired secret information, original noisy values, extra
phase states or a coherent source oracle are different contracts. This
theorem does not bar them by calling them copies of the same source.

## Weighted Coherent Queries: A Laurent-Monomial Dimension Bound

For M fixed native index entries the exact phase oracle has K=2M nontrivial
diagonal phases z_1,...,z_K. A query/inverse of canonical signed power k
multiplies a computational branch by1 or z_j^k. Known gates, public-label
preprocessing and clean ancillas have no dependence on these hidden values.
After pathwise weighted exposure W=sum |k_t|, amplitudes are Laurent
polynomials in the z_j, with coefficient exponent vectors c in Z^K and
||c||_1<=W. This includes coherent index choices and measured/adaptive queries:
defer measurements, keep their records, and pad the bounded computation.

The final purification can therefore be written

    |Psi_z>=sum_(||c||_1<=W) (product_j z_j^c_j) |v_c>,

where the vectors v_c depend on public labels and the algorithm, NOT z.
Every final state lies in their span, even if workspace is enormous.
The vectors need not be orthogonal; linear dependencies only lower dimension.
The exact number of integer exponent signatures is

    L(K,W)=sum_(j=0..min(K,W)) 2^j*binomial(K,j)*binomial(W,j).

Choose j nonzero coordinates, their signs, then positive magnitudes with
total<=W. Magnitude compositions count binomial(W,j). The implementation
uses a checked exact integer term recurrence; it does not enumerate these
signatures, all secrets or the q^n group. If the term cap is exceeded,
return UNKNOWN, never a partial sum as an upper bound.

The dimension argument yields for ANY such complete receiver

    P_full_recovery <=min(1,L(2M,W)/q^n).

For the ideal linear bank z_j=chi_q(a_j.s), monomials collapse to ordinary
secret characters of frequencies sum c_j*a_j; this can only strengthen the
bound. But linearity is NOT needed for this dimension upper bound. It also
covers exact noisy phases from arbitrary p(C|s): all possible z still lie
in the SAME public vector span. No smallness/independence of noise is needed
for this capacity statement. Independent/controlled errors remain essential
to the SEPARATE ideal/noisy approximation and upstream source reductions.
Compiled phase-gate errors must be charged separately when interpreting a
physical implementation; separately approximated powered gates must not be
silently treated as exact powers of one approximate base gate.

The bound assumes access through the fixed bank ONLY. Giving the algorithm
original b,d as classical inputs or allowing its OTHER gates to depend on
them invalidates this restriction. It does not constrain a general quantum
LWE algorithm using classical data directly. Hidden initial states, arbitrary
new-label oracles and uncharged large powers likewise require new ledgers.

This is an elementary phase-bank adaptation of established quantum
polynomial/dimension methods, not a novelty claim; see
[Beals et al.](https://arxiv.org/abs/quant-ph/9802049). Their Boolean-oracle
degree results are not imported as a theorem for this different source.
The displayed argument supplies the precise Laurent and access conventions.

## Genuine Corrections To The Displayed Indexed Profiles

At n64,q3^64,M512, weighted W128 andW1024 have signature-count bit lengths
693 and2599, while the secret count has6493 bits. Thus BOTH constant-success
indexed profiles are excluded even though their previous NOISE ledger was
nonvacuous. Exact necessary exposure is found by integer doubling/bisection;
the report keeps the two consecutive exact counts bracketing the target.
There is no inferred asymptotic fit or assumed frequency independence.

A coarse asymptotic consequence is L(K,W)<=(2K+1)^W, since every exponent
can be assembled from W signed unit/zero steps. Therefore constant-success
recovery requires W=Omega(n*log q/log M) for a polynomial bank. At
q=3^(2n), M=poly(n), this is Omega(n^2/log n), still polynomial.
This is NOT an exponential query lower bound or a no-go for the project.

## Capacity Versus The Generic Noise Certificate At ALL Exposures

The indexed source adapter uses the sufficient proxy loss

    min(1,W*d0), d0=sqrt(80M*V/q^2),

plus gate/caller/rounding errors. d0 is an UPPER error proxy, not a lower
bound on actual noise. Let l>0 be a certified rational lower enclosure of
d0, and B=floor(1/l). The generic certificate subtracts at least min(1,W*l).

For K>=2 and integer W>=1, L(K,W)/W is nondecreasing: the j1 term is
constant, j>=2 terms binomial(W,j)/W=binomial(W-1,j-1)/j are increasing,
and the j2 increment alone is2*binomial(K,2)>=2, greater than the decreasing
1/W term. Consequently if

    L(K,B)/q^n <=B*l,

EVERY W in1..B has capacity ceiling <=the loss subtracted by that generic
certificate. Beyond B the proxy subtraction is already1. At B0 the latter
argument covers every positive W immediately. W0 remains chance guessing.
Gate/rounding costs can only worsen the certificate, so their omission
strengthens this particular falsifier rather than hiding a success claim.

For n64,q3^64,M512,alpha1/1048576 and the continuous-Gaussian moment upper
V<=q^2*alpha^2/3+1/2, B=8973. L(1024,8973) has5704 bits against6493 secret
bits. The exact boundary inequality holds, ruling out any positive full-
recovery lower bound beyond chance using THIS generic subtraction, at ANY
weighted exposure. It does NOT prove the actual noisy receiver impossible.
A sharper/direct robustness analysis, larger bank, lower alpha, alternative
data access or different target can escape it. The larger-bank and lower-
alpha controls deliberately preserve this distinction. Lower alpha also
changes the upstream lattice approximation factor; it is not a free edit.

## Implemented Controls And Revised Constructive Priority

Live artifacts include four copy profiles, three indexed profiles, three
joint Gaussian profiles,25 exact small signed-ball references, and the exact
all-exposure incompatibility witness. Independent arithmetic replay checks
every count, threshold, interval and status. Small ball enumerations in
tests validate the combinatorial identity; they are not oracle algorithms.
Tamper tests target falsely feasible source profiles and wrong large counts.

Update the source profiles so they visibly state full-recovery capacity,
not merely small source approximation loss. Choose a receiver regime that
passes NECESSARY capacity and source-noise prerequisites before spending on
a circuit. One plausible correction is a larger original bank or smaller
inverse-polynomial alpha with explicitly changed lattice parameters.
Passing those gates does not replace the central missing operation:
efficient noncharacter joint processing of the original fixed bank.

## Subsequent Gaussian Refinement

The [Gaussian bank robustness derivation](NATIVE_GAUSSIAN_BANK_ROBUSTNESS.md)
now escapes the generic-ledger exclusion at the SAME M512,alpha1/1048576
parameters. Its stronger Gaussian-tail premise yields an expected norm bound
2*alpha*sqrt(pi*log(4M))+pi/q, rather than sqrt(80MV/q^2).
At necessary exposure15306 the resulting noise loss is about0.143, not1.
The earlier all-exposure statement about THAT moment-only certificate remains
valid; it must not be promoted to a no-go for the actual Gaussian source.
Larger banks or lower alpha are therefore not presently required just to
escape this noise certificate. A decoder and all remaining precision debts
are still missing.
