# Mersenne Coordinate Schmidt Filter

2026-10-29. **WRITTEN DERIVATION; INDEPENDENT AUTOMATED REVIEW COMPLETED.**
Exact and robust representation bounds, not a sampling-hardness theorem,
novelty claim, implementation, or quantum advantage claim. An independent
reasoning agent found no mathematical error under the stated count premises.
This is not formal verification or human peer review. Parent-executed finite
controls and analytic certificates are distinguished in Section 7.

## 1. Original Instance And Count Premises

Preserve the [native relation](MERSENNE_RECIPROCAL_RESEARCH_TARGET.md):

    n odd prime >=17; q=2^n; N=n^2; K=(N-1)/8;
    s=floor((n-3)/4); d=2^s-1;
    f_s(x)=Tr(inv0(x)^d), inv0(0)=0;
    H[j,i]=alpha_i^j, 0<=j<K;
    C=ker H; D=rowspan H; |D|=q^K;
    Omega_b={x in C : f_s(x_i)=b_i for every i}.

The checked public field representation, arbitrary distinct public alpha_i,
and arbitrary target bits b_i are unchanged. No favorable point layout,
planted witness, subfield restriction, or change of parity equations is used.
The additive Fourier transform F uses Tr(sum_i x_i*z_i) and factors by
field coordinate. Every local predicate fiber has exactly q/2 elements.

