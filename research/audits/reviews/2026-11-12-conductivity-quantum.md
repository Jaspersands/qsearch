# Independent review: finite-series quantum conductivity endpoint

2026-11-12. Mathematical review of the final finite-series construction in
`PERIODIC_CONDUCTIVITY_NATIVE_ADMISSION.md`. No experiments, Git operations,
network access, external API calls, or QSVT theorem are used in this review.

## Claim established and scope

For every Boolean phase circuit of size B on the directed edges of the
two-dimensional torus of side L=2^n, and every fixed rational contrast
1<rho<=rho0, there is a uniform quantum algorithm estimating the stated
finite-cell scalar K_j to additive error epsilon with failure probability
at most delta in

`poly(B,n,log(1/epsilon))*epsilon^-2*log(1/delta)`

gates, with polynomial classical compilation and workspace. Here one may
assume 0<epsilon<=1 and 0<delta<1/2; the other accuracy/confidence regimes
reduce to these. Input representations must be readable, as usual; if rho
is supplied rather than fixed, its rational bit length is additionally
charged. No regularity, IID, source-state, nonzero-correction, or supplied
solution promise is needed. This is a circuit-model upper bound, not a
novelty, quantum execution, practical speedup, or classical lower-bound
statement. The separate classical marked-path proof is not reviewed here.

The construction closes after making the Fourier convention, qubit-rotation
angle, controlled phases, and finite error budgets explicit below. I found
no obstruction to the claimed polynomial upper bound.

## Energy and finite-series identities

Write eta=eta_j, A=diag(a), and G=range(D). Rescaling the potential by
sqrt(N) converts the native minimization exactly into

`K_j = min_(g in G) <eta+g,A(eta+g)>`,

with ||eta||=1 and Pi eta=0. With V=D K0^(+,-1/2), V is an isometry from
the zero-mean node space onto G. Consequently M=V* S V+P0 has spectrum
in [1/rho,1], q=V* S eta is zero mean, and completing the square gives

`K_j/rho = <eta,S eta> - <q,M^-1 q>`.

In particular, q=0 causes no division by zero or preparation cost.

For A=c(I+z Sigma), define b=Pi Sigma eta and
H=I_G+z(Pi Sigma Pi)|G. The gradient minimizer is -z H^-1 b, so

`K_j/c = 1+z<eta,Sigma eta> - z^2<b,H^-1 b>`.

The operator in H has norm at most one and z<1. Its norm-convergent Neumann
series gives exactly the written T_r and SERIES. Every T_r is real, since
the alternating product begins and ends with Sigma and is Hermitian, and
|T_r|<=1. The error on retaining r=0,...,k-1 is at most

`c*z^(k+2)/(1-z)`.

Thus a deterministic k=max(1,O_rho(log(1/epsilon))) suffices. These facts
hold uniformly over all phase circuits, including constant media.

## Fourier reflection, zero mode, and normalization

Fix the transform convention

`(F_- f)(k) = N^-1/2 sum_x exp(-2*pi*i*k.x/L) f(x)`.

Then F_- D_j F_-^*=exp(+2*pi*i*k_j/L)-1, as in the note. At nonzero k,
Pi(k)=v(k)v(k)*; at k=0 it is the zero matrix on the two directions.
Hence

`Rgrad = (F_-^* tensor I) [direct_sum_k R_k] (F_- tensor I)`,

where R_k=I-2v(k)v(k)* for k!=0 and R_0=I. Using the opposite QFT sign
requires conjugating the written symbol. This is a convention choice, not
an additional input promise.

Let s_l=sin(pi*k_l/L), theta=atan2(s_2,s_1), and use the standard convention
R_y(t)=exp(-itY/2). Then

`A_k=diag(exp(pi*i*k_1/L),exp(pi*i*k_2/L))*R_y(2*theta)`

prepares v(k) up to its common factor i. That common factor cancels in

`R_k=A_k*(I-2|0><0|)*A_k^*`.

The factor two in R_y is necessary. The central phase flip is I-2|0><0|,
not its negative. The k=0 branch must bypass this flip and act as identity.
There is no constant-gradient direction to add. For n>=1 the nonzero sine
norm is at least 2/L. Therefore p=O(n+log(1/alpha)) absolute precision bits
suffice to approximate the normalized direction to O(alpha). Sine,
normalization and angle arithmetic are uniformly computable in polynomial
time in p; exact zero-coordinate cases can be branched on directly.

Compute the finite-angle descriptions reversibly, apply the rotations and
their exact compiled inverses around the central flip, then uncompute the
descriptions. The arithmetic workspace is returned to zero. Using paired
approximate QFTs and their exact inverses gives an actual unitary reflection
within operator error alpha of Rgrad. Uniform finite-gate synthesis is paid
at precision alpha divided by the polynomial number of elementary gates;
this still costs poly(n,log(1/alpha)). Approximation here is operator norm,
with controlled global phases retained, not equality only up to an unknown
global phase. This is ordinary finite-gate synthesis, with no QSVT backend.

The one-flag LCU is explicitly

