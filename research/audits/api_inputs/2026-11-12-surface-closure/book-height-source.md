Primary book https://www.math.u-bordeaux.fr/~jcouveig/publi/book.pdf
Text SHA256 0ae7a4befba82ce944abeb0f71f745403bcbb9c8418232d050c8e6effba83dd9
PDF text has symbol extraction defects; do not infer ambiguous signs. Physical line excerpts follow.

Lines 4260-4360
scheme X together with a Hermitian line bundle .L; kk/. Let x be in X.K/.
Then, by the properness of X over OK , x extends uniquely to an OK -valued
                       bookcourant     January 8, 2011




88                                                                   CHAPTER 4

point, also denoted x, and one defines

.4:3:2/                   hK .x/ WD deg x  .L; kk/:

The same method as the one used above can be applied to get an absolute
height hW X.Q/ ! R. For K ! K 0 a finite extension, each x in X.K 0 /
extends uniquely to an x in X.OK 0 /, and one defines
                                     deg x  .L; kk/
.4:3:3/                    h.x/ WD                    :
                                       dimQ K 0
It is not hard to verify that this height function h is in the class (mod-
ulo bounded functions) that is attached to XK and LK (without metric);
see Proposition 7.2 of Chapter 6 of [Co-Si], or Theorem 4.5 of Chapter V
                                 n
in [Ed-Ev]. In fact, for X D PO    K
                                     , and L D O.1/ with a suitable metric,
the height h just defined is equal to the one defined in (4.2.1).


4.4 ARITHMETIC SURFACES, INTERSECTION THEORY, AND ARITH-
METIC RIEMANN-ROCH

The context in which we are going to apply Arakelov theory is that of
smooth projective curves X over number fields K. In [Ara] Arakelov de-
fined an intersection theory on the arithmetic surfaces attached to such
curves, with the aim of proving certain results, known in the case of function
fields, in the case of number fields. The idea is to take a regular projective
model X over B WD Spec.OK / of X, and try to develop an intersection the-
ory on the surface X , analogous to the theory one has when K is a function
field. If K is a function field over a finite field k, say, one gets a projective
surface X over k, fibered over the nonsingular projective curve B over k that
corresponds to K. On such a projective surface, intersecting with principal
divisors gives zero, hence the intersection pairing factors through the Picard
group of X , the group of isomorphism classes of invertible OX -modules.
In the number field case one “compactifies” B by formally adding the in-
finite places of K; the product formula then means that principal divisors
have degree zero. Instead of the Picard group of X , one considers the group
of isomorphism classes of certain metrized line bundles on X , as defined
above. In [Fal1] (see also Chapters II, III and I of [Szp]), Faltings extended
                        bookcourant         January 8, 2011




SHORT INTRODUCTION TO HEIGHTS AND ARAKELOV THEORY                              89

Arakelov’s work by establishing results such as a Grothendieck-Riemann-
Roch theorem in this context. Since then, Arakelov theory has been gener-
alized by Gillet and Soulé (see [Sou] and [Fal2]). Below, we will use the
theory as given in [Fal1] and Chapter II of [Szp]. We start with some prepa-
rations concerning Riemann surfaces. The aim of this subsection is to give
the arithmetic Riemann-Roch theorem as stated and proved by Faltings.
   Let X be a compact Riemann surface of genus g > 0. The space of holo-
                               1
morphic differentials H0 .X; X  / carries a natural Hermitian inner product:
                                      i
                                         Z
.4:4:1/                    .!; / 7!         ! ^ :
                                      2 X
Let .!1 ; : : : ; !g / be an orthonormal basis with respect to this inner product.
This leads to a positive .1; 1/-form  on X given by
                                        g
                                i X
.4:4:2/                     D      !k ^ !k ;
                               2g
                                       kD1
                                                               R
independent of the choice of orthonormal basis. Note that X  D 1. We
refer to [Ara] for a proof of the following proposition. Denote by C 1 the
sheaf of complex-valued C 1 -functions on X, and by A1 the sheaf of com-
plex C 1 1-forms on X. Recall that we have a tautological differential op-
erator d W C 1 ! A1 . It decomposes as d D @ C @ where, for any local C 1
function f and any holomorphic local coordinate z, with real and imaginary
parts x and y, one has @f D 21 . @f
                                 @x
                                      i @f
                                        @y
                                           /  dz and @f D 12 . @f
                                                                @x
                                                                   C i @f
                                                                       @y
                                                                          /  d z.

4.4.3 Proposition For each a in X, there exists a unique real-valued ga;
in C 1 .X fag/ such that the following properties hold:

   1. we can write ga; D log jz z.a/j C h in an open neighborhood of a,
      where z is a local holomorphic coordinate and h is a C 1 -function;

   2. @@ga; D  i on X        fag;
      R
   3. X ga;  D 0:

Lines 8930-9635

In this chapter we start applying Arakelov theory in order to derive a bound
for the height of the coefficients of the polynomials PD0 ;fl ;m as in (8.2.10).
We proceed in a few steps. The first step, taken in Section 9.1, is to relate the
height of the bl .Qx;i / as in Section 8.2 to intersection numbers on Xl . The
second step, taken in Section 9.2, is to get some control on the difference
of the divisors D0 and Dx as in (3.4). Certain intersection numbers con-
cerning this difference are bounded in Theorem 9.2.5, in terms of a number
of invariants in the Arakelov theory on modular curves Xl . These invari-
ants will then be bounded in terms of l in Sections 11.1, 11.2, and 11.3.
Finally, in Section 11.7, the height of the coefficients of the PD0 ;fl ;m will
be bounded. In this chapter, we do our best to formulate the most important
results, Theorem 9.1.3, Theorem 9.2.1, and Theorem 9.2.5, in the context of
curves over number fields, that is, outside the context of modular curves.


9.1 RELATING HEIGHTS TO INTERSECTION NUMBERS

We pick up the notation at the end of Section 8.2, so we have a modu-
lar curve Xl D X1 .5l/Q with l > 5, nonconstant morphisms bl and
xl0 W Xl ! PQ1
               , and certain divisors Dxfin D di D1
                                               P x
                                                       Qx;i on Xl;Q that have
support outside the cusps. It is our objective in this section to link the abso-
lute height h.bl .Qx;i // of the algebraic numbers bl .Qx;i / to certain quanti-
ties coming from Arakelov intersection theory. The height of xl0 .Qx;i / will
be bounded in terms of h.bl .Qx;i // in Section 11.5. The final estimates for
these heights, depending only on l, will be done in Section 11.7.
                       bookcourant     January 8, 2011




188                                                                CHAPTER 9

9.1.1 Theorem Let x be in V , and let i be in f1; : : : ; dx g. Let K be a
number field containing Q.5l / and such that Qx;i is defined over K. Let
X be the minimal regular model of Xl over K. Then we have

                       1                           X
  h.bl .Qx;i //            .Qx;i ; bl 1/X C l 2     sup g
                    ŒK W Q                          X
                                                             !
                              1X                               1
                                      Z
                            C             log.jbl j2 C 1/X C log 2 :
                              2  X                           2

