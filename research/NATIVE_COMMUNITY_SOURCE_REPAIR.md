# Native community detection: source-law gate and constructive repair

2026-11-13. Source repair CLOSED WRITTEN at the fixed-q scope below.
Stronger classical comparison remains OPEN; no new quantum advantage accepted.
The preceding tower endpoint is CLOSED at its exact ERH/factoring scope.
Fresh STATE/TRAPS and corpus been-tried/baselines checks preceded primary
literature. The independent147LF comparison left one community readout lead,
but actual source inspection uncovered a prerequisite failure. Recovery and
any claimed Shor-level endpoint are deferred. No quantum implementation.

## Chosen scientific question and native contract

Can the Kikuchi guiding-state overlap be proved from ONE actual Bernoulli
hypergraph, with no independent-graph or planted-label advice? This directly
removes a specific unverified end-to-end source gate. If it cannot, retain
the scoped source finding and pivot; do not build a subsystem around it.

Native input: all p-edge indicators Y on n vertices, known rational q in
(0,1/2), epsilon in(0,q), fixed even p>=4 and fixed k>=3. Latent labels are
independent uniform in[k]; conditional on labels, edges are independent
Bern(q+epsilon*f_x(S)), with f=sum_c product_(i in S)(1[x_i=c]-1/k).
Null edges are iidBern(q). All inputread/O(n^p) storage and numerical bits
are charged. No latent labels, fresh-instance oracle or QRAM supplied free.
Target DETECTION, initially a concrete nonempty growing ell=lambda*p=o(sqrt n)
regime. Fixed q bounded away0 is a permissible first scope; sparse q needs
separate preparation/moment bounds. Desired quantum mechanism is actual
prepared guide plus sparse Kikuchi energy filtering and amplitude amplification.

Expected asymptotics, if repaired: retain the known dominant n^(ell/4) cost
with explicitly paid exp(O(ell logell)) and polynomial input costs against
the n^ell Kikuchi comparator. This is a quartic-scale repair, NOT a proposed
polynomial-versus-superpolynomial/Shor-level discovery. Its value is resolving
whether a published source guarantee can be safely used in further ideas.
Low-degree/LCDF bounds are not lower bounds on every classical algorithm.
Strong classical competitors: explicit/matrix-free Kikuchi, applicable
planted-XOR refinements, and classical distributional cloning. The corpus
catalog returned no direct baseline; the actual primary cloning theorem
was inspected instead. No absence-of-catalog-hit hardness inference.

## Exact source imports rejected

Parent fully checked208LF independent audit
`audits/reviews/2026-11-13-community-source-independence.md`, against actual
Schmidhuber--Zlokapa arXiv2510.08494v1, C.3.1/C.3.3, Definitions2/27/29,
Lemma58 and equations184--214. This is a SOURCE PROOF GAP, not a falsification
of the detection algorithm or its final scaling.

1. For A=(Y-q)/sqrt(q(1-q)) with conditional mean beta*f, M~Bern(zeta),
   Cov(MA,(1-M)A | labels)=-zeta(1-zeta)*beta²*f². The claimed conditional
   independence fails. Conditioning on the mask restores observational
   independence but changes the guiding mean to a masked certificate;
   matrix-dependent directions cannot then be averaged as if fixed.
2. Distinct hyperedges need not have independent label functions. For p4,
   take rowunique1234,5678 and columnunique1256,3478, plus a=lambda-2>=1
   common disjoint edges. Each row is internally vertex-disjoint. Set
   C_ab=delta_ab/k-1/k² and M=C^(Hadamard p/2). Then for every fixedk>=2,
   every evenp and lambda>=3,

      E_x W(a,2)=beta^4 Tr(M^4)*(1-(beta²*Tr(M²))^a)>0.

   This contradicts the zero term imported from Lemma58 in the native law.
   Literal unconditional-iid assumptions would instead make that lemma
   inapplicable. Atp4k3 TrM4=2/59049, TrM2=2/243; atp4k2 they are1/4096,1/64.
   The exact4096label Sympy control gives767/452984832 atq1/4,epsilon1/8.
   Analytic all-lambda proof, not the finite control, establishes the scope.
3. Replacing beta byzeta*beta in all moment entries is not literal:
   E[(MA)²]=zeta while unmasked dictionary entry is1.

Controls: `audits/controls/community_source/exact_falsifiers.py/.json`.
These only test exact algebra and do not establish a runtime or failure
of all possible algorithms. Published Theorem50's overlap is not admitted.
The classical certificate/ordered tensor interface is separately under review.

## Concrete replacement operations under proof attack

