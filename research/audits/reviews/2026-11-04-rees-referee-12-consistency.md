# Rees HSP: referee 12, whole-paper consistency pass (2026-11-04)

Independent AI referee. I worked only locally: no git, no network, and no .tex file was edited.
Files read: `docs/papers/rees-hsp/main.tex` and the six appendix files it inputs,
`references.bib`, `README.md`, `numbers.tex`, rows I163–I187 of
`research/audits/reviews/2026-11-02-rees-integration-log.md`, and the Rees lines of
`research/STATE.md`. Line numbers refer to the files as they were on 2026-11-04 at about 21:05.

**Counts: 0 Errors, 0 Gaps, 13 Imprecisions, 7 Style.** I found no quantity that disagrees
across files, and no stale E_2 value. Every finding below is a wording, scope or citation issue.

## 1. Build

I copied the sources to `scratchpad/build12/` and ran
`PATH=/Library/TeX/texbin:$PATH latexmk -g -pdf -interaction=nonstopmode main.tex`.

- The build exits 0 and gives 148 pages, matching the README and STATE.
- `main.log` has 0 "multiply defined", 0 "undefined" and 0 Overfull. It has 3 Underfull hboxes,
  all in the bibliography (ISS2012, Lidl–Niederreiter, Nayak). BibTeX gives 0 warnings.
- There are 225 `\label`s and no duplicates. All 42 cited keys are defined. Two entries are
  never cited (FultonHarris1991, HallgrenRussellTaShma2003). `plain` does not print them, so
  they are harmless.
