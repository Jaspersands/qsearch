# Hidden Structure Problem Taxonomy and Epistemic Research Ledger

**Investigation**: Investigation 25 (Taxonomy & Problem Ledger)  
**Date**: 2026-10-11  
**Status**: AUDITED & REVISED (Formal Retraction of Universal 4-Class Partitioning Theorem)  
**Core Invariants**: `speedup_claim_allowed = False`, `accepted_speedup_candidate = False`  

> [!WARNING]
> **Adversarial Audit Retraction Notice (2026-10-11)**:
> The previously claimed **"Universal Quantum Hidden Structure Classification Theorem"** (asserting that all algebraic hidden structure problems partition into four exhaustive, mutually exclusive classes $\mathcal{Q}_{\text{exp}}, \mathcal{C}_{\text{poly}}, \mathcal{S}_{\text{subexp}}, \mathcal{I}_{\text{exp}}$ and precluding all other quantum speedups) is **FORMALLY WITHDRAWN**.
> 
> **Decisive Counterexamples & Audit Findings**:
> 1. **Parabolic Subgroups in $GL(n, q)$**: Solvable/Lie matrix groups admitting polynomial quantum algorithms (Decker et al., MFCS 2014, arXiv:1406.6511), disproving the claim that $\mathcal{Q}_{\text{exp}}$ is restricted to nilpotent central induction. The claimed classical transvection dequantization was mathematically invalid (yielding zero collisions).
> 2. **Constant-Exponent Solvable Groups**: $\mathbb{F}_p^n \rtimes H$ with $p = O(1)$ has trivial center $Z(G) = \{1\}$ and is non-nilpotent, yet admits polynomial quantum algorithms (Friedl et al., STOC 2003 / SICOMP 2014), disproving the claim that trivial center forces subexponential sieving.
> 3. **Nilpotent 2-Groups ($D_{2^k}$)**: Nilpotent of class $k-1$, yet reflection hidden subgroups satisfy $H \cap Z(G) = \{0\}$; central quotienting yields zero information, leaving the problem computationally equivalent to the Kuperberg sieve. Nilpotency is **neither necessary nor sufficient** for polynomial quantum algorithms.
> 4. **Unitary Entanglement Depth Bound Scope**: The $\Omega(n)$ entanglement depth lower bound applies strictly to unitary distillation circuits, and is bypassed by adaptive measurements (Kuperberg sieve, $E_D = 2$) and unentangled measurements (Ettinger-Høyer-Knill, $E_D = 1$).
> 5. **Stabilizer Rank Simulation**: Low-$T$-count circuits do not classically dequantize unknown non-stabilizer coset inputs via Bravyi-Gosset simulation. Proving exponential stabilizer rank for magic tensor powers is an open conjecture (Peleg et al. 2021).
> 
> In accordance with Q-Search research standards, this document replaces the unproved 4-class "universal theorem" with an auditable **Multi-Dimensional Research Taxonomy and Epistemic Problem Ledger**.

---

## 1. Executive Overview

The landscape of quantum speedups for algebraic hidden structure problems cannot be reduced to a coarse one-dimensional partition. Algorithmic tractability depends on an intricate interplay of algebraic, representation-theoretic, and oracle access parameters.

We establish an auditable research taxonomy parameterized by four structural axes:
$$(\mathcal{G}, \mathcal{P}, \mathcal{M}, \mathcal{F})$$
where:
- $\mathcal{G}$ is the ambient group family (abelian, bounded-class nilpotent, general nilpotent, constant-exponent solvable, growing-exponent solvable, symmetric, or classical Lie/matrix group).
- $\mathcal{P}$ is the subgroup promise (normal, bounded index, parabolic/unipotent, cyclic, reflection/involution, or general).
- $\mathcal{M}$ is the oracle access model (multiplicative black-box evaluation, additive Lie algebra Fourier sampling, or explicit generator presentation).
- $\mathcal{F}$ is the underlying field / exponent regime (constant characteristic, growing characteristic, or $2^n$).

---

## 2. Structural Parameter Axes

