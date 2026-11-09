# Rees paper: Schedule 3 integration (K7 merge and zero-sum results), 2026-11-05

**Status: done. AI-checked, pending human review. Nothing committed; no git state changed;
no network; `research/reductions/rees_hsp_reduction.json` untouched; `make_numbers.py` not
run.** Written by the Schedule 3 integrator (exclusive owner of the Schedule 3 text in
`main.tex`, `appendix-schedule3.tex`, `appendix-free-coordinate.tex`,
`appendix-codimension.tex`, and of new `references.bib` entries for this pass).
Integration-log rows: I195–I201 (see the end of this note).

Backups of every file touched, taken before the first edit:
`/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/bak-s3/`
(`main.tex`, the three appendices, `references.bib`, `core/main-core.tex`,
`REES_FULL_CONTINUATION.md`, the integration log). All edits were exact-string replacements,
each asserted to match once, on a fresh read. Another integrator edited other parts of
`main.tex` during the pass (`rem:is-runtime`, `prop:triangular-sde`); those edits are intact (log rows I192–I194).

## 1. Task A: the K7 merge

### 1.1 Design

The owner's decision is to merge `thm:random-column` (uniform-kernel sampler, proved in
Appendix B) and `thm:free-coordinate` (free-coordinate sampler, proved in Appendix C).

**One theorem, label `thm:free-coordinate`, title "Random-column schedule (Schedule 3)".**
Its parts (i)–(iii) are the old free-coordinate parts, **word for word** (the edit script
asserted that (i) and (iii) are byte-identical to the old ones). Part (ii) gains the old
random-column example of a public bound ("for example g_d ≤ u−1, or … a promise on codim h")
and the definition of w. The old random-column theorem becomes **part (iv), "Uniform-kernel
sampler"**: under the hypotheses of part (ii) (n_0 unused), with the uniform-kernel sampler at
every node, it states the old (i) verbatim (μ, the bank event 4/μ + 2p^{a_d−M}, acceptance
1/(4κ_d^M), 4κ_d^M B trials, caps) and the old (ii) by reference to (ii)'s B, 4m' trees and
error split, which are identical to the old ones.

Why this shape:
- Parts (i)–(iii) keep their numbers, so the ~25 existing `\ref{thm:free-coordinate}(i/ii/iii)`
  are unchanged and still point to identical content.
- The label `thm:random-column` was **deleted**, not aliased. An alias would have silently
  turned "Theorem random-column(i)" (the uniform-kernel node) into the free-coordinate node
  bound (i). Deleting it made every stale reference an undefined-reference build error; the
  final build has none, and `grep thm:random-column` over the built `.tex` files returns 0.
- Proofs stay attached to their content: Appendix B is now "Proof of Schedule 3 with the
  Uniform-Kernel Sampler (Theorem 4.13(iv))" and its proof environment is "Proof of Theorem
  4.13(iv)". Appendix C is "Proof of the Free-Coordinate Schedule (Theorem 4.13(i)–(iii))".
- No circularity. Appendix C's proof of (ii) reuses "the proof of part (iv) in Appendix B, from
  'For the trees of part (iv)' to its end" (that phrase is now in Appendix B). Appendix B's
  proof of (iv) uses nothing from Appendix C. (Only `prop:mixed-schedule`, which is not part of
  (iv), cites `lem:fc-forest`(a), as before.)
- The merged preamble adds: "Every part also holds for coset-copy input, with c fresh copies of
  ρ_H in place of the c oracle queries of each lifted source (Lemma copy-lift)". This is A4
  below for (iii). For (ii) and (iv) it was already proved: Appendix B's `lem:s3-tree`(a) proof
  names Lemma copy-lift for the leaves.
- The intro paragraph "Schedule 3: random-column kernel rejection" now defines κ, h, P_κ, D and
  q once. It describes the common node (find y ∈ D^M in the kernel, then roots, Bezout, exact
  check), fair-bit sampling (the definition moved out of the old (i)), and then the two
  samplers. The two old status paragraphs are merged into one. It keeps: the label law is
  derived, not assumed; i.i.d. supply only; independent bank, not fixed matrix; the rank-guard
  abort; the RREF second-moment sketch; (iii) does not use Thm power-sde(ii); the withdrawn
  dg_d+2 version. The K7 sentence is now "Part (ii) has the hypotheses and conclusion of part
  (iv), with at most 2B ln2·u^{u−1}+1 trials per node in place of 4κ_d^M B, and it supersedes
  that trial count. Part (iv) is kept because Proposition mixed-schedule, Tables fcs-budget and
  random-column-budget and Proposition app-codim-rc use its node."

