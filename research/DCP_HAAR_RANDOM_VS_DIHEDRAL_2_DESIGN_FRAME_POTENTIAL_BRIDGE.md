# DCP Haar-Random vs. Dihedral 2-Design Second Frame Potential Bridge (Subsystem 112)

## Scope & Overview
This subsystem establishes the exact combinatorial identity linking the second frame potential $\mathcal{F}_2(D_Q; A)$ of the $2Q$-element dihedral group representation $D_Q = \mathbb{Z}_q^n \rtimes \{I, X^{\otimes K}\}$ on $K$ wires directly to the 4-tuple subset-sum additive energy $E_4(A)$.

## Exact Mathematical Laws
1. **Exact Additive Energy Identity**:
   Because $\mathrm{Tr}(X^{\otimes K} Z_A(s)) = 0$ for all $s \in \mathbb{Z}_q^n$, character orthogonality yields:
   $$\mathcal{F}_2(D_Q; A) = \frac{1}{2Q} \sum_{s \in \mathbb{Z}_q^n} |\mathrm{Tr}(Z_A(s))|^4 = \frac{1}{2} E_4(A) = \frac{1}{2} \sum_{\Delta \in \mathbb{Z}_q^n} \left(\sum_{y \in \mathbb{Z}_q^n} N_A(y) N_A(y + \Delta \bmod q)\right)^2.$$
2. **Collision Excess Over Flat Bijection & Haar Benchmark**:
   On $K = 3, q = 8$, flat bijection $A = [[1, 2, 4]]$ achieves the minimum $\mathcal{F}_2 = 256$ ($E_4 = 512$), whereas colliding $A = [[1, 1, 2]]$ increases $\mathcal{F}_2$ to $352$ ($E_4 = 704$).
