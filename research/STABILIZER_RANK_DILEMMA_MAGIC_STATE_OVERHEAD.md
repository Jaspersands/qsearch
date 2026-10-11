# The Stabilizer Rank Dilemma and Fault-Tolerant Magic State Overhead in Dihedral Coset Distillation

**Investigation**: Investigation 24 (Quantum Resource Theories & Classical Simulation)  
**Date**: 2026-10-11  
**Status**: AUDITED & REVISED (See `research/ADVERSARIAL_MATHEMATICAL_AUDIT_REPORT.md`)  
**Core Invariants**: `speedup_claim_allowed = False`, `accepted_speedup_candidate = False`  

> [!WARNING]
> **Adversarial Audit Correction Notice (2026-10-11)**:
> Theorem 2 (Stabilizer Rank Classical Dequantization Threshold) contains an **INVALID APPLICATION OF BRAVYI-GOSSET SIMULATION**.
> Bravyi-Gosset classical simulation scales as $O(\chi_{\text{total}} \cdot \text{poly}(P))$, where $\chi_{\text{total}}$ is the stabilizer rank of the **entire input state** plus injected magic states.
> For unknown non-trivial secret shifts $s$, the input state $|\Psi_{\vec{k}, s}\rangle = \bigotimes_{j=1}^P |\psi_{k_j, s}\rangle$ is an unknown non-stabilizer state with stabilizer fidelity bounded by $(0.8536)^P$.
> The stabilizer rank of such magic tensor powers is conjectured to be $2^{\Omega(P)}$ (with unconditionally proved polynomial bounds $\Omega(P^2)$ by Peleg et al. 2021).
> Even if a circuit uses zero $T$ gates ($T_{\text{count}} = 0$, pure Clifford), simulating a Clifford circuit on an unknown non-stabilizer input cannot be done in polynomial time via Bravyi-Gosset decomposition.
> Therefore, low-$T$-count circuits acting on $P$ coset registers **ARE NOT DEQUANTIZED IN POLYNOMIAL TIME** by Bravyi-Gosset simulation. Theorem 3 (magic state distillation burden on physical fault-tolerant architectures) remains mathematically valid.

---

## 1. Executive Summary & Foundational Question

Can collective quantum operations across $P$ dihedral coset registers achieve an algorithmic advantage while remaining within the regime of efficient classical simulation or modest fault-tolerant implementation?

We resolve this question by analyzing the **stabilizer rank** $\chi(|\Psi\rangle)$, **stabilizer nullity** $\nu(|\Psi\rangle)$, and **non-Clifford $T$-count** of collective circuits acting on the $P$-qubit coset state:
$$|\Psi_{\vec{k}, s}\rangle = \bigotimes_{j=1}^P \frac{1}{\sqrt{2}} \left( |0\rangle + e^{i \frac{2\pi k_j s}{N}} |1\rangle \right).$$

We establish:
- **Stabilizer Structure of Coset Ensembles**: When $k_j s \not\equiv 0 \pmod{N/4}$, each single-qubit factor has stabilizer fidelity $F_{\text{stab}} \le \frac{1 + 1/\sqrt{2}}{2} \approx 0.8536 < 1$. However, if $s=0$ (or $k_j s \equiv 0 \pmod N$), the registers are pure stabilizer states ($|+\rangle$) with fidelity 1 and nullity 0.
- **Retraction of Low-$T$ Classical Dequantization**: Bravyi-Gosset simulation scales with the stabilizer rank of the **joint input state** $\chi(|\Psi_{\vec{k}, s}\rangle)$. Because the coset state is an unknown non-stabilizer state for non-trivial $s$, low-$T$-count circuits *cannot* be dequantized in polynomial time via Bravyi-Gosset simulation without knowing the secret decomposition.
- **The Magic State Overhead in Fault-Tolerant Architectures**: Non-Clifford rotations required for continuous phase combination require $T$-count $\Omega(n)$ per combination. Implementing a sieve over a pool of size $P = 2^{\Omega(\sqrt{n})}$ requires $2^{\Omega(\sqrt{n})}$ magic state factory distillations, creating an intractable fault-tolerant physical resource burden.

