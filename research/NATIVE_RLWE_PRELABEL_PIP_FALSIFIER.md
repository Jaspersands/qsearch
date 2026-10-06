# Native RLWE: Prelabel PIP And Unit Wrappers Miss Short Relations

Date: 2026-10-04. LOCAL DERIVATION / REVIEW PENDING. An OUTPUT-CLASS
existence bound under the native public-label distribution, not a quantum
runtime lower bound, average-case hardness theorem, independent verification
or new algorithm. This closes one conditional common-content branch left
open by `NATIVE_RLWE_UNIT_ORBIT_GENERATOR_AUDIT.md`.

## 1. Precise Attempt Being Tested

Take `R=Z[X]/(X^d+1)`, d a power of two, d>=2. The normalized public
matrix is `[I,M]`, with M an integer negacyclic/adjoint lift of an
independently uniform native ratio modulo q. Its d coefficient residues
have q equiprobable values. Begin with the fixed-native-pair version;
Section 4 strengthens it to an adaptive numerator at the reference primes.

Before seeing that ratio, choose integer native coordinates `(k,f)`.
They can be random, expensive, field-dependent or conditioned on any
information INDEPENDENT of this ratio. Form the actual kernel relation

```
v(M)=(qk+Mf,-f).
```

After seeing M, grant arbitrary unit multiplication, with no cost bound.
Can `u v(M)` become short enough to seed the original box/norm decoder's
GLOBAL Babai certificate? Such a certificate requires its first basis
column to satisfy `E^2 ||u v||^2 < t^2`, where
`t=floor(q/(2R_s+1))`.

The same question covers PIP applied to a preselected principal content
ideal `(f,k)=alpha R`. Choose any fixed generator alpha0 for the proof,
not an assumed efficient operation. The quotient `(f0,k0)=(f,k)/alpha0`
is an integer pair independent of M. Every alternative PIP generator
is alpha0 times a unit, even if chosen adaptively using M. Thus all
primitive generator quotients are unit multiples of the SAME base pair.

This fixed-pair version does NOT cover arbitrary nongenerator divisors,
nonunit multipliers, label-adaptive native coordinates or coherent outputs
outside this short-relation class. Residue-preserving lift choices ARE
allowed while k stays fixed; changing k to preserve an existing physical
vector under a lift change is a different operation. Mixing prior pairs
into a NEW label-adaptive pair changes this version's output class. The
high-CRT version below permits arbitrary adaptive k but still preselects f.

## 2. Integer Injection, Not Modular Invertibility

Fix any nonzero f and k. The cyclotomic characteristic-zero field ensures
that multiplication C_f is invertible over Q. Consequently

```
m -> C_f m+qk
```

is INJECTIVE on the q^d integer coefficient lifts. It need not be
invertible modulo q. For every radius R0>=1, therefore

```
Pr_M[||qk+Mf||<=R0] <= N_d(R0)/q^d,
N_d(R0)=#{z in Z^d:||z||<=R0} <= (2R0+1)^d.
```

This avoids losing a factor q^(d/2) at nonunit modular f. For example,
f=q gives a CONSTANT modular map but an injective INTEGER map. A modulo-q
point-mass argument would not prove this bound; exact fixed k is essential.
Even allowing ANY residue-preserving lift works: each integer g determines
at most one lift m=C_f^-1(g-qk), hence at most one public label. The number
of labels admitting any short g is still at most N_d(R0). This also allows
lift choices depending on the selected unit. Allowing arbitrary modular
recentering by changing k is outside this general version, but is covered
by the stronger high-CRT version below.

The adjoint coefficient involution is an integer signed permutation, so
it does not change the number or uniform law of the coefficient choices.

## 3. Elementary Unit Packing In Power-Two Cyclotomics

Let U(f,R0) contain units u with `||uf||<=R0`, f nonzero. No regulator,
class number, GRH, log-CVP or unit-group algorithm is used in the bound.
There are h=d/2 conjugate embedding pairs. Put

```
L=bit_length(d*R0),  z_i=log2 |sigma_i(uf)|.
```

