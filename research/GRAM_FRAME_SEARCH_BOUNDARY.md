# Gram Frame Search Boundary

30 October 2026. Exact algebraic lemmas and finite arithmetic controls, not a
hardness theorem, quantum barrier, compiled receiver, or source-cost decision.
This supplements [the invariant-Gram receiver](INVARIANT_GRAM_REES_RECEIVER.md)
and [the genuine Rees reduction](REES_HSP_REDUCTION.md).

## Minimal Gram Image And Its Quantifiers

Work over F_p, p>3. Let W be a full-row-rank d-by-M matrix, with columns v_i,
row space U, and Phi_W(a)=W diag(a) W^T. Put

    S = image(Phi_W) = span_i {v_i v_i^T}.

**Lemma 1.** dim S >= d. Equality holds exactly when W has a disjoint-support
row basis, equivalently its columns lie on d independent lines, allowing zero
columns. This is also equivalent to one fixed congruence diagonalizing EVERY
matrix in S, before the coefficients or Gram outcomes are known.

Proof: choose d independent columns, forming P, and change row basis by P^-1.
The selected columns are e_1,...,e_d, so S contains all d diagonal units.
If dim S=d, every other v_i v_i^T is diagonal. Its off-diagonal entries are
products of coordinates, so v_i has at most one nonzero coordinate. The
converse is immediate. A fixed simultaneous diagonalizing congruence puts S
inside the d-dimensional diagonal space, forcing equality. This also gives
a constructive chart: select independent columns by elimination and invert P.

The fixed-basis qualifier is essential. For W=[e_1,e_2,e_1+e_2], dim S=3>2,
yet every individual symmetric 2-by-2 Gram outcome is diagonalizable over F_p
by an outcome-dependent congruence. The lemma does not prohibit that operation
or conclude that a particular tuple is not simultaneously diagonalizable.

## Universal Admissible Frame

**Lemma 2.** For every d,r>=1 there is a public frame, independent of the
target tuple, realizing ALL r-tuples in Sym_d(F_p)^r with actual nonzero
vector central labels, while all cubic and central quadratic restrictions
vanish on U. The realization uses M=2*max(d(d+1)/2,r) slots.

Set D=d(d+1)/2. Start with v_j=e_a and v_j=e_a+e_b for a<b. These D rank-one
matrices form a basis because every symmetric Q satisfies

    Q = sum_a (Q_aa - sum_(b!=a) Q_ab) e_a e_a^T
        + sum_(a<b) Q_ab (e_a+e_b)(e_a+e_b)^T.

Pad the list to m=max(D,r) by repeating e_1. Give W the paired columns
(v_j,v_j), and choose nonzero c_j in F_p^r spanning F_p^r, for example cycling
through its coordinate vectors. Set

    beta_(j,+) = ell_(j,+) = c_j,
    beta_(j,-) = ell_(j,-) = -c_j.

Every beta_i and ell_i is a nonzero VECTOR; individual components may vanish.
Both central label matrices have rank r. Equal paired coordinates imply

    B_l(u,v) = sum_i beta_(i,l) u_i v_i = 0,
    T_l(u,v,w) = sum_i ell_(i,l) u_i v_i w_i = 0

for every u,v,w in U and every l. These are full multilinear restrictions,
not just cancellations at chosen generators. Nevertheless

    Q_l = sum_j (alpha_(j,+,l)+alpha_(j,-,l)) v_j v_j^T

is arbitrary: put the displayed decomposition coefficients on plus slots,
zero on minus slots, and zero on padding. W has rank d and dim S=D.

## Genuine Positive-Probability Source

Let L have basis X,Y_l,U_l,V_l, 1<=l<=r, with abelian ideal spanned by all
Y_l,U_l,V_l and brackets [X,Y_l]=U_l, [X,U_l]=V_l. This is an actual
semidirect Lie algebra: X acts by chains Y_l -> U_l -> V_l -> 0. It has
class three, gamma_2=<U_l,V_l>, and gamma_3=<V_l>. Its genuine positive Rees
cover is A=tL + t^2 gamma_2 + t^3 gamma_3, of dimension 1+6r. In G=exp(A),

    N = exp(<t^2 U_l,t^2 V_l,t^3 V_l>),
    Z = exp(<t^2 V_l,t^3 V_l>) <= center(G).

N is abelian normal, with characters (alpha,beta,ell) on these coordinates.
Take h=<X>. Its actual homogeneous lift is K=exp(<tX>), with K intersect N=1;
K is nonnormal. The ordinary hiding-function tuple at three distinct nonzero
evaluation points supplies these mixed K-coset states with three original
queries per lifted source, with evaluation workspace cleaned. No label oracle,
hidden-subgroup advice, or source purification is substituted.

