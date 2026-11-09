# Independent review: the Legendre spherical kernel

5 November 2026. Read-only mathematical derivation followed by this record.
Sources checked locally: Chen, `chen_cartan_9809209.txt`, Sections 5, 8-11;
and the GL2 QFT toolbox, Equation (8), Section 6.2.2, and Equations
(125)-(130). No numerical spectrum, Git action, or network access was used
in this review. Statements below are identities, not novelty claims.

## Spaces, normalization, and the exact Chen identity

Let p be odd, G=PGL2(F_p), X the unordered pairs of distinct rational
projective points, and Y the unordered Frobenius-conjugate nonrational
pairs. Write n_s=|X|=p(p+1)/2 and n_n=|Y|=p(p-1)/2. Choose a public
nonsquare lambda, base pair x0={0,infinity}, and base quadratic
Q0(u,v)=u^2-lambda*v^2. Their stabilizers H_s,H_n are the split and
nonsplit torus normalizers, of orders 2(p-1),2(p+1), respectively.

For the anisotropic form Q representing a column of Y, put

    T_{ {x,y},Q }=chi(Q(x)Q(y)).

Projective-vector rescaling changes Q(x) by a square. Rescaling Q changes
both signs together. The global sign acquired by a single homogeneous
phase under G therefore cancels in T: this is an ordinary G-intertwiner.
The normalized off-diagonal two-copy state is T|Q>/sqrt(n_s). Its preceding
off-diagonal projection succeeds with probability p/(p+1).

Let M be Chen's 0/1 incidence matrix from Y to X: M_{R,Q}=1 when the two
rational lines of R are orthogonal for the polar bilinear form of Q.
It is his N' N correspondence. Each column is a perfect matching on
P1, with (p+1)/2 edges; each row has (p-1)/2 incidences. Let D be Chen's
symmetric split-pair adjacency N sigma_{-1} N. The neighbors of x0 are
exactly {a,-a}, for a in F_p^*/{+/-1}. Let J_XY denote the rectangular
all-ones matrix. Then

    T = 2 D M - J_XY.                                      (A)

Proof: normalize a column to Q=u^2+buv+cv^2. At row x0, T=chi(c).
The pair {a,-a} is Q-orthogonal exactly when c-a^2=0. Since Q is
anisotropic, c is nonzero; consequently (DM)_{x0,Q}=(1+chi(c))/2.
Equivariance proves (A) at every row. This identifies OUR kernel with a
specific combination of Chen's correspondences; merely citing his
isogeny theorem would not have established this identity.

Chen's Propositions 5.3-5.4 give multiplicity-free modules

    C[X] = C[Y] direct-sum St.

One can also prove multiplicity-freeness because every orbital on either
pair space is self-paired: a projective involution exchanges two pairs;
for conjugate pairs that involution is Frobenius-fixed. All orbital
matrices are symmetric, so their algebra is commutative. The absent St
sector is directly visible: each column has vertex-star sum -1, and is
orthogonal to all differences of vertex stars.

For a nontrivial common irreducible rho, let d_rho be the real eigenvalue
of D. Chen's operator relations give the M squared singular value
p-d_rho^2. Thus (A) gives

    singular_value_rho(T)^2 = 4 d_rho^2 (p-d_rho^2).          (B)

On the trivial sector the squared singular value is (p^2-1)/4; on the
extra St sector the adjoint kernel is zero. In particular ||T||<=p.
This bound is a mathematical normalization statement, not by itself an
implemented block encoding.

## Principal vectors and the scalar INCLUDING its phase

Use I_{alpha,alpha^{-1}}, where alpha(-1)=1 and alpha^2!=1, in the
toolbox's projective-point model. The normalized fixed vectors are

    v_s(x)=alpha(x)^(-1)/sqrt(p-1), x!=0,infinity;
    v_s(0)=v_s(infinity)=0;
    v_n(x)=alpha(x^2-lambda)^(-1)/sqrt(p+1), x finite;
    v_n(infinity)=1/sqrt(p+1).

Choose beta^2=alpha and define the Jacobi sum
J_beta=sum_z beta(z)chi(1-z), with characters extended by zero at zero.
Then |J_beta|=sqrt(p), and Chen's principal D eigenvalue is

    d_alpha = beta(-1) Re J_beta.                          (C)

Indeed substitute u=x^2 into (1/2)sum_x alpha(x)chi(1+x^2), and use
J(beta chi,chi)=chi(-1) conjugate(J_beta).

Define mu=(sqrt(p^2-1)/2)<v_s,v_n>. Its exact value is

    mu = (1/2)sum_(x!=0) alpha(x/(x^2-lambda))
       = (1/2)beta(lambda)^(-1)
           [J(beta,beta^(-2))-J(beta chi,beta^(-2))]
       = i beta(-1) beta(4lambda)^(-1) Im J_beta.           (D)

For the last equality use J(A,A)=A(4)^(-1)J(A,chi), the usual Gauss
quotient identity, and the conjugation relation used in (C). These
identities apply because beta, beta chi, and alpha are nontrivial.
Changing beta to beta chi leaves (C)-(D) unchanged. In particular the
phase is specified; an absolute-value formula would be insufficient.

The toolbox's Equation (8) fixes the positive matrix-entry convention

    F_G|g> = sum_rho sqrt(dim(rho)/|G|)
                    sum_ij rho(g)_ij |rho,i,j_dual>.

