# Referee report: Theorem A / Corollary A of `2026-11-07-rees-sde-subquad-A.md` (Rees diagonal SDE, worst case below a²)

Adversarial, unanchored AI referee pass, 7 November 2026, pending human review. Under review: the
report `2026-11-07-rees-sde-subquad-A.md` and its folder `2026-11-07-rees-sde-subquad-A/`
(the agent's code was run only as the object under test). Inputs re-read in full:
`2026-11-05-rees-sde-q1.md` and `-q1-check.md`, `2026-11-05-rees-sde-worst-case.md`,
`2026-11-05-rees-sde-two-relation.md`, `appendix-sde-side.tex` ll. 33–87. Scripts and outputs of
this check are in `2026-11-07-rees-sde-subquad-A-referee/`; nothing else was written (no git, no
`.tex`, no STATE/handoff, `make_numbers.py` not run). Interpreter `/opt/anaconda3/bin/python`,
all runs under `nice -n 10`, at most two processes.

**Independent code.** `ref_alg.py` re-implements ALG-T from the text of the report and imports
nothing from the agent's folders: own echelon linear algebra, own forward pass with different tie
rules (the swap removes the *last* eligible reserved column; blocks split the *smallest* class and
peel its *last* element), own augmenting-path matroid intersection with the Edmonds certificate
verified (and a brute-force cross-check on small instances), absorption in reverse order, own
(F1)/(F2) and (S) checks, own backward pass and witness verifier. Every inequality of the proof is
asserted at run time. `ref_ineq.py` and `ref_weil.py` are exact integer/rational checks of
Lemma C and of the Lemma W consequences.

## 0. Verdict

**CORRECT.** Theorem A and Corollary A hold as stated. I re-derived every lemma from scratch
(§1 below), found no error in any proof step, and my independent implementation produced
0 assertion failures and 0 unsolved banks on 76 planted heavy stalls (68 Rado-flat recursions,
37 with W ≠ U, up to two over-capacity rounds), on 61 banks from the agent's and its checker's
generators (top phase, top-phase stall, complete absorptions, every branch of ALG-T), and on
168 random/degenerate banks. The
small-prime Lemma 2 test with absorbed blocks (p = 257) is consistent with the bound by a factor
of more than 10 and every failing pass had a cross-class coincidence, as the proof requires.

What remains is only presentational (§3): a few imprecise sentences, none affecting a claim.
The claim gates listed in the report's §11 are right and must stay: nothing here is uniform in p,
nothing is said at p = 3 or κ = p − 1, and the arity statement is "provable by these methods",
not optimal.

Weakest links, for a human reader, in order: (1) Lemma 2's first-coincidence conditioning
(standard, but the one place where probability enters; re-derived in §1(a)); (2) Lemma M's
accounting of the columns outside W (elementary; re-derived in §1(c)); (3) the chain of case
conditions in ALG-T (§1(e)).

## 1. The obligations (a)–(i)

### (a) Lemma 2 (steering without circuits) with absorbed singleton blocks, up to 3J − 2 blocks: HOLDS

Re-derivation. Let rounds 1..L be a flag (disjoint supports, blocks inside classes, (F1), (F2)),
U_L = Ω_1 ⊕ … ⊕ Ω_L (direct by (F1), inductively), Src outside all rounds with span(Src) ⊆ U_L,
n_l ≤ E_max, G*_{E_max}(p) ≥ 1.

- *Values.* With τ_l ∈ U_l written uniquely as Σ_{b≥1} β_b W^{(l)}_b + τ′, τ′ ∈ U_{l−1} (unique by
  (F1)), and x_i = δ_i(β_{b(i)} + s) with β_0 = 0: Σ_{i∈S_l} x_iλ_i = Σ_b (β_b + s) W_b =
  Σ_{b≥1} β_bW_b + s·e_l, and x_i ∈ P ∪ {0} iff β_b + s ∈ Q°_{−c_b}, c_b = cos δ_i for i ∈ G_b.
  Only the "if" direction of Theorem B(ii) is used and it is elementwise: it needs the blocks to
  lie inside classes and nothing else. Absorbed singleton blocks carry the class of their δ_i, so
  they are covered. τ_{l−1} = τ′ − s e_l ∈ U_{l−1} by (F2).
- *Telescoping.* Σ_l(τ_l − τ_{l−1}) + Σ_σ t_σσ = τ_L − τ_0 − τ_L = 0 since U_0 = 0; x ≠ 0 since
  Src ≠ ∅ and t_σ ∈ P.
- *Functionals.* Π_j: U_L → U_j the coordinate projection along Ω_{j+1} ⊕ …; by induction
  τ_j = Π_j(τ_L) − Σ_{l>j} s_l Π_j(e_l) (uses Π_j∘Π_{j+1} = Π_j and e_{j+1} ∈ U_j). The offset
  difference at (j, b, b′) is F = −Σ_σ t_σφ(σ) − Σ_{l>j} s_l φ(e_l) with
  φ = (coord_b − coord_{b′})∘(Ω_j-coords)∘Π_j, nonzero on U_L (onto Ω_j, basis W^{(j)}_{1..}).
- *Failure needs a cross-class coincidence.* Without one at level l, equal same-class offsets
  merge and ≤ n_l ≤ E_max distinct offsets with arbitrary classes remain, so |Good_l| ≥ G*_{E_max} ≥ 1
  by the definition of G* (which includes all-equal classes). With one, Good_l ⊆ {−β_b} is tested
  directly.
- *First coincidence.* Fix a tie rule; the failure event is contained in the disjoint union over
  cross pairs of A_{j,bb′} = {F_{j,bb′} = 0} ∩ {no cross-class coincidence at any level > j}.
  Case 1: some l > j has φ(e_l) ≠ 0; m := least such l (= the last-drawn variable with a nonzero
  coefficient). A_{j,bb′} ⊆ {F = 0} ∩ {no coincidence at levels ≥ m}; the second event is
  measurable in the history H = (t, s_L, …, s_{m+1}); on it, s_m is drawn uniformly from
  Good_m(β^{(m)}(H)) of size ≥ G*; F = α(H) − s_m φ(e_m) because the coefficients of
  s_{m−1}, …, s_{j+1} vanish by minimality of m; so P[A] ≤ E[1_{…} P(F = 0 | H)] ≤ 1/G*. Case 2:
  all φ(e_l) = 0 for l > j; by (S) some σ ∈ Src has φ(σ) ≠ 0, the t_σ are i.i.d. uniform on P, so
  P[F = 0] ≤ κ/(p − 1). Summing over the ρ cross pairs gives the bound.

Nothing in this uses the circuit property, J, or the number of blocks except through n_l ≤ E_max
in |Good_l| ≥ G*_{E_max}, and ρ ≤ Σ_l C(n_l, 2) ≤ (E_max/2)Σ_l(n_l − 1) = E_max·dim U_L/2. (F1) for
absorbed flags is Lemma R, (b) below. The report's three re-derivation points (i)–(iii) in its §2
are correct.

Empirical check (`ref_lemma2_1.out`): κ = 2, J = 2, p = 257 (G*_3(257) ≥ 26 by the worst-case
report's exact table), 350 flags each with one absorbed singleton block (a 3-block round), Src = B.
First-pass failures 4 against a summed Lemma-2 bound of 50.4; over 7,000 passes 19 failures, and
**every** failing pass had a cross-class coincidence. Consistent with the proof, with a wide margin.

### (b) Lemma R (absorption) and Lemma A (closure) on absorbed flags: HOLDS

Lemma R re-derived: with i ∈ G_{l,b}, |G_{l,b}| ≥ 2, λ_i ∉ U_L, the new generators of round l are
W′_b = W_b − δ_iλ_i (b ≥ 1) or unchanged (b = 0) and W′_{n_l} = δ_iλ_i; their span together with
U_{l−1} is exactly U_l + Fλ_i, so by induction U′_{l′} = U_{l′} + Fλ_i for l′ ≥ l and
U′_L = U_L ⊕ Fλ_i. It is spanned by Σ_{l′}(n_{l′} − 1) + 1 = dim U_L + 1 generators, which are
therefore a basis, giving (F1) for every round; (F2) holds since each e_{l′} ∈ U_{l′−1} ⊆ U′_{l′−1}
and e_l, δ are unchanged; the new block has the class of δ_i. Singleton blocks lie in U_l
(b ≥ 1: δ_iλ_i = W_b; b = 0: δ_iλ_i = e_l − Σ_{b≥1}W_b), so a column outside the current realized
space is always in a block of size ≥ 2 and any I ⊆ Rout independent modulo U can be absorbed in
any order, giving U ⊕ span(I) with |I ∩ S_l| extra blocks in round l. My code absorbs in reverse
order and re-verifies (F1)/(F2) after each step: 0 violations in all runs.

Lemma A: for any flag realizing U_t ≠ 0 and Src = Fr_t ∩ U_t spanning U_t, each φ_{j,bb′} is a
nonzero functional on U_t, hence nonzero on span(Src); so (S) holds without even using the e_l.
This is used for the unabsorbed flag (case 1) and for the absorbed flag realizing U⁺
("closure on U⁺"); both are flags, U ≠ 0 because b ≥ 1 (π ≥ 1 ⇒ pool ⊆ span(B∩U) ≠ 0) and
U⁺ ⊇ U. Corollary A of Q1 (pool ⊆ span(B∩U), Fin = (B∩U) ∪ pool spans span(B∩U), |B∖U| = q + ε)
re-derived: swaps only remove σ ∈ B∖U_{l′} and U grows, so B_l ∩ U_l ⊆ B_L ∩ U_L; T ∩ U = ∅;
B independent so b = dim span(B∩U) and |B∖U| = r − b = q + ε.

### (c) Lemma M (Rado flat): HOLDS

- *Model.* M₁ = linear matroid on Rout modulo U, rank dim U⁺ − dim U = q − q⁺; M₂ = partition
  matroid by rounds with capacity c. By Lemma R, absorptions of load ≤ c reaching U⁺ are exactly
  the common independent sets of size q − q⁺. Edmonds' min–max (Schrijver Thm 41.1) gives Z with
  |I| = r₁(Z) + r₂(Rout∖Z); W := U + span(Z), q_W = q − r₁(Z).
- *Columns outside W.* pool ⊆ span(B∩U) ⊆ U (a true-pool column has circuit {c}, i.e. c ∈ U),
  B∩U ⊆ U, round columns in U, and Rout ∩ Z ⊆ W; so only (Rout∖Z) ∪ X can lie outside, with
  X = (B∖U) ∪ T, |X| ≤ (q + ε) + q = r + q − b ≤ r − 1 in case 3 (b ≥ q + 1).
- *r₂ := r₂(Rout∖Z) = |I| − r₁(Z) ≤ q − q⁺ − 1 − r₁(Z) = q_W − q⁺ − 1 ≤ q_W − 1.*
- *O_big.* r₂ = c|O_big| + Σ_{l∉O_big}|S_l ∩ (Rout∖Z)|, so |Rout∖Z| = r₂ + Σ_{l∈O_big}(|S_l ∩ (Rout∖Z)| − c)
  ≤ r₂ + |O_big|(r + 1 − c) with c|O_big| ≤ r₂ and r + 1 − c ≥ 0 (r ≥ 2q + 2 > c). Hence
  |Rout∖Z| ≤ (q_W − 1) + ⌊(q_W − 1)/c⌋(r + 1 − c).
- *|S_l| ≤ r + 1.* The support of round l is a circuit modulo U_{l−1} with S_l∖{c} ⊆ T independent
  modulo U_{l−1}, so |S_l| ≤ (r − dim U_{l−1}) + 1 ≤ r + 1, where r is the rank of the bank in
  which the forward pass ran, i.e. of the current (sub-)bank; absorption does not change supports.
- *O_big ≠ ∅ and c + 1 ≤ q_W ≤ q.* If O_big = ∅, r₂ = |Rout∖Z| ≥ r₁(Rout∖Z) and
  |I| ≥ r₁(Z) + r₁(Rout∖Z) ≥ r₁(Rout) = q − q⁺ by subadditivity of rank, contradicting
  incompleteness. So r₂ ≥ c and q_W ≥ r₂ + 1 ≥ c + 1; q_W ≤ q since r₁(Z) ≥ 0.
- *Recursion.* Columns in W ≥ F(r) − bound ≥ F(r − q_W) = F(dim W) by (I1), whose hypotheses
  c + 1 ≤ q_W ≤ q ≤ (r − 2)/2 hold; the sub-bank has rank r″ ≤ dim W < r and F is increasing.
  (The report's parenthetical that the columns in W need not span W is right; U is spanned by
  block sums involving columns of Rout∖Z. My runs confirm this: the sub-bank's rank was usually
  below dim W.)

Checked at run time by my code on every W-event (68 in `ref_planted_1.out`): certificate
r₁(Z) + r₂ = |I| (plus a brute-force maximum on instances with |Rout| ≤ 11), set-inclusion
outside(W) ⊆ (Rout∖Z) ∪ X, r₂ ≤ q_W − 1, O_big ≠ ∅, c|O_big| ≤ r₂, |S_l| ≤ r + 1, the
outside-W bound, c + 1 ≤ q_W ≤ q, (I1), and the recursion count. 0 violations. Instances with
|O_big| = 2 (two over-capacity rounds) and with W ≠ U (twisted rounds, 37 instances) were included.

### (d) Lemma C: HOLDS (by hand and by my code)

By hand: (C0) from k = 1 and k = x in the definition; (C1) by chaining (C0) t times (each
argument r − i(J−1) ≥ J − 1 since t(J−1) ≤ m ≤ r) then monotonicity; (Y): difference
= (C−1)(r−b) − q + D_J(q) − D_J(b) ≥ (C−2)q ≥ 0 using r − b ≥ q and monotonicity (tight at C = 2,
b = q, r = 2q); (I1): t ≥ 2, ⌊(m−1)/c⌋ ≤ t/2 from m − 1 < (t+1)(J−1), then the displayed
RHS − LHS ≥ (t/2)(r+1) − (J−1)t(t−3)/2 + (C−1)m − r + 2, positive for t ∈ {2,3} (middle term ≥ 0,
rest ≥ 3) and for t ≥ 4 (using (J−1)(t−1) < m ≤ (r−2)/2); (I2) and (TS) as in the report (the
report's "(3r+6)/4" in (I2) is right; it uses m ≤ (r−2)/2).

By code (`ref_ineq.py` → `ref_ineq.out`, D_J from the literal definition, exact integers and
rationals): (C0), monotonicity of F, (C1) for all 0 ≤ m ≤ r, π ≥ 2, (Y) (r ≤ 500), (I1), (I2),
(TS), and the sharper (TS′) with C′ = max(2, J−3) and m ≤ J − 2 (Lemma T_m(c)), the
top-reachability inequality F(r) − F(r−m) > r − 1 for m ≥ J − 1 and r ≥ 2m + 2, the closed bound
D_J(q) ≤ q²/(2(J−1)) + q(1/(J−1) + 5/2) (J ≥ 3), and F(a) ≤ a²/(2(J−1)) + a(2J − 3/2 + 1/(J−1)):
**all hold for every J ∈ [2, 30] and r ≤ 2500** (0 violations). Edge cases: J = 2 (c = C = 2,
(TS) slack 2), J = 3 (C = 2; (Y) and (TS) tight with slack 0 at (r, q, b) = (2k, k, k) and
(m, m′) = (3, 1)); (I1) has slack ≥ 14 everywhere, least at J = 2; D_3(q) = ⌊(q+2)²/4⌋ and
D_2(q) = (q+1)(q+2)/2 − 1 confirmed to q = 60. Tightness of (Y) and (TS) is real but harmless:
the inequalities are used as "≥".

### (e) Completeness of the ALG-T case analysis and the §2 derivation: HOLDS

§2: at a stall the columns partition into B (r), round columns, pool (π) and the unused set T
(every column is in exactly one of these; swapped-out columns return to the unused list). T is
exactly the last scan's independent list, so |T| ≤ q. Each round at quotient q′ consumes k + 1
columns with 1 ≤ k ≤ q′ (S∖{c} ⊆ T) and gains n_l − 1 = min(J−1, k) by Theorem B(i), so
(cost) + D_J(q′ − gain) ≤ D_J(q′) and telescoping gives |Rcols| ≤ D_J(r) − D_J(q). Hence
π = M − r − |Rcols| − |T| ≥ (C−1)r + D_J(q) − q ≥ r + 1 ≥ 2, whence b ≥ 1, U ≠ 0, r ≥ 2. All of
this was asserted by my code at every stall (84 stalls): 0 violations.

Cases: ε = 0 → 1 (Lemma A, U ≠ 0). Else ε ≥ 1; b ≤ q → 2 ((Y) needs only C ≥ 2, 1 ≤ b ≤ q,
r ≥ q + b, all automatic; Y proper since r ≥ 2b > b). Else b ≥ q + 1, ε ≥ 1, so r ≥ 2q + 2 and
|X| ≤ r − 1; columns outside U⁺ lie in X. q⁺ ≥ c → 3.0 ((I2): c ≤ q⁺ ≤ q ≤ (r−2)/2 automatic).
Else q⁺ ≤ c − 1 = 2J − 3; matroid intersection incomplete → 3.1 (Lemma M; (I1) hypotheses
automatic); complete, q⁺ = 0 → 3.2 (Src = B spans V); complete, 1 ≤ q⁺ = m ≤ 2J − 3 → 3.3:
closure on U⁺ (Lemma A) or U⁺-recursion (count checked) or top phase. T_m(c): for m ≥ J − 1,
F(r) − F(r−m) ≥ (r+1) + Cm > r − 1 ≥ |X′| (needs r ≥ J − 1, true as r ≥ 2m + 2), so the
U⁺-recursion fires first and the top phase has m ≤ J − 2 (my code asserts this). In the top phase
the outcomes are direct solution, leaf (T_m(a)), or stall at 1 ≤ m′ ≤ m with ≤ m + m′ columns
outside H_cur and (TS) (hypotheses 1 ≤ m′ ≤ m ≤ 2J − 3 automatic). No stall falls outside the
cases and no case is entered with a failing count hypothesis.

### (f) Lemma T_m: HOLDS

(a) (F1)/(F2) for a singleton-blocked circuit modulo H_cur are immediate. (S) for lower pairs is
Lemma S: φ_{j,bb′} (defined on V via the full flag) is nonzero on V and vanishes on every top Ω_l;
for a singleton-blocked round span(e_l) + Ω_l = span(S_l); so vanishing on Src and on all e_l
(l > j) means vanishing on Src ∪ (top supports) = Fr, which spans V (B ⊆ Fr), contradiction. (S)
for a top pair of round j: φ vanishes on U_{j−1} ⊇ H ∪ (earlier top supports); vanishing on Src
and on e_l for later top rounds l forces vanishing on their supports; Z ⊆ Src (Z is reserved,
never scanned) and set-aside columns ⊆ Src; hence φ vanishes on H + span(X′∖S_j) ⊇ H + span(Z)
= V, contradiction. Top rounds have ≤ (codim H_cur) + 1 ≤ m + 1 ≤ J − 1 blocks. Src ⊇ Z ≠ ∅.
(b) Outside H_cur: lower round columns (⊆ H), top round columns (⊆ H_cur after their round),
set-aside columns, Fr ∩ H are all inside; only Z∖H_cur (≤ m) and the unused list (independent
modulo H_cur, ≤ m′) remain. My code asserts the outside count and (TS) at every top-phase stall.

### (g) The recursion: HOLDS

Every recursion is on the columns lying in a proper flat W (Y, U⁺, W, H_cur), with
≥ F(dim W) columns; the sub-bank's rank r″ ≤ dim W < r and F(r″) ≤ F(dim W), so the induction
hypothesis applies with no coordinate change needed. Depth ≤ r, no branching, each level
polynomial (forward pass O(M + r) scans of O(M) eliminations; one matroid intersection with a
rank oracle; the agent's extra "least load" loop is a diagnostic and also polynomial). A nonzero
solution of the sub-bank extended by zeros is a nonzero solution of the bank. Termination and the
dimension drop were asserted by my code at every recursion.

### (h) Corollary A arithmetic: HOLDS

F(a) = D_J(a) + Ca with C = 2J − 4 (J ≥ 3) ≤ a²/(2(J−1)) + a(1/(J−1) + 5/2 + 2J − 4), which is the
report's bound (verified exactly for J ≤ 24, a ≤ 1500); with J = ⌈log_κ a⌉ this is O(a²/log a).
J = ⌈log_κ a⌉ < log_κ a + 1 gives κ^J < κa and κ^E = κ^{3J−2} < κa³; then 8κ^{2E}E² < 72κ²a⁶J² and
2Eaκ^E < 6Jκa⁴. J = ⌈log_κ a⌉ ≥ max(κ, 3) iff a > κ^{max(κ,3)−1}; for smaller a, J = max(κ, 3) is a
constant. Lemma W: for every e ≤ E, κ^{−e}(p − e − (κ^e − 1)(e − 1)√p) ≥ p/(2κ^E) once
p ≥ 8κ^{2E}E² (`ref_weil.py`: exact integer check for κ ≤ 5, E ≤ 30, at the threshold and on a
grid above it); the report's "(κ^E − 1)(E − 1)√p + E ≤ p/(2√2) + p/100 ≤ p/2" is right. Per-pass
failure ≤ (Er/2)(2κ^E/p) ≤ 1/2 iff p ≥ 2Erκ^E, and κ/(p−1) ≤ 2κ^E/p for E ≥ 2, so the max is the
G* term. Exact least primes from Lemma W (`ref_weil.out`): E = 5: 61,524 (κ = 2) and 3,748,116
(κ = 3), reproducing the Q1 referee; E = 7: 2,322,604 (κ = 2) and 688,117,852 (κ = 3), so
Corollary A₃'s "2.33·10⁶" and "6.89·10⁸" are safe roundings up, and 1792r, 30618r are exact. The
agent's thmprime primes 2,330,021 and 689,000,047 lie inside the range. Corollary A₃ uses J = 3 ≥ κ
for κ ∈ {2, 3}, D_3(r) = ⌊(r+2)²/4⌋, C = 2, E = 7, c = 4: consistent with Theorem A.

### (i) Hidden assumptions, circularity: none found

No general position anywhere (the forward pass takes circuits of the actual columns; stalls are
handled by counting). The only randomness is in the back substitution (t_σ, s_l); the reduction is
deterministic given the fixed splitting rule, and any fixed rule works (my rule differs from the
agent's and all asserts pass). The induction is on rank only; the lemmas do not depend on
Theorem A. J ≥ κ is needed and stated (a circuit's dependency meets ≤ κ classes, so min(J, |S|)
blocks inside classes exist). p ≡ 1 (mod κ) is implicit in κ | p − 1. Zero columns are returned
as solutions; repeated and proportional columns are allowed and were tested.

## 2. Computations

| artifact | what | result |
|---|---|---|
| `ref_ineq.py` → `ref_ineq.out` | Lemma C, (TS′), top-reachability, closed bounds; J ∈ [2, 30], r ≤ 2500 ((Y): r ≤ 500); D_J from the literal definition | 0 violations; tight cases of (Y), (TS) listed; §7 numbers of the report reproduced (122, 970, 7924, 75272, 98309) |
| `ref_weil.py` → `ref_weil.out` | Lemma W consequence p ≥ 8κ^{2E}E² ⇒ G*_E ≥ p/(2κ^E), κ ≤ 5, E ≤ 30, exact integers; least primes for E ∈ {5,…,10} | holds; 61,524 / 3,748,116 (E = 5), 2,322,604 / 688,117,852 (E = 7) |
| `ref_run.py random 1` → `ref_random_1.out` | independent ALG-T on 168 random, proportional/repeated and nested banks at M = F(r), κ ∈ {2,3}, J ∈ {3,4}, r ≤ 12 | 168/168; 123 reach V, 45 direct; no stall |
| `ref_run.py planted 1` → `ref_planted_1.out` | referee's planted heavy stalls: one or two full circuits with q > c private directions, twisted E′-rounds (fresh unrealised direction cancelled inside every block of the referee's split rule), proportional pool copies; κ ∈ {2,3}, J ∈ {2,3,4}, r ≤ 44, p ∈ {1009, 10007, 10009} | **76/76, 0 assertion failures**; 84 stalls; 68 Rado-flat recursions (least load up to 11 > c; 37 with W ≠ U; |O_big| = 2 on 12); 16 complete absorptions at load ≤ c (rounds of up to 10 blocks), leaf (flag, B); recursion slack ≥ 21 columns; one 10-block leaf at p = 10009, κ = 3 needed 15 passes (far below the theorem's prime range, where the bound is vacuous) |
| `ref_run.py lemma2 1` → `ref_lemma2_1.out` | Lemma 2 with an absorbed singleton block at p = 257, κ = 2, J = 2 | 350 leaves; 4 first-pass failures vs summed bound 50.4; 19/7000 failures, all with a cross-class coincidence |
| `ref_run.py agent 1` → `ref_agent_1.out` | banks from the agent's generators (`planted`, `vtwist`, `topbank` incl. the degenerate shapes; J ∈ {3,4}, r ≤ 40, p ∈ {10007, 100003}), solved by the referee's code with its own tie rules | **54/54, 0 assertion failures**; 92 stalls; 9 W-recursions, 65 absorptions (load ≤ c), 36 U⁺-recursions from case 3.3, 6 from case 3.0, 10 Y-recursions, 7 closures on U⁺, 2 closures, 4 top-phase leaves; least recursion slack 0 (count tight, holds) |
| `ref_run.py adv 1` → `ref_adv_1.out` | banks from the check's `topstall` and `multibig` generators (J ∈ {3,4,5}, r ≤ 46) | **7/7, 0 assertion failures**; the top-phase stall branch T_m(b) ran once (`rec:topstall`, (TS) asserted, slack 15), 2 top leaves, 2 W-recursions with \|O_big\| = 2, absorptions with 9-block rounds |
| `run_tests.py heavy 7`, `run_tests.py topbank2 5` (agent's code, new seeds) → `agent_topbank2_seed5.out` | reproducibility of the agent's own runs | heavy: 8/8 by case 2 as reported; topbank2: 16/16, branches rec:U+ 8, rec:H 11, closure-H 4, as in the report |

Finite computations prove nothing about scaling; they test the bookkeeping of the proof on the
shapes the proof is about (over-capacity rounds, W ≠ U, complete absorptions, top phase). Taken
together, the referee's runs exercised every branch of ALG-T: case 1, case 2, 3.0, 3.1 (W = U and
W ≠ U, one and two over-capacity rounds), 3.2, 3.3 with closure on U⁺, with the U⁺-recursion,
with a top-phase leaf, and with a top-phase stall.

Two notes on the referee's own code, for honesty: (i) the first run of the `agent` group raised
"(F2) fails" on two `topbank` shapes; the traceback showed a tag collision in *my* top-phase scan
(flag coordinates tagged 0..dim−1 mixed with column tags), which corrupted the relation δ; after
the fix all 54 banks pass and the forward pass, which uses untagged bases, was never affected.
(ii) In `ref_ineq.out` the printed `I2` slack is 0 only because that field was initialised to 0;
the violation count for (I2) is 0, which is the statement checked.

## 3. Imprecisions (no effect on any claim; suggested fixes)

1. Theorem A's leaf description, "a set of columns spanning a flat V′ … a flag on them realizing
   V′": in a closure leaf (case 1 or closure on U⁺) the round columns span U⁺ ⊋ V′ = U. Say
   "a flag realizing a flat V′ of dimension r′, with a nonempty Src ⊆ V′ outside the rounds";
   r′ = Σ_l(n_l − 1) is what enters ρ ≤ Er′/2.
2. §5 T_m(c) "In particular T_m(b) needs J ≥ 4" means "is reachable only for J ≥ 4" (at J = 3 the
   top phase has m = 1 and |X′| ≤ 2 would already have triggered the U⁺-recursion).
3. §0.3 "p ≥ max(2.33·10⁶, 1792r)": the exact Lemma-W threshold is 2,322,604; the rounding is
   upward and safe. Likewise 6.89·10⁸ for 688,117,852.
4. §0.2 "The prime condition is p ≥ 72κ²a⁶J² and p ≥ 6Jκa⁴" holds only when J = ⌈log_κ a⌉
   (a > κ^{max(κ,3)−1}); for smaller a the original max(8κ^{2E}E², 2Eaκ^E) with constant J applies.
   The §6 parenthetical says this; §0.2 should too.
5. §4's remark "The Q1 fallbacks Y and U are the special cases W = span(B∩U) and Z = ∅" is an
   analogy: span(B∩U) is not of the form U + span(Z). Harmless.
6. §2's bound for (I2), "t(3r+6)/4", and Lemma C's statement are correct; no change.

## 4. What a human should still read

Lemma 2 (§1(a) above, 15 lines) and Lemma M (§1(c), 10 lines). Both are short and I found them
right; the rest is counting and matroid routine. The report's own gates (not uniform in p; no
novelty claim; the paper's stated arity unchanged until the owner decides) are correct and should
stay in place.
