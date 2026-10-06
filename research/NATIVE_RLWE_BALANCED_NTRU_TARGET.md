# Native RLWE: Balanced Relation And Controlled-Index Completion

Status: LOCAL DERIVATION / REVIEW PENDING. A sufficient target and exact
classical postprocessing, NOT an efficient relation generator, new NTRU
algorithm, quantum speedup, or asymptotic source attack.

FOLLOW-UP: [the quaternion graph-kernel audit](NATIVE_RLWE_QUATERNION_KERNEL_AUDIT.md)
constructs a label-adaptive definite quaternion left ideal for this actual
kernel. Its metric distortion is source-typically unavoidable for every real
positive congruence lift in the original coordinates. No quaternion generator
or balanced relation is supplied; the completion targets below still apply.

## 1. Strip Away The Unnecessary Sampler

For the full public kernel K of `[I,M]`, one embedding-balanced relation
with a controlled completion multiplier can supply a classical full-rank
sublattice and finite decoder. Primitive relations give a full-kernel
basis, but that is NOT necessary for the endpoint. This is weaker than
producing a prescribed Gaussian,
neutral-coordinate samples, a coherent inverse or a whole short basis.
It is STRONGER than producing an arbitrary short vector. The rank-two
module, completion cost/index and reciprocal embedding energy cannot be
replaced by a rank-one principal-ideal oracle.

Use an equivalent negacyclic multiplication representation of M and
write a relation as `v1=(g,-f)` with `g=Mf (mod q)` in
`R=Z[X]/(X^d+1)`. Adjoint/involution conventions must match the public
matrix when decoding original records. The target distribution is the
actual conditional UNIFORM public ratio, not a ratio planted from short
f,g. The [d64 classical certificate](NATIVE_RLWE_CLASSICAL_COVER_CERTIFICATE.md)
already defeats a quantum requirement for one finite kernel.

