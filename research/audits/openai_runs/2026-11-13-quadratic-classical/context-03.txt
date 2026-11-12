# Actual odd-degree Selmer identification and finite-place reduction
Source https://www.impan.pl/shop/en/publication/transaction/download/product/83397
Retained local_kummer_cluster/stoll_2descent.pdf; see source.json for PDF hash.

Physical lines214-253

214: which we call ∞. This point is in C(Q).
215:    For a field extension K of Q, let
216:                                      × 2        × 2
217:                  HK = ker(NK : L×           ×
218:                                 K /(LK ) → K /(K ) ).
219: 
220: This fairly concrete group will replace the rather abstract group H 1 (K, J[2]).
221:     Let Div0⊥ (C) denote the group of degree zero divisors on C with support
222: disjoint from the support of the principal divisor div(y). Then for every K
223: 250                                    M. Stoll
224: 
225: we get a homomorphism
226:                                            X                Y
227:            FK : Div0⊥ (C)(K) → L×
228:                                 K,                nP P 7→       (x(P ) − θ)nP ,
229:                                             P               P
230: which induces a homomorphism
231:                                 δK : J(K) → HK
232: with kernel 2J(K). The induced map J(K)/2J(K) → HK will also be
233: denoted by δK .
234:     Lemma 4.1. The assignments K 7→ J(K)/2J(K), K 7→ HK and K 7→
235:   1
236: H (K, J[2]) are functors from the category of field extensions of Q into the
237:                                                                           ∼
238:                                                                           =
239: category of F2 -vector spaces. There is a natural isomorphism ιK : HK −→
240: H 1 (K, J[2]). The maps δK give a natural injection J(K)/2J(K) ,→ HK ,
241: and ιK ◦ δK equals the coboundary morphism J(K)/2J(K) → H 1 (K, J[2]).
242:       Proof. This is proved in [16].
243:    This gives us the following characterisation of the Selmer group. Recall
244: that H = HQ according to our convention.
245:     Proposition 4.2. The 2-Selmer group of J over Q can be identified as
246: follows:
247:          Sel(2) (Q, J) = {ξ ∈ H | resv (ξ) ∈ δv (J(Qv )) for all v}.
248: Here, resv denotes the canonical “restriction” map H → Hv , induced by
249: functoriality from the inclusion Q ,→ Qv .
250:    In order to make this practical, we have to reduce the set of places that
251: have to be considered to a finite set. This requires some preparations. The
252: reader who is only interested in the resulting algorithm can safely proceed
253: to Corollary 4.7.

Physical lines374-410

374:    Corollary 4.7. Let S = {∞, 2} ∪ {p | p2 divides disc(f )}. Then
375:    Sel(2) (Q, J) = {ξ ∈ H | val(ξ) ∈ IS (L)/IS (L)2 ,
376:                                        resv (ξ) ∈ δv (J(Qv )) for all v ∈ S}.
377:    This suggests the following strategy:
378: (1) Find the set S.
379: (2) For each v ∈ S, determine Jv = δv (J(Qv )) ⊂ Hv .
380: (3) Determine a suitable finite subgroup H e of L× /(L× )2 that contains the
381:     Selmer group and find a basis of e H.
382:                  (2)                              Q
383: (4) Compute Sel (Q, J) as the inverse image of v∈S Jv under
384:                             Y               Y
385:                                         e →
386:                                  resv : H       Hv .
387:                                v∈S               v∈S
388: 
389:    We will consider each of the steps in turn.
390:     Step (1). We must compute the discriminant of f and factor it. Since
391: we have to factor f anyway in order to find the splitting of L into fields, we
392: may do that first and then find the bad primes from the product formula
393: for disc(f ) in terms of the discriminants and resultants of the factors. In
394: practice, f will often be irreducible, and this simplification cannot be used.
395: Another possible simplification is that we only need primes that occur at
396: least twice in the factorisation. This means that we can split off “small”
397: primes first. If d is the remaining factor, we check if d √ is a square. If it is
398:                                                             3
399: not, it will suffice to
400:                       √ find all prime factors of d below     d, and if it is, we
401: only have to factor d. I do not know if one can get a measurable speedup
402: this way. The current implementation simply factors the discriminant.
403:     Step (2). The reason for doing this step before step (3) is that the
404: knowledge of the Jv allows us to find a smaller bounding group H   e in the
405: third step. For example, if it turns out that Jp = ker(valp ) for some odd
406: p ∈ S, then we can drop p from S altogether.
407:     Hence we can subdivide this step.
408: (2.1) For all p ∈ S \ {∞}, compute Jp = δp (J(Qp )) and its image Gp =
409:       valp (Jp ) in Ip .
410: (2.2) Remove from S all odd p with Gp = 0.

Physical lines476-522

476: (3.2.1) Put the results of step (2.1) together to produce a basis of G.
477: (3.2.2) Compute the image of this basis in Cl(L)/2Cl(L) and find a basis of
478:         the kernel W of the map G → Cl(L)/2Cl(L).
479: (3.2.3) For each element aI(L)2 of this basis of W , find some ideal b ∈ I(L)
480:         such that ab2 is principal, and take a generator of ab2 as an element
481:         of the basis of e
482:                         H.
483:     The image of a in Cl(L) is needed in step (3.2.3) to find b.
484:     Once we know the class groups, we can give an upper bound for the
485: Selmer group dimension without having to find generators for principal ide-
486: als and without having to compute the fundamental units of the number
487: fields involved. (Both of these tasks tend to require much more computa-
488: tional effort than the determination of the class group alone for fields of
489: medium complexity.) We only need to find the ideal class an ideal belongs
490: to and to know the unit rank of the number fields, which is determined by
491: the signature.
492:    Lemma 4.10. We have the following bound on the Selmer group dimen-
493: sion:
494:  dim Sel(2) (Q, J) ≤ m∞ + dim Cl(L)[2] + dim ker(G → Cl(L)/2Cl(L)) − 1.
495:   Proof. The sum of the numbers of real and pairs of conjugate complex
496: embeddings of all the number fields Lj equals m∞ . By Lemma 4.9, we have
497:                     ×    × 2
498:        dim V = dim OL /(OL ) + dim Cl(L)[2] = m∞ + dim Cl(L)[2].
499:                       e we see that the bound given is just one less than
500: By the definition of H,
501: its dimension. Since Gp lies in the kernel of the norm map to Ip (Q)/Ip (Q)2 ,
502: the norm map on L× /(L× )2 maps H    e into h−1i ⊂ Q× /(Q× )2 . Since −1 ∈ H
503:                                                                            e
504: and N (−1) = −1, this implies that
505:                             e → Q× /(Q× )2 ) = dim H
506:                 dim ker(N : H                      e − 1.
507:                                                         e whence the
508: But the Selmer group is contained in the kernel of N on H,
509: claim.
510: 256                                M. Stoll
511: 
512:     Note that for the computation of ker(G → Cl(L)/2Cl(L)), we only need
513: to find the images of various prime ideals in the ideal class group, whereas
514: in order to find an actual basis of H,   e we must find the units, and we
515: must determine generators for principal ideals. We can of course bound
516: dim ker(G → Cl(L)/2Cl(L)) by dim G, if we even want to avoid the compu-
517: tation of images in the class group.
518:     Suppose that we already have got a lower bound l on the Mordell–Weil
519: rank. We might have found a number of independent points on J, for exam-
520:                                        e = l+dim J(Q)[2]+1, the computation
521: ple. If at this point, we see that dim H
522: can be stopped, since ker(N |H  f) must be the Selmer group, and the rank must
