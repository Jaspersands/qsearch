# Checked primary local-field excerpts


## research/audits/sources/dyadic_reset/om2012.txt


Physical lines 1170-1210

1170: OUTPUT:
1171:   true if F (x) is irreducible over Op [x] and false otherwise.
1172: 
1173:               5. Complexity analysis of the Montes algorithm
1174:    All tasks we are interested in may be performed modulo pν , for a sufficiently
1175: high precision ν. Thus, we may assume that the elements of A are finite π-adic
1176: developments. In particular, the computation of the p-adic valuation v = vp has a
1177: negligible cost.
1178: Definition 5.1. An operation of A is called p-small if it involves two elements
1179: belonging to a fixed system of representatives of A/p.
1180:    Working at precision ν, each multiplication in A costs O(ν 1+ǫ ) p-small operations
1181: if we assume the fast multiplications techniques of Schönhage-Strassen [SS71]. 
1182:    Let q := #F. We assume that a p-small operation is equivalent to O log(q)1+ǫ
1183: word operations, the cost of an operation in the residue field F = A/p. This is the
1184: case in most of the Dedekind rings that naturally arise in practice.
1185: 5.1. Complexity of the basic subroutines.
1186: Lemma 5.2. [vzGG03, Cor. 14.30] Let F be a finite field with qF elements, and
1187: g(x) ∈ F [x] a polynomial of degree d. The cost of the routine Factorization(F , g)
1188: is O d2+ǫ + d1+ǫ log(qF ) operations in F .
1189:      The following observation is easy to prove by an inductive argument.
1190: Lemma 5.3. Let m1 , . . . , mi be positive integers such that m1 | · · · | mi and
1191: m1 < · · · < mi . Then, m1 + · · · + mi ≤ 2mi .
1192: Lemma 5.4. [Pau10, Lem. 18] Let t be a strongly optimal type of order i − 1 ≥ 1.
1193: Let a(x) ∈ O[x] be a polynomial of degree less than mi . The computation of the
1194: multiadic expansion of a(x),
1195:                      X
1196: (13)      a(x) =             aj (x)φ1 (x)j1 · · · φi−1 (x)ji−1 , deg aj < m1 ,
1197:                     j=(j1 ,...,ji−1 )
1198: 
1199: where 0 ≤ jk < ek fk , for all 1 ≤ k < i, has a cost of O((mi )1+ǫ ) operations in A.
1200:    Actually, in [Pau10] it was proved an estimation of O(m2i ) operations in A,
1201: assuming ordinary arithmetic. If we assume fast multiplication, the cost of the
1202: computation of the φi−1 -expansion of a(x) may be estimated in O((mi )1+ǫ ) oper-
1203: ations in A [vzGG03, Thm. 9.15]. By using this estimation, the proof of [Pau10,
1204: Lem. 18] leads to Lemma 5.4.
1205: Lemma 5.5. Let t be a strongly optimal type of order i − 1 ≥ 0, with representative
1206: φ(x). Let ω be a positive integer and g(x) ∈ A[x] a polynomial of degree d ≥ ωmi .
1207: Then, the cost of the routine Newton(t,ω,g) is O(ωd1+ǫ ) operations in A.
1208: Proof. The computation of the first ω + 1 coefficients of the φ-development of g(x)
1209: requires ω + 1 divisions with remainder:
1210:            g = φ · q1 + a0 ,     q1 = φ · q2 + a1 ,   ···   ,   qω = φ · qω+1 + aω .

Physical lines 1752-1810

