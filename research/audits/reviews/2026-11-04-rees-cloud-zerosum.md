# Rees HSP cloud research session: zerosum

- Session: `session_01B1JoChaW8s7QvRQso9tgez` (Claude Code cloud session)
- Started: 2026-11-04T01:56Z; final result event: 2026-11-04T04:38Z
- Task: Fast (polynomial-time, near-linear-arity) zero-sum subset finder over F_p^g for the kappa = p-1 grade node.
- Harvested 2026-11-05 from the session's single `result` event via the claude.ai events API.
  Body below is verbatim (SHA-256 of body: `4397bcbbd627a62a2569949f181bff548fe03e1292348ef2c541b4352a97b4a5`, 47804 chars).
- Status: AI-generated, AI-checked only, pending human review. All Rees claim gates stay false.
- Comparison with the paper: `2026-11-04-rees-cloud-research-harvest.md`.

---

I don't have a polynomial-time algorithm at M = O(g) or O(g log g), and I couldn't get a degree in g that stays fixed as p grows. What I do have is polynomial time at M = O(g²) for p = 3 and M = O(g⁴) for p = 5, 7, both proved, plus working code. All 1800 trials succeeded. Nothing was committed or pushed.

Most of the useful prior art is a 2025 paper you weren't pointed to: Kothari–O'Donnell–Wu, arXiv:2510.07515 ("KOW" below). It treats exactly this problem and already gives polynomial time at about n⁴ for uniform inputs when p = 5, 7. My contribution beyond it is a cleaner variant with an explicit proof and smaller constants. The full report follows, ready to paste into research/audits/reviews/2026-11-04-rees-cloud-zero-sum.md.

---

# Rees HSP, cloud pass: polynomial-time zero-sum node at κ = p−1 (2026-11-04)

Status: AI-checked, pending human review. Nothing was committed or pushed.

## 0. Summary

* **Prior art.**
  * Kothari–O'Donnell–Wu, arXiv:2510.07515 (v3, Mar 2026) [KOW], studies this problem under the name "F_q^n-Subset-Sum", in the worst case and on average.
    * Average case (Thm 1.9/4.12): polynomial time at arity C_q·n^{2⌊(q+3)/4⌋}·log(1/ε). That is n⁴ for q = 5, 7, n⁶ for q = 11 and n⁸ for q = 13.
    * q = 3, worst case (Thm 1.2): n²/3 + Cn log n.
  * Imran–Ivanyos, arXiv:2304.08376 [II]: worst case at n^{O(p log p)}. They ask for poly(np) time at arity (np)^{O(1)}.
* **(B) Uniform vectors on an unknown subspace U, with dim U = a ≤ g.**
  * p = 3: worst case, deterministic, arity (a+1)(a+2)/2 [proved; known from ISS07/KOW]. Measured arity ≈ 0.29·a², 100/100 at every g up to 80.
  * p ∈ {5, 7}: a new nested variant of KOW (§4).
    * Proved (Theorem B): arity ≤ about 2.2·a⁴ + O(a·log(1/τ) + g), failure probability ≤ τ, time poly(g, log 1/τ).
    * Measured arity: about 0.08–0.09·a⁴ at g = 80.
    * Compared with KOW, it drops the log q·log(1/ε) factor: the (0,1,2)-objects come from a deterministic "±1-spanning gadget" rather than from d random batches. The objects are also built in the quotient by the top-level span.
  * A degree in g that does not depend on p is **not achieved**. It is stated as an open problem in [II §6] and [KOW §5.1].
* **(B) at M = O(g) or O(g log g):** no polynomial algorithm is known for any p ≥ 3.
  * For p = 3, KOW explicitly ask whether o(n²) is possible.
  * The average-case problem at m ≈ 2n is the hardness assumption behind the Wave signature scheme, which is believed to need 2^{Ω(n)} time.
  * The best known trade-off below quadratic arity is BKW/Wagner at exp(O(n/log(m/n))), which is not polynomial (§6).
* **(A) Worst case.**
  * p = 3: degree 2.
  * p ≥ 5: the best known is II's n^{(1/4)q̄ log₂ q̄}, where q̄ is p rounded up to a power of 2 (KOW Thm 1.8). That is n⁶ for p = 5, 7 and n¹⁶ for p = 11, 13.
  * A degree independent of p is open.
  * **II's claimed worst-case-to-average reduction (§6 of arXiv:2304.08376) looks flawed:** the second-stage inputs are not uniform (§5). So (A) and (B) are not known to be polynomially equivalent.
  * I sketch a worst-case n⁴ route for p = 5 and show exactly where it breaks (§5) [argued, gap].
* **For the paper.** A drop-in lemma (§8) replaces the p^{O(g)} search at κ = p−1.
  * Time becomes poly(g).
  * Arity becomes O(a²) for p = 3, O(a⁴) for p = 5, 7, and KOW's O(a^{2⌊(p+3)/4⌋}) for p ≥ 11.
  * This is a real trade: many more samples in exchange for polynomial time.

## 1. Literature (checked against the PDFs)

| Ref | Statement used |
|---|---|
| Olson 1969; van Emde Boas 1969 | D(C_p^n) = n(p−1)+1. Existence only. |
| Ivanyos–Santha, TCS 657 (2017), arXiv:1503.09016 [IS] | Thm 3: SDE(F_q,n,m,d) is solvable in polynomial time when n > d^{d log d}(m+1)^{d log d}. Prop. 9: d = 2 at (m+1)². The zero-sum case is d = p−1. |
| Ivanyos–Sanselme–Santha, nil-2 HSP, 2007/08 [ISS07] | Claim 1 gives worst-case F_3 subset-sum at (n+1)(n+2)/2 (as quoted in KOW). |
| Imran–Ivanyos, arXiv:2304.08376 [II] | Lemma 3 ("halving"). Prop. 4: ±1 zero-sums at p^{O(p log p)}·n^{O(p)}. Prop. 5: doubling collisions. Thm 2: subset zero-sum at p^{O(p² log p)}·n^{O(p log p)}, deterministic, worst case. §6: open question and a claimed worst→average reduction (see §5). |
| Kothari–O'Donnell–Wu, arXiv:2510.07515 [KOW] | Thm 1.2: F_3 worst case at n²/3 + Cn log n. Lemma 3.3: reducible vectors. Thm 3.7: ±⌊q/4⌋-zero-sums in the worst case at about (1−1/q)·n²/2. Lemma 3.10: (0,1,2) → (0,1). Lemma 3.11: random shift → (0,1,2). Thm 3.12/4.12: average-case subset-sum at n^{⌈⌈q/2⌉⌉}. §5.1: open questions. §5.6: Wave; BKW at exp(O(n/log(m/n))). |
| Göös–Kamath–Sotiraki–Zampetakis, CCC 2020, arXiv:1912.04467 | For m > (p−1)n the search problem is in PPA_p, and Chevalley_p is PPA_p-complete. So finding a solution at the Davenport threshold is unlikely to be in P. |
| Hashimoto, arXiv:1507.03674 | Underdefined MQ in odd characteristic still costs 2^m. Its bottleneck is a diagonal system Σ a x² = b, which for p = 3 is exactly this problem. |
| Alon–Linial–Meshulam, JCTA 57 (1991) | O(p log n) bases form an additive basis. The proof is not constructive, and I found no algorithmic version. |

## 2. Setting, and the unknown subspace

