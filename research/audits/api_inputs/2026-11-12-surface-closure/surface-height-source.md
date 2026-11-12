Source https://www.cse.iitk.ac.in/users/nitin/papers/Surfaces.pdf
Local source SHA256 504289c9cd964bec432b83fe12337a6b8ec509f26f3bdc334f1e0d8d6e96d9e3
Physical text line ranges below. Source assumptions must be retained.


Lines 1255-1395
 3: Compute the image of the monodromy fixed subspace, i.e., those elements γ ∈ Fη fixed
    by each σj for 1 ≤ j < r, with the monodromy action as computed in Algorithm 7.
 4: Compute the Galois action on the monodromy fixed subspace FuG := ϕ−1            G
                                                                               u (Fη ) element-
    wise, using the cospecialisation ϕu . This gives H1 (X , µℓ ) with Gal(K/K) action.
 5: Now, for the second cohomology work with the curve Ṽ. Choose an auxiliary prime
    of good reduction P of size O(ℓ), distinct from ℓ, and compute the subspace EP ⊂
    Jac(ṼP )[ℓ] using Algorithm 8.
 6: Lift the subspace EP to the characteristic zero subspace E ⊂ Jac(Ṽ)[ℓ] using Theorem 4.4.
 7: Compute the space of invariant tensors
                                          (E ⊗ Fu )G
    with knowledge of the G - action.
 8: Compute the diagonal Gal(K/K) action as a matrix on the subspace of tensors which
    has been isolated in the above step, element-wise. This gives the space H1 (P1 , F) with
    Gal(K/K) - action. To obtain the full H2 (X , µℓ ), we just add the space < γE > ⊕ <
    γF >, on which Galois acts via the cyclotomic character on each component.



                                 6. Complexity analyses
  In this section, we prove the upper bounds for the complexities stated of the subroutines
used in the earlier sections. We do not deduce the exact complexities beyond showing that
                                               26
they are bounded by polynomial functions of ℓ and log q. We also keep track of the heights
of the algebraic numbers involved in the computations.
6.1. Algorithms of Sections 2 and 3. Noting that the complexity of Algorithm 1 is
independent of ℓ, we begin with the following.
Lemma 6.1. Algorithm 2 runs in time poly(ℓ).
Proof. Pila [Pil90, §2] shows that the data representing the multiplication by ℓ map is
bounded by a polynomial in ℓ. Further, the coefficients occurring in the ideal (ℓ) Iη have
height bounded by a polynomial in ℓ due to Theorem B.4 and the fact that the Faltings
height of the (normalisation of the) curve (ℓ) C over K given by (ℓ) Iη is bounded by a poly-
nomial in ℓ [Jav14, Theorem 6.0.6].
                                                                                           □
Lemma 6.2. Algorithm 4 runs in time poly(ℓ).
Proof.
     • Step 1: The complexity of Algorithm 2 has been shown to be polynomial in ℓ.
     • Step 2: Zero-dimensional system solving can be done using a primitive element in
       time polynomial in the degree of the system by [Rou99].
     • Step 3: Computing the first m coefficients of a branch can be done in poly(m) time by
       Theorem 3.4. It suffices to compute the first poly(ℓ) coefficients to uniquely specify
       a branch by Lemma 3.5.
     • Step 4: Once a choice of Puiseux series for τ is made, simple arithmetic (addition,
       squaring) can be performed using it in polynomial time.
                                                                                           □
Lemma 6.3. Algorithm 5 runs in time poly(ℓ).
Proof.
     • Step 1: Specialisation of the ideal (ℓ) Iη to u mearly involves making the substitution
       t = u.
     • Step 2: The specialised ideal (ℓ) Iu is now zero-dimensional over K and its roots can
       be found by a system solver [Rou99]. The Weil height of the ℓ – torsion points is
       bounded by a polynomial in ℓ by Theorem B.4.
     • Step 3: Convergence to an algebraic number with poly(ℓ) precision is guaranteed by
       Theorem 3.12.
                                                                                             □
