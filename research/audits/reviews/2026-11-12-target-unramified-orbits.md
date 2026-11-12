# Target-prime unramifiedness of the finite orbit algebra

2026-11-12. Focused independent review after reading current `STATE.md`,
`SURFACE_NATIVE_TORSION_MODULE.md`, the arithmetic section of
`SURFACE_NATIVE_COVER_CONSTRUCTION.md`, the full-similitude review, and the
closed-divisor encoding review. No Git, network, API, archive, new code, or
numerical control. The interpreter, if needed, is `/opt/anaconda3/bin/python`.

**Disposition.** The stated genuine frame torsor has a smooth proper
normalized compactification at the target p. The local argument uses
tame inertia killing and purity, with no ramified base extension. Its
compact Jacobian ell-torsion is unramified. Consequently the product of
an unbranched regular fibre with any Galois-stable fixed-rank torsion
subspace is unramified. This pays the ABSTRACT target-prime property of
the reconstructed finite Q-algebra, even when a chosen divisor encoding
has bad reduction at p. Computing a p-maximal order is a separate
algorithmic obligation, assigned elsewhere.

The hypotheses must include extension of the torsor over the ENTIRE
open model U/Z_p. A generic-fibre cover with the same tame horizontal
inertia is insufficient: a ramified constant twist is a counterexample.

## 1. Exact hypotheses and the finite set

Let the smooth native quintic and its cubic Lefschetz pencil lift over
Z_p. Assume its relative branch divisor D in P^1_Z_p is finite etale,
of fixed geometric degree r=220. Thus after an unramified extension it
is a disjoint union of sections, with distinct nodal singular fibres.
Put U=P^1_Z_p minus D. The smooth proper pencil family over U has a
relative Jacobian J_fibre/U. Let ell>53 be prime and put

    n=62,   Gamma=GSp_n(F_ell),   d=|Gamma|,   p>d.

Its genuine full similitude-frame scheme T is a finite etale RIGHT
torsor over U for the CONSTANT group Gamma, of rank d. This follows
from the abelian scheme's ell-torsion, its perfect Weil pairing, and
the primitive-root scheme inside mu_ell, all finite etale when ell is
invertible. In particular this is the actual arithmetic torsor attached
to the family, not an abstract geometric twist.

At each generic geometric branch point, inertia on the fibre torsion
is a nontrivial transvection of order ell. On the full frame torsor this
acts freely in cycles of length ell. Horizontal ramification indices
are therefore ell; there are no additional horizontal branch points.
Let C be the normalization of P^1_Z_p in the generic-fibre algebra of T.
Geometric disconnectedness of T or C is allowed.

Write J_C for the product/descended product of the Jacobians of the
geometric compact components. Let

    E subset J_C[ell](Qbar),    dim_(F_ell) E=R,

be any Galois-stable vector subspace, with R fixed independently of ell.
The safe default is the full natural Gamma-socle already constructed:

    S=N^vee,  W=Hom_Gamma(S,J_C[ell]),
    E=im(S tensor W -> J_C[ell]),
    m=dim W=(r-2)n,   R=nm=(r-2)n^2.                    (1)

For n=62,r=220 this is R=837992. A separately verified Galois-stable
parabolic subspace would give R=62*96=5952 instead. Nothing in this
review proves that filtering or its specialization compatibility; the
unramifiedness argument applies to it once those inputs are proved.

For a rational integral base value a whose reduction lies in U(F_p),
let B_a=T_a be the full fibre torsor and define the finite Galois set

    Z=B_a(Qbar) x E,      |Z|=d ell^R.                   (2)

The associated finite etale Q-algebra is
Q[Z]=Map_Gal(Z,Qbar), of dimension d ell^R. This notation denotes
equivariant functions, not the group algebra of E.

## 2. Local compactification: the missing vertical check

The local structural inputs are the tame Abhyankar lemma for a DVR
extension and Zariski--Nagata purity for a finite normal cover of a
regular scheme. Their hypotheses are checked below; no assertion about
good reduction is imported from a report label.

