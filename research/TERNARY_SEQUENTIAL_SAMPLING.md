# Sequential Classical Sampling From Fixed-Prime BPQM Success

31 October 2026. Constructive conditional classical sampling theorem;
independent automated whole-composition review completed, no fatal gap found.
Three reviewers checked primary theorem scope, posterior/transfer algebra
and short-cycle geometry. This is not human peer review, a novelty claim or
an executed large-instance sampler. It removes the prospective superpolynomial
quantum sampling separation under the SAME premises and native input law below.
Section7 gives the general fixed-prime theorem; Sections1-6 derive the original
ternary construction and the binary corollary.

## Problem, Candidate And Dependencies

Match six distinguishable sockets at each of V spins to three at each of
M=2V constraints uniformly. Give every matched socket pair (incidence) one
independent uniform nonzero F3 coefficient. Aggregate repeated incidences to obtain
H of size V by M. J is independent uniform in F3^M. The target is UNIFORM
on all original x satisfying J+H^T x in {1,2}^M, with ABSTAIN as the target
law when the solution set is empty. No conditioning on rank, simplicity,
girth, satisfiability or a planted solution is allowed. The raw signed socket
graph is supplied, as in the original block-decoder input; it is not inferred
from an aggregated matrix after cancellations have hidden its edges.

The CLASSICAL algorithm initializes the short-cycle components
exactly, then adds the remaining ORIGINAL constraints one at a time and
resamples a small tree neighborhood conditional on its unchanged exterior.
It uses polynomial arithmetic and exact tree/unicyclic dynamic programming.
There is no quantum decoder call, unknown partition function or SAT oracle.

The proof imports two EXISTING quantitative premises of the quantum proposal:

- Its original signed-trine density-evolution bound
  F_(13+t)<=f*lambda^(2^t-1), f<=0.006332239, lambda<1/3.
- Vanishing ensemble-average whole-code error delta_M of the actual
  offset-independent decoder. The cited q-ary Theorem30 and this success-
  region certificate are the prior justification for delta_M->0.

