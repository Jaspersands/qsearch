# DCP Coherent CNOT Uncomputation Echo Visibility Bridge (Subsystem 106)

## Scope & Overview
This subsystem resolves the exact expectation value of a compressed survivor wire when the syndrome target wire is uncomputed via $\mathrm{CNOT}_{0 \to 1}^\dagger$ (or traced out without $Z_1$ syndrome readout) versus measured in the computational $Z_1$ basis.

## Exact Mathematical Laws
1. **Exact Heisenberg Parity Identity**:
   Because $\mathrm{CNOT}_{0 \to 1}^\dagger (X_0 \otimes I_1) \mathrm{CNOT}_{0 \to 1} = X_0 \otimes X_1$, probing $X_0$ without reading out $Z_1$ yields $\langle X_0 \rangle_{\mathrm{uncomputed}} = \gamma^2 \cos(\theta_0)\cos(\theta_1) = \frac{1}{2}\gamma^2(\cos(\theta_0 + \theta_1) + \cos(\theta_0 - \theta_1))$.
2. **Quarter-Period Blind Spot of Uncomputed Echo on Zero-Sum Pairs**:
   On a zero-sum pair $\theta_0 + \theta_1 \equiv 0 \pmod{2\pi}$, conditioning on $d_1 = 0$ maintains constant visibility $+\gamma^2$ across all $\theta_0$, whereas uncomputing $d_1$ mixes the sum and difference branches $50/50$ into $\gamma^2 \cos^2(\theta_0)$, vanishing identically at $\theta_0 = \pm \pi/2$.
