# The Symplectic Parabolic Hidden Subgroup Problem: Algebraic Structure, Classical Transvection Upper Bound, and Oracle Gaps

2026-10-23: the retraction of the OLD whole-Lie field-oracle construction
below remains in force. SYMPLECTIC_FIELD_CHART_REDUCTION.md now proposes a
DIFFERENT field-only graph-chart/HPGP route with a final rejection
certificate and a scoped Omega(sqrt(q)) opaque-label classical query bound.
SYMPLECTIC_PRIME_SQUARE_REDUCTION.md treats a separate ring input. Neither
revives the old oracle map or its false lower bound; no free field-to-ring
extension is allowed. See PARABOLIC_CUT_LIST_CORRECTION.md before applying
downstream blanket dequantization or gate-lower-bound claims.

**Investigation**: Investigation 26 (Symplectic Groups & Geometric Non-Abelian HSP)  
**Date**: 2026-10-11  
**Status**: AUDITED & RETRACTED (Speedup claim and lower bound retracted; algebraic structure preserved)  
**Core Invariants**: `speedup_claim_allowed = False`, `accepted_speedup_candidate = False`  

---

## 1. Executive Summary & Audit Retraction Notice

> [!CAUTION]
> **Adversarial Audit Retraction Notice (2026-10-11)**:
> 1. **False Classical Query Lower Bound (DISPROVED)**:
>    The claimed classical lower bound of $\Omega(q^{n(n+1)/4})$ queries is **FALSE**.
>    There exists an explicit classical counteralgorithm running in **$O(n q^n)$ expected queries**:
>    For any non-zero vector $v \in \mathbb{F}_q^{2n}$, the symplectic transvection $T_v(x) = x + \Omega(x, v) v$ is in $Sp(2n, \mathbb{F}_q)$ in every characteristic.
>    Testing $f(I) = f(T_v)$ holds if and only if $v \in W$.
>    Since $v \in W$ with probability $\frac{q^n - 1}{q^{2n} - 1} = \frac{1}{q^n + 1}$, testing random vectors finds $n$ linearly independent vectors in $W$ in $O(n q^n)$ expected queries.
>    For each fixed $n \ge 4$, $n q^n \ll q^{n(n+1)/4}$ as $q$ grows. At $n=3$ the exponents are equal, so this comparison alone is not a refutation there.
> 2. **Missing Quantum Multiplicative-to-Additive Oracle Reduction (UNESTABLISHED)**:
>    The standard HSP oracle $f$ provides evaluations on the multiplicative group $Sp(2n, \mathbb{F}_q)$.
>    The proposed Fourier sampler assumed an oracle on the additive group $(\mathfrak{sp}(2n, \mathbb{F}_q), +)$ whose fibers are additive cosets of $\mathfrak{p}_W$.
>    Replacing $X$ by $I + X$ fails globally on the ambient Lie algebra (matrices can be singular or non-symplectic). No reduction from the multiplicative oracle to the additive Lie algebra has been established.
> 3. **Characteristic-Two Trace-Form Failure (DISPROVED IN CHAR 2)**:
>    For $n \ge 2$ in characteristic 2, the trace pairing $\text{tr}(S C)$ vanishes on off-diagonal elements because coordinates enter multiplied by 2.
>    For example, $C = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ satisfies $\text{tr}(S C) \equiv 0$ for every symmetric matrix $S \in \text{Sym}_n(\mathbb{F}_2)$.
>    Thus, the lower-block matrix is orthogonal to $\mathfrak{u}_W$ but does *not* stabilize $W$, disproving $\mathfrak{u}_W^\perp = \mathfrak{p}_W$ in characteristic 2.
>
> **Status**: The claimed quantum speedup and classical lower bound are **RETRACTED**. Theorem 1 (Levi decomposition and abelian unipotent radical) is preserved as a verified algebraic lemma.

---

## 2. Verified Algebraic Lemma: Structure of the Siegel Parabolic

### Lemma 1: Levi Decomposition and Unipotent Radical Linearity
Let $V = \mathbb{F}_q^{2n}$ equipped with the standard non-degenerate alternating bilinear form $\Omega = \begin{pmatrix} 0 & I_n \\ -I_n & 0 \end{pmatrix}$.
Let $W \le V$ be a Lagrangian (maximal isotropic) subspace ($\dim(W) = n, \Omega|_W \equiv 0$).
The stabilizer $P_W = \text{Stab}(W)$ in $Sp(2n, \mathbb{F}_q)$ admits a semidirect product decomposition:
$$P_W = L_W \ltimes U_W,$$
where:
1. The Levi factor is $L_W \cong GL(n, \mathbb{F}_q)$.
2. The unipotent radical is:
   $$U_W = \{ u \in Sp(2n, \mathbb{F}_q) : (u - I) V \subseteq W \text{ and } (u - I) W = \{0\} \}.$$
3. Every element $u \in U_W$ satisfies $(u - I)^2 = 0$.
4. The map $X \mapsto I + X$ is an exact group isomorphism from the additive vector space of the Lie algebra:
   $$\mathfrak{u}_W = \{ X \in \mathfrak{sp}(2n, \mathbb{F}_q) : X V \subseteq W, X W = \{0\} \} \cong (\text{Sym}_n(\mathbb{F}_q), +),$$
   to the unipotent radical $U_W$.
5. The unipotent radical $U_W$ is an **elementary abelian group** of order $q^{\frac{n(n+1)}{2}}$.

