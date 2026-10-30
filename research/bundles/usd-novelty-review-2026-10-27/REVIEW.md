# Bounded Novelty And Usefulness Review

Date: 2026-10-27. Status: completed theorem-level audit; not a circuit or
implementation review. All changes for this audit are confined to this sidecar.

## Decision

**Demote the proposed family-level novelty claim.** Two independent reasons
are now established:

1. The essential exact-unambiguous transfer mechanism already appears in
   DFS24. Its explicit overlap identity gives the same squared-success divided
   by target-normalization factor. Unequal decoding probabilities and syndrome
   characters are a short generalization of that argument, not a new mechanism.
2. The stated complete AG family has a polynomial-time, **matrix-only classical
   bounded-distance decoder**. Ordinary perfect-decoding DQI, using a truncated
   radial Fourier source, consequently gives high-probability quantum search
   and **ideal exact uniform sampling conditional on verification** on the
   same inputs. Neither a supplied curve nor geometry reconstruction is needed.

This does **not** establish a classical algorithm for full-support search or
uniform fiber sampling. A classical decoder executed coherently inside a
quantum reduction is not a classical solution to the reduction's output task.
No reduction from a natural hard task into this exact AG promise was verified.
There is no supported Shor-level or quantum-advantage claim.

The defensible remaining work is an attributed specialization/resource study:
state the exact-herald corollary cleanly, compare the signed-pair implementation
against the matrix-only locator/DQI baseline, and keep search, sampling, and
classical hardness claims separate. Do not use the absence of a found hardness
reduction or an identical displayed theorem as evidence of novelty.

## Native Scope

Write `V = rowspan(B)`, `W = V*V`, and `N = |V| = p^k`. The family under review
has fixed `p=1019` and, for `e>=8`,

```text
m=22e, g=5e+1, deg(G)=10e+3=2g+1, k=5e+3,
V=C_L(D,G), dim(W)=15e+6,
d(V)>=12e-3, d(W)>=2e-6.
```

The decoder argument below only needs the distance and dimension inequalities,
not equality in the Schur-square dimension formula. Generalized evaluation
multipliers, row-basis changes, and coordinate permutations do not change the
argument: compute the square from the actual supplied matrix.

The input interface is `B,s`, with the AG/code promises providing the theorem's
guarantees. It is not a theorem for every full-row-rank matrix: `B=I,s=0` is an
immediate infeasible example. Let

```text
Omega_s = {z in (F_p^*)^m : Bz=s},
lambda_s = N |Omega_s| / (p-1)^m.
```

The reviewed ideal USD result is squared JOINT fidelity `p_bar/lambda_s` after
accepted decoding, and raw verified success at least `p_bar^2/lambda_s`.
Workspace is part of the joint target; inverse decoding need not clean every
work register on the actual postselected state. This audit adopts the prior
review's ideal algebra and does not re-prove it.

## Exact Prior-Art Boundary

### DFS24: Explicit Identity, Immediate Generalization

