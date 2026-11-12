# 2026-11-12 Rees paper: headline class-9 exponent 145 → 53 applied

Integrator pass for the owner decision of 2026-11-12. All content is AI-checked, pending human
review. Nothing in this pass promotes a claim: 53 rests on Lemma `lem:rounds` (proved here, AI-checked
and refereed by AI only). G. Ivanyos confirmed only the full-depth bound ⌈log₂(d+1)⌉ (exponent 145).

Backup of every touched file (pre-edit):
`research/audits/reviews/2026-11-09-rees-paper-pass-prep/backup-pre-headline53-2026-11-12/`
(core/main-core.tex, core/numbers.tex, core/main-core.pdf, main.tex, numbers.tex, all
appendix-*.tex, main.pdf, arxiv/METADATA.md).

Edit scripts (exact old→new strings, each asserted to match exactly once):
`/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/265ea4e4-9d06-4353-9b18-ca6cd6e80035/scratchpad/h53/`
`core1.py core2.py core3.py meta.py full1.py full2.py full3.py full4.py full5.py` (helper `edlib.py`).
Every edit applied; none failed.

## 1. Numbers

- `render_numbers.py` re-run; output identical to `2026-11-12-rees-headline-53/numbers.tex.new`
  (MD5 7b0c2d752ad74b59a4e978bafa774421). Copied to `docs/papers/rees-hsp/core/numbers.tex` and
  `docs/papers/rees-hsp/numbers.tex`. `make_numbers.py` was not run.
- Macro changes: QueryExp 145→53, SdeAttempts 1081→441, OrigQueriesBits 1573→564, InstCallsBits
  1570→561, ReesOuterQueryExp 147→55, ReesOuterOrigQueriesBits 2194→794.
- NOT touched: `arxiv/numbers.tex`, `arxiv/main-core.tex` (outside the brief; `build_package.sh`
  copies from `core/`). They are stale until the next package build.

## 2. Core, `docs/papers/rees-hsp/core/main-core.tex` (63 edits)

Part A of `core.patch.md`, with the headline-53 report:
- Abstract (C1, C1b, C25a): "grows like c² log c" → "is Ω(c²)"; the solver is the "collision step" of
  Ivanyos–Santha.
- eq:Bd (l. 164, A2): B_d(a) = a+1 if κ_d = 1, else G(κ_d,a)^{⌈log₂ t_{p,κ_d}⌉}; t_{p,κ} defined;
  published arity B̄_d = G(d,a)^{⌈log₂(d+1)⌉}.
- thm:main (3), (4) (A3, A4): (m+1)^{E_1(c)−1}, E_1(9) = \ReesClassNineQueryExp; A5; rem:main-solver
  (A6): Ivanyos covers the full depth only (145), and lem:rounds is AI-proved and AI-refereed only.
- Imports (A7): Chevalley–Warning, Weil [LN Ch. 6], Rabin; E_1(9) is an exact computation. A8; a
  sec:status sentence (C9).
- thm:is-import (l. 528, A9 + R3): now IS Theorem 11 only (the collision step). The text says the
  rounds are in the proof of IS Theorem 3, §3.3.
- rem:is-import (a)–(d) (A10): (d) Las Vegas preprocessing. It makes ⌈log₂(3(c−1)/ε)⌉ cut-off
  attempts per grade, aborting before any query with probability ≤ ε/3. With Schedule 2 it is split
  ε/6 + ε/6.
- rem:is-printed (A11).
- New lemmas (A12):
  - lem:rounds (l. 556), titled after the proof of IS Theorem 3, §3.3.
  - lem:zero-sum-length (l. 572). (iii) now has "⌈log₂ t⌉ = 1 if h is even, = 2 otherwise" (R3).
    (iv) gives per-trial success 1/2 (h even) and ≥ 1/(4κ) (h odd) (R3). The proof explains the y^κ
    = −1 step. It carries a full-line `% NEEDS HUMAN VERIFICATION` on the Weil locator.
- lem:bezout (A13); rem:zero-sum "(here t_{5,4} = 5)" (A14).
- Schedule 1 paragraph (A15 + R3): preprocessing; merge; the arity G(κ_d,g_d)^{⌈log₂ t_d⌉} with base
  κ_d. It explains why κ_d is legitimate: s^d ranges exactly over the κ_d-th powers, and the import
  needs a degree dividing p−1.
