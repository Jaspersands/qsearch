# 2026-11-13 Binary recoupling source gate and bounded Legendre admission

## Decision

The inspected sources do NOT admit a polylogarithmic arbitrary-binary Hahn
or Clebsch--Gordan compiler. They also do not justify simply quantizing the
classical butterfly tables. A direct Gaussian singlet postselection proposal
has a numerical-spin success cost, as quantified below.

After the parent's distinct proposal during this review, admit at most ONE
bounded construction attempt: a clean Gauss--LEGENDRE unitary via dyadic
low-phase interpolation and high-phase Fourier/LCU blocks. This is not a
Hahn transfer or a completed theorem. Its random-access analytic and circuit
lemmas are precise unpaid obligations. No novelty or advantage is inferred.
STATE/TRAPS and actual retained primary sections were read; no network/API/Git,
archives, implementation, numerical optimization, or shared-status edit occurred.

## 1. What the actual QUT theorem says

Duong--Hosters, *Efficient quantum ultraspherical transform and a well-conditioned
quantum spectral method*, arXiv2611.06651v1, is retained as
`sources/2026-11-13-binary-recoupling/ultraspherical.txt`.
Physical LF183--228 define the EXACT matrix

    (Q_N^(m))_(k,j)=sqrt(w_j)*C_k^(m)(x_j)/sqrt(h_k^(m)),
    h_k^(m)=pi*2^(1-2m)*Gamma(k+2m)/[k!*(k+m)*Gamma(m)^2],

where x_j are zeros of C_N^(m), and w_j are Gauss weights for
(1-x^2)^(m-1/2) dx. Gaussian quadrature makes its rows orthonormal, hence
it is an N-dimensional unitary. Its columns are WEIGHTED GAUSS samples,
not equally spaced integer Hahn inputs.

Actual Theorem1, LF239--286, fixes an integer m>=2 and requires
K=N+m=2^n. It gives a clean unitary on the valid N-dimensional subspace,
uniform norm error <=epsilon, including unused-label/ancilla leakage, and
the same guarantee for its adjoint. The stated gate count is

    O_m(n^3 log(n/epsilon)+n log^2(1/epsilon)),

with O_m(log n+log log(1/epsilon)) ancillas. Classical circuit parameters
are computable in poly(n,log(1/epsilon)) time. Thus this theorem is NOT
merely dense preprocessing, a supplied node table, or a nonunitary map.
Its constants depend on fixed m. The proof's explicit final scope at
LF1472--1491 counts arbitrary single-qubit rotations and CNOTs and excludes
input preparation and discrete-gate synthesis. Those exclusions must remain.

The mechanism (LF502--548,597--625) uses
G_k(theta)=sin^m(theta)*p_k^(m)(cos(theta)), finite trigonometric expansions,
a Fourier transform, small grid shifts, diagonal quadrature corrections,
and a unitary completion of the coefficient map. The m-dependent Darboux
ladder has m-1 steps; the theorem does not bound it in log m.

The source identifies this with Jacobi alpha=beta=m-1/2 (LF959--967).
Its extension discussion does NOT prove all fixed Jacobi transforms: even
for asymmetric half-integer parameters, an endpoint-divergent separated
coefficient can cost O(N) block subnormalization (LF970--980). LF1026--1041
also limits its exact finite-order Fourier intertwiner to half-integer
Jacobi parameters. Legendre alpha=beta=0, i.e. Gegenbauer parameter 1/2,
is outside Theorem1. This is a limitation of that particular construction,
not an impossibility theorem for approximate Legendre circuits.

## 2. Why neither retained transform transfers to binary Hahn

Prakash et al., `sources/binary_fock_kerr/prakash.txt`, Definition3.13
(LF1553--1585), defines the different discrete matrix

    U_H(x,l)=sqrt(rho(x)/h_l)*Q_l(x;alpha,beta,N),
    rho(x)=binom(alpha+x,x)binom(beta+N-x,N-x),  x=0,...,N.

Its actual Theorem3.15 (LF1924--1953) allows arbitrary nonnegative integer
alpha,beta,N but costs O(N polylog((N+alpha+beta+1)/epsilon)) gates and
O(N+polylog((N+alpha+beta+1)/epsilon)) qubits. Its CG identification uses
j1=(N+alpha+beta)/2, j2=N/2, M=(beta-alpha)/2. The numerical N dependence
is exponential in binary-spin input length. The source itself retains the
Hahn bottleneck in the Jacobi/oscillator discussion (LF2371--2388), including
the extra coherent radial-label erasure problem. A scalar coefficient or
one prepared eigenstate does not perform this arbitrary-superposition map.

QUT changes both the polynomial family and the quadrature grid; its fixed
m does not cover growing alpha,beta. Its N+m power-of-two condition cannot
be removed merely by padding a different quadrature transform. No source-
proved inexpensive unitary bridge to the Hahn matrix was found. The known
Krawtchouk/beam-splitter compiler remains prior art and is not revisited.

Bremer--Yang, `sources/2026-11-13-binary-recoupling/fast_jacobi.txt`, restricts
its algorithm to a,b in (-1/2,1/2), explicitly noting loss of accuracy and
eventual failure for growing parameters (LF35--56). Its weighted Gauss
transform is itself orthogonal (LF154--166); do not incorrectly call the
target nonunitary. But its classical factorization stores n-by-r and r-by-n
tables, all n nodes/weights, and an n-by-26 low-degree block (LF919--968).
It costs O(rn) preprocessing and O(rn log n) application. The quoted
r=O(log n/log log n) behavior is a numerical conjecture (LF1062--1073),
and the displayed interpolation construction uses requested accuracy 10^-12
(LF990--1000), not a proved arbitrary-precision binary-parameter clock.
Neither the table entries' coherent access nor the norms of the nonunitary
factor blocks are supplied free by that arithmetic complexity result.

