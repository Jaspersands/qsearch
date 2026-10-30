# A Native Non-Bass Family And A Stronger Output Falsifier

2026-10-26. Proposed reduction and exact supplied-order controls. No native
isogeny recovery, geometric label, quantum execution, or novelty claim.

## Result And Research Decision

The preceding local-order audit isolated large-prime non-Bass components,
but did not realize that regime from a standard native input. This note
supplies a charged realization from prime-degree IsERP. It also gives a
stronger false-positive control than an index-correct lattice with fractional
norms: the WRONG output can itself be a genuine maximal order with every
ordinary algebraic certificate correct.

Consequently native division cannot be replaced by tests of discriminant,
norms, involution, ring closure, subgroup size, or a convenient ambient order.
Keep the actual curve and evaluators through output verification. Neither
the realization nor the controls prove that the resulting native inputs are
hard, that our additive source works, or that its mechanism is new.

## 1. Exact Native Input And Charged Adjoint Construction

Start with supersingular E0,E in characteristic p>3 and an odd prime q!=p.
Supply a separable q-isogeny phi:E0->E through an efficient evaluator, not its
kernel or the target endomorphism ring. Supply a full evaluable source order
O0=End(E0), with basis 1,a2,a3,a4. Curves, compatible common fields, degree
bounds, evaluator descriptions and costs are paid. Adapting a source-order
basis to include its primitive identity is integer lattice arithmetic.

This is the standard IsERP setting with a known source order, not a new
opaque-label search problem. Native map encodings are part of the input.
For relevance to large-prime speedups their description and evaluation cost
must not already scale linearly in q. A dense degree-q rational map need not
be a succinct hard input. Known chains or other encodings may reveal enough
information for a separate classical attack and must remain available to it.

Do NOT assume a dual evaluator appears for free. If phi already has an
efficient represented-morphism encoding admitting adjoints, use it. Otherwise
there is the following conditional construction using the same imported PPAV
machinery as the proposed source:

1. Use the existing genus-one conversion and scalar-Frobenius normalization
   on both endpoints. Fix the base field and its embeddings.
2. Choose powersmooth M>4q with gcd(M,pq)=1. The prime factors of M are
   polynomially bounded in log(q)+log(p). Work separately at each prime;
   do not build an enormous joint torsion field.
3. Generate CRT generators of E0[M] and evaluate the supplied phi on them.
   Its degree is coprime to M, so the images generate E[M].
4. Invoke the published polarized-isogeny interpolation routine with N=q,
   N'=M. Its uniqueness threshold holds. This gives the SAME phi in the
   represented model; it does not discover the kernel or target order.
5. Apply the represented adjoint routine to obtain phi^dagger. All these
   preprocessing costs and outputs are available to the classical comparator.

