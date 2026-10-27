# Rees HSP: Specialist Review Brief

27 October 2026. AI-assisted research draft, not peer-reviewed. This is a
local assessment package, not a submission or an announcement. No recipient
has been selected and nothing has been sent. External contact requires the
user's explicit instruction.

## The Question To Decide

Does the proposed homogenization/state-conversion composition correctly
remove the bounded-prime restriction for fixed-class nilpotent HSP, and is
that consequence already covered by published work?

Start with [the corrected manuscript](rees_hsp_review.tex). Assess
correctness and prior-art subsumption separately. The project does not
claim that either has been settled by automated review, finite tests, or
the absence of a matching search result.

## Primary Claim

Fix c. Given an explicitly represented n-dimensional nilpotent Lie algebra
L/F_p of class at most c<p, with p odd, and a coherent ordinary fixed-width
oracle hiding an arbitrary subgroup H of the BCH group exp(L), recover a
basis of log(H) in bounded-error time polynomial in n, log p, oracle-label
width and log(1/epsilon), with constants/exponents depending on c.

Both n and p grow. H need not be normal, transverse, graded, or supplied
by generators. The input need not have a positive grading or an abelian
codimension-one ideal. Public field/group arithmetic and cleanup are paid.
The manuscript also gives a separately specified fresh-coset-copy input;
it does not obtain a hiding oracle by sampling those copies.

The general uniquely encoded fixed-class nilpotent-group corollary uses
additional published input/reduction algorithms. Review the explicit-Lie
claim first. The growing-class/small-derived-dimension and explicit
prime-power-ring extensions are secondary, not premises of that claim.

## The Proposed Additional Interface

Write gamma_r for the lower-central spaces and form

    A = direct_sum_(r=1..c) t^r gamma_r(L) inside L[t].

For c distinct nonzero s_i, the tuple evaluator

    f_hat(a) = (f(exp(E_s1(log a))), ..., f(exp(E_sc(log a))))

hides exactly direct_sum_r t^r(log(H) intersect gamma_r(L)), by invertible
Vandermonde interpolation in the VECTOR-SPACE quotient L/log(H).
Evaluation is a genuine Lie homomorphism because high brackets actually
vanish; it is not evaluation of an arbitrarily truncated polynomial ring.
The hidden lift is invariant under public degree dilations Delta_s.
Grade one is tL, NOT the associated-graded abelianization.

At a central grade d, measure characters lambda_i and find a nonzero scale
witness with sum_i s_i^d lambda_i=0. Controlled twisted right actions and
target discard yield the exact quotient coset state on EVERY successful
complete record, including zero characters and zero scales. The all-zero
witness is forbidden. This record-independent output permits recursion
using fresh disjoint inputs. The final additive quotient retains all of
log(H), recovered by ordinary abelian Fourier sampling.

The potential contribution is the public reduction/composition above.
Central Fourier conversion, diagonal solving, abelian HSP and basic
Lie/group constructions are not presented as new primitives.

## Resource Contract To Check

For r_d=dim gamma_d(L), use the published sufficient arity

    B_d(r_d) = [d^(d(d-1)/2)(r_d+1)^d]^ceil(log_2(d+1)).

Let P=product_(d=2..c) B_d(r_d), m=n+t, with
t=ceil(log_p(3/epsilon)). The explicit-Lie schedule uses c*m*P original
queries or original copies. All leaves, merge instruments and terminal
Fourier readouts enter the precision budget. The general polynomial-time
SDE algorithm is imported, not replaced by Chevalley-Warning existence,
a random-label assumption or exhaustive field search.

These bounds are polynomial only at fixed c and can be enormous. Neither
practical superiority nor a compiled quantum receiver is claimed. The
separate parameterized corollary first computes the ACTUAL class from the
lower-central series; see the correction below.

## Closest Published Dependencies And Comparators

