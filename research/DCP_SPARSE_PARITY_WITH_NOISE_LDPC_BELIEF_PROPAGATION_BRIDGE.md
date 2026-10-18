# DCP Sparse Parity-With-Noise LDPC Hyperbolic-Tangent Belief Propagation Bridge (Subsystem 92)

## Scope & Overview
This subsystem establishes the exact hyperbolic-tangent log-likelihood ratio (LLR) algebra and MAP bit-error suppression when CNOT kernel elimination produces an overcomplete star-tree of noisy parity checks $c_l = z_0 \oplus z_l$ on the secret LSB vector $z = s \bmod 2 \in \{0,1\}^n$.

## Exact Mathematical Laws
1. **Exact Tanh-Rule Extrinsic LLR Update**:
   A noisy parity check $c_l = z_0 \oplus z_l$ with measurement bias $\gamma_{\mathrm{check}}$ and partner observation bias $\gamma_{\mathrm{partner}}$ contributes exact extrinsic bias $\gamma_{\mathrm{ext}} = \gamma_{\mathrm{check}} \gamma_{\mathrm{partner}}$ and extrinsic log-likelihood ratio $\mathrm{LLR}_{\mathrm{ext}} = 2 \operatorname{atanh}(\gamma_{\mathrm{check}} \gamma_{\mathrm{partner}})$ to target bit $z_0$.
2. **Exact Bayes Equivalence and Exponential Error Suppression**:
   Across $L$ disjoint auxiliary checks, the additive belief-propagation posterior $\mathrm{LLR}_{\mathrm{post}}(z_0) = y_0 \mathrm{LLR}_0 + \sum_{l=1}^L (y_{p,l} y_{c,l}) \mathrm{LLR}_{\mathrm{ext}}$ matches brute-force $2^L$-state marginal Bayes inference to $< 10^{-12}$ across all $2^{2L+1}$ syndrome outcomes and monotonically reduces the MAP bit-error probability from $0.25$ ($L=0$) to $0.1190$ ($L=4$).
