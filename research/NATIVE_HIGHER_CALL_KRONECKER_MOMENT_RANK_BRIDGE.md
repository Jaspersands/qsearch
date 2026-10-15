# Native Higher-Call Kronecker Moment-Rank Bridge: 4-Tuple Difference-Variety Parseval Identity, Harmonic Conjugate Symmetry, and $L_2$ Signal Energy Bounds

## 1. Motivation and Scope

In `theorems/native_higher_call_weighted_fourier_pinching_audit.py` (Subsystem 17), we proved that the first moment $\mathbb{E}_{s \sim \mathbb{Z}_q^n}[P_{\epsilon, \sigma}(x \mid s)]$ of a general $k$-call interleaved Fourier-response schedule pinches onto the signed frequency-collision variety $\mathcal{V}_\epsilon(f) = \{(w, w') : \tau_\epsilon(w) \equiv \tau_\epsilon(w') \pmod q\}$. However, whether a single problem instance with fixed secret $s \in \mathbb{Z}_q^n$ produces a detectable readout fluctuation $P_{\epsilon, \sigma}(x \mid s) - \mathbb{E}_{s'}[P_{\epsilon, \sigma}(x \mid s')]$ is governed by the **second moment (variance) across secrets $s \sim \mathbb{Z}_q^n$**.

This note proves three exact theorems characterizing the secret-Fourier harmonic decomposition of $P_{\epsilon, \sigma}(x \mid s)$, the 4-tuple Kronecker difference-variety Parseval identity for $\operatorname{Var}_s[P_{\epsilon, \sigma}(x \mid s)]$, and the 4-tuple multiplicity upper bound on total $L_2$ signal energy.

## 2. Theorem 1 — Exact 4-Tuple Kronecker Difference-Variety Parseval Identity

