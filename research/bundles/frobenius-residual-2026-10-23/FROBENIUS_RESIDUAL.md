# The Second Digit Removes The Rank-One Frobenius Bottleneck

2026-10-23. Constructive deductions with exact arithmetic controls.
Independent mathematical and novelty review PENDING. No geometric source,
quantum receiver, cryptanalytic instance or speedup was executed.

## Research Decision

The previous source-pullback test left ell+1 Lagrangian extensions of a
rank-one image. That count ignored information already present in the
recovered source endomorphism. Its action modulo ell squared leaves exactly
TWO compatible kernels in the split case, and NONE in the nonsplit case.
Two ordinary calls to the SAME proposed source select the correct kernel.

The remaining rank-zero case is not evidence that a new nonabelian quantum
receiver is needed: a public centralizer embedding reduces it to an existing
GL2 or SL2 Borel HSP. Thus the entire subfamily with an actual known
skew-Frobenius map is either classically recoverable relative to the original
source, or reducible to published quantum machinery. Do not build a special
Rees receiver for this subfamily. A new efficient NATURAL source could still
be valuable; this deduction does not establish or falsify such a source.

## 1. Exact Input And Access

Keep the original polarized ell-isogeny phi:A=E^2 -> B and its weak evaluator.
The latter returns a common unknown unit multiple of the images of a full
ordered auxiliary basis, with the SAME phi at every level. Require ell odd,
p>3 prime, ell != p, known full source End(A), paid order actions and a paid
common field with compatible auxiliary extensions. The source-pullback
bundle supplies the bounded CRT step, with declared target-map norm bounds.

This pass additionally requires an ACTUAL known target endomorphism gamma:

    gamma^dagger = -gamma,       gamma^2 = -p I.

For an appropriately descended target over F_p this can be p-Frobenius.
A generic model over F_(p^2) has no automatic such endomorphism: Frobenius
to a different conjugate variety is not an endomorphism. An isomorphism to
that conjugate must be constructed and its cocycle checked. A self-adjoint
twist squaring to +p is outside the theorem. Scalar p^2-Frobenius is not a
substitute. No such map was extracted from an indecomposable geometric input.

Using actual gamma and legal weak packets, reconstruct exactly in the known
source order

    alpha = phi^dagger gamma phi,
    alpha^dagger = -alpha,       alpha^2 = -p ell^2 I.

The callback formula is ell W_r^(-1) gamma_r W_r, so the common scalar
cancels. The hidden phi, End(B), a point basis of A[ell], and K are NOT
inputs to this classical extraction. The finite controls use phi only
inside source callbacks and correctness comparisons.

For selection and the Borel reduction use ONLY the already proposed source

    f(M) = f(N) iff MK = NK,       M,N in Sp_4(F_ell).

Every call retains its entire geometric implementation cost. A finite
opaque-label fixture checks the reduction but does not implement f from B.
Classical selection needs ordinary evaluations; the imported Borel receiver
needs coherent reversible evaluations. If the source is unavailable, those
parts remain conditional. They do not become free new oracles.

## 2. The Integral Lattice Condition

Let Lambda=T_ell(A), K=ker(phi) modulo ell, and choose any lift Ktilde.
The transported target lattice is Lambda_K=Lambda+Ktilde/ell. Integrality
of alpha/ell on that lattice is equivalent to

    alpha Lambda subset ell Lambda + Ktilde,
    alpha Ktilde subset ell^2 Lambda + ell Ktilde.

In any integral basis beginning with K, for alpha=[[A,B],[C,D]], this says
A,D vanish mod ell and C vanishes mod ell^2. This is the independently
implemented old kernel-output criterion, not a newly weakened test.
An independent quaternion Hom-module check is

    J_K^(-1) Left(alpha) J_K / ell is integral.

Both methods agree on the tested rank-one completions. Compatibility with
ONE map is not compatibility with the entire modeled input.

## 3. Rank One: A Well-Defined Quotient Operator

