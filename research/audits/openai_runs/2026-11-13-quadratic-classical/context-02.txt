# Primary source, Bosma and Stevenhagen 1996
URL: https://jtnb.centre-mersenne.org/item/10.5802/jtnb.170.pdf
Downloaded original scanned PDF; pdftotext OCR omits some displayed formulas. Do NOT invent missing formulas; flag anything depending on them. Parent will check page images.

J OURNAL DE T HÉORIE DES N OMBRES DE B ORDEAUX




 W IEB B OSMA
 P ETER S TEVENHAGEN
 On the computation of quadratic 2-class groups
 Journal de Théorie des Nombres de Bordeaux, tome                       8, no 2 (1996),
 p. 283-313
 <http://www.numdam.org/item?id=JTNB_1996__8_2_283_0>




     © Université Bordeaux 1, 1996, tous droits réservés.
     L’accès aux archives de la revue « Journal de Théorie des Nombres
     de Bordeaux » (http://jtnb.cedram.org/) implique l’accord avec les condi-
     tions générales d’utilisation (http://www.numdam.org/conditions). Toute uti-
     lisation commerciale ou impression systématique est constitutive d’une
     infraction pénale. Toute copie ou impression de ce fichier doit conte-
     nir la présente mention de copyright.




                       Article numérisé dans le cadre du programme
                     Numérisation de documents anciens mathématiques
                                  http://www.numdam.org/
                           283



           On the computation of quadratic 2-class groups




               par WIEB BOSMA ET PETER STEVENHAGEN


     RÉSUMÉ. Nous décrivons un algorithme dû à Gauss, Shanks et Lagarias qui
     étant donné un entier D ~ 0,1 mod 4 non carré et la factorisation de D,
     détermine la structure du 2-sous-groupe de Sylow du groupe des classes de
     l’ordre quadratique de déterminant D ; la complexité de cet algorithme est
     en   temps polynomial probabiliste en log|D|.

     ABSTRACT. We describe an algorithm due to Gauss, Shanks and Lagarias
     that, given a non-square integer D ~ 0, 1 mod 4 and the factorization of D,
     computes the structure of the 2-Sylow subgroup of the class group of the
     quadratic order of discriminant D in random polynomial time in log |D|.




1. Introduction.
Let D = o, I mod 4 be a non-square integer, and denote by Cl(D) the strict
class group of the quadratic order O Z[(D +  =
                                                       B/D)/2]  of discriminant D.
The group Cl(D) may be identified with the class group of primitive integral
binary quadratic forms of discriminant D, and this yields a description that
is very useful for explicit computations. There do exist algorithms that
compute CI(D) in a time that is subexponential in the length log D of the
input; see [3] and [5, 7] for the respective cases D &#x3E; 0 and D 0. However,
these algorithms are far from polynomial-time, and it is unlikely that they
will be used in the near future for discriminants D having more than, say,
50 decimal digits.
   The algorithm in this paper only computes the 2-Sylow subgroup C(D) =
CI(D)2 of the class group. It runs in random polynomial time [8, j] if the
factorization of D is given as part of the input, and it handles most 50-
digit discriminants in a matter of seconds. In contrast to the situation
for algorithms that compute the full class group C1(D), it turns out that
not only the size of D, but also the number of prime factors of D and the

   Class. Math. : Primary 11Y40, 11R11; Secondary 11E16, 11E20.
   Mots-clés : Quadratic 2-class groups, binary and ternary quadratic forms.
                _


                                 -   _   ,                  -




   Manuscrit reçu le 29 janvier 1996
284


’depth’ of the resulting class group greatly influence the running time. For
instance, consider the 501-digit discriminant


which is the product of five primes exceeding 101°° that are 1 mod 4 and
squares modulo each other. It is chosen in such a way that C(D) ~ C4 X C128
has high 4-rank. It takes less than a second to find the elementary abelian
2-groups C(173. D~ ^-_’ Cfl t3£ C( -43. D). Now consider the sample of 2-class
groups




with approximate timings on a Sun MP670 workstation indicated in brack-
ets. We see that the algorithm takes more time if the resulting 2-class
group is ’further’ from elementary 2-abelian, and that the real quadratic
case D &#x3E; 0 appears to be somewhat harder than the imaginary quadratic
case. We will give a complete quantitative explanation for both obser-
vations. Note that computation of the full class group for any of these
discriminants is currently completely unfeasible.
   The basis of our algorithm is a method to solve the duplication equation
2x    c in quadratic class groups that is due to Gauss [6, section 286}. It has
      =


been implemented and used to compute various imaginary quadratic 2-class
groups C(D) by Shanks D. All of Shanks’s examples were cyclic or almost
cyclic, and he did not give an algorithm to handle general D. Doing so is
essentially a matter of linear algebra, as was shown by Lagarias [], who ana-
lyzed the algorithm from the point of view of its computational complexity
but referred to [] for a practical implementation. There does not seem to be
a complete description of the mathematical content of the algorithm in the

existing literature, and this paper intends to fill this gap. It turns out that a
careful description of the mathematics leads to something which is not too
far from an actual implementation in a high level programming language
like that of                   Moreover, it naturally yields an algorithm that in-
cludes the improvements of Shanks regarding the Gaussian solution of the
duplication equation and avoids the unnecessary coprimality assumptions
on the first coeB&#x26;cients of the quadratic forms in U.
                                                                             285


   The algorithm has been successfully exploited [] in the verification of the
heuristics of the second author [9, ] regarding the solvability in integers of
the negative Pell equation x2 - dy2 = -1. This verification involved the
computation of C(D) for several millions of large, highly non-cyclic real
quadratic 2-class groups.
   The description of the actual algorithm is contained in section 3 of this
paper. It is preceded by a summary of the basic results on binary quadratic
forms and followed by a worked example illustrating some technical points
of the algorithm. The algorithm itself is essentially a matter of linear
algebra once one knows how to generate the 2-torsion subgroup of CI(D)
and how to solve the equation 2x c for elements c in the principal genus
                                    =



2Cl(D). The ’division-by-2-algorithm’ used in solving 2x c is based on
                                                               =


the reduction theory of ternary quadratic forms. As this reduction theory
is considerably less well known than the corresponding theory for binary
quadratic forms, a concise description of it has been included as section 5. It
is used in section 6, which deals with the solution of the duplication equation
that forms the backbone of the algorithm. A final section 7 comments on
the performance of the algorithm.
   We thank Andreas Meyer for detecting a number of typos in an earlier
version of this paper.




2.  Quadratic class groups.
Let D = 0,1 mod 4 be an integer that is not a square. The class group
CI(D) of discriminant D is defined to be the quotient of the group of in-
vertible ideals of the quadratic order C~D Z[(D+B/D)/2] by the subgroup
                                            =


of principal ideals having a totally positive generator. Note that the posi-
tivity requirement is automatically fulfilled for negative D, and that CI(D)
is the (strict) class group of the quadratic field Q( m) if D is fundamental,
i.e., if D is the discriminant of the field C~(~).
   The relative ease with which one can perform computations in CI(D)
comes from an alternative    description in terms of binary quadratic forms
which is due to Gauss. Consider the set .~D of primitive integral binary
quadratic forms of discriminant D, i.e., forms Q = (a, b, c) ax 2 +bxy+cy 2
                                                              =


in two variabIes x, y with coefficients a, b, c E Z that satisfy gcd(a, b, c) = 1
and b2 - 4ac D. For D 0, we require in addition that a is positive.
               =


The group SL2 (Z) of integral 2 x 2-matrices of determinant 1 has a natural
right action on FD defined by QS(x, y) Q(sx + ty, ux + vy) for S
                                             =                                 =



        SL2(Z), and the orbit space                    maps bijectively to the
286


group Cl(D) under the map



The power of ~ in the map above is only there to ’preserve orientation’
and vanishes for negative D. By transport of structure, XD /SL(Z) be-
comes a group that we identify with CI{D) . Accordingly, we speak of the
class rather than of the orbit of a form in Cl(D) . In the case that D is a
square, which we have excluded so far, the orbit space                can be
made into a group by Gauss’s original method that we will discuss later
in this section. Following Gauss [6, end of section 249], we will write the
group operation in C1(D) additively. This appears to be the most conve-
nient notation for computational purposes, as most computations in class
groups use techniques coming from linear algebra, and it is in line with the
common usage to treat divisor class groups as additive objects.

   As the forms (a, b, c) and (a, b + 2ka, c + kb -I-1~2a) are in the same class
for all k E Z, every class contains a form (a, b, c) with bi ~          It is not
hard to show [2, propositions 5.3.4 and 5.6.3] that every class contains a
quadratic form (a, b, c) with


so it  follows that CI(D) is finite for all D, square or not. Given a form
in       one can efficiently compute [8] a unimodular transformation that
reduces this form to one of the finitely many forms (a, b, c) satisfying lbl
jai     .JiDi73.  However, it is not in general possible to decide efficiently
whether two quadratic forms are in the same class in Cl(D). This is a
serious difEculty that prevents us from working directly in the class group
itself. Instead, one has a finite set of reduced forms 4DD that maps surjec-
tively to the class group Cl(D), and one works with these reduced forms
as representatives of the classes of Cl(D). For D          0, an appropriate def-
inition of reduced forms ensures that the map lb D - Cl(D) is a bijection
and the situation is perfectly satisfactory. For D &#x3E; 0 however, there are
usually many reduced forms mapping to the same class in CI(D), and in
this case an arbitrary form in           can be efficiently reduced to a form in

q.D,  but  not to an element     of Cl(D). As an example, one can think of the
form (-l, 0, d) for d &#x3E; 0 that represents the unit element in Cl(4d) if and
only if the negative Pell equation x2 - dy2 -1 is solvable in integers.
                                                =


This example is of fundamental importance in 0.
   In the case of non-square discriminants D, our map shows that the prin-
cipal form (1,0, -D/4) (for even D) or (1, l, (1 - D)/4) (for odd D) maps
                                                                            287


to the unit element in Cl(D). The opposite form (a, -b, c) of (a, b, c) is
the inverse of the class of (a, b, c) as it maps to the conjugate ideal class
in Cl(D). If we work out how the multiplication of ideals translates into
a composition formula for quadratic forms, we find [2, 5.4.6] that the sum
of the classes of the primitive quadratic forms (a,, bi, cl) and (a2, b2, C2) in
CI(D) contains a form (a3, b3, C3) satisfying




It was shown by Dirichlet that the forms can be chosen in such a way
inside their equivalence class that one only needs to perform compositions
for which d = 1, known as compositions of ’concordant forms’. In fact, it
suffices [4, lemma 3.2] to have a composition of concordant forms (al, b, cl)
and (a2, b, C2) having the same middle coefficient b that satisfies b2 -= D mod
4ala2- In this situation, one has ci  =     and c2   =      for some integer c,
and (2.2) yields an identity


that is known as Dirichlet composition of forms.
   Together with the reduction of arbitrary forms to forms in a finite set
     the composition formulae provide us with a computational model for
the class group. More precisely, there is for each D a finite set 4~D of
reduced forms of discriminant D that is usually too large to be enumerated.
Given a form F E        one can efficiently find some form Fred E 40D that
is in the same class. Given              tPD, the composition formula (2.2)
makes it possible to compute efficiently a reduced form F3     =
                                                                 Fi o F2 E q. D
whose class in CI(D) is the sum of the classes of Fl and F2. The opposite
of a reduced form is trivially computed, so we can perform the ’group
operations’ of CI(D) on the level of       However, since equivalence cannot
be tested efficiently when D is large and positive, passing from 16 D to Cl(D)
is an entirely non-trivial matter. It is exactly this complication which
led Shanks [, p. 849] to believe that one cannot always decide efficiently
whether certain 2-torsion classes in CI(D) are actually trivial. We will come
back to this problem, which will turn out ot be non-existent, in section 3.
The ambiguity between forms and their classes will however necessitate a
careful formulation of our algorithm in section 3, where we compute the
2-primary part of CI(D) while working with representing forms.
   As we will be interested in duplication in the class group in later sections,
we mention the   following important example of concordant composition.
288


2.4. DUPLICATION LEMMA. Let                 be a form of discriminant D with
gcd(a, b)   = 1.
                 If A, v E Z satisfy Aa +  vb =
                                                 1, then we have 2[(a, b, c)] =
[(a2, b - 2vac, c’)] E CI(D) for    some  integer c’. In particular, we have
2j(a, b, c)~ I(a2,b,c/a)] if a divides c.
                =                                                             E3

This lemma can be used in the opposite direction to solve the equation
2(PJ [Q] for a form Q that represents a square k2 coprime to 2D. Indeed,
        =



suppose we have Q(u, v)       k2 for certain u, v E Z, and assume without loss
                                 =


of generality that u and v are coprime. Transforming Q by a unimodular
                  we obtain an equivalent form Qs satisfying           0) k2,
matrix S     =
                    ~vt~,                                                   =



so we have Qs       (k2, l, m) for certain l, E
                        =                      m     Z. The  form (k, l, km) of
discriminant l2 4k2m D is primitive since gcd(k, l) gcd(k, 2D) 1,
                       -
                                =                             =              =


and the duplication lemma shows that we have 2((k, l, km)] = [(k2, l, n)]        =



IQ] -
    In section 6, we will employ the original description of Gauss of the
group structure on Cl(D), which is quite different from the one we have
given above and also works for square discriminants. In this description, a
form Q (a3, b3, c3) of discriminant D is the composition of two primitive
            =



quadratic forms (a,, bl, cl) and (a2, b2, C2) of discriminant D if there exist
bilinear relations




over Z that         yield the identity




and satisfy an ’orientability condition’ that distinguishes the forms       bi, cl)
and (a2, b2, C2) in (2.5) from their opposite forms (al, -bl, cl) and (a2, -b2, C2) -
Write                                   I       I




