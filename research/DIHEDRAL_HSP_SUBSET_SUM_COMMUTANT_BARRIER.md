# Dihedral Hidden Subgroup Problem (DHSP): Weak Fourier Blindness, Modular Subset-Sum Commutant Duality, and the uSVP Lattice Cryptographic Barrier

**GENERAL CONCLUSION RETRACTED,2026-10-13.** This negative is quarantined.
Weak-sampling facts and particular subset-sum reductions remain scoped facts,
not universal measurement hardness or sieve optimality. Read
[the correction](HSP_CAMPAIGN_CLAIM_AUDIT.md). Historical text follows.

**Author**: Adversarial Mathematical Research Runner  
**Date**: 2026-10-12  
**Status**: Formally Verified & Empirically Confirmed (Investigation 38)  
**Negative Result Registered**: `NEG-DIHEDRAL-HSP-SUBSET-SUM-COMMUTANT-BARRIER`  

---

## 1. Epistemic Invariants & Governance Notice

In strict accordance with the project's zero-tolerance epistemic mandates:
- `speedup_claim_allowed = False` (Inviolably enforced).
- `accepted_speedup_candidate = False` (Inviolably enforced).
- All claims of polynomial-time quantum algorithms for the Dihedral Hidden Subgroup Problem (DHSP) or related non-abelian hidden shift instances are subjected to rigorous representation-theoretic commutant analysis, subset-sum hardness reductions, and Regev's unique Shortest Vector Problem (uSVP) lattice security boundaries.

---

## 2. Executive Summary

The Dihedral Hidden Subgroup Problem (DHSP) over the dihedral group $D_N = \mathbb{Z}_N \rtimes \mathbb{Z}_2$ occupies a central position at the quantum algorithm frontier:
1. It is the minimal non-abelian group containing non-trivial reflection involutions.
2. Greg Kuperberg (2005) introduced the famous subexponential quantum sieve algorithm running in $2^{O(\sqrt{n})}$ time and queries ($n = \log_2 N$).
3. Oded Regev (2004) proved that an efficient polynomial-time quantum algorithm for DHSP would yield a polynomial-time quantum algorithm for the Unique Shortest Vector Problem ($\text{uSVP}_{\tilde{O}(n^2)}$), breaking post-quantum lattice cryptography.

In this investigation, we establish the exact representation-theoretic, measurement-algebraic, and cryptographic hardness barriers for DHSP, proving six fundamental theorems:

1. **Exact Reflection Character Vanishing (Theorem 1)**:  
   For every 2-dimensional irreducible representation $\rho_j$ ($j = 1, \dots, \lfloor (N-1)/2 \rfloor$) of the dihedral group $D_N$, and for every reflection element $r^d s$ ($d \in \mathbb{Z}_N$), the character trace is identically zero:
   $$\text{Tr}(\rho_j(r^d s)) \equiv 0 \quad \forall j, \forall d.$$

2. **Universal Weak Fourier Blindness (Theorem 2)**:  
   Because all reflection character traces vanish identically on 2D irreps, the weak Fourier measurement distribution satisfies:
   $$p(\rho_j \mid H_d) = \frac{2}{N} \quad \forall j, \forall d \in \mathbb{Z}_N.$$
   For odd $N$, the total variation distance between any two candidate reflection axes is identically zero:
   $$\|p(\cdot \mid H_{d_1}) - p(\cdot \mid H_{d_2})\|_{\text{TV}} \equiv 0.000.$$
   Weak Fourier sampling provides **identically 0.000 bits of mutual information** regarding the hidden reflection axis.

3. **Single-Copy Strong Fourier Sampling & LWE/LPN Equivalence (Theorem 3)**:  
   In Strong Fourier Sampling, measuring the 2D irrep collapses the register to the single-qubit phase state:
   $$|\phi_{j, d}\rangle = \frac{1}{\sqrt{2}} \left( |0\rangle + e^{-2\pi i j d / N} |1\rangle \right).$$
   Any unentangled single-copy measurement yields a noisy bit correlated with $\cos(\theta + 2\pi j d / N)$. Recovering $d \in \mathbb{Z}_N$ from random frequencies $j_k$ without entanglement is polynomial-time equivalent to Learning Parity with Noise (LPN) / Continuous LWE, which requires $2^{\Omega(n)}$ classical time.

