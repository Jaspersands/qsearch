# Referee 14 (Fable) applied to the Rees HSP paper

Date: 2026-11-05. This was an AI-only integrator pass, with no human review. Input:
`2026-11-05-rees-referee-14-fable.md` (2 Errors, 8 Gaps, 20 Imprecisions, 12 Style).
Files edited: `docs/papers/rees-hsp/main.tex`, `appendix-schedule2.tex`,
`appendix-schedule3.tex`, `appendix-free-coordinate.tex`, `appendix-torsion-blackbox.tex`
and `core/main-core.tex`. Not touched: tables' numbers, `numbers.tex`, `E_W`, `143`,
`references.bib`, `research/reductions/rees_hsp_reduction.json`, `formal/`,
`docs/outreach/`. No git, no network, `make_numbers.py` not run. Every edit was an
exact-string replacement with an asserted count, applied after re-reading the file.
Private backups of the files as they stood before this pass are in the session
scratchpad, `ref14/backup/`.

Note on the shared scratchpad: the first backup went to the shared `scratchpad/backup/`
folder at 03:37, which another concurrent agent also uses. It overwrote that folder's
copies of the `.tex` files with the then-current versions. The other agent rewrote some
of them at 03:39. If an agent relied on `scratchpad/backup/*.tex` as a pre-edit copy from
before 03:37, that copy is gone.

Build (scratch copies): full paper 170 pp., core 27 pp. Both builds exited 0 with
0 Overfull, no undefined reference or citation, and no "Float too large".
`pytest -q tests/tools/test_rees_paper_numbers.py`: 2 passed.

## Findings

Key: V = verified independently; A = applied; R = rejected; G = stated as a gap;
P = applied in part or in a different form.

