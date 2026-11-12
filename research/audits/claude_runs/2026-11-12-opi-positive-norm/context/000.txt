New independent obligation, 12November2026. Native model: explicit scalar RS OPI full halfset tables; P_s=(1-s)I+sP0 reversible with exactly samplable stationary distribution and updates. Quantum input is coherent stationary state or paid conditioned-flat |T>. Previously proposed generic killed-walk bound is included for notation, but the NEW target is sections4 and5. Claims there are provisional.

## 3. Constructive classical sampler for a positive filter

General statement, independent of RS: let P be a finite reversible chain
with classically samplable stationary pi and updates, and let G be a paid
rational function into[g0,1], g0>0. Let
 C=sum_(j=0)^M w_j[(D(P)+bG)/nu]^j,
with nonnegative rational weights, nonzero total, b>=0, nu>0. All parameters
and M have polynomial charged description/execution size. Let
 R=(P+bG)/(1+b), a substochastic kernel. It is implemented by one choice:
with probability1/(1+b), make a P step; otherwise stay and survive with
probabilityG(current state), and kill if that Bernoulli fails.

Define d_j=w_j[(1+b)/nu]^j, A=sum_jd_j. A single survival trial atx samples
j with probability d_j/A and takes j steps ofR. Its survival probability is
 p(x)=A^-1 sum_j w_j nu^-j (P+bG)^j1(x).
Detailed balance gives
 C|sqrt(pi)> = A sum_x sqrt(pi(x))p(x)|x>.
Therefore samplex~pi, run TWO independent survival trials FROM THE SAME x,
and retain x iff both survive. Conditioned on acceptance this is EXACTLY
the computational-basis law of normalized C|sqrt(pi)>.

Every R step has survival at least
 t0=(1+b g0)/(1+b), so t0^M<=p(x)<=1. Acceptance>=t0^(2M), and
 expected work O(M t0^(-2M))<=O(M exp[2(1-g0)bM]).           (COST)
The output law q has q(x)/pi(x) between t0^(2M) and t0^(-2M), and
 TV(q,pi)<=exp[2(1-g0)bM]-1.                              (LAW)
There is no oracle for p(x), no path enumeration, and no conditional future
samples. Each pair is generated independently. Rational d_j weights have
polynomial bitlength O(M times parameter bitlength), even if A is large;
integer-weight sampling and every Bernoulli can be capped, charging their
failure in epsilon. Cap outer trials at t0^(-2M)log(1/epsilon), with harmless
constant factors and integer ceilings; a union bound pays finite random
bit generation. Log(1/epsilon) clocks require bounded/geometric-tail input
samplers, which the native uniform/field/subset samplers provide. For generic
expected-cost-only input samplers, use one global Markov cutoff with
poly(1/epsilon) cost; restarting a timeout biases the law. The exact algebraic
law is separate from bounded-runtime
approximate sampling. No quantum state or phase information is reconstructed.

For g0=1/2 and the native source prescription (PRODUCT), this gives a
classical polynomial sampler and q/ pi=1+O(Lambda^-2) uniformly; TV has the
same upper bound. For any fixed marked set S, q(S)<=exp(bM)pi(S).
If C is implemented as a contraction, its HERALDED marked amplitude is
at most sqrt(q(S)), so this filter cannot create a superpolynomial gain
over the stationary starting overlap. This is an upper bound for this
specific use of this filter, not a lower bound on all search algorithms.

## 4. Resumption 2026-11-12: conditioned targets and a stronger norm bound

NEW PROVISIONAL derivation, not covered by the earlier paid sampler review.
Let P_s=(1-s)I+sP0 be reversible, G in[0,gbar], and suppose the known
rationalgbar is ACTUALLY ATTAINED. Charge its computation/score normalization;
an upper bound without controlled slack is not equivalent. Let b>=0,
nu>=E=lambda_max(D(P_s)+bG), and w_j=1/(M+1). The source's ideal score
has gbar=1; its implemented normalizer is a paid upper bound on E.

