# Planted $q$-ary MacWilliams Dual Weight Enumerator Bridge

## 1. Exact Identities Established
1. **$q$-ary MacWilliams Krawtchouk Transform**:
   For any check matrix $B \in \mathbb{F}_q^{d \times n}$ with row-space weight enumerator $A_w(B)$ and dual weight enumerator $A_k^\perp(B) = |\{z \in \ker(B) : \mathrm{wt}_H(z) = k\}|$:
   $$A_k^\perp(B) = q^{-d} \sum_{w=0}^n A_w(B) K_k(w; n, q).$$
2. **Noisy $\mathrm{QFT}_q^{\otimes n}$ Valid-Check Probability Bridge**:
   Under $q$-ary depolarizing rate $\gamma \in [0,1]$ ($p_0 = 1 - \gamma(q-1)/q$, $p_{\neq 0} = \gamma/q$),
   $$P_{\mathrm{valid}}(B, \gamma) = \sum_{k=0}^n A_k^\perp(B) p_0^{n-k} p_{\neq 0}^k = q^{-d} \sum_{w=0}^n A_w(B) (1 - \gamma)^w.$$
3. **Scoped Off-Dual vs. On-Dual Controls**:
   - When $B s \neq 0 \pmod q$ (off-dual secret), exactly $1/q$ of row-space checks satisfy $\langle u^T B, s \rangle = 0 \pmod q$.
   - When $s \in \ker(B)$ ($B s = 0 \pmod q$, on-dual constructive control), $100\%$ of row-space checks satisfy $\langle u^T B, s \rangle = 0 \pmod q$.
