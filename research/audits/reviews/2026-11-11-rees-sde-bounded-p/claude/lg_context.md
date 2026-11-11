# Context: label-set gadgets for the diagonal power-residue zero-sum problem (self-contained)

Problem. p prime, kappa >= 2 with kappa | p-1, P = {x^kappa : x in F_p^*} (index kappa in F_p^*),
S = P u {0}. Given columns v_1..v_M in F_p^a (worst case), find a nonzero x in S^M with
sum x_i v_i = 0. A "piece" is a set X of columns (in a quotient space V); D(X) = {c in F_p^X :
sum c_i v_i = 0}, k = dim D(X). Fix a basis delta^1..delta^k of D(X); the label of column i is
l_i = (delta^1_i, ..., delta^k_i) in F_p^k. Labels of columns not in any dependency are 0 (ignored).
The nonzero labels span F_p^k. R(X) = { sum y_i v_i : y in S^X }.

Fact used throughout (elementary): for lambda notin P, S cap lambda S = {0}. A nonzero linear
functional on a line F_p^* u takes every value of F_p^*, so it is not S-valued (kappa >= 2).

Lemma 2 (repo, proved). X realizes a d-dimensional subgroup <h_1..h_d> by S-weights (all p^d
elements) iff there are Phi_i in S^d (i in X) and gamma_alpha in F_p^k (alpha in F_p^d \ 0) with
    y_alpha(i) = <alpha, Phi_i> + <gamma_alpha, l_i>  in S   for all alpha != 0, i in X,
and the realized vectors alpha.h are nonzero... More precisely the repo uses: a family is
FEASIBLE if all y_alpha(i) in S; WEAKLY NONDEGENERATE if for every projective direction [alpha]
some lambda alpha (lambda in F_p^*) has y_{lambda alpha} not identically 0 on X. (A) feasible +
weakly nondegenerate => X gains d dimensions or yields an S-witness. (B) If X realizes a
d-dim subgroup then a feasible weakly nondegenerate family exists. Phi may be chosen per label
(the decision problem is about the label SET L = {l_i}); "L is d-feasible" means such a family
exists with Phi a function of the label.

Lemma R (repo, proved). WLOG gamma_{lambda alpha} = lambda gamma_alpha for lambda in P.
Lemma Q + Lemma N (repo, proved). Let L span F_p^k and have no nonzero S-valued linear
functional. In every feasible family, direction [alpha] is degenerate iff gamma_{r alpha} =
r gamma_alpha (r notin P fixed). Hence nondegeneracy depends on gamma only, and WLOG Phi is
P-equivariant in the label (Phi(lambda l) = lambda Phi(l), lambda in P).

Finite inputs (repo): for kappa = 2 the full planar set F_p^2 \ 0 has no weakly nondegenerate
2-family at p = 7, 11 (CaDiCaL UNSAT with LRAT proofs checked by a fixed checker; the p = 7 and
p = 11 runs are for the nested planar set {l : l_1 != 0}, a subset of the full set) and at p = 13
(CaDiCaL UNSAT, proof not yet checked). It does have one at p = 5 (explicit model). At p = 3
(S = {0,1}) the full planar set has none.

# Claims to be checked

Notation. For a d-family (y_alpha) on a label set L, and alpha in F_p^d, put y_0 = 0. The map
alpha -> [y_alpha] in F(L)/Lin(L) (F(L) = all functions L -> F_p, Lin(L) = restrictions of
linear functionals) is linear because y_alpha - sum_j alpha_j y_{e_j} is in Lin(L). Its kernel
K(L) is a subspace of F_p^d.

Lemma K. If L has no nonzero S-valued linear functional, then K(L) = {alpha : y_alpha = 0 on L},
and the family is weakly nondegenerate iff K(L) = 0.
Proof: alpha in K(L) iff y_alpha|L is linear; it is S-valued, so it is 0. K(L) is a subspace, so
lambda alpha in K iff alpha in K.

Lemma V (vanishing). Let L span F_p^k and have no nonzero S-valued linear functional, and fix a
feasible family with Lemma R normalization. For alpha != 0 put Delta_alpha = gamma_{r alpha} -
r gamma_alpha. Then y_alpha(l) = 0 for every l in L with <Delta_alpha, l> = 0, and for a full line
F_p^* u contained in L, K(F_p^* u) = {alpha : <Delta_alpha, u> = 0} (as a set it is a subspace).
Proof: y_{r alpha} - r y_alpha = <Delta_alpha, .> since <r alpha, Phi> = r <alpha, Phi>. Where
<Delta_alpha, l> = 0: y_alpha(l) in S cap r^{-1} S = {0}. On a full line: if <Delta_alpha,u> = 0 then
y_alpha vanishes on the line; conversely if y_alpha vanishes on the line, so does y_{r alpha}
(K is a subspace) and then <Delta_alpha, u> = 0.

