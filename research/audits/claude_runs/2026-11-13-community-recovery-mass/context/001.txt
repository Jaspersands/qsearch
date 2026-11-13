Already independently checked native classical proof excerpt; charge these premises exactly, not the old original source guide.

the deliberately enormous explicit constant C=2^300 gives

    Pr(||T||>C sqrt(D ell))
       <=2N (18/(d C^2))^t <=2n^(-2ell).                  (5)

Indeed ln(d C^2/18)>384. All sufficiently-large-n conditions are explicit
scalar inequalities depending only on fixed d. No empirical constant,
unproved small-n claim, Poissonization, normalized matrix or degree
concentration is used. This proves the needed log removal directly.

## 3. Independent-copy symmetrization: no actual Z required

Let theta_E be ANY independent-Bernoulli success probabilities, and define
    H=sum_E (Y_E-theta_E) A_E.
Take an independent copy Y' solely in the proof. Convexity of the
Schatten-2t norm to its 2t power gives, conditioning first on Y,

    E Tr(H^(2t))
       <= E Tr((sum_E (Y_E-Y'_E) A_E)^(2t)).               (6)

Each difference is 0 or +/-1. Conditional on the entire unsigned support,
its nonzero signs are independent fair signs. Thus (4)--(5) apply uniformly
to every support; averaging introduces no loss. Equation (5) holds for H.
This is valid conditional on EVERY planted label vector, even though the
theta_E differ across edges. No covariance approximation is used.

Under the null theta_E=q and H=A. Under planting
    A=epsilon M_x+H,  M_x=sum_E f_x(E) A_E.
The alternative actual Y-Z proposal also satisfies (5) under the null,
since its support is Bern(2q(1-q)) and its signs are fair conditionally.
It is unnecessary once (6) is used. In particular the native algorithm
neither requests nor fabricates a second statistical instance.

## 4. All-label planted witness on the SET slice

This pays the multicommunity signal without a Boolean gauge or block-slice
invariance claim. Fix any community c and let
    w_a(i)=1[x_i=a]-1/k,  v0=(w_c/||w_c||)^tensor(ell).
For every label vector, ||w_c||^2>=n/k^2 and |w_c(i)|<=1.
On the full ordered tensor space define the PSD lift

    B_lift=sum_(J subset [ell], |J|=d) sum_a
              (tensor_(j in J) |w_a><w_a|) tensor I_(J complement).

Its norm is at most k binom(ell,d)n^d. Retaining community c alone gives
    <v0,B_lift v0>>=binom(ell,d)n^d/k^(2d).                (7)

Let Pi be collision-free projection. Each coordinate marginal of v0 has
maximum mass <=k^2/n, so
    1-||Pi v0||^2 <= binom(ell,2)k^2/n.
The normalized v=Pi v0/||Pi v0|| satisfies
    ||v-v0||<=k ell/sqrt(n).
It is fully symmetric under all ell coordinate permutations.

Let K_x be the ORDERED native matrix with coefficient f_x(E) when exactly
d positions change, with all 2d changed vertex labels distinct, and zero
otherwise. It is not literally Pi B_lift Pi. For each row and choice of J,
an unwanted term must place one new vertex in the old J vertices, giving
at most d^2 n^(d-1) assignments, each of magnitude at most k. Symmetry and
the row-sum bound therefore give

    ||Pi B_lift Pi-K_x||<=k d^2 binom(ell,d)n^(d-1).       (8)

By (7)--(8),
    <v,K_x v> >= binom(ell,d)n^d
          [k^(-2d)-2k^2 ell/sqrt(n)-k d^2/n].             (9)
For ell=o(sqrt(n)) the bracket is eventually at least k^(-2d)/2,
uniformly over all labels. This supplies a concrete sufficient-n condition.

Define the genuine isometry from the ell-SET slice by
    W|S>=(ell!)^(-1/2) sum_(orderings of S) |ordered S>.
Every legal set transition has exactly d! ordered target lifts for each
ordered source. Therefore, EXACTLY,
    W* K_x W=d! M_x.                                    (10)
Since v is symmetric, z=W*v is a unit vector. Using
D<=binom(ell,d)n^d/d!, equations (9)--(10) yield

    <z,M_x z> >= D/(2k^p).                              (11)

This vector is an analysis witness only. The algorithm never learns c,
x, w_c or z. In particular (10) does not conflate the ell-set isometry W
with the p-block isometry J in the earlier guide certificate.

## 5. Detection and completely finite integer clock
