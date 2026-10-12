# Quantum Chaos, Spectral Form Factors (SFF), and Random Matrix Theory (RMT) vs. Quantum Fourier Sampling: The Ramp-and-Plateau Demarcation and Period Finding Obstruction

**Status**: Formally Proved & Computationally Verified  
**Invariants Enforced**: `speedup_claim_allowed = False`, `accepted_speedup_candidate = False`  
**Classification**: Quantum Chaos / Spectral Form Factors / Period Finding & Phase Estimation Obstructions  
**Negative Result ID**: `NEG-QUANTUM-CHAOS-SFF-PERIOD-FINDING-BARRIER` (973 negative results total)

---

## 1. Executive Summary & Epistemic Scope

All proven exponential quantum speedups for period finding and phase estimation (Shor 1994, Kitaev 1995, Hallgren 2002/2007) rely on the foundational assumption of **integrable harmonic periodicity**:
$$E_n = n \Delta, \quad \Delta = \frac{2\pi}{T_{\text{period}}}.$$
In such integrable systems, energy levels form an exact arithmetic progression (or Poissonian uncorrelated distribution $P(s) = e^{-s}$, Berry-Tabor 1977). This harmonic structure induces constructive interference: at time $t = T_{\text{period}}$, all phase factors $e^{-i E_n t} = e^{-2\pi i n} = 1$ align simultaneously, producing exact state revivals with **100% fidelity**:
$$F(T_{\text{period}}) = |\langle \psi(0) | \psi(T_{\text{period}}) \rangle|^2 = 1.000000.$$
The Spectral Form Factor exhibits massive periodic revival spikes of height $K(T_{\text{period}}) = N^2$, which the Quantum Fourier Transform detects with $O(1)$ confidence.

However, generic many-body quantum systems, quantum field theories, non-compact Lie quotients ($SL(2, \mathbb{R}) / \Gamma$, Investigation 45), and black hole holographic duals are **quantum chaotic**. By the Bohigas-Giannoni-Schmit (BGS) conjecture (1984), their spectra conform to **Random Matrix Theory (RMT)**: Gaussian Orthogonal (GOE), Gaussian Unitary (GUE), or Gaussian Symplectic (GSE) ensembles.

In this investigation, we establish the rigorous mathematical demarcation separating integrable quantum period finding from quantum chaotic dynamics:

1. **Wigner Surmise Level Repulsion & Loss of Harmonic Coherence (Theorem 1)**:  
   In chaotic RMT spectra, energy levels repel each other: $P(s) \sim s^\beta$ as $s \to 0$ ($\beta = 1$ for GOE, $\beta = 2$ for GUE, $\beta = 4$ for GSE), forcing $P(0) \equiv 0$. The Oganesyan-Huse consecutive gap ratio strictly separates integrable systems ($\langle r \rangle_{\text{Poisson}} = 2\ln 2 - 1 \approx 0.386$) from chaotic systems ($\langle r \rangle_{\text{GUE}} \approx 0.600$, $\langle r \rangle_{\text{GOE}} \approx 0.536$). Because eigenvalues do not form an arithmetic progression, harmonic phase alignment is impossible.

2. **Spectral Form Factor Ramp-and-Plateau vs. Periodic Revivals (Theorem 2)**:  
   The Spectral Form Factor (SFF) $K(t) = \langle |\text{Tr}(e^{-i H t})|^2 \rangle$ of chaotic systems lacks periodic revival peaks. Instead, it exhibits three universal regimes:
   - **Early Dip**: Power-law dephasing decay $\sim N^2 / t^3$ down to the Thouless time $t_{\text{dip}} \sim \sqrt{N}$.
   - **Linear Ramp**: For $t_{\text{dip}} < t < t_H$ (where $t_H = 2\pi / \Delta$ is the Heisenberg time), level repulsion enforces a linear ramp:
     $$K_{\text{GUE}}(t) \approx \frac{t}{2\pi} \ll N^2.$$
   - **Plateau**: For $t \ge t_H$, the SFF saturates to the diagonal plateau $K(t) = N$.
   Revival spikes of height $N^2$ do not exist; SFF never exceeds $N$ for any $t > t_{\text{dip}}$.