Work at the closed point of a branch section after strict henselian
completion of the unramified base. Let R_0 be the resulting complete
strictly henselian DVR, with uniformizer p and algebraically closed
residue field. It contains mu_ell because ell is invertible. The
completed target is

    A=R_0[[t]],

with the branch section t=0. The given cover is finite etale over
A[1/t]. In particular it is etale at the generic point of the special
fibre (p): vertical unramifiedness is part of the hypothesis, not a
consequence of the generic horizontal inertia calculation.

Adjoin an ell-th root of the branch parameter:

    B=R_0[[s]],   t=s^ell,

and normalize the pulled-back generic cover. This normalization is
finite: the rings involved are excellent and the generic algebra is
finite and separable. It is etale at every height-one prime of B:

* Away from (s), the cover is the base change of the given finite etale
  cover of A[1/t]. This includes the vertical height-one prime (p).
* At (s), the DVR tame Abhyankar lemma kills the horizontal ramification
  of index ell after adjoining s. Any remaining residue-field extension
  there is separable (its residue characteristic is zero), so the
  normalized cover is unramified at this height-one prime too.

The base B is regular of dimension two. Purity now says the finite
normal cover is etale everywhere: a new branch locus supported only at
the codimension-two point (p,s) is impossible. Since B is strictly
henselian, the normalized cover is a disjoint union of copies of B.

Descend along the Kummer group mu_ell. It permutes these copies and acts
on their base parameter by s -> zeta s. For an orbit of copies, let H
be the stabilizer of one copy, with h=|H|. The invariant ring is

    R_0[[s]]^H = R_0[[s^h]] = R_0[[w]],
    t=w^(ell/h).                                        (3)

These invariants recover the original normal algebra: they have its
generic algebra by Galois descent and are its integral closure over A.
Thus every completed local piece of the original normalization is
R_0[[w]], with t=w^e and e dividing ell. At an actual transvection branch
e=ell; e=1 covers an unramified piece. The same normal form can initially
have a unit multiplying w^e, which is absorbed over the strictly
henselian base because e is invertible.

Equation (3) proves relative smoothness at the boundary. Off the boundary
the cover is etale over the smooth U. Normalization is finite over the
proper P^1_Z_p, hence proper, and its local descriptions are flat and
smooth over the DVR. Smoothness descends from this faithfully flat
unramified/strict henselian verification. Consequently

    C -> Spec Z_p is smooth and proper.                  (4)

The proof uses no ramified extension of Z_p. The numerical hypothesis
p>d is stronger than the local requirement: invertible horizontal
ramification indices, the etale open extension, and disjoint branch
sections are what the argument actually needs. All deck maps extend to
C by uniqueness of normalization.

For clarity, merely examining generic inertia would miss a genuine
failure: P^1 over a ramified quadratic extension of Q_p gives a generic
degree-two constant cover with no horizontal branch at all, but its
normalization over Z_p is not smooth. It does not extend etale over U.
A ramified central twist of a geometric frame cover has the same defect.
Likewise branch collision, as in the double cover with branch points
0,p,1,infinity, invalidates the disjoint-section step.

## 3. Unramified Jacobian torsion and the natural subspace

After an unramified extension splitting the geometric components, (4)
gives a product of smooth proper connected curves. Their relative
Picard varieties of degree zero are abelian schemes. They and their
descent form the abelian scheme denoted J_C over Z_p. No rational
basepoint is required for this existence statement. Multiplication by
ell is finite etale, so

    J_C[ell] is finite etale over Z_p.                   (5)

Equivalently target-p inertia acts trivially on its geometric points.
This includes the cyclotomic components: mu_ell and the component
scheme are unramified at p. No assertion that all components are
Frobenius conjugate is needed.

