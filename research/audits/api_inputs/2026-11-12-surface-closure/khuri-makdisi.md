Primary source: https://arxiv.org/abs/math/0105182
SHA256 of retained text 706c51d45bf55ae2acd77c377cad980edf24afe4de24b0b13294bce7037d1d42
PDF control characters removed; mathematical text unchanged.
arXiv:math/0105182v3 [math.NT] 29 Jun 2002
                                             Linear algebra algorithms for divisors on an algebraic curve

                                                                              Kamal Khuri-Makdisi

                                                     Abstract. We use an embedding of the symmetric dth power of any algebraic
                                                     curve C of genus g into a Grassmannian space to give algorithms for working
                                                     with divisors on C, using only linear algebra in vector spaces of dimension
                                                     O(g), and matrices of size O(g 2 ) × O(g). When the base field k is finite, or
                                                     if C has a rational point over k, these give algorithms for working on the
                                                     Jacobian of C that require O(g 4 ) field operations, arising from the Gaussian
                                                     elimination. Our point of view is strongly geometric, and our representation
                                                     of points on the Jacobian is fairly simple to deal with; in particular, none
                                                     of our algorithms involves arithmetic with polynomials. We note that our
                                                     algorithms have the same asymptotic complexity for general curves as the
                                                     more algebraic algorithms in Hess’ 1999 Ph.D. thesis [He1], which works with
                                                     function fields as extensions of k[x]. However, for special classes of curves,
                                                     Hess’ algorithms are asymptotically more efficient than ours, generalizing other
                                                     known efficient algorithms for special classes of curves, such as hyperelliptic
                                                     curves [C], superelliptic curves [GPS], and Cab curves [HS]; in all those cases,
                                                     one can attain a complexity of O(g 2 ).




                                                                                  1. Introduction
                                                  Let C be a smooth algebraic curve of genus g over a field k, and assume for
                                             simplicity in this introduction that C has a rational point over k. When g = 1, C
                                             is an elliptic curve, and can be represented as a plane cubic; this is the Weierstrass
                                             model. In that case, the group law on C is easy to describe and to implement, and
                                             has led to many effective algorithms in cryptography that make use of the difficulty
                                             of solving the discrete logarithm problem in the group of k-rational points of C
                                             when k is a finite field. If the genus of C is larger, then one can try to work with
                                             the group law on the Jacobian of C. If C admits a morphism of small degree to
                                             P1 (for instance, if C is hyperelliptic), and if the genus g is large compared to the
                                             order of k, then subexponential algorithms are known for the discrete logarithm on
                                             the Jacobian; see [AdMH] for hyperelliptic curves, [GPS] for superelliptic curves,
                                             and [He1] for general curves. Computing in the Jacobian of a large genus curve is
                                             nonetheless of intrinsic interest.
                                                  One problem is that for large g, the Jacobian is somewhat difficult to describe
                                             directly as an algebraic variety. For instance, if one wishes to embed the Jacobian
                                             into projective space, the standard way is to take a very ample line bundle (say, 3
                                             or 4 times the theta-divisor), which leads to an embedding of the Jacobian into a
                                                 1991 Mathematics Subject Classification. 11Y16, 14Q05, 14H40, 11G20.
                                                 Version submitted for publication, March 26, 2002.
                                                                                            1
2                               KAMAL KHURI-MAKDISI


projective space of exponentially large dimension (e.g., 3g − 1 or 4g − 1). This is not
practical for explicit computations, especially as the equations defining the group
law on the Jacobian will probably be similarly intractable. The other way to deal
with the Jacobian is to use the fact that it is essentially an ideal class group attached
to the function field of C; a divisor is a certain kind of ideal, and linear equivalence
between divisors is equivalence in the ideal class group. Thus one works directly
with divisors (or ideals) on C, and spends time mostly on finding appropriate
elements of the function field in order to reduce divisors to a canonical form modulo
linear equivalence. If the curve C is hyperelliptic, this is relatively easy, since the
Jacobian is analogous to the ideal class group of a quadratic field; questions about
the Jacobian can be translated into questions about binary quadratic forms over
the polynomial ring k[x]. This allows one to implement the group operations on the
Jacobian of a hyperelliptic curve in “time” proportional to g 2 , as in [C]. By this
we mean that the algorithms require O(g 2 ) operations in the field k. The articles
[GPS] and [HS] give O(g 2 ) algorithms for a wider class of curves, the superelliptic
and Cab curves, using more sophisticated techniques to work with the ideal classes;
the implied constants are however quite large, and there is some possibility that
they could grow with the genus g. As for a general curve of genus g, there are
algorithms by F. Hess (see [He1] and [He2]), which both implement the group
operations in the Jacobian, and determine its group structure over a finite field.
Hess’ algorithms begin with a map of degree n from the curve C to P1 , and work
with ideals in the function field of C, viewed as a degree n extension of k[x]. If n is
fixed or bounded, then Hess’ algorithms require O(g 2 ) field operations to implement
the group law on the Jacobian. This generalizes the previously mentioned results on
hyperelliptic, superelliptic, and Cab curves. However, the minimum possible n for a
general curve of genus g is approximately g/2 (see [GH], p. 261). In this case (and,
more generally, for n = O(g)), the complexity of Hess’ algorithms rises to O(g 4 )
field operations per group operation in the Jacobian. Besides Hess’ algorithms for
general curves, we note two earlier geometric algorithms that are due to Huang and
Ierardi [HI] and Volcheck [V]. Both algorithms rely on a description of C as a plane
curve with singularities, and the steps can become fairly involved (approximately
O(g 7 ) field operations are needed per group operation in the Jacobian).
     In this paper, we give a set of straightforward geometric algorithms for the
Jacobian of C that involve only O(g 4 ) field operations. Moreover, our algorithms
are quite simple to implement, as they only involve linear algebra (row reduction) on
matrices of size O(g 2 )×O(g), and in vector spaces of dimension O(g). In particular,
no polynomial algebra is ever used explicitly (a fortiori, no Gröbner bases or field
extensions either). One can however argue that the representation of C that we
use implicitly works with quadratic polynomials in O(g) variables. Specifically,
we take a line bundle L on C, whose degree N is approximately 6g, and work
with the projective representation of C arising from H 0 (C, L). In our setting, the
homogeneous ideal defining C is generated by quadratic polynomials (elements of
Sym2 H 0 (C, L)), which can be thought of as the kernel of the multiplication map
(1.1)       µ : H 0 (C, L) ⊗ H 0 (C, L) → Sym2 H 0 (C, L) → H 0 (C, L⊗2 ).
We note that the dimensions of the vector spaces H 0 (C, L) and H 0 (C, L⊗2 ) are both
O(g), being approximately 5g and 11g, respectively. Then µ can be described in
terms of any suitable bases for these vector spaces. This article does not present any
new ideas on how to efficiently construct curves C represented in the above form,
      LINEAR ALGEBRA ALGORITHMS FOR DIVISORS ON AN ALGEBRAIC CURVE                   3


and, what is more, how to construct curves along with some nontrivial elements of
their Jacobians. Nonetheless, the first question is easy to answer in principle: for
example, choose a polynomial f (x, y) which describes a plane curve with singular-
ities that is a projection of C, and which passes through a given nonsingular point
P0 such as (0, 0); then we can let L = OC (N P0 ), and use the algorithms of [He1]
and of [He2] (or perhaps those of [HI] or of [V]) to compute the global sections
of L and of L⊗2 , and hence the map µ. This must only be done once, in obtaining
the initial description of C in the form suitable for our algorithms. As for the sec-
ond question above, we have not come up with any interesting methods to produce
divisors on our curve C, corresponding to nontrivial points on the Jacobian. The
best that we can do is to suggest choosing the plane curve to pass through a small
number of given points P1 , . . . , Pn , with n small compared to g. Then we can obtain
divisors generated by the P1 , . . . Pn , but these divisors may not be “typical,” for
all we know. Another topic that we have not addressed (but which is covered in
[He1]) is the question of efficiently computing the order, or, even better, the group
structure, of the Jacobian over a finite field.
     The basic forms of our algorithms, given in Section 4, are fairly easy to describe
and to understand. The algorithms involve only subspaces of the two vector spaces
H 0 (C, L) and H 0 (C, L⊗2 ) and the map µ, and require one to solve various systems
of linear equations in this setting. In Section 5, and to a lesser extent in Section 4,
we give some faster, but slightly more complicated, algorithms for working with
divisors on C and with the Jacobian, including an algorithm that essentially solves
the general Riemann-Roch problem for a divisor (written as a difference of effective
divisors) D1 − D2 in time O(max(g, deg D1 , deg D2 )4 ). These faster algorithms still
require time O(g 4 ), but work with vector spaces of smaller dimension; for example,
we can get away with taking the line bundle L to have degree approximately 3g, but
then need to work (implicitly) with polynomials of higher degree in the projective
embedding of C. Nonetheless, the structure of our faster algorithms is virtually
identical to that of the basic forms of our algorithms. Our results follow from three
main insights:

    1. We use a simple representation for effective divisors D on C, in terms of the
       projective embedding given by the line bundle L above. Namely, so long
       as the degree d of D is small compared to that of L, we can identify D
                                            ∗
       uniquely by the linear subspace WD     of projective space that is spanned by
       D (in a way that makes sense even if D has points of multiplicity greater
       than 1). Dually, we represent D by the space WD ⊂ H 0 (C, L) consisting of
       global sections s ∈ H 0 (C, L) that vanish at D. Since the effective divisor D
       corresponds to a point on the symmetric power Symd C, we are essentially
       working with an embedding of C into the Grassmannian parametrizing codi-
       mension d subspaces of H 0 (C, L). As discussed in Section 2 below, this is
       much better than passing to a projective model of Symd C using the Plücker
       embedding. Perhaps other computational issues in algebraic geometry can
       become simpler if one is willing to work more extensively with Grassman-
       nians and linear algebra, instead of always sticking to projective space and
       polynomials. The author hopes that this article will promote further inves-
       tigation into the topic.
    2. We no longer insist on reducing divisors to a canonical form, but instead
       represent an element of the Jacobian as an effective divisor of a certain
4                                   KAMAL KHURI-MAKDISI


        degree d ≥ g + 1. The basic form of our algorithms in Section 4 can use any
        d ≥ 2g +1, and an improvement in Section 5 uses d ≥ g +1. It is quite doable
        to bring this down to d = g, but at the expense of some complications in the
        algorithms. As a result, a given element of the Jacobian can be represented
        by many different subspaces WD , where only the linear equivalence class of
        D is well-defined. We of course give an algorithm to determine when two
        divisors represent the same point in the Jacobian; it also takes time O(g 4 ).
        (More precisely, our algorithms take time O(max(d, g)4 ), in case someone
        should wish to work with divisors of extremely large degree.)
     3. We work in terms of multiplication of sections of line bundles, as well as a
        form of division (Lemma 2.2 and Lemma/Algorithm 2.3). This amounts to
        working directly in the projective coordinate ring of C, instead of the full
        polynomial algebra of the projective space in which C lies. This produces
        a substantial time savings, since for fixed ℓ << g, the space of degree ℓ
        polynomials has dimension O(dim V ℓ ) = O(g ℓ ), while the restriction of such
        polynomials to C is the space H 0 (C, L⊗ℓ ), whose dimension is O(ℓg). More-
        over, the multiplication and division operations are the basis of our addition
        and flipping algorithms (Theorems/Algorithms 3.6 and 3.10), which are fun-
        damental to our work. The flipping algorithm is especially important: given
        a divisor D on C, and a hyperplane containing D, it allows us to find the
        “complementary” divisor D′ such that D + D′ is the intersection of C with
        the hyperplane in question. The algorithm is inspired by geometric consid-
        erations, as explained in the discussion preceding Theorem/Algorithm 3.10.
        The flipping algorithm is what allows us to pass to divisor classes; for ex-
        ample, flipping twice with respect to different hyperplanes replaces D with
        another divisor linearly equivalent to it.

     We conclude this introduction by pointing out the connection between our way
