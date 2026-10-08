# Next Target: A Classical Noise-Degradation Reduction

Status: SUPERSEDED BY IMPLEMENTED CONDITIONAL CLASSICAL REDUCTION.
Read `TERNARY_NOISE_DEGRADATION.md`, its live report and exact independent
checker. The public sampler, rounding adapter, scalable precision budgets,
finite convolution and source parameter profiles are implemented and tested.
No unconditional hardness or speedup is admitted. The next higher-leverage
target is `NATIVE_NOISY_PHASE_INPUT_TARGET.md`; this older draft is retained
as the derivation/self-critique history, not a current implementation checklist.

## Revised Primary Mechanism: Do Not Deconvolve Unnecessarily

The simpler and stronger first route is to add the existing PUBLIC native
noise nu itself to each paired noisy-linear sample. The resulting noise is
P*nu, not exactly nu, but statistical closeness is enough for transferring
a fixed decoder's success. No inverse characteristic function or positivity
repair is required. For symmetric chi, phi is real in [-1,1], and

    P*nu-nu=(2/(3*q^2))[(phi-1)(cos theta_u+cos theta_v)
                          +(phi^2-1)cos(theta_u-theta_v)].

Triangle inequality on the finite table gives

    TV(P*nu,nu) <= [2*(1-phi)+(1-phi^2)]/3
                  <= 4*(1-phi)/3
                  <= 80*V/(3*q^2).

The last step uses the public integer-error second-moment bound V and
cos x>=1-x^2/2, pi^2<10. This argument does NOT need phi>0. Cap the TV
bound at1, and charge at most M times the per-record bound, plus separate
sampling error. Reuse `ternary_covariant_noise.sample_noise` as the public
law reference: ideal rejection from uniform has expected THREE proposals,
not a full q^2 table. Its current numerical implementation is not by itself
a certified arbitrary-precision sampler; implement/charge that missing
precision layer before claiming a scalable reduction.

This dominates the inverse-kernel route below for the initial approximate
success transfer: fewer assumptions, simpler sampler, and a smaller leading
TV bound. Do not spend the next pass implementing deconvolution merely
because it gives an exact smoothed target identity. The inverse route is
retained as a scoped mathematical countercontrol, not the primary plan.

## Optional Exact-Smoothed Mechanism And Countercontrol

Pair two ordinary noisy linear samples (a,b=a.s+E1) and
(c,d=c.s+E2) over Z/q, with q=3^r, the SAME unknown secret, IID full labels,
and independent errors drawn from a public symmetric distribution chi.
Let phi=E[cos(2*pi*E/q)]>0. The paired noise P=chi tensor chi has Fourier
coefficients phi,phi,phi^2 at (1,0),(0,1),(1,-1), respectively.

The existing native measured noise is

    nu(u,v)=q^-2 [1+(2/3)(cos theta_u+cos theta_v
                                      +cos(theta_u-theta_v))],
    theta_u=2*pi*u/q, theta_v=2*pi*v/q.

Try adding secret-independent public noise drawn from

    K(u,v)=q^-2 [1+(2*(1-epsilon)/(3*phi))(cos theta_u+cos theta_v)
                    +(2*(1-epsilon)/(3*phi^2))*cos(theta_u-theta_v)].

Finite Fourier multiplication gives P*K=(1-epsilon)*nu+epsilon*Uniform
EXACTLY, provided K is nonnegative. Other P Fourier coefficients do not
matter because K has no other represented modes. This uses TWO classical
input samples per output native-style record and does not know the secret.

## Positivity And Why Smoothing Is Necessary

If 0<l<=phi, set

    C=(2/3)[2*(1/l-1)+(1/l^2-1)], epsilon>=C/(1+C).

Comparing K to (1-epsilon)*nu+epsilon*Uniform bounds their pointwise
difference by (1-epsilon)*C/q^2. Since nu>=0, this gives K>=0.
A slightly larger epsilon supplies a strict positivity margin for numerical
sampling. If chi has a known second-moment bound E[E^2]<=V on integer
representatives, cos x>=1-x^2/2 and pi^2<10 give

    phi>=1-20*V/q^2.

Thus for V/q^2 sufficiently small, epsilon=O(V/q^2). The M-record target
law differs from the EXACT native classical transcript by TV at most
M*epsilon, plus separately charged sampling/evaluation error.

The UNSMOOTHED kernel fails: at (u,v)=(q/3,2q/3), all three cosines=-1/2,
so q^2*K=1-(2/phi+1/phi^2)/3<0 whenever 0<phi<1. If P has nonzero
Fourier coefficients EVERYWHERE, inverse convolution is unique and this
refutes an exact additive-noise degradation of this form. If P has other
Fourier zeros, uniqueness fails; additional kernel modes could repair it.
Do not silently promote this scoped obstruction to all reductions.

For l>=1/2, the displayed kernel's density relative to uniform is at most
19/3. Rejection sampling therefore needs only constant EXPECTED proposals,
not a q^2 table, PROVIDED phi and cosines can be evaluated with the required
certified precision in polynomial(log q, error bits) time. That proviso is
an implementation/proof obligation, not permission to hide a full-table step.

## Required Verification Before Admission

1. Check native Fourier normalization/signs, exact finite convolution and
   the simpler add-native-noise TV bound above.
2. Implement public moment/TV/sample accounting, including the NONPOSITIVE
   unsmoothed inverse-kernel countercontrol as a separate diagnostic. Do not
   require deconvolution for the primary approximate reduction.
3. Build a certified public sampler or isolate its numerical approximation
   and charge a per-record TV budget. No true-secret input is permissible.
4. Identify a precise noisy-linear-problem source theorem at modulus3^r,
   with appropriate error law, public moment bound, secret distribution and
   hardness parameters. Prime-modulus results do not transfer automatically.
5. Make M*epsilon negligible while preserving the source theorem's noise,
   modulus, dimension and approximation requirements. Do not assume M is
   fixed independently of a hypothetical decoder's running time.
6. Prove a success-transfer statement for any fixed classical native decoder
   under the resulting transcript TV loss. Hardness remains conditional on
   the specified source problem; failure of current attacks is not hardness.

Relevant primary starting points, NOT yet checked for these parameters:
[Regev, On Lattices, Learning with Errors, Random Linear Codes, and
Cryptography](https://cims.nyu.edu/~regev/papers/qcrypto.pdf) and
[Brakerski et al., Classical Hardness of Learning with Errors](https://arxiv.org/abs/1306.0281).

CRITICAL NON-IMPLICATION: producing a classical transcript close to the
native measured law does NOT prepare the unknown coherent native qutrit
states. Even a correct classical-hardness transfer would not supply the
quantum input bridge or an efficient receiver. Those remain independent
obligations. This target may fail on source-theorem parameters or sampler
precision; such failures must be retained rather than patched by assertion.
