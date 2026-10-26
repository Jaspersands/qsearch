# Compact Non-Abelian Lie Group Hidden Subgroup Problem: $SU(2)$ / $SO(3)$ Wigner-D Matrix Character Blindness, Spin-Coherent Projection, and Multi-Copy Commutant Inflation

Status: SUPERSEDED / QUARANTINED_OVERBROAD_NO_GO (2026-10-19).
The spin-one Catalan formula is false; commutant dimension does not establish a
circuit lower bound or exclusion from BQP. Zero weight is not spin coherent.
Read [the counterchecks and retained scopes](NONABELIAN_BARRIER_SCOPE_AUDIT.md).
The historical text below is preserved as provenance, not endorsed mathematics.

**Historical Status (RETRACTED)**: Formally Proved & Computationally Verified
**Invariants Enforced**: `speedup_claim_allowed = False`, `accepted_speedup_candidate = False`  
**Classification**: Algebraic Quantum Algorithms / Non-Abelian Continuous Lie Groups / Representation Obstructions  
**Negative Result ID**: `NEG-SU2-COMPACT-LIE-HSP-COMMUTANT-INFLATION` (970 negative results total)

---

## 1. Executive Summary & Epistemic Scope

Investigations 42 and 43 established that continuous period finding over real quadratic and higher-degree number fields succeeds in polynomial time for fixed degree because the quotient group $T^r = \mathbb{R}^r / \Lambda_K \cong (S^1)^r$ is a compact **abelian** Lie group with 1-dimensional character representations. A central foundational question in quantum complexity theory is: **Can quantum Fourier sampling be extended to continuous non-abelian Lie groups, such as the compact group $SU(2)$ or $SO(3)$?**

In this investigation, we establish the complete algebraic, geometric, and measurement-algebraic mechanics of the Hidden Subgroup Problem over $SU(2)$ and $SO(3)$. We prove that the non-abelian structure of $SU(2)$ recreates the identical structural barriers observed in finite non-abelian groups ($S_n$, $D_N$), ruling out efficient weak Fourier algorithms:

1. **Wigner Character Conjugacy Invariance (Theorem 1)**:  
   By the Weyl character formula for $SU(2)$, the character of the irreducible representation $V_j$ (spin $j \in \frac{1}{2}\mathbb{Z}_{\ge 0}$, dimension $d_j = 2j + 1$) is a class function depending strictly on the conjugacy rotation angle $\theta \in [0, \pi]$:
   $$\chi_j(\theta) = \frac{\sin((2j + 1)\theta)}{\sin \theta}.$$
   For any subgroup $H \le SU(2)$ and any rotation $g \in SU(2)$, $\chi_j(g h g^{-1}) = \chi_j(h)$ identically for all $h \in H$.
2. **Weak Fourier Universal Orientation Blindness (Theorem 2)**:  
   For both continuous maximal tori $U(1)_\vec{n} = \{ e^{-i \theta \vec{n} \cdot \vec{\sigma}} \}$ and discrete binary polyhedral subgroups (binary tetrahedral $2T$, binary octahedral $2O$, binary icosahedral $2I$), the weak Fourier sampling distribution $P(j \mid g H g^{-1})$ is **strictly invariant under the orientation $g$**:
   $$\text{TV}(P(\cdot \mid g_1 H g_1^{-1}), \, P(\cdot \mid g_2 H g_2^{-1})) \equiv 0.000 \quad (0.000\text{ bits of mutual information}).$$
   Weak Fourier sampling extracts zero information regarding the orientation or embedding of the hidden subgroup.
3. **Rank-1 Spin-Coherent Projection (Theorem 3)**:  
   Under strong Fourier sampling, the subgroup projector for maximal torus $U(1)_\vec{n}$ onto the spin-$j$ representation $V_j$ (for integer spin $j \in \mathbb{Z}$) is strictly of **rank 1**:
   $$\Pi_{U(1)_\vec{n}}^{(j)} = |j, \vec{n}, 0\rangle \langle j, \vec{n}, 0|,$$
   projecting onto a pure **spin-coherent state** with zero magnetic quantum number along direction $\vec{n}$. For half-integer spin $j \in \mathbb{Z} + 1/2$, the projector is identically zero ($\Pi^{(j)} = 0$).
