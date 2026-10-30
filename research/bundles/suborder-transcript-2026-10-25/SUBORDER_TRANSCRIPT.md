# Direct Small-Level Transcripts From An Evaluable Suborder

2026-10-25. Proposed reduction with explicit proofs and exact supplied-map
controls. Independent review pending. No native curve backend, geometric
source, unknown-kernel recovery, full EndRing solver or quantum execution.
This note separates a local input conversion from the much stronger,
still-conditional whole-algorithm consequence.

## Decision And Exact Problem

The large-prime audit found two separate heuristic dependencies in the
existing full-suborder route. Rather than build an arbitrary-order weak
isogeny evaluator, obtain only the SMALL-prime transcript that our source
actually consumes. At these levels, known suborder actions give a unique
projective intertwiner by linear algebra. A global degree-envelope argument
then removes the need to choose an orientation or primitively saturate the
suborder first. This is a proposed way to avoid upstream norm-solving; it
does not validate the independently unreviewed dimension-16 source itself.

Assume the following ORIGINAL, charged input, not target-order advice:

- Supersingular elliptic curves E0 and E in characteristic p>3, with explicit
  compatible finite fields and the full evaluable O0=End(E0).
- A unital rational algebra isomorphism theta:End^0(E0)->End^0(E), represented
  by an effective full-rank suborder R of End(E) and its quaternion dictionary.
- A known positive N such that theta(N O0) is contained in R, with exact
  integral coordinates of those four scaled basis elements in R.
- Paid point arithmetic and generation of actual small-prime torsion bases.

Computing a reference curve/order and a compatible rational dictionary from
a less explicit input is an additional preprocessing obligation. It is not
granted by this note or by the control fixtures. Quantum factoring may be
charged for N; matched classical baselines receive the same factorization.
Any GRH or other assumption in reference-curve construction remains visible.

N can be obtained by clearing denominators in the four-dimensional lattice
inclusion. It need not be the smallest possible N, coprime to p, or primitive
with respect to the UNKNOWN End(E). Write N=p^v*m, with gcd(m,p)=1.

## 1. Global Map Exists, But Is Not Supplied

Choose any nonzero geometric isogeny u:E0->E for an EXISTENCE argument only.
Conjugation by u is an isomorphism of the rational endomorphism algebras.
Its comparison with theta is an automorphism of a central simple algebra,
so Skolem--Noether gives an invertible rational source endomorphism b with

    theta(a) = (u b) a (u b)^-1.

The rational line Q*(u b) meets Hom(E0,E) in a rank-one lattice. Let psi
be a generator, unique up to sign. Thus psi is an integral, PRIMITIVE
isogeny implementing theta: it is not an integer multiple of another
integral map. This is not a procedure for computing u, b or psi. None is
passed to the transcript or source algorithm below.

### Degree envelope

Let D=deg(psi). At any prime ell != p, primitivity implies that the
ell-primary kernel is cyclic. Otherwise its two Smith exponents would both
be positive, its kernel would contain E0[ell], and psi would be divisible
by [ell] as an integral map. Write its order as ell^k.

For a in O0, theta(Na) is integral, so

    psi [N] a = theta(Na) psi.

Consequently every N*a preserves ker(psi). The full source order acts as
M2(Z/ell^k) on E0[ell^k]. In a basis whose first vector generates the cyclic
kernel, choose a sending it to the second basis vector. Preservation forces
ell^k to divide N. Therefore the entire separable degree d divides m.

For a supersingular elliptic curve the p-primary part of an isogeny is
purely inseparable. If its degree were divisible by p^2, its kernel would
contain ker[p], since two relative Frobenius factors differ from [p] by an
isomorphism. This again contradicts primitivity. Hence

    D = p^epsilon * d,  epsilon in {0,1},  d | m,  so D | p*m.

No Frobenius orientation choice, primitive inclusion, unknown-target order,
or search for a small quadratic nonresidue is needed for this envelope.
The p-primary subgroup of E0 is fixed by every endomorphism: naturality of
relative Frobenius preserves its kernel. The same holds for its doubled
product, so it introduces no additional hidden group-action variable.

This argument depends on the FULL source order and a genuine GLOBAL theta.
Independent local matrix representations do not prove either promise.
Moreover the bound is for the primitive map only. The control psi=1+i and
2*psi has the same theta and projective transcript, but degrees 2 and 8;
N=2 gives p*m=22, which 8 does not divide. Do not infer degree from local
intertwiners or apply the envelope to an arbitrary scalar multiple.

