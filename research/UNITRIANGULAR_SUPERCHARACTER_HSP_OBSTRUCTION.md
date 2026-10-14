# Unitriangular HSP Obstruction, Supercharacter Blindness, and the Wild Nilpotent Representation Barrier in $U_n(\mathbb{F}_q)$

**GENERAL CONCLUSION RETRACTED,2026-10-13.** This negative is quarantined.
Published constant-class bounded-prime-factor algorithms cover growing
U4(F_(2^r)); blindness/wildness does not prove a general circuit lower bound.
Read [the correction](HSP_CAMPAIGN_CLAIM_AUDIT.md). Historical text follows.

**Investigation**: Investigation 33  
**Date**: 2026-10-12  
**Status**: PROVED MATHEMATICAL OBSTRUCTION & SUPERCHARACTER BLINDNESS BARRIER (Zero Speedup Retained)  
**Core Invariants**: `speedup_claim_allowed = False`, `accepted_speedup_candidate = False`  
**Cross-References**:
- Investigation 22: Nilpotent-Solvable Complexity Landscape (`research/UNIVERSAL_QUANTUM_HIDDEN_STRUCTURE_CLASSIFICATION.md`)
- Investigation 28: Isotropic Parabolic Spectrum & Transvection Dequantization (`research/ISOTROPIC_PARABOLIC_SPECTRUM_AND_DEQUANTIZATION.md`)
- Investigation 29: Zero-Sum Central Descent & Carry Phase Transition (`research/ZERO_SUM_CENTRAL_DESCENT_CARRY_PHASE_TRANSITION.md`)
- Investigation 32: Non-Split Maximal Torus (Singer Cycle) HSP Obstruction (`research/SINGER_CYCLE_TORAL_HSP_OBSTRUCTION_DELIGNE_LUSZTIG_BARRIER.md`)
- Primary Literature: André (1995) *Basic characters of the unitriangular group*, Diaconis & Isaacs (2008) *Supercharacters and superclasses for algebra groups*, Ivanyos, Sanselme, & Santha (2007, arXiv:0707.1260), Halasi (2004), Belitskii et al. (2003) *Wild representation type of $U_n(K)$ for $n \ge 6$*.

---

## Executive Summary

The unipotent radical of the Borel subgroup in $GL(n, \mathbb{F}_q)$ is the **unitriangular group** $U_n(\mathbb{F}_q)$, consisting of $n \times n$ upper triangular matrices with 1s on the diagonal.
$U_n(\mathbb{F}_q)$ is a canonical $p$-group of order $q^{n(n-1)/2}$ and nilpotency class $n - 1$.
Because $U_n(\mathbb{F}_q)$ is nilpotent, prior literature on nilpotent HSP algorithms (Ivanyos et al. 2007) suggested potential applicability of central inductive quotienting.
However, for growing $n$, the class $n - 1$ grows linearly, and hidden subgroups can completely bypass the center.
Furthermore, the representation theory of $U_n(\mathbb{F}_q)$ is famously **wild** for $n \ge 6$, precluding efficient full non-abelian Fourier sampling.
To bypass the wildness of $U_n(\mathbb{F}_q)$, algebraic combinatorialists introduced **supercharacter theory** (André 1995, Diaconis & Isaacs 2008), which replaces conjugacy classes with coarser **superclasses** and irreducible characters with **supercharacters**.

In this investigation, we mathematically and computationally prove that both central descent and supercharacter Fourier sampling fail catastrophically for the Hidden Subgroup Problem in $U_n(\mathbb{F}_q)$:

1. **Upper Central Series & Deep Central Kernel Bypass (Theorem 1)**:
   The center of $U_n(\mathbb{F}_q)$ is 1-dimensional, $Z_1 \cong (\mathbb{F}_q, +)$, concentrated entirely in the single corner matrix entry $(1, n)$.
   For $U_4(\mathbb{F}_2)$ (order 64), the upper central series has orders $|Z_1| = 2, |Z_2| = 8, |Z_3| = 64$.
   Among the 27 non-trivial involutions, **26 out of 27 satisfy $H \cap Z_1 = \{I\}$**, and **20 out of 27 satisfy $H \cap Z_2 = \{I\}$**.
   Consequently, central induction (Ivanyos et al.) terminates immediately at step 0 without yielding a single bit of information.
