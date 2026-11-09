# prov: consistency check of the Provenance and Verification Record (9 Nov 2026)

Checker `prov`. This check was done by AI only; no human has reviewed it. It checks
consistency, not proofs.

## Header

**Scope.**
- `T/appendix-provenance.tex`, lines 1-374: all 89 items, including:
  - the three 9 Nov items `prov:dl-central-scalars`, `prov:bb-corollary` and `prov:bb-corollary-pe`;
  - the two `% E2-UPDATE` comments (lines 56 and 281-284);
  - the new Checks sentence of `prov:s2-exceptional` (line 288).
- For every item I checked:
  - (a) each cited path exists;
  - (b) each `\ref` label exists, and the item's status, parameters and numbers agree with the statement it describes (headers and the named passages of `T/main.tex` and `T/appendix-*.tex`);
  - (c) quoted numbers agree with the body, and with the cited output files (spot checks by grep or by read-only scripts);
  - (d) the 9 Nov items describe their files accurately;
  - (e) no private names, and no claims of human review, novelty, speedup or hardware.
- No proofs were checked. Apart from reading files and two trivial counts, I ran no computation (about 1 core-minute in all).
- Scripts and outputs are in `O/prov/`.

**Files checked (shasum).**

| shasum | file |
|---|---|
| 2545e44aeb3ff7f97a204932c46f20ac8c77ec62 | `T/appendix-provenance.tex` (374 lines) |
| 0ed1a1f82b13fef77fc94a48e35efc93f8d23ee4 | `T/main.tex` |
| 8abf0e08ebeb059ba862bf7b0c905e38b1ae3624 | `T/appendix-schedule2.tex` |
| 4966e7646cc5737cf5bf1f0feda9f8a3e7875e04 | `T/appendix-schedule3.tex` |
| ec9ab51739f4305beea3e64705f61d9b5370e9f6 | `T/appendix-free-coordinate.tex` |
| f8553ee2c6474d9daa36b12716a9d8ac46d3ad35 | `T/appendix-subspace.tex` |
| 0f89bd2386391c0277f5396de97f51d8cc0919ed | `T/appendix-torsion-blackbox.tex` |
| 844ef46f6487fef0bbd4d0a95adbdd72a9f3a406 | `T/appendix-codimension.tex` |
| 9b7379e908ca7e5dd0d7aec5d7351b84bd6f9267 | `T/appendix-sde-side.tex` |
| 020a873804d10f895c46de144c15f2f7b042a968 | `T/appendix-backends.tex` |
| fc8a2ac43259e4b763ee85c5e421e8e930b56159 | `T/appendix-filters.tex` |
| c7e587fbc60d3c4a24b95db17c69f8537aefef92 | `T/numbers.tex` |
| e8e1b9b9361491dc66101c61db019b4b5967a41f | `O/diffs/patch9nov-appendix-provenance.tex.diff` |

**Verdict: MINOR ONLY.** There is no GAP and no BREAK. Three findings (1-3) are ERROR-level:
false sentences of the record, none of which affects a stated result. The rest are
status-wording inconsistencies and missing citations.

## Findings (most severe first)

### 1. ERROR: stale counts for the black-box end-to-end control
**Where:** `appendix-provenance.tex:199` (`prov:bb-corollary`), and the body at `main.tex:1277`.

**The text.** It says "four groups of order up to $5^5$, $30$ hidden subgroups, all recovered;
two negative controls rejected".

**What the cited folder holds.** `research/audits/reviews/2026-11-08-rees-blackbox-e2e/` has
five runs:

| run | hidden subgroups |
|---|---|
| heis5_s3 | 8 |
| affine5 | 8 |
| affine7 | 6 |
| free23_5 | 8 |
| ut5_5 | 8 |

That is 38 hidden subgroups. Every one has `blackbox_subgroup_recovered` and
`recovered_equals_log_H` true (script `O/prov/e2e_counts.py`, output `e2e_counts.out`).
- ut5_5 is a subgroup of UT_5(F_5), abstractly the free23_5 group. It was added on 9 Nov
  12:37-12:47 (README.md lines 21 and 43-50).
