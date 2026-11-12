Source: research/audits/sources/classical_surface_2026/javanpeykar.txt; locally saved source.json holds URL/SHA. Line numbers are physical pdftotext lines.

Lines 1-175:
                                                POLYNOMIAL BOUNDS FOR ARAKELOV INVARIANTS OF BELYI
                                                                     CURVES

                                                                                      ARIYAN JAVANPEYKAR

                                                                             WITH AN APPENDIX BY PETER BRUIN


                                                    Abstract. We explicitly bound the Faltings height of a curve over Q polynomially in its Be-




arXiv:1403.6404v1 [math.AG] 25 Mar 2014
                                                    lyi degree. Similar bounds are proven for three other Arakelov invariants: the discriminant,
                                                    Faltings’ delta invariant and the self-intersection of the dualizing sheaf. Our results allow us
                                                    to explicitly bound these Arakelov invariants for modular curves, Hurwitz curves and Fermat
                                                    curves in terms of their genus. Moreover, as an application, we show that the Couveignes-
                                                    Edixhoven-Bruin algorithm to compute coefficients of modular forms for congruence subgroups
                                                    of SL2 (Z) runs in polynomial time under the Riemann hypothesis for ζ-functions of number
                                                    fields. This was known before only for certain congruence subgroups. Finally, we use our results
                                                    to prove a conjecture of Edixhoven, de Jong and Schepers on the Faltings height of a cover of
                                                    P1Z with fixed branch locus.




                                                                       1. Introduction and statement of results

                                             We prove that stable Arakelov invariants of a curve over a number field are polynomial in the
                                          Belyi degree. We apply our results to give algorithmic, geometric and Diophantine applications.

                                          1.1. Bounds for Arakelov invariants of three-point covers. Let Q be an algebraic closure
                                          of the field of rational numbers Q. Let X be a smooth projective connected curve over Q of
                                                                                                             1
                                          genus g. Belyi [3] proved that there exists a finite morphism X → PQ ramified over at most three
                                          points. Let degB (X) denote the Belyi degree of X, i.e., the minimal degree of a finite morphism
                                          X → P1Q unramified over P1Q \{0, 1, ∞}. Since the topological fundamental group of the projective
                                          line P1 (C) minus three points is finitely generated, the set of Q-isomorphism classes of curves with
                                          bounded Belyi degree is finite.
                                             We prove that, if g ≥ 1, the Faltings height hFal (X), the Faltings delta invariant δFal (X),
                                          the discriminant ∆(X) and the self-intersection of the dualizing sheaf e(X) are bounded by a
                                          polynomial in degB (X); the precise definitions of these Arakelov invariants of X are given in
                                          Section 2.3.

                                          Theorem 1.1.1. For any smooth projective connected curve X over Q of genus g ≥ 1,
                                                                 − log(2π)g            ≤ hFal (X)        ≤    13 · 106 g degB (X)5
                                                                        0              ≤  e(X)           ≤ 3 · 107 (g − 1) degB (X)5
                                                                        0              ≤ ∆(X)            ≤    5 · 108 g 2 degB (X)5
                                                               −108 g 2 degB (X)5      ≤ δFal (X)        ≤    2 · 108 g degB (X)5 .

                                             1991 Mathematics Subject Classification. 11G30, 11G32, 11G50, 14G40, 14H55, 37P30.
                                             Key words and phrases. Arakelov theory, Belyi degree, arithmetic surfaces, Riemann surfaces, Arakelov in-
                                          variants, Faltings height, discriminant, Faltings’ delta invariant, self-intersection of the dualizing sheaf, branched
                                          covers.
                                                                                                    1
2                   ARIYAN JAVANPEYKAR WITH AN APPENDIX BY PETER BRUIN


    The Arakelov invariants in Theorem 1.1.1 all have a different flavour to them. For example,
