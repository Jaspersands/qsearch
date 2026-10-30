# High-Rank Gram Decision

30 October 2026. Follow-up to the constructive scalar receiver. The previous
goal pass made progress: it supplied a complete ideal channel argument and
a tested controller. This pass revises its comparison and tests whether its
mechanism supplies a credible high-rank algorithm. No speedup is admitted.

## Corrected Baseline

The previous 18/36 sequential comparator was unnecessarily weak.
[Ivanyos--Sanselme--Santha, Section 5 Claim 1, manuscript page 13](https://www.irif.fr/~santha/Papers/iss12.pdf#page=13)
gives a sufficient diagonal-quadratic arity

    B2(s) = (s+1)(s+2)/2.

At s=2 this is six, not nine. Scalar cubic solving uses two inputs when
p=2 mod 3 and three otherwise. The three-input construction uses an
existing curve solver, with zero and repeated-class cases handled separately.
Therefore a stronger sufficient comparator is 12/18. The Gram bank of
14/16 is worse in the first regime and saves two inputs against this
particular comparator in the second. No optimality or uniform performance
improvement follows. The corrected report explicitly records these limits.

The published quadratic claim includes arbitrary and degenerate coefficients;
it is not a generic-input heuristic. Its algorithm uses linear algebra,
quadratic nonresidue selection and scalar finite-field solving. The printed
completion constant on manuscript page 15 omits squares on the retained
variables; the quadratic equation requires those squares. This typo does
not change the recursive construction. No integrated sequential quantum
implementation has been added or claimed.

## Candidate And Input Model

For an actual class-three Rees group, let N=A2+A3 be the abelian normal
subgroup being erased. Suppose the measured top characters are public
vectors ell_i in F_p^r. Seek a public scale frame W of dimension d on M
independent mixed lifted coset states, with

    sum_i ell_i*u_i*v_i*w_i = 0 for all u,v,w in W.

Measuring the restricted lower-character Gram forms preserves the required
scaled-action coherence, as in the scalar proof. The candidate then needs
to find a nonzero common zero of the s measured quadratic forms on W.
It may never expose individual noncentral characters, consume hidden-subgroup
advice, assume uniform labels without proof, or postselect rare sectors for
free. The target is a genuinely smaller complete source/time bound than
sequential descent, not just a correct finite frame.

## The Dense Quadratic Step Is Payable, But Not Free

There is a simple constructive fallback for arbitrary symmetric matrices
Q1,...,Qs on d variables, obtained by reducing to the published diagonal
solver above. This reduction is an elementary deduction, not a claim that
the paper states this exact general-form threshold.

Greedily choose nonzero vectors v_j satisfying

    v_i^T Q_l v_j = 0 for all i<j and all l.

At step j these are at most s(j-1) linear constraints. If v_j is a common
zero, return it immediately. Otherwise, the selected vectors are linearly
independent: pairing any proposed dependence against v_i with a form for
which v_i^T Q_l v_i is nonzero forces its i-th coefficient to vanish.
Thus, when d>s(B2(s)-1), we either return early or obtain B2(s) vectors
on which all forms are simultaneously diagonal. Solve that diagonal system
and lift its nonzero witness through the independent vectors.

A sufficient dimension is therefore

    d >= s^2*(s+3)/2 + 1.

All preprocessing is finite-field linear algebra, for example at most
O(B2(s)*d^3) field operations with straightforward elimination. The imported
solver is polynomial in s and log p with its paid randomness assumptions.
This supplies a real search route with surplus variables. By contrast,
d>2s guarantees existence by Chevalley--Warning but does not supply this
algorithm at that threshold. No claim about a best possible threshold or
hardness of guaranteed homogeneous search is made.

For the direct version with all s=dim(A2) lower labels kept coherent,
building this much W by disjoint cubic blocks makes the obvious fallback
WORSE than sequential descent: it multiplies the same cubic block cost by
Theta(s^3), rather than B2(s)=Theta(s^2). A better overlapping-frame
construction would have to pay for its own coupled quadratic solver and
still beat the matched TOTAL bound. Moving the difficulty between the two
steps is not progress toward an algorithmic separation.
Disjoint blocks already diagonalize the forms, so a sensible implementation
uses B2(s) directly and recovers the sequential schedule. The larger generic
fallback is an available search bound, not a necessary cost or lower bound.
If additional preprocessing removes central forms or exploits restricted
source support, charge it and compare the complete schedules again; this
simple comparison does not rule out such an improvement.

## Two Decisive Structural Checks

The [Gram image analysis](GRAM_FRAME_SEARCH_BOUNDARY.md) shows that common
factorization Q_l=W diag(alpha_l) W^T alone is not a tractability promise.
Arbitrary tuples occur on positive-probability sectors of genuine class-three
Rees sources, with nonzero central records. The sectors may be very rare;
this is not an average-case hardness claim. A three-dimensional frame can
already have two measured forms with no common nonzero zero.

For a rank-d frame with columns v_i, the span of v_i v_i^T has dimension
at least d. Equality holds exactly when the frame has a disjoint-support
row basis. Thus a single coefficient-independent basis diagonalizes its
ENTIRE Gram image exactly in the block case. This does not prohibit a
basis chosen after a particular measured tuple, especially for one form.

The [fixed collision-frame audit](CUBIC_COLLISION_FRAME_OBSTRUCTION.md)
tests the most immediate proposed reuse of the current cubic solver.
A two-level three-class collision scaffold cannot universally yield a
two-dimensional totally singular contraction space with fixed internal
cell weights. A rank-four cell tensor makes this obstruction hold for that
bank's FIXED-CELL IMAGE too, not every direction in a padded bank.
Independent cubic witnesses need not have vanishing
mixed triples. This excludes that specific reuse mechanism, not overlapping
frames in general, changed internal weights, or other quantum instruments.

## Decision And Next Gate

Do not promote the high-rank Gram extension or continue scalar optimization.
The scalar channel remains a correct constructive example under its stated
ideal assumptions; the broad performance motivation has weakened.

A new continuation of this branch must supply one of:

- A public high-rank frame construction with complete cost that beats the
  sequential cubic-times-quadratic bound AFTER common-zero search.
- A proved restriction on the ACTUAL allowed Gram distribution that enables
  an efficient solver; a common rectangular factorization is insufficient.
- A different collective instrument with its full branchwise channel and
  source accounting, not a diagonal witness selector with assumed weights.

Otherwise pivot to a motivated native algorithmic problem. In particular,
do not substitute another source-count calculator, constant-factor solver
port, or finite oracle benchmark for the missing general mechanism. Existing
source/application audits must be consulted so that already dequantized
polynomial and tensor families are not resurrected by renaming them.

Harvey checked the primary quadratic source and scalar-cubic comparator.
Russell reviewed actual-source Gram realizability and the fixed-basis lemma.
Epicurus derived and checked the two-level collision obstruction. All reviews
are automated. Mathematical deductions, finite controls and implementation
status remain separate; no human peer review or formal proof is claimed.
