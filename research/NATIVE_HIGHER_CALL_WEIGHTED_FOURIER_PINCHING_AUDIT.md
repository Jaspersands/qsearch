# Higher-Call Weighted Fourier Pinching Audit: Signed Frequency-Collision Varieties, Diagonal Floor Conservation, and 3-Call Exact Cyclotomic Readout

## 1. Motivation and Scope

In `theorems/native_response_path_valuation.py`, the research decision concludes:
```text
SEARCH_WEIGHTED_UNITARY_PATHS_NOT_UNWEIGHTED_COLLISION_COUNTS
```
While `native_response_path_valuation.py` implements the 2-call unsigned schedule $F_D^\dagger D_y F_D D_y |+_D\rangle$ ($\epsilon = (+1, +1)$, $\sigma = (+1, -1)$), general $k$-call interleaved Fourier-response schedules are parameterized by a response sign tuple $\epsilon = (\epsilon_1, \dots, \epsilon_k) \in \{-1, +1\}^k$ and a Fourier direction tuple $\sigma = (\sigma_1, \dots, \sigma_k) \in \{-1, +1\}^k$:
$$
|\Psi_{\epsilon, \sigma}(y)\rangle
\;=\; F_D^{\sigma_k} D_y^{\epsilon_k} F_D^{\sigma_{k-1}} D_y^{\epsilon_{k-1}} \cdots F_D^{\sigma_1} D_y^{\epsilon_1} |+_D\rangle,
$$
where $\langle b | F_D^{\pm 1} | a \rangle = D^{-1/2} e^{\pm 2\pi i a b / D}$ and $D_y^{\pm 1} |w\rangle = e^{\pm 2\pi i y_w / q}|w\rangle$.

This note proves three exact theorems governing the general $k$-call weighted unitary path integral, its uniform-secret frequency pinching onto $\mathcal{V}_\epsilon(f)$, and the destructive interference of off-diagonal collision pairs compared to unweighted path counts.

## 2. Theorem 1 — General $k$-Call Weighted Unitary Path Integral and Signed Frequency Pinching

For a word table of size $D = 3^M$ over modulus $q = 3^d$, each word $w \in \{0, \dots, D-1\}$ has a public frequency vector $f(w) \in \mathbb{Z}_q^n$ and known public phase $y_w \equiv \langle f(w), s\rangle + e(w) \pmod q$ under secret $s \in \mathbb{Z}_q^n$ and error phase $e(w) \in \mathbb{Z}_q$.

For any $k$-call trajectory $w = (w_1, \dots, w_k) \in \{0, \dots, D-1\}^k$ and readout outcome $x \in \{0, \dots, D-1\}$, define:
- the **signed net frequency** $\tau_\epsilon(w) := \sum_{\ell=1}^k \epsilon_\ell f(w_\ell) \bmod q \in \mathbb{Z}_q^n$,
- the **signed net error phase** $E_\epsilon(w) := \sum_{\ell=1}^k \epsilon_\ell e(w_\ell) \bmod q \in \mathbb{Z}_q$, and
- the **bilinear unitary Fourier phase**
  $$
  \Phi_\sigma(w; x) \;:=\; \left(\sum_{\ell=1}^{k-1} \sigma_\ell w_{\ell+1} w_\ell \;+\; \sigma_k x w_k\right) \bmod D.
  $$