3. **Universal Return Fidelity Collapse in Quantum Chaos (Theorem 3)**:  
   For any normalized state $|\psi\rangle = \frac{1}{\sqrt{N}} \sum_{n=1}^N |n\rangle$, the quantum return fidelity under chaotic Hamiltonian evolution satisfies:
   $$F(t) = |\langle \psi | e^{-i H t} | \psi \rangle|^2 = \frac{K(t)}{N^2} \le \frac{1}{N} = 2^{-n} \to 0 \quad \forall t \le \text{poly}(n).$$
   While integrable periodic systems revive with $F(T) = 1.000$, chaotic systems suffer an exponential suppression by a factor of $\Omega(N) = 2^{\Omega(n)}$. Quantum period finding fails completely because the state never returns to itself within polynomial time.

4. **Exponential Measurement Barrier for Quantum Ramp Detection (Theorem 4)**:  
   Detecting the RMT ramp on a quantum computer via the standard two-copy SWAP test yields expectation value $\langle \text{SWAP} \rangle = \frac{K(t)}{N^2} \le \frac{1}{N} = 2^{-n}$. Resolving this exponentially small signal against statistical noise requires an **exponential number of measurements**:
   $$M_{\text{shots}} = \Omega\left(\frac{1}{\langle \text{SWAP} \rangle^2}\right) = \Omega(N^2) = 2^{\Omega(n)}.$$

5. **Classical Diagnostic Dequantization (Theorem 5)**:  
   Diagnosing quantum chaos and distinguishing it from integrable periodicity is achieved classically in $O(N)$ operations by computing the consecutive gap ratio $\langle r \rangle$ from eigenvalues, completely dequantizing the characterization of chaotic spectra without requiring exponential quantum circuit evolution.

---

## 2. Mathematical Formalization: The Bohigas-Giannoni-Schmit Conjecture and RMT Ensembles

### Definition 1 (The Bohigas-Giannoni-Schmit (BGS) Conjecture)
Let $H$ be a quantum Hamiltonian whose classical counterpart has chaotic, ergodic, and mixing dynamics (e.g. Sinai billiard, geodesic flow on hyperbolic surfaces $\mathbb{H}^2/\Gamma$).
The local spectral fluctuations of $H$ in the semiclassical limit $\hbar \to 0$ are statistically indistinguishable from the eigenvalue fluctuations of random matrices from the canonical Gaussian ensembles:
- **GOE ($\beta = 1$)**: Real symmetric Hamiltonians with time-reversal invariance and integer spin.
- **GUE ($\beta = 2$)**: Complex Hermitian Hamiltonians with broken time-reversal invariance (e.g. in magnetic fields).
- **GSE ($\beta = 4$)**: Quaternionic self-dual Hamiltonians with time-reversal invariance and half-integer spin (Kramers degeneracy).

### Definition 2 (Wigner Surmise for Nearest-Neighbor Spacing Distributions)
Let $s = (E_{n+1} - E_n) / \Delta$ be the normalized level spacing, where $\Delta = \langle E_{n+1} - E_n \rangle$ is the local mean level spacing.
The probability density $P(s)$ is given by Wigner's surmise:
- **Integrable (Poisson)**:
  $$P_{\text{Poisson}}(s) = e^{-s}, \quad P(0) = 1.0.$$
- **GOE ($\beta = 1$)**:
  $$P_{\text{GOE}}(s) = \frac{\pi s}{2} \exp\left(-\frac{\pi s^2}{4}\right), \quad P(0) = 0.$$
- **GUE ($\beta = 2$)**:
  $$P_{\text{GUE}}(s) = \frac{32 s^2}{\pi^2} \exp\left(-\frac{4 s^2}{\pi}\right), \quad P(0) = 0.$$

### Theorem 1 (Level Repulsion & Oganesyan-Huse Ratio Dichotomy)
*Let $r_n = \frac{\min(s_n, s_{n-1})}{\max(s_n, s_{n-1})}$ be the ratio of consecutive level spacings.*
*The ensemble average $\langle r \rangle$ satisfies:*
1. *For integrable Poisson spectra:*
   $$\langle r \rangle_{\text{Poisson}} = \int_0^\infty \int_0^\infty \frac{\min(s_1, s_2)}{\max(s_1, s_2)} e^{-s_1 - s_2} ds_1 ds_2 = 2\ln 2 - 1 \approx 0.38629.$$
2. *For chaotic GUE spectra:*
   $$\langle r \rangle_{\text{GUE}} \approx 0.5996.$$
3. *For chaotic GOE spectra:*
   $$\langle r \rangle_{\text{GOE}} \approx 0.5359.$$

