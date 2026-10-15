# DCP Noisy Tree-Merge Error-Propagation Audit: $2^L$-Fold Phase-Error Convolution, Double-Exponential Visibility Decay, and Classical-vs-Tree SNR Crossover

## 1. Motivation and Scope

In `theorems/dcp_noisy_fourier_likelihood_decoder_audit.py` (Subsystem 8), single-copy noisy DCP states with symmetric modular phase noise $e \sim K_\eta$ on $\mathbb{Z}_q$ were shown to have fundamental Fourier visibility damped by $\lambda_1 = \sum_{e \in \mathbb{Z}_q} K_\eta(e)\cos(2\pi e/q) \in (0, 1]$. Separately, in `theorems/dcp_truncated_qft_tree_merge_joint_channel_audit.py` (Subsystem 16), depth-$L$ binary CNOT tree-merge circuits combining $K = 2^L$ leaves were analyzed under truncated-QFT leaf preparation.

A natural question is whether binary CNOT tree-merge circuits can coherently purify or suppress independent additive modular phase errors $e_1, \dots, e_{2^L} \stackrel{\text{i.i.d.}}{\sim} K_\eta$ across $K = 2^L$ leaves, or whether post-selected CNOT tree-merging compounds the leaf phase errors by $2^L$-fold convolution. This note proves three exact theorems resolving noisy tree-merge error propagation.

## 2. Theorem 1 — Exact $2^L$-Fold Convolution of Leaf Phase Errors under Tree-Merge Post-Selection

Consider $K = 2^L$ independent noisy DCP leaf states on $\mathbb{Z}_q$, where leaf $j \in \{1, \dots, 2^L\}$ carries a random phase error $e_j \sim K_\eta$ on its relative phase factor $\omega_q^{(s + e_j) d_j}$, with symmetric noise kernel $K_\eta(-e) = K_\eta(e)$ and Fourier coefficients
$$
\lambda_m \;:=\; \sum_{e \in \mathbb{Z}_q} K_\eta(e)\cos\!\left(\frac{2\pi m e}{q}\right), \qquad m \in \mathbb{Z}_q.
$$

**Theorem 1 (Exact $2^L$-Fold Convolution and Harmonic Power Law).**
Under a depth-$L$ binary CNOT tree-merge that aligns leaf differences $d_1 = d_2 = \dots = d_{2^L} = d$, the post-selected root state accumulates the sum of all $2^L$ leaf phases, inducing the $2^L$-fold cyclic convolution error distribution
$$
E^{(L)} \;:=\; \sum_{j=1}^{2^L} e_j \bmod q \;\sim\; K_\eta^{* 2^L}
$$
on $\mathbb{Z}_q$. By the discrete Fourier convolution theorem on $\mathbb{Z}_q$, the $m$-th harmonic visibility of the depth-$L$ root state is given exactly by
$$
\Lambda_m^{(L)} \;:=\; \sum_{E \in \mathbb{Z}_q} K_\eta^{* 2^L}(E)\cos\!\left(\frac{2\pi m E}{q}\right) \;=\; \bigl(\lambda_m\bigr)^{2^L}.
$$

## 3. Theorem 2 — Double-Exponential Root Visibility Decay in Tree Depth $L$

**Theorem 2 (Double-Exponential Visibility Decay and Noise Threshold Scaling).**
1. For any non-trivial symmetric noise kernel with $\lambda_1 \in (0, 1)$, the fundamental Fourier visibility at the root of a depth-$L$ binary tree-merge decays **double-exponentially** in $L$:
   $$
   \Lambda_1^{(L)} \;=\; \lambda_1^{2^L} \;=\; \exp\!\bigl(-2^L \ln(1/\lambda_1)\bigr).
   $$
2. To preserve root visibility $\Lambda_1^{(L)} \ge \tau \in (0, 1)$ at tree depth $L$, the single-leaf damping factor must satisfy
   $$
   \lambda_1 \;\ge\; \tau^{2^{-L}}, \qquad 1 - \lambda_1 \;\le\; 1 - \tau^{2^{-L}} \;=\; O\!\bigl(2^{-L}\ln(1/\tau)\bigr).
   $$

## 4. Theorem 3 — Exact Fisher-Information Crossover: Classical Single-Leaf Readout Dominates Uncorrected Tree-Merge

**Theorem 3 (Classical $K$-Copy Aggregation vs Coherent Depth-$L$ Tree-Merge).**
Given $K = 2^L$ noisy DCP leaf copies with fundamental visibility $\lambda_1 \in (0, 1)$:
1. **Single-Leaf Classical Readout ($K$ measurements at depth $0$)**: Measuring each of the $K = 2^L$ leaves directly in the Fourier basis yields $K$ independent samples with fundamental harmonic amplitude $\lambda_1$, achieving cumulative first-harmonic SNR proxy
   $$
   \mathrm{SNR}_{\text{leaf}}(K, \lambda_1) \;=\; K\,\lambda_1^2 \;=\; 2^L \lambda_1^2.
   $$
2. **Coherent Depth-$L$ Tree-Merge Readout**: Merging $K = 2^L$ leaves into a single root state yields root harmonic amplitude $\Lambda_1^{(L)} = \lambda_1^{2^L}$ and root SNR proxy (per surviving root state, before even paying post-selection success probability)
   $$
   \mathrm{SNR}_{\text{root}}(L, \lambda_1) \;=\; \bigl(\Lambda_1^{(L)}\bigr)^2 \;=\; \lambda_1^{2^{L+1}}.
   $$
3. For every $L \ge 1$ ($K = 2^L \ge 2$) and every $\lambda_1 \in (0, 1]$,
   $$
   \frac{\mathrm{SNR}_{\text{root}}(L, \lambda_1)}{\mathrm{SNR}_{\text{leaf}}(2^L, \lambda_1)} \;=\; 2^{-L}\,\lambda_1^{2(2^L - 1)} \;\le\; 2^{-L} \;<\; 1,
   $$
   with strict inequality for all $L \ge 1$. Thus uncorrected CNOT tree-merging strictly degrades harmonic SNR relative to direct single-leaf Fourier readout across the entire noisy regime $\lambda_1 \in (0, 1]$.
