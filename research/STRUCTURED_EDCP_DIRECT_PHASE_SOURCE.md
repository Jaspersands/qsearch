# Structured EDCP: Direct Preparation From Classical Phase Tags

Date: 2026-09-26. LOCAL DERIVATION / REVIEW PENDING.

SIMPLER DISTINCT SOURCE (2026-09-29):
`NATIVE_RLWE_PHASE_DECODER_TARGET.md` prepares phase states from the original
normal-form Ring-LWE sample modulo q, without this note's Q=q^d+1 reduction
or fresh-selector hashing. It retains the hardness bridge and provides a
prior-aware one-block information certificate. Do not interchange the two
state families, label distributions or source-error ledgers.

## 1. Decision And Limits

There is a simpler forward construction of the required coefficient PHASE
states from the retained classical integer instance. Fresh small random
linear combinations provide labels and noisy, CLASSICALLY KNOWN phase tags.
Preparing Gaussian coefficient registers and applying these tags gives a
joint quantum output close to the ideal phase source, within the explicit
width/sample budget below. No final quantum grid, random-code separation
event or unheralded clean-component weight is needed on this route.

`STRUCTURED_EDCP_PHASE_SOURCE_MOMENTS.md` further improves the budget for the
specific upstream Gaussian/secret distribution. Its source-averaged moment
contract is distinct from the bounded-lift contract proved here.

This is not classical simulation of arbitrary measurements. It is a quantum
state-preparation algorithm from classical data. It supplies neither a decoder
nor a hardness theorem for the input family. It does not assert equivalence
of arbitrary EDCP access models. The construction uses familiar small linear
combinations and Gaussian smoothing ideas; novelty is NOT claimed.

The broader width budget changes the next research target. Old numerical
small-width obstructions must be recomputed before being applied here. Read
`STRUCTURED_EDCP_WIDE_PHASE_INFORMATION.md` for information sufficiency,
remaining classical comparisons, and concrete finite parameters.

## 2. Source Contract And Actual Algorithm

Use the notation and source premises of
`STRUCTURED_EDCP_CLASSICAL_READOUT_SIMULATION.md`, sections 2-4:

    d>=2 a power of two, q>=2, Q=q^d+1,
    E(c)=sum_i q^i*c_i mod Q, S_q=(q^d-1)/(q-1),
    A in Z_Q^(M x n), b=A*s+e mod Q.

A's marginal is delta_A-close to uniform. With joint failure probability
delta_lift, the errors fail to have actual integer negacyclic lifts v_j with
E(v_j)=e_j and ||v_j||_infinity<=B. The source, secret, errors and any retained
classical side information are fixed BEFORE the fresh selectors. Correlations
among them are allowed. The sampler does not know s, v_j or e_j.