1752: 
1753: word operations, if p is small.
1754: 5.4. Approximate factorization of polynomials over local fields. Theorem
1755: 5.15 leads to an improvement of the complexity estimates of all routines mentioned
1756: in the Introduction. In this section, we discuss the new estimation obtained for the
1757: factorization of polynomials over local fields, up to a prescribed precision.
1758:     Let F ∈ A[x] be a monic separable polynomial of degree n, and denote δ :=
1759: vp (Disc(F )). Let p be a non-zero prime ideal of A, and F1 , . . . , Fg ∈ Op [x] the
1760: irreducible factors of F over Op . Suppose an OM factorization of F over Op [x] has
1761: been computed, in the form of a family tF1 , . . . , tFg of OM representations of the
1762: irreducible factors, that faithfully represents F , and satisfies (12). Then, the single-
1763: factor lifting algorithm (SFL) derives from each tFs a monic polynomial Ps ∈ A[x],
1764: irreducible over Op , such that Ps ≈ Fs and Ps ≡ Fs (mod mν ), for an arbitrary
1765: prescribed precision ν.
1766: Theorem 5.17. The SFL algorithm requires O(nns ν 1+ǫ + nδs1+ǫ ) p-small opera-
1767: tions, where ns := deg Fs , δs := δ(Fs ).
1768: Proof. Let rs be the Okutsu depth of Fs . Along the proof of [GNP12,    Lem. 6.5], it
1769: is obtained an estimation of O nns (ν 1+ǫ + (Vrs +1 /e(Fs ))1+ǫ ) p-small operations.
1770:                                                                  
1771: 
1772: In Lemma 2.2 we have seen that the Okutsu discriminant δ0 (Fs ) := Vrs +1 /e(Fs ) is
1773: bounded from above by 2δs /ns . This proves the theorem.                           
1774: 
1775:  By applying the SFL routine to each OM representation tF1 , . . . , tFg , we get an
1776: OM factorization, F ≈ P1 · · · Pg , such that Ps ≡ Fs (mod mν ), for all 1 ≤ s ≤ g.
1777: Theorem 5.18. A combined application of the Montes and SFL algorithms, com-
1778: putes an OM factorization of F with prescribed precision ν, at the cost of
1779:       O n2+ǫ + n1+ǫ (1 + δ) log q + n1+ǫ δ 2+ǫ + n2 ν 1+ǫ p-small operations.
1780:                                                          
1781: 
1782:   If p is small, we obtain a cost of O n2+ǫ + n1+ǫ δ 2+ǫ + n2 ν 1+ǫ word operations.
1783:                                                                    
1784: 34                              BAUCH, NART, AND STAINSBY
1785: 
1786: 
1787: Proof. The estimation is obtained by adding to the cost of the Montes algorithm,
1788: given in Theorem 5.15, the sum of the costs of SFL given in Theorem 5.17, for
1789: 1 ≤ s ≤ g, having in mind that n1 + · · · + ng = n, δ1 + · · · + δg ≤ δ.      
1790:    In comparison with previous estimations, the total degree in n, δ and ν is reduced
1791: from 4 + ǫ to 3 + ǫ.
1792: 
1793:                                          References
1794: [FPR02] D. Ford, S. Pauli, and X.-F. Roblot, A Fast Algorithm for Polynomial Factorization
1795:  over Qp , Journal de Théorie des Nombres de Bordeaux 14 (2002), 151–169.
1796: [FV10] D. Ford, O. Veres, On the Complexity of the Montes Ideal Factorization Algorithm, in G.
1797:  Hanrot and F. Morain and E. Thomé, Algorithmic Number Theory, 9th International Sympo-
1798:  sium, ANTS-IX, Nancy, France, July 19-23, 2010, LNCS, Springer Verlag 2010.
1799: [vzGG03] J. von zur Gathen, J. Gerhard, Modern Computer Algebra, second Edition, Cambridge
1800:  University Press, 2003.
1801: [GMN10] J. Guàrdia, J. Montes, E. Nart, Okutsu invariants and Newton polygons, Acta Arith-
1802:  metica 145 (2010), 83–108.
1803: [GMN11] J. Guàrdia, J. Montes, E. Nart, Higher Newton polygons in the computation of dis-
1804:  criminants and prime ideal decomposition in number fields, Journal de Théorie des Nombres de
1805:  Bordeaux 23 (2011), no. 3, 667–696.
1806: [GMN12] J. Guàrdia, J. Montes, E. Nart, Newton polygons of higher order in algebraic number
1807:  theory, Trans. Amer. Math. Soc. 364 (2012), no. 1, 361–416.
1808: [GMN12a] J. Guàrdia, J. Montes, E. Nart, A new computational approach to ideal theory in
1809:  number fields, arXiv:1005.1156v3[math.NT].
1810: [GMN12b] J. Guàrdia, J. Montes, E. Nart, Higher Newton polygons and integral bases, arXiv:

## research/audits/sources/local_kummer_cluster/integral_bases.txt


Physical lines 50-70

