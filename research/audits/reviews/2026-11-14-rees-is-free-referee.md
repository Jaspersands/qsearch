# 2026-11-14 Referee report: Theorem main without the Ivanyos–Santha import for c ≤ 9

Hostile AI referee. Everything here is AI-checked, pending human review.

- **Under review:** `research/audits/reviews/2026-11-14-rees-is-free.md` and its folder (`fragment.tex`, `edits.py`, `compare_degs.out`).
- **Core:** `docs/papers/rees-hsp/core/main-core.tex`, md5 `71743611d8b66af3e0d485110953a9e1`. It was read only and not edited. No existing file was edited.
- **My scripts and outputs:** `research/audits/reviews/2026-11-14-rees-is-free-referee/`.

## Verdict

**PROVED WITH FIXES.**

The mathematics holds: Lemma lem:plus-free-const, Theorem thm:plus-free and Corollary cor:main-free. It is **PROVED given the cited theorems** (Weil, Rabin, Chevalley–Warning, through the existing lemmas of sec:halving and sec:plus) **and an exact computation for p < 2·10^6**. I recomputed that exact computation independently, and it agrees at all 496,058 pairs. So for c ≤ 9, Theorem main holds with the same Q_q and the same bounds (3)–(5), and E_+(9) = 20, without thm:is-import, lem:rounds or the zero sums.

The fixes concern the text:
- one sentence of related work that the change makes wrong (F3);
- one sentence of the status section that now contradicts edit E5c (F4);
- several consistency and wording points.

The optional rem:plus-free-ten is adequately supported, but it needs one missing preprocessing detail (F9).

The result rests on Section sec:plus and Theorem plus as written, which are themselves refereed by AI only.

## Recomputation (obligation 2)

`indep_isfree.py` was written by me from the text of sec:plus: Definitions plus-rc, plus-ell and plus-schedule, Corollary plus-chain, Lemmas plus-stage and plus-finish, and the T_j recursion. It shares no code with `isfree_check.py`, `plus_mine.py`, `run2.py` or `plus2.py`.

**Data reused**, documented in the script header, with every entry re-verified by my own checker of Def. plus-rc / plus-ell:
- `certs_stage1.json`, `tierB_witnesses.json` and `v2/certs_tl6_all.json` (headline-below-38);
- the five ℓ-level tables (k9-below-21);
- the FOUND entries of `ref20_copy/rc_cache.json`.

**Availability is under-approximated.** A step counts as available only in two cases:
- p ≥ T_exist, by Lemma plus-sm(i). I re-checked the table thresholds: Φ(T) < 1 ≤ Φ(T − 1) for all six.
- A verified certificate exists. For p ≤ 523 that is either stored or found by my own bitset DFS (budget 2·10^4 nodes, capped searches treated as unavailable).

Every candidate arity is monotone in the inner arities, so any dominance found under this under-approximation holds for the true schedule.

**Results** (`indep_2e6.out`, `compare3.out`):

| quantity | result |
|---|---|
| (p, κ) pairs, p < 2·10^6, 2 ≤ κ ≤ 9 | 496,058 |
| pairs with no IS-free candidate | 0 |
| pairs with no candidate satisfying e_Z ≤ κL and K_Z < κ^{f(κ)L} | 0 |
| pairs with no candidate of degree ≤ κ | only (5,4) (e° = 5, L = 3) |
| candidates violating K_Z ≤ (κ−1)^{f(e_Z)}, the lemma's bound, at any pair | 0 |
| bad certificates | 0 |
| degree disagreements with `degs_isfree_2000000.json` | 0 |
| degree disagreements with `ref20_copy/degs_ref20_noS1_2000000.json` | 0 |
| max e° per κ | {2:2, 3:2, 4:5, 5:4, 6:6, 7:5, 8:6, 9:4}, the same as `compare_degs.out` |
| E(c), c = 2..9, S1 forbidden, p < 2·10^6 | 3, 5, 9, 10, 14, 16, 18, 20 |
| attainers at c = 9 | 266: the 260 primes ≡ 1 (mod 2520) and 37, 43, 73, 127, 181, 631 |
| smallest margins κ^{f(κ)L}/K_Z | the same as `isfree_2e6.out` (2 at κ = 2 … 1.41e33 at κ = 9) |
| max least constant K° per κ | {2:1, 3:2, 4:27, 5:16, 6:125, 7:72, 8:9, 9:262144}, all ≤ c_κ, so C^+_c = C_c holds for H° |

