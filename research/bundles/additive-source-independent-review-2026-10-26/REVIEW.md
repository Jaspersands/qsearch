# Independent Adversarial Review: Additive Source And Symmetry Harvest

Date: 2026-10-26. One authorized reviewer, working independently. This is the
original review resumed after an interruption, not a second review or an
endorsement of the author's self-audit. No agents were started or chats messaged.

## Verdict

**No fatal flaw found in the additive framed-source reduction under the exact
native-input promises and the stated represented-PPAV algorithm contract.**
The frame really forces integral additive translation, including over the full
unknown quaternion order. The finite frame has the same equivalence relation.
The explicit quadratic stabilization supplies a route to represented models;
an unknown maximal order, reference curve, or evaluable comparison isomorphism
is not needed. Missing execution of these published algorithms is not a
mathematical counterexample.

**The classical pullback/extraction lemma survives the review.** Coprimality of
the converter multiplier with the current index is essential to its converse.
Useful symmetries yield native maps outside the current order, and the stated
height/compression strategy can keep the costs polynomial. **No nonnegligible
hitting probability is established.** The recovery theorem is conditional,
with a uniformity qualification detailed below. The complete zero-query failure
control is valid but does not settle any random-query distribution.

This is a bounded mathematical review, not a formal verification of the
imported PPAV paper, an executed geometric algorithm, a novelty certificate,
or a proof of quantum advantage. The parent's separate stable-product audit
is outside this review; no conclusion from it is assumed or reproduced here.

## Severity-Ranked Findings

### 1. [P2] State a uniform sampler, not an instance-wise existence hypothesis

Location: [HARVEST.md:116](/Users/jaspersands/Developer/qsearch-research-work/classical-symmetry-harvest-2026-10-26/HARVEST.md:116),
lines 116-127 and 138-147.

Literally, "for EVERY ... R, there is a polynomial-time samplable distribution"
has the quantifiers `for every R, there exists a sampler`. That alone does not
give the one algorithm required by the claimed uniform expected-polynomial
solver. A different sampler could hard-code a good query for each individual
input, without a procedure for finding that sampler from the native input.
Likewise, the polynomial in the success bound must not vary with R.

The sufficient hypothesis is: there exist **one uniform classical randomized
algorithm S and one polynomial P**, such that, on every proper normalized
native order reached by the procedure, S uses only the available native data,
runs in time P(L), and outputs a legal query with probability at least 1/P(L)
of exposing an automorphism outside M_g(R). Its query and auxiliary-frame
descriptions must have uniformly polynomial length. Here L is the original
paid input length, and this guarantee must cover every adaptively reached R.

Under that interpretation, the conditional recovery proof is sound. This is
a formal missing qualification, not a counterexample to the intended uniform
hitting conjecture. No sampler or hitting theorem was found in the code or
receipt. The note correctly labels hitting as unproved; it must remain so.

**No P0/P1 contradiction was found within the assigned scope.** In particular,
the absence of a dimension-128 implementation is not promoted to a finding
against the mathematical reduction. The following limitations are already
acknowledged in the source and are not newly discovered bugs: enormous fixed
costs, lack of a native run, lack of a classical lower bound, and lack of a
novelty proof.

## Exact Theorem Scope

The additive conclusion supported by this review is the following conditional
composition statement.

1. Input is an actual supersingular elliptic curve E over an explicitly
   represented finite field of characteristic p>3, and four genuine native
   endomorphisms forming a Z-basis of a full-rank unital suborder R of the
   geometric O=End(E). A binary degree bound, evaluator descriptions, their
   polynomial evaluation bounds on the required extension-field points, and
   compatible field representations are paid input. These are promises, not
   properties certified merely by finite trace transcripts.
2. Import the always-correct expected-time represented-PPAV operations used
   from the retained 2026/1142 paper: small-torsion arithmetic, quotients with
   the stated definition-field behavior, products, geometric polarized
   isomorphisms, automorphisms, and canonicalization. Use the explicit
   genus-one theta conversion, not representability alone, for the original E.
