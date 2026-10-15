# Response-Phase Fourier Factorization: Tensor Qutrit Dequantization, 1-Call Cyclic Autoregressive Chain Rule, and Signed 2-Call Pinching

## 1. Scope and Dishonesty Guardrails

`NATIVE_RESPONSE_PATH_VALUATION.md` analyzed the two-call cyclic Fourier schedule $F_D^\dagger D_y F_D D_y |+_D\rangle$ ($D = 3^M$) and noted that dense classical FFT simulation of that schedule stores $D = 3^M$ amplitudes and costs $O(D \log D) = O(M 3^M)$ work. Three structural questions immediately arise for algorithm design:
1. What happens if the cyclic Fourier transform $F_{3^M}$ over $\mathbb{Z}_{3^M}$ is replaced by the physical **tensor-product qutrit Fourier transform** $F_3^{\otimes M}$ over $\mathbb{F}_3^M$?
2. Does a **single-call** cyclic Fourier readout $F_{3^M} D_y |+_D\rangle$ require $O(3^M)$ classical work, or does the additive digit structure of $\eta_y(w)$ make it classically tractable in $O(M)$ time?
3. How does the **signed $(+1, -1)$ two-call schedule** $F_D^\dagger D_y^\dagger F_D D_y |+_D\rangle$ differ from the unsigned $(+1, +1)$ schedule $F_D^\dagger D_y F_D D_y |+_D\rangle$ under uniform-secret pinching and original noise?

This note and `theorems/native_response_fourier_factorization_audit.py` prove exact cyclotomic theorems answering all three questions:
- **Finite audit is not a general impossibility result**: This audit establishes product and one-call identities, not a polynomial two-call sampler. The separate [paid classical baseline](NATIVE_BANDED_QFT_BASELINE.md) now DOES give approximate classical sampling of two-call FULL cyclic QFT public-phase schedules at inverse-polynomial accuracy, by combining QFT truncation and doubled marginal contraction. Exact full-bandwidth sampling, three-plus calls and arbitrary entangling mixers are not claimed (`new_active_negative_result_created = false`).
- **No speedup candidate**: Auditing these schedules does not supply a polynomial-time quantum distinguisher (`accepted_speedup_candidate = false`).

## 2. Theorem 1: Exact $O(M)$ Product Factorization of Tensor-Product Qutrit Schedules

Because the native word phase $\eta_y(w) = \sum_{j=0}^{M-1} \eta_{y,j}(w_j) \pmod q$ is additive across the $M$ pair sites $w = (w_0, \dots, w_{M-1}) \in \{0, 1, 2\}^M$, the diagonal response unitary factorizes as an exact tensor product of 1-qutrit diagonal gates:
$$D_y = \bigotimes_{j=0}^{M-1} D_{y,j}, \qquad D_{y,j} = \operatorname{diag}\!\left(\omega_q^{\eta_{y,j}(0)},\, \omega_q^{\eta_{y,j}(1)},\, \omega_q^{\eta_{y,j}(2)}\right) \in \mathrm{U}(3).$$

### Proposition 2.1 (Tensor-Product Qutrit Interleaving Dequantizes to $M$ Independent Single-Qutrit Readouts)
For any sequence of tensor-product qutrit mixers $V_\ell = \bigotimes_{j=0}^{M-1} V_{\ell, j}$ (in particular $V_\ell = F_3^{\otimes M}$) and any sign pattern $(\epsilon_1, \dots, \epsilon_k) \in \{-1, +1\}^k$, the $k$-call state
$$|\Psi_y^{\mathrm{tensor}}\rangle = \left(\prod_{\ell=1}^k V_\ell D_y^{\epsilon_\ell}\right) |+_3\rangle^{\otimes M} = \bigotimes_{j=0}^{M-1} |\psi_{y,j}^{(k)}\rangle, \qquad |\psi_{y,j}^{(k)}\rangle = \left(\prod_{\ell=1}^k V_{\ell,j} D_{y,j}^{\epsilon_\ell}\right)|+_3\rangle,$$
is a product state across the $M$ qutrits. For $k = 2$ with $F_3^{\otimes M}$, the Born probability of any outcome $x = (x_0, \dots, x_{M-1}) \in \mathbb{F}_3^M$ is the exact product of $M$ marginal 3-outcome distributions:
$$\mathbb{P}_{\mathrm{tensor}}(x_0, \dots, x_{M-1}) = \prod_{j=0}^{M-1} P_j(x_j), \qquad P_j(x_j) = \left|\frac{1}{3\sqrt{3}} \sum_{w_j, v_j \in \{0,1,2\}} \omega_q^{\epsilon_1 \eta_{y,j}(w_j) + \epsilon_2 \eta_{y,j}(v_j)}\, \omega_3^{v_j(w_j - x_j)}\right|^2.$$
Computing all $M$ single-qutrit distributions $\{P_j(0), P_j(1), P_j(2)\}_{j=0}^{M-1}$ requires $27 M$ path terms ($O(M)$ time) rather than $3^{2M}$ path terms, and differs from the cyclic $F_{3^M}$ distribution for $M \ge 2$ because $F_{3^M}$ contains inter-digit twiddle phases $\omega_{3^M}^{v \cdot w}$.

