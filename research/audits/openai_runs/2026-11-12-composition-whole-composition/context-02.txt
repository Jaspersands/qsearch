# Native cover presentation: exact admitted interfaces

2026-11-12. Constructive CLASSICAL surface comparator. This note records two
independently reviewed bridges. Native atlas, actual normalized frame and
downstream coordinate reconstruction remain separate until proved.

## Unmarked level cover from a supplied bounded Jacobian atlas

Fix fibre genus a and atlas type tau: projective ambient dimension, equation
count/degree, complete addition chart count/bidegree. Supply the actual
RADICAL ideal on every affine patch, identity, and coefficient t-degree T
and logarithmic height B over Q(t). Promise full geometric Sp_(2a)(F_ell)
monodromy for odd prime ell and the original principal polarization.

Then an unmarked splitting cover over Q(zeta_ell)(t), its ordered torsion
basis coordinates, base map, and deck generators have a deterministic
construction with degree, logarithmic height, bit cost and dense output
bounded by (2+ell+B+T)^C_tau. No family-dependent fixed-curve constant or
unpaid t-degree is hidden in the bound. Review:
audits/reviews/2026-11-12-surface-level-cover.md.

Expanded binary multiplication charts use the SAME parent chart for both
arguments of doubling. O(log ell) levels give polynomial counts/degrees/
heights in numerical ell. Impose identity cross-products for ALL charts;
completeness and etaleness of [ell] produce the reduced torsion scheme.
Pila's fixed-variable membership bound gives an explicit polynomial-size
coefficient matrix whose kernel/intersections construct the finite algebra.
Ratios of its minors bound t-degrees and heights in characteristic zero.

Take the fixed tensor power for ordered bases and exclude all nonzero
linear relations by support idempotents in the ORIGINAL algebra. A bounded
primitive-element search and cyclotomic/LLL-Hensel factorization then produce
components. Any basis generates the same splitting field. Over the cyclotomic
base, arithmetic image is contained in Sp and contains geometric Sp, hence
equals it; each component degree is |Sp|. Deck maps are computed by changing
the basis and testing the defining factor, with one common coefficient field.

The invariant alternating form is recovered only up to E=cB. ONE certified
nonzero Weil-pairing value fixes c and normalizes the universal frame. This
marking scalar is not a permission to choose the arithmetic Frobenius scalar.
Radicality is substantive: z²=0 cannot replace z=0 just because geometric
point sets agree. Fixed-variable elimination is valid only at the fixed fibre
genus; the auxiliary cover genus grows and requires separate algorithms.

## Native bounded atlas for the actual genus-31 fibre

The atlas input is now constructed for a smooth complete intersection
(5,3) in P3 over Q(t), with FIXED ambient/projective/parameter degree and
coefficient bit size B. The independent proof and advisory-report
dispositions are in audits/reviews/2026-11-12-native-jacobian-atlas.md;
the parent checked the complete proof and actual Anderson source.
Output type/degrees are format constants, coefficient heights O(B+1),
and bit cost polynomial in B. No rational curve point or field extension
is supplied. The constants are enormous; no practical claim follows.

A fixed resultant grid chooses a basepoint-free degree-15 hyperplane
pencil. At most90 values ramify. Among0,...,1875 choose1786 etale closed
fibres: five form reduced E of degree75, the other1781 give an evaluation
algebra of degree26715. Here n=h0(E)=45. The complete-intersection Koszul
resolution computes every needed RR space L(kE) by fixed-size linear
algebra; a finite-etale trace pairing supplies Anderson's compression
functional over Q(t) for ALL divisor classes simultaneously.

The source's abeliant is an integral universal polynomial of degree2n.
Every Jacobi discriminant has per-slot poles <=(8n-4)E, total26700.
Evaluation at26715 geometric points is therefore injective for every
discriminant. Tensor the CLOSED evaluation algebra rather than splitting
its support, apply every source permutation formula, and expand its
coefficients in a Q(t)-basis. At every pair each split component is zero
or on the SAME correct sum line, so every nonzero coefficient vector is
a valid addition law and these vectors cover EVERY geometric pair.
One explicit addition bidegree is(28350,28350).

Raw Jacobi equations are not assumed radical. Fixed-format elimination,
generic finite-algebra trace radical, contraction and saturation produce
the true radical projective ideal. A Poincare-family construction over an
algebraic closure gives an actual morphism Pic0->J_red; the complete atlas
makes J_red a smooth group variety. Proper bijectivity in characteristic
zero then gives an isomorphism, which descends by its naturality. A
geometric basepoint used in this proof is NOT an algorithmic input.

This pays the native atlas for this fixed-format family only. It does
not pay growing-genus auxiliary-cover normalization, arbitrary special
fibres/primes, normalized Weil pairing, or arithmetic reconstruction.
The genuine pairing/frame obligation remains in the native-completion
dispatch. Polynomial torsion-cover presentation follows by composing
with the supplied-atlas theorem under its full-monodromy promise.

## Arithmetic action from a genuine full similitude-frame scheme

