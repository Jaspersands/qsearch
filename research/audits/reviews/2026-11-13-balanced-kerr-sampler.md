# Balanced one-pulse Kerr: coherent classical sampler composition

13 November2026. Parent derivation, repaired after full independent composition review. This combines
specific proved components, not a numerical asymptotic extrapolation.

## Contract and dependency boundary

For every binary K>=1, rational zeta=a/b, and rational 0<epsilon<=1/4,
start |K,0>, apply B(pi/4), exp(2pi i zeta binom(N,2)), B(pi/4), and sample
one count within epsilon total variation. The proposed classical BIT bound is
poly(log(K+1),bitlength(zeta),1/epsilon). No oracle, supplied advice, numeric-K
input expansion, or postselection is free. General passive angles are excluded.
K=0 is immediate. This is a WRITTEN algorithm, not an implementation or a
novelty/separation claim. Dependencies individually parent-read in full:

* balanced-kerr-kernel.md: absolute coherent all-parity kernel, C=2^16.
* balanced-kerr-endpoints.md: endpoint amplitude absolute 2^-p, polynomial
  in endpoint index, logK, phase bits and p; actual real Hiary paid there.
* kerr-coherent-rejection.md: rational-characteristic Gaussian theta phase
  sampler with finite dyadic output, plus coherent amplitude evaluation.
  Its general phase-only Cauchy rejection obstruction does not apply here.

All files have prefix 2026-11-13 in this directory. The parent topic records
actual primary-source checks and the other native classical comparators.

## 1. Explicit branches and central input replacement

Put delta=epsilon/2^10, p=ceil(log2(1/delta)), T=100(p+10), and

    Y=ceil(2^100 (1+T)^12 delta^-4).

If K<=2Y, direct K+1 Fock evolution with certified finite arithmetic and
probability rounding is polynomial in the declared resources. Matrix entries
are finite binomial sums, whose bit lengths and cancellation precision are
polynomial in numerical K. Precision O(K+phasebits+log1/delta) suffices by
absolute term bounds. Construct probabilities and their normalized cumulative
law within delta TV. This branch is enormous but explicitly polynomial.
Assume K>2Y henceforth. Set m=n-K/2 on lattice Z+(K mod2)/2 and

    b_n=2^(-K/2)*sqrt(binom(K,n)),   u_m=(2/(pi K))^(1/4) exp(-m^2/K).

For |m|<=sqrt(KT), Stirling's explicit 1/(12j) remainder and the series of
log(1+-2m/K) give |log(b_n/u_m)|<=16(T^2+1)/K. For example the exact main
expression is -F(2m/K)/2+m^2/K-(1/4)log(1-4m^2/K^2), with
F(v)=K/2*((1+v)log(1+v)+(1-v)log(1-v)); its quartic remainder is
O(m^4/K^3). All factorial arguments here are integers >=K/4.
Hoeffding bounds the discarded b squared norm by 2 exp(-2T). Direct
Gaussian integral comparison bounds the discarded normalized Gaussian squared
norm by 8 exp(-T). Poisson summation gives the full Gaussian normalization
sqrt(pi K/2)*(1+O(exp(-pi^2 K/2))), also on the half-integer lattice.
Consequently the normalized central Gaussian differs from b, in l2 on the
physical interval, by <=2^10(T^2+1)/K+16 exp(-T/2)<delta.

The theta theorem has RATIONAL imaginary parameter. Choose rational v>0 with
|pi*v-1/K|<=delta/(2^30 K), and put gamma=pi*v. Normalizing exp(-gamma*m^2)
changes l2 by <delta/2^20: the derivative of the normalized vector has norm
sqrt(Var(m^2))<=8K throughout gamma in [1/(2K),2/K], by Gaussian integral
moment bounds. Computing pi to O(logK+log1/delta) bits pays this choice.
Let g be this normalized full-lattice Gaussian, h its normalized restriction
to |m|<=sqrt(KT), and attach the exact Kerr chirp to both. Their l2 distance
is <=16 exp(-T/4)<delta/2^20. Coherent phases preserve all these norms.
The normalized h has ||h||_1^2<=16 sqrt(K), and sum m^2 |h_m|^2<=4K;
the same moment bound holds for g. Both follow by comparing Gaussian sums
and their second moments with the integrals (K>2Y makes the unit-step errors
negligible). No pointwise relative approximation of tiny output probabilities
is used.

## 2. Coherent bulk approximation and normalized parity density

Write phi_r=2 atan sqrt(r/(K-r)), A_r=sqrt(2/pi)[r(K-r)]^-1/4,
and psi_h(phi)=sum_m h_m exp(i*m*phi), with h including its Kerr chirp.
The kernel theorem, h's l1 bound, and sum k^-3/2<=3/sqrt(Y-1) give
squared bulk amplitude error at most

    128 C^2 (1+T)^4/sqrt(Y-1) < delta^2, C=2^16.