Here  runs through the embeddings of K into C and g is the Arakelov-
Green function on Xl; .

In the next chapters we shall derive bounds that are polynomial in l for all
terms in the above estimate.
   Theorem 9.1.1 will be derived from Theorem 9.1.3 below, which states
a fairly general result. We start with a definition. Let K be a number field
                 1                                              1
and consider PO    K
                     . Let 1 denote the OK -point .1 W 0/ of PO   K
                                                                    . For any
                1
section P in POK .OK / we define by .P; 1/P 1 the degree (see (4.3.1)) of
P  OP 1 .1/, where OP 1 .1/ has the Fubini-Study metric, that is, the metric
k  kP 1 given by

                                                   jx1 j
.9:1:2/             k1kP 1 .x0 W x1 / WD
                                           .jx0 j2 C jx1 j2 /1=2

      1
over PC . Here 1 is the tautological section of OP 1 .1/.


9.1.3 Theorem Let X be a geometrically irreducible, smooth, and com-
plete curve of positive genus over a number field K, and let X be a proper
semistable model of X over the ring of integers OK of K. Suppose that we
have a nonconstant morphism f W X ! PK1 and a K-rational point Q of X
with f .Q/ ¤ 1. Write the divisor div.f / of f as div.f /C div.f / , with
div.f /C and div.f / effective and without common irreducible compo-
nents. Assume that the Zariski closure of Supp.div.f /C / [ Supp.div.f / /
in X is étale over OK . For any closed point s of Spec.OK /, denote by
ms .f / the supremum of the multiplicities of div.f / on X along the irre-
                        bookcourant     January 8, 2011




APPLYING ARAKELOV THEORY                                                         189

ducible components of the fiber at s of X . Then we have the inequality
                                          X
.f .Q/; 1/P 1 .Q; f  1/X C deg f             sup g
                                              X
                     1X
                         Z                      X
                   C        log.jf j2 C 1/X C   ms .f / log #k.s/ :
                     2  X                     s

Here the first sum runs over the embeddings of K into C, and the last sum
runs over the closed points of Spec.OK /.


Proof Note that the locus of indeterminacy of f on X consists of finitely
many closed points. This implies that there exists a blow-up XQ ! X of X
such that f extends to a regular map f W XQ ! PO   1
                                                     K
                                                       . For any such XQ we
have by construction

              .f .Q/; 1/P 1 D deg f .Q/ .OP 1 .1/; k  kP 1 /
                              D deg Q f  .OP 1 .1/; k  kP 1 /
                              D deg Q .OXQ .f  1/; k  kP 1 / ;

where we write 1 to emphasize that f  1 is the inverse image under f of
1.Spec.OK //, and not the Zariski closure f  1 of the inverse image under
f of 1.Spec.K//. If we let k  kX denote the canonical Arakelov metric on
OX .f  1/ then we can write

                                                                    k  kP 1
 deg Q .OXQ .f  1/; k  kP 1 / D deg Q .OXQ .f  1/; k  kX              /
                                                                    k  kX
                                D deg Q .OXQ .f  1/; k  kX /
                                      X         k  kP 1
                                          log..          /.Q //
                                       
                                                k  kX
                                                   X         k  kX
                                D .Q; f  1/XQ C       log..           /.Q // :
                                                    
                                                             k  k P 1



A bound for log..k  kX =k  kP 1 /.Q // follows by testing on the tautological
section 1, giving

                                                  1
log k1kX .Q / log k1kP 1 .Q / D g .f  1; Q /C log.jf .Q /j2 C1/ :
                                                  2
                      bookcourant     January 8, 2011




190                                                                 CHAPTER 9

Applying Proposition 9.1.4 below at this point shows that
                           1
            g f  1; Q C log jf .Q /j2 C 1
                                                  
                               2
                                   1
                                     Z
                .deg f / sup g C      log.jf j2 C 1/ X :
                          X       2 X
This accounts for the second and third terms in the bound of the theorem.
We are finished once we prove that .Q; f  1/XQ .Q; f  1/X is bounded
by s ms .f / log #k.s/ for a particular choice of XQ . (The usual projec-
    P

tion formula shows that in fact .Q; f  1/XQ is independent of the choice
of XQ .) On any XQ we write f  1 as a sum f  1 D .f  1/hor C .f  1/vert
of a horizontal and a vertical part. Note that .f  1/hor D f  1, with
the Zariski closure now taken in XQ . Since the local intersection multiplic-
ities of Q and f  1 do not go up when passing from X to XQ , we have
.Q; .f  1/hor /XQ D .Q; f  1/XQ  .Q; f  1/X , and thus we are reduced
to proving that, for a particular choice of XQ , .Q; .f  1/vert /XQ is bounded
                 P
from above by s ms .f / log #k.s/.
   We exhibit a specific blow-up, and we calculate which multiplicities f