Approximate classical clone: choose a faircoin, place observedY in one
output and an independent freshBern(q) in the other, then forget the coin.
For delta=epsilon*f both marginals areBern(r),r=q+delta/2. The exact joint
chi-square distance to independentBern(r) copies is

    delta^4/[16*r²*(1-r)²] <= beta^4*f^4.

Independent processing of all edges gives conditional-and-mixed-label TV
at most .5sqrt(exp(binomial(n,p)*beta^4)-1), uniformly in labels.
At beta=C*n^(-p/4)*ell^(1/2-p/4)*sqrt(logn), this vanishes when
ell >> (logn)^(2/(p-2)). Stronger known signals can first be attenuated by
mixing observedY with freshBern(q). Two cloned DATASETS are formed once
and then reused coherently; no fresh IID graphs are promised per quantum
call. TV transfer is through the whole algorithm, not multiplied by its
number of oracle calls. Finite precision and exact admissible range remain
part of the paid compiler obligation.

The exact prior GRAPH-CLONE, Brennan2019 Lemma14, was read at its actual
statement/proof. It maps TWO inputbiases to independent products subject
to likelihood inequalities. It does not automatically handle the multilevel
community f. A singlebit channel gives joint probabilities affine in input
bias; two nonconstant affine marginals would have a quadratic product, so
exact agreement at >=3 biasvalues is unavailable for that simple interface.
No novelty claim for the approximate kernel.

PROVED conditional covariance operation: independent real A_e=m_e+xi_e,
E xi=0, Var xi<=v, andPi removes repeatedcoordinate/vertex tuples. For
U=Pi A^tensorlambda, V=Pi m^tensorlambda, exact bound

 ||Cov(U)|| <= sum_j binom(lambda,j)^2*j!*v^j*||m||^(2lambda-2j)
             <= ||m||^(2lambda)*(exp(lambda²*v/||m||²)-1).

Parent checked the full paid covariance report and its partial-matching
proof. There are binom(lambda,j)^2*j! matchings of j distinct row and column
positions. Each matching operator is a left/right tensor permutation of
D^tensorj tensor |m^tensor(lambda-j)><m^tensor(lambda-j)|, D=diag(Var A_e).
Its norm is at most v^j ||m||^(2lambda-2j). Edge-distinct support makes the
matching sum exactly the covariance; no same-side contraction survives.
Diagonal contractions supported on distinct edge indices also work. At m=0
use lambda!*v^lambda. Independence conditional on labels is required (at
least 2lambda-wise); unconditional label averaging is not used. Native v<=2
is sufficient; setting v=1 without checking is invalid.

For an independent high-energy projector P and an explicit isometry J from
the edge-tuple encoding, set s=J*PJV/||PJV||. Its norm is at most one and
<s,V>=||PJV||. Thus directional Chebyshev bounds the probability that
||PJU||<(1-eta)||PJV|| by ||Cov U||/(eta²||PJV||²). The compression J*PJ
need not itself be a projector. The actual certificate and J remain a
separate independent proof obligation.

The report's O6/F4 claim that detection necessarily needs a rank(P)-paid
trace bound and fourth moments is REJECTED for this algorithm. We need a
small normalized spectral mass, not constant angle or ||P(U-V)|| control.
Each tuple has distinct edges, so E||U||²<= (2M)^lambda, M=binom(n,p).
Markov gives ||U||²<=(2M)^lambda/rho with probability at least1-rho.
Combine this with the unnormalized directional lower bound: spectral mass
is at least c*rho*(beta_guide²*mu/constant)^lambda. Under the null, the
matrix bound makes P=0 with high probability regardless of the guide.
No quadratic-guide null statistic or fourth-moment bound is needed.
This is a parent derivation, not acceptance of the report's verdict label.

New cheapest baseline correction: a symmetric clone halves matrix beta,
which increases the required ell by 2^(4/(p-2)); at p=4 this can erase a
quartic exponent comparison on the SAME original input. Comparing both
algorithms at the same unoptimized ell would be misleading. A concrete
repair under independent audit is an ASYMMETRIC clone: observed Y goes to
the guide with probability t and to the matrix otherwise; the other output
is fresh Bern(q). Marginals are q+t*delta and q+(1-t)*delta. Its exact
chi-square error against their independent product is

 t²*(1-t)²*delta^4/[r_guide*(1-r_guide)*r_matrix*(1-r_matrix)].

Taking t=1/ceil(log2 n) keeps matrix beta within1-o(1) of the original,
while guide preparation/amplification pays the logarithmic attenuation.
This may preserve the dominant exponent comparison; no such comparison
is accepted before full composition and same-input parameter optimization.
Guide norms, classical certificate, finite-bit channel, all gate/error
costs and TV transfer must close before any endpoint is accepted.

