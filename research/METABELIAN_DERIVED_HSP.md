# Metabelian-Derived HSP Through Right-Fiber Fourier Sampling

2026-10-22. CONSTRUCTIVE ROUTE, UNDER REVIEW. This proposes a larger
scope than the class-three-normal receiver. It establishes a written
source/degree argument, exact algebraic diagnostics and an explicit
strict-scope witness. It does NOT establish novelty, a fully verified
algorithm, practical resources, or a useful external speedup.

Subsequent passes supply a public higher-degree phase compiler and the
generalized right-fiber instrument/source-to-scalar Lean composition.
See METABELIAN_INDUCED_PHASE_COMPILER.md and RIGHT_FIBER_SOURCE_REFINEMENT.md.
INDUCED_END_TO_END_RESOURCE_AUDIT.md now supplies a separate higher-degree
support theorem, conditional adaptive schedule and exact resource artifact.
INDUCED_COCYCLE_UNIVERSAL_REFINEMENT.md adds the universal written
Lie-to-cocycle/substitution argument, exact normal-form certificates and
formal operator-specialization lemmas. A single machine-checked
Lie-to-controller refinement, complete adaptive receiver, physical
synthesis, novelty and application obligations remain.

INDUCED_RECEIVER_COMPOSITION_THEOREM.md now gives one complete written
procedure from the original f to arbitrary H, separates published
algorithmic dependencies from missing local implementations, and closes
the nonzero-vector/active-scale formal interface. It also supplies an
exact shared-randomness falsifier for marginal-only composition arguments.
The theorem remains provisional and independently unverified; it is not
an executed receiver or a speedup admission.

AMBIENT_FILTERED_INDUCED_RECEIVER.md now refines the resource route using
actual lower-central adapted coordinates and heterogeneous full jets.
Weighted phase degree falls from kc to c; the class-nine witness uses
155 retained jets and15 erasure stages instead of1155 and45. The p43
sufficient query ceil-log2 envelope falls333018 ->4496, still impractical.
The public filtered compiler and coordinate-degree Lean lemmas are
checked; the complete physical receiver, independent review, novelty
and useful application remain open. The old uniform bounds below remain
valid conservative comparators, not the strongest available schedule.

## The Scientific Question

Is class(N)<=3, for N=L', intrinsic to full-jet erasure, or an artifact
of the particular central/B-Fourier basis? The following construction
indicates it is an artifact. A normal group N with ABELIAN N' admits
a complete, fixed-label, translation-only regular decomposition even
when its nilpotency class exceeds three. Its scalar phases have higher
degree; the previous quadratic-parameter compiler cannot handle them.