Debris-Alazard, Fallahpour, Stehle, *Quantum Oblivious LWE Sampling and
Insecurity of Standard Model Lattice-Based SNARKs*,
[arXiv:2401.03807v2](https://arxiv.org/pdf/2401.03807v2), Section 4,
Algorithm 1, Theorem 3, and especially **Lemma 13, equation (22), printed p.29**:

```text
<psi_ideal | psi> = sqrt(q^n / Z_f(A)) p_AGE(A).
```

Their proof eliminates cross terms using unambiguous Gaussian elimination;
failure retains a distinct label. Set `lambda=Z_f(A)/q^n`: the squared
unconditioned overlap is explicitly `p_AGE(A)^2/lambda`. Conditioning on its
exact success sector divides this by `p_AGE(A)`, giving `p_AGE(A)/lambda`.

The full theorem concerns their product-state USD/erasure decoder, efficient
preparation, and normalization/high success for most sampled matrices. It does
not directly instantiate on the fixed AG matrices here. In particular, the
singular full-support local ensemble does not provide their nonzero-probability
single-symbol USD automatically.

**Classification:** explicit special-case identity; immediate proof-level
extension to averaged `p_c` and unit-modulus syndrome phases. These phases
cancel in the surviving diagonal terms. Not a literal published theorem for
the present AG family, but strong prior art against claiming a new generic
zero-error transfer principle.

### Ragavan-Shutty: The Decoder And Syndrome Reduction Are Known

[*Quantum Algorithms for OPI Variants Beyond Locality and Classical
Decodability*, arXiv:2610.00502v2](https://arxiv.org/html/2610.00502v2):
Remark 4.5 already handles arbitrary compatible syndromes by shifting a
particular solution. Lemma 5.2 gives the signed antisymmetric pair isometry;
Lemma 5.3 gives the Schur relinearization and unique-solution-or-failure
decoder. Theorem 5.4 has failure bound `2|V|E+epsilon`, obtained through the
generic Theorem 3.30.

The stronger exact-unambiguity analysis avoids that generic loss. It is an
attributed sharper specialization of the existing circuit, not a refutation
of the more general theorem. The exact numerical bound
`(1-E)^2/(1+alpha)` was not found as a displayed theorem here.

Section 6's auxiliary-code classical attacks also prevent treating a full
Schur cube as a general classical-hardness certificate. The parent's binary
signed-pair implementation is outside this audit; wedge and square-root-SWAP
primitives are not claimed as new.

### Gibbs Through Decoding: Closely Related General Proof

Piveteau, Quek, Franco Garrido,
[*Gibbs state preparation through quantum decoding*,
arXiv:2610.03566v1](https://arxiv.org/pdf/2610.03566v1), Algorithm 2 and
Theorem 3.1, printed pp.18-20, equations (65)-(74), retain a reference label,
postselect correct decoding, and invert the decoder. The theorem bounds
trace-norm error by `p_fail + 2a + a^2`, where `a` measures a coherent bad-branch
sum. Equations (71)-(72) separate the unnormalized ideal state into accepted
and bad contributions.

With a separate orthogonal USD failure flag, the same decomposition immediately
gives conditional squared overlap `(1-p_fail)/lambda`. This is a flagged
extension/specialization of the proof, not its displayed theorem for `F_1019`.
One must not simply set `a=0`: heralded failure still carries coherent norm.

Lemma 4.3 and Theorem 4.1 instead use random-sign averaging. Section 5.2's
dequantization applies to the binary symbol-USD/erasure strategy for commuting
Hamiltonians, not automatically to the q-ary Schur decoder.

### Soft Decoders: Average-Syndrome, Not Worst-Syndrome

Chailloux-Tillich,
[*Quantum advantage from soft decoders*,
arXiv:2411.12553v2](https://arxiv.org/html/2411.12553v2), Section 1.2.1,
explicitly identifies DFS24's unambiguous oblivious sampling. Definition 9 and
Theorem 5 reduce syndrome decoding to dual coset sampling with faithfulness
`1-sqrt(1-P_dec)` and runtime `O((T_dec+T_F)/P_dec)`. Faithfulness is an
**average over syndromes**, although the input matrix need not be random.

This does not by itself supply the desired all-syndrome guarantee. Its
Reed-Solomon/ISIS applications do not map a natural hard problem into the
present arbitrary-divisor, fixed-prime AG promise. The reduction direction
is not a hardness reduction into our target family.

### Other Required Comparisons

| Primary version and location | Verified boundary |
| --- | --- |
| Chailloux-Tillich, [*The Quantum Decoding Problem*, 2310.20651v1](https://arxiv.org/html/2310.20651v1), Sections 4.1, 6.2, Theorem 8 | Symmetric USD and USD-to-erasure decoding are established. Their measured erasure-subset/shortened-code route yields short codewords, not the same retained-label theorem. Section 6.3.1 warns that generic high decoding success alone need not transfer. |
| Horinaga-Yamakawa, [2607.14650v2](https://arxiv.org/pdf/2607.14650v2), Theorem 5.1, printed pp.28-29, equations (19)-(21) | This theorem is for general linear codes, not only MDS codes. It requires polynomial list size, a Fourier tail condition, a coherent tail-sum condition, and target normalization. Those premises are not supplied merely by `p_bar` or by theme similarity. No direct theorem match established. |
| Dalai-Girardi-Lami, [*Zero-Error List Decoding for Classical-Quantum Channels*, 2601.09786v1](https://arxiv.org/html/2601.09786v1), Lemma 3 | Diagonally dominant Gram matrices admit two-supported-row factorizations. An antecedent for pair/list measurements, not a new exact-herald transfer statement. |
| Buzet-Chailloux, [*Fine-Grained Unambiguous Measurements*, 2510.07298v2](https://arxiv.org/html/2510.07298v2), Theorems 5-7 and Section 1.4 | Their limits concern code-independent recovery of parities of symmetric binary states. Section 1.4 explicitly distinguishes this from code-aware discrimination. Not a no-go for the Schur decoder. |
| [*Affine Filtering Measurements and Their Applications to Quantum Decoding*, 2606.07852v1](https://arxiv.org/html/2606.07852v1), Sections 3-4 | Related affine-output unambiguous measurements; not an established instance of the present worst-syndrome guarantee. Screened at framework/statement level, not an exhaustive proof audit. |
| [*Optimization Using Locally-Quantum Decoders*, 2604.24633v1](https://arxiv.org/html/2604.24633v1), Section 7.3, Lemma 4, Theorems 4-5 | Squared overlap and trace-distance guarantees are averaged over character offsets. Theorem 4 gives average trace distance at most `sqrt(epsilon)`. Section 8's Turbo Prange comparison is a warning about matched classical algorithms, not blanket dequantization. |

## Decisive Same-Matrix Baseline

### A Direct Error-Correcting Pair

Couvreur-Marquez-Corbella-Pellikaan,
[*Cryptanalysis of McEliece Cryptosystem Based on Algebraic Geometry Codes
and their Subcodes*, arXiv:1401.6025v3](https://arxiv.org/html/1401.6025v3),
**Definition 5, Section 4.1**, gives the ECP conditions and the associated
polynomial bounded-distance decoding guarantee. Instantiate them with

```text
target code C = V,
A = V,
D_ecp = W^perp,  W = V*V,
t = 2e-7.
```

The following is an independently checked parameter application, not a claim
that this exact AG instance is printed in that paper:

```text
A*D_ecp subset V^perp,
dim(A)=5e+3 > t,
d(D_ecp^perp)=d(W) >= 2e-6 > t,
d(A)+d(V) >= 24e-6 > 22e=m.
```

For the first inclusion, `<a*d,v> = <d,a*v> = 0`, since `a*v` belongs to `W`.
All spaces are computed by Schur products and Gaussian elimination on `B`.
No curve, divisor, evaluation points, hidden partition, or reconstruction
oracle is supplied. The AG promise proves the distances; the algorithm does
not need to solve general minimum-distance computation.

An explicit decoder also checks the application without appealing to a
black-box reconstruction theorem. Given `r=c+epsilon`, `c in V`, with at most
`t` errors:

1. Solve the homogeneous linear conditions `a in V`, `a*r in W`; choose a
   deterministic nonzero solution. Such a solution exists because imposing
   zeros on the error support costs at most `t<dim(V)` constraints.
2. Every solution works: `a*epsilon = a*r-a*c` belongs to `W` and has weight at
   most `t<d(W)`, hence is zero.
3. Therefore `r=c` wherever `a` is nonzero. There are at most `m-d(V)<d(V)`
   remaining coordinates. Solve for the unique codeword in `V` agreeing on
   the known positions by linear algebra.
4. Check membership and distance at most `t`; otherwise return failure.

This is polynomial on the same explicit input and works for every error in
the radius. Outside the radius, final verification prevents an unsupported
bounded-distance answer. In the native parameters, `2t<d(V)` also ensures
uniqueness. A deterministic implementation can be reversibly evaluated and
uncomputed with polynomial overhead; no particular gate count is certified here.

### Why The Filtration Lead Was Not Needed

The same paper's Section 6.2 attacks a public code `C_L(E)^perp`, not simply
`C_L(E)` with the same degree. For target `V=C_L(G)`, the dual presentation has
degree `m+2g-2-deg(G)=m-3=22e-3`, not `22e-1`. The recalled interval
`2g+1 <= deg(E) <= (n-2)/2` occurs in closure/subcode results and is not, by
itself, a theorem reconstructing our desired decoder. Section 6.3 has additional
conditions; Section 6.5 discusses dualizing and shortening. I did not certify
the full ECA bootstrap for these parameters and do not rely on it.

The explicit ECP above closes the access gap directly. The conclusion is
therefore stronger than a geometry-supplied conditional comparison, without
claiming a new general structural attack.

### Truncated-Source DQI

The comparator uses the perfect-decoding Fourier construction underlying
[*Optimization by Decoded Quantum Interferometry*,
arXiv:2408.08292v5](https://arxiv.org/html/2408.08292v5), Sections 3 and 6-7.
The formulas below are this review's direct specialization, not a quotation
of an all-constraints theorem from that paper.

Let `S=(F_p^*)^m`, and let `f=F^dagger |S>` use the normalized uniform state.
Its one-coordinate amplitudes are

```text
f_i(0)=sqrt((p-1)/p),
f_i(x)=-1/sqrt(p(p-1)) for x!=0.
```

Define

```text
tau = Pr[Binomial(m,1/p) <= t],
f_t(x) = f(x) 1[wt(x)<=t] / sqrt(tau).
```

Since `2t<d(V)`, the shifted supports `c+supp(f_t)`, `c in V`, are disjoint.
The locator decoder therefore erases the retained codeword label exactly on
this entire source. For the syndrome character `chi_s`, the ideal output
before Fourier transformation is the normalized state

```text
(1/sqrt(N)) sum_(c in V) chi_s(c) X^c |f_t>.
```

The Fourier output has support only on `Bz=s`. For every full-support `z`,
summing a nontrivial character over nonzero field elements gives `-1` in
each selected coordinate. Consequently

```text
(F f_t)(z) = sqrt(tau)/(p-1)^(m/2),
P_verified(s) = lambda_s * tau.
```

**Conditional on verification the ideal distribution is exactly uniform on
`Omega_s`.** This is stronger than an intrinsic negligible-bias bound. It is
not a claim that finite-precision compiled gates are exact.

A directly prepared normalized truncated source has the displayed trial
success. The radial probabilities can be computed with a polynomial-size
binomial dynamic program; uniform nonzero symbols and the weight-parity sign
complete the source specification. This is not an exponentially large table.
Alternatively, preparing the product source and heralding `wt<=t` succeeds
with probability `tau`; counting that preparation attempt as part of one raw
trial gives `lambda_s*tau^2`. Do not mix these two trial conventions.

A convenient uniform bound is

```text
alpha_dist = (p^k-1)/(p-1)^(12e-3),
|lambda_s-1| <= alpha_dist,
1-tau <= binom(22e,2e-6)/1019^(2e-6) = tail,
P_verified(s) >= (1-alpha_dist)(1-tail).
```

The normalization estimate follows from summing nonzero Fourier characters
of `V`; it is independent of the syndrome. Both errors decay exponentially
with `e`. At `e=8`, the B-only radius is `9`, the source's expected weight is
`176/1019`, and the tail union bound is below `10^-14.299`; the displayed
normalization bound is below `10^-150.369`. Higher entries in the control
script are parameter calculations, not constructed higher-level inputs.

**Theorem-level consequence:** the same-input family already admits ordinary
classical-decoder DQI for both witness search and ideal conditional uniform
sampling. This does not say its concrete gate count or failure exponent beats
the USD implementation. At `e=8`, the supplied USD `E` bound is smaller than
this conservative locator tail. Resource comparison remains legitimate.

### COFI Is Relevant, But Its Saturation Wording Is Insufficient

Matthews-Shapiro,
[*COFI-DQI*, arXiv:2609.31484v1](https://arxiv.org/html/2609.31484v1),
Definition 3.1 and Theorem 3.2, already puts complete Riemann-Roch AG
intersection problems inside ordinary DQI. Map the native task by finding
`z0` with `Bz0=s`, writing `z=z0+c`, `c in ker(B)`, and forbidding `-z0_i`.
The relevant optimization code is `ker(B)=V^perp`; its decoder is for `V`.

Its theorem's saturation wording `s/n=1` must not be used alone to infer a
finite all-constraints guarantee. The cited original DQI Theorem 4.1 and
Section 9.4, equation (138), give an **asymptotic expected fraction** tending
to one. That limit need not imply any probability of satisfying every
constraint. The exact truncated-source calculation above supplies the needed
finite guarantee separately. Geometry-based AG decoders would also be a
conditional comparator, but the matrix-only ECP makes that extra access
unnecessary here.

## Sampling Versus Search

The user's sampling follow-on is correct, with conditioning specified. If the
accepted USD joint state has squared fidelity `F=p_bar/lambda_s` with the
uniform-fiber target and blank work, projecting onto valid data cannot lower
that fidelity. Tracing out work and measuring therefore gives

```text
TV(ideal verified conditional output, Uniform(Omega_s)) <= sqrt(1-F).
```

This is an immediate operational consequence of fidelity and contraction,
not a new USD reduction. In particular, the family bounds give negligible
sampling error when `E` and the normalization error are exponentially small.
For ideal raw verified success at least `beta=p0^2/L`, an entire compiled raw
outcome distribution within TV distance `delta<beta` changes the verified
conditional distribution by at most `delta/beta`. A capped run contributes
its abort probability `eta` if aborts count in the output metric. The cap must
use the actual success lower bound, at least `beta-delta`, not silently the
ideal bound.

Repeated trials do not remove the USD sampler's fixed-input intrinsic bias.
There is no exact-uniform or arbitrary-accuracy-at-fixed-input conclusion
from that bound alone. Easy witness extraction also does not establish easy
uniform sampling. However, the ordinary-DQI comparator above covers the
sampling task too, with exactly flat ideal amplitudes on the verified fiber.

## Useful Tasks And No-Go Scope

**No forward useful-hard-task reduction was verified.** OPI/COFI reformulates
the native code-intersection relation, and Regev/oblivious/Gibbs constructions
turn decoding capability into another quantum task. These facts do not map
worst-case hard instances, practical cryptographic instances, or a natural
hard sampling distribution into this particular fixed-prime, complete-AG
promise. General decoding hardness, restricted Reed-Solomon ISIS results,
and lattice/SNARK applications do not survive a change of matrix family by
assertion. General counting hardness likewise needs promise-preserving
reductions; conditioning or shortening may leave this family.

The requested no-go search yielded scoped warnings, not a universal theorem:

- [*Gibbs Sampling in the Shattered Phase by Decoded Quantum Interferometry*,
  2609.40345v1](https://arxiv.org/html/2609.40345v1), Theorem 3.1 and Section 7,
  has average-sign transfer and a classical Prange sampler matching the
  relevant USD temperatures. Shattering is not unrestricted search/sampling
  hardness.
- Parekh, [*No Quantum Advantage in Decoded Quantum Interferometry for MaxCut*,
  2509.19966v2](https://arxiv.org/html/2509.19966v2), Theorem 3 and Corollary 1,
  shows the pertinent high-girth graph regime is classically tractable. This
  is not a theorem about these AG matrices.
- Anschuetz-Gamarnik-Lu, [*Spin Glass Transitions Obstruct Decoded Quantum
  Interferometry*, 2509.14509v2](https://arxiv.org/html/2509.14509v2),
  Assumption I.5 and Theorems I.6-I.7, concerns specified LDPC ensembles and
  decoder/stability hypotheses. It is not an all-code no-go.

The existing local greedy/fiber-repair results already rule out treating the
implemented degree-eight search instance as an advantage demonstration.
Their finite cutoffs do not prove asymptotic classical tractability; failure
of those baselines does not prove hardness. No full-support classical
dequantization follows from the locator found here.

Calling this Shor-level is unsupported because no comparable useful task,
promise-preserving reduction, or demonstrated separation from the relevant
classical algorithms has been established. This is not a demand for a proven
classical superpolynomial lower bound, which is not known even for factoring.

## Defensible Next Step

1. Attribute the exact-herald transfer to the DFS24 antecedent and its
   immediate generalization; attribute the signed-pair/Schur decoder to
   Ragavan-Shutty. Present the sharpened bound as a useful corollary.
2. Make the B-only locator plus truncated-source DQI the mandatory baseline
   for this family. Any continued claim must be a concrete resource,
   robustness, or broader-promise improvement over it, not the first
   polynomial quantum solver/sampler for the family.
3. Preserve approximate uniform sampling as a distinct task specification,
   but do not label it hard without a matched classical analysis or a
   promise-preserving reduction. The exact ideal comparator prevents using
   that distinction alone to rescue novelty here.
4. Stop this bounded literature audit. The next useful work is the parent's
   implementation/resource comparison or a genuinely new task reduction,
   not further open-ended searches for absent citations.

Suggested modest description:

> An explicit exact-herald analysis and resource realization of a known
> signed-pair/Schur quantum decoder, with worst-syndrome success and sampling
> bounds, benchmarked against a matrix-only ECP/ordinary-DQI construction.

Even this describes a contribution scope, not a certified publication-novelty
claim. Whether the concrete implementation improves resources remains open.

## Evidence And Remaining Qualifications

**Completed independently:** the requested four local reports were read;
the primary statements and proofs identified above were inspected; DFS24's
full PDF equation (22) was checked rather than relying on an incomplete HTML
rendering; the ECP/locator lemma and radial-source formulas were checked
algebraically. The comparison script passed three small Fourier-state cases
across all their syndromes, plus parameter-bound checks. All **16 cached
source hashes** match [source_manifest.json](/Users/jaspersands/Developer/qsearch-research-work/usd-novelty-review-2026-10-27/source_manifest.json).
Reproduce with `python -B comparison_controls.py` in this directory, using a
Python environment with NumPy.

The cached corpus was reused after resumption. Only the user's specific late
Couvreur-Marquez-Corbella-Pellikaan lead was added. Version-pinned references
above define the reviewed corpus; this is not a guarantee that no later or
unlocated result exists. The source manifest records retrieval URLs, UTC
times, byte counts, and SHA-256 hashes.

**Parent-reported, not independently audited here:** the completed binary
signed-pair gate pass; the locator implementation and its actual-matrix,
monomial-transform, and small-RS tests; the latest 611-test combined milestone,
syntax/validation pass, and 20 locator replays. These reports do not substitute
for the theorem checks above, nor are they being re-certified by this audit.

**Not completed or claimed:** a compiled implementation of the ordinary-DQI
comparator; a matched gate-count comparison; verification of all higher tower
source backends; exhaustive prior-art coverage; a natural-hard-task reduction;
classical full-support search or sampling dequantization; or a quantum
advantage. Source-generation costs and finite-precision/channel-error costs
remain charged. The direct ECP resolves the B-only decoding-access issue for
the stated promise, so that issue is no longer an unresolved qualification.
