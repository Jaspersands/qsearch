Source: research/audits/sources/surface_module_2026/anderson_abeliants.txt
SHA256: b1cd29b28752f5676d331e22d4388763b16bee5e6959f44469e66fc4574d27a4
Physical newline ranges; PDF extraction may lose glyphs.

LINES 1-70
1:                                             ABELIANTS AND THEIR APPLICATION TO AN ELEMENTARY
2:                                                        CONSTRUCTION OF JACOBIANS
3: 
4: 
5: 
6: 
7: arXiv:math/0112321v1 [math.NT] 5 Dec 2001
8:                                                                               GREG W. ANDERSON
9: 
10: 
11: 
12: 
13:                                                     Abstract. The abeliant is a polynomial rule which to each n by n by n + 2
14:                                                     array with entries in a commutative ring with unit associates an n by n matrix
15:                                                     with entries in the same ring. The theory of abeliants, first introduced in
16:                                                     an earlier paper of the author, is simplified and extended here. Now let J
17:                                                     be the Jacobian of a nonsingular projective algebraic curve defined over an
18:                                                     algebraically closed field. With the aid of the theory of abeliants we obtain
19:                                                     explicit defining equations for J and its group law.
20: 
21: 
22:                                                                                 1. Introduction
23:                                                Let C be a nonsingular projective algebraic curve defined over an algebraically
24:                                             closed field k and let J be the Jacobian of C. The point of the paper is to give
25:                                             an elementary construction of J, i. e., to obtain by purely algebraic and relatively
26:                                             simple means explicit defining equations for J and its group law. For histori-
27:                                             cal perspective see [Milne 1986]. Our construction is similar in spirit to that of
28:                                             [Mumford Tata Lectures II], but differs from the latter in (at least) two important
29:                                             respects. Firstly, we need not assume that C is hyperelliptic. Secondly, we obtain
30:                                             a description of J not as a glued-together collection of affine varieties, but rather
31:                                             as a projective variety.
32:                                                Our construction of J is based in large part on the notion of abeliant introduced
33:                                             in the author’s earlier paper [Anderson 1997]. The abeliant is just a polynomial rule
34:                                             which to each n by n by n + 2 array with entries in a commutative ring with unit
35:                                             associates an n by n matrix with entries in the same ring. We simplify and extend
36:                                             the theory of abeliants in this paper (§2). One of the new results obtained here is
37:                                             an expansion of each entry of the abeliant as a sum indexed by four permutations
38:                                             of n letters (§2.8).
39:                                                Our construction of J proceeds in three main stages. The first stage is to de-
40:                                             rive from the theory of abeliants a theory of abstract Abel maps (§3). The first
41:                                             stage is more or less pure multilinear algebra and has a priori nothing to do with
42:                                             algebraic curves. The abstract Abel map is roughly analogous to the Plücker em-
43:                                             bedding, but with this important difference: it collapses not GLn -orbits but rather
44:                                             GLn × GLn -orbits to lines. In the second stage of the construction of J we set up a
45:                                             representation of divisor classes of C of sufficiently high degree by square rank one
46:                                             matrices with entries in the function field of C (§4.2) and then set up correspond-
47:                                             ing matrix representations of addition and subtraction of divisor classes (§4.3).
48:                                             Since the matrix representing a divisor class is well-defined only up to GLn × GLn -
49:                                             equivalence, we have to solve a problem in the invariant theory of GLn × GLn to
50: 
51:                                               Date: This paper has been published.     The journal citation is Advances in Mathematics
52:                                             172(2002), 169–205.
53:                                                                                           1
54: 2                                   GREG W. ANDERSON
55: 
56: 
57: complete the construction of J. Of course it is precisely this sort of problem that
58: the theory of abstract Abel maps is designed to solve. Thus the third and final
59: stage of the construction of J comes down to interpreting the abstract Abel map
60: in certain special cases associated to C as the Abel map (Theorem 4.4.6).
61:     The explicit elementary point of view on hyperelliptic Jacobians developed by
62: Mumford and many others has been quite useful in number theory and com-
63: puter science. To give just two examples of applications, we cite the papers
64: [Flynn Poonen Schaefer 1997] and [Adleman DeMarrais Huang 1999].                The
65: first is a study of the rational points on a certain curve of genus 2 connected with
66: iteration of quadratic polynomials; the second is a cryptologically motivated study
67: of the discrete logarithm problem in Jacobians of hyperelliptic curves defined over
68: finite fields. We expect the explicit elementary point of view on not-necessarily-
69: hyperelliptic Jacobians developed here to be analogously useful. A particularly
70: interesting problem that might be approachable from our point of view is that of

