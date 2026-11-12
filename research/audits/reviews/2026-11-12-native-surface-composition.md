# Native quintic point counting: whole-composition review

2026-11-12. Independent review of
`SURFACE_CLASSICAL_NATIVE_RECONSTRUCTION.md`, starting from current
`STATE.md` and `TRAPS.md`. This is a review of the native claim, not another
review of a supplied finite-orbit algebra. Read the linked main construction,
height, numerical, finite-etale and boundary notes, the stable 806-line
reconstruction review, and the completed native-pencil-monodromy and
boundary-determinant reviews. Rechecked the relevant actual Deligne, Hall,
Pila2005 and Merkl/Javanpeykar source statements and effective inequalities.
No Git, network, API, archives, implementation or numerical experiment.
Commands used `/opt/anaconda3/bin/python`. Parent owns shared-state changes.

## Decision and quantifiers

ACCEPT the mathematical composition. With the proved native interfaces
included, there is no further supplied-input condition in the stated
prime-field, fixed-degree problem. In particular I found no first unpaid
input between native coefficients and the final integral polynomial.

Precisely, there is a classical randomized algorithm and computable absolute
constants C,c, depending only on the fixed quintic/cubic-pencil formats, such
that for EVERY prime p, EVERY smooth quintic X/F_p supplied by its binary
coefficients, and 0<eta<1/2, it runs in at most

    C (1+B+log(1/eta))^c

bit operations and returns the exact degree-53 integral P2 with probability
at least 1-eta. Capped failure is reported as FAIL, never as a partial module
or guessed answer. If an always-returning bounded-error formulation is
desired, replace FAIL by a fixed dummy output. All geometric hypotheses
used below are derived or certified from the input, not additional promises.

This is an algorithmic existence/proof conclusion, not a claim that the
construction has been implemented, practically timed, or made usable. Its
exponents are enormous and are not bounded by the output degree 53. No
novelty, hardness, separation or quantum-execution claim is implied.

## 1. Native geometry really supplies the cover hypotheses

The pencil search does not require a specially supplied or recognizable
monodromy basis. A cubic section of the embedded surface separates second
jets at one point and first jets at two distinct points. For the latter,
multiply a linear form nonzero at the first point and zero at the second
by itself, then multiply by arbitrary linear forms; reverse the points for
the other jets. These degree-three sections independently prescribe the two
first jets. Quadratic local monomials, homogenized to degree three, prescribe
the single second jet.

Consequently, in odd characteristic, the incidence of a singular cubic
section has generically one ordinary node. Degenerate Hessians and two
singular points impose further conditions: second-jet surjectivity and
two-point first-jet surjectivity give the required codimension. A general
pencil avoids those smaller loci and meets the discriminant transversely;
its axis is transverse too. This proves nonemptiness for each smooth input,
not only for a generic quintic.

The equations for these failures have fixed numbers of variables and fixed
degrees. Elimination/Bezout therefore gives a COMPUTABLE uniform bound D_bad
on the degree of a proper bad parameter locus. For p>2D_bad, uniform random
cubic pairs have success probability bounded below by a constant. Fixed-size
elimination certifies the transverse degree-45 base scheme, distinct critical
values, and a single ordinary node at each singular fibre, including infinity.
It does not merely test a few fibres. The small-p branch below pays p<=2D_bad.

Adjunction and Euler characteristic give g0=31, n=62 and r=220. The
irreducibility argument A+B=3H, A.B=1, 1<=H.A<=7 contradicts
A^2=3(H.A)-1<=(H.A)^2/5. Thus every nodal normalization has genus 30.

The completed monodromy review closes the remaining quantifier issue:
Deligne 4.3.3 uses finite coefficients and ALL transported vanishing cycles;
their span is H1 because H1(X,F_ell)=0. Local irreducible-node cycles are
primitive and remain nonzero. Actual 4.2.7, after generic-only 4.2.6, gives
conjugacy of the parameterized integral Picard--Lefschetz homomorphisms for
these fibre-dimension-one pencils. Equality of their rank-one operators gives
integral conjugacy up to sign, hence mod-ell conjugacy. Irreducibility follows.
Hall's actual Theorem 3.1 applies with r_Hall=1 and S0 empty, giving full
Sp_62(F_ell) for every odd ell!=p. There is no hidden input-dependent
exceptional-ell set or additional generic-pencil test.

Lift the certified coefficients to integers in [0,p-1]. The good conditions
are open conditions containing the special point, so they hold over Z_p and
Q. Their fixed-format resultants have coefficient bits O(B); in particular
the degree-220 branch set has absolute logarithmic height hB=O(B). Its total
absolute Galois orbit has cardinality at most 220, including infinity. This
is exactly the branch-height input of the later uniform height theorem.