## 3. Theorem 2: Exact $O(M)$ Triangular Autoregressive Chain Rule for One-Call Cyclic DFT Readout

Consider the **one-call cyclic Fourier state** $|\widehat{\psi}_y\rangle = F_{3^M} D_y |+_D\rangle$ on $\mathbb{Z}_{3^M}$ ($D = 3^M$). Use output digits LSB first, $v=\sum_k v_k3^k$, and original site/input digits MSB first, $w=\sum_k w_k3^{M-1-k}$, matching `word_rows`. Then
$$\langle v | F_{3^M} D_y |+_D\rangle=\prod_{k=0}^{M-1} A_k(v_0,\dots,v_k),\qquad A_k=\frac{1}{3}\sum_{t=0}^2\omega_q^{\eta_{y,k}(t)}\omega_{3^{k+1}}^{v_{\mathrm{prefix}}t}\omega_3^{v_kt},$$
where $v_{\mathrm{prefix}}=\sum_{i<k}v_i3^i$. There is NO additional $1/\sqrt3$ factor in the product.

### Theorem 3.1 (Triangular Parseval Normalization and $O(M)$ Exact Classical Autoregressive Sampling)
For every $k$ and every lower-digit prefix, set $\alpha_t=\omega_q^{\eta_{y,k}(t)}\omega_{3^{k+1}}^{v_{\mathrm{prefix}}t}$, which has unit modulus. The three $A_k$ values are the unitary three-point DFT applied to $\alpha/\sqrt3$. By Parseval:
$$\sum_{v_k \in \{0, 1, 2\}} P_k(v_k \mid v_0, \dots, v_{k-1}) = 1 \quad \text{where} \quad P_k(v_k \mid v_0, \dots, v_{k-1}) := \left|A_k(v_0, \dots, v_k)\right|^2,$$
and the full $3^M$-outcome cyclic DFT Born distribution satisfies the **exact triangular chain rule**
$$\mathbb{P}_{\mathrm{1\text{-}call, cyclic}}(v_0, \dots, v_{M-1}) = \prod_{k=0}^{M-1} P_k(v_k \mid v_0, \dots, v_{k-1}).$$
Consequently, evaluating $\mathbb{P}_{\mathrm{1\text{-}call, cyclic}}(v)$ at any outcome $v \in \mathbb{Z}_{3^M}$ or sampling $v = (v_0, \dots, v_{M-1})$ sequentially digit-by-digit requires only $O(M)$ classical work, without allocating $3^M$ amplitudes. Only at $k \ge 2$ response calls ($F_D^\dagger D_y^{\pm 1} F_D D_y |+_D\rangle$), where the second gate $D_y^{\pm 1}(v)$ couples site $k$ to site $M - 1 - k$, is this triangular autoregressive factorization broken.

## 4. Theorem 3: Signed $(+1, -1)$ vs Positive $(+1, +1)$ Two-Call Cyclic Readout and Diagonal Invariance

Consider the signed $(+1, -1)$ two-call cyclic schedule
$$|\Psi_y^{(-,+)}\rangle = F_D^\dagger D_y^\dagger F_D D_y |+_D\rangle, \qquad \langle x | \Psi_y^{(-,+)}\rangle = \frac{1}{D^{3/2}} \sum_{w, v \in [D]} \omega_q^{\eta_y(w) - \eta_y(v)}\, \omega_D^{v(w - x)}.$$
1. **Difference-relation pinching**: Averaging over $s \sim \operatorname{Uniform}(\mathbb{Z}_q^n)$ pinches the 4-tuple sum $(w, v; w', v') \in [D]^4$ onto the **difference collision relation**
   $$f_A(w) - f_A(v) \equiv f_A(w') - f_A(v') \pmod q.$$
2. **Diagonal data-phase cancellation is not a probability floor**: On $w=v$, the secret and error phases cancel, but the Fourier phase is $\omega_D^{w(w-x)}$, NOT one. The diagonal amplitude is $D^{-3/2}\sum_w\omega_D^{w(w-x)}$. For odd $D=3^M$ its squared modulus is $D^{-2}$, by the quadratic Gauss sum identity. It can interfere destructively with off-diagonal paths; neither $D^{-1}$ nor $D^{-2}$ is a lower bound on the full outcome probability. At $D=3,q=9$, valid paired-row phases $(8,1,0)$ give $P(x=0)\approx0.0519901<1/9<1/3$. The exact countercontrol and all diagonal Fourier component weights are now recorded and replayed independently.

These finite exact routines enumerate distributions to check identities; they are
NOT the claimed linear-time sampling implementation. Operation counts above use
scalar arithmetic, not free exact cyclotomic arithmetic or uncharged bit precision.
The separate `native_banded_qft_baseline.py` implements dense-free sampling with
explicit phase and random-bit error budgets.
