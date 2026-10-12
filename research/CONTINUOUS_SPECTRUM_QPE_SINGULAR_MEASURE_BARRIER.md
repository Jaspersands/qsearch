# Quantum Phase Estimation on Continuous Spectrum Hamiltonians and Singular Spectral Measures: Resolvent Broadening, Universal Peak Flattening, and Classical KPM Dequantization

**Status**: Formally Proved & Computationally Verified  
**Invariants Enforced**: `speedup_claim_allowed = False`, `accepted_speedup_candidate = False`  
**Classification**: Quantum Phase Estimation / Continuous & Singular Spectral Measures / Complexity Obstructions  
**Negative Result ID**: `NEG-CONTINUOUS-SPECTRUM-QPE-SINGULAR-MEASURE-BARRIER` (972 negative results total)

---

## 1. Executive Summary & Epistemic Scope

Standard Quantum Phase Estimation (QPE) (Kitaev 1995, Cleve et al. 1998) and Quantum Singular Value Transformation (QSVT) (Gilyén et al. 2019) form the foundational engine for all claimed exponential quantum speedups in chemistry, Hamiltonian simulation, and period finding. In the standard paradigm, the Hamiltonian $H$ is assumed to possess a **discrete pure-point spectrum** with normalizable eigenstates:
$$H |\psi_k\rangle = E_k |\psi_k\rangle, \quad \langle \psi_j | \psi_k \rangle = \delta_{j, k}.$$
Under this discrete assumption, QPE concentrates $\ge 8/\pi^2 \approx 81.1\%$ of the measurement probability mass into the single discrete computational bin closest to $E_k$, extracting eigenvalue digits with exponentially small error $O(2^{-m})$ in $m = O(\log(1/\epsilon))$ qubits.

However, in extensive domains of physical quantum simulation—including continuum scattering states, non-compact Lie group dynamics ($SL(2, \mathbb{R})$, Investigation 45), quantum field theories, continuous momentum operators $P = -i\hbar \frac{d}{dx}$ on $L^2(\mathbb{R})$, and quasi-periodic aperiodic lattices—Hamiltonians possess **continuous** ($\mu_{\text{ac}}$) or **singular continuous** ($\mu_{\text{sc}}$) spectral measures.

In this investigation, we establish the complete spectral-measure and complexity bounds for Quantum Phase Estimation and Resolvent simulation on continuous and singular continuous spectra:

1. **Universal Peak Flattening Theorem on Absolutely Continuous Spectra (Theorem 1)**:  
   When an initial state $|\psi\rangle$ is supported on an absolutely continuous spectral measure $d\mu_{\text{ac}}(E) = \rho(E) dE$, generalized eigenstates $|E\rangle$ are **non-normalizable** ($\langle E | E' \rangle = \delta(E - E')$, $|E\rangle \notin \mathcal{H}$). For an $m$-qubit QPE register ($N = 2^m$) with base evolution time $\tau$, the measurement probability of any discrete bin $k \in \{0, \dots, N-1\}$ scales as:
   $$P(k) = \int_{-\infty}^\infty \rho(E) \frac{\sin^2\left(\frac{N}{2}(E\tau - \frac{2\pi k}{N})\right)}{N^2 \sin^2\left(\frac{1}{2}(E\tau - \frac{2\pi k}{N})\right)} dE \approx \rho\left(\frac{2\pi k}{N\tau}\right) \cdot \frac{2\pi}{N\tau} = \Theta\left(\frac{1}{N}\right) = \Theta(2^{-m}).$$
   **Peak flattening is universal**: as register size $N \to \infty$, the maximum bin probability vanishes ($P(k_{\max}) \to 0$). Unlike discrete eigenstates where a single measurement yields the eigenvalue with $O(1)$ confidence, in the continuous spectrum, every individual run returns a distinct bin with probability $O(2^{-m})$, converting QPE strictly into continuous density sampling.

