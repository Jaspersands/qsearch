Primary-source scope: Oki ICALP2020, actual intro and Remark12 below. Noncommutative weighted-matrix results cannot be silently specialized to commutative sparse resultant cancellation. LS Theorem1.11 excerpt follows, explicit finite Q-algebra inputs required.

On Solving (Non)commutative Weighted
Edmonds’ Problem
Taihei Oki
Department of Mathematical Informatics, Graduate School of Information Science and Technology,
University of Tokyo, Japan
taihei_oki@mist.i.u-tokyo.ac.jp

       Abstract
In this paper, we consider computing the degree of the Dieudonné determinant of a polynomial
matrix A = A` + A`−1 s + · · · + A0 s` , where each Ad is a linear symbolic matrix, i.e., entries of
Ad are affine functions in symbols x1 , . . . , xm over a field K. This problem is a natural “weighted
analog” of Edmonds’ problem, which is to compute the rank of a linear symbolic matrix. Regarding
x1 , . . . , xm as commutative or noncommutative, two different versions of weighted and unweighted
Edmonds’ problems can be considered. Deterministic polynomial-time algorithms are unknown for
commutative Edmonds’ problem and have been proposed recently for noncommutative Edmonds’
problem.
      The main contribution of this paper is to establish a deterministic polynomial-time reduction from
(non)commutative weighted Edmonds’ problem to unweighed Edmonds’ problem. Our reduction
makes use of the discrete Legendre conjugacy between the integer sequences of the maximum
degree of minors of A and the rank of linear symbolic matrices obtained from the coefficient
matrices of A. Combined with algorithms for noncommutative Edmonds’ problem, our reduction
yields the first deterministic polynomial-time algorithm for noncommutative weighted Edmonds’
problem with polynomial bit-length bounds. We also give a reduction of the degree computation
of quasideterminants and its application to the degree computation of noncommutative rational
functions.

2012 ACM Subject Classification Theory of computation → Algebraic complexity theory; Com-
puting methodologies → Linear algebra algorithms; Computing methodologies → Combinatorial
algorithms

Keywords and phrases skew fields, Edmonds’ problem, Dieudonné determinant, degree computation,
Smith–McMillan form, matrix expansion, discrete Legendre conjugacy

Digital Object Identifier 10.4230/LIPIcs.ICALP.2020.89

Category Track A: Algorithms, Complexity and Games

Funding This work was supported by JST CREST Grant Number JPMJCR14D2, Japan, Grant-in-
Aid for JSPS Research Fellow Grant Number JP18J22141, Japan and JST ACT-I Grant Number
JPMJPR18U9, Japan.

Acknowledgements The author thanks Satoru Iwata and Hiroshi Hirai for careful reading and
helpful suggestions, and Christian Engels, Tasuku Soma, Shuichi Hirahara and Yuni Iwamasa for
discussions.


 1      Introduction

The background of this paper goes back to Edmonds [10]. In 1967, Edmonds posed a question
whether there exists a polynomial-time algorithm to compute the rank of a linear (symbolic)
matrix B over a field K, which is in the form

     B = B0 + B1 x1 + · · · + Bm xm ,

            © Taihei Oki;
                                                                                                     EA
            licensed under Creative Commons License CC-BY
                                                                                                      TC S
47th International Colloquium on Automata, Languages, and Programming (ICALP 2020).
Editors: Artur Czumaj, Anuj Dawar, and Emanuela Merelli; Article No. 89; pp. 89:1–89:14
                   Leibniz International Proceedings in Informatics
                   Schloss Dagstuhl – Leibniz-Zentrum für Informatik, Dagstuhl Publishing, Germany
89:2   On Solving (Non)commutative Weighted Edmonds’ Problem


       where B0 , B1 . . . , Bm ∈ K n×n and x1 , . . . , xm are commutative symbols. Here, B is re-
       garded as a matrix over the polynomial ring K[x1 , . . . , xm ] or the rational function field
       K(x1 , . . . , xm ). In case where B is the Edmonds or Tutte matrix of a bipartite or nonbipar-
       tite graph G, the rank computation for B corresponds to solving the maximum matching
       problem on G. More generally, Lovász [27] showed that Edmonds’ problem is equivalent
       to a linear matroid intersection problem if all Bi are of rank 1, and to a linear matroid
       parity problem if all Bi are skew-symmetric matrices of rank 2. For general linear matrices,
       the celebrated Schwartz–Zippel lemma [34] provides a simple randomized algorithm if |K|
       is large enough [27]. However, no deterministic polynomial-time algorithm still has been
       known; the existence of such an algorithm would imply nontrivial circuit complexity lower
       bounds [22, 36].
           Recent studies [11, 17, 20] address the noncommutative version of Edmonds’ problem
       (nc-Edmonds’ problem). This is a problem of computing the noncommutative rank (nc-rank)
       of B, which is the rank defined by regarding x1 , . . . , xm as pairwise noncommutative, i.e.,
       xi xj 6= xj xi if i 6= j. In this way, B is viewed as a matrix over the free ring Khx1 , . . . , xm i
       generated by noncommutative symbols x1 , . . . , xm . The nc-rank of B is precisely the rank of
       B over a skew (noncommutative) field K<       ( x1 , . . . , x m )
                                                                       >, called a free skew field, which is the
       quotient of Khx1 , . . . , xm i defined by Amitsur [2]. We call a linear matrix over K having
       noncommutative symbols an nc-linear matrix over K. The recent studies [11, 17, 20] revealed
       that nc-Edmonds’ problem is deterministically tractable. For the case where K is the set
       Q of rational numbers, Garg et al. [11] proved that Gurvits’ operator scaling algorithm [16]
       deterministically computes the nc-rank of B in poly(n, m) arithmetic operations on Q.
       Algorithms over general field K were later given by Ivanyos et al. [20] and Hamada–Hirai [17]
       exploiting the min-max theorem established for nc-rank. In [16] and [20] applied to the case
       of K = Q, bit-lengths of intermediate numbers are proved to be bounded by a polynomial of
       the input bit-length.
           In this paper, we shall consider “weighted” versions of commutative and noncommutative
       Edmonds’ problem introduced by Hirai [18]. First, consider commutative symbols x1 , . . . , xm
       and an extra commutative symbol s. Define a matrix

           A = A` + A`−1 s + · · · + A0 s` ,                                                                (1)
                                                                          n×n
       where Ad = Ad,0 + Ad,1 x1 + · · · + Ad,m xm ∈ K[x1 , . . . , xm ]       is a linear matrix over K for
       d = 0, . . . , `. We call (1) a linear polynomial matrix over K. The weighted Edmonds’ problem
       (WEP) is the problem to compute the degree (in s) of the determinant of A. Analogously to
       Edmonds’ problem, WEP includes a bunch of weighted combinatorial optimization problems
       as special cases, such as a maximum weighted perfect matching problem, a weighted linear
       matroid intersection problem and a weighted linear matroid parity problem; see [18, Section 5].
           Defining noncommutative weighted Edmonds’ problem (nc-WEP) requires some more
       involved algebraic notions due to noncommutativity. Let x1 , . . . , xm be noncommutative
       symbols and s an extra symbol that commutes with any element in Khx1 , . . . , xm i. An
       nc-linear polynomial matrix A over K is a matrix in the form of (1) with each Ad regarded as
       an nc-linear matrix. Then A can be viewed as a matrix over the rational function (skew) field
       F (s) over F := K<    ( x1 , . . . , x m )
                                               >. Since entries of A are noncommutative, the determinant of
       A is nontrivial. Here, we employ the Dieudonné determinant [9], which is a noncommutative
       generalization of the usual determinant defined for matrices over skew fields. We denote the
       Dieudonné determinant of A by Det A. The Dieudonné determinant retains useful properties
       of the usual determinant such as Det AB = Det A Det B. While the value of Det A is no
       longer in F (s), its degree (in s) is well-defined [8, 35]. See Section 2.1 for the definition of
       Dieudonné determinant.
T. Oki                                                                                                     89:3


   The nc-WEP is the problem to compute deg Det of a given nc-linear polynomial matrix.
Hirai [18] formulated the dual problem of nc-WEP as the minimization of an L-convex
function on a uniform modular lattice, and gave an algorithm based on the steepest gradient
descent. Hirai’s algorithm uses poly(n, m, `) arithmetic operations on K while no bit-length
bound has been given for K = Q.
   A weighted combinatorial optimization problem often reduces to an unweighted problem.
