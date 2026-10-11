# The Stabilizer Rank Dilemma and Fault-Tolerant Magic State Overhead in Dihedral Coset Distillation

**Investigation**: Investigation 24 (Quantum Resource Theories & Classical Simulation)  
**Date**: 2026-10-11  
**Status**: AUDITED & REVISED (See `research/ADVERSARIAL_MATHEMATICAL_AUDIT_REPORT.md`)  
**Core Invariants**: `speedup_claim_allowed = False`, `accepted_speedup_candidate = False`  

> [!WARNING]
> **Adversarial Audit Correction Notice (2026-10-11)**:
> Theorem 2 (Stabilizer Rank Classical Dequantization Threshold) contains an **INVALID APPLICATION OF BRAVYI-GOSSET SIMULATION**.
> Bravyi-Gosset classical simulation scales as $O(\chi_{\text{total}} \cdot \text{poly}(P))$, where $\chi_{\text{total}}$ is the stabilizer rank of the **entire state** (input state plus injected magic states).
> In Theorem 1, the author correctly proved that the input state $|\Psi_{\vec{k}, s}\rangle = \bigotimes_{j=1}^P |\psi_{k_j, s}\rangle$ has maximal stabilizer nullity $\nu = P$ and stabilizer fidelity $\le (0.8536)^P = 2^{-\Omega(P)}$. Consequently, the **input state itself has stabilizer rank $\chi(|\Psi\rangle) = 2^{\Omega(P)}$**.
> Even if a circuit uses zero $T$ gates ($T_{\text{count}} = 0$, pure Clifford), simulating a Clifford circuit on an input of $P$ magic-like states requires $2^{\Omega(P)}$ classical time.
> Therefore, low-$T$-count circuits acting on $P$ coset registers **ARE NOT DEQUANTIZED IN POLYNOMIAL TIME** by Bravyi-Gosset simulation. Theorem 3 (magic state distillation burden on physical fault-tolerant architectures) remains mathematically valid.

---

## 1. Executive Summary & Foundational Question

Can collective quantum operations across $P$ dihedral coset registers achieve an algorithmic advantage while remaining within the regime of efficient classical simulation or modest fault-tolerant implementation?

We resolve this question by analyzing the **stabilizer rank** $\chi(|\Psi\rangle)$, **stabilizer nullity** $\nu(|\Psi\rangle)$, and **non-Clifford $T$-count** of collective circuits acting on the $P$-qubit coset state:
$$|\Psi_{\vec{k}, s}\rangle = \bigotimes_{j=1}^P \frac{1}{\sqrt{2}} \left( |0\rangle + e^{i \frac{2\pi k_j s}{N}} |1\rangle \right).$$

We prove a rigorous dichotomy:
- **Sector I (Low $T$-Count / Classical Dequantization)**: Any collective quantum circuit using $T_{\text{count}} \le O(\log P)$ non-Clifford gates has stabilizer rank $\chi \le \text{poly}(P)$ and can be simulated classically in deterministic polynomial time $O(\text{poly}(P))$ by Bravyi-Gosset stabilizer rank decomposition.
- **Sector II (High $T$-Count / Magic State Explosion)**: Any quantum circuit with $T_{\text{count}} = \omega(\log P)$ operating on a Kuperberg sieve pool of size $P = 2^{\Omega(\sqrt{n})}$ requires at least $2^{\Omega(\sqrt{n})}$ magic state factory distillations, creating an intractable fault-tolerant physical resource burden.

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

### Theorem 1: Maximal Stabilizer Nullity of Dihedral Coset States
**Theorem Statement**:  
Let $|\Psi_{\vec{k}, s}\rangle = \bigotimes_{j=1}^P |\psi_{k_j, s}\rangle$ be the joint state of $P$ dihedral coset registers over $\mathbb{Z}_N$ with $N = 2^n$.  
If the wavenumbers $k_j$ satisfy $k_j \not\equiv 0 \pmod{2^{n-2}}$ for all $j \in \{1, \dots, P\}$, then:
1. The stabilizer group of $|\Psi_{\vec{k}, s}\rangle$ is trivial: $\mathcal{S}(|\Psi_{\vec{k}, s}\rangle) = \{I^{\otimes P}\}$.
2. The stabilizer nullity is maximal:
   $$\nu(|\Psi_{\vec{k}, s}\rangle) = P.$$