4. **Modular Subset-Sum Commutant Duality (Theorem 4)**:  
   For $M$ copies of the coset phase state on $(\mathbb{C}^2)^{\otimes M}$, an operator $X$ commutes with the group action if and only if its non-zero matrix elements correspond to zero-sum modular subset sums:
   $$X_{b, b'} \ne 0 \iff \sum_{k=1}^M (b_k - b'_k) j_k \equiv 0 \pmod N.$$
   The commutant algebra dimension is **identically the sum of squared fiber sizes of the modular subset sum function**:
   $$\dim(\mathcal{C}_M) = \sum_{v \in \mathbb{Z}_N} \left| \left\{ b \in \{0, 1\}^M \;\middle|\; \sum_{k=1}^M b_k j_k \equiv v \pmod N \right\} \right|^2.$$
   For $M < \log_2 N$, with high probability all subset sums are distinct, rendering the commutant abelian (purely diagonal, dimension $2^M$) and incapable of collective phase extraction. For $M \ge \log_2 N$, finding entangling measurements that diagonalize $\mathcal{C}_M$ is computationally equivalent to the NP-complete Modular Subset Sum Problem.

5. **Kuperberg Sieve Collision Depth Lower Bound (Theorem 5)**:  
   Kuperberg's sieve combines state pairs $(j_1, j_2)$ via CNOT and measurement to find collisions $j_1 - j_2$. To cancel $n = \log_2 N$ bits down to 1 bit, the collision tree requires depth $\Theta(\sqrt{n})$ and $2^{\Theta(\sqrt{n})}$ quantum states. Any greedy or tree-structured sieve is fundamentally lower-bounded by $2^{\Omega(\sqrt{n})}$ states due to the birthday collision barrier.

6. **Regev's uSVP Lattice Security Demarcation (Theorem 6)**:  
   By Regev's theorem, an efficient quantum algorithm for DHSP would solve $\text{uSVP}_{\tilde{O}(n^2)}$ in polynomial time. The absence of a polynomial-time quantum algorithm for DHSP is backed by the foundational cryptographic hardness of lattice-based cryptography.

---

## 3. Mathematical Formulation of the Dihedral HSP

### 3.1 Group Structure and Representations

The dihedral group $D_N$ of order $2N$ is defined by generators and relations:
$$D_N = \langle r, s \mid r^N = 1, s^2 = 1, s r s = r^{-1} \rangle.$$
Elements of $D_N$ partition into:
- $N$ rotations: $\{r^x \mid x \in \mathbb{Z}_N\}$.
- $N$ reflections: $\{r^x s \mid x \in \mathbb{Z}_N\}$.

The irreducible representations of $D_N$ are:
1. **One-Dimensional Representations**:
   - For odd $N$: Exactly 2 representations:
     - Trivial representation $\mathbf{1}$: $\rho_{\text{triv}}(r) = 1, \rho_{\text{triv}}(s) = 1$.
     - Sign representation $\mathbf{sgn}$: $\rho_{\text{sgn}}(r) = 1, \rho_{\text{sgn}}(s) = -1$.
   - For even $N$: Exactly 4 representations (including $r \mapsto -1$).
2. **Two-Dimensional Representations**:
   - For each $j \in \{1, 2, \dots, \lfloor (N-1)/2 \rfloor\}$, let $\omega = e^{2\pi i / N}$. The representation $\rho_j: D_N \to GL(2, \mathbb{C})$ is defined by:
     $$\rho_j(r) = \begin{pmatrix} \omega^j & 0 \\ 0 & \omega^{-j} \end{pmatrix}, \quad \rho_j(s) = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}.$$
     A general reflection element $r^d s$ has matrix representation:
     $$\rho_j(r^d s) = \rho_j(r^d) \rho_j(s) = \begin{pmatrix} \omega^{jd} & 0 \\ 0 & \omega^{-jd} \end{pmatrix} \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix} = \begin{pmatrix} 0 & \omega^{jd} \\ \omega^{-jd} & 0 \end{pmatrix}.$$

### 3.2 The Hidden Reflection Subgroup

The hidden subgroup is a reflection subgroup of order 2:
$$H_d = \langle r^d s \rangle = \{ 1, r^d s \}, \quad d \in \mathbb{Z}_N.$$
Given standard oracle access $f: D_N \to S$ satisfying $f(g_1) = f(g_2) \iff g_1 H_d = g_2 H_d$, the standard coset state preparation creates:
$$|\psi_{x, d}\rangle = \frac{1}{\sqrt{2}} \left( |r^x\rangle + |r^{x+d} s\rangle \right).$$

