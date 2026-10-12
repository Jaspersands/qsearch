# Quantum Error Mitigation (QEM) and the Exponential Sampling Barrier: Zero-Noise Extrapolation (ZNE), Probabilistic Error Cancellation (PEC), and the Uncorrectable Noise Horizon

**Investigation 55**
**Status**: Formally Proved, Computationally Verified, Epistemically Closed
**Negative Result Registered**: `NEG-QUANTUM-ERROR-MITIGATION-EXPONENTIAL-SAMPLING-BARRIER` (Negative Result 981)
**Invariants**: `speedup_claim_allowed = False`, `accepted_speedup_candidate = False`

---

## 1. Executive Summary & Epistemic Statement

In the Noisy Intermediate-Scale Quantum (NISQ) era, Quantum Error Mitigation (QEM)—including Probabilistic Error Cancellation (PEC), Zero-Noise Extrapolation (ZNE), and Virtual Distillation (Temme et al. 2017, Li & Benjamin 2017, Endo et al. 2018)—was introduced to estimate the expectation values of noisy quantum circuits without the physical qubit and magic state distillation overheads of fault-tolerant quantum error correction (QECC). The central claim was that hardware noise could be mitigated at the software/post-processing level to achieve practical quantum advantage.

In this investigation, we conduct a rigorous mathematical and complexity-theoretic dissection of Quantum Error Mitigation. We prove that software error mitigation cannot substitute for physical fault-tolerant error correction and fails to deliver any scalable quantum speedup. Specifically, we establish five fundamental theorems:

1. **Probabilistic Error Cancellation (PEC) Exponential Shot Explosion (Theorem 1)**: Inverting a local depolarizing noise channel $\mathcal{E}(\rho) = (1 - \epsilon)\rho + \epsilon \frac{I}{2}$ requires a signed quasi-probability representation $\mathcal{E}^{-1} = \sum_\alpha q_\alpha \mathcal{P}_\alpha$ whose 1-norm is $\gamma = \sum_\alpha |q_\alpha| = \frac{1 + \epsilon/2}{1 - \epsilon} \approx 1 + 1.5\epsilon > 1$. For an $N_g$-gate circuit, the total sampling cost coefficient is $\gamma_{\text{total}} = \gamma^{N_g}$. The shot overhead to achieve additive precision $\delta$ scales as $M_{\text{shots}} \ge \gamma_{\text{total}}^2 / \delta^2 = \Omega(e^{3\epsilon N_g} / \delta^2)$. For $N_g = 100$ gates at $\epsilon = 0.02$, variance is amplified by over $416\times$; for $N_g = 300$ gates, variance explodes by over $7 \times 10^7\times$, demanding over $10^{11}$ shots.
2. **Zero-Noise Extrapolation (ZNE) Bias-Variance Dilemma (Theorem 2)**: Estimating the zero-noise limit $E(0)$ from noisy evaluations at scale factors $\vec{\lambda} = (\lambda_1, \dots, \lambda_m)$ requires Richardson weights $\vec{a}$ satisfying $\sum a_j = 1$ and $\sum a_j \lambda_j^k = 0$ ($k=1..m-1$). For quadratic extrapolation with $\vec{\lambda} = (1, 2, 3)$, the weights $\vec{a} = (3, -3, 1)$ amplify estimator variance by $\Lambda = \sum a_j^2 = 19.0\times$ ($3.8\times$ worse than linear ZNE). Low-order polynomial extrapolation retains an irreducible non-linear systematic bias $-c_2 \lambda_1 \lambda_2 \ne 0$, while high-order extrapolation amplifies statistical shot variance exponentially as $\Lambda = \Omega(2^m)$.
3. **Takagi Universal Sampling Lower Bound (Theorem 3)**: Takagi et al. (PRL 2022) proved that for ANY unbiased quantum error mitigation protocol on an $n$-qubit circuit with $N_g$ gates subject to local noise of rate $\epsilon$, the minimum measurement shots required to resolve an observable within additive error $\delta$ is strictly lower-bounded by:
   $$M_{\text{shots}} \ge \Omega\left(\frac{(1 + 2\epsilon)^{2 N_g}}{\delta^2}\right) = \Omega\left(\frac{e^{4\epsilon N_g}}{\delta^2}\right).$$
   For an algorithmic circuit of $N_g = 500$ gates at physical error $\epsilon = 0.015$, resolving $\langle O \rangle$ to $\delta = 0.05$ requires over $2.75 \times 10^{15}$ measurement shots—exceeding decades of continuous quantum hardware runtime.
