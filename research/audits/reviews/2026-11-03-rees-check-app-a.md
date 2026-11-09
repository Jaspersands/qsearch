# Rees paper, Appendix A (Schedule 2): unanchored adversarial proof check

Date: 2026-11-03. Item 1 of `research/REES_FULL_CAMPAIGN_4.md`. Target:
`docs/papers/rees-hsp/appendix-schedule2.tex` (474 lines, as of 2026-11-02 night), and the
statements of `main.tex` that it proves or that cite it: Theorem `thm:power-sde`(ii),
Proposition `prop:decoupled-sde`, and the "Terms" paragraph before them.

**Status: AI check, pending human review.** No human has read these proofs or this check.

**Method.** I read the appendix and the `main.tex` statements first and formed my own verdict
on every step: I re-derived every identity by hand and recomputed every constant. Then I wrote
exact scripts (`2026-11-03-rees-check-app-a/`) for everything that can be checked in finite
time. Only after that did I read `2026-11-02-rees-weil-threshold.md` and
`2026-11-02-rees-small-prime-arity.md` (Section 6). Labels: **proved** (my own derivation),
**exact** (exact integer or rational computation), **interval** (rigorous mpmath interval
arithmetic), **float** (50-digit floats or bisection).

## 0. Verdict

The appendix is **sound**. I found **no error** in any lemma, proposition, theorem or table
entry. There are **three small gaps**, all in side remarks or accounting, each with a one- or
two-sentence fix (G1–G3). There are also five precision nits (N1–N5) and one point the
integrator should make explicit (D1): the definition of $E_2$ allows zero entries, and that
choice decides several quoted values.

| # | Kind | Where | Summary |
|---|---|---|---|
| G1 | gap (reason incomplete; claim true) | sentence after the definition of a two-level contraction | "Replacing $\xi$ by $\xi^u$ only relabels the cosets" does not cover every coset generator: the general one is $\xi^u q$ with $q \in Q_0$, which also rescales $W$ diagonally. The claim still holds (proof below; exact check over every coset generator, $\kappa = 3,4,5$, $p < 140$). |
| G2 | gap (abort budget) | proof of Cor. `cor:app-s2-decoupled` | The $2^{-k}$ budget leaves out the coset-generator search. With $r = \lceil (k+1)/\log_2(8/5)\rceil$ rounds, plus Phase 1 at $2^{-k-1}$, plus $\xi$ at $2^{-k-3}$, the total is $1.125\cdot 2^{-k}$. Fix: $r = \lceil (k+3)/\log_2(8/5)\rceil$. |
| G3 | gap (overstated cost) | paragraph after Prop. `prop:app-s2-TW` | "gives the conclusion of Theorem `thm:app-s2-main` … for every prime $p > T_W$" includes the cost bound. In the band $T_W < p < 4((\kappa-1)\kappa^\kappa+1)^2$ the stated method costs $O(\kappa p)$, up to about $\kappa^{2\kappa+3}$ coset tests, which exceeds $(1+\kappa^\kappa)\poly$. The next sentence says so, but the first sentence claims too much. |
| D1 | definition point (no error) | Def. of $E_2$, Cor. `cor:app-s2-small`, scope list | Zero entries are allowed in the definition, and the quoted sets depend on that. With all entries nonzero (what Props TW/TA and Phase 0 construct) the sets grow: κ=2 adds {3}; κ=3 adds {7, 13} (so it would not be ∅); κ=4 adds {61}; κ=5 adds {191, 211, 241, 251} **[exact]**. |
| N1 | nit | κ ≥ 6 case of Prop. TA(ii) | The step $(1-1/P)^{-\kappa} \le 1 + 2\kappa/P$ is used without a reason. Bernoulli gives it at once. |
| N2 | nit | Prop. TA(i) | "for every prime $p > T_A$" uses the monotonicity of (ii); say "by (ii)". |
| N3 | nit | Thm. `thm:app-s2-main` cost | The Bezout exponent needs $d$ reduced modulo $p-1$: an extra $O(\log d)$ operations on integers of size $\max(d,p)$. This is irrelevant in the paper ($d \le c$). |
| N4 | nit (main.tex) | Prop. `prop:decoupled-sde` | "The scalars depend only on $(p,\kappa,a)$": the appendix shows they depend on $(p,\kappa,\xi)$, and $a$ does not enter. |
| N5 | nit | before eq. `eq:app-s2-R` | $\Phi = \kappa(1-1/R)$ is defined and never used again. |