This paper explores a reduction from (nc-)WEP (a weighted problem) to (nc-)Edmonds’
problem (an unweighted problem). The main result of this paper is the following.
I Theorem 1. The (nc-)WEP deterministically reduces to (nc-)Edmonds’ problem for an
(nc-)linear matrix of size `n2 with m symbols.
    Theorem 1 provides an efficient randomized algorithm for WEP through the Schwartz–
Zippel lemma and a deterministic polynomial-time algorithm for nc-WEP via the rank
computation algorithms [11, 18, 20] for nc-linear matrices. This algorithm for nc-WEP is
much different from Hirai’s algorithm [18]; in particular, while Hirai’s algorithm calls an
oracle of nc-Edmonds’ problem polynomially many times, our algorithm calls it only once
(the matrix size would be augmented instead). Furthermore, in case of K = Q, our reduction
does not exponentially swell the input bit-length because every entry of the nc-linear matrix
constructed in this reduction is some coefficient of an entry in the input nc-linear polynomial
matrix. Thus, by employing an algorithm [11, 18] for nc-Edmonds’ problem with bit-length
bounds, we obtain the following.
I Theorem 2. We can deterministically solve nc-WEP in poly(n, m, `) arithmetic operations
on K. In addition, if K = Q, the bit-lengths of intermediate numbers are bounded by a
polynomial of the input bit-length.
    We also give a reduction from computing the degree of a quasideterminant [12, 13],
