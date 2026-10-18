# DCP CNOT-Star-Conjugated Schur-Weyl Projector Selection Rules and Harmonic Parity Bridge

## 1. Bitwise-Complement Weight Shift Identity ($w_{\mathrm{star}}(\bar{x}) = w_{\mathrm{star}}(x) \pm 1$)
Under the $r$-qubit CNOT star $U_{\mathrm{star}}\lvert x_0, x_1, \dots, x_{r-1}\rangle = \lvert x_0, x_1 \oplus x_0, \dots, x_{r-1} \oplus x_0\rangle$, any bitstring $x \in \{0,1\}^r$ and its bitwise complement $\bar{x} = x \oplus 1^r$ have identical syndrome bits and opposite control bits, so $w_{\mathrm{star}}(\bar{x}) = w_{\mathrm{star}}(x) + (1 - 2x_0) \ne w_{\mathrm{star}}(x)$. Because every $\pi \in S_r$ preserves Hamming weight, $\langle x \rvert U_{\mathrm{star}}^\dagger \Pi_\lambda U_{\mathrm{star}} \lvert \bar{x}\rangle = 0$ identically for all $r \ge 1$ and $\lambda \vdash r$, excluding all degree-$r$ phase harmonics without a control-wire Hadamard gate $H_0$.

## 2. Odd-$r$ Even-Harmonic Restriction and $r=3$ Closed-Form Law
For odd $r$, every pair $(x, y)$ with $w_{\mathrm{star}}(x) = w_{\mathrm{star}}(y)$ has even Hamming distance $\mathrm{wt}(x \oplus y) \equiv 0 \pmod 2$. At $r = 3$:
$$\mathrm{Tr}\!\big(U_{\mathrm{star}}^\dagger \Pi_{\mathrm{Sym}^3} U_{\mathrm{star}} (\rho_0 \otimes \rho_1 \otimes \rho_2)\big) = \frac{1}{2} + \frac{1}{6}\Big(\gamma_1\gamma_2\cos(\theta_1 - \theta_2) + \gamma_0\cos\theta_0\big(\gamma_1\cos\theta_1 + \gamma_2\cos\theta_2\big)\Big).$$