Cauchy--Schwarz gives `|sigma_i(uf)|<=sqrt(d)R0<2^L`.
The nonzero integer norm has absolute value at least one, so
`sum_i z_i=(1/2)log2 |Norm(f)|>=0`. Hence every coordinate lies in

```
-(h-1)L <= z_i < L.
```

The lower endpoint is strict for h>1 but may be zero at d=2.
Partition this box into half-bit bins `floor(2z_i)`. There are at most
`(dL+1)^h` bin tuples, conservatively including endpoint slack.

If two units land in the SAME tuple, their ratio w is a unit with EVERY
conjugate of absolute value strictly less than sqrt(2). Negacyclic
Parseval in the integral coefficient basis gives

```
(1/d) sum_embeddings |sigma(w)|^2 = ||w||_coeff^2 < 2.
```

This is a positive integer. It must be one, so w is a signed monomial,
one of the 2d roots of unity. Thus each tuple contains at most 2d units:

```
|U(f,R0)| <= 2d(dL+1)^(d/2).
```

This uses the orthogonal integer basis of the power-two cyclotomic.
Do NOT transfer the constant log-separation to arbitrary number fields
or nonorthogonal orders. The bound counts an infinite unit group with
a finite norm promise, not merely a searched catalogue of powers.

## 4. Uniform Natural-Label Output-Class Bound

Every successful `u v(M)` has BOTH blocks of norm <=R0. The f-block
therefore restricts u to U(f,R0), a set independent of M. For each fixed
u in that set, integer injection applied to `(uk,uf)` bounds the g-block.
Union over all those units:

```
Pr_M[exists unit u: ||u v(M)||<=R0]
 <= B(d,q,R0)
 := min(1,2d(dL+1)^(d/2) (2R0+1)^d/q^d).
```

The unit choice may depend arbitrarily on M. No algorithm, classical or
quantum, can output a member of this class on labels where it is empty.
This is not an obstruction to a different output class or quantum
measurement. If f=0, a nonzero valid relation in this class has norm >=q;
our decoder radii below are <q, so that branch is excluded separately.
The zero pair is not a valid first basis vector.

For K preselected coordinate pairs, charge K times this bound. Random
catalogues independent of M follow by conditioning and averaging. A
coherent selector does not change the existence bound IF its eventual
output is one of these unit-multiple relations. New inter-line arithmetic
outputs are not covered.

Choose the conservative integer `R0=ceil(t/E)`. This overcounts every
possible first column of a passing global profile, including its strict
boundary. This general version does NOT exclude actual short residuals
from a particular coset using a bad global basis, affine witnesses,
moment-based Gaussian decoding or primal attacks. The affine extension
below excludes a specific prelabel-denominator subclass, not all witnesses.

### Stronger High-CRT Version: Arbitrary Adaptive Numerators

At d>=4 and prime q=3 modulo 8, the quotient ring has two irreducible
CRT components of equal degree h=d/2. Fix only a NONZERO denominator
f before seeing M; permit arbitrary label-adaptive k, unit u and numerator.
Let J=fR+qR. If f is a unit modulo q, its modular image is uniform on
all q^d residues, so the preceding integer-ball bound applies even with
arbitrary correction k. If f is zero modulo q, `||uf||>=q`, impossible
at R0<q. The remaining case has exactly one nonzero CRT component.

Then J is one prime ideal of norm q^h, and Mf is uniform on J/qR, which
has q^h elements. Every nonzero z in J has `q^h | Norm(z)`; Hadamard
and Parseval give `|Norm(z)|<=||z||^d`, hence `||z||>=sqrt(q)`.
This is the same reviewed high-degree ideal-spacing premise used in
`NATIVE_RLWE_NONUNIT_WITNESS_AUDIT.md`, not a low-degree CRT inference.
Packing disjoint balls gives

```
#{g in J:||g||<=R0} <= (1+2R0/sqrt(q))^d.
```

Consequently, for a fixed unit u, existence of ANY short numerator g
with `g=Muf (mod q)` has probability at most this count divided by q^h.
The ideal J is unchanged by u. Counting all possible short uf as before,
and using the conservative integer s=floor(sqrt(q)), yields the unified
bound for unit and nonunit modular f:

```
B_CRT = min(1, 2d(dL+1)^(d/2) (s+2R0)^d/[s^d q^(d/2)]).
```

