# Referee report on `2026-11-08-rees-sde-uniform-p.md` (lookahead steering, control fan-in, bounded-p obstructions)

AI-only adversarial referee, 8 November 2026, one Claude Code session; not human-reviewed. Scripts and
outputs in `2026-11-08-rees-sde-uniform-p-referee/` (interpreter `/opt/anaconda3/bin/python`). Only
this file and that folder were written. No git, no network, `make_numbers.py` not run. Nothing in the
report's folder was modified or executed; where ALG-T is needed, the unmodified `subquad.py` of the
Theorem A folder is imported.

Read: the report; Theorem A report §0, §2, §6 and `subquad.py` (`forward_fast`, `leaf`, `solve_T`),
`q1core.init_state`, `mk_round`, `steer_bad`, `sss.split_blocks`, `sss.backward`; Q1 report §1–2
(Lemma 2); two-relation report §4 (Lemma W, E_cg). Every derivation below is my own; every number
is from my own code unless marked "report".

## 0. Verdicts

| item | verdict |
|---|---|
| 1 Theorem L | **CONFIRMED.** Control = last-drawn nonzero coefficient; one exclusion per pair; protection is final. 65 ALG-T leaves (own lookahead, own φ/ctrl code): invariants hold at every level, 0 fallbacks; 25 leaves at p = 13 (hypothesis false) show 22 leaves with fallbacks, so the test discriminates. The allowed set can be chosen deterministically. |
| 2 Corollary L1 | **CONFIRMED WITH CORRECTION** (cost accounting only). Zero-error at p ≥ max(C_old, κ^E(Er+2)) is right. The per-level rejection cost of Theorem A (≤ 2κ^E draws) does not carry over: it is ≤ 2κ^E·p/(p − κ^E Er), i.e. ≤ 4κ^E only from p ≥ 2Erκ^E (Theorem A's own linear term) and up to p = κ^E(Er+2) at the new threshold. Still polynomial. |
| 3 EC banks | **Lemma E2 CONFIRMED** (27 instances through the unmodified ALG-T). **Lemma E1 CONFIRMED.** **Lemma E3 CONFIRMED WITH CORRECTION:** "completing the leaf is *exactly* the nowhere-zero problem Ct ∈ (F_p^*)^r" is false; nowhere-zero is sufficient, not necessary. Exact at p = 5, r = 8: success 0.48 vs nowhere-zero 0.15–0.17. The table's "exact" column is true pass success and is instance dependent (r = 4, p = 5: 0.625, 0.875, 1.000 on three instances; report 0.875). The "local resampling cannot repair" conclusion is correctly scoped (s_l irrelevant; fixed scan order); under a random scan order my run gives N*_src ≤ 2, N*_lev ≤ 3. |
| 4 Thresholds | **CONFIRMED** exactly (integer arithmetic): primes 583,991; 84,822,113; 172,103,821; 282,423,985,969; the preceding prime ≡ 1 (mod κ) fails in each case; C_old values match. |
| 5 Lemma P, Lemma R, small p | **CONFIRMED.** Identity Σ_c\|Good\| = p + E(κ−1) on every distinct β in 47 (κ,E,p) cases; P(b) exact. Lemma R brute-forced (every non-constant class vector, n = 3, 4; κ = 2, 3): holds at every p, with a coincident β; quantifiers as stated. Values reproduced and extended: κ = 2 two-class G*_3 = 1 (p ≤ 13), 2 (17–23), 3 (29), …, 6 (59, 61); κ = 3 G*_3 = 0 at exactly {7,…,181, 193, 211, 241} ∩ [7, 283] and ≥ 2 at 199, 223, 229, 271, 277, 283 (= E_cg(3,3) of the two-relation report). |
| 6 Tradeoff | **CONFIRMED WITH CORRECTION** (asymptotic formula). Table (c) reproduced exactly. The formula "p = a^γ ⇒ J ≈ ((γ−1)/3) log_κ a, F ≈ 3a²/(2(γ−1) log_κ a)" holds only for 1 < γ ≤ 2; for γ ≥ 2 the a-free constant C_old ~ 4κ^{2E}(E−1)² binds and J ≈ (γ/6) log_κ a, F ≈ 3a²/log_κ p; for γ ≥ 6 the cap gives F ≈ a²/(2 log_κ a). The report's own table shows it (κ = 2, a = 10⁴, p = 10¹²: formula J ≈ 9, actual J = 5). Precise statement in §6. |

Nothing in the report is refuted. Two statements are overstated (E3 "exactly"; the γ-formula) and one
cost is mis-transferred (L1). The claim gates of the report's §7 are correctly kept false.

## 1. Theorem L

**Derivation (own).** F_π = φ_π(τ_j) = −Σ_σ t_σ φ_π(σ) − Σ_{l>j} s_l φ_π(e_l), from τ_j = Π_j(τ_L) −
Σ_{l>j} s_l Π_j(e_l) and φ_π ∘ Π_j = φ_π. Draw order t_1..t_k, s_L..s_1. Variables with nonzero
coefficient: sources with φ_π(σ) ≠ 0 and levels l > j with φ_π(e_l) ≠ 0. Among the levels the last
drawn is the least such l, which is ctrl(π) = m; if none, the last drawn is the last source with
nonzero coefficient. So ctrl(π) is the last-drawn variable with nonzero coefficient. After it is
drawn, s_{m−1}, …, s_{j+1} have coefficient 0 (minimality of m) and s_l for l ≤ j do not enter F_π,
so F_π is final. One value of the control variable zeroes F_π (f ≠ 0). At variable v the excluded
set has ≤ N_v elements, one per pair controlled by v, so no two pairs "compete beyond the count":
|Bad_v| ≤ N_v by construction, whatever the pairs. At level m the induction gives no cross-class
coincidence (every pair of round m is controlled by an earlier-drawn variable, each protected), so
after merging equal same-class offsets there are e ≤ n_m ≤ E pairwise distinct offsets and
|Good_m| ≥ G*_E(p) ≥ N*_lev + 1 > |Bad_m|. Sources: |P ∖ Bad_i| ≥ (p−1)/κ − N_{src,i} ≥ 1. I find no
gap. Since any element of the allowed set works, the back substitution is in fact deterministic
(take the least allowed value); randomness is only a convenience.

**Code (own, `lookahead_check.py`).** Independent implementation of φ, ctrl, fan-in and the pass,
run on the leaves ALG-T (unmodified `subquad.py`, hooked at `sss.backward`) produces on uniform and
EC banks. At every level it asserts (I1) no cross-class coincidence at that level, (I2) if
|Good_l| ≥ N_l + 1 the allowed set is nonempty, and after each control draw that F_π never changes
again; sources likewise. It records the leaf-dependent hypothesis H(leaf): min_l |Good_l| ≥ N*_lev + 1
and |P| ≥ N*_src + 1 (sharper than G*_E(p) ≥ N*_lev + 1).

| run | leaves | H(leaf) true | fallbacks | witnesses |
|---|---|---|---|---|
| κ=2, J=3, p=29, r ∈ {8,12,16,24}, uniform+EC | 32 | 14 | 0 | 6400/6400 passes + deterministic |
| κ=2, J=4, p=101, r ∈ {12,18,24} (4-block rounds) | 12 | 6 | 0 | 1200/1200 |
| κ=3, J=3, p=307 (G*_3 = 2), r ∈ {8,12} | 8 | 7 | 0 | 800/800 |
| κ=2, J=3, p=29, EC shuffled scan order | 13 | 2 | 0 | 2600/2600 |
| κ=2, J=3, p=13 (G*_3 = 1; hypothesis fails) | 25 | 0 | 22 leaves; 191 emptyGood failures | discriminates |

No assertion ever fired. Leaves with H false but no fallback are expected (the bound is a worst case).

## 2. Corollary L1

N*_lev, N*_src ≤ ρ ≤ (E/2)Σ_l(n_l − 1) = Er′/2 ≤ Er/2 (F1 gives Σ(n_l − 1) = dim U_L). At p ≥ C_old,
G*_E ≥ p/(2κ^E) ≥ Er/2 + 1 ⟺ p ≥ κ^E(Er + 2); and (p−1)/κ ≥ Er/2 + 1 follows from that. So zero
error at p ≥ max(C_old, κ^E(Er+2)) is correct, and the linear term is halved against 2Erκ^E.
C_old = least p with LW_E(p) ≥ p/(2κ^E) re-derived exactly (§4); monotonicity of the condition in p
holds because each e-term is an increasing function of √p beyond its root.

**Correction.** Theorem A's statement includes "each round costs ≤ 2κ^E expected draws". With the
allowed set Good ∖ Bad and rejection sampling, the expected draws are p/(|Good| − |Bad|) ≤
2κ^E p/(p − κ^E Er). At Theorem A's own p ≥ 2Erκ^E this is ≤ 4κ^E (zero error at no extra
cost); at the new threshold p = κ^E(Er+2) it is p itself (κ = 2, J = 3, r = 40: p = 36,096 vs
256; `tradeoff_check.out`). Exact enumeration of Good costs O(Ep). Either way the time is
polynomial in (κ^E, r, M, log p) in the admissible range, so the corollary stands; its cost line
should read "≤ 2κ^E p/(p − κ^E Er) expected draws per level". The report's own code enumerates Good
for p ≤ 3·10⁵, which hides this.

