# Rees HSP paper: referee pass 3 (body), applied, 2026-11-04

AI session; AI-checked, pending human review. Source report:
`research/audits/reviews/2026-11-04-rees-referee-3-body.md` (0 errors, 1 gap,
19 imprecisions). Also applied: `2026-11-04-rees-qft-wire.md` Section 8 and
the Lean class-five boundary of `2026-11-04-rees-lean-c5.md` Section 6.
Files edited: `docs/papers/rees-hsp/main.tex` only (no appendix, not
`main-full-draft.tex`, not `numbers.tex`). No git, no network, no claim gate.

Status words: **applied** (the referee's replacement, at most adjusted to the
current text); **edited** (a different or extended wording, see note);
**already resolved**; **skipped**.

## Referee findings (gap and imprecision only)

| id | finding | status | file | note |
|---|---|---|---|---|
| G1 | thm:main proof, Schedule 1 at d not dividing p-1 | edited | main.tex | Proof now says Schedule 1 runs Thm is-import at exponent kappa_d = gcd(d,p-1), converts by the Bezout exponent of Rem is-import(b), and M_d = B_d(g_d) >= B_{kappa_d}(g_d). The "only imported ingredients" sentence after thm:main now lists the Bezout conversion at grades with d not dividing p-1. The theorem statement is unchanged (see decision 1). |
| I1 | Related work, "not abelian-by-cyclic" | applied | main.tex | Added the exponent-p step ("as p > 3"). |
| I2 | def:input-contract(i) vs thm:main vs thm:rees-cover(i) | edited | main.tex | Def (i): "class at most c". thm:rees-cover (i): class equal to that of L (so at most c); (iii): groups of the class of L, at most c; proof rewritten with c' = class of L (a k-fold bracket of homogeneous elements lies in t^j gamma_j, j >= k). Notation table entry for c: "bound on the nilpotency class (gamma_{c+1} = 0)". The B_d(0) remark was not applied (decision 2). |
| I3 | Abstract, exponent depends on c | applied | main.tex | ", with an exponent that depends on c". |
| I4 | prop:refresh example, two-target lift | edited | main.tex | "the two-target lift map a -> (R_a, R_{2a})" plus one sentence that it illustrates the lift map, not thm:main (which would use c = 1). |
| I5 | Section 3, undefined t in G(kappa_d,g_d)^{ceil log2 t} | applied | main.tex | Renamed to ell_d <= kappa_d + 1, the number of terms of the computed zero sum, in Section 3 and in the Schedule 1 paragraph. Merged with the existing "recalled in Section sec:sde" clause. |
| I6 | Section 3, "the charged count" | applied | main.tex | "the count charged by Remark rem:combined-schedule". Rechecked: 4*9*1024*531441*64 = 1.254e12 uses B_2(3), B_3(2), B_2(1) (kappa_4 = 2 at p = 7). |
| I7 | Bezout-lift bookkeeping inconsistent | edited | main.tex | Not the referee's replacement (which drops the lift as a condition). Per the integrator: rem:combined-schedule now says the steps behind thm:main include the Bezout lift of Rem is-import(b) at every Schedule 1 grade with d not dividing p-1; the paragraph after thm:free-coordinate says its free-coordinate nodes use the elementary identity eq:s3-bezout directly, not Schedule 1, so the lift is not used, and (iii) depends on the steps behind thm:main other than that lift. No status changed. See decision 1. |
| I8 | thm:free-coordinate preamble, kappa_d < p-1 vs part (iii) | already resolved | main.tex | Current hypothesis sentence: "... and kappa_d < p-1 at every such node (part (iii) uses other nodes at the remaining grades)"; the theorem title points to Lemma s3-law for the label law. Not changed. |
| I9 | After thm:power-sde, "verified exactly for r <= 14" | applied | main.tex | Two-line proof for every strictly decreasing profile, with M_d^sym at a = g_d; the r <= 14 check is kept as a check. Rechecked: kappa_d <= d gives (kappa_d-1)g_d+1 <= (d-1)(g_d+1); g_d <= r-d+2; c-1 <= r. |
| I10 | prop:triangular-sde, "g generates F_p^x"; inputs | applied | main.tex | "the image of g generates F_p^x/P"; "given g and (alpha,beta)"; closing sentence now "deterministic given g, (alpha,beta) and the roots", with a pointer to prop:decoupled-sde for the cost of (alpha,beta). |
| I11 | thm:uniform-compilation(i), ODE in t | applied | main.tex | "coefficientwise in an auxiliary variable theta, with Z(theta) = BCH(X, theta Y)", plus "(this theta is not the Rees variable t)". Rechecked that Z' = [ad_Z/(1-e^{-ad_Z})]Y is the derivative of log(e^X e^{theta Y}). |
| I12 | lem:qft-mod reused local symbols | edited (partial) | main.tex | Only the clash inside the proof fixed: the ratio a = 2^{t-1}/N is now A_pe (3 places); the qubit keeps the name a. Other reused letters (t, r, tau, M, W, Z, K, L, S, Q, E) left (decision 3). No replacement LaTeX was given. |
| I13 | tab:full-grade-budget rounding; profile existence | applied | main.tex | Caption: "Entries in scientific notation are rounded up to two significant figures" (all seven macros are `sci:up` in numbers_map.json). Also added that both profiles occur: class 12 for the filiform algebra [e_1,e_i] = e_{i+1}, and (6,3,1) for [x_1,x_2] = y_1, [x_1,x_3] = y_2, [x_1,y_1] = z (Jacobi and lower central series checked by hand). See decision 4. |
| I14 | Resource profile, "this is 144 at c = 9" | applied | main.tex | "so E_W(9) = 143 and the query exponent E_W(9)+1 is 144 (146 with Schedule 1 alone)". |
| I15 | cor:codim proof, k <= 2 | applied | main.tex | "dimension at most 3, hence class at most two". |
| I16 | prop:black-box(iv), ker pi | applied | main.tex | ker Phi in all three places in (iv). The appendix keeps pi (defined there). |
| I17 | Subspace artifact, ell = 420400 | applied | main.tex | Parenthesis: ell comes from the artifact's generic transfer bound and is larger than step (3) requires. Rechecked: step (3) with B_leaf = 2^1569.49, n = 97, p = 43, gamma = 0.005 needs about 2.5e5 blocks for error 1/12. |
| I18 | tab:query-crossover column (v), 15 for 8 ell | applied | main.tex | Caption addition, with "8 ell = 8 ln 6 ~ 14.33". Recomputed: with 8 ell the largest qualifying primes are 83, 121493, 42767, 641; with 15 they are 83, 119659, 42283, 631 (the paper's thresholds 84, 119671, 42290, 638 are valid "p <" bounds). The script `birthday_crossover.py` line 16 uses max(2(1+t), 15). |
| I19 | Abstract Lean boundary and tab:lean-modules stale | edited | main.tex | See rows L1-L4 below. |

Not in scope and not applied: the DL "fine" item's suggestion (Smith normal
form invariant factors {1,3,6}, so rank 52 for every p > 3; decision 5) and
the tool note on `make_numbers.py --check`.