Lemma 1 (lines, kappa = 2). For a full line l_u = F_p^* u in L and any d-family, codim K(l_u) <= 1.
Proof: otherwise choose an injective linear B: F_p^2 -> F_p^d with B(F_p^2) cap K(l_u) = 0; then
(y_{B beta})_beta is a 2-family on l_u (Phi'(l) = (y_{Be_1}(l), y_{Be_2}(l)) in S^2) whose kernel
is B^{-1}(K) = 0, hence weakly nondegenerate on the label set F_p^* (k = 1). By Lemma Q/N one may
take Phi' P-equivariant; then every y'_beta is a P-equivariant function on F_p^*, a 2-dimensional
space (kappa = 2) containing the 1-dimensional Lin; so the rank is <= 1, a contradiction.

Theorem LG (kappa = 2). Let L in F_p^k \ 0 and let FL be the set of full lines (lines through 0
whose nonzero points all lie in L). Suppose FL spans F_p^k and, for every two distinct u, w in FL,
the planar section L cap span(u, w) (as a label set in that plane) has no weakly nondegenerate
2-family. Then every d-family on L (any d) has K(L) of codimension <= 1; in particular for d >= 2
it is not weakly nondegenerate, and no piece whose label set is L realizes a 2-dim subgroup or
contains an S-witness.
Proof. L has no nonzero S-valued functional (it would vanish on each full line, and FL spans), so
Lemma K applies to L and to every section containing two independent full lines. For u in FL let
K_u = K(l_u), codim <= 1 (Lemma 1). For u != w in FL, W = span(u, w): restricting gives a d-family
on L cap W with K(L cap W) subset of K_u cap K_w. If codim K(L cap W) >= 2, reparametrizing as in
Lemma 1 gives a weakly nondegenerate 2-family on L cap W, excluded. So codim(K_u cap K_w) <= 1,
hence any two K_u that are hyperplanes coincide: there is a hyperplane H of F_p^d with H subset of
K_u for every u in FL. For 0 != alpha in H, y_alpha = 0 on every full line. For lambda in F_p^*,
g = y_{lambda alpha} - lambda y_alpha is linear, equals y_{lambda alpha} on full lines, hence is an
S-valued linear functional on each full line, hence 0 there, hence g = 0 (FL spans). So
y_{r alpha} = r y_alpha on L, giving y_alpha in S cap r^{-1}S = {0}: direction [alpha] is degenerate.
The last clause: an S-witness supported in X is an S-valued functional on L (zero here), and a
realized 2-dim subgroup gives a weakly nondegenerate 2-family by Lemma 2(B), Lemma N.

Corollary 1. If F_p^2 \ 0 has no weakly nondegenerate 2-family, then for every k >= 2 and every d >= 2
no piece with label set F_p^k \ 0 gains 2 dimensions; same for the nested sets {l : l_1 != 0} if the
nested planar set has none (a plane spanned by two lines off {l_1 = 0} meets the nested set in a
nested planar set). So p = 7, 11 (and 13 if certified): full and nested label sets give at most
one dimension per piece, for every number k of dependencies.

Theorem LG_R (general rank, kappa = 2). Let L be F_p^*-closed... For any d-family on a set L whose
full lines span, rank(L) := codim K(L) equals dim of sum over u in FL of K_u^perp (each of dim <= 1,
so these are points n_u). If rank(L) >= R, choose R full lines with independent n_u; their span W
has dim R and the restricted family has rank R on L cap W. Hence: if F_p^R \ 0 has no weakly
nondegenerate R-family, then for every k, F_p^k \ 0 has no family of rank >= R. (Used at p = 5,
R = 3: F_5^3 \ 0 is certified infeasible for d = 3.) [Note: K(L) = intersection of K_u needs
"y_alpha = 0 on L iff on every full line", true when L is a union of full lines.]

Corollary 2 (pool labels). If a pool of columns has the full label set F_p^r \ 0 (each nonzero
vector of F_p^r occurs as the label of some column w.r.t. a basis of D(pool)), then for every
sub-piece X of the pool, the nonzero labels of X w.r.t. a basis of D(X) form the full set
F_p^{k} \ 0, k = dim D(X). Sketch: D(X) corresponds to M_X = span(labels of pool columns outside
X)^perp; the labels of X are the images of the pool labels in X under F_p^r -> F_p^r / U,
U = span(labels outside X); every point outside U is a label in X (labels outside X lie in U), so
the images cover (F_p^r/U) \ 0.
