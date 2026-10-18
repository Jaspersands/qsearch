# DCP Walsh-Hadamard Bent-Function Nonlinear Carry Spectrum Bridge (Subsystem 109)

## Scope & Overview
This subsystem establishes the exact Walsh-Hadamard Fourier spectrum of the quadratic binary-XOR carry phase function $f_{\mathrm{sym}}(u) = \sum_{1 \le j < l \le m} u_j u_l \pmod 2$ on $m$ overlapping CNOT survivor wires at modulus $q = 4$ ($t = 2$).

## Exact Mathematical Laws
1. **Even Overlap Multiplicity ($m = 2k$) — Bent Flat Spectrum**:
   Because $J_{2k} - I_{2k}$ has full rank $2k$ over $\mathbb{F}_2$ for even $m = 2k$, $f_{\mathrm{sym}}(u)$ is a maximally nonlinear bent Boolean function with flat Hadamard spectrum $|\widehat{F}(w)| = 2^{-k} = 2^{-m/2}$ and uniform outcome distribution $P(w) = 2^{-2k}$ ($H = 2k$ bits).
2. **Odd Overlap Multiplicity ($m = 2k + 1$) — Semi-Bent Spectrum**:
   For odd $m = 2k + 1$, $J_{2k+1} - I_{2k+1}$ has rank $2k$ and kernel $\mathrm{span}\{1^{2k+1}\}$, concentrating $P(w) = 2^{-2k}$ onto half of the Hadamard strings ($H = 2k$ bits).
