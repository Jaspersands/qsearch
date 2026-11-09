# Rees HSP: referee 6, the black-box appendix

4 November 2026. Independent AI referee pass. **AI-checked, pending human review.**

## Scope and ground rules

Files read in full:

* `docs/papers/rees-hsp/appendix-torsion-blackbox.tex`, all 1357 lines.
* `docs/papers/rees-hsp/main.tex`:
  * the abstract and intro (lines 93-126);
  * the regimes table `tab:main-regimes` (lines 204-220);
  * the notation table `tab:notation-bb` (lines 318-335);
  * `thm:ring-to-field` and its proof (lines 976-1000);
  * `sec:black-box-groups`, `prop:black-box` and `thm:bb-envelope` with its sketch and remark (lines 1008-1049);
  * the statement of `lem:qft-mod` and its step E (lines 734-762).
* `references.bib`, for the keys used.
* `research/audits/reviews/2026-11-04-rees-h3-recheck.md`, including its "Applied" section.
* The Rees lines of `research/STATE.md`.

Ground rules: no `.tex` edited, no git, no network. `main.tex` has no label `prop:torsion*`. I read `thm:ring-to-field` (Section `sec:ring`, "Prime-Power Rings and the Ring-to-Field Reduction") in its place.

## Verdict

**The appendix is in good shape and the (H3) fixes are carried through correctly. Three errors remain, all in counts or presentation; no correctness argument breaks.**

* **The (H3) fixes.** Every place that states a time or gate exponent agrees with the new τ_c, with its c = 1, c = 2 and c ≥ 3 cases, and with the AKS Õ(log^{21/2}) assumption. The checklist is below.
* **The proof steps.** I re-derived every step I was asked to check. All hold:
  * the Sylow split, order finding, factoring, the Miller step and the Chernoff coupling;
  * the purification for Imran–Ivanyos;
  * `lem:tb-kernel` and `lem:tb-chart`, Steps 0-6;
  * `prop:tb-recursion`, the superadditivity step, the per-grade arity bound and the E_W(c) table;
  * the error split of the counted algorithm.
* **The three errors.**
  * **E1.** On the failure branches of chart acquisition, the stated per-branch query and call bounds are false. A two-line size check fixes it.
  * **E2.** The refinement "exponent E_W(c) when every e_p = 1" is false at c = 1.
  * **E3.** The regimes table states the large-prime bounds as if they covered all primes.
* **The main gap (G1).** main.tex states the total time unconditionally. The appendix needs a proviso on the degree of the normal-form arithmetic, and main.tex drops it.
* **Outside scope (E4).** The bib entry `FIMSS2014` is the wrong paper.

Counts: **Errors 4** (one outside scope), **Gaps 3**, **Imprecisions 7**, **Style 4**.

## Was the (H3) recheck carried through?

The following agree with τ_c = max(E_W(c)+1+max(3,β̂_c), 23/2) and with AKS at Õ(log^{21/2} n):

| place | content | status |
|---|---|---|
| appendix (H3) paragraph, lines 1260-1290 | r = ⌈log₂(1600πt)⌉; truncation 1/800 and synthesis 1/800 in operator norm; ≤ 1/400 TV per run, ≤ 1/200 per pair; CEMM without section numbers; the VBE "architecture" wording; S1 parenthetical | ✓ |
| lem:tb-sylow(d), lines 602-645 | `\cite{Shor1997}`; the convergent rule; the −1/200 placed before the product bound; the coupling; the explicit Chernoff form | ✓ |
| prop:tb-count-gates(d), line 1295 | Õ(sℓ^{23/2}), plus the G1 term of the recheck | ✓ |
| proof of (d), line 1352 | 4ℓ tests of ≤ 2ℓ bits at Õ(ℓ^{21/2}) each; the remaining cost itemized | ✓ |
| statement after (a)-(d), lines 1305-1310 | τ_c, with the cases c ≥ 3, c = 1 and (in the proof) c = 2 | ✓ |
| Exponents, lines 1352-1357 | sℓ^{23/2} ≤ N^{23/2}; E_W(c)+4 ≥ 14 > 23/2 for c ≥ 3; τ_2 and τ_1 | ✓ (arithmetic rechecked) |
| main.tex thm:bb-envelope(iii), line 1031 | Õ(sℓ^{23/2}) and `\cite{AKS2004}` with no theorem number | ✓ |
| main.tex, line 1034 | the three cases c ≥ 3, c = 2, c = 1 | ✓ (but see G1) |
| main.tex tab:main-regimes, line 220 | gates only, N^{E_W(c)+4+o(1)}, which holds for every c ≥ 1 | ✓ (but see E3) |
| abstract and intro | no time or gate exponent stated for the black-box theorem | ✓, nothing to update |
| "NEEDS HUMAN VERIFICATION" comments | present in both files, consistent with each other | ✓ |

The arithmetic of each case:
* E_W(2) = 5, so τ_2 = max(6+max(3,β̂₂), 23/2) ≥ 23/2.
* E_W(3) = 11, so E_W(3)+4 = 15 > 23/2.
* For c ≥ 10, E_W(c) ≥ c gives E_W(c)+4 ≥ 14.
* At c = 1 there is no grade d ≥ 2, so no solver is called and τ_1 = 23/2.

