# Conditional Classical Latent-Error Coincidence Identities

CORRECTED 2026-10-16 / EXTERNAL REVIEW PENDING. The identities below condition
CLASSICAL hidden-error variables on equality and retain one original error.
No phase-qubit equality instrument is supplied. This is NOT a physical CNOT
merge, quantum purification construction or universal decoder/SNR comparison.
See DCP_LATENT_ERROR_ACCESS_REVIEW.md for the exact access obstruction and
the distinction between retained error e and a CNOT sum error2e.

## 1. Motivation and Scope

The earlier CNOT noise audit motivates a CONDITIONAL CLASSICAL calculation:
assume an external observer can compare latent error variables exactly and
retain one leaf when they coincide. The phase-qubit source does not supply
that access. An actual CNOT branch adds or subtracts errors; it does not
herald their equality or implement the retained-error posterior below.

The useful content is the classical posterior identity, its telescoping
probability and the proxy bound SNR<=survival<=1. Numerical direct-leaf
comparisons are diagnostics, not a universal dominance theorem or quantum
resource bound. At p0 and p1 the visibility gain is neutral as well.

## 2. Theorem 1 — Single-Step Coincidence-Pruned Distribution and the $p^* = 2/3$ Crossover

Let $K_\eta$ be the symmetric nearest-neighbor modular noise kernel on $\mathbb{Z}_q$ ($q \ge 3$):
$$
K_\eta(0) \;=\; 1 - p, \qquad K_\eta(+1) \;=\; K_\eta(-1) \;=\; \frac{p}{2}, \qquad p \in [0, 1],
$$
with baseline fundamental Fourier visibility $\lambda_1(p) = (1 - p) + p\cos(2\pi/q)$.

**Theorem 1 (Single-Step Coincidence Renormalization and $p^* = 2/3$ Purification Threshold).**
1. Post-selecting two independent copies $e_1, e_2 \stackrel{\text{i.i.d.}}{\sim} K_\eta$ on exact coincidence $e_1 = e_2$ succeeds with probability
   $$
   P_{\text{acc}}^{(1)}(p) \;=\; \sum_{e \in \mathbb{Z}_q} K_\eta(e)^2 \;=\; (1 - p)^2 + \frac{p^2}{2} \;=\; 1 - 2p + \frac{3}{2}p^2,
   $$
   and produces the renormalized error distribution $K^{(1)}(e) = K_\eta(e)^2 / P_{\text{acc}}^{(1)}(p)$ with fundamental Fourier visibility
   $$
   \lambda_1^{(1)}(p) \;=\; \frac{(1 - p)^2 + \frac{p^2}{2}\cos(2\pi / q)}{(1 - p)^2 + \frac{p^2}{2}}.
   $$
2. The single-step visibility gain satisfies
   $$
   \lambda_1^{(1)}(p) - \lambda_1(p) \;=\; \frac{p(1 - p)(2 - 3p)\bigl(1 - \cos(2\pi / q)\bigr)}{2\bigl((1 - p)^2 + p^2 / 2\bigr)}.
   $$
   Consequently:
   - For $0 < p < 2/3$, $\lambda_1^{(1)}(p) > \lambda_1(p)$ (coincidence pruning strictly purifies the phase error).
   - At $p^* = 2/3$, $K_\eta(0) = K_\eta(\pm 1) = 1/3$ is flat on $\{-1, 0, +1\}$, so $K^{(1)} = K_\eta$ and $\lambda_1^{(1)}(2/3) = \lambda_1(2/3)$.
   - For $2/3 < p < 1$, $\lambda_1^{(1)}(p) < \lambda_1(p)$ (coincidence pruning amplifies the $\pm 1$ side-lobes and degrades visibility).

## 3. Theorem 2 — Exact Telescoping $2^L$-Moment Identity for Depth-$L$ Tree Survival

At classical conditioning layer $\ell$, independent latent errors with
posterior $K^{(\ell-1)}$ are compared and one ORIGINAL error is retained.
Conditional coincidence probability is the squared-weight sum, updating the
retained-error posterior to $K^{(\ell)}(e)=K^{(\ell-1)}(e)^2/P_{acc}^{(\ell)}$.
These are not quantum merge nodes or a derived error channel on phase qubits.