3. Fix the source four-square matrix T, base field, embeddings, torsion bases,
   marking primes and auxiliary prime plan before coherent queries. Marks are
   signed points and unordered graph relations with separately fixed labels.
   All levels and all relations are compared under one common isomorphism.
4. Use unconditional expected-polynomial four-square algorithms, bounded
   field arithmetic/descent, standard reversible simulation, finite-abelian
   HSP, and the published native isogeny-division algorithm. These operations
   and the initial evaluators are charged, not treated as unit-cost oracles.

Then d=[O:R] is computable, and for d>1 the construction gives a canonical
classical label on A=R/dR with fibers exactly H=dO/dR. For each error parameter
epsilon, a bounded polynomial-size reversible evaluation circuit can be
sampled whose entire A-domain is correct with probability at least
1-epsilon. Abelian HSP plus lattice reconstruction and native division gives
a bounded-error quantum polynomial-time full-order computation in the paid
input length. For d=1, the supplied basis already is the answer.

This needs no additional GRH or quaternion norm-distribution assumption in the
additive route. That statement is relative to the imported geometric theorem's
contract, whose complete proof was not independently re-proved here. It is
not an unconditional certification of every subroutine in that paper.

There is no theorem here for a bare curve, one non-scalar endomorphism,
rank-two commuting input, arbitrary evaluator programs, growing geometric
dimension, or practical cryptographic cost. The classical conclusion requires
the additional **uniform** hitting hypothesis in Finding 1.

## Independent Proof Checks

### Native coordinates, index, and norm

References: [ADDITIVE_SOURCE.md:24](/Users/jaspersands/Developer/qsearch-research-work/additive-framed-source-2026-10-26/ADDITIVE_SOURCE.md:24),
lines 24-47; [PREPROCESSING.md:45](/Users/jaspersands/Developer/qsearch-research-work/native-suborder-preprocessing-2026-10-26/PREPROCESSING.md:45),
lines 45-80.

Small prime torsion gives reduced traces of words of length at most three.
The bound |Trd(word)|<=2 B^2 makes centered CRT with product greater than
4 B^2 sufficient. Solving the nondegenerate trace system reconstructs the
table, identity, and involution of R, without locating O in a reference algebra.
Only Section 2 of this preprocessing is needed; its later reference-curve,
dictionary, GRH, and quantum-factorization branches are not imported.

For G_ij=Trd(alpha_i alpha_j^dagger), det(G)=p^2 d^2. Since the norm inner
product is G/2 in dimension four, its covolume is p*d/4, not p*d. The index
formula in the additive note is nevertheless correct because it uses G.
The finite group O/R has order d, so dO is contained in R and |dO/dR|=d.
Changing a representative in R/dR adds an integral element to gamma.

The norm bound follows from the triangle inequality for sqrt(Norm):
sqrt(Norm(beta)) <= sum_i u_i sqrt(Norm(alpha_i)) < 4d sqrt(B).
It is uniform over the entire query domain. No restriction gcd(d,p)=1 is
needed; only the auxiliary torsion primes must avoid p.

### Principal polarization and the full quaternion frame

References: [ADDITIVE_SOURCE.md:49](/Users/jaspersands/Developer/qsearch-research-work/additive-framed-source-2026-10-26/ADDITIVE_SOURCE.md:49),
lines 49-132; [additive_source.py:104](/Users/jaspersands/Developer/qsearch-research-work/additive-framed-source-2026-10-26/additive_source.py:104),
lines 104-167.

Write A=I4 tensor L, B=I4 tensor adj(L), and K=T tensor I2.
Then AB=n^4 I, KK^dagger=(n^4-1)I, A+B=tI, and K commutes with A,B.
Block multiplication therefore gives Z^2-tZ+I=0. Its Schur complement is
B-K^dagger A^-1 K=A^-1, proving positivity. The integral inverse tI-Z
proves principality. On the product of elliptic curves, these integral
Hermitian matrices have scalar integral diagonal entries and define the
claimed polarizations. The real quaternion realization is used for proof,
not as supplied computational data.