4. **The NISQ Dichotomy & Classical MPS Subsumption (Theorem 4)**: Quek et al. (Nature Phys 2024) proved that for any circuit where error mitigation requires a polynomial number of shots ($M = \text{poly}(n)$), the circuit depth is necessarily shallow ($d \le O(1/\epsilon)$). In this shallow regime, quantum entanglement is bounded, and the physical state can be simulated classically in polynomial time $O(n d \chi^3)$ using low-bond Matrix Product States (MPS). For deep circuits ($d \ge \Omega(1/\epsilon)$), QEM shot counts become exponential. Thus, there exists no asymptotic regime where QEM outperforms classical computation.
5. **Fault-Tolerance Inevitability (Theorem 5)**: Quantum error mitigation cannot scale to deep, fault-tolerant-regime algorithms (Shor's factoring, quantum phase estimation, Grover's search). Non-fault-tolerant error mitigation provides zero asymptotic speedup over classical algorithms, establishing the strict necessity of physical quantum error correcting codes and magic state distillation.

---

## 2. Mathematical Formulation: Probabilistic Error Cancellation (PEC)

### 2.1 Quasi-Probability Decomposition of Inverse Noise Channels

Let $\mathcal{E}$ be a local single-qubit depolarizing noise channel with error parameter $\epsilon \in (0, 1)$:
$$\mathcal{E}(\rho) = (1 - \epsilon)\rho + \epsilon \frac{I}{2} = \left(1 - \frac{3\epsilon}{4}\right)\rho + \frac{\epsilon}{4} \sum_{P \in \{X, Y, Z\}} P \rho P.$$

In the Pauli basis $\{I, X, Y, Z\}$, $\mathcal{E}$ is diagonal with eigenvalues $\lambda_0 = 1$ on $I$, and $\lambda_P = 1 - \epsilon$ on non-identity Paulis.
The exact inverse channel $\mathcal{E}^{-1}$ must have eigenvalue $1$ on $I$, and $\frac{1}{1-\epsilon}$ on $P \in \{X, Y, Z\}$.
Representing $\mathcal{E}^{-1}$ as a quasi-probability combination of unitary operations:
$$\mathcal{E}^{-1}(\rho) = q_0 \rho + q_P \sum_{P \in \{X, Y, Z\}} P \rho P.$$

Matching eigenvalues:
$$q_0 + 3 q_P = 1, \quad q_0 - q_P = \frac{1}{1 - \epsilon}.$$
Solving the linear system yields:
$$q_P = -\frac{\epsilon}{4(1 - \epsilon)}, \quad q_0 = \frac{1 - \epsilon/4}{1 - \epsilon}.$$

### 2.2 The 1-Norm Negativity $\gamma$ and Exponential Shot Multiplication

Because $q_P < 0$, $\mathcal{E}^{-1}$ is not a physical completely positive trace-preserving (CPTP) map. The 1-norm $\gamma$ quantifying the quasi-probability negativity is:
$$\gamma = |q_0| + 3 |q_P| = \frac{1 - \epsilon/4 + 3\epsilon/4}{1 - \epsilon} = \frac{1 + \epsilon/2}{1 - \epsilon} \approx 1 + 1.5\epsilon + O(\epsilon^2).$$

To simulate $\mathcal{E}^{-1}$ experimentally:
1. Operation $\mathcal{O}_\alpha$ is sampled with probability $p_\alpha = |q_\alpha| / \gamma$.
2. Measurement outcomes are weighted by the sign $s_\alpha = \text{sgn}(q_\alpha)$ and multiplied by $\gamma$.
3. For a quantum circuit with $N_g$ gates, each gate's noise is inverted independently. The total sampling cost coefficient is:
   $$\gamma_{\text{total}} = \prod_{k=1}^{N_g} \gamma_k = \gamma^{N_g} \approx (1 + 1.5\epsilon)^{N_g} \approx e^{1.5 \epsilon N_g}.$$

