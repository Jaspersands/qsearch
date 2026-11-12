# Scalar OPI tilted-walk admission and positive-filter sampling

2026-11-07, CLOSED written admission test 2026-11-12. Independent
core/norm/spectrum/maximum reviews checked; two frozen exact controls.
This tests a specific complete candidate, not all tilted walks or all OPI
algorithms. No quantum implementation, novelty or separation is asserted.

## Selection and candidate

Start current STATE/TRAPS; preceding Gaudin counterfamily pass made progress.
Independent comparison found no fresh paid receiver for growing-degree
character reconstruction, no normalization for native narrow lattice-Gaussian
preparation, and no new hidden-Clifford cubic derivative processor. The
existing cyclotomic specialization screen was reused, not restarted.
Corpus been-tried and baselines preceded actual primary reading of Ozgul--
Chakrabarti2609.40088v1, retained under audits/sources/opi_tilted_walk/.
Its Theorem4.6 offers a concrete new filter and resource prescription.

Question: can that tilted-walk prescription turn the natural Reed--Solomon
resampling walk into a polynomial-time high-score scalar OPI algorithm,
starting from the easily prepared uniform codeword state? This would be a
new constructive route to the externally motivated full-table search task,
where the known Johnson-list DQI sampler is the strongest quantum comparator.
The cheapest attacks are exact score drift, the source's normalization, and
a matched classical simulation of the actual filtered output distribution.

Native input is unchanged from SCALAR_OPI_NATIVE_PRIORITY.md: q=2^t,
m=q-1 distinct nonzero points a_i, k=floor(Rm), fixed0<R<1, independent
uniform q/2-element halfsets F_i supplied as complete tables. X is the
space of degree<k polynomials, size D=q^k. H(c)=sum_i1_F_i(c(a_i)).
Output an explicit c of a specified high score, checked on ALL original
rows. No planted solution, target state or hidden transition oracle.

Candidate mixer P0: choose A uniformly among(k-1)-subsets of the m rows
and z uniformly in F_q; replace c by c+z D_A, D_A(X)=prod_(i inA)(X-a_i).
Take P_s=(1-s)I+sP0 for rational0<s<=1. This is symmetric and uniform-
stationary; it is irreducible because the D_A include a Lagrange polynomial
basis for a fixed k-element information set, and has a self-loop z=0.
Classical updates and score evaluation cost polynomial native bits. Coherent
updates have no free inverse debt: combine the lazy and active-zero events
into ONE diagonal branch, of probability1-s(1-1/q); a nonzero change
has exactly A as its roots among the given points and z as its leading
coefficient, so scan the m points to erase its address. Uniform subset
preparation and field/table access must be charged. No new circuit is built.

Use an explicit affine rational score G=a+cH in[1/2,1], c>0, and the filter
 C=(1/(M+1))sum_(j=0)^M[(P_s+bG)/nu]^j,
where b>=0 and nu>0 are paid rational parameters. The source ideal uses
nu=lambda_max(P_s+bG); its implementation section7.3 pays a computable
replacement. The classical result below covers ANY supplied rationalnu.
Unknown Hmax is never a supplied free input: source max-normalization is an
analysis convention or must be handled by its paid parameter trials.
The simple native score G=1/2+H/(2m) already has the required range. Any
source-valid affine normalization with the same slope retains the score
spread used below. The argument applies to Theorem4.6's actual formula,
not an unproved extension of its premises when maxG<1.

Strong classical baselines are Prange completion, published systematic-basis
pivots/annealing, and the retained anchor-plane batching. They receive the
same full tables. The current proposed classical counterpart additionally
samples the normalized positive-filter output, with all rejection cost paid.
Desired quantum upside would be a superpolynomial increase in high-score
sampling probability at polynomial preparation/filter cost; it is not inferred
from the paper's comparison to particular MAX-k-CSP classical algorithms.

Proof obligations/falsifiers: correct scalar source and complete input access;
coherent mixer construction; affine drift/smoothness, admissible log-Sobolev
and variation constants; normalizationnu; total filter/herald/search cost;
a surviving comparison against Prange and the positive-filter sampler. A
constant or vanishing likelihood-ratio change kills THIS proposed admission.
Conditioned/nonstationary initial states require separate paid preparation
and are not covered by the stationary-start simulation theorem.

## 1. Exact native score drift and laziness

For each row i, Pr(i inA)=(k-1)/m. OutsideA, D_A(a_i) is nonzero and
zD_A(a_i) is uniform inF_q, so its halfset acceptance has mean1/2. Thus,
for EVERY halfset input and EVERY codeword c,
 P0 H = alpha H +(1-alpha)m/2, alpha=(k-1)/m.
Writing r=1-alpha=(m-k+1)/m and mu=E_uniform G=a+cm/2,
 P_s G=(1-sr)G+sr mu.                                      (DRIFT)

