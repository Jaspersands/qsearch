# 2026-11-13 — Independent coherent Gauss–Legendre construction

**Disposition.** The dyadic construction closes at the stated coherent-transform
scope. Combined with the independently proved per-index scalar routine, it gives
a uniform clean circuit for the exact Gauss–Legendre orthogonal matrix, with
operator error at most epsilon and gates/workspace polynomial in log N and
p=ceil(log2(1/epsilon)). Classical generation costs B_epsilon+poly(log N,p),
where B_epsilon pays reading an arbitrary rational accuracy encoding; a
dyadic requested accuracy needs no extra input convention. No array of N nodes, postselection,
unknown-state inverse, or unproved butterfly factorization is used.
This is a mathematical construction, not an implementation or an advantage,
novelty, Hahn/CG, Jacobi-family, or differential-equation claim.

Inputs checked: current STATE/TRAPS, the topic/contract, actual
Johansson–Mezzarobba (JM) LF507–539, actual QSVT Corollaries10/18 and Lemma19
(retained `sources/periodic_conduction/qsvt.txt`, LF745–759,1150–1215), and
the complete 186-line `2026-11-13-legendre-scalar-source.md` proof. The two
empty paid reports supply no evidence. Below, indices j=1,...,N are one-based.
Round epsilon down to a dyadic in [epsilon/2,epsilon]; the ordinary reading
cost of a supplied rational accuracy is charged. Use this dyadic below.

## 1. Native scalar interface and partition

The scalar review proves, with fixed polynomial BIT caps, theta_j and w_j
to absolute/relative requested precision, separately for every index. In
particular, with nu=N+1/2 and bar(theta)_j=(j-1/4)pi/nu,

    |theta_j-bar(theta)_j| <= pi/(4nu),
    (2/5) sin(theta_j)/N <= w_j <= 4 sin(theta_j)/N.

The weaker displayed lower weight bound suffices here. Its proof and root
stopping rule, not the source's all-root theorem, are the scalar interface.
The same review pays log-Gamma ratios by shifted Stirling with remainder;
it does not materialize a factorial of binary degree. All scalar algorithms
can be reversibly run to their worst-case cap. Invalid labels use a fixed
valid dummy index and a zero-mask branch, never an unsafe division.

N=1 is the identity. Otherwise pad the data register to dimension M, the
power of two in [8N,16N), and target U_ext=U_N direct-sum I_(M-N).
Gauss quadrature applied to P_k P_l proves U_N^*U_N=I: its degree is at most
2N-2, and integral P_k P_l=delta_kl/(k+1/2). Padding removes any need for
an assumed rank-N polar decomposition after numerical perturbation.

Use rows j<=ceil(N/2), with the odd center included once, and reflect the
other rows by P_k(-x)=(-1)^k P_k(x). Partition these j and the labels k+1
into power-of-two intervals J<=j<2J, K<=k+1<2K. Exact masks clip the final
intervals and exclude the center from the reflected copy. There are at
most 2(1+ceil(log2 N))^2 rectangles. Put p=JK/N and

    H=32+ceil(log2(N/epsilon)), R=H, L=16H.

Call a rectangle low when p<=L, high otherwise. From the indexed brackets,
on a valid positive-half rectangle

    sin(theta_j)>=2J/(3N),  theta_j<=min(2pi J/nu,pi/2).

For K>=2, k>=K/2. K=1 rectangles are always low. These inequalities also
show that all small denominators below lose only O(log N) scalar bits.

## 2. Low phase: analytic domain, finite coefficients, actual clock

Set Q=2K, Theta=min(2pi J/nu,pi/2), u=(k+1/2)/Q, v=theta_j/Theta.
Then u,v are in [0,1] and Q*Theta<=4pi L. Mehler–Dirichlet with
t=theta sin(phi) gives the nonsingular function

 F(u,v)=(2/pi) integral_0^(pi/2)
   cos(Q*Theta*u*v*sin(phi))
   /sqrt(sinc(Theta*v*(1+sin(phi))/2)
         *sinc(Theta*v*(1-sin(phi))/2)) dphi.                 (1)

It agrees with P_k(cos(theta_j)) at the desired arguments. At theta=0
use the analytic value sinc(0)=1. For complex arguments the square root
means the product of the two separately chosen principal square roots.

There are explicit fixed complex neighborhoods. Map the Bernstein ellipse
of parameter 2 to [0,1], in BOTH u and v, and take |Im(phi)|<=1/8.
Then |u|,|v|<=9/8 and |sin(phi)|<=cosh(1/8)<9/8. Both sinc arguments
therefore have modulus at most 153pi/256<2. For |z|<=2,

    |sinc(z)-1| <= sinh(2)/2-1 < 5/6.