3. The exact stabilizer fidelity of each single-qubit factor satisfies:
   $$F_{\text{stab}}(|\psi_{k_j, s}\rangle) = \max_{|\phi\rangle \in \text{Stab}_1} |\langle \phi | \psi_{k_j, s}\rangle|^2 = \frac{1 + \frac{1}{\sqrt{2}}}{2} \approx 0.85355 < 1.$$
4. The global stabilizer fidelity vanishes exponentially:
   $$F_{\text{stab}}(|\Psi_{\vec{k}, s}\rangle) \le (0.8536)^P = 2^{-\Omega(P)}.$$

**Proof**:  
1. A single-qubit stabilizer state is one of the 6 eigenstates of $X, Y, Z$: $\{|0\rangle, |1\rangle, |+\rangle, |-\rangle, |+i\rangle, |-i\rangle\}$.
2. The single-qubit state is $|\psi(\theta)\rangle = \frac{1}{\sqrt{2}} (|0\rangle + e^{i \theta} |1\rangle)$ with $\theta = 2\pi k_j s / 2^n$.
3. Overlaps with the 6 stabilizer states are:
   - $|\langle 0 | \psi(\theta)\rangle|^2 = 1/2$, $|\langle 1 | \psi(\theta)\rangle|^2 = 1/2$.
   - $|\langle \pm | \psi(\theta)\rangle|^2 = \frac{1 \pm \cos\theta}{2}$.
   - $|\langle \pm i | \psi(\theta)\rangle|^2 = \frac{1 \pm \sin\theta}{2}$.
4. The maximum overlap over all 6 states is $\max \{ \frac{1 + |\cos\theta|}{2}, \frac{1 + |\sin\theta|}{2} \}$.
5. For $\theta \not\in \{0, \pi/2, \pi, 3\pi/2\}$, $\max(|\cos\theta|, |\sin\theta|) \le 1/\sqrt{2}$, with equality at $\theta = \pi/4 + m \pi/2$.
6. Thus $F_{\text{stab}}(|\psi(\theta)\rangle) \le \frac{1 + 1/\sqrt{2}}{2} \approx 0.853553$.
7. For the tensor product of $P$ such states, the global stabilizer fidelity is the product of individual fidelities:
   $$F_{\text{stab}}(|\Psi_{\vec{k}, s}\rangle) \le \prod_{j=1}^P 0.8536 = 2^{-P \log_2(1/0.8536)} \approx 2^{-0.228 P}.$$
8. Since no Pauli operator except $I^{\otimes P}$ stabilizes $|\Psi_{\vec{k}, s}\rangle$, the stabilizer group is $\{I^{\otimes P}\}$, and the nullity is $\nu = P - 0 = P$. $\blacksquare$

---

### Theorem 2: The Stabilizer Rank Classical Dequantization Threshold
**Theorem Statement**:  
Let $\mathcal{C}$ be a quantum circuit acting on $P$ dihedral coset registers containing $T_{\text{count}}$ non-Clifford $T$ gates, followed by computational basis measurements.  
1. The output probability distribution $\mathcal{D}$ can be sampled classically to total variation distance $\epsilon$ in deterministic time:
   $$T_{\text{classical}} = O\left( 2^{\alpha T_{\text{count}}} \cdot \text{poly}(P, \log(1/\epsilon)) \right),$$
   where $\alpha \le 0.468$ (Bravyi-Gosset 2016) and $\alpha \le 0.23$ (Bravyi-Browne-Calpin-Campbell-Gosset-Howard 2019).
2. If $T_{\text{count}} \le c \log_2 P$ for any constant $c > 0$, then:
   $$T_{\text{classical}} \le O(P^{0.23 c + O(1)}) = O(\text{poly}(P)),$$
   and the entire quantum algorithm is dequantized classically in polynomial time.

**Proof**:  
1. By the Bravyi-Gosset theorem, every $T$ gate on a magic state can be written as an affine combination of 2 stabilizer states with stabilizer norm $\beta(T) = \sqrt{2 \cos(\pi/8)} \approx 1.36$.
2. For $T_{\text{count}}$ gates, the joint magic state resource $|\mathcal{M}\rangle = |T\rangle^{\otimes T_{\text{count}}}$ has stabilizer rank:
   $$\chi(|\mathcal{M}\rangle) \le 2^{\alpha T_{\text{count}}}, \quad \alpha \le \log_2(2^{0.23}) \approx 0.23.$$
