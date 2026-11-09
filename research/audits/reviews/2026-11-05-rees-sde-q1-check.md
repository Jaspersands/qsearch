# Referee check: Rees diagonal SDE, Q1 (closure, absorption, Theorem Q1)

AI-only adversarial check, 5 November 2026, pending human review. Under review:
`2026-11-05-rees-sde-q1.md` and its folder `2026-11-05-rees-sde-q1/`. Scripts and outputs of this
check are in `2026-11-05-rees-sde-q1-check/`. Everything ran under `nice -n 10`, with at most 2
processes. No `.tex` file, git state, `STATE.md` or `make_numbers.py` was touched.

**Independent code.** `myq1.py` re-implements ALG-Q1 from the report's text and imports nothing
from the authors' code. It has its own:
- field arithmetic, elimination, primitive root and coset classes;
- forward pass, with different tie rules: it swaps out the *last* eligible σ, and splits blocks by
  the `last`, `first` or `random` rule;
- absorption by an **exact minimum-load** search (brute force over absorption bases), where the
  authors use a greedy rule;
- check of (S) at every leaf, and of (F1)/(F2) for every flag;
- backward pass by rejection sampling, so large p works;
- witness verifier `verify`.

Every inequality used in the proof of Theorem Q1 is asserted at run time.

## 1. Verdict table

| claim | verdict | fix |
|---|---|---|
| Lemma 2 (steering without circuits) | **Holds** | none. Re-derived: Theorem B(ii) needs only blocks inside classes; Cases 1 and 2 of the first-coincidence bound never use the circuit property; ρ counts every cross pair, including the top pair and 2-block rounds |
| Lemma A (closed prefix) | **Holds** | none. Its hypothesis U_t ≠ 0 is essential, see the next row |
| Corollary A: structure of a stall (pool ⊆ span(B∩U), Fin spans span(B∩U), \|B∖U\| = q+ε, ε = 0 ⇔ Lemma A) | **Holds** | none |
| Corollary A, "every stall with \|B∖U_L\| = q is solved … needs no column count"; §0 item 1 ("needs no column count beyond reaching the stall"); LaTeX (i) | **Error (edge case)** | Add **U_L ≠ 0**. Counterexample: e₁, e₂, e₁+e₂ in F₇², κ = 2. It stalls with U_L = 0, q = 2, \|B∖U\| = 2, ε = 0, and it has **no** nonzero solution (`cor_a_counterexample.out`). The bank of one column is another. U_L ≠ 0 holds as soon as one round exists, so it is automatic when M ≥ D_3(r)+r (then π ≥ 1) |
| Lemma R (absorption) | **Holds** | none. The blocks stay inside one class: the new singleton has the class of its parent block. At most 3+c distinct offsets remain after same-class merging, so G*_{3+c} applies. The "moreover" part was asserted on every absorption (0 violations) |
| Lemma S | **Holds** | none |
| Lemma T′ (top pair) | **Holds** | none. Every pair was tested at every top-pair event (0 bad) |
| Theorem Q1(a): case counts, recursion, determinism | **Holds** | Two small gaps. The proof shows c ≤ ⌊r/2⌋ only for q ≥ 3; add "for q ≤ 2, b, ε ≥ 1 give r ≥ q+2". The code's forward pass uses the *random* splitting rule; the theorem needs a fixed rule (any rule works) |
| Budget f(r) = ⌊(r+2)²/4⌋ + **3r** | **Holds, but the 3r is not needed** | The same proof works at f(r) = ⌊(r+2)²/4⌋ + **r**, the budget of Conjecture 5 (§3.1). So the report's arity remark ("the extra 2r is used only in cases 2–4"), its §4 bullet "Not covered … cases 2–4 use the extra 2r", and the reason given in the §6 gate ("Q1 uses 3a, not a") are **errors**. The gate itself stays false, because c is not bounded |
| Theorem Q1(b) | **Holds** (true by definition) | The word "heavy" is used in two senses. §0 item 4 requires "both checkable recursion counts failing"; Theorem (b) and §4 do not. By the §0 definition, **none** of the 8 computed stalls is heavy, since rec-Y applied to all of them. Use one definition |
| Theorem Q1(c): failure bound and p-thresholds | **Holds** | none. The numbers re-derive exactly (§3.3). Also fix §0 item 3, "succeeds with probability ≥ 1/2 per pass": this holds only under the p-condition |
| "Heavy stalls with c ≥ 3 exist [computed]" | **Holds with fix** | They exist in the *weak* sense: absorption would need ≥ 3 splittings in one round (confirmed with exact minimum load, κ = 2 and κ = 3). ALG-Q1 *with its fallbacks* produced no leaf with c ≥ 3. At the 3r budget it **provably cannot** for r ≤ 8 (any absorption rule), or r ≤ 10 (minimum-load rule) (§3.2). So every search in the report (a ≤ 7) ran where the obstruction cannot appear |
| 33/33 search banks solved by closure | **Holds** | none. Reproduced with the authors' code (new seed) and own code under 3 split rules and own swap rule: 99/99, 0 vanishing functionals, 0/20 single-pass failures each |
| §5 artifact numbers | **Holds** | none. 648; 13,176; 8 heavy; 184/0; 310/28/85/9/7; 338/100/13 all match the outputs |
| [argued] matroid-intersection load | **Holds** | none. Rado's theorem gives the min-max |
| Proposed LaTeX (§9) | **Holds with fix** | (i) needs U_L ≠ 0, and "succeeds" must become the failure bound. Define the sources and "free columns". Reword "stalls with c = 3 occur". Use the paper's provenance-item convention instead of `\file` in the body. Text in §5 |

