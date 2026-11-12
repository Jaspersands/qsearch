# Global GRH two-Selmer composition: retained primary-source packet
Prepared 2026-11-12T14:29:36.871400+00:00. Selected theorem/algorithm text only; no abstract used as evidence. No API/network/Git call.
Scope: arbitrary number-field factors of the branch algebra, with conditional GRH class generators; no odd-degree/Galois or totally-real premise imported.
BS source: https://arxiv.org/pdf/2510.02280v2 (corrected v2, 24 Nov 2025).
BS PDF: research/literature_cache/arxiv_2510_02280v2.pdf; SHA256 037f365f75cd9c8d00870fe20ca3d04a78c2b23831cf91e5b53d7d6c31d58a4a.
BS text: research/literature_cache/arxiv_2510_02280v2.txt; SHA256 98b13eb752fe7fb68e2e4228ffe3e89b39a444d3c5a3fa5bf210e4d0e5194c28; generated locally with /opt/anaconda3/envs/qsearch-cas/bin/pdftotext -layout.
IB source: https://weimann.users.lmno.cnrs.fr/integral_bases.pdf (Poteaux--Weimann, Fast Integral Bases Computation).
IB PDF: research/audits/sources/local_kummer_cluster/integral_bases.pdf; SHA256 dc0f37af3eed8841cf9afb35f40a0a191957d7d699f53cc5e5ae76d43127513e.
IB text: research/audits/sources/local_kummer_cluster/integral_bases.txt; SHA256 780b5f6d1c1a3664bd87df94d837dbb5832d5e9596012b3c0b4fbe352ca1ce1f.
Line locations below are LF-delimited physical text lines matching rg -n. Form-feed/control characters are stripped. IB control-coded fi/ff/fl/ffi ligatures and ε are mapped to readable glyphs. Other PDF line-breaking/superscript artifacts remain visible; consult the retained PDF for typesetting.

Audit obligations and transcription cautions (editorial, not additional source claims):
- BS Theorem1 is the arbitrary-degree compact S-unit theorem; its stated parameters are n, log|Delta|, |S| and max log Norm(p). Theorem5 is the imported HSP theorem, NOT a standalone exact S-unit basis theorem. Its PDF-checked condition is r<=lambda/36, and its failure bound is mu with logarithmic dependence log(1/mu). Carry that failure through exact recovery and all field factors explicitly.
- Definition8 means alpha=gamma_0*gamma_1^l*...*gamma_k^(l^k), with exact polynomial-size atoms and polynomial k; choose l=2. Section8.1 also charges an LLL-reduced integral basis, phases/logarithms, exact valuations and denominator treatment for fractional S-units. Expanded gigantic products are not an input/output shortcut.
- General factors can have roots of unity beyond +/-1. The paper states U(S)=mu(K) times its free part and displays this again in Algorithm6, but the selected passages do NOT give an explicit separate polynomial-bit torsion-generator extraction algorithm. The audit must pay it and include torsion per factor; free-logarithmic generators alone are insufficient modulo squares.
- Algorithm5's printed output says O is a finite abelian group; the preceding paragraph and Proposition8 identify the intended output as Cl(O). Its displayed r+|S| generator list omits torsion notation (irrelevant to valuations but not to full S-unit squareclasses). Preserve rather than silently promote this shorthand.
- Section8.2 supplies GRH prime ideals of norm<=48*(log|Delta|)^2 and explicitly says their number is polynomial. Pay enumeration/ideal representations and maximal orders, all primes over the native bad-prime set, and norm/sign/local maps. Treat Q separately when Delta=1.
- IB is the NUMBER-FIELD-capable source below. The identically named surface_module_2026/integral_bases is a different Abelard FUNCTION-FIELD paper, not this theorem. IB Theorem1 requires squarefree factorization of the index or discriminant; its Z bound is in word operations in the stated Boolean RAM model. Charge native polynomial coefficient bits and factorization explicitly; the packet does not infer a stronger bit bound by omitting them.

