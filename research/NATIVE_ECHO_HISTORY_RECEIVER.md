# Multi-Round Echo With Explicit Mediator Histories

LOCAL CONSTRUCTION / REVIEW PENDING. Original native source access, not circuit
search over invented oracles. No efficient decoder, novelty or speedup claim.
This tests an actual escape from the one-echo obstruction, rather than treating
an uncovered architecture as evidence of advantage.

## Actual Receiver

Use the even-native original batch and split in
[the partial-echo specification](NATIVE_PARTIAL_PHASE_ECHO.md). M=m+w,
q=3^r, s in Z_q^n, F_A,F_B sums of the original public frequency pairs.
Apply public per-copy phase settings ONCE at input. For each committed K_l,

    R_l = inverse_F3_B D_(K_l)^dagger inverse_F3_A D_(K_l),
    D_K |x,y> = chi_q(F_A(x)^T K F_B(y)) |x,y>.

Apply R_(d-1)...R_0 to the SAME batch without intermediate measurement or
repreparation. Each round computes frequencies, phases, clears A scratch,
transforms A, computes the UPDATED A frequency, undoes the phase, clears BOTH
frequency registers, and transforms B. Unknown preparation/inverse, cloning
and fiber access are absent. Gate counts grow by d, source copies do not.
Peak frequency scratch is unchanged because it is cleared between rounds.
Public arithmetic workspace and finite-precision hardware synthesis are owed.

Multiple rounds are outside the single-echo shifted-probe theorem. Even for
one round, A-independence cannot be inferred just from the schedule's matrix:
the policy generating that matrix matters. The resource ledger keeps those
premises separate.

## Exact-Form Conditional Contraction

For mediator word y and A wire i define the three-entry phase diagonal

    P_(i,l)(y)[j] = chi_q(f_i(j)^T K_l F_B(y)),
    U_(i,l)(y) = P_(i,l)(y)^dagger inverse_F3 P_(i,l)(y),
    psi_i(s)[j] = chi_q(s.f_i(j)-eta_i(j))/sqrt(3).

A mediator history is h=(y_0,...,y_(d-1)). Put

    L_i(h,s,a_i) = [U_(i,d-1)(y_(d-1)) ... U_(i,0)(y_0) psi_i(s)]_(a_i),
    W=3^w, H=W^d, y_d=b.

The final amplitude is

    W^(-(d+1)/2) sum_h
      chi_q(s.F_B(y_0)-eta_B(y_0))
      product_(l=0..d-1) omega_3^(-y_(l+1).y_l)
      product_i L_i(h,s,a_i).

This is a mediator-history tensor contraction. It enumerates H=3^(wd)
histories, not the 3^M original cube. The streaming program costs
O(H*d*m*n^2) modular arithmetic/phase work, plus polynomial input validation.
Working storage is polynomial in m,d,w,n,r and the W mediator-word list;
histories themselves are streamed. It uses numeric phases and is not a
certified large-size stable likelihood implementation.

The exponent is w TIMES d. Constant d and logarithmic w permit polynomial
conditional contraction; logarithmic d and logarithmic w generally do not.
No efficiency claim may ignore this product or silently truncate histories.
Evaluating P(outcome|GIVEN s) does not recover unknown s. The report's MAP
reference still enumerates every q^n hypothesis and every 3^M output.

The general tensor-network simulation perspective is established literature:
[Markov and Shi](https://arxiv.org/abs/quant-ph/0511069). The concrete history
formula here is a local derivation, not a claim that contraction itself is new.
Do not mistake conditional classical simulation for a quantum-input
dequantization theorem or an efficient algorithm for HSP. The distinction
between an information-optimal measurement and its efficient implementation
is central in [Bacon, Childs and van Dam](https://arxiv.org/abs/quant-ph/0504083).

## Physical Dephasing And Same-Copy Baseline

Dephase the FULL B WORD in the computational basis before EACH echo round.
The first word is uniform; after each B Fourier, the next word is uniform
given the previous complete trajectory. Conditioned on h, A is a product of
the local U_i history states. The final B output b is uniform. Thus

    P_dirty(a,b|s) = 1/(H*W) sum_h product_i |L_i(h,s,a_i)|^2.

This is full-word history dephasing, NOT tracing only frequency scratch.
Frequency collisions could preserve more coherence; do not import this law
into an uncleared-F_B circuit. Tests attach physical dephasing channels to
the full batch and replay every round independently of the history formula.

Cauchy gives P_clean(a,b|s) <= H P_dirty(a,b|s), pointwise for every secret
and cohort. H can be large; this is not a weak-inference impossibility bound.
In particular it does not bound advantage above the chance level1/3 by a
small quantity. A polynomial domination factor alone does not supply a
sampler for P_clean under unknown s.

The matched baseline draws h CLASSICALLY and uniformly, applies the known
local A unitaries, measures A, and measures the original B inputs separately
with their initial settings and inverse_F3. It retains h and all A/B data,
uses exactly M original quantum samples, and only single-copy quantum gates.
Discarding h and the B input readout simulates the dirty output, so the
baseline is at least as informative as that dephased channel. It is LOCC,
not an algorithm operating solely on classical labels. Its optimal reference
decoder is exponential, just like the coherent comparison's decoder.

## Predeclared Controls And Outcome

Twelve full-IID cohorts: three seeds at each (q,n,M,w) in
(9,1,4,1), (9,2,4,2), (27,1,5,1), (81,1,6,1). Five public THREE-round policies:
zero/product, fixed repeated lens, fixed alternating lens, full-A inverse
calibrated alternating lens, and calibrated two rounds followed by product.
Two initial-setting policies are retained. Calibration failures return zero
without rejecting source rows. No coupling is selected using the hidden secret.

All96 non-product records lose to their OWN matched history-LOCC baseline.
The largest coherent-minus-baseline difference is approximately -0.090418
for full MAP and -0.037995 for least-trit MAP. These are conditional finite
controls, not a source-population or arbitrary-depth theorem. A best-policy
selection made by enumerating all secrets is not an efficient search policy.

Zero lenses check a misleading failure mode: two or four inverse_F3 rounds
produce computational-basis measurement of this phase-only input and hence
uniform outputs, with no secret information. Three rounds give the forward
Fourier product measurement, whose MAP equals the one-round inverse Fourier
measurement after outcome relabeling. Repeated gate count alone is not progress.

The independent Q(zeta9) checker replays all ten policies of the complete
q9,n1,M3 control. Clean probabilities, clean MAP comparisons and pointwise
history domination are exact cyclotomic checks. Baseline path probabilities
are exact; their reported full/trit MAP sums are independently NUMERICAL
maximizations, not certified algebraic-sign decisions. Other cohorts remain
numerical references. Neither checker certifies asymptotic performance.

## Decision And Falsifiers

This particular small-mediator three-round family is deprioritized. Do not
keep expanding a coupling menu without an algebraic reason for extracting an
informative feature and an efficient decoding strategy. Larger depth, wider
mediators or different transforms remain logically open, but an uncovered
case is not promising evidence. Every larger schedule must charge 3^(wd)
contraction and confront strong same-input baselines.

Falsifiers: streaming amplitudes differ from physical replay; history
probabilities fail normalization; dephasing is confused with frequency-class
pinching; clean likelihood exceeds the Cauchy factor; decoder enumeration is
hidden; or finite cohort optimization is promoted to scalable advantage.

```
python theorems/native_echo_history_receiver.py --write
node research/certificates/native_echo_history_receiver_crosscheck.js
python -m pytest -q tests/test_native_echo_history_receiver.py
```
