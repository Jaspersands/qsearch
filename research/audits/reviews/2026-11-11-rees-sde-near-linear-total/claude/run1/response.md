# Referee report: diagonal SDE claims (context_claims.md)

**Bottom line.** I found no fatal error in Claims 1–6. Claims 1, 2, 3, 5 and 6 are correct as written. Claim 4's mathematics is correct. Its algorithmic version needs one clarification, and its hypothesis p ≥ κ⁴ is logically redundant. The cheapest decisive attack was a counterexample to Lemma R's case split, and it fails.

## 1. Per-claim verdicts

**Claim 1: CORRECT.** Checked step by step:
- **Identity.** Identify span T with F_p^D and expand the indicator of Σy_i^κλ_i = 0 in additive characters. This gives exactly p^{-D} Σ_u Π S(⟨u,λ_i⟩).
- **Product bound.** p^z((κ-1)√p)^{n-z} = ((κ-1)√p)^n A^z.
- **Inclusion-exclusion.** For each T', #{u ≠ 0 : T' ⊆ Z(u)} = p^{D-rk T'} − 1. Terms with rk T' = D vanish, which justifies the restriction to rk T' < D.
  - Replacing (A−1)^{|T'|} by A^{|T'|} needs A ≥ 1, i.e. p ≥ (κ−1)²; the hypothesis implies this.
  - Dividing by p^{n-D} gives (κ−1)^m p^{c−m/2}.
  - Every remaining T' has c ≥ 1 and m ≥ 1.
- **Densest step.** With no zero columns, the only rank-0 subset is ∅. For rk T' ≥ 1, |T'| ≤ δ·rk T', so m ≥ δc.
  - t/(2+t) is increasing, so η' ≥ η suffices.
  - The sum over m ≥ 1 of C(n,m)x^m equals (1+x)^n − 1 ≤ e^{1/2} − 1.
  - N > 1 and N is an integer, so N ≥ 2 and some y ≠ 0 exists.
- **Redundant hypothesis.** The bound n0 ≤ ⌊(2+η)d⌋+1 is never used (a larger bank contains a smaller one).
- **Corollary (b).** Correct:
  - Each x ∈ P0^n has at most κ^n preimages y.
  - The positivity condition 0.35κ^{-n} > p^{-(n-D)} holds because n − D ≥ n/2 and p > 9κ². This should be stated explicitly.
  - The parametric minimization of δ·rk − |·| is submodular. Its breakpoints are rationals with denominators ≤ d.

**Claim 2: CORRECT.**
- Z(u) is exactly the set of columns in W(u), since W(u) ⊆ u^⊥.
- Since rk(T∩W) = w, densest gives n − n_W ≥ δ(D−w). This holds for w = 0 as well, with no zero columns.
- Integrality gives n − n_W ≥ 2(D−w)+1. Distinct proper flats correspond to distinct proper column subsets, so there are at most 2^n − 1 of them.
- The strict inequality follows from √p > (2κ−2)^{2d+1} ≥ (2κ−2)^n. The final step uses p^{n-D}2^{-n} ≥ p·2^{-n} > 1.
- For κ = 2 the claim is subsumed by Chevalley–Warning.

**Claim 3: CORRECT.**
- If x_{−v} = 0, then x_D would be a solution of D, contradicting deadness. So x_{−v} ∈ P.
- P is a group, so x_D/x_{−v} ∈ P0^{2u}.
- The edge case u = 0 is trivial.

**Claim 4 (mathematics): CORRECT.**
- **Coverage.** Every spanning bank with no zero column falls into (A), (B) or (C): some proper U has ≥ 2u+1 columns, exactly 2u columns, or ≤ 2u−1 for all U (which is ssc). Zero-column and non-spanning banks are handled first, by trivial solution or by induction at rank d' < d.
- **Quotient argument.** Columns of B∖D lie outside U by definition, so their images are automatically nonzero; nothing further is needed. The step uses only |B∩U| = 2u, not the failure of (A). If w = 0, the U-step yields y_w ≠ 0, x_D = 0, which still works.
- **Use of the hypothesis.** The induction invokes the conclusion only at dimensions u, d−u, or d' < d. The hypothesis is invoked at dimension d only in case (C). The strong induction is well-founded.
- **Repair (cosmetic).** p ≥ κ⁴ is logically unnecessary. An ssc bank at d = 1 is any bank of 3 columns spanning F_p, so H(1) already equals C(1). The Lemma W computation instead shows H(1) holds unconditionally for p ≥ κ⁴: p − 2 − (κ²−1)√p ≥ √p − 2 > 0. Lemma W is imported, not verified here. It is the standard Weil multiplicative-character bound and is plausible.

**Claim 4 (algorithmic version): CORRECT WITH REPAIR.** The unrestricted minimum of f(T) = 2rk(T) − |T| over T ⊆ B∖{e} is trivially ≤ 0: f(∅) = 0, and f(B∖{e}) = 0 whenever B∖{e} spans. The plain minimum therefore detects only (A).
- **(A)** is detected by min f < 0. Any such T has 1 ≤ rk T ≤ d−1, since |B∖{e}| = 2d.
- **(B)** requires, for each ordered pair (e, g) with g ≠ e, the minimal minimizer M of f over {T : g ∈ T ⊆ B∖{e}}, followed by a check that rk M < d.
  - The minimizers form a lattice. With (A) excluded, min f = 0.
  - Any tight proper T ∋ g contains M, so rk M ≤ rk T < d.
  - Every tight proper flat has ≥ 2 columns and misses at least one. So O(n²) submodular-minimization calls suffice.
- **Execution order.** The recursion is sequential: w depends on the oracle's quotient answer. The tree has ≤ d leaves and ≤ 2d−1 nodes, with a polynomial-time rank oracle over F_p.
- The κ = 2 remark is correct.

**Claim 5: CORRECT.**
- No zero column can lie in G, so G is dead.
- |G| ≤ 2u follows from N(u) = 2u+1.
- B̄ may contain zero columns (columns of B inside U). This is harmless.
- If w ≠ 0, Claim 3 gives x_G with Σx_Gλ = −w and x_G ≠ 0, contradicting "unused."
- The edge cases u = 0 and u = a are fine. Only the inequalities N ≤ 2d'+1 are used.

**Claim 6: CORRECT.**
- 2^n ≥ 2p^a > p^a, and ±1 ∈ P.
- −1 ∈ P is automatic for κ odd. For κ even it holds iff p ≡ 1 mod 2κ.
- The base-p encoding fits in n−1 bits because p^a ≤ 2^{n−1}. It is computable by a poly(n, log p)-size circuit, and a collision s ≠ t maps back to s − t.
- This gives membership in PWPP, nothing more.

## 2. Data line N(3,3,13) ≥ 8, N(3,2,13) = 5

No contradiction.
- **Claims 1 and 2.** Their thresholds (≥ (2·2·10)^6 for Claim 1; 4^{14} for Claim 2 at d = 3) far exceed 13. A 7-column bank also lies below the 3d+1 = 10 of Claim 1.
- **Claim 4.** The dead ssc bank means H(3) fails at p = 13, so Lemma R simply does not apply.
- **Predicted consistency check.** C(1) holds at p = 13. A dead 3-bank in F_13 plus a dead pair on a new axis would be a dead 5-bank in F_13², contrary to max = 4. C(2) holds by the data. The proof of Lemma R then predicts that every dead 7-bank in F_13³ must be ssc. The reported bank is ssc, as required. A non-ssc dead 7-bank would have refuted Claim 4 or the d = 2 data.
- **Sanity check.** |P0| = 5, so the 5^7 search space is right.
- **Implication.** Totality at d = 2 does not propagate to d = 3 at fixed small p. This is consistent with Claim 2 needing a p-threshold that grows with d.
- I did not rerun the computation.

## 3. Known results (from memory; no browsing available)

- N(κ,d,p) is a weighted Davenport constant D_A(F_p^d) with weight set A = P. I recall literature on weighted Davenport constants (Adhikari and coauthors), including quadratic-residue weights in cyclic groups. I cannot confidently state any result covering Claims 1–4 for F_p^d. Status: **unknown**.
- Solvability of systems of additive (diagonal) forms with 2R+1 variables, under rank or "partition" conditions, resembles Davenport–Lewis-type theory. I am not confident of a precise finite-field statement matching Claims 1 or 2. Status: **unknown**.
- I am confident of one structural fact. The condition "every subspace U holds ≤ 2·dim U columns", i.e. densest ratio ≤ 2, is exactly the Edmonds / Nash-Williams matroid-covering criterion for the bank to be a union of two independent sets. Claims 1, 2 and 4 effectively split on this criterion. It is a known tool, not a known proof of these claims.
- Claim 3 is the standard "append −v" Davenport-type argument.

## Proof obligations and falsifiers remaining

- Verify Lemma W independently.
- State the positivity condition in Corollary (b).
- Write out the minimal-minimizer detection over pairs (e, g) explicitly.
- **Falsifier for Claim 4:** a dead, non-ssc (2d+1)-bank at some p where C(d') holds for all d' < d.
- **Falsifier for Claim 2:** any dead (2d+1)-bank with p > (2κ−2)^{4d+2}.