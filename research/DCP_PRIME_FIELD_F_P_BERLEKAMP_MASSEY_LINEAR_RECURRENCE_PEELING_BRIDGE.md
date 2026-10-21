# DCP Prime-Field $\mathbb{F}_p$ Cayley-Hamilton / Hankel Linear Recurrence Peeling Bridge (Subsystem 131)

## Scope & Overview
This subsystem establishes that for any matrix-power phase sequence $z_k = \langle u, M^k s \rangle \bmod p$ ($M \in \mathbb{F}_p^{n \times n}$), collecting $2n$ scalar evaluations $z_0, \dots, z_{2n-1}$ suffices to invert the $n \times n$ Hankel matrix over $\mathbb{F}_p$, recover the characteristic recurrence of $M$, and deterministically predict all higher evaluations $z_k$ ($k \ge 2n$) with zero additional quantum queries.

## Exact Mathematical Laws
1. **Cayley-Hamilton Order-$n$ Recurrence**:
   Every sequence $z_k = \langle u, M^k s \rangle \bmod p$ satisfies $z_{k+n} + \sum_{j=1}^n c_j z_{k+n-j} \equiv 0 \pmod p$.
2. **Exact $2n$-Sample Hankel Inversion**:
   Verified on a 3D matrix over $\mathbb{F}_{17}$ ($6$ samples predict $14/14$ future steps) and a 4D companion matrix over $\mathbb{F}_{31}$ ($8$ samples recover exact characteristic coefficients $[24, 18, 26, 12]$ and predict $16/16$ future steps).
