Source: research/audits/sources/classical_surface_2026/surfaces.txt; locally saved source.json holds URL/SHA. Line numbers are physical pdftotext lines.

Lines 21-185:
6. Complexity analyses                                                                           26
7. Conclusion                                                                                    29
Acknowledgements                                                                                 29
References                                                                                       30
Appendix A. Recovering zeta                                                                      33
Appendix B. Height bounds                                                                        34
Appendix C. Results of Igusa                                                                     36
Appendix D. Abstract Abel map and embeddings of Jacobians                                        37




                                                1
                                        1. Introduction
1.1. Main result. Let X ⊂ PN be a fixed smooth, projective, geometrically integral (prop-
erties we abbreviate to nice) surface of degree D over a finite field Fq , described by a system
of homogeneous polynomial equations f1 , . . . , fm each of degree ≤ d. We assume X is ob-
tained via good reduction of a nice surface X over a number field K at a prime p ⊂ OK .
The zeta function of X is
                                                   ∞
                                                                  !
                                                  X            Tj
                           Z(X/Fq , T ) := exp        #X(Fqj )       .
                                                  j=1
                                                               j
Fix a prime ℓ coprime to q. From the Weil conjectures for X, we know that
                                            P1 (X/Fq , T )P3 (X/Fq , T )
                         Z(X/Fq , T ) =                                    ,
                                        (1 − T )P2 (X/Fq , T )(1 − q 2 T )
                                                   
where Pi (X/Fq , T ) := det 1 − T Fq⋆ | Hi (X, Qℓ ) is the (reversed) characteristic polynomial
of the geometric Frobenius acting on the ith ℓ – adic étale cohomology group of X. In [CE11,
Epilogue], the existence of an algorithm that computes the point count #X(Fq ) in time
polynomial in log q is conjectured. We prove this conjecture by exhibiting an algorithm that
computes the action of Frobenius on the étale cohomology groups with torsion coefficients
Hi (X, Z/ℓZ) 1 for primes ℓ = O(log q), from which the zeta function of X, and thereby
its point count can be recovered by a Chinese-remainder process. Our main result is the
following.
Theorem 1.1. There exists an algorithm that, on input X as above, outputs Z(X/Fq , T ) in
time bounded by a polynomial in log q.
Remark. This theorem is restated in more detail as Theorem 5.1 in Section 5 and proved
therein. We in fact give an algorithm to compute the étale cohomology groups Hi (X , µℓ )
with Gal(K/K) - action in time polynomial in ℓ, from which, for an input prime p, the local
zeta function and point counts follow in polynomial time.
1.2. Motivation. Our work is fundamentally motivated by the following paraphrase of a
question of Serre [Ser16, Preface].
Question (Serre). Is there an algorithm that, given a Z – scheme X of finite type, computes
the point count of its reduction #X(Fp ) at any prime p in time polynomial in log p?
   In particular, this work solves the above question in the case dim X = 2, when X is nice,
at large enough primes of good reduction. In their book on computing the coefficients of the
Ramanujan τ – function, Couveignes and Edixhoven [CE11, Epilogue] propose the existence
of a strategy to count points on surfaces over finite fields, using the theory of Lefschetz
pencils and dévissage; techniques which were used in Deligne’s celebrated proof [Del74] of
the Weil conjectures. If realised, this would be an extension of polynomial-time counting
methods from the dimension-one case of curves (and the conceptually similar case of abelian
varieties) [Sch85, Pil90] to varieties of a higher dimension.
   An important motivation for these algorithms is computational evidence for conjectures
in the Langlands program [Gel84], a vast philosophy encompassing several areas of modern
  1we abuse notation by referring to the base change of X to X ×
                                                                   Fq Fq , also as X
                                                  2
mathematics including number theory, representation theory and algebraic geometry. An
object of study in part of the program, is the L – function of a variety X /Q, a conglomeration
of the zeta functions at all the local factors. The Langlands-Rapoport conjecture [LR87], in
particular, gives the mod – p point-counts of Shimura varieties 2 a certain group-theoretic
description.
   Another angle of motivation is diophantine geometry, i.e., counting or classifying ratio-
