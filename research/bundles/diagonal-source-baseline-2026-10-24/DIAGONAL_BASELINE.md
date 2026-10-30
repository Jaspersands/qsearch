# A Sample-Only Classical Gate For Low-Rank Diagonal Sources

2026-10-24. LOCAL REDUCTION, INDEPENDENT REVIEW PENDING. No new group
algorithm, general mixed-state dequantization, quantum execution or novelty
claim. This closes a classical-baseline gap, not a quantum-source gap.

## Question And Decision

The preceding mixed-conjugation source does not require a supplied density
matrix. It would therefore be insufficient to reject only applications
that expose a full matrix table. A diagonally encoded classical distribution
with polynomial support is already classically manageable from ordinary
samples, even without a minimum weight or separation between unequal weights.

For a supplied defining-characteristic affine matrix p-group, the complete
symmetry subgroup can be recovered in randomized polynomial time under the
SAME rank cap and global orbit-gap promises. The final set-stabilizer
algorithm is published prior art; we implement sampling/coarsening/encoding
and finite controls, not that general group backend.

This specifically rejects sparse classical-data distributions with these
actions as a motivation for the new Rees source. It does NOT reject unknown
non-diagonal quantum states, an unknown diagonalizing basis, arbitrary
succinct permutations, or general mixed-state symmetry learning.

## Native Contract And Costs

Let Omega=F_p^n, with p supplied prime and efficient exact arithmetic. Input
access is independent samples from one fixed unknown distribution P with
support size at most a supplied R. Equivalently, the original quantum input
is diagonal rho=sum_x P(x)|x><x|; computational-basis measurement yields the
same samples and requires no collective quantum operation. No support list,
probability evaluator, purification, chosen-label sampling, source inverse,
or full basis of size p^n is provided.

Supply faithful affine matrix generators for a p-group G acting on Omega.
The monomial quantum action may have any phases; they cancel under diagonal
conjugation. The target is exactly

    H={g in G : g.P=P}.

For every g outside H, promise TV(P,g.P)>=delta>0. Rank, diagonality, the
group promise and global separation are not verified by observing a few
samples. R and 1/delta must be polynomial for the efficiency claim. The
input and sample-label bit costs include n log p and the public generators.

Abstract group coordinates with an additional kernel require a paid
kernel/lifting interface. A black-box action is not a faithful matrix
presentation. These are not interchangeable access models.

## 1. Uniform Frequency Accuracy Without Learning Rare Weights

For failure eta in (0,1], set

    e = delta/[16 R(R+1)],
    N = ceil[ceil_log2(2R/eta)/(2 e^2)].

Draw exactly N samples. Write p_hat(x) for their frequencies, zero for
unseen labels. For each of the at most R true support points, Hoeffding
gives Pr[|p_hat(x)-P(x)|>e]<=2 exp(-2Ne^2). A union bound and
ceil_log2(z)>=ln(z) for z>=1 give simultaneous accuracy with probability
at least 1-eta. Zero-probability labels are never observed in the IID model.
The sample count is O(R^4 delta^-2 log(R/eta)); no inverse minimum weight
or inverse difference of probabilities occurs.

This is a promise-conditional statement. A noisy or non-IID source needs a
separate error budget. In particular, this is not a test that the original
unknown state is diagonal.

## 2. Deterministic Interval Chains Preserve Equal Weights

Rounding empirical frequencies independently to fixed bins is unsafe:
equal true weights can land on opposite sides of a boundary. Instead append
ONE dummy frequency zero, sort the observed frequencies, and join adjacent
entries when their difference is at most 2e. Take connected components.

Discard the component containing zero, including all implicitly unseen
labels. For every other component C, assign each of its observed labels

    A(x)=a_C=min_(z in C) p_hat(z)-e.

Set A=0 elsewhere. The retained a_C are positive and distinct. A is an
unnormalized diagonal operator, not a newly normalized distribution.

On the simultaneous accuracy event:

1. If P(x)=P(y)>0 and both appear, their estimates differ by at most 2e;
   the sorted chain therefore places them in the same component. If one
   is unseen then P(x)<=e, so the other's estimate is <=2e and it belongs
   to the discarded zero component. All equal true weights receive the
   same rounded value, including zero weights.
