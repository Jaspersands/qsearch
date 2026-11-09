# Referee 17 (core version) applied to the Rees core paper

Date: 2026-11-05. Input: `2026-11-05-rees-referee-17-core.md` (0 Error, 2 Gap F1–F2,
16 Imprecision F3–F15, F19, F21, F22, 4 Style F16–F18, F20; Section 5 lists seven
statements stronger in the core than in the companion). Integrator: one AI session;
AI-checked, pending human review. Integration-log row I227. No table entry, `numbers.tex`,
macro, claim gate (`research/reductions/rees_hsp_reduction.json`) or `docs/outreach/` file
changed. No network; `make_numbers.py` not run. Every "AI-checked, pending human review"
label and every `NEEDS HUMAN VERIFICATION` comment kept; one more restored (F7).

Files edited: `docs/papers/rees-hsp/core/main-core.tex` (24 changed lines);
`docs/papers/rees-hsp/references.bib` (Olson1969 appended, copied byte for byte from
`core/references.bib`); `docs/papers/rees-hsp/main.tex` (one `\cite{Olson1969}` added where
it already names "Olson's theorem for abelian $p$-groups"). Edits were located by text, not
line number. Backups: scratchpad `main-core.orig.tex`, `main.orig.tex`,
`references.orig.bib`.

## Checks done before editing

- **F1.** The guard sentence exists only in the core. `main.tex` has no controlled-oracle
  guard (its merge primitive is "the identity on invalid words"), so the companion needed
  no change. The referee's argument holds: Lemma `lem:hybrid` compares the steps only on
  ideal states supported on the canonical subspaces, where any unitary extension of $U_f$
  equals $U_f$ ($\eta_j = 0$), and the implemented suffix only has to be a channel.
- **F5.** Recomputed with the formula of Proposition 7.4(v) ($t = 1$, $16\lceil\ln 6\rceil = 32$),
  first integer $p$ with $Q \ge Q_{\mathrm q}$: with $8\ell$ rounded up to $15$ (as
  `birthday_crossover.py` does) 84, 119671, 42290, 638, the printed values; with
  $8\ell = 8\ln 6$ itself 86, 121497, 42773, 642, the referee's values. The largest primes
  below the latter are 83, 121493, 42767, 641, exactly the companion caption's "primes up to
  ..." values. Both conventions agree; the note now gives both readings.
- **F6 / Section 5 item 1.** Re-derived the memoized count: at step $j$ compute
  $W^{(k)}_j$ for $k = 1,\dots,d-1$ from $Z_0,\dots,Z_j$ and $W^{(k-1)}_{\le j}$, each with
  $j+1$ brackets, total $(d-1)d(d+1)/2$. The core's proof is correct, and prime factors
  $\le d$ is right since every denominator is $\le d$ or a von Staudt–Clausen prime $q \le d$.
  Decision: keep the core's proved count and say that the artifact and the companion use the
  unmemoized $(d-1)d(d+1)(d+2)/6$. The companion is not changed: its "exactly ... for the
  implemented recurrence ... Optimized schedules may use fewer" is consistent with this.
- **F7.** The companion does claim operator-norm isometry error for Kitaev's construction
  (`main.tex` Theorem `thm:uniform-compilation`(iii)), so the core's item (iii) statement
  stays. The sentence "All internally controlled phase gates are synthesized with their
  relative phases, so the bound is on the isometry $CJ$, not only on output probabilities"
  is not in the companion and was removed. The companion's `NEEDS HUMAN VERIFICATION`
  comment on the Kitaev and Cleve–Watrous locators was restored, with a visible hedge and
  a pointer to the companion's explicit Lemma `lem:qft-mod`.
- **F19.** Core cites 29 keys; all are in `core/references.bib`. Before: only Olson1969 was
  missing from the master. After appending it, every one of the 37 core entries is in the
  master with identical text (scripted comparison). The 13 master-only entries are not cited
  by the core. Eight core entries are not cited by the core, so the Appendix A note says
  "every entry appears, identically" rather than "the subset cited here".
- **F22.** Opened `research/reductions/rees_nongradable_control.json` and
  `theorems/rees_nongradable_control.py`: 32 certificates, entries 0–31 of the row-major
  matrix $D[\text{output},\text{input}]$ (the $e_1,\dots,e_4$ components of
  $De_1,\dots,De_8$), multipliers in $\{1, 3, 6\}$, each verified by integer replay in the
  generator. The text now says what a certificate is.
- **F11.** The exponent-$p$ step is valid: a cyclic quotient of exponent $p$ has order
  $\le p$, index 1 would make $G$ abelian, index $p$ is excluded.

## Findings