For the full natural socle, every right Gamma deck map is defined over
Q on the genuine full torsor. Its induced action on J_C[ell] commutes
with absolute Galois. Since S is constant, for every equivariant phi,
sigma composed_with phi is again equivariant. Hence the image E in (1)
is Galois stable. The evaluation map is injective because S is absolutely
simple with endomorphism ring F_ell; only its socle is semisimple, not
the ambient torsion representation. Its rank is the fixed R in (1).

Every Galois-stable subspace of (5) is unramified, including the general
E in Section 1. It corresponds to a finite etale subgroup scheme over
Z_p. This conclusion does not require a basis, equations for the entire
ambient torsion, or a full ambient torsion splitting field.

The total genus of C is O_r(d), whereas R is fixed. Splitting all of
J_C[ell] would allow a field group of rank O(d), whose order is not a
polynomial in ell. That larger operation is not used here.

## 4. Regular fibres, field degree, and constant deck action

Because a mod p lies in U(F_p), the section a:Spec Z_p -> P^1_Z_p
factors through U. Therefore B_a is a finite etale Gamma-torsor over
Z_p, and inertia acts trivially on B_a(Qbar). Together with (5), this
proves that target inertia acts trivially on Z in (2).

Choose any geometric b in B_a. For sigma in Gal(Qbar/Q), write

    sigma(b)=b rho_b(sigma),   rho_b(sigma) in Gamma.

Since the right deck action is constant and defined over Q,
rho_b is a homomorphism. The stabilizer of b is exactly ker rho_b.
Consequently Q(b)/Q is Galois, and it ALREADY contains every point b g
of the fibre. Its degree and the splitting-field degree of B_a are

    [K_B:Q]=|im rho_b| <= d.                             (6)

This holds even if the fibre algebra or generic torsor is disconnected.
There is no d! splitting-field factor: the full fibre is a torsor, not
an arbitrary set of d unrelated roots.

The action on the vector space E is a representation

    rho_E:Gal(Qbar/Q) -> GL_R(F_ell).

Its kernel defines a Galois field K_E splitting the POINTS OF E, with
[K_E:Q]<=|GL_R(F_ell)|. The compositum splits the entire product set:

    [K_B K_E:Q] <= d |GL_R(F_ell)|.                      (7)

Both fields and their compositum are unramified at p. No splitting of
individual divisor-support points is asserted or needed.

For fixed n,r,R,

    d < ell^(n(n+1)/2+1),
    |E|=ell^R,     |GL_R(F_ell)|<ell^(R^2).              (8)

Thus the set cardinality and the common splitting-field degree are
polynomial in ell, with fixed exponents. For n=62 the exponent bounding
d is 1954. One does not assume p>|Z| or p>|GL_R|; an unramified extension
can have degree greater than p, or divisible by p.

## 5. Canonical divisors need not have good coordinate reduction at p

The rational object is the BASE VALUE a. A chosen b in its frame fibre
need not be a Q-rational curve point; its field is paid by (6). All
geometric components and an origin on each are available over K_B:
choose constant deck representatives for the multiplier quotient and
take the corresponding deck translates of b.

If the characteristic-zero basepoint choices make the relevant effective
representatives unique, their closed divisors and their closed encodings
are defined over K_B K_E. Galois invariance follows from uniqueness,
component by component. Pairing the encoding with b gives the same
Galois set Z; any actual presentation must preserve this equivariance.
Changing coordinates or making a nonminimal order does not change Z.

No hypothesis that every such divisor has distinct or etale support at
p is necessary. Supports of a closed divisor can even split over a
ramified extension while the divisor and its torsion class are defined
over an unramified field. For example a divisor cut out by X^2-p is
defined over Q despite its ramified individual roots. Coordinate
denominators, collisions, or a jump in the chosen canonical RR chart
at p do not imply ramification of the underlying finite orbit set.

