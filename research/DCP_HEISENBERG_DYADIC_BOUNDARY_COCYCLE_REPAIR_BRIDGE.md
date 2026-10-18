# DCP Dyadic Heisenberg $H_3(\mathbb{Z}_{2^t})$ Coherent Boundary-Cocycle Phase-Repair Bridge

## 1. Public-Carry Boundary Cocycle Repair Unitary $U_{\mathrm{cocycle}}(b; \Delta)$
In $H_3(\mathbb{Z}_{2^t})$, the wrap-around defect $\binom{x + 2^t}{2} \equiv \binom{x}{2} + 2^{t-1} \pmod{2^t}$ multiplies the finite-difference state by $(-1)^{s_1 \cdot \mathbf{1}[x_1 + \Delta \ge 2^t]}$. Applying the public carry-controlled $Z$ gate $U_{\mathrm{cocycle}}(b; \Delta)\lvert x_1\rangle = (-1)^{b \cdot \mathbf{1}[x_1 + \Delta \ge 2^t]}\lvert x_1\rangle$ with $b = s_1 \bmod 2$ restores $100\%$ unit $\mathrm{QFT}_{2^t}^\dagger$ concentration at $k_1 \equiv \Delta s_1 \pmod{2^t}$ across all $2^t$ shifts $\Delta \in \mathbb{Z}_{2^t}$.

## 2. Deterministic Single-Shot Parity Extraction at $\Delta = 2^{t-1}$
At the half-period shift $\Delta = 2^{t-1}$, $\mathbf{1}[x_1 + 2^{t-1} \ge 2^t] = \mathrm{MSB}(x_1)$, rendering the unrepaired even-$s_1$ and odd-$s_1$ difference states orthogonal and enabling single-shot $X$-basis extraction of $s_1 \bmod 2$ on $\mathrm{MSB}(x_1)$ with probability $1.0$.