The attainer lists for E(c), c = 2..9, agree with Lemma plus-exponent(ii).

**Independence from the rc_cache data.** The run below 600 was repeated without the rc_cache certificates (`indep_600_norc.out`). All 341 pairs still agree.

**Capped searches.**
- My budgeted DFS capped 1394 step searches below 600. These were treated as unavailable, and the degrees still agree everywhere.
- The authors' three capped DFS runs at p = 307 are the steps (9, Z_9, Ω) with Ω ∈ {{0,1,3}, {0,2,8}, {0,6,7}}. Treating them as unavailable is **conservative** for the IS-free claim: under-approximation can only raise A°. It is also neutral for e° = e^+, because both schedules see the same availability, and (i) follows from (ii) anyway.
- The value e^+(307, 9) = 4 is therefore **UNKNOWN between 3 and 4**: such a step plus a second step would give a degree-3 chain. This cannot change any E(c), because p = 307 attains none of them. Its sums for c = 2..9 are 3, 5, 7, 8, 11, 12, 14, 18, against the maxima 3, 5, 9, 10, 14, 16, 18, 20.

**Exactness at the attainer primes.** My searches were exhaustive (no caps) at p = 5, 7, 11, 29 and 31. At p = 43, a rerun with a 2·10^7 budget (`p43_bigbudget.out`) had no caps, and 48 steps were exhausted as NONE. So the attainers of E(4), E(6), E(7) and E(8) at those primes are exact for this enumeration. This is a side check of Lemma plus-exponent(ii), not part of the claim.

**κ = 10** (`kappa10_ref.py`; outputs `kappa10_ref_4e4.out` and `kappa10_ref_2e6.out`; H°_5 is from my program):
- 1044 primes below 4·10^4 have 10 | p−1;
- every one of them has an admissible plan and a dominating candidate;
- the histogram {3:1026, 4:9, 6:8, 16:1} is identical to `kappa10.out`;
- the maximum, 16 at p = 11 (t = 11, L = 4, plan (H°_5, 4, F0), K = 16^4), is as stated;
- extended to all p < 2·10^6 (37,188 primes): no failure.

All runs used `nice -n 19`. The largest took 86 s with RSS well under the cap.

## Obligation 1: the statements and proofs

