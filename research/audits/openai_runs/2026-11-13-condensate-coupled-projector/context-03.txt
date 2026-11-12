# 2026-11-13 — Independent condensate spectral and paired-growth audit

**Accepted:** ideal uniform-permutation qRSt has exactly the native condensate
spectral law; exact rational local probabilities give a deterministic
poly(D,b) BIT clock to joint-path TV error 2^(-b). Return amplitude and
probability have polynomial classical additive-error estimators. The up-path
kernel is correct. After the later paired-tableau construction is included,
the normalized mode-1 mean and ALL normalized mode-1 factorial moments are
also classically estimable with polynomial additive-error cost, even for
growing moment order.

**Repaired:** a monotone k-annihilator correlator contains sqrt((D)_k).
Only its NORMALIZED version has the claimed uniformly bounded estimator
for growing k. The unnormalized all-k polynomial estimator asserted in
the Claude report does not follow. Also, its missing mode-1 pair interface
is now paid in the AVERAGED joint law below; a conditioner on an arbitrary
supplied shape is not provided.

**Open:** the full mode-1 distribution/sampler, full occupation sampling,
relative accuracy for tiny probabilities, and efficient contraction of the
alternating moment formulas. No novelty, speedup or general lower bound is
inferred. Estimation costs poly(1/epsilon), not poly(log(1/epsilon)).

Read: current STATE/TRAPS and MACDONALD_CONDENSATE_CLASSICAL; the terminal
252-line Claude spectral report; after the parent's update, the material
paired-growth and variance sections of the terminal OpenAI coherent report.
Checked against the COMPLETE actual Aigner–Frieden source: Definitions 2.6,
4.24, 4.28; Theorem 3.3; Proposition 4.17 and its proof; normalization proofs
in §4.5; and all of Theorem 4.25/Lemma 4.26. Local file has 2811 LF lines.
No network, API, Git, implementation or sweep was used.

## 1. The full source proof and the native positive specialization

Set N=D+1, t=D/N, q=t^3, D>=1. Keep these GLOBAL parameters at every smaller
degree; D=0 is the trivial vacuum case. Source [i,j] means 1-q^i t^j.
For a partition lambda, its positive boundary runs h_i,v_i satisfy
sum h_i<=D and sum v_i<=D. Proposition 4.17 rewrites every forward and
backward corner probability as a monomial times O(D) ratios of [i,j],
where i,j>=0 and i+j>0. This remains true in the shifted factors [i,j]^±.
For example [0,v_r]^+=[1,v_r-1] and [h_r,0]^-=[h_r-1,1] are nonzero,
including the endpoint cases v_r=1 or h_r=1.

The omitted beta details in that proof can be checked directly. Removing
one cell changes a to a-1 along its old row and l to l-1 along its old
column. Thus, with arms/legs evaluated in lambda,

    beta = product_R [a,l+1]/[a-1,l+1]
           * product_C [a+1,l]/[a+1,l-1],
    beta_bar = product_R [a+1,l]/[a,l]
               * product_C [a,l+1]/[a,l].

These are exactly the reciprocal alpha definitions. Grouping successive
cells by boundary runs telescopes them to the four beta products of
Proposition 4.17. The adjacent run contributes
[0,v_r]^+[h_r,0]^- / ([0,1]^+[1,0]^-) in the first case, and
[0,v_r][h_r,0]/([0,1][1,0]) in the second. The alpha/alpha_bar formulas
follow by the same row/column telescoping when adding a cell.

The potentially negative exponents in the ORIGINAL gamma formula must
not be used as a positivity argument. Directly from source LF 1507–1510:
if r<=s, put H=h_(r,s)>=1,V=v_(r+1,s)>=0; then gamma is
[H,V][H-1,V+1]/([1,0][0,1]). If r>s, put H=h_(s+1,r-1)>=0,
V=v_(s+1,r)>=1. Then

    gamma=q^(-1-2H)t^(1-2V)
                   [H,V][H+1,V-1]/([1,0][0,1]).

Combining the latter monomial with Definition 4.13 gives the NONNEGATIVE
prefactor q^(1+2H)t^(V-1). The other case gives t^V. This verifies the
source gamma rewrite and the endpoint signs without a spectral-gap claim.

