# Fresh Random Scales Are A Source Requirement

2026-10-25. Exact parent control and mathematical counterexample to a
WEAKENED implementation contract. This is not a candidate algorithm, a
hardness experiment, or an independent review of the main deduction.

## Physical Input And Output

Use the existing easy abelian control at p=257:

    U(a)=diag(1,omega^a), psi=(|0>+|1>)/sqrt(2), H={0},
    S=(1,-1,16,-16), omega=exp(2*pi*i/p).

The first three power sums of S vanish modulo p. A packet has four fresh
copies. Its computational-basis bits b_s produce the frequency
J=sum_s s*b_s with probability 1/16 per bit string. Exactly four of the
sixteen strings give J=0. This derives the address state from the actual
target amplitudes, not from the claimed overlap inequality.

After the uniform address controls U(s*u*a), discarding the targets leaves
a mixture of Fourier states |chi_(u*J)>. Thus the complete address state's
Fourier eigenvalues are the law of u*J. Its ideal mixed coset source is I/p.
There is no postselection, state-preparation inverse, or source noise here.

## Independent Scales

For a fresh uniform u in F_p the frequency distribution is

    q = (1/4) delta_0 + (3/4) Uniform(F_p).

Independent scale choices and independent target copies for k packets give
the cyclic convolution q^(*k), NOT an average of conditional kth powers:

    q^(*k) = 4^(-k) delta_0 + (1-4^(-k)) Uniform(F_p),
    TD(source_k,I/p) = (1-1/p)*4^(-k).

## Reusing One Scale Fails

Now use the SAME uniform u for every packet, but still use fresh target
copies and discard u. Every individual packet has exactly the same
marginal as above. The total frequency instead is u*(J_1+...+J_k). Put

    a_k = Pr[J_1+...+J_k=0].

The address eigenvalue distribution and distance are now

    q_shared = a_k delta_0 + (1-a_k) Uniform(F_p),
    TD(source_shared,I/p) = (1-1/p)*a_k.

The characteristic function of J is

    mu_hat(t)=cos^2(pi*t/p)*cos^2(16*pi*t/p) >=0.

Fourier inversion gives a_k=(1/p)*sum_t mu_hat(t)^k >=1/p. Since
mu_hat(t)<1 for every t!=0, a_k tends to 1/p. Consequently

    TD(source_shared,I/p) >= (p-1)/p^2 = 256/66049,

with equality in the limit. More packets do NOT remove this error floor.
The zero scale is legal for an individual packet; the problem is reusing
that random choice across the whole amplification bank.

At k=8, exact integer frequency counts give:

- Independent scales: TD=1/65792 (approximately 0.0000152).
- Shared scale: TD=41409225/1077936128 (approximately 0.0384153).

No source promise has been falsified: the main proof already requires
independent scales. This is a counterexample to silently replacing that
requirement with correct one-packet marginals. Nor does it establish that
every correlated implementation fails; a different correlation scheme
would require its own complete-source argument.

## Verification And Integration

`source_independence_control.py` enumerates only the sixteen target basis
strings, averages the 257 scales, and uses exact integer cyclic convolution
for at most twelve packets. `test_source_independence_control.py` tests the
two complete source distributions and the correlated-source falsifier.
This bounded reference calculation is not an operational p-sized algorithm.

Keep scales independent across amplification packets AND across receiver
leaves, use fresh IID target copies, and discard scale records before the
receiver. Do not replace independent draws with a reused seed or a single
fixed scale without a new proof. The old main proof and its receipt were
not changed to add this separate control.

Parent validation: all eight new tests passed. The combined dilation,
uniform-measurement and spectral-mixture suites passed 107 tests in 14.58s,
with warnings as errors and pytest's cache disabled. The five parent Python
files passed syntax checks; the unchanged original `replay.py check` passed
with receipt SHA256
`9a6f31f65bafa3d9a4fc90e5917245819b2320cfff422f9b9727890c9b96a590`.
The new control was also executed directly to obtain the exact values above.
These checks do not include the separate reviewer's subsequently added
controls, nor do they run the migrating main repository's full validation.