| Finding | Verified? | Outcome | Notes |
|---|---|---|---|
| E1 `main.tex` rem:two-level-threshold-size | V. The closed form Θ^cf_2, minimised over k, recomputes to 220539 (κ=5) and 1680700 (κ=7). 3781 and 30823 are Θ_2 of rem:app-s2-chains-scope (threshold-7-check §G1, l.171) | A | The sentence now names the closed form (cor:app-s2-union-chain), gives its values (about 2.2e5 and 1.7e6), and attributes 3781 and 30823 to the numerical evaluation of the criteria. |
| E2 title date and status box | V | A | Both now read 5 November. The core paper was already dated 5 November. |
| G1 thm:is-import header and rem:is-import(c) | V. The arithmetic in (c) holds; the reading of the source is AI-only | A (main and core) | The header now carries "imported, as read by AI sessions only (Remark (e)), pending human review". (c) is phrased "as we read that paper … not confirmed with the authors or by a human". The core rem:is-printed has the same caveat. A human still has to read Sections 3.1–3.3 of arXiv:1503.09016v2. |
| G2 `appendix-schedule2` tower, "Finding the scalars" | V. prop:app-s2-TA(iii) needs U ≤ 1+1/(8q), that is p > T_S(q). cor:app-s2-decoupled already splits the cases into sampler and exhaustive search | A + G | The text now uses the sampler for p > T_S(q) and exhaustive search otherwise, and states that the 3/8 bound per round is not proved for T_A(q) < p ≤ T_S(q). |
| G3 `appendix-free-coordinate` proof of (iii) | V, in part. lem:hybrid already allows classical control. lem:s3-hybrid is the precise statement (per-record instruments, aborts, unused slots) and the appendix header lists it as used | A | The proof now cites lem:s3-hybrid and notes that its proof uses lem:hybrid plus the fact that the records are classical. |
| G4 lem:s3-hybrid support hypothesis | V: the hypothesis is asserted and not argued. The referee's replacement says "S_j is the image of S_{j-1}", which is wrong: S_j is defined as a span of canonical encodings, not as an image | P | Its own sentence was added to the proof. S_j is a tensor product of the local canonical subspaces with clean workspace. The listed ideal steps write only canonical encodings and return clean workspace. Aborts only set a flag. |
| G5 schedule3 proof of (iv), independence of tree aborts | V | A | Uses the referee's conditional wording, which matches l.352. |
| G6 prop:rc-lower: bank undefined and "almost every bank" | V. The proof at free-coordinate l.357 proves exactly the s-quantified form | A | The statement now defines the bank (M ≥ a ≥ 1 i.i.d. labels, uniform on an a-dimensional subspace) and quantifies by s ≥ 1. |
| G7 thm:bb-envelope dependence on Theorem 4.7(ii) | V. In lem:tb-count-exponent, E_W = E_1 for c ≤ 7 and E_W = E_1 − 2 for 8 ≤ c ≤ 12 | A (main and core) | The existing "with Schedule 1 alone" sentence now names E_1(c), says the theorem then does not depend on power-sde(ii), and says the combined rule changes the exponent only for c ≥ 8. The "conditional on" sentence is kept. |
| G8 Lean class-seven scope | V. `formal/README.md` lists three class-seven modules. Their files are in `formal/Formal/`, but `Formal.lean` does not import them, `Audit.lean` has 488 guards and none for class seven, `2026-11-05-rees-lean-c7.md` does not exist, and a `lake build Formal.BCHClassSevenSubgroups` was still running | A (paper only) | One sentence after the Lean module paragraph records these facts. The modules are excluded from tab:lean-modules and from the 450/488 counts, and c ≥ 7 stays outside the boundary. **The README is ahead of the build.** It was not edited here (the Lean agent owns it). The owner or the Lean agent should make it consistent once the build finishes. |
| I1 rem:sde-subquadratic(a), H and c | V | A | H became W_0 (the referee's Π would collide with projections) and c became γ, in (a) only. |
| I2 (b), K | V | A | K became θ, an "unknown key", at all 14 occurrences in (b). |
| I3 block-steered and worst-case letters | V | A (modified) | E became J (69 tokens; E_W, E_cg and E_2 untouched). G_E and G^*_E became 𝒢_J and 𝒢^*_J; the referee's Γ would collide with the grade sets Γ_0, Γ_F, Γ_2, Γ_3. In M_J: m became μ and r became r_0; \varrho is not in the macro allowlist of `test_rees_paper_numbers`. L became Λ. The pairs count ρ became ρ_pr. "c a^2" became "C_0 a^2 for every constant C_0 ≥ 1". |
| I4 rem:is-runtime ℓ, G, N | V | A | The prime became q (as in the Appendix A tower), the level index became j, the shorthand G became 𝒢, and N became N_col. ℓ_d is unchanged. |
| I5 caption and abstract conditions | V | P | Abstract: "conditionally also on the two-level schedule" was added to the black-box item, which already sits in the abstract's list of "conditional results". Caption: the added sentence pushed tab:main-regimes into "Float too large" (reported by the integrator), so it was reverted. The same conditions already appear in Contributions item (4), directly after the table. |
| I6 `d` in thm:bb-envelope | V | P | No rename across files. A parenthesis in the statement now says that d is the rank of F_{s,c} in (ii)–(iii) and a grade index in K_c and E_W. A full rename to d_F across Prop 7.1, the notation table and app:tb-counts is left for a later pass. |
| I7 cor:subspace-hsp "argued" | V (the convention at l.368 defines "argued") | A | The text now points to the full proof of the completed form in Appendix D (thm:app-sub-hsp). |
| I8 comparison with Imran–Ivanyos | V (lem:tb-count-prime: Q_core(m) has exponent E_W in m) | A | The text now reads "E_W(9) = 143 in n_p when e_p = 1, or 144 when e_p > 1". |
| I9 Thm 4.8(iii) combined rule | V (free-coordinate l.199) | A | The text now says that there the rule takes the linear schedule or Schedule 1 at d = p−1, and that no Schedule 2 node occurs. |
| I10 Thm 4.8(ii) β arguments | V | A | The text now reads `β = β(4u, 2u+1; a_d)` at every grade. |
| I11 SIS sentence and δ clash | V | A | The main sentence now uses the appendix hypotheses (p ∈ [g^k, 2g^k], arity ≤ min(p²g^{−2θ}, poly), abort clause attached to the method) and cites MicciancioPeikert2013. In appendix (c), δ became θ. |
| I12 ζ in the chain proof | V (ζ = ξ^h at l.116) | A | ζ became γ in the proof of thm:app-s2-chain only (11 occurrences). |
| I13 barrier display letters | V. Recomputed: the threshold 146 at κ=4, p=17, h=2 is correct | A | h, Λ, m, r became h', Λ', a', s. |
| I14 tower notation (D, q, k, ρ) | V | A | A notation sentence was added after the first sentence of app:s2-tower. The moment ratio ρ became ρ_2 (ll. 519, 523, 620). |
| I15 κ=7, \|K\|=4; T_R(9,3) | V (threshold-7-check l.128; tower-check l.126: T_R(9,3) = 134723.2) | A | The list sentence now adds "(for κ = 7 also \|K\| = 4)". In both places the value now reads `T_R(9,3) ≈ 1.347·10^5 < 135000`. The referee's "for any K ∋ 0" was not adopted, because the search scope for κ ≠ 7 was not checked. |
| I16 "does not lower the Schedule 2 arity" | V for the chains: C(a+3,3) is below (a+1)((κ−1)a+1) for small a (for example a = 1). R for the tower: there (a+1)∏((q_t−1)a+1) ≥ (a+1)((κ−1)a+1) for every a ≥ 1 | P | "For large a" was added at app:s2-chains l.551 and in main rem:two-level-threshold-size. Tower l.467 is unchanged, since that statement is true for all a. |
| I17 lem:fc-node used for an arbitrary law | V | A | A transfer sentence was inserted before the proof of (i). |
| I18 FCS, σ_p, vacuous L, M_d ≥ g_d+2 | V. At L = g−1 the second term of eq:fc-beta is ≥ 1, so L ≥ g; σ_p ≤ p by Cauchy–Davenport | A | FCS is now defined after (F1)–(F6). σ_p ≤ p is proved, and the Chebyshev bound is marked as imported and not re-derived. A note says the switch-recursion bound is informative only for L ≥ 2. The sharper M_d ≥ g_d+2 is used at ll. 330 and 498. |
| I19 notation row h | V | A | The row now cites Thm 4.8 and Sec. app:s3-setting. |
| I20 witnesses and monotonicity | V for "for example". R for "integers only": x^{x(x−1)⌈log₂(x+1)⌉/2} is nondecreasing on the reals x ≥ 1, because base and exponent are both nondecreasing there | P | Only "attained for example at" was applied. |
| S1 length and structure | n/a | owner decision | See below. |
| S2 header labels applied inconsistently | V (14 unlabelled headers) | R (owner) | The proposed fix deletes "AI-checked, pending human review" from headers, which this pass may not do. Adding labels to the 14 headers is a possible later pass. |
| S3 Section vs Appendix | V | A | Five `Section~\ref{app:…}` in the body became `Appendix~\ref{…}`. |
| S4 dates in the abstract | V | A | The parenthesis was deleted. |
| S5 Cor 6.2 letters | V | A | The guard rank is now r_obs. K and S became 𝔨 and 𝔰, as in Appendix F. |
| S6 Thm 7.3(iii) 40-line item | V | R (owner) | Moving it to Appendix E is a restructuring. |
| S7 tab:random-column-budget label | V | A | "AI-checked, pending human review." was appended to the caption. |
| S8 letter reuse in Appendices B and C | V | deferred | A large rename across two appendices plus main.tex:761 and :326; not safe tonight alongside concurrent editors. |
| S9 "source comment" pointers | V | A | free-coordinate ll.36 and 345 now name the check files (`2026-11-02-rees-free-coordinate-appendix/fc_appendix_check.py`, `…schedule3-cost/fcs_budget.py`). schedule3 l.41 now says the script stayed in an AI scratchpad and is not in the repository. |
| S10 free-coordinate redundancies | V | P | The ε/9 paragraph was cut to three sentences, and the duplicated "Let the labels…" in rem:fc-tradeoff was removed. The irrationality sentence was kept, because it is correct and short. |
| S11 ξ-independence of tower scalars | V (each R_t = D_{t−1}Z_{D_t} is a subgroup, so uR_t = R_t) | A | |
| S12 why the listed primes lie in E_2 | V | A | The referee's one-clause reason replaces the longer one. |

## Claim gates and labels

No speedup, novelty, human-review, implemented-receiver, general-SDE or
formal-compiler claim was added, and no "AI-checked, pending human review" label was
removed. The status of thm:is-import is now stated more weakly, not more strongly.

## For the owner: structure (S1, S2, S6; nothing applied)

The referee's main objection is that the document reads as a project log. The paper is
170 pp., with a 66-page body, about 184 `\file{}` paths in the body, 13 "previous
version" and 8 "withdrawn" passages, a 38-line status box and 20 `% NEEDS HUMAN
VERIFICATION` comments. The cuts below are proposed and none removes a theorem. The
referee estimates that together they bring the body to about 35–40 pp.

1. Move Remarks 4.11–4.13 (`rem:sde-subquadratic`, `rem:sde-block-steered`,
   `rem:sde-worst-case`, main.tex ~702–741, about 4 pp.) to a new appendix, "Side results
   on the arity of the diagonal equation". Each says "nothing else in the paper uses it".
   Keep one pointer sentence in `rem:triangular-scope`.
2. Move most of Remark 4.10 (`rem:two-level-threshold-size`, about 1.5 pp.), the part
   from "The rest of this remark summarizes arguments made only in the cited reports"
   onward, to Appendix A after `tab:app-s2-thresholds`.
3. Remark 4.6 (`rem:is-runtime`): keep the two displayed step bounds and "C_1 not
   computed". Move the Turing-machine tape layout to Appendix E next to
   `prop:tb-count-gates`, its only user.
4. Section 5.1, the backend paragraphs (Gate-level control, Binary arithmetic,
   Coherent-label backends, Instances, Scope; about 5 pp.): replace them with one table
   (backend, file, instance, qubits, gates, what is simulated or only counted) and at most
   15 lines of text. Move the prose to a supplement.
5. Status box (main.tex 62–99): cut it to about five lines (a draft, no human review, the
   main theorem proposed, change logs in `research/audits/reviews/`). Move the version
   history and the 13 "previous version" and 8 "withdrawn" passages to a "Changes"
   appendix. The referee lists them at ll. 173, 235, 433, 461, 519, 551–558, 640, 766,
   993, 1040, 1087, 1127, 1172, 1192, 1325.
6. Replace the body's `\file{}` paths with short artifact tags and add an "Artifacts"
   appendix table that maps each tag to its path and report.
7. Move Section 8 (classical filters, main.tex ~1188–1222) to an appendix and keep 8.1
   (classical query complexity) in the body.
8. Caption of `tab:main-regimes` (20 lines): move everything after its second sentence
   into the paragraph before the table. This would also free room in that float, which
   is near "Float too large".
9. Theorem 7.3(iii) (S6): replace it with the one-line pointer to
   `prop:tb-count-gates` that the referee drafted, and move the itemized terms to
   Appendix E.
10. Appendices B and C duplicate an induction (`prop:mixed-schedule` vs `lem:fc-forest`,
    `prop:s3-uniform` vs `prop:fc-uniform`(a)). Merge them into one proposition with two
    trial counts. In Appendix A, reduce the E_2(8) run provenance (about 900 words) to a
    table and a pointer.
11. Status labels (S2): one rule is needed. Either label every theorem-like header, or
    put one blanket sentence in the status box and keep only the "conditional", "finite
    computation" and "argued" labels on headers. The second option removes labels, so
    the owner has to approve it.

## Open items carried forward

- A human must read IvanyosSantha2015 Sections 3.1–3.3 (G1). The main theorem depends on
  that reading.
- `formal/README.md` and the Lean build disagree on class seven (G8). Reconcile them when
  the class-seven build completes. The paper's boundary sentence will then need updating,
  together with tab:lean-modules and the 450/488 counts.
- Tower step 1 in the band T_A(q) < p ≤ T_S(q) has no proved sampler bound (G2). Only
  exhaustive search, constant for fixed q, is claimed there.
- Deferred: S8 (renames in Appendices B and C) and the full I6 rename to d_F.
