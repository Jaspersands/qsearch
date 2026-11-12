PRIMARY SOURCE: https://mathe2.uni-bayreuth.de/stoll/papers/ratpts-selmer-2016-12-07.pdf
Retained text research/audits/sources/local_halving_saturation/stoll.txt, sha256 719e418aa05e24e22d22bbadc25cffd9a5eaf700c7ad0068415fa21aed9f65be

Physical newline lines 755-944:
avoid failure of the algorithm are likely to be satisfied. This follows from work of Bhargava
and Gross [BG13], which we use in a similar way as in [PS14]: the ‘probability’ that the map
Sel2 J → J(Q2 )/2J(Q2 ) is injective is at least 1−21−g−dimF2 J(Q2 )[2] , and the ‘probability’ that
the image has intersection with Y contained in R is at least 1 − (#(Y /R) − 1)21−g . Since by
the results of [PS14] Y is usually small and by [Sto15] the size of Y modulo R is uniformly
bounded by some constant times g 2 , there is a very good chance that both conditions are
satisfied when g is large.

                 5. Halving points on odd hyperelliptic Jacobians

In this section we describe an algorithm that computes one ‘half’ or all ‘halves’ of a point
P ∈ 2J(k), where J is the Jacobian of a hyperelliptic curve C of odd degree over the field k.
We assume that char(k) 6= 2, so that C can be given by an equation y 2 = f (x) with f ∈ k[x]
squarefree and of odd degree 2g + 1.
Recall that each point in J(k) is uniquely represented in the form [D − d∞], where D is an
effective divisor in general position defined over k and d = deg D ≤ g. An effective divisor D
is said to be in general position if its support does not contain ∞ and D 6≥ P + ι(P ) for any
point P ∈ C, where ι : C → C is the hyperelliptic involution.
Any effective divisor D in general position can be described by its Mumford representation
(a, b). Here a ∈ k[x] is a monic polynomial of degree d = deg D whose roots are the
x-coordinates of the points in the support of D, with appropriate multiplicity (so that a
corresponds to the image of D under the hyperelliptic quotient map to P1 ), and b ∈ k[x] is
another polynomial such that b(ξ) = η for any point P = (ξ, η) in the support of D and
satisfying a | f − b2 . This polynomial b is uniquely determined modulo a; in particular, we
obtain a unique representation if we require deg(b) < d. However, it is sometimes useful to
allow additional flexibility, so we will not always insist on this normalization. In fact, we
may also want to allow polynomials a of larger degree (this leads to even more non-unique
representations, but can be useful in certain situations).
                                                 17
 We will use the notation (a, b) to denote the divisor D, and we will write [a, b] = [(a, b)−d∞]
for the point on J corresponding to it.
Let c be the leading coefficient of f . Then in terms of the Mumford representation, the
descent map µ : J(k) → L  is given by
                                 [a, b] 7−→ (−c)deg(a) a(θ) · (L× )2
if a and f are coprime. In the general case, write a1 and f1 for a and f divided by their
(monic) gcd; then
                  µ([a, b]) = µ̃(a) := (−c)deg(a) a(θ) − a1 (θ)f1 (θ) · (L× )2 ;
                                                                      

compare [Sch95].
Since the kernel of µ is 2J(k), this gives us a way of deciding whether a point P ∈ J(k) is
divisible by 2 in J(k): this is equivalent to the existence of a polynomial s ∈ k[x] such that
                             s(θ)2 = (−c)deg(a) a(θ) − a1 (θ)f1 (θ) ;
                                                                    

equivalently,
                               s2 ≡ (−c)deg(a) (a − a1 f1 ) mod f.
We will now state a result that shows how to compute a point Q ∈ J(k) such that 2Q = P ,
given such a polynomial s.
Note that when a = a21 a2 , then P = [a, b] is divisible by 2 if and only if P2 = [a2 , b] is, and
each point Q such that 2Q = P has the form Q = Q1 + Q2 where Q2 satisfies 2Q2 = P2 and
Q1 = [a1 , b]. So we can assume that a is squarefree.
Proposition 5.1. Let a ∈ k[x] be monic and squarefree, of degree ≤ 2g + 1. Let d denote
gcd(a, f ), so that a = da1 and f = df1 as above. Suppose we have b, s ∈ k[x] with
                 f ≡ b2 mod a        and       (−c)deg(a) (a − a1 f1 ) ≡ s2 mod f,
so that [a, b] ∈ 2J(k). For polynomials u, v and w, consider the following system of congru-
ences:
(5.1)              vd ≡ ws mod f1 ,      vd ≡ ub mod a1 ,      uf1 ≡ ws mod d.
Then this system has a nontrivial solution (u, v, w) with w monic such that
(5.2)       deg(u) < deg(a)/2,     deg(v) ≤ g + deg(a)/2 − deg(d) and            deg(w) ≤ g.
Each such solution satisfies the relation
(5.3)                             u2 f1 = dv 2 − (−c)deg(a) a1 w2 .
Now assume that (u, v, w) is a solution such that w has minimal degree. Let d1 = gcd(u, w);
then d1 divides f a1 and v. Write d1 = df da with df = gcd(d1 , f ) and da = gcd(d1 , a1 ). Set
w1 = w/d1 , u1 = u/d1 , v1 = v/d1 and let r ∈ k[x] be such that
                      ru1 ≡ −v1 d mod w1 da           and     r ≡ 0 mod df .
Then Q = [w, r] satisfies P = 2Q.
If Q and Q0 are computed starting from s and s0 such that s0 6≡ ±s mod f , then Q and Q0
are distinct.
                                                 18
 Proof. First note that, since f is squarefree, we have that d and f1 are coprime. Also, d
and a1 are coprime, since a divisor in general position contains no ramification point with
multiplicity 2 or more. So f1 , a1 and d are coprime in pairs and squarefree. The fact that a
divides f − b2 implies that d divides b and that d is also the gcd of a and b.
The first claim is that the system of congruences has a nontrivial solution when the degrees
of the polynomials are bounded as stated. To see this, note that the conditions are linear in
(the coefficients of) u, v and w, and that the total number of coefficients of u, v and w is
  ddeg(a)/2e + (g + bdeg(a)/2c − deg(d) + 1) + (g + 1) = 2g + deg(a) − deg(d) + 2
                                                              = deg(f1 ) + deg(a1 ) + deg(d) + 1.
On the other hand, the number of linear constraints is deg(f1 ) + deg(a1 ) + deg(d). So there
are more variables than constraints, hence nontrivial solutions exist.
We claim that w cannot be zero in such a solution. Otherwise, the first congruence would
imply that f1 divides v (since f1 , a1 and d are coprime in pairs), which for degree reasons
(recall that deg(a) ≤ 2g + 1) is only possible when v = 0. In a similar way, the second
congruence would then imply that a1 divides u (since a1 is coprime to b), whereas the third
congruence implies that d divides u, so a divides u, which is only possible when u = 0. But
then our solution is trivial, a contradiction. So w 6= 0, and without loss of generality, w can
be taken to be monic.
We show that every solution as above satisfies relation (5.3). Namely, by the first congruence
and since s2 ≡ (−c)deg(a) a mod f1 ,
          d2 v 2 = (dv)2 ≡ (sw)2 = s2 w2 ≡ (−c)deg(a) aw2 = (−c)deg(a) da1 w2 mod f1 ,
so (since d and f1 are coprime), the relation holds mod f1 . Next, by the second congruence,
                     d2 v 2 = (dv)2 ≡ (bu)2 = b2 u2 ≡ f u2 = df1 u2 mod a1 ,
so (since d and a1 are coprime), the relation holds mod a1 . Finally, by the last congruence,
                 u2 f12 = (uf1 )2 ≡ (sw)2 = s2 w2 ≡ −(−c)deg(a) a1 f1 w2 mod d,
so (since d and f1 are coprime again), the relation holds also mod d. It follows that it holds
mod f1 a1 d. Since the degrees of all terms are strictly less than the degree of f1 a1 d, equality
follows, and (5.3) is verified.
We note that the fact shown above that a nontrivial solution has w 6= 0 implies that w
determines the solution uniquely. It follows that there is in fact a unique solution with
w monic and deg(w) minimal.
Since d is squarefree, (5.3) implies that the gcd d1 of w and u also divides v. We can therefore
divide all three by this gcd, obtaining u1 , v1 and w1 ; they satisfy
                                 u21 f1 = dv12 − (−c)deg(a) a1 w12 .
If some irreducible factor p of d1 does not divide f a1 , then (u/p, v/p, w/p) also satisfy
the system of congruences, contradicting the minimality of deg(w). Now assume that p2
divides d1 for some irreducible polynomial p. Then p divides f1 , a1 or d, say p | a1 (the
other cases are analogous). Since a1 is squarefree, the congruence vd ≡ ub mod a1 implies
(v/p)d ≡ (u/p)b mod a1 , and so again (u/p, v/p, w/p) satisfy the system of congruences,
                                                 19
 contradiction. So d1 is squarefree and must therefore divide a1 f1 d. In particular, we can
write d1 = df da as claimed.
Note that (u1 b)2 ≡ u21 f ≡ (v1 d)2 mod a1 , so that a1 divides (u1 b − v1 d)(u1 b + v1 d). We claim
that da = gcd(u1 b + v1 d, a1 ). For this, consider an irreducible factor p of da . If p divides
u1 b − v1 d, then (u/p, v/p, w/p) are a solution, a contradiction. So p must divide u1 b + v1 d.
Conversely, if p is any irreducible factor of a1 that divides u1 b + v1 d, then (noticing that b is
invertible mod a1 ) for p to divide ub − vd, it must necessarily divide u and v, so p | da .
u1 is invertible mod w1 , but also mod da (since u1 and v1 are coprime as well — a1 is
squarefree — and da is coprime with f1 and d). Furthermore, df is coprime with w1 (and of
course also with da ), for essentially the same reason. Therefore a polynomial r exists such
that u1 r ≡ −v1 d mod w1 da and r ≡ 0 mod df .
Now we consider the function
                   φ = u(x)y − v(x)d(x) = df (x)da (x) (u1 (x)y − v1 (x)d(x))
on C. Its divisor of zeros is
                                                                                           
         2(df , 0) + (da , b) + (da , −b) + (d, 0) + (da , −b) + (a1 /da , b) + 2(w1 , −r)
                                                                            
                   = (a1 , b) + (d, 0) + 2 (df , 0) + (da , −b) + (w1 , −r)
                  = (a, b) + 2(w, −r).
To see this, note that the norm in k[x] of the last factor of φ is u21 f − v12 d2 = (−c)deg(a) da1 w12
and that u1 b ≡ v1 d mod a1 /da and u1 b ≡ −v1 d mod da (and so also r ≡ b mod da ). Setting
Q = [w, r], we therefore obtain 2Q = P .
We now show that Q determines s mod f up to sign. Given Q = [w, r] such that 2Q = P ,
there is a unique function (up to scaling) on C whose divisor is (a, b) + 2(w, −r) − n∞
(where n = deg(a) + 2 deg(w)); this function must then be φ, which gives us u and v up to
scaling; the relation u2 f1 = dv 2 − (−c)deg(a) aw2 then fixes them up to a common sign. Write
df = df1 dd with df1 = gcd(df , f1 ) and dd = gcd(df , d). In a similar way as above for da , one
shows that df1 = gcd(w1 s + v1 d, f1 ) and dd = gcd(u1 f1 + w1 s, d). Since w1 is coprime with f ,
this determines s mod f via the congruences
                         w1 s ≡ v1 d mod f1 /df1 ,      w1 s ≡ −v1 d mod df1 ,
                         w1 s ≡ u1 f1 mod d/dd ,        w1 s ≡ −u1 f1 mod dd .
A common sign change of u and v (which is the only ambiguity here) results in a sign change
of s.                                                                                     

We can try to use the algorithm implied by Proposition 5.1 over a p-adic field. It will possibly
run into precision problems when some of the roots of a get close to roots of f (but with the
resultant of a and f still being nonzero, albeit p-adically small) or when the resulting point
is represented by a divisor of lower degree or such that some points are close to the point
at infinity. In practice, however, these problems occur fairly rarely. A possible remedy in
such a case is to replace (a, b) by another representation (a0 , b0 ) such that [a0 , b0 ] = [a, b] and
deg(a) > g. Writing f −b2 = ac, we have [c−2hb−h2 a, −b−ha] = [a, b] for all polynomials h.
Taking h to be constant already allows us to replace a by a polynomial a0 that is coprime
with f (and probably we can also arrange a0 to be squarefree) and satisfies deg(a0 ) ≤ g + 1
                                                   20
 if deg(a) = g. Another possibility is to consider points in a residue disk given by suitable
Laurent series, perform the computation on the Laurent series and then specialize.
Remark 5.2. In the context of computing q(P ), the following observation can be useful.
Given P = [a, b] with deg(a) ≤ g + 1 and T = [h, 0] ∈ J(k)[2] with h | f and deg(h) ≤ g,
we can use the method described in Proposition 5.1 to compute halves of P + T without
first computing a representation of the sum. For simplicity assume gcd(a, f ) = 1 (this can
be arranged, see above). Then P + T = [ah, b0 h] where b0 h ≡ b mod a. There will be s1
and s2 such that s21 ≡ (−c)deg(a) ah mod f /h and s22 ≡ −(−c)deg(a) a(f /h) mod h. We obtain
the congruences
                vh ≡ ws1 mod f /h,      vh ≡ ub mod a,      u(f /h) ≡ ws2 mod h
with deg(u) < (deg(a) + deg(h))/2, deg(v) ≤ g + (deg(a) − deg(h))/2 and deg(w) ≤ g.
In a similar way, we can divide P + P 0 by 2: let P = [a, b], P 0 = [a0 , b0 ] and assume that
deg(a) + deg(a0 ) ≤ 2g + 1 and that a, a0 and f are coprime in pairs. Given a polynomial s
                               0
such that s2 ≡ (−c)deg(a)+deg(a ) aa0 mod f , the system to be solved is
                       v ≡ ws mod f,     v ≡ ub mod a,      v ≡ ub0 mod a0
with deg(u) < (deg(a) + deg(a0 ))/2, deg(v) ≤ g + (deg(a) + deg(a0 ))/2 and deg(w) ≤ g.

We mention one implication that can be helpful in applications.
Corollary 5.3. Let [a0 , b] be the Mumford representation of a point P ∈ J(k), write a0 = a20 a
with a squarefree and monic and fix a polynomial s such that s2 ≡ (−c)deg(a) (a − a1 f1 ) mod f
as above. Let (u, v, w) be the solution with w monic and of smallest degree of the system (5.1)
with the restrictions in (5.2), and let Q ∈ J(k) be the associated point such that 2Q = P .
Then µ(Q) = µ̃(a0 )µ̃(w).

Proof. This is because according to Proposition 5.1, Q = [a0 , b]+ [w, r] for some r ∈ k[x].  
Corollary 5.4. In the situation of Corollary 5.3, we have the following special cases.
(1) If P = [(ξ, η) − ∞] ∈ 2J(k) with η 6= 0, fix s ∈ k[x] such that s2 ≡ c(ξ − x) mod f . Let w
    be the monic polynomial of smallest degree such that the residue of smallest degree of ws
    modulo f has degree ≤ g. Then the point Q ∈ J(k) with 2Q = P that is associated to s
    satisfies
                                             µ(Q) = µ̃(w).
(2) If P = [(ξ1 , η1 ) − (ξ2 , η2 )] ∈ 2J(k) with ξ1 6= ξ2 and ηj 6= 0 for j ∈ {1, 2}, fix s ∈ k[x]
    such that s2 ≡ (x − ξ1 )(x − ξ2 ) mod f . Let w be the monic polynomial of smallest degree
    such that the residue v of smallest degree of ws modulo f has degree ≤ g + 1 and satisfies
    η2 v(ξ1 ) + η1 v(ξ2 ) = 0. Then the point Q ∈ J(k) with 2Q = P that is associated to s

PRIMARY SOURCE: https://arxiv.org/pdf/math/0105182
Retained text research/audits/sources/surface_torsion_selection/khuri_makdisi_divisors.txt, sha256 706c51d45bf55ae2acd77c377cad980edf24afe4de24b0b13294bce7037d1d42

Physical newline lines 147-200:
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

Physical newline lines 240-292:
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