The stationary Rayleigh quotient gives E>=1+b E_pi G>=1. At a maximizing
basis state, the diagonal gives E>=1-s+b gbar (self-loop ofP0 only improves
this). Consequently
 1+b gbar<=E+s, (1+b gbar)/nu<=1+s/E<=1+s.
Writing A=sum_j w_j[(1+b gbar)/nu]^j, we have A<=exp(sM).        (DIAGONAL)
This is valid for arbitrarily large b. No LSI or spectral-gap lower bound
is used. In the source degree prescription REG gives
 sM<=log(1/(1-eta))/(r gamma)+s=O(1)
at fixed rate/spread/eta, independently of b. Thus raising b alone cannot
remove this bound while retaining that degree prescription.

Use killed walks R=(P_s+bG)/(1+b gbar): choose a P_s step with probability
1/(1+b gbar), otherwise stay and survive with probabilityG/gbar. The two
independent degrees use weights d_j=w_j[(1+b gbar)/nu]^j. Even when the
smallest G is zero, the j=0 term guarantees
 p(x)>=1/[(M+1)A]>=exp(-sM)/(M+1).
Thus the SAME paired sampler from pi has acceptance at least
 exp(-2sM)/(M+1)^2, cost polynomial in M and parameter bits if sM=O(loginput).
This replaces the earlier exp(bM) cost for the known-attained-maximum case.
The state measurement law is exactly sampled, not its phases or a unitary.

For a nonempty T, |T>=sum_(x inT)sqrt(pi(x)/pi(T))|x>. A row sum bound gives
 0<=sum_j w_j nu^-j(P_s+bG)^j1_T(x)<=A<=exp(sM).
For ANY marked S subsetT, the actual heralded marked amplitude obeys
 ||Pi_S C|T>||<=exp(sM)*sqrt(pi(S)/pi(T)).                   (CONDITIONED)
This bounds an actual amplitude, not just the source theorem's certificate.
Theorem4.6 has S subset T_eta subsetT, so it applies to that target geometry.
No extra superpolynomial gain over the overlap of the SAME paid initialstate
is possible at bounded sM. The cost to prepare/sample T is still charged.

A classical sampler from pi_T also samples the normalized PROJECTED law of
Pi_T C|T>: run the two killed walks with an additional test that each final
state lies inT. Their j=0 terms ensure the same acceptance lower bound.
Membership in T and a classical sampler for pi_T must be paid. This does NOT
sample the complete C|T> output outsideT, and does not give free conditioning.
Arbitrary nonnegative initial amplitudes, sM growing faster than loginput,
unknown/unattained maxima or normalizers belowE are outside these statements.

## 5. Exact spectrum of the native anchor mixer

NEW PROVISIONAL independent baseline derivation. Let v(a)=(1,a,...,a^(k-1)).
Additive Fourier characters are indexed by nonzero t inF_q^k. Averaging z
in the P0 update shows
 lambda_t=Pr_A[t dot coeff(D_A)=0]=Pr_A[t in span{v(a):a inA}].
All eigenvalues are nonnegative. For a uniform j-subset B write p_j for
Pr[t in span(v(B))]. If t is not yet in that span and j<=k-2, at mostONE
new evaluation point can make it enter: two such points would violate the
linear independence of the j+2<=k distinct Vandermonde rows. Therefore
 p_(j+1)<=p_j+(1-p_j)/(m-j), p_0=0, and inductively p_j<=j/m.
Thus lambda_t<=(k-1)/m=alpha. Equality is attained when t=v(a_i), because
membership occurs iff i is inA (any k distinct rows are independent).
The exact spectral gap ofP0 is r=(m-k+1)/m; forP_s it is sr. No finite
spectrum extrapolation is involved. This does not itself prove optimization
mixing or high-score hitting, and is not a free log-Sobolev constant.

