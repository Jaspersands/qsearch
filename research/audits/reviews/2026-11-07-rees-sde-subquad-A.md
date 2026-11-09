# Rees diagonal SDE, worst case below a²: (T) holds with load c = 2(J−1); every bank with D_J(r) + O(Jr) columns is solved in Las Vegas time κ^{O(J)}·poly

AI-only pass, 7 November 2026, one Claude Code session plus one independent adversarial subagent
(§12). Not human-reviewed, not in Lean, no novelty or priority claim. Scripts and outputs:
`2026-11-07-rees-sde-subquad-A/`, interpreter `/opt/anaconda3/bin/python`. Only this file and that
folder were written: no `.tex`, no git, no STATE/handoff edit, `make_numbers.py` not run.

Labels: **[proved]** (complete proof here or in a cited report, re-derived), **[exact]**
(complete finite computation, script named), **[sampled]** (exact arithmetic on random or
structured samples), **[argued]**, **[conjecture]**, **[literature]**.

## 0. Verdict

1. **(T) is proved [proved], with absorption load c = 2(J − 1), i.e. at most 3J − 2 blocks per
   round, for every J ≥ max(κ, 2), at the budget F(r) = D_J(r) + C_J r with C_J = max(2, 2J − 4).**
   This is Theorem A (§6). The Q1 obstruction ("heavy stalls", unbounded c) is removed by one new
   step, the **Rado flat**: when no absorption of load ≤ c exists, the min–max certificate of the
   matroid intersection (linear matroid mod U against the partition matroid of the rounds with
   capacity c) is a flat W = U + span(Z) of codimension q_W > c, and only
   (q_W − 1) + ⌊(q_W − 1)/c⌋(r + 1 − c) + (r − 1) columns lie outside W. For c = 2(J − 1) this
   is at most F(r) − F(r − q_W), so the recursion on W applies (Lemma M, §4). Three smaller
   changes complete the case analysis: the Y-recursion of Q1 already applies whenever b ≤ q
   (not only b ≤ q − 2); the U⁺-recursion applies whenever q⁺ ≥ 2(J − 1); and a top phase of
   singleton-block rounds over a reserved basis of V/U⁺ handles 1 ≤ q⁺ ≤ 2J − 3 (Lemma T_m, §5).
2. **Corollary A (subquadratic worst case) [proved].** Let κ ≥ 2, J = max(κ, 3, ⌈log_κ a⌉),
   E = 3J − 2, and let p ≡ 1 (mod κ) be a prime with p ≥ max(8κ^{2E}E², 2Eaκ^E). Every bank in
   F_p^a, of any form, with at least
   F(a) = D_J(a) + max(2, 2J−4)·a ≤ a²/(2(J−1)) + a(2J − 3/2 + 1/(J−1)) = O(a²/log a)
   columns is solved by a Las Vegas algorithm in expected time κ^E·poly(a, M, log p). For fixed κ
   this is polynomial in a and log p: once a > κ^{max(κ,3)−1}, J = ⌈log_κ a⌉ and κ^E < κa³
   (for smaller a, J ≤ max(κ, 3) is a constant). Each back substitution fails with
   probability ≤ 1/2, the randomness being in the back substitution only. The prime condition is
   p ≥ 72κ²a⁶J² and p ≥ 6Jκa⁴: polynomial in a for fixed κ, not uniform in p.
3. **Corollary A₃ (J = 3, κ ∈ {2, 3}) [proved].** Every bank of rank r with at least
   ⌊(r+2)²/4⌋ + 2r columns is reduced deterministically to a leaf with ≤ 7 blocks per round;
   back substitution fails with probability ≤ 1/2 for κ = 2 at every prime
   p ≥ max(2.33·10⁶, 1792r), and for κ = 3 at every prime p ≥ max(6.89·10⁸, 30618r)
   (`weil_thresholds.out`). So the best worst-case arity provable by these methods drops from
   (a+1)(a+2)/2 to ⌊(a+2)²/4⌋ + 2a at large p, and to O(a²/log a) with J = ⌈log_κ a⌉.
4. **Weakest step.** The new steps (Lemma M, Lemma T_m, the counts of §3) are short and were
   asserted at run time on every branch. The weakest link is inherited: the steering Lemma 2
   (first-coincidence argument of Theorem 2(c), Q1 Lemma 2), now used with up to 3J − 2 blocks
   and with absorbed blocks. It was re-derived here (§2) and checked by the Q1 referee, but it is
   a conditioning argument that no human has checked. Second weakest: the count chain
   D_J(r) − D_J(r−m) ≥ t(r+1) − (J−1)t(t−1)/2 (§3), proved and also verified exactly for
   J ≤ 20, r ≤ 1500.