the Faltings height hFal (X) plays a key role in Faltings’ proof of his finiteness theorem on abelian
varieties; see [16]. On the other hand, the strict positivity of e(X) (when g ≥ 2) is related to
the Bogomolov conjecture; see [45]. The discriminant ∆(X) “measures” the bad reduction of the
curve X/Q, and appears in Szpiro’s discriminant conjecture for semi-stable elliptic curves; see [44].
Finally, as was remarked by Faltings in his introduction to [17], Faltings’ delta invariant δFal (X)
can be viewed as the minus logarithm of a “distance” to the boundary of the moduli space of
compact connected Riemann surfaces of genus g.
    We were first led to investigate this problem by work of Edixhoven, de Jong and Schepers
on covers of complex algebraic surfaces with fixed branch locus; see [15]. They conjectured an
arithmetic analogue ( [15, Conjecture 5.1]) of their main theorem (Theorem 1.1 in loc. cit.). We
use our results to prove this conjecture; see Section 6 for a more precise statement.


1.2. Outline of proof. To prove Theorem 1.1.1 we will use Arakelov theory for curves over a
number field K. To apply Arakelov theory in this context, we will work with arithmetic surfaces
associated to such curves, i.e., regular projective models over the ring of integers OK of K. We
refer the reader to Section 2.2 for precise definitions and basic properties of Arakelov’s intersection
pairing on an arithmetic surface. Then, for any smooth projective connected curve X over Q of
genus g ≥ 1, we define the Faltings height hFal (X), the discriminant ∆(X), Faltings’ delta invariant
δFal (X) and the self-intersection of the dualizing sheaf e(X) in Section 2.3. These are the four
Arakelov invariants appearing in Theorem 1.1.1.
    We introduce two functions on X(Q) in Section 2.3: the canonical Arakelov height function
and the Arakelov norm of the Wronskian differential. We show that, to prove Theorem 1.1.1, it
suffices to bound the canonical height of some non-Weierstrass point and the Arakelov norm of
the Wronskian differential at this point; see Theorem 2.4.1 for a precise statement.
    We estimate Arakelov-Green functions and Arakelov norms of Wronskian differentials on finite
étale covers of the modular curve Y (2) in Theorem 3.4.5 and Proposition 3.5.1, respectively. In our
proof we use an explicit version of a result of Merkl on the Arakelov-Green function; see Theorem
3.1.2. This version of Merkl’s theorem was obtained by Peter Bruin in his master’s thesis. The
proof of this version of Merkl’s theorem is reproduced in the appendix by Peter Bruin.
    In Section 4 we prove the existence of a non-Weierstrass point on X of bounded height; see
Theorem 4.5.2. The proof of Theorem 4.5.2 relies on our bounds for Arakelov-Green functions
(Theorem 3.4.5), the existence of a “wild” model (Theorem 4.3.2) and Lenstra’s generalization
of Dedekind’s discriminant conjecture for discrete valuation rings of characteristic 0 (Proposition
4.1.1).
    A precise combination of the above results constitutes the proof of Theorem 1.1.1 given in
Section 4.6.
                POLYNOMIAL BOUNDS FOR ARAKELOV INVARIANTS OF BELYI CURVES                                  3


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
                  1
morphism π : Y → PQ étale over U , where Y is a smooth projective connected curve over Q of
genus g ≥ 1,
                                                                                       3 N −2
             − log(2π)g                   ≤ hFal (Y )    ≤    13 · 106 g(4N HB )45N 2         N!
                                                                                                  (deg π)5
                                                                   7                45N 3 2N −2 N !
                  0                       ≤  e(Y )       ≤ 3 · 10 (g − 1)(4N HB )                   (deg π)5
                                                                                      3 N −2
                  0                       ≤ ∆(Y )        ≤    5 · 108 g 2 (4N HB )45N 2       N!
                                                                                                  (deg π)5
                    3 N −2
                                                                                 45N 3 2N −2 N !
 −108g 2 (4N HB )45N 2     N!
                              (deg π)5    ≤ δFal (Y )    ≤           8
                                                               2 · 10 g(4N HB )                  (deg π)5 .

   Theorem 1.3.1 is a consequence of Theorem 6.0.4. Note that in Theorem 6.0.4 we consider
                                                     1
