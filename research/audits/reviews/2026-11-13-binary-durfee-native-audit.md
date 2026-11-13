# Compact binary Frobenius input: a charged Kronecker coefficient compiler

2026-11-13. Independent whole-composition audit of
`KRONECKER_BINARY_DURFEE_COMPILER.md`. Fresh STATE/TRAPS and the actual
primary excerpts in `api_inputs/2026-11-13-binary-durfee/actual-sources.txt`
were read; the retained Pragacz factorization and Barvinok--Pommersheim
Theorem 4.4/Algorithm 5.2 were also read in their full local text.
No network, API, Git, subagent, finite control or live paid report was used.

**Disposition:** the proposed binary-input algorithm is sound. For fixed
positive d,e, it computes ordinary g(lambda,mu,nu) exactly in deterministic
poly_(d,e)(L) BIT time from compact binary Frobenius coordinates of total
length L, whenever Durfee(lambda)<=d and Durfee(mu)<=e. Counting is supplied
by an actual fixed-dimensional polynomial-time algorithm, not an oracle.
This is a new proof obligation beyond the previously checked numerical-n
compiler; the dense numerical-n grid is not used. No priority, novelty,
growing-Durfee or full-ratio-promise conclusion is drawn.

## 1. Native input and fixed structural sizes

Validate strictly decreasing nonnegative arm and leg arrays of equal length.
Their partition size is the binary sum of all arms, all legs, and that length.
Unequal input sizes give coefficient zero. If n=0, the sole coefficient is one.
Assume henceforth n>0 and put
    a=Durfee(lambda), b=Durfee(mu), c=Durfee(nu).
Then 1<=a<=d, 1<=b<=e. Let lambda's coordinates be (alpha|beta), mu's
(gamma|delta), and nu's (r|s). No numerical-length row list is reconstructed.

Use X=(x_1,...,x_a | y_1,...,y_a) and Z=(u_1,...,u_b | v_1,...,v_b), with
    p_l(X)=sum x_i^l+(-1)^(l-1)sum y_j^l.
The tensor alphabet T has 2ab even letters xu,yv and 2ab odd letters xv,yu.
The already proved Frobenius-character identity is

    F=hs_nu(T)=sum_(rho,sigma partition n)
                  g(rho,sigma,nu) hs_rho(X)hs_sigma(Z).                (1)

It is an algebraic identity, not an algorithm enumerating this sum.
Hook vanishing leaves only (a,a)- and (b,b)-hook shapes. If c>2ab, F=0 by
the (2ab,2ab)-hook vanishing of hs_nu(T), and independence of the surviving
product basis implies the desired g=0. This early exit is polynomial in L.
Otherwise c<=2ab is fixed, as needed for the remaining compiler.

## 2. Exact super-Weyl extraction, including smaller Durfee terms

Set Q_X=product_(i,j)(x_i+y_j), and define Q_Z analogously. Use
    Delta(x)=product_(i<j)(x_i-x_j),
and the same orientation for y,u,v. Expand

    Q_X^-1=product_i x_i^(-a)
               product_(i,j) sum_(k>=0)(-y_j/x_i)^k,                 (2)

and similarly Q_Z^-1 in v/u. Then the proposed coefficient is exactly

    g(lambda,mu,nu)
      =[x^alpha y^beta u^gamma v^delta]
         F Delta(x)Delta(y)Delta(u)Delta(v)/(Q_X Q_Z).                (3)

Here is a full check that (3) isolates the target. For a surviving rho of
Durfee EXACTLY a, let eta_i=rho_i-a and theta_j=rho'_j-a for i,j<=a.
The rectangular hook factorization is
    hs_rho(X)=Q_X s_eta(x)s_theta(y).
This is the supplied primary Pragacz factorization (9), translated from
its ascending-partition/difference-alphabet convention by B=-y; the tail
partition transposes under the resulting odd specialization.
After Q_X cancels, the two Weyl alternants have exponent lists
    rho_i-i and rho'_j-j.
Both lists are strictly decreasing and nonnegative. The target lists alpha,
beta therefore occur only for rho=lambda, and only in the identity term of
each alternant, with coefficient +1. There is no factorial multiplicity.

If instead Durfee(rho)<a, then rho_a<a, with zero padding understood. Use
the independently checked Cauchy--Binet formula
    hs_rho(X)=sum_(kappa subset rho) s_kappa(x)s_(rho'/kappa')(y).