Lemma 6.4. Algorithm 6 runs in time poly(ℓ).
Proof.
     • Step 1: Follows from the complexity of Algorithm 4.
     • Step 2: An element γ ∈ Fη \ ϕz (Fz ) can be chosen by ensuring that at least one of
       the tuple of Puiseux expansions associated to γ is ramified at z, i.e., is in fact belongs
       to K⟨⟨t − z⟩⟩ \ K((t − z)).
     • Step 3: As each Puiseux expansion is specified only upto the first poly(ℓ) coefficients
       by Lemma 3.5, one has to simply multiply each (non-constant) coefficient by a power
       of ζℓ .
                                               27
     • Steps 4 & 5: The complexity follows from that of Algorithm 5.
     • Step 6: The addition of the group law can be performed efficiently by Theorem D.1.
     • Step 7: The complexity of computing the abstract Abel map and its inverse (Algo-
       rithm 10) is given by Theorem D.1.
     • Step 8: Pairings can be computed in polynomial time using a divisorial description
       by Algorithm 3.
     • Step 9: Square root over Z/ℓZ can be found in randomised polynomial time.
     • Step 10: The rational functions in τ corresponding to Puiseux expansions around z,
       can be found in polynomial time via linear algebra combined with poly(ℓ) truncations.
                                                                                          □
Lemma 6.5. Algorithm 7 runs in time poly(ℓ).
Proof.
     • Step 1: Follows from the complexity of Algorithm 6.
     • Steps 2 and 3 : This boils down to the problem of expressing elements in the splitting
       field of the ℓ – torsion of the Jacobian of the generic fibre, as rational functions in a
       primitive element for the field extension. This can be solved on the level of Puiseux
       series as well, with poly(ℓ) truncation, by Lemma 3.5.
                                                                                              □

