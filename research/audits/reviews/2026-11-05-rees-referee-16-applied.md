# Referee 16 (overnight pieces) applied to the Rees paper

Date: 2026-11-05. Input: `2026-11-05-rees-referee-16-overnight.md` (0 Error, 0 Gap,
6 Imprecision F1–F3, F5–F7, 4 Style F4, F8–F10). Integrator: one AI session; AI-checked,
pending human review. Integration-log row I226. No table, `numbers.tex`, $E_W$, the
exponent 143, claim gate or `docs/outreach/` file changed. No git, no network;
`make_numbers.py` not run.

Each finding was checked against the current `.tex` text (located by text, not line
number) and, where relevant, the source report: `2026-11-05-rees-is-restarts.md` §1–2
(Lemma 1: the classifier holds $\eta \in H_\pi$; "at most one run, and no restart, when
κ is prime"; (iii) general κ), `2026-11-05-rees-is-restarts-composite.md` §0 (Theorem A,
$r_{\mathrm{run}}$ for every κ ≥ 2), `2026-11-05-rees-application-4.md` Steps 3–6 (the
$1-\hat\delta/p \ge 1/2$ Schwartz–Zippel step), and the text of
`rem:app-s2-joint-moments` ("this step is not proved here. Granting it, ...").
Edits were exact-string replacements with count asserted 1
(scratchpad `apply_r16.py`); backups in scratchpad `r16_backup/`.