## Biasse--Song selected body text
```text
[BS physical lines 98-108: Theorem1 and compact output context]
L98: compact representations of the desired field elements with respect to a given integral basis
L99: for O, while [15] only returns fixed point rational approximations of the units. Compact
L100: representations are usually easier for further algebraic processing. Our main results are
L101: summarized in the next theorem.
L102: 
L103: Theorem 1 (S-unit group computation). There is a quantum algorithm for computing
L104: the S-unit group of a number field K in compact representation which runs in polynomial
L105: time in the parameters n = deg(K), log(|∆|), |S| and maxp∈S {log(N (p))}, where ∆ is the
L106: discriminant of the ring of integers of K.
L107: 
L108: Corollary 1. There are quantum polynomial time algorithms for the resolution of the fol-
[BS physical lines 212-224: Order basis and size input convention]
L212: Number fields A number field K is a finite extension of Q. Its ring of integers OK has
L213: the structure of a Z-lattice of degree n = [K : Q], and the orders O ⊆ OK are the sublattices
L214: of OK which have degree n and which are equipped with a ring structure. Throughout this
L215: paper, we assume that O is an order in a number field K, and we denote by ω1 , . . . , ωn a
L216: Z-basis, that is O = Zω1 ⊕ . . . ⊕ Zωn . A number field has n1 real embeddings and n2 pairs
L217: of complex embeddings which we denote (σj : K → R)j≤n1 , ((σj , σj ) : K → C)j≤n2 with
L218: n1 + n2 = n = deg(K). These embeddings    P define two essential maps,
L219:                                                                      Q namely the norm and
L220: trace maps which are given by T (x) := σ σ(x) ∈ Q and N (x) := σ σ(x) ∈ Q. The trace
L221: map is additive while the norm map is multiplicative. Note that T (O) ⊆ Z and N (O) ⊆ Z.
L222: We measure the size of the ring O by log |∆| where ∆ := (det(σj (ωk )))2 is its discriminant,
L223: and it equals the volume of the fundamental domain of O. Equivalently, the discriminant
L224: can be defined from the trace map by ∆ := det(T (ωi ωj ))i,j≤n .
[BS physical lines 242-255: S-unit group, roots of unity]
L242: 
L243: 
L244:                                               5
L245: The S-unit group The S-units are a generalization of the units O∗ , which are the
L246: invertible elements of O. The unit group can alternatively be defined as the α ∈ O with
L247: |N (α)| = 1, or the α ∈ O such that (α) = O. The unit group O∗ satisfies O∗ ≃ µ ×
L248: ⟨ε1 ⟩ × . . . × ⟨εr ⟩, where r := n1 + n2 − 1, µ is the set of roots of unity and the εi are
L249: torsion-free units. Let S = {pi } be a finite set of prime ideals of O, the S-units are the
L250:                                                                           v (α)     v   (α)
L251: elements α ∈ K such that there is (vi (α))i≤|S| ∈ Z|S| with (α) = p11 · · · p|S|      |S|
L252:                                                                                            . Note
L253: that the S-units are elements of K. They form a multiplicative group U (S) satisfying
L254: U (S) ≃ µ × ⟨ε1 ⟩ × . . . × ⟨εr+|S| ⟩, where r := n1 + n2 − 1, µ is the set of roots of unity and
L255: the εi are torsion-free S-units.
[BS physical lines 1525-1535: Torsion versus free quotient in the proof]
L1525: µ(K) be the group of torsion units, and LS ⊆ Rn1 +n2 −1 ×Zs be the rank-n1 +n2 +s−1-lattice
L1526: that is the projection of US . Then we have the exact sequence
L1527: 
L1528:                0 → (Zn1 × (R/Z)n2 )/µ(K) → G/US → (Rn1 +n2 −1 × Zs )/LS .
L1529: 
L1530: Hence Vol(G/US ) = Vol ((Zn1 × (R/Z)n2 )/µ(K)) Vol (Rn1 +n2 −1 × Zs )/LS
L1531:                                                                                
L1532: 
L1533:    The volume of (Rn1 +n2 −1 × Zs )/LS is equal to the absolute value of determinant of the
L1534: matrix of a basis of LS . Let (αj )j≤r+|S| be a minimal generating set for US /µ(K). Its matrix
L1535: M with respect to the embedding in Rr × Z |S| is related to the matrix M ′ := (Log(αj )) by
[BS physical lines 1576-1594: Actual Theorem5: HSP failure and output]
L1576: Theorem 5 (Theorem 6.2 [16]). Let f be an HSP instance with parameters ((a, r, ε), λ, d)
L1577: such that r ≤ 36 1
L1578:                    λ and ε ≤ 1/2. Let 0 < η ≤ λ1 (L∗ ) and 0 < µ < 1 be a precision
L1579: parameter and error parameter respectively. There is a quantum algorithm that makes K =
L1580: O (log d + log(1/µ) + m log a) oracle calls to f and generates K vectors ũ(1) , . . . ũ(s) ∈ Rm
L1581: having the following properties except with error probability at most µ:
L1582: 
L1583:   1.   ∥ũ(i) ∥ ≤ 3a
L1584:                   π for i = 1, . . . , K;
L1585: 
L1586:   2.   For each i, ∥ũ(i) − u(i) ∥ ≤ η for some u(i) ∈ L∗ ;
L1587: 
L1588:   3.   u(1) , . . . , u(K) generate L∗ .
L1589: 
L1590:                                                         26
L1591:                                             2 
L1592: The quantum circuit uses O Km log aK               quantum gates on O m log aK
L1593:                                                                                
L1594:                                   ηµ                                        ηµ qubits.
[BS physical lines 1647-1706: Definition8 and Section8.1 exact compact recovery]
L1647: 8     Applications to other number theory problems
L1648: 8.1    Recover an exact representation of the S-units
L1649: The solution of HSP is given to us as approximations of generators of the hidden subgroup.
L1650: For many applications, an exact (and polynomially bounded) representation is preferable.
L1651: Therefore, we process the solutions to the S-units problem classically to produce a compact
L1652: representation of the generators of the S-unit group.
L1653: 
L1654: Definition 8 (Compact representation). Let l > 0 be a constant, a compact representation
L1655: of α ∈ O with respect to the integral basis (ωj )j≤n of O is a set of exact representations of
L1656:                                                                     k
L1657: polynomial size algebraic numbers γj satisfying α = γ0 γ1l · · · γkl , where k is polynomial in
L1658: the size of the input.
L1659: 
L1660:     Biasse and Fieker [4, Sec. 5] described an efficient method based on [18, Alg. 7.53] to
L1661: classically compute a compact representation of an algebraic number in polynomial time.
L1662: These methods rely on the knowledge of an exact representation of the algebraic number
L1663: we wish to represent (which is not the case here). A modification of [18, Alg. 7.53] using
L1664: the approximation of the vector corresponding to an algebraic number yields a compact
L1665: representation of that number.
L1666:     Our algorithm for the compact representation of an S-unit takes as input l > 0 and a
L1667: rational approximation (to an arbitrary polynomial precision q) of a vector of the form
L1668: 
L1669:                        (log(|α|1 , · · · , log(|α|n1 +n2 ), θ, vp1 (α), · · · , vp|S| (α)),
L1670: 
L1671:                                           Q vp (α)
L1672: where α is an S-unit. We can assume that j pj j       ⊆ O. If not, we replace each log(|α|j )
L1673: by                                                  
L1674:                             X
L1675:                                 |vpk (α)|ek log(pk ) + log(|α|j )
L1676:                                 vpk (α)<0
L1677: 
L1678:                                                                                   |vp (α)|ek
L1679: (where N (pk ) = pekk ), thus calculating a compact representation of α vp (α)<0 pk k
L1680:                                                                         Q
L1681:                                                                                              .
L1682:                                                                             k
L1683: From that, we can easily derive a compact representation of α. Then, we choose k0 minimal
L1684:           log(|α|                                  Q ⌊vp (α)/lk ⌋
L1685: such that lk0 j ≤ log(|∆|), initiate an ideal I to j pj j         , and we compute rational
L1686:                                     k
L1687: approximations vj of (|α|j )1/l . Then at each step, I is replaced by I l and we compute
L1688: an LLL-reduced element δk of the ideal C ⊆ O such that I −1 = d1k C for the scaled T2
L1689:                             v2              pQ
L1690: norm T2,(vj )j (δ) := |δ|2i vj2 where v := n
L1691:                      P
L1692:                                                  vj . The ideal I is then replaced by βk I where
L1693:       δk
L1694: βk := dk , and vj ← vj · |βk |j . At every step k from k0 to 0, we know that
L1695: 
L1696:     • βk has polynomial size,
L1697:          k             1
L1698:     • βkl 0 · · · βk (α) lk0 −k has polynomial size,
L1699: 
L1700:     • I ⊆ O and has polynomial size (i.e. log(I) is polynomial),
L1701: 
L1702:     • j vj ≥ N (I) ≥ 1.
L1703:       Q
L1704: 
L1705: 
L1706: 
[BS physical lines 1731-1736: Algorithm4 exact input/output]
L1731:     Q Rational       approximations of log(|α|j ), phase vector of α and vj ≥ 0 such that (α) =
L1732:          vj
L1733:        p
L1734:       j j   , l > 0, and approximations ω   cj of an LLL-reduced integral basis of O.
L1735:                                                                    Q k
L1736: Output: Exact representation of γ0 , · · · , γk0 such that α = k γkl .
[BS physical lines 1769-1779: Proposition7 exact recovery correctness]
L1769: Proposition 7. Algorithm 4 is correct and returns a compact representation of the input
L1770: α in polynomial time.
L1771: 
L1772: Proof. The invariant properties on the size of the elements are deduced in the same way as
L1773: in the proof of [4, Prop. 5.1]. The only important different is the way we compute an exact
L1774: representation of βP −1 . Barbai’s algorithm allows us to find in polynomial time a lattice
L1775: element β̃ in L := j Zc
L1776:                b                          b β̃) ≤ 2n d(β,
L1777:                           ωj such that d(β,            b L).
L1778:                                                           b If the precision is larger than n,
L1779: then the coefficients of β̃ on the basis ω
[BS physical lines 1784-1819: Section8.2, Algorithm5 and Proposition8]
L1784: 8.2    Computation of class groups
L1785: Let B = {p1 , · · · , pN } be a set of invertible prime ideals of an order O whose classes generate
L1786: Cl(O). We have a surjective morphism
L1787:                                             φ               π
L1788:                                ZN        −−−−→      I   −−−−→ Cl(O)
L1789:                                                   Q ei                  ,
L1790:                           (e1 , . . . , eN ) −−−−→ i pi −−−−→ i [pi ]ei
L1791:                                                               Q
L1792: 
L1793: 
L1794: and the class group Cl(O) is isomorphic to ZN / ker(π ◦ φ). Therefore, computing the class
L1795: group boils down to computing ker(π ◦ φ), which is the lattice of (e1 , ..., eN ) ∈ ZN such
L1796: that pe11 , . . . , peNN = (α) for some α ∈ K. These α are S-units for S = B, and the exponent
L1797: vectors of a generating set of US give us a generating set for ker(π ◦ φ) from which we derive
L1798: Cl(O)
L1799:     The best unconditional bounds on |S| are exponential in log(|∆|). As the complexity of
L1800: the computation of the |S|-unit group is polynomial in |S|, we cannot achieve a polynomial
L1801: complexity unconditionally that way. However, under the Generalized Riemann Hypothesis
L1802: (GRH), the classes of all prime ideals of O of norm up to 48 log(|∆|)2 generate Cl(O). The
L1803: size of S := {p ⊆ O prime | N (p) ≤ 48 log(|∆|)2 } is polynomial in log(|∆|), and calculating
L1804: the corresponding S-unit group is therefore polynomial in n and log(|∆|).
L1805: 
L1806: Algorithm 5 Ideal class group of O
L1807: Input: O
L1808: Output: d1 , · · · , dn such that O ≃ Z/d1 Z ⊕ · · · ⊕ Z/dn Z.
L1809:  1: S ← {p ⊆ prime | N (p) ≤ 48 log(|∆|)2 }.
L1810:  2: Compute the S-unit group US .
L1811:  3: Let (αj , vj,1 , · · · , vj,|S| )j≤r+|S| be the generating set for US computed.
L1812:  4: diag(d1 , · · · , dn ) ← Smith Normal Form of M = (vj,k ).
L1813:  5: return d1 , · · · , dn .
L1814: 
L1815: 
L1816: 
L1817: Proposition 8. Under the Generalized Riemann Hypothesis, Algorithm 5 is correct and
L1818: runs in polynomial time.
L1819: 
[BS physical lines 1843-1849: Algorithm6 explicit torsion notation]
L1843: Algorithm 6 Principal ideal problem
L1844: Input: O and an ideal a ⊆ O.
L1845: Output: Decide if a is principal and if so a compact representation of a generator α.
L1846:  1: Factor a, let S = {p1 , · · · , pk } be the divisors of a.
L1847:  2: Compute the S-unit group US = µ × ⟨ε1 ⟩ × · · · × ⟨εr+|S| ⟩.
L1848:                                           Q mi,j
L1849:  3: Let M = (mi,j ) such that εi = j pj .
```