Its approximating probabilities on Y<=r<=K-Y are

    q_r=A_r^2/4 * |psi_h(phi_r)+(-1)^r psi_h(-phi_r)|^2.

Indeed the amplitude is A_r exp(-pi*i*r/2) times the bracket/2. This keeps
both interfering saddles, even at zeros. The native two-gate row sign has
no count effect. Unitarity plus section1 and the bulk bound imply
sum_bulk |P_r-q_r|<10delta, by |||x|^2-|y|^2||_1<=||x-y||_2(||x||_2+||y||_2).

For s=0,1 define on phi in [0,pi]

    f_s(phi)=|psi_h(phi)+(-1)^s psi_h(-phi)|^2/(4pi).

Parseval and cancellation of the cross terms give sum_s int f_s=1 EXACTLY,
for integer and half-integer m. A sector may have zero mass; never normalize
it individually. The same identity holds with g in place of h. Moreover the
map h to the two coherent wavefunctions is an isometry, so replacing h by g
changes the joint phase/parity law by TV<=||h-g||_2. Rounding contracts TV.

## 3. Same-parity rounding and its summed error

Round r(phi)=K sin^2(phi/2) to the nearest count in {0,...,K} of parity s,
clipping the outer cells to the interval endpoints. For a bulk count r,
its cell is I_r=[phi_(r-1),phi_(r+1)]. Let R^h_r=int_(I_r) f_(r mod2).
Put J(r)=sqrt(r(K-r)); phi'(r)=1/J(r) and q_r=2 f_s(phi_r)/J(r).
The largest bulk cell width is <=4/sqrt(KY). Cauchy-Schwarz/Parseval gives

    sum_s ||f_s'||_1 <=4 sqrt(sum m^2 |h_m|^2)<=8 sqrt(K).

