Primary https://arxiv.org/pdf/1403.6404, retained PDF/source hash in research/audits/sources/classical_surface_2026/javanpeykar-source.json.

Physical lines700-744
  Instead, we use a theorem of Merkl to prove explicit bounds for the Arakelov-Green function
on a Belyi cover in Theorem 3.4.5. More precisely, we construct a “Merkl atlas” for an arbitrary
Belyi cover. Our construction uses an explicit version of a result of Jorgenson and Kramer ( [23])
on the Arakelov (1, 1)-form due to Bruin.
14                     ARIYAN JAVANPEYKAR WITH AN APPENDIX BY PETER BRUIN


     We use our results to estimate the Arakelov norm of the Wronskian differential in Proposition
3.5.1.
     Merkl’s theorem ( [33, Theorem 10.1]) was used to prove bounds for Arakelov-Green functions
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

Physical lines1538-1630
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

Physical lines1738-1816
                             [SL2 (Z) : Γ1 (n)] = n2 (1 − 1/p2 ) ≤ n2 ,
                                                                 p|n
                                              8 14
we conclude that ∆(X1 (n)) ≤ 5 · 10 n .                                                                         

                             6. Bounds for heights of covers of curves

  Let X be a smooth projective connected curve over Q. We prove that Arakelov invariants of
(possibly ramified) covers of X are polynomial in the degree. Let us be more precise.

Theorem 6.0.4. Let X be a smooth projective connected curve over Q, let U be a non-empty
open subscheme of X, let Bf ⊂ P1 (Q) be a finite set, and let f : X → PQ
                                                                       1
                                                                         be a finite morphism
                 1
unramified over PQ − Bf . Define B := f (X − U ) ∪ Bf . Let N be the number of elements in the
orbit of B under the action of Gal(Q/Q) and let HB be the height of B as defined in Section 1.3.
Define
                                                                       3 N −2
                                          cB := (4N HB )45N 2                   N!
                                                                                     .
Then, for any finite morphism π : Y → X étale over U , where Y is a smooth projective connected
curve over Q of genus g ≥ 1,
                      − log(2π)g                ≤    hFal (Y )     ≤        13 · 106 gcB (deg f )5 (deg π)5
                           0                    ≤     e(Y )        ≤     3 · 107 (g − 1)cB (deg f )5 (deg π)5
                           0                    ≤     ∆(Y )        ≤        5 · 108 g 2 cB (deg f )5 (deg π)5
             −108 g 2 cB (deg f )5 (deg π)5     ≤    δFal (Y )     ≤         2 · 108 gcB (deg f )5 (deg π)5 .

Proof. We apply Khadjavi’s effective version of Belyi’s theorem. More precisely, by [26, Theorem
                                            1    1              1
1.1.c], there exists a finite morphism R : PQ → PQ étale over PQ − {0, 1, ∞} such that R(B) ⊂
{0, 1, ∞} and
                                                                       3 N −2
                                          deg R ≤ (4N HB )9N 2                  N!
                                                                                         .
Note that the composed morphism
                                                     π                    f                  R
                              R◦f ◦π :Y                          /X             / P1             / P1
                                                                                     Q             Q

is unramified over P1Q − {0, 1, ∞}. We conclude by applying Theorem 1.1.1 to the composition
R ◦ f ◦ π.                                                                                                      

                                                           1
  Note that Theorem 6.0.4 implies Theorem 1.3.1 (with X = PQ , Bf the empty set and f : X →
 1
PQ the identity morphism.)
  In the proof of Theorem 6.0.4, we used Khadjavi’s effective version of Belyi’s theorem. Khad-
javi’s bounds are not optimal; see [28, Lemme 4.1] and [26, Theorem 1.1.b] for better bounds
when B is contained in P1 (Q). Actually, the use of Belyi’s theorem makes the dependence on the
32                          ARIYAN JAVANPEYKAR WITH AN APPENDIX BY PETER BRUIN


branch locus enormous in Theorem 6.0.4. It should be possible to avoid the use of Belyi’s theorem
and improve the dependence on the branch locus in Theorem 6.0.4. This is not necessary for our
present purposes.

