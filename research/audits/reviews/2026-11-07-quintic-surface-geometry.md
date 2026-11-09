# Quintic surface P2: closed geometry/source delta review

2026-11-07. Selection B is the exact FULL P2 polynomial of ANY smooth
QUINTIC SURFACE in P3/Fp, with degree fixed and binary input. Read updated
STATE/TRAPS and the retained actual primary passages below. Interpreter
`/opt/anaconda3/bin/python`; no Git/network/API, implementation or new tests.

**Verdict: CLOSED/PASS for the geometry and source delta.** The previous
quartic torsion-cover construction applies with the replacements proved here.
Every chart dimension remains an absolute constant. This is not a fresh proof
of the separate modular induction/twisted-trace extraction, a uniform theorem
in growing surface degree, a classical lower bound, novelty or execution.

## Numerical and cohomological replacements

For a smooth quintic X, H^2=5 and K_X=H. From
`c(T_X)=(1+H)^4/(1+5H)` one gets `c2(X)=11*5=55`.
Complex integral Lefschetz gives simple connectedness and H1 in homology=0.
Universal coefficients give torsion-free H2 in cohomology, and Poincare
duality gives H3=0. Thus `b2=55-2=53`.
Lifting the defining coefficients to integers gives a smooth characteristic-
zero fiber: smoothness modulo p ensures the discriminant is nonzero. Smooth
proper base change imports the free rank53 Z_ell cohomology for EVERY
ell!=p. No Tate conjecture or unknown exceptional-prime set is used.

Use the SOURCE-PAID cubic-Veronese Lefschetz pencil, as in the previous
geometry review and `surface_torsion_selection/surface_p1.txt`883–928.
For its divisor D=3H,

`D^2=45`, `D.K_X=15`, `g=1+(45+15)/2=31`, `r=2g=62`.

The transverse base scheme has degree45. Blowing it up gives Euler number
55+45=100; subtracting `2*(2-2*31)=-120` gives220 ordinary nodal fibers
(geometric count, or sum of degrees of closed bad points).

Each singular Lefschetz fiber is geometrically irreducible. Otherwise the
connected reduced curve with exactly one ordinary node has D=A+B and
A.B=1. Choose the smaller positive degree `a=H.A`, so1<=a<=7. Then
`A^2=D.A-1=3a-1`, whereas Hodge index gives `A^2<=a^2/5`. This would force
`a(15-a)<=5`, impossible on that interval (its minimum is14). Nonreduced
fibers are incompatible with the ordinary-node condition. This argument does
not assume K_X=0 and therefore survives the K3-to-quintic change.

The primitive vanishing-cycle/nearby-cycle proof is unchanged: one component
makes H2(special)->H2(generic) an isomorphism, so the vanishing evaluation is
primitive. Picard-Lefschetz therefore identifies specialization with inertia
invariants after reduction for EVERY ell!=p. Thus R1 pi_*Fell=j_*V, R0 is
constant, and R2 is Tate. Euler Leray needs no degeneration and gives

`P2(X,T) P_base(pT)=(1-pT)^2 L_P1(j_*V,T)`.

Here P_base is the actual degree45 finite scheme's Frobenius polynomial,
not45 assumed rational points. Arithmetic V is the contragredient of raw
Jacobian ell-torsion, with the arithmetic/geometric Frobenius conventions
already fixed in the prior review. Full GL frames retain all arithmetic data.

On U=P1 minus220 tame punctures, Hc0=0 and
`dim Hc1-dim Hc2=62*(220-2)=13516`, `dim Hc2<=62`.
Therefore the safe rational-function degree guards become numerator<=13578
and denominator<=62. Weil gives `|c_i|<=binom(53,i)*p^i`, so centered CRT
modulus `>2^54*p^53` suffices. Retaining ell>53 is a conservative cutoff;
it is NOT justified by an alleged need for division in mod-ell Newton
identities, since the repaired readout uses characteristic-zero Newton.

## Uniform construction: all fixed-size hypotheses survive

The generic curve is now a smooth COMPLETE INTERSECTION (5,3) of degree15.
The bounded-bias surface-point finder must factor QUINTIC line restrictions,
not quartics. Its noncontained intersections have at most5 rational points.
A line on X has normal bundle O(-3), by adjunction from K_X=H; hence it has
no tangent deformations, and the Hilbert scheme of lines is zero-dimensional.
Its fixed-degree Grassmannian equations bound its size uniformly. Contained
lines contribute only O(p^-3) to expected incidence, while total expected
incidence is `#X(Fp)/(p^2+1)=1+O(1/p)`. Rejecting contained lines leaves
constant success probability. Choosing a root has only bounded bias.
The pointed-pencil incidence argument and exact nodal/transversality tests
then provide a rational section P0 with the previously paid finite clocks.

Set `d0=2g+1=63`, `D0=d0 P0`, `L=O_C(3D0)`, `deg L=N=189`.
The Khuri-Makdisi membership/addition hypotheses continue to hold. To impose
or compute the canonical reduced representative, use
`D1=D+d0P0` of degree126 and `D2=(2d0-m)P0` of degree95..126,
for0<=m<=31. The Riemann-Roch upper bound is EXACTLY
`N-2g-1=189-62-1=126`.
Relevant original locators are `khuri_makdisi_divisors.txt`815–851,
1024–1030 and1252–1275. The unique-minimal-divisor argument remains
`surface_p1.txt`377–384; the positive-dimensional raw divisor representation
must still be canonicalized before torsion elimination.

