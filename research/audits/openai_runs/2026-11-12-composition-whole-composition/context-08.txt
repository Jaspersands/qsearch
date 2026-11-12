Source https://www.cse.iitk.ac.in/users/nitin/papers/etale-P1.pdf
SHA256 text bcc728c78de1828f39e88933aa1532997e4c42c3e06fa4f864eb1ca6a1d90059

Physical lines 615-680
odromy in a Lefschetz pencil. We then recall a big mod-ℓ monodromy result, obtained by an adap-
tation of work of Hall. Finally, we state a version of Deligne’s equidistribution theorem [Del80,
3.5.3] due to Katz. As before, let π : X̃ → P1 be a Lefschetz pencil of curves on a smooth, projec-
tive surface X. We denote by U0 ⊂ P1 the locus parameterising smooth fibres (of genus g) and by
U = U0 × Fq . Let Z = P1 \ U be the finite set parameterising the critical fibres. Write F = R1 π⋆ Qℓ
and F ℓ = R1 π⋆ µℓ for the respective direct-image sheaves.
     7we omit Tate-twists by fixing an isomorphism Z/ℓZ ≃ µ (F ) and choosing a generator for the group of roots of
                                                                  ℓ   q
unity.
   8if f (T ) = Q (1 − α T ), then f (T )(r) := Q (1 − αr T ).
                 j      j                        j      j
                                   THE FACTOR P1 (T ) OF THE ZETA FUNCTION                                  13


    Let u ∈ U be a geometric point. The arithmetic étale fundamental group (see [Mur67] for the
definition) π1 (U0 , u) acts on Fuℓ and by passage to the limit, on Fu . This latter representation
restricted to the geometric étale fundamental group π1 (U, u) is called the monodromy of the pencil.
Since F is tamely ramified, the action of π1 (U, u) factors through the tame fundamental group 9
π1t (U, u). By a theorem of Grothendieck [Gro57, 182-27], π1t (U, u) is generated topologically by #Z
elements σi for each zi ∈ Z, satisfying the relation Π#Z i=1 σi = 1. The Picard-Lefschetz formulas
make this action explicit. See [Mil80, Ch V, Theorem 3.14] or [FK13, III.4.3] for a proof.
Proposition 3.4 (Picard-Lefschetz formulas). For any γ ∈ Fuℓ , we have
(3.1)                                     σi (γ) = γ − ϵi · ⟨γ, δzi ⟩ · δzi ,
                                                                      1/ℓ       1/ℓ
where for a uniformising parameter θi at zi , we have σi (θi ) = ϵi · θi .
   Clearly, the monodromy action respects the symplectic pairing. By the hard-Lefschetz theorem,
we know that H1 (Xu , Qℓ ) ≃ H1 (X, Qℓ ) ⊕ Eu , with H1 (X, Qℓ ) = Eu⊥ . In particular, π1 (U, u) acts
trivially on H1 (X, Qℓ ), implying that the monodromy action factors through Sp(Eu ), the group of
symplectic transformations of the vector space Eu . We know [Del74, 5.10] that the image of π1 (U, u)
is open and Zariski-dense in Sp(Eu ). Further, by the conjugacy of vanishing cycles, we also know
π1 (U, u) acts absolutely irreducibly on Eu .
   One seeks a version of the above to compute the mod-ℓ geometric monodromy for certain equidis-
tribution estimates coming from Theorem 3.7. Consider the torsion-free sheaf R1 π⋆ Zℓ of rank 2g
on U . It has as subsheaf, the sheaf of integral ℓ-adic vanishing cycles EZℓ ⊂ R1 π⋆ Zℓ of rank, say,
2r. This in turn, corresponds to representations ρ : π1 (U0 , u) → GL(2r, Zℓ ) and ρ = ρ|π1 (U, u).
Let V := EZℓ ⊗Zℓ Fℓ be the lisse Fℓ -sheaf giving rise to, respectively, the mod-ℓ representations ρℓ
and ρℓ . There are multiple ways to show big mod-ℓ monodromy for ‘almost all primes ℓ’ (all but
finitely many), but [Hal08, §4-6] gives a method that works for every prime ℓ ≥ 5 invertible on
the characteristic. However, the generic rank of the local system V is a priori dependent on ℓ, and
guaranteed to be 2r only when the cohomology groups Hi (X, Zℓ ) are all torsion-free. The following
result appears to be known to Hall and Katz ([Hal08, pg 5] and [Hal23]); for completeness, we
provide a brief proof below.
Theorem 3.5 (Big mod-ℓ monodromy). If Hi (X, Zℓ ) are all torsion-free, we have
                                        G := ρℓ (π1 (U, u)) = Sp(2r, Fℓ ).
