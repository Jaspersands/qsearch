# DCP Pauli/Sign Twirling Coherent Carry to Stochastic Dephasing Bridge (Subsystem 121)

## Scope & Overview
This subsystem establishes the exact quadratic suppression of worst-case trace distance when a coherent residual carry phase error $U_\delta = \mathrm{diag}(1, e^{i\delta})$ on a survivor wire is conjugated by $\{I, X\}$ Pauli twirling (or averaged over balanced $\pm \delta$ syndrome branches).

## Exact Mathematical Laws
1. **Linear Coherent vs. Quadratic Twirled Trace Distance**:
   While $U_\delta\lvert +\rangle$ has linear trace distance $D_{\mathrm{tr}}^{\mathrm{coherent}}(\delta) = |\sin(\delta/2)| = O(|\delta|)$ from $\lvert +\rangle\langle +\rvert$, $\{I, X\}$ twirling cancels the off-diagonal imaginary commutator skew $\pm i \sin(\delta/2)\cos(\delta/2)(Z\rho - \rho Z)$ and yields the pure phase-flip channel $\cos^2(\delta/2)\rho + \sin^2(\delta/2)Z\rho Z$ with exact quadratic trace distance:
   $$D_{\mathrm{tr}}^{\mathrm{twirled}}(\delta) = \sin^2\!\left(\frac{\delta}{2}\right) = \left(D_{\mathrm{tr}}^{\mathrm{coherent}}(\delta)\right)^2,$$
   achieving a $> 20.0\times$ error suppression at $\delta = 0.10$ rad ($0.04998 \to 0.002498$).