At q=t^3, every bracket becomes 1-t^e with positive e<=8N; the prefactor
is t^E with 0<=E<=8N. All are finite positive rationals. The local identities
sum_s p_(r,s)=1 and sum_r pbar_(r,s)=1 follow from the actual §4.5 Lagrange
interpolation proofs. Those are rational-function identities; the positive
finite-factor expressions permit specialization without any pole. No
assumption about distinct global Lax eigenvalues is involved.

The COMPLETE Lemma 4.26 proves growth-wise compatibility by moving a
northeast-to-southwest lattice path across one cell. All four cases check:
(1) an empty unchanged cell contributes one; (2) a union/intersection cell
has equal edge-weight ratios by row/column cancellation (source (3.10));
(3) an unmarked collision uses local compatibility for a removed corner;
(4) a marked cell contributes precisely (1-t)/(1-q)=1/r1. At the final
boundary there are D marked cells, and the edge weights are psi_P phi_Q.
Thus

    r1^(-D) Prob_forward(growth)
       = Prob_backward(growth) psi_P phi_Q.

Theorem 4.25 sums this identity. Both forward and backward growth procedures
are normalized because every local distribution is normalized; the backward
procedure recovers a permutation, as in source Definition 2.6. This fills
the missing cases in the paid extract. The right boundary is P and the
bottom boundary is Q (source LF 582–586).

## 2. Exact spectral law, with all factorial and norm factors

Let h_lambda=<P_lambda,P_lambda>, b_lambda=1/h_lambda, and
kappa_lambda=[p1^D]P_lambda. Source Theorem 3.3 and Q_lambda=b_lambda P_lambda
give

    sum_(P in SYT(lambda)) psi_P = D! kappa_lambda,
    sum_(Q in SYT(lambda)) phi_Q = b_lambda D! kappa_lambda.

Indeed only p1^D can contain the squarefree monomial x1...xD, and its
coefficient is D!; squarefree semistandard fillings are standard tableaux.
The one-cell factors are positive, so kappa_lambda>0 for every shape.

The weighted permutation side of Theorem 4.25 has constant weight r1^(-D).
For a UNIFORM permutation, its output pair law is therefore exactly

    Prob(P,Q)=r1^D psi_P phi_Q / D!.

Summing over shapes gives

    pi_D(lambda)=D! r1^D kappa_lambda^2 / h_lambda.                 (1)

The native normalized condensate is chi_D=p1^D/sqrt(D! r1^D), and the
positive normalized eigenvector is |lambda>=P_lambda/sqrt(h_lambda).
Their overlap is sqrt(D! r1^D/h_lambda) kappa_lambda. Squaring proves that
(1) is exactly the spectral law in the native Hall-Fock contract. It is
not the real-time occupation law. No sum over tableaux is computed by the
algorithm; those sums are used only in this proof.

## 3. Exact rational local probabilities and a finite BIT/TV clock

Draw a uniform permutation conceptually, and run the source D-by-D growth
algorithm. At each cell the northeast/southwest shapes either differ
(deterministic union), all three old shapes coincide with no mark (copy),
coincide with a mark (r=0 corner distribution), or coincide one box above
the northwest shape (r>0 distribution). These are all source growth types.
Every shape has size <=D. There are at most D^2 stochastic cells, each
with at most D+1 choices, and polynomial-time shape/rank bookkeeping.

Use EXACT rationals for local probabilities and CDFs. Each t^e or 1-t^e
has O(D log N) numerator/denominator bits for the exponents of §1. Each
probability uses O(D) factors, so its bit length is O(D^2 log N). Adding
at most D+1 probabilities gives CDFs of O(D^3 log N) bits, for example by
using the product of their denominators. Reduced exact rational arithmetic
also has that bound. There is no numerical zero test or small-denominator
conditioning problem. No product of probabilities over a whole growth is
required by the sampler.

Fisher–Yates draws the permutation with at most D categorical choices.
For each categorical choice, use a fresh B-bit integer U and compare
U/2^B with the exact rational CDF; skip zero intervals. Coupling to a
continuous uniform, a categorical distribution with at most N outcomes
changes with probability at most N*2^(-B). These are uniform CONDITIONAL
bounds, so they add over adaptive histories.

The paired extension in §6 uses at most 3D^2+3D such choices, including
permutation generation and insertion ranks. A single conservative choice

    B=b+ceil(log2(64N^4))

