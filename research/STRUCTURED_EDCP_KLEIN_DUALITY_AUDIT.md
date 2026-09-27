# Structured EDCP: Gaussian Sampling And Its Classical Dual

Date: 2026-09-25. LOCAL DERIVATION / REVIEW PENDING.

This pass examines an actual joint-fiber implementation proposal: coherent
Klein Gaussian sampling, optionally corrected by quantum rejection. It gives
a matched classical decoder, exact cost identities, and a fidelity obstruction
for the obvious native basis. It is not a general lattice-sampling lower bound,
an efficient basis-finding algorithm, a verified source reduction, or a novelty
claim. No production integration or candidate promotion is included.

FOLLOW-UP (2026-09-27): section 9 treats optimized filters, not just the
universal rejection envelope. A filter preserving the untouched blocks'
coefficient labels cannot cheaply repair their unconditional marginal on
most informative source fibers. Its scope and preparation-leakage limitation
are explicit; arbitrary coherent cross-block mixing remains open.

## 1. Decision

There are three distinct cases, not one solved Gaussian-sampling subroutine.

1. A sufficiently good basis permits the usual near-Gaussian Klein sampler.
   The SAME basis permits efficient classical Babai decoding after local
   Fourier readout. Compare that decoder before paying for a joint measurement.
2. The obvious native basis is much too wide in the relevant growing regime.
   Universal-envelope rejection has an exponential cost even when many blocks
   supply enough information. Its favorable-looking finite cases do not scale.
3. Omitting rejection does not fix that basis. The unrejected sampler retains
   an unconditional distribution on most coordinates, while the desired fiber
   conditions them on a modular equation. Section 6 bounds the resulting
   success-weighted fidelity, allowing rare fibers rather than demanding
   worst-case precision.

Finding a better basis remains potentially valuable research: classical
postprocessing can be part of an important quantum algorithm. The conclusion
is NOT that local Fourier sampling or the original problem is classical.
The comparison concerns the decoder AFTER the stipulated quantum readout.

## 2. Source, Widths And Prior Art

Work first with scalar rank one, q>=3, d>=2, Q=q^d+1 and L public labels.
Condition on an invertible first label and normalize it to a_1=1; charge that
source event separately. Put D=d*L and

    f=(a_l*q^i)_(l=1..L,i=0..d-1),
    Phi(c)=f*c mod Q,
    Lambda=ker(Phi: Z^D -> Z_Q),         det(Lambda)=Q.

The target fiber for u has amplitudes proportional to
exp(-pi*||c||^2/sigma^2), c in Lambda+t(u), with Phi(t(u))=u. Define

    s_G=sigma/sqrt(2),
    rho(c)=exp(-pi*||c||^2/s_G^2),
    Z_u=sum_(Phi(c)=u) rho(c),
    theta(t)=sum_(k in Z) exp(-pi*k^2/t^2),
    Z_all=theta(s_G)^D,                  r(u)=Z_u/Z_all.          (1)

Thus s_G is a PROBABILITY width; sigma is an AMPLITUDE width. The desired
state has coefficients sqrt(rho(c)/Z_u). The source-paper width discrepancy
and periodization errors in the preceding notes remain separate obligations.

