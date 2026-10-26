# Classical Mask Closure For The Inverse-Trace Relation

2026-10-23. Constructive deductions following the completed independent
review in `independent_review_2026_10_22/`. Independent whole-proof review
is still appropriate. This is a classical attack, not a quantum speedup,
a claim of new combinatorial mathematics, or a hardness result for inputs
outside its scope. Tests check the algebra and implementation separately.

## Decision

Do not propose public changes of coordinates as an automatic repair of the
native inverse-trace candidate. Scalar, translation and Frobenius masks
inherit the review's classical attacks. More surprisingly, independently
random binary-linear masks usually make a simpler attack sufficient: one
binary linear solve using accepted subspaces on the zero-target positions.

At native N=n^2, K=floor(N/8), even n, and z zero targets after public bit
offsets, the masked attack's rank-failure probability is at most

    2^(n*K - n*z/2).

For z near N/2 this is 2^(-Omega(n^3)). This bound assumes independent
uniform masks and a fixed zero support; Section 4 pays for adaptive supports.
Every successful output is checked on the ORIGINAL masked input. A failed
rank test is UNKNOWN, not evidence of hardness or an empty native fiber.

## 1. Public Input And A Deterministic Attack Interface

Let F=F_(2^n) be given by a verified field presentation. Let H be a public
K-by-N matrix over F with every K columns independent. The original
Vandermonde matrix on arbitrary distinct supplied points has this property;
the argument is not restricted to those particular column normalizations.
An arbitrary public syndrome s in F^K is allowed.

At coordinate i supply an invertible binary-linear map L_i:F->F, an
element c_i in F, and a bit delta_i. The requested original relation is

    Hx=s,
    Tr(inv0(L_i(x_i)+c_i)) + delta_i = b_i,   for every i.

All additions in the predicates are binary; inv0(0)=0 is part of the
contract. The masks are explicit binary matrices, not hidden advice or
oracles. Write e_i=b_i+delta_i and Z={i:e_i=0}.

Assume an explicit m-dimensional binary-linear subspace W of F is known
to satisfy Tr(inv0(w))=0 for EVERY w in W. For even n, take the subfield
W=F_(2^(n/2)), so m=n/2. Compute its basis by binary elimination on the
Frobenius fixed-space equation, or from the image of x->x+x^(2^(n/2)).
Trace transitivity proves the predicate on the whole subspace; a finite
spot check would not certify it. No table of 2^n field elements is used.

Choose t with Tr(inv0(t))=1 by inverting a trace-one basis element.
Initialize

    x_i^0 = L_i^(-1)(c_i + e_i*t).

Every initial coordinate already has its requested bit. For i in Z the
entire affine space x_i^0 + L_i^(-1)(W) remains accepted. Expand the
following map over F_2:

    A: direct_sum_(i in Z) L_i^(-1)(W) -> F^K,
       (w_i) -> sum_(i in Z) H_i*w_i.

Solve A*w=s-H*x^0 by binary Gaussian elimination and return x=x^0+w,
with w zero outside Z. If the right-hand side is outside the image,
return UNKNOWN for THIS ansatz. Rank nK guarantees success for EVERY
syndrome and all the initialized one values. Lesser rank can still solve
the particular right-hand side. Verify Hx=s and every original predicate.

This deterministic algorithm works for any supplied masks once the rank
condition holds. It does not need their randomness to verify a witness.
It also works without the MDS promise when the expanded map is surjective;
MDS is needed only for the uniform probability bound below.

## 2. Exact Mask-Rank Calculation

Fix H independently of the mask draw, and choose each L_i independently
and uniformly in GL_n(F_2). Then
W_i=L_i^(-1)(W) is an independent uniform m-subspace. A fixed nonzero
binary functional annihilates W_i with probability

    a = (2^(n-m)-1)/(2^n-1).

One proof is to count nonzero functionals in W_i's annihilator: it has
exactly 2^(n-m)-1 of the 2^n-1 possible nonzero functionals. Symmetry makes
each equally likely. This counts subspaces, not independent basis vectors.

