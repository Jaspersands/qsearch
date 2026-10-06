# Correlated Carry-Packet Bell Readout

Status: **LOCAL DERIVATION / REVIEW PENDING**. No independent theorem review,
novelty claim, unknown-secret decoder, major speedup, or standard-LWE claim.
This note deliberately moves beyond product extraction: correlated output can
contain useful information even when no public common radical gives guaranteed
secret equations. It supplies exact likelihood primitives and a narrowly scoped
negative result, not an algorithm discovery.

## Input And Observable

Use two independently supplied native packets with the same logical width k,
modulus q=4 or 8, and unknown vector secret s. Their public charts are
x_l(z)=a_l XOR K_l z, where K_l spans ker(B_l), B_l=A_l mod 2. Define
F_l(z)=(A_l x_l(z)-A_l a_l)/2 mod(q/2). The origin contribution is a global
phase. All initial syndrome outcomes are retained; neither repeated labels nor
an unknown preparation inverse is granted.

Apply CNOT from the left logical register to the right, measure the right
register as u, then Hadamard-measure the left as v. The XOR outcome u is uniform
on F2^k, independently of s. Conditional on u the phase is

```text
G_s(z) = s . [F_1(z)+F_2(z+u)] mod(q/2).
P(u,v | s) = 2^(-3k) |sum_z exp(2 pi i G_s(z)/(q/2)) (-1)^(v.z)|^2.
```

There is a plus sign, not a conjugation, between the packet phases. Matching
quadratic tensors, identical labels, and copies of the same state are NOT
required for this physical measurement.

For a nonzero h chosen before inspecting v, retain b=h.v. Its exact joint law is

```text
tau_s(u,h) = 2^-k sum_z i^g_s(z),
g_s(z) = [4/(q/2)] [G_s(z+h)-G_s(z)] mod 4,
P(u,b | s) = 2^-k [1+(-1)^b tau_s(u,h)]/2.
```

The involution z -> z+h makes tau real. Charge the 2^-k XOR probability when
claiming a chosen u; a conditional likelihood is not free postselection.
Several parities of the SAME v are generally correlated. Multiplying their
Bernoulli likelihoods is invalid. Selection after inspecting v requires its
own joint-law calculation.

## Exact Polynomial-Size Compiler

For one packet and offset o, put H_i=K_i.h and
w_li=A_li (-1)^(a_i XOR (K_i.o)) H_i. Then

```text
F_l(z+h+o)-F_l(z+o) = (1/2) sum_i w_li (-1)^(K_i.z).
```

The constant sum is even because B_l K_l=0. At q=8 its Z4 polynomial has
constant (sum w)/2, linear coefficient -sum_i w_i K_ij, and quadratic coefficient
2 sum_i (B_li H_i K_ij K_ih), modulo four. Higher coefficients vanish. At q=4
multiply by two, leaving a binary affine derivative. Thus cubic carry phases
at q=8 still admit exact quadratic parity marginals.

`theorems/dcp_correlated_bell.py` stores coefficients rather than phase tables.
Its `quadratic_gauss` evaluates a Z4 quadratic exactly with rational real and
imaginary parts: split odd linear parity into two affine hyperplanes and use
binary symplectic/Arf elimination on each. The rank is checked independently
with the existing GF(2) rank backend. Construction and evaluation are polynomial
in the explicit public chart dimensions; no 2^k state array is used.

`q4_full_bell_likelihood` computes the FULL correlated joint outcome law at
q=4 by a quadratic Walsh sum. Full q=8 likelihood is deliberately unimplemented:
the undifferentiated phase can be cubic. Neither primitive searches the secret
space. Enumerating q=4 or q=8 trial secrets still costs 2^n or 4^n. Both fixed
moduli are calibration levels, not the growing-modulus breakthrough target.

