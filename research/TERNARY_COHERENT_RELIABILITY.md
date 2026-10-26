# Ternary Coherent Reliability: Exact Headers And Integer CORDIC

Status: LOCAL DERIVATION REVIEW PENDING. This first-stage artifact implements
message arithmetic and digit-controlled rotations. The immediate follow-up
in TERNARY_CORDIC_STEP.md now ALSO implements the missing reversible digit
generation, full local compute/rotate/uncompute and clean work registers.
The whole growing-block receiver and advantage remain NOT implemented.

Producer: `python theorems/ternary_coherent_reliability.py --write`.
Tests: `tests/test_ternary_coherent_reliability.py`.
Artifact: `research/phase_workbench/ternary_coherent_reliability.json`.

## Question And Prior Art

The signed-trine decoding-to-sampling route needs a known decoder independent
of offset J. Its bounded receiver enumerates coherent herald histories, which
can be exponential. The dephased simplex-grid comparison in
TERNARY_BPQM_CERTIFICATE.md is not that receiver. Can the actual conditional
channel and compression rotations instead have polynomial-width controls,
including exact zero and arbitrarily unlikely branches?

This is implementation work on known message-passing and arithmetic ideas,
not a claimed new decoding paradigm. Piveteau and Renes already identified and
repaired exponential global side information for **binary** BPQM:
[2109.08170v3](https://arxiv.org/abs/2109.08170v3). Their published bounds are
not automatically bounds for the present ternary circuit. Reversible CORDIC
also has prior art, e.g. [2411.14434](https://arxiv.org/abs/2411.14434). The
integer square-root sign comparison below is the local construction being
checked, not a claim that CORDIC or reversible arithmetic is novel.

Claude's corpus query retrieved BPQM_LOG_RELIABILITY.md and
COHERENT_BPQM_TREE.md. The binary log contract is classical-only; the tree
compiler explicitly has exponential herald tables. Neither resolves this
ternary gate question. Claude's rediscovery/failure-mode audit is guidance,
not an expert novelty certificate or a proof of a universal barrier.

## Exact Integer Headers

Keep a nonnegative integer triple n with normalized spectrum n/sum(n), without
GCD reduction. An all-zero triple is a DARK header; it has no normalized
spectrum. It is retained, not omitted or turned into the uniform channel.

For two headers a,b, the actual ternary conventions give:

```
same-symbol node:  n_t = sum_j a_(t-j) b_j
SUM-check herald h: n_j = a_(j+h) b_j
compression fiber t: w_j = a_(t-j) b_j
```

All indices are modulo 3. A nonzero field coefficient +/-1 permutes frequency
indices by that sign. No cyclic gauge, absolute-overlap replacement or herald
phase removal is allowed. SUM-check amplitudes retain omega^(x h); arithmetic
only computes probabilities controlled by the untouched herald.

Let each ORIGINAL leaf have an exact integer header with denominator capacity
Q_i. By induction, sum(n) <= product_i Q_i. Same-symbol sums multiply exactly;
each conditional-check/fiber sum is at most the product of child sums. Thus
physical leaves (0,1,1) on T distinct channels need at most T+1 bits per weight,
even though there can be exponentially many herald histories. The capacity
argument also holds for rational nonphysical control channels.

This does NOT authorize cloning a repeated physical output. Header carries a
numerical capacity, not a proof that a caller's computation tree has distinct
leaves. A graph scheduler must establish that separately. Retaining all node
headers gives polynomial space in tree size, not a constant-space decoder.

### Actual Gate Construction

`message_program(b, kind, signs=...)` compiles to positive controlled-X gates:

1. Standard shift-and-add multiplication using the installed Qiskit CDKM
   half-adder, lowered to its actual CX/CCX operations.
2. Out-of-place products into clean scratch; a CDKM fixed-width adder
   accumulates the required product; inverse multiplication cleans scratch.
3. At most three selector values, each with three terms. This is constant
   field-size branching, NOT enumeration of upstream histories.

The established adder is [Cuccaro et al.](https://arxiv.org/abs/quant-ph/0410184);
the implementation is checked against
[Qiskit's CDKM convention](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.CDKMRippleCarryAdder).
The artifact pins the local Qiskit version; unexpected lowering gates/phases
cause rejection, not silent interpretation as a permutation.

For arbitrary b-bit nonnegative input weights the output width is 2b+2, so
even three maximum-size products cannot overflow. The actual local circuit
uses 14b+11 qubits, O(b^2) bounded-control-X gates, maximum four controls,
and preserves all input and selector wires. Ancillas and outputs must start
clean for the arithmetic law. On dirty inputs it is still a total unitary,
not the same arithmetic specification. Unused qutrit selector |11> writes a
zero header for check/fiber; same-symbol nodes ignore selector altogether.

The source itself constructs every gate, not a mathematical update oracle.
Sparse basis evaluation executes these actual permutation gates; it is not a
full many-qubit hardware simulation. Independent full-statevector tests of
the small multiplier check phases and arbitrary dirty-subspace action too.

## Division-Free Rotation Decisions

For squared amplitudes a,b >=0, write theta=atan2(sqrt(b),sqrt(a)). A Givens
rotation by theta takes (sqrt(a),sqrt(b)) to (sqrt(a+b),0).

Use ordinary vectoring CORDIC with alpha_i=atan(2^-i), retaining signed integer
coefficients P,Q. Initially P=1,Q=0. At iteration i:

```
sigma = sign(P sqrt(b) - Q sqrt(a)), choosing + on equality
P' = 2^i P - sigma Q
Q' = 2^i Q + sigma P
```

The sign is evaluated EXACTLY: handle opposite signs/zero terms first, then
compare P^2 b and Q^2 a, reversing the result when P,Q are both negative.
There is no square root, division, probability cutoff or floating-point
operation in `cordic_digits`. Its Python integers are a CLASSICAL reference,
not a reversible circuit simulation.

For nonzero pairs, if r_i is the residual angle after iteration i then
|r_0|<=alpha_0 and |r_i|<=alpha_i by induction: each step changes r by
sign(r)*alpha_i, and alpha_(i-1)<2 alpha_i. Hence B steps give

```
|theta - sum_i sigma_i alpha_i| <= alpha_(B-1) <= 2^(1-B).
```

This is uniform in a,b; there is no minimum-herald-probability factor. If
a=b=0, the pair is DISABLED and its rotation is identity on the whole block.

Integer widths are explicit. After B iterations,

```
P^2+Q^2 = product_(i=0..B-1) (2^(2i)+1)
|P|+|Q| <= product_(i=0..B-1) (2^i+1) =: S_B.
```

`bit_length(S_B)+1` signed bits therefore suffice, O(B^2). The sign products
need O(T+B^2) bits when the squared amplitudes have O(T) bits. A conservative
schoolbook classical arithmetic construction costs O(B*(T+B^2)^2) bit
operations. Retain-and-reverse simulation supplies a polynomial reversible
construction in principle, but this note does not substitute that existence
argument or the CORDIC paper's different bounds for an actual compiled circuit.
At B=32 this deliberately simple representation charges **500 signed bits**,
not an attractive constant-size arithmetic module.

### Actual Rotation Application

`rotation_program(B, pair)` applies the computed sign register to the qutrit
encoding |00>,|01>,|10>; |11> is fixed. Each microstep has a base Ry controlled
by enabled/pair membership and a sign-controlled correcting Ry. Thus it uses
2B logical controlled rotations per Givens pair, with at most three controls.
It never measures the digits. Arbitrary complex superpositions of all sign,
enabled and data registers are tested against an independent block operator,
including its inverse and every inactive/dark block.

**Interface supplied in the immediate follow-up:** TERNARY_CORDIC_STEP.md
compiles those sign/enabled registers reversibly from integer weights, uses
them and uncomputes them. The current module's `cordic_digits` result is still
only a classical reference; it must NOT be used as classical advice for a
superposition of headers. No published arcsine gate was imported and relabeled
as a complete ternary compiler. This first artifact's false compilation flag
describes its own scope, not the newer follow-up implementation.

Weights used to generate the digits must remain unchanged by the rotation.
At a same-symbol node they depend on retained child headers and the surviving
frequency t, not on the garbage frequency j that the Givens rotations change.
After the rotations, reverse the digit computation, then the weight scratch.
Store node headers/flags until their matching inverse; do not discard or
dephase them. The Givens completion differs from the earlier Householder off
the physical source span, so a future whole decoder must be retested, not
silently substituted into the saved global sampler artifact.

## Uniform Whole-Program Precision

Compress (sqrt(w0),sqrt(w1),sqrt(w2)) by G01 then G02, using pairs
(w0,w1) and (w0+w1,w2). Each ideal-real CORDIC Givens differs from its exact
Givens by operator norm at most 2^(1-B); the composition differs by at most
2^(2-B). This compares the entire unitary, not only typical source vectors.

Let E count EVERY compression occurrence in the full prepare/A/subtract/
A-dagger sampler, including nested root inverses. With exact weight arithmetic,
proper digit uncomputation and consistent adjoints, telescoping gives output
TV perturbation at most

```
min(1, E*2^(2-B) + source_trace_error + sum_of_gate_operator_errors).
```

Orthogonal herald blocks contribute their maximum error, not the number of
histories. Finite gate synthesis and constant-angle rounding must be included
in the separate gate budget; the numerical Qiskit gates do not discharge it.
For E=10^12 and target 10^-3, B=52 suffices for the ideal-angle term alone.
This is an illustrative precision contract, NOT a 10^12-operation run.

If valid distinct-leaf root trees have T=polylog(M), and an offset-independent
global decoder using them really has vanishing word error, the bit sizes and
this arithmetic route are polynomial in M and log(1/epsilon). Neither tree
availability on the saved loopy socket graphs nor that finite-block premise
is established by this pass. The level-13 convergence certificate's enormous
original-tree size remains charged; no practical code length follows.

## Attempts To Falsify And Next Test

- Exhaustive 768 clean one-bit message cases include all weights and selector
  encodings. Larger signed-coefficient cases, maximum weights, complex
  superpositions, scratch cleanup and exact inverse recovery are tested.
- Exact CORDIC comparisons cover all sign combinations, ties, endpoints and
  4096-bit coefficients. Uniform angle/compression checks include ratios as
  small as 2^-2048. Numerical checks corroborate, not prove, the bound above.
- Do not mistake the existence of polynomial arithmetic for a useful native
  sampler. Uniform conditional sampling remains the advantage target, and
  the saved 16/32-spin inputs already have exact classical uniform samplers.
- The construction may be impractical because it keeps O(B^2)-bit CORDIC
  coefficients, large multiplication scratch and all branch history. It may
  also fail to compose with a correct growing-block decoder. A good local
  rotation does not resolve any of those questions.

The immediate next step is now DONE in TERNARY_CORDIC_STEP.md: variable-weight
decisions, updates, coherent rotation and complete arithmetic uncomputation,
with actual gate/qubit counts. It is very expensive, not a practical claim.
NEXT: verify the growing-block decoding/collision premise and compose the
new completion with a root receiver/full unconditional wrapper. No further
threshold or angle-table scans are needed.
