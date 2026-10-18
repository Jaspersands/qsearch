# Product-Group Sine-Window Source Coordinate-Marginal Dephasing and Full-Vector Subset-Sum Equivalence Obstruction

## 1. Motivation and Scope

In `theorems/lattice_product_phase_source.py`, the public sine-localized lattice parent (`theorems/lattice_sine_window_source.py`, `research/LATTICE_SINE_WINDOW_SOURCE.md`) is read out via $n$ local coordinate Fourier transforms $\mathrm{QFT}_{q}^{\otimes n}$ of dyadic modulus $q = 2M = 2^L$ ($L = m + 1$), reducing the QFT controlled-phase gate count per parent preparation from $\binom{n L}{2}$ (for the cyclic $\mathrm{QFT}_{q^n}$ readout) to $n\binom{L}{2}$.

A natural algorithmic question on the clean / promised sine-window route is whether replacing the cyclic group $\mathbb{Z}_{q^n}$ with the product group $\mathbb{Z}_q^n$ enables **coordinate-by-coordinate (divide-and-conquer) polynomial-time decoding**—for example, recovering or predicting $h_1 \in \mathbb{Z}_q$ using only coordinate-1 labels $k_1 \in \mathbb{Z}_q$ at cost $\mathrm{poly}(n, L, q)$ without solving an $n$-dimensional subset-sum problem over $\mathbb{Z}_q^n$.