## 1. Per-statement verdicts

**Lemma `lem:app-s2-gcd` (gcd reduction). Holds [proved].**
(a) The image of $x\mapsto x^d$ has order $(p-1)/\kappa$ and lies in $Q_0$.
(b) $t\kappa d' \equiv \kappa \pmod{p-1}$, so $s_b^d = u_b^\kappa$, and $t \ge 1$ keeps zeros at zero. Edge case $q' = 1$ (κ = p−1): $t = 1$.
(c) Needs $a+1$ columns. The end-to-end runs use $d \in \{2,6,10\}$, $\{3,15,21\}$ and $\{4,12\}$ with $\gcd(d,p-1) = \kappa$ **[exact]**.

**Coset generator, coset test, roots (paragraphs). Hold.** A uniform $x$ is a coset generator
with probability $\varphi(\kappa)/\kappa \ge 1/\kappa$. $X^\kappa - w$ has $\kappa$ distinct
roots for $w \in Q_0$, since $\kappa \mid p-1$ and $p \nmid \kappa$. The Rabin citation was not
checked (as the header says).

**Lemma `lem:app-s2-tensor` (two-level tensor). Holds [proved + exact].** Level one: after
normalising, $c_{b^*} = 1 \in Q_0$, so $i(b^*) = 0$ and $\omega_{b^*} = 1$ is a legal root.
Level two: the relation for $i = 0$ follows from $z_0 = 1$ and linearity. Both identities in
(b) check by direct expansion. $S_{00} \ni b^*$ because $j(\nu^*) = 0$.
"Each coordinate in $W\otimes W$" is right, because $W\otimes W$ is exactly the set of
$\kappa\times\kappa$ matrices whose rows and columns lie in $W$. The cost count is an
overestimate but valid.
Exact runs: 135 instances at $(\kappa,p) = (2,257), (3,26263), (4,4194329)$, $a = 1,2,3$, with
random, all-zero, repeated, rank-one and sparse columns. Both identities of (b) were asserted
for each, and $S_{00} \ne \emptyset$ in each (`algorithm_check.py`).

**Definition of contraction and of $E_2$; $\xi$-independence. Claim holds; given reason incomplete (G1).**
Every coset generator is $\xi' = \xi^u q$ with $\gcd(u,\kappa) = 1$ and $q \in Q_0$; for $q \ne 1$
this is not a power of $\xi$ in general. The fix is in "Proposed paper text" (P1). Exact check: for $\kappa = 3,4,5$ and every prime
$p \equiv 1 \pmod\kappa$, $\kappa+1 < p < 140$, whether $p \in E_2(\kappa)$ is the same for all
coset generators **[exact]**.

**Lemma `lem:app-s2-witness`. Holds [proved].** Zero entries $C_{ij}$ simply zero their cells.
$u_b \ne 0$ on $S_{00}$ because $C_{00} \ne 0$.

**Lemma `lem:app-s2-normal` (normal form). Holds [proved].** The annihilator has dimension
$\kappa^2 - (\kappa-1)^2 = 2\kappa-1$. The kernel of $(\alpha,\beta)\mapsto(z_iz_j(\alpha_j+\beta_i))$
is $\{(c\mathbf 1,-c\mathbf 1)\}$ because every $z_iz_j \ne 0$. The coset clause follows from
$z_iz_j \in Q_{i+j}$. The normalisation $\beta_0 = 0$ is WLOG.

