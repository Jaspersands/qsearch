# Rees paper: appendix proof of the free-coordinate Schedule 3 theorem (continuation item 4, K7)

AI session only (Claude Code, 2026-11-02). No human review. Status of every claim below:
**AI-checked, pending human review.** This session wrote only
`docs/papers/rees-hsp/appendix-free-coordinate.tex`, this report and the folder
`research/audits/reviews/2026-11-02-rees-free-coordinate-appendix/`. It edited no other file,
committed nothing and flipped no gate.

## 0. Verdict

- **Proved (AI-checked, pending human review):** `thm:free-coordinate` (i), (ii) and (iii) as stated
  in `main.tex`, and `prop:rc-lower`, in a new Appendix F of about ten pages (pp. 87–96 of the test
  build). No step of (i)–(iii) failed and no counterexample to them was found. One clause of
  `prop:rc-lower` is false as worded (§3 item 7, with the smallest failing instance).
- Part (iii) is proved in a slightly **stronger** form. Any public pair (M_d, n_0) with
  β(M_d, n_0; g_d) ≤ τ_d works, not only the explicit pair in the statement. This matters because
  Table `tab:fcs-budget` was computed with the *least* such pair, not the explicit one.
- **Trial bound rechecked.** The report's `fcs_budget.py` was rerun, and its output is byte-identical to the
  committed `fcs_budget_out.txt`. An independent exact script reproduces the three (iii) columns of
  `tab:fcs-budget`. The largest per-node trial cap is **2^33.78** (p = 5281, grade 4, κ = 4,
  g_4 = 14, B = 40). Under part (ii) at u = 18 it is 2^34.3. So "about 2^34" holds.
- **Independent referee** (a fresh AI agent, read-only, given the files but not my reasoning).
  It found one ERROR, in the last clause of `prop:rc-lower` (§3 item 7). It found no error in
  (i)–(iii), confirmed the reuse of Appendix B and recomputed the table and the u = 2 constants
  exactly. Its GAPs and NITs are folded into §3 and into the appendix.
- **K7: the two Schedule 3 theorems can now be merged.** Every downstream use of `thm:random-column`
  (Cor `cor:fpt-r`, Cor `cor:codim`, Appendix E, Remark `rem:combined-schedule`, §`sec:recursion`)
  cites part (ii) only. `thm:free-coordinate`(ii) has the same hypotheses and conclusion, with a
  smaller trial count. See §6(e).

## 1. Exact statement proved

Setting: a finite p-group of class c < p, with Rees cover and quotient groups G_d as in
`main.tex` §`sec:recursion`, and an arbitrary H. The label law is not an extra assumption inside a
tree. It is derived from Lemma `lem:central` and Proposition `prop:descent` via Lemma `lem:s3-law`
and the tree factorization. In that sense the theorem stays "conditional on the label law", as the body says.

- **(i) One node** (Lemma `lem:fc-node`). Assume labels i.i.d. uniform on a subspace of dimension
  a ≤ g_d, κ_d < p−1, n_0 ≥ 1 and L = M − n_0 ≥ 0. Outside a bank event of probability at most
  β = 4/(h^{n_0−1}q^a) + (p^a−1)/((p−1)p^L), each trial is accepted with probability at least
  q^r/2 ≥ 1/(2κ^r), independently. Then ⌈2B ln2·q^{−r}⌉ trials on the same bank fail with probability at most
  2^{−B}. Root extraction and field draws are each capped at 2^{−B}. No condition on p, M or r is used beyond h ≥ 2.
- **(ii) Constant arity** (Lemma `lem:fc-params`, proof of (ii)). Assume u ≥ 2, c ≤ u, a_d ≤ u−1,
  p ≥ 16u², M = 4u and n_0 = 2u+1. Then β ≤ 4·15^{−2u}u^{−u−1} + 2p^{−u−1}, and each node uses at most
  2B ln2·u^{u−1}+1 trials. One tree aborts with probability at most 1/16, and the 4m'-tree
  restart gives success probability at least 1−ε at cost 2^{O(u log(u+2))}·poly(m, log p, w, log 1/ε), with
  absolute constants uniform in c (Prop `prop:fc-uniform`(a)).