5. **Computations [sampled; exact asserts].** ALG-T ran in strict mode (every count inequality of
   the proof asserted, every leaf checked for (F1), (F2) and (S), every witness verified) on
   986 banks here and 277 more in the independent check (κ ∈ {2, 3}, J ∈ {3, 4, 5}, rank up to
   46; table in §9): 0 assertion failures, 0 unsolved, 0 leaves violating (S), 1 single-pass
   failure (at p = 100003, below the theorem's prime range). The Rado-flat branch fired 62 times
   here (least absorption loads up to 10 > c) and 118 times in the check. On 13 of the 62 the
   U-recursion count of Q1 fails, and on 6 both the U- and the Y-recursion counts fail
   (`vtwist_1.out`, `vtwist2_2.out`, `thmprime_1.out`): these are exactly the heavy stalls Q1
   could not handle. 62 banks ran at primes inside the range of Corollary A₃
   (p = 2,330,021 for κ = 2 and p = 689,000,047 for κ = 3). Finite computations prove nothing
   about scaling in a.
6. **What does not change [gates].** The method needs p ≥ poly(a); it is not uniform in p and
   says nothing at p = 3 (F_3 subset sum) or κ = p − 1 (BIS_p). Θ(a²/log a) is the limit of
   flag-based schemes whose cost κ^{blocks} must stay polynomial [argued, §10]. The paper is not
   changed by this pass; integrating Theorem A would change only Remark `rem:sde-worst-case-q1`
   and the sentence "the best arity proved … remains (a+1)(a+2)/2" in the SDE remarks
   (owner decision; not done here).

## 1. Notation

As in the Q1 report §1. Bank λ_1..λ_M ∈ F_p^a, rank r, span V. SSS(J): reserved basis B, greedy
circuits modulo the realized space U, min(J, |S|) blocks inside classes (fixed rule: split the
largest class, peeling its first element), swaps, true pool. Round l: support S_l, relation δ_l,
blocks G_{l,b}, W_{l,b} = Σ_{i∈G_{l,b}} δ_iλ_i, e_l = Σ_b W_{l,b}; flag conditions (F1) block sums
b ≥ 1 independent mod U_{l−1}, (F2) e_l ∈ U_{l−1}. Steering functionals φ_{j,bb′}; hypothesis (S):
no φ of a cross-class pair vanishes on span(Src) + span(e_l : l > j). At a stall: U = U_L,
q = r − dim U, pool, T (unused, independent mod U, |T| ≤ q), Fr (free columns), Fin = Fr ∩ U,
b = |B ∩ U|, ε = dim U − b, X = Fr ∖ U = (B∖U) ∪ T, Rout = round columns outside U,
U⁺ = span(round columns ∪ Fin) = U + span(Rout), q⁺ = r − dim U⁺. G*_E(p) = least |Good(β)| over
≤ E pairwise distinct offsets and arbitrary classes (Q1 §1). D_J as in the worst-case report §3.1:
D_J(0) = 0, D_J(q) = max_{1≤k≤q}(k + 1 + D_J(q − min(J−1, k))).

Throughout: **c = 2(J − 1), C = max(2, 2J − 4), F(r) = D_J(r) + C r, E = J + c = 3J − 2.**

## 2. Inputs, re-checked at general J

- **Theorem 2(b) of the worst-case report, general J [proved there; re-derived].** Every round at
  quotient q′ costs k + 1 ≤ q′ + 1 columns and gains min(J − 1, k), so (cost) + D_J(q′ − gain)
  ≤ D_J(q′). At a stall M = r + |Rcols| + π + |T| with |Rcols| ≤ D_J(r) − D_J(q) and |T| ≤ q. At
  M ≥ F(r) this gives **π ≥ (C − 1)r + D_J(q) − q ≥ 2** (D_J(q) ≥ q + 1).
- **Corollary A of Q1** (pool ⊆ span(B∩U), Fin spans span(B∩U), |B∖U| = q + ε) [proved there,
  checked by the Q1 referee]. With π ≥ 1: b ≥ 1 and U ≠ 0.
- **Lemma 2 of Q1 (steering without circuits) [proved there; re-derived].** For any flag with
  ≤ E_max blocks per round, blocks inside classes, and nonempty Src outside the rounds with
  span(Src) ⊆ U_L satisfying (S): each back substitution fails with probability
  ≤ ρ·max(1/G*_{E_max}(p), κ/(p−1)), ρ = number of cross-class block pairs over all rounds
  ≤ (E_max/2)·Σ_l(n_l − 1) ≤ E_max·r/2. Re-derivation points: (i) Theorem B(ii) of the
  two-relation report needs only blocks inside classes, so absorbed singleton blocks (which keep
  the class of their parent block) are covered; (ii) Case 1 conditions on the history before
  s_m, where m is the least l > j with φ(e_l) ≠ 0, and s_m is uniform on a set of size
  ≥ G*_{E_max} because level m had no coincidence on the event bounded; (iii) Case 2 uses only that
  F is affine with nonzero slope in some t_σ, uniform on P. Nothing depends on the size of
  E_max beyond G*_{E_max}.
- **Lemma A (closure), Lemma R (absorption), Lemma S (singleton top rounds)** of Q1 [proved
  there, checked by the Q1 referee]. Lemma A and Lemma S hold for every flag, in particular for
  absorbed flags. Lemma R: absorbing any set I ⊆ Rout independent mod U, in any order, gives a
  flag realizing U ⊕ span(I), with |I ∩ S_l| extra singleton blocks in round l.
- **Lemma W at E = Θ(log a) [proved; scales].** For e ≤ E distinct offsets and any classes,
  |Good| ≥ κ^{−e}(p − e − (κ^e − 1)(e − 1)√p). The proof (two-relation report §4) expands each
  indicator in the κ characters; a term with support of size w is a character sum of
  f(s) = Π_b (s + β_b)^{t_b} with distinct roots and 0 < t_b < κ, so f is not a constant times a
  κ-th power and Weil (Lidl–Niederreiter Thm 5.41) gives (w − 1)√p [literature]. Nothing in it
  depends on E except the count κ^e − 1 of terms. If p ≥ 8κ^{2E}E² then
  (κ^E − 1)(E − 1)√p + E ≤ p/(2√2) + p/100 ≤ p/2, so **G*_E(p) ≥ p/(2κ^E)**; with ρ ≤ Er/2 the
  per-pass failure is ≤ Erκ^E/p ≤ 1/2 once p ≥ 2Erκ^E, and a round costs p/|Good| ≤ 2κ^E
  expected draws of E coset tests each. Exact least thresholds: `weil_thresholds.out`
  (E = 5 reproduces the Q1 referee's 61,524 and 3,748,116).

## 3. Lemma C (counts) [proved; exact check `dj_ineq.py` → `dj_ineq.out`]

(C0) D_J(x) ≥ 2 + D_J(x − 1) (take k = 1), so D_J is increasing; and D_J(x) ≥ x + 1 + D_J(x − J + 1)
for x ≥ J − 1 (take k = x).

(C1) For 0 ≤ m ≤ r and t = ⌊m/(J−1)⌋: **D_J(r) − D_J(r − m) ≥ t(r + 1) − (J − 1)t(t − 1)/2.**
Chain (C0) at x = r, r − (J−1), …, r − (t−1)(J−1) (each ≥ J − 1), then monotonicity.

(Y) If C ≥ 2, 1 ≤ b ≤ q and r ≥ q + b: b + (C − 1)r + D_J(q) − q ≥ F(b). Indeed the difference is
(C−1)(r−b) − q + D_J(q) − D_J(b) ≥ (C−2)q ≥ 0.

(I1) If c = 2(J−1), C ≥ 1, c + 1 ≤ m ≤ q and r ≥ 2q + 2:
(m − 1) + ⌊(m−1)/c⌋(r + 1 − c) + (r − 1) ≤ F(r) − F(r − m).
*Proof.* t = ⌊m/(J−1)⌋ ≥ 2, and m − 1 < (t+1)(J−1) gives ⌊(m−1)/c⌋ ≤ t/2. So LHS
≤ m − 2 + (t/2)(r+1) − t(J−1) + r. By (C1), RHS − LHS ≥ (t/2)(r+1) − (J−1)t(t−3)/2 + (C−1)m − r + 2.
If t ∈ {2, 3} the middle term is ≤ 0 and the rest is ≥ (r+1) − r + 2 > 0. If t ≥ 4, then
(J−1)(t−1) < m ≤ (r−2)/2, so (J−1)t(t−3)/2 < t(r−2)/4 and RHS − LHS > t(r+4)/4 − r + 2 > 0. ∎

(I2) If 2(J−1) ≤ m ≤ (r−2)/2: r − 1 ≤ F(r) − F(r − m). By (C1) with t ≥ 2 and (J−1)(t−1) < r/2,
RHS ≥ t(3r + 6)/4 ≥ (3r + 6)/2. ∎

(TS) If C ≥ 2J − 4 and 1 ≤ m′ ≤ m ≤ 2J − 3: m + m′ ≤ F(r) − F(r − m′). By (C0),
RHS ≥ (C + 2)m′ ≥ m′ + (2J − 3) ≥ m′ + m. ∎

`dj_ineq.out` verifies (Y) for r ≤ 300, (I1), (I2), (TS) for every r ≤ 1500, J ≤ 20, the fast
D_J recursion against the brute one, and the closed bound D_J(q) ≤ q²/(2(J−1)) + q(1/(J−1)+5/2).
It also records the least capacity c*(J) for which (I1) holds for all r ≤ 1500: c*(3) = 3,
c*(4) = 5, …, c*(20) = 26, always < 2(J−1) [exact for r ≤ 1500 only].

## 4. Lemma M (Rado flat) [proved; new]

*Setting.* A stall in case 3: ε ≥ 1, b ≥ q + 1 (so r ≥ 2q + 2 and |X| ≤ 2q + ε = r + q − b ≤ r − 1).
Let M₁ be the linear matroid on Rout (independence modulo U), of rank q − q⁺, and M₂ the
partition matroid whose parts are Rout ∩ S_l, with capacity c. By Lemma R, an absorption of load
≤ c reaching U⁺ is exactly a common independent set of size q − q⁺.

*Statement.* If the maximum common independent set I has |I| < q − q⁺, let Z ⊆ Rout attain
Edmonds' min–max |I| = r₁(Z) + r₂(Rout ∖ Z) [literature: Edmonds 1970; Schrijver, Combinatorial
Optimization, Thm 41.1; computed with the augmenting-path algorithm, Thm 41.2], and let
W = U + span(Z), q_W = r − dim W = q − r₁(Z). Then **c + 1 ≤ q_W ≤ q**, and the columns outside W
number at most (q_W − 1) + ⌊(q_W − 1)/c⌋(r + 1 − c) + (r − 1), which is ≤ F(r) − F(r − q_W) by (I1).
So W holds ≥ F(dim W) columns and the recursion on W applies.

*Proof.*
- Outside W lie only columns of Rout ∖ Z and of X: pool, B∩U and round columns in U lie in U ⊆ W,
  and Rout ∩ Z ⊆ W.
- r₂ := r₂(Rout∖Z) = |I| − r₁(Z) ≤ q − q⁺ − 1 − r₁(Z) ≤ q_W − 1.
- Let O_big be the rounds with |S_l ∩ (Rout∖Z)| > c. Each contributes c to r₂, the others their
  full size; and |S_l| ≤ r + 1 (a circuit mod U_{l−1}). So |Rout∖Z| ≤ r₂ + |O_big|(r + 1 − c) and
  c|O_big| ≤ r₂, which gives the bound.
- O_big ≠ ∅: otherwise r₂ = |Rout∖Z| ≥ r₁(Rout∖Z), so |I| ≥ r₁(Z) + r₁(Rout∖Z) ≥ r₁(Rout) = q − q⁺,
  a contradiction. Hence r₂ ≥ c and q_W ≥ r₂ + 1 ≥ c + 1. ∎

(The sharper |S_l| ≤ r − dim U_{l−1} + 1 is not needed. The columns lying in W need not span W,
since U is spanned by block sums that involve columns of Rout ∖ Z; the recursive call then runs
at the rank r″ ≤ dim W of those columns, with ≥ F(dim W) ≥ F(r″) columns because F is
increasing.)

The point that Q1 missed: the obstruction to a low load is not a single round but a set of rounds
O_big, and the min–max ties |O_big| to the codimension q_W of a flat they leave out, so the columns
those rounds put outside W (at most r + 1 each) are paid for by the q_W·r/(J−1) columns that
F(r) − F(r − q_W) provides. The Q1 fallbacks Y and U are the special cases W = span(B∩U) and Z = ∅.

## 5. Lemma T_m (top phase above a small codimension) [proved; new]

*Setting.* A flag (lower rounds, possibly absorbed) realizes H of codimension m ≥ 1 in V, every
round column lies in H, Fr = free columns with span(Fr) = V (B ⊆ Fr), X′ = Fr ∖ H. Reserve Z ⊆ X′,
a basis of V/H (it exists since Fr ∩ H ⊆ H). Run the greedy forward pass on X′ ∖ Z modulo the
current space H_cur ⊇ H with **singleton blocks**: a circuit S mod H_cur with |S| ≥ 2 becomes a top
round (a monochromatic one with e = 0 is a direct solution); a column in H_cur is set aside.

*Statement.* (a) If the top pass reaches V, the flag (lower + top rounds) with
Src = Fr ∖ (top supports) satisfies (F1), (F2) and (S); top rounds have ≤ m + 1 blocks.
(b) If it stalls at codimension m′ ≥ 1, at most m + m′ columns lie outside H_cur.
(c) In ALG-T the top phase is reached only with m ≤ J − 2 (found by the independent check): for
m ≥ J − 1, (C0) and monotonicity give F(r) − F(r − m) ≥ D_J(r) − D_J(r − J + 1) + Cm ≥ r + 1 + Cm
> r − 1 ≥ |X′|, so the U⁺-recursion of case 3.3 applies first. Hence top rounds have ≤ J − 1
blocks, (TS) is needed only for m ≤ J − 2, and **C = max(2, J − 3) already suffices** for
Theorem A [proved; the runs used C = max(2, 2J − 4)]. In particular T_m(b) needs J ≥ 4.

*Proof.* (F1)/(F2) for a singleton-block circuit mod H_cur are immediate (S ∖ {s₀} independent mod
H_cur, e ∈ H_cur). (S) for a lower pair is Lemma S (top rounds are singleton-blocked, span(Fr) = V).
(S) for a pair of top round j: φ vanishes on U_{j−1} ⊇ H ∪ (earlier top supports), and for a
singleton-blocked later round l, span(e_l) + Ω_l = span(S_l); so if φ vanished on Src and on every
e_l (l > j) it would vanish on H + span(X′ ∖ S_j) ⊇ H + span(Z) = V, contradicting φ ≠ 0 on V.
(b): outside H_cur lie only Z ∖ H_cur (≤ m columns) and the unused columns, which are independent
mod H_cur (≤ m′). ∎

## 6. ALG-T and Theorem A

**ALG-T** (`subquad.py: solve_T`). Zero column → solution. Run the forward pass of SSS(J)
(`forward_fast`, identical to `q1core.forward` on 570 cross-checked banks, `check_fast.out`).
Direct solution → return; reaches V → leaf (flag, B). At a stall, the first case that applies:

| case | condition | action | justification |
|---|---|---|---|
| 1 | ε = 0 | leaf (flag, Fin) | Lemma A (U ≠ 0) |
| 2 | b ≤ q | recurse on Y = span(B∩U) | cols(Y) ≥ b + π ≥ F(b) by (Y) |
| 3.0 | q⁺ ≥ 2(J−1) | recurse on U⁺ | outside ⊆ X, ≤ r − 1 ≤ F(r) − F(r−q⁺) by (I2) |
| 3.1 | max absorption (cap c) incomplete | recurse on W | Lemma M |
| 3.2 | complete, q⁺ = 0 | absorb; leaf (flag, B) | Lemma R; (S) as span(B) = V |
| 3.3 | complete, q⁺ = m ∈ [1, 2J−3] | absorb; then closure on U⁺ if Fr∩U⁺ spans it; else recurse on U⁺ if \|X′\| ≤ F(r) − F(r−m); else top phase: leaf, or recurse on H_cur | Lemma A; count; Lemma T_m with (TS) |

**Theorem A [proved].** Let κ ≥ 2, J ≥ max(κ, 2), c = 2(J−1), C = max(2, 2J−4), F(r) = D_J(r) + Cr,
E = 3J − 2, and let p ≡ 1 (mod κ) be prime. For every bank λ_1..λ_M ∈ F_p^a of rank r ≥ 1 with
M ≥ F(r), ALG-T runs in deterministic time poly(M, a, log p) and returns either a nonzero
x ∈ (P∪{0})^M with Σx_iλ_i = 0, or a leaf: a set of columns spanning a flat V′ of dimension
r′ ≤ r, a flag on them realizing V′ with blocks inside classes, at most E blocks per round
(lower rounds ≤ J + c, top rounds ≤ J − 1 by Lemma T_m(c)), (F1), (F2), and a nonempty Src outside the rounds
with span(Src) ⊆ V′ satisfying (S). If G*_E(p) ≥ 1, each back substitution from the leaf returns
a nonzero solution with probability ≥ 1 − (Er′/2)·max(1/G*_E(p), κ/(p−1)); for
p ≥ max(8κ^{2E}E², 2Erκ^E) this is ≥ 1/2 and each round costs ≤ 2κ^E expected draws.

*Proof.* Induction on r. r = 1: a stall would need π ≥ 2 pool columns in span(B∩U) with U = 0,
impossible, so the pass reaches V or returns a direct solution. For r ≥ 2 at a stall, §2 gives
π ≥ 2, b ≥ 1, U ≠ 0.
- Case 1: Lemma A.
- Case 2: Y ⊊ V has dim b ≥ 1 and holds B∩U and the pool, so ≥ b + π ≥ F(b) columns by (Y).
- Case 3: b ≥ q + 1 and ε ≥ 1, so r ≥ 2q + 2 and |X| ≤ r − 1. Columns outside U⁺ lie in X.
  3.0 by (I2). If q ≤ c every absorption basis has load ≤ q ≤ c, so 3.1 needs q > c and is
  Lemma M. In 3.2/3.3 Lemma R gives a flag realizing U⁺ with ≤ c extra blocks per round and every
  round column in U⁺. q⁺ = 0: span(B) = V gives (S). q⁺ = m ≤ 2J − 3: closure is Lemma A;
  the U⁺-recursion is valid by its count (outside U⁺ is exactly X′); otherwise Lemma T_m(a) gives a
  leaf, or T_m(b) with (TS) gives ≥ M − (m + m′) ≥ F(r − m′) columns in H_cur.
- Every recursion is on a proper flat holding ≥ F(its dimension) columns. The columns in it are
  written in coordinates of their own span (a linear isomorphism onto that span, which preserves
  solutions), whose rank r″ is at most the flat's dimension, so they number ≥ F(r″). A solution of
  the sub-bank extended by zeros solves the bank. Recursions do not branch, so the depth is ≤ r. Each level
  costs one forward pass (O(M + r) scans, Theorem 2(a)), O(M) spans, and one or two matroid
  intersections with a linear-algebra oracle, all polynomial.
- The failure bound is Lemma 2 with E_max = E, ρ ≤ Er′/2, and §2 for the prime range. ∎

**Corollary A** (§0 item 2) [proved]. F is increasing, so F(r) ≤ F(a) for every rank r ≤ a, and
F(a) ≤ a²/(2(J−1)) + a(1/(J−1) + 5/2) + (2J−4)a by the closed bound. With J = ⌈log_κ a⌉ ≥ κ:
κ^J < κa, so κ^E = κ^{3J−2} < κa³, the expected time is polynomial, and the prime bound is
8κ^{2E}E² < 72κ²a⁶J² and 2Eaκ^E < 6Jκa⁴. (This uses J = ⌈log_κ a⌉, i.e. a ≥ κ^{max(κ,3)};
for smaller a, J ≤ max(κ, 3) is a constant.) The κ-th roots and Bezout exponent of
`prop:triangular-sde` convert x to a solution of the target.

## 7. Numbers

| a | κ | J | F(a) = D_J(a) + C_J a | triangular (a+1)(a+2)/2 | J = 3: ⌊(a+2)²/4⌋ + 2a | F(a) / (a²/(2(J−1))) |
|---|---|---|---|---|---|---|
| 16 | 2 | 4 | 122 | 153 | 113 | 2.86 |
| 64 | 2 | 6 | 970 | 2145 | 1217 | 2.37 |
| 256 | 2 | 8 | 7924 | 33153 | 17153 | 1.69 |
| 1024 | 2 | 10 | 75272 | 525825 | 265217 | 1.29 |
| 1024 | 3 | 7 | 98309 | 525825 | 265217 | 1.13 |

(`dj_ineq.out`.) The linear term C_J a = (2J−4)a dominates the gain only for small a; the ratio
tends to 1. The Chevalley–Warning existence threshold is κa + 1.

## 8. Does the steering machinery scale to J = Θ(log a)? [proved, §2]

Yes. Lemma W is uniform in E (only the term count κ^e − 1 grows); Lemma 2 never uses E except
through G*_E; ρ ≤ Er/2 grows linearly; the cost per round is 2κ^E draws of E coset tests. With
E = 3J − 2 and J = ⌈log_κ a⌉ every one of these is polynomial in a. The exact least primes for
G*_E ≥ p/(2κ^E) from Lemma W are in `weil_thresholds.out`; they are 2.5–3× below 8κ^{2E}E².

## 9. Computations

All runs used `nice -n 10`, at most two processes, exact arithmetic, strict mode (every inequality
used by the proof asserted at run time: Theorem 2(b) decomposition, (Y), (I1) with the Lemma M
bound and its certificate r₁(Z) + r₂ = |I|, (I2), (TS), load ≤ c, the outside-count of every
recursion), (F1)/(F2) and (S) (`steer_bad = 0`) at every leaf, and every witness verified. Budget
M = F(r) exactly unless stated. Primes 10007 (κ = 2) and 100003 (κ = 3).

| artifact | banks | what | result |
|---|---|---|---|
| `check_fast.out` | 570 | `forward_fast` vs reference `q1core.forward`, 12 families, J ∈ {3,4,5}, a ≤ 9 | 0 mismatches |
| `heavy_1.out` | 8 | Q1 heavy stalls `heavy_found_3.jsonl` (κ = 2, a = 7), J = 3 | 8/8; now case 2 (b = 2 ≤ q = 3) |
| `fams_1.out` | 512 | the 12 Q1 families + proportional, nested, half-rank-dense, repeated; κ ∈ {2,3}, J ∈ {3,4}, a ∈ {8,11,12,14,16} | 512/512 |
| `planted_1.out` | 56 | one or two early full circuits keeping Q − J + 1 private directions, then E′-rounds, then pool (± proportional copies); r ∈ {14,…,24} | 56/56; 32 Rado-flat recursions; least load up to 9 |
| `vtwist_1.out` | 10 | planted + v-twisted rounds (r ∈ {24,28,30}, Q = 8): least load 6 > c = 4 | 10/10 by W; U-count fails on 6, U- and Y-counts both fail on 2 |
| `topbank_1.out`, `topbank2_1.out` | 36 + 16 | complete absorption leaving q⁺ ∈ {1,…,4}; J = 4, r = 40 degenerate tops | all solved; top-phase leaves, U⁺-, H-recursions, closure on U⁺ |
| `vtwist2_2.out` | 10 | vtwist at r ∈ {32, 36, 40}, J ∈ {3, 4}, least load 6–10 | 10/10 by W; U-count fails on 5, U- and Y-counts both fail on 4 |
| `thmprime_1.out` | 62 | planted, vtwist, topbank and the 12 families at a ∈ {11, 12}, J = 3 (E = 7), at p = 2,330,021 (κ = 2) and p = 689,000,047 (κ = 3) | 62/62; 10 W-recursions (2 with U-count failing); 0 single-pass failures |
| `critical_1.out` | 33 | Q1-search critical banks (`chain4`, `chainfull`), padded to F(a) by proportional copies | 33/33; 16 closures (case 1), 17 reach V |
| `climb_1.out` | 243 | hill climb maximising the least absorption load, κ = 2, J = 3, a = 12 | 243/243, least load ≤ 4 reached by climbing |
| `stress_1.out` | 80 | capacity c = 1 (below the theorem), strict off | 80/80; 54 W-events, every one still had ≥ F(dim W) columns |
| `check/adv_*.out` (independent check) | 277 | top-phase stall (J ∈ {4,5}), several over-capacity rounds, perturbed orders, climb | 277/277; 118 W-recursions, 20 top-stall recursions (the only runs of T_m(b)); 1 single-pass failure |
| `dj_ineq.out` | — | Lemma C inequalities, J ≤ 20, r ≤ 1500 | all hold |
| `weil_thresholds.out` | — | least primes from Lemma W, E ∈ {5,…,16} | §2 |

Single-pass failures: 0 in all 986 strict runs here; 1 in the check (`adv_multibig_1.out`,
p = 100003, below the theorem's range). Totals: 986 strict + 80 stress `solve_T` runs here, 277
strict in the check, plus 570 + 72 forward-pass cross-checks. Branch coverage here: case 1
closure, case 2 (Y), 3.0 (U⁺), 3.1 (W), 3.2, closure on U⁺, H-recursion and top-phase leaves at
m = 1; the top-stall branch T_m(b) only in the check.

## 10. Limits and what (d) would have to show

- **The absorption load alone is unbounded [proved for the planted family; exact on the
  instances].** In `planted(r, [Q])` all of Rout lies in the first round and has rank Q − J + 1
  mod U, so every complete absorption has load Q − J + 1 ≈ r/2 for Q ≈ r/2; on the computed
  instances the least load (matroid intersection with increasing capacity) is 6–10. So "c = O(1)
  without new recursion" is false, and Theorem A needs the Rado flat.
- **Θ(a²/log a) is the limit of this design [argued].** A round with n blocks realizes ≤ n − 1
  directions at cost κ^n; for polynomial cost n = O(log a). On banks whose columns are in general
  position modulo every realized space (the hypothesis of `rem:sde-subquadratic`(a)), a round at
  quotient q needs ≥ q + 1 columns, so any flag with ≤ n blocks per round uses
  ≥ Σ_i (a − i(n−1) + 1) ≈ a²/(2(n−1)) columns. Going below a²/log a needs rounds with
  multi-dimensional relation spaces or a non-flag scheme.
- **Not uniform in p.** Every statement needs G*_E(p) ≫ Er, i.e. p ≥ poly(a).

## 11. Claim gates, next question, next command

Gates that must stay false:
- "Uniform in p", or anything at p = 3 or κ = p − 1.
- "o(a²) is necessary, or a²/log a is optimal" (only argued for flag schemes, §10).
- "The paper's proved arity changed": the paper still says (a+1)(a+2)/2; Theorem A is AI-checked
  only, pending human review and owner decision.
- Any novelty or priority claim (the large-p diagonal-system literature was not searched here).

Next hard question: (i) human check of Lemma M and of Lemma 2 with absorbed blocks; (ii) does a
capacity c = O(1) (independent of J) suffice with a sharper Rado count, which would give
E = J + O(1) and prime exponent ~2 instead of ~6? In the stress run with c = 1 every one of 54
W-events still had enough columns (`stress_1.out`), but (I1) is false for c = 1 at large r, so
this needs either a sharper bound on the columns of O_big outside W or a different flat; (iii) primes p = a^{O(1)} with a smaller
exponent, or the label law of `lem:s3-law` (i.i.d. on K_d^⊥), where `rem:sde-block-steered`
already gives M_J.

Next command: `cd research/audits/reviews/2026-11-07-rees-sde-subquad-A && nice -n 10
/opt/anaconda3/bin/python -B run_tests.py vtwist 2` with r ∈ {32, 36, 40} and J = 4 shapes;
expected artifact `vtwist_2.out`; acceptance: all strict asserts pass and every bank whose least
load exceeds c is solved by the W branch.

## 12. Independent adversarial check

A fresh general-purpose subagent was given this report (§§2–6), the Q1, Q1-check and worst-case
reports, and the code, with ten obligations (a)–(j). It wrote only to
`2026-11-07-rees-sde-subquad-A/check/` and modified no existing file.

| item | verdict | action |
|---|---|---|
| (a) Lemma M | holds; certificate, outside-W bound, O_big ≠ ∅ and q_W ≥ c + 1 re-derived; the partition-matroid model matches Lemma R singleton absorption exactly | none |
| (b) counts (C1), (Y), (I1), (I2), (TS) | hold; own exact check J = 2..14, r ≤ 800 (`check/ineq_check.out`); (Y) and (TS) are tight (slack 0) but valid | none |
| (c) case 2 at b ≤ q | holds | none |
| (d) case 3 bookkeeping | holds | none |
| (e) Lemma T_m | holds; **the stall branch T_m(b) had never run**; top phase only at m ≤ J − 2 | added T_m(c) and the sharper C = max(2, J − 3); its own `adv_topstall` ran T_m(b) 20 times |
| (f) Lemma 2 with up to 3J − 2 blocks | holds; no hidden use of circuits, J or block count | none |
| (g) Lemma W at E = Θ(log a) | holds; **arithmetic slip** "p/(2√2) + 0.15p ≤ p/2" (0.5036) | fixed to p/100 (E < 0.002p there) |
| (g′) Corollary A scope | **"κ^E < κa³ once a ≥ κ³" false for κ ≥ 4** (κ = 4, a = 64: equality) | fixed: fixed κ, a > κ^{max(κ,3)−1} |
| (h) recursion | holds; wording: the columns in W need not span W | fixed in §4 and §6 |
| (i) code | faithful; `forward_fast` = reference on 72 more banks | none |
| (j) breaking attempts | no counterexample in 277 strict runs; smallest recursion slack 15 columns | recorded in §9 |
| placeholder | "1,4xx banks" in §0 | fixed |

Residual verdict of the check: Theorem A and Corollary A (fixed κ) hold as stated; both reports
are AI-only, and Lemma M and Lemma 2 with absorbed blocks still need a human reader.