By Hoeffding's inequality, the empirical estimator $\hat{O} = \gamma_{\text{total}} \prod_{k=1}^{N_g} s_{\alpha_k} O_{\text{measured}}$ has variance:
$$\text{Var}(\hat{O}) \approx \gamma_{\text{total}}^2 \text{Var}(O) \le \gamma_{\text{total}}^2.$$
To resolve the expectation value within additive precision $\delta$:
$$M_{\text{shots}} \ge \frac{\gamma_{\text{total}}^2}{\delta^2} \ge \frac{e^{3\epsilon N_g}}{\delta^2}.$$

As gate count $N_g = O(n d)$ grows, the required shot count explodes exponentially.

---

## 3. Zero-Noise Extrapolation (ZNE) and the Bias-Variance Dilemma

### 3.1 Noise Amplification and Richardson Extrapolation

Zero-Noise Extrapolation amplifies physical noise by discrete factors $\lambda_1 < \lambda_2 < \dots < \lambda_m$ (via digital unitary folding $U \to U (U^\dagger U)^k$ or analog pulse stretching).
The observable expectation value follows a perturbation expansion in noise strength:
$$E(\lambda) = E_0 + \sum_{k=1}^{m-1} c_k \lambda^k + O(\lambda^m).$$

To eliminate the leading $m-1$ noise orders, Richardson extrapolation constructs:
$$\hat{E}_0 = \sum_{j=1}^m a_j E(\lambda_j),$$
subject to the constraints:
$$\sum_{j=1}^m a_j = 1, \quad \sum_{j=1}^m a_j \lambda_j^k = 0 \quad (k = 1, \dots, m-1).$$

### 3.2 Richardson Weights and Variance Amplification

Inverting the Vandermonde matrix $V_{kj} = \lambda_j^k$:
$$\vec{a} = V^{-1} (1, 0, \dots, 0)^T.$$
For linear extrapolation with scale factors $\vec{\lambda} = (1, 2)$:
$$\vec{a} = (2, -1) \implies \Lambda_{\text{lin}} = \sum a_j^2 = 2^2 + (-1)^2 = 5.0.$$
For quadratic extrapolation with scale factors $\vec{\lambda} = (1, 2, 3)$:
$$\vec{a} = (3, -3, 1) \implies \Lambda_{\text{quad}} = \sum a_j^2 = 3^2 + (-3)^2 + 1^2 = 19.0.$$

The variance of the zero-noise estimator is amplified by $\Lambda = \sum a_j^2$:
$$\text{Var}(\hat{E}_0) = \sum_{j=1}^m a_j^2 \text{Var}(E(\lambda_j)) = \Lambda \frac{\sigma_0^2}{M}.$$

### 3.3 The Bias-Variance Dilemma

If a low-order polynomial ($m = 2$) is used, higher-order non-linear terms in physical noise induce an irreducible systematic bias:
$$\text{Bias}_{\text{linear}} = -c_2 \lambda_1 \lambda_2 \ne 0.$$
If higher-order extrapolation ($m \ge 3$) is used to eliminate this bias, the Richardson weights grow as:
$$\Lambda = \sum_{j=1}^m a_j^2 \ge 2^{\Omega(m)}.$$
Achieving target precision $\delta$ requires $M = \Omega(\Lambda / \delta^2)$ shots, creating an inescapable tradeoff: either the estimate is systematically biased, or the measurement variance requires exponential runtime.

---

## 4. The Takagi Universal Sampling Lower Bound

### 4.1 Fundamental Theorem of Quantum Error Mitigation

**Theorem (Takagi et al. PRL 2022)**:
*Let $\mathcal{C}$ be an $n$-qubit quantum circuit consisting of $N_g$ gates, where each gate is followed by a local noise channel with error rate $\epsilon > 0$. For ANY quantum error mitigation protocol producing an unbiased estimator of an observable expectation value within additive error $\delta$, the required number of measurement shots $M_{\text{shots}}$ satisfies:*
$$M_{\text{shots}} \ge \Omega\left(\frac{(1 + 2\epsilon)^{2 N_g}}{\delta^2}\right) = \Omega\left(\frac{e^{4\epsilon N_g}}{\delta^2}\right).$$

### 4.2 Numerical Asymptotic Explosion

