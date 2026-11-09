# Exact cubic-space axis list for one full-weight Pauli rotation

Date: 2026-11-06. Independent proposed derivation; all-n review pending.
This note proves a classical algebraic operation GIVEN the exact cubic
vanishing space of the stated Bell support. The parent owns the separate
native Bell-law/support-gap proof and product-learning source audit.
No new source law, general cubic decoder, uniqueness of the rotation axis,
or quantum advantage follows from this note or its finite control.

## 1. Input and output of the algebraic operation

Let V=F_2^(2n) have its known nondegenerate alternating form omega, and
write the canonical coordinates as (x_1,...,x_n,z_1,...,z_n). Put

    q=sum_i x_i z_i,   ell=sum_i x_i,   p=(0,1^n),
    B={v: x_i z_i=0 for every i},
    S=(B union (B+p)) intersect {q=0}.

The input is the EXACT degree-at-most-three Boolean vanishing space K3
of an affine symplectic image g(S), g(v)=Fv+t. Boolean polynomials use
unique squarefree algebraic normal form, x_i^2=x_i. Numerical n is charged.

For every n>=4 there is a polynomial-time, polynomial-space classical
operation returning precisely n+1 nonzero vectors

    {F z_1,...,F z_n,F p},

where z_i denotes the i-th canonical z-direction. In particular the list
contains the conjugated rotation axis Fp. The affine displacement t is
unneeded. No uniqueness is asserted, and the procedure does not search
over an exponential family of matrices. The n<=3 cases are of bounded
Hilbert-space dimension and can be handled by ordinary tomography in an
approximate-preparation application.

## 2. The exact vanishing space, including its universal overlap

For fixed x, let A={i:x_i=1}. If A is empty, every z is allowed. If
|A| is odd, the active z_i must all be zero. If |A| is positive and even,
the active z_i are either all zero or all one. Inactive z_i are free.

For n>=3, every f in K3 has the form

    f=q*l + sum_{i<j} s_ij E_ij,
    E_ij=x_i x_j(z_i+z_j),   l affine linear.                 (1)

Here is a coefficient proof, not an assumption that the displayed ideal
generators exhaust K3. The points (x,0) and (0,z) kill all pure-x and
pure-z monomials, including constants. Using x=e_i with z_i=0 kills
all one-x terms except x_i z_i and x_i z_i z_j. Using x=e_i+e_j with
z_i=z_j=0 kills x_i x_j z_k for k outside {i,j}. Thus the only possible
terms are

    sum_i a_i x_i z_i
    +sum_{i!=j} b_ij x_i x_j z_i
    +sum_{i!=j} c_ij x_i z_i z_j.

Set x=e_i+e_j and z_i=z_j=t. For k outside {i,j}, the coefficient of
t z_k forces c_ik=c_jk. Hence c_ik=gamma_k for i!=k. The coefficient
of t forces

    b_ij+b_ji=a_i+a_j+gamma_i+gamma_j.                       (2)

These constraints suffice on all of S: odd active sets have active z=0;
on even active sets the displayed sums cancel using (2). Equivalently,
take l=sum_i(a_i+gamma_i)x_i+sum_i gamma_i z_i and then adjust each
symmetric b-pair by E_ij. This proves (1).

Consequently

    dim K3=2n+binom(n,2),   K2=<q>.

The parameterization q*Aff_1 plus E is NOT a direct sum. Its one overlap is

    sum_{i<j} E_ij=q*ell+q.                                 (3)

Let Q=sum_i x_i wedge z_i be the alternating quadratic top form, and let
W be the space of cubic top parts of K3. Then

    W=(Q wedge V*) + span{T_ij},
    T_ij=x_i wedge x_j wedge (z_i+z_j),
    dim W=2n+binom(n,2)-1.                                  (4)

The degree filtration of Boolean polynomials has exterior powers as its
associated graded over F_2. Thus affine translations affect only lower
terms, and under g(v)=Fv+t the top space is transported by the usual
exterior representation of F^{-1}. This is why the affine Bell shift
does not have to be recovered.

## 3. Compute an infinitesimal stabilizer by linear equations

Define

    L={M in sp(V,omega): D_M W subset W},

where D_M is the infinitesimal substitution action on exterior forms.
This is an explicitly computable VECTOR SPACE. For each basis matrix of
sp(V), act on a basis of W and project modulo W; nullspace computation
gives L. The matrix space sp(V) has dimension n(2n+1), the ambient exterior
cube has dimension binom(2n,3), and W has O(n^2) dimensions. All matrices
have polynomial dimensions. No algebraic-group enumeration is performed.