## 3. EC banks

**Lemma E2 (own check, `ec_check.py`).** `init_state` takes the greedy basis in index order, which is
B (rows of an invertible matrix). `forward_fast` scans `unused` in index order with T reset per
round; u_1..u_{J−1} are independent mod U (direct sum), w reduces with coefficients c mod U + span(T),
so δ = (−c, 1) and e = Σδ_iλ_i = 0 exactly; `split_blocks` with target min(J, |S|) = J gives
singletons; non-monochromatic δ prevents "direct". On 27 instances (p ∈ {5, 7}, L = 2..7) the
unmodified ALG-T returned L rounds, all e_l = 0, 3 singleton blocks, S_l = circuit l, B = first r
columns, and stopped before any padding column. Confirmed.

**Lemma E1.** τ_{l−1} = Π_{l−1}(τ_l) when e_l = 0: immediate. Confirmed.

**Lemma E3.** Class pattern (c,c,c′) with 2 cross pairs, functionals independent on Π_l^*, C ∈ GL_r:
confirmed. Two-class G*_3 ≥ 1 for all p ≥ 5: E_cg(3,2) = ∅ (two-relation report: exact to 257,
Weil beyond 202) and my exact values to 61. **But** "a pass succeeds whenever Ct is nowhere zero" is
only one direction. With a coincidence β_b = β_{b′} (c_b ≠ c_{b′}) Good forces s = −β_b and is then
nonempty iff the third offset difference lies in Q°_{−c_{b″}}, which happens for about half the
values at κ = 2. Exact enumeration over P^r (own flag construction, no ALG-T in the loop):