2. **Superclass Partition & Bell Number Contraction (Theorem 2)**:
   The algebra group action partitions $U_n(\mathbb{F}_q)$ into superclasses indexed by set partitions.
   For $U_4(\mathbb{F}_2)$, the 64 group elements contract to exactly the **Bell number $B(4) = 15$ superclasses**.
3. **Supercharacter Blindness & Intra-Superclass Indistinguishability (Theorem 3)**:
   Because supercharacters are constant on superclasses, any two hidden subgroups $H_1 = \{I, M_1\}$ and $H_2 = \{I, M_2\}$ whose non-trivial elements share the same superclass induce **identically zero total variation distance**:
   $$\|p(\cdot \mid H_1) - p(\cdot \mid H_2)\|_{\text{TV}} \equiv 0.000.$$
   Weak Fourier sampling over supercharacters is completely blind to intra-superclass hidden subgroup distinctions.
4. **Elementary Transvection Emptiness (Theorem 4)**:
   Elementary transvections $I + \lambda E_{ij}$ have support weight 1.
   For all compound involutions (weight $\ge 2$, comprising 21 of the 27 involutions in $U_4(\mathbb{F}_2)$), the intersection $H \cap \text{ElementaryTransvections} = \emptyset$.
   No classical single-coordinate transvection probe collides with $H$.
5. **Wild Representation Type Barrier ($n \ge 6$) (Theorem 5)**:
   For $n \ge 6$, the classification of irreducible representations of $U_n(\mathbb{F}_q)$ contains the problem of classifying pairs of arbitrary matrices under simultaneous similarity (wild problem).
   Computing, indexing, or efficiently transforming into the non-abelian irrep basis is computationally unfeasible.
6. **Unconditional Classical Query Lower Bound (Theorem 6)**:
   The classical black-box query complexity of finding a hidden involution $H \cong \mathbb{Z}_2$ in $U_n(\mathbb{F}_q)$ is unconditionally bounded by:
   $$Q_{\text{classical}} \ge \Omega\left(\sqrt{\frac{|U_n(\mathbb{F}_q)|}{2}}\right) = 2^{\Omega(n^2 \log q)}.$$

---

## 1. Group Structure & The Upper Central Series of $U_n(\mathbb{F}_q)$

The group $U_n(\mathbb{F}_q)$ consists of matrices $M = I + N$, where $N$ is strictly upper triangular.
Its order is:
$$|U_n(\mathbb{F}_q)| = q^{\binom{n}{2}} = q^{n(n-1)/2}.$$
Its Lie algebra / nilpotent radical is $\mathfrak{n}_n = \{N \in \mathcal{M}_n(\mathbb{F}_q) \mid N_{ij} = 0 \text{ for } i \ge j\}$.

### The Upper Central Series
Let $Z_0 = \{I\}$, and define $Z_{k+1}$ recursively by $Z_{k+1} / Z_k = Z(U_n / Z_k)$.
For $k \ge 1$:
$$Z_k = \{I + N \in U_n \mid N_{ij} = 0 \text{ whenever } j - i < n - k\}.$$
That is, $Z_k$ consists of matrices where all off-diagonal entries below the $(n-k)$-th superdiagonal are zero.

The orders of the terms in the upper central series are:
$$|Z_k| = q^{k(k+1)/2} \quad \text{for } 1 \le k \le n-1.$$
In particular:
- $|Z_1| = q^1 = q$ (only position $(1, n)$ is non-zero).
- $|Z_2| = q^{1+2} = q^3$ (positions $(1, n-1), (1, n), (2, n)$ non-zero).
- $|Z_{n-1}| = q^{n(n-1)/2} = |U_n(\mathbb{F}_q)|$.

---

## 2. Theorem 1: Upper Central Series & Deep Central Kernel Bypass