of representing divisors, and the way in Cantor’s algorithm for hyperelliptic curves;
it should be possible to say something similar for superelliptic and Cab curves. For
simplicity, we restrict to the case where k does not have characteristic 2, and so
consider a curve C : y 2 = f (x), where f (x) ∈ k[x] has degree 2g +1. Then a reduced
(effective) divisor D of degree d ≤ g is represented in Cantor’s algorithm by the
pair of polynomials (a(x), b(x)), with a(x) monic of degreeQd, b(x) of degree at most
d − 1, and b(x)2 ≡ f (x) (mod a(x)). If we factor a(x) = i (x − xi ), possibly with
some repeated xi , then D is the sum of the points (xi , b(xi )) on the curve. On the
other hand, in our representation, we choose a line bundle L and represent D by the
global sections of L vanishing at D. We can take L = OC (N P∞ ), for N ≥ 3g + 1,
where P∞ is the “point at infinity” with vP∞ (x) = 2 and vP∞ (y) = 2g + 1. To
simplify, we shall take N = 2m to be even. Then a basis for H 0 (C, L), arranged in
increasing order of pole at P∞ , is {1, x, x2 , . . . , xg , y, xg+1 , xy, xg+2 , x2 y, . . . , xm }.
Those sections that vanish at D are then of the form p(x)a(x) + q(x)(y − b(x)),
where deg p(x) ≤ m − d and deg q(x) ≤ m − 1 − g. Our working with these sections
using linear algebra can be thought of as performing polynomial operations on a(x)
and b(x), but with a bound on the degree of intermediate results. (Of course,
our algorithms also work in a more general setting.) An alternative way to deal
with the above is to consider the affine curve C − P0 ; its affine coordinate ring is
k[x, y]/(y 2 − f (x)) ∼
                      = k[x] ⊕ k[x]y, and the elements vanishing at D form an ideal
generated (even as a k[x] module) by the two elements a(x) and y − b(x).
      LINEAR ALGEBRA ALGORITHMS FOR DIVISORS ON AN ALGEBRAIC CURVE                     5


                                Acknowledgements
    I am grateful to K. Murty for posing to me the question of whether one could
work algorithmically with abelian varieties without using explicit equations. I would
also like to thank M. Thaddeus for very useful conversations on linear systems, in
particular, for his referring me to the article [L], and for his suggestion to think
                                                                                    ∗
primarily in terms of the space WD and sections of L, rather than its dual WD
and the projective embedding. My thanks go to C. Gasbarri for helpful comments
and references. I also gratefully acknowledge the support of the Clay Mathematics
Institute, which partially supported this research by funding me as a Clay Scholar
in the summer of 2000, and which supported my participation in the Clay Mathe-
matics Institute Introductory Workshop in Algorithmic Number Theory at MSRI
in August 2000. Finally, I would like to thank the mathematics department at
Columbia University for its hospitality at the time of the final revisions to this
manuscript.



 2. Embedding the symmetric power of a curve into a Grassmannian
    Let X be an algebraic variety over a field k; for the moment, we take k to
be algebraically closed. It is standard to try to embed X into projective space by
choosing a very ample line bundle L on X, and using L to get an embedding of X
into P(H 0 (X, L)). Here P(V ) is the projective space that parametrizes codimension
one subspaces of V . The standard embedding associates x ∈ X to the subspace
{s ∈ H 0 (X, L) | s vanishes at x}. More generally, one can try to embed X into a
Grassmannian variety, using a suitably positive rank d vector bundle E. We then
associate to x ∈ X the analogous subspace Wx of global sections of E vanishing
at x. Under suitable hypotheses, this gives us an embedding ϕ : X → Gd (V ),
where Gd (V ) parametrizes codimension d subspaces W of V . The map ϕ can be
composed with the Plücker embedding Gd (V ) → P(∧d V ) to obtain an embedding
of X into projective space. For practical purposes, this may be unhelpful, as the
dimension of ∧d V is dimd V -dimensional, which is significantly greater than dim V
once d ≥ 2. If moreover d increases  with dim V , the ngrowth
                                                             √     in the dimension can
be exponential; for example, 2n  n    grows  roughly as 4  /  πn  by  Stirling’s formula.
This suggests that we would be better off working with subspaces of V , and doing
explicit calculations using linear algebra, instead of passing to a possibly exponential
number of explicit projective coordinates via the Plücker embedding. The case that
interests us most is when X is the dth symmetric power Symd (C) of a curve C. We
shall embed Symd (C) into a certain Grassmannian without explicitly mentioning
vector bundles. The alert reader will see that we are essentially working with the
Quot scheme by hand (see Section 8.2 of [BLR]).
    Let g be the genus of C, take d ≥ 1, and fix once and for all a line bundle L
on C of degree N ≥ 2g + d ≥ 2g + 1. The Riemann-Roch theorem implies that the
space V = H 0 (L) = H 0 (C, L) has dimension N + 1 − g, and L gives an embedding
of C into P(V ) ∼= PN −g . In fact, a well-known theorem by Castelnuovo, Mattuck,
and Mumford states that this embedding of C is projectively normal, and there is
an even stronger theorem due to Fujita and Saint-Donat, which states that if in
fact N ≥ 2g + 2, then the ideal of C is generated by quadrics ([L], Section 1.1).
Now a point on Symd (C) can be identified with an effective divisor D = P mP P
                                                                               P
6                               KAMAL KHURI-MAKDISI

                      P
on C, of degree d =       mP ; we associate to D the subspace WD given by
(2.1)                      WD = H 0 (L − D) ⊂ V = H 0 (L).
Thus WD consists of the global sections s of L vanishing at D (i.e., s vanishes at
each P to order at least mP ). Note that we are freely abusing notation by often
failing to distinguish between line bundles and divisors, and by referring to tensor
operations on line bundles additively when it suits us; it would be more standard
to write WD = H 0 (L(−D)). Due to the condition on the degree N , the line bundle
L − D is nonspecial and has no base points, so WD has codimension d in V , and
we can recover D from WD . We summarize this discussion in the following lemma,
while noting incidentally that the argument also extends to the trivial case d = 0.
     Lemma 2.1 (Representation of divisors). Let C be an algebraic
                                                            P        curve of genus
