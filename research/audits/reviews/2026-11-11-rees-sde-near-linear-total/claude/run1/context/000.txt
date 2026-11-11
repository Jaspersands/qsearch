# Claims to audit (diagonal SDE, total regime). Author: one AI session, 2026-11-11. Unreviewed.

## Setting

kappa >= 2, p prime with p = 1 mod kappa, P = (F_p^*)^kappa (index kappa), P0 = P u {0} = {y^kappa : y in F_p}.
A bank is a list of columns lambda_1..lambda_n in F_p^d (repetitions allowed). A solution is a
nonzero x in P0^n with sum_i x_i lambda_i = 0. A bank is *dead* if it has no solution.
cone(B) = {sum x_i lambda_i : x in P0^n}. Rescaling one column by an element of P bijects
solution sets. N(kappa, d, p) = least n such that every bank of n columns in F_p^d has a
solution. Chevalley-Warning (CW): N <= kappa d + 1. Dead pair: (mu, c mu) with -c not in P
(dead because x mu + y c mu = 0 forces x = -c y). d dead pairs on a basis give 2d dead
columns, so N >= 2d + 1 for every kappa >= 2, every p.

Tools used:
- (Gauss) For c != 0, S(c) := sum_{y in F_p} e_p(c y^kappa) satisfies |S(c)| <= (kappa-1) sqrt(p); S(0) = p.
- (Lemma W, from an earlier repo report) For e <= p pairwise distinct offsets beta_1..beta_e in F_p and
  any classes eps_b in Z_kappa, #{s in F_p : s + beta_b in g^{eps_b} P for all b}
  >= kappa^{-e} (p - e - (kappa^e - 1)(e - 1) sqrt(p)). (Weil, expanding each indicator in characters.)

## Claim 1 (Theorem E, polynomial-prime threshold)

Let eta > 0, and let B be a bank of n0 > (2+eta) d columns in F_p^d, n0 <= floor((2+eta)d) + 1. Suppose
p^{eta/(2(2+eta))} >= 2(kappa-1) n0. Then B has a solution.

