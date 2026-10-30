# Adversarial Review: Full-Grade Rees Source Consumption

Date: 2026-10-27.

## Verdict And Findings

**The scoped obstruction survives this review. No adaptive pooling or unused-target recycling counterexample was found within the stated architecture.** The argument proves that a free perfect diagonal-system solver cannot give a uniform polynomial-resource, constant-success implementation of this prescribed descent on the supplied growing-class family. It does not prove an unrestricted HSP lower bound.

Independent reasoning was completed before reading the parent's [RESULT.md](/Users/jaspersands/Developer/qsearch-research-work/rees-source-tree-2026-10-27/RESULT.md). That statement already includes the important repairs: the small-pool case, full-record source coupling, disjoint consumption, and separate native budget and label cap. I found no fatal mathematical error in its main theorem under that contract.

Two qualifications should remain explicit:

1. **The factorial count is conditional on the generic-label event.** The polynomial-budget success bound is an unconditional probability statement. These must not be shortened to an unconditional factorial expected-cost lower bound; the stated estimates do not establish that stronger assertion.
2. **The optional subdivision remark needs its own probabilistic premise.** Its product inequality is correct. Applying it to another schedule requires exact fresh-source reset at every block and a union bound over those blocks, not merely the good event for the original full-grade streams. This is a clarification to [RESULT.md:134](/Users/jaspersands/Developer/qsearch-research-work/rees-source-tree-2026-10-27/RESULT.md:134), not a defect in the full-grade theorem.

The reported 38 controls and the corrected numerical rows are not used as theorem evidence. This review does not audit their implementation or certify the entire Rees reduction.

## 1. The Precise Object Being Lower-Bounded

Fix the unknown hidden subgroup throughout the experiment. Each physical source has an identity, a stage, and an ancestry. The permitted descent has these properties:

- Every top source is obtained through the prescribed Rees lift, costing c original copies, or c ordinary oracle calls in the alternative access model.
- At stage j, only the specified central grade Z_j is removed. A source is measured on that whole grade once; reading its saved label again does not create another source or another random draw.
- A merge produces one next-stage source. Its nonempty active support consists of distinct, currently available targets. All those targets are consumed. Inactive targets may remain available.
- Conditional on the permitted classical transcript, a new output is the exact next coset density and is independent of disjoint outstanding targets. Top sources satisfy the corresponding joint fresh-source contract.
- The policy may adaptively schedule measurements and merges, choose subsets and scales, retry classical computations, discard sources, and stop early. It may not acquire lower-stage sources independently, reuse consumed quantum targets, or use an alternative output channel.

Let B bound charged original resources and let N separately bound the number of distinct labels inspected at each stage over the **entire run**, including restarts. For the intended polynomial-operation consequence, both are polynomially bounded. An expected label cap or a cap on the number of retained labels is not a substitute for this deterministic acquisition cap.

The theorem concerns the event of producing a terminal source by this architecture. A direct classical answer, learning h by another quantum measurement, or learning h and then preparing a terminal state directly is not such an event. Likewise, the factor c is the cost of the specified lift, not an optimality theorem for every possible lift.

## 2. Algebra And The Label Law

The advertised Lie algebra is V semidirect F_p x, where V has basis y_0,...,y_(c-1), is abelian, and ad_x is one nilpotent Jordan block. This verifies Jacobi directly. For 2 <= j <= c,

    gamma_j(L) = span(y_(j-1),...,y_(c-1)),
    dim gamma_j(L) = c+1-j,
    gamma_c(L) != 0,   gamma_(c+1)(L) = 0.

Thus c is the actual class, not merely a chosen class bound. The vector

    v = x + sum_(i=0..c-1) a_i y_i

has nonzero x coefficient. Consequently h = span(v) meets every gamma_j for j >= 2 trivially, for every choice of the a_i. It is a Lie subalgebra because it is a line. The positive Rees hidden lift is exactly t*h.

Write A_<=j for the Rees algebra after deleting grades above j, G_j for its BCH group, and H_j for the image of the lifted hidden subgroup. The chosen subgroup Z_j = exp(t^j gamma_j(L)) is central, with rank

    r_j = c+1-j,

and H_j intersects Z_j trivially. Here Z_j means the selected central grade, not necessarily the entire center of G_j.

For rho_j = |G_j|^(-1) sum_(h in H_j) R_h, central Fourier measurement gives

    Pr(lambda = ell) = 1/|Z_j| = p^(-r_j)

for every ell in F_p^(r_j). This follows by character orthogonality: the only central element whose right action has nonzero trace against rho_j is the identity. It does not depend on a.

