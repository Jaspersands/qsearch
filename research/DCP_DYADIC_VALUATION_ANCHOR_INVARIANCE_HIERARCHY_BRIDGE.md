# DCP Dyadic Valuation and Mod-$2^k$ Anchor-Invariance Hierarchy Bridge

## 1. Exact Equivalence Theorem
For any $A \in \mathbb{Z}_{2^t}^{n \times K}$, $v \in \{0,1\}^K$, and $1 \le k \le t$:
$$\tilde{A}(v, x_0) \equiv A v \pmod{2^k} \quad \forall x_0 \in \{0,1\}^K \quad \Longleftrightarrow \quad A_{\cdot, r} \equiv 0 \pmod{2^{k-1}} \quad \forall r \in \mathrm{supp}(v).$$
- At $k = 1$ ($\bmod 2$), $2^{k-1} = 1$ divides every integer, so $\tilde{A}(v, x_0) \equiv A v \pmod 2$ is universally anchor-invariant.
- At $k = 2$ ($\bmod 4$), if $A v \equiv 0 \pmod 4$ but $\mathrm{supp}(v)$ contains an odd entry $A_{i,r} \equiv 1 \pmod 2$, $\tilde{A}_i(v, x_0) \bmod 4$ splits $50/50$ between $0$ and $2 \pmod 4$.
- When $A_{\cdot,r} \equiv 0 \pmod{2^{k-1}}$ for all $r \in \mathrm{supp}(v)$ (constructive even/doubly-even controls), $\tilde{A}(v, x_0) \equiv A v \pmod{2^k}$ holds across $100\%$ of anchors.
