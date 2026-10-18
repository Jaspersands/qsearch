# DCP Cyclotomic Galois / Frobenius Automorphism Prime-Power Peeling Bridge (Subsystem 102)

## Scope & Overview
This subsystem establishes the exact Galois group equivariance of CNOT witnesses over $R_q = \mathbb{Z}_q[X]/(X^n + 1)$ ($n = 2^k, q = 2^t$) under $\mathrm{Gal}(\mathbb{Q}(\zeta_{2n})/\mathbb{Q}) \cong (\mathbb{Z}_{2n})^\times = \{\tau_u : X \mapsto X^u, u \text{ odd}\}$ and proves the universal midpoint annihilation and constant-term projection laws under complex conjugation $\tau_{2n-1}: X \mapsto -X^{n-1}$.

## Exact Mathematical Laws
1. **Exact Galois Homomorphism & Mod-2 Permutation Invariance**:
   Each $\tau_u$ acts on coefficient vectors as a signed permutation matrix $P_u \in \mathbb{Z}_q^{n \times n}$ whose mod-2 reduction is a pure coordinate permutation fixing degree $0$.
2. **Universal Midpoint Degree-$(n/2)$ Annihilation Under $\mathrm{id} + \tau_{2n-1}$**:
   Because $(2n - 1)(n/2) = n(n - 1) + n/2$ has an odd wrap count $n - 1$ for every $n = 2^k \ge 2$, $(\tau_{2n-1}(f))_{n/2} \equiv -f_{n/2} \pmod q$, so summing $f + \tau_{2n-1}(f)$ via CNOT identically annihilates degree $n/2$ across all $f \in R_q$ while doubling $f_0 \mapsto 2 f_0 \pmod q$.
