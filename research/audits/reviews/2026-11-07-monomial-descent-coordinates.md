# Monomial descent: compact-coordinate audit and exact replacement

2026-11-07. Support lemma treated CONDITIONALLY. Reviewed STATE/TRAPS,
CYCLIC_SUPPORT_MONOMIAL_DESCENT.md's proposed compact-coordinate section,
and actual Lenstra--Silverberg1509.08843 Theorems1.10/1.11 and
Algorithms8.3/8.4 in `/tmp/qsearch_lenstra_silverberg_1509_08843.txt`.
No Git/network/API, implementation or finite sweep. Interpreter:
`/opt/anaconda3/bin/python`.

## Optional logarithmic route: bounds and one verifier repair

The proposed delta_N=2^(-8N^2-10) separation is valid for every N>=1.
Here is a direct norm proof avoiding an uninspected transcendence theorem.
Suppose every conjugate of a unit u has |log|sigma(u)||<delta_N. For
v=sigma(u)*conj(sigma(u))!=1, the algebraic integer v-1 has degree d<=N^2.
Every conjugate of v has modulus at most exp(2delta_N), so its nonzero
integer norm gives

    |v-1| >= (1+exp(2delta_N))^(-(d-1))
           >= exp(-N^2*(log2+2delta_N)).

But |v-1|<3delta_N, and the displayed bounds are incompatible for the
chosen delta_N (indeed N^2 delta_N<=2^-18). If every v=1, all conjugates
of u have modulus1. The monic integer polynomials of its powers have
uniformly bounded degree and coefficients, so only finitely many powers
occur; u is a root of unity. This also covers small N without a missing
exception. A nonunit S-unit has a nonzero integer valuation, of size>=1.

For positive free rank R, a minimum lattice length delta_N implies

    covol >= vol_R(B(delta_N/2)) >= (delta_N/sqrt(R))^R.

The last inequality follows from the inscribed cube in the unit ball.
With M=sqrt(mR)*2^L bounding the largest singular value, the smallest is
at least s=(delta_N/sqrt(R))^R/M^(R-1). Its reciprocal has polynomial
BIT length in N,R,m,L. A target of norm<=sqrt(m)*2^L' has coordinate norm
at most C=s^-1 sqrt(m)*2^L'. Taking matrix operator error<=s/(16max(1,C))
and target error<=s/16 makes rational least-squares coordinates accurate
within1/4, so integer rounding is justified ON THE COMPLETE-BASIS EVENT.
Atom-log precision must include log(sum absolute compact exponents), which
is polynomial in their binary encoding, not the exponent values. R=0 must
bypass matrix inversion and proceed directly to torsion.

The torsion bound is valid: phi(w)<=N and phi(w)^2>=w/2, since each odd-prime
factor contributes p^(a-2)(p-1)^2>=1 to phi(w)^2/w and the only possible
factor below1 is1/2 from p=2,a=1. Thus w<=2N^2, including N=1.
Reduction modulo a prime ell not dividing w injects roots of unity:
if a nonidentity root of order d|w reduced to1, the exact identity
1+zeta+...+zeta^(d-1)=0 would reduce to d=0, a contradiction.

One genuine resource caveat affects the claimed DETERMINISTIC verifier:
rational factorizations of atom norms do not alone provide a deterministic
polynomial-time prime-ideal decomposition routine. The usual finite-field
factorization step is randomized. Supply and deterministically check full
prime-ideal/valuation certificates, or use deterministic gcd-free IDEAL
coordinates to certify that the residual is a unit. Torsion comparison may
also be done in the full quotient O_E/ell O_E by matrix inversions and binary
powering, avoiding selection of a residue field. Once unitness is proved,
the proposed delta_N/8 log accuracy and delta_N/2 threshold do correctly
separate roots of unity from non-root units. No finite-precision inequality
was found to fail, but these extra algorithms should not be silently omitted.

The parent has replaced this route by the exact relation method below.
Therefore its logarithms, finite valuations, conditioning and verifier
repair are OPTIONAL and are not obligations of the replacement endpoint.

## Accepted exact atom-lattice replacement

Let epsilon_1,...,epsilon_t be a COMPLETE compact generating list of E's
S-units, including torsion. A free basis modulo torsion plus a primitive
root of unity suffices; an independent proper-index list does not. The new
method permits redundancies and requires no unique coordinates.

Form one polynomial-size list alpha_1,...,alpha_K of EXPANDED nonzero field
atoms containing all compact generator leaves, their images under every
supplied g, and every expanded a_gi. Include the torsion generator and its
images. Applying g to an atom is polynomial-bit rational linear algebra;
never apply it by expanding a huge compact product. Repeated atoms may be
merged or retained consistently.

Record binary integer columns p_j,p_gj,q_gi with

    epsilon_j=alpha^p_j,  g(epsilon_j)=alpha^p_gj,
    a_gi=alpha^q_gi.

Actual LS Theorem1.11(i) supplies the FULL integer relation lattice

    Lambda=ker(Z^K -> E*, v -> alpha^v)

in deterministic polynomial time for an unrestricted finite system of
explicit atoms. The theorem checks units in the Q-algebra E, which here
means nonzero field elements; it does not require algebraic-integer units.
This is a source theorem actually read, not an assumed generic compact-
circuit equality oracle.

For unknown integer Z_ij and x_i=product_j epsilon_j^Z_ij, the descent
equation is EXACTLY

    sum_j Z_ij p_j - sum_(k,j) A_g[i,k] Z_kj p_gj - q_gi in Lambda.

The minus signs and indices agree with x_i/(g star x)_i=a_gi. If H is an
integer basis matrix for Lambda, introduce a separate integer y_gi and
equate this vector to H y_gi. All equations are linear over Z, with
polynomially many rows/unknowns and polynomial-bit entries. HNF/SNF gives
feasibility and polynomial-bit solution exponents. Returned x_i remain
compact, including negative exponents.

Do NOT saturate Lambda or replace it by its rational span: the atom -1
already has relation lattice2Z, whose saturation would falsely identify
-1 with1. The full lattice retains all torsion, so no real rounding,
separate torsion discrete logarithm, norm factorization or sign inference
is needed in this formulation.

An independent positive verifier recomputes Lambda deterministically from
the explicit atoms and checks these residual-vector memberships. It does
not trust S-unit completeness or an unverified relation-basis certificate.
NO still requires the complete generating-list event and the conditional
support theorem. A merely independent list can create a false NO.

## Paying torsion through the same actual source

If torsion is not supplied by the complete S-unit primitive, scan
1<=m<=2N^2. Construct the explicit Q-algebra E[T]/Phi_m, of dimension
N phi(m)<=2N^3. Actual LS Theorem1.10 decomposes it into fields with the
projection maps in deterministic polynomial time. A factor of Q-dimension
N is precisely a degree-one factor over E. Its embedded E is inverted by
rational linear algebra; the image of T then gives a primitive mth root
in E. Cyclotomic polynomial degrees and coefficient bit lengths are
polynomial here. Taking the largest successful m gives a generator of
the finite cyclic group of roots of unity. This covers torsion-only rank0
and avoids an uncited number-field factorization or good-prime oracle.

Disposition: ACCEPT the exact flattened atom-lattice interface, conditional
only on the separately paid support and complete-S-unit inputs. The optional
logarithmic bounds are mathematically sound with the stated verifier caveat,
but are unnecessary. No novelty, classical separation, integral/short-point
claim or execution is established by this review.
