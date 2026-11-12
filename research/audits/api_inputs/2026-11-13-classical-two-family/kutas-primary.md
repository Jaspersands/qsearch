# Actual primary source
URL: https://arxiv.org/pdf/1606.01053 ; v2 Sep2018, published JSC94(2019)173-182. Original local PDF retained alongside source SHA256 metadata. Physical pdftotext lines115-466 (Proposition7 through Theorem20/Remark22), no abstract-only inference.

Definition 5. Let H be a quaternion algebra over K, with quaternion basis 1, u, v, uv. Let
s = λ1 + λ2 u + λ3 v + λ4 uv. Then let σ(s) = λ1 − λ2 u − λ3 v − λ4 uv be the conjugate of s. We
call T r(s) = s + σ(s) the trace of s and N(s) = sσ(s) the norm of s. Note that both T r(s)
and N(s) are in K.

Remark 6. One can show that the functions T r(x) and N(x) do not depend on the quaternion
basis and coincide with the usual reduced trace and reduced norm (see [24]).

Proposition 7. The following statements are equivalent:

  1. HK (α, β) ∼
               = M2 (K),

  2. There exists a nonzero element s ∈ HK (α, β) such that N(s) = 0,

  3. The quadratic form x21 − αx22 − βx23 + αβx24 is isotropic over K,

  4. There exists a nonzero element s ∈ HK (α, β) such that T r(s) = 0 and N(s) = 0,

  5. The quadratic form αx2 + βy 2 − z 2 is isotropic over K.

Remark 8. If we write out condition (2) in terms of the quaternion basis we obtain (3). This
shows that if
                               x21 − αx22 − βx23 + αβx24 = 0,
then 1+x1 u+x2 v+x3 uv is a zero divisor (or equivalently has norm zero) in HK (α, β). Condition
(4) if written out would give the equation αx20 + βy02 − αβz02 = 0 (since every element x for
which T r(x) = 0 is the linear combination of u, v and uv). By a change of variables we arrive
at (5) (x := yα0 , y := xβ0 , z := z0 ). Thus from a solution to the equation

                                       αx2 + βy 2 − z 2 = 0,

a zero divsor in HK (α, β) can be obtained by a polynomial-time algorithm (first reverse the
change of variables and then apply condition (3) as discussed above).
   Details can be found in [24] (or [4],[21]). Note that this shows that there is a strong
connection between quaternion algebras and quadratic forms in three variables over K.

                                                 3
 2.2    Algorithmic results
Now we review some algorithmic results concerning quaternion algebras and quadratic forms
over Q. Note that we only consider deterministic and randomized polynomial-time algorithms
(which may use oracles for factoring integers). In this note every randomized algorithm is of
Las Vegas type. In this section we consider an algebra to be given as a collection of structure
constants, which means the following. Let A be an algebra over the field K. Let a1 , . . . , am
be a K-basis of A. Then the products of the basis elements can be expressed as the K-linear
combination of the basis elements:

                             ai aj = γij1a1 + γij2a2 + · · · + γijmam .

    The γijk ∈ K are called structure constants. Note that specifying A with structure constants
is equivalent to giving A by its regular representation.
Example 9. Let HK (α, β) be a quaternion algebra with the quaternion basis 1, u, v, uv. Then
every basis element is given by a 4 × 4 matrix:
                                                                      
              1 0 0 0        0 1 0 0        0 0 1 0           0    0 0 1
            0 1 0 0 α 0 0 0  0 0 0 −1  0                    0 −α 0
                                                                      .
            0 0 1 0  0 0 0 1 β 0 0 0   0                    β 0 0
              0 0 0 1        0 0 α 0        0 −β 0 0        −αβ 0 0 0

    Rónyai [21] gave a polynomial-time algorithm for finding a quaternion representation from