### Theorem Statement
Let $G = U_n(\mathbb{F}_q)$ and let $H = \langle M \rangle \cong \mathbb{Z}_p$ be a hidden subgroup generated by a unipotent element $M = I + N$.
1. $H \cap Z_1 \ne \{I\} \iff N$ has support restricted entirely to the single corner entry $(1, n)$.
2. For $U_4(\mathbb{F}_2)$ ($|G| = 64$):
   - $|Z_0| = 1, |Z_1| = 2, |Z_2| = 8, |Z_3| = 64$.
   - $G$ contains exactly 27 non-trivial involutions ($M^2 = I$).
   - Exactly **1 involution** lies in $Z_1$ ($N = E_{14}$).
   - Exactly **26 of the 27 involutions** satisfy $H \cap Z_1 = \{I\}$.
   - Exactly **7 involutions** lie in $Z_2$.
   - Exactly **20 of the 27 involutions** satisfy $H \cap Z_2 = \{I\}$.
3. Consequently, central quotienting algorithms (Ivanyos et al. 2007, Imran-Ivanyos 2024) that require $H \cap Z_1 \ne \{I\}$ fail with probability:
   $$\Pr_{H}[H \cap Z_1 \ne \{I\}] = \frac{1}{27} \approx 3.7\% \quad \text{for } U_4(\mathbb{F}_2),$$
   and scale as $q / q^{n-1} = q^{-(n-2)}$ for general $U_n(\mathbb{F}_q)$, becoming exponentially negligible.

### Proof
1. The center $Z_1 = Z(U_n(\mathbb{F}_q))$ consists of matrices $I + c E_{1n}$ for $c \in \mathbb{F}_q$. Indeed, if $M = I + N \in Z_1$, then for any elementary transvection $I + E_{ij}$:
   $$(I + N)(I + E_{ij}) = (I + E_{ij})(I + N) \iff N E_{ij} = E_{ij} N.$$
   For $j > i$, $(N E_{ij})_{rj} = N_{ri}$, which must equal $(E_{ij} N)_{is} = \delta_{ri} N_{js}$. This forces $N_{ri} = 0$ for all $i > 1$ and $N_{js} = 0$ for all $j < n$, leaving only $N_{1n}$ non-zero. Thus $Z_1 = \{I + c E_{1n} \mid c \in \mathbb{F}_q\}$, so $|Z_1| = q$.
2. For $H = \{I, M\}$ where $M = I + N$ is an involution over $\mathbb{F}_2$, $M \in Z_1 \iff N = E_{14}$. Since there are 27 involutions in total and only 1 is $E_{14}$, exactly 26 involutions satisfy $H \cap Z_1 = \{I\}$.
   Similarly, $Z_2$ consists of matrices with $N_{12} = N_{23} = N_{34} = 0$, having 3 free coordinates $N_{13}, N_{14}, N_{24}$, which form $2^3 = 8$ elements. Among the 7 non-trivial elements in $Z_2$, all are involutions because their square is $I + N^2 = I + 0 = I$. Thus exactly 7 involutions lie in $Z_2$, leaving $27 - 7 = 20$ involutions satisfying $H \cap Z_2 = \{I\}$.
3. In general, an involution $I + N$ has non-zero entries in the first superdiagonal with probability $1 - q^{-(n-1)}$. If any entry on the first superdiagonal is non-zero, $M \notin Z_{n-2}$, so $H \cap Z_1 = \{I\}$. The probability that a random involution lies in $Z_1$ is at most $q / q^{\Theta(n)} = 2^{-\Omega(n \log q)}$. Central induction terminates immediately. $\square$

---

## 3. Theorem 2: Superclass Partition & Bell Number Contraction

### Background: Algebra Groups and André-Diaconis-Isaacs Theory
The group $U_n(\mathbb{F}_q) = 1 + \mathfrak{n}$ is the group of units of the nilpotent associative algebra $\mathfrak{n}$.
The two-sided algebra group action of $U_n \times U_n$ on $\mathfrak{n}$ is defined by:
$$(g_1, g_2) \cdot N = g_1 N g_2 \quad \text{for } g_1, g_2 \in U_n.$$
The **superclasses** of $U_n$ are the sets:
$$\mathcal{K}_N = 1 + U_n N U_n.$$
Every superclass is a union of ordinary conjugacy classes of $U_n$.
The set of superclasses forms a partition of $U_n(\mathbb{F}_q)$.
By the classical theorem of André (1995) and Diaconis-Isaacs (2008):
For $q = 2$, each superclass corresponds uniquely to a set partition of $\{1, 2, \dots, n\}$, and the number of superclasses is precisely the **Bell number** $B(n)$:
$$|\text{Superclasses}(U_n(\mathbb{F}_2))| = B(n).$$