**Theorem 2 (Exact Telescoping $2^L$-Moment Survival Law).**
For any probability distribution $K_\eta$ on $\mathbb{Z}_q$ and any tree depth $L \ge 1$:
1. The surviving root error distribution at depth $L$ is
   $$
   K^{(L)}(e) \;=\; \frac{K_\eta(e)^{2^L}}{\sum_{z \in \mathbb{Z}_q} K_\eta(z)^{2^L}},
   $$
   with conditional root visibility $\lambda_1^{(L)} = \frac{\sum_{e} K_\eta(e)^{2^L}\cos(2\pi e/q)}{\sum_{e} K_\eta(e)^{2^L}}$.
2. The joint probability that all $2^L - 1$ internal binary coincidence checks across layers $\ell = 1, \dots, L$ simultaneously succeed telescopes exactly to the $2^L$-th moment norm of $K_\eta$:
   $$
   P_{\text{surv}}^{(L)}(K_\eta) \;:=\; \prod_{\ell=1}^{L} \bigl(P_{\text{acc}}^{(\ell)}\bigr)^{2^{L-\ell}} \;=\; \sum_{e \in \mathbb{Z}_q} K_\eta(e)^{2^L}.
   $$

*Proof.*
Let $S_{2^\ell} := \sum_{e \in \mathbb{Z}_q} K_\eta(e)^{2^\ell}$ with $S_1 = 1$. By induction on $\ell$, $K^{(\ell-1)}(e) = K_\eta(e)^{2^{\ell-1}} / S_{2^{\ell-1}}$, so $P_{\text{acc}}^{(\ell)} = S_{2^\ell} / S_{2^{\ell-1}}^2$. Taking the product over $\ell = 1, \dots, L$ gives
$$
\prod_{\ell=1}^{L} \left(\frac{S_{2^\ell}}{S_{2^{\ell-1}}^2}\right)^{2^{L-\ell}}
\;=\; \prod_{\ell=1}^{L} \frac{S_{2^\ell}^{2^{L-\ell}}}{S_{2^{\ell-1}}^{2^{L-\ell+1}}}
\;=\; \frac{S_{2^L}^{2^0}}{S_1^{2^L}} \;=\; S_{2^L} \;=\; \sum_{e \in \mathbb{Z}_q} K_\eta(e)^{2^L}. \quad \square
$$

## 4. Theorem 3 — Conditional Classical Proxy Upper Bound Only

Define the **throughput-adjusted root SNR** per initial $2^L$-leaf batch as
$$
\mathrm{SNR}_{\text{pruned-tree}}(L; K_\eta) \;:=\; P_{\text{surv}}^{(L)}(K_\eta) \cdot \bigl(\lambda_1^{(L)}\bigr)^2
\;=\; \frac{\bigl(\sum_{e \in \mathbb{Z}_q} K_\eta(e)^{2^L}\cos(2\pi e/q)\bigr)^2}{\sum_{e \in \mathbb{Z}_q} K_\eta(e)^{2^L}},
$$
and compare against direct single-leaf Fourier readout of the same $K = 2^L$ leaves, $\mathrm{SNR}_{\text{leaf}}(2^L; K_\eta) = 2^L\,\lambda_1(K_\eta)^2$.

**Theorem 3 (Throughput-Adjusted SNR Upper Bound).**
For every probability distribution $K_\eta$ on $\mathbb{Z}_q$ and every depth $L \ge 1$,
$$
\mathrm{SNR}_{\text{pruned-tree}}(L; K_\eta) \;\le\; P_{\text{surv}}^{(L)}(K_\eta) \;=\; \sum_{e \in \mathbb{Z}_q} K_\eta(e)^{2^L} \;\le\; 1,
$$
For a nonzero fixed baseline visibility, the direct-leaf PROXY scales as
2^L times its squared visibility. This does not establish a universal strict
dominance theorem. At q3,p2/3 the kernel is uniform, both visibilities and
both proxies are EXACTLY zero at every depth, and their ratio is undefined.
The code records an exact tie with a null ratio, not floating strictness.
The saved nonzero comparisons remain finite numeric diagnostics only.

Even if extra orthogonal error labels were physically supplied, conditioning
on coincidence then performing all CNOT sum branches would produce error
2^L*e moduloq, not e; branch probabilities and the stronger-access classical
baseline would also have to be charged. None of these identities is a
substitute for that source/channel construction.
