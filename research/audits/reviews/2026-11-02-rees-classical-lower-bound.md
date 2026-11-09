# Rees full campaign 2, item 9: classical query lower bound and the query separation

Date: 2026-11-02. AI session only; no human has read this. Status of every claim:
AI-checked, pending human review. No claim gate was touched; `speedup_claim_allowed`
stays false everywhere.

Artifacts (all in `2026-11-02-rees-classical-lower-bound/`):

- `classical_lb.py` → `classical_lb.json`, `classical_lb.out`: the exact checks
  (structure, lower bound, birthday upper bound, Monte Carlo, base-K counts,
  quantum/classical comparison).
- `birthday_crossover.py` → `birthday_crossover.json`: where the classical birthday
  algorithm uses fewer queries than the paper's Schedule-1 count, plus the line-case
  constant.
- `fil4_local_search.py` → `fil4_local_search.json` / `.out`: the order-625 group.
- `proposed_paper_text.tex`, `proposed_references.bib`: the paper text below, in
  files. It was test-compiled into a scratch copy of the current `main.tex`
  (inserted before `\section{Mechanical Verification ...}`) with no new errors,
  overfull boxes or undefined references. The only undefined reference in that
  build, `thm:bb-envelope`, is already in `main.tex`.
- `refs/`: full texts read (arXiv PDFs plus `pdftotext`), listed in Section 2.

## 1. Summary

**Statement (proved; the proof is standard).** Take the oracle model of `main.tex`
Def. `def:input-contract`: explicit Lie algebra `L ≅ F_p^m` of class `c < p`, a hiding
function with arbitrary labels, and arbitrary `H`. Any classical randomized algorithm
that returns `log H` with probability at least `1-δ` for every `H` (δ < 1/2) makes `q`
queries with

    C(q,2) ≥ (1-δ)·(p^m-1)/(p-1) - 1,   hence   q > sqrt(2(1-δ)·p^(m-1)).

- This holds already for `H` promised to be **non-normal** of order `p` (with
  `(p^m-p^z)/(p-1) ≥ p^(m-2)(p+1)` in place of `(p^m-1)/(p-1)`, where `z = dim Z(L)`).
- It holds in a size form: for every ideal `k` with `dim k ≤ m-2`, identifying `H ⊃ exp k`
  with `[H:exp k] = p` needs `q > sqrt(2(1-δ)|G|/|H|)`.
- The nonadaptive birthday algorithm matches the bound. It uses
  `Q = 5(m+t) + 16⌈ℓ⌉ + ⌈sqrt(2 p^(m-1) max(2t+2, 8ℓ))⌉` queries, where
  `t = ⌈log_p(2/ε)⌉` and `ℓ = ln(2/ε)`, and finds every `H` with probability at least
  `1-ε`.

So the classical randomized query complexity is **Θ(p^((m-1)/2))** for fixed δ. The
constants depend only on δ, not on `c` or on the structure constants.

**Separation (conditional on Theorem `thm:main`; queries only).** Schedule 1 makes
`Q_q = c(m+t)∏_{d=2}^c B_d(g_d)` queries, with `t = ⌈log_p(3/ε)⌉`. This count does not
depend on `p` once `p ≥ 3/ε`, and it is `poly_c(m)`. The classical/quantum query ratio
is therefore at least `p^((m-1)/2)/poly_c(m) = 2^Ω(m log p)` whenever `m ≥ 2` and
`p^(m-1) → ∞`. Three limits apply:

- (a) A query separation itself is **not new**: Ettinger–Høyer–Knill already gives
  `O(log²|G| + log 1/ε)` quantum queries for every group, with exponential-time
  processing.
- (b) The constants are huge. At δ = ε = 1/3, the lower bound exceeds `Q_q` only for
  `p ≥ 443` (Heisenberg), `p ≥ 997` (Dixmier–Lister), and `p > 2^174.7` for the paper's
  class-9 profile.
- (c) Nothing is said about any explicit `f`.

**Exact computation.** On Heis(F_3), Heis(F_5), Heis(F_7), Fil4(F_5) and the abelian
control F_3^3, the union bound in the lower bound is attained: the exact optimal
classical success against the uniform line prior reaches 2/3 at exactly the predicted
`q`. The one unsettled cell is Fil4(F_5) with the non-central prior, where the optimum
is 15 or 16. The birthday algorithm's exact worst case is always an order-`p` subgroup, and its
exact minimum `Q` is within a factor 1.2–1.3 of the lower bound.

## 2. Literature: full texts read, and what each gives

