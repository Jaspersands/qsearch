# DCP Even-Sublattice Parity Blindness and Mod-$2^{t-1}$ Rescaling Bridge

## 1. Scope and Motivation
When disjoint $\bmod 2$-kernel vectors $V_1, \dots, V_m \in \ker(A \bmod 2)$ are applied to compress the clean DCP state conditioned on the anchor subspace event $y = (I_K, V) u$, the resulting effective columns
$$\tilde{A}_j(x_0) = \sum_{r \in \mathrm{supp}(V_j)} (1 - 2(x_0)_r) A_{\cdot, r} \pmod{2^t}$$
satisfy $\tilde{A}_j(x_0) \equiv A V_j \equiv 0 \pmod 2$ for every anchor $x_0 \in \{0,1\}^K$. Thus $\tilde{A}_j(x_0)$ lies in the index-$2^n$ even sublattice $(2\mathbb{Z}_{2^t})^n$, not the full group $\mathbb{Z}_{2^t}^n$.

## 2. Exact Theorems Established
1. **Universal Evenness & Odd-Shift Blindness**:
   Every compressed difference $\tilde{A}(x_0)(u - u') \bmod 2^t$ is even in every coordinate. Consequently, any shift $h \in \mathbb{Z}_{2^t}^n$ with at least one odd coordinate (including the $t=1$ half-period target $h = (1, 0, \dots, 0)$) has strictly zero compressed collisions and $\mathrm{Adv}_{\mathrm{cond}} = 0$ identically across all $A, V, x_0$.
2. **Exact Halving Isomorphism ($t \ge 2$)**:
   Dividing by $2$ defines an exact bijection $B_j(x_0) = (\tilde{A}_j(x_0) \bmod 2^t)/2 \in \mathbb{Z}_{2^{t-1}}^n$, mapping the half-period target $h = (2^{t-1}, 0, \dots, 0) \in \mathbb{Z}_{2^t}^n$ to $h' = (2^{t-2}, 0, \dots, 0) \in \mathbb{Z}_{2^{t-1}}^n$.
3. **Fixed-Instance vs. Upper-Bit Ensemble Dichotomy**:
   - **Fixed-Instance Resonant Controls**: For $A = [[2, 0]] \bmod 4$ and $V_1 = (1, 1)^T$, $B_1(x_0) = 1 \pmod 2$ for all $4$ anchors ($\mathrm{Adv}_{\mathrm{cond}} = 1.0$, unconditional branch contribution $1/2$). For $A = [[1, 1]] \bmod 4$ and $V_1 = (1, 1)^T$, $B_1(x_0) = 1 \pmod 2$ for half of the anchors ($\mathbb{E}_{x_0}[\mathrm{Adv}_{\mathrm{cond}}] = 1/2$, unconditional branch contribution $1/4$).
   - **Upper-Bit Ensemble Uniformity over $\mathbb{Z}_{2^{t-1}}^n$**: Decomposing $A = A^{(0)} + 2 A^{(\mathrm{high})}$ with $A^{(0)} = A \bmod 2$ and $A^{(\mathrm{high})} = \lfloor A/2 \rfloor \in (\mathbb{Z}_{2^{t-1}})^{n \times K}$, for any fixed $(A^{(0)}, V_1, \dots, V_m, x_0)$ with disjoint non-empty supports, as $A^{(\mathrm{high})}$ varies uniformly over $(\mathbb{Z}_{2^{t-1}})^{n \times K}$, the halved columns $(B_1(x_0), \dots, B_m(x_0))$ are exact IID uniform over $(\mathbb{Z}_{2^{t-1}}^n)^m$ with reduced group size $Q_{\mathrm{even}} = 2^{n(t-1)}$.