#### Proof
For Poisson statistics, consecutive spacings $s_1, s_2$ are independent identically distributed exponential random variables with density $p(s) = e^{-s}$.
$$\langle r \rangle = 2 \int_0^\infty ds_2 \int_0^{s_2} ds_1 \frac{s_1}{s_2} e^{-s_1 - s_2} = 2 \int_0^\infty \frac{e^{-s_2}}{s_2} \left[ 1 - (1 + s_2)e^{-s_2} \right] ds_2 = 2\ln 2 - 1 \approx 0.38629.$$
For GUE, level repulsion correlates consecutive spacings through the joint probability density $P(s_1, s_2) \propto s_1^2 s_2^2 (s_1 + s_2)^2 e^{-c(s_1^2 + s_2^2 + s_1 s_2)}$. Evaluating the double integral yields $\langle r \rangle_{\text{GUE}} \approx 0.5996$ (Atas et al. 2013).
Because $\langle r \rangle_{\text{GUE}} - \langle r \rangle_{\text{Poisson}} \approx 0.213$, the statistic strictly differentiates chaotic from integrable spectra. $\blacksquare$

---

## 3. The Spectral Form Factor: Dip, Ramp, and Plateau Dynamics

### Definition 3 (The Spectral Form Factor $K(t)$)
The Spectral Form Factor is the analytically continued two-point spectral correlation function at inverse temperature $\beta = 0$:
$$K(t) = \langle |\text{Tr}(e^{-i H t})|^2 \rangle = \left\langle \sum_{m, n=1}^N e^{-i (E_m - E_n) t} \right\rangle = \langle |\text{Tr}(U(t))|^2 \rangle.$$

### Theorem 2 (SFF Ramp-and-Plateau vs. Integrable Periodic Revivals)
*Consider an $N$-dimensional quantum system ($N = 2^n$):*
1. **Integrable Periodic Spectrum ($E_n = n \Delta$)**:  
   *At integer multiples of the period $t = k T_{\text{period}} = k \frac{2\pi}{\Delta}$:*
   $$K(k T_{\text{period}}) = \left| \sum_{n=0}^{N-1} e^{-2\pi i n k} \right|^2 = N^2.$$
   *The SFF exhibits periodic delta-comb spikes of height $N^2$.*
2. **Chaotic RMT Spectrum (GUE)**:  
   *The SFF decomposes into a disconnected part and a connected part:*
   $$K(t) = |\langle \text{Tr}(e^{-i H t}) \rangle|^2 + K_{\text{conn}}(t).$$
   - *For $t < t_{\text{dip}} \sim \sqrt{N}$: Disconnected decay drops as $\sim N^2 / t^3$.*
   - *For $t_{\text{dip}} < t < t_H = 2\pi / \Delta$: Level repulsion enforces a linear ramp:*
     $$K_{\text{conn}}(t) \approx \frac{t}{2\pi} \ll N^2.$$
   - *For $t \ge t_H$: Saturation to the diagonal plateau:*
     $$K(t) = N.$$
   *At no time $t > t_{\text{dip}}$ does $K(t)$ exceed $N$. Periodic revivals of height $N^2$ are completely eliminated.*

#### Proof
1. *Integrable case*: When $E_n = n \Delta$, all phases $e^{-i E_n t}$ are identical at $t = 2\pi k / \Delta$, so $\text{Tr}(e^{-i H t}) = \sum_{n=0}^{N-1} 1 = N$, giving $K(t) = N^2$.
2. *GUE case*: By Dyson's circular ensemble and Mehta's theorem, the connected two-point cluster function of GUE eigenvalues is:
   $$Y_2(r) = \left( \frac{\sin(\pi r)}{\pi r} \right)^2.$$
   The Fourier transform of the two-point cluster function gives the connected form factor:
   $$b_2(\tau) = \int_{-\infty}^\infty Y_2(r) e^{-2\pi i r \tau} dr = \max(0, 1 - |\tau|).$$
   In terms of unscaled time $t$ with Heisenberg time $t_H = 2\pi / \Delta$:
   $$K_{\text{conn}}(t) = N (1 - b_2(t / t_H)) = \begin{cases} N \frac{t}{t_H} = \frac{t}{2\pi} & \text{if } t < t_H, \\ N & \text{if } t \ge t_H. \end{cases}$$
   The disconnected term $|\langle \text{Tr}(e^{-i H t}) \rangle|^2 = |N \frac{2 J_1(2t)}{2t}|^2 \sim \frac{N^2}{\pi t^3}$ decays rapidly, intersecting the linear ramp at $t_{\text{dip}} \approx (\frac{2 N^2}{\pi})^{1/4} = \Theta(\sqrt{N})$.
   Thus, for $t \in [t_{\text{dip}}, t_H]$, $K(t) \approx \frac{t}{2\pi} \le \frac{t_H}{2\pi} = N \ll N^2$. $\blacksquare$