nal points on a variety X /Q. One approach towards this is computing the Brauer-Manin
obstruction [CTS21] (essentially measuring the failure of local-global principles) for specific
varieties. This is defined using the Brauer group H2 (X , Gm ) of the variety in question, which
is the étale cohomology in degree two, with coefficients in the multiplicative sheaf. With a
view towards the diophantine setting, it would be prudent to have algorithms for the scenario
over a finite field, with constant torsion coefficients to begin with.

1.3. Potential applications in computing. A fundamental aspect of our work is the
explicitisation of the étale cohomology of a surface, which should be viewed as an arithmetic
or discrete analogue of the usual topological or Betti cohomology over the complex numbers.
The latter notions do not translate easily to the setting over a finite field, and thus required
the revolution of the Grothendieck school, thereby putting the Weil conjectures in proper
context.
   Our work lays the stepping stones toward solving a foundational problem for topological
computation in the discrete setting, i.e., over finite fields. In particular, we, for the first
time, make explicit (and give algorithms to compute) the étale cohomology groups with
constant torsion coefficients Hi (X, µℓ ) of a nice surface X. This generalises to being able to
compute with cohomology in degrees one and two, for varieties of higher dimension as well
[RSV24, KV25].
   The progenitor of point-counting algorithms, Schoof’s algorithm [Sch85] for elliptic curves,
paved the way for elliptic curve cryptography, which is ubiquitous today. In particular, it
is necessary to run a point-counting algorithm to select a curve suitable for cryptosystems.
It is conceivable that our algorithms may come of use in efficiently designing cryptosystems
around surfaces as well. Further, Brauer groups, mentioned earlier, arise naturally in the
context of class field theory and homogeneous spaces, for which a general framework has
been proposed with regard to applications to cryptography [Cou06].

1.4. Prior work & special cases. As mentioned earlier, the first advance in point-counting
over finite fields came with Schoof’s algorithm for elliptic curves. This was generalised to
curves of higher genus and abelian varieties by Pila [Pil90]. The cohomology groups in higher
degree, however, have only recently been shown to be computable [MO15, PTvL15].
   In Roy-Saxena-Venkatesh [RSV24], a randomised algorithm was given to compute the
factor P1 (X/Fq , T ) for a nice variety X of fixed degree, in time polynomial in log q. Levrat
has sketched a strategy to compute the full zeta function for surfaces [Lev22, IV.3.5, VI.4]
(see also [Lev24, §5]) based on the description of Couveignes-Edixhoven, but its runtime is
exponential.
   When the characteristic p of the base field is fixed, the point-counting problem is essentially
solved by Lauder-Wan [LW06] for varieties and Harvey [Har15] for general arithmetic schemes

  2algebraic varieties equipped with rich arithmetic data
                                                    3
by means of p – adic algorithms. As opposed to using étale cohomology, they feature p –
adic trace formulas. These algorithms, however, have a runtime exponential in log p.

1.5. Obstructions in the prior techniques. The main difficulty in counting points on
surfaces in polynomial time so far, has been the lack of a concise representation of the étale
cohomology groups Hi (X, µℓ ), particularly for i = 2, on which the induced Frobenius action
may be computed. In the approach of Levrat [Lev24], following Edixhoven, one reduces the
computation of the group H2 (X, µℓ ) to the computation of H1 (V, µℓ ), where V is a curve
of genus polynomial in ℓ. While algorithms are known to compute the first cohomology of
curves [HI98, Cou09], their runtime is exponential in its genus. Thus for a prime ℓ of size
O(log q), which is required for the intended Chinese remainder process, the above strategy
implemented directly ends up giving an exponential-time algorithm.
   Another approach would be to work directly with the Brauer group of X, whose ℓ – torsion
the group H2 (X, µℓ ) captures. Elements in the Brauer group are, a priori, equivalence classes
of Azumaya algebras; but it is not clear how one may obtain bounds to represent them, along
with their group law and the equivalence relation they are subjected to.

