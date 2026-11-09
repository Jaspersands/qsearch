# Rees manuscript: candidate full draft, change log (item 11)

2 November 2026. AI session only (Claude Code). This is an editing pass, not a review: no
proof was re-derived here, and no claim changes status. Item 11 of
`research/REES_FULL_CAMPAIGN.md`.

- **Candidate copy:** `docs/papers/rees-hsp/main-full-draft.tex` (copied from `main.tex`
  as it stood on 2 Nov; `main.tex` was not touched). Diff:
  `git diff --no-index docs/papers/rees-hsp/main.tex docs/papers/rees-hsp/main-full-draft.tex`
  (after pass 2: 109 lines added, 47 changed or removed).
- **Sources applied:** the ranked text fixes of the six finished reports in this folder:
  core proof check §3 and §9 (`2026-11-01-rees-core-proof-check.md`), priority check §7–§8
  (`2026-11-01-rees-priority-check.md`), Cor fpt-r / ring-to-field §6 (and the optional §5
  table rows) (`2026-11-02-rees-fpt-torsion-check.md`), black-box "Ranked text fixes" and
  "Matching wording" (`2026-11-02-rees-black-box-check.md`), combined schedule §5 and §7
  (`2026-11-02-rees-combined-schedule.md`), and the small-prime §9 Schedule-2 hypothesis
  wording as a marked proposal (`2026-11-02-rees-small-prime-arity.md`). **Pass 2** (rows
  33–60): the listed `main.tex` text fixes of nine later campaign reports: `-a1-priority`,
  `-weil-threshold`, `-codimension`, `-subspace-source`, `-prime-power-compiler`,
  `-compilation-filters`, `-lean`, `-is-solver` and `-end-to-end`. Items 3 (dfs2) and 12
  (application) were still running and are left out.
- **Build check (exact):** `pdflatex` → `bibtex` → `pdflatex` ×2 on copies of
  `main-full-draft.tex`, `numbers.tex` and `references.bib` in the session scratchpad (no
  build products in the repo). Pass 1 result: 23 pages. **Pass 2 result:** 27 pages, exit 0
  (first pass with `-halt-on-error`), no `LaTeX Warning`, no undefined reference or citation,
  no overfull box (three arXiv-id and one math overflow were fixed; see row 60), `bibtex` 0
  warnings, and no `??` in the PDF text. A script compared all 43 distinct `\ref`/`\eqref`
  targets with the `\label`s (none missing) and all 12 cited keys with `references.bib` (none
  missing; pass 2 adds no `\cite` key, see B7). Table 1 was checked visually on page 6.

## Change log

"Old line" is the line in `main.tex`. Every row is **applied** in the copy unless the status
says otherwise. "Claim label kept" means the claim keeps its current label (proposed,
conditional, or AI-checked pending human review).

