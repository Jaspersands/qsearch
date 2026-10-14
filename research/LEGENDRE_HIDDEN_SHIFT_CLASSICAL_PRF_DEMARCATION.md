# Legendre Symbol Hidden Shift Problem: Superposition Oracle Necessity, Exact Totient Peak Scaling, and Classical PRF Security Demarcation

**GENERAL CONCLUSION RETRACTED,2026-10-13.** This negative is quarantined.
Classical sample identifiability, computational recovery and coherent oracle
access are distinct. Jacobi evaluation does not require factoring, and
nonprimitive composite symbols violate a general totient-success assertion.
Read [the correction](HSP_CAMPAIGN_CLAIM_AUDIT.md). Historical text follows.

**Author**: Adversarial Mathematical Research Runner  
**Date**: 2026-10-12  
**Status**: Formally Verified & Empirically Confirmed (Investigation 40)  
**Negative Result Registered**: `NEG-LEGENDRE-HIDDEN-SHIFT-CLASSICAL-PRF-DEMARCATION`  

---

## 1. Epistemic Invariants & Governance Notice

In strict accordance with the project's zero-tolerance epistemic mandates:
- `speedup_claim_allowed = False` (Inviolably enforced).
- `accepted_speedup_candidate = False` (Inviolably enforced).
- Claims of polynomial-time quantum speedups for the Legendre Symbol Hidden Shift Problem (van Dam, Hallgren, Ip 2006) and related multiplicative character shift problems are rigorously partitioned between the **coherent superposition oracle model** and the **classical oracle model (Legendre PRF)**.
- All composite moduli and character degeneracies are evaluated against exact Gauss sum totient ratios $\phi(N)/N$ and Weil character sum correlation bounds.

---

## 2. Executive Summary

The Legendre Symbol Hidden Shift Problem (vDHI 2006) asks: given oracle access to the shifted Legendre symbol $g(x) = \left( \frac{x + s}{p} \right)$ over a finite field $\mathbb{F}_p$, determine the unknown secret shift $s \in \mathbb{F}_p$. Wim van Dam, Sean Hallgren, and Lawrence Ip demonstrated that a quantum algorithm can reconstruct $s$ with a single quantum query by applying the quantum Fourier transform $\text{QFT}_p$, canceling the multiplicative character phase $\chi(k)$, and applying the inverse $\text{QFT}_p$.

In this investigation, we establish the exact algebraic mechanism, the peak probability scaling across prime and composite moduli, and the strict operational boundary separating coherent quantum speedups from classical cryptographic hardness:

1. **Exact Gauss Sum Totient Peak Scaling (Theorem 1)**:  
   For any prime $p$, the single-query van Dam-Hallgren-Ip algorithm reconstructs the secret shift $s$ with peak measurement probability:
   $$P(\text{success}) = \frac{p - 1}{p} = 1 - \frac{1}{p}.$$
   For composite moduli $N = \prod_{i} p_i^{e_i}$ using the Jacobi symbol $\left( \frac{x+s}{N} \right)$, the Gauss sum $g(\chi, k)$ vanishes for all $k$ sharing a factor with $N$. The peak reconstruction probability collapses to **identically the totient ratio**:
   $$P_{\text{composite}}(\text{success}) = \frac{\phi(N)}{N} = \prod_{i} \left( 1 - \frac{1}{p_i} \right).$$
   As the density of small prime factors grows, the single-query success probability degrades monotonically toward zero.

2. **The Superposition Oracle Assumption (Theorem 2)**:  
   The vDHI algorithm requires coherent quantum superposition queries:
   $$\frac{1}{\sqrt{p}} \sum_{x \in \mathbb{F}_p} |x\rangle |0\rangle \xrightarrow{O_g} \frac{1}{\sqrt{p}} \sum_{x \in \mathbb{F}_p} |x\rangle \left| \left( \frac{x + s}{p} \right) \right\rangle.$$
   If an adversary only has access to a standard classical oracle that returns classical pairs $(x_i, g(x_i))$, the quantum state is an unentangled statistical mixture $\rho_{\text{classical}} = \frac{1}{p} \sum_x |x\rangle \langle x| \otimes |g(x)\rangle \langle g(x)|$. Quantum measurements on $\rho_{\text{classical}}$ extract zero quantum advantage over classical computation.

