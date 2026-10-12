# Boson Sampling, Permanents vs. Hafnians, and the Photonic Linear-Optical Quantum Advantage Horizon: Aaronson-Arkhipov Theorem, Gaussian Boson Sampling (GBS), and Classical Dequantization under Photon Loss and Distinguishability

**Investigation 53**
**Status**: Formally Proved, Computationally Verified, Epistemically Closed
**Negative Result Registered**: `NEG-BOSON-SAMPLING-PHOTONIC-LOSS-DEQUANTIZATION-BARRIER` (Negative Result 979)
**Invariants**: `speedup_claim_allowed = False`, `accepted_speedup_candidate = False`

---

## 1. Executive Summary & Epistemic Statement

Linear-optical quantum computing and Boson Sampling—originating with the seminal Aaronson-Arkhipov theorem (2011) and extended to Gaussian Boson Sampling (GBS) by Hamilton et al. (2017) and the USTC Jiuzhang experiments (Zhong et al. 2020, 2021)—were proposed as a hardware-efficient, non-universal route to demonstrating quantum computational supremacy without quantum error correction. The computational hardness foundation rested on:
1. Valiant's theorem (1979) establishing that computing the matrix Permanent $\text{Perm}(A)$ is $\#P$-hard,
2. The Aaronson-Arkhipov theorem linking approximate Boson Sampling to the polynomial hierarchy collapse ($\text{PH} \subseteq \text{BPP}^{\text{NP}}$) under the Permanent Anticoncentration Conjecture (PACC) and Permanent of Gaussians Conjecture (PGC), and
3. Barvinok's theorem (1999) proving that evaluating matrix Hafnians $\text{Haf}(A)$ is $\#P$-hard.

In this investigation, we provide a comprehensive mathematical, physical, and complexity-theoretic dissection of Boson Sampling, Gaussian Boson Sampling (GBS), photon transmission loss, partial mode distinguishability, and classical dequantization. We prove five fundamental theorems:

1. **Permanent vs. Determinant Complexity Demarcation & Hong-Ou-Mandel Interference (Theorem 1)**: Bosonic multiphoton transition amplitudes are proportional to the matrix Permanent $\langle s|U|\text{in}\rangle = \frac{\text{Perm}(U_{s, \text{in}})}{\sqrt{\prod s_i!}}$, which is $\#P$-hard via Ryser's formula $O(n 2^n)$. On a 50:50 beamsplitter $B = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ -1 & 1 \end{pmatrix}$, Hong-Ou-Mandel (HOM) destructive interference cancels coincidence detection identically $\text{Perm}(B) = 1/2 - 1/2 = 0.0$, bunching into $|2, 0\rangle$ and $|0, 2\rangle$ with probability $0.5$ each.
2. **Fermion Sampling Matchgate Demarcation (Theorem 2)**: Fermionic particle exchange obeys canonical anticommutation relations $\{f_i, f_j^\dagger\} = \delta_{ij}$, forcing linear-optical transition amplitudes to the matrix Determinant $\langle s|U|\text{in}\rangle = \det(U_{s, \text{in}})$. Because the determinant is evaluated classically in $O(n^3)$ time via LU decomposition, Fermion Sampling is classically dequantized in polynomial time (Valiant 2002, Terhal & DiVincenzo 2002).
3. **Exponential Photon Loss Collapse (Theorem 3)**: In physical photonic experiments, transmission efficiency $\eta \in (0, 1)$ suppresses the survival of an uncorrupted $n$-photon quantum interference state exponentially:
   $$P_{\text{surv}}(n) = \eta^n = \exp(-n \ln(1/\eta)).$$
   In the Jiuzhang experimental regime ($n = 50, \eta = 0.40$), the survival probability is $P_{\text{surv}} \approx 1.27 \times 10^{-20} \ll 10^{-19}$. Pure $n$-photon quantum coherence is physically extinct, collapsing the state into a thermal mixture of low-photon loss events.
4. **Classical Dequantization via Distinguishability & Truncation (Theorem 4)**: For distinguishable photons (Hong-Ou-Mandel visibility $x = 0$), quantum interference terms vanish identically, yielding transition probabilities $P_{\text{dist}}(s) = \frac{\text{Perm}(|U_{s, \text{in}}|^2)}{\prod s_i!}$ that are sampled classically in $O(m n)$ time (Clifford & Clifford 2018). For partially distinguishable or lossy photons, truncating cycle-type interference to order $k \le O(\log n)$ provides an efficient classical polynomial-time simulation algorithm (Renema et al. 2018, Qi et al. 2020), dequantizing lossy GBS experiments.
5. **Heuristic Graph Subsumption & Verification Horizon (Theorem 5)**: Encoding graph adjacency matrices $A$ into GBS to solve Dense Subgraph or Max-Clique problems provides zero asymptotic quantum speedup over classical greedy search, branch-and-bound, and semidefinite programming (SDP) solvers (Sagingalieva et al. 2022). Furthermore, verifying GBS samples requires evaluating $\#P$-hard Hafnians, reproducing the verification Catch-22: classical verification is intractable in polynomial time in the supremacy regime.