Put U=im(alpha mod ell), W=ker(alpha mod ell). Assume dim U=1. Since alpha
is skew-adjoint, W=U-perp; since alpha^2 vanishes modulo ell, U subset W.
The quotient W/U is a nondegenerate two-dimensional symplectic space.
Define

    beta([v]) = [alpha vtilde / ell mod ell]  on W/U.

There are three lift issues, all necessary:

1. For v in W the numerator is divisible by ell. Changing vtilde by ell z
   changes the result by alpha z mod ell, which belongs to U.
2. For u=alpha z mod ell, use alpha z as its lift. Its divided image is
   alpha^2 z/ell = -p ell z, zero modulo ell. Thus the map kills U.
3. The image belongs to W because alpha(alpha vtilde/ell)=-p ell vtilde.

Computing beta twice gives beta^2=-p I modulo U. Dividing the skew pairing
identity by ell shows beta remains skew-adjoint for the quotient form.
In dimension two this implies trace(beta)=0. Its characteristic polynomial
is X^2+p, separable because ell is odd and ell != p.

Every compatible kernel contains U and lies in W. It corresponds to a
line K/U. The prime-square lattice condition is EXACTLY invariance of this
line under beta: alpha Ktilde/ell modulo ell must lie in K. Hence:

- If -p is a nonsquare mod ell, there is no eigenline and no compatible K.
  A genuine original input cannot have rank one in this case.
- If -p is a square mod ell, the two distinct eigenlines give exactly two
  compatible K. They are automatically Lagrangian because U is the radical
  of W and each added quotient subspace is one-dimensional.

All computation is fixed-dimensional linear algebra plus a square root in
F_ell. The root implementation has a declared random-draw cap and an explicit
abort, with a probability bound conditional on independent uniform draws.
No loop enumerates ell or factors ell-1. The prime-square representation is
a lift of the PUBLIC source algebra chart, not a geometric ell-torsion basis.

### Selecting The Correct Candidate

For distinct candidate Lagrangians K0,K1 choose v in K0 but not K1. The
transvection T_v=I+v v^T J is symplectic and stabilizes a Lagrangian R iff
v lies in R. Indeed, if it stabilizes R and v is outside R, then B(v,R)=0,
so v lies in R-perp=R, a contradiction. Therefore

    f(T_v)=f(I) iff K=K0.

This uses two ORIGINAL source calls. It is not two torsion point evaluations.
The implementation never certifies the global f promise: even a constant
invalid callback can mislead selection. That limitation is tested explicitly.

Rank two was already classical: im(alpha mod ell)=K. The new rank-one
deduction closes the gap left by the image/word test for this subfamily.

## 4. Rank Zero: An Existing Borel Problem

Now alpha=ell beta in the integral source order. The action of beta modulo
ell is known, skew-adjoint, and satisfies beta^2=d I with d=-p !=0. The
lattice condition reduces exactly to beta K subset K.

### Split Case

Let d=s^2. The eigenspaces V+,V- both have dimension two and are Lagrangian;
the alternating pairing identifies V- with the dual of V+. The stable
Lagrangians are

    V+, V-, and X + Ann(X) for X in P(V+).

There are ell+3. In dual eigenbases the public symplectic embedding is

    GL_2(F_ell) -> Sp_4(F_ell),   A |-> diag(A,A^(-T)).

First test the two exceptional planes V+,V- using basis transvections.
An identity label and at most four transvection labels suffice. If neither
is the hidden K, restricting f through this embedding hides EXACTLY the
Borel stabilizer of the unknown projective line X. The implemented inverse
output map is X -> X+Ann(X); equivariance and the full small-field collision
partition are checked, not merely group membership.

### Nonsplit Case: Constructive SL2 Embedding

No extension-field factorization or search over ell points is required.
The symmetric nondegenerate quadratic form Q(x)=B(x,beta x) in four
variables has a nonzero isotropic vector u over the odd finite field.
Congruence diagonalization followed by the already implemented bounded
four-variable quadratic solver finds one in randomized polynomial bit time.
Solve the two linear equations B(u,v0)=1, B(u,beta v0)=0. Set

    v = v0 + Q(v0)/(2d) beta u.

Then Q(v)=0. In the public basis (u,v,beta u,beta v) the two matrices are

    B = diag(J2,-d J2),       beta = [[0,d I2],[I2,0]].

