# Independent next-direction comparison

13 November 2026. Selection review only. No new algorithm, speedup, novelty,
or lower bound is admitted. STATE, TRAPS, GOAL, and
NEXT_CONSTRUCTIVE_MECHANISMS were read. No network, API, Git, numerical
sweep, or shared-state edit was made. Current primary papers below were
downloaded by the parent; their actual theorem text was then inspected.

**Decision: none of these three mechanisms currently justifies replacing
the live full-native relation completion. Do not fund the Anderson overlap
proof.** It was the strongest fresh classical-input contender before the
current-literature check, which supplied a matched classical algorithm.
The Markov learner has a concrete constructive route but insufficient
relevance to this owner's computational-discovery goal. The Jack transform
has the greater remaining algorithmic upside, but presently lacks an
actual unitary recursion. That is a candidate for primary-source screening,
not an admitted next proof campaign. If the last sparse-support attempt
stops, this review does not justify extending its nearby barriers either.

## 1. Finite-bath Anderson preparation: initially first, now classically matched

The externally motivated problem is a finite metallic impurity model used
in condensed-matter and embedding calculations. For odd n=2M+1 let

    H(U,V) = sum_(j=-M)^M sum_sigma [j/(M+1)] c†_(j,sigma)c_(j,sigma)
             + (V/sqrt(n)) sum_(j,sigma)
                    (d†_sigma c_(j,sigma)+c†_(j,sigma)d_sigma)
             + U (n_(d,up)-1/2)(n_(d,down)-1/2).

Input is the explicit finite model, rational U,V, and epsilon,eta. Charge
n numerically and all coefficient bits. For example fix 0<=U<=4 and
1/2<=V<=1; these are absolute compact bounds, not binary-encoded unbounded
coupling promises. The degree-two coefficient V/sqrt(n) is explicitly
computable; polynomial-bit approximation is sufficient after charging
operator error. The target was the GLOBAL ground energy to additive
epsilon and a state of energy at most E0+epsilon. This is neither an exact
ground-state trace-distance demand nor a thermodynamic/continuum Bethe
Ansatz limit. Inverse-polynomial epsilon=n^(-c), for fixed c, is essential
to the proposed asymptotic comparison.

The concrete quantum operation would be spectral filtering of the explicit
U=0 Gaussian ground state Omega0. A sufficient single new theorem is

    <Omega0, 1_[E0,E0+epsilon](H(U,V)) Omega0>
        >= C^(-1) (epsilon/(n+1))^C,

uniformly in the declared family, for a fixed C. Repeated phase estimation
and selection of the lowest recorded energy would then prepare a low-energy
state and estimate E0 in polynomial(n,1/epsilon,log(1/eta)) time. There is
no supplied ground energy, adiabatic path gap, inverse state oracle, or
unknown eigenvector. Quadratic-plus-one-quartic Hamiltonian simulation and
Gaussian input preparation have polynomial native descriptions. Energy
resolution and all repetitions must be charged; QPE does not cost only
log(1/epsilon). Degeneracy does not obstruct this energy-output version.

The cheapest substantive falsifiers were zero overlap from conserved
spin/parity/particle sectors, an unexpectedly superpolynomial edge-weight
decay, or an uncharged Kondo scale when U/V^2 grows. The compact coupling
regime avoids claiming uniformity in that last limit. Anderson-orthogonality
or Fermi-liquid folklore is not a quantitative lower-bound proof.

The retained OLD primary Bravyi--Gosset source, actual Theorem 1, gives
n^3 exp[O(m log^3(m/epsilon))] classical arithmetic cost; Theorem 4 already
gives polynomial cost under a constant full many-body gap. These were read
in audits/sources/two_gaussian_learning/bravyi_gosset.txt, physical lines
182--236 and 405--424. Thus even before the new source, constant precision
or constant-gap preparation was not an attractive advantage target.

**Decisive current correction.** Actual Theorem 1.1, printed page 4, of
Arunachalam et al., 2610.02130v1, states classical runtime

    poly(N,1+||V_imp||) exp[O(m log(m/epsilon))]