| Reference | Read | What is used |
|---|---|---|
| Ettinger, Høyer, Knill, IPL 91(1):43–48 (2004), arXiv:quant-ph/0401083 (`refs/quant-ph_0401083.txt`) | full text | Thm 1: exact algorithm, `O(log⁴|G|)` queries, outputs a generating set. Thm 2: `Prob[H|H] ≥ 1 - 4r/2^(s/2)` with `r` subgroups and `s` queries, so `s = Θ(log²|G| + log 1/ε)` gives bounded error. Exponential-time processing (intro, p. 2). |
| Childs, *Lecture Notes on Quantum Algorithms*, version of 17 Apr 2025 (`refs/childs_qa.txt`) | full text | §5.3, Thm 5.1: if `G` has `N` subgroups meeting only in the identity, a deterministic algorithm needs `Ω(√N)` queries (`t(t-1) ≥ N`). The randomized adaptation is only remarked. §10.3, eq. (10.10): `k ≥ 2(log N - log ε)/log(1/max F)` copies, with `F ≤ 1/√2`. |
| Ye, Huang, Li, Wang, *Query complexity of generalized Simon's problem*, Inf. Comput. 104790 (2021), arXiv:1907.07367 (`refs/1907.07367.txt`) | full text | Thm 1: randomized `Ω(max{k, √(p^(n-k))})` for GSP(p,n,k) over `Z_p^n`. Lemma 1 is the same collision argument with a random rank-`k` subgroup. Claims 1–2: `Pr[e ∈ S] = (p^k-1)/(p^n-1)`. This is our class-1 case. |
| Nayak, *Deterministic algorithms for the HSP*, QIC 22(9&10):755–769 (2022), arXiv:2104.14436 (`refs/2104.14436.txt`) | full text | §1: Simon's classical bound, and the basic randomized birthday algorithm `O(√(n/m))` for known `|H|`. Cor 4.2: deterministic `2⌈√(n ln n)⌉` queries for any group. Thm 5.2. |
| Ye, Li, *Deterministic algorithms for the HSP*, Inf. Comput. 104975 (2022), arXiv:2110.00827 (`refs/2110.00827.txt`) | full text | Thm 3: deterministic `Ω(log|ℋ| / log(|G|/|H|))` for identification. Context only. |
| Ye, Li, *Sample complexity of HSP*, arXiv:2107.02987 (`refs/2107.02987.txt`) | full text | Context: classical sample-model bounds. It credits Childs for the `Ω(√N)` trivially-intersecting bound. Not used. |
| Wu, Qiu, Tan, Li, Cai, arXiv:1905.08549 (`refs/1905.08549.txt`) | skimmed | Exact quantum GSP bounds. Not used. |
| Simon, SIAM J. Comput. 26(5):1474–1483 (1997) | **not fetched** | Cited for the original collision argument. Its statement is taken from Nayak §1, who notes the printed bound is `Ω(2^(k/4))` at error `1/2 - 2^(-k/2)`, and `2^(k/2-1)` at error 1/4. |

## 3. The results and proofs

The full proofs are in the "Proposed paper text" below (Lemma `lem:collision`,
Proposition `prop:classical-query`). Here is what each step rests on.

**Lemma (collision bound, relative to a base subgroup K).** *Proved; standard.* Take a
prior μ on subgroups `H > K`, let `ρ = max_{g∉K} Pr[g ∈ H]` and `π = max μ(H)`.
Identification gives `C(q,2)ρ ≥ 1-δ-π`. Deciding `K` against `supp μ` gives
`C(q,2)ρ ≥ 1-2δ`.

The proof couples lazily sampled oracles for `K` and for `H`, using the same coins and
the same fresh labels. The two runs agree until some `x_i^{-1}x_j ∈ H \ K`. The base
subgroup `K` is the only change from Childs Thm 5.1 and Ye et al. Lemma 1; it gives the
size form and the normal/non-normal splits.

**Structure facts.** *Proved; elementary.*

- `c < p` gives exponent `p`. The order-`p` subgroups are the `exp(F_p v)`, and each
  `g ≠ 1` lies in exactly one of them.
- An order-`p` subgroup is normal exactly when it is central. A nonabelian `L` has
  `z ≤ m-2`.
- For an ideal `k`, the index-`p` overgroups of `exp k` are the `exp(k + F_p v)`, and
  each `g ∉ exp k` lies in exactly one. There are `(p^(m-k)-1)/(p-1)` of them, and
  `(p^(z_k)-1)/(p-1)` of them are normal, where `z_k = dim Z(L/k)`.

The script checks these on five groups (`classical_lb.json` → `structure`,
`base_K`). It checks every element for exponent `p`, every line for being a subgroup,
normal ⇔ central for every line, and every overgroup count against the formula.

**Upper bound (birthday).** *Proved.* The output is always contained in `𝔥`. Group
the queries by left coset of `H`. The `e = Q − #cosets` ratios to the first point of
each coset are iid uniform on `H`. The Burnside basis theorem then bounds the
generation failure by `p^(-t)/(p-1)`. The occupancy lower tail `Pr[e < k+t]` is
dominated by a Bernoulli sum, and the Chernoff bound `exp(-μ/8)` applies. One `Q`
works for every `k`, because `p^(m-k) max(2(k+t), 8ℓ)` is non-increasing in `k`.