Suppose Gmax-mu>=gamma>0; no maximizing codeword is input to the algorithm.
For any source-admissible pseudo-Lipschitz constant L with P_sG>=(1-L)G,
and any variation upper bound V>=max_x sum_yP_s(x,y)(G(x)-G(y))^2,
 L>=s r gamma, V>=s r^2 gamma^2.                           (REG)
The first uses Gmax<=1 at a maximizer. The second uses Jensen CONDITIONAL
on the P0 step, whose mean loss there is r(Gmax-mu); the lazy self-loop
contributes zero. Jensen over the whole lazy step would lose a factor s.

Let Lambda=logD=k logq. The source Condition3.4 is
 <psi|P_s|psi><=1-omega Ent_uniform(|psi|^2/pi).
Testing a basis vector gives omega<=s(1-P0(x,x))/Lambda<=s/Lambda. (LSI)
This is an upper bound on ANY claimed valid omega, not a missing lower bound
or an assertion that the current chain's LSI has been fully computed.

The actual Theorem4.6 chooses A0=1-rho-L, with A0-mu>0, and
 b*=min(1,(sqrt(1+8omega^2 A0(A0-mu)/V)-1)/A0).
Using sqrt(1+x)-1<=x/2,
 b*<=4omega^2(A0-mu)/V<=4s/[Lambda^2(r gamma)^2].            (TILT)
Its degree is M=max_(x inS)ceil(log(G(x)/(1-eta))/L), hence
 M<=log(1/(1-eta))/(s r gamma)+1.
For fixed eta bounded away from1 and fixed r,gamma>0,
 b*M <=4[log(1/(1-eta))/(r gamma)^3+s/(r gamma)^2]/Lambda^2
       =O(Lambda^-2).                                      (PRODUCT)
This holds for arbitrary laziness s, whenever the source's other hypotheses
are satisfied and M is afforded. If those hypotheses fail, the source gives
no admission. Replacing b* by a smaller rational approximation preserves it;
arbitrary larger tilts or longer degrees are outside this prescription.

## 2. Paid score spread and the original table ensemble

A stronger deterministic certificate is available for EVERY halfset input.
Fix k-1 rows and accepted values and interpolate any c0 satisfying them.
Along c_z=c0+zD_A, all anchors remain accepted; each other row visits every
field value once. Thus the exact average over the q line members is
 (1/q)sum_z H(c_z)=(m+k-1)/2.
For the native slope, Gmax-mu>=(k-1)/(4m), a constant at fixed positive
rate and growing q. Enumerating this line is polynomial in the full-table
input length and yields a VERIFIED score certificate. This is the already
applicable anchor-line classical baseline, not a new optimization algorithm.

One classical Prange completion chooses an information set of k rows, draws
one accepted value from each and interpolates c. Conditional on these tables
and choices, the untouched m-k tables remain independent, so exactly
 H(c)=k+Binomial(m-k,1/2).
Consequently H(c)>=m/2+k/4 except with probability at most
 exp[-k^2/(8(m-k))]. For G=1/2+H/(2m), or max-shifted affine normalization
of the same slope, Gmax-mu>=k/(8m). At fixed positive rate this is a fixed
gamma with probability1-exp(-Omega(m)). H(c) is actually verified; no hidden
maximum or tail oracle is needed for this lower bound. This is a classical
source-specific theorem, not empirical failure evidence or hardness.
This binomial law is over the original random-table ensemble, not after
conditioning on the full input. Repeated completions on the SAME tables
do not automatically multiply its failure probability.

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

Independent norm/identity-term review checked on 12November2026.
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
Membership in T and a classical sampler for pi_T must be paid. This version
samples only the projection ontoT, and does not give free conditioning.
Starting instead from pi samples the full output by the same endpoint tests,
but its guaranteed acceptance loses a factor pi(T); no efficient general
full-output simulation follows from a rare conditioned start.
Arbitrary nonnegative initial amplitudes, sM growing faster than loginput,
unknown/unattained maxima or normalizers belowE are outside these statements.

## 5. Exact spectrum of the native anchor mixer

Independent Fourier/span-incidence review checked. Let v(a)=(1,a,...,a^(k-1)).
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

Independently checked proof, 12November2026. It removes the maximum-advice issue
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
On the event, for ANY b>=0 and paid nu>=E, the UNIFORM positive average with
polynomially paid M and sM=O(log nativebits) has the classical sampler above.
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

The efficiency claim is high probability over the table ensemble, not a
polynomial unconditional expected runtime on exceptional tables. Cap the
number of outer proposals at (M+1)^2 exp(2sM) log(1/delta), with integer
ceilings and rational upper bounds; include all inner bit-generation caps.
Then the failure/approximation allowance is at most 2^m/q^k+delta plus
the charged implementation error. The sampler's algebraic law remains
correct on exceptional tables, but its efficient acceptance bound may fail.

