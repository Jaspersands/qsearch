Source research/audits/sources/surface_module_2026/mascot_lift.txt; SHA256 bffc16d45d3b3a7906f9cba913bde32ed02134b3dc10f09281fd342626448e69
Actual primary reconstruction warning and numerical pipeline excerpts.

LINES 80-144
80: Remark 1.3. Although we focus on the case of representations of Gal(Q/Q) for the
81: simplicity of exposition, it is completely straightforward to generalize the techniques
82: presented in this article to the case of mod ` representations of Gal(k/k) where k
83: is a number field, by taking C to be defined over k, and replacing p by a finite
84: prime p of k whose residual characteristic is distinct from ` and at which C has
85: good reduction.
86: 
87: Remark 1.4. The case of a representation with values in GLd (Fλ ), where Fλ is
88: a finite extension of F` , can also be treated by our methods (provided of course
89: that the curve C is known), since restriction of scalars and the flexibility of [Dok13]
90: allows us to treat it as a representation with values in a subgroup of GLd[Fλ :F` ] (F` ).
91: 
92: 
93: 
94: 
95:                                             2
96: 1.2    Outline
97: Our strategy to compute ρ may be summarized as follows:
98: 
99:   1. Compute d points forming a basis of the image of Tρ in J(Fq )[`], where q = pa
100:      with a ∈ N large enough to split ρ (i.e. large enough that the points of the
101:      reduction of Tρ mod p are defined over Fq ),
102: 
103:   2. Fix an integer e ∈ N, and lift these points to approximations with accu-
104:      racy O(pe ) of `-torsion points in J(Qq ), that is to say to points of J(Zq /pe ),
105:      where Qq denotes the unramified extension of Qp whose residue field is Fq
106:      and Zq is the ring of integers of Qq ,
107: 
108:   3. Compute all the F` -linear combinations of these d points, thus obtaining a
109:      model of Tρ over Zq /pe ,
110: 
111:   4. Evaluate a rational map α : J 99K A1 defined over Q at these `d points, and
112:      form the monic polynomial F (x) whose roots are these values,
113: 
114:   5. Check that these values are distinct, else take another map from J to A1 and
115:      try again,
116: 
117:   6. Identify F (x) as a polynomial with coefficients in Q, or, if this fails, start over
118:      with a larger value of e.
119: 
120:    Indeed, for each nonzero t ∈ Tρ , α(t) lies in the field of definition Q(t) of t, so
121: the splitting field of F (x) is a subfield of the field corresponding to the kernel of ρ,
122: and agrees with it with high probability since most elements of a number field are
123: primitive elements. More precisely, a sufficient condition for the Galois action on
124: the roots of F (x) to reflect faithfully that on the points of Tρ is that α be injective
125: on Tρ , which is what we check at step 5.
126: 
127: Remark 1.5. In step 2, we are justified in speaking of J(Zq /pe ) thanks to our
128: assumption that C has good reduction at p.
129: 
130: Remark 1.6. Because of the identification performed at step 6, the output of this
131: algorithm is not guaranteed to be correct, and should be certified by methods such
132: as [Mas18a].
133: 
134:     Throughout this algorithm, we use Kamal Khuri-Makdisi’s methods [KM04], [KM07]
135: to compute in J. We give a brief presentation of these techniques in section 2, in-
136: cluding a recipe to construct rational maps from J to A1 and comments on the
137: implementation over a p-adic field.
138:     The core of this article is devoted to the presentation of a technique to lift
139: torsion points from Fq to Qq (up to some arbitrary p-adic accuracy) in Makdisi’s
140: framework. After differential calculus preliminaries in section 3, we show how to lift
141: a point from J(Fq ) to J(Zq /pe ) for any e ∈ N in section 4, and then how to ensure
142: that the lift of an `-torsion point over Fq remains `-torsion over Zq /pe in section 5.
143:     Finally, we explain in detail how to use these tools to compute Galois represen-
144: tations in section 6, and we give explicit examples in section 7.

LINES 1850-1895
1850:     The complexity of this algorithm is O (g log q+(a+d) log `)dg ω where d = dim ρ,
1851: assuming we have to give up the current x a bounded number of times, and neglecting
1852: the cost of discrete logarithms in µ` and of linear algebra over F` .
1853: 
1854: Remark 6.5. We can further improve the efficiency of the algorithm if, every time
1855: a new yr has been verified to be linearly independent of y1 , · · · , yr−1 , we repeatedly
1856: apply the Frobenius Φ to yr and add the corresponding points to our partial basis
1857: of Tρ as long as no linear dependence is detected. Indeed, the application of Φ by
1858: algorithm 8 is very fast. This idea is very similar to that presented in section 6.4
1859: below.
1860: 
1861: Remark 6.6. In order to be able to use the “linearized” version of the Frey-Rück
1862: pairing, we need Fq to contain the `-th roots of unity (else this pairing would be
1863: trivial anyway). This is often the case, since the determinant of the representation ρ
1864: usually involves the mod ` cyclotomic character due to the existence of the Weil
1865: pairing. In any case we can always extend Fq , but this would considerably slow
1866: down all the computations.
1867: 
1868:                                              34
1869: 6.3     The rest of the computation
1870: Now that we have obtained an F` -basis of Tρ ⊂ J(Fq )[`] by algorithm 13, we first
1871: fix an e ∈ N, and we lift our basis into a basis of Tρ ⊂ J(Qq )[`] to accuracy O(pe )
1872: by a combination of algorithms 10 and 11 as explained in remarks 5.6 and 5.2.
1873: We then use algorithm 3 to compute all the points of Tρ , and we evaluate these
1874: points by algorithm 7, still at precision O(pe ). All these computations can be mas-
1875: sively parallelized, and their complexity is O(ea
1876:                                                e   log p)O(g ω+3 + g ω+1 log ` + g ω `d ) bit
1877: operations.
1878:     Finally, we form the monic polynomial F (x) whose roots are the values in Qq
1879: that we have just obtained. Since Tρ is globally invariant under Galois, F (x) has
1880: coefficients in Qp , and these coefficients approximate rational numbers within O(pe ).
1881: We can identify these rationals by rational reconstruction, provided that e is large
1882: enough.
1883: Remark 6.7. The value of e is chosen from experience; see section 7 below for
1884: concrete examples. If e is too low, rational reconstruction will most likely fail,
1885: but might also produce incorrect results. Therefore the output of our algorithm to
1886: compute ρ is not guaranteed to be correct, and should be certified by methods such
1887: as [Mas18a].
1888:     Arakelov theory could in principle provide us with bounds on the height of these
1889: rationals, but in practice these bounds are often extremely pessimistic, as noted
1890: in [Mas13].
1891: 
1892: 6.4     Saving effort thanks to the Frobenius
1893: We have already noted in remark 6.3 that for the efficiency of the computations,
1894: we should if possible choose the prime p so that the degree a = [Fq : Fp ] is small.
1895: However, when this is not possible (e.g. because we cannot afford to compute the
