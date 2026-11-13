# Rees core: Schedule 1H+ subsection, edit list and compile check (draft, 2026-11-14)

AI-written drafting helper report, pending human review. No Git, no network. The real core folder
was not touched: `main-core.tex` still has its 08:17 timestamp. `numbers.tex` was not touched.
`make_numbers.py` was not run.

## Verdict

**DRAFT READY FOR INTEGRATION, but the merged write-up is UNREFEREED.** The deliverables are:

- the subsection `sec-schedule1hplus.tex` (labels `plus-*`);
- 56 snippet-anchored edits (`edits.md`), generated from the same data as `apply_edits.py`;
- one hand-added macro, `\ReesClassNinePlusExp{20}`.

Applied to a scratch copy of the core, they compile cleanly with pdfTeX (TeX Live 2020):

| | Baseline core | With the new section and edits |
|---|---|---|
| Pages | 57 | 68 (the section is pp. 30–39) |
| Undefined references | 0 | 0 |
| Overfull boxes | 0 | 0 |
| hyperref warnings | 0 | 0 |

Log: `2026-11-14-rees-schedule1hplus-draft/compile_check.log`.

Every component lemma comes from a draft that an AI referee graded PROVED WITH FIXES:

- the 21 draft: `headline-21-referee`, and recomputed in `headline-21-recompute`;
- the 20 draft: `headline-20-referee`.

All fixes are applied. The merged Definition `def:plus-schedule` and Theorem `thm:plus` are a new
text that no referee has read.

## Files (all in `research/audits/reviews/2026-11-14-rees-schedule1hplus-draft/`)

- **`sec-schedule1hplus.tex`**: the subsection, to be `\input` (or pasted) after "against degree $24$
  for Schedule~1 there)."
- **`edits.md`**: edits A1–Z3, old→new, each old snippet unique in the current core. The section
  numbers.tex at its top gives the macro.
- **`apply_edits.py`**: applies the same list to a scratch copy. It refuses a path containing
  `rees-hsp/core`, checks uniqueness, and writes `edits.md`.
- **`band_check.py` / `.out`**: thresholds and band cost of Thm plus(iv), in mpmath at 60 digits.
  The maximum is $3.371\cdot10^{14}$, at $\mathrm U_m$, which is below the stated $4\cdot10^{14}$.
- **`k7check.py` / `.out`**: for $523<p<9604$ with $p\equiv1\pmod 7$, $e_7=3$ everywhere. At
  29, 43 and 113, no $\mathrm U_m$ contraction exists for any $m$.
- **`crossover_plus.py` / `.out`**: the four small rows of `tab:query-crossover` under 1H+. The
  control run reproduces the core's table exactly.
- **`compile_check.log`**: the pdflatex log of the compile check.

## Claims and labels

- **Lemmas `plus-refine`, `plus-chain`, `plus-tensor`, `plus-ell-node`, `plus-stage`,
  `plus-finish`**: PROVED (AI, refereed in draft form).
- **Lemma `plus-sm`**: PROVED given Weil and Rabin. The Lidl–Niederreiter locator is unverified,
  as in the core.
- **Prop `plus-tables`**: exact computation. The tables were checked by four programs. They store
  $B(y)$ with $C_y=g^{y_1+\dots+y_\ell}B(y)$ (fix G1).
- **Thm `plus`**:
  - PROVED here: (i), (ii) and (iv) (AI, unrefereed in merged form).
  - Only argued: the clause $\sup_pK^+_\kappa<\infty$ in (iii).
- **Lemma `plus-exponent`(ii)**, $E_+(c)=3,5,9,10,14,16,18,20$ with the attainers $p\equiv1\pmod{2520}$
  and 37, 43, 73, 127, 181, 631: PROVED given the cited theorems and the exact computation of
  record (20-referee `run2_allB.out`).
- **Lemma `plus-exponent`(i)**, the lower bound $\lceil c/2\rceil^2+2\lfloor c/2\rfloor-13$: NEW
  here. Its proof is short (PROVED), but it is UNREFEREED.
- **Lemma `plus-exponent`(iii)**, $C^+_c=C_c$ for $c\le9$:
  - computed only for the first-draft schedule (`const_ref.py`);
  - the merged additions (TL6, (e), Tier B at all $p\le523$) are covered by a hand argument.
  - So it is NOT recomputed for the merged schedule.
- **Class-9 row of `tab:query-crossover` under 1H+**: NOT computed. It keeps the 1H count, which
  is an upper bound, and the caption says so.
- **1H+ at full depth** (the analogue of 95): NOT computed.
- **`rem:plus-is`** (S1 not needed for $\kappa\le9$): an unrefereed observation. Thm main keeps
  `thm:is-import` as a hypothesis.

## Material findings

1. **Deviation from the fragments: Tier B (d) is at every $p\le523$, not at 28 listed primes.**
   This is the "allB" variant. Availability is existence, which an exhaustive search decides. This
   resolves recompute F1, because the definition no longer points at artifact tables. The values
   match 20-referee `run2_allB.out` and recompute variant B.
2. **The certificate-check count was overstated in an earlier draft, and is now fixed** (section,
   proof of plus-exponent(ii)):
   - $\mathrm{TL}_6$ certificates had two independent checkers (`v2/verify_tl6_all.py` and the
     20-referee's `verify_tl6.py`);
   - the other steps had four.
3. **Theorem main now uses data at four primes.** These are the five $\ell$-level tables, at
   $p=13,19,37,73$. Edit M15 says so in the import sentence.
4. **The class-3 example changes** (X3–X5). It becomes $Q_q\le3(5+\tau)\cdot16\cdot15\approx2^{12.08}$
   (was $2^{17.68}$). This uses $(\mathrm{GE};\mathrm{TL}_3)$, which is available at every
   $p\equiv1\pmod3$; the gap list is empty.
5. **New rows for `tab:query-crossover`** (T3–T5):
   - filiform: 9.66 / 79 / 27 / 108;
   - free: 12.08 / 61 / 28 / 153;
   - Dixmier–Lister: 13.31 / 17 / none / 269.
6. **Wording that would otherwise become false**: rem:query-separation(b), outlook "Smaller
   arities" (37 is now above the proved 20), and "Halving at the confirmed depth" (Q2, U1–U3).
7. **Left unchanged on purpose:**
   - line ~623 ($A_4(2)=243$ at $p=5$): a true statement about 1H, whose 1H+ value was not
     computed;
   - the Heisenberg row: $A^+_2(1)=4$, argued.
8. **Length.** The section adds 11 pages. If space matters, the cost recursion in Thm plus(ii) and
   the constant argument of plus-exponent(iii) could move to the full version.

## Adversarial self-check

- **No program was written from the merged text.** I matched Definition `plus-schedule` against
  the 20-referee's `plus2.py` allB by reading only. A divergence would leave the 20 resting on a
  slightly different schedule. Examples: the (fΩ) finishes, $|\Omega_t|\le3$, union steps for
  every available $m$.
- **I reran none of the large computations.** These are the $2\cdot10^6$ sweep, the certificate
  checks and the tail classes modulo 5040; I cite their saved outputs. Finite checks only falsify.
- **The hand argument for $C^+_c=C_c$ is the weakest link.** It relies on computed facts about
  where degrees drop, and does not bound plans with large $s$ in general.
- **The availability bound in Thm plus(i) is impractical.** It is a $10^{46}$ exhaustive search,
  which proves only that a constant exists. Practical runs use certificates.
- **The lower bound (i) is new and has had no second reader.**
- **Every result here is AI-checked, pending human review.** No human has read Section 1H+.