| p | r | exact success (3 instances) | Pr[Ct nowhere zero] |
|---|---|---|---|
| 5 | 4 | 1.000, 0.625, 0.875 | 0.50, 0.375, 0.75 |
| 5 | 8 | 0.484, 0.477, 0.484 | 0.172, 0.148, 0.148 |
| 5 | 14 | 0.300, 0.292, 0.290 | 0.046, 0.043, 0.045 |
| 7 | 8 | 0.583, 0.583, 0.591 | 0.289, 0.279, 0.289 |

So the completion problem is "find t ∈ P^r with every Good_l(β_l(t)) ≠ ∅", strictly weaker than the
nowhere-zero problem; the Alon–Jaeger–Tarsi identification concerns a sufficient condition. The
report's "exact" column (0.875 → 0.175, instance of unknown seed) is the true pass success, and the
report's own remark "about half of the coincidences are fatal" already contradicts "exactly". The
lookahead could exclude only the fatal values at the last source (≈ ρ/2 instead of ρ exclusions at
κ = 2); this moves the collapse point by a constant factor, not the e^{−Θ(r/p)} shape, which stays
sampled/unproved as the report says.

**Scope of "local resampling cannot repair".** Correct as scoped: resampling s_l is useless by E1;
the obstruction is to Lemma-2-type completion of the leaf ALG-T's *deterministic index-order scan*
returns. The report's §3.3 claim that a random scan order restores locality is reproduced: EC banks
with shuffled columns through the unmodified ALG-T give N*_lev ≤ 3, N*_src ≤ 2 on 13 leaves
(r = 16, 24, 32, p = 29), 0 fallbacks. Two further scoping remarks the report could add: (i) a Las
Vegas restart of the *forward* pass with a fresh random order is already a repair, so "the linear
term is real for ALG-T" is a property of the fixed scan rule, not of the leaf-completion problem
class; (ii) sources may also take the value 0 (x ∈ (P ∪ {0})^M, x ≠ 0 needs one nonzero source),
enlarging the last source's domain by one. Neither changes the asymptotics.

## 4. Thresholds (Corollary L2)