### Axis 1: Group Algebraic Structure ($\mathcal{G}$)
1. **Abelian Groups**: $G \cong \prod \mathbb{Z}_{d_j}$. All irreps are 1-dimensional; abelian QFT extracts character evaluations directly in $\text{poly}(\log |G|)$ gates.
2. **Bounded-Class Nilpotent Groups**: Lower central series terminates in $c = O(1)$ steps. Central quotients $G_i / G_{i+1} \le Z(G / G_{i+1})$ can be dismantled inductively via Shor's abelian QFT in $\text{poly}(\log |G|)$ gates (Ivanyos et al. 2007).
3. **General Nilpotent Groups with Growing Class**: E.g. $D_{2^k}$ (class $k-1$) or unitriangular $U_n(\mathbb{F}_q)$ (class $n-1$). Central induction fails when $H \cap Z(G) = \{1\}$; requires adaptive sieving or remains open.
4. **Constant-Exponent Solvable Groups**: Solvable groups with derived length $d = O(1)$ and exponent $e = O(1)$ (e.g. $\mathbb{F}_p^n \rtimes H$ with $p = O(1)$). Solved in polynomial quantum time despite $Z(G) = \{1\}$ (Friedl et al. 2003).
5. **Growing-Exponent Solvable Groups**: E.g. $D_N$ ($N$ odd) or $AGL(1, p)$ ($p = 2^{\Omega(n)}$). Relative phases live on continuous circles; subject to Kuperberg sieve collision entropy $2^{\Omega(\sqrt{\log N})}$.
6. **Symmetric & Alternating Groups**: $S_n, A_n$. Typical irreps have factorial dimensions $d_\lambda = 2^{\Omega(n \log n)}$. Single-copy Fourier sampling is factorially extinguished; multi-copy commutants have dimension $(n!)^m$.
7. **Classical Lie / Matrix Groups**: $GL(n, \mathbb{F}_q), Sp(2n, \mathbb{F}_q), SO(n, \mathbb{F}_q)$. Behavior depends sharply on whether the subgroup is unipotent/parabolic (BQP tractable) or a maximal torus (factorial commutant intractability).

### Axis 2: Subgroup Promise ($\mathcal{P}$)
1. **Normal Subgroups**: $H \trianglelefteq G$. For all finite groups, normal HSP is in BQP via abelianization and commutator quotienting (Hallgren et al. 2000).
2. **Parabolic / Flag Stabilizers**: $H = P_W = \text{Stab}(W)$. Contains an abelian or nilpotent unipotent radical $U_W$. In $GL(n, q)$, solved in BQP (Decker et al. 2014).
3. **Cyclic / Unipotent Subgroups**: $H = \langle g \rangle$. In abelian groups, solved by Shor; in non-abelian groups, generally open unless $g$ acts centrally or admits a solvable embedding.
4. **Involutions / Reflections**: $H = \{1, \tau\}$ with $\tau^2 = 1$. Standard model for Graph Isomorphism ($S_n$), Code Equivalence ($W_n$), and Dihedral HSP ($D_N$).

### Axis 3: Oracle Access Model ($\mathcal{M}$)
1. **Multiplicative Black-Box Oracle**: $f: G \to S$ with $f(x) = f(y) \iff x y^{-1} \in H$. Standard HSP model.
2. **Additive / Lie Algebra Oracle**: Oracle evaluates linear cosets over a vector space or Lie algebra $(\mathfrak{g}, +)$.
3. **Generator / Matrix Presentation**: Group and subgroup are specified by explicit generating sets. Bypasses black-box query lower bounds; amenable to classical linear algebra and group-theoretic algorithms (Babai, Luks, Beals).

---

## 3. The Audited Epistemic Problem Ledger

The table below summarizes the exact mathematical status of key hidden structure problems across classical and quantum complexity, with verified literature citations.