- There are now three negative controls. Two (the naive pullback and the single kernel
  sample) are rejected in all five runs. The third (9 Nov) is a forced strict subkernel
  K' ⊊ K. It applies only to heis5_s3, and every public check accepts it
  (`chart_exp_homomorphism` true; README lines 32-41). This is the error term the corollary
  allows, but the item does not record it.
- The body sentence at `main.tex:1277` says "three small unitriangular matrix groups and ...
  the free two-generator class-three group of exponent $5$". It omits the ut5_5 run. Its
  "exhaustive or sampled as recorded" can now be "exhaustive": all five runs are exhaustive
  (README, 9 Nov).

**Fix at line 199:** "(five groups of order up to $5^5$, $38$ hidden subgroups, all
recovered; the naive pullback and the single kernel sample rejected by the public checks in
all five; a forced strict subkernel, applicable to the Heisenberg run only, passes every
public check, as the error term of the corollary allows; ...)".

**Fix at main.tex:1277:** "on four small unitriangular matrix groups (one of them, in
$\UT_5(\mathbb{F}_5)$, isomorphic to the next) and on the free two-generator class-three
group ...".

### 2. ERROR: wrong source locators (three items) and one imprecise locator
Scripts: `O/prov/locators.py` and `locators2.py`. They print the heading of every cited
section next to the item's description; outputs are `locators.out` and `locators2.out`.

- **(a) `prov:s2-chains`, line 275.** The item says "Section~4.6 the line-probability bound".
  - Section 4.6 of `2026-11-05-rees-threshold-7.md` is "Routes B.1-B.3" (Proposition 4.6,
    Proposition 4.7 and Lemma 4.8). It contains no probability bound.
  - The bound displayed in `rem:app-s2-chains-scope` (`appendix-schedule2.tex:637-654`) is
    Theorem 3.1 of Section 3 ("The bounded-excess barrier [proved]", report lines 245-252).
    The expressions agree: θ_r = (κ−1+p^{−r})/κ. Its reading for schemes is Corollary 3.3.
  - The pointer matters: the body sends the reader to this item for the proof ("not
    reproduced here, see ... item prov:s2-chains").
  - **Fix:** "(Proposition~4.6 is the projection statement; Theorem~3.1 of Section~3 is the
    line-probability bound and Corollary~3.3 its reading for round schemes)".
- **(b) `prov:fc-lower`, line 327.** The item cites "(Section 5)".
  - `prop:rc-lower` (main.tex:786) is Propositions 6.1 and 6.2 of Section 6, "Lower bounds"
    (lines 269-289 of `2026-11-02-rees-schedule3-cost.md`): the Markov bound for
    uniform-kernel rejection and the bound for bank-oblivious designs.
  - Section 5 is Theorem 5.1, Lemma 5.2 and Proposition 5.3 (the W+FCS rule, law transfer,
    k-level FCS).
  - **Fix:** "(Section 6, Propositions 6.1 and 6.2)".
- **(c) `prov:fc-numbers`, line 322.** The item cites "(Section 6, the six primes of part~(ii))".
  - The class-nine numbers at the six primes p ≥ 5184 (5281, 105019, 2^31−1, 2^61−1,
    194522647344910884721, 2^127−1) are rows of the table in Section 9, "Class-9 numbers"
    (lines 342-362).
  - Section 6 has no such table.
  - **Fix:** "(Section 9, the rows $p \ge 5184$ of its table)".
- **(d) `prov:tb-evaluation`, line 358 (imprecise rather than false).** The item says
  "Section~2: the lemma checked exactly on $\UT_{c+1}(\mathbb{Z}/p^e)$ and on relatively free
  groups built in GAP at $p = 7, 11$, $e = 2, 3$, $c = 5, 6$".
  - Section 2 of `2026-11-02-rees-prime-power-compiler.md` holds the theorem and its proof.
    The exact checks are in Section 3 (UT targets: ten (p,e,c), with e = 3 at c = 6 only
    when p ∈ {7, 11}) and Section 4 (GAP groups with M = p^2, i.e. e = 2 only).
  - The same parameter phrase appears at `appendix-torsion-blackbox.tex:780-782` and
    `main.tex:1245`. Read as the union of both checks it is not false.
  - **Fix:** "(Section~2: the proof; Sections~3 and~4: exact checks on
    $\UT_{c+1}(\mathbb{Z}/p^e)$ at ten $(p,e,c)$ with $c \le 7$, and on relatively free groups
    built in GAP at $p = 7, 11$, $e = 2$, $c = 5, 6$; Section~6: ...)".

