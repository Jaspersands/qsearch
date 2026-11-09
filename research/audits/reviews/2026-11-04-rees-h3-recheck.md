# Rees HSP: independent recheck of the (H3) discharge

4 November 2026. Independent AI referee pass. **AI-checked, pending human review.**

Scope:
* `docs/papers/rees-hsp/appendix-torsion-blackbox.tex`: prop:tb-count-gates (line 1238, the (H3) paragraph on lines 1239-1269, item (c), proof (c) on lines 1314-1318, the exponents on lines 1326-1329) and lem:tb-sylow (lines 556-635, part (d) on lines 598-635).
* `docs/papers/rees-hsp/main.tex`: thm:bb-envelope (line 1017), item (iii) (line 1031), the status paragraph (line 1034), and lem:qft-mod (line 725), step E.
* `research/STATE.md`, Rees lines, for context only.

Ground rules: no .tex edited, no git, no network. Scratch scripts are in the session scratchpad:
* `/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/h3num.py` checks the constants, Chernoff, Jordan totient and lcm.
* `/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/6a6cfdd7-c9d4-4169-9805-7e18625bbdd7/scratchpad/pe.py` simulates the exact order-finding distribution.

I ran `research/audits/reviews/2026-11-04-rees-h3-check/modexp_check.py` with `/opt/anaconda3/bin/python`. It passed, and its output matches the bounds in the text. I judged the text independently first. The earlier review was read only after this pass (last section).

## Verdict

**The (H3) discharge is sound in substance, but its error budget is wrong over a finite gate set.**

* Every count I re-derived matches:
  * 80n²+27n per controlled multiplication;
  * 7n+6 qubits;
  * 160n³+O(n²) per run;
  * 4ℓ+2 oracle multiplications.
* The probability chain checks, and so do T and the Chernoff step. The Miller-type splitting step is correct.
* **One genuine error.** Over a fixed finite gate set, the synthesis error is not included in the 1/200 per pair. With both errors counted, the loss per pair is 1/100, and (4/π²)²·6/π² − 1/100 = 0.0899 < 1/11. The fix is to halve both budgets, and the asymptotics are unchanged.
* **The c = 1 total-time exponent is false as written.** This error was already there before this pass.
* The classical time of the preprocessing is under-itemized: only the AKS part is listed. This is harmless to the exponents.

Counts: **Errors 2, Gaps 2, Imprecisions 4, Style 2.**

## Recomputations

### 1. Gates and qubits

I counted from `theorems/rees_circuit_arith.py` (the `cuccaro_add`, `mod_add_reg` and `const_mul_acc` blocks):

| block | count |
|---|---|
| Cuccaro adder, n bits (`add_ext`) | 3n + 1 + 3n = 6n+1 |
| `sub_ext` | 6n+1 + 2(n+1) = 8n+3 |
| modular addition `mod_add_reg` | 3(6n+1) + 2(8n+3) + 4 loads of ≤ n + 3 CNOT/X = **38n+12** |
| one shift-and-add step | 2 controlled loads (≤ n each) + 38n+12 = 40n+12 |
| one pass (n steps) | 40n²+12n |
| controlled multiplication | 2 passes + 3n (controlled swap) = **80n²+27n** |
| one run | (2n+1)(80n²+27n) + (2n+1)(r+2) + 1 = **160n³+134n²+27n + (2n+1)(r+2) + 1** |
| qubits | (2n+1) + n + n + (3n+5) = **7n+6** |

* The transform term (2n+1)(r+2) is a valid upper bound. It covers:
  * t initial H gates;
  * t H gates in the inverse transform;
  * Σ_{k=2}^{min(r,t)}(t−k+1) ≤ t(r−1) gates CR_k^{-1}.

  That totals ≤ t(r+1). The final +1 is the X that sets |1⟩.
* All gates have at most two controls. The guarded loads are Toffolis on (guard, x_i). So the gate set {X, CNOT, SWAP, Toffoli} is respected.
* The construction x ← x+... is correct:
  1. y ← y + κx.
  2. x ← x − κ⁻¹y, the inverse of a bijection on canonical inputs, so x becomes 0.
  3. Swap.

  With control 0, every step is the identity.