- **(iii) Every prime p > c** (Lemmas `lem:fc-choice`, `lem:fc-forest`, proof of (iii)). Use FCS at
  every grade with 2 ≤ κ_d < p−1 and any public (M_d, n_0) with β(M_d, n_0; g_d) ≤ τ_d =
  ε/(9(c−1)S n_d). The explicit choice in the theorem is one such pair. Use the linear schedule at κ_d = 1, and
  Schedule 1 at degree d at κ_d = p−1, which forces d = p−1. Cap at B = ⌈log₂(27N/ε)⌉. Then the run
  returns 𝔥 with probability at least 1−ε from c·S·∏M_d queries. The error splits as bank events ≤ ε/9,
  caps ≤ ε/9, rank ≤ ε/3 and approximation ≤ ε/3, a total of 8ε/9.
  The arity satisfies M_d ≤ g_d(1 + 2lnκ_d/ln(p/κ_d)) + 3ln(8/τ_d)/ln(p/κ_d) + 3. The classical time is at most
  Q·(2 + 2B ln2·max κ_d^{g_d})·poly(max M_d, B, c, log p), plus Q times one Schedule 1 call when
  p ≤ c+1. At fixed c this is 2^{O(max g_d log κ_d)}·poly(m, log p, log 1/ε).
- **`prop:rc-lower`** (§F.9). Proved as stated, with one exception: the last clause ("the free-coordinate sampler meets this within the factor 4B ln 2") holds only outside the bank event β(M, n_0; a) of (i). The smallest failing instance is p = 5, κ = 2, a = 1, M = 2, R = [1 2]. That bank is generic, but −2x ∈ {3, 2} ⊄ D = {0, 1, 4} for both x ∈ P_2 = {1, 4}, so every trial is rejected; there β ≥ 1 for every n_0. The appendix states this restriction, and §6(e) gives the wording fix. The pivot-pattern failure is in fact at most 1/(p−1).

Proof structure: the RREF law (`lem:fc-rref`), a second moment over proportional classes
(`lem:fc-moment`) and one node (`lem:fc-node`). Everything after the node reuses Appendix B by
`\ref`: Lemmas `lem:s3-law`, `lem:s3-root`, `lem:s3-node`(c)(d) argument, `lem:s3-tree`, eqs
`s3-bezout`, `s3-nodes`, `s3-ninstr`, Prop `prop:s3-uniform`, and the restart proof of
`thm:random-column`(ii).

## 2. Rechecks (folder `2026-11-02-rees-free-coordinate-appendix/`)

```bash
cd research/audits/reviews/2026-11-02-rees-free-coordinate-appendix && nice -n 10 /opt/anaconda3/bin/python -B -u ../2026-11-02-rees-schedule3-cost/fcs_budget.py > fcs_budget_rerun.txt
cd research/audits/reviews/2026-11-02-rees-free-coordinate-appendix && nice -n 10 /opt/anaconda3/bin/python -I -B -u fc_appendix_check.py > fc_appendix_check_out.txt
```

- `fcs_budget_rerun.txt` took 17 s and is identical to `../2026-11-02-rees-schedule3-cost/fcs_budget_out.txt`
  (`diff` empty).
