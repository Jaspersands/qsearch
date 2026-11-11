# Referee report: SPARSE2 (Claim 1) and the lifting lemma with its simplex corollary (Claim 2)

## Verdicts

- **Claim 1 (SPARSE2): ACCEPT WITH FIXES.** I found no correctness gap. The fixes are presentational: the r-rule must be specified, and the numerical claims should be labelled as finite checks.
- **Claim 2, lifting lemma: ACCEPT WITH FIXES.** The proof is correct. It needs one undefined term defined, and it needs a stated generalization of Lemma 2(B).
- **Claim 2, corollary:**
  - The statements about R(X_r) and about 2-dim subcode supports: **ACCEPT WITH FIXES**.
  - The final cost sentence ("each piece costs ≥ (12/25)·5^r … equals SPARSE2's bound"): **REJECT as stated**. Downgrade it to a first-stage remark.

I did not find a cheap falsifier for the central claim. Every attack below closed.

## Claim 1 findings

**1.1 (a) Applying Lemma 2(A) to Y = supp W. Holds.**
- Each row of W = row(AG) lies in D0 ⊆ D(X) and is supported on Y. So it restricts to a dependency of Y.
- With labels ℓ_i = A g_i, we have Σ_{i∈Y} ⟨γ_α, ℓ_i⟩ v_i = Σ_i (γ_αᵀ A G)_i v_i = 0. This is a W-codeword, which is exactly the cancellation Lemma 2(A) needs.
- Spanning: G has rank r, so its column space is all of F_5^r. Then A(F_5^r) = F_5², and since columns with A g_i = 0 contribute nothing, the labels on Y span F_5². Fact F5 therefore applies.
- Witness branch: if h_1, h_2 are dependent, take α ≠ 0 with α·h = 0. Weak nondegeneracy gives some λα with y_{λα} ≢ 0 on L. Every label in L occurs on some column, so this realizer is a nonzero S-vector on Y with sum 0. Correct.

**1.2 (b) Averaging. Holds.**
- 2-dim subspaces of row(G) biject with 2-dim subspaces of (F_5^r)*, because the rows of G are independent. These in turn biject with codimension-2 subspaces K = ker A.
- The codim-2 subspaces containing a fixed g ≠ 0 correspond to codim-2 subspaces of F_5^r/⟨g⟩. So ρ_r = [r−1,2]_5/[r,2]_5 = (5^{r−2}−1)/(5^r−1). The q-binomial algebra checks.
- Columns with g_i = 0 (coloops of D0) are in no supp W. They contribute 0 to both the minimum and the average, so the bound min ≤ (1−ρ_r)·#{g_i ≠ 0} ≤ (1−ρ_r)(q+r) holds.
- 1 − ρ_r = (5^r − 5^{r−2})/(5^r − 1). Check: r = 2 gives 1, which recovers the q+2 cost of B′.

**1.3 (c) Compatibility with Lemma 1. Holds.**
- Pieces are pairwise disjoint because returned columns never belonged to a piece.
- Returned columns are simply re-projected into V/⟨h1,h2⟩.
- Each stage's gain or witness is computed modulo the current U. That is exactly the "realizes modulo earlier ones" hypothesis of the chain.
- A witness found in a quotient lies in U and is nonzero, so Lemma 1 back-propagates it.
- A zero column (v_i = 0) is itself a weight-1 witness. Either the algorithm processes it as usual or it can be short-circuited.

**1.4 (d) Pool requirement and closed form. Holds, with slack.**
- Monotonicity: need(q) = max(q+r, cost + need(q−2)) is monotone in cost, and the actual cost ≤ c(q). So need(n) ≤ G(n).
- Induction: G(q−2) ≥ q for q ≥ 4 (and G(0)=1, G(1)=3 cover the small cases). Also q + r − c(q) ≤ (q+r)/25 + 1. Hence G(q) = c(q) + G(q−2) for every stage, and G(n) ≤ Σc + 3.
- The q = 1 base case is right: {a+bc : a,b ∈ S} = F_5 for every c ≠ 0.
- Per-stage bound: r0 ≤ log_5 q + 2, and (q + log_5 q + 2)/(5q−1) ≤ 1 for q ≥ 2. So c(q) ≤ (24/25)(q + log_5 q + 3).
- Summation:
  - Σq ≤ (n²+2n)/4 for both parities.
  - There are at most n/2 stages, each with log_5 q ≤ log_5 n.
  - Result: 0.24n² + 0.48 n log_5 n + 1.92n + 3.
- The stated "+3n+3" is therefore valid but loose. The "(q−2)/2" step in the context is unnecessary.

**1.5 (e) Running time. Holds.**
- With 5^{r0} ≤ 25q, the number of subspaces is [r0,2]_5 ≈ 5^{2r0−1}/96 ≤ ~1.3q².
- Each support count costs O(r(q+r)). That gives O(q³ log q) per stage.
- Gaussian elimination and re-projection cost O(n³) per stage. Reading the input costs O(mn).
- The Fact F5 lookup is O(1): canonize L ⊆ F_5²∖0 under |GL_2(F_5)| = 480 and index a fixed table.
- Total: deterministic poly(n, m).

**1.6 Fix: the r-rule.** "Choose r ∈ [2, ⌈log_5 q⌉+2] (deterministic rule)" is underspecified. The proof only covers r = r0 or r = argmin_r ⌊(q+r)(1−ρ_r)⌋. State one of these.