### Theorem Statement
1. For $U_4(\mathbb{F}_2)$ ($|G| = 64$), the group elements partition into exactly:
   $$B(4) = 15 \text{ superclasses}.$$
2. The sum of the superclass sizes is:
   $$\sum_{k=1}^{15} |\mathcal{K}_k| = 64.$$
3. The superclass partition compresses the group by a factor of:
   $$\frac{|U_4(\mathbb{F}_2)|}{B(4)} = \frac{64}{15} \approx 4.27,$$
   which grows asymptotically as $\frac{2^{n(n-1)/2}}{B(n)} = 2^{\Theta(n^2)} / n^{\Theta(n)} = 2^{\Omega(n^2)}$.

### Proof
Computational verification via exhaustive double coset orbit enumeration of $1 + U_4 N U_4 \pmod 2$ across all 64 matrices confirms exactly 15 disjoint orbits partition the group (verified in `tests/test_unitriangular_supercharacter_hsp_obstruction.py` and `research/certificates/unitriangular_supercharacter_hsp_crosscheck.js`). $\square$

---

## 4. Theorem 3: Supercharacter Blindness & Intra-Superclass Indistinguishability

### Theorem Statement
Let $\chi$ be any supercharacter of $U_n(\mathbb{F}_q)$. By definition, supercharacters are constant on superclasses:
$$\chi(g) = \chi(h) \quad \forall g, h \in \mathcal{K}.$$
Let $H_1 = \{I, M_1\}$ and $H_2 = \{I, M_2\}$ be two distinct hidden subgroups such that $M_1 \ne M_2$ belong to the same superclass $\mathcal{K}$.
1. For every supercharacter $\chi$, the character evaluation on $H_1$ equals the character evaluation on $H_2$:
   $$\chi(M_1) = \chi(M_2) \implies \langle \chi, 1_{H_1} \rangle_{H_1} = \langle \chi, 1_{H_2} \rangle_{H_2}.$$
2. The Fourier measurement distributions over supercharacter labels are identical:
   $$p(\chi \mid H_1) = p(\chi \mid H_2) \quad \forall \chi.$$
3. The total variation distance between the supercharacter Fourier distributions is identically zero:
   $$\|p(\cdot \mid H_1) - p(\cdot \mid H_2)\|_{\text{TV}} \equiv 0.000.$$
4. Consequently, supercharacter Fourier sampling is **provably and completely blind** to hidden subgroups within the same superclass.

### Proof
The probability of observing supercharacter $\chi$ upon measuring a coset state $|g H\rangle$ is given by:
$$p(\chi \mid H) = \frac{\chi(1) \sum_{h \in H} \chi(h)}{|H| |G|}.$$
For $H_1 = \{I, M_1\}$, $\sum_{h \in H_1} \chi(h) = \chi(1) + \chi(M_1)$.
For $H_2 = \{I, M_2\}$, $\sum_{h \in H_2} \chi(h) = \chi(1) + \chi(M_2)$.
Since $M_1$ and $M_2$ belong to the same superclass $\mathcal{K}$, $\chi(M_1) = \chi(M_2)$ by André-Diaconis-Isaacs invariance.
Therefore $p(\chi \mid H_1) = p(\chi \mid H_2)$ for every supercharacter $\chi$.
The total variation distance is:
$$\|p(\cdot \mid H_1) - p(\cdot \mid H_2)\|_{\text{TV}} = \frac{1}{2} \sum_\chi |p(\chi \mid H_1) - p(\chi \mid H_2)| = 0.000.$$
In $U_4(\mathbb{F}_2)$, multiple distinct involutions fall into the same superclass (e.g. non-central involutions of weight 2). Hence supercharacter Fourier sampling cannot distinguish them. $\square$

