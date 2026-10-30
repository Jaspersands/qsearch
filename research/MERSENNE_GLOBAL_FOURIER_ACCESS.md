# Mersenne Global Fourier Access

2026-10-29. **WRITTEN IMPLICATION INDEPENDENTLY REVIEWED; NOT IMPLEMENTED.**
The parent reports that Heisenberg found no fatal error in the list-sampler,
error-budget, and theorem-scope deduction. This is automated mathematical
review, not formal verification, human peer review, or an implementation claim.

Exact signed Walsh queries plus approximate local sampling and complete
classical list decoding give APPROXIMATE classical sampling of the Born law
after complete-list amplitude summation, BEFORE the final Fourier transform.
They do not yet solve native search or native uniform sampling.

## 1. Exact Input And Dependencies

Keep the SAME [native Mersenne relation](MERSENNE_RECIPROCAL_RESEARCH_TARGET.md):

    n odd prime >=17; q=2^n; N=n^2; K=floor(N/8)=(N-1)/8;
    s=floor((n-3)/4); r=n-4s in {3,5}; d=2^s-1;
    f_s(x)=Tr(inv0(x)^d), with inv0(0)=0;
    H[j,i]=alpha_i^j, 0<=j<K;
    C=ker H; D=rowspan H=C^perp; M_D=|D|=q^K;
    Omega_b={x in C : f_s(x_i)=b_i for every i}.

Input: a checked public irreducible degree-n binary modulus, N distinct
public field points alpha_i, and arbitrary target bits b_i. The dual and
normalized additive Fourier transform F use Tr(sum_i x_i z_i).
All input validation, field arithmetic, random bits, queries, and decoding
are charged. No field table, planted witness, or favorable-input promise
is supplied. Finding a witness and sampling uniformly from Omega_b remain
different tasks.