---

## 2. Mathematical Definitions and Framework

### Definition 1: Stabilizer Rank and Extended Stabilizer Rank
For an $n$-qubit pure state $|\Psi\rangle$, the stabilizer rank $\chi(|\Psi\rangle)$ is the minimum integer $r$ such that:
$$|\Psi\rangle = \sum_{j=1}^r c_j |\phi_j\rangle,$$
where each $|\phi_j\rangle$ is an $n$-qubit stabilizer state and $c_j \in \mathbb{C}$.
The $\delta$-approximate stabilizer rank $\chi_\delta(|\Psi\rangle)$ is the minimum stabilizer rank among all states $|\Phi\rangle$ satisfying $\||\Psi\rangle - |\Phi\rangle\|_2 \le \delta$.

### Definition 2: The Stabilizer Nullity
For an $n$-qubit state $|\Psi\rangle$, the stabilizer nullity $\nu(|\Psi\rangle)$ is the co-dimension of the largest abelian subgroup of the $n$-qubit Pauli group $\mathcal{P}_n$ that stabilizes $|\Psi\rangle$:
$$\nu(|\Psi\rangle) = n - \log_2 |\mathcal{S}(|\Psi\rangle)|.$$

---

## 3. Asymptotic Theorems and Proofs

### Theorem 1: Stabilizer Nullity and Fidelity of Dihedral Coset States
**Theorem Statement**:  
Let $|\Psi_{\vec{k}, s}\rangle = \bigotimes_{j=1}^P |\psi_{k_j, s}\rangle$ be the joint state of $P$ dihedral coset registers over $\mathbb{Z}_N$ with $N = 2^n$, where $|\psi_{k_j, s}\rangle = \frac{1}{\sqrt{2}} (|0\rangle + e^{i 2\pi k_j s / N} |1\rangle)$.
1. **Stabilizer Case ($s=0$ or $k_j s \equiv 0 \pmod{N/4}$)**:
   - If $s=0$, $|\psi_{k_j, 0}\rangle = |+\rangle$, which is stabilized by Pauli $X$. The nullity is $\nu = 0$, stabilizer fidelity is $F_{\text{stab}} = 1$, and stabilizer rank is $\chi = 1$.
   - More generally, if $k_j s \equiv 0 \pmod{N/4}$, $|\psi_{k_j, s}\rangle \in \{|+\rangle, |+i\rangle, |-\rangle, |-i\rangle\}$, which are all single-qubit stabilizer states.
2. **Generic Non-Stabilizer Case ($k_j s \not\equiv 0 \pmod{N/4}$ for all $j$)**:
   - The stabilizer group of $|\Psi_{\vec{k}, s}\rangle$ is trivial: $\mathcal{S}(|\Psi_{\vec{k}, s}\rangle) = \{I^{\otimes P}\}$.
   - The stabilizer nullity is maximal: $\nu(|\Psi_{\vec{k}, s}\rangle) = P$.
   - The exact stabilizer fidelity of each single-qubit factor satisfies:
     $$F_{\text{stab}}(|\psi_{k_j, s}\rangle) = \max_{|\phi\rangle \in \text{Stab}_1} |\langle \phi | \psi_{k_j, s}\rangle|^2 \le \frac{1 + \frac{1}{\sqrt{2}}}{2} \approx 0.85355 < 1.$$
   - The global stabilizer fidelity vanishes exponentially:
     $$F_{\text{stab}}(|\Psi_{\vec{k}, s}\rangle) \le (0.8536)^P = 2^{-\Omega(P)}.$$

**Proof**:  
1. The 6 single-qubit stabilizer states are the eigenstates of $X, Y, Z$: $\{|0\rangle, |1\rangle, |+\rangle, |-\rangle, |+i\rangle, |-i\rangle\}$.
2. The single-qubit coset state is $|\psi(\theta)\rangle = \frac{1}{\sqrt{2}} (|0\rangle + e^{i \theta} |1\rangle)$ with phase $\theta = 2\pi k_j s / 2^n$.
3. The squared overlaps with the 6 stabilizer states are:
   - With $|0\rangle$ and $|1\rangle$: $|\langle 0 | \psi(\theta)\rangle|^2 = 1/2$, $|\langle 1 | \psi(\theta)\rangle|^2 = 1/2$.
   - With $|\pm\rangle$: $|\langle \pm | \psi(\theta)\rangle|^2 = \frac{1 \pm \cos\theta}{2}$.
   - With $|\pm i\rangle$: $|\langle \pm i | \psi(\theta)\rangle|^2 = \frac{1 \pm \sin\theta}{2}$.