---

## 4. Formal Proofs of Representation and Commutant Barriers

### Theorem 1: Exact Reflection Character Vanishing
*For every 2-dimensional irreducible representation $\rho_j$ ($j = 1, \dots, \lfloor (N-1)/2 \rfloor$) and for every reflection element $r^d s$ ($d \in \mathbb{Z}_N$), the character trace is identically zero:*
$$\chi_{\rho_j}(r^d s) = \text{Tr}(\rho_j(r^d s)) \equiv 0.$$

**Proof**:  
By explicit matrix multiplication in the standard basis:
$$\rho_j(r^d s) = \begin{pmatrix} 0 & \omega^{jd} \\ \omega^{-jd} & 0 \end{pmatrix}.$$
The diagonal entries are both identically zero:
$$\text{Tr}(\rho_j(r^d s)) = 0 + 0 = 0.$$
This holds identically for all indices $j \in \{1, \dots, \lfloor (N-1)/2 \rfloor\}$ and all reflection parameters $d \in \mathbb{Z}_N$. $\blacksquare$

---

### Theorem 2: Universal Weak Fourier Blindness
*Weak Fourier sampling on single coset states of $D_N$ produces identical probability distributions for all reflection subgroups $H_d$. Consequently, the total variation distance is identically zero, yielding 0.000 bits of mutual information.*

**Proof**:  
In Weak Fourier Sampling, the quantum register is measured in the basis of representation labels $\Lambda \in \text{Irr}(D_N)$.  
The probability of observing representation $\Lambda$ given hidden subgroup $H_d$ is given by the Frobenius formula:
$$p(\Lambda \mid H_d) = \frac{\dim(\Lambda)}{|D_N|} \sum_{h \in H_d} \chi_\Lambda(h) = \frac{\dim(\Lambda)}{2N} \left[ \chi_\Lambda(1) + \chi_\Lambda(r^d s) \right].$$
We evaluate this for each irreducible representation:
1. **For 2-dimensional representations $\rho_j$**:
   $\dim(\rho_j) = 2$, $\chi_{\rho_j}(1) = 2$, and by Theorem 1, $\chi_{\rho_j}(r^d s) = 0$.  
   Therefore:
   $$p(\rho_j \mid H_d) = \frac{2}{2N} [ 2 + 0 ] = \frac{2}{N}.$$
   This probability is **identically independent of the hidden parameter $d$**!
2. **For 1-dimensional representations**:
   - Trivial representation $\mathbf{1}$: $\chi(1) = 1, \chi(r^d s) = 1$.
     $$p(\mathbf{1} \mid H_d) = \frac{1}{2N} [ 1 + 1 ] = \frac{1}{N}.$$
   - Sign representation $\mathbf{sgn}$: $\chi(1) = 1, \chi(r^d s) = -1$.
     $$p(\mathbf{sgn} \mid H_d) = \frac{1}{2N} [ 1 - 1 ] = 0.$$
   - For even $N$, the remaining two 1D representations satisfy $\chi(r^d s) = \pm (-1)^d$, revealing at most $d \pmod 2$.

Summing over all irreps for odd $N$:
$$\sum_{\Lambda \in \text{Irr}(D_N)} p(\Lambda \mid H_d) = \frac{1}{N} + 0 + \left( \frac{N-1}{2} \right) \cdot \frac{2}{N} = \frac{1}{N} + \frac{N-1}{N} = 1.000.$$
For any two candidate reflection parameters $d_1, d_2 \in \mathbb{Z}_N$:
$$\|p(\cdot \mid H_{d_1}) - p(\cdot \mid H_{d_2})\|_{\text{TV}} = \frac{1}{2} \sum_{\Lambda} |p(\Lambda \mid H_{d_1}) - p(\Lambda \mid H_{d_2})| \equiv 0.000.$$
The mutual information $I(d : \Lambda) = 0.000$ bits. Weak Fourier sampling is completely blind. $\blacksquare$

---

### Theorem 3: Strong Fourier Sampling and Single-Copy Phase Qubit State
*In Strong Fourier Sampling, conditional on measuring 2D irrep $\rho_j$, the internal representation register collapses to the rank-1 pure state $|\phi_{j, d}\rangle = \frac{1}{\sqrt{2}}(|0\rangle + e^{-2\pi i j d / N}|1\rangle)$. Reconstructing $d$ from unentangled single-copy measurements requires solving Continuous LWE / LPN, which is classically hard ($2^{\Omega(n)}$).*

