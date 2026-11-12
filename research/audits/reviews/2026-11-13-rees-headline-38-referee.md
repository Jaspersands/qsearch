# 2026-11-13 Hostile referee: core headline E_H(9) = 38 (Schedule 1H, §5.1 of main-core.tex)

AI referee (one Claude session), pending human review. No Git, no network, no paper file edited,
`make_numbers.py` not run, no claim gate touched. Text refereed: `docs/papers/rees-hsp/core/main-core.tex`
as it stands on 2026-11-13 (1216 lines; PDF 55 pp. of the same timestamp). Scripts and outputs:
`research/audits/reviews/2026-11-13-rees-headline-38-referee/`.

## 0. Verdict

**CORRECT WITH FIXES.** All fixes are wording, status or a missing one-line justification; I found
no mathematical gap in §5.1, in the new error accounting, or in the new numbers.

- Every new proof (lem:stage, lem:finish, the T_j recursion, lem:two-term, def:schedule1h,
  thm:halving (i)–(iii), cor:hcd, rem:kappa-two, lem:halved-exponent (i)–(iii)) was re-derived
  line by line from the TeX. Status: **PROVED given cited theorems** (thm:is-import, lem:rounds as
  proved in the paper, Weil's bound for two-variable diagonal equations with nonzero right side,
  Rabin), plus the exact computation for p < 26244.
- **38 stands.** It is attained exactly at the primes p ≡ 1 (mod 2520). My own code, written from
  the definitions, reproduces E_H(c) = 3, 6, 10, 14, 20, 25, 29, 38. Above 26244 the hand tail
  argument in the text is a complete proof; it is not just asserted.
- **Status is unchanged.** 38 inherits everything 53 rests on (lem:rounds: AI only, not confirmed
  by Ivanyos), plus §5.1 (AI only). No human has read either.

## 1. Findings

Line numbers refer to `core/main-core.tex`. None is a mathematical error. F1–F3 concern how
status is reported, F5–F6 are missing justifications, and the rest are cosmetic.

**F1 (status honesty), line 246.** The text says the halving "was proved by one AI session and
refereed by another (verdict: correct with fixes, all applied here)". The 11-12 referee read the
attack note's version, not the §5.1 write-up. That version used Hasse–Weil for the curve, had an
F2 finish and had no 4κ⁴ admissibility switch. The integrator's own report (§8) says that §5.1
"has had no referee in this form". Replace

> which was proved by one AI session and refereed by another (verdict: correct with fixes, all applied here), and on the exact computation of Lemma~\ref{lem:halved-exponent}; no human has read it.

with

> which was proved by one AI session and refereed in that draft by a second (verdict: correct with fixes, all applied here); the write-up of Section~\ref{sec:halving}, which differs from the draft in Lemma~\ref{lem:two-term} and Definition~\ref{def:schedule1h}, was refereed by a third AI session (verdict: correct with fixes, which are applied), and the exponent also rests on the exact computation of Lemma~\ref{lem:halved-exponent}; no human has read it.

(If F1–F7 are not applied, drop "which are applied".)

**F2 (status), line 555, rem:is-printed.** Replace

> It does not cover the shorter depth or the exponent $\ReesClassNineQueryExp$ at $c = \ReesClassNineClass$.

with

> It does not cover the shorter depth, the halving of Section~\ref{sec:halving}, or the exponents $\ReesClassNineQueryExp$ and $\ReesClassNineHalvedExp$ at $c = \ReesClassNineClass$.

rem:main-solver (line 210) already says "His confirmation covers neither the shorter depth L_d nor
the halving", which is correct. Only this remark lags behind it.

**F3 (status), line 1112, Outlook "Halving at the confirmed depth".** The clause "which the
confirmation of Remark~\ref{rem:is-printed} covers" can be read as covering 95. After "the same
halving gives the class-nine exponent $95$ in place of $145$", insert

> (the confirmation covers the inner solver only, not the halving)

I recomputed 95 independently (`full_depth_95.json`: 95 at 2521, 7561, 12601, 15121, 20161 below
30000, and 95 as the residue-tail maximum). So the number is right.

**F4 (consistency), line 1094, rem:query-separation.** This line is still true, but it is weaker
than the theorem. Replace

> at fixed $c$ it is polynomial in $m$ with exponent at most $E_1(c)$, uniformly in $p$ (Lemma~\ref{lem:exponent}).

with

> at fixed $c$ it is polynomial in $m$ with exponent at most $E_H(c) \le E_1(c)$, uniformly in $p$ (Lemmas~\ref{lem:halved-exponent} and~\ref{lem:exponent}).