1.6. Proof ideas. Our algorithm studies the étale cohomology of a surface by using the for-
malism of monodromy of vanishing cycles arising from a Lefschetz pencil. More specifically,
we fibre the given surface X as a Lefschetz pencil of hyperplane sections, and then blow it
up at the axis, yielding a morphism to P1 . The cohomology of the blowup X̃ , is understood
using the sequence (2.5) coming from the Galois cohomology of the tame fundamental group
of the line with the critical locus (i.e., the finite set Z = P1 \ U where the fibres are nodal)
removed. In particular, one needs to be able to compute the monodromy action on the
cohomology of the generic fibre.

  Our solution is to first compute the ℓ – division polynomial system (the zero dimensional
ideal whose roots are the distinct ℓ – torsion points) for the torsion in the Jacobian of the
generic fibre, and view the choice of a cospecialisation morphism at a singular point z as
picking a Puiseux series expansion around z. Working in characteristic zero, we compute
the local monodromy using this Puiseux expansion. Additionally, we identify the vanishing
cycle δz at z using an auxiliary smooth point uz within the radii of convergence of the
Puiseux expansions around z combined with numerical/diophantine approximation methods
in a technique we call ‘re-centering’. Specifically, we also compute each vanishing cycle as
an element in the ℓ-torsion of the Jacobian of the generic fibre.

   Following this, we move to the étale open cover V → U trivialising the locally constant
sheaf F = R1 π⋆ µℓ on U. The normalisation of P1 in the function field of V yields a morphism
of smooth projective curves Ṽ → P1 ramified exactly at Z. Calling the representation
ρℓ : π1 (U, η) → Aut(Fη ), we write G := im(ρℓ ), and note that the cover V → U has Galois
group G. The group G acts naturally on Ṽ via automorphisms, which extends to an action
on H1 (Ṽ, µℓ ) ≃ Jac(Ṽ)[ℓ].

  Further, to compute the part of H2 (X , µℓ ) corresponding to H1 (U, F), it suffices to compute
the invariant subspace of H1 (Ṽ, µℓ ) ⊗Z/ℓZ Fη , under the diagonal action of G. This is done
by choosing an auxiliary prime P with characteristic distinct from ℓ and of size O(ℓ), of
                                                4
good reduction and isolating the subspace spanned by the images of all G - equivariant
homomorphisms from Fη∨ to Jac(ṼP )[ℓ] (which we call the mod-P Edixhoven subspace) in
the cohomology of the reduced curve. We then P – adically lift the concerned subspace to
the char zero Edixhoven subspace E, using work of Mascot [Mas20] on Hensel-lifting torsion
points. With this, the arithmetic Galois action follows, along with zeta function and point
counts, for large primes of good reduction.

1.7. Leitfaden. Section 2 delineates the cohomological preliminaries that form the funda-
mental basis of our algorithms. Section 3 develops subroutines including Weil pairings and
Puiseux expansions for vanishing cycles, which are used in the algorithms of Section 4. The

Lines 985-1108:
       subsequently computed.
4.1. The trivialising cover. The étale cover V → U that trivialises the locally constant
sheaf is obtained by normalising the function field of P1 in the Galois closure of the field
K(Jac(Xη )[ℓ]) that the relative ℓ – torsion Jac(Xη )[ℓ] of the Jacobian of the generic fibre
is defined over. Passage to the Galois closure of a field is efficiently possible, simply by
computing a primitive element, and going to its splitting field.
   As seen earlier, this extension is of degree bounded by a polynomial in ℓ, and a birational
planar model of the curve representing this extension can be computed via a primitive
element. Call V the curve so obtained, and denote its normalisation by Ṽ. A representation
for the latter is computed via resolution of singularities, for which there is a polynomial-time
(in the genus g of the curve) algorithm [Koz94]. Further, the associated map j : V → U can
be computed in polynomial-time. The map on the smooth compactifications j̃ : Ṽ → P1 is
ramified only at Z, and its degree is bounded by a polynomial in ℓ.
                                               20