6.2. Algorithms of Sections 4 and 5.
Lemma 6.6. Algorithm 8 runs in time poly(ℓ · char(FP ) · log(#FP )).
Proof.
     • Step 1: One can use a P – adic algorithm such as Harvey’s [Har15] to count points
       on ṼP to output its zeta function with the stated complexity. It is sufficient to count
       points upto an extension of degree bounded by the genus g, which in this case is
       bounded by a polynomial in ℓ.
     • Step 2: A basis for the space Si can be computed in polynomial time using random
       sampling on the curve, following [Cou09, Theorem 1].
     • Step 3: The G - action is computed on the points of the curve ṼP following 4.2 in
       polynomial time. The number J is bounded by a polynomial in ℓ by Lemma 4.2.
     • Step 4: Firstly, the dual M ∨ can be identified with M for the G – action via the
       self-duality given by the symplectic Weil pairing. Next, the dimension of the space
       HomG (M ∨ , Si ) is bounded independently of ℓ, and each G – equivariant homomor-
       phism can be computed as a matrix via linear algebra. In other words, there are only
       poly(ℓ) homs, and a basis for the sum of their images can be found using [Cou09].
     • Step 5: One can list all the invariant tensors with knowledge of the G – action.
       Further, zero-testing is efficient and can be done in polynomial time, so it simply
       remains to count the number of invariant tensors in each space, which is always
       bounded by a polynomial in ℓ. Finally the Betti number β2 can be computed as
       #Z + 2β1 + 2 − 4g, where g is the genus of the generic fibre of the pencil.
                                                                                             □
Lemma 6.7. Algorithm 9 runs in time poly(ℓ).
                                               28
Proof.
     • Step 1: This can be done in polynomial time.
     • Step 2: The complexity is the same as that of computing a Puiseux series expansion,
       except we are now working around a smooth point. The poly(ℓ) truncation bounds
       remain, and the total complexity is the same as that of Algorithm 4.
     • Step 3: Follows from the complexity of Algorithm 7.
     • Step 4: The arithmetic Gal(K/K) action on FuG factors via a finite extension K ′ /K
       that the subspace is rational over. This extension has degree bounded by a polynomial
       in ℓ, as its Galois group is a subgroup of GL(FuG ), whose rank is independent of ℓ.
     • Step 5: Follows from the complexity of Algorithm 8.
     • Step 6: Follows from [Mas20], i.e., the complextiy of Theorem 4.4. The preceision e
       required depends on the complexity of the algebraic numbers occurring in an explicit
       description of the Edixhoven subspace. We know by Theorem 4.5 that the heights
       are bounded by a polynomial in ℓ. Further, the points occurring in the support of
       the divisors concerned, each also have degree bounded by a polynomial in ℓ, as the
       Edixhoven subspace becomes rational over such an extension.
     • Step 7: The G- action on the space of tensors can be computed element by element,
       as its dimension is independent of ℓ.
     • Step 8: Again the Gal(K/K) action factors through a finite extension K ′′ /K, with
       degree bounded by a polynomial in ℓ. Its action on E is obtained via points on Ṽ,
       and the action on Fu can be computed akin to Step 4.
                                                                                           □

                                      7. Conclusion
   In this article, we have provided an algorithm to compute the number of points on a
fixed, nice surface in polynomial time, having made its étale cohomology groups explicit. An
area for improvement would be the dependence of the total complexity on the degree of the
surface which is, at the moment, exponential. In another direction, one could ask if in the
realm of quantum algorithms, the dependence on the degree could be made polynomial. The
immediate next question, with regard to point counting, is that of algorithms for varieties of
a higher dimension, to begin with, threefolds. Specifically, one would need a method to com-
pute vanishing cycles, the Poincaré duality pairing in H2 and the corresponding trivialising
cover.

Lines 1616-1698
                               Appendix B. Height bounds
 In this section, we recall the theory of heights and state certain height bounds to comple-
ment our algorithms.

Let K/Q be a number field. Denote by MK the set of places of the ring of integers OK
and denote by vp for p ∈ MK the associated p – adic valuation. Let Kp denote the comple-
tion of K and set nvp = [Kp : Qp ].
Definition B.1. Let P = [x0 : . . . : xN ] ∈ PN (K) be a point. The Weil height h(P ) is
defined as                                                       
                                1      X
                     h(P ) =               nvp · log(max ∥xj ∥vp ) .
                             [K : Q] p                j


Definition B.2. Let C be a curve over K and let J denote its Jacobian. The Néron-Tate
height, denoted ĥ for a point P ∈ J is defined as follows
                                                  h(2j P )
(B.1)                                ĥ(P ) := lim         .
                                              j→∞   4j
   It is clear that the Néron-Tate height vanishes on torsion points. We next recall the
following, that relates the two height functions introduced above, on an abelian variety.
Theorem B.3 (Zarhin-Manin). Let A be a polarised abelian variety over a number field K,
together with an ample, symmetric line bundle Θ. Then, there exist constants c1 and c2 ,
depending on A and g such that for any P ∈ A(K),
(B.2)                           ĥ(P ) − c1 ≤ h(P ) ≤ ĥ(P ) + c2
with
      2g−1                       
      2                   2g−2   67                                            1
c1 =        + 1 ·hΘ (A)+ 2     +     ·g·log 2 and c2 = (22g −1)·hΘ (A)+(22g+1 − )·g·log 2,
        3                        12                                            3
  where hΘ (A) is the height of the neutral element 0A of A.
                                               34
Proof. Apply [ZM72, 3.2] to the divisor 4 · Θ.                                            □

Theorem B.4 (Height of torsion point). Let C ⊂ PN be a smooth, projective curve of genus
g and degree D over a number field K, and denote by J its Jacobian. Let ℓ be a prime
number, and let P ∈ J[ℓ] be an ℓ – torsion point. Consider the embedding of J into PM
given by Theorem D.1. Then, we have

                                        |h(P )| ≤ C,

where C is a constant that depends only on N , g, D, the height of the coefficients of the
equations defining C, the extension degree, and the logarithm of the discriminant of the
number field K/Q. The dependence is polynomial in the last three items. In particular, the
height of an ℓ – torsion point is bounded by a quantity independent of ℓ.

Proof. As P is assumed to be torsion, we know ĥ(P ) = 0. We note firstly, that by Theo-
rem D.2, the height of the Jacobian constructed in Theorem D.1 is bounded above by the
height associated to the 4 · Θ – embedding. The result then follows from Theorem B.3,
combined with the results of [PW21, §2] and [Rém10, §1].                             □

Remark. Theorem B.4 holds with the base field K replaced by a function field Fq (t) or a
function field over a number field K(t). We merely change the notion of height; in the
former case, one uses a geometric height function, and in the latter case, a height function
that captures both the geometric and arithmetic data, such as Moriwaki’s height function
[Mor00]. The general underlying principle is that the naive height only differs from the
canonical height by a bounded amount (see [Sil83, §4]).

  We now recall a result of Javanpeykar, which resolves a conjecture of Edixhoven-de Jong-
Schepers [EDJS10, Conjecture 5.1], that bounds the Faltings height of the Jacobian of a
ramified covering of the projective line.

Theorem B.5 (Javanpeykar). Let U ⊂ P1Z be a nonempty open subscheme. There exist
integers a, b ∈ Z>0 such that for any prime ℓ, and any connected finite étale cover

                                      Ψ : V → UZ[1/ℓ] ,

the Faltings height of the Jacobian of the normalisation of P1 in the function field of V is
bounded by
                                          (deg Ψ)a
where a is a constant that depends only on the height of Z = P1Q \ UQ and the action of
Gal(Q/Q) – on Z. In particular,
                                                        3 A−2
                                                               
                        a = 6 + log 13 · 106 A · (4AB)45A 2 A!

where A is the number of elements in the orbit of Z under the action of Gal(Q/Q) and B is
a bound for the height of the elements of Z.

Proof. See [Jav14, Theorem 6.0.6].                                                        □
                                             35
                                Appendix C. Results of Igusa
  In this appendix, we recall certain results of Igusa related to fibre systems of Jacobian

Lines 1740-1835
[And02], who provides an ‘elementary’ algebraic construction of the Abel map [And97]. In
[And04], it is shown that the construction matches with an ‘edited’ 4 · Θ – embedding asso-
ciated to the Θ – divisor on the Jacobian of a curve.

   We explain briefly Anderson’s construction of the ‘abstract Abel map’. Let C ⊂ PN be a
smooth, projective curve of genus g over a field K. Let E be a line bundle of degree w ≥ 2g+1
and let D be a line bundle of degree zero. Let u be a basis for H0 (C, D−1 ⊗ E) and let v be
a basis for H0 (C, D ⊗ E). Denote by C {0,...,w+1} the w + 2 – fold power of C with numbering
remembered, and for a section f of a line bundle on C, denote by f (i) the pullback by the
ith projection. Then the abstract Abel map sends D to the w × w matrix with entries
                                      (0)      ..       ..      (0)
                                    vd          .        .    u
                                                              d
                                       ..      (i)      (j)
                                                                ..
                                        .    uc       vc         .
(D.1)                   abel(D)ij =       ·     .  ·     .  ·
                                      (i)
                                     vc         ..       ..   u
                                                              d (j)
                                      ..                         ..
                                       .    u\
                                             (w+1)   v\
                                                      (w+1)       .
for 1 ≤ i, j ≤ w, where the leftmost term in the product denotes the determinant of the
w × w matrix obtained by stacking the v (t) as row vectors numbered 0 to w + 1 and removing
the rows numbered 0 and i. In particular, the construction maps classes of degree zero line
bundles to w × w matrices with the entry from the ith row and j th column being from the
space
                                               Nw+1 (s) ⊗4               !
                                                      E
                H0 C {0,...,w+1} ,     ⊗2
                                                  s=0
                                                 ⊗2        ⊗2          ⊗2   .
                                   (E ) ⊗ (E ) ⊗ (E (j) ) ⊗ (E (w+1) )
                                     0       (i)


In summary, the abstract Abel map gives a way to realise any degree zero divisor on C as a
point on its Jacobian, embedded into projective space.

We now sketch below how to obtain the equations for the Jacobian, i.e., the ideal of poly-
nomials vanishing on the image of the abstract Abel map.
   (1) Fix an effective divisor E of C with deg(E) ≥ 2g + 1.
   (2) Set w = dim L(E) = deg(E) − g + 1.
   (3) Write S = supp(E), A = H0 (S, OC ) and L = L(2E).
Then, the Jacobian of C is given by the projective algebraic variety J of K – proportionality
classes of Jacobi matrices of type (K, w, A, L). A proof is given in [And02, Theorem 4.4.6].
From [And02, 3.7.3], we see that the complexity of the construction is at worst exp(poly(g)).

In the case K = k(t) is the function field of the projective line, and C is a curve over
K, we want to choose an effective divisor E on C for the embedding so that upon speciali-
sation to a smooth value t = u, the corresponding embedding of the Jacobian of Cu is given
by Eu . This is achieved as follows.
                                             37
     • Choose an effective divisor E of C of degree ≥ 2g + 1 via taking all the zeros of a
       rational function λ on C, with k(t) – coefficients. We may assume div(λ) = λ+ − λ− ,
       with λ+ and λ− effective of degree ≥ 2g + 1, and no redundancies between them.
       Also assume that the divisor E specialised to any u ∈ P1 contains no singular point
       of Xu in its support.
     • For a smooth point u, the associated divisor Eu is obtained by specialising λ+ to u.
     • The Jacobian of the curve Cu corresponds to the specialisation of the Jacobian of C
       at t = u, via the divisor Eu .

Algorithm 10 Abstract Abel map and its inverse on ℓ – torsion
      • Input: The generic fibre Xη of a Lefschetz pencil π : X → P1 on a smooth projective
        surface X over a number field K, and a degree zero divisor D ∈ Pic0 (Xη )[ℓ] repre-
        sented using Theorem 2.2.
      • Output: The image abel(D) of the map in (D.1) as a point in projective space PM
        lying on the Jacobian Jη , satisfying the conditions of the paragraph above.
 1: Choose an effective divisor E of Xη of degree w ≥ 2g + 1 via taking all the zeros of a
    rational function λ, with K(t) – coefficients on Xη . We may assume div(λ) = λ+ − λ− ,
    with λ+ and λ− effective of degree ≥ 2g + 1, and no redundancies between them. Also
    assume that the divisor E specialised to any u ∈ P1 contains no singular point of Xu in
    its support.
 2: Compute bases v for H0 (Xη , E + D) and u for H0 (Xη , E − D) using an effective Riemann-
    Roch algorithm via Theorem 2.1.
 3: Maintaining w + 2 sets of variables, compute the pullbacks u(i) and v (j) for each i, j ∈
    {0, . . . , w + 1}. These are merely the same rational functions associated to a specific set
    of variables.
 4: Compute the map (D.1) using these pullbacks.
                                                            0
 5: For any u ∈ P1 , the embedding of the Jacobian Pic (Xu ) ,→ PM is given by the divisor
    Eu . If we specialise the input divisor D to u, we get Du ∈ Pic0 (Xu )[ℓ].
                                     0
 6: To invert the Abel map on Pic (Xu )[ℓ], given a point in PM corresponding to an element
    of Pic0 (Xu )[ℓ], we simply go through all the ℓ2g divisorial representatives of ℓ – torsion as
    a result of the algorithm from Theorem 2.2 and check which of them map to our given
    point via the divisor Eu and the map (D.1). There will be a unique pre-image as the
    Abel map is injective.

Remark. The only dependence on ℓ in Algorithm 10 is the input divisor D ∈ Pic0 (Xη )[ℓ]. By
Theorem 2.2, we know that D can be efficiently represented poly(ℓ) time and the bases for
the Riemann-Roch spaces H0 (Xη , E ± D) are computed using Theorem 2.1.
   By [Igu56a, Theorem 3] (see also [Igu56b]), we know that the specialisation of the Jacobian
of the generic fibre Xη of a Lefschetz pencil π : X → P1 on a surface X to a singular z ∈ Z