### 3. ERROR, inside the E2-UPDATE (8) spot: wrong source for the intermediate decided ranges
**Where:** `appendix-provenance.tex:287` (`prov:s2-exceptional`).

**The text.** "decided ranges up to $13873$ for $\kappa = 8$ and $16363$ for $\kappa = 9$
there, ...; $14281 \in E_2(8)$, $18199 \in E_2(9)$". Here "there" is
`2026-11-03-rees-dfs2-prune.md`.

**What that report says.** It was last modified 4 Nov 11:46. Its §4 (lines 196-207) says:
- κ = 8: decided for p ≤ 4201 plus listed primes; largest known element of E_2(8) is 8009;
- κ = 9: decided on [3584, 5689] plus listed primes; largest known element is 17551.

None of 13873, 16363, 14281 or 18199 occurs in it.

**Where the numbers come from.** They are the dfs2b snapshot of 5 Nov, 06:40-06:49 AEDT,
recorded in `2026-11-04-rees-k9-sweep.md` §6 (lines 300-308: "This is what the paper's dfs2b
snapshot now quotes (I223)"). The comment at line 281 repeats "(dfs2-prune source)".

**For the update pass:**
- cite k9-sweep §6 for that intermediate snapshot, or drop it in favour of the new snapshot;
- keep dfs2-prune for the prunes and for the 6073/6067 agreement, which it does contain.

### 4. MINOR: `prov:sde-decoupled` uses the defined label "argued" for results Appendix A proves
**Where:** `appendix-provenance.tex:57`.

**The text.** "the Weil bound and the second moment over $\beta$ argued in the sources".

**Why it is inconsistent.** Under the convention at `main.tex:74-75` and `main.tex:386`,
"argued" means the proof is given only in a source. But:
- `cor:app-s2-decoupled` (`appendix-schedule2.tex:360`) proves the same statement from
  `prop:app-s2-TW` and `prop:app-s2-TA`, with full proofs in the appendix;
- items `prov:s2-main` and `prov:s2-TA` call these "proved".

This is the same class of issue as referee 19's I2.

**Fix:** "Status: conditional as stated (Corollary~\ref{cor:app-s2-decoupled} proves it
from Propositions~\ref{prop:app-s2-TW} and~\ref{prop:app-s2-TA}, items~\ref{prov:s2-main}
and~\ref{prov:s2-TA}; the second-moment part re-derived independently); ...".

### 5. MINOR: one statement, two status words
Appendix items call proved what the body and a sibling item call conditional.

- **(a) Schedule 2 theorem.** `prov:s2-main` (line 250) says "proved" for `thm:app-s2-main`.
  That theorem is `thm:power-sde`(ii), which is conditional in the body (`main.tex:697`;
  `main.tex:712`: "No human has read the proof, so part (ii) stays conditional") and in
  `prov:sde-power` (line 51).
- **(b) Decoupled corollary.** `prov:s2-TA` (line 254) says "proved" for
  `cor:app-s2-decoupled`, which is `prop:decoupled-sde`, conditional at `main.tex:714`.
- **(c) Schedule 3 theorem.** `prov:s3-main` (line 294) and `prov:fc-main` (line 302) say
  "proved in Appendix" for `thm:free-coordinate` (iv) and (i)-(iii). The header at
  `main.tex:769` and `prov:sde-fc` (line 87) say these are conditional on the steps behind
  Theorem main.
- **(d) `prov:sde-fc`, line 87.** It folds `prop:rc-lower` into "conditional", although the
  header at `main.tex:786` has no condition and `prov:fc-lower` says proved. It also says
  "and on the label law", while `main.tex:784` says the label law "is not an extra
  hypothesis" (it is derived in Lemma s3-law).
