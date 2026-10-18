# Planted $q$-ary Punctured-Coordinate Projection Bridge: Bipartite Schmidt Entanglement Spectrum, Puncturing–Shortening QFT Duality, and $d_{\min}(B)$ Rank-Locking

## 1. Motivation and Scope

A natural dimensional-reduction strategy for planted $q$-ary subspace problems is **coordinate puncturing**: restricting quantum measurements or classical linear probes to a subset $J \subset \{1, \dots, n\}$ of $m = |J|$ kept coordinates while tracing out or ignoring the complementary $t = n - m$ coordinates $\bar{J} = \{1, \dots, n\} \setminus J$.

For a dimension-$d$ planted subspace $B = \operatorname{rowspan}(M) \subset \mathbb{F}_q^n$, define:
- the **punctured codes** $B_J := \pi_J(B) \subseteq \mathbb{F}_q^m$ of dimension $d_J := \operatorname{rank}(M_{:, J})$ and $B_{\bar{J}} := \pi_{\bar{J}}(B) \subseteq \mathbb{F}_q^t$ of dimension $d_{\bar{J}} := \operatorname{rank}(M_{:, \bar{J}})$;
- the **shortened subcodes** $B_{\ker(J)} := \{b \in B : \pi_J(b) = 0\}$ ($\dim = k_{\bar{J}} := d - d_J$) and $B_{\ker(\bar{J})} := \{b \in B : \pi_{\bar{J}}(b) = 0\}$ ($\dim = k_J := d - d_{\bar{J}}$).

This note proves three exact theorems governing the reduced quantum state $\rho_{B, J} = \operatorname{Tr}_{\bar{J}}(|\psi_B\rangle\langle\psi_B|)$, punctured $\mathrm{QFT}_q^{\otimes m}$ dual sampling, and $d_{\min}(B)$ rank-locking of $J$-supported linear probes.

## 2. Theorem 1 — Exact Bipartite Schmidt Spectrum and Purity Across $(J, \bar{J})$

Define the symmetric **bipartite entanglement rank exponent** across $(J, \bar{J})$:
$$
e_{J, \bar{J}}(B) \;:=\; d_J + d_{\bar{J}} - d \;=\; d_J - k_J \;=\; d_{\bar{J}} - k_{\bar{J}} \;\ge\; 0.
$$

**Theorem 1 (Bipartite Schmidt Spectrum and Purity Law).**
Quotienting $B$ by the direct sum of the local shortened subcodes $B_{\ker(\bar{J})} \oplus B_{\ker(J)}$ (of dimension $k_J + k_{\bar{J}} = 2d - d_J - d_{\bar{J}}$) yields $q^{e_{J, \bar{J}}(B)}$ mutually orthogonal Schmidt coset states on $\mathbb{F}_q^J \times \mathbb{F}_q^{\bar{J}}$. Consequently, both reduced density operators $\rho_{B, J} := \operatorname{Tr}_{\bar{J}}(|\psi_B\rangle\langle\psi_B|)$ and $\rho_{B, \bar{J}} := \operatorname{Tr}_J(|\psi_B\rangle\langle\psi_B|)$ have $q^{e_{J, \bar{J}}(B)}$ equal non-zero eigenvalues $q^{-e_{J, \bar{J}}(B)}$, with
$$
\operatorname{rank}(\rho_{B, J}) \;=\; q^{d_J + d_{\bar{J}} - d}, \qquad
\operatorname{Tr}\bigl(\rho_{B, J}^2\bigr) \;=\; q^{-(d_J + d_{\bar{J}} - d)}, \qquad
S(\rho_{B, J}) \;=\; (d_J + d_{\bar{J}} - d)\log_2 q\text{ bits}.
$$

## 3. Theorem 2 — Puncturing–Shortening Duality Under Local $\mathrm{QFT}_q^{\otimes m}$ Readout

Let $\iota_J : \mathbb{F}_q^m \to \mathbb{F}_q^n$ denote zero-padding outside $J$.

**Theorem 2 (Punctured QFT Support vs Shortened Dual Code).**
1. **Local $\mathrm{QFT}_q^{\otimes m}$ Support**: Applying $\mathrm{QFT}_q^{\otimes m}$ to the kept register $J$ of $|\psi_B\rangle$ and measuring in the computational basis produces the uniform distribution over the **punctured dual** $\pi_J(B^\perp) = \bigl(\pi_J(B_{\ker(\bar{J})})\bigr)^\perp \subseteq \mathbb{F}_q^m$ of cardinality $q^{m - k_J} = q^{m - d + d_{\bar{J}}}$.
2. **Shortened Dual Identity for $J$-Supported Checks**: The dual of the punctured code $B_J = \pi_J(B) \subseteq \mathbb{F}_q^m$ consists precisely of the shortened dual vectors supported on $J$:
   $$
   (B_J)^\perp \;=\; \bigl\{\, u_J \in \mathbb{F}_q^m : \iota_J(u_J) \in B^\perp \,\bigr\} \;\subseteq\; \pi_J(B^\perp), \qquad \bigl|(B_J)^\perp\bigr| \;=\; q^{m - d_J}.
   $$

## 4. Theorem 3 — $J$-Supported Classical Probe Dichotomy and $d_{\min}(B)$ Rank-Locking

**Theorem 3 (Exact $J$-Supported Probe Distribution and Minimum-Distance Rank-Locking).**
1. Under a uniform $J$-supported probe $u = \iota_J(u_J)$ ($u_J \sim \operatorname{Unif}(\mathbb{F}_q^m)$) and window $W \subset \mathbb{F}_q$ of size $R = |W|$, $N_W(\iota_J(u_J); B)$ equals $q^d\,\mathbf{1}_{0 \in W}$ for $u_J \in (B_J)^\perp$ (probability $q^{-d_J}$) and equals $q^{d-1}R$ for $u_J \notin (B_J)^\perp$ (probability $1 - q^{-d_J}$), with variance
   $$
   \operatorname{Var}_{u_J \sim \mathbb{F}_q^m}\!\bigl[N_W(\iota_J(u_J); B)\bigr] \;=\; q^{2(d - d_J)}\bigl(q^{d_J} - 1\bigr)\!\left(\mathbf{1}_{0 \in W} - \frac{R}{q}\right)^2.
   $$
2. **Minimum-Distance Rank-Locking ($t < d_{\min}(B)$)**: Let $d_{\min}(B) := \min_{b \in B \setminus \{0\}} \mathrm{wt}_H(b)$. Whenever the number of punctured coordinates satisfies $t = n - |J| < d_{\min}(B)$, no non-zero codeword $b \in B \setminus \{0\}$ can be supported entirely inside $\bar{J}$, so $B_{\ker(J)} = \{0\}$ and $d_J = d$ for **every** coordinate subset $J$ of size $|J| > n - d_{\min}(B)$. Thus puncturing fewer than $d_{\min}(B)$ coordinates cannot increase the dual-hit probability above $q^{-d}$.
