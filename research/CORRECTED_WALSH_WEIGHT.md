# Corrected Walsh Output: A Large-Copy Bound

Status: **derived, review pending; finite identities independently cross-checked;
no formal verification or novelty established**. This is not a new algorithm.

The prior fixed-parity/Fourier-envelope argument did not cover corrected
majority. This analysis uses the actual corrected output distribution instead
of its Boolean Fourier norm. It applies to EVERY decision on those corrected
bits, but only after the source labels have been discarded. It also leaves
an intermediate copy-count window unresolved.

## Program and Scope

Start with k standard mixed coset states, either null or for one shared
H={e,h}, where h is uniform in an involution conjugacy class of size M.
Use G=S_n, D=|G|. Fix one central reflection

    U = sum_lambda phi_lambda P_lambda = sum_g a_g R_g,
    phi_lambda in {-1,+1}.

Its real coefficients satisfy a_g=a_(g^-1), sum_g a_g^2=1. They are constant
on conjugacy classes. The phase rule can depend on n and the promised hidden
cycle type, not the observed source tuple or hidden member. The implemented
algorithmic readout uses the existing negative-character reflection; a
zero-character reflection provides a separate check.

Measure each source irrep lambda_i, perform the uniform full-subset-mask
query U_S, measure the mask register in the Walsh basis, and set

    z_i = y_i xor 1[phi_lambda_i=-1].

Discard the original source labels and physical inputs. Retaining a source
count, selecting positions from sources, or using sources again in the final
decision is NOT this program. Neither are complex phases, nonuniform mask
amplitudes, multiple queries, or subset-dependent phase rules. Ideal primitive
access is assumed; approximate implementations need their separate channel
error allowance. This does not supply a gate-level QFT backend.

## Exact Weight Law

Put b_g=a_(hg), c_h(g)=a_g+b_g, c_0(g)=a_g. Define J_h(g)=1[g in H] and
J_0(g)=1[g=e]. For each hypothesis eta=0 or h,

    alpha_eta(u,v) = [1+J_eta(u^-1 v)+c_eta(u^-1)+c_eta(v)]/4,
    beta_eta(u,v)  = [1+J_eta(u^-1 v)-c_eta(u^-1)-c_eta(v)]/4.

The complete weight law is

    P_eta(w) = binomial(k,w) sum_(u,v) a_u a_v
                  alpha_eta(u,v)^(k-w) beta_eta(u,v)^w.

To derive this, sum the naturally weighted source/bit factors in
[Source-Selected Parity](SOURCE_SELECTED_PARITY.md) after applying the
matching phase correction. Regular-character orthogonality gives the J
terms; the signed character sum gives c_eta. Take the product across copies
only AFTER this local source sum. The same h is used throughout.

The probability of an ordered bit string depends only on its weight.
Conditional on weight, all strings are uniform under either hypothesis.
Therefore full corrected-string total variation equals weight-law total
variation; an arbitrary bit classifier cannot exceed the latter. The joint
distribution with the discarded source tuple need not have this property.

Individual group-pair weights and local factors can have signs. They are
not probabilities. The implementation groups equal integer (alpha,beta)
numerators and evaluates every binomial coefficient with arbitrary-precision
integers and exact fractions. Positivity and normalization are checked after
the FULL signed contraction, never imposed by clipping.

## Positive Comparison Mixture

Keep only group pairs satisfying u^-1 v in H_eta. For the null this means
u=v and produces

    Q_0 = sum_g a_g^2 Bin(k,(1-a_g)/2).

For the alternative, pairing g with gh gives

    Q_h = (1/2) sum_g (a_g+b_g)^2 Bin(k,(1-a_g-b_g)/2).

Unitarity gives sum_g a_g b_g=0. Also a_g+b_g is constant on right H-cosets,
and sum_g (a_g+b_g)^2=2. Thus these really are normalized positive mixtures
with parameters in [0,1]. No renormalization of selected events is involved.

They are NOT the full finite-k laws. The omitted group-pair terms can have
substantial total variation. At S6,k=1 the actual corrected law is the same
point mass under both hypotheses, while the comparison mixtures differ
from that law. This is a regression test, not a proposed algorithm.

### Off-Coset Error

For a pair outside H_eta, alpha+beta=1/2 and

    |alpha|+|beta| = max(1,|c_eta(u^-1)+c_eta(v)|)/2.

The two c values belong to distinct H_eta-cosets. The squared c values sum
to one over cosets, so Bessel/Cauchy-Schwarz gives a uniform radius at most
1/sqrt(2). This alone yields TV(P_eta,Q_eta)<=D*2^(-k/2)/2.

A sharper split matters for the intended k=O(n log n) budget. Let every
nonidentity conjugacy class have size at least L>=16. Centrality and
sum_g a_g^2=1 imply |a_g|<=1/sqrt(L) for g!=e. If both u and v lie outside
H_eta, each |c_eta|<=2/sqrt(L); the radius is then at most 1/2. If one lies
inside H_eta, the radius is at most 1/2+1/sqrt(L). The sum of absolute pair
weights touching H_eta is at most

    2 (sum_(u in H_eta) |a_u|) ||a||_1 <= 4 sqrt(D).

For either hypothesis this gives

    TV(P_eta,Q_eta) <= (1/2)[D*2^-k
                          +4 sqrt(D)(1/2+1/sqrt(L))^k].

This bounds the whole law, not only one moment. The finite implementation
also computes a tighter exact triangle bound from the actual off-coset
radius spectrum, and checks the measured mixture error against it.

## Central-Amplitude Overlap

Let f(g)=a_g^2, a central probability distribution, and define

    O(h) = sum_g f(g) f(hg).