- **(e) `prov:pr-fpt-r`, line 174.** It says "(on Theorem~\ref{thm:main} and ...)", but
  `cor:fpt-r`(i) is conditional on "the steps behind Theorem main" and on
  Theorem free-coordinate(iii).

**Fix.**
- Append to s2-main, s2-TA, s3-main and fc-main: "(the body statement keeps its conditional
  label; item~\ref{prov:sde-power} / \ref{prov:sde-decoupled} / \ref{prov:sde-fc})".
- In sde-fc: "Theorem~\ref{thm:free-coordinate} conditional on the steps behind
  Theorem~\ref{thm:main} (the label law derived in Lemma~\ref{lem:s3-law}, not assumed);
  Proposition~\ref{prop:rc-lower} proved (item~\ref{prov:fc-lower}); ...".
- In pr-fpt-r: "on the steps behind Theorem~\ref{thm:main} and on ...".

See also "For the human expert", point 1.

### 6. MINOR: `prov:dl-central-scalars` (9 Nov, lines 24-26) omits its check report and the p = 11 run
**What I verified (all agree with the item and with `prop:dl-central-scalars`, main.tex:464-489):**

| file | content |
|---|---|
| `autp_p5.out` | \|Aut\| = 976562500 = 4·5^12, image on Z C2×C2, scalars [1, 4] |
| `autp_p7.out` | 166095446412 = 12·7^12, image D12, scalars [1, 6] |
| `brute_p3.out` | 12 classes, scalars [1, 2] |
| `split_check.out` | p = 13, 5, 17, 29: 15 checks each, ALL OK |

**Omissions.**
- **(i) No Source or Checks line.** The independent referee report
  `research/audits/reviews/2026-11-09-rees-dl-scalars-schedule2-referee.md` is not cited
  anywhere in the paper. Its claim 1 is "CORRECT, proof complete for every field of char not
  2". It includes Gröbner-basis checks over the algebraic closure (`dl.sage`, `dl3.sage`,
  `der.py`, `results.out` in its folder): only {1, p−1} at p = 3, 5, 7 and 11. Its wording
  fix W2 is applied at `main.tex:254` ("beyond $\pm1$").
- **(ii) The folder's `*.out` includes `autp_p11.out`:** "timed out after 300 s at nice 19".
  The item does not say so, and `pc11.g` is not named.

**Fix:** append "The GAP run at $p = 11$ did not finish in $300$ s (\file{autp_p11.out}).
Checks: \file{research/audits/reviews/2026-11-09-rees-dl-scalars-schedule2-referee.md}
(Section~1: an independent Gröbner-basis computation over $\overline{\mathbb{F}}_p$ finds
only $\pm1$ at $p = 3, 5, 7, 11$; scripts and output in the folder of that name)."

### 7. MINOR: 9 Nov black-box items, missing check reports and a stale `prov:bb-chart`
- **(i) `prov:bb-chart` (lines 193-195) is out of date.** It describes `thm:bb-envelope` as
  it was before 9 Nov. The theorem now treats e_p > 1 by the socle recursion of
  `cor:black-box-pe` with `rem:oblivious`, and no longer depends on `thm:ring-to-field`(iii)
  (`O/diffs/patch9nov-main.tex.diff`, hunks @@ -235 and @@ -1208).
- **The check of that change is cited nowhere.** It is claim 2 of the dl-scalars-schedule2
  referee: "CORRECT in substance", with gaps G2.1-G2.4. The text contains the fixes for those
  gaps: `rem:oblivious` now says "every function $f$", reduces measured coordinates modulo p,
  and uses a 4T cut-off with Phase 0 inside. Neither `prov:bb-chart` nor
  `prov:bb-corollary-pe` cites this referee report.
- **(ii) `prov:bb-corollary` omits `2026-11-09-rees-blackbox-citation-check.md`.** That
  report checks the Khukhro and Cicalò-de Graaf-Vaughan-Lee locators; its outcomes are now in
  `main.tex:171`, 177, 180 and 277.
