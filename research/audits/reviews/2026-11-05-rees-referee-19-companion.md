# Referee 19: pre-send check of the restructured extended companion

Date: 2026-11-05. AI referee (Claude Fable 5.1), read-only; no file other
than this report was edited. No git, no network. Python
`/opt/anaconda3/bin/python -I` under `nice -n 19` for the statement diffs
and the PDF page count (`pypdf`).

Object: `docs/papers/rees-hsp/main.tex` with the ten `appendix-*.tex`
(built PDF `pdf/rees-companion-2026-11-05.pdf`, 201 pages), compared with
the pre-restructure archive
`docs/papers/rees-hsp/archive/main-2026-11-05-before-restructure/` and with
the core `docs/papers/rees-hsp/core/main-core.tex` (27 pages). The
restructure record is
`research/audits/reviews/2026-11-05-rees-companion-restructure.md`.

Line numbers below refer to the current files.

## Summary

Verdict: **yes after the listed fixes** (all small; none touches a proof).
Counts: Error 0, Gap 0, Imprecision 5, Style 6.

The restructure lost no theorem-like environment, no hypothesis, no proof
and no status label. Every statement that changed is either a repository
path replaced by a pointer to Appendix J, a piece of removed history, a
block moved verbatim into a new remark (verified intact), or a statement
synchronised with the referee-18 fixes of the core (verified against the
core). The companion contains every core result in the same or a more
general form. The text now reads as a paper; the project-log residue that
remains is listed under Style.

## 1. Restructure integrity (archive versus new)

Method: a script extracted every `theorem`, `lemma`, `proposition`,
`corollary`, `definition` and `remark` environment from both versions
(comments stripped), keyed by label, and compared header and body word by
word. Scratchpad: `ref19/extract.py`, `ref19/wdiff.py`, output
`ref19/wdiff.out`.

Counts: archive 163 environments, new 166. Labelled environments missing
from the new version: none. New labelled environments: `rem:sde-side-tape`,
`rem:sde-side-barrier`, `rem:tb-count-envelope`. The four unlabelled
environments (two definitions and one remark in Appendix A, one remark in
Section 10) are byte-identical in both versions after whitespace
normalisation. Changed statements: 39 of 162 common environments. All 39
were read; they fall into four classes.