## 2. Re-derivations (what was checked and how)

- **Lemma 2.**
  - Values and telescoping: re-derived as in Theorem 2(c).
  - With Src ⊆ U_L, τ ∈ U_L, so the coordinates in the flag basis exist.
  - The steering functionals live on U_L. Each is nonzero there, because Π_j is the identity on
    U_j and W^{(j)}_{1..} is a basis of Ω_j.
  - Restricting the sources to U_L changes nothing in Case 1. Case 2 needs only that some
    σ ∈ Src has φ(σ) ≠ 0, which (S) gives once every φ(e_l), l > j, vanishes.
- **Corollary A.**
  - B∩U_l only grows: swaps remove only σ ∈ B∖U, and U grows. So the pool lies in span(B∩U_L).
  - The unused columns are independent modulo U.
  - Then b = dim span(B∩U) = dim span(Fin), and |B∖U| = r − b = q + ε.
  - The spanning claim "B∩U_L and the pool span U_L" therefore holds **exactly** when ε = 0. The
    report states this correctly, but only for U_L ≠ 0 (row 4).
- **Lemma R.**
  - Write W′_b = W_b − δ_iλ_i and W′_n = δ_iλ_i, with e unchanged. Then
    Ω′_l = Ω_l + Fλ_i for b = 0 and for b ≥ 1.
  - The final space is U_L ⊕ Fλ_i, spanned by dim U_L + 1 generators. Hence (F1) holds for
    every round.
  - Singleton blocks lie in U_l, so every round column outside the current space is in a block of
    size ≥ 2.
- **Lemma S, Lemma T′.**
  - For singleton blocks, span(e) + Ω = span{λ_i : i ∈ S}. So vanishing on Src and on every
    e_l (l > j) would force vanishing on Fr, and Fr ⊇ B spans V.
  - The top functional is a multiple of v ↦ v̄, nonzero at any third column of X.
- **Theorem Q1 counts.**
  - π ≥ 2r + D_3(q) − q at the 3r budget.
  - Case 2: needs 2r + 1 ≥ 2b, true. Case 3: needs |X| ≤ r − b + q ≤ r + 1 and
    f(r) − f(r−2) = r + 7. CODIM1: f(r) − f(r−1) ≥ 4.
  - The identities D_3(q) − D_3(q−2) = q + 1 and the case inequalities were checked for r < 400
    and r < 200 (`barrier.out`).
- **Determinism.**
  - Every recursion is a single branch on a sub-bank of smaller rank, and nothing backtracks
    (`recurse` returns `None` on failure). So the depth is ≤ r.
  - Each level costs one forward pass, ≤ r absorptions and O(M²) Gaussian eliminations.
  - This is polynomial in (M, a, log p).

## 3. New findings

### 3.1 The budget D_3(r)+r already suffices [proved here; checked with the counts asserted]

Run the same proof with f₁(r) = D_3(r) + r. Each step goes through.
- **Stall.** Theorem 2(b) gives π ≥ M − r − (D_3(r) − D_3(q)) − q ≥ D_3(q) − q ≥ 1, so U ≠ 0,
  b ≥ 1 and r ≥ 2.
