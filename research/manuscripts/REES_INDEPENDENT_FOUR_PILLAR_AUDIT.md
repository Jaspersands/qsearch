# Independent Four-Pillar Audit of Rees HSP Solution

**Date:** 30 October 2026
**Auditor:** External AI-assisted specialist audit (Consolidated multi-agent review across four independent specialized auditors: Proof & Resource Auditor, Prior-Art Analyst, Scope Auditor, Application & Significance Analyst).
**Status:** Formal technical review and disposition for Codex. **Automated technical audit, NOT human peer review or an external novelty certificate.** No unauthorized Git, network, or external actions performed.

---

## Executive Summary

This audit provides an adversarial, line-by-line scrutiny of the Rees Hidden Subgroup Problem (HSP) solution across the four core areas requested by Codex and external evaluation directives:
1. **Complete Proof Scrutiny, State Conversion, Recursion & Full Resource Accounting** (including the exact Lean 4 verification boundary).
2. **Definitive Prior-Art Assessment & Growing-$p$ Barriers** (distinguishing lack of direct subsumption from proof of novelty, respecting corrections R1 and R2).
3. **Rigorous Scope Checking & Failure Boundaries** (explicit Lie algebras vs. black-box groups, prime-power Lie rings, and the relation-lattice vs. $\Omega_1$ trap).
4. **Applications, Classical Dequantization Landscape & Practical Significance** (concrete resource wall at $1.56 \times 10^{21}$ queries, comparison with Shor's algorithm, and 10 criteria for escaping classical collapse).

---

## 1. Scrutiny of the Complete Proof & Resource Accounting

### 1.1 State Conversion Mechanics
* **Spectral Projectors and Multiplicity Cancellation:**
  For $Z \le Z(G)$ elementary abelian over $\mathbb{F}_p$ and non-normal $H \le G$, spectral projectors $\Pi_\lambda = |Z|^{-1}\sum_{z \in Z} \chi_\lambda(-z) R_z$ commute with $\rho_H = |G|^{-1}\sum_{h \in H} R_h$ because $Z \le Z(G)$ implies $R_z R_h = R_{hz} = R_h R_z$. When $K = H \cap Z \neq 1$, $\operatorname{Tr}(\rho_H \Pi_\lambda) = \frac{|K|}{|Z|} 1_{K^\perp}(\lambda)$. For any $\lambda \in K^\perp$ and $g = h_0 z_0 \in HZ$, the $|K|$ preimages in the sum cancel $|K|^{-1}$, yielding $\operatorname{Tr}(\rho_\lambda R_g) = \chi_\lambda(z_0)$ identically independent of the coset representative decomposition. Zero-probability branches ($\lambda \notin K^\perp$) have mass identically zero and are never conditioned on.
* **Non-Homomorphic Section Coboundary Absorption:**
  Let $\pi: G \twoheadrightarrow Q = G/Z$ and $\sigma: Q \to G$ be an arbitrary public section ($\pi(\sigma(q)) = q$). In general, $\sigma$ is **not** a group homomorphism: $\sigma(r)^{-1}\sigma(q) = \sigma(r^{-1}q) \cdot z_{\text{coboundary}}$ with $z_{\text{coboundary}} \in Z$. On active slots $I = \{i : s_i \neq 0\}$, the reduced control register evaluates:
  $$\rho_{\text{out}}[q,r] = \frac{1}{|Q|} \prod_{i \in I} \operatorname{Tr}\!\left(\rho_{\lambda_i} R_{\Delta_{s_i}(\sigma(r)^{-1}\sigma(q))}\right).$$
  Because $\Delta_{s_i}(z_{\text{coboundary}}) = s_i^d z_{\text{coboundary}}$, the coboundary factor incurs phase $\chi_{\sum_{i \in I} s_i^d \lambda_i}(z_{\text{coboundary}}) = \chi_0(z_{\text{coboundary}}) = 1$ because the SDE solution enforces $\sum_{i \in I} s_i^d \lambda_i = 0$. Thus, **all section coboundaries are absorbed into $Z$ and annihilated by the SDE relation.**
* **Inactive Slot Padding:**
  When $s_i = 0$, $\Delta_0$ is not an automorphism. The algorithm **must** pad inactive slots with the identity operator $I$, evaluating $\operatorname{Tr}(\rho_{\lambda_i} I) = 1$. The state conversion is sound if and only if $I \neq \emptyset$ (at least one active scale is nonzero).

### 1.2 Recursion Mechanics & Disjoint Preparation Trees
* **Grade-1 Retention of Derived Subgroups:**
  At the end of descending stages $d = c, c-1, \dots, 2$, the remaining grade is $A_1 = tL$, where $tL \cong L$ as an additive group. The hidden subgroup image is $t(\mathfrak{h} \cap \gamma_1(L)) = t\mathfrak{h}$. Unlike the associated graded Lie algebra $\operatorname{gr}_1(L) = L/[L,L]$ (which completely erases derived components), $A_1 = tL$ retains all of $\mathfrak{h} = \log H$, including elements in $[L,L]$.
* **Mandatory Disjoint Fresh Preparation Trees:**
  Pointwise record independence ensures that for each successful branch, the output state $\rho_{HZ/Z}$ is in an exact tensor product with classical records $(\boldsymbol{\lambda}, \mathbf{s})$. However, reusing coset banks or correlated samples across recursion stages is **completely fatal**:
  1. *Opposite-character cancellation:* Separable correlated banks can satisfy $k a + 2(-k/2)a = 0 \pmod p$, leaking hidden generator coordinates into unheralded phase cancellation.
  2. *Basis-dependence bias:* Correlating banks introduces off-diagonal coherences that break right-translation invariance.
  3. *Conditioning distortion:* Reusing states across stages conditions on previous SDE acceptance, invalidating the i.i.d. Haar-like distribution over $K_d^\perp$.
  Therefore, independent, disjoint preparation trees (costing $N_{\text{inst}} \le 2mP$) are strictly non-negotiable.

### 1.3 Full Resource Accounting
* **Instrument Counts & Diamond-Norm Budget:**
  Total instruments across all recursive stages satisfy $N_{\text{inst}} = N_{\text{leaf}} + N_{\text{merge}} + N_{\text{read}} \le 2mP$. Using unconditional diamond-norm contractivity without postselection division, allocating $\varepsilon / (3 N_{\text{inst}})$ per physical gate/instrument guarantees that total channel error remains bounded by $\varepsilon/3$.
* **Uniform ODE BCH Denominators:**
  Uniform ODE integration of the BCH series costs $O(c^4)$ Lie brackets with rational coefficients in $\mathbb{Z}[1/c!]$. Denominators are invertible for all primes $p > c$.

### 1.4 Exact Lean 4 Verification Boundary

The following table catalogs what the Lean 4 formalization kernel-verifies versus what remains unverified paper/Python obligations:

| Component | Status in Lean 4 | Verified In File | Unverified Paper/Python Obligation |
| :--- | :--- | :--- | :--- |
| **Rees Lie Homogenization** | **Kernel-Verified** | `formal/Formal/ReesHomogenization.lean` | None. Algebraically complete for all $c < p$. |
| **Vandermonde Invertibility** | **Kernel-Verified** | `formal/Formal/ReesHomogenization.lean` | None. Distinct points in $\mathbb{F}_p^\times$ are invertible for $c < p$. |
| **Central Projection $\Pi_\lambda$** | **Kernel-Verified** | `formal/Formal/CentralCharacterDescent.lean` | Full density-matrix projector trace norm. |
| **Non-Transverse Multiplicity $|K|$** | **Kernel-Verified** | `formal/Formal/ReesHomogenization.lean` | Physical POVM dilation and instrument error bounds. |
| **Group BCH Transport ($c \le 3$)** | **Kernel-Verified** | `formal/Formal/BCHClassThree.lean` | None for class $c \le 3$. |
| **Group BCH Transport ($c \ge 4$)** | **Unverified in Lean** | Paper only (`theorems/uniform_bch_rees.py`) | Formal proof that $\exp \circ E_s \circ \log$ is a group homomorphism for $c \ge 4$. |
| **SDE Receiver Theorem** | **Assumed Axiom** | Paper only (`formal/Formal/CentralCharacterDescent.lean`) | Total SDE policy is an unverified axiom (`total_sde_policy_hyp`). |
| **Ivanyos–Santha SDE Solvers** | **Unverified in Lean** | Paper/Python (`theorems/pilot_receiver_policy.py`) | No Lean code for collision tree, arity bounds, or Hensel lifting. |
| **Gate Synthesis & Clocks** | **Unverified in Lean** | Paper/Python only | Solovay–Kitaev decomposition, diamond-norm error hybrid, depth-first DAG space. |

---

## 2. Definitive Prior-Art & Novelty Assessment

### 2.1 Comparison with Published Literature

| Prior Work | Model / Family | Prime / Exponent Regime | Barrier at Class $c \ge 3$ with Growing $p$ |
| :--- | :--- | :--- | :--- |
| **Ivanyos–Sanselme–Santha (2007/2012)** | Nilpotent class $c=2$ | Any $p$ | Fails at $c \ge 3$: non-homogeneous lines dilate outside $\mathfrak{h} + \gamma_c(L)$; cross-terms cannot be linearized into central characters. |
| **Ivanyos–Santha (2015/2017)** | Diagonal equations & HPGP | Fixed degree $d$, growing $p$ | HPGP assumes univariate/abelian normal subgroup. In class $c \ge 3$, codimension-1 normal subgroups are non-abelian; coset offsets scramble coefficients. |
| **Imran–Ivanyos (2023/2024)** | Nilpotent class $c \ge 3$ | **Bounded primes only** ($p = O(1)$) | Uses untwisted translations on unhomogenized $G$; requires zero-sum subsequences (Davenport constant $\ge p$) or Fermat degree-$(p-1)$ powers ($p^{\Omega(p^2 \log p)}$). |
| **Morales (2026)** | Quasi-Hamiltonian / Semidirect | Specific split semidirect | Requires abelian normal base and split scalar action; fails on filiform and non-split central extensions. |
| **Imran (2026)** | Parabolic subgroups in $\mathrm{GL}_n$ | Special linear Lie type | Exploits matrix root spaces; does not apply to abstract or non-matrix nilpotent groups. |
| **Ivanyos–Magniez–Santha (2001)** | Commutator-bounded | $|[G,G]| = \mathrm{poly}(\log |G|)$ | Requires small derived group; fails when derived subgroup grows as $p^r$ with large $p$. |

### 2.2 Reconciling Corrections R1 and R2
* **Correction R1 (BCH Denominators):** BCH coefficients have denominators whose prime factors are at most $c$ (i.e. lying in $\mathbb{Z}[1/c!]$), NOT dividing $c!$. (At $c=3$, the coefficient $1/12$ occurs; $12 \nmid 6$).
* **Correction R2 (SDE Bounds are Not $\Omega$ Lower Bounds):** The published Ivanyos–Santha collision arity $B_d(r_d)$ is an upper bound on a specific collision algorithm, NOT an established complexity lower bound $\Omega(r^d)$. In fact, for $\gcd(d, p-1)=1$, ordinary linear algebra over $\mathbb{F}_p$ yields degree-$d$ witnesses with only $r_d+1$ columns.

### 2.3 Why Not Finding an Exact Published Result $\ne$ Proof of Novelty
Novelty cannot be asserted merely because a keyword search fails to find "Rees algebra quantum HSP." The positive Rees algebra $A = \bigoplus_{r=1}^c t^r \gamma_r(L)$ and the Lazard correspondence are classical mathematics (Rees 1956, Lazard 1969). The algorithmic novelty, if upheld, rests specifically on:
1. Recognizing that $c$ coherent evaluations of an unhomogenized oracle $U_f$ simulate an exact oracle for the homogenized Lie cover $(\exp A, \widetilde{H})$.
2. Coupling homogeneous degree-$d$ automorphisms $\Delta_s$ with central character measurement to replace Imran–Ivanyos's exponential zero-sum requirement with Ivanyos–Santha's fixed-degree diagonal equations.

---

## 3. Rigorous Scope Checking & Failure Boundaries

### 3.1 Primary Explicit $\mathbb{F}_p$ Lie Algebra Model
* **Assumptions:** Explicit basis and structure constants over $\mathbb{F}_p$; odd prime $p > c$; coherent fixed-width XOR oracle $U_f |x\rangle|y\rangle = |x\rangle|y \oplus f(x)\rangle$.
* **Robustness:** Handles non-normal, non-transverse $H$. Extends to projective and noisy state sources via twirled coset-center purifications.

### 3.2 Parameterized Extension ($r = \dim[L,L]$)
* **Actual-Class Preprocessing ($F1$):** Class $c$ must be computed first by public linear algebra in $\le n$ strict decreases.
* **Symmetric Contraction:** Requires large characteristic $p \ge 16 g_d^{2g_d+2}$ to guarantee that diagonal zero-sum vectors have nonzero coordinates, shrinking query arity to $(r_d+1)((g_d-1)r_d+1)$.

### 3.3 Explicit Prime-Power Lie Rings
* **Scope:** $\bigoplus \mathbb{Z}/p^{a_i}\mathbb{Z}$ with $p > c$.
* **FPT Limitation:** Prime-power descent is **FPT in $(c, r)$, NOT polynomial in unrestricted rank.**
  * *$\mathbb{Z}/9 \times \mathbb{Z}/9$ Non-Unit Scale Falsifier:* Without uniform valuation batching, mixed valuations prevent Hensel lifting because leading coefficients vanish mod $p$.
  * *$\mathbb{Z}/5^4$ $[x,y]=5y$ Falsifier:* Class-vs-rank disconnect proves that derived cyclic rank does not bound nilpotency class over rings.

### 3.4 Black-Box Nilpotent Groups: Two Critical Pitfalls
* **Pitfall 1: Semi-Elementary Descent vs. $\Omega_1$ ($C_{p^2} \rtimes C_p$ Counterexample):**
  In black-box groups, descending via $L = \pi^{-1}(A[p])$ terminates when the abelianization $A = K/(K'H_0)$ is elementary abelian. **Elementary abelian abelianization does NOT imply exponent $p$.**
  *Counterexample:* The group $G = C_{p^2} \rtimes C_p = \langle a, b \mid a^{p^2}=b^p=1, [a,b]=a^p \rangle$ has $G' = \langle a^p \rangle \cong C_p$ and $G/G' \cong C_p \times C_p$ (elementary abelian), but $\exp(G) = p^2$. Restricting to the order-$p$ subgroup $\Omega_1(G)$ cannot be done by abelianization quotienting alone; it requires an explicit relation-lattice torsion preimage in Lazard coordinates.
* **Pitfall 2: Free Lie Pullback Dimension Explosion:**
  For a black-box group with $s$ generators, the free class-$c$ nilpotent Lie algebra $F_{s,c}$ has dimension $d = \sum_{j=1}^c \dim \operatorname{Lie}_j(s) \sim s^c / c$. This dimension grows **exponentially** in $c$ and can vastly exceed the black-box encoding width $b = \lceil \log_2 |G| \rceil$. Algorithmic bounds stated in terms of $b$ cannot be substituted for Lie dimension $n$ without paying the $s^c$ dimension penalty.

---

## 4. Applications, Classical Dequantization & Practical Significance

### 4.1 Quantitative Resource Reality Check

The table below contrasts the concrete query costs across nilpotency class $c$:

| Class $c$ | Exponent in $n$ (Published IS SDE) | Exponent in $n$ (Oct 29 Symmetric Contraction) | Benchmark Query Count ($r=c-1, p=2^{127}-1$) |
| :---: | :---: | :---: | :---: |
| **2** | 3 | 3 | $1.42 \times 10^3$ |
| **3** | 11 | 5 | $8.95 \times 10^4$ |
| **4** | 23 | 7 | $1.21 \times 10^7$ |
| **6** | 59 | 11 | $4.87 \times 10^{11}$ |
| **8** | 119 | 15 | $6.20 \times 10^{15}$ |
| **12** | 335 | 23 | **$1.56 \times 10^{21}$** |

Even after the dramatic October 29 symmetric contraction, the live query ledger records **$1.56 \times 10^{21}$ queries at $c=12$**. This definitively ends any claim of practical speedup or near-term utility.

### 4.2 Comparison with Shor's Algorithm
* **Shor's Algorithm:** Solves abelian HSP (order finding/factoring) with $O(n^2 \log n)$ gate complexity, minimal query overhead, and direct, catastrophic cryptanalytic impact on deployed public-key infrastructure (RSA, ECC).
* **Rees HSP Algorithm:** Solves non-abelian nilpotent HSP in an oracle model. It incurs steep polynomial exponents ($n^{23}$ at $c=12$), astronomical constant factors, and does not attack any deployed cryptosystem. Its contribution is strictly structural query complexity, not practical computation.

### 4.3 Classical Dequantization Filter Matrix
Every proposed candidate application in the repository has collapsed classically due to five distinct algebraic filters:
1. **Luks Solvable Matrix-Group Stabilizer:** Solves point, vector, and subspace stabilizers in polynomial time for explicit matrix $p$-groups.
2. **Infinitesimal Lie Kernel:** Solves quadratic form stabilizers via linear systems $X^T B + B X = 0$.
3. **Reverse-Gradient PIT & No-Carry Lemma:** Evaluates arithmetic circuit stabilizers over $\mathbb{F}_p$ without carrying across digits.
4. **Polynomial Orbit-Module Rank Filter:** Learns polynomial-degree matrix invariants in classical polynomial time whenever the orbit module rank is polynomial.
5. **Moore-Gradient Semantic Filter:** Inverts semantic polynomial labels with accessible gradients.

### 4.4 Ten Constructive Criteria for Escaping Classical Dequantization
To avoid classical dequantization while remaining within the solvable regime of the Rees algorithm, an application must satisfy all ten criteria:
1. **Syntactic Degree $\delta \ge p$:** Prevents reverse-gradient polynomial identity testing.
2. **Superpolynomial Orbit-Module Rank:** Precludes low-dimensional linear representation learning.
3. **Non-Split 2-Jet Propagation:** Defeats anchored iterated-quadratic Taylor expansions.
4. **Characteristic-$p$ Ramified Multivariate Iteration:** Destroys p-adic and Archimedean metric contractivity.
5. **Non-Linear Lie Radical:** Prevents Luks reduction to linear representation stabilizers.
6. **Unknown-Affine Support Invariance:** Defeats classical prefix-support tensor-train sweeps.
7. **Homogeneous Nilpotency Class $c \ge 3$:** Ensures the problem does not fall into published ISS nil-2 algorithms.
8. **Small Nilpotency Class ($c \le 6$):** Keeps the concrete query count below the physical threshold $10^{12}$.
9. **Accessible Coherent Oracle $U_f$:** The function $f$ must be efficiently computable coherently without requiring exponential state synthesis.
10. **Non-Trivial Hidden Dimension:** The hidden subgroup must have dimension $\ge 1$ and not be normal in $G$ (avoiding simple abelian character sampling).

---

## 5. Executive Actionable Directives for Codex

1. **Cease "Practical" Framing:** Do not attempt to describe the Rees HSP solution as practical, near-term, or comparable to Shor's algorithm. Frame it strictly as an **oracle quantum complexity milestone** that closes a long-standing theoretical open problem (fixed-class nilpotent HSP with growing prime).
2. **Lean Formalization Boundary:** In all publications and documentation, explicitly state that Lean kernel-verifies the Lie-algebraic homogenization and character projection; do not claim that Lean proves the SDE receiver runtime, gate compilation, or the full algorithm.
3. **Black-Box Group Guardrails:** Never omit the relation-lattice torsion construction when claiming black-box group results; elementary abelianization does not guarantee exponent $p$ ($C_{p^2} \rtimes C_p$). Always charge the $s^c$ free Lie algebra dimension when pulling back to $F_{s,c}$.
4. **Application Sieve:** Before proposing or investing cycles in any application, run it through the **Ten Constructive Criteria** in Section 4.4. If it fails even one criterion, it collapses to classical polynomial time or quantum intractability.
