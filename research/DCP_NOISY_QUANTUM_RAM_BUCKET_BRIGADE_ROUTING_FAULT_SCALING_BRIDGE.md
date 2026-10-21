# DCP Noisy Quantum RAM Bucket-Brigade Routing Fault Scaling Bridge (Subsystem 137)

## Scope & Overview
This subsystem establishes the exact query fidelity separation between a Giovannetti-Lloyd-Maccone Bucket-Brigade qRAM and a conventional Fanout-Decoder qRAM when coherently looking up subset-sum fiber representatives in a table of size $L = 2^d$.

## Exact Mathematical Laws
1. **Logarithmic vs. Exponential Switch Activation**:
   A fanout decoder activates all $2^d - 1$ switches per query ($F_{\mathrm{fanout}} = (1 - \epsilon_{\mathrm{active}})^{2^d-1}$), whereas a Bucket-Brigade qRAM activates only $d$ switches along the addressed root-to-leaf path ($F_{\mathrm{BB}} = (1 - \epsilon_{\mathrm{active}})^d (1 - \epsilon_{\mathrm{wait}})^{2^d-1-d}$), achieving a $> 64.4\times$ infidelity reduction at $d = 10$ ($L = 1024, \epsilon_{\mathrm{active}} = 10^{-3}$).