## 2. Fixed exponents, growing genus, and bit accounting

Put a=31. The full-frame degree satisfies

    d=|GSp_62(F_ell)|<ell^(2a^2+a+1)=ell^1954.

Riemann--Hurwitz bounds the compact component genus by O(r d). The plane
degrees, coefficient bits and deck maps are polynomial in ell,B by the
native atlas/level-cover construction. The atlas type and original fibre
genus are FIXED before ell varies. Expanded binary multiplication charts
remain in the original fixed variables; their counts, degrees and log
heights grow by fixed recurrences through O(log ell) levels. Fixed-variable
membership matrices and their minors then give polynomial bit bounds.
Eliminating a growing collection of unexpanded circuit variables is not
being substituted for that proof.

After the cover genus grows, the construction uses the polynomial-degree
trace-lattice normalization, exact closed-place RR, finite-field torsion,
and KM section linear algebra. It does NOT apply a fixed-genus Jacobian
atlas theorem or fixed-variable Jacobian elimination at that growing genus.
Centered truncated inverse Newton maps and bounded original-matrix minors
pay normalization bits; an arithmetic-operation count is not the sole bound.

The two relevant constant ranks are

    m=(220-2)*62=13516,       R=62*m=837992.

The common primary-killing degree is

    H=ell^ceil(log_ell(max(1,2g))) product_(j=1)^m(ell^j-1)
      <=ell*max(1,2g)*ell^(m(m+1)/2).

Thus it is polynomial in ell,g with a FIXED exponent. The nilpotent bound
uses the ambient dimension 2g, not m. All primary multiplicities and the
Weil-dual union are included. Actual Lauder--Wan zeta work is polynomial in
NUMERICAL auxiliary P, not log P; P itself is paid below. Pairing rank equal
to the independently known primary dimension certifies a complete space
even if a Couveignes trial returns only a strict subgroup. No successful
partial list is used as a complete basis.

Every later rank, tensor square and enumeration is a polynomial in ell,B:
|U|=ell^m, the redundant orbit has size d*ell^m, and the function-algebra
tensor square has the square of that size. Horner/group-law computations
reuse these spaces; no tensor power grows with the number of Frobenius
iterations. A fixed finite composition of these bounds remains polynomial.

## 3. All arithmetic inputs are constructed in the required order

The Anderson construction supplies the actual radical complete Jacobian
atlas, not raw equations with only the correct point set. The divisor and
pairing construction supplies a genuine evaluation frame and its normalized
principal-polarization pairing. The full GSp action is rational. Consequently
the arithmetic coefficient system is the original one, not an arbitrary
scalar-ambiguous realization of a geometric representation.

From a complete Sp-intertwiner basis phi_j on one component, the explicit
full intertwiners have component a

    Phi_(j,a)(v)=P(g_a) phi_j(g_a^(-T)v).

For fixed nonzero s0 in the CONSTANT module S=Ndual, ev_s0 is injective
because a nonzero map from the simple S has zero kernel. It is Galois
equivariant by postcomposition. Hence U={Phi(s0)} is an ACTUAL Galois-stable
rank-m torsion subgroup of the full product Jacobian. It need not be
Gamma-stable; no deck action on U or final Hom restriction is used. This
also avoids concatenating ell-1 independent socles, which would be fatal.

The auxiliary normalization and fixed-pole data produce one integer M of
polynomial bit length before P is selected. Choose P above all known degree,
Wronskian, bad-basevalue, cyclic-coordinate and separator counts and outside
M*ell*|Gamma| and p. There are at most log_2(|M|*ell*|Gamma|) excluded prime
divisors. Effective prime-counting bounds therefore put a good prime in a
polynomial numerical interval. Primality and gcd tests suffice; no varying
integer factorization is assumed.

Freeze the bounded basevalue grid before P; choose its successful a and b
after P by testing ALL relevant classes and component/basepoint translates.
No later b-dependent determinant is appended to M. The regular fibre has
a P-unit discriminant separating polynomial. A rational factor gives the
finite-etale semilocal order Z_(P)[y(b)]. Known-b RR is obtained there from
fixed pole spaces using

    H0(j*pi^-1(a))=(x-a)^(-j)H0(j*pi^-1(infinity)),

thick-fibre idempotents and saturated coefficient kernels. High degree gives
free base change and unit residue minors. This is the explicit anti-circular
repair, not a second unspecified good-prime search.