| Work | Supplied result and comparison boundary |
| --- | --- |
| [Ivanyos--Sanselme--Santha, nil-2 HSP](https://arxiv.org/html/0707.1260v1) | Covers arbitrary H at class at most two. Its Section 3 reduces fixed-class nilpotent HSP to local exponent-p/order-at-most-p instances; that reduction does not itself supply a higher-class solver. Automorphism-twisted phase cancellation is already present. |
| [Ivanyos--Santha, diagonal systems](https://arxiv.org/html/1503.09016v2) | Supplies an algorithm at fixed equation degree with growing equation count and field size, plus hidden-polynomial-graph and specified semidirect-product applications. The proposed proof imports this solver; the oracle-to-homogeneous-cover interface is the additional step to scrutinize. |
| [Imran--Ivanyos, zero sums and hidden subgroups](https://arxiv.org/html/2304.08376v1) | Supplies central subgroup-state conversion and fixed-class algorithms with bounded prime divisors. Its Theorem 1 is exact with source/inverse access; the bounded-error forward-conversion branch must be distinguished. Its general bounded-prime runtime is not uniform polynomial in log p. |

The [bounded prior-art audit](review_evidence/2026-10-27-prior-art-scope.md)
also checks smooth-solvable, graph-state and recent special-group results.
It identifies an apparently additional scope relative to the particular
theorems examined, not a novelty certificate. A published theorem plus a
paid input-preserving reduction covering the whole contract would settle
the subsumption question even if the local proof is correct.

## Read And Attack In This Order

1. Manuscript Sections 1--2: the exact input, actual polynomial Lie cover,
   nonnormal subgroup interpolation and preservation of all original
   directions in grade one.
2. Central-character and quotient-conversion sections: signs/normalization,
   nontrivial H intersect Z, forbidden labels, zero scales, nonhomomorphic
   public sections and the identity on every complete successful record.
3. Full clocks and approximation: fresh-input recursion, fixed-degree SDE
   hypotheses, whole-instrument error, all consumed sources and final readout.
4. Only then the general black-box extension: paid public presentations or
   free-Lie pullback, local order-p promise, small-prime branch, normalizer
   recursion, full torsion preimages and adaptive error clocks.
5. Compare the full scope with prior work. Finally ask whether there is a
   meaningful natural-input application; correctness does not establish one.

A decisive correctness falsifier is one admissible algebra/subgroup and
positive-probability branch with a valid nonzero cancellation witness for
which the claimed quotient density is wrong. Another is a required imported
algorithm whose actual promise or runtime fails to match the invocation.
Finite successes alone cannot close either universal question.

## Review Evidence And The Applied Correction

The [2026-10-23 automated adversarial review](review_evidence/2026-10-23-correctness-review.md)
reconstructed the explicit-Lie argument and inspected the named outer
reductions. It found no fatal counterexample and one repairable resource
qualification, F1. It was performed by a separate AI reviewer, NOT a human
specialist, a theorem prover or a peer-review venue.

F1 matters for the variable-class parameterized corollary. A Heisenberg
algebra has actual class 2 and derived dimension 1 but also satisfies the
loose upper bound c=p-1. The assertion c<=dim[L,L]+1 and a c-evaluation
cost would then fail literally. The corrected text computes the actual
class by public linear algebra BEFORE choosing the cover, evaluation
points, BCH truncation or source budget. This was already corrected in the
isolated reviewed revision; it is now reconciled into the repository file.
The existing public compiler already used the actual lower-central profile.

Both reports are preserved byte-for-byte in review_evidence/. Their old
absolute workspace links identify historical snapshots; they are not
portable links and should not be mistaken for current manuscript line
numbers. The reports' primary literature URLs remain usable. The current
mathematical text matches the corrected isolated revision; only the author
status line and date differ. No reviewed conclusion has been upgraded to
human validation, formal verification or experimental quantum execution.

## What This Package Does Not Claim

There is no established lattice, graph-isomorphism, code-equivalence or
cryptanalytic application. The explicit-action audit already finds strong
classical/known-quantum competitors for several tempting applications.
General transporter problems do not follow from stabilizer recovery.
Unimplemented public algorithms are reproduction work, not automatically
new mathematical gaps; conversely passing their interface tests does not
prove those imported algorithms or the whole theorem.

The next useful external response is a concrete flaw, exact prior-art
subsumption, or a specialist reconstruction of the proposed contribution.
An additional small benchmark or a further nearby generalization is not a
substitute. See [the unsent outreach draft](REES_OUTREACH_DRAFT.md) and
[the local verification ledger](REES_REVIEW_VERIFICATION.md).
