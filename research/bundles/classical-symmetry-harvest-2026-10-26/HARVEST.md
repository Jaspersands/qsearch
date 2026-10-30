# Classical Symmetry Harvesting Before Quantum Period Finding

2026-10-26. The independent additive-source review found no fatal flaw in
the extraction lemma and required the uniform sampler qualification now
stated in Section 4. The parent's correction has not been re-reviewed.
No native PPAV automorphism computation or unknown EndRing recovery was
executed. This is an adversarial CLASSICAL attack on the preceding
additive-source proposal, not another quantum candidate or oracle problem.

## Question And Decision

Does the classical work already performed inside the proposed geometric
label source expose new endomorphisms before a quantum receiver is used?

There is an exact legal extraction procedure. Under a stated, UNPROVED
nonnegligible-success hypothesis it would yield a classical polynomial-time
full-suborder solver. The extraction does not need the unknown comparison
isomorphism or a maximal-order coordinate oracle. The hypothesis is the
research question, not an established fact.

An all-automorphisms negative control shows that growth is not automatic,
even for a proper suborder. It does not show that random queries have low
success probability. Neither the quantum proposal nor this classical attack
has an established advantage or novelty claim.

## 1. Native Contract And Available Operations

Use the SAME native input: E supersingular, p>3, and a full-rank unital
R<=O=End(E) given by efficiently evaluable basis maps. Charge native degrees,
field representations, evaluator lengths and all geometric calls. Let
d=[O:R], computable from the trace-norm discriminant. No O basis is supplied.

For a legal source query, the preceding construction gives a positive
principal matrix Z in M_g(R), with g=128 after stabilization, and integral
matrices C,F in M_g(R) satisfying, for Q=D^2,

    C^dagger C = Q Z,
    F^dagger Z F = Q I,
    F C = C F = Q I.

The represented quotient q:X=E^g -> Y is Q-polarized. There is a PROOF-ONLY
polarized isomorphism u:Y -> (E^g,Z) with u*q=F. Do not assume u can be
evaluated. All adjoints on X below use its OLD product polarization.

