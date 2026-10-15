# DCP Noisy-Fourier Quadrature Decoder, CNOT Tree-Merge Visibility Law, and Sign Disambiguation

## 1. Motivation and Scope

In `theorems/lattice_cube_dcp_readout.py`, compiling a public `CubeCosetSource` (`theorems/lattice_cube_coset_source.py`) produces an `OpaquePhaseBackend` whose emitted receipts carry a public Fourier label $k \in \mathbb{Z}_N$ ($N = (2 M_{\text{box}})^n$) and an opaque single-qubit phase state. Under the two-point cube promise with bad-register rate $p_{\text{bad}} \in [0, 1)$, averaging over the cell distribution at fixed label $k \in \mathbb{Z}_N$ yields the reduced single-qubit phase density matrix
$$
\rho(k; s, v_0) \;=\; \frac{1}{2}
\begin{pmatrix}
1 & v_0 e^{-2\pi i k s / N} \\
v_0 e^{2\pi i k s / N} & 1
\end{pmatrix},
\qquad v_0 \;=\; 1 - p_{\text{bad}},
$$
where $s = \operatorname{encode\_position}(\delta, M_{\text{box}}) \bmod N$ is the encoded signed box shift of the hidden partner difference $\delta \in (-M_{\text{box}}, M_{\text{box}})^n$.

The backend exposes two destructive quantum operations on live receipts:
1. `merge(left, right)`: applies a CNOT between two live phase registers followed by a computational-basis measurement $b \in \{0, 1\}$ on the target qubit, updating the surviving control qubit's label to $k_{\text{out}} = k_1 + (-1)^b k_2 \bmod N$;
2. `measure(receipt_id, axis)`: measures a live phase register in the Pauli $X$, $Y$, or $Z$ basis, returning $y \in \{0, 1\}$ (spin $z = 1 - 2y \in \{+1, -1\}$).

This note proves three exact theorems governing CNOT tree-merge visibility propagation, $\{X, Y\}$ quadrature sign disambiguation, and the exact classical matched-filter / log-likelihood decoder operating directly on `OpaquePhaseBackend`.

## 2. Theorem 1 — Exact CNOT Tree-Merge Visibility Multiplication Law

**Theorem 1 (Multiplicative Visibility Under CNOT Combination).**
Let $\rho_1 = \rho(k_1; s, v_1)$ and $\rho_2 = \rho(k_2; s, v_2)$ be two independent balanced phase-density registers over $\mathbb{Z}_N$. Under the CNOT + target-$Z$ measurement channel (`OpaquePhaseBackend.merge`):
1. Both measurement branches $b \in \{0, 1\}$ occur with exact probability
   $$
   \Pr[b = 0] \;=\; \Pr[b = 1] \;=\; \frac{1}{2},
   $$
   independently of $k_1, k_2, s, v_1, v_2$.
2. Conditioned on branch $b \in \{0, 1\}$, the post-measurement control register has public label $k_{\text{out}} = k_1 + (-1)^b k_2 \bmod N$ and exact density matrix
   $$
   \rho_{\text{out}} \;=\; \rho\bigl(k_1 + (-1)^b k_2;\; s,\; v_1 v_2\bigr),
   $$
   with multiplied visibility $v_{\text{out}} = v_1 v_2$.
3. Consequently, a complete binary CNOT merge tree of depth $d \ge 0$ consumes $2^d$ independent original source registers of initial visibility $v_0 = 1 - p_{\text{bad}}$ and produces one depth-$d$ receipt with exact visibility
   $$
   v_d \;=\; v_0^{2^d} \;=\; (1 - p_{\text{bad}})^{2^d}.
   $$

*Proof.*
In the computational basis $\{|00\rangle, |01\rangle, |10\rangle, |11\rangle\}$, $\rho_1 \otimes \rho_2$ has diagonal entries $1/4$. Applying $\operatorname{CNOT}_{1 \to 2}$ swaps $|10\rangle \leftrightarrow |11\rangle$. Projecting the second qubit onto $|b\rangle\langle b|$ ($b \in \{0, 1\}$) extracts the $2 \times 2$ block $B_b$ on the first qubit:
$$
B_0 \;=\; \frac{1}{4}
\begin{pmatrix}
1 & v_1 v_2 e^{-2\pi i (k_1 + k_2) s / N} \\
v_1 v_2 e^{2\pi i (k_1 + k_2) s / N} & 1
\end{pmatrix},
\qquad
B_1 \;=\; \frac{1}{4}
\begin{pmatrix}
1 & v_1 v_2 e^{-2\pi i (k_1 - k_2) s / N} \\
v_1 v_2 e^{2\pi i (k_1 - k_2) s / N} & 1
\end{pmatrix}.
$$
Thus $\operatorname{Tr}(B_0) = \operatorname{Tr}(B_1) = 1/2$, and dividing $B_b$ by $\operatorname{Tr}(B_b) = 1/2$ yields $\rho(k_1 + (-1)^b k_2; s, v_1 v_2)$. Induction over a binary tree of depth $d$ gives $v_d = v_0^{2^d}$. $\square$

## 3. Theorem 2 — Quadrature $\{X, Y\}$ Orthogonality and Oriented Shift Recovery

