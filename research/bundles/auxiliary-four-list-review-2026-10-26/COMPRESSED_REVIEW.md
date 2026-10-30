# Independent Proof Review: Compressed Graded Algebra

Date: 2026-10-26. Bounded follow-on review of the Gemini handoff.

## 1. Decision And Findings

**ACCEPT the proposed algebraic construction under the true-quadrics,
complete-section-ring promise. REVISE the implementation handoff to make
the verifier, descent, and output-size boundaries below explicit.**

No counterexample was found to the free-module formula, the stated cubic
cokernel identity, unique reconstruction for a good pencil, or the FULL
written all-degree matrix certificate. These conclusions do not depend on
the parent's elliptic control. An independent genus-two reconstruction
and adverse pencil control are recorded below.

Three concrete qualifications should accompany implementation:

1. **The demo `certify()` is weaker than the written certificate.** At
   [control.py:26](/Users/jaspersands/Developer/qsearch-research-work/auxiliary-four-list-review-2026-10-26/compressed_inputs/control.py:26),
   conjugate all actions by `T=diag(1,-1,-1,1)`. The helper still accepts,
   including its `XY*1=e_gamma` check, but `X*1=-e_x` and `Y*1=-e_y`.
   The abstract module remains isomorphic; the designated basis and stored
   representatives no longer agree. The full written beta cyclic checks
   reject this. Thus the 11 passing tests are not already a verifier of
   every listed acceptance gate. Also check explicitly that U=uI and V=vI.
2. **Extension-field descent must not fix u,v artificially.** A chosen
   extension-field pencil need not be Frobenius-stable. Descend fixed
   graded spaces and maps, not an assumed base-field free module over the
   same pencil. Section 6 gives an explicit polynomial construction.
3. **Keep the reduction-map output compressed.** An evaluable exact
   normal-form map is sufficient; a dense matrix with a column for every
   ambient degree-seven monomial reinstates the excluded 99-million-column
   output. The stated cubic elimination count is not the entire adapter
   cost, nor a small-memory/performance guarantee.

These are actionable handoff qualifications, not a rejection of the
mathematical proposal. In particular the parent already calls its code a
symbolic control and its genus-41 construction unimplemented.

I used the independent matrix geometry review only for the initial promise:
the supplied kernel is the entire I_2 of a smooth geometrically integral
curve in its complete degree-ell embedding, ell>=2g+2, and I=(I_2).
I did not reuse that review's graded-algebra construction as a proof here,
review native recovery, or attempt genus-41 arithmetic. All writes are in
this review directory. No parent, Git, UI, or agent actions occurred.

## 2. CM, Pencil, Hilbert Series, And Freeness

Let k be the working field and
`R = direct_sum_{n>=0} H^0(X,H^n) = k[X_1,...,X_N]/(I_2)`.
The full section-ring and quadratic-presentation hypotheses both matter.
A subcode or a ring defined only by some point-vanishing quadrics is not
an admissible replacement.