| # | Source (report §, fix) | Section / old line | Old text (summary) | New text (summary) | Status |
|---|---|---|---|---|---|
| 0 | none (editorial) | status box, after l. 80 | — | One sentence: this copy applies the fixes of six AI-only checks; change log path; "not a human review, and no claim changes status". | Applied; no claim affected |
| 1 | fpt-torsion §6.5 | abstract l. 92 | "an all-prime bound 2^{O(r log(r+2))}·poly in the derived dimension r" | "a bound … valid for every prime p > c with the class not fixed" | Applied; Cor stays conditional |
| 2 | priority §8; core §9.1 (and core §8.1 ruling 5a) | §1 Related work, l. 116 | Scope comparison; DHIS and IS Cor 8 together; II Thm 1 "bounded primes"; "None of these obviously contains…" | Adds ISS Thm 2 (classical reduction to exponent p, |H| ≤ p); separates IS Cor 8 (m growing) from DHIS (m constant); states that, if Thm main is correct, IS Cor 8/DHIS are special cases of its regime (p > class, Lazard via matrix log); grade-by-grade elimination is IS Thm 5 §5's mechanism transplanted through the Rees cover; only the cover for arbitrary H "may be new, and this has not been established"; II: conditional on zero-sum for larger primes, smooth order an open problem (§6), no near-preserving automorphisms beyond class two (§1); Morales "bounded generator rank" and "under an input assumption". Kept the free class-3 example and the input-model sentence. Ends "We found no result covering … our search was limited". | Applied (merged; see conflict C4); `novelty_established` untouched |
| 3 | core §3.1 (second half) | Def input-contract, l. 166 | "The Lazard correspondence makes h an F_p-linear Lie subalgebra" | Names the subgroup form (subgroups ↔ Lie subrings), plain-text pointer to Khukhro Thm 10.13, and "an additive subgroup of an F_p-space is a subspace". | Applied; needs bib entry (B1) |
| 4 | core §3.1 | Thm rees-cover proof (iii), l. 235 | "universal combination of brackets … denominators invertible mod p > c. Lie homomorphisms therefore commute with ∗." | Adds the group-law half: Dynkin denominators in Z[1/c!]; associativity, identity and inverse identities hold in the free class-c Lie algebra over Q, hence over Z[1/c!] (free module embedding), hence over F_p; Lazard 1954 and Khukhro Ch. 9–10 cited; then homomorphisms commute with ∗. | Applied; needs bib entry (B1) |
| 5 | core §3.4 | §3 setting, l. 319 | "G is any finite group …" | Adds: R is the right regular representation R_g|x⟩ = |xg⁻¹⟩, so tr R_g = |G|[g = 1]; the proofs use both. | Applied (clarity only) |
| 6 | core §3.2 (also §9.6) | §4.1, l. 367 | "On a uniform Q address register, apply …" | "Prepare the Q address register in the uniform superposition |Q|^{-1/2}Σ_q|q⟩ (not the maximally mixed state, which would give a diagonal output), and apply …" | Applied. Same ambiguity in `REES_HSP_REDUCTION.md:166` not fixed (not this item's file) |
| 7 | core §3.3 | after Prop descent, l. 382 | "fresh disjoint preparations supply independent inputs" | Adds (2d): conditioning on any classical event determined by the record (solver success, retries) leaves the kept outputs independent copies of ρ_{HZ/Z}. | Applied |
| 8 | core §9.5 (and §7.2) | §4.2 recursion, l. 400 | Readout returns h | Adds the one-line argument that K = ⟨exp b_i⟩ ≤ H has log K ⊇ h, so K = H. | Applied |
| 9 | core §9.4 (and §6.3) | budget bullets, l. 405–406 | Solver third and approximation third | Solver bullet: "Under Schedule 1 this share is zero … the third is unused." Approximation bullet: "in diamond norm"; trace distance is ½‖·‖₁, so operator-norm isometry error η gives trace distance ≤ η. | Applied |
| 10 | combined §7.1 | Schedule 1, l. 420 | "If d ∤ p−1 … the displayed d-bound remains sufficient." | Adds: B_{κ_d}(a) (or a+1 when κ_d = 1) is also sufficient and is the arity the reduced solver uses; the B_d counts are upper bounds, not exact counts. | Applied |
| 11 | priority §7 (text part) | Schedule 1, l. 420 | "(checked against arXiv:1503.09016v2)" | Adds: section, theorem and corollary numbers for IS refer to that arXiv version (the accepted journal version); FAW 2015 numbering not checked. | Applied; bib edits listed (B2) |
| 12 | core §9.2 (core §5.3) | Schedule 1, l. 420 | "The cleaner bound d^{d log d}(a+1)^{d log d} stated in its Theorem 3 is looser." | "The threshold printed in its Theorem 3 has (a+1)-exponent d log d, smaller than the exponent d⌈log₂(d+1)⌉ that this proof supports, and for large a it is not implied by the proof as written. We therefore use the proof's count." | Applied conservatively (conflict C1) |
| 13 | core §9.3; combined §5 caption / §6 | after Thm power-sde, l. 439 | "Part (ii) is a proposed corollary checked only by automated review" | "proposed corollary … checked in writing by an AI session, which found no gap and singled out the Weil-count step for human review (core check §5.4). No human has read it, so part (ii) stays conditional, and Thm main does not use it." | Applied; label kept conditional (conflict C3) |
| 14 | small-prime §9 (§0.3–0.4, §2–3) | after l. 439 (new paragraph) | — | "Proposal, not adopted (owner's decision)": replace p ≥ 16κ^{2κ+2} by p > T_W(κ) = ((A+√(A²+4κ^κ))/2)², A = (κ−2)κ^κ+1, or (p,κ) outside the listed exceptional sets for κ ≤ 5 (∅ for κ = 2, 3; κ = 4 and κ = 5 sets listed). Notes the decoupled contraction and no human/priority review. Theorem keeps its hypothesis. | **Superseded in pass 2 by row 34** (merged into a conditional proposition); theorem, remark and table unchanged |
| 15 | combined §7.2 (+ §0, §3.3, §7.5) | new Remark `rem:combined-schedule` after Schedule 2 | — | Rule W: per grade from public (p, d, g_d): linear (g_d+1) if κ_d = 1; Schedule 2 if κ_d ≥ 2 and p ≥ 16κ_d^{2κ_d+2}; else Schedule 1 at degree κ_d (B_{κ_d}(g_d)). Valid for every p > c and every H, no label law; AI-only check, conditional on the steps behind Thm main, on (ii) and on the Bezout lift; no human check. Most saving from the reduced degree; worst-case m-exponent unchanged for c ≤ 7, falls by two at c = 8, 9 (143 vs 145 at c = 9). | Applied; conditional. 143 is hard-coded (see N1) |
| 16 | combined §7.3 | same Remark | — | "The rule does not mix in Schedule 3"; Thm random-column (ii) assumes 4u columns at every grade, so a mixed tree needs a node-count-weighted bank bound. | Applied |
| 17 | fpt-torsion §6.7 | Thm random-column (ii), l. 449 | "poly(m, log p, log(1/ε))" | "poly(m, log p, w, log(1/ε)), where w is the oracle label width" | Applied |
| 18 | combined §5, §7.4 | Table `tab:main-regimes`, l. 184–196 | Rows: Fixed class (IS); Large field; … | Kept the Fixed-class (Schedule 1) row unchanged; Large-field sources cell adds "a factor g_d+1 when κ_d = 1"; **added** a "Fixed class c, combined (Rem.)" row with the report's §5 schedule and sources cells ("at most Π B_d(g_d)"). Caption: combined row is a public-data schedule choice and uses the two-level schedule, "checked only by AI sessions, not by a human"; combined row added to the conditional list. | Applied conservatively (conflict C2) |
| 19 | fpt-torsion §5 (optional rows) | Table, l. 195–196 | "random column / IMS fallback"; "ring-to-field" | Derived dim.: "all p > c, class not fixed"; "random column (p ≥ 16(r+1)²) / IMS Theorem 11 (p < 16(r+1)²)". Torsion rank: "socle core via Cor fpt-r, at most b normalizer rounds (Thm ring-to-field)". | Applied |
| 20 | black-box ranked 2; matching wording "Line 531" | §5.2, l. 531 | "The separate conditional black-box outer envelope is for groups with b-bit encodings … call cap b(b+1)" | Adds: the envelope is for the acquired-chart route (local dimensions ≤ b), e.g. (R2); it does not bound the free pullback (local dimension rank F_{s,c}, composition length e·d). Names the three recursions: b (whole-socle recursion, Thm ring-to-field (iii)), b(b+1)/2 (central-flag scan of the source note), b(b+1) (chain-pass scan, ≤ r+1 passes of ≤ r calls per Sylow of length r, summed). | Applied |
| 21 | fpt-torsion §6.5 | Cor fpt-r title, l. 540 | "All-prime bound in derived dimension; conditional" | "Bound in derived dimension for every prime p > c, class not fixed; conditional" | Applied |
| 22 | fpt-torsion §6.6 | Cor fpt-r proof, l. 546 | Large-p branch: "Theorem random-column gives the bound." | Adds: this branch inherits Thm random-column's use of the i.i.d. label law (AI-checked only), so the corollary is conditional for that reason too. | Applied |
| 23 | fpt-torsion §6.1 (§A3) | Cor fpt-r proof, l. 546 | IMS Thm 11: "time polynomial in the input size plus |G′|" | Cites "Theorem 11, Section 5" (arXiv numbering); arbitrary H; charges one reversible BCH evaluation poly(m, r, log p) per group-oracle call; amplifies IMS's fixed constant error by O(log 1/ε) runs, certifying H′ ≤ H via f(x) = f(1) on returned generators, computing |H′| by linear algebra, outputting the largest certified H′. | Applied |
| 24 | fpt-torsion §6.4 | §6.2 setup, l. 559 | "B the full input bit length, including the e_i log₂ p coordinate bits" | Adds the oracle label width to B; defines T_f and Q_f, with Q_f·T_f charged separately. | Applied (symbol renamed, C8) |
| 25 | fpt-torsion §6.4 | Thm ring-to-field (ii), l. 568 | time 2^{O(R log(R+2))}·poly(B, log 1/ε) | "…, plus Q_f·T_f" | Applied |
| 26 | fpt-torsion §6.2 | Thm ring-to-field (iii), l. 569 | "Each nontrivial step enlarges the known part of H, so there are at most b calls" | Two stop rules: no call on a trivial section; reject (and stop on) a returned subspace that is not a Lie subalgebra strictly containing the known part. Then ≤ b calls on every branch, plus Q_f·T_f; without the first rule H = G costs b+1. | Applied |
| 27 | fpt-torsion §6.8 | Thm ring-to-field proof, l. 574 | rank argument for a section S/K | Adds: every nested section is S/K with S a subring and K an ideal of S, so the rank bound covers all depths. | Applied |
| 28 | fpt-torsion §6.3 (and §6.4) | Quotient oracle, l. 577 | "This is the construction of the source note, Section 2." | "This quotient oracle is the construction of the source note, Section 2. The recursion of (iii), with full socle intersections in nested sections, is this paper's; the note's own central-flag scan uses up to b(b+1)/2 calls." Cost line adds HNF/SNF arithmetic, Q_f·T_f, one original query per local query. | Applied |
| 29 | black-box ranked 3, 7; matching wording "Sylow paragraph" | §7.1, l. 591 | "Decomposing G into Sylow subgroups, which needs |G| and its factorization …, reduces the problem to p-groups when every prime divisor of |G| exceeds c." | Needs only generator orders and their factorizations (order finding, factoring; preprocessing); |G| not needed; H = Π(H ∩ G_p); exponent of G_p = largest p-part of generator orders (regularity, class < p); primes p ≤ c by II Thm 1 given the subgroup-state unitary from f and its inverse, cost imported and not in the envelope; the proposition treats p > c. | Applied |
| 30 | black-box ranked 4, 5; matching wording (i) — **superseded in pass 2 by row 49** | Prop black-box (i), l. 597 | "The project's word compiler covers exponent p in general class, and prime-power exponents only for c ≤ 4" | Φ-evaluation cost O(d·W_c·e log p) with reversible cleanup, d = rank F_{s,c} ≤ Σ_{k≤c} s^k, W_c depending only on c; Z[1/c!] identities hold mod p^e for all c < p but compilers cover prime powers only for c ≤ 4 and p > 4; no mod-p^e compiler beyond; "a limit of the compilers' contracts, not a mathematical one". | Applied |
| 31 | black-box ranked 1, 6; matching wording (ii) | Prop black-box (ii), l. 598 | e = 1: tuple lift applies; e > 1: outer recursion with Thm main on each F_p section | e = 1: working dimension rank F_{s,c}, not log_p|G|; chart acquisition would reduce it. e > 1: conditional on Thm ring-to-field (iii), not Cor fpt-r; route (R1) outer recursion on F_{s,c} over Z/p^e with hidden Φ⁻¹(H), Thm main per F_p socle section, ≤ e·d local calls; route (R2) ker Φ by one abelian HSP on (F_{s,c},+) (zero f queries, poly(d, e log p, log 1/ε) Φ evaluations), Smith-form chart F_{s,c}/ker Φ ≅ log G, then Thm ring-to-field on G (≤ log_p|G| ≤ ℓ local calls of dimension ≤ ℓ). | Applied; e > 1 stays conditional |
| 32 | black-box ranked 1; matching wording (iii) | Prop black-box (iii), l. 599 | "The correct local object is Φ⁻¹(Ω_1(G)) = {x : px ∈ log ker Φ}, which needs the relation lattice of ker Φ." | "In general Φ(Ω_1(F_{s,c})) = ℧_{e−1}(G), which can be a proper subgroup of Ω_1(G). Neither route in (ii) restricts to Ω_1 of the cover and pushes forward. Where Ω_1(G) is wanted, Φ⁻¹(Ω_1(G)) = {x : px ∈ ker Φ} is computable from the abelian kernel computation of (ii)." Metacyclic example and the previous-version sentence kept. | Applied |

### Pass 2 rows

"Old line" is now the anchor text in the copy (pass-1 rows already moved the line numbers).

| # | Source (report §, fix) | Section / anchor | Old text (summary) | New text (summary) | Status |
|---|---|---|---|---|---|
| 33 | a1-priority §9.1, §5.3 | §1 Related work, after II "open problem [Section 6]" | — | II Prop 3 / §6: an average-case or randomized poly(np) zero-sum finder would give a non-exact algorithm for smooth order and bounded class; "If Thm main is correct, it gives a non-exact algorithm for explicit Lazard p-groups of fixed class c < p by a different route (scalar SDE weights)". | Applied; conditional on Thm main; no novelty claim |
| 34 | weil-threshold fixes 1–3; small-prime §9 (replaces row 14) | after Thm power-sde, in place of the row-14 proposal paragraph | "Proposal, not adopted" paragraph (T_W, exceptional sets for κ ≤ 5) | New **Proposition `prop:decoupled-sde` ("conditional, AI-checked only")**: for p ∉ E_2(κ), in particular κ ≥ 3 and p ≥ κ^{κ+1}, the decoupled contraction C_ij = z_i z_j(α_j+β_i) gives the arity (a+1)((κ−1)a+1); scalar cost O(κ^{κ+1} log κ)·poly(log p, k) for p ≥ T_S(κ) ≤ 10κ^{κ+1}, constant search below. A paragraph lists E_2(2..6), says κ ≥ 7 has only bounds, names both reports, notes that no human or priority review has been done, says that p ≥ c^{c+1} would cover κ_d ≥ 3, and states that the theorem, remark and table keep 16κ^{2κ+2} ("owner's decision"). | Applied as a separate conditional statement (C9); weil fix 4 not applied |
| 35 | a1-priority §9.1, §5.1 | Related work | — | Worst-case zero-sum length for fixed q improved to q^{q²}(n+1)^{q−1} "as stated in arXiv:2609.40321, Thm 1.11 (see also arXiv:2510.07515, §5.2); still exponential in q". | Applied; plain-text arXiv ids (B7) |
| 36 | a1-priority §9.4, §5.2 | Related work | — | II's zero-sum theorem used as a black box at non-constant class, hidden order p (arXiv:2609.34996). | Applied |
| 37 | a1-priority §9.2 | Related work, "do not exist in general beyond class two" | unqualified | Adds: the remark concerns automorphisms of G; the dilations here are automorphisms of the cover 𝒜, reached through E_s. | Applied |
| 38 | a1-priority §9.3, §8 | Related work, last sentence | "We found no result … our search was limited" | "We are not aware of a prior result …. Our search read the full texts of the papers citing arXiv:1503.09016 and arXiv:2304.08376 that Semantic Scholar and OpenAlex listed on 2 Nov 2026, plus topical searches. It has known gaps: Google Scholar lists more citations of the latter than we could obtain. … not exhaustive." | Applied |
| 39 | codimension §9 fix 2 | §1.3, "is withdrawn; see Remark rem:codim" | withdrawn, no replacement | Keeps the withdrawal; adds "A bound of the same form now follows instead, conditionally, from an abelian-ideal reduction (Corollary cor:codim)". | Applied |
| 40 | codimension §9 fix 1 | §6.1, `rem:codim` | Remark: earlier claim withdrawn, filiform example, pointer to the unaudited reduction note | New **Corollary `cor:codim` (Hidden codimension; conditional)**: k given, ordinary oracle, c < p not fixed; (i) every fixed k: poly(m, log p, w, log 1/ε); (ii) also conditional on Thm random-column: 2^{O(k log(k+2))}·poly time, 2^{O(k log(k+2))}·poly(m, w, log 1/ε) queries. Proof sketch as in the report (maximal abelian ideal, abelian HSP for K, normalizer, transported oracle through any section, terminal dim ≤ k(k+1)/2 and class ≤ 2k−1, Schedule 3 at u = 2k for p ≥ 64k², birthday learner below, k ≤ 2 via core). Status paragraph: AI-checked only; same conditional status as Cor fpt-r; a gap between upper bounds, not a separation; normalizer recursion as in ISS; priority not assessed. Remark `rem:codim` retitled "Why the direct descent cannot give the codimension bound", keeps the filiform example and adds that the reduction disposes of it in one abelian call (𝓘 = span(e_1..e_{m−1}) = N(h)). | Applied; conditional (C13) |
| 41 | codimension §9 fix 3 | Table `tab:main-regimes` | — | New row "Hidden codim. k | all p > c, oracle input | abelian-ideal reduction, then random column (p ≥ 64k²) / classical birthday (p < 64k²) | 2^{O(k log(k+2))}·poly total (Cor. cor:codim)". Caption: row added to the conditional list; "needs an ordinary oracle and a given k"; "last three rows". | Applied |
| 42 | subspace §fix 1 | §7.2 opening | — | "G = exp(L) explicit over F_p of class c < p, so of exponent p, as in Thm main; black-box and exponent-p^e groups are not covered." | Applied |
| 43 | subspace fix 2 | proof of Thm subspace-source (ii) | coupon-collector sentence only | Adds: p_k is state-independent, so attempts are a sum of independent geometric variables; rejection must apply the inverse LCU before discarding, which gives the Lüders complement preserving ∧^k V; without recovery the invariant fails at d = r = 3, k = 2. | Applied |
| 44 | subspace fix 3 | §7.2 after the theorem, "which is not reproduced here" | determinant step deferred to the note | Four-step composition (design with ℓ blocks and the address density σ; phase cancellation via Σ_s s^j = 0; separation and TD(σ, ρ) ≤ √(p^n)(1−γ)^ℓ/2; hybrid over B_leaf sources), the Heis(F_3), H = Z(G), r = 2 falsifier for the plain c-point lift, and new **Corollary `cor:subspace-hsp` (Flat subspace HSP; proposed, conditional)** with the report's access model and charged costs. Status paragraph: argued from proved lemmas, AI-checked with exact simulations, no human review; scope exclusions; no explicit family and no quantum backend known. The "Second, weak Schur sampling…" sentence now begins "Separately". | Applied; label "proposed, conditional" (C14) |
| 45 | subspace fix 4 | §7.2 budget paragraph | ranks, raw-copy bits, attempt caps | Adds hypothetical promises δ = 1/10, ε = 1/3; T ≈ 2^1592 exterior states; M = 14, ℓ = 420400, Mℓ = 5,885,600 per lifted source against c = 9; "sufficient bounds, not observed costs". `\SubQubits` is not used in the paper, so nothing to drop. | Applied; hard-coded numbers (N2) |
| 46 | subspace fix 5 | Table caption | — | Caption sentence: the flat-subspace source spends Mℓ exterior states per lifted source, each ≤ N+1 raw copies, instead of c copies (caption sentence, not a new row). | Applied |
| 47 | is-solver fix 1 | Schedule 1, "van de Woestijne's deterministic solver" | which equation unstated | "(over F_p this is z_1^d + ⋯ + z_{d+1}^d = 0, solved by writing −1 as a sum of at most d d-th powers; van de Woestijne, ISSAC 2005, §6)" | Applied; plain-text citation (B7) |
| 48 | is-solver fixes 2, 3 | Schedule 1, after the B_{κ_d} sentence (row 10) | — | The deterministic run needs only G(κ_d,a)^{⌈log₂ t⌉} columns (t ≤ κ_d+1). Artifact sentence: `theorems/rees_is_sde_solver.py` returns verified witnesses at κ_d ≤ 3 at full arity and at κ_d = 4 when the zero sum has two terms; larger κ_d exceed 10^8 columns at a = 1; "a classical solver only: the reduction does not call it, it has had no human review, and the general SDE step is not counted as implemented". | Applied (C10); `general_sde_implemented` stays false |
| 49 | prime-power-compiler fixes 1, 3 (replaces row 30's compiler sentences) | Prop black-box (i) | "Each evaluation of Φ costs O(d·W_c·e log p) … compilers … prime powers only for c ≤ 4 and p > 4 … limit of the contracts" | Certified inverse-BCH words are Z[1/c!] identities; evaluated with a/b ↦ ab⁻¹ mod p^e they compute Lazard addition and bracket for every class c < p and every e (free Z_(p) Lie ring; Lazard functoriality, Trappeniers arXiv:2406.02475 Thm 2.3). Explicit costs: precomputation ≤ (d−s)(m_[] + 2b_e q_[]), per evaluation ≤ d(2b_e + m_+ + 2b_e q_+), with b_e the bit length of p^e and m, q depending only on c; poly(s, e log p), no oracle query. AI-proved, exact checks at p = 7, 11, e = 2, 3, c = 5, 6 (GAP relatively free groups); circuit counted, not synthesized; the implemented compiler `theorems/universal_lazard_words.py` still works mod p, so its prime-power coverage stays c ≤ 4, p > 4 until changed. | Applied; class-≤4 limit dropped as a mathematical limit (C11) |
| 50 | compilation-filters fix 1 | Thm uniform-compilation (i) | "on 𝒜 … exactly (c−1)c(c+1)(c+2)/6 brackets … divisions by factorials up to c! … O(n³)" | Stage-d form on G_d: exactly (d−1)d(d+1)(d+2)/6 brackets of O(D_d³) operations, D_d = Σ_{k≤d} g_k, "in this unoptimized schedule"; at d = c the old count on 𝒜; divides only by integers with prime factors ≤ c. | Applied |
| 51 | compilation-filters fix 2 | proof of (i) | "terms of degree ≤ c have denominators with primes ≤ c" | Justified by the recurrence: coefficients B_j/j! of z/(1−e^{−z}) for j < c (von Staudt–Clausen) and division by k+1 ≤ c. | Applied |
| 52 | compilation-filters fixes 3, 5 | Thm uniform-compilation (ii) | Bennett uncited; merge primitive unstated | Bennett (IBM J. Res. Dev. 17, 1973) named in plain text; merge primitive = controlled right translation x ↦ x ∗ (−δ_s(σ(u))), identity on invalid words and s = 0 slots, same four passes; σ and δ_s public linear maps. | Applied (B7) |
| 53 | compilation-filters fixes 4, 5 | Thm uniform-compilation (iii) | "following Cleve and Watrous"; q_max undefined | Kitaev (arXiv:quant-ph/9511026, §5, Thm 2, eq. (25)) with finite-gate synthesis (e.g. arXiv:quant-ph/0505030), or log depth by the Cleve–Watrous sketch (arXiv:quant-ph/0006004, §7.1); Kitaev's precision 2(pε′)^{1/2} met with ε′ = η²/(4p); q_max = max(n, m, max_d(2M_d g_d + D_{d−1})). | Applied (C17; B7) |
| 54 | compilation-filters fix 6 | §8 intro, "which fails for N ≤ p < 2N−1" | "fails" | "The truncated series exp(ad_x) is defined, since ad_x^p = 0, but differs from conjugation exactly when N ≤ p ≤ 2N−2 (witness x = J_N, M = E_{N1})". | Applied |
| 55 | compilation-filters fix 7 | after Prop conjugation | — | Luks Thm 3.2(5) computes the stabilizer classically for every matrix p-group acting by conjugation, every N and p; the proposition is a self-contained linear-algebra form when G = exp(L), N ≤ p. | Applied |
| 56 | compilation-filters fixes 8, 9, 10 | Remark filters; closing paragraph | items (i)–(iii); item (ii) "linear unipotent action", "a fixed anchor", "needs p > max(D,(D−1)Δ)"; "factorization and Frobenius or gradient recognizers" | New item (0): explicit linear actions (Luks Thm 3.2(5),(7)), with (i)–(iii) for succinct superpolynomial representations. Item (ii): action of exp(L) with nilpotency index ≤ p (note uses UT_5 blocks, p > 5); "an anchor fixed by every group element"; "a moved anchor can give K = 1 while H ≠ 1"; "is proved under p > max(D,(D−1)Δ), a sufficient condition". Closing paragraph names the derivative/gradient attack (SUCCINCT_POLYNOMIAL_STABILIZER_AUDIT §3) and the gradient recognizer for the Moore-form family. | Applied |
| 57 | lean §1 (rebuild result) | §9.1 boundary paragraph | "On 31 October … lake build succeeded" | Adds: 2 Nov AI rebuild from source in a copy (Lean/Mathlib v4.35.0), no error, warning or sorry; guards mapped to modules; per-module counts and total 180 exact. | Applied; table unchanged (lean fix 4) |
| 58 | lean fix 1 (in the form allowed by the brief) | §9.1 "Inside and outside the boundary" | — | Five Lean files kept as review artifacts **outside `formal/`** (`research/audits/reviews/2026-11-02-rees-lean/`, 83 more guards): Lie-level cover facts in every class; conditional on a natural group-law hypothesis discharged in Lean only for c = 3, the general-class tuple criterion, quotient tower and per-step descent. "Not part of formal/ or of the 180 guards …, and the boundary stated here does not include them." | Applied (C12); lean fixes 2–3 not applied |
| 59 | end-to-end fixes 1, 2 | §3 after the finite control; §2.2 after the subalgebra counts | — | New paragraph "Exact end-to-end simulation" (artifact `theorems/rees_end_to_end_sim.py`: 4 groups, 32 subgroups, exact Z[ζ_p], i.i.d. labels, Chevalley–Warning arity κ_d g_d + 1, log H recovered every run; "a finite classical simulation of exponential size, not an implementation of Schedule 1 or of a coherent receiver"). Negative-control sentence scoped to the controls run: with one evaluation point, wrong intermediate sources exactly when [G,G] ⊄ H (11 of 16), final annihilator still h in all 11. | Applied (C16); `coherent_receiver_implemented` stays false |
| 60 | none (layout) | preamble; Table 1 float | — | New macro `\arxivid` (breakable arXiv ids) used for the seven new plain-text ids; Table 1 placement `[ht]` → `[htbp]` (it had floated to the last pages); codim Cor (i) reworded so its math fits the line. | Applied; no content change |

## Conflicts and judgement calls (more conservative wording applied)

- **C1. Printed threshold of IS Theorem 3.** The core check (§5.3, "font check of the PDF")
  reads it as n > d^{d² log d}(m+1)^{d log d}. The priority check (§9.5) and `main.tex:420`
  write d^{d log d}(m+1)^{d log d}. Both agree on the (m+1)-exponent d log d, which is the
  only part the core fix needs. The copy quotes only that exponent and no longer prints the
  d-power. Someone with the PDF should settle the d-power.
  **Settled 2026-11-02 (parent session):** in arXiv:1503.09016v2, p. 3, `pdftotext -bbox` puts
  a "2" at x 267.5–270.9, y 222.7, directly after and above the exponent's "d" (x 263.3–267.4,
  y 224.5). So the printed threshold is n > d^{d² log d}(m+1)^{d log d}, as the core check read
  it, and `main.tex:420` and the priority check are wrong. The copy's wording stays correct;
  it may now print the full threshold.
- **C2. Table rows.** Combined §5 says to replace the first two rows by one combined row.
  Combined §7.4 instead edits the Large-field row (so it assumes the row stays). The core
  check's verdict is that Thm main holds under Schedule 1 alone, while the combined rule uses
  Schedule 2 at some grades and is conditional. Replacing the Schedule-1 row would merge the
  main theorem's row with a conditional one. Applied: both original rows kept (Large field
  with the §7.4 edit), and a combined row added and marked conditional in the caption.
