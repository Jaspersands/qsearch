# Native tower batching: independent dependency and bit audit

2026-11-13. The completed 689-line OpenAI report was read in full, together
with STATE/TRAPS, the native four-operation contract, the retained tower
note, the 332-line tagged-coordinate proof and the stable sparse-gluing and
maximal-order reviews. No API, network, Git, live report or finite sweep.

**Core finding:** the six-child scheduling and aggregate payload recurrences
close. There is no same-field U/C cycle in this schedule. The conclusion
uses a uniform affine-height postprocessor for an ALREADY KNOWN ternary
witness, including at rational leaves. Its auxiliary-order implementation
is a separate arithmetic lemma, not an unexplained call to a conic solver.
The stable 240-line proof of that lemma has now been read in full. The
precise modular scope and prerequisites are stated at the end.

The material interface repairs are: return original-target views explicitly;
sparsify and square-reset AFTER undoing their normalization; use exact
coefficient-prime support; and enforce each form's own prime cutoff. A
field-only bound for arbitrary restored original targets would be false.

## 1. What target normalization does, and does not, preserve

Fix K and its ORIGINAL support S_K. This support is never enlarged during
native U recursion. For target ideals J_j the ideal reset gives
  (w_j) J_j=M_j,   Jbar_j=odd_(outside S_K)(M_j),
where each log N(Jbar_j) is bounded by a polynomial in the original field
data. The exact isomorphism of PAIR spaces is
  Psi:([x],c) |--> ([x product_j w_j^c_j],c).                 (1)
Its inverse divides by that product. All tags, including pure tags with
element class 1, remain present. No local norm condition may forget this
change of representative.

Counterexample to an unrestricted height inference: over Q, S={2}, let
J=(p) for an arbitrarily large odd prime. Every element with tag 1 has odd
p-valuation, so its rational height is at least log p. The reset w=1/p makes
Jbar the unit ideal and sends (p,1) to (1,1). Undoing it restores that height.
Thus a field-only height bound applies to NORMALIZED presentations, or to
restored requests whose original target norms were already field-bounded.
It does not apply to arbitrary original targets. The desired root S-basis
has no target tags, so this distinction does not obstruct that endpoint.

Here is a complete subrequest interface, needed in place of an informal
instruction to extract an answer from the common presentation. Let columns
(x_l,c_l) be the complete aggregate basis in normalized targets. To extract
a request using a specified subset of targets:

1. Compute the kernel of all forbidden-tag rows by binary elimination.
2. Take a basis of this kernel; record its full-column-rank matrix T in the
   aggregate coordinates. Form the corresponding element products.
3. Divide by the normalization scalars for their ORIGINAL requested tags.
4. Sparsify in those ORIGINAL tag coordinates, recording the additional
   binary basis changes, and square-reset the actual restored elements.

For a query (x,c) in this view, pad its tags by zero, apply (1), call the
aggregate coordinate routine ONCE, and solve Tz=v, including the recorded
later basis changes. Square resets do not change the class-coordinate map.
There is no recursive search for a subrequest basis and no fresh U call.
All matrices, scalar products and reset witnesses have their expanded cost.

For a local character chi, a normalized pair ([x],c) represents the original
element x/product w_j^c_j. The actual row to use is
  chi(x)+sum c_j chi(w_j) over F2.                           (2)
This also pays the report's phrase "corrected by the scalars" constructively.

## 2. Sparse native bases really remove batch-size height feedback

For any target list, its tag image is
  ker(F2^r --> Cl(O_K,S_K)/2),  c |--> [product J_j^c_j].
Its codimension is at most c_K<=log_2 h_K. This is a structural identity,
not an instruction to compute a class group. The already checked ideal-reset
plus HNF count gives a polynomial field-data upper bound for c_K.

A subspace of codimension c has a basis whose vectors have weight at most
c+1: put a parity-check matrix in pivot-column form and lift one nonpivot
coordinate at a time. From a computed pair basis, binary elimination gives
the zero-tag kernel and lifts of this sparse tag basis. If ell additional
character equations are imposed first, the image codimension rises by at
most ell. Both assertions include repeated or zero targets.