Rendered (combined build, §4): Theorem 4.13 on p. 30, Appendix B on p. 75, Appendix C on p. 86,
Remark C.8 (`rem:fc-zero-sum-sis`) on p. 94.

### 1.2 Reference table (every old reference, its new target, and why it still matches)

"Hyp." means hypotheses. FC(x) = `Theorem~\ref{thm:free-coordinate}(x)`.

| # | File: place | Old reference | New target | Why the hypotheses and conclusion still match |
|---|---|---|---|---|
| 1 | main: Contributions list | Thms power-sde(ii), random-column and free-coordinate | Thms power-sde(ii) and FC | The list names both samplers, and both are now parts of FC. |
| 2 | main: abstract | "(proved for oracle input, argued for coset copies)" | "(for oracle input and for coset copies)" | A4 (§2.7) proves the coset-copy case of FC(iii), which Cor fpt-r(i) uses. |
| 3 | main: `tab:main-regimes`, Random column row | "kernel rejection (Thm random-column)" | "uniform-kernel rejection (FC(iv))" | The row's conditions (p ≥ 16u², u ≥ c, u > max a_d) and (4u)^{c−1} leaves per tree are exactly FC(iv), i.e. FC(ii)'s hypotheses. |
| 4 | main: same table, free-coordinate row | "(Thm free-coordinate)" | "(FC(i)–(iii))" | Same content. It is made specific because (iv) is now in the same theorem. |
| 5 | main: same table, coset-copy row | "extending Thm fc … is argued, not proved" | "Thm fc included, by Lemma copy-lift at its leaves" | A4; the preamble of the merged theorem. |
| 6 | main: notation, h | Thm random-column | FC(iv) | h = (p−1)/κ_d is defined in the intro paragraph and used in (iv)'s μ. |
| 7 | main: notation, u | Thm random-column | FC(ii), (iv) | u's conditions (u ≥ 2, c ≤ u, a_d ≤ u−1, p ≥ 16u²) are stated in (ii), and (iv) assumes them. |
| 8 | main: notation, B | random-column(i); free-coordinate(iii) | FC(i)–(iv) | B appears as the cap exponent in all four parts. |
| 9 | main: §4 recursion, before the proof of Thm main | "Schedule 3 uses its own split (random-column(ii))" | "its own splits (FC(ii)–(iv))" | (ii) and (iv) use the restart split and (iii) the union-bound split; each is stated in its part. |
| 10 | main: `rem:combined-schedule` | "uniform-kernel nodes of random-column(i)" | "uniform-kernel nodes of FC(iv)" | FC(iv) states the node bounds of old (i) verbatim. The remark (and prop:mixed-schedule) uses that node with its own u_d, as before. |
| 11 | main: `rem:combined-schedule` | "the tree restarts of random-column(ii)" | "the tree restarts of FC(ii) and (iv)" | The restart scheme (4m' trees, keep the first m') is stated in (ii) and inherited by (iv). Identical to old (ii). |
| 12 | main: Schedule 3 intro paragraph | "uniform-kernel sampler of Thm random-column needs about κ^M trials"; "for Theorem random-column(ii) itself at u = 18" | "for part (iv) of the theorem below at u = 18" | The 2^{223.8}–2^{236.0} trial caps are the 4κ_d^M B count of old (ii), which is now (iv). |
| 13 | main: old status paragraph | "Part (ii) has the hyp. and conclusion of random-column(ii) … random-column is kept because …" | "Part (ii) has the hyp. and conclusion of part (iv) … Part (iv) is kept because …" | The same statement, inside one theorem. |
| 14 | main: `tab:random-column-budget` caption | "Random-column schedule (Theorem random-column; random_column_rees.json)" | "… with the uniform-kernel sampler (FC(iv); …)" | The artifact was generated for the uniform-kernel schedule. M = 4u, the leaves, tree attempts and query caps are those of (iv). |
| 15 | main: `tab:fcs-budget` caption | "the nodes of Theorem random-column(i), with u_d = …" | "the uniform-kernel nodes of FC(iv), with u_d = …" | As for #10. |
| 16 | main: after Cor fpt-r | "earlier proof used Thm random-column for p ≥ 16(r+1)²" | "used the uniform-kernel sampler of FC(iv) (or part (ii))" | Appendix B's "Application to Cor fpt-r" uses (iv) with u = r+1. (ii) has the same hypotheses and conclusion. |
| 17 | main: `cor:codim`(ii) | "or alternatively on Theorem random-column" | "or alternatively on FC(ii) or (iv)" | The route is `prop:app-codim-rc`, which needs the old (ii) with u = 2k. FC(iv) is that statement, and FC(ii) has the same hypotheses and conclusion. |
| 18 | main: proof of `cor:codim` | "Theorem random-column with u = 2k and M = 8k covers p ≥ 64k²" | "FC(iv), or its part (ii), with u = 2k and M = 8k" | Same as #17. |
| 19 | main: Formal boundary | "arity bounds of Schedules 1–3 (Thms power-sde and random-column, …)" | "(Thms power-sde and FC, …)" | Both Schedule 3 arity statements are now in FC. |
| 20 | App B: header comment and section title | "(Theorem random-column)" | "with the Uniform-Kernel Sampler (FC(iv))" | Appendix B proves exactly (iv): the node lemmas, the tree, the restarts and the error split. |
| 21 | App B: intro | "proves both parts of Thm random-column" | "proves part (iv) of FC … Appendix C proves (i)–(iii) and reuses the tree, restart and error-split argument below for (ii)" | Same content. The forward pointer replaces K23's worry about the proof attaching to its own theorem. |
| 22 | App B: setting | "The parameters are as in the theorem" | "those of part (iv), that is, of its part (ii) without n_0" | These are the old theorem's parameters. |
| 23 | App B: `lem:s3-mu`, `lem:s3-tree`(c), `prop:s3-uniform` | "Under the hyp. of Thm random-column" | "Under the hyp. of FC(iv)" | (iv)'s hypotheses are the old ones (u, c ≤ u, a_d ≤ u−1, p ≥ 16u², M = 4u). |
| 24 | App B: proof | "Proof of Thm random-column. Part (i) … For part (ii), …" | "Proof of FC(iv). Part (iv) is proved in two steps. Its node bounds … For the trees of part (iv), …" | The proof is unchanged except for these part names. |
| 25 | App B: `prop:s3-uniform`(c) proof | "the proof of random-column(ii)" | "the proof of FC(iv) above" | Same proof. |
| 26 | App B: Application to Cor fpt-r | "Theorem random-column applies" | "FC(iv) applies" | u = r+1 meets (iv)'s hypotheses, as before. |
| 27 | App B: `prop:mixed-schedule` and its proof | "as in the proof of random-column(ii)"; "the proof of random-column(ii) applies word for word" | "as in the proof of FC(iv) above"; "the tree part of the proof of FC(iv) above applies word for word" | The same restart argument. |
| 28 | App C: header comment, section title, intro | "full proof of Thm free-coordinate"; "proves all three parts" | "(i)–(iii)"; "(part (iv) is proved in Appendix B)" | The proof covers exactly (i)–(iii). |
| 29 | App C: Status (line ~36) | "as for Theorem random-column, it is derived below" | "as for part (iv) in Appendix B" | Same: the label law is derived in both appendices. |
| 30 | App C: intro (K23 spot, line ~38) | "the restart argument in the proof of Theorem random-column" | "… in the proof of part (iv) of FC in that appendix" | It points at a *different part's* proof, in Appendix B, which does not use (i)–(iii), so it does not point back at itself (the K23 concern). |
| 31 | App C: proof of (ii) | "The procedure is that of random-column(ii), with (F1)–(F6) in place of (N1)–(N6)"; "the proof of random-column(ii) in App B applies word for word, from 'For part (ii)' to its end" | "that of part (iv), …"; "the proof of part (iv) in App B …, from 'For the trees of part (iv)' to its end" | The quoted phrase was changed in Appendix B at the same time (#24), so the quotation is exact. |
| 32 | App C: §fc-numbers (K23 spot, line ~291, now ~311) | "for Theorem random-column(ii) itself at u = 18" | "for the uniform-kernel sampler of FC(iv) at u = 18" | 2^{193.9}–2^{236.0} is the 4κ^M B cap of (iv). |
| 33 | App F (codim): `thm:app-codim`(ii) and Status | "or alternatively on Thm random-column" (twice) | "or alternatively on FC(iv) or (ii)"; "on FC(iv) (or its part (ii))" | As #17. |
| 34 | App F: before §codim-random-column | "using g_d instead of a_d in Thm random-column would lose the bound" | "in parts (ii) and (iv) of FC" | Both parts take the public bound on a_d. |
| 35 | App F: `prop:app-codim-rc` (title, body, proof) | "conditional on Thm random-column"; "Thm random-column with u = 2k, M = 8k applies"; "on which Thm random-column relies"; "random-column(ii) then gives" | FC(iv) throughout, plus one sentence: "Part (ii) of the same theorem has the same hyp. and conclusion, with fewer classical trials per node, and can be used in place of part (iv)." | The proof uses old (ii)'s hypotheses (u = 2k, c_J ≤ u, a_d ≤ u−1, p ≥ 16u²) and its conclusion (success probability, cost form, 4m'·(4u)^{c_J−1}·c_J queries). FC(iv) states all of them. |
| 36 | App F: example of class 5 at k = 3 | "and Theorem random-column cannot be applied … with u < 2k−1" | "parts (ii) and (iv) of FC cannot …" | Both need c ≤ u. |
| 37 | App F: Exact checks (K23 spot, line ~328) | "internal inequalities of Theorem random-column" | "of FC(iv)" | `section6_bounds.py` checks the μ bound and the 4κ^M B trial counts, which are (iv)'s. |
| 38 | main: `tab:query-crossover` caption (K23 spot) | none | none | **K23 is stale here.** The caption no longer cites either theorem. It cites only Rem query-separation and Prop classical-query. No change was needed. |
| 39 | `core/main-core.tex` | no `\ref` to either theorem (it has its own labels) | — | Its Schedule 3 prose stays true. Two consistency edits were made (row I198): the free-coordinate status ("conditional derivation … AI-checked only" → "proved in the full version's appendix on the free-coordinate sampler … AI-checked, pending human review; the full version states both samplers as one theorem"), and `appendix-free-coordinate.tex` was added to its file list. The core paper builds: 26 pp., 0 Overfull, no undefined references. |