## Other edits

| id | edit | status | file | note |
|---|---|---|---|---|
| L1 | Abstract Lean sentence | edited | main.tex | "class-three, class-four and class-five group and central-descent steps (class five since 4 November 2026)"; "class c >= 6 ... outside that boundary". |
| L2 | sec:formalization, first paragraph | edited | main.tex | Adds the class-five modules and report; a `lake build` of them succeeded with no error, warning or sorry (report Section 4); their 21 guards were added to Audit.lean; no clean-copy build. Guards for the table's modules 396 -> 417; adds that Audit.lean has 38 guards for unrelated modules, 455 in all. |
| L3 | tab:lean-modules | edited | main.tex | Three rows: BCHClassFive 8, BCHClassFiveSubgroups 8, ReesGeneralLawClassFive 5; total 417. Counts by namespace of the `#print axioms` lines in formal/Formal/Audit.lean (455 in all; 396 for the 27 old rows, unchanged; 38 outside the paper). All 21 new guards print [propext, Classical.choice, Quot.sound], except classFive_of_lowerCentralSeries, which prints [propext, Quot.sound]. |
| L4 | "Inside and outside the boundary" | edited | main.tex | Group-law hypotheses discharged at c = 3, 4, 5; one sentence on class five (fields with 2, 3, 5 invertible; subgroups over F_p, p > 5; tuple hiding and measured terminal source at points 1..5); at c = 3, 4, 5 the general-class theorems need no group-law hypothesis, other inputs (SDE policies) remain; c >= 6 conditional. "Outside": c >= 6. |
| B1 | Gate-level control, two sentences | edited | main.tex | qft-wire Section 8 text pasted, except that the lemma's own citation (rees_qft_mod.py, report 2026-11-04-rees-qft-mod.md, N list), which the old sentences carried, is kept after "the circuit of Lemma lem:qft-mod". The sentence "it is not wired into these circuits" is gone. |
| B2 | Gate-level control, sentence "These are fixed finite instances ..." | applied | main.tex | As proposed. The paragraph's final sentence ("They are not a coherent receiver ...") is unchanged. |
| B3 | lem:qft-mod proof, zero-input refinement | applied (checked) | main.tex | Added to the "Total" step: on psi = |0>, ||(V-U)(|0>(x)|0>)|| <= 3 pi 2^{-tau}. Argument: V = V' PREP; with P_0 the ideal preparation, (V-U)|00> = V'(PREP-P_0)|00> + (V'P_0 - U)|00>, and V'P_0|00> = U|00> exactly: PH is the identity (xy = 0, rotations act on zero bits of Z); S has eigenvalue 1 on chi_0 = u_N, so E leaves M in |+>^t; the approximate inverse transform maps |+>^t exactly to |0> for every r, because each CR_k^{-1}, kept or omitted, is diagonal and acts on a pair one of whose qubits has passed its H and is |0>; l = 0, nu~(0) = 0, ADD is the identity. Checked against the proof's text (V = SW E^-1 DEC^-1 ADD DEC E PH PREP; DEC with l = 0 gives W = 2^{t-1}, top b bits 0) and against the implementation `theorems/rees_qft_mod.py`, `aqft_inv_ops` (for s = t-1..0: H on M[s], then CR between M[j], j < s, and M[s]). The paper says only "standard product form"; the textbook order (rotations controlled by already-processed qubits, then H) also satisfies the stated property. 3 pi 2^{-tau} <= eta/(b+3) follows from the choice of tau. |
| C1 | Gate-level control and lem:coherent-linear-sde | edited | main.tex | "(Lemma lem:coherent-linear-sde; it is not wired into these circuits)" -> "(...; none of the three backends uses it)", since there are now three backends; true per the coherent-sde report (Section 5, item 2) and qft-wire Limits item 7. Lemma and its follow-up paragraph read consistently with B1 (no "not wired" sentence about the QFT lemma remains). |

Counts: 20 referee findings: 13 applied, 6 edited (one of them partial),
1 already resolved, 0 skipped. Other edits: 9 (L1-L4, B1-B3, C1; B2 and B3
applied, the rest edited).

## Build and test

- Build in the scratchpad `build/` copy (all `*.tex` and `references.bib`),
  `latexmk -pdf -interaction=nonstopmode main.tex`: exit 0, **130 pages**
  (the backup `bak-i157` builds to 129). No Overfull, no "Float too large",
  no undefined reference or citation; the only Underfull lines are the
  three known bibliography ones (Ivanyos-Sanselme-Santha, Lidl-Niederreiter,
  Nayak).
- `/opt/anaconda3/bin/python -m pytest -q -p no:cacheprovider tests/tools/test_rees_paper_numbers.py`: 2 passed.
  No new macro outside the whitelist (A_pe is `A_{\mathrm{pe}}`; no `\mathsf`).
  `make_numbers.py` was not run.

## For the integrator to decide

1. **Bezout lift in the hypothesis of thm:main.** The proof and the
   sentence after the theorem now cite Rem is-import(b), but the statement
   still says only "assume Theorem is-import". Options: add "(with
   Remark is-import(b) at grades with d not dividing p-1)" to the statement,
   or take the referee's route. Note that eq:s3-bezout (Appendix schedule3,
   proved there) is the same identity as the lift (s = u^t with t d
   = kappa mod p-1), so the lift could be proved in Rem is-import(b) and
   dropped as a condition in rem:combined-schedule and in
   appendix-free-coordinate.tex line 275. Not done, to keep statuses.
