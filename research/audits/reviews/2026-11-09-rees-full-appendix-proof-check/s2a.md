# s2a: proof check of the Schedule 2 appendix, lines 1-482

Checker: s2a, 2026-11-09. Paths R, T and O are as defined in `O/BRIEF-COMMON.md`.

## Header

**Scope**

- `T/appendix-schedule2.tex`, lines 1-482. This covers every statement from `lem:app-s2-gcd` to `rem:app-s2-four-cycle`. I also read lines 655-672 (`lem:app-s2-two-rows`), because `prop:app-s2-chebotarev` uses that lemma.
- `T/main.tex`, lines 690-763: the Terms paragraph, `thm:power-sde`, `prop:decoupled-sde` with the definition of E_2(kappa), `rem:two-level-threshold-size` and `rem:combined-schedule`. Lines 161-388 and 572-689 were read for context only (the query count of `thm:main`, Schedule 1, B_d, `eq:sde-target`).
- `T/appendix-provenance.tex`, lines 245-292 (the items the appendix cites), read for consistency only.
- `T/numbers.tex`: `ReesClassNineQueryExp` and the `Psde*` macros.
- Diffs: the hunks of `O/diffs/appendix-schedule2.diff` and `O/diffs/patch9nov-appendix-schedule2.tex.diff` that fall inside lines 1-482.

**Files checked (sha1)**

| file | shasum |
|---|---|
| T/main.tex | 0ed1a1f82b13fef77fc94a48e35efc93f8d23ee4 |
| T/appendix-schedule2.tex | 8abf0e08ebeb059ba862bf7b0c905e38b1ae3624 |
| T/appendix-provenance.tex | 2545e44aeb3ff7f97a204932c46f20ac8c77ec62 |
| T/numbers.tex | c7e587fbc60d3c4a24b95db17c69f8537aefef92 |
| O/diffs/appendix-schedule2.diff | 034b57385bbc93a802f7702bf1799135edf9aa9d |
| O/diffs/patch9nov-appendix-schedule2.tex.diff | 2c00ca3bc1a9215670494ef7d0bb1a41fcbb80b5 |

**Verdict: MINOR ONLY.**

- No theorem, lemma, proposition, corollary or table entry in the range is wrong.
- Theorem `thm:app-s2-main` holds on any columns, as stated.
- There are eight minor findings:
  - finding 1: a false sentence in a proof whose conclusion still holds;
  - finding 2: a definition that does not determine its object;
  - findings 3-8: fixes to wording, scope and quantifiers.

**Answers to the specific tests**

- **`thm:app-s2-main` on any columns.** Yes, it holds, with J = kappa(k+3) and K_j = ceil(2 kappa^{j+1} tau).
  - Worst-case time is bounded: Phase 0 makes a fixed number of draws, and every Phase 1 attempt is cut off.
  - The output is never wrong, because it is checked exactly.
  - The abort probability is at most 0.75 * 2^{-k}.
  - An independent implementation produced 0 wrong outputs in 1110 runs on adversarial columns.
- **Threshold table.** Every entry for kappa = 2..9 was recomputed, at 60 digits and bracketed in interval arithmetic. All agree.
- **T_W and T_A.** Both claims are proved, and every constant was rechecked.
- **Zero entries in E_2 contractions.** They are handled consistently in the appendix and the main text. Independent exact searches reproduce E_2(2..5), both with zero entries allowed and with every entry nonzero.
- **Barrier and Chebotarev propositions.** The quantifiers are right and the scope remarks are honest. Findings 1 and 4 are minor.
- **Main text.** `thm:power-sde`(ii), `prop:decoupled-sde`, the definition of E_2 and `rem:combined-schedule` match the appendix in parameters, thresholds, abort and cost. The worst-case exponents (unchanged for c <= 7; 107 at c = 8; 143 at c = 9) are reproduced, with an exact argument.

**Scripts and compute.** Scripts and outputs are in `O/s2a/`.