Only kappa with at most a rows survive. Every such kappa has kappa_a<a.
Each monomial of Delta(x)s_kappa(x) has an exponent equal to kappa_a in
some x variable. In (2), EVERY x exponent first decreases by a and then
can only decrease further. Thus every resulting monomial has at least one
negative x exponent. Multiplication by Delta(y) cannot change this fact.
It cannot match the nonnegative target alpha. The identical argument
excludes every smaller-Durfee sigma through a negative u exponent.

Coefficient extraction in the disjoint alphabets consequently kills all
terms of (1) except the target, proving (3). These theoretical identities
are finite in each degree; no basis enumeration enters the computation.

## 3. Constant-size rational expression for F

Giambelli in Frobenius coordinates, as stated in the retained actual primary,
gives
    hs_nu(T)=det(hs_(r_i+1,1^(s_j))(T))_(1<=i,j<=c).
Expand its c! determinant terms, a constant depending only on d,e.
For a selected permutation pi, give hook i PRIVATE auxiliary variables
t_i,w_i and extract t_i^(r_i) w_i^(s_pi(i)). The hook generating identity is

    sum_(r,s>=0) hs_(r+1,1^s)(T)t^r w^s
       =(H_T(t)E_T(w)-1)/(t+w),
    H_T(t)=product_(o odd)(1+o t)/product_(e even)(1-e t),
    E_T(w)=product_(e even)(1+e w)/product_(o odd)(1-o w).             (4)

For the desired nonnegative r,s, replace the numerator by H_T(t)E_T(w)
and expand
    (t+w)^-1=t^-1 sum_(j>=0)(-w/t)^j.
The coefficient becomes sum_(j=0)^s (-1)^j h_(r+j+1)e_(s-j), which is the
usual hook Jacobi--Trudi identity. The discarded 1/(t+w) has only negative
t powers. Because each hook has its OWN t_i,w_i, no other factor can repair
such a negative t_i exponent. Dropping those subtracted terms is valid
even after multiplying all c hook factors.

Expand only the four Vandermondes, the c! permutations, and the constant
numerators in (4). Each resulting term has known sign and the form

    z^h product_(ell=1)^D (1-epsilon_ell z^(v_ell))^-1,              (5)

in the 2a+2b+2c physical/auxiliary variables. The numerator shift h has
fixed-size exponents; binary input arms/legs occur only in the target.
Each epsilon is +/-1. There are

    D=a^2+b^2+c(4ab+1)
      <=d^2+e^2+8d^2e^2+2de                             (6)

geometric indices: a^2+b^2 from Q_X,Q_Z, and for each hook 2ab H-denominator
indices, 2ab E-denominator indices and one w_i/t_i index.
Only the Q indices and the c ratio indices carry a negative geometric sign.
The number of numerator/determinant terms is bounded by
c!(a!b!)^2 2^(4abc), hence is a fixed constant. Duplicate monomials may
simply be kept as separate signed terms.

## 4. One formal chamber and a finite box BEFORE cancellations

There is a common formal-series completion for every term in (5). Assign
weights x_i=u_j=t_h=1 and y_i=v_j=w_h=2. All geometric ratios have strictly
POSITIVE weight: y/x,v/u,w/t have weight 1; even-letter*t has weight 3 or 5;
odd-letter*w has weight 5. Consequently the generated exponent semigroup
is pointed, and every fixed Laurent coefficient receives only finitely many
terms. Polynomial identities and inverse cancellations hold in this common
completion. No analytic convergence region or ambiguous infinite sum is used.

The coefficient equations give the stronger uniform box 0<=k_ell<=n.
For each hook i, let j_i be its w_i/t_i index. Its w_i equation is
    j_i + sum E-denominator indices + numerator w_i degree = s_pi(i).
Every summand is nonnegative. Thus j_i and each E-index are at most n.
Its t_i equation is
    sum H-denominator indices = r_i+j_i+1-numerator t_i degree,
so each H-index is at most r_i+s_pi(i)+1. Even OFF-DIAGONAL hooks satisfy
    r_i+s_j+1 <= sum_h(r_h+s_h)+1=n-c+1<=n.              (7)