*Proof*:  
In an adapted symplectic basis where $W = \text{span}(e_1, \dots, e_n)$, any element $M \in P_W$ has block form $\begin{pmatrix} A & B \\ 0 & D \end{pmatrix}$.
The symplectic condition $M^T \Omega M = \Omega$ yields $D = A^{-T}$ and $(A^{-1} B)^T = A^{-1} B$.
Setting $S = A^{-1} B \in \text{Sym}_n(\mathbb{F}_q)$, every element factors uniquely as:
$$M = \begin{pmatrix} A & 0 \\ 0 & A^{-T} \end{pmatrix} \begin{pmatrix} I & S \\ 0 & I \end{pmatrix}.$$
Because $\begin{pmatrix} I & S_1 \\ 0 & I \end{pmatrix} \begin{pmatrix} I & S_2 \\ 0 & I \end{pmatrix} = \begin{pmatrix} I & S_1 + S_2 \\ 0 & I \end{pmatrix}$, $U_W$ is abelian of order $q^{n(n+1)/2}$. $\blacksquare$

---

## 3. Disproof of the Claimed Classical Lower Bound: The $O(n q^n)$ Symplectic Transvection Algorithm

**Theorem (Classical Transvection Subspace Reconstruction)**:  
Let $H = P_W = \text{Stab}(W)$ be the hidden Siegel parabolic subgroup accessed via a standard oracle $f: Sp(2n, \mathbb{F}_q) \to S$.  
There exists an explicit randomized classical algorithm that recovers an exact basis for $W$ using an expected **$O(n q^n)$ oracle queries**.

**Proof**:  
1. For any non-zero vector $v \in \mathbb{F}_q^{2n}$, define the symplectic transvection:
   $$T_v(x) = x + \Omega(x, v) v.$$
2. *Symplectic Invariance*: For all $x, y \in V$:
   $$\Omega(T_v(x), T_v(y)) = \Omega(x + \Omega(x, v)v, y + \Omega(y, v)v)$$
   $$= \Omega(x, y) + \Omega(y, v)\Omega(x, v) + \Omega(x, v)\Omega(v, y) + 0$$
   $$= \Omega(x, y) + \Omega(x, v)\Omega(y, v) - \Omega(x, v)\Omega(y, v) = \Omega(x, y).$$
   Thus $T_v \in Sp(2n, \mathbb{F}_q)$ for **every characteristic** (including characteristic 2).
3. *Stabilizer Criterion*: We have $T_v \in P_W \iff T_v(W) = W$.
   - If $v \in W$: Since $W$ is isotropic, $\Omega(w, v) = 0$ for all $w \in W$. Thus $T_v(w) = w$ for all $w \in W$, so $T_v$ fixes $W$ pointwise and $T_v \in P_W$.
   - If $v \notin W$: Since $W$ is maximal isotropic ($\dim W = n$), $W^\perp = W$. Because $v \notin W$, $v \notin W^\perp$, so there exists at least one $w \in W$ such that $\Omega(w, v) = \alpha \ne 0$.
     Then $T_v(w) = w + \alpha v$. If $w + \alpha v \in W$, then $\alpha v \in W \implies v \in W$, contradiction.
     Thus $T_v(w) \notin W$, so $T_v \notin P_W$.
4. Therefore, testing $f(T_v) = f(I)$ is an **exact membership test**:
   $$f(T_v) = f(I) \iff v \in W.$$
5. *Sampling Efficiency*: Drawing a uniformly random non-zero vector $v \in \mathbb{F}_q^{2n}$, the probability of acceptance is:
   $$P_{\text{accept}} = \frac{q^n - 1}{q^{2n} - 1} = \frac{1}{q^n + 1}.$$
6. Testing $v$ takes 2 queries ($f(I)$ and $f(T_v)$). The expected number of trials to find a vector in $W$ is $q^n + 1$.
7. Conditioned on having found $k < n$ linearly independent vectors in $W$, a random vector in $W$ is independent of the previous $k$ vectors with probability $1 - q^{k-n} \ge 1/2$.
8. By coupon collector / linear independence arguments, finding $n$ linearly independent vectors in $W$ takes an expected:
   $$Q \le 2 n (q^n + 1) = O(n q^n) \text{ queries}.$$
9. Comparing $O(n q^n)$ with the claimed lower bound $\Omega(q^{n(n+1)/4})$:
   - For $n = 4$: $O(n q^4) \ll q^5$.
   - For $n = 10$: $O(n q^{10}) \ll q^{27.5}$.
   The birthday-paradox lower bound on the full orbit space $|\Lambda|$ is **completely invalid** because the algorithm queries adaptive, structured transvection elements $T_v$ whose collision probability with $P_W$ is $q^{-n}$, not $q^{-n(n+1)/2}$. $\blacksquare$

---

## 4. Unresolved Proof Obligations for Quantum Symplectic HSP

To establish a valid quantum speedup for the Siegel Parabolic HSP, the following two open mathematical obstacles must be resolved:
1. **Multiplicative-to-Additive Oracle Reduction**: Construct an explicit, lawful quantum reduction from the multiplicative oracle $f: Sp(2n, \mathbb{F}_q) \to S$ to an additive Fourier sampling routine on $\mathfrak{u}_W$ without assuming an unphysical Lie algebra oracle.
2. **Characteristic-2 Trace Duality Repair**: Formulate a characteristic-independent non-degenerate pairing for the symplectic Lie algebra that correctly identifies $\mathfrak{u}_W^\perp = \mathfrak{p}_W$ in characteristic 2, or restrict the theorem with explicit odd-characteristic hypotheses.

Pending resolution of these obligations, **no quantum speedup claim is allowed**.