Integral shears give the forward congruence even when beta and delta do not
commute: U_gamma U_delta=U_(gamma+delta). The adjugate transformation is
n^4 times the inverse-congruence identity, so it remains valid when t changes.

For the converse, commuting with the separately labeled matrix units forces
two repeated 2-by-2 blocks over O. This is a coefficientwise matrix-unit
calculation over any ring, not a scalar-matrix assumption. At g=128 the
32-copy frame includes operators between different stabilizing copies; a
fixed regrouping permutation converts the eightfold product ordering to this
two-block ordering. The cross equation is

    (I8 tensor T) tensor (W^dagger V) = (I8 tensor T) tensor I2.

Since n>=2, T is invertible over Q, forcing V=(W^dagger)^-1.
W e1=e1 and V e2=e2 imply W^dagger e2=e2, hence
W=[[1,delta],[0,1]] with delta in O. The upper-right entry of
L'=W^dagger L W then gives beta'-beta=n*delta. This proves the precise
equivalence beta'-beta in dO, not just a norm or discriminant condition.

### Finite marks and a single common isomorphism

Reference: [ADDITIVE_SOURCE.md:134](/Users/jaspersands/Developer/qsearch-research-work/additive-framed-source-2026-10-26/ADDITIVE_SOURCE.md:134),
lines 134-170 and 204-224.

For an invertible map w, equality of the graph relation under w on both
coordinates is exactly w e=e w on the indicated torsion. It does not fix
the domain points individually. The ordered images of the two E[s] basis
pairs instead impose pointwise equality of the two inclusions, as intended.

Both source polarization matrices have real eigenvalues between 1/T_max
and T_max. From w^dagger Z w=Z', one obtains ||w||_op<=T_max. With quaternion
Frobenius norm squared defined as the sum of entry degrees,

    ||we-ew||_F^2 <= 4g T_max^2,
    ||w iota-iota||_F^2 <= (T_max+1)^2.

An integral map killing all prime-to-p marking levels factors through
[Rmark], entrywise. A nonzero integral quotient entry has degree at least
one. Thus Rmark^2>8g T_max^2 forces exact agreement, with ample slack.
This uses the entry-degree norm, not an unmentioned factor of two from the
PPAV trace norm. The published PPAV convention is
||a||_PPAV^2=Tr(a^dagger a)=2 sum_ij deg(a_ij) on E^g.

Canonicalizing the unmarked model, transporting all marks by one computed
isomorphism, and minimizing the entire tuple over its full automorphism
group is enough: equality of the resulting labels supplies one common
isomorphism of all marks. The proof never minimizes independently per level
or per relation. Ordered full graphs, missing inclusions, or fresh T per
query would be different and incorrect constructions.

### Effective model conversion and fields

References: [ADDITIVE_SOURCE.md:172](/Users/jaspersands/Developer/qsearch-research-work/additive-framed-source-2026-10-26/ADDITIVE_SOURCE.md:172),
lines 172-217 and 226-261;
[SMOOTH_REPOLARIZATION.md:69](/Users/jaspersands/Developer/qsearch-research-work/smooth-repolarization-2026-10-23/SMOOTH_REPOLARIZATION.md:69),
lines 69-152;
[PRIME_SQUARE_FLAGS.md:25](/Users/jaspersands/Developer/qsearch-research-work/prime-square-flags-2026-10-23/PRIME_SQUARE_FLAGS.md:25),
lines 25-74 and 98-141.

The converter needs the quadratic identity, not a dimension-two hypothesis
once that identity is supplied. Here t>=2n^2>=8. For c=gcd(t+2,t-2)|4 and
even D>t+2, the stated modular coin construction gives nonnegative X,Y.
The eight coefficients are commuting self-adjoint polynomials in Z, so the
eight-square matrix identity applies despite the ambient noncommutative
endomorphism algebra. Consequently F=Z8^-1 C^dagger is integral and
F^dagger Z8 F=D^2 I, FC=CF=D^2 I.

