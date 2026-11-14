# Hostile referee: full-version sync to the 68-page core snapshot (2026-11-14)

AI only (one Claude Code referee agent, with one helper sub-agent for the HSP23 appendix),
pending human review. Targets: `docs/papers/rees-hsp/main.tex` and `appendix-*.tex` (276 pp.),
against `2026-11-14-rees-full-sync/core-snapshot-68pp.tex`, the pre-sync backup
`2026-11-09-rees-paper-pass-prep/backup-full-pre-sync-2026-11-14/`, the sync report
`2026-11-14-rees-full-sync.md` and its `superset_map.md`.

- No existing file was edited. There were no Git commands and no network use.
- The compile ran on a scratch copy under `nice -n 19`.
- Scripts and outputs are in `2026-11-14-rees-full-sync-referee/`:
  - `labdiff.py`, a per-label word diff, snapshot against full;
  - `spandiff.py`, a line-range word diff;
  - `snapmiss.py` with output `snapshot_missing_sentences.txt`: snapshot sentences absent from the
    full version;
  - `lostsent.py` with output `lost_sentences.txt`: pre-sync sentences absent after the sync;
  - `check.py`, the helper's exact sympy checks of HSP23;
  - `compile_*.txt` and `compile_main.log`.

Line numbers below are those of the files on disk at review time. Labels: PROVED, PROVED given cited
theorems, CONDITIONAL, REFUTED, UNKNOWN, NOT computed.

## Verdict: ACCEPT WITH FIXES

**What holds.**
- `thm:main` is word-identical to the snapshot. Its hypotheses, the exponents 20, 38, 53 and 145, and
  its caveats are the snapshot's.
- Ivanyos is cited only for the full-depth bound.
- No sentence claims `thm:main` without the Ivanyos–Santha import.
- `cor:plus-chain` with Δ_t ⊇ lift is PROVED by its stated proof.
- The HSP23 appendix is faithful to its sources, with minor fixes.
- The compile is clean apart from two dangling PDF link destinations.

**What does not hold.**
1. The sync left the full version's own results, and one abstract sentence, still identifying
   Theorem main with its old Schedule 1 form. They now say false things: findings 1 and 2.
2. The superset claim "0 MISSING" is not quite true. One snapshot paragraph with a modelling
   assumption, and the notation it defines, did not make it into the full version: finding 3.

All three fixes are textual. No mathematical result is refuted.

## Checks performed

### 1. Superset map

**All 24 ADAPTED rows** were diffed word by word (`labdiff.py`) or by line range. Each full-version
item contains the snapshot item's content, up to the notation θ→λ, merges, relabelled section
references and added status tags. There are two exceptions:
- `rem:black-box-scope` now contradicts its own corollary's proof (finding 2).
- `rem:query-separation` acquired a new false sentence (finding 4).

**STRONGER `cor:plus-chain`** (main.tex:1150). **PROVED** by reading.
- Lemma `lem:plus-refine` (l.1133) assumes Δ ⊇ lift_D(Ω′).
- Its proof uses only that the D-class of every nonzero c^ν_b lies in Δ.
- Classes in Δ outside the lift give zero vectors U^ν_i. These are harmless rows of the
  (r−1)a × n elimination.
- The chain proof is induction with that lemma plus (r−1)a+1 ≤ (r−1)(a+1). The arity and constants
  use |Δ_t|, so a larger Δ_t only enlarges them.

**STRONGER `thm:uniform-compilation`** (l.1450). It is not strictly stronger:
- the snapshot's (i) clause "and O(d³) further vector operations" is absent;
- the snapshot's (iii) definition of C and J is absent;
- the inverse-transform sentence after the proof is absent (finding 3).

It should be ADAPTED.

**18 random SAME/ADDED rows** (seed 20261114; list in `sample_labels.txt`):
- 13 labelled environments are identical (ratio 1.000), or differ only by \bigcup→\cup, a status
  tag, or "solution"→"valid witness" / Q→Ḡ in `prop:descent`.
- 5 section labels were checked by span diff: same up to headings.
- The map note for `lem:plus-tensor` ("verbatim except z_m sentence") is inaccurate. The text is
  identical apart from \bigcup. Editorial.

**Snapshot sentences absent from the full version.** `snapmiss.py` lists 231 of them, after
normalisation. I read all of them. Almost all are rewordings kept under "older equivalent wording".
The substantive losses are in finding 3.

