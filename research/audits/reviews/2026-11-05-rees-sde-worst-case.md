# Rees diagonal SDE, worst case: no quadratic existence barrier, and steering without (ND′)

**Status: COMPLETE, AI-checked, pending human review.** 5 November 2026, overnight AI-only pass:
one Claude Code session, then one independent adversarial subagent (findings and fixes in §10).
Not human-reviewed, not in Lean, no novelty or priority claim.

- **Labels.** **[proved]** (full proof here), **[cited]**, **[computed]** (exact finite
  computation, script named), **[sampled]** (exact arithmetic on random or structured samples),
  **[conjecture]**.
- **Files.** Code and outputs are in `2026-11-05-rees-sde-worst-case/`, interpreter
  `/opt/anaconda3/bin/python`. Only this file and that folder were written: no `.tex`, no
  registry/JSON gate, no handoff/STATE edit, no git.

## 0. Verdict

1. **Option (B) is impossible as posed [proved].** No family of column sequences of length c·a² (or
   of any length > κa) leaves the target without a nonzero solution. By Chevalley–Warning every
   sequence of κa + 1 columns is solvable.
   - The longest unsolvable sequence has length N(κ, a, p), with **2a ≤ N(κ, a, p) ≤ κa**.
   - N(2, a, p) = 2a, N(κ, 1, p) = 2 once G*_2(p) ≥ 1 (for example p − 2 > (κ²−1)√p), and
     N(p−1, a, p) = (p−1)a by Olson's theorem.
   - Exact small values are in §2.

   So a quadratic lower bound can only concern the cost of *finding* a solution. At arities where
   every instance is solvable, such a bound would be an unconditional lower bound for a total search
   problem, out of reach of current techniques. Conditional or restricted-model bounds are not
   excluded; this pass proves none.
2. **Option (A), in part [proved]: (ND′) can be enforced by reserving a basis.** Theorem 2 (§3)
   modifies the steered block solver of `rem:sde-block-steered` in three ways:
   - it reserves r = rank columns spanning the bank as steering sources, with weights uniform in P;
   - it builds the flag from greedy circuits of the other columns;
   - it swaps a scanned column into the reserved basis when that column falls into the realized
     space.

   Then neither (H1) nor (ND′) is needed: every steering functional is nonzero on the reserved
   basis. For every bank and every admissible p:
   - with M ≥ D_E(r) + r + π columns, where π counts "true-pool" events, the forward pass reaches
     the span;
   - each backward pass then succeeds with probability ≥ 1 − ρ·max(1/G*_E(p), κ/(p−1)), where
     ρ ≤ rE/2;
   - with M ≥ D_E(r) + r, a stall implies π ≥ 1.

   Here D_3(r) = ⌊(r+2)²/4⌋ and D_E(r) ≤ r²/(2(E−1)) + r(1/(E−1) + 5/2).
3. **Worst-case corollary for banks in general position [proved].** A bank is in general position
   if every r of its columns span it. Such banks have π = 0. So for every general-position bank,
   with no randomness over the columns, the arity is **⌊(a+2)²/4⌋ + a** at E = 3, with per-pass
   failure ≤ 1/2:
   - for κ = 2 at every prime p ≥ max(256, 20a);
   - for κ = 3 at every prime p ≥ max(2750, 162a).

   With E = max(κ, 3, ⌈log_κ a⌉) and p ≥ poly(a) the arity is O(a²/log a).

   Caveat: general position of M columns of rank r ≥ 2 already forces M ≤ p + r − 1 (arc bound).
   So at this budget it forces p ≥ ⌊(r+2)²/4⌋ + 1, and the corollary is a large-p statement:
   p ≳ a²/4, against p ≥ 64a² in `rem:sde-block-steered`.
4. **Open [conjecture].** For arbitrary banks the only failure of the forward pass is a *stall*,
   which (at M ≥ D_E(r) + r) requires a true-pool event: a scanned column in the span of the
   reserved columns already lying in the realized space. Stalls do occur on solvable banks; the
   strongest example is the "lines" family of §5.

   Three repairs, a finishing pass and random restarts were added. With them the procedure solved
   all 2,520 structured and adversarial banks tried at the budget. There is no proof. **The best
   proved arity for arbitrary columns remains (a+1)(a+2)/2** (`prop:triangular-sde`).
## 1. Problem and notation

The paper's target (`eq:sde-target`, main.tex l. 527) is a nonzero (s_1..s_M) ∈ F_p^M with
Σ s_i^d λ_i = 0. With κ = gcd(d, p−1) ≥ 2, s ↦ s^d maps F_p onto P ∪ {0}, P = (F_p^×)^κ. So the
target is **solvable** iff there is x ∈ (P∪{0})^M ∖ {0} with Σ x_iλ_i = 0, and such an x converts
back by κ-th roots and a Bezout exponent, as in `prop:triangular-sde`. Throughout: λ_1..λ_M ∈ F_p^a
(the *bank*), r its rank, V its span, Q_ν = g^ν P, Q_ν° = Q_ν ∪ {0}, cos(y) = ν for y ∈ Q_ν.

**Admissible primes.** For E ≥ 2 let G*_E(p) be the minimum of
|Good(β)| = |{s ∈ F_p : β_b + s ∈ Q°_{−c_b} for all b}| over:
- 1 ≤ e ≤ E;
- arbitrary classes c_1..c_e, **including all equal**;
- pairwise distinct β_1..β_e.

Call p *admissible* if G*_E(p) ≥ 1. `rem:sde-block-steered` uses the same quantity G_E with at
least two classes; the single-class case is new here and needed for monochromatic rounds.

- Lemma W of the two-relation report (§4) never uses the classes, so
  G*_E(p) ≥ κ^{−E}(p − E − (κ^E−1)(E−1)√p) [proved there; re-checked: the character expansion is
  class-independent].