In canonical coordinates write a symplectic infinitesimal matrix as

    M=[ A  B ; C  A^t ],   B=B^t, C=C^t.

The uniform classification, for EVERY n>=4, is

    L={a I_(2n)+N_D:
           a in F_2, N_D=[0 0; D 0],
           D=diag(c_1,...,c_n)+b*11^t}.                    (5)

In particular dim L=n+2. There is no n-parity exception.

Proof. Every symplectic infinitesimal matrix preserves Q, so it preserves
Q wedge V*. It remains to test each T_ij. Decompose exterior cubics by
their numbers of x and z factors; the three blocks below cannot cancel
one another.

* The C block gives the pure-x cube
  x_i wedge x_j wedge sum_k(C_ik+C_jk)x_k. W has no pure-x component.
  Thus C_ik=C_jk for distinct i,j,k. Each off-diagonal column is constant;
  symmetry makes all these constants the same b. The diagonal is free.

* The B block gives an x z^2 form with x support confined to {i,j}.
  The entire x z^2 component of W is Q wedge Z*. If such a form equals
  Q wedge zeta, every outside index k forces z_k wedge zeta=0. There
  are TWO outside indices when n>=4, so zeta=0. Hence D_B T_ij=0.
  Its three-distinct-index coefficients first force all off-diagonal
  B_ik=0. The remaining coefficients at x_j z_i z_j and x_i z_i z_j
  force B_ii=B_jj=0. Therefore B=0.

* The A block gives an x^2 z form. W contains no monomial x_j x_k z_i
  with three distinct indices. In D_A T_ij its coefficient is A_ik,
  so A is diagonal. Write its diagonal entries a_i. Then
  D_A T_ij=a_j x_i x_j z_i+a_i x_i x_j z_j.
  In the x^2 z component of W, the sums of the two oriented coefficients
  on each pair have the form u_i+u_j; equivalently their sum around every
  triangle is zero. The displayed form has only the (i,j) pair nonzero,
  with value a_i+a_j. A triangle containing an outside index forces
  a_i=a_j. Thus A=a I.

Conversely, a scalar matrix acts on exterior cubics by that scalar, while
the allowed C matrices act trivially on every T_ij. This proves (5).

The first tempting shortcut FAILS: L is abelian, so its commutator algebra
cannot single out p. The saved n=4 control witnesses this specific failure;
the classification above proves it uniformly. The next steps use the
square-zero part and its rank-one elements instead.

## 4. Intrinsic square-zero part and its Lagrangian support

In (5), all N_D N_E=0 and all elements commute. Therefore

    (a I+N_D)^2=a I.

Over F_2 the square map on this commuting space is LINEAR. Compute each
basis matrix's square and take their linear kernel. This produces

    N={M in L:M^2=0},  dim N=n+1.                            (6)

This description is intrinsic and conjugation-equivariant. It is NOT a
generic assertion that matrix squaring is linear. Commutativity follows
from the proved promise classification; it can also be checked directly
on the computed basis.

Let U=intersection_{N in N} ker N, computable by stacking matrices.
Canonically U is the z-space: the diagonal D's already force x=0.
Thus U has dimension n, is Lagrangian, and is also the sum of all images
of matrices in N. Every N annihilates U and maps V into U. If desired,
symplectic Gaussian elimination chooses a Lagrangian complement and
identifies these maps with symmetric n-by-n matrices D. Such a choice is
paid linear algebra, not the unknown original Clifford frame.

There is a more intrinsic way to extract their diagonals. For N in N,
the function

    v -> omega(v,Nv)

is F_2-linear: symmetry of the bilinear form omega(v,Nw) cancels its
cross terms. Let lambda(N) be the unique vector satisfying

    omega(v,lambda(N))=omega(v,Nv) for all v.                (7)

It is computed by evaluating the right side on a basis of V and solving
with the known symplectic form. It lies in U and is linear in N. In a
symmetric D frame it is precisely the diagonal vector of D.

A matrix N in this space has rank at most one precisely when

    N(v)=omega(v,lambda(N))*lambda(N) for every v.            (8)

For a nonzero rank-one symplectic self-adjoint map, symmetry forces its
image vector and its defining covector to be symplectic duals; the only
nonzero scalar in F_2 is 1. This proves the forward direction. The reverse
direction and the zero case are immediate. Thus (8) yields explicit
Boolean QUADRATIC equations in the n+1 linear coordinates of N.

## 5. Polynomial extraction of all rank-one matrices

