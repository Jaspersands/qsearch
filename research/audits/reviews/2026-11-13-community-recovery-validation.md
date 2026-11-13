# Native community validation; three-way cloning is unnecessary

2026-11-13. Independent derivation after STATE/TRAPS, post-purity selection,
and the existing two-way source repair. No network/API/Git, numerical
controls, shared-status changes, candidate generator, or quantum-clock claim.

**Main result.** At the retained fixed-q frontier, the ORIGINAL observed
graph validates arbitrary data-dependent candidate labelings uniformly.
No validation clone or conditional independence of candidate and graph is
needed. The proposed three-way channel also has the requested error bound,
proved in Section 4 below, but is unused in the simpler construction.

## 1. Exact signal, centering, and mean

Fix even p=2d>=4, k>=3, and 0<q<1/2. For labels x in [k]^n define

    w_a^x(i)=1[x_i=a]-1/k,
    f_x(E)=sum_(a=1)^k product_(i in E) w_a^x(i),
    Y_E independently Bern(q+epsilon f_x(E)), conditional on x.

The native 0<epsilon<q guarantees valid probabilities. Holder in the color
index gives |f_z(E)|<=product_(i in E)||w^z(i)||_p<=1 for EVERY labeling z,
since p>=2 and ||w^z(i)||_2=sqrt(1-1/k). Put M=binom(n,p).

For a candidate z, its computable score is

    S_z=sum_(|E|=p) f_z(E)(Y_E-q).

For analysis only, let P_ab=n^(-1)#{i:x_i=a,z_i=b}, with row/column
marginals rho_a,tau_b, and set

    C=H P H, H=I-11^T/k,
    C_ab=P_ab-rho_a/k-tau_b/k+1/k^2
        =n^(-1)sum_i w_a^x(i)w_b^z(i).

This is the centering required by the native signal. It is NOT P-rho*tau^T.
All row/column sums of C vanish, without an empirical balance promise.
Write E(C)=sum_ab |C_ab|^p=sum_ab C_ab^p. Expanding ordered vertex tuples,
then discarding tuples with repeated indices, proves

    mu_z:=E[S_z|x]
      =epsilon*n^p/p! * (E(C)+e_z),
    |e_z|<=K_0/n,  K_0=k^2*binom(p,2).                  (1)

Indeed, for each a,b the all-tuples sum is n^p C_ab^p, while at most
binom(p,2)n^(p-1) tuples repeat an index and every summand has modulus<=1.
This is the claimed O(epsilon n^(p-1)) correction with an explicit constant.
No label averaging across overlapping edges or across candidates is used.

## 2. Signal energy is equivalent to permutation advantage

Let A(z,x)=max_pi n^(-1)#{i:z_i=pi(x_i)}. For every permutation,

    sum_a C_(a,pi(a)) = sum_a P_(a,pi(a))-1/k.

Thus m(C):=max_pi sum_a C_(a,pi(a))=A(z,x)-1/k. For all such C,

    k^(1-2/p)/(k-1)^2 * E(C)^(1/p)
       <= m(C) <= k^(1-1/p) E(C)^(1/p).                (2)

The upper bound is Holder on a permutation diagonal. For the lower bound,
let B=max_ab |C_ab|>=k^(-2/p)E(C)^(1/p). A zero-sum row contains a
positive entry C_ab>=B/(k-1): this is immediate if an absolute maximizer
is positive, and otherwise follows by summing the other entries of its row.
For a uniform permutation conditioned on pi(a)=b, the zero row/column sums
give E[sum_i C_(i,pi(i))]=k C_ab/(k-1). Its maximum is at least this mean.
This proves (2), including C=0. Even p is essential to the energy identity.

In particular, a genuinely correlated candidate with A>=1/k+rho, rho>0,
has E(C)>=e_0:=rho^p/k^(p-1). Conversely any constant positive energy
forces constant permutation advantage. Neither C nor the maximizing
permutation is computed by the validation algorithm.

## 3. Uniform validation on the original graph

For a FIXED candidate z, independence of the edges conditional on x gives

    Var(S_z|x)<=sum_E f_z(E)^2/4<=M/4,
    Pr(|S_z-mu_z|>=u | x)<=2 exp(-2u^2/M).             (3)

For a training-independent validation graph the same conditional variance
would hold after conditioning on a training-generated candidate. That
extra graph is unnecessary: union bound (3) over ALL k^n possible z gives

    Pr(exists z: |S_z-mu_z|>u | x)
       <=2 exp(n log k-2u^2/M).                       (4)

Consequently (4) covers any later data-dependent list, randomized/quantum
candidate-generation procedure, and score-selected candidate. It does not
assert the fixed-candidate variance for a selected data-dependent z.

For an explicit recovery consequence, fix a desired constant rho>0 and e_0
as above. Assume n>=8K_0/e_0, and put

    A_0=epsilon*n^p/p!,    u=e_0*A_0/8.

On the uniform event in (4):

* Every candidate with agreement >=1/k+rho has S_z>=3e_0 A_0/4.
* Every candidate with S_z>=3e_0 A_0/4 has E(C)>=e_0/2 and hence
  agreement >=1/k+rho/[(2k)^(1/p)(k-1)^2].

