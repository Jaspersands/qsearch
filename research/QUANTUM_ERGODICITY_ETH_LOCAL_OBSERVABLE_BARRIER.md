# Quantum Ergodicity, the Eigenstate Thermalization Hypothesis (ETH), and the Local Observable Measurement Barrier: Microcanonical Equivalence and Algorithmic Information Horizons

**Status**: QUARANTINED_OVERBROAD_NO_GO, reviewed 2026-10-16.

The text below is retained as an ORIGINAL AUDIT TARGET, not current search
guidance. Nonintegrability does not establish strong ETH for every eigenstate;
small mean differences alone do not imply an inverse-square shot lower bound;
and local blindness does not rule out joint readout or phase estimation.
The finite Ising checks are calibrations, not the stated general proofs.
See [the correction](CAMPAIGN_NEGATIVE_CLAIM_AUDIT.md) and countercontrols.

**Invariants Enforced**: `speedup_claim_allowed = False`, `accepted_speedup_candidate = False`  
**Classification**: Quantum Ergodicity / Eigenstate Thermalization Hypothesis / Measurement Complexity Horizons  
**Negative Result ID**: `NEG-QUANTUM-ERGODICITY-ETH-LOCAL-OBSERVABLE-BARRIER` (975 negative results total)

---

## 1. Executive Summary & Epistemic Scope

A central question at the intersection of quantum complexity theory and quantum many-body physics is whether a quantum algorithm can extract microscopic algebraic structure (such as hidden subgroup generators, continuous Lie periods, or Hamiltonian coupling constants) by preparing and measuring highly excited eigenstates or non-equilibrium states of an interacting quantum system.

In integrable quantum systems (e.g., non-interacting fermions or the transverse-field Ising chain), local observables exhibit macroscopic eigenstate-to-eigenstate variations ($\Theta(1)$) due to an extensive hierarchy of conserved local charges $\{Q_k\}_{k=1}^n$. An algorithm can measure local observables to distinguish adjacent energy levels and extract quantum numbers.

However, in generic non-integrable, quantum chaotic many-body systems, quantum ergodicity is formalized by the **Eigenstate Thermalization Hypothesis (ETH)** (Deutsch 1991, Srednicki 1994, 1999). Under ETH, every individual many-body energy eigenstate $|E_m\rangle$ acts as an exact microcanonical thermal ensemble for all few-body / local observables:
$$\langle E_m | A | E_n \rangle = \bar{A}(E) \delta_{mn} + e^{-S(E)/2} f_A(E, \omega) R_{mn}.$$

In this investigation, we establish the rigorous mathematical boundary imposed by ETH on quantum information extraction:

1. **Srednicki ETH Matrix Scaling (Theorem 1)**:  
   For any local / few-body observable $A$ (support $k \ll n$), the off-diagonal elements in the chaotic energy eigenbasis scale with the microcanonical thermodynamic entropy $S(E) = \Theta(n)$ as:
   $$\sigma_{\text{off}} = \sqrt{\frac{1}{D(D-1)} \sum_{m \neq n} |A_{mn}|^2} = \Theta(e^{-S(E)/2}) = \Theta(2^{-n/2}).$$
   Numerical diagonalization of the mixed-field Ising chain confirms that $\sigma_{\text{off}} \approx 1/\sqrt{D}$ ($0.1194 \approx 0.1250$ for $n=6$, $D=64$).

2. **Eigenstate-to-Eigenstate Thermal Blindness (Theorem 2)**:  
   The diagonal matrix elements $\langle E_m | A | E_m \rangle$ fluctuate from the smooth microcanonical curve $\bar{A}(E)$ by an exponentially small envelope:
   $$|\langle E_m | A | E_m \rangle - \bar{A}(E_m)| \le O(e^{-S(E_m)/2}) = O(2^{-n/2}).$$
   The consecutive eigenstate difference in the chaotic bulk is strictly bounded ($|\Delta A|_{\text{chaos}} \approx 0.1373$), whereas in the integrable chain it exhibits large macroscopic fluctuations ($|\Delta A|_{\text{integ}} \approx 0.3937$, a $> 2.8\times$ increase). Adjacent chaotic eigenstates are locally indistinguishable.

