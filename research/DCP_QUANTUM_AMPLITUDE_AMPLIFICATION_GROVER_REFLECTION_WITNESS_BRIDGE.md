# DCP Coherent Grover-BHMT Quantum Amplitude Amplification of CNOT Syndrome Branches Bridge (Subsystem 117)

## Scope & Overview
This subsystem establishes the exact $k$-step Brassard-Høyer-Mosca-Tapp (BHMT) coherent amplitude amplification law on CNOT witness compression trees prior to syndrome measurement, and proves that a weight-$3$ witness ($p_0 = 2^{-(3-1)} = 1/4$) achieves $100\%$ deterministic syndrome preparation ($P_1 = 1.0$) in a single reflection step while preserving $100\%$ conditional survivor phase fidelity.

## Exact Mathematical Laws
1. **Chebyshev-Trigonometric Amplification & Survivor Phase Invariance**:
   Applying $k$ steps of $Q = -U_{\mathrm{prep}} S_0 U_{\mathrm{prep}}^\dagger S_\chi$ with syndrome-only oracle $S_\chi = I_{\mathrm{surv}} \otimes (I - 2\lvert y^*\rangle\langle y^*\rvert)$ rotates the syndrome probability to $P_k(p_0) = \sin^2((2k+1)\arcsin\sqrt{p_0})$ with survivor fidelity $F_{\mathrm{surv}} = 1.0$.
2. **1-Step Deterministic Preparation at Weight $w = 3$ ($p_0 = 1/4$)**:
   At $p_0 = 1/4$ ($\theta_0 = \pi/6$), $k = 1$ step rotates $3\theta_0 = \pi/2$, boosting acceptance from $0.25$ to $1.00$ ($4.0\times$ boost), whereas at $w = 2$ ($p_0 = 1/2, \theta_0 = \pi/4$), standard $\pi$-reflection over-rotates to $\sin^2(3\pi/4) = 0.50$.