The input is a stream λ₁, λ₂, … of i.i.d. uniform vectors of an unknown subspace U ≤ F_p^g with dim U = a. The goal is a nonempty T with Σ_{i∈T} λ_i = 0.

**Lemma S (span estimation) [proved].**
* Read g+s vectors and let U′ be their span.
* Then Pr[U′ ≠ U] ≤ #{hyperplanes of U}·p^{−(g+s)} ≤ p^{a−g−s} ≤ p^{−s}.
* If U′ = U, then in the RREF basis of U′ the coordinates of every later sample are i.i.d. uniform on F_p^a.
* Every later vector is checked for membership in U′, so a wrong estimate is detected and never used silently. □

From here on, work in F_p^a.

## 3. p = 3 (worst case)

**Theorem A [proved; ISS07 Claim 1, KOW Thm 2.2].** Any (a+1)(a+2)/2 vectors of F_3^g whose span has dimension a contain a zero-sum subset, and a deterministic polynomial-time algorithm finds one.

*Proof.* Use levels (Lemma L in §4) with coefficients in {0,1}.
1. At a level whose current dimension is ℓ, take the first linear dependency among at most ℓ+1 projected vectors. Write it as Σ_{J₁} x − Σ_{J₂} x = 0, where J_c = {i : α_i = c} and 2 = −1 in F_3.
2. If J₁ or J₂ is empty, the other is a 0/1 zero-sum at this level.
3. Otherwise let u = Σ_{J₁} x = Σ_{J₂} x. If u = 0, the set J₁ is a zero-sum.
4. If u ≠ 0, then 0·u, 1·u and 2·u = −u are realized by ∅, J₁ and J₁ ∪ J₂. These are the {0,1}-representatives of u. Make u a new level.
5. Each level lowers the dimension by 1 and uses at most ℓ+1 vectors. At dimension 0 the next vector projects to 0.

A solution found at any level lifts to a 0/1 zero-sum by Lemma L. The total count is Σ_{ℓ=1}^{a}(ℓ+1) + 1 = (a+1)(a+2)/2. □

The code uses KOW's sparse-relation variant: it takes r = ⌈log₃(ℓ+1)⌉ extra vectors and picks the minimum-support relation among the 3^r combinations. Worst-case checks are in adversarial_p3.py. One case is the Davenport-extremal input "each e_i twice, plus one more vector", which is solved with the minimum possible 2g+1 = 41 vectors.

## 4. p ∈ {5, 7}: the nested algorithm (main new content)

Write F = F_q with q ∈ {5,7}, and h = (q−1)/2. Field elements are represented in [−h, h].

**Lemma L (levels and lifting) [proved].**

*Setup.* A level sequence consists of:
* vectors u₁, …, u_L;
* pivots π_j with u_j[π_j] ≠ 0;
* maps P_j(y) = y − (y[π_j]/u_j[π_j])·u_j and Q_j = P_j∘⋯∘P₁, with Q_{j−1}u_j = u_j;
* pairwise disjoint blocks T_j of items, where each item x has a value val(x, c) for c in a coefficient set C ∋ ±1.

For every c ∈ F we require a representative ρ_j(c) ∈ C^{T_j} with Q_{j−1}(Σ_{x∈T_j} val(x, ρ_j(c)_x)) = c·u_j.

*Assumption (★).* For every item x used at level j or later, Q_{j−1}val(x,c) = c·Q_{j−1}val(x,1).

*Claim.* Let y satisfy Q_L(y) = 0. Set r := y. For j = L, …, 1: let c := (Q_{j−1}r)[π_j]/u_j[π_j], add ρ_j(c), and subtract the value added from r. This finds choices from the blocks with Σ val = y.

*Proof.*
1. y − Q_j y ∈ span(u₁..u_j), and Q_j u_i = 0 for i ≤ j.
2. Invariant: before step j, r ∈ span(u₁..u_j). Then Q_{j−1}r = c·u_j.
3. By (★) and the defining property of ρ_j, the added value is c·u_j plus an element of span(u₁..u_{j−1}). So after step j, r ∈ span(u₁..u_{j−1}).
4. At the end r = 0. Blocks are disjoint, so the choices never collide. □

Implementation: c = (r·M_{j−1}[:,π_j])·u_j[π_j]^{−1}, using the stored column of the composite projection M_{j−1}. Lifting costs O(n) per level.

**Lemma R (reducible vectors from a circuit) [proved; KOW Lemma 3.3 plus a collision case].** Let x_i, i ∈ S, be a circuit (a minimal dependent family) with relation α ∈ [−h,h]^S, which is unique up to a scalar.

(a) Suppose the nonzero |α_i| are not all equal. Put u := Σ_{|α_i|≥2} sgn(α_i)·x_i. Then u ≠ 0, and every c·u with c ∈ F is a ±1-combination of the x_i:
* c = 1: coefficients sgn(α_i) on {|α_i| ≥ 2};
* 2 ≤ c ≤ h: coefficients c−α_i if α_i ≥ 2, −α_i if |α_i| ≤ 1, and −c−α_i if α_i ≤ −2;
* −c: negate the coefficients for c.

(b) Suppose α ∝ σ ∈ {±1}^S, q = 5, and σ takes both signs. Then z := Σ_{σ=+1} x_i ≠ 0, and ±z and ±2z are realized by ±S₊ and ±S.

*Proof.*
* (a), coefficients: these are KOW's identities. c·u − Σ α_i x_i equals the stated sum, and every coefficient lies in [−1,1] because h−1 ≤ 1. Since h ≤ 3, every c ∈ F lies in [−h,h].
* (a), u ≠ 0: u is a ±1-combination supported on a subset of the circuit. If that subset is proper, its vectors are independent, so u ≠ 0. If it is all of S, then u = 0 would make sgn(α) a relation. Then sgn(α) ∝ α, and all |α_i| would be equal.
* (b): S₊ is a proper nonempty subset, so z ≠ 0. Also Σ_{S₋} x = z, so Σ_S x = 2z. For q = 5, F = {0, ±1, ±2}. □

"Degenerate" means neither (a) nor (b) applies. For q = 7 that is any circuit with all |α_i| equal. For q = 5 it is a circuit with all α_i equal.

**Lemma D (non-degeneracy) [proved; Monte Carlo check in check_rho.py].** Take i ≥ 1 and i+1 i.i.d. uniform vectors of F^i. The event "the first i form a basis and the circuit through the last one is non-degenerate" has probability at least ρ_q:
* ρ₅ := ∏_{k≥1}(1−5^{−k})·(1−2/5) ≥ 0.456;
* ρ₇ := ∏_{k≥1}(1−7^{−k})·(1−3/7) ≥ 0.478.

*Proof.* Given a basis, the coordinates c of the last vector are uniform in F^i, and the relation is (1; −c). It is degenerate exactly when:
* q = 7: every nonzero c_b ∈ {±1}, probability (3/7)^i ≤ 3/7;
* q = 5: every c_b ∈ {0, −1}, probability (2/5)^i ≤ 2/5. □

Measured success probability:

| i | 1 | 2 | 3 | 5 | 10 |
|---|---|---|---|---|---|
| q = 5 | 0.47 | 0.64 | 0.72 | 0.75 | 0.77 |
| q = 7 | 0.48 | 0.70 | 0.77 | 0.82 | 0.83 |