Thus summed integration-vs-center variation error is <=32/sqrt(Y).
On [r-1,r+1], |(log phi')'|<=1/(min(r,K-r)-1). For Y>=8 this implies
| |I_r|-2/J(r) | <=(4/Y)*(2/J(r)). If D=sum_bulk|R^h_r-q_r|,
then sum_bulk q_r<=1+D and hence

    D<=32/sqrt(Y)+(4/Y)*(1+D)<=72/sqrt(Y)<delta.

This is only an O(1/Y) relative geometry bound; no unproved stronger
O(1/Y^2) estimate is needed. With R the rounded FULL g joint law,
sections1-3 give sum_bulk |P_r-R_r|<12delta. Crucially this argument does
not assert q is normalized, discard endpoint mass, or condition on bulk mass.

## 4. Sampling the full joint law and finite-bit implementation

Write the unnormalized full psi as Theta(phi); its squared Fourier norm is
Z=sum exp(-2gamma*m^2)>=sqrt(K)/4. It is a theta function with rational
characteristic (K mod2)/2, tau=zeta+i*v, and
z=zeta*(K-1)/2+phi/(2pi); a global Kerr phase cancels from probabilities.
Use exact rational TURN coordinates x. One implementation samples
u from |theta_[a,0](u|tau)|^2 on the unit circle, subtracts z0=zeta*(K-1)/2
modulo one, chooses a signed representative in [-1/2,1/2], and folds to
x in [0,1/2]. The two coherent arguments are z_plus/minus=z0+-x. If an
argument is reduced as z=z_bar+ell, retain its SEPARATE multiplier
exp(2pi*i*a*ell), a=(K mod2)/2. For oddK this is (-1)^ell; omitting it can
swap the parity sectors with TV1 (oddK,zeta0). This is in addition to all
modular-transform phases. Radian phi=2pi*x is used only in bounded-precision
trigonometry; every theta input remains rational.
The retained theta compiler samples the circle law |Theta|^2/(2pi Z) in
polynomial native bits and log1/accuracy, with a requested dyadic phase grid.
Fold the circle to [0,pi], choose fair s, and accept with probability

    |Theta(phi)+(-1)^s Theta(-phi)|^2
      /[2(|Theta(phi)|^2+|Theta(-phi)|^2)].

The proposal density is (|Theta(phi)|^2+|Theta(-phi)|^2)/(4pi Z).
The accepted unnormalized density is exactly f_s/2, so TOTAL acceptance is
1/2. This cancellation is global across the sectors, including zero sectors.
For target error eta, cap this rejection at Jtheta=ceil(log2(16/eta))
iterations; ideal failure is <=eta/16. Put sigma=eta/[2^16(Jtheta+1)]
and pay all approximation errors per trial at this smaller scale.

There are no infinite exact comparisons. Here eta is a requested per-call
TV error, eventually delta divided by the total outer clock. Gaussian
integral bounds give sup|Theta|<=4sqrt(K), normalized phase density<=64sqrt(K).
Set a0=sigma*isqrt(K)/2^20, an exact rational threshold. Compute
S_tilde for S=|Theta(phi)|^2+|Theta(-phi)|^2 within a0/4; reject when
S_tilde<=3a0/2. A rejected quantized point has S<=2a0. Else S>=a0.
Evaluate both COMPLEX amplitudes to absolute
sigma^3/[2^50(K+1)^2], compute the ratio with interval guard bits and clip
to [0,1]. The cost is polynomial(logK,phasebits,log1/eta). The phase grid
below changes S by <a0/4. Thus all added threshold losses lie in the exact
proposal set S<=3a0, whose mass is <=3a0/(2Z)<sigma/2^17. Off this set,
the whole grid-displacement segment has S>=a0 and the ratio is stable.
No magnitude-only modular transform is used: its coherent unit phases must
be retained, as in the attached theta proof. Dyadic bit coins are capped.

For rounding, there are at most K+1 cell boundaries, with density<=64sqrt(K).
Also sup|Theta'|<=16K, hence |S'|<=2^10 K^(3/2). Away from the
deleted set, the acceptance ratio derivative is <=2^40 K/sigma, by the
quotient rule and |numerator|<=2S. If rounding crosses the threshold, both
points have S at most twice the threshold once the following grid is used;
that event remains covered by the deleted-set bound with a factor two.
Take grid resolution

    Rbits=ceil(6log2(K+1)+4log2(1/sigma)+100).

This pays acceptance-ratio continuity by <sigma/2^20 and total count
boundary-band mass <sigma/2^20. Evaluate sin^2 and the boundary
comparison with O(Rbits+logK) guard bits. All ambiguous bins are assigned a
fixed fallback and charged to those bands. The theta sample's own TV error and dyadic coin error are each <=sigma.
Coupling across all Jtheta trials pays <eta/16 total implementation error;
with the ideal failure <=eta/16, the returned count law is within eta TV
of R. No discrete law is compared in TV to a continuous phase law: the
comparison uses the common quantized-phase coupling and the paid boundary
bands. Every phase is reduced modulo one with
polynomial-bit rational arithmetic, RETAINING the characteristic-shift factors; no denominator-sized expansion occurs.

## 5. Exact endpoint replacement without a small-mass conditioning gate

Let E={r:min(r,K-r)<Y}, M=|E|<=2Y. The endpoint compiler gives each complex
amplitude with absolute accuracy delta/[100(M+1)], hence clipped squared
probabilities p_r in [0,1] with sum_E|p_r-P_r|<=delta/10. Precompute them
in polynomial(Y,logK,phasebits,log1/delta) time.

Use the following proposal once per trial. With probability M/(M+1), choose
uniform r in E and accept with probability p_r. Otherwise generate from the
full R sampler and accept only a bulk count. With ideal R the accepted
unnormalized law, multiplied by M+1, is

    T_r=p_r on E,   T_r=R_r on the bulk.

We have ||T-P||_1<13delta, S=sum T in [1-13delta,1+13delta], and
TV(T/S,P)<=13delta. Thus acceptance >=1/[2(M+1)]. Cap outer trials at
L=ceil(4(M+1)log(1/delta)); failure <=delta. Approximate uniform index,
mixture coins and endpoint coins to TV<=delta/(100L); call the rounded R
sampler to eta=delta/(100L). Coupling pays all implementation errors by
<delta/10 over the capped sequence. Fallback on exhausted clocks adds delta.
Total TV is <16delta<epsilon, with no lower bound on either bulk mass or
individual endpoint probability needed. All loops/call counts/operand lengths
are polynomial in logK, phase bits and 1/epsilon. Constants are huge; no
practical resource claim follows.

## Falsifiers and remaining claim gates

This composition fails if any dependency lacks its stated absolute BIT
interface, if the central all-parity coherent kernel bound fails, or if the
joint theta compiler drops modular phases or silently conditions on a sector.
Endpoint revivals and tiny probabilities have explicit handling above.
A finite successful simulation cannot prove the result. The full225LF independent composition review was parent-read, including its
TV1 omitted-sign falsifier, exact rational threshold, and all error clocks.
Its explicit repairs are incorporated above. For every clock, replace logs
by integer upper bounds obtained by rational power-of-two comparisons;
for example L=4(M+1)ceil(log2(1/delta)) suffices. The repaired composition
is established at this WRITTEN balanced scope; general-angle CDF/sampling
remains open. See 2026-11-13-balanced-kerr-composition-review.md.
No quantum advantage, novelty, implementation, or practical runtime is claimed.