| Problem Family | Group $\mathcal{G}$ & Promise $\mathcal{P}$ | Access Model $\mathcal{M}$ | Classical Query Lower Bound | Best Classical Algorithm | Quantum Complexity Upper Bound | Quantum Obstruction / Lower Bound | Epistemic Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **Abelian HSP** | Abelian $G$, arbitrary $H$ | Multiplicative | $\Omega(\sqrt{\|G\|})$ (Birthday) | $O(\sqrt{\|G\|})$ | **$\text{poly}(\log \|G\|)$** (Shor 1994) | Unconditional query bound $\Omega(\log \|G\|)$ | **Proved BQP Speedup** |
| **Heisenberg HSP** | $H_{2n+1}(\mathbb{F}_p)$, isotropic $H$ | Multiplicative | $\Omega(p^{n/2})$ | $O(p^n)$ | **$\text{poly}(n, \log p)$** (Hallgren et al. 2000) | None | **Proved BQP Speedup** |
| **Bounded Nilpotent HSP** | Nilpotent class $c = O(1)$ | Multiplicative | $\Omega(\sqrt{\|G\|})$ | $O(\sqrt{\|G\|})$ | **$\text{poly}(\log \|G\|)$** (Ivanyos et al. 2007) | None | **Proved BQP Speedup** |
| **Nilpotent 2-Group HSP** | $D_{2^k}$, reflection $H \cong \mathbb{Z}_2$ | Multiplicative | $\Omega(2^{k/2})$ | $2^{O(\sqrt{k})}$ | **$2^{O(\sqrt{k})}$** (Kuperberg 2005) | Central induction yields 0 bits; $E_D \ge 0.63k$ for unitary | **Open in BQP** |
| **Const-Exponent Solvable** | $\mathbb{F}_p^n \rtimes H$, $p=O(1)$ | Multiplicative | $\Omega(p^{n/2})$ | $2^{\Omega(n)}$ | **$\text{poly}(n)$** (Friedl et al. 2003) | None | **Proved BQP Speedup** |
| **Growing-Exponent Solvable** | $D_N$, $N$ odd, reflection $H$ | Multiplicative | $\Omega(\sqrt{N})$ | $2^{O(\sqrt{\log N})}$ | **$2^{O(\sqrt{\log N})}$** (Kuperberg 2005) | Collision pool $P \ge 2^{\Omega(\sqrt{\log N})}$; $E_D \ge 0.63n$ unitary | **Open in BQP** |
| **Parabolic HSP in $GL(n, q)$** | $GL(n, \mathbb{F}_q)$, parabolic $P_W$ | Multiplicative | $\Omega(q^{n/2})$ | $2^{\Omega(n)}$ queries | **$\text{poly}(n, \log q)$** (Decker et al. 2014) | None | **Proved BQP Speedup** |
| **Siegel Parabolic in $Sp(2n, q)$** | $Sp(2n, \mathbb{F}_q)$, Siegel $P_W$ | Multiplicative | $\le O(n q^n)$ queries | $O(n q^n)$ (Transvections) | Open for mult oracle; $\text{poly}$ for additive | Mult-to-additive reduction open; char-2 trace pairing fails | **Unestablished** |
| **Isotropic Parabolic in $Sp(2n, q)$ ($k \le O(\log n)$)** | $Sp(2n, \mathbb{F}_q)$, isotropic $P_U$ | Multiplicative | $O(n q^k)$ | $O(n q^k)$ (Transvections) | $\text{poly}(n)$ classical | Classical dequantization via $T_u \in P_U \iff u \in U^\perp$ | **Dequantized Classically** |
| **Maximal Torus in $GL(n, q)$** | $GL(n, \mathbb{F}_q)$, $T \cong (\mathbb{F}_q^\times)^n$ | Multiplicative | $\Omega(q^{n(n-1)/4})$ | $2^{\Omega(n^2 \log q)}$ | Open ($2^{O(n \log n)}$) | Single-copy $I \le 2^{-\Omega(n^2)}$; commutant $(n!)^m$ | **Strong Quantum Barrier** |
| **Graph Isomorphism** | $S_n$, involution $H \cong \mathbb{Z}_2$ | Multiplicative | $\Omega(\sqrt{n!})$ | $2^{O(\log^c n)}$ (Babai 2016) | Open | Single-copy $I \le \frac{1}{2 \ln 2 \cdot n!}$; commutant $(n!)^m$ | **Strong Quantum Barrier** |
| **Linear Code Equivalence** | $W_n = (S_n \times S_n) \rtimes \mathbb{Z}_2$ | Multiplicative | $\Omega(n!)$ | Quasi-poly for LCD / bounded-hull | Open | Single-copy $I \le \frac{1}{2 \ln 2 \cdot n!}$; commutant $(n!)^m$ | **Strong Quantum Barrier** |
| **Monomial Code Decoupling** | Monomial phases $(\mathbb{F}_q^\times)^n$ | Matrix generator | $O(kn)$ | $O(kn)$ (Projective normalization) | $O(kn)$ classical | Classical subsumption | **Dequantized Classically** |
| **Self-Dual Code Gauge** | $GL_k(\mathbb{F}_2)$ row scrambler | Matrix generator | $O(k^2 n)$ | $O(k^2 n)$ (Classical RREF) | $O(n^3)$ classical | Gauge dimension eliminated classically | **Dequantized Classically** |
| **Algebraic Geometry Codes** | Curve automorphism | Matrix generator | $O(n^4)$ | $O(n^4)$ (Star square / conductor) | $O(n^4)$ classical | Classical subsumption | **Dequantized Classically** |
| **CFI Graphs ($\Delta \le 4$)** | Color flip automorphisms | Graph adjacency | $O(n^4)$ | $O(n^4)$ (Luks solvable towers) | $O(n^4)$ classical | Classical subsumption | **Dequantized Classically** |
| **Cospectral Graphs (Godsil-McKay)** | Switching cospectral pairs | Graph adjacency | $O(n^3)$ | $O(n^3)$ (2-Weisfeiler-Lehman) | Continuous walk blinded ($I = 0$) | Quantum walk invariant blind; 2-WL splits | **Dequantized Classically** |