4. **Multi-Copy Catalan Commutant Inflation (Theorem 4)**:  
   For $M$ copies of the vector representation $V_1 \cong \mathbb{C}^3$, the commutant algebra of $SU(2)$-invariant observables has dimension equal to the Catalan number:
   $$\dim(\mathcal{C}_M) = C_M = \frac{1}{M+1}\binom{2M}{M} = \Theta\left( \frac{4^M}{M^{3/2}} \right).$$
   Constructing the optimal entangling measurement requires diagonalizing this algebra via Racah $6j$-recoupling circuits, which is $\#P$-hard in general (Aharonov-Jones-Landau 2009).
5. **Continuous Non-Abelian Demarcation (Theorem 5)**:  
   Unlike abelian continuous groups $(\mathbb{R}^r, +)$ where 1D character orthogonality allows efficient period finding, non-abelian compact Lie groups suffer from multi-dimensional irrep blindness ($d_j = 2j + 1$) and exponential commutant inflation, placing the $SU(2)$ / $SO(3)$ HSP outside standard BQP solvability.

---

## 2. Mathematical Formalization: $SU(2)$ Representation Theory

### Definition 1 (The Special Unitary Group $SU(2)$)
The Lie group $SU(2)$ consists of $2 \times 2$ unitary matrices with determinant 1:
$$SU(2) = \left\{ U = \begin{pmatrix} \alpha & \beta \\ -\overline{\beta} & \overline{\alpha} \end{pmatrix} : \alpha, \beta \in \mathbb{C}, \ |\alpha|^2 + |\beta|^2 = 1 \right\} \cong S^3.$$
Every element $U \in SU(2)$ can be parameterized by an axis $\vec{n} \in S^2$ and an angle $\phi \in [0, 2\pi)$ via:
$$U(\vec{n}, \phi) = \cos(\phi / 2) I - i \sin(\phi / 2) (\vec{n} \cdot \vec{\sigma}),$$
where $\vec{\sigma} = (\sigma_x, \sigma_y, \sigma_z)$ are the Pauli matrices. The rotation angle in $SO(3)$ is $\phi$, and the conjugacy class parameter in $SU(2)$ is $\theta = \phi / 2 \in [0, \pi]$.
The Haar measure on $SU(2)$ in class coordinates is:
$$d\mu(U) = \frac{2}{\pi} \sin^2 \theta \, d\theta \, d\Omega(\vec{n}).$$

