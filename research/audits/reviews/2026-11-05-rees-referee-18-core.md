# Referee report 18: core version of the Rees/HSP paper (pre-submission check)

Manuscript: `docs/papers/rees-hsp/core/main-core.tex` with `core/numbers.tex` and `core/references.bib`, dated 5 November 2026. Built in the scratchpad with `latexmk -pdf`: 26 pages, 0 Overfull boxes, no undefined references or citations.

Referee: independent, read-only pass, 5 November 2026. The paper was read and checked in full before referee 17's report was opened; Section 5 below compares afterwards. Checks were done by hand and with short exact computations (`/opt/anaconda3/bin/python -I`, sympy): Dixmier–Lister brackets (Jacobi on all 56 triples), lower central dimensions, derivation rank over $\mathbb{Q}$ and modulo $p = 5,\dots,31$, all five rows of Table 1 (both $\log_2 Q_{\mathrm q}$ and the three threshold columns, under both rounding conventions), the exponent $145$, $B_4(2)$, and the monotonicity of $B_d$. Line numbers refer to `core/main-core.tex` as of this date. No file other than this report was written.

---

## 1. Verdict

**Yes, after the listed fixes.** The fixes are small (one afternoon): two notational or wording corrections in text new since referee 17, a notation clash between the Rees variable $t$ and the sample surplus $t$, one citation to verify, and a restructuring of the main theorem statement for readability. None changes a proof.

What a human expert will have to decide is not whether the core's own proofs are right (I found no error in any statement the core proves) but whether the imported Ivanyos–Santha arity is read correctly and whether the cover construction is new. Both are flagged candidly in the manuscript, and both are exactly what expert reviewers are for.

Counts: **0 Error, 0 Gap, 6 Imprecision, 6 Style** (Section 4). Referee 17: 20 of 22 findings fully resolved, 2 partially (F2 restructuring, F18 status tags), see Section 5.

---

## 2. Correctness

### 2.1 Theorem 1.2 (`thm:main`) and its proof (Section 7), step by step

**Statement.** Quantifiers are right: $c$ fixed first, then uniform in $p > c$, in $\mathcal{L}$ (any nilpotent Lie algebra with $\gamma_{c+1} = 0$), in $H$ (arbitrary) and in $\eps$. "Assume Theorem 5.1" names the import in the hypothesis, which is the right convention; Remark 1.3 (`rem:main-solver`, new) lists exactly the four properties used (total at a public arity, deterministic, polynomial time, arity polynomial in $g_d$ uniformly in $p$) and says where the explicit $B_d$ enters (only the displayed bound). I checked that the proof uses nothing else from the solver except one thing the remark leaves implicit: that it returns the scalars $s_i$ and not only $s_i^d$ (Remark 5.2(a)); see Finding 6.

**The procedure (line 545).** $t = \lceil\log_p(3/\eps)\rceil$, $m+t$ terminal samples, each a tree with $P = \prod_{d=2}^c M_d$ leaves. Consistent with Section 4.3 (line 423).

**Lift (Lemmas 3.2, 3.3, 3.5).** Lemma 3.2: for $C = \log(a^{-1}\ast b) = \sum_k t^kC_k$, $E_{s_i}$ is a group homomorphism, so $\widehat f(a) = \widehat f(b)$ iff $\sum_k s_i^kC_k \in \hh$ for all $i$; $(s_i^k) = \diag(s_i)\cdot\text{Vandermonde}$ is invertible; $\hh$ is a subspace; so iff $C_k \in \hh$ for all $k$, i.e. $C \in \hlift$. The intersection form over all $s \in \Fp^\times$ needs $p-1 \ge c$ points, supplied by $p > c$. $\hlift$ is a subalgebra ($[\hh\cap\gamma_i, \hh\cap\gamma_j] \subseteq \hh\cap\gamma_{i+j}$), and $\delta_\theta(E_s^{-1}\hh) = E_{s/\theta}^{-1}\hh$ permutes the family. Correct. Lemma 3.3: the reduced state has entries $|\widetilde G|^{-1}[\widehat f(a) = \widehat f(b)] = |\widetilde G|^{-1}1_{\exp\hlift}(a^{-1}\ast b)$, the entries of $\rho_{\exp\hlift}$ under the convention $\langle x|\rho_H|y\rangle = |G|^{-1}1_H(x^{-1}y)$. Correct. Lemma 3.5: $R$ is a homomorphism ($R_gR_h = R_{gh}$), so the retained entry is $|\widetilde G|^{-1}\prod_i\tr(\rho_HR_{E_{s_i}(b^{-1}\ast a)}) = |\widetilde G|^{-1}\prod_i 1_H(E_{s_i}(b^{-1}\ast a))$, and $1_{\exp\hlift}(b^{-1}\ast a) = 1_{\exp\hlift}(a^{-1}\ast b)$. Correct; the hypothesis on the points is now present (referee 17 F3).

