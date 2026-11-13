
# ultraspherical actual excerpts

Physical LF239-285

                                                                                                                                        4

can be written in the ultraspherical polynomial basis as                        Theorem 1 (Efficient quantum ultraspherical transform).
                                                                                Fix an integer m ≥ 2 and a dimension N ≥ 1 with
                                      N −1
                                      X           (m)                           K = N + m = 2n . Let 0 < ε < 1/2 be the target error.
                         f (x) =             fˆk pk (x),                (14)    There is a unitary circuit U = Um,N,ε on n system qubits
                                      k=0                                       and a ancillary qubits such that, for every normalized
                                                                                input |ψ⟩ ∈ CK supported on |0⟩, . . . , |N − 1⟩,
where fbk is the coefficient of the kth basis polynomial. Col-
lect those coefficients into the vector fb = (fˆ0 , . . . , fˆN −1 )⊤ .                                        (m)
                                                                                              U |0a ⟩|ψ⟩ − |0a ⟩QN |ψ⟩ 2 ≤ ε.        (19)
The discrete orthogonality property says that this co-
efficient vector and the vector of weighted samples,                            This uniform bound is an operator-norm guarantee on the
 √
( wj f (xj ))N  −1
              j=0 , have the same Euclidean norm. Thus,                         valid input subspace, including leakage into unused output
after dividing by ∥f  b ∥2 , each can be viewed as a normal-                    labels or nonzero ancillas. The adjoint circuit implements
                                                                                  (m)†
ized quantum state. One state encodes the values of f                           QN with the same error and resource bounds.
at the sample points; the other encodes its expansion                              The circuit U can be implemented using
coefficients in the ultraspherical basis:
                                                                                                                  n          1
                                                                                          Gm (n, ε) = Om n3 log + n log2
                                                                                                         
                                        N −1                                                                                          (20)
                                  1 X√                                                                            ε          ε
              |f (m) ⟩ :=              wj f (xj )|j⟩,
                                ∥f
                                 b ∥2
                                        j=0                                     single-qubit rotations and CNOT gates, together with
                                                                        (15)
                                        N −1
                   (m)            1 X ˆ
                                                                                                                        
                                                                                                                       1
              |f
               b         ⟩ :=         fk |k⟩.                                                   a = Om log n + log log              (21)
                                ∥f
                                 b ∥2
                                        k=0
                                                                                                                       ε

The transform and its inverse then satisfy                                      ancillary qubits, where Om allows constants that depend
                                                                                on the fixed parameter m. All ancillas start and return
     (m)                   (m)                (m)† b (m)

Physical LF957-1043
for ρ = 0 and ρ = 1, using gs,m,K (bν (x) + ρ).                            satisfies
  After the fold, the lower n − 1 qubits of the system                                                     r
register hold b (Appendix B.4). On Iν , the polynomial is
                                                                                                           X                Γ
                                                                                                                            bs
                                                                                            ⟨0|Uin |0⟩ =         |s⟩⟨s| ⊗      ,             (77)
applied through the dyadic signal Bν of Eq. (31), which                                                    s=0
                                                                                                                            2
acts on the ν least significant of these qubits. Its di-
agonal entry on the folded label b = 2ν + v ∈ Iν is                       on the valid paired labels, with ∥Γ
                                                                                                            b s −Γs ∥2 ≤ ηΓ . All inter-
xν,v = (2v − 2ν + 1)/(2ν − 1), the rescaled coordinate                    polation data, rotation angles, and QET phase sequences
x of b, so that bν (xν,v ) = b. QET with a polynomial P                   are computed classically before quantum execution.
then encodes P (Bν )/2 as in Eq. (28), and P (xν,v ) approx-                 Extension to other Jacobi parameters. For integer m,
imates gs,m,K (b) for even m and gs,m,K (b + ρ) for odd m.                the QUT covers Jacobi polynomials with equal parameters
The same signal serves every order s and, for odd m, both                 α = β = m−1/2, and both ingredients of the input correc-
values of ρ; these enter only through the selected QET                    tion extend to asymmetric pairs of half-integer parameters.
phase angles. Since the interval circuit acts as the identity             First-order Darboux steps analogous to Aq shift (α, β) by
outside Iν , the entries of Bν on other folded labels do not              (±1, ±1), so a number of steps independent of N connects
enter the input block.                                                    the four Chebyshev families (±1/2, ±1/2) to every admis-
  Appendix B.3 shows that these rescaled functions are                    sible half-integer pair [42]. The resulting intertwiner has
