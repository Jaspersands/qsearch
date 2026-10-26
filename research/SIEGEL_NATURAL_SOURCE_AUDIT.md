# Can The Siegel Reduction Reach A Useful Input Problem?

2026-10-23. Source/access audit following SYMPLECTIC_FIELD_CHART_REDUCTION.md.
No new cryptanalytic result or impossibility theorem. Two tempting source
constructions fail different tests: one already has an abelian algorithm;
the other need not supply the exact promised oracle at all.

Later same-day progress: SIEGEL_MARKED_SOURCE_RIGIDITY.md gives sufficient
auxiliary-torsion bounds that repair label injectivity, including unknown
invertible scalars, for JOINTLY marked POLARIZED quotients. It also gives
exact counterexamples to weaker thresholds, separate per-level
canonicalization and dropping the polarization. This is a geometric
separation lemma, not a constructed efficient action/evaluator/canonicalizer.

Further source progress: SIEGEL_ELEMENTARY_REPOLARIZATION.md constructs
degree-one elementary action lifts on E^g,g>=2 and derives the changed
principal polarization. Its accessible-torsion action is computable, but
conversion to an efficient polarized model and canonical labels remains
unproved. The2026 PPAV-framework paper identified there needs full review.

## 1. Accessible Torsion Evaluation Already Has An Abelian Baseline

Suppose the input provides an efficiently usable basis P_1,...,P_(2n) of
the relevant prime-order torsion A[ell], canonical point encodings, efficient
group operations, and coherent evaluation of a homomorphism phi on it.
Here ell is the torsion prime, not the characteristic of the base field.
Define, using only that input,

    h(x_1,...,x_(2n)) = phi(sum_i x_i P_i),  x_i in F_ell.

