# Rees HSP: removing the normal-form proviso from the black-box total time

4 November 2026. AI pass, local only: no git, no network, no `.tex` edited. **AI-checked, pending human review.**

Follows up finding G1 of `2026-11-04-rees-referee-6-blackbox.md`. That report's "Applied" section kept the proviso and did not adopt the optional Howell-form discharge.

## Verdict

**The proviso can be removed, and τ_c does not change.**

* **The only term it covers.** The proviso covers one term of the total time: the public module arithmetic, (M1)–(M3) and the idealizer, in the normalizer rounds of Algorithm RtF. RtF runs on the acquired chart for the primes p > c with e_p > 1.
* **The other computations are already explicit.** Chart acquisition (`lem:tb-chart`), the coordinates of chart elements, and the coherent section and exponential maps all have explicit costs. `lem:tb-kernel` never computes a generating set on the theorem's route.
* **The new bound.** Run those rounds over Z/M, M = p^{e_p}, with the Howell sequences and Smith form that `lem:tb-chart` already builds (Steps 2 and 4). A round then costs O(m^5) ring operations modulo M, where m ≤ n_p is the number of cyclic summands of the chart. There are at most n_p + 1 rounds. In all, the normalizer steps cost

  **O(Σ_p n_p^6 b_M^2) ⊆ O(ℓ^8) ⊆ O(N^8) bit operations,**

  independent of s, w and ε, on every branch.
* **Why τ_c is unchanged.** τ_c ≥ 23/2 > 8 for every c, so the term never dominates. It also stays below 17/2 if the AKS bound is later improved.
* **No citation is load-bearing.** The proof uses only the appendix's own Howell construction and Smith form, plus a sharper operation count for the construction and one new observation: the local Howell sequence gives left kernels. Storjohann–Mulders and Howell are cited for context only. Kannan–Bachem stays cited only for the general `thm:ring-to-field`, which keeps its poly(B) statement.

## 1. What the proviso is, where it is used, and what needs it

### 1.1 Text

* **main.tex, `thm:bb-envelope`(iii).** The classical time lists "polynomial normal-form arithmetic per normalizer step", with no degree.
* **main.tex, the total-time paragraph after the items.** It reads: "provided the degree of the normal-form arithmetic of the normalizer steps is at most the exponent of the total time stated next (Proposition prop:tb-count-gates), the total time is O_c(N^{E_W(c)+1+max(3,β̂_c)+o(1)}) for c ≥ 3; …".
* **appendix, `prop:tb-count-gates`(d).** It has "plus poly(ℓ) normal-form arithmetic per normalizer step with at most L ≤ ℓ steps". After the items: "The total time is O_c(N^{τ_c+o(1)}) with τ_c = max(E_W(c)+1+max(3,β̂_c), 23/2), provided the degree of the normal-form arithmetic is at most τ_c."
* **appendix, proof of (d).** It has "Normalizer steps: Proposition prop:tb-recursion, at most n_p rounds per prime." No cost is given. The exponent paragraph then bounds every time term except this one.

### 1.2 Where it is used

* **One term.** The proviso is used only to absorb that one term into N^{τ_c}. No query, gate or error count depends on it.

### 1.3 Which computations need it

**Chart acquisition (`lem:tb-chart`): does not need it.**

* The sample matrix Y ∈ (Z/M)^{k×d} is processed by Howell sequences (Step 2) and a Smith form over Z/M (Step 4).
* This takes O_c(dk^2 + k^4) ring operations, each O(b_M^2) bits. It is charged in (d) as O_c(s^cΛ^2ℓ^2 + Λ^4ℓ^2).
* No integer normal form is used.

**Normal forms of chart elements: do not need it.**

* The coordinate map, `lem:tb-chart`(c), costs O(k^2) ring operations per vector.
* The coherent maps (the section σ∘ι_M of `lem:tb-quotient-oracle`, and x ↦ exp x through the precomputed Φ(ε̃_i)) are linear maps with classical matrices, or straight-line programs. Their gates are already in (a) and (ii).
* What is new in Section 2 is only how the classical matrix of σ∘ι_M is computed. The coherent map keeps the same shape: m_0·m multiply-accumulates modulo p^{e_j}, with m_0, m ≤ n_p. So (a) is unchanged.

**`lem:tb-kernel`: does not need it on the theorem's route.**

* Its statement includes "poly(d, e log p) public normal-form arithmetic", and its proof says ker π is "found by Smith normal form".
* That computes a generating set of ker π. Route (R2), which is the route of the theorem, never does this: `lem:tb-chart` decides membership by Yu = 0, and the lemma says so.
* So no time term of `thm:bb-envelope` charges it. If one wants it explicit anyway, it is a right kernel of Y, that is, a left kernel of Y^T. Primitive (P3) below gives it in O(d(t+d)^2) ring operations. That is O_c(s^{3c}) and is not needed.

