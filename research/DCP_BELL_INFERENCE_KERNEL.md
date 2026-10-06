# Bell Inference Kernel: Information Geometry And Its Limits

Status: **LOCAL DERIVATION / REVIEW PENDING**. No independent theorem review,
novelty, efficient residue decoder, generic hardness, native-noise reduction,
or speedup claim. This pass compares DIFFERENT candidate-secret laws rather
than treating collision as information. It also attempts to falsify both its
learning and noise interpretations.

## Exact Source-Averaged Cross-Secret Kernel

Use the full conditional Bell law from `DCP_CORRELATED_BELL_READOUT.md`, with
two native carry packets at q=2^t>=8, Q=q/2 and N=2^k. Fix LOW charts,
initial syndromes and XOR outcome u; average all remaining IID higher label
entries. For residues s,t in Z_Q^n define

```text
K(s,t) = E_high [N sum_v p_s(v|u,A) p_t(v|u,A)].
```

Then K(s,t)=1 whenever t is neither s nor -s modulo Q. This holds even when
s and t have the SAME low parity, are linearly dependent, or include zero.
It is stronger than claiming independence only for distinct parity classes.

For a negation orbit of character order at least four,

```text
K(s,s)=K(s,-s)=sum_h 2^-R(h),
```

where R(h) is the selected physical row rank in BOTH charts. This extends the
previous odd-secret condition to every effective character order >=4. For
order one/two, the joint phase is binary quadratic. If its combined alternating
matrix has rank r, K(s,s)=2^(k-r). Translation by u and syndrome origins
change linear terms, not this rank. Zero gives K(0,0)=N.

### Character Derivation

Parseval gives K(s,t)=sum_h E[tau_s(h)tau_t(h)]. For h!=0, some physical
coordinate flips. Its random higher label has character coefficient

```text
s_l (-1)^x(z) + t_l (-1)^x(w)
```

for each secret component l. All these coefficients can vanish only if
t=s or t=-s. Otherwise one nontrivial cyclic character kills every term.
The h=0 term is one. No claim of independence of secret-weighted rows is needed.

If t=s and 2s!=0, cancellation requires OPPOSITE physical signs on every
selected coordinate. The solutions are w=z+h+j, with j in the selected-row
kernel, of size 2^(k-R(h)). Their fixed-low phase cancels exactly. If t=-s,
the same count uses equal signs. Character order two instead leaves the
binary-quadratic radical, giving the separate rank formula above.

The implementation computes off-orbit values without mask enumeration,
including at 64 logical qubits. Diagonal order>=4 rank sums remain exponential
and capped. Clean order-two diagonals use polynomial GF(2) rank. These are
SOURCE-average identities, not predictions for one fixed high-label matrix.

## What This Actually Establishes

Let D0 draw the same public source data and a uniform v. A candidate's density
relative to D0 is f_s=N p_s. Centered densities g_s=f_s-1 have inner product
K(s,t)-1. Representatives of distinct negation orbits are therefore exactly
orthogonal, with squared norm K(s,s)-1. Distinct order>=4 orbits have squared
L2 separation at least 2-2/N.

This proves identifiability modulo sign for the ORDER-AT-LEAST-FOUR class in
this SOURCE-averaged L2 sense. It
does NOT prove polynomial sample complexity, typical-instance separation,
large Hellinger/TV distance, or computable likelihoods. A high spike on a rare
event can have substantial L2 norm and negligible usable probability mass.
All real Bell measurements still alias s and -s; terminal residue verification
and original high-bit completion are separately costed in the previous note.

**Important exception:** zero norm gives no identifiability. For fixed q=8
low charts B1=[[1,0,1,1],[0,1,1,1]] and B2=[[1,0,0,0],[0,1,0,0]], the order-two
residues (2,0) and (0,2) are NOT negations, but both combined quadratic matrices
have rank k=2. Both full laws are exactly uniform for EVERY higher-label table.
The report records this full-rank derivation and 32 physical probability checks;
those checks do not pretend to exhaust all higher labels. Do not turn orbit
orthogonality alone into universal identifiability or omit the norm condition.