an arbitrary structure constant representation. Thus we may assume that a quaternion algebra
is given by a quaternion basis.
Definition 10. Let A ∼= Mn (K) be given by structure constants. The explicit isomorphism
problem is to compute an isomorphism between A and Mn (K).
Remark 11. Finding an explicit isomorphism is equivalent to finding an element r of rank 1
in A. Indeed, the left action of A on the left ideal Ar produces such an isomorphism (the
vector space Ar has dimension n and the left action is K-linear so every element of A can be
represented by an n × n matrix and this map is an isomorphism).
    Rónyai showed ([21]) that there is a randomized polynomial-time reduction from factoring
square-free integers to the explicit isomorphism problem in the case A ∼  = M2 (Q). Ivanyos and
Szántó [15] proposed a polynomial-time ff-algorithm to solve this problem. They construct a
maximal order (using the algorithm from [14]) and use lattice reduction to find a zero divisor.
Note that an ff-algorithm can also be thought of as a randomized polynomial-time algorithm
which is allowed to call oracles for factoring integers.
    Cremona and Rusin gave a different algorithm [6] for the same task which runs in polynomial
time if one is allowed to call an oracle for integer factorization. They proposed an algorithm
which finds nontrivial zeros of quadratic forms in three variables over Q. From this data a
zero divisor in A can be constructed via the description in Proposition 7. The algorithms from
[10],[20] and [13] generalize these results to matrix algebras of higher degree.
    However, if K is a number field then the algorithms from [13] and [15] run exponentially in
the degree and the logarithm of the discriminant of the number field.
    In the next section we consider the case where A ∼= M2 (K) where K is a quadratic extension
of Q. It turns out that this is related to finding nontrivial zeros of quadratic forms over Q in
several variables. Hence we cite these two results:

                                                 4
 Fact 1 (Simon [23]). There is a randomized polynomial time-algorithm for finding nontrivial
zeros (or proving that no such zero exists) of quadratic forms over Q in dimension at least 4 if
one is allowed to call oracles for factoring integers.

    The paper of Simon [23] was presented at the conference ”Recent Developments in Computa-
