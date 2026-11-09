# Referee report 14 (unanchored, adversarial): the Rees HSP paper

Date: 2026-11-05. Reviewer: an AI session (Claude Fable 5.1), unanchored: the
paper was read in full before any project note. Nothing in this report is a
human review. Scope: `docs/papers/rees-hsp/main.tex` (1417 lines) and the six
`appendix-*.tex` files it inputs, `references.bib`, and the integration log rows
I190--I211 of `research/audits/reviews/2026-11-02-rees-integration-log.md`.
Method: full read of `main.tex`; the appendices were read in three parallel
adversarial passes briefed on the same questions (Appendix A with the 4--5
November subsections; Appendices B and C; Appendices D--F plus Sections 8--9),
whose numerical reproductions are recorded below. A scratch build of the paper
(`latexmk -g -pdf`) in the session scratchpad compiled cleanly: 167 pages, no
undefined reference or citation, no multiply-defined label, no overfull box
reported in the log. No repository file other than this report was edited.

## Referee summary

**Recommendation: major revision; not acceptable in its present form.**

Reasons, in order of weight.

1. The paper does not vouch for its own main result. Theorem 1.2 (`thm:main`)
   is labelled "Proposed", its proof "AI-checked, pending human review", and
   its one imported ingredient, Theorem 4.4 (`thm:is-import`), is a reading of
   Ivanyos--Santha that the paper says was "checked against arXiv:1503.09016v2
   by AI sessions only" and that includes the claim that the bound printed in
   the source's Theorem 3 does not follow from its proof (Remark 4.5(c)). A
   referee for a theory venue cannot certify a theorem the authors present as
   unverified; the honest labelling is to the paper's credit, but it is also a
   statement that the manuscript is not ready. Every other result carries the
   same label (88 occurrences of "AI-checked" in `main.tex`, 33 in the
   appendices). The mathematics I could check in the main chain (Theorem 2.1,
   Lemmas 2.2, 2.5, 3.1, 4.3, Proposition 4.1, the error split, the proof of
   Theorem 1.2, Proposition 4.9) is correct as written; the gaps found are in
   the appendices and the new remarks, and are listed below.

2. The document is a project log, not a paper. 167 pages, of which the body is
   66; 184 `\file{...}` repository paths in the body; 13 "previous version" and
   8 "withdrawn" passages inside theorem sections; a 38-line status box that is
   a changelog; three remarks of about four pages in Section 4.3 (4.11--4.13)
   that "nothing else in the paper uses"; five paragraphs of about five pages
   in Section 5.1 describing finite simulations backend by backend; 20
   `% NEEDS HUMAN VERIFICATION` comments. A referee cannot locate the claims
   that matter. Concrete cuts and moves are in the Style section; they would
   bring the body to about 35--40 pages without losing a theorem.

3. The schedules are consistent. Every arity, threshold and cost bound of
   Schedules 1--3, the combined rule, `tab:main-regimes` and `E_W(c)` was
   checked against its defining statement and, where numerical, recomputed:
   `E_W(c) = 5, 11, 23, 38, 56, 77, 107, 143` for `c = 2..9` with witnesses
   `p = 3, 7, 13, 61, 61, 421, 2521, 2521`, the Schedule 1 exponent `145` at
   `c = 9`, "unchanged for `c <= 7`, falls by two for `c = 8, 9`", the
   `tab:query-crossover` entries `9.00` and `27.76`, `B_3(2) = 531441`,
   `B_4(2) ~ 3.7e16`, the Schedule 3 constants of Theorem 4.8(i)--(iv), the
   thresholds `T_A`, `T_S`, the tower and chain arities and thresholds, and the
   `E_2(kappa)` data quoted in the text all agree. One quoted number is
   attributed to the wrong threshold (Error 1).

