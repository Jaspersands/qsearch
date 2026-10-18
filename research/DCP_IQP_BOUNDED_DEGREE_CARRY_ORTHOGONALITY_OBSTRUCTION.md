# Clean and Noisy DCP IQP / Polynomial-Phase Readout: Directional-Derivative Structure, Carry-Polynomial Degree $2^{t-1}$, and Sparse-Row Advantage Bounds

## 1. Motivation and Scope

In `theorems/dcp_native_parity_observables.py` (`research/DCP_NATIVE_PARITY_OBSERVABLES.md`), we showed that a polynomial-size circuit $H^{\otimes K}(I - 2|1^K\rangle\langle 1^K|)H^{\otimes K}$ can induce a dense observable in the computational basis, leaving open whether **Instantaneous Quantum Polynomial-time (IQP) / diagonal polynomial-phase circuits** $D_P = \operatorname{diag}((-1)^{P(x)})$ ($\deg_{\mathbb{F}_2}(P) \le d$) combined with Pauli-$X$ bit-flip observables $X(u) = \bigotimes_{r=0}^{K-1} X^{u_r}$ ($u \in \{0, 1\}^K \setminus \{0\}$) can predict the clean DCP parity bit $S_1 \bmod 2$ in polynomial time.

This note proves three exact theorems characterizing the conjugated IQP observables
$$
O_{P, u} \;:=\; D_P\,X(u)\,D_P^\dagger \qquad \bigl(D_P = \operatorname{diag}((-1)^{P(x)}),\; u \in \{0, 1\}^K \setminus \{0\}\bigr)
$$
and establishing why polynomial-term IQP readouts fail on both clean ($v = 1$) and noisy ($v < 1$) DCP sources.

## 2. Theorem 1 — Exact IQP Directional-Derivative Matrix Law and Row-Degree 1

For any Boolean polynomial $P : \mathbb{F}_2^K \to \mathbb{F}_2$ of algebraic degree $\deg_{\mathbb{F}_2}(P) \le d$ and any non-zero flip mask $u \in \{0, 1\}^K \setminus \{0\}$, define the directional derivative $\Delta_u P : \mathbb{F}_2^K \to \mathbb{F}_2$ by
$$
\Delta_u P(x) \;:=\; P(x) \oplus P(x \oplus u).
$$

**Theorem 1 (Exact Conjugated IQP Observable Entry Identity and Row Sparsity).**
1. The Hermitian unitary observable $O_{P, u} = D_P X(u) D_P^\dagger$ ($O_{P, u}^2 = I_{2^K}$, $\|O_{P, u}\|_{\text{op}} = 1$) has exact computational-basis matrix entries
   $$
   O_{P, u}[x, y] \;=\; (-1)^{\Delta_u P(x)}\,\mathbf{1}\bigl[y = x \oplus u\bigr],
   $$
   where $\deg_{\mathbb{F}_2}(\Delta_u P) \le \max(0, d - 1)$, and every row $x \in \{0, 1\}^K$ of $O_{P, u}$ has **exactly $1$ non-zero entry** (at column $y = x \oplus u$).
2. On the $K$-copy parity density difference $\Delta\rho(A) = \rho_{\text{even}}(A) - \rho_{\text{odd}}(A)$ (`theorems/dcp_native_parity_bridge.py`) with target $h = (2^{t-1}, 0, \dots, 0)^T \in \mathbb{Z}_{2^t}^n$ and visibility $v \in [0, 1]$, the exact parity prediction advantage of $O_{P, u}$ is
   $$
   \mathrm{Adv}(O_{P, u}; A) \;=\; \frac{1}{4}\operatorname{Tr}\bigl(O_{P, u}\,\Delta\rho(A)\bigr)
   \;=\; \frac{v^{\mathrm{wt}_H(u)}}{2^{K+1}} \sum_{x \in \{0, 1\}^K} (-1)^{\Delta_u P(x)}\,\mathbf{1}\!\left[\sum_{r \in \mathrm{supp}(u)} (1 - 2 x_r) A_{\cdot, r} \equiv h \pmod{2^t}\right].
   $$

## 3. Theorem 2 — Lucas Carry-Degree $2^{t-1}$ Orthogonality on Symmetric Unit Supports