This note proves three exact theorems establishing that:
1. Single-coordinate marginal readout on $\mathrm{QFT}_q^{\otimes n}$ samples is **identically maximally mixed ($\bar{\rho}_{k_1}(h) = I_2/2$)** whenever any auxiliary shift coordinate $h_2, \dots, h_n$ is non-zero modulo $q$.
2. Across $K$ product-group samples, the optimal quantum advantage for predicting $h_1 \bmod 2$ under a uniform prior $h \sim \mathrm{Unif}(\mathbb{Z}_q^n)$ requires full $n$-vector subset-sum cancellation $A(x - x') \equiv (q/2, 0, \dots, 0)^T \pmod q$, leaving the group size $|G| = q^n = (2M)^n$ and BCDV copy threshold $K_{\min} = \lceil \log_2(1 + 2\epsilon q^n) \rceil$ **strictly invariant** between cyclic and product-group readouts.
3. Postselecting product-group samples with zero auxiliary labels ($k_2 = \dots = k_n = 0 \pmod q$) restores scalar $h_1$ coherence but succeeds with probability $q^{-(n-1)} = 2^{-L(n-1)}$ per preparation.

## 2. Theorem 1 — Exact Single-Coordinate Marginal Dephasing Identity

Under the promised single-shift template of `theorems/lattice_product_phase_source.py` with visibility $v \in [0, 1]$ and parent displacement $h = (h_1, \dots, h_n) \in \mathbb{Z}_q^n$, each measured vector label $k = (k_1, \dots, k_n) \sim \mathrm{Unif}(\mathbb{Z}_q^n)$ leaves the conditional colour qubit in state
$$
\rho_k(h) \;=\; \frac{1}{2}\begin{pmatrix} 1 & v\,\omega_q^{-\langle k, h\rangle} \\ v\,\omega_q^{\langle k, h\rangle} & 1 \end{pmatrix}, \qquad \langle k, h\rangle \;=\; \sum_{i=1}^n k_i h_i \bmod q.
$$

**Theorem 1 (Exact Auxiliary-Coordinate Character Erasure).**
For any fixed shift $h = (h_1, h_{\text{aux}}) \in \mathbb{Z}_q \times \mathbb{Z}_q^{n-1}$ and any coordinate-1 label $k_1 \in \mathbb{Z}_q$, averaging $\rho_{(k_1, k_{\text{aux}})}(h)$ over the uniform auxiliary labels $k_{\text{aux}} = (k_2, \dots, k_n) \sim \mathrm{Unif}(\mathbb{Z}_q^{n-1})$ yields the exact marginal state:
$$
\bar{\rho}_{k_1}(h) \;:=\; \frac{1}{q^{n-1}} \sum_{k_{\text{aux}} \in \mathbb{Z}_q^{n-1}} \rho_{(k_1, k_{\text{aux}})}(h)
\;=\; \frac{1}{2}\begin{pmatrix} 1 & v_{\text{eff}}(h_{\text{aux}})\,\omega_q^{-k_1 h_1} \\ v_{\text{eff}}(h_{\text{aux}})\,\omega_q^{k_1 h_1} & 1 \end{pmatrix},
$$
where the effective marginal visibility is
$$
v_{\text{eff}}(h_{\text{aux}}) \;=\; v \cdot \prod_{i=2}^n \left(\frac{1}{q}\sum_{k_i=0}^{q-1} \omega_q^{-k_i h_i}\right) \;=\; v\,\mathbf{1}\bigl[h_2 \equiv \dots \equiv h_n \equiv 0 \pmod q\bigr].
$$
In particular, for all $(q^{n-1} - 1)$ non-zero auxiliary shifts $h_{\text{aux}} \neq 0 \pmod q$, $\bar{\rho}_{k_1}(h) = \frac{1}{2}I_2$ is independent of $h_1$ and $k_1$, with trace distance $0$ from the maximally mixed state.

## 3. Theorem 2 — $K$-Copy Coordinate-1 Parity Invariance and Subset-Sum Equivalence

Suppose a receiver collects $K$ independent product-group samples with label matrix $A = [k^{(1)}, \dots, k^{(K)}] \in \mathbb{Z}_q^{n \times K}$ to predict the first-coordinate parity $h_1 \bmod 2$ under uniform prior $h \sim \mathrm{Unif}(\mathbb{Z}_q^n)$ and original independent $Z$ visibility $v \in [0, 1]$.

**Theorem 2 (Full-Vector Subset-Sum Requirement and Cyclic-vs-Product Copy Threshold Invariance).**
1. Averaging the $K$-copy state $\bigotimes_{r=1}^K \rho_{k^{(r)}}(h)$ over $h \in \mathbb{Z}_q^n$ conditioned on $h_1 \equiv 0 \pmod 2$ versus $h_1 \equiv 1 \pmod 2$ annihilates every off-diagonal pair $(x, x') \in \{0, 1\}^K \times \{0, 1\}^K$ unless the **entire $n$-component vector difference** matches $h^* = (q/2, 0, \dots, 0)^T \in \mathbb{Z}_q^n$:
   $$
   \bigl(\rho_{\text{even}}^{(K)}(A) - \rho_{\text{odd}}^{(K)}(A)\bigr)[x, x']
   \;=\; \frac{2}{2^K}\,v^{\mathrm{wt}_H(x \oplus x')}\,\mathbf{1}\bigl[A(x - x') \equiv (q/2, 0, \dots, 0)^T \pmod q\bigr].
   $$
2. Because any nonzero signed difference $d = x - x' \in \{-1, 0, 1\}^K \setminus \{0\}$ has at least one unit entry $\pm 1 \in \mathbb{Z}_q^\times$, $A d \bmod q$ is uniformly distributed over $\mathbb{Z}_q^n$ of size $|G_{\text{prod}}| = q^n = (2M)^n = |G_{\text{cyclic}}|$. Consequently, the source-averaged optimal quantum parity advantage bound
   $$
   \mathbb{E}_A\bigl[\mathrm{Adv}_{\text{opt}}(A)\bigr] \;\le\; \min\!\left(\frac{1}{2},\; \frac{(1 + v)^K - 1}{2\,q^n}\right)
   $$
   and the minimum copy count $K_{\min}(n, L, \epsilon, v)$ are **identical** for the product-group source $\mathbb{Z}_q^n$ and the unlifted cyclic source $\mathbb{Z}_{q^n}$.

## 4. Theorem 3 — Auxiliary-Zero Postselection Sample Complexity

**Theorem 3 (Subspace Postselection Tradeoff).**
If a receiver postselects product-group preparations whose measured auxiliary coordinates vanish ($k_2 \equiv \dots \equiv k_n \equiv 0 \pmod q$), each retained sample is a valid 1D phase state for $h_1 \in \mathbb{Z}_q$ with full visibility $v$, reducing the conditional subset-sum group size from $q^n$ to $q$. However, because $k \sim \mathrm{Unif}(\mathbb{Z}_q^n)$, the single-shot acceptance probability is
$$
P_{\text{accept}}(n, q) \;=\; q^{-(n-1)} \;=\; (2M)^{-(n-1)} \;=\; 2^{-L(n-1)},
$$
so acquiring $K_1$ retained 1D samples requires expected total preparations $\mathbb{E}[N_{\text{prep}}] = K_1\,q^{n-1} = K_1\,2^{L(n-1)}$.
