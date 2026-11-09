# Referee report 17: core version of the Rees/HSP paper

Manuscript: `docs/papers/rees-hsp/core/main-core.tex` (dated 5 November 2026, 27 pages when built with `core/numbers.tex` and `core/references.bib`). Companion consulted: `docs/papers/rees-hsp/main.tex` with `appendix-*.tex`, only to check deferred steps and to compare statements.

Referee: independent, read-only pass, 5 November 2026. All checks below were done by hand and with short exact computations (`/opt/anaconda3/bin/python`, sympy) on the Dixmier–Lister algebra, the arity formulas and the table. Line numbers refer to `core/main-core.tex` as of this date.

Build note. `latexmk -pdf` on `core/main-core.tex` compiles cleanly with `core/references.bib` (27 pages, no undefined references). With `../references.bib`, as the referee brief suggested, the citation `Olson1969` is undefined: it exists only in `core/references.bib` (line 353), while `../references.bib` has twelve entries the core copy lacks. The two files have drifted (Finding 19).

---

## 1. Summary of the claimed contributions (in my words)

The paper treats the hidden subgroup problem (HSP) in a finite $p$-group $G$ of nilpotency class $c<p$, given explicitly through its Lazard Lie algebra $\mathcal{L}\cong\mathbb{F}_p^m$ (structure constants), with an arbitrary hidden subgroup $H\le G$, and either a coherent oracle $U_f$ or fresh copies of the coset state $\rho_H$.

1. **Lift to a graded cover.** Instead of grading $G$ (impossible in general: the Dixmier–Lister algebra has only nilpotent derivations), the paper forms the positive lower-central Rees algebra $\mathcal{A}=\bigoplus_{k=1}^c t^k\gamma_k(\mathcal{L})$, which is positively graded, carries dilation automorphisms $\delta_\theta$ and evaluation homomorphisms $E_s:\mathcal{A}\to\mathcal{L}$, and is a Lazard group $\widetilde G$ for the same $p$. Querying $f$ at $c$ distinct nonzero evaluations yields a tuple oracle that hides exactly the *homogeneous* subgroup $\exp(\widetilde{\mathfrak h})$, $\widetilde{\mathfrak h}=\bigoplus_k t^k(\mathfrak h\cap\gamma_k(\mathcal{L}))$ (Vandermonde interpolation, Lemma 3.2). A single evaluation does not suffice (Proposition 3.4). $c$ copies of $\rho_H$ give the same lifted source without an oracle (Lemma 3.5).

2. **Exact grade-by-grade descent.** On the quotient $G_d$ of the cover by grades $>d$, the top grade $Z_d$ is central and scaled by $s^d$ under $\delta_s$, and $\delta_s$ preserves the (homogeneous) hidden subgroup. Measuring the full $Z_d$-character on $M_d$ fresh sources, solving the homogeneous diagonal system $\sum_i s_i^d\lambda_i=0$ for the measured labels, and applying controlled right actions by $\delta_{s_i}(\sigma(q))$ produces *exactly* one coset state of $G_{d-1}$ for every label tuple and every nonzero solution (Proposition 4.3). Grade one is a copy of all of $\mathcal{L}$, so abelian Fourier sampling at the end recovers all of $\mathfrak h=\log H$, including derived directions.

3. **Schedule 1 and the main theorem.** With the deterministic fixed-degree diagonal-equation solver of Ivanyos and Santha (imported as Theorem 5.1, with a gcd reduction to $\kappa_d=\gcd(d,p-1)$), the procedure is bounded-error and runs in time $\mathrm{poly}_c(m,\log p,w,\log(1/\varepsilon))$ with explicit query count $Q_{\mathrm q}=c(m+t)\prod_{d=2}^cB_d(g_d)$, exponent of $m$ about $c^2\log c$ (145 at $c=9$). Gate compilation is by exact reversible arithmetic plus approximate $\mathrm{QFT}_{\mathbb{F}_p}$, with an additive error composition on canonical subspaces (Lemma 6.2).

4. **Classical query complexity.** In the same oracle model the classical randomized query complexity is $\Theta(p^{(m-1)/2})$ for $m\ge2$ (collision lower bound, even for non-normal $H$ of order $p$; birthday upper bound with explicit constants), giving a query separation that the paper itself qualifies (large constants, oracle model only, no concrete application).

5. **Outlook.** Conditional extensions (Schedules 2 and 3, derived-dimension and codimension bounds, prime-power rings, black-box groups, subspace sources) are described in prose with pointers to the companion; none is claimed.

The paper is explicit that everything was written and checked by AI sessions only.

---

## 2. Correctness assessment

