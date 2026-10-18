# DCP $d$-ary Qudit Phase-Register Modular SUM Carry and Step-Function Linearity Bridge

## 1. Universal Mod-$d$ Descent and Higher-Radix Step-Function Non-Linearity ($d \ge 3$)
Under the $d$-ary modular SUM gate $x_r(u; y) = (y_r + v_r u) \bmod d$ over $\mathbb{Z}_{d^t}^n$:
$$\Phi(u; y) - \Phi(0; y) \equiv (A v) u - d \sum_{r \in \mathrm{supp}(v)} A_{\cdot, r} \mathbf{1}[y_r + u \ge d] \pmod{d^t}.$$
- Whenever $A v \equiv 0 \pmod d$, $\Phi(u; y) - \Phi(0; y) \equiv 0 \pmod d$ holds across $100\%$ of syndromes $y \in \mathbb{Z}_d^K$.
- For $d = 2$ ($u \in \{0, 1\}$), $\mathbf{1}[y_r + u \ge 2] = y_r u$ is linear in $u$ for all $y_r$, whereas for $d \ge 3$, $\mathbf{1}[y_r + u \ge d]$ is a non-linear step function of $u \in \mathbb{Z}_d$ for $y_r \ne 0$, so all-anchor linearity modulo $d^t$ holds iff $A_{\cdot, r} \equiv 0 \pmod{d^{t-1}}$ for all $r \in \mathrm{supp}(v)$.