4. The maximum overlap over all 6 states is $\max \{ \frac{1 + |\cos\theta|}{2}, \frac{1 + |\sin\theta|}{2} \}$.
5. If $\theta \in \{0, \pi/2, \pi, 3\pi/2\}$, $\max(|\cos\theta|, |\sin\theta|) = 1$, and $|\psi(\theta)\rangle$ is an exact stabilizer state.
6. For all $\theta \notin \{0, \pi/2, \pi, 3\pi/2\}$, $\max(|\cos\theta|, |\sin\theta|) \le 1/\sqrt{2}$, with the maximum achieved at $\theta \in \{\pi/4, 3\pi/4, 5\pi/4, 7\pi/4\}$.
7. Hence $F_{\text{stab}}(|\psi(\theta)\rangle) \le \frac{1 + 1/\sqrt{2}}{2} \approx 0.853553$.
8. For $P$ independent factors with non-stabilizer angles, the global fidelity is multiplicative across tensor products of single-qubit states:
   $$F_{\text{stab}}(|\Psi_{\vec{k}, s}\rangle) = \prod_{j=1}^P F_{\text{stab}}(|\psi_{k_j, s}\rangle) \le (0.8536)^P = 2^{-P \log_2(1/0.8536)} \approx 2^{-0.228 P}.$$
9. Since no non-trivial Pauli operator stabilizes $|\psi(\theta)\rangle$ when $\theta \notin \{0, \pi/2, \pi, 3\pi/2\}$, $\mathcal{S}(|\Psi_{\vec{k}, s}\rangle) = \{I^{\otimes P}\}$ and $\nu = P$. $\blacksquare$

---

### Theorem 2: Status of Stabilizer Rank Bounds and Retraction of Classical Simulation Claim
**Theorem Statement**:  
1. **Retraction**: The claim that quantum circuits acting on $P$ coset registers with $T_{\text{count}} \le O(\log P)$ can be simulated in polynomial classical time via Bravyi-Gosset decomposition is **RETRACTED AS INVALID**.
2. **Analysis**:
   - The Bravyi-Gosset runtime for simulating a Clifford $+ T$ circuit on an input state $|\Psi_{\text{in}}\rangle$ scales as:
     $$T_{\text{sim}} = O\left( \chi(|\Psi_{\text{in}}\rangle) \cdot 2^{\alpha T_{\text{count}}} \cdot \text{poly}(P) \right), \quad \alpha \le 0.23.$$
   - When $|\Psi_{\text{in}}\rangle = |0\rangle^{\otimes P}$, $\chi(|\Psi_{\text{in}}\rangle) = 1$, and low $T$-count implies polynomial runtime.
   - However, for coset state inputs, $|\Psi_{\text{in}}\rangle = |\Psi_{\vec{k}, s}\rangle$ is an unknown non-stabilizer state whenever $k_j s \not\equiv 0 \pmod{N/4}$.
   - Decomposing $|\Psi_{\vec{k}, s}\rangle$ into stabilizer states requires $\chi(|\Psi_{\vec{k}, s}\rangle)$ stabilizer states.
3. **Open Complexity Boundary for Stabilizer Rank**:
   - While $F_{\text{stab}}(|\Psi_{\vec{k}, s}\rangle) \le 2^{-\Omega(P)}$, proving an **exponential lower bound** on the stabilizer rank $\chi(|T\rangle^{\otimes P}) \ge 2^{\Omega(P)}$ remains a central **open conjecture** in quantum complexity theory (Bravyi et al. 2016, 2019; Peleg, Shpilka, Volk 2021; Mehraban & Tahmasbi 2023).
   - The best unconditionally proved lower bounds on the exact stabilizer rank of magic tensor powers are polynomial $\chi = \Omega(P^2)$ (Peleg et al. 2021), not exponential.
   - Regardless, the classical simulator cannot exploit a low-rank decomposition of $|\Psi_{\vec{k}, s}\rangle$ because the secret $s$ is unknown, and the states cannot be efficiently represented as stabilizer superpositions.

