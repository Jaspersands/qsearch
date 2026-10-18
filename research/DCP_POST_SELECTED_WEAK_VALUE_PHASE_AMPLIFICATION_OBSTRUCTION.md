# DCP Post-Selected Weak-Value Phase Amplification Obstruction (Subsystem 96)

## Scope & Overview
This subsystem resolves whether post-selecting a weakly coupled pointer onto a nearly orthogonal state at angle $\epsilon \ll 1$ ("weak-value phase amplification") can reduce total quantum sample complexity for DCP phase estimation.

## Exact Mathematical Laws
1. **Conditional Contrast Amplification vs. Acceptance Probability**:
   While conditioning on the rare post-selected port amplifies the conditional expectation contrast by $O(1/\epsilon)$, the acceptance probability drops as $P_{\mathrm{acc}}(\theta; \epsilon) = \frac{1}{2}(1 - \gamma \cos(2\epsilon)\cos\theta) = O(\epsilon^2 + \theta^2)$.
2. **Exact Fisher Information Chain-Rule Conservation**:
   By the exact additive decomposition $I_{\mathrm{total}}(\theta; \epsilon) = P_{\mathrm{acc}} I_{\mathrm{cond}}(\theta \mid \mathrm{Accept}) + I_{\mathrm{binary}}(\mathrm{Accept}/\mathrm{Reject}) \le I_Q = \gamma^2$, the per-prepared-copy post-selected Fisher information $P_{\mathrm{acc}} I_{\mathrm{cond}}$ never exceeds the complete non-post-selected quantum Fisher information bound $\gamma^2$.
