# Kerr coherent rejection: a theta compiler and an exact transfer obstruction

13 November 2026. Independent constructive audit; STATE/TRAPS and the three
specified native notes read. No API, network, Git, archives, numerical tests,
or live paid reports used. This does NOT establish a full native count sampler.

**Finding.** The modular theta proposal is valid, including a finite-bit,
fixed-clock sampler for its rounded phase law. But the direct continuous
condensate/Cauchy transfer has an explicit native family costing Omega(sqrt K)
trials, even with perfect theta sampling and amplitude evaluation. This is a
scoped falsifier of that transfer, not a lower bound on other classical methods.
An output-dependent Krawtchouk/two-branch transfer remains unpaid.

## 1. The modular envelope really has constant total mass

Write theta(z|tau)=sum_n exp(pi*i*tau*n^2+2*pi*i*n*z), tau=beta+i*alpha,
alpha>0. Here alpha,beta are binary rationals; real translations and linear
unit phases can also be supplied. First consider theta00 and z real modulo 1.
Reduce tau by gamma=[[A,B],[c,d]] in SL2(Z) so that

    tau'=(A*tau+B)/(c*tau+d)=u+i*v, |u|<=1/2, |tau'|>=1,
    v>=sqrt(3)/2, w=c*tau+d, v=alpha/|w|^2.