Remaining classical work is `poly(Q, m, log p)` for fixed `c`. This is BCH for the
differences, a sort for the labels, and Lie closure plus Gaussian elimination, using
the Lazard subgroup correspondence `⟨exp S⟩ = exp(Lie(S))`.

**What is new.** Little.

- The lemma is Simon's argument (Childs Thm 5.1 deterministic; Ye et al. Lemma 1
  randomized, abelian). The birthday algorithm is folklore (Nayak §1).
- Only the following is specific to this setting: for groups of exponent `p`, the
  worst case is an order-`p` subgroup. This gives a tight `Θ(p^((m-1)/2))` for
  identifying **arbitrary** `H` (including non-normal `H`), with explicit constants
  and the base-`K` size form.
- The bound uses nothing beyond "exponent `p`, order `p^m`" and Lazard's subgroup
  correspondence. So the explicit structure constants give a classical algorithm no
  query advantage. The bound is identical for every `L`, including the abelian one,
  where it is Ye et al. Thm 1 at `k = 1`.
- The paper should present this as a standard proposition, not a contribution.

**Normal H.** Lower bounds are only `√(p^(z_k-1))`-type (part (iii)). For
Heisenberg, `z = 1` gives nothing from central lines. The base `K = Z` gives
`Ω(√p)`, since the `p+1` planes through the center are normal. No matching upper bound
is claimed for the normal-only promise.

## 4. Contrast with the quantum bound

**Paper count.** Sources per terminal sample are `∏ B_d(g_d)`, at `c` queries each,
with `m + t` terminal samples and `t = ⌈log_p(3/ε)⌉` (`main.tex`
`sec:recursion`). This gives `Q_q = c(m+t)∏_{d=2}^c B_d(g_d)`. The script reproduces
the class-9 profile's `ceil(log2) = 1573` from `rees_hsp_reduction.json` exactly
(`class9_ceil_log2_check`).

**EHK / Barnum–Knill information bound.**
`⌈4 log2(r/ε)⌉ ≈ m² log2 p` copies, where `r` is the number of subspaces of `F_p^m`.
This is the "copies" column of the table below.

Crossovers at δ = ε = 1/3 (exact integer arithmetic; `classical_lb.json` →
`comparison`, `birthday_crossover.json`):

| family | c | m | g_2..g_c | log2 Q_q | LB > Q_q from p = | birthday < Q_q for p < | EHK-type copies at crossover |
|---|---|---|---|---|---|---|---|
| Heisenberg | 2 | 3 | 1 | 9.00 | 443 | 84 | 81 |
| filiform | 3 | 4 | 2,1 | 27.76 | 337,853 | 119,671 | 301 |
| free 2-gen class 3 | 3 | 5 | 3,2 | 33.19 | 92,107 | 42,290 | 407 |
| Dixmier–Lister | 3 | 8 | 4,2 | 35.06 | 997 | 638 | 644 |
| class-9 profile | 9 | 19 | 17,16,14,12,9,6,3,1 | 1572.66 | 2^174.72 | 2^174.47 | 62,909 |

Reading the table:

- Between the two thresholds, neither the lower bound nor the proved birthday
  constant decides which side wins.
- The asymptotic birthday constant for a line is `√(2 ln 3) ≈ 1.48` against the lower
  bound's `√(4/3) ≈ 1.15` (`birthday_crossover.json`, `line_case_constant`; the ratio
  is 1.4836 at p = 1009). So the true crossover is close to the "LB" column.
- At the paper's own reference profile (class 9, `m = 19`), the stated quantum bound
  gives a query advantage only for `p > 2^174.7`. At a 61-bit prime it needs about
  `2^1573` queries, while the classical lower bound and the birthday algorithm are both about `2^550`.

The separation statement is in Remark `rem:query-separation` below, with limits
(a)–(c).

## 5. Exact computations

All rows are exact unless marked "float". `classical_lb.py` asserts the
upper-bound validity, the Monte Carlo agreement and the overgroup counts, and exits 0.

**Lower bound constant (exact).** The best deterministic `q`-query success against a
uniform prior on lines is exactly `(cov*(q)+1)/N`. Here `cov*(q)` is the maximum, over
`q`-point sets, of the number of prior lines that contain some `log(x^{-1}x')`. The
reason: until a collision the transcript is fresh labels independent of `H`, and a
collision reveals a line exactly. The union bound is `cov* ≤ C(q,2)`.

| group | prior | N | lines needed for 2/3 | q from bound | exact q_min | how |
|---|---|---|---|---|---|---|
| F_3^3 (class 1 control) | all lines | 13 | 8 | 5 | 5 | exhaustive cov*(2..5) = 1,3,6,10 |
| Heis(F_3) | all lines | 13 | 8 | 5 | 5 | exhaustive, same values |
| Heis(F_3) | non-central | 12 | 7 | 5 | 5 | exhaustive |
| Heis(F_5) | all / non-central | 31 / 30 | 20 / 19 | 7 | 7 | exhibited 7-set, 21 = C(7,2) lines |
| Heis(F_7) | all / non-central | 57 / 56 | 37 | 10 | 10 | exhibited 10-set, 44 lines |
| Fil4(F_5) | all lines | 156 | 103 | 15 | 15 | exhibited 15-set, 103 lines (`fil4_local_search.json`) |
| Fil4(F_5) | non-central | 155 | 103 | 15 | 15 or 16 | swap search: 102 lines at q = 15, 104 at q = 16; not settled |