| Finding | Verified | Action | Final text (changed part) |
|---|---|---|---|
| F1 (Imprecision) `appendix-schedule2.tex` `rem:app-s2-tower-scope` | Yes. The proof of `lem:app-s2-refine` needs $\beta_{i(b)}$, i.e. every input class in $R$; the union variant only replaces "$c^\nu_{b_\nu} = 1$". | Applied, reworded slightly. | "keep $\alpha_0 + \beta_0 \in Q^{(D)}_0$, keep the requirement that the $D$-classes of the inputs lie in $R$, and ask the inputs, in place of a coefficient equal to $1$, only for one coefficient of class $0$." |
| F2 (Imprecision) `appendix-schedule2.tex` `rem:app-s2-joint-moments`, opening | Yes. The range $\Lambda \ge \sqrt{8\kappa}$ rests on the threshold-2 Theorem 5 bound (not proved here), and the remark later says "If that bound is right". | Applied, reworded (shorter than proposed; the proposed "the part this remark reproduces is ... its consequence for $6 \le \Lambda \le \sqrt{8\kappa}$" is not used, because the remark says "the report shows" that range rather than reproducing it). | "costs a factor of order $\kappa$ in the threshold, and the cited reports argue that for large $\kappa$ most of this loss can be removed, conditionally on the central-moment bound cited below (...)" |
| F3 (Imprecision) `main.tex` `rem:two-level-threshold-size` | Yes. The barrier needs the step marked "not proved here. Granting it" in the appendix. The appendix's own lead sentence "The method cannot go much lower." was also flat, so it was hedged too. | Applied, reworded; also appendix and core. | main: "... an $O(\kappa^\kappa)$ threshold. It is also argued, and not proved here, that this method cannot push below $\kappa^\kappa/2$, since below $\kappa^\kappa/2$ no lower bound valid for every law of the column counts that satisfies the same Weil-controlled moment brackets is positive (Remark `rem:app-s2-joint-moments`; AI-checked, pending human review)." Appendix: "The method cannot go much lower, granting one step argued in the reports." Core (Schedule 2 paragraph): "...; the reports also argue that the method behind it cannot go below $\kappa^\kappa/2$)". |
| F4 (Style) `appendix-schedule2.tex` proof of `prop:app-s2-cyclotomic`(i) | Yes. $x = 0$ gives $z = -y \in Q_{b+\varepsilon}$; $b-\varepsilon$ is right only because $2\varepsilon = p-1 \equiv 0 \pmod\kappa$. The later "$c \ne b-\varepsilon$ into $v \ne \varepsilon$" then reads correctly. | Applied as given. | "possible with $x = 0$ exactly when $c = b + \varepsilon = b - \varepsilon$ (as $2\varepsilon = 0$ in $\mathbb{Z}_\kappa$, since $(-1)^2 = 1$), with $y = 0$ ..." |
| F5 (Imprecision) `main.tex` `rem:is-runtime` | Yes. Lemma 1 and Theorem A define and bound the variant for every κ ≥ 2; the text introduced it only for prime powers but later bounds it "for every $\kappa_d \ge 2$". The sentence "Each restart multiplies $\lvert\langle\eta\rangle\rvert$ by at least $q$" is prime-power-specific, so it now starts "If $\kappa = q^e$". | Applied, reworded (merged with F6). | "The following deterministic variant is defined for every $\kappa \ge 2$; when $\kappa = q^e$ is a prime power it makes at most $e \le \log_2\kappa$ runs, and a single run, never repeated, when $\kappa$ is prime, and for general $\kappa$ it makes at most $r_{\mathrm{run}}$ runs, defined below (AI-checked, pending human review)." and "If $\kappa = q^e$, each restart multiplies ...". |
| F6 (Imprecision) same sentence, "with no restart" | Yes in the paper's own wording: the next sentences call the trigger "a restart [that] enlarges $\eta$" and then check; for prime κ a trigger can occur, and the check then succeeds, so no second run starts (report: "the single run is never repeated"). | Applied, reworded (shorter than proposed). | "a single run, never repeated, when $\kappa$ is prime" |
| F7 (Imprecision) `main.tex` `rem:is-runtime`, $\nu+1$ | Yes. A subgroup of a cyclic group of order dividing $p-1$ can be enlarged $\Omega(\log p)$ times; the bound $\nu$ needs $\langle\eta\rangle \le H_\pi$ (report §1: "The classifier holds $\eta \in H_\pi$"). $H_\pi$ was defined only in the next sentence, so the two sentences were swapped. | Applied, reworded. | "Let $\pi$ be the set of primes dividing $\kappa$, let $H_\pi$ be the Hall $\pi$-subgroup of the cyclic group $\Fp^\times$, whose order has exactly $\nu$ prime factors counted with multiplicity, and call ... its $\pi'$-part. The algorithm of Theorem `thm:is-import` makes at most $\nu+1$ runs, since each restart of [IS, Section 3.1] strictly enlarges a subgroup of $H_\pi$." |
| F8 (Style) `main.tex` application-4 paragraph | Yes. Exactness (report Steps 2–5) needs $(\nu-1)\hat\delta < p$ and $\hat\delta < p$; Step 6 needs $1-\hat\delta/p \ge 1/2$. The referee's parenthetical "the first term makes the Lie method exact" omits $\hat\delta < p$, so it was corrected. | Applied, reworded; notation note added. | "that $p > \max((\nu-1)\hat\delta, 2\hat\delta)$ (exactness below needs only $p > \max((\nu-1)\hat\delta, \hat\delta)$; the factor $2$ is used by the randomized kernel computation)"; and after the nilpotency index: "; in this paragraph $\nu$ and $D$ have these meanings". |
| F9 (Style) `appendix-free-coordinate.tex` `rem:fc-witness-h3`(a) | Yes; re-derived: $\ell_\infty$ Minkowski in the index-$p$ lattice $\mathfrak p$ gives $\lVert v\rVert_\infty \le p^{1/\varphi}$; rounding against $v\zeta_h^i$ leaves $\ell_1$-norm $\le \tfrac12\varphi c_h\lVert v\rVert_1 \le c_h\varphi^2p^{1/\varphi}/2$; $2^{j-1}$ positive and $2^{j-1}$ negative terms give the $+1$. | Applied, lightly reworded ("the image of", "at most" twice, indexed basis). | "... powers of $\zeta_h$, and conversely $D_j$ contains the image of every signed sum with at most $2^{j-1}$ positive and at most $2^{j-1}$ negative terms; for the upper bound, Minkowski's theorem gives $v \ne 0$ in the degree-one prime $\mathfrak{p} = (p,\zeta_h-\omega)$, $\omega \in \Fp$ of order $h$, with $\lVert v\rVert_\infty \le p^{1/\varphi(h)}$, and rounding against the basis $(v\zeta_h^i)_{0 \le i < \varphi(h)}$ of $(v) \subseteq \mathfrak{p}$ gives every residue a representative of $\ell_1$-norm at most $c_h\varphi(h)^2p^{1/\varphi(h)}/2$." |
| F10 (Style) `appendix-free-coordinate.tex` `rem:fc-witness-h3`(b) | Yes. $\sigma_p + 1 \le \lceil 2\log_2(p-1)\rceil + 5 < 2\log_2 p + 6$. | Applied (first option). | "$M_d = O((2\log_2p+6)^{j^*_h}g_d^{\,1+j^*_h}\log(1/\tau))$" |

Rejected: none. Reworded: F2, F3, F5–F9 as noted. `core/main-core.tex`: only F3 (one
clause); it has no $r_{\mathrm{run}}$/restart-count text (its "there are no restarts"
concerns the fixed quantum allocation of Schedule 1, unchanged), no cyclotomic, Minkowski
or Theorem W hypothesis text of the affected form.

New LaTeX uses no `\mathsf`, `\mathrel`, `\begingroup`, `\aa` or `\ni` (the pre-existing
`K \ni 0` and `E^{\mathsf T}` occurrences were not touched). All "AI-checked, pending human
review" labels kept.

## Checks

- Full paper (scratch copy `build_r16`, `latexmk -g -pdf`): exit 0, **177 pages**,
  0 Overfull, no undefined references or citations, no "Float too large".
- Core (scratch copy `build_r16_core`): exit 0, **28 pages**, 0 Overfull, no undefined
  references, no "Float too large".
- `tests/tools/test_rees_paper_numbers.py`: 2 passed.
