# DCP Adaptive Bayesian Posterior Phase-Feedforward Alignment Bridge (Subsystem 86)

## Scope & Overview
This subsystem establishes the exact distinguishing bias and sample complexity advantage of adaptive phase-feedforward counter-rotation $R_Z(-\phi_{\mathrm{known}})$ during iterative dyadic secret bit peeling on single-qubit DCP states $\rho(a, s, \gamma)$ over $\mathbb{Z}_{2^t}$.

## Exact Mathematical Laws
1. **Quadrature Blind-Spot Obstruction of Non-Adaptive Pauli-$X$ Peeling**:
   At stage $r$ of dyadic bit peeling with known prefix $s_{\mathrm{low}} = s \bmod 2^r$ and compressed label $a = 2^{t-1-r} u$ ($u$ odd), the phase splits as $\theta(b_r) = \phi_{\mathrm{known}} + \pi b_r \pmod{2\pi}$ where $\phi_{\mathrm{known}} = \pi u s_{\mathrm{low}} / 2^r$. Fixed Pauli-$X$ measurement yields $\langle X \rangle = (-1)^{b_r} \gamma \cos(\phi_{\mathrm{known}})$, which vanishes identically ($\langle X \rangle = 0$) whenever $\phi_{\mathrm{known}} \equiv \pm \pi/2 \pmod{2\pi}$ (e.g., at $s_{\mathrm{low}} = 2^{r-1}$).
2. **Exact Phase-Feedforward Restoration**:
   Applying $R_Z(-\phi_{\mathrm{known}}) = \mathrm{diag}(1, e^{-i\phi_{\mathrm{known}}})$ maps $\rho(a, s, \gamma) \mapsto \frac{1}{2}(I + (-1)^{b_r} \gamma X)$, restoring the full Helstrom distinguishing bias $D_{\mathrm{TV}}^{\mathrm{feedforward}} = \gamma$ uniformly across all $2^r$ prefixes $s_{\mathrm{low}}$.
3. **Exact $2\times$ Fisher-Information Advantage over Non-Adaptive Random $X/Y$ Sampling**:
   Random 50/50 $X/Y$ quadrature sampling achieves effective squared-bias Fisher information $\frac{1}{2}\gamma^2(\cos^2\phi_{\mathrm{known}} + \sin^2\phi_{\mathrm{known}}) = \frac{1}{2}\gamma^2$, requiring strictly $2\times$ the sample complexity of adaptive phase-feedforward ($I_{\mathrm{eff}}^{\mathrm{feedforward}} = \gamma^2$) at every prefix $s_{\mathrm{low}}$.