Unlike the arbitrary-q fixed-pair proof, this includes arbitrary adaptive
k; both versions allow residue-preserving lift choices within their
respective native-coordinate premises. Preselecting f up to units, then
solving its numerator however expensively, is not enough on typical labels.
One must escape the prelabel denominator class. A label-adaptive f can,
and classical LLL explicitly does. Arbitrary primes with low CRT degree
do NOT inherit this bound: a retained d=8,q=17 example has a nonunit of
norm 2<sqrt(17).

### The Affine Witness Endpoint Is Covered Too, With Scope

For a syndrome w fixed independently of M, the condition
`g+Muf=w (mod q)` shifts the uniform image to an affine coset. Differences
of its integer representatives lie in J, so the SAME packing bound holds.
An individual shifted representative may be shorter than sqrt(q); it is
the separation between representatives that matters. The unit case again
has all q^d residues. The bound therefore extends to actual chosen affine
preimages with NONZERO prelabel denominator, not only homogeneous bases.

A catalogue of T syndromes independent of M costs factor T. Conditional
on original a1, the normalized original targets
`w_t=C_a1^-T (t e0)` are such a catalogue, since the native ratio remains
uniform and independent of a1. Charge all q scalar labels if t is adaptive.
A prelabel denominator may depend on a1 only when that conditional
independence is retained. Do NOT apply this to arbitrary M-dependent
polynomial syndromes or to denominators derived from the original data.

For the direct box/norm decoder, any passing affine witness has
`||c||<t_star/(2E)`, where `t_star=floor(q/(2R_s+1))` is the optimal
scalar spacing. Our larger R0=ceil(t_star/E) overcounts all such witnesses.
Zero-denominator affine witnesses are NOT excluded by the ratio-M bound;
they need the separate first-label source analysis below. No all-decoder
or all-quantum claim follows.

### Close The Zero-Denominator Branch Using The Existing Source Lemma

This is the k=0 case of `NATIVE_RLWE_SPARSE_WITNESS_AUDIT.md`, not a new
mechanism. On the original source, a1 is uniform conditioned on being a
unit. Its inverse-adjoint vector v=C_a1^-T e0 is uniform on the ring's
`(q^(d/2)-1)^2` units. If the second witness block is zero, every nonzero
scalar target requires `g=t*v (mod q)`. Charge all q-1 targets and all
integer points in the radius-R0 ball, including adaptive selection:

```
B_zero = min(1, (q-1)(2R0+1)^d/(q^(d/2)-1)^2).
```

Thus under BOTH the original first-label law and the independent uniform
ratio law, the combined affine output class has probability at most
`q*K*B_CRT+B_zero`. K counts prelabel nonzero denominator unit classes,
potentially conditioned on a1 but not the ratio or original records b.
The probe checks this SUM, not merely each summand, against 10^-8 for
K=2^d at all six reference lanes. Retain an easy a1=1 countercontrol:
this is a source-probability bound, not impossibility on every input.

## 5. Exact Reference Bounds And Scaling

`certificates/native_rlwe_prelabel_unit_bounds.json` stores factored
integer bounds, not enormous decimal numerator/denominator strings or
floating probability estimates. Strict upper binary exponents are obtained
from numerator/denominator bit lengths; the requested 10^-8 comparisons
are performed on the full integers.

| d | Lane | One prior pair: B < 2^exponent | Catalogue of 2^d pairs |
| --- | --- | ---: | ---: |
| 64 | Spherical | -868 | -804 |
| 64 | Hidden elliptical | -879 | -815 |
| 256 | Spherical | -4434 | -4178 |
| 256 | Hidden elliptical | -4431 | -4175 |
| 1024 | Spherical | -21389 | -20365 |
| 1024 | Hidden elliptical | -20999 | -19975 |

Both B and B_CRT have the displayed strict binary exponents at these
rows. All six exact comparisons pass for K=1, K=d^10 and K=2^d.
The affine version ALSO passes 10^-8 when charging q scalar targets AND
2^d prelabel denominators, even after adding the zero-denominator bound
under the separate first-label law. Prime/high-CRT premises come from the existing
saved recursive prime certificates; this probe does not replay those
prime chains or claim independent proof verification.
These are derived event bounds, not observed success rates. The original
prior/noise laws are not sampled by this probe; their norm/box contracts
are separate reduction premises.