Attainment is NOT a deterministic input-format promise. For every k<m,
take a dependence sum_(i inJ)c_i v(a_i)=0 among k+1 rows; every c_i is
nonzero. For a nonzero F2-linear functional ell and bits beta_i summing to1,
choose F_i={y:ell(c_i y)=beta_i}. These are legal balanced halfsets and no
polynomial can hit all of them. This explicit exceptional family is consistent
with (MAXIMUM); it refutes any attempt to make that event a per-input certificate.

## 7. Source and independent-review dispositions

Actual primary PDF2609.40088v1, SHA6811ae8eaa9727db490653abc2f16c58eb8fa4dda9a8605d4349a163605c620b,
was read for discriminant definition, Condition3.4, Theorem4.6 and section7.3.
The source uses uniform weights including j=0, the displayed ceiling degree,
RMS variation L2 with V=L2^2, and S subset T_eta subset T. Its implementation
uses a certified positive omega in Eub=1+b*mu+b^2*V/(8omega^2), plus slack;
this is not a free native-chain LSI certificate. These facts were checked
against the actual full source, not the shortened review packets. Nothing
here disputes the paper's MAX-k-CSP or hypercube results.

Paid reports, each fully read and checked by the parent:
- claude_runs/2026-11-07-positive-filter-sampler: completed; exact paired law,
  independent degrees and finite-clock caveats accepted. Its stronger TV
  bound is valid; necessity language about bM is not used (constant G already
  defeats a universal necessity claim). This report reviewed section3 only.
- openai_runs/2026-11-12-opi-drift-core: completed; DRIFT/REG/LSI/PRODUCT and
  Prange proof checked. Deterministic anchor-line spread and pooling both
  diagonal coin events accepted. This packet preceded sections4-6.
- claude_runs/2026-11-12-opi-positive-norm: completed; DIAGONAL, identity-term
  cost, conditioned projection and spectral recurrence checked. Native z
  includes zero; source bridge independently verified above. Corrected its
  intermediate A<=rho^M when rho<1 to A<=max(1,rho)^M. Rejected its generic
  assertion of EXACT conditional output after state-dependent inner timeout:
  the bounded implementation has a charged error/abort allowance, not that
  stronger law. Its full-output variant pays an additional pi(T) loss.
- openai_runs/2026-11-12-opi-maximum: completed; exact balanced-table second
  moment, exceptional counterfamily and global-event quantifiers checked.
  Accepted polynomial-M and ensemble-runtime repairs. General convex weights
  retain the amplitude bound, but sampler efficiency needs w0>=1/poly.
- claude_runs/2026-11-12-opi-source: TRUNCATED, not a completed review.
  Useful missing-packet/normalizer warnings checked against full source.
  Rejected an alleged RMS-convention ambiguity and unsupported independent
  Prange-restart tail on reused tables. No retry; its ACCEPT-like prose is
  not evidence of closure.

All paths above are relative to audits/. No report was promoted by its label.
No maximizing witness, free nu, conditioned start, oracle, postselection,
unbounded degree, or common randomness between the two trials is admitted.

## 8. Frozen controls, decision and next experiment

audits/controls/opi_tilted_walk/control.py ran ONCE in Sage on fixed
q8,m7,k2,seed20261107,64 codewords. Exact stochasticity/symmetry/drift and
matrix-versus-independent-path laws agree. A deliberately SHARED degree
changes every output weight, TV about0.00019311. Filter TV from uniform is
about0.0100018; mean score about3.53156. Native one-restart Prange has exact
mean253/56 about4.51786; its saved witness has verified score5/7. The actual
repository prime-field Prange routine rejects q8, so the extension-field
comparator was evaluated explicitly. No source LSI certification from this
fixture. Two schemes being exactly compared does not establish an algorithm
or scaling from the fixture.

second_moment.py ran ONCE on all216 q4,m3,k2 halfset tables and all16
codewords: Z distribution0:12,2:192,4:12; EZ2/(EZ)^2=10/9,
Pr(Z=0)=1/18<=1/9<=1/2. This checks formula transcription only; the general
proof is section6. No retuning or q8 rerun. Parent read both scripts/results.

DECISION: reject this scalar-OPI stationary-start tilted-walk admission.
The prescribed bM produces only 1+O(log(D)^-2) likelihood change. The broader
uniform-average filter with polynomial M and bounded sM is classically
sampled even at arbitrary tilt, on a high-probability event of the original
ensemble; its actual flat-conditioned marked amplitude gains at most a
constant factor at the source degree. Generic OPI and the known Johnson-list
DQI comparator remain OPEN. No general longer-power, repeated-filter,
non-flat-start or source-paper no-go, hardness, novelty or separation.

Next scientific action: independent direction selection, not another tilt
sweep. Compare a native end-to-end application whose source/readout can be
paid against its strongest classical output-specific baseline. The fresh
periodic-conduction factorization is under primary-source comparison with
the already-accounted ternary subset-sum and classical-data sketch routes.
Acceptance of any next candidate requires its own explicit native input,
scalar/witness output, total resources and classical falsifier.