- Every Python run used `nice -n 19 timeout <s> /opt/anaconda3/bin/python -I`, single-threaded and one at a time.
- The C search `e2search.c` was compiled with `cc -O2` and also run under `nice` and `timeout`.
- Total compute was under 15 core-minutes.

## Findings

All findings are MINOR. They are listed most substantive first.

### 1. MINOR: barrier proof. "eta_m < 1 forces m <= kappa-2" is false for m > p, and "p >= 7" is not implied

**Location**

- `appendix-schedule2.tex:434` and `:438`, in the proof of `prop:app-s2-barrier`(iii).
- The definition of eta_m, at `:353` (`rem:app-s2-joint-moments`).

**Argument: first sentence**

- eta_m = kappa^m E_kappa(m,p)/(p-m) is defined "for $m \ge 1$".
- The proof shows that eta is nondecreasing and that eta_{kappa-1} > 1, and concludes "So $\eta_m < 1$ forces $m \le \kappa-2$".
- Monotonicity holds only while p - m > 0. For m > p we have eta_m < 0 < 1, yet m > kappa - 2. So the sentence is false.
- Part (iii) quantifies over "every $m \ge 1$ with $\eta_m < 1$", so it includes these m. At m = p, eta_p is undefined.
- The conclusion of (iii) still holds for m > p:
  - binom(rh, m) = 0, because rh <= p-1 < m, so both sides of the bracket are 0;
  - binom(M_S, m) = 0 under L, because every coordinate of L is at most h, the maximum of N.

**Argument: "p >= 7"**

- The merge estimate uses "$p \ge 7$". The hypotheses (kappa >= 3, p = 1 mod kappa, p <= kappa^kappa/2) do not imply it: kappa = 4, p = 5 is allowed.
- The estimate is still valid:
  - a merge needs some m' >= 2 with eta_{m'} < 1, hence eta_2 < 1 by monotonicity;
  - since kappa^2 E_kappa(2,p) >= (kappa-1)^2 sqrt p, eta_2 < 1 forces p > (kappa-1)^4 >= 16;
  - the bound is then (9/16)(4/9) 16^{-3/2} < 0.004 <= 0.02.

**Finite checks (no counterexample)**

- `O/s2a/barrier.py` checks the brackets on the exact law and on L at 16 pairs (kappa, p). These include the m = 2 merges at (4,97), (4,101), (4,109) and (4,113).
- `O/s2a/extra_checks.py`:
  - eta_{kappa-1} > 1 for every p <= kappa^kappa/2, kappa = 3..10;
  - the least p with eta_2 < 1 lies just above (kappa-1)^4: 97, 281, 661, 1373, 2441, 4159 and 6661 for kappa = 4..10.

**Fix**

- At line 353, replace `for $m \ge 1$ put` with `for $1 \le m < p$ put`.
- At line 438, replace `and $p \ge 7$` with `and $p > (\kappa-1)^4 \ge 16$ (since $\eta_2 \le \eta_{m'} < 1$ and $\kappa^2E_\kappa(2,p) \ge (\kappa-1)^2\sqrt p$)`.

### 2. MINOR: the character chi is not determined by chi(xi) = omega

**Location.** `appendix-schedule2.tex:115` (`app:s2-weil`, just before `eq:app-s2-indicator`).

**Argument**

- xi is only a coset generator: its image generates F_p^x/Q_0. It need not generate F_p^x.
- Then several characters take the value omega at xi, and not all of them are trivial on Q_0 or of order kappa.
- Example: p = 13, kappa = 2, xi = 8. Here 8 is a non-square of order 4, and 2 is a primitive root.
  - With psi(2) = e^{2 pi i/12}, the characters psi^t with psi^t(8) = -1 are t in {2, 6, 10}.
  - psi^2 and psi^10 have order 6.
  - For these two, "it has order exactly $\kappa$" is false, and so is the indicator formula `eq:app-s2-indicator`.
- The intended chi, the one trivial on Q_0, is unique, and everything downstream is correct for it. My scripts use that chi.