**Lemma G (±1-spanning gadget) [proved].** Let S be a space of known dimension ℓ with i.i.d. uniform samples given in coordinates.
* Repeat attempts. At current dimension i, draw i+1 fresh vectors and project them.
* If Lemma D's event holds, turn the circuit into a level using Lemma R. Otherwise discard the attempt.
* After ℓ successful attempts, the blocks B form a ±1-spanning gadget: every t ∈ S is a ±1-combination of B (Lemma L with y = t, since Q_ℓ = 0 on S).
* Attempts are independent, and each succeeds with probability ≥ ρ_q, because fresh vectors project to uniform vectors of the current space whatever the history. □

**Lemma O ((0,1,2)-objects, no randomness needed) [proved].** Let B be a ±1-spanning gadget of S and let w₀ ∉ B be one more vector.
* Put t := −(Σ_B w + w₀) and let α be a ±1-representation of t on B.
* Define κ := 1+α on B and κ(w₀) := 1.
* Then Σ κ_i w_i = 0, with κ ∈ {0,1,2}^{B∪{w₀}} and κ(w₀) = 1. □

This replaces KOW Lemma 3.11, which needs d = log(q/ε) random batches and a subset-sum DP over F_q.

**Algorithm N (nested).**
* **Top.** A worst-case ±1 solver runs on items. It uses Lemma L with KOW Lemma 3.3, and any ±1 relation counts as a solution.
* **Item k.** Suppose the top has j−1 levels when item k is created, with top span Z_j = span(z₁..z_{j−1}).
  * Take fresh vectors v and project them by Q^{top}_{j−1}.
  * Build a gadget of S = Q^{top}_{j−1}(U), which has dimension a−j+1, and apply Lemma O.
  * This gives J₁(k) ∋ v₀ (coefficient 1) and J₂(k) (coefficient 2).
  * With u_k = Σ_{J₁} v and u′_k = Σ_{J₂} v (actual vectors of U), we have u_k + 2u′_k =: ζ_k ∈ Z_j.
* **Values.** val(k,+1) := u′_k and val(k,−1) := u_k + u′_k = −u′_k + ζ_k. They are realized by the 0/1 sets J₂(k) and J₁(k) ∪ J₂(k).
* **Early stop.** If J₂(k) = ∅, then u_k ∈ Z_j. Lift the 0/1 set J₁(k) through the top levels (Lemma L with base −u_k) and stop.

**Theorem B [proved].** Let p ∈ {5,7} and consider Algorithm N in its fresh-vector variant. Define

  M_p(a,g,τ) = g + ⌈log_p(2/τ)⌉ + (a+1)(a+4)/2 + ⌈(a+1)·(a(a+1)(a+4) + 8 ln(2/τ))/ρ_p⌉ ≈ 2.2·a⁴.

With probability ≥ 1−τ the algorithm reads at most M_p samples and outputs a nonempty T with Σ_T λ_i = 0. Every output is checked, so it is always correct. Time is poly(g, M_p) = poly(g, log 1/τ).

*Proof.*
1. **Correctness.**
   * (★) holds at the top: item k is used only at top levels j ≥ j(k), and ζ_k ∈ Z_{j(k)} ⊆ span(z₁..z_{j−1}), so Q_{j−1}ζ_k = 0.
   * The solver ends with a ±1 combination F of items with Q_L(Σ_F sgn·u′) = 0. Hence Q_L(Σ_F val) = 0 as well.
   * Lemma L lifts this to item choices with Σ val = 0 exactly.
   * Replace each (k,+1) by J₂(k) and each (k,−1) by J₁(k) ∪ J₂(k). The result is a disjoint union of 0/1 sets with sum 0.
   * It is nonempty: J₂ ≠ ∅ for +1 choices, and v₀ ∈ J₁ for −1 choices. The early-stop case is identical, with base u_k.
2. **Item count.**
   * At top dimension ℓ, a relation among ℓ+1 items always exists.
   * It gives either a new level (Lemma 3.3; if u = 0, the |α| ≥ 2 part is a ±1 zero-sum) or a solution.
   * So there are at most a top levels, and at most Σ_{ℓ=1}^{a}(ℓ+1) + 1 ≤ (a+1)(a+4)/2 =: I_a items.
3. **Sample count.**
   * Each item needs at most a successful attempts (Lemma G), each costing at most a+1 vectors, plus one v₀. So at most n_s = a·I_a successes are needed in total.
   * By Chernoff, K₀ = (2n_s + 8 ln(2/τ))/ρ attempts yield ≥ n_s successes, except with probability e^{−(2n_s+8 ln(2/τ))/8} ≤ τ/2.
   * Lemma S with s = ⌈log_p(2/τ)⌉ accounts for the other τ/2.
4. **Time.**
   * Each attempt costs O(a³).
   * Projecting each vector with the composite matrix costs O(a²).
   * Lifting costs O(a) per level plus O(|rep|·a). □

The experiments use the practical variant. Vectors that a block leaves unused are recycled within and across gadgets, and relations are sparse with r = 2. This changes only the arity, never correctness, which is deterministic and checked. Table rows with recycling off are included.

**Why the degree is 4 and not 2.**
* The ±1 layer has degree 2: each of about a levels needs about a vectors of linear algebra.
* Turning ±1 into 0/1 needs a second ±1 layer over objects, and each object costs a full ±1 gadget.
* I found no way to share one gadget among several objects, because Lemma O consumes all of B with coefficient 1+α. Degree 3 would have to come from there.

## 5. Worst case (A): status, a flaw in II's reduction, and a near-miss

**II §6 reduction looks flawed [argued, pending human check].**
* II add uniform r_i to the worst-case x_i, run the average-case solver A on groups, then run A again on y_k = Σ_{T_k} r_i.
* But Σ_{T_k}(x_i + r_i) = 0, so y_k = −Σ_{T_k} x_i. This is a subset sum of the adversarial x's, over a set T_k that is independent of the x's. It is not uniform: if x_i ≡ e, every y_k lies on ⟨e⟩.
* The claimed success probability δ in stage 2 is therefore unjustified.
* KOW treat worst-case n^{O(q)} as open, which is consistent with this.

**Near-miss for p = 5 [argued, gap].**
* By Lemma R(b), for q = 5 a degenerate circuit is either a usable collision or an all-equal circuit.
* In the worst case, a pool with more than 2ℓ nonzero projections always contains a non-uniform circuit or a mixed-sign collision. (If every fundamental circuit is uniform, then x = −Σ_{S_x} b with the S_x pairwise disjoint.)
* Lemma O and Lemma 3.10 already work in the worst case. So worst-case subset-sum at O(n⁴) for p = 5 would follow from one more statement: from poly(n) arbitrary vectors, one can build a ±1-gadget B with span(B) ⊆ span(levels), plus one extra vector in that span.
* The gap:
  * A circuit block contributes |T_j|−1 dimensions, and its own level absorbs only one of them.
  * An adversary can stop later levels from absorbing the rest. Example: e₁, e₂, e₁+2e₂, followed only by vectors of ⟨e₂⟩.
  * The target t = −Σ_{B′} v then lies outside span(levels).
* I did not close this gap.

## 6. Negative statements (where I failed)

1. **No poly(g) algorithm at M = O(g) or O(g log g)** for any p ≥ 3, even for uniform inputs. I have neither an algorithm nor a lower bound. Evidence of hardness:
   * Wave rests on average-case F_3 (±1 ≡ 0/1) at m ≈ 2n, with 2^{Ω(n)} cryptanalysis [BCDL19, quoted in KOW §5.6].
   * KOW explicitly ask about o(n²) for F_3.
   * At the Davenport threshold the problem is PPA_p-complete [GKSZ].