Apply this AFTER inverse normalization when the caller expects the original
presentation. In the actual U recursion its first-child requested targets
are norms of already normalized targets, hence already have bounded norms;
its second-child targets have the ideal-reset bound. Sparse representatives
in those original targets therefore have odd support in fixed S_K and at
most c_K+ell+1 bounded-norm ideals. Weighted squareclass reset bounds their
intrinsic height by a field-data polynomial W, independent of tag count.

The first norm-compatible H basis must undergo this operation before its
relative norm conics are submitted. Its local equations occur only at fixed
S_K and real places. Thus their number is field-bounded. Its dimension is
still at most r+D_K, where D_K=dim K(S_K,2) is field-bounded, but a large
dimension does not make each of its conic coefficients large.

Dense intermediate products can contain polynomially many basis elements.
Their cost depends on the current payload. They are explicitly expanded and
reset before entering a recursive conic. There is no claim that the dense
products themselves have height W. A coefficient-tag J_q for a gluing form
may have large norm; undoing that particular scalar is handled instead by
the final common-value support bound in the next section.

## 3. One coefficient tag, a shared pool, and a linear common-value bound

Let q=<a1,a2,a3,a4> be a promised isotropic nonsingular quaternary. Diagonal
degenerate cases are detected and solved by the fixed-rank wrappers. First
square-normalize the coefficients, retaining their coordinate rescalings.
Let S_q consist of fixed S_K and the ACTUAL nonzero prime-ideal valuations
of these coefficients. A support-covering rational factorization must be
followed by ideal valuations and deletion of zero-valuation primes. Keeping
all primes over every rational factor is insufficient for the linear bound.

For H the sum of extensive coefficient heights n*h(a_i), and
  w_q=sum_(P in S_q) log N(P),
weighted normalization and the height/product formula give
  w_q <= C(H+W),                                           (3)
with an absolute C. The field polynomial W is fixed in the original data.

Set d1=-a1*a2, d2=-a3*a4. At each place in S_q choose a local squareclass b_v
satisfying (b_v,d1)=(a1,d1), (b_v,d2)=(-a3,d2). Local isotropy ensures that
these two character equations are consistent. Define ONE coefficient tag
  J_q=product_(P in S_q minus S_K, v_P(b_v) odd) P.            (4)
The choices can be prescribed simultaneously: a smooth isotropic quadric
with a K-point is K-rational and has weak approximation. In detail, its
projection chart from a K-point is an open of affine space; locally move
off the exceptional loci and apply weak approximation to its coordinates.
This is an existence proof, not an algorithm requiring that K-point.
It gives an unknown global nonzero common value with those local classes.

The already source-checked ERH ray-class argument moves its outside-S_q odd
ideal to split prime ideals with norm <=X_q=(32 L_q)^2, preserving the chosen
local classes and signs. Its remaining outside-S_K parity is J_q plus a
sum of those primes. Thus a COMPLETE tagged presentation with this one J_q
and the allowed prime tags contains a feasible affine slice. No norm-image
surjectivity or odd-class-order hypothesis is introduced.

For all ready forms take one pool of degree-one primes through
X_batch=max X_q. Each form's mask MUST require:
  P outside S_q,  N(P)<=X_q,  and both residue-square tests.
The individual cutoff condition is missing from the report's literal mask;
adding it preserves feasibility and justifies its individual height bound.
There are at most n*X_batch pool ideals. Normalize all target ideals, build
one aggregate U, and impose own coefficient tag 1, other coefficient tags
0, and the appropriate masks/character rows using (2). A unit J_q still has
its formal tag. Duplicate targets are not removed without tracking labels.

Fixing other tags and deleting disallowed prime variables leaves at most
c_K+ell_q affine constraints on the allowed prime tags after eliminating
the zero-tag variables. Select pivot columns of this projected system.
Exactly as in the checked sparse-gluing proof, a solution can be chosen
using at most
  rho_q<=c_K+ell_q,  ell_q<=2|S_q|+2r1                      (5)
allowed primes. One uses two quadratic Hilbert CHARACTER rows per finite
place, not a redundant degree-times-as-many row count. The latter estimate
would lose the needed absolute height slope. Dyadic norm-image computation
may use a larger temporary matrix, but a nonsplit quadratic local norm
subgroup has index two, giving one independent character for each binary
norm condition. Split or complex factors impose none.