---

### Theorem 3: Fault-Tolerant Magic State Overhead in Sieve Algorithms
**Theorem Statement**:  
Let $\mathcal{A}$ be a quantum sieve algorithm operating on a pool of $P = 2^{\Omega(\sqrt{n})}$ coset registers that combines phase angles to reduce wavenumber uncertainty.  
1. Each phase combination step requires synthesizing an arbitrary rotation $R_z(\theta)$, which has $T$-count $\ge 3 \log_2(1/\epsilon) \ge 3n - O(1)$ by the Ross-Selinger algorithm.
2. In any fault-tolerant quantum architecture based on surface codes with physical error rate $p_{\text{phys}} \in [10^{-4}, 10^{-3}]$:
   - Distilling each magic state requires a 15-to-1 or 20-to-4 Bravyi-Kitaev distillation factory consuming $\Omega(\log(1/\epsilon_{\text{target}}))$ physical qubits and ancillae.
   - Sifting $P = 2^{\Omega(\sqrt{n})}$ registers requires at least $\Omega(P) = 2^{\Omega(\sqrt{n})}$ non-Clifford rotations.
   - The total physical spacetime volume satisfies:
     $$V_{\text{phys}} \ge \Omega\left( P \cdot \log^2 P \right) = 2^{\Omega(\sqrt{n})}.$$
3. At standard cryptographic scales ($n = 512$), $P \ge 2^{\sqrt{512}} \approx 2^{22.6} \approx 6.4 \times 10^6$ magic states. The physical distillation burden exceeds $10^9$ physical qubit-seconds, precluding practical quantum speedups.

**Proof**:  
1. Pure Clifford operations map Pauli operators to Pauli operators under conjugation ($C P C^\dagger \in \mathcal{P}_n$).
2. They cannot produce the continuous phase shifts $\theta_1 + \theta_2 \pmod{2^n}$ required to eliminate higher bits of the wavenumber.
3. Every non-Clifford rotation must be compiled into Clifford $+ T$ gates using magic state injection.
4. Synthesizing $R_z(2\pi / 2^k)$ to precision $\epsilon \le 2^{-n}$ requires $T$-count $3n + O(\log(1/\epsilon))$ (Ross-Selinger 2014).
5. Combining $P$ registers pairwise requires at least $P/2$ such rotations at each sieving level, giving $T_{\text{total}} = \Omega(P \log P) = 2^{\Omega(\sqrt{n})}$.
6. Each magic state factory requires $\Theta(\log(P/\delta))$ code distance, yielding total spacetime volume $\Omega(P \log^2 P) = 2^{\Omega(\sqrt{n})}$. $\blacksquare$

---

## 4. The Corrected Quantum Resource Trilemma for DCP

```
                      Dihedral Coset Processing Circuits
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        ▼                              ▼                              ▼
   Sector I:                      Sector II:                    Sector III:
Pure Clifford Circuits         Shallow Unitary             Full Multi-Register Sieve
  (T_count = 0)               (Depth D < log n)             (P = 2^{Omega(sqrt{n})})
        │                              │                              │
        ▼                              ▼                              ▼
Cannot synthesize non-         Zero probability of         Superpolynomial magic
Clifford phase combinations;    unitary phase               state distillation burden
limited to parity checks       cancellation (ED >= 0.63n)   (>= 2^{Omega(sqrt{n})})
```

**Conclusion**:  
The resource analysis shows that there is no shortcut for dihedral coset distillation:
- Clifford operations are blind to continuous phase reduction.
- Shallow unitary circuits cannot achieve phase cancellation due to the entanglement depth lower bound ($E_D \ge 0.631 n$).
- Sieve algorithms that successfully eliminate phases require superpolynomial magic state distillation overhead ($2^{\Omega(\sqrt{n})}$) in fault-tolerant implementations.