For a live receipt with label $k \in \mathbb{Z}_N$ and state $\rho(k; s, v_d)$, measuring in Pauli axis $A \in \{X, Y\}$ produces spin $z = 1 - 2y \in \{+1, -1\}$ with expectation
$$
\mathbb{E}[z \mid k, A = X] \;=\; v_d \cos\!\left(\frac{2\pi k s}{N}\right),
\qquad
\mathbb{E}[z \mid k, A = Y] \;=\; v_d \sin\!\left(\frac{2\pi k s}{N}\right).
$$
Define the basis waveform $\phi_X(\theta) = \cos(2\pi \theta)$ and $\phi_Y(\theta) = \sin(2\pi \theta)$.

**Theorem 2 (Quadrature Correlation Kernel and Sign Disambiguation).**
1. **Sign ambiguity of $X$-only measurement**: Under $X$-only measurement ($A = X$), the expected correlation against candidate shift $s' \in \mathbb{Z}_N$ over uniform $k \sim \mathbb{Z}_N$ is
   $$
   \mathbb{E}_{k \sim \mathbb{Z}_N}\bigl[z \cos(2\pi k s' / N) \mid A = X\bigr]
   \;=\; \frac{v_d}{2}\bigl(\mathbf{1}_{s' \equiv s \pmod N} + \mathbf{1}_{s' \equiv -s \pmod N}\bigr),
   $$
   which is symmetric under $s' \leftrightarrow -s' \bmod N$ and cannot distinguish $\delta$ from $-\delta$.
2. **Exact Kronecker delta of balanced $\{X, Y\}$ quadrature measurement**: When the measurement axis $A \in \{X, Y\}$ is chosen with equal weight $1/2$ (or deterministically paired across $\{X, Y\}$), the expected quadrature correlation score $S(s') = z \phi_A(k s' / N)$ satisfies
   $$
   \mu(s') \;:=\; \mathbb{E}_{k \sim \mathbb{Z}_N,\, A \sim \{X, Y\}}\bigl[z \phi_A(k s' / N)\bigr]
   \;=\; \frac{v_d}{2 N} \sum_{k=0}^{N-1} \cos\!\left(\frac{2\pi k (s - s')}{N}\right)
   \;=\; \frac{v_d}{2}\,\delta_{s, s'}
   $$
   for **every** $s, s' \in \mathbb{Z}_N$.
3. **Exact single-shot variance**: Under uniform $k \sim \mathbb{Z}_N$ and balanced $A \sim \{X, Y\}$, the second moment of $S(s') = z \phi_A(k s' / N)$ is identically
   $$
   \mathbb{E}\bigl[S(s')^2\bigr]
   \;=\; \mathbb{E}_{k \sim \mathbb{Z}_N}\!\left[\frac{1}{2}\cos^2\!\left(\frac{2\pi k s'}{N}\right) + \frac{1}{2}\sin^2\!\left(\frac{2\pi k s'}{N}\right)\right]
   \;=\; \frac{1}{2}
   $$
   for **all** $s' \in \mathbb{Z}_N$ (because $\cos^2 \theta + \sin^2 \theta = 1$ pointwise). Consequently,
   $$
   \operatorname{Var}\bigl(S(s)\bigr) \;=\; \frac{1}{2} - \frac{v_d^2}{4},
   \qquad
   \operatorname{Var}\bigl(S(s')\bigr) \;=\; \frac{1}{2} \quad (s' \ne s).
   $$

## 4. Theorem 3 — Raw-Copy Sample Efficiency Frontier Across Merge Depths

**Theorem 3 (Depth-0 vs Depth-$d$ Quadrature SNR Per Raw Source Preparation).**
Suppose a budget of $M_{\text{raw}}$ original source preparations is partitioned into $M_d = M_{\text{raw}} / 2^d$ depth-$d$ CNOT merge trees ($d \ge 0$), each measured once in the $\{X, Y\}$ quadrature basis. The empirical average $\widehat{C}_d(s') = \frac{1}{M_d}\sum_{m=1}^{M_d} S_m(s')$ has false-target signal-to-noise ratio
$$
\operatorname{SNR}_d(M_{\text{raw}})
\;:=\; \frac{\bigl(\mathbb{E}[\widehat{C}_d(s)] - \mathbb{E}[\widehat{C}_d(s')]\bigr)^2}{\operatorname{Var}(\widehat{C}_d(s'))}
\;=\; \frac{(v_d / 2)^2}{1 / (2 M_d)}
\;=\; \frac{M_{\text{raw}}}{2^{d+1}}\,(1 - p_{\text{bad}})^{2^{d+1}}.
$$
For every $p_{\text{bad}} \in [0, 1)$ and every merge depth $d \ge 1$,
$$
\frac{\operatorname{SNR}_d(M_{\text{raw}})}{\operatorname{SNR}_0(M_{\text{raw}})}
\;=\; 2^{-d}\,(1 - p_{\text{bad}})^{2^{d+1} - 2}
\;\le\; 2^{-d} \;<\; 1.
$$
Thus, when final readout is single-qubit Pauli measurement without coherent multi-stage label targeting, unmerged depth-$0$ quadrature decoding strictly dominates depth-$d \ge 1$ CNOT tree merging per raw source preparation.
