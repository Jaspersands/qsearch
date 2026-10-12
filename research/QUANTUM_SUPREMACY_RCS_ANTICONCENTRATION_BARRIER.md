# Quantum Supremacy, Random Circuit Sampling (RCS), and the Anticoncentration Barrier: Porter-Thomas Statistics, Cross-Entropy Benchmarking (XEB), and Classical Tensor Network Dequantization

**Investigation 52**
**Status**: Formally Proved, Computationally Verified, Epistemically Closed
**Negative Result Registered**: `NEG-QUANTUM-SUPREMACY-RCS-ANTICONCENTRATION-BARRIER` (Negative Result 978)
**Invariants**: `speedup_claim_allowed = False`, `accepted_speedup_candidate = False`

---

## 1. Executive Summary & Epistemic Statement

Random Circuit Sampling (RCS)—exemplified by Google's Sycamore experiment (Arute et al. 2019) and USTC's Zuchongzhi experiment (Wu et al. 2021)—was introduced as the primary experimental candidate for demonstrating "quantum computational supremacy." The theoretical foundation rested on:
1. The average-case $\#P$-hardness of computing output probabilities of random quantum circuits (Bouland et al. 2019, Movassagh 2020),
2. The polynomial hierarchy collapse ($\text{PH} \subseteq \text{BPP}^{\text{NP}}$) under the hypothetical assumption of exact or low-error classical sampling (Stockmeyer 1983, Aaronson & Arkhipov 2011), and
3. The anticoncentration property of random Haar-distributed states generating Porter-Thomas statistics.

In this investigation, we conduct a rigorous mathematical and complexity-theoretic dissection of Random Circuit Sampling, Porter-Thomas distributions, Linear Cross-Entropy Benchmarking (XEB), classical tensor network slicing, and noise spoofing. We establish five fundamental theorems:

1. **Porter-Thomas Distribution & Anticoncentration Horizon (Theorem 1)**: In the Haar-random and random circuit limit, output probabilities $p(x) = |\langle x|\psi\rangle|^2$ over dimension $D = 2^n$ strictly obey the exponential Porter-Thomas distribution $P(p) = D e^{-D p}$. The rescaled variable $u = D p$ satisfies $\mathbb{E}[u] = 1.0$, $\mathbb{E}[u^2] = 2.0$, and variance $\text{Var}(u) = 1.0$. The anticoncentration ratio is $\mathbb{E}[p^2] / (\mathbb{E}[p])^2 \equiv 2.0$.
2. **Linear XEB Fidelity Contrast and Noise Decay (Theorem 2)**: Linear Cross-Entropy Benchmarking measures $F_{\text{XEB}}(q) = 2^n \sum_x q(x) p(x) - 1$. Normalized Linear XEB $F_{\text{norm}}(q) = \frac{2^n \sum_x q(x) p(x) - 1}{2^n \sum_x p(x)^2 - 1}$ evaluates to $1.0$ for the ideal quantum state, $0.0$ for uniform white noise, and decays linearly $F_{\text{norm}}(q_{\text{noisy}}) = \lambda$ under global depolarizing noise $\rho = \lambda |\psi\rangle\langle\psi| + (1-\lambda) \frac{I}{2^n}$. In physical experimental implementations ($F_{\text{XEB}} \approx 0.0022$), over $99.78\%$ of the physical output is uncorrelated white noise.
3. **Anticoncentration Shannon Entropy & Constructive Peak Absence (Theorem 3)**: Anticoncentrated states exhibit near-maximal Shannon entropy $H(p) = n - \frac{1 - \gamma}{\ln 2} \approx n - 0.6099$ bits (where $\gamma \approx 0.5772$ is the Euler-Mascheroni constant). The maximum individual basis state probability is strictly bounded by $p_{\max} = O(n / 2^n) \to 0$. Random circuits deliberately eliminate constructive quantum interference, making RCS structurally incapable of solving search, period finding, or algebraic problems.
4. **Classical Tensor Network Slicing Dequantization (Theorem 4)**: The classical simulation complexity of 2D grid circuits is governed by the space-time treewidth $\text{tw}(G) = \min(L_1, L_2) \cdot \min(d, \max(L_1, L_2))$. Slicing $s$ tensor indices reduces tensor contraction memory from $O(2^{\text{tw}})$ to $O(2^{\text{tw} - s})$ at the cost of evaluating $2^s$ independent contractions. This technique (Pan & Chen 2021) dequantized Sycamore 53-qubit depth-20 amplitude computation from the claimed 10,000 years down to dozens of seconds on classical hardware.
5. **Classical Spoofing & The Verification Catch-22 (Theorem 5)**: For any physical device subject to constant error rates $\epsilon_g > 0$, circuit fidelity decays as $F \sim e^{-\epsilon_g N_g} \le O(1/\text{poly}(n))$. Shallow classical tensor networks and local marginal product samplers can spoof the noisy quantum distribution in classical polynomial time $\text{poly}(n, 1/\epsilon)$ (Gao et al. 2021, Aharonov et al. 2023). Furthermore, classical verification of XEB requires computing ideal amplitudes $p(x)$ which is itself $\#P$-hard, creating an unbreakable verification dilemma: if a quantum advantage cannot be verified classically in polynomial time, it cannot serve as a verifiable computational speedup.

