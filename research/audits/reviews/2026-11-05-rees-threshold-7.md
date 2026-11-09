# Two-level SDE threshold, round 7: flexible-line chains, union targets, and a bounded-excess barrier

5 November 2026 (overnight pass). AI-only research pass: one Claude Code session, no helper
agents. It is not a human review, a Lean proof or a priority claim. **"AI-checked, pending human
review" applies to every claim below.** No `.tex` file, no git state and no registry file was
touched; `research/reductions/rees_hsp_reduction.json` was not opened.

Labels: **[proved]** full proof written here; **[exact]** complete finite computation (script
named, every witness re-checked by a separately written checker); **[float]** explicit closed-form
or proved-monotone functions evaluated in 40-digit arithmetic; **[conjecture]**; **[argued]**.

Scripts and outputs: `2026-11-05-rees-threshold-7/` (interpreter `/opt/anaconda3/bin/python`;
`rectu.c` is copied unchanged from `2026-11-05-rees-threshold-6/` and compiled here with `cc -O2`;
the binary `rectu` is scratch and should not be committed). Everything ran under `nice -n 10`
with at most two processes.

Notation as in `appendix-schedule2.tex` and the inserted subsection `app:s2-tower`: p prime,
κ | p − 1, ξ a coset generator, P_D = (F_p^×)^D, Q^{(D)}_m = ξ^m P_D, and the D-class of x ≠ 0 is
ind(x) mod D. A *relation modulo U* is a weight vector c with Σ_b c_bλ_b ∈ U. For D | p − 1,
0 ∈ R ⊆ Z_D and 0 ∈ K ⊆ Z_D, an **RC(D; R → K) contraction** is (α, β) ∈ F_p^{Z_D} × F_p^R with

- α_j + β_i ∈ {0} ∪ ⋃_{k∈K} Q^{(D)}_{k−i−j} for all i ∈ R, j ∈ Z_D, and
- α_0 + β_0 ∈ Q^{(D)}_0.

This is Definition 2.1 of threshold-6 (`lem:app-s2-refine` is the case K = {0}). Translating β_0
to 0 and dividing by α_0 ∈ Q^{(D)}_0 changes no class, so we always take **α_0 = 1, β_0 = 0**.

## 0. Verdict

**(A) Quadratic arity at a polynomial threshold for composite κ: not achieved, and the specific
mechanism asked for is impossible.**

- **Barrier (Theorem 3.1) [proved].** Let p ∈ E_2(κ). A round object that consists of
  m + h fresh uniformly random columns in an m-dimensional quotient, with h fixed, has *no*
  flexible line (under any rule: universal, column-dependent, adaptive or computationally
  unbounded) with probability at least
  1 − κp^hθ_1^{m+h} − Σ_{r=2}^{κ−1} p^{r(κ−1+h)}θ_r^{m+h}, where θ_r = 1 − (1 − p^{−r})/κ.
  This tends to 1 as m → ∞.
  - "One dependency plus O(1) extra columns in each of L sub-steps" is such an object, with
    h = 1 + O(L). So it cannot realise the triangular solver's line at any p ∈ E_2(κ) once the
    quotient dimension m exceeds m_0(κ, p, h).
  - This happens at primes where the tower works. Examples are κ = 8 with p ∈ {11689, 12809},
    both in E_2(8) and above the tower threshold ((κ−1)²+1)² = 2500, and κ = 4 with
    p ∈ {17, 37, 53}.
  - The barrier is asymptotic. m_0, the least m at which the bound drops below 1, is about
    (κ−1)(κ−1+h)·ln p/ln(κ/(κ−1)): it is 146 at κ = 4, p = 17, h = 2 and 5450 at κ = 8,
    p = 12809, h = 4. For small m, kernel-2 objects at p = 17 do have lines (§5.3, exact).
- **What the combination does give (Theorem 2.2) [proved; exact tests].** The triangular
  recursion can be nested through the levels of any admissible chain (towers, union chains, and
  mixtures of both). This gives **C(a+L+1, L+1)** columns at exactly the thresholds of the chain's
  steps.
  - For the tower of `cor:app-s2-tower` this replaces (a+1)∏((q_t−1)a+1) by C(a+L+1, L+1),
    which is never larger. As a → ∞ the ratio tends to 1/((L+1)!∏(q_t−1)).
  - The degree L + 1 is unchanged: the arity is cubic for κ ∈ {4, 6, 9} and quartic for κ = 8.
    At a = 10 that is 286 columns for κ = 4 and κ = 6, against 1331 and 2541 for the tower.
  - Tests: end-to-end with exact arithmetic for κ = 4 (p = 17, 37, 53, 41, 61), κ = 6 (seven
    E_2(6) primes, up to 859) and κ = 8 (p = 97, 113, 193, 257, **11689, 12809**), on random
    and adversarial columns. Every output was checked with pow() (§5.1).
- **Reduction (Proposition 2.4) [proved].** O(a²) at a chain's threshold follows from any
  polynomial-time finder of P_D-relations modulo U that uses O(m) columns in an m-dimensional
  quotient, where D = D_{L−1}. Such a finder is exactly the open linear-arity problem for the
  smaller exponent D. Lemma 3.4 [proved] shows that a round which applies an RC contraction to a
  relation it contains needs excess h ≳ m·log D/log(p/D).

**(B) Prime κ: yes. A proved threshold far below κ^{κ+1}, at cubic arity [proved; float values;
exact small-κ sets].**

- **Union steps by a second moment (Proposition 4.1) [proved].** This is new here: threshold-6
  had only Weil bounds for union targets.
- **Two-step union chain (Theorem 4.3).** Let κ ≥ 4, which includes every prime κ ≥ 5. For the
  chain Z_κ → {0,…,k−1} → {0} and every prime p ≡ 1 (mod κ) above Θ_2(κ, k), any
  **C(a+3, 3)** columns admit a solution. Here
  Θ_2(κ, k) ≤ max(1 + 4.05κ(κ/k)^κ, 11.6κ³(κ/k)^4(1.2 + ln κ)^4, 100κ, 4κ^{k+1}, 4k²κ^5).
- **Asymptotics (Corollary 4.4).** For κ ≥ 16, the choice k = ⌈κ ln ln κ/ln κ⌉ gives
  **Θ_2(κ) ≤ 4.05κ²(ln κ)^κ = κ^{κ·ln ln κ/ln κ + O(1)}**. That is below κ^{κ/2} for every
  κ ≥ 19, and by the table also for 13 ≤ κ ≤ 18. It is far below T_A(κ) > (κ−1)κ^κ.
- **Values [float].**

  | κ | Θ_2, cubic C(a+3,3) | Θ_3, quartic C(a+4,4) | T_A(κ) |
  |---|---|---|---|
  | 5 | 3781 | 1217 | > 12500 |
  | 7 | 30823 | 15133 | > 4.9·10^6 |
  | 11 | 1.16·10^6 | 3.80·10^5 | > 2.8·10^12 |
  | 13 | 7.42·10^6 | 1.06·10^6 | > 3.6·10^15 |

  Θ_3 is the threshold of the three-step chain.
- **Exact sets for κ = 5, 7 [exact].** The chain Z_7 → {0,1,2} → {0,1} → {0} fails **exactly
  at {29, 43, 71}** among all p ≡ 1 (mod 7). Threshold-6's best set was {29, 43, 71, 113}. A
  four-step chain also covers 43.
  - So over all admissible chains, **only 29 and 71 remain uncovered at κ = 7**, and only 11 at
    κ = 5.
  - Mixed chains newly cover 67 at κ = 6; 89, 137 and 233 at κ = 8; and 109, 127, 163, 181,
    199, 307 and 433 at κ = 9 (§4.5). After this, the only primes with no admissible chain
    are 5, 13 (κ = 4); 11 (κ = 5); 7, 13, 19, 31, 43 (κ = 6); 29, 71 (κ = 7); 17, 41, 73
    (κ = 8); and 19, 37, 73 (κ = 9).