**Fix.** Replace `Let $\chi$ be the multiplicative character of $\Fp^\times$ with $\chi(\xi) = e^{2\pi i/\kappa} \eqqcolon \omega$;` with:

`Let $\chi$ be the multiplicative character of $\Fp^\times$ that is trivial on $Q_0$ and has $\chi(\xi) = e^{2\pi i/\kappa} \eqqcolon \omega$ (it exists and is unique, since the image of $\xi$ generates $\Fp^\times/Q_0 \cong \mathbb{Z}_\kappa$);`

### 3. MINOR: the status line overclaims "exact checks of every claim"

**Location.** `appendix-schedule2.tex:11`. This sentence is new in the 9 Nov prep (`appendix-schedule2.diff`, hunk `@@ -1,88 +1,14 @@`); the old text cited source notes instead.

**Argument**

- The theorems of the appendix are general in p, kappa and a. Finite computations can test them, but they cannot check them exactly.
- Some items in the range are explicitly argued or conditional:
  - `rem:app-s2-joint-moments` says "the argument is only sketched here";
  - the central-moment bound it cites is "not proved here".
- The sentence conflicts with the project rule that finite checks only falsify.

**Fix.** Replace `Exact checks of every claim of this appendix are recorded in Appendix~\ref{app:provenance}, items~\ref{prov:s2-main}--\ref{prov:s2-scope}.` with:

`The provenance of the claims of this appendix, and the finite computations that test them, are recorded in Appendix~\ref{app:provenance}, items~\ref{prov:s2-main}--\ref{prov:s2-scope}.`

### 4. MINOR: the main text states the barrier for "the same" brackets, without the restriction eta_m < 1

**Location.** `main.tex:726`, `rem:two-level-threshold-size`.

**Argument**

- `prop:app-s2-barrier`(iii) gives the brackets only for m with eta_m < 1.
- `rem:app-s2-barrier-scope` (appendix line 449) says the proposition "says nothing about ... the one-sided upper brackets with $\eta_m \ge 1$".
- The main text says the explicit law "satisfies the same Weil-controlled moment brackets". That reads as all of them, which is broader than what is proved.

**Fix.** Replace `satisfies the same Weil-controlled moment brackets` with:

`satisfies the same two-sided Weil-controlled moment brackets (those with $\eta_m < 1$ in Remark~\ref{rem:app-s2-joint-moments})`

### 5. MINOR: the main-text Terms paragraph omits the Bezout step

**Location.** `main.tex:695`, the Terms paragraph before `thm:power-sde`.

**Argument**

- `lem:app-s2-witness` gives u != 0 with sum_b u_b^kappa lambda_b = 0. It does not give sum_b s_b^d lambda_b = 0.
- For d != kappa, the Bezout exponent of `lem:app-s2-gcd`(b) is also needed, as in the proof of `thm:app-s2-main`.

**Fix.** Replace `turns any array into a solution of~\eqref{eq:sde-target} (Lemma~\ref{lem:app-s2-witness})` with:

`turns any array into a nonzero $u$ with $\sum_b u_b^\kappa\lambda_b = 0$ (Lemma~\ref{lem:app-s2-witness}), and a Bezout exponent turns $u$ into a solution of~\eqref{eq:sde-target} (Lemma~\ref{lem:app-s2-gcd})`

### 6. MINOR: the Phase 1 cut-off needs an explicit T_1

**Location.** `appendix-schedule2.tex:189`, in the proof of `thm:app-s2-main`, under "Abort probability".

**Argument**

- The text says "Let $T_1$ be an upper bound on its expected running time. Run it with a cut-off at $2T_1$ steps".
- To impose this cut-off, the algorithm must compute T_1. So T_1 must be an explicit function of the input, not merely a bound that exists.
- The cost paragraph ("$T_1 = \poly(a,\kappa,\log p)$", plus the root extractions) supplies this in substance. The wording should say it.

**Fix.** Replace `Let $T_1$ be an upper bound on its expected running time.` with:

`Let $T_1 = T_1(a,\kappa,\log p)$ be an explicit polynomial upper bound on its expected running time (Lemma~\ref{lem:app-s2-tensor} and the root extractions), so that the algorithm can compute it.`

### 7. MINOR: tau is not quantified in Prop. TW(ii)

**Location.** `appendix-schedule2.tex:215`, `prop:app-s2-TW`(ii).

**Argument**

- tau is defined only inside the description of Phase 0, which comes earlier and is a separate context.
- Statement (ii) holds for every tau > 0.
- "except with probability $e^{-\tau}$" should read "at most".

**Fix.** Replace `so $\lceil 2\kappa^\kappa\tau\rceil$ uniform draws find some $\alpha_j \in X_j$ except with probability $e^{-\tau}$.` with:

`so, for every $\tau > 0$, $\lceil 2\kappa^\kappa\tau\rceil$ uniform draws find some $\alpha_j \in X_j$ except with probability at most $e^{-\tau}$.`

The same wording recurs at line 557, outside my range; I did not check it there.

### 8. MINOR: a >= 1 versus grades with g_d = 0

**Location**

- `appendix-schedule2.tex:13` and `thm:app-s2-main` (line 157, "Let $a \ge 1$").
- `main.tex:167` ("class at most $c$") and `main.tex:192` (g_d = dim gamma_d(L)).

**Argument**

- Because the class is only bounded by c, g_d = 0 can occur for some d <= c. The combined rule (`main.tex:759`) then sets M_d = 1.
- The appendix assumes a >= 1.
- The case is trivial: for a = 0, s = (1) solves the target, and the algorithm works unchanged.
- I did not check whether the recursion of `sec:recursion` skips such grades.

**Fix.** Either write `with $a \ge 0$ (for $a = 0$ every nonzero $s$ is a solution)` at line 13 and in `thm:app-s2-main`, or add a sentence to the main text saying that grades with $g_d = 0$ are skipped.

## Checked and correct

For each line below, I read the proof and found no gap. Where finite checks are listed, they found no counterexample. Finite checks only falsify; none of them is offered as a proof.

- **`lem:app-s2-gcd`(a, b).**
  - The kappa-th and d-th powers coincide.
  - s_b = u_b^t with t d' = 1 mod q' gives s_b^d = u_b^kappa.
  - Exercised at d = 4 and 6 (kappa = 2) and at d = 9 (kappa = 3) in `schedule2_run.py`.
- **`lem:app-s2-tensor`.**
  - The arity (a+1)((kappa-1)a+1) is exactly what the two dependences need.
  - The cells are disjoint, and b* lies in S_0^{nu*}, which lies in S_00.
  - Every coordinate of T_ij lies in W (x) W.
  - All of this is asserted on every run of `schedule2_run.py`.
- **Two-level contraction and the choice of xi.**
  - The definition allows zero entries and requires C_00 != 0.
  - Independence from the choice of xi (the P1 text) is proved correctly.
  - The e2search verdicts are the same for other coset generators (`e2_k4_xi3.out`, `e2_k5_xi.out`).
- **`lem:app-s2-witness`.**
  - Correct also when some C_ij = 0: that cell gets weight 0, and u != 0 because C_00 != 0 and b* lies in S_00.
  - 1486 search witnesses were verified by a separate script (`verify_witnesses.py`).
- **`lem:app-s2-normal`.** The normal form C_ij = z_i z_j (alpha_j + beta_i) and the normalisation alpha_0 = 1, beta_0 = 0 are correct.
- **`lem:app-s2-weil-count` and `eq:app-s2-error`.**
  - The closed form of E_kappa(l,p) is reproduced exactly for kappa = 2..12 and l <= 3 kappa.
  - On 2500 random instances, the worst |N - main term|/E is 0.71 (`exact_checks.py`).