- **(iii) Two checks have no file of their own.** These are "an adversarial AI review"
  (bb-corollary) and "one independent AI check" (bb-corollary-pe). The first is known only
  from the draft's header comment; the second only from the "Disposition" section of the
  exponent-pe report (lines 214ff). Add "(not kept as a separate file)".

**Fix for bb-chart:** add "Checks: \file{...-dl-scalars-schedule2-referee.md} (claim~2: the
case $e_p > 1$ through Corollary~\ref{cor:black-box-pe} and Remark~\ref{rem:oblivious})".
Cite the same report in bb-corollary-pe for `rem:oblivious`.

### 8. MINOR: E2-UPDATE spots, internal consistency
Everything else in the two E2 spots is internally consistent (see "Checked and correct").
These three points are not.

- **(i) The new Checks sentence (line 288) is under-qualified.** It says the cloud solvers
  re-decided "$145$ primes in $(9769, 20000]$ for $\kappa = 8$ ... all with the verdicts of
  the pruned search".
  - That interval holds 265 primes ≡ 1 (mod 8). The 145 are those the pruned search had not
    decided on 4 Nov, which the body says at `appendix-schedule2.tex:723`, and so does the
    harvest report.
  - **Fix:** add "(those the pruned search had not decided on 4~November)".
- **(ii) The Checks sentence and the retained snapshot disagree.**
  - 77 of those 265 primes lie above 16993. The retained snapshot (line 289, 5 Nov 10:37:
    κ = 8 decided to 16993, next undecided 17033) says the pruned search had not decided
    them at that time.
  - Their pruned verdicts exist only in later files. For example, `FEASIBLE k=8 p=17033` is
    in `small-prime/dfs2b_k8_hi_q0.out` (modified 5 Nov 12:59) and in
    `dfs2b_k8_6362_20000.out` (6 Nov 12:23).
  - So the Checks sentence and the snapshot become consistent only once the planned new
    snapshot replaces the old one.
  - **Acceptance test for the update:** the new snapshot time is no earlier than the last
    pruned verdict in (9769, 20000].
- **(iii) "the $29$ primes $\equiv 9 \pmod{16}$ in $(20000,49417]$" (line 289) is misleading.**
  It reads as if these were all such primes, but there are 339
  (`O/prov/e2_consistency.out`). The 29 are the ones left unresolved
  (`2026-11-04-rees-threshold-5.md` line 34: "The remaining 29 primes, all ≡ 9 (mod 16)").
  - **Fix:** "the $29$ primes of $(20000,49417]$ left without a contraction, all
    $\equiv 9 \pmod{16}$".

### 9. MINOR: `prov:sde-worst-case`, line 75, over-attributes "repeated with independent code"
- The phrase is right for N(3,2,p), N(4,2,17) and the bounds on G*_3(p) (`nmax.py` and
  `gstar.py` in §2 of the check report).
- It is not right for the 48 planted trials or the 2,520 banks. Those are the source report's
  runs (`2026-11-05-rees-sde-worst-case.md` line 62; check report item I5). The check ran
  other banks: 4,840 in general position and the adversarial families.
- The body (`appendix-sde-side.tex:74`, 76) makes no such claim for them.

**Fix:** "...; the values $N(3,2,p)$, $N(4,2,17)$ and the bounds on $\mathcal{G}^*_3(p)$
finite computations, repeated with independent code; the $48$ and $2{,}520$ trials finite
and sampled computations of the source, with further independent runs on other banks in the
check; ...".

### 10. MINOR: `prov:cd-checks`, line 372, says "$400$ groups built by brute force"
`main()` of `2026-11-02-rees-codimension/group_check.py` runs 400 (G, H) cases. These are two
filiform groups with four subgroups each, plus 392 randomly generated groups of upper-
triangular matrices, which need not be distinct. Its output `group_check_out.txt` says
"cases (G,H): 400; runs: 800". The wording is inherited from the source report.

**Fix:** "$400$ pairs $(G, H)$ (two filiform groups and $392$ random groups of unitriangular
matrices)".