**1.7 Fix: label the finite controls.** "Checked numerically for n ≤ 30000" and "below B′ for all n ≥ 29" concern the exact recursion G. They are not proofs.
- The analytic bound 0.24n² + 0.48 n log_5 n + 1.92n + 3 beats n²/4 + 1.5n + 2 only when 0.01n² > 0.48 n log_5 n + 0.42n + 1. That means n ≳ 200.
- The asymptotic claim (leading constant 6/25 < 1/4) is fully proved. The small-n crossover is a finite check only.

## Claim 2 findings

**2.1 K_H is a subspace. Correct.**
- α ↦ Σ α_j Φ_j|_H is a linear map into the space of functions H∖0 → F_5.
- The restrictions of linear functionals form a subspace of that space.
- K_H is the preimage of a subspace under a linear map, hence a subspace.

**2.2 "K_H = 0 ⇒ contradiction". Correct, but "strongly nondegenerate" is undefined.**
- Define it as: y_α ≢ 0 for every α ≠ 0. That implies weak nondegeneracy, which is what the induction hypothesis needs.
- If K_H = 0, then for every α ≠ 0, y_α|_H equals a non-linear function plus a linear one, so it is not linear and in particular ≢ 0.
- Feasibility survives restriction: the values stay in S, and γ_α|_H is a functional on H ≅ F_5^{k−1}, with H∖0 corresponding to L_{k−1}.

**2.3 Pigeonhole and the degeneracy step. Correct for weak nondegeneracy as defined.**
- Counting: for k ≥ 4 there are (5^k−1)/4 ≥ 156 hyperplanes. Each K_H contains at least one of the 31 lines of F_5³. So some line ⟨α⟩ ⊆ K_{H1} ∩ K_{H2} with H1 ≠ H2.
- Vanishing on H1 ∪ H2: for α ∈ K_H, each y_{λα}|_H is an S-valued linear functional on H. Since dim H ≥ 3 ≥ 1, a nonzero functional is surjective and would take the value 2. So y_{λα}|_H = 0 for all λ.
- Extending to all of F_5^k: y_{λα} − λy_α = ⟨γ_{λα} − λγ_α, ·⟩ is linear. It vanishes on H1 ∪ H2, which spans F_5^k. So y_{λα} = λ y_α everywhere.
- Taking λ = 2: if y_α(ℓ) = ±1 then y_{2α}(ℓ) = ±2 ∉ S. So y_α ≡ 0, and then every y_{λα} ≡ 0. The direction [α] is degenerate, a contradiction. ∎

**2.4 Lemma 2(B) is applied outside its stated scope.** Lemma 2(B) is stated with d = k. The corollary uses labels in F_5^r with gain dimension 3 ≠ r.
- The proof does carry over verbatim provided W = D(X). That holds here: rank(X_r) = q, so dim D(X_r) = r and D(X_r) is the simplex code itself.
- The no-witness part also holds. A nonzero S-codeword would be a nonzero functional on all of F_5^r∖0, which takes the value 2.
- Fix: state the d ≠ k version of Lemma 2(B) explicitly, with the hypothesis W = D(X).
- "No Y ⊆ X_r gains 3" then follows from R(Y) ⊆ R(X_r).

**2.5 The support formula is correct.** A 2-dim subcode corresponds to a 2-dim space Γ of functionals. Its support is (5^r−1) − (5^{r−2}−1) = 5^r − 5^{r−2}.

**2.6 The cost sentence: REJECT as stated.** Four problems:
- **Unproved input.** It relies on "one dependency never gains two dimensions", a finite check that is not among the given inputs and is uncertified here. For the record, the 0-dependency case is easy: with D(Y) = 0, each map α ↦ y_α(i) is linear and S-valued, hence 0.
- **First stage only.** The bound holds only for pieces gaining in the original V. Once some H is realized, the remaining columns of X_r acquire new dependencies modulo H. The simplex structure is gone, so this is not a bound on later pieces or on a whole run.
- **Mismatched r.** At q = 5^r − 1 − r, SPARSE2's rule gives r0 = r + 1, since ⌈log_5 q⌉ = r. So SPARSE2 takes 5^r columns, not the 5^r − 1 of X_r. "Equals SPARSE2's averaging bound at that (q, r)" compares against a different r than the algorithm uses.
- **Scope.** It is a statement about this framework only. It is not a lower bound for the problem. The corollary and the lifting lemma are framework limitations, not hardness evidence.

## Item 3: room below 6/25

**Evident reason the bound cannot be improved within a single stage** (proved, given the lifting lemma and T3):
- Suppose the window is a simplex block. Then every 2-dim subcode has the same support, so min = average and no better W-selection rule helps.
- Every 3-dim dependency space of any Y ⊆ X_r is a 3-dim simplex subcode. Its label map is onto F_5³, so every nonzero label occurs. Fact T3 then makes it infeasible.
- So no selection rule can force a "provably feasible family of 3-dim label sets". The adversary realizes only full label sets, and dropping columns only shrinks the dependency space.
- Enlarging r does not help either: 1 − ρ_r > 24/25 for every r ≥ 3, and 1 − ρ_2 = 1.
- Hence 6/25 is the floor for any per-stage rule of the form "pick a 2- or 3-dim subcode of the window's dependencies".

**The only lever left is cross-stage (speculative).** A real 3-dim gain would be worth a lot: its cost per dimension is about (124/125)/3 ≈ 0.33 of q, versus 0.48 for 2-dim gains. To use it:
- The algorithm, which chooses h through the Φ freedom in F5, would have to force a non-simplex window in some later quotient. Note that returned columns carry labels in K, a 5^{r−2}-element subspace.
- Proof obligation: show the adversary cannot keep every window simplex-like in V/⟨h⟩ for all choices of Φ.
- Falsifier: a recursive adversary construction that keeps every window simplex-like regardless of Φ. That would show 6/25 is the worst case for this framework, though still not for the problem itself.