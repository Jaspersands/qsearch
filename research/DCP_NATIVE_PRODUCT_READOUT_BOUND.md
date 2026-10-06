# A Native Bound For Nonadaptive Individual Readout

LOCAL DERIVATION / REVIEW PENDING. No independent theorem review, novelty,
accepted candidate, fast native decoder or quantum speedup is claimed.

Follow-up: [fixed-order adaptive audit](DCP_ADAPTIVE_PRODUCT_READOUT_BOUND.md)
allows outcome feedback and retains the resulting odd Fourier characters.
Its bound is much weaker and vacuous with two surplus samples; do NOT extend
this document's exponential suppression to adaptive local readout.

## Why This Is Different

The earlier Fourier-noise converse required a specific conversion to noisy
classical equations. This pass instead analyzes LEGAL measurements of the
actual product phase states. No artificial chosen oracle or Fourier-error
model is introduced.

The [optimal collective measurement/subset-sum connection](https://arxiv.org/abs/quant-ph/0501044)
is prior literature. This local derivation is a sample-budget screen for one
measurement class, not a claim to improve that optimal measurement theorem.

## Native Model

Let q=2^L, G=q^n, and A be IID uniform n-by-m native labels. For uniform unknown
s in Z_q^n independent of A, receive the m phase qubits

    tensor_i (|0>+exp(2*pi*i*<a_i,s>/q)|1>)/sqrt2.

After seeing the ENTIRE A, choose any independent qubit POVM on each qubit.
Private ancillas and arbitrarily many local outcomes are allowed. All choices
must precede measurement outcomes; shared public randomness is allowed.
Afterward, any unlimited classical or quantum processing of the CLASSICAL
record may propose s. Rejections count as unsuccessful.

This does NOT cover entangled preprocessing or choices depending on earlier
outcomes. It also does not cover a larger source pool silently used to select
a favorable batch. Such sampling/selection costs need their own ledger.

## Weighted Classifier Bound

Write each nonzero effect as E_y=w_y*(I+r_y*sigma), with w_y>0,
|r_y|<=1, sum_y w_y=1 and sum_y w_y*r_y=0. Set the reference outcome
distribution to w_y, not a uniform distribution over outcomes.
For phase angle theta, the outcome probability is

    p_y(theta)=w_y*(1+r_yx*cos(theta)+r_yy*sin(theta)).

Let T=sum_y w_y*r_xy*r_xy^T. T is positive, trace(T)<=1. Then

    sum_y p_y(theta)^2/w_y
      = 1 + (cos(theta),sin(theta))*T*(cos(theta),sin(theta))^T
      = c0 + c_plus*exp(2i*theta) + conjugate(c_plus)*exp(-2i*theta),

where c0<=3/2 and |c_plus|<=1/4. The cancellation of the linear term uses
POVM completeness. Unequal weights, out-of-plane effects and many outcomes
do not evade these inequalities.

For fixed A, independent product outcomes have reference distribution
Q(y)=product_i w_(i,y_i). A deterministic maximum-likelihood classifier is
optimal for this classical record, regardless of computational power.
Partition outcome space into disjoint decision regions D_s. Cauchy gives

    P_A(correct)^2 <= (1/G) E_s sum_y p_s(y)^2/Q(y).

Indeed sum_s sum_(y in D_s) Q(y)<=1, while the second quadratic sum is
bounded by sum_s sum_all_y p_s(y)^2/Q(y). This does not assume any particular
decoder, and supports arbitrary abstention or classical postprocessing.

## Public-Label-Adaptive POVMs Still Obey A Common Gate

Expand the product of the local collision functions into characters indexed
by delta in {-1,0,1}^m. Averaging uniform s kills every term unless
2*A*delta=0 modulo q. By triangle inequality and the coefficient bounds,
EVERY choice of POVMs for this fixed A is simultaneously bounded by

    C_A = sum_delta 1[2*A*delta=0]*(3/2)^(m-|delta|)*(1/4)^|delta|.

The bound is attained at the collision-functional level by all-X projective
measurements: equivalently C_A=E_s product_i (1+cos(theta_i)^2).
Attaining this functional does NOT imply maximum decoding success.
Full-A-dependent axes or POVM weights cannot exceed C_A. That is why source
averaging remains legitimate despite adaptive dependence on public LABELS.

For nonzero delta one coefficient is a unit. Hence A*delta is uniform in
Z_q^n and Pr(2*A*delta=0)=1/(q/2)^n. This doubled-character alias term must
NOT be dropped at a two-power modulus. The zero term contributes(3/2)^m;
all coefficient weights sum to2^m. Therefore

    E_A C_A = (3/2)^m + [2^m-(3/2)^m]/(q/2)^n,

    E_A P_A(correct) <=
      min(1,sqrt(((3/2)^m+[2^m-(3/2)^m]/(q/2)^n)/q^n)).

The same squared expression bounds E_A[P_A(correct)^2]. Markov gives a
simultaneous typical-label gate: the probability that ANY allowed product
POVM for A has uniform-secret correctness>=delta is at most that expression
divided by delta^2, capped at1. It applies to source-selected POVMs, not free
selection among exponentially many different input batches.

At native L=4n+1, m=nL+16, n=8,16,32, exact rational arithmetic gives
conservative mean-success bounds2^-50,2^-211,2^-851. The threshold is about
m=nL/log2(3/2) for the first term to become vacuous; avoiding the bound is not
a sufficient condition for efficient decoding. Larger sample budgets remain
open and existing high-sample local FFT baselines are not contradicted.

This is an average-uniform-secret, native-source statement, not a bound for
every individual fixed secret or every individual matrix. A decoder always
guessing one particular secret is an obvious counterexample to that overreach.

## Adaptive Positive Countercontrol

On q=4 and labels(1,2), measure the label2 qubit in X to learn secret parity.
Then measure label1 in X for even secrets, Y for odd secrets. The outcomes
recover EVERY secret exactly. The module evaluates the actual branch
probabilities; nonadaptive all-X decoding succeeds only3/4 and its fixed-A
collision gate is sqrt(3/4)<1.

Thus the fixed-A proof cannot be extended to outcome-adaptive instruments by
pretending they are independent product measurements. The literal label pattern
has native probability1/16; no scalable native selector or adaptive decoder is
implemented. This control also does NOT refute a yet-unproved native-average
adaptive bound. It identifies which step of the present proof stops applying.

The q=2 exception is also explicit: doubled characters all vanish and this
bound becomes vacuous at the ordinary binary linear-algebra width. The code
does not falsely reject that genuinely easy regime.

## Falsifiers And Next Construction

- An allowed fixed-A product POVM exceeding C_A falsifies the coefficient
  argument; completeness and positivity must be checked for every effect.
- A complete native census disagreeing with the alias-corrected mean falsifies
  the source argument. Never assume prime-field character orthogonality here.
- Prior-outcome-dependent axes, entangling gates, access to another unmeasured
  register or favorable batch selection change the model; audit them explicitly.
- Next work should construct outcome-adaptive or native-subgroup collective
  dynamics, or a different arithmetic mechanism. Rotating label-adaptive
  product axes and adding a more powerful outcome decoder cannot fix this
  near-entropy-width obstruction.

## Artifacts

    python theorems/dcp_native_product_readout_bound.py --save
    PYTHONPATH=theorems python -m pytest -q tests/test_dcp_native_product_readout_bound.py
    node research/certificates/dcp_native_product_readout_crosscheck.js

The report contains9 actual product-POVM controls, complete native matrix
censuses,3 growing-modulus ledgers, an order-two ledger and the adaptive
countercontrol. Small calibrations are not algorithm candidates or toy oracle
searches. Independent code checks are not independent mathematical review.
Gemini owns production registry/CLI integration and full production regressions.
