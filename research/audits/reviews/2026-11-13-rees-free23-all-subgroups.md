# free23 without a cover: spoiled copies, and every subgroup (2026-11-13)

**Status: AI-checked, pending human review.** One AI session (Claude), hostile to its own conclusions. Target:
Theorem F23 of `2026-11-13-rees-free23-theorem.md` (Route A) and its referee. Scripts and outputs are in
`2026-11-13-rees-free23-all-subgroups/`; they import the second referee's group code read-only. No existing file was
edited. Finite checks only falsify (TRAPS 7). "(memory)" marks citations not re-read here.

## Verdict

* **(A) Spoiled copies are harmless: PROVED (given Lemma 0 and the F23 lemmas).** The threshold p ≥ 5000 and the
  brute-force branch are both removed: Route A works for every prime p ≥ 5.
  * **Lemma 0′.** A spoiled copy (λ′·e′ = 0) leaves, after the front end with outcome y, the classical mixture
    uniform on R_y = {x : q_y′(x) = 0}, where q_y = A_1x + A_2x² + A_3x³ are Lemma 0's public forms at the true θ.
    |R_y| ∈ {1, 2}, and Pr[y] = |R_y|/p².
  * **Lemma S.** A run whose used supports contain spoiled copies ends, before the final QFT, on one line w* + F_pe′
    with phase c_0 + μτ, where μ is the same public form as in Lemma E. So the equation holds **with certainty**,
    exactly as in the unspoiled case.
  * **Lemma C′.** Pr[D_l = 0] = 1/p for every level-2 state, spoiled or not. This replaces the referee's open
    "spoiled-triple Lemma C".
  * **Theorem F23′.** For every p ≥ 5, one attempt succeeds with probability s(p) ≥ (1 − 3/p)²(1 − 1/p). That is
    0.128 at p = 5, 0.280 at 7, 0.481 at 11, 0.546 at 13, and ≥ 0.998 for p ≥ 5000. The copy count is unchanged:
    18m/q_adm(p) + O(1) per attempt. Nothing is detected; spoiled copies are tolerated.
* **(B) Classification (Lemma T, PROVED by hand; counts checked exhaustively at p = 5 and 7).** free23 has 13 types
  of subgroups, determined by the image in G/[G,G], s = log H ∩ γ_2 and s ∩ γ_3. Every type is recovered without the
  cover, by one of three routes:
  * abelian Fourier sampling on an H-independent or computed subgroup (types 3, 5, 6, 9, 11, 12, 13, and type 10
    when the public g_0 ∥ e). Types 1, 2 and 4 are a certified-nothing default after the F23 or IS branch;
  * **Route A** (Theorem F23′), needed only when H is hard cyclic;
  * Ivanyos–Santha Cor 8, inside G/⟨q⟩ ≅ fil4 or G/γ_3 ≅ heis, needed only when H = ⟨exp η⟩·S with S = F_pq a generic
    central line, or S = γ_3.
  
  Route A itself fails for every non-hard-cyclic type, for a precise reason (§B2): labels on one line, so no
  admissible triple; or zero labels; or every copy spoiled. But none of those types needs it.
* **(C) Theorem HSP23 (PROVED given cited theorems; AI-checked, pending human review).** The standard HSP in free23
  over F_p, p ≥ 5, for **arbitrary** H, is solvable without the cover with poly(log p) queries and time. The error is
  one-sided and at most (1 − s(p))^R + ε_IS. The cited theorems are IS Cor 8 (Prop 7 + Thm 5 + Thm 3), standard
  abelian HSP, Las Vegas roots, and an exact QFT_p (approximate-QFT hybrid from memory). Every certified output is
  correct, because membership is checked by classical oracle queries.
* **(D) Exact end-to-end simulations, falsification only.**
  * Route A with unconditioned labels: p = 5, 150 attempts, and p = 7, 40 attempts.
  * The whole algorithm, all 13 types: p = 7, 11 and 13.
  * Result: 0 wrong outputs (143 whole-algorithm instances; 190 Route-A attempts), 0 wrong equations (314/314), and 0
    failures of the support-line and phase checks of Lemma S (286 spoiled runs). Numbers in §D.
* **(E) Free 3-generator class-3 group: Route A breaks at its first step (PROVED by hand).** G/ker λ has no abelian
  normal subgroup of index p, so the IS front end, and with it Lemma 0, has no analogue.
* **H-dependence audit.** No step quotients by a non-normal subgroup or uses a normalizer. The only H-dependent
  quotient is by ⟨q⟩ = H ∩ γ_3, which is central, computed and certified to lie in H first; it is the same as the
  label promotion G/ker λ that F23 already uses (§B3). This is not the frozen-normalizer error of the old drafts.
* **Claim gates stay false:** "cover unnecessary for free23", novelty, speedup. The core paper is not edited.

## 0. Setting

* **Notation** as in F23 §0. L is free 2-generator class 3 over F_p, p ≥ 5, with basis X_0, X_1, Z, U, W, and
  G = (L, BCH).