The [represented-PPAV framework](https://eprint.iacr.org/2026/1142),
A18-A21 and A25-A27, provides evaluation, composition, adjoints,
automorphisms and product maps on represented inputs. The label construction
already enumerates automorphisms of its canonical model to normalize the
joint marks. A classical competitor may retain those intermediate maps.
Restricting that competitor to opaque final labels would be an unfair
access restriction.

## 2. Extract Native Endomorphisms Without u

For each returned a in Aut(Y), compute the known native morphism

    L = q^dagger a q : E^g -> E^g.

Its corners L_ij=pr_i L inc_j are actual endomorphisms of the ORIGINAL E.
If the source canonicalizes Y first, replace q by its known composition with
that polarized isomorphism and use automorphisms of the canonical model.

For the correctness argument only, write w=u a u^-1. Then w is an integral
Z-unitary matrix, and

    L = F^dagger Z w F = Q F^-1 w F = C w F,
    F L C = Q^2 w,
    L^dagger L = Q^2 I.

The last identity also follows directly from q q^dagger=Q I and a^dagger a=I.
For each column j, sum_i deg(L_ij)=Q^2, hence every nonzero corner has
degree at most Q^2. Thus no unknown map, free division or unbounded degree
is concealed in extraction.

Recover coordinates of a corner x in the CURRENT R basis alpha_i using

    G_ij=Trd(alpha_i alpha_j^dagger),
    b_j=Trd(x alpha_j^dagger),        coordinates(x)=G^-1 b.

These are native trace computations by the existing small-torsion method,
not coordinates read from the unknown order. Noninteger coordinates certify
x outside R. All corners themselves are integral because they are native
morphisms, regardless of those relative coordinates.

## 3. Preserve Information Through The Converter

Require gcd(Q,d)=1 for the clean equivalence

    w in M_g(R)  iff  L in M_g(R).

The forward implication uses C,F in M_g(R). For the converse, L in M_g(R)
implies Q^2 w=FLC in M_g(R). Also d*w is in M_g(R), since d*O is contained
in R. Bezout for Q^2 and d gives w in M_g(R). This is entrywise additive
reasoning, valid for the noncommutative subring R.

Without coprimality the converse fails: the exact test has d=9, Q=9,
w outside M_2(R) but ALL corners of L inside R. A multiplier that shares
the missing index can erase the useful residue information.

There is a necessary repair: the current smooth converter requires D EVEN.
It cannot be coprime to an even d. First perform native 2-saturation:
enumerate the 15 nonzero classes x in R/2R and test whether x/2 is integral
using the published isogeny-division algorithm. If d is even, O/R has an
element of order two, so one such class succeeds. Adjoin the returned map,
close the ring, reduce its basis, and repeat. At most log2(d) strict
enlargements are needed. Norm divisibility rejects cases too small for the
division theorem before it is called. This is constant-size local algebra,
not a search through a large-prime torsion group.

After d is odd, choose even squarefree D away from p*d and larger than the
source trace threshold. Small-prime products still reach that threshold
with polynomially bounded primes: the forbidden logarithmic prime mass is
at most log(p*d). The canonical geometric object is independent of the
converter's auxiliary D. This is a legal classical use of the same source.

## 4. Conditional Classical Recovery Theorem

Suppose there exist ONE uniform classical randomized algorithm S and ONE
polynomial P with the following guarantee. For EVERY proper normalized
native order R reached adaptively by the procedure below, S uses only the
available native data, runs in time at most P(L), and outputs a legal
source query such that

    Pr[Aut(E^g,Z_query) has some w outside M_g(R)] >= 1/P(L),

where L is the ORIGINAL paid native input length, not a stage-dependent
encoding length. Query and auxiliary-frame descriptions have length at most
P(L). S may choose an admissible fixed four-square source frame for each
independent batch; it must not inspect O, use unknown geometric maps, or
receive input-specific advice. Trials at each stage use fresh independent
randomness. The guarantee must hold at every adaptively reached order,
not only at the initial order.

Instance-wise existence of good samplers or different polynomials for
different R is INSUFFICIENT. Neither S nor this uniform hitting guarantee
has been constructed or proved. This qualification resolves Finding 1 of
additive-source-independent-review-2026-10-26/REVIEW.md; the independent
report remains unchanged.

Assume the same native represented-source primitives as the quantum
proposal. Then the following is an expected polynomial-time CLASSICAL
full-suborder algorithm:

1. Adjoin the native automorphisms of E itself and 2-saturate R. These are
   required easy baselines, not evidence of a new algorithmic advantage.
2. Sample a legal polarization, construct q, enumerate ALL unmarked
   polarized automorphisms, and extract their corners L_ij.
3. If a corner lies outside R, adjoin it and close the generated ring under
   multiplication by exact trace-coordinate arithmetic and HNF.
4. Normalize the basis and its evaluator encodings as described below.
   Recompute d and continue until d=1.

Every strict enlargement lowers the positive index by a factor at least
two. Thus at most log2(d_initial) successful stages are needed. Ring closure
has the same strict-descent certificate. Under the uniform hypothesis,
the conditional expected number of trials at every stage is at most P(L),
including after any earlier adaptive history. The original-input bounds
below give one uniform polynomial B(L) for expected native construction,
extraction and normalization costs per trial. Consequently the expected
total cost is at most log2(d_initial)*P(L)*(P(L)+B(L)), plus polynomial
preprocessing. At d=1 the native integral lattice is exactly O; no hardness
assumption is needed. Correct termination does not certify the unproved
runtime hypothesis.

This theorem is CONDITIONAL on the hitting hypothesis. Neither enumeration
of a few visibly known symmetries nor a supplied full-order fixture can
establish it. A small query set with no growth cannot refute all such
distributions or establish native quantum advantage.

### Avoid Exponential Height And Program Growth

It is insufficient to say each stage is polynomial in its own enlarged
input. Repeated polynomial expansion over log(d) stages could be exponential
in the original input. Normalize after each strict lattice enlargement.

In dimension four, the norm lattice of R' has covolume p*[O:R']/4, and
every nonzero vector has squared length equal to a positive integer degree.
Minkowski's second theorem bounds the fourth successive minimum by a
constant times p*[O:R']; fixed-dimensional lattice reduction therefore
gives basis degrees <=C*p^2*[O:R']^2 for a universal constant C. Bit heights
are bounded in terms of the ORIGINAL log(p), log(d), not a stage recurrence.

Compress the corresponding native basis evaluators as well. To stay within
the explicitly prime-to-p interpolation interface, for each endomorphism
x choose c in {0,1,2} such that

    deg(x+[c]) = deg(x)+c*Trd(x)+c^2

is nonzero modulo p. A degree-two monic polynomial over p>3 cannot vanish
at all three distinct residues. Interpolate/compact x+[c] using its known
small-torsion images and retain x as that compact map minus [c]. This avoids
assuming prime-to-p degree for every extracted corner or silently extending
Theorem 7.1 to an inseparable target multiplier. The native endpoints are
already represented elliptic curves. The algorithms and uniform field costs
must still be paid; the local scalar-shift helper does not execute them.

## 5. A Complete Failure Control, Not A Failed Symmetry Search

Choose an admissible Pell pair n,k with n^2-2k^2=1, n>1. In the additive
source fix roots (2k^2,2k,0,0), whose square sum is n^4-1. At gamma=0,
let J=[[0,-1],[1,0]], R0=diag(J,J), and define the scalar integer matrix

    P8 = [[I+k R0, k R0],
          [k I,    R0+k I]].

It has the integral inverse

    P8^-1 = [[I-k R0, -k I],
             [k R0,    k I-R0]].

For P=P8 tensor I2, direct multiplication gives Z_0=P^T P. Thus the
unmarked polarized source is the STANDARD product E^16, up to a known
integral scalar change of coordinates. Stabilization gives E^128 and does
not change the conclusion.

Every automorphism of the standard product is monomial with entries in
Aut(E): its column norms sum to one, forcing exactly one norm-one entry
per column, and unitarity forces a permutation of rows. Consequently, if
the easy baseline already adjoined Aut(E) to R, ALL automorphisms of Z_0
have entries in R. Every extracted corner lies in R, even if R is proper.
This is a proof for the entire group, not an unsuccessful finite search.

The exact supplied-order control uses p=11, n=17, k=12 and an index-17
suborder stabilizing an i-eigenline modulo 17. It contains all four units
of the ambient order. Conjugated adjacent swaps and one coordinate unit
generate the entire automorphism group, and all their entries stay in R.
The example is an arithmetic witness to a failed UNIVERSAL growth claim,
not a hard native EndRing instance or an executed PPAV computation.

Only this zero query and the stated four-square choice are covered. There
is no conclusion about the success probability of nonzero/random queries,
other four-square choices, or different polarizations.

## 6. Research Consequences And Falsifiers

- The complete quantum-source implementation must expose this classical
  leakage test. Its own automorphism list cannot be withheld from a fair
  competitor. Record native index before/after, complete-list provenance,
  and whether missing information survived the coprime converter.
- Formal symmetries built solely by ring operations from M_g(R) cannot
  enlarge R. Enumerating words in known copy permutations or scalar
  symmetries is not a substitute for the actual geometric automorphism
  computation.
- Framed automorphisms are not the target: the two-inclusion frame has
  trivial stabilizer at a fixed gamma. Harvest the UNMARKED variety.
- Reuse the earlier projector extraction analysis; it is not new here.
  A28 irreducible decomposition does not automatically yield elliptic
  factors, and its previous Frobenius obstruction remains scoped to
  projectors rather than all automorphisms.
- A uniform hitting theorem would dequantize the full-rank source problem
  and could itself be valuable. A vanishing hitting rate for one sampler
  does not validate the proposed quantum advantage. Source correctness,
  novelty, other classical attacks and the full-rank input barrier remain.

Next: determine the information content of automorphisms at NONZERO queries,
or find a theorem on the sampled polarization family that implies or rules
out nonnegligible growth. Do not build the enormous geometric backend or
add more easy-unit examples without a hypothesis about that distribution.