- **[computed]** `g_mono.py` → `g_mono_k2*.out`, `g_mono_k3*.out` (single-class patterns, e ≤ 3,
  exact by FFT correlation, normalised by translation and P-scaling):
  - κ = 2: single-class exceptions {3, 5, 7}, min ratio 0.1089 on 256 ≤ p ≤ 5000;
  - κ = 3: single-class exceptions {7, 13, 19, 31, 37, 43, 61, 73} ⊆ E_cg(3,3), none in
    300 ≤ p ≤ 11000; min ratio 0.017 (300–2750) and 0.0269 (2750–11000).
- Combined with the two-relation report's cross-class tables:
  - **κ = 2, E = 3: admissible ⇔ p ≥ 11, and G*_3(p) ≥ p/10 for every p ≥ 256.** This is exact to
    5000; beyond that Lemma W gives (p − 3 − 14√p)/8 ≥ p/10 for p ≥ 4930.
  - **κ = 3, E = 3: admissible ⇔ p ∉ E_cg(3,3), and G*_3(p) ≥ p/54 for p ≥ 2750.** This is exact
    to 11000; Lemma W gives ≥ p/54 for p ≥ 10829.

## 2. Option (B): existence has a linear threshold

**Proposition 1 [proved; (iv) cited].** Let N(κ, a, p) be the largest M such that some bank of M
columns in F_p^a is unsolvable.
- (i) N(κ, a, p) ≤ κa.
- (ii) N(κ, a, p) ≥ a·N(κ, 1, p) ≥ 2a.
- (iii) N(κ, 1, p) = 2 whenever every set Good(β) with two distinct offsets is nonempty, i.e.
  G*_2(p) ≥ 1. By Lemma W this holds when p − 2 > (κ²−1)√p, and by §1 it holds for κ = 2 (all p)
  and κ = 3 (all p ∉ E_cg(3,3)). By the Hasse–Weil bound it also holds whenever
  p + 1 > (κ−1)(κ−2)√p, so for κ ∈ {2, 3} it holds at every p. Hence N(2, a, p) = 2a.
- (iv) N(p−1, a, p) = (p−1)a.

*Proof.*
- (i) The a forms Σ_i λ_{ij}s_i^κ have degree κ in M > κa variables. Chevalley–Warning gives a
  common zero s ≠ 0, and x_i = s_i^κ ∈ P ∪ {0} is not all zero.
- (ii) Take a unsolvable one-dimensional banks c^{(j)} ∈ (F_p^×)^{n} and place c^{(j)} on
  coordinate j, i.e. the columns c^{(j)}_t e_j. A solution x restricts on block j to a solution of
  c^{(j)}. Some block is nonzero, which is a contradiction. For n = 2 take (1, −u) with u ∉ P: then
  x_1 = u x_2 with x_1, x_2 ∈ P ∪ {0} forces x = 0.
- (iii) Let c_1, c_2, c_3 be nonzero; zero columns are trivially solvable, and longer banks contain
  three columns. Put Z = 1. We need X ∈ Q_0° with
  Y = −(c_1X + c_3)/c_2 = (−c_1/c_2)(X + c_3/c_1) ∈ Q_0°, that is,
  X + c_3/c_1 ∈ Q°_{−cos(−c_1/c_2)}. This asks for s = X in a set Good(β) with the two distinct
  offsets 0 and c_3/c_1 and classes 0 and cos(−c_1/c_2), and then x = (X, Y, 1) ≠ 0.
  (Alternatively, the smooth curve c_1X^κ + c_2Y^κ + c_3Z^κ = 0 has genus (κ−1)(κ−2)/2 and so at
  least p + 1 − (κ−1)(κ−2)√p points by Hasse–Weil [cited: Weil 1949], and any point gives x.)
  With (ii) and the pair (1, −u), N(κ, 1, p) = 2.
- (iv) Here P = {1}, and the problem is zero-sum: the Davenport constant of (Z/p)^a is
  a(p−1) + 1 (Olson 1969) [cited]. ∎

**Exact values [computed]** (`max_unsolvable.py` → `max_unsolvable.out`). This is an exhaustive DFS
over banks containing e_1, e_2 (WLOG by GL_2), with columns up to P-scaling, pruning solvable prefixes.

| κ | p | N(a=1) | N(a=2) | CW bound κa (a=2) |
|---|---|---|---|---|
| 2 | 7, 13 | 2 | 4 | 4 |
| 3 | 7 | 2 | 5 | 6 |
| 3 | 13, 19, 31 | 2 | 4 | 6 |
| 4 | 13 | 3 | 6 | 8 |
| 4 | 17 | 2 | 5 | 8 |

Reading:
- The existence threshold is linear in a. For κ ≤ 3 it sits at 2a at every p ≥ 13 computed; for
  κ = 4 it does not (N(4,2,13) = 6 and N(4,2,17) = 5, at small p).
- κ = 4, p = 17 shows N(κ,2,p) > 2N(κ,1,p) can happen at small p.
- Whether N(κ, a, p) = 2a for p ≥ C(κ) is open [conjecture].
- **Consequence.** For a > κ/c, *every* sequence of c·a² columns is solvable, so option (B) as posed
  (no nonzero solution) cannot hold for any c > 0. The gap between the existence threshold (≤ κa, about 2a) and the best
  polynomial-time arity (quadratic) is a pure search gap. For κ = p − 1 it contains the problem
  BIS_p of Göös–Kamath–Sotiraki–Zampetakis, which the paper already cites.

**Strongest unconditional "lower bound" available.** The circuit-scheme bound of
`rem:sde-subquadratic`(a) is a model lower bound for exact one-circuit-per-direction schemes. The
conditional PRF bound of `rem:sde-subquadratic`(b) is at arity a + 2 < κa + 1. Neither applies at
total arities. Theorem 2 below evades the model bound, as the block solver does: it realizes
coset-generic pieces, not exact subspaces.

## 3. Theorem 2: source-steered block solver

**Algorithm SSS(E)** (`sss.py`: `forward_swap`, `backward`, `sss_theorem`). Fix E ≥ κ. Input: a
bank λ_1..λ_M with no zero column (a zero column is a solution).