Consider the canonical unit-column collision sector where $\mathrm{supp}(u)$ has size $w = 2^t$ and $A_{0, r} \equiv 1 \pmod{2^t}$ for $r \in \mathrm{supp}(u)$. Then for $x \in \{0, 1\}^w$,
$$
\sum_{r=0}^{w-1} (1 - 2 x_r) \;=\; 2^t - 2\,\mathrm{wt}_H(x) \;\equiv\; 2^{t-1} \pmod{2^t}
\;\Longleftrightarrow\; \mathrm{wt}_H(x) \equiv 2^{t-2} \pmod{2^{t-1}} \qquad (t \ge 2).
$$
Similarly, the MSB carry indicator $C_{t-1}(x) := \binom{\mathrm{wt}_H(x)}{2^{t-1}} \bmod 2$ on $w = 2^{t-1}$ variables equals $1$ iff $x = 1^w$, so its algebraic normal form (ANF) over $\mathbb{F}_2$ is the full-product monomial $\prod_{r=0}^{2^{t-1}-1} x_r$ of **exact $\mathbb{F}_2$-degree $2^{t-1}$**.

**Theorem 2 (Exact Reed-Muller Orthogonality Against Low-Degree Derivatives).**
For every Boolean polynomial $Q : \mathbb{F}_2^w \to \mathbb{F}_2$ ($w = 2^{t-1}$) of algebraic degree $\deg_{\mathbb{F}_2}(Q) < 2^{t-1}$ (which includes $\Delta_u P$ for every IQP polynomial $P$ of degree $\deg_{\mathbb{F}_2}(P) \le 2^{t-1}$):
$$
\sum_{x \in \{0, 1\}^w} (-1)^{Q(x)}\,(-1)^{C_{t-1}(x)} \;=\; \sum_{x \in \{0, 1\}^w} (-1)^{Q(x)} \;-\; 2\,(-1)^{Q(1^w)},
$$
and the degree-$2^{t-1}$ ANF coefficient of $Q(x) \oplus C_{t-1}(x)$ is $\bigoplus_{x \in \{0, 1\}^w} Q(x) \oplus 1 = 0 \oplus 1 = 1 \neq 0$, so no polynomial of degree $< 2^{t-1}$ can match the carry parity $C_{t-1}(x)$ on all inputs; its minimum Hamming distance to $C_{t-1}$ is $1$ (the Reed-Muller minimum distance $2^{w - (w-1)} = 2^0 = 1$).

## 4. Theorem 3 — Clean Source-Average Bound and Label-Adaptive Sparse-Row Bound

Let $O = \sum_{j=1}^{M_{\text{terms}}} w_j\,O_{P_j, u_j}$ ($|w_j| \le 1$, $\|O\|_{\text{op}} \le 1$) be any linear combination of $M_{\text{terms}}$ conjugated IQP observables.

**Theorem 3 (Clean and Noisy Multi-Term IQP Advantage Bounds).**
1. **Label-Independent Clean & Noisy Source-Average Bound**: For any $M_{\text{terms}}$ non-zero masks $u_1, \dots, u_{M_{\text{terms}}} \in \{0, 1\}^K \setminus \{0\}$ and polynomials $P_1, \dots, P_{M_{\text{terms}}}$ chosen independently of $A \sim \mathrm{Unif}(\mathbb{Z}_{2^t}^{n \times K})$, each signed sum $\sum_{r \in \mathrm{supp}(u_j)} (1 - 2 x_r) A_{\cdot, r} \bmod 2^t$ contains at least one odd unit coefficient $\pm 1 \in \mathbb{Z}_{2^t}^\times$ and is therefore uniformly distributed over $\mathbb{Z}_{2^t}^n$. Consequently, even on a **perfectly clean source ($v = 1$)**,
   $$
   \mathbb{E}_A\bigl[\bigl|\mathrm{Adv}(O; A)\bigr|\bigr]
   \;\le\; \frac{1}{2}\sum_{j=1}^{M_{\text{terms}}} |w_j|\,v^{\mathrm{wt}_H(u_j)}\,2^{-n t}
   \;\le\; \frac{M_{\text{terms}}}{2 \cdot 2^{n t}}.
   $$
2. **Label-Adaptive Row-Sparsity Bound**: Even if $(u_j, P_j)$ are chosen **adaptively as arbitrary functions of the public label matrix $A$**, $O = \sum_{j=1}^{M_{\text{terms}}} w_j O_{P_j, u_j}$ has at most $D \le M_{\text{terms}}$ non-zero entries per row, and therefore obeys the universal $D$-sparse observable bound (`theorems/dcp_native_parity_observables.py`): on every label matrix $A$ whose minimum target-edge Hamming distance is $w_{\min}(A) \ge r + 1$,
   $$
   \bigl|\mathrm{Adv}(O; A)\bigr| \;\le\; \min\!\left(\frac{1}{2},\; \frac{\sqrt{M_{\text{terms}}}\,v^{w_{\min}(A)}}{2}\right).
   $$