Definition used (report §2 and `thresholds.py`): C_loc(κ,J) = least prime p ≡ 1 (mod κ) with
LW_E(p) ≥ N_loc + 1 and (p−1)/κ ≥ N_loc + 1, LW_E(p) = min_{e≤E} κ^{−e}(p − e − (κ^e−1)(e−1)√p),
N_loc = max cross pairs among E blocks (balanced classes; brute-forced over all class vectors for
E ≤ 10: 12, 25, 16, 33). `thresholds_exact.py` tests "LW_E(p) ≥ N+1" as, for every e,
A_e := p − e − (N+1)κ^e ≥ 0 and A_e² ≥ (κ^e−1)²(e−1)² p (integers only), primality by sympy.

| κ, J | least integer | least prime ≡ 1 (mod κ) | report | preceding prime ≡ 1 fails? | C_old (integer) | report |
|---|---|---|---|---|---|---|
| 2, 3 | 583,982 | **583,991** | 583,991 | 583,981: yes | 2,322,604 | match |
| 2, 4 | 84,822,109 | **84,822,113** | 84,822,113 | 84,822,097: yes | 339,075,436 | match |
| 3, 3 | 172,103,820 | **172,103,821** | 172,103,821 | 172,103,809: yes | 688,117,852 | match |
| 3, 4 | 282,423,985,962 | **282,423,985,969** | 282,423,985,969 | 282,423,985,927: yes | 1,129,679,882,536 | match |