The basis is nonsingular because its displayed alternating form is.
Consequently A |-> diag(A,A) embeds SL_2(F_ell) in Sp_4 and centralizes beta.

To see completeness of the parameterization, write a nonzero w as
x u+y v+z beta u+t beta v. A beta-stable plane is span(w,beta w), since d
is nonsquare. Its isotropy is Q(w)=2d(xt-yz)=0. Thus (x,y) and (z,t) are
proportional, so it is uniquely

    K_[a:b] = span(a u+b v, beta(a u+b v)),  [a:b] in P^1(F_ell).

There are ell+1. The embedding acts by its ordinary projective-line action.
Restricting the ORIGINAL f therefore gives precisely an SL2 Borel HSP.
Recovering its line recovers K with the displayed formula.

### Published Quantum Dependency

Denney, Moore and Russell, [arXiv:0809.2445](https://arxiv.org/abs/0809.2445),
published in Quantum Information and Computation 10 (2010), pp. 282-291,
Sections 5-6, give the efficient SL2/PSL2/PGL2 Borel receiver. The split
GL2 case also follows from the more general parabolic theorem of Decker,
Ivanyos, Kulkarni, Qiao and Santha,
[arXiv:1406.6511](https://arxiv.org/abs/1406.6511), Theorem 1.
These are IMPORTS, not new receiver claims and not executed implementations.
The classical public embeddings above have polynomial bit cost; the quantum
cost still includes every coherent invocation of the original f.

## 5. Attempts To Falsify The Argument

- Complete ell=5 censuses yield 8,2,1 compatible planes for split ranks
  0,1,2, and 6 for nonsplit rank zero. Counts match the OLD prime-square
  criterion. The old ell=11 rank-one example has 12 image-line completions,
  but only two pass the independent quaternion Hom-module criterion.
- A TRUE integral alpha with alpha^dagger=-alpha and alpha^2=-175 I in
  characteristic 7 at ell=5 has rank one and no compatible plane. Thus exact
  source identities alone do NOT certify an underlying weak-isogeny input.
- Every GL2(F5) and SL2(F5) element, for every projective line, is checked
  against the original opaque-label collision partition. The split singleton
  orbits are checked separately; omitting them would invalidate the reduction.
- Compatible prime-square chart changes leave rank-one candidates unchanged.
  Public symplectic conjugation leaves both rank-zero families equivariant.
- 127-bit controls run without field-size enumeration. These are local
  arithmetic matrices, NOT certified global geometric inputs.
- Positive-square self-adjoint maps, wrong exact squares, invalid group
  elements, duplicate candidates and exhausted random budgets are rejected.
- The receiver/geometry flags remain false. Capped uniform-random bounds
  are theoretical guarantees, not empirical estimates from seeded replay.

The remaining attack surface is substantial: source existence, actual target
map availability, consistent weak access, costs of model arithmetic, and
independent proof review. These finite controls do not settle those issues.
No classical hardness conclusion follows from ell+1 remaining candidates.
Other same-input attacks could solve the rank-zero problem classically.

## 6. Revised Next Work

Do not spend another pass tuning finite matrices or creating a new Borel
receiver. The strongest question is whether a real, indecomposable target
provides gamma and the existing marked source with the promised costs.
The full generic surface problem WITHOUT gamma is not resolved here.

There is also a possible alternate CLASSICAL verification route for the two
rank-one candidates: use the existing kernel-to-module construction, the
imported effective module-to-geometry converter, and common marked
isomorphism tests against the original B. This would avoid the stabilized
Sp4 label source but requires all converter/reference/field/height promises
from EFFECTIVE_OUTPUT_AUDIT.md (in particular its conservative ell<=p^C
scope) and an implemented candidate-map comparison. It is not executed or
counted as a separate result here. Do not use unmarked isomorphism alone.

Before any claim of a new natural algorithm, compare this Borel route with
existing Frobenius-oriented isogeny methods and try to obtain the same output
classically from the full weak input. Any actual geometry backend should be
integrated only after migration and should retain all unresolved proof flags.
