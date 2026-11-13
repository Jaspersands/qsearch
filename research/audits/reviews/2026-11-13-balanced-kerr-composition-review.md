# Balanced Kerr sampler: independent full composition audit

13 November 2026. Read STATE/TRAPS, the complete stable 204-line parent sampler,
the balanced-kernel proof, the complete 200-line endpoint proof, and the retained
theta interface. No network, API, Git, tests, archives, or shared-status edits.
No paid report or approval label is used as mathematical evidence.

**Disposition.** With the explicit characteristic-shift correction in section 4,
the written construction supplies the claimed classical sampler for EVERY
binary K, rational Kerr phase, and requested TV error in its balanced native
contract. The finite precision and normalization obligations close. The proof
uses the already charged real-Hiary BIT interface in the endpoint compiler;
it does not establish that imported theorem anew. Constants are enormous.

The contract is exactly |K,0>, B(pi/4), exp(2*pi*i*zeta*binom(N,2)), B(pi/4),
then one count. Runtime is polynomial in log(K+1), the rational phase/input
bits, and 1/epsilon. No general-angle, arbitrary-input, multiple-pulse,
practical implementation, priority, hardness, or quantum-advantage claim follows.

## 1. Input replacement and kernel composition

The coefficient matrix V and the literal B differ by (-1)^(r+n). For this
specific initial state, two balanced rotations contribute only (-1)^(K+r)
to an output amplitude. Hence the parent's use of positive binomial input
amplitudes and V is exact for count probabilities, for every K parity.

The small-K branch K<=2Y is legal: numerical K is then polynomial in the
charged 1/epsilon. Binomial/coefficient integers have O(K) bits; normalized
matrix entries can be computed without a cyclotomic-field expansion. Exact
phase reduction and enough absolute guard bits pay all O(poly(K)) operations.
Probability rounding and renormalization are well conditioned around total
mass one. K=0 is the separate deterministic vacuum case.

For K>2Y, the Stirling comparison is correct. If u=2m/K, its exact nonconstant
logarithmic part is

    -K/4*((1+u)log(1+u)+(1-u)log(1-u))
       +m^2/K-(1/4)log(1-u^2),

with the stated O(1/K) factorial remainder. Its magnitude on the central
window is <=16(T^2+1)/K. The binomial and Gaussian tails and the normalization
error are smaller than the stated allocations because K>2Y and T=100(p+10).
The rational choice of v, gamma=pi*v, changes the normalized vector by at
most 8K*|gamma-1/K|, using the variance derivative of a normalized Gaussian.
Thus no call to the rational theta primitive at an irrational tau is hidden.

The coarse moment bounds can be proved without an asymptotic oracle. For
gamma in [1/(2K),2/K] and K>=64, shifted Gaussian sums give

    sum exp(-gamma*m^2)<=3sqrt(K),
    Z=sum exp(-2gamma*m^2)>=3sqrt(K)/4.

Here integral upper/lower sums differ by at most the supremum of the Gaussian.
Its second/fourth-moment sums differ from their integrals by at most twice
the corresponding supremum. These give E_g m^2<=2K and
sqrt(Var_g(m^2))<=8K. The central restriction has squared norm >=3/4, whence
||h||_1^2<=16sqrt(K) and E_h m^2<=4K, as used by the parent.

The infinite-lattice g is NEVER passed to the finite Krawtchouk matrix.
Only its central restriction h, supported in 0<=n<=K, enters that step.
The later h-to-g replacement is through an infinite-lattice Fourier isometry.
This distinction prevents an uncharged nonphysical tail operation.

The kernel theorem applies to this window for every bulk r and every chirp.
Its squared error with ||h||_1^2<=16sqrt(K) is bounded by the parent's
128*C^2*(1+T)^4/sqrt(Y-1). With C=2^16 and
Y=ceil(2^100*(1+T)^12*delta^-4), it is strictly below delta^2.
Input replacement plus this coherent amplitude error imply the claimed
sum_bulk |P_r-q_r|<10delta. No tiny-output relative error is used.

## 2. Joint parity is normalized, including odd K and zero sectors

For m in Z+(K mod 2)/2, define psi(phi)=sum_m h_m exp(i*m*phi) and

    v_s(phi)=(psi(phi)+(-1)^s psi(-phi))/(2sqrt(pi)),
    f_s=|v_s|^2,  0<=phi<=pi,  s=0,1.

