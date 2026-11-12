Buchmann-Lenstra 1994 actual primary source, https://jtnb.centre-mersenne.org/item/10.5802/jtnb.113.pdf
   Finding rings of integers is customarily viewed as a local problem, in the
sense that it suffices to do it
                              prime-by-prime. Algorithmically, however, the
bottleneck is of a global nature: how to find the prime numbers that one
needs to look at? Once these are known, the problem admits a solution.
This is expressed in our next result. If m is an integer, then an order A in
K is said to be maximal at m if gcd(m, (0 : A)) = 1.

THEOREM 1.2. There is a polynomial time algorithm that, given an alge-
braic number field K, an order A irc K, and a squarefree positive integer
m, determines an order B in K containing A that is maximal at m.

From 1.2 we see in particular that if m is prime one can find, in polynomial
time, an order in K that is maximal at m. If m is taken to be the product
of the primes p for which p2 divides the discriminant of A, then the order
B in Theorem 1.2 equals 0.
   We next formulate a few complexity results of purely theoretical interest.

THEOREM 1.3. Under polynomial transformations, the following two prob-
lems are equivalent:
    (a) given an algebraic number field K, find the ring of algebraic integers
         of K;
 226


      (b) given a positive integer d, find the largest squarefree divisor of d.
    Theorem 1.3 represents a slight improvement over a theorem of Chistov
(6), as explained in 6.11. We shall prove that the corresponding recognition
problems are also equivalent (Theorem 6.12).
   Suppose that an order A in an algebraic number field is given. In the
proof of Theorem 1.3 we shall see that, given the largest squarefree divisor
of the discriminant AA of A, one can find the ring of integers 0 of K in
polynomial time. In 6.13 we argue that it is hard to go in the opposite
direction: if given 0 one can easily find the largest squarefree divisor of
AA, then problem 1.3(b) is easy as well. It is possible, however, to compute
the largest square divisor of AA quickly from 1; again it is hard to go in the
opposite direction (see 6.14).
   If the ring of integers of a number field K is known, then the discriminant
of K is easy to compute. One may wonder whether, conversely, it is easy
to compute the ring of integers of K from the discriminant of K. In 6.10
we shall see that this is currently not the case. However, we do have the

following result.
THEOREM 1.4. There are polynomial time algorithms that given an alge-
braic number field K and one of (a), (b), determine the other:
      (a) the ring of algebraic integers of K;
      (b) the largest squarefree divisor of the discriminant of K.
   In the body of the paper we work with orders in products of number fields
rather than orders in number fields. This presents no additional difficulty.
One may remark, though, that the case of products of number fields can
in polynomial time be reduced to the case of a single number field, by the
main result of [15]. Also, several of our results are local in the sense that
they are directed not at constructing 0, but at constructing an order that
is maximal at a given integer m, as in Theorem 1.2.
   We have refrained from considering more general base rings than the
ring Z of rational integers. Over some base rings, the problem of finding
5.7. Orders and fractional ideals. As in [18, 2.7 and 2.10], an order A
will be given by its degree n over Z and the multiplication map A Q9 A
A. This comes down to specifying a system of n3 integers              such that
                        for some basis w 1, W2, ... ,7 wn of A over Z. Note
that one can verify in polynomial time whether or not a given system of
rt3 integers       encodes an order, by checking the ring axioms and the
non-vanishing of the discriminant AA in a straightforward way; here AA is
computed directly from its definition (see 2.2) . An ideal of an order A will
be specified by means of a basis of the ideal over Z, expressed in terms of
the given basis of A over Z, as was done for subgroups in 5.5; this may for
practical purposes not always be the most efficient representation, but for
theoretical purposes it will suffices. To make the representation of an ideal a
unique, we may require that the given basis consists of the rows of a matrix
in Hermite normal form. In that case all entries of the matrix are bounded
by the index of a in A. This is often useful if an algorithm deals with many
ideals and one wishes to control the growth of the numbers occurring in
the algorithm. A fractional ideal a is given by means of a pair d, b, where
d is a positive integer and b is an ideal of A of finite index; then a d-1 b.
                                                                      =