### 2. Main theorem, abstract and introduction

- `thm:main`: ratio 1.000.
- Abstract (l.114) and status quote (l.69–104): 20 / 38 / 53 / 145, "AI-checked and AI-refereed
  only", and conditional on Theorem `thm:is-import`.
- Ivanyos appears only as confirming the full-depth bound: l.75–78, 278, 388, 872, 1660, 2194, and
  appendix-provenance.tex:45.
- `rem:plus-is` (l.1335, verbatim from the snapshot) says the computation is "suggesting" the import
  is not needed for c ≤ 9, "while Theorem main retains the import as a hypothesis". That complies
  with the brief, so no change is needed.
- Nothing in `thm:main` is stronger than in the snapshot.
- Sentences elsewhere in the abstract are stale (findings 1 and 2).

### 3. HSP23 appendix

The helper sub-agent read all sources. I spot-checked its claims:
- the s(p) values (finding 8.1);
- "the F23 referee re-derived it" against `2026-11-13-rees-free23-theorem-referee.md:125`, which
  says "my derivation agrees", so the claim is partly right (finding 8.3);
- the "small p" wording against `…-all-subgroups-referee.md:225`, which matches the source;
- `check.py`, re-run: all identities have difference 0, and the type counts are 1901 and 6453.

**Labels.**
- The labels are correct: AI-proved and AI-refereed only, pending human review.
- The appendix is conditional on IS Cor. 8, abelian HSP, Rabin root finding and exact QFT_p.
- It is "not used elsewhere": no `f23:` label is referenced outside the appendix, and `app:free23`
  appears only as pointers, at main.tex:346, 351 and 369.

**Bound and referee fixes.**
- s(p) ≥ (1−3/p)²(1−1/p) for p ≥ 5 matches all-subgroups.md:180 and referee:21 exactly.
- The step-6 dependence is flagged at l.5 and l.277.
- All five all-subgroups referee fixes, and the applicable F23 referee fixes, are applied.
- The open items stay open: the IS equation-independence bound, free33, and the hybrid argument
  cited from memory.

### 4. Consistency

This is findings 1, 2, 4–7 and 10.
- No sentence states 53 as the headline.
- The class-nine profile paragraph (l.1678) and `tab:query-crossover-s1` are labelled as Schedule 1.
- `tab:query-crossover` is labelled as 1H+, with a 1H row that is marked as an upper bound.

**The two black-box proofs** (`cor:black-box` l.1980 against `app:core-proofs` l.7; `cor:black-box-pe`
against l.29) are consistent:
- error splits: kernel ε/4 (ε/8 + ε/8, or Lemma tb-kernel at δ = ε/4), core ε/2, socle calls
  ε/(2b′);
- t = min(d, L) + ⌈log_p(8/ε)⌉;
- abort rules;
- worst-case count c(L+τ)∏B_d(L), with B_d monotone.

Both run Theorem main, that is, Schedule 1H+. This contradicts `rem:black-box-scope` (finding 2).
There are two dangling references (findings 3 and 12).

### 5. Compile

The scratch copy was built with pdflatex ×2, bibtex, then pdflatex ×3:
- 276 pages;
- 0 `!` errors;
- 0 undefined references or citations;
- 0 multiply-defined labels;
- 0 overfull boxes;
- 5 underfull boxes, all in the bibliography;
- bibtex clean.

**Three things the sync report does not mention.**
- **Two dangling destinations.** `pdfTeX warning (dest): name{theorem.M.3}` and `{theorem.M.7}`
  "referenced but does not exist" appear. They are also in the repo's own `main.log`. These are
  `f23:types` and `f23:alg`: theorem environments whose body begins directly with an `enumerate`, so
  two hyperlinks go nowhere (finding 9).
- **An extra pass was needed.** A fresh directory needed a fifth pass: pass 4 still printed "Label(s)
  may have changed".

## Findings

Severity:
- **MAJOR**: a false or contradictory sentence in a statement or the abstract, or a superset gap.
- **MINOR**: a false or imprecise sentence elsewhere.
- **EDITORIAL**: the rest.

### MAJOR 1. The coherent receiver is still identified with Theorem main's count and arities

Theorem main now uses A⁺_d and the Las Vegas Schedule 1H+. Proposition `prop:coherent-receiver` needs a
deterministic Turing machine and uses M_d = B_d(g_d). No receiver at A⁺_d is proved.

