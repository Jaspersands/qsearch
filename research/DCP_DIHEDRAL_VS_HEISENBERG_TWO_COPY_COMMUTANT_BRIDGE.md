# DCP Dihedral Sign-Inversion vs. Heisenberg $H_3(\mathbb{Z}_{2^t}) / H_3(\mathbb{Z}_p)$ Two-Copy Commutator Bridge

## 1. Odd-Prime $H_3(\mathbb{Z}_p)$ Unit Concentration vs. Dyadic $H_3(\mathbb{Z}_{2^t})$ Boundary-Cocycle Law
- **Odd Prime $p \ge 3$**: Because $2^{-1} \equiv (p+1)/2 \pmod p$ exists in $\mathbb{F}_p$, $\binom{x+p}{2} \equiv \binom{x}{2} \pmod p$ is strictly $p$-periodic, so coherent shift-difference $x_2 \equiv x_1 + \Delta \pmod p$ concentrates $\mathrm{QFT}_p^\dagger$ onto $k_1 \equiv \Delta s_1 \pmod p$ with probability $1.0$ for all $\Delta \in \mathbb{Z}_p$.
- **Dyadic Modulus $q = 2^t$**: Because $(1, s_1, s_2)^{2^t} = (0, 0, 2^{t-1}s_1 \bmod 2^t)$, $\binom{x+2^t}{2} \equiv \binom{x}{2} + 2^{t-1} \pmod{2^t}$ flips the sign on the last $\Delta$ wrap-around states $x_1 \in [2^t - \Delta, 2^t - 1]$ when $s_1$ is odd, yielding the exact closed-form peak probability:
$$P_{\mathrm{QFT}_{2^t}}\!\big(k_1 = \Delta s_1 \bmod 2^t\big) = \begin{cases} 1 & \text{if } s_1 \equiv 0 \pmod 2, \\ \left(1 - \dfrac{2\Delta}{2^t}\right)^2 & \text{if } s_1 \equiv 1 \pmod 2. \end{cases}$$
