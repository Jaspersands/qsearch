# Retained Work-Register Multiplicity Erasure, Target-Amplitude Monotonicity, and Preimage Attack Equivalence

## 1. Scope and Dishonesty Guardrails

`NATIVE_KNOWN_SEED_GROUP_WORKBENCH.md` established that on the integer-secret slice $b \in \mathbb{Z}_q^n$ ($N = q^n$) with $B$ cohorts of $M$ qutrits ($D = B \cdot 3^M$), projecting the source register onto $|0\rangle$ leaves an unnormalized retained work state $|\Psi_{\mathrm{work}}(s, e)\rangle = \sum_{\sigma \in \mathbb{Z}_q^n} z_\sigma(s, e) |\sigma\rangle$, and identified the next target:
> "Study the weighted subset-sum map and multiplicity erasure on the retained work register. Constant relative frame conditioning does not remove an exponentially small absolute block-encoding scale. A classically compilable short-preimage sampler is also a classical chosen-frequency attack and must not be granted as a free quantum ingredient."

This note and `theorems/native_retained_work_multiplicity_erasure_audit.py` prove three exact theorems auditing retained work-register multiplicity erasure and preimage access:
- **No universal quantum lower bound**: Proving that passive diagonal work-register contractions $|w_\sigma| \le 1$ cannot increase the absolute target probability above $1/N$ applies to diagonal frequency-domain preconditioning of the single-pass retained work state, not to all quantum algorithms (`universal_quantum_lower_bound_claimed = false`, `new_active_negative_result_created = false`).
- **No speedup candidate**: Auditing exact multiplicity erasure and classical chosen-frequency preimage attacks does not supply a scalable quantum or classical solver (`accepted_speedup_candidate = false`).

## 2. Theorem 1: Conditional Readout Leakage from Fibre Multiplicity Variance

Let $p_\sigma = m_\sigma / D$ be the pushforward frequency distribution on $\mathbb{Z}_q^n$, where $\sum_{\sigma \in \mathbb{Z}_q^n} p_\sigma = 1$ and $C_A = \sum_{\sigma \in \mathbb{Z}_q^n} p_\sigma^2$. In the noiseless case ($e = 0$), $z_\sigma(s, 0) = p_\sigma \omega_q^{\langle \sigma, s\rangle}$, so the source-zero acceptance probability is $P_{\mathrm{zero}}(0) = C_A$. Applying the inverse QFT $F_q^\dagger$ on $\mathcal{H}_{\mathrm{work}} \cong \mathbb{C}^N$ maps $|\Psi_{\mathrm{work}}(s, 0)\rangle$ to
$$\widetilde{\Psi}_b = \frac{1}{\sqrt{N}} \sum_{\sigma \in \mathbb{Z}_q^n} p_\sigma\, \omega_q^{\langle \sigma, s + b\rangle}, \qquad b \in \mathbb{Z}_q^n.$$
At the true candidate $b = -s \bmod q$:
$$\widetilde{\Psi}_{-s} = \frac{1}{\sqrt{N}} \sum_{\sigma \in \mathbb{Z}_q^n} p_\sigma = \frac{1}{\sqrt{N}} \implies P(\text{readout } -s \text{ AND zero} \mid e=0) = |\widetilde{\Psi}_{-s}|^2 = \frac{1}{N}.$$
Consequently, the conditional probability of reading out the true secret $-s$ given source-zero is
$$P(\text{readout } -s \mid \text{zero}, e=0) = \frac{1 / N}{C_A} = \frac{1}{1 + N \sum_{\sigma \in \mathbb{Z}_q^n} (p_\sigma - 1/N)^2},$$
and the conditional leakage probability onto wrong secrets $b \ne -s$ is
$$P(\text{wrong secret } b \ne -s \mid \text{zero}, e=0) = 1 - \frac{1}{N C_A} = \frac{N C_A - 1}{N C_A} = \frac{\sum_\sigma (p_\sigma - 1/N)^2}{\sum_\sigma p_\sigma^2}.$$

## 3. Theorem 2: Multiplicity Erasure Block-Encoding Scale and Target-Amplitude Monotonicity

