# Referee 15 (Fable) applied to the Rees paper

Date: 2026-11-05. Input: `2026-11-05-rees-referee-15-fable.md` (0 Error, 2 Gap,
7 Imprecision, 3 Style). Integrator: one AI session; AI-checked, pending human
review. Integration-log row I222. The Gate-level control paragraph was not
touched. No table number, `numbers.tex`, $E_W$, the exponent 143 or claim gate
changed. No git, no network.

Each finding was checked against the current `.tex` text and, where it cites
one, the source report (`2026-11-05-rees-threshold-9.md` Remark 5 and §2.4,
`-threshold-9-check.md` §3, `-application-4.md` §2.1). Edits were exact-string
replacements with count asserted 1 (2 for the repeated "use exactly $\rho$
runs"), dry-run first on scratch copies; backups are in the session
scratchpad (`ref15/backup/`).

| Finding | Verified | Action |
|---|---|---|
| G1 (Gap) `main.tex` sentence after `thm:free-coordinate` | Yes. Part (iii) allows the zero-sum node (search up to $p^{g_d}$) at $\kappa_d = p-1$; `rem:fc-witness-h3`(c) uses the node of `rem:fc-zero-sum-arity`(b) at $\Gamma_0$. | Applied, improved. The sentence now says a grade with $\kappa_d = p-1$ uses that node or Schedule 1 rather than the zero-sum node. The referee's closing parenthesis is replaced by the observation that at $c = 9$ no grade has $\kappa_d = p-1$ ($p \ge 11$), so the exponent 19 is the same for both choices. One sentence was also added to `rem:fc-witness-h3`(c) (`appendix-free-coordinate.tex`) so that the proof covers the Schedule 1 option. Schedule 1 never aborts, and for fixed $c$ its arity $B_d(g_d)$ and its time (`rem:is-runtime`) are polynomial. The exponents $E$ still use the (b) node. |
| I1 (Imprecision) `main.tex` version note | Yes. `ReesSdeSolver`, `ReesMergeReduction`, `app:s2-chains`, `app:s2-local`, `rem:app-s2-joint-moments`, `rem:sde-worst-case`, `rem:fc-zero-sum-arity`, `rem:fc-witness-h3`, the composite run counts and the application-4 paragraph (Theorem W of the report) were all missing. | Applied, adjusted. The two modules are named, and `lean-sde-solver.md` is cited. The note says "restart variant and its run counts", since there is one variant, and calls Theorem W "the fourth application search after Remark `rem:filters`", because the paper does not use the name Theorem W. |
| G2 (Gap) `appendix-schedule2.tex` `rem:app-s2-joint-moments`, barrier step | Yes. The parenthesis was the whole argument, and Remark 5 was not cited. | Applied, corrected. Remark 5 is added to the citation list. The referee's "after a change of $\eta_m$ by a constant factor" is **rejected**: Remark 5 step 4 gives $\rho_a\rho_b(1+\eta_a)(1+\eta_b) \le \rho_m(1+0.4\eta_m) \le \rho_m(1+\eta_m)$, so the brackets themselves contain the products, and the check report confirms this (largest ratio $0.067\eta_m$). New text: under independent copies the BGP law gives these moments the values they have there, as sums over compositions of products of one-column moments. Remark 5 argues, and its check re-derives, that for $\eta_m<1$ these lie inside the $S$-brackets, via $\rho_a\rho_b \ge \rho_{a+b}$ and superadditivity of $E_\kappa(\cdot,p)$. The text says this step is not proved here, and the conclusion is stated as "granting it". |
| I2 (Imprecision) core: chains and Schedule 2 arity | Yes. $\binom{4}{3} = 4 < 2\kappa$ at $a = 1$ for $\kappa \ge 4$. | Applied as given ("for large $a$"). |
| I3 (Imprecision) core: Theorem W needs a known bound $\hat\delta$ | Yes. `main.tex` assumes "a bound $\hat\delta \ge \delta(F)$ is known" and drops the promise only for polynomially bounded $p$. | Applied, reworded. It now takes a bound $\hat\delta \ge \delta$ with $p > \max(\nu-1,2)\hat\delta$, and for polynomially bounded $p$ the largest admissible $\hat\delta$ can be used. $\nu$ is defined as in I4. |
| I4 (Imprecision) `main.tex` application-4 paragraph: $\nu$ | Yes. The proof uses $A^\nu = 0$ for each $A$ (report §2.1: "so $A^\nu = 0$ for every $A \in L$"). | Applied as given. |
| I5 (Imprecision) `main.tex` `rem:two-level-threshold-size`: divisor $D$ | Yes. `lem:app-s2-divisor` assumes $D \ge 2$. | Applied as given. |
| I6 (Imprecision) core: threshold $\kappa^{\kappa+o(1)}$ out of date | Yes. The companion states $6\kappa^\kappa+1$ for $\kappa \ge 729$, conditional on the threshold-2 Theorem 5 bound, with a $\kappa^\kappa/2$ barrier. | Applied, with the status kept as "argued": "argued in reports, conditional on a central-moment bound argued in one of them, and not proved in the full version; the method behind it cannot go below $\kappa^\kappa/2$". |
| I7 (Imprecision) `main.tex`: "no certificate built only from those moments" | The point is right but the proposed fix is not. The appendix brackets cover every $S$, including $\lvert S\rvert = \kappa$, at orders $m \le \kappa-2$; they are not brackets "of at most $\kappa-1$ columns", and the check report calls "certificates built from moments of at most $\kappa-1$ columns" "not a theorem". | Applied, reworded to the appendix's precise form: "this method cannot push below $\kappa^\kappa/2$, since there no lower bound valid for every law of the column counts that satisfies the same Weil-controlled moment brackets is positive". |
| S1 (Style) missing space after a period | Yes. | Applied (combined with I7). |
| S2 (Style) $\rho$ for the run count in `rem:is-runtime` | Yes, it clashes with $\rho_H$. All five occurrences are in the remark. | Applied: $\rho \to r_{\mathrm{run}}$ at all five. Core has no run-count text. |
| S3 (Style) "the report shows" for a mixed proof | Yes. Threshold-9 §2.3: conditions (A)–(C) are checked by `verify_corollary.py` for $729 \le \kappa \le 10^6$, with estimates for $\kappa > 10^6$. | Applied as given. |

Core (`core/main-core.tex`) contains none of the G1, I1, I4, I5, I7, S1–S3 or
G2 text, so only I2, I3 and I6 apply there.

Checks. Scratch builds (copies under `$TMPDIR/ref15build`): `main.tex` exit 0,
176 pages, 0 Overfull, no undefined references or citations, no "Float too
large"; `core/main-core.tex` exit 0, 28 pages, 0 Overfull, no undefined
references or citations, no "Float too large".
`pytest -q tests/tools/test_rees_paper_numbers.py`: 2 passed. `make_numbers.py`
not run. Nothing committed.