This matches the exact branch law and all-record contraction in [REES_HSP_REDUCTION.md:134](/Users/jaspersands/Developer/qsearch-research-work/rees-independent-review-2026-10-23/source/REES_HSP_REDUCTION.md:134). That contraction returns rho_(j-1) for every positive-probability complete label tuple and every valid witness, not just after averaging over labels. The prescribed copy-lift cost is separately stated in [REES_COPY_ONLY_OUTER_REDUCTION.md:193](</Users/jaspersands/Desktop/quantum algorithm search/research/REES_COPY_ONLY_OUTER_REDUCTION.md:193>); the ordinary-query version is in [REES_HSP_REDUCTION.md:91](/Users/jaspersands/Developer/qsearch-research-work/rees-independent-review-2026-10-23/source/REES_HSP_REDUCTION.md:91).

## 3. Why Adaptive Acquisition Can Be Coupled

The necessary invariant is conditional and joint. Given a complete permitted transcript T, the outstanding quantum bank factors into its live source registers. An unmeasured stage-j register has state rho_j. An already measured register has its appropriate conditional sector state rho_(j,lambda). Its saved label is part of T. Classical correlations in the choice of live identities are harmless after conditioning on T.

This invariant is preserved as follows:

1. A fresh top source is independent of the outstanding bank.
2. Measuring a previously unmeasured register changes only that factor. Its new label is uniform conditional on T, including previous labels from other stages.
3. Subset selection and solver randomness are classical. On fixing their records, selection does not entangle the chosen registers with the unchosen registers.
4. Applying a valid merge to the chosen product factors, then tracing the active targets, returns the fixed density rho_(j-1). The untouched factors remain a tensor factor. This is where the all-record identity is needed.
5. Discarding registers, keeping inactive targets, or performing additional classical retries preserves the invariant.

Therefore, when the policy requests its kth new label at stage j, that draw can be identified with the kth member of an upfront IID stream U_(j,1),...,U_(j,N). If the run requests fewer labels, pad with unused independent draws. Scheduling may depend on every previous revealed label. No assertion that the selected, retained, or eventually successful labels are IID is required.

In particular, do **not** condition the rank calculation on successful completion, on a chosen subset, or on a random final pool size. Those conditionings can bias labels. Bound the exceptional event on the entire padded stream first, then use a deterministic implication for every possible adaptive history. Independence between the stage exceptional events is unnecessary.

### What Would Invalidate This Step

Correct individual coset marginals do not suffice. Let rho_(j,lambda) denote the normalized central sector state, and consider the two-register bank

    Omega = p^(-r_j) sum_lambda
                rho_(j,lambda) tensor rho_(j,-lambda).

Each marginal is exactly rho_j, since averaging the sectors recovers rho_j. Nevertheless the two labels are always opposite. The scales (1,1) give a valid cancellation for every degree j. For r_j >= 2 this is a support-two cancellation, with probability one, on a bank whose individual marginals look correct.

This is a counterexample to a **marginal-only** formulation, not to the stated fresh-source contract. It also explains why independence of an output from its own classical records, in isolation, would be insufficient: it must be independent of the outstanding quantum bank as well. The parent's contract explicitly supplies this stronger property.

Likewise, recording extra measurements on nominally discarded quantum targets could alter the conditional output state. Such records cannot be added while continuing to invoke the original trace-out identity without a new proof.

## 4. Exact Small-Dependence Bound

For k <= r, expose k independent uniform vectors in F_p^r successively. Conditional on the first i being independent, their span has p^i elements, so the next vector lies outside it with probability 1-p^(i-r). Hence

    d(p,r,k) = 1 - product_(i=0..k-1) (1-p^(i-r)),
    d(p,r,k) <= sum_(i=0..k-1) p^(i-r)
              = (p^k-1)/(p^r*(p-1)).

In particular d(p,r,r) < 1/(p-1).

If N >= r, any dependent subset of at most r distinct indices can be extended to a dependent r-subset. Union over those r-subsets, without assuming that different subsets are independent:

    Pr(E_r) <= min(1, binom(N,r)*d(p,r,r))
             <= min(1, binom(N,r)/(p-1)).

If 0 < N < r, the event that some subset is dependent is exactly the event that the entire N-tuple is dependent. Its probability is d(p,r,N). For N=0 it is zero. Using binom(N,r)=0 in the large-pool expression when N<r would be wrong; the parent correctly does not do that.

A compact bound covering every case is obtained by setting m=min(N,r):

    beta(p,r,N) = min(1, binom(N,m)*d(p,r,m)),

with d(p,r,0)=0 and the usual empty-product convention. The parent's simpler piecewise upper bound is equally sufficient.

There is no further union over scale choices or solver invocations. Every nonzero witness has a nonempty active support S and satisfies

    sum_(i in S) s_i^j * lambda_i = 0,
    s_i^j != 0 for every i in S.

