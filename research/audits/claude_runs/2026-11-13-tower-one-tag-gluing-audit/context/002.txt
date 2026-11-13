# Sparse support for feasible gluing — independent proof, 2026-11-13

**Accepted.** A feasible system of ell original squareclass-linear conditions
has a representative using at most c+ell odd primes from the auxiliary pool,
where c=dim_F2 Cl(O_K,S)/2. Neither this class group nor its generators need
be computed. A sharper bound is an explicit matrix rank computed below.
The weighted reset then gives the stated pool-cardinality-independent OUTPUT
height. Construction of the pool and of the complete source remains charged.

This is an independent proof of the parent's construction, not a finding
ascribed to the EMPTY sparse-gluing report. No API, network, Git, numerical
control or new implementation was used. Current STATE was read; the stable
weighted/divisor-reset proofs and their inspected actual LLL source are reused.

## 1. Contract and exact parity cokernel

Let K have degree n and discriminant Delta=|disc K|. Let S be a finite set
of finite K-primes, and let Q={P_1,...,P_m} be distinct primes disjoint from S,
with N(P_i)<=X, X>=1. Remove duplicates or S-primes before forming Q.
Assume a COMPLETE expanded generating family (in particular a basis suffices)
for
  E=K(S union Q,2)
is available. Its construction is not a free oracle supplied by this proof.
Let
  pi:E -> F_2^m
be the outside-S parity vector, and let
  phi:E -> F_2^ell
be the original Hilbert-symbol/sign rows. These must be homomorphisms on
squareclasses. The requested target v0 is feasible: v0 belongs to phi(E).
Without that premise, the algorithm detects inconsistency, not a gluing point.

Write C_S=Cl(O_K,S), and define
  kappa:F_2^m -> C_S/2C_S,
  q |-> [product_i P_i^q_i] mod 2C_S.
Then
  W=pi(E)=ker(kappa).                                        (1)
For one direction, the principal ideal of alpha in E differs from its parity
ideal by a square ideal, away from S. Conversely, if a parity ideal has class
in 2C_S, divide it by a suitable squared fractional ideal; the remaining
S-ideal class is principal, providing an alpha with exactly that outside-S
parity. This is an existence proof of (1), not principalization in the algorithm.

Thus
  c_Q:=m-dim W = dim image(kappa)
       <=dim C_S/2C_S = c <= log_2 h_K.                       (2)
The ordinary ideal class group is the correct one here: signs have not been
restricted in forming W. The additional real-sign conditions are included
in phi below. No narrow-class premise is silently needed.

## 2. Sparse feasible parity by Gaussian elimination

Form the image
  Z=image(E --(pi,phi)--> F_2^m x F_2^ell).
The known source generators supply its columns explicitly. Since projection
of Z to the first factor is W,
  codim Z = m+ell-dim Z <= c_Q+ell.                           (3)
Compute a basis of its annihilator, as rows of
  M=[M_Q | M_v].
Then (q,v0) belongs to Z exactly when
  M_Q q = M_v v0.                                           (4)
The right side lies in image(M_Q) by feasibility. Select a basis of pivot
COLUMNS of M_Q. Express M_v v0 in those columns and set all other q entries
to zero. This gives
  weight(q) <= rho:=rank(M_Q) <= c_Q+ell <= c+ell.             (5)
Also rho<=m. A rank-zero system is handled in the same way, giving q=0.
It is not necessary to find a minimum-weight solution of a general binary
system: a rank-supported solution already proves the required bound.

Recover a source coefficient vector z by solving the image-column system
  (pi,phi)(product_j e_j^z_j)=(q,v0).
Set alpha=product_j e_j^z_j. All operations here are exact binary linear
algebra, polynomial in the explicit matrix dimensions and source encoding.
The algorithm computes c_Q and rho from its matrices; it never computes C_S.
Dependent source generators cause no problem, provided they span ALL E.
An incomplete list can invalidate (1) and the bound, even if every returned
alpha is valid. Completeness is an essential premise.

## 3. The output height, after the paid squareclass reset

