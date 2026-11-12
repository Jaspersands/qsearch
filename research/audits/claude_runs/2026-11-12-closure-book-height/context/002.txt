Source https://arxiv.org/pdf/1403.6404
Local source SHA256 59357cc190f89098d32e4dd1d1c1c7802e25b26aeeea3a8766cafea8089086bc
Physical text line ranges below. Source assumptions must be retained.


Lines 100-115

1.3. Arakelov invariants of covers of curves with fixed branch locus. We apply Theorem
1.1.1 to prove explicit bounds for the height of a cover of curves. Let us be more precise.
   For any finite subset B ⊂ P1 (Q) and integer d ≥ 1, the set of smooth projective connected
curves X over Q such that there exists a finite morphism X → P1Q étale over P1Q − B of degree d
is finite. In particular, the Faltings height of X is bounded by a real number depending only on
B and d. In this section we give an explicit version of this statement. To state our result we need
to define the height of B.
  For any finite set B ⊂ P1 (Q), define the (exponential) height as HB = max{H(α) : α ∈ B},
                                                                  Q               1/[K:Q]
where the height H(α) of an element α in Q is defined as H(α) = ( v max(1, kαkv ))        . Here
K is a number field containing α and the product runs over the set of normalized valuations v of
K. (As in [26, Section 2] we require our normalization to be such that the product formula holds.)

Theorem 1.3.1. Let U be a non-empty open subscheme in P1Q with complement B ⊂ P1 (Q). Let
N be the number of elements in the orbit of B under the action of Gal(Q/Q). Then, for any finite

Lines 450-690
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
     This theorem is essential to the proof of Theorem 1.1.1 given in Section 4.5. We give a proof
of Theorem 2.4.1 at the end of this section.

Lemma 2.4.2. For a smooth projective connected curve X over Q of genus g ≥ 1,
                               g
              log kϑkmax(X) ≤ log max(1, hFal (X)) + (4g 3 + 5g + 1) log 2.
                               4
Proof. We kindly thank R. de Jong for sharing this proof with us. We follow the idea of [19, Section
2.3.2], see also [10, Appendice]. Let Fg be the Siegel fundamental domain of dimension g in the
Siegel upper half-space Hg , i.e., the space of complex (g × g)-matrices τ in Hg such that the
following properties are satisfied. Firstly, for every element uij of u = ℜ(τ ), we have |uij | ≤ 1/2.
Secondly, for every γ in Sp(2g, Z), we have det ℑ(γ · τ ) ≤ det ℑ(τ ), and finally, ℑ(τ ) is Minkowski-
reduced, i.e., for all ξ = (ξ1 , . . . , ξg ) ∈ Zg and for all i such that ξi , . . . , ξg are non-zero, we have
ξℑ(τ )t ξ ≥ (ℑ(τ ))ii and, for all 1 ≤ i ≤ g − 1 we have (ℑ(τ ))i,i+1 ≥ 0. One can show that Fg
contains a representative of each Sp(2g, Z)-orbit in Hg .
   Let K be a number field such that X has a model XK over K. For every embedding σ : K → C,
let τσ be an element of Fg such that Jac(XK,σ ) ∼
                                                = Cg /(τσ Zg + Zg ) as principally polarized abelian
                 POLYNOMIAL BOUNDS FOR ARAKELOV INVARIANTS OF BELYI CURVES                              11


varieties, the matrix of the Riemann form induced by the polarization of Jac(XK,σ ) being ℑ(τσ )−1
on the canonical basis of Cg . By a result of Bost (see [19, Lemme 2.12] or [37]), we have
              1     X
(5)                       log det(ℑ(τσ )) ≤ g log max(1, hFal (X)) + (2g 3 + 2) log(2).
           [K : Q]
                     σ:K→C
Here we used that the Faltings height of X equals the Faltings height of its Jacobian. Now, let
ϑ(z; τ ) be the Riemann theta function as in Section 2.1, where τ is in Fg and z = x + iy is in Cg
with x, y ∈ Rg . Combining (5) with the upper bound
                                                                               3
(6)                          exp(−π t y(ℑ(τ ))−1 y)|ϑ(z; τ )|        ≤ 23g +5g