The minimum over e is attained at e = E in all four cases. (C0 for (3,4): my strict-inequality integer
is 282,419,970,644 vs the report's float 282,419,970,645; the prime 282,419,970,727 agrees.)

## 5. Lemma P, Lemma R, small-p values

**Lemma P(a).** Fix s. If s ∉ {−β_b}: one class vector. If s = −β_{b₀} (unique b₀ by distinctness):
κ. Sum (p − E) + Eκ = p + E(κ−1). Hence min_c |Good| ≤ (p + E(κ−1))/κ^E and G*_E(p) = 0 when
p < κ^E − E(κ−1) (E ≤ p needed for E distinct offsets; for p < E the e = p term gives κp < κ^p
anyway). Asserted on every distinct β in `good_exact.py` for κ = 2, E = 3 (16 primes to 61), E = 4
(53, 59, 61), κ = 3, E = 3 (28 primes to 283): all true. **P(b).** E|Good| = |Q°|·(|Q°|/p)^{E−1} with
|Q°| = (p+κ−1)/κ, Markov gives Pr[Good ≠ ∅] ≤ p((1+(κ−1)/p)/κ)^E: confirmed exactly.

**Lemma R.** Quantifiers as proved: for every prime p ≡ 1 (mod κ), every n ≥ 3 and every class vector
with ≥ 2 classes there is β (β_0 = 0, coincidences allowed) with Good(β) = ∅. It holds at every p,
not only small p; its β has a cross-class coincidence, so it says nothing about G*_E (distinct
offsets), as the report notes. Brute force over all β: κ = 2, n = 3 (p = 5, 7, 11, 13), n = 4
(5, 7, 11); κ = 3, n = 3 (7, 13, 19): no failure for any non-constant c. For monochromatic c with
repeats allowed, an empty Good exists at p = 5, 7 but not at p = 11, 13 (κ = 2, n = 3), matching the
report's G^mono remark. The inference "Θ(a) unsteered such rounds succeed with probability
e^{−Θ(a/p)}" needs roughly independent, roughly uniform offsets across rounds; it is labelled
[argued] and must stay so.

**Values.** κ = 2, E = 3: all-classes G*_3 = 0, 0, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 4, 5, 6, 6 and
two-class 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 6, 6 for p = 5 … 61 — the report's rows match; the
report says "exact for p ≤ 61" but its `good_small.out` stops at 53 for E = 3; p = 59, 61 are now
covered. κ = 2, E = 4: (all, two-class) = (0, 1), (0, 0), (0, 1) at 53, 59, 61: match. κ = 3, E = 3:
0 at every prime ≡ 1 (mod 3) up to 97 (match), and further 0 exactly at 103, 109, 127, 139, 151,
157, 163, 181, 193, 211, 241 and ≥ 2 at 199, 223, 229, 271, 277, 283: this is E_cg(3,3) of the
two-relation report, independently reproduced. Witnesses are in `good_k*_E*.out`.

## 6. Tradeoff: what is proved

**Reproduced.** `tradeoff_check.py` (own D_J recursion, D_3(a) = ⌊(a+2)²/4⌋ checked, own exact LW)
gives the report's table (c) entry for entry, rules (a) and (b), κ ∈ {2,3}, a ∈ {10³, 10⁴}.

**Precise statement (as proved, AI-only, inheriting Theorem A's chain: Lemma 2, Lemma W via Weil,
Lemma M, Lemma T_m, none human-checked).** Fix κ ≥ 2, a prime p ≡ 1 (mod κ) and a. Let J(a,p) be the
largest J with max(κ,3) ≤ J ≤ max(max(κ,3), ⌈log_κ a⌉), E = 3J−2, LW_E(p) ≥ p/(2κ^E) and
p ≥ κ^E(Ea+2). If such J exists, every bank in F_p^a with at least F(a) = D_J(a) + max(2, 2J−4)a
≤ a²/(2(J−1)) + O(Ja) columns is solved by ALG-T with lookahead back substitution, every pass
succeeding, in expected time poly(a, M, log p)·κ^{O(J)} (per-level draws ≤ 2κ^E p/(p − κ^E Ea)).
This is an *upper bound on a sufficient column count for one algorithm*. No lower bound is proved at
any p; at bounded p nothing below (a+1)(a+2)/2 is proved or refuted. "o(a²) iff p/a → ∞" is a
statement about this bound F(a,p): J(a,p) → ∞ iff log_κ(p/a) → ∞ (with a → ∞), because
admissibility needs both κ^{3J}·Ea ≲ p and C_old(κ,J) ≈ 4κ^{6J−4}(3J−3)² ≤ p.

**Correction to §4(a)'s asymptotics.** With p = a^γ (γ > 1 fixed) the two constraints give
J ≈ min((γ−1)/3, γ/6, 1)·log_κ a: the linear term binds for 1 < γ ≤ 2, the a-free constant C_old for
2 ≤ γ ≤ 6, the time cap J ≤ ⌈log_κ a⌉ for γ ≥ 6. Hence F ≈ 3a²/(2(γ−1) log_κ a) only for γ ≤ 2;
F ≈ 3a²/(γ log_κ a) = 3a²/log_κ p for 2 ≤ γ ≤ 6; F ≈ a²/(2 log_κ a) for γ ≥ 6. The report's table
confirms this: κ = 2, a = 10⁴, p = 10¹² (γ = 3) gives J = 5, not ≈ 9, because J = 6 fails
C_old(2,16) = 3.87·10¹². The sentence "in general F = O(a²/log(p/a)) once p ≥ a^{1+Ω(1)}" needs
p ≤ a^{O(1)} as well; the clean form is F = O(a²/min(log_κ a, log_κ(p/a))), since
J ≥ (1/6)min(log_κ(p/a), log_κ a) − O(1) in all three regimes. Rule (b) is stated correctly as
conditional on Q-loc, and §0's "the a-free Weil constant usually decides J for a ≤ 10⁴" is right
(the two columns differ only at (2, 10⁴, 10⁷)).

## 7. Not re-run; remaining weak points

Not re-run: the break-family claims (design_mix N*_lev = 29, twist 9), `run_k2_Cloc`/`run_k3_Cloc`/
`run_k2J4_Cloc_par`, the large-r sampled EC rates (p = 11, 29; r ≥ 40), `ec_shuffle_copies`, and the
Alon–Jaeger–Tarsi literature identification (which, per §3, concerns a sufficient condition only).
Weak points as the report states them stand: the e^{−Θ(r/p)} EC decay is sampled; the a²/(2 log_κ p)
heuristic rests on "spread targets"; Q-loc is open. Additional: the per-level cost in L1 (§2 above),
and Lemma E3's "exactly" should be weakened to "if" in the report and in §0 item 1.

**Suggested text corrections.** §0(1)/§3.1: "Completion is the nowhere-zero problem" → "Completion
succeeds whenever Ct is nowhere zero; the exact success condition is that every Good_l(β_l(t)) is
nonempty, which also admits about half of the coincidences at κ = 2". §2 Corollary L1: add the draw
cost 2κ^E p/(p − κ^E Er). §4(a): replace the single γ-formula by the three regimes above and
"O(a²/log(p/a))" by "O(a²/min(log a, log(p/a)))". §5 table caption: two-class G*_3 exact to 53 in
the report's own run (61 here).
