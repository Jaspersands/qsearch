# Bounded Prior-Art Review: Fixed-Class Lazard HSP

Review and web retrieval date: **2026-10-27 (Australia/Sydney)**. Theorem numbers below refer to the linked versions. This is a scope comparison, not a correctness review or novelty certificate.

## Decision

**The full proposed theorem is not a consequence established by the specific published statements and reductions examined here. It is a precisely scoped, apparently uncovered extension relative to those results, not a novelty finding.** Substantial special cases and almost all of the receiver ingredients are already covered. The strongest general match is Imran--Ivanyos's central-state descent; the strongest growing-prime overlaps are the complete nil-2 algorithm and fixed-class elementary-abelian-by-cyclic algorithms.

This assessment rests on explicit mismatches in theorem hypotheses and resource bounds, not on an unsuccessful keyword search. It does not establish that no other publication or short combination covers the claim.

## Target Contract

For each fixed class bound `c`, the input supplies a prime `p>c`, structure constants for an `n`-dimensional nilpotent Lie algebra `L/F_p`, and a coherent ordinary function oracle on the BCH/Lazard group `G=exp(L)` hiding an **arbitrary** subgroup `H`. Recover a basis of `log(H)` with failure at most `epsilon`, in `poly_c(input bits, log(1/epsilon))` total time and queries. Both `n` and `p` may grow; arithmetic must be polynomial in **log p**, not p. Oracle-label width is charged. No normality, supplied grading, abelian codimension-one ideal, or bounded rank is promised. This is not a theorem for growing `c` or an assertion about arbitrary copy-only inputs.

## Closest General Match

