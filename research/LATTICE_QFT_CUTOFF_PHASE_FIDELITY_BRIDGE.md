# Lattice QFT Cutoff Phase-Fidelity Bridge: Exact Banded Dyadic Kernel, Universal Label Uniformity, and Joint-Channel Receiver Visibility

## 1. Motivation and Scope

In `theorems/lattice_cube_dcp_readout.py`, `OpaquePhaseBackend` rejects approximate-QFT batches (`plan.exact == False`) with the guard:
```text
APPROXIMATE_SOURCE_NOT_AN_EXACT_DCP_PROMISE; joint-channel receiver contract required
```
Meanwhile, `theorems/lattice_qft_precision.py` bounds the worst-case operator norm $\|F_{2^\ell}^{(b)} - F_{2^\ell}\|_2$ of the separation-cutoff-$b$ approximate QFT synthesized by `synth_qft_full(ell, do_swaps=True, approximation_degree=ell - 1 - b)`.

To connect the approximate QFT compiler (`theorems/lattice_qft_precision.py`) to the lattice cube-coset readout (`theorems/lattice_cube_dcp_readout.py`) and the $\{X, Y\}$ quadrature receiver (`theorems/dcp_noisy_fourier_likelihood_decoder_audit.py`), we need the exact joint-channel law of the colour-and-label readout at any cutoff $b \in \{0, \dots, \ell - 1\}$.

This note proves three exact theorems characterizing the matrix entries of $F_{2^\ell}^{(b)}$, universal label uniformity across all cutoffs $b \ge 0$, and the exact effective quadrature visibility $v_{\text{eff}}^{(b)}$ of the joint approximate-QFT channel.

## 2. Theorem 1 — Exact Banded Dyadic Phase Kernel of the Cutoff-$b$ QFT

For $\ell \ge 1$ wires ($N = 2^\ell$), write basis indices in binary as $x = \sum_{j=0}^{\ell-1} x_j 2^j$ and $k = \sum_{m=0}^{\ell-1} k_m 2^m$ with $x_j, k_m \in \{0, 1\}$.

**Theorem 1 (Exact Matrix Entries of $F_{2^\ell}^{(b)}$).**
For every separation cutoff $b \in \{0, \dots, \ell - 1\}$, the ideal cutoff-$b$ QFT unitary $F_{2^\ell}^{(b)}$ (retaining Hadamards and controlled-phase rotations $\operatorname{CP}(\pi / 2^d)$ with wire separation $1 \le d \le b$, followed by bit-reversal swaps) has exact matrix entries
$$
\langle k | F_{2^\ell}^{(b)} | x \rangle
\;=\; \frac{1}{\sqrt{2^\ell}} \exp\!\left(2\pi i\, \Theta_\ell^{(b)}(k, x)\right),
$$
where the banded dyadic phase functional $\Theta_\ell^{(b)} : \{0, \dots, 2^\ell-1\}^2 \to 2^{-b-1}\mathbb{Z}$ is
$$
\Theta_\ell^{(b)}(k, x)
\;:=\; \sum_{\substack{0 \le m, j < \ell \\ \ell - 1 - b \le m + j \le \ell - 1}} k_m x_j\, 2^{m + j - \ell}.
$$
In particular, every matrix entry of $F_{2^\ell}^{(b)}$ has exact modulus $|\langle k | F_{2^\ell}^{(b)} | x \rangle| = 2^{-\ell/2}$.

*Proof.*
In the exact QFT $F_{2^\ell}$, $\frac{k x}{2^\ell} \equiv \sum_{m + j \le \ell - 1} k_m x_j 2^{m + j - \ell} \pmod 1$ because terms with $m + j \ge \ell$ are integers. Prior to the final bit-reversal swaps on wire $j$ and wire $m' = \ell - 1 - m$, the pair $(m, j)$ with $m + j = \ell - 1 - d$ corresponds to wire separation $d = |m' - j| = \ell - 1 - (m + j)$ and phase angle $2\pi \cdot 2^{-(d+1)} = \pi / 2^d$. Truncating all controlled-phase gates with $d > b$ omits precisely the terms with $m + j < \ell - 1 - b$, leaving $\Theta_\ell^{(b)}(k, x)$ while preserving the product of unit-modulus phases on every computational basis trajectory. $\square$

## 3. Theorem 2 — Universal Label Uniformity and Pure Two-Point Conditional States

