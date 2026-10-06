# Singer Hidden Shifts: Geometry Is Not The Remaining Hard Problem

**LOCAL DERIVATION / REVIEW PENDING.** No novel algorithm, accepted candidate,
general DHSP lower bound or complete classical dequantization. This is a
natural finite-geometry source audit, not a new artificial oracle proposal.
It is a separate source from the power-of-two random-label walk audit: Singer
quotient orders need not be powers of two. No walk-locality bound is transferred.

## Decision

Do not promote finite-geometry Singer shifts as a route to a new Shor-level
algorithm merely because a classical shift search fails and a quantum Fourier
decoder succeeds. Under the declared public-field promise, classical extraction
already exposes a finite-field discrete logarithm. Shor supplies the known
quantum residual solver. Conversely, increasing the base field to make classical
positive samples rare also creates a quantum membership-query barrier.

This adds a necessary classification between "classically dequantized" and
"possibly groundbreaking": **classical extraction plus an already-known quantum
solver**. A surviving classical runtime gap is not evidence of a new mechanism.
The result is not a claim that discrete logarithms are easy classically.

Nor should exhaustive search be the only classical residual comparator.
[Kleinjung--Wesolowski, Theorem1.1](https://arxiv.org/abs/1906.10668) gives
expected time `(p*n)^(2*log2(n)+O(1))` for DLog in F_(p^n), hence quasi-polynomial
time for fixed characteristic. Its theorem statement was checked, not its full
proof or an implementation. This applies to the binary residual, and also to
q=2^b,m=3 with p=2,n=3b IF a field normal/target has been supplied or extracted.
It does not pay the exponential membership sampling/query cost for extracting
that target in the sparse regime. The report records a theorem comparator,
not a runtime benchmark or newly implemented descent algorithm.

## Source, Encoding And Residual Map

Let E=F_(q^m), m>=2, with public field arithmetic and public primitive alpha.
The cyclic projective quotient E*/F_q* has order

`v=(q^m-1)/(q-1)`.

Define the known Singer set by `D(k)=[Tr(alpha^k)=0]`, k in Z_v. The unknown
membership oracle is `D_s(k)=[Tr(beta*alpha^k)=0]`, beta=alpha^s. Our sign
convention shifts D by -s. Public scalar multiplication does not change the
zero predicate, so it is well-defined on the quotient. The binary outputs are
NOT full trace values when q>2.

Recovering the normal line z=F_q* beta gives a public residual:

`gamma=alpha^(q-1), w=z^(q-1), gamma^s=w, order(gamma)=v`.

The unknown scalar disappears because every nonzero base-field scalar has
(q-1)-st power one. This is an ordinary discrete logarithm in a known subgroup
of E*. No inverse oracle, exhaustive field table or secret-dependent operation
is used by the geometry decoder.

The implementation uses FLINT finite fields and modular linear algebra for
prime q<=31 and fields up to2^64. Parameter-only proofs/ledgers also cover
power-of-two base orders. It does not implement arbitrary prime-power nested
field embeddings. Public primitive-element certification currently factors
q^m-1 in bounded controls; this setup is explicitly NOT claimed polynomial-time
classical preprocessing. The extraction theorem takes a valid public primitive
element/field representation as input. Setup cannot be hidden in a speedup claim.

## Classical Reconstruction

### Binary Membership

Over F_2, a zero-membership bit determines the trace value itself:
`Tr(beta*alpha^i)=1-D_s(i)`. Query i=0,...,m-1. The powers of primitive alpha
form a field basis, and the finite-field trace pairing is nondegenerate.
Writing beta in the public polynomial basis gives an invertible m-by-m system
over F_2. Solve it classically in polynomial time to recover beta EXACTLY.

Thus the binary public-reference hidden-shift problem is classically
polynomial-time Turing equivalent to finite-field discrete log:

- Hidden shift -> m membership queries -> beta -> discrete log.
- Given a nonzero DLog target beta, simulate each membership query by public
  exponentiation, multiplication and trace. A classical shift solver gives its log.

The second direction is specific to the binary quotient, where F_2* is trivial.
No unproved general-q root-extraction reduction is being silently invoked.
Even at field degree64, the implemented extraction uses64 queries, not2^64
table accesses. It does not compute the large residual log.

### Other Fixed Base Fields

Draw k uniformly from Z_v and retain positive samples alpha^k. These are
uniform projective points in the hidden trace hyperplane. At current rank r,
the probability that a query adds an independent point is

`p_r=(q^(m-1)-q^r)/(q^m-1)`, r=0,...,m-2.

After collecting m-1 independent points, solve their trace constraints. The
kernel is precisely the one-dimensional normal line. Expected query count is

`E=sum_r 1/p_r < q(m-1)+q^2/(q-1)^2 <= q(m-1)+4`.

To prove the inequality, substitute j=m-1-r and bound
`1/(1-q^-j)=1+q^-j/(1-q^-j)`; summing the geometric remainder gives the stated
upper bound. Each point is computed by known field exponentiation; its
discrete log is NOT needed. A finite budget may fail and must retain that
outcome. Markov gives failure<=E/budget; no finite successful run proves a
typical-source or worst-case runtime statement.

This is polynomial when q is fixed or polynomial in the input length, not
polynomial in log(q) without restriction. An oracle returning FULL trace values
is a stronger interface: m chosen queries recover beta for any base field with
polynomial field arithmetic. The zero/nonzero interface must not be replaced
with those values. Full trace sequences naturally live on E*'s exponent group,
not automatically on the projective quotient's cyclic value encoding.

The full-field classical DLog comparator covers the order-v subgroup residual:
compute the canonical log of w to primitive alpha, then divide that log by q-1.
For valid w it is a multiple of q-1. No general-group descent theorem is assumed.

## Sparse Membership Quantum Query Gate

Here is a separate LOCAL adaptation of a query hybrid argument. It applies to
ANY fixed public subset D of Z_v, cardinality k, not just a difference set.
Hidden shift is uniform among v hypotheses. Initial memory is secret-independent.
The only secret-dependent input is a charged coherent XOR membership oracle;
adaptive queries, arbitrary known computation, measurements purified into
ancillas and reference entanglement are allowed. A supplied beta/program,
secret-correlated state, full-value oracle or extra unknown oracle is excluded.

Compare a T-query algorithm against the same circuit with an all-zero oracle.
At each reference query, averaging over shifts gives marked input mass EXACTLY
k/v, regardless of the known circuit's query distribution. XOR differs from
identity by operator norm at most2 on that marked part. Telescope using the
reference prefixes and the actual unitary suffixes. Cauchy-Schwarz yields

`E_s ||psi_s-psi_empty||^2 <= 4*T^2*k/v`.

The empty-oracle output can guess a uniform s with mean probability at most1/v.
Minkowski on the correct-output projected vectors therefore gives

`mean_s Pr[recover s] <= min(1,(1/sqrt(v)+2*T*sqrt(k/v))^2)`.

The empty oracle is a HYBRID REFERENCE, not a promised Singer instance. The
proof does not assume that the real algorithm forgets classical query records.
Finite ledgers round square roots UP with exact dyadic arithmetic; there is no
floating-point certification. Constant success for Singer density~1/q needs
Omega(sqrt(q)) membership queries. No multi-register decoder can erase that
access cost. For q=2^b,m=3,T=b^2, the certified mean-success bounds at b32/64/128
are approximately .000976563,3.64e-12,3.16e-30. At b8/16 they are vacuous.

This does NOT bound white-box inputs carrying beta, full-value access, generic
injective DHSP functions, supplied phase/coset states, all natural structured
oracles or classical computational difficulty. In particular q=2 is dense,
so this query bound is vacuous there and cannot refute Shor or the known Singer
quantum algorithm. Total implementation trace error must be added if these
ideal bounds are transferred to an approximate physical algorithm.

## Injectivization Is Not Free When Density Vanishes

Let a tuple contain r Boolean translated membership values. Its all-zero output
occurs at at least v-r*k inputs, since the union of r translated positive sets
has size at most r*k. If the tuple is injective, at most one input can map to
all-zero. Therefore EVERY such injectivization needs

`r >= ceil((v-1)/k)`.

For Singer projective planes (m=3), this lower bound is EXACTLY q. It holds
even for carefully chosen offsets and does not require the difference-set law.
Packing the r bits into one function output does not make their r underlying
membership calls free or their exponentially long description polynomial.

For difference sets, the exact nonzero-shift influence is
`gamma=2(k-lambda)/v`. Independent random offsets have union failure bound
`v^2*(1-gamma)^r`. A conservative sufficient r for failure<=1/64 is
`ceil((2*bit_length(v)+6)/gamma)`, using 1-gamma<=exp(-gamma), ln2<1.
Thus the random construction uses O(log(v)/gamma) offsets. Logarithmic size
requires gamma bounded below; for growing-q Singer instances gamma~2/q.
A constant-q theorem cannot silently be transferred to the sparse regime.

## Complete Fourier State And Trivial-Frequency Accounting

For a (v,k,lambda) difference set, put R=k-lambda. Start with normalized
membership phase, apply the known abelian QFT, and cancel nontrivial public
Fourier phases. Let the trivial-character phase be eta=+1 or -1. The ACTUAL
Fourier amplitudes are

`eta*a` at zero, `-b*chi(s)` elsewhere,
`a=1-2k/v`, `b=2*sqrt(R)/v`.

These generic spectral controls use values(x-s), so the recovered translation
is +s; the trace-source exponent convention above translates the set by -s.
Both conventions are explicit in the records and must not be interchanged.

Hence after inverse QFT,

`p_target=(eta*a-b*(v-1))^2/v`,
`p_each_other=(eta*a+b)^2/v`.

Their sum is exactly1: the difference-set identity gives
`a^2+(v-1)*b^2=1`. The leading target term4R/v alone is NOT a probability;
for the Paley11 control it exceeds one. Replacing sqrt(R) with R in the
Fourier coefficient similarly breaks normalization. The literal v16 bent
control has success49/64 for eta+1 and one for eta-1. These details affect
finite controls and prevent false-certification, not a blanket refutation of
known asymptotic mechanisms. All eight controls execute the normalized QFT
pipeline, retaining every output probability.

Computing the correcting diagonal by enumerating a difference set is an
exponential calibration table, not an efficient coherent phase compiler.
Flat magnitude proves that a unitary exists, not that it can be implemented.
An accepted mechanism must provide a uniform public phase recipe, its precision,
coherent workspace cleanup and total costs, and survive the residual-DLog test.

## Attempts To Prove This Audit Wrong

- **Opaque group/field representation:** the classical decoder uses a known
  polynomial field basis and trace pairing. Removing them changes the input
  problem; this audit does not dequantize arbitrary opaque group actions.
- **Growing q:** positive reconstruction loses polynomial bit complexity.
  That is real, but the charged membership-query gate simultaneously worsens.
  A full trace-value or public-beta interface bypasses the gate by adding data.
- **Hidden primitive setup costs:** public certificate construction can be hard.
  The producer logs factorization and does not count it as a proved efficient
  classical preprocessing step. A new reduction must account for its parameters.
- **More quantum memory/adaptivity:** the sparse gate's reference-prefix proof
  allows both. Secret-correlated initial memory invalidates its common reference.
- **Different source operations:** arbitrary full hiding functions and supplied
  states are outside the gate. Do not infer a general DHSP impossibility.
- **Classical recovery overclaim:** geometry is extracted; the large residual
  log is NOT computed. Only v<=128 exhaustive calibration logs are ever run.
- **Literature errors overclaim:** normalization diagnostics are local checks of
  literal formulas. A correct phase/sign convention preserves known efficient
  cases; no claim of refuting the established framework is made.

## Research Consequence And Handoff

Follow-up: [known-solver query closure](SINGER_SHOR_ACCESS_CLOSURE.md) constructs
a paid Shor-coordinate/additive-Fourier route with O(sqrt(q)) membership calls,
matching this sparse gate in query order. It retains every Fourier outcome and
requires no generalized Gauss-sum correction compiler. It is NOT a new algorithm,
an actual Shor compiler or efficient input-bit runtime for unrestricted q.

The next useful target must remove a genuine blocker, not disguise an existing
Shor solver. Seek a consequential source with tractable public spectral/action
structure that does not classically expose an already-solved quantum residual,
or a retained-domain mechanism outside this membership gate. A modification
must identify which premise it changes and why its natural reduction supplies
that stronger interface. Increasing field size, counting easy quantum queries,
or supplying a compiled phase table is insufficient.

GPT should pursue that mathematical mechanism or reduction. Gemini should
integrate this as a residual-hardness/source-access audit, NOT a candidate:
distinguish "already-Shor residual" from "classically dequantized", expose
query/offset costs and phase normalization, and run full production validation.

Files: `theorems/singer_residual_hardness.py`, its matching focused tests,
`research/classical_baselines/singer_residual_hardness.json`, independent
polynomial-field/DFT checker under `research/certificates/`, and matching
hypothesis/source-audit records. Large exponents are decimal JSON strings.

Verified:23 new focused tests; related regression101 passed,1 writer test
deselected in7.39s. The writer test was first run and FAILED at
`tests/test_phase_family_naturalness.py:78` because its scaling record was missing;
that preexisting producer integration defect is delegated, not fixed or hidden.
The independent JS checker replays434 source queries,11138 trace entries,
22 primitive certificates,22 residual witnesses,5 exact ledgers and566 output
probabilities. Independent-language checks are not independent theorem review.
No full production suite, CLI validation, UI change, commit or push is claimed.

## Literature Inspection

[Roetteler's difference-set paper](https://arxiv.org/abs/1608.02005) supplies the
framework and Singer lead; sections3-4 were read in HTML and the v1 PDF. Printed
pages7-8 were visually checked for the literal coefficient/probability formulas;
pages13-14 were text-inspected for the white-box field/Gauss-sum interface.
PDF SHA256: `fe90f4d7322ee6c422f90ea5b9944f3f6a5a0bc279a0499b09083db4864d4fb7`.
The geometry extraction, sparse-query and offset bounds here are local
review-pending derivations, not attributed paper theorems or novelty claims.
[Shor](https://arxiv.org/abs/quant-ph/9508027) is the residual-solver comparator;
[BBBV](https://arxiv.org/abs/quant-ph/9701001) is background for query hybrids,
not a claimed full-paper audit in this pass. The previously missing CFIP
dissertation remains unverified; the university abstract and repository access
attempt did not provide its definition.
