# DCP Radix-4 Quaternary QFT Butterfly Stage-Depth Halving Bridge (Subsystem 119)

## Scope & Overview
This subsystem establishes the exact unitary equivalence between the $k$-stage radix-4 quaternary Cooley-Tukey $\mathrm{QFT}_{4^k}^\dagger$ and the $2k$-stage radix-2 $\mathrm{QFT}_{2^{2k}}^\dagger$, proving an exact $2\times$ reduction in outer Cooley-Tukey stages and strict truncation fidelity dominance.

## Exact Mathematical Laws
1. **Radix-4 Kronecker Factorization & $2\times$ Stage Halving**:
   Pairing $m = 2k$ qubits into $k$ base-4 digit pairs replaces the $2k$ radix-2 stages with $k$ radix-4 stages using local 2-qubit $\mathrm{QFT}_4^\dagger$ blocks.
2. **Band-1 Local $\mathrm{QFT}_4^\dagger$ Block Dominance**:
   Dropping all inter-pair twiddles yields the depth-2 tensor product $(\mathrm{QFT}_4^\dagger)^{\otimes k}$, achieving $100\%$ peak survival on 4-adic multiples ($y = 4$ on $N = 16$: $1.00$ vs. $0.50$ for $H^{\otimes 4}$) and strictly dominating radix-2 band-1 truncation on general odd frequencies ($y = 5$: $0.7286$ vs. $0.5177$).