1. **Reserve.** Let B be the first r indices whose columns are independent, so B is a basis of V.
2. **Forward pass.** Put U_0 = 0 and make every column outside B *unused*. While dim U < r:
   - Scan the unused columns in order, keeping a list T of scanned columns independent modulo U.
     The first column c with c ∈ U + span T has a unique relation δ (δ_c = 1) on T ∪ {c} modulo U.
     Its support S is a circuit modulo U, since the relations of T ∪ {c} modulo U form a line.
   - **|S| = 1**, i.e. c ∈ U. Write c = Σ_{σ∈B} γ_σ σ.
     - If some σ ∈ B ∖ U has γ_σ ≠ 0, **swap**: c replaces σ in B, σ becomes unused, and B stays a
       basis of V.
     - Otherwise c ∈ span(B ∩ U). This is a **true-pool event**: c is set aside.
   - **|S| ≥ 2.** Remove S from the unused columns, and let e = Σ_{i∈S}δ_iλ_i ∈ U. If δ is
     monochromatic and e = 0, return x = ζδ with ζ ∈ Q_{−cos δ} (a direct solution). Otherwise split
     S into E_l = min(E, |S|) blocks G_0..G_{E_l−1}, each inside one class {i : cos δ_i = c}.
     This is possible because δ has at most κ ≤ E classes. Put W_b = Σ_{i∈G_b}δ_iλ_i and
     U_l = U_{l−1} ⊕ Ω_l with Ω_l = span(W_1..W_{E_l−1}). The sum is direct, of dimension E_l − 1,
     by Theorem B(i) of the two-relation report: the only relation of the W_b modulo U_{l−1} is
     Σ_b W_b = e.
   - If the scan finds no c, the pass **stalls**.
3. **Backward pass** (when dim U_L = r). Draw t_σ uniformly from P for σ ∈ B (the final B), and put
   x_σ = t_σ and τ = −Σ_σ t_σσ ∈ V. For l = L, …, 1:
   - write τ = Σ_{b≥1}β_bW^{(l)}_b + τ′ with τ′ ∈ U_{l−1}, and put β_0 = 0;
   - if two offsets of different classes coincide, Good_l(β) ⊆ {−β_b}: test that value directly;
     otherwise draw s uniformly from Good_l(β) = {s : β_b + s ∈ Q°_{−c_b} for all b} by rejection;
   - fail if Good_l(β) is empty; otherwise put x_i = δ_i(β_{b(i)} + s) on round l and set
     τ ← τ′ − s e_l.

   Output x, which is verified. (The code enumerates Good exactly for p ≤ 30000, which covers the
   coincidence case.)

**Theorem 2 [proved].** Let κ ≥ 2, E ≥ κ, and let p be admissible (§1). Let λ_1..λ_M ∈ F_p^a be
**any** bank of rank r ≥ 1.

- (a) **Termination and cost.** The forward pass makes O(M + r) scans, each of O(M) Gaussian
  eliminations of size at most a × (r+1). It ends in one of three ways: a direct solution, a stall,
  or dim U_L = r. It is deterministic once the block-splitting rule is fixed. The code also offers a
  randomised splitting rule, which the theorem does not need.
- (b) **Columns.** Let π be the number of true-pool events and D_E the function of §3.1. At a stall,
  with q = r − dim U_L ≥ 1, the bank has M ≤ D_E(r) − D_E(q) + r + π + q ≤ D_E(r) + r + π − 1
  columns. So if M ≥ D_E(r) + r + π the pass does not stall, and if M ≥ D_E(r) + r every stall has
  π ≥ 1.
- (c) **Success.** If dim U_L = r, each backward pass returns a valid nonzero x with probability at
  least 1 − ρ·max(1/G*_E(p), κ/(p−1)).
  - Here ρ = Σ_l N_l over **all** rounds, where N_l is the number of pairs of blocks of round l in
    different classes.
  - ρ ≤ rE/2, because N_l ≤ C(E_l, 2) ≤ (E/2)(E_l − 1).
  - For E = 3: ρ ≤ r if κ = 2, and ρ ≤ 3r/2 if κ = 3.
  - Passes are independent given the forward pass.
  - When no cross-class coincidence occurs, round l takes p/|Good_l| ≤ p/G*_E(p) expected draws,
    each costing E coset tests. A coincidence costs one test.
- (d) **General position.** If every r columns of the bank span V, there is no true-pool event.
  Hence, for every bank in general position with M ≥ D_E(r) + r, the procedure is Las Vegas with
  the success bound of (c), and its only randomness is in the backward passes.

*Proof.*
- **(a) Termination.** Each scan ends in one of four ways:
  - it consumes at least 2 columns into a round. There are at most r rounds, since each gains ≥ 1
    dimension;
  - it makes a swap. A swap puts c ∈ U into B and removes σ ∉ U, so |B ∩ U| rises by one. U never
    shrinks and |B ∩ U| ≤ r, so there are at most r swaps;
  - it makes a true-pool event, at most M of them;
  - it stalls, or returns a direct solution.
  For the swap, B stays a basis because γ_σ ≠ 0.
- **(b) Columns.** Let D_E(q) be the worst-case number of columns consumed by rounds to go from
  quotient dimension q to 0. A round at quotient q uses a circuit of k + 1 columns, 1 ≤ k ≤ q, and
  gains E_l − 1 = min(E−1, k), with E_l = min(E, k+1). Hence
  D_E(q) = max_{1≤k≤q} [k + 1 + D_E(q − min(E−1,k))], with D_E(0) = 0.
  - Every round at quotient q satisfies (cost) + D_E(q − gain) ≤ D_E(q). Telescoping bounds the
    columns consumed between quotients r and q by D_E(r) − D_E(q).
  - At a stall the columns split into: B (r of them), rounds (≤ D_E(r) − D_E(q)), the true pool
    (π), and the unused columns. The unused columns are independent modulo U_L because the scan
    found no dependency, so there are ≤ q of them.
  - D_E(q) ≥ q + 1, from the circuit with k = q. This gives both inequalities.
