# Bounded-Codimension HSP: Public Abelian-Ideal Reduction

30 October follow-up: the [hybrid parameter bound](BOUNDED_CODIMENSION_HYBRID_BOUND.md)
combines the same reduction with whole-grade cancellation and a paid
classical collision branch. Conditional on the same Rees proof, its
all-prime parameter factor is `2^O(k^2 log(k+2))`, improving the historical
scalar-line bound below. It establishes no native application or speedup.

Date: 2026-10-23. Status: LOCAL PROOF; independent review pending.
Public algebra implemented and tested. No quantum receiver, unknown hidden
intersection learner, useful application, novelty certification or speedup
claim is supplied by the implementation.

## Question And Answer

Can a small hidden codimension replace the ambient nilpotency-class bound
in the proposed Rees route? Yes, conditionally on that route's remaining
whole-proof obligations. A public abelian-ideal procedure reduces the input
to abelian HSP calls and a remainder with dimension at most k(k+1)/2 and
class at most 2k-1. The original class may grow with the input dimension.

The reduction itself does not use the Rees construction. It uses ordinary
abelian HSP to learn COMPLETE intersections and classical normalizers.
Only its bounded-size terminal solver depends on the proposed Rees theorem.
For k<=2 the terminal group has class at most two, so the published nil-2
algorithm suffices instead. This special case is a corollary using known
machinery, not a claim of an independently new quantum primitive.

## Input And Output Contract

- An explicit n-dimensional nilpotent Lie algebra L over a verified odd
  prime field F_p. Its actual class c satisfies c<p; c need not be fixed.
- Canonical field coordinates and genuine bilinear structure constants,
  with a polynomial-time reversible implementation of their arithmetic.
- An ordinary coherent oracle f on G=exp(L), with equal labels exactly
  on left cosets of H=exp(h). Thus f(x)=f(y) iff x^{-1}y is in H.
- A promise codim_L(h)<=k. The desired output is a basis of h.
- Input construction, oracle label width and evaluation cost remain paid.

For k=0, h=L follows from the promise. The zero algebra also needs no
oracle. Nonzero abelian remainders are solved by ordinary abelian HSP.
There is NO claim that arbitrary black-box growing-class groups can be
converted to this input in polynomial time, nor that a copy-only source
supplies these ordinary oracle queries for free.

The frozen-table interface validates alternating structure, antisymmetry,
Jacobi, nilpotence and c<p. It then uses the resulting bilinear table for
every operation. It does not certify that an external nonlinear callback
agrees with this table away from basis vectors. An actual oracle must use
the SAME validated group law. Replacing its law by a table is not allowed.

## 1. Construct A Maximal Abelian Ideal

Start A_0=0. Given an abelian ideal A_j, solve the linear constraints

    [x,A_j]=0,        [L,x] subset A_j.

If there is a solution outside A_j, adjoin it as the next basis vector.
Then A_(j+1) is again an abelian ideal, and the retained ordered basis
satisfies [L,A_i] subset A_(i-1) for each i. No search through subspaces,
maximum-dimension optimization or enumeration of F_p is required.

Why does termination give C_L(A)=A? The centralizer C_L(A) is an ideal:
Jacobi and the ideal property of A imply [L,C_L(A)] subset C_L(A).
If C_L(A)/A is nonzero, its L-action is nilpotent because L is nilpotent.
Take the last nonzero member of its iterated-action filtration. Every
vector in that member is killed by all of L. A lift x therefore satisfies
the two extension constraints and lies outside A, a contradiction.
Consequently A is self-centralizing, and in particular inclusion-maximal.

Let a=dim A. The faithful action of L/A on A lands in strictly triangular
a-by-a matrices in the constructed flag basis. Hence

    dim L <= a + a(a-1)/2 = a(a+1)/2.

The triangular image has class at most a-1, so gamma_a(L) subset A.
Another a brackets with L kill A through its flag. Therefore

    class(L) <= 2a-1.