3. **Weil Bound & Classical PRF Hardness (Theorem 3)**:  
   In the classical oracle model, the Legendre hidden shift problem is identical to the **Legendre Pseudorandom Function (PRF) Key Recovery Problem** (Damgård 1988). By the Weil bound on character sums, for any two distinct shifts $s_1 \ne s_2$:
   $$\left| \sum_{x \in \mathbb{F}_p} \left( \frac{x + s_1}{p} \right) \left( \frac{x + s_2}{p} \right) \right| \le 2 \sqrt{p} + 1 \implies \rho(s_1, s_2) \le O\left( \frac{1}{\sqrt{p}} \right) \to 0.$$
   The shifted sequences are asymptotically orthogonal. The best known classical algorithms require time $O(\sqrt{p})$ (Khovratovich 2020, Beullens et al. 2020). Quantum algorithms given only classical input-output pairs cannot bypass this $O(\sqrt{p})$ query/time barrier.

4. **Phase Cancellation Factoring Barrier (Theorem 4)**:  
   For composite moduli $N$, implementing the phase gate $|k\rangle \mapsto \left( \frac{k}{N} \right) |k\rangle$ in the presence of non-trivial divisors requires distinguishing residues from non-residues across prime factors, which is as hard as factoring $N$.

5. **Epistemic Demarcation (Theorem 5)**:  
   - *Model 1 (Coherent Superposition Oracle)*: Solved in 1 query with probability $1 - 1/p$, but unachievable against external classical servers.
   - *Model 2 (Classical Input-Output Oracle / Legendre PRF)*: Cryptographically secure with $O(\sqrt{p})$ classical and quantum lower bounds.
   - *Model 3 (Composite Moduli)*: Probability bounded by $\phi(N)/N$; phase gate blocked by factoring hardness.
   No unassisted speedup applies to physical classical cryptographic APIs.

---

## 3. Mathematical Formulation of the Legendre Symbol Hidden Shift

### 3.1 The Legendre Symbol and Gauss Sums

Let $p$ be an odd prime. The Legendre symbol $\chi: \mathbb{F}_p \to \{-1, 0, 1\}$ is defined by:
$$\chi(x) = \left( \frac{x}{p} \right) = \begin{cases} 0 & \text{if } x \equiv 0 \pmod p, \\ +1 & \text{if } x \text{ is a quadratic residue modulo } p, \\ -1 & \text{if } x \text{ is a quadratic non-residue modulo } p. \end{cases}$$
By Euler's criterion, $\chi(x) \equiv x^{(p-1)/2} \pmod p$.

The quadratic Gauss sum is defined as:
$$\tau_p = \sum_{x \in \mathbb{F}_p} \chi(x) e^{2\pi i x / p}.$$
By classical algebraic number theory (Gauss 1811):
$$\tau_p = \begin{cases} \sqrt{p} & \text{if } p \equiv 1 \pmod 4, \\ i \sqrt{p} & \text{if } p \equiv 3 \pmod 4. \end{cases}$$
In all cases, $|\tau_p|^2 = p$.

For any non-zero frequency $k \in \mathbb{F}_p^*$:
$$\sum_{x \in \mathbb{F}_p} \chi(x) e^{2\pi i k x / p} = \chi(k)^{-1} \sum_{x} \chi(k x) e^{2\pi i k x / p} = \chi(k) \tau_p.$$
For $k = 0$: $\sum_{x \in \mathbb{F}_p} \chi(x) = 0$ because there are exactly $(p-1)/2$ residues and $(p-1)/2$ non-residues.

---

## 4. Formal Proofs of Complexity Theorems

### Theorem 1: Exact Totient Peak Probability Scaling
*For any prime $p$, the van Dam-Hallgren-Ip algorithm with 1 quantum query succeeds in reconstructing the secret shift $s$ with peak measurement probability:*
$$P(\text{success}) = \frac{p - 1}{p} = 1 - \frac{1}{p}.$$
*For composite modulus $N$, using the Jacobi symbol, the peak measurement probability is exactly:*
$$P_{\text{composite}}(\text{success}) = \frac{\phi(N)}{N} = \prod_{p \mid N} \left( 1 - \frac{1}{p} \right).$$

