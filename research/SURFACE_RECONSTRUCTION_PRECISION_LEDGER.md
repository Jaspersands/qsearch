# Explicit majorants for the native reconstruction precision

2026-11-12. Reviewed scoped height-to-precision derivation. This supplies computable
majorants for the already proved height chain; it is not an implementation
of Arakelov geometry, a semistable-model algorithm, or a new surface theorem.
Parent checked the completed arithmetic report and its explicit derivations.
The prior effective-polynomial proof and all geometry/local-computation
hypotheses remain mandatory; this note does not construct those inputs.

## Input and aim

On ONE geometrically connected component let d be its cover degree, g its
genus, r>=3 a bound on the total branch orbit, and hB a computed upper bound
on absolute LOGARITHMIC branch heights. The native plane model has known
degree and rational coefficient bit bounds. Choose the common integer a>0,
regular at the auxiliary prime, and the residue-good coordinate c as in the
reconstruction review. Their actual integer values are known. All formula
evaluation can use outward rational/integer bounds on logarithms.

Aim: produce an integer K bounding every rational product/interpolation
coefficient's logarithmic height, so P^e>2*exp(2K) certifies reconstruction.
No unknown torsion field or analytic chart is constructed. Field extensions
in the height proof occur only inside normalized inequalities.

## An explicit analytic constant

Use the exact angular Whitney/root atlas in merkl-log-atlas. Write
L=1+log(1/delta), theta0=(delta/100)(3/4)^d, a(s)=min(1/4,dist(s,B)),
rho(s)=a(s)/100. Its balls of radius rho(s)/16 are disjoint. For a dyadic
layer t<=a(s)<2t, each ball has spherical area at least t^2/1600^2 and
their union is inside r caps of radius3t and total area at most36r t^2.
Hence there are fewer than2^27*r centers per layer. The capped layer has
fewer than2^29 centers, by the total sphere area and radius1/6400. There
are at most2L+d+10 layers. Including every lift and the at-most-rd branch
charts, the deliberately loose bound

    N <= 2^42(r+1)d(d+L)

suffices. The already proved full-chart density and ordered-overlap bounds
are c1<=d^2 and M<=500d(4/3)^d, so log M<=9d. Actual Javanpeykar/Bruin
Theorem3.1.2 at inner radius7/8 bounds BOTH the Green upper bound and its
local two-sided regularization by2^16*N*d^2. This also bounds the3/4 version.

The exact product formula gives average L<=L0, where

    L0=1+r(r-1)(2hB+1),
    Lambda=2^60(r+1)d^3(d+L0).

Thus Lambda bounds the relevant embedding-averaged analytic quantities.
No exponential in hB, uncomputed real separation, optimized decimal
constant, spectral estimate, or ineffective existence theorem occurs.

## Point, Faltings, theta and discriminant majorants

For a positive integer v OUTSIDE the branch set B define

    Z(v)=Lambda+(d+1)r(hB+log(1+v)+1)+2d^2 log d+7.

The actual finite div(d pi) intersection identity, not just contraction to
the minimal model, bounds h_Z(b)<=Z(v) on the SPECIFIC cover-compatible
semistable normalization-resolution for pi(b)=v. It combines source
Proposition4.2.4/Theorem4.3.2 with the point-height proof's differential
bound1/800. The finite extension degree cancels after normalization.
It is invalid to replace this Z by an arbitrary additional blowup model.

Set v0=g^3+r+1, A_g=g(g+1)/2 and

    W=A_g*Lambda+[g(g-1)/2]log4+(g/2)log(2g^2 d^2),
    F=A_g*Z(v0)+W,
    Delta=2g(g+1)(4g+1)*Z(v0)+12W+93g^3,
    Theta=(g/4)log max(1,F)+(4g^3+5g+1)log2.

Some integer 1<=v<=v0 lies outside B and has no Weierstrass point above it:
there are at most g^3-g Weierstrass points and r branch values, strictly
fewer than v0 excluded integers. Integer v is finite and has no finite
intersection with infinity. Actual source Theorem2.4.1
and Lemma2.4.2 therefore bound h_Fal by F, minimal semistable node sum by
Delta, and averaged log theta supremum by Theta. No test for that auxiliary
height-proof point is needed by the algorithm: monotonic Z(v0) is a bound
for an existing suitable v. This is distinct from the ACTUAL common a
whose height enters the canonical divisor calculation next.

## Canonical support majorant from the proved intersection chain

For the actual a put Z=Z(a), and take a generous spherical derivative
constant1000d in the global Green lower bound. Define

    Ccross=Z+Lambda+log(1000d)+(1/2)log(1+a^2),
    Hpi=d*Lambda+(1/2)log(1+a^2)
                    +d[log(1000d)+Lambda+1/2],
    Vpi=d*(Z+Delta),
    Support=d*[A_g*Z+2g^2*Delta+Theta+(g/2)log(2pi)+F/2+g*Ccross]
                    +g*[d*Lambda+Hpi+Vpi].

Then the finite/analytic chain in SURFACE_TORSION_HEIGHT_CHAIN.md bounds
sum_(Q in D_t with multiplicity) h(pi(Q)) by Support. The formula deliberately
overcounts the nonnegative cross/contraction terms. It retains the book's
actual -[D.(D-omega)]/2 sign, TWO distinct pole/Green contributions, and
log(2pi). It applies to torsion classes and unique canonical D_t with all
specified support exclusions. It does not claim a height bound for arbitrary
representatives or for a basepoint whose height was omitted.

All quantities are polynomials with fixed exponents in d,g,hB,log(1+a).
For fixed r and g=O_r(d) this is the effective version of the loose d^9*S
support envelope. A simpler larger power bound can be used, but is unnecessary.

