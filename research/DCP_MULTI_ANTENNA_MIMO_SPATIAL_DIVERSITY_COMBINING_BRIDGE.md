# DCP Multi-Antenna MIMO Spatial Diversity LLR Combining Bridge (Subsystem 110)

## Scope & Overview
This subsystem establishes the exact Bayes-optimal Log-Likelihood-Ratio (LLR) combining weights $w_l^* = 2\operatorname{atanh}(\gamma_l)$ across $L$ heterogeneous CNOT survivor branches and proves its strict superiority over unweighted majority voting.

## Exact Mathematical Laws
1. **Exact Maximal-Ratio LLR Combining**:
   Observing outcomes $y \in \{-1, +1\}^L$ across branches with visibilities $\gamma_1, \dots, \gamma_L$ yields posterior $\mathrm{LLR}(y) = \sum_{l=1}^L 2\operatorname{atanh}(\gamma_l) y_l$.
2. **Majority Voting Reversal vs. LLR Dominance**:
   On $\gamma = [0.90, 0.25, 0.25]$, unweighted majority voting degrades error from $0.05$ to $0.161875$ ($>3.23\times$ worse), whereas on $\gamma = [0.80, 0.65, 0.60, 0.55]$, LLR combining ($0.06281$) strictly beats both single-best selection ($0.10$) and unweighted majority ($0.07853$).
