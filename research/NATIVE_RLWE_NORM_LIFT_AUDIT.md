# Native RLWE: Norm Descent Must Recover Orientation, Not Just A Norm

Date: 2026-10-04. LOCAL DERIVATION / REVIEW PENDING. Scoped source/output-
class bounds and necessary scalar-content gates. NOT a quantum algorithm,
general hardness theorem, security estimate or independent verification.

## 1. Actual Escape Audited

The subfield-cover audit does not exclude lifting a homogeneous relation
and then completing it into unrestricted affine outputs. Test that escape
without assuming a planted short key. The
[Albrecht--Bai--Ducas paper](https://eprint.iacr.org/2016/127.pdf) studies
norm descent for overstretched NTRU under a short-key promise. Its
[author's slides](https://www.maths.ox.ac.uk/system/files/attachments/subfield-attack.pdf)
explicitly require a sufficiently short subfield solution to be a multiple
of the normed secret pair. That promise is not supplied by the native
uniform ratio law. These results do not dispute that planted-key attack.

Use R=Z[X]/(X^d+1), d>=8 a power of two, and S=Z[Y]/(Y^h+1), h=d/2,
Y=X^2. Write tau(X)=-X. For the PUBLIC ratio m,

```
eta=N_(R/S)(m)=m*tau(m) (mod q).
```

Given a lower relation `a=eta*b (mod q)` in S, the elementary lift is

```
g=embed(a), f=embed(b)*tau(m), g=m*f (mod q).
```

It really is a label-adaptive direction. Its integrality, original height,
content, numerator/denominator balance and completion quality are not
free. Distinguish RAW integer lifting, MODULAR recentering and FRACTIONAL
common-content extraction; they do not obey the same bound.

## 2. Raw Lift: Integral Multipliers Cannot Repair The Norm

Fix the canonical coefficient lift of the independently uniform native
m. For ANY nonzero integral multiplier alpha in R, even chosen adaptively,

```
f=alpha*tau(m),
abs(Norm_R(f))=abs(Norm_R(alpha))*abs(Norm_R(m))
             >=abs(Norm_R(m)).
```

This includes arbitrary subfield b and arbitrary integral units/nonunits
applied to the raw pair. Hadamard gives `abs(Norm_R(f))<=||f||^d`.
Consequently any such f with norm <=R0 requires `abs(Norm_R(m))<=R0^d`.

There are h conjugate complex embedding pairs. The product norm condition
implies at least one embedding of m has magnitude <=R0. In every embedding,
the coefficients m_0 and m_h contribute independently along the real and
imaginary axes, since sigma(X^h)=+/-i. Conditional on all other coefficients,
each axis has q distinct consecutive integer values. A disk of radius R0
contains at most `(2R0+1)^2` of these grid points. Union over h embeddings:

```
B_raw <= min(1,h*(2R0+1)^2/q^2).
```

No catalogue factor is needed: the norm obstruction covers ALL adaptive
integral multipliers. It does NOT include recentering f by q multiples or
fractional multipliers. It is a short-seed output-class bound, not rejection
of every completed basis with an arbitrary column order.

Use the conservative first-vector radius `R0=ceil(t_star/E_noise)` from
the balanced-relation target; direct affine witnesses need an even smaller
radius. The exact bound is <=1e-8 in all six saved reference lanes.
Exceptional norm-one inputs and unit shape repair are retained controls,
not contradictions to a high-probability source statement.

## 3. Fractional Content: A Classical Gate Before PIP

For ANY actual integer native relation `(g,-f)`, put

```
k=(g-m*f)/q, I=(f,k), N_I=[R:I].
```

Compute N_I as the absolute determinant of a classical column HNF of
`[C_f,C_k]`. This does not assume that I is principal. Do not substitute
the ambient ideal `(f,g)` when q is not invertible modulo f.
This is polynomial-bit-complexity linear algebra on EXPLICIT integer
coordinates; expanding a compact enormous input is not free. Keep input
bit lengths, lift and integral-kernel membership in its cost ledger.

ANY field scalar theta yields an integral valid kernel relation exactly
when `theta*I` is contained in R. Its coefficient lattice then has integer
index at least one. Scaling covolume gives

```
abs(Norm(theta))*N_I=[R:theta I]>=1.
```

If a scaled pair is to have norm <=R0, a necessary gate is therefore

```
max(abs(Norm(f)),abs(Norm(g))) <= N_I*R0^d.
```

This covers ALL eligible fractional scalars, not just a searched unit
basis or principal-generator quotients. Quantum PIP cannot bypass a failed
gate, even at zero cost. Passing does not establish principal content,
short embeddings, a successful completion or an efficient generator.
The saved primitive classical d64 LLL relation passes; there is no
general native-kernel hardness conclusion.

For raw norm lifts with nonzero a,b, there is a sharper corollary. Since g is in I,
`N_I<=abs(Norm_R(g))=abs(Norm_S(a))^2`, while
`abs(Norm_R(f))=abs(Norm_R(m))*abs(Norm_S(b))^2`. If

```
abs(Norm_S(a)) <= C^h*abs(Norm_S(b)),
```

then any eligible fractionally scaled denominator of norm <=R0 forces
`abs(Norm_R(m))<=(C*R0)^d`. The raw source bound becomes

```
B_fractional <= min(1,h*(2*C*R0+1)^2/q^2).
```

This permits arbitrary label-adaptive a,b and fractional content extraction,
but keeps the UNRECENTERED denominator identity and the stated algebraic
norm-ratio promise. Comparable coefficient norms do NOT imply that promise;
an explicit lower-field unit countercontrol prevents that substitution.

Largest integer C giving the exact <=1e-8 bound at the reference rows:

| d | Spherical | Hidden elliptical |
| ---: | ---: | ---: |
| 64 | 14 | 15 |
| 256 | 210 | 209 |
| 1024 | 2765 | 2133 |

These are conditional source bounds, not security bits or attack thresholds.
Recentered denominators and larger algebraic norm ratios remain outside
this corollary. The exact content gate itself still applies to their actual
native coordinates, but its source success law needs new analysis.

## 4. Modular Lift: The Norm Summary Leaves Large Fibres

Now permit ANY integer lift of `f=embed(b)*tau(m) (mod q)`, with
2R0<q. Require b to come from a catalogue selected using only the MODULAR
relative norm eta, plus information independent of the remaining orientation
conditional on eta. Selection among that catalogue may use the full input.
The catalogue must not be constructed from the original training records
or exact integer norm carries without a new independence argument.

For q prime, q=3 mod 8 and d>=8,

```
R_q = F_(q^h) x F_(q^h),
S_q = F_(q^(h/2)) x F_(q^(h/2)).
```

Each R component is a quadratic extension of its S component. On units,
the relative norm is surjective with fibres of size
`L=(q^(h/2)+1)^2`. Uniform m conditioned on eta is uniform on that fibre.
For unit b in S_q, f is therefore uniform on its shifted norm fibre.

Write f=f0+X*f1, with f0,f1 in S. Its norm equation is

```
f0^2-Y*f1^2=b^2*eta (mod q).
```

For each fixed f1, there are at most FOUR possibilities for f0 modulo q:
at most two square roots in each of the two S fields. Short f requires
short f1. Since 2R0<q, each residue has at most one representative in the
coefficient cube [-R0,R0]^h. Thus

```
B_unit_b <= min(1,4*(2R0+1)^h/(q^(h/2)+1)^2).
```

### Nonunit Lower Multipliers Are Included

If b has exactly one nonzero S component, its f-image orbit has size
`q^(h/2)+1`, not L. Both f0 and f1 belong to one S prime ideal. Every
nonzero polynomial there has norm >=sqrt(q), by norm divisibility and
Hadamard in degree h. Ideal packing bounds the possible short f1 by
`(1+2R0/sqrt(q))^h`; the square-root cap remains four. With s=floor(sqrt(q)),

```
B_nonunit_b <= min(1,4*(s+2R0)^h/[s^h*(q^(h/2)+1)]).
```

If b=0 modulo q, both lifted relation blocks are zero modulo q. No nonzero
pair of norm <q exists in that case. The zero pair must not be marked as
algorithmic success.

For an arbitrary mixed catalogue of K nonzero multipliers, charge
`K*max(B_unit_b,B_nonunit_b)`. The native ratio's nonunit event is separately
charged by `epsilon=(2*q^h-1)/q^(2h)`. No source mass is silently dropped.
At all six references, even K=2^d plus epsilon remains <=1e-8 exactly.

This is NOT a bound for an unrestricted full-label multiplier generator,
an arbitrary post-recentering unit optimizer or access to exact integer
norm carries. A sufficiently large catalogue may contain useful points;
its size alone does not establish a quantum runtime lower bound.

## 5. Wide Coherent Support Does Not Rescue Ordinary Amplification

Allow a coherent preparation over ALL b in S_q, using unique modular
representatives, with arbitrary distribution whose
weights depend only on eta. Evaluate the norm lift coherently. On unit m,
the map b->embed(b)*tau(m) is injective. Neither phases nor reversible
uncomputation of b changes the mass of a DIAGONAL success projector.
Duplicate integer lifts need a separate reversible carry/junk ledger;
their labels cannot be erased for free to assert constructive interference.
The valid-success projector excludes the zero relation. Average marked
mass over the native source is at most

```
p_bar=max(B_unit_b,B_nonunit_b)+epsilon.
```

Markov implies that on at least 99% of source inputs,
`p_m<=100*p_bar`. The artifact finds the largest integer B satisfying
`100*p_bar<=2^(-2B)`. Ordinary Grover reflections have success bounded by
`(2r+1)^2*p_m`; for B>=3 and r<=2^(B-2), this is less than one half.
Thus those ordinary amplification iterations must EXCEED:

| d | Spherical: 2^exponent | Hidden elliptical |
| ---: | ---: | ---: |
| 64 | 307 | 310 |
| 256 | 1562 | 1561 |
| 1024 | 7474 | 7378 |

These are LOCAL derived operation-class bounds on >=99% of the stated
source, not hardware runtime/security estimates or an all-quantum query
lower bound. The amplification framework is established prior art:
[Brassard--Hoyer--Mosca--Tapp](https://arxiv.org/abs/quant-ph/0005055).
Structured orientation-dependent interference BEFORE the projector may
escape; it must be specified and costed, not called ordinary amplification.

## 6. Attempted Refutations And Revised Priority

- Raw integral units: counted by the norm invariant; rare unit inputs can
  still be repaired. Fractional content uses a different, explicit gate.
- Modular recentering: permitted by the fibre bound, excluded by the raw
  invariant. Do not conflate those two arguments.
- Nonunit b or nonunit m: included by ideal packing or an explicit event
  charge, respectively. No modular-invertibility assumption is hidden.
- Tiny/split fields: not a universal root cap. The retained q=17, degree-4
  base ring has SIXTEEN square roots of one, refuting the constant four
  outside the native high-CRT family. The d=4 split-extension control has
  a different fibre size and is not used for the large-degree theorem.
- Content norm is sufficient: false. A wrong ambient ideal falsely admits
  division of `(q,0)`; native content rejects it. Even both component norms
  equal to one do not give a pair of total norm one.
- A classical escape: the actual d64 LLL relation is primitive and short,
  and passes the necessary content gate. These results cannot establish
  general kernel hardness or a quantum advantage.
- Known NTRU attacks: the planted-key lift premise is not the native law.
  Full-public-label geometric methods, including the
  [Kirchner--Fouque analysis](https://www.iacr.org/archive/eurocrypt2017/10210293/10210293.pdf),
  must still be matched classical competitors; the bounds are not a rejection
  of all subfield/subring attacks.

Next theoretical work should require an actual orientation-sensitive
operation, or a source-conditioned large native-content construction that
passes the classical norm gate AND the final reciprocal-energy/profile
gate. Norm/DLP/PIP labels without those operations are not a generator.
Stop adding wrappers that optimize only the modular norm summary.

## 7. Reproducible Evidence And Gemini Handoff

```
python research/certificates/native_rlwe_norm_lift_probe.py --save
```

The probe checks 21,283 exact modular norms, three uniform norm maps,
448 multiplier-image distributions, 864 unit-fibre bounds, 64 nonunit
packing controls, 108 raw norm/Hadamard controls and six reference lanes.
It also checks 48 native/ambient ideal identities in the unit-mod-q case,
48 eligible fractional scalar controls, 48 norm-ratio corollaries, the
saved native d64 classical escape and the stated false-positive controls.
Small cases are identity checks, not toy benchmark families. Prime chains
are referenced but not replayed, and original prior/noise laws not sampled.

Gemini: add the native ideal-NORM rejection gate before any PIP/short-
generator call, preserving f,k, actual lift, HNF index, both algebraic
norms and radius. Preserve rejection versus insufficient evidence. Separate
raw, recentered, content-divided and orientation-adapted norm lifts in
records; never combine their scope flags. Charge the public nonunit event.
Add ordinary-amplification costs only for the specified preparation/projector
class. Run actual-source classical norm-descent/compressed-cover competitors
and routine registry/CLI/full-suite integration there. No production wiring,
full-suite run, commit or independent proof/novelty promotion in this pass.
