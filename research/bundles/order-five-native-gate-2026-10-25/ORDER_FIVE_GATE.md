# Two Actual Curve Maps Remove The Kernel Ambiguity

2026-10-25. Proposed local deduction, not independently reviewed or formally
verified. This is a conditional classical attack on a concrete native
subfamily, not a new quantum algorithm, novelty claim or general solver.

## Decision

The previous regular-spectrum result still needed an actual public map
and, in nonunique cases, a valid original geometric source to choose among
the candidates. Here BOTH gaps disappear for the explicit target models

    C_c/F_p: y^2=x^5+c,  c in F_p^*, p>5 prime, p=4 modulo 5,
    B=Jac(C_c).

There are two actual public maps: sigma(x,y)=(zeta_5 x,y), defined over
F_(p^2), and the p-power Frobenius pi of this prime-field curve model.
Together they force the existing source-pullback word test to recover
the full kernel for every genuine incoming polarized ell-isogeny in the
original input contract, for odd ell different from p and 5. No geometric
hiding-function evaluation or target-order completion is needed.

The useful new deduction is the access-matched composition with the old
word attack. The curve family, automorphism, Mumford formulas and spectrum
are established arithmetic geometry, not discoveries of this project.
For example [Fan--Gong--Jao, Section 3](https://cacr.uwaterloo.ca/techreports/2008/cacr2008-04.pdf)
gives the efficient order-five automorphism and its cyclotomic polynomial;
[Guralnick--Howe](https://arxiv.org/abs/0804.0578) treats automorphism spectra
more generally. Superspeciality of this family for p=4 mod 5 is also
recorded in [The Level of Pairs of Polynomials, Example 2.3](https://pure.rug.nl/ws/portalfiles/portal/127612112/The_level_of_pairs_of_polynomials.pdf).

NO incoming phi was constructed or recovered geometrically in this pass.
The theorem is conditional on receiving the original valid weak input.
This does not assert that every p,ell or chosen E admits such a phi.

## Original Input And Paid Access

Retain phi:A=E^2 -> B, phi^dagger phi=phi phi^dagger=[ell], with the
known full source order, positive trace Gram and public source splitting.
All auxiliary weak images W_r=u_r phi_r share a common scalar on a full
ordered basis, and all levels must describe the same isogeny. Enough
legal fresh small levels, their point fields and basis operations remain
assumptions/costs of the SAME original input. This pass does not turn a
short transcript into an arbitrary weak evaluator.

The algorithm receives the ACTUAL equation above, not merely a claim
that a generic target is isomorphic to it. An isomorphism from another
model would need to be supplied, verified and paid; none is found here.
The full source order and phi may live over a larger common field. The
explicit prime-field equation still supplies pi after that extension.
Replacing pi by the scalar Frobenius of the larger field can destroy the
argument. No smaller-field descent or hidden map is granted.

No target order, Hom basis, geometric ell-torsion basis, secret phi or
secret kernel enters the attack. The only additional field needed to
write sigma is degree two over F_p. Factoring Phi_5 over that field is
fixed-degree finite-field algebra, not enumeration of p elements.

## Geometry And Public Map Certificates

Smoothness follows since c!=0 and p!=2,5. The polynomial
(x^5+c)^((p-1)/2) has only exponents divisible by five. The four
Cartier--Manin indices p-1,p-2,2p-1,2p-2 are 3,2,2,1 modulo five.
Their coefficients vanish, so the Cartier matrix is zero. The standard
genus-two criterion gives geometric superspeciality. This proves a
growing-characteristic family, not just the p=19 control. It does not
provide a product splitting or an incoming polarized isogeny.

Choose a primitive fifth root zeta over F_(p^2). Since p=-1 modulo five,
zeta^p=zeta^(-1). Both maps fix the unique point at infinity, so point
pushforward induces unambiguous maps on degree-zero divisor classes:

    gamma = sigma_*,       pi = Frob_p,
    gamma^dagger gamma=1,  pi^dagger pi=p,
    pi gamma=gamma^(-1) pi.                              (1)

The squared Rosati norms are 4 and 4p respectively. In particular they
are explicit small bounds for the existing exact source reconstruction.
Inseparability of pi causes no issue on ell-torsion or auxiliary r-torsion
when ell,r differ from p. Its adjoint action is p pi^(-1) there; no
unprovided geometric inverse-Frobenius oracle is required.

The quotient of C_c by sigma is the genus-zero curve with coordinate y.
Norm followed by pullback is 1+gamma+...+gamma^4 and factors through its
zero Jacobian. Hence Phi_5(gamma)=0. Gamma is not the identity; equivalently
its action on curve differentials includes zeta and zeta^2. Since Phi_5
is irreducible of degree four over Q, the degree-four rational Tate
characteristic polynomial is EXACTLY

    chi_gamma(T)=Phi_5(T)=T^4+T^3+T^2+T+1.                (2)

There is no auxiliary polynomial-guessing step. The known geometry proves
it. For ell!=5 its roots are the four distinct primitive fifth roots.

### Divisor Evaluation

For a reduced Mumford pair (u(X),v(X)), u monic of degree d<=2 and
u dividing x^5+c-v^2, the maps are

    gamma: (u,v) -> (zeta^d u(X/zeta), v(X/zeta)),
    pi:    (u,v) -> (u^(p),v^(p)),

where the superscript on the second line raises COEFFICIENTS to the
p-th power, not the variable. Identity and degree-one divisors are
included. Infinity is fixed, so no base-divisor correction is missing.
The formulas preserve the reduced degree bounds and divisor relation.

The executable frontend currently operates on F_(p^2) divisor data.
The same formulas extend to a compatible paid auxiliary field, but its
construction, torsion basis and pairing-based action extraction are NOT
implemented here. Do not infer an auxiliary-torsion backend from point
tests over F_(p^2).

## Why These Two Maps Suffice For Every Kernel

Work on V=B[ell] with its alternating form, extending scalars to an
algebraic closure only for the proof. Equation (2) gives one-dimensional
gamma eigenlines E_1,E_2,E_3,E_4 with eigenvalues zeta,zeta^2,zeta^3,zeta^4.
Since gamma is symplectic, E_i pairs only with E_(-i), and that pairing
is nonzero by nondegeneracy of V. Thus

    W_1=E_1+E_4, W_2=E_2+E_3

are orthogonal nondegenerate symplectic planes. Invertible pi exchanges
E_i with E_(-i) by (1). A subspace invariant under gamma is a sum of its
distinct eigenlines; invariance under pi forces inverse pairs. Therefore
the only joint invariant subspaces are 0, W_1, W_2 and V. Any proper
nonzero such subspace is a NONDEGENERATE plane. This classification over
the algebraic closure also excludes additional possibilities over F_ell.

Let L=ker(phi^dagger), a Lagrangian plane in V. No proper common invariant
subspace can contain L, because the only candidates would have dimension
two and be nondegenerate, whereas L is isotropic. Let Gamma be the
adjoint-closed alphabet gamma, gamma^dagger, pi, pi^dagger, and set

    S_0=L, S_(j+1)=S_j+sum_(a in Gamma) a S_j.

If S_j stops growing it is common invariant. Since it contains L it must
then equal V. Starting in dimension two, it follows that S_2=V: there
are at most two strict dimension increases. This is a general linear
algebra proof, not extrapolation from the finite census.

On source ell-torsion, im(phi)=L and ker(phi^dagger)=L. Therefore the
images of the actual pulled-back words span

    phi^dagger S_2 = im(phi^dagger) = ker(phi)=K.

The first words are alpha_a=phi^dagger a phi. A second word is obtained
in the known full source order as

    alpha_(ab)=alpha_a alpha_b/ell.

This exact division is justified by phi phi^dagger=ell. Consequently
the EXISTING extract_kernel routine, with its adjoints and at most two
layers, recovers all of K. No list-selection oracle is needed. This
proof actually uses no product-polarization classification after the
original source reconstruction is available.

## Costs, Failure Conditions And Scope

Recover two exact source pullbacks with the old norm-bounded trace-CRT
algorithm at bounds 4 and 4p, then at most sixteen pair products of the
four-element adjoint-closed alphabet. Public source reduction and
four-dimensional linear algebra finish the attack. Bit complexity of
the added arithmetic is polynomial in log p, log ell and source
description/bounds. Auxiliary point access, field operations and source
order evaluation retain the old charges; this is not a claim they are
free or that the geometry backend has been implemented.

An input failing a model, norm, relation or rank check is inconsistent or
outside this gate. It is not evidence of hardness. Ell=5 has repeated
spectrum and is excluded; ell=2, ell=p and other target models are also
outside this implementation. Using only gamma does NOT imply this
two-map conclusion: for split Phi_5 there are invariant Lagrangians.
Using a commuting scalar map instead of the true p-Frobenius violates
the inversion relation and is rejected even if its multiplier matches.

The selected explicit family is highly symmetric and known in the
literature. It is not representative of generic superspecial targets.
Neither the number of such targets in a research distribution nor the
existence of a prescribed incoming ell-isogeny is established. The result
should REMOVE these supplied-model cases from an advantage claim, not
generate benchmark instances around them or advertise a new generic
cryptanalytic solver.

## What The Controls Establish

* Actual C/F_19 with c=-1 has 438 points over F_(19^2). The frontend
  checks the maps and their relation on every affine point, plus identity
  and forty degree-two divisor controls with distinct x coordinates.
* Native map acquisition is checked at seven characteristics, including
  p=4294967279; it factors degree-four polynomials rather than searching
  the field. Exhaustive
  point enumeration is separately capped and used only for controls.
* The local split-spectrum case ell=11 checks ALL 1464 Lagrangians.
  Every tested orbit already has dimensions (2,4,4); the theorem only
  needs the weaker at-most-two-layer bound. This is not a geometric
  distribution over incoming isogenies.
* Selected prime-square neighbor computations independently translate
  target orbit growth into source pullback images and recover the known
  local reference kernel. Those inputs contain the reference L and are
  clearly marked controls; the production attack must never receive it.

No native phi, native auxiliary torsion bases, end-to-end kernel recovery,
independent mathematical review or quantum advantage was produced.

## Next Decision

Public map acquisition is now concrete for THIS supplied target family.
A decisive execution would construct one genuine incoming weak isogeny
with its exact permitted auxiliary data and recover K using only that
data. Mechanical integration can wait for the verified checkout; no
new research infrastructure is needed. For broad discovery, move beyond
these highly symmetric targets or return to a genuinely constructive
HDQI/native inverse-trace mechanism. More local primes do not establish
generic coverage or a Shor-level result.