- `fc_appendix_check.py` is independent code that imports nothing from the report. It is exact
  (Fractions; ln 2 only through rational bounds) and took about 5 minutes niced. It ends with
  `ALL CHECKS PASSED`.
  - [1] The part (ii) inequalities for u = 2..120. The β bound for u = 2..30, at every κ ≤ u
    dividing p−1 and every a ≤ u−1, at three primes per u.
  - [2] The class-nine table. With the least arities: p = 11: 42.3 / 28.3 / 47.0; 1031: 36.6 / 33.4 /
    50.8; 5281: 39.1 / 33.8 / 52.2; 2^31−1: 35.9 / 31.0 / 49.8; 2^61−1: 34.1 / 33.5 / 51.0;
    2^127−1: 34.0 / 31.0 / 49.5. These equal the table, so its (iii) columns are confirmed. The
    explicit choice raises each FCS arity by 1–2 columns and log₂Q by 0.2–1.3, with the same maximal cap of 33.8.
    At all six primes no grade uses Schedule 2 or Γ_0.
  - [3] Lemma `lem:fc-moment`: exact mean and variance h^{n+1}(q^r−q^{2r}), plus the Chebyshev and
    oblivious identities, in six cases.
  - [4] Exhaustive bank enumeration in six cases. C is exactly uniform given (r, π) for every pattern.
    The bad fraction is at most β; the one case with β < 1 is (13, 2, 1, 4, 3), with 0.0845 against 0.283.
    The generic-pattern failure is at most 1/(p−1), and the uniform-kernel mean equals (q^n − p^{−n})q^a.
    The report's own Part B covers further cases with β < 1.
- **Test compile.** The scratchpad copy of `main.tex`, `numbers.tex`, `references.bib` and all
  `appendix-*.tex` got `\input{appendix-free-coordinate}` after `\ReesAppendix{appendix-codimension}`,
  then `latexmk -pdf`, rerun after the referee fixes. Result: exit 0, 102 pages, no undefined or multiply defined references,
  no overfull boxes, no `??` in the appendix text. The only three underfull boxes are in `main.bbl`
  (bibliography), not in the new file. The new file uses only main.tex macros (`\Fp`, `\eps`,
  `\poly`, `\rank`, `\hh`, `\GL`, `\file`).

## 3. Where the stated theorem text and the proof differ

Items 1–6 are text fixes, not failures. Item 7 is the one statement that is false as worded.

1. **(iii) explicit vs least arity.** The statement says "take … n_0 = … and M_d = …". The
   table uses the least public pair, so as written the table is not computed by the theorem's rule.
   The appendix proves the general rule (R1), so both are covered. See the wording fix in §6(c).
2. **(iii) classical time.** "2^{O(max g_d log κ_d)}·poly(m, log p, log 1/ε)" holds only **at
   fixed c**. Q = c·S·∏M_d is itself only polynomial at fixed c. Add "for fixed c".
3. **`tab:main-regimes`, free-coordinate row.** "(g_d log κ_d + log(1/ε))" should read
   "(g_d log κ_d + log(1/τ_d))". τ_d = ε/(9(c−1)S n_d) also carries S and n_d.
4. **(ii) rank guard.** "Each node uses at most 2B ln2·u^{u−1}+1 trials" holds on every bank of
   the ideal support. The appendix adds Appendix B's guard ("abort if the observed rank exceeds u−1")
   so that it holds on every record. Suggest stating that guard in (ii), as `thm:random-column` does.
5. **Error split of (iii).** The body's status paragraph cites the report's split, which includes
   Schedule 2 at ε/9. Under (iii) as stated, **no Schedule 2 node and no Bezout-lifted Schedule 1
   node occur**. Grades with κ_d = p−1 have d = p−1, and the combined rule then takes Schedule 1 at
   degree d. So (iii) inherits only the steps behind Theorem `thm:main` plus the label law, not
   Schedule 2 or the Bezout lift. The report's script can also take Rule W's arity where smaller,
   which means Schedule 2 at grade 9 for p = 105019. That variant needs `thm:power-sde`(ii) as an
   extra hypothesis. It is not used at the table's six primes.
6. **`prop:rc-lower`.** "fails with probability at most 1/(p−1) + 2p^{a−M}" is true, but the proof gives 1/(p−1).
   No change is needed. "On almost every bank" means outside an event of probability 1/s + 1/(p−1),
   where s ≥ 1 is free.
7. **`prop:rc-lower`, last clause (false as worded; the independent referee found it).** It needs
   "outside the bank event β of Theorem `thm:free-coordinate`(i)". The counterexample is in §1.
   My first draft of the appendix had the same error, and it is fixed there.
