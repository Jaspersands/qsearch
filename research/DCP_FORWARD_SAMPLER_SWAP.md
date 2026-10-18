# Forward Sampler / SWAP Parity: A Clean Route, A Noisy Failure

LOCAL DERIVATION / EXTERNAL REVIEW PENDING. No native sampler, algorithm,
novelty or general negative result is supplied. Run
`python theorems/dcp_forward_sampler_swap.py --write`. The live artifact is
`phase_workbench/dcp_forward_sampler_swap.json`, with matching contract/tests.

This is an attempted CONSTRUCTIVE answer to the useful-bit question, followed
by a stronger self-critique that defeats this particular template under the
independent native noise promise. Clean and other measurements remain open.

## 1. A Forward-Only Physical Instrument

For L=2^K let f_x=A*x in G=Z_q^n and h=(q/2,0,...,0). Original input is the
unknown phase state L^-1/2 sum_x chi_S(f_x)|x>, possibly independently dephased.
Assume a known coherent, read-only full-target-controlled preparation

```text
U_t|0> = sum_(y,g) alpha_(t,y,g)|y,g>.
```

y is a K-bit witness, g arbitrary retained sampler history. Each target's
preparation is normalized, including invalid outputs. No amplitude, phase,
uniformity or history promise follows just from classical solver success.

The proposed circuit:

1. Compute t=f_x+h from the original word, into a blank target register.
2. Apply U_t ONCE to a blank witness/history register, keeping t unchanged.
3. Uncompute the EXPLICIT target using unchanged x. Do not measure t.
4. Verify f_y=f_x+h. On failure output a fair random bit and pay the attempt.
5. On validity, perform a Hadamard/controlled-SWAP/Hadamard test, swapping the
   K original word wires with the K witness wires. Plus guesses even parity.

The validity predicate is symmetric under x<->y because h=-h. The original
unknown input is consumed, never reflected about or prepared inversely.
No U_t inverse is used. Compute/uncompute arithmetic is public and costs
poly(K,n,logq); the forward sampler, its coherent control, witness/history
space, K controlled-SWAPs, flag arithmetic and precision must ALL be paid.
Erasing the computed target is not erasing the sampler's internal history.

## 2. The Exact History-Gram Observable

After step3 the isometry on the original word is

```text
V|x> = |x> sum_(y,g) alpha_(f_x+h,y,g)|y,g>.
```

Let P enforce validity and W swap only x,y. The effective binary-decision
observable, with fair guesses on failure, is O=V^dagger P W P V. In entries,

```text
O[x,y] = 1[f_x-f_y=h] * sum_g alpha_(f_x,x,g)*conj(alpha_(f_y,y,g)).
```

It is Hermitian with norm<=1. For original independent visibility v, EVERY
fixed secret has success

```text
1/2 + (1/(2L))*sum_(x,y: f_x-f_y=h) v^Hamming(x,y)*Re O[x,y].
```

Thus the performance depends on phase-aligned HISTORY OVERLAPS, not just
verified output probabilities. Arbitrary input state tests compare this complex
observable to an actual forward/flag/SWAP statevector instrument. Additional
tests mix every independent original Z error and every finite secret.

### What Works Conditionally For Clean Inputs

If U_t prepares phase-aligned uniform amplitudes on each nonempty fiber F_t,
with a common clean history, O has entries1/sqrt(|F_f|*|F_(f+h)|) on target
blocks. This is the optimal clean parity observable, giving success

```text
1/2 + (1/2)*sum_f sqrt(p_f*p_(f+h)), p_f=|F_f|/L.
```

Empty target fibers may return invalid outputs; their failures are charged.
No full fiber ranking, native quantum input inverse or sampler inverse is
required by this instrument. Preparing the required states remains a severe
computational obligation. A clean garbage promise does not alone fix the
relative phases of the witness amplitudes.

For native IID labels, distinct Boolean words have uniform signed differences,
so E_A sum_f(p_f-1/|G|)^2=(1-1/|G|)/L. Cauchy bounds expected total variation
from uniform by0.5*sqrt((|G|-1)/L). The overlap above is>=1-2*TV(p,uniform).
Hence mean success>=1-0.5*sqrt((|G|-1)/L). At K=log2|G|+4 it is>=7/8,
CONDITIONAL on the missing clean aligned uniform sampler. These source means
hold for each fixed secret; they are not per-label promises.

The actual finite tables are EXPONENTIAL calibration, not an implementation
of this obligation. Generic membership search for a given full target has
marked fraction roughly1/|G| even with many solutions, so its characteristic
Grover search cost is roughly sqrt(|G|), not polynomial simply because K is
larger. This is a cost for that generic method, not a lower bound exploiting
the public arithmetic structure. A genuine structured sampler would matter.

## 3. Try To Kill It: A Single SWAP Loses Noisy Singular Modes

