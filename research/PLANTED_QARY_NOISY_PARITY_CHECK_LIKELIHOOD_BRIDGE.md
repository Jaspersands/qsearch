# Planted $q$-ary Noisy Parity-Check Likelihood Bridge: Exact Weight-Power Fourier Damping, Off-Dual Noise Invariance, and Dual Minimum-Distance Scaling

## Correction And Decision

The v1 quantum-readout claim was false: random translation of a coherent
coset state does NOT convolve its Fourier measurement distribution. The
classical character and window identities remain valid. Version 2 separates
translation noise, phase noise and an incoherent classical source, with actual
density-operator QFT controls and a separate Born-sum JavaScript replay.
No new algorithm, coherent state-preparation procedure, or quantum advantage
is supplied. The implementation supports prime fields only. For extension
fields, field multiplication and trace characters must replace residue arithmetic.

## 1. Motivation and Scope

In `theorems/planted_qary_second_moment_probe_variance_bridge.py` (Subsystem 24), noiseless linear probes $u \in \mathbb{F}_q^n$ against a dimension-$d$ planted subspace $B = \operatorname{rowspan}(M) \subset \mathbb{F}_q^n$ were shown to have constant acceptance fraction $R/q$ for all $u \notin B^\perp$ and deterministic indicator $\mathbf{1}_{0 \in W}$ for all $u \in B^\perp$.

When codewords $b \in B$ are corrupted by i.i.d. $q$-ary depolarizing coordinate noise $e = (e_1, \dots, e_n) \sim \mathcal{D}_\gamma^{\otimes n}$ (where each coordinate $e_j \in \mathbb{F}_q$ equals $0$ with probability $1 - \frac{q-1}{q}\gamma$ and equals each non-zero element of $\mathbb{F}_q^\times$ with probability $\frac{\gamma}{q}$, for $\gamma \in [0, 1]$), how does the noisy observation $x = b + e \in \mathbb{F}_q^n$ transform both the quantum $\mathrm{QFT}_q^{\otimes n}$ dual distribution and the classical probe window-acceptance probabilities? This note proves three exact theorems resolving noisy parity-check likelihood and window acceptance on $\mathbb{F}_q^n$.

## 2. Theorem 1 — Exact Hamming-Weight Power Damping of Dual Character Expectations

For a single coordinate $e_j \sim \mathcal{D}_\gamma$ on $\mathbb{F}_q$ and any scalar $u_j \in \mathbb{F}_q$, the character expectation is
$$
\mathbb{E}_{e_j \sim \mathcal{D}_\gamma}\bigl[\omega_q^{u_j e_j}\bigr] \;=\;
\begin{cases}
1, & u_j = 0, \\
1 - \gamma, & u_j \in \mathbb{F}_q^\times.
\end{cases}
$$

**Theorem 1 (Exact Weight-Power Law for Noisy Planted Subspace Characters).**
For any dimension-$d$ subspace $B \subset \mathbb{F}_q^n$, noise rate $\gamma \in [0, 1]$, and probe $u \in \mathbb{F}_q^n$ of Hamming weight $\mathrm{wt}_H(u) = |\{j \in \{1, \dots, n\} : u_j \ne 0\}|$:
1. The expected character value over a noisy codeword $x = b + e$ ($b \sim \operatorname{Unif}(B)$, $e \sim \mathcal{D}_\gamma^{\otimes n}$) factorizes as
   $$
   \mathbb{E}_{b \sim B,\, e \sim \mathcal{D}_\gamma^{\otimes n}}\bigl[\omega_q^{\langle u, b + e\rangle}\bigr] \;=\;
   \begin{cases}
   (1 - \gamma)^{\mathrm{wt}_H(u)}, & u \in B^\perp, \\
   0, & u \notin B^\perp.
   \end{cases}
   $$
2. These expectations describe the Fourier transform of a CLASSICAL probability
   distribution. They are not Born probabilities for a quantum Fourier measurement.
   In particular, writing $|B\rangle=|B|^{-1/2}\sum_{b\in B}|b\rangle$,
   a random translation gives $\rho_X=\mathbb E_e X^e|B\rangle\langle B|X^{-e}$.
   Since $F X^e|B\rangle$ has amplitude
   $|B^\perp|^{-1/2}\omega_q^{\langle u,e\rangle}$ on $B^\perp$ and zero elsewhere,
   $$P_X(u)=\mathbf 1_{u\in B^\perp}/|B^\perp|.$$
   This holds for ANY distribution of translations, even correlated ones.
3. The formula incorrectly assigned to translation in v1 instead applies to
   PHASE noise $Z^f|x\rangle=\omega_q^{\langle f,x\rangle}|x\rangle$ with the
   stated independent coordinate law. It also applies when independent
   translation noise is present, since translation cannot change the Fourier
   probabilities. Phase multiplication translates Fourier support:
   $$
   P_{XZ}(u \mid B, \gamma) \;=\; q^{-(n-d)} \sum_{v \in B^\perp} \left(1 - \frac{q-1}{q}\gamma\right)^{n - \mathrm{wt}_H(u - v)} \left(\frac{\gamma}{q}\right)^{\mathrm{wt}_H(u - v)}.
   $$
   For the positive-exponent QFT convention the support translates by $-f$;
   this symmetric noise law makes the displayed convolution identical.
