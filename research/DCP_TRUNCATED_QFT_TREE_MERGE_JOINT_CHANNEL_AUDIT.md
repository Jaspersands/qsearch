# DCP Truncated-QFT Tree-Merge Joint-Channel Audit: Additive Phase-Defect Propagation, Branch-Symmetry Sine Cancellation, and Exact Visibility Factorization

## 1. Motivation and Scope

In `theorems/lattice_cube_dcp_readout.py`, `OpaquePhaseBackend` enforces the guard:
```text
APPROXIMATE_SOURCE_NOT_AN_EXACT_DCP_PROMISE; joint-channel receiver contract required
```
whenever a source batch is compiled with a separation-cutoff-$b$ approximate QFT ($b < \ell - 1$). In `theorems/lattice_qft_cutoff_phase_fidelity_bridge.py` (Subsystem 10), we proved the single-copy ($d = 0$) joint-channel law of the cutoff-$b$ QFT $F_{2^\ell}^{(b)}$, showing that every two-point cell $(x_0, x_1)$ and label $k \in \mathbb{Z}_{2^\ell}$ produces a pure phase state with pointwise phase defect
$$
\delta\theta_\ell^{(b)}(k; x_0, x_1)
\;=\; 2\pi\left(\Theta_\ell^{(b)}(k, x_1) - \Theta_\ell^{(b)}(k, x_0) - \frac{k(x_1 - x_0)}{2^\ell}\right) \pmod{2\pi},
$$
and single-copy quadrature visibility
$$
v_{\text{eff}, 0}^{(b)}
\;=\; (1 - p_{\text{bad}})\,\mathbb{E}_{(x_0, x_1) \in G,\, k \sim \mathbb{Z}_{2^\ell}}\Bigl[\cos\bigl(\delta\theta_\ell^{(b)}(k; x_0, x_1)\bigr)\Bigr].
$$

What happens when independent copies emitted under the approximate QFT $F_{2^\ell}^{(b)}$ are combined through a depth-$d$ binary tree of CNOT merges (`OpaquePhaseBackend.merge`)? One might worry that correlated or non-Gaussian phase defects $\delta\theta_\ell^{(b)}$ prevent a closed-form multi-level visibility law.

This note proves three exact theorems resolving the multi-level joint channel:
1. **Additive Phase-Defect Propagation**: Under CNOT merge on branch $b_{\text{br}} \in \{0, 1\}$, the post-merge phase defect relative to the wrapped label $k_{\text{out}} = (k_1 + (-1)^{b_{\text{br}}} k_2) \bmod 2^\ell$ is **exactly** $\delta\theta_1 + (-1)^{b_{\text{br}}}\delta\theta_2 \pmod{2\pi}$.
2. **Branch-Symmetry Sine Cancellation**: Because both CNOT branches $b_{\text{br}} \in \{0, 1\}$ occur with exact probability $1/2$ and carry opposite signs $\pm \delta\theta_2$, averaging $\cos(\delta\theta_1 + (-1)^{b_{\text{br}}}\delta\theta_2)$ over $b_{\text{br}} \in \{0, 1\}$ cancels $\sin(\delta\theta_1)\sin(\delta\theta_2)$ **pointwise**, yielding $\cos(\delta\theta_1)\cos(\delta\theta_2)$.
3. **Exact Depth-$d$ Joint Visibility Factorization**: Consequently, for every tree depth $d \ge 0$ and every QFT cutoff $b \in \{0, \dots, \ell - 1\}$, the exact branch-averaged quadrature visibility is $v_{\text{eff}, d}^{(b)} = \bigl(v_{\text{eff}, 0}^{(b)}\bigr)^{2^d}$.

## 2. Theorem 1 — Exact Additive Phase-Defect Propagation Under CNOT Merge

**Theorem 1 (Signed Phase-Defect Addition Modulo $2\pi$).**
Let $(c_1, k_1)$ and $(c_2, k_2)$ be two two-point cell outcomes with encoded position pairs $(x_{1,0}, x_{1,1})$ and $(x_{2,0}, x_{2,1})$ sharing the common modular shift $s \equiv x_{1,1} - x_{1,0} \equiv x_{2,1} - x_{2,0} \pmod{2^\ell}$. Under readout with $F_{2^\ell}^{(b)}$ followed by a CNOT merge (`OpaquePhaseBackend.merge`):
1. Both target-$Z$ measurement branches $b_{\text{br}} \in \{0, 1\}$ occur with exact probability $1/2$.
2. On branch $b_{\text{br}} \in \{0, 1\}$, the output label is $k_{\text{out}} = (k_1 + (-1)^{b_{\text{br}}} k_2) \bmod 2^\ell$, and the surviving control qubit is a pure phase state whose phase defect relative to the ideal angle $2\pi k_{\text{out}} s / 2^\ell$ is
   $$
   \delta\theta_{\text{merged}}^{(b)}(b_{\text{br}})
   \;\equiv\; \delta\theta_\ell^{(b)}(k_1; x_{1,0}, x_{1,1}) \;+\; (-1)^{b_{\text{br}}}\,\delta\theta_\ell^{(b)}(k_2; x_{2,0}, x_{2,1}) \pmod{2\pi}.
   $$