| Finding | Verified | Action | Final text (changed part) |
|---|---|---|---|
| F1 (Gap) guard on oracle calls, start of Section 6 | Yes | Applied as proposed. Core only; companion has no such sentence. | "The oracle $U_f$ is specified only on canonical encodings. We assume, as is standard, that the supplied black box is some unitary on the whole register space that agrees with $U_f$ on canonical inputs; which unitary is irrelevant, because Lemma `lem:hybrid` compares each implemented step with the ideal one only on ideal states, which are canonical, and otherwise needs only that every implemented step be a channel on the full space. No guard or controlled oracle call is needed." |
| F2 (Gap) AI-only import of Ivanyos–Santha | Yes (the hedges exist; the restructuring is a scope decision) | **Restructuring deferred to owner.** One sentence added at the end of Remark `rem:is-printed`. | "In particular, the explicit arity $B_d$ of (eq:Bd), and with it the query count of Theorem `thm:main` and the exponent $\ReesClassNineQueryExp$ at $c = \ReesClassNineClass$, rest on this AI-only reading of [IvanyosSantha2015], which needs human confirmation against the source." |
| F3 (Imprecision) Lemma `lem:copy-lift` | Yes; proof uses Lemma `lem:homogeneous`; companion has the hypothesis | Applied as proposed. | "Let $s_1,\dots,s_c \in \Fp^\times$ be distinct. Exactly $c$ fresh copies ..." |
| F4 (Imprecision) abstract | Yes (Section 3.4 proves it over $\Fp$, $p > 3$) | Applied as proposed. | "admits no positive grading over $\Fp$ for any $p > 3$." |
| F5 (Imprecision) Table 1 caption, column (v) | Yes (see checks) | Applied, extended with the companion's prime reading. | "...uses fewer than $Q_{\mathrm q}$ queries; this column is computed with $8\ell = 8\ln 6 \approx 14.33$ rounded up to $15$, which only enlarges $Q$, so the listed values are conservative (with $8\ell$ itself they are $86$, $121{,}497$, $42{,}773$ and $642$, so the thresholds are the primes up to $83$, $121{,}493$, $42{,}767$ and $641$)." |
| F6 (Imprecision) Theorem `thm:uniform-compilation`(i) | Yes (see checks) | Applied, reworded: core's count kept, qualifier and artifact clause added. | "at most $(d-1)d(d+1)/2$ bracket evaluations when the coefficients $W^{(k)}_o$ of the recurrence in the proof are stored and reused (the recurrence without this reuse, which the artifact `theorems/uniform_bch_rees.py` implements and the full version counts, uses exactly $(d-1)d(d+1)(d+2)/6$), each costing ..." |
| F7 (Imprecision) proof of (iii), Kitaev | Yes (see checks) | Applied, reworded: the phase/isometry sentence removed, not kept; flag restored. | "... A logarithmic-depth alternative is sketched in [CleveWatrous2000, Section 7.1]. The locators in [Kitaev1995] and [CleveWatrous2000] have not been checked by a human; the full version (Appendix `app:artifacts`) also gives an explicit construction of the Fourier transform over $\mathbb{Z}/N$, for odd $N$, with the same operator-norm guarantee on the canonical subspace and an explicit gate count (AI-checked, pending human review), which does not depend on this reading of [Kitaev1995]." plus comment `% NEEDS HUMAN VERIFICATION (as in ../main.tex): Kitaev1995 "Section 5, Theorem 2 and eq. (25)" and CleveWatrous2000 "arXiv version, Section 7.1" not checked offline (referee 12, 2026-11-04).` |
| F8 (Imprecision) hybrid application, non-canonical labels | Yes | Applied as proposed. | "Classical steps are defined on every bit string: a label coordinate holding a value $\ge p$ is reduced modulo $p$ before the solver runs, so every implemented step is a channel on the full space." |
| F9 (Imprecision) Definition `def:input-contract`(i) | Yes | Applied, reworded as a promise (the companion says "genuine structure constants"; no rejection step added to the algorithm). | "... of class at most $c$ (a promise; antisymmetry, the Jacobi identity and $\gamma_{c+1}(\mathcal{L}) = 0$ can be checked in time polynomial in $m$ and $\log p$);" |
| F10 (Imprecision) "makes $Q_{\mathrm q}$ queries" | Yes | Applied, also to copies. | "it makes at most $Q_{\mathrm q} = \dots$ queries in case (a), or uses at most $Q_{\mathrm q}$ copies in case (b)" |
| F11 (Imprecision) abelian-by-cyclic | Yes | Applied as proposed. | "So $G$ has no abelian subgroup of index $p$. Since $G$ has exponent $p$, every cyclic quotient of $G$ has order at most $p$, so $G$ has no abelian normal subgroup with cyclic quotient: it is not abelian-by-cyclic." |
| F12 (Imprecision) "special cases" | Yes | Applied, reworded to fit the sentence. | "So, when $p > c$, the instances treated by these results are instances of the setting of Theorem `thm:main` (for $p$ at most the class, ...); this compares scope only, we do not compare running times, and the bounds of those papers are not implied by ours. The growing-prime, fixed-class feature is not new by itself." |
| F13 (Imprecision) Theorem `thm:is-import` time | Yes | Applied as proposed. | "in time polynomial in $M$ and $\log p$, where the polynomial depends on $d$." |
| F14 (Imprecision) bijectivity of $\delta_\theta$ | Yes; companion has it | Applied as proposed. | "..., is bijective with inverse $\delta_{\theta^{-1}}$, and ..." |
| F15 (Imprecision) Lemma `lem:instrument` proof | Yes | Applied as proposed. | "In the application to $G = G_d$ (Section `sec:recursion`), $z$ is central, so $x \ast (-z) = x - z$ in coordinates and $R_z$ is a subtraction on the top-grade coordinates." |
| F16 (Style) diamond norm unused | Yes (only occurrence) | Applied. | "Trace distance is $\frac12\|\cdot\|_1$." |
| F17 (Style) vacuous grades | Yes | Applied ("would suffice"; Theorem 1.3 keeps $M_d = B_d(g_d)$). | "(if $g_d = 0$, which happens when the class of $\mathcal{L}$ is below $d$, the stage is vacuous and $M_d = 1$ would suffice; the counts below keep $B_d(0)$ for uniformity)" |
| F18 (Style) boilerplate in `\date`; Outlook length | Yes | Date: applied as a `\thanks` footnote. **Outlook cut to half a page deferred to owner**; the proposed new Section 8 opening, part of that cut, not applied. | `\date{5 November 2026\thanks{Core version. All results are AI-checked, pending human review; see Section~\ref{sec:status}.}}` |
| F19 (Imprecision) bib drift | Yes (see checks) | Applied: Olson1969 added to the master and cited in `main.tex`; Appendix A item added. | "Bibliography: every entry of `core/references.bib` appears, identically, in `docs/papers/rees-hsp/references.bib`." `main.tex`: "(Olson's theorem for abelian $p$-groups~\cite{Olson1969})". |
| F20 (Style) invisible hedge on van de Woestijne | Yes | Applied, reworded: locator not resolved offline, so a visible hedge; comment kept. | "... sum of at most $d$ $d$-th powers (the section locator in [vandeWoestijne2005] has not been checked by a human)." |
| F21 (Imprecision) register bound | Yes | Applied as proposed. | "Depth-first evaluation of the recursion tree, with every consumed target and every oracle label register measured and reset as soon as it is traced out, stores at most ..." |
| F22 (Imprecision) row certificates | Yes (artifact opened) | Applied, wording adjusted to the artifact. | "$\DlRowCerts$ integer row certificates, each an integer combination of the derivation equations equal to $1$, $3$ or $6$ times one of the $32$ coefficients of $e_1,\dots,e_4$ in $De_1,\dots,De_8$, show that ..." |