- I scanned for garbled text in the .tex (comments stripped, lines joined, math masked) and in
  `pdftotext` output. The scan looked for doubled words, double spaces, `. .`, `,.`, empty
  parentheses, article pairs, sentences pasted twice, and 9-word n-grams repeated within a
  paragraph. It found nothing. The three doubled-word hits in the PDF text ("and and", "any
  any", "a a") are display-layout artifacts; the source reads correctly. Parenthesis
  imbalances on single lines of `appendix-torsion-blackbox.tex` balance across its hard-wrapped
  lines. README line 9 has one unmatched `(`, and it belongs to the interval
  `(49417, ⌈T_A(8)⌉]`.
- The inline `% NEEDS HUMAN VERIFICATION` comments at main.tex:217, 968 and 1015 swallow no
  prose. The PDF text continues correctly after each.

## 2. The requested cross-checks (all agree)

| Item | Where | Result |
|---|---|---|
| r = ⌈log₂(1600πt)⌉; 1/800 per run; 1/400 per run with synthesis; 1/200 per pair | tb:1448–1471, tb:626–628 | agree; 2πt·2^{-r} ≤ 1/800 follows from r |
| 1/11 per pair; 1/22 per attempt | tb:627, 639, 644–649 | agree; (4/π²)²·6/π² − 1/200 = 0.09485 > 1/11 |
| T = ⌈88ℓ + 176 ln(2s/ε_pre)⌉ | tb:646, tb:1539 | agree; μ = T/22 ≥ 4ℓ + 8 ln(2s/ε), so μ/2 ≥ 2ℓ and e^{−μ/8} ≤ ε_pre/(2s) |
| 7n+6 qubits; 80n²+27n; 160n³ | tb:1456–1460 | agree; (2n+1) + 2n + (3n+5) = 7n+6; 2n(40n+12) + 3n = 80n²+27n |
| τ_c and the cases c = 1, 2, ≥ 3; 23/2 and 21/2; E_W(c)+1, E_W(c)+4 | main:1051–1054, tb:1488–1502, 1549–1553, README:9, STATE | agree in all four places |
| E_W(c) query exponent restricted to c ≥ 2 | main:1062, tb:1403–1409 | agree; the regimes table, notation table and main:944 claim only E_W(c)+1 |
| E_W values 5, 11, 23, 38, 56, 77, 107, 143; 145 and 146 with Schedule 1 | main:351, 684, 944, 1062, 1070; tb:1347–1349; numbers.tex | agree (recomputed) |
| T^IS_d = C₁d³M_db³(g_d²+b²); R_d | main:200, 313, 612, 848 | agree |
| +4bQ and qubit count of prop:coherent-receiver | main:844–848, 868, 871 | agree; I rederived the sum and both qubit counts |
| 11489, 0.99; 14347, 17839, 0.30; 49417; ⌈T_A(8)⌉ = 117441563; 29 primes; E_2(8) ⊆ [3,20000] ∪ X_29 | main:653, s2:470, README:9, STATE | agree; 11489/8^{4.5} = 0.992 and 17839/9^5 = 0.302; T_A(8) = 1.17·10⁸ in tab:app-s2-thresholds |
| Stale values 10321, 10433, 11161, 13537, 13807, 17659, 17713, 0.89, 0.96, 0.29; "(8^8/2, T_A(8)]" open | all files | none left; 8^8/2 appears only as the closed boundary of two covered ranges |
| Class four over F_5: 9 subgroups, 5 nonnormal | main:797 | agree; no other count of that instance in the paper |
| QFT-backend bounds 0.0142, 0.0112, 0.0993, 0.0895, 0.0986; (t,r,τ) | main:793, 795 | agree; I recomputed (t,r,τ) from the conditions of lem:qft-mod for η = 1.5e-3, 2.8e-4 and 2.5e-4 |
| Implemented vs existence-only vs simulated | abstract main:102; 232, 242, 799, 832, 871; README:3, 9 | agree: coherent receiver existence only; witness circuits wired into four backends on fixed instances |
| Conditionality (thm:is-import, prop:triangular-sde, p ∉ E_2(κ_d), steps behind thm:main) | main:181, 230–242, 587, 690, 709, 812, 823, 834, 1046–1062 | agree |
| thm:main ε/3 split; receiver 1−2ε/3 | main:555–565, 584, 840, 866 | agree |
| thm:bb-envelope ε/4 per part; ε/(4ℓ) per chart and per core call | main:1039, 1052; tb:1244–1246, 1270–1271, 1424–1433 | agree; the chart error ε/(8ℓ) + 2kd·ε/(16ℓkd) = ε/(4ℓ) |
| Lean guards: 417 in the table, 455 in all | main:1274, 1316; README:9 | agree (the table rows sum to 417) |

## 3. Findings

### Imprecisions

**I1. lem:coherent-quadratic-sde: the wiring sentence omits the full circuit.** main.tex:821.
Quote: "It is wired only into the fourth backend, at its two instances; into the fifth, …". The
full circuit (`rees_circuit_full.py`) combines the third and fourth backends, and both of its
instances have κ_2 = 2, so this circuit is in it too. The linear lemma says so ("and so into
`rees_circuit_full.py`", main:810), so the two sentences read inconsistently. Drop-in:

```latex
It is wired only into the fourth backend, at its two instances (and so into \file{theorems/rees_circuit_full.py}); into the fifth, at grade two of the class-three filiform algebra over $\mathbb{F}_7$ ($a=2$, $p=7$, checked there on samples); and into the coherent class-four circuit over $\mathbb{F}_7$, at grades four and two.
```

**I2. (H3): "the bound … ≤ 1/800 proved there"; the bit reversal is left unstated.**
appendix-torsion-blackbox.tex:1447–1450. Quote: "By the bound $2\pi t2^{-r} \le 1/800$ proved
there". lem:qft-mod proves ε_aq ≤ 2πt2^{-r}. The value 1/800 comes from the choice of r here,
not from the lemma. Step E of that lemma also omits the final bit reversal, and the decoder
there absorbs it. Order finding must read the measured bits in reverse, and (H3) does not say
so. Drop-in for the sentence:

```latex
with every $\mathrm{C}R_k^{-1}$, $k > r = \lceil\log_2(1600\pi t)\rceil$, omitted, and without the final bit reversal, as there (the measured bits are read in reverse order before the continued-fraction step). The omission costs at most $\eps_{\mathrm{aq}} \le 2\pi t2^{-r}$ in operator norm, by the bound proved there, and $2\pi t2^{-r} \le 1/800$ by the choice of $r$; since the trace distance of two pure
```

**I3. The solver exponent β̂_c is called "not computed" although rem:is-runtime bounds its
Schedule 1 part.** main.tex:1051 and the caption at main:204 ("involves an uncomputed solver
exponent"); tb:1493–1497. rem:is-runtime (I177, I179) gives
T^IS_d = C₁d³M_db³(g_d²+b²) ≤ 2C₁c³M_d((a+1)b)⁵, with b ≤ 2log₂p. So the grades that run
Schedule 1 need β̂ ≤ 5, granting the tape-layout sketch. Only the Schedule 2 grades are
unbounded. That bound would make τ_c ≤ E_W(c)+6 at those grades. This is optional, but the
current wording undersells what the paper proves. Drop-in, replacing the parenthesis at the end
of thm:bb-envelope(iii):

```latex
(by Remark~\ref{rem:is-runtime}, granting its tape-layout sketch, every Schedule~1 call satisfies this with exponent $5$, since $g_d^2+b^2 \le 2((g_d+1)b)^2$ and $b \le 2\log_2 p$; the Schedule~2 calls are not bounded here, so $\hat\beta_c$ is not computed).
```

**I4. prop:coherent-receiver: the workspace lists omit the copy of s_i.** main.tex:848 ("one
controlled dilation (the register $\mathrm{G}$, the powers and the arithmetic ancillas)") and
main.tex:864 (the list of reused registers). The proof (I175) copies s_i into b fresh qubits
before squaring. That register is neither in W nor in the reused-register list. The qubit count
is unaffected asymptotically, but the lists are incomplete. Drop-ins:

```latex
one controlled dilation (the register $\mathrm{G}$, the copy of $s_i$, the powers and the arithmetic ancillas)
```

```latex
Registers that are reused (the workspace of $W_d$, the register $\mathrm{S}$, the registers of $\mathrm{G}$, of the copy of $s_i$ and of the powers, the arithmetic and evaluation ancillas)
```

**I5. Γ_× counts SWAP gates, while the gate set is said to implement only X, CNOT and Toffoli
exactly.** main.tex:836 (Γ_× = 158b²+46b), 838 and 181. The multiply-accumulate gate lists use
SWAP (main:793). Over a gate set where a SWAP costs three CNOTs, Γ_× bounds the gates only up
to a factor 3. The polynomial claim is unaffected, but the explicit bound in (iv) is not stated
over the gate set of (i). Drop-in for the definition in prop:coherent-receiver:

```latex
and $\Gamma_\times = 158b^2+46b$, an upper bound on the gates of one modular multiply--accumulate of the second arithmetic backend, counted over $\{X,\mathrm{CNOT},\mathrm{SWAP},\mathrm{Toffoli}\}$ (over the gate set of~(i), where a SWAP is three CNOTs, the bound in~(iv) holds with $3\Gamma_\times$ in place of $\Gamma_\times$).
```

**I6. rem:is-runtime assumes κ ≥ 2, then states the κ_d = 1 count.** main.tex:609. Quote:
"Let $\kappa = \kappa_d \ge 2$, …; at $\kappa_d = 1$ the count is $a^2(a+1)+2a+2b(a+1)$". The
displayed T^IS_d is then used for every d (main:200, 848). Drop-in for the opening:

```latex
Let $\kappa = \kappa_d$, $a = g_d$, $b = \lceil\log_2 p\rceil$, $G = G(\kappa,a)$, and, for $\kappa \ge 2$, let $\nu \le b-1$ be the number of prime factors, with multiplicity, of the largest divisor of $p-1$ all of whose prime factors divide $\kappa$ (the case $\kappa_d = 1$ is counted separately below).
```

**I7. The "Terms" paragraph is partly stale for κ = 8.** main.tex:628. Quote: "For $\kappa = 8$
and $9$ the search has not reached that threshold, and only partial information is quoted."
That is still true of the exhaustive search. But since I162 and I187, explicit contractions
cover every prime up to ⌈T_A(8)⌉ except [3,20000] ∪ X_29, and this paragraph is the reader's
first summary. Drop-in:

```latex
For $\kappa = 8$ and $9$ the exhaustive search has not reached that threshold, and only partial information is quoted; for $\kappa = 8$, explicit contractions cover every prime $p \equiv 1 \pmod 8$ in $(49417, \lceil T_A(8)\rceil]$, so only $[3,20000]$ and a list of $29$ primes remain open (see the paragraph after Proposition~\ref{prop:decoupled-sde}).
```

**I8. The AKS 17/2 note ignores the O(ℓ⁹) fallback.** Comments at main.tex:1060–1061 and
tb:1510–1511 ("The normalizer term O(l^8) … stays dominated under the improved bound as well").
The text at tb:1204–1206 says (P1) "is not load-bearing", because without it the total is
O(ℓ⁹), "still below the exponent 23/2". Under the 17/2 scenario, 9 > 17/2, so (P1) becomes
load-bearing. Drop-in for both comments (in main.tex write (iii) for (d)):

```latex
% The normalizer term O(l^8) of (d) (Lemma tb-howell-rounds) has exponent 8 < 17/2, so it stays
% dominated under the improved bound; the O(l^9) fallback without (P1), stated after that lemma,
% would not be, so (P1) becomes load-bearing if 17/2 is adopted.
```

**I9. KothariODonnellWu2026: locators against a 5-page proceedings entry.** main.tex:679
(`\cite[Theorem~2.2]`, `\cite[Lemma~3.6]`) and main:126 (`\cite[arXiv version, Section~5.2]`);
references.bib:274 (STOC 2026, pp. 101–105). Only one of the three locators names the version.
A 5-page extended abstract with a Lemma 3.6 is doubtful. Drop-in (after a human check):

```latex
at $p=3$ it is the $\mathbb{F}_3$ subset-sum bound recorded in~\cite[arXiv version, Theorem~2.2]{KothariODonnellWu2026}. Using sparse dependencies~\cite[arXiv version, Lemma~3.6]{KothariODonnellWu2026} lowers the count
% NEEDS HUMAN VERIFICATION: Theorem 2.2 and Lemma 3.6 of KothariODonnellWu2026 -- arXiv:2510.07515 or the STOC pages 101--105?
```

**I10. Three arXiv identifiers need an online check.** references.bib:78 (HoltSubramanian2026,
arXiv:2609.38085), 284 (KothariMetgerODonnellShuttyWu2026, arXiv:2609.40321) and 292
(BoucherFouqueShen2026, arXiv:2609.34996). Five-digit numbers above 34000 in a single month are
unusual. I cannot verify them offline, and the entries may well be right. Drop-in (a comment
above each entry, until checked):

```latex
% NEEDS HUMAN VERIFICATION: arXiv identifier not checked offline (referee 12, 2026-11-04).
```

**I11. The "NEEDS HUMAN VERIFICATION" tags do not cover STATE's list.** STATE.md:108–112 says
these citations need a human and that one can "grep NEEDS HUMAN VERIFICATION in the .tex": AKS,
CEMM, Imran–Ivanyos theorem and section numbers, Kitaev §5 Thm 2, Cleve–Watrous 7.1, van de
Woestijne, IMS Thm 11, ISS §3, Bene Watts Alg 1–2, Khukhro, Lidl–Niederreiter 5.41. The grep
finds AKS, van de Woestijne, IMS, ISS and Bene Watts. CEMM is tagged in lower case (tb:619). The
following have no tag: Kitaev and Cleve–Watrous (main:742); Imran–Ivanyos Theorem 1,
Propositions 1, 2, 4, 5 and Sections 1 and 6 (main:126, 1070); Khukhro Chapters 9–10 (main:176,
380). Lidl–Niederreiter 5.41 is flagged in the prose of appendix-schedule2.tex:194, not by a
tag. Drop-ins (comments after the citing lines):

```latex
% NEEDS HUMAN VERIFICATION: Kitaev1995 "Section 5, Theorem 2 and eq. (25)" and CleveWatrous2000 "arXiv version, Section 7.1" not checked offline.
% NEEDS HUMAN VERIFICATION: ImranIvanyos2023 Theorem 1, Propositions 1, 2, 4, 5 and Sections 1, 6 -- numbering of the QIP version or of arXiv:2304.08376?
% NEEDS HUMAN VERIFICATION: Khukhro1998 Chapters 9--10 locators not checked offline.
% NEEDS HUMAN VERIFICATION: Lidl--Niederreiter Theorem 5.41 (see the prose remark here).
```

At tb:619, replace "Needs human verification before adding them back." with:

```latex
% offline; cited without them. NEEDS HUMAN VERIFICATION before adding them back.
```

**I12. The README calls IMS Theorem 11 checked; the .tex calls it unchecked.** README.md:5:
"The two key citations (Ivanyos–Santha arity, Ivanyos–Magniez–Santha Theorem 11) were checked
against the arXiv papers." main.tex:217 and 968 tag the same locator NEEDS HUMAN VERIFICATION
("not checked offline", referee 10). A reader sees a contradiction. Drop-in for the two
comments:

```latex
% NEEDS HUMAN VERIFICATION: IMS "Theorem 11" (arXiv:quant-ph/0102014) was checked online by an AI session on 2026-10-31 (README) but not rechecked offline by referee 10 (2026-11-04).
```

**I13. The README names only referee passes 6 and 7.** README.md:9: "the text fixes of AI
referee passes 6 and 7 (black-box appendix and front matter; …)". Passes 5, 8, 9, 10 and 11
were also applied (I180, I182, I184–I186), as STATE says. Drop-in:

```text
the text fixes of AI referee passes 5 to 11 (circuits, black-box appendix, front matter, SDE section, core, regimes, subspace and Lean; `research/audits/reviews/2026-11-04-rees-referee-{5..11}-*.md`)
```

### Style

**S1. Symbols reused in the order-finding text.** In lem:tb-sylow(d) (tb:604–651), p^a is the
exponent and a is the random base; r is the order of a, and r is also the truncation parameter
in (H3) (tb:1448). In (H3), t = 2n+1 counts control qubits, while the notation table and
thm:bb-envelope define t = ⌈log₂(12ℓ/ε)⌉ (main:350, 1047). Inside one sentence of
thm:bb-envelope(iii) (main:1051), k is the kernel sample count in ε/(16ℓkd) and the rotation
index in R_k. Drop-in: in lem:tb-sylow(d), rename the base and its order:

```latex
An attempt on $F$ draws $\alpha$ uniformly from $\{1,\dots,F-1\}$; … If $r_\alpha$ is the order of $\alpha$, then $r_\alpha \mid u$ forces $x = \alpha^{r_\alpha/2}$ when $r_\alpha$ is even
```

In (H3), use `t_{\mathrm{of}} = 2n+1` and `r_{\mathrm{of}} = \lceil\log_2(1600\pi t_{\mathrm{of}})\rceil`. In
thm:bb-envelope(iii), write "rotations $R_j^{\pm1}$, $\mathrm{C}R_j^{\pm1}$".

**S2. Three DOIs are silently dropped.** references.bib:388, 400 and 412: Shor1997,
CleveEkertMacchiavelloMosca1998 and AKS2004 put the DOI in a `doi` field, which `plain.bst`
ignores, while every other entry has its DOI in `note`. Drop-ins:

```latex
  note    = {doi:10.1137/S0097539795293172; arXiv:quant-ph/9508027}
  note    = {doi:10.1098/rspa.1998.0164; arXiv:quant-ph/9708016}
  note    = {doi:10.4007/annals.2004.160.781}
```

**S3. "IMS" is undefined in the regimes table.** main.tex:217: "(IMS Theorem~11 also, oracle
input)". Drop-in:

```latex
(\cite[Theorem~11]{IvanyosMagniezSantha2001} also, oracle input)
```

**S4. prop:black-box(iv): a vacuous inclusion and an unstated unit.** main.tex:1039: "this is
$O_c(s^c\ell^2 + \ell^4) \subseteq O_c(s^c\ell^3 + \ell^4)$". The ℓ³ form is used nowhere, and
the unit is ring operations, while thm:bb-envelope(iii) states bit operations. Drop-in:

```latex
this is $O_c(s^c\ell^2 + \ell^4)$ ring operations, that is $O_c(s^c\ell^4 + \ell^6)$ bit operations, when $\log_2(8\ell/\eps) \le \ell$.
```

**S5. Standard algorithms named without a citation.** These are Pohlig–Hellman (main:609),
Tonelli–Shanks (main:814, 818), Adleman–Manders–Miller (main:825, 829) and Howell and Smith
normal forms (main:1039, 1051; lem:tb-howell-rounds). The appendix header (tb:17–31) proposes
keys (KannanBachem1979, Storjohann1996, Howell1986, StorjohannMulders1998, Reutenauer1993) that
were never added. Drop-in for the first Howell mention, once the entries exist:

```latex
Howell~\cite{Howell1986} and Smith normal forms over $\mathbb{Z}/M\mathbb{Z}$~\cite{KannanBachem1979,StorjohannMulders1998}
```

**S6. Bibliography hygiene (invisible in the PDF).** FultonHarris1991 and
HallgrenRussellTaShma2003 are never cited. Three keys disagree with their years
(ImranIvanyos2023 is 2024, IvanyosSantha2015 is 2017, MartinYip2024 is 2025). HardyWright2008
has no `address`. No change is needed for the build. Optional drop-in:

```latex
  address   = {Oxford},
```

**S7. Bibliography typesetting.** The paper has no `fontenc`, so accented names (Gábor,
Miklós, Göös) are built in OT1, and the bibliography gets 3 Underfull boxes. Optional drop-in
for the preamble (it also changes the package list in README line 13):

```latex
\usepackage[T1]{fontenc}
```

## 4. NEEDS HUMAN VERIFICATION comments (complete list from grep)

1. main.tex:217 (regimes table, derived-dimension row): IMS "Theorem 11" numbering, referee 10.
2. main.tex:610 (rem:is-runtime): van de Woestijne "Section 6 / 6.1": the 6-page ISSAC 2005 paper or the thesis? Referee 9.
3. main.tex:624 (Schedule 1 paragraph): the same van de Woestijne question, repeated at the second citation site.
4. main.tex:968 (cor:fpt-r, p = c+1): IMS "Theorem 11, Section 5" of arXiv:quant-ph/0102014, referee 10.
5. main.tex:1015 (ring-to-field note): Ivanyos–Sanselme–Santha "Section 3 of the arXiv version", referee 10.
6. main.tex:1055–1059 (after thm:bb-envelope): whether AKS2004 Theorem 5.3 gives Õ(log^{15/2} n). If so, 23/2 becomes 17/2 everywhere, the c ≥ 3 form of the time holds for c ≥ 2, and τ₁ = 17/2.
7. main.tex:1089–1091 (subspace section, wedge-gap item): whether Bene Watts et al., Algorithms 1–2, already include the recovery W† on rejection. Referee 11.
8. appendix-subspace.tex:258–259: the same Bene Watts question.
9. appendix-torsion-blackbox.tex:526: Ivanyos–Sanselme–Santha "Section 3 of the arXiv version", referee 10.
10. appendix-torsion-blackbox.tex:618–619 (lowercase "Needs human verification"): CEMM section numbers (5 and 6 in an earlier draft) were dropped and not confirmed.
11. appendix-torsion-blackbox.tex:1504–1509 (prop:tb-count-gates): the same AKS 15/2 question as item 6.

Related comments without the tag: appendix-torsion-blackbox.tex:29–31 (StorjohannMulders1998,
"volume and pages not confirmed offline", context only); appendix-schedule2.tex:194, in prose
(Lidl–Niederreiter Theorem 5.41 "not checked against the book"). The untagged citations from
STATE's list are under I11.

## Applied (11-04)

Applied by the integrator session on 2026-11-04, locally only (no git, no network, no commits).
Backups of every touched file: `/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/bak-i188/`.
Files changed: `main.tex`, `appendix-torsion-blackbox.tex`, `appendix-schedule2.tex`,
`references.bib`, `README.md` (all in `docs/papers/rees-hsp/`). No claim gate changed; every
"AI-checked, pending human review" label is kept (counts unchanged per file);
`research/reductions/rees_hsp_reduction.json`, `docs/outreach/` and `numbers.tex` were not touched.

**Tally: 14 applied, 4 modified, 2 skipped** (of 13 Imprecisions and 7 Style findings).

| Finding | Status | Note |
|---|---|---|
| I1 | applied | drop-in as given (lem:coherent-quadratic-sde wiring sentence). |
| I2 | applied | drop-in as given, with the S1 symbols $t_{\mathrm{of}}$, $r_{\mathrm{of}}$. The bit-reversal claim was checked against main.tex step E of lem:qft-mod ("without the final bit reversal, which DEC absorbs"). |
| I3 | modified | Claim verified from rem:is-runtime: $T^{\mathrm{IS}}_d = C_1d^3M_db^3(g_d^2+b^2) \le 2C_1d^3M_d(g_d+1)^2b^5 \le 64C_1c^3M_d((a+1)\log_2 p)^5$, using $g_d \le a$, $g_d^2+b^2 \le 2((g_d+1)b)^2$ (as $b \ge 1$), $b \le 2\log_2 p$ (as $p \ge 2$) and $d \le c$; it needs nothing beyond the remark (granting its tape-layout sketch, as the remark itself does). Wording: the parenthesis of thm:bb-envelope(iii) now states exponent 5 with this explicit constant for every Schedule 1 call, says the Schedule 2 calls are not bounded, and keeps "$\hat\beta_c$ is not computed"; $b$ is defined in place because the $b$ of tab:notation-bb differs. The same sentence was added at the definition of $\hat\beta_c$ in prop:tb-count-gates(d). The table caption ("involves an uncomputed solver exponent") was left as it was: a longer caption made the regimes table a float too large for its page, and the old wording is still true. |
| I4 | applied | both drop-ins; the proof's copy of $s_i$ ($b$ CNOTs) was confirmed. |
| I5 | applied | drop-in, plus "with $G_{\mathrm{meas}}$ counted over that gate set", so that the factor-3 statement claims nothing about $G_{\mathrm{meas}}$. Numbers unchanged: a multiply-accumulate with $s$ SWAPs among at most $\Gamma_\times$ gates costs at most $\Gamma_\times + 2s \le 3\Gamma_\times$ gates once each SWAP is three CNOTs. |
| I6 | applied | drop-in as given. |
| I7 | modified | The drop-in's restriction "$p \equiv 1 \pmod 8$" was dropped to match the paragraph after prop:decoupled-sde, which states $E_2(8) \cap (49417, \lceil T_A(8)\rceil] = \emptyset$; the new text also says that all but the 29 listed primes in $(20000, 49417]$ are covered. |
| I8 | applied | both comments, (iii) in main.tex and (d) in the appendix. |
| I9 | modified | Tag only (main.tex, after the Theorem 2.2 / Lemma 3.6 sentence, also naming the "arXiv version, Section 5.2" locator of the introduction). The locators were not rewritten to "arXiv version": the referee conditions that on a human check. |
| I10 | applied | tag comment above each of the three `@misc` entries in references.bib (BibTeX ignores text between entries; the build is clean). |
| I11 | applied | tags for Kitaev/Cleve–Watrous, Imran–Ivanyos (introduction, plus a short tag at the Propositions 1, 2, 4, 5 site), Khukhro (one tag covering both locators), Lidl–Niederreiter 5.41 and StorjohannMulders1998 (header comment); CEMM tag upper-cased. |
| I12 | modified | Per the integrator: the README now says the IMS Theorem 11 locator was checked online by an AI session on 31 October, was not rechecked offline by referee 10, and is tagged, so it is to be treated as unchecked. The two .tex comments were left as they were, since they already say "not checked offline". |
| I13 | applied | README now names passes 5 to 11 with the glob `research/audits/reviews/2026-11-04-rees-referee-{5..11}-*.md`. |
| S1 | applied | (H3): $t_{\mathrm{of}}$, $r_{\mathrm{of}}$ (also in the gate count $(2n+1)(r_{\mathrm{of}}+2)$); thm:bb-envelope(iii): $R_j^{\pm1}$, $\mathrm{C}R_j^{\pm1}$. In lem:tb-sylow(d) the base is $\theta$ and its order is $r_\theta$, not $\alpha$/$r_\alpha$, because part (c) of the same lemma uses $\alpha_i$ for the exponents $p^{\alpha_i}$. |
| S2 | applied | DOIs of Shor1997, CEMM1998 and AKS2004 moved into `note`. |
| S3 | applied | drop-in as given. |
| S4 | applied | drop-in as given; consistent with the $O_c(s^c\ell^4+\ell^6)$ chart time of thm:bb-envelope(iii). |
| S5 | skipped | The proposed keys need bibliographic data (volume, pages) that cannot be confirmed offline (StorjohannMulders1998 is flagged as such); adding unverified entries is worse than the present uncited mentions. Left for a session with network access. |
| S6 | applied | the optional `address = {Oxford}` for HardyWright2008. The rest needs no change, as the finding says (uncited entries are not printed; key-year mismatches are invisible). |
| S7 | skipped | A trial build with `\usepackage[T1]{fontenc}` gave 2 Overfull and 4 Underfull boxes, which the build gate forbids. README line 13 is unchanged. |

Also changed: README line 9 now gives the page count as 149 (the edits add one page; STATE.md still
says 148 and should be refreshed at the next STATE rewrite).

**Build** (copy in `/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/build/`, `latexmk -g -pdf`): exit 0, 149
pages, 0 Overfull, 3 Underfull (bibliography, as before), no "Float too large", no undefined or
multiply defined references, 0 BibTeX warnings. `pytest -q tests/tools/test_rees_paper_numbers.py`:
2 passed.

**`grep -n "NEEDS HUMAN VERIFICATION" docs/papers/rees-hsp/*.tex`** (complete output, 18 lines; long lines shortened with "…"):

1. appendix-schedule2.tex:195: `% NEEDS HUMAN VERIFICATION: Lidl--Niederreiter Theorem 5.41 (see the prose remark here; referee 12, 2026-11-04).`
2. appendix-torsion-blackbox.tex:32: `% NEEDS HUMAN VERIFICATION: StorjohannMulders1998 volume and pages (ESA 1998), if the key is added.`
3. appendix-torsion-blackbox.tex:527: `% NEEDS HUMAN VERIFICATION: ISS "Section 3 of the arXiv version" not checked offline (referee 10, 2026-11-04).`
4. appendix-torsion-blackbox.tex:620: `% offline; cited without them. NEEDS HUMAN VERIFICATION before adding them back.` (CEMM section numbers)
5. appendix-torsion-blackbox.tex:1516: `% thm:bb-envelope. NEEDS HUMAN VERIFICATION.` (AKS 15/2 question)
6. main.tex:127: `% NEEDS HUMAN VERIFICATION: ImranIvanyos2023 Theorem 1, Propositions 1, 2, 4, 5 and Sections 1, 6 -- numbering of the QIP version or of arXiv:2304.08376? (referee 12, 2026-11-04).`
7. main.tex:218: `… (\cite[Theorem~11]{IvanyosMagniezSantha2001} also, oracle input) % NEEDS HUMAN VERIFICATION: IMS "Theorem 11" numbering not checked offline (referee 10, 2026-11-04).`
8. main.tex:382: `% NEEDS HUMAN VERIFICATION: Khukhro1998 Chapters 9--10 (here) and Chapter 10 (here and in the input contract) locators not checked offline (referee 12, 2026-11-04).`
9. main.tex:612: `% NEEDS HUMAN VERIFICATION (referee 9, 2026-11-04): the ISSAC 2005 paper has six pages (pp. 348--353); check whether "Section~6" / "Section~6.1" of vandeWoestijne2005 refers to it or to the thesis of the same title.`
10. main.tex:626: the same van de Woestijne comment as line 612.
11. main.tex:682: `% NEEDS HUMAN VERIFICATION: Theorem 2.2 and Lemma 3.6 of KothariODonnellWu2026 -- numbering of arXiv:2510.07515 or of the STOC 2026 pages 101--105? Also "arXiv version, Section 5.2" in the introduction (referee 12, 2026-11-04).`
12. main.tex:746: `% NEEDS HUMAN VERIFICATION: Kitaev1995 "Section 5, Theorem 2 and eq. (25)" and CleveWatrous2000 "arXiv version, Section 7.1" not checked offline (referee 12, 2026-11-04).`
13. main.tex:972: `… \cite[Theorem~11, Section~5]{IvanyosMagniezSantha2001} (numbering of the arXiv version). % NEEDS HUMAN VERIFICATION: "Theorem 11, Section 5" of arXiv:quant-ph/0102014 not checked offline (referee 10, 2026-11-04).`
14. main.tex:1019: `… (\cite{IvanyosSanselmeSantha2012}, Section~3 of the arXiv version). % NEEDS HUMAN VERIFICATION: "Section 3 of the arXiv version" of Ivanyos--Sanselme--Santha not checked offline (referee 10, 2026-11-04).`
15. main.tex:1063: `% NEEDS HUMAN VERIFICATION.` (AKS 15/2 question, after thm:bb-envelope)
16. main.tex:1076: `% NEEDS HUMAN VERIFICATION: ImranIvanyos2023 "Propositions 1, 2, 4, 5" numbering (see the tag in the introduction; referee 12, 2026-11-04).`
17. main.tex:1097: `  % correct either way. NEEDS HUMAN VERIFICATION.` (Bene Watts et al. Algorithms 1–2)
18. appendix-subspace.tex:259: `% W^dagger on rejection was not checked (no offline copy). NEEDS HUMAN VERIFICATION.` (Bene Watts)

In addition, references.bib (not .tex, so outside the grep) carries
`% NEEDS HUMAN VERIFICATION: arXiv identifier not checked offline (referee 12, 2026-11-04).` at
lines 78 (HoltSubramanian2026), 285 (KothariMetgerODonnellShuttyWu2026) and 294
(BoucherFouqueShen2026).