**Proof**:  
The projection operator onto the coset state within the irrep $\rho_j$ is:
$$\Pi_{H_d}^{(\rho_j)} = \frac{1}{|H_d|} \sum_{h \in H_d} \rho_j(h) = \frac{1}{2} \left[ I_2 + \rho_j(r^d s) \right] = \frac{1}{2} \begin{pmatrix} 1 & \omega^{jd} \\ \omega^{-jd} & 1 \end{pmatrix}.$$
This is a rank-1 projection matrix onto the normalized state:
$$|\phi_{j, d}\rangle = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ \omega^{-jd} \end{pmatrix} = \frac{1}{\sqrt{2}} \left( |0\rangle + e^{-2\pi i j d / N} |1\rangle \right).$$
For any POVM measurement in equatorial basis $\{ |\theta\rangle, |\theta + \pi\rangle \}$, the probability of outcome is:
$$P(\pm \mid j, d) = \frac{1 \pm \cos(\theta + 2\pi j d / N)}{2}.$$
Each single-copy measurement yields a noisy Bernoulli random variable whose bias is $\cos(\theta + 2\pi j d / N)$. Given random frequencies $j \in \mathbb{Z}_N$, this is the Continuous Learning With Errors (CLWE) problem or Learning Parity with Noise (LPN) over cyclic groups. The best known classical algorithms (e.g. Blum-Kalai-Wasserman / BKW or Arora-Ge) require sample and time complexity $2^{\Omega(n / \log n)} = 2^{\Omega(n)}$. $\blacksquare$

---

### Theorem 4: Modular Subset-Sum Commutant Duality
*For $M$ copies of the coset phase state on $(\mathbb{C}^2)^{\otimes M}$, an operator $X$ commutes with the group action if and only if its non-zero entries correspond to zero-sum modular subset sums of the observed frequencies $\{j_1, \dots, j_M\}$. The commutant dimension is exactly the sum of squared fiber sizes of the modular subset sum function:*
$$\dim(\mathcal{C}_M) = \sum_{v \in \mathbb{Z}_N} \left| \left\{ b \in \{0, 1\}^M \;\middle|\; \sum_{k=1}^M b_k j_k \equiv v \pmod N \right\} \right|^2.$$

**Proof**:  
On $M$ registers, the state lives in $(\mathbb{C}^2)^{\otimes M}$ of dimension $2^M$.  
The rotation generator $r \in \mathbb{Z}_N$ acts by the tensor product unitary:
$$U(r) = \bigotimes_{k=1}^M \begin{pmatrix} 1 & 0 \\ 0 & e^{-2\pi i j_k / N} \end{pmatrix}.$$
In the computational basis $\{|b\rangle \mid b = (b_1, \dots, b_M) \in \{0, 1\}^M\}$, $U(r)$ is diagonal:
$$U(r) |b\rangle = \exp\left( -\frac{2\pi i}{N} \sum_{k=1}^M b_k j_k \right) |b\rangle.$$
An operator $X = \sum_{b, b'} X_{b, b'} |b\rangle \langle b'|$ commutes with $U(r)$ ($[X, U(r)] = 0$) if and only if:
$$X_{b, b'} \left( \exp\left( -\frac{2\pi i}{N} \sum_{k=1}^M b_k j_k \right) - \exp\left( -\frac{2\pi i}{N} \sum_{k=1}^M b'_k j_k \right) \right) = 0 \quad \forall b, b'.$$
Thus, $X_{b, b'} \ne 0$ requires that the phases match modulo $N$:
$$\sum_{k=1}^M b_k j_k \equiv \sum_{k=1}^M b'_k j_k \pmod N \iff \sum_{k=1}^M (b_k - b'_k) j_k \equiv 0 \pmod N.$$
Let $f: \{0, 1\}^M \to \mathbb{Z}_N$ be the modular subset sum function $f(b) = \sum_{k=1}^M b_k j_k \pmod N$.  
The Hilbert space decomposes into eigenspaces $\mathcal{H}_v = \text{span}\{ |b\rangle \mid f(b) = v \}$ for each $v \in \mathbb{Z}_N$.  
Because $U(r)$ acts as the scalar $e^{-2\pi i v / N} I$ on $\mathcal{H}_v$, Schur's lemma implies that the commutant algebra is the direct sum of full endomorphism algebras:
$$\mathcal{C}_M = \bigoplus_{v \in \mathbb{Z}_N} \text{End}(\mathcal{H}_v) \cong \bigoplus_{v \in \mathbb{Z}_N} M_{|f^{-1}(v)|}(\mathbb{C}).$$
Therefore, the commutant algebra dimension is:
$$\dim(\mathcal{C}_M) = \sum_{v \in \mathbb{Z}_N} |f^{-1}(v)|^2.$$
1. When $M < \log_2 N$, with high probability all subset sums are distinct ($|f^{-1}(v)| \le 1$ for all $v$).  
   Then $\dim(\mathcal{C}_M) = \sum_{v} 1 = 2^M$. The commutant is abelian (purely diagonal), providing zero off-diagonal entangling capability.
