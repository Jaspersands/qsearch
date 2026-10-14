# Conditional Source Refresh: Algebra And Bounds, Not A Supplied Oracle

The sign/mask transform, exact collision censuses and conditional source
ledgers are implemented. An actual certified Gaussian-dither sampler and a
wider-noise producer are NOT supplied. No complete recursive reduction,
quantum speedup, novelty or active negative is admitted. External theorem
review is pending. This supersedes the algebra/bounds portion of the earlier
working note, not its unresolved sampler and coverage requirements.

## Actual Access And Producer Input

At a declared original quotient g, compute all derived observations DIRECTLY
from the original bank using cumulative prefix P and scale L=q/g:

    a_g = a modg, y_g = nearest_L((y-a.P) modq) modg.

Original IDs/hashes and corrected responses are retained. Supplied sign
rows T, secret mask z and integer dithers G then give

    A' = T*A_g modg, y' = T*y_g + G - A'*z modg.

The producer input contains ONLY modulus, labels and responses. Signs, mask,
prefix, source IDs and all research receipts are kept separately. They must
not be passed as hidden advice to an algorithm promised only ordinary noisy
linear inputs. EVERY sign-label accumulation, sign-response term, mask dot
product and original response rounding is counted. Whole entry caps abort
before any original response is processed. Supplied calibration dithers are
integers, not a certified Gaussian source. No transform can set the source
or randomness certificates true merely by attaching a provenance string.

For a true P the child secret is h=(s-P)/L. If z is freshly uniform and hidden,
h-z is uniform conditional on the ENTIRE fixed parent. Given a producer list
element w and a tested coefficient c, w+c*z is a hypothesis for c*h. This
unmasking does not identify the correct coefficient; its domain still costs.
The actual finite control includes nonzero high secret quotients and derived
errors, not a zero-secret or noiseless transform substituted for the source.

## Label Entropy At Composite Roots

For fixed A let P_A be the sign-sum distribution. With N=g^n and m IID
uniform original labels,

    E_A[chi2(P_A || U)] = (N-1)/2^m.

Equal sign rows have probability2^-m. Distinct rows differ in a coefficient
2 or-2, a unit at every odd ternary root, so their sums collide with
probability1/N under random A. The identity follows by expanding collision
probability. This is not a prime-field shortcut. Cauchy--Schwarz gives
TV(P_A,U)<=sqrt(chi2)/2. Conditional on A, fresh independent sign rows
give k-row TV at most k*TV(P_A,U). Markov on chi2 therefore yields

    Pr_A[k*TV(P_A,U)>eta_label]
        <= k^2*(N-1)/(4*eta_label^2*2^m).

Large instances carry upward population/factor bit certificates and a
conservative capped dyadic budget, rather than expanded enormous rational
denominators or floating logarithms. Each finite census checks EVERY matrix
and sign row. The zero matrix has conditional TV1-1/N, proving ensemble
quality is not pointwise quality. Full rank alone is not a certificate.

## Same-Parent Error And Gaussian Translation

For ANY fixed integer e and independent centered signs,

    E_T||T*e||^2 = k||e||^2.

An IID continuous Gaussian with width sigma has shift KL
pi*||T*e||^2/sigma^2. Pinsker, rounding data processing and Jensen give the
conservative rounded-Gaussian batch bound2*sqrt(k)*||e||/sigma.
The comparison retains T, so it does not assume T*A and T*e independent.
Discarding T is permitted; exposing it as extra algorithm input is not part
of the declared ordinary-source promise. Fresh sign coins/dithers/masks and
the sampler's total loss are required, not inferred from calibration data.

For true original quotients e_g=nearest(gX), uniformly for g>=g_min,

    ||e_g||^2/g^2 <= 2*sum X_i^2 + m/(2*g_min^2).

For target normalized width b and noise tolerance eta_noise define

    H = (eta_noise^2*b^2/(4k) - m/(2*g_min^2))/2.

If H>0, sum X_i^2<=H gives the required noise tolerance at EVERY supported
root using ONE common original event. For centered D_a marginals,
E sum X_i^2=m*a^2/(2*pi)<m*a^2/6, so failure is at most m*a^2/(6H).
No independence of original errors or of labels/errors is used by this
moment union. The IID label premise is separate. H<=0 and budgets>=1 stay
vacuous; they are not assertions that no better refresh exists.

The largest supported root bounds each label failure. A union covers EVERY
reachable fixed root in the declared interval, regardless of subsequent
adaptive selection. Common energy and label failures are added, never
multiplied. Masking gives a uniform secret, whose TV to uniform primitive
secrets is exactly3^-n. This extra loss is paid for a producer promised only
primitive secrets. Conditional one-refresh coverage is at least

    max(0, p_ideal - eta_label - eta_noise - 3^-n - delta_sampler),

IF the parent quality event, new-width producer success and complete sampler
loss are proved. Missing p_ideal or sampler loss leaves the field NULL.
Neither is fabricated from the target width or from a successful transform.
Source failures must also be compared against the FIRST producer's coverage
before conditioning on it. A positive refresh bound alone is not that proof.
The ledger also reports (1-delta_source)*p_refresh as an unconditional lower
bound IF source/producer/sampler contracts hold. This uses a conditional
guarantee on EVERY good fixed parent, not independence between source quality
and producer coverage. A vacuous source-quality budget forces this field0.

## Scaling And Falsifiers

Live ledgers vary original width n^-3,n^-9,n^-16 at n32/n128, using m=n^3
and explicit k, target width n^-1, tolerances n^-3 and root ranges of order
n^7 to n^9. These are CONDITIONAL budgets, not million-row executions or
observed Gaussian recoveries. n8 has no declared interval above the chosen
rounding floor and is recorded explicitly. Wider-source budgets can be
vacuous even when label entropy is ample. Narrower budgets do not establish
a producer at the MUCH wider target noise or resolve intermediate roots.

The common-energy interval does not cover roots below g_min. A terminal
decoder or a separate sharper rounding argument is still required there.
Repeated refreshes may improve coverage on a good fixed parent, but larger
concatenated lists can still cause quasipolynomial recursive branching.
Wrong-prefix branches remain outside the true-source contract; the earlier
subgroup-null countercontrol still applies. No general lower bound follows.
The live algebra control also has an explicit FALSE prefix giving exactly the
same quantized child and producer input. Original corrected-response receipts
differ. Mixing/masking/dithering that same child cannot restore lost prefix
information. This finite alias is not a Gaussian source theorem or general
no-go; it prevents treating successful producer-input formation as proof
that a supplied original prefix is true.

## Literature And Workflow

This combines familiar leftover hashing, Gaussian translation and noise
flooding ideas. The [Hollow LWE primary abstract](https://eprint.iacr.org/2025/340)
concerns rotated keys and hollow matrices in a different cryptographic
setting; it does not certify this rounded-Gaussian fixed-parent bridge.
Its full theorem and relevant noise-rerandomization lemmas still need review.
No novelty is asserted. The original BTV interface audit remains applicable.

    python theorems/native_source_refresh.py --write
    node research/certificates/native_source_refresh_crosscheck.js
    python -m pytest -q tests/test_native_source_refresh.py

NEXT: certified public Gaussian dithers with explicit precision/tail/abort
loss, then a real producer promise at the declared target width and output
count. Mathematical review and coefficient ambiguity remain separate gates.
