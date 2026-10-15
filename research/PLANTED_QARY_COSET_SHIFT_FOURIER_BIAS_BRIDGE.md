# Planted $q$-ary Coset-Shift Fourier-Bias Bridge: QFT Phase Erasure, Off-Dual Shift Invariance, and Exact First-Moment Equalization on Affine Cosets $B + a$

## 1. Motivation and Scope

In homogeneous planted $q$-ary code problems, the secret structure is a linear subspace $B = \operatorname{rowspan}(M) \subset \mathbb{F}_q^n$ of dimension $d$ ($|B| = q^d$) containing $0 \in B$. In inhomogeneous (affine/syndromic) variants, the planted support is an **affine coset**
$$
B + a \;:=\; \{\, b + a : b \in B \,\} \;\subset\; \mathbb{F}_q^n, \qquad a \in \mathbb{F}_q^n.
$$
This note proves three exact theorems comparing quantum $\mathrm{QFT}_q^{\otimes n}$ readout and classical linear-probe window acceptance on affine cosets $B + a$ versus linear subspaces $B$.

## 2. Theorem 1 — Exact QFT$_q^{\otimes n}$ Dual-Subspace Support Conservation and Shift-Phase Erasure

For any dimension-$d$ subspace $B \subset \mathbb{F}_q^n$ and shift $a \in \mathbb{F}_q^n$, define the uniform affine coset superposition
$$
|\psi_{B+a}\rangle \;:=\; q^{-d/2} \sum_{b \in B} |b + a\rangle \;\in\; (\mathbb{C}^q)^{\otimes n}.
$$

**Theorem 1 (Exact QFT Dual Support Conservation and Shift Erasure).**
1. Applying $\mathrm{QFT}_q^{\otimes n}$ (where $\langle u | \mathrm{QFT}_q^{\otimes n} | x \rangle = q^{-n/2}\omega_q^{\langle u, x\rangle}$) to $|\psi_{B+a}\rangle$ yields
   $$
   \mathrm{QFT}_q^{\otimes n}|\psi_{B+a}\rangle \;=\; q^{-(n-d)/2} \sum_{u \in B^\perp} \omega_q^{\langle a, u\rangle} |u\rangle,
   $$
   where $B^\perp = \{u \in \mathbb{F}_q^n : M u = 0\}$ is the $(n-d)$-dimensional dual subspace ($|B^\perp| = q^{n-d}$).
2. Measuring $\mathrm{QFT}_q^{\otimes n}|\psi_{B+a}\rangle$ in the computational basis produces the outcome distribution
   $$
   P_{\text{QFT}}(u \mid B + a) \;=\; \bigl|\langle u | \mathrm{QFT}_q^{\otimes n} | \psi_{B+a}\rangle\bigr|^2 \;=\;
   \begin{cases}
   q^{-(n-d)}, & u \in B^\perp, \\
   0, & u \notin B^\perp,
   \end{cases}
   $$
   which is **identically independent of the shift $a \in \mathbb{F}_q^n$** (total variation distance $0$ across all $a \in \mathbb{F}_q^n$).

## 3. Theorem 2 — Deterministic Shift Invariance Outside $B^\perp$ and Dual-Subspace Collapse

For any linear probe $u \in \mathbb{F}_q^n$ and acceptance window $W \subset \mathbb{F}_q$ of size $R = |W|$, let
$$
N_W(u; B + a) \;:=\; \bigl|\bigl\{\, x \in B + a : \langle x, u\rangle \in W \,\bigr\}\bigr|.
$$

**Theorem 2 (Pointwise Off-Dual Shift Invariance and Dual Collapse).**
1. **Off-Dual Shift Invariance ($u \notin B^\perp$)**: Whenever $u \notin B^\perp$, the linear form $b \mapsto \langle b, u\rangle$ maps $B$ surjectively ($q^{d-1}$-to-$1$) onto $\mathbb{F}_q$. Because translation by $\langle a, u\rangle \in \mathbb{F}_q$ is a bijection on $\mathbb{F}_q$, the affine map $b \mapsto \langle b + a, u\rangle$ is also $q^{d-1}$-to-$1$ onto $\mathbb{F}_q$, so for **every** $a \in \mathbb{F}_q^n$:
   $$
   N_W(u; B + a) \;=\; q^{d-1} R \;=\; N_W(u; B) \qquad \forall u \in \mathbb{F}_q^n \setminus B^\perp.
   $$
2. **Dual-Subspace Collapse ($u \in B^\perp$)**: Whenever $u \in B^\perp$, $\langle b + a, u\rangle = \langle a, u\rangle$ is constant across all $b \in B$, so
   $$
   N_W(u; B + a) \;=\; q^d \cdot \mathbf{1}_{\langle a, u\rangle \in W} \qquad \forall u \in B^\perp.
   $$

## 4. Theorem 3 — Exact First-Moment Equalization on Non-Trivial Cosets $a \notin B$

**Theorem 3 (Exact First-Moment Dichotomy Between $a \in B$ and $a \notin B$).**
Averaging $N_W(u; B + a)$ over a uniform probe $u \sim \operatorname{Unif}(\mathbb{F}_q^n)$:
1. **Trivial Coset ($a \in B$, so $B + a = B$)**: Every $u \in B^\perp$ satisfies $\langle a, u\rangle = 0$, giving
   $$
   \mathbb{E}_{u \sim \mathbb{F}_q^n}\bigl[N_W(u; B)\bigr] \;=\; \mathbf{1}_{0 \in W} \;+\; (q^d - 1)\frac{R}{q}.
   $$
2. **Non-Trivial Coset ($a \in \mathbb{F}_q^n \setminus B$)**: Because $a \notin B = (B^\perp)^\perp$, the linear functional $u \mapsto \langle a, u\rangle$ restricted to $B^\perp$ is non-zero and hence surjective ($q^{n-d-1}$-to-$1$) onto $\mathbb{F}_q$. Thus $\Pr_{u \sim B^\perp}[\langle a, u\rangle \in W] = R / q$ regardless of whether $0 \in W$, and the global first moment over $u \sim \mathbb{F}_q^n$ equals the exact unstructured mean for **every** window $W$ of size $R$:
   $$
   \mathbb{E}_{u \sim \mathbb{F}_q^n}\bigl[N_W(u; B + a)\bigr]
   \;=\; \left(1 - q^{-d}\right) q^{d-1} R \;+\; q^{-d} \cdot q^d \frac{R}{q}
   \;=\; q^{d-1} R \qquad \forall a \in \mathbb{F}_q^n \setminus B.
   $$
