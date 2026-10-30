# Bell Readout Does Not Need Coherent Relative Decoding

2026-10-23. LOCAL COMPOSITION, INDEPENDENT REVIEW PENDING. No novelty or
speedup admission. This follows established transduction and tensor-network
sampling ingredients; it is not a new general simulation principle.

## Concrete Question

The interacting Pauli estimator in the neighboring research bundle addresses
individual expectations, not a joint output distribution. Can the complete
Bell measurement of the relatively transduced TFD instead supply an
advantage? For a source whose Bell outcomes can be sampled classically, the
answer is no under the same polynomial-filter approximation promises.

The classical algorithm is simply: sample a source Bell label u, then return
Mu. Neither phase correction nor a decoder is executed. This does NOT
sample arbitrary measurements of the target TFD.

## Population Identity, Including Bad Decoder Inputs

For a normalized source label state sum_u a_u|u>, the relevant quantum
circuit, just before the final inverse Bell transform, has the form

```
|u>|0> -> chi(u) |u xor d(Mu)> |Mu>.
```

Here M is a public binary linear map, chi is a unit-modulus phase, and d is
any total decoder function, correct or not. Ancillas computing d are
uncomputed. For every fixed output y, distinct source labels u with Mu=y
leave distinct source strings u xor d(y). Tracing that register therefore
gives target-label probabilities

```
Pr[y] = sum_(u:Mu=y) |a_u|^2.
```

The result holds for mixed source states by linearity, replacing |a_u|^2
with their label-basis diagonal entries. It does not require a successful
decoder, source independence across sites, an injective global map, or
knowledge of the phases. It is an equality of populations, NOT states.

Measuring the physical output in its full pairwise Bell basis cancels the
protocol's final inverse Bell transform. Its law is therefore exactly the
classical pushforward above. Relative decoding is essential for coherent
state preparation but irrelevant to this particular measurement law.

## Relation To The Ideal Thermal Target

The previous identity is about the actual circuit's output. It alone says
nothing about closeness to the ideal target TFD. Here is the separate step.
Let Q be a shared polynomial filter of degree D. Under the explicit Pauli
compatibility and relative-distance promises, its coefficient relation is

```
Q(H_A) = sum_u C_A(u) P_A(u)
Q(H_B) = sum_u chi(u) C_A(u) P_B(Mu),
```

and M is injective on the occurring source labels. Since normalized Pauli
vectors form the Bell basis, their Born weights are |C_A(u)|^2 divided by
the coefficient squared norm. Normalized filter Bell laws thus obey

```
p_B,Q = M_* p_A,Q.
```

Let the source and target polynomial-filter states be within trace distance
eta_A and eta_B of their respective canonical TFDs. A classical source
Bell sampler with TV error delta_src then satisfies, by contraction and the
triangle inequality,

```
TV(M_* p_A,implemented, p_B,thermal) <= delta_src + eta_A + eta_B.
```

No probability of a particular label is divided out. There is no rejection,
postselection, decoder-inversion cost, or partition-function oracle. An
efficient decoder is not even needed for this classical consequence: the
coefficient/injectivity and approximation premises suffice. If one instead
uses the quantum circuit's proven trace-distance bound as a black box, the
same conclusion follows by measurement monotonicity, with that bound paid.