This already exhibits an ordinary linear dependence. On E_r's complement, |S| >= r+1, regardless of how the solver found it. Restricting coefficients to jth powers can obstruct additional solutions, but cannot create a solution among independent vectors. Even unrestricted nonzero coefficients would obey this support lower bound.

## 5. Adaptive Recycling Attacks

**Inspect a large pool and choose the best subset.** Covered: E_r is existential over every small subset of the whole inspected stream, not over one predetermined batch. Pooling changes which subset is chosen, not whether the global exceptional event is necessary.

**Measure once and repeatedly reuse an unused label.** Allowed. The corresponding unacted-on register remains in its measured sector. Reconsidering its label adds neither a new IID draw nor another quantum target. If it eventually participates actively, it is consumed then. Until that point it can occur in arbitrarily many unsuccessful classical candidate lists without affecting the proof.

**Keep zero-scale targets after a successful merge.** Also allowed. Conditional on all labels and the chosen witness, these registers were not acted on and factor from the fixed output. Only the active support is charged at that merge. The lower bound never charges a discarded zero-scale target as a necessary child. Thus it survives this improvement over the older consume-every-batch convention.

**Use a saved consumed label in another witness.** The classical equation may still be solvable, but the required physical target is absent. A correct implementation must verify that every active index names a distinct live source. Copying a classical label does not duplicate its source. The tensor-product contraction is not justified by applying several nominal target actions to the same register.

**Retain only favorable labels, restart, or stop as soon as a short relation appears.** Covered by the padded-stream event, provided N counts all inspected sources across all attempts. Resetting the label counter at a restart, or counting only the retained pool, would change the budget and invalidate the bound. Repetition can amplify a rare event only by paying for the additional inspected sources.

**Premultiply all labels by a common invertible matrix.** This preserves dependence. Individually transforming targets or their labels through new, source-dependent automorphisms is a different instrument and is not licensed by the scalar-witness equation. Merely changing the classical description cannot change the physical character.

**Premeasure future grades or pass a conditioned remainder to the next stage.** That need not be an exact fresh next-stage coset independent of the transcript. It falls outside the reset contract and needs a new analysis. The present proof should not be advertised as covering such a sieve.

**Produce several exact-looking marginals from one consumed bank.** Excluded by the disjoint-output contract. Correct marginals alone would not make them independent sources. No claim that this exclusion follows from a general no-cloning argument is needed or made.

These attacks reveal no loss from the recycling explicitly permitted by the parent. Each apparent saving either remains inside the already-counted pool or changes the quantum source interface.

## 6. Source Ancestry And The Quantitative Theorem

Let E_j be the small-dependence event for the padded stage-j stream, and let E be their union. On E's complement every merge at stage j consumes at least r_j+1 distinct active sources.

Induct backward through the ancestry of a terminal source. A top-stage source has one lifted leaf. If each stage-j source needs at least w_j distinct leaves, a stage-(j-1) output requires at least (r_j+1)*w_j leaves: its active children's ancestries are disjoint. This is a tree argument, not a count of attempted batches. Discarded work and unused registers can only add cost.

Consequently

    w_c = 1,
    w_1 >= product_(j=2..c)(r_j+1) = 2*3*...*c = c!.

The prescribed lift then costs at least c*c! original resources. For a run with B<c*c! and per-stage label cap N,

    {terminal source produced} is contained in E,

    Pr(terminal source produced)
        <= min(1, sum_(j=2..c) beta(p,r_j,N)).

The parent's piecewise beta replacement gives the claimed bound as well. This probability is over the whole unconditioned run, not conditional on eventual success. Early stopping and any number of free classical attempts are already included.

For supplied primes 2^(c^2)<p<2^(c^2+1), log_2 p=Theta(c^2). The original Lie tensor has at most O(c^3) field entries, hence O(c^5) bits in a dense encoding; the Rees dimension is c+1+c(c-1)/2=O(c^2). This is a polynomial-size explicit public input in the oracle-access model, not an explicitly listed hiding-function table. Prime generation is not being claimed as part of the result.

For N>=1 the exceptional probability is at most

    min(1, (c-1)*max(1,N^(c-1))/(p-1)).

If N is bounded by any fixed polynomial in c and log p, its logarithm is O(log c), giving

    Pr(terminal source produced) <= 2^(-c^2 + O(c log c))

whenever B<c*c!. Every fixed polynomial native budget satisfies that strict inequality for sufficiently large c. This proves the proposed obstruction to a uniform polynomial-resource, bounded-error implementation. It does not say that every family with growing c is difficult; for example, the actual input can grow so quickly that c! is polynomial in its length.