The numerical divisor conversion is also an actual construction. Reinitialize
the residue KM classes with D0=(2g+1)b and rerun the unique torsion lifts in
that background. Mascot Algorithm 7 through line 5, on x=-t, gives
W0=L((d0+g)b-D_t). Multiply by the known L(A-(d0+g)b), both line bundles
having degree at least 2g+1, to obtain all L(A-D_t) by the section-product
theorem. Residue surjectivity and Nakayama give unit-pivot full-precision
matrices. The enlarged ambient/evaluation bank is charged. One does not use
the false replacement L(F-D) intersection L(F-A)=L(F-D-A), which fails when
D and A meet. The subsequent quotient algebra and x,y multiplication solves
retain nonreduced support and require no canonical ideal/inverse-Abel oracle.

## 4. Height effectivity is sufficient for certified reconstruction

The uniform bounds use LOGARITHMIC hB; Javanpeykar's exponential HB in his
separate stated theorem is not silently relabeled. The retained Merkl proof
works for every compact cover with the stated branch set and a probability
canonical measure. It pays density on the full unit disks and both ordered
transition derivatives. Only logarithmic transition size is charged.

There is no ineffective analytic constant. For example, the stable atlas
proof permits the deliberately loose explicit bounds

    N_charts <= 2^42(r+1)d(d+L),   c1<=d^2,   log M_atlas<=9d,
    Lambda <= 2^60(r+1)d^3(d+L).

For completeness, disjoint Whitney balls of radius rho/16 have per-layer
area at least t^2/1600^2 and total enclosing area at most 36r t^2. Thus
there are fewer than 2^27 r centers per uncapped layer, fewer than 2^29
in the capped layer, and at most 2L+d+10 layers. At r1'=7/8 the displayed
actual Merkl bound is below 2^16*N_charts*d^2. These give the last inequality
and a computable local regularization bound. No numerical chart construction
or optimization oracle is needed for its use as a height inequality.

The product formula gives the effective embedding average

    L_bar <= 1+r(r-1)(2hB+1).

Actual Javanpeykar Proposition 4.2.4/Theorem 4.3.2, together with the
cotangent estimate, bound the height on the SPECIFIC cover-compatible
normalization-resolution by

    hZ(b) <= Lambda_bar+(d+1)r(hB+log(1+a)+1)+2d^2 log d+7.

The same source's explicit point/Wronskian inequalities give polynomial
stable Faltings, stable-node and averaged theta budgets. Field extensions
and semistable models here are existential in a normalized height proof:
division by [K:Q] removes their degree. No algorithm is asked to construct
an unbounded semistable extension. The finite contraction/current lemma
transfers to the relatively minimal model and pays the vertical pole term;
the global Green lower bound pays the polar cross-intersections. Thus the
book's negative one-half intersection term and actual log(2*pi) constants
produce the stated polynomial canonical support-height bound.

The supplied plane coefficients then bound y-values as well as pi-values.
Closed A,B,C heights include tangent inverses, repeated support and confluent
Vandermonde denominators. Their constants can be read from the explicit
derivative recurrences and determinant size bounds; no unspecified
number-field-basis height is used. All needed logarithms may be replaced by
computable larger integer bounds when setting precision.

All-(b,t) encodings use global rational scalar functions and canonical
divisors, so uniqueness makes them globally Galois-equivariant. Auxiliary
Frobenius invariance alone would not suffice. The P-unit separator gives
Lagrange tables with explicitly polynomial rational coefficient heights.
If those heights are at most K, choose T0>=exp(K) and P^e>2T0^2. Then exact
rational reconstruction is unique; e log P is polynomial. This provides
the ACTUAL finite-etale Q-algebra, not an empirically reconstructed candidate.

The relation-idempotent equalizer gives exactly Q[U] and the Hopf maps.
Quotienting before target-prime maximalization removes the basepoint fibre;
that fibre itself need not be unramified at p.

## 5. Original-prime action, boundary and surface determinant

The constructed generic frame is identified with the intrinsic frame functor
of the original relative Jacobian. It therefore extends finite etale over
the ENTIRE U_Zp, including the vertical generic point. Disjoint branch
sections and tame Kummer killing followed by purity give a smooth proper
compactification over Z_p, without ramified base extension. This pays
unramifiedness of U and excludes the ramified-constant-twist counterexample.

The known-prime order algorithm acts on the already reconstructed Q[U].
Its input rank and coefficient bits are polynomial, and its trace-dual and
discriminant bounds pay every iteration in poly(rank,bits,log p). It does
not factor an unknown discriminant or enumerate p elements. Hopf maps extend
to the p-local maximal order. Its reduction is the true coordinate Hopf
algebra. The map a->a^p induces ARITHMETIC Frobenius on geometric points.