I checked every proof in the core line by line. Verdict: **I found no mathematical error in any statement the core proves.** The weight of the paper rests on one imported theorem that neither I nor (by the paper's own account) any human has verified against the source. Details by layer.

### 2.1 Quantifiers, access model, query versus time

- Quantifiers (Theorem 1.3): $c\ge1$ is fixed first; the algorithm is then uniform in the prime $p>c$, in $\mathcal{L}$ (any nilpotent Lie algebra with $\gamma_{c+1}=0$, so $c$ may be a strict upper bound on the class), in $H$ (arbitrary, no normality) and in $\varepsilon$. The polynomial degree depends on $c$ and the bound is explicitly not uniform in $c$. This is stated correctly.
- Access model: coherent oracle $U_f|g,z\rangle=|g,z\oplus f(g)\rangle$ with $w$-bit labels, specified on canonical encodings only; or fresh independent copies of $\rho_H$. Both routes are treated (Lemmas 3.3 and 3.5). One inconsistency: Section 6 "guards" each oracle call by applying $U_f$ *controlled* on a flag qubit, which presumes controlled-$U_f$ access that Definition 1.2 does not grant (Finding 1). The guard is unnecessary: Lemma 6.2 only needs the implemented step to be a channel on the full space, and any unitary extension of $U_f$ is one. The fix is a few words.
- Query versus time: queries are counted exactly ($c$ per lifted source, $P=\prod M_d$ lifted sources per terminal sample, $m+t$ terminal samples); the count is independent of $p$ once $p\ge3/\varepsilon$. Time is bounded only as $\mathrm{poly}_c$; the solver's time is inherited from the import ("$\mathrm{poly}(M,\log p)$ for fixed $d$", degree unspecified). For a core version this is acceptable; the companion's Remark `rem:is-runtime` gives an explicit step bound with an uncomputed constant.
- The classical lower bound is in the classical query model with a label set of size at least $|G|$; the quantum upper bound allows any $w$. The two models agree for the problem as posed (all $H$, including $H=1$), which forces $w\ge m\log_2p$. Fine.

### 2.2 Layer 1: the cover and the lift (Section 3)

- Theorem 3.1(i)–(iii): checked. The class computation, centrality of the top grade, $E_s\circ\delta_\theta=E_{\theta s}$, and the $\mathbb{Z}[1/c!]$ argument for the truncated BCH product (Dynkin denominators divide products of integers $\le N\le c$; identities hold in the free nilpotent Lie ring over $\mathbb{Z}[1/c!]$, which is a free module embedding into its $\mathbb{Q}$-form; specialize to $\mathbb{F}_p$, $p>c$) are correct. The proof of (ii) omits bijectivity of $\delta_\theta$ (inverse $\delta_{\theta^{-1}}$), which the companion includes (Finding 14).
- Lemma 3.2 (exact homogenization): correct. The matrix $(s_i^k)$ is $\mathrm{diag}(s_i)$ times a Vandermonde matrix; since $\mathfrak h$ is a subspace, invertibility gives $C_k\in\mathfrak h$ for all $k$. The intersection form $\bigcap_{s\in\mathbb{F}_p^\times}E_s^{-1}(\mathfrak h)$ needs $p-1\ge c$ distinct nonzero points, which $p>c$ supplies. Dilation invariance via $\delta_\theta(E_s^{-1}\mathfrak h)=E_{s/\theta}^{-1}\mathfrak h$ is correct.
- Lemma 3.3 (lifted source): correct; the matrix-entry computation and the convention $\langle x|\rho_H|y\rangle=|G|^{-1}1_H(x^{-1}y)$ agree.
- Proposition 3.4: correct. $u=s\,tz-t^2z$ lies in $\mathcal{A}$ because $z\in\gamma_2$; $E_s(\delta_\theta u)=s^2\theta(1-\theta)z$. The $\mathbb{F}_3$ example checks ($\delta_2(u)=2tz-4t^2z=2tz-t^2z$).
- Lemma 3.5 (copy-only lift): the trace identity $\mathrm{tr}(R_{g_a}\rho_HR_{g_b}^\dagger)=1_H(g_b^{-1}g_a)$ and the use of Lemma 3.2 are correct. The statement omits the hypothesis that the points are distinct and nonzero (Finding 3).
- Section 3.4 (Dixmier–Lister): I recomputed. The ten brackets satisfy Jacobi (all 56 triples); the derivation system has 224 equations in 64 unknowns, rank 52 over $\mathbb{Q}$ and modulo $p=5,7,11,13,101,10007$, so $\dim\mathrm{Der}=12$; every derivation maps $\mathcal{L}$ into $\mathrm{span}(e_5,\dots,e_8)$ at these primes; lower central dimensions $(8,4,2)$, cover dimension 14. The "divide the degrees by their gcd" argument for non-gradability is correct. I did not check the 32 integer row certificates, which are what carries the claim to *every* $p>3$.

### 2.3 Layer 2: instrument, conversion, recursion (Section 4)

- Lemma 4.1 (instrument): correct; $\Pi_\lambda$ are the central character projectors, the ancilla ends in $F|\lambda\rangle$, and the $F^\dagger$ readout gives $\lambda$. The sentence "$x\ast(-z)=x-z$ in coordinates" belongs to the Lazard application, not to the general finite-group setting of the subsection (Finding 15).
- Lemma 4.2 (branch law): $\mathrm{tr}(\rho_H\Pi_\lambda)=|Z|^{-1}\sum_{z\in K}\chi_\lambda(-z)=|K|/|Z|\cdot[\lambda\in K^\perp]$, $\rho_\lambda$ as displayed, $\mathrm{tr}(\rho_\lambda R_g)=\chi_\lambda(z)$ on $g=hz$ with the $|K|$-fold multiplicity cancelling: all correct. No transversality or normality needed, as claimed.
- Proposition 4.3 (pointwise conversion): correct and the heart of the paper. The output entry at $(q,r)$ is $|Q|^{-1}\prod_{i\ \mathrm{active}}\mathrm{tr}(\rho_{\lambda_i}R_{\delta_{s_i}(g)})$ with $g=\sigma(r)^{-1}\sigma(q)$; off $HZ$ every active factor vanishes (the active set is nonempty); on $g=hz$ the factors multiply to $\chi_{\sum_is_i^d\lambda_i}(z)=1$. The result is the coset density of $HZ/Z$ on $Q$, for every label tuple. The independence remark (outputs do not depend on the record) is correct and is what makes the tree recursion legitimate.
- Remark 4.4: the $\mathrm{SUM}$ computation $|\chi_a\rangle|\chi_b\rangle\mapsto|\chi_{a-b}\rangle|\chi_b\rangle$ is right, and "output character $4$" refers to the last register, consistent with the sentence that follows.
- Section 4.3 (recursion): $\bigoplus_{k>d}\mathcal{A}_k$ is a $\delta$-stable ideal; $Z_d$ central in $\mathcal{A}^{(d)}$; $H_d$ homogeneous; $K_d=t^d(\mathfrak h\cap\gamma_d)$; $H_dZ_d/Z_d=H_{d-1}$; zero-insertion section is public; $G_1=t\mathcal{L}$ additive with $H_1=t\mathfrak h$. The generator argument from a basis of $\mathfrak h$ via the subgroup form of Lazard is correct. Leaf count $P=\prod M_d$ is correct.

### 2.4 Layer 3: Schedule 1 (Section 5)

- Theorem 5.1 is imported and is the single point of failure. What the proof of Theorem 1.3 actually uses: (a) deterministic, (b) total at arity $B_d(a)$ for arbitrary columns, (c) returns the scalars $s_i$ themselves, (d) polynomial time for fixed $d$, (e) only for $d\mid p-1$. The paper is candid that this reading is AI-only and, in Remark 5.3, asserts that the bound printed in the source's Theorem 3 is weaker than what its proof gives. The arithmetic of that remark is right ($d\lceil\log_2(d+1)\rceil>d\log_2d$ for $d\ge2$; at $d=2$, $a=1$ both bounds give 64, so the discrepancy is only visible for larger $a$), but whether the source's proof gives $G(d,a)^{\lceil\log_2(d+1)\rceil}$ I cannot confirm offline. **This must be verified by a human against arXiv:1503.09016v2 before acceptance** (Finding 2). I note that (c) is almost certainly right for any algorithm that *solves* a diagonal system, since the unknowns are the $s_i$; the risk is in (b) and the exact arity.
- Lemma 5.4 (reduced degree): correct. With $ud+v(p-1)=\kappa$, $u\ge0$, $s_i=x_i^u$ gives $s_i^d=x_i^\kappa$ on nonzero $x_i$, same support; $B_d(a)$ is increasing in $d$; $B_1(a)=a+1$. The edge case $\kappa=p-1$ (possible only when $d=c=p-1$) works with $u=0$.
- Remark 5.5 (zero-sum, $p=5$, $d=4$, $a=2$): the eight columns have no nonempty zero-sum subsequence, and the Davenport constant $2p-1=9$ is correctly quoted. $B_4(2)=G(4,2)^3=36520347436056576\approx3.7\cdot10^{16}$: checked.
- Schedule 1 paragraph: consistent with Theorem 5.1 and Lemma 5.4. When $g_d=0$ (class of $\mathcal{L}$ strictly below $c$) the stage is vacuous but still charged $B_d(0)>1$ columns (Finding 17).

### 2.5 Layer 3: compilation and error composition (Section 6)

- Theorem 6.1(i): the ODE $Z'=\psi(\mathrm{ad}_Z)Y$, $\psi(z)=z/(1-e^{-z})=1+z/2+\sum_{k\ge2}B_kz^k/k!$, the coefficient recurrence $(j+1)Z_{j+1}=\sum_k(\beta_k/k!)W^{(k)}_j$, the dependency order, and the memoized count $(d-1)\sum_{o<d}(o+1)=(d-1)d(d+1)/2$ are correct. Von Staudt–Clausen gives denominators of $B_k$ as products of primes $q$ with $q-1\mid k$, hence $q\le d$; coefficients in $\mathbb{Z}[1/d!]$. Note the artifact implements the *unmemoized* recurrence with $(d-1)d(d+1)(d+2)/6$ brackets, and the companion states only that count (Section 5 below).
- (ii): the four-pass clean in-place product is correct (compute–copy–uncompute, then erase $v$ via $(-u)\ast(u\ast v)$).
- (iii): imported from Kitaev with Solovay–Kitaev synthesis; the $\eta/2+\eta/2$ split and $\varepsilon'=\eta^2/(16p)$ are consistent with the quoted precision $2(q\varepsilon')^{1/2}$. The claim that the bound is on the isometry $CJ$ "not only on output probabilities" is an AI reading of the source; the companion flags its Kitaev locator as needing human verification and the core does not (Finding 7). The inverse-transform bound after the proof is a correct one-line identity.
- (iv): the register count $2+\sum_{d\ge2}(M_d-1)$ is correct for depth-first evaluation with reset of consumed registers.
- Lemma 6.2 (hybrid on a canonical domain): the telescoping argument is standard and correct; the application paragraph (pure-state bound $\sqrt{1-|\langle\phi|\phi'\rangle|^2}\le\|\phi-\phi'\|$, convexity, classical control as a mixture) is correct. One point left implicit: the implemented classical solver must be defined on non-canonical label strings that the approximate $F^\dagger$ can produce (Finding 8).
- Corollary 6.3 and the $N_{\mathrm{QFT}}$ count in Section 7: checked; $N_d=\prod_{d'<d}M_{d'}$ is the number of stage-$d$ merges per tree; total error $\varepsilon/3+\varepsilon/3<\varepsilon$.

### 2.6 Assembly (Section 7)

The proof of Theorem 1.3 composes the three layers correctly. The induction from $d=c$ down to $2$ produces $m+t$ independent exact copies of $\rho_{t\mathfrak h}$; Lemma 2.1 gives failure $\le1/((p-1)p^t)\le\varepsilon/3$ with $t=\lceil\log_p(3/\varepsilon)\rceil$ (checked, including $k=0$). The query count and the bound $B_d(g_d)\le d^{d(d-1)\lceil\log_2(d+1)\rceil/2}(m+1)^{d\lceil\log_2(d+1)\rceil}$ are right; the exponent $1+\sum_{d=2}^9d\lceil\log_2(d+1)\rceil=145$ is right. The Heisenberg example (both the non-normal line and the central line) is right, including $B_2(1)=64$ and the Chevalley–Warning remark.

### 2.7 Classical query complexity (Section 7.2)

- Lemma 7.3 (collision bound): the lazy-sampling coupling and the divergence condition ($x_j$ in a new $K$-coset but an old $H$-coset, hence $x_i^{-1}x_j\in H\setminus K$) are correct; the averaging argument in (i) and the decision version (ii) are correct.
- Proposition 7.4: (i)–(iv) checked, including the counts $(p^m-p^z)/(p-1)\ge p^{m-2}(p+1)\ge p^{m-1}+1$, "a one-dimensional ideal of a nilpotent Lie algebra is central", and the arithmetic $q^2\ge2(1-\delta)p^{m-1}-2\delta+q>2(1-\delta)p^{m-1}$. (v): the independence of the $e$ in-coset differences given the coset pattern, the Burnside-basis hyperplane bound, the coupling $e\ge X$ on $\{e<s\}$, the Chernoff step $\Pr[X\le\mu_X/2]\le e^{-\mu_X/8}$, and both cases $Q-s\le M$ and $Q-s>M$ are correct. The $\Theta$ statement follows with $m\le2p^{(m-1)/2}$.
- Table 1: I recomputed $\log_2Q_{\mathrm q}$ (9.00, 27.76, 33.19, 35.06, 1572.66) and the "LB $>Q_{\mathrm q}$ from" column (443, 337853, 92107, 997, $2^{174.7}$): all agree. The "(v) $<Q_{\mathrm q}$ for $p<$" column does **not** follow from the displayed formula in (v): with $8\ell=8\ln6\approx14.33$ I get 86, 121497, 42773, 642 instead of 84, 119671, 42290, 638. The companion's caption explains that the artifact rounds $8\ell$ up to 15; the core caption dropped that sentence (Finding 5). The "copies" entry 81 for the Heisenberg row reproduces from $\lceil4\log_2(3r)\rceil$ with $r$ the number of subspaces of $\mathbb{F}_{443}^3$.

---

## 3. Novelty and positioning, as the paper states it

The paper is unusually explicit about what is and is not new, and I take its account at face value (no web search was permitted).

- **Not new, by the paper's own account:** the degree-by-degree elimination with scalar weights is the mechanism of Ivanyos–Santha 2015, Theorem 5, Section 5; the fixed-class, growing-prime regime appears already in Bacon–Childs–van Dam (hidden subgroups of order $p$ in $\mathbb{F}_p\ltimes\mathbb{F}_p^m$, $m$ constant) and Ivanyos–Santha, Corollary 8 (constant class, $m$ unrestricted, via the hidden polynomial graph problem); a query separation per se is not new (Ettinger–Hoyer–Knill).
- **Claimed as possibly new:** using the positive lower-central Rees cover so that (a) the dilations exist for every Lazard group, including characteristically nilpotent ones such as Dixmier–Lister, and (b) the hidden subgroup on the cover is automatically homogeneous for arbitrary $H$, which sidesteps the obstruction noted by Imran–Ivanyos that automorphisms nearly preserving $H$ need not exist beyond class two. The interpolation lemma (Lemma 3.2) is the device that makes (b) work, and Proposition 3.4 shows it cannot be done with one evaluation.
- **Relative to Imran–Ivanyos 2023:** they solve bounded-class black-box nilpotent groups exactly when all primes are bounded, and pose bounded class with smooth order as open; the present paper gives a *non-exact* algorithm for explicit Lazard $p$-groups for every $p>c$, with scalar weights instead of zero-sum subsequences, in a different (explicit-chart) input model. The black-box composition is only sketched in the outlook and explicitly not claimed.
- **Relative to Morales 2026 and Holt–Subramanian 2026:** the paper gives a concrete group (free two-generator class-three Lazard group, order $p^5$) outside both families; the argument is correct.
- The paper states that its citation search was AI-run and not exhaustive.

My assessment: the positioning is honest and the comparison is fair. The one place where the core hardens the companion's language is Section 1.4 ("So these results are special cases of the regime of Theorem 1.3" versus the companion's "if Theorem 1.3 is correct, these results are special cases"), which is defensible since the core proves Theorem 1.3 modulo the import, but the sentence should make clear it compares scope, not running time (Finding 12). Whether the Rees-cover homogenization has appeared before in the HSP literature is exactly the kind of question that needs a human expert; I cannot settle it.