therefore gives joint-path TV error <=6N^3*2^(-B)<2^(-b). It also covers
the simpler spectral-only sampler. All loops have fixed polynomial bounds,
and all integer arithmetic has polynomial bit length in D and b. Hence
this is a deterministic poly(D,b) runtime bound for a randomized sampler,
not an uncharged exact rational coin or an unbounded rejection algorithm.
The ideal kernel is exact; the finite fair-bit implementation has the
stated TV tolerance. No tight exponent such as O(D^3 W^2) is adopted.

## 4. Return amplitude and probability: additive guarantees

With the admitted exact rational native eigenvalues E_lambda and time
2pi*tau, tau=a/c,

    A(tau)=<chi_D|exp(-2pi i tau H)|chi_D>
          =E_(lambda~pi_D) exp(-2pi i tau E_lambda).

Compute tau E_lambda modulo 1 EXACTLY before evaluating the phase. The
established common denominator D^(3D)N^D and binary time length L give a
polynomial BIT clock; numerical |tau| does not enter. Approximate the phase
to absolute error epsilon/64, and sample pi_D to TV epsilon/64. The complex
expectation bias is at most 3epsilon/64.

For 0<epsilon<1, average at least

    ceil(512 epsilon^(-2) log(4/delta))

independent trials. Hoeffding applied to real and imaginary parts (even
using the loose component range [-2,2]) gives amplitude error <=epsilon
with probability >=1-delta. Thus the cost is
poly(D,L,epsilon^(-1),log(delta^(-1))). Estimate A to epsilon/4 and output
clip(|Ahat|^2,0,1) for an additive-epsilon return-probability estimate.
The return probability is exactly the output event nu=(1^D).
This is additive estimation; relative error for an exponentially small
return probability is not paid.

## 5. The up chain and the normalized monotone-correlator repair

All degree-n quantities here retain the original global q,t. The marginal
of the recording tableau T, with final shape lambda of size n, is

    Prob(Q=T)=r1^n kappa_lambda phi_T.

The positive kernel

    K_n(eta,lambda)=r1 phi_(lambda/eta) kappa_lambda/kappa_eta       (2)

is stochastic. One can verify its normalization without another source:
Theorem 3.3's one-variable branching gives
partial_(p1) P_lambda=sum_(eta<lambda) psi_(lambda/eta)P_eta.
Adjointness and phi=(b_lambda/b_eta)psi give
p1 P_eta=r1 sum_lambda phi_(lambda/eta)P_lambda. Taking its p1^(n+1)
coefficient proves that the terms in (2) sum to one. Products of K telescope
to the displayed recording-tableau law, so the bottom boundary is exactly
this Markov growth chain. Its degree-n marginal is pi_n. Formula (2) is an
IDENTITY, not an oracle for computing kappa ratios.

Put c_n(lambda)=sqrt(n! r1^n/h_lambda) kappa_lambda and
 a1=sqrt(r1) partial_(p1). Its positive one-box matrix is

    A_(eta,lambda)=sqrt(r1) psi_(lambda/eta)
                                sqrt(h_eta/h_lambda).

Direct substitution gives

    A_(eta,lambda)c_(n+1)(lambda)
       =sqrt(n+1)c_n(eta) K_n(eta,lambda).                       (3)

For k annihilations separated by rational times 2pi*tau_0,...,2pi*tau_k,
telescoping (3) yields the exact monotone correlator

    G_k = sqrt((D)_k) E_path
            exp(-2pi i sum_(j=0)^k tau_j E_(lambda^(D-j))).       (4)

The bra and ket are the normalized condensates chi_(D-k), chi_D, and the
path is the qRSt growth from degree 0 to D. Compute the SUM of rational
phase arguments modulo one and then one exponential. The normalized
G_k/sqrt((D)_k) is bounded by one and has the same polynomial additive-error
estimator for all 0<=k<=D (charging the total binary time description).
For UNNORMALIZED additive error epsilon, this estimator instead requires
accuracy epsilon/sqrt((D)_k), giving a sufficient sample count of order
(D)_k/epsilon^2. This is not polynomial uniformly in growing k. The Claude
report's unnormalized all-k claim is rejected at that scope; no impossibility
of other unnormalized estimators is asserted.

