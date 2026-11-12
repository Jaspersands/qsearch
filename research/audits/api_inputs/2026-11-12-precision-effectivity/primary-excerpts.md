SOURCE research/audits/sources/classical_surface_2026/javanpeykar.txt
https://arxiv.org/pdf/1403.6404
SHA256 59357cc190f89098d32e4dd1d1c1c7802e25b26aeeea3a8766cafea8089086bc

Physical lines 404-514:
2.3. Arakelov invariants of curves. Let X be a smooth projective connected curve over Q of
genus g ≥ 1. Let K be a number field such that X has a semi-stable minimal regular model
p : X → Spec OK ; see Theorems 10.1.8, 10.3.34.a and 10.4.3 in [29]. (Note that we implicitly
chose an embedding K → Q.)
    The Faltings delta invariant of X, denoted by δFal (X), is defined as
                                              1     X
                                 δFal (X) =               δFal (Xσ ),
                                            [K : Q]
                                                     σ:K→C

where σ runs over the complex embeddings of K into C. Similarly, we define
                                                          !1/[K:Q]
                                        Y
                         kϑkmax (X) =           max kϑk            .
                                                   Picg−1 (Xσ )
                                           σ:K→C
                 POLYNOMIAL BOUNDS FOR ARAKELOV INVARIANTS OF BELYI CURVES                           9


Moreover, we define
                                           !1/[K:Q]                                 !1/[K:Q]
                           Y                                             Y
                R(X) =            R(Xσ )              ,    S(X) =             S(Xσ )           .
                          σ:K→C                                      σ:K→C
The Faltings height of X is defined by
                                      d det p∗ ωX /O
                                      deg               d det R· p∗ OX
                                                        deg
                                                    K
                         hFal (X) =                   =                ,
                                          [K : Q]           [K : Q]
where we endow the determinant of cohomology with the Faltings metric; see Section 2.1. Note
that hFal (X) coincides with the stable Faltings height of the Jacobian of XK ; see [41, Lemme 3.2.1,
Chapitre I]. Furthermore, we define the self-intersection of the dualizing sheaf of X, denoted by
e(X), as
                                            (ωX /OK , ωX /OK )
                                      e(X) :=                  ,
                                                 [K : Q]
where we use Arakelov’s intersection pairing on the arithmetic surface X /OK . The discriminant
of X, denoted by ∆(X), is defined as
                                               P
                                                   p⊂OK δp log #k(p)
                                   ∆(X) =                                ,
                                                          [K : Q]
where p runs through the maximal ideals of OK and δp denotes the number of singularities in the
geometric fibre of p : X → Spec OK over p. These invariants of X are well-defined; see [36, Section
5.4].
   To bound the above Arakelov invariants, we introduce two functions on X(Q): the height and
the Arakelov norm of the Wronskian differential. More precisely, let b ∈ X(Q) and suppose that
b induces a section P of X over OK . Then we define the height of b, denoted by h(b), to be
                                        d
                                        degP ∗ ωX /OK   (P, ωX /OK )
                               h(b) =                 =              .
                                           [K : Q]        [K : Q]
Note that the height of b is the stable canonical height of a point, in the Arakelov-theoretic sense,
with respect to the admissible line bundle ωX /OK . We define the Arakelov norm of the Wronskian
differential at b as                                                 !1/[K:Q]
                                                 Y
                            kWrkAr (b) =                  kWrkAr (bσ )          .
                                               σ:K→C
These functions on X(Q) are well-defined; see [36, Section 5.4].
   Changing the model for X might change the height of a point. Let us show that the height of
a point does not become smaller if we take another regular model over OK .

Lemma 2.3.1. Let Y → Spec OK be an arithmetic surface. Assume that Y is a model for XK .
If Q denotes the section of Y over OK induced by b ∈ X(Q), then
                                                    (Q, ωY/OK )
                                           h(b) ≤               .
                                                      [K : Q]
Proof. By the minimality of X , there is a unique birational morphism φ : Y → X ; see [29,
Corollary 9.3.24]. By the factorization theorem, this morphism is made up of a finite sequence

                           Y = Yn
                                      φn
                                             / Yn−1 φn−1 / . . .    φ1
                                                                         / Y0 = X
 10                     ARIYAN JAVANPEYKAR WITH AN APPENDIX BY PETER BRUIN