* **Hard cyclic H.** H = ⟨exp η⟩ with η = e_0X_0 + e_1X_1 + e_3Z + η_c and e ≠ 0.
* **Labelled copy.** (λ, ρ_{K,χ_λ}) with K = Hγ_3.
* **Front end.** For λ ≠ 0 it uses g_0 = (λ_1, −λ_0), a chart x′, n = λ·x′, f(v) = λ·v/n and
  h(v) = det(x′,v)/det(x′,g_0).
* **Lemma 0's forms.** A_3 = −(n²/6)h(e), A_2 = (kn/2)h(e) + (n/2)e_3 and A_1 = −jh(e) − ke_3 + λ(η_c), with δ = n.
  The referee fits the sign convention CONV = (−1, −1, 1), and the scripts use the same one.
* **Spoiled copy.** f(e) = 0, that is, λ·e = 0.
* **Oracle model (for (B) and (C)).** The standard HSP oracle f: G → S, constant exactly on left cosets of H.
  Coset states are made from f, and a classical query f(g) = f(1) decides g ∈ H.

## A. Spoiled copies

### A1. Lemma 0′ (PROVED)

**Statement.** Let λ ≠ 0, let e ≠ 0, and suppose λ·e = 0. Then e = h·g_0 with h = h(e) ≠ 0. After promotion to
G/ker λ, the QFT over N_λ and the outcome y = (j,k) in the occupied sector:
1. the pair (y, x_0) is uniform on the incidence set I = {(y, x) : q_y′(x) = 0}, where
   q_y′(x) = A_1 + 2A_2x + 3A_3x²;
2. given y, the x-register is (1/|R_y|)Σ_{x∈R_y}|x⟩⟨x|, with R_y = {x : q_y′(x) = 0};
3. |R_y| ≤ 2, since the leading coefficient of q_y′ is 3A_3 = −(n²/2)h ≠ 0.

*Proof.*
1. **H lies in N_λ.** Since e ∈ F_pg_0, we have η ∈ log N_λ mod ker λ, so H ≤ N_λ (mod ker λ).
2. **Each coset sits at one x.** Write a coset as gH with g = m·exp(x_0x′), m ∈ N_λ. Then
   gH = {m·Ad_{exp(x_0x′)}(exp tη)·exp(x_0x′)}, because Ad_{exp(x_0x′)} preserves the normal subgroup N_λ. So every
   coset lies at the single chart coordinate x = x_0. The base point is uniform, so x_0 is uniform.
3. **The N_λ-register.** It holds a uniform superposition, with the label character, over a coset of the abelian
   subgroup exp(F_p·Ad_{x_0}η)·(γ_3/ker λ). The character is trivial on H itself.
4. **The Fourier outcome.** It is therefore uniform on the y in the sector with ỹ(Ad_{exp(x_0x′)}η) = 0.
5. **Expanding Ad.** Ad_{exp(xx′)}η = η + x[x′,η] + (x²/2)[x′,[x′,η]]. Here [x′,g_0] = −δZ, λ([x′,Z]) = n and
   δ = n. This gives ỹ(Ad_xη) = jh + k(e_3 − xhn) − (λ(η_c) + xne_3 − (x²/2)hn²) in the occupied sector l = −1, and
   that equals −q_y′(x) term by term.
6. **Counting.** The condition is linear in j with coefficient h ≠ 0. So for each x_0 there are exactly p outcomes y,
   which gives (1). Different x_0 come from different cosets, so the mixture is incoherent, which gives (2). ∎

**Check** (`spoiled.py`, `spoiled.out`; exact mixed states, summed over base points covering every coset of K).
* In 288 (instance, y) blocks at p = 5 and 7, there were 0 failures of diagonality, support = R_y, equal weights,
  and Pr[y] = |R_y|/p².
* |R_y| was 2 in 206 blocks and 1 in 82.

### A2. Lemma S: spoiled runs give correct equations (PROVED, given Lemma 0, Lemma L and the F23 Lemmas W, E)

**Statement.** Fix one run of Route A: any admissible labels, Lemma-B weights, and any outcomes. Suppose some used
copy is spoiled. Then:
1. the state before the final QFT_{F_p²} is a mixture of pure states;
2. each pure state is supported on exactly one line w* + F_p e′ (with M = I), with constant modulus;
3. along that line its phase is c_0 + μ(θ)τ, where μ is the public linear form of Lemma E.

Hence z·e′ = μ with certainty, and ℓ′·ε = 0 holds exactly as in Lemma E.

*Proof.*
1. **At most one spoiled copy per triple.** The spoiled labels form the single line {λ : λ·e′ = 0} of γ_3*, and
   labels in a triple are pairwise independent.
2. **A spoiled triple's plane state lives on a line.** Let triple j have its spoiled copy at position i*. By Lemma 0′
   that copy is a delta at some x_0 ∈ R_y (one branch of the mixture). The plane state χ_j(a), with
   a ↦ x_r + (s_if_i(a))_i a bijection onto {Σn_ix_i = r} (Lemma P(b) of the pair-measurement report), is supported
   on ℓ_j = {a : x_{r,i*} + s_{i*}f_{i*}(a) = x_0}. That is a line parallel to ker(λ_{i*}·) = F_pe′. Its modulus is
   constant there, because the other two copies are flat (Lemma 0).