**F5 (unstated step behind the table), line 1075, caption of tab:query-crossover.** The caption
defines Q_q as the maximum over all primes p ≥ 11. The computation is exact below 26244 and runs
over residues mod 5040 above. That residue step needs "A_d depends only on p mod 5040 for
p ≥ 26244", and the paper never states it. The fact is true; I verified it on all 1320 primes in
[26244, 40000], with 0 mismatches. After "and at $p \equiv 1 \pmod{2520}$ for the last row." insert

> For $p \ge 26244$ the arities $A_d(a)$, $d \le 9$, depend only on $p$ modulo $5040$: by Lemma~\ref{lem:zero-sum-length}(ii)--(iii) and Definition~\ref{def:schedule1h} the candidates there are~(a), with $L = 1$ or $2$ according as $(p-1)/\kappa$ is even or odd, and the plan $(1,\mathrm{F1})$, and $\kappa_d$ and these parities are determined by $p \bmod 5040$; below $26244$ the maximum is an exact computation.

**F6 (explicit T), line 722, proof of thm:halving(ii).** rem:is-import(d) cuts each attempt off
at 4T. That needs T as a computable function. The proof only says "by induction its expected time
is bounded as claimed". This is routine, but the theorem says "explicit". Insert before "When every
plan run is at a degree":

> Explicitly, let $R_\kappa(p)$ bound the expected number of field operations of one Las Vegas extraction of a root of $X^\kappa - x$~\cite{Rabin1980}, and let $T^{\mathrm{(a)}}_\kappa(a)$ be the deterministic cost of candidate~(a) (Lemma~\ref{lem:rounds}). Then $T_1(a) = O(a^3)$, $T_\kappa(a) \le T^{\mathrm{(a)}}_\kappa(a)$ when~(a) is run, and otherwise $T_\kappa(a) \le sA_\kappa(a)\bigl(T_D(a) + R_\kappa(p)\bigr) + (a+1)\bigl(O(\kappa\log p) + R_\kappa(p)\bigr) + O\bigl(2^sA_\kappa(a) + aA_\kappa(a) + a^3\bigr)$ field operations, at most $2\kappa$ draws of $u$ being expected per representation; this recursion defines $T$.

**F7 (cosmetic), line 690, lem:two-term.** The proof gives T_1 ⊇ F_p^×. Equality also needs
0 ∉ T_1, which only Remark kappa-two shows, and only later. Definition and Theorem use "⊇". Replace
"so $T_1 = \Fp^\times$ for every even $\kappa$" with "so $T_1 \supseteq \Fp^\times$ for every even
$\kappa$".

**F8 (labels), lines 744 and 213.** The second sentence of (iii), C^H_c = C_c for c ≤ 9, is also
an exact computation (line 752 says so). The lemma title and the import sentence omit it, and
thm:main(4) uses it.
- Line 744: replace "part~(ii) partly an exact computation" with "parts~(ii) and~(iii) partly an
  exact computation".
- Line 213: replace "also use exact computations (Lemmas~\ref{lem:halved-exponent} and~\ref{lem:exponent})"
  with "and $C^H_c = C_c$ for $c \le 9$ also use exact computations (Lemmas~\ref{lem:halved-exponent} and~\ref{lem:exponent})".

**F9 (pre-existing, optional), line 213.** The list "Its only imported ingredients" omits
Dirichlet's theorem on primes in progressions. It is used only for the lower bounds in
lem:exponent(i) and lem:halved-exponent(i), and the same sentence quotes the lower bound
⌈c/2⌉²+2⌊c/2⌋. After "Las Vegas root finding~\cite{Rabin1980}" add "(the lower bounds on $E_1(c)$
and $E_H(c)$ also use Dirichlet's theorem on primes in arithmetic progressions)". This omission is
older than this pass.

**F10 (bookkeeping, not paper text).**
- Top-level `docs/papers/rees-hsp/numbers.tex` does **not** contain `\ReesClassNineHalvedExp`.
  Only `core/numbers.tex:9` does. The integrator report §4 says the two are identical, so someone
  has since removed it, presumably fix (b) of that report. The core build only needs core/.
- `arxiv/` copies and METADATA "50 pages" (now 55) are stale until `build_package.sh` is rerun.
- `core/numbers.tex:8` cites `s1h_independent.out` as the source. Appendix line 1139 says "from
  the computation above", which is `halved_schedule.py`. Both give 38.

## 2. Line-by-line obligations