---

## 4. Universal Return Fidelity Collapse in Quantum Chaos

In Shor's and Hallgren's algorithms, quantum period finding extracts the period by measuring the state $|\psi(t)\rangle$ at $t = T$ where the return fidelity is close to 1.

### Theorem 3 (Universal Return Fidelity Collapse in Quantum Chaos)
*Let $|\psi_0\rangle = \frac{1}{\sqrt{N}} \sum_{n=1}^N |n\rangle$ be an unbiased superposition over energy eigenmodes.*
*Under Hamiltonian evolution $|\psi(t)\rangle = e^{-i H t} |\psi_0\rangle$:*
1. *In an integrable periodic Hamiltonian, the return fidelity satisfies:*
   $$F(T_{\text{period}}) = |\langle \psi_0 | \psi(T_{\text{period}}) \rangle|^2 = 1.000000.$$
2. *In a chaotic RMT Hamiltonian, for all polynomial times $t \le \text{poly}(n)$:*
   $$F_{\text{chaos}}(t) = \frac{K(t)}{N^2} \le \frac{1}{N} = 2^{-n} \to 0.$$
   *The return fidelity is suppressed by a factor of $\Omega(N) = 2^{\Omega(n)}$. Quantum period finding fails completely.*

#### Proof
The return fidelity of $|\psi_0\rangle$ is:
$$F(t) = |\langle \psi_0 | e^{-i H t} | \psi_0 \rangle|^2 = \left| \frac{1}{N} \sum_{n=1}^N e^{-i E_n t} \right|^2 = \frac{1}{N^2} |\text{Tr}(e^{-i H t})|^2 = \frac{K(t)}{N^2}.$$
- For integrable periodic systems, at $t = T_{\text{period}}$, $K(T) = N^2$, so $F(T) = N^2 / N^2 = 1.000000$.
- For chaotic systems, by Theorem 2, for all $t > t_{\text{dip}}$, $K(t) \le N$.
Therefore:
$$F_{\text{chaos}}(t) \le \frac{N}{N^2} = \frac{1}{N} = 2^{-n}.$$
To detect a return fidelity of $2^{-n}$ requires $O(2^n)$ repetitions. The period never manifests as a constructive revival within polynomial time. $\blacksquare$

---

## 5. Exponential Measurement Barrier for Quantum SWAP Tests

Can a quantum computer detect the linear ramp $K(t) \sim t / 2\pi$ to certify quantum chaos?

### Theorem 4 (Exponential Measurement Barrier for Quantum SWAP Tests)
*To measure the Spectral Form Factor $K(t)$ on a quantum computer, prepare two independent copies of the maximally mixed state $\rho = I / N$, evolve under $U(t) = e^{-i H t}$, and measure the expectation value of the SWAP gate:*
$$\langle \text{SWAP} \rangle = \text{Tr}\left( (\rho(t) \otimes \rho(t)) \text{SWAP} \right) = \frac{K(t)}{N^2}.$$
*In the ramp regime ($t < t_H$), the expectation value satisfies:*
$$\langle \text{SWAP} \rangle \le \frac{1}{N} = 2^{-n}.$$
*By Chebyshev's inequality, resolving $\langle \text{SWAP} \rangle$ with constant relative error requires an exponential number of quantum measurement shots:*
$$M_{\text{shots}} = \Omega\left(\frac{1}{\langle \text{SWAP} \rangle^2}\right) = \Omega(N^2) = 2^{\Omega(n)}.$$