For the complete normally generated embedding of a smooth curve, R is
normal. The section-ring/projective-normality equivalence is stated in
[Brown--Erman, Section 3.3](https://www.cambridge.org/core/journals/compositio-mathematica/article/linear-syzygies-of-curves-in-weighted-projective-space/C7B17880FDA1605421F0E5297B3E64BA).
Its dimension is two, so normality implies Cohen--Macaulay by
[Serre's S2 criterion](https://stacks.math.columbia.edu/tag/031O).
There is no contradiction with `H^1(X,O_X)` having dimension g: that
cohomology contributes to top local cohomology, not a depth-one defect.

If u,v have no common geometric zero, R/(u,v) is finite-dimensional.
Thus they form a homogeneous system of parameters. In this CM ring they
are regular; this is the parameter criterion of
[Stacks, Lemma 10.104.2](https://stacks.math.columbia.edu/tag/02JN).
It also follows that k[u,v] really is a polynomial ring and R is finite
over it. One cannot assume this for an arbitrary pair of independent forms.

For n>=1, nonspeciality gives `dim R_n=n ell+1-g`; `dim R_0=1`.
Consequently, with b=N-2=ell-g-1,

```text
Hilb_R(t) = (1+b t+g t^2)/(1-t)^2,
Hilb_{R/(u,v)}(t) = 1+b t+g t^2.
```

Choose lifts of an actual quotient basis in degrees 0,1,2. They generate
R over S=k[u,v] by graded induction: in every higher degree the quotient
is zero, so a section is u times a lower-degree section plus v times one.
The resulting surjection

```text
F = S e_0 + S(-1)^b + S(-2)^g -> R
```

has identical Hilbert series on both sides, so its kernel vanishes in
every degree. This proves freeness with precisely the proposed shifts.
It does not appeal to an unsupported claim that every finite S-module is
free. The rank is `1+b+g=ell`.

For ell=84,g=41,N=44, the degree-seven dimension is
`8+42*7+41*6=548`. These are dimensions over k in a fixed degree, not
the dimension of the entire ring or the degree of a degree-one map.

For the sampling bound, fix a nonzero u. Its zero divisor has degree ell
and at most ell geometric support points. At each such point, evaluation
on the k-vector space R_1 is a nonzero linear map, because H is globally
generated. Its kernel contains at most a 1/Q fraction of R_1, even for a
point defined over an extension. A union bound therefore gives failure
at most ell/Q. A successful v is automatically independent of u.
Taking Q>=2ell gives the claimed success probability. This also covers
multiple zeros of u; the support count only becomes smaller.

## 3. The A3 Test And All Cubic Relations

Write A=R/(u,v), V=A_1, and W=A_2. Since u,v are linear and R is
quadratically presented, A is the quadratic algebra
`Sym(V)/(J_2)`, where `J_2=ker(Sym^2(V)->W)`.

Consider the map

```text
d: Lambda^2(V) tensor V -> V tensor W,
d((a wedge b) tensor c) = a tensor (bc) - b tensor (ac).
```

Here is the precise cokernel proof. Start with V tensor V tensor V and
quotient the last two slots by commutativity and J_2, giving V tensor W.
Quotienting additionally by im(d) imposes interchange of the first two
slots. The two adjacent interchanges generate all permutations, so the
result is `Sym^3(V)/(V J_2)`, exactly A_3. Relations J_2 in the first two
slots are consequently included too; they are not missing equations.
No division by 2 or 3 is used. The alternating map is well-defined also
in characteristic two.

This identity fails without the quadratic-presentation promise. For
example, `A=k[t]/(t^3)` has A_3=0 and dim A_1=dim A_2=1, but d=0 and
its cokernel has dimension one: the extra cubic relation was not supplied.
This is outside the parent's hypotheses and explains why they are needed.

For an implementation the complete indexed family is

```text
1 <= i < j <= b,   1 <= k <= b,
```

including k=i and k=j. There are `binom(b,2)*b` rows before redundancies.
Using only triples of distinct indices is incorrect. In the independent
genus-two example it lowers the coefficient rank from six to two.

If the equation matrix has rows indexed by these triples and columns by
the unknowns beta_i gamma_a, it is the transpose orientation of d.
Thus surjectivity of d is precisely full COLUMN rank b*g of the equation
matrix. This orientation is consistent with the handoff.

Since A is generated in degree one, A_3=0 implies A_n=0 for all n>=3.
It therefore certifies no projective common zero of u,v. Under the true
presentation, testing the cokernel of d is a valid way to compute A_3;
it is not circularly assuming the desired multiplication actions.
The A_1 and A_2 dimension checks alone are insufficient; see Section 8.

## 4. Unique Reconstruction And Its Limits

Express all beta_j beta_k in the exact R_2 normal-form basis. Their gamma
coefficients are scalars. All other coefficients involve u,v and known
basis vectors 1,beta_l. Hence

```text
beta_i(beta_j beta_k)-beta_j(beta_i beta_k)=0
```

is a linear equation over k in the b*g unknown F_3-valued products
`X_(i,a)=beta_i gamma_a`. Its coefficient matrix is exactly the matrix
above, and its known right side lies in F_3 of dimension `4+3b+2g`.
It is not a polynomial system in unknown matrix entries.

For a certified good pencil, freeness already proved in Section 2
supplies actual multiplication actions in this basis. Thus the system
is consistent. Full column rank makes their F_3 coordinates unique.
Solving a full-rank row subsystem and checking every remaining equation
is valid; accepting an arbitrary subsystem without those checks is not.

Full rank by itself does not prove consistency of arbitrary proposed
right sides. Nor does it recognize a smooth curve or make a corrupted
R_2 table true. The original exact normal forms and geometric input
promise remain premises. The additional matrix checks below turn the
computed output into a useful independent algebra certificate.

The construction is complete because R is generated by R_1: u,v act
as scalars, beta_i*1 and beta_i*beta_j are known, and these X_(i,a)
are every remaining column. All entries have the prescribed degree
`1+shift(column)-shift(row)`, hence degree at most three. No separate
unknown gamma*gamma products are needed; use their stored quadratic
representatives and the commuting generator actions.

## 5. All-Degree Soundness Of The Full Certificate

This argument uses the entire polynomial matrix identities, not tests
at finitely many values of u,v or associativity only through degree three.

Let P=k[u,v,beta_1,...,beta_b], R=P/(I_2), and F the proposed FREE
S-module. Require U=uI,V=vI, pairwise commuting beta matrices, and
every exported quadratic to act by zero. These give an algebra map
`rho:R -> End_S(F)`. Define the S-linear map

```text
phi:R -> F,     a |-> rho(a)e_0.
```

Define `psi:F -> R` using the recorded actual lifts of 1,beta_i,gamma_a.
The correct A_0,A_1,A_2 bases and A_3=0 prove psi is surjective by graded
induction. The cyclic-basis conditions are exactly

```text
rho(beta_i)e_0=e_i,
rho(recorded_gamma_a)e_0=e_a.
```

They imply `phi psi=id_F`. Hence psi is also injective, so psi and phi
are inverse S-module isomorphisms. Transporting multiplication from R
gives the claimed algebra on F, and rho is its true multiplication action
in every degree. A hidden higher-degree relation would contradict this
isomorphism. No finite-degree Hilbert extrapolation is involved.

This also identifies the exact role of the control.py counterexample:
its conjugated matrices still represent the right abstract algebra, but
not in the named beta basis. The full certificate's cyclic checks and
R_2 agreement rule it out. The proposed certificate is sound; the current
demo helper is not yet its complete implementation.

## 6. Extension Fields And Descent

For large ell at fixed q, take a represented extension K/k of degree
`d=max(1,ceil(log_q(2ell)))`. Its degree is logarithmic in ell at fixed q.
The construction then gives `R_K` free over `K[u,v]`. Smooth geometric
integrality, the true quadratic presentation, and the Hilbert dimensions
persist under this field extension. The all-degree certificate applies
over K, and faithful field extension preserves its equalities for the
original presentation.

It does NOT follow that this chosen polynomial subring descends. A concrete
countercontrol is the conic

```text
R=F_3[X,Y,Z]/(XZ-Y^2),
K=F_9=F_3(alpha), alpha^2=-1,
u=X+alpha Z, v=Y.
```

This pencil is basepoint-free: when Y=0 the conic has only the two
geometric points with XZ=0, and u is nonzero at each. But Frobenius sends
u to X-alpha Z, which is not in the K-span of u,v. Coefficient Frobenius
with formal u,v held fixed is therefore the wrong descent action.

There is a simple exact descent procedure for each requested finite
truncation, without descending the pencil or expanding all monomials:

1. Express each ORIGINAL k-defined degree-one generator X_l as an action
   in the certified K-module, using the stored inverse basis change.
2. Start with the basis {1} of R_0(k). From a chosen k-defined basis of
   R_{j-1}, form the N*dim(R_{j-1}) products X_l*b inside the compact F_j.
3. Select a K-linearly independent spanning subset of these candidates.
   They are all intrinsically k-defined, and independence/spanning is
   unchanged by faithful field extension. The selected subset is therefore
   a k-basis of R_j. Store its original-generator words or expression trees.
4. Express products in these bases by exact K-linear algebra. Uniqueness
   and k-defined inputs force every structure constant to lie in k; check
   that each is fixed by a->a^q and extract its base-field coordinates.

For fixed h, every compact dimension is O(h*ell), and the number of
candidates per degree is O(N*h*ell), not the ambient monomial count.
This gives a polynomial, concrete descent of bases, multiplication, and
original-section inclusion. It does not promise a global free module
over a base-field pencil with those same u,v.

Alternatively one may compute the genuine semilinear Frobenius on F_j
using original polynomial representatives, then take fixed spaces. The
action must move the extension-defined pencil and basis, as the conic
example shows. Neither option is implemented in this review. The native
evaluation frames and tangent normalization still have to be transported
and verified by the eventual adapter, not inferred from descent alone.

## 7. Complexity And Output Contract

Let m=binom(b,2)*b, n=b*g, and c=4+3b+2g. The cubic solve with all
right sides costs `O(m*n*(n+c))` by naive elimination. Since g<=N-3,
this is `O(N^5 g^2)` for g>=1, as claimed. At g=0 the unknown system is
empty; other setup work is not zero.

Charge quadratic normal-form computation, coordinate changes, polynomial
matrix certification, finite-field construction/arithmetic, descent, and
the actual requested multiplication-table output separately. For example,
dense degree-two elimination admits an O(N^6) bound; the cubic-only bound
need not dominate it for small g and large ell. These remain polynomial.

The exact genus-41 SIZE counts, not an allocated or benchmarked system, are:

```text
m = 36,162 equations
n = 1,722 unknowns
c = 212 right-side coordinates
m*n = 62,270,964 coefficient entries
m*(n+c) = 69,937,308 augmented entries
n*(n+c) = 3,330,348 augmented pivot entries
```

A dense augmented array alone is about 280 MB at four bytes per field
entry, before overhead. Streaming independent pivot rows can avoid storing
the full array; all redundant equations still need checking. Sparsity of
the initial rows does not prevent elimination fill-in. Polynomiality is
not a measured practical running time.

For a compact reduction map, apply original-generator action matrices to
e_0 for a supplied monomial or expression, and add terms as needed.
Materialize dense structure constants only between compact graded pieces
when required. Demanding a dense ambient-monomial-to-R_7 matrix has the
unavoidable 99,884,400-column output at N=44; the compressed design cannot
make that output small. No higher-degree Groebner basis or such dense map
is needed by the proposed certificate and reduction procedure.

## 8. Independent Controls And Reproducibility

The script
[compressed_controls.py](/Users/jaspersands/Developer/qsearch-research-work/auxiliary-four-list-review-2026-10-26/compressed_controls.py)
does not import the parent's multiplication construction. Only the explicit
demo-verifier countercontrol imports its frozen helper. Exact results are in
[compressed_controls.json](/Users/jaspersands/Developer/qsearch-research-work/auxiliary-four-list-review-2026-10-26/compressed_controls.json).

The main control is the smooth genus-two curve `y^2=x^5+x+1` over F_17,
with H=6 infinity and complete section basis `1,x,x^2,y,x^3`. Squarefreeness
of the degree-five polynomial is checked. In homogeneous variables ordered
`(u,v,x,z,y)=(1,x^3,x,x^2,y)`, its four quadrics are

```text
x^2-u z,    x z-u v,    z^2-v x,    y^2-v z-u x-u^2.
```

Choose the good pencil (u,v), betas (x,z,y), and gammas (xy,zy).
The script starts from these quadratic normal forms, BUILDS the nine-row
cubic system, and solves all six missing actions with seventeen right
sides. All equations are checked. The recovered actions pass full matrix
commutation, quadratic identities, homogeneous shifts, and every cyclic
basis relation. This tests reconstruction, not just hand-entered actions.

| Control | Exact result |
| --- | --- |
| Full genus-two cubic system | Rank 6 of 6; all right sides consistent |
| Only distinct triples | Rank 2, demonstrating the missing repeated-index constraints |
| Direct Macaulay quotients versus generated free pieces, degrees 0..7 | Both give 1,5,11,17,23,29,35,41 |
| Generator change (x+2z+3u, 5z+v, y+4x) | Reconstructed matrices agree with independently conjugated actions |
| Abstract coefficient map in characteristics 2,3,5,17 | Rank 6 in each; this is not a smooth-curve claim in characteristic 2 |
| Parent elliptic helper after diag(1,-1,-1,1) conjugation | Accepts despite failing the designated beta cyclic relations |

For the bad pencil choose `(v+x, v+y-u)`. It contains the point
`[u:v:x:z:y]=[1:0:0:0:1]`. Eliminating v=-x and y=u+x gives the quotient

```text
F_17[u,x,z]/(x^2, u z, z^2, x z+u x),
Hilbert dimensions = (1,3,2,1,1,...) .
```

Thus the expected A_1 and A_2 dimensions both pass, but A_3 has dimension
one and the cubic coefficient rank is five, not six. This directly checks
the proposed decisive pencil test on a genuine smooth-curve example.

All **11 frozen parent tests also passed** in the existing local environment
with python-flint. The system Python lacked that dependency; no package
installation or environment modification was performed.

Run from this review directory:

```sh
env PYTHONDONTWRITEBYTECODE=1 /Users/jaspersands/Developer/qsearch-research-work/matrix-lift-access-review-2026-10-26/.venv/bin/python -B compressed_controls.py > compressed_controls.json
env PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /Users/jaspersands/Developer/qsearch-research-work/matrix-lift-access-review-2026-10-26/.venv/bin/python -B -m pytest -q -p no:cacheprovider compressed_inputs/test_compressed_control.py
```

Finite tests support the implementation proposal but do not prove its
all-degree or all-genus statements; those are proved above. No genus-41
arrays, native lift, divisor operations, sampler, group order, or native
witness were constructed. The extension-field discussion is a proof and
explicit procedure, not a tested extension-field adapter.

## 9. Frozen Inputs

Reviewed copies and their SHA-256 hashes:

```text
compressed_inputs/HANDOFF.md
957ed7da20003a28c244dd30ff3914c73dbbc589638f796a9275bbf9a3ebc16b
compressed_inputs/control.py
173a6209e2db7266a8aed76ea806d814dbfb2773d0788e72f7bb1f5f49dba208
compressed_inputs/test_compressed_control.py
d03759e87cb0bc8524c499b94124c93244f86fff6160cc4c297673bf37e3dc93
compressed_controls.py
b2cec2a2f38cc3a4e2ba8d6e4699c1f4e4886b74f02585251884c952f0553270
compressed_controls.json
6591b0c43515287e18bcc74fdcc5df14520a073af8bd2438ae874232d978a4f7
```

The matrix geometry review used for the initial true-quadrics promise had
SHA-256 `8f011b48e00f6159f4f788669289074dd4b11c2b4ea94189e39e02ed32192c7c`.
No claim of originality is made for the construction or these arguments.

**Final handoff:** the proposed compression is mathematically defensible.
Implement the FULL certificate, retain repeated-index cubic equations,
make the descent/output representation explicit, and measure the actual
linear algebra before claiming practicality. This remains a reviewed
design with small independent controls, not a completed native backend.