8. **Preamble scope.** "Assume the labels … and κ_d < p−1" should be read as concerning sampler
   nodes only. Part (iii) allows grades with κ_d = p−1 and derives the label law (Lemma
   `lem:fc-forest`(a)). The appendix says so in the proof of (i). Suggested wording: "Assume the
   labels at a stage-d sampler node …".
9. **Computability of T_r and n_0.** The appendix notes that T_r is computable (its argument
   is irrational) and that any integer above it works. It also notes that n_0 and the ceiling of
   log_p have exact integer forms. No change to the statement is needed.

## 4. Still missing

- Human review of Appendix F, and of Appendix B, which it reuses.
- The **block-splitting sentence** after `prop:rc-lower` ("Splitting the public coordinates … keeps
  the label law at each level … about κ^{g_d/k} at arity ∏_j M_j") is still proved only in the report
  (Lemma 5.2, Prop 5.3), not in any appendix.
- A polynomial-time sampler, and any adaptive method below κ^a at arity a+O(1) (open). The zero-sum
  grade κ_d = p−1, where (iii) falls back on Schedule 1.
- A JSON artifact and `make_numbers.py` support for `tab:fcs-budget`. Its numbers stay literal.
- The derived-dimension and codimension corollaries restated at every prime via (iii). Not done.

## 5. Claim gates that must stay false

Everything in `research/registry/conjectures.json` and every `claim_gates` block stays false. In particular:
- `research/reductions/random_column_rees.json`: `proof_promotion`, `candidate_promotion`,
  `fixed_bank_success_guaranteed`, `joint_source_law_verified`, `intrinsic_rank_promise_verified`,
  `observed_bank_rank_certifies_intrinsic_rank`, `quantum_receiver_implemented`,
  `native_application_established`, `novelty_established`.
- `research/reductions/rees_hsp_reduction.json`: `independent_review`, `novelty_established`,
  `speedup_claim_allowed`, `coherent_receiver_implemented`, `general_sde_implemented`.
- Also implicit in this work: polynomial-time Schedule 3, worst-case (law-free) small arity, and any
  human-reviewed status. This session flips nothing.

## 6. Proposed paper text (for the integrator; not applied)

**(a) Include the appendix.** In `main.tex`, after `\ReesAppendix{appendix-codimension}`:

```latex
\ReesAppendix{appendix-free-coordinate}
```

**(b) Theorem title of `thm:free-coordinate`:**

```latex
\begin{theorem}[Free-coordinate random-column schedule; conditional on the label law, proof in Appendix~\ref{app:free-coordinate}]
```

**(c) Part (iii), two phrases.**
- Replace "take $\tau_d = \eps/(9(c-1)Sn_d)$, $n_0 = 1 + \lceil \dots\rceil$ and $M_d = n_0 + g_d + \lceil\log_p(2/\tau_d)\rceil$, so that $\beta \le \tau_d$" with:
  "take $\tau_d = \eps/(9(c-1)Sn_d)$ and any public $M_d \ge n_0 \ge 1$ with $\beta \le \tau_d$ at $a = g_d$, for example $n_0 = 1 + \lceil (g_d\log(1/q) + \log(8/\tau_d))/\log h\rceil$ and $M_d = n_0 + g_d + \lceil\log_p(2/\tau_d)\rceil$ (Table~\ref{tab:fcs-budget} uses the least such $M_d$)".
- Replace "and the classical time is" with "and, for fixed $c$, the classical time is".

**(d) Status paragraph after the theorem.** Replace the whole paragraph ("The proof (\file{…}, Sections~3--5) is … class-nine profile.") with:

```latex
Appendix~\ref{app:free-coordinate} proves all three parts; the proof is checked by AI sessions only, pending human review. It is a second-moment argument on the reduced row echelon form. Conditional on the rank and the pivot pattern, the entries of $R$ in the columns after the last pivot are independent and uniform. For $x \in P_\kappa^{n'}$ the vectors $-R_{\cdot,F'}x$ are pairwise independent unless proportional, and proportional ones are accepted together. Part~(ii) reuses the tree and restart argument of Appendix~\ref{app:schedule3}. Part~(iii) uses one union bound in place of tree restarts. It uses no Schedule~2 node and no Bezout lift, because a grade with $\kappa_d = p-1$ has $d = p-1$ and uses Schedule~1 at degree $d$. The derivation is \file{research/audits/reviews/2026-11-02-rees-schedule3-cost.md}, and exact finite checks are in that report's folder and in \file{research/audits/reviews/2026-11-02-rees-free-coordinate-appendix/}. The probability bound concerns an independent bank, not every fixed matrix. Table~\ref{tab:fcs-budget} gives the resulting counts on the class-nine profile, with at most $2^{33.8}$ classical trials per node.
```

**(e) `prop:rc-lower`.** Title: `[Rejection cost; AI-checked only, proof in Appendix~\ref{app:free-coordinate}]`.
Last clause: replace "and the free-coordinate sampler meets this within the factor $4B\ln 2$" with
"and, outside the bank event $\beta$ of Theorem~\ref{thm:free-coordinate}(i), the free-coordinate sampler meets this within the factor $4B\ln 2$".

**(f) Block-splitting sentence after `prop:rc-lower`:** append "(\file{research/audits/reviews/2026-11-02-rees-schedule3-cost.md}, Lemma~5.2 and Proposition~5.3; not proved in the appendices)".

**(g) `tab:main-regimes` free-coordinate row:** replace `\log(1/\eps)` by `\log(1/\tau_d)`.

**(h) K7, merging the two theorems: possible now; owner's or integrator's choice.**

Option M (merge) needs two `\label`s on one theorem. LaTeX resolves both to the same number, so all
existing references stay valid.
1. Delete the `thm:random-column` theorem environment. Move its status paragraph's
   withdrawn-version sentences to after the merged theorem.
2. Put `\label{thm:random-column}\label{thm:free-coordinate}` on the free-coordinate theorem, titled
   `[Random-column schedule; conditional on the label law, proof in Appendix~\ref{app:free-coordinate}]`.
3. Add a remark for the old sampler:
   ```latex
   \begin{remark}[Uniform-kernel sampler]\label{rem:uniform-kernel}
   If each node instead samples uniform kernel vectors of its label matrix and rejects zero and every vector with an entry outside $D$ (step~(N3) of Appendix~\ref{app:schedule3}), part~(ii) holds with the same arity and tree budget and $4\kappa_d^MB$ trials per node: outside a bank event of probability at most $4/\mu + 2p^{a_d-M}$, with $\mu = ((h+1)^M-1)/(h\,p^{a_d}) \ge 2^{8u+1}u^{2u+1}$, each sample is accepted with probability at least $1/(4\kappa_d^M)$. Appendix~\ref{app:schedule3} proves this. By Proposition~\ref{prop:rc-lower} about $\kappa_d^M$ trials are also necessary for that sampler, about $2^{128}$ on the class-nine profile.
   \end{remark}
   ```
4. In Appendix B, change its title and opening sentence from "Theorem~\ref{thm:random-column}" to
   "Remark~\ref{rem:uniform-kernel}". Its other `\ref{thm:random-column}` uses refer to the
   hypotheses of part (ii), which are unchanged.
5. Merge the two Random-column rows of `tab:main-regimes` into the free-coordinate row.
6. Rewrite the last sentences of Remark `rem:combined-schedule` to say "part~(iii) of
   Theorem~\ref{thm:random-column}".

Downstream statements need no change. They all use part (ii), with identical hypotheses (u, c ≤ u,
a_d ≤ u−1, p ≥ 16u², M = 4u) and the identical cost form 2^{O(u log(u+2))}·poly.

Option K (keep both): apply (a)–(g) only. K7 is then closed as "both theorems proved, in Appendices B
and F".

I recommend Option M once Appendix F has been read. It removes a theorem whose sampler is known to
need about 2^128 trials per node, and it keeps all references.