**Proof**:  
1. **Prime Case**:  
   The query state is:
   $$|\psi_g\rangle = \frac{1}{\sqrt{p - 1}} \sum_{x \in \mathbb{F}_p, x \ne -s} \chi(x + s) |x\rangle.$$
   Applying $\text{QFT}_p$:
   $$\text{QFT}_p |\psi_g\rangle = \frac{1}{\sqrt{p(p-1)}} \sum_{k \in \mathbb{F}_p} \left( \sum_{x} \chi(x + s) \omega^{k x} \right) |k\rangle.$$
   Substituting $y = x + s$:
   $$\sum_{x} \chi(x + s) \omega^{k x} = \omega^{-k s} \sum_{y} \chi(y) \omega^{k y} = \begin{cases} 0 & \text{if } k = 0, \\ \chi(k) \tau_p \omega^{-k s} & \text{if } k \ne 0. \end{cases}$$
   Thus:
   $$\text{QFT}_p |\psi_g\rangle = \frac{\tau_p}{\sqrt{p(p-1)}} \sum_{k \in \mathbb{F}_p^*} \chi(k) \omega^{-k s} |k\rangle.$$
   Applying the phase gate $|k\rangle \mapsto \chi(k) |k\rangle$ (since $\chi(k)^2 = 1$ for all $k \in \mathbb{F}_p^*$):
   $$|\phi_{\text{canceled}}\rangle = \frac{\tau_p}{\sqrt{p(p-1)}} \sum_{k \in \mathbb{F}_p^*} \omega^{-k s} |k\rangle.$$
   Now applying the inverse $\text{QFT}_p^\dagger$:
   $$\langle z | \text{QFT}_p^\dagger |\phi_{\text{canceled}}\rangle = \frac{\tau_p}{\sqrt{p(p-1)}} \cdot \frac{1}{\sqrt{p}} \sum_{k \in \mathbb{F}_p^*} \omega^{-k s} \omega^{-k z} = \frac{\tau_p}{p \sqrt{p-1}} \sum_{k=1}^{p-1} \omega^{-k (s + z)}.$$
   - At target index $z = -s \pmod p$:  
     The exponent is $\omega^0 = 1$ for all $k \in \{1, \dots, p-1\}$.  
     The sum is $\sum_{k=1}^{p-1} 1 = p - 1$.  
     The target amplitude is:
     $$\langle -s | \text{QFT}_p^\dagger |\phi_{\text{canceled}}\rangle = \frac{\tau_p (p - 1)}{p \sqrt{p - 1}} = \frac{\tau_p \sqrt{p - 1}}{p}.$$
     The target measurement probability is:
     $$P(\text{success}) = \left| \frac{\tau_p \sqrt{p - 1}}{p} \right|^2 = \frac{|\tau_p|^2 (p - 1)}{p^2} = \frac{p (p - 1)}{p^2} = \frac{p - 1}{p} = 1 - \frac{1}{p}.$$
   - At any non-target index $z \ne -s \pmod p$:  
     The full sum over all $k \in \mathbb{F}_p$ is 0, so $\sum_{k=1}^{p-1} \omega^{-k (s + z)} = -1$.  
     The non-target probability is:
     $$P(z) = \left| \frac{\tau_p (-1)}{p \sqrt{p - 1}} \right|^2 = \frac{p}{p^2 (p - 1)} = \frac{1}{p (p - 1)}.$$
     Summing over all $p - 1$ non-target indices gives $(p - 1) \cdot \frac{1}{p (p - 1)} = \frac{1}{p}$.  
     Total probability: $\frac{p - 1}{p} + \frac{1}{p} = 1.000$.