### 11. MINOR: `prov:core`, line 20, has a containment cross-check dated 5 Nov
- On 9 Nov both papers gained `cor:black-box`, `cor:black-box-pe`, `prop:dl-central-scalars`,
  `rem:oblivious`, `rem:black-box-scope` and `rem:black-box-pe-source`.
- I compared the `+` lines of `O/diffs/patch9nov-core_main-core.tex.diff` with `T/main.tex`,
  without reading `T/core` (`O/prov/core_vs_main.py` → `core_vs_main.out`). The statements are
  the same up to status tags and cross-references. `rem:oblivious` is more general in the
  companion (combined rule, cut-off), and `rem:black-box-scope` is reworded. So containment
  plausibly still holds, but the record does not say so.

**Fix:** append "; the six statements added to both papers on 9~November~2026 have the same
text up to status tags and cross-references, Remark~\ref{rem:oblivious} being more general
here".

### 12. MINOR: status wording
- `prov:cl-app3` (line 166) has "Status: argued, not proved here; pending human review." It
  lacks "AI-checked", although line 6 says every status is AI-checked.
- `prov:pr-ring` (line 178) and `prov:bb-chart` (line 194) write "AI-checked only". The
  convention elsewhere is "AI-checked, pending human review".

## Checked and correct

- **(a) Paths, all 89 items** (`extract.py`, `resolve_bare.py`):
  - 338 `\file` paths resolve at the repo root.
  - 70 bare names, `.../` abbreviations and globs resolve against the item's own folder or
    against `research/audits/reviews`.
  - Six do not resolve, and none is an error. Three are `verify_schedule2.py`, which the text
    itself says is not kept in the repository. The other three are the phrases "the matching
    `.log`/`.out` files", which name no file.
  - `numbers.tex`, `main.tex` and `make_numbers.py` resolve under `docs/papers/rees-hsp/`.
- **(b) Labels.**
  - All 370 `\ref` targets exist, and no label is defined twice.
  - Every `prov:` label cited by the body exists. The three new items are cited from
    `main.tex`.
  - The order of the entries follows the paper, grouped by topic (`order.py`).
  - Each of the 89 items has exactly one Status line.
- **(e) Scan for names and claims.**
  - The only names are those of cited authors or theorems (Dixmier-Lister, Ivanyos-Santha,
    Ettinger-Høyer-Knill, van de Woestijne, Benjamini-Gurel-Gurevich-Peled, Deligne-Katz,
    Tonelli-Shanks, Moore forms, Dynkin, Bonferroni). There is no private correspondent.
  - Line 6 says "The reports are AI-written; none is a human review", and line 201 says "no
    novelty is claimed".
  - There is no claim of speedup or of execution on hardware ("qubit counts" are circuit
    counts).
- **`prov:dl-central-scalars`:** data as in finding 6, and the status "proved" matches the
  header of the proposition.
- **`prov:bb-corollary-pe`:**
  - `run.out` SUMMARY: groups 48, subgroups 5359, all recovered, 13900 instances.
  - Readout correct in 958 of 960 trials; the two failures (81_3, 243_2) are rejected by the
    public check.
  - Orders 3^4-3^6, 5^4 and 5^5; class 2-4; exponent 9-125; 40-bit handles.
  - The source's verdict is "holds with fixes", and the fixes are present in the text
    (`rem:oblivious`; no use of ring-to-field(iii); rational ε; the p = 2 transform).
  - The credit to ISS2012 is present, and so is "does not exercise Theorem main" (body
    `main.tex:1303`).