Theorem 4.1. We have the following isomorphism of Gal(K/K) – modules
                                                     G
                            1  1         1
(4.1)                     H (P , F) ≃ H (Ṽ, µℓ ) ⊗ M

where M = Fη .

Proof. First, consider the Hochschild-Serre spectral sequence [Mil98, Theorem 14.9]

                               Hi (G, Hj (V, F|V )) ⇒ Hi+j (U, F)

associated to the Galois cover V → U. One has the five-term long exact sequence

           0 → H1 (G, M ) → H1 (U, F) → H1 (V, F|V )G → H2 (G, M ) → H2 (U, F).

Now, for large enough ℓ (i.e., so that the integral ℓ - adic cohomology groups are torsion-
free) we know by [KV25, Theorem 13], that G = Sp(Eη ), where E ⊂ F|U is the locally
constant subsheaf of vanishing cycles. In particular, by mod-ℓ hard Lefschetz, we may write
M ≃ M ′ ⊕ M ′′ , where M ′ = Eη and M ′′ ≃ H1 (X , µℓ ) is a trivial G - module. Thus, for such
ℓ, we have that Hi (G, M ) = 0 for 1 ≤ i ≤ 2, as after splitting, the centre has order 2 and acts
non-trivially on M ′ (for ℓ > 2, which we assume anyway). The passage to Ṽ follows from
a purity argument by moving to positive characteristic, thanks to Deligne’s main theorem
[Del80, Théorème 2].
                                                                                               □

4.2. Geometric Galois action. In this subsection, we describe how to compute the G-
action on points of Ṽ.
     • Consider the primitive element τ for the field extension K(Ṽ)/K(P1 ).
     • The extension has Galois group G, the geometric monodromy group. For each gen-
       erator ρℓ (σj ) ∈ G for 1 ≤ j < r, express σj (τ ) as a rational function of τ , akin to
       Algorithm 7.
     • As each σj gives rise to a birational automorphism of the smooth projective curve Ṽ,
       it hence extends to an isomorphism, which can be given in terms of polynomials.
     • Hence simply evaluate the corresponding isomorphism on the input point, this gives
       the G – action on the points of Ṽ.
     • This extends to an action on Jac(Ṽ), via divisors.

4.3. Arithmetic Galois action. We first give a method to isolate the Edixhoven subspace
E ⊂ Jac(Ṽ)[ℓ] that is relevant for the Galois contribution on the second étale cohomology of
the input surface. For this, we make use of an auxiliary prime P of good reduction, distinct
from ℓ, and work with the positive-characteristic curve ṼP .

Remark. We abuse notation by using G to also refer to the monodromy of the mod-P
Lefschetz pencil. Provided P is large enough compared to the data of the surface, there is
an equality between the number of singular fibres in char zero and in positive char. Further,
let u ∈ U and u ∈ UP such that u ≡ u mod P. Let ξ = spec(FP (t)) be the geometric generic
point. Then, we can consistently transport the G-action on Fη to Fξ via the diagram
                                               21