**Theorem 3.1.** (i) $k$-fold brackets of homogeneous elements lie in $t^j\gamma_j$ with $j \ge k$; $\gamma_{c'}$ is spanned by left-normed $c'$-fold brackets, one of which is nonzero, so the class of $\A$ is exactly $c'$; $[t^iy, t^cz] \in t^{i+c}\gamma_{i+c} = 0$. (ii) $E_s\circ\delta_\theta = E_{\theta s}$, bijectivity with inverse $\delta_{\theta^{-1}}$ (now stated). (iii) Dynkin denominators divide products of integers $\le N \le c$; the three group identities hold in the free class-$c$ nilpotent Lie ring over $\mathbb{Z}[1/c!]$, a free module embedding in its $\mathbb{Q}$-form; specialize at $p > c$. Correct.

**Descent (Lemmas 4.1, 4.2, Proposition 4.3).** $\Pi_\lambda = |Z|^{-1}\sum_z\chi_\lambda(-z)R_z$: I verified $R_z\Pi_\lambda = \chi_\lambda(z)\Pi_\lambda$, $\Pi_\lambda^2 = \Pi_\lambda$, $\sum_\lambda\Pi_\lambda = I$; the ancilla ends in $F|\lambda\rangle$ and $F^\dagger$ reads $\lambda$; $2g$ single-coordinate transforms. Lemma 4.2: $\tr(\rho_H\Pi_\lambda) = |Z|^{-1}\sum_{z\in K}\chi_\lambda(-z) = (|K|/|Z|)[\lambda\in K^\perp]$; $\rho_\lambda = \rho_H\Pi_\lambda/\Pr$ as displayed; a nonzero term of $\tr(\rho_\lambda R_g)$ needs $g \in HZ$, with $|K|$ decompositions all giving $\chi_\lambda(z)$ since $\lambda \perp K$. Correct, no normality or transversality used. Proposition 4.3: the output entry at $(q,r)$ is $|Q|^{-1}\prod_{i\ \text{active}}\tr(\rho_{\lambda_i}R_{\delta_{s_i}(\sigma(r)^{-1}\sigma(q))})$ (I rederived the sign conventions: $R_gR_h^\dagger = R_{h^{-1}g}$ and $\delta_{s_i}$ is a homomorphism). Off $HZ$ every active factor vanishes because $\delta_{s_i}$ preserves $H$ and $Z$, and the active set is nonempty. On $g = hz$, $\delta_{s_i}(g) = \delta_{s_i}(h)\cdot s_i^dz$ and the product of characters is $\chi_{\sum_is_i^d\lambda_i}(z) = 1$. The result is $|Q|^{-1}1_{HZ}(\sigma(r)^{-1}\sigma(q)) = |Q|^{-1}1_{HZ/Z}(r^{-1}q)$, the coset density of $HZ/Z$. Correct for every label tuple. The independence sentence (joint state of record and output is a product $p\otimes\rho_{HZ/Z}$, so disjoint blocks give independent outputs) is correct and is what licenses the tree.

**Recursion (Section 4.3).** $\bigoplus_{k>d}\A_k$ is a $\delta$-stable ideal; $Z_d = t^d\gamma_d$ is central in $\A^{(d)}$ and scaled by $s^d$; $H_d$ homogeneous; $K_d = t^d(\hh\cap\gamma_d)$; $H_dZ_d/Z_d = H_{d-1}$; zero-insertion section is public; $G_1 = t\mathcal{L}$ with $H_1 = t\hh$. Generators: $\log\langle\exp b_i\rangle$ is a subalgebra containing a basis of $\hh$. Correct.

**Schedule 1 (Section 5).** Lemma 5.4: with $ud + v(p-1) = \kappa$, $u \ge 0$, $s_i = x_i^u$ gives $s_i^d = x_i^\kappa$ on nonzero $x_i$ and the same support; $B_d(a)$ increases in $d$ (checked numerically for $d \le 7$); $B_1(a) = a+1$; the edge case $\kappa = p-1$ (only at $p = c+1$, $d = c$) is covered. The Schedule 1 paragraph returns a nonzero solution for every label tuple and every $p > c$. Remark 5.5: $B_4(2) = 36520347436056576 \approx 3.7\cdot10^{16}$, the eight columns in $\mathbb{F}_5^2$ have no zero-sum subset, Davenport constant $9$: checked. Theorem 5.1 itself is imported and is the single item I cannot verify offline (Section 6, item 1).

**Compilation and error (Section 6).** Theorem 6.1(i): $Z' = \psi(\ad_Z)Y$ with $\psi(z) = z/(1-e^{-z}) = 1 + z/2 + \sum_{k\ge2}B_kz^k/k!$ (the $+1/2$ is the right sign for this convention); $(j+1)Z_{j+1} = \sum_k(\beta_k/k!)W^{(k)}_j$; $W^{(k)}_j$ uses only $Z_0,\dots,Z_j$; memoized count $(d-1)d(d+1)/2$; von Staudt–Clausen gives denominators with primes $q \le d$. Correct. (ii) The four-pass in-place product (compute $u\ast v$ out of place in two passes, then $(-u)\ast(u\ast v) = v$ in two passes to erase register 2, uncomputing from registers that are still present) is correct. (iii) Imported (Kitaev, Solovay–Kitaev); the $\eta/2 + \eta/2$ split with $\eps' = \eta^2/(16p)$ matches the quoted precision $2(q\eps')^{1/2}$; flagged as unchecked by a human, with the explicit alternative in the full version. (iv) Register count correct. Lemma 6.2: the telescoping sum, the support hypothesis on ideal prefixes, and the final step to total variation are correct; the application paragraph (pure-state bound $\sqrt{1-|\langle\phi|\phi'\rangle|^2} \le \|\phi-\phi'\|$, convexity, classical control as a mixture of branches, labels $\ge p$ reduced modulo $p$) is correct. Corollary 6.3 correct.

**Assembly (Section 7).** Induction $d = c,\dots,2$ gives $m+t$ independent exact copies of $\rho_{t\hh}$; Lemma 2.1 gives failure $\le \frac{p^k-1}{p-1}p^{-(m+t)} < \frac{1}{(p-1)p^t} \le \eps/3$ (I checked the $k = 0$ case and the inequality chain). $N_{\mathrm{QFT}}$: $n$ per lifted source, $2M_dg_d + D_{d-1}$ per stage-$d$ merge, $N_d = \prod_{d'<d}M_{d'}$ merges per tree (so $N_2 = 1$ and $N_c = P/M_c$), $m$ per terminal sample: correct, and public before the run. Total error $2\eps/3 < \eps$. Query count $c(m+t)\prod B_d(g_d)$ and the bound with $C_c$: correct; $1 + \sum_{d=2}^9 d\lceil\log_2(d+1)\rceil = 1 + (4+6+12+15+18+21+32+36) = 145$: correct. Running time paragraph: correct for fixed $c$. The Heisenberg example (both lines, $B_2(1) = 64$, Chevalley–Warning at three variables) is correct.

### 2.2 Classical query complexity (Section 8)

Lemma 8.1 (collision bound): the lazy-sampling oracles $O_K$, $O_H$ with shared coins and label stream agree until the first query in a new $K$-coset but an old $H$-coset, i.e. $x_i^{-1}x_j \in H\setminus K$; the law of the $O_K$-run's queries is independent of $H$; union bound gives $\binom q2\rho$; (i) averages the $O_K$-run's output over $\mu$ to get $\pi$; (ii) is the decision version. Correct. Proposition 8.2: (i) $\rho = \pi = 1/N_1$, $q \ge 2$ since $(1-\delta)N_1 - 1 > 0$, and $q^2 = q(q-1) + q \ge 2(1-\delta)p^{m-1} - 2\delta + q > 2(1-\delta)p^{m-1}$ using $N_1 \ge p^{m-1}+1$; (ii) normal of order $p$ implies central, count $(p^m-p^z)/(p-1) \ge p^{m-2}(p+1) \ge p^{m-1}+1$, $z \le m-2$ for nonabelian $\mathcal{L}$; (iii) $\mathfrak{k}+\Fp v$ is a subalgebra since $\mathfrak{k}$ is an ideal, each $g \notin K$ lies in exactly one, one-dimensional ideals of nilpotent Lie algebras are central; (iv) immediate; (v) I rederived the whole argument: the $e$ in-coset differences are i.i.d. uniform on $H$ given the coset pattern; Burnside basis theorem and the hyperplane bound $< p^{d-e}/(p-1) \le \eps/2$ at $e \ge k+t$; the coupling $\{e < s\} \subseteq \{X < s\}$ with $X$ a sum of independent Bernoullis of mean $\mu_X = \sum_{i=1}^{Q-s}\min(1,i/M)$; Chernoff $\Pr[X \le \mu_X/2] \le e^{-\mu_X/8}$; both cases $Q-s \le M$ (using $p^{k-1}(t+1) \ge k+t$) and $Q-s > M$. The $\Theta$ statement with $m \le 2p^{(m-1)/2}$ follows. All correct.

Table 1: recomputed all five rows. $\log_2Q_{\mathrm q}$: $9.00$, $27.76$, $33.19$, $35.06$, $1572.66$. LB crossover primes: $443$, $337853$, $92107$, $997$; class-9 row $\log_2p \approx 174.72$. The (v) thresholds reproduce under the stated rounding ($84$, $119671$, $42290$, $638$) and the caption's alternative values ($86$, $121497$, $42773$, $642$) under exact $8\ell$. Copies column: $81$, $301$, $407$, $644$ from $\lceil4\log_2(3r)\rceil$ with $r$ the number of subspaces at the crossover prime. All agree.

### 2.3 Dixmier–Lister (Section 3.4)

Recomputed: the ten brackets satisfy Jacobi; lower central dimensions $(8,4,2)$; derivation system rank $52$ over $\mathbb{Q}$ and modulo $p = 5, 7, 11, 13, 17, 19, 23, 29, 31$; the $12$-dimensional nullspace has zero coefficient on $e_1,\dots,e_4$ in every $De_i$ and zero coefficient on $e_1,\dots,e_6$ in $De_5,\dots,De_8$, matching the displayed family. The gcd argument for non-gradability is correct. I did not open the 32 row certificates (referee 17 did, per its application log).

### 2.4 Text new since referee 17

- **Remark 1.3 (`rem:main-solver`), line 156.** Correct and useful; it answers referee 17's F2 in substance (any solver with the four properties gives the theorem by the same proof). One property left implicit: the solver must return the scalars $s_i$, since $\delta_{s_i}$ is applied (Finding 6).
- **"Smaller arities", line 679.** The Schedule 2 arity $(g_d+1)((\kappa_d-1)g_d+1)$ at $p \ge 16\kappa_d^{2\kappa_d+2}$ and the triangular $(g_d+1)(g_d+2)/2$ match the full version (`main.tex` line 765 and Proposition `prop:triangular-sde`). The block-steered count is misquoted: the full version's Remark `rem:sde-block-steered` gives $M_J(a) = \lfloor(a+2)^2/4\rfloor + [a\ \text{odd}]$ for $J = 3$ blocks and $a^2/(2(J-1)) + O(a)$ in general, where the block count is $J_d = \max(3,\kappa_d)$ (rule (R1) of `appendix-free-coordinate.tex`, line 202), not $\kappa_d$; and the option exists only for $\kappa_d \ge 2$. The core's "$\kappa_d \le 3$" includes $\kappa_d = 1$, where the general formula divides by zero and where the linear node with $g_d+1$ columns is used instead (Finding 1). The "$145$ to $143$" sentence matches $E_W(9) = 143$ (`main.tex` lines 380, 1135).
- **Schedule 3 sentences, line 679.** The time $2^{O(r\log(r+2))}\cdot\poly$ with the class not fixed matches `main.tex` line 1029 (Corollary `cor:fpt-r`, conditional, i.i.d. supply only). The fixed-class polynomial-time sentence matches Remark `rem:fc-witness-h3`(c) of the appendix, which uses weight-doubling nodes at the grades of $\Gamma_{\mathrm F}$ ($2 \le \kappa_d < p-1$) and, at a grade with $\kappa_d = p-1$ (possible only when $p = c+1$, $d = c$), either Schedule 1 or the weight-doubling zero-sum node. The core sentence mentions only the first kind (Finding 7). Nothing is claimed; the status labels are present.
- **Shortened Outlook, lines 673–685.** Now about half a page, with one pointer per item; the opening sentence disclaims every item. Fine for expert review.

---

## 3. Readability of the main theorem and the abstract for an HSP expert

**Theorem 1.2 as it stands** is one paragraph of eleven lines that mixes the input contract (already given in Definition 1.1 immediately above), internal names ("Schedule 1", "arity $M_d = B_d(g_d)$", "evaluation points $1,\dots,c$") that an expert does not yet know, the conclusion, the query count with its upper bound, and the gate set. The symbol $g_d$ appears in the query count without being recalled (it is defined on line 100), and $t$ is the Rees variable two lines earlier and the sample surplus here. An expert in quantum algorithms will want, in this order: what is given, what is output, with what resources, under what imported assumption. Concrete proposal (Finding 4): put the three inputs as an enumerated list, state the output, then the query count, then the explicit bound as a separate display with the one-line consequence "polynomial in $m$ for fixed $c$, independent of $p$ once $p \ge 3/\eps$"; move "evaluation points $1,\dots,c$, Schedule 1 with $M_d = B_d(g_d)$" to the sentence after the theorem, where the proof is located; recall $g_d = \dim\gamma_d(\mathcal{L})$ in the statement; rename the surplus. A one-sentence informal version before the theorem helps too:

```latex
In words: for every fixed $c$, the hidden subgroup problem in $p$-groups of class $c < p$, given by the structure constants of their Lazard Lie algebra, has a bounded-error quantum algorithm polynomial in $\log|G| = m\log_2 p$ for every hidden subgroup, with an explicit query count that depends on the arity of one imported classical subroutine.
```

**Abstract.** It is one paragraph of about 330 words with a 70-word third sentence, and it names "Rees cover", "graded dilation", "controlled-right-action channel" and "complete central character measurements" before an expert knows what the oracle is. Proposal (Finding 5): about 190 words in the order problem, obstacle, idea in two sentences, result, classical bound, status. Draft LaTeX is in Finding 5.

Two smaller readability points: the term "Lazard $p$-group" of the title is never defined in the text (Finding 9); and the result's relation to Ivanyos–Santha should be said in one sentence near the theorem ("the descent is theirs; the cover is what makes it apply to arbitrary $H$ in arbitrary $\mathcal{L}$"), which Section 1.4 does well but only on page 5.

---

## 4. Findings

Classification: **Error** (false or unsupported statement), **Gap** (missing justification or unverified dependence), **Imprecision** (true but misleading, incomplete or inconsistent), **Style**. Replacement text uses no `\mathsf`, `\mathrel`, `\begingroup`, `\aa` or `\ni`.

### Finding 1 (Imprecision). Line 679. Block-steered arity: wrong parameter and a vacuous case.

Current text (part):

> for the i.i.d.\ uniform labels of fresh ideal sources only, a block-steered variant needs $\lfloor(g_d+2)^2/4\rfloor+[g_d\text{ odd}]$ columns when $\kappa_d \le 3$, and $g_d^2/(2(\kappa_d-1))+O(g_d)$ in general, at primes large compared with $g_d^2$ and the number of nodes;

The full version (Remark `rem:sde-block-steered`, rule (R1)) uses $J_d = \max(3,\kappa_d)$ blocks, gives $a^2/(2(J-1)) + O(a)$ in the block count $J$, and offers the option only at grades with $\kappa_d \ge 2$. At $\kappa_d = 1$ the displayed general formula divides by zero and the linear node ($g_d+1$ columns) applies.

```latex
for the i.i.d.\ uniform labels of fresh ideal sources only, a block-steered variant with $J_d = \max(3,\kappa_d)$ blocks needs $\lfloor(g_d+2)^2/4\rfloor+[g_d\text{ odd}]$ columns when $\kappa_d \in \{2,3\}$, and $g_d^2/(2(J_d-1))+O(g_d)$ for $\kappa_d \ge 3$, at primes large compared with $g_d^2$ and the number of nodes (at $\kappa_d = 1$, $g_d+1$ columns suffice by linear algebra);
```

### Finding 2 (Imprecision; needs a human check of the source). Line 666. The Ettinger–Høyer–Knill query bound.

Current text (part):

> Ettinger, H{\o}yer and Knill determine $H$ in any finite group with $O(\log^2|G| + \log(1/\eps))$ queries~\cite[Theorem~2]{EttingerHoyerKnill2004}, here $O(m^2\log^2 p + \log(1/\eps))$, but with exponential-time processing.

I recall the EHK theorem as $O(\log|G|)$ queries, and their algorithm identifies $H$ with certainty, so the $\eps$ is foreign to it. The $O(\log^2|G| + \log(1/\eps))$ count is what the fidelity-counting argument of~\cite[Eq.~(10.10)]{ChildsQA}, used for the "copies" column of Table 1, gives (number of subgroups at most $|G|^{\log_2|G|}$). Either bound keeps the paper's point (a query separation per se is not new), but the attribution and the locator "Theorem 2" should be checked by a human with the source in hand. If my recollection is right:

```latex
Ettinger, H{\o}yer and Knill determine $H$ in any finite group with $O(\log|G|)$ queries~\cite{EttingerHoyerKnill2004}, here $O(m\log p)$, but with exponential-time processing (the counting argument of~\cite[Eq.~(10.10)]{ChildsQA}, used for Table~\ref{tab:query-crossover}, gives $O(\log^2|G| + \log(1/\eps))$ copies).
```

### Finding 3 (Imprecision). Lines 146, 148, 419, 545, 547, 554, 562. The letter $t$ is both the Rees variable and the sample surplus.

Current text (line 547, part):

> Induction from $d = c$ down to $d = 2$ gives $m+t$ independent exact copies of $\rho_{t\hh}$ on $t\mathcal{L} \cong \Fp^m$.

Here $t$ means two different things in one sentence; the same happens in Theorem 1.2 ($Q_{\mathrm q} = c(m+t)\dots$ two lines after $t\mathcal{L}$) and in Table 1's caption ("where $t = 1$"). Rename the surplus; $\tau$ is free in the core outside the proof of Theorem 6.1(i), where the ODE parameter can become $\xi$.

```latex
% Theorem 1.2 and Section 7, everywhere the surplus occurs:
With $\tau = \lceil\log_p(3/\eps)\rceil$, it makes at most
\[
  Q_{\mathrm q} = c\,(m + \tau)\prod_{d=2}^{c} B_d(g_d) \;\le\; \dots
\]
% line 547:
Induction from $d = c$ down to $d = 2$ gives $m+\tau$ independent exact copies of $\rho_{t\hh}$ on $t\mathcal{L} \cong \Fp^m$.
% Table 1 caption: "and $p \ge 11$, where $\tau = 1$"
% Proposition 8.2(v) uses its own $t = \lceil\log_p(2/\eps)\rceil$; rename it to $\tau$ as well.
```

### Finding 4 (Style). Lines 144–154. Restructure the main theorem statement.

Current text: the single-paragraph statement quoted in Section 3 above.

```latex
\begin{theorem}[Main theorem]
\label{thm:main}
Fix an integer $c \ge 1$, and let $B_d$ be the arity~\eqref{eq:Bd} of the Ivanyos--Santha solver, Theorem~\ref{thm:is-import}, which is imported and assumed. There is a quantum algorithm that, given
\begin{enumerate}[label=(\roman*),leftmargin=2em]
  \item a prime $p > c$ and the structure constants of a nilpotent Lie algebra $\mathcal{L} \cong \Fp^m$ with $\gamma_{c+1}(\mathcal{L}) = 0$, so that $G = (\mathcal{L},\ast)$ is a $p$-group of class at most $c$,
  \item a rational $\eps \in (0,1)$, and
  \item either \textup{(a)} a coherent oracle $U_f$ for a function $f : G \to \{0,1\}^w$ with $f(x) = f(y) \iff x^{-1}\ast y \in H$, or \textup{(b)} fresh independent copies of $\rho_H$, where $H \le G$ is an arbitrary subgroup,
\end{enumerate}
outputs, with probability at least $1-\eps$, a basis of $\hh = \log H$, and hence generators of $H$. Write $g_d = \dim_{\Fp}\gamma_d(\mathcal{L})$ and $\tau = \lceil\log_p(3/\eps)\rceil$. The algorithm makes at most
\[
  Q_{\mathrm q} = c\,(m + \tau)\prod_{d=2}^{c} B_d(g_d)
\]
queries in case~\textup{(a)}, or uses at most $Q_{\mathrm q}$ copies in case~\textup{(b)}, and $\poly_c(m,\log p,w,\log(1/\eps))$ further gates from a fixed finite universal gate set that implements $X$, CNOT and Toffoli exactly (for example Clifford$+T$), together with classical operations. Here
\[
  Q_{\mathrm q} \;\le\; C_c\, c\,(m+\tau)\,(m+1)^{\sum_{d=2}^c d\lceil\log_2(d+1)\rceil},
  \qquad
  C_c = \prod_{d=2}^c d^{\,d(d-1)\lceil\log_2(d+1)\rceil/2},
\]
so for fixed $c$ the query count is polynomial in $m$ and does not depend on $p$ once $p \ge 3/\eps$. No property of $H$, such as normality, is assumed. The guarantee is bounded-error, not exact.
\end{theorem}

The algorithm is the procedure of Section~\ref{sec:proof-main}: evaluation points $1,\dots,c$ and Schedule~1 (Section~\ref{sec:schedule1}) with arity $M_d = B_d(g_d)$ at every grade $d = 2,\dots,c$.
```

(The last sentence replaces the corresponding clause now inside the statement; Remark 1.3 follows unchanged.)

### Finding 5 (Style). Line 58. Shorter abstract.

Current text: the 330-word abstract.

```latex
\begin{abstract}
Let $G$ be a finite $p$-group of nilpotency class $c < p$, given by the structure constants of its Lazard Lie algebra $\mathcal{L} \cong \Fp^m$, and let $f$ hide an arbitrary subgroup $H \le G$. Beyond class two, the known polynomial-arity method for aligning random central characters, the degree-by-degree elimination of Ivanyos and Santha, needs automorphisms that preserve $H$ and scale the centre, and such automorphisms need not exist: the eight-dimensional class-three Dixmier--Lister algebra has no positive grading over $\Fp$ for $p > 3$. We do not grade $G$. We query $f$ at $c$ distinct nonzero evaluations of the graded cover $\A = \bigoplus_{k=1}^c t^k\gamma_k(\mathcal{L})$. The resulting oracle hides a homogeneous subgroup of the cover, which every graded dilation preserves, although the oracle uses no knowledge of $H$; one evaluation is not enough. The Ivanyos--Santha descent then removes the grades $c,\dots,2$ exactly, branch by branch, and grade one retains all of $\log H$, which abelian Fourier sampling recovers. With their fixed-degree diagonal-equation solver, the algorithm is bounded-error and runs in time polynomial in $m$, $\log p$, the label width and $\log(1/\eps)$ for every fixed $c$, with an explicit query count. In the same oracle model, for $m \ge 2$, the classical randomized query complexity is $\Theta(p^{(m-1)/2})$, even for non-normal hidden subgroups of order $p$. All proofs were checked by AI sessions only and are pending human review.
\end{abstract}
```

### Finding 6 (Imprecision). Line 158. Remark 1.3 omits that the solver must return the scalars.

Current text (part):

> it is total, returning a nonzero solution of~\eqref{eq:sde-target} for any $M_d$ label columns in $\Fp^{g_d}$ and every prime $p > c$;

Proposition 4.3 applies $\delta_{s_i}$, so the proof needs the $s_i$ themselves, not only the powers $s_i^d$ (Remark 5.2(a)); a solver that returned $s_i^d$ would need deterministic root extraction, which is not available.

```latex
it is total, returning the scalars $s_1,\dots,s_{M_d}$ of a nonzero solution of~\eqref{eq:sde-target} (not only their $d$-th powers, Remark~\ref{rem:is-import}(a)) for any $M_d$ label columns in $\Fp^{g_d}$ and every prime $p > c$;
```

### Finding 7 (Imprecision). Line 679. The fixed-class Schedule 3 sentence omits the grade with $\kappa_d = p-1$.

Current text (part):

> at fixed class, with weight-doubling witness nodes at the grades with $2 \le \kappa_d < p-1$, it would give polynomial classical time at every prime $p > c$,

The full version's Remark `rem:fc-witness-h3`(c) also needs a node at a grade with $\kappa_d = p-1$, which exists only when $p = c+1$ (then $d = c$); there it uses Schedule 1 or the weight-doubling zero-sum node.

```latex
at fixed class, with weight-doubling witness nodes at the grades with $2 \le \kappa_d < p-1$ and Schedule~1 at a grade with $\kappa_d = p-1$ (which occurs only for $p = c+1$), it would give polynomial classical time at every prime $p > c$,
```

### Finding 8 (Style). Line 317. One clause for the nilpotency of the derivations.

Current text (part):

> Every such $D$ maps $\mathcal{L}_{\mathrm{DL}}$ into $[\mathcal{L}_{\mathrm{DL}},\mathcal{L}_{\mathrm{DL}}] = \Span(e_5,\dots,e_8)$ and that space into $\Span(e_7,e_8)$, which it kills, so $D^3 = 0$ and every derivation is nilpotent.

The second and third inclusions follow from the first by the derivation rule, but the reader has to see this; say so.

```latex
Every such $D$ maps $\mathcal{L}_{\mathrm{DL}}$ into $[\mathcal{L}_{\mathrm{DL}},\mathcal{L}_{\mathrm{DL}}] = \Span(e_5,\dots,e_8)$, hence, by the derivation rule $D[x,y] = [Dx,y] + [x,Dy]$, maps $\gamma_2$ into $[\gamma_2,\mathcal{L}_{\mathrm{DL}}] = \gamma_3 = \Span(e_7,e_8)$ and $\gamma_3$ into $\gamma_4 = 0$, so $D^3 = 0$ and every derivation is nilpotent.
```

### Finding 9 (Style). Line 49 (title) and Section 2. "Lazard $p$-group" is never defined.

Current text (line 200, part): "By the Lazard correspondence~\cite{Lazard1954,Khukhro1998}, the subgroups of $(\mathcal{L},\ast)$ are exactly the Lie subalgebras of $\mathcal{L}$, ..."

```latex
We call a finite $p$-group of nilpotency class $c < p$ a \emph{Lazard $p$-group}; every such group is $(\mathcal{L},\ast)$ for its Lazard Lie algebra $\mathcal{L}$. By the Lazard correspondence~\cite{Lazard1954,Khukhro1998}, the subgroups of $(\mathcal{L},\ast)$ are exactly the Lie subalgebras of $\mathcal{L}$, ...
```

### Finding 10 (Imprecision). Line 585. The label-set size is an assumption, not a fact.

Current text (part):

> The label set has at least $|G|$ elements.

Definition 1.1 allows any $w$. The sentence is a standing assumption of this section, forced only because $H = 1$ is an admissible hidden subgroup.

```latex
We assume $2^w \ge |G|$, as the hidden subgroup $H = 1$ requires.
```

### Finding 11 (Style). Line 657 (Table 1, class-9 row). A non-prime in a column of primes.

Current text (part): `$2^{174.72}$ & $2^{174.47}$`

The caption says the column lists the smallest prime; for this row the entries are thresholds in logarithmic form. Mark them.

```latex
class-$\ReesClassNineClass$ profile & 9 & 19 & $(17,16,14,12,9,6,3,1)$ & $1572.66$ & $\approx 2^{174.7}$ & $\approx 2^{174.5}$ & $62{,}909$ \\
```

and add to the caption: "For the last row the two threshold columns give the approximate size of the threshold rather than a prime."

### Finding 12 (Style). Throughout. Frequency of the status tag.

"AI-checked, pending human review" or an equivalent occurs about twelve times (abstract, title footnote, Section 1.6, Theorem 5.1's title, Remark 5.2(e), the proof of Theorem 6.1(iii), five times in Section 9, Appendix A). For the expert-review round this is acceptable and even helpful; for journal submission keep it in the title footnote, Section 1.6, and at each imported or conditional statement only (Theorem 5.1, Remarks 5.2–5.3, Section 9's opening sentence), and drop the per-paragraph tags in Section 9.

```latex
% Section 9, each paragraph: delete the trailing "Status: ...; AI-checked, pending human review." and "All AI-checked, pending human review." once the opening sentence of the section carries the disclaimer.
```

---

Tally: 12 findings. Errors: 0. Gaps: 0. Imprecisions: 6 (Findings 1, 2, 3, 6, 7, 10). Style: 6 (Findings 4, 5, 8, 9, 11, 12).

---

## 5. Status of referee 17's findings

Checked against the current `core/main-core.tex`.

| 17-F | Topic | Status now |
|---|---|---|
| F1 (Gap) | Controlled-oracle guard | Resolved (line 480: any unitary extension of $U_f$; no guard). |
| F2 (Gap) | AI-only reading of Ivanyos–Santha; abstract arity | **Partially resolved.** Remark 1.3 (`rem:main-solver`) now states the four solver properties the proof uses and says any solver with them gives the theorem; Remark 5.3 ends with the explicit sentence that $B_d$ and the exponent $145$ rest on the AI-only reading. The restructuring into an abstract arity plus corollary was not done (owner decision). For the expert-review round this is adequate: the experts are the humans who must confirm the reading. For journal submission the restructuring, or confirmation with the source's authors, remains the decisive step. |
| F3 | Lemma 3.5 hypothesis | Resolved (line 287). |
| F4 | Abstract: field for non-gradability | Resolved (line 58). |
| F5 | Table 1 (v) column rounding | Resolved (caption, line 645; both conventions given, values reproduce). |
| F6 | Bracket count qualifier | Resolved (line 488). |
| F7 | Kitaev phase claim and flag | Resolved (line 508: sentence removed, visible hedge and pointer to the explicit construction, comment restored at line 509). |
| F8 | Non-canonical label strings | Resolved (line 533). |
| F9 | Input validation | Resolved (line 128, as a promise). |
| F10 | "at most" queries | Resolved (line 146). |
| F11 | Abelian-by-cyclic step | Resolved (line 171). |
| F12 | "special cases" | Resolved (line 167). |
| F13 | Solver polynomial depends on $d$ | Resolved (line 434). |
| F14 | Bijectivity of $\delta_\theta$ | Resolved (line 240). |
| F15 | Lazard sentence in general lemma | Resolved (line 347). |
| F16 | Diamond norm | Resolved (line 202). |
| F17 | Vacuous grades | Resolved (line 473). |
| F18 (Style) | Date boilerplate; Outlook length | **Mostly resolved.** Date moved to a `\thanks` footnote (line 52); Outlook cut to about half a page (lines 673–685). The per-paragraph status tags remain (Finding 12 here). |
| F19 | Bibliography drift | Resolved (Appendix A, line 703; the build finds every citation). |
| F20 | Invisible hedge on van de Woestijne | Resolved (line 437, visible hedge; comment kept at line 438). |
| F21 | Register bound assumptions | Resolved (line 491). |
| F22 | Row certificates | Resolved (line 317, says what a certificate is). |

Referee 17's Section 5 (statements stronger in the core than in the companion): items 1–3, 6, 7 were fixed through F6, F3, F10, F7, F5; items 4 and 5 were judged acceptable there and are unchanged. I found no new divergence between core and companion in the proved material; the one divergence in the new Outlook text is Finding 1.

---

## 6. What a human expert must check first

1. **Theorem 5.1, Section 5 (p. 13–14).** Against arXiv:1503.09016v2, Theorem 11 and the proof of Theorem 3, Sections 3.1–3.3: (a) that the algorithm is deterministic and total at $G(d,a)^{\lceil\log_2(d+1)\rceil}$ columns for arbitrary columns, (b) that it returns the scalars $s_i$, (c) that it is valid for every prime with $d \mid p-1$, including $d = p-1$, and (d) whether the printed bound of their Theorem 3 is indeed weaker than what the proof gives (Remark 5.3). Everything in Theorem 1.2 except the explicit arity survives any outcome (Remark 1.3); the number $145$ does not.
2. **Proposition 4.3 with Lemma 4.2, Section 4.2 (p. 10–11).** The exact, branch-by-branch quotient conversion is the heart of the paper and the step the authors call new in combination. Ten minutes with the trace computation suffice.
3. **Lemma 3.2 and Theorem 3.1(iii), Section 3.1–3.2 (p. 7–8).** Interpolation across $c$ evaluations and the $\mathbb{Z}[1/c!]$ specialization of the BCH identities.
4. **Novelty, Section 1.4 (p. 5–6).** Whether homogenizing the hidden subgroup on the Rees cover appears anywhere in the HSP or Lie-algebra literature; the paper's own search was AI-run and the "may be new" is unassessed by any expert.
5. **Section 6 (p. 15–17).** The operator-norm reading of Kitaev's Fourier transform (Theorem 6.1(iii)) and that the hybrid Lemma 6.2 is applied with the right subspaces; also the locators in Kitaev 1995, Cleve–Watrous 2000 and van de Woestijne 2005.
6. **Section 8 (p. 18–21).** Proposition 8.2, in particular (v); correct as far as I can tell, so this is a short read.
7. **Citations to check with the sources:** Ettinger–Høyer–Knill "Theorem 2" and its bound (Finding 2); Childs eq. (10.10); Olson 1969 for the Davenport constant of $C_p^2$; Lidl–Niederreiter Chapter 6 for Chevalley–Warning.

---

## 7. Recommendation

Send to human experts after applying Findings 1, 3, 6, 7 and 10 (fifteen minutes of edits, no proof changes), and preferably Findings 4 and 5 (readability of the theorem and abstract, which the owner asked for). Finding 2 should be checked by whoever has the EHK paper at hand; if the recollection here is right, the current sentence understates a cited result, which is harmless but untidy. Findings 8, 9, 11 and 12 can wait for the journal round.

The core's own mathematics is, as far as I can verify, correct and complete, the classical section is finished, and the paper is unusually clear about what it imports and what it does not claim. What it needs now is a human reading of Ivanyos–Santha 2015 and a human opinion on novelty, which is exactly the review being requested.