- **Case 2** (q ≥ 3, b ≤ q−2). cols(Y) ≥ b + π ≥ b + D_3(q) − q = b + D_3(q−2) + 1
  ≥ D_3(b) + b + 1 > f₁(b).
- **Case 3** (q⁺ ≥ 2). There are ≤ r+1 columns outside U⁺, as before. So
  cols(U⁺) ≥ D_3(r) − 1 = D_3(r−2) + r ≥ f₁(r−2) ≥ f₁(r−q⁺).
- **CODIM1 recursion.** cols(H) ≥ f₁(r) − 2 ≥ f₁(r−1), since D_3(r) − D_3(r−1) ≥ 1.
- **Cases 1 and 4, and parts (b) and (c),** use no count.

So Theorem Q1(a)–(c) hold verbatim for every bank of rank r with ≥ ⌊(r+2)²/4⌋ + r columns, which
is the budget of Conjecture 5. Conjecture 5 is still not proved, because c is not bounded.

Computed, with all counts asserted for f₁ (`run_banks_c1.out`, `fresh_c1_k*.out`,
`target_c1_k*.out`):
- 396 runs on the 33 search banks, which sit exactly at f₁(a), in 3 split rules and shuffled
  orders;
- 4,004 family and climb banks, and 1,400 targeted banks, κ ∈ {2, 3}, a ≤ 10;
- **0 assertion failures, 0 unsolved.**
- 9 weak heavy stalls (one with optimal load 4: κ = 3, a = 8, q = 4). All were resolved by the
  fallbacks, and the largest leaf load was 2.

**Caveat for integration.** This is one AI pass. The endorsed LaTeX (§5) keeps the report's 3r.
The +r version is offered as an option that needs one more independent check.

### 3.2 Where a c ≥ 3 leaf can occur at all [proved by counting]

Take a case-4 stall with q ≥ 3, b ≥ q−1, ε ≥ 1 and r = q+b+ε. The two fallbacks fail only if:
- (Y fails) |Rcols| + |T| ≥ f(r) − r + b − f(b) + 1;
- (U fails) Rout + |T| ≥ f(r) − r + b − f(r−q) + 1, using cols(U) = b + π + (|Rcols| − Rout).

At the report's budget (C = 3):
- **The Y-fallback alone** fails only if D_3(b) > D_3(q) + q + 2ε. This needs b ≥ 5, so
  **r ≥ 9** (`barrier.out`). So for every bank of rank ≤ 8, ALG-Q1 with its Y-fallback has
  **c ≤ 2, under any absorption rule.**
- **Both fallbacks, crude** (Rout ≤ |Rcols| ≤ D_3(r) − D_3(q)): possible from r = 9, but only with
  q = 3. The first shape with q ≥ 4 is at r = 11 (`barrier_both.out`).
- **q = 3 with minimum-load absorption.** Load ≥ 3 holds iff q⁺ = 0 and all of Rout lies in one
  round (Rado, capacity 2). So Rout ≤ r + 1, and both fallbacks can then fail only from
  **r = 39** (`barrier_both.out`). With the Y-fallback alone, the sharper bound is r ≥ 11
  (`barrier_q3.out`).
- Hence, with minimum-load absorption and both fallbacks, **c ≤ 2 for every bank of rank ≤ 10.**

Consequences:
- The report's searches (κ = 2, a ≤ 7; κ = 3, a ≤ 6) could never have found a c ≥ 3 leaf.
- The search proposed in §8 must go to a ≥ 11 at the 3r budget. At the r budget the counts are
  much looser: crude both-fail shapes appear from r = 6.

### 3.3 Numbers [re-derived] (`barrier.out`)

Lemma W bound κ^{−E}(p − E − (κ^E − 1)(E − 1)√p), and the least p at which its minimum over
e ≤ E is ≥ p/(2κ^E):

| κ | E = 3 | E = 4 | E = 5 | E = 6 |
|---|---|---|---|---|
| 2 | 796 (p/16) | 8,116 (p/32) | **61,524 (p/64)** | 396,924 |
| 3 | 10,828 (p/54) | 230,416 (p/162) | **3,748,116 (p/486)** | 52,998,424 |

