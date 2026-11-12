Primary Javanpeykar1403.6404; physical pdftotext lines1070-1738, retained PDF provenance as in merkl-source.md.
                                                                                   dwyl
                                                           l=0           k=1

Let r1 < r < 1 be some real number. By Cauchy’s integral formula, for any 0 ≤ l ≤ g − 1,
                        Z
      dl fk        l!                   fk                    l!                       g!
            (b) =                                  dwy ≤               sup |fk | ≤            sup |fk |.
      dwyl        2πi     |wy |=r (wy − wy (b))l+1       (r − r 1 )l+1
                                                                        Vy
                                                                                   (1 − r1 )g Vy

                                                  1
By the preceding estimations, since g! ≤ g g and 1−r 1
                                                       ≤ deg π
                                                         1−s1 , we obtain that

                             g−1
                                         
                                                              g
                                                                                    !1/2 
                             X                    g!          X
     log |Wwy (ω)(b)|   ≤             log                             sup |fk |2         
                                              (1 − r1 )g               Vy
                                l=0                           k=1
                                                                                                !1/2 
                             g−1
                             X                                g
                                                              X
                                        g!                      256 exp(3π)(deg π)4
                        ≤             log                                    
                                    (1 − r1 )g               π2
                          l=0                    k=1
                                                                            
                                       2          1       g      256g exp(3π)
                        = g log(g!) + g log             + log                    + 2g log(deg π)
                                               1 − r1     2           π2
                                                                   
                                           1        1      256 exp(3π)
                        ≤   4.5 + log             + log                   g 2 log(deg π)
                                        1 − s1      2           π2
                        ≤ 13g(deg π)2 .

Since g ≥ 1 and π : Y → X(2) is a Belyi cover, the inequality deg π ≥ 3 holds. Thus,

                                                           13g(deg π)5
                                     13g(deg π)2 ≤                     ≤ g(deg π)5 .                         
                                                               27
               POLYNOMIAL BOUNDS FOR ARAKELOV INVARIANTS OF BELYI CURVES                            21


                                 4. Points of bounded height

4.1. Lenstra’s generalization of Dedekind’s discriminant bound. Let A be a discrete val-
uation ring of characteristic zero with fraction field K. Let ordA denote the valuation on A. Let
L/K be a finite field extension of degree n, and let B be the integral closure of A in L. Note that
L/K is separable, and B/A is finite; see [39, Proposition I.4.8].
  The inverse different D−1
                         B/A of B over A is the fractional ideal

                                       {x ∈ L : Tr(xB) ⊂ A},

where Tr is the trace of L over K. The inverse of the inverse different, denoted by DB/A , is the
different of B over A. Note that DB/A is actually an integral ideal of L.
  The following proposition (which we would like to attribute to H.W. Lenstra jr.) is a general-
ization of Dedekind’s discriminant bound ( [39, Proposition III.6.13]).

Proposition 4.1.1. (H.W. Lenstra jr.) Let A be a discrete valuation ring of characteristic
zero with fraction field K, and let B be the integral closure of A in a finite field extension L/K of
degree n. Suppose that B is a discrete valuation ring of ramification index e over A. Then, the
valuation r of the different ideal DB/A on B satisfies the inequality

                                      r ≤ e − 1 + e · ordA (n).

                                                                                           1
Proof. Let x be a uniformiser of A. Since A is of characteristic zero, we may define y := nx ;
note that y is an element of K. The trace of y (as an element of L) is x1 . Since 1/x is not in
A, this implies that the inverse different D−1
                                            B/A is strictly contained in the fractional ideal yB. (If
not, since A and B are discrete valuation rings, we would have that yB is strictly contained in
the inverse different.) In particular, the different DB/A strictly contains the fractional ideal (nx).
Therefore, the valuation ordB (DB/A ) on B of DB/A is strictly less than the valuation of nx. Thus,

           ordB (DB/A ) < ordB (nx) = e · ordA (nx) = e(ordA (n) + 1) = e · ordA (n) + e.