I recheck the E_W table from scratch:
* 421 = lcm(2..7)+1 is prime.
* 841 = 29² and 1681 = 41², so the first prime p ≡ 1 mod 840 is 2521. It is prime: no divisor up to 47.
* The values 5, 11, 23, 38, 56, 77, 107, 143 follow.

The AKS number remains for a human. My recollection agrees with both earlier reviews: the Annals version states Õ(log^{21/2} n) as the main complexity theorem and derives Õ(log^{15/2} n) later in §5, through Fouvry and Baker–Harman. I cannot confirm the theorem numbers offline. The conservative 21/2 choice is safe.

## Recomputations (summary)

* **Order finding.**
  * The best t-bit approximation of k/o is measured with probability ≥ 4/(π²o), and the events are disjoint over k, since 2^t > 2o².
  * Gcd and lcm: Pr[gcd(k₁,k₂,o) = 1] = J₂(o)/o² ≥ 6/π².
  * (4/π²)²·6/π² − 1/200 = 0.09486 > 1/11.
  * (10/11)^{⌈11 ln(2s/ε)⌉} ≤ ε/(2s).
* **Splitting step.**
  * The success probability is ≥ 1/22 for every history.
  * With μ = T/22 ≥ 4ℓ + 8 ln(2s/ε): μ/2 ≥ 2ℓ > 2ℓ−2, and e^{−μ/8} ≤ ε/(2s).
  * The union over the two failure modes and s generators gives ε_pre.