The two cross terms cancel on summing s, and differences of two permitted
m values are integers. Consequently

    sum_s int_0^pi |v_s|^2=||h||_2^2,
    sum_s int_0^pi |v_s'|^2=sum_m m^2|h_m|^2.                    (1)

Both statements hold on the half-integer lattice. The map is a complex-linear
isometry, not an incoherent approximation. Replacing h by normalized g changes
the joint phase/parity Born law in TV by at most ||h-g||_2. One parity sector
may have exactly zero mass; neither sector is normalized separately.

The leading coherent kernel yields exactly

    q_r=A_r^2/4*|psi(phi_r)+(-1)^r psi(-phi_r)|^2
       =2*f_(r mod2)(phi_r)/sqrt(r(K-r)).

Thus the parity-sensitive cross term is retained before probabilities are
formed. The earlier generic phase-only Cauchy rejection lower bound does not
apply to this output-dependent formula.

## 3. Bulk quadrature is a summed bound, not pointwise smoothing

Rounding K*sin^2(phi/2) to the nearest legal count of parity s gives, for a
bulk r, the exact cell [phi_(r-1),phi_(r+1)]. Endpoint clipping is harmless
because these bulk cells do not meet the outer truncations. Their widths are
<=4/sqrt(KY). Equation (1) and Cauchy give

    sum_s ||f_s'||_1<=2sqrt(sum m^2|h_m|^2)<=4sqrt(K),

which is stronger than the parent's safe 8sqrt(K) bound. Hence the summed
center-value variation error is at most the stated 32/sqrt(Y).
On each cell, the logarithmic derivative of phi'(r)=1/sqrt(r(K-r)) has
magnitude <=1/(Y-1). Therefore the relative cell-width error is <=4/Y.
If D=sum_bulk |R^h_r-q_r|, then sum_bulk q_r<=1+D, so

    D<=32/sqrt(Y)+(4/Y)*(1+D)<=72/sqrt(Y),  Y>=8.

This bootstrap is valid without assuming q is normalized. Together with the
isometric h-to-g replacement, sum_bulk |P_r-R_r|<12delta follows. Nothing here
assumes the bulk has positive or appreciable total mass; endpoint revivals
are covered by the later replacement, not discarded by a tail assertion.

## 4. Material coherent correction: retain characteristic shifts

Work in exact rational TURN coordinates x, not irrational radian inputs to
the theta compiler. Set a=(K mod 2)/2, z0=zeta*(K-1)/2, tau=zeta+i*v. Up to
one common, irrelevant Kerr phase,

    Theta(phi)=theta_[a,0](z0+phi/(2*pi) | tau).

Sample the theta circle, subtract z0 modulo one, take its signed representative
in [-1/2,1/2], and fold to x in [0,1/2]. Both coherent evaluations have rational
arguments z_plus=z0+x and z_minus=z0-x. If the evaluator reduces these to
z_bar_plus/minus in [0,1), with integers ell_plus/minus, it MUST return

    Theta(+-2*pi*x)=exp(2*pi*i*a*ell_plus/minus)
                         *theta_[a,0](z_bar_plus/minus | tau).   (2)

Track the two factors separately, in addition to all modular-transformation
phases. For odd K they are separate signs (-1)^ell. They are not a common
global phase that can be dropped. Floor/reduction of these rational arguments
is exact polynomial-bit arithmetic, regardless of near-integer arguments.

This is a real falsifier of an omitted sign: for odd K and zeta=0, psi is even
and the true joint law has only sector s=0. For 0<x<1/2, reducing -x to 1-x
and dropping the half-characteristic sign makes the two evaluations opposite,
so it returns only sector s=1. The subroutine laws then have TV distance one.
The corrected rule (2) removes this failure. It is mandatory in the repaired
algorithm, not an optional convention.

## 5. Finite-grid and rejection clock, with an explicit threshold rule

After folding and a fair sector bit, the exact proposal density per sector is
S/(4*pi*Z), S=|Theta(phi)|^2+|Theta(-phi)|^2. Acceptance N/(2S), where
N=|Theta(phi)+(-1)^s Theta(-phi)|^2, gives f_s/2. Total success is exactly
1/2 even if one sector vanishes. No unknown Z is computed or divided out.

