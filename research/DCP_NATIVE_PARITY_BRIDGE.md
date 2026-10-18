# A Native Parity Predictor Would Suffice For Cyclic DCP

CONDITIONAL REDUCTION / EXTERNAL REVIEW PENDING. No native predictor, quantum
solver, speedup or novelty claim is supplied. This replaces the stronger and
unnecessary full-vector/sign-orientation proposal in older handoffs.

Run `python theorems/dcp_native_parity_bridge.py --write`. The live receipt is
`reductions/dcp_native_parity_bridge.json`; the precise assumptions and
falsifiers are in `hypotheses/dcp_native_parity_bridge_contract.json`.

## 1. The Missing Primitive

Let q=2^t, n=t-8. A native input consists of IID uniform CLASSICAL full labels
a_j in Z_q^n and corresponding unknown phase qubits

```text
|psi_(a_j)(S)> = (|0> + omega_q^(<a_j,S>) |1>)/sqrt(2),
```

with one fixed uniform S in Z_q^n for an entire invocation. Noise is either
clean, under an explicit predictor contract, or ORIGINAL INDEPENDENT Z faults
with visibility v=1-1/n. An efficient procedure predicting S_1 mod2 with
average advantage epsilon>=1/poly(t), using poly(t) original copies and
finite gates, would suffice to solve clean cyclic DCP in polynomial resources.
It must work at every dimension n>=n0 for a FIXED n0. A large-dimension-only
primitive can have a prohibitive constant tail; it is not silently free.

This is a one-way conditional implication, not an equivalence. Native phase
sources, classical evaluation of a known phase function, coherent label
oracles, and access to a preparer's environment are DIFFERENT access models.

## 2. Exact Random Self-Reduction

Start with scalar clean cyclic-DCP samples (a,|psi_a(s)>), a uniform in Z_q.
For one invocation choose a PRIVATE global r uniform in Z_q^n. For EACH fresh
scalar sample append n-1 fresh uniform auxiliary labels u and apply the KNOWN
single-qubit phase gate with numerator <(a,u),r> modulo q. Then

```text
a*s + <(a,u),r> = <(a,u),(s+r_1,r_2,...,r_n)> modq.
```

For every fixed scalar s, r maps bijectively to uniform S. Augmented labels
are exactly IID uniform and independent of S. The adapter accepts NO scalar
secret. One mask is shared across ALL packets in an invocation; refreshing
it per packet changes the source and can destroy the shared-secret promise.

The predictor sees only labels, phase-qubit registers and public dimensions.
It must NOT receive r, recovered prefixes, preparation angles, injected error
coins or their workspace. In particular r_2,...,r_n are known to the reduction
controller but are UNKNOWN native secret coordinates to the predictor.
`native_decoder_view()` whitelists public metadata; serializing the entire
adapter dataclass does NOT enforce this boundary. Actual quantum/backend
isolation remains unimplemented.

If required, independent Z faults can be injected with exact probability
1/(2n). Uniform k=ceil(log2(2n))-bit words, rejecting values>=2n and applying Z
only on accepted word0, achieve this exactly. Rejection probability is<1/2.
Tags remain private. Marginal visibility alone does not justify independence.

If the native output predicts S_1 mod2, XOR r_1 mod2 predicts s mod2. Global
secret-negation ambiguity does not affect this bit. No full vector, sign
orientation, source inverse, selected rare labels or unknown phase evaluation
is used. Fresh masks, source batches, internal randomness and initialized
workspace make repeated invocations independent for each fixed scalar s.

## 3. Bit Recursion And Honest Tail Cost

Suppose the already recovered low k bits p=s mod2^k are correct. On a FRESH
original sample apply phase -2*pi*a*p/q_original. Its new phase is

```text
2*pi * (a mod2^(t-k)) * ((s-p)/2^k) / 2^(t-k).
```

Truncating an original uniform label preserves uniformity without filtering.
Apply the lift at the current modulus and its current n=t-k-8. For uniform
advantage epsilon and stage error parameter b, an odd
R>=b/(2*epsilon^2) independent predictions have majority error
<=exp(-2*R*epsilon^2)<=exp(-b)<2^-b. Bounds are conditional on earlier prefixes
being correct; a union bound charges the first incorrect stage.

If n0=2, stop at nine remaining bits and enumerate512 suffix candidates.
If the predictor only works for n>=64, the terminal modulus is2^71 and the
tail has2^71 candidates, NOT512. The receipt explicitly displays this case.
For fixed n0 this is asymptotically constant but can be completely impractical;
if n0 grows with input size, the polynomial implication can fail.

To test a complete candidate c, rotate a fresh CLEAN original sample by
-2*pi*a*c/q and measure X. A correct candidate always gives plus; any false
candidate gives plus with average probability exactly1/2 over fresh uniform a:
the nontrivial character sum vanishes even when s-c is nonprimitive.
L independent tests give false survival2^-L. Enumerating K candidates costs
K*L source calls and union error<=(K-1)*2^-L. This verifier is not a supplied
inverse of an unknown preparation. No noisy-majority finishing theorem is used.