Its kernel is available by evaluating native maps on small r^2-torsion of
the old E^128. A direct A26 call at r^2 is permitted by that primitive's
stated contract. The refined alternative is also correct: for maximal
isotropic G, rG is isotropic, G[r]=(rG)^perp, and extending rG to a
Lagrangian J gives a two-stage polarized quotient, including nonfree G.
Neither approach assumes that rG itself is already Lagrangian.

The equality of kernels and multipliers gives u q=F, where u is only used
in the proof. For s not dividing D, q([D^-2 mod s] C(P))=u^-1(P).
Both coordinates of every graph pair are transported this way. This is an
actual construction from the old model followed by published quotients;
it is not an invocation of geometric representability as a converter.

Field references: [FIELD_NORMALIZATION.md:39](/Users/jaspersands/Developer/qsearch-research-work/elliptic-field-normalization-2026-10-25/FIELD_NORMALIZATION.md:39),
lines 39-68 and 104-120;
[ELLIPTIC_INPUT.md:32](/Users/jaspersands/Developer/qsearch-research-work/elliptic-theta-input-2026-10-26/ELLIPTIC_INPUT.md:32),
lines 32-159.

The supersingular Frobenius cases give pi^12=[q^6]; hence rational 8-torsion
and definition of geometric endomorphisms over F_(q^12). The explicit
L(4O) construction retains y and therefore point signs. Its translation
matrices are certified by degree-eight section identities; normalization
of the Heisenberg action needs at most one further degree-four extension.
Thus the conservative fixed base F_(q^48) suffices for this route.

All quotient intermediates inherit the same scalar Frobenius. This makes
every chosen flag rational and forces geometric homomorphisms between the
intermediates to descend. Separate r^2 and s torsion fields have relative
degrees at most r(r-1) and s-1. Temporary joint fields have polynomial
degree, and outputs must be converted back through the specified embeddings
after each stage. Galois minimization is not geometric canonicalization.
Effective quotient/definition-field handling remains an imported A26
contract, not a consequence of abstract stability alone.

### Uniform costs, coherent evaluation, and output

References: [ADDITIVE_SOURCE.md:236](/Users/jaspersands/Developer/qsearch-research-work/additive-framed-source-2026-10-26/ADDITIVE_SOURCE.md:236),
lines 236-275; [UNIFORM_SOURCE_CLOCK.md:68](/Users/jaspersands/Developer/qsearch-research-work/elliptic-theta-input-2026-10-26/UNIFORM_SOURCE_CLOCK.md:68),
lines 68-168.

The dimensions are 16 before the converter and 128 after it. There are
2048 graph relations, s^256 pairs per relation, and 4^128 theta coordinates
per point. The direct primary kernel list has r^256 points; refinement
uses two lists of r^128 points. These are output-list counts, not total
operation counts. Even brute-force searching all old r^2-torsion would
cost r^512 at fixed g, still polynomial in small r. A linear-algebra kernel
calculation avoids that particular enumeration.

The largest auxiliary primes and their number are polynomial in the paid
input length: the required product logarithms are polynomial and excluding
p, D, or p*d removes only polynomial logarithmic prime mass. Object sizes
are controlled over the fixed base; point sizes over separate polynomial
degree extensions. Flattened quotient chains prevent recursive duplication.
Applying the imported fixed-dimension polynomial bounds to these uniformly
bounded interfaces gives a whole-label expected bound B(L). The constants
are prohibitive, but no input-dependent dimension is hidden in this step.

For each query, a 2B cap fails with probability at most 1/2. Repeating
h>=ceil(4 log2(d)+log2(1/epsilon)) times and union-bounding over d^4 queries
gives one good frozen tape with probability at least 1-epsilon. No
independence across queries is required. Successful outputs must be exact
canonical labels; reversible copy/uncompute must erase all intermediate
choices. This is a valid uniform construction argument, not a compiled
oracle. Ordinary finite-abelian Fourier sampling is sufficient, with its
approximation/repetition error included in the total error budget.

For recovered generators h_j, Gamma=<d e_i,h_j> has determinant d^3 exactly
when the proposed subgroup has size d. The lattice Gamma/d contains R.
If its four basis maps are genuinely integral, it is contained in O; the
index d then forces equality with O. Ring closure need not be separately
assumed for that last containment-and-index argument.