4. Overstatement: none found. The paper claims no speedup ("We claim no
   speedup for any concrete problem", l. 1314), no novelty ("may be new, and
   this has not been established", l. 134), no human review, no implemented
   coherent receiver (ll. 368, 848, 920), no general SDE solver (l. 640), no
   checked formal compiler (l. 1392). Two small factual inconsistencies remain
   (the title date; the Lean class-seven scope versus `formal/README.md`).

Verdict on the integration rows I190--I211: all 22 insertions were located and
read; each carries a status label; none claims novelty, speedup or review. The
problems with them are notation (the new remarks reuse `H`, `K`, `c`, `E`,
`G`, `m`, `r`, `L` with new meanings) and placement.

## Top 5 findings

1. **Error** `main.tex:674`: the values `3781` and `30823` are attributed to
   the closed-form chain threshold of Corollary `cor:app-s2-union-chain`,
   whose values are about `2.2e5` and `1.7e6`; they belong to the numerically
   evaluated criterion of Remark `rem:app-s2-chains-scope`. (Full entry: E1.)
2. **Gap** `appendix-schedule2.tex:539`: the tower's step 1 is said to use the
   sampler of Proposition `prop:app-s2-TA`(iii) at `p > T_A(q)`, but that sampler's `3/8`
   bound is proved only for `p > T_S(q) > T_A(q)`. (G2.)
3. **Gap** `appendix-free-coordinate.tex:270` and `appendix-schedule3.tex:258`:
   the proof of Theorem 4.8(iii) invokes Lemma 4.3 (`lem:hybrid`) where the
   procedure has classical control and abort branches, which is the case of
   `lem:s3-hybrid`; and that lemma's support hypothesis is asserted in its
   statement and never argued. (G3, G4.)
4. **Gap** `main.tex:606--618, 1325, 1390` and `formal/README.md:21--22, 78--80`:
   the main theorem rests on an AI-only reading of the imported solver,
   including a claim that the source misprints its bound; and the paper's Lean
   boundary says class `c >= 7` is conditional while the README it cites as the
   scope description lists three class-seven modules (untracked, not imported
   by `Formal.lean`, not guarded in `Audit.lean`). One of the two documents is
   stale. (G1, G8.)
5. **Imprecision** `main.tex:706, 708, 715, 717, 726, 622`: the remarks added
   on 5 November reuse the paper's load-bearing letters with new meanings in
   the same section that defines them: `H` (a hyperplane), `K` (a secret key),
   `c` (a scalar and an arbitrary constant), `E` (number of blocks), `G_E(p)`,
   `m`, `r`, `L`, and in Remark 4.6 `\ell` is both the prime dividing `kappa`
   and the level index, `G` is `G(kappa,a)` and `N` a column count. (I1--I4.)

## Findings

Line numbers refer to the working-tree files on 2026-11-05. Replacements avoid
`\mathsf`, `\mathrel`, `\begingroup`, `\aa`.

### Errors

**E1.** `main.tex:674` (Remark `rem:two-level-threshold-size`).
Current: `above an explicit threshold that is at most $4.05\,\kappa^2(\ln\kappa)^\kappa = \kappa^{\kappa\ln\ln\kappa/\ln\kappa+O(1)}$ for $\kappa \ge 16$; computed values of the threshold are $3781$ for $\kappa = 5$ and $30823$ for $\kappa = 7$, against $T_A(\kappa) > (\kappa-1)\kappa^\kappa$.`
Why: "the threshold" is the closed form `\Theta^{\mathrm{cf}}_2` of `cor:app-s2-union-chain`; its minimum over `k` is `2.21e5` at `kappa = 5` and `1.68e6` at `kappa = 7` (recomputed from the stated formula). The quoted values are the numerically evaluated criterion `\Theta_2(\kappa) = \min_k \max(T_U,\min(W,T_R))` of `rem:app-s2-chains-scope`, two orders of magnitude lower.
Replacement:
```latex
above an explicit closed-form threshold that is at most $4.05\,\kappa^2(\ln\kappa)^\kappa = \kappa^{\kappa\ln\ln\kappa/\ln\kappa+O(1)}$ for $\kappa \ge 16$; evaluating the underlying second-moment criteria numerically instead of in closed form (Remark~\ref{rem:app-s2-chains-scope}) gives thresholds $3781$ for $\kappa = 5$ and $30823$ for $\kappa = 7$, against $T_A(\kappa) > (\kappa-1)\kappa^\kappa$.
```

**E2.** `main.tex:57` and `main.tex:63` (title page and status box).
Current: `\date{November 4, 2026 (corrected draft, not reviewed by a human specialist)}` and `\textbf{Research status, 4 November 2026.}`
Why: the status box itself describes "The version of 5 November 2026" (l. 91) and the Lean paragraph records 5 November additions; the dated title contradicts the content. Low stakes, but a wrong date on a draft that cites its own change log by date is a factual error.
Replacement: `\date{November 5, 2026 (corrected draft, not reviewed by a human specialist)}` and `\textbf{Research status, 5 November 2026.}`

### Gaps

**G1.** `main.tex:606` (Theorem `thm:is-import` header) and `main.tex:615` (Remark `rem:is-import`(c)).
Current: `\begin{theorem}[Ivanyos--Santha {\cite[Theorem~11 and the proof of Theorem~3, Sections~3.1--3.3]{IvanyosSantha2015}}]` and `The bound printed in that theorem, $d^{d^2\log d}(a+1)^{d\log d}$, does not follow from the proof for large $a$, because $d\lceil\log_2(d+1)\rceil > d\log_2 d$.`
Why: this is the only imported ingredient of Theorem 1.2, its header carries no status, and (c) asserts as fact that a published theorem misprints its bound; (e) says the reading is AI-only. The arithmetic of (c) is right for any logarithm base at least `e`, but a paper whose main theorem depends on reading a source correctly must say in the header that the reading is unverified, and (c) must be phrased as the authors' reading. No LaTeX fix removes the dependence; a human must read Sections 3.1--3.3 of arXiv:1503.09016v2 before submission.
Replacement (header): `\begin{theorem}[Ivanyos--Santha {\cite[Theorem~11 and the proof of Theorem~3, Sections~3.1--3.3]{IvanyosSantha2015}}; imported, as read by AI sessions only (Remark~\ref{rem:is-import}(e)), pending human review]`
Replacement (c): `As we read that paper, the bound printed in its Theorem~3, $d^{d^2\log d}(a+1)^{d\log d}$, is not what its proof gives for large $a$, because $d\lceil\log_2(d+1)\rceil > d\log_2 d$; we therefore use the bound the proof establishes. This reading has not been confirmed with the authors or by a human.`

**G2.** `appendix-schedule2.tex:539` (tower, "Finding the scalars").
Current: `step~$1$ alone uses the sampler of Proposition~\ref{prop:app-s2-TA}(iii), with $O(q^{q+1}\log q)$ draws per round.`
Why: Proposition `prop:app-s2-TA`(iii) needs `U_q(p) <= 1 + 1/(8q)`, that is `p > T_S(q)`; Corollary `cor:app-s2-tower` only guarantees `p > T_A(q)`. In the band `T_A(q) < p <= T_S(q)` the `3/8` success bound per round is not proved.
Replacement:
```latex
step~$1$ alone uses the sampler of Proposition~\ref{prop:app-s2-TA}(iii) when $p > T_S(q)$, with $O(q^{q+1}\log q)$ draws per round, and exhaustive search otherwise (Corollary~\ref{cor:app-s2-decoupled}).
```

**G3.** `appendix-free-coordinate.tex:270` (proof of Theorem 4.8(iii)).
Current: `changes the joint law of all records, abort flags and the output by at most $\eps/3$, by Lemma~\ref{lem:hybrid}.`
Why: the instruments are controlled by classical records and have abort branches; the lemma that covers that is `lem:s3-hybrid` (which the appendix header at l. 38 says it uses), not the bare Lemma 4.3.
Replacement: `changes the joint law of all records, abort flags and the output by at most $\eps/3$, by Lemma~\ref{lem:s3-hybrid} (whose proof uses only Lemma~\ref{lem:hybrid} and the classicality of the records).`

**G4.** `appendix-schedule3.tex:258` (Lemma `lem:s3-hybrid`).
Current: `Every ideal step of the procedure of this appendix (central instruments, kernel computation, rejection sampling, root extraction, Bezout lift, conversion channel and abort branches) maps states supported on $\mathcal{S}_{j-1}$ to states supported on $\mathcal{S}_j$.`
Why: this is the hypothesis Lemma 4.3 needs; it is asserted in the statement and never argued in the proof (l. 262).
Replacement (append to the proof at l. 262): `The support claim is the definition of the canonical subspaces in Section~\ref{sec:recursion}: each $\mathcal{S}_j$ is by construction the image of $\mathcal{S}_{j-1}$ under the $j$-th ideal step, the classical steps act on record registers only, and an abort branch leaves every unconsumed register in place.`

**G5.** `appendix-schedule3.tex:268` (proof of Theorem 4.8(iv)).
Current: `The trees act on disjoint fresh registers with independent coins, so their abort events are independent, each of probability at most $1/16$.`
Why: the union bound over `3m'`-subsets needs the bound conditional on the other trees' records; independence is true but unargued (l. 352 phrases it correctly).
Replacement: `Conditional on the records of all other trees, a tree acts on fresh registers with fresh coins, so by Lemma~\ref{lem:s3-tree}(c) it aborts with probability at most $1/16$; hence any fixed set of $3m'$ trees all abort with probability at most $16^{-3m'}$.`

**G6.** `main.tex:769` (Proposition `prop:rc-lower` statement).
Current: `Condition on rank $r = a$ and on the pivot pattern $\{1,\dots,r\}$, which fails with probability at most $1/(p-1)$.`
Why: the statement never says what the bank is; the proof (`appendix-free-coordinate.tex:351`) needs labels i.i.d. uniform on a subspace of dimension `a >= 1` with `M >= a`, and "almost every bank" is quantified only in the proof.
Replacement: `Let $M \ge a \ge 1$ labels be independent and uniform on a subspace of dimension $a$. Condition on rank $r = a$ and on the pivot pattern $\{1,\dots,r\}$, which fails with probability at most $1/(p-1)$.` and, for the conclusion, `so, for every $s \ge 1$, outside an event of probability at most $1/s + 1/(p-1)$, uniform-kernel rejection needs at least $q^{-M}/(2s) \ge \kappa^M e^{-M(\kappa-1)/p}/(2s)$ trials for success probability $1/2$.`

**G7.** `main.tex:1112` (Theorem `thm:bb-envelope`, status sentence) and `appendix-torsion-blackbox.tex:1344--1363`.
Current: `The result is conditional on Theorem~\ref{thm:main}, on Theorem~\ref{thm:power-sde}(ii) through the combined rule, and, for $e_p > 1$, on Theorem~\ref{thm:ring-to-field}(iii) with its stop rules.`
Why: the maximum defining `E_W(c)` is attained at primes where every grade except `d = 2` (for `c = 8, 9`) runs Schedule 1, and `E_W(c)` equals the Schedule 1 exponent for `c <= 7`. The dependence on the AI-only Theorem 4.7(ii) therefore buys nothing in the stated exponent for `c <= 7` and two units for `c = 8, 9`, yet makes the whole theorem conditional on it. Schedule 1 at degree `kappa_d` is already inside Theorem 1.2.
Replacement (insert after the first sentence of l. 1112): `With Schedule~1 alone (at degree $\kappa_d$), every statement of this theorem holds with $E_W(c)$ replaced by $E_1(c) = 1 + \sum_{d=2}^c d\lceil\log_2(d+1)\rceil$ and without the dependence on Theorem~\ref{thm:power-sde}(ii); since $E_W(c) = E_1(c)$ for $c \le 7$ (Lemma~\ref{lem:tb-count-exponent}), the combined rule changes the exponent only for $c \ge 8$.`

**G8.** `main.tex:1390` (`for $c \ge 7$ they remain conditional on them`), `main.tex:1325` (`$488$ in all`) versus `formal/README.md:21--22, 78--80`.
Current (paper): `So at $c = 3$, $4$, $5$ and $6$ the general-class Rees theorems need no group-law hypothesis ..., and for $c \ge 7$ they remain conditional on them.`
Why: the README the paper cites as the scope description of `tab:lean-modules` lists `BCHClassSeven`, `BCHClassSevenSubgroups`, `ReesGeneralLawClassSeven`. Those files exist untracked in `formal/Formal/`, are not imported by `formal/Formal.lean`, and `Audit.lean` has 488 `#print axioms` guards with no class-seven entry, matching the paper. One document is premature or stale; a reader with both will not know which. No LaTeX change if the README is corrected; otherwise add three rows, update `450`/`488` and the boundary sentence.

### Imprecisions

**I1.** `main.tex:706` (Remark `rem:sde-subquadratic`(a)).
Current: `and let $H$ be the span of the images of $S\setminus\{i,j\}$, a hyperplane in the span $W$ of the images of $S$.` and `For $c\in\Fp^\times$ the vectors $x\in\Fp^S$ with $\sum_l x_l\lambda_l+U=ch$ are $cz+s\delta$`
Why: `H` is the hidden subgroup and `c` the class on every page of the paper, including this one (the remark cites Theorem 1.2 and `E_W(c)`).
Replacement: `and let $\Pi$ be the span of the images of $S\setminus\{i,j\}$, a hyperplane in the span $W$ of the images of $S$.` ... `some $h\ne0$ in $\Pi$` ... `For $\gamma\in\Fp^\times$ the vectors $x\in\Fp^S$ with $\sum_l x_l\lambda_l+U=\gamma h$ are $\gamma z+s\delta$` ... `$\gamma z\in(P\cup\{0\})^S$, which fixes $\mathrm{cos}(\gamma)$. Since $\kappa\ge2$, some multiple $\gamma h$ is not in $R_U(S)$`.

**I2.** `main.tex:708` (Remark `rem:sde-subquadratic`(b)).
Current: `and let $K\in\Fp$ be unknown.` (and `K` for the key throughout (b)).
Why: `K = H \cap Z` and `K_d` are defined in Section 3 and used in the same section.
Replacement: `and let $\theta\in\Fp$ be an unknown key.` with `\theta` for `K` throughout (b): `$\chi(\theta+c_i)$`, `$x_i=u_i(\theta+c_i)$`, `$\alpha/\beta=\theta$`, `$\theta$ is recovered`, `key $\theta$`, `recovering $\theta$`.

**I3.** `main.tex:715, 717` (Remark `rem:sde-block-steered`) and `main.tex:724--740` (Remark `rem:sde-worst-case`).
Current: `split $S$ into blocks $S_1,\dots,S_E$`, `let $G_E(p)$ be the least $|\mathrm{Good}(\beta)|$`, `M_E(a)=1+m(a+1)-\tfrac{(E-1)m(m-1)}{2}+[r>0](r+1),\qquad a=m(E-1)+r`, `where $L\le\lceil a/(E-1)\rceil$ is the number of rounds`, and at l. 726 `So for $a>\kappa/c$ every bank of $c\,a^2$ columns has a nonzero solution`.
Why: `E_s` is the evaluation map, `G` the group, `m` the dimension of `L`, `r = g_2`, `L = \sum_{p>c} n_p` in Theorem 7.3, and `c` is the class. Four of the paper's primary symbols are redefined inside two remarks of Section 4.
Replacement: rename the block count to `J` and the counting variables: `split $S$ into blocks $S_1,\dots,S_J$`, `$E_{\mathrm{cg}}(J,\kappa)$`, `$\Gamma_J(p)$` for `$G_E(p)$` (and `$\Gamma^*_J(p)$` in `rem:sde-worst-case`), `M_J(a)=1+\mu(a+1)-\tfrac{(J-1)\mu(\mu-1)}{2}+[\varrho>0](\varrho+1),\qquad a=\mu(J-1)+\varrho,\ 0\le\varrho<J-1`, `where $\Lambda\le\lceil a/(J-1)\rceil$ is the number of rounds`, and at l. 726: `So for every constant $C_0 \ge 1$ and every $a > \kappa/C_0$, every bank of $C_0\,a^2$ columns has a nonzero solution`. Apply the same renaming to `D_E`, `E\ge\kappa`, `E=3`, `\kappa^E` and `\rho\le rE/2` (`\varrho_{\mathrm{pairs}} \le rJ/2`, since `\rho` is also the value of `R` in Proposition 4.9).

**I4.** `main.tex:622` (Remark `rem:is-runtime`).
Current: `When $\kappa = \ell^e$ is a prime power, the following deterministic variant makes at most $e \le \log_2\kappa$ runs` ... `One call runs \cite[Lemma~12]{IvanyosSantha2015} with $G/G_\ell$ nodes at level $\ell$, where $G_\ell = \kappa^{\ell(\ell-1)/2}(a+1)^\ell$.` ... `$G = G(\kappa,a)$` ... `$N = G^{L} \le B_{\kappa}(a) \le M_d$`.
Why: in one remark `\ell` is the prime dividing `kappa`, the level index of the tree and (as `\ell_d`) the number of zero-sum terms; `G` is the group everywhere else and `N` the black-box input size and `N_{\mathrm{instr}}`.
Replacement: `When $\kappa = q^e$ is a prime power` (and `q` for the prime throughout: `multiplies $|\langle\eta\rangle|$ by at least $q$`, `cyclic $q$-group`, `$q$-th-power nonresidue for every $q \mid \kappa$`); `with $\Gamma/\Gamma_j$ nodes at level $j$, where $\Gamma_j = \kappa^{j(j-1)/2}(a+1)^j$`; `$\Gamma = G(\kappa,a)$`; `$N_{\mathrm{col}} = \Gamma^{L} \le B_{\kappa}(a) \le M_d$` and `$40\kappa^3 N_{\mathrm{col}}\, b(a^2+b^2)$`.

**I5.** `main.tex:213` (caption of `tab:main-regimes`), `main.tex:110` (abstract).
Current (caption): `The hidden-codimension row needs an ordinary oracle and a given $k$.` (no conditions are given for the black-box row); abstract: `and a bounded-error algorithm for black-box nilpotent groups of fixed class with unique encoding, polynomial in the input size.`
Why: ll. 134 and 242 name Theorem 4.7(ii) and Theorem 6.3(iii) as conditions of Theorem 7.3; the caption and abstract do not.
Replacement (caption, after that sentence): `The black-box row is conditional on Theorem~\ref{thm:main}, on Theorem~\ref{thm:power-sde}(ii) through the combined rule and, when $e_p > 1$, on Theorem~\ref{thm:ring-to-field}(iii).` Abstract: `and, conditionally on Theorem~\ref{thm:main} and the two-level schedule, a bounded-error algorithm for black-box nilpotent groups of fixed class with unique encoding, polynomial in the input size.`

**I6.** `main.tex:1096` (Theorem `thm:bb-envelope` statement).
Current: `and $A_c$, $d$, $k$ as in Proposition~\ref{prop:black-box}` followed in the same sentence by `$E_W(c) = \max_{p>c}\bigl(1 + \sum_{d=2}^c e_d(p)\bigr)$`.
Why: `d` is the rank of `F_{s,c}` (used in (ii): `$2k\,d\,(2b_M + A_c)$`) and the grade index, in one statement.
Replacement: write the rank as `$d_F \coloneqq \rank F_{s,c}$` throughout the theorem, Proposition 7.1(i),(iv), the notation table (l. 354) and `app:tb-counts` (e.g. `$2k\,d_F\,(2b_M + A_c)$`), keeping `d` for grades; and `$E_W(c) = \max_{p>c}\bigl(1 + \sum_{d=2}^c e_d(p)\bigr)$ (a maximum over finitely many values, by Lemma~\ref{lem:tb-count-exponent})`.

**I7.** `main.tex:1168` (after Corollary `cor:subspace-hsp`).
Current: `It is argued from proved lemmas, not a reviewed proof, and no human has read it.`
Why: by the paper's own convention (l. 368) "argued" means proof only in a cited note, but l. 1170 says Appendix D proves a completed form in full (Theorem `thm:app-sub-hsp`).
Replacement: `It is proved in full in Appendix~\ref{app:subspace} (Theorem~\ref{thm:app-sub-hsp}), checked by AI sessions only, and no human has read it.`

**I8.** `main.tex:1120` (Remark "Comparison with the bounded-prime algorithm").
Current: `against $E_W(9)+1 = 144$ for $p > c$`.
Why: the Imran--Ivanyos exponents quoted are in `n = \log_p|G_p|`; in `n_p` the Rees exponent is `E_W(c)` when `e_p = 1` and `E_W(c)+1` when `e_p > 1` (Lemma `lem:tb-count-prime`); `E_W(c)+1` is the exponent in `N`.
Replacement: `against $E_W(9) = 143$ in $n_p$ when $e_p = 1$, or $E_W(9)+1 = 144$ when $e_p > 1$, for $p > c$`.

**I9.** `main.tex:761` (Theorem 4.8(iii)).
Current: `At the other grades use the combined rule of Remark~\ref{rem:combined-schedule}`
Why: read alone, the combined rule may select Schedule 2; the appendix (`appendix-free-coordinate.tex:199`) shows it never does here, only because every grade with `2 <= kappa_d < p-1` is already a sampler grade.
Replacement: `At the other grades use the combined rule of Remark~\ref{rem:combined-schedule}, which there is the linear schedule ($\kappa_d = 1$, $M_d = g_d+1$) or Schedule~1 at degree $d = p-1$ ($\kappa_d = p-1$); no Schedule~2 node occurs;`

**I10.** `main.tex:759` (Theorem 4.8(ii)).
Current: `Then $\beta \le 4\cdot 15^{-2u}u^{-u-1} + 2p^{-u-1}$`
Why: `\beta` has three arguments in part (i) and `eq:fc-beta`.
Replacement: `Then $\beta(4u, 2u+1; a_d) \le 4\cdot 15^{-2u}u^{-u-1} + 2p^{-u-1}$ at every grade`.

**I11.** `main.tex:773` (paragraph after `prop:rc-lower`) and `appendix-free-coordinate.tex:279, 283` (Remark `rem:fc-zero-sum-sis`).
Current (main): `and a polynomial-time method at arity at most $p^2g_d^{-2\delta}$ on primes $p = \Theta(g_d^{\,k})$, for constants $k > 1$ and $\delta > 0$, would, with abort probability at most $1-1/\poly(g_d)$, approximate worst-case lattice problems in dimension $g_d$ within polynomial factors`
Why: the appendix hypothesis is `p \in [g_d^k, 2g_d^k]` and `M_d <= min(p^2 g_d^{-2\delta}, poly(g_d))`; the main sentence drops the `poly` bound and attaches the abort clause to the lattice algorithm; `\delta` is a failure probability in (b) and a constant in (c) of the same remark.
Replacement (main): `and a polynomial-time method that, on primes $p \in [g_d^{\,k}, 2g_d^{\,k}]$ for some constants $k > 1$ and $\theta > 0$, reads at most $\min(p^2g_d^{-2\theta},\poly(g_d))$ labels and aborts with probability at most $1 - 1/\poly(g_d)$, would approximate worst-case lattice problems in dimension $g_d$ within polynomial factors, in quantum polynomial time if the method is quantum (\cite[Theorem~1.1]{MicciancioPeikert2013}; Remark~\ref{rem:fc-zero-sum-sis}; AI-checked, pending human review).` In the appendix (c): `Fix constants $k > 1$ and $\theta > 0$ ... $M_d \le \min(p^2g_d^{-2\theta}, \poly(g_d))$ ... $p \ge \sqrt{M_d}\,g_d^{\,\theta}$`.

**I12.** `appendix-schedule2.tex:573` (chain proof).
Current: `For $\zeta \in \Fp^\times$ of $D$-class $n$ and a round $k$` (and `$\zeta_k$`, `$\zeta = 1$`, `$\zeta = \zeta_k$`).
Why: `\zeta := \xi^h` is fixed at l. 116 as the primitive `kappa`-th root of unity used by the coset test.
Replacement: `\gamma` for every `\zeta` in that proof (`$\gamma \in \Fp^\times$ of $D$-class $n$`, `$\gamma = 1$`, `$\gamma_k$`, `$-\gamma_k\alpha_{n_k}e_k$`, `$\sum_k\gamma_k(\alpha_{n_k}e_k + v_k)$`).

**I13.** `appendix-schedule2.tex:631--634` (barrier display).
Current: `for $p \in E_2(\kappa)$, fixed $h \ge 1$ and uniform $\Lambda \in \Fp^{m\times(m+h)}$` ... `\kappa p^h\Bigl(1 - \frac{1-p^{-1}}{\kappa}\Bigr)^{m+h} + \sum_{r=2}^{\kappa-1}p^{r(\kappa-1+h)}`
Why: `h = (p-1)/\kappa` throughout the appendix and `tab:notation-sde`; `\Lambda` is the count of Lemma `lem:app-s2-stage`; `r = |R|` in this subsection; `m` is the cyclotomic count elsewhere.
Replacement:
```latex
for $p \in E_2(\kappa)$, fixed $h' \ge 1$ and a uniform matrix $\Lambda' \in \Fp^{a\times(a+h')}$, the set $\{\Lambda' x : x \in (Q_0\cup\{0\})^{a+h'}\}$ contains a line $\Fp w$ with $w \ne 0$ with probability at most
\[
  \kappa p^{h'}\Bigl(1 - \frac{1-p^{-1}}{\kappa}\Bigr)^{a+h'} + \sum_{s=2}^{\kappa-1}p^{s(\kappa-1+h')}\Bigl(1 - \frac{1-p^{-s}}{\kappa}\Bigr)^{a+h'},
\]
which tends to $0$ as $a \to \infty$. The bound is asymptotic: it drops below $1$ only for $a \ge 146$ at $\kappa = 4$, $p = 17$, $h' = 2$.
```

**I14.** `appendix-schedule2.tex:469` (tower setting).
Current: `For $D \mid \kappa$ put $P_D = \{x^D : x \in \Fp^\times\}$`
Why: `D = P_\kappa \cup \{0\}` and `q = (h+1)/p` in `tab:notation-sde` and Appendix C; this appendix uses `D` for a divisor of `kappa`, `q` for its largest prime factor (l. 528) and `k = |K|` (ll. 580, 607) against the abort parameter `k`; `\rho` is a moment ratio at l. 519 and a vector at l. 573.
Replacement (insert after the first sentence of l. 469): `In this subsection and the next, $D$ denotes a divisor of $\kappa$ and $q$ a prime factor of $\kappa$ (not the set $D = P_\kappa\cup\{0\}$ and the ratio $q = (h+1)/p$ of Appendix~\ref{app:schedule3}), and in Subsection~\ref{app:s2-chains} $k = |K|$ is not the abort parameter.` and rename `\rho` at ll. 519, 620 to `\rho_2`.

**I15.** `appendix-schedule2.tex:545` (uncovered lists).
Current: `nor a union chain with $|K| \in \{2,3\}$ was found: ... $\{29,43,71,113\}$ for $\kappa = 7$` and later `for $\kappa = 7$ they were run there, over every $K \ni 0$ with $|K| \in \{2,3,4\}$`; also `$T_R(9,3) \approx 1.35\cdot10^5$` while `the searches stop at $135000$` (l. 627).
Why: the `|K| = 4` verdict for `kappa = 7` is not stated, and whether the `kappa = 9` coverage has a gap depends on `T_R(9,3) <= 135000`; from the stated criterion `T_R(9,3) = 134723.2`, but `\approx` hides it.
Replacement: `nor a union chain for any $K \ni 0$ with $|K| \in \{2,3\}$ (for $\kappa = 7$ also $|K| = 4$) was found:` and, in both places, `$T_R(9,3) = 134724 < 135000$`.

**I16.** `appendix-schedule2.tex:551` and `:467`.
Current: `Its arities are of degree at least $3$ in $a$, so it does not lower the Schedule~2 arity`
Why: true as polynomials in `a`; at `a = 1` the chain arity `\binom{4}{3} = 4` is below `2\kappa`.
Replacement: `Its arities are of degree at least $3$ in $a$, so for large $a$ it does not lower the Schedule~2 arity $(a+1)((\kappa-1)a+1)$, and`

**I17.** `appendix-free-coordinate.tex:151` (proof of Theorem 4.8(i)).
Current: `The hypothesis of part~(i) is the label law used in Lemma~\ref{lem:fc-node}(a), with $a = a_d$`
Why: Lemma `lem:fc-node` is stated only for the input `\rho_{H_d}^{\otimes M}\otimes\omega`; part (i) is stated for any `a`-dimensional law.
Replacement (insert before): `Parts~(a)--(c) of Lemma~\ref{lem:fc-node} use the bank only through Lemmas~\ref{lem:fc-rref} and~\ref{lem:fc-moment}, so they hold verbatim for any bank independent and uniform on a subspace of dimension $a$ and coins independent of it.`

**I18.** `appendix-free-coordinate.tex:256` (`FCS` undefined), `:294` (`\sigma_p` bound imported without proof), `:303` (vacuous `L`), `:330, 498` (`M_d \ge g_d+1` derivation).
Current (330): `and $M_d - n_0^{(d)} \ge g_d - 1$ (through its second term), so $M_d \ge g_d + 1$`
Why: at `L = g_d-1` the second term of `eq:fc-beta` equals `(p^{g_d}-1)/(p^{g_d}-p^{g_d-1}) > 1`, so `\beta < 1` forces `L >= g_d` and `M_d >= g_d+2`; `FCS` never defined in the PDF; the Chebyshev bound at 294 is the only displayed bound of the remark neither proved nor exactly checked; at 303 for `p = 2^j+1` the quantity `L` is at most `1` for all moderate `n`.
Replacement (330, 498): `and $M_d - n_0^{(d)} \ge g_d$ (at $L = g_d - 1$ the second term of~\eqref{eq:fc-beta} is at least $1$), so $M_d \ge g_d + 2$`. (72): `a node running (F1)--(F6) is called an \emph{FCS node} (free-coordinate sampler) below.` (294): `$\sigma_p \le p$ because, by Cauchy--Davenport, the subset sums of $p-1$ nonzero elements cover $\Fp$; the bound $\sigma_p \le \lceil2\log_2(p-1)\rceil+4$ is the Chebyshev argument of~\cite[Proposition~5.3]{KothariMetgerODonnellShuttyWu2026}, imported here and not re-derived.` (303): `..., valid when $L \ge 2$, that is for $n$ large in terms of $p$ and $\delta$. So $M = \Omega_p(n^2/\log n)$ for fixed $\delta$.`

**I19.** `main.tex:315` (`tab:notation-sde`, row `h`).
Current: `Sec.~\ref{app:s2-gcd}; Thm.~\ref{thm:free-coordinate}(iv)`
Why: for Schedule 3, `h` is defined in the paragraph before Theorem 4.8 and used in all four parts.
Replacement: `Sec.~\ref{app:s2-gcd}; Sec.~\ref{sec:sde} (Schedule~3 paragraph); Sec.~\ref{app:s3-setting}`

**I20.** `appendix-torsion-blackbox.tex:1349` and `:1336`.
Current: `attained at $p = 3, 7, 13, 61, 61, 421, 2521, 2521$` and `$x \mapsto x^{x(x-1)\lceil\log_2(x+1)\rceil/2}$ is nondecreasing on $x \ge 1$`.
Why: these are the smallest witnesses; the maximum is attained at every prime `p \equiv 1 \pmod{\operatorname{lcm}(2,\dots,c)}` below the binding threshold (1024 for `c <= 7`, 104976 for `c = 8, 9`); the ceiling makes the real function non-monotone, only integer points are used.
Replacement: `attained for example at $p = 3, 7, 13, 61, 61, 421, 2521, 2521$` and `is nondecreasing on the integers $x \ge 1$`.

### Style

**S1. Length and structure (the referee's main objection).** Concrete moves, none of which removes a theorem:
- `main.tex:702--741` (Remarks 4.11--4.13, about 4 pp, each saying "nothing else in the paper uses it"): move to a new appendix "Side results on the arity of the diagonal equation"; keep in `rem:triangular-scope` the one sentence that points to them.
- `main.tex:672--675` (Remark 4.10, 1.5 pp of threshold discussion and barrier arguments "made only in the cited reports"): move to Appendix A after `tab:app-s2-thresholds`.
- `main.tex:620--632` (Remark 4.6, Turing-machine tape layout): keep the two displayed bounds and the sentence "for an absolute constant $C_1$ that is not computed"; move the layout to Appendix E next to `prop:tb-count-gates`, which is the only user.
- `main.tex:840--848` (Gate-level control, Binary arithmetic, Coherent-label backends, Instances, Scope: about 5 pp): replace by one table (backend, file, instance, qubits, gates, what is simulated, what is only counted) and one paragraph of at most 15 lines; move the prose to a supplement.
- `main.tex:62--99` (status box): cut to five lines (draft; no human review; main theorem proposed; change logs in `research/audits/reviews/`); the per-version history belongs in a "Changes" appendix together with the 13 "previous version" and 8 "withdrawn" passages at ll. 173, 235, 433, 461, 519, 551--558, 640, 766, 993, 1040, 1087, 1127, 1172, 1192, 1325.
- `main.tex:184 \file{...}` paths in the body: replace by short artifact tags and one "Artifacts" appendix table mapping tag to path and report.
- `main.tex:1188--1222` (Section 8 classical filters): tangential to the HSP result; move to an appendix, keep Section 8.1 (classical query complexity) in the body.
- `main.tex:213` (caption of `tab:main-regimes`, 20 lines): move everything after the second sentence into the paragraph before the table.
- Appendix B (uniform-kernel sampler) duplicates Appendix C's induction (`prop:mixed-schedule` vs `lem:fc-forest`; `prop:s3-uniform` vs `prop:fc-uniform`(a)); state one proposition with two trial counts and make `prop:mixed-schedule` a corollary of `lem:fc-forest`. Appendix A ll. 1--79 (integrator comment block), 302, 539, 545/553--563 (definitions stated twice), 631--635, 645 (about 900 words of `E_2(8)` run provenance) can be cut to a table and a pointer.
Expected result: body about 35--40 pp, appendices about 90 pp, plus a supplement.

**S2. Status labels are applied inconsistently.** 14 theorem-like headers carry no label (`main.tex:379, 398, 447, 490, 536, 551, 579, 606, 611, 696, 784, 1038, 1081, 1119`), while l. 368 says the label "applies to every result of this paper" and l. 600 lists the untagged ones as "AI-checked, pending human review". Either tag all headers or none. Recommended: add to the status box (l. 63) the sentence `Every theorem, lemma, proposition and remark of this paper is AI-checked and pending human review; headers carry a label only when a result is in addition conditional, a finite computation, or argued elsewhere.` and delete the bare `AI-checked, pending human review` from headers, keeping `conditional`, `finite computation`, `argued`.

**S3.** `main.tex:670, 773, 1016`: `Section~\ref{app:s2-scope}`, `Section~\ref{app:fc-split}`, `Section~\ref{app:fc-mixed}` versus `Appendix~\ref{app:...}` 25 times elsewhere. Replacement: `Appendix~\ref{...}` (or `Section~\ref{...}` everywhere; the appendix subsections print as A.x, so "Section" is also defensible, but not both).

**S4.** `main.tex:110` (abstract): `(class five since 4 November and class six since 5 November 2026)`. Dates belong in Section 9. Replacement: delete the parenthesis.

**S5.** `main.tex:1033` (proof of Corollary 6.2): `a guard (abort if $r > k$; it never fires on the ideal support, where $r \le a_d \le k$)`; `r` is the derived dimension of the adjacent Corollary 6.1 and Table 1; `K`, `S`, `b` are also reused here. Replacement: `a guard (abort if the observed rank $r_{\mathrm{obs}} > k$; it never fires on the ideal support, where $r_{\mathrm{obs}} \le a_d \le k$)`, and `$\mathfrak{k} = \hh \cap \mathcal{I}$`, `$\mathfrak{s} = N_{\mathcal{L}}(\mathfrak{k})$` as in Appendix F.

**S6.** `main.tex:1100` (Theorem 7.3(iii), a 40-line item duplicating Proposition `prop:tb-count-gates`(a)--(d)). Replacement: `\item For the primes $p > c$, and for order finding, factoring and the charts, the gate count is $O_c(N^{E_W(c)+4+o(1)})$ and the total time is $O_c(N^{E_W(c)+1+\max(3,\hat\beta_c)+o(1)})$ for $c \ge 3$ (Proposition~\ref{prop:tb-count-gates}, which also gives $c = 1, 2$, itemizes every term and discharges (H1)--(H3)).` and move the rest to Appendix E.

**S7.** `main.tex:957` (caption of `tab:random-column-budget`) lacks the status label its sibling `tab:fcs-budget` carries. Replacement (append): `AI-checked, pending human review.`

**S8.** `appendix-schedule3.tex:53--54, 68, 77, 120` and `appendix-free-coordinate.tex:48, 70, 203, 251, 507`: letter reuse that the text itself apologises for (`P_\kappa` for `D`; `S`, `L`, `R`, `N`, `q`, `\alpha,\beta` with two meanings each). Replacement: in B use `D = \{0\}\cup\{x^\kappa\}`, `\Omega = D^M\setminus\{0\}`, `L_\kappa`, `R_{\mathrm{rd}}`, `\varrho` for `p^{-a}`; in C use `N_{\mathrm F}` for the sampler-node count and `B = \lceil\log_2(27N_{\mathrm F}/\eps)\rceil` throughout (also `main.tex:761`); then delete the reconciling sentences at C:48, C:70 and the clause in `main.tex:326`.

**S9.** `appendix-free-coordinate.tex:36, 345` and `appendix-schedule3.tex:41`: `as recorded in the source comment of this appendix`. A PDF reader cannot see source comments. Replacement: cite the check file, e.g. `as recorded in \file{research/audits/reviews/2026-11-02-rees-free-coordinate-appendix/fc_appendix_check_out.txt}`, or drop the sentence.

**S10.** `appendix-free-coordinate.tex:275` (comparison with the derivation note's `\eps/9` split), `:505/507` (duplicated sentence), `:70` (irrationality of `2B\ln2\,q^{-r}`): delete or reduce to one sentence each; replacements in the parallel pass are `A grade may instead take the combined rule's arity when it is smaller; at grades where that rule takes Schedule~2, Theorem~\ref{thm:power-sde}(ii) becomes a hypothesis and its Las~Vegas calls must be capped at total failure $\eps/9$. No row of Table~\ref{tab:fcs-budget} uses this.` and `In practice take $T_r = \lceil 2B\lambda q^{-r}\rceil$ with a rational $\lambda \ge \ln 2$, for instance $\lambda = 7/10$.`

**S11.** `appendix-schedule2.tex:496`: `The scalars $(\alpha^{(t)},\beta^{(t)})$ depend only on $(p,\kappa,\xi)$, not on the columns.` Existence is in fact `\xi`-independent for the tower (each `R_t` is a subgroup), which matters because l. 557 stresses that union steps do depend on `\xi`. Replacement (append): `; whether they exist does not depend on $\xi$, because the relabelling $i \mapsto ui$ of Subsection~\ref{app:s2-chains} fixes each subgroup $R_t$.`

**S12.** `appendix-schedule2.tex:545` (last sentence): `All the listed primes lie in $E_2(\kappa)$: restricting the rows of a two-level contraction at $(p,\kappa)$ to $R$ gives an $\mathrm{RC}(\kappa;R)$ contraction, and at each listed prime some step with $D = \kappa$ fails.` The two-level construction is among the constructions searched, so membership is immediate. Replacement: `All the listed primes lie in $E_2(\kappa)$, since the two-level construction is among the constructions searched.`

## Checks that passed (recorded so they need not be redone)

- Build: 167 pp., no undefined `\ref`/`\cite`, no multiply-defined label; every `\ref`/`\eqref` target in the six appendices exists; every `\file{}` path cited in Appendix A exists on disk.
- Main chain: Theorem 2.1 (BCH over `\mathbb{Z}[1/c!]`, class of the cover), Lemma 2.2 (Vandermonde times `\diag(s_i)`), Proposition 2.3, Lemma 2.5 (entry `\prod_i 1_H(E_{s_i}(b^{-1}a))`), Lemma 3.1 (`|K|/|Z|`, the `|K|` cancellation), Proposition 4.1 (branch-by-branch identity, `\delta_s(HZ) = HZ`), the `N_{\mathrm{instr}}`, `N_{\mathrm{solver}}` and `n_d` counts, Lemma 4.3 and its pure-state bound `\sqrt{1-|\langle\phi|\phi'\rangle|^2} \le \|\phi-\phi'\|`, the rank bound `1/((p-1)p^t)`, the proof of Theorem 1.2 (`2\eps/3` total), Remark 4.5(b) (`td \equiv \kappa \pmod{p-1}`), Proposition 4.9 (realisation weights, back substitution, `(a+1)(a+2)/2`), Remark 4.11(a) (circuit gives no plane), the `M_E(a)` formula at `E = 2, 3`, Remark 4.13(a) (`2a \le N \le \kappa a`), the `T^{\mathrm{IS}}_d \le 64C_1c^3M_d((a+1)\log_2p)^5` conversion, Theorem 7.3's `L \le \ell/\log_2(c+1)`.
- Schedules: Theorem 4.7(ii)/(iii) numbers (`B_4(2) = G(4,2)^3`, Davenport constant `9`), Theorem 4.8(i)--(iv) constants against Appendices B--C (`\beta`, `q^r/2`, `\lceil 2B\ln2\,q^{-r}\rceil`, `4\cdot15^{-2u}u^{-u-1}+2p^{-u-1}`, `2B\ln2\,u^{u-1}+1`, `B = \lceil\log_2(64(4u)^{c-1})\rceil`, `1/16`, `2^{-2m'}`, `\tau_d`, `B = \lceil\log_2(27N/\eps)\rceil`, `\mu \ge 2^{8u+1}u^{2u+1}`, `1/(4\kappa^M)`), `tab:main-regimes` rows against their theorems, `rem:combined-schedule` against Theorem 7.3's `e_d(p)`, `E_W(2..9)` and the Schedule 1 exponent `145` (= `\ReesClassNineQueryExp`), `tab:query-crossover` first two rows, `tab:fcs-budget` `p = 11` row having no Schedule 2 grade.
- Appendix A numerics: `T_A(3) = 79.039`, `\lceil T_A(8)\rceil = 117441563`, `\Theta_2(5) = 3780.8`, `\Theta_2(7) = 30823.1`, `T_R(9,3) = 134723`, tower thresholds, `W(D,2) < ((D-1)^2+1)^2` for `D \ge 4` (fails at `D = 3`, so the stated hypothesis is needed and present), `11689 \in E_2(8)`, `17911 \in E_2(9)`, `E_2(8) \subseteq [3,20000]`.
- Appendices D--F: Corollary 6.2 hypotheses (ordinary oracle, given `k`, `p \ge 2k+1` / `p \le 2k`, `2^{O(k\log(k+2))}`), Theorem 7.4 constants, the `\delta/2+\delta/2` and four-quarter error splits, Proposition 8.3 arithmetic including the Chernoff step, Remark 8.4(a)--(c).
- Overstatement: no claim of speedup, novelty, human or independent review, an implemented coherent receiver, a general SDE solver or a checked formal compiler; AI-only results carry "AI-checked, pending human review" (see S2 for the header inconsistency); the Lean paragraph says "machine-checked in Lean; AI-run, pending human review" at every Lean claim; `450`/`488` guards match `formal/Formal/Audit.lean`.
- Integration rows I190--I211: all 22 insertions located (`rem:premature`, `rem:mixed-source`, Terminology paragraph, `prop:triangular-sde`, application-3 paragraph l. 1222, `rem:is-runtime`, merged `thm:free-coordinate`, `rem:fc-zero-sum-sis`, l. 773 sentence, coset-copy wording, Lean c6, `rem:sde-subquadratic`, exact-exponent clause l. 840, `app:s2-tower`, `rem:sde-block-steered`, referee-13 fixes, receiver-sims paragraphs ll. 844--848, `app:s2-chains`, `rem:fc-zero-sum-arity`, `rem:sde-worst-case`); each carries a label.

## Counts

Error 2; Gap 8; Imprecision 20; Style 12.