The sampling mechanism is established prior art, not invented here.
[Gentry, Peikert and Vaikuntanathan](https://www.cs.toronto.edu/~vinodv/trapcvp.pdf),
section 3, analyze randomized nearest-plane Gaussian sampling from a supplied
basis. [Chevignard, Shen and Schrottenloher](https://arxiv.org/pdf/2605.20133)
give controlled one-dimensional Gaussian preparation, a quantum Klein state,
and rejection-based corrections with an explicit cost factor.
Their Algorithm 2/Corollary 3 support coherent conditional-coordinate
preparation; their displayed Theorem 7 uses center zero and states a
distributional error guarantee. It must NOT be cited as automatically giving
uniform coherent coset preparation with source-dependent centers, harmless
normalization, or free basis preprocessing. The estimates below are derived
directly for the specified idealized coset sampler.

## 3. The Native Basis And The Real Basis Gap

Let S be the signed cyclic shift, B=q*I-S, and let T_a be the integer
negacyclic multiplication matrix for a's canonical coefficient lift. An
explicit COLUMN basis of Lambda is

    K = [ B   -T_(a_2)  ...  -T_(a_L) ],
        [ 0       I     ...       0   ]
        [ ...                         ]
        [ 0       0     ...       I   ].                      (2)

The first d columns generate the first-block evaluation kernel; the others
compensate changes to each remaining coefficient block. Its determinant is
Q, and every column has zero Phi, so it is the whole kernel, not a sublattice.
The lift t(u) can be the first-block canonical digits with other blocks zero.

In this COLUMN order, after orthogonalizing the first block, every remaining
Gram--Schmidt vector is a bottom coordinate unit vector. For the first d,
the initial norm is sqrt(q^2+1), and no later orthogonalized norm exceeds a
column norm. Thus, writing g_i=||b_i^*||,

    max_i g_i=sqrt(q^2+1),   g_i=1 for i>d,   prod_i g_i=Q.      (3)

The dense random multipliers do not magically disappear computationally:
they affect the conditional centers. Equation (3) instead explains why this
particular basis has a poor width profile. For ANY basis,

    max_i g_i >= Q^(1/D) = (q^d+1)^(1/(d*L)).                 (4)

The gap between q and roughly q^(1/L) is a genuine basis-finding target.
Determinant bounds and adequate information do not supply such a basis.
Nor can one replace the public source by a trapdoor-generated matrix and
declare the same source problem solved.

## 4. A Matched Classical Decoder From The Same Basis

Take ANY explicit integer basis K of Lambda. Reverse the column order of
its dual basis:

    C=K^(-T)*J,       where J reverses columns.

Its Gram--Schmidt lengths are 1/g_(D+1-i). The reversal matters. Moreover

    Lambda^* = Z^D + (f^T/Q)*Z.                               (5)

The inclusion follows from the defining congruence, and both sides have
determinant 1/Q. For the charged wrapped-Gaussian approximation to local
Fourier readout, the integer measurements have the form

    y=f^T*x+e mod Q,
    e_i independent with Pr[e_i=k] proportional to
                     exp(-pi*k^2/r_e^2),
    r_e=Q/(2*s_G)=Q/(sqrt(2)*sigma).                           (6)

Consequently y/Q is a dual-lattice point plus e/Q. Run Babai nearest plane
in C. Equivalently use the INTEGER basis Q*C and integer target y. Since
f's first coordinate is one, the first coordinate of the returned integer
vector modulo Q gives the decoded secret x. Validate all other coordinates
against f*x modulo Q. No secret prior or generic CVP oracle is required.

### Exact Discrete Noise Bound

This argument does not replace the integer noise by a continuous Gaussian.
For any real unit direction v and real t, completing the square gives

    E exp(t*<v,e/Q>) <= exp(t^2/(16*pi*s_G^2)).                (7)

The shifted Z^D Gaussian mass is at most its unshifted mass, by Poisson
summation and nonnegative Fourier coefficients. This proves (7) for the
actual discrete Gaussian product at EVERY width, not only a smooth limit.
Chernoff then yields

    Pr[|<v,e/Q>|>=h] <= 2*exp(-4*pi*s_G^2*h^2).

If each projection onto the normalized dual Gram--Schmidt directions is
less than half its corresponding length, backwards nearest-plane rounding
recovers the correct dual lattice point. Induction on those rounding steps
and a union bound give

    Pr[incorrect x] <= min(1, 2*sum_i exp(-pi*(s_G/g_i)^2))
                    <= min(1, 2D*exp(-pi*(s_G/max(g))^2)).     (8)

The true local Fourier noise is not exactly (6). From the prior-CVP note,
add D*rho_mix/(1+rho_mix), where

    rho_mix=2*exp(-pi*sigma^2/2)/(1-exp(-3*pi*sigma^2/2)),

and add source, periodization, measurement and arithmetic errors separately.
A bound exceeding one is vacuous, not evidence of hardness or dequantization.
This decoder uses the actual public structured f; its coordinates are not
silently replaced with independent generic LWE labels.

### Why This Covers The Standard Smooth Klein Regime

Put t_i=s_G/g_i. Poisson summation gives, uniformly in real center a,

    |rho_(t_i)(Z-a)/t_i - 1| <= eps_i,
    eps_i=2*exp(-pi*t_i^2)/(1-exp(-3*pi*t_i^2)).

If all eps_i<1, let ell=sum_i log((1+eps_i)/(1-eps_i)). The exact Klein
coordinate law q_u and desired law p_u=rho/Z_u obey

    exp(-ell) <= q_u(c)/p_u(c) <= exp(ell).

To see this, the sequential denominator is a product of shifted Gaussian
masses, each in t_i*[1-eps_i,1+eps_i]. Normalization places Z_u between
the same product extrema. Thus the positive-amplitude Klein state differs
from the desired fiber by squared vector norm at most

    2*(1-exp(-ell/2)).                                       (9)

Finite coordinate tails and coherent arithmetic errors are additional costs.
The Gaussian-coordinate construction must erase its calculation workspace;
leaving ordinary random-sampler seeds entangled is not coherent preparation.

When (9) is small by this standard smoothing argument, (8) is small on the
same basis profile. There is no demonstrated advantage to using that basis
only inside an entangled measurement. An efficient way to find such a basis
would still be an important decoder result and should not be discarded.

## 5. Universal-Envelope Rejection: Exact Resource Accounting

For arbitrary widths, define

    C_K=prod_i theta(s_G/g_i).

Every shifted coordinate normalizer is at most the corresponding unshifted
theta value. The ideal universal-envelope rejection filter on a Klein state
therefore accepts with probability

    A_u=Z_u/C_K.                                             (10)

This equality concerns THIS envelope-based filter, not optimal rejection
over all possible proposals or specialized envelopes. Its ideal amplitude
amplification repetition scale is T_u=sqrt(C_K/Z_u). Even granting free
normalization, perfect coherent control, and ignoring gate/precision factors,
its natural-fiber average has the exact identity

    E_(u~r) T_u = sqrt(H_K*P_opt),
    H_K=C_K*Q/Z_all,
    P_opt=(sum_u sqrt(r(u)))^2/Q.                             (11)

This is a per-fiber repetition proxy, not a theorem identifying the cost of
every coherent variable-time algorithm. A full coherent decoder would also
need fixed or coherently managed stopping, phase correctness, and error
control over the source superposition; none are granted by (11).

The estimate cannot be dismissed as only a few rare fibers dominating an
average. With chi2=Q*sum_u r(u)^2-1, Markov's inequality gives

    Pr_(u~r)[T_u<=T] <= min(1, (1+chi2)*T^2/H_K).             (12)

Indeed 1/T_u^2=Q*r(u)/H_K and its source expectation is (1+chi2)/H_K.
When the fiber law is sufficiently flat and H_K exponential, polynomial-cost
fibers carry negligible source probability. Skipping expensive fibers then
fails the WEIGHTED error contract from the preceding interval-transfer note.

For the native basis (2), the L dependence cancels EXACTLY:

    H_native = Q*prod_(i=1)^d theta(s_G/g_i) / theta(s_G)^d.   (13)

Adding more blocks may increase P_opt but does not reduce this envelope
factor. When 1<<s_G<<q, it is asymptotic to Q/s_G^d. At q=d^2,
sigma=sqrt(d), an information-sufficient fiber law with P_opt>=1/2 gives
the following analytic lower bounds on log2(E T_u):

| d | log2 average repetition proxy, lower bound |
|---|---|
| 64 | approximately 303.5 |
| 256 | approximately 1599.5 |
| 1024 | approximately 7935.5 |

The tiny positive theta corrections are retained analytically; these displayed
decimals are rounded, not exact rational lower bounds. These are NOT executed
quantum circuits, simulations at these sizes, or verified reduction parameters.

For any basis, Poisson summation also yields a useful profile identity:

    H_K = (s_G/theta(s_G))^D * prod_i theta(g_i/s_G).           (14)

Track the whole profile, not merely the largest basis vector. A few bad
directions could call for a different method than an entirely poor basis.
Finding that method and its classical competitor is the next real question.

## 6. Omitting Rejection: A Weighted Fidelity Obstruction

There is a separate loophole to test: perhaps the unrejected sampler already
works on most SOURCE fibers even though worst-case smoothing fails.

For the COLUMN order in (2), the last D-d coordinates are sampled first,
from independent centered width-s_G Gaussians. This marginal does not depend
on u at all. Let p_1 be the first block's evaluation distribution, and let
r_rest be the distribution of sum_(l>=2) a_l*E(c_l) from the other independent
blocks. The target total-fiber law is r=r_rest*p_1.

Let beta_v be the nonnegative amplitude overlap between the first-block
Klein proposal and the true first-block fiber, both normalized for residue v.
It lies in [0,1]. Directly summing over the unchanged remaining-block marginal
gives the EXACT joint-fiber overlap

    BC_u = (r_rest*a)(u)/sqrt(r(u)),
    a(v)=sqrt(p_1(v))*beta_v.

Consequently the success-weighted squared fidelity of the unrejected sampler
has the identity and upper bound

    E_(u~r) F_u = ||r_rest*a||_2^2
        <= ||r_rest||_2^2 * ||sqrt(p_1)||_1^2
        = (1+chi2_rest)*P_one,
    chi2_rest=Q*sum_v r_rest(v)^2-1,
    P_one=(sum_v sqrt(p_1(v)))^2/Q.                           (15)

The inequality is Young's convolution inequality and beta_v<=1. It also
applies if a different first-block conditional routine replaces Klein,
provided the other blocks are STILL sampled from their unconditional prior.
Thus even a perfect first-block subroutine cannot repair that marginal.

If L-1 remaining blocks already have chi2_rest=O(1), while P_one is
exponentially small as in the native narrow-Gaussian regime, the entire
weighted fidelity is exponentially small. This handles the source-weighted
approximation criterion, not just adversarial rare residues. It does NOT
apply automatically at a minimal L for which L-1 blocks lack information,
or to a sampler that actually conditions the remaining blocks on u.

This identifies the missing operation concretely: condition the freely
sampled blocks on their required total modular contribution, rather than
always solving only the first block after sampling the others independently.

## 7. Verification Actually Executed

All checks below were bounded mathematical references using existing exact
arithmetic helpers. No CLI/registry/UI wiring, full-suite run, or commit.

Eight basis cases used (q,d,L)=(5,2,2),(5,4,2),(5,4,3),(7,2,2), each in
native and exact-SymPy-LLL form. They passed exact determinant, full-kernel,
integer scaled-dual, quotient-membership, and REVERSED reciprocal
Gram--Schmidt checks. Native maximum g values were sqrt(26) or sqrt(50).
Reduced maxima were 2.449490, 2.724885, 2.236068, 3.162278 respectively.

288 integer-noise decoding trials used s_G/max(g) in {0.3,1,2}, twelve per
basis/ratio. At ratio 2, all 96 trials recovered the secret; ideal failure
upper bounds were between 2.79e-5 and 8.37e-5. At ratio 1, 91/96 recovered;
at ratio 0.3, 16/96 recovered and all stated bounds were vacuous. Widths
were adjusted to each basis/ratio, so these are NOT a matched-width LLL
comparison or a scaling claim. All returned vectors passed the public
structured-code membership check. Trials used (6), not an uncharged claim
about the physical Fourier-noise law.

NumPy seed 20260925; successive public label lists were [1,19], [1,296],
[1,5,559], [1,40]. The discrete error was sampled on
[-ceil(8*r_e),ceil(8*r_e)], with the radius at least two. Its omitted mass
per coordinate is bounded by r_e^2/(pi*R_e)*exp(-pi*R_e^2/r_e^2), rather
than assumed zero. Dense one-dimensional probability arrays were REFERENCES.

A unimodular shear K=[[1,10],[0,1]] verified why reversal is necessary:
scaled integer target (2,2) and scale 5 return (0,20) with the unreversed
dual, versus the correct zero with the reversed dual. Another 72 discrete
Gaussian MGF checks covered non-coordinate directions, probability widths
0.6,1.3,4 and scales 1,7. All satisfied (7)'s general-width precursor.

Joint conditional-law references at q=5,d=2,L=2,a_2=7 used probability
widths s_G=1.3 and 3, enumerating 28,561 and 194,481 coefficient vectors.
Per-fiber Klein normalization errors were below 1.1e-14. Rejection-proxy and
theta-profile identities agreed within 1e-8; no claim rests on decimal
equality alone. Outputs were:

| s_G | P_opt | average rejection proxy | H_K | weighted squared vector error, unrejected |
|---|---|---|---|---|
| 1.3 | 0.7322510423 | 3.3235244628 | 15.0847376329 | 0.7252865216 |
| 3.0 | 0.9999935084 | 1.7000565762 | 2.8902111244 | 0.1238437584 |

These integrate finite boxes. Gaussian input tails are charged by the union
bound D*s_G^2/(pi*R)*exp(-pi*R^2/s_G^2); the Klein mass omitted from each
fiber was checked separately. A finite table is not a scalable sampler.

Ten further residue-convolution references checked (15) at q=5, d in {2,4},
s_G=1.3, and L=2,...,6, with first-block coefficient radius 6. Each used
exact first-block conditional references and explicitly bounded Q-sized
convolutions, not a large-d solver. Representative results:

| d | L | chi2_rest | weighted fidelity | upper bound from (15) |
|---|---|---|---|---|
| 2 | 2 | 8.6227460784 | 0.4445348480 | vacuous |
| 2 | 6 | 0.0888986726 | 0.2577038101 | 0.2773764082 |
| 4 | 2 | 84.7483353748 | 0.1676087022 | vacuous |
| 4 | 6 | 0.0237557228 | 0.0700777889 | 0.0717343666 |

P_one was 0.2547311474 and 0.0700698076 respectively. The nested label
lists, from seed 20260925, were [1,19,4,16,5,9] and
[1,296,300,265,180,319]. Nonunit subsequent labels are retained and pushed
forward correctly, not inverted. These are finite identity checks, not a
natural-label distribution estimate. Finally, 360 arbitrary positive-law
controls checked the source-weighted fast-fiber bound (12).

## 8. Red Team And Next Tasks

FOLLOW-UP: `STRUCTURED_EDCP_CONDITIONAL_CORE_BARRIERS.md` extends section 6
to ANY target-independent rest-frequency marginal, even an optimized one,
and derives a separate tensor-cut rank obstruction. It also gives a positive
extension lemma once an informative conditional core is genuinely available.
`STRUCTURED_EDCP_CLASSICAL_READOUT_SIMULATION.md` supplies a classical
approximation to the specified local readout from retained (A,b); the older
post-readout-only qualification below no longer applies to that access model.

FOLLOW-UP: `STRUCTURED_EDCP_PROFILE_LIST_DECODER.md` now supplies a
full-profile randomized classical list decoder, not merely a proposed
selective-enumeration heuristic. With the documented width/noise/numerical
conditions, polynomial H also gives polynomial post-readout list decoding;
adding independent blocks preserves H exactly. Keep basis construction and
genuine cross-block conditioning as research targets, but do not treat a
few poor basis directions alone as evidence of a superpolynomial advantage.

* A stronger basis need not be classically easy to obtain. Charge its actual
  computation, source coverage and amortization; run (8) on that SAME basis.
* An inverse-polynomial near-Gaussian error from the standard smoothing
  argument is enough for a good classical decoder here. A different,
  source-weighted approximation might work outside that regime; test (12)
  and (15) only when their actual hypotheses apply.
* The rejection envelope may be loose. A source-specific sharper envelope,
  different proposal, walk or measurement is not excluded by (11)--(14).
  Section 9 now constrains sharper filters when the proposal's rest marginal
  is unchanged and the successful map does not mix its coefficient labels.
* The measured data remain quantum-generated. None of these arguments
  supplies a classical sampler for the original source or proves its
  original computational problem classically easy.
* Prior-aware methods can beat this prior-free baseline. The weighted
  prior-CVP decoder stays relevant and must not be replaced by this one.
* A few poor Gram--Schmidt directions are a genuine remaining avenue:
  compare coherent conditioning with classical selective enumeration in
  those directions. A polynomial rejection profile alone is not a speedup.
* The key constructive target is a compact proposal that conditions the
  remaining blocks on u, or a genuinely different coherent readout. Neither
  a short-basis assumption nor unconditional coefficient sampling supplies it.

Gemini: implement `theorems/structured_edcp_klein_duality.py` as a checker and
matched baseline only. Reuse exact integer Babai on Q*K^(-T)*J; never pass
rational bases to helpers that cast entries with int(). Implement log-domain
theta profiles, all source/error charges, (8)--(15), native/reduced basis
validation, the reversal countercontrol, and bounded conditional references.
Reject missing full-kernel certificates, silent target-law changes, and
unjustified efficient-sampler claims. Record negative results for the
SPECIFIED native-basis samplers, not for all structured EDCP algorithms.

Main model stays on the residual mathematical target: conditioning across
blocks, improving the basis profile with a real source, and identifying
whether any proposed coherent benefit survives the matched classical decoder.

## 9. Optimized Filtering Does Not Repair The Native Rest Marginal

This extension is LOCAL DERIVATION / REVIEW PENDING. It applies to a broader
class of filters than section 5, but not to arbitrary conditional-state
algorithms. It does NOT require the other L-1 blocks to be informative on
their own, unlike the particular convolution bound in section 6.

### Contract And A Pointwise Bound

Let mu_1 and mu_rest be the first-block and remaining-block product Gaussian
probability laws. They may both be full or consistently coordinate-truncated.
Use W=theta(s_G) or W=Z_R as their scalar normalizer. For the two frequency
maps f_1 and f_rest, let

    p(x)=Pr[f_1(C_1)=x],
    v(x)=Pr[f_rest(C_rest)=x],
    r=p*v.

The target fiber's rest marginal is EXACTLY

    P_u(z)=mu_rest(z)*p(u-f_rest(z))/r(u).                   (16)

Only r(u)>0 matters. Unlike basis normalization, this identity does not
require unit labels. Suppose a proposal has the unconditional rest marginal
mu_rest, and its successful instrument is block diagonal in the rest's
coefficient labels z. It may depend on u,z, act arbitrarily on the first
block and ancillas, and contain measurements or postselection. It cannot
move amplitude between different z labels in its effective successful map.

If A_u is success probability and rho_u the normalized output, then

    A_u*Pr_(rho_u)[z] <= mu_rest(z).                        (17)

This follows for each z from trace-nonincreasingness of that controlled
block. Internal first-block coherence is allowed. The ideal native Klein
proposal satisfies the marginal premise. An untruncated native proposal
followed by a target-box restriction also obeys the required domination on
the finite target support.

For a threshold tau>0 define

    S_tau={x:p(x)>=tau},
    S_u={z in target support : u-f_rest(z) in S_tau},
    eta_u=P_u(S_u complement).

Then

    mu_rest(S_u) <= r(u)/tau,
    E_(u~r) eta_u = p(S_tau complement).                   (18)

Both statements follow by expanding (16); no independent-residual or
uniform-frequency approximation is made. If the squared target fidelity
F_u=<phi_u|rho_u|phi_u> is at least 1-epsilon_F, trace distance gives
Pr_(rho_u)(S_u)>=1-eta_u-sqrt(epsilon_F). Combining with (17)-(18),

    A_u*max(0,1-eta_u-sqrt(epsilon_F)) <= r(u)/tau.          (19)

Thus even a filter optimized with full knowledge of the target law must
respect this bound. It is not an artifact of the Klein envelope being loose.
Postselection success and conditional fidelity have not been conflated.

### Gaussian Likelihood Mass And Source Weight

For Z=pi*||C_1||^2/s_G^2 and 0<=beta<1, Poisson summation gives

    E exp(beta*Z) <= (1-beta)^(-d/2).

Indeed the scalar MGF is theta(s_G/sqrt(1-beta))/theta(s_G), and its Poisson
form is at most (1-beta)^(-1/2). Conditioning each digit on [-R,R] only
decreases this increasing moment. For t>d/2, Chernoff therefore yields

    Pr[Z>t] <= epsilon_rad(t),
    epsilon_rad(t)=exp(-t+d/2+(d/2)*log(2*t/d)).             (20)

Every c_1 with Z<=t has probability >=exp(-t)/W^d. Its evaluation residue
has at least that mass, even when evaluation is not injective. Set

    tau=exp(-t)/W^d.

Equations (18)-(20) imply E_r eta_u<=epsilon_rad(t). Also
E_r[Q*r(u)]=1+chi2(r). For any 0<eta_0<1 and kappa>0, except on source
mass at most

    epsilon_rad(t)/eta_0 + (1+chi2(r))/kappa,

every branch with F_u>=1-epsilon_F satisfies

    A_u <= kappa*exp(t)*W^d /
             [Q*(1-eta_0-sqrt(epsilon_F))],                 (21)

provided the denominator is positive. Cap probability bounds at one.
No condition on chi2(v) is needed. If only E_labels chi2(r) is bounded,
the same calculation gives a JOINT source/label exception bound, conditional
on the specified label event; it is not a per-label certificate.

This bound permits an efficient constructor that genuinely changes the
rest marginal. Amplitude amplification itself can mix the rest register;
(21) bounds the base filter's success, and hence its USUAL A^(-1/2)
amplification proxy, not the runtime of every structured circuit using it.

### Reference At The Current Three-Block Widths

Use the moment-source widths in `STRUCTURED_EDCP_IDEAL_COLLISION_CORE.md`,
t=d, eta_0=0.1, epsilon_F=0.01, kappa=100 and R=ceil(sigma*sqrt(d)).
For a conservative analytic bound use W<=theta(s_G) in (21). The information
references are conditional on the binary-rank event; its probability and
the full physical-source ledger remain separate.

| d | log10 upper A_u on the good event | log10 lower usual A_u^(-1/2) proxy | upper exception reference |
|---:|---:|---:|---:|
| 64 | -828.536070376 | 414.268035188 | 0.010546722 |
| 256 | -3830.11817814 | 1915.05908907 | 0.010000175 |
| 1024 | -17276.0091241 | 8638.00456205 | 0.010000011 |

These 140-digit formula references use conservative rounded chi-square
inputs 0.000280,0.0000175,0.00000110. They are not interval certificates,
executed rejection samplers or quantum resource estimates for all algorithms.
The radial exception uses epsilon_rad(d)=(2/e)^(d/2). In particular the
claim here is about 0.99 squared fidelity on most source fibers, not exact
preparation on an adversarial worst-case residue.

### Preparation Error Must Not Hide The Acceptance Scale

A polynomially small ADDITIVE approximation error cannot automatically be
ignored beside an exponentially small acceptance bound. More generally, if
the actual proposal/instrument only guarantees rest marginal domination
by c_dom*mu_rest plus additive leakage ell_u on the relevant event, then
the right side of (19) becomes

    c_dom*r(u)/tau + ell_u.                                (22)

An ell_u of 0.001 destroys the displayed exponential upper bound. A
multiplicative marginal guarantee, or sufficiently small charged leakage,
is needed to transfer that scale to an implementation. The Gaussian
constructor can in principle be specified to much higher precision; do not
assume its proof merely from a generic TV tolerance. Physical source error
in the frequency law and proposal-preparation error are distinct quantities.

### Checks And A Deliberate Escape Control

Targeted references actually run on 2026-09-27:

- 3,420 positive capped-likelihood filter controls with Q=3,5,11 checked
  (19), including exact-target and approximate-target filters. Another 684
  full complex controlled two-dimensional contractions checked marginal
  domination and fidelity. Gaussian structure was not needed for these
  algebraic controls. NumPy seed 20260927.
- 108 source-weighted tail identities verified (18) independently by
  summing all frequencies. Twelve discrete Gaussian radial convolutions at
  d=2,4,8 and s_G=0.3,0.8,1.4,3 respected (20). Their digit sums were cut
  at ceil(8*s_G), so these are finite numerical references.
- The three growing-width analytic rows above were evaluated, retaining
  the positive radial tails and conservative information inputs.
- Outside the contract, take p=(0.99,0.01), v=(0.01,0.99), u=0. A
  two-dimensional Householder transformation sends sqrt(v) to the normalized
  target rest amplitudes (1,1)/sqrt(2) with probability and fidelity one.
  At tau=0.5, misapplying (19) would say 0.5<=0.0396. This transformation
  MIXES rest labels, so the countercontrol confirms the exclusion is real.
  It is an explicit small algebraic control, not a scalable constructor.

Gemini should extend the existing Klein checker with the effective successful
map's rest-label support, c_dom/leakage, tau/t, radial tail, density exception,
success and squared fidelity. Do not report the exponential acceptance scale
when additive leakage dominates it. Keep cross-block mixing, informative
conditional-core proposals and genuinely quantum basis construction open.
The next theory pass must construct such an operation, not merely choose a
more elaborate scalar rejection envelope for the same unconditional proposal.