of blowing-ups along closed points; see [29, Theorem 9.2.2]. For i = 1, . . . , n, let Ei ⊂ Yi denote
the exceptional divisor of φi . Since the line bundles ωYi /OK and φ∗i ωYi−1 /OK agree on Yi − Ei ,
there is an integer a such that

                                   ωYi /OK = φ∗i ωYi−1 /OK ⊗OYi OYi (aEi ).

Applying the adjunction formula, we see that a = 1. Since φi restricts to the identity morphism
on the generic fibre, we have a canonical isomorphism of admissible line bundles

                                   ωYi /OK = φ∗i ωYi−1 /OK ⊗OYi OYi (Ei ).

Let Qi denote the section of Yi over OK induced by b ∈ X(Q). Then

        (Qi , ωYi /OK ) = (Qi , φ∗i ωYi−1 /OK ) + (Qi , Ei ) ≥ (Qi , φ∗i ωYi−1 /OK ) = (Qi−1 , ωYi−1 /OK ),

where we used the projection formula in the last equality. Therefore, we conclude that

              (Q, ωY/OK ) = (Qn , ωYn /OK ) ≥ (Q0 , ωY0 /OK ) = (P, ωX /OK ) = h(b)[K : Q].                    

2.4. Bounding Arakelov invariants in the height of a non-Weierstrass point. In this
section we prove bounds for Arakelov invariants of curves in the height of a non-Weierstrass point
and the Arakelov norm of the Wronskian differential in this point.

Theorem 2.4.1. Let X be a smooth projective connected curve over Q of genus g ≥ 1. Let
b ∈ X(Q). Then
                           e(X)     ≤           4g(g − 1)h(b),
                         δFal (X) ≥ −90g 3 − 4g(2g − 1)(g + 1)h(b).
Suppose that b is not a Weierstrass point. Then
                                       1
                    hFal (X) ≤         2 g(g + 1)h(b) + log kWrkAr (b),
                    δFal (X) ≤ 6g(g + 1)h(b) + 12 log kWrkAr (b) + 4g log(2π),
                     ∆(X) ≤ 2g(g + 1)(4g + 1)h(b) + 12 log kWrkAr (b) + 93g 3 .

Physical lines 716-741:
Definition 3.1.1. A Merkl atlas for X is a quadruple ({(Uj , zj )}nj=1 , r1 , M, c1 ), where {(Uj , zj )}nj=1
is a finite atlas for X, 12 < r1 < 1, M ≥ 1 and c1 > 0 are real numbers such that the following
properties are satisfied.
      (1) Each zj Uj is the open unit disc.
      (2) The open sets Ujr1 := {x ∈ Uj : |zj (x)| < r1 } with 1 ≤ j ≤ n cover X.
      (3) For all 1 ≤ j, j ′ ≤ n, the function |dzj /dzj ′ | on Uj ∩ Uj ′ is bounded from above by M .
      (4) For 1 ≤ j ≤ n, write µAr = iFj dzj ∧ dzj on Uj . Then 0 ≤ Fj (x) ≤ c1 for all x ∈ Uj .

     Given a Merkl atlas ({(Uj , zj )}nj=1 , r1 , M, c1 ) for X, the following result provides explicit bounds
for Arakelov-Green functions in n, r1 , M and c1 .

Theorem 3.1.2 (Merkl). Let ({(Uj , zj )}nj=1 , r1 , M, c1 ) be a Merkl atlas for X. Then
                                         330n            1
                       sup grX ≤                   log        + 13.2nc1 + (n − 1) log M.
                     X×X\∆            (1 − r1 )3/2     1 − r1
Furthermore, for every index j and all x 6= y ∈ Ujr1 , we have
                                                       330n            1
          | grX (x, y) − log |zj (x) − zj (y)|| ≤                log        + 13.2nc1 + (n − 1) log M.
                                                    (1 − r1 )3/2     1 − r1

Proof. Merkl proved this theorem without explicit constants and without the dependence on r1
in [33]. A proof of the theorem in a more explicit form was given by P. Bruin in his master’s
thesis. This proof is reproduced, with minor modifications, in the appendix.                                 

3.2. An atlas for a Belyi cover of X(2). Let H denote the complex upper half-plane. Recall
that SL2 (R) acts on H via Möbius transformations. Let Γ(2) denote the subgroup of SL2 (Z)