* `modexp_check.py` gave:
  * all 13 odd moduli exhaustive and correct, with clean ancillas. The maximum count is ≤ 80b²+27b in every case, e.g. 3018 ≤ 3042 at F = 63;
  * the four full exponentiations correct;
  * the bound respected at b up to 32.
* Black box: 2ℓ+1 forward plus 2ℓ+1 backward out-of-place multiplications, so 4ℓ+2.
  * The "further gates" are controlled loads of ℓ-bit constants (O(ℓ) per step), the copy-out and the transform: O(ℓ²) in all. Encodings are ℓ-bit (line 537), so no w-dependence enters.

### 2. Probability chain

* **Exact per-k bound.** Phase estimation per eigenvector gives P(best t-bit approximation) ≥ 4/π². This holds exactly, not asymptotically, so each k has probability ≥ 4/(π² o_i).
  * With t = 2ℓ+1 and o_i ≤ 2^ℓ: |b/2^t − k/o_i| ≤ 2^{−2ℓ−2} < 1/(2o_i²). So k/o_i is a convergent (Hardy–Wright Thm 184).
  * It is the last convergent with denominator ≤ 2^ℓ. Two such fractions differ by ≥ 2^{−2ℓ}, while consecutive convergents here would be within 2^{−2ℓ−1} of each other.
  * Simulated exactly for ℓ ≤ 5 and all o ≤ 2^ℓ (`pe.py`): min P(k/o)·o·π²/4 = 2.02 ≥ 1.
* **lcm step.** lcm(o/gcd(k₁,o), o/gcd(k₂,o)) = o/gcd(k₁,k₂,o). Verified exhaustively for o < 60.
* **Pair bound.** Pr[gcd(k₁,k₂,o)=1] under the uniform law is J₂(o)/o² = ∏_{q|o}(1−q⁻²) ≥ 1/ζ(2) = 6/π². Verified.
  * The actual law is pointwise ≥ (4/π²)·uniform, so the exact pair succeeds with probability ≥ (4/π²)²∏(1−q⁻²).
* **Numerically:** (4/π²)²·6/π² = 0.099856; minus 1/200 = 0.094856 > 1/11 = 0.090909, a margin of 0.0039.
  * With 1/100 instead (see E1): 0.089856 < 1/11.