## 3. Cheap check on direct Gaussian singlet conditioning

Take two equally squeezed mode pairs in the Schwinger singlet pairing.
Writing r for the geometric parameter, their normalized joint amplitudes
are (1-r)*r^((a+b)/2)*(-1)^b on occupation patterns
(a,b) for party one and (b,a) for party two. Conditioning each party's
total occupation to N produces the spin-N/2 singlet, with probability

    P_N(r)=(N+1)(1-r)^2 r^N.

For N>=1 its maximum is at r=N/(N+2), and equals
4(N+1)N^N/(N+2)^(N+2)=Theta(1/N). In particular it is <=4/(N+2).
Ordinary amplification of THIS projected Gaussian branch therefore costs
Theta(sqrt(N)) uses at its optimum, not polylog N. This is not a general
Gaussian/CG lower bound: the resulting singlet already has an easy direct
uniform-superposition construction. It rejects postselection as an unpaid
shortcut and supplies no full coupling transform.

## 4. One distinct operation worth a bounded construction attempt

The parent's new target is ONLY the N-dimensional Gauss--Legendre unitary

    L_(j,k)=sqrt(w_j*(2k+1)/2)*P_k(cos(theta_j)),

where cos(theta_j) are zeros of P_N and w_j its Gauss weights. Input is
arbitrary amplitudes on binary labels 0<=k<N; output is the weighted
Gauss-sample amplitude vector, with all work returned clean and uniform
operator error <=epsilon. Desired uniform preprocessing and gate costs are
poly(log N,log(1/epsilon)), without an N-entry table or unknown-state inverse.
The classical fast-Jacobi transform is a real comparator for this fixed
parameter, but has a different expanded-vector access/output model.

Reflect theta into (0,pi/2], using P_k(-x)=(-1)^k P_k(x). Partition the row
distance from the nearest endpoint into dyadic sizes J and k+1 into dyadic
sizes K. Put p=JK/N. There are O(log^2 N) rectangles. Under certified
uniform bounds theta_j=Theta(J/N), w_j=O(J/N^2), the elementary |P_k|<=1
gives entries O(sqrt(p)/sqrt(N)). A separated rank-one rectangle carries
an additional sqrt(JK) normalization, so the crude low-phase block cost is
O(p), NOT O(sqrt(p)). It is still polylogarithmic when p<=L=polylog(N/epsilon).

There is a concrete cancellation-preserving low-phase evaluator. The
Mehler--Dirichlet integral, after t=theta*sin(phi), is

    P_nu(cos(theta))=(2/pi) integral_0^(pi/2)
       cos((nu+1/2)*theta*sin(phi))
       /sqrt(sinc(theta*(1+sin(phi))/2)
             *sinc(theta*(1-sin(phi))/2)) dphi.                    (1)

Here sinc(z)=sin(z)/z with its continuous value at zero. The apparent
endpoint singularity cancels exactly. On real theta<=pi/2 the denominator
is bounded away from zero, and when nu*theta=O(L) the oscillation is O(L).
Real interpolation samples are bounded by a constant, so a certified
degree-poly(L,log(1/delta)) bivariate Chebyshev interpolation would also have
polynomial coefficient l1 norm. This is a plausible separable LCU operation,
not an invocation of the exact finite Darboux ladder excluded by the source.

Two named obligations remain before claiming the compiler:

1. **Uniform analytic/random-access lemma.** Prove the required node/weight
   enclosures and their reversible per-index evaluation in poly(log N,
   log(1/delta)) BIT time; prove the low-phase complex-neighborhood remainder
   and a high-phase Watson/Darboux remainder uniform at k*sin(theta)>=L.
   High-phase terms must separate exp(+-i(k+1/2)theta) from bounded local
   amplitudes. Global endpoint-divergent coefficients may not be normalized
   separately. No fixed-precision numerical rank experiment pays this lemma.
2. **Full coherent block composition.** Give the Fourier-grid relabeling,
   dyadic selectors and scalar oracles without tables; account for every
   block normalization and the sum over all rectangles; and prove a clean
   near-unitary completion/OAA with actual inverses and fixed-gate precision.
   Allocate global operator-norm error, e.g. conservatively delta_entry
   <=epsilon/[N*polylog(N/epsilon)], rather than only pointwise epsilon.

A Gauss-node displacement N*Delta_j=O(1) would make the phase correction
exp(i*k*Delta_j) amenable to a short Taylor LCU, but this bound, its oracle,
and the chosen Fourier modulus/relabeling must be proved. The source QUT's
power-of-two dimension condition is not automatically a circuit for this grid.

The cheapest decisive failure is a high-phase remainder, coherent scalar
oracle, or block normalization that still grows as a positive power of N
after restricting to its declared rectangle. Conversely, proving these two
lemmas would close THIS fixed-parameter Legendre transform, not arbitrary
Hahn, binary CG, a Racah transform, or a downstream spectral-solver endpoint.
That single construction attempt is admissible; the original binary-Hahn
transfer and a further Krawtchouk repetition are not.

All source paths above are relative to `research/audits/`; locators are
physical LF counted with split('\n'). The stated primary theorems were read
at the cited scope, not independently reproved in full by this admission check.