LINES 560-1245
560:    We abstract and refine the part of the theory of [Anderson 1997] having to do
561: with invariants of GLn × GLn .
562: 
563: 3.1. Segre matrices.
564: 
565: 3.1.1. Basic data. Throughout §3 we work with data
566:                                                   k, n, A, L
567: consisting of
568:     • an algebraically closed field k,
569:     • an integer n ≥ 2,
570:     • a finitely generated k-algebra A without zero divisors, and
571:     • a finite-dimensional k-subspace L ⊂ A.
572: Here and below k-algebras are commutative with unit. We often refer to elements
573: of k as constants or scalars.
574: ABELIANTS AND THEIR APPLICATION TO AN ELEMENTARY CONSTRUCTION OF JACOBIANS
575:                                                                          9
576: 
577: 
578: 3.1.2. Matrix terminology. Let X and Y be matrices with entries in a k-algebra R.
579: We                   say                  that                 X                   is
580: k-general if there exists both a row of X with k-linearly independent entries and a
581: column of X with k-linearly independent entries. As in §2, we say that X is of rank
582: ≤ 1 if every two by two submatrix has vanishing determinant. We say that X and
583: Y are k-equivalent if there exist square matrices Φ and Ψ with entries in k such that
584: det Φ 6= 0, det Ψ 6= 0, the product ΦXΨ is defined, and Y = ΦXΨ. Also, given
585: vectors x and y in a common vector space over k, we say that x is k-proportional
586: to y if x = cy for some nonzero scalar c.
587: 
588: 3.1.3. Definition. A Segre matrix X is an object with the following properties:
589:    • X is an n by n matrix with entries in L.
590:    • X is of rank ≤ 1.
591:    • X is k-general.
592: If we need to draw attention to the basic data we say that X is of type (k, n, A, L).
593: 
594: 3.1.4. Key propertries. Let X be a Segre matrix. The following hold:
595:    • Any matrix with entries in A to which X is k-equivalent is a Segre matrix.
596:    • The transpose X T is a Segre matrix.
597:    • There exists a factorization X = uv where u (resp. v) is a column (resp. row)
598:      vector with entries in the fraction field of A.
599:    • Given any such factorization X = uv, the entries of u (resp. v) are
600:      k-linearly independent.
601:    • Given any two such factorizations X = uv = u′ v ′ , there exists unique nonzero
602:      f in the fraction field of A such that u′ = f u and v ′ = f −1 v.
603: The proofs of these facts are very easy and therefore omitted. We take these facts
604: for granted in all subsequent work with Segre matrices.
605: 
606: 3.1.5. Goal. We aim to put the k-equivalence classes of Segre matrices into explicit
607: bijective correspondence with the points of an explicitly defined projective algebraic
608: variety over k. Our results are summarized by Theorem 3.7.6 below.
609: 
610: 3.2. Examples of Segre matrices involving elliptic functions.
611: 
612: 3.2.1. The spaces ΣN . For background on elliptic functions, see [Whittaker Watson,
613: Chap. XX]. Let σ(z) be the Weierstrass σ-function attached to a lattice Λ ⊂ C. By
614: construction σ(z) has simple zeroes on the lattice Λ and no other zeroes. For each
615: nonnegative integer N , let ΣN be the space of entire functions f (z) such that the
616: meromorphic function f (z)/σ(z)N is Λ-periodic. We have Σ0 = C and for N > 0
617: we have dimC ΣN = N .
618:                                                                            L∞
619: 3.2.2. Specification of a type. Fix an integer n ≥ 2. Clearly the
620:                                                                L∞ C-algebra ℓ=0 Σ2nℓ
621: is without zero-divisors. It can be shown that the C-algebra ℓ=0 Σ2nℓ is generated
622: over C by Σ2n . It follows that the quadruple
623:                                          ∞
624:                                                        !
625:                                         M
626: (24)                              C, n,     Σ2nℓ , Σ2n
627:                                       ℓ=0
628: 
629: is a type. We are going to classify Segre matrices of this type.
630: 10                                GREG W. ANDERSON
631: 
632: 
633: 3.2.3. An analytic construction of Segre matrices. Let ~σ (z) be a row vector of length
634: n with entries forming a C-basis of Σn , e. g.
635:                                                                               
636:       ~σ (z) = σ(z)n     σ(z)n ℘(z)    σ(z)n ℘′ (z)  ···      σ(z)n ℘(n−2) (z) ,
637: where
638:                                         d2
639:                                  ℘(z) = −    log σ(z)
640:                                         dz 2
641: is the Weierstrass ℘-function attached to the lattice Λ. It is not difficult to prove
642: that for each t ∈ C the n by n matrix
643: (25)                            ~σ (z − t/n)T ~σ (z + t/n)
644: of entire functions of z is a Segre matrix of type (24) the C-equivalence class of
645: which depends only on t mod Λ, not on the choice of ~σ (z).
646: Proposition 3.2.4. The map sending t ∈ C to the corresponding Segre matrix
647: of the form (25) puts the complex torus C/Λ in bijective correspondence with the
648: family of C-equivalence classes of Segre matrices of type (24).
649: Proof. In any given fundamental domain for Λ a not-identically-vanishing function
650: belonging to the space Σn has exactly n zeroes and moreover these zeroes sum to
651: an element of Λ. Further, the family of functions Σn has no zero in common. Now
652: let X(z) be a matrix C-equivalent to a matrix of the form (25). Then the functions
653: in any given row of X(z) have in any given fundamental domain for Λ exactly n
654: common zeroes, and these must sum to t modulo Λ. Therefore the correspondence
655: in question is one-to-one.
656:    Now fix a Segre matrix X(z) of type (24) arbitrarily. Choose in X(z) a column
657: u(z) and a row v(z), each with C-linearly independent entries. Let f (z) be the
658: entry of X(z) common to u(z) and v(z); then f (z) does not vanish identically. Let
659: p (resp. q) be the number of common zeroes of the entries of u(z) (resp. v(z)) in any
660: given fundamental domain for Λ. Any subspace of Σ2n defined by prescribing n + 1
661: zeroes in a given fundamental domain for Λ is (n − 1)-dimensional over C; this is a
662: consequence of Riemann-Roch in genus one. Since the entries of u(z) (resp. v(z))
663: are C-linearly independent, it follows that p ≤ n (resp. q ≤ n). Since every two by
664: two submatrix of X(z) has vanishing determinant, we have
665:                                 X(z) = u(z)v(z)/f (z),
666: hence f (z) divides every entry of the product u(z)v(z), hence p + q ≥ 2n, hence
667: p = q = n, and hence the common zeroes of the entries of the matrix u(z)v(z)
668: coincide with the zeroes of f (z).
669:    For some complex numbers P1 , . . . , P2n summing to 0 and some nonzero complex
670: number C we have a factorization
671:                           f (z) = Cσ(z − P1 ) · · · σ(z − P2n ).
672: Moreover, by re-indexing the points P1 , . . . , P2n if necessary, we can arrange for the
673: vectors
674:                        u(z)                                         v(z)
675:      u∗ (z) =                              , v ∗ (z) =
676:               Cσ(z − P1 ) · · · σ(z − Pn )              σ(z − Pn+1 ) · · · σ(z − P2n )
677: to have entries that are entire functions of z. Now put
678:                       t = −(P1 + · · · + Pn ) = Pn+1 + · · · + P2n .
679: ABELIANTS AND THEIR APPLICATION TO AN ELEMENTARY CONSTRUCTION OF JACOBIANS
680:                                                                         11
681: 
682: 
683: Then the entries of the vector u∗ (z + t/n) (resp. v ∗ (z − t/n)) belong to Σn and
684: hence, since C-linearly independent, form a C-basis for Σn . It follows that for some
685: n by n matrices Φ and Ψ with entries in C we have
686:       u∗ (z + t/n) = Φ~σ (z)T , v ∗ (z − t/n) = ~σ (z)Ψ, det Φ 6= 0, det Ψ 6= 0.
687: Finally, we have
688:                          X(z) = Φ~σ (z − t/n)T ~σ (z + t/n)Ψ,
689: i. e., X(z) is C-equivalent to a Segre matrix of the form (25). Therefore the corre-
690: spondence in question is onto.
691: 
692: 3.3. An ad hoc tensor formalism.
693: 
694: 3.3.1. Definition of A⊗Z . Let A⊗Z be the tensor product over k of copies of A
695: indexed by Z, formed according to the definition [Jacquet-Langlands 1970, pp. 301-
696: 303]. By that definition the k-algebra A⊗Z is generated by symbols of the form
697:                         O
698:                             ai (ai ∈ A, ai = 1 for |i| ≫ 0)
699:                          i∈Z
700: 
701: subject to obvious relations. Put
702:                                          O a        if i = ℓ
703:                                a(ℓ) :=
704:                                                 1    if i 6= ℓ
705:                                          i∈Z
706: 
707: for all a ∈ A and ℓ ∈ Z. More generally, given a matrix X with entries in A and
708: ℓ ∈ Z we define a matrix X (ℓ) with entries in A⊗Z by the rule
709:                                       
710:                                  X (ℓ)   = (Xij )(ℓ) .
711:                                            ij
712: 
713: For any subset I ⊆ Z, let A⊗I denote the k-subalgebra of A⊗Z generated by all
714: elements of the form a(ℓ) where a ∈ A and ℓ ∈ I. If I is a finite subset of Z, then the
715: k-algebra A⊗I can naturally be identified with the usual tensor product over k of
716: copies of A indexed by I. For any subset I ⊂ Z, the k-algebra A⊗I is characterized
717: in the category of commutative k-algebras with unit by a universal property we
718: need not belabor. We make the identifications
719:                                           a(0) = a
720: for all a ∈ A, thus equipping A⊗Z with the structure of A-algebra. Finally, note that
721: the k-algebra A⊗Z is without zero divisors; this fact plays an extremely important
722: role in the sequel.
723: 
724: 3.3.2. Partial specializations of A⊗Z . Let S be the set of k-algebra homomorphisms
725: A → k. For all a ∈ A and s ∈ S we denote the value in k of a at s by a|s . More
726: generally, given a matrix X with entries in A, we define a matrix X|s with entries
727: in k by the rule
728:                                    (Xij )|s = (X|s )ij .
729: Now let I be a set of integers and let
730:                                     s = {sℓ }ℓ∈I ∈ S I
731: be any family of points of S indexed by I. We define the partial specialization
732:                                (a 7→ aks ) : A⊗Z → A⊗(Z\I)
733: 12                               GREG W. ANDERSON
734: 
735: 
736: associated to the family s to be the unique k-algebra homomorphism such that
737:                                        
738:                                         a|sℓ if ℓ ∈ I
739:                              a(ℓ) ks =
740:                                         (ℓ)
741:                                          a    if ℓ 6∈ I
742: for all a ∈ A and ℓ ∈ Z. More generally, given a matrix X with entries in A⊗Z , we
743: define a matrix Xks with entries in A⊗(Z\I) by the rule
744:                                  (Xks )ij = (Xij )ks .
745: 
746: 3.3.3. Derangements and their action on A⊗Z . A derangement is by definition a
747: map of the set Z of integers to itself. The support of a derangement σ is by definition
748: the set
749:                                     {ℓ ∈ Z | σℓ 6= ℓ},
750: i. e., the set of integers actually moved by σ. For each derangement σ we define
751:                                   σ∗ : A⊗Z → A⊗Z
752: to be the unique k-algebra homomorphism such that
753:                                    σ∗ (a(ℓ) ) = a(σℓ)
754: for all a ∈ A and ℓ ∈ Z and more generally, given any matrix Z with entries in
755: A⊗Z , we define a matrix σ∗ Z with entries in A⊗Z by the rule
756:                                  (σ∗ Z)ij = σ∗ (Zij ).
757: For any derangements σ and τ we have
758:                                     σ∗ τ∗ = (στ )∗ .
759: 
760: 3.3.4. The bar operation. We define the bar operation
761:                                                 ∼
762:                                 (a 7→ ā) : A⊗Z →A⊗Z
763: to be the unique k-algebra automorphism such that
764:                                      a(ℓ) = a(−ℓ)
765: for all a ∈ A and ℓ ∈ Z. More generally, given a matrix Z with entries in A⊗Z we
766: define Z by the rule
767:                                  ( Z )ij = Z ij .
768: The bar operation is none other than the automorphism of A⊗Z associated to the
769: sign-reversing derangement ℓ 7→ −ℓ. Since
770:                                  a = a(0) = a(0) = a
771: for all a ∈ A, the bar operation is an A-algebra automorphism.
772: 
773: 3.3.5. Special derangements. Given distinct integers i and j, let hi | ji be the unique
774: derangement with support {i, j}; in other words, hi | ji exchanges i and j and fixes
775: all other integers. Given integers i and j (possibly not distinct), let [i 7→ j] be the
776: unique derangement with support contained in the set {i} sending i to j; in other
777: words, [i 7→ j] maps i to j and fixes all other integers.
778: ABELIANTS AND THEIR APPLICATION TO AN ELEMENTARY CONSTRUCTION OF JACOBIANS
779:                                                                         13
780: 
781: 
782: 3.4. Criteria for k-generality.
783: Lemma 3.4.1. Let integers ℓ1 < · · · < ℓN be given. Let u be a column vector of
784: length N with entries in A and put
785:                                                   
786:                            U = u(ℓ1 ) . . . u(ℓN )
787: thereby defining an N by N matrix with entries in A⊗{ℓ1 ,...,ℓN } . The entries of the
788: vector u are k-linearly dependent if and only if the determinant of the matrix U
789: vanishes identically.
790: Proof. (⇒) By row operations leaving the determinant unchanged we can transform
791: U to a matrix with an identically vanishing row.
792:    (⇐) We proceed by induction on N . The case N = 1 is trivial; assume now
793: that N > 1. Without loss of generality we may assume that the determinant
794: of every N − 1 by N − 1 submatrix of U is nonvanishing, for otherwise we are
795: done by induction on N . Also without loss of generality we may assume that
796: (ℓ1 , . . . , ℓN ) = (0, . . . , N − 1). Expanding U by minors of the first column we
797: obtain a relation
798:                                                                                              
799:            a1 u 1 + · · · + aN u N = 0    a1 , . . . , aN ∈ A⊗{1,...,N −1} , a1 · · · aN 6= 0
800: among the entries of u. By the Nullstellensatz there exists
801:                             s = (s1 , . . . , sN −1 ) ∈ S {1,...,N −1}
802: such that
803:                        (a1 · · · aN )ks = (a1 ks ) · · · (an ks ) 6= 0
804: and for any such s we obtain by partial specialization a nontrivial k-linear relation
805:             (a1 u1 + · · · + aN uN ) ks = (a1 ks ) · u1 + · · · + (aN ks ) · uN = 0
806: among the entries of u.
807: Lemma 3.4.2. Let integers ℓ1 < · · · < ℓn be given. Let X be an n by n ma-
808: trix P
809:      with entries in A of rank ≤ 1. The matrix X is k-general if and only if
810:        n     (ℓν )
811: det    ν=1 X       6= 0.
812: Proof. We may assume without loss of generality that (ℓ1 , . . . , ℓn ) = (1, . . . , n). Let
813: u be the j th column of X and let v be the ith row of X, where i and j are presently
814: to be chosen in a useful way. Put
815:                                                        (1) 
816:                                                         v
817:                           (1)          (n)
818:                                                       .. 
819:                     U= u         ··· u         , V =  . .
820:                                                                    v (n)
821: We claim that
822:                                                         
823:                                                              (1)       (n)
824: (26)            det U · det V = det X (1) + · · · + X (n) · Xij · · · Xij .
825: In any case we have
826:                                        Xij X = uv
827: since X is of rank ≤ 1. If Xij = 0, then both sides of (26) vanish. Suppose now
828: that Xij 6= 0. After localizing A suitably, we may assume that Xij is a unit of A.
829: Then we have
830:                                                                   −1
831:                                                   (1)          (n)
832:                  X (1) + · · · + X (n) = u diag Xij , . . . , Xij      v,
833: 14                                 GREG W. ANDERSON
834: 
835: 
836: whence (26) after taking determinants on both sides and rearranging the resulting
837: identity. The claim is proved.
838:    To prove the implication (⇒), we choose i and j so that the entries of u are
839: k-linearly independent and the entries of v are k-linearly independent. Then the
840: entry Xij common to u and v is nonzero and the left side of (26) is nonvanishing
841: by Lemma 3.4.1. It follows that the determinant in question does not vanish.
842:    To prove the implication (⇐), we choose i and j so that Xij 6= 0. Then the
843: right side of (26) is nonvanishing and hence neither det U or det V vanish. By
844: Lemma 3.4.1 the entries of u are k-linearly independent and the entries of v are
845: k-linearly independent. It follows that the matrix X is k-general.
846: Proposition 3.4.3. Let X be an n by n matrix with entries in A of rank ≤ 1. The
847: following conditions are equivalent:
848: (27)                                 X is k-general.
849: 
850:                                              (ℓ)
851: (28)                                  ∆n+1
852:                                        ℓ=1 X     6= 0.
853: 
854: (29)                                abeln+1
855:                                         ℓ=0 X
856:                                               (ℓ)
857:                                                   6= 0.
858: Proof. For distinct i, j ∈ {0, . . . , n + 1} put
859:                                                                  
860:                                                 X
861:                          Dij = det                          X (ℓ)  .
862:                                        ℓ∈{0,...,n+1}\{i,j}
863: 
864: Consider two more conditions:
865: (30)               Dij 6= 0 for some distinct i, j ∈ {0, . . . , n + 1}.
866: 
867: (31)                Dij 6= 0 for all distinct i, j ∈ {0, . . . , n + 1}.
868: We have implications
869:                      (31) ⇒ (28) ⇒ (30) ⇒ (27) ⇒ (31) ⇒ (29),
870: the first two by definition of the discriminant, the next two by Lemma 3.4.2, and
871: the last by identity (19). To complete the proof it suffices to prove the implication
872: (29)⇒(30). Put Z = abeln+1 ℓ=0 X
873:                                  (ℓ)
874:                                      to abbreviate notation. By hypothesis there exist
875: indices i and j such that Zij 6= 0. We then have
876:         0 6= Zij · h0 | n + 1i∗ Zij = Zij Zji = Zii Zjj = D0i Di,n+1 D0j Dj,n+1 ,
877: the first equality by identity (4), the second by fact (15) and the third by identity
878: (19). Therefore condition (29) does indeed imply condition (30).
879: 3.5. Normalization and self-similarity.
880: 3.5.1. Definitions. Let an n by n matrix X with entries in A of rank ≤ 1 be given.
881: Let
882:                           s = (s1 , . . . , sn+1 ) ∈ S {1,...,n+1}
883: be given. We say that X is s-normalized under the following conditions:
884: (32)      For i, j, ℓ = 1, . . . , n we have Xij |sℓ 6= 0 if and only if i = j = ℓ.
885: 
886: (33)                   For i, j = 1, . . . , n we have Xij |sn+1 = 1.
887: ABELIANTS AND THEIR APPLICATION TO AN ELEMENTARY CONSTRUCTION OF JACOBIANS
888:                                                                         15
889: 
890: 
891: We say that X is s-self-similar under the following conditions:
892:                                                    
893: (34)                        ∆ X|s1 , . . . , X|sn+1 6= 0.
894:                                              
895: (35)           abel X, X|s1 , . . . , X|sn+1 is k-proportional to X.
896: 
897: Proposition 3.5.2. Fix an n by n matrix X with entries in A of rank ≤ 1. Fix
898: s = (s1 , . . . , sn+1 ) ∈ S {1,...,n+1} . (i) If X is s-normalized then condition (34) holds.
899: (ii) If condition (34) holds then X is k-general.
900: Proof. (i) This follows from identity (10). (ii) Put ∆ = ∆n+1
901:                                                           ℓ=1 X
902:                                                                 (ℓ)
903:                                                                     . By hypothesis
904: ∆ks 6= 0, hence ∆ 6= 0, whence the result by Proposition 3.4.3.
905: Proposition 3.5.3. Fix a Segre matrix X and s = (s1 , . . . , sn+1 ) ∈ S {1,...,n+1} .
906: There exist n by n matrices Φ and Ψ with entries in k such that
907:                                                                                  
908:  ΦXΨ = abel X, X|s1 , . . . , X|sn+1 , (det Φ)2 (det Ψ)2 = ∆ X|s1 , . . . , X|sn+1 .
909: Moreover if X is s-normalized then Φ and Ψ may be taken diagonal.
910: Proof. This follows directly from key relation (11).
911: Lemma 3.5.4. Fix a Segre matrix X and s = (s1 , . . . , sn+1 ) ∈ S {1,...,n+1} . If X
912: is s-self-similar then there exist diagonal matrices Φ and Ψ with entries in k such
913: that det Φ · det Ψ 6= 0 and Φ−1 XΨ−1 is s-normalized.
914: Proof. By hypothesis (35) there exists a nonzero scalar c such that
915:                                                             
916:                        X = c · abel X, X|s1 , . . . , X|sn+1 .
917: It follows by identity (16) that for ℓ = 1, . . . , n every entry of the matrix
918:                                                                     
919:                        X|sℓ = c · abel X|sℓ , X|s1 , . . . , X|sn+1
920: vanishes save possibly the ℓth diagonal entry. Let E be the n by n matrix with all
921: entries equal to 1. Since X|sn+1 is of rank ≤ 1 we can write
922:                                       X|sn+1 = ΦEΨ
923: where Φ and Ψ are diagonal matrices with entries in k. By hypothesis (34) and
924: identity (10) neither is it possible for det Φ · det Ψ to vanish, nor for there to exist
925: some index ℓ = 1, . . . , n such that the ℓth diagonal entry of X|sℓ vanishes. Therefore
926: the pair (Φ, Ψ) has all the desired properties.
927: Proposition 3.5.5. Fix a Segre matrix X and s ∈ S {1,...,n+1} . Put
928:                           Z = abeln+1
929:                                   ℓ=0 X
930:                                         (ℓ)
931:                                             ,    ∆ = ∆n+1
932:                                                       ℓ=1 X
933:                                                             (ℓ)
934:                                                                 .
935: Assume that ∆ks 6= 0. (i) Up to k-proportionality Zks is the unique s-self-similar
936: Segre matrix k-equivalent to X. (ii) There exists a unique s-normalized Segre matrix
937: k-equivalent to X.
938: Proof. (i) By Proposition 3.5.3 the matrix
939:                                                                   
940:                             Zks = abel X, X|s1 , . . . , X|sn+1
941: is a Segre matrix k-equivalent to X. Further, Zks is s-self-similar by the iterated
942: abeliant identity (21). Finally, any two k-equivalent s-self-similar Segre matrices
943: are k-proportional by the abeliant transformation law (3).
944:    (ii) We may assume without loss of generality that X is s-self-similar. By
945: Lemma 3.5.4 there exists at least one s-normalized Segre matrix k-equivalent to X.
946: 16                                  GREG W. ANDERSON
947: 
948: 
949: Now suppose that Y and Y ′ are s-normalized Segre matrices both
950: k-equivalent to X. By Proposition 3.5.3 and our additional assumption that X
951: is s-self-similar, we have X = ΦY Ψ = Φ′ Y ′ Ψ′ where Φ, Ψ, Φ′ , Ψ′ are nonsingular
952: diagonal matrices with entries in k, hence we have ΦEΨ = Φ′ EΨ′ where E is the
953: n by n matrix with all entries equal to 1, hence there exists a nonzero scalar c such
954: that Φ′ = cΦ and Ψ′ = c−1 Ψ, and hence Y = Y ′ .
955: 3.6. The abstract Abel map: definition and key properties.
956: 3.6.1. Definition. The abstract Abel map by definition sends each Segre matrix X
957: to the n by n matrix abeln+1
958:                           ℓ=0 X
959:                                 (ℓ)
960:                                     with entries in A⊗{0,...,n+1} . The abstract Abel
961: map generalizes and abstracts the explicit algebraic representation of the Abel map
962: studied in [Anderson 1997].
963: 3.6.2. Catalog of key properties. Fix a Segre matrix X. Let
964:                            Z = abeln+1
965:                                    ℓ=0 X
966:                                          (ℓ)
967:                                              , ∆ = ∆n+1
968:                                                     ℓ=1 X
969:                                                           (ℓ)
970: 
971: 
972: be the image of X under the abstract Abel map and the naturally associated dis-
973: criminant, respectively. The following hold:
974:    • Z 6= 0 and ∆ 6= 0, by Proposition 3.4.3.
975: 
976:      • If X is replaced by a k-equivalent matrix, then Z and ∆ are replaced by
977:        nonzero scalar multiples, by (3) and (8).
978: 
979:      • If X is replaced by X T , then Z is replaced by Z T and ∆ remains unchanged,
980:        by (4) and (9).
981: 
982:      • h0 | n + 1i∗ Z = Z T , by (4).
983: 
984:      • π∗ Zij = Zπi,πj for any bijective derangement π supported in {1, . . . , n},
985:        by (5).
986: 
987:      • [1 7→ 2]∗ Z12 = Z11 , by (6).
988: 
989:      • Z is of rank ≤ 1, by (15).
990:                                                                       n
991:                                                                       Y                 2
992:      • ∆     =    h2|n + 1i∗ h0|1i∗ Z11 · h0|1i∗ Z11 · h0|2i∗ Z22 ·         (h0|ℓi∗ Zℓℓ ) ,
993:                                                                       ℓ=3
994:        by (20).
995: 
996:      • abeln+1
997:            ℓ=0 [0 7→ −ℓ]∗ Z = ∆ · Z, by (21).
998:                                      Y                                  Y
999:      • Zij ∈ k-span of L ·                    L(b)   · L(n+1) ·                      L(a) ,
1000:                                  b∈{1,...,n}\{j}                  a∈{1,...,n}\{i}
1001:        by (23).
1002: 
1003: Proposition 3.6.3 (“The abstract Abel theorem”). Let         X     and     X′    be
1004: Segre matrices with corresponding images Z and Z ′ under the abstract Abel map, re-
1005: spectively.     Then X ′ is k-equivalent to X if and only if Z ′ is
1006: k-proportional to Z.
1007: ABELIANTS AND THEIR APPLICATION TO AN ELEMENTARY CONSTRUCTION OF JACOBIANS
1008:                                                                         17
1009: 
1010: 
1011: Proof. (⇒) This follows directly from identity (3).
1012:    (⇐) Put
1013:                       ∆ = ∆n+1
1014:                              ℓ=1 X
1015:                                        (ℓ)
1016:                                            , ∆′ = ∆n+1         ′ (ℓ)
1017:                                                        ℓ=1 (X ) .
1018:                                             ′
1019: By Proposition 3.4.3 neither ∆ nor ∆ vanish identically. By the Nullstellensatz
1020: there exists
1021:                          s = (s1 , . . . , sn+1 ) ∈ S {1,...,n+1}
1022: such that
1023:                                ∆ks 6= 0, ∆′ ks 6= 0.
1024: By Proposition 3.5.3 and hypothesis we have
1025:                               X ∼ Zks ∼ Z ′ ks ∼ X ′ ,
1026: where ∼ denotes k-equivalence.
1027: 3.7. Characterization of the image of the abstract Abel map.
1028: 3.7.1. J-matrices. A J-matrix Z is by definition an object with the following prop-
1029: erties:
1030: (36)     Z is an n by n matrix with entries in the k-span of L · A⊗{1,...,n+1} .
1031: 
1032: (37)                                   Z 6= 0.
1033: 
1034: (38)                             Z is of rank ≤ 1.
1035: 
1036: (39)       abeln+1
1037:                ℓ=0 [0 7→ −ℓ]∗ Z = ∆ · Z for some 0 6= ∆ ∈ A
1038:                                                            ⊗{1,...,n+1}
1039:                                                                         .
1040: Since A⊗Z is a k-algebra without zero-divisors, Z uniquely determines ∆. We call
1041: ∆ the discriminant of the J-matrix Z. If we need to call attention to the basic
1042: data we say that Z is a J-matrix of type (k, n, A, L). In view of the properties
1043: catalogued in §3.6.2, it is clear that every matrix in the image of the abstract Abel
1044: map is automatically a J-matrix.
1045: Proposition 3.7.2 (“The abstract Jacobi inversion theorem”). Fix                    a
1046: J-matrix Z with associated discriminant ∆. (i) For all s ∈ S {1,...,n+1} the par-
1047: tial specialization ∆ks is a scalar and for some s that scalar does not vanish. (ii)
1048: For any s ∈ S {1,...,n+1} such that the scalar ∆ks does not vanish, the corresponding
1049: partial specialization Zks is a Segre matrix with image under the abstract Abel map
1050: k-proportional to Z.
1051: Proof. (i) This follows from the Nullstellensatz.
1052:    (ii) Put
1053:                                      X = Zks .
1054: The matrix X is an n by n matrix with entries in L by condition (36) and of rank
1055: ≤ 1 by condition (38). By applying firstly the partial specialization operation ks
1056: and secondly the bar operation to both sides of the identity figuring in condition
1057: (39), we obtain the relation
1058:                               abeln+1
1059:                                   ℓ=0 X
1060:                                         (ℓ)
1061:                                             = ∆ks · Z.
1062: The right side does not vanish by condition (37) combined with our hypothesis
1063: that ∆ks 6= 0. It follows by Proposition 3.4.3 that X is k-general and hence a Segre
1064: matrix. It follows as well that the image of X under the abstract Abel map is
1065: k-proportional to Z.
1066: 18                                GREG W. ANDERSON
1067: 
1068: 
1069: 3.7.3. Jacobi matrices. A Jacobi matrix Z is by definition an object with the fol-
1070: lowing properties:
1071: (40)              Z is an n by n matrix with entries in A⊗{0,...,n+1} .
1072: 
1073: (41)                                       Z 6= 0.
1074: 
1075:                                                    2        2
1076: (42)          Z12 ∈ k-span of L · L(1) · L(2) · L(3) · · · L(n) · L(n+1) .
1077: 
1078: (43)                               Z11 = [1 7→ 2]∗ Z12 .
1079: 
1080:               π∗ Zij = Zπi,πj for any bijective derangement π supported
1081: (44)
1082:               in {1, . . . , n}.
1083: 
1084:                                      Z11     Z12
1085: (45)                                                 = 0.
1086:                                      Z21     Z22
1087: 
1088: (46)                         abeln+1
1089:                                  ℓ=0 [0 7→ −ℓ]∗ Z = ∆ · Z,
1090: 
1091: where
1092:                                                                  n
1093:                                                                  Y                 2
1094: (47)     ∆ = h2|n + 1i∗ h0|1i∗ Z11 · h0|1i∗ Z11 · h0|2i∗ Z22 ·         (h0|ℓi∗ Zℓℓ ) .
1095:                                                                  ℓ=3
1096: 
1097: We call ∆ the discriminant of the Jacobi matrix Z. If we need to draw attention
1098: to the basic data we say that Z is of type (k, n, A, L). It is clear that the set of
1099: k-proportionality classes of Jacobi matrices forms a projective algebraic variety.
1100: Moreover, in view of the properties cataloged in §3.6.2, it is clear that the abstract
1101: Abel map takes its values in the set of Jacobi matrices. Note that a Jacobi matrix
1102: Z is uniquely determined by its entry Z12 .
1103: Lemma 3.7.4. The discriminant of a Jacobi matrix does not vanish identically
1104: and belongs to A⊗{1,...,n+1} .
1105: Proof. Fix a Jacobi matrix Z with associated discriminant ∆. By conditions (41)
1106: and (44) either every diagonal entry of Z is nonvanishing or every off-diagonal entry
1107: of Z is nonvanishing; but then by condition (45) every entry Z is nonvanishing. By
1108: definition (47) it follows that ∆ does not vanish identically. By conditions (42) and
1109: (43) we have
1110:                                   Z11 ∈ A⊗{0,2...,n+1} .
1111: By condition (44) we have
1112:                           Zℓℓ = h1 | ℓi∗ Z11 ∈ A⊗{0,...,n+1}\{ℓ}
1113: and further
1114:          hℓ | 0i∗ Zℓℓ ∈ A⊗{1,...,n+1} , h2 | n + 1i∗ h1 | 0i∗ Z11 ∈ A⊗{1,...,n+1} .
1115: By definition (47) it follows that ∆ belongs to A⊗{1,...,n+1} .
1116: Proposition 3.7.5. Every Jacobi matrix is a J-matrix and vice versa.
1117: ABELIANTS AND THEIR APPLICATION TO AN ELEMENTARY CONSTRUCTION OF JACOBIANS
1118:                                                                         19
1119: 
1120: 
1121: Proof. By Proposition 3.7.2 every J-matrix is in the image of the abstract Abel
1122: map and hence a Jacobi matrix in view of the properties cataloged in §3.6.2. Thus
1123: the “vice versa” part of the proposition is proved. Now fix a Jacobi matrix Z with
1124: associated discriminant ∆. We verify that Z has the properties required of a J-
1125: matrix as follows. To abbreviate notation temporarily let V denote the k-span of
1126: L · A⊗{1,...,n+1} . We have Z12 ∈ V by condition (42). We have [1 7→ 2]∗ V ⊆ V and
1127: hence Z11 ∈ V by condition (43). We have π∗ V ⊆ V for any bijective derangement
1128: π supported in {1, . . . , n} and hence Zij ∈ V for all i, j ∈ {1, . . . , n} by condition
1129: (44). Therefore Z satisfies condition (36). Conditions (37) and (41) are exactly the
1130: same. Clearly Z satisfies condition (38) by conditions (44) and (45). Finally, Z
1131: satisfies condition (39) by condition (46) combined with Lemma 3.7.4.
1132: Theorem 3.7.6. (i) The set of k-proportionality classes of Jacobi matrices forms a
1133: projective algebraic variety. (ii) The abstract Abel map takes values in the set of Ja-
1134: cobi     matrices.           (iii)    The     abstract   Abel     map      puts     the
1135: k-equivalence classes of Segre matrices into bijective correspondence with the k-
1136: proportionality classes of Jacobi matrices.
1137: Proof. (i,ii) These facts have already been noted above.
1138:    (iii) The correspondence in question is well-defined and one-to-one by Proposi-
1139: tion 3.6.3. The correspondence is onto by Propositions 3.7.2 and 3.7.5.
1140: 3.7.7. Remark. We briefly describe the big picture in more geometrical language.
1141: We temporarily introduce the following notation:
1142:     • Let V be the quasi-affine variety of Segre matrices.
1143:     • Let G denote the product of two copies of the n by n general linear group
1144:       over k and let G act in the obvious way on V .
1145:     • Let J be the projective variety of k-proportionality classes of Jacobi matrices.
1146: For each s ∈ S {1,...,n+1} :
1147:     • Let Vs be the open subvariety of V consisting of Segre matrices X satisfying
1148:       the inequality ∆n+1
1149:                         ℓ=1 (X|sℓ ) 6= 0.
1150:     • Let Us be the affine variety consisting of n by n matrices X with entries in L
1151:       that are of rank ≤ 1 and s-normalized.
1152:     • Let Us′ be the quasi-projective variety consisting of s-self-similar Segre matri-
1153:       ces modulo k-proportionality.
1154:     • Let Js be the open subvariety of J consisting of points represented by Jacobi
1155:       matrices with discriminant ∆ such that ∆ks 6= 0.
1156: By Proposition 3.4.3 and the Nullstellensatz the open subvarieties Vs cover V .
1157: By identity (8) the variety Vs is G-stable. By Proposition 3.5.2 the variety Us is
1158: contained in Vs . By Proposition 3.5.5 the quotient Vs /G can naturally be identified
1159: with Us′ and also with Us . By Lemma 3.7.4 and the Nullstellensatz the open sets
1160: Js cover J. By Propositions 3.5.5, 3.6.3, 3.7.2 and 3.7.5, the set Js can naturally
1161: be identified with Us′ and hence also with Us . The upshot is that the family {Us }
1162: can be viewed as an affine open covering of J.
1163: 3.8. Examples of Jacobi matrices involving elliptic functions.
1164: 3.8.1. The set up. We continue in the set up of §3.2.1. By Proposition 3.2.4 com-
1165: bined with Theorem 3.7.6 every Jacobi matrix of type (24) is C-proportional to the
1166: image of some matrix of the form (25) under the abstract Abel map for a value of
1167: the parameter t ∈ C uniquely determined modulo the period lattice Λ. To figure
1168: 20                                           GREG W. ANDERSON
1169: 
1170: 
1171: out what these Jacobi matrices actually look like, we are going to apply the ab-
1172: stract Abel map to the matrix (25). But before we proceed we have a notational
1173: collision to deal with: f (ℓ) denotes the ℓth derivative of f in the present context.
1174: To fix the problem we think of and write out the “superscript ℓ” operation defined
1175: in §3.3.1 as the high school algebra operation of “substitution of the variable zℓ for
1176: the variable z.”
1177: 
1178: 3.8.2. A classical determinant identity and related abeliant identity. By combining
1179: the classical identity
1180: (48)
1181:                                                                                  n
1182:                                                                                             !
1183:                                                                                  X                     Y
1184:                         ′
1185:                                            (−1)n−2 ℘(n−2) (z1 )
1186:      1    ℘(z1 )
1187:            1!        − ℘ (z
1188:                           2!
1189:                              1)
1190:                                      ···        (n−1)!
1191:                                                                              σ         zi        ·              σ(zi − zj )
1192:      ..     ..           ..                             ..               =
1193:                                                                                  i=1                 1≤i<j≤n
1194:       .      .            .                              .                                   n
1195:                                                                                              Y
1196:      1    ℘(zn )         ′
1197:                     − ℘ (z n)
1198:                                      ···   (−1)   n−2
1199:                                                       ℘(n−2) (zn )                                    σ(zi )n
1200:             1!          2!                          (n−1)!
1201:                                                                                              i=1
1202: 
1203: (see [Frobenius Stickelberger 1877, p. 179] or [Whittaker Watson, Chap. XX, Misc.
1204: Ex. 21]) with abeliant identity (14), we find after a straightforward calculation that
1205: 
1206: (49)
1207:                                                                                        σ(n) (0)
1208:                                                                                          ~
1209:                                                                                                          4
1210:                                                                                            n!
1211:                                                                                     σ(n−2) (0)
1212:                                                                                        ~                 
1213:                                                                                                       
1214:                    abeln+1 σ (zℓ − t/n)T ~σ (zℓ + t/n) ij             det              (n−2)!          
1215:                        ℓ=0 ~                                                                  ..       
1216:                                                                                                .       
1217:                                                                                             σ(0)
1218:                                                                                             ~
1219:                                                                                               0!
1220:                                                                                                         
1221:                                       X                                           X
1222:      =           σ t +                             zℓ  × σ t −                                        zℓ 
1223:                               ℓ∈{0,...,n+1}\{0,i}                        ℓ∈{0,...,n+1}\{i,n+1}
1224: 
1225:                                                                                                          
1226:                                        X                                               X
1227:           ×      σ t +                                  zℓ  × σ t −                                   zℓ 
1228:                               ℓ∈{0,...,n+1}\{j,n+1}                          ℓ∈{0,...,n+1}\{0,j}
1229: 
1230:                                Y                                                 Y
1231:           ×                                  σ(zα − zβ ) ×                                                σ(zα − zβ )
1232:                    α,β∈{0,...,n+1}\{0,i}                             α,β∈{0,...,n+1}\{i,n+1}
1233:                                α<β                                               α<β
1234: 
1235:                                  Y                                                 Y
1236:           ×                                         σ(zα − zβ ) ×                                         σ(zα − zβ ).
1237:                    α,β∈{0,...,n+1}\{j,n+1}                               α,β∈{0,...,n+1}\{0,j}
1238:                                 α<β                                               α<β
1239: 
1240: Identity (49) granted, it is not difficult to verify that the variety of
1241: C-proportionality classes of Jacobi matrices is a complex manifold isomorphic to
1242: the complex torus C/Λ. We omit further details.
1243: 
1244:                          4. Elementary construction of Jacobians
1245: ABELIANTS AND THEIR APPLICATION TO AN ELEMENTARY CONSTRUCTION OF JACOBIANS

