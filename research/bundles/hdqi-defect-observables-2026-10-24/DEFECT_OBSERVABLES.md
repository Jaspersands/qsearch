# Pilot Pauli Readouts Beyond Polynomial Sign Cost

Date: 2026-10-24. Status: LOCAL, UNREVIEWED mathematical construction and
capped exact reference tests. Not an independently established theorem,
production FPRAS, state-preparation algorithm, or quantum advantage.

## 1. Decision And Scope

The general degree-scale filtered-parent gap remains open. The recent
[spectral-width comparison](https://arxiv.org/html/2610.02859v1) has an
exp(-beta W) loss; it does not supply the needed degree-scale bound.
This pass instead attacks the operational use of the proposed pilot.

Use the explicit canonical independent generators

    O_i = X_i product_{j<i, j~i} Z_j,
    H = sum_i J_i O_i, S = exp(-beta H/2), Z = tau(S^2),
    |pi> = S|0>/sqrt(Z), D = 1 + max_degree(G),
    b = beta max_i |J_i|, lambda = b^2.

Inputs are the public graph, rational real couplings |J_i|<=1, rational
beta>=0, and an explicit Hermitian coefficient Pauli Q=i^p X^u Z^w.
tau is normalized trace. No amplitude, Gibbs, or spectral oracle is given.

LOCAL CLAIM: if D lambda <= 1/64, every such Pauli expectation has a
randomized classical additive-epsilon estimator with failure <=delta and
runtime polynomial in explicit input size, 1/epsilon and log(1/delta),
with an exponent independent of degree. This includes polynomial-L1 sums
of Paulis and their pullbacks through verified LINEAR HDQI decoders.
No polynomial bound on C=Z_commuting/Z is required.

This extends the local signed cluster construction in
`../hdqi-cluster-baseline-2026-10-24/CLUSTER_BASELINE.md`, whose proof is an
explicit dependency, not independent external validation. Connected
expansions, forest formulas, and importance sampling are established
methods; no generic-method novelty is asserted.

It does NOT give full output samples, coherent pilot preparation, nonlinear
decoder simulation, relative error on rare observables, or Gibbs accuracy
of an arbitrary decoder. In particular it does not solve the parent gap.

## 2. Large Flip Sets Can Be Discarded

Let mu(y)=|<y|pi>|^2. The redundancy-free thermal error bound gives

    Pr[T subset supp(Y)] <= product_{i in T} (beta |J_i|/2)^2.   (1)

This bound, at every beta, is from
[Hastings--Schmidhuber, Appendix A.2](https://arxiv.org/html/2610.03697v1).
Its argument uses coupling-sign conjugations, convexity of the trace
exponential, and Schatten Holder bounds on the mixed coupling derivative.
It is not a consequence of independent error bits.

Put U=supp(u), h=|U|. Partition the overlap sum for X^u Z^w by Y_U=T.
Cauchy--Schwarz bounds each part by

    sqrt(Pr[Y_U=T] Pr[Y_U=U\T]).

Bound these exact-pattern probabilities by the corresponding inclusion
probabilities in (1), then sum the 2^h patterns. The phases have modulus
one, so

    |<pi|Q|pi>| <= product_{i in U} beta |J_i|.                 (2)

Applying the same argument to any subset of U yields the sharper valid
bound product_{i in U} min(1,beta |J_i|). No independence is assumed.
If it is <=epsilon/4, output zero with that deterministic additive bound.
If any flipped coupling is zero the expectation is exactly zero.

Otherwise b<=1/8 implies 8^h < 4/epsilon. Thus only h=O(log(1/epsilon))
needs further work. Also the pilot is real: if p is odd, its Hermitian
Pauli matrix is purely imaginary and the expectation is exactly zero.
The h=0 case is the already established parity estimator. Below h>=1.

## 3. An Exact Twisted Trace Identity

For an ordered word P(u)=product_i O_i^u_i, define

    ell(u)_j = sum_{i>j, i~j} u_i mod 2.

There is no missing internal phase: P(u)=X^u Z^ell(u), and P(u)|0>=|u>.
The automorphism alpha_z(T)=Z^z T Z^z multiplies each ordered word P(y)
by (-1)^(z.y). Set z=w+ell(u), H_z=alpha_z(H), S_z=alpha_z(S). Then

    <pi|Q|pi> = i^p N_z(U)/Z,
    N_z(U) = tau(S P(u) S_z),
    Z_z = tau(S S_z) > 0,  0<Z_z/Z<=1.                       (3)

The coefficient of P(y+u) in P(u)P(y) is (-1)^(ell(u).y).
This proves (3) using orthonormal ordered words, including anti-Hermitian
P(u). All matrices here are real; N_z(U) is real. When p is odd it is
zero for the observable under consideration, as noted above.

Estimate N_z(U)/Z_z by the marked expansion below and Z_z/Z by the
existing parity log-partition estimator. Never estimate N and Z separately
to fixed absolute accuracy, or divide by an exponentially small Z_z.

## 4. One Marked Polymer

The ordinary polymers are nonempty connected SETS A of G, with activities
w_z(A) from the two exponential segments of Z_z. They obey

    |w_z(A)| <= lambda^|A|.                                  (4)

In a word contributing to N_z(U), total generator multiplicity is odd on
U and even elsewhere. Group all connected components meeting U into one
marked set A_0. It contains U, and every component of G[A_0] meets U.
The remaining components are ordinary polymers, incompatible with A_0
if they overlap it or touch it by an edge. Nonadjacent components commute,
so summing segment interleavings gives the EXACT polymer factorization.

Let v_z(A_0) be the marked activity, with insertion P(u) between segments.
Summing absolute coefficients over positive odd/even multiplicities gives

    |v_z(A_0)| <= product_{i in U} sinh(beta |J_i|)
                  product_{i in A_0\U} [cosh(beta J_i)-1]
                <= (2b)^h lambda^(|A_0|-h).                  (5)

This is a signed expansion. Do not replace v_z or w_z by absolute values
in the estimator. The absolute values are ONLY majorants.

Add a formal activity t v_z(A_0). All marked polymers overlap on U, so at
most one is allowed. The augmented partition is exactly Z_z+t N_z(U).
Differentiate its formal logarithm at t=0. For k ordinary occurrences,
including repeated ones, the result is

    N_z(U)/Z_z = sum_{k>=0} 1/k! sum_{A_0,A_1,...,A_k}
                    phi(B) v_z(A_0) product_{i=1}^k w_z(A_i). (6)

B is the occurrence incompatibility graph. phi(B) is its connected
alternating spanning-subgraph sum, with phi=1 for one occurrence. The
factor is 1/k!, NOT 1/(k+1)!, since the marked occurrence is distinguished.
Disconnected B has phi=0. Absolute convergence is proved below, so the
formal identity extends along the real-temperature path from zero.

## 5. Uniform Marked-Set Importance Sampling

Write r=|A_0|-h and n=h+r. A spanning forest rooted at U has exactly one
specified root per component. For an induced set A_0 let f_U(A_0) be its
number of such forests; it is the determinant of the induced Laplacian
with ALL root rows/columns deleted. It is positive exactly for the allowed
marked sets. For r=0 it equals one, including disconnected roots.

On n labeled vertices with the first h fixed as roots, the number of
complete-graph rooted forests is

    C_(h,0)=1; C_(h,r)=h(h+r)^(r-1) for r>=1.

Draw one uniformly, fix the h root labels to U, and traverse away from
the roots. Each nonroot selects one of D neighbor slots at its parent's
host vertex; unused slots, collisions, and hitting a prescribed root fail.
Failure returns zero, not a renormalized successful draw.

For each resulting A_0 there are exactly r! f_U(A_0) labeled embeddings.
Return

    Y_0 = v_z(A_0) C_(h,r) D^r / [r! f_U(A_0)].              (7)

Thus E[Y_0 g(A_0)] sums v_z(A_0) g(A_0) over all allowed marked sets of
size h+r. Since C_(h,r)/r! <= exp(h+r), writing a=e D lambda gives

    |Y_0| <= exp(h) (2b)^h a^r.                            (8)

Uniform forests can be sampled by
[Wilson's loop-erased walk](https://doi.org/10.1145/237814.237880) on the
complete graph with the h roots already in the tree. Every walk step hits
a fixed root with probability at least h/(n-1), so expected work is
polynomial. Cap each walk after ceil((n-1)/h log(r/delta_f)) steps for a
failure budget delta_f; a cap failure must be reported. Coupling to the
uncapped walk bounds the additional failure probability. Across N draws
allocate delta_f/N to each draw (and separately budget any ordinary random
primitive). For r=0 no walk is required. It is not a zero
activity or a valid sample. The implementation distinguishes these cases.

## 6. Full Marked-Cluster Draw And Uniform Bounds

Use the existing touching-set sampler for every ordinary child of size s:
its returned Y has |Y|<=a^s and unbiased activity sum over sets touching
the chosen parent vertex. The closed-neighborhood multiplicity is retained.

Define excess order l=r+sum_{i=1}^k s_i. For 0<=l<=L sample

    p_l = 2^(L-l)/(2^(L+1)-1).

There are exactly 2^l choices of r>=0 and an ordered positive composition
(s_1,...,s_k) of l-r, including k=0,r=l. Choose one uniformly.
Set s_0=h+r and t_total=h+l. For k>=1 draw a tree on k+1 occurrence labels,
rooted at 0, with weight product_{i>0} s_parent(i). Its total weight is

    A = s_0 t_total^(k-1),

and weighted Prufer symbols with probabilities s_i/t_total implement it.
For k=0 use A=1. Draw the marked root by (7). For each child select a
uniform vertex in its parent set, then use the touching-set sampler.
Let b_i be the number of vertices in the parent touched by its child.
For a successful draw return

    X = (2^l/p_l) (A/k!) [phi(B)/trees(B)]
                     product_{i>0} (1/b_i) product_{i>=0} Y_i. (9)

The tree distribution cancels A and the parent-vertex choices; the b_i
divisors cancel multiple contacts. Summing over trees cancels trees(B).
The forest correction accounts for all root embeddings. Therefore E[X]
is exactly (6) truncated to excess order L. No division by s_0 or an
extra host-size factor belongs in (9).

For k>=1, A/k! <= exp(h+l), and |phi(B)|<=trees(B). Equations (8)-(9)
give, with B_h=8^h and D lambda<=1/64,

    absolute sum at excess order l <= B_h (16 D lambda)^l,
    tail above L <= B_h 4^(-L)/3,
    |X| <= 2 B_h,
    |N_z(U)/Z_z| <= 4 B_h/3.                              (10)

For example before rounding constants the order bound is
exp(2h)(2b)^h (2e^2 D lambda)^l. The draw bound has 4e^2 D lambda in
place of 2e^2 D lambda and an extra factor two. Both are covered by (10).
These bounds control absolute sums, not just cancellation-prone means.
They also justify the marked series identity in (6).

## 7. Error And Bit Complexity

For an additive tau-error estimate of R=N_z(U)/Z_z choose

    L minimal with B_h 4^(-L)/3 <= tau/4,
    N >= 128 B_h^2 tau^(-2) log(2/delta_r),
    eta <= tau/[32 B_h (L+1)].

Compute each activity normalized by its envelope in (4) or (5) to error
eta, and clip that real number to [-1,1]. The product error is at most
(L+1)eta; the combinatorial prefactor after envelopes is <=2B_h. Thus
activity bias <=tau/16. Hoeffding gives statistical error <=tau/2 with
failure <=delta_r. The remaining margin covers rational arithmetic and
forest failure budgets. Exact integer random choices introduce no bias.

Activities are NOT free oracles. For marked A_0, inclusion-exclusion is

    v_z(A_0) = sum_{U subset T subset A_0} (-1)^|A_0\T|
                  tau(exp(-beta H_T/2) P_T(u) exp(-beta H_(z,T)/2)).

Use at most h+L coefficient qubits, certified rational Taylor tails, and
absolute precision equal to envelope times eta/2^|A_0| per restricted
term. Ordinary activities use the existing analogous computation.
This costs exp(O(h+L)) times polynomial arithmetic work. Very small beta
requires O((h+L)log(1/b)) additional bits, charged to input bit length;
zero b is a separate exact case. Forest/tree determinants and Ursell
coefficients also cost at most exp(O(h+L)).

Set tau=epsilon/4. Obtain log Z_z and log Z to accuracy
xi=epsilon/[32(B_h+1)] each and let r_hat be their exponentiated difference,
clipped to [0,1]. Then |r_hat-Z_z/Z|<=4xi. The product R_hat*r_hat has
error <epsilon, using |R_hat|<=2(B_h+1). Multiply by i^p (real sign on
this branch) and clip to [-1,1]. Allocate delta among both log estimates,
the marked estimate, and forest failures by a union bound.

The cutoff in Section 2 ensures B_h<4/epsilon whenever this calculation
is needed. Hence h+L=O(log(1/epsilon)), while the existing log-partition
estimator costs polynomial in m and the requested precision. This proves
the claimed degree-independent polynomial bound, conditional on the
written local cluster proof. It is not a practical running-time claim.

## 8. Actual Linear-Decoder Physical Readouts

Let B_phys=[X;Z] label the physical generators, and let the decoder be an
explicit binary matrix D_dec with B_phys D_dec B_phys=B_phys, verified on
generator columns. Do not infer linearity from example outputs.

For a physical Pauli Q with binary label q, the earlier exact partner rule
reduces to y'=y+h with h=D_dec q. If B_phys h != q the expectation is zero.
Otherwise its phase is

    i^p (-1)^(w.y) = tau(P_phys(y+h)^dagger Q P_phys(y)).       (11)

Ordered Pauli multiplication has a quadratic phase, so its difference
under a fixed translation is affine with even linear coefficients modulo
four. Evaluate (11) at 0 and the m unit masks to obtain p and w in
polynomial time. Thus the pullback is ONE coefficient Pauli, not an
exponential sum. All physical signs and Y phases are included.

This proves a classical additive comparator for the ACTUAL decoded
physical Pauli expectations in the entire stated small-degree regime,
including noncommuting generators. It does not assume correct Gibbs
decoding. It does not apply to a general nonlinear or quantum decoder.
For a polynomial-L1 observable use per-term precision epsilon/sum|c_j|
and a union bound. Full measurement-law sampling remains separate.

## 9. Strictly Beyond Polynomial C: An Explicit Family

This is a cost-separation control, NOT an advantage instance. Put g=k^2,
k>=2, and take r cliques of size g. Link successive cliques by one new
connector vertex joined to distinct designated vertices in its two cliques.
Use different attachment vertices within a clique. The graph is connected,
has m=rg+r-1 and maximum degree g. Give clique terms coupling one and
connectors coupling j_c=1/(80*16^3). Set beta=1/(16k), a=1/16.

Then D lambda=(g+1)/(256g)<1/64. With connectors switched off each clique
has H_block^2=gI, so its log sign cost is

    g log cosh(a/sqrt(g)) - log cosh(a) >= a^4/20.

For 0<=x<=1 use
x^2/2-x^4/12 <= log cosh x <= x^2/2-x^4/12+x^6/45.
These follow by integrating x-x^3/3 <= tanh x <= x-x^3/3+2x^5/15;
the derivative bounds follow from tanh x<=x and the lower bound itself.

Restoring the connectors changes log Z by at most beta(r-1)j_c, by the
operator norm perturbation bound for the trace exponential. log Z_commuting
can only increase. Therefore

    log C >= r a^4/20 - beta(r-1)j_c >= r/(40*16^4).          (12)

Take r=k^4: log C grows as Omega(k^4), while log m=O(log k). C is genuinely
superpolynomial, not merely poorly upper-bounded by our old estimator.
The new theorem's regime still holds. Large rows in the receipt are exact
parameter ledgers only; the corresponding graphs/states were NOT built.
This family is deliberately structured and is not asserted classically hard.

## 10. Adversarial Checks And Remaining Scientific Work

Tests must check whole Pauli expectations against independent dense matrices,
not only marginals; odd-Y zeros; disconnected root sets; signed and zero
couplings; noncommuting physical generators; redundant generators; and
decoder outputs that are not Gibbs. Exact finite proposal expectations must
match the ordered-tuple marked expansion, including repeated polymers.
Missing forest/contact/factorial factors must fail explicit controls.

The executable is a small rational reference with exponential guards and
diagnostic draws. It does NOT implement the entire precision-managed
large-instance estimator or certify its short-run mean. Confidence bounds
are an algorithmic proof, not a claim that N large draws were run.

The constructive pilot-preparation problem remains worthwhile, but an
energy-readout advantage with linear decoding is now challenged even beyond
polynomial C. A serious next candidate needs a specific nonlinear/quantum
decoder and useful output, a temperature outside the comparator's scope,
or a coherent/sampling task not reduced to additive Pauli estimation.
Do not infer hardness for any of those remaining cases.