Now supply the GENUINE frame torsor with evaluation into the original
L=J_fibre[ell]=R1 f_*mu_ell over Fq, with full geometric Sp monodromy and
nontrivial transvection inertia at r punctures. All presentation sizes are
charged. Gamma=GSp_n(F_ell), N=F_ell^n constant, S=N^vee. A frame is
(c,zeta), e(cu,cv)=zeta^(u^T Jv), with RIGHT action

    (c,zeta).g=(c g,zeta^lambda(g)).

Evaluation identifies the associated sheaf T x^Gamma N with the ACTUAL L.
All right deck maps commute with arithmetic Frobenius; N being constant does
not make L constant. Cartan--Leray on the disconnected torsor has H0 a
permutation module. Shapiro and central -I kill its group-cohomology
obstructions. Norm-zero transvection inertia makes the compact Hom equal
the OPEN cohomology Hom, not the parabolic part. Hence

    Hom_Gamma(N^vee,H1(C_full,mu_ell)) = H1(U,L)(1),
    dim = (r-2)n.

Independent review: audits/reviews/2026-11-12-surface-full-similitude.md.
Apply q^-1 to the output matrix for arithmetic Frobenius on H1(U,L), or
q^-2 for L'=R1 f_*F_ell. Geometric Frobenius is the inverse matrix.
Do not confuse Galois action on divisors with inseparable morphism pullback.

Write A(g)=R_g^* (LEFT), P(g)=(R_g)_*=A(g^-1) (RIGHT). On one component
W0=Hom_Sp(S,J_C0[ell]), the exact pushforward equations and operator are

    phi g^T=P(g)phi,
    F_W(phi)=P(g_q^-1) sigma_q phi g_q^T,  lambda(g_q)=q.

Changing g_q by any Sp element, including -I, cancels exactly; no unknown
scalar survives. The transformed origin must be included on BOTH divisor
parts. Other cyclotomic components are DECK TRANSLATES, not necessarily
Frobenius conjugates; one component's zeta is sufficient for that reason.

The native-module algorithm applies over ONE field: first cyclotomic degree
ord_ell(q), then the charged regular-fibre avoidance extension and ONE
residue point of degree<=|Sp|, then the universal primary-killing extension.
Full primary multiplicities and pairing rank certify completeness. Costs
remain poly_(n,r)(ell, NUMERICAL P, presentation size, log1/eta), not polylogP.
No support splitting or lcm of separately chosen component fields is used.

Falsifiers include wrong torsion/frame dimensions, failed deck identities,
incorrect pushforward convention, failed exact Frobenius transport, or
omitted factors of the full frame fibre. A single factor's constant field
does not certify full geometric monodromy. Genuine native frame/evaluation,
inertia promises, parabolic filtering, arithmetic model, heights and
reconstruction are still required. No complete comparator or separation
follows from these two interfaces alone.

## Native normalized pairing and full frame now constructed

Parent read all of audits/reviews/2026-11-12-native-normalized-frame.md.
For the original fixed (5,3) curve, Anderson3.7.2 specializes a Jacobi point's
46 slots to a true Segre matrix over a tower with each degree<=15. Two points
fit ONE common extension of degree<=15^92, a fixed format constant. A nonzero
ROW's common section-zero divisor as O(2E) sections has degree75 and class
E+t. Include support on E and multiplicities; the COLUMN has the opposite sign.
Thus actual divisors for the two original points exist constructively over
this one field; no inverse-Abel, rational-point or Brauer-obstruction advice.

Complete-intersection section spaces L(kE), closed jet constraints and
fixed-variable ideal membership compute RR, move the divisors disjoint, and
find principal functions. Choose denominator sections nonzero on the other
divisor to avoid a displayed 0/0. Evaluate functions by multiplication
DETERMINANTS on closed Artin algebras, retaining multiplicities and the
F-valued answer (not an accidental further norm to Q(t)). Direct polynomial
product and ratios-of-minors bounds pay t-degrees, coefficient bits and all
field arithmetic. Actual Couveignes convention is e(delta,epsilon)=g(delta)/
f(epsilon), where div f=ell delta, div g=ell epsilon.

The answer lies in mu_ell of the original field by functoriality; compare
with all known powers of zeta, no discrete-log oracle. One such pairing fixes
the scalar of the invariant alternating form. Symplectic Gram-Schmidt on the
ACTUAL basis selects the whole genuine normalized Sp-frame factor. Regarding
that same field as a Q(t)-algebra with zeta coordinate, rather than taking
Weil restriction, gives the full GSp frame of degree |GSp|. Changing a frame
by g also changes zeta to zeta^lambda(g); tautological evaluation into the
original Jacobian is retained. This pays the formerly missing arithmetic
scalar linkage. The optional norm-back divisor route works for ell>15 because
each tower degree<=15; pairing itself needs no such coprimality restriction.

Intrinsic composition at p is separate from formula quality: the smooth
original relative Jacobian over U_Zp has finite etale ell-torsion and genuine
frame/evaluation when p!=ell. The constructed GENERIC object is identified
with this functor, hence has its intrinsic etale extension even if the chosen
rational equations invert p. This does not construct good target-p formulas.
Target arithmetic instead uses SURFACE_FINITE_ETALE_RECONSTRUCTION.md.