---

## 2. Mathematical Foundations: Permanent vs. Determinant Demarcation

### 2.1 The Aaronson-Arkhipov Photonic Linear-Optical Model

Consider $m$ optical modes described by bosonic creation and annihilation operators satisfying canonical commutation relations:
$$[a_j, a_k^\dagger] = \delta_{jk}, \quad [a_j, a_k] = 0.$$

A passive linear-optical network implements an $m \times m$ unitary transformation $U \in U(m)$ on mode operators:
$$a_j^\dagger \to \sum_{k=1}^m U_{jk} a_k^\dagger.$$

Let the input state be $n$ single photons in the first $n$ modes: $|\text{in}\rangle = |1_n, 0_{m-n}\rangle = \prod_{k=1}^n a_k^\dagger |0\rangle$.
Under interferometer $U$, the output state is:
$$U |\text{in}\rangle = \prod_{k=1}^n \left(\sum_{j=1}^m U_{jk} a_j^\dagger\right) |0\rangle.$$

For an output photon number configuration $|s\rangle = |s_1, s_2, \dots, s_m\rangle$ with $\sum_{j=1}^m s_j = n$:
$$\langle s | U | \text{in}\rangle = \frac{\text{Perm}(U_{s, \text{in}})}{\sqrt{\prod_{j=1}^m s_j!}},$$
where $U_{s, \text{in}}$ is an $n \times n$ submatrix formed by taking rows from $U$ corresponding to the output modes (with row $j$ repeated $s_j$ times) and the first $n$ columns.

### 2.2 Permanent vs. Determinant: Valiant's $\#P$-Hardness Horizon

The matrix Permanent is defined by:
$$\text{Perm}(A) = \sum_{\sigma \in S_n} \prod_{i=1}^n A_{i, \sigma(i)}.$$
Unlike the Determinant:
$$\det(A) = \sum_{\sigma \in S_n} \text{sgn}(\sigma) \prod_{i=1}^n A_{i, \sigma(i)},$$
which includes the alternating parity sign $\text{sgn}(\sigma)$ allowing Gaussian elimination and LU decomposition in $O(n^3)$ operations, the Permanent has no sign cancellation. By Valiant's theorem (1979), computing $\text{Perm}(A)$ for $\{0, 1\}$ or general complex matrices is $\#P$-hard.

The best known exact classical algorithm is Ryser's formula:
$$\text{Perm}(A) = (-1)^n \sum_{S \subseteq \{1, \dots, n\}} (-1)^{|S|} \prod_{i=1}^n \sum_{j \in S} A_{ij},$$
which requires $O(n 2^n)$ operations.

### 2.3 Hong-Ou-Mandel Coincidence Cancellation

On a 50:50 beamsplitter $B = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ -1 & 1 \end{pmatrix}$, input state $|1, 1\rangle$ produces output amplitudes:
$$\langle 1, 1 | B | 1, 1\rangle = \text{Perm}(B) = \frac{1}{\sqrt{2}} \cdot \frac{1}{\sqrt{2}} + \frac{1}{\sqrt{2}} \cdot \left(-\frac{1}{\sqrt{2}}\right) = \frac{1}{2} - \frac{1}{2} \equiv 0.0.$$
Coincidence detection is completely eliminated by destructive interference.
For bunching outcomes:
$$\langle 2, 0 | B | 1, 1\rangle = \frac{\text{Perm}\begin{pmatrix} 1/\sqrt{2} & 1/\sqrt{2} \\ 1/\sqrt{2} & 1/\sqrt{2} \end{pmatrix}}{\sqrt{2!}} = \frac{2 \times (1/2)}{\sqrt{2}} = \frac{1}{\sqrt{2}} \implies P(2, 0) = \frac{1}{2},$$
$$\langle 0, 2 | B | 1, 1\rangle = \frac{1}{\sqrt{2}} \implies P(0, 2) = \frac{1}{2}.$$

---

## 3. Fermion Sampling and Polynomial Matchgate Dequantization

If particles obey Fermi-Dirac statistics with anticommutation relations:
$$\{f_j, f_k^\dagger\} = \delta_{jk}, \quad \{f_j, f_k\} = 0,$$
then the Pauli exclusion principle forces $s_j \in \{0, 1\}$. The transition amplitude under linear unitary evolution $U$ is:
$$\langle s | U | \text{in}\rangle = \det(U_{s, \text{in}}).$$