Dependencies are the [written carry evaluator](MERSENNE_CARRY_WALSH_DRAFT.md),
the [local access audit, Section 2](MERSENNE_CLASSICAL_ACCESS_AUDIT.md#2-genuine-polynomial-differential-access-with-a-boundary),
the [Mersenne fiber bound](MERSENNE_RECIPROCAL_RESEARCH_TARGET.md#5-conditional-paid-quantum-guarantee),
and the [complete classical decoder](BINARY_GS_DECODER.md).
Walsh calls must return exact signed integers W(u), costing conservatively
O(n^45) time and O(n^21) bits of workspace. A low-precision residue is
insufficient. An implementation WORK_CAP is not probability-bounded ABORT.

## 2. Signed Source, Native Cutoff, And Decoder

The Fourier amplitude of the normalized uniform local accepted set is

    a_b(u)=(q*[u=0]+(-1)^b*W(u))/(sqrt(2)*q),
    W(u)=sum_x (-1)^(f_s(x)+Tr(u*x)),
    pi(u)=W(u)^2/q^2,  pi(0)=0,  sum_u pi(u)=1.

Its measured law is (1/2)*[u=0]+(1/2)*pi(u), independent of b.
Its signed amplitude is NOT independent of b. Define

    a_bold(e)=product_i a_(b_i)(e_i),
    w=floor(3N/5),  g(e)=[wt(e)<=w]*a_bold(e),
    tau=||g||^2=2^-N*sum_(j<=w) binom(N,j) >=1/2.

Weight counts nonzero FIELD symbols. Before truncation the support pattern
is N independent fair bits; conditional on a pattern, active labels are
independent with law pi. Thus uniform support masks conditioned on weight
<=w, followed by exact pi labels, would sample |g|^2/tau.

Decode D=RS[N,K] on the original points at radius w. Put

    a=N-w=ceil(2N/5),  J_gap=a^2-N*(K-1)>0,
    L=floor(N*(a-K+1)/J_gap)<=7,  P=8.

The [pairwise-agreement proof](BALANCED_CODEWORD_FILTER.md#3-a-paid-finite-list-decoder-interface)
bounds every complete radius-w list by L. The ratio decreases with a and
increases with K-1 here; substituting a>=2N/5 and K-1<=N/8 bounds it by
55/7<8. P is fixed publicly, not chosen from the received list size.

| n | N | K | w | L | P |
|---|---|---|---|---|---|
| 17 | 289 | 36 | 173 | 7 | 8 |
| 31 | 961 | 120 | 576 | 7 | 8 |
| 61 | 3721 | 465 | 2232 | 7 | 8 |

A list bound alone is not an algorithm. [BINARY_GS_DECODER.md, Sections 1-3](BINARY_GS_DECODER.md#1-all-linear-roots-without-field-enumeration)
supplies deterministic complete decoding: Guruswami-Sudan interpolation,
Roth-Ruckenstein extraction, and exact distance filtering. Multiplicity 4
and weighted degree 4a-1 suffice: Y-degrees 0..12 alone give
52a-78(K-1)>10N monomials against 10N constraints. Total Y-degree is <=13.
Dense interpolation costs O(N^3) field operations and O(N^2) field storage.
The extraction tree has <=1+K*deg_Y(Q) nodes. Base-field roots use
gcd(Y^q-Y,h) and public-basis trace cuts, without field enumeration.
A conservative bit bound is O(N^3*n^3), with polynomial storage.
This charges an actual complete decoder, not a unique-decoding heuristic
or a claim that native-size decoder/sampler execution has occurred.

## 3. Exact Gram Scope

Define the mathematical operator A=M_D^(-1/2)*sum_(d0 in D) T_(d0), where
(T_(d0)v)(z)=v(z-d0). Then F^-1 A F=sqrt(M_D)*Pi_C. This does not make A
a physical isometry or a free operation.

The exact proof is [Exact Predicate Channel, Orthogonal Pattern Basis](EXACT_PREDICATE_CHANNEL.md#orthogonal-pattern-basis).
Locally phi_0=|0> and phi_1(u)=W(u)/q are orthonormal and have disjoint
zero/nonzero support. Their tensor products phi_sigma span W_pat, and

    g=2^(-N/2)*sum_(wt(sigma)<=w) (-1)^(b dot sigma)*phi_sigma.

Hence the EXACT radius-truncated g lies in W_pat. If R_c is the product
uniform root state for pattern c, the F R_c are another orthonormal basis
of W_pat. Restriction to C preserves their disjoint supports. Consequently
the compressed A^*A is diagonal in that basis with eigenvalues

    lambda_c=2^N*|Omega_c|/q^(N-K).

Equivalently it is H_N diag(lambda_c) H_N in the phi_sigma basis, with
normalized Hadamard H_N. Invariance of W_pat under A is NOT required.
The Mersenne character/MDS bound holds for every c and supplied point set:

    beta=min(1,(1+2^s*ceil(sqrt(q)))/q),
    gamma=beta+(1-beta)/q,
    eta=min((q^K-1)*beta^(N-K+1), q^K*gamma^N),
    |lambda_c-1|<=eta<q^(-N/8)<1/2.

Thus (1-eta)||v||^2<=||Av||^2<=(1+eta)||v||^2 for v in W_pat, giving

    Z:=||Ag||^2 in [(1-eta)*tau,(1+eta)*tau].             (1)

Clipping label probabilities need not preserve W_pat. We NEVER apply (1)
to square roots of clipped laws. Clipping below affects only classical
proposals; exact g remains in every amplitude calculation.

## 4. Complete-List Rejection Identity

For every received z compute the complete list and exact signed sums

    List(z)={d0 in D:wt(z-d0)<=w},
    B(z)=sum_(d0 in List(z)) g(z-d0),
    R(z)=sum_(d0 in List(z)) |g(z-d0)|^2.

Ideal reference proposal: draw e from |g|^2/tau, draw d0 uniformly from D,
and set z=d0+e. Uniform D sampling uses nK fair bits and O(NK) field
operations. Its density and acceptance rule are

    rho(z)=R(z)/(M_D*tau),
    alpha(z)=|B(z)|^2/(P*R(z)), or 0 when R(z)=0.

Cauchy-Schwarz gives |B|^2<=|List(z)|*R<=P*R. Therefore

    rho(z)*alpha(z)=|B(z)|^2/(P*M_D*tau),
    p_acc=Z/(P*tau)>=(1-eta)/P,
    nu_pre(z)=|B(z)|^2/(M_D*Z).                          (2)

This is the Born law of Ag/sqrt(Z), BEFORE F^-1. Expected ideal outer
trials are <=P/(1-eta). Without a lower bound on Z/tau this rejection
identity alone can have exponential cost.

Use EXACT ORIGINAL signed amplitudes, not clipped amplitudes or absolute
values. Write t_e=product_i(q*[e_i=0]+(-1)^(b_i)*W(e_i)).
For retained e, g(e)=t_e/(sqrt(2)*q)^N. The common denominator cancels:
alpha=(sum t_e)^2/(P*sum t_e^2). Integers have O(nN) bits, so cancellation
and the rational acceptance probability are computed exactly.
Z need not be known to sample. Exact normalized CT amplitude queries
B/sqrt(M_D*Z) are NOT provided; sampling below is approximate as well.

## 5. Explicit Finite-Clock Error Budget

Fix rational 0<epsilon<=1/2. At most T outer trials are allowed:

1. Draw at most H uniform N-bit support masks, keeping the first with
   weight <=w; otherwise return ABORT. Failure is <=2^-H because tau>=1/2.
   Conditional success gives the exact truncated support-pattern law.
2. Draw each active phase label using a strict-clock sampler with TV error
   <=delta from pi, INCLUDING its ABORT and random-bit errors.
3. Draw a uniform D message, form z, and compute B,R by complete decoding
   and exact ORIGINAL signed amplitudes.
4. With b_rand fair bits accept using floor(2^b_rand*alpha)/2^b_rand.
   This downward rounding changes one acceptance kernel by <2^-b_rand.
5. Return the first accepted z, or ABORT after T trials. Retain every
   local/support ABORT; do not substitute arbitrary labels or witnesses.

Coupling to the ideal reference and counting at most TN label calls gives

    TV(actual,nu_pre)
      <= exp(-(1-eta)*T/P)+TN*delta+T*2^-H+T*2^-b_rand.    (3)

ABORT is included; nu_pre assigns it zero mass. Heisenberg's safe budget is

    T=2P*ceil(log2(4/epsilon)),
    delta=epsilon/(4TN),
    H=b_rand=ceil(log2(4T/epsilon)).

Since eta<1/2, every term in (3) is <=epsilon/4. This does NOT claim an
exact conditional nu_pre law when the proposals use clipped local laws.

The local contract is realizable with finite fair bits. The local audit
gives sum pi(u)^2<=Delta/q, Delta=14 or30 for r=3 or5. Clip at C_clip/q,
C_clip=ceil(3Delta/delta). The ideal accepted clipped law is within
delta/3 of pi and has acceptance >=(1-delta/3)/C_clip. Cap uniform-field
proposals at J_loc=2*C_clip*ceil(log2(3/delta)), giving failure <=delta/3.
Round each local rational acceptance downward with
b_loc=ceil(log2(3J_loc/delta)) fair bits; total rounding error is <=delta/3.
Thus the full per-label error, including ABORT, is <=delta.

Conservative evaluator work, including list amplitudes, is

    O(n^45*T^2*N^2*log(TN/epsilon)/epsilon),

plus T complete-decoder calls and polynomial integer/random-bit work.
Serial Walsh calls reuse O(n^21) workspace; decoder storage, O(nN)-bit
signed products, counters, and coin thresholds add polynomial space.
Runtime is polynomial in 1/epsilon, NOT merely log(1/epsilon). There is
no unbounded exact rational-coin primitive, uncharged postselection, or
permission to count a computational WORK_CAP as the ABORT in (3).

## 6. Final-Fourier Limitation And Primary Comparisons

The ideal quantum protocol has unnormalized accepted state Ag/sqrt(P),
hence herald probability Z/P. Classical rejection conditions on the ball
first and accepts with Z/(P*tau). These differ by tau; only their ideal
conditional PRE-Fourier Born laws coincide.

The [exact channel identity](EXACT_PREDICATE_CHANNEL.md#exact-paid-output-law),
with k_m(t)=2^-N*sum_(wt(sigma)<=w)(-1)^(sigma dot t), gives

    Pr[pattern c AND quantum herald]=lambda_c*|k_m(b+c)|^2/P,
    p_native=lambda_b*tau^2/P,
    nu_post(x)=2^N*|k_m(b+f_s(x))|^2/(q^(N-K)*Z), x in C.

The ideal quantum output conditional on native success is uniform on
Omega_b. The classical z from (2) is not that output or a native witness.
Since |k_m(t)|<=tau, (1) gives

    log2 max_x nu_post(x)<=-7n^3/8+n^2-n/8+O(1).

Every polynomial-size output set has negligible mass. This defeats the
sparse-output hypothesis, not all classical samplers. Inverse-polynomial
additive marginal estimates do not automatically resolve conditional
probabilities of exponentially small prefixes. Efficient point queries
also do not supply those global prefix masses.

[Jo, Theorem 5.2](https://arxiv.org/html/2607.16541v2) is a paid coherent
complete-list construction. [Horinaga--Yamakawa, Theorem 5.1](https://arxiv.org/pdf/2607.14650v2)
is a quantum prime-power theorem with source/tail/normalization premises
and a final inverse QFT, not a classical SQ closure theorem.
[Schwarz--Van den Nest, Theorems 1-2](https://arxiv.org/html/1310.6749)
also require approximate output sparsity, which fails above even if CT
access were granted. [Marwaha et al., Section 3.2 and Theorem 24](https://arxiv.org/html/2509.14443)
do not turn additive estimation into general sampling; their general
computable-weight sampling theorem uses an NP oracle.

The same-input polynomial representation has degree <N-K, rate about7/8,
and acceptance sets h_i*{x:f_s(x)=b_i}, h_i=product_(j!=i)(alpha_i-alpha_j).
It is not arbitrary OPI or the rate-1/8 dual decoding problem. A future
full paid-output TV-epsilon sampler would give verified native search
with probability >=p_native-epsilon, and conditional near-uniform error
O(epsilon/p_native), not exact uniformity. No such sampler is proved here.
The parent owns integration and checks; reported finite controls and the
independent review do not constitute execution of this new sampler.