50: Model of computation. For the sake of simplicity, we will express our complexity
51: results in the case A = k[t] (resp. A = Z). We work with computation trees
52: [6, Section 4.4]. When considering A = k[t], we use an algebraic RAM model,
53: counting only the number of arithmetic operations in k. For A = Z, we consider
54: the Boolean RAM model.
55:     We classically denote O() and Oe() to respectively hide constant and loga-
56: rithmic factors in our complexity results ; see e.g. [9, Chapter 25, Section 7]. We
57: additionally let O (d) = O(d1+(d) ) with (d) → 0. We have Oe(d) ⊂ O (d), and
58: freely speak of almost linear in d for both notations. As in [24], we express our
59: complexity with O () because we deal with dynamic evaluation via the deter-
60: ministic algorithm of [16]. Our results could be express with the Oe() notation
61: using some Las Vegas sub-algorithm instead.
62: Discriminant and index. Our results will be expressed using the size functions
63: h(a) = P deg(a) when A = k[t] (resp. h(a) = log(|a|) when A = Z). Note that
64: h(a) = p vp (a)h(p) where the sum runs over the primes p of A and vp stands
65: for the p-adic valuation. Let us denote ∆ = ∆f the discriminant of f and ∆L/K
66: the discriminant of L/K . Both quantities are related by the formula
67:                                   ∆ = D2 ∆L/K                                  (2)
68: where D = Df ∈ A is the index of f , generator of the indexP ideal [B : A[θ]].
69: We denote for short h∆ := h(∆), hD := h(D) and hred := p2 |∆ h(p). Looking
70: at the triangular basis (1), we observe that D = ua1 · · · ad−1 for some unit

Physical lines 116-230