NTRU completion and reduction are established prior art; see Algorithms
6-7 and the key-generation checks in the
[official Falcon specification](https://falcon-sign.info/falcon.pdf).
The following exact sufficient certificate is a local specialization,
not a claim to invent those algorithms.

## 2. A Costed Sufficient Completion Condition

Let f,g be nonzero integer polynomials, with

```
N_f = det(C_f),  N_g = det(C_g),  gcd(N_f,N_g)=1.
```

This norm-gcd condition is SUFFICIENT, not necessary for every possible
completion or useful kernel basis. Choose integers u,v with
`u N_f+v N_g=1` and define integer adjugate polynomials

```
a_f=N_f C_f^-1 e0,  a_g=N_g C_g^-1 e0,
G=q u a_f,  F=-q v a_g.
```

Then `fG-gF=q`. Determinants, rational inverses, extended gcd and integer
coefficient operations are explicit classical algorithms. Hadamard
bounds make their bit sizes polynomial in d and the input coefficient
bit lengths. Do not invoke a free ideal-CVP or NTRU-solve oracle.

G,F are q-multiples, so `(G,-F)` is in K even without a modular-unit
argument. With norm-gcd one the column matrix

```
B_rot = [C_g, C_G; -C_f, -C_F]
```

lies in K and has determinant of absolute value q^d. Membership plus
determinant proves it is the full kernel basis. Two arbitrary independent
R-relations may instead supply a finite-index sublattice; that can still
solve the point-finding endpoint if its profile passes the certificate.

### Do Not Mistake Norm-Gcd For Ideal Primitivity

The exact controlled-index alternative is classical integer linear
algebra. Form `J=[C_f,-C_g]`. Its column lattice is the coefficient
lattice of the ideal `(f,g)`. Obtain a column Hermite basis H together
with an integer transformation T, `H=J T`, preserving the column lattice.
This requires a genuine unimodular transformed HNF, not an arbitrary
subset of independent input columns. Set

```
delta = lcm(denominators of H^-1 e0).
```

This is the MINIMAL positive integer for which `delta e0` belongs to
that ideal lattice. Exact integer coefficients from `delta T H^-1 e0`
give polynomials G0,F0 with `fG0-gF0=delta`. Set G=qG0,F=qF0. They lie
in the kernel, and the rotation basis determinant is `(q delta)^d`,
with index `delta^d` in K. Delta divides `gcd(N_f,N_g)` and can be much
smaller. No CVP or unit-group oracle is hidden in this completion.

For `f=2+X,g=2-X` at d=2 the norm-gcd is 5, but
`f(g-1)-g=1`: the ideal is primitive and delta=1. For f=g=2,
delta=2 although the norm-gcd is 2^d. The second example cannot produce
a determinant-q completion for odd q, but can produce a full-rank
sublattice. Whether its profile suffices is a separate numerical question.

Thus mandatory scalar norm-gcd-one rejection would discard legitimate
relations. Use a controlled delta and a FINAL profile gate; full-kernel
sampling requirements must not leak into finite point-finding.

### Preferred Completion: Use Native Kernel Coordinates

Further audit in `NATIVE_RLWE_UNIT_ORBIT_GENERATOR_AUDIT.md` removes
another unnecessary restriction. Set `k=(g-Mf)/q`. Every second kernel
vector has `G=MF+qz`, so

```
fG-gF=q(fz-kF).
```

The optimal positive CONSTANT completion multiplier for this fixed
relation is therefore the integer order delta_K of e0 in the ideal
`(f,k)`, computed by exact transformed HNF of `[C_f,-C_k]`. This gives
G=MF+qz directly; demanding G,F be q-multiples can overcharge the index.
The ideal is unchanged by changing M's lift by qH. Its delta_K divides
the ambient ideal order because `(f,g)=(f,qk)` is contained in `(f,k)`.

The native vector `(q,0)` has ambient order q but kernel-coordinate
order one, and can extend to a full native basis. Its geometry still
fails. Hence proper ambient content is NOT the kernel-primitivity test.
Use delta_K in the energy/profile formulas below for this preferred
completion; older adjugate/ambient completions remain valid sufficient
methods. This does not minimize over different relations or arbitrary
nonconstant determinant completions.

## 3. Exact Reduction And Reciprocal Energy

Put `Z1=(C_g;-C_f)`, `Z2=(C_G;-C_F)` and

```
A=Z1^T Z1=C_g^T C_g+C_f^T C_f,
P=Z1^T Z2,  alpha=A^-1 P e0.
```

Negacyclic multiplication and its adjoint commute. Round the rational
coefficients of alpha to integers gamma, set delta=alpha-gamma, and
replace `(G,F)` by `(G-gamma*g,F-gamma*f)`. This preserves `fG-gF=q delta`.
There is no need for a floating FFT rounding certificate.

For a completion `fG-gF=q delta`, the exact orthogonal complement satisfies

```
Z_perp=Z2-Z1 A^-1 P,
Z1^T Z_perp=0,  Z_perp^T Z_perp=(q delta)^2 A^-1.
```

Every diagonal entry of a negacyclic convolution matrix is trace/d.
Writing v2' for the reduced completion's first column gives

```
T_perp=((q delta)^2/d) trace(A^-1),
||v2'||^2=T_perp+delta^T A delta,
||delta||^2<=d/4.
```

Since `lambda_max(A)<=trace(A)=d||v1||^2`,

```
Gamma(B_rot) <= d(||v1||^2+||v2'||^2)
             <= Phi_delta(v1)
Phi_delta(v1)=d(1+d^2/4)||v1||^2+(q delta)^2 trace(A^-1).
```

For the original box/norm decoder, a sufficient end-to-end condition is
`E^2 Phi_delta(v1)<t^2`, with `t=floor(q/(2R_s+1))`. Better: compute the
actual completed basis's exact GS profile Q and test `E^2 Q<t^2`.
The proxy Phi can fail while the actual profile passes.

This replaces a vague short-vector goal by two quantitative objectives:
small norm AND small reciprocal embedding energy. A short vector with a
very small embedding can give an enormous perpendicular completion.

## 4. A Sharper Pointwise Certificate

If rational bounds certify `0<a_lo I <= A <= a_hi I`, then

```
Gamma(B_rot) <= d[(q delta)^2/a_lo+(1+d/4)a_hi].
```

For delta=1 and `a_lo=q/L^2`, `a_hi=q L^2`, the gate becomes

```
E^2 d q L^2 (2+d/4) < t^2.
```

An exact rational LDL/positive-definiteness certificate with strict
endpoint slack can verify the bounds. Floating embedding estimates are
references, not certificates. Zero pivots need an appropriate semidefinite
procedure; a strict-positive verifier must not silently accept them.

At the saved d^12 rows, integer floors of the allowable L reference are:

| d | Spherical | Hidden elliptical |
| --- | ---: | ---: |
| 64 | 1267 | 1127 |
| 256 | 45391 | 45739 |
| 1024 | 1792170 | 2323006 |

Always recheck the strict squared inequality for a proposed L. These
large margins signal a potentially EASY parameter regime, not quantum
leverage. For the spherical reference scaling, the sufficient allowable
L grows roughly as d^3/log^(5/2)(d). No generator attaining this bound on
growing-degree native modules has been established here.

## 5. Try To Kill The Proposal

1. **Primitive failure.** With ratio one, `f=g=2` is short and balanced,
   but every fG-gF is even and cannot equal odd q. Claiming a full-kernel
   completion from norm or spectral balance alone is unsound. A delta=2
   sublattice may still be legal: check its profile, not its primitivity.
2. **Unit imbalance.** At d=4, eta=1+X+X^2 has norm one. The primitive
   relation `f=g=eta^8` has an exact energy imbalance
   `trace(A) trace(A^-1)>10^8 d^2`. Common units preserve primitivity while
   destroying a naive norm/balance assumption. This is an easy-ratio
   algebra control, not a source-family obstruction.
3. **Rank failure.** One rotation orbit has rank at most d. A scalar
   multiple second orbit leaves determinant zero. A global cover
   certificate requires 2d independent integer columns.
4. **Distribution substitution.** Generating short f,g and publishing
   g/f changes the public law. Falcon key generation cannot be treated
   as a solver for independently uniform native ratios.
5. **Hidden oracle cost.** The [2019 module-LLL paper](https://eprint.iacr.org/2019/1035.pdf)
   includes field-dependent oracle work; the
   [fully classical follow-up](https://eprint.iacr.org/2022/1356.pdf)
   removes the quantum wrapper. Neither supplies this balanced primitive
   relation for free. Growing field degree rules out hiding the oracle
   in constant preprocessing. No quantum separation follows from the
   word "module" or "NTRU".
6. **Classical falsifier.** An actual d64 native kernel already passes
   an ordinary classical profile gate. Search harder identical-input
   classical competitors before proposing quantum mechanisms here.
7. **Endpoint mismatch.** A finite chosen preimage needs neither IID
   Gaussianity nor lattice saturation. Reimposing those constraints on
   classical competitors manufactures a gap unrelated to recovery.

## 6. Exact Controls And Next Work

`certificates/native_rlwe_ntru_completion_probe.py`, seed 290953, checks
18 uniform-ratio small kernels at d=2,4,8. Classical LLL supplies reference
relations; these are identity controls, NOT source-family attacks.

All 18 completed full bases pass exact membership/determinant and
Schur-complement checks and 18 independent direct-GS/Bareiss comparisons.
There are 144 affine-preimage/cover checks,
including nonsaturated 2B bases, and 54 conditional decoder controls.
Retained failures: norm-gcd/zero rejection, balanced nonprimitive pairs,
dependent orbits and the primitive unit-imbalance example.
Four HNF controls retain norm-gcd false negatives and the minimal
nonprimitive completion multiplier.

### Actual d64 Single-Relation Falsifiers

`certificates/native_rlwe_balanced_relation_d64_probe.py` loads the saved
classical LLL rows on the SAME native kernel. It verifies exact kernel
membership, determinant, Schur identity, completion rounding energy and
GS-profile inequalities. Both decoder lanes pass the exact profile,
orbit-bound and reciprocal-proxy gates in all four runs:

| LLL row | Completion | Norm-gcd | Multiplier | Full kernel? | Exact GS upper Q |
| --- | --- | ---: | ---: | --- | ---: |
| 0 | Adjugate/norms | 1 | 1 | Yes | 34504054203683090387993166 |
| 4 | Adjugate/norms | 769 | 769 | No | 1343177067893862797530259681 |
| 4 | Ideal HNF | 769 | 1 | Yes | 44561121420840822609064258 |
| 4 | Native-coordinate HNF | 769 | 1 | Yes | 44561121420840822609064258 |

The norm-completed row-4 basis has index 769^64, yet still passes the
decoder certificate. The HNF branch demonstrates an ACTUAL native-row
false negative for a norm-gcd-one gate, not just a planted example.
These completions use prior CLASSICAL LLL preprocessing; it is not free
input and its cost must be charged. None proves a growing-degree solver.
The source prior/noise laws are not sampled by these completion probes.

```sh
python research/certificates/native_rlwe_balanced_relation_d64_probe.py --save
python research/certificates/native_rlwe_balanced_relation_d64_probe.py --relation-index 4 --save
python research/certificates/native_rlwe_balanced_relation_d64_probe.py --relation-index 4 --completion-method ideal-hnf --save
python research/certificates/native_rlwe_balanced_relation_d64_probe.py --relation-index 4 --completion-method kernel-hnf --save
```

Transformed HNF follows the exact API in the
[official python-flint documentation](https://python-flint.readthedocs.io/en/latest/fmpz_mat.html).
Saved artifacts expose completion method, multiplier and sublattice index.

Main-model priority: construct or exclude an ACTUAL costed generator for
the controlled-index reciprocal-energy target. A useful proposal must state its
native input law, output guarantees/probability, retries, preprocessing,
bit complexity and strongest classical competitor. No unimplemented
short-vector/CVP/ideal oracle may appear in its costed core.

Read the unit-orbit audit before proposing a scalar/unit optimizer for
the fixed native generators. Exact finite obstructions reject that output
class's GLOBAL profile certificate even with free scalar access. A new
direction, rather than only embedding-shape repair, is required there.

The follow-up `NATIVE_RLWE_PRELABEL_PIP_FALSIFIER.md` gives a natural-label
output-class bound for prelabel denominators up to units, even with fully
adaptive numerator solving at the high-CRT reference primes. It also
tracks the scoped affine endpoint and separate zero-denominator source
law. Principal-content extraction on preselected pairs does not supply
the missing generator. Actual label-adaptive denominators, including the
saved classical LLL relations, are outside the bound. REVIEW PENDING,
not a general hardness or quantum-runtime theorem.

`NATIVE_RLWE_SUBFIELD_COVER_AUDIT.md` supplies the next matched CLASSICAL
competitor: an explicit one-level rank-3d/2 affine cover in the original
metric. Deeper restrictions have both geometric and source-density
falsifiers for their FINAL affine output class. This does not rule out
lifting/completing a subfield homogeneous relation into unrestricted
outputs. Test that escape rather than conflating the two endpoints.

The subsequent `NATIVE_RLWE_NORM_LIFT_AUDIT.md` adds a necessary gate
for ALL fractional scalar maps of an actual native relation: compute
the classical HNF ideal NORM N_I of `(f,k)`, then require both component
algebraic norms <=N_I*R^d. This differs from delta_K, the minimal positive
constant completion multiplier. Neither gate alone supplies embedding
balance, profile quality or a generator. It also audits raw and modular
norm-descent lifts under their separate source/access promises.

Gemini tasks: add exact spectral/profile/ideal validators, independently seeded
native-ratio sweeps, original-coordinate decoding, actual source-law draws
and held-out falsifiers. Keep proxy failure distinct from actual profile
failure and both distinct from hardness. Do not promote a quantum result
without a complete generator and identical-input classical comparison.
