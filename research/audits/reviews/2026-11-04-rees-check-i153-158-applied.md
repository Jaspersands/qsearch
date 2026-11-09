# Rees paper: fixes from the i153-158 check, as applied

Date: 2026-11-04. Source report:
`research/audits/reviews/2026-11-04-rees-check-i153-158.md`. AI session
(Claude) applying the checker's fixes for the integrator. Before any edit, the
.tex files and `references.bib` were backed up to
`/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/bak-i159/`.
Files edited: `docs/papers/rees-hsp/main.tex`, `appendix-free-coordinate.tex`,
`appendix-schedule2.tex`, `appendix-torsion-blackbox.tex`, `references.bib`.
`main-full-draft.tex` was not touched. No git, no network, `make_numbers.py`
not run. This is not a human review.

Each fix was checked against the current text and the statements it cites
before it was applied. "applied" means the report's LaTeX was used as given.
"edited" means it was used with the changes noted.

| id | status | file | note |
|---|---|---|---|
| 1a | applied | main.tex | Overloaded-letter list extended by $b,L,M,P,D,\tau$, plus the $g_1,\dots,g_s$ vs $g_k$ clause. I confirmed the second meanings at Gate-level control, Lem `lem:qft-mod`, Thm `thm:free-coordinate`(i) and Thm `thm:uniform-compilation`(i). |
| 1b | applied | main.tex | The notation sentence now opens the Organization list ("at the end of this section"). The old sentence is removed. |
| 2a | edited | main.tex | Hybrid sentence: the reduced charge now covers only forward transforms on $\lvert0\rangle$, with the clause "in these circuits every transform with input $\lvert0\rangle$ is a forward one". I kept the old parenthetical in shortened form: "on that input the phase and phase-estimation steps of its proof are exact". I checked that `hybrid_budget` in `theorems/rees_circuit_qft_wire.py` restricts the reduction to `kind == "qft"`. The 18/124 zero-input counts were not re-run; they come from the report. |
| 2b | applied | main.tex | The two zero-input bounds are now in the statement of `lem:qft-mod`. I checked them: $3\pi2^{-\tau}\le\eta/(b+3)$ follows from the choice of $\tau$, and the inverse bound follows from $V^\dagger-U^\dagger=V^\dagger(U-V)U^\dagger$ applied to $u_N\otimes\lvert0\rangle$. One clause was added to the proof's $V^\dagger$ sentence so that the proof derives the second bound. "of the proof of Lemma" now reads "of Lemma" (merged into 2a). |
| 2c | edited | main.tex, references.bib | Cites `CuccaroDraperKutinMoulton2004` and `VedralBarencoEkert1996`. I checked that the generated adder (`cuccaro_add` in `theorems/rees_circuit_arith.py`) is CDKM's MAJ/UMA ripple, $2n\cdot3+1=6n+1$ gates. Changes from the report's text: (i) "the gate counts below are those of these constructions" now reads "counted from the generated gate lists of these constructions (`theorems/rees_qft_mod.py`)", since the counts are not derived in the paper; (ii) "the artifact checks both exhaustively for widths at most 6" now reads "checks the adder on every input of width at most 6 and the multiplier on all $x,y<N$, with two accumulator values, for $N\in\{3,\dots,27\}$". That is the scope stated in `2026-11-04-rees-qft-mod.md` section 4. |
| 2d | applied | main.tex | "for three subgroups" added. Matches qft-wire report l.187: $\langle e_2\rangle,\langle e_1\rangle,\langle e_1+e_3\rangle$. |
| 3a | applied | main.tex | Derivation of $P$ inserted. I rechecked it: $\sum_{k<g}2(g+1-k)=g(g+3)$, $\sum_{k<g}(g-1)(g-k)=(g-1)g(g+1)/2$, and $2n_F+2(g+1)\ell(e)$ equals the lemma's $P$. |
| 3b | applied | main.tex | Sentence on the uncounted coherent $\delta_s$ inserted right after the deferred-measurement sentence, not at the end of the paragraph. |
| 4a | applied | main.tex | Now points to Lem `lem:app-s2-gcd`(b). I checked that lemma: $t\ge1$, $td'\equiv1\pmod{q'}$, and the proof covers $u_b=0$, so the exponent is positive and the identity holds on all of $\Fp$. Its $t$ matches the remark's ($td/\kappa\equiv1\bmod (p-1)/\kappa$). The Lean row `ReesSdeGcd` cites the same lemma. |
| 4b | applied | main.tex | "free-coordinate" added to the caption of `tab:main-regimes`. |
| 4c | edited | main.tex | Defined once, after the $\square$ of the proof of Thm `thm:main`, before every use (Rem `rem:combined-schedule`, the discussion after Thm `thm:free-coordinate`, Cor `cor:fpt-r`(i), Prop `prop:mixed-schedule`). All four still read correctly. Beyond the report's list, the definition also names Thm `thm:rees-cover`, the two imports already named after Thm `thm:main` (subgroup Lazard, the QFT compilation) and Rem `rem:is-import`(b). Together these make it exactly the inputs of that proof, so it does not silently drop an import. The reduced-dependence sentence covers only what the report shows: Thm `thm:free-coordinate`(iii) at $p>c+1$, and hence Cor `cor:fpt-r`(i). The reason given is that a grade with $\kappa_d=p-1$ would have $d=p-1>c$, which is the argument of the proof of Cor `cor:fpt-r`(i). No result's stated conditions were changed. |
| 5a | applied (with optional sentence, edited) | main.tex | Date and status header now say 4 November. The optional history sentence was reworded so that it does not list contents that I did not inventory: "adds the class-five Lean modules and material from the AI-only checks and artifacts of 3--4 November ...; these are not a human review either." |
| 6a | applied | appendix-free-coordinate.tex | "$1\le e\le p-2$" added; cosmetic "If a node at a grade $d\in\Gamma_0$ is a zero-sum node" applied. |
| 6b | edited | appendix-free-coordinate.tex | The report's parenthesis takes "the first $a+\lceil\log_p(2/\tau)\rceil$ labels", but $a$ is unknown at that point, so the count would be circular. I used the public bound instead: "the first $g_d+\lceil\log_p(2/\tau)\rceil$ labels, with $g_d\ge a$ public". The probability bound still holds: $\Pr[\text{no span}]\le (p^a-1)/((p-1)p^{n})<p^{-(n-a)}\le\tau/2$ for $n\ge a+\lceil\log_p(2/\tau)\rceil$. $\tau$ is the one introduced later in the same item. |
| 7a | applied | appendix-schedule2.tex | "per distinct value of $\kappa_d$ ... every node whose grade has that value". |
| 8a | applied (optional; strict improvement) | appendix-torsion-blackbox.tex, main.tex | Tight form $O_c(s^c\ell^2(\ell+\log(s+1))^2)$ is now used in Prop `prop:tb-count-gates`(b), its proof and Thm `thm:bb-envelope`(iii). The exponent step now reads $s^c\ell^2(\ell+\log(s+1))^2\le N^{\max(c,4)+o(1)}$. I checked it via $s\ell\le N$ and $\log(s+1)\le N$. The conclusion $O_c(N^{E_W(c)+4+o(1)})$ is unchanged, since $E_W(c)\ge\max(c,5)$. No other occurrence of $s^c\ell^5$ remains in the paper sources. |