* **Miller step.** If r = 2^{j'}r′, then x = (a^{r/2})^{m/r′} = a^{r/2}, because m/r′ is odd.
* **Imran–Ivanyos purification.** Tracing out the label of |G_{≤c}|^{-1/2} Σ_x |x⟩|f(x)⟩ gives weight |H′|/|G_{≤c}| = 1/[G_{≤c}:H′] on each normalized coset state, which is Ξ. The inverse is U_f followed by the inverse preparation. ✓
* **lem:tb-kernel.** There are (p^k−1)/(p−1) < p^k hyperplanes, giving p^{k−t} ≤ δ/2. With 2kd transforms at η = ε/(16ℓkd), the transform error is δ/2 at δ = ε/(4ℓ). ✓
* **lem:tb-chart.**
  * Step 1: B^{⊥⊥} = B.
  * Howell-form membership and construction: the invariant ⟨R_t⟩ = ⟨r_{t+1..q}⟩ holds, so q ≤ k.
  * Column scan: r ≤ n on the success event.
  * Smith form over Z/M: PA = col(PCQ), and ε_i = P^{−1}De_i.
  * Step 5 contractions: O(r³k).
  * Lyndon content bound: binom(m;α)/m ≤ (m−1)!.

  The counterexample C₉×C₃ is right: samples are (x, 3y, 0).
* **Counts.**
  * Q_p ≤ cK_cφ(n_p), and φ(x) = x(x+t)(x+1)^{E−1} is superadditive.
  * (i) gives cK_c(L+t)(L+1)^{E_W}.
  * k ≤ 2Λ/log₂p, since log₂p ≤ ℓ ≤ Λ; b_M ≤ 2e_p log₂p.
  * (d) chart time 16dΛ²ℓ² + 64Λ⁴ℓ².
  * (b): 2Σ_p kd ≤ 4dΛℓ transforms.
  * (c): O(sℓ³(ℓ+log(s/ε))) ≤ 2N⁴.

## Findings

### E1 (Error): the "every branch" counts fail on the failure branches of chart acquisition

**Where.**
* Appendix line 1243-1244: "The stop rules and the per-call time-out of Proposition~\ref{prop:tb-recursion} make the counts above hold on erroneous branches as well."
* Also lem:tb-count-grade ("a bound fixed by public data"), lem:tb-count-prime ("at most $n_p$ core calls are made on every branch") and thm:bb-envelope(i).

**Why it is wrong.**
* The bounds are in terms of the true n_p and L.
* When Lemma tb-kernel fails (probability ≤ ε/(4ℓ) per prime), the rows of Y need not generate (ker π)^⊥. Then A = YF ⊆ (Z/M)^k can have order up to M^{min(k,d)}.
  * The computed chart then has size n′_p = Σ_i e_i, up to e_p·min(k,d). That exceeds n_p, and it can exceed ⌊ℓ/log₂ p⌋.
  * The column scan of Step 3 can keep up to e_p k columns rather than n ≤ k.
* The algorithm does not know n_p, because |G| is never computed. So it cannot cap the call count or the core dimension at n_p on such a branch.
* The stop rules of RtF bound the calls by log_p of the computed chart, not by n_p. For e_p = 1 the single core call runs at the computed dimension, up to min(k,d).
* So on these branches the query count, the call count and the cost bound of Lemma tb-chart (O(dk²+k⁴)) are not the stated ones. The error budget is unaffected; only the worst-case counts are.

**Fix.** Add two checks after each chart. They never fire on the success event.

In app:tb-counts, after "the chart of route~(R2) acquired by Lemma~\ref{lem:tb-kernel} at $\delta = \eps/(4\ell)$," insert:
```latex
with two size checks: the column scan of Lemma~\ref{lem:tb-chart} stops and reports failure as
soon as more than $\lfloor\ell/\log_2 p\rfloor$ columns are kept, and, writing
$n'_q = \sum_i e_i$ for the size of the chart computed for a prime $q$, the algorithm stops and
reports failure if $\prod_q q^{n'_q} > 2^\ell$, the product running over the primes $q > c$
processed so far. On the success event of Lemma~\ref{lem:tb-kernel} the chart is correct, at most
$n_p \le \lfloor\ell/\log_2 p\rfloor$ columns are kept and $\prod_q q^{n_q} \le |G| \le 2^\ell$, so
neither check fires there. On every branch $n'_p \le \lfloor\ell/\log_2 p\rfloor \le k$ and
$\sum_{p>c} n'_p \le \ell/\log_2(c+1)$,
```
At line 1243, replace the last sentence of the proof of (iv) with:
```latex
The stop rules and the per-call time-out of Proposition~\ref{prop:tb-recursion}, together with
the two size checks after each chart, make the counts above hold on erroneous branches as well,
with $n_p$ replaced by the computed chart size $n'_p$ and $L$ by $\lfloor\ell/\log_2(c+1)\rfloor$.
```
In main.tex thm:bb-envelope(i), after `number at most $c\,K_c\,(L+t)(L+1)^{E_W(c)}$`, insert:
```latex
(on every branch, with $L$ replaced by $\lfloor\ell/\log_2(c+1)\rfloor$; Appendix~\ref{app:tb-counts})
```
The N-forms are unchanged.

### E2 (Error): the exponent-p refinement is false at c = 1

**Where.**
* Appendix lines 1218-1222: "If every $e_p = 1$, ... superadditivity of $x \mapsto x^j$ ($j \ge 1$) gives $\sum_p (n_p+t)(n_p+1)^{E-1} \le \dots \le 2^E (L+t)(L+1)^{E-1}$ ... these are ... $O_c(N^{E_W(c)})$".
* main.tex line 1040: "If every Sylow subgroup for $p > c$ has exponent $p$, the large-prime query exponent is $E_W(c)$."

**Why it is wrong.**
* The step uses superadditivity of x^{E−1}, which needs E−1 ≥ 1.
* At c = 1, E_W(1) = 1 and the sum is Σ_p (n_p + t) = L + t·#{p}. This can reach ~ (ℓ/log ℓ)·log(1/ε).
* For example, take s = 1, a cyclic group of squarefree order with ~ℓ/log ℓ prime factors, and log(1/ε) ≈ ℓ. Then N ≈ 2ℓ and the count is N^{2−o(1)}, not O(N).
* For c ≥ 2 the step is valid, since E_W(c) ≥ 5.

**Fix.** At appendix line 1218, replace `If every $e_p = 1$, put` with `If $c \ge 2$ and every $e_p = 1$, put`. After `and neither depends on $s$.` (line 1222) insert:
```latex
(At $c = 1$, where $E_W(1) = 1$, the count is $\sum_p (n_p + t) \le L(t+1) = O(N^2)$, and the
exponent $E_W(1)$ is not claimed.)
```
At main.tex line 1040, replace `If every Sylow subgroup for $p > c$ has exponent $p$,` with `If $c \ge 2$ and every Sylow subgroup for $p > c$ has exponent $p$,`.

### E3 (Error): the regimes-table row states the large-prime bounds for all primes

**Where.** main.tex line 220:

> "Black-box, unique encoding ... & all primes ($p \le c$ via~\cite[Thm.~1]{ImranIvanyos2023}) & ... & $O_c(N^{E_W(c)+1})$ queries, $O_c(N^{E_W(c)+4+o(1)})$ gates"

The caption adds that the row "also covers the primes $p \le c$".

**Why it is wrong.**
* thm:bb-envelope gives O_c(N^{E_W(c)+1}) queries and N^{E_W(c)+4+o(1)} gates only for the primes p > c.
* The primes p ≤ c add poly(log|G|) queries, "whose exponent ... is not bounded here", and the gates of Imran–Ivanyos are "added separately".
* Read literally, the row claims a bound that the theorem does not give.
* The caption's title also says "($p > c$)" while this row says "all primes".

**Fix.** Replace the row with:
```latex
Black-box, unique encoding (Thm.~\ref{thm:bb-envelope}) & all primes ($p \le c$ via~\cite[Thm.~1]{ImranIvanyos2023}, counted separately) & combined rule on an acquired chart; $\le n_p$ socle rounds if $e_p > 1$ & for $p > c$: $O_c(N^{E_W(c)+1})$ queries, $O_c(N^{E_W(c)+4+o(1)})$ gates; $p \le c$ adds $\poly(\log|G|)$ queries \\
```
In the caption, replace `it also covers the primes $p \le c$, through~\cite[Theorem~1]{ImranIvanyos2023}.` with:
```latex
it also covers the primes $p \le c$, through~\cite[Theorem~1]{ImranIvanyos2023}, whose queries and gates are not included in the stated bounds.
```
After the edit, check that the table does not overfull.

### E4 (Error, outside scope): the bib entry FIMSS2014 is the wrong paper

**Where.** references.bib, `FIMSS2014`:

> title "On {$K$}-wise Independent Distributions and {Boolean} Functions", note "arXiv:1201.3261"

It is cited in main.tex line 126 for the HSP in solvable groups of bounded derived length and bounded exponent.

**Why it is wrong.** As I recall, that result is Friedl, Ivanyos, Magniez, Santha and Sen, "Hidden translation and translating coset in quantum computing", SIAM J. Comput. 43(1):1-24 (2014), arXiv:quant-ph/0211091. The title in the entry does not match the cited content. I cannot confirm the arXiv id 1201.3261 offline, but the title is certainly not this result.

**Fix** (bib data from memory; a human should confirm):
```latex
@article{FIMSS2014,
  author  = {Friedl, Katalin and Ivanyos, G{\'a}bor and Magniez, Fr{\'e}d{\'e}ric and Santha, Mikl{\'o}s and Sen, Pranab},
  title   = {Hidden Translation and Translating Coset in Quantum Computing},
  journal = {SIAM Journal on Computing},
  volume  = {43},
  number  = {1},
  pages   = {1--24},
  year    = {2014},
  note    = {arXiv:quant-ph/0211091}
}
```

### G1 (Gap): main.tex drops the appendix's proviso on the normal-form arithmetic

**Where.**
* Appendix lines 1306-1308: "The total time is $O_c(N^{\tau_c+o(1)})$ ..., provided the degree of the normal-form arithmetic is at most $\tau_c$."
* main.tex line 1031 says only "polynomial normal-form arithmetic per normalizer step".
* main.tex line 1034 then states the total time for c ≥ 3, c = 2 and c = 1 with no proviso.

**Why it matters.**
* The main-text time claim is stronger than what the appendix proves. The appendix cites "Kannan–Bachem; Storjohann" for (M1)-(M3) but gives no degree.
* The normalizer steps for e_p > 1 are the only time term without an explicit exponent.

**Fix (required).** In main.tex line 1034, replace `and the total time is $O_c(N^{E_W(c)+1+\max(3,\hat\beta_c)+o(1)})$ for $c \ge 3$;` with:
```latex
and, provided the normal-form arithmetic of the normalizer steps runs within the same bound
(Proposition~\ref{prop:tb-count-gates}), the total time is
$O_c(N^{E_W(c)+1+\max(3,\hat\beta_c)+o(1)})$ for $c \ge 3$;
```

**Fix (optional; derived in this review, not checked by a second pass).** The proviso can be discharged by running (M1)-(M3) on the chart with Howell forms over Z/M, as in Lemma tb-chart Step 2. Embed L_G in (Z/M)^{m} by t_i ↦ p^{e_p−e_i}t_i. The bit-length step of the paragraph "Public module arithmetic" then becomes unnecessary. Drop-in for the proof of (d), after `Normalizer steps: Proposition~\ref{prop:tb-recursion}, at most $n_p$ rounds per prime.`:
```latex
On the chart, $m \le n_p$, and every lattice of (M1)--(M3) may be replaced by a generating set in
$(\mathbb{Z}/M)^m$, embedding $\mathcal{L}_G$ by $t_i \mapsto p^{e_p-e_i}t_i$; the idealizer of (M2)
is then the kernel of a map given by an $m \times m^2$ matrix over $\mathbb{Z}/M$, whose entries are
$m^2$ brackets of $O(m^3)$ ring operations each, and its kernel, the presentation of (M1) and the
socle tensor of (M3) are read from Howell and Smith forms as in Lemma~\ref{lem:tb-chart} at
$O(m^5)$ ring operations. With $b_M \le 2e_p\log_2 p \le 2n_p\log_2 p$ and $n_p\log_2 p \le \ell$, a
prime costs at most $n_p\cdot O(n_p^5)\cdot O(b_M^2) = O(n_p^8\log_2^2 p) \le O(\ell^8)$ bit
operations, and all primes $O(\ell^8) \le N^{8} \le N^{\tau_c}$, since $\tau_c \ge 23/2$.
```
If this is adopted, delete the proviso in both files. A second check of the kernel-by-Howell-form cost is needed first.

### G2 (Gap): the N-forms of the chart gates and chart time are derived only under log₂(8ℓ/ε) ≤ ℓ

**Where.** Appendix Exponents paragraph, lines 1352-1356:

> "$s^c\ell^2(\ell+\log(s+1))^2 \le N^{\max(c,4)+o(1)}$, ... $s^c\ell^4 + \ell^6 \le N^{\max(c,6)}$ ... the charts by $\max(c,6) \le \max(E_W(c)+4,\,23/2)$"

**Why it is incomplete.**
* These are the ℓ-only forms, valid only when log₂(8ℓ/ε) ≤ ℓ.
* The N-claims ("(a)–(c) are $O_c(N^{E_W(c)+4+o(1)})$", total time N^{τ_c}) are stated unconditionally. thm:bb-envelope says "no other count depends on this condition".
* The unconditional forms do hold, but no line derives them:
  * chart time: 16dΛ²ℓ² + 64Λ⁴ℓ² with Λ ≤ 2N+4 gives O_c(N^{max(c,2)+2} + N⁶);
  * chart transforms: 4dΛℓ·O((ℓ + log(16ℓkd/ε))²), using s^cℓ ≤ N^c, gives O_c(N^{c+3+o(1)}).

**Fix.** In the Exponents paragraph, after `$s^c\ell^4 + \ell^6 \le N^{\max(c,6)}$,` insert:
```latex
and, without the condition $\log_2(8\ell/\eps) \le \ell$, the chart time of~(d) is
$O_c(s^c\Lambda^2\ell^2 + \Lambda^4\ell^2) \le O_c(N^{\max(c,2)+2} + N^6)$ and the transforms of~(b)
cost $4d\Lambda\ell\cdot O((\ell + \log(16\ell kd/\eps))^2) \le O_c(N^{c+3+o(1)})$, since
$d \le c\,s^c$, $s^c\ell \le N^c$, $\Lambda \le 2N+4$ and $\log(16\ell kd/\eps) = O_c(N)$,
```
Then replace `the charts by $\max(c,6) \le \max(E_W(c)+4,\,23/2)$` with:
```latex
the charts by $\max(c+2,6) \le \max(E_W(c)+4,\,23/2)$, and the transforms of~(b) by $c+3 \le E_W(c)+4$
```

### G3 (Gap, harmless): the per-query gate count in (a) omits two O(ℓ³) terms

**Where.**
* Appendix line 1328: "A leaf makes $c$ queries, each with $O_c(n_p(2b_M + A_c)) = O_c(\ell^2)$ multiplication calls ..., $O(w)$ gates for the label register and $O(n)$ field operations for $E_s$."
* lem:tb-count-prime, line 1206: "The section $\sigma$ and the socle map $\iota_M$ are public coordinate arithmetic."

**What is missing.**
* For e_p > 1, each local query evaluates σ∘ι_M coherently on a quantum register. That is a public linear map from F_p^{m′} to chart coordinates modulo p^{e_i}: up to n_p² constant multiply-accumulates of a ⌈log₂p⌉-bit digit into a b_M-bit residue.
  * The cost is O(n_p²b_M log p) ≤ O(ℓ n_p b_M) ≤ O(ℓ³) gates, using n_p b_M ≤ 2ℓ e_p ≤ 2ℓ².
* Each of the O(n_p b_M) multiplication calls also loads an ℓ-bit classical constant, at O(ℓ) gates: O(ℓ³) per query.
* Both fit the ℓ³ in Q_f(ℓ³+w), but neither is counted.

**Fix.** At line 1328, after `$O(w)$ gates for the label register` insert:
```latex
, $O(\ell)$ gates per multiplication call to load its classical constant ($O(\ell^3)$ per query),
the coherent public map $\sigma\circ\iota_M$ of Lemma~\ref{lem:tb-quotient-oracle} at
$O(n_p^2 b_M\log p) \le O(\ell^3)$ gates by~(H2)
```

### I1 (Imprecision): the strip step needs up to 4ℓ tests, not 2ℓ

**Where.** Appendix lines 638-640: "This ends at $o_i$ after at most $\log_2 v \le 2\ell$ tests of $O(\ell)$ multiplications each (only denominators at most $2^\ell$ are kept)."

**Why it is imprecise.**
* Each successful test lowers Ω(v), and each distinct prime contributes one final failing test. So the count is ≤ Ω(v) + ω(v) ≤ 2log₂v ≤ 4ℓ.
* The parenthetical is unclear: v is an lcm of two denominators ≤ 2^ℓ, so it can be as large as 2^{2ℓ}.
* The O(sℓ²) multiplication count is unchanged.

**Fix.**
```latex
This ends at $o_i$ after at most $\Omega(v) + \omega(v) \le 2\log_2 v \le 4\ell$ tests of $O(\ell)$
multiplications each.
```

### I2 (Imprecision): the mod-F runs need the convergent rule with 2^n, not 2^ℓ

**Where.** Appendix line 623: "a pair of runs modulo $F$ as in~(H3) ... gives, with probability above $1/11$, some $u$". The convergent rule is stated only for the black-box runs, with "denominator at most $2^\ell$".

**Why.** For a run modulo F the order of a is below F ≤ 2^n with n = ⌈log₂F⌉ ≤ 2ℓ. The rule and the 1/11 bound must be read with n and t = 2n+1. The (H3) paragraph does fix t = 2n+1 but not the denominator cap.

**Fix.** After `as in~(H3) of Proposition~\ref{prop:tb-count-gates}` insert:
```latex
(with $n = \lceil\log_2 F\rceil$ in place of $\ell$: $2n+1$ control qubits and the last
convergent with denominator at most $2^n$, which bounds the order of $a$ since it is below $F$)
```

### I3 (Imprecision): the error split of tab:tb-steps and its paragraph is not the split of the counted algorithm

**Where.**
* Appendix line 1067: "Split the error as $\eps = \eps_{\mathrm{pre}} + \eps_{\mathrm{small}} + \sum_{p > c}\eps_p$".
* Table rows, line 1093: "(R2): kernel ... $d + O(\log(1/\eps_p))$ evaluations ... & $\eps_p/2$" and "(R2): recursion ... & $\eps_p/(2\ell)$ per core".

**Why.**
* app:tb-counts and thm:bb-envelope(iv) use four global quarters: ε/(4ℓ) per chart and ε/(4ℓ) per core call.
* With the table's per-prime split, a core call would get ε_p/(2ℓ), which is a different ε in t and in the terminal samples.
* The kernel row's sample count also differs from the min(d, ⌊ℓ/log₂p⌋) + ⌈log_p(2/δ)⌉ of Lemma tb-kernel.

**Fix.** Replace the two sentences at line 1066-1068 (`Split the error as ... large primes.`) with:
```latex
The error is split as in Appendix~\ref{app:tb-counts}: $\eps/4$ for Lemma~\ref{lem:tb-sylow}(d),
$\eps/4$ for the primes $p \le c$, $\eps/(4\ell)$ for each of the at most $\ell$ charts and
$\eps/(4\ell)$ for each of the at most $\ell$ core calls.
```
In the table:
* replace `$d + O(\log(1/\eps_p))$ evaluations of $\Phi$` with `$\min(d,\lfloor\ell/\log_2 p\rfloor) + \lceil\log_p(8\ell/\eps)\rceil$ evaluations of $\Phi$`;
* replace `$\eps_p/2$` with `$\eps/(4\ell)$`;
* replace `$\eps_p/(2\ell)$ per core` with `$\eps/(4\ell)$ per core`;
* in the e = 1 and (R1) rows, replace `$\eps_p$` and `$\eps_p/(ed)$ per core` with `(not used in Theorem~\ref{thm:bb-envelope})`.

### I4 (Imprecision): the oracle model in thm:bb-envelope, and the in-place oracle of Imran–Ivanyos

**Where.**
* main.tex line 1027: "coherent multiplication and its inverse (the appendix does not use the inverse)".
* Appendix line 540: "The in-place oracle ... together with its adjoint yields this one".
* Appendix line 550: "This also supplies the inversion oracle of the black-box model of~\cite{ImranIvanyos2023}."

**Why.**
* "Its inverse" is ambiguous. If it means the adjoint of an in-place oracle, the appendix does use it, to build the XOR oracle. If it means a group-inversion oracle, it is not used, so it should not be assumed.
* The black-box model of Imran–Ivanyos is, as usual, presumably in-place: |x,y⟩ ↦ |x,xy⟩ and |x,y⟩ ↦ |x,x^{-1}y⟩. I cannot verify this offline.
* From the XOR oracle the appendix supplies only the inversion. The in-place product needs one more line: compute xy out of place, then erase y by XOR-ing x^{-1}(xy) into it, with x^{-1} = x^{M−1} computed and uncomputed in a clean register.

**Fix.** In main.tex line 1027, replace `coherent multiplication and its inverse (the appendix does not use the inverse)` with:
```latex
a coherent multiplication oracle, either $\lvert x,y,z\rangle \mapsto \lvert x,y,z\oplus xy\rangle$ or the in-place $\lvert x,y\rangle \mapsto \lvert x,xy\rangle$ together with its adjoint (no group-inversion oracle is needed; Appendix~\ref{app:tb-blackbox})
```
At appendix line 550, after `This also supplies the inversion oracle of the black-box model of~\cite{ImranIvanyos2023}` insert:
```latex
, and its in-place multiplication: compute $xy$ out of place, then XOR $x^{-1}(xy) = y$ into the
input register, with $x^{-1} = x^{M-1}$ computed and uncomputed in a clean register, and swap
```

### I5 (Imprecision): the gate set of items (b) and (a) is not stated

**Where.**
* Appendix item (b), line 1289: "each to isometry error $\eta = \eps/(16\ell kd)$, that is $O_c(s^c\ell^2(\ell+\log(s+1))^2)$ gates". The same applies to the transform term of (a).
* main.tex line 1031, the same count.

**Why.**
* These counts take the rotations R_k^{±1} and CR_k^{±1} of Lemma qft-mod as single gates.
* Over a fixed finite gate set, (H1)'s own parenthetical adds a factor polylog(b/η) = polylog(ℓkd/ε).
* (c) is unaffected: its rotations are O(ℓ log ℓ) per run, at constant precision.
* The N-exponents absorb the factor through the +o(1), but the explicit counts should name the gate set.

**Fix.** In item (b), after `gates when $\log_2(8\ell/\eps) \le \ell$`, insert:
```latex
(rotations $R_k^{\pm1}$, $\mathrm{C}R_k^{\pm1}$ of Lemma~\ref{lem:qft-mod} counted as single gates;
over a fixed finite gate set, times $\operatorname{polylog}(\ell kd/\eps)$, as in~(H1))
```
Add the same parenthetical in main.tex line 1031 after `$O_c(s^c\ell^2(\ell+\log(s+1))^2)$ gates when $\log_2(8\ell/\eps) \le \ell$`.

### I6 (Imprecision): the list in the appendix status paragraph of what is cited rather than proved is incomplete

**Where.** Appendix lines 45-47: "Everything else below is proved here, except the cited results of Imran and Ivanyos (Lemma~\ref{lem:tb-small-primes}), Shor's order finding and factoring, and the AKS test".

**Why.** Further results are also imported, not proved:
* the exact 4/π² phase-estimation bound of CEMM;
* Hardy–Wright Theorem 184;
* Dawson–Nielsen synthesis;
* the Hermite and Smith normal-form algorithms (Kannan–Bachem, Storjohann);
* the exact Watrous-type uniform superposition used by Imran–Ivanyos;
* Lazard's correspondence (Trappeniers' form);
* Dynkin–Specht–Wever and the Hall/Lyndon basis.