The same reasoning rules out expected-polynomial **total charged operations** with constant success in this model. If expected cost were M=poly(c,log p) and success at least 2/3, truncating at 6M operations loses at most 1/6 success by Markov's inequality. The truncated run would still succeed with probability at least 1/2 and would have polynomial deterministic caps, contradicting the displayed bound for large c.

This does not establish E[cost] >= c*c!, nor a high-probability factorial bound for runs allowed to inspect factorially many labels. Substituting N of order c! can make the union bound vacuous at the chosen p scale. The valid statements are the conditional factorial ancestry count and the negligible polynomial-budget success probability.

## 7. Optional Fixed Subdivisions

There is a valid extension, but its assumptions should be stated rather than inferred from the full-grade theorem. Fix in advance a public flag subdividing each grade j into central factors of positive dimensions b_(j,1),...,b_(j,q_j), whose sum is r_j. Require the same exact fresh-source reset and disjoint active consumption at every substep, with at most N newly inspected labels per substep.

The hidden line remains disjoint from every such factor. The preceding argument applies separately to its uniform b-dimensional labels. Outside the union of the **block-specific** exceptional events, the necessary source multiplier is

    product_j product_l (b_(j,l)+1)
        >= product_j (1+sum_l b_(j,l))
        = c!.

The inequality follows repeatedly from (a+1)(b+1)>=a+b+1. There are at most sum_j r_j=c(c-1)/2 blocks, so polynomial label caps give the same exceptional-probability scale 2^(-c^2+O(c log c)).

This does not follow by projecting an already selected full-grade pool and treating its projections as fresh uniform inputs. Nor does it cover choosing a quotient from a just-observed character's kernel. Such choices can force zero restricted labels; any resulting conditioned quantum remainder requires separate analysis. The original full-grade statement can simply omit this extension without weakening its main conclusion.

## 8. Direct Answers, Prior Art, And Research Scope

Central labels alone do not identify the hidden line in this family: their acquisition law is the same for every a, and classical choices and solver outputs computed only from those labels and independent coins have the same property. Under a uniform prior on the p^c possible coefficient vectors, guessing the exact line from only this transcript succeeds with probability at most p^(-c). This observation is not a bound on algorithms retaining other oracle information or making other quantum measurements.

In particular, success at recovering h need not pass through a terminal source. The theorem cannot dismiss an algorithm that learns h earlier, changes the cover, uses coherent composition, reuses quantum targets through a different instrument, or operates on a different state representation. Those are precisely the kinds of architectural changes that this result leaves open. Approximate instruments also need a complete-protocol error analysis; correctness of isolated marginals is insufficient.

The limited primary-source check supports conservative attribution:

- Central subgroup-state conversion and multiplication of source costs across a central series already appear in Imran--Ivanyos, Lemma 2 and Proposition 2 of [Zero sum subsequences and hidden subgroups](https://arxiv.org/html/2304.08376). The present lower bound must not claim those mechanisms as new.
- Diagonal cancellation as a linear relation with power-restricted coefficients, together with fixed-degree algorithms and constant-class semidirect-product applications, appears in Ivanyos--Santha, Definition 1 and Section 4 of [Solving systems of diagonal polynomial equations over finite fields](https://arxiv.org/html/1503.09016).
- Automorphism-based actions and linear/quadratic cancellation in nilpotency class two predate this proposal; see Ivanyos--Sanselme--Santha, [An efficient quantum algorithm for the hidden subgroup problem in nil-2 groups](https://arxiv.org/abs/0707.1260).
- An unrestricted oracle-query lower-bound interpretation would be untenable: Ettinger--Hoyer--Knill give polynomial quantum query complexity for general finite-group HSP, without polynomial total time, in [The quantum query complexity of the hidden subgroup problem is polynomial](https://arxiv.org/abs/quant-ph/0401083).

The review's rank calculation, deferred-revelation argument, and ancestry induction are elementary. Their application gives a useful obstruction to improving this particular receiver solely by improving the SDE solver. It is not a novelty certificate, a new hard application, or evidence for a quantum/classical separation. The [derived-rank note:41](</Users/jaspersands/Desktop/quantum algorithm search/research/DERIVED_RANK_REES_EXTENSION.md:41>) changes to public scalar-line descent and supplies an upper bound; neither that bound nor the fixed-class proposal is contradicted.

## Final Recommendation

Retain the parent's main full-grade theorem with its current architecture contract. State the joint conditional-source invariant prominently, retain physical source identities when discussing recycling, and keep the factorial count explicitly conditional. Either qualify the subdivision sentence by the blockwise reset and exceptional-event argument above or omit it. No additional finite controls are needed to resolve the adaptive-recycling issue addressed here.

Only this new review file was written. No repository, Git, UI, implementation, or parent artifact was changed.
