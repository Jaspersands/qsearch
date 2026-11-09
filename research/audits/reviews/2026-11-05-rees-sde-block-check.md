# Adversarial check and integration: steered block-refined SDE solver (rem:sde-block-steered)

**Status: COMPLETE. No Error; 1 Gap and 7 Imprecisions, all fixed in the inserted text. Remark
inserted.** 5 November 2026, AI-only pass (one Claude Code session, no helper agents). Not
human-reviewed. **AI-checked, pending human review.** Subject:
`2026-11-05-rees-sde-two-relation.md` ("the report") and its folder. Scripts and outputs of this
check are in `2026-11-05-rees-sde-block-check/`; interpreter `/opt/anaconda3/bin/python`. No git
actions, no network, `rees_hsp_reduction.json` untouched, `make_numbers.py` not run, no table or
headline number changed.

## 0. Verdicts

| claim | verdict |
|---|---|
| Theorem B (coset-generic flexibility of one circuit split into E blocks) | **holds** (re-derived; exhaustive re-check, §2) |
| Theorem C (steered recursion), arity M_E(a), success bound | **holds** (re-derived, §1; independent solver, §3) |
| M_3(a) = ⌊(a+2)²/4⌋ + [a odd]; M_E = a²/(2(E−1)) + O(a); O(a²/log a) at E = ⌈log_κ a⌉ | **holds** |
| Corollary C (i.i.d. uniform columns) and the prime bounds κ = 2: p ≥ 64a², κ = 3: p ≥ max(2750, 1000a²) | **holds**, with Imprecisions I1, I4 |
| E_cg(3,2) = ∅, E_cg(3,3) = the 22 primes ≤ 241, G_3 ratios | **holds** (independent code, §2) |
| (H1), (ND′) polynomial-time checkable | **holds**, Imprecision I2 (they are properties of the forward pass) |
| Worst case unchanged, counterexamples | **holds for κ = 2; Gap G1 for κ = 3** (solvability not shown at the report's a = 6), closed at a ∈ {8, 10} |
| CHMT uniform claim fails at a ≤ 2 | **holds** (Imprecision I6) |
| Applies to Rees labels (task (e)) | **yes, with a = a_d via the observed span**; no effect on any count of the paper or on E_W (§4) |

## 1. Re-derivation (task (a), (b))

**Theorem B.** (i) A relation Σμ_bW_b ∈ U gives the column relation (μ_{b(i)}δ_i), a multiple of δ
because S is a circuit mod U, so μ is constant; hence dim Ω = E − 1 and Σ_bW_b = Λδ = e ∈ U.
(ii) Λx ≡ Σβ_bW_b mod U forces x − δ∘β_{b(·)} ∈ Fδ, i.e. x_i = δ_i(β_{b(i)} + s); since
δ_i ∈ Q_{c_b}, x_i ∈ P ∪ {0} iff β_b + s ∈ Q°_{−c_b}; value Σβ_bW_b + s·e. (iii) Same-class blocks
with equal offsets merge; a coincidence-free β leaves E′ ≤ E distinct offsets with ≥ 2 classes, so
Good(β) ≠ ∅ off E_cg. Correct. β is defined modulo constants (ΣW_b ≡ 0), and β_b − β_{b′} is well
defined on Ω, so the C(E,2) hyperplanes are well defined.

**Lemma W.** The character expansion has κ^e − 1 nontrivial terms; a term of support w is bounded
by (w−1)√p (LN Thm 5.41, distinct β, exponents 0 < t_b < κ) plus e − w for the removed s ∈ {−β_b};
(w−1)√p + e − w ≤ (e−1)√p. Hence |Good| ≥ κ^{−e}((p−e) − (κ^e−1)(e−1)√p). Correct; the bound
decreases in e, so e = E is the worst case. My bisection gives p_W(3,2) = 202, p_W(3,3) = 2710,
p_W(4,2) = 2033 (as the report), and p_W(κ,κ) for κ = 4..9: 585233, 1.56·10⁸, 5.44·10¹⁰,
2.44·10¹³, 1.38·10¹⁶, 9.61·10¹⁸.

**Theorem C, column count.** Under (H1) round l has E_l = min(max(E,|C_l|), q_l+1) ≥ min(E, q_l+1)
blocks (|C_l| ≤ κ ≤ E, which is why E ≥ κ is needed: it keeps E_l ≤ E), so it gains ≥ min(E−1, q_l).
f_E(q) = q + 1 + f_E(q − min(E−1,q)), f_E(0) = 1, unrolls to
M_E(a) = 1 + m(a+1) − (E−1)m(m−1)/2 + [r>0](r+1), a = m(E−1) + r. E = 3, a = 2m: (m+1)² =
(a+2)²/4; a = 2m+1: m² + 3m + 3 = ⌊(a+2)²/4⌋ + 1. E = 2 gives (a+1)(a+2)/2. **The minimum:** since
f_E is nondecreasing, taking the largest gain at every round is optimal, so M_E(a) is the least column
count of any run with at most E blocks per round; M_E is nondecreasing in a and nonincreasing in E
(checked for a ≤ 59, E ≤ 7 in `mybrt.arity` / `closed_arity`). At E = 3 this is ⌊(a+2)²/4⌋ + [a odd],
about half the triangular count.

**Theorem C, values and failure.** τ_{l−1} = π_{l−1}(τ_l) − s_l e_l, with π dropping the round-l
coordinates; the values telescope to −τ_0 = 0 and the top/stop weight is nonzero. The level-j offsets
are linear in (y or ζ, s_L, …, s_{j+1}), with the coefficient of s_l equal to minus the level-j
coordinates of e_l. A pass fails only at a cross-class coincidence. If the first one (scanning down)
is at (j,b,b′) and m > j is the smallest index with a nonzero coefficient, then level m had no
coincidence, so s_m is uniform on a set of size ≥ G_E(p), F is affine in s_m with nonzero slope, and
s_{m−1..j+1} do not enter: probability ≤ 1/G_E(p). If only y (or ζ) enters, F = c·y ≠ 0 by (ND′).
Union bound: ≤ Σ_j N_j/G_E(p) ≤ L·C(E,2)/G_E(p), L = ⌈a/(E−1)⌉. Correct.

**Corollary C (task (b): which events fail, how likely).** Bank side, per round l: first q_l fresh
columns not a basis mod U_{l−1}, ≤ 1/(p−1); last column with some but not all quotient coordinates 0,
≤ q_l/p (all zero gives a stop round). Per cross pair: the s_{j+1}-coefficient is a nonzero
functional of e_{j+1} = Σδ_iu_i, which is uniform on U_j because the U_j-parts u_i are independent of
the quotient parts that fix δ; so it is 0 with probability 1/p (also for e_stop and λ_top). Total
≤ (Σ_l(q_l+1) + L·C(E,2))/(p−1) ≤ (M_E(a) + L·C(E,2))/(p−1). Pass side: ≤ L·C(E,2)/G_E(p) per back
substitution, independent across passes given the bank. The draw cap is a Las Vegas cap.

**Prime bounds.** κ = 2, E = 3: 2 cross pairs per round, L ≤ (a+1)/2. G_3(p) ≥ p/10 for p ≥ 256
(exact to 5000, min ratio 0.1103 at p = 263, independently recomputed; Lemma W
(p − 3 − 14√p)/8 ≥ p/10 for p ≥ 4930). With p ≥ 64a² (≥ 256 for a ≥ 2): pass ≤ 10(a+1)/(64a²)
≤ 0.118 ≤ 1/8; bank ≤ ((a+2)²/4 + a + 2)/(64a² − 1) ≤ 0.032 ≤ 1/16. κ = 3, E = 3: ≤ 3 cross pairs.
p ≥ 2750 > 241 avoids E_cg(3,3); G_3 ≥ p/40 on 2750..11000 (exact, min 0.02530 at p = 2767,
independently recomputed) and ≥ p/54 for p ≥ 10829 by Lemma W, so G_3 ≥ p/54 for p ≥ 2750. With
p ≥ 1000a²: pass ≤ 81(a+1)/(1000a²) ≤ 0.061 for a ≥ 2 (the report's 0.17 is the a = 1 value);
bank ≤ 0.002. O(a²/log a): p_W(E,κ) ≈ κ^{2E}E² ≈ κ²a²log²a and G_E ≈ p/κ^E ≫ L·C(E,2) ≈ aE/2,
so p ≥ Cκ²a²log²_κ a suffices; time κ^E·poly = poly. Correct.

## 2. Findings (graded)

- **G1 (Gap) — κ = 3 counterexamples not shown solvable.** The report's planted κ = 3 instances are at
  a = 6, M = M_3(6) = 16 < 3a + 1 = 19, so Chevalley–Warning does not apply, and solvability was not
  checked; the draft remark said "solvable column sets with M_E(a) ≥ 2a+1 columns … (for κ = 3, E = 3
  …)". 2a + 1 is the κ = 2 CW count. **Fix:** κ = 3 needs M_3(a) ≥ 3a + 1, i.e. a ≥ 8. With the
  report's generator and my solver: κ = 3, E = 3, a = 8 (M = 25 = 3a+1), p ∈ {1009, 2767}, and a = 10
  (M = 36 ≥ 31), p = 1009: 24/24 instances have three coset classes in round 1 (blocks forced), (ND′)
  fails in 24/24, and my solver fails in 24/24 with 40 back substitutions, with fixed and with random
  splits (`run_planted.out`). So the claim holds once stated with M_E(a) ≥ κa + 1. Text fixed.
- **I1 (Imprecision) — the stop round.** The remark required "every round's columns form a circuit";
  a final round whose dependency lies in one coset need not be a circuit (e.g. λ ∈ U), and the top
  round is a single column. Corollary C's "the run stops early with success" is loose: a stop round
  still needs steering, which (ND′) covers through e_stop. Text now exempts the last single-coset round.
- **I2 (Imprecision) — what is checkable.** (H1) and (ND′) depend on the forward pass (column order and
  block choices, random at κ = 2), not on the columns alone. Both are checkable in polynomial time once
  the pass is fixed: (H1) is the kernel dimension and support of each δ; (ND′) needs the level-j
  coordinates of the e_l (l > j) and of λ_top/e_stop, O(L) solves and O(L·E²) comparisons. **What the
  solver does on failure:** `brt.py` continues with the dependency it found (smaller gain, possibly
  "budget"), or restarts the back substitution and finally reports failure; every returned vector is
  asserted to be a witness, so it never outputs a wrong answer. Text says this.
- **I3 (Imprecision) — E_cg definition in the draft remark** omitted "classes not all equal" and used an
  undefined min_β|Good(β)|. Defined E_cg and G_E(p) as in report §4.
- **I4 (Imprecision) — failure probability missing from the i.i.d. conclusion.** The bank-side failure
  (≤ 1/16) is a property of the columns and is not reduced by repeating the back substitution; the
  pass-side failure is ≤ 1/8 per pass. Text: fails with probability ≤ 1/16 over the columns and
  otherwise ≤ 8^{−k} after k passes (valid for κ = 2 and κ = 3 under the stated bounds, a ≥ 2).
- **I5 (Imprecision) — "the label law".** Report §0 item 5 calls i.i.d. uniform columns in F_p^a "the
  label law"; the Rees law is i.i.d. uniform on an unknown subspace. It reduces to Corollary C (§4).
- **I6 (Imprecision) — Proposition H(a).** "padded by repeating a column when a = 1" is unnecessary:
  a(a+1)/2 + 1 = 2a for a ∈ {1, 2}, so the instance (e_j, −g·e_j) already has the right size. The
  statement is right (x_1 = g x_2 forces x = 0) and trivially so at m = 1 (a univariate quadratic need
  not have a root): CHMT's class must be a restricted class. Not in the paper text.
- **I7 (Imprecision) — `brt.py` cap.** For p > 20000 `good_set` stops after 4000 random draws and the
  status says "good-empty"; it is a cap, not a proof of emptiness. The report's "empty Good" counts are
  at p = 1009 (exhaustive), so no reported number is affected.

Not re-derived in full: Lemma 2.1 and Proposition A (§2, read, consistent; not used in the paper) and
E_cg(4,2) (not used in the paper).

## 3. Tests (task (d))

Report suite rerun: `test_two_relation.py`, **8 passed** (nice, 1 core).

Independent code (`2026-11-05-rees-sde-block-check/`, no import from the report folder except the
adversarial generator in `run_planted.py`): `mybrt.py` keeps U as an echelon basis with coordinate
maps, reduces fresh columns once, finds dependencies by incremental elimination, splits blocks by its
own rule and draws s by rejection.

| check | script → output | result |
|---|---|---|
| E_cg(3,2), all p ≤ 260 (p_W = 202) | `ecg.py` → `ecg_k2_E3.out` | ∅; G(257) = 29 |
| G_3/p, κ = 2, 256 ≤ p ≤ 5000 | → `ecg_k2_E3_hi.out` | min 0.1103 (p = 263); 0 exceptional |
| E_cg(3,3), p ≤ 2750 (p_W = 2710) | → `ecg_k3_E3.out` | exactly the report's 22 primes, max 241; min G/p 0.0065 (p = 307, G = 2) |
| G_3/p, κ = 3, 2750 ≤ p ≤ 11000 | → `ecg_k3_E3_hi.out` | min 0.02530 (p = 2767, G = 70) ≥ 1/40 |
| Weil bound vs exact G | asserted in `ecg.py` for every prime | 0 violations |
| Theorem B (i)–(iii) exhaustively | `thmB.py` → `thmB.out` | 36 circuits, 10 (p, κ, q, E): dim Ω = E−1 in all; (ii) 0 mismatches; (iii) 0 misses at p ∉ E_cg (13, 59 for (3,2); 271 for (3,3); 61 for (4,2)), misses at p ∈ E_cg (31, 37 for (3,3); 29, 59 for (4,2)); at 241 ∈ E_cg(3,3) the 2 sampled circuits had no failing pattern |
| uniform columns at the stated bounds | `run_random.py uniform` → `run_uniform.out` | 480 runs, 24 settings: κ = 2 at p = next prime ≥ 64a², κ = 3 at p ≥ max(2750, 1000a²), a ∈ {2,3,4,5,6,8,10,12}; also κ = 2 E ∈ {4,5} (a up to 30), κ = 4 E = 4, κ = 5 E = 5, κ = 3 E = 4, p up to 10⁹+9. **480/480 ok**, every witness verified, columns used = M_E(a) exactly (or fewer after a stop round), 0 (H1)/(ND′) failures, 1 back substitution each |
| Rees-label mode | `run_random.py label` → `run_label.out` | i.i.d. on a random a-dim subspace of F_p^g, public budget M_3(g): 100/100 ok, used ≤ M_3(a) |
| failure rates below the bounds | `run_stats.py` → `run_stats.out` | 6 small-p settings × 300 banks: bad-bank rate ≤ bound in all (e.g. κ = 2, p = 257, a = 6: 0.060 vs 0.098; κ = 3, p = 2713, a = 6: 0.003 vs 0.009); pass failure 0.005 vs 0.31 and 0 vs 0.12; 0 wrong witnesses |
| planted (ND′) failures | `run_planted.py` → `run_planted.out` | κ = 3, a ∈ {8, 10}: 24/24 fail (G1). κ = 2, a = 6: the report's planting targets its own split, and my split solves 8/8, as the report says ("random splits rescue") |
| paper numbers test | `tests/tools/test_rees_paper_numbers.py` | 2 passed (before and after the edit) |

## 4. Task (e): Rees labels

**Does Theorem C apply?** Yes. By `lem:s3-law` the labels at a stage-d node are i.i.d. uniform on
K_d^⊥ (dim a_d ≤ g_d), i.e. λ_i = E x_i with x_i i.i.d. uniform in F_p^{a_d} and ker Λ = ker X. The
procedure is equivariant under invertible linear maps (dependencies, classes, blocks, coordinates in
the round basis and Good sets are unchanged), even data-dependent ones. Run it on coordinates in the
span V′ of the bank. On the event V′ = K_d^⊥ its run equals the intrinsic run on (x_i) with a = a_d,
so P(fail) ≤ P(rank X < a_d) + (Corollary C bound at a_d), and P(rank X < a_d) ≤
(p^{a_d}−1)/((p−1)p^M). The bounds are increasing in a, so they hold with g_d in place of a_d, and
the public arity M_E(g_d) suffices (only M_E(a_d) columns are consumed). Neither a_d nor a basis is
needed. Checked: `run_label.out`.

**What it changes.**
- *Schedule 3 arity: no.* Theorem C's arity is quadratic. Schedule 3 is linear,
  g_d(1 + O(log κ/log(p/κ))), in part (iii), and constant, 4u, in parts (ii)/(iv), with
  exponential classical time. Theorem C adds a different point: polynomial classical time with the
  label law, at quadratic arity.
- *A "random-label two-level" option in the combined rule: possible, not adopted.* It is admissible
  at a grade with 2 ≤ κ_d < p − 1 only under three conditions. (G1) p ∉ E_cg(E, κ_d), with
  E = max(3, κ_d). (G2) Per-pass success: L·C(E,2) ≤ G_E(p)/2. (G3) Bank abort
  (M_E(g_d) + L·C(E,2))/(p−1) ≤ τ_d = ε/(9(c−1)S n_d), the error split of thm:free-coordinate(iii),
  because this failure cannot be repeated away. (G3) needs p large compared with g_d² and with the
  node count n_d.
- *Computed preview* (`preview_e.py` → `preview_e.out`). This is the class-nine profile, ε = 1/3,
  S = 20, with log₂ of the combined-column Q of tab:fcs-budget. Variant A takes E = max(3, κ_d).
  Variant B takes the best E ≤ 8 with κ^E ≤ 2²⁰.

| p | table (combined) | triangular preview (rem:triangular-scope) | Theorem C option A | option B |
|---|---|---|---|---|
| 11 | 202.1 | 202.1 | 202.1 (no grade admissible) | 202.1 |
| 1031 | 167.3 | 164.0 | 167.3 (G3 fails: bank 0.11 per node) | 167.3 |
| 5281 | 852.3 | 851.4 | 852.3 | 852.3 |
| 2³¹−1 | 944.9 | 940.5 | 940.3 (grades 2, 3) | 934.2 |
| 2⁶¹−1 | 555.4 | 542.0 | 533.4 (grades 2–8; grade 9 needs p ≥ p_W(9,9) ≈ 9.6·10¹⁸) | 528.1 |
| 2¹²⁷−1 | 61.5 | 48.3 | 41.4 (all κ ≥ 2 grades) | 39.2 |

  All of these stay far above the label-law columns of the same table: (iii) is at 34.0–42.3 and the
  uniform-kernel column at 49.9–52.9. The bank-abort sums are ≤ 8.3·10⁻⁴ wherever the option is used (≤ ε/9 by construction).
- *E_W: unchanged* (`ew_preview.py` → `ew_preview.out`: [5, 11, 23, 38, 56, 77, 107, 143], asserted
  equal to the paper). E_W(c) takes, at a fixed p, the exponent of a per-grade bound valid for all
  g_d. Theorem C's prime conditions grow with g_d, so at a fixed p the option is unavailable for
  large g_d, and its arity is quadratic in any case. For scale only: an invalid g-independent reading
  (guard p ∉ E_cg alone) would give [3, 9, 21, 36, 54, 71, 103, 139]. It is the g-dependence that
  keeps E_W fixed. tab:main-regimes is unchanged.

No table, macro or headline number was changed. The paper text says the counts do not use the option.

## 5. Inserted text

The remark below was inserted into `docs/papers/rees-hsp/main.tex`, directly after `\end{remark}`
of `rem:sde-subquadratic`. The edit was an exact-string insertion with an asserted single
occurrence, and a backup is in `scratchpad/bak-block/main.tex.bak`. It is a copy of
`2026-11-05-rees-sde-block-check/remark.tex`. No bib entry was added, since `LidlNiederreiter1997`
is already in the bibliography. The other concurrent edits to main.tex and appendix-schedule2.tex
were not touched.

```latex
\begin{remark}[Steered block-refined triangular solver; conditional; AI-checked, pending human review]
\label{rem:sde-block-steered}
This remark comes from an AI-only pass (\file{research/audits/reviews/2026-11-05-rees-sde-two-relation.md}), checked and corrected by a second, adversarial AI pass (\file{research/audits/reviews/2026-11-05-rees-sde-block-check.md}); no human has checked it, nothing else in the paper uses it, and it gives no worst-case improvement. Keep the notation of Proposition~\ref{prop:triangular-sde}, with $Q_\nu=g^{\nu}P$ and $Q_\nu^\circ=Q_\nu\cup\{0\}$. Let $S$ be a circuit modulo $U$ whose dependency $\delta$ has entries in at least two cosets, and split $S$ into blocks $G_1,\dots,G_E$, each contained in one set $\{i:\mathrm{cos}(\delta_i)=c_b\}$; put $W_b=\sum_{i\in G_b}\delta_i\lambda_i$. Then the classes of the $W_b$ modulo $U$ span a space $\Omega$ of dimension $E-1$, and their only relation is $\sum_bW_b=e:=\sum_{i\in S}\delta_i\lambda_i\in U$. For $\beta\in\Fp^E$ the weights $x_i=\delta_i(\beta_b+s)$, $i\in G_b$, lie in $P\cup\{0\}$ exactly when $s\in\mathrm{Good}(\beta)=\{s:\beta_b+s\in Q_{-c_b}^\circ\text{ for all }b\}$, and their value is $\sum_b\beta_bW_b+s\,e$; every $x\in(P\cup\{0\})^S$ whose value lies in $\Omega$ modulo $U$ has this form. By the Weil bound~\cite[Theorem~5.41]{LidlNiederreiter1997}, $|\mathrm{Good}(\beta)|\ge\kappa^{-E}\bigl(p-E-(\kappa^E-1)(E-1)\sqrt p\bigr)$ whenever the $\beta_b$ are pairwise distinct. Let $E_{\mathrm{cg}}(E,\kappa)$ be the set of primes $p\equiv1\pmod\kappa$ at which $\mathrm{Good}(\beta)=\emptyset$ for some $E'\le E$, some classes $c_1,\dots,c_{E'}$ not all equal and some pairwise distinct $\beta_1,\dots,\beta_{E'}$, and let $G_E(p)$ be the least $|\mathrm{Good}(\beta)|$ over such data. Exhaustive computations up to the Weil bound, repeated by the second pass with independent code (finite computations, AI-checked, pending human review), give $E_{\mathrm{cg}}(3,2)=\emptyset$ and $E_{\mathrm{cg}}(3,3)=\{7,13,19,31,37,43,61,67,73,79,97,103,109,127,139,151,157,163,181,193,211,241\}$. So for $p\notin E_{\mathrm{cg}}(E,\kappa)$ a circuit realises every point of $\Omega$ off the at most $\binom{E}{2}$ hyperplanes $\{\beta_b=\beta_{b'}\}$ with $c_b\ne c_{b'}$, by drawing $s$ uniformly until $E$ coset tests pass, about $p/G_E(p)$ draws; by part~(a) of Remark~\ref{rem:sde-subquadratic} it never realises a whole plane. Running the triangular recursion with these blocks, and drawing the free scalar $s$ of each round uniformly from $\mathrm{Good}(\beta)$ in the back substitution, moves the next residual along $e$ and steers it off the bad hyperplanes. Suppose that $E\ge\kappa$, that $p\notin E_{\mathrm{cg}}(E,\kappa)$, that the columns of every round, except a last round whose dependency lies in one coset, form a circuit modulo the current space, and that no residual offset difference $\beta_b-\beta_{b'}$ with $c_b\ne c_{b'}$ is identically zero as a linear function of the drawn scalars. Both conditions concern the forward pass, including its choice of blocks, and can be checked in polynomial time once that pass is fixed; when one fails the procedure may abort, and it never returns a wrong solution, since its output is checked. Under these conditions each back substitution returns a nonzero solution with probability at least $1-L\binom{E}{2}/G_E(p)$, where $L\le\lceil a/(E-1)\rceil$ is the number of rounds, and the recursion uses at most
\[
  M_E(a)=1+m(a+1)-\tfrac{(E-1)m(m-1)}{2}+[r>0](r+1),\qquad a=m(E-1)+r,\ 0\le r<E-1,
\]
columns, which is $(a+1)(a+2)/2$ for $E=2$, $\lfloor(a+2)^2/4\rfloor+[a\text{ odd}]$ for $E=3$, and $a^2/(2(E-1))+O(a)$ in general; the expected time is polynomial in $a$ and $\log p$ times $\kappa^E$. For i.i.d.\ uniform columns both conditions hold with probability at least $1-\bigl(M_E(a)+L\binom{E}{2}\bigr)/(p-1)$; this is a property of the columns, and repeating the back substitution does not reduce it. Hence, for i.i.d.\ uniform columns in $\Fp^a$ with $a\ge2$ and $E=3$, a randomised polynomial-time procedure with $\lfloor(a+2)^2/4\rfloor+[a\text{ odd}]$ columns fails with probability at most $1/16$ over the columns, and otherwise with probability at most $8^{-k}$ after $k$ back substitutions, for $\kappa=2$ at every prime $p\ge64a^2$ and for $\kappa=3$ at every prime $p\ge\max(2750,1000a^2)$ (the second range uses an exhaustive computation of $G_3(p)$ for $p\le11000$); with $E=\lceil\log_\kappa a\rceil$ and $p\ge\poly(a)$ it uses $O(a^2/\log a)$ columns. The steering condition is genuinely needed: there are column sets with $M_E(a)\ge\kappa a+1$ columns, hence solvable by the Chevalley--Warning theorem, on which it fails and every back substitution fails (planted instances, exact computations, AI-checked, pending human review: for $\kappa=3$, $E=3$ and $a\in\{8,10\}$, where the blocks are forced to be the coset classes, and for $\kappa=2$, $E=3$ and $a=6$ with a fixed block rule). So for arbitrary columns the best arity proved in this paper remains $(a+1)(a+2)/2$. The labels of Lemma~\ref{lem:s3-law} are i.i.d.\ uniform on the unknown subspace $K_d^\perp$, and the procedure commutes with invertible linear maps of the columns, so run on coordinates in the span of its bank, which is $K_d^\perp$ except with probability at most $(p^{a_d}-1)/((p-1)p^{M})$, it behaves as on i.i.d.\ uniform columns in $\Fp^{a_d}$; with the public arity $M_E(g_d)$ it would therefore give a polynomial-time option that uses the label law, but only at primes large compared with $g_d^2$ and with the number of nodes of the recursion. The query counts of Theorem~\ref{thm:main}, Remark~\ref{rem:combined-schedule}, Theorem~\ref{thm:free-coordinate} and the tables do not use it, and it would not change $E_W(c)$, because its prime condition grows with $g_d$.
\end{remark}
```

Changes from the report's §10 draft are G1 (κa + 1 and the κ = 3 values of a), I1, I2, I3 and I4,
the source line naming this check, and the closing label-law sentences required by task (e).

## 6. Build

The build ran in `scratchpad/build-block/` (copies of `*.tex` and `references.bib`) with
`latexmk -g -pdf`. It exited 0 and the remark appears as Remark 4.13 on p. 31. The log has
0 Overfull boxes, no undefined references or citations, and no "Float too large".
`tests/tools/test_rees_paper_numbers.py` gives 2 passed. Integration log: row **I206**.

## 7. Claim gates (must stay false)

- "Theorem C gives a worst-case o(a²) or (a+2)²/4 polynomial solver." False: (ND′) fails on solvable
  planted inputs (G1 instances).
- "The paper's counts, tables or E_W use Theorem C." False: the preview is not adopted.
- "Theorem C improves Schedule 3's arity." False: Schedule 3 is linear or constant, and Theorem C is
  quadratic.
- "The result is uniform in p." False: it needs G_E(p) ≫ L·C(E,2) and p ≫ M_E(a).

**Next hard question** (unchanged from the report): can (ND′) be enforced adaptively, using slack
columns, re-randomized splits or a two-defect round, so that the a²/4 count holds in the worst case
for p ≫ a? A secondary question for the Rees option: can redrawing a failing round from slack columns
replace the union bound (G3), and so remove the dependence on n_d?