The usual T identity follows termwise; the S identity is the Fourier transform
of a Gaussian followed by Poisson summation. Composing these two identities
tracks the square-root phase and half-characteristics a,b exactly. In modulus,

    theta(z|tau) = phase*w^(-1/2)*exp(-pi*i*c*z^2/w)
                   *theta_[a,b](z/w|tau'),

where the displayed constant phase has modulus one. Since Im(z/w)=-c*v*z,
completion of squares cancels the entire real Gaussian prefactor. Therefore

    |theta(z|tau)|^2 <= |w|^-1 [sum_n exp(-pi*v*(n+a-c*z)^2)]^2.       (1)

This cancellation is exact; evaluating two exponentially large/small factors
separately is unnecessary. Let n0 be nearest to c*z-a and t=c*z-a-n0.
For |t|<=1/2, the sum divided by its largest term is at most

    1+2 sum_(k>=1) exp(-pi*v*(k^2-k))
      <=3+2 exp(-2*pi*v)/(1-exp(-2*pi*v)) <4.

Consequently a valid, deliberately loose majorant is

    E(z)=16*|w|^-1 sum_n exp(-2*pi*v*(n+a-c*z)^2).                    (2)

For c!=0 its integral is E_tot=16/sqrt(2*alpha). Its normalized density is
sampled by choosing j uniformly modulo |c|, drawing a real Gaussian Y with
density sqrt(2*v)*exp(-2*pi*v*Y^2), and putting
z=(a+j+Y)/c modulo 1 (the sign of c merely reverses the circle).
The binary residue j is sampled without enumerating |c| values.

Parseval and Poisson give the exact norm and lower bound

    Z=int_0^1 |theta|^2 =sum_n exp(-2*pi*alpha*n^2)
      =(2*alpha)^(-1/2) sum_m exp(-pi*m^2/(2*alpha))
      >=(2*alpha)^(-1/2).

Thus rejection with ratio |theta|^2/E accepts with probability Z/E_tot>=1/16.
For c=0 the reduction has alpha>=sqrt(3)/2; directly |theta|<2 and Z>=1,
so uniform-circle rejection with envelope 4 accepts with probability >=1/4.
No normalizing-theta oracle is needed in either case.

The same construction covers shifted Gaussian Fourier coefficients: allow
real rational characteristics a0,b0, rather than just half-characteristics.
T and S still give the displayed formula with real characteristics and a
unit constant; reduce characteristics modulo integers, retaining their phase.
The norm is now Z_a0=sum_n exp(-2*pi*alpha*(n+a0)^2).
Our reduction uses c!=0 only if the original alpha<1. In that case the interval
|n+a0|<=alpha^(-1/2) contains at least alpha^(-1/2) integers, so

    Z_a0>=exp(-2*pi)/sqrt(alpha).

The acceptance in (2) is therefore >1/10000, uniformly in the center.
If c=0, the largest-term bound gives a uniform-circle envelope equal to
16 times the squared largest Fourier coefficient, with acceptance >=1/16.
This pays arbitrary Gaussian centers; it does not pay a number measurement.

## 2. What the finite-bit theta statement means

A finite machine cannot output a real with TV-close continuous law. The actual
interface is: for supplied cell resolution R, output floor(2^R*z) with TV error
delta from that rounded ideal law, in polynomial BIT time in the rational-input
length, R, and log(1/delta). No assertion compares a finite atomic distribution
in TV directly with a continuous density.

Here is a constructive clock. Center Re(tau) by an integer T move, and invert
only while |tau|<1. While Im(tau)<1/2, every inversion at least doubles it.
Once Im(tau)>=1/2, one inversion and centering finish: if the inverted real
part needs a unit translation, its new squared modulus is
1+(1-2*|Re(tau)|)/|tau|^2>=1. The number of steps is O(1+log^+(1/alpha)).
Every integer translation has polynomial bit length, and the accumulated
matrix and transformed rational parameters have polynomial bit length.

For evaluation divide the transformed Gaussian series by its largest term.
Relative weights are exp(-pi*v*(k^2-2*k*t)), |t|<=1/2. Their sum is <4;
the squared-weight denominator is >=1. Truncating |k| at O(sqrt(log(1/delta)))
has uniformly exponentially small error. Relative phases use binary modular
arithmetic on n0+k, not a loop of length n0 or c. Underflowing exponential
terms are discarded at a stated absolute threshold. Elementary exp/sqrt/phase
evaluation to the requested bits therefore computes the rejection ratio
stably, even between narrow peaks. Carry the modular unit phases when complex
amplitudes are requested; magnitude evaluation alone is not a coherent oracle.

For completeness the Gaussian draw also has a bounded finite-bit realization.
Draw T=sqrt(v)*Y on a box [-L,L], L=O(sqrt(log(1/delta))), by uniform-box
rejection against exp(-2*pi*T^2); its tail is O(delta), acceptance is Omega(1/L),
and a polynomial number of capped trials pays its timeout. Uniform residue
sampling has a separate capped fair-bit rejection clock. Round each acceptance
probability on a sufficiently fine dyadic grid and allocate delta divided by
the total number of trials to each error; the outer acceptance is bounded below
as above, so its timeout uses O(log(1/delta)) trials with an absolute constant.

The required guard bits are polynomial, not inverse peak width in unary.
For a direct check, let H>=2 bound absolute transformed rational parameters,
their nonzero reciprocal magnitudes, and |c|+|d|. Its logarithm is polynomial
in the input bits. After largest-term scaling, derivatives of relative weights
and phases are bounded by a fixed polynomial in H times Gaussian k-moments.
Those moments are uniformly bounded since v>=sqrt(3)/2. The denominator >=1
then gives a polynomial-in-H Lipschitz bound for the ratio, piecewise across
nearest-integer boundaries; the ratio itself is continuous there. Similarly
the rounded-law boundary loss is bounded by 2^R times the phase displacement
times a density bound of polynomial size in H. Thus R+O(log H+log(1/delta))
working bits, with fixed extra guards for the finite sum, pay discretization.
This is a proof of an effective BIT interface, not an implemented sampler.

## 3. Exact native obstruction to the phase-only Cauchy transfer

This tests a concrete full-output route, without substituting an incoherent
mixture. Let b_n be the ACTUAL balanced first beam-splitter amplitudes, so
|b_n|^2=2^-K binom(K,n). For any final beam splitter B2 define the normalized
condensates and their efficiently sampled binomial count laws by

    |chi_z> = B2 sum_(n=0)^K b_n exp(2*pi*i*n*z)|n,K-n>.

Let r>=1, K=2*r^2, Q=100*r, mu=K/2, and use the native Kerr phase a/b=1/Q.
Both beam-splitter angles may be fixed rational turns, e.g. pi/4 and pi/8.
Define the periodic coefficient

    c_Q(z)=sum_(m in Z) exp(-pi*(m-mu)^2/Q^2)
                *exp(pi*i*m*(m-1)/Q)*exp(-2*pi*i*m*z).

The vector Phi=int_0^1 c_Q(z)|chi_z> dz is EXACTLY the native Kerr output
Psi with its pre-B2 number amplitudes multiplied by exp(-pi*(n-mu)^2/Q^2).
This is an explicit controlled approximation, not a new input promise.
For X=Bin(K,1/2)-K/2, E X^4=(3K^2-2K)/16, hence

    ||Phi-Psi|| <=(pi/Q^2)*sqrt(E X^4)
       <=pi*sqrt(3)*K/(4Q^2)=pi*sqrt(3)/20000 <1/3000.              (3)

The normalized Phi count law is within 1/1500 TV of the genuine native law,
uniformly in B2. Also ||Phi||<=1. Other fixed accuracies are obtained by
increasing the constant in Q; all input bit lengths remain O(log K).

Since mu is integral, c_Q is a real translation of theta(z|1/Q+i/Q^2)
times a unit phase. The exact modular matrix [[-1,0],[Q,-1]] gives

    w=i/Q, tau'=i-1/Q, v=1.

Section 1 therefore gives ||c_Q||_infinity<=4*sqrt(Q), whereas Parseval gives
||c_Q||_2^2>=Q/sqrt(2). It follows, without asymptotic estimates, that

    ||c_Q||_1 >= ||c_Q||_2^2/||c_Q||_infinity >=sqrt(Q)/(4*sqrt(2)),
    ||c_Q||_1^2>=Q/32.                                            (4)

Now allow ANY normalized nonnegative phase proposal rho, including one chosen
with knowledge of B2, and suppose its count mixture is sampled by first z~rho
and then the condensate count law. Write

    p_rho(j)=int rho(z)*|chi_z(j)|^2 dz,
    A_rho=int |c_Q(z)|^2/rho(z) dz.

The generic coherent Cauchy bound is |Phi_j|^2<=A_rho*p_rho(j). Rejection
against this envelope is correct and keeps the cross terms. Nevertheless

    A_rho >= (int |c_Q|)^2 >= Q/32,
    success = ||Phi||^2/A_rho <=32/Q.                              (5)

Zeros of rho on nonzero c only make A infinite. The inequality follows from
ordinary Cauchy, with the optimal phase-only choice rho proportional to |c_Q|.
Choosing the directly compiled rho proportional to |c_Q|^2 costs its L2 norm
instead and likewise requires Theta(Q) trials. Even a free exact Phi_j oracle
does not remove (5). A polynomial-in-log K capped run of THIS rejection
architecture succeeds with probability tending to zero.

Thus fast theta sampling does not by itself remove numerical revival-branch
cost. An output-dependent tighter envelope, or a different reconstruction,
is not covered by this obstruction. The native sampler itself remains open.

## 4. Opposite-angle coherence and the remaining constructive obligation

The pointwise inequality |psi(phi)+exp(i*t)*psi(-phi)|^2
<=2*(|psi(phi)|^2+|psi(-phi)|^2) is a valid coherent rejection majorant.
It is not a free normalization guarantee: if Z=int |psi|^2, acceptance for
this circle density is ||psi+exp(i*t)*psi(-.)||_2^2/(4Z), which may vanish.
For even theta00 and t=pi the numerator is identically zero. A genuine native
output construction must pay its GLOBAL normalization rather than normalize
each potentially cancelling pair independently.

The exact small-period comparator also forbids discarding the cross term.
With balanced input, a/b=1/2 and final B(theta), the two Fourier condensates
(i,1)/sqrt(2) and (-i,1)/sqrt(2) acquire phases exp(+-i*K*theta), giving

    P_theta(y)=2^-K binom(K,y)*(1+(-1)^y*sin(2*K*theta)).

At theta=+-pi/(4K), the two laws are supported on opposite parities and have
TV distance one. Their prefix differences are exactly
2^(1-K)*(-1)^s*binom(K-1,s), with supremum O(K^-1/2). This family is ALREADY
handled by the finite-period coherent branch sampler. It is a stress test
for coherence and precision, not hardness or a failure of rejection in general.

A full route must now construct and sample an OUTPUT-dependent count envelope
for sum_n (B2)_(j,n)*b_n*exp(pi*i*(a/b)*n*(n-1)), evaluate its complex
amplitudes stably, and bound envelope mass by poly(log K,1/epsilon) uniformly.
Bulk two-saddle formulas do not pay endpoints, coalescing saddles, near-trivial
rotations, or near revivals. The theta theorem above supplies no such estimate;
the lower bound (5) shows why a generic phase-only Cauchy substitute is inadequate.
No unread Krawtchouk asymptotic theorem, CD compiler, or Hiary extension is used.
The strongest retained native baseline remains the numerical-period coherent
sampler. No full classical match, speedup, hardness, novelty, or implementation
claim follows from this review.