**The normalizer steps of RtF on the chart: these need it.**

* For e_p > 1, every round presents S/K, which is (M1), computes the socle tensor, which is (M3), forms K' = q^{-1}(U), and computes S' = I_S(K'), which is (M2).
* The appendix ("Public module arithmetic") does this with full-rank integer lattices in Z^m, which have Hermite and Smith forms with unimodular transforms. It cites Kannan–Bachem 1979 and Storjohann 1996 for polynomial time but gives no degree. This is the unbounded term.
* For e_p = 1 there is one core call and no normalizer round.

## 2. Explicit polynomial time over Z/M

### 2.1 Set-up

* **The ring.** Take the setting of Section `app:tb-ring`: L = ⊕_{i=1}^m (Z/p^{e_i})ε_i with integer structure constants, e = max e_i, M = p^e, b = Σ e_i ≥ m, and b_e = ⌈log_2(M+1)⌉ (the appendix's definition; b_M ≤ b_e ≤ b_M + 1).
* **Embedding.** The map ψ(t)_i = p^{e−e_i}t_i is an injective additive map L → (Z/M)^m. Its image V = ⊕ p^{e−e_i}(Z/M) is a Z/M-submodule.
* **Storage.** Every additive subgroup of (Z/M)^m is a Z/M-submodule. So each subgroup A ≤ L is stored by a Howell sequence, in the sense of (HF1) and (HF2) of `lem:tb-chart` Step 2, for ψ(A). It has at most m rows, since the pivots are distinct.
* **Bracket.** The bracket on V is ψ∘[·,·]∘(ψ^{-1}×ψ^{-1}), at O(m^3) ring operations. It does not depend on the lifts, because p^{e_i}[ε_i, ε_j] = 0.

### 2.2 Primitives (ring operations modulo M)

**(P1) Construction.** This is the construction of `lem:tb-chart` Step 2 on q_0 generators in (Z/M)^n. It costs **O(max(q_0,1)·n^2)**, which sharpens the O((q_0+n)n^2) stated there.

* At a position where a pivot is chosen, one vector leaves the remaining set and one, p^{e−a}·pivot, is appended. Other positions change no count.
* So the remaining set never holds more than q_0 vectors, and each of the n positions costs O(q_0 n).
* This sharpening matters. With the old count the idealizer costs O(m^6) per round, and the total becomes ℓ^9. That is still below 23/2 but above 17/2.

**(P2) Membership with coefficients.** This is the membership scan of Step 2, with the multipliers recorded. It costs O(n^2).

**(P3) Left kernel.** Let Λ = {λ : Σλ_iα_i = 0} for rows α_1..α_a ∈ (Z/M)^n.

* Build the Howell sequence of the rows (α_i | e_i) ∈ (Z/M)^{n+a}.
* The rows whose pivot lies in the last a positions have the form (0 | λ), and their λ generate Λ. The cost is O(a(n+a)^2).
* **Proof.** Let w be in the row span with zero first block. At each pivot j_t ≤ n the scan of Step 2 sees the entry 0 and uses multiplier 0. That is a valid lift of 0/p^{a_t}, so the correctness argument of Step 2 keeps w in S_{t+1}. The scan therefore writes w as a combination of rows with pivot > n.
* **What is new.** This is the property that makes a Howell form, rather than an echelon form, correct for kernels over Z/M. That point is Howell's and Storjohann–Mulders'. Here it follows from (HF2) alone.

**(P4) Smith form.** This is `lem:tb-chart` Step 4 on an a × n matrix C, also recording Q^{-1}. It costs O((a+n)^3). The result satisfies (row span C)·Q = ⊕_t p^{a_t}(Z/M)e_t, with a_t = e past the last nonzero pivot.

### 2.3 One round, at most O(m^5)

Let S and K be given by Howell rows s_1..s_a and k_1..k_β, with a, β ≤ m.

| Step | Computation | Cost |
|---|---|---|
| (N1) stop rule 1 | S = K iff every s_j ∈ K, by (P2) | O(m^3) |
| (N2) (M1) | R = {λ : Σλ_js_j ∈ K} is the projection of the left kernel of (s; k), by (P3). (P4) on R gives Q and d_i, u_i = Σ_j (Q^{-1})_{ij} s_j, S/K = ⊕_{d_i≥1} (Z/p^{d_i})u_i and σ(t) = Σ t_i u_i. Coordinates: y ↦ (λQ)_i mod p^{d_i}, with λ from (P2). Structure constants: m^2 brackets | O(m^5) |
| (N3) (M3) | (M3) verbatim with a_i = d_i, plus the matrix of σ∘ι_M | O(m^3) |
| (N4) stop rule 2 | read at most m_0 = dim Ω returned vectors (a longer output counts as a stopped call), eliminate over F_p, and test bracket closure on m_0^2 pairs | O(m^5) mod p |
| (N5) K' | (P1) on the k_j and the σ(ι_M(x)) | O(m^3) |
| (N6) (M2) | (P4) on K' gives θ(v) = (p^{e−b_l}(vQ')_l)_l with ker θ = ψ(K'). Then I_S(K') is the image of the left kernel of the a × γm matrix with rows (θ[s_i,k'_1], …, θ[s_i,k'_γ]). Costs: m^2 brackets at O(m^3); (P3) at O(a(γm+a)^2) | O(m^5) |