- **(c) Values.** By Theorem B(ii) of the two-relation report, round l's weights lie in P ∪ {0}
  exactly when s ∈ Good_l(β), and their value is Σ_bβ_bW_b + s e_l. So τ_{l−1} = τ′ − s e_l ∈ U_{l−1},
  and the values telescope: Σ_i x_iλ_i = −τ_0 = 0. The t_σ are nonzero, so x ≠ 0.
- **(c) Steering forms.**
  - Write V = Ω_1 ⊕ … ⊕ Ω_L, and let Π_j be the coordinate projection of V onto
    U_j = Ω_1 ⊕ … ⊕ Ω_j. Since e_l ∈ U_{l−1}, induction gives
    τ_j = Π_j(τ_L) − Σ_{l>j} s_l Π_j(e_l).
  - For a pair (b, b′) of round j, φ_{j,bb′} = (β_b − β_{b′}) ∘ (Ω_j-coordinates) ∘ Π_j is a linear
    functional on V. It is **nonzero**: W^{(j)}_1.. is a basis of Ω_j, so β_b − β_{b′} (with β_0 = 0)
    is nonzero on Ω_j, and the map V → Ω_j is onto.
  - The offset difference at level j is
    F_{j,bb′} = −Σ_{σ∈B} t_σ φ_{j,bb′}(σ) − Σ_{l>j} s_l φ_{j,bb′}(e_l).
  - B spans V, so **for every (j, b, b′) some φ_{j,bb′}(σ) ≠ 0**. This replaces (ND′), for every bank.
- **(c) Failure events.**
  - A pass can fail only if Good_l(β) = ∅ at some level. This needs a cross-class coincidence at
    that level. Without one, equal same-class offsets merge into one block, at most E distinct
    offsets remain, and admissibility gives |Good| ≥ G*_E(p) ≥ 1.
  - So a failure implies that some cross-class coincidence occurs. Scan the levels downward and
    bound, for each cross pair (j, b, b′) of each round, the probability that the **first**
    cross-class coincidence of the pass is at (j, b, b′). This covers all rounds, including those
    with two blocks: a coincidence there is harmless for that round (β is constant and s = −β_0
    works), but it can force the s of that round.
  - On this event no level m > j had a cross-class coincidence, so each such s_m was drawn uniformly
    from a set of ≥ G*_E(p) elements.
  - Case 1: some s_l (l > j) has φ_{j,bb′}(e_l) ≠ 0. Let m be the least such l. Given the history
    before s_m is drawn, F_{j,bb′} is affine in s_m with nonzero slope, and s_{m−1}, …, s_{j+1} do
    not enter it. So the probability is ≤ 1/G*_E(p).
  - Case 2: otherwise F_{j,bb′} = −Σ t_σφ(σ), with some coefficient nonzero and the t_σ i.i.d.
    uniform on P. So the probability is ≤ 1/|P| = κ/(p−1).
  - Summing over the ρ cross pairs gives (c). The cost statement follows, since a pass meets a
    coincidence with probability at most the same bound.
- **(d) General position.** A true-pool event gives a scanned column c ∉ B with c ∈ span(B ∩ U).
  Here |B ∩ U| ≤ dim U ≤ r − 1, since the loop runs only while dim U < r. So {c} ∪ (B ∩ U) is a
  dependent set of at most r columns. In general position every set of at most r columns is
  independent: extend it to r columns, which span V. ∎

**Remarks.**
- The probability in (c) is over the backward-pass coins only. Unlike Corollary C of the
  two-relation report, nothing is assumed about the distribution of the columns.
- The swap is what makes (d) true. Without it (`sss.py: forward`), a column landing in U is wasted
  even in general position.
- The reserve costs r ≤ a columns, and the top column of `rem:sde-block-steered` is no longer
  needed. The greedy circuits can cost more than full ones: D_3(r) − (M_3(r) − 1) = [r even] ≤ 1.
  For E ≥ 4 the excess can exceed ⌈r/(E−1)⌉ (for example E = 4, r = 3: excess 2), and it is
  ≤ 2r by the bound of §3.1.

### 3.1 The count D_E [proved + computed]

- **D_3(q) = ⌊(q+2)²/4⌋ for q ≥ 1.**
  - At E = 3, D(q) = max(2 + D(q−1), q + 1 + D(q−2)) for q ≥ 2, with D(0) = 0 and D(1) = 2. A
    circuit with k ≥ 2 gains 2 at cost ≤ q + 1; one with k = 1 gains 1 at cost 2.
  - With f(q) = ⌊(q+2)²/4⌋, f(q) − f(q−1) = ⌊(q+2)/2⌋ and f(q) − f(q−2) = q + 1. So
    q + 1 + f(q−2) = f(q) ≥ 2 + f(q−1) for q ≥ 3. Also f(1) = 2 and f(2) = 4 = max(2 + 2, 3 + 0).
- **General E ≥ 3: D_E(q) ≤ q²/(2(E−1)) + q(1/(E−1) + 5/2).**
  - Call a round *big* if k ≥ E − 1 (gain E − 1, cost ≤ q + 1) and *small* if k ≤ E − 2 (gain k,
    cost k + 1 ≤ 2k). Small rounds cost ≤ 2q in total.
  - The i-th big round (i ≥ 0) is at quotient ≤ q − i(E−1) and needs quotient ≥ E − 1, so
    i ≤ m − 1 with m = ⌊q/(E−1)⌋.
  - The big rounds therefore cost ≤ m(q+1) − (E−1)m(m−1)/2. This is increasing in m up to
    (q+1)/(E−1) + 1/2, so it is ≤ its value at m = q/(E−1), namely q²/(2(E−1)) + q/(E−1) + q/2.
  - For E = 2, D_2(q) = (q+1)(q+2)/2 − 1.
- **[computed]** `dcount.py` → `dcount.out`: the closed form holds for q ≤ 400, and the bound for
  q ≤ 400 and E ≤ 12.