Unchanged on purpose: all `\ref{thm:free-coordinate}(i)`, `(ii)`, `(iii)` (same content), and
`main-full-draft.tex` and `archive/` (old drafts, not built). Two comment-only mentions remain
outside the paper: `theorems/rees_fcs_budget.py` (docstrings name `thm:random-column(i)/(ii)`;
now FC(iv)/(ii)) and `research/AGENT_HANDOFF.md`. They are listed as a mechanical follow-up and
were not edited (out of scope).

## 2. Task B: verification of the zero-sum results

Tests: `cd research/audits/reviews/2026-11-04-rees-s3-zero-sum && nice -n 10
/opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider test_zs.py` → **10 passed**. `results.json` is byte-identical before and after; pytest does not rewrite it.

Each proof below was re-derived from the paper's lemmas, not from the report's prose.

### 2.1 Z1 (zero-sum node ⇔ average-case binary SIS): **TRUE**, with two wording corrections

*Node ⇒ solver.* L = ⊕_{j≤g} (filiform of class p−1, [e_{j,0},e_{j,i}] = e_{j,i+1}). It has
γ_k = span{e_{j,i} : i ≥ k} and class p−1 < p (needs p ≥ 3), with g_c = g and κ_c = p−1, so
c ∈ Γ_0. For H = 1 we get K_c = 0, and by `lem:s3-law` a grade-c bank (first stage, fresh
leaves) is uniform on F_p^{g×M}. Given the labels, each register is ρ_λ = |G|^{-1}Σ_z χ_λ(−z)R_z
(`lem:central` with H = K = 1). This equals (|Z|/|G|)·Π_λ, the maximally mixed state on
range Π_λ. That range meets the span of each Z-coset in exactly one line (Z acts regularly on a
coset, and Π_λ projects onto one isotypic line). So ρ_λ can be prepared from λ: a uniform
quotient address, the public section, and one Fourier state on Z. The report writes this as an
explicit mixture of pure states with χ_λ(+z). Whether the sign is right depends on the R_z
convention, so the paper text uses the sign-free description above. A simulator holding X
therefore reproduces the node's whole input exactly, and the node's exact check (F5) makes any
non-abort a nonzero x = 1_T ∈ {0,1}^M with Xx = 0. **Correction:** the run time is "the node's
time plus poly(M, g, p) for preparing the states", not "the same time".

