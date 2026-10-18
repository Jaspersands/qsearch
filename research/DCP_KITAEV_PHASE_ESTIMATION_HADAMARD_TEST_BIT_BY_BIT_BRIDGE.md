# DCP Kitaev Non-Adaptive $X/Y$ Hadamard Test vs. Coherent $R_Z$ Feedforward Bridge (Subsystem 111)

## Scope & Overview
This subsystem compares Kitaev's non-adaptive two-quadrature ($X$ and $Y$) Hadamard test with classical Bayesian post-rotation against coherent adaptive $R_Z(-\phi_{\mathrm{known}})$ phase feedforward (Subsystem 86).

## Exact Mathematical Laws
1. **2-Copy Kitaev vs. 1-Copy Coherent Feedforward Bayes Error Identity**:
   Even with optimal LLR post-rotation using $\phi_{\mathrm{known}}$, measuring 1 copy in $X$ and 1 copy in $Y$ yields exact Bayes error $\frac{1}{2}(1 - \gamma \max(|\cos\phi|, |\sin\phi|)) \ge \frac{1}{2}(1 - \gamma)$, which at $\phi = \pi/4, \gamma = 0.8$ ($0.21716$) is more than $2\times$ worse than a single copy of coherent $R_Z(-\phi_{\mathrm{known}})$ feedforward ($0.10$).
2. **Exact $2.0\times$ Per-Copy Fisher Information Gain**:
   Coherent $R_Z(-\phi_{\mathrm{known}})$ feedforward achieves $I_{\mathrm{Fisher}} = \gamma^2 = 2 I_{\mathrm{Fisher}}^{\text{Kitaev-}XY}$ across all $\phi_{\mathrm{known}}$.