for global ground energy AND a Bogoliubov transformation U_out and a
normalized superposition of exp[O(m log(m/epsilon))] Fock vectors attaining
that energy. See audits/sources/impurity_current_baseline/
arunachalam_et_al.txt, physical lines 135--196. This is actual model and
theorem text, not an inference from its abstract.

Our model has N=2(n+1) fermionic modes and m=4 impurity Majoranas. Absorb
-U(n_up+n_down)/2 into H0 and restore the scalar U/4 afterwards;
V_imp=U n_up n_down has norm U. The one-body operator norm is bounded by
1+V+U/2, hence normalization changes epsilon only by a constant factor.
The theorem explicitly allows the required model. Its stated cost is
polynomial at inverse-polynomial precision without a spectral-gap promise.
Moreover its Fock vectors share ONE Bogoliubov transformation. A polynomial
list of orthonormal Fock amplitudes can be loaded coherently and followed
by that transformation, so demanding a preparable low-energy state does
not restore the proposed advantage. Precision auditing of the paper's
whole algorithm is the parent's separate task; no stronger theorem is
imported here. Jiang et al., 2610.02167v2, was also located by the parent;
its abstract/informal theorem is unnecessary to this disposition.

This kills this selection argument, not the displayed edge-weight
conjecture. Do not rescue it by quietly changing to growing impurity size,
unbounded coupling, or full real-time dynamics: each is a different task
with new baselines. The current paper itself discusses dynamics separately.

## 2. Markov-switched Gaussian noise: constructive, lower goal value

Input is fresh independent episodes of a stationary two-state hidden Markov
process. At time t, state Z_t selects one of two unknown FULL ordinary
fermionic Gaussian CPTP maps G1,G2 on n modes. The classical transition is
independent of the user's inputs. Known Majoranas and ordinary channel
uses are provided; hidden states, weights, transition probabilities,
source environments, inverses, and controlled-channel uses are not.
Output is an explicit two-state classical-memory/Gaussian-channel circuit
approximating the entire T-use process to epsilon in operational distance
against arbitrary adaptive entangled testers, with confidence 1-eta.
Target cost is polynomial(n,T,1/epsilon,log(1/eta)). This would be useful
for correlated-noise characterization, but is a quantum-data learning
theorem, not a classical-input quantum computational advantage.

There is a specific new operation. Let p=Pr(Z=1), q=1-p, lambda be the
nontrivial Markov eigenvalue, theta_i the Gaussian Choi covariance vector,
Delta=theta_1-theta_2, and mu=p theta_1+q theta_2. Independent local probe
outcomes have conditional means theta_(Z_t). Their centered cross-time
moments obey the ordinary tensor identities

    C_1 = pq lambda Delta tensor Delta,
    C_2 = lambda C_1,
    C_123 = pq(q-p) lambda^2 Delta tensor Delta tensor Delta.

These follow from E[Z_(t+r)-p | Z_t]=lambda^r(Z_t-p) and
(Z-p)^2=pq+(q-p)(Z-p). They cover negative lambda and do not use Wick
factorization across a single unknown mixture. Three-step episodes give
all entries with polynomially many bounded-observable measurements.
Away from small signal, a rank-one inverse recovers lambda, Delta and p
up to harmless branch exchange. The transition matrix then has rows
(p+q lambda,q(1-lambda)) and (p(1-lambda),q+p lambda).

A full proof must give observable threshold tests and a fixed precision
ledger. There are physically plausible gap-free exits: a rare branch is
seen with probability at most T min(p,q); nearly equal Gaussian channels
are close by the existing full diamond continuity bound; a small |lambda|
is close to IID switching by a T-step coupling bound. Reconstruction must
preserve CPTP and stochastic positivity. A telescoping argument on the
classical-memory dilation must pay the final adaptive process norm.
Nonstationary reset and input-dependent hidden transitions are OUTSIDE
this input contract.