Index alone is insufficient. Independently recomputing the R=Z+3O control
with d=27 and spurious subgroup <e1> gave det(Gamma)=19683=27^3 and the
nonintegral output [1]/27. Its numerator degree is 1, and its quotient
degree is 1/729. This is not a counterexample to the specified verifier:
the imported division algorithm first rejects when deg(beta)/d^2 is not
a positive integer. A valid nonzero quotient automatically has
deg(beta)>=d^2>d, meeting the displayed division theorem's precondition.
The zero map is handled separately. The division result does not require
d or the input isogeny's degree to be prime to p; its auxiliary torsion is.

## Classical Competitor

### What is proved

References: [HARVEST.md:24](/Users/jaspersands/Developer/qsearch-research-work/classical-symmetry-harvest-2026-10-26/HARVEST.md:24),
lines 24-112 and 149-174;
[harvest.py:42](/Users/jaspersands/Developer/qsearch-research-work/classical-symmetry-harvest-2026-10-26/harvest.py:42),
lines 42-124.

For an unmarked polarized automorphism a of the represented Y, the native
map L=q^dagger a q is computable. Writing w=u a u^-1 only in the proof,

    L=F^dagger Z w F=C w F,
    F L C=Q^2 w,
    L^dagger L=Q^2 I,                 Q=D^2.

Thus each corner on the original E is integral and has degree at most Q^2.
Mixed traces and G^-1 recover its rational R-coordinates without knowing O.
An outside corner strictly enlarges the order. Conversely, when gcd(Q,d)=1,
L in M_g(R) gives both Q^2 w and d w in M_g(R); Bezout gives w in M_g(R).
This proves the claimed equivalence, entrywise, without commuting ring
elements or evaluating u. Computing q^dagger atom by atom charges only the
small quotient factors, rather than enumerating the full Q-torsion.

Because D is even, 2-saturation is necessary before demanding coprimality.
The 15 nonzero classes of R/2R suffice: if d is even, the finite abelian
group O/R has an element of order two. Its doubled representative lies in
R but not 2R. Native division finds an integral half, and each strict
enlargement reduces the index by at least two. The same argument covers
ring closure by exact rational coordinates and HNF.

The resource repair is substantive. With every nonzero integral norm at
least one, Minkowski's second theorem bounds the fourth successive minimum
by C*p*[O:R']; fixed-dimensional reduction gives basis degrees at most
C'*p^2*[O:R']^2. Normalization and evaluator compaction must occur after
each strict enlargement, including closure steps. For x+[c], c in {0,1,2},
the monic quadratic deg(x)+c Trd(x)+c^2 cannot vanish at all three residues
modulo p>3. The selected prime-to-p map can be compacted using interpolation
on paid small torsion; subtracting [c] recovers x. This removes a possible
iterated program-length blowup, assuming the imported interpolation routine.

Under Finding 1's uniform hypothesis, there are at most log2(d_initial)
successful stages and polynomial expected trials per stage. This is a
conditional classical solver, not evidence that the hypothesis holds.

### What the failure family actually proves

References: [HARVEST.md:176](/Users/jaspersands/Developer/qsearch-research-work/classical-symmetry-harvest-2026-10-26/HARVEST.md:176),
lines 176-211;
[test_harvest.py:80](/Users/jaspersands/Developer/qsearch-research-work/classical-symmetry-harvest-2026-10-26/test_harvest.py:80),
lines 80-125.

For the stated Pell pair and fixed four-square choice, the explicit integral
unimodular P gives Z_0=P^T P. Every product-polarized automorphism of E^g
has columns whose integral nonnegative entry norms sum to one, so it is a
monomial matrix with entries in Aut(E). If R contains these units, conjugating
by scalar integral P and P^-1 keeps every entry in R. Stabilization preserves
this conclusion. The zero query therefore fails for the entire automorphism
group, not merely for a searched subset.