For the reference q of order d^12 and spherical `R_s E` of order
`d^2 log^(5/2)(d)`, L=O(log d). The logarithm of the cube-based bound is

```
log B <= -(3/2)d log d - 2d log log d + O(d).
```

Both bounds have this scaling: R0 is of order q/(R_s E), which dominates
sqrt(q), so the high-CRT packing expression has the same leading terms.
Do not extrapolate this formula to every polynomial modulus or CRT type.
Thus even an exp(O(d)) prelabel catalogue fails with high probability
asymptotically under those stated scalings. This is still a source/output-
class statement, not a lower bound for label-adaptive relation generation.

## 6. Attempted Refutations And Surviving Direction

- **Modular nonunits:** not a loophole. The exact lift map is injective
  over Z even when its reduction modulo q collapses. Four finite controls
  deliberately collapse that modular map.
- **Huge compact units:** not a loophole for this endpoint. Every unit
  producing an explicit short f-block is included in the counting argument.
  Units that cannot be expanded/verified still do not supply the certificate.
- **Adaptive PIP generator:** changing the generator of a preselected
  principal ideal changes the quotient by a unit. A new label-adapted
  denominator outside the prior unit classes is not covered. Merely
  changing the numerator/coordinate ideal does not escape the high-CRT bound.
- **Infinite units:** counted using the norm promise and exact Parseval,
  without assuming bounded powers of a chosen unit basis.
- **Polynomial sample/candidate count:** charge its true catalogue size.
  The exact reference bounds survive much larger catalogues than polynomial.
- **Classical counterexample:** the saved native d64 LLL row DOES satisfy
  the first-vector length promise, with nonzero f,k generated FROM M.
  The successful full classical profiles remain valid. The proof therefore
  cannot be promoted to native-kernel or quantum hardness.
- **Different output:** arbitrary nonunit multipliers, content extraction
  that creates a new denominator class, or non-norm decoders remain outside.
  Affine witnesses with a nonzero prelabel denominator and the stated target
  catalogue ARE covered; zero denominators use the separate first-label
  law and B_zero, not the ratio bound. A
  principal-ideal short-vector operation is not identical to finding a
  principal generator; do not silently identify the two.

The decisive generator obligation is a source-adaptive DENOMINATOR outside
the prelabel unit classes, not prior random coefficients followed by known
number-field postprocessing. PIP/unit methods on an ALREADY useful
label-adaptive pair may still help, but cannot be credited with generating
that pair. This is stronger than requiring a new numerator or merely
changing its lift.

## 7. Checks And Handoff

Run `python research/certificates/native_rlwe_prelabel_unit_probe.py --save`.
The exact controls check 12 integer injections, 36 finite small-ball counts,
12 adaptive-lift image controls, 36 adaptive-lift small-ball counts,
four modular-collapse examples, 196 root-unit ratios, 1344 nonroot Parseval
separations, 12 finite unit-catalogue count controls, six reference bounds
and one actual label-adaptive LLL escape. A d=2 root-unit control retains
the non-strict log-box endpoint. High-CRT controls add two exact
uniform-image distributions, 72 ideal minimum-norm checks, six adaptive
numerator packing checks and six affine-coset spacing checks. Retain the
low-residue-degree counterexample. Two exact unit-population and six
adaptive scalar-target controls check the separate zero-denominator bound;
retain the easy first-label countercontrol. The small controls are identity
checks, not new problem families or algorithmic benchmarks.

Gemini: integrate this as a scoped rejected OUTPUT class, not a candidate
hardness proof. Distinguish fixed-pair arbitrary-q from prelabel-denominator
high-CRT claims. Record independence from M, CRT degrees/prime provenance,
target catalogue, separate zero-denominator source law, principal-generator versus ideal-
SVP access, radius and source-law premises. Preserve the adaptive LLL
escape; label-adaptive f is outside BOTH bounds, but adaptive k is allowed
by the high-CRT bound. No routine CLI
wiring, full production-suite run, speedup or novelty promotion here.