- **E_2 data (`e2_consistency.py`).**
  - Next undecided primes are 17033 and 16651. The κ = 9 list is prime, ≡ 1 (mod 9) and
    sorted.
  - There are 83 primes ≡ 1 (mod 8) below 2442 and 83 primes ≡ 1 (mod 9) below 3584, and
    82/83 are exceptional in each (small-prime-arity, table of Section 3).
  - 8^8/2 = 8388608, ⌊9^9/2⌋ = 193710244, and 424549 is the largest k9 exception.
  - The reruns over the low ranges give 137/122 primes and 5/4 feasible primes.
  - 20071, 20089 and 20107 are INFEASIBLE in `out/dfs2b_*.out`.
  - Counts: 1534715 (t1-sweep-hi); 1373 and 3098 (k9-sweep); 29 unresolved
    (threshold-5: 661 of 690 resolved).
  - The cloud harvest (indep 9473, 9769, 6073, 17623, 6067; e2k8low 145 with a 110/35 split)
    supports the new Checks sentence, subject to finding 8.
  - E2-UPDATE (7) is consistent: `prov:sde-decoupled` defers κ = 8, 9 to the s2-scope item,
    which covers them.
- **SDE items.**
  - The E_2 sets agree with `prov:s2-small` ({5,13,17,29,37,53}).
  - T_S ≤ 10κ^{κ+1} for 3 ≤ κ ≤ 40, and E_2(7) below 5·10^6.
  - 143 at c = 9 and the triangular-solver numbers agree.
  - `prov:sde-is-solver` agrees; power-sde agrees for r ≤ 14 and in four cases.
  - `prov:sde-is-runtime` carries the referee-19 I2 text.
  - Part labels: `rem:sde-subquadratic` ((a), (c) proved; (b) conditional; κ = 2,
    p ∈ {13, 29}, a = 3); `rem:sde-block-steered` (conditional; E_cg; p ≤ 5000 and
    p ≤ 11000; planted failures); `rem:sde-worst-case-q1` ((i)-(iii) and the reduction;
    sampled stalls; no bound on c); `rem:sde-worst-case` ((a), (b) proved, (c) open; the
    numbers, but see finding 9).
- **Free-coordinate and Schedule 3 items.**
  - Part labels agree for `rem:fc-witness-h3` ((a), (b), (d) proved; (c) from (b)),
    `rem:fc-zero-sum-sis` ((a)-(d)), `rem:fc-zero-sum-arity` ((a)-(c), σ_p imported from
    KMOSW2026 Prop 5.3) and `rem:fc-tradeoff` ((a), (b)).
  - The zero-sum-node JSON values log2 Q = 13.17/24.29/42.32 against 58.85/155.81/676.81
    agree.
  - The six primes p ≥ 5184 agree with appendix-free-coordinate.tex:356.
- **Backends.**
  - Rows 1-7 of `tab:backends` map to gc-control … gc-full.
  - 574/56/92/39 and 14 of 14 agree.
  - p ≤ 127, b ≤ 12, ten configurations, 2·10^6.
  - Twelve configurations = 9 (gh report) + 3 (gh-check §4).
  - The test asserts (c−1)c(c+1)(c+2)//6 (`tests/test_uniform_bch_rees.py`).
- **Lean.**
  - Guards sum to 514 = 263 + 165 + 86.
  - Counts: class five 21; class six plus two SDE rows 33; class seven 21; solver plus merge
    29; S2Local 14.
  - Audit.lean has 552 `#print axioms`.
  - Toolchain and Mathlib are both v4.35.0.
  - The clean-build log shows 2:02:51 and EXIT=0, and ReesSdeGcd is the Bezout module.
- **Ring, codimension and subspace items.**
  - The ring_to_field JSON has seven torsion controls.
  - Codimension outputs agree: 5666, 22664, 19940, 6063, (3,2), (6,3); 400 cases, 800 runs,
    198 transports, 596801 parent queries; 86 cases with maxima 3.308, 12.735 and 2.335.
  - `cd-main` conditions agree with `thm:app-codim`.
  - The subspace profile agrees: p = 43, c = 9, m = 19, n = 97.
  - `thm:bb-envelope` "conditional, AI-checked only" matches `prov:bb-chart`, apart from
    finding 7.
  - The scalar-flag wording of `cor:fpt-r` agrees.
- **Locators.** 49 of 50 section or statement locators name an existing heading or
  statement; the 50th, "items Z1-Z3 and A5", exists too. Content matched by heading title
  except for the four cases in finding 2.

## Not checked / UNKNOWN

