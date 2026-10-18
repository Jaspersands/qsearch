# DCP Noisy Syndrome Measurement Readout Bit-Flip Bridge (Subsystem 88)

## Scope & Overview
This subsystem quantifies the exact impact of classical syndrome measurement readout bit-flip errors $\eta \in [0, 1/2]$ on CNOT witness compression and Pauli-$X$ sign-flip frame routing (Subsystems 51, 65, 77, 78), and establishes the exact $O(\eta^2)$ error suppression of 1-ancilla parity-check verification.

## Exact Mathematical Laws
1. **Single-Pair and Two-Pair Readout Damping**:
   A classical readout bit-flip error rate $\eta$ on a syndrome wire $d_m$ inverts the conditional Pauli-$X^{d_{m,\mathrm{obs}}}$ sign-rectification frame with probability $\eta$, damping single-pair phase coherence by $(1 - 2\eta)\gamma$ and two-pair Stage-2 parity visibility by $(1 - 2\eta)^2 \gamma^2$.
2. **Exact $O(\eta^2)$ Suppression via 1-Ancilla Parity-Check Verification**:
   Copying a syndrome bit to a verification ancilla $d_m' = d_m$ prior to readout and post-selecting on readout agreement ($d_{m,\mathrm{obs}} = d_{m,\mathrm{obs}}'$) succeeds with probability $(1-\eta)^2 + \eta^2$ and reduces the effective syndrome error rate to:
   $$\eta_{\mathrm{post}}(\eta) = \frac{\eta^2}{(1-\eta)^2 + \eta^2},$$
   achieving an $18.1\times$ error reduction at $\eta = 0.05$ ($\eta_{\mathrm{post}} = 0.002762$).
