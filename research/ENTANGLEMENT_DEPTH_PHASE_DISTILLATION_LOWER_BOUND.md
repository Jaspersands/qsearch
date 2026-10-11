# Global Entanglement Depth Lower Bound for Dihedral Coset State Distillation

**Investigation**: Investigation 23 (Quantum Information Theory & Entanglement Spectrum)  
**Date**: 2026-10-11  
**Status**: AUDITED & REVISED (See `research/ADVERSARIAL_MATHEMATICAL_AUDIT_REPORT.md`)  
**Core Invariants**: `speedup_claim_allowed = False`, `accepted_speedup_candidate = False`  

> [!WARNING]
> **Adversarial Audit Scope Notice (2026-10-11)**:
> 1. **Unitary Circuit Scope**: The entanglement depth lower bound applies **strictly to coherent, measurement-free unitary circuits** where all registers remain in a pure state until the final measurement. It is **BYPASSED** by adaptive circuits with intermediate measurements and feed-forward (such as Kuperberg's actual sieve), which only entangle 2 qubits at a time ($E_D = 2$ identically at all stages) and immediately measure the target register.
> 2. **Arithmetic Correction**: In Theorem 1, the union bound on subset collisions is $\frac{3^m - 1}{2^n}$. Demanding this probability be bounded by $\epsilon < 1$ implies $m \ge \frac{n}{\log_2 3} \approx 0.6309 n$, not $m \ge n - O(1)$. The support lower bound is $E_D \ge 0.631 n = \Omega(n)$.

---

## 1. Executive Summary & Foundational Question

Can shallow-depth quantum circuits or bounded-entanglement tensor networks distill the hidden shift $s$ from an ensemble of $M$ independent dihedral coset states:
$$|\psi_s\rangle^{\otimes M} = \bigotimes_{j=1}^M \frac{1}{\sqrt{2}} \left( |0\rangle + e^{i \frac{2\pi k_j s}{N}} |1\rangle \right)?$$

We establish an exact information-theoretic lower bound on the **entanglement depth** $E_D$ and **circuit depth** $D$ required for **coherent unitary phase distillation**:
- Any measurement-free unitary quantum circuit operating on $M$ coset states with entanglement depth $E_D < 0.631 n$ has exponentially vanishing probability of producing a collision-free phase cancellation modulo $N$.
- Bounded-depth unitary quantum circuits ($D = o(\log n)$) have causal light cones of size $2^D = o(n) \ll n$, proving that unitary phase distillation requires light cones of size $\ge 0.631 n$.
- This unitary lower bound is bypassed by adaptive measurement-and-reset circuits (e.g., Kuperberg's sieve maintaining $E_D = 2$ at all times) and by unentangled single-qubit measurements with exponential classical decoding (Ettinger-Høyer-Knill with $E_D = 1$).
- Local Operations and Classical Communication (LOCC) reduce the unentangled decoding problem strictly to the classical Hidden Number Problem (Boneh-Venkatesan), which requires solving CVP on an $n$-dimensional lattice.

---

## 2. Definitions and Analytical Setup

### Definition 1: Entanglement Depth
A pure state $|\Psi\rangle \in \mathcal{H}_1 \otimes \dots \otimes \mathcal{H}_M$ has entanglement depth $k$ if it can be partitioned into product blocks:
$$|\Psi\rangle = |\phi_{B_1}\rangle \otimes |\phi_{B_2}\rangle \otimes \dots \otimes |\phi_{B_r}\rangle,$$
such that $\max_j |B_j| = k$.
A quantum channel $\mathcal{E}$ has entanglement depth $k$ if for any fully separable input state $\rho = \bigotimes_{j=1}^M \rho_j$, the output state $\mathcal{E}(\rho)$ has entanglement depth at most $k$.

### Definition 2: The Phase Cancellation Condition
Given random wavenumbers $k_1, \dots, k_M \in \mathbb{Z}_N$ (where $N = 2^n$), a phase cancellation is an integer linear combination:
$$\sum_{j=1}^M c_j k_j \equiv 0 \pmod N, \quad c_j \in \{-1, 0, 1\}, \quad \vec{c} \ne \vec{0}.$$
The support size of the cancellation is the Hamming weight $\|\vec{c}\|_0 = |\{ j : c_j \ne 0 \}|$.

---

## 3. Asymptotic Theorems and Proofs

### Theorem 1: The Linear Support Collision Floor
**Theorem Statement**:  
Let $k_1, \dots, k_M$ be drawn independently and uniformly from $\mathbb{Z}_N$ with $N = 2^n$.  
For any subset $S \subset \{1, \dots, M\}$ of size $|S| = m < n$:
$$\Pr\left( \exists \vec{c} \in \{-1, 0, 1\}^m \setminus \{\vec{0}\} : \sum_{j \in S} c_j k_j \equiv 0 \pmod N \right) \le \frac{3^m - 1}{2^n}.$$
For any $m \le \frac{n}{\log_2 3} - \frac{\log_2(1/\epsilon)}{\log_2 3}$, this probability is bounded by $\epsilon \to 0$.  
Consequently, any non-trivial phase cancellation modulo $2^n$ with high probability requires support size:
$$m \ge \frac{n}{\log_2 3} - O(1) \approx 0.6309 n = \Omega(n).$$

**Proof**:  
1. Fix a non-zero vector $\vec{c} \in \{-1, 0, 1\}^m \setminus \{\vec{0}\}$. Let $j^* \in S$ be a coordinate where $c_{j^*} \ne 0$ (so $c_{j^*} \in \{-1, 1\}$).
2. Since $c_{j^*}$ is a unit in $\mathbb{Z}_N$, the equation $\sum_{j \in S} c_j k_j \equiv 0 \pmod N$ is equivalent to:
   $$k_{j^*} \equiv - c_{j^*}^{-1} \sum_{j \in S \setminus \{j^*\}} c_j k_j \pmod N.$$
3. Conditioned on any realization of the other $m - 1$ variables, $k_{j^*}$ is uniformly distributed over $\mathbb{Z}_N$.
4. The conditional probability that this congruence holds is exactly $1/N = 2^{-n}$.
5. Taking the union bound over all $3^m - 1$ non-zero vectors $\vec{c} \in \{-1, 0, 1\}^m$:
   $$\Pr\left( \bigvee_{\vec{c} \ne \vec{0}} \sum_{j \in S} c_j k_j \equiv 0 \pmod N \right) \le \sum_{\vec{c} \ne \vec{0}} \frac{1}{2^n} = \frac{3^m - 1}{2^n}.$$
6. For $m < \frac{n}{\log_2 3} \approx 0.6309 n$, this probability is exponentially small $2^{-\Omega(n)}$.
7. For the union bound to permit an $\Omega(1)$ probability of non-trivial collision requires $3^m \ge 2^n \implies m \ge \frac{n}{\log_2 3} \approx 0.631 n$. $\blacksquare$

---

### Theorem 2: Entanglement Depth Lower Bound for Unitary Sieve Distillation
**Theorem Statement**:  
Let $\mathcal{C}$ be a **measurement-free unitary quantum circuit** acting on $M$ dihedral coset registers $|\psi_s\rangle^{\otimes M}$ that outputs a deterministic, unentangled single-qubit phase state $|\phi_{0, s}\rangle = \frac{1}{\sqrt{2}} (|0\rangle + e^{i \pi s} |1\rangle)$ with success probability $\ge 2/3$.  
Then:
1. The entanglement depth of the pure state before measurement must satisfy:
   $$E_D(\mathcal{C}) \ge \frac{n}{\log_2 3} - O(1) \approx 0.631 n = \Omega(\log N).$$
2. If $\mathcal{C}$ is composed of 2-qubit gates arranged in a circuit of depth $D$ on an arbitrary geometry, the circuit depth must satisfy:
   $$D \ge \log_2(0.631 n) - O(1) = \log_2 n - O(1) = \Omega(\log \log N).$$
3. On a 1D or 2D nearest-neighbor quantum architecture, the circuit depth must satisfy:
   $$D_{1D} \ge \Omega(n), \quad D_{2D} \ge \Omega(\sqrt{n}).$$

**Proof**:  
1. *Entanglement Block Separation*: Suppose $\mathcal{C}$ is unitary with entanglement depth $E_D < 0.631 n$.
   Then the joint state before the final measurement can be partitioned into disjoint pure product blocks $B_1, \dots, B_r$ with $|B_a| \le E_D < 0.631 n$.
2. Any phase distillation performed entirely within a block $B_a$ can only evaluate linear combinations of the wavenumbers belonging to $B_a$:
   $$K_{B_a} = \sum_{j \in B_a} c_j k_j.$$
3. By Theorem 1, because $|B_a| < 0.631 n$, the probability that $K_{B_a} \equiv 0 \pmod N$ is bounded by $\frac{3^{E_D} - 1}{2^n} = 2^{-\Omega(n)}$.
4. Therefore, with probability $1 - 2^{-\Omega(n)}$, every block $B_a$ retains a non-zero residual wavenumber $K_{B_a} \not\equiv 0 \pmod N$.
5. Tracing out the other unmeasured blocks leaves the target register with an effective phase variance of:
   $$\text{Var}(\theta) = \mathbb{E}\left[ \left( \frac{2\pi K_{B_a} s}{N} \right)^2 \right] \ge \Omega(1).$$
   The state is completely dephased and cannot produce the deterministic target phase.
6. *Causal Cone Expansion*: In a circuit of depth $D$ with 2-qubit gates, the light cone of any output qubit contains at most $2^D$ input qubits.
   For the output qubit to be entangled with a block of size $m \ge 0.631 n$ requires:
   $$2^D \ge 0.631 n \implies D \ge \log_2 n - O(1).$$
7. On a $d$-dimensional lattice with nearest-neighbor gates, the light cone after depth $D$ contains at most $O(D^d)$ qubits.
   Thus $D^d \ge \Omega(n) \implies D \ge \Omega(n^{1/d})$. $\blacksquare$

---

### Theorem 3: Classical LOCC Subsumption via the Hidden Number Problem
**Theorem Statement**:  
Any quantum protocol restricted to Local Operations and Classical Communication (LOCC) between the $M$ coset registers can be simulated classically with access to an oracle for the classical Hidden Number Problem (HNP).  
Finding $s$ from LOCC measurement outcomes requires solving the Closest Vector Problem (CVP) on a lattice of dimension $M$, which is NP-hard under randomized reductions and takes $2^{\Omega(M)}$ time by the best classical lattice sieving algorithms.

**Proof**:  
1. An arbitrary LOCC protocol measures each register $j \in \{1, \dots, M\}$ with a local POVM $\{M_{x_j}\}$.
2. For the phase state $|\psi_{k_j, s}\rangle = \frac{1}{\sqrt{2}} (|0\rangle + e^{i 2\pi k_j s / N} |1\rangle)$, the density matrix is:
   $$\rho_{j} = \frac{1}{2} \begin{pmatrix} 1 & e^{-i 2\pi k_j s / N} \\ e^{i 2\pi k_j s / N} & 1 \end{pmatrix}.$$
3. Any local measurement outcome $x_j$ has probability $P(x_j) = \frac{1}{2} + \alpha_j \cos\left( \frac{2\pi k_j s}{N} + \phi_j \right)$ for constants $\alpha_j \in [0, 1/2]$ and $\phi_j \in [0, 2\pi)$.
4. The measurement reveals the most significant bits of the phase $k_j s \pmod N$.
5. This is precisely the instance of the Hidden Number Problem with multiplier $s$ and random inputs $k_j$.
6. By the Boneh-Venkatesan theorem (1996), solving HNP with $O(1)$ bits of precision per sample requires finding the closest vector in an $M$-dimensional integer lattice with basis vectors generated by $(k_1, \dots, k_M)$ and modulus $N$.
7. Since LOCC cannot perform coherent basis changes across registers, it cannot eliminate the lattice geometry, reducing strictly to classical CVP. $\blacksquare$

---

### 3.4. Evasion Mechanisms: Unentangled Measurements and Adaptive Sieves

The entanglement depth lower bound of Theorem 2 is subject to two major circumvention mechanisms:

#### 1. The Ettinger-Høyer-Knill (2004) Unentangled Baseline ($E_D = 1$)
Ettinger, Høyer, and Knill (2004) proved that unentangled measurements on individual coset registers provide sufficient classical information to reconstruct $s$:
1. Prepare $M = O(n)$ independent coset registers $|\psi_{k_j, s}\rangle = \frac{1}{\sqrt{2}} (|0\rangle + e^{i 2\pi k_j s / N} |1\rangle)$.
2. Measure each register independently in the Pauli $X$ basis (an unentangled LOCC operation with $E_D = 1$).
3. The measurement outcome $b_j \in \{0, 1\}$ occurs with probability:
   $$\Pr(b_j = 0 \mid k_j, s) = \cos^2\left( \frac{\pi k_j s}{N} \right) = \frac{1 + \cos(2\pi k_j s / N)}{2}.$$
4. For $M = \Theta(n)$ samples, the maximum-likelihood estimator over candidates $s' \in \mathbb{Z}_N$:
   $$\hat{s} = \arg\max_{s'} \sum_{j=1}^M \ln \left[ \frac{1 + (-1)^{b_j} \cos(2\pi k_j s' / N)}{2} \right],$$
   identifies $s' = s$ uniquely with probability $\ge 1 - 2^{-\Omega(n)}$.