2. **Empty grades.** thm:main charges B_d(0) > 1 sources at grades with
   g_d = 0; M_d = 1 there would be cheaper (referee, "not an error"). Not
   applied.
3. **lem:qft-mod local names.** Only A_pe renamed; decide whether to rename
   the other locally reused letters.
4. **tab:full-grade-budget profile examples.** Added on my own check (not
   in the artifact); delete if the caption should stay artifact-only.
5. **Dixmier-Lister rank sentence** ("rank 52 modulo every prime
   5 <= p <= 23"): the referee (a "fine" item) proposes the Smith-form
   statement, invariant factors in {1,3,6}, so rank 52 for every p > 3.
   I did not recompute it, and it is not applied.
6. **Lean build.** The paper now says a `lake build` of the three modules
   succeeded (report Section 4) and that their 21 guards were added to
   Audit.lean. No report records a build of Audit.lean after the guards
   were added. The `.lake` files suggest one ran (Audit.olean 13:10:48,
   after Audit.lean at 13:10:29), but BCHClassFive.lean (13:07:57) is newer
   than its olean (12:59:09). I ran no Lean. Suggest a `lake build --wfail`
   and a guard recount before this text is relied on.
7. **qft-wire numbers** (24/6 and 148/24 transforms, 154/835 qubits, gate
   counts, "below 0.1", "0.6 times") are copied from the report, not
   recomputed. eta is printed rounded up (1.488e-3 -> 1.5e-3); the scaled
   bound is still about 0.0995 < 0.1, but the margin is small.
8. **Differences from the backup that are not mine.** main.tex line 864
   (cor:fpt-r proof: "the time of the node at the grade d = p-1") was
   already in main.tex when I first read it. appendix-schedule2.tex line 269
   (a new last sentence on Phase 0 under prop:mixed-schedule) differs from
   the backup, but I did not edit it. Both are in the build above.
