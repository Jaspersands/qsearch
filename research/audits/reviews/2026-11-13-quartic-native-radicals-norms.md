# Quartic native radicals and the relative norm subspace

2026-11-13. Focused independent review of the appended native section of
`QUARTIC_RELATIVE_NORM_CLASSICAL.md`, the 254-line support-correction proof,
and the retained `quartic_native_radicals/*.json`. Current STATE was read.
No network, API, Git, archive, implementation, or numerical sweep.

**Accepted with an explicit recognition clarification.** Both radical
branches are correct and have polynomial coordinate size. A rational
cubic-resolvent root alone does NOT certify that the quartic is Galois;
the rational norm-square test below supplies that certificate without a
Galois or number-field-factorization oracle. The norm subspace V is
computable in polynomial bit time with finite local support and common
local frames. The relative conic solver remains the stated CONDITIONAL
interface, including its output-height and confidence clock. No whole
quartic algorithm is promoted independently of that condition.

## 1. Native extraction, including the zero-discriminant branch

Let

    h=X^4+aX^3+bX^2+cX+e

be monic irreducible over Q, and let theta=X mod h. Native monic integer
factors have coefficient bit size polynomial in their original input.
Form

    R(T)=T^3-bT^2+(ac-4e)T+4be-a^2e-c^2.

Its roots are the three quantities `alpha beta+gamma delta` for the three
unordered pairings of the four roots of h. They are distinct, since their
differences are products of differences of distinct roots of h.

A rational root u selects a Galois-invariant unordered pairing. Take the
pair containing theta, with sum s and product t. The other pair has sum
`-a-s` and product `u-t`. Comparing coefficients gives

    s^2+a*s+b-u=0,       t^2-u*t+e=0,
    c=(2s+a)t-su,        theta^2-s*theta+t=0.          (1)

Eliminating t and s^2 gives the actual native formula

    s=-(a*theta^2+2(b-u)*theta+c)/(2*theta^2+a*theta+u).

The denominator cannot vanish: it is a nonzero rational polynomial of
degree 2 at an element of degree 4.

Put `Ds=a^2-4b+4u`. If Ds!=0, then

    (2s+a)^2=Ds,       t=(c+s*u)/(2s+a).

Ds is a nonsquare in Q. Otherwise s would be rational, the nonzero
quantity 2s+a would make t rational by (1), and theta would satisfy a
rational quadratic. Thus F=Q(s) is genuinely quadratic.

If Ds=0, put `s=-a/2` and use `t=s*theta-theta^2`. This t still satisfies
(1). It is nonrational, because rational t would again give a quadratic
for theta. Hence

    Delta_t=u^2-4e=(2t-u)^2

is nonzero and nonsquare in Q, and F=Q(t). This also rules out the feared
second degeneracy Delta_t=0. The identity `c=-su` follows from (1);
no division by 2s+a is made in this branch.

In either case set

    d=s^2-4t,          z=2theta-s.

Then `z^2=d`, `theta=(s+z)/2`, and L=F(z). The element d is nonzero and
not a square in F, since otherwise theta would belong to F. These are
actual embeddings and a relative basis, not an abstract radical oracle.

For Galois quartic L/Q the group is C4 or V4. Its action on the three
pairings has respectively one or three fixed points, so R has respectively
one or three rational roots. Rational polynomial factorization over Q
finds them in polynomial time; enumerating divisors of a constant term is
neither required nor an acceptable replacement.

## 2. Coordinates, normality, and the odd quadratic base

All preceding computations have polynomial bit size. The coefficients of
R have O(B) bits for fixed degree and B-bit h; its rational roots have
O(B) bits by the rational-root/height bound. Inverting the quadratic
polynomial in theta uses a constant-size rational linear system. Its
nonzero determinant and adjugate have O(B) bits. Subsequent inversions in
the quadratic field have the same fixed-degree bound.

Extract the squarefree signed integer D and rational q with
`Ds=D q^2`, or `Delta_t=D q^2` in the zero branch. This uses a charged
integer-factorization call on a polynomial-bit integer. In the first
branch embed `sqrt(D)=(2s+a)/q`; in the second use
`sqrt(D)=(2t-u)/q`. Expressing d in the basis `1,sqrt(D)` is then exact
quadratic arithmetic. The coordinate matrix of

    1, sqrt(D), z, sqrt(D)*z

