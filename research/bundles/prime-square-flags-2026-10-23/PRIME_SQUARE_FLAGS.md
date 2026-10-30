# Prime-Square Kernel Refinement And The Common Definition Field

2026-10-23. PROPOSED SOURCE REFINEMENT; INDEPENDENT REVIEW PENDING.
Exact finite-module and lattice controls only. No PPAV quotient, canonical
geometric oracle, secret-kernel recovery or quantum algorithm was executed.

## Scientific Question

Can the smooth stabilized source use two prime-polarized quotient stages
instead of listing a prime-square kernel, including when that kernel is
non-free, WITHOUT introducing accumulating extension fields?

Answer: the following argument gives a candidate construction under the
EXISTING paid common-definition-field promise, made explicit below. This
reduces a large fixed exponent in the proposed source. It is not a new HSP
algorithm and does not establish novelty, classical hardness or a speedup.

The preceding smooth-repolarization bundle uses dimension d=16 and an
r^2-polarized endomorphism F with kernel G. It safely called the direct
quotient primitive with the full r^(2d)-point list. Replacing G by rG in a
prime quotient call is invalid when G has non-free factors. We instead
construct an intermediate maximal isotropic H with rG contained in H
contained in G[r].

## 1. Exact Refinement Lemma

Let r differ from the characteristic, X be a principally polarized abelian
variety of dimension d, and G be a maximal isotropic subgroup of X[r^2].
All groups in this section are geometric points; field descent is separate.
Choose compatible Tate coordinates with alternating form J. Write

    G = (Z/r^2)^a + (Z/r)^b,       2a+b = 2d.
    I = rG inside X[r],            dim I = a.
    W = G[r] inside X[r],          dim W = a+b = 2d-a.

These are abstract direct-sum types, not chosen canonical splittings.
Identify X[r] with F_r^(2d) by writing its points as r times coordinates
in X[r^2]. Then

    W = I^perp.

Indeed, if x has r^2-torsion coordinates v in G and w in W has coordinates
r z, isotropy of G gives v^t J (r z)=0 mod r^2. Thus the r-torsion
coordinates v mod r of r x are orthogonal to z. This proves inclusion;
the displayed dimensions prove equality. Also I is isotropic: use
v^t J u=0 mod r^2 for x,y in G, then reduce mod r.

Extend I to any Lagrangian H of the symplectic F_r-space X[r]. This can be
done by ordinary finite-field elimination. Since H contains I and is
isotropic, H lies in I^perp=W. Consequently

    rG contained in H contained in G[r] contained in G,
    |H| = r^d,              |G/H| = r^d.

Let q1:X -> X1=X/H be the r-polarized quotient. The group q1(G) is killed
by r, because rG lies in H. It is maximal isotropic in X1[r]. One way to
check the last assertion, including the correct pairing, is the following
lattice calculation. Work locally at r with source lattice L and form J.
Choose lifts of an F_r-basis of H, and let the columns of T span rL+H.
The quotient lattice is L1=(T/r)L. In these coordinates

    Q = r T^(-1),             J1 = T^t J T / r,
    Q^t J1 Q = r J.

J1 is integral and perfect. If v is an r^2-torsion coordinate vector of
an element of G, its image has r-torsion coordinates T^(-1)v. Those are
integral locally at r because rG is contained in H. For v,w in G,

    (T^(-1)v)^t J1 (T^(-1)w) = v^t J w / r = 0 mod r.

Thus q1(G) is isotropic and has the requisite order r^d. Its quotient
q2:X1 -> X2 is r-polarized, and q2 q1 has exactly kernel G and multiplier
r^2. This also handles G=X[r], when I=0 and W=X[r]. In that example,
the invalid first kernel rG would be trivial; H must be chosen instead.

The implementation uses Smith transformations for the kernel, finite-field
linear algebra for H, and an independent Hermite-lattice calculation for
J1 and q1(G). These matrices are NOT actual geometric point coordinates
for an implemented PPAV backend.

## 2. A Rational G Does Not By Itself Give A Rational H

The descent question cannot be dropped. In a two-dimensional symplectic
F_3-space, the matrix

    [[0,-1],[1,0]]

preserves the whole space but no line: x^2+1 is irreducible over F_3.
It preserves G=X[3] in the corresponding mod-9 control, but no possible
first Lagrangian H. Squaring this matrix gives -I and removes that local
obstruction. This is a torsion-module countercontrol, not a claim that
every displayed lift is the Frobenius of a specified elliptic curve.

For an arbitrary Frobenius action one must either prove a stable flag
exists, pay for a suitable extension and track it, or retain the direct
r^2 quotient. Choosing an arbitrary H and pretending it descends is wrong.

## 3. The Source Contract Supplies Scalar Frobenius

The smooth source uses a supersingular elliptic curve E, A=E^2, and an
isogeny phi:A -> B. Its paid common finite field k must define phi AND
every element of the supplied full endomorphism-order basis of E. This
is stronger than merely saying the basis exists over an algebraic closure.
An evaluator whose field dependencies are unspecified does not suffice.

