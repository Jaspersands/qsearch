# DCP Mod-$2$ Bucket-Pairing Disjoint Kernel Capacity and Exact Binomial Expectation Bridge

## 1. Within-Bucket Disjoint Pairing Law
Grouping the $K$ columns of $A^{(0)} = A \bmod 2 \in \mathbb{F}_2^{n \times K}$ into $2^n$ residue buckets $B_c = \{r : A^{(0)}_{\cdot, r} = c\}$ of size $k_c$ extracts $k_{0^n}$ weight-$1$ kernel wires and $\sum_{c \ne 0^n} \lfloor k_c / 2 \rfloor$ disjoint weight-$2$ kernel wires:
$$m_{\mathrm{pair}}(A) = k_{0^n} + \sum_{c \in \mathbb{F}_2^n \setminus \{0^n\}} \left\lfloor \frac{k_c}{2} \right\rfloor \ge \frac{K - (2^n - 1)}{2}.$$

## 2. Exact Closed-Form Ensemble Expectation
Under uniform random $A^{(0)} \in \mathbb{F}_2^{n \times K}$, for all $n \ge 1$ and $K \ge 1$:
$$\mathbb{E}_{A^{(0)}}\big[m_{\mathrm{pair}}(A^{(0)})\big] = \frac{K}{2} + \frac{K}{2^{n+1}} - \frac{2^n - 1}{4}\Big(1 - \big(1 - 2^{1-n}\big)^K\Big).$$