**Imran--Ivanyos, _Zero sum subsequences and hidden subgroups_, arXiv:2304.08376v1; published QIP 23:14 (2024).** Theorem 1 requires constant class, unique black-box encodings, and that "the prime factors of |G| are also bounded by a constant". Its exact algorithm accesses a subgroup-state preparation oracle **and its inverse**. An ordinary reversible hiding oracle supplies this access. Lemma 2 converts subgroup states to the quotient by a central elementary abelian subgroup for arbitrary `H`; Propositions 2 and 3 give exact and bounded-error iterative variants conditional on a zero-sum solver. Thus arbitrary-H central conversion and iteration are prior art. [Primary text](https://arxiv.org/html/2304.08376v1); [published version](https://link.springer.com/article/10.1007/s11128-023-04228-2).

Theorem 2 supplies sequence length `S(p,m)=p^{O(p log^2 p)} m^{O(p log p)}`. The following remark **already considers the Ivanyos--Santha SDE algorithm**, using degree `d=p-1`; this does not yield polynomial dependence on `log p`. Replacing exact computation by bounded error does not remove that parameter dependence. The missing general growing-prime conclusion is therefore not supplied by simply citing these results together.

## Growing-Prime Algorithms Already Available

**Ivanyos--Sanselme--Santha, nil-2 HSP, arXiv:0707.1260v1; Algorithmica 62, 480--498 (2012).** Theorem 1 covers every hidden subgroup of every class-at-most-two group: "Then there is an efficient quantum procedure which finds H." This is a bounded-error algorithm without a bounded-prime restriction. Section 2.3 explicitly measures time polynomially in the ranks and `log p`. The input is an ordinary hiding oracle, with efficient group arithmetic; Section 3 uses refined polycyclic presentations and discusses their construction for uniquely encoded black-box groups. The explicit Lie input is not an escape from this coverage. [Theorems 1--2 and Sections 2--4](https://arxiv.org/html/0707.1260v1); [publication](https://link.springer.com/article/10.1007/s00453-010-9467-0).

Theorem 2 reduces HSP in a subgroup/quotient-closed constant-class family to exponent-p groups with `|H|` equal to 1 or p. It **does not lower the class to two or supply the higher-class solver**. Proposition 1 and Lemmas 5--6 already use automorphism-twisted actions and cancellation of linear/quadratic phases. Consequently, neither those primitives nor arbitrary-H recovery alone is the prospective contribution.

**Ivanyos--Santha, _Solving systems of diagonal polynomial equations over finite fields_, arXiv:1503.09016v2; TCS 657, 73--85 (2017).** Theorem 3 starts "Let d be constant." It gives a deterministic classical SDE algorithm over `F_q`, polynomial in `N` and `log q`, with the printed sufficient condition

`N > d^{d^2 log d} (m+1)^{d log d}`

for `m` equations and `N` variables. This is an actual algorithm, not just Chevalley--Warning existence. Theorem 5 and Corollary 6 solve univariate, vector-valued hidden polynomial graph states at fixed degree, allowing growing output dimension. Proposition 7 and Corollary 8 apply to `F_p^m semidirect C_p` of fixed nilpotency class, initially for order-p hidden subgroups outside the normal `F_p^m`. Both p and m may grow. The public semidirect action and the prescribed graph-state source matter; these statements do not assert arbitrary-Lie-algebra HSP. [Accepted manuscript, Theorems 3, 5, Proposition 7, Corollaries 6, 8](https://arxiv.org/html/1503.09016v2).

**Do not understate that semidirect overlap.** Decker--Ivanyos--Santha--Wocjan, _Hidden Symmetry Subgroup Problems_, arXiv:1107.2189v2, Section 5.2 explicitly recalls reduction of **all** hidden subgroups in `F_p^m semidirect C_p` to complements, then describes the polynomial-graph reduction. Combined with the preceding fixed-class solver, arbitrary H within that family is already covered. Theorem 5 also solves fixed-degree multivariate HPGP, but its oracle must have fibers `y-Q(x)=constant`. Merely having bounded-degree BCH coordinates does not establish that source promise. [Section 5.2 and Theorem 5](https://arxiv.org/html/1107.2189v2).

The related Decker--Hoyer--Ivanyos--Santha paper, arXiv:1305.1543v2 (QIC 2014), Theorem 1, treats fixed-degree scalar graph states over growing fields. Its technical Theorem 3 fixes output dimension `m`, unknown-parameter dimension `r`, and degree `D`. It already performs recursive phase linearization, but does not state the target HSP theorem. [Theorems 1 and 3](https://arxiv.org/html/1305.1543v2).

## Other Potential Matches

- **Smooth solvable groups:** Friedl--Ivanyos--Magniez--Santha--Sen, arXiv:quant-ph/0211091v4 (SIAM J. Comput. 2014), Theorem 4.16 solves HSP when the commutator subgroup is smoothly solvable, in the uniquely encoded black-box/oracle model. Section 2.2.3 requires bounded derived length and derived factors with a bounded-exponent subgroup of polylogarithmic index. Fixed nilpotency class does not imply this when p grows. Their elementary-abelian translation algorithm, Theorem 3.5, costs `(n+p)^{O(p)}`; Corollary 3.6 adds logarithmic confidence dependence. These are time algorithms, but not the required uniform growing-prime bound. [Definitions and Theorems](https://arxiv.org/html/quant-ph/0211091v4).
- **Current generalization:** Morales, arXiv:2608.05321v2, revised 2026-09-28, is a **preprint**. Theorem B covers scalar-action `A semidirect C_{p^k}` with bounded generator rank of A and `Exp(A)/p=poly(log|G|)`; Theorem A is the cyclic-normal-factor case. Theorem C covers arbitrary H in quasi-Hamiltonian groups with supplied Sylow and structural coordinates. These are algorithmic claims, not just distinguishability bounds. Our scope deduction: in the exponent-p, odd-p regime, the scalar action is trivial (its order divides both a p-power and p-1); Proposition 14's quasi-Hamiltonian action `a -> a^{1+p^s}` is likewise trivial. These families therefore do not cover the nonabelian target class. [Theorems A--C, Proposition 14, Section 4 input model](https://arxiv.org/html/2608.05321v2).
- **Information versus time:** Ettinger--Hoyer--Knill, arXiv:quant-ph/0401083v1 (IPL 2004), Theorem 1 gives `O(log^4|G|)` queries for arbitrary finite-group HSP, with exponentially small error and an exact variant under arbitrary one-qubit gates. The paper explicitly allows exponential time. This covers query sufficiency, not the target total-time theorem. [Theorem 1 and Section 2](https://arxiv.org/html/quant-ph/0401083v1).

The current-paper screen also checked [Dong et al., arXiv:2511.19494](https://arxiv.org/abs/2511.19494), on random generation and abelian-HSP sample counts, and [Liu et al., arXiv:2609.35656](https://arxiv.org/abs/2609.35656), on **abelian StateHSP** sample/query access. Their stated scopes do not supply general nonabelian subgroup recovery.

## Explicit Residual Question

**Does an existing publication already give a uniform, total-time `poly_c(input bits, log(1/epsilon))` algorithm, polynomial in n and log p, for arbitrary hidden subgroups of every explicitly represented exponent-p Lazard group of class at most fixed `c<p`, without the above structural restrictions?** A useful first separating regime is class three, `p>3`, unbounded dimension and ranks, with no promise of an abelian ideal of codimension one. This is a comparison regime, not a certified hard family.

For the proposed mechanism, the precise additional interface to locate in prior art is the **public oracle reduction** to a positive graded cover whose hidden lift is dilation invariant and still projects to the full original hidden Lie subalgebra in degree one. If available, that interface could connect known fixed-degree SDE algorithms to known central-conversion ideas. Neither central descent nor the SDE primitive should be presented as new. This review has **not** verified that interface, its composition, or its claimed runtime; it has only isolated what the examined scope statements leave unaccounted for.

## Review Boundary

Read-only inputs: [REES_HSP_REDUCTION.md](/Users/jaspersands/Developer/qsearch-research-work/rees-independent-review-2026-10-23/source/REES_HSP_REDUCTION.md) and [REES_RESOURCE_AND_PRIOR_ART.md](/Users/jaspersands/Developer/qsearch-research-work/rees-formal-core-2026-10-24/REES_RESOURCE_AND_PRIOR_ART.md). Search covered the named primary papers, their directly relevant reductions, and targeted 2024--2026 searches for nilpotent HSP, Lie/Lazard, SDE, Rees/homogenization, and graded/Carnot terminology. Only primary texts support the comparisons above. No finite-matrix tests, parent-proof recheck, implementation, application analysis, repository/Git/UI changes, or infrastructure work was performed. **No novelty or application is established; the bounded comparison ends here.**