in `1,theta,theta^2,theta^3` is nonsingular, with polynomial-bit rational
entries. Its inverse has polynomial-bit entries by the fixed-size
Cramer bound. Both embedding directions are therefore paid.

A rational resolvent root also occurs for non-Galois D4 quartics. Here is
an exact recognition test. Let `n_d=N_F/Q(d)`. Then

    L/Q is Galois iff n_d is a square in F
                 iff n_d in Q^{*2} or n_d/D in Q^{*2}. (2)

Indeed the conjugate extension is F(sqrt(tau(d))), and
`tau(d)/d=n_d/d^2`. A rational number is a square in F precisely when it
is a rational square or D times a rational square, as expansion in
`1,sqrt(D)` shows. These are rational integer-square-root tests, with
no number-field factoring.

More precisely, choose `c0 in F` with `c0^2=n_d`. A lift of tau sends
`z -> c0/z`. Its square sends `z -> tau(c0)z/c0`. If n_d is a rational
square, c0 is rational and the group is V4. If n_d/D is a rational square,
c0 is a rational multiple of sqrt(D), and the group is C4. The cases
are disjoint because D is nonsquare. This proves the exact classification
rather than inferring it from the number of rational resolvent roots.

If L/Q is in the one-finite-ramified-prime family, so is its quadratic
subfield F: ramification indices multiply in towers. The previously
proved special-Q inertia argument then makes Cl(F) odd, for real OR
imaginary F. The fundamental discriminant of the computed quadratic F
is explicit (`D` if D=1 mod 4, otherwise `4D`), so its one-prime property
can itself be checked from the charged factorization. No class-number
oracle is involved. If one also wants to certify the original field's
one-prime property rather than use that input-family condition, its
maximal order/discriminant is available from the already paid native
order algorithm with factorization of disc(h). Polynomial discriminant
and FIELD discriminant must not be confused: an index can add primes.

For a branch factor of the original monic f, the native support of
`2 disc(f)` already contains every ramified prime needed here. Extra
index or cross-resultant primes in that support are permitted. Outside
S the quadratic extension is unramified, hence `v_P(d)` is even and
`[d] belongs to F(S,2)`, regardless of the chosen radical's denominators.

The retained two controls test the nonzero branch for Phi5 and the zero
branch for `X^4-34X^2+17`. They do not establish the general height bound,
the V4 case, normality recognition, or the norm tables; those are proved
here rather than inferred from the controls.

## 3. A finite exact description of V

Compute a complete explicit basis `a_1,...,a_k` of F(S,2) with the retained
quadratic squareclass compiler. Its output coordinates and k are polynomial.
For every place v of F use the quadratic Hilbert symbol `(a_i,d)_v`.
The required space is exactly the kernel of these binary rows:

    V=F(S,2) intersect N_L/F(L*).

For a place outside S the residue characteristic is odd and both
valuations are even. Their squareclasses are unit classes, whose odd
Hilbert symbol is 1. Thus only the at most `2|S_Q|` finite places over
S_Q and at most two real places are needed. Complex places impose no
condition. Completeness is the quadratic Hasse norm theorem, equivalently
Hasse--Minkowski for `x^2-d*y^2-a*z^2`; this is an existence statement,
not the algorithmic conic-solver clock.

At a real embedding the row tests whether a_i is negative when d is
negative. Signs of `A+B sqrt(D)` are computed exactly by integer/rational
comparisons, including comparison of A^2 with B^2 D. There is no
unbounded floating-point sign decision.

At an odd place with residue size q, write
`a=pi^alpha*u`, `d=pi^beta*v`, with u,v units. The exact formula is

    (a,d)=(-1)^(alpha*beta*(q-1)/2)
           *chi_res(u)^beta*chi_res(v)^alpha.          (3)

Only valuation parities and residue quadratic characters are needed.
Residue fields have degree at most 2 and `log q<=2 log p`; exponentiation
computes the characters in polynomial bit time. At unramified primes take
pi=p; at a ramified odd prime in the quadratic field, sqrt(D) is a local
uniformizer. Split places are distinguished by the selected simple
residue roots and their fixed Hensel lifts. Random searches for modular
nonresidues/root routines use bounded independent retries with a union
budget; a failed clock returns ABORT, not an unproved deterministic
least-nonresidue bound.