Counts: 16 findings (1 gap, 14 imprecisions, 1 cosmetic). 10 applied as given
(1a, 1b, 2b, 2d, 3a, 3b, 4a, 4b, 6a, 7a), 5 edited (2a, 2c, 4c, 5a, 6b), and
the optional 8a applied. None skipped.

## Build and test

- Built in
  `/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/build/`
  with `latexmk -pdf`: **131 pages**. The unedited backup gives 130 pages.
  No Overfull, no "Float too large", no undefined references or citations,
  and no LaTeX warnings. The only Underfull lines are the three known ones in
  `main.bbl`.
- `tests/tools/test_rees_paper_numbers.py`: **2 passed**.

## Decisions for the integrator

1. **Bib author names (2c).** The brief gave surnames only. I wrote the
   standard full names: Steven A. Cuccaro, Thomas G. Draper, Samuel A. Kutin,
   David Petrie Moulton; Vlatko Vedral, Adriano Barenco, Artur Ekert. I added
   no DOI, journal or page data beyond the brief. Please verify the names, or
   cut them to initials.
2. **4c scope.** The definition is wider than the report's list (see the row
   above). If you want the report's narrower list, delete Thm
   `thm:rees-cover`, the import clause and the Rem `rem:is-import`(b) clause.
   Not done: Cor `cor:fpt-r`(ii), with the zero-sum node at $p=c+1$, also
   makes no Schedule 1 call. The report does not show this, so I did not
   state it.
3. **6b.** Choose between my $g_d$-based label count and the report's
   fallback, which states (a) for known $a$ only.
4. **5a.** The optional history sentence is worded generically. Replace it
   with a precise list if you want one.

I looked for the issue of 4a and 6a elsewhere, a Euclid exponent
$\alpha\le0$ applied to a zero entry. The free-coordinate appendix does not
have it: (F4) (l.66) and the split node (l.365) set $s=\sigma^\alpha$ only
where $\sigma\ne0$, and $s=0$ elsewhere. Nothing to change there.