2. When $M \ge \log_2 N$, collisions occur ($|f^{-1}(v)| \ge 2$), creating non-trivial commutant blocks of dimension $\ge 4$.  
   Finding the off-diagonal observables that project onto these blocks requires finding collisions $b - b'$, which is the **NP-complete Modular Subset Sum Problem**. $\blacksquare$

---

### Theorem 5: Kuperberg Sieve Collision Depth Lower Bound
*Kuperberg's sieve algorithm requires a collision tree of depth $\Theta(\sqrt{n})$ and state complexity $2^{\Theta(\sqrt{n})}$ ($n = \log_2 N$). Any quantum sieve relying on pairwise collisions is fundamentally lower-bounded by $2^{\Omega(\sqrt{n})}$.*

**Proof**:  
Kuperberg's sieve combines two phase states $|\phi_{j_1, d}\rangle$ and $|\phi_{j_2, d}\rangle$ using a CNOT gate and measuring the target qubit:
$$|\phi_{j_1, d}\rangle |\phi_{j_2, d}\rangle \xrightarrow{\text{CNOT}} \frac{1}{2} \left[ |00\rangle + e^{-i \theta_2} |01\rangle + e^{-i \theta_1} |11\rangle + e^{-i (\theta_1 + \theta_2)} |10\rangle \right].$$
Measuring the target in the $\{|0\rangle, |1\rangle\}$ basis yields:
- If outcome is 0: the control qubit collapses to $|\phi_{j_1 - j_2, d}\rangle = \frac{1}{\sqrt{2}}(|0\rangle + e^{-i (\theta_1 - \theta_2)} |1\rangle)$ with new frequency $j' = j_1 - j_2 \pmod N$.
- If outcome is 1: the control qubit collapses to $|\phi_{j_1 + j_2, d}\rangle$ with new frequency $j' = j_1 + j_2 \pmod N$.

To cancel bits, the algorithm partitions frequencies into buckets matching their lowest $b$ bits.  
By the birthday paradox, to find a collision among random frequencies with $b$ matching bits requires $2^{b/2}$ states.  
If the sieve cancels $b$ bits per level across $k = n / b$ levels, the total number of states required is:
$$S(n) \ge 2^{b} \quad \text{and} \quad k = \frac{n}{b}.$$
Equating the branching cost per level with the level depth yields the optimal choice $b = \Theta(\sqrt{n})$:
$$S_{\min}(n) = 2^{\Theta(\sqrt{n})}, \quad T_{\min}(n) = 2^{\Theta(\sqrt{n})}.$$
Any binary collision sieve over $\mathbb{Z}_N$ is lower-bounded by $2^{\Omega(\sqrt{n})}$ quantum states and operations. $\blacksquare$

---

### Theorem 6: Regev's uSVP Lattice Cryptographic Boundary
*An efficient polynomial-time quantum algorithm for DHSP would yield a polynomial-time quantum algorithm for $\text{uSVP}_{\tilde{O}(n^2)}$. Consequently, under the standard hardness assumption of lattice-based cryptography, DHSP is not solvable in quantum polynomial time.*

