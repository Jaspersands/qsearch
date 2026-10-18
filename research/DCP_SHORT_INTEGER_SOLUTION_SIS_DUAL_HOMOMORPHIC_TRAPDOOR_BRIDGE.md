# DCP Short Integer Solution (SIS) Dual Gadget Trapdoor Witness Compilation Bridge (Subsystem 115)

## Scope & Overview
This subsystem establishes the exact constructive duality between Micciancio-Peikert / GPV gadget trapdoors $A = [G \mid -G R \bmod 2^t]$ for the SIS lattice $\Lambda_{2^t}^\perp(A)$ and zero-carry binary CNOT witness compilation.

## Exact Mathematical Laws
1. **Exact Binary Zero-Sum Trapdoor Identity**:
   For $G = I_n \otimes [1, 2, \dots, 2^{t-1}]$ and binary $R \in \{0,1\}^{(nt) \times m}$, $T = \begin{pmatrix} R \\ I_m \end{pmatrix} \in \{0,1\}^{K \times m}$ satisfies $A T \equiv 0 \pmod{2^t}$ with zero carry defect on the all-zero CNOT syndrome branch.
2. **Punctured Dyadic Scale Extraction**:
   Puncturing a single active gadget bit $\mathrm{idx} = i t + r$ from column $t_j$ ($v = t_j - e_{\mathrm{idx}} \in \{0,1\}^K$) yields $A v \equiv -2^r e_i \pmod{2^t}$, which Pauli-$X$ sign rectification converts into the exact canonical dyadic scale $+2^r e_i \pmod{2^t}$.