*Solver ⇒ node.* Let W be the span of the first t labels. Pr[W ≠ V] ≤ (p^a−1)p^{−t}/(p−1)
(`lem:s3-moment`(d) on a uniform a×t matrix). On W = V, the map v ↦ v_P (entries at the
pivot set) is an isomorphism V → F_p^a. So the later coordinates are P'x_i, with P' = E_P
invertible and determined by the first block; they are uniform and independent of the first
block. A solution x gives Σ_i x_iλ_{t+i} = Σ_j (Yx)_j b_j = 0. The blocks are independent (i.i.d.
labels, independent coins), so k blocks abort with probability ≤ (δ + p^{g−t}/(p−1))^k. The
witness has s_i = 0 on the first t targets, which are consumed and discarded as
`prop:descent` allows, and the output is ρ_{H_{d−1}} by `lem:fc-zero-sum`(d). **Note:** "exact
two-way equivalence" means polynomial equivalence with the stated losses. A node built this way
can abort, so a tree that uses it must add its abort share, as for the variant after
`lem:fc-zero-sum`. The paper text says so.

### 2.2 Z2 (lattice consequence via MP13): **TRUE as an implication**; corollary wording corrected

MP13 Thm 1.1, read from the local author copy (`…/2026-11-02-rees-linear-arity/lit/mp13_LWsE.txt`,
line 105; Thm 3.8 at line 965), states: m = poly(n), β ≥ β_∞ ≥ 1, q ≥ β·n^δ; average-case SIS
with solutions ‖z‖₂ ≤ β, ‖z‖_∞ ≤ β_∞ is as hard as worst-case approximation within
γ = max{1, ββ_∞/q}·Õ(β√n). Thm 3.8 also requires that q have at most poly(n) divisors below β_∞,
which a prime q satisfies. With β = √M, β_∞ = 1, n = g and q = p, the condition q ≥ βn^δ is exactly
M ≤ p²g^{−2δ}, and ββ_∞/q ≤ g^{−δ} ≤ 1, so γ = Õ(√(Mg)). By Z1(i), a node with abort ≤ 1−1/poly
is an average-case solver with non-negligible success. The reduction is black-box, so a quantum
node gives a quantum lattice algorithm. Verified.