Physical lines 1314-1438:
   Let us introduce a bit more notation. Let I1 be the set of i in I such that Di is horizontal (i.e.,
                                  P
pi = 0) or pi > deg π. Let D1 = i∈I1 Di . We are now finally ready to combine our results to
bound the “non-archimedean” part of the height of a point.

Proposition 4.2.4. Let P ′ : S → Y ′ be a section, and let Q : S → X be the induced section. If
the image of P ′ is not contained in the support of KY ′ , then

                     (KY ′ , P ′ )fin ≤ deg π(D1 , Q)fin + 2(deg π)2 log(deg π)[K : Q].

Proof. Note that                                                        
                                                  X         X
                                          B=                      rij fij  Di .
                                                  i∈I       j∈Ji
                                                                    P
Let I2 be the complement of I1 in I. Let D2 =                           i∈I2 Di , and note that D              = D1 + D2 . In
particular,
                                     XX
                  (B, Q)fin    =                 rij fij (Di , Q)fin
                                     i∈I j∈Ji
                                     XX                                    XX
                               =                 rij fij (Di , Q)fin +                 rij fij (Di , Q)fin .
                                     i∈I1 j∈Ji                             i∈I2 j∈Ji

Note that, for all i in I1 and j in Ji , the ramification of Dij over Di is tame, i.e., the equality
                                                          P
rij = eij − 1 holds. Note that, for all i in I, we have j∈Ji eij fij = deg π. Thus,
                XX                            XX
                        rij fij (Di , Q)fin ≤       eij fij (Di , Q)fin = deg π(D1 , Q)fin .
                i∈I1 j∈Ji                         i∈I1 j∈Ji

We claim that
                        XX
                                    rij fij (Di , Q)fin ≤ 2(deg π)2 log(deg π)[K : Q].
                        i∈I2 j∈Ji
                  POLYNOMIAL BOUNDS FOR ARAKELOV INVARIANTS OF BELYI CURVES                                            25


In fact, since, for all i in I2 and j in Ji , by Proposition 4.2.3, the inequality

                                                       rij ≤ 2eij mi epi

holds, we have that
                                                                                                           
                   XX                                           X                               X
                                 rij fij (Di , Q)fin   ≤    2          mi epi (Di , Q)fin            eij fij 
                  i∈I2 j∈Ji                                     i∈I2                           j∈Ji
                                                                          X
                                                       =    2(deg π)             mi epi (Di , Q)fin .
                                                                          i∈I2