2. **Composite Modulus Case**:  
   For $N = \prod p_i^{e_i}$, the Jacobi symbol $\chi(x) = \left( \frac{x}{N} \right)$ has non-zero values only for $x \in \mathbb{Z}_N^*$, of which there are $| \mathbb{Z}_N^* | = \phi(N)$.  
   The Gauss sum satisfies:
   $$g(\chi, k) = \begin{cases} \chi(k) \tau_N & \text{if } \gcd(k, N) = 1, \\ 0 & \text{if } \gcd(k, N) > 1. \end{cases}$$
   The sum in the target amplitude extends over only the $\phi(N)$ coprimes $k \in \mathbb{Z}_N^*$.  
   The target amplitude is:
   $$\langle -s | \text{QFT}_N^\dagger |\phi_{\text{canceled}}\rangle = \frac{\tau_N \phi(N)}{N \sqrt{\phi(N)}} = \frac{\tau_N \sqrt{\phi(N)}}{N}.$$
   The target measurement probability is:
   $$P_{\text{composite}}(\text{success}) = \left| \frac{\tau_N \sqrt{\phi(N)}}{N} \right|^2 = \frac{|\tau_N|^2 \phi(N)}{N^2} = \frac{N \phi(N)}{N^2} = \frac{\phi(N)}{N}.$$
   This holds identically for all composite moduli $N$. $\blacksquare$

---

### Theorem 2: Superposition Oracle Necessity
*The van Dam-Hallgren-Ip algorithm requires quantum superposition queries to $g(x) = \left( \frac{x+s}{p} \right)$. In any setting where the oracle is accessed via classical requests, no quantum algorithm can extract $s$ faster than classical query algorithms.*

**Proof**:  
In a classical oracle model, the adversary submits classical queries $x_1, \dots, x_T$ and receives classical responses $y_i = g(x_i) \in \{+1, -1\}$.  
The quantum state accessible to the adversary is:
$$\rho = \frac{1}{p} \sum_{x \in \mathbb{F}_p} |x\rangle \langle x| \otimes |g(x)\rangle \langle g(x)|.$$
Because $\rho$ is diagonal in the computational basis, it is a classical probability distribution over pairs $(x, g(x))$.  
By Holevo's theorem, the accessible quantum information of any POVM on a classical ensemble is bounded by the Shannon mutual information of the classical distribution:
$$I_{\text{quantum}}(s : M) \le I_{\text{classical}}(s : (X, Y)).$$
Consequently, quantum queries cannot be constructed from classical data without coherent superposition access. $\blacksquare$

---

### Theorem 3: Weil Bound & Classical Legendre PRF Hardness
*In the classical query model, finding the secret shift $s$ from pairs $(x_i, g(x_i))$ is equivalent to the Legendre PRF Key Recovery Problem. By the Weil bound, any classical algorithm requires at least $\Omega(\sqrt{p})$ operations.*

**Proof**:  
The Legendre PRF (Damgård 1988) defines the pseudorandom function $F_K(x) = \left( \frac{x + K}{p} \right)$ with secret key $K = s$.  
By the Weil bound for character sums on curves (Weil 1948):
For any distinct $s_1 \ne s_2 \in \mathbb{F}_p$, the polynomial $(x + s_1)(x + s_2)$ is not a square in $\mathbb{F}_p[x]$.  
The character correlation satisfies:
$$\left| \sum_{x \in \mathbb{F}_p} \left( \frac{x + s_1}{p} \right) \left( \frac{x + s_2}{p} \right) \right| \le 2 \sqrt{p}.$$
The normalized correlation coefficient is bounded by:
$$|\rho(s_1, s_2)| = \frac{1}{p} \left| \sum_{x \in \mathbb{F}_p} \chi(x + s_1) \chi(x + s_2) \right| \le \frac{2 \sqrt{p}}{p} = \frac{2}{\sqrt{p}}.$$
As $p \to \infty$, $\rho(s_1, s_2) \to 0$. The shifted sequences are quasi-orthogonal random sequences.  
By the collision bounds for pseudorandom function key recovery (Khovratovich 2020, Beullens et al. 2020), any classical attack based on table lookups or baby-step giant-step requires at least:
$$T_{\text{classical}} = \Omega(\sqrt{p} / \text{poly}(\log p)) = 2^{\Omega(n / 2)}.$$
Under the classical query model, the problem is cryptographically hard. $\blacksquare$

---