2. **Merging methods (Wagner, BKW, iterative halving) are not polynomial [argued].**
   * Each merge level at least halves the list and cancels b coordinates, which needs a list of size at least p^b.
   * Polynomial lists force b = O(log g), hence at least g/log g levels, hence a 2^{g/log g} loss.
   * Their best is exp(O(g/log(M/g))). The optimum of M ≈ 2^t·p^{a/(t+1)} is 2^{2√(a log₂ p)}.
3. **Other suggested approaches.**
   * Coordinate-by-coordinate grouping (any p elements of F_p contain a zero-sum) loses a factor between 2 and p per coordinate, giving 2^a to p^a.
   * Lattice reduction on {x : Σ x_iλ_i ≡ 0} finds short signed vectors, i.e. collisions. Turning them into 0/1 is exactly the ±1 → 0/1 step, which costs one more squaring here. LLL's 2^{M/2} factor rules out using it directly at large M.
4. **A degree independent of p**, for (A) or (B): not achieved.
   * Best known degrees for (B): 2 (p = 3); 4 (p = 5, 7; KOW and Theorem B); 6 (p = 11); 8 (p = 13).
   * Best known degrees for (A): 2, 6, 6, 16, 16.
   * In the gadget framework, degree = number of nested linear-algebra layers. Each ±1-halving costs one squaring (KOW ask whether n^{o(k)} is possible), and ±1 → 0/1 costs another.

## 7. Experiments

Python, numpy, and a small C row-reduction kernel compiled at import, with a pure-numpy fallback. One core per trial on a 4-core cloud VM. Inputs are i.i.d. uniform on a hidden random subspace of dimension a. Arity counts every vector read, including the g+8 used for span estimation. Every output was checked against the original vectors in F_p^g.

1800 trials ran in total, with 0 failures and 0 exceptions.