Two distinct paid jobs, no retries:
`audits/api_inputs/2026-11-13-community-source-repair/dispatch.json`:
Claude/high covariance completed, fully parent-read and reaped: exact
matching and directional bounds accepted; unnecessary rank/fourth-moment
gate rejected as above. OpenAI/max native whole compiler is still running.
Contexts
are narrow contract and sanitized actual primary excerpts, no credentials.
They are advisory. Next action: classical certificate independent review,
then returned covariance/whole-compiler proofs; stop on a decisive failure
without a concrete repair. Every material report claim needs parent checking.

## Closed written native detection construction

Parent read all 613 lines of the completed OpenAI compiler, all 375 lines of
the independent certificate audit, and all 341 lines of the independent
cloning proof. Only the necessary checked proof chain below is admitted.
The source's disputed lemmas are not reinstated. The optional long
motif/variance expansion in the certificate note is unnecessary here.

**Scope.** Fixed even p>=4, k>=3, rational q bounded away from0 and1/2
(q=1/4 suffices), explicit one-bit-per-edge input, known rational epsilon.
Let ell=p*lambda grow, ell=o(sqrt n), at a known signal near

 beta_*=C_(p,k)*n^(-p/4)*ell^((2-p)/4)*sqrt(log n),

where C_(p,k) is a computable sufficient constant. Stronger known signals
may first be attenuated, with all original-input comparisons preserved.
Require epsilon_*<=q/2, automatic eventually here. A fully rational example
at p4: L=ceil(log2 n), J=ceil(sqrt L), ell=4*ceil(L²/4), epsilon_*=A/(nJ),
where a sufficiently large fixed computable INTEGER A pays the certificate
constant. The original epsilon may equal epsilon_*. All input bits are paid.

**One observed source.** Form asymmetric clones ONCE with t=1/L. The ideal
comparison pair is independent conditional on the SAME labels, with matrix
SNR b=(1-t)beta_* and guide SNR h=t*beta_*. Actual joint TV is at most
.5sqrt(exp(4M*t²*beta_*^4)-1), uniformly in labels, M=binom(n,p). At threshold
its exponent is O(ell^(2-p)); the p4 example has TV=O(L^-2). Four bounded
Bernoulli draws per edge, with ceil(log2(4M/eta_num)) random bits each,
add at most eta_num error. Original data, masks and attenuation randomness
are not passed to the quantum routine. Null clones are exactly independent
when q is generated exactly. TV transfers ONCE through the complete
trace-preserving algorithm, including timeout; no postselection conditioning.

**Certificate for every label vector.** Set w_c(i)=1[x_i=c]-1/k and
F=sum_c w_c^tensorp on full ordered registers, including repeated vertices
in this analysis tensor only. Then ||F||²>=k*(n/k²)^p and |F_entry|<=1.
On ell registers define the positive semidefinite operator

 B=sum_(|I|=p/2) sum_c tensor_I |w_c><w_c| tensor identity_elsewhere.

Its norm is O(n^(p/2)ell^(p/2)). The actual collision-free mean divided
by b is Pi_cf B Pi_cf-E, with ||E||=O(ell^(p/2)n^(p/2-1)): each omitted
transition reuses an old changed vertex. In phi=(F/||F||)^tensorlambda,
contraction of one position against w_c has squared norm >=n/k^(2p+2).
Keeping just terms changing one position in each of p/2 different blocks
gives energy >=c_(p,k)n^(p/2)ell^(p/2); the other B terms are positive.
Collision probability O(ell²/n) changes the normalized vector by
O(ell/sqrt n), preserving this bound for every label vector.

The exact isometry is J|E>=sum_permutations |ordered E>/sqrt(p!). With
V=Pi f^tensorlambda, JV=(p!)^(-lambda/2)Pi_cf F^tensorlambda. The compressed
transition multiplicity is product_i t_i!, absent in source equation54-to56;
the lift pays it automatically. No unknown label is supplied to the algorithm.

Correct Bernstein includes Bernoulli amplitude: for D=n^(p/2)ell^(p/2),
summand norm<=2*(p/2)!/b, variance<=4D. At
b>=B_(p,k)n^(-p/4)ell^((2-p)/4)sqrt(log n), null and planted centered noise
are <=c*b*D/4 with high probability. Thus tau=c*b*D/2 gives null norm
<=tau/2 and planted certificate pass mass ||PJV||²/||V||²>=c/8.
Source Lemma30 is FALSE at its wider printed scope: q=n^(1-p),epsilon=q/2,
ell~logn has an edge with high probability and norm>=Omega(n^((p-1)/2)),
above the printed bound. This counterfamily is BELOW the repaired threshold.