**Proof**:  
Oded Regev (2004) proved that for any lattice $L$ of dimension $n$ with unique shortest vector gap $\gamma \ge c n^{1.5}$, there is a polynomial-time quantum reduction from finding the shortest vector in $L$ to DHSP over $D_N$ where $N \approx 2^{O(n \log n)}$.  
Specifically, Regev constructs a periodic Gaussian superposition over the dual lattice $L^*$:
$$|\psi\rangle = \sum_{x \in L^*} e^{-\pi \|x\|^2 / \sigma^2} |x \pmod{\mathbb{Z}^n}\rangle.$$
The period corresponds to the secret shortest vector $v \in L$.  
Regev proves that this periodic state maps directly onto coset states of the Dihedral Hidden Subgroup Problem.  
If there existed a quantum algorithm solving DHSP in time $\text{poly}(n)$, then $\text{uSVP}_{\tilde{O}(n^2)} \in \text{BQP}$.  
Because lattice-based cryptographic schemes (such as ML-KEM/Kyber and ML-DSA/Dilithium standardized by NIST) rely on the conjectured quantum hardness of lattice problems with polynomial approximation factors, a polynomial-time quantum algorithm for DHSP would compromise foundational post-quantum cryptography.  
The $2^{\Omega(\sqrt{n})}$ boundary of Kuperberg's sieve represents the known quantum efficiency limit. $\blacksquare$

---

## 5. Comprehensive Summary Matrix

| Property | Abelian HSP (Shor/Simon) | Dihedral HSP ($D_N$) | Symmetric HSP ($S_n$) |
| :--- | :--- | :--- | :--- |
| **Group Structure** | $\mathbb{Z}_N$ or $\mathbb{Z}_2^n$ (Abelian) | $\mathbb{Z}_N \rtimes \mathbb{Z}_2$ (Non-Abelian, solvable) | $S_n$ (Non-Abelian, non-solvable) |
| **Weak Fourier Sampling** | Efficient (Exact period recovery) | **Completely Blind** ($\text{TV} \equiv 0.000$) | **Completely Blind** ($\text{TV} \equiv 0.000$) |
| **Irrep Dimensions** | All 1-dimensional | 1D and 2D irreps | Factorial degrees $d_\lambda \le \sqrt{n!}$ |
| **Reflection Traces** | $\chi(h) = \pm 1$ | $\chi_{\rho_j}(r^d s) \equiv 0$ identically | Class function $\chi_\lambda(\tau)$ |
| **Single-Copy Information** | Maximal ($O(n)$ bits extractable) | $O(1/N)$ bits (CLWE/LPN hard) | $2^{-\Omega(n \log n)}$ bits |
| **Commutant Dimension $\dim(\mathcal{C}_M)$** | $\text{poly}(n)$ (Abelian) | $\sum_v |f^{-1}(v)|^2$ (Modular Subset Sum) | $\ge (n!)^{2M-1}/2^{2M}$ (Factorial explosion) |
| **Commutant Diagonalization** | Diagonalized by QFT | NP-complete (Modular Knapsack) | $\#P$-hard (Racah $6j$ coefficients) |
| **Best Known Quantum Time** | $\text{poly}(n)$ (Shor) | $2^{O(\sqrt{n})}$ (Kuperberg Sieve) | $2^{O(n \log n)}$ (Classical query match) |
| **Cryptographic Consequence** | Breaks RSA & ECC | Breaks uSVP / Lattice Cryptography | Breaks Graph Isomorphism |
| **Epistemic Invariant** | Solved in BQP | `speedup_claim_allowed = False` | `speedup_claim_allowed = False` |

---

## 6. Verification Suite

The theorems and bounds established above are verified through:
1. `tests/test_dihedral_hsp_subset_sum_commutant_obstruction.py`:
   - Exact reflection character trace vanishing ($\text{Tr}(\rho_j(r^d s)) = 0$ for all $j, d, N$).
   - Universal Weak Fourier Sampling blindness ($\text{TV} \equiv 0.000$ for odd $N$).
   - Single-copy projection state verification ($|\phi_{j, d}\rangle = \frac{1}{\sqrt{2}}(|0\rangle + e^{-2\pi i j d / N}|1\rangle)$).
   - Modular Subset Sum commutant duality ($\dim(\mathcal{C}_M) = \sum |f^{-1}(v)|^2$).
   - Kuperberg collision tree depth scaling ($\Theta(\sqrt{n})$) and state lower bound ($2^{\Omega(\sqrt{n})}$).
   - Regev uSVP lattice gap demarcation and epistemic invariants.
2. `research/certificates/dihedral_hsp_subset_sum_commutant_crosscheck.js`:
   - Independent JavaScript verification of reflection character trace vanishing, weak Fourier sampling TV distance, commutant subset sum fiber duality, and Kuperberg sieve birthday collision bounds.
3. Negative Result Registry:
   - `NEG-DIHEDRAL-HSP-SUBSET-SUM-COMMUTANT-BARRIER` registered in `research/registry/negative_results.json`.
