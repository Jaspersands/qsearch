# Native Noncentral Filter Tradeoff And Its Label-Adaptive Escape

LOCAL DERIVATION / REVIEW PENDING. No new algorithm, universal receiver
lower bound, memory bound or novelty claim. This applies standard
[amplitude-amplification mathematics](https://arxiv.org/abs/quant-ph/0005055)
to the actual relative orbit isometry, with source access kept explicit.

## Exact Source-Weighted Operator, Not A Scalar Success Guess

Let V be the public orbit isometry, Q=V V^dagger, and P a fixed known
projector on the group register. Put C=V^dagger P V, so0<=C<=I. Starting
with V rho V^dagger and applying k iterations of (2Q-I)(I-2P), the good
component is P V a_k(C), where

    a_0(x)=1, a_1(x)=3-4x,
    a_(k+1)(x)=2(1-2x)a_k(x)-a_(k-1)(x).
    p_k=Tr(rho C a_k(C)^2).

For x=sin(theta)^2, sqrt(x)*a_k(x)=sin((2k+1)theta). Thus

    p_k <= (2k+1)^2 p_0.

This holds for mixed inputs and inaccessible entangled references; it does
not need reflection about the unknown source. The complete good vector,
not just a fitted probability, is tested against this polynomial.

The bound has an exact interval SOS. Let L=2k+1. The unit-circle identity

    L^2-|sum_(j=-k)^k exp(2ij theta)|^2
      =4 sum_(d=1)^(2k) (L-d) sin(d theta)^2

gives the nonnegative polynomial L^2*x-x*a_k(x)^2. For odd d=2m+1,
sin(d theta)^2=x*a_m(x)^2. For even d=2m it equals
4x(1-x)*U_(m-1)(1-2x)^2. This proves the inequality for all k;
the independent integer checker additionally replays k0..8 certificates.

## Exponential Cut ONLY For Frequency-Label-Blind Filters

For the original IID native mixed source the group marginal is Xi_H,
whose maximum eigenvalue is |H|/|G|=3^(-nr). A LABEL-INDEPENDENT group
projector of rank d therefore satisfies

    p_k <= min(1,(2k+1)^2*d/3^(nr)).

Constant success requires d*(2k+1)^2 to be exponential in nr. Rank is NOT
memory bits or circuit size: the cheap predicate 'rotation coordinate=0'
has rank |G|/3. High-rank filters, different/adaptive filters, additional
seed operations, multi-outcome readouts and general collective decoders
are not excluded. No claim about their usefulness follows from this cut.

M independent originals acted on by the SAME diagonal group action have
overlap indicator_H(g)^M=indicator_H(g), so their unconditioned group
marginal is still Xi_H. Extra copies change the seed compression, not the
initial label-blind group mass. Calls to the original controlled action
cost M*(2k+1). This is not the product-group orbit on G^M.

## Counterexample To Extending The Cut To Observed Labels

The observed native frequency label is available to the algorithm. After
conditioning on it, the group marginal need not be Xi_H. Let that label
be a with three distinct rotations, and perform the abelian Fourier
transform on the normal translation coordinates. Select frequency a,
retaining all three rotation coordinates. This is a rank3 GROUP filter,
but it depends on the observed label. Its compression is exactly I/3.

For ANY unknown seed vector psi, including an entangled reference, the
selected Fourier amplitude at rotation t is psi_t/sqrt(3); the original
qutrit is |0>. The success branch relocates the original seed into the
rotation register. One available relative iteration raises probability
1/3 to25/27. A second lowers it to1/243; amplification is not monotone.
All failure mass remains charged. No seed reflection, cloning, secret
decoder or extra information is supplied.

Exact growing-root controls at levels3/4 have |G|81/243 and group rank3.
Their constant success violates the would-be label-blind bounds1/9 and1/27.
This is a concrete falsifier of a broader rank cut, NOT a breakthrough:
the output is only the original native qutrit in another register.
The independent Q(zeta_9) checker verifies every frequency-row map on
arbitrary seed inputs, not a few known-secret success probabilities.

## Matched Direct Baseline For The Public-Guess Filter

The low-rank test on (|e>+|k>)/sqrt(2), with a PUBLIC fixed generator guess
k, is compared to the direct known stabilizer projector

    E_k=(I+R(k)+R(k)^dagger)/3.

Under the unconditioned ideal source, E_k accepts with probability1 if
the guess matches and1/3 otherwise. Testing M separate original copies
and requiring all accepts gives false acceptance3^(-M), whereas measuring
the diagonal tensor R(k)^tensorM still gives1/3. The direct per-copy
controlled-action cost is M, not M*(2k+1) orbit calls.

This is an existing quantum verification primitive, NOT dequantization.
It does not search all3^(nr) guesses efficiently. Importantly, averaging
over labels does not prove that recorded label-aware outcomes contain no
other information. Classical inference from those records remains an
explicit independent obligation. Do not manufacture an uninformative
oracle model by throwing away labels the algorithm actually receives.

## Research Decision

Stop optimizing label-blind low-rank orbit filters at polynomial depth.
Keep label-dependent and noncentral operations open, but require an output
not equivalent to a known direct measurement or seed relocation. A useful
next step must mix or exploit original word/phase structure, and preserve
the complete source/error budget. Neither a constant herald probability
nor a known format conversion is evidence of efficient secret recovery.

Eight complete source controls include M1/M2, levels1/2 and matching/mismatching
public guesses. Three actual filters give168 depth histories. Two growing-root
countercontrols, nine exact SOS certificates and symbolic scaling ledgers
remain review-pending. General varying-phase signal processing, hardware
precision, arbitrary receivers and a full-depth native decoder are open.