Primary dependencies: [Mandal et al., Theorem30](https://arxiv.org/html/2609.05857v1#S6)
and [Mandal--Pfister's q-ary node operations](https://arxiv.org/html/2601.21330).
The known channel-duality framework is [Renes1701.05583](https://arxiv.org/abs/1701.05583).
The binary local specialization already exists in the retained
bundles/bpqm-tree-duality-2026-10-24/TREE_DUALITY.md. Here the signed q=3
posterior calculation and the finite-graph insertion argument are explicit.

The first premise supplies classical tree reconstruction decay by exact
channel duality. The second is used ONLY as a mathematical count-flatness
bound. Both must refer to this same socket/coefficient ensemble. Consequently
any invalidity in them also invalidates the original quantum comparison.
Only existence and performance of the ideal decoder POVM are needed: its
unitary dilation supplies the norm/Parseval count identity. Efficient coherent
compilation, finite-gate synthesis and a native quantum run are NOT premises
of the resulting classical algorithm.

Conclusion: a classical polynomial-time sampler with ensemble-average
TV error tending to zero, including failures, whenever those same premises
hold. This removes the proposed exponential sampling advantage for this
specific ensemble. It does not settle worst-case ternary CSP, arbitrary
quantum decoders or a different spin model. Novelty is not asserted.

## 1. Exact Ternary Tree Duality

Represent a symmetric classical observation channel by its posterior shape
nu=(nu_0,nu_1,nu_2), modulo the observed cyclic translation, with the correct
probability law on shapes. A revealed symbol has shape delta_0. Put
mu=(0,1/2,1/2), and hat(nu)=sum_j nu_j omega^j.

Two independent observations of the same uniform symbol combine by

    d_h=sum_j a_(j+h)*b_j,
    nu_h(j)=a_(j+h)*b_j/d_h,   Pr(h)=d_h.

This is precisely the BPQM CHECK spectral update. Zero-probability branches
are omitted; no favorable branch is renormalized. The native three-spin
factor sends mu convolved with its two signed child posterior shapes. This
is the BPQM BIT convolution, with the physical mu included. Reflections from
F3* coefficients and translations from offsets preserve |hat(nu)|; coefficient
averaging must still use the original independent socket law.

Let A combine FIVE same-spin observations and B convolve mu with TWO child
shapes. For free-boundary tree reconstruction with the distant Gibbs boundary
drawn and then revealed, and for the BPQM extrinsic recursion, respectively,

    V_0=delta_0,  V_(t+1)=A(B(V_t)),
    U_0=mu,       U_(t+1)=B(A(U_t)).

Hence U_t=B(V_t) and V_(t+1)=A(U_t) exactly in distribution. The relevant
quantum mean fidelity at q=3 is F_t=E|hat(U_t)|. For any posterior shape,

    KL(nu || uniform)<=chi^2(nu,uniform)=2|hat(nu)|^2<=2|hat(nu)|.

Conditional independence gives I(X;Y_1,...,Y_s)<=sum_j I(X;Y_j). Pinsker
therefore bounds the expected root posterior TV by sqrt(s F_t), for s<=6
branches after the factor depth t. A tree of smaller degrees is a degraded
observation experiment: complete the missing branches and reveal their data.
Thus sqrt(6 F_t) is also a uniform bound for these truncated degree-bounded
trees, averaged over their ORIGINAL random coefficients and planted tree law.

This is free-boundary reconstruction, NOT worst-boundary uniqueness. The
existing simplex split/degradation certificate is consistent with this
direction: revealing the split flag makes the classical observation more
informative, while it worsens the quantum pure-state discrimination problem.
Replacing discarded mass by a point spectrum likewise gives the classical
observer MORE information. No coherent register is discarded in this argument.

## 2. One-Constraint Replacement Identity

Fix an already imposed prefix and its exact uniform solution law pi_old.
The new factor event is A. Let I be its internal tree neighborhood and b
the exterior assignment. Define

    w(b)=Pr_pi_old[A | outside=b],   p=Pr_pi_old[A]=Z_new/Z_old.

Keep b from an old sample and sample the interior EXACTLY from the new
conditional distribution. If w(b)=0, return ABSTAIN. The output differs
from pi_new only through the exterior marginal; in particular, for p>0,

    e <= (1/(2p)) E_old |w(b)-p|
       <= (1/p) E_old |w(b)-2/3|.

The first inequality allows merging all failed boundary records into ABSTAIN.
It is equality if those records are retained separately. The second follows
from p=E_old w and the triangle inequality. No minimum bound on EACH w(b)
is needed: frozen or impossible boundaries are included in the error.

When deleting the new factor leaves three disjoint tree neighborhoods,
the three root posterior laws conditional on the exterior are independent.
Uniform root laws make A have probability exactly2/3. Product-TV contraction
then bounds |w-2/3| by the sum of the three root posterior deviations.
Under the PLANTED PREFIX law, their average is at most

    3 sqrt(6 F_t).

Why this is the actual local law: choose all planted spins independently
uniform, choose nonzero noises independently on the existing factors, and
set their offsets accordingly. Marginalizing exterior factor noises leaves
exactly the free Gibbs law on each local tree. The conditional interior given
the full exterior depends only on the local labels and boundary spins, by
the factorization. No independence of the entire quenched boundary is assumed.

## 3. One Final Planting Transfer, With Exact Prefix Cancellation

Fix H and a constraint order chosen from its topology, independently of J.
Let Z_i be the solution count after its first i factors, and

    z_i=Z_i / [3^V (2/3)^i],    0<=i<=M.

Let Q_i be the uniform law on those offsets and P_i their planted law. Exact
counting gives dP_i/dQ_i=z_i. Under P_i, a conditional planted spin is uniform
on prefix solutions. Since planted generation chooses ONE uniform spin vector
and then independent nonzero noises for all factors, the prefix marginal of
the FINAL planted law P_M is exactly P_i. This holds for a topology-dependent
order, including putting all bad factors first.

Let R_i=P_(i-1) times an independent UNIFORM new offset. Because
p_i=Z_i/Z_(i-1)=(2/3)z_i/z_(i-1),

    dP_i/dR_i = z_i/z_(i-1) = (3/2)p_i.

Multiplying the previous replacement bound by this density CANCELS its
potentially small p_i denominator exactly:

    E_P_i e_i <= (3/2) E_R_i E_pi_(i-1)|w-2/3|
               <= (9/2) sqrt(6 F_t).

Zero-count prefixes have zero planted mass; they require no division. Empty
boundary conditionals within a nonempty prefix are already included in e_i.
The ideal e_i is a function only of H and the prefix offsets. The block and
ordering use no future labels. Thus E_P_M e_i=E_P_i e_i.

For EACH fixed full instance with nonempty target, Markov-kernel contraction
telescopes these local errors from exact initialization. ABSTAIN is absorbing
and included as an ordinary extra outcome. Average this pointwise bound under
P_M, then transfer the final bounded error function ONCE from P_M to Q_M:

    E_Q_M TV(output,target) <= eta_H + sum_i E_P_i e_i,
    eta_H=TV(P_M,Q_M)=(1/2)E_Q_M|z_M-1|<=sqrt(2 delta_H).

On an empty full target, every successful purported output is checked against
the original constraints and cannot occur. The sampler returns ABSTAIN, so
the specified extended target law is respected. Geometry aborts are charged
separately. No actual count z_i, planted witness or decoder is supplied to the
algorithm. This argument transfers ANALYSIS, not input generation.

As a separately checked alternative, z_i is a nonnegative martingale:

    z_i=E[z_M | J_1,...,J_i],   z_0=1.

Therefore Doob's inequality for |z_i-1| gives

    Pr_J[exists i: |z_i-1|>=1/2] <= 2 E_J|z_M-1| = 4 eta_H,

This gives a looser one-time transfer proof, but is not needed for the sharper
prefix-cancellation argument. Paying M*eta_H would be an avoidable loss; mere
delta_M->0 need not support such a loss.

## 4. Short Cycles Must Be Initialized, Not Ignored

Set t=O(log log M) large enough that F_t<=M^-8. Choose an incidence radius
r=4t+10. Mark a factor bad if its full radius-r incidence neighborhood has
a cycle, keeping socket multiplicities when counting cycles. Put all bad
factors first. Include all their incident variables in the initial subgraph.
If any connected component of this subgraph has cycle rank greater than one,
ABSTAIN. Otherwise sample it exactly by tree/unicyclic dynamic programming;
sample isolated spins independently. An empty initial component certifies
the full target is empty and also returns ABSTAIN.

Here is a sufficient event with explicit radii: EVERY vertex-centered
radius-(r+2) ball has cycle rank at most one. Every bad factor has a unique
witness cycle C. Adjacent bad factors are distance two apart, so their
witness cycles both lie in a radius-(r+2) ball and must be the SAME C.
Induction along a bad-component path proves all its factors share C. For
any c in C, each such factor is within r of c; every incident variable is
within r+1. That entire component therefore lies in a unicyclic ball.

A radius-(r+2) exposure uses K=O(5^(r+2)) sockets at maximum degree6.
Each pairing has collision probability O(K/M); two collisions have probability
O(K^4/M^2). Union over the 3M/2 vertices gives O(K^4/M)=polylog(M)/M.
This counts two parallel edges as one cycle and three as excess two. Bounds
are asymptotic; probabilities are capped at one for small M.

For each remaining factor, deleting that factor leaves three disjoint tree
neighborhoods to the needed depth. All prefix factors are a subgraph of this
full neighborhood, so the same property holds throughout the algorithm.
Retain all actual constraints incident to an interior spin and pin their
boundary spins when doing the conditional tree dynamic program.
Concretely, from each root variable use generations0 through t as interior
and generation t+1 as boundary; a generation costs TWO incidence edges.
The root reconstruction bound from F_t uses t+1 factor-generations. Include
only already imposed factors plus the new root factor in the conditional law,
while topology may be explored in the full graph. Radius r=4t+10 safely
contains every incident factor and boundary vertex. Missing prefix branches
contribute no artificial pinning.

This graph event depends only on the original socket topology. It neither
conditions the source on simplicity nor deletes parallel constraints. The
algorithm checks the bad components directly and aborts if they are complex;
it need not certify the stronger sufficient event.

## 5. Bound, Resources And Falsifiers

Combining the preceding pieces gives

    E_(H,J) TV(output,target)
       <= Pr[bad geometry] + sqrt(2 E_H delta_H)
          + (9/2) M sqrt(6 F_t) + epsilon_coins.

All terms tend to zero under the SAME premises used for the quantum sampler.
The delta term needs no strong finite-size rate: prefix cancellation avoids
multiplication by M. The initial components together contain O(M) nodes;
their exact counts have O(M) bits. Cut one cycle variable, try its three
values, count the remaining forest, and sample proportionally. Later blocks
have polylog-size and polylog-bit counts. Bounded-degree BFS, exact integer
dynamic programming and sampling therefore take polynomial BIT time, with
fixed but enormous constants/exponents; no near-linear bit bound is needed.
Cap exact rational coin-generation retries with total epsilon_coins=o(1).
No practical block size or empirical speed comparison is claimed.

Strongest prior comparators were rank-conditioned rejection, exact finite
SAT pools and hash isolation with paid cell solving. The current mechanism
uses the tree and disorder information that those baselines did not exploit.
Its decisive falsifiers are an incorrect posterior/herald law, a failure of
the exact prefix likelihood ratio, a double-counted field of conditioning,
unsolved multi-cycle initial components with nonvanishing probability, or
an invalid quantum-to-count premise. Finite SAT timeouts and worst-boundary
freezing neither establish nor refute this ensemble-average construction.

The primary sampling comparison includes
[Efthymiou2007.07145v4](https://arxiv.org/html/2007.07145v4), whose
single-factor SET contraction is stronger than free-boundary nonreconstruction
and whose random hypergraph model is different. It cannot simply be cited
as this regular signed ternary theorem. The separately checked argument here
may still be a specialization of broader prior machinery; no novelty follows.
For our single constraint the JOINT distribution of the other two spins,
conditional on distinct first-spin values, has TV exactly1/2: distinct
forbidden affine lines each remove three of nine pairs. SET B.1 would require
less than1/[d(k-1)]=1/12 at d=6,k=3. Uniform individual pairwise marginals
do not change this joint coefficient. This only excludes that sufficient
condition, not classical sampling.

Local heat bath has rare counterexamples within the original support:
for V>=4 with 3 not dividing V, duplicate each cyclic triple
(x_i,x_(i+1),x_(i+2)) with offsets1 and2 and coefficients+1. Each pair forces
the sum to zero; consecutive equations give x_i=x_(i+3), so only the three
constant solutions remain. Every proper-coordinate-block update is frozen.
This refutes all-instance irreducibility, not typical sampling or the present
initialized insertion algorithm.

## 6. Binary Native Gibbs Corollary

The same argument applies to the retained binary signed regular arity3,
spin-degree6 model, M=2V, at c=13/20, with normalized factor weights

    psi_a(x)=1+c*(-1)^(J_a+(Bx)_a),
    z_i=2^(-V) sum_x product_(a<=i) psi_a(x).

Its target is the original Gibbs law on ALL spins, with IID uniform J.
The planted noise has probabilities (1+c)/2 and (1-c)/2. Here mean new-factor
weight is1, so dP_i/d(P_(i-1) times uniform J_i)=p_i=Z_i/Z_(i-1).
Replacement gives e_i<=E_old|w-1|/p_i; its denominator cancels as above.
After deleting a good clause, w-1=c*(-1)^J m_1*m_2*m_3 for the three root
posterior magnetizations. Each has at most five existing branches, hence

    E_P_i e_i <= c sqrt(q_L),

where q_L bounds the cavity posterior second moment. The retained exact
TREE_DUALITY.md gives q_(12+s)<=(80/169)*10^(-2^s). The retained
CLUSTER_TRANSFER.md count identity gives eta_full<=sqrt(E delta_B).
Therefore, under the same binary whole-code theorem,

    E TV <= bad_geometry + sqrt(E delta_B) + c M sqrt(q_L) + coin_error ->0.

Choose q_L<=M^-8 with L=O(loglog M). The proof needs the ideal POVM's
vanishing error, not a quantum implementation. Positive factors eliminate
empty conditional blocks. At c=13/20, DP uses integer weights33 and7 after
removing common denominators. This remains polynomial bit complexity.

For the MATRIX-ONLY binary input, use the aggregated incidence graph G'.
Its factor degrees are1 or3. Initially mark every factor within radius R
of a degree1 factor, plus factors with cyclic radius-R neighborhoods.
Every degree1 factor arises from repeated raw sockets and thus a raw cycle;
the marked set is contained in the raw bad set at radius R+2. Visible cycles
also lift to raw cycles. Under the corresponding radius-(R+4) tangle-free
event, the marked support components are subgraphs of raw unicyclic components
and permit the same exact DP. Remaining insertion neighborhoods have genuine
arity3 and variable degree at most6. Their missing branches are simply absent.
This preprocessing depends only on binary topology, not J; no lost raw-socket
information is queried. The raw graph is used to prove its probability bound.

The corollary does not refute the published DQI/Prange theorem on a different
large-arity Erdos--Renyi ensemble, or classical/quantum stable-algorithm
barriers. It addresses the explicit regular c=13/20 point and the local
BPQM success premises retained in this repository.

## 7. General Fixed-Prime BPQM Success Region

**General theorem, independently reviewed 2026-10-31.** Fix a prime q,
constant degrees 3<=a<b, and a fixed rational probability vector mu on F_q.
Zero entries and nonsymmetric mu are allowed. Let H be the V-by-M matrix
of the original (a,b)-regular configuration multigraph, aM=bV, with one
independent uniform nonzero coefficient on EVERY matched incidence. Supply this raw
socket representation; sum parallel incidences in the native matrix.
Draw J uniformly from F_q^M, independently. The target, on all original
spins x in F_q^V, is

    pi_(H,J)(x) proportional to product_i mu(J_i+(H^t x)_i).

Define an empty target as the point mass ABSTAIN. Define the symmetric
pure-state channel by

    |psi_c> = sum_z sqrt(mu(z)) omega^(c*z) |z>,

where omega is a primitive qth root of unity. Suppose this channel belongs
to the BPQM success region of the cited qary block theorem. Then the
classical initialized insertion algorithm has polynomial BIT complexity
and ensemble-average TV from the target tending to zero as M grows.
This is pointwise for each fixed q,a,b,mu; it is not uniform for an
M-dependent approach to a threshold. No algorithm decides membership in
that success region, and the sampler does not query such an oracle.

The source theorem is explicitly imported, not newly proved here:
[2609.05857v1](https://arxiv.org/html/2609.05857v1#S6), Section2.1,
Definition4, Lemmas7/14-16/21, Theorems26/30. It fixes PRIME q; circulant
Gram matrices need not have positive real overlaps, full rank, or reflection
symmetry. Theorem26 gives the double-exponential fidelity tail and
Theorem30 the ensemble-average whole-code error. The ordinary channel
and exact finite weights above avoid adding an arbitrary initial herald
mixture or a weight-evaluation oracle to that theorem's scope.

### Coefficient-aware tree identity

Write D_c nu for the pushforward of a law by z->cz. Use additive ERROR
shapes for observations Y=X+E, rather than silently reflecting a posterior.
For factor f and its root variable v, the outgoing error law is

    D_(-h_vf^(-1)) [ mu * product_convolution_(u!=v) D_(h_uf) nu_(u->f) ].

Indeed J_f=N_f-sum_u h_uf X_u, N_f~mu. Substituting the child observations
into -h_vf^(-1)(J_f+sum_(u!=v)h_uf Y_u) gives X_v plus exactly that error.
At a variable, two independent observations have relative shift h and
combined error law

    d_h=sum_j alpha(j+h) beta(j),
    nu_h(j)=alpha(j+h) beta(j)/d_h,       Pr(h)=d_h.

Discard only zero-probability flags. These are precisely the spectral
convolution and weighted shifted-product rules after the corresponding
edge-frequency chart changes. Keep the D_c permutations, reflections,
complex Fourier phases and flag weights. Section3.4 of the source proves
that normalized relative coefficients have the required independent
uniform law. No assumption mu(cj)=mu(j) is used. Missing prefix branches
are removed observations, so completing to the full regular tree only
increases information under the planted free-boundary law.

For nu_hat(r)=sum_j nu(j)omega^(rj), put

    F_t=E[(q-1)^(-1) sum_(r!=0) |nu_hat_t(r)|].

The matching channel fidelity is exactly this quantity. Parseval gives

    D(nu||uniform)<=chi_squared(nu,uniform)
       =sum_(r!=0)|nu_hat(r)|^2 <=sum_(r!=0)|nu_hat(r)|.

Conditional independence of the at most b incoming observations, followed
by Pinsker and Jensen, gives the sufficient root bound

    eta_t := E TV(root posterior,uniform) <=sqrt(b(q-1)F_t/2).

The boundary is sampled and revealed in the planted tree; this is not a
worst-boundary assertion. The depth convention is as in Section1: a
factor-message at level t uses root boundaries t+1 factor generations away.

### Arbitrary-rank count-flatness and weighted insertion

For a fixed H, let W=im H^t, C=ker H and N=|C|. The Gram matrix of the
uniform codeword states indexed by C is diagonalized by characters indexed
by cosets J+W. Its eigenvalues are

    lambda_[J]=N sum_(z in J+W) product_i mu(z_i).

With psi=q*mu, normalized partition z(J)=q^(-V)sum_x product_i psi(...)
is EXACTLY lambda_[J], including rank-deficient H. It is also the likelihood
ratio between planted J and uniform J. Let A=N^(-1)sum_[J]sqrt(lambda_[J]).
Covariantizing any uniform-codeword POVM, then applying Cauchy--Schwarz to
its character-sector matrix elements, bounds its success by A^2. Therefore
any decoder with block error delta_H implies 1-delta_H<=A^2. The classical
affinity/TV inequality now gives

    eta_H=TV(planted J,uniform J)<=sqrt(1-A^2)<=sqrt(delta_H).

Explicitly, in the orthonormal character sectors with p_J=lambda_J/N>0,
the fiducial state has amplitudes sqrt(p_J). Twirling gives a seed POVM
element whose diagonal entries are1/N; positivity bounds each off-diagonal
entry in modulus by1/N. Its success is at most
(sum_J sqrt(p_J))^2/N=A^2. Sectors of zero probability contribute zero.

This sharpens, but does not invalidate, the looser sqrt(2delta_H) used
earlier. Zero eigenvalues and rank deficiencies need no conditioning. The
POVM is used to bound a partition function; the classical algorithm never
runs or simulates it and is not a decoder for unknown quantum outputs.

For any topology-only prefix order, set Z_i=sum_x product_(j<=i)psi_j(x)
and z_i=Z_i/q^V. Planted prefix P_i has likelihood z_i relative to uniform
prefix Q_i. Writing p_i=Z_i/Z_(i-1) and R_i=P_(i-1) times uniform J_i gives

    dP_i/dR_i=p_i.

For outside spins b, let w(b)=E_old[psi_i|b]. Exact replacement inside the
tree block, with ABSTAIN when w=0, has error

    e_i<=E_old|w-p_i|/(2p_i)<=E_old|w-1|/p_i.

Multiplication by the prefix likelihood cancels the denominator. With
Delta_mu=max(mu)-min(mu), uniformizing the a separate root marginals gives
the conservative bound E_P_i e_i<=q*a*Delta_mu*eta_t. In fact one uniform
root suffices for this additive factor, but that improvement is not needed.
All these expectations average the ORIGINAL coefficient law; they are
not pointwise statements for every signed H. The full planted law has
exactly these prefix marginals. Telescope the Markov kernels and transfer
the bounded final error function to uniform J ONCE, as in Section3.

### Algorithm, resources and resulting bound

Choose t=ceil(tau*loglog(M+3)) with tau>1/log(a-1), and radius r=4t+10.
Initialize all cyclic-radius-r factors first, using exact weighted DP on
each tree/unicyclic component; if a component has excess cycle rank, return
ABSTAIN. Insert the remaining factors in any topology-only order. Resample
their entire specified interior from the exact NEW conditional, including
every prior factor incident to it, and retain the actual outside boundary.
Failure is absorbing, and final original-weight verification is mandatory.

The geometric argument of Section4 uses only bounded degree. With
D=max(a,b), every radius-(r+2) ball has cycle rank at most one, with failure probability
O(D^(4(r+2))/M)=polylog(M)/M. On that event, all initially marked connected
components are unicyclic and all later insertion neighborhoods are trees.
Thus, with epsilon_coins for a cap on exact rational coin retries,

    E_(H,J) TV(output,pi_(H,J))
       <= Pr[bad geometry] + sqrt(E_H delta_H)
          + q*a*Delta_mu*M*sqrt(b(q-1)F_t/2) + epsilon_coins ->0.

Theorem26 supplies F_t<=C exp(-c(a-1)^t) for constants depending on the
fixed channel; Theorem30 supplies E_H delta_H->0. The chosen depth works
without computing these constants or a DE table. The proof does not need
a quantitative finite-block rate. In particular, mere block-error
convergence WITHOUT the separate tree-tail mechanism would not suffice.

Use a common integer denominator for the fixed rational mu. DP numerators
and denominators have O(M) bits initially and polylog(M) bits on local
blocks. Cutting one cycle variable requires q cases, and factor sums have
q^a terms, both constants here. There are polynomially many arithmetic
operations and random-bit draws. Capping the ordinary integer-rejection
coin after M retries per draw gives total epsilon_coins=o(1) and a bounded
polynomial runtime. No potentially exponential global assignment is enumerated.

This closes a prospective SUPERPOLYNOMIAL sampling separation throughout THIS
fixed-prime regular BPQM success class, conditional on the imported theorem.
Polynomial or practical quantum improvements remain possible. It does
not close quantum communication advantages, all-instance sampling, dense
AG/DQI constructions, growing/succinct alphabets, arbitrary graphical
models, or mixed-state channels. Prime powers require additive-character
and source-theorem work not included here. The general qary interface is
RAW SOCKETS; only the binary matrix-only repair in Section6 was separately
proved. No novelty or practical complexity claim follows.

## Verification And Next Selection

Executed:27 existing tests in tests/test_ternary_bpqm_certificate.py passed,
including the full exact level13 certificate and directed physical controls.
The independent reviewer recomputed the exact first-level value961/2048 and
tail multiplier. No new quantum/compiler tests or whole suite were run.

The focused Sage control classical_baselines/ternary_insertion_identities.sage
checks nonconstant conditional probabilities with exact TV1/6, a zero-mass
boundary with ABSTAIN and TV1/3, and all40 prefixes of a small affine system
for the count-martingale and planted-density identities. These are algebraic
falsifiers, not random-ensemble evidence or an implemented sampler.

The generalization's independent reviews checked the actual primary
fixed-prime theorem, nonsymmetric coefficient/error charts, arbitrary-rank
Gram/count identity, weighted prefix cancellation and paid DP. The final
Sage control classical_baselines/bpqm_general_identities.sage passed:
actual planted F5 observations match the asymmetric factor and weighted
relative-shift laws, and30 exact character eigenvalues match original-spin
partition sums, including rank deficiency. These controls falsify algebraic
errors; they are not a production sampler or evidence for a new threshold.

The intervening fixed-field AG audit recovered the existing matrix-only
ECP/truncated-DQI comparator and the stronger NORM_SAMPLER_CLOCK_FALSIFIER.md.
The latter already proves exponential acceptance clocks for fresh quadratic
norm proposals at fixed q, not merely a vacuous union bound. Four-base/AJT
existence, root count FPTAS and small fixed-bank repairs do not supply a
polynomial extractor. No new correlated repair was found. The fixed-F1019
source is nonvacuous along dyadic e, while arbitrary-level construction is
still unimplemented. These are recovered scope facts, not new theorems.

Stop new fixed-prime regular BPQM parameter campaigns as prospective
unmatched samplers. Re-entry requires leaving a stated premise and supplying
a paid new receiver/output mechanism. The broader remaining scientific
question is a motivated native problem with an end-to-end quantum comparator
outside this class. AG has such a known comparator but still needs a useful
reduction or new classical selector; Hawk has no paid generator mechanism,
and integral similarity is already prior art. No extra backend, larger
fixture or nearby restricted-walk barrier is justified by this pass.