- **main.tex:115** (abstract): "a coherent receiver with the same queries and error also exists" →
  "a coherent receiver with the Schedule~1 query count $c(m+\tau)\prod_d B_d(g_d)$, an upper bound
  for that of Theorem~\ref{thm:main}, and the same error also exists"
- **main.tex:1565**: "that a general receiver exists at the arities of Theorem~\ref{thm:main}" → "that
  a general receiver exists at the Schedule~1 arities $B_d(g_d)$"
- **main.tex:1567** (title): "Coherent receiver at the arities of Theorem~\ref{thm:main}" →
  "Coherent receiver at the Schedule~1 arities"
- **main.tex:1569**: "$Q = cSP$ (the count $Q_{\mathrm q}$ of Theorem~\ref{thm:main})" →
  "$Q = cSP = c(m+\tau)\prod_{d=2}^cB_d(g_d)$ (the Schedule~1 count, an upper bound for $Q_{\mathrm
  q}$ of Theorem~\ref{thm:main})"
- **main.tex:1571**: "makes the $Q$ oracle calls of Theorem~\ref{thm:main}" → "makes $Q$ oracle
  calls"
- **main.tex:1604**: "It costs the same queries as Theorem~\ref{thm:main} and the same error budget" →
  "It costs the queries of the Schedule~1 form of Theorem~\ref{thm:main}
  (Remark~\ref{rem:main-solver}) and the error budget of Section~\ref{sec:recursion}"
- **appendix-backends.tex:47**: "with the query count, arities and error of Theorem~\ref{thm:main}" →
  "with the Schedule~1 query count and arities and the error bound of Theorem~\ref{thm:main}"

### MAJOR 2. Which solver the black-box corollaries use, and the combined-rule comparisons

The proofs of `cor:black-box`, `cor:black-box-pe` and `app:core-proofs` run Theorem main, and so does
the outlook (l.2196, "proved … with Schedule 1H⁺"). Several places say "Schedule 1 alone" instead.
Several more say that the combined rule of `thm:bb-envelope` gives smaller counts than the
corollaries. Against Schedule 1H+ that is false at c = 9: E_W(9) = 53 > 20.

- **l.115**: "which gives smaller query counts, conditionally also on that schedule" → "which gives
  smaller query counts than Schedule~1 alone (not than Schedule~1H$^+$), conditionally also on that
  schedule"
- **l.312** (table): "Schedule~1 on an acquired chart" → "Theorem~\ref{thm:main} (Schedule~1H$^+$) on
  an acquired chart"
- **l.320**: "Schedule~1 on a chart acquired without queries to $f$" → "the algorithm of
  Theorem~\ref{thm:main} on a chart acquired without queries to $f$"
- **l.353**: "in place of Schedule~1 alone, which gives smaller query counts" → "in place of
  Schedule~1H$^+$, which gives smaller query counts than Schedule~1 alone, but not than
  Schedule~1H$^+$"
- **l.1995**, two changes:
  - "stated with Schedule~1 alone." → "stated with the solver of Theorem~\ref{thm:main} (no
    Schedule~2); its worst-case count uses $B_d \ge A^+_d$."
  - "with Schedule~1 alone, by a Sylow split" → "with the same solver, by a Sylow split"
- **l.2000**: "and Schedule~1 alone, extends" → "(no Schedule~2), extends"
- **l.2058**, two changes:
  - "in place of Schedule~1 at every grade" → "in place of Schedule~1H$^+$ at every grade"
  - "so its query counts are never larger and are smaller whenever such a grade occurs" → "so its
    query counts are never larger than with Schedule~1 alone, and are smaller whenever such a grade
    occurs; they are not compared with Schedule~1H$^+$, whose class-nine exponent
    $\ReesClassNinePlusExp$ is below $E_W(9) = 53$"
- **l.2064**: "in place of the Schedule~1 arities of Theorem~\ref{thm:main}" → "in place of the
  arities $A^+_d(g_d)$ of Theorem~\ref{thm:main}"
- **l.2196**: "This version states the same composition (Theorem~\ref{thm:bb-envelope}) with
  Schedule~2 as well, which would give smaller query counts at some primes, under the conditions of
  the paragraph on smaller arities." → "This version states the same composition with the combined
  rule of Remark~\ref{rem:combined-schedule} (Schedules~1 and~2, without Schedules~1H and~1H$^+$) as
  Theorem~\ref{thm:bb-envelope}; at some primes its counts are smaller than with Schedule~1 alone,
  but they are not compared with Schedule~1H$^+$, and combinations of the two are not claimed
  (Remark~\ref{rem:halving-core})."
  - The same sentence is in the core outlook ("The full version states …"). It is passed to the
    integrator; I did not edit the core.

