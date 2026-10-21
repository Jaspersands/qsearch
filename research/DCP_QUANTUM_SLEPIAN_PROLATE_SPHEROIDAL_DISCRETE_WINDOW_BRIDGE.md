# DCP Slepian Discrete Prolate Spheroidal Sequence (DPSS) Mainlobe Concentration Bridge (Subsystem 125)

## Scope & Overview
This subsystem establishes the exact Rayleigh-Ritz variational duality between the Discrete Prolate Spheroidal Sequence (DPSS / Slepian ground state $\psi_{\mathrm{DPSS}}^*$) and the Dirichlet-Laplacian sine window ($\psi_{\mathrm{sin}}^*$, Subsystem 89) on finite quantum registers $\{0, \dots, P-1\}$.

## Exact Mathematical Laws
1. **Slepian Variational Optimality for In-Band QFT Concentration**:
   The principal eigenvector $\psi_{\mathrm{DPSS}}^*(x; P, B)$ of the $P \times P$ Dirichlet-Toeplitz kernel $(K_B)_{x,y} = \frac{\sin(\pi(2B+1)(x-y)/P)}{P\sin(\pi(x-y)/P)}$ globally minimizes out-of-band QFT leakage $L_{\mathrm{leak}}(B) = 1 - \langle \psi, K_B \psi \rangle$.
2. **Complementary Pareto Frontier**:
   At $B = 1$ (3-bin mainlobe), $L_{\mathrm{leak}}(1; \psi_{\mathrm{DPSS}}^*) < L_{\mathrm{leak}}(1; \psi_{\mathrm{sin}}^*) < L_{\mathrm{leak}}(1; \psi_{\mathrm{box}})$, while $\gamma(1; \psi_{\mathrm{box}}) < \gamma(1; \psi_{\mathrm{DPSS}}^*) < \gamma(1; \psi_{\mathrm{sin}}^*) = \cos(\frac{\pi}{P+1})$, with $|\langle \psi_{\mathrm{sin}}^* \mid \psi_{\mathrm{DPSS}}^* \rangle|^2 > 0.998$.