- **`thm:app-s2-main`, on any columns.**
  - Worst-case time is bounded:
    - Phase 0 makes at most J + sum K_j <= kappa(k+4) + 4 tau kappa^kappa draws, each costing at most kappa coset tests;
    - Phase 1 is cut off at 2T_1 and runs at most k+1 times.
  - The output is never wrong, because it is checked exactly before output.
  - The abort probability is at most 2^{-k-3} + 2^{-k-3} + 2^{-k-1} = 0.75 * 2^{-k}. J = kappa(k+3), K_j = ceil(2 kappa^{j+1} tau) and tau = k+3+ceil(log2 kappa) give the two 2^{-k-3} terms.
  - The cost is (1+kappa^kappa) poly.
  - An independent implementation (`schedule2_run.py`) made 1110 runs:
    - eight column families: random, zero, repeated, e_1, rank one, sparse, basis pattern and entries in {0, +-1};
    - kappa = 2, 3, 4 and 6, with p at 4 kappa^{2kappa+2} and at 16 kappa^{2kappa+2}, and with d in {4, 6, 9} different from kappa;
    - result: 0 wrong outputs and 2 xi-search aborts at k = 1 (expected about 2.25).
- **`lem:app-s2-stage`.**
  - Every step of the chain to Lambda >= p/(2 kappa^l) at p >= 4 kappa^{2kappa+2} is correct.
  - The measured Lambda * 2 kappa^l / p is at least 1.87 for kappa = 2, 3, 4 (`exact_checks.py`, item (6)).
- **Correctness of Phase 0.** Accepted t_j are nonzero and distinct. This is enforced, and it is also forced: t_j = t_i would put xi^{j-i} in Q_0.
- **`rem:app-s2-four`.**
  - p >= 4 kappa^{2kappa+2} suffices.
  - The 9 Nov change says the recursion runs Phase 0 inside every attempt, at a cost of one Phase 0 per attempt. This is consistent with the theorem and with the main-text recursion (k = 2, Phase 0 inside each attempt).
- **`prop:app-s2-TW` and the paragraph after it (the P3 text).**
  - The T_W formula and parts (i) and (ii) are correct; T_W(2) = ((1+sqrt 17)/2)^2 = 6.5616.
  - For kappa <= 9, 16 kappa^{2kappa+2}/T_W >= 26.
  - Parts (i) and (ii) were checked at 2546 (p, xi) pairs above T_W, for kappa = 2, 3, 4, with no failure.
- **`lem:app-s2-moments`.** E[n_j] and E[n_j^2] were reproduced by brute force at 10 pairs (p, kappa).
- **`lem:app-s2-cyclo`.** The bound on |kappa^2 m_b - (p-kappa-1)| holds at 2070 primes. The worst deviation equals the bound, so the bound is tight.
- **`prop:app-s2-TA`.**
  - (i) R <= U_kappa(p) at 1493 primes with Delta <= 1/2; the smallest margin is 0.001.
  - (ii) T_A > (kappa-1) kappa^kappa for kappa = 2..40, and T_A <= kappa^{kappa+1} for kappa = 3..40.
  - (ii) The point values at kappa = 3, 4, 5 are reproduced:
    - Delta(81) = 0.2857 and U_3 = 1.48419;
    - Delta(1024) = 0.1943 and U_4 = 1.27937;
    - Delta(15625) = 0.0965 and U_5 = 1.20238;
    - the margins are 0.0158, 0.0540 and 0.0476.
  - (ii) Every constant of the kappa >= 6 chain holds for kappa = 6..200 at 700 digits (`k6check.py`).
  - (iii) The Chebyshev step and (p/h)^kappa <= e kappa^kappa are correct. A round succeeds with probability at least 3/8; empirically, 0.96-0.99.
- **`tab:app-s2-thresholds`.**
  - Every entry of rows kappa = 2..9 was recomputed at 60 digits by bisection. T_A and T_S were bracketed in interval arithmetic at a relative distance of 10^-12.
  - All agree with the printed values, including:
    - T_A(3) = 79.0394;
    - T_A(7) = 4941830.3, below 5*10^6;
    - ceil(T_A(8)) = 117441563;
    - T_S/kappa^{kappa+1} <= 9.08 at kappa = 3 and <= 8.40 for 4 <= kappa <= 40.
  - Script: `thresholds.py`.