This is unique if we require that d is coprime to the largest integer e for
which b C eA.

PROPOSITION 5.8. There are polynomial time algorithms that given an
order A and fractional A-ideals al, a2, determine al + a2, a2, al n a2,
 246


and al : a2.

Proof. For sum and intersection this follows directly from Proposition 5.6.
The computation of a, - a2 is easily reduced to the case that ai, a2 are
contained in A. In that case,    a2 is the image of the multiplication map
al (9 a2  A,
          -; which  can be calculated by Proposition 5.6. The computation
of al : a2 can be reduced to the case that a2 :) A ~ al. In that case, we
have al : a2 C A : A = A, which implies that al : a2 is equal to the inverse
image of Hom(a2, ai ) under the map A -~ Hom(a2, a2) that sends x E A to
the multiplication-by-x map. This inverse image can, again, be calculated
by Proposition 5.6. This proves 5.8.
5.9. Overorders. Let A be an order, given by integers                   as above.
Overorders of A and their fractional ideals will be represented as fractional
ideals of A itself. Several algorithms in Section 6 compute many overorders
of A, and for the complexity analysis of these algorithms it is important to
note that the length of the data encoding any overorder B of A is uniformly
bounded by a polynomial function of           log(laijkl+2), i. e., of the length
of the data encoding A itself. This follows from what was said above about
fractional ideals and the fact that the index of A in B divides AA-

6. Approximating maximal orders

  In this section we prove the results stated in the introduction. We begin
with an auxiliary algorithm that corresponds to the case that the number
m in Theorem 1.2 is a prime number.



Algorithm 6.1. We describe an algorithm that, given an order A and a
prime number p, determines an overorder B of A that is maximal at p. The
algorithm begins by putting B A. Let t be the least positive integer for
                                  =


which pt &#x3E; ~A : Z~ .
   Calculate the kernel b of the Fp-linear map              B/pB that sends
every x E B/pB to       as well as the inverse image a of b under the natural

map B ~ B/pB;     this can be done by the algorithms of Section 5. Calculate
the overorder B’     a : a of B (see 5.8). If B’
                        =                            =
                                                      B, then the algorithm
stops. If B’ ~ B, then replace B by B’ and iterate. This completes the
description of the algorithm.
PROPOSITION 6.2. Given an order A and a prime number p, Algorithm fi.l
determines in polynomial time the unique overorder B of A that is maximal
at p and for which (B : A) is a power of p.
                                                                                 247


Proof. Let B be any overorder of A that is encountered in the algorithm.
Then B/pB is a finite ring containing Fp, and we have [BlpB : Fp]    [B :   =



Z] = [A : Z]. Let y B/pB.
                   E         Then  two of the subspaces


of B/pB must have the same dimension over Fp and are therefore equal.
Hence there exists i, 0 i ~A : Z], such that yi (B/pB) =
and this space is then equal to             for all j &#x3E; i. In particular, y is
nilpotent if and only if y [A:Z] 0, and if and only if ypt 0. This proves
                                 =                              =


that an element x of B belongs to a if and only if (x mod pB) belongs
to the nilradical of B/pB. Therefore a is an ideal of B containing pB.
This implies that B C B’ C p-l B, so that (B’ : B) is a power of p. It
follows that either B’   = B or ABI = ~B/p2s for some positive integer s.
Hence the algorithm goes through at most (log                   log(p2) iterations
before it stops. From Section 5 one sees that each iteration can be done
in polynomial time. Hence the entire algorithm runs in polynomial time.
We also find that ~B : A~ is a power of p for each B that occurs in the
algorithm.
   Let now B be the final overorder that is obtained. Then we have B             =


B’   = a : a, so by 2.4(c) the order B is maximal at p. From gcd(p, (0

B)) = 1 and the fact that (B : A) is a power of p it follows that B/A
is the p-primary subgroup of the quotient O/A of additive groups. This
determines B uniquely. This completes the proof of 6.2.

The second auxiliary algorithm corresponds to the case that the number m
in Theorem 1.2 is built up from prime numbers that exceed the degree of
A over Z, but without the squarefree-ness assumption.