implies the result. Let us prove (6). Note that, if we write y = ℑ(z) = (ℑ(τ )) · b for b in Rg ,
                                                   X
                exp(−π t g(ℑ(τ ))−1 y)|ϑ(z; τ )| ≤   exp(−π t (n + b)(ℑ(τ ))(n + b)).
                                                     n∈Zg
                                                             Pg
Since ℑ(τ ) is Minkowski reduced, we have mℑ(τ )m ≥ c(g) i=1 m2i (ℑ(τ ))ii for all m in Rg . Here
                                             t
        g−1                                  √
                  3 g(g−1)/2
c(g) = g43        4          . Also, (ℑ(τ ))ii ≥ 3/2 for all i = 1, . . . , g (see [21, Chapter V.4] for
these facts). We deduce that
                                                                  g
                                                                                                    !
  X                                              X                X
                t                                                                      2
          exp(−π (n + b)(ℑ(τ ))(n + b)) ≤             exp −             πc(g)(ni + bi ) (ℑ(τ ))ii
  n∈Zg                                           n∈Zg             i=1
                                                 Yg X
                                         ≤                   exp(−πc(g)(ni + bi )2 (ℑ(τ ))ii )
                                                 i=1 ni ∈Z
                                                 Yg                                           g
                                                               2                          2
                                         ≤                                     ≤ 2g 1 + √         .
                                                 i=1
                                                     1 − exp(−πc(g)(ℑ(τ ))ii )         π 3c(g)
This proves (6).                                                                                        

Lemma 2.4.3. Let a ∈ R>0 and b ∈ R≤1 . Then, for all real numbers x ≥ b,
                         1     1                          1        1
    x − a log max(1, x) = x + (x − 2a log max(1, x)) ≥ x + min( b, a − a log(2a)).
                         2     2                          2        2
Proof. It suffices to prove that x − 2a log max(1, x) ≥ min(b, 2a − 2a log(2a)) for all x ≥ b. To
prove this, let x ≥ b. Then, if 2a ≤ 1, we have x − 2a log max(1, x) ≥ b ≥ min(b, 2a − 2a log(2a)).
(To prove that x − 2a log max(1, x) ≥ b, we may assume that x ≥ 1. It is easy to show that
x − 2a log x is a non-decreasing function for x ≥ 1. Therefore, for all x ≥ 1, we conclude that
x − 2a log x ≥ 1 ≥ b.) If 2a > 1, the function x − 2a log(x) attains its minimum value at x = 2a
on the interval [1, ∞).                                                                                 

Lemma 2.4.4. (Bost) Let X be a smooth projective connected curve over Q of genus g ≥ 1.
Then
                                        hFal (X) ≥ − log(2π)g.

Proof. See [18, Corollaire 8.4]. (Note that the Faltings height h(X) utilized by Bost, Gaudron
and Rémond is bigger than hFal (X) due to a difference in normalization. In fact, we have h(X) =
                 √                                                                          √
hFal (X) + g log( π). In particular, the slightly stronger lower bound hFal (X) ≥ − log( 2π)g
holds.)                                                                                                 
12                   ARIYAN JAVANPEYKAR WITH AN APPENDIX BY PETER BRUIN


Lemma 2.4.5. Let X be a smooth projective connected curve over Q of genus g ≥ 1. Then
                       1                                       g        g g      g 
  log S(X) + hFal (X) ≥ hFal (X) − (4g 3 + 5g + 1) log 2 + min − log(2π), − log         .
                       2                                        2        4 4       2
Proof. By the explicit formula (2) for S(X) in Section 2.1 and our bounds on theta functions
(Lemma 2.4.2),
                                  g
         log S(X) + hFal (X) ≥ − log max(1, hFal (X)) − (4g 3 + 5g + 1) log 2 + hFal (X).
                                  4
Since hFal (X) ≥ −g log(2π), the statement follows from Lemma 2.4.3 (with x = hFal (X), a = g/4
and b = −g log(2π)).                                                                             

Lemma 2.4.6. Let X be a smooth projective connected curve of genus g ≥ 2 over Q. Then
                       (2g − 1)(g + 1)       1
                                       e(X) + δFal (X) ≥ log S(X) + hFal (X).
                           8(g − 1)          8
Proof. By [11, Proposition 5.6],
                                        8(g − 1)
                          e(X) ≥                     (log R(X) + hFal (X)) .
                                     (g + 1)(2g − 1)