- **`cor:app-s2-decoupled`.**
  - The abort budget is correct: 2^{-k-3} for xi, plus 2^{-k-3} for the rounds (r = ceil((k+3)/log2(8/5))), plus 2^{-k-1} for Phase 1, which is below 2^{-k}.
  - The cost is O(kappa^{kappa+1} log kappa) draws per round.
- **`cor:app-s2-small` and the E_2 data.** I ran an independent exhaustive DFS (`e2search.c`), with zero entries allowed and no symmetry breaking. It gives:
  - E_2(2) = {} for p <= 400;
  - E_2(3) = {} for p <= 3000;
  - E_2(4) = {5,13,17,29,37,53}, over every p = 1 mod 4 below T_A(4) = 869.0;
  - E_2(5) = {11,31,41,61,71,101,131,151,181}, over every p = 1 mod 5 below T_A(5) = 12657.6.
  - With every entry nonzero, the sets gain {3}, {7,13}, {61} and {191,211,241,251} respectively, as the text says.
  - The symmetric form fails at kappa = 3 exactly at {7, 13, 19, 61} below 400.
- **Zero entries.**
  - They are treated consistently in the definition (entries in Q_0 u {0}), in `lem:app-s2-witness`, in `cor:app-s2-small`, in the scope list, and in main.tex lines 695 and 716.
  - Props TW and TA and Phase 0 construct contractions with all entries nonzero, which is stronger.
- **`lem:app-s2-kwise`.** The law, its (kappa-1)-wise marginals and the converse were checked exactly in rationals for kappa = 2..8 (`barrier.py`).
- **`prop:app-s2-barrier`.**
  - (i) and (ii) were verified on the explicit L at (3, 7).
  - (iii) The brackets were checked for L and for the true law at 16 pairs (kappa, p).
  - The quantifiers are right: "does not imply" is a statement about the set of statements, and L is a model of that set.
  - Every constant of the proof was re-derived: the differences of c_m and d_m, the merging inequality, 13/36, 0.02 and 0.4. The only exception is finding 1.
- **`rem:app-s2-barrier-scope`.** Honest. It names the one-sided upper brackets with eta_m >= 1, and E prod n_j, as outside the proposition. It also says that the converse of `lem:app-s2-kwise` does not make any certificate work.
- **`prop:app-s2-chebotarev`.**
  - The quantifiers are right: every coset generator, every lambda, every sigma and tau.
  - The cases p | kappa and p = 2 with kappa = 2 kappa' are handled.
  - Row 0 needs kappa - 1 >= 2 zero cells, which `lem:app-s2-two-rows` excludes.
  - Chebotarev for the Galois closure gives density 1/[L~:Q].
  - `lem:app-s2-two-rows` (lines 655-672) was read and is correct.
- **`rem:app-s2-chebotarev-scope`.** Honest. p = 196681 is prime, and every u with 1 <= |u| <= 16 is a fourth power mod p (verified).
- **`rem:app-s2-four-cycle`.**
  - The formulas for S_e were brute-forced on 190 tuples at (3,7), (3,13), (4,13), (5,11) and (6,13).
  - The vanishing claims were tested on 40 random e at (3,7).
  - The total bound binom(kappa,2)^2 (kappa-1)^3 p^{2kappa-1} < kappa^7 p^{2kappa-1}/4 is correct.
- **main.tex, `thm:power-sde`.**
  - (i) is correct.
  - (ii) has the same parameters as `thm:app-s2-main`: p >= 16 kappa^{2kappa+2}, M = (a+1)((kappa-1)a+1), abort at most 2^{-k}, checked output, and cost (1+kappa^kappa) poly.
  - (iii) The example is correct:
    - the 8 columns at p = 5, d = 4, a = 2 have no nonempty zero-sum subset;
    - D(C_5^2) = 9;
    - B_4(2) = 331776^3, about 3.65*10^16.
