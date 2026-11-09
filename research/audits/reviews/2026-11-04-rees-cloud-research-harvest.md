# Rees HSP: harvest of five cloud research sessions (run 3-4 Nov 2026), compared with the paper

Harvested 2026-11-05 (AI only; nothing committed, pushed, sent or edited in the .tex).
All Rees claim gates stay false; everything below is AI-checked, pending human review.

Reports saved verbatim (each SHA-256 matches the session's `result` event):

| key | session | ran (UTC) | saved as |
|---|---|---|---|
| a1 | session_01B1JoCfZNsKGrJofznH8ixw | 11-03 22:54-23:14 | 2026-11-04-rees-cloud-a1.md |
| sde | session_01B1JoCgVr4ufcSUoZpvsgRm | 11-03 22:54-23:36 | 2026-11-04-rees-cloud-sde.md |
| cites | session_01B1JoCgtowBkxbmwPsfia8r | 11-04 01:56-02:10 | 2026-11-04-rees-cloud-cites.md |
| zerosum | session_01B1JoChaW8s7QvRQso9tgez | 11-04 01:56-04:38 | 2026-11-04-rees-cloud-zerosum.md |
| prio3 | session_01B1JoCj7cgT6oZy4a3Z56bG | 11-04 05:01-05:19 | 2026-11-04-rees-cloud-prio3.md |

Compared against the working tree of 2026-11-05 evening: `docs/papers/rees-hsp/main.tex`
(companion), its appendices, `references.bib`, `core/main-core.tex`, and `research/STATE.md`.
Line numbers are those of that working tree. Note that all five sessions ran before the
overnight passes I190-I243, so several of their "open" items are already superseded in the paper.

## A. Ranked list of NEW items that would change the paper

1. **Citer coverage sentence is out of date (a1).** `main.tex:120` (end of Related work):
   "Google Scholar lists three further citing works of Imran--Ivanyos that we could not
   identify." a1 read Scholar's citing lists without a CAPTCHA: 14 entries = 13 works for
   Imran-Ivanyos, 14 entries = 13 works for Ivanyos-Santha. The three formerly unidentified II
   citers are: Imran's BME PhD thesis (2024, full text read), Ding-Gong-Jiang-Tang IACR ePrint
   2026/2083 (abstract only, PDF 403) and Emerencia's VUB PhD thesis (2024, abstract only).
   None anticipates the result. IS citers additionally read: arXiv 1307.6429 (Scholar entry looks
   spurious), ERCIM News 112 (2018), MDPI Math. 9(24):3299; Nikolov-Galabov (ResearchGate) unread.
   Suggested: replace the clause by "Google Scholar's citing lists (13 works each) were also
   checked; two Imran-Ivanyos citers and one Ivanyos-Santha citer were read only from their
   abstracts." `core/main-core.tex:186` lists the indexes "on 2 November 2026" without Scholar;
   add Scholar there too. A1 stays "possibly new"; `novelty_established` stays false.
2. **Strongest new supporting citation (a1): Imran's PhD thesis.** M. Imran, *The Hidden
   Subgroup Problem and Quantum Cryptanalysis*, BME 2024: Thm 3.1 (p. 42) needs class AND prime
   factors bounded; Sec. 3.5 (p. 55) poses a poly(np) zero-sum finder as an open question and says
   a positive answer gives the smooth-|G| case. Not in references.bib. Would sit next to the
   `\cite[Section~6]{ImranIvanyos2023}` open-problem sentence at `main.tex:120` and
   `core/main-core.tex:184`/`:697`. (Optional second: the Dutto-Mercuri-Murru-Romano survey
   arXiv:2512.02087, p. 39, which also names II's bounded-prime result as the nilpotent frontier;
   prio3 and a1 read it only by abstract plus term search.)
3. **KOW is cited for a bound it does not state (cites #13).** `main.tex:120`: "improved to
   $q^{q^2}(n+1)^{q-1}$, as stated in [KMOSW Thm 1.11] (see also [arXiv version, Section 5.2]
   {KothariODonnellWu2026})". KOW v1-v3 Sec. 5.2 only quotes II's older
   $m \ge q^{Cq^2\log q}n^{\lfloor q/2\rfloor\lceil\log_2 q\rceil}$; the $q^{q^2}(n+1)^{q-1}$ bound is
   KMOSW Thm 1.11 alone (cites #12 confirms it). Move the "see also KOW" to the older
   $n^{O(q\log q)}$ bound. Same pattern, without pinpoint, at `core/main-core.tex:184`.
4. **Kitaev's QFT precision is the paper's derivation, not Kitaev's statement (cites #24).**
   `core/main-core.tex:523` ("Kitaev's construction ... implements the Fourier transform ... with
   precision $2(q\eps')^{1/2}$") and `main.tex:760` ("makes Kitaev's precision $2(p\eps')^{1/2}$
   equal to $\eta/2$"). Kitaev quant-ph/9511026v1 Thm 2 gives $2(|\Omega|\eps)^{1/2}$ for the
   eigenvalue measurement $Q_q$; no precision is stated for the transform $V_q$, and the transfer
   via eq. (25) needs $T_q$ (state creation incl. amplitude rotations) to be exact, which Kitaev
   does not state. Reword as "our derivation from Thm 2 and eq. (25), assuming $T_q$ exact", or
   point at `lem:qft-mod` as the self-contained route. This touches thm:uniform-compilation(iii),
   whose $\eps'=\eta^2/(16p)$ was just fixed (I239). The section/theorem/equation numbers
   themselves exist (resolves, AI-only, the NEEDS HUMAN VERIFICATION comment at `main.tex:761`;
   Cleve-Watrous Sec. 7.1 exists and is a sketch, as the paper says).
5. **Imran-Ivanyos resource sentence has a wrong name and an undercount (cites #8).**
   `main.tex:1222`: (a) "hidden-subgroup-membership routine" -> HSMC is *hidden subgroup modulo
   the commutator* (the subgroup $HG'$); (b) "each converting $\prod_{i=2}^c S(p,n_i)$ copies" is
   the cost of ONE converted copy of the $G/G'$ subgroup state; each HSMC call needs as many such
   copies as the [II22] abelian algorithm uses (the paper's "plus the exponent of their exact
   abelian subroutine" partly covers this; make it explicit); (c) the $n_i$ are those of the
   semi-elementary quotient, not of $G$; (d) $\sigma_p$ is not printed in II (it follows from
   their ineq. (3) at $i=\lfloor\log d_0\rfloor$ with Prop 5's $\lceil\log p\rceil$; II's displayed
   bound is weaker). $\sigma_p$ agrees with KOW Thm 1.8 ($n^{(\bar q/4)\log_2\bar q}$); I re-checked
   10/18/50/50 at c = 9 against that. Suggested wording: "the proofs of Props 1, 2, 4, 5 give
   (our computation) ...". The numbering question in the comment at `main.tex:121` is answered
   (AI-only): arXiv v1 and QIP 23:14 numbering are identical.
6. **II's worst-to-average reduction is suspect (zerosum Sec. 5; independently the local
   s3-arity side finding of 11-05, recorded in integration-log I210 but not in the paper).**
   `main.tex:120`: "Their Proposition 3 and Section 6 say that a randomized or average-case
   zero-sum finder at cost poly(np) would give a non-exact algorithm". The Sec. 6 sketch feeds
   $y_k=\sum_{T_k} r_i = -\sum_{T_k} x_i$ to the average-case solver; $T_k$ is independent of the
   worst-case $x$, so $y_k$ is a fixed-set subset sum of adversarial vectors and is not uniform
   (all $x_i=e$ puts every $y_k$ on $\langle e\rangle$). I checked this argument and agree it is
   a real gap in the sketch as written (argued, not a proof that no reduction exists). cites #6
   adds that Prop 3 assumes a worst-case finder succeeding w.h.p.; the average-case remark is in
   Sec. 6 only. Suggest: keep the attribution but add "the average-case part rests on a sketch in
   their Sec. 6 that we could not complete". No theorem of the paper uses it (the paper's own
   Gamma_0 node reads i.i.d. labels directly).
7. **KOW Lemma 3.6 pinpoint (cites #15).** `main.tex:702`: "Using sparse dependencies
   [KOW Lemma 3.6] lowers the count to $(1-1/p)a^2/2+O(a\log a)$." Lemma 3.6 is only the sparse
   dependency step; the count $(1-q^{-1})\ell^2/2+\ell\log_q(\ell+1)+O(\ell)$ is Remark 3.8 (on
   Thm 3.7, which for $q>3$ finds a $\pm\lfloor q/4\rfloor$-zero-sum, not a subset sum); for
   $q=3$ it is Thm 1.2 via Lemma 2.3. The transfer to $\kappa$-th-power weights is the paper's
   own adaptation. Reword as "(our adaptation of [KOW Lemma 3.6, Remark 3.8])". The sde report
   independently notes the gain is from KOW's F_3 sparsity trick and is negligible at large p.
8. **Weil bound cited inconsistently (cites #40).** `appendix-sde-side.tex:51` cites
   `\cite[Theorem~5.41]{LidlNiederreiter1997}` bare, while `appendix-schedule2.tex:120` says that
   number "was not checked against the book" and uses Martin-Yip Lemma 2.2 (arXiv 2403.04312v2).
   The cloud check also confirmed 5.41 only via three secondary arXiv sources (book unseen;
   first-edition numbering UNSURE). Use the schedule2 wording at sde-side:51.
9. **van de Woestijne nontriviality (cites #23).** `core/main-core.tex:452`, `main.tex:644`
   (and the Sec. 6.1 reduction at `appendix-sde-side.tex:17`): ISSAC'05 Thm 6.2 solves
   $\sum_{i=0}^n x_i^n=0$ deterministically but does not say the solution is nontrivial; the
   Leiden thesis (hdl 1887/4392) Thm 5.3 does ($x_0\ne0$). The "write $-1$ as a sum" step is
   Sec. 6.2. Add the thesis citation where a NONZERO solution is used.
10. **Luks pinpoint for conjugation (cites #32).** `appendix-filters.tex:29`: "By Luks [Thm
    3.2(5)], the stabilizer is computable ... for every matrix p-group acting by conjugation,
    for every N and p." (5) is the vector stabilizer; conjugation is (8) (centralizer), or (5) on
    the induced $N^2$-dimensional action. Thm 3.2 is polynomial in $n+\log|F|+\nu$, $\nu$ the
    largest prime of $|G|$ other than the characteristic, so "every N and p" is right for
    p-groups in characteristic p only; state that. `:35` ((5),(7)) is fine for p-groups.
11. **Smaller pinpoint fixes (cites).**
    - `main.tex:1279` Kimmel et al.: "Appendix C, Theorems 1 and 20" is arXiv 1608.00281v1
      numbering; the bib entry is npj 3:13, where Thm 20 is Supplementary Thm A3. Add "arXiv
      version" (cites #28).
    - `main.tex:1279` Bene Watts Thm 5 / Rem 6: output is the anti-symmetric STATE on the
      support, success $1-r(1-\lambda_{\min}/r)^n$, so copies depend on $\lambda_{\min}$; Rem 6
      only lets the loop stop early. Check that "cost polynomial in ... $1/\delta$" covers
      $\lambda_{\min}$ of the filtered states; Thm 7 / Rem 8 give better counts (cites #30).
      (Remark is "argued" already.)
    - `main.tex:1022`, `core/main-core.tex:619` Ye et al. Lemma 1 is for rank-k subgroups
      GSP(p,n,k), $\Omega(\sqrt{p^{n-k}})$; the "meet only in the identity" form is k = 1; say so
      (cites #35).
    - `appendix-torsion-blackbox.tex:692-693`: II use exact Watrous to prepare $|M_1\rangle$ for a
      subgroup of a subnormal series, not $G$; say "as for the subgroups in [II Sec. 2.2]"
      (cites #10).
    - Khukhro Ch. 10 (`main.tex:171`, `:265`, `:398`; core :135/:215/:257): only the table of
      contents was seen (Ch. 10 = Mal'cev/Lazard correspondences, Sec. 10.2 p. 121); add
      Trappeniers Cor 2.4 as the checkable subgroup statement, and pin `references.bib:185`
      Trappeniers to v2/v3 (v1 has another title and no Thm 2.3) (cites #27, #39).
    - Notation clash: IS's $B_\ell(d,m)=d^{\ell(\ell-1)/2}(m+1)^\ell$ vs the paper's $B_d(a)$
      (e.g. $B_2(1)=64$ at `core/main-core.tex:586`); a footnote avoids confusion (cites #19).
    - `appendix-schedule2.tex:11` "first two levels of the collision recursion [IS Lemma 12]":
      Lemma 12 is a depth-d recursion; the literal two-level blocks-of-blocks ($G(d,m)^2$
      vectors) is the proof of Thm 3, Sec. 3.3. Say which is meant (cites #21, UNSURE).
12. **KMOSW's QUANTUM F_3 result is not mentioned (sde Sec. 2).** KMOSW Thm 1.3 / Cor 1.4: quantum
    poly time for F_3 subset sum at $m=\eps n^2$ for every fixed $\eps>0$ (Regev + binary-error
    LWE decoder). `appendix-sde-side.tex:46` (rem:sde-subquadratic(c)) correctly says "classical";
    since the paper is quantum, one clause noting the quantum $\eps a^2$ at p = 3 (still
    quadratic, consistent with `main.tex:702` last sentence) would pre-empt a referee. Read by the
    sde session from arXiv 2609.40321v1; not re-checked here.
13. **Optional additions from the sde session (proved there; I re-derived 13a).**
    a. Planting obstruction (sde Lemma 4.3): full-rank $\Lambda$, $M\ge\kappa a+1$, $T$ with
       $x_T\ne0$ for every nonzero solution => $\dim\pi_T(\ker\Lambda)\ge(1-1/\kappa)|T|+1/\kappa$
       (Chevalley-Warning on the columns outside $T$). So the planted key-finding hardness of
       rem:sde-subquadratic(b) (`appendix-sde-side.tex:44`) cannot be embedded in instances at
       the Chevalley-Warning length; a hardness proof there must be non-local. Fits as one
       sentence after (b), which already says it does not exclude methods at solvable arities.
    b. The converse of (b): a uniformly random instance with a 2-dim kernel at $M=a+2$ IS the
       power-residue pattern problem (up to one twist). Minor.
    c. Obstructions to routes for $o(a^2)$ at large p: Regev/CLZ needs decoding at error rate
       $\approx1-1/\kappa$ (via Tao's uncertainty principle, cited from memory); KOW's CIS
       machinery needs APs in $P$, bounded by $\sqrt p\log p$ (Polya-Vinogradov); Groebner
       (msolve) degree exactly $\kappa^a$, diagonal = dense. None is in the paper; only worth a
       sentence if a referee asks why o(a^2) was not attempted.

## B. Already reflected in the paper (no change needed)

- prio3 bottom line (no covering result; ingredients A2-A5 known; A1 the possibly-new element;
  input-model difference with II; Morales, Holt-Subramanian, Boucher-Fouque-Shen scopes): all at
  `main.tex:120` / `core/main-core.tex:182-186`, including the II Sec. 1 automorphism remark and
  the cover-dilation answer to it.
- cites items OK (26 of 40), e.g. ISS Thm 2, IS Cor 8 / Prop 7 / Thm 5 Sec. 5 / Thm 11 /
  Secs. 3.1-3.3, II Thm 1 / Sec. 1 / Prop 1 / Sec. 2.1, KMOSW Thm 1.11, KOW Thm 2.2, GKSZ Def 6.1,
  Trappeniers Thm 2.3 (v2/v3), Go Thm 2, Bene Watts Algs 1-2, Childs Thm 5.1 and eq. (10.10),
  Nayak Sec. 1 / Cor 4.2, EHK Thm 2. cites #19 is a third AI reading confirming
  $C(d,m)\le G(d,m)^{\lceil\log_2(d+1)\rceil}$ behind rem:is-printed (the OD3 human check of IS
  pp. 3, 7-10 is still needed). cites #26 confirms IMS Thm 11 / Sec. 5 exist in quant-ph/0102014
  (comments at `main.tex:229`, `:1119`), the one-step-per-oracle-call point being the standard
  convention.
- cites #16 (ISS Claim 1 randomized): already handled, `main.tex:687` says deterministic given
  $g$, Las Vegas otherwise.
- cites #22 is a FALSE ALARM against the current text: `appendix-subspace.tex:287` uses
  $j+1$ variables for degree $j$, exactly Fact 2's $d+1$; no change.
- sde Sec. 4.2 (equivalence with power-residue / Legendre-PRF key finding at $M=a+2$): already
  `rem:sde-subquadratic(b)` (`appendix-sde-side.tex:44`, with Beullens et al. in the bib);
  sde's MQ remark ~ rem:sde-subquadratic(c) (Cheng-Hashimoto-Miura-Takagi threshold).
- zerosum: its "drop-in lemma" (Theorem B: poly time, arity ~2.2a^4 at p = 5, 7) is DOMINATED by
  the paper's adopted Gamma_0 node `rem:fc-zero-sum-arity` (`appendix-free-coordinate.tex:296`,
  OD2/I234): arity $O_c(g^{1+\lceil\log_2 c\rceil}\log(1/\tau))$, degree 3 at p = 5 and 4 at p = 7,
  and by KMOSW Thm 1.10 (degree 3 at p = 5, 7), which the zerosum report never cites. Its only
  residual gain: additive instead of multiplicative $\log(1/\tau)$ at p = 7 (degree 4 vs 5 at
  $\tau=2^{-g}$). Its p = 3 Theorem A is ISS Claim 1 / KOW Thm 2.2 (in the paper). Its barriers
  (merging, lattice) are covered more rigorously by `rem:fc-zero-sum-arity(c)`. Not worth adopting.
- a1 bibliographic checks agree with references.bib: II title "Zero Sum Subsequences and Hidden
  Subgroups" (QIP 23:14), IS TCS title without "On", KOW STOC DOI 10.1145/3798129.3800731; the
  three Sept-2026 arXiv IDs (Morales 2608.05321, Holt-Subramanian 2609.38085, Boucher-Fouque-Shen
  2609.34996) and KMOSW 2609.40321 exist with these titles (AI-only; the NEEDS HUMAN VERIFICATION
  comment at `references.bib:294` can be narrowed accordingly).

## C. Contradictions

1. **sde verdict vs the paper (paper supersedes).** sde Sec. 1/3: "no polynomial-time solver
   using $c\,a^2$ columns with $c<1/2$", even on random columns, with an argued barrier "every
   free-vector design pays $\sum(\ell+1)$". The paper (later: I203, I206, I211, adopted I233) has
   `rem:sde-block-steered` (`appendix-sde-side.tex:51-55`): $\lfloor(a+2)^2/4\rfloor+[a\text{ odd}]$
   columns ($c=1/4$) and $O(a^2/\log a)$ for i.i.d. uniform columns at $p\ge\mathrm{poly}(a)$, and
   `rem:sde-worst-case(b)` (`:72-74`) for every bank in general position. The barrier fails
   because splitting one circuit into $J$ coset blocks realises $J-1$ directions; the paper's
   `rem:sde-subquadratic(a)` (`:42`) proves the one-direction bound only for unsplit circuits.
   Do not quote the sde verdict. sde's T1/T2 trade-offs are dominated. For ARBITRARY columns both
   agree: $(a+1)(a+2)/2$ is the best proved.
2. **Report-internal errors to avoid importing.**
   - prio3 Sec. 0/5 and zerosum Sec. 1 quote IS Thm 3 as $n>d^{d\log d}(m+1)^{d\log d}$; the
     printed bound is $d^{d^2\log d}(m+1)^{d\log d}$ (sde Sec. 2 and the paper, `main.tex:620,644`,
     `core/main-core.tex:469-471`). The paper is right.
   - zerosum Sec. 6: "At the Davenport threshold the problem is PPA_p-complete [GKSZ]".
     GKSZ give BIS_p membership in PPA_p (completeness is for Chevalley_p); the paper's
     membership-only wording (`appendix-free-coordinate.tex:305`) is the correct one.
   - arXiv 1507.03674 is "Huang-Bao" in sde but "Hashimoto" in zerosum. The paper does not cite
     it; resolve the authorship before any use.
3. No report contradicts a theorem of the paper. prio3's consistency check of the tuple map
   (Vandermonde injectivity) agrees with the paper's construction.

## D. What the reports did NOT read in full (adversarial notes)

- a1: ePrint 2026/2083 and the Emerencia thesis abstract only; Nikolov-Galabov unread;
  ePrint 2026/2678 (Di Concilio-Flores-Kahrobaei-Noce survey) abstract only, citation of II
  unconfirmed. DBLP not searched (anti-bot), OpenAlex quota exhausted.
- prio3: Scholar cited-by blocked (a1, earlier, got through); DBLP blocked; Holt-Subramanian,
  Dutto et al., 2202.04047, IACR 2026/2678 and several 2610.* papers abstract/term-search only;
  QIP/TQC 2025-26 programmes never surfaced. H. Wang arXiv:2204.03295 (general-HSP claim, no
  journal version) read by abstract; prio3 does not regard it as credible prior art.
- cites: Khukhro and Lidl-Niederreiter books unseen (TOC / secondary only); published versions of
  ISS (Algorithmica), Go et al. (QST), Ye et al. (I&C) not reachable; IMS SPAA, GKSZ CCC,
  Cleve-Watrous FOCS, EHK IPL, KOW STOC not tried. Items 23 and 28-40 were checked by helper
  agents with spot re-reads of 30, 32, 33, 38.
- sde: Tao's uncertainty principle cited from memory; Thomae-Wolf, Cheng et al., Furue et al.,
  Hashimoto ePrints not checked (Cloudflare); BGLS abstract only; Legendre-PRF cryptanalysis not
  checked.
- zerosum: says "checked against the PDFs" but omits KMOSW entirely (see B).

## E. Next step (for the integrator; owner decides)

Apply A1-A11 as wording/citation edits in one pass (no theorem, table, E_W or numbers.tex
change; do NOT run make_numbers.py), rebuild main.tex and core, and add a log row. A12-A13 are
optional. The human-review list should gain: II Sec. 6 sketch (A6), Kitaev precision transfer
(A4), vdW thesis Thm 5.3 (A9), and the unread Scholar citers (D).
