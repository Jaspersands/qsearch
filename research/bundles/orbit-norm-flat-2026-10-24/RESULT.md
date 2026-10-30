# Classical Norm-Flat Completion Of High-Rate Cubic Orbits

2026-10-24. LOCAL UNREVIEWED PROOF. This is a stronger classical falsifier
on the EXISTING anisotropic cubic-orbit relation, not a new oracle task.
It does not establish novelty, solve the lower-rate candidate, or construct
a quantum algorithm. The previous pass's formal Rees work is unrelated.

## Decision And Exact Scope

For M disjoint ordered three-point orbits over F_p, keep the original
public nonsquare nu, nonzero b_i, explicit halfsets F_i, and output ONE
polynomial P of degree<n=3K. Write its orbit values as (x_i,y_i,z_i).
The exact predicates remain

    z_i + b_i*(x_i^2-nu*y_i^2) in F_i.

Set r=3M-n, d=M-r=n-2M, k=floor((d+1)/2), D=2k. For 1<=r<M and D>=r,
the algorithm below returns a perfect native polynomial in expected
polynomial time for EVERY fixed valid input. One complete attempt fails
with probability at most

    (p^r-1)/((p-1)*p^D) < 1/((p-1)*p^(D-r)).

The guarantee uses independent uniform algorithm coins, not random inputs
or a population average. All failed centers are paid. Full interpolation
r=0 is already trivial and is not presented as an attack result.
Asymptotically the sufficient rate is R=n/(3M)>=5/6, with the exact even
dimension condition above taking precedence at finite sizes.

The existing ideal quantum perfect-search derivation applies for R>2/3.
This attack removes its high-rate region as advantage evidence, not the
whole range. The saved p12289,M4096,n9828 example has r2460,d1636,D1636:
the gate FAILS. It is unresolved by this attack, not hard or unsatisfiable.
The old native p2053,n204 low-rate score comparison is also not settled.

## Exact Parity Representation

Let a range over ALL N=3M original evaluation points. Put

    A(X)=product_a (X-a),  h_a=1/A'(a),
    H_(j,a)=h_a*a^j,  0<=j<r.

These are the actual generalized-RS parity checks: a word is the evaluation
of a polynomial of degree<n exactly when H word=0. This follows from
Lagrange interpolation and the leading-coefficient identity. No random
matrix or supplied polynomial replaces the original code.

Separate H into Hx,Hy,Hz at the first, second and third orbit points.
Pick ANY fixed t_i in F_i, for example the least element. The problem is
equivalent to finding x,y with

    Hx*x + Hy*y + Hz*(t-b*(x^2-nu*y^2)) = 0.

This is the earlier exact structured MQ representation. The new step is
a public common quadratic-zero subspace for THESE equations, followed by
a fixed-instance full-rank probability proof.

## Public Norm Subspace

Let c_i be the last point in each orbit and

    B(X)=product_i (X-c_i),  delta_i=1/B'(c_i).

Work algebraically in E=F_p[theta]/(theta^2-nu), with conjugation bar(theta)
=-theta and norm N(x+theta*y)=x^2-nu*y^2. Pick g_i in E with

    N(g_i)=delta_i/(h_(c_i)*b_i).

The targets are nonzero. Norm surjectivity guarantees a preimage. The
reference deterministically enumerates at most p candidate y values using
a square lookup table. This O(Mp) work is paid and is polynomial in the
EXPLICIT table-input size; it is not claimed polynomial in log p alone.
No polynomial norm-factorization promise or hidden norm root is supplied.

Define U={ (g_i*Q(c_i))_i : Q in E[X], deg Q<k }. It has F_p dimension D=2k.
For any Q, Q*bar(Q) has base-field coefficients and degree<=2k-2<=d-1.
Consequently each parity moment of the quadratic part is

    sum_i h_(c_i)*c_i^j*b_i*N(g_i*Q(c_i))
       = sum_i delta_i*c_i^j*(Q*bar(Q))(c_i) = 0.

The final identity holds since j+2k-2<=r+d-2=M-2. Thus ALL r quadratic
forms vanish identically on U, including their polarized cross terms.
Anisotropy of each individual block does not prevent this global
cancellation AFTER parity checks. This is not a local accepted affine line.

## Affine Completion And Fixed-Input Probability

Sample a center w0=(x0,y0) uniformly from F_p^(2M), independently on every
attempt. Restrict w=w0+u, u in U. Because the quadratic part vanishes on U,
the r equations in the D coordinates of u are now LINEAR. The linear terms
Hx,Hy and the target t are retained, not discarded by homogeneous reasoning.
If the coefficient matrix J(w0) has full row rank, it solves EVERY right
hand side, even one depending on w0. Gaussian elimination gives u. Set
z=t-b*N(w), interpolate the original word, check degree<n, and independently
replay every original predicate by Horner evaluation.

For any nonzero dual vector lambda in F_p^r, the weighted quadratic form
has coefficients h_(c_i)*b_i*f_lambda(c_i), where deg f_lambda<r.
Its nonzero support has size at least M-r+1=d+1>=k. Restriction of U to
that support is injective: a degree<k extension polynomial cannot vanish
there. The associated norm polar form is nondegenerate on those blocks,
since p is odd, nu and b_i are nonzero, and the weights there do not vanish.