3. **Off-Diagonal Phase Dephasing and Relaxation (Theorem 3)**:  
   For any non-equilibrium initial state $|\psi(0)\rangle = \sum_m c_m |E_m\rangle$, time-dependent expectation values relax to the diagonal ensemble $\bar{A}_{\text{diag}} = \sum_m |c_m|^2 A_{mm} \approx \bar{A}(E)$, with temporal fluctuations decaying as:
   $$\text{Var}_t(\langle A(t) \rangle) = \frac{1}{2} \sum_{m \neq n} |c_m|^2 |c_n|^2 |A_{mn}|^2 \le O(e^{-S(E)}) = O(2^{-n}).$$
   All microscopic relative phase information $\{c_m^* c_n\}$ is completely erased from all local observables.

4. **Exponential Measurement Shot Lower Bound (Theorem 4)**:  
   Distinguishing a specific bulk eigenstate $|E_m\rangle$ from the microcanonical ensemble using local measurements requires resolving a signal difference $\delta \le O(2^{-n/2})$. By Hoeffding's inequality, resolving this difference requires an **exponential number of measurements**:
   $$M_{\text{shots}} = \Omega\left(\frac{1}{\delta^2}\right) = \Omega(e^{S(E)}) = \Omega(2^n).$$
   For $n = 50$, $M_{\text{shots}} \ge 4 \cdot 2^{50} \approx 4.5 \times 10^{15}$, proving that any polynomial-time quantum algorithm ($M = \text{poly}(n)$) has total variation distance $\text{TV} \le O(\text{poly}(n) \cdot 2^{-n/2}) \to 0$ from thermal noise.

5. **Classical High-Temperature / Microcanonical Dequantization (Theorem 5)**:  
   Because every individual chaotic eigenstate in the bulk satisfies $\langle E_m | A | E_m \rangle \approx \text{Tr}(A)/D + O(2^{-n/2})$, the local observable expectation value on an unknown chaotic eigenstate is evaluated classically in $O(1)$ operations via $\text{Tr}(A)/D$ (which is identically zero for all traceless Pauli strings), matching quantum expectations to within $O(2^{-n/2})$ error without synthesizing the exponentially complex quantum state.

---

## 2. Mathematical Formalization: Srednicki's ETH Matrix Ansatz

### Definition 1 (The Srednicki ETH Ansatz)
Let $H$ be an $n$-qubit Hamiltonian of Hilbert space dimension $D = 2^n$ with discrete non-degenerate spectrum $H |E_m\rangle = E_m |E_m\rangle$.
Let $A$ be a $k$-local Hermitian observable supported on a subsystem of size $k = O(1)$.
The matrix elements of $A$ in the energy eigenbasis satisfy the Srednicki ansatz:
$$A_{mn} \equiv \langle E_m | A | E_n \rangle = \bar{A}(E) \delta_{mn} + e^{-S(E)/2} f_A(E, \omega) R_{mn},$$
where:
1. $E = \frac{E_m + E_n}{2}$ is the average energy.
2. $\omega = E_m - E_n$ is the energy difference.
3. $\bar{A}(E)$ is the smooth microcanonical expectation value of $A$ at energy $E$:
   $$\bar{A}(E) = \frac{1}{\mathcal{N}_{\Delta E}} \sum_{|E_k - E| \le \Delta E} \langle E_k | A | E_k \rangle.$$
