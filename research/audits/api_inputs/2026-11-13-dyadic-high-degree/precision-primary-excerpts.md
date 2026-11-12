# Checked primary precision source

https://xavier.caruso.ovh/papers/publis/padicprec.pdf

Physical text lines 315-366:


  We emphasize that we require an equality in (3.1), and not just an inclusion! With this
definition in hand, we are able to state our main lemma.


   Lemma 3.4. Let E and F be two K-Banach spaces and f : U → F be a function defined
on an open subset U of E. We assume that f is differentiable at some point v0 ∈ U and that
the differential f 0 (v0 ) is surjective.
   Then, for all ρ ∈ (0, 1], there exists a positive real number δ such that, for all r ∈ (0, δ), any
                           −
lattice H such that BE       (ρr) ⊂ H ⊂ BE (r) is a first order lattice for f at v0 .


    Proof. Without loss of generality, v0 = 0 and f (0) = 0. Since f 0 (0) is surjective, the open
mapping theorem provides a C > 0 such that BF (1) ⊂ f 0 (0)(BE (C)). Let ε > 0 be such that
εC < ρ, and choose Uε ⊂ E as in Definition 3.1. We may assume Uε = BE (δ) for some δ > 0.
                                                             −
    Let r ∈ (0, δ). We suppose that H is a lattice with BE     (ρr) ⊂ H ⊂ BE (r). We seek to show
that f maps H surjectively onto f (0)(H). We first prove that f (H) ⊂ f 0 (0)(H). Suppose
                                       0

x ∈ H. By differentiability at 0, kf (x) − f 0 (0)(x)k ≤ εkxk. Setting y = f (x) − f 0 (0)(x), we have
kyk ≤ εr. The definition of C implies that BF (εr) ⊂ f 0 (0)(BE (εrC)). Thus there exists x0 ∈
                                                                      −
BE (εrC) such that f 0 (0)(x0 ) = y. Since εC < ρ, we get x0 ∈ BE       (ρr) ⊂ H and then f (x) =
  0          0      0
f (0)(x − x ) ∈ f (0)(H).
    We now prove surjectivity. Let y ∈ f 0 (0)(H). Let x0 ∈ H be such that y = f 0 (0)(x0 ). We
inductively define two sequences (xn ) and (zn ) as follows:
    – zn is an element of E satisfying f 0 (0)(zn ) = y − f (xn ) and kzn k ≤ C · ky − f (xn )k (such
      an element exists by definition of C), and
                                   TRACKING p-ADIC PRECISION                          Page 7 of 21


  – xn+1 = xn + zn .
For convenience, let us also define x−1 = 0 and z−1 = x0 . We claim that the sequences (xn )
and (zn ) are well defined and take their values in H. We do so by induction, assuming that
xn−1 and xn belong to H and showing that zn and xn+1 do as well. Noticing that
                        y − f (xn ) = f (xn−1 ) + f 0 (0)(zn−1 ) − f (xn )
                                                                                              (3.2)
                                   = f (xn−1 ) − f (xn ) − f 0 (0)(xn−1 − xn )
we deduce using differentiability that ky − f (xn )k ≤ ε · kxn − xn−1 k. Since we are assuming
that xn−1 and xn lie in H ⊂ BE (r), we find ky − f (xn )k ≤ εr. Thus kzn k ≤ C · εr < ρr and
then zn ∈ H. From the relation xn+1 = xn + zn , we finally deduce xn+1 ∈ H.
  Using (3.2) and differentiability at 0 once more, we get
                        ky − f (xn )k ≤ ε · kzn−1 k ≤ εC · ky − f (xn−1 )k,
for all n > 0. Therefore, ky − f (xn )k = O(an ) and kzn k = O(an ) for a = εC < ρ ≤ 1. These
conditions show that (xn ) is a Cauchy sequence, which converges since E is complete. Write
x for the limit of the xn ; we have x ∈ H because H is closed. Moreover, f is continuous on
H ⊆ Uε since it is differentiable, and thus y = f (x).


Physical text lines 530-585:



  We may now provide two sufficient conditions to effectively recognize first order lattices.

                                 P
  Proposition 3.12. Let f = n≥0 fn be a function as above. Let C be a positive real
