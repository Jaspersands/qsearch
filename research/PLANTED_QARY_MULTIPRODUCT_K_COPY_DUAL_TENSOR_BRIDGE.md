# Planted $q$-ary Multiproduct $K$-Copy Dual-Tensor Bridge: Primal-Difference Shift Cancellation, Constant-Sum Dual Fiber Spectral Decomposition, and $K$-Invariant Coset Purity

## 1. Motivation and Scope

In `theorems/planted_qary_coset_shift_fourier_bias_bridge.py` (Subsystem 21), we showed that a single copy of an affine coset state $|\psi_{B+a}\rangle = q^{-d/2}\sum_{b \in B}|b + a\rangle$ ($\dim(B) = d$) measured in the computational basis after $\mathrm{QFT}_q^{\otimes n}$ erases the coset shift $a \in \mathbb{F}_q^n$ completely.

When $K \ge 2$ copies $|\psi_{B+a}\rangle^{\otimes K}$ are available, how do coherent multi-copy operations—such as primal modular subtraction $U_{\text{sub}}|x_1, x_2\rangle = |x_1, (x_2 - x_1) \bmod q\rangle$ and $K$-copy Fourier transform $\mathrm{QFT}_q^{\otimes n K}$—transform the shift $a$ and decompose the shift-averaged $K$-copy state $\bar{\rho}_B^{(K)} := \mathbb{E}_{a \sim \mathbb{F}_q^n}[(|\psi_{B+a}\rangle\langle\psi_{B+a}|)^{\otimes K}]$? This note proves three exact theorems resolving the $K$-copy dual-tensor structure of planted affine coset states.

## 2. Theorem 1 — Exact Two-Copy Primal-Difference Shift Cancellation

Let $U_{\text{sub}} \in U(q^{2n})$ denote the coordinatewise modular subtraction unitary $U_{\text{sub}}|x_1, x_2\rangle := |x_1,\, (x_2 - x_1) \bmod q\rangle$ on $\mathbb{F}_q^n \times \mathbb{F}_q^n$.

**Theorem 1 (Exact Two-Copy Disentanglement and Shift Cancellation into $|\psi_B\rangle$).**
For every dimension-$d$ subspace $B \subset \mathbb{F}_q^n$ and every shift $a \in \mathbb{F}_q^n$, applying $U_{\text{sub}}$ to two identical affine coset copies $|\psi_{B+a}\rangle \otimes |\psi_{B+a}\rangle$ disentangles the second register into the homogeneous subspace state $|\psi_B\rangle$ with zero shift:
$$
U_{\text{sub}}\bigl(|\psi_{B+a}\rangle \otimes |\psi_{B+a}\rangle\bigr) \;=\; |\psi_{B+a}\rangle \otimes |\psi_B\rangle,
$$
and in the dual Fourier basis,
$$
(\mathrm{QFT}_q^{\otimes n} \otimes \mathrm{QFT}_q^{\otimes n})\,U_{\text{sub}}\bigl(|\psi_{B+a}\rangle \otimes |\psi_{B+a}\rangle\bigr)
\;=\; \left(q^{-(n-d)/2}\sum_{u_1 \in B^\perp}\omega_q^{\langle a, u_1\rangle}|u_1\rangle\right) \otimes \left(q^{-(n-d)/2}\sum_{u_2 \in B^\perp}|u_2\rangle\right).
$$

*Proof.*
Expanding $U_{\text{sub}}(|\psi_{B+a}\rangle \otimes |\psi_{B+a}\rangle) = q^{-d}\sum_{b_1 \in B}\sum_{b_2 \in B} |b_1 + a,\, (b_2 - b_1) \bmod q\rangle$ and substituting $b' := (b_2 - b_1) \bmod q \in B$ (which ranges bijectively over $B$ for each fixed $b_1 \in B$) factors the sum into $(q^{-d/2}\sum_{b_1 \in B}|b_1 + a\rangle) \otimes (q^{-d/2}\sum_{b' \in B}|b'\rangle) = |\psi_{B+a}\rangle \otimes |\psi_B\rangle$. $\square$

## 3. Theorem 2 — Exact Constant-Sum Dual Fiber Spectral Decomposition of $\bar{\rho}_B^{(K)}$

For each $s_\perp \in B^\perp$, define the $K$-copy constant-sum dual fiber
$$
\mathcal{F}_K(s_\perp; B^\perp) \;:=\; \bigl\{\, (u_1, \dots, u_K) \in (B^\perp)^K : u_1 + \dots + u_K \equiv s_\perp \pmod q \,\bigr\},
$$
which has exact cardinality $|\mathcal{F}_K(s_\perp; B^\perp)| = q^{(K-1)(n-d)}$, and define the normalized fiber state
$$
|\Phi_{B^\perp}^{(K)}(s_\perp)\rangle \;:=\; q^{-(K-1)(n-d)/2} \sum_{(u_1, \dots, u_K) \in \mathcal{F}_K(s_\perp; B^\perp)} |u_1, \dots, u_K\rangle.
$$

**Theorem 2 (Orthonormal Constant-Sum Dual Fiber Decomposition).**
Averaging the $K$-copy Fourier state $\mathrm{QFT}_q^{\otimes n K}|\psi_{B+a}\rangle^{\otimes K}$ over a uniform shift $a \sim \operatorname{Unif}(\mathbb{F}_q^n)$ pinches pairs $(u_1, \dots, u_K)$ and $(u'_1, \dots, u'_K)$ in $(B^\perp)^K$ onto the equality of their dual sums $u_1 + \dots + u_K \equiv u'_1 + \dots + u'_K \pmod q$, yielding the exact spectral decomposition into $q^{n-d}$ orthonormal fiber projectors:
$$
\mathrm{QFT}_q^{\otimes n K}\,\bar{\rho}_B^{(K)}\,(\mathrm{QFT}_q^{\otimes n K})^\dagger
\;=\; \frac{1}{q^{n-d}} \sum_{s_\perp \in B^\perp} |\Phi_{B^\perp}^{(K)}(s_\perp)\rangle\langle\Phi_{B^\perp}^{(K)}(s_\perp)|.
$$

## 4. Theorem 3 — Exact $K$-Invariance of Coset-Ensemble Rank, Spectrum, and Purity

**Theorem 3 ($K$-Invariant Rank $q^{n-d}$ and Purity $q^{-(n-d)}$).**
Because the $q^{n-d}$ distinct affine cosets $B + a \in \mathbb{F}_q^n / B$ have pairwise disjoint supports in $\mathbb{F}_q^n$, the states $\{|\psi_{B+a}\rangle\}_{B+a \in \mathbb{F}_q^n / B}$ are mutually orthogonal ($\langle \psi_{B+a} \mid \psi_{B+a'}\rangle = \mathbf{1}_{a - a' \in B}$), and therefore $\{|\psi_{B+a}\rangle^{\otimes K}\}_{B+a \in \mathbb{F}_q^n / B}$ remain $q^{n-d}$ mutually orthogonal pure states for every $K \ge 1$. Consequently, for every copy count $K \ge 1$:
$$
\operatorname{rank}\!\left(\bar{\rho}_B^{(K)}\right) \;=\; q^{n-d}, \qquad
\operatorname{Tr}\!\left(\bigl(\bar{\rho}_B^{(K)}\bigr)^2\right) \;=\; q^{-(n-d)}, \qquad
S\bigl(\bar{\rho}_B^{(K)}\bigr) \;=\; (n - d)\log_2 q\text{ bits}.
$$