Exact valuations require only polynomial precision. If
`a=(A+B*omega)/C` in the integral quadratic basis, its integral numerator
has nonzero integer norm. Each numerator valuation is bounded by the
valuation of this norm, and the denominator subtracts `e_P*v_p(C)`.
Consequently `(needed digits)*log p` is bounded by the norm/denominator
bit lengths. This covers large cancellation at a split prime and
negative valuations. The same bound applies to d and every basis query.

## 4. Dyadic norm tables, including their precision and frames

Fix a dyadic completion E of F, of absolute degree at most 2. The relative
algebra is either E times E, with unrestricted norm image, or a quadratic
FIELD H/E of absolute degree at most 4. Construct these actual local
factors/orders from the native quadratic/quartic polynomials using the
reviewed local backend. No factorization over an unspecified number field
is assumed.

The computed embedding F->L groups the L-completions above each E. When
F splits at 2, evaluate the embedded sqrt(D) and compare it with its two
fixed Q_2 roots. Here D is an odd unit congruent to 1 modulo 8, and the
two roots have difference of valuation 1; a fixed additional guard after
coordinate conversion distinguishes them. When F is a dyadic field,
there is only one base place. The dimensions of the grouped factors
then distinguish the split relative algebra from the quadratic field.

For the field H let `e_H,f_H` be its absolute ramification and residue
degrees, and fix an integral basis and uniformizer. Hensel at 1 proves

    1+P_H^(2e_H+1) is contained in H^{*2}.

Enumerate representatives of its unit quotient. Their exact number is

    (2^f_H-1)*2^(2e_H*f_H) <= 15*2^8=3840 < 2^12.

This is a constant because `[H:Q_2]<=4`, not because a large residue
field has been ignored. Norms of these units, together with the norm of
one H-uniformizer, span the COMPLETE norm image in E*/E*2: every H-element
is a uniformizer power times a unit, and the omitted principal units
are squares. Compute all these labels in ONE fixed native squareclass
frame of E. Label every a_i in that same frame, then take the binary
annihilator of the table span. This pays common coordinates explicitly;
separately chosen unmatched squareclass bases would not suffice.
The E-frame can itself be built by enumerating its unit quotient modulo
`1+P_E^(2e_E+1)`, which has at most 48 elements, taking the quotient by
its subgroup of squares, and adjoining the valuation-parity bit. That
principal-unit subgroup consists of actual E-squares, so this finite
quotient is exact. All residue lifts and the uniformizer come from the
computed local integral basis; none are additional inputs.

Constant table cardinality does NOT mean constant input precision. Norms
can be computed using the explicit relative basis `1,z`, by
`N(A+Bz)=A^2-d B^2`. Conversion to that basis is polynomially conditioned
from native data. For a degree-four completion its absolute trace
basis discriminant is

    disc(1,omega)^2 * N_E/Q2(4d).

For a degree-two completion over Q_2 it is `4d_v`. Clear the known rational
coordinate denominators first. The resulting valuation bounds follow
from the integer norms of those denominators and d, all of polynomial
bit length. Comparing with an integral-basis discriminant bounds the
conversion determinant/index; constant-size adjugate inversion therefore
has a computable polynomial precision loss. The local order's own
index/factor guards are bounded by v_2 disc(h), as already reviewed.

Table units have norm valuation zero; the uniformizer norm has relative
residue-degree valuation at most 2. Their E-labels require only a fixed
number of digits AFTER those conversion guards. Query a_i and d may
need more digits, but their preceding integral-norm bounds supply a
polynomial cap. Thus all tables, embeddings, valuation discoveries and
labels have actual polynomial bit cost and visible finite tests.

## 5. Remaining conditional interface

The binary kernel in Section 3 gives basis representatives of V as
products of polynomially many a_i. Expanded quadratic coordinates remain
polynomial-bit. The separate support-correction review then applies
exactly as written: conditional on polynomial-bit relative conic lifts,
factor their cleared norms/denominators, compute the enlarged quadratic
squareclass basis, and solve the parity system. Its odd-class hypothesis
is supplied above; it needs no ideal principalization.

No further radical, Galois, subfield, squareclass-coordinate, local-norm,
or finite-support oracle remains in this native interface. The outstanding
condition is still the relative conic backend with its proved polynomial
BIT clock, explicit nonzero output and coordinate-height bound. Extra
integer factorizations of polynomial-bit intermediate data remain an
explicit resource. This review does not replace that conditional backend
by a field-operation claim or promote the whole quartic endpoint.
