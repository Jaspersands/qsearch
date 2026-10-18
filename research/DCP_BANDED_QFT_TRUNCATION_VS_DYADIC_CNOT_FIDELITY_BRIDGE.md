# DCP Banded-QFT Truncation Phase-Leakage vs. Exact Dyadic Sublattice Fidelity Bridge

## 1. Bitwise Product Formula for Band-$b$ Peak Survival Probability
For a pure dyadic state $\lvert \psi(K_0)\rangle$ with $K_0 = \sum_{l=0}^{m-1} k_l 2^{m-1-l} \in \mathbb{Z}_{2^m}$, the band-$b$ truncated inverse Fourier transform $\mathrm{QFT}_{2^m}^{(b)\dagger}$ ($1 \le b \le m$) achieves exact peak survival probability:
$$P_{\mathrm{QFT}^{(b)}}(K_0 \mid K_0) = \prod_{j=0}^{m - 1 - b} \cos^2\!\left(\pi \sum_{l = j + b}^{m - 1} k_l 2^{j - 1 - l}\right).$$

## 2. Zero-Leakage Sublattice Criterion ($K_0 \in 2^{m-b}\mathbb{Z}_{2^m}$)
$P_{\mathrm{QFT}^{(b)}}(K_0 \mid K_0) = 1.0$ holds if and only if $K_0 \equiv 0 \pmod{2^{m-b}}$. In particular, $b = 1$ ($H^{\otimes m}$ with zero two-qubit gates) is lossless on the half-period subgroup $\{0, 2^{m-1}\}$ targeted by dyadic CNOT elimination.