| a | triangular (a+1)(a+2)/2 | M_3(a), i.i.d. columns (`rem:sde-block-steered`) | **D_3(a)+a, every GP bank** | D_4(a)+a | D_5(a)+a | CW 2a+1 / 3a+1 |
|---|---|---|---|---|---|---|
| 4 | 15 | 9 | 13 | 12 | 12 | 9 / 13 |
| 6 | 28 | 16 | 22 | 19 | 18 | 13 / 19 |
| 10 | 66 | 36 | 46 | 37 | 33 | 21 / 31 |
| 20 | 231 | 121 | 141 | 105 | 88 | 41 / 61 |
| 50 | 1326 | 676 | 726 | 510 | 403 | 101 / 151 |
| 100 | 5151 | 2601 | 2701 | 1852 | 1428 | 201 / 301 |

## 4. Corollaries

**Corollary 3 (general-position banks, E = 3) [proved].** Let the bank be in general position in its
span, of rank r ≤ a, with M ≥ ⌊(r+2)²/4⌋ + r. The bound ⌊(a+2)²/4⌋ + a suffices, since D_3 is
nondecreasing.
- (i) κ = 2, every prime p ≥ max(256, 20a): each backward pass fails with probability
  ≤ ρ·(10/p) ≤ 10a/p ≤ 1/2. This uses ρ ≤ r ≤ a, G*_3(p) ≥ p/10 (§1) and 10/p ≥ 2/(p−1).
- (ii) κ = 3, every prime p ≥ max(2750, 162a): the bound is (3r/2)(54/p) ≤ 81a/p ≤ 1/2.
- (iii) In both cases k passes fail with probability ≤ 2^{−k}. The expected time is polynomial in a
  and log p.

**Caveat (arc bound).** For r ≥ 2 general position forces the columns to be pairwise
non-proportional, i.e. an arc in PG(r−1, p), so M ≤ p + r − 1 [standard]. At this budget the
hypothesis therefore already implies p ≥ ⌊(r+2)²/4⌋ + 1. Corollary 3 is a statement about primes
p ≳ a²/4.

**Corollary 4 (general E) [proved].** Let E = max(κ, 3, ⌈log_κ a⌉) and
p ≥ max(8κ^{2E}E², 2aEκ^E).
- Lemma W gives G*_E(p) ≥ p/(2κ^E), since (κ^E−1)(E−1)√p + E ≤ p/2.
- The per-pass failure is therefore ≤ (rE/2)·(2κ^E/p) ≤ aEκ^E/p ≤ 1/2.
- So every general-position bank with M ≥ D_E(a) + a ≤ a²/(2(E−1)) + 4a columns is solved by a
  Las Vegas procedure in expected time κ^E·poly(a, log p).
- When a ≥ κ^{κ}, κ^E ≤ κa, so the arity is O(a²/log a), the time is polynomial, and
  p ≥ 8κ²a²E² suffices.

**Remarks.**
- **Relation to `rem:sde-block-steered`.** That remark has similar arities, without the +a reserve
  and the small greedy loss, for i.i.d. uniform columns (failure probability over the columns) or
  under the run-dependent (H1) and (ND′). Corollary 3 holds for every general-position bank, with no
  column randomness. Both are large-p statements, quadratic in a.
- **Rees labels.** The labels of `lem:s3-law` are i.i.d. uniform on K_d^⊥. M ≈ a²/4 uniform columns
  are in general position only when p ≫ C(M, r), which is exponential in a, so Corollary 3 does not
  apply to them. Whether true-pool events are rare for uniform columns was not proved here: the
  relevant subspaces depend on the run, and scanned columns are rescanned. **For the Rees
  application `rem:sde-block-steered` remains the relevant statement.** The paper's counts are
  unchanged.

## 5. What remains: stalls, the strongest counterexample, and the experiments

**The obstruction [proved, from Theorem 2].** For an arbitrary bank with M ≥ D_E(r) + r, SSS(E)
fails in only two ways:
- by stalling, which requires a true-pool event, i.e. a scanned column c ∈ span(B ∩ U_l) ⊊ V;
- or in a backward pass, which happens with probability ≤ ρ·max(1/G*_E(p), κ/(p−1)) per pass
  whatever the bank, and is cured by repetition.

The remaining worst-case obstruction is therefore the column count of the forward pass on banks with
many short dependent sets. It is not steering.

**Strongest counterexample to Theorem 2 without general position [computed].**
- The "lines" banks place their columns on a + 1 lines F·v_j in general position, with random
  multipliers. They are solvable, since M ≥ κa + 1.
- The Theorem-2 algorithm (`sss_theorem`) stalls on 25/120 of them (κ = 2, p ∈ {1009, 10007},
  a ∈ {3, 5, 7}).
- Every stall has a true-pool event, as Theorem 2(b) predicts. `run_theorem_planted.out` records
  ('stall', had pool): 25 and ('stall', no pool): 0.
- An explicit stalled bank, p = 1009, κ = 2, a = 3, M = 9:
  `[[170,720,640],[72,522,340],[337,384,757],[512,970,855],[724,989,767],[14,606,963],[823,827,687],[966,829,143],[854,768,10]]`.
  Columns 5 and 9 are proportional (442·col5 + col9 = 0, and 442 is a residue). The full algorithm
  below solves it through a collinear triple.

**Planted family of the two-relation report §6.2.** These banks are not in general position: the
checker found 13–27 dependent r-subsets at a = 4 and 380–590 at a = 6. So Theorem 2(d) does not
cover them, and the following are experiments only:
- padded to D_E(a) + a, the Theorem-2 algorithm solved 48/48 (`run_theorem_planted.out`;
  κ ∈ {2, 3}, a ∈ {4, 6, 8}), and plain SSS without swaps solved 96/96 (`run_planted.out`;
  E ∈ {3, 4});
- **unpadded** (exactly M_E(a) < D_E(a) + a columns), plain SSS solved only 1/24
  (`run_planted.out`), because the reserve leaves too few columns.

The paper's κ = 3, a = 10 planted instance was not run under the Theorem-2 algorithm.

**Repairs and the full algorithm** (`sss.py: sss_rec, finish_stall, sss_full`) [sampled, no proof]:
- (R1) **Collinear triples.** Three columns on one line form a one-dimensional instance, solvable by
  Proposition 1(iii).