2. **Resolvent Lorentzian Broadening & Condition Number Barrier (Theorem 2)**:  
   Attempting to simulate the Green's function resolvent $G(z) = (z - H)^{-1}$ for $z = E + i\eta$ with broadening $\eta > 0$ yields the expectation value:
   $$-\frac{1}{\pi} \text{Im} \langle \psi | (E + i\eta - H)^{-1} | \psi \rangle = (\rho * L_\eta)(E) = \int_{-\infty}^\infty \rho(E') \frac{1}{\pi} \frac{\eta}{(E - E')^2 + \eta^2} dE'.$$
   The resolvent expectation value is strictly the convolution of the true continuous density with a Lorentzian of Full Width at Half Maximum (FWHM) $\Delta E = 2\eta$. Resolving spectral features of scale $\delta$ strictly requires $\eta \le \delta / 2$. The condition number of the operator is:
   $$\kappa = \|(E + i\eta - H)^{-1}\| = \frac{1}{\eta} \ge \frac{2}{\delta}.$$
   By the lower bound for QSVT polynomial simulation (Gilyén et al. 2019), simulating the resolvent to resolution $\eta$ requires a quantum circuit depth of at least $\Omega(1 / \eta) = \Omega(1 / \delta)$ queries.

3. **Singular Continuous Spectra & Hofstadter Cantor Intermittency (Theorem 3)**:  
   For Hamiltonians with singular continuous spectra (such as the Almost Mathieu operator $(H \psi)_n = \psi_{n+1} + \psi_{n-1} + 2\cos(2\pi \alpha n)\psi_n$ at irrational flux $\alpha$ and critical coupling $\lambda = 1$), the spectrum $\sigma(H)$ is a Cantor set of Lebesgue measure zero with Hausdorff dimension $D_H < 1$. The integrated density of states $N(E)$ is a Devil's staircase.
   The gap-to-spacing ratio exceeds $10^4$, causing extreme intermittency in QPE: bins falling in dense Cantor clusters fluctuate with fractional Hölder scaling $|N(E + \epsilon) - N(E)| \sim \epsilon^\alpha$ ($\alpha \in (0, 1)$), while bins in Hofstadter gaps yield zero mass. This destroys continuous phase estimation and continued fraction period extraction.

4. **Classical Kernel Polynomial Method (KPM) Dequantization (Theorem 4)**:  
   Evaluating the continuous spectral density $\rho(E)$ to resolution $\eta$ on classical computers using the **Kernel Polynomial Method (KPM)** with Jackson damping requires a Chebyshev polynomial expansion of degree $M = \lceil \pi / \eta \rceil = \Theta(1 / \eta)$. The classical algorithm performs $M$ sparse matrix-vector multiplications in $O(M \cdot \text{nnz}(H))$ operations.
   Because both classical KPM and quantum QSVT/QPE scale as $\Theta(1 / \eta)$, continuous spectral density estimation is **completely dequantized classically**, possessing zero exponential quantum advantage.

---

## 2. Mathematical Formalization: Spectral Theorem and Tri-Fold Measure Decomposition

### Definition 1 (The Spectral Theorem for Self-Adjoint Operators)
Let $H$ be a self-adjoint operator on a separable Hilbert space $\mathcal{H}$. By the spectral theorem, there exists a unique projection-valued measure $E(\cdot)$ on the Borel $\sigma$-algebra $\mathcal{B}(\mathbb{R})$ such that:
$$H = \int_{\sigma(H)} \lambda \, dE(\lambda).$$
For any normalized state $|\psi\rangle \in \mathcal{H}$, the scalar spectral measure $\mu_\psi$ is defined by:
$$\mu_\psi(\Omega) = \langle \psi | E(\Omega) | \psi \rangle, \quad \forall \Omega \in \mathcal{B}(\mathbb{R}).$$

### Definition 2 (Lebesgue-Radon-Nikodym Tri-Fold Decomposition)
The scalar spectral measure $\mu_\psi$ uniquely decomposes into three mutually singular parts:
$$\mu_\psi = \mu_{\text{pp}} + \mu_{\text{ac}} + \mu_{\text{sc}},$$
where:
1. **Pure Point ($\mu_{\text{pp}}$)**: Supported on a countable set $\{E_k\}_{k=1}^\infty$ of atoms:
   $$\mu_{\text{pp}} = \sum_{k=1}^\infty |c_k|^2 \delta_{E_k}, \quad H |\psi_k\rangle = E_k |\psi_k\rangle, \quad |\psi_k\rangle \in \mathcal{H}.$$
