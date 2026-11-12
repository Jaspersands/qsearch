Source: research/audits/sources/surface_module_2026/couveignes_edixhoven_book.txt
SHA256: 0ae7a4befba82ce944abeb0f71f745403bcbb9c8418232d050c8e6effba83dd9
Physical newline ranges; PDF extraction may lose glyphs.

LINES 8970-9065
8970:                        1                           X
8971:   h.bl .Qx;i //            .Qx;i ; bl 1/X C l 2     sup g
8972:                     ŒK W Q                          X
8973:                                                              !
8974:                               1X                               1
8975:                                       Z
8976:                             C             log.jbl j2 C 1/X C log 2 :
8977:                               2  X                           2
8978: 
8979: Here  runs through the embeddings of K into C and g is the Arakelov-
8980: Green function on Xl; .
8981: 
8982: In the next chapters we shall derive bounds that are polynomial in l for all
8983: terms in the above estimate.
8984:    Theorem 9.1.1 will be derived from Theorem 9.1.3 below, which states
8985: a fairly general result. We start with a definition. Let K be a number field
8986:                  1                                              1
8987: and consider PO    K
8988:                      . Let 1 denote the OK -point .1 W 0/ of PO   K
8989:                                                                     . For any
8990:                 1
8991: section P in POK .OK / we define by .P; 1/P 1 the degree (see (4.3.1)) of
8992: P  OP 1 .1/, where OP 1 .1/ has the Fubini-Study metric, that is, the metric
8993: k  kP 1 given by
8994: 
8995:                                                    jx1 j
8996: .9:1:2/             k1kP 1 .x0 W x1 / WD
8997:                                            .jx0 j2 C jx1 j2 /1=2
8998: 
8999:       1
9000: over PC . Here 1 is the tautological section of OP 1 .1/.
9001: 
9002: 
9003: 9.1.3 Theorem Let X be a geometrically irreducible, smooth, and com-
9004: plete curve of positive genus over a number field K, and let X be a proper
9005: semistable model of X over the ring of integers OK of K. Suppose that we
9006: have a nonconstant morphism f W X ! PK1 and a K-rational point Q of X
9007: with f .Q/ ¤ 1. Write the divisor div.f / of f as div.f /C div.f / , with
9008: div.f /C and div.f / effective and without common irreducible compo-
9009: nents. Assume that the Zariski closure of Supp.div.f /C / [ Supp.div.f / /
9010: in X is étale over OK . For any closed point s of Spec.OK /, denote by
9011: ms .f / the supremum of the multiplicities of div.f / on X along the irre-
9012:                         bookcourant     January 8, 2011
9013: 
9014: 
9015: 
9016: 
9017: APPLYING ARAKELOV THEORY                                                         189
9018: 
9019: ducible components of the fiber at s of X . Then we have the inequality
9020:                                           X
9021: .f .Q/; 1/P 1 .Q; f  1/X C deg f             sup g
9022:                                               X
9023:                      1X
9024:                          Z                      X
9025:                    C        log.jf j2 C 1/X C   ms .f / log #k.s/ :
9026:                      2  X                     s
9027: 
9028: Here the first sum runs over the embeddings of K into C, and the last sum
9029: runs over the closed points of Spec.OK /.
9030: 
9031: 
9032: Proof Note that the locus of indeterminacy of f on X consists of finitely
9033: many closed points. This implies that there exists a blow-up XQ ! X of X
9034: such that f extends to a regular map f W XQ ! PO   1
9035:                                                      K
9036:                                                        . For any such XQ we
9037: have by construction
9038: 
9039:               .f .Q/; 1/P 1 D deg f .Q/ .OP 1 .1/; k  kP 1 /
9040:                               D deg Q f  .OP 1 .1/; k  kP 1 /
9041:                               D deg Q .OXQ .f  1/; k  kP 1 / ;
9042: 
9043: where we write 1 to emphasize that f  1 is the inverse image under f of
9044: 1.Spec.OK //, and not the Zariski closure f  1 of the inverse image under
9045: f of 1.Spec.K//. If we let k  kX denote the canonical Arakelov metric on
9046: OX .f  1/ then we can write
9047: 
9048:                                                                     k  kP 1
9049:  deg Q .OXQ .f  1/; k  kP 1 / D deg Q .OXQ .f  1/; k  kX              /
9050:                                                                     k  kX
9051:                                 D deg Q .OXQ .f  1/; k  kX /
9052:                                       X         k  kP 1
9053:                                           log..          /.Q //
9054:                                        
9055:                                                 k  kX
9056:                                                    X         k  kX
9057:                                 D .Q; f  1/XQ C       log..           /.Q // :
9058:                                                     
9059:                                                              k  k P 1
9060: 
9061: 
9062: 
9063: A bound for log..k  kX =k  kP 1 /.Q // follows by testing on the tautological
9064: section 1, giving
9065: 

LINES 9347-9600
9347: 9.2 CONTROLLING Dx D0
9348: 
9349: In this subsection, the hypotheses are as follows (unless stated otherwise).
9350: We let K be a number field, OK its ring of integers, B WD Spec.OK /,
9351: pW X ! B a regular, split semistable curve over B whose generic fiber
9352: X ! Spec K is geometrically irreducible and of genus g  1. We let D be
9353: the closure in X of an effective divisor of degree g (also denoted D) on X .
9354:                       bookcourant     January 8, 2011
9355: 
9356: 
9357: 
9358: 
9359: 196                                                                  CHAPTER 9
9360: 
9361: We let x be a K-rational torsion point of the Jacobian of X, that is, a torsion
9362: element of Pic.X /, which has the property that there is a unique effective
9363: divisor Dx on X such that x D ŒDx D. Finally, we let P W B ! X be a
9364: section of p, that is, an element of X .B/.
9365:    We denote by ˆx;P the unique finite vertical fractional divisor ˆ (that
9366: is, with rational coefficients that are not necessarily integral) on X such that
9367: .Dx D ˆ; C / D 0 for all irreducible components C of fibers of p,
9368: and such that P .B/ is disjoint from the support of ˆ. It is not difficult
9369: to see that a ˆ satisfying the first condition exists and that it is unique up
9370: to adding multiples of fibers of p (the intersection pairing restricted to the
9371: divisors with support in a fiber is negative semidefinite); see Lemme 6.14.1
9372: of [Mor2]. The second condition removes the ambiguity of adding multiples
9373: of fibers.
9374:    We denote by ıs the number of singular points in the geometric fiber at a
9375: closed point s of B.
9376: 
9377: 9.2.1 Theorem The OB -module R1 p OX .Dx / is a torsion module on B,
9378: and we have:
9379:                                  1                   1X
9380: .Dx ; P / C log #R1 p OX .Dx / C .!X =B ; !X =B / C     ıs log #k.s/
9381:                                  8                   8 s
9382:                 1                                1
9383:       D .D; P /    .D C ˆx;P ; D C ˆx;P !X =B / C deg det p !X =B
9384:                 2                                2
9385:             XZ                               g
9386:           C         log k#k.Dx Q/   .Q/ C ŒK W Q log.2/:
9387:                X 
9388:                                              2
9389: Here s runs over the closed points of B, and  runs through the complex
9390: embeddings of K.
9391: 
9392: We derive Theorem 9.2.1 from three lemmas. For the moment we work
9393: in Q ˝Z Pic.X
9394:          c /.
9395: 
9396: 9.2.2 Lemma The admissible line bundles
9397: 
9398:          OX .Dx D/ ˝ p  P  OX .Dx D/_            and    OX .ˆx;P /
9399: 
9400: are numerically equivalent. That is, for any admissible line bundle F on X
9401: we have
9402: 
9403:       .OX .Dx     D/ ˝ p  P  OX .Dx      D/_ ; F / D .OX .ˆx;P /; F /:
9404:                         bookcourant     January 8, 2011
9405: 
9406: 
9407: 
9408: 
9409: APPLYING ARAKELOV THEORY                                                    197
9410: 
9411: Proof In this proof we just write ˆ for ˆx;P . We denote the first line
9412: bundle in the lemma by ‰. Since Dx D is torsion, there is a positive
9413: integer N such that ‰ ˝N is trivial on the generic fiber as a classical line
9414: bundle (that is, without taking the metrics into account). We have a canoni-
9415: cal isomorphism P  ‰ Q! OB on B. Combining, we find that ‰ ˝N has a
9416: rational section s with divX .s/ vertical and P  s 7! 1. The latter condition
9417: implies that P intersects to zero with divX .s/ for the Arakelov intersection
9418: product. On the other hand, as p  P  OX .Dx D/_ is trivial on the fibers
9419: of p over finite places of B, we have .N.Dx D/ divX .s/; C / D 0 for
9420: all irreducible components C of fibers of p. Hence in fact ˆ D N1 divX .s/.
9421: To prove the lemma, it suffices now to prove that ‰ ˝N Q! OX .divX .s//
9422: given by s 7! 1, with 1 the tautological section, is an isometry. Because
9423: of admissibility, it suffices to check that this is so when restricted to P ; but
9424: here we get the canonical isomorphism P  ‰ Q! OB . This is indeed an
9425: isometry by the definition of ‰.                                               
9426: 
9427: 9.2.3 Lemma Let X be a compact Riemann surface of genus g  1. Let
9428: D be an effective divisor on X of degree g satisfying h0 .D/ D 1. Then the
9429: determinant of cohomology .OX .D// is identified with H 0 .X; OX .D//.
9430: Further, the formula
9431:                       ı.X /
9432:                               Z
9433:            log k1k C        C    log k#k.D Q/  X .Q/ D 0
9434:                         8      X
9435: holds for the length (with respect to Faltings’ metrization of the determinant
9436: of cohomology) of the tautological section 1 of H 0 .X; OX .D//.
9437: 
9438: Proof Since h0 .D/ D 1, H 0 .X; OX .D// D C. Therefore, the set of
9439: points Q on X such that h0 .D Q/ > 0 is the support of D. Let Q be
9440: a point outside the support of D. Then h0 .D Q/ D 0. According to
9441: the axioms for the metrization of the determinant of cohomology, the exact
9442: sequence
9443: 
9444:            0 ! OX .D        Q/ ! OX .D/ ! Q Q OX .D/ ! 0
9445: 
9446: gives rise to an isometry
9447: 
9448:   .OX .D// Q! .OX .D           Q// ˝ Q OX .D/
9449:                                    Š O. ‚/ŒOX .D          Q/ ˝ Q OX .D/:
9450:                       bookcourant     January 8, 2011
9451: 
9452: 
9453: 
9454: 
9455: 198                                                                   CHAPTER 9
9456: 
9457: Taking the norm on left and right of a tautological section we obtain, us-
9458: ing (4.4.6),
9459: 
9460:             k1k D exp. ı.X /=8/  k#k.D            Q/ 1  G.D; Q/;
9461: 
9462: where log G.D; Q/ D gD;X .Q/. Taking logarithms and then integrating
9463: against X .Q/ gives the result.                                   
9464: 
9465: 9.2.4 Lemma (Noether formula) We have
9466:                                                X
9467:   12 deg det p !X =B D .!X =B ; !X =B / C          ıs log #k.s/
9468:                                                s
9469:                                            X
9470:                                        C       ı.X /     4gŒK W Q log.2/ ;
9471:                                            
9472: 
9473: the first sum running over the closed points of B, the second sum running
9474: over the complex embeddings of K.
9475: 
9476: Proof See [Fal1] and [Mor3].                                                      
9477: 
9478: Proof [Proof of Theorem 9.2.1] We first show that R1 p OX .Dx / is a tor-
9479: sion module. As it is a coherent OB -module, it suffices to show that it is zero
9480: on the generic point of B, that is, that H1 .X; OX .Dx // is zero. By Riemann-
9481: Roch, we have h0 .Dx / h1 .Dx / D 1. By definition of Dx , we have
9482: OX .Dx / Š Lx .D/. And by construction of D, we have h0 .Lx .D// D 1.
9483: This shows that h1 .Dx / D 0.
9484:    Let us now prove the identity in Theorem 9.2.1. We start by noting that,
9485: by (4.4.7)
9486: 
9487:                    .Dx    D; P / D deg P  OX .Dx         D/:
9488: 
9489: By Lemma 9.2.2, OX .Dx / ˝ p  P  OX .Dx D/_ and OX .D C ˆx;P /
9490: are numerically equivalent. The Riemann-Roch theorem then gives
9491: 
9492:   deg det Rp .OX .Dx / ˝ p  P  OX .Dx        D/_ /
9493:                 1
9494:              D .D C ˆx;P ; D C ˆx;P                !X =B / C deg det p !X =B :
9495:                 2
9496:                            bookcourant          January 8, 2011
9497: 
9498: 
9499: 
9500: 
9501: APPLYING ARAKELOV THEORY                                                          199
9502: 
9503: By the projection formula for the determinant of cohomology we can write
9504: the left-hand side as
9505: 
9506:   deg det Rp .OX .Dx / ˝ p  P  OX .Dx               D/_ /
9507:                            D deg det Rp OX .Dx /           deg P  OX .Dx     D/ :
9508: 
9509: Since p OX .Dx / is canonically trivialized by the function 1, we have
9510:                                  X
9511:       deg det Rp OX .Dx / D          log k1k log #R1 p OX .Dx /;
9512:                                        
9513: 
9514: where for each complex embedding , the norm k1k is the length of the
9515: tautological section 1 of .OX .Dx // D H 0 .OX .Dx //. By Lemma 9.2.3
9516: we can then write
9517:                               XZ
9518:       deg det Rp OX .Dx / D           log k#k .Dx Q/   .Q/
9519:                                           X
9520:                                        X
9521:                                   C         ı.X /=8      log #R1 p OX .Dx / :
9522:                                        
9523: 
9524: Combining everything gives
9525:                      1
9526: .Dx     D; P / D       .D C ˆx;P ; D C ˆx;P !X =B / deg det p !X =B
9527:                      2 Z
9528:                      X
9529:                    C        log k#k.Dx Q/   .Q/
9530:                             X
9531:                        X
9532:                    C        ı.X /=8       log #R1 p OX .Dx / :
9533:                        
9534:                                                                P
9535: We obtain the required formula upon eliminating                    ı.X /=8 with the
9536: Noether formula, Lemma 9.2.4.                                                         
9537: 
9538: 9.2.5 Theorem We have an upper bound
9539:                                          1
9540: .Dx ; P / C log #R1 p OX .Dx /           .D; D !X =B /
9541:                                          2 X
9542:                                        C 2g 2   ıs log #k.s/
9543:                                                     s2B
9544:                                             X                        g
9545:                                        C            log k#k;sup C     ŒK W Q log.2/
9546:                                                 
9547:                                                                      2
9548:                                         1
9549:                                        C deg det p !X =B C .D; P / ;
9550:                                         2
9551:                       bookcourant     January 8, 2011
9552: 
9553: 
9554: 
9555: 
9556: 200                                                                       CHAPTER 9
9557: 
9558: where s runs through the closed points of B, and where the supremum norm
9559: k#k;sup is taken over Picg 1 .X /.
9560: 
9561: The required upper bound follows directly from Theorem 9.2.1 by using
9562: Lemma 9.2.6 below and the fact that .!X =B ; !X =B /  0 (see Theorem 5
9563: of [Fal1]).
9564: 
9565: 9.2.6 Lemma We have an upper bound
9566: 
9567:       1
9568:         .D C ˆx;P ; D C ˆx;P        !X =B /
9569:       2
9570:                                 1                              X
9571:                                  .D; D       !X =B / C 2g 2         ıs log #k.s/ ;
9572:                                 2
9573:                                                                s2B
9574: 
9575: with s running through the closed points of B.
9576: 
9577: Proof In this proof we just write ˆ for ˆx;P . By the definition of ˆ, we
9578: have .Dx D ˆ; ˆ/ D 0, or, in other words, .ˆ; ˆ/ D .Dx D; ˆ/.
9579: Using this we can write
9580:   1                               1                   1
9581:     .DCˆ; DCˆ !X =B / D             .D; D !X =B /C .ˆ; !X =B D Dx / :
9582:   2                               2                   2
9583:                   P
9584: We write ˆ D         C ˆ.C /  C , and for any finite fiber Fs of p we put
9585: As WD supC jˆ.C /j with C running through the irreducible components
9586: of Fs . Since !X =B ; D and Dx intersect any irreducible component C with
9587: non-negative multiplicity, we find
9588:                                                                    !
9589:         1                           1 X
9590:           .ˆ; !X =B D Dx /                As Fs ; !X =B C D C Dx
9591:         2                           2 s
9592:                                       X
9593:                                  2g      As log #k.s/ :
9594:                                           s
9595: 
9596: We are going to prove that As  gıs , and then we are done. So let s be a
9597: finite place of B. Let S0 be the set of irreducible components of Fs , and let
9598: S1 be the set of double points on Fs . Let s be the dual graph of Fs (thus, the
9599: set of vertices of s corresponds to S0 , the set of edges corresponds to S1 ,
9600: and the graph is defined by the incidence relations). Choose an orientation