**(a) lem:two-term (690–695): PROVED given the cited Weil bound.**
- N counts u^κ + εv^κ = η with η ≠ 0. For a two-variable diagonal equation with nonzero right
  side, |N − p| ≤ (κ−1)²√p. (Jacobi sums: the χ₁χ₂ = 1 terms have modulus 1 ≤ √p, the others √p.)
  This is the same form as in lem:zero-sum-length(iii), so no new import is needed. The LN 6.37
  locator is still flagged `NEEDS HUMAN VERIFICATION` (line 595).
- (κ−1)²√p = κ²√p − (2κ−1)√p ≤ p/2 − (2κ−1)√p, which holds iff √p ≥ 2κ², that is p ≥ 4κ⁴.
- At most 2κ pairs have uv = 0. That leaves ≥ p/2 + (2κ−1)√p − 2κ ≥ p/2 pairs with uv ≠ 0. Each
  u occurs at most κ times, so there are ≥ p/(2κ) good u, a fraction > 1/(2κ).
- Each such pair gives η = y₁ + εy₂ with **both** y_i ∈ P. This is stronger than the
  y_i ∈ P ∪ {0} that is needed.
- The bound applies at p ≥ 4κ⁴: 64, 1024, 5184, 16384 for κ = 2, 4, 6, 8. At p < 4κ⁴ the
  definition uses exact tables, so it does not need the lemma. The exact range p < 26244 = 4·9⁴
  covers p < 4κ⁴ for every κ ≤ 9.
- κ = 2 is proved by hand for every odd p (rem:kappa-two; checked: −1 square ⇒ ε nonsquare;
  −1 nonsquare ⇒ ε square and two squares).
- Falsifier: T₁ = F_p^× and 0 ∉ T₁ at all 12,675 pairs (p, κ), κ ∈ {2,4,6,8},
  p ∈ [4κ⁴, 60000]. The count bound #u ≥ p/(2κ) holds for every coset of η at 845 pairs
  (`weil_T1_check.json`).

**lem:stage, lem:finish and the T_j recursion (658–686): PROVED.**
- The q-coset argument P_D = P ∪ qP is correct, and no primitive root is used (M1(i) applied).
- The stage case split I/J is correct, including Σ_J x′v = −q⁻¹u = εu.
- Disjointness and non-emptiness hold.
- F0 and F1 are correct.
- The recursion T_j = T_{j−1} ∪ εT_{j−1} ∪ (T_{j−1} + εT_{j−1}) follows from splitting y. It is
  independent of q: changing q multiplies ε by P.
- T_j stabilizes by j ≤ κ+1. In fact j ≤ κ suffices.
- The recursion matches a brute-force evaluation of T(c^{(j)}) straight from the definition at
  every p < 120, κ ∈ {2,4,6,8}, j ≤ 3: 0 mismatches.

**def:schedule1h and thm:halving (697–724): PROVED.**
- (i) Arity is nondecreasing in s, so the least admissible s ≤ κ+1 is always the plan chosen.
  The log₂G^L bound is not even needed. Candidate (a) gives A_κ ≤ G^L.
- (ii) Induction on κ and on the level is correct. The κ-th roots are explicit inputs (M1(ii)).
  The u-draws succeed with probability ≥ 1/(2κ), and the outcome z = 0 is an additional success.
  The output is checked, and "deterministic if every plan is at p < 4κ′⁴" is correct given the
  preprocessing.
- (iii) Correct. The min-arity choice is bounded through the degree-optimal candidate with least
  constant, and the inner solver is the min-arity H_D. This is consistent with Definition 1H's
  arity A_D(a)^s n_F.

**cor:hcd, rem:kappa-two: PROVED.**
- (1,F0) is never admissible, because −ε = q⁻¹ ∉ P.
- At a=0, A_2(0) = 1. Tie: (1,F1) is chosen over (2,F0).

**(b) Error budget: ε in total.**
- rem:is-import(d), line 545: preprocessing ≤ n_pre·ε/(6n_pre) = ε/6 and solver ≤ N·ε/(6N) = ε/6,
  so the third is ε/3.
- Proof of thm:main, lines 836 and 843: span failure ≤ 1/((p−1)p^τ) ≤ ε/3, aborts ≤ ε/3, QFT
  approximation ≤ ε/3. Total **ε**.
- n_pre ≤ 2(c−1) holds: there are at most c−1 distinct degrees in {2..c}, each with a zero sum
  and a q.