**lem:plus-free-const: correct.** I re-derived K for each candidate type against Def. plus-schedule and Thm plus(iii):
- (b) TL: (κ−1)(a+1)^2, which equals (κ−1)^{f(2)}.
- (c) TW: 2K_3, degree e_3+1.
- (d), (f2), (f3), chain finishes: K_0∏(|Δ_t|−1). The bound uses |Δ_t| ≤ D_t ≤ κ and f(e_0+L') − f(e_0) = e_0L' + f(L') ≥ L'.
- (e): (κ−1)^{f(ℓ)} by definition.
- Plans: K_N^s K_F, bounded by superadditivity, with F0 = (0, 1) and F1 = (1, 1).

Two further points:
- The inner hypothesis at D = 2 forces K°_2 = 1, which holds (plan over GE). The computation finds no violation of K_Z ≤ (κ−1)^{f(e_Z)} at any candidate of any pair, which is a falsification test of the lemma and passed.
- The deduction "e_Z ≤ κ ⇒ arity_Z(a) < G(κ,a)^L for every a ≥ 0" is valid. A_Z(a) ≤ K_Z(a+1)^{e_Z} (proof of Thm plus(iii)), with K_Z ≤ (κ−1)^{f(κ)} < κ^{f(κ)} ≤ κ^{f(κ)L} and e_Z ≤ κ ≤ κL. Here L ≥ 1 because t ≥ 2, and (a+1)^{e} ≤ (a+1)^{κL}.

**thm:plus-free (i)/(ii): correct.**
- **Induction.** The induction over divisors is sound: A^+ = min(G^L, A°) once the inner arities agree, and e^+ = min(κL, e°).
- **Strictness.** The inequality is strict, so the tie order, which puts (a) first, never selects (a).
- **"Never the least arity" against "never needed".** (ii) proves the former, for every a ≥ 0, every depth ≥ L and every inner solver. "Not needed" then holds for this procedure only, which is how the edits use it.
- **Large p (p ≥ 2·10^6).** The argument is correct:
  - all six table steps have T_exist ≤ 1,995,734 < 2·10^6;
  - p ≥ 4·9^4 makes (1, F1) the admissible plans, by definition;
  - the per-κ candidates of degree ≤ κ follow lem:plus-exponent's large-prime paragraph.
- **(5,4) hand proof: correct.**
  - h = 1, so P = {1}, and ξ = g = 2.
  - ε = −ξ^{−2} = −4^{−1} = −4 = 1 (mod 5), so c^{(2)} = (1,1,1,1).
  - T_2 = {1,2,3,4} = F_5^×, so F1 is admissible at s = 2.
  - The plan has degree 2·2 + 1 = 5 ≤ 12 = κL and constant 1 < 4^{18}.
  - t_{5,4} = 5, so L = 3.

**thm:plus-free (iii): correct.**
- **Las Vegas task count.** With (a) and the zero sums removed, the Las Vegas tasks of Thm plus(iv) are ξ (only for p ≥ 2·10^6) and at most 11 contraction searches. q = ξ^{κ'/2} is deterministic for even κ' ≤ 9 (Def. plus-schedule, preprocessing). So there are at most 12.
- **t is not needed.** t_{p,κ} is not needed at all to compute A°. It enters only the comparison.
- **No other IS use.** I found no other place where the solver proof or the preprocessing uses IS:
  - Cor hcd(i)'s zero-sum F0 is not a candidate;
  - for p < 4κ^4 the F0 vectors come from the T_j tables.

**Precision.** H°_κ depends on p, but the statement defines it before "Let p be…". This is F10.

## Obligation 3: scope of cor:main-free

I checked the proof of thm:main (Section sec:proof-main), rem:main-solver, rem:is-import(d) and rem:oblivious, and the proofs of the four corollaries.

**Where the import enters.** thm:is-import enters only through candidate (a): Thm plus(ii) → Thm halving(ii) → lem:rounds.

**Unaffected parts:**
- **Error budget:** n_pre ≤ 12 ≤ 2(c−1)+12.
- **Las Vegas cut-offs:** unchanged.
- **Determinism:** the main theorem is bounded-error and claims no determinism. "Schedule 1 alone … deterministic given its zero sums" remains a statement about Schedule 1.
- **The bounds (3)–(4):** they are inequalities among defined numbers (A^+ = A°, A, B, B̄ and the exponents E_1, E_H, E_+), proved without IS.
- **C^+_c = C_c:** this needs K° ≤ c_κ, which holds (table above). The large-p constants are explicit.

**Corollaries:**
- cor:black-box calls thm:main at class ≤ c.
- cor:black-box-pe calls it on F_p sections of class ≤ c, through rem:oblivious, which holds verbatim for H°.
- cor:nilpotent calls black-box-pe at p > c, plus Imran–Ivanyos Thm 1 at p ≤ c. That is a different import, and it is correctly kept.
- cor:utz calls cor:nilpotent at c = n − 1, so n ≤ 10.

None of them uses Schedule 1 elsewhere. The scope claims are **PROVED given cited theorems + exact computation**.

## Findings and fixes

**F1 (minor, wording), fragment.tex closing paragraph after the proof of thm:plus-free.**
- old: `So at $\kappa \le 9$ candidate~(a) never attains an arity, at the depth $L_d$ or at any larger depth:`
- new: `So at $\kappa \le 9$ candidate~(a) never attains the least arity $A^+_\kappa(a)$, for any $a \ge 0$, at the depth $L_d$ or at any larger depth:`
- In the same paragraph, replace `two independently written programs (AI-written, Appendix~\ref{app:artifacts}), which agree` with `three independently written programs (AI-written, Appendix~\ref{app:artifacts}; the third, by the referee, under-approximates availability by verified certificates only), which agree`.

**F2 (minor, structure), E3 together with cor:main-free.** With E3, Theorem main asserts the c ≤ 9 case itself, and that case is proved only by a later "corollary" whose proof re-runs Section proof-main with H°. This is not circular, but it reads backwards.
- Retitle PART 3 `\begin{corollary}[Theorem~\ref{thm:main} without the import for $c \le 9$]` → `\begin{proposition}[The case $c \le 9$ of Theorem~\ref{thm:main}]`, and `\end{corollary}` → `\end{proposition}` (keep the label).
- Add at the end of the paragraph "Correctness of the ideal procedure" of sec:proof-main: `For $c \le 9$ the same argument, with $\mathcal H^\circ$ in place of $\mathcal H^+$, uses no part of Theorem~\ref{thm:is-import} (Proposition~\ref{cor:main-free}).`

**F3 (medium, misdescription introduced by the change), main-core.tex:222, related work.** The composition of [BCvD, Lemma 1] with [IS15, Cor 8] still needs all of IS15, which the paper no longer imports for c ≤ 9.
- old: `conditional on the same import as Theorem~\ref{thm:main}; we have not found`
- new: `conditional on~\cite[Corollary~8]{IvanyosSantha2015}, which rests on their Theorems~3 and~5; we have not found`
- Add this as edit E8b.

**F4 (medium, contradicts E5c), main-core.tex:257, Verification Status.** The chain "20 rests on everything 38 rests on", with "38 … on everything 53 rests on", which includes lem:rounds, contradicts E5c ("not on … Lemma rounds").
- old: `The stated exponent $\ReesClassNinePlusExp$ rests on everything $\ReesClassNineHalvedExp$ rests on and, in addition, on Section~\ref{sec:plus}.`
- new: `The stated exponent $\ReesClassNinePlusExp$ rests on the halving of Section~\ref{sec:halving}, on Section~\ref{sec:plus} and on the exact computations of Lemma~\ref{lem:plus-exponent} and Theorem~\ref{thm:plus-free}; by Theorem~\ref{thm:plus-free} it does not rest on Lemma~\ref{lem:rounds} or Theorem~\ref{thm:is-import}.`

**F5 (minor, status), E10.**
- In the new sentence, replace `whose degrees were reproduced by two independently written programs; it was written by one AI session, has not been refereed, and no human has read it.` with `whose degrees were reproduced by three independently written programs; it was written by one AI session and refereed by a second (verdict: proved with fixes, applied here), and no human has read it.`
- The stale "has not itself been refereed" at main-core.tex:257 and :787 (flagged by the author) should be updated at the same time.

**F6 (minor), E12.** Lemma rounds is also used only for c ≥ 10.
- In E12's new text, replace `Theorem~\ref{thm:is-import} (for $c \ge 10$), Lemma~\ref{lem:rounds} and` with `Theorem~\ref{thm:is-import} and Lemma~\ref{lem:rounds} (both only for $c \ge 10$) and`.

**F7 (minor, consistency).** After E7a, E13a and E13b the text says the corollaries are conditional "only for c ≥ 10", but their statements still assume the import unconditionally. This is conservative, not wrong. For consistency, either add these edits or leave the statements and drop "and only for $c \ge 10$" from E7a and E13a:
- main-core.tex:1172: `Fix $c \ge 1$ and assume Theorem~\ref{thm:is-import}. Let $G = \langle g_1,\dots,g_s\rangle$ be a black-box group` → `Fix $c \ge 1$, and if $c \ge 10$ assume Theorem~\ref{thm:is-import} (Corollary~\ref{cor:main-free}). Let $G = \langle g_1,\dots,g_s\rangle$ be a black-box group`
- main-core.tex:1196: the same, with anchor `…\rangle$, its encodings, its multiplication oracle, $f$, $w$ and $L$`.
- main-core.tex:1239: `Fix $c \ge 1$ and assume Theorem~\ref{thm:is-import}; for the primes $p \le c$` → `Fix $c \ge 1$, and if $c \ge 10$ assume Theorem~\ref{thm:is-import}; for the primes $p \le c$`
- main-core.tex:1270: `Fix $n \ge 2$ and assume Theorem~\ref{thm:is-import}.` → `Fix $n \ge 2$, and if $n \ge 11$ assume Theorem~\ref{thm:is-import}.`

**F8 (optional), main-core.tex:189, thm:main(3).**
- old: `the $t_{p,\kappa}$,`
- new: `for $c \ge 10$ the $t_{p,\kappa}$,`
- For c ≤ 9, A^+ = A° does not depend on t. The current text overstates the dependence, which is harmless.

**F9 (PART 2, rem:plus-free-ten).** The support is adequate, and independently confirmed.
- **Why the support holds.** "Checked only below 4·10^4" is not a weakness. The check is complete over the primes below 4·10^4. Above 4·10^4 the claim is proved from (1, F1) over H°_5, with e°_5 ≤ 4. That bound comes from three programs below 2·10^6 and from TL_5 above 2·10^6.
- **Missing detail.** At κ = 10 the node is (f1) with ε = −q^{−1}, and q comes from Def. schedule1h: Las Vegas θ trials unless h is odd. So at c = 10 the preprocessing has up to 13 Las Vegas tasks, or q = ξ^5 can be used (ξ is a nonsquare, so (ξ^5)^h = −1).
- **Sentence to add.** After `so Lemma~\ref{lem:plus-free-const} applies.`, insert: `The preprocessing at $\kappa = 10$ adds the element $q$, which may be taken to be $\xi^5$, so it has at most $13$ Las Vegas tasks, within the budget of Remark~\ref{rem:is-import}(d).`
- **Recommendation.** It may be adopted as a remark (low priority): it buys only c = 10 and n = 11. Its last two sentences (κ = 11 has only candidate (a)) are worth keeping in any case. If PART 2 is dropped, drop the clause in E11 as the fragment says.

**F10 (minor, quantifiers), thm:plus-free.** Move `Let $p$ be an odd prime and $\kappa \le 9$ a divisor of $p-1$.` to the start of the statement, before "let $\mathcal H^\circ_\kappa$ be".

**F11 (minor), E14b in the Outlook.** That section says "Nothing in this section is claimed here", but the new sentence states a proved fact. Append `(proved; Theorem~\ref{thm:plus-free})` after "at either depth".

**F12 (artifacts), E15.** Add: `\file{research/audits/reviews/2026-11-14-rees-is-free-referee/indep_isfree.py} (third program, availability only from verified certificates) and \file{kappa10_ref.py} in the same folder, with their outputs.`

**Other edits.** E1, E2, E4, E5a–c, E6a–b, E7b–c, E8, E9a–b, E11, E13b and E14a make no claim stronger than proved and drop no caveat. They also correctly state what still needs IS:
- c ≥ 10, and c ≥ 11 at p ≡ 1 (mod 11);
- standalone Schedules 1 and 1H (53 and 38);
- the full-depth values 145 and 95.

E11's "only candidate at κ = 11" is correct: (b)–(e), (f2), (f3) and (fΩ) need κ ≤ 9, and (f1) needs even κ.

## Adversarial self-check

1. **Shared reading of the text.** My program implements the same Definition plus-schedule that the two earlier programs read. A misreading shared by all three (for example of which chains count as finishes, or of admissibility of F_K) would not be caught. I read the definition from the core, not from their code, and I did not open `isfree_check.py`, `plus_mine.py` or `plus2.py` beyond locating data paths. The match at all 496,058 pairs, including (5,4) = 5 and the 266 attainers, is evidence of agreement, not of correctness.
2. **Data reuse.** Positive availability below T_exist rests on stored certificates, which my checker re-verified (0 bad), and on my own search. Negative availability is only under-approximated by me. This suffices for the IS-free claim, by monotonicity. It does not independently establish the exact degrees at primes ≤ 523 where my search capped. Lemma plus-exponent(ii)'s exact values there remain on the earlier exhaustive C searches, except at the attainer primes 5, 7, 11, 29, 31 and 43, where my searches were exhaustive.
3. **Monotonicity argument.** "Under-approximation is conservative" uses that every candidate's arity is nondecreasing in the inner arities and that removing steps only removes candidates. Both are true by Def. plus-schedule: arities are products of inner arities and positive factors, and minima over fewer candidates are larger.
4. **Bounds, not exact arities.** The dominance test uses the bound K_Z(a+1)^{e_Z}, not exact arities. It is sufficient, not necessary, so it cannot produce a false pass.
5. **Finite checks only falsify.** The large-p case is a proof, which I checked by hand. The κ ≤ 9 computation is an exact finite computation over a finite set, so for p < 2·10^6 it is the proof itself, not a sample.
6. **Not checked.** I did not re-check Lemma plus-sm, the table thresholds beyond Φ at T_exist and T_exist − 1 in floating point, or Thm plus(ii) itself. The result inherits their AI-only status. I did not compile the patched TeX.