### Theorem 4: Phase Cancellation Factoring Barrier for Composite Moduli
*For composite moduli $N = p q$, implementing the phase gate $|k\rangle \mapsto \left( \frac{k}{N} \right) |k\rangle$ on arbitrary quantum states requires distinguishing quadratic residues modulo $N$, which is computationally equivalent to integer factoring.*

**Proof**:  
For composite $N = p q$, the Jacobi symbol is $\left( \frac{k}{N} \right) = \left( \frac{k}{p} \right) \left( \frac{k}{q} \right)$.  
A number $k$ with $\left( \frac{k}{N} \right) = 1$ is a quadratic residue modulo $N$ if and only if $\left( \frac{k}{p} \right) = 1$ and $\left( \frac{k}{q} \right) = 1$.  
The problem of distinguishing quadratic residues from pseudo-squares (elements with Jacobi symbol $+1$ but non-residues modulo $p$ and $q$) is the **Quadratic Residuosity Problem (QRP)** (Goldwasser-Micali 1982).  
It is a foundational result of algebraic cryptography that determining the Legendre symbols $\left( \frac{k}{p} \right)$ and $\left( \frac{k}{q} \right)$ without knowing the factors $p, q$ is polynomial-time equivalent to factoring $N$.  
Therefore, the phase gate cannot be implemented as an efficient circuit over $\mathbb{Z}_N$ without knowing the prime factorization of $N$. $\blacksquare$

---

## 5. Comprehensive Summary Matrix

| Metric / Property | Prime Modulus $\mathbb{F}_p$ (Superposition) | Prime Modulus $\mathbb{F}_p$ (Classical Access) | Composite Modulus $\mathbb{Z}_N$ ($N = p q$) |
| :--- | :--- | :--- | :--- |
| **Oracle Access** | Coherent Quantum Superposition | Classical Input-Output Pairs | Coherent Superposition |
| **Quantum Algorithm** | van Dam-Hallgren-Ip (1 query) | Classical Birthday / Collision | vDHI with Jacobi symbol |
| **Success Probability** | **$\frac{p - 1}{p} = 1 - \frac{1}{p}$** | N/A (Requires $\ge \Omega(\sqrt{p})$ samples) | **$\frac{\phi(N)}{N} = (1 - 1/p)(1 - 1/q)$** |
| **Classical Query Time** | $O(p)$ naive, $O(\sqrt{p})$ BSGS | **$O(\sqrt{p})$** (Legendre PRF Hardness) | $O(\sqrt{N})$ or Factoring $N$ |
| **Character Correlation** | Orthogonal via Gauss Sum $|\tau_p| = \sqrt{p}$ | Weil bound: $|\rho| \le 2/\sqrt{p}$ | Vanishes on non-coprimes |
| **Real-World API Threat** | **Zero** (Servers do not accept $|x\rangle$) | **Zero** (Legendre PRF remains secure) | **Zero** (Blocked by Factoring) |
| **Epistemic Invariant** | Model-specific theorem | Cryptographic PRF Security | Algebraic Degeneracy |

---

## 6. Verification Suite

The theorems and bounds established above are verified through:
1. `tests/test_legendre_hidden_shift_prf_demarcation.py`:
   - Exact Gauss sum identity verification ($|\tau_p|^2 = p$ for all primes $p$).
   - Exact success probability scaling $P = (p - 1)/p$ for primes $p \in [7, 11, 13, 17, 19, 23]$.
   - Exact composite totient scaling $P = \phi(N)/N$ for composite moduli ($N = 15, 21, 35$).
   - Weil bound character correlation verification ($|\sum \chi(x + s_1) \chi(x + s_2)| \le 2\sqrt{p} + 1$).
   - Epistemic invariants: `speedup_claim_allowed = False`, `accepted_speedup_candidate = False`.
2. `research/certificates/legendre_hidden_shift_crosscheck.js`:
   - Independent JavaScript verification of Gauss sums, totient peak probabilities, and Weil bounds.
3. Negative Result Registry:
   - `NEG-LEGENDRE-HIDDEN-SHIFT-CLASSICAL-PRF-DEMARCATION` registered in `research/registry/negative_results.json`.