For an unordered frequency pair{f,f+h}, define the positive-entry block
C_f[x,y]=v^Hamming(x,y), x in F_f, y in F_(f+h). Write A_f[x,g]=alpha_(f,x,g).
Normalization of each target preparation implies ||A_f||_F<=1, even with
arbitrarily many history states, invalid witnesses and arbitrarily expensive
computation. Its contribution obeys

```text
Re Tr[A_f^dagger C_f A_(f+h)]
 <= ||C_f||_op * ||A_f||_F * ||A_(f+h)||_F <= ||C_f||_op.
```

Consequently the BEST possible one-SWAP advantage is

```text
sup_U adv = (1/L)*sum_(unordered f,f+h) ||C_f||_op.
```

This is attainable by preparing the leading left/right singular vectors with
one common history. The pairs are disjoint, so these choices are compatible.
The implementation includes an explicitly exponential SVD reference and tests
attainment. A general quantum measurement instead attains sum_f||C_f||_*/L,
the nuclear norm collecting ALL singular modes. Clean C_f has rank one;
independent noise generally destroys that simplifying property. One-SWAP
optimality therefore does not establish general quantum optimality.

### Source-Average Bound Even With A Free Ideal Sampler

There are at most |G|/2 frequency pairs. Cauchy and ||C||_op<=||C||_F give

```text
(sup_U adv)^2 <= (|G|/(2L^2))*sum_f ||C_f||_F^2.
```

Every ordered Boolean pair x!=y hits h with native probability1/|G|. Summing
v^(2*distance) over those pairs gives L*((1+v^2)^K-1). Each unordered frequency
block counts half of this ordered mass. Jensen therefore proves

```text
(E_A sup_U adv)^2 <= (((1+v^2)/2)^K - 2^-K)/4.
```

This bound allows the sampler to depend on ALL labels, v, and unlimited
computation/history. It is not merely a failure of a particular implementation.
At v=1-1/n, K=2*n*t, it is exponentially small in t (hence n for t=n+8).
The live artifact evaluates the exact rational squared bound and rounds OUTWARD
to powers of two; it never uses floating underflow as evidence.

Changing K alone does not fix the native noisy template. For K<n*t/2 the
universal copy bound already gives exponentially small bit advantage. For
K>=n*t/2, (1+v^2)/2<=1-3/(4n) gives advantage<=0.5*exp(-3*t/16).
Thus this single full-word instrument cannot provide an inverse-polynomial
native noisy bit predictor for any fixed K schedule. A polynomial repetition
of its bit-only, independently prepared outputs does not amplify an
exponentially small average distinguishing signal to a constant.

This is NOT a theorem about samplers coherently controlled by the ORIGINAL
word beyond its full target, original-word-dependent history cleanup, adaptively
selected subwords/pools, retained quantum output registers, repeated different
interacting readouts, general POVMs, correlated noise or clean sources. Such
escapes need new source and channel proofs; they are not prohibited. Native
high-rank noise must not be used to dismiss clean scalar-DCP algorithms.

## 4. Concrete Falsifiers And Repairs

The known dyadic-plus-zero-column calibration A=(1,2,4,0) mod8 has a real
H/CNOT uniform sampler: copy three target bits into blank witness bits and
apply H on the free fourth bit. It is NOT native-typical or a proposed new
oracle problem. With the SAME classical output distribution:

- Clean aligned history gives success1.
- A retained target or full-witness copy gives success1/2.
- An orthogonal seed recording the free bit gives success3/4.
- Alternating phases on the two witnesses give success1/2 even with no history.

A known target-copy history can be erased by target-controlled CNOTs BEFORE
erasing the explicit target; no sampler inverse is required. In this calibration
the alternating sign is repaired by a known Z on the free witness wire.
These explicit repairs prevent an overclaim that all sampler history or phases
are inherently fatal. Generic history removal and phase alignment are not free.

At A=(2,2,2,2) mod8,v3/4, the best single-SWAP success is about.747029,
below the full quantum optimum about.793172. The finite controls pay all
invalid outputs, use actual original phase/error states, and do not inspect
private error labels to select favorable branches.

## Revised Priority

Do not develop this exact noisy full-word SWAP template further without an
escape from its spectral restriction. Preserve the clean forward-sampler
route, but require a uniform phase/history-certified native sampler, not
classical success counters. For the noisy route, investigate physical
MULTIMODE block operations, dense nonlinear product-record inference, or a
different source/noise contract. No general active negative belongs in the
registry from this class result.

Prior-art context: the subset-sum/optimal-measurement connection is established
by [Bacon, Childs and van Dam](https://arxiv.org/abs/quant-ph/0501044).
Controlled-SWAP comparison is standard, e.g.
[Buhrman, Cleve, Watrous and de Wolf](https://arxiv.org/abs/quant-ph/0102001).
This local derivation and its tests are not external mathematical review or a
claim of novelty.