LINES 1249-1673
1249: 4.1. Basic notation and terminology. As above, let k be an algebraically closed
1250: field. We work in the category of quasi-projective varieties over k. As above, let
1251: C be a nonsingular projective algebraic curve of genus g. We assume that g > 0.
1252: Divisors are divisors of C. Given a divisor D, we write L(D) = H 0 (C, OC (D)) and
1253: ℓ(D) = dimk L(D).
1254: 4.2. Matrix representation of divisor classes.
1255: Lemma 4.2.1. Let D be a divisor such that deg D ≥ 2g. Then we have
1256:                                ℓ(D) = deg D − g + 1.
1257: Moreover, we have
1258:                           ℓ(D′ ) ≥ ℓ(D) ⇒ deg D′ ≥ deg D
1259: for all divisors D′ .
1260: Proof. Riemann-Roch.
1261: 4.2.2. G-forms. Let G be a divisor such that
1262:                                              1
1263:                          deg G ≡ 0 mod 2,      deg G ≥ 2g
1264:                                              2
1265: and put
1266:                                     1
1267:                                n = deg G − g + 1.
1268:                                     2
1269: By definition a G-form X is an object with the following properties:
1270:     • X is an n by n matrix with entries in L(G).
1271:     • Every two by two submatrix of X has vanishing determinant.
1272:     • There exists in X some row and also some column with k-linearly independent
1273:       entries.
1274: A G-form is the same thing as a Segre matrix of type
1275:                                     ∞
1276:                                                     !
1277:                                     M
1278:                               k, n,   L(mG), L(G) .
1279:                                    m=0
1280: If G > 0, then a G-form can also be viewed as a Segre matrix of type
1281:                                                          
1282:                         k, n, H 0 (C \ supp G, OC ), L(G) .
1283: Here and below supp D denotes the support of a divisor D. Our immediate goal
1284: is to put the k-equivalence classes of G-forms in canonical bijective correspondence
1285: with the divisor classes of degree 21 deg G. The “dictionary” we ultimately obtain
1286: is summarized by Proposition 4.2.6 below.
1287: 4.2.3. Representation of divisors of degree 12 deg G by G-forms. Let G and n be as
1288: above. Let D be a divisor of degree 12 deg G. Let u (resp. v) be a column (resp. row)
1289: vector with entries forming a k-basis for L(D) (resp. L(G − D)). Put X = uv. It
1290: is clear that that X is a G-form the k-equivalence class of which depends only on
1291: D, not on the choice of vectors u and v. In this situation we say that the G-form
1292: X represents the divisor D of degree 21 deg G. We claim that for every divisor D′
1293: in the divisor class of D and every G-form X ′ representing D′ , the G-form X is
1294: k-equivalent to X ′ . To prove the claim, write D = D′ + (f ) where f is a nonzero
1295: meromorphic function on C. Then
1296:                   L(D′ ) = f · L(D), L(G − D′ ) = f −1 · L(G − D),
1297: 22                               GREG W. ANDERSON
1298: 
1299: 
1300: hence the G-form X = uv = (f u)(f −1 v) represents not only D but also D′ , and
1301: hence X is k-equivalent to X ′ . The claim is proved.
1302: 4.2.4. Unique determination of the class of a divisor by a representing G-form.
1303: Let G and n be as above. Suppose that divisors D and D′ of degree 21 deg G are
1304: represented by k-equivalent G-forms X and X ′ , respectively. We claim that D and
1305: D′ belong to the same divisor class. To prove the claim we may assume without
1306: loss of generality that X = X ′ . Write X = uv = u′ v ′ where u and u′ are column
1307: vectors, v and v ′ are row vectors, and the entries of u (resp. v, u′ , v ′ ) form a k-
1308: basis for L(D) (resp. L(G − D), L(D′ ), L(G − D′ )). There exists a unique nonzero
1309: meromorphic function f on C such that u′ = f u and v ′ = f −1 v, hence
1310:             L(D) = f −1 · L(D′ ) = L(D′ + (f )) ⊂ L(min(D, D′ + (f ))),
1311: and hence D = D′ + (f ) by Lemma 4.2.1. The claim is proved.
1312: 4.2.5. Construction of a divisor represented by a given G-form. Let G and n be
1313: as above. Let X be a G-form. Choose a column u and a row v of X each with
1314: k-linearly independent entries. Let f be the entry common to u and v; then f does
1315: not vanish identically. Consider now the effective divisors
1316:                D = G + min(vj ),    E = G + min(ui ), F = G + (f ).
1317:                           j                     i
1318: 
1319: We claim that X represents the divisor D. In any case, since X is of rank ≤ 1 we
1320: have X = uv/f and hence
1321:                    D + E ≥ F,    deg D + deg E ≥ deg F = deg G.
1322: Since the entries of v are k-linearly independent and belong to L(G − D), we have
1323: ℓ(G − D) ≥ n and hence 21 deg G ≥ deg D by Lemma 4.2.1 . Similarly we have
1324: 1
1325: 2 deg G ≥ deg E. It follows that
1326:                                    1         1
1327:                 deg D = deg E =      deg G = deg F, D + E = F.
1328:                                    2         2
1329: In turn it follows that the entries of v form a k-basis for L(G − D) and that the
1330: entries of u/f form a k-basis for L(G − E + (f )) = L(D). Therefore X = uv/f
1331: does indeed represent the divisor D. The claim is proved.
1332: Proposition 4.2.6. Let G be a divisor of even degree such that 21 deg G ≥ 2g.
1333: There exists a unique bijective correspondence
1334:                                                                
1335:                    k-equivalence               divisor classes
1336:                                          ↔
1337:                    classes of G-forms          of degree 21 deg G
1338: with respect to which, for any G-form X and any divisor D of degree 21 deg G, the
1339: k-equivalence class of X corresponds to the divisor class of D if and only if X
1340: represents D.
1341: Proof. All the hard work is done; we just have to sum up. For each divisor
1342: D of degree 12 deg G arbitrarily fix a column (resp. row) vector uD (resp. vD )
1343: with entries forming a k-basis of L(D) (resp. L(G − D)). The product uD vD
1344: is a G-form the k-equivalence class of which depends only on D, not on the
1345: choice of uD and vD (§4.2.3). The map D 7→ uD vD sends divisor classes into
1346: k-equivalence classes (§4.2.3). The map D 7→ uD vD sends distinct divisor classes
1347: into distinct k-equivalence classes (§4.2.4).       The image of the map
1348: D 7→ uD vD meets every k-equivalence class of G-forms (§4.2.5).
1349: ABELIANTS AND THEIR APPLICATION TO AN ELEMENTARY CONSTRUCTION OF JACOBIANS
1350:                                                                         23
1351: 
1352: 
1353: 4.2.7. Remark. The dictionary provided by Proposition 4.2.6 is essentially just a
1354: chapter of algebro-geometrical folklore, cf. [Eisenbud Koh Stillman 1988, Prop. 1.1].
1355: The Eisenbud-Koh-Stillman paper greatly inspired us. Our presentation of the
1356: dictionary is a much simplified version of the presentation in [Anderson 1997].
1357: 4.3. Matrix representation of divisor class addition and subtraction.
1358: 4.3.1. A theorem of Mumford. By [Mumford 1970, Thm. 6, p. 52] we have
1359:                              
1360:             deg D ≥ 2g + 1
1361: (50)                           ⇒ L(D + E) = k-span of L(D) · L(E)
1362:             deg E ≥ 2g
1363: for all divisors D and E.
1364: 4.3.2. Kronecker products. Given a p by q matrix A and an r by s matrix B both
1365: with entries in some ring R, the Kronecker product A ◦ B is defined to be the pr
1366: by qs matrix with entries in R admitting a decomposition into r by s blocks of the
1367: form                                                  
1368:                                              ..
1369:                                              .        
1370:                           A◦B =    . . . Aij   B ... 
1371:                                                        .
1372:                                               ..
1373:                                                .
1374: The Kronecker product of matrices is compatible with ordinary matrix multiplica-
1375: tion in the sense that
1376:                             (A ◦ B)(X ◦ Y ) = (AX) ◦ (BY )
1377: whenever AX and BY are defined.
1378: Proposition 4.3.3. Let divisors G, G′ , D and D′ be given subject to the following
1379: conditions:
1380:                       deg G = 2 · deg D, deg G′ = 2 · deg D′ ,
1381:                                                             
1382:               1        1                       1       1
1383:        min      deg G, deg G′ ≥ 2g, max          deg G, deg G′ ≥ 2g + 1.
1384:               2        2                       2       2
1385: Put
1386:                          1                     1
1387:                     n = deg G − g + 1, n′ = deg G′ − g + 1,
1388:                          2                     2
1389: and
1390:                        1
1391:                  n′′ = (deg G + deg G′ ) − g + 1 = n + n′ + g − 1.
1392:                        2
1393: Fix a G-form X representing D and a G′ -form X ′ representing D′ . Let P and Q
1394: be any nn′ by nn′ permutation matrices and consider the block decomposition
1395:                                                     
1396:                                                a b
1397:                             P (X ◦ X ′ ) Q =
1398:                                                c d
1399: where the block d is n′′ by n′′ and the other blocks are of the appropriate sizes. (i)
1400: For some P and Q the corresponding block d is k-general. (ii) For any P and Q
1401: such that d is k-general, d is a (G + G′ )-form representing D + D′ .
1402: Proof. Write X = uv and X ′ = u′ v ′ where u (resp. v, u′ , v ′ ) is a column (resp. row,
1403: column, row) vector with entries forming a k-basis of L(D) (resp. L(G − D), L(D′ ),
1404: L(G′ − D′ )).
1405:    (i) By Mumford’s theorem (50) the entries of u ◦ u′ span L (D + D′ ) over k and
1406: hence for some permutation matrix P the last n′′ entries of the vector P (u ◦ u′ ) form
1407: a k-basis of L (D + D′ ). Similarly, the entries of v ◦ v ′ span L (G + G′ − D − D′ )
1408: 24                               GREG W. ANDERSON
1409: 
1410: 
1411: over k and for some permutation matrix Q the last n′′ entries of (v ◦ v ′ ) Q form
1412: a k-basis of L (G + G′ − D − D′ ). With P and Q thus chosen the block d is a
1413: (G + G′ )-form representing D + D′ and a fortiori k-general.
1414:    (ii) Now suppose we are given P and Q such that d is k-general. Then the
1415: last n′′ entries of P (u ◦ u′ ) are forced to be k-linearly independent and hence to
1416: form a k-basis of L (D + D′ ). Similarly the last n′′ entries (v ◦ v ′ ) Q are forced to
1417: form a k-basis of L (G + G′ − D − D′ ). Then the block d is indeed a (G + G′ )-form
1418: representing D + D′ .
1419: Lemma 4.3.4. Let E be a nonzero effective divisor. Let RE be the ring consisting
1420: of the meromorphic functions on C regular in a neighborhood of the support of E
1421: and let IE ⊂ RE be the ideal consisting of functions vanishing to order at least E.
1422: Then there exists a k-linear functional
1423:                                      σ : RE → k
1424: factoring through the quotient RE /IE such that the induced k-bilinear map
1425: (51)          ((a mod IE , b mod IE ) 7→ σ(ab)) : RE /IE × RE /IE → k
1426: is a perfect pairing of (deg E)-dimensional vector spaces over k.
1427: Proof. Choose any meromorphic differential ω on C such that
1428:                                  ordx ω + ordx E = 0
1429: for all points x ∈ supp E, where ordx abbreviates “order of vanishing at x”. Then,
1430: so we claim, the k-linear functional
1431:                                               
1432:                                  X
1433:                         a 7→         Resx (aω) : RE → k
1434:                                x∈supp E
1435: 
1436: has all the desired properties. The proof of the claim is an exercise in residue
1437: calculus we can safely omit.
1438: Lemma 4.3.5. Let G and E be divisors such that
1439:                                       1
1440:               deg G ≡ 0 mod 2, E > 0,   deg G − deg E > 2g − 2.
1441:                                       2
1442: There exists a k-linear functional
1443:                                      ρ : L(G) → k
1444:                                 L(G)
1445: factoring through the quotient L(G−E) such that for all divisors D of degree 21 deg G
1446: the induced k-bilinear map
1447:                                                       L(D)     L(G−D)
1448:        ((a + L(D − E), b + L(G − D − E)) 7→ ρ(ab)) : L(D−E) × L(G−D−E) →k
1449: is a perfect pairing of (deg E)-dimensional vector spaces over k.
1450: Proof. For each divisor D choose a meromorphic function fD on C such that
1451:                                    ordx f = ordx D
1452: for all points x ∈ supp E; then we have
1453:                            −1              −1
1454:                    L(D) ⊆ fD  RE , L(D) ∩ fD  IE = L(D − E),
1455: where RE and IE are as defined in Lemma 4.3.4. Now choose a k-linear functional
1456: σ : RE → k such that the pairing (51) is perfect and put
1457:                            ρ = (x 7→ σ(fG x)) : L(G) → k,
1458: ABELIANTS AND THEIR APPLICATION TO AN ELEMENTARY CONSTRUCTION OF JACOBIANS
1459:                                                                         25
1460: 
1461:                                                                        L(G)
1462: thereby defining a k-linear functional factoring through the quotient L(G−E) . Sup-
1463:                          1
1464: pose now that deg D = 2 deg G and consider the commutative diagram
1465:                    L(D)           L(G−D)      ×     L(G)      ρ
1466:                   L(D−E)    ×    L(G−D−E)     →    L(G−E)    → k
1467:                     ↓               ↓                ↓         ↓
1468:                                               ×              σ
1469:                   RE /IE    ×     RE /IE      →    RE /IE    → k
1470: where the vertical arrows are induced by multiplication by
1471:                                          −1
1472:                                 fD , fG fD  , fG , 1,
1473: respectively. By construction all the vertical arrows are injective and of course the
1474: last is bijective. Further, the source of each vertical arrow other than the last is
1475: of dimension over k equal to deg E by Riemann-Roch. Therefore all the vertical
1476: arrows are bijective and hence ρ has the desired nondegeneracy property.
1477: 4.3.6. Compression functionals. In the situation of Lemma 4.3.5 we call ρ : L(G) →
1478: k an E-compression functional. To make the calculations below run smoothly it is
1479: convenient to introduce in this context the following notation. Given any matrix
1480: Y with entries in L(G), let ρY be the result of applying ρ entrywise to Y , i. e., the
1481: matrix with entries in k defined by the rule (ρY )ij = ρYij .
1482: Proposition 4.3.7. Let G and E be divisors such that
1483:                                             1
1484:                deg G ≡ 0 mod 2, E > 0,        deg G − deg E ≥ 2g
1485:                                             2
1486: and put
1487:             1                               1
1488:         n = deg G − deg E − g + 1, n′ = deg G − g + 1 = n + deg E.
1489:             2                               2
1490: Let ρ : L(G) → k be an E-compression functional. Let D be a divisor of degree
1491: 1                                                                     ′     ′
1492: 2 deg G and let X be a G-form representing D. Let P and Q be any n by n
1493: permutation matrices and consider the block decomposition
1494:                                                
1495:                                           a b
1496:                                P XQ =
1497:                                           c d
1498: where the block a is deg E by deg E, the block d is n by n and the other blocks are
1499: of the appropriate sizes. (i) For some P and Q we have det ρa 6= 0. (ii) For any
1500: P and Q such that det ρa 6= 0 the matrix z defined by the rule
1501:                                                                  
1502:            w x                 1       0      a b       1 −(ρa)−1 (ρb)
1503:                     =
1504:             y z          −(ρc)(ρa)−1 1        c d       0       1
1505: is a (G − 2E)-form representing D − E.
1506: Proof. Write X = uv where u (resp. v) is a column (resp. row) vector with entries
1507: forming a k-basis of L(D) (resp. L(G − D)).
1508:    (i) For suitably chosen permutation matrices P and Q the first deg E entries of
1509: the column vector P u (resp. row vector vQ) project to a k-basis of the quotient
1510:   L(D)            L(G−D)
1511: L(D−E) (resp. L(G−D−E) ). For such P and Q we have det ρa 6= 0 by definition of
1512: E-compression functional.
1513:    (ii) After replacing X by P XQ
1514:                                 we may assume that P = Q = 1. After replacing
1515:                                 w x
1516: X by the k-equivalent matrix            we may assume that
1517:                                  y z
1518:                            det ρa 6= 0, ρb = 0, ρc = 0,
1519: 26                               GREG W. ANDERSON
1520: 
1521: 
1522: in which case our task is simply to show that the block d is a (G − 2E)-form. By
1523: definition of E-compression functional the first deg E entries of u (resp. v) project
1524:                                L(D)            L(G−D)
1525: to a k-basis of the quotient L(D−E)   (resp. L(G−D−E)   ). Also by definition of E-
1526: compression functional the last n entries of u must belong to L(D − E) and since
1527: k-linearly independent must form a k-basis of L(D −E). Similarly the last n entries
1528: of v must form a k-basis of L(G − D − E). Therefore d is indeed a (G − 2E)-form
1529: representing D − E.
1530: 
1531: 4.4. Completion of the construction.
1532: 
1533: 4.4.1. Candidate for the Jacobian. Fix an effective divisor E of degree ≥ 2g + 1
1534: and put
1535:      S = C \ supp E, A = H 0 (S, OC ),    n = ℓ(E) = deg E − g + 1, L = L(2E).
1536: The projective algebraic variety J of k-proportionality classes of Jacobi matrices of
1537: type (k, n, A, L) is our candidate for the Jacobian of C.
1538: 
1539: 4.4.2. Candidate for the Abel map. For each divisor D of degree zero arbitrarily
1540: fix a 2E-form XD representing D + E. Now a 2E-form is the same thing as a
1541: Segre matrix of type (k, n, A, L). By Proposition 4.2.6 it follows that the map
1542: D 7→ XD puts the divisor classes of degree zero in bijective correspondence with
1543: the k-equivalence classes of Segre matrices of type (k, n, A, L). For each divisor
1544: D of degree zero let ZD be the image of XD under the abstract Abel map. By
1545: Theorem 3.7.6 it follows that the map D 7→ ZD puts the classes of divisors of
1546: degree zero into bijective correspondence with the points of J. The bijective map
1547: from classes of divisors of degree zero to J induced by the map D 7→ ZD is our
1548: candidate for the Abel map.
1549:                                                                         T
1550: Lemma 4.4.3. For all divisors D of degree zero, X−D is k-equivalent to XD , and
1551:                                   T
1552: (hence) Z−D is k-proportional to ZD .
1553: Proof. This boils down to the transpose symmetry (4) of the abeliant.
1554: Lemma 4.4.4. Fix an E-compression functional ρ : L(4E) → k. Fix Segre matri-
1555: ces X and X ′ of type (k, n, A, L). Fix a divisor D (resp. D′ ) such that X (resp. X ′ )
1556: is k-equivalent to XD (resp. XD′ ). Let P and Q be any n2 by n2 permutation ma-
1557: trices and consider the block decomposition
1558:                                                         
1559:                                                 • • •
1560:                             P (X ◦ X ′ ) Q =  • a b 
1561:                                                 • c d
1562: where the block a is deg E by deg E, the block d is n by n, the other blocks are of
1563: the appropriate sizes, and the bullets hold places for blocks the contents of which do
1564: not concern us. Further, consider the block-decomposed matrix
1565:                                                                             
1566:     w x                     det ρa        0        a b        det ρa −(ρa)⋆ (ρb)
1567:             = det ρa ·                                                               .
1568:     y z                  −(ρc)(ρa)⋆ det ρa          c d         0        det ρa
1569: (i) For some P and Q the corresponding block z is k-general. (ii) For any P and
1570: Q such that the corresponding block z is k-general, z is a Segre matrix of type
1571: (k, n, A, L) and moreover z is k-equivalent to XD+D′ .
1572: ABELIANTS AND THEIR APPLICATION TO AN ELEMENTARY CONSTRUCTION OF JACOBIANS
1573:                                                                         27
1574: 
1575: 
1576: Proof. (i) By Propositions 4.3.3 and 4.3.7 there exist P and Q such that the fol-
1577: lowing hold:
1578:                   
1579:            a   b
1580:    •                   is a 4E-form representing D + D′ + 2E.
1581:            c   d
1582:    • det ρa 6= 0.
1583: 
1584:    • z is a 2E-form representing D + D′ + E.
1585: 
1586: A fortiori z is k-general.
1587: 
1588:   (ii) By hypothesis we have
1589:                                 det ρw 6= 0, ρx = 0, ρy = 0,
1590: and there exists a factorization
1591:                                                         
1592:                                w       x               p                  
1593:                                                =                   r   s
1594:                                y       z               q
1595: where the entries of the column vector (resp. row vector) on the right belong to
1596: L(D + D′ + 2E) (resp. L(−D − D′ + 2E)), the blocks p and r are vectors of
1597: length deg E, and the blocks q and s are vectors of length n. By definition of
1598: E-compression functional (Lemma 4.3.5) it follows that the entries of p (resp. r)
1599:                                                ′
1600:                                                  +2E)       L(−D−D′ +2E)
1601: project to a k-basis of the quotient L(D+D
1602:                                          L(D+D′ +E) (resp. L(−D−D′ +E) ). Also by
1603: definition of 2E-compression functional it follows that the entries of q (resp. s)
1604: belong to L(D + D′ + E) (resp. L(−D − D′ + E)). Finally, since z = qs is k-general,
1605: the entries of q (resp. s) must be k-linearly independent, and hence the entries of q
1606: (resp. s) must form a k-basis of L(D + D′ + E) (resp. L(−D − D′ + E)). Therefore
1607: the block z is indeed a 2E-form representing D + D′ + E and hence k-equivalent
1608: to XD+D′ .
1609: Lemma 4.4.5. Fix an E-compression functional ρ : L(4E) → k. Fix Jacobi ma-
1610: trices Z and Z ′ of type (k, n, A, L) with discriminants ∆ and ∆′ , respectively. Fix
1611: a divisor D (resp. D′ ) of degree zero such that Z (resp. Z ′ ) is k-proportional to ZD
1612: (resp. ZD′ ). For any s, s′ ∈ S {1,...,n+1} and any n2 by n2 permutation matrices P
1613: and Q consider the block decomposition
1614:                                                              
1615:                                                      • • •
1616:                        P ((Zks ) ◦ (Z ′ ks′ )) Q =  • a b  ,
1617:                                                      • c d
1618: where the block a is deg E by deg E, the block d is n by n, the other blocks are of
1619: the appropriate sizes, and the bullets hold places for blocks the contents of which do
1620: not concern us. Consider the block decomposed matrix
1621:                                                                                   
1622:   w x               ′                det ρa        0        a b       det ρa −(ρa)⋆ (ρb)
1623:            = ∆ks ·∆ ks′ ·det ρa·
1624:    y z                             −(ρc)(ρa)⋆ det ρa        c d         0        det ρa
1625: and finally put
1626:                                   Z ′′ = abeln+1
1627:                                              ℓ=0 z
1628:                                                    (ℓ)
1629:                                                        .
1630:                      ′                        ′′
1631: (i) There exist s, s , P and Q such that Z does not vanish identically. (ii) For
1632: any s, s′ , P and Q such that Z ′′ does not vanish identically, Z ′′ is a Jacobi matrix
1633: of type (k, n, A, L) and moreover Z ′′ is k-proportional to ZD+D′ .
1634: 28                                   GREG W. ANDERSON
1635: 
1636: 
1637: Proof. (i) By Proposition 3.7.2 there exists s ∈ S {1,...,n+1} (resp. s′ ∈ S {1,...,n+1} )
1638: such that ∆ks (resp. ∆′ ks′ ) is a nonzero scalar and hence the corresponding par-
1639: tially specialized matrix Zks (resp. Z ′ ks′ ) is k-equivalent to XD (resp. XD′ ). By
1640: Lemma 4.4.4 there exist P and Q such that the block z is k-general. Finally, Z ′′
1641: does not vanish by Proposition 3.4.3.
1642:    (ii) By Proposition 3.7.2 and hypothesis the partial specialization ∆ks
1643: (resp. ∆′ ks′ ) is a nonzero scalar and hence the corresponding partial specializa-
1644: tion Zks (resp. Z ′ ks′ ) is a Segre matrices of type (k, n, A, L) that is k-equivalent
1645: to XD (resp. XD′ ). By hypothesis det ρa is a nonzero scalar and hence z is by
1646: Lemma 4.4.4 a Segre matrix of type (k, n, A, L) that is k-equivalent to XD+D′ . Fi-
1647: nally, since Z ′′ is the image of z under the abstract Abel map, Z ′′ is k-proportional
1648: to ZD+D′ .
1649: Theorem 4.4.6. There is exactly one way to equip our candidate for the Jacobian
1650: ( §4.4.1) with the structure of algebraic group so that our candidate for the Abel
1651: map ( §4.4.2) becomes a group homomorphism. (Thus our candidates become the
1652: Jacobian and the Abel map.)
1653: Proof. Since our candidate for the Abel map is bijective, the set underlying J comes
1654: canonically equipped with a group law. The only issue remaining to be resolved
1655: is whether or not that group law is algebraic, i. e., expressible Zariski-locally by
1656: regular functions. Well, by Lemma 4.4.3 the inversion operation in J is algebraic,
1657: and by Lemma 4.4.5 the addition operation in J is algebraic. We’re done.
1658: 4.5. Remark. To give some indication of how the complexity of our construction
1659: of J grows as a function of the genus of C, we make the following observation.
1660: Suppose that C is a nonsingular plane algebraic curve of degree d ≥ 3 and hence
1661: genus (d−1)(d−2)
1662:            2       > 0 with defining equation F = F (x, y, z) ∈ k[x, y, z]. By the
1663: method of proof of Theorem 4.4.6 the divisor classes of C of degree zero can be put
1664: in natural bijective correspondence with the k-equivalence classes of Segre matrices
1665: of type
1666:                                                                          
1667:                  d(d − 1)
1668: (52)          k,          , k[x, y, z]/(F ), {forms of degree 2d − 4}/(F )
1669:                      2
1670: and in turn the Jacobian of C can be identified with the projective variety of k-
1671: proportionality classes of Jacobi matrices of type (52).
1672: 
1673:                                  5. Acknowledgements