* **Pair loop.** (10/11)^{⌈11 ln(2s/ε)⌉} ≤ e^{−ln(2s/ε)} = ε/(2s). ✓
* **Splitting step.**
  * The probability ≥ 1/22 = (1/2)(1/11) holds for every history: a non-unit a splits F, and for each unit a the pair bound holds.
  * The bound "≥ 1/2 that r is even and a^{r/2} ≢ −1" is Shor's 1 − 2^{1−k} with k ≥ 2 distinct odd primes. F is not a perfect power, so k ≥ 2.
  * The last-non-1-term argument is correct for any multiple u of r. If r = 2^{j'}r′, then x = (a^{r/2})^{m/r′} = a^{r/2}, because m/r′ is odd and (a^{r/2})² = 1.
* **T and Chernoff.** μ = T/22 ≥ 4ℓ + 8 ln(2s/ε), so μ/2 ≥ 2ℓ and e^{−μ/8} ≤ ε/(2s).
  * The form used is the multiplicative lower tail Pr[X ≤ (1−δ)μ] ≤ e^{−δ²μ/2} with δ = 1/2.
  * An incomplete factorization means at most 2ℓ−2 < μ/2 successes.
  * It applies through stochastic domination. Attempts are not independent (which F gets attacked depends on the history), but each succeeds with conditional probability ≥ 1/22 whatever the history, which is enough by a standard coupling. The text states the condition ("whatever happened before") but not the coupling (I3).
  * Exact binomial tails over a grid of (ℓ, s, ε) are at most 2·10⁻⁵ times ε/(2s).
* **Union.** ε/(2s) + ε/(2s) per generator, over s generators, gives ε_pre. ✓

### 3. Approximation error

* r = ⌈log₂(800πt)⌉ gives 2^r ≥ 800πt, so 2πt·2^{−r} ≤ 1/400.
* The bound ε_aq = Σ_{k>r}(t−k+1)·2 sin(π/2^k) ≤ 2πt·2^{−r} is right. I recomputed it exactly for t up to 8193: for example 0.00152 ≤ 0.00153 at t = 2049.
* From operator norm to total variation: ‖(U′−U)⊗I‖ ≤ δ. The trace distance of the pure states is √(1−|⟨ψ|φ⟩|²) ≤ ‖ψ−φ‖ ≤ δ, and measurement and classical post-processing do not increase it. So TV ≤ 1/400 per run, and ≤ 1/200 per pair (TV of products is subadditive).
* **This is justified for the truncation alone.** It is not justified once gate synthesis is added (E1).

### 4. Citations

| citation | used for | assessment |
|---|---|---|
| Shor1997 §5 | reduction of factoring to order finding; probability ≥ 1 − 2^{1−k} ≥ 1/2 | Correct: the SIAM numbering has §5 "Prime factorization". At line 603 the 4/π² is attributed to Shor through the arXiv id. Shor's own bound is the asymptotic 1/(3r²) per state; 4/π² is CEMM's (I2). |
| CEMM 1998 §§5–6 | exact 4/π² phase-estimation bound and its use in order finding | The content is right. I cannot verify the section numbers offline. The earlier review reports checking them. |
| AKS2004 Thm 5.3 | Õ(log^{15/2} n) per primality test | **The stakes are high.** With only the Õ(log^{21/2} n) bound, the certificates cost s·ℓ^{23/2}, which exceeds N⁹ at c = 2 and breaks the stated time exponent. I first recalled Thm 5.3 as the 21/2 bound. On reflection the Annals numbering is Thm 5.1 (21/2), Lemma 5.2 (Fouvry; Baker–Harman), Thm 5.3 (15/2). This agrees with the earlier review, which reports checking the Annals text. A human should confirm the number. Lenstra–Pomerance (Õ(log⁶ n)) would be a safe alternative. No finding is raised. |
| Hardy–Wright Thm 184 | \|x − p/q\| < 1/(2q²) ⇒ p/q is a convergent | Correct; the numbering is unchanged in the 6th edition. |
| VBE1996 §IV | "on 7n+6 qubits, as in" | The architecture matches. As I recall, VBE's own count is 7n+1, so "as in" overstates the match (I4, low confidence). |
| DawsonNielsen2006 | polylog synthesis | Correct. |

### 5. Totals and exponents

* s ℓ⁴ = (sℓ)ℓ³ ≤ N⁴. ✓
* s ℓ³ log(s/ε) ≤ N⁴ needs a separate step. Since log₂ s ≤ s ≤ sℓ, log(s/ε) ≤ N; and sℓ³ ≤ (sℓ)ℓ² ≤ N³. So 2N⁴ is right, but the parenthetical only shows the first half (S2).
* AKS: at most 4ℓ−1 entries are tested, since a binary splitting tree has ≤ 2ℓ leaves. Each test is on ≤ 2ℓ bits, so the cost is Õ(sℓ^{17/2}) ≤ N^{17/2+o(1)} < N⁹. ✓
* E_W(c) ≥ c, since every e_d ≥ 1. E_W(2) = 1 + 2·⌈log₂3⌉ = 5. So E_W(c) + 4 ≥ 9 for c ≥ 2, and the time exponent E_W+1+max(3,β̂) ≥ E_W+4 ≥ 9 covers both N^{17/2+o(1)} and N^{max(c,6)}. ✓
* **c = 1:** E_W(1) = 1 and no solver is called, so the claimed time exponent is 2 + 3 = 5. But the charts alone cost ℓ⁶ and AKS costs N^{17/2}. See E2.

### 6. Claim hygiene

* Nothing in the (H3) paragraph, lem:tb-sylow, thm:bb-envelope(iii) or the status paragraph says that a coherent receiver is implemented or that a speedup exists.
* "AI-checked, pending human review" appears:
  * at line 1239, for (H2);
  * at lines 1268-1269, for (H3);
  * in the main.tex status paragraph (line 1034);
  * in the title of lem:qft-mod.
* The appendix header (line 38) carries the AI-only status for lem:tb-sylow. ✓

## Findings

### E1 (Error): the finite-gate-set synthesis error is not in the 1/200

Lines 1259-1264:

> "over a fixed finite gate set its $O(\ell\log\ell)$ rotations ... are synthesized to total error $1/400$ ... The success bounds of Lemma~\ref{lem:tb-sylow}(d) are those of the exact transform ..., less $1/200$ per pair of runs"

Line 608: "(the $1/200$ is the transform error of~(H3) ...)"

**Why it is wrong.**
* Truncation already uses 1/400 per run (line 1246). Synthesis adds up to another 1/400.
* So a run's output distribution moves by up to 1/200, and a pair's by up to 1/100.
* Then (4/π²)²·6/π² − 1/100 = 0.08986 < 1/11. The inequality "> 1/11" fails, and with it the constants 11, 1/22 and T that depend on it.
* The paragraph is correct only when rotations are counted as gates.

**Fix: halve both budgets.** The gate formula keeps its form, and r grows by one.

At line 1245-1247, replace
```
with every $\mathrm{C}R_k^{-1}$, $k > r = \lceil\log_2(800\pi t)\rceil$, omitted; by the bound
$2\pi t2^{-r}$ proved there, this moves the output distribution of a run by at most $1/400$ in
total variation.
```
by
```
with every $\mathrm{C}R_k^{-1}$, $k > r = \lceil\log_2(1600\pi t)\rceil$, omitted. By the bound
$2\pi t2^{-r} \le 1/800$ proved there, in operator norm, and since the trace distance of two pure
states is at most their norm distance, this moves the output distribution of a run by at most
$1/800$ in total variation.
```

At lines 1260-1262, replace
```
are
synthesized to total error $1/400$ by~\cite{DawsonNielsen2006} at a factor
$\operatorname{polylog}(\ell)$,
```
by
```
are
synthesized to total operator-norm error $1/800$ by~\cite{DawsonNielsen2006} at a factor
$\operatorname{polylog}(\ell)$, so that with the truncation a run moves by at most $1/400$ in
total variation and a pair by at most $1/200$,
```

At line 608, replace `(the $1/200$ is the transform error of~(H3) in` by `(the $1/200$ bounds, by~(H3) in`, and after `Proposition~\ref{prop:tb-count-gates})` insert `, the total-variation effect on a pair of runs of truncating and synthesizing the transform`.

### E2 (Error): the total-time exponent is false at c = 1

* Appendix lines 1288-1290: "the total time is $O_c(N^{E_W(c)+1+\max(3,\hat\beta_c)+o(1)})$".
* main.tex line 1034: "the total time is $O_c(N^{E_W(c)+1+\max(3,\hat\beta_c)+o(1)})$".

**Why it is wrong.**
* The theorem fixes any c. The appendix treats c = 1 explicitly at line 1239 ("for $p = 2$, which occurs only when $c = 1$").
* At c = 1, E_W(1) = 1 and no solver is called, so the exponent is 5. But the chart time is ℓ⁶ (≤ N⁶) and the primality certificates are Õ(sℓ^{17/2}).
* The justification "below $E_W(c)+4 \ge 9$" (line 1328) holds only for c ≥ 2.
* At c = 1 the gate claim N^{E_W+4} = N⁵ still holds: (a) is Q_f(ℓ³+w) ≤ N²·N³ = N⁵, (b) is N^{4+o(1)}, (c) is 2N⁴.

**Fix.** In the appendix at line 1289 and in main.tex at line 1034, after `\max(3,\hat\beta_c)+o(1)})$`, insert:
```
for $c \ge 2$; for $c = 1$, where $E_W(1) = 1$ and no solver is called, the same counts give
total time $O(N^{17/2+o(1)})$, dominated by the primality certificates
```
In the appendix, keep the existing proviso on the degree of the normal-form arithmetic, read with 17/2 at c = 1.

### G1 (Gap): the classical time of lem:tb-sylow(d) beyond AKS is not counted

Line 1239: "the unit inversions of Lemmas~\ref{lem:tb-chart} and~\ref{lem:tb-sylow} are classical bit operations counted in~(d)". Item (d) (lines 1279-1283) lists only the AKS term for lem:tb-sylow.

**What is missing.** Per run:
* continued fractions;
* the constants a^{2^i} mod F and κ⁻¹ mod F, at O(ℓ²) each, O(ℓ³) in all;
* the gate list, Õ(ℓ³).

Per attempt: gcds, the sequence a^{2^i m}, and the perfect-power tests.

In all this is Õ(sℓ³(ℓ + log(s/ε))) ≤ N^{4+o(1)}. It is harmless to every exponent, but the "counted in (d)" claim is currently false.

**Fix.** In item (d), after `Lemma~\ref{lem:tb-sylow}(d)~\cite[Theorem~5.3]{AKS2004},` insert:
```
plus $\tilde O(s\ell^3(\ell+\log(s/\eps)))$ bit operations for the rest of
Lemma~\ref{lem:tb-sylow}(d) (continued fractions, gcds, perfect-power tests, the constants
$a^{2^i}$ and $\kappa^{-1} \bmod F$, and the gate lists of its runs),
```
In the Exponents line (line 1328), after `$s\ell^{17/2} \le N^{17/2}$,` insert `$s\ell^3(\ell+\log(s/\eps)) \le 2N^4$ again for the latter,`.

### G2 (Gap): thm:bb-envelope(iii) omits the preprocessing classical time

main.tex line 1031:

> "Classical time is $O_c(s^c\ell^4 + \ell^6)$ bit operations for the charts ..., polynomial normal-form arithmetic per normalizer step, and at most $Q_f\cdot(2\ell)^{\hat\beta_c}\ldots$ for the diagonal-equation solvers."

This omits the AKS term Õ(sℓ^{17/2}), which is in the Proposition's (d), and the G1 term. Yet the AKS term is the one that forces "E_W(c)+4 ≥ 9".

**Fix.** After `for the diagonal-equation solvers` insert:
```
, plus $\tilde O(s\ell^{17/2})$ bit operations for the primality certificates and
$\tilde O(s\ell^3(\ell+\log(s/\eps)))$ for the rest of the order finding and factoring
(Proposition~\ref{prop:tb-count-gates}(d))
```

### I1 (Imprecision): the −1/200 is in the wrong place in the inequality chain

Lines 607-608:

> "$\Pr[v = o_i] \ge (4/\pi^2)^2\prod_{q \mid o_i}(1-q^{-2}) \ge (4/\pi^2)^2\cdot 6/\pi^2 - 1/200$"

The first inequality holds only for the exact transform. For the circuit actually run, the 1/200 must be subtracted before the product bound is used.

**Fix.**
```
so $\Pr[v = o_i] \ge (4/\pi^2)^2\prod_{q \mid o_i}(1-q^{-2}) - 1/200
\ge (4/\pi^2)^2\cdot 6/\pi^2 - 1/200 > 1/11$, where the first term bounds the exact transform
```

### I2 (Imprecision): the 4/π² source and the convergent-selection rule

Lines 603-605:

> "One run of Shor's order-finding circuit (\arxivid{quant-ph/9508027}) ... returns, with probability at least $4/\pi^2$, the reduced fraction of $k/o_i$"

Problems:
* The exact 4/π² is the CEMM phase-estimation bound; Shor's own bound is asymptotic.
* The rule that picks the fraction (the last convergent with denominator ≤ 2^ℓ) is not stated.
* The citation style is inconsistent with `\cite{Shor1997}` elsewhere.

**Fix.**
```
One run of Shor's order-finding circuit~\cite{Shor1997} with $2\ell+1$ control qubits and the
exact transform returns, with probability at least $4/\pi^2$
\cite[Sections~5 and~6]{CleveEkertMacchiavelloMosca1998}, the reduced fraction of $k/o_i$ for
some $k$, as the last convergent with denominator at most $2^\ell$ of the measured
$b/2^{2\ell+1}$ (since $|b/2^{2\ell+1} - k/o_i| \le 2^{-2\ell-2} < 1/(2o_i^2)$, by
\cite[Theorem~184]{HardyWright2008}, and distinct fractions with denominators at most $2^\ell$
differ by at least $2^{-2\ell}$),
```

### I3 (Imprecision): the Chernoff bound for dependent attempts

Lines 625-627: "the number of successes dominates a binomial variable of mean $\mu = T/22$ ...; by the Chernoff bound".

The domination is true, but it needs the coupling, because the attempts are adaptive, not independent.

**Fix.** After `attempts,` insert:
```
coupling attempt $j$ with an independent uniform $U_j \in [0,1]$ so that it succeeds whenever
$U_j \le 1/22$ (possible because its success probability given the history is at least $1/22$),
```
After `by the Chernoff bound` insert `$\Pr[X \le \mu/2] \le e^{-\mu/8}$ for $X \sim \mathrm{Bin}(T,1/22)$`.

### I4 (Imprecision, low confidence): the "as in" attached to the VBE qubit count

Lines 1255-1256: "gates on $7n+6$ qubits, as in~\cite[Section~IV]{VedralBarencoEkert1996}".

As I recall, VBE count 7n+1 qubits for their exponentiation. The architecture is theirs, but the count here is the paper's own.

**Fix.** Replace `as in~\cite[Section~IV]{VedralBarencoEkert1996}` with `following the architecture of~\cite[Section~IV]{VedralBarencoEkert1996} (the qubit count here is that of the blocks above)`.

### S1 (Style): the 38n+12 parenthetical does not add up as worded

Lines 1252-1254: "(two passes of $n$ controlled loads and modular additions of at most $38n+12$ gates, and $3n$ gates for the controlled swap)".

Read literally, this gives 2n(38n+12) + 3n = 76n² + 27n. The loads are what make it 80n².

**Fix.**
```
(two passes of $n$ steps, each two controlled loads of at most $n$ gates and one modular
addition of at most $38n+12$ gates, so $2n(40n+12)$, and $3n$ gates for the controlled swap)
```

### S2 (Style): the exponents parenthetical covers only half the bound

Line 1328: "$s\ell^3(\ell+\log(s/\eps)) \le 2N^4$ (as $s\ell^4 = (s\ell)\ell^3 \le N^4$)".

**Fix.**
```
(as $s\ell^4 = (s\ell)\ell^3 \le N^4$ and, since $\log_2 s \le s\ell$,
$s\ell^3\log(s/\eps) \le (s\ell)\ell^2\,(s\ell + \log(1/\eps)) \le N^4$)
```

## Comparison with the earlier review (read after this pass)

Agreements with `2026-11-04-rees-h3-check.md`:
* every count;
* the 1/11 margin with 1/200;
* T and Chernoff;
* the Miller-step lemma;
* the citations to Shor §5 and Hardy–Wright 184.

Its handling of the AKS number agrees with my settled recollection. It reports checking the Annals text: Thm 5.3 is 15/2 and Thm 5.1 is 21/2.

Its application log (lines ~280) already notes the c = 1 problem. It calls it a pre-existing gap, "left unchanged". E2 here records it as an Error that is still present.

New here:
* **E1.** The earlier review calls the Dawson–Nielsen synthesis to 1/400 "negligible". It does not notice that this doubles the per-pair loss to 1/100, which breaks "> 1/11".
* **G1 and G2.** Its "side finding" adds only the AKS term to (d), and nothing to thm(iii).
* I1-I4, S1 and S2.

Neither review checks CEMM's section numbers offline, so that remains for a human.

## Applied (11-04)

Edited locally: `docs/papers/rees-hsp/appendix-torsion-blackbox.tex` and `docs/papers/rees-hsp/main.tex`. No git, no network. Backups are in the session scratchpad (`bak-i178/`). The build had 141 pages, 0 Overfull, no "Float too large" and no undefined references. `tests/tools/test_rees_paper_numbers.py` passed (2 tests). `modexp_check.py` was rerun and passed; no gate constant changed. All "AI-checked, pending human review" labels are kept (31 in main.tex, 2 in the appendix, as before).

**Constants.**
* The only change is r = ⌈log₂(1600πt)⌉, which was ⌈log₂(800πt)⌉. Truncation and synthesis are each 1/800 in operator norm. That makes ≤ 1/400 TV per run and ≤ 1/200 per pair.
* (4/π²)²·6/π² − 1/200 = 0.09486 > 1/11, with margin 0.0039. I rechecked this, and also checked 2πt·2^{−r} ≤ 1/800 for every t < 20000.
* 11, 1/22, T = ⌈88ℓ + 176 ln(2s/ε)⌉, ⌈11 ln(2s/ε)⌉, the Chernoff step, 80n²+27n, 7n+6 and (2n+1)(r+2)+1 are unchanged.

**AKS citation (choice).** I cannot confirm offline that AKS2004 Theorem 5.3 is the Õ(log^{15/2} n) bound. So the text now cites only the paper's main bound Õ(log^{21/2} n), as `\cite{AKS2004}` with no theorem number, in (d), in the proof of (d) and in thm:bb-envelope(iii).
* As a result the certificates cost Õ(sℓ^{23/2}), not Õ(sℓ^{17/2}).
* Effect on the time exponent:
  * For c ≥ 3 nothing changes, since E_W(c)+4 ≥ 14 > 23/2. E_W(c) ≥ 11 for 3 ≤ c ≤ 9 by lem:tb-count-exponent, and E_W(c) ≥ c otherwise.
  * At c = 2 the time exponent becomes max(6+max(3,β̂₂), 23/2).
  * At c = 1 it is 23/2.
* LaTeX comments marked "NEEDS HUMAN VERIFICATION" in both files say that confirming the 15/2 bound turns 23/2 into 17/2. The c ≥ 3 form would then hold for c ≥ 2, and the c = 1 time would be N^{17/2+o(1)}.
* Lenstra–Pomerance was not added, because its bibliographic data could not be checked offline.

Per finding:
* **E1: applied.** It is used as given at the truncation and synthesis sentences of (H3). At lem:tb-sylow(d) the line-608 fix is merged into the I1 rewrite: "the 1/200 bounds, by (H3) …, the total-variation effect on a pair of runs of truncating and synthesizing the transform".
* **E2: modified.** The fix restricts the original form, and c = 1 is stated separately as asked, but with 23/2 rather than 17/2 because of the AKS choice.
  * The appendix now defines τ_c = max(E_W(c)+1+max(3,β̂_c), 23/2) for every c ≥ 1, with the normal-form proviso read at τ_c.
  * The appendix gives the value of τ_c for c ≥ 3, c = 2 and c = 1, and the proof of the Exponents step is rewritten to match.
  * main.tex states c ≥ 3, c = 2 and c = 1 separately.
  * The gate claim N^{E_W(c)+4+o(1)} is now stated for every c ≥ 1.
* **G1: applied.** The term was added to (d), and the proof of (d) gained one sentence that itemizes the cost: per run, per attempt, per generator. Line 1328 now cites 2N⁴ for "the gates of (c) and again for the latter part of (d)".
* **G2: applied, modified.** It uses 23/2 instead of 17/2 and cites `\cite{AKS2004}` with no theorem number.
* **I1: applied.**
* **I2: modified.**
  * `\cite{Shor1997}` replaces the arXiv id.
  * The convergent rule is added as given.
  * CEMM is cited without section numbers. This is done here and also in the (H3) paragraph, which said "Sections 5 and 6", since those numbers are unconfirmed. A LaTeX comment records this.
* **I3: applied.**
* **I4: applied.**
* **S1: applied.**
* **S2: applied.**