- **C3. Schedule 2 status.** Core §9.3 allows "proof checked in writing (this review)".
  Combined §5–6 keeps "checked only by automated review" in the caption and forbids any
  human-checked claim. These do not contradict each other; the copy says "checked in writing
  by an AI session … No human has read it … stays conditional" in the text, and "checked only
  by AI sessions, not by a human" in the caption.
- **C4. Related-work paragraph.** Priority §8 replaces the whole paragraph, which would drop
  the paper's free two-generator class-3 example and the input-model comparison. Priority
  §9.6 notes that the example was not tested there, but the paper gives its proof inline.
  Core §9.1 asks for two extra sentences (Cor 8 a special case; IS §5 mechanism). Applied:
  the §8 wording plus the two core sentences, the example and the input-model sentence kept.
  "Possibly new" (A1) became "may be new, and this has not been established"; the special-case
  sentence starts "if Theorem main is correct".
- **C5. Schedule 2 hypothesis.** The combined rule (combined report) uses 16κ_d^{2κ_d+2};
  the small-prime report proposes T_W(κ) or exceptional-set wording. Per the brief, only the
  proposal paragraph was added. The theorem, the combined remark and the table keep
  16κ^{2κ+2}.
- **C6. Φ⁻¹(Ω_1(G)).** `main.tex` writes {x : px ∈ log ker Φ}; the black-box report writes
  {x : px ∈ ker Φ}. In the free chart log is the identity on coordinates, so they are the
  same set; the report's form was used.
