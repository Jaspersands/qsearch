# 2026-11-13 Native community energy, one-particle mass, and one vector

## Scope and conclusion

The proposed ALL-LABEL operator gate holds, with the d! ordered/set factor
explicit. It applies uniformly to every complex density matrix above the
energy threshold, including states chosen adaptively from the observed graph.
A finite randomized classical procedure constructs ONE certified unit
high-Rayleigh vector and its exact rational one-particle density in
n^(ell+O_p(1))*poly(B,log(1/eta)) BIT time. No spectral projector is supplied
or constructed. Labels occur only in the proof.

This is not a labeling decoder. Cloning, rounding, validation, any quantum
composition, novelty, and advantage remain unproved here. STATE/TRAPS and
the assigned stable notes were read. No API/network/Git/archive or numerical
experiment was used. The retained uniform noise theorem is reused at its
stated sufficient-n scope, not reasserted for small n without its conditions.

## 1. Native operators and factorials

Fix p=2d>=4, k>=3 and rational 0<q<1/2; take known rational 0<epsilon<q.
Conditional on x in [k]^n, independent edge bits have means q+epsilon*f_x(E),

    w_a(i)=1[x_i=a]-1/k,  f_x(E)=sum_a product_(i in E) w_a(i).

The actual algorithm sees only these bits and the public parameters. Write

    N=binom(n,ell), D=binom(ell,d)binom(n-ell,d),
    V=n^d binom(ell,d), r=k*d^2*V/n, c=1/(2k^p), a=c*epsilon*D.

On ell-SETS, A=sum_E(Y_E-q)A_E, where (A_E)_(S,T)=1[S triangle T=E].
Each row has D possible neighbors. Its mean is epsilon*M_x.

On ordered injective ell-tuples let K_x have entry f_x(E) when exactly d
slots change and their 2d old/new labels are distinct, and zero otherwise.
Define A_ord by the same rule with Y_E-q. The isometry

    W|S>=(ell!)^-1/2 sum_(orderings of S) |ordered S>

satisfies EXACTLY W* K_x W=d!*M_x and W* A_ord W=d!*A. For a fixed
ordered source and legal set transition there are precisely d! target
orderings: the ell-d common entries stay in their original slots. Summing
ell! source orderings cancels the isometry's ell!, leaving d!, not ell!.
The symmetric range of W is invariant, since the ordered operator commutes
with every slot permutation.

On the full (C^n)^tensor ell let Pi be injective-tuple projection and put

    B=sum_(J subset [ell], |J|=d) sum_a tensor_(j in J)|w_a><w_a|,

with identity on other slots. B is PSD, ||B||<=kV, and the exact comparison is

    ||Pi B Pi-K_x||<=r.                                             (1)

For each source row and J, an unwanted target must use at least one of the
d old J-vertices among its d new slots. There are at most d^2*n^(d-1)
such assignments; each summed community coefficient has magnitude <=k.
Projection only removes assignments, and repeated J contributions are
charged separately. The symmetric row-sum bound proves (1), including the
diagonal and terms changing fewer than d slots. Thus also M_x>=-r/d!*I.

## 2. All-label energy implies one-particle planted-span mass

Let L=span{w_a}, P_L its orthogonal projector, and N_L=sum_j P_L^(j).
Since |w_a><w_a|<=n P_L, and projectors in distinct slots commute,

    tensor_(j in J)|w_a><w_a| <= n^d product_(j in J)P_L^(j)
                              <= (n^d/d)sum_(j in J)P_L^(j).

Each slot occurs binom(ell-1,d-1) times. Therefore

    B <= (kV/ell) N_L.                                             (2)

For ANY trace-one PSD sigma supported on injective tuples, define
rho_1=(1/ell)sum_j Tr_except_j sigma. Equations (1),(2) and any valid noise
bound ||A_ord-epsilon*K_x||<=nu give the deterministic implication

    Tr(P_L rho_1) >= [Tr(A_ord sigma)-nu-epsilon*r]/(epsilon*kV).     (3)

The statement needs no real-amplitude condition, purity, independence of
sigma from the graph, planted gauge, balanced labels, or spectral gap.
For a set-slice density sigma_S use sigma=W sigma_S W*: its energy in (3)
is d!*Tr(A sigma_S). Positivity order and trace alone prove the claim.

The retained ordered noise theorem gives, conditional on EVERY x,

    ||A_ord-epsilon*K_x||<=d!*T,
    T=2^300 ceil(sqrt(D*ell)),                                     (4)

except with probability <=2n^(-2ell), under its explicit scalar large-n
conditions. Compression gives the set-noise bound T on this SAME event.
There is no extra union bound over states, communities, or repeated trials.

For concrete constants impose

    d!*D/V >= 1/2,       r/d! <= cD/8,       T<=a/8.                (5)

Then every sigma with Tr(A_ord sigma)>=d!*a/2 satisfies

    Tr(P_L rho_1) >= c/(8k)=1/(16k^(p+1))=:mu.                     (6)

Indeed the numerator in (3) is at least d!*a/4. The exact ratio is
d!*D/V=(n-ell)_d/n^d. It is at least 1/2 if n>=2d(ell+d).
Given that ratio, n>=32k^(p+1)d^2 suffices for the second inequality in (5).
The last follows, for example, from

    epsilon^2 D >= (16*2^300/c)^2 ell.                              (7)

At fixed q this is the retained log-free normalized-SNR scale. Dividing
A_ord by sqrt(q(1-q)) divides its energy and noise thresholds by the same
factor and replaces epsilon by beta; no q or factorial disappears.

There is also a useful soft-band statement. On (4),(5), A_ord>=-d!*a/4.
If at least 1-delta of sigma's mass lies at eigenvalues >=3d!*a/4, then
its energy is at least d!*a(3/4-delta). Thus delta<=1/4 suffices for (6).
No separation between individual eigenvalues inside or around that band is
assumed, and no band projector is provided as algorithmic input.