g, and let L be a line bundle on C of degree N . Let D =       mP P be an effective
divisor on C of degree d (we allow D to be empty, in which case d = 0). Let
WD = H 0 (L − D) ⊂ H 0 (L) = V . Then if d ≤ N − 2g + 1, it follows that WD
has codimension d in V . If furthermore d ≤ N − 2g, then H 0 (L − D) has no base
points, in the sense that H 0 (L − D − P ) ( H 0 (L − D) for all points P of C. In
that case, the multiplicity mP can be recovered by noting that mP is the minimum
order to which any section s ∈ WD vanishes at P (viewing s as a global section of
L).
    Proof. This follows immediately from the Riemann-Roch theorem.
     Thus the map D 7→ WD is injective, and allows us to view Symd (C) as a subset
of Gd (V ). For N large compared to d and g, Theorem 8.2.8′ of [BLR] guarantees
that this injection of points is an embedding of varieties; we suspect that this holds
in our setting, but have not checked the matter further, as we do not need this
fact. Another way to view this map is via the embedding of C into P(V ) given by
our choice of L. Given a degree d divisor D on C, then its points span a certain
                             ∗
d-dimensional subspace WD       of the dual space V ∗ (now identifying points of P(V )
                               ∗
with nonzero elements of V up to multiplication of P      scalars). Assuming that the
multiplicities in D are all at most 1 (i.e., that D = i Pi for distinct Pi can be
                                           ∗
viewed as a reduced scheme), then WD         is precisely the annihilator of WD with
respect to the pairing between V and V ∗ . If D has some higher multiplicities, we
                                                                   ∗
can still make sense of this last statement by understanding WD      to be spanned not
only by P , but by the mP th infinitesimal neighborhood (i.e., osculating plane) of
                                                                           ∗
P on C (see [GH], pp. 248 and 264). We shall interchangeably use WD          to refer to
                                    ∗
the d-dimensional subspace of V and to the corresponding (d − 1)-plane in P(V ).
In this point of view, the fact that H 0 (L − D) has no base points means that the
points of D are linearly independent (even including multiplicity), and that the
          ∗
plane WD     intersects C precisely in the divisor D. This gives another way to see
the injectivity of the map D 7→ WD .
     So far, we have worked over an algebraically closed field. The above discussion
continues to hold if C and L are defined over an arbitrary perfect base field k,
provided that we restrict ourselves to divisors D rational over k. This means that
for all Galois automorphisms σ ∈ Gal(k/k), we have an equality of divisors (and
not just of divisor classes) σD = D. In that case, the vector spaces V and WD are
finite-dimensional over k, and all our work can be done over the field k. This is
quite convenient computationally, as we do not need to work with individual points
of D, which can themselves be defined over extensions of k. Still, our main goal in
        LINEAR ALGEBRA ALGORITHMS FOR DIVISORS ON AN ALGEBRAIC CURVE                                        7


working with Symd (C) is to descend to the Jacobian J of C. In that setting, the
above notion of rationality can fall somewhat short: a point of J(k) need not be
representable by a divisor rational over k, since we now only require equality of the
divisor classes D and σ(D). This problem arises only if C itself has no points defined
over k; in that case, the obstruction to lifting a point of J(k) to a divisor rational
over k lies in the Brauer group of k (see Remark 1.6 of [M]). We are primarily
interested in the case where k is a finite field (so the Brauer group is trivial), so
we shall henceforth ignore the above distinction between rationality questions on
the symmetric product and on the Jacobian. We merely remark that in working
with various spaces of sections of line bundles (such as H 0 (L − D)), we shall work
over the algebraic closure k when needed, and then deduce the desired results for
k. A typical example is the following lemma, which is a slight generalization of the
theorem by Castelnuovo, Mattuck, and Mumford cited above.
    Lemma 2.2 (“Multiplication”). Let C be a smooth, geometrically connected al-
gebraic curve of genus g over a perfect field k, and let L1 and L2 be two line bundles
on C (both defined over k), of degrees d1 and d2 . Assume that d1 , d2 ≥ 2g +1. Then
the canonical (multiplication) map
(2.2)                        µ : H 0 (L1 ) ⊗k H 0 (L2 ) → H 0 (L1 ⊗ L2 )
is surjective.
     Proof. We sketch a proof, adapting the exposition in Sections 1.3 and 1.4 of
[L], which treats the case L1 = L2 . It is enough to prove the result after extending
the base field from k to k, since base extension of linear maps defined over k does
not change the dimension of their kernels or images. This principle will be used
constantly in this article.
     We assume without loss of generality that d1 ≤ d2 , and begin with the following
exact sequence of vector bundles on C (using the notation of [L]):
                                                                  α
(2.3)                        0 → ML1 → H 0 (L1 ) ⊗ OC −
                                                      → L1 → 0.
Here α is the “evaluation” map, and ML1 = ker α. We have used the fact that L1 is
base point free, i.e., that it is generated by global sections. Tensoring (2.3) with L2
and taking cohomology reduces our problem to showing that H 1 (ML1 ⊗ L2 ) = 0.
To this end, choose r = d1 − 1 − g points P1 , . . . , Pr on C in general position (this
is where we really need to work over k). Then, by Lemma 1.4.1 and the beginning
of the proof of Theorem 1.2.7 of [L], we obtain the following exact sequence (where
we have temporarily lapsed back into writing line bundles multiplicatively):1
                               Xr
(2.4)              0 → L−11  (     Pi ) → ML1 → ⊕ri=1 OC (−Pi ) → 0.
                                    i=1
Tensoring this sequence with L2 and taking cohomology reduces our problem to
showing, first, that H 1 (L2 (−Pi )) = 0 for all i (as is clear
                                                              Pby   using Serre duality
                                                                r
and looking at degrees), and, second, that H 1 (L2 ⊗ L−1  1  (  i=1 Pi )) = 0. This last
     1 This is where we use the fact that d ≥ 2g + 1, so r ≥ g, and we can guarantee that
      P                                              1
L1 (− Pi ) not only has a two-dimensional space of global sections, but is also base point free for a
generic choice of points P1 , . . . Pr , because it is a generic line bundle of degree
                                                                                P      g+1. We then obtain
(2.4) by combining (2.3) with an analogous exact sequence for L1 (− Pi ), and using the snake
lemma. We also note that the analog of (2.3) allows us to deduce that L−1               Pi ) ∼
                                                                                     P
                                                                                 1 (         = ML1 (− P Pi ) .
This is known as the “base point free pencil trick”; for more details, refer to the exposition in [L]
and to [ACGH], pp. 126 and 151, particularly Exercise K.
8                                KAMAL KHURI-MAKDISI

                                                                 Pr
statement is equivalent to requiring H 0 (K ⊗ L−1    2 ⊗ L1 (−      i=1 Pi )) = 0, where
we write K for the canonical bundle on C. Since we have assumed that d2 ≥
d1 , we see that the line bundle L3 = K ⊗ L−1      2 ⊗ L1 has degree at most 2g − 2.
Therefore dim H 0 (L3 ) ≤ g, because we can embed H 0 (L3 ) into the g-dimensional
space H 0 (L3 (D)), where D is any effective divisor of degree 2g − 1 −P    deg L3 . Since
the r points P1 , . . . , Pr impose r ≥ g zeros, we obtain that H 0 (L3 (− ri=1 Pi )) = 0
for generic P1 , . . . , Pr , as desired.

    Our last result in this section is a converse of sorts to Lemma 2.2, since it
describes a kind of “division” of sections of line bundles. This relatively easy
lemma/algorithm is crucial to our results, perhaps even more so than the somewhat
deeper Lemma 2.2.

     Lemma/Algorithm 2.3 (“Division”). Let C be a curve as in Lemma 2.2. Let
L1 and L2 be line bundles (written multiplicatively in this lemma/algorithm), and
let D1 and D2 be effective divisors on C, where everything is defined over k. (We
allow D1 or D2 to be zero.) Assume that L2 (−D2 ) has no base points (over k);
for example, it is sufficient to have deg L2 − deg D2 ≥ 2g. Let µ : H 0 (L1 ) ⊗
H 0 (L2 ) → H 0 (L1 ⊗ L2 ) be the multiplication map, as before. Assume that we know
the subspaces H 0 ((L1 ⊗ L2 )(−D1 − D2 )) ⊂ H 0 (L1 ⊗ L2 ), and H 0 (L2 (−D2 )) ⊂
H 0 (L2 ). Then we can compute H 0 (L1 (−D1 )) to be the space
(2.5)
   {s ∈ H 0 (L1 ) | ∀t ∈ H 0 (L2 (−D2 )),   µ(s ⊗ t) ∈ H 0 ((L1 ⊗ L2 )(−D1 − D2 ))}.

Note that for computational purposes, it is enough to let t range only over a basis
for H 0 (L2 (−D2 )) (and not over the whole space) in equation (2.5).

    Proof. The fact that H 0 (L1 (−D1 )) is a subset of the space defined in (2.5) is
immediate. As for the reverse inclusion, it follows from the fact thatP  H 0 (L2 (−D2 ))
has noP base points. To see why, extend scalars to k, and write D1 = P mP P , and
D2 = P nP P , where only finitely many of the mP and nP are nonzero. For any
point P on C, base point freeness means that we can find t ∈ H 0 (L2 (−D2 )) which
(when viewed as a section of H 0 (L2 )) vanishes at P to order exactly nP . Thus, if
s ∈ H 0 (L1 ) satisfies the condition in equation (2.5), then µ(s ⊗ t) vanishes at P to
order at least mP + nP , from which we conclude that s vanishes at P to order at
least mP . Since P was arbitrary, we obtain that s ∈ H 0 (L1 (−D1 )), as desired.


     Remark 2.4. Lemma/Algorithm 2.3 works even if the output, H 0 (L1 (−D1 )),
fails to be base point free. The fact that our section s is required to vanish at D1
may well have severe consequences for the behavior of s at other points of C.

     Remark 2.5. In Remark 3.8 below, we shall see that actually calculating
H 0 (L1 ⊗ L2 ) as the image of µ, as in Lemma 2.2, can be done in O(δ 4 ) steps,
if the dimensions of the vector spaces involved are of the order of δ. (In our appli-
cations, δ is a small constant times g.) We caution the reader to avoid an overly
naive implementation of the calculation that would take time O(δ 5 ). We shall also
see in the same remark below that the operation in Lemma/Algorithm 2.3 can be
implemented in time O(δ 4 ).
      LINEAR ALGEBRA ALGORITHMS FOR DIVISORS ON AN ALGEBRAIC CURVE                    9


                        3. Basic algorithms on divisors
     As in Section 2, let C be a curve of genus g over a perfect field k, and fix a line
bundle L on C of large degree N , which will be at least 2g + 1, and typically some-
what larger. Throughout this section, except briefly in Theorem/Algorithm 3.14,
the letters D, D′ , and E will refer to effective divisors on C (that are rational over
k), of degrees d, d′ , and e.
     We represent an effective divisor D of degree d ≤ N − 2g by the codimension d
subspace WD = H 0 (L − D) of the vector space V = H 0 (L); alternatively, we can
                               ∗
work with its annihilator WD      ⊂ V ∗ , corresponding to the span of the points of D
(counting multiplicity) in the projective embedding of C into P(V ). In later sec-
tions, we give various choices of parameters that allow us to apply the algorithms of
this section to compute in the Jacobian of C. For ease of following the exposition in
this section, we advise the reader to keep in mind the application given in Section 4.
In that setting, g ≥ 1, and L will have the form 3L0 = OC (3D0 ) for D0 a divisor
of degree d0 ≥ 2g; there is some benefit in even assuming that d0 ≥ 2g + 1, as this
allows us to use either Theorem/Algorithm 3.6 or 3.13, whereas if we use d0 = 2g,
we can only use the latter Theorem/Algorithm. The reader should probably use
the value d0 = 2g + 1, whence N = 3d0 = 6g + 3. The values of d that will appear in
our application are d = d0 (= 2g + 1, say) and d = 2d0 (= 4g + 2); an effective divisor
D of degree d0 will be called small, and a divisor of degree 2d0 will be called large.
A small divisor D will describe a point on the Jacobian J corresponding to the line
bundle OC (D − D0 ), and a large divisor D′ will usually arise as an effective divisor
equivalent to 3D0 − D for some small divisor D. Nonetheless, we carry through our
analysis for more general values of N and d, subject to certain inequalities. This
allows for different versions of our algorithms, depending on which parameters and
design choices are most suitable in a given context.
     We begin by identifying the subspaces WD ∩ WE and WD + WE , in terms of
                                                                ∗
divisors related to D and E. These subspaces are dual to WD       + WE∗ and WD ∗
                                                                                 ∩ WE∗ .
From either point of view (either thinking of WD as a space of sections which vanish
                ∗
at D, or of WD    as the span of the points of D), it is very plausible that these new
subspaces should correspond to the divisors D ∪ E and D ∩ E, at least if all the
multiplicities of points are at most 1. The content of Proposition/Algorithm 3.2 is
that a result of this kind holds in general, provided we make the following definition.
                                P                  P
     Definition 3.1. If D = mP P and E = nP P are two (effective) divisors,
then we define
                       X                                      X
(3.1)      D∪E =          max(mP , nP )P,            D∩E =        min(mP , nP )P.
Note that if D and E are both defined over k, then so are D ∪ E and D ∩ E.

     Proposition/Algorithm 3.2 (Union and intersection). Given D and E as
                                                                  ∗
in Definition 3.1, then in all cases WD ∩ WE = WD∪E (or, dually, WD  + WE∗ =
   ∗
WD∪E ). If furthermore deg(D ∪ E) ≤ N − 2g, then we can recover D ∪ E from
                                                                   ∗
the subspace WD∪E , and we also obtain WD + WE = WD∩E (dually, WD    ∩ WE∗ =
   ∗
WD∩E ).
    Proof. The first statement is trivial, as we are requiring sections to vanish
at P simultaneously to order at least mP and at least nP . The condition on
the degree of D ∪ E is to ensure that H 0 (L − (D ∪ E)) is base point free by
Lemma 2.1, so that we can recover D ∪ E. Moreover, codim WD∪E = deg(D ∪ E)
10                             KAMAL KHURI-MAKDISI


in that case. As for WD∩E , we always have WD + WE ⊂ WD∩E . If we know that
deg(D ∪ E) ≤ N − 2g, then we can conclude equality by comparing dimensions,
since codim(WD + WE ) = codim WD + codim WE − codim(WD ∩ WE ), and an
analogous equality holds for the degrees of the corresponding divisors.

     Remark 3.3. In the context of Section 4, Proposition/Algorithm 3.2 allows us
to find the union and intersection of two small divisors D and E, since in that case
the degree of D ∪ E cannot exceed d + e = 2d0 = N − d0 ≤ N − 2g. In case these
divisors are disjoint, as can be measured by looking at their intersection, this gives
a simple way to compute the sum of these divisors. We formalize this below, and
throw in an easy algorithm to see if one divisor is contained in the other. By this
we mean the following definition:
                   X                X
(3.2)        D=        mP P ⊂ E =       nP P ⇐⇒ for all P, mP ≤ nP .

    Proposition/Algorithm 3.4 (Disjointness and inclusion). Given divisors D
and E, of degrees d and e respectively, then:
    1. If d+e ≤ N −2g, then we can test if D ∩E = ∅ by checking if WD +WE = V
                         ∗
       (alternatively, WD  ∩WE∗ = 0). In that case, D +E = D ∪E can be calculated
       as WD+E = WD ∩ WE , by Proposition/Algorithm 3.2. An alternative to
       checking if WD + WE = V is to simply compute WD ∩ WE and to see if the
       intersection has codimension d + e.
    2. If d, e ≤ N − 2g, then we can test if D ⊂ E (in the sense of (3.2)) by testing
                                         ∗
       whether WE ⊂ WD (dually, if WD       ⊂ WE∗ ).

     Remark 3.5. The linear algebra calculations to which we reduce our problem
in our algorithms can be tested easily using standard techniques of Gaussian elimi-
nation. This involves choosing a basis for V (hence an isomorphism V ∼     = k N +1−g ),
and expressing everything in terms of the resulting coordinates on V . A subspace
such as WD can then be represented in terms of a basis for WD , expressed in terms
                                                                ∗
of the coordinates on V . Alternatively, one can work with WD     instead of WD , since
                      ∗
for small divisors, WD has smaller dimension. The drawback to this is that using
   ∗
WD   appears to be less efficient for our later algorithms, which involve the multipli-
cation map µ. We also refer the reader to a side observation in Remark 3.8 for an
idea of how to test whether D and E are disjoint even if d + e > N − 2g; however,
that method requires the slightly stronger hypothesis that d, e ≤ N − 2g − 1. Alter-
natively, one can replace L with a line bundle of higher degree, as in the discussion
at the end of Section 5.
    We now describe an algorithm to add two divisors in general, whether or not
they are disjoint. We need to assume knowledge of the multiplication map
(3.3)                µ : V ⊗ V = H 0 (L) ⊗k H 0 (L) → H 0 (2L).
In the case that interests us, N ≥ 2g + 2. Then knowledge of µ is tantamount
to knowing the quadratic polynomials that define C in the projective embedding
given by L, as mentioned just before equation (2.1). The map µ can be represented
explicitly in terms of bases for V and for H 0 (2L). The technique in the theorem
below is fundamental, and plays a role in all the remaining algorithms of this
article. We give a geometric interpretation of this technique after the proof of
Proposition/Algorithm 3.9 below. In Theorem/Algorithm 3.13 below, we give a
        LINEAR ALGEBRA ALGORITHMS FOR DIVISORS ON AN ALGEBRAIC CURVE                  11


second algorithm for addition of divisors, using some similar ideas. The other
algorithm works in a slightly more general context than the following algorithm,
but the first algorithm is perhaps simpler to explain.
     Theorem/Algorithm 3.6 (Addition of divisors (first method)). Let D and E
satisfy d, e ≤ N − 2g − 1. Then we can compute WD+E in the following steps:
     1. Restricting µ to the subspace WD ⊗ WE = H 0 (L − D) ⊗ H 0 (L − E) of
        V ⊗ V , we obtain from Lemma 2.2 that µ(WD ⊗ WE ) = H 0 (2L − D − E).
        The subspace H 0 (2L − D − E) of H 0 (2L) can be computed as the span of
        µ(si ⊗ s′j ), as si and s′j range over bases for WD and WE respectively.
     2. Using Lemma/Algorithm 2.3, we compute
(3.4)         WD+E = {s ∈ V | ∀t ∈ V,       µ(s ⊗ t) ∈ H 0 (2L − D − E)}.
         Recall that one only needs to let t range over a basis for V .
     Proof. In order to apply Lemma/Algorithm 2.3, we need to observe that
H 0 (L) is base point free. This holds by Lemma 2.1, since our assumptions imply
that N ≥ 2g + 1 + d ≥ 2g.

     Remark 3.7. In order for knowledge of WD+E to allow us to uniquely recover
D + E, we need to know that d + e ≤ N − 2g; in the setting of Section 4, for
example, this would require both D and E to be small (and d0 ≥ 2g + 1), even
though the above algorithm correctly calculates WD+E in case one of the divisors
is small, and the other large. Nonetheless, for use in Theorems/Algorithms 4.1
and 5.5 and elsewhere, we have presented the above algorithm in the general case,
even if WD+E does not uniquely determine D + E. We note as an aside that this
last case happens precisely when H 0 (L − D − E) has base points, and in that case
the inclusion
(3.5)              µ(H 0 (L − D − E) ⊗ H 0 (L)) ⊂ H 0 (2L − D − E).
will be strict, since H 0 (2L − D − E) will never have base points, by Lemma 2.1.
(This of course does not affect the validity of our proof; in the easy half of the proof
of Lemma/Algorithm 2.3, we only need the inclusion in equation (3.5) to obtain
that WD+E ⊂ {s as above}.)

     Remark 3.8. We discuss some practical issues in implementing the above al-
gorithm, beyond the fact that Theorem/Algorithm 3.6 settles the theoretical issue
of computing WD+E . We also discuss the running time of the algorithm. Let the
dimensions of the vector spaces involved in the calculation be of the order of δ
(this is approximately dim V = N + 1 − g, which is O(g) for all our applications).
Then an overly naive implementation of the algorithm as stated above takes time
O(δ 5 ), but a little care brings this down to O(δ 4 ). We can use some randomness
to make the algorithm slightly faster, but still taking O(δ 4 ) steps. (We remind the
reader that we count an operation in the field k as a single step, taking one unit
of time.) We note that our second algorithm below, Theorem/Algorithm 3.13, also
takes time O(δ 4 ).
     We first discuss why the naive implementation of Theorem/Algorithm 3.6 runs
in time O(δ 5 ), and how to reduce this time to O(δ 4 ). We assume that µ is
implemented in terms of fixing a basis {ti } for V , and storing all the products
vij = µ(ti ⊗ tj ) ∈ H 0 (2L). Moreover, a subspace WD is represented by choosing
12                                  KAMAL KHURI-MAKDISI


a basis, and writing all the basis elements in terms of the ti . Then it takes O(δ 3 )
operations to calculate each individual µ(si ⊗ s′j ), as si and s′j range over bases for
WD and WE . Since there are O(δ 2 ) such pairs (si , s′j ), it seems that we will need
O(δ 5 ) steps merely to write down a spanning set for H 0 (2L − D − E), viewed as
a subspace of the O(δ)-dimensional space H 0 (2L). However, we can proceed more
quickly, at the expense of using more memory, as follows: first calculate (and store)
each product wij = µ(si ⊗ tj ), as si ranges over a basis for WD , and tj ranges over
the standard basis for V . This takes only O(δ 4 ) steps, since each individual multi-
plication µ(si ⊗ tj ) now needs only O(δ 2 ) operations, as it involves only the vi′ j for
a fixed j and varying i′ . Now if E = 0, we are already done; more generally, we use
the wij to assemble all the products µ(si ⊗ s′j ) in a further O(δ 4 ) steps. Since these
products will virtually always be linearly dependent, we should then use Gaussian
elimination to reduce these products to a basis for H 0 (2L − D − E). This takes
O(δ 4 ) operations, since we have O(δ 2 ) vectors to reduce inside the O(δ)-dimensional
space H 0 (2L).2
     All of this takes some time. So in practice (at least when d + e ≤ N − 2g),
one should rely on the fact that the divisors D and E are likely to be disjoint, and
simply compute WD ∩ WE , as mentioned in Proposition/Algorithm 3.4. This only
takes O(δ 3 ) operations. If the intersection has the right codimension d + e, which
should happen rather often, then we immediately obtain WD+E as this intersection.
We note that in the undesirable case d + e > N − 2g, it does not seem to be
worth the computational effort to check if D and E are disjoint; one might as well
use Theorem/Algorithm 3.6 directly. (Here is one idea of how one can adapt our
algorithms to check that D and E are disjoint, even if d+ e > N − 2g: first calculate
H 0 (2L − D) = µ(WD ⊗ V ), and similarly H 0 (2L − E); this works, and takes time
O(δ 4 ) as before. Then find the intersection H 0 (2L − D) ∩ H 0 (2L − E) inside the
larger ambient space H 0 (2L) instead of H 0 (L). This amounts to using 2N instead
of N , which allows us to proceed as in Proposition/Algorithm 3.4, since d + e is
now less than 2N − 2g.)
     Coming back to the issue of calculating µ(WD ⊗ WE ), we note that we can
also try to avoid calculating all O(δ 2 ) products µ(si ⊗ s′j ). Instead, we randomly
choose O(δ) pairs of the form (s, s′ ), where s ∈ WD and s′ ∈ WE are random
(nonzero) elements. In that case, the resulting products µ(s ⊗ s′ ) are likely to
already span H 0 (2L − D − E), especially if we take, say, twice as many pairs (s, s′ )
as the dimension of H 0 (2L − D − E). With high probability, this reduces the time
we spend on finding µ(WD ⊗ WE ), but it still involves O(δ 4 ) operations, since one
must calculate the µ(s ⊗ s′ ). On the other hand, this reduces the time spent on
Gaussian elimination to O(δ 3 ), but without an assurance of success as we have not
necessarily used a full spanning set for H 0 (2L − D − E).
     As for the “division” calculation in step 2 of Theorem/Algorithm 3.6, it can be
done in O(δ 4 ) operations as follows: first, find a matrix M , representing a linear
transformation from H 0 (2L) to k d+e , whose kernel is precisely H 0 (2L − D − E).
This amounts to finding a basis of the annihilator H 0 (2L − D − E)∗ ⊂ H 0 (2L)∗ ,
and can be done in time at most O(δ 3 ) (even O(δ 2 ), if the basis for H 0 (2L − D − E)

     2 It would be interesting to try to use the fact that for fixed i and varying j (or vice-versa),

the products µ(si ⊗s′j ) are known to be linearly independent before we start Gaussian elimination.
Still, there are advantages to obtaining a basis for H 0 (2L − D − E) in echelon form, once we invoke
Lemma/Algorithm 2.3.
        LINEAR ALGEBRA ALGORITHMS FOR DIVISORS ON AN ALGEBRAIC CURVE                           13


is already in echelon form). Recall that we have on hand all the products vij =
     ⊗ tj ) ∈ H 0 (2L), where theP