**Correction.** The report's summary and its proposed (c) say "the exponent of g in the arity
of every polynomial-time node must grow with p". That is not what follows. A node of arity
C g^e p² is not touched, because then M > p²g^{−2δ}. The correct consequence, which the report's
body states and the paper now states, is: no polynomial-time node has arity ≤ C g^e p^j at
every prime, with constants C, e and j < 2. Proof: on p ∈ [g^k, 2g^k], C g^e p^j ≤ p²g^{−2δ} once
k(2−j) > e + 2δ. The nonexistence is conditional on the standard assumption, as the report
says.

### 2.3 Z3 (scope): **conclusion TRUE; the report's stated reason is false in m**, so it was rewritten

True part: every arity of FC(iii) is ≥ 2 (M_d ≥ g_d + 1 at every node type,
`prop:fc-uniform`(b)), so Q ≥ 2^{c−1}, and at Γ_0, c = p−1.

**False part.** The proposed (d) says "the query count … is superpolynomial for every choice of
node" wherever (c) applies. Counterexample: g copies of the filiform algebra of class c = p−1
with p ≈ g^k, plus an abelian direct summand of dimension N = 2^{c²}. Then m ≈ 2^{c²}, every
g_d = g, every FCS arity is O(g + c log m), and Q ≤ cS·(C c³)^{c} = m^{o(1)}·S = poly(m). So
the count is polynomial in m while (c)'s hypotheses hold at the top grade.