---

## 4. Findings

Classification: **Error** (a false or unsupported statement), **Gap** (a step whose justification is missing or depends on unverified input), **Imprecision** (true but misleading, incomplete or inconsistent), **Style**. Replacement text avoids `\mathsf`, `\mathrel`, `\begingroup`, `\aa`, `\ni`.

### Finding 1 (Gap). Line 475. The oracle guard presumes controlled oracle access.

Current text (line 475, second half):

> The oracle $U_f$ is specified only on canonical encodings, so each call is guarded: an exact reversible test sets a flag when every coordinate of the query register is below $p$, $U_f$ is applied controlled on the flag, and the flag is uncomputed. The guarded call is a unitary on the whole register space and agrees with $U_f$ on canonical inputs, so every implemented step is a channel on the full space, as Lemma~\ref{lem:hybrid} requires.

Definition 1.2 grants $U_f$, not a controlled version of it. Controlled-$U_f$ can be simulated (swap in a fixed canonical point $g_0$ and a register holding $f(g_0)$ learned with one extra query), but the paper neither says so nor charges the extra query. The guard is in fact unnecessary: Lemma 6.2 needs only that each implemented step be a channel on the full space, and any unitary extension of $U_f$ beyond the canonical subspace is one.

Proposed replacement:

```latex
The oracle $U_f$ is specified only on canonical encodings. We assume, as is standard, that the supplied black box is some unitary on the whole register space that agrees with $U_f$ on canonical inputs; which unitary is irrelevant, because Lemma~\ref{lem:hybrid} compares each implemented step with the ideal one only on ideal states, which are canonical, and otherwise needs only that every implemented step be a channel on the full space. No guard or controlled oracle call is needed.
```