**Weil bound (as quoted).** It matches Lidl–Niederreiter Thm 5.41 as I know it: $\psi$ of order
$m>1$; $f$ monic of positive degree, not an $m$-th power; $d$ distinct roots; then
$|\sum\psi(af(x))| \le (d-1)\sqrt q$. **I did not open the book.**

**Lemma `lem:app-s2-weil-count`. Holds [proved + exact].** The indicator identity uses only
that $\chi$ is trivial on $Q_0$ with $\chi(\xi) = \omega$. Points of $R$ outside $S$ contribute
at most 1 each, and $f_e$ has multiplicities in $[1,\kappa-1]$, so it is not a κ-th power.
Both sums in the closed form are exact (`thresholds.py` §1, exact rationals in
$\mathbb Q[\sqrt p]$, $\kappa \le 15$, $\ell \le 2\kappa+2$). The bound
$E \le (\ell-1)\sqrt p + 1$ uses $\ell \le \kappa$ only for the constant term.
Exhaustive count of $N$ on 10 690 random instances ($p < 140$, every $\kappa \mid p-1$,
$\ell \le \kappa+2$): no violation, and the worst $|N - (p-\ell)/\kappa^\ell|/E$ is 0.80
**[exact]**.

**Theorem `thm:app-s2-main` (Schedule 2) and Lemma `lem:app-s2-stage`. Hold [proved + exact].**
- *Stage lemma.* The roots $0,-t_0,\dots$ are distinct because accepted $t_j$ are nonzero ($2z_j^2t \in Q_0$) and new. The chain $\Lambda \ge p/\kappa^\ell - \ell\sqrt p \ge p/(2\kappa^\ell)$ needs $\sqrt p \ge \max(\ell+1,\, 2\ell\kappa^\ell)$; both follow from $\sqrt p \ge 2\kappa^{\kappa+1}$ (`thresholds.py` §2, every $\kappa \le 59$, $\ell \le \kappa$).
- *Exact $\Lambda$ at the boundary.* At $p$ just above $4\kappa^{2\kappa+2}$ ($p = 257$ for κ = 2, $26251$ for κ = 3), over 40 random admissible prefixes per stage, the minimum of $\Lambda/(p/(2\kappa^{j+1}))$ is 1.99 and 1.93 **[exact]**. So the hypothesis $p \ge 4\kappa^{2\kappa+2}$ of Remark `rem:app-s2-four` is not near-tight at small κ, and nothing breaks at the boundary.
- *Abort budget.* $(1-1/\kappa)^{\kappa(k+3)} \le 2^{-k-3}$. Each stage fails with probability at most $e^{-\tau}$, and $\kappa 2^{-\tau} \le 2^{-k-3}$ for $\tau = k+3+\lceil\log_2\kappa\rceil$. Markov with $k+1$ independent attempts gives $2^{-k-1}$. Total $0.75\cdot 2^{-k}$.
- *Cost.* $\sum_{\ell=2}^\kappa \kappa^\ell < \kappa^{\kappa+1}/(\kappa-1) \le 2\kappa^\kappa$ for $\kappa\ge2$.
- *End to end.* The full algorithm (Phase 0 at those primes, then tensor, witness, Bezout exponent and exact check) solved all 135 instances above. Phase 0 used 11, 31 and 419 draws at κ = 2, 3, 4 **[exact]**.
- The statement matches `main.tex` Theorem `thm:power-sde`(ii) word for word in substance: hypothesis $p \ge 16\kappa^{2\kappa+2}$, arity, cost and abort bound.

**Remark `rem:app-s2-four`. Holds.** Only the stage lemma uses the size of $p$. Reusing Phase 0
across nodes is harmless: Prop. `prop:descent` gives the exact output for every valid witness,
so shared scalars create no correlation.