The receipt allocates separate stage, false-candidate, bounded-noise-coin and
approximate-control error budgets. At most two known single-wire rotations
per original call suffice for the prefix and mask controls. Their diamond
errors add under the channel hybrid bound, including adaptive execution.
Exact arithmetic takes schoolbook O(n*t^2) bit operations per adapted sample.
Known dyadic phases are exported as Z/S/T and higher dyadic rotation terms.
Higher rotations require finite-gate synthesis; they are NOT unit-cost native
gates. Standard efficient synthesis gives polynomial precision overhead, but
actual finite-gate words are not executed or certified by this module.

## 4. Useful-Bit Access Is Not Total Mutual Information

Fix K TOTAL original native phase qubits, labels A, and uniform S. For Boolean
x in {0,1}^K define full frequency f_x=A*x modq, L=2^K, G=q^n, and
h=(q/2,0,...,0). The difference of the parity-conditioned source densities is

```text
(rho_even-rho_odd)[x,x']
  = (2/L) * v^Hamming(x,x') * 1[f_x-f_x'=h],
```

for independent original Z visibility v. If no target difference occurs,
these two states coincide EXACTLY. No secret-blind postprocessing, adaptive
instrument or joint measurement can produce that bit information. If no
nonzero h in (q/2)*F_2^n occurs, the ENTIRE low secret vector is independent
of all readout. This concerns the uniform prior; leaking a known auxiliary
secret coordinate can unlock an otherwise blind first bit and is prohibited.

Every nonzero signed difference d in {-1,0,1}^K has a unit coefficient, so
A*d is uniform in Z_q^n even though this is not a field. Since h has order2,
d and -d define the same event. Thus

```text
Pr_A[specified bit may be accessible] <= (3^K-1)/(2*G),
Pr_A[any low secret parity may be accessible] <= (3^K-1)*(2^n-1)/(2*G).
```

The artifact uses conservative exact powers from3^5<2^8, not floating
rounding to assert impossibility. These are sufficient high-probability
BLINDNESS bounds, not a sharp accessibility threshold.

### A Stronger Average-Advantage Bound

For clean states let d_f count Boolean preimages of f and p_f=d_f/L.
Each unordered frequency pair{f,f+h} is a rank-two block of the density
difference. Its nonzero eigenvalues are +/-2*sqrt(d_f*d_(f+h))/L, hence

```text
optimal parity success = 1/2 + (1/2)*sum_f sqrt(p_f*p_(f+h)).
```

This handles noninjective maps; counting only distinct frequencies is wrong.
Since positive INTEGER occupancies satisfy sqrt(ab)<=ab, averaging over native
IID labels gives the universal upper bound

```text
E_A[optimal parity prediction advantage] <= min(1/2,(2^K-1)/(2*G)).
```

For original INDEPENDENT Z noise, the entrywise nuclear-norm bound gives the
stronger upper bound min(1/2,((1+v)^K-1)/(2*G)). Summing v^Hamming over all
ordered Boolean pairs contributes L*(1+v)^K. This stronger formula does NOT
follow from marginal visibilities for correlated faults. The clean bound
continues to hold after ANY secret-blind channel by data processing.

At n64,t72, a clean average advantage1/16 requires at least4606 original
qubits by this necessary bound. One width192 packet has advantage<=2^-4417,
despite the earlier conditional total-information lower bound>=16bits.
Exact independent v63/64 noise raises the necessary copy count further.
The receipt uses2*n*t as a non-excluded example budget; it does NOT assert
that this budget suffices or that a decoder exists.

These statements count ALL original draws, including discarded packets. An
adaptive procedure bounded by K IID source calls can be viewed as acting on K
pre-drawn samples. They do not cover a chosen-label/coherent-oracle source,
secret-dependent label laws or an accessible purification.

## 5. What This Changes, And How It Could Fail

The next target is an efficient FIRST-BIT measurement using enough total
original copies, not another one-packet mutual-information plot or a fit with
the simulator's private secret. Testing multi-packet inference must budget
Theta(n*t) copies before even expecting a constant bit advantage. This is
polynomial copy complexity, NOT a computational lower bound or an algorithm.

The reduction fails as an algorithm until an actual predictor is supplied.
Likely failure modes: inaccessible coherent subset-sum operations, exponential
likelihood/measurement compilation, an advantage that vanishes under growing
modulus, incorrect noise/source transfer, or an exorbitant small-dimension
tail. A finite explicit Helstrom measurement demonstrates no efficient method.
The current implementation only certifies identities, conditional resource
implications, and bounded physical controls; external mathematical review is
still required.

The single-bit copy threshold and subset-sum connection are established prior
art, not claimed discoveries: [Bacon, Childs and van Dam](https://arxiv.org/abs/quant-ph/0501044).
Known-angle compilation context: [Dawson and Nielsen](https://arxiv.org/abs/quant-ph/0505030).
