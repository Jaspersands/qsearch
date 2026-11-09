# Adversarial check and integration: Rees SDE below quadratic arity

5 November 2026 (run on 4 Nov evening). AI-only pass: one Claude Code session acting as
adversarial checker and then as integrator of one remark. Input:
`2026-11-05-rees-sde-subquadratic.md` (the "report"), its folder of scripts and `lit/`. This is
not human review and not Lean. Everything below and in the inserted remark is **AI-checked,
pending human review.** No git state was changed, nothing was pushed, `make_numbers.py` was not
run, and `research/reductions/rees_hsp_reduction.json` was not touched.

Every proof was re-derived here without using the report's reasoning, and the finite claims were
re-checked with a new script written from scratch (`2026-11-05-rees-sde-subquadratic-check/indep_check.py`,
no imports from the report's folder; outputs `*.out` in the same folder).

## 1. Verdicts

| # | Claim | Verdict | Fix |
|---|---|---|---|
| 1 | Theorem 1: a circuit modulo U whose dependency δ is not in one coset has no 2-dimensional subspace in R_U(S), under any rule | **Holds** | None to the statement. See 1.1 for the definitions and the role of the coset hypothesis. |
| 1b | Corollary 1: one dimension per circuit; (a+1)(a+2)/2 columns under general position | **Holds with fix** | The proposed remark's hypothesis "no dependency used lies in a single coset" contradicts its own count: the final column of the triangular scheme is itself a circuit with dependency (1), which lies in one coset. Correct form: a scheme that finishes when a set realizes a nonzero-weight element of the current space, and meets no single-coset circuit before F_p^a is realizable, uses at least a(a+3)/2 + 1 columns. Fixed in the inserted text. |
| 2 | Proposition 2: a circuit has a line in R_U(S) iff a C-restricted two-level contraction exists; at C = Z_κ iff p ∉ E_2(κ) | **Holds** | None. A side claim in report §3 fails: "at 71 ≤ p ≤ 181 for κ = 5 every sampled q = 1, 2 circuit has a flexible line" is false at p = 71, q = 2 (8/12 in the report's own `flexline_e2.out`). Correct range: 101 ≤ p ≤ 181 (p = 71 only for q = 1). Not used in the paper. |
| 3 | Exact example: five columns in F_p^3 (2-dimensional relation space) with R = F_p^3 at κ = 2, p ∈ {13, 29} | **Holds** | None. Reproduced 4/4 at both primes with a different seed and a different code path. |
| 4 | Theorem 3: solving every solvable instance at M = a+2 recovers the key of c ↦ χ(K+c); failure ≤ κ^{1−k} + κpκ^{−k}e^{κk/(p−1)} + (p−1)^{1−k} | **Holds with fix** | The bound and the reduction hold (1.4). Fixes to the proposed remark: (i) state the two cases the reduction handles (some K + c_i = 0, all c_i equal); (ii) "every solution has t = K" → "every solution has β ≠ 0 and α/β = K" (β = 0 solutions have no t); (iii) the assumption is not standard (1.5); (iv) the van Dam–Hallgren–Ip algorithm uses superposition queries, and the reduction supplies only classical queries at random points, so the report's "quantumly easy, consistent with the quantum setting" is misleading; (v) the scope (1.6). |
| 4b | Corollary 3 (deciding) | **Holds with fix** | The bound κ^{1−k} + κ(p+1)κ^{−k} is not an upper bound when κk > 1. Correct: κ^{1−k} + κp(1/κ + 1/p)^k + p^{1−k} ≤ κ^{1−k} + κpκ^{−k}e^{κk/p} + p^{1−k}. Not used in the paper. |
| 5 | Proposition 4: at κ = 2, p = 3 the problem is F_3 subset sum; a uniform-in-p o(a²) method would beat every known classical algorithm | **Holds** | None. (F_3^×)^2 = {1}, so weights are in {0, 1}. The KMOSW quotes were checked in `2026-11-02-rees-linear-arity/lit/arxiv_2609.40321.txt` lines 126–141 and 270–290: classical εn² for every ε "seems to require substantially new ideas", and the 0.1022n² algorithm has no complete description or proof. One sentence added to (c). |
| 6 | Proposition 5: isotropic recursion uses 2^{a+1} − 1 variables | **Holds** | None. N(a) = 2N(a−1) + 1, N(1) = 3; a form in n variables, degenerate or not, has a totally isotropic subspace of dimension ⌊(n−1)/2⌋. |
| 7 | (c): best polynomial threshold for underdetermined MQ over odd q is n ≥ m(m+1)/2 (Cheng–Hashimoto–Miura–Takagi) | **Holds as cited** | Read only from the list in §2 of Hashimoto, JSIAM Letters 15 (2023) (`lit/hashimoto_jsiaml2023.txt` lines 183–199; it is not Table 2), not from CHMT. Open point for the human reviewer: through the report's normalisation (fix one linear form, n = M − 1), CHMT would give κ = 2 at M = a(a+1)/2 + 1 < (a+1)(a+2)/2 if it applies to every instance. The title says "a class of" systems, so that is not claimed anywhere. |
| 8 | Lifting through extensions | **Holds** | None (y = g^e is a κ-th power in F_{p^k} iff (κ/gcd(κ,k)) divides e). |
| 9 | Four bib entries | **Consistent; unverified** | See 1.7. All four carry `% NEEDS HUMAN VERIFICATION`. |

### 1.1 Theorem 1: definitions, unbounded rules, the coset hypothesis

- **Definitions.** R_U(S) = {Σ_{i∈S} x_iλ_i + U : x ∈ (P∪{0})^S} ⊆ F_p^a/U. A *flexible direction*
  of S modulo U is a line F_p w (w ≠ 0) with F_p w ⊆ R_U(S): every multiple of w is the value of
  some admissible weights on S, modulo U. U is *realizable* by disjoint sets S_1..S_l if every
  element of U is a value Σ x_iλ_i with admissible weights on their union. If U is realizable and
  V/U ⊆ R_U(S) for a fresh S, then V is realizable (write y = r + u with r realized by S modulo U).
  The inserted remark states both definitions, which the report's proposed text left implicit.
- **Proof re-derived.** W = span of the images, dim W = |S| − 1; H = span of S∖{i,j} has
  dimension |S| − 2 since proper subsets of a circuit are independent. A plane T ⊆ W meets H
  nontrivially. For h ∈ H∖0 with preimage z on S∖{i,j}, the preimages of ch are cz + sδ; for
  s ≠ 0, coordinates i, j are sδ_i, sδ_j in distinct cosets, so not both in P. So s = 0 and
  cz must be admissible, which pins cos(c); with κ ≥ 2 some ch is missing. If |S| = 2 then
  dim W = 1 and there is no plane at all.
- **Unbounded rules.** The conclusion is about the set R_U(S), which contains every value any
  rule can produce from S, whatever it depends on and however long it runs. So the claim holds
  for computationally unbounded rules. It does not bound methods that are not of the
  "one set at a time, modulo the realized space" form.
- **The hypothesis "entries not all in one coset" is needed and is stated** (in the report's
  Theorem 1 and in the remark). Counterexample when it fails: κ = 2, columns e_1, e_2, −e_1 − e_2,
  δ = (1,1,1): R_0(S) = F_p^2 exactly at p = 29, 53, 101 (`mono.out`); a random single-coset
  circuit at p = 29 also contains a plane (`thm1.out`). A single-coset δ is itself a solution
  after scaling, so this case is harmless for the solver; the remark says so.
- **Finishing.** A circuit with δ meeting two cosets cannot realize a nonzero-weight element of U:
  Λx ∈ U forces x ∈ F_pδ, and no nonzero multiple of δ is admissible. Hence such a scheme
  finishes only with a single-coset circuit, which is what the corrected count uses.

### 1.2 Proposition 2

Re-derived both directions of (ii), the reduction (i) to coset-constant b (choosing
representatives so that b' stays nonconstant), and (iii) in both directions (universal ⇒
restricted for any C with |C| ≥ 2; restricted at C = Z_κ ⇒ universal by the shift
α'_j = yα_{j+j_0}, β'_i = yβ_{i+i_0}, y ∈ Q_{i_0+j_0}). The universal object is exactly the paper's
two-level contraction (C_ij = z_iz_j(α_j + β_i) ∈ Q_0°, C_00 ≠ 0 ⇔ α_j + β_i ∈ Q_{−(i+j)}°,
α_0 + β_0 ≠ 0). The hypothesis |C| ≥ 2 is needed (it is the same as Theorem 1's) and the remark
states it ("under the hypotheses of this part").

### 1.3 Kernel-2 example

`kernel2.out` (new seed): R_0(S) = F_p^3 in 4/4 samples at p = 13 and at p = 29, κ = 2, five
random columns with relation space of dimension exactly 2 (checked).

### 1.4 Theorem 3: the bound

Re-derived. Given no K + c_i = 0, the c_i are i.i.d. uniform on F_p∖{−K}. u, w are dependent iff
all c_i are equal: probability (p−1)^{1−k}. β = 0 needs all ε_i equal: κ^{1−k}. For fixed t ≠ K and
θ, the count of c ∉ {−K, −t} with χ(t+c) − χ(K+c) = θ is the number of y ∈ F_p∖{0,1} in Q_θ, that
is (p−1)/κ − [θ = 0] (no character sum is needed). So each i satisfies "c_i = −t or the coset
condition" with probability 1/κ + 1/(p−1) (θ ≠ 0) or 1/κ (θ = 0), independently. The union over
p−1 values of t and κ values of θ is at most κ(p−1)(1/κ + 1/(p−1))^k ≤ κpκ^{−k}e^{κk/(p−1)}. With
k = ⌈log_κ p⌉ + m, κ^{1−k} ≤ κ^{1−m}/p and κpκ^{−k} ≤ κ^{1−m}. The stated bound is correct (and
slightly loose). A solution with β ≠ 0, t = K has cos x_i = cos β, so it is admissible only for
β ∈ P, and it reveals K.

Checks (`reduction.out`, `bound.out`):
- 36 tiny instances (p ∈ {7, 13, 17}, κ ∈ {2, 3, 4}, k ∈ {5, 6}), exhaustive over (P∪{0})^k with
  my own kernel construction: planted solution always present; no solution outside span(u, w);
  the predicted failure event (all ε equal, or some E_{t,θ}) equals the actual event "some solution
  does not reveal K" in 36/36.
- Monte Carlo of that exact event, 40,000 trials each, p = 1009:

| κ | k | failure (s.e.) | refined union | stated bound |
|---|---|---|---|---|
| 2 | 14 | 0.1129 (0.0016) | 0.1249 | 0.1268 |
| 2 | 16 | 0.0295 (0.0008) | 0.0313 | 0.0318 |
| 4 | 9 | 0.0157 (0.0006) | 0.0158 | 0.0160 |
| 3 | 12 | 0.0057 (0.0004) | 0.0058 | 0.0059 |

All rates are below the bound. The report's 2000-trial rates (0.0335 at κ = 2, k = 16, and 0.0175
at κ = 4, k = 9) were slightly above it, within one standard error; the larger sample removes
that.

### 1.5 The assumption and the citations

- **Not a standard assumption.** The needed hypothesis is: recovering K from O(log p) values of
  c ↦ χ(K + c) at uniformly random points takes classical time superpolynomial in log p. It
  follows from pseudorandomness of the Legendre / power-residue PRF (key recovery from random
  queries breaks the PRF), so it is weaker than PRF security. It is a cryptographic conjecture
  (studied as the Legendre PRF, with no reduction to a standard problem), not a standard
  complexity assumption such as LWE. The remark now says so.
- **Damgård 1988** proposed Legendre / Jacobi sequences as pseudorandom generators. The report
  did not re-read it; the remark now cites it only for that.
- **Beullens–Beyne–Udovenko–Vitto 2020** (abstract and record only): key-recovery attacks of cost
  about p·polylog(p)/M² from M ≤ p^{1/4} queries, also for generalizations. The remark cites it
  only for "no classical key-recovery algorithm polynomial in log p is known".
- **van Dam–Hallgren–Ip 2006** (abstract and record only): polynomial-time quantum algorithm for
  the shifted Legendre symbol problem **with quantum (superposition) access** to the function.
  The proposed remark attributed to them the conjecture of classical pseudorandomness ("conjectured
  classically pseudorandom and solved by ... in [vDHI]"); that attribution was not checked against
  the paper, so the remark no longer makes it. It now says the reduction uses classical random
  queries, which their algorithm does not use.
- **Beullens et al.** in the task text: the report cites two different Beullens papers. The
  restricted-syndrome one (Beullens–Briaud–Øygarden, CiC 2024, read in full in `lit/`) is not
  used by the remark; only Beullens–Beyne–Udovenko–Vitto is.

### 1.6 Scope "M < κa + 1"

Correct but incomplete. a + 2 < κa + 1 iff (κ−1)a > 1, so it holds for a ≥ 2 (κ = 2) or a ≥ 1
(κ ≥ 3); the remark now says "for a ≥ 2". The theorem concerns the single arity M = a + 2, where
random instances are unsolvable with high probability (Corollary 3). It says nothing about any
arity at which every instance is solvable. That includes M ≥ κa + 1, and also, for p ∉ E_2(κ),
the triangular arity (a+1)(a+2)/2 even when it is below κa + 1 (for example κ = 5, a = 2: 6 < 11).
The remark now says this.

### 1.7 Bibliography entries

Internally consistent: BBUV pages 313–330 match the DOI suffix; Damgård's CRYPTO '88 volume is
LNCS 403, published 1990; CHMT is PQCrypto 2014, LNCS 8772; vDHI is SIAM J. Comput. 36(3), 2006.
The report gave no pages for vDHI; 763–778 was added from memory. No page number, DOI or ePrint
number could be confirmed offline, so each entry has a `% NEEDS HUMAN VERIFICATION` comment. In
`main.tex` the name "Damgård" is not spelled out, because the macro test rejects `\aa`; the bib
entry keeps it.

## 2. Test reruns

- `test_subquadratic.py` (in the report's folder, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 ... -p no:cacheprovider`):
  **6 passed in 6.55 s**.
- Exact-count scripts rerun into the scratchpad and compared with `diff`: `circuit_flex.py circuits`,
  `circuit_flex.py kernel2`, `flexline_structure.py`, `flexline_e2.py`, `legendre_reduction.py
  countlemma`, `legendre_reduction.py crosscheck`: **all six outputs byte-identical** to the
  committed `.out` files. They match the report: 133 circuits, 0 violations; Prop 2 (i) 105/105,
  (ii) 97/97; count lemma 8 (p, κ) pairs, 0 mismatches; cross-check 54/54; kernel-2 [3,3,3,3] at
  p = 13 and 29. The sampled `sweep` and `bound_check` were not rerun; 1.4 replaces them with a
  larger independent sample.
- Independent script (`2026-11-05-rees-sde-subquadratic-check/indep_check.py`):
  - `thm1`: 70 circuits (14 (p, κ, q), random and adversarial patterns), 0 planes among
    non-single-coset ones.
  - `prop2`: (i) 69 circuits, 0 mismatches between "R has a line" and a brute-force
    restricted-contraction search; (iii) for κ = 2, 3, 4, 5 and 17 primes, restricted (C = Z_κ)
    = universal = (p ∉ E_2(κ) as listed in the paper), 0 mismatches.
  - `mono`, `kernel2`, `reduction`, `bound`: as in 1.1, 1.3, 1.4.
- Paper: `latexmk -g -pdf` in `scratchpad/build-sub/`: exit 0, **0 Overfull**, no undefined
  reference or citation, no "Float too large", no LaTeX warning, BibTeX 0 warnings; the four new
  `\bibitem`s are present. `tests/tools/test_rees_paper_numbers.py`: **2 passed** (after removing
  `\aa`, see 1.7). Backups of `main.tex` and `references.bib` taken first in `scratchpad/bak-sub/`.

## 3. Exact text inserted

### 3.1 `main.tex`, new remark directly after `\end{remark}` of `rem:triangular-scope`

```latex
\begin{remark}[Below quadratic arity; AI-checked, pending human review]
\label{rem:sde-subquadratic}
This remark comes from an AI-only pass (\file{research/audits/reviews/2026-11-05-rees-sde-subquadratic.md}), checked and corrected by a second, adversarial AI pass (\file{research/audits/reviews/2026-11-05-rees-sde-subquadratic-check.md}); no human has checked it, and nothing else in the paper uses it. Keep the notation of Proposition~\ref{prop:triangular-sde}. For a set $S$ of columns and a subspace $U\le\Fp^{a}$ put $R_U(S)=\{\sum_{i\in S}x_i\lambda_i+U : x\in(P\cup\{0\})^{S}\}\subseteq\Fp^a/U$. Call $U$ \emph{realizable} by disjoint sets of columns if every element of $U$ is a value $\sum_i x_i\lambda_i$ with weights $x_i\in P\cup\{0\}$ on their union. If $U$ is realizable and $S$ is disjoint from the sets used, then every subspace $V\supseteq U$ with $V/U\subseteq R_U(S)$ is realizable, as the spaces $U_{k+1}=U_k\oplus\Fp v_{k+1}$ are in the proof of Proposition~\ref{prop:triangular-sde}.

\textup{(a)} \emph{One dependency gives one direction.} Suppose the images of $S$ in $\Fp^a/U$ form a circuit: they are dependent and every proper subset is independent, so their relations are the multiples of one $\delta\in\Fp^S$ with every $\delta_i\ne0$. Suppose also that the entries of $\delta$ do not all lie in one coset $g^\nu P$. Then $R_U(S)$ contains no $2$-dimensional subspace. This is a property of the set $R_U(S)$, so it bounds every rule for choosing the weights, universal or depending on the columns, whatever its running time. Indeed, choose $i,j\in S$ with $\mathrm{cos}(\delta_i)\ne\mathrm{cos}(\delta_j)$ and let $H$ be the span of the images of $S\setminus\{i,j\}$, a hyperplane in the span $W$ of the images of $S$. A plane $T\subseteq R_U(S)$ lies in $W$, so it contains some $h\ne0$ in $H$. Let $z\in\Fp^S$ be the vector supported on $S\setminus\{i,j\}$ with $\sum_l z_l\lambda_l+U=h$; it is unique and nonzero. For $c\in\Fp^\times$ the vectors $x\in\Fp^S$ with $\sum_l x_l\lambda_l+U=ch$ are $cz+s\delta$, $s\in\Fp$. For $s\ne0$ their $i$th and $j$th entries $s\delta_i$ and $s\delta_j$ lie in different cosets, so such a vector lies in $(P\cup\{0\})^S$ only if $s=0$ and $cz\in(P\cup\{0\})^S$, which fixes $\mathrm{cos}(c)$. Since $\kappa\ge2$, some multiple $ch$ is not in $R_U(S)$, a contradiction. The hypothesis on $\delta$ is needed: for $\kappa=2$ and $p\in\{29,53,101\}$ the columns $e_1,e_2,-e_1-e_2$, with $\delta=(1,1,1)$, have $R_0(S)=\Fp^2$; such a $\delta$, however, is itself a solution. Consider a scheme that enlarges the realizable space one set at a time, each set a circuit modulo the space realized so far, and finishes when some set realizes an element of that space with weights not all zero. A circuit whose dependency meets two cosets adds at most one dimension, and it cannot finish the scheme, since its only relations modulo the current space are the multiples of $\delta$. So, until it meets a circuit whose dependency lies in one coset, such a scheme gains at most one dimension per circuit and needs at least $a$ circuits to make $\Fp^a$ realizable. If moreover the fresh columns are in general position modulo the current space $U$ (any $a-\dim U$ of them independent modulo $U$), a circuit modulo $U$ has at least $a-\dim U+1$ columns, and a scheme that meets no circuit with dependency in one coset before $\Fp^a$ is realizable uses at least $a(a+3)/2+1=(a+1)(a+2)/2$ columns, the count of Proposition~\ref{prop:triangular-sde}. This is a lower bound for schemes of this form only. Moreover, under the hypotheses of this part, $R_U(S)$ contains a line $\Fp w$, $w\ne0$, if and only if there are $\alpha\in\Fp^{\kappa}$ and a nonconstant map $\beta$ from the set $C=\{\mathrm{cos}(\delta_i):i\in S\}$ to $\Fp$ with $\alpha_\nu+\beta_{c}\in g^{-(\nu+c)}P\cup\{0\}$ for all $\nu\in\mathbb{Z}_\kappa$ and $c\in C$. For $C=\mathbb{Z}_\kappa$ such a pair exists if and only if $p\notin E_2(\kappa)$. So rules that depend on the columns give a circuit a line exactly when a contraction restricted to $C$ does, and at $p\in E_2(\kappa)$ a circuit whose dependency meets all $\kappa$ cosets realizes no line. Sets with a two-dimensional space of relations are not covered: for $\kappa=2$, $p\in\{13,29\}$ and $a=3$, each of four random sets of five columns has $R_0(S)=\Fp^3$ (exhaustive finite computation, AI-checked, pending human review).

\textup{(b)} \emph{Planted hardness below the Chevalley--Warning bound; conditional.} Let $\chi(y)\in\mathbb{Z}_\kappa$ be the coset of $y\ne0$, and let $K\in\Fp$ be unknown. Suppose an algorithm returns, in time $T$, a nonzero $x\in(P\cup\{0\})^{a+2}$ with $\sum_i x_i\lambda_i=0$ for every $\lambda_1,\dots,\lambda_{a+2}\in\Fp^{a}$ for which such an $x$ exists. Draw $k$ independent uniform points $c_i\in\Fp$ and obtain $\chi(K+c_i)$; if some $K+c_i$ is $0$, output $-c_i$. Otherwise put $\varepsilon_i=\chi(K+c_i)$, pick $u_i\in g^{-\varepsilon_i}P$, and, unless all $c_i$ are equal, take columns in $\Fp^{k-2}$ whose relation space is exactly the span of $u=(u_i)_i$ and $w=(u_ic_i)_i$. The vector $x_i=u_i(K+c_i)$ is a solution. Every solution is $\alpha u+\beta w$. If $\beta=0$, all $\varepsilon_i$ are equal. If $\beta\ne0$, then $x_i=\beta u_i(t+c_i)$ with $t=\alpha/\beta$, and for every $i$ either $c_i=-t$ or $\chi(t+c_i)-\chi(K+c_i)=-\mathrm{cos}(\beta)$. Since $c\mapsto(t+c)/(K+c)$ is a bijection of $\Fp\setminus\{-K\}$ onto $\Fp\setminus\{1\}$, for fixed $t\ne K$ each $i$ satisfies this with probability at most $1/\kappa+1/(p-1)$, independently of the others. A union bound over $t$ and $\mathrm{cos}(\beta)$ shows that every solution has $\beta\ne0$ and $\alpha/\beta=K$, except with probability at most $\kappa^{1-k}+\kappa p\,\kappa^{-k}e^{\kappa k/(p-1)}+(p-1)^{1-k}$. For $k=\lceil\log_\kappa p\rceil+m$ this is at most $\kappa^{1-m}\bigl(1/p+e^{\kappa k/(p-1)}\bigr)+(p-1)^{1-k}$. So $K$ is recovered in expected time $T+\poly(k,\log p)$ from the values of $c\mapsto\chi(K+c)$ at $k$ uniformly random points. This function is the power-residue pseudorandom function with key $K$; for $\kappa=2$ it is the Legendre PRF, the shifted Legendre symbol, whose use as a pseudorandom generator goes back to~\cite{Damgard1988}. No classical key-recovery algorithm polynomial in $\log p$ is known for it or for its power-residue generalization~\cite{BeullensBeyneUdovenkoVitto2020}. Van Dam, Hallgren and Ip~\cite{vanDamHallgrenIp2006} find the shift of the Legendre symbol in quantum polynomial time, but from superposition queries, which this reduction does not supply. Hence, if recovering $K$ from $O(\log p)$ values at random points takes classical time superpolynomial in $\log p$ (a cryptographic assumption, not a standard complexity-theoretic one), then no classical algorithm solves every solvable instance with $M=a+2$ columns in time $\poly(a,\log p)$ for primes $p$ of size $\kappa^{a+O(1)}$. For $a\ge2$ these instances have $M=a+2<\kappa a+1$ columns, so the statement concerns solving whenever a solution exists, below the Chevalley--Warning bound. It says nothing about arities at which every instance is solvable, such as $M\ge\kappa a+1$ and, for $p\notin E_2(\kappa)$, the arity of Proposition~\ref{prop:triangular-sde}.

\textup{(c)} For $\kappa=2$ the problem is a homogeneous underdetermined system of $a$ quadratic equations. The best polynomial-time threshold known for underdetermined quadratic systems over fields of odd characteristic is again quadratic, $n\ge m(m+1)/2$ variables for $m$ equations~\cite{ChengHashimotoMiuraTakagi2014}, and recursing through totally isotropic subspaces of one form at a time uses $2^{a+1}-1$ variables. At $p=3$, where $\kappa=2=p-1$, the problem is $\mathbb{F}_3$ subset sum, so a method at arity $o(a^2)$ for $\kappa=2$ that is uniform in $p$ would improve on every known classical polynomial-time algorithm for that problem (Remark~\ref{rem:triangular-scope}).
\end{remark}
```

### 3.2 `main.tex`, `rem:triangular-scope`, sentence replaced

Old: `No polynomial-time method at arity $o(a^2)$ is known for any fixed $\kappa\ge2$; at $\kappa=p-1$ the problem is ...`

New:

```latex
No polynomial-time method at arity $o(a^2)$ is known for any fixed $\kappa\ge2$. Remark~\ref{rem:sde-subquadratic} (AI-checked, pending human review) shows that schemes enlarging the realizable space one circuit at a time cannot reach such an arity for columns in general position, and that, under a cryptographic assumption, no classical polynomial-time algorithm solves every solvable instance at arity $a+2$; neither statement excludes a method at an arity at which every instance is solvable. At $\kappa=p-1$ the problem is ...
```

### 3.3 `references.bib`, appended

```bibtex
% NEEDS HUMAN VERIFICATION: volume 403, pages 163--172 and the 1990 publication year are from the
% 2026-11-05 subquadratic report and memory, not confirmed offline (the paper was not re-read).
% Subquadratic checker, 2026-11-05.
@inproceedings{Damgard1988,
  author    = {Damg{\aa}rd, Ivan B.},
  title     = {On the Randomness of {Legendre} and {Jacobi} Sequences},
  booktitle = {Advances in Cryptology -- {CRYPTO} '88},
  series    = {Lecture Notes in Computer Science},
  volume    = {403},
  pages     = {163--172},
  publisher = {Springer},
  year      = {1990}
}

% NEEDS HUMAN VERIFICATION: pages 313--330 (consistent with the DOI) and the ePrint number were
% read from the abstract and record only, not confirmed offline. Subquadratic checker, 2026-11-05.
@article{BeullensBeyneUdovenkoVitto2020,
  author  = {Beullens, Ward and Beyne, Tim and Udovenko, Aleksei and Vitto, Giuseppe},
  title   = {Cryptanalysis of the {Legendre} {PRF} and Generalizations},
  journal = {IACR Transactions on Symmetric Cryptology},
  volume  = {2020},
  number  = {1},
  pages   = {313--330},
  year    = {2020},
  doi     = {10.13154/tosc.v2020.i1.313-330},
  note    = {IACR ePrint 2019/1357}
}

% NEEDS HUMAN VERIFICATION: pages 763--778 and the DOI are from memory and the report's record
% search, not confirmed offline. Subquadratic checker, 2026-11-05.
@article{vanDamHallgrenIp2006,
  author  = {van Dam, Wim and Hallgren, Sean and Ip, Lawrence},
  title   = {Quantum Algorithms for Some Hidden Shift Problems},
  journal = {SIAM Journal on Computing},
  volume  = {36},
  number  = {3},
  pages   = {763--778},
  year    = {2006},
  doi     = {10.1137/S009753970343141X},
  note    = {arXiv:quant-ph/0211140}
}

% NEEDS HUMAN VERIFICATION: pages 40--58 are from the report, not confirmed offline; the threshold
% n >= m(m+1)/2 was read from Section 2 of Hashimoto, JSIAM Letters 15 (2023), not from this paper.
% Subquadratic checker, 2026-11-05.
@inproceedings{ChengHashimotoMiuraTakagi2014,
  author    = {Cheng, Chen-Mou and Hashimoto, Yasufumi and Miura, Hiroyuki and Takagi, Tsuyoshi},
  title     = {A Polynomial-Time Algorithm for Solving a Class of Underdetermined Multivariate Quadratic Equations over Fields of Odd Characteristics},
  booktitle = {Post-Quantum Cryptography ({PQCrypto} 2014)},
  series    = {Lecture Notes in Computer Science},
  volume    = {8772},
  pages     = {40--58},
  publisher = {Springer},
  year      = {2014}
}
```

## 4. Dropped or changed from the report's proposed text

- Nothing was dropped as failing. Changes: definitions of R_U(S) as a subset of the quotient and of
  "realizable"; the counterexample showing the coset hypothesis is needed; the corrected
  finishing condition for the (a+1)(a+2)/2 count, with "lower bound for schemes of this form
  only"; the two edge cases of the reduction; "β ≠ 0 and α/β = K"; the k = ⌈log_κ p⌉ + m form of
  the bound; the assumption stated as a cryptographic one; vDHI restricted to superposition
  queries, without the unverified attribution of the conjecture; the scope extended to every
  arity at which all instances are solvable, including the triangular one; one sentence on p = 3.

## 5. Claim gates that stay false

- "An o(a²) SDE solver exists" or "is impossible": neither is claimed.
- "The SDE search is hard at any arity where every instance is solvable": not claimed.
- "The triangular solver is optimal": only among one-circuit-at-a-time schemes under general
  position that meet no single-coset circuit early.
- Hardness from a standard assumption: no, only from the power-residue PRF key-recovery conjecture.
- Novelty or priority: none claimed.