Identify binary functionals on F^K with v in F^K using the nondegenerate
absolute-trace pairing. On coordinate i the functional is
Tr((v dot H_i)*w_i). It is identically zero on F precisely if v dot H_i=0.
Thus the probability that a given v!=0 annihilates ALL correction columns
is a^wt(v^T H_Z). The expected number of nonzero annihilators is exactly

    E = sum_(v!=0) a^wt(v^T H_Z)
      = sum_(t=0..K-1) binom(z,t)*(1-a)^t*a^(z-t)*(q^(K-t)-1),
    q=2^n, z=|Z|>=K.                                      (1)

To derive (1), expand each weight factor as
a+(1-a)*1_(v dot H_i=0). Any t<K specified zero positions impose t
independent F-linear equations by MDS, leaving q^(K-t)-1 nonzero v.
For t>=K there are none. This is the usual MDS weight-enumerator argument,
also used in the independent review, not an independence assumption about
the parity equations or inverse-trace bits.

Rank failure implies at least one nonzero annihilator, so its probability
is at most min(1,E). Bounding the finite sum by the full binomial gives

    E <= q^K * [a+(1-a)/q]^z
       = 2^(n*K-m*z).                                    (2)

The simplification is exact: a+(1-a)/q=2^(-m). Dimension counting by
itself does NOT establish (2); the random-subspace calculation and MDS
enumerator are essential. The first moment E is NOT the exact failure
probability: a deficient matrix can have many nonzero annihilators.

For even n and z=2K+h, (2) is 2^(-n*h/2). With n=20, N=400, K=50,
and z=200, the bound is 2^-1000 for any fixed support of that size,
every public syndrome and every MDS H. This is a symbolic probability
bound over masks, not a measured run or a practical runtime comparison.

## 3. Costs And Source Assumptions

There are nK binary rows and mz correction columns. Elementary elimination,
field multiplication, mask inversion, subfield construction and final
verification all have polynomial bit cost. A conservative dense bit-cost
bound for elimination is O((nK)*(mz)*(nK+mz)); at the native parameters
this is O(n^9). Bit-packed implementation can improve constants, but no
optimized timing advantage over a quantum circuit is claimed.

Independent uniform GL_n masks can be drawn by rejection from uniform
binary n-by-n matrices; success probability is the positive product
product_(j=1..n)(1-2^(-j)), bounded below by a constant. The mask-generation
clock must be capped and charged when claiming bounded running time. The
algorithm itself can take already supplied masks and simply test rank.

There is no sampling of rare full native witnesses, enumeration of F,
unknown-kernel oracle, planted witness or quantum subroutine. The output
law is biased toward rare accepted subspaces. This solves SEARCH on the
stated inputs, not uniform conditional sampling. In particular, the exact
uniform output of the reviewed quantum procedure has not been classically
reproduced by this construction.

## 4. Adaptive Targets And Failure Modes

The simplest bound fixes Z independently of the random masks. If targets
or offsets are chosen after seeing the masks, do not reuse it without a
uniformity argument. Rank is monotone when more zero columns are added.
A union bound over all z0-subsets gives the simultaneous statement

    Pr[some support of size >=z0 has deficient rank]
      <= min(1, binom(N,z0)*E(z0))
      <= min(1, binom(N,z0)*2^(nK-m*z0)).                 (3)

For the n=20 example and z0=200, binom(400,200)<2^400, so this probability
is less than 2^-600, simultaneously for ALL such target supports and all
syndromes. Near z0=2K the extra factor can make the bound useless. It is
not legal to suppress that factor by calling a chosen target random.

Important falsifiers and exclusions:

- Identical or adversarial masks need not satisfy the probability claim.
  With every mask the identity and a Vandermonde first row of ones, the
  first syndrome component of all subfield corrections stays in the
  subfield. There are explicit inconsistent right-hand sides even with
  many more columns than rows. The stronger unmasked buffer attack from
  the review still handles its stated scope; failure here does not refute it.
- H chosen adversarially AFTER the masks is not covered by (1)--(3).
  A successful deterministic rank/correction certificate remains valid,
  but the distributional theorem cannot be imported for such dependent H.