µ(ti P                                     ti are a basis for V . We now need to solve for
s = i xi ti such that for all j, i xi M (vij ) = (0, . . . , 0) ∈ k d+e . Computing the
various M (vij ) takes O(δ 4 ) steps, and the resulting Gaussian elimination to solve
for the tuples (. . . , xi , . . . ) representing s takes O(δ 4 ) operations, being a system
of O(δ 2 ) equations in O(δ) variables. We point out that we will later still be
able to perform similar calculations (inspired by Lemma/Algorithm 2.3) in O(δ 4 )
operations, even if we no longer have t ranging over all of V . This is necessary for
equation (3.7) in Proposition/Algorithm 3.9, as well as Theorems/Algorithms 3.10,
                                                                ′
3.13, and 3.14. The idea is that we need to compute vij           = µ(ti ⊗ t′j ) for ti as before,
            ′                                                                           ′
but with tj ranging over a basis for some suitable subspace of V . Each vij                can be
                                                              2
computed from the existing collection of vij in O(δ ) operations, so it takes time
                               ′
O(δ 4 ) to assemble the vij       , and the calculation proceeds as before.
    Our next algorithm is a straightforward P
                                            illustration of thePideas in Theo-
rem/Algorithm 3.6. Given two divisors D =      mP P and E =      nP P , we may
wish to calculate the divisor
                                X
(3.6)                     E\D =    max(0, nP − mP )P.
In case the multiplicities are at most 1, then this is the usual operation on sets of
points. If D ⊂ E, this is just subtraction of divisors.
     Proposition/Algorithm 3.9 (Set subtraction). Given D and E, with d ≤
N − 2g and e ≤ N − 2g − 1, we can calculate WE\D as follows: First, calculate
H 0 (2L − E) = µ(WE ⊗ V ). Then compute
(3.7)           WE\D = {s ∈ V | ∀t ∈ WD ,           µ(s ⊗ t) ∈ H 0 (2L − E)}.
    Proof. Lemma 2.2 gives us the surjectivity of µ : H 0 (L − E) ⊗ H 0 (L) →
  0
H (2L − E). As for (3.7), it follows from a modification of the argument in
Lemma/Algorithm 2.3, since H 0 (L − D) has no base points. Note again that the
computation on (3.7) can be done effectively by letting t range only over a basis
for WD .
     We now come to the most important basic algorithm in this section. It is close
to Theorem/Algorithm 3.6 and Proposition/Algorithm 3.9, but we shall first pause
to describe what the algorithm is doing geometrically. Our discussion will also shed
light on Theorem/Algorithm 3.6. The geometric picture is best understood in terms
of the projective embedding of C into P(V ) given by L, and in terms of ideals of
the graded projective coordinate ring of P(V ). To this end, let A = Sym∗ V be
this projective coordinate ring; A is the symmetric algebra on V , and an element
of V is a linear (degree one) polynomial whose vanishing set defines a hyperplane
in P(V ). The curve C is defined by a homogeneous ideal IC , which is generated
in our application by elements of degree two, and these elements can more or less
be identified with the kernel of µ : V ⊗ V → H 0 (2L). (The quotient A/IC is the
projective coordinate ring of C, and µ is just multiplication in this quotient.) Given
                                                          ∗
a divisor D and its associated subspaces WD and WD          , we shall abuse notation
                   ∗
and also write WD for the corresponding plane in P(V ), as described just after
Lemma 2.1. In that case, we write IW for the ideal defining this plane; IW is then
                                                                             ∗
generated by WD , which consists of the linear functions vanishing on WD       . As we
                          ∗
have seen before, D = WD ∩ C. In terms of ideals, this means that D is defined by
the ideal ID = IW + IC = WD A + IC .
14                             KAMAL KHURI-MAKDISI


    Now our next algorithm implements the following operation: given a section
f ∈ WD , we know that f (viewed as a section of L) vanishes at a divisor of
the form E = D + D′ belonging to the equivalence class of L. We then wish
to find WD′ , essentially by the same method as in Proposition/Algorithm 3.9.
Geometrically, the zero set of f is a hyperplane H passing through D, and its ideal
IH is generated by f . Then the divisor E is the intersection H ∩ C, and is defined
by IE = IH + IC = f A + IC . As a zero-dimensional scheme, we then obtain that
D′ = E \ D should be defined by
(3.8)    ID′ = (IE : ID ) = {a ∈ A | aID ⊂ IE } = {a ∈ A | aWD ⊂ f A + IC }.
Namely, functions should vanish on D′ if and only if when we multiply them by a
function vanishing on D, we obtain a function vanishing on E = D ∩ D′ = H ∩ C.
This fact is not so immediate if D and E have multiplicities greater than 1; it is
essential, for example, that our divisors lie on a fixed curve, so that every extra
order of vanishing at a point P imposes exactly one more condition on homogeneous
polynomial functions, provided that the degree of E is not too large. At any rate,
we are not interested in the ideal defining D′ itself, but rather in the plane WD  ∗
                                                                                     ′
                ′
spanned by D . Dually, we only wish to determine WD , which consists of the
                                                              ′

linear functions vanishing on D′ . Thus we only seem to need to find the degree
one elements of ID′ . Using (3.8), this leads us to the calculation that we present
below in Theorem/Algorithm 3.10. (Multiplication of linear functions and taking
the quotient by the quadratic elements of IC is exactly the map µ.) Again, the fact
that we can content ourselves with the degree one elements of ID′ is not so trivial:
in general, the vanishing set of a homogeneous ideal on projective space depends
only on the saturation of that ideal (exercise II.5.10 of [Ha]; note that step 2 in
Theorem/Algorithm 3.6 is effectively computing a saturation). Now knowing the
degree one elements of a saturation can in principle involve elements of arbitrarily
high degree in the ideal. To do this algorithmically in general would probably
involve Gröbner basis techniques, which will typically be slower than our methods —
the Gröbner basis calculations can take exponential time in the worst case (although
they are efficient for “most” calculations), and even their average case behavior is
likely to be slower than our linear algebra calculations. The point of our techniques
is that we can use them to justify the geometric reasoning in the above heuristic
argument. We therefore (finally) present the following result.
    Theorem/Algorithm 3.10 (Flipping algorithm). Let D be an effective divi-
sor of degree d ≤ N − 2g. Take a nonzero element f ∈ WD , and write the divisor
of f (viewed as a section of L) as
(3.9)                            (f ) = E = D + D′ .
Thus d′ = deg D′ = N − d, and D′ belongs to the divisor class of L − D. Then we
can compute WD′ in the following steps:
    1. Calculate H 0 (2L − D − D′ ) = µ(f ⊗ H 0 (L)).
    2. Compute WD′ = {s ∈ H 0 (L) | for all t in (a basis for) WD , µ(s ⊗ t) ∈
       H 0 (2L − D − D′ )}.
Note that if furthermore d ≥ 2g, then knowledge of WD′ determines D′ uniquely,
by Lemma 2.1.
     Proof. The identity in the first step (which amounts to computing the image
of the degree two elements of f A in the quotient A/IC ) does not need Lemma 2.2,
      LINEAR ALGEBRA ALGORITHMS FOR DIVISORS ON AN ALGEBRAIC CURVE                   15


but turns out to be much simpler. In fact, multiplication by f is a bijection between
H 0 (L) and H 0 (2L − D − D′ ), the inverse being division by f (which does not
introduce any poles!). Then the second step above (which is the degree one part of
the left hand side of (3.8), whose computation involves some degree two elements
on the right hand side) follows from Lemma/Algorithm 2.3, since H 0 (L − D) has
no base points.

    Remark 3.11. In the setting of our application in Section 4, we have L =
OC (3D0 ), N = 3d0 , and d0 ≥ 2g. The above algorithm then allows us to go
from a divisor D (which may be small or large, corresponding to d = d0 or 2d0
respectively) to a complementary divisor D′ (which is then respectively large or
small), such that D + D′ is linearly equivalent to 3D0 . This is reminiscent of the
theory behind the Weierstrass embedding of an elliptic curve via a cubic equation,
except that we are contenting ourselves with quadratic equations and must therefore
use a more positive line bundle for our embedding of C. In Section 5, we go
through analogs of our construction using smaller divisors (e.g., d0 = g + 1, and
N = deg L = 3g + 3), working instead with “higher degree equations,” roughly in
the sense of multiplications V ⊗ V ⊗ . . . ⊗ V → H 0 (nL).

    Remark 3.12. Theorem/Algorithm 3.10 also runs in time O(δ 4 ), in the nota-
tion of Remark 3.8. This is because the “multiplication” involved in computing
µ(f ⊗ V ) takes O(δ 3 ) steps, including reducing the basis {µ(f ⊗ ti )} for H 0 (2L −
D − D′ ) to echelon form. (We already know that the vectors {µ(f ⊗ ti )} are linearly
independent.) It then takes another O(δ 4 ) steps to implement the second “division”
step of Theorem/Algorithm 3.10, by the same discussion as in Remark 3.8.
     Now that we have discussed the flipping algorithm, we use a slight variant of
it to give a second algorithm to compute the sum of two divisors. It is not clear
whether this is more efficient than Theorem/Algorithm 3.6, as the new algorithm
still requires time O(δ 4 ), although it involves slightly different linear algebra. On
the other hand, it has slightly weaker hypotheses, and can work in the setting of
Section 4 with d0 = 2g.
    Theorem/Algorithm 3.13 (Addition of divisors (second method)). Let D and
E be two divisors with 2g ≤ d ≤ N − 2g. (We do not make any assumptions on e.)
Then we can compute WD+E = H 0 (L − D − E) as follows:
    1. Choose a nonzero f ∈ WD , whose divisor (viewing f as a section of L) is
       (f ) = D + D′ ; proceed as in Theorem/Algorithm 3.10 to compute WD′ .
    2. Also compute H 0 (2L − D − D′ − E) = µ(f ⊗ WE ).
    3. Now compute WD+E = {s ∈ V | ∀t ∈ WD′ , µ(s ⊗ t) ∈ H 0 (2L − D − D′ −
       E)}.
    Proof. This is an almost verbatim adaptation of the argument in Theo-
rem/Algorithm 3.10. The hypothesis on d ensures that WD and WD′ have no
base points. Note that, as in Theorem/Algorithm 3.6, we cannot hope to recover
the actual divisor D + E unless d + e ≤ N − 2g.
    We conclude this section with an algorithm which tells whether a given codi-
mension d subspace W ⊂ V actually is of the form WD for a divisor D. In other
words, given a point on the Grassmannian Gd (V ), we wish to identify whether or
not it lies in the image of Symd (C). Since we have not explicitly written down
16                             KAMAL KHURI-MAKDISI


equations describing this subvariety of the Grassmannian, we have to do something
cleverer than checking whether certain polynomial functions vanish. The answer
turns out to be relatively straightforward, using Theorem/Algorithm 3.10. Once
again, the algorithm takes time O(δ 4 ).
      Theorem/Algorithm 3.14 (Membership test). Let W ⊂ V = H 0 (L) have
codimension d, where 2g ≤ d ≤ N − 2g. (In particular, N ≥ 4g.) Choose any
nonzero f ∈ W , and compute W ′ in the same way as in Theorem/Algorithm 3.10;
i.e.,
(3.10)            W ′ = {s ∈ V | ∀t ∈ W,    µ(s ⊗ t) ∈ µ(f ⊗ V )}.
Then W is of the form WD for some (uniquely determined) D if and only if the
codimension of W ′ in V is N − d, or equivalently if dim W ′ = d + 1 − g.
    Proof. If W is of the form WD , then the resulting W ′ is equal to the space
WD′ in Theorem/Algorithm 3.10, where the degree of D′ is d′ = N − d. Then
L − D′ has degree
              P       d, and the result follows. Conversely, given any W , define a
divisor D =      mP P by the property that for each P , mP is the minimum order
to which any nonzero section s ∈ W vanishes at P (viewing s as a section of L). In
other words, D is the largest possible divisor for which W ⊂ WD , and D is the only
possible candidate for a divisor which might give rise to W . (One easily checks that
D is defined over k, even if the individual points are only defined over k, but we do
not actually need this fact for our proof, and give our proof by working entirely over
k. As usual, there is no problem in extending scalars from k to k for the proof.)
Note that we do not yet know whether deg D = d, in contrast to our previous
notational convention. We do know, however, that deg D ≤ d, since otherwise,
by Lemma 2.1, the codimension of WD would be at least d + 1, contradicting the
inclusion W ⊂ WD . We see in fact that deg D = codim WD ≤ d = codim W , and
that W = WD if and only if deg D = d.
    Now our choice of f gives us in particular a nonzero element of WD , so the
divisor of f is of the form D + D′ , where
(3.11)                  d′ = deg D′ = N − deg D ≥ N − d.
The same reasoning as in Lemma/Algorithm 2.3 then shows us that W ′ = WD′ (the
main point is that µ(f ⊗V ) = H 0 (2L−D −D′ ), just as in Theorem/Algorithm 3.10;
on the other hand, for each P , we can already find a section t ∈ W that vanishes
at P precisely to the minimum possible order mP ). Now suppose that deg D′ were
different from N − d. In that case, equation (3.11) would imply that d′ ≥ N − d + 1.
Let E be the sum of any N − d + 1 points of D′ ; then the codimension of WD′
in V would be greater or equal to the codimension of WE , which we know to be
N − d + 1 (we are using the fact that N − d + 1 ≤ N − 2g + 1, so as to apply
Lemma 2.1). This would contradict our assumption on the codimension of WD′ ;
hence we conclude that deg D′ = N − d after all, and hence by (3.11) we conclude
that deg D = d and that W = WD , as desired.

4. The large model: Weierstrass-style algorithms on divisor classes and
                            on the Jacobian
    We now describe a way to work with divisor classes on C, which is inspired by
the usual geometric definition of the group law on an elliptic curve represented by
the plane cubic equation y 2 = x3 + ax + b. Actually, in many cases, we give two
         LINEAR ALGEBRA ALGORITHMS FOR DIVISORS ON AN ALGEBRAIC CURVE                17


algorithms for the basic operations, the first of which is straightforward and elegant,
and the second of which is somewhat more efficient, and is given to illustrate various
techniques. In Section 5, we give slightly faster algorithms, using a somewhat more
compact representation of divisor classes. In all cases, the various algorithms require
O(δ 4 ) operations in the field k, where δ = dim V is approximately 5g. The main
improvement in speed in Section 5 comes from our bringing δ down to a smaller
multiple of g there. Thus the algorithms in Section 5 supersede the ones here, at
the expense of elegance. The basic structure of all the algorithms is roughly the
same in all settings. We refer to the setup in this section as the large model.
     We write D ∼ E to denote that the divisors D and E are linearly equivalent,
and we denote the equivalence class of D by [D]. We keep the notation of Section 3,
and specialize the situation to our application as follows. Take an effective divisor
D0 of degree d0 ≥ 2g (or 2g + 1, if we wish to repeatedly use Theorem/Algorithm
3.6 instead of 3.13). Fix the ambient line bundle L = OC (3D0 ); thus N = 3d0 ≥ 6g.
Not surprisingly, we also assume that g ≥ 1 (but everything works with g = 0 and
d0 ≥ 1, if one is desperate or perverse enough to use these algorithms in that case).
We note that it may be tricky to find D0 of a specific degree, unless the curve C
contains one or more explicitly known rational points. In the best case, d0 = 2g,
and the dimension of the space V is δ = N + 1 − g = 5g + 1.
     An element of the Jacobian of C is a linear equivalence class of degree zero
divisors; these can all be obtained as classes of the form [D − D0 ], where D is
an effective divisor of degree d0 , called a small divisor. Given such a divisor, it
corresponds to the element xD of the Jacobian, given by

(4.1)         xD = [D − D0 ],    which is represented by the subspace WD ⊂ V.

(Thus, if d0 = 2g, then WD is a (3g + 1)-dimensional subspace of V .) We shall also
occasionally make use of large divisors, namely, divisors of degree 2d0 , for intermedi-
ate results in computations. We have already addressed in Theorem/Algorithm 3.14
the question of how to test whether a subspace W ⊂ V actually corresponds to an
element of the Jacobian. We now turn to the question of deciding when two such
subspaces, of the form WD and WE , represent the same element of the Jacobian.
This amounts to testing whether the divisors D and E are linearly equivalent.

    Theorem/Algorithm 4.1 (Equality of divisor classes). Let D and E be di-
visors of the same degree d ≤ N − 2g; typically, they will be either both small,
or both large divisors, represented by WD and WE . Choose any nonzero section
f ∈ WD , whose divisor (viewing f as a section of L) is (f ) = D + D′ ∼ L ∼ 3D0 .
Then compute WD′ +E in one of the following two ways:
        • Use Theorem/Algorithm 3.10 to compute the space WD′ , and then compute
          WD′ +E by Theorem/Algorithm 3.6 or 3.13. This is less efficient but easier to
          explain than the method proposed below. However, this first method further
          requires the assumption that 2g + 1 ≤ d ≤ N − 2g − 1, in case we use
          Theorem/Algorithm 3.6. If we use Theorem/Algorithm 3.13 instead, then
          we can weaken the assumption to 2g ≤ d ≤ N − 2g.
        • Alternatively, adapt the method of Theorem/Algorithm 3.13, without explic-
          itly calculating WD′ . Namely, calculate H 0 (2L − D − D′ − E) = µ(f ⊗ WE ),
          and then obtain WD′ +E = {s ∈ V | ∀t ∈ WD , µ(s ⊗ t) ∈ H 0 (2L − D −
          D′ − E)}.
18                             KAMAL KHURI-MAKDISI


Then, in either case, E ∼ D (i.e., [E] = [D], meaning xE = xD on the Jacobian), if
and only if the space WD′ +E is not zero, in which case it must be one-dimensional.
    Proof. The second method to calculate WD′ +E works by the same reasoning
as in the proof of Theorem/Algorithm 3.13. Now if there exists a nonzero s ∈
WD′ +E , then its divisor of zeros (s) (viewing s as a section of L) is an effective
divisor of degree N which contains D′ + E. By comparing degrees, we see that
D′ + E = (s). However, (s) and (f ) are linearly equivalent (both belong to the
class of L), from which we obtain E ∼ D. Conversely, if we     have0 E ∼ D, then
D′ +E ∼ L, and it follows that WD′ +E = H 0 OC (L−D′ −E) ∼     = H (OC ) = k.

    Remark 4.2. In the first method above, instead of using Theorem/Algorithm
3.6 or 3.13 to compute WD′ +E , we can choose the section f randomly, in which
there is a high probability that the divisors D′ and E are disjoint. In that case,
we simply check if there are any nonzero elements in WD′ ∩ WE = WD′ +E . As
mentioned in Remark 3.8, it may not be worth our while to test whether D′ and E
are disjoint; however, if the intersection is zero, then we can at least immediately
conclude that xE 6= xD , which saves a good amount of time. Another point to
consider is that if we wish to test the equality of many different classes [E] against
[D] by the first method, we should probably compute WD′ just once, instead of
choosing a random f each time. We note incidentally that the space WD′ +E that
we compute has codimension less than the degree of D′ + E, a fact that follows
immediately from the fact that WD′ +E is either zero or one-dimensional. We refer
the reader to Remark 3.7 for some further discussion.
     We now describe the main building block in our algorithms to effectively com-
pute in the Jacobian of C. This algorithm is analogous to the main geometric
construction on the Weierstrass model of an elliptic curve in the plane. Namely,
given two points P1 , P2 on the elliptic curve, we draw the line through them and find
its third point of intersection Q with the curve. This means that [Q] = −([P1 ]+[P2 ])
in the group law on the elliptic curve. We generalize this to the case of divisors of
degree d0 on our curve C.
    Proposition/Algorithm 4.3 (“Addflip”). Consider two subspaces WD1 , WD2
associated to two small divisors D1 , D2 on C, corresponding to the classes xD1 , xD2
on the Jacobian. The following algorithm then computes the subspace WE associated
to a divisor E such that xE = −(xD1 + xD2 ) (i.e., xD1 + xD2 + xE = 0):
    1. First compute WD1 +D2 , either by Theorem/Algorithm 3.6 or 3.13, or if
       possible by part 1 of Proposition/Algorithm 3.4.
    2. Now apply Theorem/Algorithm 3.10 to obtain the space WE corresponding
       to a “flip” E of D1 + D2 , where D1 + D2 + E ∼ 3D0 .
     Proof. Immediate. Note that step 1 is analogous to drawing the line through
two points on a Weierstrass model elliptic curve in the plane, and step 2 is analogous
to finding the third point on the intersection of the elliptic curve with the line. Also
note that in step 1, our use of Theorem/Algorithm 3.6 or 3.13 means that we do
not need to give special treatment to the case where D1 = D2 . In the Weierstrass
model, this would mean that our line through a double point is automatically
calculated as the appropriate tangent line. It is however simpler in the Weierstrass
model to find the line through two distinct points. The analogous statement in
our situation is: if we know beforehand that D1 and D2 are disjoint, then we
      LINEAR ALGEBRA ALGORITHMS FOR DIVISORS ON AN ALGEBRAIC CURVE                 19


can avoid using the more complicated theorems/algorithms, and instead simply
calculate WD1 +D2 = WD1 ∩ WD2 as in Proposition/Algorithm 3.4. This will save
a lot of time. In practice, the divisors D1 and D2 are likely to be disjoint, so one
should first calculate the intersection, and only use the more complicated algorithms
for adding divisors in case the codimension of WD1 ∩ WD2 is not 2d0 .
     Now that we have implemented the “addflip” operation f (x1 , x2 ) = −(x1 + x2 )
on the Jacobian of C, we can describe algorithms for all the group operations. We
begin with negation. Given a small divisor D, we seek E such that xE = −xD ,
or in other words D + E ∼ 2D0 . This can be done in a straightforward way, but
we give a slight modification which uses vector spaces of smaller dimension. This
will make the negation algorithm more efficient, a point especially worth noting,
since Theorem/Algorithm 4.5 (which adds two points on the Jacobian), involves
a negation. Similar ideas also come into play for subtraction in the Jacobian, as
discussed in Proposition/Algorithm 4.6.
     Theorem/Algorithm 4.4 (Negation). Let WD be given, where D is a small
divisor. Then we can compute WE , where xE = −xD , in either one of the following
two ways:
      • Apply Proposition/Algorithm 4.3 to D1 = D and D2 = D0 . We of course
        keep the space WD0 at hand; it corresponds to the zero element on the Ja-
        cobian.
      • Alternatively, if one is willing to hold in memory more extensive information
        on the multiplication map µ, one can find WE using vector spaces of smaller
        dimension. Namely, we need to know the multiplication maps µ21 and µ32 ,
        where we write µmn for the map
            µmn : H 0 OC (mD0 ) ⊗ H 0 OC (nD0 ) → H 0 OC ((m + n)D0 ) .
                                                                            
(4.2)
       We then proceed as follows:
          1. With respect to µ21 , compute the space H 0 OC (2D0 − D) as
                                                                      

          {s ∈ H 0 OC (2D0 ) | ∀t ∈ H 0 OC (D0 ) , µ21 (s ⊗ t) ∈ WD }.
                                                
(4.3)
          2. Choose any nonzero f ∈ H 0 OC (2D0 − D) , and note that (f ) =
                                                          

             D + E ∼ 2D0 (viewing f as a section of OC (2D0 )). Then using µ32 ,
             compute
          H OC (5D0 − D − E) = µ32 H 0 OC (3D0 ) ⊗ f = µ32 (V ⊗ f ).
            0
                                                          
(4.4)
          3. Now use µ32 again to compute WE = H 0 OC (3D0 − E) as
                                                                    

(4.5) {s ∈ V | ∀t ∈ H 0 OC (2D0 − D) , µ32 (s ⊗ t) ∈ H 0 OC (5D0 − D − E) }.
                                                                         

     Proof. The first method proposed is completely straightforward. As for jus-
tifying the second method, we note that the assertion in step 1 follows from the
usual argument, since our requirement that d0 ≥ 2g implies that H 0 OC (D0 )
has no base points. Equation (4.4) is analogous to the identity in step 1 of Theo-
rem/Algorithm 3.10. Finally, the assertion in step 3 follows since H 0 OC (2D0 −D)
also has no base points.
    Our last major algorithm is to add two divisor classes on the Jacobian; by now,
the description is almost trivial. We note a similar algorithm for subtraction, which
unexpectedly is slightly more efficient than the addition algorithm.
20                            KAMAL KHURI-MAKDISI


    Theorem/Algorithm 4.5 (Addition on the Jacobian). Given small divisors
D1 and D2 , or rather their corresponding subspaces WD1 and WD2 , we can compute
a space WE corresponding to a divisor E with xE = xD1 + xD2 (i.e., E ∼ D1 +
D2 − D0 ) as follows:
    1. First use Proposition/Algorithm 4.3 to compute the space WE ′ , where xE ′ =
       −(xD1 + xD2 ).
    2. Now use Theorem/Algorithm 4.4 to find a negation E of E ′ .

    Proposition/Algorithm 4.6 (Subtraction). Given D1 and D2 , we can find
E such that xD1 − xD2 = xE in either one of the following two ways:
      • First negate D1 , thereby obtaining a small divisor D′ with xD′ = −xD1 .
        Then apply Proposition/Algorithm 4.3 to D′ and D2 . This yields WE ,
        where xE = −(−xD1 + xD2 ) as desired. Note that this method only in-
        volves one negation, instead of the two negations that would be involved if
        we first negated D2 , and then used the addition algorithm.
      • Alternatively, we take the operations in Theorems/Algorithms 4.4 and 3.13,
        and remove certain redundant steps to streamline the subtraction algorithm.
        This amounts to the following steps:
            1. Compute H 0 OC (2D0 − D1 ) by “dividing out” D0 , as in step 1 of
               Theorem/Algorithm 4.4.
                                f ∈ H 0 OC (2D0 − D1 ) , viewed as a section of
                                                          
            2. Take a nonzero
               H 0 OC (2D0 ) . Write (f ) = D1 + D1′ , and use µ32 as in step 2 of
                             

               Theorem/Algorithm 4.4 to calculate
                  H 0 OC (5D0 − D1 − D1′ − D2 ) = µ32 (WD2 ⊗ f ).
                                                 
(4.6)
          3. Analogously to step 3 in Theorem/Algorithm 4.4, compute H 0 (L −
              ′            0             ′
                                               
             D1 − D2 ) = H OC (3D0 − D1 − D2 ) as
(4.7)
{s ∈ V | ∀t ∈ H 0 OC (2D0 − D1 ) ,   µ32 (s ⊗ t) ∈ H 0 OC (5D0 − D1 − D1′ − D2 ) }.
                                                                               

          4. Finally, apply Theorem/Algorithm 3.10 to obtain WE as the “flip” of
             the space H 0 (L − D1′ − D2 ).
    Proof. The first method is completely straightforward. As for the second, it
boils down to the facts that xD1′ = −xD1 and that xE = −(xD1′ + xD2 ).

 5. Further improvements to the algorithms in Section 4: the medium
                           and small models
     We now sketch two ways to modify the algorithms from the previous section,
while speeding up the algorithms by a constant factor, so the asymptotics of our
algorithms become a smaller multiple of O(g 4 ). In both cases, we achieve this
linear speedup by reducing the degree of the basic line bundle L, and with it the
dimension of the ambient space V .
     We shall refer to our first method as the medium model. We fix as before an
effective divisor D0 of degree d0 ≥ 2g + 1. (It is possible, but a bit awkward, to
work with d0 = 2g, but this would hamper us in our liberal use of Lemma 2.2.)
We let L = OC (2D0 ), and represent a point xD = [D − D0 ] by the space WD , as
before. Here deg D = d0 ; in case d0 = 2g + 1, we obtain that WD is a (g + 2)-
dimensional subspace of the (3g + 3)-dimensional space V = H 0 OC (2D0 ) . Since
        LINEAR ALGEBRA ALGORITHMS FOR DIVISORS ON AN ALGEBRAIC CURVE                21


δ = dim V = 3g + 3 in this case, we have improved the quantity δ 4 by a factor of
around (5/3)4 ≈ 7.7 over the previous section; this is offset by the fact that we now
have to do about twice as much linear algebra per operation in the Jacobian. So
we predict an effective speedup by approximately a factor of 4.
    Our first observation regarding the medium model is that we can still use
Theorems/Algorithms 3.14 and 4.1 to test for membership of and equality in the
Jacobian in the medium model. We also observe that negation is now simply
a matter of “flipping,” as in Theorem/Algorithm 3.10. We need to make some
modifications to the addition and subtraction algorithms, though. We first give the
algorithm for the “addflip” operation, analogously to Proposition/Algorithm 4.3.
The idea is virtually the same, but we need to keep track of more multiplication
maps. We shall generally use the notation µmn to denote the same multiplication
map as in equation (4.2):
(5.1)            µmn : H 0 (mD0 ) ⊗ H 0 (nD0 ) → H 0 ((m + n)D0 ).
Note that we have simplified notation in this section by writing mD0 instead of,
say, OC (mD0 ).
     Proposition/Algorithm 5.1 (Addflip (medium model)). Given WD1 = H 0 (2D0 −
D1 ) and WD2 = H 0 (2D0 − D2 ), we calculate WE , where xE = −(xD1 + xD2 ), as
follows:
     1. Compute H 0 (4D0 − D1 − D2 ) = µ22 (WD1 ⊗ WD2 ), by Lemma 2.2.
     2. Compute H 0 (3D0 − D1 − D2 ) = {s ∈ H 0 (3D0 ) | ∀t ∈ H 0 (D0 ), µ31 (s ⊗ t) ∈
        H 0 (4D0 − D1 − D2 )}.
     3. Take a nonzero f ∈ H 0 (3D0 − D1 − D2 ); viewing f as a section of OC (3D0 ),
        we obtain (f ) = D1 + D2 + E, where xE is the desired class. Now compute
        H 0 (5D0 − D1 − D2 − E) = µ32 (f ⊗ H 0 (2D0 )).
     4. Obtain WE = {s ∈ V | ∀t ∈ H 0 (3D0 − D1 − D2 ), µ23 (s ⊗ t) ∈ H 0 (5D0 −
        D1 − D2 − E)}.
    The addition algorithm is then obtained by performing an addflip, followed by
a regular flip to negate the result. Subtraction can be done similarly to the first
method of Proposition/Algorithm 4.6. Alternatively, one can adapt the second
method from Proposition/Algorithm 4.6: step 1 in that setting is superfluous, and
one can obtain H 0 (3D0 − D2 ) = µ21 (WD2 ⊗ H 0 (D0 )) for use in step 2 there, and
continue with step 3. Then modify step 4 of that algorithm to resemble the last two
steps of Proposition/Algorithm 5.1. We have described the alternative subtraction
algorithm to illustrate possible techniques, but the simpler subtraction is probably
just as quick.
    We next turn to what we shall call the small model. In principle, one can
represent all points on the Jacobian using divisors of degree g, which can be uniquely
described using an ambient line bundle of degree 3g. However, in order to use
Lemma 2.2, and to avoid some contortions, we shall use instead a divisor D0 of
degree d0 = g + 1 (or at least d0 ≥ g + 1), and put L = OC (3D0 ). So in this case
V = H 0 OC (3D0 ) has dimension 2g + 4, but we need to go up to at least H 0 (7D0 )
within our calculation. We use the same notation for µ as in (5.1). The algorithms
in this setting are reasonably direct generalizations of those in Section 4 and of
those in the medium model; the main problem is that a divisor D′ of degree 2d0
may not be recognizable from the space H 0 (L − D′ ), which may have base points;
so we need to work a bit more to deal with D′ by looking instead at H 0 (L′ − D′ )
22                             KAMAL KHURI-MAKDISI


for a line bundle L′ of sufficiently high degree. On the other hand, the small
model uses smaller-dimensional vector spaces and should give the fastest algorithms
among the ones discussed in this paper. In the small model, we can test equality
on the Jacobian using the second method of Theorem/Algorithm 4.1 (the reader
is invited to find an analog of the first method, using techniques analogous to
those in Propositions/Algorithms 5.2–5.4). We therefore content ourselves with
the algorithms to test for membership of the Jacobian, for the addflip operation,
and a slight improvement for negation (instead of reducing it to addflip). Addition
and subtraction can then be done in a straightforward way, as in Section 4. We note
that one can obtain a slight improvement to the subtraction algorithm, similarly to
the second method in Proposition/Algorithm 4.6. The details are slightly lengthy,
and are left to the reader.
     Proposition/Algorithm 5.2 (Membership test (small model)). Let W ⊂ V
be a codimension d0 subspace. Then we can test whether W = WD for some D as
follows:
     1. Let f be a nonzero element of W , and form the space W+ = µ43 (H 0 (4D0 ) ⊗
        f ) ⊂ H 0 (7D0 ).
     2. Calculate W ′ = {s ∈ H 0 (4D0 ) | ∀t ∈ W, µ43 (s ⊗ t) ∈ W+ }.
     3. Then W comes from a divisor D if and only if W ′ has codimension 2d0 in
        H 0 (4D0 ).
    Proof. This is entirely analogous to Theorem/Algorithm 3.14. The idea is
that we hope to have (f ) = D + D′ , whence W+ = H 0 (7D0 − D − D′ ) and
W ′ = H 0 (4D0 − D′ ). We have had to use the higher-degree line bundle OC (4D0 )
in addition to L, in order to ensure that the degrees are large enough for us to be
able to use Lemma/Algorithm 2.3.

    Proposition/Algorithm 5.3 (Addflip (small model)). Given two subspaces
WD1 = H 0 (3D0 − D1 ) and WD2 = H 0 (3D0 − D2 ), we can find WE , where xE =
−(xD1 + xD2 ), by modifying Proposition/Algorithm 4.3 as follows:
    1. Compute H 0 (3D0 − D1 − D2 ) by Theorem/Algorithm 3.6, without discarding
       the intermediate result H 0 (6D0 − D1 − D2 ). (It is a good idea to obtain
       H 0 (4D0 − D1 − D2 ) in the process; this can be done by setting up linear
       equations to simultaneously “divide” out both H 0 (3D0 ) and H 0 (2D0 ) from
       H 0 (6D0 − D1 − D2 ), the former via (3.4), and the latter via an analogous
       calculation that largely overlaps with (3.4).)
    2. Take a nonzero f ∈ H 0 (3D0 − D1 − D2 ); so, viewing f as a section of
       OC (3D0 ), we have (f ) = D1 + D2 + E for the desired E.
    3. Calculate WE as
(5.2)
   {s ∈ H 0 (3D0 ) | ∀t ∈ H 0 (6D0 − D1 − D2 ), µ36 (s ⊗ t) ∈ µ36 (f ⊗ H 0 (6D0 ))}.
       Note that this method involves calculation in H 0 (9D0 ) = H 0 (3L); if we have
       done the extra computation in step 1, we can limit ourselves to H 0 (7D0 ), by
       replacing 6D0 by 4D0 throughout (5.2).
    Proof. Immediate. Note the trouble that we went to because H 0 (3D0 − D1 −
D2 ) is not necessarily base point free, which meant that we had to use (5.2) instead
of doing a regular “flipping” algorithm after step 1 above. However, we still point
      LINEAR ALGEBRA ALGORITHMS FOR DIVISORS ON AN ALGEBRAIC CURVE                      23


out that, generically, H 0 (3D0 − D1 − D2 ) is base point free, since its degree is
d0 ≥ g + 1.

    Proposition/Algorithm 5.4 (Negation (small model)). Given WD , we can
find WE , where xE = −xD , by using the addflip operation. Alternatively, we can
use the following slightly faster method:
    1. Calculate H 0 (5D0 − D) = µ23 (H 0 (2D0 ) ⊗ WD ). Then calculate H 0 (2D0 −
       D) = {s ∈ H 0 (2D0 ) | ∀t ∈ V, µ23 (s ⊗ t) ∈ H 0 (5D0 − D)}.
    2. Take a nonzero f ∈ H 0 (2D0 − D), and compute H 0 (6D0 − D − E) =
       µ24 (f ⊗ H 0 (4D0 )).
    3. Finally, compute WE = {s ∈ H 0 (3D0 ) | ∀t ∈ WD , µ33 (s ⊗ t) ∈ H 0 (6D0 −
       D − E)}.
    Proof. This is just like Theorem/Algorithm 4.4, but we have included the
algorithm to show in step 1 the technique of going from H 0 (3D0 −D) to H 0 (2D0 −D)
by virtue of first “going up,” then “going down.” This is because the degree of
D0 is too small for us to automatically be able to “divide” by H 0 (D0 ). If we
were originally careful enough to select D0 so that H 0 (D0 ) were base point free,
we could have begun as in Theorem/Algorithm 4.4. However, we cannot in any
way guarantee that H 0 (2D0 − D) is base point free, since D is arbitrary; hence,
concluding with the computation in (4.5) was never an option in the setting of the
small model.
      We conclude this paper with a brief discussion of converting points on the Jaco-
bian between their representations in the different models. The first observation is
that it is easy to pass between two representations of the same (as always, effective)
divisor D in terms of spaces WD of sections of two different line bundles L1 and
L2 . (Typically, L1 = OC (n1 D0 ) and L2 = OC (n2 D0 ) for a fixed D0 and integers
n1 , n2 .) So the problem is to pass from a knowledge of H 0 (L1 − D) to one of
H 0 (L2 − D). Let us assume for a moment that deg L1 ≥ 2g + 1 + deg D. Then take
auxiliary line bundles L′1 , L′2 of degree at least 2g + 1, such that L1 + L′1 = L2 + L′2 ;
here, addition of line bundles really refers to their tensor product. Then, using
multiplication of sections in H 0 (L1 − D) and H 0 (L′1 ), we can obtain the space
H 0 (L1 + L′1 − D) = H 0 (L2 + L′2 − D). We can then “divide” by H 0 (L′2 ) to obtain
H 0 (L2 − D), as desired. This is similar to step 1 in Proposition/Algorithm 5.4. Of
course, if the degree of L1 is sufficiently larger than the degree of L2 , we only need
to perform a single division, without first raising the degree using L′1 . Similarly, if
the degree of L2 is large compared to that of L1 , then a single multiplication step
is sufficient.
      The above discussion seems to require the use of Lemma 2.2 for the multiplica-
tion step. We can modify the procedure, though, to work whenever H 0 (L1 − D) is
base point free (such as when deg L1 ≥ 2g + deg D). The idea is to take a nonzero
section f ∈ H 0 (L1 − D), whose divisor (viewing f as a section of L1 ) is D + D′ .
Here we caution that the degree of D′ may be large, so that H 0 (L1 − D′ ) may well
have base points. To get around this, we take an auxiliary line bundle L′ of degree
at least 2g + 1 + deg D′ , and multiply f by H 0 (L′ ) to obtain H 0 (L1 + L′ − D − D′ ).
Dividing out H 0 (L1 − D) then yields H 0 (L′ − D′ ). We can then multiply f by
H 0 (L′1 + L′ ), where L′1 has suitably large degree, and then divide by H 0 (L′ − D′ )
(which is now base point free), to obtain H 0 (L′1 + L1 − D) even in the case where
we could not use Lemma 2.2 as in the above paragraph. We note that throughout
24                               KAMAL KHURI-MAKDISI


all these computations, the degrees of the intermediate line bundles are at most
O(max(deg L1 , deg L2 , g)).
     Now that we have full control over the ambient line bundle L used to represent
individual divisors D, we shall always assume that the degree of L is sufficiently
large, and use L to represent all divisors (so D is given by WD = H 0 (L − D),
unless stated otherwise). We now discuss how to change the basepoint D0 used
to map a divisor D to the point xD = [D − D0 ] on the Jacobian. It is always
easy to add an effective divisor E to D0 , since [D − D0 ] = [(D + E) − (D0 + E)],
so we can use Theorem/Algorithm 3.6 to replace WD with WD+E . In particular,
we can also assume that deg D0 ≥ 2g + 1. Thus the main question that remains
is how to replace D0 by a new basepoint E0 of smaller degree. This means that
given D, we wish to find E such that [D − D0 ] = [E − E0 ]; in other words, we
seek an effective divisor E ∼ D + E0 − D0 . Writing D1 = D + E0 (which we
compute as usual by Theorem/Algorithm 3.6, and whose degree is even larger than
deg D = deg D0 ≥ 2g + 1), we have reduced our question to the following result,
which leads to an efficient algorithm for the Riemann-Roch problem on C. Like
our other algorithms, this one requires O(max(deg D0 , deg D1 , g)4 ) field operations
in k. Remember that there is no loss of generality in letting L have large degree
N ≥ 2g + 1 + deg D1 .
     Theorem/Algorithm 5.5. Let deg L = N , and assume given (effective) di-
visors D1 and D0 , whose degrees lie between 2g + 1 and N − 2g − 1. Then we can
compute the space H 0 (D1 − D0 ), and with it (if the space is nonzero) an effective
divisor E ∼ D1 − D0 . The procedure is:
     1. Use Theorem/Algorithm 3.10 to compute D1′ (specifically, to compute WD1′ =
        H 0 (L − D1′ )), where D1 + D1′ ∼ L. Thus L − D1′ − D0 ∼ D1 − D0 , and
        an explicit isomorphism from H 0 (D1 − D0 ) to H 0 (L − D1′ − D0 ) is given
        by multiplication by the section f of L with (f ) = D1 + D1′ used in the
        calculation of WD1′ .
     2. Compute H 0 (2L − D1′ − D0 ) = µ(WD1′ ⊗ WD0 ), and use it to compute
        WD1′ +D0 ∼= H 0 (D1 − D0 ), as in Theorem/Algorithm 3.6.
     3. A divisor E as above exists if and only if we can find a nonzero g ∈ WD1′ +D0 ,
        in which case we view g as a section of L and see that its divisor is (g) =
        D1′ + D0 + E. Then calculate
(5.3)
   WE = {s ∈ H 0 (L) | ∀t ∈ H 0 (2L − D1′ − D0 ),       µ′ (s ⊗ t) ∈ µ′ (g ⊗ H 0 (2L))}.
       Here µ′ : H 0 (L) ⊗ H 0 (2L) → H 0 (3L) is the multiplication map. (We did
       not use the notational convention of (5.1), since we are not assuming that
       L is a multiple of D0 .)
     Proof. We know that µ′ (g ⊗ H 0 (2L)) = H 0 (3L − D1′ − D0 − E), and our
generous assumptions about degrees ensure that H 0 (2L − D1′ − D0 ) is base point
free. Note that we do not assume that the smaller space H 0 (L − D1′ − D0 ) is base
point free; indeed, its degree is deg D1 − deg D0 , which may be quite small. The
rest of the proof is standard by now.

                                       References
[ACGH] E. Arbarello, M. Cornalba, P. Griffiths, and J. Harris, Geometry of Algebraic Curves,
 Grundlehren der mathematischen Wissenschaften 267, Springer, 1985.
      LINEAR ALGEBRA ALGORITHMS FOR DIVISORS ON AN ALGEBRAIC CURVE                            25


[AdMH] L. M. Adleman, J. DeMarrais, and M.-D. Huang, A subexponential algorithm for discrete
 logarithms over the rational subgroup of the Jacobians of large genus hyperelliptic curves over
 finite fields, pp. 28–40 in Algorithmic Number Theory (“ANTS-I”), (Ithaca, NY, 1994), eds. L.
 M. Adleman and M.-D. Huang, Lecture Notes in Computer Science 877, Springer, 1994.
[BLR] S. Bosch, W. Lütkebohmert, and M. Raynaud, Néron Models, Ergebnisse der Mathematik
 3. Folge, Bd. 21, Springer, 1990.
[C] D. G. Cantor, Computing in the Jacobian of a hyperelliptic curve, Mathematics of Computa-
 tion 48 (1987), 95–101.
[GPS] S. D. Galbraith, S. Paulus, and N. P. Smart, Arithmetic on superelliptic curves, Mathe-
 matics of Computation 71 (2002), 393–405.
[GH] P. Griffiths and J. Harris, Principles of Algebraic Geometry, Wiley, 1978, reprinted 1994.
[Ha] R. Hartshorne, Algebraic Geometry, Springer, 1977.
[He1] F. Hess, Zur Divisorenklassengruppenberechnung in globalen Funktionenkörpern, 1999
 Ph.D. thesis available from
 http://www.math.TU-Berlin.DE/~kant/publications/diss/diss_FH.ps.gz
[He2] F. Hess, Computing Riemann-Roch spaces in algebraic function fields and related topics,
 Journal of Symbolic Computation 33 (2002), 425–445.
[HS] R. Harasawa and J. Suzuki, Fast Jacobian group arithmetic on Cab curves, pp. 359–376
 in Algorithmic Number Theory (“ANTS-IV”) (Leiden, 2000), ed. W. Bosma, Lecture Notes in
 Computer Science 1838, Springer, 2000.
[HI] M.-D. Huang and D. Ierardi, Efficient algorithms for the Riemann-Roch problem and for
 addition in the Jacobian of a curve, Journal of Symbolic Computation 18 (1994), 519–539.
[L] R. Lazarsfeld, A sampling of vector bundle techniques in the study of linear series, pp. 500–
 559 in Lectures on Riemann surfaces (Trieste, 1987), eds. M. Cornalba, X. Gomez-Mont and A.
 Verjovsky, World Scientific Publishing Co., 1989.
[M] J. Milne, Jacobian varieties, pp. 167–212 in Arithmetic Geometry, eds. G. Cornell and J.
 Silverman, Springer, 1986.
[V] E. Volcheck, Computing in the Jacobian of a plane algebraic curve, pp. 221–233 in Algorithmic
 Number Theory (“ANTS-I”), (Ithaca, NY, 1994), eds. L. M. Adleman and M.-D. Huang, Lecture
 Notes in Computer Science 877, Springer, 1994.

    Mathematics Department and Center for Advanced Mathematical Sciences, Amer-
ican University of Beirut, Bliss Street, Beirut, Lebanon
    E-mail address: kmakdisi@aub.edu.lb