- **main.tex, the paragraph after `thm:power-sde`.**
  - The 4 kappa^{2kappa+2} remark is correct.
  - So is the product bound: prod M_d <= (c-1)! [(r+1)!/(r-c+2)!]^2 <= r! ((r+1)!)^2.
  - So is the claim that p >= 16 c^{2c+2} covers every grade.
  - The `Psde*` arities in numbers.tex match (a+1)((kappa-1)a+1).
- **main.tex, `prop:decoupled-sde` and the definition of E_2(kappa).**
  - They match `cor:app-s2-decoupled` and `lem:app-s2-normal`.
  - "kappa >= 3 and p >= kappa^{kappa+1}" follows from TA(ii).
  - The T_S bounds (<= 10 kappa^{kappa+1}, and <= 9 kappa^{kappa+1} for kappa >= 4, for 3 <= kappa <= 40) are reproduced.
  - E_2(2..5) are as quoted.
- **main.tex, `rem:combined-schedule`: the worst-case exponent.** The claims are exact: unchanged for c <= 7, falling by 2 for c = 8 (109 to 107) and for c = 9 (145 to 143).
  - Reason:
    - the value 145 needs kappa_d = d for every d <= 9, that is 2520 | p-1;
    - hence p >= 2521 > 1024 = 16 * 2^6, where grade 2 switches to Schedule 2 (exponent 2 instead of 4);
    - every other deviation from Schedule 1 at kappa_d = d costs at least 5;
    - 143 is attained at p = 2521;
    - for c = 8 the same argument applies, since lcm(2..8) = 840 and the first prime = 1 mod 840 is 2521;
    - for c = 7, p = 421 < 1024 keeps every grade on Schedule 1.
  - Finite confirmation over primes below 2*10^5: `ew_check.py`.
- **Diffs in range.**
  - Most changes are editorial: source notes replaced by provenance items, "passes" changed to "succeeds", and the reordered inclusion of b* in S_0^{nu*} and S_00.
  - The two changes of substance are the `rem:app-s2-four` change (checked above) and the new status sentence (finding 3).

## Not checked / UNKNOWN

- **`rem:app-s2-joint-moments`.** I did not reconstruct the following; they are sketched and conditional. Only the bracket itself was checked.
  - the Bonferroni lower bound F;
  - F > 0 for 6 <= Lambda <= sqrt(8 kappa) when kappa >= 729;
  - the thresholds 6 kappa^kappa + 1 (kappa >= 729) and 5.5 kappa^kappa + 1 (kappa >= 1677);
  - "F not positive on a fine grid for kappa <= 27".
- **The central-moment bound of `rem:two-level-threshold-size`** (4e ceil(ln 4 kappa)^2 kappa^kappa + 1 for kappa >= 32, improving on T_A for kappa >= 15). It is argued in the paper; I did not check it.
- **E_2 data for kappa >= 6.** Not checked, because the brief forbids searches for kappa >= 6:
  - E_2(6) and E_2(7);
  - the kappa = 8 and 9 decided ranges, the separate runs and the explicit-contraction intervals in `prop:decoupled-sde`;
  - the "1.7 kappa^{(kappa+1)/2}" sentence of `rem:two-level-threshold-size`, which rests on these data.