**Fix.** Replace the sentence with:
```latex
Everything else below is proved here, except the cited results: Imran and Ivanyos
(Lemma~\ref{lem:tb-small-primes}, including the exact uniform superposition they use), Shor's
order finding and factoring with the phase-estimation bound
of~\cite{CleveEkertMacchiavelloMosca1998} and~\cite[Theorem~184]{HardyWright2008}, the AKS test
(Lemma~\ref{lem:tb-sylow}(d)), gate synthesis~\cite{DawsonNielsen2006}, polynomial-time Hermite
and Smith normal forms, the Lazard correspondence~\cite{Lazard1954,Trappeniers2024}, and the
Dynkin--Specht--Wever theorem and Lyndon basis of free Lie rings.
```

### I7 (Imprecision): citations I could not verify offline

These are not wrong as far as I know, but each needs a human check against the source:

* **ImranIvanyos2023** (Zero sum subsequences and hidden subgroups, QIP 23, arXiv:2304.08376). The appendix relies on:
  * the hypotheses of Theorem 1, as paraphrased in lem:tb-small-primes;
  * Proposition 1 needing the prime factors as input;
  * Lemma 1, the purification criterion;
  * §2.1, constant-gate exact transforms for bounded primes;
  * §2.2, the "exact version of Watrous's method".

  It also relies on the claim that their model's only non-exact gates are those charged to the small-prime share by lem:hybrid. If their uniform-superposition preparation uses amplitude-amplification angles that depend on |G_{≤c}|, those must also be synthesized within ε/4. The text's "gate synthesis only" should then include them.