Suppose a passive diagonal operator $W = \operatorname{diag}(w_\sigma)$ with $|w_\sigma| \le 1$ is applied to the retained work register before $F_q^\dagger$.
1. **Exact Multiplicity Erasure on $\operatorname{supp}(p)$**:
   To equalize $w_\sigma p_\sigma = c_{\mathrm{flat}}$ across all supported frequencies $\sigma \in \operatorname{supp}(p) = \{\sigma : m_\sigma \ge 1\}$ subject to $0 \le w_\sigma \le 1$, the maximum physical scale is
   $$c_{\mathrm{flat}}^* = \min_{\sigma \in \operatorname{supp}(p)} p_\sigma = \frac{m_{\min}^+}{D}, \qquad w_\sigma^* = \begin{cases} m_{\min}^+ / m_\sigma, & m_\sigma \ge 1, \\ 0, & m_\sigma = 0. \end{cases}$$
   Writing $S_+ = |\operatorname{supp}(p)|$, the conditional probability of reading out $-s$ given joint source-zero and filter success becomes
   $$P(\text{readout } -s \mid \text{erased, zero}, e=0) = \frac{\left|\frac{1}{\sqrt{N}} S_+ c_{\mathrm{flat}}^*\right|^2}{S_+ (c_{\mathrm{flat}}^*)^2} = \frac{S_+}{N},$$
   which equals $1$ if and only if $\operatorname{supp}(p) = \mathbb{Z}_q^n$ (full frequency support).
2. **Absolute Target-Amplitude Monotonicity (No Free Scale Boost)**:
   For **any** contraction $|w_\sigma| \le 1$ and **any** error vector $e$, the joint probability of surviving source-zero, surviving $W$, and reading out $-s$ satisfies
   $$P_W(\text{readout } -s \text{ AND zero}, e) = \frac{1}{N}\left|\sum_{\sigma \in \mathbb{Z}_q^n} w_\sigma z_\sigma(0, e)\right|^2 \le \frac{1}{N}\left(\sum_{\sigma \in \mathbb{Z}_q^n} |z_\sigma(0, e)|\right)^2 \le \frac{1}{N}\left(\sum_{\sigma \in \mathbb{Z}_q^n} p_\sigma\right)^2 = \frac{1}{N}.$$
   In particular, for the optimal multiplicity eraser $W^* = \operatorname{diag}(w_\sigma^*)$ at $e = 0$:
   $$P_{W^*}(\text{readout } -s \text{ AND zero}, e=0) = \frac{1}{N}\left(\frac{S_+\,m_{\min}^+}{D}\right)^2 \le \frac{1}{N} = P_I(\text{readout } -s \text{ AND zero}, e=0),$$
   with strict inequality whenever $m_\sigma$ is non-constant or $\operatorname{supp}(p) \subsetneq \mathbb{Z}_q^n$. Thus passive multiplicity erasure increases conditional purity only by discarding excess fibre mass; it never increases the absolute target amplitude above $1/\sqrt{N}$.

## 4. Theorem 3: Classical Chosen-Frequency Preimage Equivalence

If a solver is granted a preimage oracle $\mathcal{O}_{\mathrm{pre}}$ that, given a target frequency $\sigma \in \mathbb{Z}_q^n$, returns a valid word $(b, w) \in [B] \times [3^M]$ with $\sigma(b, w) = \sigma$ (when $\sigma \in \operatorname{supp}(p)$), then querying $\mathcal{O}_{\mathrm{pre}}$ on the $n$ standard basis vectors $e_0, \dots, e_{n-1} \in \mathbb{Z}_q^n$ directly yields $n$ uncoupled scalar equations for the masked secret coordinates:
$$\eta_y(b_i, w_i) \equiv \langle e_i, s_{\mathrm{masked}} \rangle + \theta_e(b_i, w_i) = s_{\mathrm{masked}, i} + \theta_e(b_i, w_i) \pmod q, \qquad i \in \{0, \dots, n-1\}.$$
Hence a preimage sampler supplies classical coordinate observations and cannot
be assumed as an uncharged quantum preparation primitive. It recovers coordinates
directly in the NOISELESS case, provided those frequencies are supported.
With noise, the equations still contain $\theta_e$: a decoder, a sufficiently
small aggregate error law, and any repeated-sample independence/cost must be
proved. Subtracting calibration errors is NOT a public attack. The module now
labels that subtraction as a private forward-equation check and refuses the
formerly unconditional noisy-recovery interpretation.