For any trajectory pair $(w, w') \in \{0, \dots, D-1\}^k \times \{0, \dots, D-1\}^k$, define its signed frequency difference
$$
\Delta\tau_\epsilon(w, w') \;:=\; \bigl(\tau_\epsilon(w) - \tau_\epsilon(w')\bigr) \bmod q \;\in\; \mathbb{Z}_q^n
$$
and its weighted unitary pair amplitude at readout $x \in \{0, \dots, D-1\}$:
$$
B_{\epsilon, \sigma}(w, w'; x) \;:=\; \frac{1}{D^{k+1}} \exp\!\left(\frac{2\pi i}{q}\bigl(E_\epsilon(w) - E_\epsilon(w')\bigr) + \frac{2\pi i}{D}\bigl(\Phi_\sigma(w; x) - \Phi_\sigma(w'; x)\bigr)\right).
$$
Grouping trajectory pairs by $\delta = \Delta\tau_\epsilon(w, w') \in \mathbb{Z}_q^n$ defines the **secret-Fourier harmonics**
$$
C_{\epsilon, \sigma}(\delta; x) \;:=\; \sum_{\substack{(w, w') \in \{0, \dots, D-1\}^{2k} \\ \Delta\tau_\epsilon(w, w') = \delta}} B_{\epsilon, \sigma}(w, w'; x), \qquad P_{\epsilon, \sigma}(x \mid s) \;=\; \sum_{\delta \in \mathbb{Z}_q^n} C_{\epsilon, \sigma}(\delta; x)\,\omega_q^{\langle \delta, s\rangle}.
$$

**Theorem 1 (Exact Parseval Identity for Secret Variance via Non-Zero Difference Fibers).**
For every $(\epsilon, \sigma) \in \{-1, +1\}^k \times \{-1, +1\}^k$ and every readout outcome $x \in \{0, \dots, D-1\}$:
1. The zero-difference harmonic equals the secret-averaged distribution: $C_{\epsilon, \sigma}(0; x) = \mathbb{E}_{s \sim \mathbb{Z}_q^n}[P_{\epsilon, \sigma}(x \mid s)]$.
2. By character orthogonality on $\mathbb{Z}_q^n$, the variance of $P_{\epsilon, \sigma}(x \mid s)$ over $s \sim \operatorname{Unif}(\mathbb{Z}_q^n)$ equals the sum of squared moduli of the non-zero difference harmonics:
   $$
   \operatorname{Var}_{s \sim \mathbb{Z}_q^n}\bigl[P_{\epsilon, \sigma}(x \mid s)\bigr]
   \;:=\; \mathbb{E}_{s \sim \mathbb{Z}_q^n}\!\left[\bigl(P_{\epsilon, \sigma}(x \mid s) - C_{\epsilon, \sigma}(0; x)\bigr)^2\right]
   \;=\; \sum_{\delta \in \mathbb{Z}_q^n \setminus \{0\}} \bigl|C_{\epsilon, \sigma}(\delta; x)\bigr|^2.
   $$

## 3. Theorem 2 — Hermitian Conjugate Symmetry and Zero-Outcome-Sum Conservation

**Theorem 2 (Conjugate Symmetry and Outcome Annihilation of Non-Zero Harmonics).**
1. **Hermitian Conjugate Symmetry**: Under pair transposition $(w, w') \leftrightarrow (w', w)$, $\Delta\tau_\epsilon(w', w) \equiv -\Delta\tau_\epsilon(w, w') \pmod q$ and $B_{\epsilon, \sigma}(w', w; x) = \overline{B_{\epsilon, \sigma}(w, w'; x)}$, so for all $\delta \in \mathbb{Z}_q^n$ and $x \in \{0, \dots, D-1\}$:
   $$
   C_{\epsilon, \sigma}(-\delta \bmod q; x) \;=\; \overline{C_{\epsilon, \sigma}(\delta; x)}.
   $$
2. **Outcome Sum Annihilation**: Because $\sum_{x=0}^{D-1} P_{\epsilon, \sigma}(x \mid s) = 1$ identically for every $s \in \mathbb{Z}_q^n$, uniqueness of the Fourier expansion on $\mathbb{Z}_q^n$ implies
   $$
   \sum_{x=0}^{D-1} C_{\epsilon, \sigma}(0; x) \;=\; 1 \qquad \text{and} \qquad \sum_{x=0}^{D-1} C_{\epsilon, \sigma}(\delta; x) \;=\; 0 \quad \forall \delta \in \mathbb{Z}_q^n \setminus \{0\}.
   $$

## 4. Theorem 3 — 4-Tuple Kronecker Multiplicity Bound on Total $L_2$ Signal Energy

Let $M_\epsilon(\delta) := |\{(w, w') \in \{0, \dots, D-1\}^{2k} : \Delta\tau_\epsilon(w, w') = \delta\}|$ denote the cardinality of the difference fiber $\delta \in \mathbb{Z}_q^n$.

**Theorem 3 (4-Tuple Kronecker Variety Partition and $L_2$ Energy Bound).**
1. The difference-fiber cardinalities satisfy $\sum_{\delta \in \mathbb{Z}_q^n} M_\epsilon(\delta) = D^{2k}$ and $M_\epsilon(0) = |\mathcal{V}_\epsilon(f)|$, and the number of 4-tuples $(w^{(1)}, w^{(2)}, w^{(3)}, w^{(4)}) \in \{0, \dots, D-1\}^{4k}$ satisfying the additive Kronecker relation $\tau_\epsilon(w^{(1)}) - \tau_\epsilon(w^{(2)}) \equiv \tau_\epsilon(w^{(3)}) - \tau_\epsilon(w^{(4)}) \not\equiv 0 \pmod q$ is $\mathcal{K}_\epsilon^{\text{off}}(f) := \sum_{\delta \in \mathbb{Z}_q^n \setminus \{0\}} M_\epsilon(\delta)^2$.
2. Since $|B_{\epsilon, \sigma}(w, w'; x)| = D^{-(k+1)}$, $|C_{\epsilon, \sigma}(\delta; x)| \le M_\epsilon(\delta) / D^{k+1}$ for every $x$, so the total $L_2$ secret signal energy across all $D$ outcomes obeys the deterministic upper bound
   $$
   \mathcal{E}_{\epsilon, \sigma} \;:=\; \sum_{x=0}^{D-1} \operatorname{Var}_{s \sim \mathbb{Z}_q^n}\bigl[P_{\epsilon, \sigma}(x \mid s)\bigr]
   \;\le\; \frac{\mathcal{K}_\epsilon^{\text{off}}(f)}{D^{2k+1}} \;=\; \frac{1}{D^{2k+1}} \sum_{\delta \in \mathbb{Z}_q^n \setminus \{0\}} M_\epsilon(\delta)^2,
   $$
   with strict inequality whenever destructive unitary Fourier-phase interference occurs within the non-zero difference fibers.
