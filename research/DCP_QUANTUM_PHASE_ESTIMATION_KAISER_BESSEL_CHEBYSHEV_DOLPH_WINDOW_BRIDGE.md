# DCP Dolph-Chebyshev Minimax Equiripple QFT Sidelobe Window Bridge (Subsystem 133)

## Scope & Overview
This subsystem establishes the exact Dolph-Chebyshev minimax equiripple optimality law for suppressing worst-case ($L_\infty$) QFT stopband sidelobe spikes during non-dyadic DCP phase estimation on $\{0, 1, \dots, P-1\}$.

## Exact Mathematical Laws
1. **Equiripple Stopband Extrema ($1 / R^2$)**:
   With $x_0 = \cosh(\frac{1}{P-1}\operatorname{acosh}(R)) > 1$, the scaled Chebyshev spectrum $T_{P-1}(x_0 \cos(\pi f)) / R$ oscillates between $-1/R$ and $+1/R$ across all $P - 2$ stopband extrema $|f| \ge f_{\mathrm{stop}} = \frac{1}{\pi}\arccos(1/x_0)$, achieving constant peak stopband power $1 / R^2$.
2. **Strict Minimax Sidelobe Suppression**:
   At $P = 16, R = 30$, the Dolph-Chebyshev window achieves $> 35\times$ lower peak stopband power than the uniform box window and $> 3.5\times$ lower peak stopband power than the Dirichlet-sine window.