(a) Path replaced by `(Appendix~\ref{app:provenance}, item~\ref{prov:...})`
or history removed, mathematics unchanged (24): `rem:fc-zero-sum-sis`,
`rem:fc-zero-sum-arity`, `rem:fc-witness-h3`, `rem:app-s2-joint-moments`,
`rem:app-s2-barrier-scope`, `rem:app-s2-four-cycle`,
`rem:app-s2-tower-scope`, `rem:app-s2-chains-scope`, `rem:app-sub-profile`,
`rem:tb-ring-sources` (retitled), `rem:tb-compiler`, `rem:tb-scope`,
`prop:tb-count-gates`, `rem:premature`, `rem:product-channel`,
`thm:is-import` (header wording only), `thm:power-sde`,
`rem:triangular-scope`, `rem:sde-subquadratic`, `rem:sde-block-steered`,
`rem:sde-worst-case` (header punctuation), `rem:combined-schedule` (status
label added, not removed), `rem:codim`, `prop:black-box`, `rem:mixed-source`,
`rem:filters` (retitled), `lem:coherent-power-sde`,
`prop:coherent-receiver`. Judged OK. Spot checks of the rewordings: in
`prop:black-box` the sentence "Note that $a^p$ itself does have an order-$p$
preimage, $\Phi(px_1) = a^p$; it is $b$ that has none" is supported by the
preceding text of the same proposition ("$b$ has no preimage of order
$p$"); in `rem:tb-compiler` "A compiler that reduces exponents modulo $p$
alone is certified only for $c \le 4$ with $p > 4$" restates the archive's
history sentence as a fact.

(b) Synchronised with the referee-18 core fixes (9): `def:input-contract`
(promise clause, "labels of $w$ bits"), `thm:main` (enumerated form; the
sentence naming the evaluation points and Schedule 1 moved to the paragraph
after the theorem, main.tex:198, as in the core; explicit bound item (4)
added), `rem:main-solver` ("returning the scalars ... not only their $d$-th
powers"), `rem:is-import` (the $O(M\log p)$ conversion cost),
`thm:uniform-compilation` (dimension "at most $D_d$" and the general
Lie-algebra clause; the stored-coefficient count $(d-1)d(d+1)/2$; the
prime factors "at most $d$" in place of $c$; $\eps' = \eta^2/(16p)$ with the
Dawson--Nielsen synthesis step; the measure-and-reset clause in (iv)),
`lem:collision` ($\tau \to \rho$), `prop:classical-query` and
`rem:query-separation` ($t \to \tau$; both Ettinger--H{\o}yer--Knill
theorems). Each was compared with the current core statement: same
content. Checked: $2(p\eps')^{1/2} = \eta/2$ at $\eps' = \eta^2/(16p)$ and
the synthesis of $N_g$ gates to $\eta/(2N_g)$ adds $\eta/2$; the explicit
bound (4) follows from $g_d \le m$ in $B_d(g_d)$. Judged OK. The restructure
record does not mention this synchronisation; it should (see Style 2).

(c) Large blocks moved out of a statement into a new remark (3), verified
intact by keyword and by reading the new text:
`rem:is-runtime` (main.tex:625) -> `rem:sde-side-tape`
(appendix-sde-side.tex:11): the deterministic variant with the kernel
vector $\alpha$, the generator remark (GRH), the per-node operation counts,
the van de Woestijne zero-sum cost, the tape layout, the evaluation-order
sentence, the run-count bounds with the exhaustive search at
$\kappa_d \in \{6,10,12,15,30\}$, $p < 4000$, the explicit-column
constructions with $\nu \le 10^{12}$ and the "no full run at composite
$\kappa_d$" caveat are all present; the shortened remark keeps
$r_{\mathrm{run}}$, $T^{\mathrm{IS}}_d$, $T^{\mathrm{IS},\ast}_d$ and the
status label. `rem:two-level-threshold-size` (main.tex:676) ->
`rem:sde-side-barrier` (appendix-sde-side.tex:46): BGGP Proposition 26, the
primes $37, 53$ ($\kappa = 4$) and $131$ ($\kappa = 5$), the
$2^{-1/(\kappa-1)}\kappa^\kappa$ bound, Deligne--Katz, the inclusion--exclusion
sizes, $p = 97$, $43$, $1009$, the cyclotomic two-row obstruction with
$p \le \kappa^2 - 3\kappa + 3$ (labelled proved), the
$((r-1)\kappa^r+2)^2$ bound and the Paley remark are all present, with
"argued" in the header. `thm:bb-envelope`(iii) (main.tex:1202) ->
`rem:tb-count-envelope` (appendix-torsion-blackbox.tex:1568) and
`prop:tb-count-gates`(b): the $O(\ell^8)$-for-every-$\eps$ gloss, the Howell
forms, the definition of $\hat\beta_c$ with the exponent-5 bound
$T^{\mathrm{IS}}_d \le 64C_1c^3M_d((a+1)\log_2 p)^5$ are in the remark; the
$2\sum k\,d$ transforms at error $\eps/(16\ell kd)$ and the rotation-count
convention are in `prop:tb-count-gates`(b). One clause of the old (iii) is
now stated nowhere in the theorem itself (Imprecision 3). The input-size
bound $O_c(N^{E_W(c)+4+o(1)})$ was moved *into* (iii) from the paragraph
after the theorem, which still carries it together with the $c = 1, 2$
cases; consistent.

(d) Header retitles only (3): `rem:tb-ring-sources`, `rem:filters`,
`rem:sde-worst-case`. Judged OK; the status words are unchanged.

Status labels: every archive header that carried "argued", "conditional",
"finite computation" or "AI-checked, pending human review" has a new header
with the same words; three headers gained a label (`rem:combined-schedule`
body, `prop:single-evaluation`, `lem:collision`, `prop:classical-query`
headers now carry "AI-checked, pending human review", which the core
headers do not; harmless).

## 2. Readability as a paper

Front matter: title, one-paragraph "Status of this paper", abstract,
contents; Sections 1--11 in paper order (introduction with related work,
cover, instrument, descent, schedules, compilation, proof of the main
theorem, classical queries, regimes, black box, Lean); Appendices A--J with
J the provenance record (84 entries). The PDF contents confirm the
structure (Appendix G p. 164, H p. 170, I p. 177, J p. 179). The proof of
Theorem 1.2 in Section 7 is complete and cites the right lemmas; its error
accounting ($\eps/3$ Fourier, $\eps/3$ approximation, solver share unused)
matches Theorem 6.1(iii) and `lem:hybrid`. The Lean section's guard counts
sum correctly (263 + 165 + 86 = 514; the sub-totals 21, 33, 21, 29, 14 in
the text match the table rows).

Residue grep (comments stripped, Appendix J excluded) for owner, AI
session, agent, integrator, referee, previous version, withdrawn, artifact,
report, note, Codex, Gemini, Claude, overnight, pass, project, claim gate,
reduction record, cockpit, handoff, session, parent, dates: the only hits
that are not mathematical uses ("forward pass", tree "parent", "the check
succeeds", "chain-pass scan", citation keys ending in 2026) are:

- main.tex:79--80 "the corresponding claim gates of the reduction record
  (speedup allowed, total gate bound) are false" (Style 1);
- main.tex:75 and :374 "a cited report" / "a cited note or report" in the
  definition of the label "argued" (Imprecision 5);
- main.tex:913 "computed from recorded artifacts" (Style 4);
- main.tex:202 "an AI-only reading" (acceptable: it describes the status of
  the import);
- main.tex:120 "at the time of writing" (acceptable).

`\file{}` occurs only in `appendix-provenance.tex`. The restructure record's
remaining owner items stand: the decided ranges of $E_2(8)$, $E_2(9)$
(appendix-schedule2.tex:559, 636) were not refreshed from the scan outputs
and this referee did not check them; referee 14 S2 (unlabelled headers) and
S8 (letter reuse in Appendices B, C) are not applied. The README now lists
the four new appendix files (README.md:23), contrary to the record's note.

## 3. Consistency with the core

Method: the same extractor on `core/main-core.tex`, matched by label
(scratchpad `ref19/cdiff.out`). 25 core environments; 17 share a label
with the companion, 8 do not (`lem:fourier`, `lem:lifted-source`,
`lem:instrument`, `lem:bezout`, `cor:approx`, `rem:zero-sum`,
`rem:is-printed`, `rem:proof-uses`).

- `thm:main`: identical statement except the name of the count ($Q$ here,
  $Q_{\mathrm q}$ in the core; Style 3), the pointer for $B_d$ (Theorem
  `thm:is-import` here, `eq:Bd` there) and the header (Style 2). The
  sentence after the theorem (evaluation points $1,\dots,c$, Schedule 1,
  $M_d = B_d(g_d)$, $\tau = 1$ once $p \ge 3/\eps$) is present
  (main.tex:198).
- `prop:descent`: companion says "every valid nonzero witness" and "on
  $\bar G$" where the core says "every nonzero solution" and "on $Q$"; same
  content.
- `lem:central`: companion adds the clause "Measure $\{\Pi_\lambda\}$ on
  $\rho_H$." Same.
- `lem:homogeneous`, `thm:rees-cover`, `prop:single-evaluation`: identical
  up to $\lambda$ for $\theta$ and the explicit definition of $\A$ in the
  companion statement.
- `thm:uniform-compilation`: companion (i)--(iv) contain the core's (i)--(iv)
  with more detail (explicit recurrence, the four passes, Kitaev plus
  Dawson--Nielsen, Lemma `lem:qft-mod`, $p = 2$ case); "prime factors at most
  $d$" agrees.
- `prop:classical-query`, `lem:collision`, `rem:query-separation`: same
  statements ($u$ for $\ell$; the companion adds the display of
  $Q_{\mathrm q}$ and the $2^{\Omega(L_{\mathrm{in}})}$ form, which is
  correct for $m \ge 2$ since $(m-1)/(2m) \ge 1/4$).
- `thm:is-import`: same hypotheses and conclusion; the time bound is written
  "$\poly(M,\log p)$" here and "polynomial in $M$ and $\log p$, where the
  polynomial depends on $d$" in the core (Imprecision 1).
- `rem:is-import`: the companion folds the core's `lem:bezout` and
  `rem:is-printed` into (b) and (c), with the Lean pointer `ReesSdeGcd`.
- Core-only lemmas: `lem:fourier` (failure bound $1/((p-1)p^\tau)$) appears
  in Section 4.2; `lem:lifted-source` as the prose after `lem:homogeneous`
  (main.tex:418) and in the proof of Section 7; `lem:instrument` as the
  instrument description of Section 3 (main.tex:493); `cor:approx` as the
  approximation item of Section 4.2 and Theorem 6.1(iii); `rem:zero-sum`
  (Davenport constant, the $p = 5$, $d = 4$, $a = 2$ example) in Section 5.1;
  `rem:proof-uses` is covered by `rem:main-solver` and the "steps behind
  Theorem" paragraph of Section 7. Appendix J item P2 states this mapping.

No core result is stronger in the companion in a way that is not proved
there; no core result is missing.

## 4. Spot reading of the named places

Appendix A barrier results (appendix-schedule2.tex:401--481). Checked by
hand: `lem:app-s2-kwise` (nonnegativity of $P_\theta$ for $\theta \le 1/2$,
the vanishing marginals of $W$, the converse via the Fourier expansion and
the atom $\theta^{\kappa-2}(1-2\theta)$); `prop:app-s2-barrier` (the bound
$\theta \le h^\kappa/p^{\kappa-1} < p/\kappa^\kappa \le 1/2$, the
construction $(B_jm_j)$, the monotonicity of $c_m$, $d_m$, the identities
$c_{m'} - c_a - c_b = (1-\kappa^{-a})(1-\kappa^{-b})$ and
$d_{m'} - d_a - d_b \ge 0$, $\eta_{\kappa-1} \ge \sqrt6\cdot 4/9 > 1$, the
$13/36$ and $0.02$ constants with $p \ge 7$, hence the factor $0.4$);
`prop:app-s2-chebotarev` (ramification case $p = 2$, $\kappa = 2\kappa'$;
reduction of cells into one coset; two vanishing cells in row 0 excluded by
`lem:app-s2-two-rows`; density by Chebotarev on the Galois closure);
`rem:app-s2-four-cycle` (the substitution $\beta_i + \alpha_j =
(\alpha_j - \alpha_{j'})w$, the cancellation of
$\chi(\alpha_j - \alpha_{j'})$ by $\sum e_k \equiv 0$, the diagonal term,
$|S_e| = p^{2\kappa-2}(p-1)$ in both cases, the count
$\binom{\kappa}{2}^2(\kappa-1)^3 < \kappa^7/4$). All correct as stated.
The hypothesis $|J(\psi,\psi')| = \sqrt p$ keeps its NEEDS HUMAN
VERIFICATION comment.

Coherent-receiver section (main.tex:840--910). Lemmas
`lem:coherent-linear-sde`, `lem:coherent-quadratic-sde`,
`lem:coherent-power-sde` and `prop:coherent-receiver` are unchanged in
content from the archive apart from pointers; the proposition's error claim
$1 - 2\eps/3$ matches Section 7, its cost bound uses
$Sn_dM_d \le Q/c$ correctly, and the closing paragraph keeps the existence-
only disclaimer. The back-reference "the rule of Section~\ref{sec:sde}"
resolves to Section 4 (the descent), where the $s_i = 0$ rule is stated.

Lean section (main.tex:1288--1382). Facts only, no paths, no dates; counts
consistent (above). The "Inside and outside the boundary" paragraph is
unchanged in content.

Appendices G, H, I (new files). Status paragraphs present; cross-references
resolve (the build reports none undefined). Appendix H's table
`tab:backends` (main.tex:815) and the prose agree on every qubit and gate
number checked (82/5528, 744, 154/231210, 835/2997844, 182/115282,
1198/2694596, 1629/4832806, 20566/83492540, 304234, 5035924).

Provenance appendix (appendix-provenance.tex). 84 entries, each with a
Status line; one "AI session" (line 146) remains in a Source line, which is
appropriate there. A script compared each entry's Status words with the
headers of the results it names: the only substantive mismatch is item P7
(Imprecision 2); the others are entries that describe parts or checks
("finite computation" for the tests of a proved result) and are fine.

## Findings

### Imprecision

**I1.** `main.tex:613` (`thm:is-import`). Current: "in time
$\poly(M,\log p)$." The companion has no convention that $\poly$ may depend
on $d$ (elsewhere it writes $\poly_c$ for dependence on $c$), and the core
was changed by referee 17/18 to make this explicit. Proposed:

```latex
in time polynomial in $M$ and $\log p$, where the polynomial depends on $d$.
```

**I2.** `appendix-provenance.tex:38` (item P7) versus `main.tex:625`
(`rem:is-runtime` header) and `appendix-sde-side.tex:11`
(`rem:sde-side-tape` header). P7 says the Turing-machine bounds
$T^{\mathrm{IS}}_d$, $T^{\mathrm{IS},\ast}_d$ are "argued with explicit
constants left uncomputed", while both headers carry only "AI-checked,
pending human review" and the paragraph after Theorem 1.2 (main.tex:210)
says the tape layout is "sketched". Under the paper's own convention
(main.tex:374) "argued" means the proof is only in a cited source, which is
not the case here (the sketch is in Appendix G.1). Proposed: in P7 replace
"argued with explicit constants left uncomputed" by

```latex
derived in Remark~\ref{rem:sde-side-tape} as a sketch, with the absolute constants $C_1$, $C_2$, $C_3$ not computed
```

and in the two headers append "; Turing-machine bounds sketched, constants
not computed". Same alignment for `rem:two-level-threshold-size`
(`main.tex:676`): its body says "status: argued" for the central-moment
threshold but the header does not; propose the header

```latex
\begin{remark}[Size of the two-level threshold; the central-moment threshold argued; AI-checked, pending human review]
```

**I3.** `main.tex:1202` (`thm:bb-envelope`(iii)). The archive statement
said that the chart-acquisition count holds with the rotations
$R_j^{\pm1}$, $\mathrm{C}R_j^{\pm1}$ of Lemma `lem:qft-mod` counted as
single gates, and that over a fixed finite gate set it is multiplied by
$\operatorname{polylog}(\ell kd/\eps)$. The new (iii) states the three gate
counts without this convention; it survives only in
`prop:tb-count-gates`(b). Since Theorem 1.2 counts gates over a fixed finite
set, a reader of (iii) alone gets a different gate model. Proposed, after
"$O(s\ell^3(\ell+\log(s/\eps)))$ gates.":

```latex
(the rotations of Lemma~\ref{lem:qft-mod} are counted as single gates; over a fixed finite gate set every count is multiplied by $\operatorname{polylog}(\ell/\eps)$, which the $o(1)$ in the exponents below absorbs)
```

**I4.** `main.tex:1202` (`thm:bb-envelope`(iii)). "In the input size $N$
below" refers forward to the paragraph after the theorem, so the statement
is not self-contained. Proposed: replace "In the input size $N$ below" by

```latex
In the input size $N = s\ell + w + \log(1/\eps)$
```

and in the following paragraph write "For fixed $c$ and this $N$, ...".

**I5.** `main.tex:75` and `main.tex:374`. The label "argued" is defined
twice, as "a statement whose proof exists only in a cited report" and "a
statement whose proof is only in a cited note or report". The reports are
no longer cited in the text; they are reachable only through Appendix J.
Proposed, in both places:

```latex
\emph{argued} marks a statement whose proof is given only in a source listed in Appendix~\ref{app:provenance}
```

### Style

**S1.** `main.tex:79--80` (Status paragraph). "the corresponding claim gates
of the reduction record (speedup allowed, total gate bound) are false" is
project-internal (the JSON claim gates are listed in P1). Proposed: delete
the clause after the semicolon, so the sentence ends "no general SDE solver
and no human review." The P1 entry already records the gates.

**S2.** `main.tex:176`. Header "Proposed explicit-Lie theorem" where the core
has "Main theorem"; the two papers state the same theorem and the companion
calls it "the main theorem" in Section 7. Proposed:
`\begin{theorem}[Main theorem]`. Also: the restructure record should state
that `thm:main`, `def:input-contract`, `rem:main-solver`, `rem:is-import`,
`thm:uniform-compilation`, `lem:collision`, `prop:classical-query` and
`rem:query-separation` were synchronised with the referee-18 core (they
were, correctly; the record says only that no statement changed status).

**S3.** `main.tex:176--195` and `main.tex:1080`. The query count is $Q$ in
Theorem 1.2 and in `rem:main-solver`, but $Q_{\mathrm q}$ in
`rem:query-separation` and in the core; `prop:classical-query`(v) and
`prop:coherent-receiver` also use $Q$ with their own meanings. Proposed:
write $Q_{\mathrm q}$ in Theorem 1.2(3)--(4), in the sentence after it and
in `rem:main-solver`, as the core does.

**S4.** `main.tex:913`. "computed from recorded artifacts" (project jargon).
Proposed: "computed from the recorded runs (Appendix~\ref{app:provenance},
item~\ref{prov:gc-profiles})".

**S5.** Pre-existing macros the owner's style rule excludes, untouched by
the restructure and not new: `\mathsf` in `appendix-torsion-blackbox.tex`
(20 occurrences, the names $\mathsf{RtF}$ and similar),
`appendix-free-coordinate.tex:88, 92`, `appendix-schedule3.tex:124`; `\ni`
in `appendix-schedule2.tex:71, 563` and `appendix-torsion-blackbox.tex:460,
977`. The restructure record's "no new `\mathsf` ... or `\ni`" is correct.
Proposed: `\operatorname{RtF}` for the algorithm name, `\mathrm{...}` for the
other `\mathsf` uses, and `0 \in K`, `x \in S`, `p^{e-a_t}r_t \in \langle
R_t\rangle` for the `\ni` uses. Owner's call; the core has none of these.

**S6.** `main.tex:1292` (Lean section, first paragraph). One sentence of
about 190 words lists every module without a clean-copy build. Proposed: an
`itemize` with one item per group (SDE modules; class five; class six and
the two SDE modules; class seven; solver and merge; `ReesS2Local`), each
with its guard count and status label, keeping the words.

## For the owner (not findings)

- The decided ranges of $E_2(8)$ and $E_2(9)$ quoted in
  `appendix-schedule2.tex:559, 636` were not refreshed from the scan
  outputs (restructure record); not checked here.
- Referee 14 S2 and S8 remain unapplied, as the record says.
- The archive directory name and the README both describe the pre- and
  post-restructure states consistently; the README's dated "Update"
  paragraphs are a project log by design and were not assessed as paper text.

## Verdict

Ready to send to human experts alongside the core after I1--I5 and S1--S2
(S3--S6 optional). No Error, no Gap. The restructure preserved every
result, proof and status label; the three large moves are intact; the core
is contained with equal or more general statements.
