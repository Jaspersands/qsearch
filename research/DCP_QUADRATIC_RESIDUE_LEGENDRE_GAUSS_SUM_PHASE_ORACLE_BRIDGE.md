# DCP Quadratic Residue Legendre-Gauss Sum Phase Oracle Bridge (Subsystem 104)

## Scope & Overview
This subsystem establishes the exact evaluation of prime-modulus quadratic Gauss sums $G(z; p) = \sum_{x=0}^{p-1} e^{2\pi i z x^2 / p}$ and proves how phase kickback against the Legendre-weighted Fourier state extracts the exact multiplicative binary residuosity sign $\left(\frac{a s}{p}\right) = \left(\frac{a}{p}\right)\left(\frac{s}{p}\right) \in \{-1, +1\}$.

## Exact Mathematical Laws
1. **Exact Gauss Sum Law Over $\mathbb{Z}_p$**:
   For any odd prime $p$ and any $z \in \mathbb{F}_p^\times$, $G(z; p) = \left(\frac{z}{p}\right) \varepsilon_p \sqrt{p}$, where $\varepsilon_p = 1$ if $p \equiv 1 \pmod 4$ and $\varepsilon_p = i$ if $p \equiv 3 \pmod 4$.
2. **Legendre Eigenstate Kickback**:
   The Legendre Fourier state $\lvert \Gamma_p\rangle \propto \sum_{y=1}^{p-1} \left(\frac{y}{p}\right)\lvert y\rangle$ satisfies $\sum_{y=1}^{p-1} \left(\frac{y}{p}\right) e^{2\pi i z y / p} = \left(\frac{z}{p}\right)\varepsilon_p \sqrt{p}$, yielding unit-modulus binary sign kickback $\left(\frac{z}{p}\right) \in \{-1, +1\}$ across all non-zero residues.