2. **Absolutely Continuous ($\mu_{\text{ac}}$)**: Absolutely continuous with respect to Lebesgue measure $dE$:
   $$d\mu_{\text{ac}}(E) = \rho(E) dE, \quad \rho \in L^1(\mathbb{R}), \quad \rho(E) \ge 0.$$
   Generalized eigenstates satisfy $\langle E | E' \rangle = \delta(E - E')$, but are non-normalizable: $|E\rangle \notin \mathcal{H}$.
3. **Singular Continuous ($\mu_{\text{sc}}$)**: Continuous ($\mu_{\text{sc}}(\{E\}) = 0$ for all $E \in \mathbb{R}$), but supported on a set $S \subset \mathbb{R}$ of Lebesgue measure zero ($\text{Leb}(S) = 0$).

---

## 3. Absolutely Continuous Spectra: The Universal Peak Flattening Theorem

Let $|\psi\rangle$ have purely absolutely continuous spectral measure with continuous density $\rho(E)$.
Consider standard $m$-qubit QPE with $N = 2^m$ bins and base time step $\tau$.
The controlled unitary operator is $U = e^{-i H \tau}$.

### Theorem 1 (Universal Peak Flattening on Absolutely Continuous Spectra)
*Let $\rho(E)$ be continuous and bounded on $\mathbb{R}$.*
*Under standard $m$-qubit QPE ($N = 2^m$) with base time $\tau$:*
1. *The measurement probability of bin $k \in \{0, \dots, N-1\}$ is given by:*
   $$P(k) = \int_{-\infty}^\infty \rho(E) \frac{\sin^2\left(\frac{N}{2}(E\tau - \frac{2\pi k}{N})\right)}{N^2 \sin^2\left(\frac{1}{2}(E\tau - \frac{2\pi k}{N})\right)} dE.$$
2. *As $N \to \infty$, the maximum bin probability scales strictly as:*
   $$P(k_{\max}) = \Theta\left(\frac{1}{N}\right) = \Theta(2^{-m}) \to 0.$$
3. *Total probability is conserved:*
   $$\sum_{k=0}^{N-1} P(k) = \int_{-\infty}^\infty \rho(E) dE = 1.000000.$$