3. **Level 2.** Ψ_l(w) = Π_j χ_j(u_j(w + d_j)), with u_j ≠ 0 on the support. It is supported on the intersection of
   the lines u_j^{−1}ℓ_j − d_j, all parallel to e′. That intersection is one line, or empty; empty has probability
   0.
4. **Level 3.** The same argument applies to Π_l Ψ_l(u_l′(w + d_l′))ω^{R(w)}.
5. **The formal increment.** For a copy, put
   Δ(Y, τ) := τcs·q′(Y) + τ²c²s²f(e)(A_2 + 3A_3Y) + τ³c³s³f(e)²A_3. This is a polynomial in (Y, τ, θ), Lemma L, with
   no pole. Write Δ_tot(w_0, τ; θ) for the sum of Δ over all used copies, at their coordinates Y_ji(w_0), plus the
   increments of the public corrections (Q_3 of each level-2 state, scaled by u′, and R).
6. **Δ_tot is linear in τ.** The derivation of Lemma E consists only of polynomial identities in (w_0, e, ε). Lemma W
   is tensor algebra "for all e", (E3) and the level-3 conic are identities in (w, e), and nothing divides by f(e).
   So Δ_tot(w_0, τ; θ) = μ(θ)τ **identically in θ**, including spoiled θ.
7. **What the true state does.** On the support line, the true phase increment is the sum of Δ over the
   **non-spoiled** copies (Lemma 0), plus the corrections. A spoiled copy contributes nothing, since it is a delta.
   Its formal term at its coordinate Y = x_0 is Δ = τcs·q′(x_0) + 0 + 0 = 0, because q′(x_0) = 0 (Lemma 0′) and
   f(e) = 0.
8. **Conclusion.** So the true increment equals Δ_tot = μτ. A state ω^{c_0+μτ} on w* + F_pe′ has Fourier support
   {z : z·e′ = μ}. ∎

**Check** (`e2e_spoiled.py`). The referee's exact simulator (true coset states, true labels, true σ-permutations) was
run with unconditioned labels and asserted, in every spoiled run, that the support is exactly one line parallel to
e′ with ratio Ψ(w* + τe′)/Ψ(w*) = ω^{μτ}.
* p = 5: 227 spoiled runs checked, 0 line failures, 0 phase failures.
* p = 7: 59 spoiled runs checked, 0 line failures, 0 phase failures.
* All equations held: 247/247 at p = 5 and 67/67 at p = 7.

### A3. Lemma C′: D_l is uniform for every level-2 state (PROVED)

