# Native RLWE: Subfield-Restricted Affine Covers And Their Limit

Date: 2026-10-04. LOCAL DERIVATION / REVIEW PENDING. Exact classical
construction and source/output-class bounds, not a new subfield attack,
quantum algorithm, asymptotic solver or independent proof verification.

## 1. Why Test This Next

The prelabel-unit audit leaves genuinely label-adaptive directions open.
A classical competitor should exploit the field structure before any
quantum construction gets credit. Subfield attacks and smaller-dimensional
projected lattices are established techniques; the
[Duong--Yasuda--Takagi paper](https://eprint.iacr.org/2017/959.pdf) discusses
both. Its planted short NTRU-key setting does NOT establish an attack on
our independently uniform native ratio. The following construction tests
the actual public kernel without planting a key or invoking norm inversion.

The [Falcon specification](https://falcon-sign.info/falcon.pdf) uses field
norms to complete an already supplied short pair. Do not confuse that
operation with finding the missing pair on uniform public labels.

Decision: test a ONE-LEVEL compressed classical affine cover, not a deep
tower shortcut that leaves a final witness block confined to a tiny
subfield. The latter output class has a strong source-counting falsifier.
This is not a rejection of all norm-descent methods: an unrestricted
lift or completion may escape this final-output restriction.

FOLLOW-UP: `NATIVE_RLWE_NORM_LIFT_AUDIT.md` now audits that escape.
It distinguishes raw integer norm lifting, modular recentering and
fractional content, with different scope for each. Norm-only lower
solutions plus elementary lifting/ordinary amplification fail the stated
native source tests; full-label orientation-sensitive lifts remain open.

## 2. Explicit Classical Construction, No Missing Oracle

Let R=Z[X]/(X^d+1), d a power of two, q the native modulus, and normalize
ONLY the public kernel to `[I,M]`. Keep the original secrets, noise and
records. Choose a divisor h of d, set r=d/h, and let E_h embed
`Z[Y]/(Y^h+1)` into R by Y=X^r. Its coefficient matrix selects positions
`0,r,...,(h-1)r`, so `E_h^T E_h=I_h` in the ORIGINAL coefficient metric.

Restrict the second witness block to E_h y, but let the first block x
remain arbitrary. Compressed coordinates have dimension n=d+h. The exact
integer kernel basis is

```
H_h=[I_d, M E_h],
B_h=[q I_d, -M E_h; 0, I_h],
det(B_h)=q^d, H_h B_h=0 (mod q).
```

No inverse or unit assumption on M is needed. This is the FULL kernel in
the restricted real subspace, not a full-rank basis in the ambient 2d
dimensions. The embedding `(x,y)->(x,E_h y)` is isometric. A syndrome w
has the explicit compressed section `(w,0)`. Classical lattice reduction
and nearest plane therefore give, for every syndrome,

```
H_h c=w (mod q), 4||c||^2 <= Gamma(B_h_reduced),
Gamma=sum exact squared Gram--Schmidt lengths.
```

Normalize the original chosen syndrome as
`w=C_a1^-T(t e0)`, not as t e0 by changing the secret/noise distribution.
Expand the witness back to 2d coordinates. Signed rotations then supply
the original d equations as in the rotational-witness reduction.

The sufficient original box/norm decoder gate is unchanged:

```
E_noise^2 Gamma < t_star^2,
t_star=floor(q/(2R_s+1)).
```

This is an executable classical candidate baseline: matrix formation,
integer LLL/BKZ, nearest plane and original-coordinate verification. It
does NOT assume a short-vector, ideal-CVP, unit-group or quantum oracle.
Reduction cost and actual success at growing d remain to be measured.

## 3. Exact Necessary Geometric Headroom

The product of the n squared GS lengths is q^(2d). Arithmetic-geometric
mean implies

```
Gamma >= n q^(2d/n).
```

Thus the all-syndrome Babai/norm certificate is impossible unless

```
(n E_noise^2)^n q^(2d) < t_star^(2n).
```

This entirely integer test avoids taking uncertain real roots. It is
necessary, NOT sufficient. A valid nonzero actual chosen residual could
be much shorter than the worst-case cover; the next argument separately
tests that possibility under the source law.

With q of order d^12 and `P=R_s E_noise` of order d^2 log^(5/2)(d),
the necessary scaling becomes

```
q^(2h/(d+h)) > order (d+h) P^2.
```

Writing theta=h/d, the power threshold is theta>5/19. Equality still
loses to the logarithmic factors. One level, h=d/2, is not excluded
asymptotically by this gate; two levels, h=d/4, and deeper are. Exact
reference checks give:

| d | Half-degree compressed rank | Spherical headroom | Elliptical headroom |
| ---: | ---: | --- | --- |
| 64 | 96 | Not excluded | Impossible |
| 256 | 384 | Not excluded | Not excluded |
| 1024 | 1536 | Not excluded | Not excluded |

Every quarter-degree/deeper reference row fails the necessary gate.
"Not excluded" is NOT an existence, LLL-success or security claim.

## 4. Stronger Source Falsifier For Actual Affine Points

Use the actual conditional native law: a1 uniform among units, a2
independently uniform in the whole ring. Set

```
v=C_a1^-T e0, M=C_a1^-T C_a2^T.
```

Then v is uniform on units and independent of M. For EVERY fixed integer
pair (x,y) and nonzero scalar t, conditional on M,

```
x+M y=t v (mod q)
```

has probability at most 1/U, where U=#R_q^*. This includes nonunit y
and nonunit second labels; neither needs to be discarded. It is a
maximum-density statement about v, not an assumption that M is an iid
random d-by-d matrix.

For a block confined to the h-dimensional coefficient subspace, every
pair of norm <=R0 corresponds isometrically to an integer point in a
ball of dimension n=d+h. Union over ALL such points and ALL q-1 scalar
labels gives

```
B_h_point <= min(1, (q-1) N_n(R0)/U).
```

This permits arbitrary adaptive choices based on F AND b. The entire
finite output set is counted before sampling labels; it does not assume
that the algorithm's choices are independent. The same argument applies
to restriction of EITHER block without charging an a2-nonunit event.
It also strengthens the older sparse audit's conservative either-block
bound: joint pair counting gives 2*beta without its added nonunit-event
term. The older bound remains valid, just unnecessarily loose.

For exact integer reference tests, surround each integer ball point by
its unit cube. These cubes fit in a ball of radius R0+sqrt(n)/2. The unit
ball volume is <=(sqrt(2*pi*e/n))^n by Gaussian integration, and
sqrt(2*pi*e)<5. With s=floor(sqrt(n)), conservatively

```
N_n(R0) <= [(5R0+3s)/s]^n.
```

Use `R0=ceil(t_star/(2E_noise))`, which includes every strict passing
affine witness for ANY scalar label. At the high-CRT references,
`U=(q^(d/2)-1)^2`. The probe checks the bound by full integers, including
2r possible support classes: either block and every monomial shift of the
subfield subspace. Thus adaptively selecting among those supports is covered.

| d | Quarter-degree spherical: B_h_point < 2^exponent | Elliptical |
| ---: | ---: | ---: |
| 64 | -558 | -572 |
| 256 | -2806 | -2802 |
| 1024 | -12715 | -12236 |

The table is per support; the exact tests ALSO charge all eight support
classes at quarter degree. All quarter/deeper cases remain <=1e-8 after
their full support-catalogue factors. Half-degree density bounds are
VACUOUS, not evidence of successful witness finding.

At fixed theta, the spherical log-bound has leading terms

```
log B_h_point <= [(19/2)theta-5/2] d log d
                -(5/2)(1+theta) d log log d+O(d).
```

At theta=1/4 its first coefficient is -1/8. This independent source
counting excludes typical successful AFFINE witnesses in the stated
restricted output class, not only its worst-case cover certificate.

## 5. Attempted Refutations And Scope

- **Adaptive denominator:** allowed within the entire restricted output
  set. This is stronger than the prelabel-unit argument for this subclass.
- **Second-label zero divisors:** included by joint maximum-density
  counting; the construction also never inverts M.
- **A lucky chosen coset despite a bad global basis:** not excluded by
  the GS determinant gate alone, but covered by the separate point-count
  probability bound at quarter degree/deeper.
- **A new basis makes the vector sparse:** not covered. The restriction
  is in the original orthogonal coefficient basis; a label-adaptive basis
  changes the output class and metric/counting ledger.
- **A small subfield norm followed by a full-dimensional lift:** not
  generally excluded. If the FINAL affine vector has both unrestricted
  blocks, the bound does not apply. Likewise, a homogeneous relation with
  a subfield block can be completed into unrestricted affine outputs.
- **Unit multiplication:** a multiplier outside the subfield may escape
  the restriction; that new output must be evaluated, not silently counted
  as the same support. Monomial support shifts are explicitly charged.
- **Sharper or statistical decoder:** outside this norm/box certificate.
  Actual zero-noise/easier-prior inputs cannot justify the stated contract.
- **Finite controls:** do not prove growing-degree lattice reduction works.
  No prior/noise law is sampled; prime chains are referenced, not replayed.

## 6. Reproduce And Delegate

```
python research/certificates/native_rlwe_subfield_cover_probe.py --save
```

The probe verifies exact restricted kernels, metric preservation,
determinants, GS products, nearest-plane syndrome preservation and small
integer-ball counts. A finite joint-density control explicitly retains
noninvertible second blocks. Reference artifacts contain all 54 choices
of source lane and power-two restriction degree, not just successful rows.
The source arithmetic hash is recorded. LOCAL REVIEW PENDING throughout.

Gemini: implement the ONE-LEVEL compressed cover as a matched classical
baseline, starting with the SAVED d64 native ratio, before independent
source sweeps. Preserve actual original syndromes/records, exact GS/profile
checks and total cost. Reproduce the d64 elliptical headroom failure as an
expected negative control. Test classical LLL/BKZ rather than assuming a
success probability. Restrict larger runs using the necessary gate first.
Do not restore circuit search or promote the half-degree vacuous density
bound to a quantum signal. No large-degree compressed LLL run, routine
CLI/registry wiring, full production suite or commit in this theory pass.
