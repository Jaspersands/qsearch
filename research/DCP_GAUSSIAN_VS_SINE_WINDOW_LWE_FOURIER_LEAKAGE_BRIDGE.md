# DCP Discrete Gaussian vs. Sine vs. Box Window LWE Fourier Leakage Bridge (Subsystem 89)

## Scope & Overview
This subsystem establishes the exact finite-support Dirichlet-Laplacian variational optimality of the discrete sine window $\psi_{\mathrm{sin}}^*(x) = \sqrt{\frac{2}{P+1}} \sin(\frac{\pi(x+1)}{P+1})$ over all normalized profiles supported on $\{0, 1, \dots, P-1\}$, and compares its unit-shift coherence and QFT sidelobe leakage against truncated discrete Gaussians and uniform box windows.

## Exact Mathematical Laws
1. **Dirichlet-Laplacian Ground-State Optimality**:
   The unit-shift overlap $\gamma(1; \psi) = \sum_{x=0}^{P-2} \psi(x)\psi(x+1) = 1 - \frac{1}{2}\langle \psi, \Delta_D \psi \rangle$ is globally maximized over all normalized states on $\{0, \dots, P-1\}$ by the unique ground-state eigenvector $\psi_{\mathrm{sin}}^*$ of the $P \times P$ tridiagonal Dirichlet Laplacian $\Delta_D$, achieving:
   $$\max_{\|\psi\|_2 = 1} \gamma(1; \psi) = \cos\!\left(\frac{\pi}{P+1}\right).$$
2. **Strict Unit-Shift Ordering and Far-Sidelobe Tradeoff**:
   For moderate Gaussian widths $\sigma = 0.45 P$, $\gamma_{\mathrm{box}}(1) < \gamma_{\mathrm{gauss}}(1) < \gamma_{\mathrm{sin}}^*(1)$, while the truncated Gaussian achieves faster exponential tail decay outside the 5-bin QFT band $|k| \le 2$.