For even power-of-two K with 2<=K<=2d, independently draw

    U=Uniform{-K/2,...,K/2-1}+Bernoulli(1/2),
    E U=0, v_K=Var(U)=(K^2+2)/12,
    c_K=Pr[U=U']=(2K-1)/(2K^2).

For each requested block l=1,...,L, draw M such entries and compute

    a_l=u_l^T*A mod Q, t_l=u_l^T*b mod Q.                       (1)

For a public amplitude width sigma>0, define s_G=sigma/sqrt(2). Let mu_R
be D_(Z,s_G), conditioned on the symmetric interval [-R,R]. Independently
prepare the d coefficient registers of block l, and apply the known phase:

    |psi_(t_l)> = sum_(c in [-R,R]^d) sqrt(prod_i mu_R(c_i))
                     * exp(2*pi*i*t_l*E(c)/Q) |c>.             (2)

Return a_l and these quantum registers. DISCARD the newly sampled u_l,t_l
and their work registers before invoking the ideal-source contract. Retaining
the original (A,b) and pre-existing source records is permitted. Revealing
fresh tags/selectors is a different joint-output contract, not certified by
the label-replacement step below.

The target has L fresh independent uniform a_l, with t_l in (2) replaced by
<a_l,s>. This target is the coefficient phase ensemble required by the joint
decoder. It is not a coherent superposition over classical labels, a phase
oracle callable on arbitrary inputs, or full coset-state preparation.

## 3. Joint State Error, Including Correlated Source Errors

Fix any good source instance and its lift witnesses. For each i,j let

    z_(i,j)=integer evaluation of X^i*v_j mod (X^d+1),
    k_(l,i)=sum_j U_(l,j)*z_(i,j).

Then z_(i,j)=q^i*e_j mod Q and |z_(i,j)|<=B*S_q. The relative phase between
actual and target JOINT coefficient states is exactly

    exp(2*pi*i*sum_(l,i) c_(l,i)*k_(l,i)/Q).                   (3)

Integer representatives are used inside the bound; they need not be centered.
An untruncated centered discrete Gaussian has

    Var(C)<=s_G^2/(2*pi)=sigma^2/(4*pi).

One proof completes the square in its MGF and uses that shifted Gaussian
mass on Z is maximal at an integer, by Poisson summation. Differentiating
the resulting MGF bound at zero proves the variance bound. Symmetric central
truncation preserves mean zero and cannot increase the variance.

Using |exp(i*x)-1|<=|x|, coefficient independence and zero means gives

    ||Psi_actual-Psi_target||_2^2
      <= pi*sigma^2/Q^2 * sum_(l,i) k_(l,i)^2.                (4)

Pure-state trace distance is at most this vector distance. Conditional on
the source, the independent ZERO-MEAN selector entries give the exact identity

    E_U sum_(l,i) k_(l,i)^2
        =L*v_K*sum_(i,j) z_(i,j)^2
        <=L*v_K*d*M*B^2*S_q^2.                              (5)

Jensen's inequality therefore bounds the averaged cq trace distance, even
if selectors are retained temporarily for this comparison, by

    delta_phase = min(1, sqrt(pi)*sigma*B*S_q/Q
                            *sqrt(v_K*L*d*M)).               (6)

No independence of the amplified errors was used. The stronger witness-based
version replaces d*M*B^2*S_q^2 by sum z_(i,j)^2; it is not an efficiently
observable certificate when those witnesses are secret.

Next discard selectors and tags. Now the target state depends only on s and
the label. The exact composite-modulus hash calculation in the readout note is

    C_hash=(Q^n-2^n)*c_K^M+(2^n-1)*2^(-M), q odd;
    C_hash=(Q^n-1)*c_K^M,                  q even;
    delta_hash=min(1,sqrt(C_hash)/2).

Replacing L selector-derived labels by independent uniform ones costs at most
delta_A+L*delta_hash, while retaining pre-existing classical source records.
This is an ensemble statement, not a certificate for every observed matrix.
Separate the bad-lift event before (4), without conditioning the hash theorem
on an unproved good-instance distribution. The final guarantee is

    D(rho_actual,rho_ideal_R)
       <= delta_A + delta_lift + L*delta_hash + delta_phase
          + delta_implementation.                           (7)

Here D is half trace norm. Classical sampling inaccuracies and circuit/state
errors must be included once, with their actual joint budgets. A marginal
single-block fidelity does not establish (7); equations (3)-(5) are joint.

## 4. Efficient Preparation And The Error Ledger

Finite coefficient-state preparation does not enumerate (2R+1)^d entries.
Prepare a uniform signed integer in [-R,R], compute exp(-pi*c^2/sigma^2)
reversibly, rotate a success qubit with that amplitude, and herald success.
For R=ceil(sigma*sqrt(kappa)), sigma>=1 and polynomial kappa, single-coordinate
success is Theta(1/sqrt(kappa)); all d*L coordinates are prepared separately.
Cap retries and charge the abort probability. Finite arithmetic and rotations
require certified precision; this note is not a compiled circuit. Arithmetic
cost is polynomial in d,L,M,n,log Q,log R and requested precision for this
regime, rather than polynomial in Q or in the support cardinality.

Apply t_l*q^i*c_i mod Q using ordinary reversible modular arithmetic and phase
rotations, then uncompute work registers. No multiplication by an unknown
secret occurs. Any rounded public sigma must meet (6) with its ACTUAL value.

To compare with the infinite coefficient ensemble, use the per-coordinate tail

    eta_1 <= sigma^2/(2*pi*R)*exp(-2*pi*R^2/sigma^2).

Then add sqrt(d*L*eta_1) to (7). For truncated targets this comparison is not
needed. A later conversion to a periodized or Fourier-readout convention has
its own precision/aliasing errors; none is silently absorbed here.

For the reviewed upstream construction, substitute

    delta_A <= delta_amp+delta_eval,
    delta_lift <= delta_err,

from `STRUCTURED_EDCP_UPSTREAM_MIXING_AUDIT.md`, with its explicit sampling
budget. Keep its mathematical and numerical review status. Do NOT use the
unsupported production certification flag; the discrepancies in
`STRUCTURED_EDCP_UPSTREAM_NUMERICAL_REVIEW.md` remain unresolved here.

This direct route removes ONLY the final grid's p0, delta_sep and grid-width
restriction. It does not repair the unaudited reverse reduction, prove the
original input family hard, or eliminate the classical source mixing step.

## 5. Attempts To Overclaim Or Break The Construction

**Unlimited samples.** The available budget is

    sigma*sqrt(L) <= epsilon*Q /
                       (sqrt(pi)*B*S_q*sqrt(v_K*d*M)).         (8)

Holding width fixed does not allow arbitrary samples at fixed error. In the
current polynomial-q source the right side is polynomial in d. A sieve needing
exp(Omega(sqrt(log Q))) ideal blocks is not supplied at fixed useful width by
this certificate. Shrinking sigma exponentially to compensate destroys the
signal, not just the quality of a particular algorithm: for sigma<1,

    Pr_mu[C!=0] <= 2*exp(-2*pi/sigma^2)/(1-exp(-6*pi/sigma^2)).

Every ideal joint state is within sqrt(d*L*Pr[C!=0]) of the SAME all-zero
coefficient state. Uniform-secret success is at most 1/Q^n plus this distance.
This is a limitation of this sufficient source budget, not a universal lower
bound on all possible source constructions.

**Free phase-oracle access.** State error (7) does not imply closeness of
phase unitaries on arbitrary coefficient inputs. At Q=1000, sigma=1, tag error
one, a one-coordinate Gaussian state's distance is about 0.000383273. Yet
the relative phase at c=Q/2 is -1; on a superposition of 0 and Q/2 the two
oracles give orthogonal outputs. New controlled uses, inverse calls, adaptive
coefficients and extra copies require separate analysis.

**Known quadratic phases.** A common public diagonal phase preserves all
pairwise inner products. In position coordinates a centered quadratic phase
exp(i*lambda*(x-z)^2) differs from a public exp(i*lambda*x^2) by the
UNKNOWN linear phase exp(-2*i*lambda*x*z), up to a global phase. One must not
assume access to that missing center-dependent operation. A finite control
below gives a trace-distance obstruction to that particular conversion.
This does not exclude a useful public phase as part of a different decoder.

**Conditioning and retries.** If a decoder selects a favorable label event,
charge its probability. An average label-TV certificate alone does not bound
expected retries for every fixed retained A: a bad A may never yield that
event. A one-batch protocol that declares failure outside the event avoids
this problem. Bounded retries require their own bad-matrix/abort budget.

**Classical simulation.** The readout sampler has the SAME numerical error
term as (6), but replaces one specific measurement, not (2) as an arbitrary
classical quantum-state simulator. Efficient classical descriptions of circuit
inputs do not make general quantum computations classically simulable.

## 6. Bounded Checks Actually Run

Targeted mathematical checks only; no routine production wiring or full suite.

- Ninety-six joint-state controls at (q,d,M,L)=(3,2,3,1),(5,2,3,2),
  (7,2,4,2),(3,4,3,2), widths 0.5,1.3,3, eight instances each. Exact integer
  rotations satisfied (3); finite Gaussian overlaps respected (4). The original
  square-root comparison falsely failed twice when ALL k were zero: overlap
  rounded to 0.9999999999999998. Squared-distance comparisons resolve that
  numerical issue; no algebraic discrepancy was found.
- Twenty-four full cq density comparisons at q=3,5, d=2, M=3, R=1, widths
  0.5,1.3,3, four sources each. All 125 weighted selectors were enumerated.
  Trace norms of the label-indexed density differences respected exact fixed-A
  label TV plus (6). Maximum observed ratio to that bound was 0.54011450.
- An 80-digit check over all 125 selectors for z rows (1,5,-4),(5,-1,-6),
  sigma=1.3,Q=26 had mean squared shift energy 156 exactly. Mean trace distance
  was 0.3834746562 and mean vector-error square 0.1705361366, below the RMS
  bound 1.1068970751 and its square. This particular bound is vacuous as a
  trace-distance guarantee and is retained as an identity/control, not evidence
  of useful parameters. Finite Gaussian sums used [-8,8].
- In a cyclic 128-dimensional reference, real Gaussian amplitude width 8
  and its unit shift have overlap 0.9757550547. Chirping the centered Gaussian
  with exp(-pi*i*x^2/4) BEFORE shifting gives overlap 0.0018221667; chirping
  both original states AFTER shifting preserves 0.9757550547. Trace-distance
  contraction forces uniform conversion error at least 0.3905664586 for any
  common deterministic channel producing the former pair from the latter.

These small finite checks are algebra falsifiers, not candidate algorithms,
evidence of a scaling speedup, or substitutes for independent proof review.

## 7. Literature And Integration Contract

[Chen, Hu, Liu, Luo and Tu, arXiv:2310.00644v2](https://arxiv.org/html/2310.00644v2)
distinguish known amplitudes from unknown-phase Gaussian quantum LWE. Their
sections 3-6 give algorithms and hardness reductions under different phase,
sample and modulus promises. Our coefficient source is not automatically one
of those promises. Neither its growing-sample approximation loss nor a missing
secret-centered chirp can be discarded to import their algorithms. The
construction and bounds (1)-(8) here are local derivations, not theorems
attributed to that paper. No novelty review is complete.

Gemini should implement a separate `direct_phase_tag` source mode, not rewrite
old grid experiment histories. Inputs to its constructor are A,b and public
parameters only. Keep witnesses in reference tests, separate from execution.
Its artifact must distinguish cq-output access from phase-oracle access,
record the full ledger (7), actual width, requested L, discarded fresh coins,
and review status. Tests must include bad selectors, insufficient entropy,
correlated source errors, accumulated copy error, side-information leakage,
and the zero-error numerical case. Repair the upstream certificate FIRST.

The next main-model target is an efficient decoder or conditional arithmetic
map at the newly permitted widths, matched against the existing classical
readout sampler. A source simplification alone is not an algorithmic result.