- So the report's p ≥ 62000 and p ≥ 3.75·10⁶ are correct, rounded up.
- 2.5r·64/p ≤ 1/2 gives p ≥ 320r, and 2.5r·486/p ≤ 1/2 gives p ≥ 2430r. Also
  κ/(p−1) ≤ 2κ⁵/p.
- The general range p ≥ max(8κ^{2E′}E′², 2E′rκ^{E′}), E′ = 3+c, was checked for c ≤ 5.
- (Optional sharpening: c ≤ 1 needs only E = 4.)

### 3.4 Other wording errors

- §4 says the big round holds "5–6 of the Rout columns". In fact it holds **all** of Rout (5 or 6
  columns; 4 in some of the referee's reruns), as Rado requires at q = 3.
- §3's ALG-Q1 table omits the heavy-stall fallbacks. They appear only in the "Load" bullet, yet
  §0 and §4 report results that depend on them.

## 4. Computations (all witnesses verified by the independent `verify`)

| artifact | what | result |
|---|---|---|
| `rerun_closure_seed7.out` | authors' `closure_on_search_banks.py`, new seed | 33/33, 0 bad, 0/20 |
| `run_banks.py` → `run_banks.out` | own code: 33 search banks × 3 split rules (closure); 8 saved heavy banks × 40 × {no fallback, fallback} | 99/99 closures, 0 bad functionals, 0/20 failures. Heavy stall reproduced in every run, exact minimum load 3. Without fallback: 6-block leaf, 0 single-pass failures. With fallback: rec-Y |
| `run_fresh.py` → `fresh_k2.out`, `fresh_k3.out` | own families + climb, budget 3r, p ∈ {1009, 10007/10009}, a ≤ 8 (κ = 2), a ≤ 7 (κ = 3) | 2,184 + 1,820 banks, 0 assertion failures, 0 unsolved |
| `fresh_k2_p62003.out`, `fresh_k3_p3750001.out` | the same at the theorem's primes p = 62003 (κ = 2), p = 3,750,001 (κ = 3) | 245 + 140 banks, 0 failures, 0 single-pass failures |
| `run_target.py` → `target_k2.out`, `target_k3.out` | branches aimed at rec-U⁺, CODIM1, q ≥ 3; a ≤ 10 | 600 + 500 banks, 0 failures. 4 weak heavy stalls (κ = 2, a = 8; κ = 3, a = 7), all rec-Y |
| `run_banks_c1.py`, `fresh_c1_*`, `target_c1_*` | budget D_3(r)+r, all counts asserted | §3.1: 0 failures |
| `barrier.py`, `barrier_q3.py`, `barrier_both.py` | identities, thresholds, fallback barriers | §3.2, §3.3 |
| `cor_a_counterexample.py` | the U_L = 0 stall | unsolvable, as stated in row 4 |

Single-pass failures before success, over all leaves of all runs: ≤ 2 per run file, all at
p ≈ 10³–10⁴. These are consistent with Lemma 2's bound.

**Attempts to break Theorem Q1 at its budget for c ≤ 2 found nothing:**
- no count assertion failed;
- no (S) violation occurred at any leaf;
- no (F1)/(F2) violation occurred;
- no bank was left unsolved.

## 5. Final remark text endorsed for the integrator

Location: after `rem:sde-worst-case` in `docs/papers/rees-hsp/appendix-sde-side.tex`. It needs a
provenance item, given below, in `appendix-provenance.tex` after `prov:sde-worst-case`. It does
not change Theorem main, any table or the arity (a+1)(a+2)/2.

```latex
\begin{remark}[Worst case beyond general position; AI-checked, pending human review]
\label{rem:sde-worst-case-q1}
This remark is AI-checked, pending human review (Appendix~\ref{app:provenance}, item~\ref{prov:sde-worst-case-q1}); no human has checked it, and nothing else in the paper uses it. Keep the notation of Remark~\ref{rem:sde-worst-case}, with $J=3$ and $\kappa\in\{2,3\}$. A round is a set $S$ of columns with a relation vector $\delta$ that is nonzero on $S$, split into blocks each inside one class of $\delta$. Call a family of rounds with disjoint supports a flag if, for each round, the block sums with index $b\ge1$ are independent modulo the space realised by the earlier rounds, and the sum $\sum_{i\in S}\delta_i\lambda_i$ of all its block sums lies in that space. The argument for the success bound in Remark~\ref{rem:sde-worst-case}(b) uses neither the circuit property nor the bound $J$ on the number of blocks, except through $\mathcal{G}^*$. Let $S_0$ be a nonempty set of columns outside the rounds whose span lies in the realised space, give its columns independent weights uniform in $P$, and let $J'$ be the largest number of blocks of a round, with $\mathcal{G}^*_{J'}(p)\ge1$. Suppose that no offset-difference functional of two blocks in different classes vanishes on the span of $S_0$ and of the sums $\sum_{i\in S}\delta_i\lambda_i$ of the later rounds. Then each back substitution started from $S_0$ fails with probability at most $\rho_{\mathrm{pr}}\max\bigl(1/\mathcal{G}^*_{J'}(p),\kappa/(p-1)\bigr)$. Three consequences follow, where $U_L$ is the space realised when the forward pass stops.
(i) If the forward pass stalls with $U_L\ne0$ and $|B\setminus U_L|=\dim V-\dim U_L$, in particular at codimension $1$ with one reserved column outside $U_L$, then the true-pool columns and $B\cap U_L$ span $U_L$, they satisfy this condition, and back substitution on $U_L$ with them as $S_0$ has this failure bound. The condition $U_L\ne0$ holds whenever the bank has at least $D_3(r)+r$ columns.
(ii) Splitting a column $i$ with $\lambda_i\notin U_L$ out of a block of size at least two into its own block yields a flag realising $U_L\oplus\Fp\lambda_i$.
(iii) Suppose a flag realises a hyperplane of $V$, the columns outside its rounds span $V$, and at least three of them lie outside the hyperplane. Then any two of those three form a top round of two singleton blocks, and with the remaining columns outside the rounds as $S_0$ the condition above holds automatically.
With these steps, and with recursion on the columns in the span of $B\cap U_L$, or in the span of the round columns, whenever the counts of the proof guarantee enough columns there, every bank of rank $r$ with at least $\lfloor(r+2)^2/4\rfloor+3r$ columns is reduced in deterministic polynomial time either to a solution, or to a flag together with such a set $S_0$, whose rounds have at most $3+c$ blocks. Here $c\le\lfloor r/2\rfloor$ is the largest number of splittings made in one round, and $c\le2$ unless the splittings at some stall of codimension at least $3$ put three or more into one round. When $c\le2$, the back substitution fails with probability at most $1/2$ for $\kappa=2$ and $p\ge\max(62000,320r)$, and for $\kappa=3$ and $p\ge\max(3.75\cdot10^6,2430r)$. Stalls at which three splittings must go into one round occur for $\kappa\in\{2,3\}$ and $a\in\{7,8\}$. In every one found, the recursion on the span of $B\cap U_L$ applied instead (sampled computation, repeated with independent code, AI-checked, pending human review). No bound on $c$ is proved. So the best arity proved in this paper for arbitrary columns remains $(a+1)(a+2)/2$, and no count of Theorem~\ref{thm:main}, no $E_W(c)$ and no table changes.
\end{remark}
```

Provenance item (for `appendix-provenance.tex`, after `prov:sde-worst-case`):

```latex
\item \label{prov:sde-worst-case-q1} \textbf{Remark~\ref{rem:sde-worst-case-q1} (worst case beyond general position).}
Status: parts~(i)--(iii) and the reduction proved; the stalls needing three splittings in one round sampled computations, repeated with independent code; no bound on $c$; AI-checked, pending human review.
Source: \file{research/audits/reviews/2026-11-05-rees-sde-q1.md}.
Checks: \file{research/audits/reviews/2026-11-05-rees-sde-q1-check.md} (adversarial check with independent code; corrections incorporated here).
```

**Optional, pending one more independent check (§3.1).** To use the r budget, replace
`$\lfloor(r+2)^2/4\rfloor+3r$` by `$\lfloor(r+2)^2/4\rfloor+r$`. Nothing else in the remark changes.

## 6. Gates (unchanged, with corrected reasons)

The following still have to stay false:
- polynomial time for every bank at o(a²) columns;
- "heavy stalls cannot occur" (in the weak sense they do occur);
- "Conjecture 5 is proved". The reason is now only that c is unbounded, not the 3a budget;
- uniformity in p;
- any change to the quoted arity (a+1)(a+2)/2;
- any novelty claim.

The next hard question stays the report's §7, with one change: the search must use a ≥ 11 at the
3r budget, or a ≥ 6 at the r budget.