- (R2) **Coloops.** A column outside the span of the others has weight 0 in every solution, so it
  is removed.
- (R3) **Recursion.** On a stall, recurse on the columns lying in U_L, or in span(B ∩ U_L), when
  there are at least D_E(·) + dim of them.
- (R4) **Finishing pass.** Continue the forward pass on the unused columns together with B ∖ U_L,
  then steer with the unused part of B and the pool.
- (R5) **Restarts** with random column orders. `sss_full` runs them, but in the recorded runs
  `forwards` was 1 or 2.

| run | banks | result |
|---|---|---|
| `run_adv2.out`: lines (a, a+1, a+2 lines), dense subspace of codim 1, flags, sparse ±1/2 columns; κ = 2 (p = 1009, 10007; a = 3–9), κ = 3 (p = 1009, 10009; a = 4–8); budget D_3(a)+a ≥ κa+1 | 1080 | **1080 solved** |
| `run_search.out`: entries in {0, ±1, ±2}, 0/1 columns, scaled 0/±1 palettes; κ = 2 (p = 257, 1009), κ = 3 (p = 2791, 3001) | 1440 | **1440 solved** (52 of them through a zero column) |
| `run_planted.out`: random banks at the budget, plain SSS | 160 | 160 solved |
| `test_gp.out`: general-position banks (checked exhaustively), Theorem-2 algorithm exactly | 525 | **525 solved, 0 true-pool events, 0 stalls**, see §9 |

- Earlier runs of `run_adv2.py` left 3 failures without (R1) and (R2), and 6 failures with (R2) but
  without (R1), on different random draws.
  All were lines banks at codimension 1 with no circuit available for (R4). Those outputs were
  overwritten, so these counts are not artifacts.
- Every returned witness was verified (`check`).
- `sss_theorem` reports only the final status after up to 10–20 passes, so the outputs do not show
  single-pass failures. The checker's single-pass counts on general-position banks are consistent
  with Theorem 2(c): 3/560 failures at p = 257 (κ = 2, a = 4); 4/720 and 5/780 at p = 307 (κ = 3);
  28/740 at p = 31. They are in `check/c2.py`.

**Conjecture 5 [conjecture].** For κ ∈ {2, 3}, E = 3, admissible p ≥ poly(a), and every bank of
⌊(a+2)²/4⌋ + a columns, the full algorithm (R1)–(R5) finds a solution in expected polynomial time.
A proof would have to bound the true-pool loss on dense banks. The natural induction on dense
subspaces fails by counting: a stall at codimension 1 can coexist with a pool of size about
D_E(r−1).

## 6. Claim gates, next question

**Claim gates that must stay false:**
- "A polynomial SDE solver with o(a²) columns, or ⌊(a+2)²/4⌋ + a, exists for **arbitrary**
  columns." Theorem 2 needs general position, or no true-pool event. Conjecture 5 is unproved.
- "A quadratic number of columns is necessary for existence." This is false by Proposition 1.
- "A quadratic number of columns is necessary for polynomial-time solving." This is unproved, and
  unconditionally out of reach.
- "The worst-case result is uniform in p." Theorem 2 needs admissible p with G*_E(p) ≫ a, and
  general position needs p ≳ a²/4.
- Any novelty or priority claim. Reserving a steering basis is simple, and the literature on
  large-p diagonal systems was not searched in depth.

**Next hard question (Q1).** Bound the true-pool loss. Take a bank with M ≥ D_E(r) + r + X that
stalls with π true-pool events at codimension q. Show that either:
- (i) some subspace Y holds ≥ D_E(dim Y) + dim Y columns, so the recursion applies; or
- (ii) the finishing pass (R4) succeeds.

The critical case is q = 1 with |B ∖ U_L| = 1 and no unused column.

**Next command.**
`cd research/audits/reviews/2026-11-05-rees-sde-worst-case && nice -n 10 /opt/anaconda3/bin/python -B run_search.py 17`,
extended with a hill-climbing generator that maximises π.
- Expected artifact: a bank on which `sss_full` fails, which would be a counterexample to
  Conjecture 5, or a longer sampled record.
- Acceptance test: every failure is a solvable bank (M ≥ κa + 1) with a recorded stall
  certificate.

## 7. Proposed text

**Location.** `docs/papers/rees-hsp/main.tex`, immediately after `\end{remark}` of
`rem:sde-block-steered`. **Status: AI-checked, pending human review.** Nothing else in the paper
changes. The text uses only macros and citations already in the paper (`\file`, `\Fp`, `\binom`,
`LidlNiederreiter1997` through the Weil bound quoted in `rem:sde-block-steered`). Hasse–Weil is not
needed: part (a) uses the two-offset case of that bound.