116: of Monte Carlo type which computes the radical of ∆ (and this is enough for
117: our purpose) in softly optimal time in h∆ .
118: 
119: Integral basis over a prime p. If we only want a p-integral basis at a given prime
120: p ∈ A (that is an Ap -basis of B ⊗ Ap over the localisation of A at p), we get
121: similar complexity estimates than in Theorem 1, replacing hD and hred by their
122: respective local contributions vp (D)h(p) and h(p). There's no need to compute
123: and factorise the discriminant in such a case. This result has to be compared to
124: [25, Theorem 3.5] (triangular basis) or [3, Lemma 3.10] (non triangular basis).
125: 
126: The case of fractional ideals. In Section 4, we provide similar complexity results
127: to compute integral basis of an arbitrary fractional ideal I ⊂ L, expressed now
128: in terms of the size of the index [I ∗ : A[θ]] of the smallest multiple I ∗ = αI ,
129: α ∈ K such that B ⊂ I ∗ , see Theorem 7. This is an important issue towards the
130: computation of Riemann-Roch spaces in function elds.
131: Previous results. Classical methods for computing integral bases are variants of
132: the Round-2 and Round-4 routines by Zassenhaus and Ford [8,13,15,23]. The
133: central idea is to start from a known order A[α] ⊂ B , and to enlarge it for each
134: prime p ∈ A dividing the discriminant of A[α] until we reach the maximal order
135: B . Another strategy of local-to-global type was developed by Okutsu [20]: as-
136: suming given the local p-integral basis Bp for each prime ideals p ⊂ B dividing
137: a prime p ∈ A, one can compute multipliers zp ∈ L such that Bp = ∪zp Bp is
138: a p-integral basis. Then, after reducing Bp to a triangular form, one can glue
139: the various bases Bp into a global integral basis B by means of Chinese remain-
140: ders. Later on, Montes [22] extended the ideas of Ore and MacLane [17,18] and
141: developed the OM algorithm that computes a representation of the prime ide-
142: als p dividing a prime p ∈ A by way of factoring f over the p-adic completion
143: of K . This led to an ecient computation of the local basis Bp , last missing
144: ingredient in Okutsu's strategy. This opened the door to various OM-based rou-
145: tines: methods of multipliers [1,3,11], method of the quotients [12] and nally
146: the remarkably simple MaxMin algorithm of Stainsby [25] that we follow here.
147: Summary of our strategy. We do not claim any originality in our approach,
148: following the classical local to global strategy outlined in [2,25]:
149:  1. Run the fast OM algorithm [24] above each prime p ∈ A dividing ∆ (if we
150:      start with a squarefree factor, we rely on dynamic evaluation) and deduce
151:      for each prime ideal p ⊂ B dividing p a local p-integral basis together with
152:      a suitable approximant of the associated local factor Fp of f .
153:  2. Apply the MaxMin algorithm [25] to deduce a triangular p-integral basis (each
154:      numerator being a suitable multiplicative combination of the numerators of
155:      the various p-bases).
156:  3. Use the Chinese Reminder Theorem to glue these p-integral basis as a global
157:      triangular integral basis.
158: Concerning Point 2, it is remarkable that [25] allows to compute a triangular
159: p-integral basis avoiding the usual costly Hermite type reduction step. The OM
160: algorithm was the main bottleneck of the associated complexity analysis given in
161: [26] and our improvements mainly follow from the recent faster OM algorithm
162: [24], together with a careful study of the various p-adic precisions needed to
163: conduct the computations.
164: Organisation of the paper. In Section 2, we rst remind how local integral bases
165: (one for each factor of the local factorisation of f ) are deduced from the Okutsu
166: frames computed during the OM algorithm. Then, we prove that the usual preci-
167: sion vp (∆) used in the OM algorithm can be improved by 2 vp (D) + 1, key result
168: towards the proof of Theorem 1. Section 3 is dedicated to glue local bases into a
169: reduced triangular p-integral basis thanks to the MaxMin algorithm of Stainsby,
170: these p-integral bases being then glued into an integral basis of L/K using Chi-
171: nese remaindering (Subsection 3.3). Section 4 is dedicated to integral bases of
172: arbitrary fractional ideals. We pay attention to complexity issues and prove our
173: main Theorem 1 in Section 5 . Finally, we illustrate the overall strategy with an
174: example of [25] in Section 6.
175: 2      OM algorithm and local integral basis
176: 
177: Let A be a principal ideal domain with eld of fraction K and let L = K(θ)
178: be the eld extension determined by a root θ ∈ K of a monic, irreducible and
179: separable polynomial f ∈ A[x] of degree d.
180:     The OM algorithm [22], from the initial of its main artisans Ore, MacLane,
181: Okutsu and Montes, computes an OM representation of each prime ideal of L
182: lying over a given prime p ∈ A. This computational object supports several
183: arithmetic data attached to an irreducible factor (say F ) of f over the p-adic
184: completion Kp of K . In particular, it allows to compute a local integral basis of
185: the nite extension of Kp determined by F , rst step towards the local-to-global
186: computation of an integral basis of L/K . After recalling this construction, we
187: give new tight bounds for the precision required by the OM algorithm.
188: 
189: 2.1 Local integral basis and OM-factorisation.
190: We x a prime p ∈ A and consider vp : K × → Z the p-adic valuation, Kp the
191: completion of K with respect to vp and Op the valuation ring of Kp . We still
192: denote vp the canonical extension of vp to a xed algebraic closure K p of Kp .
193: 
194: Okutsu frame and local integral basis. Let F ∈ Op [x] be an irreducible monic
195: polynomial of degree n and let α ∈ K p be a root of F .
196: Denition 1. An Okutsu frame of F is a sequence [φ1 , . . . , φr+1 ], with φi ∈
197: Op [x] monic of degree mi such that (denoting m0 = 1, φ0 = 1):
198:     • m1 | m2 | · · · | mr+1 and 1 ≤ m1 < m2 < · · · < mr+1 = n.
199:     • For all g ∈ Op [x] monic, deg g < mi+1 =⇒ deg(g)
200:                                                      vp (g(α))  v (φ (α))  v (φ    (α))
201:                                                                ≤ p mii    < p mi+1
202:                                                                                 i+1
203: 
204: 
205: The polynomial φr+1 is called an Okutsu approximant of F .
206:    The degrees mi = deg(φi ) and the length r do not depend on the choice of the
207: frame. For any 0 ≤ m < n, we can write in a unique way m = j0 m0 + · · · + jr mr
208: with 0 ≤ ji < mi+1 /mi . We accordingly let
209:                              gm := xj0 φj11 · · · φjrr ∈ Op [x].
210: 
211:    The integral closure Op of Op in Kp (α) is a free Op -module of rank n. Okutsu
212: proved [20, Theorem 1]:
213: Proposition 1. Let ηm = bvp (gm (α))c. The family 1 , gp(α) , . . . , gp
214:                                                                    1
215:                                                                        η1
216:                                                                             d−1 (α)
217:                                                                              ηd−1     is an
218: Op -basis of Op . We call it an Okutsu basis of F .
219: We have η1 ≤ · · · ≤ ηd−1 = exp(F ) where exp(F ) is the integrality exponent of
220: F , least integer such that pexp(F ) Op ⊂ Op [α].
221: 
222: Denition 2. Let g0 = 1 and gn = φr+1 . The set N (F ) := {g0 , g1 , . . . , gn−1 , gn }
223: is called an extended set of Okutsu numerators of F .
224: OM-factorisation. The prime ideals p of L dividing p are one-to-one             with the
225: irreducible monic factors of f in Op [x]. We denote f = p|p Fp and we let
226:                                                                      Q
227: 
228: θp ∈ K p be an arbitrary root of Fp .
229: Denition    3. An Okutsu     factorisation of f above p is a set (Fp )p|p where
230: Fp := φp,0 , . . . , φp,rp +1 is an Okutsu frame of Fp , with φp,i ∈ A[x]. An OM-