## 2. Compute Each Small-Prime Transcript Directly

Let r be an auxiliary prime avoiding p*N. Obtain actual bases of E0[r]
and E[r] over their paid compatible fields. For a basis b_1,...,b_4 of O0,
evaluate the KNOWN maps N*b_i on E0 and theta(N*b_i) in R on E. Express
their images in those bases, giving matrices A_i and B_i.

Since r does not divide N, the normalized A_i/N and B_i/N each give a
full M2(F_r) representation. Solve the homogeneous linear equations

    B_i T = T A_i  for i=1,...,4.

There are 16 scalar equations in four unknowns. A nonzero solution exists:
the actual psi_r is invertible because r does not divide D. Any solution
times psi_r^-1 commutes with all M2(F_r), hence is scalar. Thus the solution
space is one-dimensional and every nonzero solution is

    T_r = c_r * psi_r,  c_r != 0.

Select a deterministic normalization, such as first nonzero entry one.
Its columns interpreted in the target basis give exactly the common-scalar
weak images required by the existing source. No unknown-isogeny call, norm
equation, target maximal-order basis, high-order point, or hidden kernel is
used. Cache this one tuple and reuse it across copies and group queries.

The executable wrapper checks both local multiplication/involution tables
and the one-dimensional invertible intertwiner. It makes eight known source
and eight known SUBORDER endomorphism calls per prime. Coordinates currently
cost two r^2-point tables, O(r^2) point operations/storage plus scalar and
field costs. This is polynomial only for our small auxiliary r. It is NOT
an arbitrary-order weak-evaluator construction polynomial in log(r).

No hidden native oracle appears in the code: its inputs are the four known
endomorphism evaluators at each endpoint. The executed controls instantiate
them as finite-module actions of SUPPLIED quaternion endomorphisms, not
actual curve points. They do not verify native input provenance.

## 3. Existing Source With An Unknown Degree Dividing p*m

This extension of the source proof requires independent review. It is not
implemented as a geometric backend. The algebraic change is small but its
scope must not be silently folded into the old prime-to-p exact-degree claim.

For m>=2, query M in Sp4(Z/m). Use the EXISTING double-level integral lift
at 2m, not at 2D and not at the ramified prime p. Its Gram operator is

    S=sigma^dagger sigma=I+2m*T0.

Put Psi=psi x psi and H=Psi S Psi^-1. The operator H is symmetric, positive
and unimodular, with the same quadratic trace relation as S. We need the
integrality of A=(H-I)/2 even though D is unknown and may be divisible by p.

Away from p,

    A=(m/D) Psi T0 Psi^dagger

is integral, because D divides p*m. At p, the rational quaternion division
algebra has a UNIQUE maximal order. Conjugation transporting End(E0) to
End(E) preserves these p-adic maximal orders. Thus H is integral at p,
and so is (H-I)/2 since p is odd. Integrality at every prime proves that
A is an actual integral endomorphism globally. There is no need to impose
sigma=I mod p or split the ramified algebra O0/p.

Now all earlier half-polarization identities and prime-only auxiliary
quotients apply unchanged. Trace/lift bounds use m. Marking rigidity must
use the degree UPPER BOUND p*m, not pretend D=m:

    (product of marking primes)^2 > 8*16^3*(p*m)^2.

Exclude p and all primes dividing N from every auxiliary transcript level.
Only prime-to-p auxiliary quotients are computed. The inseparable component
belongs to the unknown existence map, not to a new computed p-isogeny stage.
The elliptic common-field normalization applies to all homomorphisms,
including inseparable ones; its actual embeddings and point fields remain
paid. Uniform clocks, joint canonical markings and reversible cleanup
remain the old unresolved geometric obligations.

Under those obligations, source-label equality hides sigma(ker(Psi)). The
p-part is fixed, so it hides exactly the unknown cyclic separable kernel
K inside E0[m], doubled across the two factors. K need not have order m.
The known-degree source must NOT reject or misinterpret this case.

## 4. Unknown Local Depth, And Matched Classical Recovery

At ell^e || m, write K_ell=ell^(e-k) R*v for a primitive vector v=(x,y)
and 0<=k<=e. Probe upper and lower unipotents with parameters ell^j for
j=0,...,e, on one factor of the SAME doubled source. Their stability tests
are respectively

    ell^j*y^2=0 mod ell^k,   ell^j*x^2=0 mod ell^k.