For a uniform left coset gH, a rank-one invariant space therefore gives
carrier vector rho(g)v_H and RIGHT DUAL vector conjugate(v_H). The latter
must be unprepared/prepared, including conjugation of its coordinates in
the published GT basis. Conjugating only the projective-point phases
while retaining an unconjugated GT change of basis is not the same map.

Let S_H denote the resulting carrier-only spherical transform. Since
|H_s intersection H_n|=4, the coset-embedding overlap is

    E_s^dag E_n = [2/sqrt(p^2-1)] M.

Its right-dual overlap is <conjugate(v_s),conjugate(v_n)>, hence under
this convention S_s M S_n^dag has scalar conjugate(mu). Consequently

    tau_alpha := (S_s T S_n^dag)_alpha
       = conjugate{ beta(4lambda)^(-1)
                     [J_beta^2-conjugate(J_beta)^2]/2 }.   (E)

Thus the ADJOINT receiver coefficient, rather than the forward one, is

    conjugate(tau_alpha)/p
      = beta(4lambda)^(-1) [z_beta^2-conjugate(z_beta)^2]/2,
    z_beta=J_beta/sqrt(p).                                 (F)

This is the half-difference of two unit phases. Each z_beta is the product
of the normalized Gauss phases for beta and chi and the inverse phase for
beta chi. A two-branch LCU therefore gives (F) with constant normalization;
it is not polar inversion or a small-singular-value approximation.
All phases of the controlled fixed-vector preparations must follow the
explicit vectors above. Common per-irrep phases of the same group QFT
cancel between the two spherical transforms.

## Full rank is true, but supplies no useful lower spectral gap

For completeness, the additional possible zero d_rho=0 in (B) can be
excluded for prime p. In principal sectors, (C) expresses d_rho as the
real part, up to sign, of a magnitude-sqrt(p) Jacobi sum in Q(zeta_(p-1)).
The same expression with alpha=chi gives the twisted Steinberg sector
when p=1 mod4: the complementary determinant constituent has no H_s-fixed
vector, so averaging the reducible principal character gives this scalar.

For a selected cuspidal theta, trivial on F_p^*, choose beta^2=theta on
F_(p^2)^*. The normalizer parity implies beta restricted to F_p^* is chi.
Put

    W_beta=G_(p^2)(beta)/tau_p
          =sum_(Tr(z)=1) beta(z).

It has magnitude sqrt(p) and lies in Q(zeta_(p^2-1)). Substituting z=gamma^2
in Chen's Soto-Andrade expression and using
beta chi_(p^2)=beta^(-p) gives d_theta=-Re W_beta. If either relevant
real part vanished, its magnitude condition would put sqrt(-p) in that
cyclotomic field; if its absolute value equaled sqrt(p), it would put
sqrt(p) there. Both are impossible since p is unramified in a cyclotomic
field whose conductor is prime to p. Thus 0<d_rho^2<p for every nontrivial
common sector. T has full column rank. This argument gives NO polynomial
or inverse-polylogarithmic lower bound on its smallest singular value.

## Scoped exact scalar control

After the derivation, one predeclared Sage cyclotomic-field control used
p=7,11,13, the first positive nonsquare lambda, and every inverse-pair
representative of a nondegenerate even principal character. There were
five labels in total: exponents 2 at p7; 2,4 at p11; and 2,4 at p13,
relative to Sage's public multiplicative generator. No instance or
character was selected after observing its result.

The control built the induced action from the actual matrices
t_x=[[x,1],[1,0]] and t_infinity=I: for g and x it computed
b=t_(gx)^(-1) g t_x and applied alpha(b_11/b_22). It then checked the
WHOLE-VECTOR identities, with unnormalized v_s_raw and v_n_raw,

    sum_R M_(R,Q0) rho(g_R) v_s_raw = conjugate(mu) v_n_raw,
    sum_R T_(R,Q0) rho(g_R) v_s_raw = tau_alpha v_n_raw.

All 120 coordinate equalities passed exactly, together with (C)-(F),
|J_beta|^2=p, and |mu|^2=p-d_alpha^2. Dropping the required conjugation
failed in four of the five labels; the p13 exponent-2 scalar happens to be
real, so that particular label does not distinguish the two conventions.
The single run completed in 0.123 seconds. These are finite algebra and
phase controls, not a spectrum sweep or an implemented quantum receiver.

## Exact matched-filter receiver identity and remaining review boundary

Let P select only principal sectors. Suppose the charged partial spherical
transforms and their controlled dual-vector preparations are supplied in
the convention above. Apply S_s, the flagged LCU (F), then S_n^dag to the
native input T|Q>/sqrt(n_s). Write

    A_pr = sum_(rho principal) dim(rho) |tau_rho|^2.

The joint amplitude for LCU success and the correct output Q is exactly

    A_pr / [p n_n sqrt(n_s)],

and its joint probability is the square of that number. This follows
because each central projector has diagonal dim(rho)/n_n on the
transitive Y basis; the adjoint coefficient yields a positive |tau|^2 sum.
Using the forward coefficient instead would give tau^2 and can cancel.
No polar transform, lower bound on individual singular values, or
postselection renormalization is needed for this identity.

Conditional on a separately proved mass estimate
A_pr=p^4/8+O(p^(7/2)), the displayed joint probability tends to 1/8.
This review has NOT checked that mass estimate or the complete reversible
coset/GT circuit implementation. Those are separate claim gates. The
identities here provide neither a standalone implemented decoder nor a
novelty, hardness, or classical-separation claim.
