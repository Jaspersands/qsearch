Resumed 2026-11-12. The preceding derivation is PROVISIONAL and has no completed internal review. Start from its exact equations, not approval labels. No tools or external sources are available to you.

# Scalar OPI tilted-walk admission and positive-filter sampling

2026-11-07. PROVISIONAL hard derivation; independent review pending.
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
updates have no free inverse debt: sample zero separately; a nonzero change
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

## 2. The gamma promise is paid on the ORIGINAL table ensemble

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