for the subdeterminants of our bilinear relations. An elementary computa-
tion [4, exercise 3.1] shows that if (2.5) holds for a form Q of discriminant D,
then we necessarily have 612 tai and 613 ~a2. The orientability con-
                                     =           =


dition is that the +-sign holds in both cases. Note that the preceding defi-
nition for the composition of forms is indeed defined on SL2(Z)-equlvalence
classes.
                                                                             289


  If Q is a composition as specified above, the determinants 6jj satisfy




and the coefficients of Q are




Conversely, given primitive forms Q, (al,b1,cI) and Q2
                                            =
                                                                    (a2, b2, c2)
                                                                    =


and integers Si, ti for which (2.6) and (2.7) hold, we have bi - 4a,cl = b2 -
4aZC2   = D for some discriminant D and ((a3, b3,       [Qll + (Q2 E Cl(D).
                                                         =


For non-square D, Gauss’s definition yields the same group structure on
CI(D) as the Dirichlet composition (2.3). This is immediate from the ob-
servation that the identities (2.6) and (2.7) are satisfied for the forms in
(2.3) if one takes the bilinear relations equal to



In the particular case where we want to duplicate a form in CI(D), the
identities (2.6) suggest that we should take S2 S3 and t2 t3. The result
                                                   =            =


will be used in section 6 to prove the correctness of the algorithm to solve
the duplication equation 2x c E 2Cl(D).
                                =




2.8. LEMMA. Let F    (a, b, c) be a primitive quadratic form of discrimi-
                       =


nant D, and suppose we are given integers si, ti for i = 1, 2, 3 satisfying
the identities



Then the class 2[F] E CI(D) contains the form



If a and b are coprime in this lemma, we can find A and v satisfying Aa+ vb    =


1 and take



to find the identity 2[(a, b, c)] =   ((a2, b - 2vac, v2c2 + Ac)] from lemma 2.4.
290


3. Computing quadratic 2-class groups.
Let D - 0, 1 mod 4 be a non-square integer for which we have a complete
factorization. We want to compute the strict 2-class group C C Cl of the
quadratic order of discriminant D. The computation is essentially a matter
of linear algebra over the field of 2 elements F2. For this reason, we take
the values of all quadratic characters in this section to lie in F2 rather than
in the multiplicative group (-1).
   The factorization of D provides us with the two basic ingredients of our
algorithm. The first is an F2-basis of the character group ~D of C/2C           =



Cl/2CI, commonly known as the group of genus characters of Cl. The
second is a generating set of ambiguous forms, i.e., a set of forms whose
classes generate the 2-torsion subgroup C[2]    =
                                                  Cl[2] of C c Cl. The classes
in Cl of the elements of our set will not in general form an F2-basis for C(2~.
   Let d be the discriminant of the field              We have D =        for some
integer f &#x3E; 1 that equals the index of the quadratic order of discriminant D
inside the maximal order in
   For an odd prime divisor p of D, we write xp : (Z /DZ)* - F2 for the
quadratic character of conductor p and xd =         (~) :
                                                  (Z/DZ)* - F2 for the
quadratic character corresponding to the field      Q(@) .
   The group of field characters Xd corresponding to D is the group




of Dirichlet characters on (Z/DZ)*. Here p ranges over the odd prime
divisors of d. If d is odd, the characters xp form a basis of 3id and their
product equals ~d. If d is even, the product of xd and all characters xp is a
quadratic character of 2-power conductor associated to the quadratic field of
discriminant -4 or ~8. This character, which we denote correspondingly
by x-4, X8 or x-8, and the characters xp now form a basis for              In
all cases, the order of 3Cd equals 2’, with t the number of distinct prime
divisors of d. The abelian field corresponding to ~d is the genus field of
the quadratic field Q( vD). It is the maximal abelian extension of
that is unramified at all finite primes and abelian over Q.
   The full group 3CD of genus characters associated to the discriminant D
has a similar definition, but special care is needed to obtain the correct
characters of 2-power conductor. Writing 3C’ D for the group of characters
generated by Xj and the quadratic characters xp for odd prime divisors p
                                                                             291


of f , we have




A basis of 3CD is obtained by adding to a basis for 3id the characters xp
for the odd prime divisors of f that do not divide d and the characters
X-4 and x8 as specified in the definition above. One finds that if D has u
distinct prime divisors, then ~D has dimension u + 1 if D is divisible by
32 (and      contains all quadratic characters of 2-power conductor), u - I
for D = 4 mod 16 (when d is odd and f - 2 mod 4) and u otherwise. The
abelian field GD corresponding to 3CD is the genus field of the quadratic
order of discriminant D. It the maximal abelian extension of Q that is
contained in the ring class field of conductor f of   Q( v’Ï5).  By class field
theory,  the Galois group                       is canonically isomorphic to
CI/2CI C/2C,
         =       and  it follows that there is a  perfect pairing of F2-vector
spaces



More explicitly, the value of a character X E ~D on a class [Q] E Cl is the
common x-value of the integers coprime to D that are represented by Q.
One deduces that the value of a character X E 3ED of conductor k on the
class of (a, b, c) in Cl equals




If the conductor k of x is a prime power dividing D, as in the case of the
’basis characters’ of 3i D mentioned above, the primitivity of the form im-
plies that at least one of these conditions is satisfied. Our algorithm will
only use such basis characters. For general X E 3CD, one uses its representa-
tion on the basis. Alternatively, one can replace a form of discriminant D
by an equivalent form (a, b, c) satisfying gcd(a, D) 1, cf. [4, ex. 2.18]. An
                                                     =


element      E Cl is in the principal genus 2CI if and only if all characters
of 3ED vanish on it, so the genus characters enable us to decide efficiently
whether an element of Cl is in 2CI. In section 6, we will prove the following.

3.4. DIVISION-BY-2-ALGORITHM. Given a form Q                  whose class lies
in 2CI, we can efficiently find a form P e 1’D satisfying         =
                                                                      tQ] E Cl.
292


The class of the form P in 3.4 is only determined up to composition with
classes from CI[21, and all we know is that the form P found by the algo-
rithm lies in one of these classes. Even when Q is in the trivial class, there
is no guarantee that P will be in the trivial class.
   Apart from an explicit description of the character group of C/2C, the
factorization of D also yields generators for the subgroup C[2] of ambiguous
ideal classes in Cl. This is due to the well known fact that C[2] consists
of classes of invertible OD-ideals I C OD of index dividing D. We can
take classes of ideals of prime power index as generators. If p is an odd
prime dividing D, say           there is an invertible OD-ideal Ip =
                                                                      Z ~ pk +
Z ’ (D + ~)/2 of index pk in the order O D . As this ideal is equal to its
conjugate in OD , its class in Cl(D) is a 2-torsion element. It is the class of
the quadratic form




For D - 0 mod 4, say 2111 D with t &#x3E; 2, we have an ambiguous form




that is the principal form for D == 4 mod 16. If D is divisible by 32, there
is another ambiguous form




that is needed to complete our generating set of ambiguous forms. Thus, if
we start with the set of forms            prime, we obtain a generating set So
by leaving out QZ for D - 4 mod 16 and including Q2 for D - 0 mod 32.
If D has u distinct prime divisors, then So has u + 1 elements if D is
divisible by 32, it has u - 1 elements for D - 4 mod 16, and u elements
otherwise. This is exactly the F-dimension of the character group 3ED,
and as the cardinality of C[2] equals #(C/2C) =                    we conclude
that there is exactly one non-trivial relation in Cl between the elements
of So. For negative D, the triviality of the ideal class((~)] _ ((~))     E Cl
yields the desired relation in all cases but one (the easy case d -4). We
                                                                   =


can then form an F2-basis for C[2] from So by leaving out an appropriate
element. For D &#x3E; 0 however, the relation between the ambiguous ideal
classes is much more subtle. If the fundamental unit eD E OD is of norm
-1, the relation is again               ~(~)~   =  0. If ED is of norm +1, the
                                                                          293


ambiguous ideal class ((1+ED)] 0 yields the desired relation. The problem
                               =


is of course that ED is usually too large to be computable in practice. For
this reason, we have to start our algorithm for D &#x3E; 0 with a generating
set So for C[21, not an F2-basis. This difference between the real and
the imaginary case accounts for the slightly larger running times of the
algorithm for positive D. The relation between the generators of C[2] for
D &#x3E; 0 can be obtained as a by-product of the computation of C. From
the relation we can determine the sign of the norm of eD without explicitly
computing ED. This feature of the algorithm is exploited in [].
   The computation of C proceeds by the construction of an F2-basis for
the left argument of the character pairing



For the right argument           we have our basis X of characters of   prime
power conductor indicated above. The basis B C 0D of forms whose classes
yield a basis for C/2C will be constructed as a disjoint union of sets Aj
( j = 1, 2, ... ) in such a way that the classes of the forms in Bi =
form a basis for the canonical image of C[2’] in C/2C. The basis A, for
the image of the 2-torsion subgroup C[2] will be formed from the set So
of ambiguous forms. More generally, we will carry a set Si of 2’+’-torsion
forms along at stage i. Roughly speaking, the character pairing is used to
’split’ the set Si into a set     of basis forms and a set of forms that map
to 2C. We divide the latter forms by 2 using our algorithm 3.4 to obtain
the set ,S’z+z of 2i+2-torsion forms needed at the next level. We continue
until the union Uj    Aj yields a basis for C/2C. We are then done by the
following elementary lemma on abelian 2-groups.
3.5. LEMMA. Let G be a finite abelian 2-group, X a basis for its group of
quadratic characters, and suppose we have a disjoint union B      =
                                                                      Aj
of finite sets Aj C G such that the following holds:
a. the 2-torsion subgroup G[2] is generated by the elements              with

b. the matrix                   a   non-singular square matrix.
Then B maps to an FZ -basis for G/2G, the elements in Aj have exact order
2i in G and the natural map



is an isomorphism of groups.
294


Proof. The non-singularity of the character matrix in (b) implies that the
elements in B map to a basis for G/2G, so these elements generate the
group G. As G[2] and G/2G have the same F2-dimension, the elements of
the form 2j-laj with aj E Aj that occur in (a) necessarily form a basis
for G(2~. In particular, the elements of Aj have exact order 2-~ In order
to obtain the required isomorphism for G, we have to show that for any
relation             0 E G with coefficients kb E Z, we have ord2(kb) &#x3E; j(b)
                       =


for all b E B. Here j(b) denotes the index j for which b is in Aj . Suppose
that, on the contrary, the integer n      =                        is positive.
Then we can multiply our relation by 2n-1 and write it as



By definition of n, the expressions in brackets are integral and not all even.
This implies that we would have a non-trivial relation between the basis
elements               of G[2] . Contradiction.                               D

Note that the conclusion of the lemma implies that the subset Bi     = U~=l Aj
C G maps to a basis of the canonical image of G[2Z1 in G/2G.
   We now describe an inductive algorithm that computes sets of forms
A~ C 0D such that the hypotheses of lemma 3.5 apply to their classes in
G C. We noted already that the problem with working with forms is that
     =


we cannot decide whether two different forms are different as elements of C.

However, the forms in the sets Aj that are computed by our algorithm are
constructed in such a way that the quadratic character values of each two
of these forms are distinct. This means that B       =
                                                          Aj can indeed by
viewed as a subset of G C, as required by 3.5. Thus, we do not run into
                              =


the problem encountered by Shanks [, p. 849] . The sets of forms SZ that
are constructed during the algorithm do not in general map injectively to
C.
  Our algorithm computes more than just a set of forms Aj at stage j.
The data it stores after i steps are the following:

1.   a   ah’sjoint union      U"=1 Aj of finite sets of forms Aj, together with
     a collection   of forms Si such that C[2] is generated by elements of the
      form          I with aj E Aj and 2’[s] with 8 E Si.
2.    a subset   XZ C X of characters such that the matrix                     is
     a   non-singular square matrix.
Initialization. At the initial stage i  0, we have Bo -
                                              =
                                                                and our
set S’o of ambiguous forms that meets the non-empty requirement ( 1 ~ .
                                                                         295


Induction step. Suppose we have           X at stage i. Then the set Bi is
not a set of generators for C, and we proceed to the next stage as follows.
Consider the character matrix



whose columns X(a) E Ff give the ’complete quadratic character’ of the
forms a E          By (2), the elements X (a) for a E Bi are independent in
     and we can compose each of the elements of Si with forms from Bz to
obtain that all characters in Xi vanish on it. After doing so, we still have
(1) for our modified set SZ, and the new columns X (s) for s E Si span a
subspace Tl C Ff that is linearly disjoint from the space spanned by the
columns X(a) with a E B;. We choose Ai+l C ,Si such that the columns
X(a) with a E          form a basis of V, and we pick a set of characters
Y C X such that the matrix                       is non-singular. We clearly
have Yi 1 Xi 0, and we set Xi+I Xi
             =                      =          to obtain (2) for stage i + 1.
   The remaining forms in             are now composed with forms from

Ai+1 in such a way that the characters in X ~ Xi also vanish on them. Then
all characters in X vanish on these modified forms, so their classes are in
2C. We now apply our division-by-2-algorithm 3.4 to each of the modified
forms in            and take the solutions obtained as the set Si+,.
   If s is in Si, we can by construction write [s] E C as a sum of classes
[az+lj with        E      and 2[sz+lj with     E       We conclude that the
sets 12’[s] : s E     and             ai+1 E                    si+l E
generate the same subgroup of C [2j , so we have (1) for stage i + 1 as well.
Termination. The algorithm terminates at stage i if we have Xi = X.
This is bound to happen as we have Xi X if and only if C is annihilated
                                         =



by 2i. To see this, suppose first that C is annihilated by 2z. Condition (1)
then implies that the elements                  generate C[2], so the number
~Bz   of  such  elements is at least equal dimC[2] = ~X . It follows from
                                           to
(2) that we have ~Xz - ~Bz &#x3E; #X, so Xi - X. Conversely, if we find
X2 X at stage i, then C is annihilated by 2’ as it can be generated by a
   =



set Bi of 2’-torsion elements.
   We conclude that after lV steps, with 2N the exponent of C, we have
found a basis B  =
                         A~ for C that satisfies the conditions of lemma 3.5.
This finishes the description of the algorithm.

In the actual implementation of the algorithm, we used a refinement that
ensures that the final character matrix                becomes lower trian-
gular. Instead of        for
                  taking Ai+l     some subset of Si whose X-image spans V,
one alternately picks a character and constructs a form to produce Yi and
296


Ai+I, as follows. Let Si be our set of forms, modified such that all charac-
ters in Xi vanish on Si, and look at the submatrix MI    =
of Mi . We set Yi = S     =
                           A;+i and do the following until all entries of Mi’
equal zero. Pick a form a E Si and a character X E X - Xi such that
x(c~) ~ 0, add X to the set Yi and move the form a from S2 to Ai+1. Com-
pose the remaining forms s E ,Sz that have           0 with a-this yields a
new set SZ and continue     with the new,  smaller matrix      This process,
which is called echelonization, produces a non-singular lower-triangular ma-
trix                    for the ordering of forms and characters suggested
above. Moreover, it replaces sZ by a set of forms with classes in 2C, and
Si+l is constructed from this set applying 3.4.
   At the final stage i  N of the algorithm, there is no need to apply the
                          =



division-by-2-algorithm 3.4 to compute a set SN of 2 N+ ’-torsion forms. In
the imaginary case D     0, this is clear since we can take So to be a basis
        and find SN - 0. In the real case D &#x3E; 0, we have to work with
an extra generator in So. At the final stage N, we compute from            a
set AN that completes our basis B and a single form sD E 2C to which
we can apply 3.4 to find the single element of sN. As [SDI is divisible by
2 in a group of exponent 2~, we have                 o. We can, at the cost
of a little extra administration, carry not only the set Si along at stage i,
but also for each s E Si the representation of 2’[s] in terms of our original
2-torsion generators in So. This is simply done by keeping track of how the
forms in Si+l are constructed at stage i from the previous set         If we do
so, the relation              0 for D &#x3E; 0 provides us with the dependency
between the ambiguous forms in So . If, for some reason, we would have
even more generators in Sa, we could in the same way find a complete set
of relations between them.
   Given an element c E C, the explicit knowledge of the character pairing
with respect to the basis B for C enables us to write c on the basis B. From
the pairing, one computes a sum bo E C of elements in B C C that has the
same quadratic character values as c    =
                                          Co. This yields Co = bo + 2ci for
some class cl E C that can be found by 3.4. One inductively computes sums
bi EC of elements in B such that ci                  for I   0,1, ... , N - 1.
                                                             =



The desired representation for c is then c =
   The number k of divisions by 2 performed by the algorithm to compute C
can easily be derived from the group structure of C: for any factor (Z/2-~Z)
in the representation of lemma 3.5 one has to perform j - 1 divisions by 2.
However, since for D &#x3E; 0 there is at any stage in the algorithm one more
generator than the rank of the group necessitates, the number of divisions
performed for the maximal j, which equals lV, has to be counted twice.
                                                                         297


Writing h #C for the 2-class number of D and r E {u - 2, u - 1, u} for
           =


the 2-rank of C, we find




This explains the observation in the introduction that our algorithm usually
needs more time for real class groups than for comparable imaginary class
groups.

4. A worked example.
In order to illustrate the abstract description in the previous section, we
compute by way of example the real quadratic 2-class group C of discrimi-
nant




which has 7 distinct prime factors. We use the notation from the previous
section.
   In our example, the group of field characters 3Cd corresponding to D has
order 23 and is generated by the quadratic characters X13, X9[, X137 and
      The product of these four characters corresponds to the field
and vanishes on C, so we can form an F2-basis of 3id by dropping X149 from
our set of generators. By (3.1), we can complete this to a basis X for the

group of genus characters ~D on C by adding the characters X-4, X7 and
      Our initial set So of ambiguous forms consists of a form Qp for each
odd prime divisor of D and the form Q2 (4, 0, -D/16) at 2.
                                          =



   We initialize our algorithm by taking Bo   =
                                                Xo = 0 and compute the
character matrix Mo   =
                                       using (3.3). This yields




The space V spanned by the columns of Mo is 3-dimensional, and the
3 x 3-submatrix corresponding to the forms Q2, Q7 and Q13 and the set
Yo -                of characters is non-singular. In order to obtain a
298


lower-triangular matrix, we choose the 3 basis elements in A, as the classes
of the forms




These elements span the image C2 of C[2] in C/2C. We obtain BI      =
                                                                        Al U
Bo Al and Xi Xo U Yo Yo.
      =          =          =



  The 4 remaining forms Q4i, Q97, Q137 and Q149 from So are now com-
posed with forms from Al to make all characters vanish on them,
  and we use our division-by-2-algorithm to compute the forms slj E Si
from the duplication equations




The matrix M1 of character values in the next iteration step is readily
evaluated as




Only the column of S14 lies outside the space spanned by the columns of
the forms in   Thus A2 contains a single element, for which we take


As x41 is the only character that does not vanish on aI2, we take Yl -
and obtain a set X2 = Yo U Y1 of cardinality 4. The three remaining forms
in Sl are now composed with forms in B2   =
                                              Al n A2 to make them divisible
by 2, and we find forms in 52 from the duplication equations
                                                                       299


The next matrix of character values M2 becomes




All 3 columns of the forms    S2 lie in the space spanned by the columns
of the forms in B2 A, U A2. This immediately yields Y2 = 0 A3, so we
                  =                                           =


have X3 - X2 and B3 - B2, and 83 contains 3 forms that are computed
from the equations




The character matrix M3 becomes




which has maximal rank 6. This means that we have found the structure
of our group to be C23 x C4 x Cr6. In order to obtain a lower triangular
character matrix, we take our final two generators of order 16 as




and add Y3  =
                IX137, X971 in the suggested order to our character basis.
The result is the final character matrix
300


and our algorithm terminates. The elements aij listed in the top row form
an ordered basis ofC, i.e., the sets Ai =       satisfy the hypotheses of
lemma 3.5 for G C.=



   In the final stage of the algorithm, it turns out that the character column
of the form S32 E S3 lies in the space generated by the previous columns,
so we have to compute S33 before we find that the character matrix has
maximal rank. In the cases where we are lucky enough to obtain already a
character matrix of full rank before the final column has been computed,
our algorithm suppresses the computation of the form corresponding to this
final column. This saves an application of the division-by-2-algorithm. For
large positive discriminants, the resulting gain can be considerable.
   As observed in the previous section, the ’superfluous generator’ 332 in
the final stage of our algorithm is not entirely useless: it carries information
on the relation between the ambiguous forms in the initial set So . More

explicitly, the character values of S32 tell us that the element


is in 2C. As C is of exponent 16, this implies that SD is annihilated by 8.
Using the definition of Sij and the order relations 2iaij = 0, the resulting
relation 8S32 + 8a4l  =0 is easily traced back to yield




This is the unique non-trivial relation between the initial generators Qp.
We noted already that such relations can in principle be found from the
fundamental unit        In this fairly small example it is still possible to
compute ~D explicitly. It has norm 1, and we have




where each of t, u, v is an integer of approximately 230 decimal digits. We
find that (eD + 1 ) /t is an element of norm 13 - 97 - 412 , from which we can
read off the relation indicated above.

5. Ternary quadratic forms.
   This section describes the reduction theory of ternary quadratic forms
that is the basis of the division-by-2-algorithm in section 6.
   Let n &#x3E; 1 be an integer, and L  =Zn an n-dimensional lattice with
standard inner product (-, -) : L x L -~ Z. For every endomorphism A E
                                                                        301


End(L)     M.(Z), we have an associated quadratic form F FA on L
            =                                                  =



defined by F(X) _ (AX, X). Writing A as a matrix        with respect
to the standard basis of L, we have




For n   =   2 and n 3, we use variables x, y and z. If A ranges over the
                      =



integral symmetric ~n x n)-matrices, then FA ranges over the quadratic
forms F     =                   for which the ’mixed coefficients’ Cij with
i 54 j are even.
   We define the determinant det(F) of a form F corresponding to a sym-
metric matrix A by det(F)   =
                             det~A). In particular, the determinant of a
quadratic form Q ax2 + 2bxy + Cy2 is for us equal to
                      =




There is a natural right action of GLn(Z) on the set of quadratic forms
in n variables by ’coordinate transformations’. If a form F corresponds
to a symmetric matrix A and S E GLn (Z) is a coordinate change, then
Fs (ASX, SX) = (ST AsX, X) clearly corresponds to the matrix ST AS.
    =


Here S~’ denotes the transpose of S.
   Two quadratic forms F and G are said to be equivalent if there exists
a unimodular transformation S E SLn(Z) such that Fs       =   G. Note that
-idL acts trivially and has determinant (20131)~? so the GLn(Z)-orbits and
the SLn (Z)-orbits of forms coincide in odd dimension.
   The adjoint A* of a matrix A =          is the matrix
where the (i, j )-minor mij of A is the determinant of the matrix that is
obtained from A by deleting the i-th row and the j-th column. If A is
invertible, one has

This immediately yields the general identities det A* =                and
A*B* _ (AB)*, and an easy check yields the useful identity



For a quadratic form F corresponding to a symmetric matrix A, the adjoint
form F* of F is the form corresponding to A* . Passing to the adjoint is
compatible with the action of SLz(Z) in the sense that we have (FS)* =
(F*)s* .
302


   For n    2, we have Gauss’s binary quadratic forms (a, 2b, c)
            =                                                        ax2 +
                                                                      =



2bxy+Cy2  with even  middle  coefficient corresponding symmetric
                                                      to           matrices
     Identity (2.1) tells us that every form of determinant A is equivalent
to a form with first coefficient lal               Moreover, a unimodular
transformation that yields such an equivalent form can be efficiently com-
puted E8] .
   For n 3 we obtain ternary forms, and for forms of non-zero determinant
           =



the reduction theory proceeds by a combination of binary reduction of both
the form itself and its adjoint. Suppose the ternary form F of determinant
        0 corresponds to a symmetric matrix A          =       with adjoint
                                can use suitable unimodular transformations of
A*    = (Ai j )i~~-1. Then we
the form                             /          - B.




                          quadratic form F(x, y, 0) a, lX2 + 2al2XY +
as if we were to reduce the                                =



a22y2 of determinant alla2z - ai2 = A33, and produce a ternary form
F with unchanged adjoint coefficient A33 but with all satisfying lalli[
0. Similarly, by applying the unimodular matrix



to F we leave all invariant and change F* by an application of




Choosing the coefficients of Sl as if reducing the quadratic form F* (0, y, x) =
A3gx2 - 2A23XY + A 22 y2, which has determinant f3gf22 - f23 - AFall
by (5.1), we can satisfy the inequality IA331[                    Alternating
these two transformations, we get smaller values of lalll and ~A33I until
both inequalities laill :5 4A33/3 and A33I V41allAF113 hold at the
same time.  The form F is then said to be semi-reduced, and it satisfies
                                                                           303


A semi-reduced form remains semi-reduced under unimodular transforma-
tions of the form




and we can use these to produce a reduced ternary form. There are two
possibilities, depending on whether the coefficient all of our semi-reduced
form is zero or not.
   In case all= 0 we also have A33   =
                                    al2    0, and therefore AF = -aI3a22.
                                            =



Looking at the effect of S2 on F, we see that an appropriate choice of S2
yields a form with



A semi-reduced form with alI     =0 satisfying (5.3) is said to be reduced.
For given OF, there are only finitely many possible values of al3 and a22,
so the number of reduced forms of given determinant with all     =0 is finite.
   For a semi-reduced form with all =1= 0, we apply S2 with suitable 312 to
obtain




As A33 does not vanish, a simple inspection of the action of




on F*   shows that we can further achieve




A semi-reduced form with all =1= 0 satisfying (5.4) and (5.5) is called re-
duced. It is again true that there are only finitely many reduced forms of
given determinant with          0. Indeed, we have bounded the coefficients
    al2 and A13 ~ A23, a A33 in terms of AF, and the following elementary
completion lemma shows that in our situation, these coefficients and AF
uniquely determine the form.
304


5.6. LEMMA. Suppose we are given rational numbers ~, all, aI2, A13, A23
and A33 satisfying ðalIA33 =1= 0. Then there exists a unique rational
symmetric (3 x 3)-matrix A    =            with determinant A and adjoint
A*    =
          (Aij )3
                i. e., there is a unique way to define the starred entries in




such that A is rational and symmetric with determinant A and adjoint A* .


Proof. As al l is non-zero, we can define a22 by the relation


We now use A33 # 0 to define An, A12, A22 as the unique solutions to the
equations




and form the rational symmetric matrix B     =            It is clear that if
matrices A and A* of the required sort exist, then the relations (5.7) hold
by (5.1) and A is uniquely determined by the equality A* = B. Let us
therefore, in accordance with (5.7), define the rational symmetric matrix
A =
                by the identity ~A B* . Passing to the adjoint yields
                                     =



6,2 A*    det(B) - B, so we see from (*) that we have d2 det(B) and
          =                                                     =


A*    =B. Thus A has the correct adjoint, and from AA B* =      =A** we see
that its determinant equals A.                                            C7

As every ternary form is equivalent to a reduced form, we see that the
number of equivalence classes of ternary forms of determinant A is finite
for every A. As an example that we will need in the next section, let us
take A     -1 and determine the equivalence classes. The entries of the
           =



symmetric matrices corresponding to the ternary form F and its adjoint
will again be denoted by aij and Aij, respectively.
   By (5.2), a semi-reduced ternary form F of determinant A -1 has  =


either an     A33 = 0 or )all) = IA331‘
               =                         = 1. In the case al l A33 = 0
                                                                    =


we have a22a~3 - 1, so a22 = 1 and al3 = ~l. If ~’ is reduced, (5.3)
                                                                         305


yields a23 0 and a33 E I - 1, 0, 11, so we find 6 forms. If we are in the
             =


second case and F is reduced, then a12    =
                                             A23  =
                                                    A13  =  0 by (5.4) and
(5.5). This yields a13 a23 0 and shows that F is one of the 4 forms
                       =      =



~x2 ~ y2 ~ z~ with an odd number of coefficients -1. This shows that
there are 6 + 4  =  10 reduced forms of determinant -1. Apart from the
negative definite form -x2 - y2 - z2, all these forms are indefinite. It is
easily checked that the nine reduced indefinite forms are all equivalent, so
there are two SL3(Z)-equivalence classes. We have proved the following.

5.8. LEMMA. An indefinite ternary f orm of determinant -1 is SL3(Z)-
equivalent to the form y2 - 2xz.                                  C1

Our proof of this lemma is constructive, as it shows how to find a matrix
S’ E SL3(Z) that maps a ternary form F of determinant -1 to y2-2xz. One
simply reduces F by the procedure outlined in this section to obtain one
of the 9 reduced indefinite forms listed above, keeping track of the trans-
formation matrices encountered along the way, and performs an explicit
transformation that we did not bother to write down to obtain y2 - 2xz.
It has been shown by Lagarias [8] that this gives rise to a polynomial-time
algorithm.
fi. Division by 2 in quadratic class groups.
In order to complete the description of our algorithm, we explain in this
section how one can explicitly divide by 2 the class of a binary quadratic
form Q that is known to be in the principal genus. We have seen in the
discussion following lemma 2.4 that finding a form P satisfying 2[P] = [Q]
is closely related to the representation of suitable squares by the form Q,
i.e., to finding solutions to a ternary quadratic equation Q(~,~/) = z2.
Gauss [6, art. 2861 observed that this can be done efficiently by extending
the given binary form to a ternary form for which the represented squares
can be trivially found after reduction. It is convenient to assume that we
work with even discriminants. This is not a restriction as for odd D, the
natural map C(4D) -~ C(D) is an isomorphism. The basic observation is
the following.

6.1. LEMMA. Let Q be a binary quadratic form of even discriminants D.
Then the class of      in 2Cl(D) zf and ortly if there exists a ternary qua-
dratic     Qi o f d eterminant -1 satisfying

Proof. It suffices to show that all genus characters in XD vanish on the
class of Q   =
               (a, 2,~, J) if and only if there exists an integral symmetric
306


matrix A of determinant -1 of the form




Suppose A exists, and write 6 = -D/4 a7 - {32 for the determinant of
                                         =



Q. Then the adjoint of A is an integral matrix of the form




and the relations (5.7) with A = -1 yield




If p is an odd prime divisor of D, then p divides 6 =
                                                       a-y _ (32 and either a
or, is coprime to p, so we see from (3.3) and (6.2) that the genus character
xp vanishes on Q. The characters of odd prime conductor generate the
subgroup X’v/(Xd) C               and we see from definition (3.1) that 6 is
divisible by if x_4 is needed to generate the full group, and divisible by 8
             4
if x8 is needed. As either a or q is odd, (6.2) shows that these characters
vanish on Q as well. We conclude that the existence of A implies that Q is
in the principal genus of Cl(D) .

  Conversely, if Q is in the principal genus, we claim that the congruences


admit solutions        Z. By the Chinese remainder theorem, this amounts
to solving the congruences modulo all prime powers p~ dividing 6. Either
a or -y is a unit modulo such a prime power, say a, and the vanishing of
the corresponding genus character (or, for p  =
                                               2, characters) implies that
we can solve rrz2 = a mod p~. Taking n = -~3m-1 mod p~, we see that all
three congruences are satisfied modulo p~ .
  Now pick m and n satisfying the congruences modulo 6. As a and 6
are non-zero, we can apply the completion lemma 5.6 to find a rational
symmetric matrix A of determinant -1 and its adjoint A* that are of the
form given above. The coefficients All, A12 and A22 of A* satisfy (6.2) and
                                                                             307


are clearly integral. This makes A* and A** = -A integral, so we have
found the required matrix A.                                       D

The preceding proof shows that finding the matrix A corresponding to Ql
amounts to extracting square roots of integers modulo the prime powers
dividing D. The prime powers dividing D are supposed to be known, and
extracting square roots modulo prime powers can be done efficiently if one
knows a quadratic non-residue modulo the prime occurring in the modulus
[2, section 1.5.1~. Finding such a residue is easy in practice and can be done
in random polynomial time. A deterministic polynomial algorithm however
only exists if one assumes the generalized Riemann hypothesis. See [2, p.
33-34, remarks (2) and (3)]. It is only this minor non-deterministic step
that makes our algorithm a random polynomial time algorithm.
   In the situation of lemma 6.1, the binary form Q is represented by the
ternary form Qi. More generally, we say that a binary quadratic form Q is
represented by a ternary quadratic form F if there exist integers ai and bi
for i l, 2, 3 such that
      =




Writing AF for the symmetric matrix corresponding to F and Q      =
                                                                      (a, 2,Q, 7),
we see that (6.3) is equivalent to the identities




The representation (6.3) is proper if the integers ai and bi come from a
unimodular transformation




If this is the case, we have Q(x, y)    =
                                            QI (x, y, 0) for the ternary form
Qi    =Fs.   Moreover, we  have  Qi (0, 0, 1) det Q, and Q is represented
                                             =



by every ternary  form that is equivalent to QI. As we do not consider bi-
nary quadratic forms that are negative definite, the form QI and therefore
the representing ternary form F are indefinite. Combining lemmas 6.1 and
5.8, we now obtain the following result.
6.6. THEOREM. Let Q be a binary quadratic form of even discriminant D.
Then the class of Q is in the principal genus 2CI(D) if and only
                                                             cy  if Q can
&#x26;e
be properly repreeed    &#x26;y 6
            represented by      the ternary    $ = y2 - 2xz.
                                    terar form q.=      2.
                                                      2013

                                                                       D
                                                                       0

The representation in theorem 6.6 is found by constructing a ternary form
QI of determinant -1 as in lemma 6.1 and reducing the form QI to ~ as
308


outlined in the previous section. We find Qm 1    for some M E SL3(Z),
and S M-1 yields the representation Q(~, ~) _
         =
                                                       y, 0). However, as
Shanks observed, we do not need S but only the reduction matrix M to to
solve the equation 2(P~ _ [Q].
  Indeed, if we have Q(x, y) =                    with S E SL3(Z) as in (6.5), the
form Q represents the squares



of integers r   =
                    alb2 - a2b1 and p   =
                                            a2b3 - a3b2 that occur in the last row


of the reduction matrix M       S-1. In view of the observation following
                                  =


lemma 2.4, it is therefore to be expected that p and r occur as first coeffi-
cients of binary forms whose duplication lies in jQ).

6.7. THEOREM. Let Q be a primitive binary quadratic form of even dis-
criminant D, and Suppose we have M E SL3(Z) and a ternary form Qi
satisfying                 =    and Qf = tÏ’ = y2 - 2xz. Let (~, q, r) _
M~(0,0~ 1) be the last row of M, and define the quadratic form


Then P is a primitive form of discriminants D, and we have 2tP]             =
                                                                                tQ] E
Cl(D).

Proof. As gcd(p, q, r) divides det M 1, we have gcd(p, q, r)
                                             =
                                                                     1, so in
                                                                        =


order to show that P is primitive we have to check that p and r cannot
both be even. Suppose they are. Then q is odd. The last row of the matrix
product MS id yields the relations pal + qa2 + ra3 pbl + qb2 + rb3 0,
                =                                            =                   =


so a2 and b2 are both even. It follows from (6.4) that the coefficients




and 2# of Q     =
                    (a, 2,3, 7} are all even, contradicting the primitivity assump-
tions on Q.
   There are various ways to check the identity 2(P]        One can mul-
                                                             =



tiply M by transformations stabilizing 4D and reduce to the case that p is
                                                                            309


coprime to D, which can be handled by the method given after lemma 2.4.
However, it is much more efficient to apply lemma 2.8 directly. Taking F
in that lemma to be equal to (p, -2q, 2r) or (2p, -2q, r), i.e., in the class of
--[P], we can take the bilinear form in 2.8 respectively equal to



As we have ,~   =
                  -alb3 + a2b2 - a3b, by (6.4), it follows from 2.8 that the
class inverse to 2[P] contains the form (a, -2~,7). This implies 2[P] = [Q],
and consequently P has the required discriminant 4(q2 - 2pr) D. We can
                                                                 =


check this directly by substituting (p, q, r) in the adjoint -4~* = -y2+ 2xz
of p =
        QM ~2 - 2xz. As M* is the inverse of MT , we obtain the desired
            =


value




Theorem 6.7 shows that we can divide [Q] E Cl(D) by 2 if we can complete
Q to a ternary form QI of determinant -1 and find the transformation
matrix M that reduces QI to 16 = y2 - 2xz. Both of these steps can be
efficiently performed whenever Q is in the principal genus. This finishes
the description of the division-by-2-algorithm 3.4.

7. Performance of the algorithm.
The algorithms described in the previous sections have been implemented
in the high-level language of the computer algebra system MAGMA. Table
7.1 below shows the results of an experiment devised to give an indication of
the dependence of the performance of the algorithm on various parameters,
in particular the size and sign of the discriminant and the structure of C.
   For several n ranging from 25 to 400 (as indicated at the top of each
column in the tables), we found 5 primes close to 10’~ that are squares
modulo each other. The first table lists the primes used; the i-th prime
used for each value of n is 10" + r2. The primes 101°° + ri are the prime
factors of the discriminant D occurring in the introduction.
310


Each row in table 7.1 gives results for the discriminant pD built up from
the product D of the five primes of size 10" and an additional factor p that
is indicated in the first column. As additional factors we chose the odd
primes up to 79, with a sign chosen such that we have p = 1 mod 4, and
the even factors p ~8. We are looking here then at discriminants of 125
                   =


to just over 2000 decimal digits. It would be out of the question to factor
arbitrary discriminants of that size, or to compute a single full class group
Cl(pD).
   Each entry in the table consists of three values. The first is the 2-class
number of pD, written in a way that corresponds to the structure of the
2-class group C(pD). The two values on the second line are the number
of seconds it took our implementation to find this group structure and the
(rounded) quotient of this running time by the number of times a division
by 2 had to be performed to obtain the group structure. Thus, the first
entry says that for D the product of our five primes 1025 + ri, we have
C(-79. D) - C2 x C4 x C16 . This computation took 11 seconds. As the
computation of such a group takes 4 divisions by 2 by formula (3.6), this
is approximately 3 seconds per division.
   In a given column, the time needed per division is roughly constant. This
means that the time needed to find the   2-group structure is proportional
to the number of divisions by 2, that is, to the combination of the width
and depth of the 2-group given in (3.6). There is a small but noticeable
difference in running time between imaginary and real class groups. In the
table, they are separated by a row that indicates, for each value of n, the
average time it took the algorithm per division for the imaginary and for
the real class groups. On average, the algorithm is about 15% slower for
real quadratic class groups.
   The average running times per division in the central row give an indi-
cation of the complexity function for the major operations as a function
of the number of decimal digits. The dominant factor is the slightly worse
than quadratic time growth of ordinary integer arithmetic with the size of
the integers.
   A closer look at where the time is spent reveals that there are three main
components: the ternary reduction step, the modular square root used in
the division by 2 of a class in the principal genus, and the composition and
reduction of quadratic forms. The ternary reduction step takes up between
1/3 and 1/2 of the total time for a divison by 2. The fraction of time
needed for the modular square root (with modulus the discriminant, but
performed prime by prime) increases slightly with the size of the primes
                                             311

Table 7.1. Class groups and running times.
312


involved, and in the largest case (of 400 digit primes) takes about as long
as the ternary reduction. The contribution from the composition of forms
varies considerably but is usually much smaller. It depends primarily on
the number of reduction steps necessary after a single composition in the
very last stage of the division-by-2-algorithm. In our examples sometimes
several hundreds of reduction steps were needed, taking up to 1/5 of the
total time for the large discriminant case.

                                     REFERENCES

[1] W. Bosma, J. J. Cannon, C. Playoust, The Magma algebra system I: the user lan-
    guage, J. Symbolic Comput. (to appear).
W. Bosma and P. Stevenhagen, Density computations for real quadratic units, Math.
    Comp. 65 (1996), no. 215, 1327-1337.
[2] H. Cohen, A course in computational algebraic number theory, Springer GTM 138,
      1993.

[3] H. Cohen, F. Diaz y Diaz, M. Olivier, Calculs de nombres de classes et de régulateurs
      de corps quadratiques en temps sous-exponentiel, Séminaire de Théorie des Nombres
      Paris 1990-91, Birkhäuser, 1993, pp. 35-46.

[4] D. A. Cox, Primes of the form x2 + ny2, Wiley-Interscience, 1989.
[5] S. Düllmann, Ein Algorithmus zur Bestimmung der Klassengruppe positiv definiter
      binärer quadratischer Formen, Dissertation, Universität des Saarlandes, Saarbrücken,
      1991.

[6] C. F. Gauss, Disquisitiones Arithmeticae, Gerhard Fleischer, Leipzig, 1801.
[7] J. Hafner, K. McCurley, A rigorous subexponential algorithm for computation of
    class groups, J. Amer. Math. Soc. 2 (1989), no. 4, 837-850.

[8] J. C. Lagarias, Worst-case complexity bounds for algorithms in the theory of integral
    quadratic forms, J. of Algorithms 1 (1980),142-186.
J. C. Lagarias, On the computational complexity of determining the solvability or un-
     solvability of the equation X2 - DY2 = -1, Trans. Amer. Math. Soc. 260 (1980),
     no. 2, 485-508.

D. Shanks, Gauss’s ternary form reduction and the 2-Sylow subgroup, Math. Comp. 25
    (1971), no. 116, 837-853Erratum: Math. Comp. 32 (1978), 1328-1329.
[9] P. Stevenhagen, The number of real quadratic fields having units of negative norm,
    Exp. Math. 2 (1993), no. 2,121-136.
P. Stevenhagen, A density conjecture for the negative Pell equation, Computational
    Algebra and Number Theory, Sydney 1992, Kluwer Academic Publishers, 1995,
      pp. 187-200.
                                                               313



Wieb BOSMA et Peter STEVENHAGEN
Faculteit Wiskunde, Informatica, Natuurkunde en Sterrenkunde
Universiteit van Amsterdam
Plantage Muidergracht 24
1018 TV Amsterdam
The Netherlands
e-mail: wieb@wins.uva.nl, psh@wins.uva.nl
