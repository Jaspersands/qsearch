# Growing-Depth Native Ternary Phase Hierarchy

LOCAL DERIVATION / REVIEW PENDING. No accepted candidate, decoder, speedup,
generic hardness theorem or novelty claim. This corrects attempts to extend
the fixed-level cubic work in `TERNARY_SCHUR_TENSOR.md` to growing depth.

Successor: `TERNARY_SCHUR_CLOSURE.md` certifies ALL higher mixed top terms
through compact spans and detects saturation into disjoint kernel geometry.
This avoids expanding binomial(k+L-1,L) tensor entries.

## Exact Representation

Use an actual odd-level packet, L=2r+1, with integer secret, parent modulus
3^(r+1), low native labels A and public kernel chart j=x+Vz over F3. Its
surviving component is Q_l(z)=(C_l(x+Vz)-C_l(x))/3 modulo3^r. Measuring the
initial syndrome already loses the original top secret digit. Acquisition of
these intermediate odd-level inputs remains uncharged.

For the three-entry cyclic shift S and Delta=S-I, integer identities give

```text
S^3=I; Delta^3=-3*S*Delta
Delta^(2a+1)=(-3)^a*S^a*Delta
Delta^(2a+2)=(-3)^a*S^a*Delta^2
Delta_2=Delta*(S+I).
```

Apply differences to each three-entry native frequency table, add the physical
coordinates modulo the PARENT modulus, then divide by3 once. This computes an
order-d mixed derivative in O(n*m*d) arithmetic, storing3*n*m local entries.
It never materializes the2^d derivative cube or3^h retained phase table.
Public component arithmetic is not access to the unknown s-weighted phase,
preparation, its inverse, or a measurement on the supplied state.

The normalized phase Q_l/3^r has additive degree at most L=2r+1: every L+1
mixed derivative vanishes. Its highest derivative is constant:

```text
Delta_(u1)...Delta_(uL) Q_l
 = -3^(r-1) * sum_i A_li * product_a (V*ua)_i mod3^r.
```

The minus sign is depth independent; the depth-dependent native residue unit
cancels the alternating sign of the cyclic identity. This is a weighted
L-fold Schur tensor. Discarding its higher orders is not justified by a cubic
fit or by formal polynomial degree in lifted ternary digits.

Sharp native controls at L3,5,7,9,13,19 have respective highest derivatives
1,3,9,27,243,6561 and zero next derivative. The width stays three: growing
additive degree is a real phase-depth effect, not an interpolation artifact.
These fixed low-label algebra controls are not IID source acquisition claims.

## A Subspace That Passes Cubic Admission And Fails At Level5

Index27 physical coordinates by x in F3^3. Set A(x)=x3 and retain the three
coordinate-function columns w1=x1,w2=x2,w3=x3. All weighted kernel and cubic
products vanish. A summed monomial of total degree at most4 cannot contain
positive even exponents on each of the three variables.

But sum_x x1^2*x2^2*x3^2=2 mod3. At L5 the native fifth derivative along
(w1,w1,w2,w2,w3) is3 mod9. This same subspace has quadratic phase at L3 and
degree5 at L5. The report and independent replay evaluate the54 restricted
component values, not a3^27 quantum instrument. No sampler for this fixed low
pattern is supplied. A growing-depth receiver needs the appropriate higher
Schur constraints, not just the level3 gate.

## Degree Versus Secret Visibility

For P:F3^h->R/Z of additive degree at most d, every relative phase has order
dividing3^ceil(d/2). Choose k=ceil(d/2); all2k+1 differences vanish. The cyclic
identity then gives3^k*S^k*Delta_u P=0 for every u, so3^k*(P(x+u)-P(x))=0.
For d0, P is constant and the relative phase order is1.

This is a known nonclassical-polynomial fact, not a new general theorem. See
[Tao and Ziegler, Definition1.2 and Lemma1.7](https://arxiv.org/pdf/1101.1469v2).
The local derivation specializes the bound and its consequences to native
supplied flat phases; the inverse Gowers theorem is not a supplied decoder.

If EVERY known component Q_l/3^r has degree at most d, the entire supplied
flat-phase state can see only s modulo3^min(r,ceil(d/2)), up to global phase.
Thus constant additive degree cannot retain all residual digits as r grows.
Exact quadratic calibrations modulo9,81,6561 alias secrets2 and5.

This does NOT forbid every degree reduction: retaining order3^r requires
degree at least2r-1, so lowering native degree2r+1 to2r or2r-1 can preserve
full residual order. It also does not forbid junk carrying high phase,
coherent syndromes, other measured records, approximate constructions or
other decoders. The visibility ledger is conditional; it does not certify
the proposed degree bound. Source losses and decoder costs remain separate.

A native EVEN L4 frequency table(0,1,4) mod9 is formally j^2, yet has additive
degree4, not2. Its third difference is(0,3,6), fourth(3,3,3), fifth zero.
Replacing a growing prime-power phase by an F3 stabilizer quadratic is wrong.

## Classical And Quantum Baseline Gates

[Alrabiah et al., Theorem1.1](https://arxiv.org/html/2608.00265v1) give
copy lower bounds for low-degree testing of generic unknown phase states.
Those input promises do not match these public-component, shared-secret,
prime-power packets. Their generic bound is neither a native decoder lower
bound nor contradicted by evaluating known component derivatives. The theorem
rules out importing an unspecified efficient generic phase tester as a free
primitive. No complete proof audit of that paper is claimed.

Compare known varying-matrix univariate polynomial-phase techniques, legal
measurement inference and quantum sieves before proposing a receiver. The
public components have only n shared unknown weights, so generic learning of
an arbitrary degree-L polynomial is an unnecessarily large search space.

## Next Mechanism

Seek a depth-sensitive transformation that retains informative order3^r phase
within the degree window2r-1 through2r+1, with efficient native construction,
all branches and acquisition charged. Alternatively derive an implicit
full-source modular decoder. Fixed-level cubic cancellation alone is no
longer the next research target. No general obstruction to such mechanisms
has been proved.

Implementation: `theorems/ternary_phase_depth.py`; producer:

```sh
python theorems/ternary_phase_depth.py
node research/certificates/ternary_phase_depth_crosscheck.js
```

29 focused tests pass. Independent JS replays60 integer operator columns,
12 growing native derivatives,54 restricted native component values and18
secret-alias amplitudes. The nine-file related regression has195 passing
tests. Python/JS checks are scoped evidence, not full production validation.
Routine CLI, registry wiring and full-suite validation remain Gemini's task.