**Proposition `prop:app-s2-TW`. Holds [proved + float]; following paragraph has G3.**
- *Distinct roots.* $1-\xi^{-i}$ are distinct because the $\xi^{-i}$ lie in distinct cosets.
- *Counting identity.* $\kappa^\kappa E_\kappa(\kappa,p) = ((\kappa-2)\kappa^\kappa+1)\sqrt p + \kappa^\kappa - \kappa$, exact for every $\kappa \le 15$.
- *Positivity.* Holds exactly for $p > T_W$.
- *Part (ii).* Uses $\sqrt p \ge 1$.
- *Values.* $T_W(2) = 6.5616$, and the ratio $16\kappa^{2\kappa+2}/T_W$ falls monotonically: 156.06, 125.4, 63.6, 44.4, 36.0, 31.4, 28.4, 26.45 for κ = 2..9 **[float]**. All match the text.

**Lemma `lem:app-s2-moments`. Holds [proved + exact].** I re-derived the pair count
$h\,m'_{c'+j}$ and the index shift $m-c' = -(i+c)$. Brute force over all $y$, comparing
$\mathbb E[n_j]$ and $\mathbb E[n_j^2]$ with the formula as exact rationals for every $j$, at
$(p,\kappa) = (7,2),(11,2),(7,3),(13,3),(19,3),(31,3),(13,4),(17,4),(11,5),(13,6)$: all equal
**[exact]**.

**Lemma `lem:app-s2-cyclo`. Holds [proved + exact].** I recomputed all five families
$K(0,0), K(s,0), K(0,t), K(s,-s)$ and the Jacobi part, for both $m_b$ and $m'_c$, including the
signs $1-\kappa[b=\varepsilon]$ and $1-\kappa[c=\varepsilon]$. The bound
$|2-\kappa[b=0]-\kappa[b=\varepsilon]| \le 2(\kappa-1)$ is attained when $b = 0 = \varepsilon$.
Exact sums plus the deviation bound were checked at every prime $p \equiv 1 \pmod\kappa$ below
$2\cdot10^4$ (κ = 2, 3, 4), $1.2\cdot10^4$ (κ = 5), $8000$ (κ = 6, 7) and $5000$ (κ = 8), 5681
primes in all. There were no violations; the worst ratios were 0.81–1.00 **[exact]**. At
κ = 2 the bound is an equality at every prime (4500 equalities, checked in integers), so it
cannot be improved there.