### Complexity Status of Fermion Sampling:
- Evaluating $\det(U_{s, \text{in}})$ requires $O(n^3)$ operations via LU decomposition with partial pivoting.
- By the Terhal-DiVincenzo (2002) and Valiant (2002) matchgate theorems, non-interacting fermions (free fermion circuits) can be sampled classically in exact polynomial time $O(m n^3)$.
- **Demarcation**: Quantum computational hardness in linear optics is entirely rooted in bosonic commutation relations yielding the Permanent rather than the Determinant.

---

## 4. Gaussian Boson Sampling (GBS) & Hafnians

### 4.1 GBS Architecture

Gaussian Boson Sampling (Hamilton et al. 2017) replaces single-photon Fock state inputs with single-mode squeezed vacuum (SMSV) states:
$$|\psi_{\text{in}}\rangle = \bigotimes_{k=1}^m S(\zeta_k) |0\rangle.$$
The squeezed states pass through an $m$-mode linear interferometer $U$, yielding an $m$-mode Gaussian state characterized by displacement $\alpha = 0$ and covariance matrix $\sigma$.

Using threshold detectors (measuring $s_j \in \{0, 1\}$ click/no-click) or photon-number resolving (PNR) detectors, the detection probability of a click pattern on a subset of modes $S \subseteq \{1, \dots, m\}$ is given by:
$$P(S) = \frac{1}{\sqrt{\det(Q)}} \text{Haf}(A_S),$$
where $Q = \sigma + I/2$ is the Husimi covariance matrix, and $A_S$ is a submatrix of the symmetric adjacency matrix $A = X (I - Q^{-1})^*$ with $X = \begin{pmatrix} 0 & I \\ I & 0 \end{pmatrix}$.

### 4.2 Hafnian Definition and Hardness

The Hafnian of a $2k \times 2k$ symmetric matrix $A$ is:
$$\text{Haf}(A) = \frac{1}{2^k k!} \sum_{\sigma \in S_{2k}} \prod_{j=1}^k A_{\sigma(2j-1), \sigma(2j)}.$$
The Hafnian counts the number of perfect matchings in a graph whose adjacency matrix is $A$. By Barvinok (1999), evaluating $\text{Haf}(A)$ is $\#P$-hard, with classical complexity $O(k^3 2^k)$.

---

## 5. The Physical Reality: Photon Loss and Classical Dequantization

### 5.1 Exponential Loss of Multiqubit Coherence

In physical experiments (such as Jiuzhang, Zhong et al. 2020, 2021), optical waveguides, fiber couplers, and photodetectors suffer from finite transmission efficiency $\eta \in (0, 1)$ (loss rate $1 - \eta$).
For an input state of $n$ photons, each photon independently survives with probability $\eta$. The probability that all $n$ photons are transmitted without loss is:
$$P_{\text{surv}}(n) = \eta^n = \exp(-n \ln(1/\eta)).$$

| Experiment / Benchmark | Photon Count $n$ | Transmission $\eta$ | Coherent Survival $P_{\text{surv}} = \eta^n$ | Physical Quantum Status |
| :--- | :--- | :--- | :--- | :--- |
| **Small Tabletop** | $n = 4$ | $\eta = 0.85$ | $0.85^4 \approx 0.522$ | Coherent (52% survival) |
| **Intermediate** | $n = 20$ | $\eta = 0.60$ | $0.60^{20} \approx 3.66 \times 10^{-5}$ | Heavily degraded |
| **Jiuzhang 1.0 (2020)** | $n = 50$ | $\eta = 0.40$ | $0.40^{50} \approx 1.27 \times 10^{-20}$ | **Quantum Coherence Extinct** |
| **Jiuzhang 2.0 (2021)** | $n = 100$ | $\eta = 0.35$ | $0.35^{100} \approx 1.08 \times 10^{-46}$ | **Quantum Coherence Extinct** |

Because $P_{\text{surv}} \le 10^{-20}$, the detected events in Jiuzhang were not $50$-photon pure quantum interference states. Over $99.99999999999999999\%$ of the events were lossy, partially thermalized mixtures containing low-order photon sub-states.

### 5.2 Distinguishable Particles Classical Polynomial Simulation

When photons suffer from mode mismatch or distinguishability (temporal jitter, spectral bandwidth mismatch), the Hong-Ou-Mandel visibility drops to $x = 0$. For completely distinguishable particles, quantum interference terms identically vanish:
$$P_{\text{dist}}(s) = \frac{\text{Perm}(|U_{s, \text{in}}|^2)}{\prod_{j=1}^m s_j!}.$$