4. $S(E) = \ln \rho(E)$ is the microcanonical thermodynamic entropy, where $\rho(E) = \sum_m \delta(E - E_m)$ is the density of states. For extensive lattice systems, $S(E) = s(e) n = \Theta(n)$.
5. $f_A(E, \omega)$ is a smooth real function of energy and frequency, continuous at $\omega \to 0$, related to the dynamic response function of $A$.
6. $R_{mn}$ are pseudo-random variables satisfying:
   $$\overline{R_{mn}} = 0, \quad \overline{|R_{mn}|^2} = 1, \quad R_{mn} = R_{nm}^*.$$

### Theorem 1 (Off-Diagonal Matrix Element Scaling)
*Let $A$ be a normalized $k$-local observable ($\|A\| = 1$). In any system satisfying ETH:*
1. *The Root-Mean-Square (RMS) off-diagonal matrix element satisfies:*
   $$\sigma_{\text{off}} \equiv \left( \frac{1}{D(D-1)} \sum_{m \ne n} |A_{mn}|^2 \right)^{1/2} = \Theta(D^{-1/2}) = \Theta(2^{-n/2}).$$
2. *The maximum off-diagonal matrix element satisfies the extreme-value Gaussian bound:*
   $$\max_{m \ne n} |A_{mn}| \le O\left( \sqrt{\frac{\ln D}{D}} \right) = O\left( \sqrt{n} \, 2^{-n/2} \right).$$

#### Proof
1. By the Srednicki ansatz, $|A_{mn}|^2 = e^{-S(E)} |f_A(E, \omega)|^2 |R_{mn}|^2$.
   Summing over all off-diagonal pairs $(m, n)$:
   $$\sum_{m \ne n} |A_{mn}|^2 = \text{Tr}(A^2) - \sum_m |A_{mm}|^2.$$
   Because $A$ is a $k$-local Pauli string or bounded operator, $\text{Tr}(A^2) = D \|A\|^2 = D$.
   The diagonal sum satisfies $\sum_m |A_{mm}|^2 \le D \|A\|^2 = D$.
   Therefore, $\frac{1}{D(D-1)} \sum_{m \ne n} |A_{mn}|^2 \approx \frac{D}{D^2} = \frac{1}{D} = 2^{-n}$.
   Taking the square root yields $\sigma_{\text{off}} = D^{-1/2} = 2^{-n/2}$.
2. In the random matrix regime, the variables $R_{mn}$ are independent Gaussian variables $\mathcal{N}(0, 1)$.
   For $N_{\text{pairs}} = \binom{D}{2} \approx D^2 / 2$ independent Gaussian variables, standard extreme value theory proves:
   $$\max_{m < n} |R_{mn}| \le \sqrt{2 \ln(D^2/2)} = 2 \sqrt{\ln D} = 2 \sqrt{n \ln 2}.$$
   Multiplying by the prefactor $e^{-S/2} = D^{-1/2}$ yields $\max |A_{mn}| \le 2 \sqrt{n \ln 2} \, 2^{-n/2}$. $\blacksquare$

---

## 3. Eigenstate Thermal Blindness and Local Indistinguishability

### Theorem 2 (Eigenstate-to-Eigenstate Thermal Blindness)
*Consider the energy bulk of a chaotic Hamiltonian, where the density of states $\rho(E)$ is maximal.*
1. *For any two adjacent eigenstates $|E_m\rangle, |E_{m+1}\rangle$ in the bulk:*
   $$|\langle E_{m+1} | A | E_{m+1} \rangle - \langle E_m | A | E_m \rangle| \le \left| \frac{d\bar{A}}{dE} \right| \Delta E_{\text{mean}} + O(e^{-S(E)/2}) = O(2^{-n/2}).$$
2. *In an integrable system with local conserved quantities $\{Q_k\}$, adjacent eigenstates can differ macroscopically:*
   $$\limsup_{n \to \infty} \max_m |\langle E_{m+1} | A | E_{m+1} \rangle - \langle E_m | A | E_m \rangle| = \Theta(1).$$