Put J=product_P P^(v_P(alpha) mod 2), the integral squarefree parity ideal.
Unused pool primes have even valuation, so
  N(J) <= N(rad S) product_(i:q_i=1) N(P_i)
       <= N(rad S) X^rho.                                   (6)
Apply the stable weighted-LLL reset to alpha in
K(S union supp(q),2). It returns an integral beta=alpha gamma^2 with
  max_sigma |sigma(beta)|
    <=3*2^((n-1)/2) (Delta*N(rad S)*X^rho)^(1/n).             (7)
Every parity row and every original Hilbert/sign row is unchanged. In
particular beta still has phi(beta)=v0. At real places a nonzero square is
positive, and Hilbert symbols are unchanged by squares.

With all logarithms in base 2, (7) gives the explicit bound
  log max_sigma |sigma(beta)|
    <= log 3 +(n-1)/2 + (log Delta)/n
       +[log N(rad S)+rho log X]/n
    <= log 3 +(n-1)/2 + (log Delta)/n
       +[log N(rad S)+(c+ell)log X]/n.                       (8)
For an arbitrary supplied maximal-order integral basis Omega, let M>=1
bound all its conjugates. The trace-dual bound in the stable reset proof is
  max |coordinates_Omega(beta)|
    <= n^(2n) M^(2n-1) max_sigma |sigma(beta)|.               (9)
Thus ordinary expanded coordinate bits add only
2n log n+(2n-1)log M+O(1) to (8). The field/basis data is charged.

The source product alpha and its reset may have runtime depending on the
whole explicit source and pool, including |Q|. Multiplying the source
representatives has polynomial bit cost in their supplied expanded sizes;
integer factoring and the prescribed Gram precision are paid as in the
stable reset. The conclusion is an OUTPUT-height bound without |Q| in (8),
not a claim that one can read or build an arbitrarily large pool for free.
Beta may have NEW EVEN valuations outside S union supp(q); these do not
invalidate (6), its squareclass, or the gluing conditions.

## 4. A computable bound without class-number advice

The small-ideal reset supplies an elementary proof-only bound for c. Let
  b=n^2+2n+ceil(log_2 Delta).
Every ideal class has an integral representative of norm at most 2^b:
apply that reset to any ideal representative. An integral ideal of index
at most 2^b has an HNF matrix whose entries are at most 2^b. Therefore
  h_K <= (2^b+1)^(n(n+1)/2),
  c <= c_bar:=(b+1)*n*(n+1)/2.                              (10)
No such ideals or classes are enumerated. Use c_bar in (8) for a purely
native predetermined bound, or the stronger actually computed rho in (7).
For the standard four-variable gluing conditions, at most two Hilbert rows
per original finite prime and one sign row per real place give
  ell<=2|S|+r_1.
The lemma itself works for any explicitly given squareclass-linear rows.

A complete tagged U_K(S;P_1,...,P_m) output can replace a separately built E.
Its labels give the exact parity columns. Because the targets are distinct
individual prime-unit vectors, forgetting the label is an isomorphism onto
E: every class in E has a unique parity vector. This does not make the
complete U source or its |Q|-dependent work free.

## 5. What this does and does not settle

The linear algebra does not require the primes in Q to split. For the
intended conic gluing application, their splitting in the relevant quadratic
extensions is what makes the NEW-prime Hilbert conditions automatic; all
dyadic/coefficient-bad primes must already be accounted for in S. This proof
does not create that split pool, certify a small X, or prove feasibility.
Those must come from the separately checked pool/local-global argument.

The result removes the whole pool cardinality from the final odd-support
and height bounds. It does not by itself make the height map affine with a
constant independent of input. For example, if ell=O(H) while X is polynomial
in a current bit-height H, the displayed estimate may still contain H log H.
Iterating such a bound is not automatically a polynomial original-input
clock. This is a limitation of the established bound, not an algorithm lower
bound. No complete coupled conic/U algorithm is claimed.

Accepted precisely: (1)–(10), constructive sparse selection, preservation of
all original conditions, and the finite-bit reset at the supplied complete-
source/feasible-pool interface. Novelty, a new quantum advantage, and any
finding from the EMPTY paid report remain unclaimed.