**Guide overlap and normalization.** In the ideal pair, m=h*f. Weighted
collision estimates compare ||Pi m^tensorlambda||² with ||m||^(2lambda).
The proved matching covariance bound, using s=J*PJV/||PJV||, gives the
unnormalized projection lower bound except with probability
O(lambda²/(h²M))=o(1). Only E||U||²<=(2M)^lambda is needed for normalization.
Markov with rho=1/L gives spectral mass >=c*rho*(c_(p,k)*h²)^lambda with
probability1-o(1). This parent argument replaces the compiler's optional
sparse-q concentration extension. At fixed q every observed |A_E|² lies
between fixed positive constants; collision-free guide preparation succeeds
with probability1-O(ell²/n) for EVERY graph, so its inverse is also paid.

**Gate and bit clock.** Compile the explicit M-amplitude guide table and
its inverse, at O(M*poly(B,ell,precision)) per call. Prepare lambda copies,
apply J, test collisions and coherently amplify with its success floor.
Hamiltonian rows have O(n^(p/2)ell^(p/2)) neighbors. Each coefficient lookup
scans the M-bit table, with no free QRAM. Sparse filtering normalization
alpha=O(D/sqrt q) and window separation Delta=Theta(bD) cost
poly(n^p,ell,B), including alpha/Delta=O(1/(b*sqrt q)). Use separated
pass/reject energy windows; a gap around every eigenvalue is unnecessary.
The outer call budget is

 R<=h^(-lambda)*exp(O_(p,k)(ell))*poly(L,log(1/eta)).

Filter false-pass amplitude and per-call circuit error are o(eta/R).
Precision O(B+ell*log n+log(1/eta)) pays the hybrid error, arithmetic,
state-preparation inverses and table scans. Null soundness follows from
its norm bound even after amplification. Choose eta=o(1); statistical,
source and implementation errors sum to o(1).

The CLOSED WRITTEN gate/bit upper bound in the displayed polylog ell regime is

 n^(ell/4)*exp(O_(p,k)(ell*log ell))*poly(n^p,B).

No implementation, practicality, community-label recovery, tomography,
classical lower bound, novelty or Shor-level advantage is asserted.

## Next decisive gate: stronger same-input classical algorithms

The fair-clone p4 cancellation and asymmetric correction are established.
For the SAME original near-threshold signal, the asymmetric matrix loses
1-o(1), so the original unnormalized Kikuchi hierarchy can lower ell by
only1-o(1) under the same sufficient constant. This compares ONE explicit
method. For stronger original signals, attenuation cannot justify forcing
a classical competitor to use the weaker level. No new advantage is claimed.

Fresh corpus queries gave no direct baseline entry. Actual primary sources
were then fetched and inspected: Schmidhuber--Hastings 2607.29672v1
(Theorem5.3, section6 and Remark2.7), and Babakhani et al. 2610.40941v1
(detection Theorem3 and AppendixB). The former includes a log-free normalized
Kikuchi bound and vanishing-bias even extension. Its section13 observes
Boolean random literals, absent here. HCE's printed detection theorem has
fixed cover order and rank-one Boolean signals. These are obligations to
prove a transfer, NOT evidence that the classical attacks fail. The community
arXiv page still lists only v1 at this check.

Two DISTINCT paid classical attacks run in
`audits/api_inputs/2026-11-13-community-baseline-attack/dispatch.json`:
normalized trace adaptation and cycle-contraction detection. A log-free
native classical threshold would use ell_classical=O(log n) at the p4
beta~1/(n sqrt(log n)) example, beating repaired quantum ell~log²n.
This is the next concrete falsifier; no recovery or quantum extension first.


## Superseding log-free milestone

The classical comparison gate closed in NATIVE_COMMUNITY_CLASSICAL_MATCH.md
and the334LF independent native-classical-match proof, fully parent checked.
A direct deterministic-support trace bound applies to both slice and ORDERED
matrices, followed by exact independent-copy symmetrization of Bernoulli
noise. At fixed q it removes sqrt(logn) from the matrix SNR threshold in
this EXISTING compiler. The earlier Bernstein construction remains valid,
but its log²n-level clock is superseded in the p4 beta~1/(n sqrtlogn) window.
The paid quantum clock at ell~logn is n^(ell/4)exp(O(ell logell))poly(n^p,B).
Two classical bounds are also now established (direct trace and restricted
HCE); neither implies unrestricted dominance over the upgraded quantum
construction. No novelty, new advantage or Shor-level conclusion. No quantum
implementation, recovery or further neighboring variant is selected.