This concludes the proof of the inequality.                                                         

Remark 4.1.2. If the extension of residue fields of B/A is separable, Proposition 4.1.1 follows
from the Remarque following Proposition III.6.13 in [39]. (The result in loc. cit. was conjectured
by Dedekind and proved by Hensel when A = Z.) The reader will see that, in the proof of
Proposition 4.2.4, we have to deal with imperfect residue fields.

Proposition 4.1.3. Let A be a discrete valuation ring of characteristic zero with fraction field K,
and let B be the integral closure of A in a finite field extension L/K of degree n. Suppose that the
residue characteristic p of A is positive. Let m be the biggest integer such that pm ≤ n. Then, for
β ⊂ B a maximal ideal of B with ramification index eβ over A, the valuation rβ of the different
ideal DB/A at β satisfies the inequality

                                    rβ ≤ eβ − 1 + eβ · ordA (pm ).
22                    ARIYAN JAVANPEYKAR WITH AN APPENDIX BY PETER BRUIN


                                                                         b and B
Proof. To compute rβ , we localize B at β, and then take the completions A     cβ of A and Bβ ,
                                     cβ over A.
respectively. Let d be the degree of B       b Then, by Lenstra’s result (Proposition 4.1.1), the
inequality
                                        rβ ≤ eβ − 1 + eβ · ordAb(d).

holds. By definition, ordAb(d) = ordA (d) ≤ ordA (pm ). This concludes the proof.                      

4.2. Covers of arithmetic surfaces with fixed branch locus. Let K be a number field with
ring of integers OK , and let S = Spec OK . Let D be a reduced effective divisor on X = P1S ,
and let U denote the complement of the support of D in X . Let Y → S be an integral normal
2-dimensional flat projective S-scheme with geometrically connected fibres, and let π : Y −→ X
be a finite surjective morphism of S-schemes which is étale over U . Note that π : Y −→ X is a flat
morphism. (The source is normal of dimension two, and the target is regular.) Let ψ : Y ′ → Y be
the minimal resolution of singularities ( [29, Proposition 9.3.32]). We have the following diagram
of morphisms
                                             ψ          π
                                       Y′        /Y           /X     / S.
                                                 P
Consider the prime decomposition D =              i∈I Di , where I   is a finite index set. Let Dij be an
                              −1
irreducible component of π         (D) mapping onto Di , where j is in the index set Ji . We define rij
to be the valuation of the different ideal of OY,Dij /OX ,Di . We define the ramification divisor R
      P P
to be i∈I j∈Ji rij Dij . We define B := π∗ R. (We call B the branch divisor of π : Y → X .)
     We apply [29, 6.4.26] to obtain that there exists a dualizing sheaf ωY/S for Y → S, and a
dualizing sheaf ωπ for π : Y → X such that the adjunction formula

                                            ωY/S = π ∗ ωX /S ⊗ ωπ

holds. Since the local ring at the generic point of a divisor on X is of characteristic zero, basic
properties of the different ideal imply that ωπ is canonically isomorphic to the line bundle OY (R).
We deduce the Riemann-Hurwitz formula

                                         ωY/S = π ∗ ωX /S ⊗ OY (R).

     Let KX = −2 · [∞] be the divisor defined by the tautological section of ωX /OK . Let KY ′
denote the Cartier divisor on Y ′ defined by the rational section d(π ◦ ψ) of ωY ′ /S . We define the
Cartier divisor KY on Y analogously, i.e., KY is the Cartier divisor on Y defined by dπ. Note
that KY = ψ∗ KY ′ . Also, the Riemann-Hurwitz formula implies the following equality of Cartier
divisors
                                             KY = π ∗ KX + R.

     Let E1 , . . . , Es be the exceptional components of ψ : Y ′ −→ Y. Note that the pull-back of the
