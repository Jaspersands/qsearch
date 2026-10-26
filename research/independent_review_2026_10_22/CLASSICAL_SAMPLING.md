# Native classical sampling: constructive deductions and remaining gap

Status: independent mathematical deductions; not a claim of general
classical hardness or a polynomial native search algorithm.

## 1. An exact success calculation for systematic root proposals

Let A_b be the native solution set. Write
|A_b|=q^(N-K) 2^(-N) (1+e_b), |e_b|<=eta, using the proved character/MDS
fiber estimate. Choose ANY K pivot positions. Assign the other N-K
coordinates independently and uniformly from their accepted sets, then
solve the K field parity checks for the pivots. Each free assignment has
one completion and every valid answer has one free assignment. Hence

    Pr[full native success]=(1+e_b) 2^(-K).

This is an exact counting consequence for arbitrary targets and distinct
public points. It needs no random-code assumption, independence heuristic
for pivot outcomes, or supplied witness. For eta<1, independent restarts
have expected attempts in [2^K/(1+eta), 2^K/(1-eta)]. Each trial uses O(N)
root samples (trace-hyperplane sampling plus inversion), O(K(N-K)) field
arithmetic after a paid matrix inverse, and a native verifier. A trial cap
has explicit failure probability (1-p)^T. The result is exponential at
K=floor(n²/8); it is a valid comparator, not a dequantization.

Self-attack: this calculation applies to freshly independent systematic
root proposals. Adaptive proposals can correlate later assignments with
previous residuals, so their success is NOT bounded by 2^-K by this proof.

## 2. A direct classical Gibbs sampler at moderate temperature