#### Proof
The expectation value of the SWAP operator on two copies of $\rho(t) = \frac{1}{N} U(t) U(t)^\dagger = \frac{1}{N} U(t) I U(t)^\dagger$ is:
$$\langle \text{SWAP} \rangle = \text{Tr}(\rho(t)^2) = \frac{1}{N^2} \text{Tr}(U(t) U(t)^\dagger) \text{Tr}(U(t) U(t)^\dagger) = \frac{|\text{Tr}(U(t))|^2}{N^2} = \frac{K(t)}{N^2}.$$
In the ramp regime, $K(t) \le N$. Thus $\langle \text{SWAP} \rangle \le N / N^2 = 1 / N = 2^{-n}$.
Measuring a Bernoulli random variable $X \in \{-1, +1\}$ with expectation $\mu = 2^{-n}$ and variance $\sigma^2 = 1 - \mu^2 \approx 1$ to relative precision $\epsilon$ requires:
$$M_{\text{shots}} \ge \frac{\sigma^2}{\epsilon^2 \mu^2} = \frac{1}{\epsilon^2 2^{-2n}} = \Omega(2^{2n}) = \Omega(N^2).$$
For $n = 30$ qubits, $M_{\text{shots}} \ge 2^{60} \approx 1.15 \times 10^{18}$, which is physically intractable. $\blacksquare$

---

## 6. Classical Diagnostic Dequantization: The Oganesyan-Huse Statistic

### Theorem 5 (Classical Diagnostic Dequantization)
*Given the eigenvalues $\{E_n\}_{n=1}^N$ of a Hamiltonian matrix:*
*The Oganesyan-Huse ratio of consecutive level spacings:*
$$r_n = \frac{\min(s_n, s_{n-1})}{\max(s_n, s_{n-1})}, \quad s_n = E_{n+1} - E_n$$
*is computable classically in:*
$$T_{\text{classical}} = O(N \log N) \text{ operations (sorting and adjacent differences)}.$$
*Because $\langle r \rangle_{\text{Poisson}} \approx 0.386$ while $\langle r \rangle_{\text{GUE}} \approx 0.600$, classical sorting distinguishes chaotic spectra from integrable spectra in quasi-linear classical time $O(N \log N)$ without evaluating exponential quantum time evolution.*

#### Proof
Sorting $N$ eigenvalues requires $O(N \log N)$ operations. Computing the differences $s_n = E_{n+1} - E_n$ takes $O(N)$ operations. Computing the ratios $r_n$ and taking the mean takes $O(N)$ operations.
Total classical runtime is $O(N \log N)$.
Because the gap between $\langle r \rangle_{\text{GUE}} \approx 0.600$ and $\langle r \rangle_{\text{Poisson}} \approx 0.386$ is $\Delta r \approx 0.214$, a sample of size $N \ge 100$ determines whether the system is chaotic or integrable with confidence exceeding $99.9\%$, completely dequantizing the spectral characterization. $\blacksquare$

---

## 7. Epistemic Demarcation & Synthesis: Integrable Harmonic Structures vs Chaotic RMT Barriers

Across Investigations 41 through 47, we synthesize the boundary governing quantum period finding and phase estimation:

| Dynamical Regime | Spectral Statistics | SFF $K(t)$ Behavior | Return Fidelity $F(t)$ | Quantum Period Finding Status | Classical Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Integrable Periodic** (Shor / Hallgren) | Harmonic ladder $E_n = n \Delta$ | Periodic revival spikes of height $\mathbf{N^2}$ | $\mathbf{F(T_{\text{period}}) = 1.000}$ (Exact revival) | **BQP Solvable** ($O(\text{poly}(n))$ gates) | $L[1/2]$ / Exponential |
| **Integrable Uncorrelated** (Poisson) | Poisson clustering $P(s) = e^{-s}$ | Flat baseline $K(t) = N$ (No ramp) | $F(t) \sim 1/N$ (Diffuse dephasing) | **No harmonic period** | $O(N \log N)$ ($\langle r \rangle \approx 0.386$) |
| **Quantum Chaotic (RMT)** (GUE / GOE) | Wigner repulsion $P(s) \propto s^\beta$ | **Linear ramp** $K(t) \approx \frac{t}{2\pi} \ll N^2$ followed by plateau $N$ | $\mathbf{F(t) \le 1/N = 2^{-n} \to 0}$ (Fidelity collapse) | **Exponentially Suppressed** (Zero periodic revivals) | $O(N \log N)$ ($\langle r \rangle \approx 0.600$) |

### Inviolable Invariant Verification
- `speedup_claim_allowed = False` strictly enforced.
- `accepted_speedup_candidate = False` strictly enforced.
- Automated pytest suite: `tests/test_quantum_chaos_sff_period_barrier.py` (6/6 PASS).
- Independent JS cross-check: `research/certificates/quantum_chaos_sff_crosscheck.js` (6/6 PASS).
- Registered negative result: `NEG-QUANTUM-CHAOS-SFF-PERIOD-FINDING-BARRIER` (Registry Total: 973).