Thus each sinc lies in Re(z)>1/6, its principal inverse square root is
analytic, and their product has modulus at most 6. The integrand is bounded
by M_0=6 exp(20L). On the REAL domain each sinc is at least 2/pi and the
cosine has modulus at most 1, so |F|<=pi/2. The exponential complex bound
controls degree; it does NOT become an exponential coefficient norm.

The integrand is even and pi-periodic in phi: changing sin(phi) to its
negative exchanges the two sinc factors. Hence (1) is its full-period
average. Q_phi equally spaced trapezoidal samples have error at most
2 M_0/(exp(Q_phi/8)-1), by the Fourier coefficient bound in this strip.
Choose Q_phi the power of two just above 4096H. This error is <2^(-80H).
All samples are at real arguments of size O(L), with sinc bounded away
from zero. Range-reduced series, integer square roots and interval
arithmetic evaluate them to the same precision in poly(H) bit operations.
Computing q=Q*u and theta=Theta*v separately needs only O(log N) guard
bits even though their product is bounded. No degree-N recurrence occurs.

Interpolate F on the tensor Chebyshev–Lobatto grid, degree d=1024H in each
variable. The analytic Chebyshev tail, including interpolation aliasing,
is at most 64 M_0 2^(-d). In the finite DCT formula each two-dimensional
coefficient is bounded by 4 max|F|<=2pi<8. Compute the samples and DCT,
then round coefficients to dyadics with error <=2^(-64H). Their signs
are the signs of these finite dyadics; no exact-zero decision is required.
The resulting polynomial

    F_d(u,v)=sum_(a,b=0)^d c_ab T_a(2u-1) T_b(2v-1)

satisfies, conservatively,

    |c_ab|<=16,  sum|c_ab|<=16(d+1)^2,
    sup_[0,1]^2 |F-F_d| <= 2^(-32H).                       (2)

For example the sampled-data error contributes at most
4(d+1)^2*2^(-80H), and coefficient rounding contributes
(d+1)^2*2^(-64H); the displayed constants dominate these for H>=32.
There are only O(H^2) coefficients per rectangle. Direct quadrature and
DCT, without any fast-transform assumption, have a polynomial BIT clock.
This explicitly resolves the endpoint analytic/separation obligation.

## 3. Low rectangle block: no hidden projection probability

Define a_j=sqrt(N^2 w_j/J)<6 and b_k=sqrt((k+1/2)/K)<2. Then

    U_jk=(sqrt(JK)/N) a_j b_k F(u_k,v_j).

Known unitaries A_J,B_K prepare the uniform states on the FULL intervals
of sizes J,K. They use Hadamards on log J or log K bits and reversible
addition/reflection; truncated intervals are handled by the masks above.
The successful block of A_J Pi_0 B_K^* is exactly
|uniform_J><uniform_K|. Pi_0 is a flag for a zero data label. Its entries
are 1/sqrt(JK); this is not preparation by projecting a uniform N-state.

For each coefficient, place bounded diagonal blocks
(a_j/6)T_b(2v_j-1) and (b_k/2)T_a(2u_k-1) around that rank-one block.
Its coefficient normalization is exactly

    12*(JK/N)*c_ab.

Consequently a low rectangle costs at most 192 p(d+1)^2 in LCU norm.
The factors are ordered with the row factor AFTER and column factor
BEFORE the rank-one map. Products have separate signal registers.
Together with sqrt(w_j(k+1/2))<=2, (2) gives the claimed tiny entry error.

## 4. High phase: summable, uniformly computable coefficients

Use the actual JM expansion/remainder in LF507–539. Write
b_kr=sqrt(k+1/2) C_kr. Gamma log-convexity gives b_k0<=1, and its exact
coefficient ratio gives

 C_(k,r+1)/C_kr=(r+1/2)^2/[2(r+1)(k+r+3/2)]
                 <=(r+1)/(2k).

Put s_0=J/(2N), lambda_r=r!/(K s_0)^r=r!(2/p)^r. The column factors

    h_kr=b_kr K^r/r!

are at most 1, since h_k0<=1 and their successive ratios are at most
K/[2(k+r+3/2)]<=1. The row factors (s_0/sin(theta_j))^r are also at
most 1. Finally a'_j=sqrt(2Nw_j/(pi sin(theta_j)))<2. The r-th term of
the weighted matrix is therefore lambda_r times these bounded row/column
factors and a'_j, times

    [ exp(ik theta_j) exp(i(r+1/2)(theta_j-pi/2))
      + exp(-ik theta_j) exp(-i(r+1/2)(theta_j-pi/2)) ]/(2 sqrt N).