* **Trappeniers2024**, Theorem 2.3 with Examples 2.1-2.2, as the statement of Lazard's correspondence.
* **VedralBarencoEkert1996**, "Section IV" as the modular-exponentiation architecture.
* **AKS2004**: the 15/2 bound and its theorem number (see above). The text currently relies only on 21/2, which is safe.
* **CleveEkertMacchiavelloMosca1998**: the exact 4/π² bound. It is cited without section numbers, correctly so for now.
* **Kitaev1995** for approximate QFT over Z/p^e (lem:tb-kernel). Coppersmith's 1994 report or Lemma qft-mod itself is the more precise source. Lemma qft-mod already proves what is used, so "cf." is fine.

No fix is needed beyond a human check. If the Imran–Ivanyos preparation is not exact in a finite gate set, amend thm:bb-envelope(iv) as follows:
```latex
the primes $p\le c$ (synthesis of every non-exact gate of~\cite{ImranIvanyos2023}, including its uniform-superposition preparation)
```

### S1 (Style): the Howell-form conditions are named (H1) and (H2)

**Where.** Appendix lines 927-929, 941 and 956: "a \emph{Howell form} if (H1) ... and (H2) ...", "by (H2)", "which is (H2)".

**Why.** These collide with (H1)-(H3) of prop:tb-count-gates, which main.tex cites by name, and "(H2)" is used in both senses within 400 lines.