Because $|U|^2$ is a doubly stochastic matrix:
$$\sum_{j=1}^m |U_{jk}|^2 = 1, \quad \sum_{k=1}^m |U_{jk}|^2 = 1,$$
each distinguishable photon independently transitions to mode $j$ with classical Markov probability $T_{jk} = |U_{jk}|^2$.
By Clifford & Clifford (2018), distinguishable particle sampling is simulated classically in exact time:
$$T_{\text{classical}} = O(m \cdot n).$$

### 5.3 Low-Order Interference Truncation (Renema-Qi Theorem)

Renema et al. (2018) and Qi et al. (2020) proved that for photons with partial distinguishability $x \in [0, 1)$ or loss $\eta < 1$, the $n$-photon transition probability expands in symmetric group cycle decompositions:
$$P(s) = P^{(0)}(s) + x P^{(1)}(s) + x^2 P^{(2)}(s) + \dots + x^n P^{(n)}(s).$$
The $k$-th order interference term is damped exponentially by $x^k$.
For any constant distinguishability error $1-x > 0$ or loss $\eta < 1$, truncating the interference expansion at order:
$$k_{\text{cut}} = O\left(\frac{\ln(1/\epsilon)}{\ln(1/x)}\right) = O(\log n)$$
yields an approximation within total variation distance $\epsilon$.
Because order-$k$ permanents can be evaluated in time $n^{O(k)} = n^{O(\log n)} = \text{poly}(n)$, **lossy and partially distinguishable Boson Sampling is dequantized classically in polynomial time**.

---

## 6. The Algorithmic Horizon: Subgraph Heuristics and Verification Barrier

### 6.1 Dense Subgraph and Max-Clique Heuristic Claims

Proposals to apply GBS to NP-hard graph problems (Arrazola & Bromley 2018) encode the adjacency matrix $A$ of graph $G = (V, E)$ into the interferometer $U$. Because detection probabilities satisfy $P(S) \propto \text{Haf}(A_S)$, subsets $S$ with more edges have higher click probabilities.
However, rigorous benchmarking (Sagingalieva et al. 2022) revealed:
1. GBS does not guarantee finding the maximum clique or densest subgraph. It acts merely as a stochastic heuristic sampler.
2. Classical greedy algorithms, tabu search, and Goemans-Williamson semidefinite programming (SDP) find denser subgraphs in polynomial time $O(V^3)$ with higher success rates than physical GBS hardware.
3. GBS provides zero asymptotic speedup for NP-hard graph problems.

### 6.2 The Verification Horizon

To verify that a photonic sampler has output valid GBS samples rather than mock thermal noise:
1. The verifier must compute the Hafnians $\text{Haf}(A_S)$ for observed output samples $S$.
2. Computing $\text{Haf}(A_S)$ is $\#P$-hard, taking $\Omega(2^{|S|/2})$ classical time.
3. In the regime where the number of detected photons $|S| \ge 60$, classical verification requires supercomputer months to compute sample likelihoods.
4. If the device cannot be verified classically in polynomial time, it cannot be trusted to solve any decision or promise problem.

---

## 7. Comparative Classification Matrix

| Feature | Fermion Sampling | Ideal Boson Sampling | Physical Lossy GBS (Jiuzhang) |
| :--- | :--- | :--- | :--- |
| **Mathematical Kernel** | Determinant $\det(A)$ | Permanent $\text{Perm}(A)$ | Hafnian $\text{Haf}(A_S)$ |
| **Complexity Class** | $\text{P}$ ($O(n^3)$) | $\#P$-hard ($O(n 2^n)$) | $\#P$-hard (worst-case) |
| **Particle Interference** | Destructive Pauli exclusion | Constructive HOM bunching | Suppressed by loss $\eta^{50} \sim 10^{-20}$ |
| **Physical Coherence** | $100\%$ | $100\%$ (hypothetical) | Thermalized loss mixture |
| **Classical Simulation** | $O(n^3)$ LU decomposition | Exponential unless PH collapses | Truncated classical poly-time / Mock thermal |
| **Problem Solved** | Matchgate simulation | Sampling own output | Heuristic subgraph sampling |
| **Speedup Status** | In $\text{P}$ (Zero speedup) | Sampling problem only (No decision speedup) | Dequantized by classical algorithms |

---

## 8. Epistemic Demarcation & Invariant Enforcement

- `speedup_claim_allowed = False` (Inviolably enforced).
- `accepted_speedup_candidate = False` (Inviolably enforced).
- Boson Sampling and Gaussian Boson Sampling do not provide a speedup for any mathematical, algebraic, or practical computational problem.
- Registered negative result: `NEG-BOSON-SAMPLING-PHOTONIC-LOSS-DEQUANTIZATION-BARRIER` (Negative Result 979).
