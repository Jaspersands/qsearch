# Native Higher-Call Time-Reversal Schedule-Duality Audit: Global Sign-Conjugation Invariance, Klein Four-Group Schedule Reduction, and Symmetric-Transpose Time-Reversal Duality

## 1. Motivation and Scope

A general $k$-call interleaved Fourier-response schedule on a word register of dimension $D$ is specified by $2k$ binary signs $(\epsilon, \sigma) \in \{-1, +1\}^k \times \{-1, +1\}^k$:
$$
|\Psi_{\epsilon, \sigma}(y)\rangle \;=\; F_D^{\sigma_k} D_y^{\epsilon_k} F_D^{\sigma_{k-1}} D_y^{\epsilon_{k-1}} \cdots F_D^{\sigma_1} D_y^{\epsilon_1} |+_D\rangle,
$$
spanning $4^k$ candidate schedules at call depth $k$. Identifying exact algebraic symmetries among these $4^k$ schedules eliminates redundant circuit evaluations and reveals structural equivalences between forward and time-reversed schedules.

This note proves three exact duality theorems: global sign-conjugation invariance $(\epsilon, \sigma) \leftrightarrow (-\epsilon, -\sigma)$, final-Fourier modular reflection $\sigma_k \leftrightarrow -\sigma_k$ (forming a universal Klein four-group symmetry $\mathbb{Z}_2 \times \mathbb{Z}_2$), and the exact symmetric-transpose time-reversal identity at outcome $x = 0$.

## 2. Theorem 1 — Exact Global Sign-Conjugation Invariance $(\epsilon, \sigma) \leftrightarrow (-\epsilon, -\sigma)$

**Theorem 1 (Pointwise Born Probability Invariance Under Global Sign Negation).**
For every $k \ge 1$, every schedule $(\epsilon, \sigma) \in \{-1, +1\}^k \times \{-1, +1\}^k$, and every phase vector $y \in \mathbb{Z}_q^D$:
1. In the computational basis, $D_y^{-\epsilon_\ell} = \overline{D_y^{\epsilon_\ell}}$, $F_D^{-\sigma_\ell} = \overline{F_D^{\sigma_\ell}}$, and $|+_D\rangle = \overline{|+_D\rangle}$, so
   $$
   |\Psi_{-\epsilon, -\sigma}(y)\rangle \;=\; \overline{|\Psi_{\epsilon, \sigma}(y)\rangle}.
   $$
2. Consequently, for every readout outcome $x \in \{0, \dots, D-1\}$ and every $y \in \mathbb{Z}_q^D$,
   $$
   P_{-\epsilon, -\sigma}(x \mid y) \;=\; \bigl|\langle x \mid \Psi_{-\epsilon, -\sigma}(y)\rangle\bigr|^2 \;=\; P_{\epsilon, \sigma}(x \mid y),
   $$
   and $\rho_{-\epsilon, -\sigma}(s) = \rho_{\epsilon, \sigma}(s)^T$ for all $s \in \mathbb{Z}_q^n$.

## 3. Theorem 2 — Final-Fourier Reflection $\sigma_k \leftrightarrow -\sigma_k$ and Klein Four-Group Quotient

Let $\Pi_{\text{neg}} \in O(D)$ denote the modular negation permutation $\Pi_{\text{neg}}|x\rangle := |(-x) \bmod D\rangle$.

**Theorem 2 (Final-Fourier Reflection and 4-Fold Schedule-Space Reduction).**
1. Because $\langle x | F_D^{-\sigma_k} | w_k \rangle = D^{-1/2} e^{-\sigma_k 2\pi i x w_k / D} = \langle (-x) \bmod D | F_D^{\sigma_k} | w_k \rangle$, $F_D^{-\sigma_k} = \Pi_{\text{neg}} F_D^{\sigma_k}$. Flipping only the final Fourier direction $\sigma_k \mapsto -\sigma_k$, i.e. $\tilde{\sigma} := (\sigma_1, \dots, \sigma_{k-1}, -\sigma_k)$, permutes the output state and Born distribution by modular negation:
   $$
   |\Psi_{\epsilon, \tilde{\sigma}}(y)\rangle \;=\; \Pi_{\text{neg}}|\Psi_{\epsilon, \sigma}(y)\rangle, \qquad
   P_{\epsilon, \tilde{\sigma}}(x \mid y) \;=\; P_{\epsilon, \sigma}\bigl((-x) \bmod D \;\big|\; y\bigr).
   $$