So the lower bound's constant is attained in every cell that was settled. One cell is open: Fil4(F_5) with the non-central prior, by at most one query. Structured
"line-Sidon" query sets beat random sampling: Heis(F_3) needs 5 structured queries,
but 6 random ones.

**Birthday upper bound (exact rational occupancy law × Burnside generation
probability, over every subgroup type `(k, d(H))` from a full subalgebra census).**

| group | subgroups | exact min Q, worst-case success ≥ 2/3 | worst type | closed-form Q(1/3) | exact worst success at closed form |
|---|---|---|---|---|---|
| F_3^3 | 28 | 6 | order p | 74 | 1.0 |
| Heis(F_3) | 19 | 6 | order p | 74 | 1.0 |
| Heis(F_5) | 39 | 9 | order p | 84 | 1.0 |
| Heis(F_7) | 67 | 12 | order p | 90 | 1.0 |
| Fil4(F_5) | 220 | 19 | order p | 122 | 1.0 |

- The closed form is valid but loose at small sizes, because of its additive terms.
- Asymptotically the line case needs `1.4836·√(p^(m-1))` at `p = 1009`, against the
  limit `√(2 ln 3) = 1.4823`.
- The subalgebra census includes 55 non-normal 2-dimensional subgroups in Fil4(F_5).

**Monte Carlo (float check).** The real birthday algorithm was run on the BCH groups
Heis(F_3), Heis(F_5) and Fil4(F_5): random injective coset labels, Lie closure of the
collision differences, 2000 trials for each of 12 subgroups (normal and non-normal,
orders `p` and `p²`). Every observed success rate agrees with the exact law within
4σ (e.g. Fil4(F_5), order `p`: exact 0.6765, observed 0.6885 and 0.693).

## 6. Exact statement that now holds

- **Proved (standard; AI-checked, pending human review).** This is Proposition
  `prop:classical-query`(i)–(v) as written below. In the oracle model of Def.
  `def:input-contract`, for every `L` with `m ≥ 2`: classical randomized query
  complexity for error δ ∈ (0, 1/2) is between `sqrt(2(1-δ)p^(m-1))` and
  `O(sqrt(p^(m-1) log(1/δ)) + m)`. This holds for arbitrary `H`, already under the
  non-normal order-`p` promise. The size form over an ideal is
  `q > sqrt(2(1-δ)|G|/|H|)`.
- **Conditional on Theorem `thm:main` (AI-checked only).** The quantum query count is
  `poly_c(m)` and does not depend on `p` once `p ≥ 3/ε`. This gives a
  `2^Ω(m log p)` **query** separation, and in the oracle model also a time
  separation. It is not a separation for any explicit `f`.
- **Exact computation.** The lower bound's union-bound constant is attained in nine
  of the ten (group, prior) cells; Fil4(F_5) with the non-central prior is within one
  query. The birthday algorithm's exact worst case is an order-`p` subgroup on all
  five. The crossover primes are in the table above.

## 7. What is still missing

- **Normal-H promise.** No matching upper bound, and no general lower bound beyond the
  `√(p^(z_k-1))` family.
- **Size-sensitive decision lower bound.** "Trivial vs `|H| = p^k`" for `k ≥ 2` and
  general `L` is not settled. The upper bound is `O(√(p^(m-k)))`. A lower bound needs a
  prior on order-`p^k` subgroups with `ρ ≈ p^(k-m)`. Uniform `k`-subspaces of an abelian
  subalgebra of dimension `a` give only `√(p^(a-k))`. Not needed for the worst-case
  separation.
- **Copy input.** A classical analogue of copy input, i.e. random samples
  `(x, f(x))`, is not treated. Ye–Li 2107.02987 covers the abelian sample model.
- **Simon 1997.** Not fetched in full text; cited through Nayak §1 and Childs §5.3.
- **Fil4(F_5) non-central prior.** `q_min ∈ {15, 16}` is not settled. A 240 s swap
  search found 102 of the 103 lines needed at q = 15. An exhaustive search over
  15-subsets of 625 points is out of reach.
- **Human review.** No human has checked any of this.

## 8. Claim gates that must stay false

`speedup_claim_allowed` (`rees_hsp_reduction.json` and every Rees JSON), every Rees
claim gate, and any "quantum advantage" or "application" flag. The separation is a
relativized query statement. Its quantum side is conditional on Theorem `thm:main`.
The application search was negative.

## 9. Proposed paper text