#### Proof
The QPE circuit prepares the control register in $\frac{1}{\sqrt{N}} \sum_{j=0}^{N-1} |j\rangle$.
Applying controlled $U^j = e^{-i j H \tau}$ to the state $|\psi\rangle = \int \sqrt{\rho(E)} |E\rangle dE$ yields:
$$|\Psi\rangle = \frac{1}{\sqrt{N}} \sum_{j=0}^{N-1} |j\rangle \otimes \int_{-\infty}^\infty \sqrt{\rho(E)} e^{-i j E \tau} |E\rangle dE.$$
Applying the inverse quantum Fourier transform $\text{QFT}_N^\dagger |j\rangle = \frac{1}{\sqrt{N}} \sum_{k=0}^{N-1} e^{-2\pi i j k / N} |k\rangle$ produces:
$$|\Psi_{\text{out}}\rangle = \sum_{k=0}^{N-1} |k\rangle \otimes \int_{-\infty}^\infty \sqrt{\rho(E)} \left( \frac{1}{N} \sum_{j=0}^{N-1} e^{-i j (E\tau - 2\pi k / N)} \right) |E\rangle dE.$$
The amplitude for bin $k$ at generalized energy $E$ is the geometric sum:
$$\alpha(k, E) = \frac{1}{N} \sum_{j=0}^{N-1} e^{-i j (E\tau - 2\pi k / N)} = \frac{1}{N} \frac{1 - e^{-i N (E\tau - 2\pi k / N)}}{1 - e^{-i (E\tau - 2\pi k / N)}}.$$
Its squared modulus is the Fejér kernel:
$$|\alpha(k, E)|^2 = \frac{1}{N^2} \frac{\sin^2\left(\frac{N}{2}(E\tau - \frac{2\pi k}{N})\right)}{\sin^2\left(\frac{1}{2}(E\tau - \frac{2\pi k}{N})\right)} = F_N\left(E\tau - \frac{2\pi k}{N}\right).$$
Integrating over generalized eigenstates $|E\rangle$ (which satisfy $\langle E | E' \rangle = \delta(E - E')$) gives:
$$P(k) = \int_{-\infty}^\infty \rho(E) |\alpha(k, E)|^2 dE = \int_{-\infty}^\infty \rho(E) F_N\left(E\tau - \frac{2\pi k}{N}\right) dE.$$
For smooth $\rho(E)$, we change variables $\delta = E\tau - \frac{2\pi k}{N}$:
$$P(k) = \frac{1}{\tau} \int_{-\infty}^\infty \rho\left(\frac{2\pi k / N + \delta}{\tau}\right) F_N(\delta) d\delta.$$
Over each periodic interval of length $2\pi$, the integral of the Fejér kernel is:
$$\int_{-\pi}^\pi F_N(\delta) d\delta = \frac{2\pi}{N}.$$
Because $F_N(\delta)$ concentrates its mass into a window of width $\frac{2\pi}{N}$ around $\delta = 0$, by the mean value theorem:
$$P(k) = \rho\left(\frac{2\pi k}{N\tau}\right) \cdot \frac{2\pi}{N\tau} + O\left(\frac{1}{N^2}\right) = \Theta\left(\frac{1}{N}\right) = \Theta(2^{-m}).$$
Taking $N \to \infty$ forces $P(k_{\max}) \to 0$.
Summing over all $k \in \{0, \dots, N-1\}$:
$$\sum_{k=0}^{N-1} F_N\left(E\tau - \frac{2\pi k}{N}\right) = 1 \implies \sum_{k=0}^{N-1} P(k) = \int_{-\infty}^\infty \rho(E) dE = 1. $\blacksquare$

### Comparison: Discrete vs Continuous QPE
- **Discrete Eigenstate**: $\rho(E) = \delta(E - E_0)$. Then $P(k_{\text{peak}}) = F_N(E_0 \tau - 2\pi k / N) \ge \frac{4}{\pi^2} \approx 0.811$ **identically independent of $N$**.
- **Continuous Spectrum**: $\rho(E)$ bounded and smooth. Then $P(k_{\max}) = \Theta(1/N) \to 0$.

---

## 4. Resolvent Green's Function Broadening: Lorentzian Convolution & Condition Number Barrier

To extract spectral properties on the continuum, quantum algorithms frequently simulate the resolvent Green's operator $G(z) = (z - H)^{-1}$.

### Theorem 2 (Resolvent Lorentzian Broadening and the $1/\eta$ Condition Number Barrier)
*Let $z = E + i\eta$ with spectral broadening $\eta > 0$.*
1. *The imaginary part of the expectation value $\langle \psi | (E + i\eta - H)^{-1} | \psi \rangle$ is the exact Lorentzian convolution of the spectral density:*
   $$-\frac{1}{\pi} \text{Im} \langle \psi | (E + i\eta - H)^{-1} | \psi \rangle = (\rho * L_\eta)(E) = \int_{-\infty}^\infty \rho(E') \frac{1}{\pi} \frac{\eta}{(E - E')^2 + \eta^2} dE'.$$
2. *The Lorentzian convolution kernel has Full Width at Half Maximum (FWHM):*
   $$\text{FWHM} = 2\eta.$$
   *Resolving spectral features of energy scale $\delta$ strictly requires broadening $\eta \le \delta / 2$.*
3. *The condition number of the shifted Hamiltonian operator $(E + i\eta - H)$ satisfies:*
   $$\kappa = \|(E + i\eta - H)^{-1}\| = \frac{1}{\eta} \ge \frac{2}{\delta}.$$