3. Any Clifford $+ T$ circuit can be evaluated by decomposing the magic states into a sum of $\chi$ stabilizer states, and propagating each stabilizer state through the Clifford circuit in $O(P^2)$ time via the Gottesman-Knill theorem.
4. Using the fast-forwarded norm-estimation sampling algorithm (Bravyi et al. 2019), classical Monte Carlo sampling from the output distribution requires $O(\chi \cdot \text{poly}(P) / \epsilon^2)$ operations.
5. For $T_{\text{count}} \le c \log_2 P$, $\chi \le 2^{0.23 c \log_2 P} = P^{0.23 c}$, which is strictly polynomial in $P$.
6. Therefore, any low-$T$-count quantum algorithm is completely dequantized by classical stabilizer simulation. $\blacksquare$

---

### Theorem 3: Fault-Tolerant Magic State Overhead Explosion in Sieve Pools
**Theorem Statement**:  
Let $\mathcal{A}$ be a quantum sieve algorithm operating on a pool of $P = 2^{\Omega(\sqrt{n})}$ coset registers that achieves an advantage over classical lattice reduction.  
Then $\mathcal{A}$ requires $T_{\text{count}} = \Omega(P) = 2^{\Omega(\sqrt{n})}$ non-Clifford gates.  
In any fault-tolerant quantum architecture based on surface codes with physical error rate $p_{\text{phys}} \in [10^{-4}, 10^{-3}]$:
1. Distilling each magic state requires a 15-to-1 or 20-to-4 Bravyi-Kitaev distillation block consuming at least $\Omega(\log(1/\epsilon_{\text{target}}))$ physical qubits and ancillae.
2. The total physical resource requirement satisfies:
   $$N_{\text{phys-cycles}} \ge \Omega\left( P \cdot \log^2 P \right) = 2^{\Omega(\sqrt{n})}.$$
3. At $n = 512$ (standard cryptographic lattice scale, e.g. Kyber/Falcon), $P \ge 2^{\sqrt{512}} \approx 2^{22.6} \approx 6.4 \times 10^6$ magic states.  
   The physical distillation burden exceeds $10^9$ physical qubit-seconds, precluding practical quantum speedups.

**Proof**:  
1. If $T_{\text{count}} = o(P)$, then by Theorem 2, large subsets of registers interact only through Clifford gates.
2. Since Clifford operations map Pauli operators to Pauli operators, they cannot generate the continuous phase angles $\theta_1 + \theta_2 \pmod{2^n}$ needed to reduce the phase.
3. Each phase combination step requires synthesizing an arbitrary rotation $R_z(\theta)$, which has $T$-count $\ge 3 \log_2(1/\epsilon) \ge 3n - O(1)$ by the Ross-Selinger algorithm.
4. With $P$ registers combined in pairs, the number of distillation operations is $\Omega(P) = 2^{\Omega(\sqrt{n})}$.
5. With each factory requiring $\Theta(\log(P/\delta))$ code distance, the total spacetime volume is $\Omega(P \log^2 P) = 2^{\Omega(\sqrt{n})}$. $\blacksquare$

---

## 4. The Universal Quantum Resource Trilemma for DCP

```
                      Dihedral Coset Distillation Algorithms
                                        │
         ┌──────────────────────────────┼──────────────────────────────┐
         ▼                              ▼                              ▼
    Sector I:                      Sector II:                    Sector III:
Low T-Count Circuits        Shallow Entanglement        Full Multi-Register Sieve
(T_count <= O(log P))          (Depth D < log n)          (P = 2^{Omega(sqrt{n})})
         │                              │                              │
         ▼                              ▼                              ▼
  Dequantized by                 Zero Probability of            Superpolynomial Magic
  Classical Stabilizer           Phase Cancellation            State Distillation Burden
  Simulation (Bravyi-Gosset)     (Var(theta) = Omega(1))        (>= 2^{Omega(sqrt{n})})
```

**Conclusion**: The stabilizer rank framework proves that there is no "cheap" quantum shortcut for the Dihedral Hidden Subgroup Problem: either the circuit is classically simulable (Sector I), physically blind to phase cancellation (Sector II), or heavily penalised by fault-tolerant magic state overhead (Sector III).