**Theorem 2 (Cutoff-Invariant Uniform Labels and Conditional Purity).**
Let $\mathcal{S}$ be any `CubeCosetSource` satisfying the two-point cube promise on $\{0, 1\} \times \{0, \dots, M_{\text{box}}-1\}^n$ with $\ell = n \log_2(2 M_{\text{box}})$ position wires and bad-register rate $p_{\text{bad}}$. Under readout with the cutoff-$b$ QFT $F_{2^\ell}^{(b)}$ for **any** $b \in \{0, \dots, \ell - 1\}$:
1. **Singleton cells**: For any singleton cell $c = \{(t, a)\}$ with encoded position $x = \operatorname{encode\_position}(a, M_{\text{box}})$, every label $k \in \mathbb{Z}_{2^\ell}$ occurs with exact conditional probability $2^{-\ell}$ and post-measurement colour state $|t\rangle\langle t|$.
2. **Two-point cells**: For any two-point cell $c = \{(0, a^{(0)}), (1, a^{(1)})\}$ with encoded positions $(x_0, x_1)$, every label $k \in \mathbb{Z}_{2^\ell}$ occurs with exact conditional probability $\frac{1}{2}(2^{-\ell} + 2^{-\ell}) = 2^{-\ell}$, and the post-measurement colour state is the pure phase state
   $$
   |\psi_{\ell, k}^{(b)}(x_0, x_1)\rangle
   \;=\; \frac{1}{\sqrt{2}}\Bigl(|0\rangle + e^{2\pi i \bigl(\Theta_\ell^{(b)}(k, x_1) - \Theta_\ell^{(b)}(k, x_0)\bigr)}|1\rangle\Bigr)
   $$
   up to global phase $e^{2\pi i \Theta_\ell^{(b)}(k, x_0)}$.
3. **Global label uniformity**: Consequently, the marginal label distribution $\Pr[k] = 2^{-\ell}$ is **strictly uniform** on $\mathbb{Z}_{2^\ell}$ for every cutoff $b \in \{0, \dots, \ell - 1\}$.

## 4. Theorem 3 — Joint-Channel Quadrature Visibility and Pointwise Phase-Defect Bound

For any two-point cell with positions $(x_0, x_1)$ and shift $s = (x_1 - x_0) \bmod 2^\ell$, define the pointwise phase defect at label $k \in \mathbb{Z}_{2^\ell}$:
$$
\delta\theta_\ell^{(b)}(k; x_0, x_1)
\;:=\; 2\pi \left(\Theta_\ell^{(b)}(k, x_1) - \Theta_\ell^{(b)}(k, x_0) - \frac{k(x_1 - x_0)}{2^\ell}\right).
$$

**Theorem 3 (Exact Joint-Channel Quadrature Visibility and Cosine Lower Bound).**
1. **Pointwise phase-defect bound**: Since $k_m \in \{0, 1\}$ and $x_{1,j} - x_{0,j} \in \{-1, 0, +1\}$, every omitted pair $(m, j)$ with $m + j = \ell - 1 - d$ ($b + 1 \le d \le \ell - 1$) contributes at most $2\pi \cdot 2^{-d-1} = \pi 2^{-d}$ in magnitude, yielding
   $$
   \bigl|\delta\theta_\ell^{(b)}(k; x_0, x_1)\bigr|
   \;\le\; \pi \sum_{d=b+1}^{\ell-1} (\ell - d)\,2^{-d}
   \;=\; \pi \left(\frac{\ell - b - 2}{2^b} + \frac{1}{2^{\ell-1}}\right)
   \;=:\; \Delta_{\max}(\ell, b).
   $$
2. **Exact joint-channel quadrature correlation**: Under balanced $\{X, Y\}$ quadrature measurement scored against the ideal shift $s = (x_1 - x_0) \bmod 2^\ell$, the exact expected correlation is
   $$
   \mathbb{E}\bigl[S^{(b)}(s)\bigr] \;=\; \frac{v_{\text{eff}}^{(b)}}{2},
   \qquad
   v_{\text{eff}}^{(b)} \;=\; (1 - p_{\text{bad}})\,\frac{1}{|G| 2^\ell}\sum_{(x_0, x_1) \in G}\sum_{k=0}^{2^\ell - 1} \cos\bigl(\delta\theta_\ell^{(b)}(k; x_0, x_1)\bigr),
   $$
   and whenever $\Delta_{\max}(\ell, b) \le \pi$,
   $$
   v_{\text{eff}}^{(b)} \;\ge\; (1 - p_{\text{bad}})\,\cos\bigl(\Delta_{\max}(\ell, b)\bigr)
   \;\ge\; (1 - p_{\text{bad}})\left(1 - \frac{1}{2}\Delta_{\max}(\ell, b)^2\right).
   $$