### Definition 2 (Irreducible Representations & Wigner D-Matrices)
By the Peter-Weyl theorem, all irreducible unitary representations of $SU(2)$ are indexed by spin $j \in \{0, 1/2, 1, 3/2, 2, \dots\}$.
The representation space $V_j$ has dimension $d_j = 2j + 1$, with orthonormal basis $\{|j, m\rangle : m = -j, -j+1, \dots, j\}$.
The representation operators $\mathcal{D}^j(U)$ have matrix elements given by the Wigner $D$-matrices:
$$\mathcal{D}_{m, m'}^j(\alpha, \beta, \gamma) = \langle j, m | \mathcal{D}^j(\alpha, \beta, \gamma) | j, m' \rangle.$$
The character is the trace of $\mathcal{D}^j(U)$:
$$\chi_j(U) = \text{Tr}(\mathcal{D}^j(U)) = \sum_{m=-j}^j e^{2 i m \theta} = \frac{\sin((2j + 1)\theta)}{\sin \theta}.$$

---

## 3. Representation-Theoretic Blindness of Weak Fourier Sampling

### Theorem 1 (Wigner Character Conjugacy Invariance)
*For any spin $j \in \frac{1}{2}\mathbb{Z}_{\ge 0}$ and any element $h \in SU(2)$, the character $\chi_j(h)$ depends strictly on the conjugacy class parameter $\theta = \frac{1}{2} \arccos\left(\frac{1}{2} \text{Tr}(h)\right)$.*
*Consequently, for any rotation $g \in SU(2)$:*
$$\chi_j(g h g^{-1}) = \chi_j(h) \quad \forall h \in SU(2).$$

#### Proof
By cyclic permutation under the trace:
$$\text{Tr}(\mathcal{D}^j(g h g^{-1})) = \text{Tr}(\mathcal{D}^j(g) \mathcal{D}^j(h) \mathcal{D}^j(g)^{-1}) = \text{Tr}(\mathcal{D}^j(h) \mathcal{D}^j(g)^{-1} \mathcal{D}^j(g)) = \text{Tr}(\mathcal{D}^j(h)).$$
Since every element $h \in SU(2)$ is conjugate to $\text{diag}(e^{i\theta}, e^{-i\theta})$, the eigenvalues of $\mathcal{D}^j(h)$ are $\{e^{2 i m \theta} : m = -j, \dots, j\}$.
The character is the sum of these eigenvalues, which evaluates to $\frac{\sin((2j+1)\theta)}{\sin \theta}$, identically invariant under conjugation. $\blacksquare$

---

### Theorem 2 (Universal Weak Fourier Orientation Blindness)
*Let $H \le SU(2)$ be any closed subgroup (continuous torus $U(1)$ or discrete binary polyhedral group $2T, 2O, 2I$).*
*In the standard weak Fourier sampling paradigm, the probability of sampling representation $j$ from coset states of $g H g^{-1}$ is:*
$$P(j \mid g H g^{-1}) = \frac{d_j}{\text{Vol}(H)} \int_H \chi_j(g h g^{-1}) \, dh = \frac{d_j}{\text{Vol}(H)} \int_H \chi_j(h) \, dh = P(j \mid H).$$
*Consequently, for any two rotated subgroups $H_1 = g_1 H g_1^{-1}$ and $H_2 = g_2 H g_2^{-1}$:*
$$\text{TV}(P(\cdot \mid H_1), \, P(\cdot \mid H_2)) \equiv 0.000,$$
$$I(j ; g) \equiv 0.000 \text{ bits}.$$

#### Proof
By Theorem 1, $\chi_j(g h g^{-1}) = \chi_j(h)$ for every element $h \in H$.
Integrating over $H$ yields:
$$P(j \mid g H g^{-1}) = \frac{d_j}{\text{Vol}(H)} \int_H \chi_j(g h g^{-1}) \, dh = \frac{d_j}{\text{Vol}(H)} \int_H \chi_j(h) \, dh.$$
This integral evaluates strictly to the multiplicity of the trivial representation of $H$ in $V_j$:
$$\int_H \chi_j(h) \, dh = \text{mult}_H(V_j, \, \mathbf{1}).$$
- For continuous maximal torus $H = U(1)$:
  $$\frac{1}{2\pi} \int_0^{2\pi} \left( \sum_{m=-j}^j e^{2 i m \theta} \right) d\theta = \begin{cases} 1 & \text{if } j \in \mathbb{Z} \ (m = 0 \text{ exists}), \\ 0 & \text{if } j \in \mathbb{Z} + 1/2 \ (m = 0 \text{ does not exist}). \end{cases}$$
  This is identically independent of the rotation axis $\vec{n}$.
- For discrete binary polyhedral subgroups ($2T, 2O, 2I$), the character sum over $H$ is determined by McKay correspondence and is identically invariant under the ambient orientation $g$.
The total variation distance is $\text{TV} = \frac{1}{2} \sum_j |P(j \mid H_1) - P(j \mid H_2)| = 0.000$, and the mutual information is $I(j; g) = 0.000$ bits. $\blacksquare$

---

## 4. Strong Fourier Sampling: Spin-Coherent States & Commutant Inflation

Because weak Fourier sampling yields zero information, quantum algorithms must measure within the $(2j+1)$-dimensional representation space $V_j$.

### Theorem 3 (Rank-1 Spin-Coherent Projector Factorization)
*Let $H = U(1)_\vec{n} = \{ e^{-i \theta \vec{n} \cdot \vec{\sigma}} : \theta \in [0, 2\pi) \}$ be the maximal torus aligned with unit vector $\vec{n} \in S^2$.*
*For integer spin $j \in \mathbb{Z}$, the subgroup representation projector $\Pi_H^{(j)} = \int_H \mathcal{D}^j(h) \, dh$ is strictly of rank 1:*
$$\Pi_{U(1)_\vec{n}}^{(j)} = |j, \vec{n}, 0\rangle \langle j, \vec{n}, 0|,$$
*where $|j, \vec{n}, 0\rangle = \mathcal{D}^j(g) |j, 0\rangle$ is the pure spin-coherent state satisfying $(\vec{n} \cdot \vec{J}) |j, \vec{n}, 0\rangle = 0$.*
*For half-integer spin $j \in \mathbb{Z} + 1/2$, the projector is identically zero ($\Pi_H^{(j)} = 0$).*

#### Proof
The generator of $U(1)_\vec{n}$ in $V_j$ is $\vec{n} \cdot \vec{J}$, which has eigenvalues $m \in \{-j, -j+1, \dots, j\}$.
The projector onto the invariant subspace of $U(1)_\vec{n}$ is:
$$\Pi_H^{(j)} = \frac{1}{2\pi} \int_0^{2\pi} e^{-i \theta (\vec{n} \cdot \vec{J})} \, d\theta = \sum_{m=-j}^j \left( \frac{1}{2\pi} \int_0^{2\pi} e^{-i m \theta} \, d\theta \right) |j, \vec{n}, m\rangle \langle j, \vec{n}, m| = \sum_{m=-j}^j \delta_{m, 0} |j, \vec{n}, m\rangle \langle j, \vec{n}, m|.$$
- If $j \in \mathbb{Z}$, $m = 0$ is in the spectrum, and the sum contains exactly one term: $|j, \vec{n}, 0\rangle \langle j, \vec{n}, 0|$, which has rank 1.
- If $j \in \mathbb{Z} + 1/2$, $m = 0$ is not in the spectrum, and the sum is identically empty ($\Pi = 0$). $\blacksquare$

---

### Theorem 4 (Multi-Copy Catalan Commutant Inflation)
*Let $\mathcal{C}_M = \text{End}_{SU(2)}(V_1^{\otimes M})$ be the commutant algebra of $SU(2)$-invariant operators acting on $M$ copies of the vector representation $V_1 \cong \mathbb{C}^3$.*
1. *The dimension of the commutant algebra is given by the Catalan numbers:*
   $$\dim(\mathcal{C}_M) = C_M = \frac{1}{M + 1} \binom{2M}{M} = \Theta\left( \frac{4^M}{\sqrt{\pi} M^{3/2}} \right).$$
2. *For $M$ copies of arbitrary spin $j$, the commutant dimension grows exponentially:*
   $$\dim(\text{End}_{SU(2)}(V_j^{\otimes M})) = 2^{\Omega(M \log d_j)}.$$
3. *Diagonalizing the commutant algebra $\mathcal{C}_M$ requires evaluating general Racah recoupling $3nj$-symbols, which is $\#P$-hard in the number of copies $M$.*

#### Proof
Under the adjoint action of $SU(2)$, $V_1 \cong \mathbb{C}^3$ is the fundamental 3-dimensional vector representation of $SO(3)$.
By Schur-Weyl duality for orthogonal groups (the Brauer algebra), the algebra of $SU(2)$-invariant endomorphisms on $V_1^{\otimes M}$ corresponds to pairing and permutation graphs.
Equivalently, the multiplicity of the trivial representation $\mathbf{1}$ in $V_1^{\otimes 2M}$ is the number of Dyck paths of length $2M$, which is the Catalan number:
$$\dim(\mathcal{C}_M) = \text{mult}_{SU(2)}(V_1^{\otimes 2M}, \, \mathbf{1}) = \frac{1}{M + 1} \binom{2M}{M} = C_M.$$
By Stirling's approximation, $C_M \approx \frac{4^M}{\sqrt{\pi} M^{3/2}}$.
For general spin $j$, Clebsch-Gordan series branching rules yield paths in the $A_1$ affine Dynkin diagram, whose path count grows as $(2j + 1)^{M / 2} = d_j^{M/2}$.
By the Aharonov-Jones-Landau theorem (2009), computing matrix elements of unitary transformations diagonalizing tensor networks of $SU(2)$ representations ($6j$ and $9j$ symbols) is $\#P$-hard in general.
Thus, multi-copy entangling measurements over $M$ registers cannot be implemented in polynomial quantum circuit depth. $\blacksquare$

---

## 5. Epistemic Demarcation: Continuous Abelian vs. Continuous Non-Abelian

```
+---------------------------------------------------------------------------------------------------------+
|                  CONTINUOUS LIE GROUP HIDDEN STRUCTURE DICHOTOMY                                        |
+------------------------------------+--------------------------------+-----------------------------------+
| Property                           | Continuous Abelian (R^r / L)   | Continuous Non-Abelian (SU(2))    |
+------------------------------------+--------------------------------+-----------------------------------+
| Irrep Dimension                    | Strictly 1-dimensional         | d_j = 2j + 1 (Unbounded)          |
| Character Orthogonality            | Complete 1D basis over S^1     | Multi-dimensional Wigner D-trace  |
| Weak Fourier Sampling              | Recovers dual lattice L^* (BQP)| TV == 0.000 (Completely Blind)    |
| Commutant Dimension (M copies)     | dim(C_M) == 1 (Abelian)        | Catalan C_M = Theta(4^M / M^{1.5})|
| Entangling Measurement Circuit     | Standard tensor product QFT    | #P-hard Racah Recoupling Gates    |
| STATUS                             | BQP SOLVABLE (Investigations 42,43)| EXPONENTIAL QUANTUM BARRIER     |
+------------------------------------+--------------------------------+-----------------------------------+
```

---

## 6. Negative Result Declaration

```json
{
  "id": "NEG-SU2-COMPACT-LIE-HSP-COMMUTANT-INFLATION",
  "claim": "The Hidden Subgroup Problem over the compact Lie group SU(2) or SO(3) can be solved in polynomial time by standard quantum Fourier sampling.",
  "reason_invalid": "In SU(2), irreducible representations have dimension d_j = 2j + 1, and character traces chi_j(theta) = sin((2j+1)theta) / sin(theta) are strictly class functions. For any subgroup H <= SU(2) (including continuous tori U(1)_n and finite binary polyhedral groups 2T, 2O, 2I), the weak Fourier sampling distribution is identically invariant under ambient rotations g, forcing total variation distance to zero (TV == 0.000, 0.000 bits mutual information). While strong Fourier sampling on integer spins j yields rank-1 spin-coherent projectors |j, n, 0><j, n, 0|, single-copy measurements provide only O(log j) bits of information. Distinguishing orientations requires multi-copy measurements across M registers, where the SU(2) commutant algebra C_M = End_SU(2)(V_1^{otimes M}) explodes exponentially with Catalan dimension dim(C_M) = (1/(M+1)) binom(2M, M) = Theta(4^M / M^{3/2}). Diagonalizing this commutant requires evaluating Racah recoupling symbols, which is #P-hard in general (Aharonov-Jones-Landau 2009).",
  "source": "research/SU2_COMPACT_LIE_HSP_COMMUTANT_INFLATION.md"
}
```

---

## 7. References & Literature Demarcation

1. **Aharonov, D., Jones, V., & Landau, Z. (2009)**. *A polynomial quantum algorithm for approximating the Jones polynomial*. Algorithmica, 55(3), 395–421.
2. **Hallgren, S., Russell, A., & Ta-Shma, A. (2000)**. *Normal subgroup reconstruction and quantum computation using group representations*. In Proceedings of the 32nd Annual ACM STOC, 627–635.
3. **Moore, C., Russell, A., & Schulman, L. J. (2004)**. *The limits of quantum algorithms for hidden subgroup problems on non-abelian groups*. arXiv:quant-ph/0411081.
4. **Wigner, E. P. (1959)**. *Group Theory and Its Application to the Quantum Mechanics of Atomic Spectra*. Academic Press.
5. **Peter, F., & Weyl, H. (1927)**. *Die Vollständigkeit der primitiven Darstellungen einer geschlossenen kontinuierlichen Gruppe*. Mathematische Annalen, 97(1), 737–755.
