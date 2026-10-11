# Nilpotent and Solvable Groups in the Hidden Subgroup Problem: Structural Boundaries, 2-Group Obstructions, and Open Complexities

**Investigation**: Investigation 22 (The Structural Frontier of Non-Abelian HSP)  
**Date**: 2026-10-11  
**Status**: AUDITED & DISPROVED AS UNIVERSAL DICHOTOMY (Corrected with explicit counterexamples and bounds)  
**Core Invariants**: `speedup_claim_allowed = False`, `accepted_speedup_candidate = False`  

---

## 1. Executive Summary & Audit Disproof Notice

> [!CAUTION]
> **Audit Disproof Notice (2026-10-11)**:
> The original claim that *"polynomial-time quantum speedups exist if and only if $G$ is nilpotent"* is **DISPROVED AND FALSE**.
> 
> 1. **Nilpotence is Insufficient (The Nilpotent 2-Group Counterexample)**:
>    Every dihedral group of power-of-two order $D_{2^k} = \mathbb{Z}_{2^k} \rtimes \mathbb{Z}_2$ is a finite $2$-group, and therefore **strictly nilpotent** (with lower central series of length $k$).
>    However, for a hidden reflection $H = \{0, (s, 1)\}$, the intersection with the center is trivial:
>    $$H \cap Z(D_{2^k}) = \{0\}.$$
>    Inductive central quotienting yields zero information about the secret shift $s$ at every stage. Finding $H$ in $D_{2^k}$ is precisely the famous Dihedral Hidden Subgroup Problem, for which no polynomial-time quantum algorithm is known (best known is Kuperberg's subexponential $2^{O(\sqrt{k})}$ sieve).
>    Thus, **nilpotency alone does not guarantee quantum polynomial tractability**. Known polynomial-time algorithms for nilpotent groups (e.g. Hallgren-Russell-Ta-Shma 2000, Ivanyos-Sanselme-Santha 2007) strictly require bounded nilpotency class ($c = O(1)$) and bounded prime factors.
>
> 2. **Nilpotence is Not Necessary (The Constant-Exponent Solvable Counterexample)**:
>    **Friedl, Ivanyos, Magniez, Santha, and Sen (STOC 2003 / SICOMP 2014)** established an explicit **polynomial-time quantum algorithm** for non-nilpotent solvable groups of constant exponent and constant derived length (e.g. $\mathbb{F}_p^n \rtimes H$ with $p = O(1)$), even with trivial center $Z(G) = \{1\}$.
>
> 3. **Upper Bound vs. Lower Bound Confusion**:
>    Kuperberg's sieve provides a $2^{O(\sqrt{\log N})}$ **algorithm upper bound**, but does **not** constitute a proven universal lower bound for all quantum algorithms.
>
> **Status**: The universal "iff" dichotomy is **RETRACTED**. Below is the corrected, rigorous structural boundary.

---

## 2. The Structural Landscape of Non-Abelian HSP

The true complexity of the Hidden Subgroup Problem does not track the coarse abelian / nilpotent / solvable division, but depends critically on **three algebraic parameters**:
1. **Nilpotency Class & Center Intersection**: Does the hidden subgroup intersect the center non-trivially ($H \cap Z(G) \ne \{1\}$), and is the nilpotency class bounded ($c = O(1)$)?
2. **Group Exponent**: Is the exponent of the group constant ($\text{exp}(G) = O(1)$) or growing ($N = 2^n$)?
3. **Subgroup Promise**: Is the hidden subgroup promised to be normal, an involution, a maximal parabolic, or a general subgroup?

### Exact Comparative Analysis of Group Classes

| Group Family | Algebraic Type | Center & Derived Structure | Exponent | Quantum HSP Complexity | Primary References |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Abelian Groups** | Abelian | $Z(G) = G$ | Arbitrary | **$\text{poly}(\log \|G\|)$** (BQP) | Shor (1994) |
| **Heisenberg Groups** $H_{2n+1}(\mathbb{F}_p)$ | Nilpotent (class 2) | $Z(G) \cong \mathbb{F}_p$ | $p$ | **$\text{poly}(n, \log p)$** (BQP) | Hallgren, Russell, Ta-Shma (2000) |
| **Nilpotent Groups (Bounded Class $c$)** | Nilpotent | Central tower, $c = O(1)$ | Bounded primes | **$\text{poly}(\log \|G\|)$** (BQP) | Ivanyos, Sanselme, Santha (2007) |
| **Dihedral 2-Groups** $D_{2^k}$ | **Nilpotent** (class $k-1$) | $Z(G) \cong \mathbb{Z}_2$, $H \cap Z = \{0\}$ | $2^k$ (Growing) | **$2^{O(\sqrt{k})}$** (Open in BQP) | Kuperberg (2005), Regev (2008) |
| **Affine Groups** $\mathbb{F}_p^n \rtimes H$ | **Non-Nilpotent** (Solvable) | $Z(G) = \{1\}$ | $p = O(1)$ (Constant) | **$\text{poly}(n)$** (BQP) | Friedl, Ivanyos, Magniez, Santha, Sen (2003) |
| **Dihedral Groups** $D_N$ ($N$ odd) | **Non-Nilpotent** (Solvable) | $Z(G) = \{1\}$ | $N$ (Growing) | **$2^{O(\sqrt{\log N})}$** (Open in BQP) | Kuperberg (2005) |
| **Symmetric Groups** $S_n$ | Non-Solvable | $Z(G) = \{1\}$ | $n!$ | **Open** ($2^{O(n \log n)}$) | Hallgren et al. (2006), Moore et al. (2007) |

---

## 3. Rigorous Analysis of the 2-Group Obstruction

### Theorem 1 (Failure of Central Induction on Dihedral 2-Groups):
Let $G = D_{2^k} = \mathbb{Z}_{2^k} \rtimes \mathbb{Z}_2$ be the dihedral group of order $2^{k+1}$.
1. $G$ is nilpotent of class $k$. The lower central series is $G_1 = G$, $G_2 = 2 \mathbb{Z}_{2^k}$, $G_3 = 4 \mathbb{Z}_{2^k}$, ..., $G_k = 2^{k-1} \mathbb{Z}_{2^k} = Z(G)$, $G_{k+1} = \{0\}$.
2. Let $H = \{0, (s, 1)\}$ be a hidden reflection subgroup of order 2.
3. Because $(s, 1) \notin \mathbb{Z}_{2^k}$, $(s, 1)$ cannot belong to any term $G_j$ of the lower central series for $j \ge 2$.
4. In particular:
   $$H \cap Z(G) = \{0\}.$$
5. Any quantum algorithm that restricts queries to the center $Z(G)$ observes only the trivial intersection $H \cap Z(G) = \{0\}$.
6. The quotient group $G / Z(G)$ is isomorphic to $D_{2^{k-1}}$, and the projected subgroup is $\overline{H} \cong \mathbb{Z}_2$.
7. Inductive quotienting down the entire central series yields zero information about the secret shift $s \pmod{2^k}$.
8. Reconstructing $s$ requires distinguishing coset states across the reflection branches, reducing strictly to the Kuperberg dihedral sieve.

*Conclusion*: Nilpotency is **neither necessary nor sufficient** for polynomial-time quantum algorithms in the Hidden Subgroup Problem.