Section 5 items: 1 → F6; 2 → F3; 3 → F10; 4 → F12 (the "What may be new" wording kept;
Section 1.6 already says no expert has assessed novelty); 5 (Remark 7.5 heading) → kept,
the referee calls it acceptable; 6 → F7; 7 → F5.

Rejected: none. Reworded: F5, F6, F7, F9, F10, F12, F17, F19, F20, F22. Deferred to owner:
F2 restructuring, F18 Outlook cut.

## Owner decisions (not applied)

1. **F2, abstract arity.** The referee asks to restate Theorem 1.3 with an abstract arity
   function $A_d$ and move $B_d$, the displayed bound and the exponent 145 into a corollary
   "with the Ivanyos–Santha solver", or else to get a human (ideally the source's authors) to
   confirm the reading of arXiv:1503.09016v2, including the claim that its printed Theorem 3
   bound is not what its proof gives. The referee calls this the change most likely to
   decide acceptance. Not done here: it restructures the main theorem in both papers. The
   one-sentence statement above is in place meanwhile.
2. **F18, Outlook.** Cut Section 8 to about half a page (one or two sentences per item, one
   pointer each to the full version) and drop the per-sentence status tags in favour of
   Section 1.6. Not done: it removes content and status labels the owner asked to keep.

## Build and test

- Core (scratchpad `build_r17core`, `latexmk -g -pdf`): exit 0, **28 pages** (27 before, per the referee),
  0 Overfull, no undefined reference or citation, no "Float too large", BibTeX 0 warnings.
- Companion (scratchpad `build_r17main`): exit 0, **177 pages**, 0 Overfull, no undefined
  reference or citation, no "Float too large", BibTeX 0 warnings; Olson1969 in `main.bbl`.
- `pytest -q tests/tools/test_rees_paper_numbers.py`: 2 passed.
- New LaTeX uses no `\mathsf`, `\mathrel`, `\begingroup`, `\aa` or `\ni`.