- **Routes that give nothing [proved].**
  - (B.2) refinement κ' = κr: every tower chain for any κ' with κ | κ' fails at every
    p ∈ E_2(κ), because its first step at a multiple of κ projects onto a two-level contraction
    at κ (Proposition 4.6). Also E_2(κ) ⊆ E_2(κ').
  - (B.1) extension fields: F_p-valued contractions over F_{p^k} are relabelled F_p-contractions
    when κ ∤ k, and do not exist when κ | k (κ ≥ 3). Contractions with entries outside F_p give
    weights outside F_p (Proposition 4.7).
  - (B.3) designs: the only families that collapse the κ² conditions to κ have one essential
    parameter (Lemma 4.8). Weil certifies them only from about κ^{2κ}; the reduction is proved,
    the conclusion is argued.
- **Not changed.** The two-level problem E_2(κ) itself, its square gap, `thm:power-sde`,
  Schedule 2, E_W(c) and the tables are untouched. The union chain is an alternative
  construction at cubic arity, not a statement about E_2(κ).

**Strongest proved statement.** For every κ ≥ 4, in particular every prime κ ≥ 5, and every
prime p ≡ 1 (mod κ) with p > Θ_2(κ) (≤ 4.05κ²(ln κ)^κ for κ ≥ 16; 3781 at κ = 5, 30823 at κ = 7),
any C(a+3, 3) columns λ_b ∈ F_p^a admit s ≠ 0 with Σ_b s_b^dλ_b = 0. The s_b are computed
deterministically from scalars that depend only on (p, κ, ξ) (Theorems 2.2 and 4.3).

## 1. Where the triangular line comes from

`prop:triangular-sde`, round k: a dependency δ modulo U_k (a − k + 1 fresh columns) and the
two-level contraction give, for every ζ of class n, weights ζδ_b(α_n + β_{cls δ_b}) ∈ P ∪ {0}.
Their value is ζ(α_ne + v), with e ∈ U_k and v = Σ_cβ_cU_c, where U_c is the class-c partial sum
of δ. So the contraction turns **one relation modulo U with coefficients of arbitrary class**
into a **P_κ-flexible line**.

The same identity holds for an RC(D; R → K) contraction, provided the relation's D-classes lie
in R. That gives a flexible line whose weights have D-classes in K (§2). The question in (A) is
therefore where a relation with *restricted* classes modulo U_k comes from, and at what cost.

## 2. Flexible-line chains [proved]

**Definition 2.1 (admissible chain).** A chain is a sequence of steps (D_t, R_t, K_t),
t = 1, …, L, such that:

- 1 = D_0 | D_1 | ⋯ | D_L = κ (equal consecutive moduli are allowed);
- 0 ∈ R_t ⊆ Z_{D_t}, 0 ∈ K_t ⊆ Z_{D_t}, K_0 = {0} ⊆ Z_1 and K_L = {0};
- R_t ⊇ π_t^{−1}(K_{t−1}), where π_t : Z_{D_t} → Z_{D_{t−1}} is reduction.

The last condition says that a coefficient whose D_{t−1}-class lies in K_{t−1} has its D_t-class
in R_t; in particular R_1 = Z_{D_1}. Examples:

- the tower of `thm:app-s2-tower`: K_t = {0} and R_t = D_{t−1}Z_{D_t};
- the union chain Z_κ → K → {0}: D_1 = D_2 = κ, R_1 = Z_κ, K_1 = K = R_2, K_2 = {0};
- the mixed chains of §4.5.

**Theorem 2.2 (flexible-line chain).** Suppose RC(D_t; R_t → K_t) contractions (α^{(t)}, β^{(t)})
are given for t = 1, …, L. Then from any **M = C(a+L+1, L+1)** columns λ_b ∈ F_p^a one computes
x ∈ (P_κ ∪ {0})^M, x ≠ 0, with Σ_b x_bλ_b = 0. The computation is deterministic given ξ and the
contractions, and uses poly(M, log p) operations: at most M eliminations of size at most
a × (a+1), at most M coordinate solves, and at most LM coset tests. κ-th roots and
`lem:app-s2-gcd`(b) then solve Σ s_b^dλ_b = 0. For L = 1 and R_1 = Z_κ this is
`prop:triangular-sde`.

*Proof.* Put f_t(m) = C(m+t+1, t+1). We prove by induction on t:

> **C(t).** For every subspace U ≤ F_p^a of codimension m and every supply of fresh columns,
> procedure P_t uses at most f_t(m) of them. It returns weights w on them with
> Σ_b w_bλ_b ∈ U, every nonzero w_b of D_t-class in K_t, and a designated b* with w_{b*} = 1.

- **t = 0.** Take m + 1 fresh columns. Their images in F_p^a/U are dependent, so there is
  δ ≠ 0 with Σδ_bλ_b ∈ U; scale one nonzero entry to 1. The class condition is empty for D_0 = 1,
  and f_0(m) = m + 1.
- **t ≥ 1.** Write (α, β) = (α^{(t)}, β^{(t)}), D = D_t, and put V_0 = U. In round k = 0, 1, …:
  - Run P_{t−1} with the subspace V_k, which has codimension m − k. It returns c^{(k)} and
    b*_k. Put e_k = Σ_bc^{(k)}_bλ_b ∈ V_k.
  - For b in the support put i(b) = cls_D(c^{(k)}_b). The D_{t−1}-class of c^{(k)}_b is in
    K_{t−1}, so i(b) ∈ π^{−1}(K_{t−1}) ⊆ R_t. Put v_k = Σ_bβ_{i(b)}c^{(k)}_bλ_b.
  - If v_k ∈ V_k, stop and put k* = k. Otherwise put V_{k+1} = V_k ⊕ F_pv_k.
- **Termination and column count.** The codimension drops by one per round, and v ∈ V holds
  trivially at codimension 0. So k* ≤ m, and the column count is at most
  Σ_{k=0}^{m} f_{t−1}(m−k) = Σ_{j=0}^{m} C(j+t, t) = C(m+t+1, t+1) by the hockey-stick identity.
- **Realisations.** For ζ ∈ F_p^× with n = cls_D(ζ) and a round k < k*, put
  x^{(k)}(ζ)_b = ζc^{(k)}_b(α_n + β_{i(b)}).
  - A nonzero entry has D-class in n + i(b) + (K − i(b) − n) = K.
  - Its value is ζ(α_ne_k + v_k), using Σ_b c_b λ_b = e_k and Σ_b β_{i(b)} c_b λ_b = v_k.
- **The stop round.** Its weights y_b = c^{(k*)}_b(α_0 + β_{i(b)}) also have classes in K (take
  ζ = 1). Their value is ρ = e_{k*} + v_{k*} ∈ V_{k*}. Moreover y_{b*} = 1, because
  c^{(k*)}_{b*} = 1 has class 0, β_0 = 0 and α_0 = 1.
- **Back substitution.** Put τ_{k*} = −ρ ∈ V_{k*}. For k = k*−1, …, 0 write
  τ_{k+1} = u + ζ_kv_k with u ∈ V_k, which is unique.
  - If ζ_k ≠ 0, add x^{(k)}(ζ_k) and put τ_k = τ_{k+1} − ζ_k(α_{n_k}e_k + v_k)
    = u − ζ_kα_{n_k}e_k ∈ V_k.
  - Otherwise put τ_k = τ_{k+1} ∈ V_k.
- **Conclusion of the step.** All supports are disjoint. The total weight w has value
  ρ + Σ_kζ_k(α_{n_k}e_k + v_k) = −τ_0 ∈ V_0 = U, its classes lie in K_t, and w_{b*} = 1. This
  proves C(t).
- **Top level.** C(L) with U = 0 gives a nonzero relation whose nonzero coefficients have
  κ-class 0, that is, lie in P_κ.
- **Cost.** Each call of P_0 is one elimination. Each round is one membership test, and each
  back-substitution step is one coordinate solve. ∎

**Corollary 2.3 (adaptive tower) [proved].** Under the hypotheses of `cor:app-s2-tower`, that is
p > max(4κ^{q+1}, 4q²κ^5) and also p > T_A(q) if q ≥ 5, any **C(a+L+1, L+1)** columns admit a
solution, where L = Ω(κ). Moreover:

- C(a+L+1, L+1) ≤ (a+1)∏_t((q_t−1)a+1). Indeed C(a+L+1, L+1) = ∏_{t=1}^{L+1}(a+t)/t, and
  (a+t)/t ≤ a + 1 ≤ (q−1)a + 1.
- For κ = 2^L the threshold is ((κ−1)²+1)², at C(a+L+1, L+1) instead of (a+1)^{L+1}.
- Numbers: at a = 10, κ = 4 and κ = 6 need 286 (the tower needs 1331 and 2541) and κ = 8 needs
  1001 (tower 14641). At a = 50, κ = 8 needs 316251 (tower 6.8·10^6).
- C(a+3, 3) is below the Schedule-2 arity (a+1)((κ−1)a+1) while a ≲ 6κ, but grows faster.

**Proposition 2.4 (what O(a²) would need) [proved].**

- Let D | κ and let an RC(κ; DZ_κ) contraction be given. Suppose an algorithm, given any
  subspace U of codimension m, returns from g(m) fresh columns a relation modulo U with
  coefficients in P_D and one coefficient equal to 1.
- Then the top level of Theorem 2.2 solves the κ-problem from Σ_{j=0}^{a} g(j) columns.
  - *Proof:* run the proof of Theorem 2.2 with P_{t−1} replaced by the algorithm. Elements of
    P_D have κ-classes in DZ_κ.
- In particular, g(m) = O(m) gives O(a²) at the threshold of that single contraction.
- For D = 2 this is a linear-arity finder for quadratic-residue relations. None is known (see
  `rem:sde-subquadratic` and its report, §6).

## 3. The bounded-excess barrier [proved]

For a matrix Λ ∈ F_p^{m×n}, let R(Λ) = {Λx : x ∈ (P_κ ∪ {0})^n} ⊆ F_p^m be its realisable set.
A **flexible line** is a line F_pw ⊆ R(Λ) with w ≠ 0. For α ∈ F_p^{Z_κ} and i ∈ Z_κ, let
n_i(α) = #{β ∈ F_p : α_ν + β ∈ Q_{−ν−i} ∪ {0} for all ν}.

**Lemma 3.2 [proved].**

(a) p ∉ E_2(κ) if and only if some nonconstant α has n_i(α) ≥ 1 for every i.

(b) Let p ∈ E_2(κ) and 1 ≤ r ≤ κ − 1. Let S ∈ F_p^{κ×r} have row 0 equal to zero and rank r. Put
Z_S = {D ∈ F_p^r : ∃u ∈ F_p, u + S_ν·D ∈ Q_{−ν} ∪ {0} ∀ν}. Then
|Z_S| ≤ 1 + (p^r − 1)(κ−1)/κ. More precisely, for every D_0 ≠ 0 there is a class i with
tD_0 ∉ Z_S for all t of class i. For r = 1, Z_α ⊆ {0} ∪ {t ≠ 0 : cls t ≠ i_α} for some class i_α.

*Proof.*

- **(a), ⇒.** Let (α, β) be a two-level contraction in normal form. Then β_i witnesses
  n_i(α) ≥ 1. If α were constant, equal to a, then a + β_i ∈ ⋂_j(Q_{−(i+j)} ∪ {0}) = {0} for
  every i, so α_0 + β_0 = 0, a contradiction.
- **(a), ⇐.** Choose β_i with α_ν + β_i ∈ Q_{−ν−i} ∪ {0} for all ν.
  - β is not constant: if β ≡ b, then α_ν + b ∈ ⋂_i(Q_{−ν−i} ∪ {0}) = {0}, so α would be
    constant.
  - So some cell α_{j_0} + β_{i_0} ≠ 0. Choose y ∈ Q_{i_0+j_0} and put α'_j = yα_{j+j_0},
    β'_i = yβ_{i+i_0}.
  - Then α'_j + β'_i ∈ Q_{i_0+j_0}(Q_{−(i+j+i_0+j_0)} ∪ {0}) = Q_{−(i+j)} ∪ {0}, and
    α'_0 + β'_0 ≠ 0. This is the argument of Proposition 2(iii) of the subquadratic report.
- **(b).** Let D_0 ≠ 0 and α' = SD_0. Then α'_0 = 0 and α' ≠ 0 (rank r), so α' is nonconstant.
  - By (a), since p ∈ E_2(κ), n_i(α') = 0 for some i.
  - For t of class i: tD_0 ∈ Z_S would give u with u + tα'_ν ∈ Q_{−ν} ∪ {0}. Then
    β = u/t satisfies β + α'_ν ∈ Q_{−ν−i} ∪ {0} for all ν, so n_i(α') ≥ 1, a contradiction.
  - The nonzero vectors split into lines {tD_0}, and each line loses (p−1)/κ of its p − 1 points.
  - For r = 1 the excluded class i_α = i depends only on α, because t·1 runs over a single line. ∎

**Theorem 3.1 (bounded excess) [proved].** Let p ∈ E_2(κ), m, h ≥ 1, n = m + h, and let Λ be
uniform in F_p^{m×n}. Put θ_r = (1 + (p^r − 1)(κ−1)/κ)/p^r. Then

  Pr[R(Λ) contains a flexible line] ≤ κp^hθ_1^n + Σ_{r=2}^{κ−1} p^{r(κ−1+h)}θ_r^n.

For fixed κ, p and h this tends to 0 exponentially in m.

*Proof.*

- **Setup.** Suppose F_pw ⊆ R(Λ). For ν ∈ Z_κ pick x^ν ∈ (P ∪ {0})^n with Λx^ν = ξ^νw, and put
  y^ν = ξ^{−ν}x^ν ∈ (Q_{−ν} ∪ {0})^n. Then Λy^ν = w for every ν.
  - Conversely, such y^ν give the line, since c ∈ Q_ν, c = ξ^νπ with π ∈ P, gives
    cy^ν ∈ (P ∪ {0})^n.
- **The difference space.** Let V = span{y^ν − y^0} and r = dim V. Then:
  - r ≥ 1, since otherwise y^0 ∈ ⋂_ν(Q_{−ν} ∪ {0})^n = {0} and w = 0;
  - r ≤ κ − 1, as V is spanned by κ − 1 differences;
  - V ⊆ ker Λ.
- **Coordinates.** Pick a basis d^1, …, d^r of V and write y^ν = y^0 + Σ_jS_{νj}d^j. Here
  S ∈ F_p^{κ×r} has row 0 zero and rank r. For each coordinate b, (u, D) = (y^0_b, D_b) with
  D_b = (d^j_b)_j satisfies u + S_ν·D_b ∈ Q_{−ν} ∪ {0}. So D_b ∈ Z_S for every b.
- **Probability.** For linearly independent d^1, …, d^r, Pr[Λd^j = 0 ∀j] = p^{−rm}, because
  Λ restricted to their span is a uniform m × r matrix.
- **r ≥ 2.** The union over at most p^{(κ−1)r} matrices S and at most |Z_S|^n tuples gives at
  most p^{(κ−1)r}(θ_rp^r)^np^{−rm} = p^{r(κ−1+h)}θ_r^n, by Lemma 3.2(b).
- **r = 1.** By Lemma 3.2(b), d = d^1 is a nonzero kernel vector whose nonzero entries avoid one
  class. The union over the κ classes and over such d gives at most
  κ(pθ_1)^np^{−m} = κp^hθ_1^n. ∎

**Corollary 3.3 (round schemes) [proved].** Consider a scheme that grows a realisable chain
0 = U_0 < U_1 < ⋯ as in Corollary 1 of the subquadratic report. Suppose its round objects are the
next m_k + h_k fresh uniform columns, fixed in advance, with h_k ≤ h. Then at p ∈ E_2(κ), each
round with m_k ≥ m_0 adds a direction with probability at most the bound of Theorem 3.1 at
(m_0, h). That is because the images of fresh columns in F_p^a/U_k are uniform and independent
of U_k, and since the bound decreases in m.

So with poly(a) columns in total, the first rounds (m = a) all fail except with probability
poly(a)·e^{−Ω(a)}. In particular, the mechanism of question (A) cannot work at p ∈ E_2(κ):

- one dependency (m + 1 columns) plus O(1) extra columns in each of L sub-steps, with any use of
  tower contractions;
- this is an object with h = 1 + O(L).

**Lemma 3.4 (an RC round must contain a relation) [proved].** Let 1 < D | κ and Λ be uniform in
F_p^{m×(m+h)}. Then

  Pr[some nonzero x ∈ (P_D ∪ {0})^{m+h} has Λx = 0] ≤ ((p−1+D)/D)^{m+h}·p^{−m}.

This is a first moment: Pr[Λx = 0] = p^{−m} for each x ≠ 0. A round that applies a last-level
RC(κ; R_L) contraction to a P_{D_{L−1}}-relation modulo U inside its object therefore needs
h ≥ (m·ln(pD/(p−1+D)) − O(1))/ln((p−1+D)/D) ≈ m·ln D/ln(p/D) columns of excess. That is linear
in m, but with a small constant, so it does not exclude O(a²).

**Remarks.**

- *What is excluded.* Theorem 3.1 excludes bounded-excess objects for every rule. It does not
  exclude objects with excess linear in m: the bound needs about h ≤ m/(κ(κ−1)ln p) − κ. So an
  O(a²) scheme is not ruled out. What is ruled out is the "O(1) extra columns per sub-step" form.
- *The constant m_0.* Evaluating the bound exactly gives m_0(4, 17, 1) = 118, m_0(4, 17, 2) = 146,
  m_0(4, 37, 2) = 187, m_0(5, 31, 2) = 368, m_0(8, 11689, 4) = 5398 and m_0(8, 12809, 4) = 5450.
  The barrier is asymptotic in a, and so is the question.
- *h = 1.* This case is Proposition 2(iii) of the subquadratic report (deterministic: a circuit
  that meets every coset has no line), and the bound reproduces it.

## 4. Prime κ: union chains by a second moment

### 4.1 One union step [proved]

**Proposition 4.1.** Let D | p − 1 and D ≥ 3. Let 0 ∈ R ⊆ Z_D with |R| = r ≥ 2, and let
0 ∈ K ⊊ Z_D with |K| = k. Put:

- c_0 = k/D;
- ĉ_s = D^{−1}Σ_{m∈K}ω^{−ms} and G = Σ_{s≠0}|ĉ_s|;
- Δ(p) = (G²√p + 2c_0G + c_0²/p)·p/(c_0²(p−1)²);
- E_0 = ((p−1)/D)(c_0(p−1)/p)^{r−1} and E_U = c_0(p−1)(c_0(p−1)/p)^{r−1};
- LHS(p) = 1/E_0 + [(1+Δ)^{r−1} − 1] + (D−1)[1/E_U + (rΔ)²e^{rΔ}/2].

If LHS(p) < 1, an RC(D; R → K) contraction with every cell nonzero exists, and a uniform β
works with probability at least 1 − LHS(p). LHS is decreasing in p, so the step exists for
every p > T_U(D; R, K) := inf{p : LHS(p) < 1}.

*Proof.*

- **Setup.** Put β_0 = 0 and draw β_i (i ∈ R∖0) independently and uniformly. Let
  A_{ij} = ⋃_{k∈K}Q_{k−i−j} for (i, j) ≠ (0, 0), and A_{00} = Q_0. Let
  X_j = {x : x + β_i ∈ A_{ij} ∀i ∈ R} and n_j = |X_j|. If every n_j ≥ 1, any α_j ∈ X_j give the
  contraction, with α_0 + β_0 = α_0 ∈ Q_0.
- **Moments.** Since |A_{ij}| = c_0(p−1) for (i, j) ≠ (0, 0), E n_j = E_U for j ≠ 0 and
  E n_0 = E_0. Independence over i gives
  E n_j² = E n_j + Σ_{x≠x'∈A_{0j}}∏_{i≠0}N_{ij}(x'−x)/p,
  with N_{ij}(c) = #{y ∈ A_{ij} : y + c ∈ A_{ij}}.
- **Correlation bound.** Expand [y ∈ A_{ij}] = Σ_sĉ_sω^{(i+j)s}χ^s(y) for y ≠ 0, which has the
  same moduli |ĉ_s|. The sum over y ∉ {0, −c} of χ^s(y)χ^t(y+c) is:
  - p − 2 for s = t = 0;
  - of modulus 1 when exactly one of s, t is 0;
  - a twisted Jacobi sum of modulus √p or 1 otherwise.

  So |N(c) − c_0²(p−2)| ≤ 2c_0G + G²√p. Writing N(c) = (|A|²/p)(1+δ(c)), this gives |δ| ≤ Δ.
- **Columns j ≠ 0.** Here N_{0j} has the same form, so
  ρ_j := E n_j²/(E n_j)² = 1/E_U + p^{−1}Σ_{c≠0}∏_{i∈R}(1+δ_{ij}(c)).
  - Expand the product to first order: ∏(1+δ_i) = 1 + Σδ_i + ρ', with
    |ρ'| ≤ (1+Δ)^r − 1 − rΔ ≤ (rΔ)²e^{rΔ}/2.
  - Exactly, Σ_{c≠0}δ_{ij}(c) = 1 − p/|A| < 0, because Σ_{c≠0}N(c) = |A|(|A|−1).
  - Hence ρ_j ≤ 1/E_U + 1 + (rΔ)²e^{rΔ}/2.
- **Column 0.** Bound the weights of the pairs in Q_0 by 1:
  ρ_0 ≤ 1/E_0 + (1+Δ)^{r−1}.
- **Union bound.** Pr[n_j = 0] ≤ 1 − 1/ρ_j ≤ ρ_j − 1 by Cauchy–Schwarz. Summing over the D
  columns gives LHS(p).
- **Monotonicity.** Each of the three terms of Δ is decreasing for p ≥ 3, and E_0, E_U are
  increasing. ∎

*Remark.* For K = {0} this bound is cruder than threshold-6 Proposition 3.2, which uses exact
cyclotomic numbers (`union_threshold.py sanity`). We use that proposition for the last step.

**Lemma 4.2 (closed form) [proved].** Let D ≥ 4, 2 ≤ r ≤ D, H = G² + 0.2G + 0.1 and

  P = max(1 + 4.05D·c_0^{−r}, 11.6r²D·H²c_0^{−4}, 100r).

Then LHS(p) < 0.73 for p ≥ P. If K = {0, …, k−1}, then G ≤ 1 + ln D and H ≤ (1.2 + ln D)².

*Proof.*

- **Main terms.** Since p ≥ 100r, (1 − 1/p)^{r−1} ≥ 0.99. So
  1/E_0 + (D−1)/E_U ≤ (Dc_0 + D − 1)/(0.99(p−1)c_0^r) < 2D/(0.99(p−1)c_0^r) ≤ 0.4988.
- **Bound on Δ.** Since p ≥ 100 and c_0 ≤ 1, Δ ≤ 1.0203H/(c_0²√p). With x := rΔ this gives
  x ≤ 0.2996/√D ≤ 0.15.
- **Correlation terms.** Then (1+Δ)^{r−1} − 1 ≤ e^x − 1 ≤ 1.162x ≤ 0.175, and
  (D−1)x²e^x/2 ≤ 0.0523.
- **Total.** The sum is below 0.73.
- **Intervals.** |Σ_{m<k}ω^{−ms}| = |sin(πks/D)/sin(πs/D)| ≤ D/(2 min(s, D−s)), because
  sin πx ≥ 2x on [0, 1/2]. So G ≤ Σ_{u≤D/2}1/u ≤ 1 + ln(D/2).
- **Bound on H.** (1+L)² + 0.2(1+L) + 0.1 ≤ (1.2+L)² for L ≥ 0. ∎

Checked [float] (`union_threshold.py sanity`): P ≥ T_U and LHS(P) < 1 for all 4 ≤ D ≤ 40 and
2 ≤ k < D. Also G − (1 + ln D) ≤ −1.43 for intervals with D < 200.

### 4.2 Union chains [proved]

**Lemma 4.5 (union steps fail only at E_2) [proved; threshold-6 Lemma 7.1].** For any R and K,
E(D; R → K) ⊆ E_2(D). Restricting the rows of a two-level contraction to R gives the step,
since Q°_{−(i+j)} ⊆ Q°_{K−i−j}.

**Theorem 4.3 (two-step union chain).** Let κ ≥ 4, 2 ≤ k ≤ κ−1 and K = {0, …, k−1}. For every
prime p ≡ 1 (mod κ) with

  p > Θ_2(κ, k) := max(T_U(κ; Z_κ, K), min(W(κ, k), T_R(κ, k))),

the chain Z_κ → K → {0} has its contractions. So any C(a+3, 3) columns admit a solution of
`eq:app-s2-target` (Theorem 2.2), and so do (a+1)((κ−1)a+1)((k−1)a+1) columns by the
non-adaptive Lemma 2.2 of threshold-6. Moreover

  Θ_2(κ, k) ≤ max(1 + 4.05κ(κ/k)^κ, 11.6κ³(κ/k)^4(1.2 + ln κ)^4, 100κ, 4κ^{k+1}, 4k²κ^5).

*Proof.*

- **Step 1.** It is Proposition 4.1 with D = κ and R = Z_κ, and Lemma 4.2 gives its closed form.
- **Step 2.** It is RC(κ; K), with rows R = K (not a subgroup). It holds for
  p > min(W(κ, k), T_R(κ, k)) by threshold-6 Propositions 3.1–3.2, and for
  p ≥ max(4κ^{k+1}, 4k²κ^5) by `prop:app-s2-step-threshold`(ii), which is stated for any
  0 ∈ R ⊆ Z_D with |R| ≤ D (R need not be a subgroup).
- **Admissibility.** Step 1 outputs classes in K = R_2. ∎

**Corollary 4.4 (asymptotics) [proved].** For κ ≥ 16 put k = ⌈κ ln ln κ/ln κ⌉. Then
2 ≤ k ≤ κ−1 and **Θ_2(κ, k) ≤ 4.05κ²(ln κ)^κ**. For κ ≥ 19 this is below κ^{κ/2}.

*Proof.*

- **Ratio.** κ/k ≤ ln κ/ln ln κ ≤ ln κ, since ln ln κ ≥ 1 for κ ≥ 16.
- **Term 1.** 1 + 4.05κ(ln κ)^κ ≤ 4.05κ²(ln κ)^κ.
- **Term 4.** k < κ ln ln κ/ln κ + 1 gives κ^{k+1} < κ²(ln κ)^κ.
- **Term 5.** 4k²κ^5 ≤ 4κ^7 ≤ 4κ²(ln κ)^κ, since κ ln ln κ ≥ 5 ln κ at κ = 16 and the
  difference increases.
- **Term 2.** It is at most 11.6κ³(1.2 + ln κ)^8, which is at most 4κ²(ln κ)^κ:
  2.9κ(1.2 + ln κ)^8 ≤ (ln κ)^κ holds at κ = 16 (14.9 < 16.3 in logarithms), and the
  difference of logarithms has positive derivative.
- **Term 3.** 100κ is trivially smaller.
- **Below κ^{κ/2}.** ln 4.05 + 2 ln κ + κ ln ln κ < (κ/2)ln κ holds at κ = 19
  (27.8 < 27.97). The difference has positive and increasing derivative for κ ≥ 19. ∎

So Θ_2(κ) = κ^{κ·ln ln κ/ln κ + O(1)}. Compare κ^{(κ+1)/2}, near which E_2(κ) is believed to end,
and T_A(κ) > (κ−1)κ^κ, the proved two-level threshold.

### 4.3 Values [float] (`union_threshold.py table` → `union_table.out`)

- Θ_2 is the best k for intervals. Over all K ∋ 0 the optimum is the same for κ = 5 and κ = 7
  (`union_misc.out`, smallsets).
- Θ_3 is the best three-step chain Z_κ → [0, k_1) → [0, k_2) → {0} with C(a+4, 4) columns. Its
  middle step is Proposition 4.1 with R = [0, k_1).

| κ | k | Θ_2 | (k_1, k_2) | Θ_3 | (κ−1)κ^κ < T_A | κ^{κ/2} | log_κ Θ_2 |
|---|---|---|---|---|---|---|---|
| 5 | 3 | 3781 | (3,2) | 1217 | 1.25·10^4 | 55.9 | 5.12 |
| 7 | 3 | 30823 | (3,2) | 15133 | 4.94·10^6 | 907 | 5.31 |
| 11 | 4 | 1.16·10^6 | (5,2) | 3.80·10^5 | 2.85·10^12 | 5.3·10^5 | 5.82 |
| 13 | 5 | 7.42·10^6 | (6,3) | 1.06·10^6 | 3.6·10^15 | 1.7·10^7 | 6.17 |
| 17 | 6 | 1.08·10^9 | (8,4) | 9.73·10^6 | 1.3·10^22 | 2.9·10^10 | 7.34 |
| 19 | 7 | 1.61·10^10 | (9,4) | 4.08·10^7 | 3.6·10^25 | 1.4·10^12 | 7.98 |
| 23 | 8 | 1.72·10^12 | (11,5) | 7.76·10^8 | 4.6·10^32 | 4.6·10^15 | 8.99 |
| 31 | 10 | 6.83·10^16 | (15,7) | 8.26·10^11 | 5.1·10^47 | 1.3·10^23 | 11.29 |
| 47 | 14 | 3.15·10^26 | (22,9) | 3.41·10^17 | 1.8·10^80 | 2.0·10^39 | 15.85 |
| 61 | 18 | 1.68·10^34 | – | – | 4.8·10^110 | 2.8·10^54 | 19.17 |

Additional checks:

- Every κ from 4 to 31, together with 37, 41, 43, 47, 53, 59, 61 and 64, is in `union_table.out`.
  At every one of them Θ_2 < (κ−1)κ^κ; for κ ≥ 13, Θ_2 < κ^{κ/2}; for κ ≥ 11, Θ_3 < κ^{κ/2}.
- The asymptotic bound is checked at κ = 16, …, 256 (`union_misc.out`, asym).
- `moment_check.out` [exact sampling]: at primes just above T_U, the empirical failure rate of a
  uniform β is at most 0.01, against the bound LHS(p) ∈ [0.88, 1.0]. That is consistent, and the
  bound is loose.

### 4.4 Exact exceptional sets at κ = 5, 7 [exact]

By Lemma 4.5, a chain whose steps all have modulus κ can fail only at p ∈ E_2(κ). E_2(5) and
E_2(7) (56 primes) are known exactly, so each chain was decided at those primes only, by the
complete DFS of `rectu.c` (`union_exact.py` → `union_exact.out`). That is 534 FEASIBLE decisions,
each witness re-checked by the pow-based `check_pair`, and 33 INFEASIBLE decisions.

| κ | chain | fails exactly at |
|---|---|---|
| 5 | Z_5 → {0,1} → {0} | {11} |
| 5 | Z_5 → {0,1,2} → {0} | {11, 31, 41, 61} |
| 5 | Z_5 → {0,1,2} → {0,1} → {0} | {11} |
| 7 | Z_7 → {0,1,2,3} → {0} (threshold-6 chain A) | {29,43,71,113,127,197,211,239,337,631} |
| 7 | Z_7 → {0,1,2} → {0} | {29, 43, 71, 113, 127} |
| 7 | Z_7 → {0,1,2} → {0,1} → {0} | **{29, 43, 71}** |
| 7 | Z_7 → {0,1,3} → {0,1} → {0} | {29, 43, 71} |

So at κ = 7 the quartic chain covers 53 of the 56 primes of E_2(7), and every other
p ≡ 1 (mod 7). These are unconditional finite statements: they do not need Θ_3. The thresholds of
§4.3 lie above every failing prime, as they must.

### 4.5 All admissible chains at the remaining primes [exact]

`reach.py` explores the graph whose nodes are (D, K), with D | κ and 0 ∈ K ⊆ Z_D. An edge
(D, K) → (D', K') means that RC(D'; π^{−1}(K) → K') is feasible. Every edge query is a complete
DFS, with FEASIBLE witnesses re-checked. Pruning uses the monotonicity of feasibility: fewer rows
or a larger target is easier.

A solution chain exists if and only if (κ, {0}) is reachable from (1, {0}). The search was run at
every prime that threshold-6 left uncovered (`reach_general.out`):

| κ | uncovered by threshold-6 | now covered (chain found) | no admissible chain at all |
|---|---|---|---|
| 4 | 5, 13 | – | 5, 13 |
| 5 | 11 | – | 11 |
| 6 | 7,13,19,31,43,67 | 67: (1,{0})→(2,{0})→(6,{0,5})→(6,{0}) | 7, 13, 19, 31, 43 |
| 7 | 29,43,71 (after §4.4) | 43: Z_7→{0,3,4,5,6}→{0,4}→{0,5}→{0} | 29, 71 |
| 8 | 17,41,73,89,137,233 | 89 (4 steps), 137: …→(8,{0,6})→(8,{0}), 233: …→(8,{0,7})→(8,{0}) | 17, 41, 73 |
| 9 | 19,37,73,109,127,163,181,199,307,433 | 109, 127, 163, 181, 199, 307 (5 nodes each, e.g. 109: (1,{0})→(3,{0,2})→(9,{0,7,8})→(9,{0,7})→(9,{0})), 433: (1,{0})→(3,{0,2})→(9,{0,6})→(9,{0}) | 19, 37, 73 |

Each new chain was run end to end with exact checks (`adaptive_extra.out`). At such a prime p no
chain in the framework of Definition 2.1 exists, though other constructions are not excluded.
All the primes in the last column lie in E_2(κ), as they must: for p ∉ E_2(κ) the one-step
chain RC(κ; Z_κ) exists.

### 4.6 Routes B.1–B.3

**Proposition 4.6 (refinements project; route B.2) [proved].** Let κ | D' | p − 1. Suppose
RC(D'; R → K) holds with R mod κ = Z_κ and K mod κ = {0}. Then p ∉ E_2(κ).

- *Consequence 1.* E_2(κ) ⊆ E_2(D') (take R = Z_{D'}, K = {0}).
- *Consequence 2.* For prime κ, every tower (K_t = {0}) for any κ' with κ | κ' fails at every
  p ∈ E_2(κ). At the first t with κ | D_t, gcd(D_{t−1}, κ) = 1, so R_t = D_{t−1}Z_{D_t} covers
  every residue mod κ.

*Proof.*

- **Lifts.** Choose i_s ∈ R with i_s ≡ s (mod κ), with i_0 = 0, and j_s = s ∈ Z_{D'}. Put
  α'_s = α_{j_s} and β'_s = β_{i_s}.
- **Cells.** Since κ | D', Q^{(D')}_m ⊆ Q^{(κ)}_{m mod κ}. With k ≡ 0 this gives
  α'_s + β'_{s'} ∈ {0} ∪ Q^{(κ)}_{−s−s'}.