- lem:exponent (l. 615, A16).
- Proof of thm:main (A17 + R1): "Fix the evaluation points 1,…,c"; "(the witness scalars …, not the
  evaluation points)"; E_{s_i} → E_s, s = 1..c. Stop with "fail" if the preprocessing aborts. Error
  ε/3+ε/3+ε/3 = ε. The query bound uses e_{p,d} and E_1(c), and the time includes the preprocessing
  attempts.
- rem:oblivious (A18): "apart from its cut-off classical attempts, made before the first query, there
  are no restarts". rem:proof-uses names lem:rounds and the zero sums.
- Examples (A19):
  - Heisenberg: 8 (p ≡ 1 mod 4) or 64 (p ≡ 3 mod 4).
  - Class 3: B_3(2) = 729 or 3, B_2(3) = 32 or 1024; Q ≤ 3(5+τ)·1024·729 ≈ 2^{23.68}, with equality at
    p ≡ 7 (mod 12).
- Crossover table and rem:query-separation (A21):
  - The caption now says "largest value over p ≥ 11" and states where the maximum is attained.
  - New rows: 20.00/9,391/3,325/218; 23.68/3,413/1,567/293; 25.55/157/97/474;
    563.63/2^{62.60}/2^{62.35}/22,548.
  - 8u thresholds 83/3,373/1,583/97; 2^{174.7} → 2^{62.6}.
- Outlook (A22):
  - Preamble exception for "Halving the degree".
  - "Smaller arities" rewritten (Schedule-2 referee §5): Schedule 1/2 does not lower 53 (vs 145 →
    143 at full depth); the triangular variant gives 2c−1; the best of S1/S2/triangular is 40 at
    p = 73 (exceptional κ = 6, 8, 9); 99 at p = 1009 at the full depth; towers and chains give 37.
  - Status: "S2, triangular, 2c−1, 143, 40, 99: AI-checked and refereed by AI, pending human review;
    block-steered variant, Schedule 3 and 37: conditional".
  - The "Shorter zero sums" paragraph is replaced by "Halving the degree" (l. 986), the 38 referee
    §8 text with M1–M3 and M6 (95 in place of 145 at the full depth). Its status is "AI-proved and
    refereed by AI, pending human review; it is not in the full version". There is no R7 and no
    Cor 41.
  - Open problem (1): "grows at least quadratically in c (Lemma exponent)".
- Artifacts (A23): exact-computation items for the zero-sum depth/exponent and for halving; the
  discharge and discharge-referee notes; the solver item. The informal statement and Related Work
  mention the collision-step import (C25b, C25c).

## 3. Full version, `main.tex` + appendices (Part B)

`main.tex` (64 scripted edits plus the \bigcup fix):
- B1 status; B2–B5 thm:main(3)(4), rem:main-solver (with the B4 sentence), eq:Bd (l. 252). B6
  regimes table; B7 notation rows (B_d, B̄_d, t_{p,κ}, ℓ_d, new E_1(c)/e_{p,d} row); B8 E_W(9) = 53.
- B9 (l. 727): thm:is-import becomes IS Theorem 11 [Sections 3.1–3.2]. rem:is-import (a)–(d): (c)
  explains B̄_d vs B_d and that the confirmation does not cover depth L_d; (d) is the full A10 text
  with the ε/6 split. lem:rounds (l. 741) and lem:zero-sum-length (l. 757) are inserted after
  rem:is-import, copied from the core, with rem:is-printed → rem:is-import(c).
- B10 rem:is-runtime: L = L_d. N_col = 𝒢^L = B_d(a) ≤ M_d. The b⁴ and C₃d⁴b⁵ zero-sum terms are now
  flagged as the Las Vegas preprocessing, NOT re-derived.
- B11: "Arity and determinism" paragraph rebuilt.
  - Kept: the eq:is-arity label (now M ≥ B_d(a)), the implementation, numbering and chain sentences,
    and the van de Woestijne locator.
  - Added: the preprocessing, the base-κ_d justification, "deterministic given the precomputed zero
    sums", the solver term (preprocessing only), B_d ≤ G(κ_d,a)^{⌈log₂(κ_d+1)⌉} ≤ B̄_d, and IS Thm 11
    = collision step with rounds in the proof of Thm 3 §3.3 (R3), "E_1(c) … 53 … against 145 at the
    full depth".
  - lem:exponent (l. 806) inserted before §Schedule 2.
- Recursion budget bullets: the solver share is spent on the preprocessing (split when Schedule 2
  co-occurs). Arities are "computed from public data before any query".