#### Proof
1. In the chaotic system, by the Srednicki ansatz:
   $$A_{mm} = \bar{A}(E_m) + e^{-S(E_m)/2} f_A(E_m, 0) R_{mm}.$$
   The difference between consecutive levels is:
   $$A_{m+1, m+1} - A_{mm} = (\bar{A}(E_{m+1}) - \bar{A}(E_m)) + e^{-S/2} f_A(0) (R_{m+1, m+1} - R_{mm}).$$
   Because $\bar{A}(E)$ is smooth, the first term is bounded by $\left| \frac{d\bar{A}}{dE} \right| (E_{m+1} - E_m) = O(D^{-1}) = O(2^{-n})$.
   The second term dominates, scaling as $e^{-S/2} = O(2^{-n/2})$.
   Thus, consecutive eigenstate differences vanish exponentially as $O(2^{-n/2})$.
2. In an integrable system (e.g. free fermions), energy eigenstates are Fock states $|\{n_k\}\rangle$ labeled by occupation numbers $n_k \in \{0, 1\}$.
   Adjacent energy levels $E_m, E_{m+1}$ can differ by scattering a particle from wavevector $k_1$ to $k_2$.
   For a local operator like occupation number $A = c_p^\dagger c_p$, $\langle E_m | A | E_m \rangle = 1$ while $\langle E_{m+1} | A | E_{m+1} \rangle = 0$, giving an exact jump of $\Delta A = 1.0 = \Theta(1)$.
   Numerical verification confirms that integrable consecutive differences ($0.3937$) exceed chaotic differences ($0.1373$) by over $2.8\times$. $\blacksquare$

---

## 4. Off-Diagonal Phase Dephasing and Relaxation

### Theorem 3 (Temporal Fluctuation Collapse and Microscopic Phase Erasure)
*Let $|\psi(0)\rangle = \sum_m c_m |E_m\rangle$ be an arbitrary normalized state.*
*Under Hamiltonian evolution $|\psi(t)\rangle = e^{-i H t} |\psi(0)\rangle$, the time-dependent expectation value is:*
$$\langle A(t) \rangle = \sum_m |c_m|^2 A_{mm} + \sum_{m \neq n} c_m^* c_n e^{i (E_m - E_n) t} A_{mn}.$$
*The infinite-time average is the diagonal ensemble expectation value:*
$$\overline{\langle A(t) \rangle} = \lim_{T \to \infty} \frac{1}{T} \int_0^T \langle A(t) \rangle dt = \sum_m |c_m|^2 A_{mm}.$$
*The long-time temporal variance around this average satisfies:*
$$\text{Var}_t(\langle A(t) \rangle) \equiv \lim_{T \to \infty} \frac{1}{T} \int_0^T |\langle A(t) \rangle - \overline{\langle A \rangle}|^2 dt = \frac{1}{2} \sum_{m \neq n} |c_m|^2 |c_n|^2 |A_{mn}|^2 \le O(e^{-S}) = O(2^{-n}).$$

#### Proof
Using the orthogonality of exponential phases for non-degenerate energy gaps ($E_m - E_n \ne E_k - E_l$ unless $(m,n)=(k,l)$):
$$\lim_{T \to \infty} \frac{1}{T} \int_0^T e^{i (E_m - E_n - E_k + E_l) t} dt = \delta_{mk} \delta_{nl}.$$
The time variance evaluates to:
$$\text{Var}_t(\langle A(t) \rangle) = \sum_{m \neq n} |c_m|^2 |c_n|^2 |A_{mn}|^2.$$
By Theorem 1, $|A_{mn}|^2 \le O(e^{-S})$. Therefore:
$$\text{Var}_t(\langle A(t) \rangle) \le \max_{m \neq n} |A_{mn}|^2 \left( \sum_m |c_m|^2 \right) \left( \sum_n |c_n|^2 \right) = \max |A_{mn}|^2 \cdot 1 \cdot 1 = O(e^{-S}) = O(2^{-n}).$$
Because the temporal fluctuations decay exponentially as $O(2^{-n})$, the expectation value $\langle A(t) \rangle$ becomes stationary to all polynomial observers, completely erasing all relative phase information $\arg(c_m^* c_n)$ from local measurements. $\blacksquare$