**Fix.** Rename them to (HF1) and (HF2) at all four places:
```latex
nonzero vectors of $(\mathbb{Z}/M)^k$ a \emph{Howell form} if (HF1) its leading
```
Similarly use `and (HF2) $p^{e-a_t}r_t \in \dots$`, `$\in S_{t+1}$ by (HF2).` and `which is (HF2).`

### S2 (Style): the header comment is stale, and Khukhro is cited without its key

**Where.**
* Appendix lines 19-34: the comment lists Trappeniers2024, Khukhro1998, Shor1997, Kitaev1995 and AKS2004 among "suggested new keys", but all of them are now in references.bib.
* Line 89 cites "Khukhro's monograph \emph{$p$-Automorphisms of Finite $p$-Groups}, Chapters~9--10" without `\cite`, although the comment says it is cited by key.

**Fix.** Replace the citation text at line 89 with:
```latex
see also~\cite[Chapters~9--10]{Khukhro1998})
```
Then trim the comment to the keys that are still missing: Reutenauer1993, KannanBachem1979 and Storjohann1996.

### S3 (Style): a repeated sentence opening in main.tex

**Where.** main.tex line 1010: "The proposition below treats $p > c$. The proposition below adapts constructions from project notes ...".

**Fix.**
```latex
The proposition below treats $p > c$; it adapts constructions from project notes that are still under review.
```