### MAJOR 3. Superset gap: the snapshot's compilation preamble and inverse-transform bound

These snapshot sentences have no equivalent in the full version:
- the opening paragraph of snapshot sec:uniform-compilation (snapshot l.1018): classical steps by
  Bennett, the QFTs as the only approximate gates, U_f specified only on canonical encodings, the
  black box any unitary that agrees with U_f there, and "No guard or controlled oracle call is
  needed";
- the sentence after its proof: "Since ‖CJ − JF‖ = … the inverse transform has the same error bound."

The gap shows in three places:
- **main.tex:1984** and **appendix-core-proofs.tex:10** say "as for $U_f$ before Lemma
  hybrid", but nothing about U_f is stated there. This was already dangling before the sync.
- **main.tex:835** uses C and J ("Theorem~\ref{thm:uniform-compilation}(iii) gives ‖C|ψ⟩ − (J
  QFT)|ψ⟩‖ ≤ η"). The full version's (iii), at l.1455, does not define them.

Fixes:
- (a) Insert snapshot l.1018 verbatim immediately before `\begin{lemma}[Sequential hybrid on a
  canonical domain]` (main.tex:816).
- (b) In l.1455, after "with clean workspace", add: ", that is, by a unitary $C$ on the encoding
  register and a workspace with $\|CJ - J\,\mathrm{QFT}_{\Fp}\|_{\mathrm{op}} \le \eta$, where $J$
  embeds $\Span\{|x\rangle : 0 \le x < p\}$ with zero workspace,".
- (c) After the proof of thm:uniform-compilation, add the snapshot sentence "Since $\|CJ - J F\| =
  \|(CJ - JF)F^\dagger\|$ and $C^\dagger J - JF^\dagger = C^\dagger(JF - CJ)F^\dagger$, the inverse
  transform has the same error bound."
- (d) In the map, change thm:uniform-compilation from STRONGER to ADAPTED, and add these to the
  snapshot-material rows.

### MINOR 4. `rem:query-separation`: one sentence still swallowed, and a new false one

The sync report says the sentence hidden by the `% NEEDS HUMAN VERIFICATION` comment is now printed.
It is not:
- **main.tex:1863**: "Theorem~\ref{thm:main} adds polynomial running time at polynomially many
  queries; … far above the information-theoretic one" is still inside the comment line.
- **main.tex:1864**: a new sentence says Theorem main's "query count … does not depend on $p$ once $p
  \ge 3/\eps$". That is false. The count depends on p through A⁺_d, as the caption of
  `tab:query-crossover` says. Only the B̄_d bound is independent of p.

Fix:
- End the comment after "Theorem numbering in the IPL version not checked.".
- Move "Theorem~\ref{thm:main} adds polynomial running time at polynomially many queries; it does not
  lower the query count, and its count is far above the information-theoretic one
  (Table~\ref{tab:query-crossover})." to its own line.
- Replace l.1864 by "Its query count is polynomial in $m$ of degree at most $E_+(c)$ and is bounded
  independently of $p$ once $p \ge 3/\eps$; we make no claim about the optimal quantum query
  complexity."

The swallow is also in the core (snapshot l.1347), which is for the integrator.

### MINOR 5. Further stale sentences that say Theorem main uses B_d or deterministic Schedule 1

- **main.tex:872** (also core:566): "Theorem~\ref{thm:main} uses the smaller arity $B_d \le \bar B_d$"
  → "Schedule~1, which Theorem~\ref{thm:main} calls inside Schedules~1H and~1H$^+$, uses the smaller
  arity $B_d \le \bar B_d$"
- **appendix-backends.tex:9**: "not the $B_d(g_d)$ of Theorem~\ref{thm:main}" → "not the Schedule~1
  arities $B_d(g_d)$"
- **appendix-free-coordinate.tex:38**: "the Schedule~1 step of the proof of Theorem~\ref{thm:main}" →
  "the Schedule~1 form of the proof of Theorem~\ref{thm:main} (Remark~\ref{rem:main-solver})"
- **appendix-free-coordinate.tex:199**: "This is the deterministic step used in the proof of
  Theorem~\ref{thm:main}" → "This is the deterministic Schedule~1 step of
  Remark~\ref{rem:main-solver}"