The p=11, index-17 order supplies a proper admissible example: the preimage
of the stabilizer of an i-eigenline modulo 17 has index 17 and contains all
four units of the ambient order. In the usual basis
1,i,(1+j)/2,i(1+j)/2 with j^2=-11, norm one forces the last two coefficients
to vanish, leaving precisely +/-1,+/-i. Thus the full-unit assertion also
has a direct norm proof, not just a finite search interpretation.

This disproves "every legal query grows every proper order." It does not
bound the success probability at nonzero queries, at other choices of T,
or for another admissible sampler. The positive supplied-unit controls are
not hard native instances and do not establish progress after the mandatory
easy-unit baseline. The coprimality failure control d=Q=9 is also genuine:
useful w can be erased from every pulled-back corner when Q shares the index.

## Concrete Falsifiers And Non-Falsifiers

- A common integral polarized isomorphism preserving the complete specified
  finite frame with beta'-beta not in dO would falsify the additive theorem.
  The centralizer and degree arguments above rule this out under the stated
  hypotheses; none was found.
- An actual failure of the imported quotient/canonicalization operations on
  these legal inputs, or a required superpolynomial field/encoding size,
  would defeat the source-cost composition. A missing implementation alone
  does not do so. This review does not certify every proof in the PPAV paper.
- Dropping an inclusion, ordering an entire graph, changing T per query,
  keeping auxiliary choices in the output, or allowing independent
  isomorphisms per level changes the function. The first three have exact
  negative controls in the reviewed tests. They are not the specified source.
- A counterexample to coprime extraction would require C,F in M_g(R),
  gcd(Q,d)=1, w integral and Z-unitary outside M_g(R), but CwF entirely in
  M_g(R). The displayed Bezout identity forbids this. Dropping coprimality
  gives the existing d=Q=9 counterexample.
- To refute a proposed uniform harvest sampler, exhibit a family on which
  its success becomes smaller than every inverse polynomial, or zero. To
  refute existence of all such samplers requires a substantially stronger
  obstruction. A zero-query example proves neither assertion.

## Prior Art And Novelty