* **Correctness of (N6).** It uses bilinearity, the additive span of the k'_l, and the fact that every y ∈ S is some Σλ_is_i.
* **Correctness of (N2).** It is the isomorphism (Z/M)^a/R ≅ S/K, transported by λ ↦ λQ.
* **Output.** The Howell rows of the final K, mapped back by ψ^{-1}, generate K additively, hence as a group by `cor:tb-correspondence`(a). This replaces the Hermite basis.

### 2.4 Totals

* **Per prime.** `prop:tb-recursion` gives at most b calls, so at most b + 1 rounds. RtF on a chart with b = n'_p (the computed size) and m ≤ n'_p costs O((n'_p+1)n'^5_p) ring operations, each O(b_e^2) = O(b_M^2) bits.
* **The bound b_M ≤ ℓ.** M = exp G_p ≤ max_i o_i ≤ |G| ≤ 2^ℓ. The orders are exact whenever `lem:tb-sylow`(d) reports no failure, and a failure is always detected.
* **The bound Σ n'_p ≤ ℓ.** This holds on every branch, by the two size checks of Section `app:tb-counts`.
* **Over all primes.** O(Σ_p n'^6_p b_M^2) ≤ O(ℓ^2(Σ_p n'_p)^6) ≤ O(ℓ^8 / log_2^6(c+1)) ⊆ O(ℓ^8). Since ℓ ≤ N, this is O(N^8). There is no s-, w- or ε-dependence and no c-dependent constant.
* **Exponent in s.** It is 0. The chart has already removed s, and only the chart terms O_c(s^cΛ^2ℓ^2) depend on s.

### 2.5 Is τ_c affected?

Here τ_c = max(E_W(c)+1+max(3,β̂_c), 23/2).

