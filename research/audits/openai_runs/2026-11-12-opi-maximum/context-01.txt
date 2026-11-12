New provisional native mathematical claim; no earlier reviewer conclusions are included. Basic model q=2^t,m=q-1,k=floor(Rm),0<R<1 fixed, independent uniform q/2-element tables on every row, distinct known evaluation points, degree<k polynomials. No planted or supplied perfect solution.

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

## 6. Native maximum attainment from an exact second moment

NEW PROVISIONAL proof, 12November2026. It removes the maximum-advice issue
for the original IID balanced-halfset ensemble asymptotically; no perfect
polynomial is supplied or constructed. Let Z count codewords hitting ALL m
halfsets, q>=4 and1<=k<=m. Then EZ=q^k/2^m. Put a=(q-2)/(q-1).
For two distinct field values in one row, the joint acceptance probability
is (q-2)/(4(q-1)); for equal values it is1/2. Thus, averaging the difference
polynomial h uniformly among the q^k codewords,
 EZ^2/(EZ)^2=E_h product_i[a+(2-a)1_(h(a_i)=0)]
   =sum_(j=0)^m binom(m,j)a^(m-j)(2-a)^j q^(-min(j,k)).
The second identity is exact: any j specified Vandermonde evaluations
vanish with probabilityq^(-min(j,k)). Replacing every min(j,k) byj makes
the sum [a+(2-a)/q]^m=1. Therefore
 VarZ/(EZ)^2
   =sum_(j=k+1)^m binom(m,j)a^(m-j)(2-a)^j(q^-k-q^-j)
   <=2^m/q^k,
and Chebyshev gives Pr(Z=0)<=min(1,2^m/q^k).                  (MAXIMUM)
At fixedR>0,k=floor(Rm),m=q-1,q=2^t growing, this tends tozero as
exp[-Omega(m logq)]. On this single global table event, Hmax=m and the
explicit score G=1/2+H/(2m) has ATTAINED maximum1, mean3/4 and spread1/4.
No unknown optimum normalization or target oracle is required. Finding a
perfect codeword remains unresolved; existence is not an efficient search.

This pays the attained-maximum hypothesis in section4 with native data.
On the event, for ANY b>=0 and paid nu>=E, every positive average with
sM=O(log nativebits) has the classical stationary-output sampler above.
In particular the source-prescribed degree gives sM=O(1), independently
of b, and bounds actual marked amplitude for S subsetT by only a constant
multiple of its original overlap. This does not cover arbitrary longer
powers, different score/mixer families or non-flat initial amplitudes.
The fixed q8 fixture is NOT evidence for (MAXIMUM); its bound2^m/q^k=2
is vacuous, and it was not retuned to force maximum attainment.

If only a known uppergbar with gapDelta=gbar-Gmax is available, the exact
same diagonal argument gives A<=exp[M(s+bDelta)]. Require this TOTAL
exponent to be paid. A loose unattained upper bound is not a substitute.
The paper's actual correct near-optimum interval has Delta<=xi/2 from
Eq356 and xi=1/[n^2(Mmax+1)^2], with b<=1; its added exponent is negligible.
This source observation applies only to the correct interval, not clipped
later trials. No extension to all interval routines is inferred.