**Statement.** For every level-2 state l and every label configuration, spoiled or not, Pr[D_l = 0] = 1/p.
Consequently Pr[C forced to 0 in a run] ≤ 3/p (Lemma C's union bound).

*Proof.*
1. **D_l in terms of the outcomes.** With x_r = (r/n_1, 0, 0) and X_{ji} = x_{r,i} + s_if_i(u_jd_j), one has
   Σ_is_in_iX_{ji} = s_{j1}r_j + u_jP_2(T_j)·d_j. Using (E3) to eliminate the reference offset, the referee's closed
   form becomes

   D_l = −Σ_{j∈supp} u_j[s_{j1}r_j + P_2(T_j)·a_j + Σ_is_{ji}k_{ji}], with a_j = u_jb_j.
2. **A coupling.** The coset outcome (d_j) has the law obtained by drawing the a_j independently from |χ_j|², and
   D_l depends only on the true outcomes. So it suffices to fix one j ∈ supp and show that
   g_j = s_{j1}r_j + P_2(T_j)·a_j is uniform, conditionally on all other triples and on the front-end outcomes of
   triple j.
3. **Non-spoiled triple.** r_j is uniform, because the x-registers are flat. χ_j has flat modulus, so a_j is uniform
   and independent of r_j. With s_{j1} ≠ 0, g_j is uniform.
4. **Spoiled triple, i* ≠ 1.** ℓ_j = {λ_{i*}·a = n_{i*}x_0/s_{i*}} does not depend on r_j. Given x_0, r_j is uniform,
   so g_j is uniform.
5. **Spoiled triple, i* = 1.** Here a_j is uniform on {λ_1·a = (n_1x_0 − r_j)/s_1}.
   * If P_2(T_j) ∉ F_pλ_1, then P_2·a_j is uniform given r_j.
   * If P_2 = κλ_1, then g_j = r_j(s_1 − κ/s_1) + const. Here κ ≠ s_1², because otherwise s_2²λ_2 + s_3²λ_3 = 0,
     which is impossible for independent λ_2, λ_3 and s_2s_3 ≠ 0. And r_j is uniform given x_0.
6. **Conclusion.** u_j ≠ 0, so D_l is uniform. The 3/p bound follows from Lemma C: if every D_l ≠ 0, a u′ on the
   conic with u′·D ≠ 0 exists. ∎

**Check** (`e2e_spoiled_5.out`). D_l = 0 in:
* 59/325 clean states;
* 99/575 states with a spoiled copy;
* 66/349 states whose every support triple is spoiled.

The prediction is 1/p = 0.2 in each case. At p = 7 (`e2e_spoiled_7.out`) the counts are 19/126, 18/114 and 11/81, against
1/p = 0.143.

### A4. Theorem F23′ (PROVED given cited theorems; AI-checked, pending human review)

Same hypotheses as F23 (hard cyclic H, labelled copies), now for **every prime p ≥ 5**.

* **One attempt.** Two runs, each with a fresh uniform σ ∈ Aut(L) and 3 level-2 states of m = 9g_3(p)² triples. Then
  the cross product, the η_c step and verification.
* **Success.** An attempt outputs a generator of H with probability

  s(p) ≥ (1 − 3/p)²·(1 − 1/p).

  The two factors (1 − 3/p) come from Lemma C′, one per run; (1 − 1/p) is Lemma R(b). Lemma R(a), the |B|/(p+1)
  term, is no longer needed.
* **Copies per attempt (expected).**
  * 18m/q_adm(p) for the runs, where q_adm(p) = (p²−1)(p²−p)(p−1)²/p⁶ (0.49 at 5, 0.745 at 11, ≥ 0.9994 at 5000);
  * 2 + O(1/p) for the η_c step;
  * v verification copies (wrong candidates pass with probability ≤ p^{−v}).

  For example, m = 36 at p = 5 gives ≈ 1320 copies (q_adm = 0.4915), and m = 144 at p = 7 gives ≈ 4204
  (q_adm = 0.617; the referee observed 4217).
* **Overall error** after R attempts: ≤ (1 − s(p))^R + R·p^{−v}. In the oracle model, verification is one classical
  query, and the second term disappears.
* **Threshold.** No brute force is needed. The old p_0 = 5000 came only from Lemma R(a).

**Observed rates** (unconditioned; all failures are "C forced 0" or proportional pairs, none wrong):

| p | success rate | bound s(p) |
|---|---|---|
| 5 | 82/150 = 0.547 | 0.128 |
| 7 | 23/40 = 0.575 | 0.280 |
| 11 | 37/40 (referee) | 0.481 |
| 13 | 9/10 (referee) | 0.546 |

## B. Every subgroup of free23

### B1. Lemma T: classification (PROVED; exhaustive count check at p = 5, 7)

Lazard (p > 3) identifies subgroups with subalgebras h ≤ L. Let d_1 = dim π(h) with π: L → V = L/γ_2,
s = h ∩ γ_2 and s_3 = h ∩ γ_3.
1. **d_1 = 2 ⇒ h = L.** γ_3 is spanned by [a,[b,c]], which depends only on a, b, c mod γ_2. So γ_3 ⊆ h. Then
   γ_2 ⊆ [h,h] + γ_3 ⊆ h, and h = L.
2. **d_1 = 0.** h ⊆ γ_2, which is abelian, so every subspace is a subalgebra.
3. **d_1 = 1.** Here π(h) = F_pe. Pick η ∈ h with π(η) = e. Then h = F_pη ⊕ s, and s must be ad_η-invariant. ad_η
   sends Z to [e,Z] = e_0U + e_1W ≠ 0 and kills γ_3. So s is invariant iff s ⊆ γ_3 or [e,Z] ∈ s, and every such s
   occurs.

| # | type | log H | H ∩ γ_3 | count | route (§C) |
|---|---|---|---|---|---|
| 1 | trivial | 0 | 1 | 1 | F23 branch fails to certify → output 1 |
| 2 | central line | F_pq | line | p+1 | AbHSP(γ_2); IS-fil4 fails → output exp(s) |
| 3 | line in γ_2 | F_p(Z+c) | 1 | p² | AbHSP(γ_2) (P1) |
| 4 | γ_3 | γ_3 | γ_3 | 1 | AbHSP(γ_2); IS-heis fails → output |
| 5 | Heisenberg plane in γ_2 | span(Z+c, q) | line | p(p+1) | AbHSP(γ_2) (P3) |
| 6 | γ_2 | γ_2 | γ_3 | 1 | AbHSP(G/γ_2) |
| 7 | **hard cyclic** | F_pη | 1 | p³(p+1) | **Route A (F23′)** |
| 8 | η + generic central line | F_pη + F_pq, q ∦ [e,Z] | line | p³(p+1) | **IS Cor 8 in G/⟨q⟩ ≅ fil4** |
| 9 | η + special line | F_pη + F_p[e,Z] | line | p²(p+1) | AbHSP(M_{g_0}/⟨q⟩) |
| 10 | η + centre | F_pη + γ_3 | γ_3 | p(p+1) | AbHSP(M_{g_0}/γ_3) if g_0 ∥ e, else **IS Cor 8 in G/γ_3 ≅ heis** |
| 11 | η + Heisenberg plane | F_pη + span(Z+c, [e,Z]) | line | p²(p+1) | AbHSP(M_{g_0}/⟨q⟩) |
| 12 | maximal | F_pη + γ_2 | γ_3 | p+1 | AbHSP(G/γ_2) |
| 13 | G | L | γ_3 | 1 | AbHSP(G/γ_2) |

* `classify.py` enumerates every subspace of F_p⁵ and keeps those closed under the bracket.
  * p = 5: 1901 subalgebras.
  * p = 7: 6453 subalgebras.
  * Every type count equals the formula, and there is no other type.
* Here q ∈ γ_3 \ 0, and g_0 = (q_U, q_W) is the unique line of V with [g_0, Z] ∈ F_pq.
* M_{g_0} = exp(F_pg_0 + γ_2) is a normal maximal subgroup, and M_{g_0}/⟨q⟩ is abelian.

**Branch implications** used by the decision procedure (all PROVED from Lemma T; 0 violations over all subalgebras
at p = 5, 7):
* P1: s_3 = 0 and dim s = 1 ⇒ d_1 = 0.
* P2: s = 0 ⇒ H is trivial or hard cyclic.
* P3: s_3 = F_pq. Put T = h ∩ (F_pg_0 + γ_2). If T ⊄ γ_2 then h = T. Otherwise h = s, or s = F_pq and h is type 8.
* P4: s = γ_3 ⇒ h = γ_3, or h is type 10.
* P5: s = γ_2 ⇒ h ⊇ γ_2.
* P6: d_1 = 2 ⇒ h = L.
* P7: in type 11, [e,Z] ∈ s.

### B2. Route A on each type: where it applies and where it fails

* **Type 7 (hard cyclic).** Route A applies, with Theorem F23′, for all p ≥ 5.
* **Types 2, 5, 8, 9, 11 (H ∩ γ_3 = F_pq).** The labels are uniform on the line q^⊥ ⊂ γ_3*. So any two nonzero labels
  are dependent and **no admissible triple exists**: Route A cannot start.
  * Types 9 and 11 have q ∥ [e,Z], so λ·e = 0 for **every** label. Every copy is spoiled (Lemma 0′ applies to each)
    and carries only a delta. Route A would learn nothing even with triples.
  * In type 8, all copies live in the single quotient G/ker λ = G/⟨q⟩ ≅ fil4, where H/⟨q⟩ is cyclic of order p,
    outside the abelian N̄ = M_{g_0}/⟨q⟩ of index p. This is exactly IS Prop 7 / Cor 8. The "adaptation" of Route A
    is IS's own one-quotient merge (pair-measurement report §1). With Lemma-B arities, one equation costs 9g_3 =
    18 or 36 copies, and 3 equations are needed.
* **Types 4, 6, 10, 12, 13 (H ⊇ γ_3).** Every label is 0 and the copies are plain coset states of H ⊇ γ_3, so Route
  A's front end is undefined.
  * G/γ_3 = heis is H-independent.
  * Type 10 becomes a cyclic subgroup of order p in heis (IS Cor 8, class 2). The other types become abelian HSPs.
* **Types 1, 3 (H ≤ γ_2, H ∩ γ_3 = 1).** The labels are uniform, but e = 0. So η ∈ log N_λ for every λ, every copy is
  a delta (the Lemma 0′ mechanism), and Route A carries no information.
  * Type 3 is found directly by abelian HSP on γ_2.
  * Type 1 is the default output when the F23 branch certifies nothing.

**Theorem R / SOT(Aut) consistency, per type.** Theorem R (11-12 note §5) concerns a *uniformly random hard cyclic*
H in a class-3 group with (Z).
* **Type 7.** Route A is outside SOT(Aut), through the QFT over the non-central N_λ (exit (ii)), as the referees
  found.
* **Type-detection step.** AbHSP on γ_2 is an (O5) restriction to M = γ_2 ⊇ γ_3 followed by (O6). For hard cyclic H,
  H ∩ γ_2 = 1, so the register is *dead*: its outcomes are uniform. This matches step 5 of Theorem R's proof, which
  charges a restriction only when K̄ ⊆ M/γ_3, impossible here. So the detection step is consistent with, and costs
  nothing in, Theorem R.
* **Type 8.** In G, H is not hard cyclic, so Theorem R does not apply. In fil4 = G/⟨q⟩, H/⟨q⟩ is hard cyclic, and
  the note's own calibration says that fil4 is solved outside SOT by IS Cor 8. Consistent.
* **Type 10.** It is handled in heis, which has class 2, so Theorem R (class 3) does not apply.
* **Abelian types 2–6, 9, 11–13.** These are SOT operations: (O4) promotion by central subgroups contained in H, (O5)
  and (O6). Theorem R makes no claim about these H.
* **No conflict anywhere.**

### B3. H-dependence and the frozen-normalizer check

Every subgroup the algorithm touches, and how it is used:

| object | depends on H? | normal in G? | use |
|---|---|---|---|
| γ_2, γ_3 | no | yes | restriction (AbHSP); quotient only after certifying γ_k ⊆ H (branches s ⊇ γ_k) |
| ⟨q⟩ = H ∩ γ_3 (line) | yes, computed by AbHSP(γ_2), certified ⊆ H by queries | yes (central) | quotient G/⟨q⟩ (types 8, 9, 11) |
| M_{g_0} | through q (computed) | yes (contains [G,G]) | restriction only |
| N̄ = M_{g_0}/⟨q⟩, b = exp(x′) | through q | yes in G/⟨q⟩ | IS chart and Fourier transform |
| ker λ | through the measured label | yes (central) | F23 promotion (unchanged) |
| K̂ = exp(F_pη̂_V)γ_3 | yes (after ε is learnt) | **no** | left cosets in the η_c step only, as in the referee's fix 2; no quotient |

* **The quotient by ⟨q⟩ is legitimate.** ⟨q⟩ is central and ⟨q⟩ ≤ H. So f is constant on the cosets g⟨q⟩, and
  f̄(g⟨q⟩) := f(any lift) is a hiding function for H/⟨q⟩ on the *group* G/⟨q⟩.
* **For every nonzero label, G/⟨q⟩ = G/ker λ.** So this is precisely F23's label promotion.
* **What the old drafts did wrong.** The CLASS_THREE draft formed G/K for non-normal K (its own warning, l. 121) and
  used normalizer reductions. Neither occurs here.
* **No step uses N_G(H)**, and no step uses an automorphism built from H.

## C. Theorem HSP23 and its proof

**Theorem HSP23 (PROVED given cited theorems; AI-checked, pending human review).**

*Hypotheses.* Let p ≥ 5 be prime and G = free23 over F_p, with Lie coordinates and BCH. Let f be an oracle hiding an
**arbitrary** subgroup H ≤ G.

*Conclusion.* Algorithm HSP23 below outputs a Lie basis of log H.
* Every output it **certifies** is correct.
* An uncertified default output is wrong with probability at most (1 − s(p))^R when H is hard cyclic, and at most
  ε_IS when H is of type 8 or 10. It is never wrong otherwise.
* It uses no cover, poly(log p) time, O(R·m) quantum queries in the hard-cyclic branch, and O(1) otherwise. The
  constants are in the table below.

**Algorithm HSP23.**
1. **AbHSP on γ_2 ≅ F_p³.** Fourier-sample f|_{γ_2}. Samples lie in s^⊥ always, so their null space ŝ ⊇ s. Certify
   ŝ ⊆ s by classical queries f(exp v) = f(1) on a basis, and resample until this passes (Las Vegas). Put
   s_3 = s ∩ γ_3.
2. **s_3 = 0.**
   * If dim s = 1, output s (P1).
   * Otherwise run R attempts of Route A (Theorem F23′) with fresh labelled copies made from f. Output the first
     candidate η̂ with f(exp η̂) = f(1). If none passes, output 0 (P2).
3. **s_3 = F_pq.** Put g_0 = (q_U, q_W) and run AbHSP on M_{g_0}/⟨q⟩ (abelian, with ⟨q⟩ ⊆ H), giving T.
   * If T ⊄ γ_2, output T.
   * Else, if dim s = 2, output s.
   * Else run IS Cor 8 in G/⟨q⟩ with N̄ = M_{g_0}/⟨q⟩ and b = exp(x′). The target H̄ has order p and is not in N̄, by
     P3. If a candidate ĥ passes f(ĥ) = f(1), output span(log ĥ, q); otherwise output s (P3).
4. **s_3 = γ_3.**
   * If s = γ_2, run AbHSP on G/γ_2 and output the result (P5, P6).
   * Otherwise choose a public random g_0 and run AbHSP on M_{g_0}/γ_3, giving T. If T ⊄ γ_2, output T.
   * Otherwise run IS Cor 8 in heis = G/γ_3, certify, and output span(log ĥ, γ_3), or γ_3 if nothing passes (P4).

*Proof.*
* **Correctness of the branches.** It follows from Lemma T and P1–P7.
* **The abelian steps are exact.** For an ideal C ⊆ h and a subalgebra a with [a,a] ⊆ C, BCH gives
  exp(t)exp(t′−t) = exp(t′)·c with c ∈ exp(C) ⊆ H. So t ↦ f(exp t) on a/C hides (h ∩ a)/C.
* **The IS steps are IS Prop 7 + Thm 5 + Thm 3** (local text `2026-11-02-rees-linear-arity/lit/is_1503.09016.txt`,
  read). Their input is the random level-set states Σ_x|x⟩|u + v(x)⟩, which are our chart coset states, since every
  coset of H̄ is uH̄ with u ∈ N̄ and u·h̄^x = (u + Σ_{i<x}B^in_0)·b^x. In the needed case B is unipotent with
  (B − I)³ = 0, so B^p = I for p ≥ 5.
* **The hard-cyclic step is Theorem F23′.**
* **One-sided error.** Every output is either certified, hence ⊆ H and of the right dimension by Lemma T, or a
  default justified by P1–P4 unless a sub-algorithm failed.
* **Time.** Every step uses poly(log p) field operations, QFT_p's and Las Vegas roots. ∎

**Queries** (expected; quantum = coset states, classical = membership queries):

| branch | quantum | classical | source |
|---|---|---|---|
| AbHSP on F_p^k | ≤ k + 1 per call | ≤ k per certification attempt | standard; Σ_j 1/(1 − p^{−j}) ≤ k + 0.32 |
| Route A (type 7) | R·(18m/q_adm + 2 + O(1/p)); m ∈ {36, 144} | 1 per candidate | F23′ |
| IS fil4 (type 8) | O(1) (IS Thm 5; constant not extracted). Our implementation: 18 or 36 per equation, 3 equations | 1 | cited |
| IS heis (type 10) | O(1) (IS). Our implementation: 3 per equation, 2 equations | 1 | cited |

**Explicit constants not proved here.** I did not prove an independence bound for the IS equations in our
implementation. It collects equations until they have full rank, at most 4m of them, and then certifies. So the IS
copy counts above are per equation, and the number of equations needed is empirical (§D). The polynomial bound is
IS's.

## D. End-to-end simulations (falsification only)

**Route A, unconditioned** (`e2e_spoiled_5.out`, `e2e_spoiled_7.out`):

| p (m) | attempts | success | wrong output | equations correct | spoiled runs checked (line / phase fails) | D_l = 0: clean / spoiled / all-spoiled |
|---|---|---|---|---|---|---|
| 5 (36) | 150 | 82 (bound 0.128) | 0 | 247/247 | 227 (0 / 0) | 59/325, 99/575, 66/349 |
| 7 (144) | 40 | 23 (bound 0.280) | 0 | 67/67 | 59 (0 / 0) | 19/126, 18/114, 11/81 (1/p = 0.143) |

**The whole algorithm, every type** (`hsp_all.py`, outputs `hsp_all_{7,11,13}.out`):
* f is an explicit table on G, coset states are made from f, and membership is decided by classical queries.
* The truth is used only for diagnostics, and inside the referee's Route-A simulator, which builds the same coset
  states directly.
* In the IS branch, every front-end state was asserted equal to the public phase forms, and every equation was
  checked against the truth.

Results (`hsp_all_table.out`, built by `make_table.py`). Each cell is correct/instances, with the mean number of
quantum queries (coset states) in brackets:

| type | branch | p = 7: correct/n (mean quantum) | p = 11 | p = 13 |
|---|---|---|---|---|
| trivial | F23 | 4/4 (4) | 4/4 (3) | 3/3 (3) |
| central line | IS fil4 | 4/4 (110) | 4/4 (57) | 3/3 (137) |
| line Z+c | gamma2 line (P1) | 4/4 (2) | 4/4 (2) | 3/3 (2) |
| gamma3 | IS heis | 4/4 (14) | 4/4 (9) | 3/3 (10) |
| plane Z+c,q | plane (P3) | 4/4 (4) | 4/4 (3) | 3/3 (3) |
| gamma2 | AbHSP on G/gamma2 | 4/4 (3) | 4/4 (3) | 3/3 (3) |
| hard cyclic | F23 | 4/4 (5327) | 4/4 (855) | 3/3 (4391) |
| (b) generic | IS fil4 | 4/4 (138) | 4/4 (58) | 3/3 (106) |
| (b) special | AbHSP on M_g0/<q> | 4/4 (4) | 4/4 (4) | 3/3 (4) |
| (c) | IS heis | 4/4 (12) | 4/4 (8) | 2/2 (8) |
| (d) | AbHSP on M_g0/<q> | 4/4 (3) | 4/4 (2) | 3/3 (2) |
| (e) | AbHSP on G/gamma2 | 4/4 (2) | 4/4 (2) | 3/3 (2) |
| G | AbHSP on G/gamma2 | 4/4 (2) | 4/4 (2) | 3/3 (2) |
| (c) | AbHSP on M_g0/gamma3 | - | - | 1/1 (2) |

* **0 wrong outputs** in 143 instances (52 + 52 + 39), covering all 13 types at each of p = 7, 11, 13.
* **0 diagnostic failures:** is_frontend_fail = is_eq_wrong = f23_eq_wrong = C0_closed_form_fail = 0.
* **Route A** needed 1 attempt in 9 hard-cyclic instances and 2 attempts in 2.
* **IS equations.** The IS branches needed 2–6 equations before reaching full rank.
* **Type 10 at p = 13.** One instance had the public g_0 ∥ e, so it went to the abelian branch.
* **Uncertified defaults.** The rows "central line" and "gamma3" are instances where the IS branch, correctly,
  certifies nothing and the default output exp(s) is right. "trivial" is the F23-branch default; that pipeline is
  not simulated (self-check).
* **Peak RSS** was below 0.3 GB.

## E. The free 3-generator class-3 group: what breaks (PROVED by hand)

Let L_3 be free on x_1, x_2, x_3 of class 3, with dim = 3 + 3 + 8. Take a label λ ≠ 0 on γ_3 (dim 8) and put
L̄ = L_3/ker λ.

**Claim.** L̄ has no abelian ideal of codimension 1.
* Such an ideal A contains [L̄, L̄], so A = W + γ̄_2 with W ⊂ V of dimension 2.
* For a basis w_1, w_2 of W, [w_1, w_2] is a nonzero element of γ_2 \ γ_3. It is not in ker λ ⊆ γ_3, so A is not
  abelian.

**Consequence.**
* G/ker λ is not of the form F_p ⋉ F_p^m. The IS front end (Prop 7), Lemma 0 and Lemma 0′ have no analogue.
* The largest abelian normal subgroup that works for all λ is γ̄_2, of index p³. It leaves a 3-variable phase, which
  is outside IS Thm 5 (HPGP′ with one variable).
* Separately, Route A's level-1 relation would need ≥ 9 copies, since dim γ_3 = 8, and the P_2 and P_3 conditions
  become 8-dimensional each. Lemma B still gives a polynomial arity, of size g^8.
* Whether a multivariate aligned merge exists is **UNKNOWN**. The cover handles this group.
* No computation was done for (E).

## Claim gates and next question

**Gates.** These stay false: "cover unnecessary for free23", novelty, priority and speedup. Theorem HSP23 would
justify, after human review, replacing the core's DRAFT remark "It covers only this promise, not arbitrary H. We do
not know whether it extends to other subgroups of G" with a statement for all H. Not done here.

**Strongest counterexample or baseline.** For every non-hard-cyclic type, the route is known or standard (abelian HSP,
IS Cor 8). The only non-standard ingredient of HSP23 is Route A for hard cyclic H. So the claim "HSP in free23 without
the cover" reduces exactly to Theorem F23′.

**Next hard question.** Does an aligned merge exist when N_λ is non-abelian, starting from the free33 front end
(§E)? It is equivalent to a multivariate HPGP′ with cross-quotient labels.
* Next command: a free33 analogue of `structure_check.py` with the 3-variable chart over γ̄_2.
* Acceptance test: a public level-2 condition set that is again a power-sum system in the labels.

## Adversarial self-check

* **Is Lemma S circular?** It uses the polynomial identity Δ_tot ≡ μτ in θ. I did not re-derive Lemma E from scratch.
  I checked that its proof steps are identities ((S), (W), (E3) and the conic, all stated "for all e" with no
  division by f(e)). A gap there would also break F23 itself. The exact support-line and phase checks (§D) would
  catch a failure on the tested instances.
* **Lemma C′ coupling.** It treats a_j = u_jb_j as independent draws. That is the law of the coset outcome because
  the triples' states are a product. If the code reported b_j instead of differences, it would make no difference,
  since D uses (E3).
* **The i* = 1 case** needs κ ≠ s_1². I proved it, but it is easy to get wrong. The all-spoiled D_l = 0 rate
  (66/349 at p = 5) is consistent with 1/p.
* **s(p) at p = 5 is 0.128**, a weak but positive constant. The observed rate is 0.55, so the bound is loose.
* **The IS branches rest on a citation.** My implementation is a falsification check, not the proof. Its
  equation-independence rate is empirical. IS Theorem 5 is stated as a sketch in the source ("Proof of Theorem 5
  (sketch)"). I read Prop 7 and the Thm 5 sketch locally, not the full Thm 3 proof.
* **Oracle versus copies.** HSP23 uses the standard oracle: restrictions, quotient lifts and classical membership
  queries. F23′ alone works from labelled copies. HSP23 is not claimed in the copies-only model.
* **Default outputs.** For H trivial, the Route-A pipeline was **not simulated**, because the referee's simulator
  needs a hard η. The output 1 follows from certification failing deterministically (f(ĥ) ≠ f(1) for every ĥ ≠ 1).
* **The type-detection step is Las Vegas only for s.** It certifies ŝ ⊆ s, and ŝ ⊇ s holds always. A wrong default
  can arise only in the F23 and IS branches.
* **Small primes only.** The simulations are at p ≤ 13. Nothing was simulated at large p.
* **Cited from memory:** approximate QFT and the hybrid argument, Tonelli–Shanks and Adleman–Manders–Miller, and the
  Lazard correspondence for subgroups.
* **Not done:**
  * a GAP cross-check of the subgroup count, which is done here only through subalgebra enumeration;
  * free33 computations;
  * exact gate counts;
  * a literature search beyond the local IS text (no network).

## Reproduce (folder; python = /opt/anaconda3/bin/python, all under nice -n 19)

```
python classify.py 5 > classify_5.out; python classify.py 7 > classify_7.out          # 4 s, 20 s
python spoiled.py 5 8 11 > spoiled.out; python spoiled.py 7 6 12 >> spoiled.out         # ~1 min
./queue_spoiled.sh     # e2e_spoiled.py 5 150 501 (3 min), 7 40 502 (~5 min)  -> e2e_spoiled_{5,7}.out
./queue_all.sh         # hsp_all.py 7 4 707, 11 4 1111, 13 3 1313 -> hsp_all_{7,11,13}.out   (~25 min, < 0.3 GB RSS)
python make_table.py > hsp_all_table.out
```

Acceptance:
* classify: all OK, and every violation count is 0;
* spoiled: every SUMMARY count is 0;
* e2e_spoiled: wrong_output = 0, run_holds = run_ok, line_fail = phase_fail = full_support_fail = 0;
* hsp_all: WRONG 0 in every SUMMARY row, and is_frontend_fail = is_eq_wrong = f23_eq_wrong = 0.