For preprocessing, a hyperplane section is P0+B with degB14, and section
spaces through H0(3L) require s<=567. They are still fixed-size kernels in
the (5,3) coordinate ring, with vanishing on sB imposed before dividing by
the hyperplane equation to power s. Every size, degree and initial t-height
is a CONSTANT independent of ell,p. The finite rank/minor charts, flattened
O(log ell) multiplication atlas, fixed-variable elimination and determinant
t-height bounds therefore remain polynomial in ell,log p. There is no new
Jacobian, torsion or group-law oracle.

The reduced torsion algebra has rank ell^62. Its62-fold tensor algebra has
rank ell^3844; the independent-frame locus is the GL62(Fell) torsor, of
degree<ell^3844. Evaluate all ell^62 coefficient relations separately, using
the ambient-algebra idempotent method and flattened rational formulas, as
before. Do not branch simultaneously over every relation or replace the full
arithmetic torsor by a supplied geometric monodromy group.

All explicit elimination, radical, t-height and safe-characteristic bounds
must be RECOMPUTED for these fixed constants. The existing enlarged safe-p
envelope/direct-count fallback applies: if p is bounded by the resulting
fixed polynomial in log p, direct counting through extension degree53 is
still polynomial(log p), with a huge fixed exponent. No numerical quartic
envelope is copied without substitution.

Semistable nodal monodromy remains tame for ell!=p. Riemann-Hurwitz now
gives each geometric component genus at most `1+109*|GL62|`. Boundary and
constant fields can use `lcm(1,...,220)*|GL62|`, or the previously specified
safe polynomial multiple for twists. This uses the arithmetic frame-torsor
structure, not an exponential lcm of arbitrary factor degrees. Explicit
Kozen normalization/local-parameter output, semilinear twist descent,
component constant-field extraction and geometrically irreducible Kedlaya
inputs are unchanged, with these larger fixed ranks. No extension of degree
exponential in ell is introduced.

## Actual Kuga–Satake/Hodge scope

The stronger source is `quintic_surface_selection/schnell_mumford_tate.txt`:
Definition3 at473–481 defines “expressed with the help of abelian varieties”
using rational Hodge structures, sums, tensors, summands, H1 of abelian
varieties and Tate structures. Lemma5 at492–522 restricts the Lie-algebra
Hodge types of every such structure to(-1,1),(0,0),(1,-1). Lemma6 at530–547
shows extra(+/-2,-/+2) types when h20>1. Lemma7 at554–590 supplies the full
orthogonal algebraic monodromy for smooth surfaces of degree>=4. Theorem1
at595–606 explicitly states that the primitive H2 of a VERY GENERAL complex
surface of degree>=5 cannot be expressed with abelian varieties.

Use `V=H2_prim(X,Q)(1)`, rank52 and type(1,-1)^4,(0,0)^44,(-1,1)^4.
The connected orthogonal Lie algebra is so(V); its(+/-2,-/+2) pieces are
nonzero (each has dimension binom(4,2)=6). This suffices for Schnell's
obstruction. His loose displayed MT=O is not needed: MT is connected and
the proof only needs its orthogonal LIE ALGEBRA/connected SO52. The original
monodromy authority is now actually opened:
`deligne_weil_ii.txt`4119–4140/Theorem4.4.1 gives the finite-or-dense/open
alternative;4281–4299/Theorem4.4.9 describes the finite root-system case.
Schnell577–590 identifies the precise Deligne reflection-group lemma used.

This is a genuine obstruction to a HODGE-COMPATIBLE generic abelian-generated
replacement of quintic primitive H2; it is stronger than merely observing
that the usual spin construction is not weight1. It is NOT a theorem about
all surfaces over Fp, a point-counting lower bound, exclusion of special
abelian-type quintics, or impossibility of every classical algorithm.
`patrikis_generalized_ks.txt`36–52 and127–147 distinguishes ordinary abelian
Kuga–Satake from general conjectural motivic lifting; its special examples
229–245 do not supply a universal quintic abelian algorithm. The earlier
Fu–Vial shorthand is no longer needed as the main source authority.

`newton_strata_2026.txt`132–151 describes current Kedlaya-type/controlled-
reduction practice, including its p dependence;912–935 treats QUINTIC
SURFACES and reports computational costs for those experiments. These are
current motivation/baseline scope, NOT a source for a classical poly(log p)
algorithm or a lower bound against one.

## Fixed-degree formula record, not another admission

For the same cubic-pencil setup on a smooth degree-d surface in P3,
`g=1+3d(d-1)/2`, `b2=d^3-4d^2+6d-2`, `base=9d`, and
`nodes=d(d^2+2d+9)` follow from adjunction and Chern/Euler formulas.
This records the algebraic substitutions and avoids repeating nearby-degree
passes. The construction is NOT claimed polynomial uniformly in d: rank,
frame degree, chart dimensions and elimination exponents grow rapidly with d.
No d=6 variant or new backend is implied by this record.