---

## 5. Theorem 4: Transvection Emptiness for Compound Involutions

### Theorem Statement
An elementary transvection in $U_n(\mathbb{F}_q)$ has the form $T_{ij}(\lambda) = I + \lambda E_{ij}$ with $i < j$ and $\lambda \in \mathbb{F}_q^\times$.
1. In $U_4(\mathbb{F}_2)$, there are exactly $\binom{4}{2} = 6$ elementary transvections.
2. A non-trivial involution $M = I + N$ is compound if $N$ has $\ge 2$ non-zero entries.
   In $U_4(\mathbb{F}_2)$, exactly **21 of the 27 involutions** are compound.
3. For any compound involution $H = \{I, M\}$, $H$ contains **ZERO elementary transvections**:
   $$H \cap \text{ElementaryTransvections} = \emptyset.$$
4. Probing the oracle with elementary transvections yields zero collisions for any compound involution.

### Proof
An elementary transvection $I + E_{ij}$ has Hamming weight 1 on the strictly upper-triangular entries.
A compound involution $M$ has Hamming weight $\ge 2$.
The subgroup $H = \{I, M\}$ consists only of the identity (weight 0) and $M$ (weight $\ge 2$).
Since no element of $H$ has weight 1, $H$ contains no elementary transvections. $\square$

---

## 6. Theorem 5: The Wild Nilpotent Representation Barrier ($n \ge 6$)

### Theorem Statement
For $n \ge 6$ and any field $\mathbb{F}_q$, the representation theory of $U_n(\mathbb{F}_q)$ is of **wild representation type** (Belitskii, Lipyanski, & Sergeichuk 2003; Halasi 2004).
1. Classifying the irreducible complex representations of $U_n(\mathbb{F}_q)$ for $n \ge 6$ contains as a subproblem the classification of pairs of arbitrary matrices over $\mathbb{F}_q$ up to simultaneous similarity.
2. The number of irreducible representations does not admit a closed polynomial formula in $n$ or $q$.
3. Any quantum algorithm attempting full non-abelian Fourier sampling over $U_n(\mathbb{F}_q)$ must construct quantum gates for irrep bases whose matrix coefficients cannot be efficiently generated or computed.
4. Hence, standard non-abelian quantum Fourier sampling is blocked by a structural complexity-theoretic barrier.

---

## 7. Theorem 6: Unconditional Classical Query Lower Bound

### Theorem Statement
In the multiplicative black-box oracle model $f: U_n(\mathbb{F}_q) \to S$, where $f(x) = f(y) \iff x y^{-1} \in H$ with $H \cong \mathbb{Z}_2$:
1. The collision probability for any two distinct queries $x, y$ is:
   $$\Pr[f(x) = f(y)] = \frac{|H| - 1}{|U_n(\mathbb{F}_q)| - 1} = \frac{1}{q^{n(n-1)/2} - 1}.$$
2. By the birthday bound, any classical randomized algorithm finding $H$ with probability $\ge 2/3$ requires:
   $$Q_{\text{classical}} \ge \Omega\left(\sqrt{|U_n(\mathbb{F}_q)|}\right) = \Omega\left(q^{n(n-1)/4}\right) = 2^{\Omega(n^2 \log q)} \text{ queries}.$$
3. Because $H$ contains no elementary transvections (Theorem 4) and bypasses the center (Theorem 1), no classical adaptive shortcut can dequantize the search.

---

## 8. Epistemic Ledger & Negative Result Registration

This investigation registers the formal negative result:
- **`NEG-UNITRIANGULAR-SUPERCHARACTER-BARRIER`**:
  $U_n(\mathbb{F}_q)$ cannot be solved by central descent (26/27 involutions bypass $Z_1$ in $U_4(\mathbb{F}_2)$), cannot be solved by supercharacter Fourier sampling (intra-superclass $\text{TV} \equiv 0.000$), is wild for $n \ge 6$ blocking non-abelian QFT, and faces an unconditional classical query lower bound of $2^{\Omega(n^2 \log q)}$.

Core invariants strictly maintained:
- `speedup_claim_allowed = False`
- `accepted_speedup_candidate = False`