tional Number Theory” (http://poncelet.sciences.univ-metz.fr/~ soriano/ProgrammeCIRM.pdf)
and is implemented in MAGMA [2]. Finding nontrivial zeros of quadratic forms in 4 variables
over Q is also at least as hard as factoring integers since quadratic forms in dimension 4 with
square discriminant correspond to quadratic forms of dimension 3 (see [4]). Castel [4] improved
these algorithms and obtained an algorithm which works in dimension 5 (and above) and does
not depend on factoring integers. However, its running time calculations depend on the validity
of the Generalized Riemann Hypothesis (GRH).

Fact 2 (Castel [4]). Assuming GRH, there is a randomized polynomial-time algorithm which
finds a nontrivial zero of an indefinite quadratic form (over Q) in dimension 5 (or more).


3      Finding a zero divisor
In this √
        section we propose an algorithm for finding a zero divisor in A which is isomorphic to
M2 (Q( d)) and is given by structure constants. First we construct a subalgebra B in A which
is a quaternion algebra over Q. Then, with this information at our hands, we construct a zero
divisor. In Remark 11 we saw how to construct an explicit isomorphism from a zero divisor.
First we outline the steps of our algorithm:

Algorithm 1.

    1. Find an element u ∈ A such that T r(u) = 0 and u2 ∈ Q and u 6= 0.

    2. Find a nonzero element v such that uv = −vu and v 2 ∈ Q.

    3. Let B be the Q-subspace generated by 1, u, v, uv. B is a quaternion algebra over Q. Use
       the algorithm from [13] (or [15]) to either find a zero divisor in B or conclude that B is
       a division algebra.
                                                                                            √
    4. If B is a division algebra then find an element s ∈ B such that s2 = d. Return s − d.

    The key to each step is finding an isotropic vector for a quadratic form in several variables. In
Step 1 we solve a homogeneous quadratic equation in 6 variables, in Step 2 and 3 an equation in
3 variables and finally in Step 4 an equation in 4 variables. Step 1,2 and 3 are already exhibited
in [17]. Step 4 is the crucial new step which allows us to find a zero divisor in A and not just
a quaternion subalgebra over Q. Now we proceed by providing an algorithm for each step.
                                     √
Proposition 12. Let A ∼     = M2 (Q d) be given by structure constants. Then there exists a
randomized polynomial-time algorithm which is allowed to call an oracle for integer factorization
which finds a nonzero l ∈ A for which T r(l) = 0 and l2 ∈ Q.

Proof. First we construct a quaternion basis 1, w, w ′, ww ′ of A. We have the following:
                                           √                    √
                              w 2 = r1 + t1 d, w ′2 = r2 + t2 d

                                                 5
    If t1 or t2 is 0 then w or w ′ will be a suitable element. If r1 t2 + r2 t1 = 0 then (ww ′)2 ∈ Q
and is traceless. From now on we assume that √    t1 , t2 and r1 t2 + r2 t1 are nonzero.
   Every element whose trace is 0 is in the Q( d)-subspace generated by w, w ′ and ww ′. The
condition l2 ∈ Q gives the following equation (s1 , . . . , s6 ∈ Q):
                              √                √                    √
                     ((s1 + s2 d)w + (s3 + s4 d)w ′ + (s5 + s6 d)ww ′)2 ∈ Q

    If we expand this we obtain:
                                      √                 √                √
                             ((s1 + s2 d)w + (s3 + s4 d)w ′ + (s5 + s6 d)ww ′)2 =
                              √           √                         √          √
          (s21 + ds22 + 2s1 s2 d)(r1 + t1 d) + (s23 + ds24 + 2s3 s4 d)(r2 + t2 d) −
                                                            √          √          √
                                        (s25 + ds26 + 2s5 s6 d)(r1 + t1 d)(r2 + t2 d)
                                                      √
    In order for this to be in Q the coefficient of d has to be zero:

               t1 s21 + t1 ds22 + 2r1 s1 s2 + t2 s23 + t2 ds24 + 2r2 s3 s4 − (r1 t2 + t1 r2 )s25 −                 (1)
                                               (r1 t2 + t1 r2 )ds26 − 2(r1 r2 + t1 t2 d)s5 s6 = 0                  (2)

    The left hand side of Equation 1 is a quadratic form in the variables s1 , . . . , s6 . This implies
that if it is indefinite then it has a solution. The Gram-matrix of the quadratic form is the
following:                                                                    
                          t1 r1 0 0               0                 0
                       r1 t2 d 0 0               0                 0          
                                                                              
                        0 0 t2 r2                0                 0          
                                                                              
                        0 0 r2 t2 d              0                 0          
                                                                              
                        0 0 0 0 −(r1 t2 + t1 r2 )           r1 r2 + t1 t2 d 
                          0 0 0 0           r1 r2 + t1 t2 d −(r1 t2 + t1 r2 )d
     It is block diagonal with three 2×2 blocks. The determinant of the first block is t21 d−r12, the
determinant of the second is t22 d − r22 and the determinant of the third is (r1 t2 + t1 r2 )2 d − (r1 r2 +
t1 t2 d)2 . Now we show that this quadratic form is always indefinite. If d < 0 then t21 d − r12 < 0
(it is nonzero since t1 6= 0 and d is a square-free integer), hence the form t1 s21 + t1 ds22 + 2r1 s1 s2
is indefinite. If d > 0 then if either t1 s21 + t1 ds22 + 2r1 s1 s2 or t2 s23 + t2 ds24 + 2r2 s3 s4 is indefinite
then we are done. So the remaining case is when t21 d − r12 > 0 and t22 d − r22 > 0. However,
this implies that the quadratic form −(r1 t2 + t1 r2 )s25 − (r1 t2 + t1 r2 )ds26 − 2(r1 r2 + t1 t2 d)s5 s6 is
indefinite since

                       (t21 d − r12 )(t22 d − r22 ) = −((r1 t2 + t1 r2 )2 d − (r1 r2 + t1 t2 d)2 )

.
    Hence we have proven that the quadratic form

t1 s21 +t1 ds22 +2r1 s1 s2 +t2 s23 +t2 ds24 +2r2 s3 s4 −(r1 t2 +t1 r2 )s25 −(r1 t2 +t1 r2 )ds26 −2(r1 r2 +t1 t2 d)s5 s6
                                                                                                                   (3)
has a nontrivial zero over Q. A nontrivial zero of the quadratic form in (1) can be found by
Simon’s algorithm [23]. This is a randomized polynomial-time algorithm if one is allowed to
call an oracle for factoring integers.
                                                                                                            √
Remark 13. Observe that we only used the fact that A is a quaternion algebra over Q( d), we
did not need the fact that it is in fact a full matrix algebra.

                                                           6
 Remark 14. The main tool of this proof was an algorithm for finding nontrivial zeros of quadratic
forms in 6 variables. For this task we also could have used Castel’s algorithm [4]. However,
Castel’s algorithm is dependent on GRH and we would like to have an algorithm which is
independent of the validity of GRH.
   We proceed to the next step:
                                            √                                  √
Proposition 15. Let B = HQ(√d) (a, b + c d) given by: u2 = a, v 2 = b + c d, where a, b, c ∈
Q, c 6= 0. Then finding a nonzero element v ′ such that uv ′ + v ′ u = 0 and v ′2 is a rational
multiple of the identity is polynomial-time equivalent to finding a zero divisor in the quaternion
algebra HQ (( cb )2 − d, a).
Remark 16. By polynomial-time equivalent we mean the following. From a zero divisor in
HQ (( cb )2 − d, a) a suitable element v ′ ∈ B can be constructed in polynomial time. On the other
hand, from a suitable element v ′ ∈ B a zero divisor in HQ (( bc )2 − d, a) can be constructed in
polynomial time as well.
                                                                            √
Proof. Since v ′ anticommutes with u (i.e. uv ′ + v ′u = 0) it must be a Q( d)-linear combination
of v and uv. This implies we have to search for s1 , s2 , s3 , s4 ∈ Q such that:
                                           √              √
                                  ((s1 + s2 d)v + (s3 + s4 d)uv)2 ∈ Q

   Expanding this expression we obtain the following:
                                                       √                √
                                             ((s1 + s2 d)v + (s3 + s4 d)uv)2 =
                                  √        √                          √         √
             (s21 + s22 d + 2s1 s2 d)(b + c d) − (s23 + s24 d + 2s3 s4 d)a(b + c d)
                                                        √
   In order for this to be rational, the coefficient of d has to be zero. We obtain the following
equation:

                        c(s21 + s22 d) + 2bs1 s2 − ac(s23 + s24 d) − 2abs3 s4 = 0
   First we divide by c. Note that c is nonzero. Let f = b/c.

                         s21 + s22 d + 2f s1 s2 − a(s23 + s24 d) − 2af s3 s4 = 0                (4)

    First we diagonalize the left hand side of Equation 4. Consider the following change of
variables: x := s1 + f s2 , y := s2 ,z := s3 + s4 f , w := s4 . The transition matrix of this change
of variables is the following:                           
                                             1 f 0 0
                                           0 1 0 0 
                                           0 0 1 f  .
                                                         

                                             0 0 0 1
The transition matrix is an upper triangular matrix with 1-s in the diagonal so it has deter-
minant 1 (this means that these two quadratic forms are equivalent). In terms of these new
variables the equation takes the following form:

                            x2 + (d − f 2 )y 2 − az 2 − a(d − f 2 )w 2 = 0.
    Finding a solution of this equation is polynomial-time equivalent to finding a zero divisor
in the quaternion algebra HQ (f 2 − d, a) by Proposition 7.

                                                   7
 Remark 17. This statement can be interpreted constructively and as a complexity statement
as well. First it provides a randomized polynomial-time algorithm (which is allowed to call an
oracle for factoring integers) for finding such an element v ′ . It also says however, that finding
such an element v ′ is as hard as finding zero divisors in quaternion algebras over Q. Rónyai
proved in [21] that there is a randomized polynomial-time reduction from factoring integers
to finding zero divisors in quaternion algebras over Q. This implies that finding a quaternion
subalgebra over Q containing u is hard (otherwise one could easily find such an element v ′ ).
Also note that Simon’s algorithm could also be applied to solving Equation 4 from which a
suitable v ′ can be constructed.
                                                                                         √
Remark 18. Proposition 15 also provides the following result. Let B = HQ(√d) (a, b+c d) where
                                                                                   2     2
a, b, c ∈ Q. Then B contains a quaternion√ subalgebra over Q if√and only if HQ (b −cd2 , a) 2splits.
               2     2
The number b −cd is the norm of b+c d in the extension Q( d)|Q. Actually HQ (b −cd , a) is
then the so-called corestriction of B [7, Part II, Theorem 7]. It is known that if the corestriction
of B splits then B contains a quaternion subalgebra over Q, however, the usual proofs of this
fact are not effective. For more details on the corestriction (or norm) of central simple algebras
the reader is refferred to [7],[16].
   Finally putting Proposition 12 and 15 together we obtain the following:
                                √
Corollary 19. Let A ∼   = M2 (Q( d)) be given by structure constants. Then one can either find
a zerod divisor in √A, or a four dimensional subalgebra over Q which is a quaternion algebra
(and is split by Q( d)) by a randomized polynomial-time algorithm which is allowed to call an
oracle for factoring integers.

Proof. First we find a nonzero element l such that T r(l) = 0 and l2 ∈ Q using the algorithm
from Proposition 12. If l2 = 0, then output l as a zero divisor. If not, then we prove that there
exists an element l′ such that ll′ + l′ l = 0 and l′2 ∈ Q.
    If l2 is a square in Q, then such an l′ exists by Proposition                   2     2
                                                                √ 15. Indeed let l = c ∈ Q and let
                                                       2
w be an element in A for which wl = −lw and w = e + f d. Then Proposition 15 asserts that
a suitable l′ exists if and only if the quaternion algebra HQ (d − fe 2 , c2 ) splits. The quaternion
algebra HQ (d − fe 2 , c2 ) does split since c2 is a square in Q (thus l − c is a zero divisor).
    From now on assume that l2 is not a square in Q. There exists a subalgebra A0 in A which is
isomorphic to M2 (Q). In this√subalgebra there is an element l0 for which l and l0 have the same
minimal polynomial over Q( d). This means that there exists an m ∈ A such that l = m−1 l0 m
([24, Theorem 2.1.]). There exists a nonzero l0′ ∈ A0 such that l0 l0′ + l0′ l0 = 0. Let l′ = m−1 l0′ m.
We have that l′2 = m−1 l0′ mm−1 l0 m = m−1 l02 m = l02 , hence l′2 ∈ Q. Since conjugation by m
is an automorphism we have that ll′ + l′ l = m−1 (l0 l0′ + l0′ l0 )m = m−1 0m = 0. Thus we have
proven the existence of a suitable element l′ . Using the algorithm from Proposition 15 we can
find an element l′ such that ll′ + l′ l = 0 and l′2 ∈ Q.
    The√Q-subspace generated by 1, l, l′ , ll′ is a quaternion algebra H over      √ Q. Observe that
H ⊗ Q( d)    √ has dimension   8 over  Q  and is√naturally embedded  into M  2 (Q(  d)). Hence it must
be M2 (Q( d)), so H is really split by Q( d).
                    √
    Let A ∼= M2 (Q( d)) be given by structure constants. At this point we are able construct
a subalgebra B of A which is a quaternion algebra over Q. This was also established in the
extended abstract [17]. However, as B may be a division algebra, this seemingly does not help
us in finding a zero divisor in A.

                                                   8
     The key observation missing from [17] is the following.
                                                     √      Not every quaternion division algebra
                                                                                             √
over Q can be obtained as a subalgebra of M2 (Q( d)), only those which are split by Q( d).
The next theorem turns this observation into an algorithm for finding a zero divisor in A:
                                 √
Theorem 20. Let A ∼    = M2 (Q( d)) be given by structure constants. Then Algorithm 1 com-
putes a zero divisor in A. Algorithm 1 is randomized and runs in polynomial time if one is
allowed to call an oracle for factoring integers.

Proof. First we construct a quaternion subalgebra H over Q using Corollary 19. If H is iso-
morphic to M2 (Q), then one can find a zero divisor in it by using the algorithm form [13].√ If
                                                      2
not then there exists an element
                           √      s ∈ H such that s = d. Indeed, since H is split by Q( d)
and therefore contains Q( d) as a subfield [24, Theorem 1.2.8]. Let 1, u, v, uv be a quaternion
basis with u2 = a, v 2 = b. Every non-central element whose trace is zero (in H) is a Q-linear
combination of u, v and uv. Hence finding an element s such that s2 = d is equivalent to
solving the following equation:
                                     ax21 + bx22 − abx23 = d                                (5)
     Since H is a division algebra, the quadratic form ax21 + bx22 − abx23 has no nontrivial zeros.
Thus solving Equation 5 is equivalent to finding a nontrivial zero of the quadratic form ax21 +
bx22 − abx23 − dx24 . One can find such a zero using the algorithm from [23]. This algorithm runs
in polynomial time if one is allowed to call oracles for factoring integers. We have found an
element s in H such that s2 = d. Since H is a central simple √     algebra over Q and d is not a
square in Q, the element s is not in the center of A. Hence s − d is a zero divisor in A.
Remark 21. An alternative ending of the algorithm could be the following. Assume that we
have already found the subalgebra H. There always exists an element s ∈ H for which s2 = d.
We have seen this in the case where H is a division algebra. If H is a full matrix algebra then
it is well-known. Hence the quadratic form ax21 + bx22 − abx23 − dx24 is always isotropic. We find
an isotropic vector (x1 , x2 , x3 , x4 ). If x4 6= 0 we proceed as before. If x4 = 0 then the norm of
x1 u + x2 v + x3 uv is 0, hence it is a zero divisor.
Remark 22. We would like to note that Algorithm 1 only needs at most two oracle calls for
integer factoring in Step 2 and 4. Furthermore, there there are subexponential algorithms
for integer factorization [19],[3] and Shor’s algorithm can factor integers by a polynomial-time
quantum algorithm [22].
    First we would like to emphasize that our√algorithm can be used to find nontrivial zeros
of quadratic forms in three variables over Q( d) by Proposition 7. Moreover, Algorithm 1
is a reduction procedure in the following√sense. The task of finding a nontrivial zero of a
quadratic form in three variables over Q( d) can be accomplished by finding nontrivial zeros
of quadratic forms √
                   in 3,4 and 6 variables over Q. This reduction procedure works for any number
field instead of Q( d). Therefore if someone √  finds an algorithm for finding nontrivial zeros of
quadratic forms in 4 and 6 variables over Q( d), then one immediately  √ √  has an algorithm for
finding nontrivial zeros of quadratic forms in three variables over Q( d1 , d2 ). The reduction
procedure also works for fields of odd characteristic as demonstrated in [18].
    We conclude by considering the following question. The steps of Algorithm 1 perfectly
make sense in the case when A is a division algebra. In that case the algorithm may fail at two
points. Either it does not contain a quaternion subalgebra over Q or the subalgebra B which
is a quaternion algebra over Q does not contain an element s for which s2 = d. It is therefore
natural to ask when the failure of the first type occurs, meaning the following. Assume that A

                                                 9