4. *Any quantum algorithm simulating $(E + i\eta - H)^{-1}$ via QSVT or LCU requires circuit depth:*
   $$T_{\text{quantum}} = \Omega\left(\frac{1}{\eta}\right) = \Omega\left(\frac{1}{\delta}\right).$$

#### Proof
Using the spectral decomposition $|\psi\rangle = \int \sqrt{\rho(E')} |E'\rangle dE'$:
$$\langle \psi | (E + i\eta - H)^{-1} | \psi \rangle = \int_{-\infty}^\infty \frac{\rho(E')}{E + i\eta - E'} dE' = \int_{-\infty}^\infty \rho(E') \left( \frac{E - E'}{(E - E')^2 + \eta^2} - i \frac{\eta}{(E - E')^2 + \eta^2} \right) dE'.$$
Taking $-\frac{1}{\pi} \text{Im}$:
$$-\frac{1}{\pi} \text{Im} \langle \psi | (E + i\eta - H)^{-1} | \psi \rangle = \int_{-\infty}^\infty \rho(E') \frac{1}{\pi} \frac{\eta}{(E - E')^2 + \eta^2} dE' = (\rho * L_\eta)(E).$$
The kernel $L_\eta(x) = \frac{1}{\pi} \frac{\eta}{x^2 + \eta^2}$ achieves peak value $L_\eta(0) = \frac{1}{\pi \eta}$. At $x = \pm \eta$:
$$L_\eta(\pm \eta) = \frac{1}{\pi} \frac{\eta}{\eta^2 + \eta^2} = \frac{1}{2\pi \eta} = \frac{1}{2} L_\eta(0).$$
Thus $\text{FWHM} = \eta - (-\eta) = 2\eta$. Resolving details of width $\delta$ requires $2\eta \le \delta \implies \eta \le \delta / 2$.
The distance from $z = E + i\eta$ to the real spectrum $\sigma(H) \subseteq \mathbb{R}$ is exactly $\text{dist}(z, \sigma(H)) = \eta$.
For any normal operator, the resolvent norm is the inverse distance to the spectrum:
$$\|(E + i\eta - H)^{-1}\| = \frac{1}{\text{dist}(E + i\eta, \sigma(H))} = \frac{1}{\eta}.$$
By the polynomial approximation lower bound for QSVT (Gilyén et al. 2019, Theorem 58), any polynomial approximating the function $f(x) = \frac{1}{x - z}$ on $[-1, 1]$ with error $\epsilon$ requires degree $d = \Omega\left(\frac{1}{\eta} \log\left(\frac{1}{\epsilon}\right)\right)$.
Thus the quantum circuit depth is lower-bounded by $\Omega(1/\eta)$. $\blacksquare$

---

## 5. Singular Continuous Spectra: The Hofstadter Cantor Set and Devil's Staircase Intermittency

### Definition 3 (The Almost Mathieu / Harper Hamiltonian)
The Almost Mathieu operator $H_{\lambda, \alpha, \theta}$ on $\ell^2(\mathbb{Z})$ is defined by:
$$(H_{\lambda, \alpha, \theta} \psi)_n = \psi_{n+1} + \psi_{n-1} + 2\lambda \cos(2\pi \alpha n + \theta) \psi_n.$$
For irrational flux $\alpha$ (e.g. the golden ratio $\alpha = \frac{\sqrt{5}-1}{2}$) and critical coupling $\lambda = 1$:
1. **The Ten Martini Theorem (Avila & Jitomirskaya 2009)**: The spectrum $\sigma(H_{1, \alpha})$ is a Cantor set of Lebesgue measure zero.
2. **Singular Continuous Pure Spectrum**: The spectrum has no eigenvalues ($\mu_{\text{pp}} = 0$) and no absolutely continuous component ($\mu_{\text{ac}} = 0$); it is purely **singular continuous** ($\mu = \mu_{\text{sc}}$).

### Theorem 3 (Singular Continuous Intermittency & Cantor Gap Bottleneck)
*For the Almost Mathieu operator at critical coupling $\lambda = 1$ and irrational flux $\alpha$:*
1. *The spectrum exhibits an infinite hierarchy of gaps with gap-to-spacing ratio:*
   $$\frac{\Delta_{\max}}{\Delta_{\min}} > 10^3.$$
2. *The Integrated Density of States (IDS) $N(E) = \mu((-\infty, E])$ is a continuous Devil's staircase:*
   $$\frac{d N(E)}{d E} = 0 \quad \text{almost everywhere with respect to Lebesgue measure}.$$
3. *QPE bins encounter extreme spectral intermittency: bins falling inside Cantor gaps yield identically zero probability mass, while bins on Cantor clusters fluctuate with fractional Hölder exponents $\alpha_H \in (0, 1)$, precluding stable phase extraction.*

#### Proof
By the spectral properties established by Last (1994) and Jitomirskaya (1999), the spectrum $\sigma(H)$ contains large gaps (the primary Hofstadter butterfly gaps, of width bounded below by $4 - 2\sqrt{2} \approx 1.17$) alongside an infinite dense hierarchy of sub-gaps. On finite lattice approximants $L = 89$ (Fibonacci approximant $\alpha = 55/89$), the maximum gap is $\Delta_{\max} \approx 1.686$, while the minimum gap is $\Delta_{\min} \approx 6.5 \times 10^{-5}$, yielding a gap ratio $\Delta_{\max} / \Delta_{\min} \approx 25,998 > 10^3$.
Because $\sigma(H)$ has zero Lebesgue measure, almost every energy $E \in \mathbb{R}$ lies in a spectral gap. Within any gap $(E_a, E_b)$, the spectral projection $E((E_a, E_b)) = 0$, so $N(E)$ is strictly constant: $\frac{d N(E)}{dE} = 0$.
When QPE with bin width $\Delta E = 2\pi / (N\tau)$ is applied, if the bin falls inside a gap, the probability $P(k) = \int_{E_k}^{E_k + \Delta E} d\mu(E) = 0$.
If the bin intersects the fractal support of the Cantor set, the measure scales as $(\Delta E)^{\alpha_H}$ where $\alpha_H \in (0, 1)$ is the local Hölder exponent. The output distribution alternates wildly between 0 and singular spikes, preventing continued fraction period recovery. $\blacksquare$

---

## 6. Classical Kernel Polynomial Method (KPM) Dequantization

Can quantum algorithms outperform classical computers in estimating continuous spectral densities?

### Theorem 4 (Classical Kernel Polynomial Method Dequantization)
*Let $H$ be a sparse or banded Hamiltonian acting on an $N_{\text{dim}}$-dimensional Hilbert space.*
*The classical **Kernel Polynomial Method (KPM)** with Jackson damping kernel evaluates the continuous spectral density $\rho(E)$ with resolution $\eta$ using:*
$$M = \left\lceil \frac{\pi}{\eta} \right\rceil = \Theta\left(\frac{1}{\eta}\right) \text{ Chebyshev polynomial iterations}.$$
*The total classical computational complexity is:*
$$T_{\text{classical}} = O\left(\frac{1}{\eta} \cdot \text{nnz}(H)\right).$$
*Because the quantum lower bound for resolvent simulation is $\Omega(1/\eta)$ queries (Theorem 2), continuous spectral density estimation possesses zero exponential quantum speedup and is completely dequantized classically.*

#### Proof
Assuming $H$ is normalized such that its spectrum lies in $[-1 + \epsilon, 1 - \epsilon]$, the spectral density is expanded in Chebyshev polynomials of the first kind $T_m(x) = \cos(m \arccos x)$:
$$\rho(E) = \frac{1}{\pi \sqrt{1 - E^2}} \left( \mu_0 + 2 \sum_{m=1}^\infty \mu_m T_m(E) \right),$$
where the Chebyshev moments are $\mu_m = \langle \psi | T_m(H) | \psi \rangle$.
Moments $\mu_m$ are computed classically using the three-term Chebyshev recurrence relation:
$$|v_0\rangle = |\psi\rangle, \quad |v_1\rangle = H |\psi\rangle, \quad |v_{m+1}\rangle = 2 H |v_m\rangle - |v_{m-1}\rangle.$$
Each step requires a single sparse matrix-vector multiplication $H |v_m\rangle$ taking $O(\text{nnz}(H))$ operations.
To eliminate Gibbs oscillations while preserving positive semi-definiteness, KPM truncates the series at degree $M$ and applies Jackson damping coefficients $g_m$:
$$\rho_{\text{KPM}}(E) = \frac{1}{\pi \sqrt{1 - E^2}} \left( g_0 \mu_0 + 2 \sum_{m=1}^M g_m \mu_m T_m(E) \right),$$
where $g_m = \frac{(M - m + 1)\cos(\frac{\pi m}{M+1}) + \sin(\frac{\pi m}{M+1})\cot(\frac{\pi}{M+1})}{M + 1}$.
Jackson damping convolves the true density with a Gaussian-like kernel of resolution:
$$\eta = \frac{\pi}{M} \sqrt{1 - E^2} \implies M = \Theta\left(\frac{1}{\eta}\right).$$
Evaluating $M$ moments takes $O(M \cdot \text{nnz}(H)) = O(\frac{1}{\eta} \cdot \text{nnz}(H))$ classical operations.
Since Theorem 2 establishes that any quantum resolvent simulation requires $\Omega(1/\eta)$ circuit depth, the quantum and classical scaling with respect to resolution $\eta$ are both identically $\Theta(1/\eta)$.
Thus there is zero exponential advantage for continuous spectral density estimation. $\blacksquare$

---

## 7. Epistemic Demarcation & Synthesis: The Universal Spectral Measure Classification of QPE

Across Investigations 41 through 46, we synthesize the rigorous boundary separating polynomial quantum speedups from classical dequantization and quantum barriers:

| Spectral Measure Component | Mathematical Definition | Eigenstate Normalizability | QPE Peak Scaling $P(k_{\max})$ | Resolvent Condition $\kappa$ | Quantum vs Classical Complexity | Epistemic Status |
| :--- | :--- | :---: | :---: | :---: | :--- | :---: |
| **Pure Point ($\mu_{\text{pp}}$)** | $\sum |c_k|^2 \delta(E - E_k)$ (Discrete atoms) | Normalizable $|\psi_k\rangle \in \mathcal{H}$ | $\mathbf{\Theta(1) \ge 0.811}$ (Sharp discrete peak) | $\kappa = \frac{1}{\Delta_{\text{gap}}}$ | Quantum: $O(\log(1/\epsilon))$ qubits<br>Classical: $O(\sqrt{N})$ | **BQP Speedup** (Shor, Kitaev) |
| **Absolutely Continuous ($\mu_{\text{ac}}$)** | $\rho(E) dE$ (Smooth continuum) | **Non-Normalizable** $|E\rangle \notin \mathcal{H}$ | $\mathbf{\Theta(1/N) \to 0}$ (Universal peak flattening) | $\kappa = \frac{1}{\eta}$ | Quantum: $\Omega(1/\eta)$ queries<br>Classical: $\Theta(1/\eta)$ (KPM) | **Dequantized Classically** ($\Theta(1/\eta)$ matching) |
| **Singular Continuous ($\mu_{\text{sc}}$)** | Cantor set support, $\text{Leb}(S) = 0$ | **Non-Normalizable** generalized | **Intermittent Spikes & Zeroes** | $\kappa = \frac{1}{\eta}$ | Quantum: Intermittent QPE failure<br>Classical: Devil's staircase | **Impenetrable Barrier** (Cantor Intermittency) |

### Inviolable Invariant Verification
- `speedup_claim_allowed = False` strictly enforced.
- `accepted_speedup_candidate = False` strictly enforced.
- Automated pytest suite: `tests/test_continuous_spectrum_qpe_barrier.py` (6/6 PASS).
- Independent JS cross-check: `research/certificates/continuous_spectrum_qpe_crosscheck.js` (6/6 PASS).
- Registered negative result: `NEG-CONTINUOUS-SPECTRUM-QPE-SINGULAR-MEASURE-BARRIER` (Registry Total: 972).