Use the original [Walsh/MDS count premises](MERSENNE_CLASSICAL_ACCESS_AUDIT.md#3-any-accepted-half-assignment-can-be-completed):

    W(u)=sum_x (-1)^(f_s(x)+Tr(u*x)); W(0)=0;
    |W(u)|/q <= beta=min(1,(1+2^s*ceil(sqrt(q)))/q), u!=0;
    gamma=beta+(1-beta)/q;
    eta_m=min((q^K-1)*beta^(m-K+1), q^K*gamma^m), m>K.

For ANY coordinate subset S of size m>K, ANY syndrome y in F_q^K,
and ANY bit pattern c in {0,1}^m, these premises give

    z_S(y,c)=#{x_S:H_S*x_S=y, f_s(x_S)=c}
            =q^(m-K)*2^(-m)*(1+epsilon_(S,y,c)),
    |epsilon_(S,y,c)|<=eta_m.                              (1)

This is the uniform arbitrary-syndrome statement, not only the y=0 count.
The columns remain the ORIGINAL distinct Vandermonde columns. Their dual
words are evaluations of polynomials of degree <K; a nonzero word has
at least m-K+1 nonzero positions. The sum of beta^wt(P|S) over nonzero
polynomials P of degree <K is exactly the positive MDS expression

    sum_(h=0)^(K-1) binom(m,h)*beta^(m-h)*(1-beta)^h*(q^(K-h)-1).

It bounds the relative character-sum error and is bounded by both terms
defining eta_m. Arbitrary y only contributes unit-modulus character signs;
arbitrary c only contributes predicate signs. Thus neither changes (1).
The already established canonical numerical inequality is

    gamma*q^(1/4)<5/8;
    eta_m<(5/8)^(4K)<1 for m>=4K;
    eta_N<q^(-N/8)<1/2.                                   (2)

These are inherited analytic premises, not new conditional-mass algorithms.
In particular EVERY pattern has a nonempty fiber in EVERY syndrome sector
on any subset of size at least 4K.

## 2. Uniform Native State: Exact Rank

Choose ANY coordinate partition I,J with L=|I|=4K and R=|J|=4K+1.
For a nonempty fiber let |S;y,c> be its normalized uniform vector.
Its supports are disjoint for different pairs (y,c). The uniform native
state therefore has the exact Schmidt decomposition

    |Omega_b> = sum_y sqrt(p_y) |I;y,b_I> |J;-y,b_J>,
    p_y=z_I(y,b_I)*z_J(-y,b_J)/|Omega_b|.                  (3)

Both factors are positive by (1)-(2), for all q^K syndromes. Hence

    SchmidtRank_(I:J)(|Omega_b>) = q^K.                    (4)

The minus sign is retained to display syndrome matching; in characteristic
two it equals a plus sign. No syndrome or fiber enumeration is an algorithm
being supplied by this decomposition.

## 3. Radius-Filtered State: Exact Rank

Let w=floor(3N/5), tau=2^(-N)*sum_(j<=w) binom(N,j), and

    k_w(t)=2^(-N)*sum_(|sigma|<=w) (-1)^(sigma dot t).

The [exact channel identity](EXACT_PREDICATE_CHANNEL.md#exact-paid-output-law)
and [global access normalization](MERSENNE_GLOBAL_FOURIER_ACCESS.md#3-exact-gram-scope)
give the normalized post-Fourier state, conditioned on the quantum herald:

    Psi_w(x)=sqrt(2^N/(q^(N-K)*Z))*[Hx=0]*k_w(b+f_s(x)),
    (1-eta_N)*tau <= Z <= (1+eta_N)*tau.                  (5)

Explicitly Z=sum_c (2^N*|Omega_c|/q^(N-K))*|k_w(b+c)|^2.
Here b+f_s(x) is bitwise addition. This is NOT conditioning on native
verification; that further conditioning produces (3). All signed k_w
amplitudes in (5) are retained, not replaced by absolute values.

Order rows x_I by H_I*x_I=y and columns x_J by H_J*x_J=-y.
The amplitude matrix is a direct sum of q^K syndrome blocks. Within block
y, group rows and columns by c_I=f_s(x_I), c_J=f_s(x_J). In normalized
fiber bases its matrix, up to the common nonzero scalar in (5), is

    diag(sqrt(z_I(y,c_I))) * K_b * diag(sqrt(z_J(-y,c_J))),
    K_b[c_I,c_J]=k_w(b_I+c_I,b_J+c_J).                     (6)

All diagonal entries are positive by (1)-(2); directions orthogonal to
the uniform fiber vectors are annihilated. Thus this block has rank
rank(K_b). Changing b permutes rows and columns and cannot change rank.
For b=0, with unnormalized Boolean character matrices U_L,U_R,

    K_0=2^(-N)*U_L*M*U_R^T,
    M[sigma_I,sigma_J]=[|sigma_I|+|sigma_J|<=w].           (7)

The character matrices are invertible. Grouping M's identical rows and
columns by Hamming weight preserves its rank, reducing it to

    T[j,k]=[j+k<=w], 0<=j<=L, 0<=k<=R.

Here max(L,R)<=w<N. Rows j=0,...,w-R are the same all-one row.
Each subsequent difference T[j-1,:]-T[j,:], for j=w-R+1,...,L,
is a distinct coordinate vector at k=w-j+1>0. These N-w differences
are independent; the all-one row is independent of them because its
k=0 entry is nonzero. These rows and differences also span T. Thus

    rank(T)=N-w+1;
    SchmidtRank_(I:J)(Psi_w)=q^K*(N-w+1).                 (8)

## 4. Robust Rank, With Constants

Define the SAME quantitative constant for both states:

    kappa=((1+eta_L)*(1+eta_R))/(1-eta_N)
          =1+2^(-Omega(N)).                              (9)

For (3), (1) and |Omega_b|>=q^(N-K)*2^(-N)*(1-eta_N)
give p_y<=kappa/q^K. For (5), the squared Frobenius norm of block y is

    B_y=2^N/(q^(N-K)*Z) *
        sum_(c_I,c_J) z_I(y,c_I)*z_J(-y,c_J)*|k_w(b+c)|^2.

Parseval gives sum_c |k_w(b+c)|^2=tau. Substitution of (1) and (5) yields

    B_y <= q^(-K)*(1+eta_L)*(1+eta_R)*tau/Z
         <= kappa/q^K.                                  (10)

Every squared singular value of a block is at most its squared Frobenius
norm. The full matrix is block diagonal, so EVERY squared Schmidt weight
of either normalized state is at most kappa/q^K. Consequently, for ANY
normalized Schmidt-rank-at-most-chi vector |v>, the optimal-overlap bound is

    |<v|Psi>|^2 <= sum_(j=1)^chi p_j^down <= kappa*chi/q^K.

For pure states, trace distance is sqrt(1-|<v|Psi>|^2). Thus distance
at most epsilon<1 requires

    chi >= (1-epsilon^2)*q^K/kappa.                       (11)

This is 2^(Omega(n^3)) for fixed epsilon<1, or more generally whenever
1-epsilon^2>=1/poly(n). No uniform exponential conclusion is asserted
for fidelity requirements that vanish arbitrarily fast with n.

At n=17, K=36 and w=173: the exact ranks are 2^612 and 117*2^612.
These are analytic substitutions, not finite-control execution results.

## 5. Scope, Carry Precision, And Existing Filters

Every ordering of whole coordinates has the 4K versus 4K+1 cut used above.
Hence (8)-(11) exclude polynomial-bond open-boundary complex MPS in EVERY
such ordering, including arbitrary input-dependent coordinate permutations
and qubit layouts with each coordinate's n bits contiguous. Basis changes
within coordinates do not help. F is coordinate-local, so the identical
ranks and fidelity bounds hold BEFORE the final Fourier transform as well.

The [carry DP](MERSENNE_CARRY_WALSH_DRAFT.md) fixes a whole frequency a;
its weights A_i=[a]^(2^i) are not independent physical frequency bits.
Its ring precision M=n+2 costs O(nM) bits per element and O(n^2*M^2)
bit operations per multiplication. Centered reconstruction recovers signed
W(a); products of N such integers need O(nN) bits. Modular contraction and
centered recovery are not complex-linear operations or positive sampling
transitions. Polynomial carry width does not supply a complex MPS bond.

[Finite-field TT stabilizers](TENSOR_TRAIN_CLASSICAL_FILTER.md) assume
supplied cores and explicitly exclude complex MPS amplitudes. The
[known-reflection simulator](KNOWN_REFLECTION_TENSOR_SIMULATION.md) maintains
polynomially many product terms, which these rank bounds exclude here.
The [ternary prefix audit](TERNARY_PREFIX_SCHMIDT.md) shares the syndrome
Schmidt method, but its different family/population bounds are not invoked.

**NO SAMPLING-HARDNESS CONCLUSION.** The polynomial approximate
[PRE-Fourier sampler](MERSENNE_GLOBAL_FOURIER_ACCESS.md) is a DIRECT
counterexample: it samples the Born law of this high-rank pre-Fourier state
without representing its amplitudes as a low-bond MPS. Fidelity obstruction
is not total-variation sampling obstruction. Arbitrarily interleaved bits,
tensor geometries outside Section 6, alternative global representations,
and direct final-Fourier samplers remain open here. No new sampler is given.

## 6. Optional Analytic Corollary: Coordinate-Leaf Trees

**INDEPENDENTLY AUTOMATED-REVIEWED; NOT PART OF THE COMPUTED CERTIFICATE.**
The parent's finite certificate retains the original balanced MPS cut.
This additional corollary assumes the uniform ALL-pattern, ALL-syndrome
count bound in [Completion Moments, Section 3](MERSENNE_COMPLETION_MOMENTS.md#3-every-accepted-three-quarter-prefix-extends),
on every subset of the ORIGINAL points. For 2K+1<=m<=N, define

    eta'_m=min(eta_m, beta^(m-2K)*(1+beta)^m).

Equation (1) then holds with eta'_m. The cited Parseval/MDS bound gives
eta'_m<exp(5/2)/30<1 throughout this range, and eta'_N<=eta_N<1/2.
For ANY cut with a=|I|>=2K+1 and b=|J|>=2K+1, repeat Section 4 with

    kappa_(a,b)=((1+eta'_a)*(1+eta'_b))/(1-eta'_N)<8.

Indeed the full-fiber and Z lower bounds use eta'_N, while each side's
count upper bound uses eta'_a or eta'_b. Parseval still sums over all
N pattern bits. Thus each squared Schmidt weight of either state is
at most kappa_(a,b)/q^K, and trace-distance-epsilon approximation requires

    chi >= (1-epsilon^2)*q^K/kappa_(a,b).                  (12)

No exact filtered-rank formula for these general cuts is asserted.
Now assume a pure-state tensor network whose underlying graph is a tree
of maximum degree three, with exactly N physical leaves, one WHOLE field
coordinate per leaf, and no other physical indices. Tensors need not be
isometric; topology and leaf assignment may depend on the input.
A leaf-weighted centroid has components with at most N/2 leaves each.
There are at most three components summing to N, so one has at least N/3
leaves. Its incident edge therefore splits the leaves into two sets with
sizes in [N/3,2N/3], both at least ceil(N/3)>=2K+1.
Cutting that single virtual edge bounds Schmidt rank by its bond dimension.
Equation (12) forces that bond to be exponential for the fidelity targets
specified after (11). This excludes polynomial-bond binary/trivalent trees
under these assumptions, also before F by coordinate-local unitarity.
It does NOT cover arbitrary tensor geometries or interleaved/split-coordinate
leaves, and gives NO sampling-hardness conclusion: the PRE-Fourier sampler
remains the direct counterexample. No additional computed controls are claimed.

## 7. Executable Scope

`theorems/mersenne_global_structure.py` computes exact rational bounds for
the 4K/(4K+1) cut, serializing exponential ranks as powers of two rather
than constructing states. At n=17 and pure trace error 1/10, its conservative
required-rank lower bound is 2^611. This is an analytic certificate.

`tests/test_mersenne_global_structure.py` separately enumerates F32 with
N=9,K=1: every syndrome/pattern sector on the 4/5 split is positive, the
pattern-kernel ranks are computed over the rationals for w=5,...,9 and
four target patterns, and block masses obey the displayed normalization.
A linear-predicate F8 control has empty sectors and prevents dropping the
positivity premise. These controls are not canonical native executions.
The reviewer inspected the source/tests but did not execute them. Review
also caught a generic length cap inconsistent with n=101,...,127 wrappers;
the cap was corrected and separate boundary regressions added.