Correct argument (now in the paper as part (d)): if Q is polynomial in m (at error 1/3), then
c − 1 ≤ O(log m), so p = O(log m). The reachable-sum zero-sum node of `lem:fc-zero-sum`(c) costs
M·p^{g_c}, which is poly(m) unless g_c log p ≠ O(log m). That forces g_c ≥ log m/log p ≥
p^{1−o(1)}, whereas (c) needs g_c ≤ p^{1/k} with k > 1. So (c) never applies where the zero-sum
node is an obstacle to a polynomial Schedule 3. In the counterexample, reachable sums cost
2^{g log p} ≤ 2^{o(c)}, which is poly(m). The open question Q_b (time and arity f(p)·poly(g)) is
correctly identified.

### 2.4 A1 (where the i.i.d. law enters): **TRUE**, one omission

E1–E3 and E5 match the proofs (`lem:homogeneous`/`lem:copy-lift`; `lem:s3-law`;
`lem:s3-tree`(a) and `lem:fc-forest`(a), via `prop:descent` pointwise, no label reuse, parents
measuring other registers; `lem:s3-hybrid`). E4 lists the bank bounds. It omits that
`prop:rc-lower`, `prop:fc-split` and `prop:mixed-schedule` also use the law. They are bank bounds
of the same kind, so the conclusion stands. It was not put into the paper.

### 2.5 A2 (the supply is produced exactly): **TRUE**, one slip

This is a restatement of what the paper already says (the law is derived, not an outside
resource). **Slip:** "the tight bank (each e_j repeated p−1 times, padded)" must be
*truncated*, a sub-bank of the tight bank. Padding with zero columns creates a zero-sum
singleton. The paper text does not use A2 except by name in the continuation note.

### 2.6 A3 (Fourier sampling gives the law exactly): **TRUE**

(2) e_λ = Σ_{π over λ} e_π, because central z acts as scalars and Σ_π e_π = 1. ρ_H = |G|^{-1}Σ_{h∈H}R_h
lies in R(C[G]), so it commutes with every P_π = R(e_π). Hence (λ, branch after forgetting π)
has exactly the law of `lem:central`. (3) With function values kept, the target is |aH⟩. L_a
commutes with every R_g, so Pr[λ | aH] = ⟨H|Π_λ|H⟩ and tr(Π_λ|aH⟩⟨aH|Π_λR_g) = Pr[λ]·tr(ρ_λR_g).
I checked separately that the output of `prop:descent` depends on its inputs **only** through
the per-target traces tr(σ_iR_g): the output entry is |Ḡ|^{-1}Π_i tr(σ_iR_{δ(σ(r)^{-1}σ(q))}) for
any product input, because the address is a uniform superposition. So the output is
ρ_{HZ/Z} for every record, even though |aH⟩ itself is not ρ_H. Verified.

### 2.7 A4 (coset-copy input for FC(iii)): **TRUE**

The proof of `lem:fc-forest`(a) uses the leaves only as "fresh lifted sources ρ_{H_c} in
product". `lem:copy-lift` makes ρ_{exp(ĥ)} exactly from c copies, which are independent of
everything by Def input-contract(iii). The proof of (iii) touches the oracle only in "P leaves
of c queries each". The leaf instrument (uniform address on G̃, c controlled right actions,
cleanup) has the same n single-coordinate transforms that q_max counts, and it is compiled by
`thm:uniform-compilation`(ii)–(iii). `lem:copy-lift` is already one of "the steps behind
Theorem main". Appendix B's `lem:s3-tree`(a) already names Lemma copy-lift, so (ii) and (iv)
were already covered. Cor fpt-r(i) and (ii) (zero-sum route) follow, because the vote evaluates
no oracle. The IMS route and Cor codim still need an ordinary oracle; that wording is unchanged.

### 2.8 A5 (used by P4, h = 2): **TRUE**