analytic and uniformly bounded by the constant M of                       a fixed order and therefore maps each Fourier mode to

                                                                                                                                           13


            H1                H2                H3                H4       matically make a Jacobi transform efficient on a quantum
                     A1                A2                A3                computer. In the example discussed in Appendix G, one
    8                                                                      coefficient in the angular function diverges at an endpoint
                                                                           although the complete function is regular. Block-encoding
    7                                                                      this coefficient on the Gauss grid costs a subnormaliza-
                                                                           tion of order N . A Jacobi transform with the complexity
    6                                                                      of Theorem 1 would therefore need a discretization that
                                                                           preserves the regularity of the angular functions and an
    5
E                                                                          efficient circuit that implements it.
√
    4

    3
                                                                                  D.   Fourier block and frequency powers

    2                                                                         We next implement Es /(K −1)s for each Taylor order s.
                                                                           Recall from Eq. (47) that Es samples the sth derivatives of
    1                                                                      the trigonometric basis functions at the paired grid points.
                                                                                                                      p
                                                                           For p > 0, these functions  are  e p (θ) =  2/π cos(pθ) for
    0
        0                 0                 0                 0
                                                                                                  p
                 π                 π                 π                 π   even m and ep (θ) = 2/π sin(pθ) for odd m. Differen-
                                       θ                                   tiating s times contributes a factor ps , changes between
                                                                           sine and cosine when s is odd, and introduces a sign that
FIG. 5. From Fourier modes to ultraspherical modes: Each                   depends on m and s. We therefore implement Es /(K −1)s
panel Hq shows the potential corresponding to −∂θ2 + q(q −                 in two steps: a Fourier-based circuit produces the required
1) csc2 θ. We start with a particle in a box, whose modes are              trigonometric samples, and a second circuit applies the
sin Kθ with energies E = K 2 . Each Darboux transformation
                                                                           factor [p/(K − 1)]s .
Aq = ∂θ − q cot θ changes the potential and maps the modes
to the next well without changing their energies, except for                  The trigonometric function required after s derivatives
the lowest mode, which disappears. After m − 1 steps, sin Kθ               is determined by
                                  (m)