- Simulation paragraph (l. 635): the historical runs are relabelled as full depth (B̄_{κ_d});
  (1024, 729, 64) at F_7 are the new B_d; B̄_3(2) = 531,441 is labelled as the earlier full-depth
  arity.
- B12 rem:combined-schedule: M_d = B_d ≤ B̄_d; "worst case does not move: equals E_1(c) for c ≤ 9
  (against full depth: 145 → 143)". Adds the ε-split sentence.
- B13 prop:coherent-receiver: the statement and proof use Lemma rounds. The machine reads the zero
  sum, and its computation is not part of 𝒞 (existence statement). "Determinism of Lemma rounds
  given its zero sum".
- B14 profile paragraph: depth L_d, worst at p ≡ 2521 (mod 5040), the published_depth_profile key;
  E_W(9) = 53, query exponent 54; envelope 2^{786.7} (2^{423.9} at p = 43; 2^{324.1} with n_p ≤ 19).
- B22 proof: preprocessing step with "fail"; Lemma rounds; "deterministically given the
  preprocessing"; total error ε; the B_{κ_d} parenthetical is deleted. The steps-behind list adds
  Lemmas rounds and zero-sum-length (CW, Weil, Rabin; AI-refereed only).
- rem:oblivious: as A18. B15 examples and B16 table/query-separation: as in the core.
- B18 thm:bb-envelope:
  - e_d(p) ∈ {1, 2, e_{p,d} = κ_dL_d}; E_W = 5, 8, 16, 19, 35, 36, 44, 53; "does not change the
    exponent for c ≤ 9".
  - The solver third is shared with the preprocessing.
  - Bounded-prime comparison 143/144/93 → 53/54/3.
- l. 1336: "van de Woestijne … as in Schedule 1" → "as in the proof of IS Theorem 3" (Schedule 1 no
  longer uses van de Woestijne).
- \bigcup → \cup (3×, inside lem:rounds) because `test_rees_main_tex_has_no_undefined_macros`
  whitelists no \bigcup. The core keeps \bigcup.

Appendices:
- `appendix-torsion-blackbox.tex`: B19.
  - lem:tb-count-grade: e_d = e_{p,d}; the proof uses B_d with L_d ≤ ⌈log₂(κ+1)⌉.
  - lem:tb-count-exponent statement and proof replaced. The witnesses p = 3, 7, 5, 61, 31, 31, 2521,
    2521 were re-verified by my own BFS script: the combined rule and Schedule 1 both give
    5, 8, 16, 19, 35, 36, 44, 53.
- `appendix-provenance.tex`: B20.
  - l. 9: "exponent 143" → "exponents E_1(c)".
  - prov:sde-is-import: "shortened depth not covered".
  - prov:sde-combined: 53 = E_1(9).
  - prov:gc-profiles and prov:cl-crossover: appended.
  - New item prov:zero-sum-depth.
- `appendix-schedule3.tex`:
  - l. 314: exponent E_1(c), degree κ_dL_d.
  - (S1): M_d ≥ B_d with the precomputed zero sum. It says explicitly that the preprocessing abort is
    not in the error split of prop:mixed-schedule, and adds ≤ ε/6.
- `appendix-sde-side.tex`: L = L_d; N_col = 𝒢^L ≤ M_d; the zero-sum term is flagged as preprocessing,
  not re-derived.
- `appendix-free-coordinate.tex`: "B_d of eq:Bd". At d = p−1, p < 4κ⁴, so the zero sum is
  deterministic (BFS); the claim "deterministic step" is therefore true.
- Unchanged: appendix-backends, -codimension, -filters, -schedule2, -subspace.

`arxiv/METADATA.md` (abstract only): the same two phrase changes as the core, and the header
character count is set to 1914 (Python len; limit 1,920). **"Comments: 45 pages" is NOT changed**
(outside the abstract-only permission); the core is now 50 pages.

## 4. Compile (pdflatex/bibtex/pdflatex/pdflatex, nice -n 19)

| | before | after | errors | undefined refs | Overfull | Underfull | other |
|---|---|---|---|---|---|---|---|
| core main-core.pdf | 45 pp | **50 pp** | 0 | 0 | 0 | 0 | none; bibtex 0 warnings |
| full main.pdf | 223 pp | **227 pp** | 0 | 0 | 1 | 5 | 1 float-too-large |

The full version's 1 Overfull (5.87pt, the reading guide near l. 220), its 5 Underfull (bibliography)
and the float warning (regimes table, 74pt) are all pre-existing. I verified this by compiling the
backup in a scratch copy: identical warnings, 223 pp. Nothing was introduced.