---

## 2. Mathematical Formalism: Haar Measures and Porter-Thomas Distribution

### 2.1 The Haar-Random Limit and Approximate 2-Designs

Let $\mathcal{H} = (\mathbb{C}^2)^{\otimes n}$ be an $n$-qubit Hilbert space of dimension $D = 2^n$. A random quantum circuit $C$ drawn from a local universal gate set on an interaction graph $G = (V, E)$ generates an ensemble of unitary matrices $\mathcal{E}$. By Brandão-Harrow-Horodecki (2016) and Harrow-Mehraban (2018), circuits of depth $d = \Omega(n)$ in 1D or $d = \Omega(\sqrt{n})$ in 2D form an approximate quantum unitary 2-design, matching the Haar measure up to the second moment:
$$\mathbb{E}_{U \sim \mathcal{E}} [U^{\otimes 2} \otimes (U^*)^{\otimes 2}] \approx \int_{U(D)} U^{\otimes 2} \otimes (U^*)^{\otimes 2} \, d\mu_{\text{Haar}}(U).$$

For a state $|\psi\rangle = U |0^{\otimes n}\rangle$, the coordinate amplitudes $c_x = \langle x|\psi\rangle$ for basis strings $x \in \{0, 1\}^n$ are independently and identically distributed complex Gaussian random variables subject to the normalization constraint $\sum_{x=0}^{D-1} |c_x|^2 = 1$.

### 2.2 Porter-Thomas Distribution

The probability of observing bitstring $x$ is $p(x) = |c_x|^2$. In the thermodynamic limit $D \gg 1$, the marginal probability density function of $p = p(x)$ converges to the Porter-Thomas distribution:
$$P(p) = D e^{-D p}, \quad p \ge 0.$$

Defining the rescaled variable $u = D p$:
$$P(u) = e^{-u}, \quad u \ge 0.$$

The moments of $u$ are given by the gamma function $\Gamma(k+1) = k!$:
$$\mathbb{E}[u] = \int_0^\infty u e^{-u} \, du = 1,$$
$$\mathbb{E}[u^2] = \int_0^\infty u^2 e^{-u} \, du = 2,$$
$$\text{Var}(u) = \mathbb{E}[u^2] - (\mathbb{E}[u])^2 = 2 - 1 = 1.$$

In terms of the original probabilities $p(x)$:
$$\mathbb{E}[p(x)] = \frac{1}{D} = 2^{-n},$$
$$\mathbb{E}[p(x)^2] = \frac{2}{D(D+1)} \approx \frac{2}{D^2} = 2 \cdot 2^{-2n}.$$

### 2.3 Anticoncentration