## A Scoped Statistical-Query Obstruction

The statistical-query (SQ) oracle estimates expectations of bounded functions
on ONE joint source/output record, instead of providing raw samples. This
distinction is essential; [Feldman's general SQ framework](https://proceedings.mlr.press/v65/feldman17c)
analyzes learning through these approximate expectations, not all classical
sample algorithms. This note derives its own simple orthogonality bound.

Condition the native n by 3n pairs on both first n-column blocks being
invertible, charging that public source filter. For uniform NONZERO-PARITY
residues modulo negation, the number of candidate orbits is

```text
M = [Q^n-(Q/2)^n]/2.
```

Every centered density has the same norm d=Cbar-1, where

```text
Cbar = 2-2^(-2n)
       +(3^(2n)-2^(2n+1)+1)2^(-2n)(3/4)^(2n).
```

For any bounded query phi in [-1,1], Bessel's inequality gives
sum_orbits |E_Ds phi-E_D0 phi|^2 <= d. At absolute tolerance tau, at most
floor(d/tau^2) orbits can differ from the reference response by more than tau.
Follow the adaptive algorithm's reference-answer path. A valid adversarial
oracle can return that same reference expectation for every still-compatible
secret. After T queries, its uniform-orbit identification success is at most

```text
min(1,[T floor(d/tau^2)+1]/M).
```

Query computation is unrestricted. The bound is not a computational time
assumption. Even for fixed q=8, polynomially many inverse-polynomial-tolerance
expectation queries are insufficient asymptotically. This does NOT contradict
the known polynomial algorithms at that modulus: they can use different
measurements or raw sample algebra.

**Attempt to disprove the interpretation:** a Gaussian-elimination learner of
ordinary noiseless parity uses raw equations and is not an SQ learner. Thus
this gate cannot block symbolic transcript solvers, joint multi-record queries,
source re-pairing/chosen sources, unbounded likelihood queries, extremely small
tolerance or other quantum measurements. Do not label ALL optimization methods
SQ automatically. Only an actual reduction to bounded one-record expectations
at the declared tolerance justifies applying the bound. It does warn against
assuming a generic expected-loss/gradient engine will decode the full spectrum.

## Independent Logical Output Noise

Now apply independent bit flips at rate epsilon to each of the k measured
output bits. Let a=(1-2 epsilon)^2. Fourier coefficients acquire factor
(1-2 epsilon)^wt(h), so off-orbit centered kernels remain zero, while

```text
C_epsilon = sum_h a^wt(h) 2^-R(h)
```

for order>=4 secrets. Order-two kernels instead sum these weights on their
quadratic radical. The code checks the noise law by explicit convolution of
the EXACT full physical probabilities, not by multiplying parity marginals.

On the same native systematic source, k=2n and N=2^k,

```text
Z = N+(1+a)^k-1,
E C_epsilon = [Z+((2+a)^k-Z)(3/4)^(2n)]/N.
```

This follows by weighting each disjoint pair by a^wt(h). There are weighted
free-coordinate pairs totaling (2+a)^k; zero-member pairs have weight Z. The
remaining pairs avoid each of the 2n independent pivot overlaps with
probability 3/4.

The leading base is 3(2+a)/8. If a<2/3, equivalently
epsilon>(1-sqrt(2/3))/2, about 0.09175, the mean C_epsilon tends to ONE
exponentially, not merely to a small constant. The threshold equality is not
included. At epsilon=1/8,

```text
0 <= E C_epsilon-1 <= (25/32)^k+(123/128)^k.
```

Crucially this is a JOINT source/output chi-squared bound to a secret-independent
uniform-output reference. Public high labels are retained in that comparison;
they are not averaged away and hidden from the learner. For the declared noisy
measurement, a classical sampler can use the same public source distribution
and uniform v to approximate measured transcripts. It is NOT a classical
replacement for unknown phase-state preparation or all quantum algorithms.

## Native Attempts And Full-Prior Information

The two-prefix success probability is
p_prefix=[product_(j=1..n)(1-2^-j)]^2. For T supplied independent native pairs,
pairing fixed BEFORE higher labels, use this Bell measurement on prefix success
and discard all quantum data otherwise. Rejections are charged. All accepted
noisy FULL outputs are retained, not just a parity.

For the uniform residue prior on Z_Q^n, order<=2 has mass rho=(2/Q)^n. Other
secrets have the preceding source chi-squared d_epsilon=E C_epsilon-1. Using
KL_bits<=2 chi_squared and the trivial order-two output bound k gives

```text
KL_bits to the secret-independent full transcript reference
  <= T p_prefix [(1-rho) 2 d_epsilon + rho k].
I(s;transcript) <= min(n log2 Q, KL_bits),
P(identify negation orbit) <= min(1,2/Q^n+sqrt(KL_bits/2)).
```

The expectation is over the ORIGINAL prior, not a reset adaptive posterior.
The protocol's full classical postprocessing cannot increase this information.
At n=q=256, epsilon=1/8,T=n^2 the exact rational certificate puts orbit
identification below 1/100. Smaller parameter rows remain vacuous when they
are vacuous. No growing-modulus decoder has been supplied.

## Why The Noise Gate Is Not A Fundamental Obstruction

**Readout-only noise has a simple repair.** After H, CNOT the computational
basis value into R-1 clean ancillas and independently read all R bits. Majority
vote changes detector flip probability to the exact binomial upper tail. This
copies a basis observable, not an unknown quantum state. At epsilon=1/8,R=7,
the effective rate is below 1/100 and leaves the uniformization regime. The
module records this countercontrol and gate/ancilla/readout costs. Ideal copying
gates and independent detector errors are assumptions; no backend is certified.

**Fault location matters.** The same observed bit-flip convolution can arise
from independent logical Z errors before H. Post-H repetition copies the
already-corrupted bit and cannot undo that channel. The natural reduction's
original physical phase errors generally become CORRELATED logical errors
K^T e. Neither their independence nor their rate follows from this model.
An actual source-noise theorem, quantum error correction or different protected
measurement is required. This note deliberately refuses that transfer.

**Pairing and quantum processing matter.** Label-adaptive matching, retained
quantum memory, alternate measurements and encoded readout are outside the
fixed fresh-pair protocol. Favorable-source filtering inside its existing
classical transcript pays its native probability, but changing which quantum
packets interfere is a different source distribution and needs a new bound.

The [Bremner-Montanaro-Shepherd IQP noise study](https://arxiv.org/abs/1610.01808)
also makes simulation depend on the circuit/noise regime, including a result
for sufficiently anticoncentrated noisy outputs and a coded escape. We do NOT
import its hardness or simulation results to this native parameter-learning
family; the explicit weighted source moment above is the local argument.

## Revised Research Target

The clean laws have genuine source-averaged separation modulo sign, but generic
bounded expectation learning is a poor bet. The next high-upside capability is
a NON-SQ symbolic/collective decoding route for varying public phase tensors,
or an explicit source-preserving alignment theorem. Known-candidate circuits
are public commuting parity-phase circuits, which provides a representation
bridge to IQP tools, not an automatic algorithm or hardness transfer.

Before optimizing an estimator, require an actual inference primitive, specify
its raw-sample/quantum access, show that source selection is legal, and compose
the native error model. Do not manufacture tiny candidate circuits or promote
the SQ/noise certificates into general no-go results. The highest-value missing
object remains an unknown-residue decoder at growing q.

## Reproduction

```sh
python theorems/dcp_bell_inference_kernel.py --save
python -m pytest -q tests/test_dcp_bell_inference_kernel.py
node research/certificates/dcp_bell_inference_crosscheck.js
```

The live report records 912 exact character kernels at q=8,16,128, including
same-parity different secrets, zero/order-two exceptions, nonzero syndromes
and XOR outcomes. Separate controls exhaust 256 noisy physical-source tables,
16 systematic low-source pairs, exact SQ/noise scaling and the readout-only
countercontrol. Independent arithmetic checks are not independent theorem review.
Production CLI/registry integration and full regressions remain Gemini work.