The parent's constants have ample slack, with one useful clarification:
the sharper integral bound sup|Theta|<=4sqrt(K), rather than 8sqrt(K), makes
the stated density cap 64sqrt(K) valid also for the folded/joint laws.
Indeed Z>=sqrt(K)/4, and sum_s f_s=S/(2*pi*Z)<=64sqrt(K).
Also sup|Theta'|<=16K and |S'|<=2^10*K^(3/2) are safe elementary bounds.

For a completely rational threshold choose

    a0=sigma*isqrt(K)/2^20,

which differs by at most a factor two from the displayed parent threshold.
Compute S_tilde with absolute error <=a0/4; reject if S_tilde<=3a0/2.
Any such rejection at the quantized point has true S<=2a0. Outside that
band, S>=a0 and the ratio can be evaluated with the parent's absolute
amplitude precision sigma^3/[2^50*(K+1)^2]. The quotient error is much less
than sigma/2^20. Clip the final dyadic probability to [0,1].

Couple the theta sampler's grid cell with an exact proposal phase, using
its TV error <=sigma. The angular displacement is <=2*pi*2^(-Rbits), with
Rbits=ceil(6log2(K+1)+4log2(1/sigma)+100). The |S'| bound makes its S change
<a0/4. All additional threshold losses are therefore contained in the
EXACT-proposal set S<=3a0, of mass <=3a0/(2Z)<sigma/2^17.
Outside this set the whole intervening segment has S>=a0; quotient
differentiation gives |(N/(2S))'|<=2^40*K/sigma. Hence the grid changes the
acceptance probability by <sigma/2^20. No continuity claim is made at an
uncut zero denominator.

There are O(K) rounding boundaries. Their total angular bands have proposal
mass at most a fixed constant times K^(3/2)*2^(-Rbits), again <sigma/2^20.
For numerical sin^2 evaluation use the rational turn x and computed pi;
O(Rbits+log K) guard bits suffice. At an interior integer count boundary,
dr/dphi=sqrt(r(K-r))>=sqrt(K-1), so numerical ambiguity is contained in those
same angular bands. Outer cells are clipped deterministically. There is no
comparison of a finite atomic law directly in TV to a continuous density.

With Jtheta=ceil(log2(16/eta)) and sigma=eta/[2^16*(Jtheta+1)], couple all
theta-grid errors, threshold losses, ratio errors and dyadic coins across the
capped trials. Their sum is <eta/16; ideal timeout is <=eta/16. The common
fallback produces a law within eta of R. Requested theta/amplitude precisions
are polynomial in log K, phase bits and log(1/eta). Binary integer shifts,
characteristic signs, Gaussian/modular phases, and bit coins all have bounded
finite clocks. The previous closed theta interface supplies these calls.

## 6. Endpoints, normalization, and full resource conclusion

The endpoint proof actually pays the required growing-Y interface. Its
Krawtchouk polynomial has degree r<=Y; exact central interpolation has degree
O(p+(r+1)log K) and polynomial coefficient bits. It calls real weighted Hiary
sums with normalized monomials, not an assumed complex-Gaussian oracle.
Its direct branch is entered only when numerical K is bounded by a displayed
polynomial in these charged parameters. Upper endpoints are a known sign plus
a rational linear-phase shift. Thus all 2Y endpoint amplitudes can be computed
at the stated absolute accuracy with polynomial native cost, without a norm
or probability oracle. Squaring and clipping gives the claimed L1 error.

The outer replacement has accepted unnormalized mass T/(M+1), where T is
the computed native endpoint law on E and the full rounded R on the bulk.
The established bound ||T-P||_1<13delta implies sum T>=1-13delta and
TV(T/sum T,P)<=13delta. Therefore success is >=1/[2(M+1)] even if either
endpoint mass OR bulk mass is zero. The cap L=O((M+1)log(1/delta)) pays timeout;
each of the finitely many coin/index/R calls has error <=delta/(100L).
Use integer upper bounds on logarithms when forming a clock; no exact
comparison with an irrational log is required. All implementation and timeout
errors fit the remaining allocation, yielding TV<16delta<epsilon.

Y is polynomial in 1/epsilon, while every theta precision and phase reduction
uses polynomially many bits in log K, input bits and log(1/epsilon). Endpoint
precomputation, outer/inner clocks and the small-K branch are consequently
polynomial in the advertised joint resources. Neither numerical Kerr period
nor numerical K is expanded in the large-K branch. After enforcing (2), no
remaining all-input composition gate was found at this written balanced scope.