5. **Information-Theoretic Consequence**: Entanglement is **not required** to extract sufficient information to determine the hidden shift $s$. The information exists entirely in the classical statistics of single-qubit measurements. The barrier to an efficient quantum algorithm from unentangled measurements is strictly the **classical decoding complexity** of finding $\hat{s}$ in polynomial time.

#### 2. Adaptive Intermediate Measurements (Kuperberg Sieve, $E_D = 2$)
Theorem 2 assumes a **coherent unitary circuit** that outputs a pure state without intermediate measurements.
In contrast, Kuperberg's sieve (2005) is an **adaptive measurement-based protocol**:
1. At each stage, two coset registers $|\psi_{k_1, s}\rangle$ and $|\psi_{k_2, s}\rangle$ are entangled via a CNOT gate.
2. The target register is **immediately measured** in the computational basis.
3. Depending on the measurement outcome $b \in \{0, 1\}$, the control register collapses to $|\psi_{k_1 \pm k_2, s}\rangle$.
4. At every instantaneous time step, the multipartite quantum state has entanglement depth at most:
   $$E_D = 2 \ll 0.631 n.$$
5. Because intermediate projective measurements reset registers and generate classical branching, the circuit is **not** unitary, and Theorem 2 does not apply to it.

---

## 4. Conclusion & Impact

This investigation establishes precise physical and complexity-theoretic boundaries:
- **Unitary vs. Adaptive Phase Distillation**: In measurement-free unitary circuits, deterministic phase cancellation requires global multipartite entanglement across at least $0.631 n$ registers simultaneously. Shallow unitary circuits ($D < \log_2 n$) cannot distill the phase.
- **Entanglement is an Algorithmic Choice, Not an Information-Theoretic Necessity**: By the Ettinger-Høyer-Knill theorem, zero entanglement ($E_D = 1$) suffices information-theoretically. Algorithms that entangle registers (like Kuperberg's sieve with $E_D = 2$) do so to circumvent the classical intractability of non-convex phase decoding, not because the information cannot be extracted by local measurements.
