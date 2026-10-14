# Known Full-System Reflection Tensor Simulation

Local constructive derivation / external review pending. This closes another
specified receiver family on classically prepared phase records. It is NOT
a no-go for quantum HSP inputs, entangled work-register programs, or LWE.

## Scope

Start with the known indexed cohort seed from the coherent reflection audit:

```
W = sum_b |b> tensor product_j psi_bj,  ||W||^2=B
```

The physical initial state is W/sqrt(B). Allowed operations are known
single-factor qutrit unitaries and FULL-SYSTEM reflections I-2WW^dagger/B
about such known seeds, followed by computational measurements of all
factors. The explicit simulator implements F3 and root-diagonal local gates
and the actual same-bank full-system reflection. It has no hidden-secret
input, ideal source oracle, root table, or exponential basis table.

Write the current vector as sum_r c_r tensor_j v_rj. Local gates change one
factor and do not increase tensor rank. A full-system reflection subtracts
2<W,v>/B times W, adding at most B terms. After T reflections the stored
term count is at most B*(T+1), independently of 3^M. Scalar overlaps and
norms use pairwise products of local inner products. This is a computational
classical counterpart, not merely statistical dominance of original data.

The source's index is one B-dimensional factor, with B polynomial in the
declared source bank size. The actual known recipe already pays O(B*M)
original access; no free exponentially large index is smuggled into the
simulation. Multiple seed registers, subsystem reflections with entangled
work, intermediate entangling gates, and arbitrary controlled group/work
operations are not admitted by analogy. Unknown quantum-only seed factors
cannot be inserted into this classical simulator.

## High-root precision without a field table

Known exp(2*pi*i*k/q) entries are approximated by exact dyadic complex
rationals. Cosine uses the existing Machin/Taylor enclosure at 2h+16 bits;
its midpoint is rounded to a dyadic grid of that precision. Sine is obtained
with the correct sign and sqrt(1-cosine^2), using h+8 square-root bits.
The square-root continuity bound |sqrt(x)-sqrt(y)|<=sqrt(|x-y|) is why the
cosine precision is doubled. Scaling by the dyadic midpoint enclosing
1/sqrt(3) gives entry error at most2^-h/4, hence qutrit-vector error at
most delta=2^-h. F3 operator error is at most3*delta by Frobenius norm;
diagonal operator error at most delta. All subsequent complex tensor
arithmetic is EXACT rational arithmetic, not machine complex floats.

For M factors, the coherent seed's relative vector error is at most
e=(1+delta)^M-1, since its index sectors are orthogonal. The approximate
full-system reflection has operator error at most eta=4e+2e^2. It need not
be exactly unitary. With G local gates and T reflections, a safe relative
final vector error is

```
E <= (1+e)*(1+3*delta)^G*(1+eta)^T - 1.
```

This uses a hybrid against the IDEAL unitary program, accounting for the
norm growth of every approximate operator. Normalizing the nonzero final
rational vector costs at most another E in vector distance. Therefore its
entire product-measurement distribution differs from the logical quantum
program by at most min(1,2E) in total variation. This logical simulation
error is not the coherent reflection audit's source-to-ideal-secret error;
we simulate the ACTUAL known noisy point phases. There is no noise-law
promise, independence assumption, or source resampling in this counterpart.

If p=3h+32, all input vector/gate entries have dyadic denominator exponent
at most p. A local factor's denominator exponent is at most (G+1)*p.
Each reflection increases the coefficient denominator exponent by at most
M*(G+2)*p+log2(B). Thus T times that quantity bounds coefficient denominator
exponents. There is no exponential algebraic root-field expansion: bit
length and tensor term count are polynomial in the charged program, phase
description size, and requested approximation precision. The implementation
records actual denominator sizes and enforces a finite term cap.

## Exact finite sampling

Sequentially project one local factor onto each possible basis value, and
compute the branch's exact Gram norm. Norms are nonnegative exact rationals
and sum to the current prefix norm. Scale the dyadic weights to integers
and draw uniformly from their total using finite capped rejection sampling.
No floating probability or exponentially small conditional approximation
is used. Abort explicitly after the cap. Acceptance is at least1/2 per
independent uniform bit draw, so at most N*2^-cap unconditional sampling
error/abort for N factors. Zero-probability outcomes are never selected.
Prefixes are not separately normalized, avoiding reciprocal probability
growth in the tensor representation. Each successful LOCAL draw has the
rational conditional law at that prefix. Conditioning on completion of the
WHOLE transcript need not have the exact rational program law: future abort
probabilities can depend on earlier outcomes. Unconditional errors include
ALL aborts. An exact two-factor control gives completion-conditioned first
outcome9/13 instead of its ideal3/4, and explicitly preserves the abort mass.

This sampler may have variable polynomial work, not a fixed runtime
guarantee independent of the program. Every factor/term/precision query is
charged. Explicit exhaustion or a failed exact probability invariant is
not a promising quantum result.

## Research decision and ways to falsify it

Deprioritize known product-cohort seeds with only full-system rank-one
reflections and local gates, even when M grows and dimension B*3^M is huge.
Persistent coherence alone is insufficient. Require an operation/source
outside this precisely described closure, and then attack that operation
with its own classical baseline. Outside closure is not evidence of speedup.

Falsify this counterpart by finding a permitted operation that grows the
actual stored rank beyond B*(T+1), an incorrect exact Born prefix, a high-root
descriptor needing a root table, a broken rational approximation certificate,
an uncharged precision abort, or a literal quantum control outside its global
TV budget. Do not broaden the conclusion by treating an unimplemented
entangling/subsystem operation as if it were full-system reflection.

Entry points:
`python theorems/known_reflection_tensor_simulation.py --write`
and `python -m pytest -q tests/test_known_reflection_tensor_simulation.py`.
`node research/certificates/known_reflection_tensor_simulation_crosscheck.js`
independently verifies original source receipts, exact error/resource ledgers
and every recorded integer coin decision. It explicitly does NOT reconstruct
the whole tensor computation; small tensor norms/Born prefixes are separately
crosschecked with Python's standard-library rational arithmetic, and high-root
entries with independent high-precision transcendental evaluation.
Finite dense crosschecks validate controls only; the tensor/scalable paths
never allocate the full Hilbert space. Full production admission integration,
independent external proof review, and arbitrary adaptive quantum circuits
remain outside this subsystem.
