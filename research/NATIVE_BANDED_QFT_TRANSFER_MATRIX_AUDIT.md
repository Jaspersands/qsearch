# Banded Cyclic QFT Two-Call Schedules: Analytical Inner-Digit Elimination and $O(M 3^b)$ Transfer-Matrix Contraction

## 1. Scope and Dishonesty Guardrails

`NATIVE_RESPONSE_FOURIER_FACTORIZATION_AUDIT.md` proved that 1-call full cyclic QFT readout $F_{3^M} D_y |+_D\rangle$ satisfies an $O(M)$ triangular autoregressive chain rule, whereas 2-call full cyclic QFT readout $F_{3^M}^\dagger D_y^{\pm 1} F_{3^M} D_y |+_D\rangle$ couples site $k$ and site $M - 1 - k$ across all $M$ digits. A standard quantum-circuit question is whether truncating the cyclic QFT $F_{3^M}$ to **twiddle bandwidth $b \in \{1, \dots, M\}$** (the approximate/banded QFT $F_{3^M}^{(b)}$ retaining controlled rotations of denominator at most $3^b$) preserves 2-call classical hardness while reducing circuit gate count from $O(M^2)$ to $O(M b)$.

This note and `theorems/native_banded_qft_transfer_matrix_audit.py` prove an exact tensor-network / transfer-matrix reduction answering that question:
- **Exact $O(M 3^b)$ transfer-matrix dequantization of bandwidth-$b$ two-call schedules**: Analytically eliminating the intermediate digits $v_{M-1-k} \in \{0, 1, 2\}$ reduces the $3^{2M}$-path double sum of $(F_{3^M}^{(b)})^\dagger D_y^{\pm 1} F_{3^M}^{(b)} D_y |+_D\rangle$ to a 1D sliding-window chain of treewidth $b - 1$ (transfer-matrix state dimension $3^{b-1}$), computable exactly in $\le M \cdot 3^{b+1}$ cyclotomic operations.
- **No dequantization of full-bandwidth ($b = M$) or $\ge 3$-call schedules**: At full bandwidth $b = M$, $3^{b-1} = 3^{M-1}$ is exponential in $M$, so full-bandwidth 2-call cyclic QFT schedules are not dequantized in $\mathrm{poly}(M)$ by this transfer matrix (`full_bandwidth_b_eq_M_is_poly_M = false`, `new_active_negative_result_created = false`, `accepted_speedup_candidate = false`).

## 2. Banded Cyclic QFT $F_{3^M}^{(b)}$ and Analytical Inner-Digit Elimination

Write $w, v, x \in \{0, \dots, 3^M - 1\}$ in base-3 site coordinates as
$$w = \sum_{\ell=0}^{M-1} w_\ell\, 3^{M - 1 - \ell}, \qquad v = \sum_{m=0}^{M-1} v_m\, 3^{M - 1 - m}, \qquad x = \sum_{\ell=0}^{M-1} x_\ell\, 3^{M - 1 - \ell}.$$
In the exact cyclic DFT kernel $\omega_{3^M}^{v(w - x)}$, the product $v(w - x) \bmod 3^M$ expands as
$$v(w - x) \equiv \sum_{m=0}^{M-1} \sum_{\ell=0}^{M-1} v_m (w_\ell - x_\ell)\, 3^{2M - 2 - m - \ell} \pmod{3^M}.$$
Terms with $2M - 2 - m - \ell \ge M$ (i.e. $m + \ell \le M - 2$) are divisible by $3^M$ and vanish modulo $3^M$. Setting $k = M - 1 - m \in \{0, \dots, M-1\}$, the surviving pairs satisfy $\ell \ge k$ with twiddle denominator $3^{\ell - k + 1}$.

For any **twiddle bandwidth $b \in \{1, \dots, M\}$**, define the banded cyclic QFT kernel by retaining all twiddle couplings of denominator $3^{\ell - k + 1} \le 3^b$, i.e. $k \le \ell \le \min(M - 1,\, k + b - 1)$:
$$\Phi^{(b)}(w, v; x) := \sum_{k=0}^{M-1} v_{M-1-k} \sum_{\ell=k}^{\min(M-1,\, k+b-1)} (w_\ell - x_\ell)\, 3^{M - 1 - (\ell - k)} \pmod{3^M}.$$
- At **$b = 1$**: only $\ell = k$ survives, so $F_{3^M}^{(1)} = P_{\mathrm{rev}} F_3^{\otimes M}$ is the bit-reversed tensor-product qutrit Fourier transform.
- At **$b = M$**: all $\ell \in [k, M-1]$ survive, recovering the **exact untruncated cyclic DFT** $F_{3^M}$ identically.