After undoing the target scalars and applying the squareclass reset to the
ACTUAL common value, its extensive height is at most
  C_field + w_q + (c_K+2|S_q|+2r1)*log X_q.                 (6)
The dependence here is on original parity support, not the heights of the
inverse-normalization products used temporarily to construct it.

The apparently dangerous term is linear in w_q up to a field polynomial.
Write t=|S_q|. At most n prime ideals have any given integer norm, so sorting
them gives, with natural logarithms for this estimate,
  w_q>=log(t!)-t log n>=t log(t/n)-t.
Also log X_q=O(1+log(L0+w_q)), with L0 field-bounded: the dyadic contribution
to log N(m0) beyond w_q is exactly at most 2n log 2.
When w_q dominates n^4 and L0^2, split into t<=sqrt(w_q), which immediately
gives t log X_q=O(w_q), and t>sqrt(w_q), where the displayed lower bound
again gives t log X_q=O(w_q). The complementary bounded range is polynomial
in n,L0. Finally c_K log(1+w_q)<=w_q+O(c_K log(c_K+1)); handle r1 similarly.
Consequently (6) is <=C_b(H+W) for an ABSOLUTE C_b, after choosing W once
as a sufficiently large polynomial of the raw field/support data. This
does not define W circularly as a polynomial of itself.

Two actual ternary solves for the chosen common value, followed by cross
multiplication, give the quaternary witness. If a returned ternary has zero
last coordinate, its binary zero directly solves the quaternary instead.
This avoids producing the all-zero cross product. Undo coefficient square
rescalings at the end; their heights are bounded by half the sum of the old
and new coefficient heights, so this keeps a constant height slope.

## 4. Dependency-respecting construction: all six children are lower-field

Use Batch_i(r,m,k) for a ready U request with r targets (if present), m
ternaries, and k quaternaries over F_i. The original target presentation is
part of the request. Empty or repeated tags remain counted. P_i=0 when
k=0; otherwise P_i is the one common prime pool above. Put
  r'=r+k+P_i,   s<=r'+D_(i-1),   t=m+2k.

The actual ordered lower calls are:

1. Batch_(i-1)(r',0,0), for norm-pushed normalized targets.
2. Batch_(i-1)(0,s,0), for first-pair norm conics AFTER step 1 has returned
   in its original targets and its H basis has been sparsified/reset.
3. Batch_(i-1)(s,0,0), for residuals computed from step 2, ideal-reset, and
   followed by squareclass normalization of the stored norm lifts.
4. Batch_(i-1)(0,0,t), for the first transfer quaternaries of the ready
   original and gluing ternaries. Their coefficients are now known.
5. Batch_(i-1)(0,t,0), for middle conics prepared from step 4's witnesses.
6. Batch_(i-1)(0,0,t), for final embedding quaternaries prepared from step 5.

Between steps 3 and 4 construct the aggregate U quotient, remove exactly
([d_i],0) using the stored second-child coordinate routine, and obtain the
common values for the ready quaternaries. After step 6 reconstruct and
shorten all ternary witnesses, then glue the original quaternary answers.
No input for steps 5 or 6 is guessed before its predecessors return.

The fixed-rank transfer improvement is the source-checked E/C/E wrapper:
a split quaternion's six-dimensional pure-square transfer is 3H, hence
every four-dimensional restriction contains an isotropic vector. The
middle Pfister step is a lower ternary; the final embedding step is a lower
quaternary. Its zero-divisor exits and constant-grid choice of an invertible
anticommuting element must be retained. The parent checked these against
the actual Kutas passages; no new generic controllability/isotropy theorem
is inferred here. A scalar-dependent discriminant extension is NOT used to
solve either quaternary.

Thus the dependency graph has U_i depending on U_(i-1), C_(i-1); C_i on
E_(i-1), C_(i-1), E_(i-1); and E_i on its ALREADY BUILT aggregate U_i and
the C_i jobs scheduled in the same batch. Replacing E_i by an independent
recursive call that rebuilds U_i would be a different, unpaid algorithm.
The written six-child schedule contains no such call.

At i=0, U_Q is signed prime-parity arithmetic. Rational ternaries use the
already checked factoring backend and then the SAME witness postprocessor.
Rational quaternaries use the common U_Q and two such rational ternaries.
There are no lower-field batches or free conic oracles at a leaf.

## 5. Symbolic degree-height recurrence, with no batch exponent feedback

Use extensive absolute height H_K(x)=[K:Q]*h(x), summed on fixed-rank
tuples. Relative quadratic norm, trace and extraction of the two lower
components change it by absolute constant factors plus fixed tower-data
terms. With the usual natural-log height, coordinate conversion is only
temporary workspace: ell_K(x)<=(2/log 2)H_K(x)+kappa_K+O(1). Inversion
preserves h. One must NOT recompute the next
height bound by multiplying each returned coordinate bound by [K:Q].
Keep the shortened point vectors in expanded RATIONAL coordinates; clearing
all their denominators to propagate a chosen integral vector can insert
exactly the forbidden degree factor. The fixed-rank wrappers need field
coordinates and do not require that clearing.

The needed witness lemma is: a KNOWN nonzero isotropic vector for a diagonal
ternary can be replaced by one of extensive tuple height
  <=64*(H_coeff+log|disc K|+n^2).                            (7)
Its runtime charges the incoming expanded witness. This applies at n=1.
Let C_C=64, with a harmless enlargement for fixed-format conversions.
The sparse gluing result and two shortened ternaries give
  H(E_i output)<=C_E*(H(E_i input)+W),                       (8)
for one absolute C_E, independent of i. Cross products and recorded square
coefficient rescalings use only constantly many multiplications.

These constants have no recursive definition. To make the next step
explicit, let C0 be a fixed height bound for each of the three finite
fixed-rank wrappers and its reconstructions, including the supplied tower
radical. This is an absolute constant from their constant-degree rational
expressions and fixed-size linear systems. Set
  u1=C0,              v1=C_E*(u1+1),
  u2=C0*(1+v1),       v2=C_C*(u2+1),
  u3=C0*(1+v1+v2).
Let C_T bound the height of either gluing ternary by C_T*(H+W), from (6).
Then take
  C_*=2+(C_T+1)*max(u1,u2,u3).
Every recursive child coefficient tuple has
  H_child<=C_*(H_parent+W).                                (9)
Native U norm-conic coefficients are already bounded by W, by section 2.
All constants are fixed once the finite wrappers are fixed; none depends
on level, field degree, payload, or returned witness. This is why the
postprocessor closes the otherwise coupled height slopes.

If H0 bounds the root coefficient tuples, a safe uniform bound is
  H_max=2*C_*^(h+1)*(H0+W).                                 (10)
Since h=log_2 N, this is polynomial in original N,B,H0. In the requested
S-squareclass root, H0 is field-bounded and r0=0. Arbitrary external target
restoration can cost its charged input height, but is not fed back into a
recursive native conic without the sparse/reset operation of section 2.

Actual ideal valuations and (3) give
  P_max<=C_X*N*(H_max+W)^2,                                 (11)
for an absolute C_X. Enumerating integers/primes through that NUMERICAL
cutoff is polynomial precisely because (10) is an original-input polynomial.
This is not logarithmic-time prime enumeration.

## 6. Exact batch, payload and coordinate counts

Let B_d be the number of batches and M_d the sum of r+m+k at depth d.
Then B_d<=6^d. The six child payloads sum to
  r'+s+s+3t <=3r+3m+9k+3P_i+2D_(i-1).
Writing A=max D_i and K=3P_max+2A therefore gives
  M_(d+1)<=9M_d+K*6^d,
  M_d<=9^d*M_0+K*(9^d-6^d)/3.                              (12)
In particular
  sum_(d=0)^h M_d=O(9^h*(M_0+P_max+A+1)).                  (13)
There are O(6^h) constructed aggregate U presentations. These are
N^log_2(6) and N^log_2(9) bounds, with the polynomial (11) charged. There
is no P raised to an extra exponent at each recursive level. All conic
requests, support factorizations, target resets and auxiliary witness
fields are included in these polynomial payloads.
Batching means sharing one computed presentation, not treating a growing
batch as a unit-cost or parallel oracle. If the local linear algebra and
arithmetic cost a fixed polynomial of a batch's payload and bit bound,
summing that polynomial over (12)--(13) is still one polynomial of the
aggregate bounds. Its exponent is not recursively reapplied to payloads.

A stored aggregate coordinate routine traverses only its TWO tagged U
children. It does not rerun the C/E jobs which originally built the stored
norm lifts. Thus one query visits at most 2N-1 coordinate nodes. One kernel
query per aggregate U gives the crude total O(12^h), still polynomial.
Subrequest views add the one aggregate call and binary solves of section 1,
not a further recursive branch.

For bit sizes, all stored scalars and lifts are polynomial-sized by
(10)--(13). Forward/inverse view normalization adds a fixed polynomial to
the common-denominator metric
  L(x)=log m(x)+log max(1,max_sigma |sigma(x)|).
If x' is the query times stored lift products and Nx'=sigma^2, then
  (m*sigma)^2=N(m*x') integral implies m*sigma integral.
Norm doubles L; the trace-identity correction uses this SAME denominator.
Therefore L_child<=2L_parent+P_global for a polynomial determined by the
stored data, and after h levels L<=N*(L_input+P_global). The checked
three-branch square-root routine on the supplied quadratic tower has at
most 3^h<=N^2 calls and the same polynomial-size argument. There are no
new conic calls in either coordinates or square roots.

Every expanded factorization query is a cleared numerator/denominator norm
in degree <=2N. Its bit size is polynomial in the current expanded data,
which are polynomial in (10)--(13) and the fixed backend polynomials. This
also charges a rational leaf's old witness before its shortening step.
Polynomially many auxiliary maximal-order
computations, embeddings, exact-Gram LLL calls, HNF operations and temporary
dense products are therefore charged polynomial work, not free oracles.
The total stored coordinate data and total factorization-query bit mass
are polynomial as well.

## 7. Prerequisites, finite error clock, and disposition

The native maximal-order backend is separately source-checked in
`2026-11-13-maximal-order-source-check.md`: Buchmann--Lenstra 1994 gives a
uniform deterministic polynomial-bit maximal order from a known order and
the radical of its order discriminant. The radical includes primes with
EVEN discriminant valuations. This replaces the report's unsourced
"standard p-radical procedure" sentence.

The separately proved witness lemma (7), fully read in the stable 240-line
`2026-11-13-native-tower-witness-shortening.md`, supplies the absolute
constant 64, including n=1. Its discriminant construction is the explicit order
  O_K + D_d^-1*sqrt(d),
  D_d=product P^floor(v_P(d)/2), J_d=(d)*D_d^-2,
  abs(disc order)=4^n*abs(disc K)^2*N(J_d).
Thus its log discriminant is linear in the extensive height of d, rather
than degree times that height. Apply the admitted maximal-order algorithm,
the ordinary residual reset, and the weighted reset to the already known
norm witness; take the square root of its norm quotient in ORIGINAL K.
No U, C or E request is made over this auxiliary quadratic field. Merely
stating that auxiliary preparation is polynomial would not prove (7).

Using that admitted witness lemma and the source-checked fixed-rank wrappers,
the batch theorem is a polynomial classical reduction to INTEGER FACTORING
under the full relevant-Hecke ERH used in the split-prime theorem. All
recursive dependencies, expanded bits, target views and stored coordinates
are paid above. No relative-conic oracle remains in this conditional theorem.

Assign the polynomially bounded randomized tasks failure probabilities
eta/Q, use their finite clocks, verify exact returned identities, and ABORT
on timeout or a failed certificate. Capped repeated blocks pay any admitted
expected-polynomial finite-field routine. Deterministic prescribed LLL
precision is not a randomness source. The overall finite clock is polynomial
in N, original expanded input, and log(1/eta) OUTSIDE the explicitly charged
integer-factorization calls; their count and total query bit mass are
polynomial. No polynomial classical integer-factoring algorithm is assumed
to have been proved. The ERH hypothesis is essential to this
proof; it is not silently weakened to quadratic-only GRH.

Admitted by THIS audit: the one-tag/broadcast construction with the stated
repairs; exact six-child dependency DAG; affine height propagation from
(7); aggregate polynomial counts and coordinate/bit composition. No general
lower bound, novelty, GRH-free algorithm or quantum advantage follows.