- **C7. Combined-row sources "at most Π B_d(g_d)".** Taken from combined §5 as written; not
  re-derived here.
- **C8. Symbol clash.** The fpt report's "Q·T_f" would reuse Q, which §4 uses for G/Z. The
  copy writes Q_f·T_f.
- **C9. Schedule 2 threshold (pass 2).** The weil-threshold report asks to replace the
  hypothesis and construction of Thm power-sde (ii) (fixes 1–3) and to mark (ii) "proved in the
  AI-checked reports" (fix 4). That would rewrite a statement the core check verified in its
  symmetric form, change the thresholds the combined rule and table rely on, and raise the
  label of AI-only proofs. Applied: a separate Proposition `prop:decoupled-sde`, labelled
  "conditional, AI-checked only", with the replacement left to the owner. Fix 4 not applied.
- **C10. Solver column counts.** is-solver fix 2 says larger κ_d "exceed 10^9 columns already
  at a = 1", but its §0.4 gives G(5,1) ≈ 3.1·10⁸ (κ = 5 with a two-term zero sum). The copy
  says "exceed 10^8".
- **C11. Prime-power compiler.** Fix 1's text says A_c "depends only on c", while the report's
  own statement has A_c(M) = m_+ + 2·bitlen(M)·q_+, which grows with log M. The copy writes
  the explicit form. Against row 30 (black-box report: compilers cover prime powers only for
  c ≤ 4, p > 4): the new report proves the words for every c < p and every e, but leaves the
  implemented compiler unchanged. The copy states both: no mathematical limit, and the
  implementation still mod p.