[COMPARISON.md:8](/Users/jaspersands/Developer/qsearch-research-work/additive-framed-source-2026-10-26/COMPARISON.md:8)
correctly identifies Chen--Petit as prior art for the same full-rank endpoint.
The retained accepted manuscript was read at PDF pages 4, 8-9, 12, and 17-18:
Theorem 1 is explicitly heuristic; Remark 2 charges basis heights; the route
uses a reference order and weak isogeny. Lemmas 8/10 use GRH for the general
small reference parameter; Proposition 26 and Remark 27 expose additional
norm-solving/strong-approximation heuristics. These are separate assumptions.
[Primary accepted manuscript](https://pure-oai.bham.ac.uk/ws/portalfiles/portal/259384467/suborder_to_endomorphism_ring_2_.pdf).

The mechanism checked here is different: additive R/dR, integral-translation
labels from framed polarizations, and ordinary abelian HSP, without that
reference/dictionary/lifting route. Under the imported model contract, it
avoids those particular reference and norm-distribution assumptions. This
is a defensible mechanism/assumption comparison, not a first-solver claim.
The local reference preprocessing's GRH branch is not secretly needed by
the additive construction.

Only selected primary sources and limited fresh searches were checked.
No exhaustive subsequent-literature comparison or non-obviousness claim
is justified. Classical harvesting uses publicly available geometric
operations and must receive intermediate maps as well as final labels;
opaque-label or membership-only lower bounds are not native hardness proofs.

## Verification Performed

All commands ran with working directory
`/Users/jaspersands/Developer/qsearch-research-work`. Python bytecode writing
was disabled; pytest caching and automatic third-party plugin loading were
disabled. No source bundle was edited.

- **215 passed in 37.61s**, warnings as errors, no skips: the two assigned
  test modules plus smooth-repolarization, prime-square-flags,
  native-suborder-preprocessing, elliptic-theta-input, and
  elliptic-field-normalization. Interpreter: `/opt/anaconda3/bin/python`.
- Both original `replay_additive_source.py --check` and
  `replay_harvest.py --check` completed with exit code zero. Neither was run
  with `--write`.
- Independently recomputed **all 19 dependency hash entries** in the two
  receipts; all matched. Receipt hashes remained
  `57725d72e078ec35bd3460c66439e5475c427c450880a0aa2dd12194a1f67bb9`
  and `0d68b2df50149d61fdec2fdfe6f71e3f71507a8df9faf4f2f7472efe1ae73272`.
- An independent in-memory arithmetic check covered **156 squarefree
  auxiliary-prime plans and 624 coin/rigidity-bound cases**: n=2,...,40,
  B in {1,2,11,101}, avoiding characteristic 11, and four trace values per
  plan including endpoints. All passed; the largest prime used was 23.
  A first reviewer harness attempt had an incorrect strict-bound rounding
  for D and aborted; replacing it by the actual squarefree prime-product
  construction resolved that harness error. It was not a source failure.
- Independently recomputed the false index-only candidate described above.
  This confirms the need for native division; it does not falsify the full
  verifier, whose imported algorithm rejects the nonintegral degree first.
- Independently derived the block identities, full-order frame centralizer,
  finite-mark norm lift, native pullback and Bezout argument, height bound,
  and all-automorphism zero-query obstruction. These deductions, not the
  finite tests, support the theorem-scope verdict.

Reproduction of the test run:

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider -W error \
  additive-framed-source-2026-10-26/test_additive_source.py \
  classical-symmetry-harvest-2026-10-26/test_harvest.py \
  smooth-repolarization-2026-10-23/test_smooth_repolarization.py \
  prime-square-flags-2026-10-23/test_prime_square_flags.py \
  native-suborder-preprocessing-2026-10-26/test_native_preprocessing.py \
  elliptic-theta-input-2026-10-26/test_elliptic_theta.py \
  elliptic-field-normalization-2026-10-25/test_elliptic_fields.py
```

Primary-source inspection:

- The retained 44-page [PPAV paper](https://eprint.iacr.org/2026/1142),
  SHA256 `4504310844c227e0d49c8c628b03e9942894f14fcd6f5881dc5c0122ed645318`:
  read complete relevant PDF pages 5-15 and 24-36, including A1, A7,
  A18-A27, the theta representation/isomorphism results, Theorem 6.25 and
  Theorem 7.1. The import is a published preprint theorem, not locally
  executed software or a full independent verification of its proofs.
- [Isogeny division, version 4](https://arxiv.org/html/2309.11912v4#S4):
  checked Theorems 4.1/4.22, Algorithm 1's degree rejection, and the
  auxiliary-prime/evaluator costs. No separability assumption on the input
  map or prime-to-p restriction on the divisor is silently added.
- [Pollack--Trevino](https://math.colgate.edu/~integers/sjs15/sjs15.pdf):
  checked the distinction between ERH-dependent and unconditional
  randomized four-square algorithms, including conversion to bit cost.
- Chen--Petit local accepted PDF, SHA256
  `554c6a9f0f49cc13a59e38bf20a351a797137938dce18bd546a9ecf47a656402`.
  The live accepted-PDF URL was inaccessible through the web tool; the
  retained primary manuscript was read directly. Search snippets and
  secondary summaries were not used as theorem evidence.

## Files Changed And What Remains Unestablished

Only this new file was created:

`/Users/jaspersands/Developer/qsearch-research-work/additive-source-independent-review-2026-10-26/REVIEW.md`

No new counterexample program was needed: no counterexample to the fully
specified reduction was found, and the scoped negative controls already
exist in the preserved bundles. Historical receipts still say "unreviewed";
they were not rewritten to incorporate this later report.

Not performed or established: native dimension-128 quotients, complete
geometric labels, native pullbacks, native 2-saturation or map compression,
output-map division, quantum circuits or hardware, unknown EndRing recovery,
a uniform harvest sampler/hitting theorem, a native classical lower bound,
practical runtime, exhaustive novelty, or the parent's stable-product audit.
No Desktop, migration/staging, checkpoint, registry, UI, or Git changes were
made. All review command sessions completed.