For p>16R, lambda_(r+1)/lambda_r<=1/8 through r=R-1. Hence their sum
through R-1 is <=8/7, and the weighted remainder is at most
4*8^(-R)/sqrt N. There is no endpoint-divergent global coefficient norm.
For finite evaluation, h_k0 uses the scalar review's log-Gamma routine,
and h_kr is obtained by R bounded rational factors, not by forming K^r
and an enormous unnormalized coefficient separately. Their numerators
and denominators have O(R(log N+log R)) bits. Row powers and phases use
the paid node/weight routine and O(R) ordinary arithmetic operations.

## 5. The Fourier core has constant normalization and no permutation table

Define exactly, by rational nearest-integer arithmetic,

    a(j)=round(M*(j-1/4)/(2N+1)).

This is injective on the positive-half indices. Given a grid label a,
the only inverse candidate is round((2N+1)*a/M+1/4); check its allowed
range and recompute a(j). The rounding error in this inverse is at most
(2N+1)/(2M)<1/2. Thus forward injection AND inverse membership are
poly(log N) reversible computations. No root-dependent rounding branch
or N-entry permutation is used. A clean partial-isometry block is obtained
by computing the candidate and membership flag, erasing the original
label using the forward map on the valid branch, and swapping registers;
all invalid branches retain a nonzero failure flag. This is a unitary
circuit extension, not an assumed partial inverse oracle.

Set Delta_j=theta_j-2pi a(j)/M. The midpoint root bound gives

    |N Delta_j| <= pi/4+pi/8 < 2.

A restricted power-of-two QFT_M supplies exp(2pi i k a(j)/M)/sqrt M.
Normalization sqrt(M/N)<4 supplies the N-normalized base. Correct it by

    exp(ik Delta_j)=sum_(t=0)^(T-1)
       (i^t 2^t/t!)*(k/N)^t*(N Delta_j/2)^t + remainder,
    T=64H.

All row/column factors have modulus <=1, and the coefficient sum is <=e^2.
The remainder is <=e^2 2^T/T!<2^(-64H). Negative phases use QFT_M^*.
Thus each Fourier core has LCU normalization <4e^2. Combining Section4's
two half-weighted phases gives high-rectangle normalization <128. Right
half reflection adds just the exactly computable column sign (-1)^k.

## 6. Native finite arithmetic and the assembled block

Each matrix entry belongs to exactly one of the rectangles/reflections.
The preceding analytic errors are each below epsilon/(4096N), so the
Frobenius bound, ||E||<=N max|E_jk|, pays the full operator error.
Add the known padded identity as one further successful block. Let

 alpha be a power of two >=
   1+2(H+1)^2 [192L(d+1)^2+128],

taking the smallest such power. Then alpha=O(H^5). There are O(H^4)
LCU terms, including the high r,t expansion. This is a polynomial-sized
classically computed coefficient list, not a node/factor table of size N.

All computed diagonal block functions are first rounded to absolute accuracy
xi=epsilon/(2^16 alpha). Bounded real values are clipped to their stated
intervals; for a unit phase, round its real angle. Chebyshev evaluation loses at most its polynomial derivative
bound d^2 on [-1,1]; clipping prevents an accidental extrapolation.
The weight lower bound pays square roots/reciprocals; the smallest sin
used is >=2/(3N). Node errors entering Delta are multiplied by N.
The O(R+d) bounded product/recurrence steps and all divisions therefore
need only xi-bit precision plus O((R+d)(log N+log(R+d))) guard bits.
The scalar routine has a fixed polynomial clock at this precision.
The real coefficient table already has the precision proved in Section2.
Known QFT angles remain exact in this intermediate mathematical word;
their finite gate errors are charged in Section8, not hidden in this bound.

LCU preparation can itself avoid all tiny-probability divisions. For each
nonnegative coefficient magnitude w_l, allocate floor(2^b w_l/alpha)
uniform b-bit selector labels to its signed block, and allocate the
remaining labels to a zero block. Hadamard preparation/unpreparation
and interval comparisons implement this. Taking
b>=ceil(log2(2^16 alpha * number_of_terms/epsilon)) bounds the resulting
UNNORMALIZED matrix error by epsilon/2^16. Every weight is an explicit
polynomial-bit rational (or already approximated to that accuracy).
Signs and powers of i are retained under control. There is no sampling,
postselection, division by a tiny branch probability, or precision loop.

After these scalar roundings let W be the EXACT mathematical unitary
word whose elementary rotations use those finite, computable parameters.
Its all-zero-ancilla block is A/alpha, with

    ||A-U_ext|| <= delta,   delta=epsilon/32.               (3)