```latex
\begin{remark}[Worst case: no quadratic existence barrier, and steering by a reserved basis; AI-checked, pending human review]
\label{rem:sde-worst-case}
This remark comes from an AI-only pass (\file{research/audits/reviews/2026-11-05-rees-sde-worst-case.md}), checked by a second, adversarial AI pass whose findings are recorded and applied in that file; no human has checked it, and nothing else in the paper uses it. Keep the notation of Remark~\ref{rem:sde-block-steered}, call a sequence of columns a bank, and let $G^*_E(p)$ be defined as $G_E(p)$ but allowing all the classes to be equal. The Weil bound quoted there gives $G^*_E(p)\ge\kappa^{-E}\bigl(p-E-(\kappa^E-1)(E-1)\sqrt p\bigr)$. Exact computations up to $p=5000$ and $p=11000$, together with this bound, give $G^*_3(p)\ge p/10$ for $\kappa=2$ and $p\ge256$, and $G^*_3(p)\ge p/54$ for $\kappa=3$ and $p\ge2750$ (finite computations, AI-checked, pending human review).

\textup{(a)} \emph{Existence is linear in $a$.} Let $N(\kappa,a,p)$ be the largest number of columns in $\Fp^a$ for which~\eqref{eq:sde-target} can have no nonzero solution. Then $2a\le a\,N(\kappa,1,p)\le N(\kappa,a,p)\le\kappa a$. The upper bound is the Chevalley--Warning theorem. For the lower bound, place unsolvable one-dimensional banks on the coordinates; the two columns $1,-u$ with $u\notin P$ form one. Moreover $N(\kappa,1,p)=2$ whenever $G^*_2(p)\ge1$, for instance whenever $p-2>(\kappa^2-1)\sqrt p$. Indeed, for nonzero $c_1,c_2,c_3$ a solution with third weight $1$ asks for $X\in P\cup\{0\}$ with $X+c_3/c_1\in Q^\circ_{\nu}$, $\nu=-\mathrm{cos}(-c_1/c_2)$, which is a set $\mathrm{Good}(\beta)$ with two distinct offsets. Hence $N(2,a,p)=2a$. Exhaustive searches give $N(3,2,p)=4$ for $p\in\{13,19,31\}$, $N(3,2,7)=5$ and $N(4,2,17)=5$ (finite computations, AI-checked, pending human review). So for $a>\kappa/c$ every bank of $c\,a^2$ columns has a nonzero solution. A quadratic column count can be needed only for finding a solution, not for its existence. The gap between the counts of Proposition~\ref{prop:triangular-sde} and Remark~\ref{rem:sde-block-steered} and the existence threshold, at most $\kappa a$, is a search gap. Proving that this gap is necessary for polynomial-time algorithms would be an unconditional lower bound for a total search problem, and is not attempted.

\textup{(b)} \emph{Steering by a reserved basis.} Modify the procedure of Remark~\ref{rem:sde-block-steered} in three ways.
\begin{itemize}
\item Reserve $r$ columns $B$ that form a basis of the span $V$ of the bank, where $r$ is its rank.
\item Build the rounds greedily from the other columns. Scan them, keeping a set $T$ of scanned columns independent modulo the current space $U$, until a column $c$ lies in $U+\mathrm{span}\,T$. The support of the resulting relation is a circuit modulo $U$; split it into $\min(E,|S|)$ blocks. If that circuit is $\{c\}$, so that $c\in U$, write $c$ in the basis $B$. If $c$ has a nonzero coefficient on some $\sigma\in B\setminus U$, exchange $c$ and $\sigma$. Otherwise $c\in\mathrm{span}(B\cap U)$; call this a true-pool event and discard $c$.
\item Start the back substitution from $\tau=-\sum_{\sigma\in B}t_\sigma\sigma$, with the $t_\sigma$ independent and uniform in $P$.
\end{itemize}
Every cross-class offset difference $\beta_b-\beta_{b'}$ of every round is then a linear form in $(t_\sigma)$ and the drawn scalars. Its coefficients on the $t_\sigma$ are the values on $B$ of a nonzero functional on $V$, so they are not all zero. Hence neither the circuit condition nor the condition on the offset differences in Remark~\ref{rem:sde-block-steered} is needed.

Define $D_E(0)=0$ and $D_E(q)=\max_{1\le k\le q}\bigl(k+1+D_E(q-\min(E-1,k))\bigr)$. Then $D_3(q)=\lfloor(q+2)^2/4\rfloor$ for $q\ge1$, and $D_E(q)\le q^2/(2(E-1))+q\bigl(1/(E-1)+5/2\bigr)$ for $E\ge3$. Let $E\ge\kappa$ and $G^*_E(p)\ge1$. Let the bank, of any form, have rank $r$ and at least $D_E(r)+r+\pi$ columns, where $\pi$ is the number of true-pool events. Then the forward pass reaches $V$. Each back substitution returns a nonzero solution with probability at least $1-\rho\max\bigl(1/G^*_E(p),\kappa/(p-1)\bigr)$, and this probability is over the drawn scalars only. Here $\rho\le rE/2$ is the number of pairs of blocks in different classes, summed over the rounds; for $E=3$, $\rho\le r$ if $\kappa=2$ and $\rho\le3r/2$ if $\kappa=3$.

A true-pool event exhibits a dependent set of at most $r$ columns. So $\pi=0$ for banks in general position, that is, banks in which every $r$ columns span $V$. Hence, for every bank in general position in $\Fp^a$ with at least $\lfloor(a+2)^2/4\rfloor+a$ columns, a Las Vegas procedure fails with probability at most $1/2$ per back substitution. This holds for $\kappa=2$ at every prime $p\ge\max(256,20a)$, and for $\kappa=3$ at every prime $p\ge\max(2750,162a)$. General position of so many columns already forces $p\ge\lfloor(a+2)^2/4\rfloor+1$ when $r=a\ge2$, since the columns are pairwise non-proportional and so form an arc in a projective space of dimension $r-1$. Likewise, with $E=\max(\kappa,3,\lceil\log_\kappa a\rceil)$ and $p\ge\max(8\kappa^{2E}E^2,2aE\kappa^E)$, every bank in general position with $D_E(a)+a$ columns is solved by a Las Vegas procedure in expected time $\kappa^E$ times a polynomial in $a$ and $\log p$. For $a\ge\kappa^\kappa$ this is polynomial time with $O(a^2/\log a)$ columns. On the planted instances of Remark~\ref{rem:sde-block-steered} with $a\le8$, which are not in general position, padded to $\lfloor(a+2)^2/4\rfloor+a$ columns, the procedure succeeded in every trial (finite computation, AI-checked, pending human review).

\textup{(c)} \emph{What is open.} For arbitrary banks the procedure can stall through true-pool events, and it does so on solvable banks with many proportional columns. It was extended with three repairs, a finishing pass that uses the unused part of $B$, and restarts in random column orders. The repairs are: solving collinear triples by~(a), removing columns outside the span of the others, and recursing on the realised subspace. With them it solved each of $2{,}520$ structured and adversarial banks with $\lfloor(a+2)^2/4\rfloor+a$ columns, for $\kappa\in\{2,3\}$ and $a\le9$ (sampled computation, AI-checked, pending human review), but there is no proof. So for arbitrary columns the best arity proved in this paper remains $(a+1)(a+2)/2$. The counts of Theorem~\ref{thm:main}, the remarks above and the tables do not change.
\end{remark}
```

## 8. Artifacts