---

## 4. Master Cross-Reference Table of Investigations 1–28

| # | Investigation Focus | Domain | Primary Obstruction / Mechanism | Epistemic Status |
| :-: | :--- | :--- | :--- | :---: |
| **1** | Modular Subset-Sum Coherent Erasure | DCP / Lattices | Open channels induce total decoherence ($\text{Tr}(\rho_X^2) \le 2^{-n}$) | Valid Mathematical Obstruction |
| **2** | Non-Commutative Phase Gradient Sieve | DHSP / Sieve | Commutant dim $P+1$; pool collision entropy $P \ge 2^{\Omega(\sqrt{\log N})}$ | Valid Mathematical Lower Bound |
| **3** | Voronoi Quantum Walk on SVP | Lattices / SVP | Overlap $|\langle s\|v_{\min}\rangle|^2 \le 2^{-\Omega(n)}$; walk takes $2^{\ge 0.5 n} \gg 2^{0.292 n}$ | Valid Mathematical Obstruction |
| **4** | Fractional Knapsack Integrality Gap | Lattices / BDD | LP vertices $\Omega(2^n/n)$; branch-and-bound tree $\ge 2^{n - O(\log n)}$ | Valid Classical Hardness Proof |
| **5** | Modular Transfer Pseudospectrum | QSVT / Operators | Eigenvalue spacing $2^{-n/2}$; QSVT polynomial degree $d \ge \Omega(2^{n/2})$ | Valid Operator Lower Bound |
| **6** | Information-Set Invariant Tensor Barrier | Code Equivalence | Grover search on $N_{\text{info}}$ takes $\Omega(2^{n/2}/n^{1/4})$, dominated by Sendrier $O(n^3)$ | Valid Classical Subsumption |
| **7** | Multi-Copy Commutant on $W_n$ | Code Equivalence | $\|\overline{\rho}_k - I\|_{\text{tr}} \le \sqrt{k/n!}$; requires $k \ge \Omega(n!)$ copies | Valid Representation Lower Bound |
| **8** | Hull Dimension & Reduction to GI | Code Equivalence | Gram nullity invariant; LCD ($h=0$) and bounded-hull solve in $2^{O(\log^c n)}$ | Valid Classical Subsumption |
| **9** | Star-Product Filtering on AG Codes | Algebraic Codes | $\dim(C*C) \le 2k+g-1$; conductor filtration reconstructs curve in $O(n^4)$ | Valid Classical Subsumption |
| **10** | Projective Column Normalization | Monomial Codes | Monomial phase group $(\mathbb{F}_q^\times)^n$ eliminated classically in $O(kn)$ | Valid Classical Subsumption |
| **11** | Weisfeiler-Lehman Depth under $A' = QAQ$ | Graph Isomorphism | $Q\mathbf{1}=\mathbf{1}$ blinds 1-WL; 2-WL splits colors in $O(n^3)$ | Valid Classical Subsumption |
| **12** | Strongly Regular Bose-Mesner Invariance | Strongly Regular | Bose-Mesner algebra dim 3; all walk moments parameter-invariant | Valid Invariance Proof |
| **13** | Kronecker Multiplicities & Racah Circuits | Multi-Copy HSP | Kronecker coeff $g = 2^{\Omega(n)}$; diagonalizing requires $2^{\Omega(n)}$ gates | Valid Complexity Lower Bound |
| **14** | AGL(1, p) Character Vanishing | Affine HSP | Reflection character identically zero: $\chi_\rho(-1, s) \equiv 0$; reduces to DHSP | Valid Algebraic Reduction |
| **15** | Rooted Graphlet Tensor Trilemma | Tensor Networks | Bounded-depth dequantized in $O(n)$; global contractions $\#P$-hard | Valid Complexity Dichotomy |
| **16** | Add-Mult Incompatibility & Characters | Character Shift | Cross-correlation $\le 1/\sqrt{q}$; queries yield $O(\log q)$ bits | Valid Analytic Bound |
| **17** | Higher-Degree Bombieri-Weil Bound | Higher-Degree | Fourier probability $P(k) \le (d-2)^2/p$; mutual info $I \le 2^{-\Omega(n)}$ | Valid Number-Theoretic Bound |
| **18** | Adversarial Phase Noise Sensitivity | Oracle Robustness | Perturbation $\epsilon$ induces output error $2 T^2 \epsilon$; QEC distance $d \ge \Omega(T)$ | Valid Stability Analysis |
| **19** | Dihedral Coset Magic State T-Count | Magic State Theory | Target phase in Clifford level $n$; $T$-count $\ge 3n$; pool requires $2^{\Omega(\sqrt{n})}$ magic | Valid Fault-Tolerant Bound |
| **20** | The Commutant Rank Dilemma | Commutant Theory | Rank $\le \text{poly}$ dequantized by Monte Carlo; rank $2^{\Omega(n)}$ takes $2^{\Omega(n)}$ gates | Valid Representation Dichotomy |
| **21** | Lie-Type Matrix Groups & Deligne-Lusztig | Lie Matrix HSP | Parabolic HSP in BQP (Decker et al.); maximal tori have $(n!)^m$ commutant | Audited: Transvection claim retracted |
| **22** | The Nilpotent-Solvable Complexity Landscape | Structural HSP | Constant-exponent solvable in BQP; growing-exponent solvable/nilpotent-2 open | Audited: Dichotomy corrected |
| **23** | Unitary Entanglement Depth Lower Bound | Entanglement Theory | Unitary circuits require $E_D \ge 0.631 n$; bypassed by adaptive sieves & EHK | Audited: Scope & constants corrected |
| **24** | Stabilizer Nullity & Fault-Tolerant Overhead | Resource Theories | Magic state burden $\Omega(P \log^2 P) = 2^{\Omega(\sqrt{n})}$ for sieves | Audited: Dequantization claim retracted |
| **25** | Hidden Structure Research Taxonomy | Meta-Complexity | Replaced universal 4-class partition with audited multi-dimensional ledger | Audited: Master taxonomy established |
| **26** | Symplectic Parabolic Counteralgorithm & Gaps | Lie Matrix HSP | Transvections test $v \in W$ in $O(n q^n)$; quantum reduction unestablished | Audited: Lower bound disproved |
| **27** | Symplectic Parabolic Obstruction & Partition Barrier | Lie Representation | Ambient density collapses $q^{-1.5 n^2}$; Gel'fand rank $n+1$ spherical extinction; Partition commutant $B(2M) \ge (2M-1)!!$ gates | Proved Mathematical Obstruction |
| **28** | Isotropic Parabolic Spectrum & Dequantization | Lie Matrix HSP | $T_u \in P_U \iff u \in U^\perp$ solves HSP in $O(n q^k)$ queries; Heisenberg $k=1$ in $O(q n)$ polynomial time; Heisenberg radical $U_1$ abelian in char 2 vs class 2 in char $\ge 3$; $(Sp(4, \mathbb{F}_2), P_1)$ Gel'fand rank 3 with irreps $[1, 5, 9]$ | Proved Theorems & Classical Dequantization |

---

## 5. Epistemic Commitments & Current Research Mandate

1. **No Speedup Claims Without End-to-End Proofs**: `speedup_claim_allowed = False` and `accepted_speedup_candidate = False` remain strictly enforced.
2. **Adversarial Scrutiny of Classical Baselines**: Classical black-box query lower bounds must be challenged against adaptive, structured queries (as demonstrated by the transvection counteralgorithm in Investigation 26).
3. **Epistemic Integrity**: Preserving counterexamples, retractions, and negative results is essential to genuine mathematical research. Every theorem statement must carry precise hypotheses, access models, and asymptotic regimes.