At h = 2, P_κ = {±1} and D = {0, ±1}. A grade with h = 2 has d = κ_d = (p−1)/2 (d < p,
(p−1)/2 | d, and d ≠ p−1), so p ≥ 5. Z1(a) works with g filiform algebras of class (p−1)/2 (and
H = 1). Z1(b) works with ternary solutions. Z2 works because ‖z‖₂ ≤ √M and ‖z‖_∞ = 1. Z3 works
with c ≥ (p−1)/2, and the FCS trial cap (≈ κ^{g}) plays the role of reachable sums. T8 checks
the digit set for primes up to 400.

Also re-derived: Z5 (no two-level contraction at κ = p−1 for p ≥ 5). Its table needs the
values z_j ≠ 1 for j ≥ 1 excluded; this is implicit in the report. With that, every z_j lies in a
set of size ≤ 2, so p−2 ≤ 2. The paper cites Appendix A for this, unchanged.

## 3. Per-edit table (report §6 proposals)

| Item | Where | Grade | Reason / change |
|---|---|---|---|
| P1 | App C, paragraph after `lem:fc-zero-sum`, last sentence | **Modified** | The forward pointer now reads "a node of this kind is average-case binary SIS, and why that question does not decide whether Schedule 3 is polynomial". It states the equivalence, not one direction. |
| P2 | App C, new `rem:fc-zero-sum-sis` | **Modified** | Placed at the end of §`app:fc-mixed` (after the proof of (iii) and its split note), not between the zero-sum paragraph and `lem:fc-forest`, so the proof chain of (iii) stays contiguous. (a): sign-free description of ρ_λ, and "+poly(M,g,p) preparation" instead of "same time". (b): explicit abort bound (δ + p^{g−t}/(p−1))^k, and the requirement to add the abort share. (c): explicit hypotheses (M ≤ min(p²g^{−2δ}, poly g), abort ≤ 1−1/poly, p ∈ [g^k, 2g^k]) and the standard assumption named. The false "in particular the exponent of g must grow" is replaced by the j < 2 statement (§2.2). (d): rewritten (§2.3); "superpolynomial for every choice of node" was false. Added: the h = 2 ternary extension (A5, needed by P4). Kept: the p = 3 vs p ≥ 5 contraction sentence and the NEEDS HUMAN VERIFICATION comment on MP13's numbering. Label: "AI-checked, pending human review". |
| P2-bib | `references.bib` `MicciancioPeikert2013` | **Applied, flagged** | Authors, title and Thm 1.1 were confirmed from the local author copy (13 Feb 2013). The venue (CRYPTO 2013, LNCS 8042, pp. 21–39, Springer) is from memory and **not confirmed offline**, so the entry carries a `% NEEDS HUMAN VERIFICATION` comment. No DOI was added. |
| P3 | App C, Scope paragraph | **Modified** | "a node there that runs in time polynomial uniformly in p would solve average-case binary SIS modulo p in polynomial time (Remark …)". The report's sentence did not say "in polynomial time". |
| P4 | main, after "… κ^{a−Ω(a)} at arity a + O(1) is open." | **Modified** | The report's "for p ≥ g_d^{1+2δ}" is not the hypothesis of (c). The sentence now states the hypotheses: "a polynomial-time method at arity at most p²g_d^{−2δ} on primes p = Θ(g_d^k), for constants k > 1 and δ > 0, would approximate worst-case lattice problems in dimension g_d within polynomial factors". It adds "in both directions" and the AI-checked label. |
| P5a | `cor:fpt-r`(i) statement | **Modified** | "or, for coset-copy input, from as many copies of ρ_H". The wording was adjusted to avoid an Overfull line. |
| P5b | `cor:fpt-r`(ii) statement | **Modified** | "…at the grade d = c, also for coset-copy input." This is shorter than the report's parenthetical; same content. |
| P5c | proof of `cor:fpt-r`(i) | **Applied** (lightly reworded) | Replaces "since that theorem is stated for oracle input, this extension is argued rather than proved" with the A4 argument. |
| P5d | `tab:main-regimes`, coset-copy row | **Modified** | "(Thm fc included, by Lemma copy-lift at its leaves)" instead of "see the proof of Cor fpt-r", because the extension is now stated in the merged theorem itself. |
| P5e | IMS route of (ii) keeps "needs a coherent oracle" | **Applied** | No change made, as proposed. |
| P5+ (added) | merged theorem preamble; App C `lem:fc-forest`(a) proof and proof of (iii); abstract | **Added** | Without these, "proved" would rest on a corollary's proof. The theorem now states coset-copy input for every part, and App C's proof names Lemma copy-lift at the leaves and the copy count. The abstract's "(proved for oracle input, argued for coset copies)" became "(for oracle input and for coset copies)". |
| P6 | `REES_FULL_CONTINUATION.md` item 4, "Still open" | **Modified** | Z2 is restated with its real hypotheses, and MP13 numbering and bib are flagged. Z3 is restated as "can be polynomial only for p = O(log m), where that bound is silent" (not "any profile in that range already has 2^{c−1} queries"). Pointers to `rem:fc-zero-sum-sis` were added. The stale K7 "kept apart … owner's call" sentence in the same item was also replaced by the merge record. |
| Z4 (KMOSW nodes) | — | **Rejected for the paper** | Not proposed by the report for the paper, and it would need a human check of the KMOSW preprint. Only mentioned, as "unverified", in the continuation note. |

