# DCP Lattice Gram-Schmidt Babai Nearest Plane vs. Coordinate Rounding Bridge (Subsystem 107)

## Scope & Overview
This subsystem establishes the exact inscribed Euclidean ball radius inequality $r_{\mathrm{CR}}(B) \le r_{\mathrm{NP}}(B)$ between Babai's Coordinate-Rounding algorithm and Babai's Nearest Plane algorithm and demonstrates explicit skewed modular lattice instances where Nearest Plane recovers the exact lattice point while Coordinate Rounding overflows.

## Exact Mathematical Laws
1. **Universal Inscribed Radius Inequality**:
   The Nearest Plane orthorhombic cell has inscribed radius $r_{\mathrm{NP}}(B) = \frac{1}{2}\min_i \|\tilde{b}_i\|_2$, whereas the Coordinate-Rounding fundamental parallelepiped has inscribed radius $r_{\mathrm{CR}}(B) = \frac{1}{2 \max_i \|(B^{-1})_{i, \cdot}\|_2} \le r_{\mathrm{NP}}(B)$, with strict inequality whenever the limiting row has non-zero Gram-Schmidt coupling.
2. **Explicit Skewed 3D Recovery Separation**:
   On $B = \begin{pmatrix} 4 & 2 & 2 \\ 0 & 4 & 2 \\ 0 & 0 & 4 \end{pmatrix}$, $r_{\mathrm{NP}}(B) = 2.0 > r_{\mathrm{CR}}(B) = 1.71499$, and the perturbation $e = (1.4, -1.4, 0)^{\top}$ is decoded with $100\%$ accuracy by Nearest Plane while overflowing Coordinate Rounding.