- **appendix-free-coordinate.tex:256**: "deterministically, as in the proof of Theorem~\ref{thm:main}"
  → "deterministically (Lemma~\ref{lem:rounds})"
- **appendix-subspace.tex:102**: "the part of the procedure of Theorem~\ref{thm:main} that runs after
  the lift" → "the part of the Schedule~1 form of the procedure of Theorem~\ref{thm:main}
  (Remark~\ref{rem:main-solver}) that runs after the lift"
- **main.tex:1997**: "not Schedule~1 alone)" → "not Schedule~1 alone or Schedule~1H$^+$)"

### MINOR 6. Notation table

- **main.tex:456**: "exponent of $m$ in the bound of Theorem~\ref{thm:main}(4)" → "exponent of $m$
  in the Schedule~1 bound of Theorem~\ref{thm:main}(4)".
- Add rows for:
  - A_d(a), A⁺_d(a): the arities of Schedules 1H and 1H+ (Def. `def:schedule1h`,
    `def:plus-schedule`);
  - E_H(c), E_+(c), C⁺_c (Lemmas `lem:halved-exponent`, `lem:plus-exponent`).

  None is in the tables at l.400–500.

### MINOR 7. The Lean placeholder overstates

The text at **main.tex:2219** says the package "checks the algebraic and combinatorial content of
Section~\ref{sec:plus}". `2026-11-14-rees-lean-schedule1hplus.md` excludes several parts:
- `lem:plus-sm`(ii);
- the Weil step; (i) is checked only conditionally on a pair-count hypothesis;
- the exact computations;
- time and Las Vegas behaviour.

Fix → "checks part of the algebraic and combinatorial content of Section~\ref{sec:plus}
(Lemmas~\ref{lem:plus-refine}, \ref{lem:plus-tensor}, \ref{lem:plus-ell-node}, \ref{lem:plus-stage}
and~\ref{lem:plus-finish}, Corollary~\ref{cor:plus-chain}, and Lemma~\ref{lem:plus-sm}(i) conditional
on an explicit pair-count hypothesis; not Lemma~\ref{lem:plus-sm}(ii), the exact computations, or
running time)".

### MINOR 8. HSP23 appendix (helper findings, verified as noted)

1. **appendix-free23.tex:46** — VERIFIED. "s(7) ≥ 0.280, s(11) ≥ 0.481" are false. The exact values
   are 96/343 = 0.27988 and 640/1331 = 0.48084. Fix → `s(7) \ge 0.279`, `s(11) \ge 0.480`.
2. **l.5 and l.277** — UNKNOWN, helper's reading. "For small $p$" follows referee:225 word for word.
   Spoiled runs occur at every p, with probability up to about 3N_T/(p+1), so the s(p) bound as
   stated rests on step 6 for every p. Optional fix → "The bound $s(p)$ as stated rests, for every
   $p$ and essentially for small $p$, on …".
3. **l.262** — VERIFIED, partly. "The notes give this derivation at the level of detail reproduced
   here; the F23 referee re-derived it." The notes call it a "sketch" (pair-measurement.md:396, 428).
   The F23 referee did write "my derivation agrees" (theorem-referee:125). The all-subgroups referee
   did not re-derive it (referee:19). Fix → "The notes give this derivation as a sketch, reproduced
   here; the F23 referee re-derived it for unspoiled copies, and the all-subgroups referee did not
   re-derive it."
4. **l.315–320** (Theorem f23:route). It has no status tag or hypotheses, and its (i) needs (I4) and,
   for spoiled runs, Lemma f23:S step 6. Fix: prefix "Assume (I3) and (I4) (AI-proved, pending human
   review; for spoiled runs (i) rests on Lemma~\ref{f23:S}, step~6)."
5. **l.14 and l.18–24**. "(Lazard, p > 3)" is used without being listed as an import, while main.tex:281
   lists it for Theorem main. Fix: add "(I5) the subgroup form of the Lazard correspondence, as for
   Theorem~\ref{thm:main}" and change "(I1)--(I4)" to "(I1)--(I5)" at l.5 and l.34.
