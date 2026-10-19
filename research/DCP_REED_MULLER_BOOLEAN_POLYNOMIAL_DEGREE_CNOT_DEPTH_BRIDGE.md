# DCP Reed-Muller Boolean Polynomial Degree to CNOT Parity-Gadget Synthesis Bridge (Subsystem 122)

## Scope & Overview
This subsystem establishes the exact $(2^d - 1)$-term integer parity-XOR expansion of any degree-$d$ binary product $2^{d-1}\prod_{j=1}^d u_j$ and proves that every $d$-body hypergraph carry gate $\mathrm{C}^{d-1}Z = \mathrm{diag}((-1)^{u_1 \cdots u_d})$ decomposes into $2^d - 1$ CNOT-conjugated phase rotations of angle $\pm \pi / 2^{d-1}$.

## Exact Mathematical Laws
1. **Exact Integer Parity-XOR Identity Over $\mathbb{Z}$**:
   For all $u \in \{0, 1\}^d$:
   $$2^{d-1}\prod_{j=1}^d u_j = \sum_{\emptyset \neq S \subseteq \{1, \dots, d\}} (-1)^{|S|-1} \left(\bigoplus_{j \in S} u_j\right).$$
2. **Exact $(2^d - 1)$ Gadget Counts**:
   Synthesizing $\mathrm{CZ}$ ($d=2$), $\mathrm{CCZ}$ ($d=3$), and $\mathrm{C}^3Z$ ($d=4$) requires exactly $3$ ($\pm \pi/2$), $7$ ($\pm \pi/4$), and $15$ ($\pm \pi/8$) single-qubit phase gadgets respectively.