These assertions follow directly from (1), the u error, and (2). Therefore
maximizing the score over ANY nonempty list selects a weakly correlated
labeling whenever that list contains a rho-correlated labeling. Ties may
be broken lexicographically. This does not supply such a list.
The failure probability of this uniform validation event is at most

    2 exp(n log k-e_0^2 epsilon^2 n^p/(32 p!)).         (5)

This bound is uniform in the hidden labels. Thus it also holds for their
native IID-uniform distribution. It is a one-graph statistical bound;
rerunning computation does not manufacture independent graphs or reduce
this graph-failure floor arbitrarily.

To check the retained frontier, let
D=binom(ell,d)binom(n-ell,d), beta=epsilon/sqrt(q(1-q)), and suppose
beta^2 D>=c_0 ell for a fixed c_0>0. Since
D<=ell^d n^d/(d!)^2,

    epsilon^2 n^p/n
      >=q(1-q)c_0(d!)^2 (n/ell)^(d-1).                (6)

For fixed q and growing polylogarithmic ell this tends to infinity; in
fact ell=o(n) suffices for validation alone. Hence (5) tends to zero.
Stronger known original signal only improves (5); validation needs NO
attenuation. This does not extend the other source/compiler lemmas to
sparse q or different ell regimes.

The BIT cost is native. If q has denominator Q, then k^p Q is a common
denominator for every S_z. Exact numerator bits are
O(log M+p log k+bits(q)); one score costs O(Mpk) elementary operations.
No latent labels, approximate likelihood oracle, or real-number comparison
is required. List-generation and total-list-size costs remain separate.

## 4. Optional exact three-way channel, not used for validation

For completeness, take one Y~Bern(q+delta), |delta|<=q/2, and
w=(1-2t,t,t), 0<=t<=1/2. Choose J with probabilities w, put Y in output J,
and fill the other two outputs with independent Bern(q) draws. Call its
joint law P and the independent-marginal target R=product_i Bern(r_i),
r_i=q+w_i delta, v_i=r_i(1-r_i).

Conditioning on J shows that under P the centered pair moments are
-delta^2 w_i w_j and the centered triple moment is 2delta^3 w_1w_2w_3.
Expand P/R in the orthogonal product basis {product_(i in A)(X_i-r_i)}
under R. The first-order coefficients vanish and orthogonality gives EXACTLY

    chi^2(P||R)
      =delta^4 sum_(i<j) w_i^2 w_j^2/(v_i v_j)
        +4delta^6(w_1w_2w_3)^2/(v_1v_2v_3).           (7)

Put sigma^2=q(1-q). Concavity on [q/2,3q/2] gives v_i>=sigma^2/2,
and delta^2/sigma^2<=1/4. Also sum_(i<j)w_i^2w_j^2<=9t^2/4 and
(w_1w_2w_3)^2<=t^4<=t^2/4. Substitution yields

    chi^2(P||R)<=12 (delta/sigma)^4 t^2.              (8)

Thus the requested C_q delta^4 t^2 bound holds with C_q=12/[q^2(1-q)^2].
Require 0<epsilon_*<=min(epsilon,q/2). For all edges processed independently
conditional on labels, |f_x|<=1 and delta_E=epsilon_* f_x(E) give

    TV(actual three clones, ideal independent clones | x)
      <=(1/2)sqrt(exp(12M beta_*^4 t^2)-1),            (9)

where beta_*=epsilon_*/sigma. The same bound holds after mixing labels.
It is O(sqrt(M beta_*^4 t^2)) when that quantity tends to zero.
At beta_*^2 D=Theta(ell), ell=polylog(n), and t=1/ceil(log_2 n),
the exponent is O(ell^(2-p)t^2)=o(1). Work at n>=8 so all weights are
positive. Known stronger signal can first be attenuated exactly by keeping
the original bit with probability epsilon_*/epsilon, otherwise drawing Bern(q).

Bounded fair-bit implementations round each Bernoulli/categorical threshold.
With b=ceil(log_2(8M/eta_num)) bits per draw, coupling the constant number
of draws per edge (including optional attenuation) adds at most eta_num
TV. Rational threshold arithmetic costs poly(inputbits,b). No exact
bounded-bit Bern(1/3) sampling is asserted. Datasets are formed ONCE;
they are not a renewable source of independent graphs.

## 5. Join to an eventual recovery algorithm

Use the established TWO-way source only for candidate generation if that
algorithm needs separate guide/matrix data. Its success event may be
transferred from ideal clones to actual clones by the existing TV bound.
Independently, (4) holds on the actual original Y for every candidate.
A union bound joins these events even though Y and the clones are dependent.
There is no comparison of a joint law containing original Y and fictitious
independent clones, and no TV multiplication by the number of validation
uses. Score the returned list on original Y and select its maximum.

This closes only native validation/source bookkeeping. The all-label
accepted-band implication, correlated-candidate construction, and complete
classical/quantum clocks are not assumed or proved by this note.