**Proposition `prop:app-s2-TA`. Holds [proved + interval + exact].**
- *(i).* The identity $R = \kappa^\kappa p^{\kappa-1}/(p-1)^\kappa + LF$ is exact algebra, and so is $L \le 1$ (using $(p-2)p < (p-1)^2$). The inequality $\log(1+x) \le x - x^2/2 + x^3/3$ holds because $g' = x^3/(1+x)$. The rewriting of $(1/\kappa)\sum(1+\delta')/(1+\delta)$ uses $\sum(\delta'_c-\delta_{-c}) = 0$, and Cauchy–Schwarz gives the bound. Second-moment step: $\Pr[n>0] \ge 1/R$.
  - $R \le U_\kappa(p)$ was checked at every prime above with $\Delta \le 1/2$: no failure **[exact R vs float U]**.
  - The fraction of good $y$, counted exactly at κ = 3, $p \in \{97,103,109,139,211\}$, is 0.95–0.99 against bounds 0.17–0.59. Sampled at κ = 4, $p \in \{881, 929\}$: 0.89 and 0.93 against 0.011 and 0.053. The bound is valid and loose.
- *(ii).* Monotonicity: I recomputed the derivative of $\Delta$; $E_{\max}$ is nondecreasing in $\Delta$; the first term has negative log-derivative.
  - Lower bound: $U > 1 + \kappa^\kappa/p$, so the condition fails at $p \le (\kappa-1)\kappa^\kappa$; checked at that point for κ = 2..40.
  - Upper bound, κ ≥ 6: every constant was checked in interval arithmetic for κ = 6..199 (1000 digits): $\Delta(P) \le 1.01\kappa^{(3-\kappa)/2} \le 0.1$, $u_\Delta \ge 0.28$, $E_{\max} \le 1.2\kappa^{2-\kappa} \le 1$, first term $\le 1/\kappa + 2\kappa^{-\kappa-1}$, final sum $< 0.07$ at κ = 6. The written argument proves it for all κ ≥ 6 (see N1 for the one unexplained step). A first 50-digit run "failed" for κ ≥ 33; that was a precision artifact (terms of size $\kappa^{-\kappa-1} < 10^{-50}$), cured by 1000 digits.
  - κ = 3, 4, 5: $\Delta = 0.2857, 0.1943, 0.0965$ and $U = 1.48419, 1.27937, 1.20238$; rigorous upper bounds 1.48419, 1.28050, 1.20238, all below $\kappa/(\kappa-1)$. Margins 0.01581, 0.05397, 0.04762, matching the Remark's 0.0158, 0.0540, 0.0476 **[interval]**.
  - $U_\kappa(\kappa^{\kappa+1}) < \kappa/(\kappa-1)$ for every κ = 3..40 **[interval]**.
- *(iii).* Chebyshev gives $4(R-1)$; $K \ge \ln(4\kappa)/q$; $(p/h)^\kappa \le e\kappa^\kappa$ since $\kappa \le p-1$. Empirical round success at the first prime above $T_S$ (κ = 2: $p = 71$; κ = 3: $p = 739$; κ = 4: $p = 8597$), 300 rounds each: 0.97, 0.98, 0.98, against the claimed 3/8 **[float, sampled]**.

**Table `tab:app-s2-thresholds`. All 40 entries reproduce** to the printed precision
(`thresholds.out`), for example $T_A(3) = 79.039$, $T_A(4) = 868.996$, $T_S(4) = 8596.4$,
$T_A(9) = 3.0994\cdot10^9$. Also $T_S(\kappa)/\kappa^{\kappa+1} = 9.075$ at κ = 3, at most 8.395
for κ = 4..40, and 8.0000 from κ = 20 on. So `main.tex`'s "$\le 10\kappa^{\kappa+1}$
($\le 9$ for κ ≥ 4), $3 \le \kappa \le 40$" holds **[float]**.

**Corollary `cor:app-s2-decoupled`. Holds except for the abort budget (G2).** "Hence when
κ ≥ 3 and $p \ge \kappa^{\kappa+1}$": a prime cannot equal $\kappa^{\kappa+1}$, so $p > T_A$.
The exhaustive-search fallback below $T_S$ is a constant for fixed κ but is not within
$(1+\kappa^\kappa)\poly$. The text separates the two regimes correctly.

**Corollary `cor:app-s2-small`. Holds [exact + proved]; see D1.** My own DFS (bitmask search
over $\beta$, exhaustive at failures, every witness re-verified entry by entry) finds:
- κ = 2: no exceptional prime below 400. At $p = 3$ (where κ = 2 = p−1) the contraction $\begin{psmallmatrix}1&0\\1&1\end{psmallmatrix}$ needs a zero entry.
- κ = 3: none below 400.

The proof's list of κ = 3 primes below $T_A(3) = 79.04$ is complete: the next prime
$\equiv 1 \pmod 3$ is 97.

**Scope list.** All of these reproduce **[exact]**:
- $E_2(4) = \{5,13,17,29,37,53\}$, by complete search to $870 > T_A(4)$.
- $E_2(5) = \{11,31,41,61,71,101,131,151,181\}$, by complete search to $12658 > T_A(5)$.
- κ = p−1 has no contraction for $5 \le p < 40$, in both modes.
- The symmetric form fails at κ = 3 exactly for $p \in \{7,13,19,61\}$ below 400, both with and without zeros.
- $E_2(6) \cap [7, 571]$: agrees prime for prime with the earlier list (§2).
- The Chevalley–Warning remark ($\kappa a+1$ columns) is standard.

## 2. E_2(6) spot check

`e2_stream.py 6 7 1000 zero` is a complete search, prime by prime, with output in
`e2_k6_stream_1000.out`. I stopped it by hand after it settled $p = 571$, because exhaustive
refutations near $p = 550$ took about four minutes each on the loaded machine. On $[13, 571]$ its
exceptional set (41 primes) agrees **prime for prime** with the 53-prime list in
`2026-11-02-rees-threshold-2/xval_k6.out`:
13, 19, 31, 37, 43, 61, 67, 73, 79, 97, 103, 109, 127, 139, 151, 157, 163, 181, 193, 199, 211,
223, 241, 271, 277, 283, 307, 331, 349, 367, 373, 379, 409, 421, 433, 439, 463, 487, 499, 523, 547.
Every other prime $p \equiv 1 \pmod 6$ in $[13, 571]$ has a verified contraction **[exact]**. The 11 listed primes above 571 (577 to 859) were not re-checked.
$p = 7$ is the case κ = p−1, covered in §1.

An earlier `e2_search.py 6 3000` run hit its 1200 s limit and printed nothing. This is not a
complete reproduction of $E_2(6)$: that would need every prime up to $T_A(6) = 233\,577$.

## 3. Comparison with the earlier reports (read after my own pass)

- `2026-11-02-rees-weil-threshold.md`, §§0, 3, 6: same lemmas and the same $U$, $T_A$, $T_S$.
  - Its κ ≥ 6 constants ($A \ge 0.18$, $E_{\max} \le 1.8\kappa^{2-\kappa}$) differ from the appendix's ($u \ge 0.28$, $1.2\kappa^{2-\kappa}$, $2.4$); I verified the appendix's.
  - Its Theorem 3 counts "κK = O(κ^{κ+1} log κ) coset tests". That is draws: each draw costs up to κ coset tests. The appendix and `main.tex` already say "draws" and "$O(\kappa^{\kappa+2}\log\kappa)$ coset tests", which is correct.
  - No conflict.
- `2026-11-02-rees-small-prime-arity.md`, §§1–3: the same normal form. It already notes that zero entries are allowed, and it has the same $E_2(2..5)$ and the same symmetric failures {7,13,19,61}. Its remark that "the choice of representatives $z_i$ is irrelevant; only the coset labelling matters" is the content of G1; the appendix's one-line version lost the diagonal rescaling. No conflict.
- The appendix's header (3) says its verification script lives in a session scratchpad, not the repo. The scripts here are a repo copy of an independent re-verification.

## 4. Statement that now holds

Every statement of Appendix A holds as written, with these qualifications:
- the $\xi$-independence sentence needs the proof P1;
- Cor. `cor:app-s2-decoupled` needs $r = \lceil (k+3)/\log_2(8/5)\rceil$ rounds, or a budget that names the $\xi$ search;
- the sentence after Prop. `prop:app-s2-TW` should claim existence and arity, not the cost, in the band.

`main.tex` Theorem `thm:power-sde`(ii) is proved by the appendix exactly as stated (AI-checked,
pending human review). Prop. `prop:decoupled-sde` is proved by Props TW/TA and Cor.
`cor:app-s2-decoupled` for $\kappa \ge 3$, $p \ge \kappa^{\kappa+1}$, and for $p \notin E_2(\kappa)$.
Its quoted $E_2(4)$ and $E_2(5)$ are reproduced, and its $T_S$ bound for κ = 3..40 is
reproduced.

## 5. Still missing

- **Human review.** It is the binding gate. The steps that most deserve a human eye are the second-moment chain of Prop. TA(i) (the $\log(1+x)$ and Cauchy–Schwarz steps) and the Weil-bound citation (the book was not opened, by me or by the author).
- **$E_2(6)$ in full** (complete search to $T_A(6) = 233\,577$) and **$E_2(7)$**: reproduced only partly here, or not at all. These are quoted, not proved, in the appendix, and the earlier reports' searches are the only full ones.
- **$T_S(\kappa) \le 10\kappa^{\kappa+1}$ for all κ** is unproved, as the appendix and `main.tex` already say.

## 6. Claim gates that must stay false

- Theorem `thm:power-sde`(ii) stays **conditional**: AI-checked, pending human review. Theorem `thm:main` must not depend on it.
- The decoupled hypothesis of Prop. `prop:decoupled-sde` is **not adopted** in Theorem `thm:power-sde`, Remark `rem:combined-schedule` or Table `tab:main-regimes`. That is the owner's decision.
- There is no priority claim for any statement of the appendix, and no speedup claim (`speedup_claim_allowed` stays false).
- Every Rees claim gate in the registry stays false.

## 7. Next step

The integrator applies P1–P4 (and optionally P5–P8). A full $E_2(6)$ reproduction to
$233\,577$ would take about one CPU-hour with `e2_search.py`, or less with the C searcher of
the small-prime report. It is a candidate for a background job, not needed for the appendix's
proved content.

Reproduce (each took a few minutes or less of wall time on the loaded shared machine; `finite_checks.py` took 1.5 min):

    cd research/audits/reviews/2026-11-03-rees-check-app-a
    /opt/anaconda3/bin/python -I thresholds.py        # constants, table, interval checks
    /opt/anaconda3/bin/python -I finite_checks.py     # Weil count, moments, cyclotomic, R <= U
    /opt/anaconda3/bin/python -I algorithm_check.py   # end-to-end Schedule 2, stage lemma, samplers, symmetric form, xi
    /opt/anaconda3/bin/python -I e2_search.py 5 12658 zero    # E_2(5); 'strict' for the all-nonzero variant

## Proposed paper text

All targets are in `docs/papers/rees-hsp/appendix-schedule2.tex` unless marked. Status label for
each: AI-checked, pending human review.

**P1 (G1). Target:** the sentence after the definition of two-level contraction, beginning
"Whether a two-level contraction exists does not depend on the choice of $\xi$". Replace it with:

```latex
Whether a two-level contraction exists does not depend on the choice of $\xi$. Every other coset generator has the form $\xi' = \xi^u q$ with $\gcd(u,\kappa) = 1$ and $q \in Q_0$. Let $\pi(m) \in \mathbb{Z}_\kappa$ be the residue of $um$. Then $\xi'^m = z_{\pi(m)}s_m$ with $s_m \in Q_0$ and $s_0 = 1$, and $\pi$ is a permutation fixing $0$. The map $w \mapsto \tilde w$, $\tilde w_{\pi(m)} = s_mw_m$, carries $W' = \{w : \sum_m \xi'^m w_m = 0\}$ onto $W$. So if $C$ is a two-level contraction for $\xi$, then $C'_{ij} = s_is_jC_{\pi(i)\pi(j)}$ has every entry in $Q_0^\circ$ and $C'_{00} = C_{00} \ne 0$. For $X' \in W'\otimes W'$ we get $\sum_{i,j}C'_{ij}X'_{ij} = \sum_{a,b}C_{ab}\tilde X_{ab} = 0$, where $\tilde X_{\pi(i)\pi(j)} = s_is_jX'_{ij}$ lies in $W\otimes W$. Hence $C'$ is a two-level contraction for $\xi'$.
```

**P2 (G2). Target:** proof of Corollary `cor:app-s2-decoupled`, the sentence "For the cost, take
$r = \lceil (k+1)/\log_2(8/5)\rceil$ rounds and treat Phase~1 as in the proof of
Theorem~\ref{thm:app-s2-main}." Replace it with:

```latex
For the cost, find $\xi$ with $\kappa(k+3)$ draws as in Phase~0, which fails with probability at most $2^{-k-3}$. Then take $r = \lceil (k+3)/\log_2(8/5)\rceil$ rounds, which all fail with probability at most $2^{-k-3}$, and treat Phase~1 as in the proof of Theorem~\ref{thm:app-s2-main}, which fails with probability at most $2^{-k-1}$. The total abort probability is below $2^{-k}$.
```

**P3 (G3). Target:** the paragraph after Proposition `prop:app-s2-TW`, its first two sentences
("With Lemmas … for every prime $p > T_W(\kappa)$. Above … as in Theorem~\ref{thm:app-s2-main}."). Replace them with:

```latex
With Lemmas~\ref{lem:app-s2-tensor} and~\ref{lem:app-s2-witness}, Proposition~\ref{prop:app-s2-TW} gives a nonzero solution of~\eqref{eq:app-s2-target} from $M = (a+1)((\kappa-1)a+1)$ arbitrary columns for every prime $p > T_W(\kappa)$, and the output is never wrong. Above $4((\kappa-1)\kappa^\kappa+1)^2$ the cost is as in Theorem~\ref{thm:app-s2-main}.
```

and, in the next sentence, after "with $O(\kappa p)$ coset tests", insert:

```latex
; this is a constant for fixed $\kappa$, but it can reach order $\kappa^{2\kappa+3}$ and is not within the factor $1+\kappa^\kappa$ of Theorem~\ref{thm:app-s2-main}
```

**P4 (D1). Target:** proof of Corollary `cor:app-s2-small`, after "The search checks all
$\kappa^2$ coset conditions directly." Insert:

```latex
It allows zero entries, as the definition of $E_2$ does, and this matters: at $\kappa = 2$, $p = 3$ and at $\kappa = 3$, $p \in \{7, 13\}$, every two-level contraction has a zero entry. A third independent search (\file{research/audits/reviews/2026-11-03-rees-check-app-a.md}) reproduces the result.
```

and in the first item of the scope list, after "These are finite computations, not reproduced
here;", insert:

```latex
both $E_2(4)$ and $E_2(5)$ were reproduced by an independent complete search up to $T_A(4)$ and $T_A(5)$ (\file{research/audits/reviews/2026-11-03-rees-check-app-a.md}); requiring every entry to be nonzero would enlarge them to $E_2(4) \cup \{61\}$ and $E_2(5) \cup \{191, 211, 241, 251\}$;
```

**P5 (N1, optional). Target:** Prop. TA proof, κ ≥ 6, the sentence "The first term is
$\kappa^{-1}(1-1/P)^{-\kappa} \le \kappa^{-1}(1 + 2\kappa/P) = \dots$". After
"$\le \kappa^{-1}(1 + 2\kappa/P)$", insert:

```latex
\ (by Bernoulli's inequality $(1-1/P)^\kappa \ge 1 - \kappa/P$ and $\kappa/P \le 1/2$)
```

**P6 (N2, optional). Target:** Prop. TA(i), the sentence "In particular $p \notin E_2(\kappa)$ for
every prime $p > T_A(\kappa)$." Replace it with:

```latex
In particular, by~(ii), $p \notin E_2(\kappa)$ for every prime $p > T_A(\kappa)$.
```

**P7 (N4, optional). Target:** `main.tex`, Proposition `prop:decoupled-sde`, the sentence "The
scalars depend only on $(p,\kappa,a)$." Replace it with:

```latex
The scalars depend only on $(p,\kappa)$ and the coset generator $\xi$.
```

**P8 (N5, optional). Target:** the sentence before eq. `eq:app-s2-R`. Replace "Put $R = \mathbb{E}[n_j^2]/\mathbb{E}[n_j]^2$, which does not depend on $j$, and $\Phi = \kappa(1 - 1/R)$." with:

```latex
Put $R = \mathbb{E}[n_j^2]/\mathbb{E}[n_j]^2$, which does not depend on $j$.
```

N3 needs no paper text, because $d \le c$ in every use.