Because phi is a homomorphism, h(x)=h(y) exactly when x-y belongs to its
kernel K. This is an ordinary ABELIAN HSP on F_ell^(2n), with no need to
know coordinates on the image group. Uniform superposition, evaluation,
measurement and additive Fourier sampling recover a basis of K in
polynomial time. This is a direct application of the existing abelian
framework, not a new algorithm; see
[Kitaev](https://arxiv.org/abs/quant-ph/9511026).

If image-group coordinates are ALSO given efficiently, simply evaluate the
2n basis images and compute the kernel of their matrix by classical linear
algebra. Do not silently assume those coordinates are free when comparing
against a discrete-log representation. For F_(ell^a)-linear input, expand
in an explicit F_ell basis and use the same argument.

The premise includes the cost of finding/representing the torsion basis
and evaluating phi there. If those points require a field extension of
degree D, ordinary dense field representations cost Omega(D) base-field
coefficients. A polynomial bound in log(ell) cannot ignore a superpolynomial
D. A weak evaluator efficient in its POINT INPUT LENGTH does not make such
points succinct or provide their basis. A common nonzero scalar multiplying
all torsion images preserves the kernel; an unknown scalar that can vanish
on the target torsion does not satisfy this argument's promise.

Decision: do not pitch a new Siegel algorithm for a setting that supplies
this stronger accessible-kernel oracle. Any claim of novelty must beat the
abelian quantum baseline, not merely classical exhaustive kernel search.
This does NOT rule out weaker isogeny representations with inaccessible
large-prime torsion.

## 2. Unmarked Quotient Codomains Need Not Label Kernels Injectively

The proposed hiding function

    f(g) = isomorphism class of A/(gK)

has the right level sets only if the chosen quotient labels distinguish
every relevant kernel. That is an additional theorem, not a consequence
of being able to form a quotient or canonicalize its codomain.

Here is a concrete counterexample already in dimension two and odd torsion
characteristic, within the intended Siegel scope. Work over an algebraic
closure of characteristic 11 and take

    E: y^2 = x^3-x,
    alpha(x,y)=(-x,i*y),       i^2=-1.

Substitution verifies that alpha is an automorphism, and alpha^2=[-1].
On E[3] its square is -I. No one-dimensional F3-subspace C of E[3] is
alpha-invariant: invariance would give a scalar eigenvalue lambda with
lambda^2=-1, impossible in F3. Automorphisms of elliptic curves fixing the
origin preserve their canonical principal polarization.

Let A=E x E with product polarization and choose any lines C,D in E[3].
Then K=C x D is a maximal isotropic two-space in A[3]. The product
automorphism beta=alpha x identity preserves the polarization, induces a
symplectic matrix on A[3], and satisfies beta(K)!=K. Nevertheless it descends
to an isomorphism of the polarized quotients

    A/K -> A/beta(K).

Indeed beta maps exactly the first kernel to the second, so the quotient
universal property gives an isomorphism. Pull back the induced quotient
polarizations along the quotient maps to check that it is polarized.
Thus f(I)=f(beta), although beta is NOT in P_K. Canonicalization of the
unmarked quotient cannot fix this collision: the quotients really are
isomorphic. This is not merely two different encodings of one object.

A torsion-coordinate witness is the symplectic matrix sending e1->f1,
f1->-e1 and fixing e2,f2. It moves K=<e1,e2>. The focused test checks this
linear witness; it does NOT numerically construct isogenies or their moduli.
The geometric conclusion above is a deduction from the explicit
automorphism, not from a small matrix simulation.

Decision: do not use unmarked quotient-isomorphism classes as exact coset
labels without an injectivity proof, suitable markings, or a newly proved
algorithm that tolerates their extra collisions. This one example refutes
the universal shortcut. It does not show every generic or rigidified input
has collisions, nor that all isogeny applications are impossible.

## 3. The Known Elliptic Bridge Identifies The Real Missing Work

[Chen--Imran--Ivanyos--Kutas--Leroux--Petit](https://arxiv.org/html/2305.19897)
treat weak isogeny representations, an action on isogenies, and its Borel
stabilizers. Section 2.4 charges point representation length; Sections
4.1--4.3 separate action evaluation from stabilizer recovery and use
quaternion lifting to construct the former. Those distinctions matter:
knowing an abstract action is not an implementation of its hiding oracle.
Their elliptic result is prior art, not a new application of our n>=2
construction. No higher-dimensional extension is imported here.

A higher-dimensional attempt must supply ALL of the following without
assuming the unknown kernel or target endomorphism ring:

1. Explicit public input and target output, with an accessible algebraic
   presentation of the acting Sp group. Specify field/ring and polarization.
2. A uniform polynomial-time transformation for each matrix actually queried
   by the reduction, including conjugation by random charts. Producing a
   representation of a transformed isogeny is itself an algorithmic task.
3. Deterministic, canonical labels or a fully analysed quantum source whose
   equality/inner-product contract is precisely the one the receiver needs.
   Random representations of the same isogeny need not have equal strings;
   identical unmarked codomains need not have identical kernels.
4. A proved promise that the hidden subgroup is the FULL Lagrangian
   stabilizer. An unknown subgroup inside it, a double-coset relation or a
   collision-tolerant moduli invariant is not interchangeable with that promise.
5. Paid point fields, torsion generation, endomorphism lifting, quotient
   evaluation, markings, precision and coherent workspace. Account for
   degree and dimension, not only the length of a matrix modulo ell.
6. A comparison with direct abelian kernel recovery whenever the supplied
   access permits it, and with already established isogeny algorithms in
   the exact same public-information model.

## 4. Revised Priority

Do not implement a synthetic isogeny-labelled benchmark or a new receiver
backend merely to make the abstract theorem appear applied. The first
decisive target is a source lemma in a CONCRETE higher-dimensional weak
representation model: construct exactly the required marked quotient label
from accessible public data, prove its equality fibers, and bound its cost.
Try first to falsify it using automorphisms and an abelian-kernel baseline.

If only the strong accessible-torsion model is available, classify the
application as already covered by abelian HSP. If only unmarked codomain
labels are available, keep the current reduction blocked on its source
contract. If no tractable marked evaluator emerges, deprioritize this
application branch; retain the field-only theorem as a scoped research
result pending review, not as evidence of a Shor-level algorithm.

This is a narrowed research question, not a request for more framework or
an assertion that the source construction is impossible. The full group
query lower bound applies to opaque labels only and cannot establish the
hardness of any particular isogeny encoding.