Algorithm 8 Computing the Edixhoven subspace modulo P
     • Input: The curve Ṽ and a prime P.
     • Output: The mod-P Edixhoven subspace EP ⊂ Jac(ṼP )[ℓ].
 1: Compute the zeta function Z(ṼP /FP , T ) by counting points on Ṽ over extensions of FP ,
    using a P - adic algorithm such as Harvey’s [Har15].
 2: Compute a basis of each space
                                    Si := Jac(ṼP )[ℓ](FPi )
    as sums of ṼP – points.
 3: Compute the G – action on each subspace Si . In particular, for each generator ρℓ (σj ),
    compute its action on Si for each i upto a bound J = poly(ℓ), using 4.2 and [Cou09,
    Theorem 1].
                                         ∨
 4: Compute each element ϕ ∈ HomG (MP      , Si ) as a matrix, and a basis of the sum of the
    images. Write                           X
                                 (i)
                                EP =                  im(ϕ).
                                                    ∨ ,S )
                                           ϕ∈HomG (MP   i

                                     (i)
 5: Compute the invariant space (EP ⊗Fℓ MP )G and its dimension. If it equals β2 − 2, return
     (i)
    EP .



                                                ϕ−1
                                                 u
                                           Fη         Fu
                                                        ϱu
                                                φ−1
                                                 u
                                           Fξ         Fu
where ϕu is a choice of cospecialisation at u, φu is the corresponding positive characteristic
choice (obtained via coefficient-wise reduction of Laurent series), and ϱu is the char-zero to
positive-char comparison isomorphism coming from reduction mod P. Thus, we have an
unambiguous G - action on MP = Fξ .
Lemma 4.2. The quantity J in Step 3 of Algorithm 8 can be assumed to be bounded by a
polynomial in ℓ.
Proof. We need to show that the subspace EP ⊂ Jac(ṼP )[ℓ] is defined over a field extension
of FP of degree at most bounded by a polynomial in ℓ. We notice that via its action on the
positive characteristic surface XP , we have a Galois representation
                               Gal(FP /FP ) → GL H2 (XP , µℓ ) .
                                                              

The general linear group is of rank β2 (the second Betti number of X ) over the field Fℓ , hence
has size bounded by a polynomial in ℓ. Further, this restricts to an action on H1 (P1 , F).
Therefore, by Theorem 4.1, it is sufficient to show that EP has dimension independent of ℓ.
Using the tensor-hom duality, we see that EP can be identified with the sum of the images
of each ϕ ∈ HomG (MP∨ , H1 (ṼP , µℓ )). The hom space has dimension bounded by β2 , and the
dimension of M is independent of ℓ, so this gives the result.                                 □
                                                 22
Remark. See also [Lev24, Lemma 5.6] for an alternate proof.
Theorem 4.3. Algorithm 8 outputs the subspace EP ⊂ H1 (Ṽ, µℓ ).
Proof. We note that EP is the sum of all subspaces of Jac(Ṽ)[ℓ] isomorphic to MP as G-
modules. Further, by Lemma 4.2, it can be found within a poly-bounded extension. The
algorithm only stops when the invariant subspace has the correct dimension, indicating that
we have found the Edixhoven subspace.                                                    □
  We now indicate how to Hensel- lift torsion points P – adically, following work of Mascot
[Mas20]. We recall the following.
Theorem 4.4 (Mascot). Let C be a model for a nice algebraic curve of genus g ′ over a
number field L given via equations, and let ρ be a mod-ℓ Gal(L/L) representation contained

Lines 1109-1276:
in a subspace S ⊂ Jac(C)[ℓ] of dimension s. Let P ⊂ OL be a prime of good reduction
for C distinct from ℓ, and assume we are given P1 (CP /FP , T ). Further, assume we can
isolate the subspace SP ⊂ Jac(CP )[ℓ]. Then, given an accuracy parameter e, there exists
an algorithm to P-adically lift the torsion subspace SP to S and compute the associated
Gal(L/L) representation in time
                                        ′
                               O(poly(g
                               e          · log(#FP ) · e · ℓs )).
Proof. This is the main result of [Mas20].                                                  □
  We now give a brief, informal sketch of Mascot’s algorithm for completeness, based on
the outline [Mas20, §1.2]. For simplicity, assume the base number field is Q, and we have a
rational prime p.
     • Compute a basis of Sp ⊂ Jac(Cp )[ℓ](Fq ), where Fq /Fp is an extension over which the
       subspace Sp becomes rational.
     • Given the accuracy parameter e, Hensel-lift the basis points to approximation O(pe )
       in Jac(C)(Qq ), i.e., points of Jac(C)(Zq /pe ).
     • Compute all the possible Fℓ – linear combinations of this basis. This is a model of S
       over Zq /pe , consisting of ℓs points.
     • Write a rational map α : Jac(C) 99K A1 defined over the field Q, and evaluate at the
       ℓs points constructed in the above step. Make sure the values are distinct, else use
       another rational map.
     • Form the monic polynomial whose roots are these values and output it.
4.4. Height of divisors in the Edixhoven subspace. In this subsection, we bound the
height of the divisors we are interested in, coming from the Edixhoven subspace. The main
estimate is the following.
Theorem 4.5. For each x ∈ E ⊂ Jac(Ṽ)[ℓ], we have
(4.2)                                 h(Dx ) ≤ poly(ℓ),
where Dx is a representation of the degree zero divisor in Jac(Ṽ)[ℓ] corresponding to x, as a
sum of points in Ṽ.
Proof. We have to show that for x ∈ E ⊂ Jac(Ṽ)[ℓ], each point in the support of the divisor
representing it, in the framework of Khuri-Makdisi’s algorithms [KM07, KM04] (as used by
Mascot), has (logarithmic) Weil height bounded by a polynomial in ℓ. The strategy is to
                                              23
make use of [CE11, Theorem 9.1.3] applied to the curve j̃ : Ṽ → P1 . We first note that
Theorems 9.1.3, 9.2.1, and 9.2.5 of [CE11] are directly applicable to our setting, as they are
concerned with a general algebraic curve or Riemann surface defined over a number field. We
address each term in the inequality of [CE11, Theorem 9.1.3] separately, showing polynomial
bounds.

1. Faltings height of the curve Ṽ.
As a first step, we invoke Theorem B.5, applied to the curve Ṽ, which is the normalisation of
P1 in the function field of the cover j : V → U. Noting that the ramification locus Z = P1 \ U
has cardinality and height depending only on the surface X and independent of ℓ, we see that
the theorem directly gives that the Faltings height hF (Ṽ) of the Jacobian of Ṽ is bounded
above by
                                             deg(j)a ,
where the quantity a is independent of ℓ. Noting that deg(j) is bounded by a polynomial in
ℓ gives the result.

2. Sup norm bounds for the Arakelov-Green’s functions The sup-norm of the
Arakelov-Green’s functions g is bounded above in terms of Faltings’ delta invariant δF (·),
by [Wil16, Corollary 4.6.2]. The quantity δF (Ṽ) is in turn bounded in Javanpeykar’s result
[Jav14, Theorem 6.0.4], by a polynomial in ℓ.

3. Bounds for the theta function For the norm of the theta function ||ϑ|| on Picg−1 (Ṽ),
we have by [Jav14, Lemma 2.4.2]
                               g
                 log ||ϑ||max ≤ log max(1, hF (Ṽ)) + (4g3 + 5g + 1) log 2,
                               4
which is clearly bounded by a polynomial in ℓ, as both the genus g of Ṽ and its Faltings
height hF (Ṽ) are.

4. An integral bound Consider the integral
                                Z
                                    log(1 + |j̃|2 )µṼ ,
                                       Ṽ

where µṼ is the Arakelov 1-1 form associated to Ṽ, regarded as a Riemann surface. By
pushing forward to P1 , one may conclude a polynomial upper bound for the integral as the
degree, the number of poles and (logarithmic) height of the polynomials defining the function
j̃ are bounded by a polynomial in ℓ. Further, the ramification locus is bounded independently
of ℓ as well.

5. Bounds for intersection numbers For an ℓ - torsion divisor Dx corresponding to
x ∈ E, one can bound the intersection numbers due to work of Wilms [Wil16, Propositions
1, 2] (see also [dJ04, Proposition 2.6.1], and more generally, the discussion in §2.6 of loc.
cit.).
   With bounds for the above quantities, it follows that for each point Px in the support of
Dx , the absolute Weil height h(j̃(Px )) is bounded by a polynomial in ℓ, by a similar argument
                                              24
as in [CE11, Proposition 11.7.1]. This implies, the same for h(Px ) as the map j̃ itself has
height and degree bounded by a polynomial in ℓ.                                           □
Remark. We note that in the proofs of each of the above components, we require Ṽ to be
semistable over K. This is possible after an extension, but the degree of the extension can be
exponential in the genus g and hence ℓ. This does not affect the bounds as the inequalities
(in particular, for the intersection number as well) are normalised by the degree [K : Q], as
in [CE11, Theorem 9.1.1], ultimately giving polynomial height bounds.
Remark. As an aside, we mention that the result of Javanpeykar, Theorem B.5, provides
a heruistic towards Theorem 4.5 in the following sense. An ℓ-torsion point in Jac(Ṽ)[ℓ] is
understood as a divisor D, corresponding to an étale µℓ -torsor j′ : W → Ṽ. The composite
map
                                         j̃ ◦ j′ : W → P1
is ramified exactly at Z, and is of degree bounded by a polynomial in ℓ. Further, the curve W
also has genus bounded by a polynomial in ℓ thanks to the Riemann-Hurwitz formula, hence
has Faltings height bounded by a polynomial in ℓ by Theorem B.5. This suggests that the
(logarithmic) Weil height of the algebraic numbers that appear in a “minimal” expression
for the divisor D should also likewise be bounded by a polynomial in ℓ.
  We conclude with the below table, drawing a rough comparison with the leitmotif of the
work [CE11].

 Couveignes-Edixhoven                              This work

 Modular curve X1 (5ℓ)                             The curve Ṽ

 The Ramanujan subspace V ⊂ J1 (5ℓ)[ℓ]             The Edixhoven subspace E ⊂ Jac(Ṽ)[ℓ]

 Hecke action to compute V                         Monodromy action to compute E.
                     Table 2. Comparison to Couveignes-Edixhoven



                                    5. Main theorem
  In this section, we state and prove our main result.
Theorem 5.1. Let X be a fixed, nice surface of degree D defined over a number field K.
Then, there exists a randomised algorithm that
   (i) on input a prime number ℓ, outputs the étale cohomology groups Hi (X , µℓ ) for 0 ≤
       i ≤ 4 along with the Gal(K/K) action in time
                                           poly(ℓ),
   (ii) on input a prime p ⊂ OK of good reduction with OK /p = Fq , outputs the zeta function
        of the reduction Z(X/Fq , T ), and the point-count #X(Fq ) in time
                                         poly(log q).
                                              25
Proof. The computation of the cohomology groups Hi (X , Z/ℓZ) for i = 1, 2 is in Algorithm 9.
The computation for i = 3 follows from that of i = 1 using Poincaré duality, while the cases
i = 0, 4 are via suitable twists of the cyclotomic character. The complexity is proved in
Lemma 6.7.
  Part (ii) follows in a manner similar to that mentioned in [Mas20, Remark 1.2]. One uses
an efficient algorithm to compute the image of the Frobenius element at large primes, upto
conjugacy, such as [DD13], combined with Section A to recover the zeta function and point
count.                                                                                     □


Algorithm 9 Computing the cohomology groups Hi (X , µℓ )
     • Input: A smooth projective surface X ⊂ PN of degree D over a number field K
        presented as a system of homogeneous polynomials of degree ≤ d and a prime number
        ℓ.
     • Pre-processing: Fibre X as a Lefschetz pencil π : X → P1 . Let Z ⊂ P1 parametrise
        the singular fibres and U = P1 \Z the smooth ones. Embed the Jacobian of the generic
        fibre Xη into PM obtaining the ℓ – torsion Pic0 (Xη )[ℓ] as the K(t) – roots of the ideal
        (ℓ)
            Iη using Algorithm 2.
     • Output: The cohomology groups Hi (X , µℓ ) for 1 ≤ i ≤ 2 presented as Fℓ – vector
        spaces with bases and Gal(K/K) – action.
 1: Choose a point u ∈ U(K) of bounded height and degree, to serve as base point.
 2: Compute a cospecialisation ϕu : Fu → Fη , by making a choice of expansion for the
    primitive element τ around u, hence obtaining each γ ∈ Fη as Laurent series around u.
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

Lines 1277-1395:
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

Lines 1617-1698:
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