Proof. As the groups Hi (X, Zℓ ) are all torsion-free, we know (analogously to the situation in [Kat11,
Theorem 9.2]) that the hard-Lefschetz theorem holds with Fℓ – coefficients, i.e., for a smooth
hyperplane section Xu obtained as a fibre of our Lefschetz pencil, we have
                                         H1 (Xu , Fℓ ) ≃ H1 (X, Fℓ ) ⊕ Vu .
We now show that the representation Vu of π1 (U, u) is irreducible. Indeed if W ⊂ Vu is a stable
subspace, for any γ ̸= 0 ∈ W , we must have ⟨γ, δj ⟩ ̸= 0 for some j, as otherwise the Weil pairing
would be degenerate on H1 (Xu , Fℓ ). Therefore, by (3.1), this implies σj (γ) − γ = ϵj · ⟨γ, δj ⟩ · δj ∈ W .
As the vanishing cycles are all conjugate under the action of π1 (U, u) [Kat73a, 6.6], this means
δi ∈ W for all i, or W = Vu .
   We then invoke a theorem of Hall [Hal08, Theorem 3.1], to conclude that the image is in fact
the full symplectic group, due to the irreducibility and the transvections coming from the Picard-
Lefschetz formulas.
                                                                                                           □

  9essentially classifying finite étale covers of U tamely ramified over Z.
 14                   DIPTAJIT ROY, NITIN SAXENA          , AND MADHAVAN VENKATESH


   Let X0 /Fq now be obtained via good reduction from a smooth, projective, geometrically irre-
ducible surface X0 over a number field K at a prime p. We assume X0 ⊂ PN is of degree D > 0 and
given by the vanishing of homogeneous forms f1 , . . . , fm each of degree ≤ d. Denote X := X0 ×Fq Fq
and X an := X0 ×K C, equipped with the complex analytic topology. One has the following.

Physical lines 859-955
4.2. Lefschetz pencils on a surface. To study the zeta function of a surface, intuitively, one
wants to break it up into those of curves, each parameterized by a single variable t, and then invoke
the methods of Section 2. It is not so easy because Theorem 4.3 does not give an isomorphism when
X is a surface, e.g., H1 (Y, Qℓ ) can be a larger group for a generic curve Y lying on the surface X,
which will make the zeta function of Y ‘larger’ than that of X, introducing errors called vanishing
cycles (see Section 3.1).
   To explore these issues, in this subsection, we introduce the classic machinery of Lefschetz pencils
and describe an algorithm to fibre a given smooth projective surface X ⊆ PN of degree D over
the projective line so that the fibres are curves with singularities at worst being ordinary double
points. We assume X is given by m homogeneous forms f1 , . . . , fm , each of total degree ≤ d ∈ Z>0 .
Denote by (PN )∨ , the dual projective space.
Definition 4.4. Let X/Fq be as above. A Lefschetz pencil on X is a collection of hyperplanes
(Ht )t∈P1 such that there exists a line L ≃ P1 ⊂ (PN )∨ ; for e.g., (λ, µ) 7→ λF = µG, for linear forms
F, G on PN , satisfying the following conditions
      • the axis, of the pencil, ∆ := (F = 0) ∩ (G = 0) in PN intersects X transversally, i.e., X ∩ ∆
        is smooth of codimension 2,
      • there is a dense open subset U ⊂ P1 on which the associated intersections (λ, µ) → X ∩
        (λF = µG) are smooth and geometrically irreducible for (λ, µ) ∈ U ; and have only an
        ordinary double point as singularity for the finitely many (λ, µ) ∈   / U.
  It is a fundamental theorem that Lefschetz pencils exist on any smooth projective variety of
dimension ≥ 2, over an algebraically closed field (see [Kat73b]). Over arbitrary fields, Lefschetz
pencils exist, subject to a degree ≥ 3 Veronese embedding.10 We recall [JS12, Theorem 3].
Proposition 4.5. There exists a nonempty open subscheme (after possibly passing to a degree ≥ 3
Veronese embedding) in the Grassmannian of lines WX ⊂ Gr(1, (PN )∨ ) such that every L ∈ WX
defines a Lefschetz pencil for X.
  Algorithmically, to construct a Lefschetz pencil, we first take a field extension to ensure the
existence of a transversal hyperplane section. We saw that the dual variety X̌ parameterises those
hyperplanes that do not intersect transversally with X. Further, its singular locus X̊ parameterises
those hyperplanes that intersect X with singularity worse than a single ordinary double point. In
other words, X̌ \ X̊ consists of those hyperplanes H such that H ∩ X has a single node (see [Mil98,
  10this adds an overhead of only a polynomial in the degree D of X.
 18                   DIPTAJIT ROY, NITIN SAXENA    , AND MADHAVAN VENKATESH


Theorem 31.2] or [Kat73b]). In light of Proposition 4.2, it suffices to randomly take two linear forms
F, G ∈ (PN )∨ . With high probability, they intersect transversally with X and the line joining them
in (PN )∨ intersects X̌ at finitely many points and completely misses X̊.