The imported ingredients are the coefficient identity and injectivity in
[Shang, Wang and Stilck Franca, Theorem 4.3 and Sec. 4](https://arxiv.org/abs/2610.06667v2),
and their shared polynomial approximation in Sec. 6. These are prior art.
We use their strict degree condition and do not extend it beyond the stated
temperature window. The paper's quantum preparation result remains intact.

## Paying For The Classical Source

For the paper's explicit 1D source, each cell contains a quantum spin q_i
and a central spin c_i. Treat a cell as a constant-dimensional site. The
source Hamiltonian is geometrically 1D with bounded local interactions,
even when its target has nonlocal code parities.

[Kuwahara, Alhambra and Anshu, Theorem 3](https://arxiv.org/html/2007.11174v2#S4.SS1)
provides a constructive relative-Schatten-2 MPO approximation to the source
half-Gibbs operator at fixed inverse temperature. Vectorization converts
this MPO to a low-bond MPS on doubled cells. The Bell transformation is
on-site in this ordering and does not increase the inter-cell bond.

If ||M-F||_F <= epsilon ||F||_F with epsilon<1, normalizing their vectors
changes them in Euclidean norm by at most 2 epsilon. Pure-state trace
distance, and hence any fixed-basis measurement TV, is at most 2 epsilon.
Standard sequential MPS Born sampling supplies source labels, with numerical
sampling error delta_samp charged separately. See
[Ferris and Vidal, perfect tensor-network sampling](https://arxiv.org/abs/1201.3974).

Thus delta_src <= 2 epsilon + delta_samp. This source route needs neither
the worldline chain nor target central-sector sampling. The full ledger is

```
TV <= 2 epsilon + delta_samp + eta_A + eta_B.
```

Cost is one source thermal-MPO construction, polynomial-bond MPS sampling,
and binary multiplication by M for each output. The entire distribution is
not enumerated. Sample independence and finite-precision conditioning must
be handled by the actual sampler; they are not certified by NumPy tests.
No such scalable thermal constructor is implemented in this diagnostic.

For the explicit chain window with code distance d>2 tau N and
beta<tau/(5J0), the shared polynomial degree can lie below d/2 with
inverse-polynomial approximation error for sufficiently large N. The
classical Bell-output consequence applies in that same regime. Do not
pretend that fixed finite N permits arbitrarily small error inside a fixed
decoding degree. This is a different error restriction from the previous
worldline pinning remainder.

## Adversarial Controls

`bell_pushforward.py` has an actual finite circuit and partial trace,
not only a function that directly computes the predicted distribution.
Three complex-state controls use noninjective maps, arbitrary phases, and
deliberately wrong decoder tables. Their target populations agree with the
classical pushforward. The decoder premise is needed for the ideal-target
link, not for this circuit population identity.

The main exact control uses the N=5 version of the native relative-chain
Hamiltonian: 24 terms, noncommuting transverse/longitudinal fields, central
couplings, and nonzero nearest-neighbor ZZ interactions. F=[I_4|all-ones]
has the one-word repetition kernel with distance five. This EASY code is
a proof control, not a quantum advantage instance. All coefficients and
Pauli products are integer-exact; no source state is supplied as hidden
advice and no hiding oracle is fabricated.

For Q=I+H+H^2, degree two satisfies 2D<5. The 234 nonzero source coefficients
map injectively, the target coefficients agree exactly, and the two Bell
laws have TV zero. For Q=I+H+H^2+H^3, the promise fails: 1,099 source labels
map to 1,047 target labels. Coherent coefficient sums still agree, but the
Born pushforward differs from the ideal target by

```
1964880960 / 92843598241  > 0.
```

This counterexample prevents treating linear coefficient transport as a
Born-law identity when collisions are present. Interference and classical
probability addition are different operations.

A second counterexample has two phase-opposite pure states with identical
Bell-label populations but X expectations +1 and -1. It explicitly rejects
the claim that this sampler reconstructs arbitrary coherent observables or
arbitrary output circuits.

## Scientific Decision And Next Work

### Stronger Existing CT-State Baseline For Pauli Expectations

A second pass through prior art makes the following connection important.
[Van den Nest, Theorem 1 and Secs. 4.1-4.3](https://arxiv.org/html/0911.1624)
gives additive classical estimation when a state permits efficient amplitude
evaluation and Born sampling and the pulled-back observable is efficiently
computable sparse. These are computationally tractable (CT) states; MPS are
among the established examples. Efficient basis permutations and phases do
not remove this access. This is a known theorem, not our discovery.

For relative transduction, now ALSO assume the supplied relative decoder
d and phase correction chi are efficiently classically evaluable. Retain
the source garbage g rather than pretending decoding always succeeds. The
pre-Bell target joint state's amplitude at (g,t) is

```
u = g xor d(t)
psi(g,t) = chi(u) a(u) if Mu=t, and zero otherwise.
```

It can be sampled by sampling u and computing (u xor d(Mu), Mu); it can be
evaluated by one decoder call, one source-amplitude evaluation and the
forward-map check. No enumeration or inversion of M is involved. Thus an
MPS source plus this classical decoder gives a CT state INCLUDING garbage,
even for bad decoder inputs. Tracing out garbage is not assumed to retain
a pure target or an efficient pure-state description.

A physical Pauli on the TFD becomes an efficiently computable Hermitian
monomial on target labels under the target Bell transform. Phase conventions
matter: the transform aligning Hermitian Pauli vectors has a diagonal label
gauge in addition to the usual Clifford Bell transform. Diagonal conjugation
preserves monomial sparsity; its efficiently computable phases are retained.
It is not necessary to incorrectly call the entire gauged transform Clifford.

For a target monomial O|t> = nu(t)|t xor v>, sample u, set t=Mu and
g=u xor d(t), then t'=t xor v and u'=g xor d(t'). If Mu' != t', return
zero. Otherwise set a0=chi(u)a(u), a1=chi(u')a(u') and use

```
Y = 2 Re(conjugate(a1) nu(t) a0) / (|a0|^2+|a1|^2).
```

This is bounded by one. Pairing the physical involution (g,t)->(g,t')
proves that its expectation is the actual circuit's Pauli expectation. A
zero denominator can be assigned value zero because it is never sampled.
The implementation tests it against independently constructed target density
matrices for arbitrary complex inputs, noninjective maps, wrong decoders,
and diagonal gauges. It needs source AMPLITUDES and phases, not only Bell
samples; the phase-opposite counterexample above is therefore consistent.

If the normalized MPO source has trace error delta_M and the ideal
transduction approximation has trace error delta_trans, the Pauli bias is
at most 2(delta_M+delta_trans), plus 2 delta_samp and evaluation error.
In particular delta_M<=2 epsilon for the relative-Frobenius guarantee above.
Independent bounded samples give the usual Hoeffding statistical allowance.
Tensor and scalar arithmetic must still be paid and certified in a real
implementation. This finite callback code does not provide that certificate.

This CT consequence does not need a positive worldline representation or
the target's conditional-chain decomposition. A nonstoquastic but bounded
1D source at fixed temperature does not escape it simply by introducing a
sign problem. It DOES need the efficiently computable decoder and source
amplitude access that were unnecessary for the Bell-label sampler.

The neighboring interacting-chain Pauli argument remains useful as an
independent decoder-free route under its stronger sampling/structure
premises. It is not the preferred route when the quantum proposal already
supplies an efficient classical relative decoder and a tractable source.

### Revised Priority

Do not use a full Bell histogram, target-label event, or classical statistic
of these labels as evidence of an advantage for this tractable-source route.
These outputs have a matched classical baseline in the certified regime.
The CT composition also covers additive Pauli expectations when the decoder
is supplied. Neither gives a full computational-basis output sampler after
the inverse Bell transform, joint non-Bell measurement law, or efficient
rare-event conditioning. Single-bit marginals do not determine that law.

The next meaningful constructive task must identify a useful output outside
both attacks and supply a paid source, reduction, measurement, and quantum
runtime. Merely replacing expectation estimation with Bell sampling does
not do it. Conversely, a non-1D or otherwise classically intractable source
does not inherit this baseline for free; its quantum preparation must also
be paid. No additional label-map sweeps or infrastructure are justified.

Before promotion, independently review the shared approximation hypotheses,
source norm/temperature scaling, tensor-network finite-precision contract,
and the exact output basis of any proposed application. A postselected,
adaptive, nonmonomial, or basis-changing circuit is a different task and
requires a new argument. It is not automatically hard.
