Source: research/audits/sources/surface_module_2026/integral_bases.txt
SHA256: 26ead479488aab0fdb759caf2bb7921b7c9169920c5bcaa6c2fd569a7ba63404
Physical newline ranges; inspect lost PDF symbols.

LINES 1-135
1:                                             On the complexity of computing integral bases
2:                                                          of function fields
3: 
4:                                                                          Simon Abelard1
5: 
6:                                                Laboratoire d’informatique de l’École polytechnique (LIX, UMR 7161)
7: 
8: 
9: 
10: 
11: arXiv:2005.03964v1 [cs.SC] 8 May 2020
12:                                                                CNRS, Institut Polytechnique de Paris
13:                                                                   abelard@lix.polytechnique.fr
14: 
15: 
16: 
17:                                               Abstract. Let C be a plane curve given by an equation f (x, y) = 0
18:                                               with f ∈ K[x][y] a monic squarefree polynomial. We study the prob-
19:                                               lem of computing an integral basis of the algebraic function field K(C)
20:                                               and give new complexity bounds for three known algorithms dealing
21:                                               with this problem. For each algorithm, we study its subroutines and,
22:                                               when it is possible, we modify or replace them so as to take advantage
23:                                               of faster primitives. Then, we combine complexity results to derive an
24:                                               overall complexity estimate for each algorithm. In particular, we modify
25:                                               an algorithm due to Böhm et al. and achieve a quasi-optimal runtime.
26: 
27: 
28:                                         Acknowledgements. Part of this work was completed while the author was at the
29:                                         Symbolic Computation Group of the University of Waterloo. This paper is part
30:                                         of a project that has received funding from the French Agence de l’Innovation
31:                                         de Défense. The author is grateful to Grégoire Lecerf, Adrien Poteaux and Éric
32:                                         Schost for helpful discussions and to Grégoire Lecerf for feedback on a prelimi-
33:                                         nary version of this paper.
34: 
35: 
36:                                         1    Introduction
37:                                         When handling algebraic function fields, it is often helpful –if not necessary– to
38:                                         know an integral basis. Computing such bases has a wide range of applications
39:                                         from symbolic integration to algorithmic number theory and applied algebraic
40:                                         geometry. It is the function field analogue of a well-known and difficult problem:
41:                                         computing rings of integers in number fields and, as often, the function field
42:                                         version is easier: the algorithm of Zassenhaus [25] described for number fields in
43:                                         the late 60’s can indeed be turned into a polynomial-time algorithm for function
44:                                         fields which was later precisely described by Trager [23].
45:                                             However, there are very few complexity results going further than just stating
46:                                         a polynomial runtime. Consequently, most of the existing algorithms in the lit-
47:                                         erature are compared based on their runtimes on a few examples and this yields
48:                                         no consensus on which algorithm to use given an instance of the problem. In this
49:                                         paper, we provide complexity bounds for three of the best-known algorithms to
50:                                         compute integral bases and provide complexity bounds based on state-of-the art
51:                                         results for the primitives they rely on.
52: 2       Simon Abelard
53: 
54:     In this paper, we focus on the case of plane curves C given by equations
55: of the form f (x, y) = 0 with f ∈ K[x][y] monic in y and squarefree. We set
56: the notation n = degy f and dx = degx f . The associated function field is
57: K(C) = Frac (K(x)[y]/f (x, y)), it is an algebraic extension of degree n of K(x).
58: An element h(x, y) of K(C) is integral (over K[x]) if there exists a monic bivari-
59: ate polynomial P (x, y) such that P (x, h(x, y)) equals 0 in K(C). The set of such
60: elements forms a free K[x]-module of rank n and a basis of this module is called
61: an integral basis of K(C).
62:     Computing integral bases of algebraic function fields has applications in sym-
63: bolic integration [23] but more generally an integral basis can be useful to handle
64: function fields. For instance, the algorithm of van Hoeij and Novocin [13] uses
65: such a basis to “reduce” the equation of function fields and thus makes them
66: easier to handle. The algorithm of Hess [11] to compute Riemann-Roch spaces
67: is based on the assumption that integral closures have been precomputed. This
68: assumption is sufficient to establish a polynomial runtime, but a more precise
69: complexity estimate for Hess’ approach requires to assess the cost of computing
70: integral closures as well.
71: 
72: Our contribution. We provide complexity estimates for three algorithms ded-
73: icated to computing integral bases of algebraic function fields in characteris-
74: tic 0 or greater than n. To the best of our knowledge, no previous bounds
75: were given for these algorithms. Another approach which has received a lot
76: of attention is the use of Montes’ algorithm. We do not tackle this approach
77: in the present paper, a complexity estimate has been given by Bauch in [2,
78: Lemma 3.10] in the case of number fields. Using the Montes algorithm, a lo-
79: cal integral basis of a Dedeking domain  A at a prime ideal p is computed in
80: O n1+ε δ log q + n1+ε δ 2+ε + n2+ε δ 1+ε p-small operations, with δ the p-valuation
81: of Disc(f ) and the cardinal of A/p.
82:     Our contribution is actually not limited to a complexity analysis: the algo-
83: rithms that we present have been slightly modified so that we could establish
84: better complexity results. We also discuss possible improvements to van Hoeij’s
85: algorithm in some particular cases that are not uncommon in the literature. Our
86: main complexity results are Theorems 1, 2 and 3. Note that we count field oper-
87: ations and do not take into account the coefficient growth in case of infinite fields
88: nor the field extensions incurred by the use of Puiseux series. We also made the
89: choice not to delve into probabilistic aspects: all the algorithms presented here
90: are “at worst” Las Vegas due to the use of Poteaux and Weimann’s algorithm,
91: see for instance [21, Remark 3].
92:     We decided to give worst-case bounds and to only involve n and Disc(f ) in
93: our theorems so as to give ready-to-use results. Our proofs, however, are meant
94: to allow the interested reader to derive sharper bounds involving more precise
95: parameters such as the regularity and ramification indices of Puiseux series.
96:     We summarize these complexity estimates in Table 1 in a simpler context:
97: we ignore the cost of factorizations and bound both n and dx = degx f by D.
98: In this case, the input size is in O(D2 ) and output size in O(D4 ). The constant
99: 2 ≤ ω ≤ 3 refers to a feasible exponent for matrix multiplication, see [18] for the
100:              On the complexity of computing integral bases of function fields           3
101: 
102: smallest value currently known. Translating the above bound, the complexity of
103:                                    e 5 ) but only for a computing a local integral
104: the Montes approach is at best in O(D
105: basis at one singularity, while the algorithm detailed in Section 4 computes a
106:                                                                          e 4 )).
107: global integral basis for a quasi-optimal arithmetic complexity (i.e. in O(D
108: 
109: Organization of the paper. We sequentially analyze the three algorithms: Sec-
110: tion 2 is dedicated to van Hoeij’s algorithm [12], Section 3 to Trager’s algo-
111: rithm [23] and Section 4 to an algorithm by Böhm et al. introduced in [3]. In
112: each section, we first give an overview of the corresponding algorithm and insist
113: on the parts where we perform some modifications. The algorithms we describe
114: are variations of the original algorithms so we give no proof exactness and re-
115: fer to the original papers in which they were introduced. Then, we establish
116: complexity bounds for each algorithm by putting together results from various
117: fields of computer algebra. We were especially careful about how to handle linear
118: algebra, Puiseux series and factorization over K [[x]] [y].
119: 
120: 
121:        Table 1. Simplified complexity estimates for computing integral bases.
122: 
123:                            Algorithm            Worst-case complexity
124:                     Trager’s algorithm [23]              e
125:                                                          O(D7 )
126:                    Van Hoeij’s algorithm [12]          e
127:                                                        O(Dω+4 )
128:                   Böhm et al.’s algorithm [3]            e 4)
129:                                                          O(D
130: 
131: 
132: 
133: 
134: 2     Van Hoeij’s algorithm
135: 