*Proof.*
Before the merge, the two parent off-diagonal phases are $\phi_m = 2\pi \frac{k_m s}{2^\ell} + \delta\theta_m \pmod{2\pi}$ for $m \in \{1, 2\}$. Under CNOT merge on branch $b_{\text{br}} \in \{0, 1\}$, the post-merge off-diagonal phase is $\phi_1 + (-1)^{b_{\text{br}}} \phi_2$. Since $k_{\text{out}} \equiv k_1 + (-1)^{b_{\text{br}}} k_2 \pmod{2^\ell}$ and $s \in \mathbb{Z}$, $2\pi \frac{(k_1 + (-1)^{b_{\text{br}}} k_2) s}{2^\ell} \equiv 2\pi \frac{k_{\text{out}} s}{2^\ell} \pmod{2\pi}$, so subtracting $2\pi k_{\text{out}} s / 2^\ell$ leaves $\delta\theta_1 + (-1)^{b_{\text{br}}}\delta\theta_2 \pmod{2\pi}$. $\square$

## 3. Theorem 2 — Pointwise Branch-Symmetry Sine Cancellation and Multiplicative Visibility

**Theorem 2 (Exact Pointwise Cosine Product Across Equiprobable CNOT Branches).**
1. **Pointwise branch average**: For any two parent phase defects $\delta\theta_1, \delta\theta_2 \in \mathbb{R}$, averaging the quadrature cosine factor over the two equiprobable CNOT branches $b_{\text{br}} \in \{0, 1\}$ yields
   $$
   \frac{1}{2}\cos(\delta\theta_1 + \delta\theta_2) \;+\; \frac{1}{2}\cos(\delta\theta_1 - \delta\theta_2)
   \;=\; \cos(\delta\theta_1)\,\cos(\delta\theta_2),
   $$
   because the odd cross terms $\mp \sin(\delta\theta_1)\sin(\delta\theta_2)$ cancel identically.
2. **Exact depth-$d$ joint-channel factorization**: Over a complete binary CNOT merge tree of depth $d \ge 0$ consuming $2^d$ independent source copies emitted under $F_{2^\ell}^{(b)}$, the exact expected $\{X, Y\}$ quadrature correlation at the true shift $s$ is
   $$
   \mathbb{E}\bigl[S_d^{(b)}(s)\bigr] \;=\; \frac{v_{\text{eff}, d}^{(b)}}{2},
   \qquad
   v_{\text{eff}, d}^{(b)} \;=\; \bigl(v_{\text{eff}, 0}^{(b)}\bigr)^{2^d}
   \;=\; \left((1 - p_{\text{bad}})\,\mathbb{E}_{(x_0, x_1) \in G,\, k \sim \mathbb{Z}_{2^\ell}}\Bigl[\cos\bigl(\delta\theta_\ell^{(b)}(k; x_0, x_1)\bigr)\Bigr]\right)^{2^d}.
   $$

## 4. Theorem 3 — Joint Cutoff-and-Depth Precision Budget for Tree-Merge Receivers

**Theorem 3 (Sufficient Cutoff $b$ for Depth-$d$ Tree-Merge Visibility Retention).**
Whenever the single-copy pointwise phase-defect bound $\Delta_{\max}(\ell, b) = \pi\bigl(\frac{\ell - b - 2}{2^b} + \frac{1}{2^{\ell-1}}\bigr)$ satisfies $\Delta_{\max}(\ell, b) \le \pi / 2$, the depth-$d$ joint visibility satisfies
$$
v_{\text{eff}, d}^{(b)}
\;\ge\; (1 - p_{\text{bad}})^{2^d} \bigl(\cos \Delta_{\max}(\ell, b)\bigr)^{2^d}
\;\ge\; (1 - p_{\text{bad}})^{2^d} \left(1 - 2^{d-1}\Delta_{\max}(\ell, b)^2\right).
$$
In particular, choosing $b \ge \lceil \log_2(\pi \ell) \rceil + \lceil d / 2 \rceil$ keeps the cumulative $2^d$-leaf QFT truncation loss $2^{d-1}\Delta_{\max}(\ell, b)^2 = O(1)$ at tree depth $d$.