### S4 (Style): X is defined twice in the Chernoff sentence

**Where.** Appendix lines 631-634: "dominates a binomial variable $X$ of mean $\mu = T/22$, ...; by the Chernoff bound $\Pr[X \le \mu/2] \le e^{-\mu/8}$ for $X \sim \mathrm{Bin}(T,1/22)$".

**Fix.** Replace from `the number of successes dominates` to `\le \eps_{\mathrm{pre}}/(2s)$.` with:
```latex
the number of successes dominates $X \sim \mathrm{Bin}(T,1/22)$, of mean $\mu = T/22$ with
$\mu/2 \ge 2\ell$, and by the Chernoff bound $\Pr[X \le \mu/2] \le e^{-\mu/8}$ the factorization is
incomplete with probability at most $e^{-\mu/8} \le \eps_{\mathrm{pre}}/(2s)$.
```

## Claim discipline

* No sentence in the appendix or in the main-text passages read claims a speedup, a practical algorithm or established novelty.
* The intro says "we do not claim that it settles the question of~\cite[Section~6]{ImranIvanyos2023} before it has had human review". The theorem title carries "conditional, AI-checked only". The abstract ends with "None of this has been independently verified or assessed for novelty".
* "AI-checked, pending human review" appears:
  * in the appendix status line (line 38);
  * in the title of lem:tb-chart;
  * in the (H2) and (H3) paragraphs;
  * in main.tex at sec:black-box-groups and in the closing paragraph of thm:bb-envelope.