For rho_K=|G|^-1 sum_(k in K) R_k and the full N-character projector Pi_chi,
regular-representation trace orthogonality gives

    Tr(Pi_chi rho_K)
      = |N|^-1 sum_(n in K intersect N) conjugate(chi(n))
      = p^(-3r).

Thus every joint N-character has positive diagonal weight. For M independent
sources, the prescribed central record has probability p^(-2rM). Conditional
on it, all alpha diagonal weights are uniform on F_p^(rM). Since Phi_W is
surjective of rank D, every Gram tuple has conditional probability p^(-rD)
and joint probability p^(-2rM-rD). In particular all tuples in Lemma 2 really
occur. Uniform diagonal weights do NOT make the conditioned state classical
or license measuring individual alpha labels.

For scales s=W^T x, the actual conjugation shift is
alpha_(i,l) -> alpha_(i,l) +/- a*s_i*ell_(i,l). A Gram entry changes by
T_l(w_a,w_b,s)=0. Hence the same full-character Gram projectors are invariant
under the controlled actions, without discarding multiplicity registers.
This checks compatibility with the ideal receiver interface, not its circuit.

## Real Restrictions And Search Scope

For any admissible fixed W, beta^(l) and ell^(l) elementwise-multiplied by
each row of W lie in ker Phi_W. Therefore

    dim S <= M - dim span{beta^(l), ell^(l) * w_a : l,a}.

Frame size and geometry can constrain the image. Lemma 1 identifies the
minimal unrestricted image precisely with the disjoint-support mechanism;
Lemma 2 shows that larger admissible images can be completely general.

Actual support matters independently. For arbitrary homogeneous K, the same
trace formula is uniform on (K intersect N)^perp and zero elsewhere. In the
same L, choosing h=<U_l> gives K=exp(<tU_l,t^2U_l>) and forces alpha=0 while
allowing every beta,ell. All accessible Gram matrices are then zero, even
when dim S=D. The minimal-image necessity cannot be applied to a restricted
source image as though all coefficients were allowed.

A concrete small-frame counterexample over F5 is

    Q_1=diag(1,3,0),  Q_2=diag(0,0,1),
    q_1=x_1^2-2*x_2^2,  q_2=x_3^2.

Each scalar ternary equation has a nonzero zero, but their only common zero
is zero since 2 is nonsquare. Lemma 2 realizes this pair with d=3,r=2,M=12,
all central vectors nonzero, and joint record probability 5^-60. This only
refutes transferring the scalar ternary guarantee to multiple equations.
For d>2r, Chevalley-Warning already guarantees a nonzero common zero for
every homogeneous tuple. Representability neither proves search hardness
in that regime nor transfers hardness of arbitrary affine MQ.

The prescribed sectors can be extremely rare. The construction permits a
public frame chosen from the central record, but does not assert that any
particular frame-selection algorithm outputs it. A receiver can choose a
different frame or charge rare records to an explicit abort allowance. No
average-case hardness, receiver lower bound, or quantum barrier follows.

## Corrected Comparator And Verification

[Ivanyos--Sanselme--Santha, Section 5, Claim 1](https://www.irif.fr/~santha/Papers/iss12.pdf)
gives diagonal quadratic arity (r+1)(r+2)/2, hence six at rank two, not nine.
The scalar cubic sufficient arity is two for p=2 mod3 and three for p=1 mod3:
handle zeros and equal cube classes first; for three distinct classes a,b,c,
the existing `ternary_cubic_scales(p,(a,(-b)%p,c))` returns (1,y,z), whose
reordered (z,y,1) cancels a*z^3+b*y^3+c. Thus the corrected matched sequential
sufficient comparator is **12/18**, superseding 18/36 and 12/24. This is not
an optimality claim or an integrated sequential implementation. Broader
source-cost comparison and CLI/report changes are outside this note.

The self-contained tests check actual modular matrices, rank-one embedding,
full moment cancellation, conjugation covariance, finite Gram fiber counts,
minimal image rank and chart bases, outcome-dependent versus fixed
diagonalization, a matrix realization of L and genuine Rees closure, source
trace support, and the F5 counterexample. They do not execute a quantum
receiver or implement a scalable quadratic solver. Replay without caches:

    env PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /opt/anaconda3/bin/python -B -m pytest -q -p no:cacheprovider -W error tests/test_gram_frame_geometry.py