### Lemma 2.1 (Exact Analytical Elimination of the Intermediate Call Digits $v_m$)
Because the second response-phase gate $D_y^{\epsilon_2}(v) = \prod_{k=0}^{M-1} \omega_q^{\epsilon_2 \eta_{y, M-1-k}(v_{M-1-k})}$ is a product over $k = 0, \dots, M-1$ and $\Phi^{(b)}(w, v; x)$ is linear in each digit $v_{M-1-k}$, the $3^{2M}$-term two-call amplitude sum factorizes over $v_{M-1-k} \in \{0, 1, 2\}$ for every $w \in \{0, 1, 2\}^M$:
$$\mathcal{A}^{(b)}(x) = \frac{1}{3^{3M/2}} \sum_{w \in \{0,1,2\}^M} \omega_q^{\epsilon_1 \eta_y(w)} \sum_{v \in \{0,1,2\}^M} \omega_q^{\epsilon_2 \eta_y(v)}\, \omega_{3^M}^{\Phi^{(b)}(w, v; x)} = \frac{1}{3^{M/2}} \sum_{w \in \{0,1,2\}^M} \prod_{k=0}^{M-1} L_k^{(b)}\!\left(w_k, \dots, w_{\min(M-1,\, k+b-1)};\, x\right),$$
where each local window factor $L_k^{(b)}$ is a 3-term sum over $t = v_{M-1-k} \in \{0, 1, 2\}$:
$$L_k^{(b)}\!\left(w_k, \dots, w_{\min(M-1,\, k+b-1)};\, x\right) = \frac{1}{3}\, \omega_q^{\epsilon_1 \eta_{y,k}(w_k)} \sum_{t \in \{0,1,2\}} \omega_q^{\epsilon_2 \eta_{y, M-1-k}(t)}\, \omega_{3^M}^{t \sum_{\ell=k}^{\min(M-1, k+b-1)} (w_\ell - x_\ell) 3^{M - 1 - (\ell - k)}}.$$

## 3. Theorem 1: Exact $O(M 3^b)$ Sliding-Window Transfer-Matrix Contraction

Sweep FORWARD, k=0,...,M-1, as the Python implementation does. Before step k,
the boundary is (w_k,...,w_(min(M-1,k+b-2))). Initialize its table to one for
each assignment. Enumerate (w_k,...,w_(min(M-1,k+b-1))), multiply the previous
table entry by L_k, sum over w_k, and retain the remaining window digits.
At the right end the boundary shrinks; after the last step it is empty.
Its scalar is the complete path sum before the D^-1/2 normalization.
The earlier backward recurrence was incorrect: it discarded w_k although
earlier factors still needed it, and incorrectly declared S_0 empty.

### Theorem 3.1 (Exact Transfer-Matrix Complexity and Super-Logarithmic Bandwidth Necessity)
1. For any $M \ge 1$ and any bandwidth $b \in \{1, \dots, M\}$, the forward recurrence evaluates ONE outcome's exact Born probability $|\mathcal{A}^{(b)}(x)|^2$ using
   $$N_{\mathrm{DP}}(M, b) = \sum_{k=0}^{M-1} 3^{\min(b,\, M - k)} \le M \cdot 3^b$$
   local window evaluations (each a 3-term sum over $t \in \{0, 1, 2\}$), compared to $3^{2M}$ path pairs in the full double sum.
2. At $b = M$, the transfer-matrix contraction reproduces the exact untruncated two-call cyclic DFT readout `fourier_interleaved_readout` identically.
3. This counts local scalar evaluations, not bit complexity or distribution
   sampling. The audit code intentionally enumerates all outcomes and brute-force
   paths, so its runtime is NOT O(M*3^b). A single-point probability algorithm
   alone is insufficient to dequantize a sampler.

The separate [paid sampling baseline](NATIVE_BANDED_QFT_BASELINE.md) supplies
the missing marginalization: a doubled window network on (w,w',x), with
27^(b-1) boundary states and O(M^2*27^b) windows per sample. Exact integer
arithmetic, O(M+f+log M) phase bits, root certificates and output random bits
are charged. This establishes polynomial structural sampling cost for
b=O(log M) under its stated precision/access contract, not for full bandwidth
or three-plus calls. Resource caps are UNKNOWN, never hardness evidence.
Importantly, the new baseline also charges the TWO QFT truncation errors:
at inverse-polynomial accuracy even the FULL two-call cyclic public-phase
distribution has a polynomial structural classical approximation. The
exponential cost of the exact b=M contraction is not a hardness result.
