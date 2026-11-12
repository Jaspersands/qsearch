Source arXiv0706.0272 retained research/audits/sources/surface_module_2026/couveignes.txt; SHA256 35a28c2eb1ffc78020e221463290c36da505a8bfdefcc37b9946e1fd247491a8
Finite-field source, NOT a characteristic-zero bit theorem.

LINES 284-417
284: divisors on X .
285:     For any integer h ≥ 0 we set
286: 
287:                                     Sh = H 0 (P2 /Fq , OP2 /Fq (h))
288: the Fq -linear space of degree h homogeneous polynomials in X, Y , and Z. It is a vector space
289: of dimension (h+1)(h+2)
290:                     2
291:                           over Fq . A basis for it is made of all monomials of the form X a Y b Z c
292: with a, b, c ∈ N and a + b + c = h.
293:     We denote by
294: 
295:                                     Hh = H 0 (X /Fq , OX /Fq (h))
296: the space of forms of degree h on X . Here OX /Fq (h) is the pullback of OP2 /Fq (h) to X .
297:      Let W be a degree h form on P2 having non-zero pullback WX on X . Let H = (WX ) be
298: the divisor of this restriction. The map f 7→ WfX is a bijection from H 0 (X /Fq , OX /Fq (h)) to the
299: linear space L(H).
300:      If ∆ is a divisor on X we note Hh (−∆) the subspace of forms in Hh with divisor ≥ ∆. The
301: dimension of Hh (−C) is at least dh + 1 − g − deg(C) and is equal to this number when it exceeds
302: g − 1. This is the case if h ≥ d. The dimension of Hh (−C) is greater than 2g if h ≥ 2d.
303:      The image of the restriction map ρ : Sh → Hh contains Hh (−C) according to Noether’s
304: residue theorem [15, Theorem 7].
305:      We set SC = S2d and HC = H2d (−C), and HC = ρ−1 (HC ) ⊂ SC and KC = Ker(ρ) ⊂ HC .
306: So we have 0 → KC → HC → HC → 0.
307: P To find linear equations     for HC ⊂ SC we consider a generic homogeneous form F (X, Y, Z) =
308:                      a b c
309:    a+b+c=2d ǫa,b,c X Y Z of degree 2d in X, Y and Z. For every branch P above a singular point
310: S ∈ C (assuming for example that S has non-zero Z-coordinate) we replace in F ( X          , Y , 1) the
311:                                                                                          Z Z
312: affine coordinates x = X   Z
313:                               and y = YZ by their expansions as series in the local parameter tP at
314: this branch. We ask the resulting series in tP to have valuation at least the multiplicity of P in the
315: conductor C. Every singular branch thus produces linear equations in the ǫa,b,c . The collection of
316: all such equations defines the subspace HC .
317:      A basis for the subspace KC ⊂ HC ⊂ SC consists of all X a Y b Z c E(X, Y, Z) with a+b+c =
318: d. We fix a supplementary space MC to KC in HC and assimilate HC to it.
319:      Given a homogeneous form in three variables one can compute its divisor on X using re-
320: sultants and the given expansions of affine coordinates in terms of the local parameters at every
321: singular branch. A function is given as a quotient of two forms.
322: 
323: 3.4 The Brill-Noether algorithm
324: Linear spaces of forms computed in the previous paragraph allow us to compute in the group
325: J (Fq ) of Fq -points in the jacobian of X . We fix an effective Fq -divisor ω with degree g on X .
326: This ω will serve as an origin: a point α ∈ J (Fq ) is represented by a divisor A − ω in the
327: corresponding linear equivalence class, where A is an effective Fq -divisor with degree g. Given
328: another point β ∈ J (Fq ) by a similar divisor B −ω, we can compute the space H2d (−C−A−B)
329: which is non-trivial and pick a non-zero form f1 in it. The divisor of f1 is (f1 ) = A + B + C + R
330: 
331:                                                   7
332: where R is an effective divisor with degree 2d2 − 2g − 2δ. The linear space H2d (−C − R − ω)
333: has dimension at least 1. We pick a non-zero form f2 in it. It has divisor (f2 ) = C + R + ω + D
334: where D is effective with degree g. And D − ω is linearly equivalent to A − ω + B − ω.
335:     In order to invert the class α of A − ω we pick a non-zero form f1 in H2d (−C − 2ω). The
336: divisor of f1 is (f1 ) = 2ω + C + R where R is an effective divisor with degree 2d2 − 2g − 2δ.
337: The linear space H2d (−C − R − A) has dimension at least 1. We pick a non-zero form f2 in it.
338: It has divisor (f2 ) = C + R + A + B where B is effective with degree g. And B − ω is linearly
339: equivalent to −(A − ω).
340:     This algorithm works just as well if we replace C by some D ≥ C having polynomial degree
341: in d.
342: 
343: Lemma 1 (Arithmetic operations in the jacobian) Let C/Fq be a degree d plane projective
344: absolutely irreducible reduced curve. Let g be the geometric genus of C. Assume we are given
345: the smooth model X of C and a Fq -divisor with degree g on X , denoted ω. We assume ω is given
346: as a difference between two effective divisors with degrees bounded by a polynomial in d. This ω
347: serves as an origin. Arithmetic operations in the Picard group Pic0 (X /Fq ) can be performed in
348: time polynomial in log q and d. This includes addition, substraction and comparison of divisor
349: classes.
350: 
351:     If ω is not effective, we use lemma 2 below to compute a non-zero function f in L(ω) and
352: we write ω ′ = (f ) + ω. This is an effective divisor with degree g. We replace ω by ω ′ and finish
353: as in the paragraph before lemma 1                                                               ✷
354:     We now recall the principle of the Brill-Noether algorithm for computing complete linear
355: series. Functions in Fq (X ) are represented as quotients of forms.
356: 
357: Lemma 2 (Brill-Noether) There exists an algorithm that on input a degree d plane projective
358: absolutely irreducible reduced curve C/Fq and the smooth model X of C and two effective Fq -
359: divisors A and B on X , computes a basis for L(A − B) in time polynomial in d and log q and
360: the degrees of A and B.
361: 
362:     We assume deg(A) ≥ deg(B), otherwise L(A − B) = 0. Let a be the degree of A. We let h
363: be the smallest integer such that h ≥ 2d and hd + g + 1 > a + (d − 1)(d − 2).
364:     So the space Hh (−C − A) is non-zero. It is contained in the image of the restriction map
365: ρ : Sh → Hh so that we can represent it as a subspace of Sh . We pick a non-zero form f in
366: Hh (−C − A) and compute its divisor (f ) = C + A + D.
367:     The space Hh (−C − B − D) is contained in the image of the restriction map ρ : Sh → Hh
368: so that we can represent it as a subspace of Sh . We compute forms γ1 , γ2 , ..., γk in Sh such that
369: their images by ρ provide a basis for Hh (−C − B − D). A basis for L(A − B) is made of the
370: functions γf1 , γf2 , ..., γfk . Again this algorithm works just as well if we replace C by some D ≥ C
371: having polynomial degree in d.                                                                       ✷
372:     We deduce an explicit moving lemma for divisors.
373: 
374: Lemma 3 (Moving divisor lemma I) There exists an algorithm that on input a degree d plane
375: projective absolutely irreducible reduced curve C/Fq and the smooth model X of C and a degree
376: 
377:                                                   8
378: zero Fq -divisor D = D + − D − and an effective divisor A with degree < q on X computes a
379: divisor E = E + − E − linearly equivalent to D and disjoint to A in time polynomial in d and
380: log q and the degrees of D + , and A. Further the degree of E + and E − can be taken to be ≤ 2gd.
381: 
382:     Let O be an Fq -rational divisor on X such that 1 ≤ deg(O) ≤ d and disjoint to A. We may
383: take O to be a well chosen fiber of some plane coordinate function on X . We compute the linear
384: space L = L(D + − D − + 2gO). The subset of functions f in L such that (f ) + D + − D − + 2gO
385: is not disjoint to A is contained in a union of at most deg(A) < q hyperplanes. We conclude
386: invoking lemma 4 below.                                                                      ✷
387:     There remains to state and prove the
388: 
389: Lemma 4 (Solving inequalities) Let q be a prime power, d ≥ 2 and n ≥ 1 two integers and let
390: H1 , ..., Hn be hyperplanes inside V = Fdq , each given by a linear equation.
391:                                                                     S         Assume n < q. There
392: exists a deterministic algorithm that finds a vector in U = V − 1≤k≤n Hk in time polynomial
393: in log q, d and n.
394: 
395:     This is proved by lowering the dimension d. For d = 2 we pick any affine line
396:                                                                                 S L in V not
397: containing the origin. We observe that there are at least q−n points in U∩L = L− 1≤k≤n L∩Hk .
398: We enumerate points in L until we find one which is not in any Hk . This requires at most n + 1
399: trials.
400:     Assume now d is bigger than 2. Hyperplanes in V are parametrized by the projective space
401: P(V̂ ) where V̂ is the dual of V . We enumerate points in P(V̂ ) until we find a hyperplane K
402: distinct from every Hk . We compute a basis for K and an equation for every Hk ∩ K in this
403: basis. This way, we have lowered the dimension by 1.                                         ✷
404:     We can strengthen a bit the moving divisor algorithm by removing the condition that A has
405: degree < q. Indeed, in case this condition is not met, we call α the smallest integer such that
406: q α > deg(A) and we set β = α + 1. We apply lemma 3 after base change to the field with q α
407: elements and find a divisor Eα . We call eα the norm of Eα from Fqα to Fq . It is equivalent to
408: αD. We similarly construct a divisor eβ that is equivalent to (α + 1)D. We return the divisor
409: E = eβ − eα . We observe that we can take α ≤ 1 + logq deg(A) so the degree of the positive
410: part E + of E is ≤ 6gd(logq (deg(A)) + 1).
411: 
412: Lemma 5 (Moving divisor lemma II) There exists an algorithm that on input a degree d plane
413: projective absolutely irreducible curve C/Fq and the smooth model X of C and a degree zero
414: Fq -divisor D = D + − D − and an effective divisor A on X computes a divisor E = E + − E −
415: linearly equivalent to D and disjoint to A in time polynomial in d and log q and the degrees of
416: D + , and A. Further the degree of E + and E − can be taken to be ≤ 6gd(logq (deg(A)) + 1).
417: 