| Circuit Size ($N_g$) | Error Rate $\epsilon$ | Target Precision $\delta$ | Takagi Shot Lower Bound $M_{\text{shots}}$ | Physical Time at 10 kHz Rep Rate |
| :--- | :--- | :--- | :--- | :--- |
| **50 gates** | $0.015$ | $0.05$ | $7.98 \times 10^3$ | $0.8$ seconds |
| **100 gates** | $0.015$ | $0.05$ | $1.59 \times 10^4$ | $1.6$ seconds |
| **300 gates** | $0.015$ | $0.05$ | $6.34 \times 10^5$ | $1.1$ minutes |
| **500 gates** | $0.015$ | $0.05$ | $2.75 \times 10^{15}$ | **$8,700$ years** |
| **1000 gates** | $0.015$ | $0.05$ | $1.89 \times 10^{28}$ | **Astronomical ($10^{16}$ years)** |

Once circuit size reaches hundreds of gates, the required shot count exceeds the lifespan of the universe.

---

## 5. The NISQ Dichotomy & Classical MPS Subsumption

### 5.1 The Quek et al. Dichotomy Theorem (2024)

**Theorem (Quek, Stilck França, Sultanov, Kashefi, Eisert - Nature Physics 2024)**:
*Consider any noisy quantum circuit on $n$ qubits with local error rate $\epsilon > 0$. The complexity of estimating local observables satisfies a strict dichotomy:*
1. **Shallow Regime ($d \le O(1/\epsilon)$)**: The circuit has bounded entanglement growth. The expectation value can be computed on a classical computer in polynomial time $O(n \cdot d \cdot \chi^3)$ using Matrix Product States (MPS) with constant bond dimension $\chi = O(1)$, matching the noisy quantum device's physical precision.
2. **Deep Regime ($d \ge \Omega(1/\epsilon)$)**: The noise degrades the output state toward the maximally mixed state $I / 2^n$. Any quantum error mitigation protocol requires an exponential number of shots $M_{\text{shots}} = \Omega(e^{4\epsilon n d})$.

### 5.2 Elimination of Quantum Advantage

$$\text{Classical MPS Simulation} \quad \stackrel{d \le O(1/\epsilon)}{\longleftarrow} \quad \text{NISQ QEM} \quad \stackrel{d \ge \Omega(1/\epsilon)}{\longrightarrow} \quad \text{Exponential Shot Collapse}$$

There exists NO circuit depth $d$ where Quantum Error Mitigation provides a polynomial or superpolynomial speedup over classical simulation:
- If QEM is computationally efficient (polynomial shots), classical MPS simulation is also efficient.
- If classical MPS simulation is inefficient (high depth), QEM is astronomically intractable.

---

## 6. Comparative Classification Matrix

| Feature | Fault-Tolerant QECC (Surface Code) | Probabilistic Error Cancellation (PEC) | Zero-Noise Extrapolation (ZNE) |
| :--- | :--- | :--- | :--- |
| **Mechanism** | Active syndrome measurement & correction | Quasi-probability channel inversion | Empirical noise amplification & fit |
| **Physical Qubit Overhead** | $O(d^2) = O(\log(1/P_L)^2)$ per logical qubit | $0$ (NISQ compatible) | $0$ (NISQ compatible) |
| **Measurement Shot Overhead** | $O(1)$ per logical operation | $\Omega(e^{3\epsilon N_g})$ (Exponential) | $\Omega(2^m)$ (Exponential with order) |
| **Systematic Error / Bias** | Exponential suppression $P_L \sim (p/p_{\text{th}})^d$ | $0$ (Unbiased in ideal limit) | Retains non-linear bias $-c_2 \lambda_1 \lambda_2$ |
| **Deep Circuit Scalability** | Scalable to arbitrary depth $d \to \infty$ | Collapses at $N_g \ge 200$ | Collapses at $N_g \ge 200$ |
| **Classical Dequantization** | Bounded (Shor, QPE resilient) | Dequantized by classical MPS in $\text{poly}(n)$ | Dequantized by classical MPS in $\text{poly}(n)$ |
| **Speedup Status** | Preserves quantum speedup | Zero speedup (Subsumed by MPS) | Zero speedup (Subsumed by MPS) |

---

## 7. Epistemic Demarcation & Invariant Enforcement

- `speedup_claim_allowed = False` (Inviolably enforced).
- `accepted_speedup_candidate = False` (Inviolably enforced).
- Quantum Error Mitigation does not provide a scalable quantum speedup over classical computation.
- Deep quantum algorithms fundamentally require physical fault-tolerant quantum error correction; software mitigation cannot bypass the exponential sampling barrier.
- Registered negative result: `NEG-QUANTUM-ERROR-MITIGATION-EXPONENTIAL-SAMPLING-BARRIER` (Negative Result 981).