- For prime n>3 no large proper subfield supplies this W. Small accepted
  flats do not automatically have enough dimensions. This theorem does
  NOT solve the remaining prime-degree native problem.
- One-heavy effective targets may provide too few correction coordinates.
  Random public bit offsets against a fixed target usually restore many
  effective zeros; adversarial offsets can do the opposite. Count e, not b.
- This is not a theorem for arbitrary nonlinear masks, arbitrary Boolean
  functions, or arbitrary non-MDS matrices from dimension counts alone.
- Passing finite fixtures does not prove a general relation or verify the
  quantum construction, and failing this attack does not certify hardness.

## 5. Deterministic Closure Under Simpler Masks

There is a separate, non-random closure of the review's stronger attacks.
For public alpha_i!=0, center c_i and offset delta_i, normalize

    Tr(alpha_i*inv0(x_i-c_i))+delta_i=b_i,
    y_i=(x_i-c_i)/alpha_i,
    H'=H*diag(alpha_i),  s'=s-H*c,  b'_i=b_i+delta_i.

Then H'y=s' and Tr(inv0(y_i))=b'_i EXACTLY, including x_i=c_i.
Column scaling preserves MDS. Both review constructions work for arbitrary
syndromes and any MDS columns: the even-degree matroid-union proof permits
r=2K with an empty quotient buffer, and the degree-three transversal proof
uses only ranks of column subsets. Thus their respective 2K and 3K zero
thresholds survive these changes of coordinates without assuming random masks.

Likewise Tr(alpha*z^(2^j))=Tr(alpha^(2^((n-j) mod n))*z). Public Frobenius
twists of the inverse therefore reduce to a nonzero scalar mask. They do
not hide the proper-subfield structure from a classical algorithm.

Do NOT extend this claim carelessly to a totalized fractional-linear map.
The rational identity ax/(x+1)=a+a/(x+1) fails at x=1 if BOTH fractions
are totalized to zero: the two extensions have values 0 and a. When
Tr(a)=1 their predicate bits differ. A promised exceptional-point policy
or a separately paid avoidance method is required; the code tests this trap.

## 6. Research Consequence And Verification

The independent review closed at 2026-10-23 03:27:20 Sydney. Its strongest
native search attacks cover arbitrary supplied points for even n>=8 with
2K zeros, and 3|n, n>=6 with 3K zeros. Its previous witness receipts are
not new executions by this pass. Its quantum audit retained the ideal
construction but identified prior generic full-list/DQI theorems; it did
not establish natural-problem hardness or novelty of the specialization.

This follow-on closes a specific mutation loophole: public scalar,
translation, Frobenius, and typical independent binary-linear masks cannot
be promoted merely because they obscure visible subfield coordinates.
The masked relation must face the actual normalized attack or rank test.
Restricting to the remaining prime-degree/one-heavy cases is a changed
scope, not evidence of a major quantum advantage. The next constructive
classical question remains the review's small affine residual solver;
more masking or nearby Gibbs barriers do not resolve it.

`theorems/binary_subspace_correction.py` contains exact rank/correction and
conditional first-moment arithmetic only. It does not validate a field,
an MDS matrix, a source, or an accepted subspace from dimension parameters.
`tests/test_inverse_trace_mask_closure.py` independently reconstructs field
arithmetic, checks masked native-size witnesses at n=6,8,10 with arbitrary
syndromes, exhausts small subspace/first-moment identities, and exercises
rank, adaptivity, scalar/Frobenius and exceptional-point countercontrols.
No qsearch/UI/central-registry admission, Git write, new agent, hydration,
or relocation is part of this pass. Gemini can integrate the stated attack
contract later; this note does not authorize promoting a speedup claim.

Final focused validation: 27 new tests PASS in 0.17s. Combined with the
resident uniform-BCH and independent source-bank controls, 75 tests PASS
in 0.56s. Both new Python files pass py_compile. This is not a full-repo
suite, a run of the independent review's saved scripts, geometric execution,
or an executed quantum circuit.
