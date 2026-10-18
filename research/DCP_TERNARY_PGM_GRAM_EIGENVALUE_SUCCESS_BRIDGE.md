# DCP Pretty Good Measurement (PGM) Gram Eigenvalue Spectrum and Square-Root Occupancy Bridge

## 1. Exact Abelian Group-Convolution Gram Spectrum and Square-Root Occupancy Law
For the $Q = q^n$ secret states $\lvert\psi_A(s)\rangle = 2^{-K/2}\sum_{x \in \{0,1\}^K} e^{2\pi i \langle Ax, s\rangle/q}\lvert x\rangle$, the $Q \times Q$ Gram matrix $G_{s,s'}(A) = \langle\psi_A(s)\rvert\psi_A(s')\rangle$ has exact Fourier eigenvalues $\lambda_y(G(A)) = \frac{Q}{2^K}N_A(y)$ where $N_A(y) = \lvert\{x \in \{0,1\}^K : Ax \equiv y \pmod q\}\rvert$, yielding the exact PGM secret-recovery probability:
$$P_{\mathrm{PGM}}(A) = \frac{1}{2^K \, Q}\left(\sum_{y \in \mathbb{Z}_q^n} \sqrt{N_A(y)}\right)^2 \le \frac{R(A)}{Q},$$
with equality if and only if $N_A(y)$ is constant across all $R(A)$ occupied residues.