which is another noncommutative analogy of the determinant, to computing the degree of

              µ≥0
                     d=0

Since N0 ≤ N1 ≤ · · · ≤ N`r = N`r+1 = · · · = r by Lemma 10 (1), the minimum value of the
right hand side of (19) is attained by µ = `r. Thus we are done.                       J

I Remark 12. In view of combinatorial optimization, our algorithms are regarded as pseudo-
polynomial time algorithms since the running time depends on a polynomial of the maximum
exponent ` of s instead of poly(log `). Thus it is natural to try to solve the following problem:
Sparse Degree of Determinant (SDD)
                                              n×n
   Input : A = A1 sw1 + · · · + Am swm ∈ K[s]     , where 0 ≤ w1 ≤ . . . ≤ wm are integers.
   Output: deg det A.


                                                                                                    ICALP 2020
89:12   On Solving (Non)commutative Weighted Edmonds’ Problem


                                               k
           However, setting wk := (n + 1) for k ∈ [m] would make the rank of A the same as
                                                                            n×n
        that of a linear matrix A1 x1 + · · · + Am xm ∈ K[x1 , . . . , xm ]     (known as the Kronecker
        substitution [24]). Since giving a deterministic polynomial-time algorithm for Edmonds’
        problem has still been open for more than half a century, SDD is also a quite challenging
        problem.

         4      Computing the Degree of Quasideterminants
        The quasideterminant [12, 13] is another noncommutative analogy of the determinant than
        the Dieudonné determinant. Let A ∈ F n×n be a square matrix over a skew field F . Fix
        i, j ∈ [n] and put I := [n] \ {i}, J := [n] \ {j}. The (i, j)th quasideterminant |A|i,j of A is
        defined if A[I, J] nonsingular as
                                                        −1
             |A|i,j := A[{i}, {j}] − A[I, {j}]A[I, J]        A[{i}, J] ∈ F.


Primary source https://arxiv.org/pdf/1509.08843
PDF SHA256 ade50162f347df28c7ff9d08691befe0b31ab28847359d9675ac261fd1dd945e
Original newline lines225--246
roots of unity in orders that the authors recently developed; see [14, 12, 13]. We also proved that,
given a Q-algebra E, one can find, in polynomial time, generators for the group µ(E) of roots of
unity in E, and we presented a solution to the discrete logarithm problem in µ(E); see [14]. The
following result states that, in fact, the discrete logarithm problem in the full multiplicative group
E ∗ of E admits an efficient solution.
Theorem 1.11. (i) There is a deterministic polynomial-time algorithm that, given a Q-algebra E
  and a finite system S of elements of E, decides whether all elements of S belong to E ∗ , and if
  so determines a finite set of generators for the kernel of the group homomorphism
                                                            Y
                                ZS → E ∗ ,      (ms )s∈S 7→     sms .
                                                              s∈S

(ii) There is a deterministic polynomial-time algorithm that, given a Q-algebra E, a finite system S
     of elements of E ∗ and t ∈ E ∗ , decides whether                                 ∗
                                                   Q t belong to the subgroup hSi of E generated by
     S, and if so produces (ms )s∈S ∈ ZS with t = s∈S sms .
   The case of Theorem 1.11 in which E is assumed to be a field is already quite complicated; it was
done by G. Ge [5]. We prove Theorem 1.11 in section 8 by a reduction to the case E is a field as
dealt with by Ge.
   In [1] one finds a result that is in substance equivalent to Theorem 1.11, with a proof that proceeds
along the same lines.