- **Numbers from scripts that are not kept.** These come from `verify_schedule2.py`,
  `schedule3_exact_check.py` and `subspace_appendix_checks.py`, which are not in the repo:
  1805 instances, 5476 primes, worst ratio 1.000, 50 tensors, the κ = 6..199 constants, and
  the Schedule 3 and subspace check counts. They cannot be verified from the repository.
  - A plausibility count for 5476 does not reproduce it: there are 5733 primes ≡ 1 (mod κ)
    in the stated ranges for κ = 2..7 (`count_5476.py`). The subset actually used is not
    stated, so this is not evidence of an error.
- **The Lean commit b117b98e** (no git allowed); I only read the build time and exit code
  from the log.
- **`T/core`** (forbidden): seen only through the 9 Nov diff.
- **"Findings applied"** for bb-corollary (referee findings 1-6, 8, 9) and the exponent-pe
  fixes: spot-checked only.
- **`semidirect_check.py`** has no recorded output. I did not run it (p = 3 and m = 4 read
  from its source).
- **The dfs2b outputs are still growing.** I did not recount them at any time; following the
  brief, I checked only internal consistency.
- **Body numbers the items point to but do not quote** (for example 2^{193.9}-2^{236.0} at
  appendix-free-coordinate.tex:359): not compared with files.

## For the human expert

1. **The status convention is used for two different things.** `main.tex:70-72` and 386
   define "conditional" as dependence on a stated hypothesis or an unproved part. But
   `main.tex:712` (and `main.tex:721` for `prop:decoupled-sde`) use it because no human has
   read a proof that is given in full in Appendix A. Decide which meaning holds. Then align
   the appendix items (finding 5), and either define the second use or change the label.
2. **The whole record is AI-written.** Every check report is an AI check, and no item records
   a human check (stated at line 6).
3. **External citations the sources flag:**
   - the σ_p bound imported from KMOSW2026, Prop. 5.3;
   - the numbering of MP13 Theorem 1.1 (marked NEEDS HUMAN VERIFICATION);
   - Khukhro: the citation check could not confirm Thm 10.13 or Lemma 9.15. The body now
     cites §10.2 and Ex. 10.24, which is fine. `main.tex:410` also cites Remark 9.17, p. 109,
     which that check does not list. These need the book.
4. **Uncited 9 Nov reports.** Decide whether to cite the dl-scalars-schedule2 referee and the
   black-box citation check (findings 6 and 7). The non-unique-encoding report is not
   integrated into the paper (by its own statement), so it needs no item.

## Comparison with the earlier report (referee 19, provenance parts)

- **Fixes present and correct:**
  - **I2:** `prov:sde-is-runtime` carries the proposed text verbatim. The headers of
    `rem:is-runtime` (main.tex:668) and `rem:sde-side-tape` (appendix-sde-side.tex:11) say
    "Turing-machine bounds sketched, constants not computed". The `rem:two-level-threshold-size`
    header (main.tex:723) says "the central-moment threshold argued".
  - **I5:** "argued" is defined identically at main.tex:74-75 and 386.
  - **S1:** main.tex:78-79 ends with "no human review".
  - **S4:** main.tex:961 says "computed from the recorded runs (... item prov:gc-profiles)".
  - **I3 and I4** (body, checked by grep only) are present at main.tex:1312.
- **Their "for the owner" item is still open.** The refresh of E_2(8) and E_2(9) is now
  tracked by the E2-UPDATE (1)-(8) comments.
- **Entry counts.** They reported 84 entries, each with a Status line. The 5 Nov 14:35 copy in
  `docs/papers/rees-hsp/` has 86, and the tree has 89 (three added on 9 Nov). Each still has
  exactly one Status line.
- **What they missed.** Findings 2-5, 9, 10 and 12 concern text already present in the 5 Nov
  14:35 copy, so they were not introduced on 9 Nov. Their conclusion that "the only
  substantive mismatch is item P7" is therefore too strong:
  - finding 4 is the same class as their I2;
  - their header-comparison script would not catch the appendix-versus-body pairs of finding
    5, or the wrong locators of findings 2 and 3.
