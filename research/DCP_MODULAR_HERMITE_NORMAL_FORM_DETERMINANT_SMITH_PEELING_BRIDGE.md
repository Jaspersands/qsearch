# DCP Modular Smith Normal Form (SNF) Invariant-Factor Decoupling Bridge (Subsystem 138)

## Scope & Overview
This subsystem establishes that for any $n \times n$ compressed DCP column matrix $B \in \mathbb{Z}_q^{n \times n}$ with Smith Normal Form $U B V \equiv \mathrm{diag}(d_1, \dots, d_n) \pmod q$, the unimodular transformations $V$ and $U^{-\top}$ decouple the coupled phase register into $n$ independent cyclic channels of orders $q_i = q / \gcd(d_i, q)$.

## Exact Mathematical Laws
1. **Invariant-Factor Channel Factorization & Coset Capacity**:
   The map $s \mapsto B^\top s \bmod q$ has image cardinality $\prod_{i=1}^n \frac{q}{\gcd(d_i, q)}$ and kernel fiber cardinality $\prod_{i=1}^n \gcd(d_i, q)$ ($32$ cosets of size $2$ for $d = [1, 2] \bmod 8$; $12$ cosets of size $12$ for $d = [2, 6] \bmod 12$).
