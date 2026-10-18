# DCP Twisted-Convolution Pretty Good Measurement (PGM) and Collision-Fiber Gram Spectrum Bridge

## 1. Exact Results
1. **Collision-Fiber Block Diagonalization**:
   For $|\psi(s)\rangle = 2^{-m/2} \sum_{u \in \{0,1\}^m} \omega_q^{\langle A u, s \rangle} |u\rangle$, the uniform ensemble operator $\mathcal{E} = \frac{1}{Q} \sum_{s \in \mathbb{Z}_q^n} |\psi(s)\rangle\langle\psi(s)|$ has matrix entries $\langle u | \mathcal{E} | u' \rangle = 2^{-m} \mathbf{1}[A u \equiv A u' \pmod q]$ and non-zero eigenvalues $\lambda_y(\mathcal{E}) = c(y)/2^m$.
2. **Exact PGM Success Identity**:
   $$P_{\mathrm{PGM}}(A) = \frac{1}{Q \cdot 2^m} \left(\sum_{y \in \mathbb{Z}_q^n} \sqrt{c(y)}\right)^2 \le \frac{|\mathrm{Im}(A \bmod q)|}{Q}.$$
3. **Scoped Controls**:
   - Bijective constructive control $A = [[1, 2]] \bmod 4$: $c(y) = 1$ for all $y \in \mathbb{Z}_4$, achieving $P_{\mathrm{PGM}} = 1.0$.
   - Collision control $A = [[2, 2]] \bmod 4$: $c(0)=c(2)=2$, giving $P_{\mathrm{PGM}} = 0.5$.