number satisfying BF (1) ⊂ f1 (BE (C)). Let ρ ∈ (0, 1] and ν be a real number such that
                                                        ρ
                                 Λ(f )≥2 (ν) < ν + log      .                           (3.6)
                                                         C
Then the conclusion of Lemma 3.4 holds with δ = eν .


   Remark 3.13. On a neighborhood of −∞, the function x 7→ Λ(f )≥2 (x) − x is affine with
slope 1. This implies that, for all ρ ∈ (0, 1], there exists ν satisfying (3.6). Moreover, if ρ is
close enough to 0, then one can take δ = eν as a linear function of ρ.


  Remark 3.14. In the statement of Proposition 3.12, one can of course replace the function
Λ(f ) by any convex function ϕ with ϕ ≥ Λ(f ). If f is given by some formula or some algorithm,
such a function ϕ can be obtained using Remark 3.8.


  Proof. Pick ε in the interval (eΛ(f )≥2 (ν)−ν , Cρ ). Going back to the proof of Lemma 3.4, we
observe that it is enough to prove that

                                       kf≥2 (x)k ≤ ε · kxk.                                   (3.7)

for all x ∈ BE (δ). This inequality follows from Propositions 3.9 and 3.11 applied to the function
      Λ (x)
x 7→ ≥2x .


  Remark 3.15. It follows from the proof that Proposition 3.12 is still valid if K is not
assumed to be algebraically closed. Indeed, the functions fn — and then f also — extend to
an algebraic closure K̄ of K and (3.7) holds over K̄, which is enough to conclude the result.


  Corollary 3.16. We keep the notations of Proposition 3.12 and consider in addition a
sequence (Mn )n≥2 such that kfn k ≤ Mn for all n ≥ 2. Let NP(Mn ) denote the convex function
whose epigraph is the convex hull in R2 of the points of coordinates (n, − log Mn ) for n ≥ 2
together with the extra point (0, +∞).
  Let ρ ∈ (0, 1] and ν be a real number such that
                                                          ρ
                                 N P (Mn )? (ν) < ν + log     .
                                                           C
Then the conclusion of Lemma 3.4 holds with δ = eν .


  Remark 3.17. If K has characteristic 0 and the vector spaces E and F are finite
dimensional, then the Mn ’s defined by
                                        1                ∂ n fi
                                Mn =       · sup                (0)
                                       |n!| 1≤i≤dim E    ∂xn
                                               |n|=n

Physical text lines 987-1016:
thus belongs to fi (H0 ) because each summand does. Therefore fj (H0 ) ⊂ fi (H0 ). The inverse
inclusion is proved in the same way. The fact that H is a precision datum at x is easy and left
to the reader. Finally, if x is close enough to x0 , it is enough to check (ii) in the charts but this
was already done.

A.3. Generalization of the main Lemma
  With above definitions, Lemma 3.4 extends to manifolds. To do so, we first need to define a
norm on the tangent space Tx V (where V is some K-variety and x is a point in V ). There is
actually in general no canonical choice for this. Indeed, let us consider a K-manifold V covered
by charts Ui ’s (i ∈ I) which are open subset of K-Banach spaces Ei ’s. If x is a point in V ,
Page 18 of 21         XAVIER CARUSO, DAVID ROE AND TRISTAN VACCON



the tangent space Tx V is by definition isomorphic to Ei for each index i such that x ∈ Vi . A
natural norm on Tx V is then the one obtained by pulling back the norm on Ei . However, since
the transition maps are not required to be isometries, this norm depends on the choice of i.
They are nevertheless all equivalent because the transition maps are required to be continuous.
  In the next lemma, we choose any of the above norms for Tx V .


   Lemma A.6. Let V and W be two K-manifolds. Suppose that we are given a differentiable
function f : V → W , together with a point x ∈ V such that f 0 (x) : Tx V → Tf (x) W is surjective.
   Then, for all ρ ∈ (0, 1], there exists a positive real number δ such that, for all r ∈ (0, δ), any
lattice H in Tx V such that BT−x V (ρr) ⊂ H ⊂ BTx V (r) is a first order lattice for f at x.


  Proof. Apply Lemma 3.4 in charts.

   Remark A.7. The constant δ that appears in the lemma depends (up to some multiplica-