Therefore the map from the uniform center to lambda^T J(w0), a vector in
F_p^D, has rank D. Its deterministic linear offset does not affect
uniformity. The probability that this vector is zero is exactly p^(-D).
Rank failure means some nonzero lambda annihilates J. Proportional lambda
give the same event, so a union bound over (p^r-1)/(p-1) projective vectors
gives the stated bound. No independence between those events is assumed.

This remains true for arbitrary fixed b_i, fixed halfsets and fixed chosen
t_i. It is not an amplification of an IID-input population bound. Under
uniform independent centers T attempts fail with probability at most
delta^T, delta=1/((p-1)*p^(D-r)). Rank-deficient slices are retries, NOT
proof that the original nonlinear problem has no solution.

## Why A Larger Extension-Linear Flat Cannot Fix The Remaining Range

There is also a sharp bound on this mechanism's E-linear search space.
Let C be ANY nonzero E-linear subspace on which the r diagonal norm forms
vanish, not necessarily a GRS code. Put a_i=h_(c_i)*b_i and
T=diag(c_i). Norm polarization, including multiplication by theta, gives

    C orthogonal to T^j C for 0<=j<r

under the nondegenerate Hermitian form sum_i a_i*u_i*bar(v_i).
Restrict to C's support S. Let V_j=C+TC+...+T^j C. If V_(j+1)=V_j, then
V_j is T-invariant. Since T has distinct base-field eigenvalues, all its
invariant E-subspaces are coordinate subspaces; V_j must then be E^S.
That is incompatible with nonzero C being orthogonal to V_j.

Hence dim_E V_(r-1)>=dim_E C+r-1, whereas orthogonality implies
dim_E V_(r-1)<=|S|-dim_E C. Thus

    2 dim_E C + r - 1 <= |S| <= M.

Our choice k=floor((M-r+1)/2) attains this maximum. Searching for larger
E-linear norm flats cannot cross the failed D>=r gate. This bound does
NOT cover arbitrary F_p-linear flats lacking theta-closure, nonlinear
parameterizations, adaptive target selection, or other classical methods.
It is a local unreviewed deduction, not a general classical lower bound.

## Adversarial Checks And Limitations

- Exact basis and all polarized-pair checks verify cancellation, not just
  sampled norms. A broken norm scaling destroys the checked identity.
- On p19,M6,n15, all381 projective dual vectors give derivative rank D4.
  This verifies the finite probability-proof interface, not the theorem
  for arbitrary parameters.
- A rank-deficient center is deliberately constructed by solving one dual
  annihilation system. It must return RETRY_RANK. A separate ordinary run
  solves the SAME native input. Repeated bad centers are retained/counted.
- Nonconsecutive orbit subsets and adversarial fixed halfsets test that the
  construction did not secretly use full-field sums or random target data.
- The native large witness uses the same first684 author tables and
  multipliers as the resident cubic example, but explicitly changes n204
  to n1710. It is NOT a solution to the old n204 optimization task.
- The algorithm outputs a biased witness. It is not a uniform sampler,
  nor a refutation of a correct quantum lower bound on expected score.
- A defect in parity weights, conjugation, global cancellation, or the
  fixed-lambda rank proof would invalidate the claimed classical bound.
  Independent mathematical review is still needed; the Rees reviewer was
  not reused and reviewed no part of this result.

## Resources And Prior Art

The source table input is O(Mp). Norm scalings, actual parity checks, dense
matrices of polynomial size, exact rank/solve operations, interpolation,
and full native replay are paid. Their field-operation and bit costs are
polynomial; the reference's counters are named operations, not a full
certified complexity or quantum wall-time comparison. Failed centers
consume 2M random field draws and a full matrix/rank computation each.

Known ingredients are not discoveries here: low-dimensional products of
GRS codes are standard, for example in
[Couvreur et al.](https://arxiv.org/html/1307.6458v2). Solving quadratic
systems by fixing a complementary component and exploiting a quadratic-zero
subspace is the established oil-and-vinegar mechanism; see
[Kipnis, Patarin and Goubin](https://static.aminer.org/pdf/PDF/000/193/175/unbalanced_oil_and_vinegar_signature_schemes.pdf).
The existing general diagonal-system algorithm of
[Ivanyos and Santha](https://arxiv.org/abs/1503.09016) has different variable
thresholds and is not used as a black-box constant-ratio solver here.
No publication novelty is claimed from this limited comparison.

The earlier repository moment-mask/norm-pencil attack is different: it
uses reserved variables to approach an IID shifted OPI population. This
attack uses a concrete common norm subspace and a direct EVERY-input
random-center rank bound on the original cubic-orbit task. Neither the
general idea of norm methods nor the earlier exact MQ encoding is new.

## Next Scientific Question

The main saved rate0.8 case remains outside the proven classical region.
Do not repeat a generic MQ timeout campaign or a search for larger
E-linear flats. A productive continuation must exploit genuinely F_p-linear
non-E-linear structure, nonlinear norm fibers, target flexibility, or
derive a meaningful natural-problem reduction for the surviving quantum
range. Wider fields or more favorable high-rate seeds cannot establish
an advantage.