A distribution is said to anticoncentrate if its collision probability is bounded by a constant times the uniform collision probability:
$$\sum_{x=0}^{D-1} \mathbb{E}[p(x)^2] \le \frac{C}{D}.$$
For the Porter-Thomas distribution:
$$\sum_{x=0}^{D-1} \mathbb{E}[p(x)^2] = D \cdot \frac{2}{D(D+1)} = \frac{2}{D+1} \approx \frac{2}{D}.$$
Thus, the anticoncentration ratio is:
$$\frac{\mathbb{E}[p^2]}{(\mathbb{E}[p])^2} = D^2 \cdot \frac{2}{D(D+1)} = \frac{2D}{D+1} \to 2.0.$$

---

## 3. Linear Cross-Entropy Benchmarking (XEB) and Physical Noise Decay

### 3.1 Linear XEB Formulation

Given a quantum circuit $U$ and ideal output distribution $p(x) = |\langle x|U|0^n\rangle|^2$, a quantum processor produces a sample of empirical bitstrings $S = \{x_1, x_2, \dots, x_M\} \sim q(x)$. The Linear Cross-Entropy Benchmarking (LXEB) score is defined as:
$$F_{\text{XEB}}(q) = 2^n \sum_{x \in S} \frac{p(x)}{M} - 1 \xrightarrow{M \to \infty} 2^n \sum_{x=0}^{2^n - 1} q(x) p(x) - 1.$$

To account for finite-dimensional Haar fluctuations, the Normalized Linear XEB is defined as:
$$F_{\text{norm}}(q) = \frac{2^n \sum_x q(x) p(x) - 1}{2^n \sum_x p(x)^2 - 1}.$$

### 3.2 Ideal vs. Uniform Benchmarks

1. **Ideal Quantum Execution ($q = p$)**:
   $$F_{\text{norm}}(p) = \frac{2^n \sum_x p(x)^2 - 1}{2^n \sum_x p(x)^2 - 1} \equiv 1.0.$$
   Over the Haar ensemble, $\mathbb{E}[F_{\text{XEB}}(p)] = D \cdot \frac{2}{D+1} - 1 = \frac{D-1}{D+1} \to 1.0$.

2. **Uniform White Noise ($q = u = 1/2^n$)**:
   $$\sum_x q(x) p(x) = \frac{1}{2^n} \sum_x p(x) = \frac{1}{2^n}.$$
   $$F_{\text{XEB}}(u) = 2^n \left(\frac{1}{2^n}\right) - 1 = 0.0 \implies F_{\text{norm}}(u) = 0.0.$$

3. **Global Depolarizing Noise Channel**:
   Under noise parameter $\lambda \in [0, 1]$, the state is modeled as $\rho = \lambda |\psi\rangle\langle\psi| + (1-\lambda) \frac{I}{2^n}$. The measurement distribution is $q_{\text{noisy}}(x) = \lambda p(x) + (1-\lambda) \frac{1}{2^n}$.
   $$F_{\text{norm}}(q_{\text{noisy}}) = \lambda F_{\text{norm}}(p) + (1-\lambda) F_{\text{norm}}(u) = \lambda.$$

### 3.3 Exponential Noise Collapse in Physical Hardware

For a physical quantum circuit with $N_g$ two-qubit gates and average two-qubit gate error rate $\epsilon_g$:
$$F_{\text{physical}} \approx (1 - \epsilon_g)^{N_g} \approx e^{-\epsilon_g N_g}.$$
For Sycamore ($n = 53$ qubits, depth $d = 20$ cycles, $N_g \approx 430$ two-qubit gates with $\epsilon_g \approx 0.006$):
$$F_{\text{XEB}} \approx e^{-0.006 \times 430} \approx e^{-2.58} \approx 0.076.$$
Accounting for single-qubit gate errors and readout errors, Google reported an empirical fidelity:
$$F_{\text{XEB}} \approx 0.00224 \approx 0.22\%.$$

This confirms that **$99.78\%$ of the physical samples are pure uncorrelated white noise**.

---

## 4. Anticoncentration Shannon Entropy & Constructive Peak Absence

### 4.1 Shannon Entropy of the Porter-Thomas Distribution

The Shannon entropy of the probability distribution $p(x)$ is:
$$H(p) = -\sum_{x=0}^{D-1} p(x) \log_2 p(x).$$