2. Retained values satisfy 0<a_C<=P(x). A component has at most R labels,
   each connecting step is at most 2e, and both endpoint estimation errors
   are bounded. The loss on a retained label is at most 2R e. An observed
   discarded label has P(x)<=(2R+1)e; an unseen label has P(x)<=e. Thus

       0<=A<=rho,  ||rho-A||_1 <=2R(R+1)e=delta/8.

3. Every exact symmetry of P permutes equal true weights, hence preserves
   A. Conversely, if g preserves A, then

       TV(P,g.P) <= ||rho-A||_1 <=delta/8<delta.

   The global promise forces g in H. Therefore Stab_G(A)=H EXACTLY.

The construction does not estimate tiny unequal weights accurately or
assert they are equal. The global promise is what prevents merging them
from changing the target subgroup. If that promise is false, the conclusion
can fail; the tests include that failure.

## 3. The Classical Group Stage Is Already Available

Give each nonzero component a color j. Replace its labels by vectors

    (x,1,e_j) in F_p^(n+1+k),  k<=R,

where e_j is one-hot. Lift an affine action x -> M_g x+b_g to

    diag( [[M_g,b_g],[0,1]], I_k ).

The finite SET of encoded vectors is preserved exactly when A is preserved.
This is not a pointwise stabilizer, an uncolored support, or the span of
the set. The lifted group remains a faithful p-group in characteristic p.

[Luks, Computing in Solvable Matrix Groups, Theorem 3.2(6), Section 6.4](https://ix.cs.uoregon.edu/~luks/solmatgrp.pdf)
supplies the set stabilizer
in time polynomial in dimension, log(field size), explicit set size and mu,
the largest group-order prime other than the field characteristic. Here
mu=1. Subgroups are returned by generators, not by enumerating G or Omega.
The publication announces that algorithm and omits some structural proofs;
we rely on its stated result rather than claiming to reprove or implement it.

This extends the repository's existing explicit-set baseline to UNKNOWN
weights and UNKNOWN support supplied only by samples. The sampling step
and elementary rounding argument are local deductions using standard
concentration. Novelty has not been established.

## 4. Adversarial Scope

- Equal probabilities can acquire different empirical counts. Keeping
  raw counts as colors can erase genuine symmetries. Interval chains fix
  this, at the cost of the explicitly paid R^4 sample bound.
- Ignoring colors enlarges the subgroup; fixing each point separately
  shrinks it. A span stabilizer also solves a different problem.
- The zero component is necessary for unseen low-probability labels.
  The algorithm cannot output the exact support from polynomial samples
  when some probabilities are arbitrarily small, and does not try to.
- Without the global delta promise, unequal probabilities in one chain
  can yield a spurious symmetry. Neither low rank nor a good histogram
  alone certifies the answer.
- Low matrix rank is not sparse computational support for non-diagonal
  states. For example a pure coherent state can populate exponentially
  many basis labels. This reduction must not be applied to that input.
- For arbitrary monomial permutations lacking the stated matrix-group
  access, obtaining the small weighted set does not by itself solve its
  stabilizer. Cross-characteristic large primes do not have mu=1 either.
- Taking IID classical samples is allowed under this diagonal-source
  contract. A supplied unknown quantum basis, or a costly quantum basis
  conversion, cannot be silently given to the classical comparator.

## Research Decision

Keep the preceding non-diagonal mixed-source construction under review.
Any proposed classical-distribution application must now survive this
sample-only baseline, not merely avoid exposing its density table. The
nonnormal UT3 control is an easy regression for correctness, not a new
hiding-oracle candidate or a claimed hard instance.

This pass also rechecked the HDQI source/gap dependencies. A contemplated
full-star experiment was dropped BEFORE implementation because the existing
total-mass theorem already covers it. No new HDQI gap theorem or natural
hard application emerged from that triage. The actual open regime remains
large connected intermediate-degree inputs, outside the signed-word and
mass-based preparation/comparison guarantees.