This step imports [2026/1142](https://eprint.iacr.org/2026/1142), Theorem 7.1
and A21, on actual modeled endpoints and actual evaluation data. It was not
executed here. The retained PDF was reread at pages 10-15, 24, 34 and 36-40.
A7 really is geometric-isomorphism canonicalization, distinct from A6;
Lemma 6.22 implements it. Thus the proposed objection that A7 merely
normalizes one encoding is not valid. None of this checks the whole new
source composition or gives an unpolarized isomorphism oracle.

## 2. The Suborder Is Constructed By Known Native Maps

Define the proof-coordinate map and actual native maps

    theta(a) = phi*a*phi^dagger/q,
    b1 = 1,             bj = phi*aj*phi^dagger, j=2,3,4,
    R = <b1,b2,b3,b4>_Z = Z + q*theta(O0).

theta is a rational algebra isomorphism because phi^dagger*phi=[q]. The
algorithm never evaluates theta(aj) as an integral map. It computes bj
without division. Therefore R really is contained in O=End(E).

To check ring closure explicitly, write ai*aj=c1+sum(k>=2) ck*ak. Then

    bi*bj = q^2*c1 + q*sum(k>=2) ck*bk.

Similarly, the involution is transported from O0. Trace(bj)=q*Trace(aj)
and Norm(bj)=q^2*Norm(aj). Thus its multiplication, involution and trace
tables, and its full Gram matrix, are computable without the target order.
All of this metadata is independent of the hidden kernel line of phi.

Conjugation preserves reduced trace and norm. In theta(O0) coordinates the
basis change for R is diag(1,q,q,q), of determinant q^3. Hence

    disc(R)=p^2*q^6,           [O:R]=q^3.

The native basis degree bound is max(1,q^2*max_j deg(aj)), with polynomial
bit length in the charged original data. This is precisely a full-rank
input for the proposed additive construction, not maximal-order advice.

## 3. The Native Target Is A Neighbor, Not The Abstract Center

At a prime other than q, phi gives an isomorphism of Tate lattices (and no
change at p for this separable prime-to-p isogeny). At q identify the source
lattice T=T_q(E0) with Z_q^2. Pull back the target lattice through phi:

    L=phi^-1 T_q(E),        T subset L,        [L:T]=q.

L/T is the kernel line in q^-1 T/T. The pulled-back target maximal order
is End(L), a neighbor of M=End(T). They cannot coincide: lattices stable
under all M_2(Z_q) are homothetic to T, whose relative index is a square
power q^(2r), not q.

The input order is locally Z_q+q*M, independent of the line. It has q+2
maximal overorders: center M and q+1 neighbors. Every cyclic subgroup of
E0[q] gives an actual quotient isogeny, so these neighboring completions
are not artifacts of an invented linear oracle. The construction does not
give a compact hard encoding for every such isogeny; that is an additional
input-generation/representation question, not a free promise.

This proves that the local family from the previous pass is compatible with
native isogeny inputs. It does not make arbitrary native instances hard.
Small q and cheap extra native units can still dequantize them. In particular
our characteristic-11 controls are not unit-saturated hard benchmarks.

## 4. Wrong Maximal Order That Passes Every Algebraic Gate

In the pulled-back coordinates let O1=theta^-1 End(E). Both O0 and O1 are
maximal, both contain R0=Z+q*O0, and both have index q^3 over R0. But O0!=O1.
Taking d=q^3 gives two different candidate subgroups of R0/dR0:

    H_true = d*O1/dR0,          H_wrong = d*O0/dR0.

Both have size d. Both reconstruct a rank-four unital involution-stable
ring with discriminant p^2, integral traces, positive integral norms, and
maximality. Any verifier using only these conditions accepts both.

Yet at least one of theta(a2),theta(a3),theta(a4) is nonintegral on the
native target curve. Otherwise theta(O0) would be contained in End(E),
forcing equality of maximal orders, contrary to the neighboring lattices.
The candidate maps are bj/q. Their reduced norms are integral; that does
NOT make them actual endomorphisms. Actual native division of bj by q
must reject at least one. This is a stronger output falsifier than a fake
candidate which can already be rejected for fractional degree.

This is not a bug in candidate_lattice: that function expressly produces
an index-checked CANDIDATE. Do not "repair" it by choosing the source order
as the answer. Require the already-specified native certification downstream.

## 5. The Same Distinction Is Essential Inside The Source Proof

Let r_i=(1,q*a2,q*a3,q*a4) be the pulled-back basis of R0, so theta(r_i)=bi.
Choose delta in O1 but not O0, and form a legitimate residue query

    u = coordinates_R0(d*delta) mod d,
    gamma = sum_i u_i*ri/d.

Then gamma-delta belongs to R0, so theta(gamma) is native-integral while
gamma is nonintegral in the abstract center O0. The source shear w_gamma
is an integral framed polarized isomorphism in the TRUE order O1; it looks
fractional in O0 coordinates. Conversely choose delta in O0 but not O1:
the same rational congruence holds, but it is not a native isomorphism.

The controls test both directions using exactly the previous construction.
The source matrix Z itself is computed entirely in the SUBORDER table and
has integral coefficients there. Its quadratic identity remains valid.
Changing to either ambient coordinate system gives the same rational tensor.
No unknown order is consulted in constructing Z. Unknown-order integrality
enters only the theorem's isomorphism classification, not its computation.

Thus replacing End(E) by a convenient maximal order can cause both false
positives and false negatives. Pure matrix congruence over the rational
algebra cannot decide a geometric collision. Tests with supplied target
orders are guards against that mistake, not an implementation of the label.

## 6. Potential Contribution And Strongest Objections

Conditional on the ENTIRE additive source theorem, this native input gives
abelian HSP on (Z/q^3)^4 and recovery of End(E), with polynomial bit cost
but dimension-128 geometric operations. It supplies an explicit target
regime for that theorem, not a new quantum receiver.

Prime-degree IsERP already has quantum algorithms: see
[Chen et al., 2305.19897](https://arxiv.org/abs/2305.19897). Full-suborder
quantum algorithms also predate this work. Any possible contribution must
be a proved improvement in assumptions/source construction, not a claim
of first solving IsERP. Search results alone do not establish novelty.

The matched classical competitor retains phi, its representation, the full
source order, all preprocessing, native division, and geometric outputs.
The previous Bass/small-prime baselines still apply. A low-degree or
representation-specific recovery attack may do better. No native classical
lower bound follows from equal arithmetic metadata or a Boolean interface.

Open: full finite-frame/field/native-model composition, independent review,
useful classical leakage at nonzero queries, and novelty. No source backend
or source circuit has run. The current tests cannot settle those questions.

Next decisive task: an end-to-end audit of the exact source/certification
contract on this native IsERP reduction, including the paid conversion of
the evaluator and preservation of common base embeddings. Do not substitute
more successful arithmetic metadata or known-order tests for that work.