Under that promise the Frobenius pi_E commutes with the entire order O.
Since O spans the quaternion algebra End^0(E), its centralizer within
that algebra is Q. Therefore pi_E is a rational scalar. It is an integral
endomorphism, so pi_E=[c] for an integer c; its degree gives |k|=c^2.

The isogeny is defined over k, hence

    pi_B phi = phi pi_A = phi[c].

Surjectivity of phi implies pi_B=[c]. Products of B also have scalar
Frobenius. Every geometric finite subgroup of order prime to the
characteristic is then Frobenius-stable. In particular, ANY chosen H in
Section 1 descends over k, as does q1(G). A quotient defined over k inherits
the same scalar Frobenius by the identical surjectivity argument.

Thus the two prime stages, and every later auxiliary-prime stage, stay over
the SAME k. No compositum of successive flag-definition fields is needed.
This observation uses the known SOURCE order, not a supplied target order.
The fact that target endomorphisms are defined over k does not give an
algorithm for finding a basis of End(B).

For each auxiliary prime r, all r^2-torsion is rational over k of degree

    ord_(r^2)(c) <= r(r-1).

One can simply use the upper-bound extension without solving a large
discrete logarithm. This is charged field construction at SMALL auxiliary
r. It is not polynomial in log r, and is not permission to access the
large secret ell-torsion. Separate extensions can be used for separate
primes, with the compatible embeddings already required by the contract.

The argument assumes the quotient primitive actually produces a model and
map over the subgroup's definition field, or handles the bounded field
extension allowed by the model. A backend that outputs only over its
temporary torsion-coordinate field must implement the promised descent;
the abstract stability argument does not perform that computation.

## 4. Applying It To The Stabilized Source

The source constructs F:X -> (B,lambda_B H)^8 on X=(B,lambda_B)^8, with
F^dagger H8 F=D^2 I and D squarefree. For each r dividing D, its r-primary
kernel G_r in X[r^2] is available from the weak common-unit image basis
and the computed matrix of F. The common scalar changes generators but
not the subgroup. Use Section 1 to obtain H_r, turn its basis into points,
and supply the complete H_r list to the prime quotient primitive.

Push generators of G_r through q1. Their image is q1(G_r); enumerate its
r^d elements for the second prime quotient. Push remaining-prime kernels
and the marking points through both maps. Since distinct auxiliary primes
are coprime, earlier quotients are invertible on later-prime torsion.
They preserve isotropy there up to a unit multiplier. Repeat, retaining
the same common field by Section 3.

This is a proposed refinement of the use of primitive A26 in
[Corte-Real Santos, Piasecki and Wesolowski, 2026/1142](https://eprint.iacr.org/2026/1142).
The preceding source note retains the valid direct-call fallback. We do
not rely on an unmodified CRT loop for a non-free prime-square kernel.

Per prime, explicit kernel lists change from r^(2d) points to 2 r^d points.
For d=16 the exponents are 32 and 16. This comparison counts LISTED KERNEL
POINTS only; it is not a proved factor improvement for the entire PPAV
arithmetic, canonicalization or quantum circuit. Both costs can be enormous.
The original Sp_4(F_ell) action and eight-copy markings are unchanged.

## 5. Attempts To Falsify The Refinement

- Non-free kernel: G=X[r] destroys the rG shortcut; the flag survives.
- Mixed kernel: the t=7,D=30 example has a=8,b=16 at r=5, not a=16.
  An initially overstrong test assertion failed; the actual flag and the
  independent residual pairing checks pass. At r=2, a=0,b=32; at r=3,
  a=16,b=0. Kernel type must be computed, not inferred from point order.
- Frobenius descent: the irreducible mod-3 control destroys the general
  rational-flag assertion. The source-specific scalar argument is essential.
- Pairing after q1: checking only the order of G/H would miss a wrong
  polarization. The independent quotient-lattice identity checks both.
- Hidden field advice: if the full source order and phi are not defined
  over the paid common field, Section 3 is unavailable. Keep that source
  instance blocked or use the correctly charged direct quotient route.
- Hidden secret torsion: extension enumeration at auxiliary r is paid and
  polynomial in r, NOT log r. The procedure never enumerates ell-torsion.
- Practicality: d=16 and r^16 lists still prohibit most realistic execution.
  This is an asymptotic-source repair, not a benchmark or practical attack.
- Novelty: isotropic refinements are standard symplectic constructions.
  The contribution here is explicit handling of the non-free case and its
  field requirement in this particular candidate source. No novelty
  certification is implied by tests or by a literature search.

## 6. Remaining Decisive Questions

The same three scientific obligations remain: independently review the
complete geometric source and coherent compilation; attack the SAME weak
input and geometric labels classically; determine whether the full surface
extension is already implied by prior work. This refinement resolves none
of those wholesale. A kernel-recovery experiment or novelty claim must not
be generated from this receipt.

Source/staging are unchanged during migration. See HANDOFF.md for the
bounded integration tasks and VERIFICATION.md for the tested scope.