This is nonnegative, constant on the class of h, and sum_h O(h)=1.
Consequently O(h)<=1/M. Cauchy-Schwarz also gives

    S(h)=sum_g a_g^2 |b_g| <= sqrt(O(h)) <= 1/sqrt(M).

For any acceptance function of a binomial observation, write
F(x)=E[accept | Bin(k,(1-x)/2)]. Coupling k Bernoulli trials gives the
uniform Lipschitz bound |F(x)-F(y)|<=k|x-y|/2 on [-1,1].

The mixture acceptance difference is

    Delta = sum_g a_g b_g F(a_g+b_g)
          + sum_g a_g^2 [F(a_g+b_g)-F(a_g)].

Use sum_g a_g b_g=0 to subtract F(0) in the first term. Swapping g and hg
interchanges a and b. The absolute first term is at most k*S(h), and the
second at most k*S(h)/2. Taking the supremum over every acceptance function
therefore proves

    TV(Q_0,Q_h) <= 3k/(2 sqrt(M)).

The derivation uses no conditioned-cell mixing lemma, Fourier l1 bound for
the classifier, or approximation to a threshold by a low-degree polynomial.
Centrality is essential to the POINTWISE class-overlap step: a noncentral
real unitary on a Klein four subgroup of S6 gives O(h)=1/4>1/15 for one
fixed-point-free h. A test verifies that unitary exactly. This does not
refute a separately averaged overlap inequality for noncentral functions.

## Combined Bound and Remaining Window

For even n>=16, use L=n and M=(n-1)!!. Combining the two approximation errors
with the overlap estimate gives

    TV(P_0,P_h) <= min(1,
        3k/(2 sqrt(M)) + D*2^-k
        +4 sqrt(D)(1/2+1/sqrt(n))^k).

The elementary class-size bound L=n can be checked without character-ratio
estimates. A nonidentity permutation with support s<n has at least
binomial(n,s)>=n conjugates. For full support, let r<=n/2 be its cycle count
and m_j its cycle multiplicities. Its centralizer size is
product_j j^m_j*m_j! <= 2^(n-r)*r! <= 2^(n/2)*(n/2)!, using
j<=2^(j-1) and the monotonicity of 2^(n-r)*r! for r>=1. Thus its class has
size at least M>=n in the stated range.

Also take the minimum with the existing raw-copy information bound
sqrt((2^k-1)/(4M)). All finite numerical bounds use outward integer dyadic
rounding. Replacing sqrt(n) by floor(sqrt(n)) in the denominator increases
the exceptional radius; no floating underflow enters the certificate.

For fixed epsilon>0, k>=(1+epsilon)log_2 D and polynomial k, every displayed
term is superpolynomially small in n. Small k<=(1-epsilon)log_2 M is handled
by the raw-copy bound. These regimes DO NOT meet: roughly log_2 M through
log_2 D remains unresolved, as do parameter choices arbitrarily near their
endpoints. An inverse-polynomial upper bound alone would not exclude
polynomial repetition, so it must not be called a speedup obstruction.

Here k counts the copies ACTUALLY participating in the uniform mask, not
an available resource budget. An algorithm may discard surplus inputs and
run a smaller instance in the unresolved window. The large-k result does
not rule out that strategy or say that having extra copies is harmful in
general; it bounds this particular all-k measurement.

At S1024 the actual contract reports:

| Copies | Bound TV<=2^b | Interpretation |
| --- | ---: | --- |
| 2191 | b=-1096 | Small raw-copy bound |
| 4382 | b=0 | Unresolved by these bounds |
| 8764 | b=0 | Unresolved by these bounds |
| 17528 | b=-2174 | Full corrected-output large-copy bound |

This last statement covers majority, all-zero, fitted weight tables and
every other decision on the corrected bits, regardless of Fourier norm.
It does not cover looking at the discarded sources again.

## Finite Findings and Verification

S6's full corrected-weight Bayes distance rises from 0.028889 at k=2 to
0.265489 at k=128, but loses to the cheaper pair-event-count baseline at
every tested k in {2,4,8,16,32,64,128}. At k=128 that baseline has distance
0.846834; declared corrected majority has signed gap only 0.007046.
The implementation also records the best threshold chosen AFTER seeing
the laws, explicitly as exploratory rather than a compiled algorithm.

Twenty-four full S3/S4 weight distributions agree with matrix-derived
source/bit histograms, for two real reflections and k=1,2,3. Forty-eight
exact diagonal-mixture laws and 42 exact all-hidden-member kernel covariance
checks include S6. Tests additionally enumerate all 40 real central irrep
phase assignments of S3/S4, including negative trivial phases, and check
their normalized laws, overlap identities and off-coset Bessel radii.

Primary scope references remain [Hallgren, Roetteler and Sen](https://arxiv.org/abs/quant-ph/0511148)
for joint-coset measurement requirements and [Moore, Russell and Sniady](https://arxiv.org/abs/quant-ph/0612089)
for their specified sieve model. Their abstracts do not certify this
particular program reduction or establish its novelty. Independent review,
comparison with full prior proofs, and the intermediate window remain work.

## Next Discriminating Experiment

Do not retry corrected majority at the already obstructed large-copy budget.
The cheapest untested extension retains the NUMBER of negative source labels
alongside corrected Hamming weight. This preserves source/output correlations
that the current mixture argument discards, while leaving a small classical
output alphabet. Compute the JOINT natural-weight law before judging it;
the source marginal alone is not an information bound. Alternatively tighten
the intermediate-copy remainder, or change the quantum measurement itself.

Reproduce through `python qsearch.py run EXP-COSET-BINARY-CARRIER-INSTRUMENTS`,
then `dequantize`, `proofs`, and `validate`. No candidate is promoted.
