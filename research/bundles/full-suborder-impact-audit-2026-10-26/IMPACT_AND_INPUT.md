# Full-Suborder Result: Impact, Prior Art, And The Actual Missing Input

2026-10-26. Selected primary-literature audit and exact algebraic deductions.
This is not an independent review, novelty certificate or native execution.
The earlier additive review remains the authority for its conditional source.

## Decision

The reviewed additive construction is worth retaining as a possible
assumption-removal result for a RESTRICTED input problem. It is not the
first quantum-polynomial full-suborder algorithm, and it does not solve the
general isogeny or one-given-endomorphism problem. More circuit wiring or
dimension-128 backend work would not change that impact assessment.

The proposed mechanism difference is substantive but narrower than a new
endpoint: native additive coset labels avoid the reference-order and
powersmooth-lift route. Whether that difference is new after all available
reductions remains unestablished. Searches that fail to find another paper
are not a proof of novelty. Do not assign a numerical breakthrough probability.

The missing input can be stated sharply: TWO genuine noncommuting native
endomorphisms suffice, not four independently supplied maps. From one map,
one still needs a genuinely new direction outside its quadratic field.
The exact reduction below makes that gate checkable, without pretending to
find the second map. This is standard quaternion algebra, not a new speedup.

## 1. Primary Comparison

### Same Endpoint Already Exists