- N_solver = (m+τ)Σ_d∏_{d′<d}M_{d′} is correct: stage-d merges equal stage-(d−1) inputs.
- Markov: 2E for preprocessing attempts. For the solver, 4T gives ≤ 1/4 for overrun plus ≤ 1/4
  for failure, so ≤ 1/2 per attempt.
- Aborts after queries are fine. The coupling with the never-abort procedure gives
  P(fail) ≤ P(ideal) + P(abort). Conditioning on any label/coin event keeps the outputs exact
  (line 496).
- The Schedule-1-alone sentence ⌈log₂(3(c−1)/ε)⌉ is correct.

**(c) Arity.**
- A_d(a) := A_{κ_d}(a) (line 705). A_d ≤ B_d holds because candidate (a) is always available,
  and for κ_d = 1 both equal a+1 (line 756).
- thm:main(3) Q_q = c(m+τ)∏A_d(g_d) ≤ c(m+τ)∏B_d ≤ c(m+τ)∏B̄_d (line 189).
- The black-box corollaries keep ∏B_d (lines 924, 952, 975), which are still valid upper bounds.

**(d) Tail (line 758): proved in the text.** It is not just asserted.
- For p ≥ 26244: e^H_odd κ = κ (t = 2), e^H_2 = 2, e^H_4 = 3, e^H_6 = e^H_3+1 = 4,
  e^H_8 = e^H_4+1 = 4.
- So ê = (1,2,3,3,5,4,7,4,9). I checked ê(κ) < ê(d) for every proper divisor κ | d ≤ 9 by hand.
- Σ_{d=2}^9 ê(d) = 37, with equality iff κ_d = d for all d, that is iff 2520 | p−1. So 38.
- The text does **not** claim "depends only on p mod 5040" for the exponent, and does not need it.
  The table does need it (F5).

**(e) Consistency.**
- Abstract (line 60), thm:main(3)/(4) (lines 185–200), line 213, rem:main-solver, §status, the
  Heisenberg and class-3 examples, rem:zero-sum, the table, rem:query-separation(b) and the Outlook
  all agree with each other and with my recomputation.
- The macro `\ReesClassNineHalvedExp` = 38 is used at lines 60, 200, 210, 213, 246, 1110 and 1139.
  The literal "38" appears in lem:halved-exponent (749, 758) and in line 762.
- The status labels next to every occurrence of 38 are honest, apart from F1–F3.

**3. Ivanyos statement.**
- Line 210, "His confirmation covers neither the shorter depth $L_d$ nor the halving", is correct
  and accurate.
- Line 246 is also correct.
- Line 555 lags (F2), and line 1112 is ambiguous (F3).

**4. Leftovers.**
- I grepped the TeX and pdftotext of the PDF for "53" and "determinis". Every remaining "53" is
  labelled "Schedule 1 alone" or sits in lem:exponent.
- Every "deterministic" refers to thm:is-import, lem:rounds/bezout, Schedule 1, lem:zero-sum(iv),
  the p < 4κ′⁴ case of thm:halving(ii), Shor's primality check, or Nayak.
- No statement makes 53 the headline or calls the procedure deterministic.

## 3. Recomputation

My code was written from the TeX definitions before I opened any integrator or attack output.
`s1h_referee.py` works at the coset level: cyclotomic addition tables, exact t by sumsets, exact
T_j, and rule D as written. It covers every prime up to 60000 with no Weil shortcut. Afterwards I
compared only the summary keys of `halved_schedule.json`; they agree.

| c | E_H (mine, rule D, p ≤ 60000) | paper | E_H tail max (residues mod 5040) | E_1 (mine) | paper |
|---|---|---|---|---|---|
| 2 | 3 | 3 | 3 | 5 | 5 |
| 3 | 6 | 6 | 6 | 8 | 8 |
| 4 | 10 (p = 13 only) | 10 | 9 | 16 | 16 |
| 5 | 14 | 14 | 14 | 19 | 19 |
| 6 | 20 (p = 31 only) | 20 | 18 | 35 | 35 |
| 7 | 25 | 25 | 25 | 36 | 36 |
| 8 | 29 | 29 | 29 | 44 | 44 |
| 9 | **38**, at 2521, 7561, 12601, 15121, 20161, 30241, 35281, 42841, 45361, 47881, 55441 (all primes ≡ 1 mod 2520 < 60000) | 38 | 38 at r ∈ {1, 2521} | 53, at 2521, 7561, 12601, 42841, 47881 (≡ 2521 mod 5040) | 53 |

Other checks:
- **Variant rule X** allows multi-stage plans by exact T_s at every p < 30000. It gives the same
  E_H, so the 4κ⁴ restriction costs nothing.