Induced representations and subgroup-adapted Fourier methods are old
representation theory, not the proposed novelty. Compare the broader
Fourier framework of [Moore--Rockmore--Russell](https://arxiv.org/abs/quant-ph/0304064).
The research question is whether this source and unknown-support phase
erasure compose into a new uniform-large-prime HSP result. A fast Fourier
transform alone never supplies a hidden-subgroup decoder.

## Proposed Scope And Input

Supply an explicit Lie algebra L/F_p of FIXED class c, with N=[L,L]
METABELIAN, meaning [N',N']=0, equivalently L'''=0. Let k=class(N).
Use the ordinary coherent hiding-function oracle on exp(L), arbitrary
hidden H, and unique public Lie coordinates. For the nonabelian normal
branch take k>=2 and conservatively p>k*c. The small-class/abelian branches
can retain the previous scalar and abelian procedures. No claim for
growing class, arbitrary black-box encodings, prime-power exponent or DCP.

Proposed conclusion, contingent on full composition: bounded-error quantum
time polynomial in dim(L) and log(p), with exponents depending on c.
Classical opaque-label query hardness is not a new practical application.
The existing graph/code/explicit-matrix-action baseline audit still applies.
No access-matched hard external problem has been identified.

Start with H intersect exp(N)=1. The previously derived common section
potential g(q), original hiding-output trace and regular kernel remain
valid for this N. They do not require class(N)<=3. All hidden lifts,
retractions and coefficient values are proof witnesses, not inputs.

## Public Right-Fiber Chart

Choose I=N', or any public ABELIAN ideal with N'<=I<=N. Let A=N/I and
let s:A->N be a public linear section of the Lie quotient. A is an
additive vector space. In group notation write r(x)=exp(s(x)). Every
normal-group element has unique coordinates

```
n = r(x) exp(i),    x in A, i in I.
```

This is the RIGHT-fiber order: the subgroup element is on the right.
The coset is r(x)I; normality makes left/right coset sets agree, but does
NOT make the two coordinate orders interchangeable. No homomorphic
section or semidirect-product splitting is required.

The inverse chart is public: x is the projection of log(n), and
i=log(r(x)^-1 n). Fixed-class BCH and linear algebra implement both
directions in polynomial bit complexity. I is abelian, so its group law
is addition in these logarithmic coordinates.

For g in exp(N) define a(g) in A and the PUBLIC group-action cocycle

```
kappa(g,x) = log(r(a(g)+x)^-1 g r(x)) in I.
g r(x) exp(i) = r(a(g)+x) exp(kappa(g,x)+i).
```

The second identity uses only associativity and the fact that both fiber
elements lie in the abelian group I. Centrality is NOT required. It gives

```
kappa(gh,x) = kappa(h,x)+kappa(g,a(h)+x).
```

After inversion of the normal coordinate, apply positive abelian Fourier
on this i coordinate and measure its character lambda in I*. The actual
amplitudes are

```
K_lambda[x,n] = |I|^-1/2 [x = pr_A(n^-1)] omega^(lambda(pr_I(n^-1))).
```

The right chart is a permutation and the fiber Fourier transform is
unitary. Summing all lambda, including zero, gives a complete instrument.
Its regular blocks are the induced monomial representations

```
W_lambda(g)|x> = omega^(lambda(kappa(g,x))) |x+a(g)>.
```

The cocycle identity proves multiplicativity; translation and unit phases
prove unitarity. Crucially, lambda is FIXED under the left regular action,
even when lambda is not invariant under conjugation by N. Left regular
translation commutes with right multiplication by I. There is no coadjoint
orbit selection or irreducible-representation algorithm hidden here.

For the original hiding-output trace, the same finite sum contraction as
the regular-source theorem yields the UNNORMALIZED branch

```
|I|^-1 p^-(m+dim A) [q'-q in U]
  (W_lambda(g(q))^dag W_lambda(g(q')))[x,x'].
```

Its trace is 1/|I| for EVERY lambda under transversality. Retain them all.
The normalization uses I, not Z(N), lambda(I), or an irreducible dimension.
This argument starts at the original oracle, not at a desired matrix
kernel. It does not require a coherent evaluator for the hidden g(q).

## Why The Coordinate Side Is Essential

In the alternative chart n=exp(i) r(x), left multiplication conjugates
i. Fourier labels then move. Simply measuring that label and asserting
a fixed-label monomial representation is false. The class-four filiform
test detects nonzero cross-character blocks in this WRONG chart while
the correct right-fiber chart has zero cross-character blocks.

The old class-three normal representation makes this visible in a simpler
way. Its coherent (x,mu) action is (x+a,mu+ell_lambda(a)). The public
change nu=mu-ell_lambda(x) makes nu invariant. Measuring nu can be valid;
measuring the old mu directly is not. This is a basis change, not a
contradiction of the old early-mu-measurement falsifier.

## Polynomial Phase Without Hidden Advice

Write Q=log(g), A0=s(a(g)), B0=Q-A0 in I and X=s(x). Then

```
kappa(g,x) = log(exp(-A0-X) exp(A0+B0) exp(X)).
```

All three exponents are linear in (Q,x). The BCH series truncates at
NORMAL class k, so this is a polynomial of total degree <=k in these
variables. It can be represented by public rational Lie-word coefficients
and the public structure constants, then projected into I.

No new BCH engine is needed. The existing universal section-word
certificate becomes precisely this expression under
(X_old,Y_old,Z_old)=(-A0-X,A0,B0). Its free-associative coefficient check
is independent of any sampled hidden values. The new test evaluates this
certificate against actual matrix exp/log inside the class-nine ambient
witness below and checks that the result belongs to I.

For the proposed full receiver use the conservative jet degree D=c:
every component of Q(q) has degree <=c from the original section-word
argument. This does NOT require identifying the full center. Set
r=dim(N/I), b=dim(I), h=(r+b)*binom(m+c,m). Hidden coefficient monomials
through degree k give at most P=binom(h+k,k) public lift columns.

The induced displacement is exactly the A projection of Q(q), independent
of lambda. Existing FULL Taylor features and public GL alignment therefore
apply unchanged at degree D=c. The scalar evaluation rank suffices for
all labels without a label SDE. The retained jet width is
J=r*binom(m+D,m+1). After alignment, carrier coordinates are public affine
forms in t and the measured spectators. Assign q weight one and a jet
coordinate its Taylor weight, at most D. Each Q(q) has weight <=c and
each carrier form weight <=D=c. Consequently the compiled phase has
weight <=e=k*c and hidden-parameter degree <=k.

Erase weighted degrees e,...,1 by coefficientwise diagonal relations
over the SAME fixed hidden coefficient basis. Fourier-read the complete
jet and erase ordinary degrees D,...,1. The existing generic mixed-channel
and Taylor-transport identities are the intended receiver interfaces.
They must not be replaced by full-domain polynomial learning: U can be
unknown and proper.

The quadratic source-support certificate from the preceding pass DOES
NOT apply. Class-four filiform cocycles already contain hidden-parameter
and carrier degrees greater than two. The production SymbolicScalarPacket
multiplication rejects parameter products above degree two. That guard
is correct: suppressing it or truncating those terms would give a wrong
phase. The existing compiler cannot be reused unchanged.

The subsequent METABELIAN_INDUCED_PHASE_COMPILER.md pass supplies a
SEPARATE public general-lift compiler from the universal Lie certificate.
It verifies whole cocycle coefficients against independent semidirect
calculations, complete aligned phases and actual Taylor pullbacks, and
checks the class-nine ambient witness against matrix exp/log. It retains
all labels and spectators and enforces linearity in ideal coefficients.
The general hidden-parameter cap is k, although I=N' permits k-1 for k>=2.
The compiler keeps the conservative envelope; weighted degree remains kD.
This removes a public-algebra implementation gap, NOT the source-refinement,
physical execution, general SDE, resource composition or novelty obligations.

Optional later improvement: I=N'+Z(N) is also abelian when N is metabelian
and permits the earlier D=c-2 projection argument. Do not assume that
improvement when using I=N' alone. The conservative proposal uses D=c.

## Resources And Arbitrary Hidden Subgroups

A safe generic equation bound is Ew=P*binom(m+J+e,e), and for the ordinary
stage Eo=(1+r*binom(m+D,m))*binom(m+D,m). Use the published fixed-degree
SDE arities with degrees through e, not the partial g<=2 backend.
For t final roots the matrix-leaf count is

```
M=t * product_(j=1..e) a_j(Ew) * product_(j=1..D) a_j(Eo).
```

All exponents are constant only at fixed c. Each leaf uses the previous
full-feature rank schedule with nonzero random scales, all Fourier labels,
fresh ordinary queries and bounded retries. The conditional product-state
and complete-instrument hybrid arguments in
FULL_JET_ADAPTIVE_RESOURCE_THEOREM.md transfer only after this new local
source and phase compiler are verified. Its NUMERICAL certificate does
not accept this larger scope and must not be reused unchanged.

The subsequent INDUCED_END_TO_END_RESOURCE_AUDIT.md supplies the separate
induced_resource_certificate.py. It counts each parameter-degree block
with q degree<=hD and jet degree<=k-h, retaining at most one ideal
coefficient. Actual separated Taylor transport preserves these blocks.
At the c9/k4 witness dimensions the p43 sufficient query cap becomes
<=2^333018 instead of the generic <=2^1081434. These are reconstructible
arithmetic UPPER bounds, not executed queries or practical estimates.
The new JSON covers one transverse call; the general-H budget below is
written mathematics, not part of that certificate.

The arbitrary-H algorithm can keep the existing normalizer recursion:
solve K_H=H intersect N by recursively solving the metabelian ambient N,
pass to N_L(K_H)/K_H, and recover successive hidden images. Recompute the
derived ideal; do NOT assume N is inside the normalizer. Metabelianness of
the derived algebra is inherited by subgroups and quotients. Transversality
makes the remaining hidden subgroup abelian, and the exact image preimage
h+S' has strictly lower ambient nilpotency class as before.

There are at most (c-1)+(k-1)=c+k-2 image calls when N is nonabelian,
and at most three abelian calls. The old c+1 bound assumed k<=3 and does
not apply here. Query costs add across these calls; products are only
inside their erasure trees. Uniform caps, first-error accounting and
canonical-output amplification remain required.

## A Strictly Larger Scope Witness

Inside strictly upper-triangular 10 by 10 matrices let

```
X=sum_(i=1..9) E_i,i+1,
Y=sum_(i=1..9) i^2 E_i,i+1,
L=Lie<X,Y>, C=[X,Y], B=[X,C].
ad_C^3(B) = -1680 E_1,10 != 0 for every prime p>9.
```

The last word has ambient length nine and is in gamma_4(N), N=L'.
Strict triangularity gives class(L)<=9 and class(N)<=4, so both bounds
are attained. Also N has no superdiagonal below two and its degree-two
part is spanned by C. Bracketing two such elements has no degree-four
part because [C,C]=0. Thus N' lies on superdiagonals >=5 and [N',N']=0
inside 10 by 10 matrices. This proves metabelianness of N independently
of the sampled-prime computations.

At p=43 and 2^127-1 the exact closure calculation gives derived dimensions
19,17,10,0 and normal lower-central dimensions 17,10,5,1,0. The existing
class-three-normal frontend correctly REJECTS this input. The new source
premise accepts its metabelian normal algebra. Direct powers supply
unbounded-dimensional families with the same classes; hidden subgroups
need not split across those factors.

This is a scope witness, not a solved HSP instance or application. The
new degree bounds suggest p>36 for this c=9,k=4 receiver, so p=43 and
the large prime meet the conservative field condition.

## A Sharp Limitation Of This Representation Ansatz

Suppose a faithful regular representation is unitarily decomposed into
fixed-label blocks, each acting as a unit-phase monomial operator with
an additive translation d(g) on its carrier. Multiplicativity forces
d(gh)=d(g)+d(h). Every element of N' therefore acts diagonally in every
block. Those diagonal operators commute, so N'' acts as identity in all
blocks. Faithfulness implies N''=1.

Conversely, when N is metabelian the above I=N' construction provides
exactly such a decomposition. Thus metabelianness is the precise group
condition for this complete faithful translation-only ansatz. This is
not a limitation on arbitrary quantum channels or HSP algorithms.

For a concrete excluded case, L=ut_9 has N=L' and
[[E13,E35],[E57,E79]]=E19 !=0 inside N''. Merely changing the polarization
cannot turn its COMPLETE faithful regular action into fixed-label pure
translation blocks. A different carrier mechanism is needed there.

## Evidence, Prior Art And Falsifiers

Implemented: right-fiber group chart/action and cocycle controls; exact
rational filiform phases through normal class seven; an actual original
gH-label trace with a class-four noncentral ideal; left-fiber cross-label
counterexample; the class-nine ambient witness; and matrix exp/log checks
of the generic cocycle word. Run
`python -m theorems.right_abelian_induced_source --write`.

The original-oracle fixture uses G=F_p^2 x N and a graph subgroup with
proper projected support. It validates the GENERIC physical source but
does not pretend that its selected N is G'. The distinct matrix-algebra
witness verifies the larger ambient input premise. Neither test alone,
nor their conjunction, executes the claimed complete algorithm.

[Imran--Ivanyos](https://arxiv.org/abs/2304.08376) supplies a constant-class,
bounded-prime result, not this uniform-large-prime conclusion. The
[Ivanyos--Santha](https://arxiv.org/abs/1503.09016) diagonal solver and
polynomial-graph algorithms are dependencies, not new contributions.
The earlier access-matched HPGP and smoothly-solvable scope caveats still
apply. A targeted search found no demonstrated subsumption; this is NOT
an exhaustive novelty certificate.

Why it may fail or be unimportant:

- A general coefficient compiler may not match the actual right-fiber
  source, despite the degree proof and diagnostic cases. Compare full
  symbolic coefficients, including every higher parameter monomial.
- An implementation may measure the wrong fiber character or use the
  wrong side of the section. Cross-character blocks are a direct falsifier.
- Old quadratic lifts, degree D=c-2 without a full-center inclusion, or
  the c+1 recursion cap would invalidate the enlarged claim.
- The complete adaptive oracle-to-output proof is still unassembled;
  physical precision and all-input SDE execution remain obligations.
- A matching published reduction would remove novelty. The induced
  representation itself is certainly not new.
- Even if correct and new, fixed-class oracle HSP can remain irrelevant
  to lattice, graph, code or cryptographic applications. Existing
  classical filters and the lack of a hard application remain unchanged.

NEXT: complete receiver composition or a mechanism that removes the
large erasure tree. The generic source composition, universal cocycle
refinement, independent coefficient checks and conditional resource
argument are now available. The universal refinement is not yet a
single end-to-end Lean theorem; do not repeat local examples by inertia.
Do not admit a new speedup candidate, relax the metabelian condition,
reuse the quadratic compiler, or build UI wiring from these diagnostics.