| c | τ_c | lower bound on τ_c | normalizer exponent | dominated? |
|---|---|---|---|---|
| ≥ 3 | E_W(c)+1+max(3,β̂_c) | E_W(c)+4 ≥ 15 | 8 | yes |
| 2 | max(6+max(3,β̂_2), 23/2) | 23/2 | 8 | yes |
| 1 | 23/2 | 23/2 | 8 (abelian, so I_S(K') = S, but the bound holds regardless) | yes |
| AKS 17/2 variant | τ_1 = 17/2, and τ_c ≥ 9 for c ≥ 2 | 17/2 | 8 | yes |

* **No correction to τ_c is needed.** Every time term is now explicit except β̂_c, which is a separate, acknowledged unknown and not part of this proviso.
* **p = 2.** It occurs only at c = 1, and Z/2^e is a chain ring, so nothing changes. No "Z/2^ℓ-type" modulus is needed: M = p^{e_p} suffices.

### 2.6 Numerical check

`research/audits/reviews/2026-11-04-rees-normal-form/howell_check.py` (run with `/opt/anaconda3/bin/python -I howell_check.py SEED`; seeds 1–5 pass).

* **(P3) against brute force.** Random matrices over Z/9, Z/8, Z/27 and Z/25.
* **Mixed-exponent Lie rings over Z/9 (729 elements each).** On two such rings it compares (N6) with brute-force idealizers I_S(K'), for random subrings K' ⊆ S.
* **(N2) on S'/K'.** It checks the order Π p^{d_i}·|K'| = |S'|, that each u_i has exact order p^{d_i} modulo K', and that the coordinate map inverts σ modulo K'.
* **(M3).** It checks the divisibility claim.
* **Remaining-set bound.** It asserts that the remaining set of (P1) never exceeds q_0.
* **Scope.** This checks correctness on small cases only, not the asymptotic count.

## 3. Drop-in LaTeX (AI-checked, pending human review)

No `\mathsf`, `\mathrel` or `\begingroup`. The text refers to "the algorithm of Proposition prop:tb-recursion" rather than to its `\mathsf` name. Every new reference is to a label that already exists, apart from the new one, `lem:tb-howell-rounds`. Literature is cited in running text, as the appendix already does for Kannan–Bachem, so the build gains no undefined citations. Optional bib entries are in Section 4.

### 3.1 New lemma: appendix-torsion-blackbox.tex

Insert it immediately after the paragraph that follows the proof of `lem:tb-chart` and ends "Each ring operation is $O(b_e^2)$ bit operations." (in the source the last word is on its own line, line ~1031). Insert it before `\subsubsection{Proof of Proposition~\ref{prop:black-box}(iii): the local object}`.

```latex
\begin{lemma}[Normalizer steps over $\mathbb{Z}/M$; AI-checked, pending human review]
\label{lem:tb-howell-rounds}
Let $\mathcal{L} = \bigoplus_{i=1}^m(\mathbb{Z}/p^{e_i})\varepsilon_i$, with integer structure
constants $c_{ij}^k$, be as in the setting of Section~\ref{app:tb-ring}, and put
$e = \max_i e_i$, $M = p^e$, $b = \sum_i e_i$ and $b_e = \lceil\log_2(M+1)\rceil$ as in the
proof of part~(i). The public
arithmetic of the algorithm of Proposition~\ref{prop:tb-recursion}, namely the tests of its stop
rules, the presentation (M1) with its section and structure constants, the socle tensor (M3),
the subring $K' = q^{-1}(U)$, the idealizer (M2) and the output, can be carried out by the
procedures (N1)--(N6) below, which return objects with the properties that (M1)--(M3) specify.
Proposition~\ref{prop:tb-recursion} then holds unchanged, and its public arithmetic costs
$O(m^5)$ ring operations modulo $M$ per round and $O((b+1)m^5)$ in all, on every branch, that is
$O((b+1)m^5b_e^2)$ bit operations. No integer lattice and no normal form over $\mathbb{Z}$ is
used.
\end{lemma}

\begin{proof}
\emph{Representation.} The map $\psi : \mathcal{L} \to (\mathbb{Z}/M)^m$,
$\psi(\sum_i t_i\varepsilon_i) = (p^{e-e_i}t_i)_i$, is an injective additive map, computed in
either direction with $O(m)$ ring operations (the inverse is exact division by $p^{e-e_i}$). Every
additive subgroup of $(\mathbb{Z}/M)^m$ is a $\mathbb{Z}/M$-submodule. A subgroup $A$ of
$(\mathcal{L},+)$ is stored by a Howell sequence for $\psi(A)$ in the sense of Step~2 of the proof
of Lemma~\ref{lem:tb-chart}, with $k$ there replaced by $m$; it has at most $m$ rows, since its
pivots are distinct. For $x, y \in \psi(\mathcal{L})$ put
$[x,y] \coloneqq \psi([\psi^{-1}x,\psi^{-1}y])$, at $O(m^3)$ ring operations from the $c_{ij}^k$;
it does not depend on the lifts of the coordinates, because
$p^{e_i}[\varepsilon_i,\varepsilon_j] = [p^{e_i}\varepsilon_i,\varepsilon_j] = 0$. The rows
$p^{e-e_i}e_i$ form a Howell sequence for $\psi(\mathcal{L})$ ((HF1) as $e_i \ge 1$, (HF2) as
$p^{e_i}\cdot p^{e-e_i}e_i = 0$), and the empty sequence is one for $0$.

\emph{Primitives.} All counts are ring operations modulo $M$.
(P1) Given $q_0$ generators in $(\mathbb{Z}/M)^n$, the construction of Step~2 of the proof of
Lemma~\ref{lem:tb-chart} returns a Howell sequence of their span in $O(\max(q_0,1)\,n^2)$: at a
position where a pivot is chosen, one vector leaves the remaining set and one is appended, and
the other positions change no count, so the remaining set never has more than $q_0$ vectors
(zero vectors are discarded), and each of the $n$ positions costs $O(q_0n)$.
(P2) The membership test of Step~2, with the multipliers $v_j/p^{a_t}$ recorded, decides
$v \in A$ and, if so, returns $\lambda$ with $v = \sum_t\lambda_tr_t$, in $O(n^2)$.
(P3) For $\alpha_1,\dots,\alpha_a \in (\mathbb{Z}/M)^n$ let
$\Lambda = \{\lambda \in (\mathbb{Z}/M)^a : \sum_i\lambda_i\alpha_i = 0\}$. Apply (P1) to the
rows $(\alpha_i \mid e_i) \in (\mathbb{Z}/M)^{n+a}$, in $O(a(n+a)^2)$. The rows of the result
whose pivot lies among the last $a$ positions have the form $(0 \mid \lambda)$, and these
$\lambda$ generate $\Lambda$. Indeed the row span is
$W = \{(\sum_i\lambda_i\alpha_i \mid \lambda)\}$, so $W \cap (0 \oplus (\mathbb{Z}/M)^a) = 0 \oplus \Lambda$.
Let $w \in W$ vanish in the first $n$ positions. At a pivot $j_t \le n$ the membership test of
Step~2 meets the entry $0$ and uses the multiplier $0$, a lift of $0/p^{a_t}$, so the argument
there keeps $w$ in the span of the rows after $r_t$. The test therefore writes $w$ as a
combination of the rows with pivot beyond $n$, which vanish in the first $n$ positions.
(P4) For $C \in (\mathbb{Z}/M)^{a\times n}$, Step~4 of the proof of Lemma~\ref{lem:tb-chart}
gives $P \in \mathrm{GL}_a(\mathbb{Z}/M)$ and $Q \in \mathrm{GL}_n(\mathbb{Z}/M)$ with $PCQ$
diagonal with entries $p^{a_t}$ or $0$, and recording the inverse of each column operation also
gives $Q^{-1}$, in $O((a+n)^3)$. Put $a_t = e$ for every $t \le n$ with no nonzero diagonal entry
$p^{a_t}$. Since $P$ is invertible, the row span of $C$, multiplied by $Q$, is
$\bigoplus_{t\le n}p^{a_t}(\mathbb{Z}/M)e_t$.

\emph{One round.} Let $s_1,\dots,s_a$ and $k_1,\dots,k_\beta$ be the rows of the Howell sequences
for $\psi(S)$ and $\psi(K)$, so $a, \beta \le m$; brackets and sections are computed in
$\psi$-coordinates.

(N1) \emph{Stop rule~1.} Since $K \subseteq S$, $S = K$ if and only if every $s_j$ passes (P2)
against $K$: $O(m^3)$.

(N2) \emph{Presentation (M1).} The relation module
$R = \{\lambda \in (\mathbb{Z}/M)^a : \sum_j\lambda_js_j \in K\}$ is the projection onto the first
$a$ coordinates of the left kernel of $(s_1,\dots,s_a,k_1,\dots,k_\beta)$, so (P3) gives at most
$a+\beta$ generators of $R$ in $O(m^3)$. Apply (P4) to the matrix of these generators, with
$n = a$, to get $Q$, $Q^{-1}$ and exponents $d_1,\dots,d_a$ with
$RQ = \bigoplus_ip^{d_i}(\mathbb{Z}/M)e_i$. The map $\lambda \mapsto \sum_j\lambda_js_j + K$ from
$(\mathbb{Z}/M)^a$ onto $S/K$ has kernel $R$, and $\lambda \mapsto \lambda Q$ is an automorphism
carrying $R$ onto $\bigoplus_ip^{d_i}(\mathbb{Z}/M)e_i$ and $e_iQ^{-1}$ to $e_i$. So, with
$I = \{i : d_i \ge 1\}$ and $u_i = \sum_j(Q^{-1})_{ij}s_j \in \psi(S)$,
$S/K = \bigoplus_{i\in I}(\mathbb{Z}/p^{d_i})\,(\psi^{-1}u_i + K)$. This is (M1) with
$\delta_i = p^{d_i}$, basis $\psi^{-1}u_i$ and section
$\sigma(t) = \sum_{i\in I}t_i\psi^{-1}u_i$ ($0 \le t_i < p^{d_i}$), which maps into $S$ with
$q\circ\sigma = \mathrm{id}$. The coordinate map sends $y \in S$ to
$t_i = (\lambda Q)_i \bmod p^{d_i}$, where $\lambda$ is returned by (P2) for $\psi(y)$ against
$\psi(S)$; two such $\lambda$ differ by an element of $R$, so $t$ is well defined, at $O(m^2)$ per
vector. Since $K$ is an ideal of $S$, the structure constants of $S/K$ are the coordinates of the
at most $m^2$ brackets $[u_i,u_j]$: $O(m^5)$ in all.

(N3) \emph{Socle (M3).} (M3) applies verbatim with $a_i = d_i$, at $O(m^3)$. The map
$\sigma\circ\iota_M(x) = \sum_{i\in I}\bar x_i\,p^{d_i-1}\psi^{-1}u_i$, with $\bar x_i$ the lift of
$x_i$ to $\{0,\dots,p-1\}$, is $\mathbb{Z}$-linear, with matrix computed once per round at
$O(m^2)$; its coherent evaluation has the form counted in
Proposition~\ref{prop:tb-count-gates}(a).

(N4) \emph{Stop rule~2.} A correct call returns a basis of a subspace of $\Fp^{m_0}$,
$m_0 = |I| \le m$, so at most $m_0$ vectors; a call that returns more is treated as a stopped
call, which changes nothing on the event that the call is correct. Gaussian elimination over
$\Fp$ gives a basis of the span in $O(m^3)$, and closure of $U$ under the bracket of $\Omega$ is
tested on the at most $m_0^2$ pairs of basis vectors, at $O(m^3)$ per bracket from the tensor
and $O(m^2)$ per membership: $O(m^5)$ operations modulo $p$, each at most $O(b_e^2)$ bit
operations.

(N5) \emph{The subring $K'$.} $K' = q^{-1}(U)$ is spanned by $K$ and the
$\sigma(\iota_M(x))$ for $x$ in the basis of (N4), so (P1) on at most $\beta + m_0 \le 2m$
generators gives its Howell sequence in $O(m^3)$.

(N6) \emph{Idealizer (M2).} Let $k'_1,\dots,k'_\gamma$, $\gamma \le m$, be the rows of the Howell
sequence for $\psi(K')$. Apply (P4) to their matrix, with $n = m$, to get $Q'$ and exponents
$b_1,\dots,b_m$, and put $\theta(v) = (p^{e-b_l}(vQ')_l)_l$. Then $\theta$ is
$\mathbb{Z}/M$-linear, and $\theta(v) = 0$ if and only if $p^{b_l} \mid (vQ')_l$ for all $l$, that
is, $vQ' \in \psi(K')Q'$, that is, $v \in \psi(K')$. For $y \in S$ write
$\psi(y) = \sum_i\lambda_is_i$. By bilinearity, and since the $k'_l$ span $\psi(K')$,
$[y,K'] \subseteq K'$ if and only if $\sum_i\lambda_i\theta([s_i,k'_l]) = 0$ for every $l$. So
$\psi(I_S(K'))$ is the image under $\lambda \mapsto \sum_i\lambda_is_i$ of the left kernel of the
$a \times \gamma m$ matrix whose row $i$ is $(\theta[s_i,k'_1],\dots,\theta[s_i,k'_\gamma])$. The
$a\gamma \le m^2$ brackets cost $O(m^5)$, $\theta$ costs $O(m^3)$ to set up and $O(m^2)$ per vector,
(P3) costs $O(a(\gamma m + a)^2) = O(m^5)$, and the image and its Howell sequence (P1) cost
$O(m^3)$.

\emph{Output and totals.} The rows of the Howell sequence for $\psi(K)$, mapped by $\psi^{-1}$,
generate the final $K$ additively, hence as a group by
Corollary~\ref{cor:tb-correspondence}(a); they replace the Hermite basis in the proof of
Proposition~\ref{prop:tb-recursion}. Every object computed in (N1)--(N6) has the property that
(M1)--(M3) and steps~1--4 of the algorithm require, so the proof of
Proposition~\ref{prop:tb-recursion} applies without change. A round costs $O(m^5)$. By
Proposition~\ref{prop:tb-recursion} at most $b$ calls are made on every branch, so there are at
most $b+1$ rounds, and each ring operation costs $O(b_e^2)$ bit operations.
\end{proof}

\noindent On the chart of route~(R2) for a prime $p > c$ with $e_p > 1$, the lemma applies with
$b = n'_p$, the computed chart size, $m \le n'_p$ and $b_e \le b_M + 1$. Here $b_M \le \ell$, since
$M = \exp G_p$ divides an order $o_i \le |G| \le 2^\ell$, which
Lemma~\ref{lem:tb-sylow}(d) returns exactly whenever it reports no failure. By the size checks
of Section~\ref{app:tb-counts}, $\sum_{p>c}n'_p \le \ell$ on every branch. So the normalizer
steps of all primes cost
$O\bigl(\sum_p n_p'^{\,6}\,(b_M+1)^2\bigr) \le O\bigl(\ell^2(\sum_p n'_p)^6\bigr) \le O(\ell^8)$
bit operations on every branch, independently of $s$, $w$ and $\eps$. For $e_p = 1$ there is no
normalizer round. (With the count $O((q_0+n)n^2)$ of Lemma~\ref{lem:tb-chart} in place of (P1),
step (N6) would cost $O(m^6)$ and the total $O(\ell^9)$.)
```

### 3.2 `prop:tb-count-gates`: appendix-torsion-blackbox.tex

**(a) Statement, item (d).** Replace

```latex
  $\Lambda \le 2\ell$), plus $\poly(\ell)$ normal-form arithmetic per normalizer step with at most
  $L \le \ell$ steps, plus $Q_f\,(2\ell)^{\hat\beta_c}\operatorname{polylog}(\ell/\eps)$
```

with

```latex
  $\Lambda \le 2\ell$), plus $O(\ell^8)$ bit operations for the normalizer steps of the primes with
  $e_p > 1$ (Lemma~\ref{lem:tb-howell-rounds}), plus $Q_f\,(2\ell)^{\hat\beta_c}\operatorname{polylog}(\ell/\eps)$
```

**(b) The sentence after the items.** Replace

```latex
$\tau_c = \max(E_W(c)+1+\max(3,\hat\beta_c),\,23/2)$, provided the degree of the
normal-form arithmetic is at most $\tau_c$. For $c \ge 3$, $\tau_c = E_W(c)+1+\max(3,\hat\beta_c)$;
```

with

```latex
$\tau_c = \max(E_W(c)+1+\max(3,\hat\beta_c),\,23/2)$. For $c \ge 3$, $\tau_c = E_W(c)+1+\max(3,\hat\beta_c)$;
```

**(c) The AKS comment block under the proposition.** Append one line:

```latex
% The normalizer term O(l^8) of (d) (Lemma tb-howell-rounds) has exponent 8 < 17/2, so it stays
% dominated under the improved bound as well.
```

**(d) Proof of (d).** Replace

```latex
and $k^4b_M^2 \le 64\Lambda^4e_p^2$, and $\sum_p e_p^2 \le L^2 \le \ell^2$. Normalizer steps:
Proposition~\ref{prop:tb-recursion}, at most $n_p$ rounds per prime. Solvers: a core call has at
```

with

```latex
and $k^4b_M^2 \le 64\Lambda^4e_p^2$, and $\sum_p e_p^2 \le L^2 \le \ell^2$. Normalizer steps:
by Lemma~\ref{lem:tb-howell-rounds} and the paragraph after it, at most $n'_p+1$ rounds per prime
at $O(n_p'^{\,5})$ ring operations each, $O(\ell^8)$ bit operations over all primes and on every
branch. Solvers: a core call has at
```

**(e) The exponent paragraph.** Replace

```latex
the charts by $\max(c+2,6) \le \max(E_W(c)+4,\,23/2)$, and the transforms of~(b) by $c+3 \le E_W(c)+4$, and the certificates by $23/2$.
```

with

```latex
the charts by $\max(c+2,6) \le \max(E_W(c)+4,\,23/2)$, the transforms of~(b) by $c+3 \le E_W(c)+4$, the certificates by $23/2$, and the normalizer steps by $\ell^8 \le N^8$, with $8 < 23/2 \le \tau_c$.
```

### 3.3 `thm:bb-envelope`: main.tex

**(a) Item (iii).** Replace

```latex
Classical time is $O_c(s^c\ell^4 + \ell^6)$ bit operations for the charts when $\log_2(8\ell/\eps) \le \ell$, polynomial normal-form arithmetic per normalizer step, and at most
```

with

```latex
Classical time is $O_c(s^c\ell^4 + \ell^6)$ bit operations for the charts when $\log_2(8\ell/\eps) \le \ell$, $O(\ell^8)$ bit operations for the normalizer steps of the primes with $e_p > 1$, done over $\mathbb{Z}/p^{e_p}$ with Howell forms (Lemma~\ref{lem:tb-howell-rounds}; AI-checked, pending human review), and at most
```

**(b) The total-time paragraph.** Replace

```latex
the number of gates is $O_c(N^{E_W(c)+4+o(1)})$ and, provided the degree of the normal-form arithmetic of the normalizer steps is at most the exponent of the total time stated next (Proposition~\ref{prop:tb-count-gates}), the total time is $O_c(N^{E_W(c)+1+\max(3,\hat\beta_c)+o(1)})$ for $c \ge 3$;
```

with

```latex
the number of gates is $O_c(N^{E_W(c)+4+o(1)})$ and the total time is $O_c(N^{E_W(c)+1+\max(3,\hat\beta_c)+o(1)})$ for $c \ge 3$;
```

The c = 2 and c = 1 clauses stay as they are.

**(c) Attribution sentence, optional.** In "the gate and time counts of~(iii) are proved there by Proposition~\ref{prop:tb-count-gates}, with no compilation hypothesis:", insert "with the normalizer arithmetic by Lemma~\ref{lem:tb-howell-rounds}," after `Proposition~\ref{prop:tb-count-gates}`.

**(d) The AKS comment under the total-time paragraph.** Append the same one-line note as in 3.2(c).

### 3.4 Optional consistency edits (appendix)

**(a) "Public module arithmetic".** At the end of the paragraph, after "We use three instances.", append:

```latex
For an explicit bound, Lemma~\ref{lem:tb-howell-rounds} in Section~\ref{app:tb-blackbox} carries
out (M1)--(M3) and the steps of Proposition~\ref{prop:tb-recursion} over
$\mathbb{Z}/p^{\max_ie_i}$ with Howell sequences, at $O((b+1)m^5)$ ring operations in all.
```

**(b) `prop:tb-recursion`, "Cost".** "at most $b \le B$ rounds" should read "at most $b+1 \le B+1$ rounds". The stop-rule-1 round makes no call. This does not affect poly(B).

**(c) `lem:tb-kernel`.** After "and $\poly(d,e\log p)$ public normal-form arithmetic", add:

```latex
(explicitly, (P3) of Lemma~\ref{lem:tb-howell-rounds} applied to the transpose of the sample
matrix, $O(d(t+d)^2)$ ring operations modulo $p^e$; route~(R2) does not perform this step, since
Lemma~\ref{lem:tb-chart} never computes a generating set of $\ker\pi$)
```

### 3.5 What stays as it is

* `thm:ring-to-field` (main.tex, line ~1011) states poly(B) Hermite and Smith arithmetic for a general explicit ring input. That stays correct.
* The lemma also applies to that setting. Its cost there would be O((b+1)m^5 b_e^2). Whether to state that is optional.
* The regimes table and its caption mention no proviso. The caption's "uncomputed solver exponent" (β̂_c) is still accurate.

## 4. Citations

**Load-bearing: none.**

* The proof uses only the appendix's own Steps 2 and 4 of `lem:tb-chart`, which a previous referee already re-derived.
* Three things are added to them: the sharper count of (P1), the left-kernel property (P3), and the recording of Q^{-1} in (P4). All three are proved in the lemma.

**Context citations, suggested in running text or as new bib keys.**

* **Howell1986.** J. A. Howell, "Spans in the module (Z_m)^s", *Linear and Multilinear Algebra* 19 (1986), 67–77. This is the Howell form and its spanning property. *Unsure of the page range.*
* **StorjohannMulders1998.** A. Storjohann and T. Mulders, "Fast algorithms for linear algebra modulo N", in *Algorithms – ESA '98*, LNCS 1461, Springer, 1998, pp. 139–150. They compute Howell forms over Z/N and use them for kernels and linear systems, with operation counts of matrix-multiplication type.
  * *Unsure* of the LNCS volume and pages (recalled as 1461 and 139–150).
  * *Unsure* of the exact form of their complexity statement, so none of their bounds is quoted.
* **Storjohann2000.** A. Storjohann, *Algorithms for Matrix Canonical Forms*, PhD thesis, ETH Zürich, 2000. It has Howell, Hermite and Smith forms over principal ideal rings, with explicit operation counts. *Unsure* of the Diss. ETH number (recalled as 13922) and of chapter numbers. Not used for any bound.
* **KannanBachem1979.** R. Kannan and A. Bachem, "Polynomial algorithms for computing the Smith and Hermite normal forms of an integer matrix", *SIAM J. Comput.* 8(4) (1979), 499–507. Polynomial time with transformation matrices.
  * I do not recall a single clean exponent stated there, so the integer route is not the basis of the new bound. That is why the proviso existed.
  * Keep it for `thm:ring-to-field`.
* **Storjohann1996** (already suggested in the appendix comment). "Near optimal algorithms for computing Smith normal forms of integer matrices", ISSAC 1996. *Unsure* of the pages (recalled as 267–274).
* **Not needed, alternative.** Domich, Kannan and Trotter, "Hermite normal form computation using modulo determinant arithmetic", *Math. Oper. Res.* 12 (1987). This would be the route that stays over Z, using modular HNF modulo det D = p^b. *Unsure* of the issue and pages. Not recommended, because the Z/M route is self-contained.

## 5. Gates that must stay false; open points

**Must stay false.**

* "The normalizer arithmetic is human-checked." It is not.
* "Total time is now fully explicit." It is not: β̂_c is still uncomputed.
* "The ℓ^8 term changes τ_c." It does not.

**Needs a human check.**

* (P3)'s kernel property for the local Howell sequence, that is, (HF1)+(HF2) without reduced entries above the pivots.
* The O(m^5) count of (N6).
* That (N2) delivers exactly the presentation (M1) that `lem:tb-quotient-oracle` and `lem:tb-section-rank` use.

**Not covered here.**

* Classical post-processing inside the core calls other than the solvers, for example the final F_p elimination of Fourier samples. It is not itemized in (d). I believe it is O_c(ℓ^3)-type per call and dominated, but I did not check it.
* `research/AGENT_HANDOFF.md` and `research/STATE.md` were not updated. This was not a Codex research pass. If the edits are adopted, the integrator should add the entry.

**Next step.** Apply 3.1–3.3, plus 3.4 if wanted. Rebuild, and confirm 0 undefined references, 0 Overfull and that `tests/tools/test_rees_paper_numbers.py` passes. Then have an independent AI pass re-derive (P3) and (N6).