`U_Pi=(H tensor I) diag(I,-Rgrad) (H tensor I)`.

Its flag-zero block is (I-Rgrad)/2=Pi, with normalization exactly one.
At zero Fourier frequency this block is zero, as required. The minus sign
on the controlled Rgrad branch is operationally essential. "One flag"
means one LCU flag, in addition to the clean arithmetic workspace.

If n=0 is permitted, handle its L=1 torus separately: D=Pi=0 and the
directional coefficient is the answer. The statement ||V||=1 otherwise
needs n>=1; this harmless edge case does not affect the algorithm.

## Product and measured matrix element

For r+1 projections, use r+1 distinct zero-initialized LCU flags and form
the alternating product with r+2 material unitaries. Projecting all these
flags algebraically onto zero extracts

`Sigma Pi (Sigma Pi)^r Sigma`.

This follows because each flag is touched by only its own projection
unitary. Reusing a flag would not justify multiplication of the blocks.
Clean arithmetic workspace can be reused after its exact uncomputation.

Prepare eta by 2n Hadamards on position and the computational direction
state. The ordinary controlled-product Hadamard test has mean

`Re <0_flags,eta| U_r |0_flags,eta> = T_r`.

No flag is postselected, no successful state is renormalized, and every
trial returns a bounded sign. In particular, the zero-correction case
costs the same as every other case. Full known circuit descriptions allow
controlled versions with polynomial overhead.

The material phase must be the stated Sigma=(A/c-I)/z. If the input bit
f=1 denotes conductivity rho, Sigma=2f-1, which is the negative of the
frequently used phase oracle (-1)^f. That sign is relevant in a controlled
Hadamard test and must not be discarded as a global phase. It is trivial
to implement from the known Boolean circuit with reversible evaluation
and uncomputation, in O(B) elementary reversible gates.

## Finite random clocks and a complete error budget

Set Z=sum_(r<k) z^r. For degree law p_r=z^r/Z, the outcome
W=(-1)^r h, where h is the Hadamard sign, has mean
Z^-1 sum_(r<k)(-z)^r T_r and lies in [-1,1]. No independence among the
moments is assumed; each complete trial independently samples its degree.

There is an explicit bounded-clock sampler. Compute the rational cumulative
probabilities C_l=sum_(r<l) p_r, round each 2^b C_l down, and set the final
cumulative integer to 2^b. Sample exactly b fair bits and use this integer
inverse CDF. Its total variation error is at most k/2^b. All rational
integers involved have O_rho(k+b) bits. Taking
b=O(log k+log(1/epsilon)) therefore makes the law error O_rho(epsilon),
with no rejection loop, random runtime, or hidden rare outcome.

For clarity, let C_*=max(1,c*z^2/(1-z)). One valid allocation is:

- Choose k so the series tail is at most epsilon/4.
- Sample the degree within TV epsilon/(16 C_*); this changes the final
  scalar mean by at most epsilon/8.
- Implement each reflection with operator error at most
  alpha=epsilon/(8 C_* k), including QFT and arithmetic synthesis. The Pi
  block error is at most alpha/2. Telescoping a product of contractions
  changes its moment by at most k alpha/2 and its scalar contribution by
  at most epsilon/16. The compiled full unitaries themselves also permit
  the same bound by a direct unitary telescoping argument.
- Allow statistical error epsilon/2 with probability at least 1-delta.

The first mean is sampled exactly by a uniformly random node and classical
evaluation of the phase circuit. Equivalently, one complete bounded trial
may output

`Y=c + c*z*sigma - c*z^2*Z*W`,

where sigma is that independent classical material sign. Its range width
is at most 2(c*z+c*z^2/(1-z)), a contrast-dependent constant. Hoeffding
therefore needs O_rho(epsilon^-2 log(1/delta)) independent complete trials.
The sum of the displayed bias and statistical budgets is below epsilon.
Output arithmetic can remain rational; its bit length is polynomial in k
and the logarithm of the sample count.

Each trial uses at most k projection blocks and k+1 material evaluations,
O(k) flags, and poly(n,log(1/epsilon)) clean workspace and gates per block.
All degree sampling, angle compilation, circuit control, and material
evaluation costs are polynomial. Systematic synthesis error is bounded as
a bias per trial; no extra factor equal to the number of trials is needed.

## Required wording and claim boundaries

The Fourier convention and R_y factor-of-two clarifications were sent to
the parent during this review and incorporated in the native note. Also
retain the explicit controlled minus sign in U_Pi, the sign convention for
Sigma, fresh flags, and the n=0 convention when specifying an implementation.
These are precise construction details, not unresolved theorem-level
obstructions. The finite degree-sampling and error allocation above finish
the remaining bounded-time accounting in the written candidate.

This establishes an all-circuit polynomial quantum upper bound for the
specified scalar. It does not establish a classical separation; in
particular, an output-specific classical algorithm can match the endpoint
at fixed precision without contradicting this construction. No complete
field output, exact scalar output, growing-contrast guarantee, or quantum
execution is claimed. Future implementations must preserve these bounds;
a passing finite control is only transcription evidence.