LINES 575-665
575:                                                    12
576: 5 Pairings
577: Let n be a prime to p integer and J a jacobian variety over Fq . The Weil pairing relates the full
578: n-torsion subgroup J (F̄q )[n] with itself. It can be defined using Kummer theory and is geometric
579: in nature. The Tate-Lichtenbaum-Frey-Rück pairing is more cohomological and relates the n-
580: torsion J (Fq )[n] in the group of Fq -rational points and the quotient J (Fq )/nJ (Fq ). In this
581: section, we quickly review the definitions and algorithmic properties of these pairings, following
582: work by Weil, Lang, Menezes, Okamoto, Vanstone, Frey and Rück.
583:     We first recall the definition of Weil pairing following [20]. Let k be an algebraically closed
584: field with characteristic p. For every abelian variety A over k, we denote by Z0 (A)0 the group
585: of 0-cycles with degree 0 and by S : Z0 (A)0 → A the summation map, that associates to every
586: 0-cycle of degree 0 the corresponding sum in A.
587:     Let V and W be two projective non-singular irreducible and reduced varieties over k, and let
588: α : V → A and β : W → B be the canonical maps into their Albanese varieties. Let D be a
589: correspondence on V × W . Let n ≥ 2 be a prime to p integer. Let a (resp. b) be a 0-cycle of
590: degree 0 on V (resp. W ) and let a = S(α(a)) (resp. b = S(β(b))) be the associated point in A
591: (resp. B). Assume na = nb = 0. The Weil pairing en,D (a, b) is defined in [20, VI, §4, Theorem
592: 10]. It is an n-th root of unity in k. It depends linearly in a, b and D.
593:     Assume V = W = X is a smooth projective irreducible and reduced curve over k and
594: A = B = J is its jacobian and α = β = f : X → J is the Jacobi map (once an origin on X
595: has been chosen). If we take D to be the diagonal on X × X we define a pairing en,D (a, b) that
596: will be denoted en (a, b) or en,X (a, b). It does not depend on the origin for the Jacobi map. It is
597: non-degenerate.
598:     The jacobian J is principally polarized. We have an isomorphism λ : J → Jˆ between J
599: and its dual Jˆ. If α is an endomorphism α : J → J , we denote by t α its transpose t α : Jˆ → Jˆ.
600: If D is a divisor on J that is algebraically equivalent to zero, the image by t α of the linear
601: equivalence class of D is the linear equivalence class of the inverse image α−1 (D). See [20, V,
602: §1]. The Rosati dual of α is defined to be α∗ = λ−1 ◦ t α ◦ λ. The map α → α∗ is an involution,
603: and α∗ is the adjoint of α for the Weil pairing
604: 
605:                                   en,X (a, α(b)) = en,X (α∗ (a), b)                              (1)
606: according to [20, VII, §2, Proposition 6].
607:     If Y is another smooth projective irreducible and reduced curve over k and K its jacobian
608: and φ : X → Y a non-constant map with degree d, and φ∗ : K → J the associated map between
609: jacobians, then for a and b of order dividing n in K one has en,X (φ∗ (a), φ∗ (b)) = en,Y (a, b)d .
610:     The Frey-Rück pairing can be constructed from the Lichtenbaum version of Tate’s pairing
611: [22] as was shown in [14]. Let q be a power of p. Let again n ≥ 2 be an integer prime to p
612: and X a smooth projective absolutely irreducible reduced curve over Fq . Let g be the genus of
613: X . We assume n divides q − 1. Let J be the jacobian of X . The Frey-Rück pairing {, }n :
614: J (Fq )[n] × J (Fq )/nJ (Fq ) → F∗q /(F∗q )n is defined as follows. We take a class of order dividing
615: n in J (Fq ). Such a class can be represented by an Fq -divisor D with degree 0. We take a class in
616: J (Fq ) and pick a degree zero Fq -divisor E in this class, that we assume to be disjoint to D. The
617: 
618:                                                  13
619: pairing evaluated at the classes [D] and [E] mod n is {[D], [E] mod n}n = f (E) mod (F∗q )n
620: where f is any function with divisor nD. This is a non-degenerate pairing.
621:     We now explain how one can compute the Weil pairing, following work by Menezes, Okamo-
622: to, Vanstone, Frey and Rück. The Tate-Lichtenbaum-Frey-Rück pairing can be computed simi-
623: larly.
624:     As usual, we assume we are given a degree d plane model C for X . Assume a and b have dis-
625: joint support (otherwise we may replace a by some linearly equivalent divisor using the explicit
626: moving lemma 3.) We compute a function φ with divisor na. We similarly compute a function
627: ψ with divisor nb. Then en (a, b) = ψ(a)
628:                                        φ(b)
629:                                             . This algorithm is polynomial in the degree d of C and
630: the order n of the divisors, provided the initial divisors a and b are given as differences between
631: effective divisors with polynomial degree in d.
632:     Using an idea that appears in a paper by Menezes, Okamoto and Vanstone [24] in the context
633: of elliptic curves, and in [14] for general curves, one can make this algorithm polynomial in log n
634:                                                      −                 −
635: in the following way. We write a = a0 = a+                      +
636:                                                0 − a0 where a0 and a0 are effective divisors. Let φ
637:                                                                                               −
638: be the function computed in the above simple minded algorithm. One has (φ) = na+        0 − na0 . We
639: want to express φ as a product of small degree functions. We use a variant of fast exponentiation.
640:                                                          −
641: Using lemma 3 we compute a divisor a1 = a+        1 − a1 and a function φ1 such that a1 is disjoint
642:                                                                      −
643: to b and (φ1 ) = a1 − 2a0 and such that the degrees of a+   1 and a1 are ≤ 6gd(logq (deg(b)) + 1).
644:                                                                            −
645: We go on and compute, for k ≥ 1 an integer, a divisor ak = a+        k − ak and a function φk such
646:                                                                                                −
647: that ak is disjoint to b and (φk ) = ak − 2ak−1 and such that the      P degrees  of a+k and ak are
648:                                                                              k
649: ≤ 6gd(logq (deg(b)) + 1). We write the  P base 2 expansion of n = i ǫk 2 with ǫk ∈ {0, 1}. We
650: compute the function Ψ with divisor k ǫk ak . We claim that the function φ can be written as a
651: product of the φk , for k ≤ log2 n, and Ψ with suitable integer exponents bounded by n in absolute
652: value. QIndeed we write µ1 = φ1 , µ2 = φ2 φ21 , µ3 = φ3 φ22 φ41 and so on. We have (µk ) = ak − 2k a
653: and Ψ k µk−ǫk has divisor na so is the φ we were looking for.
654: 
655: Lemma 10 (Computing the Weil pairing) There exists an algorithm that on input an integer
656: n ≥ 2 prime to q and a degree d absolutely irreducible reduced plane projective curve C over
657: Fq and its smooth model X and two Fq -divisors on X , denoted a = a+ − a− and b = b+ − b− ,
658: with degree 0, and order dividing n in the jacobian, computes the Weil pairing en (a, b) in time
659: polynomial in d, log q, log n and the degrees of a+ , a− , b+ , b− , the positive and negative parts of
660: a and b.
661: 
662: Lemma 11 (Computation of Tate-Lichtenbaum-Frey-Rück pairings) There exists an algo-
663: rithm that on input an integer n ≥ 2 dividing q − 1 and a degree d absolutely irreducible
664: reduced plane projective curve C over Fq and its smooth model X and two Fq -divisors on X ,
665: denoted a = a+ − a− and b = b+ − b− , with degree 0, and such that the class of a has order