Chen--Petit, EUROCRYPT 2025, Theorems 1 and 3, give heuristic
quantum-polynomial full-suborder and IsERP algorithms. The accepted paper's
Remarks 27/31 identify norm-solving, strong-approximation and distribution
heuristics; Section 7 leaves their removal open. Its efficient-map and
basis-height assumptions must be retained. The local additive construction
offers a different source, not the first polynomial receiver or solver.
[Accepted primary manuscript](https://dipot.ulb.ac.be/dspace/bitstream/2013/392160/3/suborder_to_endomorphism_ring.pdf).

The local copy was checked at PDF pages 3-6, 17-19, 23 and 28-30. SHA256:
554c6a9f0f49cc13a59e38bf20a351a797137938dce18bd546a9ecf47a656402.
The earlier comparison already inspected the reference-order GRH and
dictionary assumptions separately; do not merge every assumption into one
generic "heuristic" switch.

### Rank-Two Saturation Is Not The Missing Breakthrough

Herlédan Le Merdy--Wesolowski, version 4, Theorem 5.1 and Corollary 5.3,
give polynomial primitivisation from an efficiently represented
endomorphism when its discriminant factorization is supplied. Shor supplies
that factorization quantumly. Applying the additive framework merely to
recover the integral order inside Q(alpha) would duplicate this endpoint.
Their Section 6 retains a harder oriented EndRing/vectorization problem.
[Primary text](https://arxiv.org/html/2309.11912v4#S5).

This does NOT say that all rank-two inputs are useless: their remaining
global class information is precisely the hard part. It says that making
the orientation primitive is not itself a new high-upside target.

### Oracle Equivalence Does Not Weaken The Supplied Input For Free

The Page--Wesolowski EndRing/OneEnd equivalence is an oracle reduction: its
OneEnd solver can be invoked on curves chosen by the algorithm. A single
supplied alpha on one E is not that oracle. The newer unconditional
Isogeny/EndRing/MaxOrder/HomModule equivalences likewise do not furnish the
missing oracle. [Page--Wesolowski](https://www.normalesup.org/~page/Recherche/Documents/articles/one-end.pdf),
[2025/271 primary record, revised 2026-01-30](https://eprint.iacr.org/2025/271).
The latter was checked at record/abstract level, not fully re-proved here.

### Newer Comparisons To Carry Forward

- Imran's October 2026 preprint, Theorem 1.1, treats parabolic HSP in
  GL_n over effective finite chain rings. Its oracle must already hide
  a stabilizer of a SPLIT FREE flag. It supplies neither a geometric
  isogeny source nor an arbitrary nilpotent/Rees HSP theorem. Do not build
  a new parabolic receiver without comparing it to this result. The
  local additive route instead uses an abelian group from the start.
  [Primary v2](https://arxiv.org/html/2610.28368v2).
- Delgado's September 2026 preprint, Theorem 1.1/Corollary 1.2, reports
  unconditional classical expected time and memory p^(1/3+o(1)) for
  native OneEnd and consequent EndRing/isogeny algorithms. Theorem scope
  and input/output definitions were inspected; its full proof was not
  audited. Treat this as a stronger reported classical competitor, not a
  locally verified theorem or an executed baseline. Quoting p^(1/2) as
  the current best classical cost without this comparison is outdated.
  [Primary v1](https://arxiv.org/html/2609.22018v1).
- Ouyang--Wei--Xu's October preprint studies the smoothness of minimum
  Frobenius-conjugate isogeny degrees and also claims removal of the
  earlier smoothness heuristic. Its result is separate from finding a
  compact class-product operation. [Primary v1](https://arxiv.org/html/2610.21488v1).
- The represented-PPAV framework is the imported geometric engine, not
  an EndRing oracle. Its current primary record is still a preprint;
  the local review checked a conditional composition, not a formal proof
  of every imported theorem. [Primary record](https://eprint.iacr.org/2026/1142).

These comparisons narrow claims; none proves our source novel or dequantized.
WayFinder's current abstract describes improvements for finding isogenies
via oriented curves, not a polynomial solution of our restricted endpoint.
[Primary record](https://eprint.iacr.org/2026/1219). No detailed complexity
claim from that abstract is used in this audit.

## 2. Constructive Two-Map Input Reduction

Let E be supersingular in characteristic p>3. Suppose alpha and beta are
GENUINE integral native endomorphisms, with paid efficient evaluator
descriptions and binary degree bounds. Write

    t=Tr(alpha), n=deg(alpha), u=Tr(beta), m=deg(beta),
    v=Tr(alpha*beta), c=alpha*beta.

These scalar invariants are computable using the existing charged
small-torsion/CRT trace machinery. A supplied tuple of integers is not a
certificate that such native maps exist. All following claims about E
depend on that provenance promise.

The canonical involution gives

    alpha^2=t*alpha-n,  beta^2=u*beta-m,
    beta*alpha=(v-t*u)+u*alpha+t*beta-c.

The Z-span R of (1,alpha,beta,c) is closed under multiplication. Besides
the preceding identities, the only products to check are

    alpha*c = -n*beta+t*c,
    c*beta  = -m*alpha+u*c,
    beta*c  = -t*m+m*alpha+v*beta,
    c*alpha = -u*n+v*alpha+n*beta,
    c^2     = -n*m+v*c.

All coefficients are integers, so this is already Z[alpha,beta]; there is
no iterative ring-closure search. If alpha and beta do not commute, their
quadratic subalgebras generate the quaternion division algebra and these
four elements are Q-linearly independent. One proof: if beta were in
Q(alpha) they would commute; otherwise 1,beta are a left Q(alpha)-basis.

The resulting native basis evaluators are identity, alpha, beta and their
composition. Their degrees are 1,n,m,n*m; their initial descriptions have
polynomial length in the two supplied descriptions. The earlier reviewed
full-suborder construction therefore applies under its same geometric
contract. This reduces the SUPPLIED-DATA requirement, not the difficulty
of constructing beta.

### Exact Index And A Cheap Falsifier

Define

    D = 4*n*m - n*u^2 - m*t^2 - v^2 + t*u*v.

Then

    D = Norm(alpha*beta-beta*alpha),
    det(Tr(e_i*e_j^dagger)) = D^2,
    [End(E):R] = D/p,

where e=(1,alpha,beta,c). The last identity uses the genuine supersingular
maximal-order discriminant p. In this division algebra D=0 exactly when
the pair commutes; a useful pair has D>0 and p divides D.

For a direct derivation, put A=alpha-t/2, B=beta-u/2 and
C=(2*v-t*u)/4. Then A^2=-(n-t^2/4), B^2=-(m-u^2/4), and AB+BA=2*C.
The commutator is 2*(AB-C), of norm
4*((n-t^2/4)*(m-u^2/4)-C^2)=D. Computing the trace Gram determinant in
(1,A,B,AB) gives D^2; the basis changes have determinant one.

Equivalently, with Delta_alpha=t^2-4*n and Delta_beta=u^2-4*m,

    |Delta_alpha|*|Delta_beta|-(2*v-t*u)^2 = 4*p*[End(E):R].

In particular a noncommuting beta has

    deg(beta) >= p/|Delta_alpha|.

These are discriminant constraints of the familiar Kaneko type, not a
new hardness theorem. [Love--Boneh, Theorem 4.7](https://www.math.auckland.ac.nz/~sgal018/ANTS/papers/Love-Boneh.pdf)
states the related bound for optimally embedded quadratic orders. Our
displayed identity concerns the specific two-generator order, including
its index. It does not assume both input orientations primitive.

Consequences: a search for a polynomial-VALUE-degree transverse map to a
small-discriminant orientation can be impossible. A useful high-degree map
may still have a compact evaluator, so this is not a bit-complexity lower
bound. Scalar translations of either map leave D unchanged; large scalar
parts cannot manufacture noncommutation.

### Do Not Authenticate A Curve With Its Discriminant Alone

The tuple t=u=v=0, n=1, m=25 defines a positive integral order with D=100.
Although 5 divides D, the algebra is Hamilton's: alpha^2=-1,
(beta/5)^2=-1 and they anticommute. It is ramified at 2, not at 5.
Thus neither positivity, integral multiplication, nor divisibility by a
claimed p proves geometric provenance. The new code intentionally constructs
FORMAL orders only and never accepts a native research candidate.

## 3. Why Recycling One Map Does Not Supply The Second

For a known isogeny phi:E->E' of degree d and alpha in End(E), transporting
without division gives alpha'=phi*alpha*phi^dagger. Pulling back yields

    phi^dagger*alpha'*phi = d^2*alpha.

Exact integral division does not add a new rational direction. More
generally choose known quasi-isogenies phi_i:E->E_i, and let K=Q(alpha).
Morphisms of the form phi_j*k*phi_i^(-1), k in K, are closed under sums,
composition, rational division and duals: duality introduces only the
rational degree ratio deg(phi_j)/deg(phi_i) and conjugates k inside K.
Every resulting endomorphism at E therefore remains in K.

This strengthens the input bookkeeping, not the earlier general closure
result in one-endomorphism-access-audit-2026-10-25/ACCESS_CEILING.md.
That bundle already treats products and natural Frobenius arrows. A NEW
isomorphism between independently reached endpoints, a useful geometric
automorphism, or another native endomorphism can escape this restricted
category. They must be acquired, not silently identified with transport.
An arbitrary-curve OneEnd oracle is precisely extra access of this kind.

## 4. Next Scientific Decision And Falsifiers

Keep the additive theorem on a bounded assumption-removal track. Do not
spend another pass optimizing its dimension, wiring its receiver or
repeating supplied-order examples. Its practical and Shor-level impact
does not follow from the completed independent review.

The highest-upside missing input question is now concrete:

    On a supplied native (E,alpha), obtain a compact evaluable beta with
    Norm([alpha,beta])>0 in time polynomial in the paid input length.

Conditional on the reviewed source, this would give quantum-polynomial
full EndRing from one supplied endomorphism. Compare its cost with the
GRH-conditional subexponential oriented algorithms, not just generic
bare-curve search. No construction meeting this target is supplied here.

A proposed method is falsified if it only returns an element of K, relies
on unknown End/Hom advice, requires writing an exponentially long rational
map, needs more than polynomial trials, or assumes an extra isomorphism.
The discriminant and transport identities check commutation and the order
index under the native promise. They do not certify runtime, geometric
provenance or absence of hidden advice.

The separate classical-harvest question remains decisive: specify ONE
uniform legal distribution and prove useful noncommuting output often
enough on every adaptively reached order. Known symmetries, selected
subgroups and unsuccessful finite samplers settle neither outcome.

The first sharply specified distribution to investigate is uniform beta
in R/dR after the native easy-unit and 2-saturation steps, with n=d and
one fixed admissible four-square frame T per batch. The observable is
whether the COMPLETE Aut(E^128,Z_beta) contains a corner outside R after
the certified coprime pullback, not merely whether its group order exceeds
the forced symmetries. Analyze dependence on T explicitly. A theorem for
some input-specific T would still need one uniform procedure to select it.
No inverse-polynomial success is conjectured as an established fact here.

Independent-direction check: the existing HDQI ECF branch has an explicit
quasipolynomial classical competitor and lacks a useful reduction. A fresh
rank-metric DQI paper explicitly withholds an advantage claim because of
its covering-radius obstruction; this was checked at abstract level only.
[Primary record](https://arxiv.org/abs/2606.04843). A change of metric or more
uniform-mode sweeps is therefore not yet a stronger constructive lead.
The inverse-trace branch still requires public acquisition of its modular
carry; its latest handoff forbids witness-derived carry as algorithmic input.

These comparisons do not rule out those fields. They prevent a cosmetic
pivot to an already identified missing oracle. The next pass must supply
an actual transverse-map mechanism or a specific uniform harvest conjecture
with a decisive proof/experiment, rather than another neighboring control.