Note that log R(X) = log S(X)− δFal (X)/8; see (3) in Section 2.1. This implies the inequality. 

Lemma 2.4.7. (Noether formula) Let X be a smooth projective connected curve over Q of
genus g ≥ 1. Then
                         12hFal(X) = e(X) + ∆(X) + δFal (X) − 4g log(2π).

Proof. This is well-known; see [17, Theorem 6] and [35, Théorème 2.2].                         

Proposition 2.4.8. Let X be a smooth projective connected curve of genus g ≥ 2 over Q. Then
                                         (2g−1)(g+1)
                         hFal (X)   ≤       4(g−1)   e(X) + 41 δFal (X) + 20g 3
                                         (2g−1)(g+1)
                       −g log(2π) ≤         4(g−1)   e(X) + 41 δFal (X) + 20g 3
                                        3(2g−1)(g+1)
                          ∆(X)      ≤       g−1      e(X) + 2δFal (X) + 248g 3.

Proof. Firstly, by Lemma 2.4.6,
                       (2g − 1)(g + 1)       1
                                       e(X) + δFal (X) ≥ log S(X) + hFal (X).
                           8(g − 1)          8
To obtain the upper bound for hFal (X), we proceed as follows. By Lemma 2.4.5,
                          1                                     g          g g       g 
   log S(X) + hFal (X) ≥ hFal (X) − (4g 3 + 5g + 1) log 2 + min − log(2π), − log            .
                          2                                       2         4 4        2
From these two inequalities, we deduce that
1            (2g − 1)(g + 1)      1                                 g         g    g g
  hFal (X) ≤                 e(X)+ δFal (X)+(4g 3 +5g+1) log 2+max     log(2π), log       −    .
2                8(g − 1)         8                                  2         4      2      4
Finally, it is straightforward to verify the inequality
                                                g         g    g  g 
                    (4g 3 + 5g + 1) log 2 + max    log(2π), log     −    ≤ 10g 3 .
                                                 2         4     2    4
This concludes the proof of the upper bound for hFal (X).
     The second inequality follows from the first inequality of the proposition and the lower bound
hFal (X) ≥ −g log(2π) of Bost (Lemma 2.4.4).
                POLYNOMIAL BOUNDS FOR ARAKELOV INVARIANTS OF BELYI CURVES                         13


  Finally, to obtain the upper bound of the proposition for the discriminant of X, we eliminate
the Faltings height of X in the first inequality using the Noether formula and obtain
                                                 3(2g − 1)(g + 1)
        ∆(X) + e(X) + δFal (X) − 4g log(2π) ≤                     e(X) + 3δFal (X) + 240g 3 .
                                                      (g − 1)
In [17, Theorem 5] Faltings showed that e(X) ≥ 0. Therefore, we conclude that
                                             3(2g − 1)(g + 1)
            ∆(X) + δFal (X) − 4g log(2π) ≤                    e(X) + 3δFal (X) + 240g 3 .         
                                                  (g − 1)
  We are now ready to prove Theorem 2.4.1.


Proof of Theorem 2.4.1. The proof is straightforward. The upper bound e(X) ≤ 4g(g − 1)h(b) is
well-known; see [17, Theorem 5].
  Let us prove the lower bound for δFal (X). If g ≥ 2, the lower bound for δFal (X) can be deduced
from the second inequality of Proposition 2.4.8 and the upper bound e(X) ≤ 4g(g − 1)h(b). When
g = 1, this follows from a result of Szpiro ( [12, Proposition 7.2]) and the non-negativity of h(b).
  From now on, we suppose that b is a non-Weierstrass point. The upper bound hFal (X) ≤
1
2 g(g + 1)h(b) + log kWrkAr (b) follows from Theorem 5.9 in [11] and (4) in Section 2.1.
  We deduce the upper bound δFal (X) ≤ 6g(g + 1)h(b) + 12 log kWrkAr (b) + 4g log(2π) as follows.
Since e(X) ≥ 0 and ∆(X) ≥ 0, the Noether formula implies that

                                 δFal (X) ≤ 12hFal(X) + 4g log(2π).

Thus, the upper bound for δFal (X) follows from the upper bound for hFal (X).
  The upper bound

                     ∆(X) ≤ 2g(g + 1)(4g + 1)h(b) + 12 log kWrkAr (b) + 93g 3

