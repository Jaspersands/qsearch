# Rees Application Triage: Quadratic Forms And Rank-One Probes

2026-10-23. A source-reduction audit, not a proposed benchmark, new oracle
separation, discovery admission or global impossibility result. Independent
review of the deductions below remains appropriate.

## Question And Decision

Can the proposed fixed-class nilpotent HSP algorithm recover an unknown
quadratic form by restricting its isometry group to a public low-rank
matrix group? This would be a possible application of an actual algorithm,
rather than another change to its parameter bound.

The simplest probe does NOT give the required nilpotent problem. For a
nondegenerate symmetric form in odd characteristic and a nonisotropic
probe vector, it hides exactly an unknown reflection in an affine group.
That particular HSP is equivalent, with one query per simulated query, to
the generalized dihedral HSP. Allowing all scalar multipliers in the
affine probe does not remove this difficulty. Restricting to its abelian
translation subgroup instead removes the hidden information entirely.

For alternating forms the same calculation gives a hidden LINE in an
abelian group, so the apparent easier case needs only the existing abelian
algorithm. Do not transfer that conclusion to symmetric forms.

This does not exclude using larger parts of the isometry group, more of
the original function, or a different non-oracle representation. It stops
one specific attempted application from being called solved by Rees.

## 1. Source Construction And What It Does Not Supply

Let F=F_q have odd characteristic, and let the unknown symmetric matrix A
be nonsingular of dimension d>=2. Consider the established hidden-polynomial
input model f(x)=pi(Q(x)), Q(x)=x^T A x, with pi injective on attained
values. The original access is coherent function evaluation, not the
coefficients of A. Classical field arithmetic and label widths are charged.