## 3. A positive eigenvalue exists; lower spectral control is also paid

The retained label-only witness is elementary and independent of balance:
v0=(w_b/||w_b||)^tensor ell. Retaining community b alone gives the conservative
lower bound <v0,Bv0> >= binom(ell,d)*||w_b||^(2d) >= V/k^p; the other
community summands are PSD, so no equality is asserted. Its coordinate weights
are <=k^2/n, so collision projection and normalization give
||Pi v0/||Pi v0||-v0||<=k*ell/sqrt(n). Therefore the compressed mean has

    lambda_max(M_x) >= (V/d!)[k^-p-2k^2 ell/sqrt(n)-k*d^2/n].       (8)

If the bracket is >=1/(2k^p), then lambda_max(M_x)>=cD. Sufficient simple
conditions are n>=64k^(2p+4)ell^2 and n>=4k^(p+1)d^2. The stronger second
condition in (5) can be used instead. No witness is revealed to the algorithm.

On the single noise event, (5),(8) give simultaneously

    lambda_max(A)>=7a/8,           lambda_min(A)>=-a/4.              (9)

The second inequality follows from (1), not from a Boolean gauge or an
assumption that the native mean is literally PSD. It prevents a large
negative eigenvalue from defeating the unshifted power construction below.

## 4. Exact finite classical construction of one high-Rayleigh vector

Write q=u/Q and Z=Q*A, an INTEGER sparse symmetric matrix. Set
b=bitlength(N), j=4(b+4). Draw a vector h of N independent uniform signs,
compute y=Z^j h by j sparse matrix-vector products, and, if y!=0, test EXACTLY

    2*y^T Z y >= Q*a*(y^T y).                                     (10)

Clear the known rational denominator of a when comparing. If the test
passes, output the unit vector v=y/sqrt(y^T y), represented by the integer
vector and its common squared norm. Its Rayleigh quotient is at least a/2
on EVERY input, since (10) is an exact certificate. No irrational entries
need be expanded to provide this algebraic representation.

Here is the success proof, conditional only on (9). Choose a real unit top
eigenvector e in the analysis. E(e.h)^2=1 and E(e.h)^4<=3, so
Pr(|e.h|>=1/sqrt(2))>=1/12. On that event, the normalized y has weight at
most

    2N*(6/7)^(2j) <= 1/8

outside the band lambda>=3a/4: its eigenvalues there have absolute value
at most 3a/4 by (9), whereas the top eigenvalue is at least 7a/8. The same
ratio holds for Z, so Q cancels. The displayed bound uses (6/7)^8<1/2 and
N<=2^b. The Rayleigh quotient is consequently >=3a/4-a/8=5a/8, so (10)
passes. This works with top-eigenvalue multiplicity and without any gap.

Use R=12(ceil(log2(1/eta))+1) independent trials, then ABORT if none passes.
Conditional failure is <=eta. Every branch has the same finite maximum
clock, including bad statistical instances. Overall failure is bounded by
2n^(-2ell)+eta, not by pretending that new starts resample the input graph.

Each coordinate after j steps has O(j(log Q+log D)+1) bits, since the
absolute row sum of Z is <=QD. The certificate, norm and inner products
have polynomial bit length. Neighbors are enumerated by deleting d entries
and inserting d outside vertices; edge lookup, subset ranking, and reading
all binom(n,p) source bits are charged. Thus R*j sparse products and tests
cost n^(ell+O_p(1))*poly(B,log(1/eta)), with comparable finite storage.

## 5. Exact one-particle contraction, not a free projector

For the returned vector, symmetry of Wv makes every slot marginal equal.
Directly tracing ell-1 slots gives

    (rho_1)_(i,j) = 1/[ell*(y^T y)]
       *sum_(T subset [n], |T|=ell-1, T disjoint {i,j})
              y_(T union {i})*y_(T union {j}).                      (11)

For a complex vector the second factor is conjugated. The factor 1/ell is
(ell-1)!/ell!, so no ordered multiplicity remains. Equivalently sum the
outer products of vectors u_T(i)=y_(T union{i}) for i outside T and zero
otherwise, then divide by ell*y^T y. This proves PSD and trace one exactly.
Enumerating T and its n-by-n outer product costs at most n^(ell+1)*poly(B,
ell log n) BIT operations. The result is a rational n-by-n density matrix.
No N-by-N spectral projector, N^2 matrix, or uncharged matrix oracle is used.

## 6. IID balance supplies a well-conditioned planted frame

Let n_a count label a and let F=sum_a |w_a><w_a|. For the n-by-k column
matrix U=[w_1 ... w_k], U*U annihilates the all-ones vector. For every
complex h with sum_a h_a=0 its quadratic form is exactly sum_a n_a|h_a|^2.
Hence, if all n_a lie between n/(2k) and 3n/(2k), rank(U)=k-1 and

    [n/(2k)]P_L <= F <= [3n/(2k)]P_L.                               (12)

IID uniform labels satisfy this event with probability at least
1-2k*exp(-n/(12k)) by the multiplicative binomial Chernoff bounds. Combining
(6),(12) gives Tr(F rho_1)>=n*mu/(2k). Since Tr(F)=n(k-1)/k exactly, some
normalized w_a has rho_1 expectation at least mu/[2(k-1)]. This is analysis,
not a rule accessing that hidden column or promising mass in every color.

The mass gate itself was all-label and did not need balance. With balance
included the total exceptional probability is at most
2n^(-2ell)+eta+2k*exp(-n/(12k)). Extracting and validating a labeling from
this density is the next distinct obligation, and is not claimed here.