## Poteaux--Weimann selected body text
```text
[IB physical lines 31-48: Field input and triangular basis convention]
L31: L. It is a free A-module of rank d and an integral basis of L/K is a collection
L32: b1 , . . . , bd ∈ B that form a A-basis of B .
L33:       This paper intends to give new complexity bounds for computing an integral
L34: basis and, more generally, for computing an A-basis of an arbitrary fractional
L35: ideal of L. These fundamental problems of computer algebra are cornerstones to-
L36: wards more advanced computational issues both in algebraic number theory and
L37: in algebraic geometry, such as developing a fast arithmetic of ideals in number
L38: fields [7] or computing Riemann-Roch spaces in function fields [2,14].
L39:       In all of the sequel, we will assume that L = K(θ) is generated by the root
L40: θ of a degree d monic separable irreducible polynomial f ∈ A[x]. Under this
L41: assumption, there exists an integral basis of L/K of shape
L42:                                                              
L43:                                         g1 (θ)       gd−1 (θ)
L44:                               B=     1,        ,...,                                   (1)
L45:                                          a1           ad−1
L46: 
L47: where gi ∈ A[x] is monic of degree i, ai ∈ A \ {0} and a1 | a2 | · · · | ad−1 . We call
L48: such a basis a triangular integral basis. This specific shape has various algorithmic
[IB physical lines 50-86: Boolean RAM, size parameters and actual Theorem1]
L50: Model of computation. For the sake of simplicity, we will express our complexity
L51: results in the case A = k[t] (resp. A = Z). We work with computation trees
L52: [6, Section 4.4]. When considering A = k[t], we use an algebraic RAM model,
L53: counting only the number of arithmetic operations in k. For A = Z, we consider
L54: the Boolean RAM model.
L55:     We classically denote O() and Oe() to respectively hide constant and loga-
L56: rithmic factors in our complexity results ; see e.g. [9, Chapter 25, Section 7]. We
L57: additionally let Oε (d) = O(d1+ε(d) ) with ε(d) → 0. We have Oe(d) ⊂ Oε (d), and
L58: freely speak of almost linear in d for both notations. As in [24], we express our
L59: complexity with Oε () because we deal with dynamic evaluation via the deter-
L60: ministic algorithm of [16]. Our results could be express with the Oe() notation
L61: using some Las Vegas sub-algorithm instead.
L62: Discriminant and index. Our results will be expressed using the size functions
L63: h(a) = P deg(a) when A = k[t] (resp. h(a) = log(|a|) when A = Z). Note that
L64: h(a) = p vp (a)h(p) where the sum runs over the primes p of A and vp stands
L65: for the p-adic valuation. Let us denote ∆ = ∆f the discriminant of f and ∆L/K
L66: the discriminant of L/K . Both quantities are related by the formula
L67:                                   ∆ = D2 ∆L/K                                  (2)
L68: where D = Df ∈ A is the index of f , generator of the indexP ideal [B : A[θ]].
L69: We denote for short h∆ := h(∆), hD := h(D) and hred := p2 |∆ h(p). Looking
L70: at the triangular basis (1), we observe that D = ua1 · · · ad−1 for some unit
L71: u ∈ A× and, up to reduce gi modulo ai , the basis B has global size O(dhD ), this
L72: bound being sharp. This observation suggests to emphasise the dependency of
L73: the complexity on the index D instead of the discriminant ∆ which is classically
L74: considered in the literature (see e.g. [1,3,25]).
L75: Global integral basis computation. Our main result is:
L76: Theorem 1. Suppose given a squarefree factorisation of the index D. There
L77: exists a deterministic algorithm which computes a triangular integral basis of
L78: L/K in less than
L79: 1. Oε (dhD ) operations in k if A = k[t] with char(k) = 0 or char(k) > d,
L80: 2. Oε (d hD + h2D ) operations in k if A = k[t] with char(k) ≤ d,
L81: 3. Oε (d hD + h2D ) word operations if A = Z.
L82: If we are only given the squarefree factorisation of the discriminant ∆, then a
L83: similar result holds, adding a cost O(d hred ) to the complexity estimates.
L84:    We thus get a softly linear cost in case 1. In the other cases, the over-cost in
L85: h2D is only due to the complexity of the OM algorithm [24] over small residual
L86: characteristic, so that the result would become softly linear for all cases if we
```