6. **Editorial.**
   - l.209: "linear in" holds for the τ-coefficient only.
   - l.295: also mention the global sign of the D_ℓ phase.
   - l.277: "the referee's 300 runs" should be "the 300 runs of e2e_spoiled.py at p = 5".
   - l.365: add "(route (c) not simulated on trivial H)".
   - l.5: point to "Remark~\ref{f23:approx}" instead of rem:free23.
   - l.50: ε is overloaded (gate error and the hidden vector).
   - "about 4200" (rem:free23) is fine: the oracle-model value is 4204, and the notes' 4206 is the
     copies-only term.

### EDITORIAL 9. Dangling PDF links

At **appendix-free23.tex:59 and 154**, `\label{f23:types}` and `\label{f23:alg}` → `\phantomsection\label{…}`.
A one-line lead-in before the `enumerate` would also work. This removes the two pdfTeX
"referenced but does not exist" warnings.

### EDITORIAL 10. Mixed notation for the dilation scalar

**Where.** The dilation scalar is written δ_θ at main.tex:145, 655 and 1743, and δ_λ at l.159, 187,
203, 421, 544–606, 2246 and 2306, and in appendix-subspace.tex. The notation table, at l.421 and
l.424, uses λ for both the dilation scalar and the measured label, and sec:plus uses λ_b for
columns.

**Fix.** Use θ throughout for the dilation scalar, as the snapshot does: δ_λ→δ_θ and E_{s/λ}→E_{s/θ}
in thm:rees-cover, lem:homogeneous, prop:single-evaluation, rem:fewer-points, the intro and the
notation table.

### EDITORIAL 11. `\bigcup` → `\cup`

In `lem:rounds` and `lem:plus-tensor`, this change prints a small cup with a subscript. The better
fix is to add `\bigcup` to the KNOWN list of `tests/tools/test_rees_paper_numbers.py`. That is not
my file to edit.

### EDITORIAL 12. A reference to a proof that no longer has that part

**appendix-core-proofs.tex:24** says "Kitaev's construction in the proof of
Theorem~\ref{thm:uniform-compilation}(iii)". The full version's proof has no (iii) part. Fix → "Kitaev's
construction of Theorem~\ref{thm:uniform-compilation}(iii) (or Lemma~\ref{lem:qft-mod} for odd
$p^e$)".

### EDITORIAL 13. Inaccuracies in the sync report and map

- **Sync report section 1** says the swallowed sentence of `rem:query-separation` is now printed. It
  is not (finding 4).
- **Sync report section 2** says the compile is clean. Two dangling destinations remain (finding 9).
- **Map, `thm:uniform-compilation`**: STRONGER → ADAPTED (finding 3).
- **Map, `lem:plus-tensor`**: the note is wrong (section 1 above).

## Adversarial self-check

- **Stale-reference coverage is not exhaustive.** I found the references in findings 1, 2 and 5 by
  regex: `thm:main` near B_d, "Schedule 1", "deterministic", "same queries" or "arities of". A
  reference phrased differently, such as "the algorithm above" or "the main procedure", could be
  missed. A human should grep `Theorem~\ref{thm:main}` across all appendices.
- **Finding 2 assumes the snapshot's choice of solver.** I took the corollaries to run Theorem main
  (Schedule 1H+), because their proofs say so. If the integrator prefers "Schedule 1 alone" for the
  black-box results, the fix is the reverse: change the proofs, `app:core-proofs` and the outlook. In
  either case the current text is inconsistent.
- **Is finding 1 real?** Proposition `prop:coherent-receiver` remains a correct Schedule 1 result.
  Only its identification with Theorem main is false. I judged it MAJOR because the abstract repeats
  it.
- **Finding 3 may be less serious than labelled.** Main.tex l.835 ("classical steps are defined on
  every bit string … every implemented step is a channel on the full space") partly covers the
  missing assumption. The oracle sentence itself is still absent. A human may rate this MINOR.
- **I did not re-derive the 1H+ mathematics.** That was the core-plus referee's task. My `cor:plus-chain`
  check is a reading of the two proofs, not a re-derivation of their uses in `def:plus-schedule`.
- **The HSP23 mathematics is the helper's.** I re-ran its exact identities and checked findings 8.1
  and 8.3 against the sources. Finding 8.2 is UNKNOWN. Lemma E and Lemma 0's closed form were not
  re-derived by anyone in this pass.
- **The compile was a scratch copy.** It used the TeX Live 2020 on this machine. The page count and
  warnings match the repo's `main.log`.
- **Status.** Everything here is AI-checked, pending human review. No claim gate was touched, and
  `make_numbers.py` was not run.