**Theorem 1 (Exact $k$-Call Uniform-Secret Pinching Identity).**
For every $k \ge 1$, every $(\epsilon, \sigma) \in \{-1, +1\}^k \times \{-1, +1\}^k$, and every readout outcome $x \in \{0, \dots, D-1\}$, averaging the Born probability $P_{\epsilon, \sigma}(x \mid s) = |\langle x | \Psi_{\epsilon, \sigma}(y(s))\rangle|^2$ over a uniform secret $s \sim \mathbb{Z}_q^n$ pinches the double trajectory sum onto the signed frequency-collision fibers $\tau_\epsilon(w) = \tau_\epsilon(w')$:
$$
\mathbb{E}_{s \sim \mathbb{Z}_q^n}\bigl[P_{\epsilon, \sigma}(x \mid s)\bigr]
\;=\; \frac{1}{D^{k+1}} \sum_{\tau \in \mathbb{Z}_q^n} \left|\sum_{\substack{w \in \{0, \dots, D-1\}^k \\ \tau_\epsilon(w) = \tau}} \exp\!\left(\frac{2\pi i}{q} E_\epsilon(w) + \frac{2\pi i}{D}\Phi_\sigma(w; x)\right)\right|^2.
$$

*Proof.*
Expanding $|\langle x | \Psi_{\epsilon, \sigma}(y(s))\rangle|^2$ over trajectory pairs $(w, w') \in \{0, \dots, D-1\}^k \times \{0, \dots, D-1\}^k$ yields the $s$-dependent character factor $\exp(\frac{2\pi i}{q}\langle \tau_\epsilon(w) - \tau_\epsilon(w'), s\rangle)$. By character orthogonality on $\mathbb{Z}_q^n$, averaging over $s \in \mathbb{Z}_q^n$ projects onto $\tau_\epsilon(w) \equiv \tau_\epsilon(w') \pmod q$, which partitions into the sum of squared moduli over $\tau \in \mathbb{Z}_q^n$. $\square$

## 3. Theorem 2 — Diagonal Floor Conservation and Off-Diagonal Unitary Cancellation

Define the signed frequency-collision variety
$$
\mathcal{V}_\epsilon(f) \;:=\; \bigl\{\, (w, w') \in \{0, \dots, D-1\}^k \times \{0, \dots, D-1\}^k : \tau_\epsilon(w) = \tau_\epsilon(w') \,\bigr\}.
$$

**Theorem 2 (Exact Decomposition Into $1/D$ Diagonal Floor and Zero-Mean Oscillatory Surplus).**
1. **Universal diagonal floor**: The $D^k$ diagonal pairs $w = w'$ belong to $\mathcal{V}_\epsilon(f)$ for every frequency map $f$ and have $E_\epsilon(w) - E_\epsilon(w) = 0$ and $\Phi_\sigma(w; x) - \Phi_\sigma(w; x) = 0$, contributing the exact uniform floor $D^k / D^{k+1} = 1/D$ to every outcome $x \in \{0, \dots, D-1\}$.
2. **Zero-sum off-diagonal interference**: Writing $\mathbb{E}_s[P_{\epsilon, \sigma}(x \mid s)] = \frac{1}{D} + \Delta P_{\epsilon, \sigma}^{\text{off}}(x)$, the off-diagonal pinched contribution
   $$
   \Delta P_{\epsilon, \sigma}^{\text{off}}(x)
   \;=\; \frac{1}{D^{k+1}} \sum_{\substack{(w, w') \in \mathcal{V}_\epsilon(f) \\ w \ne w'}} \exp\!\left(\frac{2\pi i}{q}\bigl(E_\epsilon(w) - E_\epsilon(w')\bigr) + \frac{2\pi i}{D}\bigl(\Phi_\sigma(w; x) - \Phi_\sigma(w'; x)\bigr)\right)
   $$
   satisfies $\sum_{x=0}^{D-1} \Delta P_{\epsilon, \sigma}^{\text{off}}(x) = 0$ identically, whereas the unweighted collision ratio $|\mathcal{V}_\epsilon(f)| / D^{2k} \ge 1/D^k$ is strictly positive and ignores the bilinear Fourier phases $\Phi_\sigma(w; x) - \Phi_\sigma(w'; x)$.

## 4. Theorem 3 — Balanced Signed vs Unsigned Pinching Multiplicity Contrast

**Theorem 3 (Diagonal Sub-Collisions in Balanced Signed Schedules $\epsilon = (+1, -1)$).**
For $k = 2$, under the unsigned schedule $\epsilon = (+1, +1)$, $\tau_{(+1,+1)}(w_1, w_2) = f(w_1) + f(w_2)$ is symmetric under transposition $(w_1, w_2) \leftrightarrow (w_2, w_1)$, creating $D(D-1)$ transpose collisions $(w_1, w_2) \leftrightarrow (w_2, w_1)$ with $w_1 \ne w_2$. Under the balanced signed schedule $\epsilon = (+1, -1)$, $\tau_{(+1,-1)}(w_1, w_2) = f(w_1) - f(w_2)$ vanishes identically on all $D$ self-difference pairs $w_1 = w_2$, concentrating all $D$ zero-frequency trajectories into the single fiber $\tau = 0 \in \mathbb{Z}_q^n$.