2. Together with global sign negation (Theorem 1), the two commuting involutions
   $$
   \iota_1(\epsilon, \sigma) \;:=\; (-\epsilon, -\sigma), \qquad
   \iota_2(\epsilon, \sigma) \;:=\; \bigl(\epsilon,\, (\sigma_1, \dots, \sigma_{k-1}, -\sigma_k)\bigr)
   $$
   generate a free Klein four-group $\mathcal{G}_4 = \{I, \iota_1, \iota_2, \iota_1\iota_2\} \cong \mathbb{Z}_2 \times \mathbb{Z}_2$ partitioning the $4^k$ schedules into $4^{k-1}$ orbits of size $4$, on each of which the computational-basis $L_2$ signal energy $\mathcal{E}_{\epsilon, \sigma}$ and the operator Hilbert–Schmidt variance $\mathcal{V}_{\text{HS}}(\epsilon, \sigma)$ are **identically constant**.

## 4. Theorem 3 — Symmetric-Matrix Transpose Identity and Time-Reversal Duality at $x = 0$

For any $k$-call schedule $(\epsilon, \sigma)$, define its **time-reversed schedule** $(\epsilon^{\text{rev}}, \sigma^{\text{rev}})$ by reversing the $k$ response signs and the first $k - 1$ internal Fourier signs:
$$
\epsilon^{\text{rev}} \;:=\; (\epsilon_k, \epsilon_{k-1}, \dots, \epsilon_1), \qquad
\sigma^{\text{rev}} \;:=\; (\sigma_{k-1}, \sigma_{k-2}, \dots, \sigma_1, \sigma_k).
$$

**Theorem 3 (Exact Zero-Outcome Time-Reversal Duality).**
For every $k \ge 1$, every schedule $(\epsilon, \sigma) \in \{-1, +1\}^k \times \{-1, +1\}^k$, and every phase vector $y \in \mathbb{Z}_q^D$:
$$
\langle 0_D \mid \Psi_{\epsilon, \sigma}(y)\rangle \;=\; \langle 0_D \mid \Psi_{\epsilon^{\text{rev}}, \sigma^{\text{rev}}}(y)\rangle,
\qquad
P_{\epsilon, \sigma}(0 \mid y) \;=\; P_{\epsilon^{\text{rev}}, \sigma^{\text{rev}}}(0 \mid y).
$$

*Proof.*
For both $\sigma_k \in \{-1, +1\}$, $\langle 0_D | F_D^{\sigma_k} = D^{-1/2}\sum_{w=0}^{D-1}\langle w| = \langle +_D |$. Thus $\langle 0_D | \Psi_{\epsilon, \sigma}(y)\rangle = \langle +_D | M_{\epsilon, \sigma}(y) | +_D \rangle$, where $M_{\epsilon, \sigma}(y) := D_y^{\epsilon_k} F_D^{\sigma_{k-1}} \cdots F_D^{\sigma_1} D_y^{\epsilon_1}$. Because $D_y^{\pm 1}$ is diagonal and $F_D^{\pm 1}$ is complex-symmetric ($(F_D^{\pm 1})^T = F_D^{\pm 1}$), taking the matrix transpose reverses the operator product:
$$
M_{\epsilon, \sigma}(y)^T \;=\; (D_y^{\epsilon_1})^T (F_D^{\sigma_1})^T \cdots (F_D^{\sigma_{k-1}})^T (D_y^{\epsilon_k})^T \;=\; D_y^{\epsilon_1} F_D^{\sigma_1} \cdots F_D^{\sigma_{k-1}} D_y^{\epsilon_k} \;=\; M_{\epsilon^{\text{rev}}, \sigma^{\text{rev}}}(y).
$$
Since $|+_D\rangle$ is real, $\langle +_D | M | +_D \rangle = \langle +_D | M^T | +_D \rangle$, proving the exact amplitude and probability equality. $\square$
