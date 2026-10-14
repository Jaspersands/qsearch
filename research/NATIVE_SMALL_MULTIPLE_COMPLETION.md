# Small-Multiple Completion From Original Records

Local constructive derivation and ensemble verification; external review
pending. No actual multiple producer, decision oracle, or quantum speedup
is supplied. The task is to specify what such a mechanism must deliver.

## Algebraic Quotient, Not A Nonunit Inverse

At q=3^r let a supplied vector w satisfy w=c*s modq, with c nonzero modq.
Write gcd(c,q)=g=3^d, Q=q/g, c=g*u, with u a unit modulo Q.
All w coordinates must be divisible by g. Otherwise this particular (c,w)
pair is exactly impossible. If compatible,

    x = u^(-1)*(w/g) modQ

is the known quotient IF w really belongs to the planted secret's orbit.
There remain g^n algebraic preimages s=x+Q*h. Local divisibility does not
verify the multiple's truth. Signed coefficients, nonunit factors and the
entire original modulus are retained. No inverse of c modulo q is invented.

## Original-Bank Completion

Using ACTUAL original responses, y-a.x=Q*(a.h)+e modq. Round each residual
to the nearest Q-spaced center to obtain a linear equation for h modulo g.
The integer rule is floor((residual+floor(Q/2))/Q) modg; Q is odd, so no
halfway ties exist. For |e|<=floor(Q/2), all equations are correct.
A basis fixed from labels mod3 before response processing has a unit
determinant at every3-power modulus. Exact Newton/Hensel inverses solve the
equations at g, with both inverse identities checked. No prime-only library
inverse is used at composite g. Inconsistent equations and missing unit
bases return explicit incomplete results. Every completed candidate is
checked against w=c*s at the ORIGINAL root.

Given a list of vectors but unknown coefficients, scan every signed centered
coefficient within a declared bound, reusing only public basis inverses.
Preflight caps apply to the WHOLE scan; they are not evidence of no candidates.
Original responses, per-trial residual work and candidate-verification work
are charged. A bound exceeding q/2 collapses to the complete centered nonzero
coefficient domain. That domain may be exponentially large and is never free.
Truth-generated multiple inputs appear ONLY in calibration artifacts, not
as a hidden receiver oracle.

## A Verifier That Covers Adaptive Candidates

For public R with4R<q, a candidate fits if all original circular errors are
at most R. Fit alone is not truth. However, if the actual errors also obey
that bound and no nonzero codeword A*h has all coordinates within2R of zero,
then the bounded fit is unique over ALL secrets. This event covers arbitrary
data-selected lists and coefficients: do not use fixed-candidate independence
or multiply an unnecessary candidate-count factor into the global event.

For a nonzero h with minimum coordinate3-adic valuation d, a uniform
original label has a.h uniform on the order L=3^(r-d) subgroup of Z_q.
Its exact small-ball probability is

    p_d = [2*floor(2R/3^d)+1] / 3^(r-d).

The number of such h is 3^((r-d)n)-3^((r-d-1)n). Independent uniform
ORIGINAL label rows therefore give the code-separation failure union bound

    sum_d [3^((r-d)n)-3^((r-d-1)n)] * p_d^m.

This counts high-valuation differences as well as units; a prime-field
approximation would miss the most dangerous partial-secret aliases.
Small instances carry exact rational bounds and complete original-label
censuses. Large bounds use exact power-block certificates: p_d^b<=2^(-k),
where k is proved by integer inequalities. Population ceiling bits and all
complete blocks are charged. Extremely tiny bounds remain symbolic, with
a looser exact capped failure budget used in composition. No logarithmic
floating-point fit or expanded million-digit probability is required.
This is an ensemble/source promise, not certification of one observed
instance's minimum distance.

## Unconditional Good-Source Events

Fix a public maximum supported valuation D and set

    T=min(R, floor((q/3^D)/2)).

Under TRUE original second-moment uppers V, the probability some |e_i|>T
is at most mV/(T+1)^2 by an integer Markov union. No independence of errors,
labels, candidate generation or coverage is needed for this union.
On the good error AND good code-separation event, ANY true supplied multiple
of valuation<=D completes correctly and is the sole bounded-fit secret.
An externally proved list-coverage failure can be added without conditioning
on a data-selected multiple being true. Without that coverage, the module
does not output a composed recovery guarantee. Original-label IID premises,
source moments and the missing producer remain explicit.
Complete evaluation of the declared coefficient domain is also required:
an analytical source budget never overrides an exhausted runtime cap.

Label-aligned large errors can produce wrong consistent answers; the tests
retain this countercontrol. Bound caps, source failures and absent list
coverage are not silently repaired from truth.

## What This Changes In The Research Target

At q=3^n, m about n^3 and V/q^2 about n^-6, coefficients with3-adic factors
of order n can have useful completion budgets. A coefficient merely bounded
by n^9 can still have a disastrous valuation. The size-only and useful-
valuation ledgers are compared separately. Their budgets are sufficient
upper bounds, not proof that unsafe cases cannot be decoded differently.

[Bogdanov, Tan and Vasudevan, 2026](https://arxiv.org/html/2610.12913v1),
Theorem3.1 and Section4.1, motivate the interface: their result still needs
a distinguisher and may produce nonunit multiples. The separate
[rounded-Gaussian tolerance audit](NATIVE_ROUNDED_GAUSSIAN_TOLERANCE.md)
addresses its GENERAL noise-function interface without importing the
discrete-Gaussian corollary. No reduction or advantage is admitted here.

The higher-upside next target is a real original-source distinguisher whose
heavy Fourier information includes a primitive or bounded-valuation secret
character, or a stronger noise-tolerant completion. Do not assume nonunit
heavy frequencies behave like random coefficients. Compare against the
entire implemented classical completion/verifier, not just the old
exponential preimage helper.

    python theorems/native_small_multiple_completion.py --write
    node research/certificates/native_small_multiple_completion_crosscheck.js
    python -m pytest -q tests/test_native_small_multiple_completion.py