Every Q_X index increases one y_j exponent. All other sources of y_j have
nonnegative exponent: tensor letters, numerators and Delta(y). There is
no negative y source. Hence each such index is at most the target beta_j<=n.
The same argument bounds Q_Z indices by target delta_j<=n. Negative
x,u,t shifts cannot generate an unbounded cycle or evade these equations.
If any equation has a negative required nonnegative sum, the term contributes
zero. The bounds hold TERM BY TERM, before signed cancellation. A larger
2n+O_(d,e)(1) box would also be safe but is unnecessary.

## 5. Exact signed coefficients as bounded integer-point counts

For each term (5), write its matching equations as
    A k=b0,  0<=k<=n,
where columns of A are v_ell and b0 is target minus h. The matrix has at
most 2a+2b+2c rows and D columns, with entries in {-1,0,1}. The right side
has O(L) bits. The coefficient is the sum of product epsilon_ell^(k_ell)
over these integer solutions, times the term's fixed sign.

Enumerate parity for the a^2+b^2+c signed indices only, a constant number
of branches. For a signed index use k=2z+eta, eta in {0,1}; leave unsigned
indices as k=z. Its sign is now the known (-1)^(sum eta). Bounds become
0<=z<=floor((n-eta)/2) or 0<=z<=n. Each branch is an explicit bounded rational
polytope in at most D variables, described by fixed-many integer equalities
and inequalities. Equalities may be entered as two inequalities. This does
not assume full-dimensionality, generic position, or interior integer points.

The actual charged classical backend is Barvinok--Pommersheim Theorem 4.4
and Algorithm 5.2. The source measures binary facet-description length
(LF155--174) and states the algorithm for rational polyhedra/polytopes in
fixed AMBIENT dimension, including these lower-dimensional bounded cases.
Theorem 4.4, LF936--964, constructs a polynomial-size signed unimodular
generating-function decomposition in L^(O(D)) time; it is not supplied advice.
An empty polytope returns zero. Algorithm 5.2, LF1056--1105, then counts
integer points by the value at one, with the apparent poles canceled.

More explicitly, take the constructed fractions z^a/prod_j(1-z^(b_j)).
Choose an integer moment-curve vector ell avoiding all finitely many
ell.b_j=0, by scanning the source's polynomial-size candidate list. Substitute
z_h=exp(t ell_h). For each fraction compute the coefficient of t^D in
    t^D exp(t ell.a)/prod_j(1-exp(t ell.b_j)),
then sum with its sign. This is its Laurent constant term. It uses exact
Taylor arithmetic to FIXED degree D, with the denominator leading signs
retained; no numerical exponentials or precision oracle are necessary.
This direct Taylor prescription also avoids relying on a copied Todd-polynomial
sign convention. Exponents, moment-curve entries, and rational intermediate
bits are polynomial in L by the source decomposition and the fixed-degree
arithmetic. A polynomial number of rational summands still has polynomial
aggregate denominator length. This pays the count, not just its access model.

## 6. Whole clock, output size and scope

Generate the alphabets, numerator terms, permutations, geometric vectors and
parity branches explicitly from a,b,c. All list sizes and ambient dimensions
are bounded functions of the FIXED d,e; nothing depends on numerical n.
Only the target coordinates, offsets and box bounds contain binary input
integers. Their sizes are O_(d,e)(L), and their construction uses polynomial
binary arithmetic. No hidden n-step recurrence or dense coefficient array
occurs. The number of calls to the counting algorithm is fixed in d,e.

Each count is at most (n+1)^D. Including all fixed-many signs and numerator
branches, the output and accumulated signed integers have
O_(d,e)(log(n+1)) bits, bounded by O_(d,e)(L). Internal count arithmetic was
paid separately above. Thus the complete uniform algorithm has a deterministic
poly_(d,e)(L) BIT clock, including exact output. This is not a free lattice-point
or coefficient oracle and requires no precomputed chambers or selected roots.

All legal compact Frobenius inputs are covered: validation, n=0, unequal
sizes, c>2ab, empty counting branches and boundary/lower-dimensional polytopes.
The conclusion does NOT extend to growing Durfee bounds, arbitrary succinct
partitions without the two fixed bounds, the full quantum dimension-ratio
promise, practical runtime, hardness, or novelty. The supplied primary
open-problem passage and priority remain separate from this checked algebraic
and charged classical computation theorem.
