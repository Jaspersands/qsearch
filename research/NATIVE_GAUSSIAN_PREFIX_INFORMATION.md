# Rounded-Gaussian Original Prefix Information

Conditional local derivation; external review pending. This is a restriction
on using only lower-modulus original responses, not a general LWE or quantum
algorithm lower bound. No hardness claim is inferred from a finite fixture.

## Why Bounded-Error Carries Do Not Transfer Automatically

Take the actual source e=round(qX), X distributed with density
exp(-pi*x^2/alpha^2)/alpha. Its real standard deviation is alpha/sqrt(2pi).
Let H=3^t divide q and s=alpha*q/H. The distribution of qX modulo H,
rescaled to a unit circle, has Fourier coefficients exp(-pi*s^2*k^2).
The absolutely convergent Fourier series and triangle inequality give

    TV(wrapped Gaussian, uniform circle)
      <= sum_(k>=1) exp(-pi*s^2*k^2)
      <= exp(-pi*s^2)/(1-exp(-3pi*s^2)).

The last step uses k^2>=1+3(k-1). Rounding is a deterministic equal-cell
partition of that circle: uniform circle values become EXACT uniform
integers modH. Data processing therefore bounds rounded error modH by the
same TV. Rounding BEFORE taking the residue does not change this partition.
Ties have zero probability under the continuous source. This is NOT an
approximation replacing rounded Gaussian by a discrete-Gaussian law.

Put K=floor(3*s^2). Since pi>3 and log(2)<1, for K>=1

    one_original_TV <= (8/7)*2^-K,
    whole_m_original_bank_TV <= min(1,(8m/7)*2^-K).

The product/telescoping bound needs genuinely IID Gaussian errors independent
of the labels. It does not follow from variance bounds or distinct source IDs.
An explicit countercontrol has two labels0,1 and observations(E,E+s), with
the SAME rounded Gaussian E. Each noise marginal has the correct law, but
the difference reveals s modH exactly. The event b2-b1=s has probability1,
versus1/H for IID uniform null responses, so bank TV is at least1-1/H.
The artifact's H9 event census verifies8/9; it is an assumption falsifier,
not a cryptographically hard instance or an attack on the IID source.
The artifact retains the exact rational s^2 and factored decay exponent.
Its published dyadic bank bound rounds UP and caps at128 certificate bits;
it never allocates a denominator2^K when K is exponentially large.

## Exact Scope Of The Cut

Condition on every public label, including their FULL modq values. For any
fixed secret, reducing each original response modH shifts its error by an
integer modH, so the complete reduced bank is within the stated TV of
IID uniform responses INDEPENDENT of the secret. This remains true after
arbitrary classical or quantum processing of those restricted records.
For two fixed-secret input laws, their distance is at most twice this budget.
For a uniform secret prefix in(Z_H)^n, any prefix-only estimator's average
recovery success is at most H^-n plus the TV budget, provided public labels
and original Gaussian noise are independent of the secret. Secret-dependent
public labels could themselves disclose it and are outside that recovery
corollary. This is information
loss at the declared interface, not a computational hardness assumption.

At q=3^n,alpha=1/n^3, polynomial bank size and H=9, the original low digits
become negligibly informative asymptotically. The n8 ledger is deliberately
vacuous; n32,n64,n128 have certified bank bounds<=2^-128 under the SOURCE
premise. The full-root H=q countercontrol stays vacuous, so the theorem does
not discard the informative full original phases used by the word-span idea.

A valid lower-secret quotient is different side information. Subtracting
that acquired prefix and rounding by a large divisor can yield a narrow
derived error law; this lemma does not forbid the source-correct quotient
adapter. Neither full original values, chosen-query access, collective
operations using those values, nor unknown-phase source models are excluded.
Bounded +/-1 calibrations do not satisfy this Gaussian premise.

    python theorems/native_gaussian_prefix_information.py --write
    node research/certificates/native_gaussian_prefix_information_crosscheck.js
    python -m pytest -q tests/test_native_gaussian_prefix_information.py