branched covers of any curve over Q (i.e., not only PQ ). We use Theorem 1.3.1 to prove [15,
Conjecture 5.1].

1.4. Diophantine application. Explicit bounds for Arakelov invariants of curves of genus g ≥ 2
over a number field K and with bad reduction outside a finite set S of finite places of K imply
famous conjectures in Diophantine geometry such as the effective Mordell conjecture and the
effective Shafarevich conjecture; see [38] and [40]. We note that Theorem 1.1.1 shows that one
“could” replace Arakelov invariants by the Belyi degree to prove these conjectures. We use this
philosophy to deal with cyclic covers of prime degree. In fact, in [22], joint with von Känel, we
utilize Theorem 1.1.1 and the theory of logarithmic forms to prove Szpiro’s small points conjecture
( [42, p. 284] and [43]) for curves that are cyclic covers of the projective line of prime degree; see [22,
Theorem 3.1] for a precise statement. In particular, we prove Szpiro’s small points conjecture for
hyperelliptic curves.

1.5. Modular curves, Fermat curves, Hurwitz curves and Galois Belyi curves. Let X
be a smooth projective connected curve over Q of genus g ≥ 2. We say that X is a Fermat curve
if there exists an integer n ≥ 4 such that X is isomorphic to the planar curve {xn + y n = z n }.
Moreover, we say that X is a Hurwitz curve if #Aut(X) = 84(g−1). Also, we say that X is a Galois
                                                       1
Belyi curve if the quotient X/Aut(X) is isomorphic to PQ and the morphism X → X/Aut(X) is
4                   ARIYAN JAVANPEYKAR WITH AN APPENDIX BY PETER BRUIN


ramified over exactly three points; see [8, Proposition 2.4], [47] or [48]. Note that Fermat curves
and Hurwitz curves are Galois Belyi curves. Finally, we say that X is a modular curve if XC is a
classical congruence modular curve with respect to some (hence any) embedding Q → C.
    If X is a Galois Belyi curve, we have degB (X) ≤ 84(g − 1). In [49] Zograf proved that, if X is
a modular curve, then degB (X) ≤ 128(g + 1). Combining these bounds with Theorem 1.1.1 we
obtain the following corollary.

Corollary 1.5.1. Let X be a smooth projective connected curve over Q of genus g ≥ 1. Suppose
that X is a modular curve or Galois Belyi curve. Then

                     max(hFal (X), e(X), ∆(X), |δFal (X)|) ≤ 2 · 1019 g 2 (g + 1)5 .

Remark 1.5.2. Let Γ ⊂ SL2 (Z) be a finite index subgroup, and let X be the compactification of
Γ\H obtained by adding the cusps, where Γ acts on the complex upper half-plane H via Möbius
transformations. Let X(1) denote the compactification of SL2 (Z)\H. The inclusion Γ ⊂ SL2 (Z)
induces a morphism X → X(1). For Q ⊂ C an embedding, there is a unique finite morphism
Y → P1Q of smooth projective connected curves over Q corresponding to X −→ X(1). The Belyi
degree of Y is bounded from above by the index d of Γ in SL2 (Z). In particular,

Lines 1739-1833:
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
                                                          3 N −2
                                                                     
                         a = 6 + log 13 · 106 N (4N HB )45N 2     N!
                                                                       .

Here we used that, g ≤ N deg π and
                                                                                       3 N −2 N !
                                                                                                   
                                        3 N −2                1+log 13·106 N (4N HB )45N 2
                  13 · 106 g(4N HB )45N 2        N!
                                                      ≤ (deg π)                                        .

This concludes the proof.                                                                                  

     Let us briefly mention the context in which these results will hopefully be applied. Let S be a
smooth projective geometrically connected surface over Q. As is explained in Section 5 of [15], it
seems reasonable to suspect that, there exists an algorithm which, on input of a prime ℓ, computes