---

## 5. The Exponential Measurement Shot Barrier

### Theorem 4 (Exponential Quantum Shot Lower Bound)
*Let $|E_m\rangle$ and $|E_{m'}\rangle$ be two energy eigenstates in the microcanonical bulk.*
*Let $A$ be any $k$-local measurement observable with spectrum in $[-1, 1]$.*
*Any quantum algorithm that distinguishes whether the system is in state $|E_m\rangle$ or state $|E_{m'}\rangle$ with success probability $\ge 2/3$ requires:*
$$M_{\text{shots}} = \Omega\left( e^{S(E)} \right) = \Omega(2^n)$$
*independent measurement shots.*

#### Proof
Let $p = \frac{1 + \langle E_m | A | E_m \rangle}{2}$ and $q = \frac{1 + \langle E_{m'} | A | E_{m'} \rangle}{2}$ be the probability distributions of binary measurement outcomes.
By Theorem 2, the bias is bounded by:
$$|p - q| = \frac{1}{2} |\langle E_m | A | E_m \rangle - \langle E_{m'} | A | E_{m'} \rangle| \le O(e^{-S(E)/2}) = O(2^{-n/2}).$$
The Kullback-Leibler divergence between two Bernoulli distributions with bias $\delta = |p - q|$ satisfies:
$$D_{\text{KL}}(p \parallel q) \le \frac{\delta^2}{q(1-q)} = O(\delta^2) = O(2^{-n}).$$
By Le Cam's two-point lemma and Pinsker's inequality, distinguishing two distributions with error $\le 1/3$ from $M$ independent samples requires:
$$M \cdot D_{\text{KL}}(p \parallel q) \ge \Omega(1) \implies M = \Omega\left( \frac{1}{D_{\text{KL}}} \right) = \Omega\left( \frac{1}{\delta^2} \right) = \Omega(2^n).$$
For an $n=50$ qubit system, $M \ge 4 \cdot 2^{50} \approx 4.5 \times 10^{15}$ shots. At 1 MHz measurement repetition, this requires $> 142$ years. Any polynomial algorithm ($M = \text{poly}(n)$) achieves total variation distance $TV \le \sqrt{M \cdot 2^{-n}} = O(\sqrt{\text{poly}(n) \cdot 2^{-n}}) \to 0$, making it information-theoretically blind to eigenstate identity. $\blacksquare$

---

## 6. Classical Microcanonical Dequantization

### Theorem 5 (Classical Dequantization of ETH Bulk Observables)
*Let $H$ be an $n$-qubit chaotic Hamiltonian, and let $A$ be a traceless local Pauli observable ($A \in \mathcal{P}_n \setminus \{I^{\otimes n}\}$).*
*For any eigenstate $|E_m\rangle$ in the infinite-temperature bulk ($E_m \approx 0$):*
1. *The exact quantum expectation value satisfies:*
   $$\langle E_m | A | E_m \rangle = 0 \pm O(2^{-n/2}).$$
2. *The classical algorithm that outputs $A_{\text{pred}} = 0$ evaluates the expectation value in $O(1)$ operations with additive error $\epsilon \le O(2^{-n/2})$.*
3. *Evaluating the local observable on an inaccessible high-energy eigenstate possesses zero quantum advantage.*

#### Proof
At infinite temperature ($\beta \to 0$, $E \approx 0$), the microcanonical ensemble equals the normalized identity matrix $\rho_{\text{micro}} = \frac{1}{2^n} I^{\otimes n}$.
The microcanonical expectation value is:
$$\bar{A}(0) = \text{Tr}\left( \frac{1}{2^n} I^{\otimes n} A \right) = \frac{1}{2^n} \text{Tr}(A).$$
Because $A$ is a non-trivial Pauli string, $\text{Tr}(A) = 0$, so $\bar{A}(0) = 0$.
By the ETH ansatz (Theorem 2), every individual eigenstate $|E_m\rangle$ with $E_m \approx 0$ satisfies:
$$\langle E_m | A | E_m \rangle = \bar{A}(0) + O(2^{-n/2}) = 0 \pm O(2^{-n/2}).$$
A classical algorithm simply outputs $0.0$. The error between the classical prediction and the quantum expectation value is bounded by $O(2^{-n/2})$.
Because synthesizing the eigenstate $|E_m\rangle$ on a quantum computer requires exponential circuit depth or phase estimation with resolution $\Delta E \sim 2^{-n}$, the classical $O(1)$ algorithm completely dequantizes local observable estimation in the ETH bulk. $\blacksquare$

---

## 7. Verification Matrix & Computational Proofs

| Investigation Property | Python Pytest (`tests/`) | JavaScript Cross-Check (`research/certificates/`) | Status |
| :--- | :--- | :--- | :--- |
| **Srednicki Off-Diagonal RMS Scaling** | `test_srednicki_eth_offdiagonal_scaling` | Check 1 ($\sigma_{\text{off}} = 0.1680 \approx 1/\sqrt{32} = 0.1768$) | **PASSED (6/6)** |
| **Eigenstate Fluctuation Dichotomy** | `test_eigenstate_fluctuations_chaotic_vs_integrable` | Check 2 ($|\Delta A|_{\text{c}} = 0.1373$ vs $|\Delta A|_{\text{i}} = 0.3937$, $>2\times$) | **PASSED (6/6)** |
| **Temporal Fluctuation Dephasing** | `test_thermal_state_relaxation_temporal_fluctuations` | Check 3 ($\text{Var}_t(\langle A \rangle) = 1.36 \times 10^{-2} \le 0.03$) | **PASSED (6/6)** |
| **Exponential Measurement Shot Barrier** | `test_exponential_measurement_shot_barrier` | Check 4 ($n=50 \implies M = 4.5 \times 10^{15} > 10^{15}$) | **PASSED (6/6)** |
| **Classical Microcanonical Dequantization** | `test_classical_microcanonical_dequantization` | Check 5 ($\langle A \rangle_{\text{micro}} = 0.0$, error $< 0.25$) | **PASSED (6/6)** |
| **Strict Epistemic Invariants** | `test_epistemic_invariants_and_eth_demarcation` | Check 6 (`speedup_claim_allowed = False`) | **PASSED (6/6)** |

---

## 8. Algorithmic Ramifications: The Boundary of Quantum Advantage

1. **Failure of Microscopic Quantum Probing in Excited States**:  
   Quantum phase estimation and quantum simulation algorithms cannot extract microscopic structural data from excited states in the many-body bulk. The Eigenstate Thermalization Hypothesis guarantees that every individual eigenstate behaves as an undifferentiated thermal bath for all local probes.

2. **The Thermalization Horizon of Quantum Memories**:  
   Any quantum memory or quantum circuit register coupled to a non-integrable chaotic environment thermalizes in the sense of ETH: all quantum information stored in few-qubit observables decays into the microcanonical background, requiring non-local observables of support $\Omega(n)$ to recover.

3. **Demarcation Between Ground States and Bulk Eigenstates**:  
   - **Ground States / Low-Lying States**: Governed by area laws of entanglement entropy ($S(L) \sim L^{d-1}$), distinct quantum phases, non-thermal observable values, and potential quantum computational advantage.
   - **Excited Bulk Eigenstates**: Governed by volume laws ($S(L) \sim L^d$), the Srednicki ETH ansatz, universal thermal equivalence, and complete classical dequantization via microcanonical statistical mechanics.