Kernel idempotent ranks recover that actual F_U=F_W without a target splitting
field: rank of multiplication by q(F)^*e0 is ell^dim ker q(F_U). Here q(F)
is formed using GROUP addition and scalar maps, not by adding coordinate
F_p-linear matrices. Testing irreducibles of degrees at most the FIXED m
recovers all elementary divisors in polynomial time in numerical ell.

The checked arithmetic identity is

    W = H1(U_base,R1 f_*F_ell)(2).

For a closed node z of degree f, put q=p^f. The geometric boundary is
V_node^dual(-2); arithmetic Frobenius on its twist(2) is F_node^T. Hence
its DIRECT W factor is exactly

    (1-epsilon_z*T^f) P_norm,z(T^f).

Parabolic duality identifies arithmetic Par(2) with geometric Par-dual.
Thus division of det(1-T F_W) by those factors gives the geometric parabolic
polynomial. This holds without semisimplicity or coprimality of factors.
The remaining Leray filtration and blowup identity give

    P2_X(T)=(1-pT)^2 P_par(T)
       / product_(closed basepoints b)(1-p^deg(b)*T^deg(b)).

The degrees are 13516 ->96 ->53. There is no missing embedded-parabolic
subspace extraction or Frobenius transport at this endpoint.

Each nodal normalization has genus 30, a bounded-format degree-28 embedding
in P11, and a residue field of degree at most 220 over F_p. Actual Pila2005
Theorems D/E construct finite complete Jacobian strata for specializations
to ANY field; E removes the divisor input, and F gives the uniform
B1(log q)^B2 algorithm. This is effective fixed-family precomputation,
independent of X,p,ell. Pila1990 for one fixed Q-curve alone would not pay
this step. No growing-genus point-count theorem is being invoked here.

## 6. CRT, all small primes, and the bounded-error clock

Choose distinct primes ell>53, ell!=p, whose product exceeds
2^54 p^53. Effective Chebyshev bounds give a list with largest ell at most
C0(1+log p), with C0 fixed and computable. Enumerating candidates and
primality testing is polynomial in B. Since every geometric H2 eigenvalue
has absolute value p, coefficient k has absolute value at most
binom(53,k)p^k<=2^53 p^53. CRT therefore determines every integer coefficient
uniquely. Torsion-free comparison identifies the computed mod-ell
determinants with these reductions.

Before doing any expensive cover work, take Q to be a computable fixed
polynomial dominating all ORIGINAL-p thresholds, including 2D_bad and
|GSp_62(F_ell)|. Test p against Q(ell_max). If it fails, count X directly
over F_(p^j), 1<=j<=53, and use integer Newton identities. The count costs
p^c0 times polynomial bit overhead for a fixed c0 (for example chartwise
enumeration uses at most a fixed power determined by 3*53). In this branch

    p^c0 <= Q(ell_max)^c0 <= poly(B).

This is a genuine complexity bound, despite enormous exponents; it is not
an unspecified finite-exception table. It includes characteristic two.
If the test passes, every CRT prime satisfies the original-p hypotheses.
Auxiliary P can still depend polynomially on B and ell; there is no demand
that p exceed that separately selected P or its class-count thresholds.

All random calls have explicit success/expected-time bounds and exact
acceptance certificates where completeness is needed. If a primitive has
success at least alpha and expected cost at most T, capping a trial at
2T/alpha loses at most alpha/2 success by Markov. Independent restarts give
failure at most delta in O(log(1/delta)) trials. There are only polynomially
many calls. Allocate eta divided by an explicit polynomial upper bound on
their number and union-bound the failures. Fixed-degree field factoring,
pencil sampling and common-field point sampling are treated the same way;
no unknown expected-time tail is silently made into a worst-case bound.
Successful pairing and RR certificates are never relaxed after a timeout.

The outer number of CRT primes is polynomial, ell_max=O(B), numerical
auxiliary P and all CONSTRUCTED field degrees are polynomial in ell,B, and precision
is polynomial too. The resulting bounded-error BIT bound follows.

## Final scope

No additional geometric genericity promise, exceptional-ell oracle, global
torsion splitting field, noncanonical field-basis height, inverse-Abel
oracle, target coordinate-faithfulness assumption, parabolic projector, or
uncapped retry remains in this composition. Its weakest-looking steps have
explicit replacements: complete pairing rank, genuine full-frame evaluation,
post-P integral known-b RR, source Algorithm7 plus section products, global
equivariant equalizer reconstruction, and quotient-first p-maximalization.

The old false ordinary-compact-Hom equals parabolic assertion remains false.
It is unnecessary because the reconstructed module is OPEN cohomology and
the exact boundary determinant is removed. Accepting this construction
therefore does not rehabilitate that source statement. What is now justified
is the native classical polynomial-bit comparator for the precise fixed
smooth-quintic prime-field problem, with its stated bounded-error contract.
