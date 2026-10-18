# DCP Bipartite Entanglement Entropy Across the Survivor-Syndrome Cut Bridge (Subsystem 99)

## Scope & Overview
This subsystem establishes the exact pre-measurement bipartite purity $\mathrm{Tr}(\rho_{\mathrm{surv}}(s)^2)$ and Rényi-2 entanglement entropy $S_2(\rho_{\mathrm{surv}}(s))$ across the cut separating the compressed survivor wire from the $(h-1)$ syndrome wires in a weight-$h$ CNOT witness tree.

## Exact Mathematical Laws
1. **Exact Cosine-Product Purity Identity**:
   Tracing out the $(h-1)$ syndrome wires prior to readout leaves the survivor wire with exact purity:
   $$\mathrm{Tr}\!\left(\rho_{\mathrm{surv}}(s)^2\right) = \frac{1}{2}\left(1 + \prod_{r=1}^{h-1} \cos^2\!\left(\frac{2\pi \langle A_{\cdot, r}, s \rangle}{q}\right)\right).$$
2. **Separability vs. Maximal Bell Entanglement**:
   The cut is separable ($S_2 = 0$) iff $2\langle A_{\cdot, r}, s \rangle \equiv 0 \pmod q$ for all $r \ge 1$, and maximally Bell-entangled ($S_2 = 1$ bit, purity $0.5$) iff at least one syndrome wire sits at a quarter-period $\cos(2\pi \langle A_{\cdot, r}, s \rangle / q) = 0$.