The quadratic representation is consistent with the Clifford formalism of
[Dehaene and De Moor](https://arxiv.org/abs/quant-ph/0304125). This citation does
not certify the source theorem or decoder proposed here.

## Native Middle-Bit Parseval Bound

Write native q=8 labels as A=B+2M+4T with independent uniform binary matrices.
Fix B, the initial syndromes, u, and a low-defined h. Stack every physical
kernel row K_i for which H_i=1, from BOTH packets, and let their rank be R.
For any fixed secret with s mod2 nonzero, the fresh middle bits randomize the
even linear term of g_s by 2 beta.z, with beta uniform in an R-dimensional
subspace. Its quadratic term is fixed by B,h; residual constant randomness
changes only the magnitude-independent global phase.

For the normalized Walsh coefficients of this fixed unit-modulus function,
Parseval gives sum_beta |a(beta)|^2=1. Consequently

```text
E_(M,T) |tau_s(u,h)|^2 = 2^-R, if s mod2 != 0.
```

Equality follows because the derivative depends only on the selected physical
rows: it is invariant under their common kernel, so all Fourier support lies
inside their span. See the full-output fourth-moment derivation in
`research/DCP_FULL_BELL_SOURCE_MOMENTS.md` for an independent argument that
also applies to every power-of-two q>=8. The condition is essential: an
all-even secret can have bias squared one.
Under the uniform Z4^n prior, that exceptional class has mass 2^-n. Selection
using ALL higher label bits among L low-defined choices is bounded by summing
their squared biases. It does not turn one adaptively synthesized h into an
L=1 low-defined menu.

## Tail-Unit Source Rank Bound

Each packet has native B of size n by 3n. Except with probability less than
2^(1-n) across the two packets, the first 2n columns have rank n. Canonical
RREF then gives n prefix-free and n tail-free coordinates, so k=2n. Consider
the dictionary h=e_(n+j), j=0,...,n-1, on the final n free coordinates.

Conditional on the prefix, systematic tail columns are IID uniform. For one
dictionary member the number C of selected pivot rows across both packets is
Binomial(2n,1/2). Given C>=r=floor(n/2), the first r selected rows project to
IID vectors on the OTHER n-1 tail coordinates. A union bound over their
nonzero linear dependencies gives rank failure below 2^(r-n+1). The selected
free coordinate supplies one additional independent direction. Thus all n
dictionary members have R>=r+1 outside an event with probability at most

```text
epsilon_n = min(1, 2^(1-n)
                   + n [2^(-2n) sum_(c=0..r-1) binom(2n,c) + 2^(r-n+1)]).
alpha_n   = min(1, epsilon_n + 2^-n + n 2^(-r-1)).
```

Missing the full-width/prefix event is CHARGED, not conditioned away. The
finite rank controls are not evidence for the asymptotic bound; the derivation
above, including independence after systematic reduction, is a review target.

## Classical Transcript Information Gate

Protocol scope: T fresh independent packet-pair attempts; one dictionary parity
per pair; all other v information discarded; no retained quantum memory or
reused packets; arbitrary classical history and full public high bits may
choose the dictionary member before v. Include all public source data and u
in the transcript. No external secret-correlated side information is granted.

Replace each emitted parity by a fair coin but keep the SAME public-source and
history-dependent selector transitions. Call this matched reference Q. In bits,
the divergence of a Bernoulli bias tau from a fair bit is
1-H2((1+tau)/2)<=tau^2. This inequality follows from its positive even-power
series whose coefficients sum to one at tau=1. For each fixed odd-parity secret
the fresh-source bound is independent of prior classical history. Average the
all-even exception under the ORIGINAL uniform secret prior, not by resetting
the adaptive posterior to uniform. Chain-rule KL and Pinsker then give

```text
D(P_(s,transcript) || P_s x Q_transcript) <= T alpha_n,
I(s;transcript) <= min(2n,T alpha_n),
P(full identification) <= min(1,4^-n+sqrt(T alpha_n/2)).
```

Every supplied attempt is charged, including failed prefix events and rejected
public outcomes. For n=128,T=n^2 the exact rational certificate proves the
information bound is below 10^-8 bits and identification success below 1/100.
Early small-n rows are vacuous and are retained as such.

This does NOT cover full Bell v, several observables from the same packet,
arbitrary high-bit-dependent parity synthesis, coherent selection, quantum
memory, side information, growing q, or general quantum decoding. A fixed
q=4 arithmetic countercontrol gives full-output Bayes success 7/8 versus 3/4
for one coordinate parity, with no common public radical. Another control has
uniform coordinate marginals but a constrained joint support. These prevent
extending a marginal obstruction to all collective information.

## Literature Transfer Gate And Next Research

[Montanaro's Bell learner](https://arxiv.org/abs/1707.04012) and the September
2026 [sample-optimal stabilizer learner](https://arxiv.org/abs/2609.10974) use
copies of the same unknown stabilizer state. Distinct native carry packets
share s but have different public phase tensors. A same-state copy source or
public alignment map must be proved before importing those sample bounds.

[Arunachalam, Bravyi, Dutt and Yoder](https://arxiv.org/abs/2208.07851) study
learning bounded-degree phase states, including generalized phase functions.
Their fixed-degree learnability does not supply a decoder for varying native
public-polynomial examples or growing carry degree. Both source-model and
degree-dependent resource bounds are required for a transfer.

Highest-value next questions:

1. Formalize FULL-outcome q=4 inference as a structured quadratic matrix-pencil
   problem, then try to decode its varying native examples without secret
   enumeration. Fixed q=4 remains a mechanism control, not a speedup claim.
2. Find a source-preserving collective observable or public alignment theorem
   exploiting shared s across varying cubic packets. Falsify any copy/inverse
   assumption or exponential compatibility rejection immediately.
3. Analyze parity synthesis outside the literal tail-unit dictionary, charging
   its full dependence on label bits and actual optimization cost. A failure of
   the dictionary is not evidence that the synthesis succeeds.
4. Extend an actual decoder through q=poly(n), with sample consumption, errors,
   source coverage and natural-problem reductions explicit. Do not keep scaling
   constant-q plots or known-secret simulations as substitutes for this task.

## Reproduction

```sh
python theorems/dcp_correlated_bell.py --save
python -m pytest -q tests/test_dcp_correlated_bell.py
node research/certificates/dcp_correlated_bell_crosscheck.js
```

The separate Node checker enumerates physical phase differences and exact
integer root counts; it does not reuse Python's Gauss elimination or derivative
compiler. Bounded arithmetic crosschecks are not independent theorem review.
Gemini owns production CLI/registry integration and full regression checks.
