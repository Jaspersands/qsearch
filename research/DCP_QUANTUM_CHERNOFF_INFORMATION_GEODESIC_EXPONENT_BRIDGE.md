# DCP Quantum Chernoff Information Geodesic Exponent Bridge (Subsystem 120)

## Scope & Overview
This subsystem establishes the exact closed-form Quantum Chernoff Bound (QCB) exponent $\xi_{\mathrm{QCB}}(\Delta\theta, \gamma)$ between single-qubit DCP states $\rho(\theta_0, \gamma)$ and $\rho(\theta_1, \gamma)$ and proves a strict collective multi-copy exponent advantage over optimal separable Helstrom measurements at all non-commuting phase differences $\Delta\theta \notin \{0, \pi\} \bmod 2\pi$.

## Exact Mathematical Laws
1. **Midpoint Optimality ($s^* = 1/2$) & Quantum Bhattacharyya Formula**:
   $$\min_{0 \le s \le 1} \mathrm{Tr}(\rho_0^s \rho_1^{1-s}) = \mathrm{Tr}(\rho_0^{1/2}\rho_1^{1/2}) = 1 - \left(1 - \sqrt{1 - \gamma^2}\right)\sin^2\!\left(\frac{\Delta\theta}{2}\right).$$
2. **Strict Collective Exponent Advantage at Non-Commuting Phases**:
   By the strict concavity of $u \mapsto \sqrt{1 - \gamma^2 u}$ on $(0, 1)$, $\mathrm{Tr}(\rho_0^{1/2}\rho_1^{1/2}) < \sqrt{1 - \gamma^2 \sin^2(\Delta\theta/2)} = B_{\mathrm{sep\text{-}Hel}}$, yielding $\xi_{\mathrm{QCB}} > \xi_{\mathrm{sep\text{-}Hel}}$ ($> 1.15\times$ at $\Delta\theta = \pi/2, \gamma = 0.85$) and exact equality at commuting $\Delta\theta = \pi$.
