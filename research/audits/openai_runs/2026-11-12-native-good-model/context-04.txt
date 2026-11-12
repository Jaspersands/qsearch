Source: research/audits/sources/surface_torsion_selection/kozen_resolution.txt
SHA256: 39bc0a1b55f42be35ae3be6de0abd43a7569563aac612efbc690893d43edd47c
Physical newline ranges; inspect lost PDF symbols.

LINES 1-550
1:                      Efficient Resolution of
2:                                               ∗
3:                  Singularities of Plane Curves
4: 
5:                                    Dexter Kozen
6: 
7:                             Computer Science Department
8:                                   Cornell University
9:                             Ithaca, New York 14853, USA
10:                                kozen@cs.cornell.edu
11: 
12: 
13: 
14:         Abstract. We give a new algorithm for resolving singularities of plane
15:         curves. The algorithm is polynomial time in the bit complexity model,
16:         does not require factorization, and works over Q or finite fields.
17: 
18: 
19: 1     Introduction
20: 
21: Resolving singularities is a central problem in computational algebraic geometry.
22: In this paper we describe a new algorithm for resolving singularities of irreducible
23: plane curves. The algorithm runs in polynomial time in the bit complexity model,
24: does not require polynomial factorization, and works over Q or any finite field.
25:     Classical algorithms for resolving singularities [2, 15, 7] use a combination of
26: methods involving
27: 
28:     – the Newton polygon, a polygon in Z2 whose vertices are the exponents of
29:       terms in f ;
30:     – Puiseux series, power series with fractional exponents.
31: 
32: These algorithms take polynomial time if we assume efficient factorization over
33: algebraic extensions of the base field and unit-time arithmetic these extensions.
34:     Teitelbaum [13] establishes bounds on the degree of field extensions con-
35: taining the Puiseux coefficients, leading to an algorithm that is polynomial in
36: the number of base field operations. However, the algorithm is not analyzed
37: for its bit complexity. The problem of intermediate coefficient swell is not of-
38: ten addressed in theoretical analyses, but is a serious consideration in practical
39: implementations [14, 17].
40:     Chistov [4] and Walsh [16] give algorithms that are polynomial time in the
41: bit complexity model, but require factorization of polynomials over Q and al-
42: gebraic number fields. The best known algorithms for these problems [12, 11, 9]
43: are theoretically polynomial time in the bit complexity model, but quite ineffi-
44: cient from a practical standpoint. There are currently no known deterministic
45: ∗
46:     In: P. S. Thiagarajan, ed., Proc. 14th Conf. Foundations Software Technology and
47:     Theor. Comput. Sci., December 1994, Madras, India, Springer Lect. Notes in Com-
48:     put. Sci., vol. 880, 1-11.
49: polynomial-time algorithms for factorization of polynomials over finite fields. For
50: practical considerations, it is important to avoid factorization if at all possible.
51:     A novel feature of our algorithm is that it does not calculate Puiseux series
52: explicitly. Rather, given a curve f (x, y) = 0, it builds a tree whose vertices are
53: labeled with approximations to local parameters of the exceptional places of the
54: curve. These are not Puiseux series as in the classical algorithms, but rational
55: functions of x and y obtained by direct reparametrizations based on information
56: obtained from the Newton polygon.
57:     The algebraic numbers involved are represented and manipulated symboli-
58: cally, using the technique of passive factorization [5, 6, 13] in conjunction with
59: the squarefree decomposition algorithm of [1]. All necessary calculations can be
60: carried out with this implicit representation, thus avoiding factoring and the
61: explicit construction of high-degree extensions.
62:     As an immediate corollary, we obtain an efficient algorithm for calculating the
63: genus of a plane curve using the Hurwitz formula [10, 7]. Trager has recently given
64: a polynomial-time algorithm for the genus problem using different techniques
65: [14].
66: 
67: 
68: 2     Algebraic Preliminaries
69: 
70: Let R be an algebraic function field over an algebraically closed field K, i.e., a
71: finite extension of a purely transcendental extension K(x) of K. A place of R is
72: a valuation ring P ⊆ R, i.e., a subring such that K ⊆ P 6= R and for all u ∈ R,
73: either u ∈ P or 1/u ∈ P. P has a unique maximal ideal I = {u ∈ P | 1/u 6∈ P},
74: and P/I ∼  = K. I is a principal ideal; a principal generator tP is called a local
75: parameter.
76:     For R = K(x), there is exactly one place for each a ∈ K with local parameter
77: x − a, denoted x = a, plus one place with local parameter 1/x, denoted x = ∞.
78:     If P is a place of R, then p = P ∩ K(x) is a place of K(x) and tp = tcP u for
79: some unit u ∈ P and positive integer c. The number c is called the ramification
80: index of P over p. Every place p of K(x) extends to at least one place P of R.
81:     Now let f (x, y) = 0 be an irreducible plane curve of degree n in y with
82: coefficients in K, and let R = K(x)[y]/f . A place p of K(x) is called simple if
83: for any two places P, P0 of R over p, P ∩ K(y) 6= P0 ∩ K(y), and all places of
84: R over p have ramification index 1 (i.e., tp is a local parameter); otherwise it is
85: called exceptional. There are only finitely many exceptional places of K(x).
86:     See [10, 7, 2, 3] for details.
87: 
88: 
89: 2.1   Statement of the Problem
90: 
91: The problem we consider in this paper is as follows. Given an irreducible plane
92: curve f (x, y) = 0 with coefficients in some subfield k ⊆ K, determine all the
93: exceptional places p of K(x). For each such p, determine the set of places P
94: of R over p. For each such P, determine its ramification index over p, a local
95: 
96: 
97:                                          2
98: parameter tP , and a birational reparametrization (change of variables) giving tP
99: in terms of x and y.
100:     In the solution of this problem, all computation should take place in the
101: subfield k. In practice, k will usually be Q or a finite field.
102: Example 1. Consider the hyperbola y 2 = x2 − 1. There are three exceptional
103: 
104: 
105: 
106: 
107:                                            2
108: 
109: 
110: 
111: 
112:                                            1
113: 
114: 
115: 
116: 
117:                 -2           -1            00            1        2
118:                                                          x
119: 
120: 
121: 
122: 
123:                                           -1
124: 
125: 
126: 
127: 
128:                                           -2
129: 
130: 
131: 
132: 
133:                                       Fig. 1.
134: 
135: 
136: places x = ±1 and x = ∞ of K(x). Each of the first two places extends to
137: one place of R with ramification index 2, with local parameters (x ± 1)/y. The
138: third extends to two places of R, each with ramification index 1 over K(x),
139: corresponding to the two asymptotes x = ±y of the hyperbola. The two local
140: parameters are x/y ± 1.
141: 
142: 2.2   Efficient Birational Reparametrization
143: A critical subroutine is birational reparametrization, or change of variables. We
144: will often wish to reparametrize an irreducible plane curve f (x, y) = 0 in terms of
145: new parameters u, v that are rational functions of x, y. We will need to compute
146: the defining equation g(u, v) = 0 of the curve in terms of the new parameters.
147:      The problem of birational reparametrization of algebraic surfaces has an
148: efficient solution in general, using multivariate gcds. For our application, all
149: cases we will encounter will be of the following special form:
150:                            u = (x − a)s (y − b)−t + c                           (1)
151:                                         −n           m
152:                             v = (x − a)         (y − b) + d
153: 
154: 
155:                                            3
156: where a, b, c, d ∈ K and s, t, m, n ∈ Z such that sm − tn = ±1. Any such map is
157: invertible, and its inverse is of the same form:
158: 
159:                              x = (u − c)m (v − d)t + a
160:                               y = (u − c)n (v − d)s + b
161: 
162: We can reparametrize efficiently as follows:
163:  1. Substitute (u − c)m (v − d)t + a for x and (u − c)n (v − d)s + b for y in f to
164:     obtain f ((u − c)m (v − d)t + a, (u − c)n (v − d)s + b).
165:  2. Multiply or divide by appropriate powers of u − c and v − d as necessary to
166:     clear denominators and eliminate extraneous factors of the form u − c and
167:     v − d.
168: The resulting polynomial g(u, v) is the irreducible representation of the plane
169: curve f (x, y) = 0 in terms of the parameters u, v.
170: Example 2. Consider the irreducible curve y 2 = x3 − x4 and the map u = x2 /y,
171: v = y 2 /x3 . This is a birational map of the form (1) with (s, t, m, n) = (2, 1, 2, 3)
172: and a = b = c = d = 0. Its inverse is x = u2 v, y = u3 v 2 . To reparametrize in
173: terms of u, v, substitute u2 v and u3 v 2 for x and y, respectively, in the equation
174: of the curve to get u6 v 4 = u6 v 3 − u8 v 4 and eliminate the factor u6 v 3 , leaving
175: the irreducible equation v = 1 − u2 v. Rewriting this as v = 1/(1 + u2 ), we see
176: that the curve is of genus zero and that u is a generator of the function field.
177: 
178: 2.3   Squarefree Decomposition
179: Another key subroutine is squarefree decomposition. One wishes to transform
180: a set A of polynomials into another set A0 such that the elements of A0 are
181: squarefree and pairwise relatively prime, and every element of A is a product of
182: powers of elements of A0 . An efficient solution to this problem was given in [1].
183: 
184: 
185: 3     First Algorithm
186: In this section, we describe the high-level structure of our algorithm. For this
187: section only, we assume that K is algebraically closed, that arithmetic in K
188: is unit-cost, and that we are provided with an efficient algorithm for factoring
189: univariate polynomials over K. These strong assumptions are to simplify the
190: high-level description. Once the algorithm is understood, we will describe in the
191: next section how to remove these assumptions.
192:      Most of the techniques used here, such as the Newton polygon, are well known
193: [2, 7, 15]. However, as mentioned in the introduction, one novel feature of our al-
194: gorithm is that we do not extend to the field of Puiseux series to obtain local
195: parameters, but reparametrize directly to obtain local parameters in the func-
196: tion field itself. This approach allows us to give an explicit description of the
197: coefficients occurring in the computation and analyze their bit complexity that
198: will be useful in the analysis of the next section.
199: 
200: 
201:                                           4
202: 3.1   Overview
203: 
204: We are given an irreducible polynomial f (x, y) ∈ K[x, y]. The algorithm builds a
205: rooted labeled tree. Each vertex τ in the tree is labeled with a reparametrization
206: fτ (xτ , yτ ) of f (x, y), along with some other information ∆τ that specifies a set
207: of places Pτ of R. The tree grows at the leaves as more information becomes
208: available that allows us to split or refine the set Pτ . The information is calculated
209: from the Newton polygon of fτ (xτ , yτ ).
210:      The edges of the tree are labeled with positive integers giving ramification
211: information, along with coefficients of birational transformations. If τ is a child
212: of σ, then the integer labeling the edge (σ, τ ) gives the ramification index of xσ
213: over xτ , and the birational transformation gives xτ and yτ in terms of xσ and
214: yσ .
215:      The information ∆τ is a Boolean combination of constraints of the form
216: h(xτ , yτ ) ∈ P or h(xτ , yτ ) ∈ I, where the symbols P, I range over places of R
217: and their unique maximal ideals, respectively. The set Pτ is the set of places of
218: R satisfying these constraints.
219:      We first do a precomputation involving discriminants to find all exceptional
220: places of K(x), and reparametrize so as to move these places to the origin. (Even
221: this step will be difficult without the assumptions above). We now want to resolve
222: the point (0, 0). In other words, we have fτ (xτ , yτ ) and ∆τ = {xτ ∈ I, yτ ∈ I},
223: thus we want to find all places of R whose maximal ideal contains xτ and yτ ,
224: along with their local parameters and ramification indices over K(x).
225:      We cause the tree to branch at a vertex τ by adding new constraints that may
226: partition the set of places associated with that vertex or give more ramification
227: information. The new constraints are obtained from the Newton polygon of fτ .
228: We continue to expand the tree at the leaves, reparametrizing, adding more
229: constraints, and refining the partition, until each leaf τ determines a unique
230: place of R and xτ is a local parameter.
231:      When we are done, the ramification index of the unique place of R associated
232: with a leaf τ is given by the product of the integers labeling the edges along
233: the path from the root to τ . The composition of the birational transformations
234: labeling the edges along the path gives xτ and yτ in terms of x and y.
235: 
236: 
237: 3.2   Formal Description
238: 
239: We are given an irreducible polynomial f (x, y) ∈ K[x, y].
240: 
241: 1. Create the root ρ of the tree and label it xρ = x, yρ = y, fρ = f , ∆ρ = ∅.
242: 2. Create a new vertex σ and an edge labeled 1 from ρ to σ. Reparametrize
243:    under the map xσ = 1/xρ , yσ = yρ and label σ with the resulting irreducible
244:    polynomial fσ (xσ , yσ ). Add the new constraint xσ ∈ I. Further resolution of
245:    this vertex will give all places of R over the place xρ = ∞ of K(xρ ).
246: 3. Compute the discriminant d(x) = discy f (x, y) and factor it. For each dis-
247:    tinct root a, create a new vertex τ and an edge with label 1 from ρ to τ .
248:    Reparametrize under the map xτ = xρ − a, yτ = yρ and label τ with the
249: 
250: 
251:                                           5
252:    resulting irreducible polynomial fτ (xτ , yτ ) = fρ (xτ + a, yτ ), along with the
253:    new constraint xτ ∈ I. Further resolution of this vertex will give all places of
254:    R over the place xρ = a of K(xρ ).
255: 4. For each child σ of ρ, if fσ (0, yσ ) is a nonzero constant, go on to step 5; there
256:    are no finite points (0, b) on the curve fσ (xσ , yσ ) = 0, i.e., no places or R
257:    with xσ ∈ I and yσ ∈ P. (Note fσ (0, yσ ) cannot be identically zero, since
258:    fσ (xσ , yσ ) is irreducible.) Otherwise, fσ (0, yσ ) is of positive degree. Factor it,
259:    and for each distinct root b, create a new vertex τ and an edge with label 1
260:    from σ to τ . Reparametrize under the map yτ = yσ − b, xτ = xσ and label
261:    τ with the resulting irreducible polynomial fτ (xτ , yτ ) = fσ (xτ , yτ + b). Add
262:    the constraints xτ ∈ I, yτ ∈ I.
263: 5. Also for each child σ of ρ, determine whether the point (0, ∞) lies on the
264:    curve fσ (xσ , yσ ) = 0 (i.e., whether there is a place of R such that xσ ∈ I
265:    and 1/yσ ∈ I). This is done by checking whether the lead coefficient of fσ ,
266:    considered as a polynomial in yσ with coefficients in K[xσ ], is divisible by xσ .
267:    If not, go on to step 6. Otherwise, create a new vertex τ and an edge with label
268:    1 from σ to τ . Reparametrize under the map yτ = 1/yσ , xτ = xσ to get the
269:    irreducible polynomial fτ (xτ , yτ ). We must have fτ (0, 0) = 0, otherwise the
270:    test above would have failed. Label τ with fτ (xτ , yτ ) and add the constraints
271:    xτ ∈ I, yτ ∈ I.
272: We now have at each leaf σ an irreducible polynomial fσ (xσ , yσ ) and constraints
273: xσ ∈ I, yσ ∈ I. By construction, fσ has no constant term, i.e. fσ (0, 0) = 0.
274: 6. If fσ (xσ , yσ ) has a linear term of the form cyσ , stop expanding this branch.
275:    In this case xσ is a local parameter, and there is a unique place satisfying ∆σ .
276: 7. Otherwise, assume fσ (xσ , yσ ) has no constant term or term of the form cyσ .
277:    For each edge of the Newton polygon of fσ (xσ , yσ ) with slope −m/n, m and n
278:    relatively prime, create a new vertex τ and an edge with label m from σ to τ .
279:    Let s and t be a minimal pair of nonnegative integers such that sm − tn = 1.
280:    Reparametrize with respect to xτ = xsσ /yσt and yτ = yσm /xnσ as described in
281:    (1). Label τ with the resulting irreducible polynomial fτ (xτ , yτ ) and add the
282:    constraints xτ ∈ I, yτ ∈ P − I.
283: 8. For each vertex τ created in step 7 with label fτ (xτ , yτ ), factor fτ (0, yτ ).
284:    For each nonzero root a of fτ (0, yτ ) (at least one such root must exist),
285:    reparametrize with respect to the map yυ = yτ −a, xυ = xτ to get fυ (xυ , yυ ) =
286:    fτ (xυ , yυ + a). Create a new vertex υ with that label and edge labeled 1 from
287:    τ to υ. Add the constraints xυ ∈ I, yυ ∈ I.
288:     Continue expanding leaves according to steps 7 and 8 until the stopping
289: condition of step 6 obtains. This must happen eventually. When done, there is
290: exactly one place of R for each leaf σ, the ramification index over K(xρ ) of this
291: place is the product of all the edge labels along the path from ρ to σ, and xσ is
292: a local parameter of the place.
293: Example 3. Consider the hyperbola y 2 = x2 − 1 of Example 1. We first compute
294: the discriminant
295:                               discy f (x, y) = 4(x2 − 1)
296: 
297: 
298:                                             6
299: with roots ±1. Substituting either of these values for x in the equation of the
300: curve gives y 2 = 0, which has a double root 0. Thus (±1, 0) are the two finite
301: exceptional points.
302:    Reparametrizing by the map x 7→ 1/x, we obtain
303: 
304:                                   x2 y 2 = 1 − x2
305: 
306: and substituting 0 for x gives 0 = 1, therefore there are no points on the curve of
307: the form (∞, b) for b finite. A similar calculation shows that there are no points
308: on the curve of the form (a, ∞) with a finite.
309:    Reparametrizing by the map (x, y) 7→ (1/x, 1/y) gives
310: 
311:                                  x2 = y 2 − x2 y 2                             (2)
312: 
313: and the point (0, 0) lies on this curve. It is an exceptional point since 0 is a
314: multiple root of the polynomial y 2 = 0 obtained by substituting 0 for x.
315:    We reparametrize the original equation under the maps x 7→ x ± 1 to move
316: the two finite exceptional points to (0, 0). The third equation (2) is already of
317: the desired form. We now have three irreducible equations
318: 
319:                                   y 2 = x2 − 2x
320:                                   y 2 = x2 + 2x
321:                                   x2 = y 2 − x2 y 2
322: 
323: labeling three children of the root, and wish to resolve the point (0, 0) for each.
324:     Now we do step 7 for the first equation. We plot the three exponent vectors
325: (0, 2), (2, 0), (1, 0), and observe that the Newton polygon has a single edge
326: through (0, 2) and (1, 0) with slope −2. According to step 7, we take m = 2,
327: n = 1, s = 1, t = 1, u = x/y, v = y 2 /x, x = u2 v, y = uv, and reparametrize to
328: obtain the irreducible polynomial
329: 
330:                               q(u, v) = v − u2 v + 2
331: 
332: We create a child with this label and an edge to it labeled 2. Now we do step 8.
333: We compute q(0, v) = v + 2, which has one nonzero root −2. We create a child
334: with label
335: 
336:                            q(x, y − 2) = y − x2 y + 2x2
337: 
338: and an edge labeled 1. The polynomial has a linear term y, so we stop expanding
339: this branch.
340:     There is one leaf and the product of the edge labels on the path from the
341: root to this leaf is 2, so we conclude that there is one place of R over the place
342: x = −1 of K(x) with ramification index 2.
343:     A similar computation holds for the second equation.
344:     For the third equation
345: 
346:                                  x2 = y 2 − x2 y 2
347: 
348:                                          7
349: we again plot the exponent vectors (2, 0), (0, 2), and (2, 2). The Newton polygon
350: has a single edge through (2, 0) and (0, 2) with slope −1, giving m = 1, n = 1,
351: s = 1, t = 0, u = x, v = y/x, y = uv. Reparametrizing, we obtain
352: 
353:                              q(u, v) = 1 − v 2 + u2 v 2 .
354: 
355: Then q(0, v) is 1 − v 2 which has two nonzero roots ±1. We create two new
356: children labeled
357: 
358:                    q(x, y − 1) = −y 2 + 2y + x2 y 2 − 2x2 y + x2
359:                    q(x, y + 1) = −y 2 − 2y + x2 y 2 + 2x2 y + x2
360: 
361: with edges to these vertices each labeled 1. The stopping condition holds at each
362: leaf, since each has a linear term ±2y. We conclude that there are two places of
363: R over the place x = ∞ of K(x), each with ramification index 1.
364: 
365: 
366: 4     Second Algorithm
367: Suppose that the coefficients of f lie in a subfield k of K. The algorithm of
368: the previous section is polynomial time, assuming unit-cost arithmetic in finite
369: extensions of k and the ability to factor. If we count the cost of the representation,
370: a naive approach may require exponential time.
371:    In this section we describe an implicit representation of the algebraic numbers
372: used in the algorithm of the previous section that allow them to be manipulated
373: using only arithmetic in the field k. We will use gcd heavily, but factorization is
374: unnecessary. This technique is called passive factorization and has been used by
375: Dicrescenzo and Duval [5, 6] and Teitelbaum [13]. We use this in conjunction with
376: the squarefree decomposition algorithm of [1] to avoid intermediate coefficient
377: swell when k = Q.
378: 
379: 4.1   Overview
380: Each of steps 3, 4, and 8 of the algorithm of Section 3 factored a polynomial
381: q(y), producing roots a. For each such a, we created a new child τ of the current
382: vertex σ and associated a with τ . The reparametrization of fσ to obtain fτ
383: involved the algebraic number a.
384:     Here, instead of factoring q to obtain the algebraic numbers a, we will just do
385: a squarefree decomposition of q using the algorithm of [1] to give finitely many
386: pairwise relatively prime factors qτ of q. We will create one new child τ for each
387: such factor qτ and associate qτ with τ . Subsequently, all computation involving
388: roots a of qτ will be done symbolically by introducing a new indeterminate a
389: and working modulo qτ (a). In effect, we will be dealing with all the roots of qτ
390: simultaneously in one subtree, instead of having a separate subtree for each root
391: as in the previous section.
392:     It may happen that some later computation causes qτ (a) to split further. This
393: will occur when a discrepancy in the behavior of the resolution over two different
394: 
395:                                           8
396: roots of qτ (a) is discovered. This discovery takes the form of another polynomial
397: in a that has a nontrivial common factor with qτ (a). When that occurs, we can
398: return to τ and split qτ using the gcd algorithm, then split τ into a separate
399: vertex for every new factor of qτ (a), replicating the entire subtree below each
400: new vertex. The tree never gets too big because of the absolute bound n on the
401: number of places.
402:     It may happen that qτ never splits. In that case the resolution over all roots
403: of qτ looks exactly the same, and the number of the places determined by the
404: subtree below τ can just be multiplied by the degree of qτ . Thus we have a single
405: node representing multiple places, but we know how many and their ramifica-
406: tions.
407:     Formally, at any vertex in the tree at any point in time, we have sequences
408:            a = a0 , a1 , a2 , . . . , ak                                                          (3)
409:             q = q0 (a0 ), q1 (a0 , a1 ), q2 (a0 , a1 , a2 ), . . . , qk (a0 , a1 , . . . , ak )   (4)
410: of indeterminates and polynomials describing them. The polynomials q gener-
411: ate a zero-dimensional variety V (q) in K k+1 . Arithmetic on coefficients will
412: be done modulo these qi . We maintain the invariants that each qi is reduced
413: modulo q1 , . . . , qi−1 and that the qi are squarefree. We also maintain the invari-
414: ant that the coefficients of qi , considered as polynomials in the indeterminates
415: a1 , . . . , ai−1 , are relatively prime to qi−1 .
416:      These conditions are determined by signs (zero or nonzero) of various sub-
417: resultants, which are minors of the Sylvester matrix [8]. These are polynomials
418: p(a0 , a1 , . . . , ai−1 ) in the coefficients of qi . For each such p, either its sign is de-
419: termined uniquely by q, i.e. p either vanishes on all of V (q) or does not vanish on
420: all of V (q), which allows the computation to be carried on; or p and qi−1 have a
421: nontrivial common factor, i.e. p vanishes on some nonempty subset of V (q) and
422: does not vanish on some other nonempty subset, in which case qi−1 splits and
423: we get a refinement. When all the splitting is done, we again have the property
424: that p(a) either vanishes on every point of V (q) or on no point of V (q).
425:      The key idea being exploited here is the same used in the BKR algorithm
426: for the theory of real closed fields [1], namely that we do not need to know the
427: algebraic numbers a themselves to solve the resolution problem, but only the
428: signs of certain polynomials in these algebraic numbers. This idea leads to an
429: efficient implementation of the passive factorization method of [5, 6, 13].
430:      Coefficients remain small under these symbolic operations. For example, in
431: step 7, we reparametrize
432:                                                 X
433:                                      f (x, y) =      pij (a)xi y j
434:                                                    ij
435: 
436: to obtain a new polynomial g(u, v). The terms of g(u, v) and those of f (x, y) are
437: in one-to-one correspondence, and corresponding terms have the same coefficient.
438: Thus g(u, v) is also of the form
439:                                        X
440:                              g(u, v) =   pk` (a)uk v ` .
441:                                                   k`
442: 
443: 
444:                                                     9
445: The polynomial g(0, y) has at least two nonzero terms. Let g(0, y) = y k h(y)
446: where h(y) is not divisible by y. In step 8, we factored h(y) and extended the
447: tree with a separate branch for each root, but here we will instead do a squarefree
448: decomposition of h(y) and extend the tree with a branch for each factor qn+1 (y).
449: For each such branch, a new indeterminate an+1 is created and qn+1 (an+1 ) is
450: added to the list q0 . . . , qn . Then we reparametrize symbolically with respect to
451: the map (u, v) = (x, y − a) to get
452:                                     X
453:                   g(u, v + a) =            pij (a)ui (v + a)j
454:                                     ij
455:                                                           j  
456:                                     X
457:                                                       i
458:                                                           X  j
459:                                 =          pij (a)u (                     v k aj−k )
460:                                                                     k
461:                                     ij                    k=0
462:                                                       j
463:                                                       X            
464:                                     X                           j
465:                                 =          pij (a)(                     ui v k aj−k )
466:                                                                 k
467:                                     ij                k=0
468:                                   X Xj 
469:                                 =  (      pij (a)aj−k )ui v k .
470:                                       k
471:                                     ik     j≥k
472: 
473: 
474: The new coefficients are
475:                                            Xj 
476:                            p0ik (a, a) =                   pij (a)aj−k
477:                                                     k
478:                                            j≥k
479: 
480: 
481: which are small. We reduce these modulo the qi and test the signs (zero or
482: nonzero) of the new coefficients p0ik (a, a) modulo the qi . As above, this may
483: cause further splitting of q in case the signs are not uniquely determined. When
484: done, we again have the property that no coefficient of g(u, v + a) vanishes at
485: any point of the variety V (q).
486: 
487: 
488: 5   Analysis
489: 
490: The tree is of small depth, since at each vertex, either there are multiple children;
491: or m > 1, in which case we get ramification (the maximum is n, and they are
492: multiplicative along edges); or the degree of the discriminant strictly decreases
493: [2, Theorem 15.1]. The number of branches is bounded by n, since there are at
494: most n places in all.
495:     There are at most as many qi at any vertex as the depth of the vertex. The
496: splitting of the tower (4) may cascade, but each such split uses only subresultant
497: computations and takes polynomial time. There are at most n splits since each
498: one creates a new branch of the tree. The product of the degrees of the qi is
499: at most n, since each sequence of roots (3) represented by the qi determines a
500: distinct place.
501: 
502: 
503:                                                10
504: Acknowledgements
505: 
506: We thank Len Adelman, Ming-Deh Huang, Doug Ierardi, Susan Landau, John
507: Little, Paul Pedersen, Moss Sweedler, Barry Trager, Emil Volcheck, Peter Walsh,
508: and especially Richard Zippel for their help. The support of the National Sci-
509: ence Foundation under grant CCR-9317320 and the U.S. Army Research Office
510: through ACSyAM, a branch of the Mathematical Sciences Institute of Cornell
511: University under contract DAAL03-91-C-0027 is gratefully acknowledged.
512: 
513: 
514: References
515:  1. M. Ben-Or, D. Kozen, and J. Reif, The complexity of elementary algebra and
516:     geometry, J. Comput. Syst. Sci., 32 (1985), pp. 251–264.
517:  2. G. A. Bliss, Algebraic Functions, Amer. Math. Soc., 1933.
518:  3. C. Chevalley, Introduction to the Theory of Algebraic Functions of One Variable,
519:     American Mathematical Society, 1951.
520:  4. A. L. Chistov, Polynomial complexity of the Newton-Puiseux algorithm, in Math.
521:     Found. Comput. Sci., vol. 233 of Lect. Notes. Comput. Sci., Springer, 1986, pp. 247–
522:     255.
523:  5. C. Dicrescenzo and D. Duval, Computations on curves, vol. 174 of Lect. Notes
524:     in Comput. Sci., Springer, 1984, pp. 100–107.
525:  6.       , Algebraic computations on algebraic numbers, in Informatique et Calcul,
526:     Wiley-Masson, 1985, pp. 54–61.
527:  7. W. Fulton, Algebraic Curves, Addison Wesley, 1989.
528:  8. D. Ierardi and D. Kozen, Parallel resultant computation, in Synthesis of Parallel
529:     Algorithms, J. Reif, ed., Morgan Kaufmann, 1993, pp. 679–720.
530:  9. S. Landau, Factoring polynomials over algebraic number fields, SIAM J. Comput.,
531:     14 (1985), pp. 184–195.
532: 10. S. Lang, Introduction to Algebraic and Abelian Functions, Springer-Verlag, sec-
533:     ond ed., 1972.
534: 11. A. K. Lenstra, Factoring polynomials over algebraic number fields, in Proc. Eu-
535:     roCal 1983, vol. 162 of Lect. Notes in Comput. Sci., Springer, 1983, pp. 245–254.
536: 12. A. K. Lenstra, H. W. Lenstra, and L. Lovász, Factoring polynomials with
537:     rational coefficients, Math. Ann., 261 (1982), pp. 515–534.
538: 13. J. Teitelbaum, The computational complexity of the resolution of plane curve
539:     singularities, Math. Comp., 54 (1990), pp. 797–837.
540: 14. B. M. Trager. Personal communication, 1994.
541: 15. B. M. Trager, Integration of Algebraic Functions, PhD thesis, Massachusetts
542:     Institute of Technology, Cambridge, MA, September 1984.
543: 16. P. G. Walsh, The Computation of Puiseux Expansions and a Quantitative Version
544:     of Runge’s Theorem on Diophantine Equations, PhD thesis, University of Waterloo,
545:     1994.
546: 17. R. Zippel. Personal communication, 1994.
547: 
548: 
549: 
550: 