Remark 6.0.5. Let us mention the quantitative Riemann existence theorem due to Bilu and
Strambi; see [4]. Bilu and Strambi give explicit bounds for the naive logarithmic height of a cover
    1
of PQ with fixed branch locus. Although their bound on the naive height is exponential in the
degree, the dependence on the height of the branch locus in their result is logarithmic.

     Let us show that Theorem 1.3.1 implies the following:

Theorem 6.0.6. ( [15, Conjecture 5.1]) Let U ⊂ P1Z be a non-empty open subscheme. Then
there are integers a and b with the following property. For any prime number ℓ, and for any
connected finite étale cover π : V → UZ[1/ℓ] , the Faltings height of the normalization of P1Q in the
function field of V is bounded by (deg π)a ℓb .

Proof. We claim that this conjecture holds with b = 0 and an integer a depending only on the
generic fibre UQ of U . In fact, let π : Y → P1Q denote the normalization of P1Q in the function
field of V . Note that π is étale over UQ . Let B = P1Q − UQ ⊂ P1 (Q) and let N be the number of
elements in the orbit of B under the action of Gal(Q/Q). By Theorem 1.3.1,
                                           X
                              hFal (Y ) :=     hFal (X) ≤ (deg π)a ,
                                                  X⊂YQ

where the sum runs over all connected components X of YQ := Y ×Q Q, and

Physical lines1837-1905
                    Appendix: Merkl’s method of bounding Green functions

by Peter Bruin

The goal of this appendix is to prove Theorem 3.1.2. Let X be a compact connected Riemann
                                                                      R
surface, and let µ be a smooth non-negative (1, 1)-form on X such that X µ = 1. Let ∗ denote
the star operator on 1-forms on X, given with respect to a holomorphic coordinate z = x + iy by

                                            ∗dx = dy,       ∗dy = −dx,
                  POLYNOMIAL BOUNDS FOR ARAKELOV INVARIANTS OF BELYI CURVES                         33


or equivalently
                                      ∗dz = −i dz̄,     ∗dz̄ = i dz.

The Green function for µ is the unique smooth function

                                          grµ : X × X \ ∆ → R,

with a logarithmic singularity along the diagonal ∆, such that for fixed w ∈ X we have, in a
distributional sense,
                                                              Z
                1
                  d ∗ d grµ (z, w) = δw (z) − µ(z) and                      grµ (z, w)µ(z) = 0.
               2π                                                 z∈X\{w}

   For all a, b ∈ X, we write ga,b for the unique smooth function on X \ {a, b} satisfying
                                                      Z
(10)                       d ∗ dga,b = δa − δb and            ga,b µ = 0.
                                                            X\{a,b}

Then for all a ∈ X, we consider the function ga,µ on X \ {a} defined by
                                            Z
(11)                             ga,µ (x) =         ga,b (x)µ(b).
                                                  b∈X\{x}

A straightforward computation using Fubini’s theorem shows that this function satisfies
                                                   Z
                         d ∗ dga,µ = δa − µ and          ga,µ µ = 0.
                                                              X\{a}

This implies that 2πga,µ (b) = grµ (a, b), where grµ is the Green function for µ defined above.
   We begin by restricting our attention to one of the charts of our atlas, say (U, z). By assumption,
z is an isomorphism from U to the open unit disc in C. Let r2 and r4 be real numbers with

                                             r1 < r2 < r4 < 1,

and write
                                             r3 = (r2 + r4 )/2.

We choose a smooth function
                                              χ̃ : R≥0 → [0, 1]

such that χ̃(r) = 1 for r ≤ r2 and χ̃(r) = 0 for r ≥ r4 . We also define a smooth function χ on X
by putting
                                     χ(x) = χ̃(|z(x)|)      for x ∈ U

and extending by 0 outside U . Furthermore, we put

                                                χc = 1 − χ.

   For 0 < r < 1, we write
                                     U r = {x ∈ U : |z(x)| < r}.

For all a, b ∈ U r1 , the function
                                           1     (z − z(a))(z(a)z − r42 )
                                 fa,b =      log
                                          2π     (z − z(b))(z(b)z − r42 )
