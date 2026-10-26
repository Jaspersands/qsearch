# Referee review: EXPLICIT_QUADRATIC_OPI

Note: `research/EXPLICIT_QUADRATIC_OPI.md`. Reviewed 2026-10-23 by codex-audit-correction-2026-10-23-r3. Overall: **needs-work**.

An in-session model judge read the note and quoted each claim from it; this is a triage, not peer review.

Both judges confirmed the balanced-predicate score formula, the accepted-flat decomposition, the trace-pairing union bound, its asymptotics and the 175/343 small check. I recomputed the filter means (0.688982, 0.747358, 0.889110, 0.816830) and the t=7,K=90 bound (2^-120.65). Both flagged the 'constructive classical explanation' headline as dropping the IID-GL, with-high-probability, fixed-R>1/2 asymptotic and review-pending conditions, and I confirmed it (at t=5,K=19 the bound is about 2^-0.76). The judges disagreed on the repair sentence: B called 'removes the finite mean-score signal' a gap because best-of-16-plus-repair is compared with a single-sample quantum mean. A held it, and I resolved it as holds because the sentence claims only the mean-score signal on the two named finite controls, quantum repetition does not change the quantum mean, and the note concedes the tail/runtime limitation in the adjacent section.

## Claims

### 1. gap

> The high-rate quadratic family has a constructive classical explanation, not a remaining quantum-advantage candidate

- Step: Revised Research Direction
- Finding: The supporting perfect-solution argument holds only with high probability for independent uniform T_i in GL(t,2), only asymptotically for fixed R>1/2 as t grows, and is review pending. The note itself says seeded replays are not IID certificates and that the complexity of the EXPLICIT inputs is the open question. At finite t the union bound can be weak: t=5,K=19 gives q^-K(1+qp)^N of about 2^-0.76, about 0.59. Rank also requires Nc<=Kt. Saved perfect inputs include N127,K90, both N31,K19, and the low-rate N7,K3 cases. The headline keeps none of these conditions.
- Conceded by the note's own self-check: no

### 2. holds

> A rational filter w has expected score

- Step: Actual Input And Known Quantum Mechanism
- Finding: For balanced predicates the DQI tridiagonal matrix has zero diagonal, and its Rayleigh quotient gives the formula. Recomputed top eigenvalues for ell=floor((K-1)/2), 0.5+lambda_max/(2N): 0.688982, 0.747358, 0.889110 and 0.816830, matching the table and the artifact enclosures. The strict condition 2ell+1<K+1 is respected. Both judges agree.
- Conceded by the note's own self-check: no

### 3. holds

> A dependence among the binary flat equations corresponds, through the nondegenerate field trace pairing, to a nonzero word of the generalized-RS dual

- Step: A Scoped High-Rate Perfect-Solution Bound
- Finding: Each binary row is Tr(beta f(alpha_i)), and F_q-linearity of the message space turns a dependence into sum_i gamma_i f(alpha_i)=0 for all f, with gamma_i in the uniform c-dimensional V_i. The MDS shortening count q^(w-K)-1, independence across positions and sum binom(m,w)(qp)^w<=(1+qp)^m give the stated bound. Both judges agree.
- Conceded by the note's own self-check: no

### 4. holds

> t->infinity through odd values gives c/t->1/2, so this upper bound tends to zero exponentially in Nt

- Step: A Scoped High-Rate Perfect-Solution Bound
- Finding: With qp<2^c, the log2 bound is at most Nt(c/t-R)+N log2(1+2^-c), negative and linear in Nt for fixed R>1/2. Recomputed: t=7,K=90 gives -120.65, below -100 as stated. The N127,K90 control has 508 rows in 630 bits. Both judges agree.
- Conceded by the note's own self-check: no

### 5. holds

> true rank-failure probability175/343, bounded by 27/49

- Step: A Scoped High-Rate Perfect-Solution Bound
- Finding: Ordered triples of 2D subspaces of F_2^3 sharing a nonzero vector: 7 identical, 126 with exactly two equal (two planes always meet in a line), and 42 distinct triples through a common line, 175 in total. The union bound is 7*(3/7)^3=27/49. Both judges agree.
- Conceded by the note's own self-check: no

### 6. holds

> implemented and removes the finite mean-score signal in both127-position controls

- Step: Revised Research Direction
- Finding: Judge B's gap was dropped. The artifact gives 109/127=0.858268 for both repaired controls, above the quantum expected reference 0.816830, while best-of-16 alone was mixed (104/127 vs 102/127), so the stated finite mean-score signal is indeed removed on those two inputs. B's point that quantum repetition would raise a best-of-T score concerns tails and cost, not the mean. The note concedes it explicitly ('a quantum sampler could also repeat'), so the sentence does not overreach.
- Conceded by the note's own self-check: no
