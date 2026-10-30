# Removing The Extra Common-Field Promise For Elliptic Inputs

2026-10-25. Deduction from standard supersingular Frobenius classification,
with exact twist controls. Independent review pending; not a new isogeny
algorithm and not an implementation of field embeddings or theta geometry.

## Result And Scope

Let E and E' be the actual supplied supersingular elliptic curve models over
ONE explicitly represented field k=F_q, q=p^s, p>3. Without knowing phi,
passing to k_star=F_(q^12) guarantees:

1. Both endpoint Frobenius endomorphisms equal [q^6].
2. Every geometric homomorphism E->E', including the unknown phi, is defined
   over k_star. All geometric endomorphisms of each endpoint are also defined.
3. Full 8-torsion of both curves and their products is k_star-rational.
4. Every prime-to-p subgroup of those products is k_star-stable. Quotients
   retain the SAME scalar Frobenius, and geometric homomorphisms between
   such intermediates descend over this fixed field.

Consequently the separate promise that phi and the full source order are
defined over a supplied common field is unnecessary for the E->E' branch
and its phi x phi construction. The source order must STILL be supplied and
efficiently evaluable. Being defined over a field does not construct a map,
recover its rational functions, or provide a missing endomorphism basis.

This applies to native-membership-baseline-2026-10-25 and the doubled-elliptic
application of double-level-source-2026-10-25. It does NOT remove the field
promise for an arbitrary supplied surface B merely because B is geometrically
isogenous to E^2. Such a surface needs its own Frobenius analysis. Original
notes and receipts remain unchanged; this is an explicitly scoped successor.

For the common input k=F_(p^2), use F_(p^24). The degree-12 relative extension
is a conservative universal bound, not a claim of minimality for each pair.
If the two curve models begin in different fields, first construct and charge
a common field with explicit compatible embeddings. No identification of
coefficients up to Frobenius/Galois is permitted.

## Proof

The necessary trace classes for supersingular elliptic curves in p>3 are
t=0 when s is odd, and t=k*sqrt(q), k in {0,+/-1,+/-2}, when s is even.
See the classification used and derived into scalar powers in
[Morrison--Panny--Sotakova--Wills, Lemma 2.2](https://arxiv.org/html/2501.16321v2#S2.SS2).
The needed statements are about ACTUAL Frobenius, not a formal companion
matrix with a repeated characteristic root.

- If t=0, pi^2=-q, so pi^12=q^6.
- If k=1 or -1, the quadratic relation gives pi^3=-q*sqrt(q) or
  +q*sqrt(q), respectively. Fourth powers give pi^12=q^6.
- If k=2 or -2, (pi-k*sqrt(q)/2)^2=0. The division algebra End^0(E)
  has no nonzero nilpotents, hence pi=+sqrt(q) or -sqrt(q). Again pi^12=q^6.

Thus every endpoint has the SAME positive scalar Frobenius over k_star.
For a geometric homomorphism u, Frobenius naturality gives

    pi_target*u = u^(q^12)*pi_source.

Since both pi are [q^6], surjectivity of this scalar map forces
u^(q^12)=u. Cancellation uses surjectivity, not separability: p divides q.
This proves definition over k_star without knowledge of u.

Because q is odd, q^6=1 mod 8. All 8-torsion is fixed. Scalar Frobenius
preserves every subgroup, and naturality with a surjective quotient map
shows that every quotient also has Frobenius [q^6]. Repeat the same descent
argument for homomorphisms between intermediates. The existing theta-model
representability and quotient primitives still have to be imported/executed;
this argument only fixes their field and level-8 hypotheses.

The necessary trace classes include some that do not occur for a particular
p; testing all classes is an overinclusive algebra check, not fabrication
of curves with every listed trace. The planner does not itself test whether
a supplied curve is supersingular.

## Why Six Is Not A Universal Fixed-Endpoint Bound

Use F_121=F_11[u]/(u^2+1). Exact point counts and Hasse-invariant checks give:

    E1: y^2=x^3+(1+u)x,     #E1(F_121)=122, t1=0;
    E2: y^2=x^3+(1+2u),     #E2(F_121)=111, t2=11.

Both curves are supersingular. Over F_(121^6)=F_(11^12),

    pi1^6=[-11^6],    pi2^6=[+11^6].

Each curve separately has all geometric endomorphisms defined, and every
kernel subgroup is stable. But there is NO nonzero homomorphism between
these FIXED endpoint models over that field: Frobenius equivariance would
give [2*11^6]u=0, impossible for a nonzero isogeny. Over F_(121^12), both
scalars are [+11^12]. This is a genuine small-field countercontrol, not an
arbitrary formal matrix pretending to be a supersingular curve.

This distinction matters when reading claims about definition fields.
[Orienteering with One Endomorphism, Lemma 2.2](https://pmc.ncbi.nlm.nih.gov/articles/PMC10533648/)
prints an F_(p^12) bound; the SEA paper also discusses degree-six fields in
its kernel/normalized-isogeny setting. Do not import such wording as an
unconditional guarantee for arbitrary fixed twisted endpoint models. The
control above falsifies that interpretation. It does not contradict the
bounded definition field of a kernel or a quotient with a freely chosen
normalized codomain. Original conventions and cited proofs need review
before drawing a broader conclusion about the papers. No external erratum
or novelty claim is made here.

## Resource Contract

One degree-12 extension increases the represented base size by a constant
factor. Finite-field construction and embedding algorithms remain charged;
no hidden-isogeny coefficients are extracted as part of this step.

For a prime-only weak level r!=p, scalar q^6 on torsion gives extension bound
r-1 over k_star. For r^2 use r(r-1). These are polynomial in the SMALL public
auxiliary primes selected by the source plans. Construct each auxiliary
field separately over the SAME embedding of k_star, and never form their
compositum. Thus the earlier uniform prime plans remain polynomial in paid
input length, including the additional constant factor twelve in base degree.

The weak evaluator must still work on these actual extension-field points,
with one genuine global phi and one common unit scalar per order. Missing
weak evaluations, zero masks, unrelated maps per level, or missing embeddings
are not repaired by this field theorem. Neither are the unpublished source
proof, coherent compilation, practical dimension-16 costs, or novelty gap.

## Verification And Handoff

elliptic_fields.py implements symbolic scalar-power accounting, a field-size
plan, and the two actual curve controls using SymPy's finite-field arithmetic.
The formal companion-matrix falsifier guards against mishandling t^2=4q.
No actual large extension, unknown isogeny, theta model, or coset source was
constructed. Tests and replay must retain those scope flags.

After the main checkout is stable, Gemini can attach the successor note to
the elliptic source's input contract. Do not overwrite the general surface
contract or old hashed receipts. The highest-value next question is still
the full large-prime source/application comparison and geometric leakage,
not more field-size optimization or smooth-degree demonstrations.