- **C12. Lean files.** Lean fixes 1–2 assume the new files are promoted into `formal/`; the brief
  says to cite them only as files outside `formal/`. Applied: they are cited as review artifacts
  separate from the paper's boundary and the 180 guards. "Outside the boundary are
  general-class BCH and Lazard transport" is unchanged (fix 2 not applied), and the abstract
  is unchanged (fix 3 not applied).
- **C13. Codimension corollary.** The report labels part (i) "conditional only on the checked
  core". The copy titles the whole corollary "conditional", because the core is itself
  pending human review. The report's ideal A is renamed 𝓘, to avoid a clash with the cover 𝒜.
- **C14. Subspace symbols.** The report's block count k and leaf count B clash with ∧^k and with
  B in Thm subspace-source (ii). The copy uses ℓ and B_leaf. Fix 5 asked for a row or a caption
  sentence; the caption sentence was chosen.
- **C15. A1 related-work wording.** Fix 1 asks that "the bound quoted for II24" be made current,
  but the paper quotes no II24 bound, so the improvement was added as a sentence. A1 §5.3 says
  Rees "gets this" for the smooth-order question. The copy says only that, if Thm main is
  correct, it gives a non-exact algorithm for explicit Lazard p-groups of fixed class c < p. It
  does not claim the smooth-order case and makes no novelty claim (a1 §8 gate).