At least one coordinate is a unit. Thus the MAXIMUM of the two first
successful j values is k. This takes at most 2(e+1) source comparisons.
There is NO parity restriction on e-k. Do not reuse the previous
content_exponent=(e-depth)/2 formula: that formula assumed a kernel whose
degree equals the full query modulus and is not this input model.

For k>0 the earlier local-ring phase receiver operates at ell^k, but its
queries must be explicit determinant-one lifts to the FULL ell^e component
and then CRT-embedded at m. For the affine queries, lift a unit a and u,
and use [[a,u/a],[0,1/a]] at ell^e. This reduces to the required query at
ell^k; it is not a nonexistent ring section. The previous two FULL-source
certification queries distinguish candidate lines. For ell=2 use the
already-polynomial classical digit baseline instead of a new quantum demo.

The same input gives the classical direction baseline 2(ell*k+1) comparisons.
All bounded-small-prime cases are consequently dequantized, even when the
suborder inclusion is nonprimitive. Large-prime geometry remains open; the
Boolean-interface query bound is not a lower bound for the native input.

## 5. Output The Target Order Without Guessing The p-Part

After recovering the separable kernel, let d be the product of ell^k and
let I_sep be its left annihilator ideal in O0, of norm d. This computation
uses the recovered lines and lattice arithmetic, not actual large-order
torsion points. At every prime ell != p its right order agrees with
theta^-1(End(E)), by the local kernel/ideal correspondence. At p its right
order is the unique maximal order, because d is coprime to p. Therefore

    right_order(I_sep) = theta^-1(End(E)).

The unknown inseparable factor is irrelevant for this OUTPUT. The local-
global argument avoids selecting between an isogeny and its Frobenius twist.
If m=1, the target abstract order is already O0 and no HSP is necessary.

To produce evaluable target basis maps, express each resulting rational
element through R, clear its denominator, and apply a verified published
endomorphism-division algorithm. This is a charged imported algorithm, not
one executed by this bundle. Similarly, rational right-order lattice
computation and complete receiver integration have not been implemented
here. An abstract order alone must not be mislabeled an effective basis.

## 6. What Was Actually Established, And How This Could Fail

Executed: local intertwiner recovery from KNOWN scaled actions, exact
source/target coordinate changes, nonprimitive suborder scales, p-divisible
scales, the primitive-degree countercontrol, and a supplied degree-22
inseparable map whose half-polarization is integral using modulus 2 with
no ramified split and no characteristic padding. See receipt and tests.

Mathematical deductions with written proofs: the projective-transcript
conversion and primitive degree envelope. Proposed composition requiring
independent review: their use in the full marked geometric source, unknown
local-depth receiver and target-order output. No global map or promise is
certified by passing local tests.

Decisive falsifiers and obligations:

1. A non-full source order or incompatible global dictionary invalidates
   the degree envelope and cross-prime consistency. Local table checks alone
   cannot certify these original promises.
2. Degree D=m is unjustified; p*m must be used in marking separation. An
   arbitrary nonprimitive scalar multiple violates even the divisibility
   bound. Both shortcuts are prohibited.
3. Coordinate tables at large primes are exponential in their bit length.
   Only the globally bounded SMALL auxiliary transcript is claimed.
4. The source must hide the complete marked kernel, not just polarization,
   local conjugacy or independent per-level automorphism classes. Failure
   here kills the whole proposed algorithm despite correct intertwiners.
5. A classical algorithm exploiting the actual curve and R can outperform
   the generic line baseline. Such an attack must receive all the same input
   and factorization. No native hardness or speedup is established.
6. Source construction/compilation remains unexecuted and unreviewed; the
   dimension-16 polynomial constants are not practical claims. Existing
   quantum full-suborder algorithms are prior art. Novelty remains unassessed.

The next high-value task is adversarial review of the combined geometric
source and this exact input reduction, or a native classical falsifier.
Do not spend another pass extending small supplied-map tables. Mechanical
integration must preserve the unknown-degree and unknown-depth distinctions.

## References

For primary input definitions and existing algorithmic context, see the
[Chen--Petit accepted manuscript](https://pure-oai.bham.ac.uk/ws/portalfiles/portal/259384467/suborder_to_endomorphism_ring_2_.pdf),
Sections 2-3, and the preceding large-prime audit. Standard central-simple
algebra and local-order facts are not novelty claims. The imported division
dependency is [Le Merdy--Wesolowski](https://arxiv.org/abs/2309.11912).
The complete source dependency remains the retained
[PPAV algorithms paper](https://eprint.iacr.org/2026/1142) and the separate
source, field and double-level notes, not the local tests here.