Literature cross-check: restricted surjectivity alone would not justify
the uniform-pushforward step used in the proof of Theorem 5.6 of
[Briaud et al., v1](https://arxiv.org/html/2509.07276v1). For example,
projection onto the first bit maps V={000,001,010,100} onto F_2, but a
uniform V sample has first bit 1 with probability 1/4, not 1/2. This
identifies a missing implication in that displayed argument, not a
counterexample to its conclusion for its actual code ensemble. The exact
native success calculation above does not assume a uniform image: it
counts each information-set assignment and uses the independently
proved native fiber count.

Use unnormalized local weight w_i(x_i)=1+(M-1)1_{f(x_i)=b_i}, M>=1.
Expand the full weight by a latent set S of active constraints:

    prod_i w_i = sum_(S subset [N]) (M-1)^|S| 1_{f_S=b_S}.

If |S|<=N-K, the projection of C onto S is surjective (MDS). Therefore
the fraction of C satisfying the active predicates is EXACTLY 2^-|S|.
Moreover this conditional uniform distribution is efficiently samplable:
extend S to an information set of size N-K; sample accepted values on S,
unrestricted values on the other information positions, and solve pivots.
This preserves the actual code, targets, field and zero convention.

For arbitrary S, the same character expansion as the repository's fiber
bound gives the accepted fraction

    2^-|S| (1+e_S),  |e_S|<=eta.

Indeed sum out coordinates outside S: only dual codewords supported inside
S survive. Their weighted enumerator is a sub-sum of the full positive
enumerator. This is uniform over S, including S=[N].

Let p=(M-1)/(M+1), r0=N-K, and

    tau=Pr[Bin(N,p)>r0].

Draw S as independent Bernoulli(p) membership, CONDITIONED on |S|<=r0,
then use the efficient conditional sampler above. This is the exact Gibbs
mixture with its unmanageable latent sets removed. The discarded joint
mass is at most (1+eta)tau/(1-eta), so its output law nu satisfies

    TV(nu, pi_M) <= min(1, (1+eta)tau/(1-eta)).

For fixed K/N=R and p<1-R by a fixed margin, tau is exponentially small
by a binomial tail bound; the algorithm is polynomial. At R=1/8 this covers
any fixed M<15. Sampling the truncated binomial and a uniform subset can be
done by rational/integer arithmetic at rational M. Alternatively reject
untruncated draws of S; the expected number is 1/(1-tau), and a fixed cap
adds its abort probability. No Markov-chain mixing argument is needed.

This is a native specialization of the established latent-constraint /
Prange mixture idea. Its derivation here uses the nonlinear root sampler
and exact MDS projection counts. See the primary-paper comparison in
`LITERATURE.md` when completed.

## 3. Why this sampler does not yet give fast full-witness search

For a particular feasible S of size s, native success is

    |A_b|/(|C| 2^-s)=(1+e_b)2^(-(N-s)).

Thus ANY distribution over independently selected feasible latent sets
(with exact uniform sampling conditional on that set) succeeds with at most
(1+eta)2^-K. Choosing s=N-K attains that bound. This statement allows all
distributions on S, but excludes adaptive nonuniform conditional samplers.

There is an apparent trap: the ideal pi_M solution mass is about
(M/(M+1))^N, which can be larger than 2^-K even at M just below 15.
This does not contradict the TV approximation. The exponentially small
discarded latent mass can contain most of an exponentially rare event.
Exponential TV accuracy is not automatically sufficient *relative* accuracy
for an exponentially rare witness. A full solver needs constant success,
not just approximate moderate-temperature sampling.

At the proposed search temperature M>=N, p=1-O(1/N), so |S| is typically
N-O(1)>N-K. The direct mixture cannot cheaply sample its typical component.
Rejecting to |S|<=N-K is superpolynomially rare, but that rejection is NOT
necessary to sample the truncated law nu: direct truncated-binomial sampling
remains polynomial even here. The failure is that nu no longer approximates
the required low-temperature law. A state-dependent choice,
nonuniform conditional root sampler, or a larger efficiently solvable
constraint family could improve this; none is ruled out here.

Strongest falsifier / next question: produce a polynomial method for the
conditional native relation when a typical active set contains N-O(1)
constraints, or show a constructive annealing/transport step that reaches
pi_N without solving those conditionals. A slow local heat bath does not
settle either possibility.

## 4. Exact hitting probability, and correction of a runtime trap

A later shared note correctly called attention to the direct-truncation
distinction above. Independently, for integer M>=1 the weights

    w_s=binom(N,s)*(M-1)^s*2^(N-s),  0<=s<=N-K,

have O(N log(M+1)) bits. Compute their sum, draw s from these integer
weights, and then draw a uniform s-subset. This samples the conditional
latent law directly in expected polynomial time for EVERY M with
polynomial input bit length. Rational M works after clearing denominators.
The earlier rare-rejection observation is a property of that rejection
implementation, not an intrinsic cost of the truncated distribution.

There is also an exact native first-hitting calculation. Define

    B_M=Pr[Bin(N,(M-1)/(M+1))<=N-K],
    A_M=Pr[Bin(N,(M-1)/M)<=N-K],
    lambda_b=1+e_b.

Exponential tilting of the finite binomial sum gives

    p_nu = Pr_nu[native witness]
         = lambda_b*(M/(M+1))^N*A_M/B_M.             (2)

Thus independent fresh trials have exactly geometric first-hitting time
of mean 1/p_nu. This is a constructive first-hitting theorem for this
sampler, NOT for the local Gibbs chain. Since the active-set size is at
most N-K, p_nu<=lambda_b*2^-K; as M tends to infinity it approaches that
systematic-root value. Monotone likelihood ratio in s shows that increasing
M increases p_nu, but cannot exceed this limit.

Write Lambda_M for the true Gibbs partition function relative to
|C|*((M+1)/2)^N. Uniform fiber estimates give 1-eta<=Lambda_M<=1+eta.
The ratio of (2) to the true Gibbs witness probability is exactly

    Pr_nu[A_b]/Pr_pi_M[A_b] = Lambda_M*A_M/B_M.

At fixed R=1/8 and 8<M<15, A_M is exponentially small while B_M tends to
one. Consequently the polynomial sampler has exponentially small relative
witness probability even though its TOTAL VARIATION error is exponentially
small. This identifies the precise rare-event failure, rather than relying
only on the looser 2^-K success cap.

Self-attack: neither the direct truncated sampler nor (2) uses an assumed
conditional sampler beyond an information set. The binomial-tail statement
alone would not establish runtime or relative witness accuracy; the paid
integer sampling and exact tilted ratio supply those missing distinctions.

## 5. Paying for a few extra active constraints does not remove the gap

For a fixed S of size N-K+r, first uniformly condition on any N-K members
of S and reject unless the remaining r predicates pass. Let
lambda_S=2^|S|*Pr_C[f_S=b_S]. Then the rejection probability of acceptance
is lambda_S*2^-r, and the accepted conditional draw has native success

    (lambda_b/lambda_S)*2^(-(K-r)).

Their product is exactly lambda_b*2^-K. In particular r=O(log N) gives a
polynomial conditional sampler beyond the information-set size, but this
particular extra conditioning does not improve total native hitting cost.
Near-complete sets require r close to K and exponential rejection work.
This is a statement about the explicit rejection construction; a genuinely
new adaptive conditional solver could bypass it. That is still the decisive
unresolved classical obligation.