Set A_Q=Q[Z]. Unramifiedness proved above says exactly that the integral
closure of Z_p in A_Q tensor Q_p is a finite etale Z_p-algebra. A
p-maximal order therefore has finite etale reduction, canonically
matching the unramified Galois set and its Frobenius action. An arbitrary
encoding order can have p-divisible discriminant from its index and fail
this test even when A_Q is unramified. The algorithm for p-maximalizing
that order, its bit bound, and the existing arithmetic/Tate conventions
are separate obligations, not consequences of choosing convenient
divisor equations.

## 6. A small-height base value with both target and auxiliary conditions

The target condition can be imposed without assuming p exceeds the
number of canonical divisors or exceptional images. At most r finite
residues of F_p are branch values. Since p>d>r+1, among

    1,...,r+1

there is a0 whose residue lies in U(F_p). The native branch polynomial
tests this condition. Now restrict to

    a=a0+p k,   k>=0.                                   (9)

Every such a has the required target-p property and is nonzero.

Let M_0 bound the number of forbidden characteristic-zero BASE VALUES
for all required canonical representatives and chart avoidance. Let
M_P bound the number of forbidden auxiliary residues in F_P, where
P!=p is a chosen good auxiliary prime. These are images of bad geometric
basepoints, so their counts are no larger than the corresponding
geometric bad-point counts. The existing Wronskian/support-avoidance
lemma gives, for example, a bound of order

    (# geometric components) * (# classes)
         * g_C^3 * (A_chart+1),                          (10)

with the actual representation's chart exceptions charged. This is
polynomial in ell for fixed n,r,R and polynomial-size plane models.
Avoiding all these base images makes EVERY point of the chosen fibre
suitable, including its deck translates; no chosen-root advice enters.

Suppose the auxiliary prime is chosen with

    P > M_0+M_P,

as well as its independently required model and characteristic bounds.
For k=0,...,M_0+M_P the residues a0+p k mod P are distinct. At most M_P
fail the auxiliary conditions, and at most M_0 of the distinct integer
values are characteristic-zero exceptions. At least one k survives.
Its height obeys

    h(a)=log a <= log p+log(M_0+M_P+r+2).                (11)

The counts are polynomial in ell and the charged geometric data. When
the upstream good-prime construction supplies numerical P polynomial
in the charged data, the enlarged threshold preserves that scope.
The height adds log p and logarithms of the counts. In particular no
requirement p>M_0+M_P was introduced.

If the auxiliary model and the lifted class identification already imply
that all good residue canonical conditions lift, M_0 can be omitted:
upper semicontinuity gives h0<=1 generically from residue h0=1, and
degree g Riemann--Roch supplies h0>=1; residue avoidance is also open.
Then k=0,...,M_P and P>M_P suffice. This shortened version requires that
specific good-model/lift compatibility, so (11) is the safe version
without re-proving it here. Selecting a good auxiliary model/prime and
constructing its class data remain the upstream paid inputs.

## 7. Exact boundary and strongest falsifiers

The accepted result is abstract good compactification, target-p
unramifiedness of Z, and the degree bound (7), under the actual arithmetic
frame-torsor/open-model hypotheses. It does not materialize a smooth
target-p plane model, normalize a supplied order algorithmically, split
the ambient torsion, or establish parabolic specialization.

The decisive failure cases are:

* A ramified constant twist: generic tame branch data alone misses it;
  extension etale over U/Z_p rules it out.
* Colliding branch sections: the Kummer/purity argument no longer gives
  one regular parameter at the boundary intersection.
* A base value reducing to a branch point: even t=z^ell over a smooth
  compact P^1 has a ramified fibre at a=p.
* An abstract cover without Q-rational constant deck action: neither the
  natural socle's stated Galois invariance nor (6) follows automatically.
* Replacing the fixed-rank E by unrestricted ambient torsion: the
  polynomial splitting-field bound is lost.
* Reducing a non-p-maximal coordinate order and interpreting collisions
  as intrinsic ramification: the order's index can cause those collisions.

None of these failures occurs under the explicit hypotheses used above.
