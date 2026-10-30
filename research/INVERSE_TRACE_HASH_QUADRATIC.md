# Hash-Conditioned Quadratic Elimination

29 October 2026. Bounded classical falsification experiment on the original
inverse-trace residuals. No new inverse representation, general algebraic
solver, quantum mechanism, solving-degree theorem, or hardness claim.

## The Specific Question

Can global degree-two elimination certify the saved empty hash cells that
the bounded SAT encoding did not complete? A checked contradiction would
improve an actual missing operation: certifying an empty cell. Failure to
find one is only inconclusive. No new point set, target, residual syndrome,
hash matrix or favorable seed may be substituted after observing a result.

The preceding suggestion to introduce quadratic inverse equations was
not a new capability. Both their compiler and an audit already exist in
`theorems/inverse_trace_algebraic_audit.py` and
[the algebraic audit](INVERSE_TRACE_ALGEBRAIC_AUDIT.md). Reuse them.
General Boolean Groebner tools also already exist, for example
[Sage/PolyBoRi](https://doc.sagemath.org/html/en/reference/polynomial_rings/sage/rings/polynomial/pbori/pbori.html).
Installing such a tool would not itself supply a low-cost native solver.

## Why The Earlier Obstruction Does Not Settle This Test

The [degree-two countercertificate](INVERSE_TRACE_QUADRATIC_CLOSURE.md)
uses two codewords whose supports intersect at one coordinate. Its
sufficient length condition is N>=2K+1. The current shortened residual has
m=K+r:18<31 at n11 and40<73 at n17. Hashing also imposes extra linear
conditions across accepted-root coordinates. Neither change is covered
by simply citing the earlier theorem.

There is a concrete obstruction to extending its arbitrary-local-table
construction. Work on the SAME residual points alpha_i and any particular
solution x_bar of H_R*x=h. Every homogeneous difference has the form

```
delta_x_i = w_i*P(alpha_i),
w_i = 1/product_(j != i)(alpha_i+alpha_j),   deg(P)<r.
```

Choose3r-1 distinct residual indices T, whenever they exist, and set

```
beta_i = w_i^(-3)/product_(j in T, j != i)(alpha_i+alpha_j).
```

Lagrange interpolation, since deg(P^3)<=3r-3<|T|-1, gives

```
sum_(i in T) beta_i*(delta_x_i)^3 = 0.
```

This has Boolean degree two: field squaring is binary-linear. Hence local
xx-covariances cannot be independently prescribed. Set the first local
covariance to e_0*e_1^T+e_1*e_0^T and all others to zero. In the supplied
polynomial basis its contribution is beta_0*(1*2^2+2*1^2)=6*beta_0,
which is nonzero. That local prescription cannot satisfy the global
linear equations and all their variable multiples. This is an obstruction
to THAT gluing construction, not proof that no different local tables work.

Sagan derived this obstruction; parent independently reproduced the field
identity on all homogeneous basis vectors and their pairwise sums:

| Saved residual | r | beta_0 | 6*beta_0 in original field | Checks |
| --- | --- | --- | --- | --- |
| n11 | 3 | 1374 | 1995 | 561 |
| n17, fixed or anchored | 4 | 14438 | 37204 | 2346 |

The field moduli encode as2053 and131081 respectively. Fixed32n local
trace-one graph samples with seed1022 have augmented ranks77 and170 in
coordinates(1,x_bits,y_bits,xx_pairs), meeting2n+binom(n,2). Thus the
indicated xx tables really are locally attainable at trace-legal means;
the failure is global extension, not local impossibility. These finite
rank certificates concern the saved fields, not an all-n rank theorem.

There is also an exact n11 hash restriction: in saved cell2, XOR raw rows
selected by bitmask0x15ab. The row is0x76400=(0x1d9<<10), with RHS zero.
It imposes a nontrivial condition within free block1, beyond that block's
trace condition. Parent replayed the raw-row combination directly.

## Test Definition

Eliminate the ORIGINAL Vandermonde parity equations, all local trace
equations, and the ORIGINAL raw binary hash. Retain deficient hashes and
handle inconsistent hashes explicitly. Use affine free coordinates for:

- the nr bits of free field symbols x_J;
- the B-rank(M) surviving accepted-root coordinates;
- the K(n-1) trace-compatible pivot-inverse bits.

Here B=(n-1)r and k=B-K. At full hash row rank, the total is
d=nr+(B-k)+K(n-1)=nm. There are198 variables at n11 and680 at n17, with
19702 and231541 square-free monomials through degree two. These include
auxiliary inverse variables; they are NOT a count of independent native
solutions or proof of exponential runtime.

Substitute the five existing exact inverse-graph identities, including
the two zero-complete equations x^2*y=x and x*y^2=y. On target-one
coordinates also add xy=1; it is invalid on allowed target-zero points.
Every retained equation is Boolean-quadratic after affine substitution.
These equations are not assumed to span all target-conditioned quadratics.
The separately checked rank certificates below establish that fact only
for the specified fields and targets.

Compute the exact binary row span of their polynomial coefficient vectors.
If it contains the constant polynomial1, retain the explicit XOR of
original equation rows witnessing1=0 and independently replay that XOR.
This is an emptiness certificate for the supplied cell. Otherwise the
result is only a consistent linear relaxation, not a native solution,
cell count, full Groebner basis, or sampling algorithm. Unfinished work
under a cap must remain UNKNOWN, not full-relaxation consistency.

Controls must evaluate compiled equations against independent field
arithmetic, cover legal zeros and nonzero h, and reject corrupted
certificates. Known-anchor cells must never produce a contradiction.
Use the saved n5/n7 cells for exact calibration, the three known-empty
n11 cells for the decisive test, and fixed/anchored n17 cells without
claiming their cardinalities. Report complete setup and elimination costs.

## Complete Local Quadratic Spans

Let U span all genuine target-conditioned graph lifts in the D-dimensional
space of square-free monomials through degree two, D=2n^2+n+1. Let S span
the sampled genuine lifts and C span the known identities: the five field
identities, the trace equation and its products with every local variable,
and xy=1 for target one only. Universal validity of C follows from the
algebraic identities, NOT agreement with samples. Consequently

```
C <= U^perp <= S^perp.
```

If dim(C)+dim(S)=D, both inclusions are equalities. This is an exact rank
certificate of ALL local quadratic relations, not a statistical coverage
claim. Store independent genuine graph points and verify their field
arithmetic, orthogonality and rank separately. The helper is
`theorems/inverse_trace_local_quadratic_span.py`; seed1022 and32n sampled
points are fixed in advance. Include the legal zero explicitly for target
zero, since missing that rare point would produce a misleading rank deficit.

| n | target | known relation rank | true graph lift rank | ambient D |
| --- | --- | --- | --- | --- |
| 7 | 1 | 49 | 57 | 106 |
| 11 | 0 | 76 | 178 | 254 |
| 11 | 1 | 77 | 177 | 254 |
| 17 | 0 | 118 | 478 | 596 |
| 17 | 1 | 119 | 477 | 596 |

All five certificates saturate and independently replay. No field truth
table is generated. The n5 controls and n7 target-zero sample do NOT
saturate; the helper returns UNKNOWN, not an inferred additional identity.
No generic all-local-quadratic compiler is needed for the current n11/n17
fields. This is a finite-field certificate, not a theorem for every n.

## Frozen Campaign Results

Run the new mode on the saved cells, without redrawing inputs or hashes:

```bash
python qsearch.py inverse-trace-sampling --quadratic-cells \
  --input research/classical_baselines/inverse_trace_hash_cells_n11.json \
  --timeout-ms 60000 --max-monomials 300000 --write \
  --output research/classical_baselines/inverse_trace_hash_quadratic_n11.json
```

Five reports use the same suffixes n5,n7,n11,n17,n17_anchor under
`research/classical_baselines/inverse_trace_hash_quadratic_*.json`.
Small inputs consume the preceding n5_reviewed/n7_reviewed reports; the
other three consume their original reports. Every batch consumes three
declared raw cells. The declared60s/cell is a cooperative limit; certificate
replay and local-span setup are paid and not forcibly interrupted. These
are not matched-time SAT benchmarks.

| Cells | variables | monomials | rows per cell | rank per cell | batch seconds |
| --- | --- | --- | --- | --- | --- |
| n5 | 20 | 211 | 120 | 99 | 0.028 |
| n7 | 56 | 1597 | 336 | 280 | 0.052 |
| n11 | 198 | 19702 | 1188 | 990 | 0.534 |
| n17 fixed | 680 | 231541 | 4080 | 3400 | 6.411 |
| n17 anchored | 680 | 231541 | 4080 | 3400 | 6.668 |

Every cell processed ALL rows and has a separately replayed dual formal
monomial vector w with w_0=1 and row dot w=0 for every intended equation.
The triangular elimination basis is not trusted by the checker; it rebuilds
the affine maps and all expected rows. Cap-stopped prefixes cannot certify
full feasibility, even with a forged internally consistent prefix receipt.
Product coordinates of w need not equal products of first moments: this
is emphatically NOT a native solution.

The three n11 cells are empty by the previous32768-point-per-cell exhaustive
hash-slice reference (which shares hash elimination). The n7 cell0 is empty
by the strengthened full4096-u reference without shared elimination.
Both sets now have certified full quadratic-relaxation feasibility. Thus
the failure is not a timeout or merely omission of another local quadratic.
All six n17 cells also have feasible relaxations. The fixed-prefix native
cardinalities remain unknown; the three anchored cells are independently
verified nonempty and use a DIFFERENT residual syndrome from the fixed run.

**Scope:** combine the local saturation certificate with the full per-cell
dual to obtain consistency of all local target-conditioned quadratics plus
the original H, trace and hash equations and their variable multiples.
This does not cover arbitrary global quadratic consequences, higher-degree
derivations that cancel to quadratics, nonlinear solution of quadratic
equations, a Groebner solving-degree bound, counting or uniform sampling.
Producer and replay checkers share compiler/map primitives; neither is an
independently formalized verifier. Independent field-evaluation tests and
Sagan's read-only review found no defect in the frozen certificate scope.

**Decision:** stop adding more local quadratic identities for these fields
or raising this linearization's timeout. They cannot change these checked
row spans. A further algebraic experiment needs a genuinely stronger
operation and a concrete complete-cell/counting hypothesis, not another
equivalent presentation of inversion. The finite failure is not hardness
evidence or progress toward a claimed quantum speedup.

## Research Allocation

Nietzsche separately reviewed constructive Rees applications. No new
motivated family with surviving nonabelian leverage was found. The existing
[specialist review package](manuscripts/REES_REVIEW_BRIEF.md) remains the
appropriate way to test the theorem's correctness and independent value;
no one has been contacted. More receiver formalization or another easy
application family is not a substitute for that question.

The reserve idea was initial-condition symmetry of an iterated quadratic
map. Supply a public quadratic P:F_p^D->F_p^D, a nonzero linear observable
ell and a UNARY iteration count T, with D=5m, p>5 and
Gamma=UT_5(F_p)^m. Seek the FORMAL stabilizer of F=ell composed with P^T.
The arithmetic circuit has size O(T*size(P)) and degree at most2^T.
One fixed fingerprint point over an extension of size
q>=2^T*p^(20m)/delta separates the entire orbit with error at most delta,
using the existing proof and |Gamma|=p^(10m). Evaluation and its reversible
cleanup cost polynomial time in the public input. The quantum consequence
is conditional on the existing Rees theorem, not a new proved application.

It has a strong classical filter. All tuples A_0,...,A_T in Gamma satisfying

```
P(A_j*x)=A_(j+1)*P(x),  0<=j<T;   ell*A_T=ell
```

form a subgroup; its first-coordinate image K lies in Stab(F). The
constraints concern explicit quadratic tensors, so the existing
defining-characteristic solvable-matrix stabilizer baseline computes K in
polynomial dimension. Retain faithful matrix blocks as in the existing
audit. If K=Stab(F), the suggested advantage disappears. Non-propagating
symmetries have not been shown useful or hard; K being proper alone is
also insufficient, for example when unobserved variables create easy
symmetries. Do not promote this reserve idea.

29 October follow-up: the [exact jet filter](ITERATED_QUADRATIC_JET_FILTER.md)
computes low homogeneous components without expanding F, giving a classical
upper group for its stabilizer. Verified group-fixed anchors strengthen
the bound; exact public commutation identities can certify equality.
The p7 coupled cancellation control is fully resolved by two anchors,
and a large tangent-to-identity family has trivial symmetry already from
its quadratic component. Written degree beyond the old guard is not
evidence that the remaining native problem is difficult.

Iterated quadratic scalar postcomposition adds no symmetry for a p-group
with odd p in the coefficient-fixing setting below.
More generally, for a p-group Gamma, a nonconstant scalar polynomial R
of degree d<p, and a formal polynomial F over a field k, assume Gamma acts
by k-fixing automorphisms of the polynomial ring, so g(R(F))=R(g(F)). Then
one has
Stab_Gamma(R(F))=Stab_Gamma(F). Indeed the orbit of F under the former
stabilizer consists of roots of R(T)-R(F) in the polynomial fraction field,
so has size at most d. Its size is a power of p and hence is one. Constant
F is immediate; constant R is excluded. Repeated low-degree scalar
composition therefore cannot create difficult new symmetries merely by
making the final degree exponential. At d=p this argument genuinely fails:
over a field of characteristic p, R(T)=T^p-T acquires translation periods.
This filter does not cover arbitrary
multivariate repeated composition or certify its classical hardness.

The present bounded elimination test is justified by the changed residual,
not by treating quadratic equations as new. Continue to higher-degree or
different-backend experiments only after examining its actual certificate
and cost results. Do not launch a general algebraic-engine rewrite.