Algorithm 3 Lefschetz pencil on a surface
      • Input: A smooth projective surface X0 /Fq of degree D presented as a system of homoge-
        neous polynomials of degree ≤ d in the projective space PN .
                                                                                    N +3
      • Pre-processing: Replace X with the degree 3 Veronese image of X in P := P( 3 )−1 .
      • Output: Hyperplanes F and G in P such that the line L through them in the dual (P)∨ ,
        is a Lefschetz pencil on X.
 1: Take a field extension FQ /Fq with degree bounded by a polynomial in D, such that smooth
    hyperplane sections exist as in Proposition 4.2.
 2: Select two random linear forms F and G on P, such that they intersect transversally with X
    (this is possible by Proposition 4.2).
 3: The line L in (P)∨ through F and G is a Lefschetz pencil on X.



Lemma 4.6. Algorithm 3 succeeds with probability at least 1 − O(1/Q).
Proof. Indeed for Q ≫ D, the locus of hyperplanes in P∨ defined over FQ that do not intersect
transversally with X is given by the dual variety X̌, which by the Lang-Weil estimates, can be
avoided with probability 1 − O(1/Q). Further, for two hyperplanes H1 and H2 that intersect
transversally with X, the condition that they define a Lefschetz pencil on X is equivalent to the
condition that the line through the corresponding points in P∨ does not intersect the singular locus
X̊ of X̌. For two randomly chosen hyperplanes, this is also ensured with probability greater than
1 − O(1/Q), again by a Lang-Weil argument.
   One checks that the output is correct by computing the finite subset Z of ‘bad’ hyperplanes
(which is possible in poly-time) and verifying that the associated fibres are indeed nodal curves.
The latter can be done by blowing up at a singular point and checking that the exceptional divisor
intersects the transformed curve at two points, which has a polynomial-time algorithm.            □
   Blowing up X along X ∩ ∆ gives a smooth projective surface X̃ and a morphism π : X̃ → P1
such that the fibre of a [λ : µ] ∈ P1 is the curve X ∩ (λF = µG). Algorithmically, the locus ∆ ∩ X
may not all be defined over Fq and going to a field extension which contains all of the points therein
may be expensive. Further, computing the blowup X̃ → X and the morphism π : X̃ → P1 may
also be exponential in the input data. Fortunately, we are able to leave π implicit, i.e., the only
knowledge we need is that the fibre of u ∈ P1 under π is Hu ∩ X, where Hu is the hyperplane
associated to u. We describe the required construction in Algorithm 3.
   Now, consider the étale sheaf R1 π⋆ Qℓ on P1 . It is locally constant of rank 2g on U , where
g is the genus of the generic fibre X̃η (which is a curve over the function field of P1 ), where
η → P1 is a geometric generic point. By the proper base-change theorem, for a point u ∈ P1 ,
we have (R1 π⋆ Qℓ )u ≃ H1 (X̃u , Qℓ ) = H1 (X ∩ Hu , Qℓ ). Further, by [Mil98, Lemma 33.2], we have
H1 (X̃, Qℓ ) ≃ H1 (X, Qℓ ).
   We now establish bounds for the genus g of the generic smooth fibre and for the critical locus
which we call Z := P1 \ U . Pick u ∈ U , the fibre X ∩ Hu is a curve in P of degree D = deg(X). By
the results of [GLP83] (see also [Mac19, Theorem 3.3]), we have
                                         g ≤ D2 − 2D + 1.
Further, the number of critical points, i.e., #Z is bounded by the size of L∩ X̌, which by the remark
following Proposition 4.2 and Bézout’s theorem, is at most DN +1 . Denote the Betti numbers
                                THE FACTOR P1 (T ) OF THE ZETA FUNCTION                                19


βi := dim Hi (X, Qℓ ). Clearly, we have11
                                            β3 = β1 ≤ 2g ≤ 2D2 .
By [Mil80, V, Theorem 3.12], we have
                                   β2 = #Z + 2β1 + 2 − 4g ≤ 2DN +1 .
4.3. An effective gcd theorem. Now, let X0 /Fq be a smooth, projective, geometrically irre-
ducible surface of degree D > 0 obtained from good reduction of a smooth, projective surface X0
over a number field K at a prime p. We assume that X0 is presented as X0 ⊂ PN , given by a
homogeneous ideal I generated by m polynomials f1 , . . . , fm of degree ≤ d for d ∈ Z>0 . Denote by
X the base change to the algebraic closure. Let ℓ be an odd prime, distinct from the characteristic,
chosen according to Proposition 3.6. In this subsection, we prove an effective version of Deligne’s
‘théorème du pgcd’ [Del80, Théorème 4.5.1], that enables one to recover P1 (X/Fq , T ) from the zeta