Let t_1,...,t_m, m=n+1, be coordinates in any computed basis of N. Form
all matrix-entry equations from (8), reducing them to squarefree Boolean
normal form. The following fixed degree-3 Macaulay calculation recovers
every solution without matrix search.

The proof is easiest in canonical coordinates, but they are NOT used by
the algorithm. Write

    D=diag(c)+b*11^t,   v=c+b*1=lambda(D).

The linear coordinates (v_1,...,v_n,b) are an invertible change from t.
Equation (8) is exactly

    v_i v_j+b=0 for every i<j.                              (9)

The diagonal equations are Boolean identities. The solutions of (9) are

    (v,b)=(0,0), (e_1,0),...,(e_n,0), (1,1).                (10)

There are n+2=m+1 solutions, and they are affinely independent in F_2^m.
The nonzero solutions correspond to D=e_i e_i^t and D=11^t. Their image
vectors are z_i and p. They need not be distinguished from one another.

Why degree THREE is sufficient uniformly: in the Boolean ring, multiplying
f_ij=v_i v_j+b by v_i and adding f_ij gives

    b v_i+b=0.                                             (11)

Thus (9) and (11) express EVERY quadratic monomial in the m variables as
an affine-linear function. There are binom(m,2) independent such relations,
one for each distinct-variable quadratic monomial. Because the m+1 points
in (10) are affinely independent, there are no nonzero affine relations,
and these are exactly all degree-at-most-two vanishing relations.

The algorithm is coordinate-independent:

1. Take the span M3 of the input quadratic equations and all their
   products by the variables t_k, with Boolean reduction. These have
   degree at most 3. A linear change to the unknown (v,b) coordinates
   preserves this space, so M3 contains (11).
2. Intersect M3 with polynomials of degree<=2 by eliminating the cubic
   coefficients. This gives the complete degree<=2 vanishing space just
   proved, not an assumed complete Groebner basis.
3. Solve its linear equations to express each t_i t_j in the basis
   1,t_1,...,t_m; use t_i^2=t_i. These are the multiplication tables of
   the m+1-dimensional coordinate algebra of (10), hence a direct product
   of m+1 copies of F_2. Associativity and completeness follow from the
   preceding affine interpolation argument.
4. Its multiplication matrices by t_i commute and are idempotent.
   Successively split joint eigenspaces into eigenvalues 0 and 1. After
   at most m such splits there are exactly m+1 one-dimensional joint
   eigenspaces, whose eigenvalue strings are every solution t.
5. Evaluate N(t), discard the zero matrix, and return lambda(N(t)).

The ambient Macaulay vector space has O(n^3) monomials and a polynomial
number of rows. All remaining algebras and matrices have O(n) dimension.
Every stage is ordinary finite-field linear algebra with a prescribed
polynomial termination bound. No search for an invertible D, minimum-rank
matrix, generic cubic factorization, or algebraic-extension point occurs.
In particular, parity-dependent singularity of I+11^t is irrelevant: this
matrix is never inverted.

## 6. Affine equivariance and learner interface

If the observed Bell support is g(S), the construction of W, its
infinitesimal stabilizer, the square-zero space, (7), and (8) transports
under the SYMPLECTIC linear part F. The output is therefore exactly
{Fz_1,...,Fz_n,Fp}; translations never enter the computation.

Conditional on obtaining the correct K3, this is a paid polynomial-size
candidate list containing the physical Pauli axis. Its Pauli sign is not
determined by binary labels. Try both rotation signs for every candidate
on fresh native copies. One branch undoes the actual rotation and is an
instance of the already sourced finite-H Clifford-product learner. Cap
all learner branches at that primitive's polynomial promise clock; a wrong
branch is not promised to return a valid product decomposition.

Reverse the proposed correction on each returned preparation and verify
against fresh original copies by SWAP tests, or by the returned preparation
circuit's inverse followed by the all-zero test. Allocate the approximation
and failure budgets across the polynomial number of candidates. A correct
branch supplies a good candidate; incorrect branches cannot force an
epsilon-inaccurate acceptance with the prescribed verification error.
This targets approximate preparation with polynomial cost in n,1/epsilon,
log(1/eta), NOT exact equality certification of arbitrary wrong branches,
recovery of the original Clifford, or uniqueness of p.

The separate proof obligations retained outside this note are the exact
native Bell law, the inverse-polynomial cubic support gap needed to learn
K3, the finite-H product learner's actual source/copy/time contract, and
the complete final error allocation. No finite rank experiment establishes
any of those gates.