4. A classical sampler loaded into basis states supplies
   $\rho_{\rm cl}=\sum_x P_X^{\rm classical}(x)|x\rangle\langle x|$.
   Every diagonal density operator has QFT probability $q^{-n}$ everywhere,
   because every squared QFT matrix entry is $q^{-n}$.

The three states $\rho_X$, $\mathbb E_f Z^f\rho_X Z^{-f}$ and
$\operatorname{diag}(\rho_X)$ have the SAME computational marginal. Therefore
even full knowledge of that marginal does not identify which Fourier law is
physically available. Tracing a register that records each codeword removes
the coherences needed by the coherent-coset argument; merely calling a
classical sampler reversibly does not erase that record for free.

Concrete falsifier: $q=3,n=2,B=\operatorname{span}(1,0),\gamma=1/2$.
Translation-only QFT has zero mass outside $B^\perp$, whereas the phase-noise
convolution has outside mass $1/3$ and probability $1/18$ at $(1,0)$.
The incoherent source has outside mass $2/3$. At $\gamma=1$ the common
computational marginal is uniform on the whole ambient space, but the
translation-only coherent state STILL Fourier-samples the dual exactly.
This is a source-access difference, not a new algorithmic speedup.

## 3. Theorem 2 — Off-Dual Noise Invariance and On-Dual Weight-Stratified Window Acceptance

For any window $W \subset \mathbb{F}_q$ of size $R = |W|$ and probe $u \in \mathbb{F}_q^n$, define the noisy acceptance probability
$$
p_W(u \mid B, \gamma) \;:=\; \Pr_{b \sim \operatorname{Unif}(B),\, e \sim \mathcal{D}_\gamma^{\otimes n}}\bigl[\langle b + e, u\rangle \in W\bigr].
$$

**Theorem 2 (Exact Noisy Window Acceptance Dichotomy).**
1. **Universal Off-Dual Noise Invariance ($u \notin B^\perp$)**: For every $u \in \mathbb{F}_q^n \setminus B^\perp$ and every fixed error vector $e \in \mathbb{F}_q^n$, the affine map $b \mapsto \langle b, u\rangle + \langle e, u\rangle$ is $q^{d-1}$-to-$1$ onto $\mathbb{F}_q$. Therefore, for **all** $\gamma \in [0, 1]$ and all off-dual weights $\mathrm{wt}_H(u)$:
   $$
   p_W(u \mid B, \gamma) \;=\; \frac{R}{q} \qquad \forall u \in \mathbb{F}_q^n \setminus B^\perp.
   $$
2. **Exact On-Dual Weight-Power Law ($u \in B^\perp$)**: For every $u \in B^\perp$, $\langle b + e, u\rangle = \langle e, u\rangle \bmod q$ has non-trivial character expectations all equal to $(1 - \gamma)^{\mathrm{wt}_H(u)}$ by Theorem 1, so for every $z \in \mathbb{F}_q$,
   $$
   \Pr_{e \sim \mathcal{D}_\gamma^{\otimes n}}\bigl[\langle e, u\rangle = z\bigr] \;=\; \frac{1}{q} \;+\; (1 - \gamma)^{\mathrm{wt}_H(u)}\!\left(\mathbf{1}_{z = 0} - \frac{1}{q}\right),
   $$
   and summing over $z \in W$ yields the exact window acceptance probability
   $$
   p_W(u \mid B, \gamma) \;=\; \frac{R}{q} \;+\; (1 - \gamma)^{\mathrm{wt}_H(u)}\!\left(\mathbf{1}_{0 \in W} - \frac{R}{q}\right) \qquad \forall u \in B^\perp.
   $$

## 4. Theorem 3 — Dual Minimum Distance $d^\perp(B)$ Controls Maximum Noisy Parity-Check Bias

Let $d^\perp(B) := \min_{u \in B^\perp \setminus \{0\}} \mathrm{wt}_H(u)$ denote the minimum Hamming weight of a non-zero dual codeword in $B^\perp$.

**Theorem 3 (Dual Minimum-Distance Bias Frontier).**
Assume $B^\perp$ has a nonzero vector, $\gamma\in(0,1)$, and
$0<R<q$. The distinguishing bias vanishes off the dual and is strictly
decreasing in Hamming weight on its nonzero vectors, with maximum at
minimum-weight dual checks:
$$
\max_{u \in \mathbb{F}_q^n \setminus \{0\}} \Delta p_W(u; B, \gamma) \;=\; (1 - \gamma)^{d^\perp(B)}\,\left|\mathbf{1}_{0 \in W} - \frac{R}{q}\right|.
$$

For the full subspace $B=\mathbb F_q^n$, the nonzero dual is empty: all
nonzero probe biases are zero and $d^\perp$ is undefined (JSON null).
For empty/full windows every bias is zero; do not claim strict decrease.

## Research Use And Remaining Obligations

These are conditional channel identities and bounded explicit controls,
not a decoder or a no-go theorem for noisy hidden subspace algorithms.
Before exploiting the translation-robust readout, exhibit and cost a coherent
coset source for the actual unknown problem. If a generator for $B$ is already
explicitly given, computing its dual is classical linear algebra; the controls
must not be promoted to a quantum advantage. For phase noise, the dual-distance
bias of these individual classical probes does not exclude joint-sample,
chosen-query or collective quantum attacks. No source inverse, purification,
environment access or efficient hidden-subspace preparation is granted.

Run `python qsearch.py planted-qary-noisy-parity-check-likelihood-bridge` and
`node research/certificates/planted_qary_noisy_parity_check_likelihood_bridge_crosscheck.js`.