### Finding 2 (Gap). Lines 427–430, 445–452. The main theorem rests on an AI-only reading of the imported solver, including a claim that the source's printed bound is wrong.

Current text (line 429):

> Let $d \ge 1$ be fixed and let $p$ be a prime with $d \mid p-1$. With $G(d,a)$ and $B_d(a)$ as in~\eqref{eq:Bd}, there is a deterministic classical algorithm that, given any $\lambda_1,\dots,\lambda_M \in \Fp^a$ with $M \ge B_d(a)$, outputs explicit field elements $s_1,\dots,s_M$, not all zero, with $\sum_{i} s_i^d\lambda_i = 0$, in time $\poly(M,\log p)$.

and (line 451):

> We use only the first inequality, which is what the proof establishes as we read it; this reading of the source is AI-only and has not been confirmed with the authors or by a human.

Everything in Theorem 1.3 except the explicit arity is independent of how one reads the source; the arity $B_d(a)$, and with it the exponent 145, is not. A journal cannot publish a theorem whose explicit bound rests on the referee-unverified assertion that a published theorem is misprinted. Two acceptable fixes: (a) have a human confirm the reading (ideally with the source's authors) and remove the hedges; or (b) restate Theorem 1.3 with an abstract arity function and give $B_d$ only as the instantiation. For (b):

```latex
\begin{theorem}[Main theorem]
\label{thm:main}
Fix an integer $c \ge 1$. Suppose that for each $d \le c$ there is a deterministic classical algorithm $\mathcal{S}_d$ and a function $A_d : \mathbb{N} \to \mathbb{N}$ such that, for every prime $p$ with $d \mid p-1$ and every $\lambda_1,\dots,\lambda_M \in \Fp^a$ with $M \ge A_d(a)$, $\mathcal{S}_d$ outputs field elements $s_1,\dots,s_M$, not all zero, with $\sum_i s_i^d\lambda_i = 0$, in time $\poly(M,\log p)$. [rest of the statement unchanged, with $B_d(g_d)$ replaced by $A_d(g_d)$ and the displayed bound on $Q_{\mathrm q}$ moved to Corollary~\ref{cor:main-is} below]
\end{theorem}

\begin{corollary}[With the Ivanyos--Santha solver]
\label{cor:main-is}
If Theorem~\ref{thm:is-import} holds as stated, Theorem~\ref{thm:main} applies with $A_d = B_d$, and then
$Q_{\mathrm q} = c\,(m + t)\prod_{d=2}^{c} B_d(g_d) \le C_c\, c\,(m+t)\,(m+1)^{\sum_{d=2}^c d\lceil\log_2(d+1)\rceil}$.
\end{corollary}
```

### Finding 3 (Imprecision). Lines 280–283. Lemma 3.5 omits the hypothesis on the evaluation points.

Current text (line 282):

> Exactly $c$ fresh copies of $\rho_H$ produce $\rho_{\exp(\hlift)}$ on $\widetilde{G}$, without any oracle.

The proof invokes Lemma 3.2, which needs $s_1,\dots,s_c\in\Fp^\times$ distinct. The companion's statement has this hypothesis; the core dropped it, which makes the core statement formally stronger and, read literally (any points), false.

```latex
Let $s_1,\dots,s_c \in \Fp^\times$ be distinct. Exactly $c$ fresh copies of $\rho_H$ produce $\rho_{\exp(\hlift)}$ on $\widetilde{G}$, without any oracle.
```

### Finding 4 (Imprecision). Line 58 (abstract). "no positive grading at all" lacks the field.

Current text:

> the eight-dimensional class-three Dixmier--Lister algebra admits no positive grading at all.

Section 3.4 proves this over $\Fp$ for $p>3$ (and the argument also works over $\mathbb{Q}$); as written in the abstract it is unqualified.

```latex
the eight-dimensional class-three Dixmier--Lister algebra admits no positive grading over $\Fp$ for any $p > 3$.
```

### Finding 5 (Imprecision). Line 639 (Table 1 caption). The "(v) $<Q_{\mathrm q}$" column does not follow from the formula in Proposition 7.4(v).

Current text (part of the caption):

> For $p$ below the value in the next column, the classical algorithm of Proposition~\ref{prop:classical-query}(v) uses fewer than $Q_{\mathrm q}$ queries.

Recomputing with the displayed $Q$ gives thresholds 86, 121497, 42773, 642 (the paper: 84, 119671, 42290, 638). The companion's caption explains that the artifact rounds $8\ell\approx14.33$ up to 15; the core dropped that sentence. Add it back:

```latex
For $p$ below the value in the next column, the classical algorithm of Proposition~\ref{prop:classical-query}(v) uses fewer than $Q_{\mathrm q}$ queries; this column is computed with $8\ell = 8\ln 6 \approx 14.33$ rounded up to $15$, which only enlarges $Q$, so the listed values are conservative (with $8\ell$ itself they are $86$, $121{,}497$, $42{,}773$ and $642$).
```

### Finding 6 (Imprecision). Line 483. Bracket count stronger than the companion's and than the artifact's.

Current text:

> the product $X \ast Y$ can be evaluated with at most $(d-1)d(d+1)/2$ bracket evaluations

The companion (`main.tex` line 797) states "exactly $(d-1)d(d+1)(d+2)/6$" for the implemented recurrence and only "optimized schedules may use fewer"; the core's own artifact list (line 714) says the implementation uses $(d-1)d(d+1)(d+2)/6$. The memoized count in the core proof is correct, but it is a claim no artifact exercises and the companion does not make. Either state both or add the memoization qualifier:

```latex
the product $X \ast Y$ can be evaluated with at most $(d-1)d(d+1)/2$ bracket evaluations when the coefficients $W^{(k)}_o$ of the recurrence below are stored and reused (the straightforward recurrence, implemented in \file{theorems/uniform_bch_rees.py}, uses $(d-1)d(d+1)(d+2)/6$)
```

### Finding 7 (Imprecision). Lines 485 and 503. The Kitaev import carries a claim about phases and no verification flag.

Current text (line 503, part):

> All internally controlled phase gates are synthesized with their relative phases, so the bound is on the isometry $CJ$, not only on output probabilities.

The companion's corresponding passage (`main.tex` lines 799–800) carries a `NEEDS HUMAN VERIFICATION` note on the Kitaev locator and offers an explicit alternative (its Lemma `lem:qft-mod`). The core drops both. Since Lemma 6.2 requires an operator-norm bound including phases, the core should either keep the flag visible or cite the explicit construction as the route it relies on:

```latex
All internally controlled phase gates are synthesized with their relative phases, so the bound is on the isometry $CJ$, not only on output probabilities. An explicit construction with the same guarantee and an explicit gate count, which does not depend on this reading of~\cite{Kitaev1995}, is given in the full version (Lemma on the approximate Fourier transform over $\mathbb{Z}/N$).
```

### Finding 8 (Imprecision). Line 527. Behaviour of the classical solver on non-canonical labels is unspecified.

Current text (part):

> The $j$-th step is either exact, with $\eta_j = 0$, or a single transform $\mathrm{QFT}_{\Fp}^{\pm1}$ on one coordinate, possibly classically controlled.

An approximate $F^\dagger$ can leave a label register in a basis state $\ge p$. The classical solver and the dilation table must be defined on such strings for the implemented step to be a channel on the full space, as the lemma requires. One sentence suffices:

```latex
The $j$-th step is either exact, with $\eta_j = 0$, or a single transform $\mathrm{QFT}_{\Fp}^{\pm1}$ on one coordinate, possibly classically controlled. Classical steps are defined on every bit string: a label coordinate holding a value $\ge p$ is reduced modulo $p$ before the solver runs, so every implemented step is a channel on the full space.
```

### Finding 9 (Imprecision). Line 128. Input validation.

Current text:

> a prime $p > c$, the dimension $m = \dim_{\Fp}\mathcal{L}$, and structure constants of a nilpotent Lie algebra $\mathcal{L} \cong \Fp^m$ of class at most $c$;

Either the input is promised to be a Lie algebra of class $\le c$ or the algorithm checks antisymmetry, Jacobi and $\gamma_{c+1}=0$ (all polynomial-time). Say which:

```latex
a prime $p > c$, the dimension $m = \dim_{\Fp}\mathcal{L}$, and structure constants of a nilpotent Lie algebra $\mathcal{L} \cong \Fp^m$ of class at most $c$ (antisymmetry, the Jacobi identity and $\gamma_{c+1}(\mathcal{L}) = 0$ are checked in time polynomial in $m$ and $\log p$, and the algorithm rejects otherwise);
```

### Finding 10 (Imprecision). Lines 146–153. "makes $Q_{\mathrm q}$ queries" versus the companion's "at most".

Current text (line 147, part): "it makes $Q_{\mathrm q} = \dots$ queries in case (a)". The companion says "at most $Q$". The procedure does make exactly $Q_{\mathrm q}$ calls, so the core is not wrong, but when $g_d=0$ at some grade the count is wasteful (Finding 17), and "at most" costs nothing:

```latex
it makes at most
```

### Finding 11 (Imprecision). Line 166. The abelian-by-cyclic step omits the exponent argument.

Current text:

> So $G$ has no abelian subgroup of index $p$ and is not abelian-by-cyclic.

The implication needs that $G$ has exponent $p$, so a cyclic quotient has order at most $p$; the companion spells this out.

```latex
So $G$ has no abelian subgroup of index $p$. Since $G$ has exponent $p$, every cyclic quotient of $G$ has order at most $p$, so $G$ has no abelian normal subgroup with cyclic quotient: it is not abelian-by-cyclic.
```

### Finding 12 (Imprecision). Line 162. "special cases" conflates scope with efficiency.

Current text:

> So these results are special cases of the regime of Theorem~\ref{thm:main} when $p > c$

The groups and hidden subgroups treated there are instances of the present setting, but no comparison of running times or query counts is made, and the present exponents are enormous. Replace with:

```latex
So the instances treated by these results are, when $p > c$, instances of the setting of Theorem~\ref{thm:main}; we do not compare running times, and the bounds of those papers are not implied by ours
```

### Finding 13 (Imprecision). Line 429. The solver's polynomial depends on $d$.

Current text (end of Theorem 5.1): "in time $\poly(M,\log p)$."

```latex
in time polynomial in $M$ and $\log p$, where the polynomial depends on $d$.
```

### Finding 14 (Imprecision). Line 235. Bijectivity of $\delta_\theta$ not shown.

Current text (part): "The dilation satisfies $\delta_\theta([t^i x, t^j y]) = \theta^{i+j} t^{i+j}[x,y] = [\delta_\theta(t^i x), \delta_\theta(t^j y)]$, and ..."

```latex
The dilation satisfies $\delta_\theta([t^i x, t^j y]) = \theta^{i+j} t^{i+j}[x,y] = [\delta_\theta(t^i x), \delta_\theta(t^j y)]$, is bijective with inverse $\delta_{\theta^{-1}}$, and
```

### Finding 15 (Imprecision). Line 342. A Lazard-specific sentence inside a general finite-group lemma.

Current text (part): "Since $z$ is central, $x \ast (-z) = x - z$ in coordinates, so $R_z$ is a subtraction."

Section 4.1 is stated for an arbitrary finite group $G$; the coordinate statement only makes sense for $G=G_d$.

```latex
In the application to $G = G_d$ (Section~\ref{sec:recursion}), $z$ is central, so $x \ast (-z) = x - z$ in coordinates and $R_z$ is a subtraction on the top-grade coordinates.
```

### Finding 16 (Style). Line 197. Diamond norm defined but never used in the core.

Current text (part): "Trace distance is $\frac12\|\cdot\|_1$, and for channels we use the normalized diamond norm $\frac12\|\cdot\|_\diamond$."

```latex
Trace distance is $\frac12\|\cdot\|_1$.
```

### Finding 17 (Style). Line 468. Vacuous grades are charged full arity.

Current text (part): "At stage $d$, take $M_d = B_d(g_d)$ columns, ..."

```latex
At stage $d$, take $M_d = B_d(g_d)$ columns (if $g_d = 0$, which happens when the class of $\mathcal{L}$ is below $d$, the stage is vacuous and $M_d = 1$ suffices; the counts below keep $B_d(0)$ for uniformity), ...
```

### Finding 18 (Style). Lines 52, 181, 671–687. Verification boilerplate.

The `\date` field reads "5 November 2026 (core version; AI-checked, pending human review)", the phrase "AI-checked, pending human review" occurs nine times, and Section 8 (Outlook) runs to about two pages of dense conditional prose with per-sentence status tags. For a journal submission: keep Section 1.6 (Verification Status) as the single place for the disclaimer, remove it from the date, and reduce Section 8 to a half-page list of items with one pointer each to the companion.

```latex
\date{5 November 2026}
```

and, for the opening of Section 8:

```latex
The results described in this section are not claimed in this paper. Each is stated in one or two sentences; proofs, or conditional derivations, are in the full version (Appendix~\ref{app:artifacts}), and all are AI-checked and pending human review. Items marked \emph{argued} have no proof there either.
```

followed by one short item per paragraph.

### Finding 19 (Imprecision). Lines 720–721. Bibliography drift between core and companion.

Current text: `\bibliographystyle{plain}` / `{\raggedright\bibliography{references}}`.

`core/references.bib` has `Olson1969` (line 353), which `../references.bib` lacks; `../references.bib` has twelve entries (Benjamini et al., Cuccaro et al., Micciancio–Peikert, ...) the core copy lacks. Appendix A says `core/numbers.tex` is a copy of the master; the same should hold for the bibliography, or the core should state that its bib is a curated subset. Make `Olson1969` part of the master file and regenerate the core copy, or add to Appendix A:

```latex
\item Bibliography: \file{core/references.bib} is the subset of \file{docs/papers/rees-hsp/references.bib} cited here, plus \file{Olson1969}, which the full version does not cite.
```

### Finding 20 (Style). Line 433. Invisible hedge.

The sentence about van de Woestijne's "Section 6" is hedged only in a LaTeX comment (`% NEEDS HUMAN VERIFICATION ...`), which no reader of the PDF sees. Either resolve the locator or write the hedge in the text:

```latex
% (replace the comment by, in the text after "\cite[Section~6]{vandeWoestijne2005}":)
(the section number refers to the thesis of that title; the ISSAC 2005 extended abstract has six pages)
```

or whichever is correct after checking.

### Finding 21 (Imprecision). Line 486. Register bound omits discarded registers.

Current text: "Depth-first evaluation of the recursion tree stores at most $2 + \sum_{d=2}^c (M_d - 1)$ cover-sized group registers at once, excluding leaf workspace and arithmetic ancillas."

The bound assumes that consumed targets and oracle label registers are measured and reset after each merge; say so.

```latex
Depth-first evaluation of the recursion tree, with every consumed target and every oracle label register measured and reset as soon as it is traced out, stores at most $2 + \sum_{d=2}^c (M_d - 1)$ cover-sized group registers at once, excluding leaf workspace and arithmetic ancillas.
```

### Finding 22 (Imprecision). Line 312. Which primes the row certificates cover.

Current text (part): "the coefficient matrix has rank $52 = 64-12$ modulo every prime $5 \le p \le 23$ (exact computation), and $\DlRowCerts$ integer row certificates show that every derivation maps ... in every characteristic $p > \DlBaseClass$ (exact computation; Appendix~\ref{app:artifacts})."

The sentence mixes a finite check (rank at $5\le p\le23$) with a claim for all $p>3$ carried by certificates; the non-gradability conclusion needs only the latter. Say what a certificate is, in one clause, so the reader can see why it covers every $p>3$:

```latex
the coefficient matrix has rank $52 = 64-12$ modulo every prime $5 \le p \le 23$ (exact computation), and $\DlRowCerts$ integer row certificates, that is, integer combinations of the derivation equations whose coefficients on the unknowns are $2^a3^b$ times a unit vector, show that every derivation maps $\mathcal{L}_{\mathrm{DL}}$ into $[\mathcal{L}_{\mathrm{DL}},\mathcal{L}_{\mathrm{DL}}]$ in every characteristic $p > \DlBaseClass$ (exact computation; Appendix~\ref{app:artifacts})
```

(adjust the description of the certificates to what the artifact actually stores; I did not open it).

---

Tally: 22 findings. Errors: none. Gaps: 2 (Findings 1, 2). Imprecisions: 16 (Findings 3–15, 19, 21, 22). Style: 4 (Findings 16, 17, 18, 20).

---

## 5. Statements stronger in the core than in the companion

1. **Theorem 6.1(i)** (line 483): core says at most $(d-1)d(d+1)/2$ brackets and division only by integers with prime factors $\le d$; companion (`main.tex` 797) says exactly $(d-1)d(d+1)(d+2)/6$ for the implemented recurrence, "optimized schedules may use fewer", and prime factors $\le c$. The core's claims are proved in the core (memoization; $d\le c$), so they are true, but they are not in the companion and the artifact does not exercise the memoized count. See Finding 6.
2. **Lemma 3.5** (line 282): the core drops "Let $s_1,\dots,s_c\in\Fp^\times$ be distinct", which the companion (`main.tex` 458) has. Formally stronger and, read literally, false. See Finding 3.
3. **Theorem 1.3** (line 147): "makes $Q_{\mathrm q}=\dots$ queries" versus the companion's "at most $Q$". True as stated; harmless. See Finding 10.
4. **Section 1.4** (line 162): "So these results are special cases of the regime of Theorem 1.3" versus the companion's "if Theorem 1.3 is correct, these results are special cases of its regime"; and "What may be new is the use of the cover" versus the companion's "Only the use of the cover ... may be new, and this has not been established." The hardening is defensible given that the core proves Theorem 1.3 modulo the import, but Finding 12 applies.
5. **Remark 7.5** (line 656): the core drops the companion's heading qualifier "conditional on Theorem 1.3" and the phrase "if Theorem 1.3 holds". Same justification as item 4; acceptable.
6. **Theorem 6.1(iii) proof** (line 503): the core asserts, of Kitaev's construction, that "the bound is on the isometry $CJ$, not only on output probabilities" and that the controlled phase gates are synthesized "with their relative phases"; the companion's corresponding text (`main.tex` 799) does not make this claim about Kitaev's construction (it makes it, with proof, for its own Lemma `lem:qft-mod`). The core also drops the companion's `NEEDS HUMAN VERIFICATION` flag on the Kitaev locator. See Finding 7.
7. **Table 1 caption** (line 639): the core's caption states the "(v)" thresholds without the companion's rounding note; as a result the core's column is not derivable from the core's own formula. Not a stronger claim, but an unsupported one in the core. See Finding 5.

Checked and found equal or weaker in the core: Definition 1.2 (core adds "labels of $w$ bits"), Theorem 3.1 (core (iii) says "class at most $c$", companion says "the class of $\mathcal{L}$"), Lemma 3.2, Proposition 3.4, Lemmas 4.1–4.2, Proposition 4.3, Remark 4.4, the recursion, Theorem 5.1, Remark 5.2 (core adds the Las Vegas remark (d) in a weaker form), Lemma 5.4 (core proves the gcd step directly; companion cites its appendix and Lean), Lemma 6.2 (core drops the diamond-norm sentence), Corollary 6.3, the proof of Theorem 1.3 (core's $N_{\mathrm{QFT}}$ count is more explicit than the companion's $N_{\mathrm{instr}}q_{\max}$ and gives the same $\varepsilon/3$), Lemma 7.3, Proposition 7.4 (identical up to the letter for $\rho$/$\tau$ and $\ell$/$u$), and the Lean paragraph of Appendix A.

---

## 6. Recommendation

**Major revision.**

The mathematics the core proves is correct as far as I can check, and the central idea (homogenize the hidden subgroup by interpolating the oracle across $c$ evaluations of the Rees cover, then run the Ivanyos–Santha descent on the cover) is clean and, if it is new, a genuine contribution to a problem that has been open in this form since Imran–Ivanyos posed it. The paper is also unusually honest about its limits. But three things stand between it and acceptance, and only one of them is cosmetic:

1. **Verify the import (Finding 2).** The explicit bound in the main theorem depends on an AI-only reading of Ivanyos–Santha 2015 that asserts the published Theorem 3 misstates what its proof gives. A human must confirm this against arXiv:1503.09016v2, preferably by writing to the authors. Until then, state Theorem 1.3 with an abstract arity function $A_d$ and put the Ivanyos–Santha instantiation and the number 145 in a corollary, so that the theorem the paper proves is cleanly separated from the theorem it imports. This is the single change most likely to decide acceptance.

2. **Fix the access-model slip and tighten the hybrid application (Findings 1 and 8).** Drop the controlled-oracle guard in favour of "any unitary extension of $U_f$", and state how the classical solver treats non-canonical label strings. Both are one-sentence fixes, but as written the compilation section contradicts the input definition.

3. **Make the core a faithful subset of the companion and cut the boilerplate (Findings 3, 5, 6, 7, 18, 19).** Restore the dropped hypothesis in Lemma 3.5, the rounding note in Table 1 and the verification flag (or the explicit-construction route) for the Fourier transform; reconcile the bracket count and the two bibliography files; reduce Section 8 to half a page; take the status tag out of the date line. A reader who has only the core should never be able to derive a number or a hypothesis different from the companion's.

If the import is confirmed by a human and the above are done, I would expect to recommend acceptance with minor changes. The classical-query section (Section 7.2) is correct and complete as it stands and needs nothing beyond Finding 5.

Independent of acceptance, two further checks would strengthen the paper: (i) open the 32 row certificates for the Dixmier–Lister derivations and state in one clause what they certify, since they are what carries "every $p>3$" (Finding 22); (ii) run the memoized BCH schedule of Theorem 6.1(i) in the artifact so that the stated bracket count is exercised somewhere (Finding 6).