## Closed coordinates without an unnamed jet constant

Let Fplane(x,y) be the known GLOBAL rational monic plane equation restricted
to a component, of total degree D. Fix an integral representative of its
coefficient vector and compute upper bounds on its affine coefficient
height and number of monomials. Put C_F=h([1,coeff(Fplane)])+log max(1,number of monomials)+log2.
The monic Cauchy root bound after specialization gives h(y)<=D h(x)+C_F.
Thus H=(D+1)Support+g*C_F explicitly bounds the sum of
multiplicity-weighted h(x)+h(y). It is enough to use this same H as an upper bound on EVERY
individual support point's coordinate-height sum; this weakens the bound
only polynomially. The actual model coefficients, not intrinsic theta data,
pay the coordinate change.

For eta=F_y-c F_x and V=F_y partial_x-F_x partial_y, compute the polynomial
recurrences separately for f=x,y:

    P_1=F_y or -F_x,
    P_(n+1)=eta V(P_n)-(2n-1)P_n V(eta), 1<=n<g.

They have degree<=2nD and polynomial coefficient bit size (each step adds
two fixed F/eta factors, not a square of the previous P_n). The polynomials
have only two variables, so constructing this formal recurrence is itself
polynomial. Their exact coefficient bit lengths give explicit majorants
B_n, with no unknown constant. For a polynomial P of degree e and M terms,
use h(P(Q))<=h_aff(P)+eH+log max(1,M). Denote this bound by Eval(P).

Each normalized Taylor coefficient is bounded by

    Jet_n=Eval(P_n)+(2n-1)Eval(eta)+log(n!), n>=1;
    Jet_0=H.

If P_n is identically zero its contribution is zero. Nonzero eta values are
guaranteed by the already checked residue condition; h(eta^-1)=h(eta) pays
all small denominators. A coarse joint jet bound is
J=2g^2*max_(f=x,y,0<=n<g) Jet_n.

Use Hz=g[H+log(1+|c|)+log2]. Confluent interpolation then gives the explicit
closed-encoding majorant

    Hclosed=(Hz+g log2)+(g Hz+g^2 log2+J+log(g!)).

The first term bounds A; the second bounds the shared-denominator vector
of B,C via Cramer's rule. These are intrinsic absolute heights: a splitting
field may be used in the proof but its degree does not multiply the bound.
Nonsplit and nonreduced divisors are included. A coordinate denominator from
the monic transformation is treated by the same known polynomial evaluation
and inverse-height rules after its residue unit check.

## Rational reconstruction threshold

The fibre-point bound is Hfib=(D+1)log(a)+C_F. Add this, each actual
closed-coordinate bound as needed, and the height-zero cyclotomic entry
to bound every scalar in the all-pair encoding by Henc. Let N_S=|Gamma|ell^m,
q be its known tuple length and u the chosen integer separator. Put

    Halpha=q Henc+q^2 log(u+2)+log(q+1),
    Hlambda=3(N_S-1)Halpha+2(N_S-1)log2,
    K=N_S^2*(Halpha+2Hlambda)+2log N_S+N_S*(Halpha+log2)+1.

This dominates the product polynomial and all UNARY/BINARY operation and
Boolean relation coefficients used here. The actual signature has maximum
arity TWO: product, equality, unary maps and constants. For an extension with
explicit maximum arity k>=2 replace K by

    K_k=N_S^k*(Halpha+k Hlambda)+k log N_S+N_S*(Halpha+log2)+1.

Unspecified fixed arity is not itself a numerical justification for K. Global equivariance
proves they are rational; auxiliary separation proves their denominators are
P-units. Let Kint>=1 be an integer upper bound for K (or K_k),
s=floor(log2 P), T=2^(2Kint), and e=floor((4Kint+1)/s)+1. Then
T>=exp(Kint) and P^e>=2^(s e)>2T^2. These known bounds pay every precision digit. Semistable models,
complex atlas evaluation and global torsion splitting fields are not inputs.

## Partial analytic audit disposition

The Claude analytic-constants request ended max_tokens with a NONEMPTY partial
report, not a completed review. Parent read all retained text. Its valid
domain correction is applied above: v must avoid B, and v0 already pays r
excluded values. Its independently checked Whitney counts agree with the
source proof. The report stops during the density calculation, so its opening
claim to have audited later constants is not used as evidence. The earlier
complete internal proof remains authoritative; completed arithmetic precision review independently supplies the remaining
derivations below. No retry.

## Completed arithmetic audit disposition

The completed OpenAI arithmetic-precision report (544 lines), fully parent-read,
rederives the actual nonminimal Z, Wronskian, Faltings/theta/minimal-node,
finite contraction/current, global Green and book9.2.5 support bounds. It
preserves the negative one-half sign, degree d versus g factors and both
pole/Green contributions. Accepted explicit additions above: monic root-height
H/Hfib, maximum-arity qualification and integer-only precision rule.

The jet identity D_z^n f=P_n/eta^(2n-1) follows by one differentiation;
normalized confluent rows binom(j,n)z_i^(j-n) have determinant product of
(z_j-z_i)^(m_i*m_j), no factorial denominator in that matrix. Shared Cramer
heights and global equivariance respectively pay rational size and rationality;
residue-unit separation separately pays P-integrality. Root checked these
distinctions. All component coordinates must be covered by Henc/q; the report's
one-divisor shorthand is not permission to omit components.

This closes only the specified height-to-precision bridge with positive genus,
regular integral a, unique supported divisors, actual global plane coefficients,
unit eta/cyclicity/separator and correctly aligned finite-flat residues. It
does not replace the independently charged geometry, model, or lifting proofs.
No semistable extension, analytic atlas, or splitting field is computed.