- **Normal form.** α'_0 + β'_0 = α_0 + β_0 ∈ Q^{(D')}_0 ⊆ Q^{(κ)}_0 is nonzero. ∎

*Exact check* (`projection_check.out`): RC(10; {0,2,4,6,8}) is INFEASIBLE at all nine primes of
E_2(5). It is feasible near 10^6, with four witnesses checked. It is also infeasible at the small
controls 191–331, because a five-row step at modulus 10 needs p of order 10^5–10^6.

Refinement therefore adds nothing for towers. Union targets (K mod κ ≠ {0}) escape the
projection, and they already work at modulus κ (§4.2).

**Proposition 4.7 (extension fields; route B.1) [proved].** Let κ be prime, F = F_{p^k}, G a
generator of F^× and ξ = G^N with N = (p^k−1)/(p−1).

- *Classes.* For y = ξ^e ∈ F_p^×, cls_F(y) = Ne ≡ ke (mod κ), because N = Σ_{l<k}p^l ≡ k.
- *κ ∤ k.* (α, β) ∈ F_p^{2κ} is a contraction over F iff (α_{kj}, β_{ki}) is one over F_p.
  - The F_p-class of α_j + β_i is k^{−1}(−(i+j)).
- *κ | k and κ ≥ 3.* No contraction over F has all its cells in F_p.
  - Every cell with i + j ≢ 0 must vanish, so for each j, β_i = −α_j for all i ≠ −j.
  - Since κ ≥ 3, any two such index sets meet, so α is constant and then α_0 + β_0 = 0.
- *Descent.* In Lemma 2.2 of threshold-6 and Theorem 2.2 here, with F_p input data, an output
  c'_b = η(α_j + β_i)c_b lies in F_p iff the cell does.
  - If all cells lie in F_p, translating by β_0 makes α and β themselves F_p-valued.
  - So F gives no new F_p-valued schedules.
  - Weights outside F_p cannot be used by `prop:descent`, which needs s_b ∈ F_p. The trace is
    additive but does not preserve P; the norm preserves classes but is not additive. [The
    last sentence is argued.]

**Lemma 4.8 (rigidity of full collapse; route B.3) [proved].** Let μ be a primitive κ-th root of
unity, e a unit and f ∈ Z_κ. Suppose α_j + β_i = Bμ^{fi}F(ej − fi) for all i, j, so that all κ²
cells are governed by the κ values F(d).

- If f is a unit, then F(d) = Cμ^d + c'. Hence α_j = BCμ^{ej} + s and β_i = Bc'μ^{fi} − s: the
  family is geometric, with one essential parameter λ = C/c'.
- Its contraction conditions are κ coset conditions on 1 + λμ^d, for d ∈ Z_κ.
- With c = ind(μ) mod κ and f = −(c + e^{−1})^{−1}, they are consistent with the target pattern
  −(i+j).

*Proof.*

- **Recurrence.** α_j + β_i − (α_j + β_0) is independent of j. So
  μ^fF(d) − F(d+f) = const for all d.
- **Solution.** This first-order recurrence along the generator f of Z_κ has the two-parameter
  solution Cμ^d + c'.
- **Classes.** The class identity follows by substituting j = e^{−1}(d + fi). ∎

*Conclusion [argued].* A one-variable problem with κ distinct shifts has expected count of order
p/κ^{κ−1}. Weil certifies it only for p ≳ κ^{2κ}. Collapsing designs are therefore *worse* than
T_A, and partial collapses meet the §6.2 square-root barrier of threshold-6.

## 5. Tests (all in `2026-11-05-rees-threshold-7/`)

### 5.1 Theorem 2.2 end to end (`adaptive_chain.py demo` → `adaptive_demo.out`, `adaptive_extra.out`)

- **What the solver does.** It uses exactly C(a+L+1, L+1) columns, half random and half
  adversarial: zero, repeated, unit and hyperplane columns. It runs the nested triangular
  recursion.
- **Checks, with pow() and not the index table:**
  - every weight is a κ-th power;
  - the weights form a nonzero relation;
  - Σu_b^κλ_b = 0 after κ-th roots;
  - columns used ≤ C(a+L+1, L+1);
  - every step pair satisfies all cells (`check_pair`).
- **Pairs.** They come from random β (the second-moment design), with a complete DFS fallback.
- **Results.** 35 + 21 "runs OK" lines (one κ = 9 line is a repeat), about 750 solver runs in all, with a ≤ 4. In
  detail:
  - κ = 4, chain 2|4: p = 17, 37, 53 ∈ E_2(4), and the controls 41, 61.
  - κ = 6, chain 3|6: p = 37, 61, 73, 97, 181, 379, 859, all ∈ E_2(6).
  - κ = 6, chain 2|6: p = 181, 379, 859. At 37, 61, 73 and 97 its step RC(6; {0,2,4}) is
    infeasible, in agreement with threshold-6 §5.1.
  - κ = 6, mixed chain: p = 37, 67.
  - κ = 8, chain 2|4|8: p = 97, 113, 193, 257, 11689, 12809, all ∈ E_2(8). 12809 is confirmed
    INFEASIBLE for the two-level problem in `2026-11-02-rees-schedules/small-prime/dfs2b_k8_hi_q3.out`.
  - κ = 8, mixed chains: p = 89, 137, 233.
  - κ = 9, mixed chains found by `reach.py` (§4.5): p = 109, 127, 163, 181, 199, 307, 433.
  - κ = 5, union chains: p = 31, 41, 61, 71, 101, 131, 151, 181 (two-step, K = {0,1}), and
    31, 181 (three-step).
  - κ = 7, union chains: p = 281, 379, 421, 1009, 3221 (chain A), 113, 197, 337, 3221
    (three-step), and 43 (four-step).
  - The triangular solver itself (L = 1) at κ = 4, p = 41.
- **Expected failures.** κ = 5, p = 11 and κ = 4, p = 13 report "no pair", correctly.

### 5.2 Brute-force re-derivations (`barrier.py e2`, `barrier.py zs` → `barrier_e2_zs.out`)

- **Lemma 3.2(a) as a decision procedure.** Exhaustive over α with α_0 = 0, it gives:
  - E_2(3) ∩ [7, 80] = ∅;
  - E_2(4) ∩ [5, 61] = {5, 13, 17, 29, 37, 53};
  - E_2(5) ∩ [11, 31] = {11, 31}.

  All three agree with the paper. The code is independent of every earlier DFS.
- **Lemma 3.2(b).**
  - At r = 1, max|Z_α| = 9, 28 and 40 at p = 17, 37 and 53, against the bound 13, 28 and 40. So
    the bound is attained at 37 and 53.
  - At p = 41 and 61 (not in E_2) the maximum is p.
  - At r = 2 (30 random S) the maximum is 61 ≤ 217 at p = 17 and 307 ≤ 1027 at p = 37.

### 5.3 Exact realisable sets (`barrier.py lines`, `barrier.py circuits`)

- **Circuits.** Circuits whose dependency meets all κ cosets have **no** line at p ∈ E_2:
  0 of 8 at each of κ = 4, p = 17, 37, 53, and κ = 5, p = 31. At p = 41 and 61 every such
  circuit has one (8 of 8).
- **Random objects** (`barrier_lines.out`), at κ = 4, p = 17, with h = 1:
  - m = 2: 11 of 12 have a line;
  - m = 3: 8 of 12;
  - m = 4: 2 of 12 — only circuits that miss a coset.
- **Excess 2 and 3.** With h = 2, 11 or 12 of 12 have a line up to m = 5. So Theorem 3.1 is
  only asymptotic: at m ≤ 5, kernel-2 objects are flexible, as §4 of the subquadratic report
  also found. The computation cannot reach m ≈ 146.

### 5.4 Other

- `union_exact.out` (§4.4), `reach_general.out` and `reach.out` (§4.5).
- `projection_check.out` (Proposition 4.6).
- `moment_check.out` (Proposition 4.1).
- `union_table.out` and `union_misc.out` (§4.3).

## 6. Checks against the known exceptional primes

- **E_2(5)** = {11, 31, 41, 61, 71, 101, 131, 151, 181}.
  - Union chains cover all of them except 11 (§4.4), and no admissible chain exists at 11
    (§4.5).
  - The claimed thresholds 1217 and 3781 exceed 181.
  - Nothing here claims p ∉ E_2(5) for any p.
- **E_2(7)** (56 primes, maximum 3221).
  - The three-step chain covers all of them except 29, 43 and 71; the four-step chain covers 43.
  - The claimed thresholds 15133 and 30823 exceed 3221, so no chain-exceptional prime can lie
    above them.
- **E_2(8) ∋ 11689, 12809.**
  - Both are covered by the 2|4|8 adaptive tower above its threshold 2500 (tested end to end).
  - At both, Theorem 3.1 forbids bounded-excess triangular rounds, asymptotically in a.
  - The union-chain thresholds Θ_2(8) = 6.8·10^4 and Θ_3(8) = 3.3·10^4 exceed max E_2(8) ≤ 20000,
    as they must.
- **Lemma 3.2(a)** reproduces E_2(4) ∩ [5, 61] and E_2(5) ∩ [11, 31] exactly.
- **No threshold here is a threshold for E_2(κ).** The two-level square gap is untouched.

## 7. Proposed LaTeX (AI-checked, pending human review; not applied)

### 7.1 New subsection for `appendix-schedule2.tex`, immediately after Remark `rem:app-s2-tower-scope` (end of subsection `app:s2-tower`) and before `\subsection{What is and is not shown}` (`app:s2-scope`)

```latex
\subsection{Flexible-line chains and union targets}
\label{app:s2-chains}

\noindent\textbf{Status: AI-checked, pending human review} (\file{research/audits/reviews/2026-11-05-rees-threshold-7.md}). Like Subsection~\ref{app:s2-tower}, this subsection is not used by Theorem~\ref{thm:power-sde}, Proposition~\ref{prop:decoupled-sde}, Remark~\ref{rem:combined-schedule} or the tables, and it changes neither $E_2(\kappa)$ nor $E_W(c)$.

For $D \mid p-1$, $0 \in R \subseteq \mathbb{Z}_D$ and $0 \in K \subseteq \mathbb{Z}_D$, an $\mathrm{RC}(D;R\to K)$ contraction is a pair $\alpha \in \Fp^{\mathbb{Z}_D}$, $\beta \in \Fp^{R}$ with $\alpha_j + \beta_i \in \{0\}\cup\bigcup_{k\in K}Q^{(D)}_{k-i-j}$ for all $i \in R$, $j \in \mathbb{Z}_D$, and $\alpha_0+\beta_0 \in Q^{(D)}_0$; translating and scaling by $\alpha_0+\beta_0$ we take $\alpha_0 = 1$, $\beta_0 = 0$. For $K = \{0\}$ it is $\mathrm{RC}(D;R)$. A \emph{chain} is a sequence of steps $(D_t,R_t,K_t)$, $t = 1,\dots,L$, with $1 = D_0 \mid D_1 \mid \cdots \mid D_L = \kappa$, $K_0 = K_L = \{0\}$ and $R_t \supseteq \{x \in \mathbb{Z}_{D_t} : x \bmod D_{t-1} \in K_{t-1}\}$. The tower of Theorem~\ref{thm:app-s2-tower} is the chain with every $K_t = \{0\}$; the \emph{union chain} $\mathbb{Z}_\kappa \to K \to \{0\}$ has $D_1 = D_2 = \kappa$, $R_1 = \mathbb{Z}_\kappa$, $K_1 = R_2 = K$.

\begin{theorem}[flexible-line chains]
\label{thm:app-s2-chain}
If $\mathrm{RC}(D_t;R_t\to K_t)$ contractions are given for $t = 1,\dots,L$, then from any $\binom{a+L+1}{L+1}$ columns $\lambda_b \in \Fp^a$ one computes, deterministically given $\xi$ and the contractions and with $\poly(\binom{a+L+1}{L+1},\log p)$ operations, a nonzero $x \in (Q_0\cup\{0\})^M$ with $\sum_bx_b\lambda_b = 0$, and hence a solution of~\eqref{eq:app-s2-target}. For $L = 1$ this is Proposition~\ref{prop:triangular-sde}.
\end{theorem}

\begin{proof}
Put $f_t(m) = \binom{m+t+1}{t+1}$. We show that for every subspace $U$ of codimension $m$, procedure $P_t$ uses at most $f_t(m)$ fresh columns and returns weights $w$ with $\sum_bw_b\lambda_b \in U$, every nonzero $w_b$ of $D_t$-class in $K_t$, and $w_{b^\ast} = 1$ for some $b^\ast$. For $t = 0$ take a dependence of $m+1$ columns modulo $U$ with one entry scaled to $1$. For $t \ge 1$ let $(\alpha,\beta)$ be the step-$t$ pair and $V_0 = U$. In round $k$ run $P_{t-1}$ with $V_k$, getting $c$ with $e = \sum_bc_b\lambda_b \in V_k$; the $D_t$-classes $i(b)$ of its coefficients lie in $R_t$ by the chain condition. Put $v = \sum_b\beta_{i(b)}c_b\lambda_b$; stop if $v \in V_k$, and otherwise put $V_{k+1} = V_k \oplus \Fp v$. At most $m+1$ rounds occur, using at most $\sum_{j=0}^{m}f_{t-1}(j) = f_t(m)$ columns. For $\zeta$ of $D_t$-class $n$ the weights $\zeta c_b(\alpha_n+\beta_{i(b)})$ have $D_t$-classes in $K_t$ and value $\zeta(\alpha_ne+v)$, with $e \in V_k$. The stop round with $\zeta = 1$ has value $\rho \in V_{k^\ast}$ and the weight $1$ at the designated column of its input. Back substitution as in the proof of Proposition~\ref{prop:triangular-sde}, with $\tau = -\rho$ and the coordinate $\zeta_k$ of $\tau$ along $v_k$ in $V_k \oplus \Fp v_k$, ends with $\tau \in V_0 = U$, and the weights, on disjoint supports, have value $-\tau \in U$. At $t = L$ with $U = 0$ the weights form a nonzero relation with every nonzero coefficient in $P_\kappa = Q_0$.
\end{proof}

For the tower of Corollary~\ref{cor:app-s2-tower} this lowers the arity from $(a+1)\prod_t((q_t-1)a+1)$ to $\binom{a+L+1}{L+1}$ at the same thresholds, but the degree $L+1$ is unchanged.

\begin{proposition}[union steps]
\label{prop:app-s2-union-step}
Let $D \mid p-1$, $D \ge 4$, $0 \in R \subseteq \mathbb{Z}_D$ with $|R| = r \ge 2$, and $0 \in K \subsetneq \mathbb{Z}_D$ with $|K| = k$. Put $c_0 = k/D$, $G = \sum_{s \ne 0}|D^{-1}\sum_{m \in K}\omega^{-ms}|$ and $H = G^2 + 0.2G + 0.1$. If
\[
  p \ge \max\bigl(1 + 4.05\,D\,c_0^{-r},\ 11.6\,r^2D\,H^2c_0^{-4},\ 100r\bigr),
\]
then an $\mathrm{RC}(D;R\to K)$ contraction with every entry nonzero exists, and a uniform $\beta$ extends to one with probability at least $1/4$. For $K = \{0,\dots,k-1\}$ one has $G \le 1+\ln D$ and $H \le (1.2+\ln D)^2$.
\end{proposition}

\begin{proof}
Draw $\beta_0 = 0$ and $\beta_i$ ($i \in R\setminus\{0\}$) uniformly, let $A_{ij} = \bigcup_{k\in K}Q^{(D)}_{k-i-j}$ for $(i,j) \ne (0,0)$, $A_{00} = Q^{(D)}_0$, $X_j = \{x : x+\beta_i \in A_{ij}\ \forall i \in R\}$ and $n_j = |X_j|$. By independence, $\mathbb{E}[n_j^2] = \mathbb{E}[n_j] + \sum_{x\ne x'\in A_{0j}}\prod_{i\ne0}N_{ij}(x'-x)/p$ with $N_{ij}(c) = \#\{y \in A_{ij} : y+c \in A_{ij}\}$. Expanding the indicator of $A_{ij}$ in the characters $\chi^{s\kappa/D}$ and using Jacobi sums, $|N_{ij}(c) - c_0^2(p-2)| \le 2c_0G + G^2\sqrt p$, so $N_{ij}(c) = (|A|^2/p)(1+\delta_{ij}(c))$ with $|\delta| \le \Delta = (G^2\sqrt p + 2c_0G + c_0^2/p)\,p/(c_0^2(p-1)^2)$, and $\sum_{c\ne0}\delta_{ij}(c) = 1 - p/|A| < 0$. For $j \ne 0$ this gives $\mathbb{E}[n_j^2]/\mathbb{E}[n_j]^2 \le 1/\mathbb{E}[n_j] + 1 + (r\Delta)^2e^{r\Delta}/2$, and for $j = 0$ it gives $\le 1/\mathbb{E}[n_0] + (1+\Delta)^{r-1}$. By Cauchy--Schwarz and a union bound over the $D$ columns, some $X_j$ is empty with probability at most $\mathrm{LHS}(p) = 1/\mathbb{E}[n_0] + (1+\Delta)^{r-1} - 1 + (D-1)\bigl(1/\mathbb{E}[n_1] + (r\Delta)^2e^{r\Delta}/2\bigr)$, where $\mathbb{E}[n_0] = \tfrac{p-1}{D}(c_0\tfrac{p-1}{p})^{r-1}$ and $\mathbb{E}[n_1] = c_0(p-1)(c_0\tfrac{p-1}{p})^{r-1}$. Under the stated bound the first two terms contribute at most $0.4988$ and the others at most $0.2266$, so $\mathrm{LHS}(p) < 3/4$. For intervals, $|\sum_{m<k}\omega^{-ms}| \le D/(2\min(s,D-s))$ gives $G \le \sum_{u \le D/2}1/u \le 1+\ln D$.
\end{proof}

\begin{corollary}[cubic arity for every $\kappa$, including prime $\kappa$]
\label{cor:app-s2-union-chain}
Let $\kappa \ge 4$, $2 \le k \le \kappa-1$ and $K = \{0,\dots,k-1\}$. For every prime $p \equiv 1 \pmod\kappa$ with
\[
  p > \Theta_2(\kappa,k) \coloneqq \max\bigl(1 + 4.05\,\kappa(\kappa/k)^\kappa,\ 11.6\,\kappa^3(\kappa/k)^4(1.2+\ln\kappa)^4,\ 100\kappa,\ 4\kappa^{k+1},\ 4k^2\kappa^5\bigr),
\]
any $\binom{a+3}{3}$ columns admit a solution of~\eqref{eq:app-s2-target}. For $\kappa \ge 16$ and $k = \lceil\kappa\ln\ln\kappa/\ln\kappa\rceil$, $\Theta_2(\kappa,k) \le 4.05\,\kappa^2(\ln\kappa)^\kappa = \kappa^{\kappa\ln\ln\kappa/\ln\kappa + O(1)}$, which is below $\kappa^{\kappa/2}$ for $\kappa \ge 19$.
\end{corollary}

\begin{proof}
Apply Theorem~\ref{thm:app-s2-chain} to the union chain $\mathbb{Z}_\kappa \to K \to \{0\}$: step~$1$ is Proposition~\ref{prop:app-s2-union-step} with $D = \kappa$ and $R = \mathbb{Z}_\kappa$, and step~$2$ is $\mathrm{RC}(\kappa;K)$, which holds for $p \ge \max(4\kappa^{k+1},4k^2\kappa^5)$ by Proposition~\ref{prop:app-s2-step-threshold}(ii), which allows any $0 \in R \subseteq \mathbb{Z}_D$. The asymptotic bound uses $\kappa/k \le \ln\kappa$ and $\kappa^{k+1} \le \kappa^2(\ln\kappa)^\kappa$, and the remaining terms are smaller for $\kappa \ge 16$.
\end{proof}

\begin{remark}[values, small primes and a barrier]
\label{rem:app-s2-chains-scope}
Evaluating the criterion of the proof of Proposition~\ref{prop:app-s2-union-step} and the thresholds of Proposition~\ref{prop:app-s2-step-threshold} numerically (AI-computed, pending human review) gives cubic-arity thresholds $3781$, $30823$, $1.16\cdot10^6$ and $7.42\cdot10^6$ for $\kappa = 5, 7, 11, 13$, and quartic-arity thresholds $1217$, $15133$, $3.80\cdot10^5$ and $1.06\cdot10^6$ for the three-step chains $\mathbb{Z}_\kappa \to K_1 \to K_2 \to \{0\}$, against $T_A(\kappa) > (\kappa-1)\kappa^\kappa$. A step at modulus $\kappa$ can fail only at $p \in E_2(\kappa)$, since restricting rows of a two-level contraction gives it, so exhaustive searches at the primes of $E_2(5)$ and $E_2(7)$ (finite computations, AI-checked, pending human review) show that the chain $\mathbb{Z}_7 \to \{0,1,2\} \to \{0,1\} \to \{0\}$ works at every prime $p \equiv 1 \pmod 7$ except $29$, $43$ and $71$, that a four-step union chain covers $43$, and that no chain in the sense above exists at $p = 29, 71$ for $\kappa = 7$, at $p = 11$ for $\kappa = 5$, or at $p = 5, 13$ for $\kappa = 4$. None of this bounds $E_2(\kappa)$: the square gap of Remark~\ref{rem:two-level-threshold-size} concerns the two-level construction itself. Conversely, chains of length $L \ge 2$ have arity of degree $L+1 \ge 3$, and at quadratic arity one cannot do better by adding a bounded number of columns to each dependency of Proposition~\ref{prop:triangular-sde}: for $p \in E_2(\kappa)$ and uniform $\Lambda \in \Fp^{m\times(m+h)}$, the set $\{\Lambda x : x \in (Q_0\cup\{0\})^{m+h}\}$ contains a line through $0$ with probability at most $\kappa p^h\theta_1^{m+h} + \sum_{r=2}^{\kappa-1}p^{r(\kappa-1+h)}\theta_r^{m+h}$, where $\theta_r = 1 - (1-p^{-r})/\kappa$, which tends to $0$ as $m \to \infty$ for fixed $h$.
\end{remark}
```

### 7.2 Sentence for Remark `rem:two-level-threshold-size` in `main.tex`

Insert after "Closing this square gap is open.", and after the tower sentence if the integrator
adopts threshold-6 §8.2:

"The gap can also be bypassed for every $\kappa \ge 4$, prime or not, at cubic arity
(AI-checked, pending human review). A chain of union-target refinements, whose first step only
asks each entry to lie in one of $k$ cosets, gives a solution from $\binom{a+3}{3}$ columns for
every prime $p \equiv 1 \pmod\kappa$ above
$\Theta_2(\kappa) \le 4.05\,\kappa^2(\ln\kappa)^\kappa = \kappa^{\kappa\ln\ln\kappa/\ln\kappa+O(1)}$
(for example $3781$ for $\kappa = 5$ and $30823$ for $\kappa = 7$;
Appendix~\ref{app:s2-chains})."

## 8. What remains

1. **O(a²) at a polynomial threshold.** Open. By Proposition 2.4 it would follow from a
   linear-arity finder of P_D-relations modulo U for some proper divisor D. By Theorem 3.1 it
   needs objects of excess growing at least like m/(κ² ln p) at E_2 primes. The cleanest
   test case is κ = 4 at p ∈ {17, 37, 53}: is there a polynomial O(a²) scheme there at all?
2. **The two-level square gap.** Untouched.
3. **Theorem 3.1 constants.** The p^{(κ−1)r} count over S is crude. A bound with
   m_0 = O(κ log p) would make the barrier visible in exact computations. Only the r = 1 term is
   sharp.
4. **The primes with no admissible chain** (§4.5) need a construction outside Definition 2.1,
   or a proof that none of the paper's kind exists. The smallest open cases are κ = 4,
   p ∈ {5, 13} and κ = 6, p = 7.
5. **Paper.** Decide whether `app:s2-chains` enters, and whether the κ = 7 sentence of
   `rem:app-s2-tower-scope` should be updated: {29, 43, 71, 113} should become {29, 71} if
   §4.4–4.5 are accepted.
6. **Human review.** Theorem 2.2, Lemma 3.2, Theorem 3.1, Proposition 4.1, Lemma 4.2,
   Theorem 4.3, Corollary 4.4 and Propositions 4.6–4.7.

## 9. Artifacts

| file | content |
|---|---|
| `adaptive_chain.py` | Theorem 2.2 solver, pair finder, pow-based checkers; `demo` and `one` modes |
| `adaptive_demo.out`, `adaptive_extra.out` | end-to-end runs (§5.1) |
| `union_threshold.py` | LHS of Proposition 4.1, T_U, closed form, chain optimisation |
| `union_table.out`, `union_misc.out` | §4.3 tables, sanity, asymptotics, all-K search |
| `moment_check.py`, `moment_check.out` | empirical check of Proposition 4.1 |
| `union_exact.py`, `union_exact.out` | §4.4 exact chain sets at E_2(5), E_2(7) |
| `reach.py`, `reach_general.sh`, `reach.out`, `reach_general.out` | §4.5 all admissible chains |
| `barrier.py`, `barrier_e2_zs.out`, `barrier_lines.out`, `barrier_circuits.out` | §5.2–5.3 |
| `projection_check.sh`, `projection_check.out` | Proposition 4.6 check |
| `rectu.c` (copy of threshold-6), `rectu` (scratch binary) | complete DFS for RC(D; R → K) |