- **Sources not opened:**
  - Lidl-Niederreiter Thm 5.41 (the Weil bound for products of multiplicative characters);
  - the expected cost of Las Vegas kappa-th roots;
  - Benjamini-Gurel-Gurevich-Peled, Prop. 26;
  - Olson 1969;
  - |J(psi, psi')| = sqrt p, which the .tex itself marks NEEDS HUMAN VERIFICATION.
- **main.tex, the block-steered option (G1-G3) and `prop:triangular-sde`.** Read, but not checked in depth; neither is among the listed statements.
- **Grades with g_d = 0.** I did not check whether `sec:recursion` skips them (finding 8).
- **Outside my range:** appendix lines 483-654 and 673 onward (tower, chains, local obstructions, scope list). Line 557 is the one mentioned in finding 7.

## For the human expert

1. **The Weil bound** (|sum psi(f)| <= (s-1) sqrt p, for a product of characters at s distinct roots; Lidl-Niederreiter Thm 5.41), as used in `lem:app-s2-weil-count`.
   - It is the one analytic input behind `thm:app-s2-main` and Props TW and TA.
   - The closed form E_kappa(l,p) is correct given it.
2. **The second-moment chain of `prop:app-s2-TA`(i):**
   - the Jacobi-sum bound |K(s,t)| <= sqrt p in `lem:app-s2-cyclo`;
   - the passage from Delta to U_kappa through E_max (u_Delta, v_Delta).
   - Every numeric check passes, but the algebra deserves one human read.
3. **`prop:app-s2-chebotarev`:** complete splitting, residue fields and Chebotarev density for the Galois closure. Also |J| = sqrt p in `rem:app-s2-four-cycle`.
4. **The model in `prop:app-s2-barrier`.**
   - The barrier covers proofs that use only statements involving at most kappa-1 of the n_j, together with the two-sided brackets.
   - It excludes E prod n_j and the upper brackets with eta_m >= 1, as the scope remark says.
   - Whether this class captures the methods one would naturally try is a judgement for the reader.
5. **The joint-moment and central-moment claims** in the Not checked list are the only parts of this range that are argued rather than proved.

## Comparison with the earlier report(s)

I read `R/research/audits/reviews/2026-11-03-rees-check-app-a.md` (sha1 e0bd915e8a627d45bb4e77072aeea8df8105e567) after my own pass.

- **Verdict.** Its verdict was "sound", with gaps G1-G3, a definition point D1 and nits N1-N5. It agrees with mine on the core: no error from `lem:app-s2-gcd` to `cor:app-s2-small`, or in the table.
- **Proposed texts P1-P8.** All eight are in the current tree, and I checked each one against it:
  - P1: the argument for every coset generator;
  - P2: r = ceil((k+3)/log2(8/5));
  - P3: the cost band above T_W;
  - P4: the zero-entry sentences;
  - P5: the Bernoulli step;
  - P6: "by (ii)";
  - P7: the main text now says (p, kappa) and xi;
  - P8: Phi removed.
  - So G1-G3 are closed.
- **N3** (O(log d) to reduce d mod p-1 for the Bezout exponent) was not adopted, as that report advised. It is irrelevant, since d <= c.
- **D1.** My nonzero-entry results agree with it exactly: {3}, {7, 13}, {61} and {191, 211, 241, 251}.
- **Coverage.**
  - That report predates the 5 Nov barrier, Chebotarev and four-cycle material and the 9 Nov status line. Findings 1, 3 and 4 concern text it did not see.
  - Findings 2 and 5-8 concern text it did see, but it did not raise them.
  - It ran an E_2(6) spot check; I did not, because the brief forbids searches for kappa >= 6.

## Scripts (`O/s2a/`)

- `thresholds.py` -> `thresholds.out`: the table, TA(ii), the point values and interval brackets. The kappa >= 6 "violations" printed there are artefacts of 60-digit precision; `k6check.py` redoes that chain at 700 digits and finds none.
- `k6check.py` -> `k6check.out`
- `exact_checks.py` -> `exact_checks.out`: E closed form, Weil count, moments, cyclo, R <= U, TW, stage count.
- `schedule2_run.py` -> `schedule2_run.out`: independent implementation of `thm:app-s2-main`.
- `e2search.c` (binary `e2search`) -> `e2_k*_*.out`: exact contraction search.
- `verify_witnesses.py` -> `verify_witnesses.out`
- `barrier.py` -> `barrier.out`: lemma kwise, barrier brackets, four-cycle sums, p = 196681.
- `extra_checks.py` -> `extra_checks.out`: eta ranges and the sampler rate.
- `ew_check.py` -> `ew_check.out`: worst-case exponents of the combined rule.