- **C16. Single-evaluation control.** End-to-end fix 2 reads as a general statement ("exactly
  when"); the evidence is the 16 negative-control cases. The copy states it for those controls
  only.
- **C17. q_max.** Compilation fix 4 writes 2M_d g_d; its statement section writes 2M_d r_d.
  With r_d = g_d these agree, and the copy uses g_d. The report also says the core check's §6.2
  q_max undercounts. That is a fix for the core report, not for the paper.

## Fixes not applied (and why)

- `research/REES_HSP_REDUCTION.md:166` ("initialize the q register uniformly"), same ambiguity
  as row 6: not this item's file (campaign rule). Parent session to fold in.
- Black-box: no row for black-box input added to `tab:main-regimes`. The report says none should
  be added.
- Combined §5's literal "replace the first two rows": not applied as written (C2).
- Small-prime report beyond the §9 hypothesis wording (Theorem 4 L-level fallback, M* tables,
  lower bounds): outside the brief's scope for this item.
- Core §5.3 caveat that IS Theorem 3 says "polynomial time" and that determinism is stated only
  in the introduction and proof: not a ranked fix. The copy still says "The algorithm is
  deterministic". Optional for the owner.
- Priority §9 and every report's "reviewer items": checks for experts, not text fixes.
- Title-page date ("October 31, 2026 (corrected draft)") and `README.md` status: left for the
  owner on acceptance.
- **Pass 2:** weil-threshold fix 4 (status upgrade; C9). Lean fixes 1–2 in their
  "promoted into formal/" form and fix 3 (abstract) (C12). Subspace fix 6 (tighter gap
  min{rδ²/4, 1/2}): it would change the code and the budget numbers. Prime-power fix 2 (an
  optional separate lemma). Codimension fix 5 (edits the reduction note, not the paper) and
  fix 4 (no change needed). Non-paper items for the parent: the `formal_draft` pointer in
  `rees_hsp_reduction.json`, the iCloud duplicate `.olean` files, the core check §6.2 q_max
  formula, the stale hashes in `rees_subspace_source.json`, and the three-line change to
  `theorems/universal_lazard_words.py` (modulus p^e).

## Needed edits outside the copy (listed, not made)

**Bibliography (`references.bib` was not edited):**

- **B1.** Add Khukhro, *p-Automorphisms of Finite p-Groups*, LMS Lecture Note Series 246,
  Cambridge University Press, 1998. Then turn the two plain-text pointers (rows 3–4) into
  `\cite[Theorem~10.13]{…}` and `\cite[Chapters~9--10]{…}`. These chapter and theorem
  numbers come from the core report; this pass did not check them against the book.
- **B2.** `IvanyosSantha2015`: the key says 2015, the entry has `year = {2017}`, and the note
  names the FAW 2015 abstract, so the rendered year is 2017. Rename the key (e.g.
  `IvanyosSantha2017`) or make the year match. Add arXiv:1503.09016 v2 as the numbering source,
  and note that the DOI is dated 2016 (online) and the volume 2017.
- **B3.** `ImranIvanyos2023`: key year 2023 (arXiv), entry 2024 (QIP 23:14). Consider
  renaming the key.
- **B4.** `FIMSS2014`: add arXiv quant-ph/0211091 and "Preliminary version in STOC 2003".
- **B5.** `IvanyosMagniezSantha2001`: `@misc` with arXiv only; the SPAA 2001 version is
  unverified. Add it if it is confirmed.
- **B6.** `IvanyosSanselmeSantha2012`: add `number = {1--2}` (Algorithmica 62(1–2)).
- `HallgrenRussellTaShma2003` (unfetched) and `FultonHarris1991` are not cited in the text.
  This is harmless, because bibtex lists only cited keys. Both are unchanged.

- **B7 (pass 2).** These are plain-text citations in the copy that need entries, after which they
  should become `\cite`s. Trappeniers, arXiv:2406.02475 (Thm 2.3). Bennett, "Logical
  reversibility of computation", IBM J. Res. Dev. 17 (1973) 525–532. Kitaev,
  arXiv:quant-ph/9511026. Cleve–Watrous, arXiv:quant-ph/0006004 (FOCS 2000). Dawson–Nielsen,
  arXiv:quant-ph/0505030. Van de Woestijne, ISSAC 2005 (zero sums of d-th powers, §6).
  arXiv:2609.40321 (Thm 1.11), arXiv:2510.07515 (Kothari–O'Donnell–Wu, §5.2) and
  arXiv:2609.34996. Author lists for the last three were not checked here; take them from the
  a1-priority report's sources. Optionally add Cicalò–de Graaf–Vaughan-Lee, J. Algebra 352
  (2012), as prior effective Lazard machinery.

**Numbers (N1).** The paper says every number comes from the JSON artifacts via
`numbers_map.json`. The copy adds hard-coded numbers from the reports: 143 (combined §3.3,
`combined_budget.py` / `combined_out.txt`), and T_W(κ) and the κ = 4, 5 exceptional sets
(small-prime §3, scripts in `2026-11-02-rees-schedules/small-prime/`). Before adoption, add
macros for them (and their JSON sources) or qualify the reproducibility sentence. The
"148 macros" count is unchanged because no macro was added. `make_numbers.py --check` checks
`main.tex` only; the copy uses only existing macros, and it compiled with `-halt-on-error`.

**Numbers (N2, pass 2).** More hard-coded numbers from reports: 2^1592, 14, 420400 and
5,885,600 (subspace budget); E_2(κ) sets for κ ≤ 6, 53 and 859 (small-prime, weil-threshold);
10^8 and 3.7·10^16 (is-solver); 32 subgroups, 11 of 16, 83 guards. Same remedy as N1.

## What now holds

- **Exact statement:** `main-full-draft.tex` contains every ranked text fix from the six
  reports, with conflicts C1–C8 resolved toward the more conservative wording. It compiles
  cleanly with all references and citations resolved. Labels are unchanged: Thm main is still
  "proposed" (AI-checked, pending human review), Schedules 2–3, Cor fpt-r, Thm ring-to-field
  and the black-box e > 1 route are still "conditional", the combined rule is a new
  conditional remark, and the small-prime threshold appears only as a proposal. After pass 2:
  the decoupled contraction (Prop `prop:decoupled-sde`) and the hidden-codimension bound
  (Cor `cor:codim`) are conditional, AI-checked-only statements; Cor `cor:subspace-hsp` is
  "proposed, conditional"; the IS solver and the end-to-end simulator appear only as
  artifacts; the new Lean files appear only as review artifacts outside `formal/`.
- **Still missing:** owner acceptance; the bib edits B1–B6; numbers N1; C1 (IS Thm 3 d-power)
  against the PDF; the human review every report requires; and folding in later reports from
  campaign items 3 (dfs2 runs) and 12 (application), which were still running at pass 2;
  bib B7 and numbers N2.
- **Claim gates that must stay false** (unchanged by this edit): in
  `research/reductions/rees_hsp_reduction.json`, `independent_review`, `novelty_established`,
  `speedup_claim_allowed`, `coherent_receiver_implemented`, `general_sde_implemented`,
  `formal_compiler_checked`, and every `is_total_gate_bound`. Also the gates the
  random-column, ring-to-field and black-box envelope reports list. In addition: "Schedule 2
  is human-checked", "polynomial arity at small primes", and "Schedule 3 / W+3 is polynomial
  time". Pass 2 adds: "A1 is new" or "first graded cover for HSP"; "the two-level threshold is
  ≈1.5κ^{(κ+1)/2}"; "E_2(κ) is known for κ ≥ 7"; the codimension, subspace, compiler and
  filter reports' own gates; and `formal_compiler_checked` (the new Lean files leave
  general-class BCH as a hypothesis).
- **Next step:** the owner diffs the copy against `main.tex` (command above), accepts or
  rejects rows, and makes B1–B7, N1 and N2. Acceptance test: the accepted text compiles with
  `latexmk -pdf`, and `make_numbers.py --check` passes with no undefined macro.
