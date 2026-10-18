# DCP Odd-Prime Modulus $\mathbb{Z}_p$ vs. Dyadic $\mathbb{Z}_{2^t}$ CNOT Zero-Sum Carry-Shift Obstruction

## 1. Invertibility of $2 \in \mathbb{F}_p^\times$ and Absence of Non-Trivial Anchor-Invariant CNOT Kernels
For any odd prime $p \ge 3$, $\gcd(2, p) = 1$, so flipping an anchor bit $(x_0)_r \in \{0, 1\}$ shifts $\tilde{A}(v, x_0) \pmod p$ by $-2 A_{\cdot, r} \pmod p$. Consequently, $\tilde{A}(v, x_0) \equiv A v \pmod p$ holds for all $x_0 \in \{0, 1\}^K$ if and only if $A_{\cdot, r} \equiv 0 \pmod p$ for all $r \in \mathrm{supp}(v)$.

## 2. Monochrome-Syndrome $2^{-(h-1)}$ Zero-Sum Law and Sub-Witness Escape
For a zero-sum witness $A v \equiv 0 \pmod p$ of Hamming weight $h = \mathrm{wt}(v) \ge 2$, $\tilde{A}(v, x_0) \equiv 0 \pmod p$ holds if and only if $\sum_{r \in \mathrm{supp}(v) : (x_0)_r = 1} A_{\cdot, r} \equiv 0 \pmod p$. Thus minimal (subset-sum-free) zero-sum witnesses achieve $\tilde{A}(v, x_0) \equiv 0 \pmod p$ on a fraction of anchors equal to $2^{-(h-1)}$ (only the monochrome $0^h$ and $1^h$ assignments).