Note that (Di , Q) = log(#k(pi )) = fpi log pi . We conclude that
                                                                   
             X                            X         X                               
                                                                       log(deg π)
                  mi epi (Di , Q)fin =                      epi fpi                 log(p)
                                                                           log p
            i∈I2                        p prime i∈I2 ,pi =p
                                                    X   log(deg π)  
                                     = [K : Q]                              log(p),
                                                                 log p
                                                             Xp ∩|D2 |6=∅

where the last sum runs over all prime numbers p such that the fibre Xp contains an irreducible
component of the support of D2 . Thus,
                                                                                   X                       
                                                                                               log(deg π)
            (B, Q)fin ≤ (deg π)(D1 , Q)fin + 2(deg π)[K : Q]                                                log(p).
                                                                                                  log p
                                                                              Xp ∩D2 6=∅

Note that
                   X                                            X
                                 log(deg π)
                                              log(p) ≤                   log(deg π) ≤ deg π log(deg π),
                                    log p
                Xp ∩D2 6=∅                                 Xp ∩D2 6=∅

where we used that Xp ∩ D2 6= ∅ implies that p ≤ deg π. In particular,

                      (B, Q)fin ≤ (deg π)(D1 , Q)fin + 2(deg π)2 log(deg π)[K : Q].

By Proposition 4.2.2, we conclude that

                    (KY ′ , P ′ )fin ≤ (deg π)(D1 , Q)fin + 2(deg π)2 log(deg π)[K : Q].                               

4.3. Models of covers of curves. In this section, we give a general construction for a model
of a cover of the projective line. Let K be a number field with ring of integers OK , and let
S = Spec OK .

Proposition 4.3.1. Let Y → Spec OK be a flat projective morphism with geometrically connected
fibres of dimension one, where Y is an integral normal scheme. Then, there exists a finite field
extension L/K such that the minimal resolution of singularities of the normalization of Y ×OK OL
is semi-stable over OL .

Proof. This follows from [30, Corollary 2.8].                                                                          

   The main result of this section reads as follows.

Theorem 4.3.2. Let K be a number field, and let Y be a smooth projective geometrically connected
curve over K. Then, for any finite morphism πK : Y → P1K , there exists a number field L/K such
that:
 26                   ARIYAN JAVANPEYKAR WITH AN APPENDIX BY PETER BRUIN


       • the normalization π : Y → P1OL of P1OL in the function field of YL is finite flat surjective;
       • the minimal resolution of singularities ψ : Y ′ −→ Y is semi-stable over OL ;
       • each irreducible component of the vertical part of the branch locus of the finite flat mor-
          phism π : Y → P1OL is of characteristic less than or equal to deg π. (The characteristic
          of a prime divisor D on P1OL is the residue characteristic of the local ring at the generic
          point of D.)

Proof. By Proposition 4.3.1, there exists a finite field extension L/K such that the minimal res-
olution of singularities ψ : Y ′ −→ Y of the normalization of P1OL in the function field of YL is
semi-stable over OL . Note that the finite morphism π : Y → P1OL is flat. (The source is normal of
dimension two, and the target is regular.) Moreover, since the fibres of Y ′ → Spec OL are reduced,
the fibres of Y over OL are reduced. Let p ⊂ OL be a maximal ideal of residue characteristic
strictly bigger than deg π, and note that the ramification of π : Y → P1OL over (each prime divisor
of P1OL lying over) p is tame. Since the fibres of Y → Spec OL are reduced, we see that the finite
morphism π is unramified over p. In fact, since P1OL → Spec OL has reduced (even smooth) fibres,
the valuation of the different ideal DOD /Oπ(D) on OD of an irreducible component D of Yp lying
over π(D) in X is precisely the multiplicity of D in Yp . (Here we let OD denote the local ring
at the generic point of D, and Oπ(D) the local ring at the generic point of π(D).) Thus, each
irreducible component of the vertical part of the branch locus of π : Y → P1OL is of characteristic
less or equal to deg π.                                                                                          

SOURCE research/audits/sources/surface_module_2026/couveignes_edixhoven_book.txt
Retained author book; source metadata in existing corpus
SHA256 0ae7a4befba82ce944abeb0f71f745403bcbb9c8418232d050c8e6effba83dd9

Physical lines 9349-9375:
In this subsection, the hypotheses are as follows (unless stated otherwise).
We let K be a number field, OK its ring of integers, B WD Spec.OK /,
pW X ! B a regular, split semistable curve over B whose generic fiber
X ! Spec K is geometrically irreducible and of genus g   1. We let D be
the closure in X of an effective divisor of degree g (also denoted D) on X .
                       bookcourant     January 8, 2011




196                                                                  CHAPTER 9

We let x be a K-rational torsion point of the Jacobian of X, that is, a torsion
element of Pic.X /, which has the property that there is a unique effective
divisor Dx on X such that x D ŒDx D. Finally, we let P W B ! X be a
section of p, that is, an element of X .B/.
   We denote by ˆx;P the unique finite vertical fractional divisor ˆ (that
is, with rational coefficients that are not necessarily integral) on X such that
.Dx D ˆ; C / D 0 for all irreducible components C of fibers of p,
and such that P .B/ is disjoint from the support of ˆ. It is not difficult
to see that a ˆ satisfying the first condition exists and that it is unique up
to adding multiples of fibers of p (the intersection pairing restricted to the
divisors with support in a fiber is negative semidefinite); see Lemme 6.14.1
of [Mor2]. The second condition removes the ambiguity of adding multiples
of fibers.
   We denote by ıs the number of singular points in the geometric fiber at a
closed point s of B.

Physical lines 9538-9559:
9.2.5 Theorem We have an upper bound
                                         1
.Dx ; P / C log #R1 p  OX .Dx /            .D; D !X =B /
                                         2 X
                                       C 2g 2   ıs log #k.s/
                                                    s2B
                                            X                        g
                                       C            log k#k ;sup C     ŒK W Q log.2 /
                                                 
                                                                     2
                                        1
                                       C deg det p  !X =B C .D; P / ;
                                        2
                       bookcourant     January 8, 2011




200                                                                       CHAPTER 9

where s runs through the closed points of B, and where the supremum norm
k#k ;sup is taken over Picg 1 .X  /.