## 6. The new paired-extension repair really pays normalized mode-1 moments

For standard tableaux of a fixed shape eta, phi_T=b_eta psi_T. The exact
PAIR law of §2 therefore gives conditional independence:

    Prob(P,Q | eta)=
       [psi_P/(n! kappa_eta)] [psi_Q/(n! kappa_eta)].             (5)

This is the missing resource: qRSt supplies TWO appropriately distributed
tableaux sharing a random eta~pi_n, with no conditioning/rejection step.

Actual source Definition 4.28, LF 1897–1907, defines insertion using only
the current partial tableau, the new entry, and fresh local corner coins.
The paragraph LF 1931–1935 identifies this with the preceding growth law.
A uniform permutation can be extended uniformly: choose a fresh rank
R in {1,...,n+1}, raise each old label >=R by one, and append R. This is a
bijection from a size-n permutation and rank to a size-(n+1) permutation.
Order relabeling preserves the relevant nested subtableau shapes and hence
the qRSt insertion law. No old growth history is needed.

Consequently, starting with a psi-weighted insertion tableau conditional
on eta and doing independent uniform-rank insertions realizes the shape
kernel K, after averaging over that tableau. More formally, under uniform
permutations the conditional insertion tableau given the entire recording
path is psi-weighted on its terminal shape by the factorized pair law.
Together with insertion locality, this identifies every next-step kernel
and its successive iterations. It is valid even when the initial tableau
happens to be a recording tableau Q: by (5) its conditional law is identical.

For a specified j in {0,...,D}, let n=D-j. Run qRSt at size n using GLOBAL
q,t, obtaining (P,Q,eta). Independently extend P and Q to size D by the
rank-insertion procedure, with separate randomness. Their final shapes
lambda,rho have the exact law

    pi_n(eta) K_(n:D)(eta,lambda) K_(n:D)(eta,rho).              (6)

Each insertion bumps strictly increasing entries, so uses at most D local
choices. Thus §3's joint BIT/TV bound applies. Approximate conditional
independence need not be proved after conditioning on rare eta: a single
coupling bounds the complete joint law (6). This construction does not
supply a conditioner on an arbitrary externally specified eta.

Let Psi_tau=exp(-2pi i tau H)chi_D and N1=a1^dagger a1. Iterating (3) without
intermediate phases gives

    (a1^j Psi_tau)_eta = sqrt((D)_j)c_n(eta)
                  sum_lambda K_(n:D)(eta,lambda) exp(-2pi i tau E_lambda).

Since (a1^dagger)^j a1^j=(N1)_j, squaring the norm and using (6) proves

    s_j := <(N1)_j>_tau/(D)_j
         = E cos(2pi*tau*(E_lambda-E_rho)).                    (7)

The observable is bounded in [-1,1], while its expectation lies in [0,1].
The same finite sampling/phase/averaging budgets therefore estimate every
s_j in poly(D,L,epsilon^(-1),log(delta^(-1))) BIT time, uniformly for j<=D.
In particular j=1 pays additive estimation of <N1>/D; j=0 is 1; j=D is
|A|^2. This CORRECTS the earlier Claude report's assertion that even the
mode-1 additive mean lacked the necessary averaged pair sampler.

## 7. What remains unpaid

Bounded estimators for normalized factorial moments do not provide a
polynomial-b accuracy sampler for N1. The exact inversion is

    Prob(N1=m)=binom(D,m) sum_(r=0)^(D-m)
                               (-1)^r binom(D-m,r) s_(m+r).

The new report's second-moment calculation is correct ONLY at its stated
estimator scope. If one samples a single index j with full-support law w
and returns Y=(-1)^j binom(D,j) W_j/w_j, where |W_j|=1 is the raw paired
phase, then

    E|Y|^2=sum_j binom(D,j)^2/w_j >=4^D.

Equality holds for w_j=binom(D,j)/2^D. This does not constrain coupled or
analytically contracted estimators, and is not a lower bound on a classical
mode-1 or full-occupation sampler. At zero time the cancellation is known
analytically. Generic conditioning after an occupation prefix also changes
the state away from the unconditioned condensate representation above.
No paid positive contraction or full conditional-output sampler is supplied.
The remaining mode-1 law and full occupation target therefore stay OPEN.