The hidden-polynomial framework is prior art; see
[Childs--Schulman--Vazirani](https://users.cms.caltech.edu/~schulman/Papers/quantum-nonlinear.pdf).
Also distinguish the solvable special bivariate families in
[Decker--Hoyer--Ivanyos--Santha](https://arxiv.org/abs/1305.1543)
from arbitrary hidden-polynomial promises. No new problem or novelty claim
is introduced here. This model by itself is not a natural computational
application or a Shor-level result.

Use the public quadratic unisolvent set

    T={e_i} union {e_i+e_j : i<j}.

There are d(d+1)/2 points. Since 2 is invertible, equality of two homogeneous
quadratic forms on T implies equality of their diagonal and cross
coefficients. Consequently the tuple

    F(g)=(f(g^(-1)*t))_(t in T),   g in GL_d(F),

has F(g)=F(h) exactly when g^(-1)h belongs to O(A). It is a standard
LEFT-coset hiding function for the full isometry group, built with
d(d+1)/2 original queries and clean reversible matrix evaluation.
The inverse in this definition fixes the coset orientation; omitting it
gives the opposite convention. This construction does not implement an
HSP solver for O(A).

If numerical Q-values or A itself are supplied instead of opaque labels,
ordinary polarization recovers A from those same evaluations classically.
Do not count a numerical form fixture as evidence for an oracle speedup.

## 2. The Exact Symmetric Rank-One Intersection

Choose a public nonisotropic vector v and a public basis with v=e_1.
Nonisotropy is testable using f(v)!=f(0); this does not reveal Q(v).
For the following calculation write the UNKNOWN form as

    A = [[alpha, c^T], [c, D]],   alpha!=0.

The symbols alpha,c,D are proof parameters, not algorithmic advice.
Consider all public rank-one updates along v,

    G_v={g(a,b)=[[a,b^T],[0,I]] : a in F*, b in F^(d-1)}.
    g(a,b)g(a',b')=g(aa', b+a*b').

The top-left block of g^T A g=A gives a^2=1. Its off-diagonal block gives

    alpha*a*b^T + a*c^T = c^T.

For a=1 this forces b=0; for a=-1 it forces b=-2c/alpha. The remaining
block equation then holds automatically. Thus

    O(A) intersect G_v = {I, g(-1,2s)},    s=-c/alpha.       (1)

This is the usual reflection fixing v's orthogonal hyperplane. No search
over unknown coefficients was used to build G_v. Conversely, recovering
its hidden s would reveal the polar functional A*v up to scale; recovering
s is precisely the unresolved algorithmic step, not something the proof
parameters provide for free.

## 3. Full Affine Multipliers Do Not Evade The Dihedral Subproblem

Let V=F^(d-1), G=V semidirect F*, and H_s={I,(-1,2s)}. Set
D=V semidirect {+1,-1}, a public subgroup. Restriction of a G hiding oracle
to D is immediately a D hiding oracle for the same H_s.

The reverse oracle construction also costs one query. Given ANY ordinary
hiding function h_D on D for H_s, choose a deterministic representative
u(a) of the pair {a,-a} using the supplied field encoding. Put

    epsilon=a/u(a) in {+1,-1},  y=b/u(a),
    h_G(a,b)=(u(a), h_D(epsilon,y)).                       (2)

Right multiplication by the hidden reflection sends

    (a,b) -> (-a,b+2a*s),
    (epsilon,y) -> (-epsilon,y+2epsilon*s),

and preserves u(a). Conversely, two equal labels in (2) have the same u
and either identical D coordinates or coordinates related by exactly this
reflection. They therefore lie in the same G coset of H_s. No other
collisions are introduced. Field inversion, sign comparison, coordinate
scaling and their clean reversals take polynomial time in d and log q.

This proves equivalence for THESE ordinary HSP oracle promises, not merely
similar-looking coset states. It does not prove a lower bound against all
quantum algorithms. The case V=F_p already contains the usual prime-order
dihedral hidden-reflection problem.

The group D is not nilpotent when V!=0 in odd characteristic: conjugation
by the reflection negates translations, and its commutators span 2V=V.
Thus gamma_2(D)=V and every later lower-central term is also V. No fixed
class input promise for Rees applies. In the translation subgroup alone,
H_s intersects V trivially for EVERY s. Opaque-label abelian HSP on that
restriction cannot recover s. The actual original labels might carry other
structure, but that would require another algorithm and proof.

## 4. Alternating Forms Are A Different Calculation

Let B be nonsingular alternating, with u=B*v. For g=I+v*w^T,

    g^T B g-B = u*w^T-w*u^T.

This vanishes exactly when w is a scalar multiple of u. Since u^T*v=0,
these updates all have a=1 and form a one-dimensional additive subgroup
inside the public translation group {I+v*w^T : w^T*v=0}. Its recovery is
an ordinary abelian HSP. This is a diagnostic contrast, not a new quantum
primitive or a proof that the symmetric case is classically hard.

## 5. Falsifiers And Research Decision

The strongest falsifiers of this triage are an incorrect intersection in
(1), extra/missing coset identifications in (2), or a claimed nilpotency
of D in odd characteristic. Focused exact tests check all rank-one updates
for selected symmetric/alternating forms and both directions of the affine
coset coordinate change. They test identities, not a generated oracle
search campaign, an executed quantum solver, or the global Rees theorem.

The proposed Rees core was reread against its stated central-instrument
formula and the published diagonal solver; this pass found no new flaw,
but adds NO independent certification of that core. The quadratic probe
does not remove its application gap. The HDQI alternatives inspected in
this pass were already covered by HDQI_PREDECESSOR_UNIFORM.md and
HERMITIAN_QUTRIT_PILOT.md; do not reopen them merely from a new abstract.

Do not build an orthogonal-group wrapper around the Rees receiver from
this probe. A next attempt must either exploit original function structure
beyond the restricted HSP, supply a genuinely different useful source,
or achieve independent/formal verification of the existing whole theorem.
No CLI/UI/central registry admission, Git write, hydration or relocation.

Validation:16 new exact identity tests;91 selected tests PASS in0.72s,
including the uniform-BCH, independent source-bank and inverse-trace mask
controls. New-file py_compile passes. No full-repository or quantum
receiver validation was performed; no running job remains from this pass.
