# Stable Products: The Missing Operation Is Global Compression

2026-10-26. Mathematical access audit and exact supplied-lattice controls.
No native curve computation, new quantum algorithm, novelty claim, or general
classical lower bound. These deductions have not had independent review.

## Decision

Do not implement a product-label HSP by silently replacing polarized
canonicalization with unpolarized or oriented canonicalization. Nor can a
finite-level orientation/pairing transcript alone supply the missing global
ideal class. The explicit example below defeats even compatible transcripts
at EVERY modulus, not just a chosen list of small primes.

A genuinely useful target would be native, compact **class-product
compression**: from curve objects representing a and b, produce a curve
object representing ab, without either ideal class or connecting Hom module
as advice. This is a precise high-upside problem, not a construction supplied
here. A product-isomorphism invariant is a weaker output contract.

## 1. Primary Literature And Exact Input Boundaries

[Boneh et al., arXiv:1807.03038v3](https://arxiv.org/html/1807.03038v3),
Section 4 and Appendix A, give the ordinary-curve product classification
under Z[Frobenius]=O_K. A product's unpolarized class depends on the product
of its ideal classes. The missing invariant need not have a group-valued
range. Section 5 and Appendix B explain why the usual polarized invariants
do not solve that problem. Do not extend the stated hypotheses to arbitrary
orders or supersingular orientations without another theorem.

[Gaudry--Soumier--Spaenlehauer, arXiv:2503.21535v2](https://arxiv.org/html/2503.21535v2),
revised 2026-07-10, Sections 2.2.2 and 3: the input contains efficient
evaluators for a FULL endomorphism-ring basis and its quaternion embedding
at each curve. Theorems 3.1-3.2 give an expected-polynomial classical
unpolarized product-isomorphism algorithm under GRH for maximal models over
F_(p^2). This is not an algorithm from one endomorphism. The older ePrint
2025/136 abstract that advertised a fixed-endpoint difficulty is stale;
the current primary record and arXiv revision supersede it. Theorem 2.5
also confirms that bare geometric supersingular products of dimension >=2
all have the same unpolarized isomorphism class. Forgetting orientation and
descent therefore destroys the desired signal. This does not say that all
products over the original smaller finite field are isomorphic there.

[Rains et al., arXiv:1912.07081v2](https://arxiv.org/html/1912.07081v2),
Theorems 1.1 and 1.3: rational maps of the stated moduli schemes invariant
under unpolarized isomorphism are constant. This rules out that algebraic
invariant route. It is NOT a computational lower bound for finite-field
algorithms or arbitrary orientation-sensitive labels.

[Arpin et al., arXiv:2407.14450v1](https://arxiv.org/html/2407.14450v1),
Section 2.4: in the inert case the primitive supersingular orientations
have two class-group orbits; their construction fixes one. An arbitrary
one-endomorphism input does not automatically supply a primitive orientation,
a common orbit, or a proved stable oriented-product classification.

The existing local PPAV audit, ppav-source-2026-10-23/PPAV_SOURCE_DECISION.md,
states the represented-POLARIZED input contracts of A7/A22/A25/A28 and their
fixed-dimension costs. None provides the missing oriented unpolarized
operation. We have not executed those geometric algorithms in this pass.

## 2. An Explicit Global Class Hidden From All Paired Local Modules

Use K=Q(sqrt(-23)), w=(1+sqrt(-23))/2 and its maximal order

    O=Z[w], w^2-w+6=0,
    I=(2,w), J=(2,w-1)=conjugate(I), I*J=2O.

These ideals and all their coordinates are SUPPLIED mathematical controls,
not an algorithm for extracting them from unknown curve equations.
Multiplication by w in the bases (1,w), (2,w), and (2,w-1) is respectively

    A=[[0,-6],[1,1]], B=[[0,-3],[2,1]], C=[[1,-3],[2,0]].

Every integral intertwiner O -> I has the form

    S(x,y)=[[x,-3y],[y,2x+y]],
    B*S=S*A, det(S)=Q(x,y)=2x^2+x*y+3y^2,
    8Q=(4x+y)^2+23y^2.

The first column determines the second, so this describes ALL such maps.
If y is nonzero and integral, Q>=23/8>2; since Q is integral, Q>=3.
If y=0 and x is nonzero, Q=2x^2>=2. Thus there is NO integral determinant
+/-1 intertwiner. O and I are not isomorphic as O-modules. This is a proof,
not an extrapolation from a bounded search.

Let P=[[0,1],[-1,0]]. The following are doubled real Gram matrices for
the norm forms Norm(z)/Norm(ideal) on the three lattices:

    G_O=[[2,1],[1,12]], G_I=[[4,1],[1,6]], G_J=[[4,-1],[-1,6]].

The normalized alternating CM forms are P in these positively oriented
bases. Direct identities give

    S^t*P*S=Q*P, S^t*G_I*S=Q*G_O.

Nevertheless there are two RATIONAL isometries with determinant one:

    S_odd=S(1/2,-1/2)=[[1/2,3/2],[-1/2,1/2]],
    S_two=S(-2/3,1/3)=[[-2/3,-1],[1/3,-1]].

Use S_two over Z_2 and S_odd over Z_l at every odd prime l. Both commute
with the orientation as above and preserve P and G. For every integer
m>=2, CRT glues these into S_m in SL2(Z/m) with

    B*S_m=S_m*A, S_m^t*P*S_m=P, S_m^t*G_I*S_m=G_O  (mod m).

The choices are compatible under reduction whenever m divides n. Hence
even the inverse system of abstract paired orientation modules does not
distinguish these globally distinct integral objects. One can construct
S_m in polynomial bit cost: separate the power of two in m and take modular
inverses of 2 on the odd part and 3 on the two-part. No full factorization
or enumeration of a level-m group is involved.

### Exact Scope Of This Falsifier

It refutes labels which factor only through these finite-module isomorphism
classes, even with pairing, compatible level reduction and the displayed
norm data. It does NOT erase curve equations, actual point coordinates,
global marked geometry, or bounds enforcing a single INTEGRAL map.
The profinite map above is not such a global map. Our previous marked-PPAV
constructions require a single geometric isomorphism and are not refuted
by this example. No arbitrary native supersingular instance was generated.

The example is also a warning about using rational solutions: both S_odd
and S_two have denominators. A rational norm-one intertwiner is not an
integral degree-one morphism merely because it is locally integral on a
chosen set of primes.

## 3. Stable Product Equality Is Not Polarized Equality

The SAME ideals give a direct stable-product countercontrol. The matrix

    T=[[2,0,2,-1],
       [0,1,0,1],
       [-1,-3,0,-3],
       [1,0,1,0]]

has determinant one and satisfies diag(A,A)*T=T*diag(B,C). Thus
I direct_sum J is globally O-isomorphic to O^2. Over K it is the map

    (u,v) -> (u+v, ((w-1)*u+w*v)/2).

Its inverse is [[w,-2],[1-w,2]], whose first row lands in I and second
row in J. These expressions verify integrality, not merely a determinant
in the fraction field. The identity I*J=2O is also checked by integer HNF.

But the product metrics are not isometric. The norm on O has minimum one.
The normalized norms on I and J both have minimum two, using

    8*(2x^2 +/- x*y + 3y^2)=(4x +/- y)^2+23y^2.

Therefore O^2 has minimum one and I direct_sum J has minimum two. This
excludes EVERY integral metric isometry, not just the displayed T.
For the associated complex CM elliptic tori these normalized forms give
their canonical principal polarizations. The stable unpolarized products
agree but their product-polarized objects do not. This is an exact CM
lattice control; no finite-field model or theta backend was executed.

Taking a union over theta structures for a FIXED polarization cannot fix
this mismatch. Nor does repeating a direct product turn a fixed-dimensional
polarized canonicalizer into a uniform class-product algorithm.

## 4. A Functorial Polarization Shortcut Cannot Preserve All Maps

On E^2, scalar shears U_t=[[1,t],[0,1]] commute with the diagonal orientation
for all integers t. If a positive Hermitian H=[[a,b],[b^dagger,d]] were
preserved by every U_t, the upper-right entry of U_t^dagger H U_t-H would
be a*t. At t=1 this forces a=0, contrary to positivity.

Thus there is no choice of positive polarization on this same object that
makes ALL its unpolarized oriented automorphisms polarized automorphisms.
This only blocks that faithful functorial shortcut. It does not forbid a
nonfunctorial canonicalization algorithm, loss of some morphisms, an altered
object, a search over polarizations, or a genuinely new construction.

## 5. The Constructive Target And Its Resource Obligations

For a fixed base E in a proved class-group torsor, demand a native routine

    Compress_E(E_a,E_b) = E_(ab)

with compact, canonical output, correct orientation/descent, polynomial
bit cost and a bounded coherent evaluator. The input must be curve models
and legitimate available maps, NOT the unknown ideals a,b or their Hom
lattices. The routine must be reusable on its OWN outputs. A formal product
with twice as many factors is not compression.

[Galbraith--Panny--Smith--Vercauteren, arXiv:1812.09116v2](https://arxiv.org/html/1812.09116v2),
Definition 2.1 and Theorem 3.3, give the known polynomial quantum reduction
from vectorization to perfect parallelization for efficient group actions.
It requires compact representations, canonical orbit encodings, generators
and efficient group operations/action. Section 4 explicitly warns that
arbitrary long class-group actions in CSIDH are not supplied by its usual
short-secret implementation. Do not hide that extra cost or treat a
probabilistic test on sampled instances as a perfect coherent oracle.

There is an important constructive qualification. If Compress already
supplies a correct compact multiplication law on the ENTIRE orbit, and
the images g_i*E of a generating set are available, it can itself evaluate
large generator powers by double-and-add. The map

    (z_1,...,z_r,t) -> Compress-product of (g_i*E)^(z_i) and E_a^t

then gives the usual abelian period-lattice route without separately
evaluating long ideal actions. Inverses can be obtained from finite orders.
This uses the proposed compression operation, not existing short walks;
its uniform scope and canonical outputs still have to be proved. It is
not an independent new HSP algorithm or an implementation of compression.

Also, perfect correctness is a sufficient calibration contract, not a
universal necessary condition. The later
[Galbraith--Lai--Montgomery work, ePrint 2024/191](https://eprint.iacr.org/2024/191)
gives improved amplification for unreliable CDH oracles, following
Montgomery--Zhandry. Its current primary abstract reports order epsilon^-4
oracle calls. We have not audited its full model in this pass. A proposed
partial compressor should be tested against its actual hypotheses, not
rejected merely for inverse-polynomial success. Finite empirical success
alone does not establish those hypotheses.

Our proposed compression contract would address parallelization, whereas
an invariant of E_a x E_b merely gives a value at ab in another set. Its
range need not support multiplication or inversion. No impossibility of
all reductions from such an invariant is claimed here; this particular
invocation of the parallelization theorem is unjustified without closure.
Raw repeated squaring of products doubles geometric dimension each time.
A compressed expression DAG does not provide a geometric evaluator with
polynomial cost in the DAG length.

A tempting algebraic specification is the determinant module
det_O(Hom(E,E_a) direct_sum Hom(E,E_b)). But the Hom modules are the global
input information we do not possess. Invoking their computation is not
an implementation. Likewise an exterior power of cohomology is not, by
itself, a constructed elliptic curve with the required integral model.

Classical comparison must be on the same input. A classical parallelizer
would already be important, but does not automatically give a classical
vectorizer. Conversely, a full native Hom ideal or isogeny supplied as
advice must be charged, not credited as a quantum discovery.

## 6. Small-Total-Multiplier Anchor Extraction Has A Classical Competitor

Suppose a construction begins with a product-polarized X=product_i E_i,
produces an N-polarized isogeny phi:X->Y, and extracts a principal elliptic
factor identified with the desired anchor E. Let p:Y->E be its orthogonal
projection, so p*p^dagger=1. Write p*phi=(psi_1,...,psi_g). Then

    sum_i psi_i*psi_i^dagger = p*phi*phi^dagger*p^dagger = [N]_E,
    sum_i degree(psi_i)=N.

At least one psi_i is a nonzero actual E_i->E isogeny of degree <=N.
If this TOTAL N is polynomial in the input bit length, searching the
bounded-degree isogenies is a classical polynomial-in-VALUE-N competitor
(with torsion, fields, kernels and target isomorphism checks charged).
Thus extracting an unfamiliar anchor through a tiny-total-multiplier
gluing is not a new way around the missing connector.

This argument does not rule out a smooth but numerically huge N represented
by a polynomial-length chain. Products of many small multipliers can be
exponential in input length. If the source already includes the anchor,
the extracted component may be just its inherited projection and carries
no information; a nonzero cross-component must be demonstrated separately.
No native gluing or bounded-degree search was run in this pass.

## 7. Adversarial Verdict And Next Decision

- Bare supersingular product invariant: rejected by geometric collapse.
- Product-polarized canonicalizer as Steinitz invariant: rejected by the
  explicit I+J versus O^2 control and the source's input contract.
- Local orientation plus pairing as a global class label: rejected by
  the compatible S_m family at ALL moduli. Adding more primes cannot fix it.
- Known-ring product-isomorphism solver as a one-endo solver: rejected
  because its full ring/evaluator input is missing, not because it is slow.
- Native class-product compression: still unsolved here; high upside but
  no mechanism yet. It remains a research QUESTION, not an accepted candidate.

An alleged repair must say which global datum defeats the S_m control,
how that datum is extracted from the native curve input, and how output
compression avoids dimension growth. A claim based only on local matrices,
known ideals or A7 on product polarizations fails before any parameter sweep.

Do not build an invariant-map or HSP framework around a placeholder for
Compress. The next decision should reconcile the independent additive-source
review and compare a genuinely native global mechanism with an independent
research direction. This pass closes another attractive shortcut; it does
not justify more nearby torsion/gauge sweeps by inertia.