The strongest matched baseline is classical two-state hidden-Markov
spectral inference from these SAME observations. The closed repository
Gaussian-channel result already permits product preparations and ordinary
Pauli readout, so entangled-probe advantage cannot be assumed. Supplied
Gaussian channels are classically tractable for covariance processing.
Thus polynomial versus unrestricted process tomography is a structural
promise benefit, not a demonstrated quantum computational gain. Existing
Gaussian results make this plausible but do not make it the best use of
this owner's discovery budget. Current exact HMM/process-learning primary
scope checks remain for the parent. No paid temporal-extension task is
recommended here.

## 3. Jack/Calogero--Sutherland transform: higher upside, no paid recursion

A distinct classical-input target is the finite homogeneous Jack transform.
Input is a partition lambda of charged numerical size D and positive
rational coupling alpha in a fixed compact interval. In the power-sum
basis write J_lambda^(alpha)=sum_(mu partitions D) theta_mu p_mu and use
the Jack inner product <p_mu,p_nu>=delta_(mu,nu) z_mu alpha^length(mu).
Output the normalized coefficient state with amplitudes proportional to
theta_mu sqrt(z_mu alpha^length(mu)), to error epsilon. This is a concrete
finite integrable spectral-transform problem with relevance to
Calogero--Sutherland states; it is not a claim that a further position-space
discretization or physical observable readout is already paid.

Proposed complete mechanism: a reversible chain of branching/recoupling
isometries, computed from explicit Jack/Pieri coefficients, taking a
partition label to this coefficient state and uncomputing every path
register. Target resources are polynomial(D,coefficient bits,log(1/epsilon))
rather than enumerating all partitions. The native partition encoding,
coefficient evaluation, normalization, error propagation and final
uncomputation are all part of that target. Compact eigenvalue labels or
formal diagonalization are not a circuit.

The exact next question would be an explicit isometry identity and circuit
recursion for ONE branching step, followed by a polynomial-depth composition.
A cheap disproof is that the normalized Pieri transition has nonorthogonal
columns or leaves a path record whose erasure needs exponentially unlikely
postselection. A coherent sampler for a branching distribution is not the
Jack coefficient transform. A generic polar decomposition also needs a
native encoding and a singular-value/resource bound. These are the same
logical accounting requirements as any spectral transform, not a claimed
no-go for Jack functions.

Strong classical comparators are direct symmetric-function recurrences,
special-coupling Schur/zonal algorithms, sparse/low-degree partition regimes,
and any classical Born sampler or observable algorithm under the SAME
parameters. Current primary checks of Jack/Dunkl quantum transforms and
integrable state-preparation literature are pending. No matching full
transform was established by the corpus lookup, but absence in the corpus
is not evidence of novelty or hardness. This route has possible
superpolynomial algorithmic upside; presently its key operation is less
concrete than the falsified Anderson comparison, so it does not justify an
immediate paid proof dispatch.

## Corpus record and final gate

For each candidate, been-tried was run before baselines with
/opt/anaconda3/bin/python tools/corpus/cli.py and --no-refresh. Queries were:

- "Anderson impurity ground state preparation orthogonality catastrophe
  overlap bath quantum algorithm";
- "stationary hidden Markov Gaussian channel correlated memory noise process
  learning three time covariance strategy diamond";
- "Jack polynomial Calogero Sutherland Dunkl eigenstate preparation branching
  transform".

Anderson retrieval returned generic gap warnings; its SDP/Max-Cut baseline
hit was irrelevant. The retained actual impurity paper led to the current
literature check that changed the decision. Markov retrieval led to
GAUSSIAN_CHANNEL_MIXTURE_ADMISSION, whose FINAL scope explicitly lowers
priority because product probes suffice. Jack retrieval returned compact
harmonic-label and commutant-gap warnings plus tensor networks; these are
screening obligations, not direct lower bounds. No archive was read.

The recommended action is one decision, not three parallel projects:
**no pivot from this comparison yet.** Let the already-running native
Taylor result decide its own fullRel gate. If it does not close that gate,
reselect from a new concrete operation after primary checks; do not spend
on an impurity overlap theorem now known to have a matched equilibrium
algorithm, or choose a Gaussian extension merely because its backend is
available. All advantage/novelty gates remain false.