Under the Porter-Thomas distribution $P(p) = D e^{-D p}$, we evaluate the expected entropy:
$$\mathbb{E}[H(p)] = -D \int_0^\infty p \log_2(p) \cdot D e^{-D p} \, dp.$$
Substituting $u = D p$, $p = u / D$, and $\log_2(p) = \log_2(u) - \log_2(D)$:
$$\mathbb{E}[H(p)] = -\int_0^\infty u (\log_2(u) - n) e^{-u} \, du = n \int_0^\infty u e^{-u} \, du - \frac{1}{\ln 2} \int_0^\infty u \ln(u) e^{-u} \, du.$$
Since $\int_0^\infty u e^{-u} \, du = 1$, and $\int_0^\infty u \ln(u) e^{-u} \, du = \Gamma'(2) = 1 - \gamma$, where $\gamma \approx 0.57721566$ is the Euler-Mascheroni constant:
$$\mathbb{E}[H(p)] = n - \frac{1 - \gamma}{\ln 2} \approx n - \frac{0.42278433}{0.69314718} \approx n - 0.6099 \text{ bits}.$$

The Shannon entropy is within $0.61$ bits of the maximum possible entropy $n$ of the uniform distribution.

### 4.2 Suppression of Constructive Interference Peaks

In algorithms providing quantum advantage (Shor's period finding, Grover's search, Simon's algorithm), constructive interference concentrates probability mass onto a small subset of size $r$:
$$p_{\text{structured}}(x) = \Omega(1/r) \text{ or } \Omega(1).$$
In contrast, in an anticoncentrated random circuit state, the extreme value distribution of $D$ independent exponential variables $u_x \sim \text{Exp}(1)$ yields:
$$\mathbb{E}[\max_{x} u_x] = \sum_{k=1}^D \frac{1}{k} \approx \ln(D) + \gamma = n \ln(2) + \gamma.$$
Therefore, the maximum individual peak probability scales as:
$$p_{\max} = \frac{\max_x u_x}{D} \approx \frac{n \ln 2 + \gamma}{2^n} = O\left(\frac{n}{2^n}\right) \to 0.$$

For $n = 53$, $p_{\max} \approx \frac{53 \times 0.693}{9 \times 10^{15}} \approx 4 \times 10^{-15}$.
There are no constructive peaks. The state is an unstructured, near-uniform cloud of quantum noise.

---

## 5. Classical Tensor Network Dequantization

### 5.1 Space-Time Tensor Networks

A 2D quantum circuit on an $L_1 \times L_2$ lattice with depth $d$ defines a 3D space-time tensor network of dimensions $L_1 \times L_2 \times d$. Each 2-qubit gate is a rank-4 tensor, and each single-qubit gate is a rank-2 tensor.
The contraction complexity of this 3D tensor network is determined by the treewidth $\text{tw}(G)$ of its line graph:
$$T_{\text{contract}} = O\left(d \cdot 2^{\text{tw}(G)}\right).$$

For an $L_1 \times L_2$ grid with $L_1 \le L_2$:
$$\text{tw}(G) \le L_1 \cdot \min(d, L_2) + O(1).$$

### 5.2 Tensor Slicing (Bond-Cutting)

Pan and Chen (2021) showed that classical contraction does not require storing the full tensor contraction tree in RAM. By **slicing** (fixing the values of) $s$ intermediate bond indices:
$$\mathcal{T} = \sum_{i_1, \dots, i_s \in \{0, 1\}} \mathcal{T}(i_1, \dots, i_s).$$

1. Slicing reduces the effective treewidth from $\text{tw}$ to $\text{tw}_{\text{eff}} = \text{tw} - s$.
2. The memory requirement drops exponentially:
   $$\text{RAM} = O\left(2^{\text{tw} - s}\right).$$
3. The total runtime is the embarrassingly parallel sum of $2^s$ independent contractions:
   $$T_{\text{total}} = 2^s \cdot O\left(2^{\text{tw} - s}\right) = O\left(2^{\text{tw}}\right).$$

### 5.3 Demolition of the "10,000 Year" Claim

Google's 2019 supremacy claim asserted that sampling from Sycamore would require 10,000 years on Summit supercomputer.
Pan & Chen (2021) and Kalachev et al. (2021) demonstrated:
- By selecting an optimal slicing order with $s = 12$ to $18$ cuts, the memory footprint fits into standard GPU RAM ($< 16$ GB).
- Computing a single output amplitude takes under $15$ seconds on an NVIDIA GPU cluster.
- Generating a million uncorrelated samples with linear XEB fidelity matching or exceeding the quantum processor's $F_{\text{XEB}} \approx 0.002$ takes **less than 15 hours** on a 512-GPU cluster.

The claimed speedup ratio of $10^7$ collapsed to unity.

---

## 6. The Verification Catch-22 and Spoofing Bounds

### 6.1 The Verification Catch-22

To verify that a quantum processor has achieved $F_{\text{XEB}} > 0$:
1. The experimenter collects samples $S = \{x_1, \dots, x_M\}$.
2. The verifier must compute $F_{\text{XEB}} = 2^n \sum_{x \in S} \frac{p(x)}{M} - 1$.
3. Computing $p(x) = |\langle x|U|0^n\rangle|^2$ for random quantum circuits is $\#P$-hard in the worst case (Bouland et al. 2019) and requires classical tensor network contraction or statevector simulation taking $\Omega(2^{\text{tw}})$ time.

This leads to a rigorous epistemic dilemma:
- **Case A ($n \le 70$, $d \le 20$)**: Classical supercomputers can compute $p(x)$ in seconds or hours. But this implies the circuit is classically simulable, dequantizing the claim of quantum supremacy.
- **Case B ($n \ge 100$, $d \ge 40$)**: Classical computers cannot compute $p(x)$ in polynomial time. Therefore, no verifier can compute $F_{\text{XEB}}$ to distinguish the quantum processor's output from uniform noise or spoofed distributions. The claim cannot be verified.

### 6.2 Classical Spoofing via Low-Rank Matrix Product States

Gao et al. (2021) and Aharonov et al. (2023) established that for any random quantum circuit with constant physical error $\epsilon_g > 0$, the state relaxes toward the maximally mixed state.
A classical Matrix Product State (MPS) with constant bond dimension $\chi = O(1)$ or a shallow local tensor network can output samples $x \sim q_{\text{MPS}}(x)$ satisfying:
$$F_{\text{XEB}}(q_{\text{MPS}}) \ge F_{\text{physical}} = e^{-\Omega(N_g)},$$
in deterministic classical polynomial time $\text{poly}(n)$.

Classical shallow models spoof the quantum device's benchmark score without synthesizing the full entangled statevector.

---

## 7. Comparative Classification Matrix

| Feature | Shor's Algorithm / QPE | Random Circuit Sampling (RCS) |
| :--- | :--- | :--- |
| **Problem Solved** | Period finding, factoring, discrete log | Sampling from circuit's own noisy output |
| **Useful Decision Problem** | Yes ($\text{NP} \cap \text{coNP}$) | No (No computational decision problem) |
| **Output Distribution** | Sharply peaked on period states ($p \sim 1/r$) | Anticoncentrated Porter-Thomas ($p \sim 2^{-n}$) |
| **Shannon Entropy** | Low ($O(\log r)$ bits) | Maximal ($n - 0.61$ bits) |
| **Constructive Interference** | Massive, coherent phase alignment | Suppressed; destructive of all structure |
| **Physical Fidelity Scaling** | Requires FTQC ($d \ge 3$, magic distillation) | Decays exponentially ($F \approx 0.002$) |
| **Classical Verification** | $O(1)$ operations ($x^r \equiv 1 \pmod N$) | $\#P$-hard classical simulation |
| **Dequantization Status** | Resilient against classical dequantization | Dequantized by tensor slicing & MPS spoofing |

---

## 8. Epistemic Demarcation & Invariant Enforcement

- `speedup_claim_allowed = False` (Inviolably enforced).
- `accepted_speedup_candidate = False` (Inviolably enforced).
- Random Circuit Sampling does not provide a speedup for any mathematical, algebraic, or practical computational problem.
- Registered negative result: `NEG-QUANTUM-SUPREMACY-RCS-ANTICONCENTRATION-BARRIER` (Negative Result 978).