Abstract: 1914 characters plain text (METADATA) and 1881 in the LaTeX source, both ≤ 1,920.

## 5. Tests (nice -n 19 /opt/anaconda3/bin/python -m pytest -q)

`tests/tools/test_rees_paper_numbers.py tests/test_rees_hsp_reduction.py tests/test_rees_fcs_budget.py
tests/test_paper_ingestion.py tests/tools/test_paper_numbers.py tests/tools/test_tools_workflow.py`
(every test that reads main-core.tex, rees-hsp/main.tex or the rees-hsp folder): **58 passed**.

The first run failed on \bigcup, which was fixed as above. The arXiv tarball was not rebuilt.

## 6. Patch items NOT applied, and why

- B21 tables NOT recomputed (outside the brief): tab:fcs-budget "combined Q" column,
  tab:full-grade-budget, tab:random-column-budget, the class-3/class-12 resource profiles. They may
  still use the full-depth B_d.
- B10/sde-side: the preprocessing running-time term of rem:is-runtime is NOT re-derived (flagged in
  the text).
- The JSON's per-call attempt model (\ReesClassNineSdeAttempts = 441) differs from the per-grade
  preprocessing model of rem:is-import(d). The text calls it conservative, and the patch notes it is
  conservative only up to one extra attempt per call.
- prop:mixed-schedule and Schedule-3 free-coordinate results do not charge the preprocessing in
  their error splits. This is stated at (S1) rather than re-proved.
- B19 optional Θ(c²) growth remark: skipped. The Hardy–Wright locator is unverified (TRAPS 10).
- The §4 referee's R4 (optional) is skipped. 38-referee M4 is not applicable (Cor 41 and R7 appear in
  neither paper); R7 = 25 is not mentioned.
- R1 is not needed in the full version: its proof of thm:main has no s_i = i clash; the remaining
  E_{s_i} are distinct-point lemmas.
- Cosmetic, left: E_1(c) (exponent) vs E_1(u) (evaluation at 1) share a symbol.
- `verify_headline.json` reports `t2_iff_even_index: false` only because of the p = 2, κ = 1 entry.
  My independent check over odd p < 26244 and κ = 2..9 finds 0 violations.

## 7. Adversarial self-check (both papers; comment lines excluded)

- **145.**
  - Core l. 206 and l. 552: the full-depth exponent Ivanyos confirmed.
  - Core l. 984: Schedule 2 at full depth gives 145 → 143.
  - Core l. 986: halving gives 95 in place of 145.
  - Full l. 245 and l. 802: full depth. l. 893: combined rule at full depth. l. 1165 and
    provenance l. 157: published_depth_profile.
  - provenance l. 300 and schedule2 l. 716: "145 primes", an unrelated count.
  - All justified.
- **147, 1573**: no hits.
- **deterministic.** Every Schedule-1 hit now says "given the precomputed zero sums / the
  preprocessing", or concerns a deterministic sub-step:
  - thm:is-import, Theorem 11 itself;
  - lem:rounds given z;
  - lem:zero-sum-length(iv) for p < 4κ⁴ or odd κ;
  - free-coordinate d = p−1, where p < 4κ⁴.
  - Historical simulation text (l. 635, backends l. 9) describes past full-depth runs.
  - Other hits are unrelated (Nayak, Childs, primality, Schedule 2 phases, subspace designs, mutants).
- **"no restarts".** Core and full rem:oblivious say "apart from its cut-off classical attempts,
  made before the first query"; the recursion bullet says "no restarts" for Schedule 1 merges. True.
- **"does not depend on p".**
  - Core l. 202 and l. 968, full l. 241 and l. 1300: applied to the upper bound c(m+τ)∏B̄_d, which is
    p-free. True.
  - Full l. 1531: E_W(c) is a max over p, so it is p-free. True.
- **Theorem~11.**
  - Every IS hit cites the collision step only.
  - The rounds are attributed to the proof of Theorem 3, §3.3 (core l. 534, full l. 802).
  - l. 281 and l. 1332 are IvanyosMagniezSantha2001, unrelated.
- **143.** Only as the full-depth Schedule-2 value (core l. 984 ×2, full l. 893). The status sentence
  labels it AI-checked and refereed by AI.
- **37.** Core l. 984 only, labelled conditional. Other hits are primes.

Residual risks for the human reader:
- the abstract still says "The elimination and its solver are those of Ivanyos and Santha", while
  the depth change is ours;
- METADATA page count;
- stale arxiv/ copies;
- the not-recomputed tables (§6).