* The status paragraph covers lem:tb-sylow, lem:tb-small-primes, lem:tb-count-* and prop:tb-count-gates; none of them carries its own label. That is acceptable.

## Next check

1. Apply E1-E3, G1 (required part) and G2. Rebuild and confirm 0 Overfull, in particular for the E3 table row.
2. A human should confirm:
   * the AKS 15/2 bound and its theorem number;
   * the Imran–Ivanyos items of I7;
   * the FIMSS2014 bib data.
3. If the optional G1 discharge is adopted, have it checked independently: the Howell-form kernel cost O(m⁵) ring operations per round, and the ℓ⁸ total. Then remove the proviso from both files.

## Applied (11-04)

Applied by an AI integration pass on 4 November 2026 to `main.tex` and `appendix-torsion-blackbox.tex` (local only; no git). Build: 143 pages, 0 Overfull, no "Float too large", no undefined references; `tests/tools/test_rees_paper_numbers.py` passes. Backups: `/private/tmp/claude-501/.../scratchpad/bak-i181/`. AI-checked, pending human review.

Counts: **12 applied, 4 modified, 2 skipped.**

* **E1: applied.** E1's chart-size claim was rechecked. When the transforms are approximate, a failed kernel step can give rows outside (ker π)^⊥, and then |A| can reach M^{min(k,d)}. The two checks never fire on the success event. Every branch then has n'_p ≤ ⌊ℓ/log₂p⌋ ≤ k and Σ n'_p ≤ ℓ/log₂(c+1), and superadditivity together with monotonicity gives (i) with L replaced by ⌊ℓ/log₂(c+1)⌋. The two checks were added in app:tb-counts as their own sentence after the composition sentence, rather than inside it. The proof of (iv) and thm:bb-envelope(i) were changed as proposed. lem:tb-count-prime got one extra parenthetical: on an erroneous chart, n_p is replaced by n'_p.
* **E2: applied.** The claim was rechecked. At c = 1, E−1 = 0 and Σ_p x_p^0 = #primes, so the step fails. For E ≥ 2 the bound X^E + tX^{E−1} ≤ 2^E(L+t)(L+1)^{E−1} holds. Both .tex files were grepped: the claim appears only at appendix (proof of (i)) and main.tex (after thm:bb-envelope). Both now say "c ≥ 2". The c = 1 parenthetical (count ≤ L(t+1) = O(N²)) was added.
* **E3: modified.** One fix covers this and referee 7 E1. The row now reads "for p > c: O_c(N^{E_W(c)+1}) queries, O_c(N^{E_W(c)+4+o(1)}) gates; plus the cost of [ImranIvanyos2023, Thm. 1] for p ≤ c". The caption now says the queries and gates for p ≤ c "are added separately and are not included in the stated bounds". The regimes table is now `\footnotesize`, because the added text made it too large for the page (by 80pt).
* **E4: skipped (false positive).** `references.bib` FIMSS2014 already reads "Hidden Translation and Translating Coset in Quantum Computing", SIAM J. Comput. 43(1):1–24, 2014, doi:10.1137/130907203, arXiv:quant-ph/0211091. The referee confused it with the next entry.
* **G1: modified.** The required part was added to the total-time sentence of main.tex thm:bb-envelope, in the appendix's own form: "provided the degree of the normal-form arithmetic of the normalizer steps is at most the exponent of the total time stated next (Proposition prop:tb-count-gates)". The optional Howell-form discharge (O(ℓ⁸)) was not adopted. It is a possible follow-up, and it needs an independent check of the O(m⁵) kernel cost first.
* **G2: applied.** The unconditional N-forms were rechecked: s^cℓ² ≤ N^{max(c,2)}, dℓ ≤ c·s^cℓ ≤ cN^c and log(16ℓkd/ε) = O_c(N). Both insertions were made in the Exponents paragraph.
* **G3: applied.** The bound was rechecked: n_p b_M ≤ 2e_pℓ ≤ 2ℓ², so n_p²b_M log p ≤ 2ℓ³.
* **I1: applied.**
* **I2: applied.**
* **I3: modified.** The new split sentence keeps the symbols the table uses, as ε_pre = ε/4 and ε_small = ε/4. The kernel and recursion rows are as proposed. The e = 1 and (R1) rows say "not used in Thm. 7.2", shortened to fit the column.
* **I4: modified.** main.tex is as proposed. The appendix sentence is hedged, because the Imran–Ivanyos model could not be checked offline: "and, if that model's multiplication is the in-place |x,y⟩ ↦ |x,xy⟩, that one too: …". The construction was checked: |x,y,0⟩ → |x,y,xy⟩ → XOR x^{-1}(xy) into y → |x,0,xy⟩ → swap.
* **I5: applied** (appendix item (b) and main.tex (iii)).
* **I6: applied.** All keys exist in references.bib.
* **I7: skipped.** It proposes no text change. The citations are left for a human check, as listed.
* **S1: applied.** The Howell conditions were renamed (HF1)/(HF2) at all four places.
* **S2: applied.** Khukhro is cited by key, and the header comment is trimmed to the keys still missing.
* **S3: applied.**
* **S4: applied.**
