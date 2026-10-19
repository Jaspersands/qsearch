# DCP Clifford CNOT Logarithmic Binary Tree vs. Linear Chain Depth Bridge (Subsystem 130)

## Scope & Overview
This subsystem establishes the exact zero-syndrome subspace equivalence ($\mathrm{span}\{\lvert 0^h\rangle, \lvert 1^h\rangle\}$) and exponential idle-memory decoherence separation between a depth-$\lceil \log_2 h \rceil$ balanced binary fan-in CNOT tree and a depth-$(h-1)$ linear CNOT star/chain.

## Exact Mathematical Laws
1. **Gate-Count & Zero-Syndrome Subspace Equivalence**:
   Both topologies use exactly $h - 1$ CNOT gates and project the all-zero syndrome $d = 0^{h-1}$ onto the identical 2D subspace $x_0 = \dots = x_{h-1}$.
2. **Super-Exponential Idle-Memory Coherence Gain**:
   Reducing circuit depth from $h - 1$ to $\log_2 h$ cuts qubit-layer idle volume from $h(h-1)$ to $h\log_2 h$, boosting coherence visibility by $\exp(\alpha_{\mathrm{idle}} h(h - 1 - \log_2 h))$ ($> 5.81\times$ at $h = 16, \alpha_{\mathrm{idle}} = 0.01$).
