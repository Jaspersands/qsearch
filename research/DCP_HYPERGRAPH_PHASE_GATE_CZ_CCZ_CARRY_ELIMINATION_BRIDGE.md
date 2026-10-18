# DCP Hypergraph Phase-Gate ($\mathrm{CZ}$ / $\mathrm{CCZ}$) Carry Elimination Bridge (Subsystem 87)

## Scope & Overview
This subsystem resolves the exact Clifford-hierarchy degree cutoff of multi-tree overlapping CNOT carries modulo $2^t$ (extending Subsystem 63) and proves when diagonal hypergraph phase gates ($\mathrm{CZ}$ at $t=2 \pmod 4$, controlled-$S$ + $\mathrm{CCZ}$ at $t=3 \pmod 8$) deterministically unentangle overlapping CNOT compression trees.

## Exact Mathematical Laws
1. **Exact Degree-$t$ Nilpotency Cutoff Modulo $2^t$**:
   In the integer expansion of an $m$-tree shared pivot $x_r = u_1 \oplus \dots \oplus u_m = \sum_{k=1}^m (-2)^{k-1} \sum_{|J|=k} \prod_{j \in J} u_j$, every carry term of degree $k \ge t + 1$ satisfies $(-2)^{k-1} \equiv 0 \pmod{2^t}$ and vanishes identically modulo $2^t$.
2. **Exact $\mathrm{CZ}$ Unentanglement at $t = 2$ ($\bmod 4$)**:
   At $t = 2$, all degree $k \ge 3$ terms vanish modulo $4$, leaving only pairwise $(-1)^{p_r u_j u_l} = \mathrm{CZ}_{j,l}^{p_r}$ where $p_r = \langle A_{\cdot, r}, s \rangle \bmod 2$. Applying $\prod_{j < l} \mathrm{CZ}_{j,l}^{p_r}$ restores $100\%$ product state fidelity ($F = 1.0$) for any $m \ge 2$ overlapping trees.
3. **Exact Controlled-$S$ + $\mathrm{CCZ}$ Unentanglement at $t = 3$ ($\bmod 8$)**:
   At $t = 3$ with $m = 3$ overlapping trees and odd $\langle A_{\cdot, r}, s \rangle$, degree-2 repair alone leaves the 3-body $\mathrm{CCZ}$ sign flip on $\lvert 111\rangle$ ($F = 9/16 = 0.5625$), whereas adding $\mathrm{CCZ}_{1,2,3}^{p_r}$ restores $F = 1.0$.