| file | content |
|---|---|
| `sss.py` | Theorem-2 algorithm (`forward_swap`, `backward`, `sss_theorem`), plain variant without swaps (`forward`, `sss`), repairs (`sss_rec`, `finish_stall`, `sss_full`), D_E (`worst_forward_cost`) |
| `dcount.py` → `dcount.out` | D_3 closed form, the D_E bound, the arity table |
| `g_mono.py` → `g_mono_k2.out`, `g_mono_k2_small.out`, `g_mono_k3.out`, `g_mono_k3_small.out`, `g_mono_k3_mid.out` | exact single-class Good minima, κ = 2 (3–5000), κ = 3 (7–11000) |
| `max_unsolvable.py` → `max_unsolvable.out` | exact N(κ, 1, p), N(κ, 2, p) |
| `run_planted.py` → `run_planted.out` | planted family (padded/unpadded) and random banks, plain SSS |
| `run_theorem_planted.py` → `run_theorem_planted.out` | Theorem-2 algorithm on the padded planted family and the lines family; explicit stalled bank |
| `run_adversarial.py` → `run_adversarial.out` | first structured sweep (plain vs recursive), before the repairs |
| `run_adv2.py` → `run_adv2.out` | structured families with all repairs: 1080/1080 |
| `run_search.py` → `run_search.out` | small-entry banks: 1440/1440 |
| `test_gp.py` → `test_gp.out` | general-position banks (checked exhaustively), Theorem-2 algorithm exactly |
| `check/c1.py`–`check/c4.py` | the adversarial checker's scratch scripts (single-pass failure counts, stall inequality on 1457 stalls, general-position counts of the planted family) |

The code imports `common.py` and `brt_tests.py` from `2026-11-05-rees-sde-two-relation/` only to
regenerate the planted family. It is independent of `brt.py`.

## 9. Computations

`test_gp.out` (Theorem-2 algorithm exactly, banks checked to be in general position by testing every
r-subset; budget ⌊(a+2)²/4⌋ + a):

| p | κ | a | M | CW κa+1 | banks | result | true-pool events |
|---|---|---|---|---|---|---|---|
| 257 | 2 | 2, 3, 4 | 6, 9, 13 | 5, 7, 9 | 60 each | all solved | 0 |
| 10007 | 2 | 5 | 17 | 11 | 15 | all solved | 0 |
| 1000003 | 2 | 6 | 22 | 13 | 15 | all solved | 0 |
| 2791 | 3 | 2, 3, 4 | 6, 9, 13 | 7, 10, 13 | 60 each | all solved | 0 |
| 307 | 3 | 2, 3 | 6, 9 | 7, 10 | 60 each | all solved | 0 |
| 10009 | 3 | 5 | 17 | 16 | 15 | all solved | 0 |

For κ = 3 and a ∈ {2, 3}, M is **below** the Chevalley–Warning bound. Theorem 2(d) then implies
that every general-position bank of that size is solvable at admissible p with
ρ·max(1/G*, κ/(p−1)) < 1. This is consistent with Proposition 1: N(3, 2, p) = 4 < 6 at the primes
computed.

Other outputs: `g_mono*.out` (§1), `max_unsolvable.out` (§2), `dcount.out` (§3.1),
`run_*.out` (§5).

## 10. Independent adversarial check (verdict and fixes)

A fresh general-purpose subagent was given this report, the code paths and the context files. It was
not given the conclusions. Its verdict:

| claim | checker verdict | action |
|---|---|---|
| Proposition 1 | correct (reran (3,7), (4,17); independent brute force confirms N(3,2,7) = 5) | Hasse–Weil not cited in the paper (G6): the proof of (iii) now uses the two-offset Weil bound already cited; Hasse–Weil kept only as an aside |
| Theorem 2(a), (d) | correct; the code matches the algorithm, and the backward pass uses the final B | none |
| Theorem 2(b) | correct; add "M ≥ D_E(r)+r" to "π ≥ 1" | done |
| Theorem 2(c) | **proof gap G1**: a coincidence in a 2-block round can force s_m, so ρ must count the cross pairs of all rounds | fixed. ρ is now over all rounds, ρ ≤ rE/2 (≤ r for κ = 2, ≤ 3r/2 for κ = 3, E = 3). The corollary thresholds are unchanged, and Corollary 4 is restated |
| Theorem 2(c), cost | gap G4: the draws after a coincidence | fixed: the forced value is tested directly |
| D_E bounds | correct; the claimed greedy loss ≤ ⌈r/(E−1)⌉ was false for E ≥ 4 (E3) | fixed: [r even] for E = 3, and the false claim removed |
| Corollaries 3, 4 | numbers correct after G1; general position forces p ≳ r²/4 by the arc bound (G2); Corollary 4 needs E ≥ max(κ, 3) | caveat added in §0, §4 and the LaTeX; E = max(κ, 3, ⌈log_κ a⌉) |
| Rees-label remark | asserted without proof (G3) | replaced by "not proved here" |
| Experiments | counts match the outputs | E1: the planted family is not in general position, so "covers" became "empirically, 48/48", and the unpadded 1/24 is reported. E2: the claim that no single pass fails is removed and the checker's single-pass counts reported. G5: the pre-repair counts are marked as non-artifacts. The 52 zero-column banks are noted |
| LaTeX remark | no forbidden macros; it needed the revisions listed | applied: the check sentence, "exact computation plus Weil", ρ, "at least", general position and E ≥ κ in the O(a²/log a) sentence, the arc caveat, a ≤ 8 for the planted runs, no Hasse–Weil, restarts |

Imprecisions also fixed:
- §0 item 1 now says that conditional or model lower bounds are not excluded.
- The κ = 4 values of N are noted.
- The Lemma W κ = 3 threshold was 10829 here; the checker computes 10828. This is harmless, and
  either value works.

Residual verdict after fixes: Proposition 1, Theorem 2 and Corollaries 3–4 hold as now stated. The
worst case for arbitrary banks is **not** settled. The paper's best proved arity for arbitrary
columns remains (a+1)(a+2)/2.