This proof uses nilpotence over the given field, not a characteristic-zero
Borel fixed-point theorem. The abelian-ideal bounds are standard Lie
algebra material, not a novelty claim. Related prior-art context includes
[Burde and Ceballos](https://arxiv.org/abs/0911.2995); its characteristic-zero
results are not being imported as finite-characteristic justifications.

An abelian SUBALGEBRA cannot replace an ideal. In the standard filiform
algebra with [e_0,e_i]=e_(i+1), span(e_0,e_(n-1)) is self-centralizing and
abelian of dimension two, despite unbounded n. It is not an ideal.

## 2. Learn The Intersection And Normalize It

If a<=k, the preceding bounds already give the desired terminal size.
Otherwise the dimension inequality forces

    K = h intersect A,       dim K >= a-k > 0.

Because exp(A) is elementary abelian, f restricted to exp(A) is an ordinary
abelian HSP oracle hiding exp(K). Learn the complete subspace K.

For y in h and x in K, [y,x] belongs both to h and to A. Thus h normalizes
K. Compute the public normalizer

    S = N_L(K) = { y : [y,K] subset K }.

It contains h, and K is an ideal in S. Work in the Lie quotient S/K.
Writing d=n-dim S, its hidden subalgebra has codimension

    codim_(S/K)(h/K) = codim_L(h)-d <= k-d.

The next bound is min(dim(S/K),k-d). The quotient dimension is strictly
smaller than n because K is nonzero. If S=K, the hidden subalgebra was
exactly K and there is no remaining instance.

Normalizing first is essential. K need not be an ideal of all of L, so
quotienting L/K directly can be mathematically undefined.

## 3. Oracle Transport Does Not Require A Homomorphic Section

Choose any public linear section sigma:S/K -> S. Exponentiating it gives
a section of exp(S) -> exp(S/K). Define

    f_new(q) = f(exp(sigma(log q))).

For two quotient elements, the difference of their lifted representatives
projects to q_x^{-1}q_y. Since K is normal in S and K subset H,

    lifted difference in H  iff  q_x^{-1}q_y in H/K.

Therefore f_new hides H/K exactly even when sigma is not a Lie or group
homomorphism, and even when K is noncentral. Replacing a representative by
another in the same K-coset cannot change its f-label.

One f_new query uses one parent f query, plus reversible section evaluation
and uncomputation. Composing at most n such sections preserves this query
count; the polynomial arithmetic/ancilla cost is not free. Recover h from
the quotient answer by taking its section lifts together with K, then
unwind the preceding reductions in reverse order.

## 4. Completeness And Error Budget

Repeat until the remainder is abelian, k=0, or its constructed ideal has
a<=k. There are at most the original n strict dimension decreases. Each
nonabelian terminal remainder satisfies

    m <= k(k+1)/2,        c_star <= 2k-1,

with the current k no larger than its initial value. It also retains
c_star<p; the loose bound 2k-1 is NOT substituted for its actual class
when deciding whether Lazard arithmetic is legal.

In an ideal abelian Fourier sampler, T independent samples are uniform
in K-perp. If r=dim(K-perp), failure to span has probability at most

    p^(r-T) <= 2^(a-T).

Thus T=a+ceil(log2(2n/epsilon)) per call is sufficient for a conservative
union budget. Approximate preparation/Fourier transforms require a
separate total error budget across all calls, including terminal samples.
Use a predetermined cap rather than condition on eventual success.

Do not substitute a subset of verified hidden elements for K. In a
filiform algebra, h=span(e_0,e_2,...,e_(n-1)) has codimension one. Under a
loose promise k=2, the proper subspace

    B=span(e_2,...,e_(n-2)) < h intersect A

passes membership and the bound dim B>=a-k. Nevertheless e_0 does NOT
normalize B, so restricting to N_L(B) loses a genuine hidden direction.
The implementation deliberately exposes this counterexample. Its public
checks cannot verify an unknown-source completeness promise.

For exact Fourier samples, the inferred orthogonal complement K_hat
contains K. Testing every basis vector for membership would then certify
equality when all pass. For noisy/incorrect samples the containment premise
can fail: membership checks alone are not an unconditional certificate.

## 5. Conditional Parameter Cost

Public linear algebra and the existing uniform BCH ODE construction cost
poly(n,c,log p), hence poly(n,log p), since c<=n for nilpotent L.
There are at most n abelian HSP calls with O(n+log(n/epsilon)) samples each.

For the terminal proposed scalar-line Rees solver, let r_d=dim gamma_d of
the terminal algebra. The fresh-source multiplier per terminal sample is

    P = product_(d=2..c_star) (d+1)^r_d
      <= (2k)^((2k-2)*k*(k+1)/2),       k>=2.

Thus P=2^O(k^3 log(k+2)). The initial Rees lift costs another c_star
original queries per leaf. This uses independent fresh source trees; no
leaf reuse or conditioning on favorable labels is licensed.

The scalar equation solver is uniform polynomial in d and log p, as
recorded in Fact 2 of [Ivanyos--Santha](https://arxiv.org/html/1503.09016).
This avoids silently treating a fixed-degree polynomial exponent as
uniform in k. Combining with the existing Rees proof, IF independently
validated, gives the candidate bound

    2^O(k^3 log(k+2)) * poly(n,log p,label width,log(1/epsilon)).

This is a conditional resource statement, not an implemented complexity
benchmark. The arithmetic tests do not run a quantum receiver or the
published scalar solver. For k<=2, m<=3 and nilpotence imply class<=2, so
the [published nil-2 HSP algorithm](https://arxiv.org/abs/0707.1260) can
replace the unverified Rees terminal step. For k=3, a class-three
five-dimensional remainder is possible; abelian/nil-2 termination must
not be assumed for all k.

## Classical Baselines And Reasons This May Not Matter

1. A classical membership sample hits H with probability at least p^(-k).
   Uniform accepted log-coordinates span h after O(n+log(1/epsilon)) hits.
   A capped rejection algorithm costs roughly p^k times that sample budget.
2. Birthday collisions improve this: independent batches of O(p^(k/2))
   uniform group elements yield a repeated f-label with constant probability.
   Choosing a pair by labels alone gives a uniform element x^{-1}y of H.
   Independent successful batches give independent hidden elements. Logs
   and span reconstruction then give a classical p^(k/2)*poly(n,log p)
   baseline, with failure caps and storage charged. This is an upper bound,
   not an optimal classical lower bound.
3. Fixed k and polynomial-size p therefore do NOT imply a superpolynomial
   separation. At fixed k, that possibility requires superpolynomial p
   relative to the non-field input size. For growing k, compare the actual
   exponents: k^3*log(k+2)=O(log n) still allows a polynomial quantum
   resource bound, while p^(k/2) can be superpolynomial for polynomial-size
   p. This is only a gap between upper bounds, not a classical lower bound.
   Growing ambient class, a nontrivial hidden subgroup and survival of
   input-specific classical attacks remain necessary for a new impact case.
4. Numeric low-degree labels, known linear actions, or a supplied hidden
   intersection can collapse the task classically. None is a hard source.
5. This may be known under a different formulation. Targeted literature
   searches did not establish novelty. The reduction builds on standard
   abelian HSP, normalizers and abelian-ideal bounds.
6. No natural-problem reduction has been established. Filiform examples
   verify the mechanism; they are NOT new benchmark problems or evidence
   of research-level quantum advantage.
7. If the proposed Rees core is wrong, the general terminal-solver claim
   fails. The public reduction and k<=2 corollary have a separate scope.

## A Conditional Application Extension, Not A Hard Family

The existing SUCCINCT_POLYNOMIAL_STABILIZER_AUDIT.md provides an actual
public-input problem, not an arbitrary relabeled oracle: compute the
formal-polynomial stabilizer of a public arithmetic circuit under a
supplied matrix p-group. Its fixed-class restriction can be replaced by
the codimension promise here, with the following explicit conditions.

Input: a size-s division-free circuit C over F_p in D variables, generators
of a promised p-subgroup Gamma<=GL(D,p), p>max(D,4), and

    [Gamma : Stab_Gamma(C)] <= p^k.

There is no supplied hidden stabilizer or invariant-generating advice.
The task remains a STABILIZER, not a transporter between two polynomials.

Every element of Gamma is unipotent. Matrix log/exp truncate before D;
p>D makes their denominators invertible. Close the F_p-span of the
generator logarithms under commutators. Lazard correspondence identifies
this explicitly computed matrix Lie algebra with log(Gamma). Its dimension
is at most D(D-1)/2 and its class is below D, but need not be constant.
This uses explicit matrix coordinates; it is not an opaque black-box
group-conversion claim. The index promise gives exactly the required
hidden Lie codimension bound.

Reuse, without weakening, the prior note's globally fixed extension-field
fingerprint f_z(g)=C(g^{-1}z). For a syntactic total-degree bound Delta,
choose q>=max(1,Delta)*p^(2D^2)/delta. A single random z separates the
entire polynomial orbit except with probability at most delta. Field
construction, original circuit evaluation, matrix arithmetic and reversible
cleanup are all polynomial in s,D,log p,log(1/delta). In particular,
log Delta=O(s); neither monomial expansion nor degree-many evaluations
are being granted for free. The same z must be retained across queries.

Consequently the proposed bounded-codimension algorithm gives the
CONDITIONAL bound

    2^O(k^3 log(k+2)) * poly(s,D,log p,log(1/epsilon))

for this promise problem. The public input bridge is specified; the general
Rees terminal proof remains unreviewed and the quantum receiver unexecuted.

This is not yet a useful separation. Existing derivative, mixed-Frobenius,
Moore-gradient, factorization and learned orbit-module filters must all be
retained. Large degree is insufficient. The orbit module has dimension
at most [Gamma:H]<=p^k, which need not be polynomial in log p even for
fixed k; this upper bound neither proves it is large nor establishes
classical hardness. For k=1, h is a codimension-one subalgebra of a
nilpotent algebra, hence an ideal containing [L,L]. Ordinary abelian HSP
on L/[L,L] already suffices. That subcase needs no new Rees mechanism.

No independently motivated family is known here to require this new
parameter regime and survive the existing semantic classical attacks.
The source search therefore yields a precise extension of an existing
conditional application, NOT a new admitted research candidate. Do not
manufacture invariant circuits from a secret H and call them hard without
auditing how their public construction reveals H.

## Implementation And Decisive Controls

`theorems/bounded_codimension_reduction.py` supplies validated public
structure tables, maximal abelian ideals with triangular flags, centralizers,
normalizers, quotient structure tables, projections, sections and pullbacks.
`reduce_at_known_intersection` has an explicit exact-intersection precondition.
It is NOT exposed as an end-to-end HSP solver.

`tests/test_bounded_codimension_reduction.py` covers growing filiform class
up to 23, UT4/UT5, changed coordinates, recursive coordinate-subalgebra
controls, noncentral K, nonhomomorphic sections, incomplete-intersection
failure, nonunique ideals, a class-three terminal remainder, malformed
structure tables and invalid characteristic/coordinate inputs. Small fiber
enumeration is test-only ground truth and is charged as such.

Verification: 37 new tests; 125 selected tests PASS in 3.32s, including
the existing uniform BCH, polynomial fingerprint and orbit-module suites.
New Python syntax checks and scoped whitespace checks PASS. Live public
reductions at (n,p)=(8,17),(17,19),(24,101) have classes 7,16,23, ideal
dimension n-1 and quotient dimension 1 with the supplied exact fixture
intersections. The separate incomplete-intersection run discards e_0 as
predicted. No quantum execution, full-repository validation or CLI workflow
was run; this is the theory/decisive-control pass, not integration work.

Next useful work: independent proof/novelty review; then identify an actual
growing-class source in a favorable field/codimension regime, compare
its semantic classical attacks, and reject it if the input already reveals
the requisite linear constraints. Do not create another synthetic oracle
campaign or promote finite reductions into a new algorithm discovery.