becomes proportional to sinm θ CN (cos θ). Orange dots mark
the Gauss–ultraspherical nodes, while circles mark the equis-                                  σs = (m + s) mod 2,                        (78)
paced grid used by sine or cosine transforms. The two grids
nearly coincide, but differ near the walls, where some grid                where σs = 0 denotes cosine and σs = 1 denotes sine.
points have no corresponding node (gray circles). The QUT                  To obtain these real transforms from the complex QFT,
uses a QFT on the equispaced grid and corrects for these small             we first apply a unitary Bin (s) that forms symmetric
shifts.                                                                    or antisymmetric combinations of grid labels and their
                                                                           reflections in a 2K-dimensional register. Define
                                                                                                   (
the same mode multiplied by a polynomial of fixed degree                                            2K − 1 − ℓ, m even,
in its frequency, whose coefficients depend only on the                                ref m (ℓ) =                           (79)
                                                                                                    2K − ℓ,      m odd.
angle [41], just as Pm−1 (u; h) in Zm−1 is a polynomial of
fixed degree in u = cot θ/K and h = 1/K. For modes
                                                                           For a paired grid label ℓj = j + ⌈m/2⌉,
on which every step has a positive norm, the phase of
the resulting normalized wave again determines the nodes                                                 |ℓj ⟩ + (−1)σs |ref m (ℓj )⟩
and weights as in Eq. (46). We present these parameter                         Bin (s)|0⟩br |ℓj ⟩sys =              √                 .   (80)
shifts and phase–quadrature identities in Appendix G.                                                                 2
   The exact construction stops at half-integer parameters.                The kets on the right denote labels of the joint br ⊗ sys
By Proposition 4, a nonzero finite-order differential oper-                register, with the branch qubit as the most significant bit.
ator with analytic, frequency-independent coefficients can                 Thus the input is symmetric for the cosine transform and
map Fourier modes to solutions of the Jacobi angular equa-                 antisymmetric for the sine transform. The QFT unitary,
tion for infinitely many frequencies only if α, β ∈ 1/2 + Z,               denoted by F, then acts on these n + 1 qubits. Its matrix
which is also exactly when the Jacobi angular functions                    entries are

# fast_jacobi actual excerpts

Physical LF160-226
                                                        j=0
here, t1 , . . . , tn , w1 . . . , wn are the nodes and weights of the n-point modified Gauss-Jacobi quadra-
ture rule corresponding to the parameters a and b. The properties of this quadrature rule and
                                                                                         (a,b)
the weighting by square roots in (7) ensure that the n × n matrix Jn                           which takes (8) to (7) is
                                                                            (a,b)
orthogonal. It follows from (1) that the (j, k) entry of Jn                       is
                                                               ´                     ¯?
                                       M (a,b) (tj , k − 1) cos ψ (a,b) (tj , k − 1)    wj .                       (10)

                                   (a,b)
Our method for applying Jn , which is inspired by the algorithm of [6] for applying Fourier
integral transforms and a special case of that in [37] for general oscillatory integral transforms,




                                                              3

exploits the fact that the matrix whose (j, k) entry is
                                             ´ ´                                 ¯¯ ?
                     M (a,b) (tj , k − 1) exp i ψ (a,b) (tj , k − 1) − (k − 1)tj     wj           (11)
                       (a,b)
is low rank. Since Jn   is the real part of the Hadamard product of the matrix defined by (11)
and the n × n nonuniform FFT matrix whose (j, k) entry is
                                             exp pi(k − 1)tj q ,                                  (12)
it can be applied through a small number of discrete nonuniform Fourier transforms. This can be
done quickly via any number of fast algorithms for the nonuniform Fourier transform (examples
of such algorithms include [18] and [31]). By “Hadamard product,” we mean the operation of
entrywise multiplication of two matrices. We will denote the Hadamard product of the matrices A
and B via A ⊗ B in this article.
We do not prove a rigorous bound on the rank of the matrix (11) here; instead, we offer the following
heuristic argument. For points t bounded away from the endpoints of the interval (0, π), we have
the following asymptotic approximation of the nonoscillatory phase function:
                                    ˆ           ˙           ˆ ˙
                      (a,b)              a+b+1                1
                    ψ       (t, ν) = ν +          t+c+O             as ν → ∞                     (13)
                                           2                  ν2
with c a constant in the interval (0, 2π). We prove this in Section 2.5, below. From (13), we expect
that the function
                                              ψ (a,b) (t, ν) − tν                                 (14)
is of relatively small magnitude, and hence that the rank of the matrix (11) is low. This is borne
out by our numerical experiments (see Figure 5 in particular).
We choose to approximate ψ (a,b) (t, ν) via the linear function νt rather than with a more complicated
function (e.g., a nonoscillatory combination of Bessel functions) because this approximation leads
to a method for applying the Jacobi transform through repeated applications of the fast Fourier
transform, if the non-uniform Fourier transform in the Hadamard product just introduced is carried
out via the algorithm in [31]. It might be more efficient to apply the non-uniform FFT algorithm in
[18], depending on different computation platforms and compilers; but we do not aim at optimizing
our algorithm in this direction. Hence, our algorithm for applying the Jacobi transform requires r
applications of the fast Fourier transform, where r is the numerical rank of a matrix which is strongly
related to (11). This makes its asymptotic complexity O prn log(n)q. Again, we do not prove a
rigorous bound on r here. However, in the experiments of Section 6.3 we compare our algorithm for
applying the Jacobi transform with Slevinsky’s       algorithm [33] ˘for applying the Chebyshev-Jacobi
                                                   2
                                            `
transform. The latter’s running time is O n log (n)/log(log(n)) , and the behavior of our algorithm
is similar. This leads us to conjecture that
                                                ˆ             ˙
                                                     log(n)
                                         r=O                    .                                  (15)
                                                  log(log(n))
Before our algorithm for applying the Jacobi transform can be used, a precomputation in addition
to the construction of the nonoscillatory phase and amplitude functions must be performed. Fortu-
nately, the running time of this precomputation procedure is quite small. Indeed, for most values
of n, it requires less time than a single application of the Jacobi-Chebyshev transform via [33].
Once the precomputation phase has been dispensed with, we our algorithm for the application of

# johansson_mezzarobba actual excerpts

Physical LF503-570
p̃k also satisﬁes (11) with |εn | ≤ 3 · 2−t , and Proposition 5 applies. The ﬁnal values
of q and p are respectively ⌈2t p̃n ⌋ and ⌈npn−1 /dn−1 ⌋ = ⌈2t p̃n−1 + αn−1 ⌋, whence the
bound (14).
    We do not use asymptotically faster evaluation techniques for large n in combi-
nation with this recurrence, since the series expansions to be presented next perform
very well in this case.
    4. Series expansions. For large n or p, we employ series expansions of Pn (x)
with respect to either n or x rather than the algorithm from the previous section. The
coeﬃcients of the series are also computed by recurrence, but fewer than n terms will
typically be required. Let us now review the various series expansions that we are
using (an asymptotic expansion as n → ∞, series expansions at x = 0 and x = 1),
before discussing their eﬃcient evaluation in the next section.
    4.1. Asymptotic series. For ﬁxed |x| < 1 or equivalently x = cos(θ) with
0 < θ < π, an asymptotic expansion for Pn (x) as n → ∞ can be given as [6, Eq. 3.4]
                                            1/2 K−1
                                                  X
                                      2                         cos(αn,k (θ))
(17)          Pn (cos(θ)) =                              Cn,k                 + ξn,K (θ)
                                  π sin(θ)
                                                   k=0
                                                                  sink (θ)

(for arbitrary K ≥ 1), where
                                        [Γ(k + 1/2)]2 Γ(n + 1)
(18)                       Cn,k =                                ,
                                      π2k Γ(n + k + 3/2)Γ(k + 1)

                       αn,k (θ) = (n + k + 1/2)θ − (k + 1/2)π/2,

and the error term satisﬁes
                                                            1/2
                                                      2              Cn,K
(19)                       |ξn,K (θ)| < 2                                    .
                                                  π sin(θ)          sinK (θ)
The coeﬃcients Cn,k are a hypergeometric sequence with

                  Cn,k       (2k − 1)2                           1      4n
(20)                    =                 ,              Cn,0 = √               .
                 Cn,k−1   4k(2n + 2k + 1)                         π (n + 21 ) 2n
                                                                              n

To evaluate the error bound, we can use the following inequality deduced from (18):
                             1       k!n!        1     k!
(21)              Cn,k ≤                     ≤             ,                n, k ≥ 1.
                           πn1/2 2k (n + k)!   πn1/2 (2n)k

10                     FREDRIK JOHANSSON, MARC MEZZAROBBA


     The condition |ξn,K (θ)| ≤ 2−p is satisﬁable as soon as sin(θ) ≥ (p + 3) ln(2)/(2n),
as we can see by choosing K = ⌊2n sin(θ)⌋ and using the inequality k! ≤ k k+1/2 e1−k .
Since the Gauss-Legendre nodes are distributed linearly in θ, the asymptotic expansion
gives a candidate algorithm for all but about (log(2)/π) p/n of the nodes as p/n → 0.
It is in fact a convergent series when 2 sin(θ) > 1, which allows evaluating Pn (x) to
unbounded accuracy for ﬁxed n when 16 π < θ < 65 π. The particular form (17) must
be used for this purpose; there is a slightly diﬀerent version of the expansion which
is asymptotic to Pn (x) (for ﬁxed K when n → ∞) but paradoxically converges to
2Pn (x) (for ﬁxed n when K → ∞); see [25, Section 10.3] and [26, Section 18.15(iii)].
     We can restate (17) as a hypergeometric series by working with complex numbers.
Letting ω = 1 − (x/y)i, with x = cos(θ) and y = sin(θ) as usual, we have
                                  √ −i π i(n+1/2)θ ik(θ−π/2) −k √ exp(i αn,k (θ))
     (1 − i)(x + iy)n+1/2 ω k =    2e 4 e         e         y = 2                 ,
                                                                     sink (θ)
and hence
                            "                     K−1
                                                              #
                       1                          X
(22)         Pn (x) = √   Re (1 − i)(x + yi)n+1/2     Cn,k ω k + ξn,K (θ).

Physical LF633-692
                                                    p        n
                       |Pn (z)| ≤ |Pn (i|z|)| ≤ |z| + 1 + |z|2 .

Therefore, the possible cancellation assuming that |Pn (x)| ≈ 1 is about
                                                          p         
                                  pA = n log2 |x| +        1 + |x|2
                                  √
bits (which is at most n log2 (1 + 2) ≈ 1.27 n), so using ball arithmetic with about
p + pA bits of working precision for the series evaluation gives p-bit accuracy.
       4.3. Expansion at one. Expanding at x = 1 yields
                                    n
                                    X                             
                                                  k            n n+k
(27)                     Pn (x) =         cn,k u ,     cn,k =
                                                               k   k
                                    k=0

where u = (x − 1)/2. The coeﬃcients cn,k are hypergeometric with initial value
cn,0 = 1 and term ratio

                                   cn,k    (n − k + 1)(n + k)
(28)                                     =                    .
                                  cn,k−1           k2

As in the previous section, we can truncate (27) and bound the error by comparison
with a geometric series.
       Proposition 8. The error when truncating (27) after the k = K−1 term satisfies
                  n
                  X                cn,K |u|K                      (n − K)(n + K + 1)
(29)                   cn,k uk ≤             ,         α = |u|
                                     1−α                               (K + 1)2
                 k=K

provided that α < 1.
    For u ≥ 0, (27) does not suﬀer from cancellation. For u < 0, we can estimate the
amount of cancellation from the magnitude of Pn (x′ ) where |u| = (x′ − 1)/2. For not
too large x′ ≥ 1, a very good approximation is
                                  ∞
                                  X n2k                          p            √
                          ′
                    Pn (x ) ≤ 2              2
                                               |u|k = 2 I0 (2n    |u|) ≤ 2 e2n |u| .
                                        k!
                                  k=0

12                       FREDRIK JOHANSSON, MARC MEZZAROBBA
                               p
We therefore need about 2n max(0, −u)/ ln(2) bits of increased precision.
      We can compute Pn′ from Pn and Pn−1 , but since this involves a division by 1−x2 ,
                                                                             Pn−1
it is better to evaluate Pn′ directly when x is close to 1. We have Pn′ (x) = k=0 c′n,k uk
where c′n,k = (k + 1)cn,k+1 /2 satisﬁes

                               n(n + 1)          c′n,k        (n − k)(n + k + 1)
(30)                 c′n,0 =            ,                 =                      .
                                  2             c′n,k−1            k(k + 1)

Since c′n,k ≤ ncn,k+1 , the analog
                       n
                       X                             

Physical LF1010-1022
than the three-term recurrence since the asymptotic expansion converges to suﬃcient
accuracy after O(1) terms for all suﬃciently large n. With the constant precision
p = 64, the main algorithm is 3.0 times faster for n = 103 and 30 times faster for
n = 104 . Conversely, fast multipoint evaluation with constant p is a factor O(n)
slower than our algorithm due to the higher internal precision.
     When p ∝ n (the three remaining plots in Figure 2), the main algorithm appears
to show the same O(n) speedup over the three-term recurrence after the crossover
point, at least initially. This speedup should level oﬀ asymptotically, but in practice
this only occurs for n larger than 104 where we have already gained a factor 10 or
more. The leveling oﬀ is visible in the bottom right ﬁgure (p = 10n).
     Fast multipoint evaluation gives a true asymptotic O(n) speedup, but since it has
much higher overhead, it only starts to give an improvement over the main algorithm
from n ≈ 104 and for p larger than n. When p = n/10, it appears that fast multipoint