Proof. If a column is 0, done. Let T be a sub-bank maximizing |T|/rk(T) (densest); delta := |T|/rk T
>= n0/d > 2+eta; write n = |T| <= n0, D = rk T, and identify span(T) with F_p^D. For every T' subset T with
rk T' < D: |T'| <= delta rk T' (T densest; also for T' empty). Count
N := #{y in F_p^n : sum_i y_i^kappa lambda_i = 0} = p^{-D} sum_{u in F_p^D} prod_{i in T} S(<u, lambda_i>).
u = 0 gives p^{n-D}. For u != 0 let z(u) = #{i : <u, lambda_i> = 0}; then
|prod| <= p^{z} ((kappa-1) sqrt p)^{n-z}. With A = sqrt(p)/(kappa-1) >= 1 and the identity
A^{z(u)} = sum_{T' subset Z(u)} (A-1)^{|T'|}:
sum_{u != 0} A^{z(u)} = sum_{T'} (A-1)^{|T'|} (p^{D - rk T'} - 1) <= sum_{T': rk T' < D} A^{|T'|} p^{D - rk T'}.
Hence |N - p^{n-D}| / p^{n-D} <= sum_{T': rk T' < D} (kappa-1)^m p^{c - m/2}, with m = n - |T'|,
c = D - rk T'. Densest gives m >= delta c, so m - 2c >= (1 - 2/delta) m = (eta'/(2+eta')) m with
eta' = delta - 2 >= eta, so each term <= x^m, x := (kappa-1) p^{-eta/(2(2+eta))} <= 1/(2n).
Sum <= (1+x)^n - 1 <= e^{1/2} - 1 < 0.65. So N >= 0.35 p^{n-D} > 1 and some y != 0 solves; x = y^kappa
(coordinatewise) is a solution of T, extended by zeros to B. QED.
Corollaries claimed: (a) eta = 1: every bank of 3d+1 columns has a solution once p >= (2(kappa-1)(3d+1))^6.
(b) A random kernel vector of T is a solution with probability >= 0.35 kappa^{-n} - p^{-(n-D)}, so a Las
Vegas algorithm runs in expected kappa^{(2+eta)d+1} poly time (T found by parametric submodular
minimization of delta*rk - |.|).

## Claim 2 (exact threshold 2d+1 at exponential primes)

If p > (2kappa-2)^{4d+2}, every bank of 2d+1 columns in F_p^d has a solution; so N(kappa, d, p) = 2d + 1.
Proof: take T densest as above (n = |T| <= 2d+1, delta = n/D > 2). Group u != 0 by the flat
W(u) = span{lambda_i : <u,lambda_i> = 0} (a proper flat of span T, of dim w, containing n_W columns of T,
and u in W^perp, at most p^{D-w} choices). Densest gives n - n_W >= delta (D - w) > 2(D-w), so
n - n_W >= 2(D-w)+1. Relative error <= sum_W ((kappa-1)/sqrt p)^{n-n_W} p^{D-w}
<= sum_W (kappa-1)^{2(D-w)+1} p^{-1/2} <= (2^n - 1)(kappa-1)^n p^{-1/2} < 1 - 2^{-n} once
sqrt(p) >= (2(kappa-1))^n; and p^{n-D} 2^{-n} > 1. (Uses sqrt p >= kappa-1 to replace n - n_W by its minimum.)

## Claim 3 (Lemma DC: dead implies covering)

If every bank of 2u+1 columns in F_p^u has a solution, then every dead bank D of 2u columns in F_p^u has
cone(D) = F_p^u. Proof: for v != 0, D u {-v} has a solution; D dead forces x_{-v} in P, and dividing by
x_{-v} gives v in cone(D).

## Claim 4 (Lemma R: reduction to strictly sub-critical banks)

Call a bank of 2d+1 columns spanning F_p^d *strictly sub-critical* (ssc) if every subspace U with
1 <= dim U <= d-1 contains at most 2 dim U - 1 of its columns. Let p >= kappa^4. If every ssc bank of
2d'+1 columns in F_p^{d'} has a solution for all d' <= d, then every bank of 2d+1 columns in F_p^d has one.
Proof (strong induction on d). d = 1: three nonzero c1,c2,c3: need x1, x2 in P with
x1 + c3/c1 in -(c2/c1) P: Lemma W with e = 2 (offsets 0 and c3/c1 distinct) gives a solution for p >= kappa^4.
d >= 2, bank B, |B| = 2d+1: zero column or B not spanning -> trivial/induction.
(A) some proper U has >= 2 dim U + 1 columns: induction inside U.
(B) else, some proper U (u = dim U >= 1) has exactly 2u columns (tight; includes proportional pairs).
  D = B cap U. Project B \ D to F_p^d / U: 2(d-u)+1 columns, none zero (else U would hold 2u+1).
  Induction gives nonzero xbar on B \ D with w := sum xbar_i lambda_i in U. Induction in U on D u {w}
  gives nonzero (y_D, y_w). If y_w = 0, y_D solves D. Else x_D = y_D / y_w has sum x_D lambda = -w, and
  (x_D, xbar) solves B (nonzero since xbar != 0).
(C) else B is ssc: hypothesis.
Algorithmic version: cases (A)/(B) are detected by submodular minimization of 2 rk(T) - |T| over T subset
B \ {e} (for each column e; every proper flat misses some column), plus minimal minimizers containing a
given column g to find tight proper flats; recursion tree has <= d leaves. So worst-case SDE at
(d, 2d+1) Turing-reduces in poly time to ssc instances (kappa = 2: CW makes the hypothesis true).

## Claim 5 (Prop L*: unused padding is useless)

Assume N(kappa, d', p) = 2d'+1 for all d' <= a. Let B u G be a bank in F_p^a with >= 2a+1 columns such
that no solution has x_G != 0 ("G unused"), and let U = span(G), u = dim U. Then G is dead, |G| <= 2u,
and the projection Bbar of B to F_p^a / U has >= 2(a-u)+1 columns (a total instance). If |G| = 2u, every
solution xbar of Bbar has sum xbar_i lambda_i = 0 exactly (else Lemma DC gives a solution using G), so the
solutions of Bbar are solutions of B: the padding added nothing.

## Claim 6 (TFNP placement, pigeonhole)

If -1 in P and n >= a log2(p) + 1, every bank of n columns in F_p^a has a {0,+-1} solution (collision of
two 0/1 combinations, since 2^n > p^a), and the search problem Karp-reduces to the PWPP-complete problem
COLLISION (circuit {0,1}^n -> {0,1}^{n-1}: encode Lambda x in [0, p^a) <= 2^{n-1} in base p).

## Data (exact, small)

- Character identity N = p^{-D} sum_u prod S verified exactly on 98 small banks; relative error always below
  the Claim 1 sum (which is vacuous at these p).
- Max dead size in F_p^2, exhaustive: kappa = 3: 5 at p = 7, 4 at p = 13..67. kappa = 4: 6 at p = 13, 5 at
  p = 17.
- A dead strictly sub-critical bank of 7 columns in F_13^3 exists for kappa = 3 (brute force over all
  5^7 vectors of P0^7): N(3,3,13) >= 8 although N(3,2,13) = 5.