follows from the inequality

                              ∆(X) ≤ 12hFal(X) − δFal (X) + 4g log(2π)

and the preceding bounds. (One could also use the last inequality of Proposition 2.4.8 to obtain

Lines 710-767
of the modular curve X1 (5p) in [13]. It is also used by David Holmes [20] to construct “weak-
pseudo-metrics” on hyperelliptic curves.

3.1. Merkl’s theorem. Let X be a compact connected Riemann surface of positive genus and
recall that µ denotes the Arakelov (1, 1)-form on X.

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
defined as
                           a b
                 Γ(2) =      c d   ∈ SL2 (Z) : a ≡ d ≡ 1      mod 2 and b ≡ c ≡ 0     mod 2 .

The Riemann surface Y (2) = Γ(2)\H is not compact. Let X(2) be the compactification of the
Riemann surface Y (2) = Γ(2)\H obtained by adding the cusps 0, 1 and ∞. Note that X(2) is
known as the compact modular curve associated to the congruence subgroup Γ(2) of SL2 (Z). The
modular lambda function λ : H → C induces an analytic isomorphism λ : X(2) → P1 (C); see
Section 4.4 for details. In particular, the genus of X(2) is zero. For a cusp κ ∈ {0, 1, ∞}, we fix
an element γκ in SL2 (Z) such that γκ (κ) = ∞.
                POLYNOMIAL BOUNDS FOR ARAKELOV INVARIANTS OF BELYI CURVES                          15


   We construct an atlas for the compact connected Riemann surface X(2). Let Ḃ∞ be the open
subset given by the image of the strip
                                                            
                                                           1
                           Ṡ∞ := x + iy : −1 ≤ x < 1, y >     ⊂H
                                                           2
in Y (2) under the quotient map H −→ Γ(2)\H defined by τ 7→ Γ(2)τ . The quotient map H −→
Γ(2)\H induces a bijection from this strip to Ḃ∞ . More precisely, suppose that τ and τ ′ in Ṡ∞ lie
in the same orbit under the action of Γ(2). Then, there exists an element
                                                 
                                             a b
                                      γ=            ∈ Γ(2)
                                             c d

Lines 1026-1115
3.5. The Arakelov norm of the Wronskian differential.

Proposition 3.5.1. Let π : Y −→ X(2) be a Belyi cover with Y of genus g ≥ 1. Then

                                   sup      log kWrkAr ≤ 6378028g(deg π)5 .
                                Y −SuppW
20                   ARIYAN JAVANPEYKAR WITH AN APPENDIX BY PETER BRUIN


Proof. Let b be a non-Weierstrass point on Y and let y be a cusp of Y such that b lies in Vyr1 . Let
ω = (ω1 , . . . , ωg ) be an orthonormal basis of H0 (Y, Ω1Y ). Then, as in Section 2.1,

                                                                                g(g + 1)
                    log kWrkAr (b) = log |Wwy (ω)(b)| +                                  log kdwy kAr (b).
                                                                                    2

By Theorem 3.4.5,

                             g(g + 1)
                                      log kdwy kAr (b) ≤                        6378027g(deg π)5 .
                                 2

Let us show that log |Wwy (ω)(b)| ≤ g(deg π)5 . Write ωk = fk dwy on Vy . Note that ωk ∧ ωk =
|fk |2 dwy ∧ dwy . Therefore,
                                              g                             g
                                        i X            i X
                                µ=          ωk ∧ ωk =      |fk |2 dwy ∧ dwy .
                                       2g             2g
                                          k=1                           k=1
                 Pg             2
We deduce that      k=1 |fk |       = 2gFy , where Fy is the unique function on Vy such that µ = iFy dwy ∧
dwy . By our upper bound for Fy (Proposition 3.4.3), for any j = 1, . . . , g,
                                                  g
                                                  X                              256 exp(3π)(deg π)4
                        sup |fj |2 ≤ sup                |fk |2 = 2gFy ≤                              .
                        Vy               Vy                                              π2
                                                  k=1

By Hadamard’s inequality,

                                                           g−1           g       2
                                                                                              !1/2
                                                           X             X dl fk
                             log |Wwy (ω)(b)| ≤                  log                      (b)        .
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

Lines 1118-1432


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

Lines 1540-1698
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