**Target 1.** A new subsection at the end of Section `sec:classical-landscape`,
after Remark `rem:filters` and before `\section{Mechanical Verification in Lean 4 and
Reproducibility}`. The exact LaTeX is `2026-11-02-rees-classical-lower-bound/proposed_paper_text.tex`
(test-compiled against the current `main.tex`). It contains Lemma `lem:collision`,
Proposition `prop:classical-query` with proof, Table `tab:query-crossover` and Remark
`rem:query-separation`. Status label: AI-checked, pending human review.

**Target 2.** One sentence after Theorem `thm:main` (after the paragraph "The proofs
below are the project's proposed justification..."):

```latex
In the same oracle model, every classical randomized algorithm needs more than $\sqrt{2(1-\delta)\,p^{m-1}}$ queries to succeed with probability $1-\delta$, even for non-normal $H$ of order $p$, and $O(p^{(m-1)/2})$ queries suffice (Proposition~\ref{prop:classical-query}). The resulting separation concerns queries only and is conditional on Theorem~\ref{thm:main}; see Remark~\ref{rem:query-separation} for its limits.
```

**Bibliography.** Add the five entries in `proposed_references.bib`: `Simon1997`,
`EttingerHoyerKnill2004`, `ChildsQA`, `YeHuangLiWang2021`, `Nayak2022`. Their
journal data were taken from the arXiv records, except Simon's, which comes from
Childs' bibliography.

The LaTeX of Target 1, verbatim:

```latex
% Proposed paper text for main.tex (item 9, 2026-11-02-rees-classical-lower-bound.md).
% Target: a new subsection at the end of Section~\ref{sec:classical-landscape},
% after Remark~\ref{rem:filters} and before \section{Mechanical Verification ...}.
% Status: AI-checked, pending human review. Bibliography entries are in
% proposed_references.bib in this folder.

\subsection{Classical Query Complexity and the Query Separation}
\label{sec:classical-query}

This subsection states what classical algorithms cannot do in the oracle model of Definition~\ref{def:input-contract}. A \emph{classical query algorithm} receives $p$ and the structure constants of $\mathcal{L}$, so it knows the group law, and evaluates the hiding function $f$ at points of $G$ of its choice. Its cost is the number of evaluations; all other computation is free. It \emph{solves the HSP with error $\delta$} if, for every subgroup $H$ and every function $f$ hiding $H$, it outputs $\hh$ with probability at least $1-\delta$. The label set has at least $|G|$ elements. Coset-copy input has no classical counterpart and is not treated here. Write $N_1 = (p^m-1)/(p-1)$ and $z = \dim Z(\mathcal{L})$.

\begin{lemma}[Collision bound]
\label{lem:collision}
Let $K \le G$, and let $\mu$ be a probability distribution on subgroups $H$ with $K < H \le G$. Put $\rho = \max_{g \in G\setminus K}\Pr_{H\sim\mu}[g\in H]$ and $\pi = \max_H \mu(H)$. Consider a classical randomized algorithm that is told $K$ and makes $q$ queries.
\begin{enumerate}[label=(\roman*),leftmargin=2em]
  \item If it outputs $H$ with probability at least $1-\delta$ for every $H$ in the support of $\mu$, then $\binom{q}{2}\rho \ge 1-\delta-\pi$.
  \item If it decides whether the hidden subgroup is $K$ or lies in the support of $\mu$, with error at most $\delta$ in each case, then $\binom{q}{2}\rho \ge 1-2\delta$.
\end{enumerate}
\end{lemma}

\begin{proof}
For a subgroup $J$, let $O_J$ answer queries by lazy sampling: a point in a left coset of $J$ queried before gets that coset's label, and a point in a new coset gets a label drawn uniformly from the labels not yet used. This realizes a uniformly random injective labelling of $G/J$, so $O_J$ hides $J$, and a bound for these random labellings is a bound for the worst case. Run the algorithm against $O_K$ and against $O_H$ with the same coins and the same stream of fresh labels. The two runs agree until the first query $x_j$ that lies in a new left coset of $K$ but in a previously visited left coset of $H$, that is, until $x_i^{-1}x_j \in H\setminus K$ for some $i<j$. Let $x_1,\dots,x_q$ be the queries of the run against $O_K$. Their law does not depend on $H$, so for $H\sim\mu$ drawn independently,
\[
  \Pr[\text{the runs differ}] \le \sum_{i<j}\Pr_{H\sim\mu}\bigl[x_i^{-1}x_j \in H\setminus K\bigr] \le \binom{q}{2}\rho .
\]
For~(i), the run against $O_H$ outputs $H$ only if the runs differ or the run against $O_K$ outputs $H$. The latter output does not depend on $H$, so averaging over $\mu$ gives $1-\delta \le \binom q2\rho + \pi$. For~(ii), the run against $O_H$ answers ``not $K$'' with probability at least $1-\delta$, and the run against $O_K$ does so with probability at most $\delta$, so the runs differ with probability at least $1-2\delta$.
\end{proof}

This is Simon's collision argument~\cite{Simon1997}. Childs proves the deterministic form for $N$ subgroups that meet only in the identity~\cite[Theorem~5.1]{ChildsQA}, and Ye, Huang, Li and Wang prove the randomized form for $\mathbb{Z}_p^n$~\cite[Lemma~1]{YeHuangLiWang2021}. Only the instantiation below is specific to the present setting.

\begin{proposition}[Classical query complexity]
\label{prop:classical-query}
Let $\mathcal{L}$ be as in Definition~\ref{def:input-contract} with $m \ge 2$, and let $0 \le \delta < 1/2$.
\begin{enumerate}[label=(\roman*),leftmargin=2em]
  \item Every classical query algorithm that solves the HSP with error $\delta$ makes $q$ queries with $\binom q2 \ge (1-\delta)N_1 - 1$, hence $q > \sqrt{2(1-\delta)\,p^{m-1}}$. This holds already under the promise $|H| = p$.
  \item If $\mathcal{L}$ is not abelian, the bound of~(i) holds under the promise that $H$ is a non-normal subgroup of order $p$, with $N_1$ replaced by $(p^m-p^z)/(p-1) \ge p^{m-2}(p+1)$.
  \item Let $\mathfrak{k}$ be an ideal of dimension $k \le m-2$ and $K = \exp\mathfrak{k}$. An algorithm that is told $K$ and promised $K < H$ with $[H:K] = p$ still needs $\binom q2 \ge (1-\delta)(p^{m-k}-1)/(p-1) - 1$, hence $q > \sqrt{2(1-\delta)\,|G|/|H|}$. Under the further promise that $H$ is normal, the same holds with $p^{m-k}$ replaced by $p^{z_k}$ when $z_k \coloneqq \dim Z(\mathcal{L}/\mathfrak{k}) \ge 2$.
  \item Deciding whether $H = 1$ or $|H| = p$, with error at most $\delta$ in each case, needs $\binom q2 \ge (1-2\delta)N_1$.
  \item Conversely, let $0<\eps<1$, $t = \lceil\log_p(2/\eps)\rceil$, $\ell = \ln(2/\eps)$ and
  \[
    Q = 5(m+t) + 16\lceil \ell\rceil + \Bigl\lceil\sqrt{2p^{m-1}\max(2t+2,\,8\ell)}\,\Bigr\rceil .
  \]
  Query $Q$ independent uniform points $x_1,\dots,x_Q$. For each label value, let $x_a$ be the first point with that label, and output the Lie subalgebra generated by the vectors $\log(x_a^{-1}x_i)$ over all later points $x_i$ with the same label. The output is always contained in $\hh$, and it equals $\hh$ with probability at least $1-\eps$, for every $H$. For fixed $c$, the remaining work is $\poly(Q, m, \log p)$.
\end{enumerate}
In particular, for fixed $\delta \in (0,1/2)$ the classical randomized query complexity of the HSP in $G$ is $\Theta(p^{(m-1)/2})$. The implied constants depend only on $\delta$; they do not depend on $c$ or on the structure constants of $\mathcal{L}$.
\end{proposition}

\begin{proof}
Since $c<p$, the elements $\exp(sx)$, $s\in\Fp$, commute and $\exp(sx)\exp(s'x) = \exp((s+s')x)$. So $G$ has exponent $p$, the subgroups of order $p$ are the sets $\exp(\Fp v)$ with $v \ne 0$, and each $g \ne 1$ lies in exactly one of them. For a subgroup $J$ with $\log J = \mathfrak{j}$, the group $Z(G)$ is $\exp Z(\mathcal{L})$ and $J$ is normal exactly when $\mathfrak{j}$ is an ideal, by the Lazard correspondence.

(i) Take $K = 1$ and $\mu$ uniform on the $N_1$ subgroups of order $p$, so $\rho = \pi = 1/N_1$. Lemma~\ref{lem:collision}(i) gives $\binom q2 \ge (1-\delta)N_1 - 1$. This forces $q \ge 2$, because $N_1 \ge 3$ and $\delta < 1/2$. Since $N_1 \ge p^{m-1}+1$, we get $q^2 = q(q-1) + q \ge 2(1-\delta)p^{m-1} - 2\delta + q > 2(1-\delta)p^{m-1}$.

(ii) A normal subgroup of order $p$ of a $p$-group meets the centre nontrivially, so it is central. Hence the non-normal subgroups of order $p$ are the $\exp(\Fp v)$ with $v \notin Z(\mathcal{L})$. There are $(p^m-p^z)/(p-1)$ of them, and a nonabelian $\mathcal{L}$ has $z \le m-2$, since $\dim \mathcal{L}/Z(\mathcal{L}) = 1$ would make $\mathcal{L}$ abelian. Take $\mu$ uniform on them. A central $g$ lies in none of them, and any other $g\neq 1$ lies in exactly one, so $\rho = \pi = (p-1)/(p^m-p^z)$. The arithmetic of~(i) applies, since $p^{m-2}(p+1) \ge p^{m-1}+1$.

(iii) The subgroups $H$ with $K<H$ and $[H:K]=p$ are the $\exp(\mathfrak{k}+\Fp v)$ with $v\notin\mathfrak{k}$. Each $\mathfrak{k}+\Fp v$ is a subalgebra because $\mathfrak{k}$ is an ideal, and there are $(p^{m-k}-1)/(p-1)$ of them. Each $g \notin K$ lies in exactly one, namely $\exp(\mathfrak{k} + \Fp\log g)$. Take $\mu$ uniform; then $\rho=\pi=(p-1)/(p^{m-k}-1)$, and~(i) applies with $m$ replaced by $m-k$ and $p^{m-k-1} = |G|/|H|$. Such an $H$ is normal exactly when $(\mathfrak{k}+\Fp v)/\mathfrak{k}$ is an ideal of $\mathcal{L}/\mathfrak{k}$. A one-dimensional ideal of a nilpotent Lie algebra is central, so there are $(p^{z_k}-1)/(p-1)$ normal choices. Each $g\notin K$ lies in at most one of them, so again $\rho=\pi$ is one over their number.

(iv) This is Lemma~\ref{lem:collision}(ii) with the $\mu$ of~(i).

(v) Equal labels $f(x_a) = f(x_i)$ give $x_a^{-1}x_i \in H$, so every generator lies in the subalgebra $\hh$, and so does the output. If $H = 1$, the output is $0 = \hh$. Let $|H| = p^k$ with $k\ge 1$, and let $M = p^{m-k}$ be the number of left cosets. Write $x_i = r_ih_i$ with $r_i$ in a fixed transversal and $h_i\in H$. For uniform $x_i$, the pair $(r_i,h_i)$ is uniform, and $h_i$ is independent of $r_i$. Let $D$ be the number of cosets visited and $e = Q-D$. The $e$ elements $x_a^{-1}x_i = h_a^{-1}h_i$, one for each non-first point $x_i$ of each visited coset, are independent and uniform on $H$, given the coset pattern. By the Lazard correspondence the output contains the logarithm of the subgroup they generate. By the Burnside basis theorem, $e$ uniform elements fail to generate $H$ only if their images in $H/\Phi(H)\cong\Fp^{d}$, $d\le k$, lie in a hyperplane. This has probability at most $\frac{p^d-1}{p-1}p^{-e} < p^{d-e}/(p-1)$. With $s = k+t$, the failure probability is therefore at most $\Pr[e<s] + p^{-t}/(p-1) \le \Pr[e<s] + \eps/2$.

Let $Y_j = 1$ if $x_j$ lands in an already visited coset. Given the past, $\Pr[Y_j = 1] = D_{j-1}/M$ with $D_{j-1} = j-1-e_{j-1}$. Realize $Y_j = [U_j < D_{j-1}/M]$ with independent uniform $U_j \in [0,1]$. On the event $e < s$, every $j$ has $D_{j-1} \ge j-s$, so $e \ge X \coloneqq \sum_j [U_j < \min(1,(j-s)^+/M)]$. Here $X$ is a sum of independent Bernoulli variables with mean $\mu_X = \sum_{i=1}^{Q-s}\min(1,i/M)$. The Chernoff bound $\Pr[X \le \mu_X/2] \le e^{-\mu_X/8}$ gives $\Pr[e<s] \le \eps/2$ as soon as $\mu_X \ge \max(2s, 8\ell)$. Put $\Phi = p^{m-1}\max(2t+2,8\ell)$. Since $s\le m+t$, we have $Q-s \ge 4(m+t) + 16\ell + \sqrt{2\Phi}$. If $Q-s \le M$, then $\mu_X \ge (Q-s)^2/(2M) \ge p^{k-1}\max(2t+2,8\ell) \ge \max(2s,8\ell)$, using $p^{k-1}(t+1) \ge k(t+1) \ge k+t$. If $Q-s > M$, then $\mu_X \ge (Q-s)-M/2 \ge (Q-s)/2 \ge \max(2s,8\ell)$. So the total failure probability is at most $\eps$.

For fixed $c$, each $\log(x_a^{-1}x_i) = \BCH(-x_a,x_i)$ costs a bounded number of brackets. Grouping equal labels is a sort, and the subalgebra generated by at most $Q$ vectors is reached after at most $m$ rounds of bracketing and Gaussian elimination. The $\Theta$ statement combines~(i) at error $\delta$ with~(v) at $\eps = \delta$, using $m \le 2p^{(m-1)/2}$ for $p\ge 2$.
\end{proof}

The upper bound~(v) is the standard birthday algorithm~\cite[Section~1]{Nayak2022}, with explicit constants. For comparison, Nayak's deterministic algorithm for arbitrary finite groups uses at most $2\lceil\sqrt{|G|\ln|G|}\,\rceil$ queries~\cite[Corollary~4.2]{Nayak2022}, here $2\lceil\sqrt{p^m m\ln p}\,\rceil$, larger than~(v) by a factor of order $\sqrt{p\,m\log p}$. For $m=1$ the problem is trivial: $G = \Fp$ has two subgroups, and two queries suffice.

\begin{table}[htbp]
\centering
\caption{Query counts at $\delta = \eps = 1/3$ and $p \ge 11$, where $t = 1$. Here $Q_{\mathrm q}$ is the Schedule~1 count $c(m+t)\prod_{d=2}^c B_d(g_d)$ of Remark~\ref{rem:query-separation}. The column ``$\mathrm{LB} > Q_{\mathrm q}$'' gives the smallest prime $p$ at which the bound $\binom q2 \ge \frac23 N_1 - 1$ of Proposition~\ref{prop:classical-query}(i) forces more than $Q_{\mathrm q}$ classical queries. For $p$ below the value in the next column, the classical algorithm of Proposition~\ref{prop:classical-query}(v) uses fewer than $Q_{\mathrm q}$ queries. The last column is the information-theoretic count of copies of $\rho_H$, $\lceil 4\log_2(3r)\rceil$ of~\cite[Eq.~(10.10)]{ChildsQA}, with $r$ the number of subspaces of $\Fp^m$, at the crossover prime; it has exponential post-processing. Exact computation, \file{research/audits/reviews/2026-11-02-rees-classical-lower-bound/classical_lb.json} and \file{birthday_crossover.json}.}
\label{tab:query-crossover}
\small
\begin{tabular}{@{}lcccrrrr@{}}
\toprule
Family & $c$ & $m$ & $(g_2,\dots,g_c)$ & $\log_2 Q_{\mathrm q}$ & $\mathrm{LB} > Q_{\mathrm q}$ from & (v) $< Q_{\mathrm q}$ for $p <$ & copies \\
\midrule
Heisenberg & 2 & 3 & $(1)$ & $9.00$ & $443$ & $84$ & $81$ \\
filiform & 3 & 4 & $(2,1)$ & $27.76$ & $337{,}853$ & $119{,}671$ & $301$ \\
free, two generators & 3 & 5 & $(3,2)$ & $33.19$ & $92{,}107$ & $42{,}290$ & $407$ \\
Dixmier--Lister & 3 & 8 & $(4,2)$ & $35.06$ & $997$ & $638$ & $644$ \\
class-$\ReesClassNineClass$ profile & 9 & 19 & $(17,16,\dots,1)$ & $1572.66$ & $2^{174.72}$ & $2^{174.47}$ & $62{,}909$ \\
\bottomrule
\end{tabular}
\end{table}

\begin{remark}[The query separation; conditional on Theorem~\ref{thm:main}]
\label{rem:query-separation}
By Section~\ref{sec:recursion}, the procedure of Theorem~\ref{thm:main} under Schedule~1 makes
\[
  Q_{\mathrm q} = c\,(m+t)\prod_{d=2}^c B_d(g_d),
  \qquad t = \lceil\log_p(3/\eps)\rceil ,
\]
oracle queries. This count does not depend on $p$ once $p \ge 3/\eps$, and at fixed $c$ it is polynomial in $m$ with exponent at most $1+\sum_{d=2}^c d\lceil\log_2(d+1)\rceil$. By Proposition~\ref{prop:classical-query}(i) and~(ii), every classical algorithm with error $\delta<1/2$ needs more than $\sqrt{2(1-\delta)p^{m-1}}$ queries, even when $H$ is promised to be non-normal of order $p$. Hence, if Theorem~\ref{thm:main} holds, then for fixed $c$ and every sequence of instances with $m\ge2$ and $p^{m-1}\to\infty$, the ratio of classical to quantum query complexity is at least $p^{(m-1)/2}/\poly_c(m)$. In the input length $n = m\log_2 p$ this is $2^{\Omega(n)}$, both for $p\to\infty$ at fixed $m$ and for $m\to\infty$ at fixed $p$. Three limits apply.
\begin{enumerate}[label=(\alph*),leftmargin=2em]
  \item A query separation by itself is not new. Ettinger, H{\o}yer and Knill determine $H$ in any finite group with $O(\log^2|G| + \log(1/\eps))$ queries~\cite[Theorem~2]{EttingerHoyerKnill2004}, here $O(m^2\log^2 p + \log(1/\eps))$, but with exponential-time processing. Theorem~\ref{thm:main}, if correct, adds polynomial running time at polynomially many queries; it does not lower the query count, and its Schedule~1 count is far above the information-theoretic one (Table~\ref{tab:query-crossover}).
  \item The constants are large. Below the crossover primes of Table~\ref{tab:query-crossover}, the stated quantum bound gives no query advantage. For the class-$\ReesClassNineClass$ profile of Section~\ref{sec:uniform-compilation}, an advantage needs $p > 2^{174.7}$.
  \item The separation concerns queries to an oracle with arbitrary labels. In this model a query lower bound also bounds classical running time from below. It says nothing about any explicitly given $f$, and we know no explicit family of hiding functions on which classical algorithms stay slow (see the start of this section). We claim no speedup for any concrete problem.
\end{enumerate}
\end{remark}
```