## 4. Build and tests

Build directory:
`/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/build-s3/`
(fresh copy of `*.tex` and `references.bib`), `PATH=/Library/TeX/texbin:$PATH latexmk -g -pdf
-interaction=nonstopmode main.tex`.

- My tree: exit 0, **151 pages** (baseline from the backups, same command: 149 pages, 0 Overfull).
- Rebuilt at the end from the current files, which include the other integrator's I193–I194
  (`build-s3b/`): exit 0, **152 pages**, 0 Overfull, 3 Underfull, no undefined, no Float too large;
  numbers test 2 passed.
- **0 Overfull** (two found in the first build were fixed by rewording: the cor:fpt-r(i)
  coset-copy clause and the first sentence of the App B proof). 3 Underfull, the same three
  as the baseline (`main.bbl` and `appendix-codimension.tex`).
- No "undefined", no "multiply defined", no "Float too large", no LaTeX warning, no `??` in the
  pdftotext output; BibTeX: 0 warnings; `MicciancioPeikert2013` is in `main.bbl`.
- 187 distinct `\ref`/`\eqref` targets and 43 distinct cited keys in `main.tex` + appendices,
  all resolved.
- `grep -c thm:random-column` over `main.tex` and all appendices: 0.
- No `\mathsf`, `\mathrel` or `\begingroup` added (counts equal to the backups').
- Core paper (`core/`, separate build dir `build-core/`): exit 0, 26 pages, 0 Overfull, no
  undefined references.
- `/opt/anaconda3/bin/python -m pytest -q tests/tools/test_rees_paper_numbers.py` (repo root):
  **2 passed**.
- Zero-sum tests: 10 passed (§2).

## 5. Gates, next question, follow-ups

Claim gates that must stay false, and do: "polynomial-time Schedule 3"; "efficient o(a²) SDE
solver exists"; "BIS_p/SIS_p hard for fixed p"; any novelty claim for Z2; human-reviewed
status. Every new statement carries "AI-checked, pending human review".

For the owner or a human reviewer:
1. MP13: confirm Theorem 1.1's numbering in the CRYPTO 2013 version, and LNCS 8042 /
   pp. 21–39.
2. The merged theorem is long (four parts, about one page). If wanted, part (iv) could move to
   a lemma in Appendix B, with the body pointing to it. Every reference above would then go to
   that lemma, and the content would not change.

Mechanical follow-ups (not done; out of scope): `theorems/rees_fcs_budget.py` docstrings
`thm:random-column(i)/(ii)` → `thm:free-coordinate(iv)/(ii)`. In `core/main-core.tex`, the
"Derived dimension" paragraph still describes only the old route (Schedule 3 for
p ≥ 16(r+1)², IMS below); it is still true, but the full version now proves Cor fpt-r for every
p > c through (iii).

## 6. Integration-log rows written

I195–I201, appended at the end of the last table of
`research/audits/reviews/2026-11-02-rees-integration-log.md`, each marked "Schedule 3
integrator".

Note for the log owner: the other integrator's rows I192–I194 were inserted between I136 and
I136's four continuation rows (`| | | |`). I did not move them.