The constants above leave ample room in (3): a product has only a constant
number of separately encoded diagonal factors, so its scalar errors sum
to O(alpha*xi), and coefficient allocation was charged separately.
All masks and label permutations are exact. No polar vectors are computed.

## 7. Explicit clean polar amplification, including leakage

Define the bounded odd rational polynomial

 P_m(x)= [integral_0^x (1-t^2)^m dt]/[integral_0^1 (1-t^2)^m dt],
 m=ceil(64 alpha^2(H+1)),   eta=epsilon^2/2^16.

Its degree is 2m+1, its coefficients have polynomial(m) bit length and
are generated by the binomial formula. It is odd and |P_m|<=1 on [-1,1].
The denominator is >=1/(2 sqrt(2m)). Integrating the Gaussian tail gives,
when m x^2>=1,

    0<=1-P_m(x)<=2 exp(-m x^2)   (0<x<=1).

Every singular value of A/alpha is >=1/(2alpha), by (3), so the displayed
m makes this error less than eta/8. One may replace P_m by
(1-eta/8)P_m to give a strict boundedness margin.

Actual QSVT Corollary10 supplies phase generation in polynomial degree
and log(1/accuracy) time. Corollary18 implements the real odd singular-value
polynomial using an extra |+> branch; Lemma19 counts uses of W,W^* and
the explicit zero-ancilla projector controls. Request polynomial error
eta/8 and round each phase to error eta/[64(2m+1)]. These statements are
used at their actual scope, with a polynomial-bit rational polynomial.
No unspecified phase list or infinite-precision primitive is supplied.

Write V for the polar factor of A. The successful block B of this ideal
QSVT word satisfies ||B-V||<=eta. Moreover ||V-U_ext||<=2delta, since
||V-A||<=delta. Unitarity of the entire QSVT word bounds its failure
component on every input by sqrt(2eta). Thus its CLEAN isometry error is
at most 2delta+eta+sqrt(2eta), already below epsilon/4.
Bounding only the successful block to O(epsilon) would not suffice;
the eta=O(epsilon^2) choice explicitly pays ancilla leakage.

## 8. Fixed gates, actual inverses, and a noncircular final clock

The elementary finite-gate compiler proved in Section4 of
`2026-11-13-jack-logprecision-independent.md` applies here. For completeness,
a real rotation is c I+s J, J=XZ, and a scalar phase has J=i I. A uniform
b-bit Hadamard selector assigns even counts to signed I,J approximating
c/2,s/2; unused counts cancel between I and -I. Its successful block is
U/2+O(2^-b). One ordinary oblivious-amplification iteration gives clean
error <=64*2^(-b/2), from the successful block 3B-4BB^*B and unitarity.
Threshold arithmetic, signs, reflections, and SELECT use only a fixed
palette H,S,X,Z,CNOT,Toffoli,controlled-H,controlled-S. Higher controls
are clean Boolean ANDs. This pays controlled scalar/global phases too.
There are no approximate rotations inside this bottom compiler.

For a diagonal block with desired real success amplitude f, use the
unitary rotation with entries f and sqrt(1-f^2); computing the square
root to absolute precision costs only twice the requested guard precision.
The QFT uses O(log^2 M) controlled phase gates. Its rotations, the row
phases, attenuation/block rotations, and the QSVT phases all have the
same finite compiler. Elementary sine/cosine values are computed by
range reduction and bounded series at polynomial bit cost.

First construct the finite high-level word, including its O(m) W uses,
arithmetic precisions and all projector controls. Its rotation count G
has an explicit polynomial(H) upper bound. Only THEN choose

    b >= 2 ceil(log2(256G/epsilon))+16.

The bottom Boolean arithmetic at this precision adds polynomial overhead
and introduces no new approximate gates. Hence there is no circular error
allocation based on its own final gate count. The hybrid error is <epsilon/4.
Every occurrence of W^* is the reversed word on the SAME workspace banks.
Different factors of a product have separate signal registers. An inverse
of a clean approximation to a unitary has the same clean error on that
unitary's range; the circuit hybrid uses this fact, not an assertion that
actual dirty scratch has silently reset. All lower compiler guarantees
hold for arbitrary logical inputs, including the upper control/signals.

In summary, R,T,d and quadrature counts are O(H), rectangle count O(H^2),
coefficient count O(H^4), alpha=O(H^5), and m=O(H^11); all remaining bit
precisions and finite programs have polynomial(H) caps. These are upper
bounds, not optimized exponents. Combining (3), polar/leakage error and
the final unitary hybrid gives the requested epsilon clean-operator bound.
Tensoring with an arbitrary reference preserves that bound. The compiler
has a fixed clock on every branch, and performs no measurement or retry.