Cartier divisor ψ ∗ KY coincides with KY ′ on
                                                        s
                                                        [
                                                 Y′ −         Ei .
                                                        i=1
                POLYNOMIAL BOUNDS FOR ARAKELOV INVARIANTS OF BELYI CURVES                                  23


Therefore, there exist integers ci such that
                                                                      s
                                                                      X
                                                            ∗
                                             K   Y′   = ψ KY +              ci Ei ,
                                                                      i=1

where this is an equality of Cartier divisors (not only modulo linear equivalence). Note that
(ψ ∗ KY , Ei ) = 0 for all i. In fact, KY is linearly equivalent to a Cartier divisor with support
disjoint from the singular locus of Y.

Lemma 4.2.1. For all i = 1, . . . , s, we have ci ≤ 0.

Proof. We have the following local statement. Let y be a singular point of Y, and let E1 , . . . , Er
be the exceptional components of ψ lying over y. We define
                                              X r
                                      V+ =         ci Ei
                                                            i=1,ci >0

as the sum on the ci > 0. To prove the lemma, it suffices to show that V+ = 0. Since the
intersection form on the exceptional locus of Y ′ → Y is negative definite ( [29, Proposition 9.1.27]),
to prove V+ = 0, it suffices to show that (V+ , V+ ) ≥ 0. Clearly, to prove the latter inequality, it
suffices to show that, for all i such that ci > 0, we have (V+ , Ei ) ≥ 0. To do this, fix i ∈ {1, . . . , r}
with ci > 0. Since Y ′ → Y is minimal, we have that Ei is not a (−1)-curve. In particular, by the
adjunction formula, the inequality (KY ′ , Ei ) ≥ 0 holds. We conclude that
                                                                    r
                                                                    X
                              (V+ , Ei ) = (KY ′ , Ei ) −                    cj (Ej , Ei ) ≥ 0,
                                                                 j=1,cj <0

where, in the last inequality, we used that, for all j such that cj < 0, we have that Ej 6= Ei .           

Proposition 4.2.2. Let P ′ : S → Y ′ be a section, and let Q : S → X be the induced section. If
the image of P ′ is not contained in the support of KY ′ , then

                                             (KY ′ , P ′ )fin ≤ (B, Q)fin .

Proof. Note that, by the Riemann-Hurwitz formula, we have KY = π ∗ KX + R. Therefore, by
Lemma 4.2.1, we get that
                                                                   X
                          (KY ′ , P ′ )fin   =        (ψ ∗ KY +         ci Ei , P ′ )fin
                                                                                 s
                                                                                 X
                                             =        (ψ ∗ π ∗ KX + ψ ∗ R +             ci Ei , P ′ )fin
                                                                                  i=1
                                             ≤        (ψ ∗ π ∗ KX , P ′ )fin + (ψ ∗ R, P ′ )fin .

Since the image of P ′ is not contained in the support of KY ′ , we can apply the projection formula
for the composed morphism π ◦ ψ : Y ′ → X to (ψ ∗ π ∗ KX , P ′ )fin and (ψ ∗ R, P ′ )fin ; see [29, Sec-
tion 9.2]. This gives

             (KY ′ , P ′ )fin ≤ (ψ ∗ π ∗ KX , P ′ )fin + (ψ ∗ R, P ′ )fin = (KX , Q)fin + (π∗ R, Q)fin .

Since KX = −2 · [∞], the inequality (KX , Q)fin ≤ 0 holds. By definition, B = π∗ R. This concludes
the proof.                                                                                                 
24                   ARIYAN JAVANPEYKAR WITH AN APPENDIX BY PETER BRUIN


     We introduce some notation. For i in I and j in Ji , let eij and fij be the ramification index
and residue degree of π at the generic point of Dij , respectively. Moreover, let pi ⊂ OK be the
maximal ideal corresponding to the image of Di in Spec OK . Then, note that eij is the multiplicity
of Dij in the fibre of Y over pi . Now, let epi and fpi be the ramification index and residue degree
of pi over Z, respectively. Finally, let pi be the residue characteristic of the local ring at the
generic point of Di and, if pi > 0, let mi be the biggest integer such that pm
                                                                             i
                                                                               i
                                                                                 ≤ deg π, i.e.,
mi = ⌊log(deg π)/ log(pi )⌋.

Lemma 4.2.3. Let i be in I such that 0 < pi ≤ deg π. Then, for all j in Ji ,

                                                  rij ≤ 2eij mi epi .

Proof. Let ordDi be the valuation on the local ring at the generic point of Di . Then, by Proposition
4.1.3, the inequality
                                       rij ≤ eij − 1 + eij · ordDi (pm
                                                                     i )
                                                                       i



holds. Note that ordDi (pm
                         i ) = mi epi . Since pi ≤ deg π, we have that mi ≥ 1. Therefore,
                           i




                                    rij ≤ eij − 1 + eij mi epi ≤ 2eij mi epi .                                             

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
                                                    X  log(deg π) 
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
                   X                                          X
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

4.4. The modular lambda function. The modular function λ : H → C is defined as
                                                     
                                     p 12 + τ2 − p τ2
                             λ(τ ) =               ,
                                       p τ2 − p 12
where p denotes the Weierstrass elliptic function for the lattice Z + τ Z in C. The function λ is
Γ(2)-invariant. More precisely, λ factors through the Γ(2)-quotient map H → Y (2) and an analytic
                      ∼
isomorphism Y (2) −→ C − {0, 1}. Thus, the modular function λ induces an analytic isomorphism
X(2) → P1 (C). Let us note that λ(i∞) = 0, λ(1) = ∞ and λ(0) = 1.
     The restriction of λ to the imaginary axis {iy : y > 0} in H induces a homeomorphism, also
denoted by λ, from {iy : y > 0} to the open interval (0, 1) in R. In fact, for α in the open interval
(0, 1),
                                                             √
                                                        M(1, α)
                                      λ−1 (α) = i          √       ,
                                                       M(1, 1 − α)
where M denotes the arithmetic-geometric-mean.

                                                                           P∞          n
Lemma 4.4.1. For τ in H, let q(τ ) = exp(πiτ ) and let λ(τ ) =              n=1 an q       (τ ) be the q-expansion
of λ on H. Then, for any real number 4/5 ≤ y ≤ 1,
                                                ∞
                                                X
                                      − log |         nan q n (iy)| ≤ 2.
                                                n=1
                 POLYNOMIAL BOUNDS FOR ARAKELOV INVARIANTS OF BELYI CURVES                                          27


Proof. Note that
                                                    ∞
                                                    X                    dλ
                                                          nan q n = q       .
                                                    n=1
                                                                         dq
It suffices to show that |qdλ/dq| ≥ 3/20. We will use the product formula for λ. Namely,
                                                   ∞
                                                   Y                              1 + q 2n
                                    λ(q) = 16q           fn (q),    fn (q) :=               .
                                                   n=1
                                                                                 1 + q 2n−1

Write fn′ (q) = dfn (q)/dq. Then,
                                    ∞
                                                            !                   ∞
                                                                                                          !
                        dλ         X  fn′ (q)                                   X d
                      q    = λ 1+q                              =λ 1+q                     (log fn (q)) .
                        dq            f (q)
                                   n=1 n                                        n=1
                                                                                      dq

Note that, for any positive integer n and 4/5 ≤ y ≤ 1,
                                                   
                                        d
                                          log fn (q) (iy) ≤ 0.
                                       dq
Moreover, since λ(i) = 1/2 and λ(0) = 1, the inequality λ(iy) ≥ 1/2 holds for all 0 ≤ y ≤ 1. Also,
for 4/5 ≤ y ≤ 1,
                                                 ∞
                                                                      !
                                                 X d                                  7
                                           −q              log fn (q) (iy) ≤             .
                                                 n=1
                                                     dq                               10
In fact,
                       ∞
                       X                                   ∞
                                                           X                    ∞
                                                                                X
                         d                                   2nq 2n−1             (2n − 1)q 2n−2
                                    (log fn (q))    =                    2n
                                                                            −
                       n=1
                               dq                          n=1
                                                                   1+q          n=1
                                                                                             1 + q 2n−1

It is straightforward to verify that, for all 4/5 ≤ y ≤ 1, the inequality
     ∞
     X                         ∞
                               X                                        ∞                   ∞
       2nq 2n−1 (iy)             (2n − 1)q 2n−2 (iy)               100 X                   X
                           −                                  ≥            2nq 2n−1 (iy) −    (2n − 1)q 2n−2 (iy)
     n=1
           1 + q 2n (iy)       n=1
                                       1 + q 2n−1 (iy)             109 n=1                 n=1

holds. Finally, utilizing classical formulas for geometric series, for all 4/5 ≤ y ≤ 1,
              X∞                                                                        
                   d                                   200q(iy)            1 + q 2 (iy)      7
        q(iy)         (log fn (q)) (iy) ≥ q(iy)               2 (iy))2
                                                                       −        2 (iy))2
                                                                                           ≥    .
              n=1
                  dq                                109(1 − q            (1 − q              10
We conclude that                                                   
                                                 dλ   1          7       3
                                             q      ≥         1−      =    .                                        
                                                 dq   2          10     20
4.5. A non-Weierstrass point with bounded height. The logarithmic height of a non-zero
rational number a = p/q is given by

                                             hnaive (a) = log max(|p|, |q|),

where p and q are coprime integers and q > 0.

                              1
Theorem 4.5.1. Let πQ : Y −→ PQ be a finite morphism of degree d, where Y /Q is a smooth
                                                                          1
projective connected curve of positive genus g ≥ 1. Assume that πQ : Y → PQ is unramified over
 1
PQ − {0, 1, ∞}. Then, for any rational number 0 < a ≤ 2/3 and any b ∈ Y (Q) lying over a,

                                                                                      d5
                                         h(b) ≤ 3hnaive (a)d2 + 6378031                  .
                                                                                      g
28                    ARIYAN JAVANPEYKAR WITH AN APPENDIX BY PETER BRUIN


Proof. By Theorem 4.3.2, there exist a number field K and a model

                                               πK : Y −→ P1K
               1
for πQ : Y −→ PQ with the following three properties: the minimal resolution of singularities
ψ : Y ′ −→ Y of the normalization π : Y −→ P1OK of P1OK in Y is semi-stable over OK , each
irreducible component of the vertical part of the branch locus of π : Y → P1OK is of characteristic
less or equal to deg π and every point in the fibre of πK over a is K-rational. Also, the morphism
π : Y → P1OK is finite flat surjective.
     Let b ∈ Y (K) lie over a. Let P ′ be the closure of b in Y ′ . By Lemma 2.3.1, the height of b is
“minimal” on the minimal regular model. That is,
                                                   (P ′ , ωY ′ /OK )
                                          h(b) ≤                     .
                                                      [K : Q]
Recall the following notation from Section 4.2. Let X = P1OK . Let KX = −2 · [∞] be the
divisor defined by the tautological section. Let KY ′ be the divisor on Y ′ defined by d(πK ) viewed
as a rational section of ωY ′ /OK . Since the support of KY ′ on the generic fibre is contained in
 −1
πK  ({0, 1, ∞}), the section P ′ is not contained in the support of KY ′ . Therefore, we get that
                                                                  X
             h(b)[K : Q] ≤ (P ′ , ωY ′ /OK ) = (P ′ , KY ′ )fin +   (− log kdπK kσ )(σ(b)).
                                                                 σ:K−→C
     Let D be the branch locus of π : Y −→ X endowed with the reduced closed subscheme structure.
Write D = 0 + 1 + ∞ + Dver , where Dver is the vertical part of D. Note that, in the notation of
Section 4.2, we have that D1 = 0 + 1 + ∞. Thus, if Q denotes the closure of a in X , by Proposition
4.2.4, we get

                (P ′ , KY ′ )fin ≤ (deg π)(0 + 1 + ∞, Q)fin + 2(deg π)2 log(deg π)[K : Q].

Write a = p/q, where p and q are coprime positive integers with q > p. Note that

                             (0 + 1 + ∞, Q)fin     = [K : Q] log(pq(q − p))
                                                   ≤ 3 log(q)[K : Q]

                                                   = 3hnaive (a)[K : Q].

We conclude that
                           (P ′ , KY ′ )fin
                                            ≤ 3hnaive (a)(deg π)2 + 2(deg π)3 .
                             [K : Q]
                           P
     It remains to estimate σ:K−→C (− log kdπK kσ )(σ(b)). We will use our bounds for Arakelov-
Green functions.
     Let σ : K → C be an embedding. The composition
                                          πσ
                                                 / P1 (C)       λ−1      / X(2)
                               Yσ

is a Belyi cover (Definition 3.2.1). By abuse of notation, let π denote the composed morphism
Yσ −→ X(2). Note that λ−1 (2/3) ≈ 0.85i. In particular, ℑ(λ−1 (a)) ≥ ℑ(λ−1 (2/3)) > s1 . (Recall
         p
that s1 = 1/2.) Therefore, the element λ−1 (a) lies in Ḃ∞
                                                         s1
                                                            . Since Vyr1 ⊃ Vy ∩ π −1 B∞
                                                                                      s1
                                                                                         , there is a
unique cusp y of Yσ → X(2) lying over ∞ such that σ(b) lies in Vyr1 .
                  POLYNOMIAL BOUNDS FOR ARAKELOV INVARIANTS OF BELYI CURVES                                       29

                                                              P∞             j
   Note that q = z∞ exp(−π/2). Therefore, since λ =              j=1 aj q        on H,
                             ∞
                             X                                   ∞
                                                                 X
                     λ◦π =         aj exp(−jπ/2)(z∞ ◦ π)j =            aj exp(−jπ/2)wyey j
                             j=1                                 j=1

on Vy . Thus, by the chain rule,
                                             ∞
                                             X
                             d(λ ◦ π) = ey         jaj exp(−jπ/2)wyey j−1 d(wy ).
                                             j=1

By the trivial inequality ey ≥ 1, the inequality |wy | ≤ 1 and Lemma 4.4.1,
                                                                         ∞
                                                                         X
   − log kd(λ ◦ π)kAr (σ(b))    = − log kdwy kAr (σ(b)) − log |ey                jaj exp(−jπ/2)wyey j−1 (σ(b))|
                                                                         j=1
                                                                       ∞
                                                                       X
                                ≤ − log kdwy kAr (σ(b)) − log |              jaj exp(−jπ/2)wyey j (σ(b))|
                                                                       j=1
                                ≤ − log kdwy kAr (σ(b)) + 2.

Thus, by Theorem 3.4.5, we conclude that
                   P
                      σ:K→C (− log kdπK kσ )(σ(b))           (deg π)5
                                                   ≤ 6378027          + 2.                                        
                               [K : Q]                          g

Theorem 4.5.2. Let Y be a smooth projective connected curve over Q of genus g ≥ 1. For any
                         1
finite morphism π : Y → PQ ramified over exactly three points, there exists a non-Weierstrass
point b on Y such that
                                                            (deg π)5
                                         h(b) ≤ 6378033              .
                                                               g

Proof. Define the sequence (an )∞
                                n=1 of rational numbers by a1 = 1/2 and an = n/(2n − 1) for

n ≥ 2. Note that 1/2 ≤ an ≤ 2/3, and that hnaive (an ) ≤ log(2n). We may and do assume that
π : Y → P1Q is unramified over P1Q − {0, 1, ∞}. By Theorem 4.5.1, for all x ∈ π −1 ({an }),

                                                                    (deg π)5
(9)                        h(x) ≤ 3 log(2n)(deg π)2 + 6378031                .
                                                                       g
Since the number of Weierstrass points on Y is at most g 3 − g, there exists an integer 1 ≤ i ≤
(deg π)2 such that the fibre π −1 (ai ) contains a non-Weierstrass point, say b. Applying (9) to b,
we conclude that
                                                   (deg π)5    (deg π)5           (deg π)5
          h(b) ≤ 3 log 2(deg π)2 (deg π)2 + 6378031          ≤2          + 6378031          .                     
                                                       g           g                  g

4.6. For a smooth projective connected curve X over Q, we let degB (X) denote the Belyi degree
of X.


Proof of Theorem 1.1.1. The inequality ∆(X) ≥ 0 is trivial, the lower bound e(X) ≥ 0 is due to
Faltings ( [17, Theorem 5]) and the lower bound hFal (X) ≥ −g log(2π) is due to Bost (Lemma
2.4.4).
30                   ARIYAN JAVANPEYKAR WITH AN APPENDIX BY PETER BRUIN


     For the remaining bounds, we proceed as follows. By Theorem 4.5.2, there exists a non-
Weierstrass point b in X(Q) such that
                                                       degB (X)5
                                      h(b) ≤ 6378033             .
                                                           g
By our bound on the Arakelov norm of the Wronskian differential in Proposition 3.5.1, we have

                                 log kWrkAr (b) ≤ 6378028g degB (X)5 .

To obtain the theorem, we combine these bounds with Theorem 2.4.1.                                


                        5. Computing coefficients of modular forms

     Let Γ ⊂ SL2 (Z) be a congruence subgroup, and let k be a positive integer. A modular form
f of weight k for the group Γ is determined by k and its q-expansion coefficients am (f ) for
0 ≤ m ≤ k · [SL2 (Z) : {±1}Γ]/12. In this section we follow [7] and give an algorithmic application
of the main result of this paper. More precisely, the goal of this section is to complete the proof
of the following theorem. The proof is given at the end of this section.

Theorem 5.0.1. (Couveignes-Edixhoven-Bruin) Assume the Riemann hypothesis for ζ-functions
of number fields. Then there exists a probabilistic algorithm that, given

       • a positive integer k,
       • a number field K,
       • a congruence subgroup Γ ⊂ SL2 (Z),
       • a modular form f of weight k for Γ over K, and
       • a positive integer m in factored form,

computes am (f ), and whose expected running time is bounded by a polynomial in the length of the
input.

Remark 5.0.2. We should make precise how the number field K, the congruence subgroup Γ
and the modular form f should be given to the algorithm, and how the algorithm returns the
coefficient am (f ). We should also explain what “probabilistic” means in this context. For the sake
of brevity, we refer the reader to [7, p. 20] for the precise definitions. Following the definitions
there, the above theorem becomes a precise statement.

Remark 5.0.3. The algorithm in Theorem 5.0.1 is due to Bruin, Couveignes and Edixhoven.
Assuming the Riemann hypothesis for ζ-functions of number fields, it was shown that the algorithm
runs in polynomial time for certain congruence subgroups; see [7, Theorem 1.1]. Bruin did not
have enough information about the semi-stable bad reduction of the modular curve X1 (n) at primes
p such that p2 divides n to show that the algorithm runs in polynomial time. Nevertheless, our
bounds on the discriminant of a curve can be used to show that the algorithm runs in polynomial
time for all congruence subgroups.
                   POLYNOMIAL BOUNDS FOR ARAKELOV INVARIANTS OF BELYI CURVES                                    31


Proof of Theorem 5.0.1. We follow Bruin’s strategy [6, Chapter V.1, p. 165]. In fact, Bruin
notes that, to assure that the algorithm runs in polynomial time for all congruence subgroups, it
suffices to show that, for all positive integers n, the discriminant ∆(X1 (n)) is polynomial in n (or
equivalently the genus of X1 (n)). The latter follows from Corollary 1.5.1. In fact, the Belyi degree
of X1 (n) is at most the index of Γ1 (n) in SL2 (Z). Since
                                                    Y
                             [SL2 (Z) : Γ1 (n)] = n2 (1 − 1/p2 ) ≤ n2 ,