| p | g | dim a | recycle | trials | success | arity mean | median | max | arity/a^k | mean time (s) | max time (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 10 | 10 | yes | 100 | 100/100 | 30 | 32 | 41 | 0.298 (k=2) | 0.002 | 0.010 |
| 3 | 20 | 20 | yes | 100 | 100/100 | 115 | 119 | 132 | 0.288 (k=2) | 0.005 | 0.012 |
| 3 | 40 | 40 | yes | 100 | 100/100 | 457 | 460 | 481 | 0.285 (k=2) | 0.021 | 0.050 |
| 3 | 80 | 80 | yes | 100 | 100/100 | 1845 | 1846 | 1883 | 0.288 (k=2) | 0.103 | 0.223 |
| 5 | 10 | 10 | yes | 100 | 100/100 | 1354 | 1395 | 1612 | 0.135 (k=4) | 0.099 | 0.196 |
| 5 | 20 | 20 | yes | 100 | 100/100 | 16355 | 16322 | 17819 | 0.102 (k=4) | 0.908 | 1.463 |
| 5 | 40 | 40 | yes | 100 | 100/100 | 222289 | 222834 | 232222 | 0.087 (k=4) | 7.641 | 9.277 |
| 5 | 80 | 80 | yes | 100 | 100/100 | 3305005 | 3300846 | 3393440 | 0.081 (k=4) | 115.2 | 119.9 |
| 7 | 10 | 10 | yes | 100 | 100/100 | 1676 | 1673 | 1859 | 0.168 (k=4) | 0.116 | 0.199 |
| 7 | 20 | 20 | yes | 100 | 100/100 | 19128 | 19130 | 20207 | 0.120 (k=4) | 0.832 | 1.228 |
| 7 | 40 | 40 | yes | 100 | 100/100 | 257943 | 257988 | 267233 | 0.101 (k=4) | 8.598 | 9.917 |
| 7 | 80 | 80 | yes | 100 | 100/100 | 3828823 | 3827618 | 3899812 | 0.093 (k=4) | 133.8 | 150.5 |
| 3 | 80 | 40 (subspace) | yes | 100 | 100/100 | 454 | 458 | 486 | 0.284 (k=2) | 0.026 | 0.052 |
| 5 | 40 | 20 (subspace) | yes | 100 | 100/100 | 16402 | 16402 | 17706 | 0.103 (k=4) | 0.759 | 1.119 |
| 7 | 40 | 20 (subspace) | yes | 100 | 100/100 | 19124 | 19084 | 20586 | 0.120 (k=4) | 0.864 | 1.275 |
| 3 | 20 | 20 | no | 100 | 100/100 | 142 | 146 | 162 | 0.356 (k=2) | 0.007 | 0.015 |
| 5 | 20 | 20 | no | 100 | 100/100 | 16902 | 16974 | 17791 | 0.106 (k=4) | 0.705 | 1.058 |
| 7 | 20 | 20 | no | 100 | 100/100 | 19332 | 19342 | 20458 | 0.121 (k=4) | 0.655 | 0.874 |

Notes:
* The arity/a⁴ ratio falls steadily for p = 5, 7: 0.135 → 0.081 and 0.168 → 0.093. Arity depends on a = dim U, not on g, as the subspace rows show.
* At g = 80 a trial uses on average about 2634 objects for p = 5 and 2837 for p = 7, and discards about 17 degenerate blocks per trial.
* The zero-sum sets found are large: |T| ≈ 6×10⁵ for p = 5 at g = 80, about 18% of the arity. If set size matters in the HSP, this needs a look.
* For comparison: the information-theoretic arity is about a·log₂p (127 for p = 3, a = 80). The old IS-style bound is g^{(p−1)⌈log₂p⌉}, i.e. 80¹² for p = 5. Exhaustive search at arity g(p−1)+1 costs p^{O(g)}.
* The p = 7, g = 80 row was finished by resume.py after a worker restart killed the driver at 28/100. Seeds are the same as run_exp.py's.

## 8. Proposed LaTeX lemma (to replace the p^{O(g)} search at κ = p−1)

```latex
\begin{lemma}[Polynomial-time zero-sum node for uniform samples]\label{lem:poly-zero-sum}
Let $p$ be a fixed prime, $U\le\mathbb F_p^{g}$ an unknown subspace with
$a=\dim U$, and $\tau\in(0,1)$. There is a deterministic classical procedure
that reads i.i.d.\ uniform samples $\lambda_1,\lambda_2,\dots\in U$, reads at
most $M_p(a,g,\tau)$ of them, runs in time $\mathrm{poly}(g,M_p)$, and with
probability at least $1-\tau$ returns a non-empty $T$ with
$\sum_{i\in T}\lambda_i=0$; any returned $T$ is correct. One may take
\begin{align*}
 M_3 &= \tfrac{(a+1)(a+2)}{2}\quad\text{(worst case, no randomness)},\\
 M_p &= g+\lceil\log_p(2/\tau)\rceil+\tfrac{(a+1)(a+4)}{2}
       +\Big\lceil \tfrac{(a+1)\,(a(a+1)(a+4)+8\ln(2/\tau))}{\rho_p}\Big\rceil
       \quad (p=5,7;\ \rho_5=0.456,\ \rho_7=0.478),\\
 M_p &= g+\lceil\log_p(2/\tau)\rceil+C_p\,a^{2\lfloor (p+3)/4\rfloor}\log(1/\tau)
       \quad (p\ge 11,\ \text{\cite[Thm.~4.12]{KOW25}} \text{ on coordinates of } U).
\end{align*}
In particular $M_p=O(g^2)$ for $p=3$ and $O(g^4+g\log(1/\tau))$ for $p\in\{5,7\}$.
\end{lemma}
\begin{proof}[Proof sketch]
$p=3$: dimension reduction with $\{0,1\}$-reducible vectors
\cite{ISS07,KOW25}. $p\in\{5,7\}$: span estimation; a worst-case $(\pm1)$
dimension-reduction solver \cite[Lem.~3.3, Thm.~3.7]{KOW25} whose items are
$(0,1,2)$-zero-sums modulo the current top span, each obtained from a
$\pm1$-spanning gadget on fresh samples by the shift $t=-\sum_{B'}w$; the
final $\pm1$ relation is converted to a $\{0,1\}$ relation as in
\cite[Lem.~3.10]{KOW25}, the top-span errors being absorbed by bottom-up
lifting. Failure only comes from span estimation ($\le p^{-s}$) and from a
Chernoff bound on gadget attempts, each succeeding with probability
$\ge\rho_p$. Full proof: audit note 2026-11-04-rees-cloud-zero-sum, Thm.~B.
\end{proof}
```

**Use in the paper.**
* At grade κ = p−1, the node changes from "arity g(p−1)+1, time p^{O(g)}" to "arity M_p, time poly(g)".
* The sample count per node rises. Measured: about 0.29a² for p = 3 and about 0.09a⁴ for p = 5, 7. The provable constant for p = 5, 7 is about 2.2a⁴.
* Any Schedule 3 or derived-dimension corollary that counts samples must use M_p. Any corollary that counts classical time loses its exponential term.
* For p ≥ 11 the degree 2⌊(p+3)/4⌋ still grows with p. A degree independent of p would answer [II §6] / [KOW §5.1].

## 9. Next hard question, command, artifact, acceptance test

* **Next hard questions.**
  1. Close the §5 gap: build a worst-case ±1-spanning gadget for p = 5 that contains its own blocks. That would give worst-case F_5 subset-sum at O(n⁴) and answer KOW's question for q = 5.
  2. Degree 3 for p = 5, 7 on random inputs: can one ±1 gadget feed Θ(a) objects?
* **Claims that must stay false:** "degree independent of p"; "M = O(g log g) in poly time"; "(A) ≡ (B) via II §6".
* **Next command:** from the folder holding the §10 files,
  ```bash
  python3 run_exp.py results.jsonl && python3 summarize.py results.jsonl
  ```
  Artifact: results.jsonl plus the table. Acceptance test: every row reports 100/100 success, and the arity/a⁴ ratio does not increase with g for p = 5, 7.
* **Human-review targets:**
  * Lemma R(a) when the |α| ≥ 2 set is the whole circuit.
  * (★) for items created at earlier top levels.
  * The II §6 flaw.
* **Mechanical items for MECHANICAL_FOLLOW_UP_PLAN.md:**
  1. Rerun the table with the fresh-vector variant to compare with M_p.
  2. Port KOW Thm 4.11 to p = 11, 13 and test whether it yields a spanning gadget.
  3. Check that the zero-sum set size |T| is acceptable in the HSP circuit.

## 10. Source code (complete)

### zerosum.py
```python
#!/usr/bin/env python3
"""zerosum.py -- polynomial-time zero-sum-subset finder in F_p^g, p in {3,5,7},
for i.i.d. uniform vectors on an unknown subspace U of F_p^g.

  p = 3 : 'sub' engine = dimension reduction with {0,1}-reducible vectors
          (ISS07 / KOW25 Thm 1.2 style, sparse relations).  Worst-case correct.
  p = 5,7: nested engine.  Top: worst-case (+-1)-solver (KOW25 Thm 3.7 style)
          whose items are (0,1,2)-zero-sums built, modulo the top span, from a
          full (+-1)-gadget ("every target is a +-1 sum") on fresh vectors.

Every output is verified: a nonempty set T of stream indices with
sum_{i in T} lambda_i = 0 in F_p^g.  Randomness only affects the arity used.
AI-generated research code, pending human review.
"""
import numpy as np, math, time, sys, os, ctypes, subprocess, tempfile, itertools

# ---------------------------------------------------------------- C kernel
_C = r"""
#include <stdint.h>
int rowreduce(int32_t *A,int k,int m,int p,const int32_t *inv){
  int w=m+k,row=0;
  for(int col=0;col<m&&row<k;col++){
    int piv=-1; for(int i=row;i<k;i++) if(A[i*w+col]){piv=i;break;}
    if(piv<0) continue;
    if(piv!=row) for(int j=0;j<w;j++){int32_t t=A[row*w+j];A[row*w+j]=A[piv*w+j];A[piv*w+j]=t;}
    int32_t s=inv[A[row*w+col]];
    for(int j=col;j<w;j++) A[row*w+j]=(A[row*w+j]*s)%p;
    for(int i=row+1;i<k;i++){int32_t f=A[i*w+col]; if(!f) continue; f=p-f;
      for(int j=col;j<w;j++) A[i*w+j]=(A[i*w+j]+f*A[row*w+j])%p;}
    row++;
  }
  return row;
}"""
_lib = None
def _load():
    global _lib
    try:
        d = tempfile.mkdtemp(); c = os.path.join(d, 'k.c'); so = os.path.join(d, 'k.so')
        open(c, 'w').write(_C)
        subprocess.check_call(['gcc', '-O2', '-shared', '-fPIC', c, '-o', so])
        _lib = ctypes.CDLL(so)
        _lib.rowreduce.restype = ctypes.c_int
    except Exception:
        _lib = None
_load()

def relations(R, p, inv32):
    """Rows of R (k x m) over F_p -> matrix N (s x k), RREF, whose rows span all
    linear relations sum_i N[t,i] R[i] = 0 (s = k - rank)."""
    k, m = R.shape
    A = np.ascontiguousarray(np.hstack([R, np.eye(k, dtype=np.int64)]) % p, dtype=np.int32)
    if _lib is not None:
        rank = _lib.rowreduce(A.ctypes.data_as(ctypes.c_void_p), k, m, p,
                              inv32.ctypes.data_as(ctypes.c_void_p))
    else:                                   # pure numpy fallback
        A = A.astype(np.int64); rank = 0
        for col in range(m):
            if rank == k: break
            nz = np.nonzero(A[rank:, col])[0]
            if nz.size == 0: continue
            pv = rank + nz[0]; A[[rank, pv]] = A[[pv, rank]]
            A[rank] = A[rank] * int(inv32[A[rank, col]]) % p
            f = A[rank + 1:, col]
            A[rank + 1:] = (A[rank + 1:] - np.outer(f, A[rank])) % p
            rank += 1
    N = A[rank:, m:].astype(np.int64)
    if N.shape[0] == 1:
        j = np.nonzero(N[0])[0][0]; return N * int(inv32[N[0, j]]) % p
    return rref(N, p, inv32)

def rref(N, p, inv32):
    N = N.copy(); r = 0
    for col in range(N.shape[1]):
        if r == N.shape[0]: break
        nz = np.nonzero(N[r:, col])[0]
        if nz.size == 0: continue
        pv = r + nz[0]; N[[r, pv]] = N[[pv, r]]
        N[r] = N[r] * int(inv32[N[r, col]]) % p
        for i in range(N.shape[0]):
            if i != r and N[i, col]: N[i] = (N[i] - N[i, col] * N[r]) % p
        r += 1
    return N

_CB = {}
def _combos(p, s):
    """All beta in F_p^s, nonzero, first nonzero entry 1 (projective points)."""
    if (p, s) not in _CB:
        _CB[p, s] = np.array([b for b in itertools.product(range(p), repeat=s)
                              if any(b) and b[next(i for i in range(s) if b[i])] == 1], np.int64)
    return _CB[p, s]

# ---------------------------------------------------------------- engine
class Solution(Exception):
    def __init__(self, choices, base=None):
        self.choices, self.base = choices, base

class Engine:
    """Dimension-reduction ('levels').  mode 'sub': coefficients {0,1} (p=3);
    mode 'pm': coefficients {-1,0,1} (p=5,7).  gadget=False: raise Solution at
    the first zero-sum (coefficients relative to the current level); gadget=True:
    build levels until the current space is 0 (degenerate blocks discarded)."""
    def __init__(self, p, mode, n, active, supply, gadget=False, r=1):
        self.p, self.mode, self.n, self.gadget, self.r = p, mode, n, gadget, r
        self.inv32 = np.array([0] + [pow(i, p - 2, p) for i in range(1, p)], dtype=np.int32)
        self.active = np.array(sorted(active), dtype=np.int64)
        self.supply = supply                     # supply(cnt) -> (ids, rows in base coords)
        self.levels = []                         # (pi, u, uinv, reps, col)
        self.M = np.eye(n, dtype=np.int64)       # composite projection, x -> x @ M
        self.ids, self.X = np.zeros(0, np.int64), np.zeros((0, n), np.int64)
        self.blocks, self.discarded, self.zero_ids = [], [], []

    def _r(self, d):
        return self.r(d) if callable(self.r) else self.r

    def fill(self, k):
        while len(self.ids) < k:
            ids, V = self.supply(k - len(self.ids))
            Y = (np.asarray(V, dtype=np.int64) @ self.M) % self.p
            nz = Y[:, self.active].any(axis=1) if len(self.active) else np.zeros(len(ids), bool)
            for t in np.nonzero(~nz)[0]:
                if not self.gadget: raise Solution((np.array([ids[t]]), np.ones(1, np.int64)))
                self.zero_ids.append(ids[t])
            keep = np.nonzero(nz)[0]
            self.ids = np.concatenate([self.ids, np.asarray(ids, np.int64)[keep]])
            self.X = np.vstack([self.X, Y[keep]])

    def step(self):
        p, d = self.p, len(self.active)
        if d == 0:
            if self.gadget: return 'done'
            self.fill(len(self.ids) + 1)          # space is 0: next item projects to 0
            raise AssertionError('unreachable')
        k = d + self._r(d)
        self.fill(k)
        R = self.X[:k][:, self.active]
        N = relations(R, p, self.inv32)[:4]
        C = (_combos(p, N.shape[0]) @ N) % p
        order = np.argsort((C != 0).sum(1), kind='stable')
        degen = None
        for t in order:
            res = self.analyze(C[t])
            if res[0] == 'sol': raise Solution(res[1])
            if res[0] == 'level':
                self.add_level(*res[1:]); return 'level'
            if degen is None: degen = res[1]
        # all candidates degenerate (gadget mode only): discard one block
        self.discarded.append(self.ids[degen])
        self._drop(degen)
        return 'degen'

    def analyze(self, alpha):
        p, X, ids = self.p, self.X, self.ids
        idx = np.nonzero(alpha)[0]; a = alpha[idx]; I = ids[idx]
        one = lambda S: (ids[S], np.ones(len(S), np.int64))
        if self.mode == 'sub':                                   # p = 3
            J1, J2 = idx[a == 1], idx[a == 2]
            if len(J1) == 0 or len(J2) == 0:
                return ('sol', one(J1 if len(J1) else J2))
            u = X[J1].sum(0) % p
            if not u.any(): return ('sol', one(J1))
            return ('level', u, {1: one(J1), 2: one(idx)}, idx)
        s = np.where(a > p // 2, a - p, a); ab = np.abs(s); sg = np.sign(s)
        if (ab == ab[0]).all():                                  # +-1 relation (collision)
            if not self.gadget: return ('sol', (I, sg))
            Sp = idx[sg > 0]
            if p == 5 and len(Sp) and (sg < 0).any():
                z = X[Sp].sum(0) % p
                if z.any():
                    o1, oa = one(Sp), one(idx)
                    reps = {1: o1, 4: (o1[0], -o1[1]), 2: oa, 3: (oa[0], -oa[1])}
                    return ('level', z, reps, idx)
            return ('degen', idx)
        H = ab >= 2
        u = (sg[H] @ X[idx[H]]) % p
        if not u.any():
            if not self.gadget: return ('sol', (I[H], sg[H]))
            return ('degen', idx)
        reps = {}
        for c in range(1, p // 2 + 1):                             # KOW Lemma 3.3, h'=1
            g = sg * H if c == 1 else np.where(s >= 2, c - s, np.where(s <= -2, -c - s, -s))
            assert np.abs(g).max() <= 1
            nz = g != 0
            reps[c] = (I[nz], g[nz]); reps[p - c] = (I[nz], -g[nz])
        return ('level', u, reps, idx)

    def _drop(self, idx):
        keep = np.ones(len(self.ids), bool); keep[idx] = False
        self.ids = self.ids[keep]; self.X = self.X[keep]

    def add_level(self, u, reps, idx):
        p = self.p
        pi = int(self.active[np.nonzero(u[self.active])[0][0]])
        uinv = int(self.inv32[u[pi]])
        col = self.M[:, pi].copy()                 # Q_{j-1}(x)[pi] = x . col
        self.levels.append((pi, u.copy(), uinv, reps, col))
        self.blocks.append(self.ids[idx])
        self._drop(idx)
        self.X = (self.X - np.outer(self.X[:, pi] * uinv % p, u)) % p
        self.M = (self.M - np.outer(self.M[:, pi] * uinv % p, u)) % p
        self.active = self.active[self.active != pi]
        if len(self.ids):
            z = ~self.X[:, self.active].any(axis=1) if len(self.active) else np.ones(len(self.ids), bool)
            if z.any():
                if not self.gadget:
                    raise Solution((self.ids[np.nonzero(z)[0][:1]], np.ones(1, np.int64)))
                self.zero_ids += list(self.ids[np.nonzero(z)[0]])
                self._drop(np.nonzero(z)[0])

def assemble(p, levels, value, choices, base, target):
    """Bottom-up lifting: extend `choices` = (ids, coefs) with level representatives
    so that base + sum value = target.  Returns dict id -> coef."""
    out = [choices] if len(choices[0]) else []
    r = (target - base) % p
    if len(choices[0]): r = (r - value(*choices)) % p
    for j in range(len(levels) - 1, -1, -1):
        pi, u, uinv, reps, col = levels[j]
        c = int((r @ col) % p * uinv % p)
        if c:
            out.append(reps[c]); r = (r - value(*reps[c])) % p
    assert not r.any(), 'assembly failed'
    ids = np.concatenate([o[0] for o in out]) if out else np.zeros(0, np.int64)
    cf = np.concatenate([o[1] for o in out]) if out else np.zeros(0, np.int64)
    assert len(set(ids.tolist())) == len(ids), 'overlap'
    return dict(zip(ids.tolist(), cf.tolist()))

# ---------------------------------------------------------------- driver
class Stream:
    """i.i.d. uniform vectors on a hidden random subspace of dimension a of F_p^g."""
    def __init__(self, p, g, a, rng):
        self.p, self.g, self.rng = p, g, rng
        while True:
            G = rng.integers(0, p, (a, g))
            if rref(G, p, np.array([0] + [pow(i, p - 2, p) for i in range(1, p)])).any(1).sum() == a: break
        self.G = G; self.a = a
    def draw(self, cnt):
        return (self.rng.integers(0, self.p, (cnt, self.a)) @ self.G) % self.p

class Ctx:
    """Vector source.  First g+s vectors estimate span(U) (RREF basis B); every
    vector is then stored with its coordinates in that basis (membership is
    checked, so a wrong span estimate is detected, never silently used)."""
    def __init__(self, p, g, stream, recycle=True, s_extra=8):
        self.p, self.g, self.stream, self.recycle = p, g, stream, recycle
        self.n = 0; self.cap = 1024
        self.O = np.zeros((self.cap, g), np.int8)
        inv = np.array([0] + [pow(i, p - 2, p) for i in range(1, p)])
        V0 = stream.draw(g + s_extra)
        B = rref(V0, p, inv); self.B = B[B.any(1)]; self.a = len(self.B)
        self.pc = np.array([int(np.nonzero(row)[0][0]) for row in self.B])
        self.Uc = np.zeros((self.cap, self.a), np.int8)
        ids = self._store(V0)
        self.spare = list(ids) if recycle else []
    @property
    def U(self): return self.Uc[:self.n].astype(np.int64)
    def _store(self, V):
        C = V[:, self.pc]
        if ((C @ self.B) % self.p != V).any(): raise RuntimeError('span estimate wrong')
        while self.n + len(V) > self.cap:
            self.cap *= 2
            self.O = np.resize(self.O, (self.cap, self.g)); self.Uc = np.resize(self.Uc, (self.cap, self.a))
        self.O[self.n:self.n + len(V)] = V; self.Uc[self.n:self.n + len(V)] = C
        self.n += len(V)
        return list(range(self.n - len(V), self.n))
    def draw(self, cnt):
        out = []
        while self.spare and len(out) < cnt: out.append(self.spare.pop())
        if len(out) < cnt: out += self._store(self.stream.draw(cnt - len(out)))
        return out, self.Uc[out].astype(np.int64)

def solve_p3(ctx):
    p = 3
    r = lambda d: max(1, math.ceil(math.log(d + 1, 3)))
    eng = Engine(p, 'sub', ctx.a, range(ctx.a), ctx.draw, gadget=False, r=r)
    val = lambda ids, cf: (cf @ ctx.Uc[ids].astype(np.int64)) % p
    try:
        while True: eng.step()
    except Solution as S:
        ch = assemble(p, eng.levels, val, S.choices, np.zeros(ctx.a, np.int64), np.zeros(ctx.a, np.int64))
    return sorted(i for i, c in ch.items() if c)

def solve_p57(ctx, r_in=2):
    p, a = ctx.p, ctx.a
    items = []                                     # (coef1 ids, coef2 ids, vplus, vminus)
    stats = {'objects': 0, 'degen': 0}
    top = None

    def make_object():
        W, gid = [], []
        def supply(cnt):
            G, V = ctx.draw(cnt)
            Y = (V @ top.M) % p
            base = len(W); W.extend(list(Y)); gid.extend(G)
            return list(range(base, base + cnt)), Y
        inner = Engine(p, 'pm', a, top.active, supply, gadget=True, r=r_in)
        while inner.step() != 'done': pass
        stats['degen'] += len(inner.discarded)
        if not len(inner.ids): supply(1); inner.ids = np.array([len(W) - 1])
        v0 = int(inner.ids[0]); left = list(inner.ids[1:])
        used = np.concatenate(inner.blocks).astype(np.int64) if inner.blocks else np.zeros(0, np.int64)
        Wm = np.array(W, dtype=np.int64)
        t = (-(Wm[used].sum(0) + Wm[v0])) % p
        val = lambda ids, cf: (cf @ Wm[ids]) % p
        alpha = assemble(p, inner.levels, val, (np.zeros(0, np.int64),) * 2, np.zeros(a, np.int64), t)
        coef = {int(i): 1 for i in used}; coef[v0] = 1
        for i, c in alpha.items(): coef[i] = 1 + c
        ci = np.array(list(coef)); cv = np.array([coef[i] for i in ci])
        assert not ((cv @ Wm[ci]) % p).any()
        if ctx.recycle: ctx.spare += [gid[i] for i in left + list(inner.zero_ids)]
        c1 = [gid[i] for i, c in coef.items() if c == 1]
        c2 = [gid[i] for i, c in coef.items() if c == 2]
        stats['objects'] += 1
        return c1, c2

    def supply_items(cnt):
        ids, rows = [], []
        for _ in range(cnt):
            c1, c2 = make_object()
            s1 = ctx.Uc[c1].astype(np.int64).sum(0) % p
            if not c2:                                       # u_k in Z: finish now
                raise Solution((np.zeros(0, np.int64),) * 2, base=(c1, s1))
            s2 = ctx.Uc[c2].astype(np.int64).sum(0) % p
            items.append((c1, c2, s2, (s1 + s2) % p))
            ids.append(len(items) - 1); rows.append(s2)
        return ids, np.array(rows, dtype=np.int64)

    top = Engine(p, 'pm', a, range(a), supply_items, gadget=False, r=1)
    def val(ids, cf):
        return sum((items[i][2] if c == 1 else items[i][3]) for i, c in zip(ids, cf)) % p
    try:
        while True: top.step()
    except Solution as S:
        base_ids, base = S.base if S.base else ([], np.zeros(a, np.int64))
        ch = assemble(p, top.levels, val, S.choices, base, np.zeros(a, np.int64))
    T = list(base_ids)
    for i, c in ch.items():
        c1, c2 = items[i][0], items[i][1]
        T += c2 if c == 1 else c1 + c2
    return sorted(T), stats

def trial(p, g, a=None, seed=0, recycle=True):
    try:
        return _trial(p, g, a, seed, recycle)
    except Exception as e:                       # recorded as a failure, never hidden
        return dict(p=p, g=g, a=a or g, ok=False, arity=-1, size=0, time=0.0, err=repr(e))

def _trial(p, g, a=None, seed=0, recycle=True):
    rng = np.random.default_rng(seed)
    st = Stream(p, g, a or g, rng)
    t0 = time.time()
    ctx = Ctx(p, g, st, recycle=recycle)
    if p == 3: T, stats = solve_p3(ctx), {}
    else: T, stats = solve_p57(ctx)
    dt = time.time() - t0
    ok = len(T) > 0 and len(set(T)) == len(T) and \
         not (ctx.O[T].astype(np.int64).sum(0) % p).any()
    return dict(p=p, g=g, a=a or g, ok=bool(ok), arity=ctx.n, size=len(T), time=dt,
                recycle=recycle, seed=seed, **stats)

if __name__ == '__main__':
    p, g = int(sys.argv[1]), int(sys.argv[2])
    a = int(sys.argv[3]) if len(sys.argv) > 3 else None
    print(trial(p, g, a, seed=int(sys.argv[4]) if len(sys.argv) > 4 else 0))
```

### run_exp.py
```python
"""Experiment driver: python3 run_exp.py OUT.jsonl  (4 worker processes)."""
import sys, json, multiprocessing as mp
from zerosum import trial
def job(t): return trial(*t)
if __name__ == '__main__':
    out = sys.argv[1]; tasks = []
    spec = [(3, g, None, 100, True) for g in (10, 20, 40, 80)]
    spec += [(p, g, None, 100, True) for p in (5, 7) for g in (10, 20, 40)]
    spec += [(3, 80, 40, 100, True), (5, 40, 20, 100, True), (7, 40, 20, 100, True)]   # proper subspaces
    spec += [(p, 20, None, 100, False) for p in (3, 5, 7)]                              # no recycling
    spec += [(p, 80, None, 100, True) for p in (5, 7)]                                  # largest last
    for (p, g, a, n, rec) in spec:
        tasks += [(p, g, a, 1000 * g + s, rec) for s in range(n)]
    with mp.Pool(4) as pool, open(out, 'w') as f:
        for r in pool.imap(job, tasks):
            f.write(json.dumps(r) + '\n'); f.flush()
```

### resume.py (finished p = 7, g = 80 after the restart; the table uses `cat results.jsonl results_resume.jsonl`)
```python
import sys, json, multiprocessing as mp
from zerosum import trial
def job(t): return trial(*t)
if __name__ == '__main__':
    done = {json.loads(l)['seed'] for l in open('results.jsonl') if json.loads(l)['p'] == 7 and json.loads(l)['g'] == 80}
    tasks = [(7, 80, None, 80000 + s, True) for s in range(100) if 80000 + s not in done]
    with mp.Pool(4) as pool, open('results_resume.jsonl', 'a') as f:
        for r in pool.imap_unordered(job, tasks):
            f.write(json.dumps(r) + '\n'); f.flush()
```

### summarize.py
```python
import json, collections, statistics as st, sys
d = collections.OrderedDict()
for l in open(sys.argv[1]):
    r = json.loads(l); d.setdefault((r['p'], r['g'], r['a'], r['recycle']), []).append(r)
print('| p | g | dim a | recycle | trials | success | arity mean | median | max | arity/a^k | mean time (s) | max time (s) |')
print('|---|---|---|---|---|---|---|---|---|---|---|---|')
for (p, g, a, rec), v in d.items():
    ok = [x for x in v if x['ok']]; ar = [x['arity'] for x in ok]; tm = [x['time'] for x in ok]
    k = 2 if p == 3 else 4
    print(f"| {p} | {g} | {a} | {'yes' if rec else 'no'} | {len(v)} | {len(ok)}/{len(v)} | {st.mean(ar):.0f} | {st.median(ar):.0f} | {max(ar)} | "
          f"{st.mean(ar)/a**k:.3f} (k={k}) | {st.mean(tm):.3f} | {max(tm):.3f} |")
    errs = [x.get('err') for x in v if not x['ok']]
    if errs: print('   errors:', errs[:3])
```

### check_rho.py (Lemma D)
```python
"""Monte Carlo check of Lemma D: Pr[first i of i+1 uniform vectors in F_q^i form a
basis AND the circuit through the last one is good] >= rho_q."""
import numpy as np, math
from zerosum import rref
rng = np.random.default_rng(1)
for q in (5, 7):
    inv = np.array([0] + [pow(i, q - 2, q) for i in range(1, q)])
    lb = math.prod(1 - q ** -k for k in range(1, 60)) * (1 - (2 if q == 5 else 3) / q)
    out = []
    for i in (1, 2, 3, 5, 10):
        good = 0; T = 4000
        for _ in range(T):
            V = rng.integers(0, q, (i + 1, i))
            B = V[:i]
            if rref(B, q, inv).any(1).sum() < i: continue
            A = np.hstack([B.T, V[i:].T]) % q
            Rr = rref(A, q, inv); c = Rr[:i, i]
            s = np.where(c > q // 2, c - q, c)
            bad = np.isin(s, [0, -1]).all() if q == 5 else np.isin(np.abs(s), [0, 1]).all()
            good += not bad
        out.append((i, round(good / T, 3)))
    print(q, 'lower bound %.3f' % lb, out)
```
Output:
```
5 lower bound 0.456 [(1, 0.473), (2, 0.642), (3, 0.716), (5, 0.754), (10, 0.773)]
7 lower bound 0.478 [(1, 0.482), (2, 0.7), (3, 0.773), (5, 0.821), (10, 0.83)]
```

### adversarial_p3.py (worst-case checks for p = 3)
```python
"""Worst-case sanity check of the p=3 engine on structured inputs (deterministic
algorithm; arity must stay <= (a+1)(a+2)/2 + r slack)."""
import numpy as np, zerosum as Z
class ListStream:
    def __init__(self, L): self.L, self.i = np.array(L) % 3, 0
    def draw(self, cnt):
        out = self.L[self.i:self.i + cnt]; self.i += cnt
        if len(out) < cnt: raise RuntimeError('out of vectors')
        return out
def run(L, g):
    st = ListStream(L); ctx = Z.Ctx.__new__(Z.Ctx)
    ctx.p, ctx.g, ctx.stream, ctx.recycle = 3, g, st, False
    ctx.n, ctx.cap = 0, 1024; ctx.O = np.zeros((1024, g), np.int8); ctx.spare = []
    inv = np.array([0, 1, 2]); B = Z.rref(np.array(L) % 3, 3, inv); ctx.B = B[B.any(1)]; ctx.a = len(ctx.B)
    ctx.pc = np.array([int(np.nonzero(r)[0][0]) for r in ctx.B]); ctx.Uc = np.zeros((1024, ctx.a), np.int8)
    T = Z.solve_p3(ctx)
    ok = len(T) > 0 and not (ctx.O[T].astype(int).sum(0) % 3).any()
    return ok, ctx.n, ctx.a
rng = np.random.default_rng(5); g = 20; I = np.eye(g, dtype=int)
cases = {
 'Davenport-extremal (each e_i twice) + 1 random': [I[i] for i in range(g) for _ in range(2)] + [rng.integers(0, 3, g)],
 'e_1 repeated': [I[0]] * 10,
 'basis then copies of e_1': list(I) + [I[0]] * 5,
 'random in 5-dim subspace': list(rng.integers(0, 3, (60, 5)) @ rng.integers(0, 3, (5, g))),
 'basis, then e_i+e_{i+1}': list(I) + [I[i] + I[(i + 1) % g] for i in range(g)] * 3,
 'random sparse (weight 2)': [I[rng.integers(g)] + I[rng.integers(g)] for _ in range(250)],
}
for k, L in cases.items():
    print(k, run(L, g))
```
Output (ok, vectors read, dim): Davenport-extremal (True, 41, 20); e₁ repeated (True, 3, 1); basis then copies of e₁ (True, 23, 20); random in 5-dim subspace (True, 11, 5); basis then e_i+e_{i+1} (True, 43, 20); random sparse (True, 76, 20).

Sources:
- [Ivanyos–Santha, arXiv:1503.09016](https://arxiv.org/abs/1503.09016)
- [Imran–Ivanyos, arXiv:2304.08376](https://arxiv.org/abs/2304.08376)
- [Kothari–O'Donnell–Wu, arXiv:2510.07515](https://arxiv.org/abs/2510.07515)
- [Göös–Kamath–Sotiraki–Zampetakis, arXiv:1912.04467](https://arxiv.org/abs/1912.04467)
- [Hashimoto, arXiv:1507.03674](https://arxiv.org/pdf/1507.03674)
- [Alon–Linial–Meshulam](https://web.math.princeton.edu/~nalon/PDFS/Publications2/Additive%20bases%20of%20vector%20spaces%20over%20prime%20fields.pdf)
- [Ivanyos–Sanselme–Santha, nil-2 HSP](https://arxiv.org/abs/0707.1260)