- **Constants:** K_κ ≤ c_κ has 0 violations for p ≤ 60000.
- **Stages:** degree-optimal plans use at most 3 stages.
- **Tail formula:** the exact rule agrees with the residue formula (e^H and A_κ(a) for
  a ∈ {0,1,3,9,17}) on all 1320 primes in [26244, 40000], with 0 mismatches.
- **t ≤ 3** holds at every p ≥ 4κ⁴ up to 60000.

Small values and examples:

| quantity | mine | paper |
|---|---|---|
| A_2(1) (p = 3,5,7,11,13,101,103; and via the Heisenberg row, at all 6053 primes 11..60000) | 4 | 4 |
| A_2(3) | 16 | 16 |
| A_4(2) at p = 5 (plan (2,F1) over A_2(2) = 9) | 243 | 243 |
| κ = 6 at p = 7 | e = 9, plan (3,F0), vs (a) degree 18 | 3 stages, F0 |
| κ = 8 at p = 41 | e = 7, plan (2,F1), vs (a) degree 24 | 2 stages, F1, vs 24 |
| full-depth halving (Outlook) | 95, at p ≡ 1 mod 2520 (p < 30000) and tail | 95 |

Table rows (`table_tail_check.json`; mpmath at 60 digits; Prop. classical-query (i), (v) as
printed):

| row | log₂Q_q | LB > Q from | (v) real threshold, 15 / 8ℓ | copies | paper |
|---|---|---|---|---|---|
| Heisenberg | 5.00 (all p) | 29 | none | 50 | 5.00, 29, none, 50 |
| filiform | 14.83 (p ≡ 1 mod 3) | 863 | 304.49 / 309.14 | 163 | 14.83, 863, 305, 163 |
| free 2-gen | 17.68 | 431 | 195.76 / 197.99 | 221 | 17.68, 431, 196, 221 |
| Dixmier–Lister | 18.91 | 41 | 26.02 / 26.19 | 350 | 18.91, 41, 27, 350 |
| class-9 profile | 314.06 (p ≡ 1 mod 2520; tail max at r ∈ {1, 2521}) | 2^{34.872} | 2^{34.623} | 12,565 | 314.06, 2^{34.87}, 2^{34.62}, 12,565 |

The paper's (v) entries are the ceilings of the real thresholds (305, 196, 27; with 8ℓ: 310, 198,
27). So "for p below" is correct for primes, and the prime lists in the caption are correct.
rem:query-separation(b), "p > 2^{34.8}", is correct (rounded down).

Scripts (all `nice -n 19`, each under 30 s, RSS < 200 MB):
- `s1h_referee.py` → `s1h_referee.json`;
- `table_tail_check.py` → `.json`;
- `weil_T1_check.py` → `.json`;
- `full_depth_95.py` → `.json`.

## 4. Adversarial self-check

- **Did I just confirm the integrator?** My code reads the same Definition, so a misreading shared
  with the integrator would not show up. To guard against that:
  - I re-derived every proof by hand.
  - I checked the T recursion against a brute-force evaluation of T(c) from the definition.
  - I ran a variant rule X.
  - I proved the tail by hand (§2(d)).
  
  My t computation is validated only indirectly: E_1 reproduces 53 and its attainment set, which
  matches lem:exponent's two independent codes.
- **Cost model.** "Arity = product of inner arities" is the one modelling assumption common to
  all three programs. The proof of thm:halving(ii) and the integrator's executor make it concrete.
  I did not run the executor, so it is an untested falsifier for me.
- **Could the min-arity choice break the exponent?** No. thm:halving(iii) bounds A_κ by the arity
  of the degree-optimal candidate, and that candidate's arity uses A_D (min-arity) with induction
  on K_D. I checked K ≤ c_κ by computation (finite; not a proof beyond 26244). The text's
  induction covers p ≥ 26244.
- **Could the Las Vegas solver bias the descent?** The output of prop:descent is the same exact
  state for every nonzero witness, so coins are irrelevant. Aborts are handled by coupling. I see
  no gap. The cut-off needs T explicit (F6), which is routine.
- **What is not covered:**
  - The Weil locator (LN 6.37) is not checked against the book.
  - thm:is-import is an AI reading.
  - lem:rounds is AI-only, and 38 inherits it.
  - Nothing here is human-reviewed.
  - Finite checks only falsify.
- **Weakest point of my own report.** F1's proposed wording records *this* report as the third
  referee. If any fix were judged to need a real repair, its "correct with fixes" would have to be
  revisited.