acquires along the irreducible components of the vertical fibers of this blow-
up. Note that the locus of indeterminacy of f on X consists precisely of
the closed points of X where an irreducible component C from the zero
divisor div.f /C of f on X and an irreducible component C 0 from its po-
lar divisor div.f / meet. Now since by assumption the Zariski closure of
Supp.div.f /C / [ Supp.div.f / / in X is étale over OK , this can only hap-
pen when at least one of C , C 0 is vertical. In points where this happens we
have to perform a sequence of successive blowings-up until a component
arises with multiplicity 0 for f , so that the components with positive multi-
plicities and the components with negative multiplicities are separated from
each other.
   We begin by observing that it will cause no harm if we pass to a finite
extension K ! K 0 . Indeed, both the left-hand side and the right-hand side
of the inequality that we wish to prove get multiplied by ŒK 0 W K if we do
this. Here is why. For the terms .f .Q/; 1/P 1 and .Q; f  1/ the scaling
by a factor ŒK 0 W K follows from general properties of the Arakelov inter-
section product (cf. [Fal1], p. 404, for example). (Note that it is understood
that over K 0 , intersection products are taken on the minimal resolution of
                        bookcourant     January 8, 2011




APPLYING ARAKELOV THEORY                                                   191
                                                P
the pullback of the model X .) That the term  supX g scales by a fac-
tor ŒK 0 W K is obvious. Finally, fix a closed point s of Spec.OK / and let
s 0 be any closed point of Spec.OK 0 / above it. Denoting by es 0 the ramifica-
tion index of s 0 over s and by fs 0 the degree of the residue field extension
of s 0 over s, we see that for any s 0 above s, the integer ms .f / gets multi-
plied by es 0 , and the number log #k.s/ gets multiplied by fs 0 . Using that
                      0                                              0
P
    s 0 es 0 fs 0 D ŒK W K, the sum running over the closed points s above s,
                                       P
we see finally that also the term s ms .f / log #k.s/ gets multiplied by
ŒK 0 W K.
    Starting with X over OK , we first do the following. Let x be a closed
point on X that is the intersection of a vertical component C and a horizon-
tal component C 0 having nonzero multiplicities m and m0 for f that have
different signs. After blowing up in x, we obtain an exceptional divisor E
whose multiplicity for f is mCm0 . We have two distinguished points on E,
one lying on the strict transform of C , and one lying on the strict transform
of C 0 . At exactly one of them there is a sign change for the multiplicities,
or m C m0 D 0. If a sign change happens at the double point lying on the
strict transform of C 0 , then we repeat the process. If a sign change happens
at the double point lying on the strict transform of C or if m C m0 D 0, we
stop, and continue with a new point x 0 , if available.
    We end up with a blow-up X 0 ! X such that an intersection of two ir-
reducible components C , C 0 that have different signs in div.f / on X 0 only
occurs for C , C 0 both vertical. For this, we did not yet need to extend the
ground field K. In order to continue, we note the following. Suppose that
we have a closed point x on the model X 0 of X over OK which is a double
point of a vertical fiber, and two irreducible components C , C 0 of that verti-
cal fiber pass through x, having nonzero multiplicities m and m0 for f that
differ in sign. Assume that K ! K 0 is a Galois extension that ramifies over
the image of x in Spec.OK /, with a ramification index e that is a multiple
of m m0 . In passing to the minimal resolution XQ of XO0 0 , the point x gets
                                                             K
replaced by a chain of e 1 projective lines of self-intersection 2. The mul-
tiplicities of f along these components change in e steps from e m to e m0 ,
so that the steps are m m0 and a multiplicity 0 will appear somewhere,
because m m0 is a divisor of e m.
    Thus we see how we can reach our goal. Take a Galois extension K ! K 0
                      bookcourant     January 8, 2011




192                                                                  CHAPTER 9

that ramifies as specified above over the images in Spec.OK / of the double
points where components meet with a different sign for f . (This is always
possible.) By our remarks above, it suffices to prove the inequality over K 0 .
By construction, the morphism f extends over the model XQ that arises in
this way. Moreover, it follows from the construction that for s 0 a closed point
of Spec.OK 0 / and s its image in Spec.OK / we have ms 0 .f /  es 0 ms .f /.
Hence the sum of the local intersection numbers .Q; .f  1/vert /s 0 for all s 0
over s is bounded from above by ŒK 0 W Kms .f / log #k.s/. This is what we
needed to prove.                                                              

9.1.4 Proposition Let f W X ! P 1 be a finite morphism of Riemann sur-
faces with X connected and of positive genus. Consider on X f 1 f1g
the function
                                      1
               h.x/ D g.f  1; x/ C log.jf .x/j2 C 1/ :
                                      2
Then h extends uniquely to an element of C 1 .X /, also denoted h. For all
x 2 X we have
                                   1
                                      Z
            h.x/  .sup g/ deg f C       log.jf j2 C 1/ X :
                     X             2 X

Proof Let us first show that h extends to a C 1 function on X . In fact, as
the beginning of the proof of Theorem 9.1.3 indicates, h is the logarithm of
the function x 7! kkX .x/=kkP 1 .x/ that gives the quotient of two metrics
on OX .f  1/: the Arakelov metric kkX and the pullback of the Fubini-
Study metric kkP 1 (see 9.1.2). But then h is in C 1 .X /. We have, by (4.4.4),
                                        1
                       Z                               Z
              h.x/ D            g.x; y/ .@@h/y C           h X :
                        y2X             i              X

For s any local holomorphic generator of OX .f  1/ we have
1         1             2    1
   @@h D      @@ log.kskX /      @@ log.ksk2P 1 / D .deg f /X f  P 1 ;
i       2 i               2 i
where P 1 is the curvature form of the Fubini-Study metric on OP 1 .1/.
Substituting this in the previous equality, and using that for all x in X we
     R
have y2X g.x; y/X .y/ D 0, we get
                                                1
                Z                            Z
       h.x/ D          g.x; y/.f  P 1 /y C      log.jf j2 C 1/ X :
                 y2X                          X 2
                        bookcourant       January 8, 2011




APPLYING ARAKELOV THEORY                                                   193

As P 1 is defined as the curvature form of the Fubini-Study metric on
                    R
OP 1 .1/, we have P 1 P 1 D deg.OP 1 .1// D 1. As the metric is in-
variant under the transitive action of SU2 , P 1 is everywhere positive. In
fact, one can compute that P 1 D .i=2/ dz d z=.1 C jzj2 /2 . We end up
with
                                        1
                                          Z
              h.x/  .sup g/ deg f C         log.jf j2 C 1/X
                        X               2 X
as required.                                                                

Proof [Proof of Theorem 9.1.1] In order to simplify our notation, we drop
the subscript l in bl . For P in P 1 .OK / we put

                         h0 .P / D .P; 1/=ŒK W Q:

Then we have h.P /  h0 .P / C 12 log 2, as for all x in C 2 we have

                    jx1 j2 C jx2 j2  2 maxfjx1 j; jx2 jg2 :

In order to bound h0 .b.Qx;i // from above we want to apply Theorem 9.1.3.
It follows from the definition of the morphism b that both the zero divisor
div.b/C and the polar divisor div.b/ of b on Xl have as their support
only K-rational closed points, namely, cusps. In particular, we never have
b.Qx;i / D 1, by construction of Dx00 . We have also seen that the Zariski
closure in X of Supp.Cusps/ is étale over OK (as OK -valued points the
cusps are disjoint), and hence the same holds for the Zariski closure in X of
Supp.div.b/C / [ Supp.div.b/ /. Theorem 9.1.3 now gives us that
                                                         X
          ŒK W Qh0 .b.Qx;i // .Qx;i ; b  1/X C deg b     sup g
                                                                  X
                                      1X
                                         Z
                                  C           log.jbj2 C 1/X
                                    2  X
                                    X
                                  C    ms .b/ log #k.s/;
                                      s

with ms .b/ the supremum of the multiplicities of div.b/ on X along the
irreducible components of the fibers of X at s. We are done if we can
prove that deg b is at most l 2 , and that ms .b/ D 0 for all s. The definition
of b shows directly that its degree is l 2 1 (it is the degree of the natural
                      bookcourant     January 8, 2011




194                                                                  CHAPTER 9

morphism from X1 .5l/ to X1 .5/). Let us now show that ms .b/ D 0 for
all s. For this we evidently need information on the divisor div.b/ on X .
   We start with working over Q.5l /. From the discussion in Section 8.1
we recall that there is a fine moduli scheme Y1 .5l/ZŒ5l  over ZŒ5l  of
elliptic curves with balanced level structure (terminology from [Ka-Ma]).
Let E.5l/ ! Y1 .5l/ZŒ5l  be the universal elliptic curve, and let P5 , Pl
be the tautological points of order 5 and l. From Proposition 8.2.8 we re-
call the elliptic curve E ! Y1 .5/0 with Y1 .5/0 D Spec.ZŒb; 1=discr.E//.
The elliptic curve E.5l/ ! Y1 .5l/ZŒ5l ;1=5 arises from E ! Y1 .5/0 by
a unique base change Y1 .5l/ZŒ5l ;1=5 ! Y1 .5/0 . This gives the regular
function b on Y1 .5l/ZŒ5l ;1=5 . As b is invertible on Y1 .5/0 it is invert-
ible on Y1 .5l/ZŒ5l ;1=5 . We conclude that div.b/ on X1 .5l/ZŒ5l  is a cer-
tain linear combination of the irreducible components of the closed sub-
schemes Cusps and X1 .5l/F5 Œl  . In order to find this linear combination,
we examine the multiplicities of b along the irreducible components that we
have isolated.
   We start with the multiplicities along the irreducible components of the
divisor Cusps. It is sufficient to study the situation over C, and here we can
make a beginning by looking at div.b/ on X1 .5/C . From the equations in
Proposition 8.2.8 we obtain that over the cusp 0 of X0 .5/C lie two cusps,
say c1 and c2 , with c1 , say, corresponding to the 5-gon with the tautological
point of order 5 being on a component adjacent to the connected component
of 0, and the other, c2 , corresponding to the 5-gon with the tautological
point of order 5 being on a component that is not adjacent to the connected
component of 0. We have div.b/ D ˙.c1 c2 / on X1 .5/C ; we could
compute the exact sign, but that is not important for us. The divisor of b on
X1 .5l/C is obtained by pulling back its divisor on X1 .5/C via the forgetful
map X1 .5l/C ! X1 .5/C . Hence, pulling back the divisor c1 c2 we get
plus or minus the divisor of b on X1 .5l/C ; the multiplicities are just the
ramification indices above the cusps c1 and c2 . Since these are in f1; lg, we
obtain that the multiplicities of b along the irreducible components of Cusps
are just 1 or l in absolute value.
   Next we calculate the multiplicities of b along the irreducible components
of X1 .5l/F5 Œl  . The structure of a connected component of the scheme
X1 .5l/F5 Œl  is as follows: it consists of two irreducible components, one
                         bookcourant     January 8, 2011




APPLYING ARAKELOV THEORY                                                      195

on which P5 has order 1, and one having an open part where P5 has order 5.
These two irreducible components intersect (transversally) in the supersin-
gular points.
   We denote by  the union of the irreducible components over F5 on which
P5 has order 1. The construction of the scheme Y1 .5/0 immediately gives
us a forgetful map X1 .5l/ZŒ5l   Supp.Cusps/ ! Y1 .5/0 . Since b is
invertible on Y1 .5/0 , the same holds for b along the irreducible components
of X1 .5l/F5 Œl  , except possibly for the irreducible components in . But
the multiplicity of b along such an irreducible component is then also zero,
as can be seen by the following argument. Let C [ C 0 be a connected com-
ponent of X1 .5l/F5 Œl  , with the irreducible component C corresponding to
P5 having order 1. All the horizontal components of div.b/ on X1 .5l/ZŒ5l 
specialize to C 0 . We know that b has multiplicity 0 along C 0 and hence it
restricts to a nontrivial rational function, also denoted b, on C 0 . The degree
of b on C 0 is zero, or equivalently m.C 0 ; C / C .C 0 ; div.b/hor / D 0, where
m is the multiplicity of b along C . Now, since .C 0 ; div.b/hor / is zero and
.C 0 ; C / isn’t, we get m D 0.
   All in all, we conclude that the absolute values of the multiplicities of the
irreducible components in div.b/ on X1 .5l/ZŒ5l  are bounded by a constant
times l, and that all multiplicities along irreducible components of fibers
over closed points s of Spec.ZŒ5l / are zero. In particular, for all closed
points s we have ms .b/ D 0. This implies in fact that the rational function
                                                   1
b on X1 .5l/ZŒ5l  extends to a morphism to PZ      . As this is a useful fact, we
record it in a Proposition. This completes the proof of Theorem 9.1.1. 

9.1.5 Proposition Let l > 5 be prime a prime number. The rational func-
                                                                           1
tion bl on X1 .5l/ZŒ5l  from Proposition 8.2.9 extends to a morphism to PZ .


9.2 CONTROLLING Dx D0

In this subsection, the hypotheses are as follows (unless stated otherwise).
We let K be a number field, OK its ring of integers, B WD Spec.OK /,
pW X ! B a regular, split semistable curve over B whose generic fiber
X ! Spec K is geometrically irreducible and of genus g  1. We let D be
the closure in X of an effective divisor of degree g (also denoted D) on X .
                      bookcourant     January 8, 2011




196                                                                  CHAPTER 9

We let x be a K-rational torsion point of the Jacobian of X, that is, a torsion
element of Pic.X /, which has the property that there is a unique effective
divisor Dx on X such that x D ŒDx D. Finally, we let P W B ! X be a
section of p, that is, an element of X .B/.
   We denote by ˆx;P the unique finite vertical fractional divisor ˆ (that
is, with rational coefficients that are not necessarily integral) on X such that
.Dx D ˆ; C / D 0 for all irreducible components C of fibers of p,
and such that P .B/ is disjoint from the support of ˆ. It is not difficult
to see that a ˆ satisfying the first condition exists and that it is unique up
to adding multiples of fibers of p (the intersection pairing restricted to the
divisors with support in a fiber is negative semidefinite); see Lemme 6.14.1
of [Mor2]. The second condition removes the ambiguity of adding multiples
of fibers.
   We denote by ıs the number of singular points in the geometric fiber at a
closed point s of B.

9.2.1 Theorem The OB -module R1 p OX .Dx / is a torsion module on B,
and we have:
                                 1                   1X
.Dx ; P / C log #R1 p OX .Dx / C .!X =B ; !X =B / C     ıs log #k.s/
                                 8                   8 s
                1                                1
      D .D; P /    .D C ˆx;P ; D C ˆx;P !X =B / C deg det p !X =B
                2                                2
            XZ                               g
          C         log k#k.Dx Q/   .Q/ C ŒK W Q log.2/:
               X 
                                             2
Here s runs over the closed points of B, and  runs through the complex
embeddings of K.

We derive Theorem 9.2.1 from three lemmas. For the moment we work
in Q ˝Z Pic.X
         c /.

9.2.2 Lemma The admissible line bundles

         OX .Dx D/ ˝ p  P  OX .Dx D/_            and    OX .ˆx;P /

are numerically equivalent. That is, for any admissible line bundle F on X
we have

      .OX .Dx     D/ ˝ p  P  OX .Dx      D/_ ; F / D .OX .ˆx;P /; F /:
                        bookcourant     January 8, 2011




APPLYING ARAKELOV THEORY                                                    197

Proof In this proof we just write ˆ for ˆx;P . We denote the first line
bundle in the lemma by ‰. Since Dx D is torsion, there is a positive
integer N such that ‰ ˝N is trivial on the generic fiber as a classical line
bundle (that is, without taking the metrics into account). We have a canoni-
cal isomorphism P  ‰ Q! OB on B. Combining, we find that ‰ ˝N has a
rational section s with divX .s/ vertical and P  s 7! 1. The latter condition
implies that P intersects to zero with divX .s/ for the Arakelov intersection
product. On the other hand, as p  P  OX .Dx D/_ is trivial on the fibers
of p over finite places of B, we have .N.Dx D/ divX .s/; C / D 0 for
all irreducible components C of fibers of p. Hence in fact ˆ D N1 divX .s/.
To prove the lemma, it suffices now to prove that ‰ ˝N Q! OX .divX .s//
given by s 7! 1, with 1 the tautological section, is an isometry. Because
of admissibility, it suffices to check that this is so when restricted to P ; but
here we get the canonical isomorphism P  ‰ Q! OB . This is indeed an
isometry by the definition of ‰.                                               

9.2.3 Lemma Let X be a compact Riemann surface of genus g  1. Let
D be an effective divisor on X of degree g satisfying h0 .D/ D 1. Then the
determinant of cohomology .OX .D// is identified with H 0 .X; OX .D//.
Further, the formula
                      ı.X /
                              Z
           log k1k C        C    log k#k.D Q/  X .Q/ D 0
                        8      X
holds for the length (with respect to Faltings’ metrization of the determinant
of cohomology) of the tautological section 1 of H 0 .X; OX .D//.

Proof Since h0 .D/ D 1, H 0 .X; OX .D// D C. Therefore, the set of
points Q on X such that h0 .D Q/ > 0 is the support of D. Let Q be
a point outside the support of D. Then h0 .D Q/ D 0. According to
the axioms for the metrization of the determinant of cohomology, the exact
sequence

           0 ! OX .D        Q/ ! OX .D/ ! Q Q OX .D/ ! 0

gives rise to an isometry

  .OX .D// Q! .OX .D           Q// ˝ Q OX .D/
                                   Š O. ‚/ŒOX .D          Q/ ˝ Q OX .D/:
                      bookcourant     January 8, 2011




198                                                                   CHAPTER 9

Taking the norm on left and right of a tautological section we obtain, us-
ing (4.4.6),

            k1k D exp. ı.X /=8/  k#k.D            Q/ 1  G.D; Q/;

where log G.D; Q/ D gD;X .Q/. Taking logarithms and then integrating
against X .Q/ gives the result.                                   

9.2.4 Lemma (Noether formula) We have
                                               X
  12 deg det p !X =B D .!X =B ; !X =B / C          ıs log #k.s/
                                               s
                                           X
                                       C       ı.X /     4gŒK W Q log.2/ ;
                                           

the first sum running over the closed points of B, the second sum running
over the complex embeddings of K.

Proof See [Fal1] and [Mor3].                                                      

Proof [Proof of Theorem 9.2.1] We first show that R1 p OX .Dx / is a tor-
sion module. As it is a coherent OB -module, it suffices to show that it is zero
on the generic point of B, that is, that H1 .X; OX .Dx // is zero. By Riemann-
Roch, we have h0 .Dx / h1 .Dx / D 1. By definition of Dx , we have
OX .Dx / Š Lx .D/. And by construction of D, we have h0 .Lx .D// D 1.
This shows that h1 .Dx / D 0.
   Let us now prove the identity in Theorem 9.2.1. We start by noting that,
by (4.4.7)

                   .Dx    D; P / D deg P  OX .Dx         D/:

By Lemma 9.2.2, OX .Dx / ˝ p  P  OX .Dx D/_ and OX .D C ˆx;P /
are numerically equivalent. The Riemann-Roch theorem then gives

  deg det Rp .OX .Dx / ˝ p  P  OX .Dx        D/_ /
                1
             D .D C ˆx;P ; D C ˆx;P                !X =B / C deg det p !X =B :
                2
                           bookcourant          January 8, 2011




APPLYING ARAKELOV THEORY                                                          199

By the projection formula for the determinant of cohomology we can write
the left-hand side as

  deg det Rp .OX .Dx / ˝ p  P  OX .Dx               D/_ /
                           D deg det Rp OX .Dx /           deg P  OX .Dx     D/ :

Since p OX .Dx / is canonically trivialized by the function 1, we have
                                 X
      deg det Rp OX .Dx / D          log k1k log #R1 p OX .Dx /;
                                       

where for each complex embedding , the norm k1k is the length of the
tautological section 1 of .OX .Dx // D H 0 .OX .Dx //. By Lemma 9.2.3
we can then write
                              XZ
      deg det Rp OX .Dx / D           log k#k .Dx Q/   .Q/
                                          X
                                       X
                                  C         ı.X /=8      log #R1 p OX .Dx / :
                                       

Combining everything gives
                     1
.Dx     D; P / D       .D C ˆx;P ; D C ˆx;P !X =B / deg det p !X =B
                     2 Z
                     X
                   C        log k#k.Dx Q/   .Q/
                            X
                       X
                   C        ı.X /=8       log #R1 p OX .Dx / :
                       
                                                               P
We obtain the required formula upon eliminating                    ı.X /=8 with the
Noether formula, Lemma 9.2.4.                                                         

9.2.5 Theorem We have an upper bound
                                         1
.Dx ; P / C log #R1 p OX .Dx /           .D; D !X =B /
                                         2 X
                                       C 2g 2   ıs log #k.s/
                                                    s2B
                                            X                        g
                                       C            log k#k;sup C     ŒK W Q log.2/
                                                
                                                                     2
                                        1
                                       C deg det p !X =B C .D; P / ;
                                        2
                      bookcourant     January 8, 2011




200                                                                       CHAPTER 9

where s runs through the closed points of B, and where the supremum norm
k#k;sup is taken over Picg 1 .X /.

The required upper bound follows directly from Theorem 9.2.1 by using
Lemma 9.2.6 below and the fact that .!X =B ; !X =B /  0 (see Theorem 5
of [Fal1]).

9.2.6 Lemma We have an upper bound

      1
        .D C ˆx;P ; D C ˆx;P        !X =B /
      2
                                1                              X
                                 .D; D       !X =B / C 2g 2         ıs log #k.s/ ;
                                2
                                                               s2B

with s running through the closed points of B.

Proof In this proof we just write ˆ for ˆx;P . By the definition of ˆ, we
have .Dx D ˆ; ˆ/ D 0, or, in other words, .ˆ; ˆ/ D .Dx D; ˆ/.
Using this we can write
  1                               1                   1
    .DCˆ; DCˆ !X =B / D             .D; D !X =B /C .ˆ; !X =B D Dx / :
  2                               2                   2
                  P
We write ˆ D         C ˆ.C /  C , and for any finite fiber Fs of p we put
As WD supC jˆ.C /j with C running through the irreducible components
of Fs . Since !X =B ; D and Dx intersect any irreducible component C with
non-negative multiplicity, we find
                                                                   !
        1                           1 X
          .ˆ; !X =B D Dx /                As Fs ; !X =B C D C Dx
        2                           2 s
                                      X
                                 2g      As log #k.s/ :
                                          s

We are going to prove that As  gıs , and then we are done. So let s be a
finite place of B. Let S0 be the set of irreducible components of Fs , and let
S1 be the set of double points on Fs . Let s be the dual graph of Fs (thus, the
set of vertices of s corresponds to S0 , the set of edges corresponds to S1 ,
and the graph is defined by the incidence relations). Choose an orientation
on s . This gives rise to the usual source and target maps s and tW S1 ! S0 .
Consider the boundary and coboundary maps d D t s W QS1 ! QS0
                        bookcourant     January 8, 2011




APPLYING ARAKELOV THEORY                                                   201

and d  D t  s  W QS0 ! QS1 . Then d d  W QS0 ! QS0 is given by
minus the intersection matrix of Fs . In particular, the map d d  sends ˆ to
the map uW C 7! .ˆ; C / D .D Dx ; C /. The kernel of d d  consists
exactly of the constant functions, and the image consists of the orthogonal
complement of the constant functions. Now consider the graph s as an
electric circuit, where each edge has a resistance of 1 ohm. By Ohm’s law
and by spelling out the maps d and d  we see that if we let at each vertex C
a current of u.C / amperes enter the circuit, subject to the condition that
P
   C u.C / D 0, the potentials '.C / at each vertex C will be given, up to
addition of a constant function, by a solution of the equation d d  ' D u.
Hence ˆ is the potential corresponding to the current C 7! .D Dx ; C /,
normalized by the condition that ˆ.CP / D 0 with CP the component that
P specializes to. We must bound the jˆ.C /j for C varying over S0 . The
worst case that may happen is that s is a chain, with D 0 and D specializing
entirely to the beginning and end point, respectively. In this case, the biggest
potential difference is g  .#S0 1/ in absolute value, so that we arrive at
jˆ.C /j  g  .#S0 1/. Now note that s is connected and that X=K has
split semistable reduction. This gives #S0 1  ıs and hence jˆ.C /j  gıs ,
as required.                                                                  
bookcourant   January 8, 2011
                        bookcourant     January 8, 2011





Lines 11607-11753
11.4 BOUNDS FOR INTERSECTION NUMBERS ON X1 .pl/

In this section, we will bound the intersection numbers occurring in the
right-hand side of the inequality in Theorem 9.2.5, in the situation described
in Section 8.2.

11.4.1 Theorem Let p and l be two distinct prime numbers, both at least 5,
and let X be the semistable model over B WD Spec ZŒpl  that is provided
by [Ka-Ma]. For two cusps P and Q (possibly equal) in X .B/ we have

                .P; P /  0;     and    j.P; Q/j D O..pl/7 /:

For a cuspidal effective divisor D of degree g on X we have

                      j.D; D     !X =B /j D O..pl/11 /:

Proof As p and l are at least 5, the genus of X1 .pl/ is at least two. By the
adjunction formula (see (4.4.8)). we have .P; P / D .P; !X =B /, and by
[Fal1], Theorem 5, we have .P; !X =B /  0, hence .P; P /  0.
  Let us now derive an upper bound for .P; !X =B /. As the automorphism
group of X over B preserves the Arakelov intersection product on X and
acts transitively on the cusps, it suffices to do this for the standard cusp 1.
The Fourier expansion at 1 of the rational function j on X is of the form
j D 1=q C f with f 2 ZŒŒq. Therefore, 1=j is regular in a neighborhood
                      bookcourant     January 8, 2011




242                                                                 CHAPTER 11

of 1, and has a zero of order one along 1. It follows that d.1=j / generates
1 !X =B , and d.1=j / D dq in 1 !X =B . By definition of the Arakelov
intersection product and Theorem 11.3.1 we then have

        .1; !X =B / D    ŒQ.pl // W Q log kdqkAr .1/ D O..pl/7 /:

We now know j.P; P /j D O..pl/7 / for all cusps P in X .B/. We will
now show that j.P; Q/j D O..pl/7 /. By the Manin-Drinfeld Theorem,
see [Dri], the image of the divisor P Q in J1 .pl/.Q.pl // is of finite
order. Let ˆ be a vertical fractional divisor such that for any irreducible
component C of a fiber of X over B we have .P Q ˆ; C / D 0. By
[Hri] or Theorem 4 of [Fal1] we have .P Q ˆ; P Q ˆ/ D 0.
Equivalently, we have

                2.P; Q/ D .P; P / C .Q; Q/        .P    Q; ˆ/:

The term .P Q; ˆ/ can be dealt with by the method used in the proof of
Lemma 9.2.6. We work this out in this special situation. We make ˆ unique
by demanding that its support be disjoint from P . Of course, this does
not change the number .P Q; ˆ/, but it makes it easier to talk about ˆ.
The support of ˆ is contained in the reducible fibers. These are exactly
the fibers in the characteristics p and l. Let us estimate the contribution at
the prime p. We have to sum over the maximal ideals of the Fp -algebra
Fp Œx=.x l 1 C    C 1/. All residue fields of this algebra are isomorphic to
a finite extension F of Fp , and the number of them is .l 1/= dimFp F . Let
XF be the fiber at one of these residue fields, and let ˆF be the part of ˆ that
has support in XF . Then XF is the union of two irreducible components I
and I 0 , with transversal intersection at the supersingular points. The number
of Fp -valued supersingular points is given by

                                                 .p        1/.l 2   1/
        s WD #XF .Fp /s:s: D # X1 .l/.Fp /s:s: D
                                              
                                                                         :
                                                            24
The degree on I of the restriction to it of OX .I 0 / is s, and, symmetrically,
degI 0 OX .I / D s. As I C I 0 D XF is a principal divisor in a neighborhood
of XF , the restrictions of OX .I C I 0 / to I and I 0 are trivial, and we have
degI OX .I / D s and degI 0 OX .I 0 / D s. It follows that ˆF is one of the
following fractional divisors: ˆF D 0 if P and Q specialize to points on
                            bookcourant        January 8, 2011




BOUNDS FOR ARAKELOV INVARIANTS OF MODULAR CURVES                           243

the same irreducible component of XF ; ˆF D .1=s/I if P specializes to a
point on I 0 and Q to a point on I ; ˆF D .1=s/I 0 if P specializes to a point
on I and Q to a point on I 0 . If we denote by .P Q; ˆ/F the contribution
to .P Q; ˆ/ at the fiber XF , we have

                          j.P      Q; ˆ/F j  .2=s/ log #F :

Summing this over the residue fields of Fp Œx=.x l 1 C    C 1/ gives, for
the contribution .P Q; ˆ/p to .P Q; ˆ/ at p,
                                     l 1     2             48 log p
         j.P         Q; ˆ/p j                log #F D              :
                                  dimFp .F / s           .p 1/.l C 1/
Likewise, we have, for the contribution at l to .P           Q; ˆ/,
                                                    48 log l
                          j.P     Q; ˆ/l j                    :
                                               .l    1/.p C 1/
So, finally,
                                      48 log l    48 log p
               j.P      Q; ˆ/j                C             :
                                   .l 1/.p C 1/ .p 1/.l C 1/
The estimate j.P; Q/j D O..pl/7 / now follows.
  To get to the second statement of the theorem, note that

               .D; D      !X =B / D .D; D C !X =B / 2.D; !X =B /
                                    X
                                  D    .Pk ; Pl / 2.D; !X =B /;
                                      k¤l

where D D P1 C    C Pg , with repetitions allowed. By our previous
estimates, we get j.D; D !X =B /j D O.g 2 .pl/7 / D O..pl/11 /.    

We will also need a lower bound for the intersection number of two distinct
points on X1 .pl/.

11.4.2 Theorem There is an integer c such that for all pairs of distinct
primes p and l such that X1 .pl/ has genus at least one, for any extension
K of Q.5l /, and for P and Q distinct points in X1 .pl/.K/ we have
                                   1
                                        .P; Q/  c.pl/6 ;
                                ŒK W Q
where .P; Q/ is the Arakelov intersection number of P and Q on the mini-
mal regular model of X1 .pl/ over OK .
                       bookcourant     January 8, 2011




244                                                                  CHAPTER 11

Proof We have

                      .P; Q/ D .P; Q/fin C .P; Q/1 ;

with .P; Q/fin the contribution from the finite places of K, and .P; Q/1 the
contribution from the infinite places. As P ¤ Q, we have .P; Q/fin  0.
On the other hand, we have
                                   X
                      .P; Q/1 D           g .P ; Q /:
                                      

By Theorem 11.3.1 we have

                            g .P ; Q /  c.pl/6

for some absolute constant c. This finishes the proof.                         


11.5 A BOUND FOR h.xl0 .Q// IN TERMS OF h.bl .Q//


Lines 11834-11980
11.6 AN INTEGRAL OVER X1 .5l/

In this section we will give an upper bound for the integral appearing in the
estimate in Theorem 9.1.1. We recall the situation: l is a prime number with
l > 5, and b is the regular function on Y1 .5/Q given by Proposition 8.2.8.
We also view b as a regular function bl on Y1 .5l/Q via pullback along the
map Y1 .5l/Q ! Y1 .5/Q that sends .E=S; P5 ; Pl / to .E=S; P5 /, where S
is any Q-scheme, E=S an elliptic curve, P5 in E.S / everywhere of order 5,
and Pl in E.S / everywhere of order l.

11.6.1 Proposition There exist real numbers A and B such that for all
primes l > 5,
                Z
                         log.jbl j2 C 1/   A C B  l 6 ;
                  X1 .5l/.C/

where  is the Arakelov .1; 1/-form.

Proof In order to simplify the notation in the proof, we will let X1 .5l/
denote the Riemann surface X1 .5l/Q .C/ of complex points of the curve
X1 .5l/Q over Q, and we will drop the subscript l in bl . We will denote
points of Y1 .5l/ as triples .E; P5 ; Pl /, with E a complex elliptic curve with
points P5 of order 5 and Pl of order l. Similarly, we will denote points of
Y1 .5/ by pairs .E; P /, and points on the j -line just by elliptic curves.
   The equations in Proposition 8.2.8 show that the rational function b on
X1 .5/ has exactly one pole, that it is of order one, and that at that point the
function j W X1 .5/ ! P 1 has a pole of order 5. The region in H consist-
ing of the  with =. / > 1 gives an embedding of the disk D.0; e 2 /
into the j -line, sending q ¤ 0 to C  =q Z . The inverse image of this
disk under j W X1 .5/ ! P 1 consists of 4 disks, one around each cusp.
The two disks around the cusps where j is ramified are given by the em-
beddings D.0; e 2=5 / ! X1 .5/, sending q ¤ 0 to .C  =q 5Z ; q/ and to
.C  =q 5Z ; q 2 /. As the integral in the proposition that we are proving does
                         bookcourant      January 8, 2011




BOUNDS FOR ARAKELOV INVARIANTS OF MODULAR CURVES                              247

not change if we replace b by its image under a diamond operator hai with
a 2 F5 , we may and do suppose that b has its pole at the center of the
punctured disk

            U D f.C  =q 5Z ; q/ W q 2 D.0; e 2=5 / g  X1 .5/ :

The integral of log.jbj2 C 1/ over the complement of the inverse image of
U in X1 .5l/ is bounded by the supremum of log.jbj2 C 1/ on X1 .5/ U .
This upper bound does not depend on l. Hence it is enough to prove that the
integral of log.jbj2 C 1/ over the inverse image of U in X1 .5l/ is bounded
by B l 6 , for a suitable B. Now this inverse image of U is a union of 2.l 1/
punctured disks Uc and Vd , with c and d running through Fl given by

                Uc D f.C  =q 5Z ; q; lc / W q 2 D.0; e 2=5 / g

and

             Vd D f.C  =q 5lZ ; q l ; q 5d / W q 2 D.0; e 2=5l / g :

For each c in Fl the map X1 .5l/ ! X1 .5/ restricts to the isomorphism
Uc ! U given by q 7! q. For each d in Fl , the restriction Vd ! U is
given by q 7! q l .
   Around the standard unramified cusp of X1 .5l/ we have the punctured
disk

               Wl D f.C  =q Z ; 5 ; l / W q 2 D.0; e 2=5 / g:

By applying a suitable element from the group of automorphisms of X1 .5l/
generated by the Atkin-Lehner pseudo-involutions and the diamond opera-
tors we can establish isomorphisms of the Uc with Wl .
   The point .C  =q 5Z ; q; lc / in Uc is then first sent to .C  =q 5Z ; q; l /
by hc 1 i, and then to .C  =q Z ; 5 ; l / by the Atkin-Lehner pseudo-involu-
tion that divides out by the group generated by the point of order 5 (see
Definition 2.5.14). The coordinate q on Wl is then identified in this way
with the coordinate q on Uc . We observe that  is invariant under each
automorphism of X1 .5l/. Lemma 11.3.7 gives a real number C1 such that
for all l and c, the positive real .1; 1/-form  on Uc can be estimated from
above by
                                        i
                             jUc  C1  dqd q :
                                        2
                        bookcourant      January 8, 2011




248                                                                     CHAPTER 11

Similarly, for each d in Fl a suitable automorphism of X1 .5l/ maps Vd to
the punctured disk Wl0 :

               Wl0 D f.C  =q Z ; 5 ; l / W q 2 D.0; e 2=5l / g :

Lemma 11.3.7 gives a real number C2 such that for all l and d , the positive
real .1; 1/-form  on Vd can be estimated from above by

                                            1           i
                     jVd  C2             2=5l /4
                                                        dqd q :
                                   .1   e               2

Now the function qb on U extends to a holomorphic function on a disk
containing U , hence jqbj is bounded on U . Hence there is a real number
C3 > 1 such that jbj2 C 1  C3 jq 2 j on U . It follows that on all Uc we
have jbj2 C 1  C3 jq 2 j, and that on all Vd we have jbj2 C 1  C3 jq 2l j
(note that under Vd ! U , .C  =q 5lZ ; q l ; q 5d / is sent to .C  =q 5lZ ; q l /).
We remark that 1=.1 e x / D x 1 .1 C O.x// as x tends to 0 from above.
Hence there is a C4 2 R such that for all l,

                                    1
                                                 C4 l 4 :
                            .1    e 2=5l /4

We get, for all l:
   Z
        log.jbj2 C 1/ 
      b   1U

                                                i
              Z
    .l 1/C1                  log.C3 jq 2 j/  dqd q
                 D.0;e 2=5 /                   2
                          1                                             i
                                   Z
                                                                2l
     C .l 1/C2                                    log.C  3 jq     j/    dqd q
                   .1 e 2=5l /4 D.0;e 2=5l /                          2
     Z                                                         i
            lC1 log.C3 jzj 2 / C C2 C4 l 5 log.C3 jzj 2l / dzd z
      jzj<1                                                       2
                                                                i
     Z
             C1 l log.C3 jzj 2 / C C2 C4 l 6 log.C3 jzj 2 / dzd z
                                                              
   
      jzj<1                                                     2
   D .C1 l C C2 C4 l 6 /. log C3 C / :

This finishes the proof of Proposition 11.6.1                                     
                         bookcourant      January 8, 2011




BOUNDS FOR ARAKELOV INVARIANTS OF MODULAR CURVES                               249

11.7 FINAL ESTIMATES OF THE ARAKELOV CONTRIBUTION

Lines 11980-12100
11.7 FINAL ESTIMATES OF THE ARAKELOV CONTRIBUTION

We will now put the estimates of the preceding sections together, in the sit-
uation of Section 8.2. We briefly recall this situation. We have a prime
number l > 5, and let Xl denote the modular curve X1 .5l/ over Q, and gl
its genus. The Jacobian variety of Xl is denoted by Jl . In Jl .Q/Œl we have
the Gal.Q=Q/-module V that realizes the representation  from Gal.Q=Q/
to GL2 .F / attached to a surjective ring morphism f W T .1; k/  F such
that the image of  contains SL2 .F /. We have an effective divisor D0
on Xl;Q.l / , of degree gl , supported on the cusps. For every x in V there
is a unique effective divisor Dx D Qx;1 C    C Qx;gl of degree gl such
                                                                      cusp
that x is the class of Dx D0 . We have written Dx D Dxfin C Dx , where
   cusp
Dx is the part of Dx supported on the cusps. The numbering of the Qx;i
is such that Dxfin D Qx;1 C    C Qx;dx . We have morphisms bl and xl0
                  1
from Xl;Q to PQ     that, seen as rational functions, have their poles contained
in the set of cusps of Xl .
   The following proposition gives upper bounds for the absolute heights of
the algebraic numbers bl .Qx;i / and xl0 .Qx;i /, polynomial in l. The height
function h used here is as defined in (4.1.6). The proof of the proposition
combines the involved arguments of the previous sections.

11.7.1 Proposition There is an integer c such that for all x in V as above,
and for all i 2 f1; : : : ; dx g, the absolute heights of bl .Qx;i / and xl0 .Qx;i /
are bounded from above by cl 12 .

Proof We will write just b for bl . Let V be as in the proposition. The-
orem 9.1.1 shows that for all x 2 V , all i 2 f1; : : : ; dx g, and all number
fields K containing Q.5l / over which Qx;i is rational, we have
.11:7:2/
                     1                            X
    h.b.Qx;i //            .Qx;i ; b  1/X C l 2     sup g
                  ŒK W Q                           X
                                                               !
                               1X                                   1
                                      Z
                             C            log.jbj2 C 1/X C log 2 :
                               2  X                               2

Here X is the minimal regular model of Xl over B WD Spec OK .
  Let us first concentrate on the second and third terms of the right-hand
                       bookcourant     January 8, 2011




250                                                                  CHAPTER 11

side of (11.7.2). Theorem 11.3.1 gives an integer c1 such that for all 
we have supX g  c1 l 6 , uniformly in all l. Proposition 11.6.1 gives an
integer c2 such that for all  we have .1=2/ X log.jbj2 C 1/X  c2 l 6 ,
                                               R

uniformly in all l. Hence, for all x 2 V , all i 2 f1; : : : ; dx g and all number
fields K containing Q.5l / over which Qx;i is rational, we have
                                  1
.11:7:3/       h.b.Qx;i //            .Qx;i ; b  1/X C c1 l 8 C c2 l 6 ;
                               ŒK W Q
uniformly in all l and V .
   We now concentrate on the first term. We recall that b  1 is an effective
cuspidal divisor on Xl . Let x be in V . We apply Theorem 9.2.5, where (in
the notation of that theorem) we assume that all Qx;i (i 2 f1; : : : ; gl g) are
K-rational, K contains Q.5l /, and P is a cusp. We also use the obvious
fact that log #R1 p OX .Dx / is nonnegative. That gives

  .Dx ; P /      1          1                         X
                             .D0 ; D0 !X =B / C 2gl2     ıs log #k.s/
  ŒK W Q     ŒK W Q       2
                                                      s2B
                             X                 gl
                           C     log k#k;sup C ŒK W Q log.2/
                               
                                               2
                                                                     
                                        1
                                      C deg det p !X =B C .D0 ; P / :
                                        2
Theorem 11.4.1, applied with B D Spec.ZŒ5l /, gives
                      1
                           j.D0 ; D0     !X =B /j D O.l 10 /;
                   ŒK W Q
and
                            1
                                 j.D0 ; P /j D O.l 8 /;
                         ŒK W Q
as D0 is an effective cuspidal divisor of degree gl and gl D O.l 2 /. By
Theorem 11.2.1 we have
                       1    X
                                log k#k;sup D O.l 6 /:
                    ŒK W Q 

By Theorem 11.1.7 we have
                      1
                           deg det p !X =B D O.l 2 log l/:
                   ŒK W Q
                        bookcourant       January 8, 2011




BOUNDS FOR ARAKELOV INVARIANTS OF MODULAR CURVES                           251

Finally, we have

                        gl2    X
                                     ıs log #k.s/ D O.l 6 /;
                     ŒK W Q
                               s2B

by the following argument. The only nontrivial contributions come from
s over 5 and over l. The total contribution at 5 is independent of which
extension K of Q.5 / we use, and for Q.5 / there is only one s over 5,
k.s/ D F5 , and ıs equals the number of supersingular points in X1 .l/.F 5 /,
which is O.l 2 /. The contribution from l can be computed over Q.l /. Then
there is one s, and k.s/ D Fl , and ıs is the number of supersingular points
in X1 .5/.F l /, which is O.l/ (see Section 8.1).
   Putting these last estimates together, we get that there is an integer c3
such that for all l and x we have
                            1